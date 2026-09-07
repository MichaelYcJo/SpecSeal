# Implementation Plan: the record carries the fix a person can paste, and a cell it copies renders whole

## Summary

`round_record.py new` extracts four tables and drops everything else in the
report, so the paste-ready fix the findings format spends four paragraphs
requiring reaches no file. A `|` inside a copied cell splits the row, and every
renderer drops the extra columns, so the cell's content disappears from the
rendered record while surviving in the raw file.

Both are repaired inside the writer. **Neither needs a new mechanism**: the
file already carries `fenced_after`, built for this exact loss one section
over, and `cell()` already states the repository's position on a pipe in a row
it composes.

## Technical context

- `skills/code-review/scripts/round_record.py#fenced_after` — **[read]** copies
  every fenced block under a heading into the record, verbatim, prose excluded.
  Its docstring names the incident it was built for: *round 1 of #161's own
  chain read "Fix below (A)" in seven Grounds cells and carried none of them,
  and the fix pass rebuilt every one from a description.* That is #187, one
  section over and already solved. It is called for `## Executed probes` alone.
- `skills/code-review/scripts/round_record.py#cell` — **[read]** refuses a `|`,
  a newline, and a comma in the two comma-split rows. It composes the header
  rows; it is not on the path a report's table row takes.
- `skills/code-review/scripts/round_record.py#table_of` and `#table_body` —
  **[read]** the copy path. A report row is taken from `raw` at the section's
  indices and written through.
- `hooks/routing.py#round_number` — **[read]** `round-(\d+)\.md`, fullmatch on
  the basename, and `chain_check.py` filters `rounds/` through it. A sibling
  file named `round-1-report.md` does not fullmatch, so it would be ignored
  rather than read as round 1 — but `stray_records` is the check that decides
  whether an unexpected file in `rounds/` is tolerated, and it has to be read
  before any sibling shape is chosen.
- **[executed]** on the branch merged at `bc123aa`, five times: a 264-line
  report became an 82-line record with `grep -c '```'` answering 0. The
  orchestrator worked around it by posting each report as a comment on the
  pull request, which is durable and is not a file any clone contains.

**What breaks in 6 months.** A sixth section is added to the record and the
reviewer is told to write a heading for it, and nothing says which headings the
record reads. The repair puts the extraction behind the same named-heading
contract the four tables already have, so the list of what a report owes is one
list rather than two.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#187** — the record keeps the report verbatim below the tables | Prose nobody parses enters a file `chain_check.py` reads. Every fence-and-heading hazard this file already guards against — `swallowed`, the never-closed fence, the comment hider — exists because of prose in this position, and #169 spent three rounds on one of them | **No** |
| **#187** — `new` writes the report to `rounds/round-N-report.md` and the record links it | One record becomes two files a reader has to open in order, and `rounds/` gains a member `routing.round_number` does not match — which `stray_records` then judges. It also puts the artefact one hop away from the agenda, where the point is that the fix pass opens one file | **No** |
| **#187** — `new` extracts fenced blocks from a heading the reviewer writes, with `fenced_after` | The reviewer omits the heading and the record silently carries no fix. Mitigated the way the four tables mitigate it: the heading is in the findings format, and a round whose findings need a fix and whose section is empty is visible in the record itself | **Yes** — the mechanism, the argument and the incident are already in the file |
| **#189** — `new` refuses a row whose cell count does not match the header | A refusal stops an unattended run to ask a person, and there is nothing for the person to decide: the escape is always right. The ticket argues this on `CLAUDE.md`'s first goal and this plan agrees | **No** |
| **#189** — `new` escapes a bare `\|` inside a copied cell | An escaped pipe renders as a pipe, which is what the reviewer wrote, and the raw file gains a backslash a later reader might mistake for the reviewer's. Stated in the record rather than hidden | **Yes** |

**Why `cell()` is not the site, stated so the next reader does not unify them.**
`cell` refuses; the copy path escapes. A pipe in a value the writer composes is
the writer's bug and a refusal is the cheap answer. A pipe in a cell the writer
copies is the reviewer's text, and the writer's job there is to carry it, not to
judge it.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | A bare `\|` inside a copied cell is escaped as the row is written, in every table `new` copies and in `close`'s fix table. The record's row count matches its header | Cases over fixture reports for each table, each seen red first; the module's existing cases | 297e74e |
| 2 | `new` carries the reviewer's paste-ready fixes into a section of the record, extracted with `fenced_after` from the heading the findings format names. The empty arm writes a record rather than refusing | Cases for a report with one fix, with two, and with none, each seen red first | |
| 3 | The reviewer's contract names the heading — `skills/code-review/SKILL.md` §*Findings format*, and `docs/review-handoff-protocol.md`'s description of what the record carries | The documents; whatever case pins their wording | |
| 4 | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` | The fragments; `fold_ledger.py --check` | |

Phase 1 first, and the order is not arbitrary: #187 makes the fixes section the
durable home for a paste-ready fix, and a paste-ready fix is where a `|` comes
from. Escaping the cell before the section exists means the two never compound
in the same run — which is what #189's ticket says they did.

## Operational impact

`round-N.md` gains a section. Records already written have none, and every
reader of the record reads named sections, so an absent one is the state they
already handle. No migration.
