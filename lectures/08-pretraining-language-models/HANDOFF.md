# Pretraining lecture — resume here

## Authoritative revision — original Stanford slides, 12 November 2026

User rejected the seven authored GPT slides and explicitly requested the supplied
Stanford slides from printed44 to the end. Replaced the active `_gpt-trajectory.qmd`
include with `_stanford-ending.qmd`: all15 original pages42–56 (printed44–58)
as local high-resolution images. Original examples, GPT-2 generation, GPT-3
diagram, scaling charts, Chinchilla table, and limitations retained in order.
Original Stanford outline retained as a transition, not our course agenda.
Attribution on every page; primary-paper links and short corrections for GPT-2
year, historical Kaplan advice, equal-budget Chinchilla, and extraction vs
membership inference. Full extracted source text in speaker notes.
Validation: render passed; browser confirms65slides, all15 source slides fit,
no missing images or JavaScript errors, sentiment controls still work.
Active deck65slides. Prior seven authored slides preserved but inactive. This
replaces the remaining research sequence; do not append duplicate ICL/scaling
sections. User wants completion with minimal further iteration. Both source PDFs
in tmp are preserved. No commit or push requested.

## Latest increment — GPT trajectory, 12 November 2026

Instructor approved the 20-minute GPT → GPT-2 → GPT-3 section. Added seven slides
in `_gpt-trajectory.qmd`, styled by `gpt-trajectory.css`, after sentiment. Active
deck: 57 slides (39 Session 1 + 18 Session 2); 50 minutes of Session 2 authored.
Sequence/timing: trajectory2, GPT transfer2, GPT-2 text interface2, GPT-2 evidence3,
GPT-3 context3, GPT-3 Figure1.3 evidence4, synthesis/bridge4 =20min.
Sentiment remains the sole worked application. Prompt examples are explicitly
authored, not model outputs; no predicted scores invented. GPT evidence reuses
the existing SST-2 chart. GPT-2 Table3 PTB/1BW columns show uneven zero-shot
LM transfer; baselines have different setups. Original GPT-3 Figure1.3 extracted
locally with attribution and the paper's aggregate-score caveat. Models trained
on 300B tokens each do not represent an equal-compute comparison.

Validation: Quarto render passed. All seven new slides visually reviewed at
1440×1000; no overflow, missing images, or browser errors. Existing full/frozen
sentiment controls pass. `git diff --check` passes.

Next only after instructor review: in-context learning in depth (20min). Do not
automatically author scaling/Chinchilla or remaining sections. No commit/push yet.

## Active direction — GPT story and compute allocation, 12 November 2026

The instructor found the application-heavy session distracting and explicitly
requested sentiment as the only worked task, then the Stanford story from printed
slide44 onward. This supersedes all previous “next section” instructions below.

Removed `_token-span.qmd` and `_practical.qmd` from index includes, and removed
the practical controller/styles from the active deck. All source and evidence
files remain available as optional material. Moved the NER frozen-feature table
out of sentiment into `_optional-ft-evidence.qmd`. Retained the broad encoder task
map, sentiment head, update controls and general equations. Replaced the closing
NER/QA question with a bridge into the GPT trajectory. The active deck has 50
slides: 39 Session1 + 5 reuse + 6 sentiment. Session2 authored budget: 30 minutes.

Revised proposed Session2: reuse10, sentiment20, GPT trajectory20, in-context
learning20, scaling/compute25, capabilities/limits10, instruction-following bridge5,
margin10 =120min. New agenda appears in `_session2-plan.qmd` and `OUTLINE.md`.
Do not author remaining blocks automatically; next discuss/build GPT → GPT-2 → GPT-3.

Inspected Stanford PDF viewer pages42–56, corresponding to printed44 onward;
viewer page52/printed54 discusses Chinchilla. Primary references:
https://arxiv.org/abs/2005.14165 (GPT-3),
https://arxiv.org/abs/2001.08361 (Kaplan scaling),
https://arxiv.org/abs/2203.15556 (Chinchilla).
Important correction: Chinchilla used the same compute budget as Gopher, with
70B versus280B parameters and more training tokens. The lesson is allocation
between parameters and tokens, not simply more total compute. Do not conflate
Kaplan’s recommendations with Hoffmann’s later findings.

Validation: rendered successfully; browser verified 50 slides, no active NER/QA
or practical slides, no JavaScript errors or missing sentiment images. Revised
agenda and all sentiment slides fit the canvas; full/frozen controls pass.
Agenda and GPT bridge visually reviewed. `git diff --check` passes.

---

## Latest checkpoint — Recorded practical experiment, 12 November 2026

Instructor requested the planned 15-minute practical section. `_practical.qmd`
adds five slides: protocol (4 min), recorded learning curves/seed comparison (4),
two correct predictions (2), two errors/hypotheses (3), and prompting bridge (2).
63 slides total. Start `#/pr-setup`; stop `#/pr-bridge` for review.

Reuses existing `assets/evidence/section4.json` and the recorded-curve controller,
isolated into `assets/practical-controls.html` without old slide dependencies.
No retraining. Validated all six runs: prediction counts match final accuracies,
all 768 probabilities are bounded and agree with predicted classes. Protocol:
256 balanced train / 128 balanced validation examples, 80 steps, seeds 351–353,
identical downstream settings within each pair, pretrained vs random BERT-tiny.
Means: 63.28125% pretrained, 60.41667% random. Seed353 reverses the comparison.

Error analysis fixes pretrained seed351 (lowest recorded seed) and step80 before
selecting cases. Correct examples: original validation IDs183 and510. Errors:
IDs256 (false positive) and435 (false negative). Display original text, gold label,
prediction, and recorded p(positive). Selection is illustrative, not random; linguistic
scope explanations are hypotheses. No calibrated-confidence or causal-attribution
claim. The saved original strings are not a reconstructed tokenization trace.

Validation: Quarto rendered 63 slides. All five new slides visually inspected
at 1440×1000; no overflow, missing images, or JavaScript errors. Mean and all
three seed buttons produce the correct saved scores and pressed states; seed353
explicitly reports the reversal. Data consistency checks and `git diff --check`
passed. The last slide is `pr-bridge`.

Next after review: zero-shot / few-shot prompting versus fine-tuning (20 min).
The current section only poses the fixed-weights question; it does not develop it.

---

## Latest checkpoint — Token labeling and extractive QA, 12 November 2026

The instructor requested the next 20-minute section. `_token-span.qmd` adds
seven slides: BIO tagging/shared head (3 min), subword-label alignment (3),
question-conditioned QA diagram (3), boundary loss/constrained decoding (4),
EM versus token-overlap F1 (2), published SQuAD results (2), synthesis/bridge (3).
58 slides total. Start `#/ts-ner`; stop `#/ts-bridge` for review.

No elementary arithmetic exercise or invented model scores. NER annotations
are authored, and the subword split is explicitly hypothetical (u1/u2), not a
claimed tokenizer trace. First-piece supervision, ignored special/padding positions,
shared head, BIO validity, and entity-level evaluation are distinguished. Reuses
`assets/section4-diagrams/qa.html`; actual character/subword alignment is discussed.
The formal QA decoder includes ordered boundaries and a stated max-length rule.
SQuAD 1.1 answerable extraction is distinguished from QNLI and SQuAD 2.0.

Research: Devlin et al. (2019), Table 2, selected BERT rows with Dev/Test EM/F1
kept separate. The 93.2 test F1 condition uses seven models and prior TriviaQA
adaptation. Do not attribute it to a plain single model or treat the table as a
controlled pretraining ablation. Metrics follow Rajpurkar et al. (2016), §6.1.

Validation: 58-slide render succeeded. All seven new slides were visually
inspected at 1440×1000. Reduced excess spacing on the two NER slides without
shrinking text; final overflow checks pass. No missing images or JavaScript
errors; final slide is `ts-bridge`. `git diff --check` passed.

Next after review: the 15-minute practical experiment with inputs, predictions,
and held-out errors. Do not add it or prompting automatically.

---

## Latest revision — Encoder task context, 12 November 2026

Instructor requested a more research-oriented level for fifth-year students and
removal of the simple numerical example. Removed `ft-pause` and `ft-solution`
and the numeric gradient values. Keep the general loss and optimizer equations.
The more nuanced authored review is “Uneven, yet moving.”; no fabricated model
probabilities remain in this increment.

Added `#/ft-encoder-tasks` immediately before `#/ft-sentiment`, adapting the task
map from supplied Stanford PDF page 30 (printed 32). It explains SST-2, CoLA,
QQP/MRPC, STS-B, and MNLI/QNLI/RTE, their decisions/output types, and links original
papers plus GLUE and BERT. Notes distinguish QNLI sentence classification from
answer-span extraction and explain task-dependent metrics and separate adaptation.

The revised increment is seven slides / 25 minutes: task context 5, sentiment
diagram 3, head 3, updates 4, general gradients 2, evidence 5, bridge 3. Total deck
51 slides. Start at `#/ft-encoder-tasks`, stop at `#/ft-bridge`. This revision
supersedes the toy exercise and eight-slide description in the previous checkpoint.
Only the requested section is changed; later token/span heads await review.
Validation: 51 slides rendered; all seven revised slides passed 1440×1000
overflow checks. Task overview and general equations visually inspected;
full/frozen interactions pass; toy slides absent; no JavaScript errors or
missing images. `git diff --check` passed.

---

## Latest checkpoint — Sentiment fine-tuning, 12 November 2026

The instructor accepted the first Session 2 section and requested the proposed
25-minute sentiment section. `_finetuning.qmd` adds eight slides after `_reuse.qmd`:
CLS-to-label diagram (3 min), head/label-space definition (2), PAUSE calculation (3),
worked solution (3), full/frozen update control (4), gradient/update rules (2),
published feature-based/fine-tuning comparison (5), and output-interface bridge (3).
The deck now has 52 slides. Start `#/ft-sentiment`; stop `#/ft-bridge` for review.

Reused the preserved sentiment SVG, toy calculation, and full/frozen control.
`assets/sentiment-diagram.html` changes the example to “I loved this film.”;
`assets/finetuning-controls.html` isolates the existing update-mode mechanism
without loading the old recorded-experiment UI. It is a schematic switch, not
live optimization. Numbers h=[1,2], W=I, b=0 give p(positive)=0.731059 and loss
0.313262 nats. Labels and class order are explicit; no solution is on the prompt.

Research evidence: Devlin et al. (2019), §5.3/Table 7, CoNLL-2003 NER, BERT-base,
Dev F1 means over five restarts. Frozen last layer=94.9; frozen concatenated last
four=96.1; full fine-tuning=96.4. Frozen features feed a two-layer 768-dimensional
BiLSTM plus classifier, so this is not a head-only controlled ablation or sentiment
benchmark. Do not mix development and test columns or claim significance without
uncertainty. Only the interface motivation previews NER/QA; no token/span heads
are authored yet.

Validation: Quarto rendered 52 slides. All eight new slides were visually
inspected at 1440×1000 and passed overflow checks. Full/frozen switches, pressed
states, consecutive PAUSE/solution, final bridge, and image loading passed; no
JavaScript errors. Toy arithmetic independently checked. Enlarged mode buttons
and rechecked affected slides. `git diff --check` passed.

Next, after review: token labeling and extractive QA (20 minutes). The practical
experiment remains deferred, with the preserved diagnostic failures intact.

---

## Latest checkpoint — Session 2 first section, 12 November 2026

Instructor requested the first 10-minute section, emphasizing paper figures,
benchmark tables, experimental context, and research breakthroughs. Only this
increment is authored: agenda (1 min), saved weights/new representations (2),
three-recipe reuse recap (2), original GPT Table 5 evidence (3), and sentiment
bridge (2). Open `#/session-2`; stop at `#/reuse-bridge` for review.

`_reuse.qmd` and `reuse.css` follow `_session2-plan.qmd` after Session 1’s closing.
The deck has 44 slides. Reuses Session 1’s weights-to-states SVG; no new simulated
model outputs. The evidence table transcribes SST-2/MNLI/QNLI accuracies for the
full model and no-pretraining ablation from Radford et al. (2018), Table 5.
`assets/build_reuse_chart.py` generates the zero-based SST-2 chart. Explicitly
identify task supervision, the full model’s auxiliary LM objective, absent
uncertainty estimates, and the lack of a compute-matched comparison. Table 5
does not explicitly identify its evaluation split; do not invent one.

Validation: Quarto rendered 44 slides. Chromium at 1440×1000 confirmed
all five new slides fit the canvas, with no JavaScript errors; all five were
visually inspected. The paper table and chart are legible and cited. The first
full-deck pass loaded every image; final scoped checks leave earlier slides’
lazy images unloaded as expected. `git diff --check` passed.

Next, after review: discuss/develop sentiment fine-tuning (25 min). Do not
include classification equations, frozen/full update mechanisms, or later
sections until requested. Preserve both reference PDFs in `tmp/`.

---

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
