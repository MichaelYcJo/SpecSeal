# Feature Specification: the record carries the fix a person can paste, and a cell it copies renders whole

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/code-review/SKILL.md` §*And commit the record before commissioning the fixes* — *the report is a message in a session that ends; the record is a file the next segment opens* | The sentence the design rests on, and the one both tickets falsify: the record opens without the artefact the findings format requires |
| `skills/code-review/SKILL.md` §*Findings format* | A paste-ready fix for every 🔴/🟡, with every invented name marked at the line that uses it — four paragraphs of contract that reach no file |
| `CLAUDE.md` § *The goal a design is chosen against* | #189 has two shapes and the ticket already argues the trade on this clause: a refusal stops an unattended run to ask a person, and there is nothing for the person to decide |
| `docs/review-handoff-protocol.md` §*round-N.md — what this round did* | The record's contract with its reader, which is where a new section has to be declared |

## Scope

**In.**

- **#187** — `round_record.py new` carries the reviewer's paste-ready fixes into `round-N.md`, from a heading the reviewer writes, using the mechanism the file already has for the probes table.
- **#189** — a bare `|` inside a cell the record COPIES no longer truncates the row. The Verdicts table's every column, `## Executed probes`, `## Inherited coordinates`, `## Deferred`, and `close`'s `Commit or grounds`.
- The reviewer's contract gains the heading, in the one place a reviewer reads it: `skills/code-review/SKILL.md` §*Findings format*, and `templates/sdd-round.md` if it names the record's sections.

**Out.**

- Changing what `cell()` does. It composes the header rows and refuses a pipe outright, and that stays: a value the writer composes with a pipe in it is a bug in the writer, where a copied cell is the reviewer's own text.
- Carrying the report's prose. #187's second candidate is refused in `plan.md` with the reason.
- Anything about the four tables' own contract. This adds a fifth section; it does not touch what the four require.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A paste-ready fix reaches the record | Given a report with a fenced block under the fixes heading; when `new` runs; then `round-N.md` carries that block verbatim, fence and comments intact | A case over a fixture report, seen red first |
| Two findings' fixes stay apart | Given two fenced blocks under the heading; when `new` runs; then both are present and in the reviewer's order | The same case, second arm |
| A record with no fixes is still a record | Given a report whose findings are all ✅ and whose fixes heading is absent or empty; when `new` runs; then the record is written and says so, rather than refusing | A case for the empty arm — a verifying round that opens nothing writes no fix |
| A bare pipe renders | Given a Verdicts row whose Grounds cell contains `a \| b`; when `new` runs; then the record's row has exactly as many cells as its header, and the rendered cell shows the pipe | A case asserting cell count and content, seen red first |
| The pipe survives `close` | Given such a row; when `close` re-serialises it; then the row still matches the header | The same case, over `close` |
| A pipe in a fix table cell renders | Given `close`'s `Commit or grounds` carrying a pipe; when it runs; then the row matches its header | A case over the fix table |
| The reviewer is told where the fixes go | Given the findings-format section; when a reviewer reads it; then it names the heading the record extracts from | The document, and the case that pins the contract if the suite has one |

## Data & interfaces

`round-N.md` gains one section. `chain_check.py` reads named sections and tables; the new one is not among them, and whether it must be is settled in `plan.md`.

No CLI change. `new` takes the same arguments.

## Open questions → questions.md

None. The three shapes #187 names are settled in `plan.md`'s Alternatives, against the mechanism this file already carries.
