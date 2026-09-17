# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — survivor exemptions

**Every row in this file used to silence nothing, and the cause was in the
first cell.** Round 2 measured the file as inert over three ranges with and
without `--exempt` and read that as the defect `seal/follow-up.md` tracks as
#371 / #308. It is not. `survivor_check.py#exempted` matches the first cell
against the candidate's PATH, and every row here was written `path:line` —
the spelling the check's own report prints for a survivor — so no row could
ever match. Measured in round 2's fix pass: one row written bare excused its
place and printed under `exempt`, the same row written with `:104` did not,
same range, same run. Every row below now carries a bare path, and the check
answers *every survivor is excused by a row above* instead of *no removed
wording is still standing* — two different facts that had been reading as one.

`path:line` was this file's own habit and nobody else's: 201 exemption rows
across the other work items are bare paths, and exactly one row elsewhere
carries a line number.

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
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/overview.md` | `config_rows` is not repaired here because `spec.md` §*Data & interfaces* lists it **Unchanged** | A statement about what that work item's own scope excluded, and it was excluded. #415 is the work item that repaired it |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/overview.md` | The spec's claim is true about the refusal and false about the row, and a template that promises a form nobody can write is the shape this work item exists to end. | A finding that work item made about its own `spec.md`, at the time it made it |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/overview.md` | ` — escaped or not — stops the line being a row of that table, and `broad-gate` reports the row as ABSENT. | The measurement that work item executed on 2026-09-15, against the reader as it then stood |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/overview.md` | tee out.txt` → `[]`, the backslash-escaped spelling → `[]`, `bin/test -q && ruff check .` → the row. | Three values read through `config_rows` on 2026-09-15. The second reads differently today, which is what #415 changed; what the row records is the reading taken then |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/overview.md` | ` reader for three callers and one of them is a `PreToolUse` hook, so a change there is a change about every row | The reasoning for leaving the reader alone in that work item. It is still the reasoning #415 followed for `hooks/mode-gate.py`, which gains nothing |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/phases/phase-1.md` | tee out.txt` → `[]`, the backslash-escaped spelling → `[]`, `bin/test -q && ruff check .` → the row. | The same measurement in the phase record that took it |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/phases/phase-1.md` | End to end, the gate then reports the row as **absent** — a true message about the wrong cause. | What that phase measured end to end. The message changed in #415 phase 2; the record is of the run that met the old one |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/phases/phase-1.md` | That is a defect in the tree rather than in this phase, and it is not repaired here | The phase saying what it deliberately left, which is what a phase record is for |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/phases/phase-2.md` | The allowed list says so in the same cell that says a pipe is legal, because a template that promises a form nobody can write is the shape this work item exists to end. | True of the cell as that phase wrote it. The cell now says how the pipe IS written, and #415's own records carry that |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/plan.md` | It is the shared reader for three callers and one of them is a `PreToolUse` hook. | That plan's grounds for an alternative it rejected. A plan is a contract for work that has been done |
| `seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/questions.md` | `config_rows` stops reading at the first line that does not parse, so a piped `Broad gate` row takes every row below it — measured on a four-row table returning `[('Mode', 'shared')]` alone. | The question that became #415, stated as its asker measured it. #415's answer is that the sentence holds only where a row above already parsed, and that narrowing is in this work item's records and in `templates/config.md` |

**What would make these stop holding.** Each quote is the anchor. If one of
those records is ever rewritten to describe the tree as it stands rather than
as that run found it, it stops being history and becomes a claim, and the
exemption goes with the wording.

## Round 1's fix pass — the range `c4e9c58b..HEAD`

That range corrects two claims of this work item's own records, so it reports
five places. **Three were real survivors and are corrected in the range**, not
exempted: `spec.md`'s A6 paragraph carried the same false generalisation as
`plan.md` did, and the W1 cell of `questions.md` and one changelog bullet both
said the refusal reports every row below as lost without the condition. That
is 🟡 1 and 🟡 2 arriving in the copies nobody had opened, which is what this
check exists for.

The two below are not stale copies of a corrected claim.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it/questions.md` | A file whose reading DOES move is a divergence row in `overview.md` naming the file — never a reason to weaken A6 into something that passes | **The rewrite's own words, on both sides.** The correction in `plan.md` keeps this sentence — it was always true and is not what 🟡 2 found wrong — so the phrase it shares is text the range ADDED as much as removed. Correcting it would delete a true instruction to erase an overlap with its own replacement |
| `hooks/config.py` | for line in text.splitlines(): if not seen_header: if CONFIG_HEADER.match(line): seen_header = True continue | **The loop `refusal` is built to walk in step with**, reported because the old `refused_row` walked it too and that copy is what the range removed. `config_rows` is the reader; its walk is untouched by this range and the whole point of `refusal` is that the two do not drift. Rewriting it to look less like the code it must agree with is the opposite of the repair |

## A coincidence of phrasing about a different subject

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/phases/phase-5.md` | The sentence was true about the reviewer and false about the sealer, and the `continue` is what made the falsehood unobservable | **A different subject entirely.** It is about a `continue` in the routing check and who a sentence described; the phrases it shares with the corrected text are *true about the* and *and false about the*. Correcting it would remove a true statement about another work item's finding to erase a coincidence of four common words |

## The destination of the text this range moved

| Path | Quote | Grounds |
|---|---|---|
| `hooks/config.py` | The header and the separator are this table's own furniture ABOVE its first row and somebody else's table BELOW it; | **This is where the removed comment went.** Phase 3 closed the copy of the loop in `tests/test_the_pull_request_language_is_the_repositorys.py`, and the two stop rules' reasoning — written there by two review rounds of #82 — moved into the implementation's docstring rather than being deleted. The check is reporting the move as a survivor, which is what it looks like from a diff |

## Docstrings about behaviour that did not change

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_mode_question_is_asked_once.py` | the header is this table's furniture ABOVE its first row | **Still true and still what the case asserts.** The header rule is untouched by this branch; what moved is where it is documented |
| `tests/test_the_pull_request_language_is_the_repositorys.py` | The other direction, so the fix above does not become a stricter rule than the one intended | **About the tolerant direction above the header**, which this branch did not change. The case is green over the one reader |
| `seal/ledger.md` | **Executed**: the first run of the parser returned `('---', '---')` as row one — a markdown separator has three pipes and two cells exactly as a real row does | **A shipped ledger row's Verified cell**, narrating a run taken in 2026-09-03. The separator rule it describes is unchanged; the row was re-read in phase 3 and carries a note saying so |

## Round 2's fix pass — the range `5137e934..HEAD`

That range rewrites the walk in `hooks/config.py#refusal` and one sentence of
`changelog.md`, so it reports five places. **None is a stale copy of a
corrected claim**, and four of the five are a stock Python idiom the rewrite
happened to stop using.

| Path | Quote | Grounds |
|---|---|---|
| `.github/scripts/close_issues_on_release.py` | `return None, False` | **A stock idiom, in a function about GitHub issues.** The removed walk returned `None, False, []` for every way of not having a refused line; this one answers whether an issue number resolved. The two share the words and nothing else |
| `tests/test_a_merged_ticket_says_so_on_the_tracker.py` | `return None, False` | The same idiom in a fake GitHub API, for the same reason |
| `tests/test_waiver_decided_at_start.py` | `lines = text.splitlines()` | **The shared phrase is `for i, line in enumerate(lines)`.** That walk reads the waiver question's tables out of `CLAUDE.md`; the walk this range rewrote read `seal/config.md`'s. Rewriting a loop so that it looks less like every other loop in the tree is not a repair |
| `tests/test_waiver_decided_at_start.py` | `lines = text.splitlines()` | The same walk, one case further down |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | the row is in the file, below a line the reader refused | **Still true and still what the case asserts.** `changelog.md`'s bullet gained the condition that a row below a refused line is named unreachable *read off the line that actually stopped the reader*; this case's fixture has ONE refused line, so the row really is below the line the reader refused and the message is exact. The two-refused-line shape has its own case beside it |

## The destination of the text this range moved — `0995f62f..HEAD`

| Path | Quote | Grounds |
|---|---|---|
| `hooks/config.py` | row under the first such header, in order. | **This is where the removed copy went.** Phase 3 closed the reimplementation of the table reader in `tests/test_the_pull_request_language_is_the_repositorys.py`, whose docstring opened with this sentence; the one reader's docstring has always opened with it. The check is reporting the removal of the copy as a survivor in the original, which is what it looks like from a diff |
