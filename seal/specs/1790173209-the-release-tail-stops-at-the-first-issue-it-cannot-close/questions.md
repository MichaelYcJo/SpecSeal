# the release tail stops at the first issue it cannot close — questions for the planner

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Decided from the tree — do not reopen

The tickets left these open; the repository answered them. Grounds are in
`spec.md` §Scope and `plan.md` §Alternatives.

1. **#266 — which direction is the error.** Masks more, closes fewer. The
   closer's own docstring states the premise it mirrors (GitHub creates no
   reference inside a fence or a span), so widening toward it is a fix; an
   unclosed issue is visible and re-runnable, a wrong close is a false record.
2. **#266 — whether the check and the closer share one pattern.** They already
   do: `issue_claims_check.py:90` imports `FENCE` and `SPAN`, and a case
   asserts identity. Widening the closer widens the check.
3. **#266 — all five shapes or the ones that occur.** Three: tilde fence,
   indented fence, double-backtick span. A four-space block is a bullet
   continuation in this repository's bodies; the HTML comment is row Q1 below.
4. **#289 — append or refuse.** Append into the existing section, keeping the
   first gather's date; a hygiene case refuses a duplicated heading.
5. **#198 — comment, summary line, or refusal.** Never refusal (the ticket's
   *Done when* and `CLAUDE.md`'s first goal). All of: the old log's close
   comment, the new log's body, and the job's output.
6. **#362 — which boundary.** The five the step must pass, in both places,
   with a re-measured table and no count.
7. **#368 — nothing to decide.** Shipped in `fc3e1175` (#440). The caller
   closes the ticket naming that commit.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does GitHub act on a closing keyword written inside an HTML comment (`<!-- Closes #N -->`) in a pull request body whose base is the default branch? The tree cannot answer it: the closer's premise names fences and spans only, and no document here measured a comment. | a measurement — a scratch pull request into a scratch repository's default branch with the keyword inside a comment, then `gh pr view --json closingIssuesReferences`. Not on this tracker. | *yes* → the shape stays unmasked (today's reading is right). *no* → a later change masks it, in the deny direction, with its own case. | unmasked, stated at the pattern | ⬜ |
| Q2 | Which read gives the roll the comment count with the least change to the module's fakes: `gh issue list --json number,title,comments` on the one list call, or `gh api repos/<owner>/<repo>/issues/<n>` through `try_run`? | the work — phase 6, by reading the fakes in `tests/test_a_release_rolls_the_flow_measurement_issue.py` | Either is one read and no write. The fakes match on argv prefix, so the choice is whichever prefix they already answer. | the list call's `--json` | ⬜ |
| Q3 | Why did `gh issue close 515` fail on the GraphQL route twice while REST closed it at once? | a measurement, and it does not block: phase 1's fallback is built for the class (one route refusing), not for the cause. If the cause is found it goes in `phases/phase-1.md`; if not, the record says so. | *a `gh` build defect* → nothing here changes. *something about #515* → nothing here changes. | unknown, stated | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **This file has none.**
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
