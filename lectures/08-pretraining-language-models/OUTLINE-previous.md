# Pretraining Language Models — revised teaching plan

The opening and Sections 1–5 are authored for review. Develop one requested section
at a time and stop for instructor review. This plan follows the instructor's
sequence; it does not duplicate Stanford's ordering or reteach tokenization and
Transformer architecture from earlier lectures.

## 1. Learning from raw text

Begin with a short sentence from a larger text collection: where could training
targets come from without manual annotation? Contrast a static word embedding
with a context-dependent representation. Briefly retrieve subword tokenization
using a normal word, an unfamiliar form, and a typo. Representability and robust
interpretation are different questions; save measured robustness for section 5.

## 2. The BERT idea

Keep the original sentence visible while hiding or replacing selected tokens.
Let students predict the missing content before showing model predictions.
Derive the contextual recovery objective from this concrete task. Then explain
the original 15% selection and conditional 80/10/10 corruption rule, including
unchanged selected tokens and loss only on selected positions. Inspect tokens,
targets, probability distributions, and errors. Mention original NSP briefly.
Ordinary typos are not the same as BERT's random-token corruption.

## 3. Three families, three training recipes

Use BERT, GPT, and T5 as representative recipes. On one fixed example, compare:

| Family | Representative pretraining task | Downstream examples |
|---|---|---|
| Encoder | Recover selected original tokens from corrupted bidirectional context | Classification, sentence-pair decisions, extractive QA |
| Decoder | Predict the next token from preceding tokens | Continuation and prompted generation |
| Encoder–decoder | Encode corrupted text; decode missing spans (T5) | Text-to-text tasks, including summarization and translation after adaptation |

These are typical matches, not exclusive capabilities. Show actual input/target
construction, attention visibility, loss positions, and a small training step
for each. Use the same visual identities for token rows, architecture, and code.
The first numerical exercise needs a PAUSE panel and its solution on the next slide.

## 4. Pretrain once, adapt to tasks

Reuse BERT with small task-specific heads: sentiment (SST-2), sentence pairs
(paraphrase or entailment), and extractive question answering (SQuAD). Explain
what is pretrained, what is newly initialized, and which weights fine-tuning
updates. Use historical results from the BERT paper and a controlled classroom
comparison with a randomly initialized baseline. Distinguish frozen features
from full fine-tuning. Avoid implying that only the head normally learns.

## 5. What did the model learn?

Use context swaps, ambiguity, and typos as interventions on fixed examples.
Inspect predictions before interpreting syntax, semantic associations, or factual
recall. Separate generalization from memorization; discuss held-out evaluation,
contamination, and inherited biases through evidence. A small probe is not proof
of general understanding. ByT5 provides an optional research comparison for
noise robustness, rather than treating robustness as guaranteed by BERT.

## 6. Modern pretraining at scale

Make data quality, deduplication, mixtures, model size, and token budget concrete
using *The Llama 3 Herd of Models*. Use *Olmo 3* as a complementary open-training
case study: documented data, stages, and checkpoints make experiments inspectable.
Choose one question about changing the training data while controlling the budget;
avoid a catalogue of model names. Introduce in-context examples briefly, contrasting
fixed weights with fine-tuning. End with a visual bridge from a base predictor to
an instruction-following assistant; reserve post-training mechanisms for Lecture 09.

## Interaction contract

Each demonstration states one question and what changes versus stays fixed.
Synchronize tokens, intermediate values, diagrams, and outputs. Prefer local
recorded model evidence and small exact browser calculations. Identify toy
examples and recorded results; preserve failures and reproducible generation
scripts. Ask for predictions before revealing conclusions.

## Presentation rhythm

Section 2 alternates a section opener, recorded prediction figure, one corruption
inspector, a PAUSE exercise and equation-based solution, a document-pair example,
a published ablation table, and a visual bridge. Preserve this variety in later
sections: a successful interaction is not a template for every slide.

## Primary reading path

- [Stanford CS224N, 2026 pretraining slides](https://web.stanford.edu/class/cs224n/slides_w26/cs224n-2026-lecture07-pretraining.pdf): pp. 5–7 for unfamiliar spellings, 10–11 for whole-model pretraining, 28–32 for BERT, 38–41 for encoder–decoder pretraining, and 56 onward for learned properties and limitations. The title page says Lecture 6 despite the lecture07 filename.
- [BERT, Devlin et al.](https://arxiv.org/abs/1810.04805): original objectives, masking procedure, transfer tasks, and results.
- [T5, Raffel et al.](https://www.jmlr.org/papers/v21/20-074.html): span corruption and text-to-text transfer.
- [Language Models are Few-Shot Learners, Brown et al.](https://arxiv.org/abs/2005.14165): in-context examples without gradient updates.
- [ByT5, Xue et al.](https://arxiv.org/abs/2105.13626): byte-level modeling and measured noise robustness.
- [The Llama 3 Herd of Models, 2024](https://arxiv.org/abs/2407.21783): data curation, mixture experiments, and compute-aware scaling.
- [Olmo 3, 2025](https://arxiv.org/abs/2512.13961): open model flow and staged training. Use the pretraining portions here.
