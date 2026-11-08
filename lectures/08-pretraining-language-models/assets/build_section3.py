"""One actual CPU SGD step per tiny, randomly initialized Transformer recipe.

Teaching experiment, not BERT/GPT/T5 checkpoints or a performance comparison.
Requires PyTorch. Fixed word vocabulary; all examples and outputs retained.
"""
import json
from pathlib import Path
import torch
from torch import nn
import torch.nn.functional as F

torch.set_num_threads(2)
vocab = ['<start>', '<eos>', '[MASK]', '<S0>', '<S1>', '<S2>', 'the', 'cat', 'sat', 'on', 'mat']
encode = lambda words: torch.tensor([[vocab.index(w) for w in words.split()]])
source = 'the cat sat on the mat'

class Tiny(nn.Module):
    def __init__(self, family):
        super().__init__()
        self.family = family
        self.word = nn.Embedding(len(vocab), 24)
        self.position = nn.Embedding(16, 24)
        self.encoder = nn.TransformerEncoder(nn.TransformerEncoderLayer(
            24, 2, 48, dropout=0, batch_first=True), 1, enable_nested_tensor=False)
        if family == 'seq2seq':
            self.decoder = nn.TransformerDecoder(nn.TransformerDecoderLayer(
                24, 2, 48, dropout=0, batch_first=True), 1)
        self.head = nn.Linear(24, len(vocab))
    def embed(self, x):
        return self.word(x) + self.position(torch.arange(x.shape[1]))
    def forward(self, x, d=None):
        causal = lambda n: torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)
        h = self.encoder(self.embed(x), mask=causal(x.shape[1]) if self.family == 'decoder' else None)
        if self.family == 'seq2seq':
            h = self.decoder(self.embed(d), h, tgt_mask=causal(d.shape[1]))
        return self.head(h)

recipes = {
    'encoder': ('the [MASK] sat on the [MASK]', None, '- cat - - - mat'),
    'decoder': ('<start> the cat sat on the', None, source),
    'seq2seq': ('the <S0> sat on the <S1>', '<start> <S0> cat <S1> mat <S2>', '<S0> cat <S1> mat <S2> <eos>')
}
records = {}
for family, (inputs, decoder_input, targets) in recipes.items():
    torch.manual_seed(351)
    model = Tiny(family)
    x = encode(inputs)
    d = encode(decoder_input) if decoder_input else None
    labels = torch.tensor([[-100 if w == '-' else vocab.index(w) for w in targets.split()]])
    selected = labels[0] != -100
    before_parameters = {n: p.detach().clone() for n, p in model.named_parameters()}
    optimizer = torch.optim.SGD(model.parameters(), lr=.05)
    optimizer.zero_grad()
    logits = model(x, d)
    loss = F.cross_entropy(logits.reshape(-1, len(vocab)), labels.reshape(-1), ignore_index=-100)
    before = logits.detach().softmax(-1)[0]
    loss.backward()
    gradient_norm = sum(float(p.grad.square().sum()) for p in model.parameters() if p.grad is not None) ** .5
    optimizer.step()
    with torch.no_grad():
        after_logits = model(x, d)
        after_loss = F.cross_entropy(after_logits.reshape(-1, len(vocab)), labels.reshape(-1), ignore_index=-100)
        after = after_logits.softmax(-1)[0]
    changes = {name: float((p.detach() - before_parameters[name]).norm()) for name, p in model.named_parameters()}
    rows = []
    for i, w in enumerate(targets.split()):
        if w != '-':
            rows.append(dict(position=i, target=w, before=float(before[i, labels[0,i]]), after=float(after[i, labels[0,i]])))
    assert float(after_loss) < float(loss.detach())
    assert all(torch.isfinite(p).all() for p in model.parameters())
    assert any(v > 0 for k,v in changes.items() if k.startswith('encoder.'))
    if family == 'seq2seq':
        assert any(v > 0 for k,v in changes.items() if k.startswith('decoder.'))
    # Check that changing a future input cannot affect an earlier causal output.
    if family in ('decoder', 'seq2seq'):
        future = (d if d is not None else x).clone()
        future[0,-1] = vocab.index('cat')
        with torch.no_grad():
            changed = model(x, future) if d is not None else model(future)
        assert torch.allclose(after_logits[:,:-1], changed[:,:-1], atol=1e-6)
    records[family] = dict(input=inputs.split(), decoder_input=decoder_input.split() if decoder_input else None,
        targets=targets.split(), selected_count=int(selected.sum()), rows=rows,
        loss_before=float(loss.detach()), loss_after=float(after_loss), gradient_norm=gradient_norm,
        parameter_count=sum(p.numel() for p in model.parameters()), parameter_update_norms=changes)
record = dict(torch=torch.__version__, seed=351, device='CPU', source=source, vocabulary=vocab,
    config=dict(width=24, heads=2, feedforward=48, layers_per_stack=1, dropout=0, optimizer='SGD', learning_rate=.05),
    protocol='Separate randomly initialized teaching models; one step on one word-tokenized example. '
    'Same example before/after, no held-out data. Not checkpoints, not learning curves, not an architecture ranking.',
    records=records)
out = Path(__file__).parent/'evidence'/'section3.json'
out.write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps({k: {f: v[f] for f in ('loss_before','loss_after','selected_count')} for k,v in records.items()}, indent=2))
