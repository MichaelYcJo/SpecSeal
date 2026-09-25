# Feature Specification: the broad gate hands cmd.exe a forward slash, and a case reaches a live gh (#448, #510)

<!-- seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md -->

Two defects in one instrument, the sealer's one broad run. Each one makes the
run say something other than what happened.

- **#448.** `broad_gate.run(..., shell=True)` hands the `Broad gate` row to
  `%COMSPEC%`. On Windows that is `cmd.exe`, and `cmd.exe` splits a command
  name at a forward slash. `bin/test -q && …` therefore runs a command called
  `bin` with the argument `/test`. The shell prints "not recognized" and exits
  1, and the failure form reports that as `suite` failing. A reader can only
  tell the two apart by opening the kept file and seeing it holds no test
  output.
- **#510.** A case that falls through its stubs onto a real `gh` passes on a
  machine where `gh` is authenticated. On CI, where the pytest job has no
  `GH_TOKEN`, the same case fails. The broad gate runs on a maintainer's
  machine, so it cannot see this class at all. CI finds it only after the
  branch has been sealed.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | The fix for each defect has to work with nobody watching. Neither one may add a question for a person. Both are chosen partly for that reason. |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Each fix carries four things: a test seen red, a stated failure direction, a prompt budget and platform honesty. The PR body answers all four for both fixes (A7). |
| `docs/the-broad-gate.md` §*What the gate runs* → *The gate that measures a tree is the copy that tree ships* | The fix lands in `skills/verify/scripts/broad_gate.py`. Because this tree ships the gate, the sealer's run on this branch uses the fixed copy. |
| `templates/config.md` §*Broad gate* (the row's one home) | The row is "one shell command line", and it belongs to a person (#401). The gate must not ask anyone to rewrite a correct row, and must not repair a wrong one quietly. The section already describes what both `/bin/sh` and `cmd.exe` do with a row, so it is where the new sentence about what `cmd.exe` is handed goes. |
| `templates/config.md` §*What is refused* ("The value must run as the command it reads as") | The #448 fix exists to make this criterion true on `cmd.exe`. The row reads as `bin/test`, and it has to run as `bin/test`. |
| `skills/agent-contract/SKILL.md` §12, §13, §14, §15 | §12: the class is enumerated (see *The class, enumerated* below). §13: the Windows half cannot rest on a platform guarantee this macOS machine has, so it is pinned with the platform as an argument. §14: every changed message is documented and pinned in the same commit. §15: every case is seen red. |
| `CLAUDE.md` §*a change writes fragments* and §*Appended is the word* | New rows go in `seal/ledger/1790260567-the-broad-gate-hands-cmd-a-forward-slash.md` and the changelog entry goes in this directory's `changelog.md`. Where this work edits an anchored unit, the existing rows are re-read and re-stamped where they live (see *Data & interfaces*). |

## Scope

**In:**

1. **#448, the command word.** When `run(..., shell=True)` is about to hand a
   string to `cmd.exe`, each command word in it (the word in command position:
   at the start of the line, and after `&&`, `||`, `&`, `|` or `(`) has its
   `/` written as `\`. Nothing else in the string changes. Arguments, quoted
   paths, `%VAR%`, operators and the refused forms stay exactly as written.
   The rewrite lives in `run`, so it reaches both of the module's
   `shell=True` callers: `SUITE` in `gate` and `suite-at-base` in
   `compare_at_base`. The kept output file and one stderr line both say what
   `cmd.exe` was handed, next to the row as written. `templates/config.md`
   §*Broad gate* says so too.
2. **#448, the report.** When the `suite` check fails and its output holds no
   pytest summary line (`suite_counts` returns `None`), the failure form says
   so in one line. The line states what was measured: this is not a count of
   failing tests. Unlike an exit code, this signal does not depend on the
   platform or on the shell's locale.
3. **#510, the suite's environment.** At import, `tests/conftest.py` takes
   away `gh`'s credentials from the suite's own environment. It points
   `GH_CONFIG_DIR` at an empty directory, removes `GITHUB_TOKEN` and
   `GITHUB_ENTERPRISE_TOKEN`, and sets `GH_TOKEN` and `GH_ENTERPRISE_TOKEN`
   to a value no server accepts, so `gh` never falls back to a login kept in
   the OS keyring. **Corrected 2026-09-25** in round 1's fix pass: this item
   said all four were removed, which leaves the keyring login reachable
   (round 1's 🟡 1). A
   case that reaches a live `gh` then fails on a developer's machine the same
   way it fails on CI. That holds for every entry point: `bin/test`, bare
   `pytest`, the `uvx` fallback, xdist workers, and every child process that
   inherits `os.environ`. `CONTRIBUTING.md` §*Running the checks* says so.
4. **#510, the enumeration.** Which cases reach `gh` today, by construction
   and by execution. See *The class, enumerated*.

**Out, each with its reason:**

- **Running the row through a POSIX `sh` on Windows** (#448's first
  candidate). The tree has already answered this: `bin/test.cmd` exists so
  that `cmd.exe` can call the runner, and `templates/config.md` describes
  what each of the two shells does with a row. See `plan.md` Alternatives 1.
- **Refusing a `/` command word on `cmd.exe` with exit 2.** That refuses a
  correct row. The only rewrite that would then pass, `bin\test`, breaks the
  row on POSIX. See `plan.md` Alternatives 2.
- **A new exit code for "nothing ran".** The shell's "not found" exit is not
  distinguishable on `cmd.exe`: #448 measured exit 1 for exactly this case,
  and the message it printed was localised. On `sh`, exit 127 can come from
  a linter that is missing after the tests ran, so it does not mean "nothing
  ran". The gate's exit codes (0/1/2) stay as they are, and Scope 2 is the
  labelling repair. See `plan.md` Alternatives 4.
- **An arm in `broad_gate.py`, or a CI leg, for #510.** The gate runs a
  plugin user's row, and that row may use `gh` on purpose. The row is the
  repository's own claim (`templates/config.md` §*Broad gate*). CI is already
  unauthenticated, so the gap is on the local side, and the local side is
  this repository's conftest. See `plan.md` Alternatives 5 and 6.
- **Other network tools #510 asks about** (`git` against a remote, `uvx`
  fetching, `urllib` in `test_the_plugin_directory_answers_the_box.py`'s
  `fetch`). The class #510 names is *a credential a developer's machine
  holds and a runner does not*. CI has network, so a fetch that needs no
  credential gives the same verdict in both places. A static read (grep for
  `clone`/`fetch`/`ls-remote` and for `git@`/`https://github` in `tests/`)
  found no case that names a remote over the network. That is labelled
  `read`: grep cannot rule out a URL that is built at runtime.
- **`%VAR%` inside a quoted path** (the known hole named in the `quote`
  docstring). It is a different mechanism, and this work does not touch it.
- **A `COMSPEC` that names something other than `cmd.exe`** (PowerShell, or a
  POSIX shell). The rewrite applies only where the shell is `cmd.exe`, and
  anything else is handed the row as written, exactly as today.

## The class, enumerated

**#448: every string this module hands to a shell.** By construction,
`broad_gate.py` has exactly one `subprocess.run` whose `shell` can be true.
It is inside `run` (read 2026-09-24: `grep shell=True` over `skills/`,
`hooks/`, `.github/`, `bin/` finds only `broad_gate.py`). `run` has exactly
two `shell=True` callers: `gate` (`checks[SUITE]`) and `compare_at_base`
(`suite-at-base`, whose runner is `first_command(row)` followed by quoted
test paths). Putting the rewrite in `run` covers both, and a structural case
(A2) holds the count. A third `shell=True` call added outside `run` turns
that case red.

**#510: the cases that reach `gh`.**

- *Code that calls `gh`* (read 2026-09-24, grep for `"gh"` in argv position),
  nine modules: `skills/verify/scripts/session_cost.py#run_gh`,
  `skills/code-review/scripts/round_record.py#pull_request_cell` and
  `#pull_request_is_ready` (both guarded by `which("gh")`),
  `.github/scripts/{tracker_labels, roll_flow_measurement_issue,
  publish_release_note, release_completeness_check,
  label_merged_on_release_branch, close_issues_on_release}.py`.
  `hooks/review-history-guard.py` only parses `gh` text and does not run it.
- *Cases that mention `gh`*, eight modules. They stub by replacing the
  script's own `run` seam in-process, or by passing `which`/`run` as
  parameters: `test_the_record_is_generated`, `test_release_hygiene`,
  `test_a_merged_ticket_says_so_on_the_tracker`,
  `test_a_release_rolls_the_flow_measurement_issue`,
  `test_the_closer_carries_on_past_a_refusal`,
  `test_a_release_publishes_its_note`, `test_a_declared_label_reaches_the_tracker`,
  `test_a_release_cannot_ship_an_untrue_milestone`.
- *By execution*, which is the only complete answer. #510 says that a whole
  suite run with `gh` removed from `PATH` gave `4170 passed, 9 skipped` after
  its repair. That is nobody's finding in this tree: it comes from the ticket
  and is measured on another tree. With Scope 3 in place, **the sealer's one
  broad run is that enumeration**, because any case that reaches a live `gh`
  fails in it. The three CI legs ask the same question again. The build does
  not run the whole suite (contract §2). At the phase-3 boundary it runs
  the eight modules above plus the modules that exercise the nine callers.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | The row's command word reaches `cmd.exe` in a form it can run | Given the platform is Windows and `COMSPEC` names `cmd.exe`, when the row is `bin/test -q && uvx ruff check . && uvx ruff format --check .`, then the string handed to the shell is `bin\test -q && uvx ruff check . && uvx ruff format --check .`. Given the same row on POSIX, or with a `COMSPEC` that is not `cmd.exe`, the string is handed unchanged | Unit case on the rewrite, with the platform and `COMSPEC` as arguments, parametrised over both. It runs on macOS and goes red when the rewrite returns its input unchanged (§13, §15) |
| A2 | Only command words change, and every `shell=True` caller gets the rewrite | Given a row with quoted arguments, `/` in arguments, `%VAR%`, `^&`, `(…)` and every operator, when it is rewritten for `cmd.exe`, then only `/` inside command words changes. A structural case counts the `shell=True` sites in `broad_gate.py` (exactly one `subprocess.run` with a `shell` argument, inside `run`) and checks that `run` applies the rewrite | Parametrised unit case, plus an AST case over the module that is red when a second shell site appears. `compare_at_base`'s runner (`bin/test "tests/x.py"`) is one of the parametrisations |
| A3 | What ran is on record | Given the rewrite changed the string, when the check runs, then the kept `<name>.txt` names both the row as written and the line `cmd.exe` was handed, and one stderr line says the same. Given no change, nothing extra is printed or kept | Unit case on `run` with the platform forced and `subprocess.run` stubbed. It asserts the kept header and the stderr line (§14) |
| A4 | The Windows half is executed where Windows exists | Given a fixture repository with the pair `bin/probe` (sh) and `bin/probe.cmd`, and the row `bin/probe`, when `run(..., shell=True)` runs on the real platform, then it exits 0 and the probe's output is in the kept file | An executed case on all three CI legs. On macOS and ubuntu it passes through `sh`. Only `windows-latest` executes the `cmd.exe` path. Its red on Windows without the fix is #448's measurement (the four-spellings table), which is the ticket's claim and not a run in this work item |
| A5 | A failing row with no test result says so | Given the `suite` check exits non-zero and its output holds no pytest summary line, when the failure form is printed, then one line says the output carries no pytest summary, so this is not a count of failing tests. Given the output holds a summary (`1 failed in 0.01s`), the line is absent. The exit code is still 1 in both cases | Unit case on `failure_lines` with a `Check`, plus one end-to-end gate run with the row `exit 1`, which reads the same under `sh` and `cmd.exe`. Red when the line is deleted (§14, §15) |
| A6 | The suite cannot see a developer's `gh` credentials | Given the suite is imported, then `GH_CONFIG_DIR` names an empty directory, `GITHUB_TOKEN` and `GITHUB_ENTERPRISE_TOKEN` are unset, and `GH_TOKEN` and `GH_ENTERPRISE_TOKEN` hold a placeholder no server accepts. Where `gh` is on PATH, `gh auth token` under the suite's environment exits non-zero or prints that placeholder. **Corrected 2026-09-25** in round 1's fix pass: this said no token variable is set and asked `gh auth status`, which does not read the keyring (round 1's 🟡 1) | Structural case, red on any machine when the conftest block is removed. Behavioural case, which skips where `gh` is absent and can be seen red only on a machine where `gh` is authenticated (the builder's; CI is unauthenticated either way, which is the point). Q2 settles whether `GH_CONFIG_DIR` alone is enough |
| A7 | The PR answers the gate contract | The PR body states, for each fix, the test seen red, the failure direction, the prompt budget (zero for both) and platform honesty (what ran on macOS, and what only `windows-latest` executes) | Read at review. `CONTRIBUTING.md` §*What a change to a gate must carry* |

**Failure directions, decided here:**

- #448's rewrite **allows more**, and in one spelling **blocks more**: a row
  that failed on `cmd.exe` now runs, and a switch written straight after a
  program other than a built-in (below) no longer does.
  A wrong allow here would need the rewrite to make `cmd.exe` run something
  other than the command the row reads as. The rewrite only ever turns `/`
  into `\` inside a command word, and `cmd.exe` has no reading in which a
  `/` inside a command name is part of the name. The exception is a `/`
  written straight after one of `cmd.exe`'s own commands (`rd/s/q`,
  `dir/b`), which is that command's switch and is left as written.
  **Corrected 2026-09-25** in round 1's fix pass: without that exception
  the rewrite turned a built-in's switch into a path, denying or changing
  a row that ran before (round 1's 🟡 2). A `/` written straight after any
  other program (`xcopy/e`) is read as part of a path and rewritten, so
  that row is **denied**: it ran before and now fails to find `xcopy\e`.
  A switch written with a blank before it (`xcopy /e`) is left as written,
  and the template says so; telling a program from a directory is #596.
  **Corrected 2026-09-25** in round 2's fix pass, which found the
  exception named only the built-ins (round 2's 🟡 1).
- #448's label changes no verdict.
- #510's scrub **blocks more**: a case that reached a live `gh` now fails
  locally. That case already fails on CI, so the only new deny is the one
  that was missing.

## Data & interfaces

- `broad_gate.py`: a pure rewrite function that takes the platform and
  `COMSPEC` as arguments, following `quote(path, windows=None)`. `run` calls
  it when `shell=True`. `Check` may carry what was handed. `failure_lines`
  gains the no-summary line. **`gate` is not edited.** Five ledger rows cite
  `skills/verify/scripts/broad_gate.py#gate@79c16119` (`seal/releases/0.10.0.md` S7 and S12,
  `0.12.0.md`, `0.12.2.md` R2 and G3), and nothing in scope needs it to
  change. `run`, `failure_lines` and `Check` have no row. If `compare_at_base`,
  `first_command` or `quote` is edited after all, the rows citing them in
  `0.10.0.md` (S5, S15) are re-read and re-stamped there.
- `templates/config.md#"## Broad gate"` is cited by `seal/releases/0.10.0.md`
  S4 and by `0.12.0.md`. Editing the section drifts both rows. They are
  re-read against the edit and re-stamped in those files.
- `CONTRIBUTING.md#"## Running the checks"` is cited by `0.10.0.md`,
  `0.15.1.md` and `0.8.2.md` (two rows). Same treatment.
- `tests/conftest.py`: one module-level block next to the `SPECSEAL_LANG` and
  `GIT_TEMPLATE_DIR` blocks, with an `atexit` cleanup like
  `_EMPTY_GIT_TEMPLATE`. No conftest unit this touches has a ledger row.
- New rows go in `seal/ledger/1790260567-the-broad-gate-hands-cmd-a-forward-slash.md`.
  The changelog entry goes in `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/changelog.md`.

## Open questions → questions.md

Q1 and Q2 are measurements and Q3 is the work's. No row needs a person.

Framed 2026-09-24 by framer, before the build.
