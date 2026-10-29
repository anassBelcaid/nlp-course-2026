# Student project gallery

Students submit `project-proposal.yml` to the instructor. Submissions do not
publish automatically. Keep detailed proposal reviews outside this public repo.

After approval, add an entry to `projects.yml` with only the title, students,
description, and thumbnail fields. Images live in `images/`; use paths such as
`images/team-project.webp` in YAML, with alt text and attribution. An omitted
thumbnail uses the shared placeholder.

Set status to `Proposal approved`, `In progress`, or `Completed`. Optional
`report`, `code`, and `demo` fields accept full HTTPS URLs. Remove the fictional
entry when adding the first real project, and omit `example` for real teams.
Use `[]` for an empty gallery.

The root `student-projects.qmd` renders the YAML through `_cards.ejs.md`.
Run `quarto render student-projects.qmd` from the repository root to rebuild.
Cards appear in YAML order in a compact responsive grid, showing a thumbnail,
title, and student names. Descriptions and status remain in YAML for future
detail pages; they are not displayed on the cards. The proposal download remains a separate resource.
