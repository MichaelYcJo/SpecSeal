# 1790550714-a-git-call-after-cd-is-charged-to-git — overview

📋 implement applied
· spec:     pending — filled when the build closes
· evidence: pending — filled at phase 3
· verified: pending — filled when the build closes

## Why this work exists

A `git` or `gh` call anywhere but the start of a Bash command read as `other`
in every `session-cost` reading, and it now reads as `git`.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The version the comparability line names | `spec.md` S10: "`--segments` prints a comparability line naming 0.15.6 and #377". `tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one` failed on it, and on the same version in `session_cost.py`'s docstring and `SKILL.md` | the line names #377 and says `CHANGELOG.md` names its release | the check's docstring: "**at or above the running version is a timer and is refused; below it is history and is kept.**" The running version is 0.15.5, so neither 0.15.5 nor 0.15.6 can be written in a loaded file before the release |
| What the tokeniser fallback decides | `spec.md` In §2: "That call is judged by today's anchored pattern". The walk is lazy, so words read before the refusal answer first | lazy walk, with the pattern for a line refused before its first word | an eager walk sends `cd /x && git log 'x` to the pattern, which answers `other`, and the spec's own grounds are that the new rule "never produces an answer worse than the old one" |

## Not verified

| Item | Who must answer |
|---|---|
| How the 0.15.5 run's own segment readings (#619) move under the new rule (`questions.md` Q1) | the owner, on the machine that holds the 0.15.5 transcripts: `session_cost.py --segments <transcript>` at 2037cf0 and at this branch's tip |
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

Nothing yet.

## Fed back into the spec

None yet.
