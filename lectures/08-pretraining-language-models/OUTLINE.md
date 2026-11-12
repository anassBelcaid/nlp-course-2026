# Pretraining Language Models — two-session teaching plan

Accepted structure: two sessions of at most two hours each. Rebuild incrementally
and stop for instructor review after each requested section.

## Current review stage

Read `HANDOFF.md` first. The active deck contains65slides and ends with the15
original Stanford reference slides (printed44–58 / PDF42–56), reproduced with
attribution. They replace the rejected seven-slide GPT rewrite and cover GPT,
GPT-2 generation, GPT-3, scaling, compute allocation, capabilities and limitations.
Do not append duplicate planned sections. Earlier detailed NER/QA and practical
sections remain optional. The original PDFs in tmp must be preserved.

## Session 1 — How does pretraining work?

| Part | Minutes |
|---|---:|
| Why pretrain? Static embeddings, contextual models, and the full reuse workflow | 15 |
| Text supplies its own targets: build self-supervised examples | 15 |
| Architecture orientation + BERT: masked prediction, 15% selection, conditional 80/10/10, one worked loss | 30 |
| GPT: familiar AR objective as pretraining, supervision comparison, checkpoint reuse | 12 |
| T5: missing-span reconstruction | 15 |
| Synthesis: construct three recipes from the same sentence | 15 |
| Questions / break / pacing margin | 18 |

End with a visual bridge: how does a pretrained word predictor become a sentiment
classifier? Introduce abstractions through a visible example. Keep the first
calculation in a PAUSE panel with the solution on the following slide.

## Session 2 — From model reuse to scale (revised 12 November)

| Part | Minutes |
|---|---:|
| From pretraining to reuse | 10 |
| Encoder task context + sentiment as the only worked application | 20 |
| GPT → GPT-2 → GPT-3: research trajectory and changing use | 20 |
| Zero-shot / few-shot prompting and in-context learning | 20 |
| Scaling laws and compute allocation: parameters versus training tokens | 25 |
| What pretraining learns, memorization, bias, and limitations | 10 |
| Visual bridge to instruction-following assistants | 5 |
| Questions / break / pacing margin | 10 |

Source route: Stanford PDF viewer pages 42–56 (printed 44 onward). Use original
GPT, GPT-2, GPT-3 papers, Kaplan et al. (2020), and Hoffmann et al. (2022).
Avoid repeating AR prediction and attention. Treat early scaling recommendations
and later compute-optimal findings as a developing empirical story, not universal
laws. Chinchilla uses fewer parameters and more training tokens at the same
training-compute budget as Gopher; distinguish total compute from compute allocation.

Retain `_token-span.qmd`, `_practical.qmd`, their assets and recorded results, and
`_optional-ft-evidence.qmd` for optional use. Do not silently reinsert them. The
current active deck contains reuse, sentiment, and the original Stanford research sequence.
Instruction tuning and efficient adaptation stay in Lecture 09. Dates remain unset.

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

The approved architecture transition is followed by the BERT increment described
below. Its masking/80–10–10 control reuses the preserved draft’s interaction.

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

## BERT increment — authored for review, 11 November 2026

Nine slides in `_bert.qmd` add the remaining 27 minutes of the BERT block:
MLM connection (2), input embeddings (4), selection (3), reused corruption
inspector (5), PAUSE loss exercise (2), worked solution (3), historical NSP (3),
task-head preview (3), and a visual bridge to GPT (2). The existing two-slide
architecture orientation supplies the first 3 minutes.

Keep detailed fine-tuning in Session 2. At this BERT checkpoint, GPT, T5, and Session 1 synthesis remained
unwritten. The GPT update below supersedes that status. New interactions are schematic, and loss values
are illustrative. No new model run or benchmark claim is introduced.

## GPT increment — revised scope, 11 November 2026

The instructor emphasized that predictions, Transformers, and AR language models
are already covered. Do not reteach causal attention, shifted-target mechanics,
probability factorization, or sequential decoding. The accepted revision is
12 minutes instead of 20; keep the saved 8 minutes as margin (18 total).

Four slides in `_gpt.qmd`: corpus → reusable weights (3 min); compare BERT/GPT
supervision with the same sentence and familiar AR loss (4); inspect weight
updates during pretraining versus fixed weights at ordinary use (3); bridge to
separate-source span reconstruction (2). The old #training-generation example
is reused only as a weight-lifecycle control, not a generation lesson. This old
example was static; the new mode switch is a lightweight teaching interaction,
not a model simulation. All displayed continuations are authored.

Remaining: T5 (15 min) and Session 1 synthesis (15 min), after instructor review.
Session 2 remains unchanged. Sources: Berkeley PDF pp. 36, 57–59; Stanford p. 31;
Radford et al. (2018), §3 for the original pretraining/transfer workflow.

## T5 increment — authored for review, 11 November 2026

Five slides in `_t5.qmd`, 15 minutes: introduce span construction (3), inspect
source and target with one-word/multiword gaps (4), trace loss and encoder/decoder
updates (4), preview text-to-text reuse (3), and bridge to the final comparison
(1). Uses the preserved cat/mat recipe and multiword extension, plus the T5
paper figure from Berkeley p. 66, also shown in Stanford p. 36.

No new prediction tutorial or numerical loss exercise. The interactive control
is deterministic example construction. Exact teaching sequences use the paper's
final-sentinel convention, explicit EOS, and aliases for special tokens; they
are not claimed to be a production tokenizer trace. The original draft and
reference PDFs remain intact. Next: the 15-minute Session 1 synthesis, after review.

## Final synthesis — authored for review, 11 November 2026

Five slides in `_synthesis.qmd`: a PAUSE construction activity (4 min), its worked
solution (3), the visibility/parameter comparison (2), weights versus contextual
states and target labels (3), and the purposeful sentiment-adaptation bridge (3).
Total 15 minutes, including the ending. The first solution appears on the next
slide, with no hidden answers or new model measurements on the prompt.

The comparison reuses earlier examples and preserves this lecture's exact
boundary choices. No new model, attention tutorial, or numerical loss exercise
is introduced. Session 1 is now fully authored at 39 slides, 102 minutes of
material plus 18 minutes of margin. Session 2 remains unstarted in the rebuilt
deck; its stored outline remains the next discussion reference.
