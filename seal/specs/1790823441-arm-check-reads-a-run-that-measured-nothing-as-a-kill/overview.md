# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — overview

📋 implement applied
· spec:     this item's spec.md (Grounding, M1–M8, Scope, S1–S11), plan.md (Alternatives A–L, Phases, Ledger, Operational impact), questions.md (J1–J14, Q1–Q5); skills/verify/SKILL.md §`arm-check`; skills/agent-contract §9, §12, §14, §15; CLAUDE.md §fragments and §ledger rows; #641's mutation_check.py baseline and main (read in its worktree)
· evidence: seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md R1–R3 added; seal/releases/0.9.5.md the clear_bytecode_cache row (re-read) and the run_arms row (corrected), seal/releases/0.15.1.md N2 (re-read), each re-stamped 2026-10-01
· verified: executed — tests/test_arm_check.py narrow at every step and on 3.13 and 3.14 with pytest alone; 26 mutations red; the script loaded and refused a run on 3.9.6; Q2 and Q3 on the real guard; evidence-check --strict exit 0; survivor-check exit 0. Unverified — the full suite, S11, the CI legs (table below)

## Why this work exists

`arm-check` printed `killed` beside every arm for a `--tests` that could not
pass at all, and cleared a stale `.pyc` from the wrong mirror under a relative
`PYTHONPYCACHEPREFIX`; now the first refuses the run as `no baseline`, exit 2,
before anything is written, and the second clears the mirror the cases read.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The count of shifted cases | spec M5 and §Scope 5 say *five existing cases*, and both name six functions (seven items with the parametrise) | the six, all rewritten | Running the module after the baseline landed turned exactly those seven items red and nothing else |
| The bound in the two rewritten timeout cases | spec §Scope 5 keeps *the per-arm timeout path they pin*; the cases passed `0.3` | `HANG_BOUND = 1.0` | The run against the unmutated module now has to finish inside the same bound before any pair is asked, and 0.3 s is an interpreter start-up on a loaded Windows runner. Each case waits four bounds, about 4 s |
| *Nothing was written* | spec S1 checks the module byte-identical | byte-identical **and** an mtime set long ago unchanged | A restore writes the same bytes, so a byte comparison cannot tell *never written* from *written and restored*; the mtime can. #641's round 2 found the sibling's *Nothing was written* sentence pinned by no case |
| The first run's capture | spec silent; the pairs run with `text=True` | the first run captures bytes and `_text` decodes them with replacement | Under `text=True` a suite printing a non-UTF-8 byte turns the refusal into a `UnicodeDecodeError` traceback; #641's runner decodes the cases' output the same way, *shown, not trusted* |
| Cases beyond S1–S9 | spec §Scope 6 lists S1–S5, S8, S9 | three more: the first run is in `--cwd`, it runs whatever the arms are, a timeout carries what was printed | Each pins a unit a mutation left green against S1–S6 (`phases/phase-1.md`, M5, M14, M15) |
| The cache case's probe | spec §Scope 5 shifts the case's count by one | the count shifted, and the probe also leaves a `.pyc` behind after each observation | The first run's clear removed the planted cache before any arm, so the per-arm clear was watched by nothing (mutation P0, `phases/phase-2.md`) |
| Where Q3's figures go | `questions.md` Q3 says *for the ledger row R1's notes* | R2's notes | R2 is the row about what the first run costs and how it is bounded; R1 is about the refusal |
| Round 1's 🟡 1 fix | the report's paste-ready block reads the module inside the `try` whose `except OSError` reports a spawn failure | each outcome recorded in its own `except`, the put-back in a `finally` beside them, a module that cannot be read counted as changed | In the report's shape a module the cases removed raises `FileNotFoundError` from the read, which that `except` reports as the command failing to start, under *Nothing was written*. The case's `removes it` parameter holds the difference |

## Not verified

| Item | Who must answer |
|---|---|
| S11 — `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` green on the tree holding both this branch and #641's, and `mutation_check.py`'s three `clear_bytecode_cache(path)` calls given `cwd=cwd` (`questions.md` Q1) | the orchestrator of whichever branch lands second on `release/v0.17.0`, with that module's narrow run |
| The full suite, the repository-wide lint and the typecheck | the orchestrator, through the sealer after the review rounds settle |
| S10's two CI legs, `arm-check-grammar (3.13)` and `(3.14)`, and the Windows leg of `pytest`, which runs this module under `-n auto` with `HANG_BOUND` and the mtime pin, and where round 1's 🟡 2 meets a real cp1252 pipe (reproduced here only through `PYTHONIOENCODING`) | the pull request's checks |

## Not done

- **`mutation_check.py`'s three `cwd=cwd` keywords.** That file is not in
  this tree. `questions.md` Q1's default stands: the branch that lands second
  adds them.
- **An interrupt arm in `main`, and a catch-all exiting 2** (#641's 🟡 3 and
  its interrupt sentence). Out of scope under spec §Scope *Out* and J9. The
  first run sits before the loop's restoring `try`, and its own `finally`
  puts back only what the command changed, so an interrupt there leaves the
  module as it was read. What a person reads then is Python's traceback.
- **#312, #313, #314, #687.** These are different classes in the same file
  (J10). The first run's bound reaches only the direct child, as #313 says of
  a pair's bound. Round 1's ⬜ 7, a command that exits 0 and leaves a child
  holding the pipe, is refused as *did not return*, and it went to #313.
- **The pairs' `text=True`** was listed here as predating this item. Round 1's
  🟡 3 contested that on §12's grounds: the class is captured output decoded
  strictly, and this branch had already fixed the other member. It is fixed.
- **The stdout `errors="replace"` in the entry block is held by no case.**
  Under UTF-8 only a lone surrogate fails strictly, and one reaches stdout
  only through a module path that is not UTF-8, which this machine's APFS
  cannot create. The value is the copy five other skill scripts carry.

## Fed back into the spec

None. The section `skills/verify/SKILL.md` §`arm-check` gained the sentence
*a `killed` is a measurement only when the command passed without the
mutation*. It describes what the command does and is not a clause of this
spec.
