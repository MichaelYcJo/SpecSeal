# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | cad946f0 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

`plan.md`'s phase 4: the 10-mutation timing both ways on one module (S11),
the ledger fragment, the changelog fragment, `overview.md` and the phase
records, with `evidence-check` on the fragment and `survivor-check` over the
branch's range for the removed `tests/__pycache__` wording. The spawn
delegated `questions.md` Q4, the default bound, to this phase's timing, with
300 s standing until it measured.

## What this phase found

**S11's answer is *not under half*, and the reason is that the cost the
ticket named was never there for the narrow form.** The loop was ten breaks
of `arm_check.py`'s `clear_bytecode_cache` and `restore` against
`tests/test_arm_check.py -q -k "cache or restore"`, three ways, interleaved
per break after one warm-up of each. The machine is the one in
`phases/phase-1.md`.

| Way | Mean | Median | Range |
|---|---|---|---|
| `rm -rf tests/__pycache__ && bin/test …`, break applied by hand | 0.76 s | 0.75 s | 0.71–0.83 s |
| `mutation-check … --tests "bin/test …"`, same arguments | 0.84 s | 0.81 s | 0.76–1.08 s |
| the same with `-p no:xdist` | 0.47 s | 0.48 s | 0.34–0.56 s |

All thirty runs were red. After a clear-all run, `tests/__pycache__` held
four files: `conftest`, the module named, the module it imports, and one left
by an earlier run. pytest compiles what the run imports, so a run naming one
module never recompiled the 142 the spec counts. The flow logs' 121 s and
96 s commands were the cases themselves. The command adds about 0.08 s, its
own interpreter start plus loading `arm_check`, measured at 0.05 s alone. The
0.47 s that remain split into that, about 0.16 s for `bin/test` and pytest to
start and collect, and 0.29 s for the six cases. The saving that exists is
`-p no:xdist`, 38 % here, and what the command buys is correctness: the
cache the clear missed, the bound, and a restore that cannot be skipped.

**That made four sentences this branch had written false, and they were
corrected before anything else.** The script's docstring, the SKILL section
and the test module's docstring said the clear *recompiled every test
module*, and the spec's suggested changelog bullet said the same. All four
now argue from the cache the clear missed. The spec keeps its sentence,
which is the framer's; `overview.md` records the divergence.

**Q4, decided: the default bound stays at 300 s.** Every mutated run this
phase timed took between 0.34 and 1.08 s, and the slowest legitimate mutated
command in the flow logs is 158 s (spec M8). Nothing measured here is near
the bound, and nothing argues for moving it. 300 s is about twice that
slowest run and a sixth of the 32-minute hang, and a smith whose run is
legitimately longer passes `--timeout` once. A new case holds the constant,
the bound a call with no `--timeout` gets, and the figure `agents/smith.md`
and `skills/verify/SKILL.md` state to one number. The constant, the parser's
default, the hand-off to the run and the documented figure were each
mutated, and each went red.

**Six ledger rows rather than five.** L6 is the class phase 1 found, a case
that plants a cache by import under an inherited
`PYTHONDONTWRITEBYTECODE`. L5 carries an anchor after all: the plan said the
measurement rows carry none, and the anchor given is the bound the timings
were read against, because Q4 was decided from them. The fragment was
written with placeholder hashes and `evidence-check --reverify --checked
2026-10-01 --ledger <fragment>` filled all 37.

**The spec's own stamp drifted, and the records arm read it.** Once the
fragment existed the work item counted as unreleased, so `evidence-check`
read its records and found `spec.md` M9's stamp on `agents/smith.md`'s
`## Phases`, at hash `cede28c2`, stale after phase 3. The stamp now
carries the hash the rows hold, with a `Corrected 2026-10-01` note keeping
the framer's reading. `evidence-check --strict` then exited 0: 3188 ok, 0
drifted.

**`survivor-check --range cd24f516..HEAD` at `cad946f0`**: 559 files
examined against the 12 sentences the range removed, none still standing,
exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the claim, in the script's docstring, the SKILL section and the test module's docstring, that clearing `tests/__pycache__` recompiled every test module | the ledger fragment's L5, which carries the measurement that refuted it |
