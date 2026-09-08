# 1788844400-a-body-naming-two-issues-claims-one — overview

📋 implement applied
· spec:     `docs/issues-and-milestones.md` §*Nothing automated reads a milestone* · `CONTRIBUTING.md` §*Running the checks*, §*What a change to a gate must carry*, §*House rules* · `CLAUDE.md` §*The goal a design is chosen against*, §*Repo rule — no real identifiers*, §*Repo rule — a change writes fragments* · `seal/follow-up.md` (read in full; no row is a prerequisite of this work and none is closed by it) · `seal/config.md` (no `Record language` row — English) · this item's own `routing.md`, `spec.md`, `plan.md`
· evidence: five rows, nine coordinates, in `seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md`
· verified: **executed** — the new module (28 passed), the three sibling modules it could disturb (49 passed with it), sixteen mutations with zero survivors, three acceptance runs against real and hand-written bodies, `evidence_check --strict` narrowed (9 ok · 0 drifted · 0 broken), `ruff check` and `ruff format --check` on both new files. **Unverified** — the full suite, the repository-wide lint and the typecheck, which are the orchestrator's

## Why this work exists

A pull request body writing a closing keyword and then two numbers in one
sentence claims the first and loses the second silently; this reports the
split at the pull request, while the author is still looking, instead of
leaving it to be noticed at the release.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the body is already read | The ticket and the handoff both say to reuse where the hygiene workflow already reads a pull request body | A first read, added to the existing job | `.github/workflows/hygiene.yml` reads `github.base_ref`, git history and files in the tree; `github.event.pull_request.body` appears nowhere in the repository. What is reused is the job — no new workflow, no new trigger, no new token scope |
| The block-boundary rule | `plan.md` §*What a sentence is* wrote rule 3 as "a line whose first non-space character is `-`, `*`, `+`, `#`, `>`, `\|`, or a `1.`-style list marker" | Every marker CommonMark requires a space after asks for one, and a whole line of `-`, `*`, `_` or `=` comes back as a break in its own right | Written that way, `#22` at the start of a line reads as a heading — and `#22` at the start of a line is this defect hard-wrapped, the one thing the module exists to see. `test_a_hard_wrapped_sentence_is_still_one_sentence` was red for exactly that, before the fix. The space requirement took the thematic break and the setext underline out of the class with it, which round 1 found as a false warning; the four whole-line alternatives put them back |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. `skills/agent-contract/SKILL.md` §2 forbids them to this segment; four modules were run narrow (`test_a_body_naming_two_issues_claims_one`, `test_docs_line_wrap`, `test_no_real_identifiers`, `test_release_hygiene`) and `ruff` was run on the two new files only | the review orchestrator, once the rounds settle |
| ✅ That the step behaves on a real GitHub runner at all: it runs first in the hygiene job, reads the body out of `env:` rather than a shell line, prints the two lists and exits 0 | measured on the run for `38cea82`, in review round 1 |
| Whether `::warning::` renders as an annotation on the job. The run on #261 cannot answer it, and naming CI as the answerer was wrong: that body claims one number and names none beside it, so the check printed its no-warning line and emitted no annotation, and the annotations API returns three for that run with none from this step. Settling it needs a pull request whose body carries the shape | the repository owner |
| Whether `github.event.pull_request.body` arrives as an empty string rather than absent for a pull request with no description. #261 has a description, so that path was not taken either, and CI cannot answer this one either. Read from GitHub's documented behaviour and from the workflow file, not executed | the repository owner |
| Whether earlier releases lost issues this way. One occurrence is measured (#162 / #150). #37, #38 and #39 are recorded in `close_issues_on_release.py`'s docstring as losing their keywords to a **different** cause — the base branch — so a survey would have to separate the two. The ticket marks this unverified and it stayed out of scope | the repository owner |

## Not done

**The stricter version was not built** — failing a release pull request whose
constituent bodies claim fewer issues than the release's milestone holds. It
needs the milestone to be trustworthy, and `docs/issues-and-milestones.md`
states in as many words that nothing automated reads a milestone and that a
wrong one costs a person a wrong answer and costs automation nothing. Making a
release depend on it turns a hand-maintained field into a release gate, and
the first wrong milestone is a red release nobody can fix in the pull request.

**`CLOSING` was not widened**, which is the repair the ticket rejects and the
reason it does: this repository would then close issues GitHub does not, and
the two would disagree about what a body means.

**The check does not travel to user repositories** through
`templates/hygiene.yml`, and does not read a closing keyword before a full
issue URL. Both are Q1 and Q3 in `questions.md` with the owner named, and both
are pinned or stated so the absence does not read as an oversight — the first
by a case, the second in `plan.md`.

**`pull_request: types:` did not gain `edited`**, so a body corrected after
the warning shows the stale warning until the next commit. Q2, with the
reasoning: `edited` re-runs every gate in the job to refresh one warning.

## Fed back into the spec

`docs/issues-and-milestones.md` gains §*A keyword claims the one number after
it* — inferred during implementation, in the sense that the rule already
existed in `close_issues_on_release.py`'s comments and had never reached the
document a person writing a pull request body would open. A planner may
overturn where it lives; the check is what enforces it either way.
