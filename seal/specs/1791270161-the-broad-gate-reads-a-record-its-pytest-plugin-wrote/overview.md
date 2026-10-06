# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — overview

## Why this work exists

The broad gate stops guessing which pytest run printed a failing line and reads a record its own pytest recorder wrote inside that run.

## Where phase 2 stopped, and what is next

Phase 1 is closed at 27365f10 (the recorder, `phases/phase-1.md`). Phase 2
is closed at the commit `plan.md`'s Status cell names: the gate loads the
recorder into the `HEAD` run and into one unchanged run at the base, reads
both records, and gives each file a row of the five-row table; the prefix
cuts, the JUnit report, the proof pass, the solo runs and the group retired
with their cases; rule 3 and the **New?** bullet are rewritten and pinned
(`phases/phase-2.md`).

Next, phase 3 (the ledger fragment with its `Corrected ·` rows, and the
changelog fragment) and phase 4 (the regression corpus). Phase 4 starts
from a skipped case: `test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives`
carries a `skip` naming phase 4, because its `REGRESSED_WORDS` still spell
the retired reasons; phase 4 re-derives the words and removes the mark.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The recorder's comment and the release-hygiene exemptions | `spec.md` R11 and `plan.md` Technical context: the `9.1.1`/`3.8.0` exemptions move "to the recorder's own comment where it names the builds it was measured on" / the recorder's docstring names builds by two components (`7.4, 8.0, 8.1 and 9.1`, xdist `3.8`) and the exact builds sit in `phases/phase-1.md` | two components in the shipped file | A three-part token in a `LOADED` file needs an exemption keyed on it, and the docstring's reader needs the minor version only. This changes Q-W2's default for phase 2: there is no token in the recorder for an exemption to move to |
| Q-W2: where the two `broad_gate.py` exemptions go | `questions.md` Q-W2 default: "moved, keyed on the recorder's path" / phase 2 deleted both rows of `VERSIONS_OF_ANOTHER_PRODUCT` and left a comment in their place | deleted | `tests/test_release_hygiene.py#timers_in` skips a listed `(file, token)` and nothing checks that a listed token still occurs, so a row naming a token the file no longer holds is a standing permission for that number to come back into `broad_gate.py` unexamined. The recorder holds no three-part token to key a moved row on (the row above). Shown biting: with a9d7b0e5's `broad_gate.py` in place, `test_no_loaded_file_names_a_version_at_or_above_the_running_one` goes red |
| The case over the shell a row is handed to | `spec.md` Scope 7: "`row_prefixes`, `POSIX_CUTS`, `CMD_CUTS` and the two row-cut parametrized cases and the shell-selection case over them" retire / the shell-selection case is kept, renamed `test_whether_cmd_exe_reads_the_row_is_one_answer` | kept | It is the one direct case of `cmd_exe_reads`, which stays: `handed_to_shell` asks it. Retiring it would leave the `bash.exe` `COMSPEC` branch with no case |
| The reader's value | `spec.md` Scope 3 and Data & interfaces: `read_record` returns "a `Record`" / it returns a `RunRecord` | `RunRecord` | `broad_gate.py#Record` already names a round record's home (#666), and a second class of that name in the same module would replace the first |
| How the reader tells a file is this run's | `spec.md` Scope 3: "a file whose `session` line carries another key is not this run's" / `read_record` reads every `*.jsonl` and keys each file by its first line's `key` alone, with no filename filter and no separate `kind == "session"` check | the first line's key | A filename prefix and a `kind` check were each implied by the key match, so a mutant of either survived every case. One check, held by the unit table |
| A runner without the gate's environment, alone | `spec.md` Scope 8 and S12: "an `env -i` runner leaves no record; where it is the only runner the word is `NO_RECORD`" / such a row leaves no record at `HEAD` either, so the file reads `NO_RECORD_AT_HEAD` and the base is not run | `NO_RECORD_AT_HEAD` | Scope 4 runs no base where `HEAD` left no record, so `NO_RECORD` cannot be reached by that layout. `NO_RECORD` is reached where the base's row stops before its pytest (`test_a_part_that_fails_at_the_base_before_the_runner_measures_nothing`) |
| A row that sets `PYTHONPATH` itself | `spec.md` §*The class* and S13, `plan.md` Alternative A: such a row "drops the recorder: no record, `new?`" / measured: pytest exits 1 on the `-p` it cannot import, before any test, so the row fails at the gate | built as measured, named in rule 3, pinned by `test_a_row_that_replaces_pythonpath_cannot_load_the_recorder`; S13's second layout uses a row that sets `PYTEST_ADDOPTS` instead | The frame's reading does not hold for this row; the owner's trade is `questions.md` Q2, and (a) is built |
| A part after the runner at the base | `spec.md` Scope 9 asks rule 3 to say the cost; the 0.18.3 text said every part after the runner runs at the base / under one unchanged run, `&&` stops at a red base's suite as it did on the branch | rule 3 says such a part runs at the base only where the base's suite passes | Measured by `test_a_part_that_is_not_pytest_runs_as_the_row_runs_it_at_the_base`: its marker is written on a passing base and not on a failing one |
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

none — phase 2 added no clause to `spec.md`. Rule 3's new sentence about a
row that replaces `PYTHONPATH` is *inferred during implementation* from a
measurement, and `questions.md` Q2 lets the owner overturn it.
