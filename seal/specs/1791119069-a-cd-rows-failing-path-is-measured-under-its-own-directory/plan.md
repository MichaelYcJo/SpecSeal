# Implementation Plan: a cd row's failing path is measured under its own directory (#761)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

Re-approved 2026-10-04 by the orchestrator after the re-frame at d22b105b (phase 1 broke approach A's premise; Q4 answered), when phases 2 and 3 were resumed.

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

**Re-framed 2026-10-04 after phase 1** (`phases/phase-1.md`, `questions.md`
Q4). Keep the root split in `compare_at_base`, but only as a pre-filter: a
failing file the base's tree lacks at the repository root is a candidate, and
decides nothing on its own. Each candidate is run alone at the base, through
the row's prefixes, and that run decides: a pytest summary gives the word the
run measured; pytest's nothing-collected line (`no tests ran in <t>s`, exit 4
or 5) gives `new`, now measured; anything else gives `new?`. Every other
failing file goes through the existing comparison unchanged. Every `new` the
gate prints then comes from a run at the base, invoked as the row invokes it,
which is what `agents/sealer.md` already says the word means.

## Technical context

Read at 94d7b2e0 unless another commit is named.

- `skills/verify/scripts/broad_gate.py#compare_at_base` — the `absent` /
  `present` split (`os.path.isfile(os.path.join(root, f))` and
  `git(scratch, "cat-file", "-e", f"HEAD:{f}")`), the comment citing round 1's
  🟡 2 above it, and the prefix loop over `row_prefixes(command,
  cmd_exe_reads())` that stops at the first output `PYTEST_SUMMARY_RE`
  matches. The split keeps its base half and loses its branch-root half; the
  candidates' solo loop sits after the existing loop, and every `run(...)`
  call stays in this function's body.
- `#verdicts_at_base`, `#FAILED_RE`, `#ERROR_RE`, `#STOPPED_EARLY_RE`,
  `#PYTEST_SUMMARY_RE`, `#STOPPED_EARLY` — unchanged. `PYTEST_SUMMARY_RE` does
  not match `no tests ran in 0.00s` (no leading count), so the
  nothing-collected line is a reading of its own and never a summary.
  `#NO_RUNNER` changes only its parenthesis (the kept-file names).
- `phases/phase-1.md` (95ac24fa), executed by `smith`: plain pytest 9.1.1
  given a missing argument prints `no tests ran in <t>s` on stdout and
  `ERROR: file or directory not found: <arg>` on stderr, exit 4; under
  `-n 2`, `-n auto`, `-rA`, `-v` and this repository's `bin/test -q` it prints
  `no tests ran in <t>s` (ruled with `=` without `-q`), exit 5, no not-found
  text, and the present file's tests do not run either. A run with nothing
  missing exits 1 with `1 failed in <t>s` (control).
- pytest 9.1.1, read in this repository's `.venv`: `Config.cwd_relative_nodeid`
  (`_pytest/config/__init__.py`) and `_pytest/terminal.py` (`mkrel`,
  `_get_node_id_with_markup`) make the short-summary path relative to the · NAME NOT IN TREE
  invocation directory, and `resolve_collection_argument` (`_pytest/main.py`) · NAME NOT IN TREE
  resolves an appended argument against the same directory. A solo run at the
  base therefore asks the directory the branch's `FAILED` line was relative
  to.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` — `base_then_feature`,
  `SUITE_ROW` (`python -m pytest -q -p no:cacheprovider tests`), `verdict_of`,
  `MEASURED_ENDINGS`, the whole-text pin of `NO_RUNNER`, and the cases
  `spec.md` S6 names.
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py#test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  — the callers of `run(..., shell=…)` must be exactly `compare_at_base` and
  `gate`. A helper that calls `run` turns it red.

**What breaks in six months.** A pytest or xdist release rewords
`no tests ran` or changes exit code 4 or 5. The nothing-collected reading then
matches nothing, the candidate's solo run settles at no prefix, and the
candidate reads `new?` — weaker, never counterfeit, and the S5 unit rows go
red on the pinned version bump rather than silently.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **H. Root split as a pre-filter; each candidate confirmed by a solo run at the base** (chosen; the orchestrator's answer to Q4) | Costs one run of each prefix up to and including the runner per candidate, only on a failing broad gate; in this repository's lint-first row that is two `ruff` runs and one `bin/test` start per failing file the base lacks. Two limits, both stated in rule 3: a base file that collects nothing reads `new` (true of the word: the base cannot fail a test it does not have, and a wrapper that drops its arguments is rule 3's existing hole); and a row that runs below a directory where the base carries a same-named file at the root is never nominated, so its run reads `new?` | **Chosen.** Measures #761 and the `cd` shared-plus-new shape under plain pytest and xdist, keeps this repository's root-run row measured, and every `new` comes from a run. Checked against the code for a direction it fails in: the un-nominated one (last row of `spec.md`'s class table) gives `new?`, never a counterfeit, because a run with a missing path prints no summary |
| A. Remove the root split; read absence off pytest's `file or directory not found` reply and re-run the same prefix without that file (the first frame, approved and refused) | **Measured in phase 1:** under xdist no not-found text is printed in any output setting, the run exits 5 with `no tests ran`, and the present files' tests do not run either. On this repository's row (`bin/test -q`, `-n auto`), a branch that adds a failing module beside a failure the base shares turns both measured words into `new?` (`phases/phase-1.md`, the before/after table) | Refused — weaker on the row this repository runs, every time a branch adds a failing test module |
| B. The issue's second fix: a row that changes directory before its runner makes every unnamed file `new?` | Detecting "changes directory" is syntactic, and the class is open: `make -C`, `env -C`, `pnpm --dir`, a runner script that changes directory itself all escape it and keep today's counterfeit `new`. And every `cd` row that today measures cleanly loses its `new`, sending a reader to the base by hand (`skills/verify/SKILL.md`, the **New?** bullet) | Rejected. Weaker verdicts where the measurement works, and the hole stays open where detection misses |
| C. Keep the root check and add round 1's proposed guard: a path absent at the base reads `new` only where the branch carries it at the root (`UNPLACED` otherwise) | That guard is exactly what lets #761 through: the branch DOES carry the path at the root, as a different file | Rejected — it is the current behaviour's premise |
| D. Probe existence with the parts before the runner plus `test -e <file>` | The runner may change directory itself, after those parts; and which part is the runner is only known after a run, so it costs the same runs and measures a different directory | Rejected |
| E. Run every failing file alone at the base | One solo run per failing file always, against H's one per candidate. Every lint-first row pays its lint parts per file, and root-run rows — where the split already asks the right directory — pay it for nothing | Rejected on cost; it measures no more than H on the members anyone has met |
| F. A `config.md` row naming the directory the runner runs in | A question added to every repository for something one run answers; `CLAUDE.md`'s goal, and #758 rejected the same shape for the runner | Rejected |
| G. H, plus a solo fallback: where the non-candidates' run collects nothing, run each of its files alone | Closes H's un-nominated direction, at one solo run per file in that event. The direction needs a `cd` row whose base carries a same-named file at the root but not below the `cd`; nobody has reported it, and H gives it `new?`, not a counterfeit | Not taken — mechanism for an unmet shape. `spec.md` §*Out* names it |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The measurement Q1 asks for: pytest 9.1.1 given one present and one missing test path, invoked from a directory below a scratch root, once plain and once with `-n 2` (xdist 3.8.0), output and exit code recorded verbatim in `phases/phase-1.md`. It fixes the reply's line form the reading matches and the text S5's measured-ending row carries. No change to the tree beyond the phase record | executed — the two runs, in a scratch directory removed afterwards (agent-contract §7) | 95ac24fa |
| 2 | The fix and its cases, in one commit with the documents (§14): the split narrowed to a pre-filter (Scope 1), the candidates' solo loop and the nothing-collected reading (Scope 2–4), the kept-file naming and `NO_RUNNER`'s parenthesis with its pin (Scope 5), `compare_at_base`'s docstring, rule 3's three sentences and their pins, the reworded docstring of the base-lacks case; new cases S1, S1x, S2 (plain and xdist), S3, S4 and the S5 unit rows | executed — S1, S1x, S2, S4 and S3's kept-file half each seen red against 94d7b2e0's `broad_gate.py` and green after; S5 each seen red by mutation of the reading; S7's pins each seen red with the sentence deleted; S6's cases and the one-shell-site case by module | 7d65dfe9 |
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

- **Cost.** One run of each prefix up to and including the runner, per
  failing file the base does not carry at the repository root. Only on a
  failing broad gate, because the comparison is reactive. Stated in rule 3,
  where the row's author reads the cost of their order.
- **Kept files.** A reader of `--keep-output` may now see
  `suite-at-base-<k>-<n>.txt` (the *n*-th candidate's run at prefix *k*)
  beside `suite-at-base-<k>.txt`, and `NO_RUNNER`'s reason names both.
- **Failure direction** (`CONTRIBUTING.md` §*What a change to a gate must
  carry*). The change gives fewer unmeasured words: a counterfeit `new`
  (#761, which wrongly sends work back through the loop) becomes a measured
  `failing on base too`, and a `cd` row's honest `new?` becomes a measured
  word. It can never give `failing on base too` without a `FAILED` or `ERROR`
  line at the base naming the file, which is the one word that lets a failure
  through without blocking. Where a candidate's solo run settles at no
  prefix, the outcome is `new?`, the cheaper mistake: it costs a reader one
  run by hand.
- **Prompt budget.** Zero. No question is added, at the gate or anywhere.
- **Platform honesty.** `no tests ran in <t>s` and exit codes 4 and 5 are
  pytest's on every platform; the arguments are still quoted by `quote` and
  the row still goes through `handed_to_shell` inside `run`. The xdist cases
  run where the fixture's interpreter carries `xdist` and skip with a reason
  elsewhere; no `cmd.exe`-specific case is added, because nothing here depends
  on the shell's grammar.
