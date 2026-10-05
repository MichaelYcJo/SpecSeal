# Post-review check — 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict

Target SHA: fb698f90 · Base: `release/v0.18.3` at a3aa139a · PR #804 (draft, `chain: capped`)
Range under check: 328d969f..fb698f90 (the code is d2db788e; c3788c92 and fb698f90 are records)
Ran by: specseal:warden on claude-opus-5-5

This is a verifying pass over the post-review fix for #812, not a round:
the run is capped. It reports what it finds at the severity it finds it.

## Summary

#812 is closed for every shape round 3 named. R1, R1-ini, R2, R2b and R3
read `new?` at fb698f90, where 56c8eb0d and 328d969f gave `failing on base
too` and a3aa139a gave `new`. No word moved toward `failing on base too`
against 56c8eb0d.

The design rule is not closed. Enumerating every path to `failing on base
too` found two shapes in which the target gives it where a3aa139a gave
`new`. Both are decisive by this pass's own bar, so both are 🔴.

- **🔴 1 — the "confirmed by its dotted name" step is itself a dotted-name
  guess.** A test is placed by its path wherever its dotted name *starts
  with* that path. A module of the package `tests/test_api/` that inherits,
  or imports, a test from `tests/test_api.py` has the dotted name
  `tests.test_api.test_users.TestU` and the `file` `tests/test_api.py`. The
  prefix check passes, and the base's failure in the package is placed on
  the module the branch broke. This is round 1's P1 again, reached through
  the confirmation step.
- **🔴 2 — `ls-files --cached --others` is not every file pytest can name.**
  A test directory reached through a tracked symlink is not listed. R3 with
  a symlink in place of the generated file reads `failing on base too`
  again. The same holds for a submodule a row initialises and a nested
  repository, by reading.

A tested fix closes both. It carries the dotted name beside the path and
demotes a path where a longer part of the dotted name spells a module, and
it judges a directory against the disk rather than the listing. With it,
every planted case of every round keeps its word, the five shapes above
read `new?`, and the three narrow modules give 519 passed, 1 skipped.

## Every path to `failing on base too` at fb698f90, by construction

`report_words` (`skills/verify/scripts/broad_gate.py:2025-2111`) returns
`ON_BASE` in one branch only: `{f} in places` with `f` not in `ambiguous`
(`:2099-2102`). Working back from it:

1. `places` gets a set only from a failing case with `exact` true
   (`:2080-2096`). A case known by its dotted name only adds to `guessed`,
   which can only cost a word. So the one source is an exact case.
2. `exact` is set in `report_cases` (`:1953`): the case carries `file`, and
   the dotted name's leading components equal `dotted(file)`.
3. The case lands on `f` where `tests = {D/address : D in roots}` meets
   `here = {C/f : C in heres}`. It is not `ambiguous` only where `tests` is
   one path and equals `here`.
4. `roots` and `heres` come from `directories_holding` over `tree`, which
   `compare_at_base` lists after the run with `git ls-files -z --cached
   --others` (`:2394-2395`).

So a wrong `failing on base too` needs one of two things. Either step 2
calls a path the test's own when it is not, or step 4's listing lacks a
file pytest named, so the true rootdir or run directory drops out of a set
that is then a wrong singleton. Every other step is exact for paths without
`..` (and `..` addresses are kept out of the directory search). 🔴 1 is the
first and 🔴 2 the second.

| Attack | Layout | fb698f90 | a3aa139a | 56c8eb0d | with the fix |
|---|---|---|---|---|---|
| Step 2: inherited from the module the package is named like | N1 | `failing on base too` | `new` | `failing on base too` | `new?` |
| Step 2: the same under `-n 2` | N1-xdist | `failing on base too` | `new` | `failing on base too` | `new?` |
| Step 2: an imported test function, no class | N1b | `failing on base too` | `new` | `failing on base too` | `new?` |
| Step 2: both files handed, no directory in the row | N1c | `failing on base too` / `new` | `new` / `failing on base too` | same as target | `new?` / `new?` |
| Step 4: a symlinked test directory and a mirror | N3 | `failing on base too` | `new` | `failing on base too` | `new?` |
| Step 4: a generated file and a mirror (round 3's R3) | R3 | `new?` | `new` | `failing on base too` | `new?` |
| Step 4: a case-only rename on a case-insensitive disk | N4 | `new?` | `new` | `new?` | `new?` |
| A report path with `..` (a test outside the rootdir) | N5 | `new` (noted below) | `new` | `new` | `new` |
| Run directory equal to the rootdir, a same-named file elsewhere | N6 | `new?` | `failing on base too` | `new?` | `new?` |
| An ignored copy of the tests the row writes | N7 | `new?` | `failing on base too` | `failing on base too` | `new?` |

N1c's second file is `tests/test_api/test_users.py`. The base fails it
through its inherited test, and the target gives it a measured `new`, which
is wrong but strict.

## Findings from execution

### 🔴 1 — a test a package's module inherits from the module it is named like is placed on that module

`skills/verify/scripts/broad_gate.py:1953` (the prefix check in
`report_cases`) and `:2079-2096` (the placement in `report_words`).

`xunit1` writes the file a test's function is defined in. The fix for round
2's 🟡 2 kept that path only where the dotted name starts with it, and #812
made that path the one source of `failing on base too`. A prefix is still a
dotted-name reading: `tests.test_api` is a prefix of
`tests.test_api.test_users.TestU` whether `test_users` is a class in
`tests/test_api.py` or a module in `tests/test_api/`. The second is P1's
layout, which round 1 found.

Executed (N1). The base holds `tests/test_api.py`, with a passing
`test_two` and a class `Base` holding `test_shared`. It also holds
`tests/test_api/test_users.py`, whose `TestU(Base)` fails `test_shared`.
The branch breaks `test_two` and mends `TestU`. The base's report, kept by
the gate, reads:

```
tests.test_api.test_users.TestU test_shared file=tests/test_api.py FAIL
tests.test_api                  test_two    file=tests/test_api.py pass
```

The failing case is exact, `roots` and `heres` are both the root, and
`tests/test_api.py` reads `failing on base too`. The branch introduced its
only failure. N1b does the same with an imported test function and a
fixture of the package's own, N1-xdist under `-n 2`, and N1c with both
files handed and no directory in the row.

**Regression against the base: yes.** a3aa139a reads `new` in N1, N1b and
N1-xdist. 56c8eb0d and 328d969f already read `failing on base too`, so
d2db788e did not introduce it. It is 9639f2ff's prefix check, which #812's
design made the one gate on the permissive word.

**Why it matters.** It takes a shared base class kept in a test module, and
a test package of the same name beside it. Round 1's P1 already showed that
a package named like a module is a layout people write. The texts promise
the opposite. Rule 3 says a test a class inherits "is known only by its
dotted name … such a test measures nothing". The changelog says "a package,
a class or a deeper module named like the file is never taken for it". The
`report_words` docstring says a test inherited from another module
"measures nothing".

**The fix reads the dotted name past the path against the files.** Where a
longer leading part of the dotted name spells a module that is a file under
the rootdir, the test was collected there, and its path is only where it was
defined. Such a case becomes a dotted one and measures nothing. The diff is
under *Paste-ready fixes*. The added function is named collected_below
(NAME NOT IN TREE).

### 🔴 2 — a test file pytest reached through a symlink is not on the tree, and a mirror is taken for the rootdir

`skills/verify/scripts/broad_gate.py:2394-2395` (the listing) and
`:2004-2022` (`directories_holding`).

d2db788e lists the scratch worktree after the run so a generated file is on
the tree. `git ls-files` lists a tracked symlink as one entry and never what
is under it. pytest names a test it reached through the link by the link's
path.

Executed (N3). This is round 3's R3 with one change: no file is generated,
and `gen` is a tracked symlink to `realgen`. The row is `{SUITE_ROW} gen
vendor`. The base's report names `tests/test_one.py`, `tests/test_two.py`
(failing) and `gen/test_g.py`. The listing after the run holds `gen`,
`realgen/test_g.py` and the vendored copies, and not `gen/test_g.py` (both
read from the kept files). `vendor` is then the one directory holding every
report path, and the root's failing `tests/test_two.py` lands on the handed
`vendor/tests/test_two.py`.

**Regression against the base: yes.** a3aa139a reads `new`, and fb698f90,
56c8eb0d and 328d969f read `failing on base too`. d2db788e closed the
generated member of the class and left this one.

**Why it matters, and how far it reaches.** The shape is as narrow as R3: a
test directory the report reaches through a path git does not list, and a
directory holding every report path under the same relative names. The
other members are read, not run. A submodule a row initialises is listed as
one gitlink entry. A nested repository is listed as its directory. A path
typed in another case on a case-insensitive disk is not listed either (N4,
which is strict only because no mirror exists). The design sentence this
pass was handed, "giving exactly one rootdir and one run directory", holds
only where the listing has every file pytest opened.

**The fix asks the disk.** Every directory of the listing, and the root, is
a candidate. A path counts where `os.path.isfile` finds it under the scratch
worktree, which follows the link and reaches a submodule's or a nested
repository's files. Extra candidates can only make a placement ambiguous,
so the change cannot move a word toward `failing on base too`. With it, N3
reads `new?` and R3 keeps `new?`.

## Findings from reading

- **⬜ 3 — the listing runs once per prefix tried, not once per prefix
  whose report is read.** `skills/verify/scripts/broad_gate.py:2389-2395`
  runs for every prefix outside the collection pass, before anything checks
  that the prefix wrote a report. A lint-first row lists the worktree after
  the lint and after the formatter too. The `overview.md` bullet ("one
  longer git call per prefix read") and this pass's prompt say otherwise.
  It costs time on a failing gate only, and no word, so it is ⬜. A guard on
  `os.path.exists(report)` makes the sentence true.
- **⬜ 4 — `overview.md` §*Not done* names a cost the listing has, and not
  the word it costs.** An ignored or untracked copy the row writes (a
  `build/` tree, a `.venv` a runner creates) that holds the handed file's
  relative path makes that file `new?`. Executed (N7): 56c8eb0d gave the
  true `failing on base too`, and the target gives `new?`. That is the
  strict direction and rule 3 covers it ("Where a second directory fits
  either"). The record says only "one longer git call". A correction to
  this run's paperwork, not counted.
- **⬜ 5 — `overview.md` and the ledger's R2 row say an inherited test
  measures nothing.** `overview.md` §*Not done* ("an inherited test, whose
  `file` is its parent class's module") and
  `seal/ledger/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict.md`
  R2 ("an inherited test, every test under `--junit-prefix` — measures
  nothing") are false for N1 at fb698f90 and true with 🔴 1's fix. A
  correction to paperwork, not counted.
- **Outside this change, noted only.** N5 hands the gate a test outside
  pytest's rootdir (`cd sub` with the ini in `sub`, the row naming
  `../tests`). The gate's comparison names the failing file `test_two.py`,
  which does not exist in `sub`; which `FAILED` text produced that name was
  not read. The file reads a measured `new` at every SHA, a3aa139a
  included. The base does fail
  that test, so the word is wrong, in the strict direction.

## Strictness accepted

Every word that moved toward `new?` against 56c8eb0d, from the end-to-end
cases and probes (executed) and the unit rows `REPORTS` pins (read):

| Shape | 56c8eb0d | fb698f90 | True word at the base |
|---|---|---|---|
| Q4c, a file failing at the base through a test it inherits from a helper | `failing on base too` | `new?` | `failing on base too` — a cost, stated in rule 3 and `overview.md` |
| N7, an ignored copy the row writes | `failing on base too` | `new?` | `failing on base too` — a cost, not stated (⬜ 4) |
| R1, R1-ini (`--junit-prefix`) | `failing on base too` | `new?` | `new` — the fix |
| R2, R2b (inherited, package and deeper module) | `failing on base too` | `new?` | `new` — the fix |
| R3 (generated file and a mirror) | `failing on base too` | `new?` | `new` — the fix |
| Unit rows `dotted-rootdir-above`, `dotted-rootdir-below`, `dotted-rootdir-is-tests` | `failing on base too` (and `new`) | `new?` | read off constructed reports |
| Unit rows `dotted-two-files`, `dotted-two-offsets` | `new?` and `new` | `new?` | read off constructed reports |

None moved toward `failing on base too` against 56c8eb0d: every case and
probe that reads it at fb698f90 reads it at 56c8eb0d too. Against
a3aa139a, five do: N1, N1-xdist, N1b, N1c and N3 (🔴 1 and 🔴 2).

## The texts against the code at fb698f90

| Text | Against the code |
|---|---|
| Rule 3: placed "only by the path … only where the test's dotted name starts with that path, and only read against the files in the base's worktree after the run" | Describes the code. Not enough for the outcome: 🔴 1 and 🔴 2 |
| Rule 3: an inherited test "is known only by its dotted name … such a test measures nothing" | False for N1 (🔴 1) |
| Rule 3: "Where a second directory fits either, the file reads `new?`" | True; it also covers N6 and N7 |
| Rule 3 and the docstring: the both-directories sentence, said of the run | True: P7-mixed reads `failing on base too` and P7-both `new?`, at every SHA where the sentence says so (N8) |
| `report_words` docstring: "`failing on base too` comes only from a test's path" | True of the code. "A test known only by its dotted name — one a class inherits from another module" is false for N1 |
| `offsets` docstring: "It decides no word" | True: it is read only into `guessed`, which can only cost a word |
| `compare_at_base` comment: "a test file the row generated is one pytest named, so pytest's rootdir is among the directories holding every path" | True for a generated file, false for a symlinked one (🔴 2) |
| The `UNPLACED` reason | True of every way the code reaches it. Round 3's ⬜ 4 is closed |
| Changelog: "so a package, a class or a deeper module named like the file is never taken for it, and a test file the row generates is found" | The first half is false for N1. The second is true |
| Changelog: the both-directories sentences | True (N8) |
| `overview.md` §*Not done* | ⬜ 3, ⬜ 4, ⬜ 5 |

## The seal

**A green run is unchanged** (read). `compare_at_base` is called only from
the suite arm, only when that arm failed and `failing_files` named a file
(`skills/verify/scripts/broad_gate.py:3541-3544`). The range touches nothing
outside `report_cases`, `offsets`, `directories_holding`, `report_words`,
`UNPLACED` and `compare_at_base`.

**A failing run lists the worktree more often than one call per prefix
read** (read). It is one `git ls-files -z --cached --others` per prefix
tried outside the collection pass (⬜ 3). Without `--exclude-standard` the
call walks every ignored directory the row wrote. 🔴 2's fix adds one
`isfile` per candidate directory until one fails, on a failing gate only.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A test a module of a package inherits, or imports, from the module the package is named like has `file` set to that module and a dotted name starting with it. It is placed on the module, and the base's failure there reads `failing on base too` for a failure the branch introduced. A regression against a3aa139a, present since 9639f2ff and left open by d2db788e | `skills/verify/scripts/broad_gate.py:1953`, `skills/verify/scripts/broad_gate.py:2079-2096` | open | Executed N1, N1-xdist, N1b, N1c: `failing on base too` at fb698f90, 56c8eb0d and 328d969f, `new` at a3aa139a, `new?` with the fix |
| 🔴 2 | `git ls-files --cached --others` does not list a file pytest reached through a tracked symlink. A mirror directory holding every report path is then the only rootdir, and the root's failing test is placed on the mirror's handed file. A regression against a3aa139a; d2db788e closed only the generated member | `skills/verify/scripts/broad_gate.py:2394-2395`, `skills/verify/scripts/broad_gate.py:2004-2022` | open | Executed N3: `failing on base too` at fb698f90, 56c8eb0d and 328d969f, `new` at a3aa139a, `new?` with the fix |
| ⬜ 3 | The listing runs once per prefix tried, before anything checks the prefix wrote a report, where the record says once per prefix read | `skills/verify/scripts/broad_gate.py:2389-2395` | open | Read |
| ⬜ 4 | `overview.md` §*Not done* names the listing's time cost and not the word it costs: an ignored copy the row writes makes the handed file `new?` | `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/overview.md` | open | Executed N7: `failing on base too` at 56c8eb0d, `new?` at fb698f90. A correction to this run's paperwork, not counted in Needs a fix |
| ⬜ 5 | `overview.md` and the ledger's R2 row say an inherited test measures nothing, which N1 contradicts at fb698f90 | `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/overview.md`, `seal/ledger/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict.md` | open | Read against N1. A correction to paperwork, not counted in Needs a fix |
| 🟢 | round 3's first finding is closed — `--junit-prefix` and an inherited test of a package or a deeper module no longer place a dotted name | `skills/verify/scripts/broad_gate.py:2079-2084` | confirmed | Executed R1, R1-ini, R2, R2b: `new?` at fb698f90, `failing on base too` at 56c8eb0d and 328d969f, `new` at a3aa139a |
| 🟢 | round 3's second finding is closed for a generated file — the listing after the run holds it | `skills/verify/scripts/broad_gate.py:2394-2395` | confirmed | Executed R3: `new?` at fb698f90. The symlinked member is 🔴 2 |
| 🟢 | round 3's third finding is closed — the both-directories sentence is said of the run in rule 3, the docstring and the changelog | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2304-2310` | confirmed | Executed N8: P7-mixed `failing on base too` and P7-both `new?` for `tests/test_y.py`, matching the sentence |
| 🟢 | round 3's ⬜ 4 is closed — the `UNPLACED` reason names the dotted name and the second directory | `skills/verify/scripts/broad_gate.py:1897-1902` | confirmed | Read; pinned in `test_the_unmeasured_word_says_so_and_every_reader_is_told_it` |
| 🟢 | No word moved toward `failing on base too` against 56c8eb0d | `skills/verify/scripts/broad_gate.py:2025-2111` | confirmed | Executed 37 end-to-end cases and 12 probes at both SHAs |
| 🟢 | A green run is unchanged | `skills/verify/scripts/broad_gate.py:3541-3544` | confirmed | Read; the three narrow modules pass at fb698f90 |
| ❓ | Windows (backslash `file`, `cmd.exe`) and the `file` attribute on pytest 7 and 8 | `skills/verify/scripts/broad_gate.py:1918-1957` | ❓ out of verified scope | Read only, on macOS with pytest 9.1.1. CI's three-platform job answers Windows; the repository owner answers pytest 7 and 8 |

## Executed probes

| What was run | Result |
|---|---|
| The 37 end-to-end test functions of `tests/test_the_seal_is_taken_once_by_the_sealer.py` that read a word (every #747, #761 and #789 layout the module plants: P1–P7, Q1–Q12 where planted, R1–R3), with a plugin that logs each word, in four `git clone --no-local` copies at fb698f90 holding the gate of fb698f90, a3aa139a, 56c8eb0d and 328d969f | Every case ran at each SHA. The words are in the table below |
| This pass's probes N1–N8 at the same four SHAs | The table below |
| A fifth copy with the fix below, every case and probe rerun | 59 passed (every planted case keeps its word); the last column |
| The three regression cases below, at fb698f90, with the fix and at a3aa139a | 3 failed at fb698f90 (each `'failing on base too' == 'new? …'`), 3 passed with the fix, 3 failed at a3aa139a |
| `bin/test -q` over `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` and `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, in the fb698f90 copy and in the fixed copy | 519 passed, 1 skipped (exit 0) at both |
| N1 and N3 rerun with a kept base temp; the base reports and the N3 listing read | N1's failing case is `tests.test_api.test_users.TestU` with `file=tests/test_api.py`; N3's report names `gen/test_g.py`, and the listing holds `gen` and `realgen/test_g.py`, not `gen/test_g.py` |
| `uvx ruff check` and `uvx ruff format` on the fixed gate | clean, unchanged |
| The broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the fixes land |

```
case / file                                                    fb698f90             a3aa139a             56c8eb0d             328d969f             with the fix
N1 inherited from the handed module   tests/test_api.py        failing on base too  new                  failing on base too  failing on base too  UNPLACED
N1 the same under -n 2                tests/test_api.py        failing on base too  new                  failing on base too  failing on base too  UNPLACED
N1b imported test function            tests/test_api.py        failing on base too  new                  failing on base too  failing on base too  UNPLACED
N1c two handed files                  tests/test_api.py        failing on base too  new                  failing on base too  failing on base too  UNPLACED
N1c two handed files                  tests/test_api/test_users.py new              failing on base too  new                  new                  UNPLACED
N3 symlinked test directory           vendor/tests/test_two.py failing on base too  new                  failing on base too  failing on base too  UNPLACED
N4 case-only rename                   tests/test_two.py        UNPLACED             new                  UNPLACED             UNPLACED             UNPLACED
N5 a test outside the rootdir         test_two.py              new                  new                  new                  new                  new
N6 same-named file elsewhere          tests/test_two.py        UNPLACED             failing on base too  UNPLACED             UNPLACED             UNPLACED
N7 ignored copy the row writes        tests/test_two.py        UNPLACED             failing on base too  failing on base too  failing on base too  UNPLACED
N8 P7-both                            tests/test_x.py          new                  new                  new                  new                  new
N8 P7-both                            tests/test_y.py          UNPLACED             failing on base too  UNPLACED             UNPLACED             UNPLACED
N8 P7-both                            tests/test_z.py          UNPLACED             new                  UNPLACED             UNPLACED             UNPLACED
N8 P7-mixed                           tests/test_y.py          failing on base too  failing on base too  failing on base too  failing on base too  failing on base too
N8 P7-mixed                           tests/test_w.py          failing on base too  failing on base too  failing on base too  failing on base too  failing on base too
R1 junit-prefix (row)                 tests/test_api.py        UNPLACED             new                  failing on base too  failing on base too  UNPLACED
R1 junit-prefix (ini)                 tests/test_api.py        UNPLACED             new                  failing on base too  failing on base too  UNPLACED
R2 inherited, package                 tests/test_api.py        UNPLACED             new                  failing on base too  failing on base too  UNPLACED
R2b inherited, deeper module          tests/test_two.py        UNPLACED             new                  failing on base too  failing on base too  UNPLACED
R3 generated file                     vendor/tests/test_two.py UNPLACED             new                  failing on base too  failing on base too  UNPLACED
P1 package named like the file        tests/test_api.py        UNPLACED             new                  UNPLACED             UNPLACED             UNPLACED
P2 deeper same-named module           tests/test_two.py        UNPLACED             new                  UNPLACED             UNPLACED             UNPLACED
Q1 module every test sits beside      tests/test_two.py        UNPLACED             new                  UNPLACED             UNPLACED             UNPLACED
Q3 shorter same-named path            a/tests/test_two.py      UNPLACED             new                  UNPLACED             UNPLACED             UNPLACED
Q4b inherited, defining file          tests/test_two.py        new                  new                  new                  new                  new
Q4c inherited from a helper           tests/test_two.py        UNPLACED             failing on base too  failing on base too  failing on base too  UNPLACED
parts dropping args (sh -c, no:junit) tests/test_two.py        NO_RUNNER            new                  NO_RUNNER            NO_RUNNER            NO_RUNNER
two runners counted (plain, xdist)    x, y, z                  MULTI_RUNNER         (no word)            MULTI_RUNNER         MULTI_RUNNER         MULTI_RUNNER
P3 runner dropping args first         tests/test_two.py        MULTI_RUNNER         (no word)            MULTI_RUNNER         MULTI_RUNNER         MULTI_RUNNER
every other planted case (25 words)   —                        same word at the four copies after a3aa139a
```

"(no word)" is a3aa139a's gate printing no comparison line for the file.
The 25 other words are each `failing on base too`, `new`, `STOPPED_EARLY`,
`NOTHING_TOGETHER` or `NO_RUNNER`, identical across the four copies after
a3aa139a. a3aa139a differs only toward the strict side or in its own older
`new?` reasons, and in one case the other way within the blocking words:
`test_a_run_with_no_summary_line_is_read_off_its_report[no-summary]` reads
`new` at fb698f90, 56c8eb0d and 328d969f and `new?` at a3aa139a, which is round 1's report
reading and not a move toward `failing on base too`.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A test outside pytest's rootdir is handed to the base by a name that does not exist there and reads a measured `new` (N5), at every SHA including a3aa139a. Strict, outside this change | a new issue | the orchestrator, who files issues |

## Paste-ready fixes

### 🔴 1 and 🔴 2 — demote a path a longer dotted name contradicts, and ask the disk

Applied together in the fifth copy. Every planted case kept its word, the
three narrow modules gave 519 passed, 1 skipped, and `ruff check` and
`ruff format` left it clean.

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ -1951,12 +1951,25 @@ def report_cases(text):
         # (#789 round 2's 🟡 2). A file the dotted name starts with is the
         # test's own; any other is placed by the dotted name.
         if where and name[: len(dotted(where))] == dotted(where):
-            cases.append((tuple(where.split("/")), failed, True))
+            cases.append((tuple(where.split("/")), failed, True, name))
             continue
-        cases.append((name, failed, False))
+        cases.append((name, failed, False, name))
     return cases
 
 
+def collected_below(name, address, roots, exists):
+    """True where a leading part of the dotted `name`, longer than the path
+    `address`, spells a module that is a file under one of `roots`: the test
+    was collected from that module, and `address` is only where its function
+    is defined -- a test a module of a package inherits, or imports, from
+    the module the package is named like."""
+    for k in range(len(dotted("/".join(address))) + 1, len(name) + 1):
+        module = (*name[: k - 1], f"{name[k - 1]}.py")
+        if any(exists(joined(d, module)) for d in roots):
+            return True
+    return False
+
+
 def dotted(path):
@@ -2001,28 +2014,31 @@ def joined(directory, address):
     return posixpath.normpath("/".join((*directory, *address)))
 
 
-def directories_holding(addresses, tree):
+def directories_holding(addresses, tree, exists=None):
     """Every directory of `tree`, the files in the base's worktree, under
     which each of `addresses` names a file (#789 round 2's 🟡 1, #812). An address
     that climbs out of the directory it is read from (`..`) is not asked
-    about; where every one does, the answer is empty."""
-    # Sorted, so the address the candidate directories are drawn from is the
-    # same on every run.
+    about; where every one does, the answer is empty.
+
+    `exists` asks the disk where the caller has one: every directory of the
+    tree is then a candidate, and a file is one the disk holds, so a path
+    pytest reached through a symlink, a submodule or a nested repository,
+    which `git ls-files` does not list, still counts."""
     plain = sorted(a for a in addresses if ".." not in a)
     if not plain:
         return set()
-    n = len(plain[0])
-    found = set()
+    if exists is None:
+        exists = tree.__contains__
+    directories = {()}
     for path in tree:
         parts = tuple(path.split("/"))
-        if len(parts) >= n and parts[len(parts) - n :] == plain[0]:
-            directory = parts[: len(parts) - n]
-            if all(joined(directory, a) in tree for a in plain):
-                found.add(directory)
-    return found
+        directories.update(parts[:i] for i in range(1, len(parts)))
+    return {d for d in directories if all(exists(joined(d, a)) for a in plain)}
 
 
-def report_words(text, files, code, stopped, alone=False, tree=frozenset()):
+def report_words(
+    text, files, code, stopped, alone=False, tree=frozenset(), exists=None
+):
@@ -2073,10 +2089,14 @@ def report_words(text, files, code, stopped, alone=False, tree=frozenset()):
         word = NEW if alone and code in NOTHING_COLLECTED_EXITS else NOTHING_TOGETHER
         return {f: word for f in files}
     paths = {f: tuple(f.split("/")) for f in files}
-    roots = directories_holding({a for a, _, exact in cases if exact}, tree)
-    heres = directories_holding(set(paths.values()), tree)
+    roots = directories_holding({a for a, _, exact, _ in cases if exact}, tree, exists)
+    heres = directories_holding(set(paths.values()), tree, exists)
     named, ambiguous, guessed, places = set(), set(), set(), []
-    for address, failed, exact in cases:
+    for address, failed, exact, name in cases:
+        if exact and collected_below(name, address, roots, exists or tree.__contains__):
+            # The path is where the function is defined, and a longer part of
+            # the dotted name spells the module that collected it.
+            exact, address = False, name
         if not exact:
             # Known only by its dotted name: it can only cost a word.
             if failed:
@@ -2400,6 +2420,7 @@ def compare_at_base(root, base, command, files, keep):
                     bool(STOPPED_EARLY_RE.search(tried.text)),
                     alone=bool(alone),
                     tree=tree,
+                    exists=lambda p: os.path.isfile(os.path.join(scratch, p)),
                 )
                 if words is not None:
                     settled.append(k)
```

The docstrings that describe the rule take the same change. In
`report_cases`, after "A file the dotted name starts with is the test's
own":

```
        # own, unless a longer part of the dotted name spells a module the
        # base's worktree holds (`report_words`, #812's post-review 🔴 1);
        # any other is placed by the dotted name.
```

In `report_words`, the sentence "A test known only by its dotted name — one
a class inherits from another module, every test of a run under
`--junit-prefix` — measures nothing" becomes:

```
    A test known only by its dotted name — one a class inherits, or a module
    imports, from another module, every test of a run under `--junit-prefix`
    — measures nothing, and so does a test whose path a longer part of its
    dotted name contradicts (a package's module inheriting from the module
    the package is named like): a failing one makes every handed file it
    could be (`offsets`) read `UNPLACED`. `tree` names the candidate
    directories and `exists` asks the disk, so a file pytest reached through
    a symlink or a submodule, which the listing lacks, still counts.
```

Rule 3 in `templates/config.md`, from "A test is placed on a file only by
the path" to "and so does a file only such tests name (#812).", becomes the
following. The pin in
`test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`
takes the same text.

```
A test is placed on a file only by the path pytest's report gives it (the gate also appends `-o junit_family=xunit1`, which writes that path), only where the test's dotted name starts with that path and no longer part of the dotted name spells a module in the base's worktree, and only read against the files on disk in the base's worktree after the run, tracked, written by the run, ignored or reached through a symlink or a submodule: pytest's rootdir is a directory under which every such path is a file, the directory the row runs pytest in is one under which every file the run was handed is, and the test is placed on the file only where each is one directory and the two name one file. Where a second directory fits either, the file reads `new?`. That path is the file a test's function is defined in, so a test a class inherits, or a module imports, from another module, and every test of a run under `--junit-prefix`, is known only by its dotted name, and a dotted name cannot tell a module from a package of the same name: such a test measures nothing, a file a failing one could be reads `new?`, and so does a file only such tests name (#812).
```

The changelog's sentences from "and reads that path against the files" to
"is known only by its dotted name." become:

```
  test's file as a path, and reads that path against the files on disk in
  the base's worktree after the run, tracked, written by the run, ignored or
  reached through a symlink, so a package, a class or a deeper module named
  like the file is never taken for it, and a test file the row generates is
  found. Where a same-named file the path could also name sits under
  another rootdir or another directory the row could run pytest in, the
  file reads `new?`. That path is where a test's function is defined, so a
  test a class inherits, or a module imports, from another module, and
  every test of a row under `--junit-prefix`, is known only by its dotted
  name, and so is a test a longer part of whose dotted name spells a module
  of the worktree.
```

### ⬜ 3 — list the worktree only after a run that wrote its report

```diff
-                listed = git(scratch, "ls-files", "-z", "--cached", "--others")
-                tree = frozenset((listed or "").split("\0")) - {""}
+                listed = (
+                    git(scratch, "ls-files", "-z", "--cached", "--others")
+                    if os.path.exists(report)
+                    else None
+                )
+                tree = frozenset((listed or "").split("\0")) - {""}
```

## Regression tests to plant

Destination: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, after
#812's cases. Each was run as written from a module importing that file's
helpers: 3 failed at fb698f90, each with `'failing on base too' == 'new?
…'`, and 3 passed with the fix. They also fail at a3aa139a, whose words
and constants differ. The module already imports `os`.

```python
API_DEFINES_BASE = (
    "class Base:\n    v = 1\n\n    def test_shared(self):\n"
    "        assert self.v == 1, 'planted'\n\n\n"
)
USERS_INHERITS_FROM_API = (
    "import os\nimport sys\n\n"
    "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
    "from test_api import Base  # noqa: E402\n\n\n"
    "class TestU(Base):\n    v = {}\n"
)


def test_a_package_inheriting_from_the_module_it_is_named_like_is_not_placed_on_it(
    tmp_path,
):
    """A module of the package `tests/test_api/` inherits its failing test
    from `tests/test_api.py`. `xunit1` writes the parent's file, and the
    dotted name `tests.test_api.test_users.TestU` starts with it, so the
    base's failure was placed on `tests/test_api.py`, whose own test the
    branch broke: `failing on base too`, where a3aa139a read `new`."""
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW,
        {
            "tests/test_api.py": API_DEFINES_BASE + PASSING_TWO,
            "tests/test_api/test_users.py": USERS_INHERITS_FROM_API.format(2),
        },
        {
            "tests/test_api.py": API_DEFINES_BASE + FAILING_TWO,
            "tests/test_api/test_users.py": USERS_INHERITS_FROM_API.format(1),
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_api.py") == gate_module().UNPLACED, (
        out.stdout
    )


def test_a_path_a_longer_part_of_the_dotted_name_contradicts_places_nothing():
    """The unit half: a path whose dotted name runs on into a module the
    tree holds is where the function is defined, not where it was
    collected."""
    gate = gate_module()
    report = junit(
        [
            ("tests.test_api", "test_two", "", "tests/test_api.py"),
            (
                "tests.test_api.test_users.TestU",
                "test_shared",
                "failure",
                "tests/test_api.py",
            ),
        ]
    )
    tree = frozenset({"tests/test_api.py", "tests/test_api/test_users.py"})
    got = gate.report_words(report, ["tests/test_api.py"], 1, False, tree=tree)
    assert got == {"tests/test_api.py": gate.UNPLACED}


@pytest.mark.skipif(os.name == "nt", reason="a tracked symlink")
def test_a_test_directory_reached_through_a_symlink_does_not_move_the_rootdir(
    tmp_path,
):
    """#812's R3 with a tracked symlink in place of a generated file: the
    report names `gen/test_g.py` through the link `gen -> realgen`, which
    `git ls-files --cached --others` does not list, and `vendor` holds every
    report path, so `vendor` was taken for the rootdir and the root's
    failing `tests/test_two.py` was placed on `vendor/tests/test_two.py`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{SUITE_ROW} gen vendor",
        {
            "realgen/test_g.py": "def test_g():\n    pass\n",
            "tests/test_two.py": FAILING_TEST,
            "vendor/__init__.py": "",
            "vendor/gen/__init__.py": "",
            "vendor/gen/test_g.py": "X = 1\n",
            "vendor/tests/__init__.py": "",
            "vendor/tests/test_one.py": "X = 1\n",
            "vendor/tests/test_two.py": "X = 1\n",
        },
        {"tests/test_two.py": PASSING_TWO, "vendor/tests/test_two.py": FAILING_TWO},
    )
    # The link goes in on the base, and the feature merges it.
    git(repo, "switch", "-q", "base")
    os.symlink("realgen", repo / "gen")
    commit(repo, "the link")
    git(repo, "switch", "-q", "feature")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-edit",
        "base",
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "vendor/tests/test_two.py") == (
        gate_module().UNPLACED
    ), out.stdout
```

## Facts for the evidence ledger

- pytest 9.1.1 under `-o junit_family=xunit1` writes, for a test a module
  of the package `tests/test_api/` inherits from `tests/test_api.py`,
  `classname="tests.test_api.test_users.TestU"` beside
  `file="tests/test_api.py"`: the defining file's dotted form is a prefix of
  the collecting module's (executed, N1's kept report).
- pytest names a test it reached through a symlinked directory argument by
  the link's path (`gen/test_g.py`), and `git ls-files -z --cached
  --others` lists the link (`gen`) and the target's files
  (`realgen/test_g.py`), never the path through the link (executed, N3's
  kept report and listing).

Needs a fix: yes — 🔴 1 (a test a package's module inherits or imports from
the module the package is named like is placed on that module by its path,
so a failure the branch introduced reads `failing on base too`), 🔴 2 (a
test file reached through a symlink is missing from the listing, and a
mirror directory is taken for the rootdir).

Loses a record or crashes: no

This pass leaves two findings needing a fix, so the broad gate has not come
due. The run is capped; the orchestrator decides whether they are fixed
after review or filed.

## Proof block

Opened in this work item's directory: `rounds/round-3-report.md` in full,
and the 328d969f..fb698f90 diffs of `changelog.md`, `overview.md` and
`survivors.md`. Also opened:

- `skills/verify/scripts/broad_gate.py` lines 1790-2470 at fb698f90, the
  call site at 3532-3544, and the 328d969f..fb698f90 diff.
- `templates/config.md` rule 3, through the 328d969f..fb698f90 diff.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: lines 680-797,
  870-905, 3945-4030, 5340-5440, and the 328d969f..fb698f90 diff.
- The 328d969f..fb698f90 diff of
  `seal/ledger/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict.md`,
  its changed rows' text.
- `skills/verify/SKILL.md` lines 505-511, `bin/test`, and the head of
  `tests/conftest.py`.

Executed: the probes and module runs in *Executed probes*, in five `git
clone --no-local` copies of the worktree under this session's scratchpad,
with a uv venv holding pytest 9.1.1 and pytest-xdist 3.8.0, and the
repository's own `bin/test` for the narrow modules. The probe files, the
copies, the venv, the kept base temp and every output are deleted.

Unverified: the full suite, lint and typecheck, which the sealer answers
after the fixes land. Windows, and pytest 7 and 8 (the ❓ row). The
submodule and nested-repository members of 🔴 2 are read, not run.
