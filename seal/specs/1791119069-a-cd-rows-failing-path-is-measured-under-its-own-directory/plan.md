# Implementation Plan: a cd row's failing path is measured under its own directory (#761)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

Remove the root-tree split in `compare_at_base` and let the run at the base
decide absence: every failing file is appended to the prefix, and where pytest
replies `file or directory not found: <file>` for one of them, that file reads
`new` and the same prefix runs again without it. Every `new` the gate prints
then comes from a run at the base, invoked as the row invokes it, which is
what `agents/sealer.md` already says the word means.

## Technical context

Read at 94d7b2e0 unless another commit is named.

- `skills/verify/scripts/broad_gate.py#compare_at_base` — the `absent` /
  `present` split (`os.path.isfile(os.path.join(root, f))` and
  `git(scratch, "cat-file", "-e", f"HEAD:{f}")`), the comment citing round 1's
  🟡 2 above it, and the prefix loop over `row_prefixes(command,
  cmd_exe_reads())` that stops at the first output `PYTEST_SUMMARY_RE`
  matches. The not-found loop sits inside that prefix loop, at the prefix that
  printed the reply, and its `run(...)` calls stay in this function's body.
- `#verdicts_at_base`, `#FAILED_RE`, `#ERROR_RE`, `#STOPPED_EARLY_RE`,
  `#PYTEST_SUMMARY_RE`, `#NO_RUNNER`, `#STOPPED_EARLY` — unchanged. `ERROR_RE`
  (`^ERROR\s+(\S+?)(?:::|\s)`) does not match `ERROR: file or directory not
  found: …` (the colon follows `ERROR` directly), and `PYTEST_SUMMARY_RE`
  does not match `no tests ran in 0.00s` (no leading count). #758 round 2
  measured both for plain pytest 9.1.1 (`rounds/round-2-report.md`, the
  *Facts for the evidence ledger* list).
- pytest 9.1.1, read in this repository's `.venv`: `_pytest/main.py`
  `Session.perform_collect` resolves every argument in a list comprehension
  through `resolve_collection_argument`, which raises `UsageError` at the
  **first** missing one — so one reply per run, never a list.
  `_pytest/config/__init__.py` `Config.cwd_relative_nodeid` and
  `_pytest/terminal.py` (`mkrel`, `_get_node_id_with_markup`) make the
  short-summary path relative to the invocation directory, the same directory
  arguments are resolved against.
- `pytest-xdist` 3.8.0, read in the same `.venv`: `xdist/dsession.py`
  `DSession.pytest_collection` returns `True` — the controller does not
  collect, so the missing argument is met inside the workers, and how their
  failure reaches the output is not readable from the source. That is Q1.
  It matters to this repository: `bin/test` passes `-n auto` unless told
  otherwise (`.github/scripts/run_tests.py`, header), and this repository's
  row ends in `bin/test -q`.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` — `base_then_feature`,
  `SUITE_ROW` (`python -m pytest -q -p no:cacheprovider tests`), `verdict_of`,
  `MEASURED_ENDINGS`, and the cases S3/S7 name.
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py#test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  — the callers of `run(..., shell=…)` must be exactly `compare_at_base` and
  `gate`. A helper that calls `run` turns it red.

**What breaks in six months.** A pytest release rewords the not-found reply.
The reading then matches nothing, the run carries no summary, and every file
of it reads `new?` — the gate gets weaker, never counterfeit, and the
measured-ending row of S5 plus the unit of S6 go red on the pinned version
bump rather than silently. The same holds for an xdist release that changes
how a worker's crash is printed, by Scope 3.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Absence from pytest's own reply at the base, at the prefix that ran it** (chosen) | Costs one more run of the runner prefix, with every part before it, per failing file the base does not carry. In this repository's lint-first row that is two `ruff` runs and one pytest start per such file, and only on a failing broad gate. A pytest reword degrades to `new?` (above) | **Chosen.** Covers every member of `spec.md`'s class table, because pytest is the party asked, and makes the sealer's sentence true for every `new` |
| B. The issue's second fix: a row that changes directory before its runner makes every unnamed file `new?` | Detecting "changes directory" is syntactic, and the class is open: `make -C`, `env -C`, `pnpm --dir`, a runner script that changes directory itself (this repository's own `bin/test` does) all escape it and keep today's counterfeit `new`. And every `cd` row that today measures cleanly loses its `new`, sending a reader to the base by hand (`skills/verify/SKILL.md`, the **New?** bullet) | Rejected. Weaker verdicts where the measurement works, and the hole stays open where detection misses |
| C. Keep the root check and add round 1's proposed guard: a path absent at the base reads `new` only where the branch carries it at the root (`UNPLACED` otherwise) | That guard is exactly what lets #761 through: the branch DOES carry the path at the root, as a different file | Rejected — it is the current behaviour's premise |
| D. Probe existence with the parts before the runner plus `test -e <file>` | The runner may change directory itself, after those parts (`bin/test`); and which part is the runner is only known after a run, so it costs the same runs and measures a different directory | Rejected |
| E. Run each failing file alone at the base | One run per failing file always, against A's one per absent file plus one. Every lint-first row pays its lint parts per file | Rejected on cost; it measures no more than A |
| F. A `config.md` row naming the directory the runner runs in | A question added to every repository for something one run answers; `CLAUDE.md`'s goal, and #758 rejected the same shape for the runner | Rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The measurement Q1 asks for: pytest 9.1.1 given one present and one missing test path, invoked from a directory below a scratch root, once plain and once with `-n 2` (xdist 3.8.0), output and exit code recorded verbatim in `phases/phase-1.md`. It fixes the reply's line form the reading matches and the text S5's measured-ending row carries. No change to the tree beyond the phase record | executed — the two runs, in a scratch directory removed afterwards (agent-contract §7) | 95ac24fa |
| 2 | The fix and its cases, in one commit with the documents (§14): the split removed, the not-found loop at the runner's prefix (Scope 2–6), the kept-file naming, `compare_at_base`'s docstring, rule 3's cost sentence and its pin, the reworded docstring of the base-lacks case; new cases S1, S2, S4, S6, S5's row, the kept-file assertion of S3 | executed — S1, S2, S4 and S3's kept-file half each seen red against 94d7b2e0's `broad_gate.py` and green after; S6 and S8 each seen red by mutation (the exact match loosened; the pinned sentence deleted); S7's cases and the one-shell-site case by module | |
| 3 | The records: ledger rows for the new and changed units in this work item's fragment, `Corrected ·` rows for `seal/releases/0.18.1.md` B3 and `Corrected · S5`, a re-read row for each other released coordinate the change drifts (Q2), and the changelog fragment | executed — `evidence-check` over the tree, reporting no drifted row left unanswered | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

No migration, no new environment variable, no new dependency, no
compatibility break in any interface a caller types.

- **Cost.** One more run of the runner's prefix, with every part before it,
  per failing file the base does not carry where the row runs its tests. Only
  on a failing broad gate, because the comparison is reactive. Stated in rule
  3, where the row's author reads the cost of their order.
- **Kept files.** A reader of `--keep-output` may now see
  `suite-at-base-<k>-<m>.txt` beside `suite-at-base-<k>.txt`.
- **Failure direction** (`CONTRIBUTING.md` §*What a change to a gate must
  carry*). The change gives fewer unmeasured words, in both directions: a
  counterfeit `new` (#761, which wrongly sends work back through the loop)
  becomes a measured `failing on base too`, and a `cd` row's honest `new?`
  becomes a measured word. It can never give `failing on base too` without a
  `FAILED` or `ERROR` line at the base naming the file, which is the one word
  that lets a failure through without blocking. Where pytest's reply cannot be
  read, the outcome is `new?`, the cheaper mistake: it costs a reader one run
  by hand.
- **Prompt budget.** Zero. No question is added, at the gate or anywhere.
- **Platform honesty.** The reply is pytest's text and the same under
  `cmd.exe`; the arguments are still quoted by `quote` and the row still goes
  through `handed_to_shell` inside `run`. The cases run on the platforms CI
  runs; no `cmd.exe`-specific case is added, because nothing here depends on
  the shell's grammar.
