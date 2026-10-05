# Round 3 report — 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict

Target SHA: 56c8eb0d · Base: `release/v0.18.3` at a3aa139a · PR #804 (draft)
Ran by: specseal:warden on claude-opus-5-5

This is the verifying round over round 2's fixes (`562ab360..bf8669c2`, the
code in 9639f2ff and d31b5da3), and the last round this item gets: the run
is capped. What it finds is reported at the severity it is found, and is
fixed after review or filed.

## Summary

Every verdict round 2 recorded as closed is closed for the shapes it named.
Every probe of round 1 and round 2 (P1–P7, Q1–Q12) was re-run end to
end at the target, at a3aa139a, at 225af880 and at 8662f9bf. None of them
gives `failing on base too` at the target where the base gave a stricter
word. The smith's P7 measurement holds: in #761's p1b layout the target
reads `failing on base too`, as the base does.

The construction pass found three things still wrong. Two are permissive
words the base did not give, and the third is a rule-3 sentence that is
false.

- **🟡 1 — a placement by dotted name is never read against the tree.** An
  inherited test falls back to its dotted name, so does every test of a row
  that sets `--junit-prefix`, and that fallback still uses the old offset
  rule. P1's package and Q1's deeper module are then placed on a module the
  base holds no test in again: `failing on base too` at the target,
  `UNPLACED` at 8662f9bf and `new` at a3aa139a. 9639f2ff introduced it,
  because 8662f9bf kept `file` for every test.
- **🟡 2 — a test file the base does not track can move the rootdir.** The
  tree is `git ls-files`, so a test file the row generates is missing from
  it. A tracked directory that holds every report path under the same
  relative names is then taken for pytest's rootdir, and the root's failing
  test lands on the handed file under that directory: `failing on base too`
  at the target, `new` at a3aa139a. Rule 3 says such a run reads `new?`.
- **🟡 3 — "a file the base tracks under both runners' directories reads
  `new?`" is false for a run with more than one failing file.** The run
  directory is read over every handed file of the group. One file tracked
  under the measured runner's directory only is enough to decide it for the
  whole group. The word is the base's (`failing on base too` at both), and
  the sentence the fix pass added in four places promises otherwise.

A tested fix closes 🟡 1 and 🟡 2. It reads a dotted name against the tree
(`spelled`), and it lists the scratch worktree after the run with
`ls-files --cached --others`. With it, R1, R2, R2b and R3 read `UNPLACED`,
every other probe keeps its word, and the five narrow modules give
664 passed, 1 skipped. 🟡 3's fix is sentences only.

## Round 2's verdicts, answered

| Round 2 | Recorded | This round |
|---|---|---|
| 🟡 1 (Q1 deeper module, Q3 shorter path) | fixed `9639f2ff` | Closed for its shapes. Q1, Q3 and Q3b read `UNPLACED`; Q10 and Q11 keep `failing on base too`; Q10b reads `UNPLACED`. The class is closed by construction where every report path and every handed file is on the tree (below). R3 is the member where a report path is not, and it is 🟡 2 |
| 🟡 2 (inherited test, `file` is where it is defined) | fixed `9639f2ff` | Closed for Q4 (`UNPLACED`), Q4b (`new`) and Q4c (`failing on base too`). The fallback it introduced is 🟡 1 |
| 🟡 3 (rule 3 named two of four uncounted runners) | fixed `9639f2ff` | Closed. Rule 3, the `compare_at_base` docstring and the changelog name all four. Q8 now reads `UNPLACED`. The sentence added after the list is 🟡 3 |
| ⬜ 4 (two comments put the fixtures' rootdir at `tests`) | fixed `9639f2ff` | Closed. Both comments in `tests/test_the_seal_is_taken_once_by_the_sealer.py` now say the fixtures' rootdir is the repository root, and `phases/phase-1.md` carries the correction |
| ⬜ 5 (`--junitxml` included is not enough for a wrapper) | fixed `9639f2ff` | Closed. Rule 3 and the changelog say "`--junitxml` and `-o junit_family=…` included". Q12 reads `NO_RUNNER` |
| ⬜ 6 (`overview.md` Not done) | answered | Rewritten. Two of its new bullets are false at the target (⬜ 5 below) |
| 🟢 rows (P3 `MULTI_RUNNER`, P5 cost, P4 reason, counting, green run) | confirmed | Re-derived. P3 `sh -c` and Qs2 read `MULTI_RUNNER (3, 1)`. P5 runs A twice and B once (`AAB`). Q7 and Qf keep their words. A green gate does not reach `compare_at_base` (below) |
| ❓ Windows, pytest 7 and 8 | out of verified scope | Still read only, on macOS with pytest 9.1.1 |

## The smith's divergence

Rule 3 used to say a runner the collection pass cannot count reads
"never `failing on base too`". The fix pass changed it to "a file the base
tracks under both runners' directories reads `new?`, and one it tracks under
the measured runner's directory only is measured there, so it can read
`new` or `failing on base too` from the wrong runner."

- **The measurement holds.** P7-p1b (`{SUITE_ROW} && sh -c 'cd sub &&
  {SUITE_ROW}'` over #761's `TWO_RUNNERS_AT_BASE`) gives `tests/test_y.py`
  `failing on base too` at all four SHAs. P7-both, where the base also
  tracks `sub/tests/test_y.py`, gives `UNPLACED` at the target and
  `failing on base too` at the other three. Round 2's P7 row was this
  layout.
- **The sentence does not hold.** `report_words` computes the run directory
  over every handed file of the group. P7-mixed adds `tests/test_w.py`,
  which the base tracks at the root only, to P7-both's run. `heres` is then
  the root alone, and `tests/test_y.py`, which the base tracks under both
  directories, reads `failing on base too` at the target and the base.
  This is 🟡 3.

## Findings from execution

### 🟡 1 — a dotted name is still placed by offset, so an inherited test or a `--junit-prefix` row reopens P1 and Q1

`skills/verify/scripts/broad_gate.py:1952` (`report_cases`, the prefix
check) and `:2113-2116` (`report_words`, the branch for an inexact
address). `report_cases` keeps `file` only where the classname starts with
it. Two report shapes fail that check for every test of a kind:

- An inherited test. Its `file` is the parent class's module.
- Every test under `--junit-prefix=pfx`, from the row or the ini file's
  `addopts`. The classname is `pfx.tests.test_api.test_users` and the file
  is `tests/test_api/test_users.py`. Executed against a real pytest 9.1.1
  report: every case came back with exact false.

Such a case is placed with the offset rule and the `shared` guard, which
never read the tree. Round 1's P1 and round 2's Q1 are the shapes that
guard does not stop, so they come back. Executed end to end:

| Probe | Layout | 56c8eb0d | a3aa139a | 8662f9bf |
|---|---|---|---|---|
| R1 | P1 with `--junit-prefix=pfx` in the row | `failing on base too` | `new` | `UNPLACED` |
| R1-ini | P1 with the prefix in `pytest.ini`'s `addopts` | `failing on base too` | `new` | `UNPLACED` |
| R2 | P1, the package's failing test inherited from `tests/test_api/helpers.py` | `failing on base too` | `new` | `UNPLACED` |
| R2b | Q1, the deeper failing test inherited from `tests/x/tests/helpers.py` | `failing on base too` | `new` | `UNPLACED` |

**Regression against the base.** In every row the base gives `new`, and the
regression is 9639f2ff's. 8662f9bf kept `file` for every test and read
`UNPLACED`.

**Why it matters.** `failing on base too` is the one word that lets a red
suite through. Two things are enough to reach it. One is a shared base
class in a test package that sits beside a same-named module. The other is
any repository whose CI sets `--junit-prefix`. Rule 3 names the inherited
half as a limit ("which cannot tell a module from a package of the same
name"). The changelog says the opposite ("so a package or a class named
like a module is never taken for it"). `--junit-prefix` is named nowhere,
and `overview.md` says every pytest writes `file`.

**The fix reads the dotted name against the same tree.** The leading
components of the dotted name spell a candidate module at each length:
`tests/test_api.py`, then `tests/test_api/test_users.py`. Where exactly one
is a file under the rootdirs, the case becomes exact with that path. Where
two are files (a module and a package of the same name) or none is (a
`--junit-prefix`), it places nothing. Q4b, Q4 and Q4c keep `new`,
`UNPLACED` and `failing on base too`, and R1 to R2b read `UNPLACED`. The
diff is under *Paste-ready fixes*.

### 🟡 2 — a test file the row generates is missing from the tree, and another directory is taken for the rootdir

`skills/verify/scripts/broad_gate.py:2357` (`tree` is `git ls-files` of the
scratch worktree, read before any run), with `directories_holding`
(`:2011-2029`) and the placement at `:2105-2112`. A unique placement is
right only when the true rootdir is among `roots`. That holds only where
every path in the report is on the tree. A file the row writes at run time
is not on it.

Executed (R3). At the base the row is `python gen.py && {SUITE_ROW} gen
vendor`. `gen.py` writes `gen/test_g.py`, which `.gitignore` excludes. The
base tracks `tests/test_two.py` (failing) and a vendored copy
`vendor/tests/test_one.py`, `vendor/tests/test_two.py` (no test) and
`vendor/gen/test_g.py`. The branch fails `vendor/tests/test_two.py`. The
report names `tests/test_one.py`, `tests/test_two.py` and `gen/test_g.py`.
`vendor` is the only tracked directory holding all three, so `roots` is
`{vendor}`. The handed file's `heres` is the root. `tests/test_two.py`
then joins to `vendor/tests/test_two.py`, which is exactly `here`.

| Probe | 56c8eb0d | a3aa139a | 225af880 | 8662f9bf |
|---|---|---|---|---|
| R3 `vendor/tests/test_two.py` | `failing on base too` | `new` | `failing on base too` | `failing on base too` |

**Regression against the base.** a3aa139a gave `new`, and the offset
readings since 225af880 give the same wrong word. Rule 3 (and `overview.md`
§*Not done*) state the opposite: "and so does every file of a run whose
report names a test file the base does not track" reads `new?`.

**Why it matters, and how far it reaches.** All of these must hold at once.
The row generates a test file. The base tracks a directory holding every
report path under the same relative names. The handed file sits under that
directory. That is narrow. The sentence a row's author reads, however,
promises the strict word, so the defect is in what ships either way.

**The fix lists the files after the run.** It runs `git ls-files -z
--cached --others` in the scratch worktree after each run whose report is
read. With no exclude option, git lists ignored files too (executed). Every
file pytest named is then present, so the true rootdir is always among
`roots`, and a unique placement is the right one. R3 then reads `UNPLACED`
(`roots` is the root and `vendor`), and nothing else this round ran
changes word. This makes rule 3's "a test file the base does not track"
sentence unnecessary; the paste-ready text drops it.

### 🟡 3 — "a file the base tracks under both runners' directories reads `new?`" holds only where every failing file of its run does

`templates/config.md:333` (two sentences: the collection-alone one and the
four-shapes one), `skills/verify/scripts/broad_gate.py:2329-2334` (the
`compare_at_base` docstring), `changelog.md`'s last bullet, and
`overview.md` §*Not done*. The pin in
`test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`
holds the rule-3 text.

`heres` is one set for the whole group: the directories under which every
handed file is tracked. Executed, P7-mixed. The row is P7's. The base
tracks `tests/test_y.py` (failing) and `sub/tests/test_y.py` (passing), and
`tests/test_w.py` at the root only. The branch fails both in `sub`.
`tests/test_y.py` reads `failing on base too` at all four SHAs, from the
root runner.

**Regression against the base.** No, the word is the base's. What is new is
the sentence, written by the round 2 fix pass in four places, which
promises `new?` for this file.

**Why it matters.** Rule 3 is where a row's author learns which rows they
can trust, and it says this one is safe. The fix is a sentence: the word is
`new?` only where the base tracks every failing file of the run under both
directories.

## Findings from reading

- **⬜ 4 — the `UNPLACED` reason does not name the tree's outcomes.**
  `skills/verify/scripts/broad_gate.py:1897-1901`. The parenthetical says
  "it names none of this file's tests, or a failing test it names could be
  this file or another one". Q10b, where a second directory fits the run,
  reads that reason while the report names the file's test. The headline,
  "does not place a test on this file alone", stays true, and the word is
  the strict one, so this is ⬜.
- **⬜ 5 — `overview.md` §*Not done* has two bullets the target makes
  false.** "Every pytest the fix passes ran writes `file`" is true, but
  under `--junit-prefix` the target drops it (🟡 1). "A test file the base
  does not track … makes every file of that run read `new?`" does not hold
  (🟡 2, R3). This is a correction to this work item's paperwork and is not
  counted in Needs a fix.
- **Outside this change, noted only.** A failing file whose path holds a
  space is not compared at all, at every SHA including a3aa139a. That is
  R4's `tests/sp ace/test_sp.py`. `FAILED_RE` (`\S+?`) stops at the space,
  so `failing_files` does not name the file. The gate stays red, which is
  the strict direction. A non-ASCII name (`tests/test_é.py`) is compared and
  reads `failing on base too` everywhere.

## The tree reading, by construction

The question is whether a placement can give a word stricter-than-base
`new` turns into `failing on base too`. Let R be pytest's true rootdir and H
the directory the row ran pytest in. A placement on `f` needs `tests` and
`here` to be singletons and equal.

- If every report path is on the tree and every handed file is on the tree
  under H, then H is in `heres`. A singleton `heres` is therefore {H}, and
  `D/address = H/f` for the one root D forces D = R. A unique placement is
  then the right file. This is why every P and Q probe is safe at the
  target.
- A report path off the tree removes R from `roots` (🟡 2).
- A dotted address never meets the tree (🟡 1).
- A handed file off the tree under H removes H from `heres`. A handed file
  pytest ran exists, so this takes a generated handed file. 🟡 2's fix
  covers it too.

| Axis | What `ls-files` lists | Result at the target |
|---|---|---|
| rootdir at the run directory, below it, above it (Q3, Q3b, Q10, Q11) | — | right word or `UNPLACED`, executed |
| a tracked test file / a generated one (R3) | the generated one is absent | 🟡 2 |
| a file tracked under both, one or neither runner directory (P7-both, P7-p1b, P7-mixed, P7's `test_x`) | — | `UNPLACED` / the base's word / 🟡 3's sentence / `new` from the lone run |
| a package and a module of one name (P1, Q5, R2) | both | `UNPLACED` by path; 🟡 1 by dotted name |
| the repository root against the scratch root | `repo_root` takes `--show-toplevel`, so both are the top | no case |
| a space and a non-ASCII name | `-z` output, decoded as UTF-8 | `é` compared right; a space is never compared (noted above) |
| a submodule | one gitlink entry, no file under it, and `worktree add` leaves it empty (executed) | the base has no test there; a candidate run alone reads `new` |
| a sparse checkout | every index entry, including files not on disk; a new worktree inherits the sparse patterns (executed, git 2.54) | extra directories only ever add candidates, so they can only make the word stricter |

## The `file` check against parametrized ids, nested classes and doctests

Executed against real pytest 9.1.1 `xunit1` reports, through
`report_cases` at the target. Every case below came back exact:

- `TestA::TestB::test_nested`;
- parametrized ids `a.b/c`, `d::e` and `[x]`;
- a `--doctest-modules` item;
- a `--doctest-glob` text file under `docs/v1.2/`;
- a test module under a dotted directory `tests/v1.2/`;
- a collection error.

pytest's `mangle_test_address` keeps a parameter out of the classname, and
`dotted` splits a dotted directory the way the classname does. End to end
(R5), the same module reads `failing on base too` at every SHA.

A test file outside the rootdir gets `file="../tests/…"` and a classname of
its bare stem, so it falls back to its dotted name: `UNPLACED` or the
strict side.

## Every shape any round ran

Each of these was run end to end this round, at the four SHAs and with the
fix. The table under *Executed probes* has every word.

| Shapes | Target permissive where a3aa139a was not? |
|---|---|
| P1, P2, P3 (both), P4 (both), P5, P6, P7 (p1b, both, mixed) | no |
| Q1, Q2, Q3, Q3b, Q4, Q4b, Q4c, Q5, Q7, Q8, Q10, Q10b, Q11, Q12, Qf (row, env, ini), Qs, Qs2 | no |
| R1, R1-ini, R2, R2b | **yes** (🟡 1) |
| R3 | **yes** (🟡 2) |
| R4, R5, R6 | no |

The spec's S1–S11 cases and every earlier pin are in the five narrow
modules, which give 664 passed, 1 skipped at the target and with the fix
(executed). Q2 and Q3b are rebuilt from their one-line names, because
round 2 recorded neither layout. Q3b is pytest's rootdir in `a` (its ini)
and a handed `a/b/tests/test_two.py`. Q2 is `--rootdir=sub sub/tests`. This
Q2 is not round 2's, whose `FAILED` line named a file that does not exist,
and here every SHA reads `failing on base too`.

## Rule 3, the SKILL.md bullet, the reasons and the changelog against the code

| Text | Against the code |
|---|---|
| Rule 3: placement "read against the files the base tracks … each is one directory and the two name one file" | Matches `report_words`. Strictly, the two joined path sets must be singletons, which is the same thing for paths with no `..` |
| Rule 3: "and so does every file of a run whose report names a test file the base does not track" | False (R3, 🟡 2) |
| Rule 3: an inherited test "is placed by its dotted name instead, which cannot tell a module from a package" | True, and the consequence is a permissive word (🟡 1). `--junit-prefix` is not named |
| Rule 3 and the docstring: four uncounted runners | True; Q8, P3 `-p no:junitxml` and P7 measured |
| Rule 3, the docstring and the changelog: "a file the base tracks under both runners' directories reads `new?`" | False for a mixed group (🟡 3) |
| Rule 3: "`--junitxml` and `-o junit_family=…` included" | True (Q12) |
| `skills/verify/SKILL.md`, the **New?** bullet | True. Every outcome the tree reading adds is "that report did not place a test on the file alone" |
| The `UNPLACED` reason | ⬜ 4 |
| The changelog: "so a package or a class named like a module is never taken for it" | False for a dotted placement (🟡 1) |
| `JUNIT_FAMILY`'s comment and `report_cases`' docstring | True of the code |

## The seal

A green run is unchanged. `compare_at_base`, and so the new `ls-files`, is
called only from the suite arm, only when that arm failed and named failing
files (`skills/verify/scripts/broad_gate.py:3561-3564`, read). R3's first,
mis-built layout gave a green gate at the target: `SEALED … nothing was
recorded`, executed. 🟡 2's fix moves the `ls-files` call into the loop, so
a failing gate pays one more git call per prefix it reads a report from.
That is still only on a failing gate.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A dotted-name placement is never read against the tree. An inherited test, and every test under `--junit-prefix`, falls back to the offset rule, and P1's package and Q1's deeper module are placed on a module the base holds no test in. A regression against a3aa139a, introduced by 9639f2ff | `skills/verify/scripts/broad_gate.py:1952`, `skills/verify/scripts/broad_gate.py:2113-2116` | open | Executed R1, R1-ini, R2, R2b: `failing on base too` at 56c8eb0d, `new` at a3aa139a, `UNPLACED` at 8662f9bf and with the fix |
| 🟡 2 | The tree is the base's tracked files, so a test file the row generates is missing and a vendored directory holding every report path is taken for the rootdir. The root's failing test is placed on the handed file. A regression against a3aa139a, and rule 3 promises `new?` | `skills/verify/scripts/broad_gate.py:2357`, `skills/verify/scripts/broad_gate.py:2011-2029`, `templates/config.md:333` | open | Executed R3: `failing on base too` at 56c8eb0d, 225af880 and 8662f9bf, `new` at a3aa139a, `UNPLACED` with the fix |
| 🟡 3 | "A file the base tracks under both runners' directories reads `new?`" is false where another failing file of its run is tracked under the measured runner's directory only. The word is the base's; the sentence is new, in four places and a pin | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2329-2334`, `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/changelog.md` | open | Executed P7-mixed: `tests/test_y.py` `failing on base too` at all four SHAs |
| ⬜ 4 | The `UNPLACED` reason's parenthetical does not name a second directory that fits the run, which the tree reading added | `skills/verify/scripts/broad_gate.py:1897-1901` | open | Read; Q10b reads the reason while the report names the file's test |
| ⬜ 5 | `overview.md` §*Not done* says every pytest writes `file` and that an untracked test file makes the run read `new?`; the target drops `file` under `--junit-prefix`, and R3 reads `failing on base too` | `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/overview.md` | open | A correction to this run's paperwork, not counted in Needs a fix |
| 🟢 | round 2's first finding is closed — Q1, Q3 and Q3b are not placed on the handed file, and Q10 and Q11 keep their words | `skills/verify/scripts/broad_gate.py:2003-2029`, `skills/verify/scripts/broad_gate.py:2099-2112` | confirmed | Executed Q1, Q3, Q3b `UNPLACED`; Q10, Q11 `failing on base too`; Q10b `UNPLACED` |
| 🟢 | round 2's second finding is closed — an inherited test is not placed on the defining file | `skills/verify/scripts/broad_gate.py:1945-1955` | confirmed | Executed Q4 `UNPLACED`, Q4b `new`, Q4c `failing on base too` |
| 🟢 | round 2's third finding is closed — the four uncounted runners are named in rule 3, the docstring and the changelog | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2321-2329` | confirmed | Read; Q8 executed, `UNPLACED` |
| 🟢 | round 2's fourth and fifth findings are closed — the fixture comments and the wrapper sentence | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4142`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:4275`, `templates/config.md:333` | confirmed | Read; Q12 executed, `NO_RUNNER` |
| 🟢 | The smith's measured divergence: P7 in #761's p1b layout reads `failing on base too`, as the base does | `templates/config.md:333` | confirmed | Executed P7-p1b at four SHAs; the sentence built on it is 🟡 3 |
| 🟢 | The `file` check holds for nested classes, parametrized ids, doctest modules and text files, dotted directories and collection errors | `skills/verify/scripts/broad_gate.py:1945-1955` | confirmed | Executed against real `xunit1` reports, and R5 end to end |
| 🟢 | A green run is unchanged | `skills/verify/scripts/broad_gate.py:3561-3564` | confirmed | Read; a green gate at the target executed |
| 🟢 | round 2's confirmed rows still hold — P3 `MULTI_RUNNER`, P5's cost, P4's reason, the counting change | `skills/verify/scripts/broad_gate.py:2402-2441` | confirmed | Executed P3, P4, P5, Q7, Qf, Qs2 |
| ❓ | Windows (backslash `file`, `cmd.exe` quoting, `shlex.quote` in `PYTEST_ADDOPTS`) and the `file` attribute on pytest 7 and 8 | `skills/verify/scripts/broad_gate.py:1870-1880` | ❓ out of verified scope | Read only, on macOS with pytest 9.1.1. CI's three-platform job answers Windows; the repository owner answers pytest 7 and 8 |

## Executed probes

| What was run | Result |
|---|---|
| P1–P7 and Q1–Q12 end to end through the gate, in four `git clone --no-local` copies at 56c8eb0d holding the gate of 56c8eb0d, a3aa139a, 225af880 and 8662f9bf, on one probe file built on the module's helpers | All probe cases ran at each SHA (exit 0). The words are in the table below |
| This round's shapes R1–R6 and P7-mixed at the same four SHAs | The table below |
| A fifth copy with the fix below applied, every probe rerun | The last column of the table |
| The four regression cases and three tree rows below, at the target and with the fix | 5 failed at 56c8eb0d (each `'failing on base too' == UNPLACED`), 6 passed with the fix |
| `bin/test`'s five modules (`test_the_seal_is_taken_once_by_the_sealer.py`, `test_the_gate_hands_cmd_a_path_it_can_run.py`, `test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, `test_release_hygiene.py`, `test_a_record_states_what_the_tree_has.py`), run with the copy's venv and `-n 8` | 664 passed, 1 skipped (exit 0) at 56c8eb0d and the same with the fix |
| `report_cases` over real pytest 9.1.1 `xunit1` reports: nested classes, parametrized ids, doctests, `--junit-prefix`, a collection error, a test outside the rootdir | every case exact except `--junit-prefix` (all) and the outside test |
| `git ls-files` with a submodule, under a sparse checkout, and in a worktree added from it; `ls-files --cached --others` with an ignored file | gitlink only; every index entry; patterns inherited; ignored file listed |
| `uvx ruff check` and `uvx ruff format --check` on the target's two touched modules, and on the fixed gate | clean |
| The broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

```
probe / file                                56c8eb0d              a3aa139a              225af880              8662f9bf              with the fix
P1 tests/test_api.py                        UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
P2 tests/test_two.py                        UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
P3-nojunit tests/test_two.py                UNPLACED              new                   failing on base too   failing on base too   UNPLACED
P3-sh tests/test_two.py                     MULTI_RUNNER (3, 1)   new                   failing on base too   MULTI_RUNNER (3, 1)   MULTI_RUNNER (3, 1)
P4-files tests/test_two.py                  NOTHING_TOGETHER      NO_RUNNER             NOTHING_TOGETHER      NOTHING_TOGETHER      NOTHING_TOGETHER
P4-suite tests/test_two.py                  UNPLACED              new                   UNPLACED              UNPLACED              UNPLACED
P5 tests/test_two.py                        failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P5 marker (parts after the runner)          AAB                   (nothing)             AAB                   AAB                   AAB
P6 tests/test_two.py                        failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P7-both tests/test_x.py                     new                   new                   new                   new                   new
P7-both tests/test_y.py                     UNPLACED              failing on base too   failing on base too   failing on base too   UNPLACED
P7-both tests/test_z.py                     UNPLACED              new                   new                   new                   UNPLACED
P7-mixed tests/test_y.py                    failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P7-mixed tests/test_w.py                    new                   new                   new                   new                   new
P7-p1b tests/test_x.py                      new                   new                   new                   new                   new
P7-p1b tests/test_y.py                      failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P7-p1b tests/test_z.py                      new                   new                   new                   new                   new
Q1 tests/test_two.py                        UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q2 sub/tests/test_two.py                    failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q3 a/tests/test_two.py                      UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q3b a/b/tests/test_two.py                   UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q4 tests/test_two.py                        UNPLACED              new                   UNPLACED              failing on base too   UNPLACED
Q4b tests/test_two.py                       new                   new                   new                   failing on base too   new
Q4c tests/test_two.py                       failing on base too   failing on base too   failing on base too   new                   failing on base too
Q5 tests/test_api.py (-n 2)                 UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Q7 tests/test_two.py                        failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q8 tests/test_two.py                        UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q10 tests/test_two.py                       failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q10b tests/test_two.py                      UNPLACED              failing on base too   failing on base too   failing on base too   UNPLACED
Q11 sub/tests/test_two.py                   failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q12 tests/test_two.py                       NO_RUNNER             failing on base too   failing on base too   NO_RUNNER             NO_RUNNER
Qf-row tests/test_api.py                    UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Qf-env tests/test_api.py                    UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Qf-ini tests/test_api.py                    UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Qs tests/test_two.py (-rN preset)           no comparison         no comparison         no comparison         no comparison         no comparison
Qs2 tests/test_two.py                       MULTI_RUNNER (3, 1)   new                   failing on base too   MULTI_RUNNER (3, 1)   MULTI_RUNNER (3, 1)
R1-prefix tests/test_api.py                 failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R1-prefix-ini tests/test_api.py             failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R2-inherited-package tests/test_api.py      failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R2b-inherited-deeper tests/test_two.py      failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R3-generated vendor/tests/test_two.py       failing on base too   new                   failing on base too   failing on base too   UNPLACED
R4 tests/sp ace/test_sp.py                  not compared          not compared          not compared          not compared          not compared
R4 tests/test_é.py                          failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
R5 nested, parametrized, doctest            failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
R6 inherited and own failing test           failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
```

The five narrow modules at 56c8eb0d, in the target's own copy: 664 passed,
1 skipped (exit 0), the same count as with the fix. The prompt's 726 passed
included three hygiene modules this round did not run; that figure is the
orchestrator's and was not reproduced here.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A failing file whose path holds a space is never compared at the base: `FAILED_RE` stops at the space, at every SHA including a3aa139a. Strict, outside this change | a new issue | the orchestrator, who files issues |

## Paste-ready fixes

### 🟡 1 and 🟡 2 — read a dotted name against the tree, and the tree after the run

Applied together in the fifth copy. The five narrow modules gave 664
passed, 1 skipped; every probe kept its word except R1, R1-ini, R2, R2b
and R3, which read `UNPLACED`. `ruff check` and `ruff format --check` are
clean.

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ -2029,6 +2029,20 @@ def directories_holding(addresses, tree):
     return found
 
 
+def spelled(name, roots, tree):
+    """The one module the leading components of the dotted name `name` spell
+    as a file the base tracks under one of `roots`, split at `/`, or None
+    where they spell none or more than one (#789 round 3). A module and a
+    package of the same name are both tracked, which is the case a dotted
+    name alone could not tell apart."""
+    found = set()
+    for k in range(1, len(name) + 1):
+        address = (*name[: k - 1], f"{name[k - 1]}.py")
+        if any(joined(d, address) in tree for d in roots):
+            found.add(address)
+    return found.pop() if len(found) == 1 else None
+
+
 def report_words(text, files, code, stopped, alone=False, tree=None):
@@ -2099,8 +2113,20 @@ def report_words(text, files, code, stopped, alone=False, tree=None):
     if tree is not None:
         roots = directories_holding({a for a, _, e in cases if e}, tree)
         heres = directories_holding({paths[f][True] for f in files}, tree)
+        # A dotted name — an inherited test, or every test under a
+        # `--junit-prefix` — is read against the tree too: the one module it
+        # spells becomes its path, and one that spells none or more than one
+        # places nothing (#789 round 3).
+        cases = [
+            (address, failed, True)
+            if exact
+            else (spelled(address, roots, tree), failed, True)
+            for address, failed, exact in cases
+        ]
     for address, failed, exact in cases:
         hit = set()
+        if address is None:
+            continue
         for f in files:
             if exact and tree is not None:
                 tests = {joined(d, address) for d in roots}
@@ -2352,9 +2378,6 @@ def compare_at_base(root, base, command, files, keep):
             f for f in files if git(scratch, "cat-file", "-e", f"HEAD:{f}") is None
         ]
         others = [f for f in files if f not in candidates]
-        # The base's tracked paths, which a report's `file` is read against
-        # (`report_words`, #789 round 2's 🟡 1).
-        tree = frozenset((git(scratch, "ls-files", "-z") or "").split("\0")) - {""}
         # One group of every other file, kept as `suite-at-base-<k>.txt`, then
@@ -2413,6 +2436,13 @@ def compare_at_base(root, base, command, files, keep):
                         second = k
                         break
                     continue
+                # The base's files after this run, tracked or not, which a
+                # report's `file` is read against (`report_words`): a test
+                # file the row generated is one pytest named, so its rootdir
+                # is among the directories holding every report path (#789
+                # round 3).
+                listed = git(scratch, "ls-files", "-z", "--cached", "--others")
+                tree = frozenset((listed or "").split("\0")) - {""}
                 words = report_words(
```

The rule-3 sentences from "A test is placed on a file by the path" to "a
module from a package of the same name." become the following. The pin in
`test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`
takes the same text.

```
A test is placed on a file by the path pytest's report gives it (the gate also appends `-o junit_family=xunit1`, which writes that path), read against the files in the base's worktree after the run, tracked or written by the run: pytest's rootdir is a directory under which every such path is a file, the directory the row runs pytest in is one under which every file the run was handed is, and the test is placed on the file only where each is one directory and the two name one file. Where a second directory fits either, the file reads `new?`. That path is the file a test's function is defined in, so a test a class inherits from another module, and every test of a run under `--junit-prefix`, is placed by its dotted name instead, read against the same files: the one module the name spells is its file, and a name that spells both a module and a package of the same name, or no file, places nothing.
```

The changelog's sentences from "by the file's path read against the files
the base tracks" to "on the module that collected it." become:

```
  A file reads `failing on base too` only where the report places a failing
  or erroring test on that file and no other, by the file's path read
  against the files in the base's worktree after the run, tracked or written
  by the run. The gate also appends `-o junit_family=xunit1`, which makes
  pytest write each test's file as a path, so a package or a class named
  like a module is never taken for it. Where a same-named file the path
  could also name sits under another rootdir or another directory the row
  could run pytest in, the file reads `new?`. That path is where a test's
  function is defined, so a test a class inherits from another module, and
  every test under `--junit-prefix`, is placed by its dotted name instead,
  read against the same files: a name that spells both a module and a
  package of the same name places nothing.
```

### 🟡 3 — the both-directories sentence, said of the run

In rule 3, the collection-alone sentence's tail, from "such a row is read
as one with a single runner: a file a later runner named reads `new?`" to
"where the base tracks it there only.", becomes:

```
such a row is read as one with a single runner: where the base tracks every failing file of a run under both runners' directories, each reads `new?`, and where it tracks any one of them under the first runner's directory only, every file of that run is measured there and can read `new` or `failing on base too` from the first runner's directory.
```

The sentence after the four uncounted shapes, from "Such a row is read as
one with a single runner: a file the base tracks" to "from the wrong
runner.", becomes:

```
Such a row is read as one with a single runner: where the base tracks every failing file of a run under both runners' directories, each reads `new?`, and where it tracks any one of them under the measured runner's directory only, every file of that run is measured there, so each can read `new` or `failing on base too` from the wrong runner.
```

The `compare_at_base` docstring, from "A file the base tracks under both
runners' directories reads `new?`" to "which is #761's p1b.":

```
    Such a row is read as one with a single runner. Where the base tracks
    every failing file of a run under both runners' directories, each reads
    `new?`, because `report_words` reads the run directory off every handed
    file (#789 round 2); where it tracks any one of them under the measured
    runner's directory only, every file of that run is measured there, and
    can read `new` or `failing on base too` from the wrong runner, which is
    #761's p1b.
```

The changelog's last two sentences become:

```
  In such a row, where the base tracks every failing file of a run under
  both runners' directories, each reads `new?`. Where it tracks any one of
  them under the measured runner's directory only, every file of that run
  is measured there, and can read `new` or `failing on base too` from the
  wrong runner.
```

### ⬜ 4 — the `UNPLACED` reason

```
UNPLACED = (
    f"{NOT_MEASURED}: pytest's report at the base does not place a test on "
    "this file alone (it names none of this file's tests, a failing test it "
    "names could be this file or another one, or a second directory of the "
    "base fits the run)"
)
```

The reason is pinned in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it`, which takes
the same text.

## Regression tests to plant

Destination: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, after
round 2's cases. The three tree rows can instead join `TREE_READINGS`. Each
was run as written: 5 failed at 56c8eb0d and 6 passed with the fix. The
third row is green on both and pins the word the fix must keep. With
`spelled` reverted, the two dotted rows and the two dotted end-to-end cases
go red; with the `ls-files` move reverted, the generated-file case goes red.

```python
DOTTED_READINGS = [
    pytest.param(
        junit(
            [
                (
                    "tests.test_api.test_users.TestU",
                    "test_inherited",
                    "failure",
                    "tests/test_api/helpers.py",
                )
            ]
        ),
        {"tests/test_api.py", "tests/test_api/helpers.py", "tests/test_api/test_users.py"},
        ["UNPLACED"],
        id="an-inherited-test-of-a-package-named-like-the-module",
    ),
    pytest.param(
        junit(
            [
                (
                    "pfx.tests.test_api.test_users",
                    "test_u",
                    "failure",
                    "tests/test_api/test_users.py",
                )
            ]
        ),
        {"tests/test_api.py", "tests/test_api/test_users.py"},
        ["UNPLACED"],
        id="a-junit-prefix",
    ),
    pytest.param(
        junit(
            [
                ("tests.test_api.TestA", "test_shared", "failure", "tests/helpers.py"),
                ("tests.test_api", "test_own", "", "tests/test_api.py"),
            ]
        ),
        {"tests/test_api.py", "tests/helpers.py"},
        ["ON_BASE"],
        id="an-inherited-test-the-tree-spells-once",
    ),
]


@pytest.mark.parametrize("report, tree, words", DOTTED_READINGS)
def test_a_dotted_name_is_read_against_the_bases_tracked_files(report, tree, words):
    """#789 round 3's 🟡 1. An inherited test and a `--junit-prefix` report
    are placed by the dotted name, read against the tree: one spelled module
    places, two (a module and a package of one name) or none place nothing."""
    gate = gate_module()
    expected = [getattr(gate, w) for w in words]
    got = gate.report_words(report, ["tests/test_api.py"], 1, False, tree=frozenset(tree))
    assert list(got.values()) == expected


P1_BASE = {
    "tests/test_api.py": "X = 1\n",
    "tests/test_api/test_users.py": FAILING_TEST.replace("test_two", "test_u"),
}
P1_FEAT = {
    "tests/test_api.py": FAILING_TWO,
    "tests/test_api/test_users.py": PASSING_TEST.replace("test_one", "test_u"),
}


def test_a_junit_prefix_does_not_place_a_package_on_the_module(tmp_path):
    """#789 round 3's 🟡 1 (R1). Under `--junit-prefix` no classname starts
    with its file, so every test fell back to its dotted name and P1's
    package was placed on `tests/test_api.py`."""
    repo = base_then_feature(
        tmp_path / "repo", f"{SUITE_ROW} --junit-prefix=pfx", P1_BASE, P1_FEAT
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_api.py") == gate_module().UNPLACED, (
        out.stdout
    )


def test_an_inherited_test_of_a_package_is_not_placed_on_the_module(tmp_path):
    """#789 round 3's 🟡 1 (R2). The failing test is inherited from
    `tests/test_api/helpers.py`, so it was placed by its dotted name
    `tests.test_api.test_users.TestU`, which also spells `tests/test_api.py`."""
    helper = (
        "class Base:\n    v = 1\n\n    def test_inherited(self):\n"
        "        assert self.v == 1, 'planted'\n"
    )
    users = "from helpers import Base\n\n\nclass TestU(Base):\n    v = {}\n"
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW,
        {
            "tests/test_api.py": "X = 1\n",
            "tests/test_api/helpers.py": helper,
            "tests/test_api/test_users.py": users.format(2),
        },
        {"tests/test_api.py": FAILING_TWO, "tests/test_api/test_users.py": users.format(1)},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_api.py") == gate_module().UNPLACED, (
        out.stdout
    )


GEN = (
    "import os\n"
    "os.makedirs('gen', exist_ok=True)\n"
    "open('gen/test_g.py', 'w').write('def test_g():\\n    pass\\n')\n"
)


def test_a_generated_test_file_does_not_move_the_rootdir(tmp_path):
    """#789 round 3's 🟡 2 (R3). The row generates `gen/test_g.py`, which the
    base does not track, and `vendor` tracks every path of the report, so
    `vendor` was taken for the rootdir and the root's failing
    `tests/test_two.py` was placed on `vendor/tests/test_two.py`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{sys.executable} gen.py && {SUITE_ROW} gen vendor",
        {
            ".gitignore": "/gen/\n",
            "gen.py": GEN,
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
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "vendor/tests/test_two.py") == (
        gate_module().UNPLACED
    ), out.stdout
```

P7-mixed is not planted: 🟡 3's fix is a sentence, and the word it states
is the base's. If the fix pass wants it pinned, P7's row over P7-both's
layout plus a root-only `tests/test_w.py` that the branch fails in `sub`
gives `tests/test_y.py` `failing on base too`.

## Facts for the evidence ledger

- pytest 9.1.1 under `--junit-prefix=pfx` writes `classname="pfx.tests…"`
  beside `file="tests/…"`, so no classname starts with its file (executed).
- A test file outside pytest's rootdir is written as
  `file="../tests/test_out.py"` with a classname of its bare stem (executed).
- `git ls-files` lists a submodule as one gitlink path and lists
  skip-worktree entries of a sparse checkout. A worktree added from a
  sparse checkout inherits its patterns. `ls-files --cached --others`, with
  no exclude option, lists ignored files (all executed, git 2.54).

Needs a fix: yes — 🟡 1 (a dotted-name placement is never read against the
tree: an inherited test or a `--junit-prefix` row reopens P1 and Q1), 🟡 2
(a test file the row generates moves the rootdir to a vendored directory),
🟡 3 (rule 3, the docstring and the changelog promise `new?` for a file
tracked under both runners' directories, which holds only where every
failing file of its run is).

Loses a record or crashes: no

This round leaves three findings needing a fix, so the broad gate has not
come due. The run is capped: they go to the post-review fix or are filed.

## Proof block

Opened this round, in this work item's directory: `rounds/round-1-report.md`
(lines 80-215), `rounds/round-2.md`, `rounds/round-2-report.md`,
`overview.md` lines 1-69, `changelog.md`, and the 8662f9bf..56c8eb0d diffs
of `phases/phase-1.md` and `survivors.md`. Also opened:

- `seal/ledger/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict.md`,
  lines 1-40.
- `skills/verify/scripts/broad_gate.py`: lines 1860-2469 at the target, the
  `git` helper (357-366), the `--root` lines (3397, 3874), the call site
  (3540-3575), and the 8662f9bf..56c8eb0d diff.
- The a3aa139a..56c8eb0d diff of `skills/verify/SKILL.md`.
- The 8662f9bf..56c8eb0d diffs of `templates/config.md` and
  `tests/test_the_seal_is_taken_once_by_the_sealer.py`.
- In that test module: lines 680-915, 3950-4030, 4790-4810 and 5270-5432.
- `bin/test`. `seal/config.md` (no `Record language` row).

Executed: the probes and module runs in *Executed probes*, in
`git clone --no-local` copies of the worktree at 56c8eb0d under this
session's scratchpad, with a uv venv holding pytest 9.1.1 and pytest-xdist
3.8.0. The probe files, the five copies, the venv, the git and report
scratch projects and every output are deleted.

Unverified: the full suite, lint and typecheck, which the sealer answers.
Windows, and pytest 7 and 8 (the ❓ row).
