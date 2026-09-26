# 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose — review round 1

| Field | Value |
|---|---|
| Target SHA | 591c6cdf163bc93fc5a0f925c26b14ccfe6cd7b6 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 621 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `d05cc2c3771aeb646432d502cb8a37b5766ac387..6c260d34b2177d92f400717b8194ddfab4cc3118`, 2 commits |
| Contract changes | none |
| New units | GIVEN_UP (depth 1); TAKEN_UP (depth 1); test_what_rule_a_gives_up_is_silent_and_says_so (depth 1); test_what_the_dotless_openers_take_up_is_named_and_says_so (depth 1); test_a_glued_mark_attempt_stops_at_the_next_hash (depth 1); test_every_other_page_that_grades_the_flag_names_malformed (depth 1) |
| Needs a fix | yes — 🟡 1 (the list of what rule (a) gives up omits two shapes the branch silenced, in the docstring and the release note) and 🟡 2 (four statements of the new grading are unpinned, and `overview.md` claims a pin for step 4 that does not exist) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item 1790381328 reviews the build at 591c6cdf against spec.md and plan.md (frame 6fc5532c, approved 0a22ea9c). It covers the owner's answer to #606's Q1, (b): `MALFORMED` graded like `DRIFTED`. It also covers #614's rule (a) edges and the decorated-line observation, and the ledger rows corrected and re-read. The classes are every place that states MALFORMED's grading, found by meaning in English and Korean, and every cell shape on both sides of rule (a)'s boundary, run at the base and at the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | rule (a)'s list of what each edge gives up leaves out two shapes the branch silenced: a digit-opening locator continued by ASCII punctuation with no hash (`docs/a.md#1-scope`, `docs/a.md#1.2`, `src/a.py#1>"x"`), and a path-less coordinate holding an unclosed `"` between its marks (`#handler>"a"b"@abcdef12`) | `skills/evidence-check/scripts/evidence_check.py:1630` | **fixed** `a0624b6323ad20a85206c94f16a48343f8900720` | fixed at a0624b6323ad20a85206c94f16a48343f8900720; Executed: `malformed_rows` over 66 shapes at 47e32d57 and 591c6cdf; both classes are named at the base and silent at the target, and the docstring, `changelog.md:32-34`, `spec.md` and the ledger note list neither |
| 🟡 2 | the grading stated in `evidence-ci`'s step 4, `SKILL.md`'s `--strict` row, the template's comment and the module docstring is pinned by nothing; `overview.md` claims step 4 is pinned | `skills/evidence-ci/SKILL.md:65` | **fixed** `a0624b6323ad20a85206c94f16a48343f8900720` | fixed at a0624b6323ad20a85206c94f16a48343f8900720; Executed: with the base's three documents over the new code, only the S6 and S7 pins fail and nothing fails for step 4; a planted case goes red for each document restored alone. Read: no test holds the flag row, the template comment or the docstring line |
| ⬜ 3 | "glued through a quoted string" holds only inside a code span; an unticked `#handler>"a b"@abcdef12` is silent, and the comment and the S8–S12 ledger claim omit the condition | `skills/evidence-check/scripts/evidence_check.py:1618` | **fixed** `a0624b6323ad20a85206c94f16a48343f8900720` | fixed at a0624b6323ad20a85206c94f16a48343f8900720; Executed: named in a span, silent out of one, at both SHAs. Not a regression; the ledger half is a correction to this run's own fragment |
| ⬜ 4 | the dotless-name openers `"` and `<` now name `C#"hello"` and `vector#<T>`; the list of what each edge gives up does not say so | `skills/evidence-check/scripts/evidence_check.py:1647` | **fixed** `a0624b6323ad20a85206c94f16a48343f8900720` | fixed at a0624b6323ad20a85206c94f16a48343f8900720; Executed for the two shapes; read for `PR#<n>`. Rare in a Code grounds cell, and a lenient run only warns |
| ⬜ 5 | `GLUED_MARKS_RE` is quadratic in a span of many `#` with no whitespace | `skills/evidence-check/scripts/evidence_check.py:1621` | **fixed** `a0624b6323ad20a85206c94f16a48343f8900720` | fixed at a0624b6323ad20a85206c94f16a48343f8900720; Executed: 0.43 s at 8 000 characters and 2.7 s at 20 000; with `#` out of the unquoted class, 0.0006 s, 215 passed and identical probe results |
| 🟢 | `MALFORMED` is graded like `DRIFTED`: 1 on a lenient run, 2 under `--strict`, 2 beside `BROKEN`, a refused record or `OLD-FORMAT`; `OLD-FORMAT` is 2 under both readings | `skills/evidence-check/scripts/evidence_check.py:2750` | confirmed | Executed: `exit_code` over every pairing; the malformed-only lenient run carries the notice as its last line and the strict run does not |
| 🟢 | #614's four observations and the shapes round 3 of work item 1790297087 already had right hold on both sides | `skills/evidence-check/scripts/evidence_check.py:1624` | confirmed | Executed: every #614 parameter and every `MALFORMED_SHAPES` value, the bare-quote shape, the opener-list shapes, `#ifdef`, `C#`, `@cache` and `org/repo#299` as expected, in a span and out |
| 🟢 | every new or moved case is red against the base checker, and the S6 and S7 pins are red against the base documents | `tests/test_a_row_points_by_content.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_evidence_check.py` | confirmed | Executed: base checker over the three modules, 30 failed and 169 passed; base documents over the new code, the S6 and S7 pins failed |
| 🟢 | every statement of `MALFORMED`'s grading in the tree says (b); the documents the spec left out state drift only and stay true | `skills/evidence-check/SKILL.md:173`, `skills/evidence-ci/SKILL.md:65`, `templates/evidence-check.yml:39`, `.github/workflows/test.yml:74` | confirmed | Read: `git grep` for `malformed` and for statements of exit 1, drift and lenient/strict outside the records, in English and Korean; README, README.ko, CONTRIBUTING and `docs/the-evidence-ledger.md` read at the lines above |
| 🟢 | the corrected rows and the re-read rows state what the code now does | `seal/releases/0.15.4.md:54`, `seal/releases/0.11.3.md:23` | confirmed | Read: word diff of every touched release file; executed: `evidence_check.py --strict .` gives 2415 ok, 0 drifted, 0 broken, 0 malformed, exit 0 |
| 🟢 | the survivor sweep is clean apart from its one judged exemption | `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/survivors.md` | confirmed | Executed: `survivor-check --range 47e32d57..591c6cdf --exempt survivors.md`, exit 0, one survivor, exempt |
| ❓ | whether the `windows-latest` leg passes over the new non-ASCII parameters | PR #621, `pytest (windows-latest, 3.12)` | ❓ out of verified scope | Pending when read. Answerer: CI at the pull request, read by the orchestrator |

## Paste-ready fixes

```python
    What each edge gives up (#614): `src/a.py@abc`, a path followed by fewer
    than six hex characters, is silent. A locator that opens with digits and
    goes on with anything but an ASCII letter, digit or `_` reads as an
    issue number when no hash follows: `docs/a.md#1장`, `docs/a.md#1-scope`,
    `docs/a.md#1.2`, `src/a.py#1>"x"`. A dotless file name takes a locator
    opening with a letter, `_`, `"` or `<` and never a digit, so
    `Makefile#1x` is silent and `C#"hello"` or `vector#<T>` is named. A
    path-less coordinate is silent where unquoted whitespace, or a `"` no
    second `"` closes, stands between its marks: `#handler @abcdef12`,
    `#handler>"a"b"@abcdef12`. With a path, the per-word rule still names
    those last two."""
```
```markdown
  now. What this gives up: `src/a.py@abc` with a hash shorter than six
  characters; a locator opening with digits and followed by anything but an
  ASCII letter, digit or underscore, when no hash follows (`docs/a.md#1장`,
  `docs/a.md#1-scope`, `docs/a.md#1.2`); `Makefile#1x`; and a path-less
  `#handler @abcdef12` or `#handler>"a"b"@abcdef12` are not named.
```
```python
def test_every_other_page_that_grades_the_flag_names_malformed():
    """Round 1's 🟡 2 of work item 1790381328. Four more places state what
    `--strict` softens, and each is held against `exit_code` rather than
    against a number written here, so the next change to the grading moves
    them or goes red."""
    lenient, strict = grading("MALFORMED")
    skill = read(os.path.join(ROOT, "skills", "evidence-check", "SKILL.md"))
    flag = table_row(skill, "`--strict`")[1]
    assert "malformed" in flag and f"exit {strict}" in flag, flag
    ci = " ".join(
        read(os.path.join(ROOT, "skills", "evidence-ci", "SKILL.md")).split()
    )
    want = (
        f"`MALFORMED`, follows the flag the way drift does: exit {lenient} "
        f"without it, {strict} with it"
    )
    assert want in ci, "evidence-ci's step 4 no longer grades MALFORMED"
    template = read(os.path.join(ROOT, "templates", "evidence-check.yml"))
    assert "softens drift\n          # and MALFORMED, and nothing else" in template
    assert f"{lenient} drift or malformed only" in ec.__doc__, "the module docstring"
```
```python
# Both marks of one coordinate: an `@` after a `#` with no whitespace between
# them outside a quoted string, so `#"x = 1  # c"@0` holds them glued and
# `@lru_cache  # memoized` does not. Searched, so every `#` is tried. The
# quoted string holds its whitespace only in a code span: outside one,
# `malformed_rows` has split the text into words before this reads it.
```
```python
# `#` is out of the unquoted class so each attempt stops at the next one:
# the attempt that starts there finds the same match, and the search stays
# linear rather than rescanning the span from every `#`.
GLUED_MARKS_RE = re.compile(r'#(?:"(?:[^"\\\n]|\\.)*"|[^\s"#])*@')
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the three touched modules at 591c6cdf | 199 passed |
| `bin/test tests/test_dispatch.py` at 591c6cdf | 16 passed (215 with the above, matching `overview.md`) |
| `evidence_check.py --strict .` at 591c6cdf | `total: 2415 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed`, exit 0 |
| `malformed_rows` over 66 shapes, each beside a good anchor, in a span and out, with the checker at 47e32d57 and at 591c6cdf | coordinates and prose as in 🟢 rows 2 and 3; the regressions of 🟡 1, ⬜ 3 and ⬜ 4 |
| `exit_code` over `MALFORMED`, `DRIFTED`, `OLD-FORMAT`, `BROKEN` alone, lenient and strict, plus `MALFORMED` with `OLD-FORMAT` and with a drifted record | 1/2, 1/2, 2/2, 2/2; 2; 1 |
| the base checker over the three touched modules | 30 failed, 169 passed: every new or moved case |
| the base `evidence-check/SKILL.md`, `evidence-ci/SKILL.md` and `test.yml` over the new code, then the lenient-run module and `test_evidence_check.py` | 2 failed (the S6 and S7 pins), 46 passed; the old step 4 fails nothing |
| 🟡 2's case planted, then each base document restored alone | green at the target; red for the flag row, for step 4 and for the template comment |
| `GLUED_MARKS_RE` with `#` removed from the unquoted class | 215 passed in the four modules; the 66 probe shapes identical; 0.0006 s where the current form takes 2.7 to 3.8 s at 20 000 characters |
| `survivor-check --range 47e32d57..591c6cdf --exempt survivors.md` | exit 0, 1 survivor, exempt |
| `gh pr checks 621` at 591c6cdf | lint, ledger, release, ubuntu and macos pass; windows-latest pending |
| the broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it on this branch. It is the sealer's, and it is not due, because this round leaves 🟡 1 and 🟡 2 open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
