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

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `agents/sealer.md` §*Boundaries* — "`new` and `failing on base too` are the gate's words: it re-ran the failing files at the base to earn them" | The promise this work makes literally true. Today a file the root check calls absent reads `new` without being re-run at all, so the sentence is false for that file. After this work every `new` comes from a run at the base |
| `skills/verify/scripts/broad_gate.py#compare_at_base` docstring — "measured — never inferred"; #758's `spec.md` Scope 3, "A word is given only from a run that measured it" | The rule the fix is held to. Absence inferred from the root's tree is an inference; absence reported by pytest at the base, from the directory the row runs it in, is a measurement |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides between the issue's two fixes. Both stop nobody. The weaker verdict (`new?`) sends a reader to run the file at the base by hand (`skills/verify/SKILL.md` §*The broad gate*, the **New?** bullet; `agents/smith.md` three-returns paragraph); a measured word does not. A config row naming the row's directory is rejected on the same ground, as #758 rejected one naming the runner |
| #758 round 2, `rounds/round-2-report.md` §*Round 1's verdicts, answered*, Finding 2 | Precedent for the same choice one shape over: round 1 proposed `new?` for a `cd` row's file; the fix pass ran it at the base instead, and the reviewer judged that sound because it "measures at least what the proposal would have measured, and it never gives a word the proposal would have withheld". This work applies the same judgment to the shape that fix left open |
| `templates/config.md` §*Broad gate* §*Choosing a value — the criterion*, rule 3 | The one home of what the comparison costs a row and which rows it cannot measure. The new cost — one more run of the runner per failing file the base does not carry — is stated there and nowhere else (the section says it is the rules' one home) |
| `skills/verify/SKILL.md` §*The broad gate* (the three words); `agents/sealer.md`; `agents/smith.md`; `README.md`, `README.ko.md` | Every place a reader learns what the words mean. Their meanings do not change, so none of them is edited; read at 94d7b2e0 to confirm none describes the root check |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A case seen red, a stated failure direction, a prompt budget, platform honesty — answered in `plan.md` §*Operational impact* |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Enumerate the class (below); pin changed text in the same commit; see every new case red |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from`; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | `seal/releases/0.18.1.md` rows B3 and `Corrected · S5` both state the root split ("a failing file reads `new` unrun only where this branch's root carries its path and the base does not"; "the ones this branch's root carries and the base does not read `new` without a run"). Both become false; their corrections are `Corrected ·` rows in `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`, never edits to the released file |

## The class, enumerated by construction

The defect is not "a `cd` part". It is: **the directory a failing path is
relative to is pytest's invocation directory, and the gate decided absence in
a different directory.** Read in pytest 9.1.1 (the version this repository's
`.venv` pins): the short-summary line names a file through
`Config.cwd_relative_nodeid` (`_pytest/config/__init__.py`), relative to
`invocation_params.dir`; and `resolve_collection_argument`
(`_pytest/main.py`) resolves an appended argument against the same
`invocation_params.dir`, raising `UsageError("file or directory not found:
<arg>")` for the first one that does not exist. So the branch's `FAILED` line
and the base's argument resolution are relative to one directory, whatever
moved it. The members, each a way that directory differs from the root:

| Member | Caught by a syntactic `cd` test | Caught by asking pytest at the base |
|---|---|---|
| `cd sub && …`, `cd sub; …`, `pushd sub && …` | `cd` yes, `pushd` only if listed | yes |
| `( cd sub && pytest )` group | no (the group is never a prefix) | the group is not reached as a prefix today, so `new?` either way — unchanged |
| `make -C sub test`, `env -C sub pytest`, `pnpm --dir sub test` | no | yes |
| a runner script that changes directory itself (this repository's own `bin/test` runs pytest from the repository root whatever the caller's directory, by its header comment) | no | yes |
| `pytest --rootdir sub …` (rootdir moved, invocation directory not) | no, and needs none | yes — `cwd_relative_nodeid` keeps the path relative to the invocation directory |

A syntactic detector covers the first row and misses the rest. The run at the
base covers every row, because pytest itself is the one asked.

## Scope

### In

1. **Absence is decided by the run at the base, under the row's own
   directory changes, never by the root's tree.** The pre-run split on
   `os.path.isfile(root/f)` and `HEAD:<f>` in the scratch worktree is
   removed. Every failing file is appended to each prefix as the existing
   prefix loop does today.
2. **pytest's own reply is the measurement of absence.** Where a prefix's
   output carries pytest's not-found reply naming exactly one of the files
   appended to it (the text `file or directory not found: <file>`, its full
   line form measured in phase 1 for plain pytest and under `pytest-xdist`,
   `questions.md` Q1), that file reads `new`: pytest, invoked as the row
   invokes it at the base, found no such file there, so the test arrived with
   this branch. The prefix that printed it is the runner — only pytest prints
   that reply — and it is **run again at the same prefix** without that file.
   This repeats until a run carries no such reply or no file is left. Each
   repeat removes one file, so the loop ends after at most one run per file.
3. **A run that carries the not-found reply is never read as a measurement
   for any file**, even where it also carries a line `PYTEST_SUMMARY_RE`
   reads. pytest stops at the first missing argument, so nothing in that run
   says anything about the others. This guards the shape Q1 may find under
   `pytest-xdist`, where a worker's crash could sit beside a summary-like
   line.
4. **Everything else reads as it does today.** The run that finally carries
   no not-found reply is read by `verdicts_at_base`: `failing on base too`
   where a `FAILED` or `ERROR` line names the file, `new` where none does and
   the run did not stop early, `new?` with `STOPPED_EARLY` or `NO_RUNNER`
   otherwise. A re-run at the runner's prefix that prints no summary leaves
   its files `NO_RUNNER`. The prefix loop, `row_prefixes`, the checkout
   failure word and every reason text are unchanged.
5. **Each run is kept.** The first run of prefix *k* is kept as
   `suite-at-base-<k>.txt`, as today. The *m*-th run of the same prefix
   (m = 2, 3, …), after a not-found reply, is kept as
   `suite-at-base-<k>-<m>.txt`. `NO_RUNNER`'s parenthesis, "each part tried
   is kept as suite-at-base-<k>.txt", stays true as written and is not
   reworded.
6. **The reply is matched to the files exactly.** A not-found line naming a
   path that was not appended, or naming a longer path that starts with an
   appended one, drops nothing. The match is the whole argument after
   `not found: `, end of line, compared for equality with each appended file.
7. **Still one shell site.** Every run, including the re-runs, is a `run(...)`
   call written in `compare_at_base`'s own body, so
   `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
   holds unchanged (it requires the callers of `run(..., shell=…)` to be
   exactly `compare_at_base` and `gate`).
8. **What a person reads changes, and is documented and pinned in the same
   commit (§14):**
   - `templates/config.md` rule 3 gains the cost: a failing file the base does
     not carry, where the row runs its tests, is found by pytest's reply at
     the base and costs one more run of the runner, with every part before
     it, per such file. The sentence is pinned.
   - `compare_at_base`'s docstring and the comment above the removed split:
     the paragraph *The absent ones are separated before the run rather than
     after it* becomes the rule of Scope 2–3, and the round-1 🟡 2 comment
     goes with the split it described.
   - The docstring of
     `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict`
     says how the absent file is now found (pytest's reply, then a re-run),
     and its assertions are unchanged.
   - `skills/verify/SKILL.md`, `agents/sealer.md`, `agents/smith.md` and the
     READMEs are not edited: the three words and their meanings do not
     change. The module docstring's paragraph *On a failing test the
     comparison against the base is reactive and mechanical* is read and
     edited only if a sentence in it is made false.

### Out, and why

| Left out | Why | Who answers |
|---|---|---|
| The syntactic alternative the issue names (a row that changes directory makes every unnamed file `new?`) | Misses four of the five members above and weakens every measurable `cd` row's `new`. `plan.md` §*Alternatives considered* | decided here, from the tree |
| `--pyargs` rows, whose missing argument reads `module or package not found: … (missing __init__.py?)` | Read in `resolve_collection_argument`; not matched, so such a run prints no summary and its files read `new?` — honest, and the failing path a `FAILED` line gives is a file path, not a module name, so the row is already a poor fit. No case for it | nobody needs to — the outcome is `new?`, never a counterfeit |
| A runner whose directory change differs between the base's copy and the branch's copy (the branch edits `bin/test`) | The comparison runs the row *at the base*, with the base's scripts, by design since #747; the base's directory is the base's answer | nobody — inherent to "the row at the base" |
| `( … )` and `{ …; }` groups | Unchanged from #758's outcome table: not reached as a prefix, `new?` | — |
| A failing file the branch reports only as `ERROR` (no `FAILED` line) gets no base comparison | #758's *Out* row, still open and unrelated to where absence is decided | the repository owner, as #758 left it |
| Reordering this repository's `Broad gate` row | The owner chose lint-first in #634; the new cost (Scope 8) is stated in rule 3, where the order is already called the repository's trade | the repository owner, already answered |

## User scenarios & acceptance *(mandatory)*

Every gate case lives in `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
built with its `base_then_feature`, `SUITE_ROW`, `verdict_of` and the kept
directory `run_gate(repo, keep=…)` already gives.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | #761 itself | Given the row `cd sub && {SUITE_ROW}`, the base failing `sub/tests/test_two.py`, and the branch still failing it while adding a passing, different `tests/test_two.py` at the root; when `broad-gate` runs; then `tests/test_two.py` reads exactly `failing on base too`, and a `suite-at-base-*.txt` is kept | executed — new case; **seen red against 94d7b2e0**, where it reads `new` and keeps no base run (§15) |
| S2 | A shared and a branch-new file under one `cd` | Given the same row, the base failing `sub/tests/test_two.py`, and the branch also adding a failing `sub/tests/test_three.py`; then `tests/test_two.py` reads `failing on base too` and `tests/test_three.py` reads exactly `new` | executed — new case; seen red against 94d7b2e0, where both read `new?` (#758 round 2's probe table records the same) |
| S3 | A runner-first row and a branch-new file at the root | The existing `test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict`: `tests/test_two.py` reads `failing on base too`, `tests/test_three.py` reads `new`; and the kept runs are exactly `suite-at-base-1.txt` and `suite-at-base-1-2.txt` | executed — the existing case with the kept-file assertion added; the kept-file half seen red against 94d7b2e0, which keeps one |
| S4 | Two branch-new files, nothing else failing | Given a runner-first row and two failing files the base does not carry; then both read `new`, and exactly two runs are kept (`suite-at-base-1.txt`, `suite-at-base-1-2.txt`) — the second run's reply names the second file and nothing is left to run after it | executed — new case; red against 94d7b2e0 on the kept-file count (0 there) |
| S5 | The reply under `pytest-xdist` reads no measured word | The output phase 1 measured for `pytest -n 2` given one present and one missing path (Q1), fed to the reading as a measured-ending row: the missing file is the one dropped, or, if the text is not there, no file of that run reads `new` or `failing on base too` | executed — a row beside `MEASURED_ENDINGS`, its text copied verbatim from the phase-1 record |
| S6 | The reply names only what was appended | A unit over the reading: `file or directory not found: tests/test_two.py.bak` with `tests/test_two.py` appended drops nothing; `… not found: tests/test_two.py` drops exactly that file; a reply naming a file not appended drops nothing | executed — unit case; each mutation of the exact match (substring, prefix, missing end anchor) turns a row red |
| S7 | The existing cases hold | `test_a_file_named_below_a_cd_is_run_at_the_base_and_not_called_new`, `test_a_runner_first_row_runs_once_at_the_base`, `test_a_row_is_cut_at_the_semicolon_its_shell_reads`, `test_a_lint_first_row_finds_a_failure_the_base_shares`, the `MEASURED_ENDINGS` and `SUMMARY_LINES` rows, and the one-shell-site case pass unchanged | executed — those cases, by module |
| S8 | The cost is documented where the row's author reads it | Rule 3 in `templates/config.md` carries the cost sentence of Scope 8, and a case pins it | executed — the pin, seen red with the sentence deleted |

## Data & interfaces

- `compare_at_base(root, base, command, files, keep)` — signature and return
  shape (`{file: word}`) unchanged. The `root` argument stays: it is still
  the clone the scratch worktree is added from and removed through.
- One new module-level reading of pytest's reply, beside `FAILED_RE` and
  `ERROR_RE`: the argument after `file or directory not found: ` to the end
  of its line. Its exact line form is phase 1's measurement (Q1); the text
  is pytest's own (`_pytest/main.py`, `resolve_collection_argument`).
- Kept outputs: `suite-at-base-<k>.txt`, then `suite-at-base-<k>-<m>.txt`
  for the m-th run of the same prefix.
- No new I/O beyond what `run` already does, which names
  `encoding="utf-8"` (sibling A, #762, walks every file I/O call).
- Ledger: new rows in
  `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`;
  `Corrected ·` rows for `seal/releases/0.18.1.md` B3 and `Corrected · S5`;
  a re-read through `evidence-check --reverify --into <that fragment>` for
  every other released row whose coordinate this change drifts (Q2).
- Changelog fragment:
  `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/changelog.md`.

## Open questions → questions.md

`questions.md` beside this file. It holds no row for a person: the issue's
open choice was decided from the tree above. What it holds are two
measurements and one row for the work, each with the default the build uses.

Framed 2026-10-04 by framer, before the build.
