# Round 2 — verifying round, review report

| Field | Value |
|---|---|
| Work item | `1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible` |
| Branch | `fix/203-204-205-206-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible` |
| Target SHA | `0eed9fa1716caaf91eb90daf4218359108472ebe` |
| Fix range reviewed | `cddf323..2bce8ab`, plus `0eed9fa` which adds only the closed record |
| Base | the open release branch this work item is cut for, at `bcf48b8` (= `origin/main`). Named by SHA rather than by number, because this branch edits the check that refuses a version at or above the running one |
| Reviewed in | a `git clone --no-local` of the repository at the target SHA, at a path unique to this round |
| Broad gate | not yet — the full suite, the repository-wide lint and the typecheck are the orchestrator's, once, after the rounds settle. Nothing here needs a fix, so the gate is now due |

## What this round did, and what it did not

This is a verifying round. Its target is the diff of round 1's fixes, and its
job is whether each of round 1's five findings is actually closed. It re-derived
the element count from the syntax tree instead of taking the fix pass's table,
and it re-ran the survivor set instead of taking the fix pass's numbers.

It did not re-walk the branch. `VERSION_TOKEN`, the loaded-set enumeration and
the arrangement measurements were untouched by the fix range — confirmed by
`git diff --name-only` and by the four hunk headers, all four inside the two
neighbouring cases — so round 1's verdicts 7 to 11 stand on round 1's grounds
and are not re-derived here.

**Nothing in this round needs a fix.** Five corrections are recorded below, all
of them prose in the run's own paperwork, and none of them is a defect the
release would ship.

## The count is six, derived here rather than taken

`ast.parse` of the expression `refusal` returns, in this clone at the target
SHA:

```
BinOp(+) chain → 4 operands
  op1  JoinedStr, 3 parts
  op2  Call        "\n  ".join(offenders)
  op3  Constant    "\n\n"
  op4  Call        what_to_write_instead()
```

Expanding the `JoinedStr` and treating each `Call` as one atom gives **six**
leaves. That matches the fix pass's answer, and it is the third counting of
this expression and the first one I can reproduce from the tree rather than
from a sentence about it.

Two things make the six honest rather than merely stated.

- **The rule that produces it is written down beside it.** Flatten the `+`
  chain, expand the f-string's parts, stop at a call. Without that rule
  `ast.parse` hands back seven terminal nodes for this expression, because the
  `"\n  "` bound to `.join` is a `Constant` like any other. The docstring states
  the rule two sentences before it states the count, so a reader can check it.
- **The count no longer carries the coverage claim on its own.** I mapped every
  character of `refusal("0.8.3", [first, second])` against the eight substrings
  the case reads: **0 of 1186 characters are read by nothing**, where round 1
  measured 103 uncovered in three runs, the largest 86. That is the measurement
  the count was standing in for, and it now holds independently of how anyone
  chooses to count leaves.

## The two survivors hold, and the narrowing holds

Seventeen mutations, each on its own, `tests/__pycache__` cleared between and
the file restored from bytes read before the first write. Twelve caught, five
survived — and the five collapse to the two the fix pass names plus one class it
does not.

- **Survivor 1 — the check's own `assert` line.** Handing it a literal leaves
  the module at 32 passed. So does changing the arguments it passes to
  `refusal`: with zero offenders in the tree that line never renders, which is
  the same hole in a second spelling.
- **Survivor 2 — the routes emitted ahead of the refused lines**, each separator
  carried along with the piece it precedes. 32 passed. **And the narrowing is
  real**: moving the routes operand alone, leaving the separators where they
  are, is caught — the assertion reading `"\n  "` before the first refused line
  goes red. The fix pass narrowed round 1's description of this survivor and the
  narrower statement is the true one.
- **A third class, outside their thirteen — insertion.** Adding a sentence to
  the end of the timer paragraph, or an extra line between the refused lines and
  the routes, each leaves the module at 32 passed. Every element is read whole,
  so nothing can go *missing*; nothing pins that nothing was *added*.

The docstring's claim is *"Two mutations survive this set"*, and that is true of
the thirteen it ran. The insertion class is not a contradiction of it. It is
recorded below so the number is in a record rather than in this transcript, and
it needs no fix: pinning the whole text is rebuilding `refusal` inside the test,
which is the design this case exists not to be.

## The eight records, and the rule that decided how each was corrected

Round 1 named four documents. The fix pass found eight and applied one rule: a
document that is a **contract made before the work**, or a **record of a
moment**, gets a correction block appended; anything else is rewritten.

| Document | What it is | Treatment | Judged |
|---|---|---|---|
| `tests/test_release_hygiene.py` — both docstrings | code | rewritten | right. A docstring is read as the current truth |
| `seal/ledger.md` R3 | a released row | struck through, correction beside it | right, and the form has precedent — rows R3 at `:1383`, F1 at `:1182` and F3 at `:1184` already carry `~~…~~ (**corrected by …**)` |
| `seal/ledger/<id>.md` S2 and S4 | this branch's own unreleased rows | rewritten | right. The row has not shipped, and the claim it makes is the current one |
| `changelog.md` fragment | an unreleased entry | rewritten | right, same reason |
| `overview.md` | the living summary | rewritten, with a correction note in the cell | right |
| `spec.md` | the contract | correction block | right |
| `plan.md` | the contract | correction block | right |
| `phases/phase-2.md` | the record of a moment | two correction blocks | right |

I checked for a ninth and found none outside the work item's own directory. The
released `CHANGELOG.md` never carried the count, and `docs/` never stated it.
`tests/test_release_hygiene.py:277` — where the phrase `the other six elements`
lived in the code — now reads *"The routes are one of the six leaves … the other
five are read whole by … below"*, and both halves are true.

What the rule leaves behind is one class the correction blocks declare
themselves out of, recorded as correction ③ below.

## `seal/ledger.md` R3, and the near miss

R3's corrected text is true. The struck sentence claimed *every* element was
deleted and caught; the parenthetical beside it keeps the honest half — the
seven mutations were real and every one of them was caught — and names *every*
as the word that was never measured. That distinction is the one worth keeping,
and the row keeps it.

**No position coordinate reached any ledger row.** Grepped for `path:line` in a
code span and bare, across `seal/ledger.md` and every `seal/ledger/*.md`: none.
Row S4 now cites `docs/flow.md`'s sentence about #179 by description rather than
by line, which is what the checker's `OLD-FORMAT` arm exists to force. The
scoped run reports `0 old-format`.

## The check the run still fails, which is this round

`chain_check.py --baseline <the release branch>` refuses at
`rounds/round-1.md:0`: `Pass` is checked beside `Fixes checked by: nobody`. That
is the state this verifying round exists to resolve, not a defect — the way out
the refusal itself names is one round at the diff of those fixes, then
`round-1.md`'s cell naming `round-2` and this round's record reading `no fixes to
check`. Recorded so the orchestrator knows the exit is the paperwork rather than
the code.

`0eed9fa` also changed round 1's `Contract changes` and `New units` from
`none — the fixes are not yet written` to bare `none`, which is correct
forward-looking bookkeeping: once that record's checker cell names a round, the
longer spelling fails.

**Both cells are true.** No top-level name was added or removed between the two
ends of the fix range — 51 before, 51 after, by AST — and the expression
`refusal` returns is byte-identical across it. So there is no new unit for this
round to judge as code, which is the whole reason the round is cheap.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's finding 1 — the timer paragraph read at its ends, 86 characters between them unread | `tests/test_release_hygiene.py#test_the_refusal_prints_every_piece_it_builds` | answered | **Executed**: both of round 1's deletions re-run one at a time, `tests/__pycache__` cleared between and the file restored from bytes kept before the first write — 1 failed / 31 passed each, where they were 32 passed. Character-coverage map of `refusal("0.8.3", [first, second])`: **0 of 1186 characters** read by no assertion. Seven further mutations over the six leaves, each caught |
| 2 | Round 1's finding 2 — records stating the enumeration as complete | `seal/ledger.md:1356` · `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md` · `tests/test_release_hygiene.py:311` | answered | **Read**: eight records corrected, not four. Rewrite where the document states the current truth, correction block where it is a contract or a record of a moment. **Executed**: grep for a surviving `seven`/`four pieces`/`three separators` claim across the tree — nothing outside this work item's own directory, and the released `CHANGELOG.md` never carried it. The strikethrough form on the released row has three precedents in the same file |
| 3 | Round 1's finding 3 — the paragraph correcting the old false limit introduced a new one | `tests/test_release_hygiene.py:333-334` | answered | **Read**: the sentence *"pinning it would mean reading this file's own source"* is gone. What replaced it says the survivor **is** pinnable, names the method, and says it stays on the list until somebody plants the case. The pin itself is deferred to `questions.md` Q2 with the review orchestrator named as answerer in `overview.md` §Not done. That closes the finding as worded — the finding was a false sentence, and no assertion the finding required is missing |
| 4 | Round 1's finding 4 — ledger row S4 cited a document that states the superseded rule | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:18` | answered | **Read**: S4 now says two documents, not three, and says why the third was left alone. **Executed**: no `path:line` coordinate in any row of `seal/ledger.md` or `seal/ledger/*.md`; the scoped checker reports `0 old-format` |
| 5 | Round 1's finding 5 — the fixture wrote the running version as a literal | `tests/test_release_hygiene.py:363` | answered | **Executed**: the case now reads `RUNNING_IN_THE_FIXTURES`, whose value at this SHA is the same string the literal held, and the module is green |
| 6 | ⬜ The docstring calls the join's receiver an argument, and calls it *never a leaf* without the rule that makes it so | `tests/test_release_hygiene.py:337-338` | open | **Executed**: in the parsed call, `func.value` is `"\n  "` and `args` is `[offenders]` — the string is the receiver, and `offenders` is the only argument. Bare `ast.walk` of the expression returns seven terminal nodes including that string; six is the count only under the flattening rule the same docstring states two sentences earlier. The count and the coverage are both right; the sentence supporting them is not |
| 7 | ⬜ A third survivor class outside the measured thirteen — insertion | `tests/test_release_hygiene.py#test_the_refusal_prints_every_piece_it_builds` | open | **Executed**: seventeen mutations, twelve caught, five survived. Adding a sentence at the end of the timer paragraph, and adding a line between the refused lines and the routes, each leave the module at 32 passed. Not a contradiction of *"two mutations survive this set"*, and not fixable without rebuilding `refusal` in the test — recorded so the number lives in a record |
| 8 | ⬜ Two correction blocks declare a reach that leaves the superseded vocabulary standing below them | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/spec.md:30` · `plan.md:45` | open | **Read**: `spec.md`'s block corrects *"the list above"*, and the acceptance table below it still reads *"builds its four pieces"* and *"any one of the three separators"*; `plan.md`'s block reaches the alternatives table's #206 row by name and leaves *"#203 as seven assertions"* in the row above it. **Executed**: all three separator mutations are caught, so every acceptance row is still satisfied — the vocabulary is superseded, not the criterion |
| 9 | ⬜ `overview.md`'s rationale says asserting the routes twice would be a second reader, and the case asserts them | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` | open | **Read**: the cell reads *"five elements in the new case, the sixth in the case above it … Asserting it twice would be a second reader of the same thing"*, while the case does assert the routes, and its own docstring item 6 says so — *"read here and by the case above"*. The rationale predates the fix range and was carried through the seven-to-six rewrite unchanged |
| 10 | ⬜ Round 1's `Fixes checked by` reason is false at the commit that closed the record | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-1.md:9` | open | **Read**: the cell reads `nobody — the fixes are not yet written` while the verdict cells in the same file name `9aadedf` and `2bce8ab`. The value `nobody — <why>` is what the ordering rule requires until this round exists; only the reason is stale, and it is the cell the orchestrator overwrites with `round-2` when it verifies this report |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py -q` at the target SHA in a fresh `git clone --no-local` | 32 passed, exit 0 |
| `ast.parse` of the expression `refusal` returns — full dump, the flattened `+` chain, the `JoinedStr` parts, and the receiver/argument split of the join | 4 operands; operand 1 is one `JoinedStr` of 3 parts; **6 leaves** under flatten-`+`/expand-`JoinedStr`/`Call`-as-atom; **7 terminal nodes** under bare `ast.walk`; the join's receiver is `"\n  "` and its only argument is `offenders` |
| Character-coverage map of `refusal("0.8.3", [first, second])` against the eight substrings the case reads | **0 of 1186 characters** read by nothing, where round 1 measured 103 |
| 17 mutations of `refusal` and of the check's own `assert`, each on its own, `tests/__pycache__` cleared between, the file restored from bytes read before the first write, and the baseline re-run and byte-compared at the end | 12 caught, 5 survived. Survived: the check's `assert` handed a literal (32 passed); the same line with its arguments reordered (32 passed); the routes ahead of the refused lines with each separator carried (32 passed); a sentence inserted at the end of the timer paragraph (32 passed); a line inserted before the routes (32 passed) |
| The narrowing — the routes operand moved ahead alone, separators left in place | **caught**, 1 failed / 31 passed. The fix pass's narrower statement of survivor 2 is the true one |
| Round 1's two closed deletions, re-run | both **caught**, 1 failed / 31 passed each |
| Nine further mutations over the six leaves — opening sentence gutted, `{running}` deleted, the closing `"\n  "` narrowed, the join receiver narrowed, the join dropping all but the first offender, `"\n\n"` narrowed, the routes call replaced by a literal, a mid-sentence clause of the paragraph deleted, the paragraph's two clauses reordered | all **caught**; the routes replacement turns two cases red, the rest one each |
| Top-level names defined in the module at each end of the fix range, by AST | 51 before, 51 after, none added and none removed — `New units: none` confirmed |
| `git diff --name-only cddf323..2bce8ab` and the hunk headers of the one `.py` file | 9 files; all four hunks inside the two neighbouring cases; `VERSION_TOKEN` and the `[vV]?` widening untouched |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict --ledger seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md .` | 5 ok · 1 drifted · 0 broken · **0 old-format**, exit 2 — the drifted anchor is the case whose docstring the fixes rewrote, which the orchestrator is taking at the closing commit. `--reverify` was NOT run |
| Grep for a `path:line` coordinate, in a code span and bare, across `seal/ledger.md` and `seal/ledger/*.md` | none — the near miss did not land |
| Grep for a surviving `seven element` / `four pieces` / `three separators` / `three documents` claim across the whole tree | nothing outside this work item's own directory; the released `CHANGELOG.md` and `docs/` never carried either count |
| `grep -n '~~' seal/ledger.md` | 7 hits across 6 rows — the strikethrough-with-a-correction form has precedent at `:1182`, `:1184` and `:1383` |
| `python3 skills/code-review/scripts/chain_check.py --baseline <the release branch>` | exit 1 — `rounds/round-1.md:0`, `Pass` checked beside `Fixes checked by: nobody`. The state this round resolves |
| `uvx ruff check` and `uvx ruff format --check` on `tests/test_release_hygiene.py` | exit 0 and exit 0 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether to plant the case pinning the check's own `assert not offenders, refusal(running, offenders)` | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/questions.md` Q2, with the decision stated in `overview.md` §Not done | the review orchestrator — already deferred by the fix pass with the answerer named, not re-opened here. Judged honest: the finding was a false sentence and the sentence is gone |
| Whether a case should pin the two documents that name the check agreeing | `questions.md` Q1 and ledger row S4 | the review orchestrator, or the repository owner it asks — already deferred, not re-opened |
| The empty code span in round 1's `fixed at <sha>` grounds cells | `skills/code-review/scripts/round_record.py`, where a `# RIDER:` comment names it as round 2's finding 9 of another work item and sends it to `seal/follow-up.md` | already recorded and predates this branch. Named here only so it is not mistaken for damage this round's record should carry |

## Paste-ready fixes

Nothing here needs a fix. The three blocks below are the ⬜ corrections, offered
so the wording is available rather than described.

Correction ⑥ — `tests/test_release_hygiene.py`, replacing the two lines that
call the receiver an argument:

```python
    Element 3 is where reading failed twice over. It split that constant into
    a paragraph and a trailing separator, and it promoted the `"\\n  "` the
    join is called ON — the receiver, not an argument — to an element of its
    own. Under the rule above it is inside element 4 rather than beside it;
    a bare `ast.walk` of the expression does return it, which is why the rule
    is stated before the count and not after.
```

Correction ⑦ — appended to the survivor paragraph, so the third class is in the
docstring rather than only in a round record:

```python
    A third class is unmeasured by design: nothing here pins that nothing was
    ADDED. A sentence inserted at the end of the timer paragraph, or a line
    inserted before the routes, leaves this module at 32 passed (round 2).
    Every element is read whole, so nothing can go missing; pinning that
    nothing was added means rebuilding `refusal` in the test.
```

Correction ⑨ — `overview.md`, the third row's Grounds cell, replacing the
sentence about a second reader:

```
the routes piece is read by both cases, and deliberately: the case above reads
it as the routes, this one reads it attached to the block that precedes it. The
five counted as new are the five nothing read before.
```

---

The two terminal lines. Round 1's five findings are all closed, each on a
measurement I made rather than on the fix pass's account. The five corrections
above are prose in the run's own paperwork — a docstring sentence about the
syntax tree, a survivor class recorded for completeness, two correction blocks
whose declared reach stops short, a stale rationale cell and a stale reason in a
record cell the orchestrator overwrites. None of them is a defect a release
would ship, and none of them contradicts a measurement.

Nothing found here leaves the root, drops a record or raises. The refusal text
is a test-time message, the module is green at the target SHA, and every record
touched is prose.

Needs a fix: no

Loses a record or crashes: no

## Proof block

Opened, at `0eed9fa1716caaf91eb90daf4218359108472ebe`:

- `tests/test_release_hygiene.py` — `refusal` and the two cases around it in full, `RUNNING_IN_THE_FIXTURES`, and the whole file through `ast.parse`
- `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-1.md` (whole) and `rounds/round-1-report.md` — the head, the findings list and the proof block
- `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/` — `spec.md`, `plan.md`, `overview.md`, `questions.md`, `changelog.md`, `phases/phase-2.md`
- `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md` (whole)
- `seal/ledger.md` — rows R1 and R3 in full, and every line carrying `~~`
- `seal/config.md`
- `docs/review-chain-spec.md` — §*`Fixes checked by` has to name a checker the repository can confirm*, and the `Contract changes` / `New units` rows
- `docs/review-handoff-protocol.md` — §*The fix surface* and §*The `Fixes checked by` field*
- `skills/code-review/scripts/round_record.py` — the `close` header and the `# RIDER:` comment on the fix-table reader
- `skills/code-review/scripts/chain_check.py` — usage
- `bin/test`

Carried from round 1 rather than re-derived: verdicts 7 to 11 — the two
lookarounds, the loaded-set enumeration, #205's four arrangements, #206's
sentence, and the direct `seal/ledger.md` edits. The fix range touches none of
the code they rest on, confirmed by `git diff --name-only` and the four hunk
headers.

Declined, and named per §3 of the agent contract: no instruction in this round's
prompt asked for a check the contract excludes. The full suite, the
repository-wide lint and the typecheck were not run and are the orchestrator's.
`evidence_check.py --reverify` was not run, as instructed.
