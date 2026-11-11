"""Record a single MLM prediction. No training or inference in the browser."""
import argparse
import hashlib
import json
from pathlib import Path
import torch
import transformers
from transformers import BertForMaskedLM, BertTokenizer

parser = argparse.ArgumentParser()
parser.add_argument('--model-dir', type=Path, required=True)
args = parser.parse_args()
torch.set_num_threads(2)
tokenizer = BertTokenizer.from_pretrained(args.model_dir, local_files_only=True)
model, info = BertForMaskedLM.from_pretrained(
    args.model_dir, local_files_only=True, output_loading_info=True)
assert not info['missing_keys'] and not info['mismatched_keys'] and not info['error_msgs']
model.eval()
source = 'she put money in the bank yesterday.'
masked = source.replace('bank', '[MASK]')
batch = tokenizer(masked, return_tensors='pt')
position = int((batch['input_ids'][0] == tokenizer.mask_token_id).nonzero().item())
target = tokenizer.convert_tokens_to_ids('bank')
with torch.inference_mode():
    logits = model(**batch).logits[0, position]
    probabilities = logits.softmax(-1)
    values, indices = probabilities.topk(5)
    loss = float(-logits.log_softmax(-1)[target])
assert torch.isfinite(probabilities).all()
assert abs(float(probabilities.sum()) - 1) < 1e-5
record = dict(
    model='prajjwal1/bert-tiny', revision=args.model_dir.name,
    weight_sha256=hashlib.sha256((args.model_dir/'pytorch_model.bin').read_bytes()).hexdigest(),
    torch=torch.__version__, transformers=transformers.__version__,
    mode='CPU; eval; no training', source=source, input=masked,
    tokens=tokenizer.convert_ids_to_tokens(batch['input_ids'][0]),
    ids=batch['input_ids'][0].tolist(), position=position, target='bank', target_id=target,
    vocabulary_size=len(probabilities),
    top5=[dict(token=tokenizer.convert_ids_to_tokens(int(i)), probability=float(v))
          for v, i in zip(values, indices)],
    target_probability=float(probabilities[target]), target_nll=loss,
    target_rank=int((probabilities > probabilities[target]).sum()) + 1,
    loading_info=info,
    protocol='Reuse the section-1 closing sentence; retain all top-five outputs, including failure. '
             'Full-vocabulary softmax, no renormalization over displayed candidates.')
out = Path(__file__).parent / 'evidence' / 'section2.json'
out.write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
