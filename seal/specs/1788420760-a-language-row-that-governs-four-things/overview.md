# A language row that governs four things — overview

<!-- The memo the review reads first: what rung this sits on, what was
verified and how, and what nobody has answered. -->

## Rung

**A skill's instructions.** Nothing here executes: two rows of a markdown
table, and the documents that tell a session how to read them. The repository
decides a rung by behaviour, and a skill's instructions are behaviour — a
session reads them and writes differently.

Not a public API and not a gate's verdict: no checker parses these rows, and
nothing refuses a commit over them. The pins are text assertions, which is
what a claim in a skill can have.

## What was verified

**Executed** — `tests/test_the_pull_request_language_is_the_repositorys.py`
(66 cases), the full suite, `ruff check .`, `ruff format --check .`, and
`evidence_check.py --strict .`. Each is named against what it covers in the
ledger fragment.

**Read** — nothing load-bearing. Every claim about what a document says is
asserted by a case that reads that document as text, which is how #82 built
this file's pins and how they stay honest.

## Not verified

| Item | Who must answer |
|---|---|
| Whether a session actually writes Korean records when the row says Korean. Nothing can assert that: the row is read by a model, and the pins can only check that the instruction is present and says what it should | the repository owner, on the first repository that sets it |
| Whether `Record language` should have a third value for *the same as the commit row*, rather than being set twice in a repository that wants both | the repository owner, if anyone asks for it |
| The full suite, `ruff check .` and a repository-wide format check | the review orchestrator's broad gate, once the rounds settle |

## Fed back into the spec

The posted review report moved from the record row to the commit row while
this was being written, because the premise behind putting it with the records
turned out to be false — posting and recording are separate acts producing
different texts, which `skills/code-review/SKILL.md:136` and `:325` say
plainly. `spec.md` carries the correction and the measurement beside it.
