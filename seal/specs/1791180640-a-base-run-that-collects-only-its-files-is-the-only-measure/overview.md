# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — overview

## Why this work exists

The broad gate gave `failing on base too`, the one word that lets a red suite
through, to files the base passes; now it gives that word only where a run of
the row at the base collected nothing but the file, and a row that cannot
show that reads `new?`.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A group of one file | `spec.md` Scope 4: "every other failing file runs in one group first" / a group of one file is the same command as that file's run alone, and the lone table decides everything the group rule does and more | a single file the base carries runs alone from the start, numbered after the candidates | the plan's cost sentence: "A base that passes every failing file costs what 0.18.2 cost"; running the same command twice spends one more run of each prefix for nothing. Inferred during implementation |
| A group whose walk writes no report | `spec.md` Scope 4: "In every other case, each file of the group runs alone: a failure, an error, no test, a non-zero exit" / every case listed is an outcome of a report | where no prefix writes a report for the group, each of its files reads `NO_RUNNER` without running alone | spec silent on the no-report case; what drops the option is the row, so a run of one file writes none either. Inferred during implementation |
| Earlier word assertions | `spec.md` S16: "Every other word assertion is unchanged" / STOPPED_EARLY retires (Scope 6), and a group that decides nothing now runs file by file (Scope 4) | three cases changed word; `phases/phase-1.md` lists them | Scope 4 and Scope 6 are the design; S16's sentence cannot hold beside them. At phase 1 one of the three, and the files-only parameter of the cannot-collect case, gave `failing on base too` where a3aa139a was stricter. Corrected at fd98c2c8 by round 1's fix pass: both now read `new?` with `COMPANY` (the next row) |
| The row's own context has to agree | `spec.md` §*The class*, condition 1: "`h` ran alone" treats a run alone as the cure / round 1's 🔴 1: a file the base passes beside the other failing files and fails alone read `failing on base too` | a group that went file by file compares its own failing count with its files' counts alone; where the files fail more alone, or one has no count alone, every `failing on base too` they earned alone reads `COMPANY` | round 1's report, and the orchestrator's choice of the strict variant (round 1's ❓): the permissive word needs the row's context to agree, not the file alone. Inferred during review |
| A runner without the gate's environment | `spec.md` Scope 7: a second runner the pass does not reach with the gate's environment is a permissive limit "the same as at a3aa139a" / round 1's 🔴 2: for a FIRST such runner the measurement moved to the runner after it, where a3aa139a read `new` | an outcome line of a session that ran tests, in the proof's output, reads `MULTI_RUNNER`; rule 3's limit keeps only such a runner that prints nothing (`-qq` or quieter) | round 1's report; only a runner that did not read `PYTEST_ADDOPTS` runs tests under the proof. Inferred during review |
| Q4, the names | `questions.md` Q4: "wording and names are phase 1's" | `NOT_ENDED`, `COLLECTED_BEYOND`, `MULTI_RUNNER`; `NO_RUNNER` reworded | `phases/phase-1.md` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck after the rounds | the sealer, spawned by the orchestrator |
| Linux (`/bin/sh` as dash) and Windows (`cmd.exe`): `PYTEST_ADDOPTS` reaching a runner inside `sh -c`, the inserted quoted file, the rest of a row after a `cmd.exe` cut, and pytest's trailer and listing lines | CI's three-platform test job (`questions.md` Q2) |
| pytest older than 8.1 through the gate end to end (the frame measured the pass's output on 7.4.4, 8.0.0 and 8.1.1; the unit table holds 8.0's tree) | the repository owner, if such a row is met |

## Not done

**Every exception to "no new permissive word" (`spec.md` S17), with its
reason.** After round 1's fix pass only one is left: the S3–S5 shape, where
the base truly fails a file whose test runs pytest itself, under a
files-only row, and a3aa139a read an inner run's lines instead (18 words of
the inner-run matrix, `phases/phase-2.md`). The others recorded before it
are gone: the warnings-only group's `tests/test_one.py` and the
interrupted group's `tests/test_two.py` read `new?` since fd98c2c8, and
round 1's layouts A, A2, B and C read `new?` there too.


- A file pytest cannot collect, under a row that passes `-rN`, gets no
  `ERROR <path>` short-summary line, only the `ERROR collecting <path>`
  banner, so its proof reads `COLLECTED_BEYOND` though the base does fail
  it. Reading the banner too would earn the word back; it is strict as it
  stands and was not part of the frame.
- Two dependencies in one group whose counts cancel (one file failing only
  beside the others, another only alone) leave the group's count equal and
  its words standing. Rule 3 names it. A leave-one-out run, the group
  without each file, would see it at one more run per file the base fails
  alone; round 1 named it as the finer alternative, and this pass, which
  may not add mechanism beyond the fix, did not take it.
- `questions.md` Q1's option (b), `new?` for every failing file of a row
  that runs pytest more than once, stays a separate change the owner can
  choose.

## Fed back into the spec

- §*The class*, condition 1, inferred during review (round 1): a run alone is
  measured against the row's own context, and the word needs the files run
  together to fail at least as many tests as they fail one by one.

- Scope 4, inferred during implementation: a group of one file is a file
  run alone; a group that writes no report reads `NO_RUNNER` for each of its
  files.
