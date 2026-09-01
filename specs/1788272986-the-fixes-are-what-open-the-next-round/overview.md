# 1788272986-the-fixes-are-what-open-the-next-round — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show goes here; each part is written when it happens. -->

📋 implement applied
· spec:     issue #57 (full body), docs/review-chain-spec.md,
            docs/review-handoff-protocol.md, skills/code-review/SKILL.md,
            agents/warden.md, agents/smith.md §Phases, CONTRIBUTING.md §What a
            change to a gate must carry, chain_check.py's docstrings
· evidence: .specseal/map/1788272986-the-fixes-are-what-open-the-next-round.md
· verified: see Not verified below; executed vs. read labeled per row in the
            ledger fragment

## Why this work exists

Ten regressions on one work item each traced to the fix that opened them, and
the largest class — a changed contract whose reach nobody revisited — is a
`grep` away; after this change the reach is a row `chain_check.py` refuses to
lose, and the units a fix creates are a surface the verifying round is told
to judge as code.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| none | | | |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ This branch's own round records carrying the new rows | rounds 1–3 written with both rows, parsed clean by `chain_check.py` in rounds 2 and 3; session of 2026-09-02 |
| ✅ `chain_check.py` on this pull request end to end | CI's invocation run locally at 55812d2 under ready-PR judgment, exit 0, all three rounds parsed; the PR's own CI run re-executes it. Session of 2026-09-02 |

## Not done

The round cap's numbers are untouched, per the issue's scope note. The
warden's report format gains no new line: the fix-surface rows are written by
the session with the fix diff open (smith or orchestrator), not copied from
the reviewer's report, so there is nothing for the reviewer to emit.

## Fed back into the spec

The `Contract changes` entry syntax (`;` between units, `→`/`->` before the
reach) is inferred during implementation — issue #57 gives the semantics
only. Marked in `questions.md` Q1 so a planner can overturn it.
