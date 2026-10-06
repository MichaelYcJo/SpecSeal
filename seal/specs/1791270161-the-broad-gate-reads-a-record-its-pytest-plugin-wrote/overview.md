# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — overview

## Why this work exists

The broad gate stops guessing which pytest run printed a failing line and reads a record its own pytest recorder wrote inside that run.

## Where the build stopped, and what is next

All four phases of `plan.md` are closed, each at the commit its Status cell
names. Phase 1 built the recorder; phase 2 the gate's two records and the
five-row table, with rule 3 and the **New?** bullet; phase 3 the ledger
fragment (nine new rows, eleven `Corrected ·` rows, 38 `Re-read ·` rows) and
the changelog fragment; phase 4 the corpus, which found that the recorder
wrote an inherited test under the module that defines it and is fixed
(`phases/phase-4.md`).

Next is the review chain: the draft pull request into `release/v0.20.0`,
the `warden` rounds, `broad-gate --preflight`, the sealer. `questions.md` Q1
and Q2 stay with the owner, (a) built for each.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The recorder's comment and the release-hygiene exemptions | `spec.md` R11 and `plan.md` Technical context: the `9.1.1`/`3.8.0` exemptions move "to the recorder's own comment where it names the builds it was measured on" / the recorder's docstring names builds by two components (`7.4, 8.0, 8.1 and 9.1`, xdist `3.8`) and the exact builds sit in `phases/phase-1.md` | two components in the shipped file | A three-part token in a `LOADED` file needs an exemption keyed on it, and the docstring's reader needs the minor version only. This changes Q-W2's default for phase 2: there is no token in the recorder for an exemption to move to |
| Q-W2: where the two `broad_gate.py` exemptions go | `questions.md` Q-W2 default: "moved, keyed on the recorder's path" / phase 2 deleted both rows of `VERSIONS_OF_ANOTHER_PRODUCT` and left a comment in their place | deleted | `tests/test_release_hygiene.py#timers_in` skips a listed `(file, token)` and nothing checks that a listed token still occurs, so a row naming a token the file no longer holds is a standing permission for that number to come back into `broad_gate.py` unexamined. The recorder holds no three-part token to key a moved row on (the row above). Shown biting: with a9d7b0e5's `broad_gate.py` in place, `test_no_loaded_file_names_a_version_at_or_above_the_running_one` goes red |
| The case over the shell a row is handed to | `spec.md` Scope 7: "`row_prefixes`, `POSIX_CUTS`, `CMD_CUTS` and the two row-cut parametrized cases and the shell-selection case over them" retire / the shell-selection case is kept, renamed `test_whether_cmd_exe_reads_the_row_is_one_answer` | kept | It is the one direct case of `cmd_exe_reads`, which stays: `handed_to_shell` asks it. Retiring it would leave the `bash.exe` `COMSPEC` branch with no case (NAME NOT IN TREE) |
| The reader's value | `spec.md` Scope 3 and Data & interfaces: `read_record` returns "a `Record`" / it returns a `RunRecord` | `RunRecord` | `broad_gate.py#Record` already names a round record's home (#666), and a second class of that name in the same module would replace the first |
| How the reader tells a file is this run's | `spec.md` Scope 3: "a file whose `session` line carries another key is not this run's" / `read_record` reads every `*.jsonl` and keys each file by its first line's `key` alone, with no filename filter and no separate `kind == "session"` check | the first line's key | A filename prefix and a `kind` check were each implied by the key match, so a mutant of either survived every case. One check, held by the unit table |
| A runner without the gate's environment, alone | `spec.md` Scope 8 and S12: "an `env -i` runner leaves no record; where it is the only runner the word is `NO_RECORD`" / such a row leaves no record at `HEAD` either, so the file reads `NO_RECORD_AT_HEAD` and the base is not run | `NO_RECORD_AT_HEAD` | Scope 4 runs no base where `HEAD` left no record, so `NO_RECORD` cannot be reached by that layout. `NO_RECORD` is reached where the base's row stops before its pytest (`test_a_part_that_fails_at_the_base_before_the_runner_measures_nothing`) |
| A row that sets `PYTHONPATH` itself | `spec.md` §*The class* and S13, `plan.md` Alternative A: such a row "drops the recorder: no record, `new?`" / measured: pytest exits 1 on the `-p` it cannot import, before any test, so the row fails at the gate | built as measured, named in rule 3, pinned by `test_a_row_that_replaces_pythonpath_cannot_load_the_recorder`; S13's second layout uses a row that sets `PYTEST_ADDOPTS` instead | The frame's reading does not hold for this row; the owner's trade is `questions.md` Q2, and (a) is built |
| A part after the runner at the base | `spec.md` Scope 9 asks rule 3 to say the cost; the 0.18.3 text said every part after the runner runs at the base / under one unchanged run, `&&` stops at a red base's suite as it did on the branch | rule 3 says such a part runs at the base only where the base's suite passes | Measured by `test_a_part_that_is_not_pytest_runs_as_the_row_runs_it_at_the_base`: its marker is written on a passing base and not on a failing one |
| Which file a test's line is written under | `spec.md` R4 and §*The class*: `report.location` is relative to the rootdir and "a test a module inherits from a helper is reported under the module that collected it" / measured in phase 4: `location[0]` names the module that DEFINES the test function, so the corpus's N1, N1b, N1c and Q4 read `failing on base too` for a file the base passes | the recorder writes `report.fspath`, the node id's path, for test lines as for collect lines | The corpus (S20) is the evidence: nine cases red with `location[0]`, all 55 green with `fspath`; `test_a_test_is_recorded_under_the_module_that_collected_it` pins it plain and under `-n 2`, and passes on pytest 7.4, 8.0, 8.1 and 9.1. The ledger's W1 says it |
| The regression corpus in phase 2 | `plan.md`: each phase leaves the tree green / the corpus's `REGRESSED_WORDS` spell reasons phase 2 retired | the corpus case is skipped with phase 4 named | `plan.md` gives the corpus's words to phase 4; leaving it red would hand phase 3 a red module, and re-deriving it here is phase 4's work |

## Not verified

| Item | Who must answer |
|---|---|
| The recorder on Linux and Windows (`PYTHONPATH` with `;`, a Windows temp path) | CI's three-platform test job, at the pull request |
| The listing spelled with `/` on Windows (S18): `record_path`'s `replace(os.sep, "/")` is the identity on POSIX, so its mutant survives on this machine by construction | CI's `windows-latest` leg, at the pull request |
| The recorder's fallbacks for pytest below 6.1 (`config.rootdir`, `os.getcwd()`) | nobody measured them; the next session decides whether a build that old is worth a probe |
| `read_record`'s branch for a file that is listed and then cannot be opened | nobody: no case reaches it on a local disk; it holds no record, the strict side |
| The full suite, lint and typecheck over the branch, and S22 (this suite under the sealer, its inner gates beside the outer recorder) | the sealer, once, after the review rounds settle |

## What was fed back into the spec

Three clauses, each marked *inferred during implementation* so a planner may overturn it:

- `spec.md` R4, §*The class* and Scope 1: the recorder writes a test under
  the module that COLLECTED it, `rootdir / report.fspath`, never
  `report.location[0]`, which names the module that defines the test
  function (phase 4, found by the corpus); `plan.md`'s six-months-on
  scenario and Alternative M follow.
- `spec.md` §*The class* and Scope 1, `plan.md`'s six-months-on scenario: a
  pytest session handed a path outside its rootdir writes no record, because
  pytest names those files against the argument that reached them and two
  can share one name; a forged record is no longer called the only way to a
  wrong `failing on base too` (round 1, 🔴 1).
- Rule 3: a row that keeps `PYTEST_ADDOPTS` and loses `PYTHONPATH` — a
  replaced `PYTHONPATH`, `python -I` or `-E`, a wrapper passing `PYTEST_*`
  alone — fails at the gate; `questions.md` Q2 lets the owner overturn it
  (phase 2, widened in round 1).
