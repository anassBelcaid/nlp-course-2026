# Section 1 — learning from raw text

The browser uses `evidence/section1.json`; Quarto does not train, download models,
or run inference. Controls transform the toy corpus or select actual recorded
model outputs. The training-scope and closing diagrams are explicitly schematic.

## Reproduce the evidence

With PyTorch and `transformers==4.57.6` installed:

```sh
python build_section1.py --cache-dir /tmp/nlp-pretraining-models
```

Run this script from its directory, or supply its path from the repository root.
`--model-dir` accepts an already downloaded snapshot to avoid network access.
The checkpoint is stored outside the course and is not published. The small
JSON records model revision, weight/vocabulary SHA-256, library versions, exact
tokens/IDs, all vectors, and the derived cosine. The committed outputs were
produced on CPU with torch 2.13.0+cpu, in eval/inference mode, without training.

## Protocol and limits

- **Corpus builder:** three authored six-word sentences, whitespace tokenization.
  Enumerate each of six possible single-withheld-word positions per sentence.
  The result is exactly 18 pairs. This is a conceptual label-construction exercise,
  not BERT's corruption policy or 18 statistically independent observations.
- **Context viewer:** `prajjwal1/bert-tiny`, pinned revision
  `6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837`, 2 layers, hidden width 128.
  Two authored sentences were chosen before inspecting outputs: “she put money
  in the bank.” and “she saw water by the bank.” Both use bank at position 6
  including CLS. Model weights, the word ID, and its position remain fixed.
  The word-table vectors are exactly equal. The final-layer cosine is about
  0.942831. All 128 coordinates appear in row-major order; there is no PCA or
  semantic-axis interpretation. Each representation has a symmetric color scale
  whose maximum is computed over both contexts and held fixed when switching.
  The tooltip exposes raw values. Different vectors show context dependence,
  not successful sense disambiguation; even random contextual networks can
  produce differences. No samples or coordinates were removed.
- **Spelling viewer:** the same actual WordPiece tokenizer maps learning to
  `[learning]`, relearning to `[re, ##lea, ##rn, ##ing]`, and laerning to
  `[la, ##ern, ##ing]`. Full IDs are in the JSON. All pieces reconstruct their
  original strings. The four-entry whole-word baseline is deliberately a toy.
  These examples show representation of the typo, not correction or robustness.
- **Fallback:** missing evidence disables data-dependent buttons and displays an
  explicit error. Schematic scope controls remain usable. Serve the rendered
  lecture over HTTP. Buttons support pointer and keyboard interaction.
- **Motion:** only the final context-flow diagram loops, while its slide is
  active. Reduced-motion preference disables that movement. Representation
  colors change directly so interpolated colors cannot be mistaken for model
  states. Scope colors transition because that diagram is explicitly schematic.

## Sources

- [BERT-tiny model card](https://huggingface.co/prajjwal1/bert-tiny).
- [Well-Read Students Learn Better](https://arxiv.org/abs/1908.08962), the compact
  BERT family underlying this checkpoint.
- [BERT](https://arxiv.org/abs/1810.04805), whole-model pretraining and transfer.
- [Stanford CS224N pretraining lecture](https://web.stanford.edu/class/cs224n/slides_w26/cs224n-2026-lecture07-pretraining.pdf), conceptual motivation and subword discussion.

The original thumbnail remains a conceptual illustration; it is not model output.

# Section 2 — the BERT idea

`build_section2.py --model-dir /path/to/the/pinned/snapshot` uses the same
PyTorch/Transformers environment and checkpoint as section 1. It records actual
MLM probabilities for the section-1 bridge sentence with bank replaced by MASK.
No model is trained or run in the browser. Every MLM parameter loads from the
checkpoint (the builder rejects missing or mismatched weights); unused pooler
and NSP weights are expected. The record includes exact tokens and IDs, checkpoint
hash, version, top five, target probability/rank, and negative log probability.
The unexpected failure is retained: house ranks first, bank ranks 105th. No
context search or output filtering was used. One example is not an evaluation.
Bars share a fixed 0–5% axis and show full-vocabulary softmax probabilities.

The corruption inspector is a deterministic browser transformation, not inference
or a random simulation of a corpus. All three branches use the same source and
selected position. Its random-token branch fixes table as the example draw;
its unchanged branch still retains the loss target. The percentages describe
the original paper's sampling recipe, not frequencies measured in this widget.
The numerical exercise separately uses explicitly illustrative probabilities.

The benchmark table transcribes three columns and three rows from Devlin et al.
(2019), Table 5: MNLI-m accuracy, MRPC accuracy, SQuAD 1.1 token F1, all dev sets.
It intentionally does not mix these with the paper's test results or MRPC F1.
The 10.1-point difference is 87.9 − 77.8. The paper controls data, fine-tuning
scheme and hyperparameters, but the left-only attention constraint persists at
fine-tuning; the slide makes that limitation explicit. Sources are linked on
slides, with interpretation details in the speaker notes.

# Section 3 — three pretraining families

`build_section3.py` records one actual CPU SGD update for each of three tiny
random Transformers. Run with PyTorch installed; no pretrained downloads are
required. The browser reads `evidence/section3.json` without running training.
The source sentence, fixed 11-token vocabulary, shifted inputs, labels, selected
probabilities, losses, parameter counts and update norms are retained. Width 24,
2 heads, one layer per stack, dropout zero, seed 351, learning rate 0.05.
The causal-only stack uses a TransformerEncoder module with a causal mask;
the seq2seq model adds a TransformerDecoder with encoder cross-attention.
These illustrate BERT/GPT/T5-style objectives, not their checkpoint architectures.
MLM omits NSP; start and EOS conventions are explicit teaching conventions.

The builder checks finite parameters, decreased training loss for these runs,
updates in both seq2seq stacks, and absence of future-token leakage in causal
outputs. Comparing losses across families is not a quality ranking. Each result
is on the same single training example before and after one step; there is no
held-out evaluation. The interactive masks show permissions, not attention
weights. Encoder–decoder mode shows decoder self-attention plus full source
access; its encoder remains bidirectional. All row and family buttons support
keyboard use. The causal loss exercise uses separately labeled illustrative
probabilities. Section 3 stops at the bridge to supervised fine-tuning.

# Section 4 — pretrain once, adapt to tasks

`build_section4_visuals.py` creates the editable SVG diagrams embedded through
`section4-diagrams/*.html`. Squares represent token states, not neurons. Lines
show allowed information flow, not measured attention weights. The sentiment
head and pair head read the final CLS state; the QA diagram applies two shared
scoring vectors to question-conditioned passage states. The two-dimensional
classification exercise and answer-span logits are explicitly illustrative.
The final probe bridge leaves outputs unknown and animates input flow only when
its slide is active; reduced-motion preference pauses/hides the moving dots.

`section4-controls.html` switches a schematic full/frozen update graph and reads
`evidence/section4.json` to plot recorded initialization comparisons. It never
runs inference or trains a model. All three paired seeds are available; the mean
is arithmetic across seeds at each checkpoint. Chart axes span 0–100% accuracy.
A missing evidence file produces an explicit message and disables run buttons.

## Reproduce the classroom comparison

With PyTorch, `transformers==4.57.6` and PyArrow installed:

```sh
python build_section4.py --cache-dir /tmp/nlp-section4-models
```

`--model-dir` and `--data-dir` accept local pinned snapshot directories. The
script pins BERT-tiny revision `6f75de8b60a9f8a2fdf7b69cbd86d9e64bcb3837`
and `stanfordnlp/sst2` revision `8d51e7e4887a4caaa95b3fbebbf53c0490b58bbb`.
Model weights are kept outside the course; evidence retains their SHA-256,
versions, selected training indices, validation records, predictions and curves.
The recorded run used torch 2.14.0+cu130 on CPU and transformers 4.57.6.

- 256 training and 128 original validation examples, class-balanced, sampled
  with seed 351. Exact normalized validation matches are removed from the
  training pool before sampling. Related phrases and pretraining overlap are
  not ruled out. Validation is not used for updates, tuning, or step selection.
- Two-layer, width-128 BERT-tiny; fixed tokenizer and maximum 64 tokens; no
  pooler; direct new linear head on final CLS. Both dropout rates are zero.
- Compare the pinned pretrained encoder to a randomly initialized encoder of
  identical architecture. Within each seed pair, the head's initial weights,
  minibatch order and all downstream hyperparameters are identical.
- Full fine-tuning: AdamW, learning rate 0.0002, weight decay .01, batch size 16,
  80 updates (five passes), seeds 351/352/353, two CPU threads. No tuning sweep.
- Evaluate steps 0, 10, 20, 40 and 80 on the same held-out subset; report final
  step 80 for every run. The builder records nonzero first-step parameter
  changes in embeddings, a contextual attention matrix, and the new head.
- Final correct counts, pretrained/random: 84/74, 76/74, 83/84 out of 128.
  Means: 63.28125% and 60.41667%; difference 2.86458 percentage points.
  Seed 353 reverses the average ordering. All six runs are retained, including
  worsening held-out loss. Three seeds and one small subset are not a benchmark
  or a statistical significance claim. Pretraining compute is additional.

Historical table: Devlin et al. (2019), Table 1, BERT-base/large SST-2 test
accuracy 93.5/94.9 and MRPC test F1 88.9/89.3; Table 2, SQuAD 1.1 dev token F1
88.5/90.9 for single models without extra TriviaQA fine-tuning. Different
columns have different metrics/splits. This documents task applicability, not
an isolated effect of pretraining or a comparison to our classroom experiment.

Section 4 stops at the fixed-model context/typo intervention bridge. Section 5
remains unauthored for instructor review.

## Section 5 — controlled diagnostics

`build_section5.py` records four predeclared sentiment interventions and three
pairs of masked-token prompts in `evidence/section5.json`. It reconstructs the
Section 4 pretrained run (seed 351, step 80) and verifies its held-out probability
vector before testing. The MLM examples instead use the original pretrained
checkpoint and head. No inference-time parameter updates or candidate
renormalization occur. Every predefined result is retained, including failures.
The JSON records tokens, IDs, target ranks, top-five completions, model hashes
and dependency versions. Run with the same environment as Section 4:

```sh
python assets/build_section5.py --model-dir /path/to/pinned/bert-tiny --data-dir /path/to/sst2-snapshot
```

`section5-controls.html` switches recorded sentiment inputs; the browser does
not train. Static MLM tables round the saved full-vocabulary probabilities.
The robustness exercise and contamination diagram are explicitly illustrative.
Published ByT5, GPT-2 extraction and CrowS-Pairs results cite their primary
papers and specify evaluation scope. The ending animation respects reduced motion.
