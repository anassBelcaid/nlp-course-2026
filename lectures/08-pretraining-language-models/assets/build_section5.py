"""Record fixed-model interventions; retain all predeclared examples and failures.

Reconstruct Section 4 seed 351 pretrained-branch classifier and verify its full
held-out predictions against the saved evidence. Then freeze it for interventions.
Separately probe the original pinned BERT-tiny MLM with predeclared sentence pairs.
Requires torch, transformers==4.57.6, pyarrow; CPU; weights not published.
"""
import argparse, hashlib, json
from pathlib import Path
import torch
from torch import nn
import torch.nn.functional as F
import pyarrow.parquet as pq
import transformers
from transformers import BertConfig, BertModel, BertForMaskedLM, BertTokenizer
from huggingface_hub import snapshot_download

REV='6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837'
# Fixed before inference; not selected for a desirable outcome.
SENTIMENT=[('original','i loved this movie',1),('meaning change','i hated this movie',0),('typo','i lovde this movie',1),('negation','i did not love this movie',0)]
PAIRS={
 'syntax':dict(candidates=['is','are'],sentences=['the key to the cabinets [MASK] here.','the keys to the cabinets [MASK] here.'],expected=['is','are']),
 'context':dict(candidates=['bank','glass'],sentences=['she put money in the [MASK].','she put water in the [MASK].'],expected=['bank','glass']),
 'fact':dict(candidates=['paris'],sentences=['the capital of france is [MASK].','france has its capital in [MASK].'],expected=['paris','paris'])
}

def main():
 p=argparse.ArgumentParser();p.add_argument('--model-dir',type=Path);p.add_argument('--data-dir',type=Path);p.add_argument('--cache-dir',default='/tmp/nlp-section4-models');a=p.parse_args()
 torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
 root=Path(__file__).parent
 s4=json.loads((root/'evidence/section4.json').read_text())
 md=a.model_dir or Path(snapshot_download('prajjwal1/bert-tiny',revision=REV,cache_dir=a.cache_dir,allow_patterns=['config.json','vocab.txt','pytorch_model.bin']))
 dd=a.data_dir or Path(snapshot_download('stanfordnlp/sst2',repo_type='dataset',revision=s4['data_revision'],cache_dir=a.cache_dir,allow_patterns=['data/train-*.parquet']))
 rows=pq.read_table(next((dd/'data').glob('train-*.parquet'))).to_pylist();byid={int(r['idx']):r for r in rows};train=[byid[i] for i in s4['training_indices']]
 tok=BertTokenizer.from_pretrained(md,local_files_only=True)
 cfg=BertConfig.from_pretrained(md,local_files_only=True);cfg.hidden_dropout_prob=0.;cfg.attention_probs_dropout_prob=0.
 enc=BertModel.from_pretrained(md,config=cfg,local_files_only=True,add_pooling_layer=False)
 torch.manual_seed(351);head=nn.Linear(cfg.hidden_size,2)
 class Classifier(nn.Module):
  def __init__(self):super().__init__();self.encoder=enc;self.head=head
  def forward(self,x):return self.head(self.encoder(**x).last_hidden_state[:,0])
 model=Classifier()
 def tokenize(texts):return tok(texts,padding='max_length',max_length=64,truncation=True,return_tensors='pt')
 interventions=tokenize([x[1] for x in SENTIMENT]);tx=tokenize([r['sentence'] for r in train]);ty=torch.tensor([r['label'] for r in train])
 def inspect():
  model.eval()
  with torch.inference_mode():return model(interventions).softmax(-1)[:,1].tolist()
 before=inspect();g=torch.Generator().manual_seed(351);batches=[]
 for epoch in range(5):batches.extend(torch.randperm(256,generator=g).split(16))
 opt=torch.optim.AdamW(model.parameters(),lr=2e-4,weight_decay=.01)
 for idx in batches:
  model.train();opt.zero_grad();loss=F.cross_entropy(model({k:v[idx] for k,v in tx.items()}),ty[idx]);loss.backward();opt.step()
 after=inspect()
 vx=tokenize([r['sentence'] for r in s4['validation']]);model.eval()
 with torch.inference_mode():vp=torch.cat([model({k:v[i:i+32] for k,v in vx.items()}) for i in range(0,128,32)]).softmax(-1)[:,1]
 old=next(r for r in s4['results'] if r['seed']==351 and r['initialization']=='pretrained')
 assert torch.allclose(vp,torch.tensor(old['positive_probabilities']),atol=1e-6), 'Section 4 checkpoint reconstruction failed'
 digest=hashlib.sha256()
 for k,v in model.state_dict().items():digest.update(k.encode());digest.update(v.detach().cpu().numpy().tobytes())
 classifier=[]
 for i,(kind,sentence,gold) in enumerate(SENTIMENT):
  tokens=tok.tokenize(sentence);classifier.append(dict(kind=kind,sentence=sentence,expected_label=gold,tokens=tokens,ids=tok.convert_tokens_to_ids(tokens),before=before[i],after=after[i],prediction_before=int(before[i]>=.5),prediction_after=int(after[i]>=.5)))
 mlm,info=BertForMaskedLM.from_pretrained(md,local_files_only=True,output_loading_info=True);mlm.eval()
 assert not info['missing_keys'] and not info['mismatched_keys']
 groups={}
 for name,spec in PAIRS.items():
  rec=[]
  for sentence,expected in zip(spec['sentences'],spec['expected']):
   batch=tok(sentence,return_tensors='pt');positions=(batch['input_ids'][0]==tok.mask_token_id).nonzero().flatten();assert len(positions)==1
   with torch.inference_mode():prob=mlm(**batch).logits[0,positions[0]].softmax(-1)
   values,ids=prob.topk(5);cand=[]
   for word in spec['candidates']:
    ix=tok.encode(word,add_special_tokens=False);assert len(ix)==1
    cand.append(dict(token=word,id=ix[0],probability=float(prob[ix[0]]),rank=int((prob>prob[ix[0]]).sum())+1))
   rec.append(dict(sentence=sentence,expected=expected,tokens=tok.convert_ids_to_tokens(batch['input_ids'][0]),ids=batch['input_ids'][0].tolist(),mask_position=int(positions[0]),candidates=cand,top5=[dict(token=tok.convert_ids_to_tokens(int(i)),probability=float(v)) for v,i in zip(values,ids)]))
  groups[name]=rec
 out=dict(pretrained_model='prajjwal1/bert-tiny',revision=REV,pretrained_sha256=hashlib.sha256((md/'pytorch_model.bin').read_bytes()).hexdigest(),classifier_state_sha256=digest.hexdigest(),torch=torch.__version__,transformers=transformers.__version__,classifier_protocol='Exact reconstruction of Section 4 pretrained branch seed 351, step 80; held-out probability vector verified at atol 1e-6. Before is pretrained encoder plus random task head.',inference='CPU eval/inference_mode; no updates during interventions; MLM is original pretrained checkpoint, not sentiment model',classifier=classifier,mlm=groups,limitations='Four sentiment examples and three two-prompt MLM diagnostics, predeclared and unfiltered; not a benchmark or proof of semantics, robust syntax, factual grounding, or memorization. No candidate renormalization. Context target choices are illustrative plausible completions, not exclusive grammatical answers.')
 (root/'evidence/section5.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'classifier':classifier,'mlm':groups},indent=2),flush=True)
if __name__=='__main__':main()
