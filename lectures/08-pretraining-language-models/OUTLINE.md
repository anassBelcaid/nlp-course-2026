# Pretraining Language Models — two-session teaching plan

Accepted structure: two sessions of at most two hours each. Rebuild incrementally
and stop for instructor review after each requested section.

## Current review stage

Read `HANDOFF.md` first when resuming. The instructor approved the current
16-slide preview: opening (1–3), “Why pretrain?” (4–9), “Text supplies its own
targets” (10–14), and the architecture transition (15–16). The detailed BERT
section is next, not yet authored in the rebuilt deck.

The Session 2 plan is preserved in `_session2-plan.qmd` and must appear only
AFTER all Session 1 content and its closing bridge. It is not included yet.
The schedule links to this in-progress preview and the preserved earlier draft.

## Session 1 — How does pretraining work?

| Part | Minutes |
|---|---:|
| Why pretrain? Static embeddings, contextual models, and the full reuse workflow | 15 |
| Text supplies its own targets: build self-supervised examples | 15 |
| Architecture orientation + BERT: masked prediction, 15% selection, conditional 80/10/10, one worked loss | 30 |
| GPT: causal prediction, shifted targets, training versus generation | 20 |
| T5: missing-span reconstruction | 15 |
| Synthesis: construct three recipes from the same sentence | 15 |
| Questions / break / pacing margin | 10 |

End with a visual bridge: how does a pretrained word predictor become a sentiment
classifier? Introduce abstractions through a visible example. Keep the first
calculation in a PAUSE panel with the solution on the following slide.

## Session 2 — How do we use the model?

| Part | Minutes |
|---|---:|
| Recall the three recipes and the learned parameters | 10 |
| Sentiment fine-tuning: head, backbone, frozen features versus full updates | 25 |
| Token labeling and extractive QA: different output interfaces | 20 |
| A small practical example: data, predictions, and held-out errors | 15 |
| Zero-shot / few-shot prompting versus fine-tuning | 20 |
| Data, scale, and limitations | 15 |
| Visual bridge from base predictor to instruction-following assistant | 5 |
| Questions / break / pacing margin | 10 |

Instruction tuning, preference optimization, LoRA, adapters, and quantization
remain in Lecture 09. The second session's date and any calendar adjustment have
not been assigned. Do not silently replace or renumber subsequent lectures.

## Preserved material

The complete earlier source is preserved unchanged in `previous-draft.qmd`.
`OUTLINE-previous.md` preserves its six-part plan. All images, styles, controls,
recorded evidence, and generation scripts remain in their original locations,
so the preserved draft retains working relative links and interactions.

Reuse especially:

- `#bert-corruption`: 15% selection and conditional mask/random/unchanged branches.
- `#bert-loss-pause` / `#bert-loss-solution`: visible givens and separate solution.
- `#family-recipes`, `#decoder-recipe`, `#seq2seq-recipe`: inspectable targets.
- `#training-generation`: parallel training and sequential generation.
- `#sentiment-head`, `#finetuning-updates`, `#qa-heads`, `#qa-span`: downstream uses.

The detailed small-model diagnostics and multiple optimizer/loss demonstrations
are a reusable reserve, not an obligation to include everything in the core.
Preserve reported failures and provenance when selecting measured evidence.

## Base lectures and visuals

Use content and actual diagrams from both supplied PDFs, with lecture and original
paper attribution. Page numbers below are PDF viewer numbers, starting at one.

- Stanford pp.10–11: embedding-only versus whole-model pretraining.
- Stanford p.19 (printed 20): pretraining/fine-tuning workflow.
- Berkeley pp.36 and 58: matched MLM/causal prediction diagrams.
- Stanford p.27 (printed 29), Berkeley p.38: BERT corruption recipe.
- Stanford p.36 (printed 38), Berkeley p.66: T5 span corruption.
- Berkeley pp.43–46: BERT task heads; p.77: fine-tuning versus in-context learning.
- Stanford p.49 (printed 51): one scaling figure, interpreted with its axes.

`TEACHING-DISCUSSION.md` records the initial audit and one-session proposal. Its
budget is superseded by this two-session plan; its source map remains useful.

## First section implementation

Six compositions: sentiment pipeline, static lookup, interactive contextual
comparison, a brief ELMo definition with its published Figure 1, Stanford paired
network figures, and staged parameter transfer. The context comparison takes
two minutes and the ELMo bridge one minute, retaining the 15-minute budget.
Controls and vector colors in the contextual comparison are schematic; they do
not report inference or measured semantic similarity. Source image provenance
is in `images/sources/README.md`. Each slide includes timed teaching notes.

Only the architecture transition has been added after these sections. The BERT masking/80–10–10 controls remain in
the preserved draft for reuse when that section is requested.

## Second section implementation

Five slides, 15 minutes: construct a source/input/target pair (3); compare two
questions from one sentence (3); PAUSE exercise (2); clickable enumeration of six
missing-word examples from one sentence (4); training loop and BERT bridge (3).

The source-selection and target-reveal mechanism reuses the earlier corpus lab's
approach in a standalone script. It manipulates six authored words and runs no
model. The solution restores the first draft’s enumeration and selected input/target
inspector for one sentence. The probability recap has been removed.
No numerical loss calculation or BERT corruption recipe is introduced yet.

## Architecture transition

Two slides, three minutes within the BERT block: restored three-family attention-path
map (2) and a large masked-position information-flow bridge into BERT (1).
Stop before the detailed BERT training section.
