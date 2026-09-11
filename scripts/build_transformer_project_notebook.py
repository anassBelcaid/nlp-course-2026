import json
from pathlib import Path


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.strip().splitlines(True)}


cells = [
md(r"""
# Project 03 · Session 3 — Build a causal Transformer

You will build a character-level Transformer without using `nn.MultiheadAttention` or `nn.TransformerEncoderLayer`. The purpose is to make every important tensor operation visible. Infrastructure is provided; the architectural decisions are yours.

By the end, your model will generate new names by **sampling** from its next-token distribution.

### Required components

1. sinusoidal `PositionalEmbedding` and combined token–position embedding;
2. causal multi-head self-attention, separated into projection, masking, reshaping, score multiplication, and output stages;
3. a position-wise MLP;
4. a pre-norm Transformer block using PyTorch `LayerNorm` and `Dropout`;
5. next-token batch loss and a training loop; and
6. temperature-controlled categorical sampling.
"""),
md(r"""
## Why `einops`?

PyTorch tensors are indexed by dimensions, but ordinary `view`, `reshape`, `transpose`, and `permute` calls do not say what those dimensions mean. [`einops.rearrange`](https://einops.rocks/1-einops-basics/) makes the transformation readable:

```python
rearrange(x, "batch time (head feature) -> batch head time feature", head=h)
```

The pattern is an executable shape explanation. We will use it only where heads are created or recombined.
"""),
code(r"""
from __future__ import annotations

import math
import random
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from einops import rearrange
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset

SEED = 351
random.seed(SEED)
torch.manual_seed(SEED)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device:", DEVICE)
"""),
md("## 0 · Data and batching — provided\n\nWe reuse the names dataset from Sessions 1–2. Inputs are shifted right with `<BOS>`; targets end with `<EOS>`. Padding must never contribute to the loss."),
code(r"""
DATA_URL = "https://raw.githubusercontent.com/karpathy/makemore/master/names.txt"
DATA_PATH = Path("babynames.txt")
if not DATA_PATH.exists():
    urllib.request.urlretrieve(DATA_URL, DATA_PATH)

names = [line.strip().lower() for line in DATA_PATH.read_text().splitlines() if line.strip()]
PAD_TOKEN, BOS_TOKEN, EOS_TOKEN = "<PAD>", "<BOS>", "<EOS>"
characters = sorted(set("".join(names)))
itos = [PAD_TOKEN, BOS_TOKEN, EOS_TOKEN] + characters
stoi = {token: index for index, token in enumerate(itos)}
PAD_ID, BOS_ID, EOS_ID = stoi[PAD_TOKEN], stoi[BOS_TOKEN], stoi[EOS_TOKEN]
VOCAB_SIZE = len(itos)

def encode(text: str) -> list[int]:
    return [stoi[c] for c in text]

def decode(ids: list[int]) -> str:
    return "".join(itos[i] for i in ids if i >= 3)

class NameDataset(Dataset):
    def __init__(self, items: list[str]): self.items = items
    def __len__(self): return len(self.items)
    def __getitem__(self, index):
        ids = encode(self.items[index])
        return [BOS_ID] + ids, ids + [EOS_ID]

def collate_names(batch):
    width = max(len(x) for x, _ in batch)
    inputs = torch.full((len(batch), width), PAD_ID, dtype=torch.long)
    targets = torch.full_like(inputs, PAD_ID)
    for row, (x, y) in enumerate(batch):
        inputs[row, :len(x)] = torch.tensor(x)
        targets[row, :len(y)] = torch.tensor(y)
    return inputs, targets

shuffled = names.copy()
random.Random(SEED).shuffle(shuffled)
n_train = int(.8 * len(shuffled)); n_valid = int(.1 * len(shuffled))
train_names = shuffled[:n_train]
valid_names = shuffled[n_train:n_train+n_valid]
test_names = shuffled[n_train+n_valid:]
train_loader = DataLoader(NameDataset(train_names), batch_size=256, shuffle=True, collate_fn=collate_names)
valid_loader = DataLoader(NameDataset(valid_names), batch_size=256, collate_fn=collate_names)
print(f"{len(names):,} names · vocabulary {VOCAB_SIZE} · splits {len(train_names):,}/{len(valid_names):,}/{len(test_names):,}")
"""),
md(r"""
## Question 1 · Position-aware embeddings

### 1a — `PositionalEmbedding`

Create the classical sinusoidal table once and register it as a **buffer**, not a parameter. For maximum length $T_{max}$ and even/odd feature indices:

$$PE(pos,2i)=\sin(pos/10000^{2i/d}),\qquad PE(pos,2i+1)=\cos(pos/10000^{2i/d}).$$

`forward(length)` returns `[1, length, d_model]`, allowing broadcasting across the batch.

### 1b — `TokenPositionalEmbedding`

Combine `nn.Embedding` with your position module:

$$Z=\sqrt{d_{model}}\,E[\text{token ids}]+PE.$$

Then apply dropout. The scaling follows the original Transformer and keeps token magnitude comparable to position magnitude.
"""),
code(r"""
class PositionalEmbedding(nn.Module):
    def __init__(self, d_model: int, max_length: int = 256):
        super().__init__()
        # TODO Q1a — build [max_length, d_model] sinusoidal encodings.
        positions = ...
        frequencies = ...
        encoding = ...
        # TODO — fill even features with sin and odd features with cos.
        ...
        self.register_buffer("encoding", encoding, persistent=False)

    def forward(self, length: int) -> torch.Tensor:
        # TODO — return [1, length, d_model].
        ...

class TokenPositionalEmbedding(nn.Module):
    def __init__(self, vocab_size: int, d_model: int, max_length: int, dropout: float):
        super().__init__()
        self.d_model = d_model
        self.token = ...
        self.position = ...
        self.dropout = ...

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        # TODO Q1b — token embedding + matching position slice, then dropout.
        ...
"""),
code(r"""
# Check Q1
position = PositionalEmbedding(d_model=8, max_length=16)
assert dict(position.named_parameters()) == {}, "Sinusoidal positions must not be learned parameters."
pe = position(5)
assert pe.shape == (1, 5, 8)
assert torch.allclose(pe[0, 0, 0::2], torch.zeros(4), atol=1e-6)
assert torch.allclose(pe[0, 0, 1::2], torch.ones(4), atol=1e-6)
embedding_probe = TokenPositionalEmbedding(VOCAB_SIZE, 8, 16, dropout=0.0)
assert embedding_probe(torch.tensor([[BOS_ID, stoi["a"]]])).shape == (1, 2, 8)
print("✓ Q1 passed: content and position combine without changing [batch, time, feature].")
"""),
md(r"""
## Question 2 · Causal multi-head self-attention

This is the core exercise. Implement it in five inspectable stages. Do not collapse the work into `nn.MultiheadAttention`.

Let the input be `x: [B, T, D]`, with `D = H × Dh`.

### 2a — Projection

One linear layer may produce concatenated $Q,K,V$. Split its last dimension into three tensors, each `[B,T,D]`.

### 2b — Reshape into heads

Use `einops.rearrange` to map `[B,T,H×Dh] → [B,H,T,Dh]`.

### 2c — Matrix multiplication

Compute scaled scores `[B,H,T,T]` with `q @ k.transpose(-2,-1) / sqrt(Dh)`.

### 2d — Causal and padding masks

Set future positions to $-\infty$. Also mask padded **keys** so real queries cannot retrieve padding. Apply softmax only after both masks.

### 2e — Retrieve, merge, project

Multiply weights by values, rearrange heads back to `[B,T,D]`, apply the output projection and dropout. Return both output and attention weights so the mechanism remains inspectable.
"""),
code(r"""
class CausalMultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        self.qkv_projection = ...       # TODO Q2a
        self.output_projection = ...    # TODO Q2e
        self.attention_dropout = nn.Dropout(dropout)
        self.output_dropout = nn.Dropout(dropout)

    def project_qkv(self, x: torch.Tensor):
        # TODO Q2a — project once and split into q, k, v.
        qkv = ...
        return ...

    def split_heads(self, x: torch.Tensor) -> torch.Tensor:
        # TODO Q2b — use rearrange, not view/permute.
        return rearrange(...)

    def attention_scores(self, q: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
        # TODO Q2c — [B,H,T,Dh] @ [B,H,Dh,T] -> [B,H,T,T].
        return ...

    def apply_masks(self, scores: torch.Tensor, token_ids: torch.Tensor) -> torch.Tensor:
        B, H, T, _ = scores.shape
        # TODO Q2d — upper triangular future mask [T,T].
        future_mask = ...
        scores = ...
        # TODO Q2d — padding-key mask broadcastable to [B,H,T,T].
        padding_keys = ...
        scores = ...
        return scores

    def merge_heads(self, x: torch.Tensor) -> torch.Tensor:
        # TODO Q2e — [B,H,T,Dh] -> [B,T,H*Dh].
        return rearrange(...)

    def forward(self, x: torch.Tensor, token_ids: torch.Tensor):
        q, k, v = self.project_qkv(x)
        q, k, v = self.split_heads(q), self.split_heads(k), self.split_heads(v)
        scores = self.attention_scores(q, k)
        masked_scores = self.apply_masks(scores, token_ids)
        weights = ...                   # TODO Q2d — softmax over keys, then dropout.
        context = ...                   # TODO Q2e — weighted value retrieval.
        merged = self.merge_heads(context)
        output = ...                    # TODO Q2e — output projection, then dropout.
        return output, weights
"""),
code(r"""
# Check Q2: shapes, probability normalization, and causality
attention = CausalMultiHeadAttention(d_model=12, num_heads=3, dropout=0.0)
attention.eval()
ids = torch.tensor([[BOS_ID, stoi["a"], stoi["n"], EOS_ID]])
x = torch.randn(1, 4, 12)
output, weights = attention(x, ids)
assert output.shape == (1, 4, 12)
assert weights.shape == (1, 3, 4, 4)
assert torch.allclose(weights.sum(dim=-1), torch.ones(1, 3, 4), atol=1e-6)
assert torch.count_nonzero(torch.triu(weights, diagonal=1)) == 0

# A changed future representation must not alter outputs at earlier positions.
x_changed = x.clone(); x_changed[:, 3] += 100
output_changed, _ = attention(x_changed, ids)
assert torch.allclose(output[:, :3], output_changed[:, :3], atol=1e-5)
print("✓ Q2 passed: attention has correct shapes and cannot see the future.")
"""),
md(r"""
## Question 3 · Position-wise MLP

Implement the simple Transformer FFN with PyTorch modules:

$$\operatorname{MLP}(x)=W_2\,\operatorname{GELU}(W_1x+b_1)+b_2.$$

Expand to `d_ff`, apply [`nn.GELU`](https://pytorch.org/docs/stable/generated/torch.nn.GELU.html) and dropout, then project back to `d_model` and apply dropout again. `nn.Linear` automatically operates on the final tensor dimension, independently at every token.
"""),
code(r"""
class PositionwiseMLP(nn.Module):
    def __init__(self, d_model: int, d_ff: int, dropout: float):
        super().__init__()
        # TODO Q3 — build Linear → GELU → Dropout → Linear → Dropout.
        self.network = ...

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return ...

mlp_probe = PositionwiseMLP(12, 48, 0.0)
assert mlp_probe(torch.randn(2, 5, 12)).shape == (2, 5, 12)
print("✓ Q3 passed: the FFN transforms features and preserves sequence shape.")
"""),
md(r"""
## Question 4 · One Transformer block

Use a **pre-norm** block:

$$x \leftarrow x + \operatorname{Attention}(\operatorname{LN}_1(x)),$$
$$x \leftarrow x + \operatorname{MLP}(\operatorname{LN}_2(x)).$$

Use [`nn.LayerNorm(d_model)`](https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html), which normalizes the final feature dimension independently for each token. Use [`nn.Dropout`](https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html) inside attention and the MLP; it is active only in `model.train()` mode.
"""),
code(r"""
class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float):
        super().__init__()
        # TODO Q4 — two LayerNorm modules, causal MHA, and position-wise MLP.
        self.norm1 = ...
        self.attention = ...
        self.norm2 = ...
        self.mlp = ...

    def forward(self, x: torch.Tensor, token_ids: torch.Tensor):
        # TODO Q4 — both pre-norm residual updates. Keep attention weights.
        attention_output, weights = ...
        x = ...
        x = ...
        return x, weights
"""),
md("## Question 5 · Assemble the causal language model\n\nCombine position-aware embeddings, a stack of independent Transformer blocks, a final LayerNorm, and a vocabulary projection. Return `[B,T,V]` logits and the attention maps from every layer."),
code(r"""
class CharacterTransformerLM(nn.Module):
    def __init__(self, vocab_size: int, d_model=96, num_heads=4, d_ff=384,
                 num_layers=3, max_length=64, dropout=0.1):
        super().__init__()
        # TODO Q5 — construct embedding, ModuleList of blocks, final norm, LM head.
        self.embedding = ...
        self.blocks = ...
        self.final_norm = ...
        self.lm_head = ...

    def forward(self, token_ids: torch.Tensor):
        x = ...
        attention_maps = []
        for block in self.blocks:
            # TODO Q5 — update x and collect this layer's attention weights.
            ...
        logits = ...
        return logits, attention_maps

model = CharacterTransformerLM(VOCAB_SIZE).to(DEVICE)
probe = torch.tensor([[BOS_ID, stoi["a"], stoi["n"]]], device=DEVICE)
probe_logits, probe_maps = model(probe)
assert probe_logits.shape == (1, 3, VOCAB_SIZE)
assert len(probe_maps) == 3
print(f"✓ Q5 passed: {sum(p.numel() for p in model.parameters()):,} trainable parameters.")
"""),
md(r"""
## Question 6 · Batch loss and prediction error

At every non-padding position, the model predicts the target next token. Flatten `[B,T,V]` logits to `[B×T,V]` and targets to `[B×T]`, then use cross-entropy with `ignore_index=PAD_ID`.

Also report token error rate:

$$\text{error}=1-\frac{\#\text{correct non-pad predictions}}{\#\text{non-pad targets}}.$$
"""),
code(r"""
def batch_loss_and_error(model: nn.Module, inputs: torch.Tensor, targets: torch.Tensor):
    # TODO Q6 — forward, padded cross-entropy, argmax predictions, non-pad error.
    logits, _ = ...
    loss = ...
    predictions = ...
    valid = ...
    error = ...
    return loss, error

batch_inputs, batch_targets = next(iter(train_loader))
loss, error = batch_loss_and_error(model, batch_inputs.to(DEVICE), batch_targets.to(DEVICE))
assert loss.ndim == error.ndim == 0 and loss.isfinite() and 0 <= error <= 1
print(f"✓ Q6 passed: initial loss={loss.item():.3f}, token error={error.item():.1%}")
"""),
md("## Question 7 · Training loop\n\nWrite one complete epoch function. Set train/evaluation mode correctly, move batches to the device, zero gradients, backpropagate only during training, clip the global gradient norm, update parameters, and return token-weighted mean loss and error."),
code(r"""
def run_epoch(model, loader, optimizer=None, max_batches=None):
    training = optimizer is not None
    # TODO Q7 — select train/eval mode.
    ...
    loss_sum = error_sum = token_count = 0.0

    for batch_index, (inputs, targets) in enumerate(loader):
        if max_batches is not None and batch_index >= max_batches: break
        inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
        valid_tokens = (targets != PAD_ID).sum().item()

        # TODO Q7 — zero gradients when training.
        ...
        with torch.set_grad_enabled(training):
            loss, error = ...
            if training:
                # TODO — backward, gradient clipping, optimizer step.
                ...

        loss_sum += loss.item() * valid_tokens
        error_sum += error.item() * valid_tokens
        token_count += valid_tokens
    return loss_sum / token_count, error_sum / token_count

optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=0.01)
history = []
for epoch in range(1, 9):
    train_loss, train_error = run_epoch(model, train_loader, optimizer)
    with torch.no_grad():
        valid_loss, valid_error = run_epoch(model, valid_loader)
    history.append((train_loss, valid_loss))
    print(f"epoch {epoch:02d} · train {train_loss:.3f}/{train_error:.1%} · valid {valid_loss:.3f}/{valid_error:.1%}")
"""),
code(r"""
plt.plot([x[0] for x in history], label="train loss")
plt.plot([x[1] for x in history], label="validation loss")
plt.xlabel("epoch"); plt.ylabel("cross-entropy"); plt.legend(); plt.show()
"""),
md(r"""
## Question 8 · Generate by sampling, not greedy decoding

At each step:

1. run the current prefix through the model;
2. select only the final-position logits;
3. divide logits by temperature $\tau>0$;
4. turn them into probabilities; and
5. sample with `torch.multinomial`.

Greedy decoding always selects the maximum-probability token and produces no diversity. Sampling treats the model output as a distribution. Lower temperature sharpens it; higher temperature flattens it.
"""),
code(r"""
@torch.no_grad()
def sample_name(model: nn.Module, temperature: float = 1.0, max_new_tokens: int = 24) -> str:
    assert temperature > 0
    model.eval()
    generated = [BOS_ID]
    for _ in range(max_new_tokens):
        token_ids = torch.tensor([generated], device=DEVICE)
        logits, _ = ...                 # TODO Q8
        next_logits = ...               # final sequence position only
        probabilities = ...             # temperature + softmax
        next_id = ...                    # torch.multinomial; convert to int
        if next_id == EOS_ID: break
        generated.append(next_id)
    return decode(generated)

for temperature in (0.6, 0.9, 1.2):
    print(f"\ntemperature={temperature}")
    print([sample_name(model, temperature) for _ in range(12)])
"""),
md(r"""
## Final reflection

Answer with concrete evidence from your implementation and outputs.

1. Write the shape of $Q$, $K$, $V$, the score tensor, attention weights, and the merged context for your batch.
2. Which exact line prevents future-token leakage? Why must it execute before softmax?
3. Why is the padding mask applied to keys? What would padded queries affect if their loss is ignored?
4. Compare generated names at temperatures 0.6 and 1.2. Discuss diversity and validity.
5. Compare this Transformer with your RNN, LSTM, and GRU from Sessions 1–2: parameter count, validation loss, training parallelism, and generation quality.
6. The attention score tensor is `[B,H,T,T]`. What happens to its size when sequence length doubles?
"""),
md(r"""
## References and implementation companions

- [Vaswani et al. · Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Harvard NLP · The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/)
- [Einops tutorial](https://einops.rocks/1-einops-basics/)
- [PyTorch LayerNorm](https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)
- [PyTorch Dropout](https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html)
- [PyTorch multinomial sampling](https://pytorch.org/docs/stable/generated/torch.multinomial.html)
"""),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

target = Path("projects/03-neural-sequence-lab/starter/03_causal_transformer.ipynb")
target.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
