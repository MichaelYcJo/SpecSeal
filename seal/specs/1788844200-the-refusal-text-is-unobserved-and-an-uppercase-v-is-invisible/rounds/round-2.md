# 1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible — review round 2

| Field | Value |
|---|---|
| Target SHA | 0eed9fa1716caaf91eb90daf4218359108472ebe |
| Ran by | warden on claude-opus-5 |
| PR | 259 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A verifying round, spawned after round 1's fixes were committed and targeted at
the diff of those fixes: `cddf323..2bce8ab`. Its job was stated as the answers
rather than new findings, with one surface exempt — what the fixes themselves
created.

The central thing it had to judge: round 1 overturned the branch's claim that
`refusal` has seven elements all pinned, and the fix pass answered six on an
AST re-derivation, explaining seven as two readings — one `JoinedStr` part
split into the paragraph and the separator closing it, and the `"\n  "`
argument of the join promoted to an element. **The round was told to
re-derive the leaves itself and to say whether six is the count**, on its own
derivation rather than theirs, because this is the third counting of the same
expression and the first two were both wrong.

Then five more.

- **The two survivors**, and the fix pass's narrowing of round 1's
  description of the second — that moving the operand alone does not survive,
  because an assertion reads the separator before the first refused line. A
  survivor list that is itself incomplete is the same defect one level up.
- **Eight records, not four**, and the rule the fix pass applied: a document
  that is a contract made before the work, or a record of a moment, gets a
  correction block rather than a rewrite, so the fact that the plan was wrong
  does not disappear.
- **`seal/ledger.md` R3 corrected in place with a strikethrough** — whether
  that is this repository's form and whether the corrected text is true.
- **The reviewer's paste-ready case, deliberately not planted.** Whether that
  closes the finding honestly or defers it while calling it answered.
- **A near miss** — writing a ledger row, the fix pass nearly used a position
  coordinate that the reviewer's own paste-ready text carried; the checker
  caught it as `OLD-FORMAT`. Confirm no position coordinate reached any row.

Facts carried as executed by the orchestrator at round 1's target: the module
at 32 passed exit 0, ruff clean, and round 1's first survivor reproduced —
deleting one clause of the timer paragraph left the module at 32 passed.

Carried as not the round's to close: two ledger anchors left un-re-verified on
the orchestrator's instruction, taken at the closing commit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's finding 1 — the timer paragraph read at its ends, 86 characters between them unread | `tests/test_release_hygiene.py#test_the_refusal_prints_every_piece_it_builds` | answered | **Executed**: both of round 1's deletions re-run one at a time, `tests/__pycache__` cleared between and the file restored from bytes kept before the first write — 1 failed / 31 passed each, where they were 32 passed. Character-coverage map of `refusal("0.8.3", [first, second])`: **0 of 1186 characters** read by no assertion. Seven further mutations over the six leaves, each caught |
| 2 | Round 1's finding 2 — records stating the enumeration as complete | `seal/ledger.md:1356` · `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md` · `tests/test_release_hygiene.py:311` | answered | **Read**: eight records corrected, not four. Rewrite where the document states the current truth, correction block where it is a contract or a record of a moment. **Executed**: grep for a surviving `seven`/`four pieces`/`three separators` claim across the tree — nothing outside this work item's own directory, and the released `CHANGELOG.md` never carried it. The strikethrough form on the released row has three precedents in the same file |
| 3 | Round 1's finding 3 — the paragraph correcting the old false limit introduced a new one | `tests/test_release_hygiene.py:333-334` | answered | **Read**: the sentence *"pinning it would mean reading this file's own source"* is gone. What replaced it says the survivor **is** pinnable, names the method, and says it stays on the list until somebody plants the case. The pin itself is deferred to `questions.md` Q2 with the review orchestrator named as answerer in `overview.md` §Not done. That closes the finding as worded — the finding was a false sentence, and no assertion the finding required is missing |
| 4 | Round 1's finding 4 — ledger row S4 cited a document that states the superseded rule | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:18` | answered | **Read**: S4 now says two documents, not three, and says why the third was left alone. **Executed**: no `path:line` coordinate in any row of `seal/ledger.md` or `seal/ledger/*.md`; the scoped checker reports `0 old-format` |
| 5 | Round 1's finding 5 — the fixture wrote the running version as a literal | `tests/test_release_hygiene.py:363` | answered | **Executed**: the case now reads `RUNNING_IN_THE_FIXTURES`, whose value at this SHA is the same string the literal held, and the module is green |
| 6 | ⬜ The docstring calls the join's receiver an argument, and calls it *never a leaf* without the rule that makes it so | `tests/test_release_hygiene.py:337-338` | **fixed** `ad6f81a` | fixed at ad6f81a; **Executed**: in the parsed call, `func.value` is `"\n  "` and `args` is `[offenders]` — the string is the receiver, and `offenders` is the only argument. Bare `ast.walk` of the expression returns seven terminal nodes including that string; six is the count only under the flattening rule the same docstring states two sentences earlier. The count and the coverage are both right; the sentence supporting them is not |
| 7 | ⬜ A third survivor class outside the measured thirteen — insertion | `tests/test_release_hygiene.py#test_the_refusal_prints_every_piece_it_builds` | **fixed** `ad6f81a` | fixed at ad6f81a; **Executed**: seventeen mutations, twelve caught, five survived. Adding a sentence at the end of the timer paragraph, and adding a line between the refused lines and the routes, each leave the module at 32 passed. Not a contradiction of *"two mutations survive this set"*, and not fixable without rebuilding `refusal` in the test — recorded so the number lives in a record |
| 8 | ⬜ Two correction blocks declare a reach that leaves the superseded vocabulary standing below them | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/spec.md:30` · `plan.md:45` | **fixed** `ad6f81a` | fixed at ad6f81a; **Read**: `spec.md`'s block corrects *"the list above"*, and the acceptance table below it still reads *"builds its four pieces"* and *"any one of the three separators"*; `plan.md`'s block reaches the alternatives table's #206 row by name and leaves *"#203 as seven assertions"* in the row above it. **Executed**: all three separator mutations are caught, so every acceptance row is still satisfied — the vocabulary is superseded, not the criterion |
| 9 | ⬜ `overview.md`'s rationale says asserting the routes twice would be a second reader, and the case asserts them | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` | **fixed** `ad6f81a` | fixed at ad6f81a; **Read**: the cell reads *"five elements in the new case, the sixth in the case above it … Asserting it twice would be a second reader of the same thing"*, while the case does assert the routes, and its own docstring item 6 says so — *"read here and by the case above"*. The rationale predates the fix range and was carried through the seven-to-six rewrite unchanged |
| 10 | ⬜ Round 1's `Fixes checked by` reason is false at the commit that closed the record | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-1.md:9` | answered | the cell holds the value the ordering rule requires until a later round exists — `nobody — <why>` — and only the reason is stale. It is the cell `round_record.py close`/`new` overwrites with `round-2`, which this close does, so there is nothing left to write |

## Paste-ready fixes

```python
    Element 3 is where reading failed twice over. It split that constant into
    a paragraph and a trailing separator, and it promoted the `"\\n  "` the
    join is called ON — the receiver, not an argument — to an element of its
    own. Under the rule above it is inside element 4 rather than beside it;
    a bare `ast.walk` of the expression does return it, which is why the rule
    is stated before the count and not after.
```
```python
    A third class is unmeasured by design: nothing here pins that nothing was
    ADDED. A sentence inserted at the end of the timer paragraph, or a line
    inserted before the routes, leaves this module at 32 passed (round 2).
    Every element is read whole, so nothing can go missing; pinning that
    nothing was added means rebuilding `refusal` in the test.
```
```
the routes piece is read by both cases, and deliberately: the case above reads
it as the routes, this one reads it attached to the block that precedes it. The
five counted as new are the five nothing read before.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_release_hygiene.py:350-358` | round 1's 1 — fixed |
| round-1 | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md:19` · `tests/test_release_hygiene.py:311` | round 1's 2 — answered |
| round-1 | `tests/test_release_hygiene.py:333-334` | round 1's 3 — answered |
| round-1 | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:18` | round 1's 4 — answered |
| round-1 | `tests/test_release_hygiene.py:339` | round 1's 5 — fixed |
| round-1 | `tests/test_release_hygiene.py#refusal` | round 1's 6 — answered |
| round-1 | `tests/test_release_hygiene.py#VERSION_TOKEN` | round 1's 7 — answered |
| round-1 | `docs/flow.md:101` | round 1's 8 — answered |
| round-1 | `tests/test_release_hygiene.py:544-556` | round 1's 9 — answered |
| round-1 | `docs/issues-and-milestones.md:66-71` · `docs/flow.md:30` | round 1's 10 — answered |
| round-1 | `seal/ledger.md:1136` · `:1355` · `:1356` | round 1's 11 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether to plant the case pinning the check's own `assert not offenders, refusal(running, offenders)` | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/questions.md` Q2, with the decision stated in `overview.md` §Not done | the review orchestrator — already deferred by the fix pass with the answerer named, not re-opened here. Judged honest: the finding was a false sentence and the sentence is gone |
| Whether a case should pin the two documents that name the check agreeing | `questions.md` Q1 and ledger row S4 | the review orchestrator, or the repository owner it asks — already deferred, not re-opened |
| The empty code span in round 1's `fixed at <sha>` grounds cells | `skills/code-review/scripts/round_record.py`, where a `# RIDER:` comment names it as round 2's finding 9 of another work item and sends it to `seal/follow-up.md` | already recorded and predates this branch. Named here only so it is not mistaken for damage this round's record should carry |
