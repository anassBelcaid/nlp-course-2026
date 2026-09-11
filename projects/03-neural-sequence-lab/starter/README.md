# Project 03 · Neural Sequence Laboratory

The guided notebooks currently include:

- `01_names_rnn.ipynb`: students build the five chapter-specific pieces of a
  character-level vanilla RNN;
- `02_names_lstm_gru.ipynb`: students implement complete LSTM and GRU cells
  while the shared training and comparison infrastructure is supplied.
- `03_causal_transformer.ipynb`: students build sinusoidal embeddings, causal
  multi-head attention with explicit `einops` reshaping, the MLP and pre-norm
  Transformer block, padded next-token loss, training, and sampled generation.

## Local setup

```bash
uv sync
uv run jupyter lab
```

The notebook can also be uploaded directly to Google Colab. On its first run,
it downloads and caches Karpathy's `names.txt` dataset as `babynames.txt`.

## Current outcomes

By the end of Session 1, students train a vanilla RNN and sample original baby
names at several temperatures. By the end of Session 2, they have implemented,
trained, diagnosed, and compared manual LSTM and GRU cells. Session 3 exposes
the complete causal Transformer path and ends with the same stochastic
generation task, enabling a controlled comparison with recurrence.
