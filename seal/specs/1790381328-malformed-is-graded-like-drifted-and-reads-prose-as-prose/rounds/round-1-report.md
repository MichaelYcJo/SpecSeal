# Round 1 report — 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose

| Field | Value |
|---|---|
| Target SHA | `591c6cdf` |
| Base | `origin/release/v0.15.5` = `47e32d57` |
| Range | `47e32d57..591c6cdf` (11 commits), PR #621 |
| Ran by | specseal:warden on claude-opus-5-5 |

Probes ran in a `git clone --no-local` of the worktree at the target SHA,
under the round's scratch directory, and the clone was removed afterwards.
Nothing was written in the worktree except this file.

## Summary

The grading change is right. `exit_code` returns 1 for `MALFORMED` alone
on a lenient run, 2 under `--strict`, and 2 whenever a `BROKEN` row, a
refused record or an `OLD-FORMAT` row sits beside it. The notice prints
on a malformed-only lenient run and not under `--strict`. Every statement
of `MALFORMED`'s grading I could find in the tree, by meaning and in
English and Korean, now says (b). The two ledger rows that stated the old
grading are corrected, and the tree reads `0 drifted · 0 malformed`
under `--strict`.

Rule (a) is right for every shape #614 and round 3 of work item
1790297087 named. Two things are still open:

1. **The stated trades are shorter than the real ones (🟡 1).** The
   branch silences two coordinate shapes the base named, and no document
   lists either one.
2. **Four of the new grading sentences are pinned by nothing (🟡 2).**
   `overview.md` says the third pin covers `evidence-ci`'s step 4. It
   does not: restoring the old step 4 leaves every case green.

Three ⬜ follow. One is a claim that holds only inside a code span. One is
a prose cost the new dotless-name openers bring. One is a quadratic
search.

## 🟡 1 — rule (a)'s stated trades leave out two shapes the branch silenced

`skills/evidence-check/scripts/evidence_check.py:1630-1635`, the *What each
edge gives up* paragraph of `refused_coordinate`. The same list appears in
`changelog.md:32-34`, in `spec.md` §*What each part gives up*, and in the
Notes of the S8–S12 row in the ledger fragment.

**What is wrong (executed).** I ran `malformed_rows` over 66 shapes, each
beside a good anchor, in a span and out of one, with the checker at
`47e32d57` and at `591c6cdf`. Two classes are named at the base and
silent at the target, and the list gives neither:

| Shape | Base | Target | Why the list misses it |
|---|---|---|---|
| `docs/a.md#1-scope`, `docs/a.md#1.2`, `src/a.py#1>"x"` (no hash) | named | silent | `ISSUE_TAIL_RE` lets any character except `[A-Za-z0-9_]` follow the digits, ASCII punctuation included. The list names only `docs/a.md#1장`, which is a non-ASCII letter |
| `#handler>"a"b"@abcdef12` (no path, no whitespace) | named | silent | `GLUED_MARKS_RE` cannot step over a `"` that no second `"` closes. The list names only unquoted *whitespace* between the marks |

The second shape is the bare-quote defect #299 was built for, written
without a path. With a path, the per-word rule still names it. The first
shape is silent with or without a path, as long as no hash follows.

**Why it matters.** The docstring presents the list as what each edge
gives up, and the release note repeats it as *What this gives up*. A
reader who trusts it believes `docs/a.md#1-scope` is still named. It is
not, and a ledger row that cites it reads as covered, which is the silence
#299 exists to end. Round 3 described the same trade for the issue-number
edge as *a digit-opening locator continued by a non-ASCII letter*. That
description was already too narrow, and the branch copied it.

**The fix.** Say what the code does. The behaviour is defensible: round 3
chose it knowingly for `1장`, and a hash still gets every one of these
shapes named through the glued marks. Only the account of the behaviour
is wrong. Paste-ready replacements for the docstring and the changelog
are below. The spec's list and the ledger note are records of this run,
and each takes the same wording as a correction.

## 🟡 2 — four statements of the new grading are pinned by nothing

These places state `MALFORMED`'s grading and are unpinned:

- `skills/evidence-ci/SKILL.md:65-69`, the new *1 is not only drift*
  paragraph;
- `skills/evidence-check/SKILL.md:173`, the `--strict` flag row;
- `templates/evidence-check.yml:39-50`, the step's comment;
- `skills/evidence-check/scripts/evidence_check.py:39-40`, the module
  docstring's `Exit codes:` line.

**What is wrong (executed and read).** I put the base's `SKILL.md`,
`skills/evidence-ci/SKILL.md` and `.github/workflows/test.yml` back over
the new code and ran the two modules that hold the pins. Exactly two cases
failed: the S6 pin, which fails on the verdict table, and the S7 pin, which
fails on the warning. Nothing failed for the old step 4. By reading, no
test mentions the flag row, the template comment or the docstring line
(`grep` over `tests/` for their wording finds only the docstring of
`test_letting_drift_warn_takes_both_halves`). That case pins the recipe's
*behaviour*: exit 0 and then exit 1 over a malformed row. It never reads
the sentence. So the `overview.md` divergence row, *step 4's new sentence
is text a reader acts on (contract §14)*, claims a pin that does not
exist.

**Why it matters.** This is the same class of sentence this work item had
to find by hand. The S6 case's own docstring says the old
`(exit 2, --strict or not)` row never went red when the grading moved.
Those four sentences are in the same position now. The next change to
the grading will leave them stale in silence, and contract §14 asks for
the pin in the same commit.

**The fix.** One case beside the S6 pin, reading the grading from
`exit_code` through the module's existing `grading` helper. I planted it
in the clone. It passes at the target. It fails with the base's
`evidence-check/SKILL.md` (the flag row), with the base's `evidence-ci`
`SKILL.md` (step 4), and with the base's template (the comment), each put
back one at a time.

## ⬜ 3 — "glued through a quoted string" holds only inside a code span

`skills/evidence-check/scripts/evidence_check.py:1618-1620`, and the S8–S12
ledger row's claim *`#handler>"a b"@abcdef12` is named*.

**What is wrong (executed).** `malformed_rows` splits the text left
outside code spans on whitespace before `refused_coordinate` sees it. So
the quoted string of an unticked `#handler>"a b"@abcdef12` is already in
two words, and the coordinate is silent: named in a span, silent out of
one, at both SHAs. It is not a regression. But the comment and the ledger
claim state the rule without that condition, and every parameter that
pins it is in a span. Paste-ready comment below. The ledger claim takes
*in a code span* as a correction.

## ⬜ 4 — the dotless-name openers refuse two more kinds of prose

`skills/evidence-check/scripts/evidence_check.py:1647-1649`. `C#"hello"`
and `vector#<T>` are silent at the base and named at the target
(executed). A placeholder such as `PR#<n>` takes the same branch (read).
All of these are rare in a `Code grounds` cell, and under (b) they only
warn on a lenient run. Still, it is a prose cost of item 12 that the list
under 🟡 1 does not name. The paste-ready docstring under 🟡 1 names it.

## ⬜ 5 — `GLUED_MARKS_RE` is quadratic in a span of many `#`

`skills/evidence-check/scripts/evidence_check.py:1621`. The regex is tried
at every `#`, and `[^\s"]` also matches `#`, so every attempt runs to the
end of the span. Measured on `#a` repeated: 0.43 s at 8 000 characters and
2.7 s at 20 000. No real row comes near that (the longest in the corpus is
8 831 characters, and it is prose with whitespace). Removing `#` from the
unquoted class gives the same matches, because a match that crossed an
unquoted `#` is still found by the attempt that starts at that `#`. The
same input then takes 0.0006 s. The four reader modules pass (215) with
the change, and all 66 probe shapes give identical results. This is
recorded rather than required, like the rider on `OLD_COORD_RE`.

## Also read, not counted

- **Documents the spec left out stay true.** `README.md` §*The ledger is
  checked*, the matching paragraph of `README.ko.md` (드리프트, `--strict`),
  `CONTRIBUTING.md:65` and `:119-124`, and `docs/the-evidence-ledger.md`
  §*What the checker refuses* each describe drift's grading and never
  `MALFORMED`'s. None of them claims that exit 1 means drift alone. The
  spec's *Out* decision holds. The same goes for
  `.github/scripts/rider_check.py:83`, `:96`, which is about riders, where
  `MALFORMED` does not occur, and for `hooks/evidence-advisor.py`'s
  docstring, which states no exit code.
- **The advisor cell in the reader table is true.** `failing_rows` keeps
  `MALFORMED` among the rows it names and drops drift
  (`hooks/evidence-advisor.py:142`).
- **Every caller of `exit_code` was checked.** It has one: `main`. No other
  script reads the checker's exit code except `broad_gate.py`, which passes
  `--strict` at `:2269`.
- **The windows-latest leg.** `pytest (windows-latest, 3.12)` was still
  pending on PR #621 at `591c6cdf` when I read the checks. Every other
  check passed.

## Regression tests to plant

- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, after
  `test_the_skill_states_the_grading_exit_code_returns_for_malformed`: the
  case under 🟡 2's fence. Shown red in the clone against each of the three
  base documents, one at a time.
- `tests/test_a_row_points_by_content.py`: if the smith wants the 🟡 1
  trades pinned, one parametrised case holding `docs/a.md#1-scope` and an
  unticked `#handler>"a"b"@abcdef12` beside a good anchor at `0 malformed`
  is the pin. It is not paste-ready here, because 🟡 1's fix is to the
  account and not to the code.

## Facts for the evidence ledger

- The S8–S12 row of `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md`:
  its claim that `#handler>"a b"@abcdef12` is named needs *in a code span*
  added (⬜ 3). Its Notes list of what each edge gives up takes 🟡 1's
  wording.
- Once 🟡 2's case lands, the S6 row's grounds can cite it beside
  `test_the_skill_states_the_grading_exit_code_returns_for_malformed`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | rule (a)'s list of what each edge gives up leaves out two shapes the branch silenced: a digit-opening locator continued by ASCII punctuation with no hash (`docs/a.md#1-scope`, `docs/a.md#1.2`, `src/a.py#1>"x"`), and a path-less coordinate holding an unclosed `"` between its marks (`#handler>"a"b"@abcdef12`) | `skills/evidence-check/scripts/evidence_check.py:1630` | open | Executed: `malformed_rows` over 66 shapes at 47e32d57 and 591c6cdf; both classes are named at the base and silent at the target, and the docstring, `changelog.md:32-34`, `spec.md` and the ledger note list neither |
| 🟡 2 | the grading stated in `evidence-ci`'s step 4, `SKILL.md`'s `--strict` row, the template's comment and the module docstring is pinned by nothing; `overview.md` claims step 4 is pinned | `skills/evidence-ci/SKILL.md:65` | open | Executed: with the base's three documents over the new code, only the S6 and S7 pins fail and nothing fails for step 4; a planted case goes red for each document restored alone. Read: no test holds the flag row, the template comment or the docstring line |
| ⬜ 3 | "glued through a quoted string" holds only inside a code span; an unticked `#handler>"a b"@abcdef12` is silent, and the comment and the S8–S12 ledger claim omit the condition | `skills/evidence-check/scripts/evidence_check.py:1618` | open | Executed: named in a span, silent out of one, at both SHAs. Not a regression; the ledger half is a correction to this run's own fragment |
| ⬜ 4 | the dotless-name openers `"` and `<` now name `C#"hello"` and `vector#<T>`; the list of what each edge gives up does not say so | `skills/evidence-check/scripts/evidence_check.py:1647` | open | Executed for the two shapes; read for `PR#<n>`. Rare in a Code grounds cell, and a lenient run only warns |
| ⬜ 5 | `GLUED_MARKS_RE` is quadratic in a span of many `#` with no whitespace | `skills/evidence-check/scripts/evidence_check.py:1621` | open | Executed: 0.43 s at 8 000 characters and 2.7 s at 20 000; with `#` out of the unquoted class, 0.0006 s, 215 passed and identical probe results |
| 🟢 | `MALFORMED` is graded like `DRIFTED`: 1 on a lenient run, 2 under `--strict`, 2 beside `BROKEN`, a refused record or `OLD-FORMAT`; `OLD-FORMAT` is 2 under both readings | `skills/evidence-check/scripts/evidence_check.py:2750` | confirmed | Executed: `exit_code` over every pairing; the malformed-only lenient run carries the notice as its last line and the strict run does not |
| 🟢 | #614's four observations and the shapes round 3 of work item 1790297087 already had right hold on both sides | `skills/evidence-check/scripts/evidence_check.py:1624` | confirmed | Executed: every #614 parameter and every `MALFORMED_SHAPES` value, the bare-quote shape, the opener-list shapes, `#ifdef`, `C#`, `@cache` and `org/repo#299` as expected, in a span and out |
| 🟢 | every new or moved case is red against the base checker, and the S6 and S7 pins are red against the base documents | `tests/test_a_row_points_by_content.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_evidence_check.py` | confirmed | Executed: base checker over the three modules, 30 failed and 169 passed; base documents over the new code, the S6 and S7 pins failed |
| 🟢 | every statement of `MALFORMED`'s grading in the tree says (b); the documents the spec left out state drift only and stay true | `skills/evidence-check/SKILL.md:173`, `skills/evidence-ci/SKILL.md:65`, `templates/evidence-check.yml:39`, `.github/workflows/test.yml:74` | confirmed | Read: `git grep` for `malformed` and for statements of exit 1, drift and lenient/strict outside the records, in English and Korean; README, README.ko, CONTRIBUTING and `docs/the-evidence-ledger.md` read at the lines above |
| 🟢 | the corrected rows and the re-read rows state what the code now does | `seal/releases/0.15.4.md:54`, `seal/releases/0.11.3.md:23` | confirmed | Read: word diff of every touched release file; executed: `evidence_check.py --strict .` gives 2415 ok, 0 drifted, 0 broken, 0 malformed, exit 0 |
| 🟢 | the survivor sweep is clean apart from its one judged exemption | `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/survivors.md` | confirmed | Executed: `survivor-check --range 47e32d57..591c6cdf --exempt survivors.md`, exit 0, one survivor, exempt |
| ❓ | whether the `windows-latest` leg passes over the new non-ASCII parameters | PR #621, `pytest (windows-latest, 3.12)` | ❓ out of verified scope | Pending when read. Answerer: CI at the pull request, read by the orchestrator |

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

## Paste-ready fixes

### 🟡 1 — `refused_coordinate`'s docstring (`skills/evidence-check/scripts/evidence_check.py:1630-1635`), replacing the *What each edge gives up* paragraph; it also covers ⬜ 4

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

### 🟡 1 — `changelog.md:32-34`, replacing the *What this gives up* sentence

```markdown
  now. What this gives up: `src/a.py@abc` with a hash shorter than six
  characters; a locator opening with digits and followed by anything but an
  ASCII letter, digit or underscore, when no hash follows (`docs/a.md#1장`,
  `docs/a.md#1-scope`, `docs/a.md#1.2`); `Makefile#1x`; and a path-less
  `#handler @abcdef12` or `#handler>"a"b"@abcdef12` are not named.
```

### 🟡 2 — destination `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, after `test_the_skill_states_the_grading_exit_code_returns_for_malformed`

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

### ⬜ 3 — the comment above `GLUED_MARKS_RE` (`skills/evidence-check/scripts/evidence_check.py:1618-1620`)

```python
# Both marks of one coordinate: an `@` after a `#` with no whitespace between
# them outside a quoted string, so `#"x = 1  # c"@0` holds them glued and
# `@lru_cache  # memoized` does not. Searched, so every `#` is tried. The
# quoted string holds its whitespace only in a code span: outside one,
# `malformed_rows` has split the text into words before this reads it.
```

### ⬜ 5 — `GLUED_MARKS_RE` (`skills/evidence-check/scripts/evidence_check.py:1621`)

```python
# `#` is out of the unquoted class so each attempt stops at the next one:
# the attempt that starts there finds the same match, and the search stays
# linear rather than rescanning the span from every `#`.
GLUED_MARKS_RE = re.compile(r'#(?:"(?:[^"\\\n]|\\.)*"|[^\s"#])*@')
```

Needs a fix: yes — 🟡 1 (the list of what rule (a) gives up omits two shapes the branch silenced, in the docstring and the release note) and 🟡 2 (four statements of the new grading are unpinned, and `overview.md` claims a pin for step 4 that does not exist)
Loses a record or crashes: no

## Proof block

Files opened this round:

- `skills/evidence-check/scripts/evidence_check.py` (lines 36-45, 60-130, 1560-1800, 2535-2550, 2715-2790, 2955-2985), and the same file at 47e32d57 for the probes
- `skills/evidence-check/SKILL.md` (lines 1-20, 150-225, 255-292, 455-505)
- `skills/evidence-ci/SKILL.md` (lines 30-120)
- `templates/evidence-check.yml` (lines 1-50)
- `.github/workflows/test.yml` (the range's hunks)
- `tests/test_a_row_points_by_content.py` (lines 860-1200), `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` (the range's hunks and helpers), `tests/test_evidence_check.py` (lines 240-290)
- `hooks/evidence-advisor.py` (lines 20-45, 100-120), `hooks/ledger-migrate.py` (lines 65-95), `.github/scripts/rider_check.py` (lines 75-100), `bin/evidence-check`, `bin/test`
- `README.md` (lines 135-165), `README.ko.md` (lines 136-150), `CONTRIBUTING.md` (lines 55-70, 110-135), `docs/the-evidence-ledger.md` (lines 60-100)
- `seal/releases/0.11.3.md`, `0.15.4.md`, `0.4.0.md`, `0.8.3.md`, `0.9.0.md`, `0.13.1.md` (the range's word diff), `seal/releases/0.15.3.md:43`, `seal/releases/0.4.0.md:46`
- `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md`
- this work item's `spec.md`, `overview.md`, `survivors.md`, `changelog.md`, `phases/phase-3.md`
- `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/rounds/round-3-report.md` and `questions.md`
