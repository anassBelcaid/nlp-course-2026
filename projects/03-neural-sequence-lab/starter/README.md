# Project 03 · Neural Sequence Laboratory

The guided notebooks currently include:

- `01_names_rnn.ipynb`: students build the five chapter-specific pieces of a
  character-level vanilla RNN;
- `02_names_lstm_gru.ipynb`: students implement complete LSTM and GRU cells
  while the shared training and comparison infrastructure is supplied.

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
trained, diagnosed, and compared manual LSTM and GRU cells.
