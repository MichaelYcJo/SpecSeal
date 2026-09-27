# 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose — review round 3

| Field | Value |
|---|---|
| Target SHA | c802aca039ae1dea6ac06d36c5a73dbe46e18288 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 621 |
| Broad gate | 5c848e8f against c1ef81fb |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790381328 is the last round: the reopening was spent at round 2. It opens round 2's fixes, `e9e23deb..9bd0cbed`, at c802aca0. The class is the trade list the fix pass built by construction. An independent sweep, not the smith's generator, checks that every flipped cell falls under a stated rule and that each rule holds over every cell it claims. It also checks that each rule's examples go red when the rule is dropped, and that M12 now fails.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | rule 3's bullet defines *glued* by whitespace and an unclosed quote only; 9 467 cells with every `@` before every `#` (`@alice#299`, `@types/node#1`, `Makefile@abcdef12#1`) moved from named to silent under the glued-marks change alone, and no bullet's wording covers them; the ledger S8–S12 and the docstring's first sentence state the order, the bullet, `changelog.md:34` and `spec.md:187` do not | `skills/evidence-check/scripts/evidence_check.py:1649` | deferred #626 | Executed: an independent sweep, 143 908 shapes × {span, word} at `47e32d57` and `9bd0cbed`, attributed by single-flag reverts on a copy equal to both checkers on every cell. Deferrable, and it does not block: every cell in the family is prose or a hash-first shape that was never valid |
| ⬜ 2 | round 2's rebuild of `GIVEN_UP` dropped `docs/a.md#1.2`, `src/a.py#1>"x"` and `Makefile#1x`, which the docstring still names; a mutant making each false leaves all 227 cases green | `tests/test_a_row_points_by_content.py:1205` | deferred #626 | Executed: three mutants, one at a time, over the four reader modules, 227 passed each; the paste-ready parameters turn each red. Deferrable, and it does not block: behaviour and text are true at `c802aca0` |
| 🟢 | round 2's finding 1 is closed — a path, a digit-first locator and a spaced hash are stated as silent, and every copy says "whatever follows the digits" | `skills/evidence-check/scripts/evidence_check.py:1643` | confirmed | Executed: canonical grid of 5 paths × 7 digit runs × 12 continuations, both contexts; rule 2 dropped from the docstring turns its two examples red |
| 🟢 | round 2's finding 2 is closed — M12 is red, and each new assertion goes red alone | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:457` | confirmed | Executed: M12 red on `instead of 2`; M12b (flag row moved as well) red on `2 < 2` |
| 🟢 | round 2's finding 3 is closed — the quadratic input is stated in the comment, the ledger and `spec.md` | `skills/evidence-check/scripts/evidence_check.py:1623` | confirmed | Executed: 1.45 s at 20 000 characters, 5.82 s at 40 000 |
| 🟢 | round 2's finding 4 is closed — rule 5 is stated in every copy and pinned | `tests/test_a_row_points_by_content.py:1217` | confirmed | Executed: rule 5 dropped turns `docs/a.md#²` and `docs/a.md#①` red |
| 🟢 | every silent-to-named cell, and every named-to-silent cell outside ⬜ 1's family, falls under a stated rule, and each rule holds over its canonical grid | `skills/evidence-check/scripts/evidence_check.py:1639` | confirmed | Executed: 5 102 + 1 870 cells fit a rule's wording; converse grid for rules 1, 2, 4, 5 and rule 3's spaced, unclosed and quoted forms, no cell against a rule |
| 🟢 | the four copies state the same five rules with the same counts | `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md:6` | confirmed | Read: docstring, `changelog.md`, `spec.md` trade list, ledger S8–S12; the one wording difference is ⬜ 1 |
| 🟢 | round 1's findings stay closed at `c802aca0`, except that two of finding 1's pins are gone (⬜ 2) | `skills/evidence-check/scripts/evidence_check.py:1639` | confirmed | Executed: the four reader modules, 227 passed; the code did not change in round 2's fix pass (`git diff e9e23deb..9bd0cbed` touches the docstring and comment only) |
| 🟢 | round 1's open question on the `windows-latest` leg is answered | PR #621, `pytest (windows-latest, 3.12)` | confirmed | Executed: `gh pr checks 621` at `c802aca0`, all six checks pass, windows-latest in 11m15s |

## Paste-ready fixes

```python
    - Both marks count only where an `@` is glued after a `#`: no `@`
      before its `#`, no whitespace between them outside a quoted string,
      which holds whitespace only in a code span, and no `"` left unclosed.
      Where they are not glued each word is judged alone, so
      `src/a.py#handler @abcdef12` is still named, and `@alice#299`,
      `@lru_cache  # memoized`, `#handler @abcdef12`,
      `docs/a.md#1-scope @abcdef12` and `#handler>"a"b"@abcdef12` are not.
```
```markdown
  - `#` and `@` count as one coordinate only where the `@` is glued after
    the `#`: no space between them outside quotes, a quoted part keeping its
    spaces only inside a code span, and no quote left unclosed. Otherwise
    each word is judged alone. `` `@lru_cache  # memoized` `` is prose now,
    and so are `@alice#299`, `#handler @abcdef12`,
    `docs/a.md#1-scope @abcdef12` and `#handler>"a"b"@abcdef12`;
    `src/a.py#handler @abcdef12` is still named.
```
```python
GIVEN_UP = {
    "a short hash after a path": ["src/a.py@abc"],
    "a digit-first locator is an issue number": [
        "docs/a.md#1-scope",
        "docs/a.md#1장",
        "docs/a.md#1.2",
        'src/a.py#1>"x"',
    ],
    "marks that are not glued are judged word by word": [
        "#handler @abcdef12",
        "docs/a.md#1-scope @abcdef12",
        '#handler>"a"b"@abcdef12',
        "@alice#299",
    ],
    "a dotless name never takes a digit, before or after #614": ["Makefile#1x"],
}
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_row_points_by_content.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_evidence_check.py`, `tests/test_dispatch.py` at `c802aca0`, in the clone | 227 passed |
| `bin/evidence-check --strict .` at `c802aca0`, in the clone | exit 0; `total: 2419 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed` |
| an independent sweep of `malformed_rows`: 143 908 shapes (every 1–4 token string over 23 tokens, plus 150 000 random 5–8 token strings) × {code span, bare words}, beside a good anchor, checker at `47e32d57` and `9bd0cbed` | 16 439 of 287 816 cells moved: 5 102 silent → named, all rules 4 and 5; 11 337 named → silent, 1 870 under rules 1–3, 9 467 reversed-order (⬜ 1); a flag copy of the rule equals both checkers on every cell |
| a canonical converse grid per rule (hash lengths 1–40, digit-first locators, spaced, glued and unclosed marks, dotless heads, non-decimal and Unicode-decimal digits) | no cell against a rule's wording; the only surprises were `²` continuations, already issue numbers at the base, and `#"a"b @abcdef12`, whose first word is named by the path-less quote opener |
| each of the five docstring bullets dropped alone, against the two example cases | each red on exactly its own examples (1, 2, 3, 2, 2 failed) |
| M12 (grading back to (a), step 4 and the module docstring moved) and M12b (the flag row moved too), against `test_every_other_page_that_grades_the_flag_names_malformed` | M12 red on `instead of 2`; M12b red on `assert 2 < 2` |
| three mutants of the statements round 2 unpinned (dotless takes a digit; `ISSUE_TAIL_RE` refuses `.`; refuses `>`), over the four reader modules | 227 passed each (⬜ 2) |
| the `_` opener removed, over `tests/test_a_row_points_by_content.py` and `tests/test_evidence_check.py` | red: `test_a_file_name_with_no_dot_takes_any_locator[Makefile#_private]` |
| ⬜ 1's and ⬜ 2's paste-ready fixes applied in the clone | the new `@alice#299` entry red against the current docstring, green with the fix; each restored pin red under its mutant; 10 passed with all applied |
| `GLUED_MARKS_RE.search` on `#"\"` repeated | 1.45 s at 20 000 characters, 5.82 s at 40 000 |
| `gh pr checks 621` at `c802aca0` | ledger, lint, release, pytest on macos, ubuntu and windows: all pass |
| the broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it on this branch. It is the sealer's, and it is due now, since this round opens nothing that needs a fix |

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
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1638` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:456` | round 2's 🟡 2 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1617` | round 2's ⬜ 4 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1635` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:448` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1622` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_row_points_by_content.py:1209` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1626` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — rule 3's order condition missing from the docstring bullet, `changelog.md` and the `spec.md` trade list | a new issue, since the run is capped | the orchestrator files it; the smith of the next work item that touches `refused_coordinate` fixes it |
| ⬜ 2 — the pins for `docs/a.md#1.2`, `src/a.py#1>"x"` and `Makefile#1x` | the same new issue | the same |
