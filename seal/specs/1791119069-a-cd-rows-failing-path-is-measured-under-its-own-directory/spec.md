# Feature Specification: a cd row's failing path is measured under its own directory (#761)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Found by round 2 of #758 (work item
`1791076832-the-broad-gate-re-runs-the-test-command-at-the-base`, read at
`refs/backup/0.18.1/local/fix/747-the-broad-gate-re-runs-the-test-command-at-the-base`,
`rounds/round-2-report.md` §*Deferred* and the probe table), and older than
it: the gate at `88b8c632` does the same.

**The defect, read at 94d7b2e0.** `compare_at_base` in
`skills/verify/scripts/broad_gate.py` splits the failing files before any run.
A file is `absent`, and reads `new` with no run, where this branch's working
tree carries the path at the repository root and the base's tree does not
(`os.path.isfile(os.path.join(root, f))` and `git cat-file -e HEAD:<f>` in
the scratch worktree). pytest names a failing file relative to the directory
it was invoked from, and a row `cd sub && bin/test -q` invokes it from `sub/`.
So when the branch adds a *different* file at `tests/test_two.py` under the
root, while the base fails `sub/tests/test_two.py`, the root check finds the
root file, the base tree lacks it at the root, and `tests/test_two.py` reads
`new` with no `suite-at-base-*.txt` kept. The word reads as measured and
nothing measured it. That is the class #747 exists to close.

**Re-framed 2026-10-04 after phase 1.** The first frame removed the root split
and read absence off pytest's `file or directory not found` reply. Phase 1
measured that under `pytest-xdist` no such reply is printed, and that one
missing path stops every other file of the run (`phases/phase-1.md`). This
repository's own row runs xdist (`bin/test` passes `-n auto`), so that design
would have turned its measured words into `new?`. The orchestrator answered
`questions.md` Q4 with the shape below, and this frame draws it.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `agents/sealer.md` §*Boundaries* — "`new` and `failing on base too` are the gate's words: it re-ran the failing files at the base to earn them" | The promise this work makes literally true. Today a file the root check calls absent reads `new` without being re-run at all, so the sentence is false for that file. After this work every `new` comes from a run at the base |
| `skills/verify/scripts/broad_gate.py#compare_at_base` docstring — "measured — never inferred"; #758's `spec.md` Scope 3, "A word is given only from a run that measured it" | The rule the fix is held to. Absence inferred from the root's tree is an inference; a run at the base, invoked as the row invokes it, that collects nothing for the file is a measurement |
| `phases/phase-1.md` (commit 95ac24fa) | The measured facts the shape rests on: plain pytest prints `ERROR: file or directory not found: <arg>` and `no tests ran in <t>s` and exits 4; under `-n 2`, `-n auto` and this repository's `bin/test -q` the run prints `no tests ran in <t>s`, exits 5, prints no not-found text, and runs none of the other files either |
| `questions.md` Q4, answered by the orchestrator 2026-10-04 | Keep the root split as a pre-filter that decides nothing; confirm each candidate with a run at the base on that file alone |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides against the syntactic fix the issue offers and against a config row: a measured word sends no reader to the base by hand (`skills/verify/SKILL.md` §*The broad gate*, the **New?** bullet; `agents/smith.md` three-returns paragraph) |
| #758 round 2, `rounds/round-2-report.md` §*Round 1's verdicts, answered*, Finding 2 | Precedent for the same choice one shape over: the fix pass ran a `cd` file at the base instead of reporting it `new?` unrun, judged sound because it "measures at least what the proposal would have measured, and it never gives a word the proposal would have withheld" |
| `templates/config.md` §*Broad gate* §*Choosing a value — the criterion*, rule 3 | The one home of what the comparison costs a row and which rows it cannot measure. The solo run's cost and the two limits (Scope 7) are stated there and nowhere else |
| `skills/verify/SKILL.md` §*The broad gate* (the three words); `agents/sealer.md`; `agents/smith.md`; `README.md`, `README.ko.md` | Every place a reader learns what the words mean. Their meanings do not change, so none of them is edited; read at 94d7b2e0 to confirm none describes the root check |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A case seen red, a stated failure direction, a prompt budget, platform honesty — answered in `plan.md` §*Operational impact* |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Enumerate the class (below); pin changed text in the same commit; see every new case red |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from`; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | `seal/releases/0.18.1.md` rows B3 and `Corrected · S5` both state the root split ("a failing file reads `new` unrun only where this branch's root carries its path and the base does not"; "the ones this branch's root carries and the base does not read `new` without a run"). Both become false; their corrections are `Corrected ·` rows in `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`, never edits to the released file |

## The class, enumerated by construction

The defect is not "a `cd` part". It is: **the directory a failing path is
relative to is pytest's invocation directory, and the gate decided absence in
a different directory.** Read in pytest 9.1.1: the short-summary line names a
file through `Config.cwd_relative_nodeid` (`_pytest/config/__init__.py`),
relative to `invocation_params.dir`, and `resolve_collection_argument` · NAME NOT IN TREE
(`_pytest/main.py`) resolves an appended argument against the same directory.
So a run at the base, of the row as written, with the file appended, asks the
right directory whatever moved it.

What changes is which files get such a run. The root split stays, and it now
only **nominates**: a failing file whose path the base's tree lacks at the
root is a candidate, and a candidate is decided by a run on it alone. The
directions, by what the base carries at the root and where the row's runner
runs:

| Base's root carries the path | Where pytest runs at the base carries it | Today (94d7b2e0) | After this work |
|---|---|---|---|
| no | no (a truly new module, any row) | `new` unrun where the branch's root carries the path; otherwise run with the others, and the whole run reads `new?` | candidate → solo run collects nothing → `new`, measured |
| no | yes (`cd sub`, `make -C`, a runner script that changes directory) | `new` unrun where the branch's root carries the path (#761); otherwise run with the others | candidate → solo run measures it → the run's word |
| yes | yes (a root-run row, the common case) | run with the others, measured | unchanged |
| yes | no (a `cd` row whose base carries a same-named file at the root but not below the `cd`) | run with the others; pytest finds nothing; the whole run reads `new?` | unchanged — a named limit (Scope 7). Honest, never counterfeit |

The last row is the direction the pre-filter never nominates. It costs that
run's files their measurement and fakes no word, because nothing in that run
prints a summary.

## Scope

### In

1. **The root split nominates and decides nothing.** A failing file whose
   path `git cat-file -e HEAD:<f>` does not find in the scratch worktree is a
   **candidate**. The branch-root condition
   (`os.path.isfile(os.path.join(root, f))`) is dropped: with every
   candidate confirmed by a run, it no longer guards anything, and dropping it
   is what lets the `cd` file both roots lack (S2) be measured rather than
   cost its run-mates theirs. No file reads any word from the split alone.
2. **Each candidate is run alone at the base.** The prefixes `row_prefixes`
   returns are walked as the existing loop walks them, with that one file
   appended, and the first prefix whose output settles it decides:
   - a line `PYTEST_SUMMARY_RE` reads → the file is present where pytest runs,
     and `verdicts_at_base` reads that run, as for any file
     (`failing on base too`, `new`, or `new?` with `STOPPED_EARLY`);
   - pytest's nothing-collected line, `no tests ran in <t>s` alone on a line
     (with or without `=` rules around it, as `PYTEST_SUMMARY_RE` allows), and
     an exit code of 4 or 5 → the base, run as the row runs it, ran nothing
     of this file → `new`, measured. Plain pytest prints that line beside its
     not-found reply and exits 4; under xdist it is the only trace and the
     exit is 5 (`phases/phase-1.md`, runs 1–5 and 10–11, and the `bin/test`
     run);
   - neither, at any prefix (a crash, a lint part failing first at the base,
     a runner that is not pytest) → `new?` with `NO_RUNNER`.
3. **Every other failing file goes through the existing comparison
   unchanged**: one run per prefix with all of them appended, stopping at the
   first summary, read by `verdicts_at_base`. With no candidate left in it,
   no missing path can stop it.
4. **Order.** The non-candidates' run first, then each candidate in the
   failing files' first-seen order. Every run, solo or not, is a `run(...)`
   call written in `compare_at_base`'s own body, so
   `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
   holds unchanged.
5. **Each run is kept.** The non-candidates' runs are kept as
   `suite-at-base-<k>.txt`, as today. The *n*-th candidate's run at prefix
   *k* is kept as `suite-at-base-<k>-<n>.txt`. `NO_RUNNER`'s parenthesis is
   reworded from "each part tried is kept as suite-at-base-<k>.txt" to name
   both forms, and its whole-text pin in
   `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_unmeasured_word_says_so_and_every_reader_is_told_it`
   moves with it (§14).
6. **Unchanged:** `row_prefixes`, `verdicts_at_base`, every regex beside it,
   `STOPPED_EARLY`, the checkout-failure word, and the signature and return
   shape of `compare_at_base`.
7. **What a person reads changes, and is documented and pinned in the same
   commit (§14):**
   - `templates/config.md` rule 3 gains three sentences, pinned: a failing
     file the base does not carry at the repository root is run alone at the
     base, which costs one run of each prefix up to and including the runner
     per such file, only when the broad gate failed; a file that run collects
     nothing from reads `new`, so a base file with no tests in it reads `new`
     (true of the word — the base cannot fail a test it does not have); and a
     row that runs its tests below a directory where the base carries a
     same-named file at the root reads `new?` for that run's files.
   - `compare_at_base`'s docstring and the comment above the split: the
     paragraph *The absent ones are separated before the run rather than
     after it* and the round-1 🟡 2 comment become the rule of Scope 1–3.
   - The docstring of
     `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict`
     says the absent file is now confirmed by a solo run; its assertions are
     unchanged.
   - `skills/verify/SKILL.md`, `agents/sealer.md`, `agents/smith.md` and the
     READMEs are not edited: the three words and their meanings do not
     change. The module docstring's paragraph *On a failing test the
     comparison against the base is reactive and mechanical* is edited only
     if a sentence in it is made false.

### Out, and why

| Left out | Why | Who answers |
|---|---|---|
| The issue's syntactic fix (a row that changes directory makes every unnamed file `new?`) | Misses `make -C`, `env -C`, `pnpm --dir` and a runner script that changes directory itself, and weakens every measurable `cd` row. `plan.md` §*Alternatives considered* | decided here, from the tree |
| The direction the pre-filter never nominates (last row of the class table) | Honest `new?`, never counterfeit; closing it needs a solo fallback on any run that collects nothing, which is mechanism for a shape nobody has reported. `plan.md` Alternatives, G | the repository owner, if it is ever met — a new issue |
| `--pyargs` rows | Their missing argument reads `module or package not found`; a solo run still prints `no tests ran` and exits 4, so the candidate reads `new` as for any row. No case for it | nobody needs to |
| A runner whose directory change differs between the base's copy and the branch's copy (the branch edits `bin/test`) | The comparison runs the row *at the base*, with the base's scripts, by design since #747 | nobody — inherent to "the row at the base" |
| `( … )` and `{ …; }` groups | Unchanged from #758's outcome table: not reached as a prefix, `new?` | — |
| A failing file the branch reports only as `ERROR` (no `FAILED` line) gets no base comparison | #758's *Out* row, still open and unrelated to where absence is decided | the repository owner, as #758 left it |
| Reordering this repository's `Broad gate` row | The owner chose lint-first in #634; the solo run's cost is stated in rule 3, where the order is already called the repository's trade | the repository owner, already answered |

## User scenarios & acceptance *(mandatory)*

Every gate case lives in `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
built with its `base_then_feature`, `SUITE_ROW`, `verdict_of` and the kept
directory `run_gate(repo, keep=…)` already gives. "Under xdist" means the
row's pytest call carries `-n 2`; a case that needs it skips where the
fixture's interpreter lacks `xdist`, and says so in its skip reason.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | #761 itself, plain | Given the row `cd sub && {SUITE_ROW}`, the base failing `sub/tests/test_two.py`, and the branch still failing it while adding a passing, different `tests/test_two.py` at the root; when `broad-gate` runs; then `tests/test_two.py` reads exactly `failing on base too`, and its solo run is kept | executed — new case; **seen red against 94d7b2e0**, where it reads `new` and keeps no base run (§15) |
| S1x | #761 itself, under xdist | S1 with `-n 2` in the row | executed — new case; seen red against 94d7b2e0 (`new`, unrun) |
| S2 | A shared and a branch-new file under one `cd` | Given the row `cd sub && {SUITE_ROW}`, the base failing `sub/tests/test_two.py`, and the branch also adding a failing `sub/tests/test_three.py`; then `tests/test_two.py` reads `failing on base too` and `tests/test_three.py` reads exactly `new` — plain and under xdist | executed — new case, parametrised; seen red against 94d7b2e0, where both read `new?` |
| S3 | A root-run xdist row (the shape of `bin/test -q`) with a truly new module | Given a runner-first root row under xdist, the base failing `tests/test_two.py`, and the branch adding a failing `tests/test_three.py`; then `tests/test_two.py` reads `failing on base too` and `tests/test_three.py` reads exactly `new`, and the kept runs are `suite-at-base-1.txt` and `suite-at-base-1-1.txt` | executed — new case; the words already hold at 94d7b2e0 (`new` there is unrun), so it is seen red on the kept-file assertion (no solo run kept there) |
| S4 | A candidate whose solo run crashes | Given the S1 shape where the base's `sub/tests/test_two.py` ends the process at import (`os._exit(3)` at module level), plain pytest; then `tests/test_two.py` reads exactly `NO_RUNNER` (`new?`) | executed — new case; seen red against 94d7b2e0, where it reads `new` unrun |
| S5 | The nothing-collected reading | A unit over the reading, fed the outputs `phases/phase-1.md` recorded verbatim (plain run 1, xdist run 2, the decorated run 7) and their exit codes: each reads as nothing collected; `no tests ran in 0.21s` with exit 0 or 1 does not; `1 failed in 0.22s` does not; `no tests ran` inside a longer line does not | executed — unit rows; each mutation of the reading (the end anchor, the exit-code condition, the `=` rule handling) turns a row red |
| S6 | The existing cases hold | `test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict`, `test_a_file_named_below_a_cd_is_run_at_the_base_and_not_called_new`, `test_a_runner_first_row_runs_once_at_the_base`, `test_a_row_is_cut_at_the_semicolon_its_shell_reads`, `test_a_lint_first_row_finds_a_failure_the_base_shares`, the `MEASURED_ENDINGS` and `SUMMARY_LINES` rows, and the one-shell-site case pass with unchanged assertions | executed — those cases, by module |
| S7 | The cost and limits are documented where the row's author reads them | Rule 3 carries Scope 7's three sentences, and `NO_RUNNER`'s reworded parenthesis is pinned whole | executed — the pins, each seen red with its sentence deleted |

## Data & interfaces

- `compare_at_base(root, base, command, files, keep)` — signature and return
  shape (`{file: word}`) unchanged.
- One new module-level reading beside `PYTEST_SUMMARY_RE`: pytest's
  nothing-collected line, `no tests ran in <t>s`, alone on a line and
  optionally ruled with `=`, read together with the run's exit code (4 or 5).
  A pure function of `(text, exit code)`, so S5 needs no repository.
- Kept outputs: `suite-at-base-<k>.txt` for the non-candidates' run;
  `suite-at-base-<k>-<n>.txt` for the *n*-th candidate's run at prefix *k*.
- `NO_RUNNER`'s parenthesis reworded to name both kept forms.
- No new I/O beyond what `run` already does, which names `encoding="utf-8"`
  (sibling A, #762, walks every file I/O call).
- Ledger: new rows in
  `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`;
  `Corrected ·` rows for `seal/releases/0.18.1.md` B3 and `Corrected · S5`;
  a re-read through `evidence-check --reverify --into <that fragment>` for
  every other released row whose coordinate this change drifts (Q2).
- Changelog fragment:
  `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/changelog.md`.

## Open questions → questions.md

`questions.md` beside this file. Q1 and Q4 are closed; Q2 is a measurement
and Q3 a row for the work, each with the default the build uses. No row is
left for a person.

Framed 2026-10-04 by framer, before the build.
