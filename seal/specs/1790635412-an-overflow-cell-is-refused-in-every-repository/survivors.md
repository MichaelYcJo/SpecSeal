# Survivors — an overflow cell is refused in every repository

Phase 4's sweep (`survivor-check --range a7f146a8..65640dc1`) reported nine
places. None presents the old enforcement or the old grading as current.
Six are records of shipped or framing work that quote the state they were
written against, one is a dated note in a released ledger row, and two are
statements that are still true.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` | `--strict`\`, where DRIFTED and MALFORMED are exit 2, and this tree would come back NOT SEALED. | a shipped work item's spec, quoting the notice that work item wrote; it records what 1790381328 built and is not a statement about the tree now |
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` | It becomes: `::warning::evidence ledger reports drift or a malformed coordinate — each row above names its verdict and what to do`. | the same shipped spec, quoting the warning it wrote |
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` | Exit codes: 0 clean · 1 drift or malformed only · 2 broken or old-format | the same shipped spec, quoting the module docstring it wrote |
| `seal/releases/0.11.3.md` | so exit 1 has two causes and the sentence names both verdict words | a dated note in a released row's Notes cell, recording the state on the day it was written; this work item's `Corrected 2026-09-29` note on the same row follows it and states the third cause |
| `seal/releases/0.15.5.md` | without `--strict`, lets a malformed coordinate through with the rest of exit 1, and `--strict` still refuses it | still true: the claim is about a malformed coordinate, which the lenient recipe still lets through and `--strict` still refuses. The row carries this work item's `Re-read 2026-09-29` note saying the pages now say the same of `OVERFLOW` |
| `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md` | module docstring: "Three verdicts name something a person must touch either way and all three are printed" | this work item's frame, quoting the advisor's docstring as it stood before the build as grounds for changing it |
| `docs/the-evidence-ledger.md` | A row under no header is counted against the five columns `templates/ledger.md` declares for a ledger row | still true: the shipped arm counts a header-less row against `LEDGER_COLUMNS`, the five columns that header declares, and the sentence's account of #501 is history |
| `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md` | A row under no header is counted against the five columns `templates/ledger.md` declares for a ledger row | a shipped work item's plan, the policy wording that work item wrote; still true for the reason the row above gives |
| `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/spec.md` | The shared file and the release files hold 767 table body rows in all; | a shipped work item's spec, recording a count taken on its own day |
