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
