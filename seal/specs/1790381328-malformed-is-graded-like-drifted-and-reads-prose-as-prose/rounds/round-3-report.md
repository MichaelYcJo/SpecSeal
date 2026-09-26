# Round 3 report — 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose

| Field | Value |
|---|---|
| Target SHA | `c802aca0` |
| Fix range verified | `e9e23deb..9bd0cbed` (1c33e360 code and cases, 543ba180 records, 9bd0cbed survivors); `c802aca0` only closes round 2's record |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 621 (draft, base `release/v0.15.5`, head `c802aca0`) |

This is the last round. The run's one reopening was spent at round 2, so
anything this round leaves open is deferred to a new issue. It is not fixed
on this branch.

This is a verifying round, so its target is the fix diff. I ran the probes
in a `git clone --no-local` of the worktree at `c802aca0`, under this
round's scratch directory. I removed the clone and every probe before
handover. I wrote nothing in the worktree except this file.

I read rounds 1 and 2 (records and reports) for coordinates, and I
re-derived every verdict below. The smith's sweep is a claim. I did not
reuse its generator or its counts.

## Summary

Round 2's four findings are closed. Two new ⬜ findings came up this round.
Neither blocks the merge, and both can be deferred.

- **The five rules explain every moved verdict except one family (⬜ 1).**
  I built a separate sweep over 143 908 shapes (287 816 cells). 16 439 cells
  moved between `47e32d57` and `9bd0cbed`. Every silent-to-named cell and
  1 870 named-to-silent cells fit a rule as the docstring words it. The
  other 9 467 cells have their `@` before their `#`: `@alice#299`,
  `@types/node#1`, `@abc#`. The glued-marks change alone moved them. The
  docstring's rule 3 bullet, the changelog bullet and the trade list in
  `spec.md` define *glued* only by whitespace and an unclosed quote. By
  those words `@alice#299` is glued and should count, but it is silent. The
  ledger row S8–S12, the docstring's opening sentence and `spec.md` item 13
  do say "an `@` glued after a `#`". So the rule sets match, but the wording
  of rule 3 differs between the copies. Every cell this family moves is
  prose or a hash-first coordinate, so no real coordinate is lost.
- **Round 2's fix dropped three pins that round 1 planted (⬜ 2).**
  `docs/a.md#1.2`, `src/a.py#1>"x"` and `Makefile#1x` are still in the
  docstring, but `GIVEN_UP` no longer holds them. I made three mutants that
  make each of those sentences false. All 227 cases of the four reader
  modules stayed green under each mutant. The code is right today, but
  nothing pins those three statements any more.

Everything else the prompt asked to check held:

- Each docstring rule dropped alone turns its own examples red.
- M12 is now red, and each of the two new assertions goes red alone.
- The four copies state the same five rules.
- The four reader modules pass (227).
- `evidence-check --strict .` exits 0.

## ⬜ 1 — reversed-order marks move a verdict, and rule 3's bullet does not say so

`skills/evidence-check/scripts/evidence_check.py:1649`, the third bullet of
`refused_coordinate`'s docstring. The same wording is in this work item's
`changelog.md:34` and `spec.md:187`.

**What is wrong (executed).** I used my own generator, not the smith's. It
takes every concatenation of one to four tokens from a 23-token alphabet
(`#`, `@`, `src/a.py`, `Mk`, `abcdef12`, `abc`, `1`, `²`, `①`, `١`, `x`,
`_`, `"`, `<`, `>`, a space, `-`, `.`, `장`, `'s`, a backslash, `)`, `:`).
It adds 150 000 random strings of five to eight tokens and keeps each
shape that holds a `#` or an `@`. That leaves 143 908 shapes. I read each
one through `malformed_rows` beside a good anchor, in a code span and as
bare words, with the checker at `47e32d57` and at `9bd0cbed`.

To attribute each moved cell, I wrote a copy of `refused_coordinate` with
one flag per code change: hash length, issue tail, glued marks, and dotless
openers. With all flags off the copy matches `47e32d57` on all 287 816
cells, and with all flags on it matches `9bd0cbed`. Each moved cell was
attributed by turning off one flag at a time. Then I checked each cell
against the literal wording of the rule it was attributed to.

| Moved | Cells | Falls under |
|---|---|---|
| silent → named | 5 102 | rule 4 (dotless opener) 4 442, rule 5 (non-decimal digit) 660; none left over |
| named → silent | 1 870 | rules 1–3 as worded (short hash, digit-first locator, marks with whitespace or an unclosed quote between them) |
| named → silent | 9 467 | the glued-marks change alone, every `@` before every `#`; no bullet's wording covers them |

The smallest of the 9 467 are `@#`, `@x#`, `@#1` and `@#²`. The realistic
ones I checked one by one:

| Shape | `47e32d57` | `9bd0cbed` (span and word alike) |
|---|---|---|
| `@alice#299`, `@alice#299's`, `@v2#1`, `@types/node#1` | named | silent |
| `@abcdef12#1`, `Makefile@abcdef12#1` | named | silent |
| `@Override#toString` | named | named (the dotless branch) |

**Why it is ⬜ and not 🟡.** Nothing wrong ships. Every cell in this family
is prose, or a coordinate written hash-first with a digit locator and no
path. That shape was never valid, and the dotless and path branches still
name most of its neighbours. What is missing is one condition in the
wording of rule 3. The bullet says "Both marks count only where they are
glued" and defines *glued* by whitespace and quotes. The docstring's first
sentence, the ledger's S8–S12 claim ("an `@` is glued after a `#`") and
`spec.md` item 13 ("an `@` follows a `#`") state the order. The bullet, the
changelog and the `spec.md` trade list do not. This is round 1's and round
2's class: the stated list is narrower than the code. This time it is only
in the prose direction. The smith's space could not reach this family,
because each of its shapes puts the hash ending after the locator.

**The fix** is in *Paste-ready fixes*. I checked it in the clone. The new
`GIVEN_UP` entry `@alice#299` is red against the current docstring
(`1 failed, 9 passed`), and with the new bullet all 10 cases pass. The same
condition has to go into `changelog.md` and the `spec.md` trade list.

## ⬜ 2 — three docstring examples lost their pins in round 2's rebuild

`tests/test_a_row_points_by_content.py:1205`, `GIVEN_UP`.

**What is wrong (executed).** Round 1's fix planted `docs/a.md#1.2`,
`src/a.py#1>"x"` and `Makefile#1x` as `GIVEN_UP` parameters. Round 2
confirmed them red under its mutants M1, M3 and M7. Round 2's fix rebuilt
`GIVEN_UP` as one or two examples per rule and left those three out. The
docstring still names all three. I made three mutants, one at a time, and
ran all four reader modules under each:

| Mutant | What it makes false | Four modules |
|---|---|---|
| the dotless branch takes `isalnum` in place of `isalpha` | "never a digit … `Makefile#1x` is not" (rule 4, and the changelog's "still not named") | 227 passed |
| `ISSUE_TAIL_RE`'s lookahead also refuses `.` | `docs/a.md#1.2` is silent (rule 2) | 227 passed |
| `ISSUE_TAIL_RE`'s lookahead also refuses `>` | `src/a.py#1>"x"` is silent (rule 2) | 227 passed |

I also probed the `_` opener. It is still pinned, by
`test_a_file_name_with_no_dot_takes_any_locator[Makefile#_private]`.

**Why it is ⬜ and not 🟡.** The behaviour and the sentences are true at
`c802aca0`. A missing pin ships no defect. It leaves three statements a
person reads with nothing to stop a later edit from making them false. That
is what §14 is for. The case's comment does not overclaim ("one or two
examples of each rule"). So this is not round 2's 🟡 2, whose case said it
went red when it did not.

**The fix** is in *Paste-ready fixes*: put the three examples back under
their rules. I checked it in the clone. Each of the three mutants turns its
own new parameter red (`1 failed, 9 passed` each), and all 10 cases pass
with the checker unchanged.

## Round 2's findings

- **🟡 1 is closed.** The docstring no longer says "when no hash follows".
  Rule 2 says "whatever follows the digits … named only where its `@` is
  glued to its `#`". Rule 3 lists `docs/a.md#1-scope @abcdef12` as silent.
  `GIVEN_UP` holds that shape. My canonical grid covers 5 path heads, 7
  digit runs (ASCII and Arabic-Indic) and 12 continuations. On it every
  shape is named at the base and silent at the fix, both glued forms stay
  named, and the spaced form in a span goes silent. The only exceptions
  were continuations of `²`, which `str.isdigit` already read as an issue
  number at the base, so nothing moved there.
- **🟡 2 is closed.** M12 puts the grading back to (a) and moves step 4 and
  the module docstring with it. The case is now red on "the flag row's
  lenient exit" (`assert 'instead of 2' in …`). With the flag row moved too
  (M12b), it is red on `assert 2 < 2`, the template's direction. So each of
  the two new assertions goes red alone.
- **⬜ 3 is closed.** The comment above `GLUED_MARKS_RE` now says a `#` inside
  a quote does not stop an attempt, and that `#"\"` repeated is still
  quadratic. The ledger S8–S12 claim and the `spec.md` item 13 say the same.
  I measured 1.45 s at 20 000 characters and 5.82 s at 40 000, in line with
  the comment's 1.5 s.
- **⬜ 4 is closed.** Rule 5 is in every copy. `docs/a.md#²` and `docs/a.md#①`
  are `TAKEN_UP` examples. Dropping rule 5 from the docstring turns both
  red.

## The five rules against their examples, and the copies against each other

I dropped each docstring bullet alone and ran the two example cases.

| Bullet dropped | Result |
|---|---|
| rule 1 | `src/a.py@abc` red (1 failed) |
| rule 2 | `docs/a.md#1-scope`, `docs/a.md#1장` red (2 failed) |
| rule 3 | `#handler @abcdef12`, `docs/a.md#1-scope @abcdef12`, `#handler>"a"b"@abcdef12` red (3 failed) |
| rule 4 | `C#"hello"`, `vector#<T>` red (2 failed) |
| rule 5 | `docs/a.md#²`, `docs/a.md#①` red (2 failed) |

The docstring, `changelog.md`, the `spec.md` trade list and the ledger's
S8–S12 each state the same five rules in the same order. Every copy uses
the same counts (2 426 shapes, 484 of 4 852 cells, 286 and 198, and the
per-rule split 8 + 135 + 43 + 100 + 168 + 30). The one difference in content
is ⬜ 1's order condition. The changelog's rule 5 leaves out "after a path",
but its only example has a path, so that is not a separate finding.

`examples()` is the one new unit. As code it is correct. It builds one
`pytest.param` per shape, in dict order, with no duplicate ids, and CI's
`windows-latest` leg ran it green at `c802aca0`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | rule 3's bullet defines *glued* by whitespace and an unclosed quote only; 9 467 cells with every `@` before every `#` (`@alice#299`, `@types/node#1`, `Makefile@abcdef12#1`) moved from named to silent under the glued-marks change alone, and no bullet's wording covers them; the ledger S8–S12 and the docstring's first sentence state the order, the bullet, `changelog.md:34` and `spec.md:187` do not | `skills/evidence-check/scripts/evidence_check.py:1649` | open | Executed: an independent sweep, 143 908 shapes × {span, word} at `47e32d57` and `9bd0cbed`, attributed by single-flag reverts on a copy equal to both checkers on every cell. Deferrable, and it does not block: every cell in the family is prose or a hash-first shape that was never valid |
| ⬜ 2 | round 2's rebuild of `GIVEN_UP` dropped `docs/a.md#1.2`, `src/a.py#1>"x"` and `Makefile#1x`, which the docstring still names; a mutant making each false leaves all 227 cases green | `tests/test_a_row_points_by_content.py:1205` | open | Executed: three mutants, one at a time, over the four reader modules, 227 passed each; the paste-ready parameters turn each red. Deferrable, and it does not block: behaviour and text are true at `c802aca0` |
| 🟢 | round 2's finding 1 is closed — a path, a digit-first locator and a spaced hash are stated as silent, and every copy says "whatever follows the digits" | `skills/evidence-check/scripts/evidence_check.py:1643` | confirmed | Executed: canonical grid of 5 paths × 7 digit runs × 12 continuations, both contexts; rule 2 dropped from the docstring turns its two examples red |
| 🟢 | round 2's finding 2 is closed — M12 is red, and each new assertion goes red alone | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:457` | confirmed | Executed: M12 red on `instead of 2`; M12b (flag row moved as well) red on `2 < 2` |
| 🟢 | round 2's finding 3 is closed — the quadratic input is stated in the comment, the ledger and `spec.md` | `skills/evidence-check/scripts/evidence_check.py:1623` | confirmed | Executed: 1.45 s at 20 000 characters, 5.82 s at 40 000 |
| 🟢 | round 2's finding 4 is closed — rule 5 is stated in every copy and pinned | `tests/test_a_row_points_by_content.py:1217` | confirmed | Executed: rule 5 dropped turns `docs/a.md#²` and `docs/a.md#①` red |
| 🟢 | every silent-to-named cell, and every named-to-silent cell outside ⬜ 1's family, falls under a stated rule, and each rule holds over its canonical grid | `skills/evidence-check/scripts/evidence_check.py:1639` | confirmed | Executed: 5 102 + 1 870 cells fit a rule's wording; converse grid for rules 1, 2, 4, 5 and rule 3's spaced, unclosed and quoted forms, no cell against a rule |
| 🟢 | the four copies state the same five rules with the same counts | `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md:6` | confirmed | Read: docstring, `changelog.md`, `spec.md` trade list, ledger S8–S12; the one wording difference is ⬜ 1 |
| 🟢 | round 1's findings stay closed at `c802aca0`, except that two of finding 1's pins are gone (⬜ 2) | `skills/evidence-check/scripts/evidence_check.py:1639` | confirmed | Executed: the four reader modules, 227 passed; the code did not change in round 2's fix pass (`git diff e9e23deb..9bd0cbed` touches the docstring and comment only) |
| 🟢 | round 1's open question on the `windows-latest` leg is answered | PR #621, `pytest (windows-latest, 3.12)` | confirmed | Executed: `gh pr checks 621` at `c802aca0`, all six checks pass, windows-latest in 11m15s |

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

## Paste-ready fixes

### ⬜ 1 — `refused_coordinate`'s docstring, the third bullet

```python
    - Both marks count only where an `@` is glued after a `#`: no `@`
      before its `#`, no whitespace between them outside a quoted string,
      which holds whitespace only in a code span, and no `"` left unclosed.
      Where they are not glued each word is judged alone, so
      `src/a.py#handler @abcdef12` is still named, and `@alice#299`,
      `@lru_cache  # memoized`, `#handler @abcdef12`,
      `docs/a.md#1-scope @abcdef12` and `#handler>"a"b"@abcdef12` are not.
```

### ⬜ 1 — `changelog.md` of this work item, the third bullet

```markdown
  - `#` and `@` count as one coordinate only where the `@` is glued after
    the `#`: no space between them outside quotes, a quoted part keeping its
    spaces only inside a code span, and no quote left unclosed. Otherwise
    each word is judged alone. `` `@lru_cache  # memoized` `` is prose now,
    and so are `@alice#299`, `#handler @abcdef12`,
    `docs/a.md#1-scope @abcdef12` and `#handler>"a"b"@abcdef12`;
    `src/a.py#handler @abcdef12` is still named.
```

### ⬜ 1 and ⬜ 2 — `GIVEN_UP` in `tests/test_a_row_points_by_content.py`

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — rule 3's order condition missing from the docstring bullet, `changelog.md` and the `spec.md` trade list | a new issue, since the run is capped | the orchestrator files it; the smith of the next work item that touches `refused_coordinate` fixes it |
| ⬜ 2 — the pins for `docs/a.md#1.2`, `src/a.py#1>"x"` and `Makefile#1x` | the same new issue | the same |

Needs a fix: no

Loses a record or crashes: no

## Proof block

I opened and read these in full, or at the cited lines:

- `rounds/round-1.md` (coordinates only, through round 2's inherited table)
  and `rounds/round-2.md` in full.
- `rounds/round-2-report.md`, in full apart from a middle section the
  output cut off. Its findings, verdict table, probes and paste-ready fixes
  I read in full.
- The fix diff `e9e23deb..9bd0cbed` for `skills/`, `tests/`,
  `seal/ledger/` and `seal/releases/0.15.4.md`, and `9bd0cbed..c802aca0`'s
  stat.
- The work item's `changelog.md`, `survivors.md` and `spec.md` lines
  105–215, and `overview.md`'s diff.
- `skills/evidence-check/scripts/evidence_check.py` lines 1590–1800 and
  2775–2798 at `9bd0cbed`, lines 1590–1650 at `47e32d57`, and the whole
  file's diff `47e32d57..9bd0cbed`, code lines only.
- `tests/test_a_row_points_by_content.py` lines 1196–1300.
- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` lines
  381–387 and 420–467.
- `skills/evidence-check/SKILL.md` lines 173 and 264–266,
  `skills/evidence-ci/SKILL.md` line 66, `templates/evidence-check.yml`
  lines 46–51, `bin/test`, and `.github/scripts/run_tests.py`'s venv lines.

I ran the commands in *Executed probes* in the clone. It and every probe
are gone.
