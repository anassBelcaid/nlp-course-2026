"""Small controlled SST-2 experiment; recorded evidence, never browser training.

Requires torch, transformers==4.57.6, pyarrow. Uses CPU and a pinned BERT-tiny.
256 training examples, 128 disjoint validation examples, 80 equal-budget steps,
3 fixed seeds, same classification head initialization and batches in each pair.
This is a classroom budget comparison, not a tuned benchmark or model ranking.
"""
import argparse, copy, hashlib, json, random
from pathlib import Path
import torch
from torch import nn
import torch.nn.functional as F
import pyarrow.parquet as pq
import transformers
from transformers import BertConfig, BertModel, BertTokenizer
from huggingface_hub import snapshot_download

MODEL='prajjwal1/bert-tiny'
REV='6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837'
DATA_REV='8d51e7e4887a4caaa95b3fbebbf53c0490b58bbb'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model-dir',type=Path)
    parser.add_argument('--data-dir',type=Path)
    parser.add_argument('--cache-dir',default='/tmp/nlp-section4-models')
    args=parser.parse_args()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    model_dir=args.model_dir or Path(snapshot_download(MODEL,revision=REV,cache_dir=args.cache_dir,allow_patterns=['config.json','vocab.txt','pytorch_model.bin']))
    data_dir=args.data_dir or Path(snapshot_download('stanfordnlp/sst2',repo_type='dataset',revision=DATA_REV,cache_dir=args.cache_dir,allow_patterns=['data/train-*.parquet','data/validation-*.parquet']))
    train_all=pq.read_table(next((data_dir/'data').glob('train-*.parquet'))).to_pylist()
    valid_all=pq.read_table(next((data_dir/'data').glob('validation-*.parquet'))).to_pylist()
    def balanced(rows,n,seed):
        rng=random.Random(seed); groups=[[r for r in rows if r['label']==i] for i in [0,1]]
        out=[]
        for group in groups: rng.shuffle(group);out+=group[:n]
        rng.shuffle(out);return out
    valid=balanced(valid_all,64,351)
    norm=lambda s:' '.join(s.lower().split())
    heldout={norm(r['sentence']) for r in valid}
    train=balanced([r for r in train_all if norm(r['sentence']) not in heldout],128,351)
    assert len(train)==256 and len(valid)==128
    tokenizer=BertTokenizer.from_pretrained(model_dir,local_files_only=True)
    def batch(rows):return tokenizer([r['sentence'] for r in rows],padding='max_length',truncation=True,max_length=64,return_tensors='pt')
    tx,vx=batch(train),batch(valid)
    ty=torch.tensor([r['label'] for r in train]);vy=torch.tensor([r['label'] for r in valid])
    cfg=BertConfig.from_pretrained(model_dir,local_files_only=True)
    # Disable dropout identically to make the small CPU experiment repeatable.
    cfg.hidden_dropout_prob=0.;cfg.attention_probs_dropout_prob=0.
    pretrained=BertModel.from_pretrained(model_dir,config=cfg,local_files_only=True,add_pooling_layer=False)
    class Classifier(nn.Module):
        def __init__(self,encoder,head):super().__init__();self.encoder=encoder;self.head=head
        def forward(self,x):return self.head(self.encoder(**x).last_hidden_state[:,0])
    results=[]
    for seed in [351,352,353]:
        torch.manual_seed(seed)
        head=nn.Linear(cfg.hidden_size,2)
        batches=[];g=torch.Generator().manual_seed(seed)
        for epoch in range(5):batches.extend(torch.randperm(256,generator=g).split(16))
        assert len(batches)==80
        for init in ['pretrained','random']:
            torch.manual_seed(seed)
            encoder=copy.deepcopy(pretrained) if init=='pretrained' else BertModel(cfg,add_pooling_layer=False)
            model=Classifier(encoder,copy.deepcopy(head))
            opt=torch.optim.AdamW(model.parameters(),lr=2e-4,weight_decay=.01)
            curve=[]
            def evaluate(step):
                model.eval()
                with torch.no_grad():
                    logits=torch.cat([model({k:v[i:i+32] for k,v in vx.items()}) for i in range(0,128,32)])
                    probs=logits.softmax(-1);pred=probs.argmax(-1)
                curve.append(dict(step=step,correct=int((pred==vy).sum()),accuracy=float((pred==vy).float().mean()),loss=float(F.cross_entropy(logits,vy))))
                return probs,pred
            probs,pred=evaluate(0)
            first_update=None
            for step,idx in enumerate(batches,1):
                model.train();opt.zero_grad()
                loss=F.cross_entropy(model({k:v[idx] for k,v in tx.items()}),ty[idx]);loss.backward()
                if step==1:
                    names=['encoder.embeddings.word_embeddings.weight','encoder.encoder.layer.0.attention.self.query.weight','head.weight']
                    saved={n:p.detach().clone() for n,p in model.named_parameters() if n in names}
                opt.step()
                if step==1:first_update={n:float((p.detach()-saved[n]).norm()) for n,p in model.named_parameters() if n in saved}
                if step in [10,20,40,80]:probs,pred=evaluate(step)
            assert all(v>0 for v in first_update.values())
            result=dict(seed=seed,initialization=init,curve=curve,first_step_parameter_changes=first_update,predictions=pred.tolist(),positive_probabilities=probs[:,1].tolist())
            results.append(result)
            print(json.dumps({k:result[k] for k in ['seed','initialization','curve']}),flush=True)
    weight=model_dir/'pytorch_model.bin'
    record=dict(model=MODEL,model_revision=REV,weight_sha256=hashlib.sha256(weight.read_bytes()).hexdigest(),data='stanfordnlp/sst2',data_revision=DATA_REV,torch=torch.__version__,transformers=transformers.__version__,device='CPU',protocol=dict(train_count=256,validation_count=128,max_length=64,steps=80,batch_size=16,optimizer='AdamW',learning_rate=2e-4,weight_decay=.01,dropout=0,seeds=[351,352,353],selection_seed=351,head='random linear head on final CLS state; pooler omitted',selection='balanced subsets; exact normalized train/validation overlaps removed before training selection',tuning='No hyperparameter search or checkpoint selection; report step 80 for all runs'),training_indices=[int(r['idx']) for r in train],validation=[dict(idx=int(r['idx']),label=int(r['label']),sentence=r['sentence']) for r in valid],results=results,limitations='Small fixed balanced subsets and one budget. Original validation is held out here; no tuning on it. Does not equal full SST-2, isolate pretraining data content, or establish optimal random-initialization performance. Pretraining compute is excluded from the matched downstream budget. Exact duplicate removal does not rule out related phrases or pretraining contamination.')
    out=Path(__file__).parent/'evidence'/'section4.json';out.write_text(json.dumps(record,indent=2)+'\n')
    print(out,flush=True)
if __name__=='__main__':main()
