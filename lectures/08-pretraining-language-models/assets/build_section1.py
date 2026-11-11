"""Record real representations/tokenization; rendering and browsing never infer.

Run with torch and transformers==4.57.6. Model cache defaults to /tmp.
No training; no selection among outputs. See README.md for the protocol.
"""
import argparse
import hashlib
import json
from pathlib import Path

import torch
import transformers
from huggingface_hub import snapshot_download
from transformers import BertModel, BertTokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=Path)
    parser.add_argument('--cache-dir', default='/tmp/nlp-pretraining-models')
    args = parser.parse_args()
    torch.set_num_threads(2)
    torch.manual_seed(43)
    model_id = 'prajjwal1/bert-tiny'
    path = args.model_dir or Path(snapshot_download(
        model_id, revision='6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837', cache_dir=args.cache_dir,
        allow_patterns=['config.json', 'vocab.txt', 'pytorch_model.bin']))
    tokenizer = BertTokenizer.from_pretrained(path, local_files_only=True)
    model = BertModel.from_pretrained(path, local_files_only=True).eval()
    records = []
    # Fixed hand-authored examples, selected before inspecting representations.
    for name, sentence in [('Money', 'she put money in the bank.'),
                           ('Water', 'she saw water by the bank.')]:
        batch = tokenizer(sentence, return_tensors='pt')
        tokens = tokenizer.convert_ids_to_tokens(batch['input_ids'][0])
        pos = tokens.index('bank')
        with torch.inference_mode():
            lookup = model.get_input_embeddings()(batch['input_ids'])[0, pos]
            contextual = model(**batch).last_hidden_state[0, pos]
        records.append(dict(name=name, sentence=sentence, tokens=tokens,
                            ids=batch['input_ids'][0].tolist(), position=pos,
                            lookup=lookup.tolist(), contextual=contextual.tolist()))
    a, b = records
    assert a['position'] == b['position'] and a['lookup'] == b['lookup']
    assert a['contextual'] != b['contextual']
    similarity = float(torch.nn.functional.cosine_similarity(
        torch.tensor(a['contextual']), torch.tensor(b['contextual']), dim=0))
    spelling = []
    for label, word in [('Familiar', 'learning'), ('New form', 'relearning'),
                        ('Typo', 'laerning')]:
        pieces = tokenizer.tokenize(word)
        assert '[UNK]' not in pieces
        assert ''.join(pieces).replace('##', '') == word
        spelling.append(dict(label=label, word=word, tokens=pieces,
                             ids=tokenizer.convert_tokens_to_ids(pieces)))
    weight = path / 'pytorch_model.bin'
    corpus = ['the cat sat on the mat', 'the dog slept by the door',
              'the child read a good book']
    examples = []
    for row, sentence in enumerate(corpus):
        words = sentence.split()
        for position, target in enumerate(words):
            context = words.copy()
            context[position] = '____'
            examples.append(dict(row=row, position=position,
                                 context=context, target=target))
    assert len(examples) == 18
    evidence = dict(
        model=model_id, revision=path.name,
        weight_sha256=hashlib.sha256(weight.read_bytes()).hexdigest(),
        vocab_sha256=hashlib.sha256((path/'vocab.txt').read_bytes()).hexdigest(),
        torch=torch.__version__, transformers=transformers.__version__,
        mode='eval; CPU; no training; no gradients',
        dimension=model.config.hidden_size, layers=model.config.num_hidden_layers,
        corpus=corpus, examples=examples, records=records, spelling=spelling,
        contextual_cosine=similarity,
        limitations='Two authored contexts; different vectors alone do not prove sense understanding. '
                     'The 18 corpus examples enumerate toy whitespace positions, not BERT masking. '
                     'Tokenization represents the typo without correcting it.')
    for record in records:
        assert torch.isfinite(torch.tensor(record['contextual'])).all()
    out = Path(__file__).parent/'evidence'/'section1.json'
    out.write_text(json.dumps(evidence, indent=2)+'\n')
    print(json.dumps({'output': str(out), 'revision': path.name,
                      'contextual_cosine': similarity, 'spelling': spelling}))


if __name__ == '__main__':
    main()
