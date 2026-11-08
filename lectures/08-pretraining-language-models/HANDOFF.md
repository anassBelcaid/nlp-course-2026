# Pretraining lecture — resume here

Checkpoint: 8 November 2026. Instructor approved the current sequence and asked
to stop after the architecture transition. This file records decisions, not
permission to author the rest of the lecture automatically.

## Exact next step

Resume with the detailed BERT section, following the agreed plan below. Check
with the instructor which increment to develop; discuss content and sources
before authoring when requested. Work section by section and stop for review.
Do not restart the approved opening or add the entire remaining lecture at once.

## Approved material and files

The rebuilt `index.qmd` has 16 slides:

| Slides | Content | Source |
|---|---|---|
| 1–3 | Title, purpose-made visual overview, Session 1 TOC | `index.qmd` |
| 4–9 | Why pretrain? Static/contextual embeddings, ELMo, whole-model pretraining | `_why-pretrain.qmd` |
| 10–14 | Text supplies targets; sentence exercise; training loop | `_self-supervision.qmd` |
| 15–16 | Encoder-only / decoder-only / encoder–decoder map; bridge to BERT | `_architecture-transition.qmd` |

The instructor particularly approved the opening's varied visual teaching style.
ELMo now includes a definition, paper link, and the paper's Figure 1, rather
than appearing as an unexplained name.

Slides 11–13 were revised after feedback: keep slide 11's illustration, ask on
slide 12 how many examples a single sentence yields under the stated
one-hidden-position rule, and inspect all six input–target pairs interactively
on slide 13. Use “The cat sat on the mat”. Count positions, including the two
occurrences of the. These are constructed targets, not measured model predictions.
Students already understand output probabilities; avoid another basic recap.

The architecture overview must precede BERT. Slide 15 reuses the earlier draft's
attention-path diagram; slide 16 returns to the full running sentence and asks
how to use both sides without revealing the answer. Detailed BERT training has
not been added. These two slides take 3 minutes inside BERT's 30-minute block.

## Agreed teaching approach

- Two sessions, each at most 2 hours. Full timing tables are in `OUTLINE.md`.
- The instructor is learning this chapter while preparing to teach it. Speaker
  notes should explain the reasoning, definitions, transitions, and figure reading.
- Use both supplied Stanford and Berkeley lectures for content and diagrams;
  cite primary papers for exact recipes and evidence.
- Vary slide compositions: diagrams, examples, published figures, equations,
  demonstrations. Keep a coherent visual identity without a monotonous template.
- Use JS/Quarto interaction only when it helps expose a mechanism or dependency.
- Start abstractions from small concrete examples; keep intermediate values visible.
- Put first calculations in a conspicuous PAUSE panel; put solutions on the next slide.
- Keep type and diagrams readable and use the full canvas deliberately. Do not
  shrink labels to force a layout. Follow the repository's `AGENTS.md`.
- Preserve effective earlier components, especially BERT masking and conditional
  80/10/10 demonstrations. Reuse selectively; the old deck was overwhelming.
- Label illustrative values versus actual measurements and explain evidence settings.
- End each part with a synthesis and a motivating question. End completed lectures
  with a visual bridge, leaving the next mechanism for the next lecture.
- Session 2's TOC appears only after the completed Session 1, never at the opening.

## Agreed BERT block — 30 minutes total

| Part | Minutes | Status |
|---|---:|---|
| Three-family architecture orientation and BERT bridge | 3 | Slides 15–16 complete |
| Connect the missing-word exercise to BERT | 2 | Next |
| Inputs: tokens, special tokens, position information, encoder | 4 | Planned |
| Select 15%; conditional 80% mask / 10% random / 10% unchanged | 8 | Reuse preserved interactive components |
| Which positions contribute to loss? PAUSE then worked solution | 5 | Planned |
| Original BERT's sentence pairs and next-sentence prediction | 3 | Brief historical context |
| Sentence classification / token labeling; bridge to generation | 5 | Planned |

The target remains the original token under all corruption branches. Distinguish
architecture (information access) from objective (what to predict). BERT, GPT,
and T5 are representative recipes, not exclusive tasks for their architectures.
After BERT: GPT 20 min, T5 15 min, synthesis 15 min, plus the session's 10-minute
margin. Earlier sections are 15 minutes each. No calendar dates were assigned;
do not renumber later lectures. Lecture 09 retains instruction tuning and efficient
adaptation topics.

## Preserved material and source map

`previous-draft.qmd` preserves the earlier 57-slide deck. Its styles, controls,
figures, generation scripts, and evidence are retained. `OUTLINE-previous.md` is
historical; `TEACHING-DISCUSSION.md` is the initial audit and its one-session
proposal is superseded by `OUTLINE.md`.

Useful anchors in the old deck:

- `#bert-corruption`: selection and conditional corruption controls.
- `#bert-loss-pause`, `#bert-loss-solution`: exercise / solution.
- `#family-recipes`, `#decoder-recipe`, `#seq2seq-recipe`: input/target comparisons.
- `#training-generation`: parallel training versus sequential generation.
- `#sentiment-head`, `#finetuning-updates`, `#qa-heads`, `#qa-span`: downstream uses.

Source PDFs currently live in the repository's untracked `tmp/`:

- `tmp/cs224n-2026-lecture07-pretraining.pdf`
- `tmp/CS288_sp26_08_Pretraining_Finetuning_Prompting.pdf`

Keep those PDFs for subsequent authoring; they are not part of this commit.
Extracted figures used by current slides are safely stored in `images/sources/`,
with attribution and extraction details in `images/sources/README.md`. The
original overview is `images/pretraining-overview.png`. The current slides do
not need `tmp/` to render. See `OUTLINE.md` for the PDF page map, including BERT,
T5, task heads, and scaling. Page references mean PDF viewer pages, not printed
slide numbers. Do not depend on temporary extracted text or browser scripts in
`/tmp/` surviving a restart.

## Build, preview, and verification

From the repository root:

```sh
quarto render lectures/08-pretraining-language-models/index.qmd
python3 -m http.server 4202 --bind 127.0.0.1 --directory _site
```

Only start the server if that port is not already serving this site.
Local preview: http://localhost:4202/lectures/08-pretraining-language-models/index.html
Transition: append `#/family-architecture-map`.
Quarto may need permission to access its cache outside the workspace.

At this checkpoint the deck rendered successfully with 16 slides. Browser checks
at 1440×1000 found no overflow in the revised exercise or transition slides;
transition screenshots were visually inspected. All six example selections
updated the input and target correctly. Context controls and source images were
also checked. The original draft remains a reserve, not an approved finished
version of the new two-session lecture.

This checkpoint is a local commit. No remote push or publication was requested.

## Suggested restart message

“Read lectures/08-pretraining-language-models/HANDOFF.md and let's continue
with the BERT section from our approved plan.”
