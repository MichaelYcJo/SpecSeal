# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b16f01cd |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The records. The ledger fragment with at least R1 (the refusal), R2 (its
bound) and R3 (the prefix), each `executed`, dated, naming how red was seen.
The changelog fragment under `### Fixed`. The three release rows spec M6
names, re-read against the edit, corrected in place where the edit made a
claim false, and re-stamped with a dated note (`evidence-check --reverify
--checked 2026-10-01 --ledger <file>`). `bin/evidence-check` green.
`overview.md` closed with S11 in `## Not verified`. Q3 measured. The spawn
added `survivor-check --range a340221b..HEAD`, and a hand-back saying what it
reported.

## What this phase found

**One of the three release rows was false and two held.** 0.9.5's `run_arms`
row said *both are now recorded where a pair with no verdict goes* of its own
example. That example is a command that hangs or cannot start whatever the
module holds, and since phase 1 such a command is refused as `no baseline`
before any pair. The sentence was narrowed in place to a pair's command, with
a `Corrected 2026-10-01` note. 0.9.5's `clear_bytecode_cache` row and
0.15.1's N2 still hold, and each carries a `Re-read 2026-10-01` note. N2 was
re-stamped twice, the second time for the step-list fix below.

**`evidence-check --strict` read this work item's records once the fragment
existed, and refused four names the tree does not hold.** One is the
sibling's `mutation_run` (NAME NOT IN TREE), which comes from the frame.
The other three are `NO_VERDICT_COMMANDS` (NAME NOT IN TREE), which phase 1
removed. None of them is wrong as a
record of what was there, so each line carries `NAME NOT IN TREE` rather than
a rewrite: `plan.md` and `spec.md` are approved text, and the phase record
names what it removed. After that, strict exit 0 with 3196 rows ok.

**`survivor-check` named one survivor, and it was a defect.**
`skills/verify/SKILL.md`'s step list still said *makes each arm wrong in turn,
runs that command* with no first run, beside `bin/arm-check`'s list, which
phase 1 had corrected. It now names the first run, and the re-run exits 0:
34 removed sentences, none still standing. Nothing went into `survivors.md`,
and that file does not exist.

**Q3**, measured on an Apple M3 Pro with 12 cores: `arm-check
hooks/review-history-guard.py --tests "bin/test tests/test_chain_hooks.py -q"`
took 107.9 s with the script from `a340221b` (copied to the scratchpad) and
110.5 s with this branch's. Both exited 0 with the same `32 arms measured ·
31 killed · 1 watched by no case`, and the guard's sha256 was unchanged after
both. One run of the command alone took 1.8 s. The figures are in R2.

**The fragment carries no header**, like every other `seal/ledger/*.md`. The
hashes were written by `--reverify` over placeholder `@000000` anchors, not
typed: 19 anchors over three rows.

**A rate-limit stop came between the Q3 timing and the ledger commit.** The
two release files were modified and uncommitted at the stop. They were
checked against what was meant before anything else was done: three rows,
seven anchors re-stamped, one `Corrected` note and two `Re-read` notes.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| 0.9.5 `run_arms` row: *Both are now recorded where a pair with no verdict goes* | the same row, narrowed to *A pair whose command hangs or cannot be spawned*, with the `Corrected 2026-10-01` note saying why |
| `skills/verify/SKILL.md`: *makes each arm wrong in turn, runs that command* | the same sentence, with the first run named before the arms |
