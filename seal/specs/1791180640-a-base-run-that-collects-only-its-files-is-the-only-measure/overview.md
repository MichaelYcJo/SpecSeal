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
| A group of several failing files | `spec.md` §*The class*, condition 1: "`h` ran alone" treats a run alone as the cure / round 1's 🔴 1, then round 2's 🔴 1: a file the base passes beside the others but fails alone read `failing on base too`, and a count comparison let another file's failures make up the count | every file of a group whose run at the base did not give `new` reads `COMPANY`; none runs alone and none is proven | the owner's decision of 2026-10-05 after round 2: a group of several failing files never earns `failing on base too`. Inferred during review |
| A runner without the gate's environment | `spec.md` Scope 7: a second runner the pass does not reach with the gate's environment is a permissive limit "the same as at a3aa139a" / round 1's 🔴 2: for a FIRST such runner the measurement moved to the runner after it, where a3aa139a read `new` | an outcome line of a session that ran tests, in the proof's output, reads `MULTI_RUNNER`; rule 3's limit keeps only such a runner that prints nothing (`-qq` or quieter) | round 1's report; only a runner that did not read `PYTEST_ADDOPTS` runs tests under the proof. Inferred during review |
| The session the proof reads | `spec.md` Scope 5: the proof shows one session listing the file / round 2's 🟡 2: the measuring runner's output went to a file, and the one session seen was the next runner's | the proof hands the measuring runner `-o verbosity_test_cases=-1` after the file and needs its node ids; a session listed by file reads `MULTI_RUNNER` | round 2's report's alternative, executed against a pytest 8.1 release, a pytest 8.3 release and 9.1.1, plain and under `-n 2`. Inferred during review |
| Q4, the names | `questions.md` Q4: "wording and names are phase 1's" | `NOT_ENDED`, `COLLECTED_BEYOND`, `MULTI_RUNNER`; `NO_RUNNER` reworded | `phases/phase-1.md` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck after the rounds | the sealer, spawned by the orchestrator |
| Linux (`/bin/sh` as dash) and Windows (`cmd.exe`): `PYTEST_ADDOPTS` reaching a runner inside `sh -c`, the inserted quoted file, the rest of a row after a `cmd.exe` cut, and pytest's trailer and listing lines | CI's three-platform test job (`questions.md` Q2) |
| pytest older than 8.1 through the gate end to end (the frame measured the pass's output on 7.4.4, 8.0.0 and 8.1.1; the unit table holds 8.0's tree) | the repository owner, if such a row is met |

## Not done

**Every exception to "no new permissive word" (`spec.md` S17), with its
reason.** After round 2's fix pass there is none. The corpus re-run at the
head (the 46 phase-2 layouts, round 1's four, round 2's ten, and the 96-run
inner-run matrix, each under both rows: 516 words against a3aa139a's gate)
gives `failing on base too` only where a3aa139a gave it too. The S3–S5
shape, the last exception after round 1, is gone: its file is one of two
failing files of one run at the base, and reads `new?`. Round 2's two
regressions are closed rather than named: a group whose count another file
made up (every file of a failed group reads `new?`), and a measuring runner
whose output never reached the gate (the proof reads only that runner's own
node ids). This repository's row in round 2's cancel2 shape reads `new?`
for all three files.

What a3aa139a gave that the head no longer gives, and the other way: 22
matrix words move from a3aa139a's `failing on base too` to `new`, each for
`tests/test_g.py` where the base passes every file and a3aa139a read an
inner run's `FAILED` line; the base's group run passes there, and `new` is
the base's word. Every other word the head gives differently from
a3aa139a is a form of `new?`.

- A file pytest cannot collect, under a row that passes `-rN`, gets no
  `ERROR <path>` short-summary line, only the `ERROR collecting <path>`
  banner, so its proof reads `COLLECTED_BEYOND` though the base does fail
  it. Reading the banner too would earn the word back; it is strict as it
  stands and was not part of the frame.
- Two routes never meet a group, as before the proof run existed, and rule
  3 names both: a file that runs alone from the start (the one failing file
  the root carries, every failing file of a `cd sub` row) is compared with
  no sibling, and a sibling the branch passes is never run at the base.
  Round 2 measured both reading `failing on base too` at every gate,
  a3aa139a included.
- A wrapper that forwards only the options it knows now refuses the proof
  run's `-o verbosity_test_cases=-1` and reads `new?` (Q12 of the corpus,
  where a3aa139a gave `failing on base too`). Rule 3 already tells a row to
  pass its arguments on.
- `questions.md` Q1's option (b), `new?` for every failing file of a row
  that runs pytest more than once, stays a separate change the owner can
  choose.

## Fed back into the spec

- §*The class*, condition 1, inferred during review (round 2): a file earns
  the word only where it is the one failing file of its run, alone from the
  start, and the session the proof reads is the measuring runner's own.

- §*The class*, condition 1, inferred during review (round 1): a run alone is
  measured against the row's own context, and the word needs the files run
  together to fail at least as many tests as they fail one by one.

- Scope 4, inferred during implementation: a group of one file is a file
  run alone; a group that writes no report reads `NO_RUNNER` for each of its
  files.
