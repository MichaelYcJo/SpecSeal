# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — review round 5

| Field | Value |
|---|---|
| Target SHA | e8f767ec9748ffc28208f6ff83fc60c2fa8181b4 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #828 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `e8f767ec9748ffc28208f6ff83fc60c2fa8181b4..e8f767ec9748ffc28208f6ff83fc60c2fa8181b4`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round for round 4's fix range `2e211cc6..23c230fe`: whether `landings` now reads a place only from a token that is wholly a path form (a code span's whole content, or a whitespace-separated word outside spans), so a `#name` apart from its path, a backslash or `+`-joined token whose tail is a path, and a path with a space land nowhere, while every shape the records use (`mod.py:4-5`, `./mod.py:5`, `mod.py#u()`, `mod.py:5,`, `(mod.py:5)`) still lands; that the depth walk's reading is unchanged; that the reframed-first-record case now pins the `previous_pair == stopped` guard; Q6 at 26; and the spec, changelog, ledger A8 and the docstring.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | A path form followed by a member or a parameter (`mod.py::u::inner`, `mod.py#u.attr`, `mod.py::u[a-b]`) is no longer read, so round 4's confirmation that a class method lands on its class no longer holds; no document names it and no case pins it | `skills/code-review/scripts/round_record.py#path_forms` | answered | docs/round-record-spec.md says the form is a whole token, a code span or a word, so `mod.py::u::inner`, `mod.py#u.attr` and `mod.py::u[a-b]` are not path forms and land nowhere, the fail-closed direction the spec chose; the reviewer found 0 such cells in 820 fix-owing rows across four tags and 138 PR heads; a class method still lands through `path:line`; executed: each such shape `first` at `2e211cc6` and `no` at the target; matches the whole-token sentence and the permissive direction; corpus scan, 820 fix-owing rows, none uses it |
| 🟢 | round 4's yellow finding 1 is closed — a `#name` apart from its path lands nowhere | `skills/code-review/scripts/round_record.py#path_forms` | confirmed | executed: four fragment shapes `no` at the target, `first` at `2e211cc6`; with the switch off the five S5 parameters fail |
| 🟢 | round 4's yellow finding 2 is closed — a path that is the tail of its token lands nowhere, for a backslash, a plus, a space inside a span and three more joins | `skills/code-review/scripts/round_record.py#PATH_FORM_RE` | confirmed | executed: `fullmatch` as `search` fails the three tail parameters; a bare path with a space is two words, which A8 scopes out |
| 🟢 | round 4's yellow finding 3 is closed — the reframed-record case sees the `previous_pair == stopped` guard | `tests/test_a_fix_of_a_fix_is_counted.py#test_a_reframed_record_is_written_and_starts_the_count_at_no` | confirmed | executed: guard off, the touched parameter fails; restored, it passes |
| 🟢 | every shape the records use still lands — the five the prompt names, the three plain forms, `./`, `@hash`, an en-dash range, a form in parentheses, in bold or bare | `tests/test_a_fix_of_a_fix_is_counted.py#test_a_location_carrying_its_py_path_still_lands` | confirmed | executed: the shape probe and the module, 58 passed; the parenthesis count dropped fails `mod.py#u()` |
| 🟢 | the depth walk's reading is unchanged | `skills/code-review/scripts/round_record.py#location_units` | confirmed | read: an early return behind a flag only `landings` passes; executed: the depth and framer modules, 43 passed |
| 🟢 | Q6 is still 26, all at round 3, with #814 and #801 first then second | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | executed: replay over the four tags with 138 pull request heads; identical landings before and after the fix on 164 record pairs |
| 🟢 | the round-record spec, the changelog, ledger A8 and the docstrings say what the code does | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | confirmed | read: each against the code; executed: evidence-check and correction-check exit 0, freeze diff empty |

## Paste-ready fixes

```markdown
unit has not changed. The form is a whole token, a code span or a word: a path
that is the tail of a longer token, a form with a member or a parameter after
its unit (`path::C::m`, `path#C.m`, `path::case[a]`), and a `#name` apart from
its path, are no form; a line inside a method, `path:line`, lands on its class.
```
```python
        # Round 5's note 1: a form with a member or a parameter after its
        # unit is a whole token that is not the form, so it lands nowhere.
        "`mod.py::u::inner`",
        "`mod.py::u[a-b]`",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_fix_of_a_fix_is_counted.py` at the target, in the round-5 scratch clone | 58 passed, exit 0 |
| A test_tmp shape probe, 48 `Location` shapes over the module's two-round fixture, at the target and in a second clone at `2e211cc6` | exit 0 in both; the rows are the table under *What lands nowhere* and ⬜ 1 |
| `bin/test` on the two location cases and the reframed case, with the `previous_pair == stopped` guard off and `fullmatch` turned into `search` | 4 failed (the three tail parameters, the reframed case with `touched=True`), 33 passed, exit 1 |
| The two location cases with `paths_only` ignored | 5 failed (the five new S5 parameters), 30 passed, exit 1 |
| The keep cases with the parenthesis count dropped | 1 failed (`mod.py#u()`), 9 passed, exit 1 |
| A test_tmp Q6 replay, `round_record.py` at the target and at `2e211cc6`, in a bare clone with 138 pull request heads and the four tags | both: 164 record pairs, 3 unresolved, 2 refused; over the tags 36 reach `first`, 26 reach `second`, all at round 3; identical landings on every pair across all 142 refs |
| A corpus scan of the `Location` cell of every 🔴 and 🟡 row in 529 distinct round records and reports at the tags, the pull request heads and the target | 820 rows; one cell loses a pair under the whole-token reading, the round-1 fragment cell at `v0.18.0` |
| `bin/test tests/test_a_fix_pass_may_add_a_unit.py tests/test_the_chain_goes_back_to_its_framer.py` | 43 passed, exit 0 |
| `bin/evidence-check --strict .` at the target | exit 0, 0 drifted, 0 broken |
| `bin/correction-check --range 4b363e68...HEAD` | exit 0, no correction marker dropped, no released ledger file changed |
| `git diff --stat 4b363e68...HEAD -- seal/releases seal/ledger.md` | empty |
| `round-record new --round 5` from this report, in a fresh scratch clone at the target | exit 0; `Fix of a fix` reads `no`, `Needs a fix` and `Loses a record or crashes` read `no`, `Pass` unchecked while ⬜ 1 is open; round-4.md's `Fixes checked by` set to round-5. The generator's chain-check printed a notice that the changelog fragment predates `23c230fe`, a docstring-only commit, so the fragment still says what ships |
| The broad gate — the full suite, the repository-wide lint and the typecheck over the branch | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:2396` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:3933` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2373` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:4715` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:28` | round 1's ⬜ 5 — answered |
| round-1 | `skills/code-review/scripts/round_record.py#landings` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py#fix_pass_units` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py#runs_of` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py#units_named_earlier` | round 1's ❓ — out of verified scope |
| round-2 | `skills/code-review/scripts/round_record.py:2434` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:2426` | round 2's 🟡 2 — fixed |
| round-2 | `docs/round-record-spec.md:697` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:27` | round 2's ⬜ 4 — answered |
| round-2 | `skills/code-review/scripts/chain_check.py#fix_of_a_fix` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/chain_check.py#frame` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/round_record.py#close` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | round 2's 🟢 — confirmed |
| round-3 | `skills/code-review/scripts/round_record.py:2259` | round 3's 🟡 1 — deferred |
| round-3 | `skills/code-review/scripts/round_record.py#range_carriers` | round 3's 🟢 — confirmed |
| round-3 | `skills/code-review/scripts/round_record.py#names_a_file` | round 3's 🟢 — confirmed |
| round-3 | `docs/round-record-spec.md:698` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/rounds/round-2.md` | round 3's 🟢 — confirmed |
| round-4 | `skills/code-review/scripts/round_record.py:2437` | round 4's 🟡 1 — fixed |
| round-4 | `skills/code-review/scripts/round_record.py:2938` | round 4's 🟡 2 — fixed |
| round-4 | `tests/test_a_fix_of_a_fix_is_counted.py:536` | round 4's 🟡 3 — fixed |
| round-4 | `tests/test_a_fix_of_a_fix_is_counted.py#test_a_location_that_lands_in_no_written_unit_reads_no` | round 4's 🟢 — confirmed |
| round-4 | `docs/round-record-spec.md` | round 4's 🟢 — confirmed |
| round-4 | `skills/code-review/scripts/round_record.py#location_units` | round 4's 🟢 — confirmed |
| round-4 | `skills/code-review/scripts/round_record.py#build` | round 4's 🟢 — confirmed |
| round-4 | `skills/code-review/scripts/round_record.py#touched` | round 4's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
