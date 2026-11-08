# Pretraining: proposed common ground for a two-hour lecture

Discussion draft, 8 November 2026. This is a proposed teaching plan, not an
approved replacement for OUTLINE.md or the presentation. No slides changed.

## What was reviewed

- Current `index.qmd`: 57 slides, opening plus Sections 1–5. Section 6 is planned
  but not authored. Speaker notes and evidence documentation were also read.
- Stanford: `tmp/cs224n-2026-lecture07-pretraining.pdf`, 56 PDF pages.
- Berkeley: `tmp/CS288_sp26_08_Pretraining_Finetuning_Prompting.pdf`, 114 PDF pages.
  This combines material across meetings, with restart markers at pages 24 and
  85 and repeated recaps; it is not a single two-hour lecture template.
- Selected source diagrams were rendered and inspected visually.

All page references below mean **PDF viewer page numbers**, starting at 1.
Stanford's printed slide numbers diverge from PDF page numbers; for example,
PDF page 36 is the slide numbered 38 about T5 span corruption.

## One story to teach

We already know how a Transformer computes representations. Its architecture
does not supply useful trained weights. A large text collection supplies
prediction targets automatically. Training on those targets produces weights
that can be reused: through task-specific fine-tuning, or, for a capable
generative model, through a prompt while keeping weights fixed.

Teaching anchor: **Where do the targets come from, what can the model see, and
which weights change?** Ask these same three questions at each stage.

Keep four ideas separate:

| Idea | Concrete meaning |
|---|---|
| Architecture | How token states exchange information: encoder, decoder, encoder–decoder |
| Objective | What prediction the loss rewards: a missing token, next token, or missing span |
| Pretraining / fine-tuning | Stages of learning and reuse of parameters |
| Prompting | Supplying input to a model; ordinarily no optimizer update |

BERT/GPT/T5 are representative combinations, not interchangeable names for
these four concepts. A contextual vector is an output of the model; learned
weights are what is saved and reused. Self-supervised does not mean no targets:
the targets come from the text itself.

## Two-hour budget

The 110 minutes below include short prediction questions and worked examples.
Reserve another 10 minutes for a break, questions, or slower explanations.
Aim for roughly 30–34 core slides, with additional material in an appendix.

| Time | Part | What the instructor needs to establish |
|---|---|---|
| 0–15 | Why pretrain? | Static embeddings versus contextual representations; whole-model reuse; show the full pretrain/adapt workflow early |
| 15–40 | BERT as the main worked example | Raw text → corruption → vocabulary predictions → loss → weight update; 15% and conditional 80/10/10; NSP only briefly |
| 40–60 | Put the pretrained model to work | Sentiment head in detail; full fine-tuning versus frozen features; one contrasting token-level task; one historical results figure |
| 60–80 | GPT and T5: change the prediction task | Causal input/target alignment, training versus generation, T5 span corruption; finish with a three-family comparison |
| 80–95 | Fine-tuning versus prompting | Same sentiment task through updated weights versus examples in context; zero-shot and few-shot; one concrete comparison |
| 95–110 | Data, scale, limits, and next lecture | Sources and filtering; model size versus training tokens; what prediction can learn and inherit; base model versus assistant |
| 110–120 | Reserved time | Questions, break, or pacing margin |

The ordering completes the BERT story before introducing two other recipes.
It differs from the current deck, which postpones BERT's practical reuse until
after an extensive three-family training comparison.

## Worked examples and mathematical depth

1. Reuse the bank-in-two-contexts example to explain contextual representations.
   A picture of different vectors is enough; the 128-coordinate/cosine analysis
   is optional and does not establish word-sense understanding.
2. Use one short sentence to show BERT inputs and targets. The Berkeley sentence
   about California and Sacramento also provides a matched causal-LM diagram.
   A hand-selected pair of masked words is illustrative, not literally a 15%
   sample from that short sentence.
3. Keep one numerical MLM cross-entropy exercise: explicit givens and PAUSE,
   followed by a separate solution slide. Explain how the loss reaches the
   embedding table, Transformer, and vocabulary head.
4. Use sentiment to show what changes downstream: a vocabulary target becomes
   a task label, a new head is attached, and full fine-tuning updates both head
   and backbone. A second complete softmax arithmetic exercise is unnecessary.
5. Use NER as the short contrasting output interface, following Berkeley p.46:
   one label per token instead of one per sentence. It also connects naturally
   to the accepted personal-data masking project. Keep extractive QA as backup.
6. Show next-token loss as the same prediction principle applied to shifted
   targets. Retain causal visibility and training/generation distinction; move
   the separate numerical sequence-likelihood exercise to the appendix.
7. For T5, show corrupted source and generated missing spans. Do not rederive
   cross-attention or a third full loss calculation.
8. Reuse sentiment once more for prompting. Examples now enter the context;
   they do not produce gradient updates at inference time.

Core mathematics: selected-token cross-entropy, causal factorization/loss, and
the task head `softmax(Wh + b)`. Derive only the first numerical loss in detail.
No scaling-law exponents, optimizer internals, or QA boundary-loss derivation
are necessary for the main story.

## Specific source visuals to include

These are actual source figures to reuse with attribution, not merely reading
references. Where a figure originated in a paper, credit both that paper and
the lecture through which it was selected. Prefer a readable crop or a clearly
labeled adaptation to a tiny full-slide screenshot. Save final assets locally.

| Teaching purpose | Source | Proposed use |
|---|---|---|
| Embedding pretraining → whole-model pretraining | Stanford pp.10–11 | Keep the paired network drawings; explain the change in pretrained parameters |
| The complete pretraining/fine-tuning workflow | Stanford p.19 (printed 20) | Introduce early; return to it when attaching a sentiment head |
| MLM inputs, output positions, and losses | Berkeley p.36 | Large diagram; annotate precisely which positions contribute direct loss |
| Original BERT corruption | Stanford p.27 (printed 29), Berkeley p.38 | Use one recipe explanation, complemented by our existing corruption inspector |
| BERT classification and sequence tagging | Berkeley pp.43–46 | Main sentiment diagram from p.45; compact NER contrast from p.46 |
| Historical evidence of downstream usefulness | Stanford p.30 (printed 32), or Berkeley p.47 | Select a few legible columns with task metrics; do not present as a controlled random-initialization comparison |
| Causal prediction paired with MLM | Berkeley p.58 | Pair with p.36: same sentence, different context access and loss positions |
| T5 missing spans | Stanford p.36 (printed 38), Berkeley p.66 | Prefer Stanford's span-and-network illustration; Berkeley provides an alternative architecture view |
| Fine-tuning versus in-context examples | Berkeley p.77 | Central side-by-side diagram; explicitly mark weights updated/fixed |
| Compute, data, and parameters | Stanford p.49 (printed 51), with p.52 (printed 54) as backup | One readable empirical scaling figure; focus on the axes and budget tradeoff |

Content-only sources: Stanford pp.12–16 and 54 for intuitions about syntax,
facts, sentiment, and inherited associations; Berkeley pp.88–91 for the three
reuse modes. The Berkeley contextual-embedding exercise on p.8 is an optional
opening question. ELMo is a short historical bridge, not a separate unit.

Do not reproduce every source sentence literally. For example, say masked
encoders are not naturally left-to-right generators, rather than that they
cannot generate at all. Keep the family table to BERT/GPT/T5 representative
recipes; avoid treating all variants as having identical objectives.

## What to do with the current deck

| Current material | Proposed decision |
|---|---|
| Original overview image | Keep immediately after the title |
| Raw-text example and whole-model initialization diagram | Keep and shorten; show the full reuse workflow sooner |
| Counting 18 constructed examples | Appendix; it delays the main learning mechanism |
| Tokenization/typo inspection | At most a brief reminder; tokenization was taught earlier |
| BERT corruption inspector and MLM exercise | Keep |
| BERT NSP and ablation table | NSP briefly; ablation as optional evidence after tasks have been explained |
| BERT-tiny failed completion as first encounter | Move to optional diagnostics; use an explicitly schematic distribution to teach the mechanism first |
| Three-family attention map | Keep as a short recap; do not reteach Transformer architecture |
| Three optimizer-step demos and extra loss exercises | Appendix or practical session |
| Fine-tuning update/frozen-feature control | Keep |
| Sentence-pair and detailed QA heads | Appendix; sentiment plus a compact NER example suffice in the main lecture |
| Small pretrained/random SST-2 comparison | Appendix; its modest, variable outcome needs experimental context that distracts from a first explanation |
| Twelve-slide diagnostics section | Reduce to roughly two core slides: what can be learned; what prediction does not guarantee |
| Planned Llama 3 and OLMo case studies | Optional reading; retain only a brief data/compute story in the core |
| Prompting / in-context learning | Add using Berkeley's concrete comparison; this is a major missing part of the authored deck |

Preserve existing recorded failures and provenance in optional material. Do not
change observations to produce a more persuasive demonstration.

## Ending and instructor preparation

Finish with a visual: raw text → pretrained base predictor → an unresolved
adaptation stage → helpful instruction-following assistant. The final question:
**“Predicting text is useful—but what teaches a model to follow our instructions?”**
Lecture 09 already covers instruction tuning, preference optimization, LoRA,
adapters, and quantization. Leave those mechanisms there. Chain-of-thought and
the research debate over in-context learning also stay outside this core.

Before authoring each part, prepare a short instructor explanation containing:

- The question being answered, in plain language.
- One concrete input, target, and diagram walkthrough.
- Which parameters are learned, reused, or held fixed.
- The one equation needed, with symbols tied to the example.
- A likely student confusion and a transition question.

Next discussion: agree on the central story and ordering, then explain the
pretraining/fine-tuning/prompting distinction together before revising slides.
