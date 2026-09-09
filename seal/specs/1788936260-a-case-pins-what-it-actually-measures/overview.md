# 1788936260-a-case-pins-what-it-actually-measures — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` of this work item · `CLAUDE.md` §*verification that runs unattended*, §*a change writes fragments, never the shared file* · `CONTRIBUTING.md` §*What a change to a gate must carry* · `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it* (via `spec.md`'s grounding) · `seal/config.md` (no `Record language` row → English) · `seal/follow-up.md` (no row is a prerequisite of this work) · `tests/test_chain_hooks.py#reader_blanking_passes` as the named precedent
· evidence: `seal/ledger/1788936260-a-case-pins-what-it-actually-measures.md` — 9 rows, the last three added by round 1's fix pass
· verified: executed — 43 cases in `tests/test_arm_check.py`, 51 counting the parametrized one's arms, each seen red against a mutation of the checker; the #310 case red on all five of its arms and green unmutated; the checker's first run over `hooks/review-history-guard.py`. Read — #262's and #310's bodies, and the two commits the ticket's table predates. Unverified — the full suite, the repository-wide lint and the typecheck (contract §2: the orchestrator's, once, after the rounds), and every platform but macOS.

## Why this work exists

A case that asserts vocabulary pins a phrase where the claim it was written
for is a ranking or a direction, and a count of a module's branches taken by
hand rots the moment the module changes; #310 is one instance and #262 is the
same failure at module scale, so the answer to the second is a checker that
derives the list rather than nine more cases.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The module's arm total | `spec.md` and the handoff both say **31**, split across four functions. The walk finds **32** | Report 32, with the per-function split matching the handoff exactly and the extra arm named under `<module>` | Both hand counts are per-function tables, so `if __name__ == "__main__":` had nowhere to be written down. The enumeration going LONG is the safe direction, and the spec's own scenario is that the count moves when the module holds another arm. `spec.md`'s 31 is not wrong — it is 31 arms inside functions, which the walk reproduces exactly |
| Which arm shapes count | #262's rule names four: `ExceptHandler`, `If`, `While`, `IfExp` | Six — `match_case` and `comprehension` added | `plan.md`'s own failure scenario names them: *"a new arm shape the walk does not know, a `match` statement, a comprehension guard."* Adding them changes no number here, because the module has neither, so the 31 is reproducible under either rule |
| Phase boundaries in git | `plan.md` lists phases 2 and 3 as separate rows | One commit for both, two phase records | Splitting them would have committed the mutation machinery with no case behind it, which is the one thing the phase after it exists to prevent. Both records name the same commit and each says what it delivered |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Contract §2 reserves the broad gate for the orchestrator, run once after the review rounds settle. Nine test modules were run — the ones my edits touch and the ones I added cases to | the review orchestrator |
| Windows and Linux. Executed on macOS (darwin 25.5.0, CPython 3.12.11) only. `bin/arm-check.cmd` is transcribed from `bin/survivor-check.cmd` and has not been run; the two platform-specific hazards the code handles (`col_offset` as a UTF-8 byte offset, and cached bytecode under `sys.pycache_prefix`) are handled by construction rather than by measurement off-platform | CI's windows and linux legs |
| What the checker's exit code should mean — `questions.md` Q1. The code is report-only today, exit 0 whether or not an arm survived, which is the first of the three answers | the repository owner |
| Whether the arms this run reports as unwatched are gaps or behaviour-preserving. `spec.md` puts it out of scope and #262 already names two of the latter kind | a later work item, informed by the run recorded in `changelog.md` |
| Whether any other case in the tree pins a document clause by substring where the claim carries a ranking or a direction — #310's own `Not verified` row, inherited unanswered. This work item fixed the one instance and did not sweep the class | whoever builds that sweep (#310 remains open on it) |

## Not done

**The nine hand-written cases for the unwatched arms.** Refused by name in
`spec.md`, and it is the whole reason #262 exists.

**A run over any module but `hooks/review-history-guard.py`.** That one has a
measured expectation to check the walk against; a sweep is a second work item
with its own numbers, and `spec.md` puts it out of scope.

**The exit rule.** Built as report-only and left there deliberately —
`questions.md` Q1 says the other two answers both need the first run's number
to exist first, and this is the run that produces it. The behaviour is pinned
by a case, so changing it later is a decision somebody has to make rather than
an edit that can slip through.

**#262's table of 33 is not corrected.** `questions.md` assumption 3: it was
true when measured, the file changed twice afterwards, and correcting a shipped
ticket's measurement would hide the argument the ticket makes.

**`PYTHONDONTWRITEBYTECODE` and the restore at the end of the run are two arms
no case kills**, and they are reported rather than removed — the checker's own
verdict applied to itself. Each is the redundant half of a pair whose property
is pinned; `phases/phase-3.md` and the code at both coordinates say what only
that half covers.

## Fed back into the spec

None. Every clause this work leaned on was already written: #262's counting
rule, `plan.md`'s refusal-not-skip requirement, and `questions.md`'s three
assumptions. What the work added is a mechanism and its record, not a new
norm — and the one norm-shaped sentence, that `arm-check` asks condition 2 of
a whole module, went into `skills/verify/SKILL.md` §2 rather than here.
