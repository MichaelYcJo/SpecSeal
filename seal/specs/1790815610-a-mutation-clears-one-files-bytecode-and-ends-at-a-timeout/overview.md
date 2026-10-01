# a mutation clears one file's bytecode and ends at a timeout — overview

📋 implement applied
· spec:     `seal/specs/1790815610-…/spec.md`, `plan.md`, `questions.md`, `routing.md`; `agents/smith.md` §Phases step 4 and §Boundaries; `skills/verify/SKILL.md` §*`arm-check` asks condition 2 of a whole module*; `skills/agent-contract/SKILL.md` §5, §9, §12, §13, §14, §15; `CLAUDE.md` §*a change writes fragments*
· evidence: `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L1–L6 added; re-read and re-stamped in place: `seal/releases/0.6.0.md` L5, `0.8.1.md` R8, `0.12.0.md` (the design gate's second copy), `0.15.1.md` N1, `0.9.5.md` (the bytecode-cache row)
· verified: executed — the new module and every module reading the two edited documents, narrow; every new case seen red first; every unit mutated with the command; both timings. Read — the Windows arm. Unverified — the full suite, lint and the broad gate (the orchestrator, through the sealer)

## Why this work exists

The smith's mutation loop cleared the wrong cache and bounded nothing; it is
now one command per break that removes the mutated file's bytecode, ends a
run that hangs, and restores from held bytes.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How `mutation_check.py` reaches `arm_check.py` | Spec M7 and plan *How the sibling import resolves*: `from arm_check import …`, resolved because a script's directory is first on `sys.path` / loaded by path with an `importlib` spec, registered first | Code | Nine shipped scripts reach another file by path and none by `sys.path`; a bare import fails under `PYTHONSAFEPATH` and when a case loads the script by spec. `phases/phase-1.md` |
| How S1 and S2 plant their caches | Spec: S1 *a planted `.pyc` made by a real import*; S2 *imported once* just before the mutation / S1 plants with `py_compile`, S2 with an unchecked-hash `.pyc` | Code | Under the command the cases inherit `PYTHONDONTWRITEBYTECODE=1`, so an import-made plant is never written and the case is red on its precondition. The unchecked-hash plant makes S2 red on every run without the removal instead of only inside one mtime second. Both claims are kept |
| The cost the old clear carried | Spec §*The class*: *forces pytest to recompile all 142 test modules on every mutated run*; plan *recompiles one module instead of 142* / measured: with one module named, the clear left four files in `tests/__pycache__`, and the clear-all loop ran at 0.76 s per mutation against 0.84 s through the command | Measurement | L5 in the fragment. The documents, the docstrings and the changelog now argue from the cache the clear missed, not from its cost. The flow logs' 121 s and 96 s commands were the cases themselves |
| Step 4's example and wording | Spec §*Data & interfaces*: `--tests "bin/test tests/<module>.py …"`, *removes that one file's cached bytecode* / `--tests "<the runner> <module> -k <cases>"`, *the mutated file's* | Pins | `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` refuses `bin/test` in a shipped definition, and `tests/test_the_set_a_work_item_always_has.py` refuses *one file* in it. Both are ratified; the text was a suggestion |
| `tests/test_arm_check.py` | Spec C2: `arm_check.py` is not edited and the test module stays green; silent on editing the test module / two plants switch bytecode writing on | Code | §12: the class the command made reachable has three members and two are there. `arm_check.py` itself is untouched |
| Refusals | Spec: a replacement that does not land exactly once / also an empty OLD, a NEW identical to OLD, a non-UTF-8 file, and a `--tests` naming no command | Code | Each would otherwise print a verdict nobody measured. `phases/phase-1.md` §*Q3* |
| The changelog's `### Changed` bullet | Spec: *That clear recompiled every test module on every mutated run* / the bullet says the clear removed valid caches and missed the stale one; a `### Fixed` bullet added for the two `arm-check` cases | Measurement | The third row above |
| Spec M9's stamp | `## Phases` of `agents/smith.md` at hash `cede28c2` / re-stamped to the hash the rows now hold, with a `Corrected` note keeping the framer's reading | Correction | `evidence-check`'s records arm reads the stamp, and phase 3's edit moved it |

## Not verified

| Item | Who must answer |
|---|---|
| The Windows arm run on Windows: `proc.kill()` ending the direct child, the verdict text it prints, and `bin/mutation-check.cmd` reaching the script | the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request. That leg runs this module whole: S6, and every other case through the direct-child strategy, but no case times out there, so `proc.kill()` on expiry is still read and not run, and nothing in this repository runs the `.cmd` wrapper |
| The full suite, repository-wide `ruff check` and `ruff format --check`, and the broad gate over this branch | the orchestrator, through the sealer, once the review rounds settle |
| How the harness's own command bound did not end #577's 32-minute hang (spec M8) | the orchestrator, who holds the flow log; this work item bounds the run inside the command and does not explain the harness |

## Not done

`arm-check`'s own bound still ends the direct child only. That is #313, which
asks for the Ctrl-C and Windows decisions on purpose; `mutation_check.py`
now holds a group bound beside `run_arms`' to fold into it. The warden's
definition does not name the command (spec §*Scope*, out). There is no copy
of the original on disk (#312). The README cheat sheet does not list the
command (`questions.md` Q2, decided in phase 3).

## Fed back into the spec

*Inferred during implementation*: a case that needs a `.pyc` to exist writes
it itself, because the cases a mutation loop runs inherit
`PYTHONDONTWRITEBYTECODE=1` (`skills/verify/SKILL.md`, the new section; L6).
And the output collection after a group kill is bounded, because a process
that left the group holds the pipe (`REAP_TIMEOUT`; L2).
