# Implementation Plan: the broad gate hands cmd.exe a forward slash, and a case reaches a live gh (#448, #510)

<!-- seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/plan.md -->

Approved 2026-09-24 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

There are three vertical slices. Phases 1 and 2 are #448. Phase 1 rewrites
the command words of the string `run` hands to `cmd.exe`, so that
`bin/test` runs as `bin\test` and resolves to `bin/test.cmd`. Phase 2 makes
the failure form say when the failing row's output carries no pytest
summary, so "the suite did not report" stops looking like "the suite
failed". Phase 3 is #510. The suite's own environment loses `gh`'s
credentials at conftest import, so a case that reaches a live `gh` fails on
a developer's machine the same way it fails on CI. That also makes the
sealer's one broad run the whole-tree enumeration of such cases.

## Technical context

- `skills/verify/scripts/broad_gate.py#run` is the one
  `subprocess.run(..., shell=shell)` in shipped code. `grep shell=True` over
  `skills/ hooks/ .github/ bin/` found nothing else (read 2026-09-24). Its two
  `shell=True` callers are `gate` (`checks[SUITE] = run(SUITE, command, root,
  keep, shell=True)`) and `compare_at_base` (`run("suite-at-base", runner,
  scratch, keep, shell=True)`, where `runner` is `first_command(row)` plus
  paths from `quote`).
- On Windows, Python builds `"{COMSPEC} /c \"{args}\""` with `COMSPEC`
  defaulting to `cmd.exe`. The rewrite is therefore keyed on *Windows and the
  basename of `COMSPEC` (or its absence) is `cmd.exe`*, and not on `os.name`
  alone. `tests/conftest.py#posix_row_shell_or_skip` already names a Windows
  machine whose `COMSPEC` is a POSIX shell.
- `broad_gate.py#quote(path, windows=None)` is the pattern to copy: the
  platform is an argument so both branches can be driven from macOS. Its
  docstring records why reading `os.name` in the body made #103's class. The
  new function takes `windows=None, comspec=None` the same way.
- `cmd.exe`'s lexer, the part the rewrite needs: quoting is `"` only, `^`
  escapes the next character outside quotes, and command separators are
  `&&`, `||`, `&`, `|`, and `(` opens a block. A command word runs from the
  first non-blank, non-`@` character in command position to the first
  unquoted blank, `<`, `>`, `&`, `|`, `(` or `)`. The rewrite changes `/` to
  `\` inside that span and nothing outside it. It is a position scan over
  the original string. It never tokenises and re-renders, because
  re-rendering is how quoting gets lost. `hooks/cmdline.py` is a POSIX
  `shlex` reader for the harness's bash. It is not reused: it reads the
  wrong shell and returns tokens, not positions.
- `broad_gate.py#suite_counts` returns pytest's counts, or `None` when no
  summary line with a wall clock is present. `failure_lines` already appends
  the counts when there are some. Phase 2's line is the `None` branch of that
  same read for `SUITE`.
- `tests/conftest.py` already changes `os.environ` at import for the same
  kind of reason (`SPECSEAL_LANG`, `GIT_TEMPLATE_DIR`, `GIT_CONFIG_*`). Each
  xdist worker imports conftest, and every child that inherits `os.environ`
  receives the change. The `gh` block goes beside those.
- The eight test modules that mention `gh` stub it in-process through the
  script's `run` seam or through `which`/`run` parameters. None of them stubs
  through `PATH` (read 2026-09-24), so a scrubbed environment cannot collide
  with a stub.

**The chosen approach's failure scenario, six months out:**

- **#448.** A row puts a path-bearing word in a position the scan does not
  treat as a command: after `call`, `start` or `if … `. `cmd.exe` then splits
  it exactly as it does today. The gate is no worse than now, and Phase 2's
  line makes the failure readable. `templates/config.md` names the positions
  that are rewritten, so the gap is written down.
- **#510.** A future `gh` release could read its keyring token without
  looking at `GH_CONFIG_DIR`. The structural case stays green while
  `gh auth status` goes red on an authenticated machine. The behavioural case
  exists for exactly that, and Q2 measures today's behaviour before the
  block is written.

## Alternatives considered

| # | Approach | Failure scenario | Verdict |
|---|---|---|---|
| 1 | #448: run the row through a POSIX `sh` on Windows where one is found | There is no reliable way to find `sh`. `shutil.which("bash")` on `windows-latest` is the WSL launcher (`conftest.py#shell_probe`'s docstring). Git for Windows' default install puts only `Git\cmd` on `PATH`, so on the machine #448 came from there is probably no `sh` at all. Under `sh`, `bin/test` is the POSIX wrapper, which runs `exec python3`, and on Windows `python3` can be the Store alias. The repository built `bin/test.cmd` so that `cmd.exe` would not have to take that route. The change also alters the meaning of any row a Windows user wrote in `cmd` syntax, and it rewrites `templates/config.md`'s two-shell account | Rejected. The tree already answers it: the `.cmd` sibling is how this repository calls its runner on Windows |
| 2 | #448: refuse, with exit 2, a command word containing `/` when the shell is `cmd.exe` | It refuses a row that is correct. The only rewrite that passes, `bin\test`, breaks the row on POSIX and on CI's bash. The row belongs to a person (#401), and the refusal would send that person to break it | Rejected |
| 3 | #448: rewrite `/` to `\` in command words only, and only for `cmd.exe`, inside `run` | See *failure scenario* above. The scan has to model `cmd.exe`'s quoting and `^`. If it gets one wrong, the effect is limited to a `/` that did not change, or a `\` placed inside a word `cmd.exe` would have split anyway | **Chosen** |
| 4 | #448: detect "nothing ran" from the exit code (`sh` 126/127, `cmd.exe` 9009) and refuse | #448 measured exit **1** for this exact case through `cmd /c`, with a localised message, so the exit code cannot separate it from pytest's 1. Under `sh`, a 127 from a missing `uvx` after the tests passed would falsely say "nothing ran". It would also add a fourth exit state to a contract `agents/sealer.md` reads | Rejected. Phase 2 reads what is actually missing, the summary, and works on either shell and in any locale |
| 5 | #510: a CI leg with `gh` removed from `PATH` | CI is already unauthenticated, so the leg asks a question CI already answers. The blind spot is on the local side | Rejected |
| 6 | #510: an arm in `broad_gate.py` that runs the row a second time with `gh` unreachable | It costs a second full suite on every seal: 3m04s parallel as measured in `docs/the-broad-gate.md`, and about 13 minutes serial. It also puts a policy on every plugin user's row, when a user's suite may call `gh` on purpose. The row is the repository's own claim | Rejected |
| 7 | #510: a failing `gh` shim first on `PATH` | On Windows, `CreateProcess` resolves a bare `gh` only to an `.exe`, so a `.cmd` or `sh` shim is never reached there. Removing `gh`'s directory from `PATH` takes `git`, `uv` and `python` with it on Homebrew layouts | Rejected |
| 8 | #510: an autouse fixture that patches `subprocess.run`/`Popen` to refuse argv `gh` | Most gates are tested by running the script as a child process, and a patch in the parent does not reach the child. The class would be closed only for in-process calls | Rejected as the mechanism. It would be a second mechanism for a subset of the class |
| 9 | #510: remove `gh`'s credentials from `os.environ` at conftest import | A case that starts a child with an environment built from nothing escapes (Q3). A `gh` that finds its keyring token without `GH_CONFIG_DIR` escapes (Q2) | **Chosen**. It covers in-process calls and children on all three platforms, needs no second run, and makes local runs match CI |

## Phases

Vertical slices, each ending runnable and verified. The narrow runs below are
the smith's. The whole suite, lint and format are the sealer's single
`broad-gate` run after the rounds settle (contract §2), and the build hands
over with the suite labelled `unverified` and the sealer named as its
answerer.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #448, the rewrite. A pure function (for example `handed_to_shell(command, windows=None, comspec=None)`) turns `/` into `\` in `cmd.exe` command words. `run` applies it when `shell=True`, keeps both lines in `<name>.txt`, and prints one stderr line when they differ. `gate`, `compare_at_base`, `first_command` and `quote` are left unedited. `templates/config.md` §*Broad gate* gets one paragraph: which shell runs the row on Windows, what it is handed, which positions are rewritten, and that nothing else is rewritten. The drifted rows citing `templates/config.md#"## Broad gate"` (`seal/releases/0.10.0.md` S4, `seal/releases/0.12.0.md`) are re-read and re-stamped where they live. The ledger fragment rows for A1–A4 are written | Scenarios A1, A2, A3 and A4 in a new module (suggested: `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`), run as `bin/test tests/<that module> -q` together with `tests/test_the_seal_is_taken_once_by_the_sealer.py -q` (the gate's existing module, since `run` sits under every one of its cases) and `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py -q`. Seen red: the rewrite returning its input makes A1/A2 red with `windows=True` on macOS, and dropping the call from `run` makes A2's structural half and A3 red. A4's Windows red is #448's measurement, not a run in this work item. After the template edit, run `evidence-check --reverify` on the two drifted rows | b75b05ad |
| 2 | #448, the report. `failure_lines` adds one line for `SUITE` when the check failed and `suite_counts` is `None`: the output carries no pytest summary, so this is not a count of failing tests. The exit code stays 1, and the panel and `gate` are untouched. The sentence is pinned verbatim (§14), and `agents/sealer.md` is checked for any wording about reading the failure form that the new line would contradict | A5: a unit case on `failure_lines` with a hand-built `Check`, both branches, and one end-to-end gate run with the row `exit 1` (the same under `sh` and `cmd.exe`, so it runs on all three legs). `bin/test tests/<phase 1's module> -q`. Seen red: delete the line and A5 goes red. The summary-present branch is shown not to fire by a row `echo 1 failed in 0.01s && exit 1` | |
| 3 | #510. First, Q2's probe: `gh auth status` with `GH_CONFIG_DIR` set to an empty temporary directory, on the builder's authenticated machine, with the result written into `phases/phase-3.md`. Then the `tests/conftest.py` block: an empty `GH_CONFIG_DIR` removed at exit, and the four token variables popped. If Q2 shows that is not enough, the fallback it names is used. One sentence in `CONTRIBUTING.md` §*Running the checks* says the suite runs with `gh` unauthenticated, and why. Q3's grep for child processes whose environment is built from nothing, with each one found either fixed or named. The static enumeration (nine callers, eight stubbing modules) is written into `phases/phase-3.md`. The drifted `CONTRIBUTING.md#"## Running the checks"` rows (`0.10.0.md`, `0.15.1.md`, `0.8.2.md` ×2) are re-read and re-stamped. The ledger fragment rows for A6 and the `changelog.md` entry for the whole work item are written | A6: the structural case (red on any machine when the block is deleted) and the behavioural `gh auth status` case (seen red on the builder's authenticated machine with the block deleted, with that run recorded in `phases/phase-3.md`). Narrow runs: `bin/test` over the new case's module plus the eight modules that mention `gh` plus the three that drive `session_cost.py#run_gh` (`tests/test_session_cost.py`, `tests/test_session_cost_post.py`, `tests/test_a_segment_feeds_the_flow_log.py`), each named explicitly. That is the phase boundary's "module and the ones it touches". The 28 modules that go through `round_record.py` reach `pull_request_cell` only behind `which("gh")`, and in a fixture repository with no GitHub remote. They are left to the sealer's run rather than sliced. The whole-tree answer to "which case reaches `gh`" is the sealer's run and the three CI legs, labelled `unverified` with those two named as answerers | |

This table is also where the work records how far it got. There is no
separate task list: a list of tasks is mutable progress, and a stale one
asserts a state that is not true, which is the failure the evidence ledger
exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
that someone can open.

What a phase discovers while it is being built, and the next phase needs to
know, goes in `phases/phase-N.md` from `templates/sdd-phase.md` when the
phase closes. After any rebase, re-read this column.

## Where each claim is executed

| Claim | Executed on this macOS machine | Executed only on CI's `windows-latest` at the pull request |
|---|---|---|
| The rewrite's output for `cmd.exe` (A1, A2) | yes, with `windows=True` and `comspec` passed in | also, with the real platform |
| `run` applies it and records both lines (A3) | yes, with the platform forced and `subprocess.run` stubbed | also |
| `cmd.exe` actually runs `bin\probe` → `bin\probe.cmd` (A4) | no. On macOS the same case runs `bin/probe` through `sh` | **yes, and only there** |
| No-summary line (A5) | yes. The row `exit 1` reads the same in both shells | also |
| Scrubbed `gh` (A6) | yes, and it can be seen red only here, where `gh` is authenticated | runs; it cannot go red on CI because CI is unauthenticated either way |
| No case in the tree reaches a live `gh` | no (contract §2) | the three legs, and before them the sealer's run |

## Operational impact

- There are no new dependencies, environment variables for users, or
  migrations.
- On Windows, a plugin user's row whose command words contain `/` is now
  handed to `cmd.exe` with `\`. Before this change such a row could not run
  on `cmd.exe` at all, so no row that works today changes behaviour.
- Contributors running the suite with `gh` authenticated now get CI's answer
  for any case that reaches `gh`. That is the intended new red, and
  `CONTRIBUTING.md` says why.
- The PR body carries `CONTRIBUTING.md` §*What a change to a gate must carry*
  for both fixes. The prompt budget is 0 for both: nothing asks anyone
  anything.
