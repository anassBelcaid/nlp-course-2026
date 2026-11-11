# Pretraining lecture — resume here

## Latest checkpoint — Session 1 written notes, 11 November 2026

Created `notes/08-pretraining-language-models/index.qmd` for the completed Session 1,
with HTML and PDF outputs. Notes expand the objective formulas, softmax gradients,
BERT corruption and context gradients, GPT target alignment, and T5 span/decoder
conventions. Four static diagrams, worked exercises, ten bibliography entries,
and a guided paper-reading list replace reliance on slide animations.

The instructor prefers detailed formula explanations and more bibliography
citations in PDFs; this preference is saved in the root authoring guide.
The schedule now links Session 1 slides, notes, and PDF. Its earlier-draft link
is removed; the draft itself and both reference PDFs in `tmp/` are preserved.
The schedule’s pretraining row also includes BERT, T5, GPT, and ELMo papers,
the Stanford/Berkeley lectures, and four coding/documentation links for masked
LM training, causal LM training from scratch, and T5.
Session 2 is still not authored. Continue only after instructor review.

---

## Latest checkpoint — Session 1 ending, 11 November 2026

T5 was accepted (“excellent”). The instructor approved and requested the final
15-minute synthesis. **Slides 35–39 are now authored for review**; Session 1 has
all planned content. Start at `#/synthesis-pause`. Stop at `#/session-1-closing`.
Session 2's plan is preserved but is NOT included or newly authored yet.

New files: `_synthesis.qmd` and `synthesis.css`. Five slides: PAUSE construction
activity (4 min), worked solution (3), context/parameter comparison (2), weights
versus states and targets (3), and animated sentiment-adaptation bridge (3).
The exercise fixes its corruption and boundary conventions, with no solution on
the prompt slide. GPT uses the existing no-START, five-target window; T5 retains
the paper-style final sentinel, source EOS, target EOS, and decoder START.

The ending combines pretrained parameters with new labeled examples, leaving
adaptation unresolved. It does not teach the Session 2 head or update equations.
The deck now has 39 slides and a Session 1 budget of 102 minutes of material plus
18 minutes of margin. The 15-minute synthesis includes the closing bridge.

Keep the established focus on pretraining and reuse. Attention, prediction,
and AR decoding mechanics have already been taught. Both reference PDFs remain
in `tmp/`, and the old draft is preserved. Do not delete the PDFs during cleanup.
Next: instructor review of the ending, then discuss the first Session 2 increment.

Validation: Quarto rendered 39 slides. Chromium at 1440×1000 found no content
overflow, missing images, or JavaScript errors. The PAUSE is immediately followed
by its solution; the final slide is the sentiment bridge, and Session 2 is absent.
All five new slides were visually inspected. Comparison-card whitespace was
reduced without shrinking text. `git diff --check` passed.

---

## Previous checkpoint — T5 increment, 11 November 2026

GPT is complete. The instructor approved the 15-minute T5 outline and requested
its implementation. **T5 slides 30–34 are now authored for review**, not yet
approved. Review at `#/t5-spans`. Stop before the Session 1 synthesis.

Files: `_t5.qmd`, `t5.css`, `assets/t5-controls.html`, and the locally saved
`images/sources/t5-span-construction.png`. Five slides: span construction (3 min),
interactive source/target inspector (4), reconstruction loss and gradient paths
(4), text-to-text reuse (3), and a visual synthesis bridge (1). Total 15 minutes.
Reuse remains a preview; detailed adaptation is still reserved for Session 2.

The instructor's emphasis remains pretraining. Prediction mechanics, attention,
and autoregressive decoding are assumed knowledge. The preserved cat/mat example
and its cat-sat extension are reused. The control constructs examples, not model
outputs. Sentinels and EOS are distinct; all non-padding target tokens receive
loss. Encoder parameters learn through decoder cross-attention dependencies.

Both full reference PDFs remain in `tmp/`; do not remove them during cleanup.
The older draft is unchanged. Only the 15-minute three-recipe synthesis remains
in Session 1, including its final visual bridge to sentiment adaptation. The
session budget stays 102 minutes of material plus 18 minutes of margin.

Validation: Quarto rendered 34 slides. Chromium at 1440×1000 found no content
overflow, missing images, or JavaScript errors. Both span selections were checked
against their expected source/target token sequences, including sentinels and EOS.
The new slides were visually inspected; the loss slide spacing and gradient path
were refined. `git diff --check` passed.

---

## Previous checkpoint — GPT pretraining increment, 11 November 2026

BERT was accepted (“that's good”). The instructor then requested GPT and agreed
that its focus must be **pretraining**, because prediction mechanics and AR LMs
have already been taught. Do not restart those explanations.

New slides 26–29 in `_gpt.qmd` are authored for review: corpus → reusable weights
(3 min), supervision comparison (4), checkpoint use/weight updates (3), and a
visual T5 bridge (2). Total 12 minutes, replacing the original 20-minute block.
Session 1 now has 102 minutes of planned material plus 18 minutes of margin.
`gpt.css` and `assets/gpt-controls.html` provide scoped styling and the small
weight-lifecycle switch. No new model outputs are claimed. The preserved draft
is unchanged. Both reference PDFs remain in `tmp/` and MUST be retained.

Validation: rendered 29 slides; Chromium at 1440×1000 found no overflow,
missing images, or JavaScript errors. Both weight-lifecycle modes were checked.
The four new slides were visually inspected; the comparison slide’s spacing
was corrected without reducing text size.

Review starts at `#/gpt-pretraining`. Stop before authoring T5. Its planned
15 minutes and the 15-minute session synthesis remain to be developed.

---

## BERT checkpoint — 11 November 2026

The approved 16-slide opening is followed by a newly authored **nine-slide BERT
increment (slides 17–25), awaiting instructor review**. Do not treat it as approved
or continue with GPT automatically. Start review at `#/bert-mlm`.

`_bert.qmd`, `bert.css`, and `assets/bert-controls.html` contain this increment.
Timings: MLM connection 2 min; inputs 4; selection 3; corruption inspector 5;
loss PAUSE 2 and solution 3; NSP 3; task-head preview 3; GPT bridge 2 = 27 min.
Together with the approved architecture orientation, BERT occupies 30 minutes.
The preserved branch inspector and loss exercise were reused; the inspector now
uses the running cat sentence. Its standalone script omits the old deck's
unrelated model-evidence fetch. The earlier draft remains unchanged.

Validation: Quarto rendered 25 slides; Chromium at 1440×1000 found no content
overflow across all slides, no missing images, and no JavaScript errors. All
three corruption branches were clicked and confirmed to retain cat as the
target. The nine new slides were visually inspected after transitions settled.

The two source PDFs were restored by the instructor after a cleanup removed
them. Both are present in `tmp/` (Stanford 56 pages; Berkeley 114 pages).
**Retain these reference PDFs during future proposal-file cleanup.** Extracted
figures remain local and the slide deck does not require the PDFs to render.

The 8 November checkpoint below is historical. Its 16-slide approval still
applies, but BERT is now authored for review. The previous checkpoint and student
project updates were pushed to origin/main; this new increment is not committed.

---

## Previous checkpoint

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
