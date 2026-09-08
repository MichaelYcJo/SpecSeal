# Feature Specification: a body naming two issues claims one

<!-- seal/specs/1788844400-a-body-naming-two-issues-claims-one/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/issues-and-milestones.md` §*Nothing automated reads a milestone* | Says what closes an issue here — a keyword in a pull request body, read by `close_issues_on_release.py` — and that a missing `Closes #N` costs an issue that stays open forever. It does not yet say that a SECOND number in the same sentence is not a second claim, which is this defect |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Four things a change to a check owes: a test seen red, a stated failure direction, a prompt budget, platform honesty. Answered in `plan.md` §*What this change owes as a gate* |
| `CLAUDE.md` §*The goal a design is chosen against* | Verification through an automated workflow is the first goal. A check that reports at the pull request is the automated form of the sentence already written in `close_issues_on_release.py` |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | The fixtures for this check are pull request bodies, which is exactly where a real org, repo or session URL gets inlined. PR #162's real body is **not** committed |

## Scope

**In.** A script that reads one pull request body and reports, in two lists,
every issue number the body **claims** (a closing keyword immediately before
the number, as GitHub itself reads it) and every number it merely
**mentions**. Where a claimed number is followed, in the same sentence, by an
unclaimed `#N`, it prints a `::warning::` naming both — the `Closes #153 and
#150` shape. It is wired into `.github/workflows/hygiene.yml`, which already
runs on every pull request.

**Out.**

- **Widening `CLOSING`.** GitHub claims the one number after the keyword and
  so does this repository's closer. Widening it would make the script close
  issues GitHub does not, and the two would then disagree about what a body
  means — worse than the loss it repairs.
- **Failing a pull request.** The check reports. A check that fails on prose
  stops a release for a false positive, and one measured occurrence does not
  carry that cost.
- **The stricter version** — failing a release pull request whose constituent
  bodies claim fewer issues than the release's milestone holds. It needs the
  milestone to be trustworthy, and `docs/issues-and-milestones.md` says in as
  many words that nothing automated reads a milestone. `plan.md`
  §*Alternatives considered* carries the rejection.
- **A survey of past releases.** #37, #38 and #39 lost their keywords to a
  different cause (the base branch), so separating the two causes is its own
  reading. The ticket marks it unverified and leaves it there.
- **Shipping the check to user repositories** through `templates/hygiene.yml`.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The measured instance | Given PR #162's real body, which writes `Closes #153 and #150` / When the check reads it / Then `#153` is reported claimed, `#150` mentioned, and one warning names the sentence | Executed against the live body fetched with `gh pr view 162`. Not committed as a fixture — it carries a session URL on a domain outside the fixture allowlist, which `tests/test_no_real_identifiers.py` refuses |
| The comma spelling | Given `Closes #1, #2` / When the check reads it / Then `#1` is claimed, `#2` mentioned, one warning | `tests/test_a_body_naming_two_issues_claims_one.py` |
| A body quoting the failure inside a fence | Given a body whose fenced block holds `Closes #1, #2` as an example of the defect / When the check reads it / Then it reports nothing at all — no claim, no mention, no warning | Same module, and executed against a hand-written body |
| A body quoting it in an inline span | Given `` see `Closes #1, #2` in the ticket `` / Then nothing is reported | Same module |
| Two keywords, no loss | Given `Closes #1 and closes #2` / Then both are claimed and no warning is printed | Same module |
| A hard-wrapped sentence | Given `Closes #1 and\n#2` — one sentence across two lines, which is how every body in this repository is written / Then the warning still fires | Same module. This is what rules out "a line is a sentence" |
| A separate paragraph | Given `Closes #1` and, after a blank line, `#2 is unrelated` / Then no warning | Same module |
| A separate list item | Given `- Closes #1` then `- #2 is next`, with no blank line between them / Then no warning | Same module |
| A number before the keyword | Given `Part of #1, and this closes #2` / Then no warning — only a number AFTER a claim is a candidate | Same module |
| A body with nothing to say | Given a body with no `#N` at all / Then it prints that and exits 0 | Same module |
| The workflow never blocks on prose | Given any body / When the step runs / Then the exit code is 0 | Same module, over every fixture above |
| A step that examined nothing is not green | Given the workflow step with no `PR_BODY` in its environment at all / Then it exits 2 and says the workflow is misconfigured | Same module |
| One definition of a closing keyword | Given someone widens `CLOSING` in `close_issues_on_release.py` / Then this check moves with it, because it imports that object rather than restating it | Same module, by identity (`is`) |

## Data & interfaces

```
.github/scripts/issue_claims_check.py            # reads PR_BODY from the environment
.github/scripts/issue_claims_check.py --body-file <path>
```

Exit codes: **0** for every body it read, whatever it found. **2** when it was
given no body to read at all — neither `PR_BODY` in the environment nor
`--body-file`.

It imports `KEYWORDS`, `CLOSING`, `FENCE` and `SPAN` from
`close_issues_on_release.py`, its sibling in the same directory, so the
definition of *what GitHub reads* has one home.

The workflow passes the body through `env:`, never interpolated into a `run:`
line. A pull request body is attacker-controlled text and `${{ }}` inside
`run:` is textual substitution into a shell script.

## Open questions → questions.md

`questions.md` carries what a person decides, not this file.
