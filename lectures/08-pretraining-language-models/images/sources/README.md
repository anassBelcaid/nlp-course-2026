# Source figures for “Why pretrain?”

Four figures are cropped directly from the instructor-supplied Stanford PDF,
`cs224n-2026-lecture07-pretraining.pdf`, Diyi Yang, CS224N, 2026. The title page
says Lecture 6. Source URL:
https://web.stanford.edu/class/cs224n/slides_w26/cs224n-2026-lecture07-pretraining.pdf

| Local PNG | PDF page | Printed slide | Extraction rectangle at 2200px page width |
|---|---:|---:|---|
| stanford-embedding-only.png | 10 | 10 | x1260 y250 w880 h590 |
| stanford-whole-model.png | 11 | 11 | x1260 y250 w880 h590 |
| stanford-pretrain.png | 19 | 20 | x110 y365 w900 h710 |
| stanford-finetune.png | 19 | 20 | x1300 y365 w830 h710 |

Rendered using `pdftoppm -f PAGE -l PAGE -scale-to 2200 -x X -y Y -W W -H H
-png -singlefile SOURCE OUTPUT_STEM`. Original diagram colors and wording are
retained. These are conceptual figures, not measured model outputs. The course
adds editable captions and parameter-transfer arrows outside the images.

Content and the context-comparison activity also draw on the instructor-supplied
Berkeley CS288 Spring 2026 PDF, `CS288_sp26_08_Pretraining_Finetuning_Prompting.pdf`,
pp.4–8, 10–16, and 19–20. The bank examples, vector symbols, and interaction are
course adaptations, not extracted Berkeley figures or model measurements.

The complete earlier slide source and its measured evidence remain untouched in
`../../previous-draft.qmd` and `../../assets/evidence/`.

## ELMo evidence

`elmo-figure1.png` reproduces both panels of Figure 1 from Peters et al. (2018),
*Deep Contextualized Word Representations*, PDF page 8 (printed 2234):
https://aclanthology.org/N18-1202.pdf

Extracted directly with `pdftoppm -f 8 -l 8 -scale-to 3600 -x 1310 -y 400
-W 840 -H 500 -png -singlefile /tmp/elmo-paper.pdf OUTPUT_STEM`. Curves, axes,
legend, and annotations are unchanged. The paper caption is replaced by an
editable attribution and explanation in the slide. The figure varies labeled
**task** training data, not language-model pretraining data. No evaluation split
is named in the figure caption; the slide does not invent one.

## BERT increment — 11 November 2026

`berkeley-mlm.png`: diagram cropped from the instructor-supplied Berkeley
CS288 Spring 2026 pretraining lecture, PDF viewer page 36. At page width 2200 px,
extract x=455, y=535, width=1220, height=605 with `pdftoppm`. The crop preserves
the input, bidirectional encoder, target labels, and loss markers; it removes
the slide's prose. Original BERT attribution: Devlin et al. (2019), §3.1.
Labels above the encoder are targets, not recorded model predictions.

The new input-embedding, task-head, and generation-bridge SVGs are editable in
`../../_bert.qmd`. They are original teaching adaptations of BERT Fig. 2,
Stanford PDF pp. 27–28, and Berkeley PDF pp. 43–46. The corruption explanation
uses Stanford p. 27 and Berkeley p. 38. No new model measurements are claimed.
Both full source PDFs have been restored in `tmp/`; preserve them.

## T5 increment — 11 November 2026

`t5-span-construction.png` crops the original/input/target example from Berkeley
CS288 Spring 2026, PDF p. 66 (page width 2400 px; x=1070, y=690, w=1135, h=380).
The underlying image is Raffel et al. (2020), T5 Figure 2. It also appears in
Stanford CS224N PDF p. 36, alongside a source/target network diagram. The crop
preserves Berkeley's encoder/decoder labels but omits the generic architecture
and overbroad capability claims. Source and target EOS are omitted in this
published illustration; our explicit teaching sequences show them.

The editable loss-flow and synthesis-bridge SVGs in `_t5.qmd` are original.
The span control reuses the previous draft's cat/mat construction and multiword
extension. It performs deterministic text manipulation, not tokenizer/model
inference. The final-sentinel convention follows T5 Figure 2; visible S₀/S₁/S₂
are aliases for the extra_id vocabulary tokens.


## Session 2 opening: GPT ablation chart

`../gpt-pretraining-ablation.svg` is redrawn from exact reported SST-2 values
in Radford et al. (2018), *Improving Language Understanding by Generative
Pre-Training*, Table 5, PDF page 8:
https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf

No pretraining: 84.0; full pretrained model: 91.3 (accuracy, percent).
The slide also transcribes MNLI 75.7/81.8 and QNLI 71.2/88.1 in the same order.
Source rows: “Transformer w/o pre-training” and “Transformer w/ aux LM (full)”.
Generated with Matplotlib by `../../assets/build_reuse_chart.py`; no invented
measurements or digitized curves. Axes start at zero; no uncertainty estimates
were supplied by Table 5. Both conditions use downstream task supervision.


## Session 2 sentiment: feature extraction versus fine-tuning

The table in `_finetuning.qmd#ft-evidence` transcribes three rows of Devlin et al.
(2019), §5.3, Table 7, PDF p. 9, https://aclanthology.org/N19-1423.pdf .
BERT-base, CoNLL-2003 NER development F1, mean of five restarts:
last hidden layer features 94.9; concatenated last-four features 96.1;
full fine-tuning 96.4. Frozen conditions train a two-layer 768-dimensional BiLSTM
and classifier; full fine-tuning uses a token classifier. The slide states these
architectural differences, development-set tuning, and the absence of uncertainty
intervals. These are not sentiment results. No new model experiment was run.


## Encoder task overview revision

`_finetuning.qmd#ft-encoder-tasks` adapts the conceptual task list from the supplied
Stanford CS224N pretraining PDF, viewer page 30 / printed slide 32. It is an
editable task map, not a copied screenshot or new benchmark result. Dataset and
benchmark papers are linked per row. The numerical toy exercise is removed;
the general supervised loss and parameter-update equations remain.


## Token labeling and extractive QA

`_token-span.qmd` reuses the preserved QA SVG. The NER sentence/BIO labels are
authored; u1/u2 explicitly denote a hypothetical subword split. No model was run.
The results table transcribes Devlin et al. (2019), Table 2, PDF p. 7:
https://aclanthology.org/N19-1423.pdf
Columns are Dev EM, Dev F1, Test EM, Test F1:
- BERT-base single: 80.8, 88.5, not reported, not reported.
- BERT-large single: 84.1, 90.9, not reported, not reported.
- BERT-large single + TriviaQA: 84.2, 91.1, 85.1, 91.8.
- BERT-large seven-model ensemble + TriviaQA: 86.2, 92.2, 87.4, 93.2.
Metrics are defined using Rajpurkar et al. (2016), §6.1:
https://aclanthology.org/D16-1264.pdf

## GPT trajectory (12 November 2026)

`../gpt3-figure-1-3.png`: original Brown et al. (2020), *Language Models are
Few-Shot Learners*, Figure 1.3, PDF page 5.
Source: https://arxiv.org/pdf/2005.14165
Extracted with Poppler (no curve changes or digitization):

```sh
pdftoppm -f 5 -singlefile -scale-to 2400 -x 420 -y 205 -W 1020 -H 630 -png gpt3-paper.pdf gpt3-figure-1-3
```

Original paper figure, not an original course illustration. Crop excludes caption;
attribution, metric, aggregate caveat and training setting are supplied in slide
`gt-gpt3-evidence`. The plot aggregates 42 accuracy evaluations; the authors caution
against treating the aggregate as a rigorous benchmark. Model sizes share a 300B
training-token budget, not equal compute. Preserve original figure labels.

GPT-2 table: exact PTB and 1BW columns of Radford et al. (2019), Table 3, p. 5.
https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
No new experiments; baseline conditions vary. GPT sentiment ablation chart reuses
`../gpt-pretraining-ablation.svg` and its existing provenance.

## Direct Stanford reference slides (authoritative replacement)

`../stanford-pretraining/slide-42.png` through `slide-56.png` reproduce PDF pages
42–56 (printed44–58) of the instructor-supplied
`tmp/cs224n-2026-lecture07-pretraining.pdf`. Original Stanford CS224N artwork and
text, not course-original figures. Attribution remains visible on every slide.
Extraction: `pdftoppm -f 42 -l 56 -scale-to 1920 -png SOURCE.pdf slide`.
No page content altered. Corrections are separate editable captions. Original
text is also included in speaker notes. These replace the authored GPT sequence.
