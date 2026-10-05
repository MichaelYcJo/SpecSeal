# 1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md`; `docs/the-record-layout.md` (whole); `docs/round-record-spec.md` §*The fix range*; `skills/implement/SKILL.md` §3 and §5; `skills/code-review/orchestration.md` §*Orchestrator: a fix pass resumes the implementer*; `skills/code-review/scripts/chain_check.py` module docstring, `#pact_notices`, `#fix_range`, `#main`; `skills/code-review/scripts/round_record.py#run_check`, `#under_tests`; `skills/settle/scripts/fold_check.py` on `Enforced by:`
· evidence: `seal/ledger/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named.md` — 4 rows for this work, 21 `Re-read ·` rows for released rows whose anchors this branch moved
· verified: executed — the new module, `tests/test_the_rules_have_one_owner.py`, and every module naming a touched file, plus 25 mutations of the arm and 4 of the rule's pins, every one red (the ancestor guard's after its case was corrected); read — the 21 re-read released claims

## Why this work exists

A fragment written by the build ships as a false release note when a later
commit changes what the work item ships, and 0.18.2 shipped three; now
`chain-check` names such commits and one section says the commit brings the
fragment along.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A fourth silent state | `spec.md` §*Scope*: silent where "round 1's `Target SHA` does not resolve (squashed)". The arm is also silent where it resolves and HEAD does not descend from it | the code | after a rebase the old commit still resolves, and `<target>..HEAD` would then read the build itself as late; `phases/phase-1.md` |
| A third attribution | `spec.md` names a fix range and *after the last round*. The arm also writes *outside every round's fix range* | the code | a commit between round 1's range and round 2's record is neither; calling it either would be false |
| Which `Target SHA` | spec silent on a row naming two SHAs | the first | `templates/sdd-round.md`: the second is a HEAD that moved while the round ran, which is after the build |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the rounds settle (contract §2) |
| The notice as GitHub renders it in a pull request's annotations | this item's own CI run — `round-record` on the PATH is the installed 0.18.2 and has no arm, so the orchestrator sees it only in CI or by running the tree's `round_record.py` |

## Not done

The five released fragments `spec.md` judges likely lagging (0.16.0 and
0.18.0) are left as they shipped: `questions.md` Q1, default (a), taken by the
orchestrator under the owner's `automation` routing; the owner is told at the
pull request. An acknowledgment row that would silence an honest notice was
not built (`plan.md` *Alternatives considered*).

## Fed back into the spec

None — the three divergences above are recorded here and in
`phases/phase-1.md`; `spec.md` is left as the frame drew it.
