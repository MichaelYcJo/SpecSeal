# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — overview

The record replaces the report as the fix pass's agenda, and it arrived
without the artefact the findings format spends four paragraphs requiring
(#187) and with the one cell that could still hold a fix truncating without a
word (#189); the record now carries the reviewer's fenced blocks and
re-serialises every copied row with its pipes escaped.

## Where spec and implementation diverged

| Side | Text | Which won | Grounds |
|---|---|---|---|
| `plan.md` | *"`new` escapes a bare `\|` inside a copied cell"* — the verdict names escaping and does not say how a cell boundary is found | the plan, with the finding rule settled by measurement | The plan settled escaping over refusing and left the reading unspecified. The sweep it asked for answered it: eight over-wide rows in 125 records, all eight with the pipe inside a code span, one of them in a probes command and one in the Finding column — so a code-span-aware reading is taken first, and the fold into the last column is the fallback. Recorded in `phases/phase-1.md` and as R1 of the ledger fragment |
| #187 | names the section `## Fix sketches` | the findings format's own word | The same skill uses *sketch* for the artefact that fails — *"arrived as sketches that read as paste-ready and were not"* — so a heading named after the failure would be the one word in the record with two meanings. The heading is `## Paste-ready fixes` |
| `spec.md` | *"The reviewer's contract gains the heading, in the one place a reviewer reads it: `skills/code-review/SKILL.md` §Findings format, and `templates/sdd-round.md` if it names the record's sections"* | four documents, not two | `agents/warden.md` §Report is what a warden actually has open while writing a report, and it carried a sentence — *"reads nothing else of the report"* — that told the reviewer to describe a fix rather than fence one. `docs/review-handoff-protocol.md` owns the record's format and had no row for the section |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the orchestrator — `agent-contract` §2 makes the broad gate theirs, run once after the rounds settle. Narrow runs here: 684 cases over the record modules and 637 over the document modules, both green, plus `uvx ruff check` and `ruff format --check` scoped to the three changed Python files |
| Whether the eight over-wide rows already committed in other work items' records should be corrected | the owner — they belong to `1788184145`, `1788433011` and `1788501054`, and this branch does not edit another work item's record. Each is a finding for the work item that wrote it |
| Whether `## Paste-ready fixes` should be read by `chain_check.py` at the pull request | the owner — `spec.md` left it to `plan.md` and `plan.md` added no checker, so the section is a declaration like `## Executed probes`. A round that opened a 🔴 and wrote no block is visible in the record and refused by nothing |
| ✅ Whether a `\|` actually RENDERS as a pipe — the property the whole #189 arm assumes, which every case in this branch asserts the PARSE of rather than the render | **executed by the review orchestrator against GitHub's own renderer**, round 1's ❓ 10: `gh api -X POST /markdown --mode gfm` over a two-column table whose first cell holds `` `a \| = b` `` returns two `td` elements, the code span rendering a plain pipe. Recorded in `rounds/round-1.md` row 10 and carried forward by `rounds/round-2.md` row 14 |

## What was fed back into the spec

Nothing was added to a policy document. Three clauses were *inferred during
implementation* and live in the ledger fragment rather than in `spec.md`,
because they are facts about the code this work item wrote:

- **R1** — which reading of a copied row is taken, and the measurement that
  ruled out folding the surplus into the last column.
- **R2** — that the empty paste-ready section states what was observed and
  never that no fix was needed, because a generator cannot tell those apart.
- **R3** — that `swallowed` reads two lists, `READ_HEADINGS` for headings and
  `REPORT_TABLES` for rows, because only a table can lose its rows to a fence
  while its heading stands.

`seal/ledger.md`'s F1 was narrowed by R3 and is corrected in place rather
than removed: its anchor still resolves, and the half of it about the row
loop is still true.
