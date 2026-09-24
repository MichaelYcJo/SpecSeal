# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | df91d9e6 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#510. First, Q2's probe: `gh auth status` with `GH_CONFIG_DIR` set to an
empty directory, on the builder's logged-in machine, with the result written
here. Then the `tests/conftest.py` block: an empty `GH_CONFIG_DIR` removed at
exit, and the four token variables removed, with Q2's fallback used only if
the probe showed the block was not enough. One passage in `CONTRIBUTING.md`
§*Running the checks* says the suite runs with `gh` logged out, and why.
Q3's grep for child processes whose environment is built from nothing, with
each one found either fixed or named. The static list of the cases that
reach `gh` is written here. The drifted `CONTRIBUTING.md` rows are re-read and
re-stamped, and the ledger row for A6 and the whole work item's
`changelog.md` are written.

## What this phase found

- **Q2: the block is enough, and the fallback was not written.** Measured on
  2026-09-25 at `6cc67d0b`, before the block existed, with `gh` 2.100.0 at
  `/opt/homebrew/bin/gh` logged in through `hosts.yml` under the default
  config directory. `gh auth status` exited 0. With `GH_CONFIG_DIR` set to
  an empty directory and the four token variables unset, it exited 1 and
  printed "You are not logged into any GitHub hosts. To log in, run: gh auth
  login". `gh` wrote nothing into the empty directory. No token variable was
  set in the session's environment, so the probe tested the config-directory
  half on a real login and the token half only by construction. The
  structural case covers the token half on any machine.
- **Q3: no child escapes the scrub.** Every mapping built for `env=` in
  `tests/` spreads `os.environ` (`dict(os.environ)`, `{**os.environ, …}`, or
  a comprehension over `os.environ.items()`), or goes to an in-process
  function rather than a child. The two in-process ones are
  `issue_claims_check.main(env={})`, which reads `PR_BODY` from the mapping
  and starts nothing, and `test_lint_python.py`'s `_ran(…, env=…)`, which
  sets variables through `monkeypatch`. The two `subprocess.Popen` calls
  (`test_lease_liveness.py`, `test_worktree_guard_signals.py`) pass no
  `env=` and so inherit `os.environ`. This was a grep read, so a wrapper
  that assembles an environment through a name it does not show would
  escape it.
- **The cases that reach `gh`, statically (read 2026-09-25).** Shipped code
  that runs `gh` is in eight files and nine callers:
  `skills/verify/scripts/session_cost.py#run_gh`,
  `skills/code-review/scripts/round_record.py#pull_request_cell` and
  `#pull_request_is_ready` (both behind `which("gh")`), and
  `.github/scripts/` `tracker_labels`, `roll_flow_measurement_issue`,
  `publish_release_note`, `release_completeness_check`,
  `label_merged_on_release_branch` and `close_issues_on_release`. Apart from
  this phase's own module, eight test modules name `gh`, and each stubs it
  through the script's `run` seam or through `which`/`run` parameters.
  None stubs it through `PATH`: `test_the_record_is_generated`,
  `test_release_hygiene`, `test_a_merged_ticket_says_so_on_the_tracker`,
  `test_a_release_rolls_the_flow_measurement_issue`,
  `test_the_closer_carries_on_past_a_refusal`,
  `test_a_release_publishes_its_note`,
  `test_a_declared_label_reaches_the_tracker` and
  `test_a_release_cannot_ship_an_untrue_milestone`. The eight and the three
  modules that drive `session_cost.py#run_gh` (`test_session_cost`,
  `test_session_cost_post`, `test_a_segment_feeds_the_flow_log`) all
  passed under the block, so none of them reaches a live `gh` today. The
  whole-tree answer is the sealer's run and the three CI legs.
- **The structural case runs the conftest in a child.** When the conftest
  is imported, the test's own environment has already been scrubbed, so a
  test cannot see the scrub by reading `os.environ`. The case instead runs
  `tests/conftest.py` through `runpy` in a child whose environment carries
  all four tokens and a `GH_CONFIG_DIR` holding a `hosts.yml`, and reads
  what is left. That makes it red on any machine when any line of the block
  goes. The line that removes the directory at exit is held too: the case
  checks that the directory is gone after the child exits.
- **One mutation left leavings.** With the cleanup line dropped, every xdist
  worker of that run left an empty `specseal-empty-gh-config-*` directory in
  the system temp directory, 12 in all. They were removed after the run. The
  case that turned red is the one that now holds that line.
- **Seen red (§15).** Mutated at `fb340ce0` from a script that restored the
  file from the bytes it read. Removing the whole block, which is the code
  before this phase, turned both cases red, and one of them was the
  behavioural `gh auth status` case on this logged-in machine. Not pointing
  `GH_CONFIG_DIR` turned 2 red. Leaving the tokens, dropping one token from
  the list, and dropping the cleanup each turned 1 red. The `CONTRIBUTING.md`
  case went red with the paragraph's lead sentence cut.
- **Four rows drifted, as the spec named:** `seal/releases/0.10.0.md` S1,
  `0.15.1.md` P3, and `0.8.2.md` R3 and R4. The new paragraph states no
  figure, no version and no rule those claims read, so each holds, and each
  carries a dated `Re-read` note. Three had two or three dates in `Checked`,
  and each now holds the one date of this reading.
- **Verified by (executed, 2026-09-25):** the new module, the eight modules
  that name `gh`, the three that drive `run_gh`, and every module that reads
  `CONTRIBUTING.md`, a ledger file, a changelog fragment, a `questions.md`,
  `conftest.py` or a document the earlier phases edited. That was 58 modules
  in one `bin/test` call: 2749 passed. The whole suite is `unverified`, and
  the sealer answers it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
