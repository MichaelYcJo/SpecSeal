# Round 1 report — 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory

Target `c553bd92` on `fix/761-a-cd-rows-failing-path-is-measured-under-its-own-directory`
(PR #787, draft), against `release/v0.18.2` at `94d7b2e0`. Issue #761.
Ran by specseal:warden on claude-opus-5-5. First round: no earlier
`round-N.md` exists, so nothing was carried from a record. What was carried
from the work item: the coordinates in `spec.md`, `plan.md` and
`phases/phase-1.md`, and phase 1's measured pytest outputs, which the probes
below reproduced in passing (`no tests ran in <t>s` with exit 4 plain and
exit 5 under `-n 2`). Every verdict was re-derived.

The review worked in a `git clone --no-local` of the branch at the target,
under `<scratchpad>/<id>/round-1/clone`, plus a second clone at `94d7b2e0` to
run the old gate side by side. Probes used a scratch venv with pytest 9.1.1
and pytest-xdist 3.8.0 (Python 3.14.3, darwin). Each probe called
`compare_at_base` directly on a two-commit scratch repository, built from a
script that drove git from Python (contract §8). The probe script, the
scratch repositories, the venv and both clones are removed.

## Summary

The approach H mechanism does what the re-framed spec asks for the shapes it
names. S1, S1x, S2, S3 and S4 hold under plain pytest and `-n 2`, and two of
the smith's mutation claims reproduce when I ran them again. Two holes in the
class remain. Both were measured, and both reach the documents this change
writes.

1. **The un-nominated direction can give `new` for a file the base fails.**
   That is worse than `new?`. When the base's pytest counts a warning, a run
   that collected nothing ends `1 warning in 0.00s` and not `no tests ran`,
   and `PYTEST_SUMMARY_RE` reads that line as a summary. Rule 3's third
   sentence, which is pinned, says each such file reads `new?`. The
   docstring says "never a counterfeit". (🟡 1)
2. **A row with two pytest runners in two directories is still a member of
   #761's class.** The candidate's solo run settles at the first runner, in
   the wrong directory. Measured: `new` for a file the base fails, and in the
   un-nominated direction `failing on base too` for a file the base never ran.
   The spec says a run of the row as written "asks the right directory
   whatever moved it". Rule 3 does not name the shape. (🟡 2)

Both holes predate the branch: `94d7b2e0` gives the same words on the same
fixtures. They are findings here because this change writes the claims they
falsify into rule 3, the docstring and the spec, and because #761's class is
the scope of this work item.

## What the account claimed, and what was checked

| Claim | Where it is made | What I found | How |
|---|---|---|---|
| The candidate rule is the base half of the split alone, `git cat-file -e HEAD:<f>` in the scratch worktree, and it decides nothing | `spec.md` Scope 1; `skills/verify/scripts/broad_gate.py:2101` | Holds. The branch-root condition is gone. Every candidate is decided by a run, and no word comes from the tree | read, and executed through S1–S4 |
| A solo run reads summary → measured word, a lone `no tests ran` with exit 4 or 5 → `new`, anything else → `new?` | `spec.md` Scope 2 | Holds for the outputs pytest prints when it counted no warning. With a warning, the nothing-collected line is `1 warning in <t>s`. For a solo run that still gives the right word, `new`, but through `verdicts_at_base`. For a run of several it gives a counterfeit (finding 1) | **executed**, probes p2 |
| A run of the row at the base with the file appended "asks the right directory whatever moved it" | `spec.md:57` | Holds for a row with one runner. It does not hold for a row with two runners in two directories (finding 2) | **executed**, probes p1, p1b |
| The un-nominated direction gives `new?`, "never a counterfeit" | `spec.md:71`; `plan.md:89`; `broad_gate.py:2087`; rule 3 sentence 3 | Holds only where the base's pytest counts no warning (finding 1) | **executed**, probes p2 |
| The case `test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd` goes red without the `alone and` guard | `phases/phase-2.md` mutation table | Holds. I dropped the guard in the clone, and that case failed | **executed** |
| `S3[plain]` goes red when the return is `verdicts` in run order | `phases/phase-2.md` | Holds. I made the mutation in the clone, and `test_a_root_run_row_measures_the_module_the_branch_added[plain]` failed | **executed** |
| The new and touched cases are green at the target | orchestrator's narrow run | Holds. 25 selected cases passed, none skipped (xdist present) | **executed** |
| Six divergences are listed in `overview.md` | the spawn prompt | Not as stated. `overview.md` has four rows: call count, the `SKILL.md` glob, the `NAME NOT IN TREE` marks, and the return order. The added limit case and the `VERSIONS_OF_ANOTHER_PRODUCT` row are recorded only in `phases/phase-2.md` and `phases/phase-3.md` (⬜ 5) | read |
| In this repository's row, the solo run costs "two `ruff` runs and one `bin/test` start" per candidate | `plan.md:89` | Does not hold. The row has three prefixes, so a candidate costs `ruff check` three times, `ruff format --check` twice, and `bin/test` once. Rule 3 states the cost correctly, in prefix runs (⬜ 6) | read |

## Findings from execution

### 🟡 1 — a run of several that counted only warnings is read as pytest's summary, and a file the base fails reads `new`

**Where.** `skills/verify/scripts/broad_gate.py:2126`, where
`PYTEST_SUMMARY_RE` is asked before anything else. With it,
`NOTHING_COLLECTED_RE` at `skills/verify/scripts/broad_gate.py:1879`.

**What happens.** pytest prints `no tests ran in <t>s` only when it counted
nothing at all. If anything was counted, including a warning, the last line
gives the counts: `1 warning in 0.00s`, or under xdist `3 warnings in 0.49s`.
That line matches `PYTEST_SUMMARY_RE`. The run is then read as a measurement.
No `FAILED` line names any file, and no `!` rule appears, so every file of
the run reads `new`.

**Measured** (probe p2, both gates). The row is `cd sub && python -m pytest -q
-p no:cacheprovider tests`. The base carries `tests/test_one.py` and
`tests/test_two.py` at the root, a failing `sub/tests/test_one.py`, and a
`sub/pytest.ini` with an unknown ini key. The branch keeps the failure and
adds a failing `sub/tests/test_two.py`. Both failing paths exist in the base's
root tree, so neither is a candidate, and they run together. At the base the
run collects nothing because `sub/tests/test_two.py` is missing:

| | plain | `-n 2` |
|---|---|---|
| without the ini key | both `new?` (`NO_RUNNER`) | both `new?` |
| with the ini key | **both `new`**; kept output ends `1 warning in 0.00s` / `ERROR: file or directory not found` | **both `new`**; kept output ends `3 warnings in 0.49s` |

`tests/test_one.py` fails at the base. The word `new` sends it back through
the loop as the branch's breakage (`agents/smith.md`, the three returns).

**Why it matters here.** This change writes the opposite claim in three
places. Rule 3's third sentence, pinned by
`tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`,
says "that run collects nothing, and each file in it reads `new?`". The
docstring at `broad_gate.py:2087` says "never a counterfeit". The spec's class
table says "Honest, never counterfeit". A pytest config warning is common at
a base. One example is an ini key whose plugin is not installed.

**Fix.** `NOTHING_COLLECTED_RE` also reads a warnings-only count line. A run
that collected nothing is never read as a summary. It settles a file run
alone as `new`, as before, and it settles a run of several as nothing. The
fix was applied in the clone. With it, the probe gives `new?` for all four
p2 runs. The proposed case and five new unit rows pass, and they fail
against the target's gate (4 failed: the two `True` warning rows and the case
under plain and `-n 2`). The 63 cases selected around the comparison pass
with it, including S1–S4, `MEASURED_ENDINGS`, `SUMMARY_LINES` and the
stopped-early cases. A `1 warning, 1 error in` line is deliberately left a
summary, because there the `ERROR` line is a measurement, and a unit row pins
that. Ledger row D1 and the `Corrected · B3` text, which describe the
nothing-collected line, change with it.

### 🟡 2 — a row with two runners in two directories is measured in the first runner's directory

**Where.** `skills/verify/scripts/broad_gate.py:2131`: a candidate's walk
stops at the first prefix that settles it. The claim is at `spec.md:57`.
Rule 3 is `templates/config.md:333`.

**What happens.** A candidate's solo run walks the prefixes from the first
one. Take a row like `pytest -q tests && cd sub && pytest -q tests`. Its first
prefix is the root runner, with the candidate appended. That runner names
files from the root, and the failing file was named by the `sub` runner, so
the root runner looks for the path in the wrong directory. That is #761's
defect: "the gate decided absence in a different directory".

**Measured** (probes p1, p1b; the same words at `94d7b2e0`):

- **p1.** The base has a passing root `tests/test_one.py` and a failing
  `sub/tests/test_two.py`, and the branch still fails the latter. The file is
  a candidate because the base's root lacks `tests/test_two.py`. Its solo
  run's first prefix is the root runner with `tests/test_two.py` appended. It
  prints `no tests ran` with exit 4, or exit 5 under `-n 2`, so
  `collected_nothing` gives **`new`**. The base fails that file.
- **p1b.** The base fails a different root `tests/test_two.py`. The branch
  fixes that file and adds a failing `sub/tests/test_two.py`. The base's root
  carries the path, so this is not a candidate, and the first prefix runs the
  root file. It reads **`failing on base too`**, the one word that lets a
  failure through without blocking. The base never had the failing test.

**Why it matters here.** In the old gate this shape reached its wrong `new`
through a different path: a later prefix whose first part printed a summary.
Rule 3 already names that path ("a part that prints pytest's summary without
running the files appended to it"). p1 now reaches `new` through
`collected_nothing`, a path the docstring calls a measurement. And no
sentence in rule 3 covers p1b. Rule 3 is "the one home of what the comparison
costs a row and which rows it cannot measure" (`spec.md` §*Grounding*). The
class table in `spec.md` §*The class, enumerated by construction* enumerates
one runner per row, and this member falls outside it. I found no code fix
that measures this shape. Continuing the walk past a nothing-collected prefix
does not help: the next prefix's first part prints a summary over the root
suite and settles it. So the fix is the statement and its pin.

## Findings from reading

### ⬜ 3 — `compare_at_base`'s second docstring paragraph still describes the old split

`skills/verify/scripts/broad_gate.py:2049-2051`: "Each run is kept as
`suite-at-base-<k>.txt`. Where no prefix prints a line read as that summary,
every present file reads `new?`, never `new`." `present` names the removed
split. "Never `new`" is now false for a candidate: its run reads `new` with
no summary, through `collected_nothing`. The paragraph four paragraphs below
says the right thing, so a developer who reads on gets the right answer.

### ⬜ 4 — the pytest 9.1.1 exemption's reason names two of the three comments that carry the number

`tests/test_release_hygiene.py:159`: the reason says the number appears in
"the comments over `ERROR_RE` and `STOPPED_EARLY_RE`". The comment over
`NOTHING_COLLECTED_RE` (`broad_gate.py:1874`) now names pytest 9.1.1 too. The
exemption is keyed on file and token, so it still covers the new comment.
Only the reason is incomplete.

### ⬜ 5 — `overview.md`'s divergence table has four rows, and the work has six

`seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:9`.
Two divergences are missing from it. One is the case
`test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd`,
added beyond S1–S7. The other is the `VERSIONS_OF_ANOTHER_PRODUCT` row in
`tests/test_release_hygiene.py`, a file the spec never names. Both are sound
(see the 🟢 rows) and both are recorded in a phase file. But `overview.md` is
the record that outlives the phases, and the spawn prompt already counted six
there. This is a correction to the work item's paperwork.

### ⬜ 6 — `plan.md` miscounts the solo run's cost on this repository's row

`seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/plan.md:89`
says "two `ruff` runs and one `bin/test` start per failing file the base
lacks". The row `uvx ruff check . && uvx ruff format --check . && bin/test -q`
has three prefixes, and a candidate runs every one of them. That is `ruff
check` three times, `ruff format --check` twice, and `bin/test` once. Rule 3's
wording, "one more run of each prefix up to and including the runner", is
right. This is a correction to the work item's paperwork.

### ⬜ 7 — a runner that remaps pytest's exit code turns a truly new module from `new` into `new?`

Probe p3, executed: the row is `sh bin/t.sh`, where the script runs
`python -m pytest -q -p no:cacheprovider "$@" || exit 1`, and the branch adds
a failing root module. At `94d7b2e0` the module read `new` with no run, a word
the old gate inferred, though it was true. At the target it reads `new?`,
because the solo run's exit is 1. The kept output still carries plain
pytest's `ERROR: file or directory not found: tests/test_three.py`. The
result is honest, so this is not a defect. But `plan.md` §*Operational
impact* says the change "gives fewer unmeasured words", and for this shape it
gives one more. Rule 3's "with exit 4 or 5" lets a row's author work this
out. A sentence naming it, or reading plain pytest's not-found reply when it
names the very file, would close it. This is the smith's call.

### ⬜ 8 — the `skills/verify/SKILL.md` glob edit is unpinned

`skills/verify/SKILL.md:509` now tells a reader to open
`suite-at-base-*.txt`. Ledger row D2 records it as "**read**, not pinned".
Contract §14 asks for a pin in the same commit, and the edit is right. The
missing pin is the finding.

## Confirmations

- **Scope 1–6 at the target.** Candidates come from the base's tree alone.
  The others' group runs first, then one group per candidate in first-seen
  order. A single loop holds a single `run(...)` call. Runs are kept as
  `suite-at-base-<k>.txt` and `suite-at-base-<k>-<n>.txt`. `NO_RUNNER` names
  both forms and is pinned whole. `row_prefixes`, `verdicts_at_base` and the
  regexes beside them are unchanged. Executed through S1–S4 and the probes;
  read in the diff.
- **Divergence: Scope 4's call count.** The case counts calls
  (`tests/test_the_gate_hands_cmd_a_path_it_can_run.py:328`,
  `sorted(callers) == ["compare_at_base", "gate"]`), and one loop over groups
  keeps it unchanged. That meets the spec's intent.
- **Divergence: the `SKILL.md` glob.** It is required by §12, and its meaning
  is unchanged (pin: ⬜ 8).
- **Divergence: the added limit case.** It is the only case that holds the
  `alone and` guard, and my mutation run showed it red without the guard.
- **Divergence: the return order.** `{f: verdicts[f] for f in files}`, pinned
  by `S3[plain]`. My mutation run showed that red too. Every file lands in
  exactly one group, so the comprehension cannot raise.
- **Divergence: the `NAME NOT IN TREE` marks.** They sit on `spec.md:55` and
  on two `plan.md` lines. Only the marker was added, and the framer's words
  are unchanged. This is the repair the checker's refusal names.
- **Divergence: the `VERSIONS_OF_ANOTHER_PRODUCT` row for 3.8.0.** Keyed on
  `(broad_gate.py, "3.8.0")`. It is the fourth member of the class the
  2.54.0 row defines, and the count is right (seal.py 2.50.1, then 2.54.0,
  9.1.1 and 3.8.0). Its own reason is complete; ⬜ 4 is about the 9.1.1
  row beside it.
- **Rule 3, sentences 1 and 2, against the code.** Sentence 1 holds: the
  walk stops at the first settling prefix, which is the runner. Sentence 2
  holds: `alone` and `collected_nothing` give `NEW`. Sentence 3 is finding 1.
- **`Corrected · B3` and `Corrected · S5`.** Each states the code at the
  target: the candidate rule, the two kept forms, the nothing-collected
  reading with exit 4 or 5, and the order of the words. Each cites the
  released row it supersedes, in the form `docs/the-evidence-ledger.md`
  gives. Neither claims anything about the un-nominated direction, so
  neither is falsified by finding 1. Finding 1's fix will change the
  sentence about the nothing-collected line.
- **Lint prefix, other tools' lines, wrapper exits (Question 1).** A
  lint-first row's lint prefixes never settle a candidate: lint run on a
  missing path prints neither line. A lint part that fails at the base stops
  the `&&` chain, so the file gets `NO_RUNNER`, as rule 3 already says.
  `bin/test` passes pytest's exit 5 through: `.github/scripts/run_tests.py:647`
  returns the child's code, and `phases/phase-1.md` measured it. A wrapper that
  remaps the code gives `new?` (⬜ 7). The nothing-collected line needs both
  the line alone on its line and exit 4 or 5, and S5's rows pin each half.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the case and the five
  `NOTHING_COLLECTED` rows in finding 1's fix. Seen red against the target's
  gate: 4 failed. Seen green with the fix: 63 passed in the selection around
  the comparison.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`:
  add finding 2's sentence to its tuple, and see it red with the sentence
  deleted.

## Facts for the evidence ledger

- pytest 9.1.1, from `sub/` with an appended path that does not exist and an
  unknown ini key: plain prints `1 warning in 0.00s` and the not-found reply,
  exit 4. Under `-n 2` it prints `3 warnings in 0.49s`, exit 5. Neither
  prints `no tests ran`. Executed in this round's probes p2.
- Two runners in two directories: the candidate's solo run settles at the
  first runner (p1), and a non-candidate's group run measures the root's
  same-named file (p1b). Executed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A run of several that collected nothing but counted a warning ends `1 warning in <t>s`, which `PYTEST_SUMMARY_RE` reads as a summary, so a file the base fails reads `new` in the un-nominated direction; rule 3's pinned third sentence, the docstring and the spec say `new?` | `skills/verify/scripts/broad_gate.py:2126` | open | executed, probes p2: `new` for a file the base fails, plain and `-n 2`, at the target and at `94d7b2e0`; with the fix all four read `new?`, and the proposed case and rows are red against the target's gate |
| 🟡 2 | A row with two pytest runners in two directories is measured in the first runner's directory: `new` for a file the base fails, and `failing on base too` for a file the base never ran; rule 3 names neither and `spec.md:57` claims the right directory is always asked | `templates/config.md:333` | open | executed, probes p1 and p1b at the target and at `94d7b2e0` |
| ⬜ 3 | `compare_at_base`'s second docstring paragraph says "every present file reads `new?`, never `new`", which names the removed split and is false for a candidate | `skills/verify/scripts/broad_gate.py:2049` | open | read |
| ⬜ 4 | The pytest 9.1.1 exemption's reason names the comments over `ERROR_RE` and `STOPPED_EARLY_RE`, and not the one over `NOTHING_COLLECTED_RE` | `tests/test_release_hygiene.py:159` | open | read |
| ⬜ 5 | `overview.md`'s divergence table omits the added limit case and the `VERSIONS_OF_ANOTHER_PRODUCT` row, which are recorded only in phase files | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:9` | open | read; a paperwork correction |
| ⬜ 6 | `plan.md` counts two `ruff` runs per candidate on this repository's row; the row's three prefixes cost five | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/plan.md:89` | open | read; a paperwork correction |
| ⬜ 7 | A runner that remaps pytest's exit code turns a truly new module from `new` (unrun) into `new?`; honest, but it contradicts the plan's "fewer unmeasured words" and rule 3 does not name it | `skills/verify/scripts/broad_gate.py:1935` | open | executed, probe p3 |
| ⬜ 8 | The `skills/verify/SKILL.md` glob edit is unpinned (contract §14) | `skills/verify/SKILL.md:509` | open | read; ledger D2 says so |
| 🟢 | Scope 1–6: the candidate rule, the solo runs, the others' group unchanged, the order, the kept names, `NO_RUNNER`'s parenthesis | `skills/verify/scripts/broad_gate.py:2034` | confirmed | executed: 25 selected cases passed with none skipped; probes p1–p3 kept the files the spec names |
| 🟢 | Divergences: one `run` call, the `SKILL.md` glob, the added limit case, the return order, the `NAME NOT IN TREE` marks, the 3.8.0 exemption | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:9` | confirmed | the limit case and the return order executed by mutation; the rest read |
| 🟢 | `Corrected · B3` and `Corrected · S5` state the code at the target and cite the rows they supersede | `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md:16` | confirmed | read against the code |

## Executed probes

| What was run | Result |
|---|---|
| The selected cases of `tests/test_the_seal_is_taken_once_by_the_sealer.py` around the comparison (S1–S5, S7, the base-lacks case, the below-a-cd case, the limit case, the runner-first, semicolon and lint-first cases, the `NO_RUNNER` pin), `-n 4`, in the clone at `c553bd92` | 25 passed, 0 skipped |
| Mutation: the `alone and` guard dropped | `test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd` failed; the clone restored |
| Mutation: the return written as `verdicts` | `test_a_root_run_row_measures_the_module_the_branch_added[plain]` failed; the clone restored |
| p1: `compare_at_base` on a row with a root runner and a `cd sub` runner; the base fails `sub/tests/test_two.py`, plain and `-n 2`, the target's gate and `94d7b2e0`'s | `new` from all four; at the target from `suite-at-base-1-1.txt`, which ends `no tests ran` (exit 4, or exit 5 under `-n 2`) |
| p1b: the same row; the base fails a different root `tests/test_two.py`, and the branch adds a failing `sub/tests/test_two.py` | `failing on base too` at both gates |
| p2: `cd sub` row in the un-nominated direction, the base failing `sub/tests/test_one.py`, with and without an unknown ini key, plain and `-n 2`, at both gates | without the key: `new?` for both files; with it: `new` for both, kept outputs ending `1 warning in 0.00s` and `3 warnings in 0.49s` |
| p3: an exit-remapping wrapper row, the branch adding a failing root module | the target gives `new?`; `94d7b2e0` gives `new` |
| Finding 1's fix applied in the clone: the probes, then the selected comparison cases plus the new case and rows | p2 all `new?`; 63 passed |
| Finding 1's new case and rows against the target's gate | 4 failed (the two `True` warning rows, and the case plain and `-n 2`); the clone restored |
| The full suite, lint and typecheck (the broad gate) | not yet — the sealer's, after the rounds settle; not run in this round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1

`skills/verify/scripts/broad_gate.py`, the comment and constant at line 1872:

```python
# The line that says pytest collected nothing: `no tests ran in 0.21s`, alone
# on a line, bare under `-q` or between `=` rules as the summary is (#761).
# Measured against pytest 9.1.1 and pytest-xdist 3.8.0 in that work item's
# `phases/phase-1.md`: given a path that does not exist, plain pytest prints
# it beside `ERROR: file or directory not found: <path>` and exits 4, and
# under xdist it is the only trace and the exit is 5. It carries no leading
# count, so `PYTEST_SUMMARY_RE` never reads it as a summary. Where the run
# counted warnings, pytest prints their count in its place, `1 warning in
# 0.00s` plain and `3 warnings in 0.49s` under xdist (#761 round 1, an ini
# key pytest does not know). That line DOES match `PYTEST_SUMMARY_RE`, so
# `compare_at_base` asks this reading first. A count of warnings beside any
# other count (`1 warning, 1 error in …`) is a summary and is not read here.
NOTHING_COLLECTED_RE = re.compile(
    r"^=*\s*(?:no tests ran|\d+ warnings?) in \d+(?:\.\d+)?s"
    r"(?: \(\d+:\d\d:\d\d\))?\s*=*$",
    re.M,
)
```

The loop in `compare_at_base`, at line 2126:

```python
                # A run that collected nothing is never read as a summary,
                # even where warnings give its last line a count. Only for a
                # file run alone does it settle anything: a group of several
                # that collects nothing does not say which of them the base
                # lacks.
                empty = collected_nothing(tried.text, tried.code)
                if empty and alone:
                    nothing = True
                    break
                if not empty and PYTEST_SUMMARY_RE.search(tried.text):
                    measured = tried.text
                    break
```

The docstring's last paragraph, at line 2085:

```python
    nominated: it runs with the others, that run collects nothing, which is
    never read as pytest's summary even where warnings give its last line a
    count, and each file of it reads `new?`, never a counterfeit.
```

`tests/test_the_seal_is_taken_once_by_the_sealer.py`, rows added to
`NOTHING_COLLECTED` before the "inside a longer line" rows:

```python
    # A run that collected nothing but counted warnings: pytest gives the
    # count in place of `no tests ran` (#761 round 1).
    ("1 warning in 0.00s\nERROR: file or directory not found: tests/x.py\n", 4, True),
    ("=== 3 warnings in 0.49s ===\n", 5, True),
    ("1 warning in 0.00s\n", 1, False),
    ("1 passed, 1 warning in 0.01s\n", 0, False),
    ("1 warning, 1 error in 0.01s\n", 2, False),
```

And the case, beside the limit case:

```python
@pytest.mark.parametrize("xdist", UNDER)
def test_a_run_of_several_that_counted_only_warnings_is_not_measured(
    tmp_path, xdist
):
    """#761 round 1. As the limit case, and the base's `sub/tests/test_one.py`
    fails while an ini key pytest does not know gives every run a warning.
    The run of the two files collects nothing, and its last line is
    `1 warning in <t>s` rather than `no tests ran`. That line is not a
    measurement: `tests/test_one.py`, which the base fails, reads `new?`,
    never `new`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {suite_row(xdist)}",
        {
            "tests/test_one.py": PASSING_TEST,
            "tests/test_two.py": PASSING_TWO,
            "sub/tests/test_one.py": FAILING_TEST.replace("test_two", "test_one"),
            "sub/pytest.ini": "[pytest]\nan_unknown_key = 1\n",
        },
        {
            "sub/tests/test_one.py": FAILING_TWO.replace("test_two", "test_one"),
            "sub/tests/test_two.py": FAILING_TWO,
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_one.py") == gate.NO_RUNNER, out.stdout
```

### 🟡 2

`templates/config.md` rule 3 (line 333), a sentence after "and each file in
it reads `new?`.":

```
A row that runs pytest in more than one directory — `pytest -q && cd sub && pytest -q` — is asked about every failing file by the first runner a prefix reaches, in that runner's directory: a file a later runner named reads `new` where that directory has no such file, and `failing on base too` where a same-named file there fails at the base. Read either word as the row's claim rather than a measurement, or write the row so one runner runs every directory.
```

Its pin, a fourth entry in the tuple of
`test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`:

```python
        "A row that runs pytest in more than one directory — `pytest -q && "
        "cd sub && pytest -q` — is asked about every failing file by the first "
        "runner a prefix reaches, in that runner's directory: a file a later "
        "runner named reads `new` where that directory has no such file, and "
        "`failing on base too` where a same-named file there fails at the base.",
```

`spec.md:57`, scoped to the rows the claim holds for, and a row for
§*Out, and why*:

```
So a run at the base, of a row with one runner as written, with the file
appended, asks the right directory whatever moved it.
```

```
| A row with two pytest runners in two directories | A candidate's solo run settles at the first runner, in its directory (`new` for a file the base fails), and a group's run can measure the root's same-named file (`failing on base too`). Measured in round 1, probes p1 and p1b, and identical at 94d7b2e0. No run of the row distinguishes the two runners' files, so rule 3 names it | the repository owner, if it is ever met — a new issue |
```

Needs a fix: yes — 🟡 1 (a warnings-only nothing-collected line read as a summary gives `new` for a file the base fails) and 🟡 2 (two runners in two directories, unnamed in rule 3).
Loses a record or crashes: no

The broad gate has not come due: this report leaves two 🟡 open.

## Proof block

Files opened in this round, at `c553bd92` unless noted:

- `skills/verify/scripts/broad_gate.py` (lines 55–90, 1421–1520, 1795–2160, 3250–3310), and the same file at `94d7b2e0` through the second clone
- `templates/config.md` (the diff of rule 3)
- `skills/verify/SKILL.md` (the diff)
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the diff; lines 685–687, 3964–4000)
- `tests/test_release_hygiene.py` (lines 120–185)
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` (lines 303–328, by search)
- `bin/test`; `.github/scripts/run_tests.py` (the exit-code lines, by search)
- `seal/config.md` (the `Broad gate` row)
- `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/`: `spec.md`, `plan.md`, `overview.md`, `questions.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`
- `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`
- `seal/releases/0.18.1.md` (rows B3 and `Corrected · S5`)
- `docs/the-evidence-ledger.md` (the `Corrected ·` lines, by search)
- `agents/sealer.md`, `README.md`, `README.ko.md`, `agents/smith.md` (the `failing on base too` lines, by search)
- `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/rounds/round-2-report.md` (its head, for the report shape)
