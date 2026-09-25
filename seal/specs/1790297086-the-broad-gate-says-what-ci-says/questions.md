# the broad gate says what CI says — questions for the planner

<!-- seal/specs/1790297086-the-broad-gate-says-what-ci-says/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The owner pressed `automation` for the whole
of `release: 0.15.4`, so nobody answers before the build. Every judgment the
tickets left open was one the tree could settle. Each is listed below with
its grounds, so nobody reopens it. The two rows that remain are
measurements, and the build proceeds on each row's default.

## Decided from the tree — not open

| # | Left open by | Decided | Grounds |
|---|---|---|---|
| T1 | #596 ("adds a filesystem read to a pure function") | Take the directory rule, and pass the directory question into the scan as a predicate. `handed_to_shell` does the read, against `run`'s `root`. | The milestone description names this fix. The predicate keeps the scan drivable the way `windows`/`comspec` already make it (`handed_to_shell` docstring). `PATH` and spelling heuristics are rejected in `plan.md` §Alternatives. |
| T2 | #596 (what "the part before the first `/`" is) | The name's characters up to its first `/`, with `"` and `^` removed and a leading `@` dropped. An empty part counts as a directory. One decision per name covers every `/` in it. | The scan already strips `@` for `CMD_BUILTINS`. An empty part is a drive-root path, and treating it as a directory keeps today's output for that shape. |
| T3 | #473 ("decide whether the gate should carry the guard") | Carry it, only where the gated repository's `release` job carries the step, keyed on `--base` naming `main`. | `docs/the-broad-gate.md` #475 paragraph ("the gate exists to say what CI will say"). A7 of work item `1789985781` forbids changing the run of a repository with no workflow. Skipping everywhere under-asks in repositories whose feature branches merge into `main`. |
| T4 | #473 ("say so in the partition's own row") | A constant beside `PARTITION`, not a fourth tuple element. | Nine sites unpack the three-tuple: seven in `tests/test_the_gate_names_every_step_ci_runs.py` and two in `broad_gate.py`, counted 2026-09-25. |
| T5 | #473 (what a person sees) | One stderr line. Panel and `workflow` count unchanged. | The panel carries no row for either arm. A step both sides skip is agreed, not unanswered. Names go to stderr and counts to the panel (`coverage_line` docstring, W1). |
| T6 | #482 ("read as YAML") | Read as text through one shared reader in `tests/conftest.py`. A step is found by its `- name:` or by the one step whose code lines name a script. | No YAML parser is installed anywhere (no `pyproject.toml`; `test_ci_gives_the_checks_what_they_need.py#jobs` docstring). `from conftest import` is the suite's helper mechanism, used by 53 modules. |
| T7 | #482 (the class) | Six sites across four modules move onto the reader. No structural case forbids a seventh. | Enumerated by `grep` in `spec.md` S2. A check over the suite's own source would be a new gate, and this is a patch release. |
| T8 | #462 ("what makes a `BASE:` line the one that counts") | A `BASE:` whose nearest shallower code line is `env:`. | The one live `BASE:` is an `env:` key (`hygiene.yml`, milestone step). The reader's own comment says the `env:` assignment is what it means. |
| T9 | #462 (a trailing comment) | Stripped too, outside quotes. | YAML ends a plain scalar at ` #`, and the shell ignores the rest of a line there. No workflow line carries one today (measured 2026-09-25), so current readings do not change. |
| T10 | #463 ("the repair is in the caller") | `base_spellings` returns `""`. The spelling check becomes a helper that asserts, driven with `--baseline ""`. | As the ticket asks. The widened pattern stays. |
| T11 | #499 (strip more paths, or move the assertion) | Move the assertion onto `` `release` ``, `WORKFLOW` and the `PARTITION` step names. | A strip list of echoed paths is maintained by hand. 1404b3a7 already had to extend it once. |

## Open

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | Does `cmd.exe`, reached through `subprocess.run(..., shell=True)`, run a non-built-in with a switch written straight against it (`where/q cmd`) as the program plus its switch, exit 0? This is #596's premise, taken from `cmd.exe`'s documented lexing and the reviewer's reading. The tree cannot answer it, because this machine is macOS and no Windows run belongs to framing. | a measurement: A6's executed case on CI's `windows-latest` leg at the pull request | **Yes:** phase 1 stands. **No** (`cmd.exe` searches for `where/q` as one name): a glued switch never ran on `cmd.exe`, so #596's harm was not real, and the directory rule only stops rewriting names that do not start in a directory. That is still correct, and the template's sentence about the blank becomes the only advice. This goes back through the review chain as a finding. | Proceed as if yes, as `broad_gate.py`'s `# --- what cmd.exe is handed` comment block ("`cmd.exe` reads a `/` in a command NAME as the start of a switch") and #596 state |⬜ still open after the build: `tests/test_the_gate_hands_cmd_a_path_it_can_run.py#test_a_switch_against_a_program_runs_on_the_real_platform` is written and is skipped on macOS. Only CI's `windows-latest` leg at the pull request answers it |
| M2 | Is #499's instance already green at the frame commit, after 1404b3a7 added `sys.executable` and the gate's realpath to the strip list? | a measurement: phase 4 runs the module from a scratch copy of the tree under a directory whose name holds `release`, before editing. A copy, never a worktree left behind (contract §7). | **Green:** the edit is still made, because the strip list is the fragile part, and the phase record says the original instance was closed by #549. **Red:** the edit closes it, and the phase record names the path that still leaked. | Make the edit either way | ✅ **Green**, measured 2026-09-25 in phase 4 before the edit: the module's no-workflow case, run with its own virtualenv from a scratch copy of 73f8fded under a directory named `release-m2`, 1 passed. 1404b3a7 (#549) had already closed the original instance by cutting `sys.executable` and the gate's realpath out of the stream. The edit was made anyway, and the same run after it (5dab37f1) is green too. |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build. None here.
- **a measurement** — a probe, a command or a count settles it.
- **the work** — unknowable at framing time. The phase that meets it decides
  it and records a divergence row.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
