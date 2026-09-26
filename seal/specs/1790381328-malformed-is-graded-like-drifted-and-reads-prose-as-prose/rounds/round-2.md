# 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose — review round 2

| Field | Value |
|---|---|
| Target SHA | eb30a068ec6620d37462bead87ae699ee56f2b10 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 621 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `e9e23deb12106f977374b00adf76874da93c4248..9bd0cbed9e9a711762f6d83e482b6a4c52559ba4`, 3 commits |
| Contract changes | none |
| New units | examples (depth 1) |
| Needs a fix | yes — 🟡 1 (the list of what rule (a) gives up still omits a digit-opening locator whose hash follows after whitespace, in the docstring, `GIVEN_UP` and the release note) and 🟡 2 (the flag row's and the template's pins stay green when the grading changes) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790381328 is the verifying round. It opens round 1's fixes, `d05cc2c3..6c260d34`, at eb30a068. The classes are the completeness of GIVEN_UP and TAKEN_UP against the code, probed on both sides of rule (a)'s boundary at the base, the build and the fix. Also whether `GLUED_MARKS_RE`'s new class changes any verdict, and whether each of the six new units goes red when its claim goes false.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the list of what rule (a) gives up says a digit-opening locator is silent "when no hash follows" and that a path keeps a spaced hash named; with a path and a hash after whitespace (`docs/a.md#1-scope @abcdef12`, `src/a.py#12 @abcdef12`, in a span) the base names it and the target is silent | `skills/evidence-check/scripts/evidence_check.py:1638` | **fixed** `1c33e360db0669e3d57611844f3af0ba1b01a0f5` | fixed at 1c33e360db0669e3d57611844f3af0ba1b01a0f5; Executed: 2 425 shapes at `47e32d57` and `eb30a068`; 96 cells of this class named then silent, all other 493 given-up cells fit a stated class; the paste-ready `GIVEN_UP` entry is red against the current docstring and green with the new one. Same wording at `changelog.md:35` and `spec.md:175` |
| 🟡 2 | two of the four grading pins do not follow `exit_code`: the flag row is checked for `exit {strict}` only and the template comment against a fixed string, so a grading change leaves both stale and green, although the case's docstring says it goes red | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:456` | **fixed** `1c33e360db0669e3d57611844f3af0ba1b01a0f5` | fixed at 1c33e360db0669e3d57611844f3af0ba1b01a0f5; Executed: mutant M12 (grading back to (a), step 4 and the module docstring moved) leaves the case green; with the two paste-ready assertions it is red, and green at the target |
| ⬜ 3 | "the search stays linear" holds for `#` outside quotes only; `#"\"` repeated still costs quadratic time (1.48 s at 20 000 characters, 5.94 s at 40 000) | `skills/evidence-check/scripts/evidence_check.py:1624` | **fixed** `1c33e360db0669e3d57611844f3af0ba1b01a0f5` | fixed at 1c33e360db0669e3d57611844f3af0ba1b01a0f5; Executed: timing before and after the fix; no verdict differs across 4 850 cells. Same claim in the S8–S12 ledger row, `spec.md:137-138` and the changelog, each a correction to this run's own records |
| ⬜ 4 | `docs/a.md#²` and `docs/a.md#①` are silent at the base (`str.isdigit`) and named at the target (`\d`); `TAKEN_UP` and the docstring do not say so | `skills/evidence-check/scripts/evidence_check.py:1617` | **fixed** `1c33e360db0669e3d57611844f3af0ba1b01a0f5` | fixed at 1c33e360db0669e3d57611844f3af0ba1b01a0f5; Executed beside a good anchor, in a span and as a word; no such shape occurs in a `Code grounds` cell |
| 🟢 | round 1's finding 1 is closed for its own shapes — `docs/a.md#1-scope`, `docs/a.md#1.2`, `src/a.py#1>"x"`, `#handler>"a"b"@abcdef12` are silent, listed and pinned | `skills/evidence-check/scripts/evidence_check.py:1635` | confirmed | Executed: mutants M1, M3, M7 each turn the matching `GIVEN_UP` parameters red; the rest of the class is this round's finding 1 |
| 🟢 | round 1's finding 2 is closed against removal — each of the four sentences restored to its base wording turns the new case red, and `overview.md`'s row is corrected | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:448` | confirmed | Executed: mutants M8–M11, each red; the part that does not follow the grading is this round's finding 2 |
| 🟢 | round 1's finding 3 is closed — the code-span condition is stated in the comment, `malformed_rows`' docstring, the opener-list case and the S8–S12 claim | `skills/evidence-check/scripts/evidence_check.py:1622` | confirmed | Read at `eb30a068`; executed: the unticked shape is silent and the ticked one named |
| 🟢 | round 1's finding 4 is closed for `C#"hello"` and `vector#<T>` — listed and pinned | `tests/test_a_row_points_by_content.py:1209` | confirmed | Executed: mutants M2 and M6 red; the leftover is this round's finding 4 |
| 🟢 | round 1's finding 5 is closed for its input — `#a` repeated reads in 0.0009 s where it took 4.19 s, and no verdict moved | `skills/evidence-check/scripts/evidence_check.py:1626` | confirmed | Executed: 4 850 cells identical at `591c6cdf` and `eb30a068`; M5 turns the stop-at-`#` case red; the remaining quadratic input is this round's finding 3 |

## Paste-ready fixes

```python
    What each edge gives up (#614): `src/a.py@abc`, a path followed by fewer
    than six hex characters, is silent. A locator that opens with a run of
    digits no ASCII letter, digit or `_` continues reads as an issue number
    unless its hash is glued to it: `docs/a.md#1장`, `docs/a.md#1-scope`,
    `docs/a.md#1.2`, `src/a.py#1>"x"`, and in a code span
    `docs/a.md#1-scope @abcdef12`, whitespace before its hash. A dotless
    file name takes a locator opening with a letter, `_`, `"` or `<` and
    never a digit, so
```
```python
    '#handler>"a"b"@abcdef12',
    "docs/a.md#1-scope @abcdef12",
]
```
```markdown
  `C#"hello"` and `vector#<T>`. What this gives up: `src/a.py@abc` with a
  hash shorter than six characters; a locator opening with digits that no
  ASCII letter, digit or underscore continues, unless its hash is glued to
  it (`docs/a.md#1장`, `docs/a.md#1-scope`, `docs/a.md#1.2`,
  `src/a.py#1>"x"`, and `docs/a.md#1-scope @abcdef12` with a space before
  the hash); `Makefile#1x`; and a path-less `#handler @abcdef12` or
  `#handler>"a"b"@abcdef12` are not named. A run of `#` characters outside
  quotes no longer takes seconds to read.
```
```python
    flag = table_row(skill, "`--strict`")[1]
    assert "malformed" in flag and f"exit {strict}" in flag, flag
    assert f"instead of {lenient}" in flag, "the flag row's lenient exit"
```
```python
    template = read(os.path.join(ROOT, "templates", "evidence-check.yml"))
    assert lenient < strict, "the template says dropping --strict softens it"
    assert "softens drift\n          # and MALFORMED, and nothing else" in template
```
```python
# `#` is out of the unquoted class so each attempt stops at the next `#`
# outside a quote: the attempt that starts there finds the same match, and a
# run of them is read in linear time. A `#` inside a quote does not stop
# one, so a chain of quoted strings holding escaped quotes (`#"\"` repeated)
# is still quadratic: 1.5 s at 20 000 characters, far past any real row.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the four reader modules (`test_a_row_points_by_content.py`, `test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `test_evidence_check.py`, `test_dispatch.py`) at `eb30a068` | 227 passed |
| `malformed_rows` over 2 425 shapes × {code span, bare word}, beside a good anchor, with the checker at `47e32d57`, `591c6cdf` and `eb30a068` | `591c6cdf` = `eb30a068` on all 4 850 cells; 589 cells named at the base and silent at the target, 138 the other way; unexplained by the lists: 🟡 1's 96 cells and ⬜ 4's two shapes |
| twelve mutants of the six new units and the four documents, one at a time, against the fix's 12 new cases | M1–M11 each red on the case that owns the claim; M12 (grading back to (a), step 4 and docstring moved) green: 🟡 2 |
| 🟡 1's and 🟡 2's paste-ready fixes applied in the clone | new `GIVEN_UP` entry red against the old docstring; all 13 cases green with the fix; M12 red with the fix |
| timing of `refused_coordinate`, `GLUED_MARKS_RE`, `URL_RE` and `malformed_rows` on 20 000 and 40 000 characters | as in ⬜ 3 and *Other super-linear paths* |
| `gh pr checks 621` at `eb30a068` | lint, ledger, release, ubuntu, macos pass; windows-latest pending |
| the broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it on this branch. It is the sealer's, and it is not due while 🟡 1 and 🟡 2 are open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1630` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-ci/SKILL.md:65` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1618` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1647` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1621` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2750` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1624` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_row_points_by_content.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_evidence_check.py` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/SKILL.md:173`, `skills/evidence-ci/SKILL.md:65`, `templates/evidence-check.yml:39`, `.github/workflows/test.yml:74` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.15.4.md:54`, `seal/releases/0.11.3.md:23` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/survivors.md` | round 1's 🟢 — confirmed |
| round-1 | PR #621, `pytest (windows-latest, 3.12)` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
