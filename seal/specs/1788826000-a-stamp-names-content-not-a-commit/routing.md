# 1788826000-a-stamp-names-content-not-a-commit — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/239-a-stamp-names-content-not-a-commit |

Answered 2026-09-08 by the repository owner, mid-run, on the run's standing
answer for the other items.

## Why this way

The owner moved this into 0.9.1 and put it first, on the grounds that it has
been delaying development every cycle rather than once: `0946350` is a commit
whose entire job was re-pointing three rider stamps after a rewrite, a patch
release exists for the same symptom reached from the release-to-`main`
direction, and `release/v0.9.1` went red on it again the moment #226 merged.

The direction is not open. `skills/evidence-check/SKILL.md` already cites the
riders' orphaned SHAs as one of the four grounds for deriving a ledger anchor
from content, and `CLAUDE.md` states the rule that came out of it — a row
carries no line number and no commit SHA. This work item is the migration that
decision never got, so it goes through the review chain like the rest: the
judgment to review is where the analogy stops holding, not whether to make it.

**#240 is the instance repair and is separate.** It re-points the one red stamp
so the release branch stops blocking every pull request into it; this item
removes the class.
