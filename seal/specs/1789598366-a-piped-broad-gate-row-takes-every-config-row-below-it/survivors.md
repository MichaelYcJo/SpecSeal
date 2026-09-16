# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — survivor exemptions

`survivor-check --range 0995f62f..HEAD` reports sixteen places after phase 4.
**One was a real survivor and is corrected in the range**, so it is not
exempted here: `seal/specs/1789445605-.../changelog.md` is a fragment that
ships into the same released section as this work item's own, so a reader
would have met *a pipe cannot be written* and *here is how it is written* in
one list. That bullet now records the measurement in the past tense and names
#415 as the repair in the same release.

The sixteen below are not stale copies of a corrected claim. They fall into
four kinds, and the kind is the grounds.

## A record of a work item that has already run says what that run found

Eleven of the sixteen are in `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/`.
That work item measured the defect and deliberately did not repair it — its
own `spec.md` lists `config_rows` Unchanged — and its records say so. Correcting
them would make a past run's records assert what a later branch did, which is
the same failure as re-pointing a ledger row instead of removing it: the claim
belonged to the code as it stood, and a record of a decision stays true
whatever the tree does afterwards. The round records of that work item are
exempt for the identical reason and are not reported here only because their
wording did not match.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789445605-…/overview.md:48` | `config_rows` is not repaired here because `spec.md` §*Data & interfaces* lists it **Unchanged** | A statement about what that work item's own scope excluded, and it was excluded. #415 is the work item that repaired it |
| `seal/specs/1789445605-…/overview.md:48` | The spec's claim is true about the refusal and false about the row | A finding that work item made about its own `spec.md`, at the time it made it |
| `seal/specs/1789445605-…/overview.md:48` | ` — escaped or not — stops the line being a row of that table, and `broad-gate` reports the row as ABSENT. | The measurement that work item executed on 2026-09-15, against the reader as it then stood |
| `seal/specs/1789445605-…/overview.md:48` | tee out.txt` → `[]`, the backslash-escaped spelling → `[]`, `bin/test -q && ruff check .` → the row. | Three values read through `config_rows` on 2026-09-15. The second reads differently today, which is what #415 changed; what the row records is the reading taken then |
| `seal/specs/1789445605-…/overview.md:64` | ` reader for three callers and one of them is a `PreToolUse` hook, so a change there is a change about every row | The reasoning for leaving the reader alone in that work item. It is still the reasoning #415 followed for `hooks/mode-gate.py`, which gains nothing |
| `seal/specs/1789445605-…/phases/phase-1.md:43` | tee out.txt` → `[]`, the backslash-escaped spelling → `[]`, `bin/test -q && ruff check .` → the row. | The same measurement in the phase record that took it |
| `seal/specs/1789445605-…/phases/phase-1.md:44` | End to end, the gate then reports the row as **absent** — a true message about the wrong cause. | What that phase measured end to end. The message changed in #415 phase 2; the record is of the run that met the old one |
| `seal/specs/1789445605-…/phases/phase-1.md:47` | That is a defect in the tree rather than in this phase, and it is not repaired here | The phase saying what it deliberately left, which is what a phase record is for |
| `seal/specs/1789445605-…/phases/phase-2.md:42` | The allowed list says so in the same cell that says a pipe is legal | True of the cell as that phase wrote it. The cell now says how the pipe IS written, and #415's own records carry that |
| `seal/specs/1789445605-…/plan.md:98` | It is the shared reader for three callers and one of them is a `PreToolUse` hook. | That plan's grounds for an alternative it rejected. A plan is a contract for work that has been done |
| `seal/specs/1789445605-…/questions.md:21` | `config_rows` stops reading at the first line that does not parse, so a piped `Broad gate` row takes every row below it | The question that became #415, stated as its asker measured it. #415's answer is that the sentence holds only where a row above already parsed, and that narrowing is in this work item's records and in `templates/config.md` |

**What would make these stop holding.** Each quote is the anchor. If one of
those records is ever rewritten to describe the tree as it stands rather than
as that run found it, it stops being history and becomes a claim, and the
exemption goes with the wording.

## A coincidence of phrasing about a different subject

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789518345-…/phases/phase-5.md:78` | The sentence was true about the reviewer and false about the sealer, and the `continue` is what made the falsehood unobservable | **A different subject entirely.** It is about a `continue` in the routing check and who a sentence described; the phrases it shares with the corrected text are *true about the* and *and false about the*. Correcting it would remove a true statement about another work item's finding to erase a coincidence of four common words |

## The destination of the text this range moved

| Path | Quote | Grounds |
|---|---|---|
| `hooks/config.py:98` | The header and the separator are this table's own furniture ABOVE its first row and somebody else's table BELOW it; | **This is where the removed comment went.** Phase 3 closed the copy of the loop in `tests/test_the_pull_request_language_is_the_repositorys.py`, and the two stop rules' reasoning — written there by two review rounds of #82 — moved into the implementation's docstring rather than being deleted. The check is reporting the move as a survivor, which is what it looks like from a diff |

## Docstrings about behaviour that did not change

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_mode_question_is_asked_once.py:112` | the header is this table's furniture ABOVE its first row | **Still true and still what the case asserts.** The header rule is untouched by this branch; what moved is where it is documented |
| `tests/test_the_pull_request_language_is_the_repositorys.py:621` | The other direction, so the fix above does not become a stricter rule than the one intended | **About the tolerant direction above the header**, which this branch did not change. The case is green over the one reader |
| `seal/ledger.md:519` | **Executed**: the first run of the parser returned `('---', '---')` as row one — a markdown separator has three pipes and two cells exactly as a real row does | **A shipped ledger row's Verified cell**, narrating a run taken in 2026-09-03. The separator rule it describes is unchanged; the row was re-read in phase 3 and carries a note saying so |
