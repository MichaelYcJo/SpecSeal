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
| Earlier word assertions | `spec.md` S16: "Every other word assertion is unchanged" / STOPPED_EARLY retires (Scope 6), and a group that decides nothing now runs file by file (Scope 4) | three cases changed word, each to the word the base gives; `phases/phase-1.md` lists them | Scope 4 and Scope 6 are the design; S16's sentence cannot hold beside them. One of the three is a `failing on base too` where a3aa139a gave `new?`, for a file the base fails in the one directory its one runner names |
| Q4, the names | `questions.md` Q4: "wording and names are phase 1's" | `NOT_ENDED`, `COLLECTED_BEYOND`, `MULTI_RUNNER`; `NO_RUNNER` reworded | `phases/phase-1.md` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck after the rounds | the sealer, spawned by the orchestrator |
| Linux (`/bin/sh` as dash) and Windows (`cmd.exe`): `PYTEST_ADDOPTS` reaching a runner inside `sh -c`, the inserted quoted file, the rest of a row after a `cmd.exe` cut, and pytest's trailer and listing lines | CI's three-platform test job (`questions.md` Q2) |
| pytest older than 8.1 through the gate end to end (the frame measured the pass's output on 7.4.4, 8.0.0 and 8.1.1; the unit table holds 8.0's tree) | the repository owner, if such a row is met |

## Not done

- A file pytest cannot collect, under a row that passes `-rN`, gets no
  `ERROR <path>` short-summary line, only the `ERROR collecting <path>`
  banner, so its proof reads `COLLECTED_BEYOND` though the base does fail
  it. Reading the banner too would earn the word back; it is strict as it
  stands and was not part of the frame.
- `questions.md` Q1's option (b), `new?` for every failing file of a row
  that runs pytest more than once, stays a separate change the owner can
  choose.

## Fed back into the spec

- Scope 4, inferred during implementation: a group of one file is a file
  run alone; a group that writes no report reads `NO_RUNNER` for each of its
  files.
