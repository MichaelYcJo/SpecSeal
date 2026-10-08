# Feature Specification: the macOS test leg runs in shards (#864)

<!-- seal/specs/1791384162-the-macos-test-leg-runs-in-shards/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | the shard count and the budget are chosen from measured figures and written beside their run ids; nothing here stops to ask a person, and the one thing the tree could not answer is a measurement a CI run gives |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `.github/workflows/` is under it: every changed or new case is seen red before it is committed; the failure direction is *block more* (a macOS shard over its budget fails at GitHub, as the unsharded leg did); the prompt budget is zero; platform honesty is the issue's own demand, so the balance on macOS is read off macOS jobs and never inferred from the Windows-measured file |
| `CONTRIBUTING.md` §*Running the checks* | the home of the sentence counting CI's jobs and of the `.test_durations` refresh recipe; both name the Windows leg alone today and both change |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | `seal/releases/0.20.0.md` S1, S2, S4 and S8 anchor `.github/workflows/test.yml#pytest` and the two test modules this work edits; `Ledger frozen from` is declared, so each drifted row is a `Re-read ·` row in this item's fragment, and the one unit this work renames takes a `Corrected ·` row that re-points S4 |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | the changelog entry and the ledger rows are this work item's fragments; `changelog/0.20.0.md`'s *ubuntu and macOS stay one job each* is released history and stays |
| `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/questions.md` Q1 (a) and Q6 (a) | inherited, not re-decided: a sharded leg's slowest shard is at or under 12 minutes; a leg's `timeout` is 1.5 times its slowest measured job, rounded up to 5 minutes, with the run id beside it. The owner left both at their defaults and 0.20.0 shipped on them (`seal/releases/0.20.0.md` S4, S8) |
| #834's inventory, part 6 rows 85 and 232–235 (`git show origin/chore/834-every-reader-and-record-is-inventoried:seal/specs/1791382684-every-reader-and-record-is-inventoried/inventory/6-tests.md`) | the `pytest` job is sliced out of `test.yml` by private readers in four places, each a guess over YAML text, and a block-style matrix entry is invisible to the one that reads entries; this work leaves one reading and makes it refuse what it does not recognise |

## Scope

**In.**

1. **The macOS leg runs as three shards.** Three `macos-latest` entries in
   the `pytest` matrix, `split: "--splits 3 --group k"` for `k` 1 to 3,
   divided by `pytest-split` from the committed `.test_durations`, the same
   file the Windows shards read. Three is the smallest count whose slowest
   shard the arithmetic in `plan.md` puts under the inherited 12 minutes on
   the slowest measured pace; the measurement decides it, and the work takes
   four if the first sharded run says so (`questions.md` Q2).

   One file, for both legs, because the division does not depend on the
   operating system: the three legs collect the same cases. At 5623d728
   (0.20.0 as shipped) macOS ran 12,730 passed and 89 skipped, ubuntu 12,739
   and 80, and the four Windows shards 2,734, 6,742, 1,120 and 2,223 passed
   and skipped together — 12,819 on each, and 12,819 when this frame
   collected the tree locally (`executed` 2026-10-07: run 37577753583's job
   logs, and a `--collect-only` run; `plan.md` §*Technical context*). So
   group `k` holds the same cases on macOS as on Windows, and the union of a
   macOS shard with its siblings is the suite by the argument S4 of 0.20.0
   already made. What the file cannot say is each case's price on macOS,
   which is why the balance is measured there and never read off the file
   (scenario S2).

2. **The macOS budget re-derived from the sharded figure.** Each macOS entry
   carries `timeout` by the inherited rule, 1.5 times the slowest measured
   macOS shard rounded up to 5, beside the run id. Until the first sharded
   run exists, the three entries carry the unsharded leg's 35 and the
   comment says so: a value arithmetic guessed could go red on the very run
   whose purpose is the figure.

3. **The matrix is read once.** A helper beside `jobs` in
   `tests/test_ci_gives_the_checks_what_they_need.py` (`pytest_matrix`, NAME NOT IN TREE: phase 1 plants it)
   returns the `pytest` job's `include:` entries as dicts, read from
   `conftest.code_lines` so a commented-out entry is not an entry, and
   refuses with its text any item under `include:` that is not a one-line
   `- { … }` flow mapping — the shape every entry of this file has, and the
   one shape the reader owns. Its input class is *owned* (this repository's
   own workflow, in a shape this suite fixes), and it refuses the unknown.
   It is driven over fixtures in that module, the way `conftest.py`'s
   readers are in `tests/test_a_workflow_is_read_the_one_way.py`. The four
   private slices `text.index("  pytest:") : text.index("  ledger:")` go —
   one each in `tests/test_a_slow_case_names_itself.py` and
   `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`, two
   in `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` — and
   each site reads `jobs(read("test.yml"))["pytest"]`, and the entries
   through the helper where it reads entries. `tests/test_arm_check.py`
   already imports `jobs` this way.

4. **The shard test holds every sharded leg.** The module keeps its file
   name and its claim widens: a table of the sharded operating systems and
   their counts, `windows-latest` 4 and `macos-latest` 3; every entry of a
   sharded system carries `--splits K --group k` with that system's `K`, the
   groups are exactly 1 to `K` once each, every other entry carries no
   `split`, the one pytest line hands `${{ matrix.split }}` to pytest, and
   the durations file parses. The case
   `test_every_group_of_the_windows_split_runs_exactly_once` is renamed to
   say each sharded leg
   (`test_every_group_of_each_sharded_leg_runs_exactly_once`, NAME NOT IN TREE: phase 1 plants it),
   which is what the `Corrected ·` row for 0.20.0's S4 re-points to; the
   other two cases keep their names.

5. **Every sentence that says macOS is one job.** Enumerated by `grep` over
   the tree outside released files and work-item records (`executed`
   2026-10-07): `test.yml`'s *ubuntu and macOS stay one job each* and its
   *`split` is empty on ubuntu and macOS*; the `timeout` comment's macOS
   line; the comment on `.github/scripts/run_tests.py#PYTEST_SPLIT`, which
   names the Windows leg as the one divided; `CONTRIBUTING.md` §*Running
   the checks*' job-count sentence and, in the refresh recipe, *because the
   matrix has no shards* (now: because the Windows leg has none) and
   *ubuntu and macOS upload the committed file* (now: ubuntu and the macOS
   shards). The recipe's shape — one Windows `store` entry in place of the
   four shard entries, the macOS shards left as they are — is otherwise
   unchanged.

6. **The records.** `phases/phase-1.md` and `phases/phase-2.md` with the
   reds seen and the run's figures;
   `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` with one
   row per scenario, the `Re-read ·` rows for 0.20.0's S1, S2 and S8 written
   by `evidence-check --reverify --into`, and the `Corrected ·` row for S4;
   `changelog.md`, one `### Changed` entry stating the macOS leg before and
   after with run ids and dates; `overview.md` closed.

**Out, and why.**

- **ubuntu stays one job.** The issue says so; 7 m 51 s to 9 m 03 s on the
  runs measured, inside 15.
- **A macOS-measured durations file.** `pytest-split` can read a second
  file (`--durations-path`), but two files are two refresh runs and two
  recipes, and the division is the same on both systems anyway (item 1).
  Today's imbalance is the file's age, not the operating system: 504 of the
  12,819 collected cases are not in the file and 727 of its 13,042 entries
  are no longer collected (`executed`, this frame's probe), and the Windows
  shards already run 6 m 03 s to 11 m 38 s of pytest time in one run. It
  becomes the next design only if four shards also miss the target, and
  then as its own issue.
- **Refreshing `.test_durations`.** `CONTRIBUTING.md`'s recipe, a dedicated
  Windows run the owner starts; it would re-balance both legs at once.
  Named in the report as a leftover, not built here.
- **Cutting the macOS-heavy cases at the source.** The shell oracle
  (`tests/test_one_heredoc_shape_agrees_with_the_shell.py`, 113 s of calls
  in the macOS top 50 of run 37577753583, skipped on Windows) and the rest
  of that table; #841's `spec.md` left them to the owner, and sharding is
  what the issue asks for.
- **The other reader of `python:`.** `tests/test_release_hygiene.py` takes
  the floor from every `python:` in the whole file, not from the job; it is
  a different reading and stays. The floor case in
  `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` reads the
  job's entries and moves onto the helper (item 3). #835 owns the registry
  that would list both.
- **`publish-release.yml`, `bin/test`, the code of `run_tests.py`.** The
  release suite runs on ubuntu unsharded; the local runner never passes
  `--splits`; only a comment in `run_tests.py` changes.
- **The READMEs and `docs/`.** Neither edition of the README has a sentence
  about the CI legs, and no document under `docs/` describes the matrix
  (`grep`, `executed` 2026-10-07); `CONTRIBUTING.md` is the home.
- **Renaming the module file.**
  `test_the_windows_leg_runs_in_shards_that_make_the_whole.py` is still a
  true sentence, and its docstring says what it now holds. A file rename
  would move three released anchors for a name.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · three macOS shards make the whole suite | Given the matrix, when CI runs on a push, then three `macos-latest` jobs run groups 1, 2 and 3 of 3, each handed `--splits 3 --group k` by the one pytest line, and their `passed` plus `skipped` sum to ubuntu's `passed` plus `skipped` at the same SHA | each job's summary line (`gh run view --job <id> --log`); the shard module red with a macOS group named twice, a group named by no entry, a Windows entry carrying no split, and a ubuntu entry carrying one |
| S2 · the balance is measured on macOS | Given the first sharded run, when its macOS jobs are read `startedAt` to `completedAt`, then the slowest is at or under 12 minutes — and if it is not, the count becomes four and the next run is read the same way; the record carries every shard's time, count and `--durations=50` head | `gh run view <id> --json jobs`; `phases/phase-2.md` |
| S3 · the macOS budget is the measured shard's | Given the slowest measured macOS shard, when the budget is set, then each macOS entry's `timeout` is 1.5 times it rounded up to 5 minutes, the comment names the run, and the job reads `${{ matrix.timeout }}` as before | the timeout case red with one macOS entry's `timeout` removed; the comment |
| S4 · the matrix has one reader | Given the suite, when a case wants the `pytest` job or its entries, then it reads them through `jobs` and the entries helper of `tests/test_ci_gives_the_checks_what_they_need.py`; no test slices `"  pytest:"` to `"  ledger:"` itself; an `include:` item that is not a one-line flow mapping is refused naming it | `grep -rn 'index("  pytest:")' tests/` empty; the helper's fixture cases red with the refusal removed and with a commented entry counted |
| S5 · the sentences name both sharded legs | Given `CONTRIBUTING.md` and the workflow's comments, when a contributor reads which legs are sharded, what the file balances, and how to refresh it, then each sentence names Windows and macOS as sharded, ubuntu as one job, and the refresh as the Windows leg's | read; no case pins the job-count sentence (`grep` for *five jobs* and *four shards* over `tests/` is empty, `executed` 2026-10-07) |

## Data & interfaces

- **Matrix entries**, one flow mapping per line under `include:`:
  `- { os: macos-latest, python: "3.12", split: "--splits 3 --group k", timeout: <minutes> }`
  for `k` in 1 to 3. The Windows and ubuntu entries keep their shape.
- **The entries helper** (`tests/test_ci_gives_the_checks_what_they_need.py#pytest_matrix`, NAME NOT IN TREE: phase 1 plants it)
  takes the workflow's text and returns the `pytest` job's include entries
  as a list of dicts of the mapping's keys, string values with their quotes
  off the way `conftest.py`'s `_unquote` reads a step's name; it raises,
  naming the line, for an `include:` item that is not a one-line flow
  mapping. Input class *owned*; unknown input *refused*. The reader of
  `.test_durations` is unchanged (class *observed*, a tool-written file).
- **No new package, no new pin.** `pytest-split` 0.11.0 is already on the
  pip line and held to `.github/scripts/run_tests.py#PYTEST_SPLIT`.
- **Figures** live in `phases/phase-N.md` with run ids and dates; the
  workflow comment names the run each budget was set from, as it does
  today.

## Open questions → questions.md

Three rows, none a person's: the first sharded run's figures (Q1), the
count if three misses (Q2), and whether #835's registry has landed when
phase 1 builds (Q3). The judgments the issue left open that the tree
answered are listed at the head of that file.

Framed 2026-10-08 by framer, before the build.
