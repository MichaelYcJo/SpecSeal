# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — overview

📋 implement applied
· spec:     filled when the build closes
· evidence: filled when the build closes
· verified: filled when the build closes

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

## Not verified

| Item | Who must answer |
|---|---|
| S11 — `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` green on the tree holding both this branch and #641's, and `mutation_check.py`'s three `clear_bytecode_cache(path)` calls given `cwd=cwd` (`questions.md` Q1) | the orchestrator of whichever branch lands second on `release/v0.17.0`, with that module's narrow run |
| The full suite, the repository-wide lint and the typecheck | the orchestrator, through the sealer after the review rounds settle |
| S10's two CI legs, `arm-check-grammar (3.13)` and `(3.14)`, and the Windows leg of `pytest` | the pull request's checks |

## Not done

Filled when the build closes.

## Fed back into the spec

Filled when the build closes.
