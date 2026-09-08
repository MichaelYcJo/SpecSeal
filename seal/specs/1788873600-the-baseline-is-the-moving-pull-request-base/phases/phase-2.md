# 1788873600-the-baseline-is-the-moving-pull-request-base — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `0aebae4` |
| Ran by | smith on `claude-opus-5[1m]` — the spawn prompt named no model; this is the harness's own model line, not a value the segment decided about itself |

## What this phase was asked

Read `docs/release-checklist.md` step 0 as part of the work: when the repair
lands, that paragraph says something the code no longer requires, and leaving
it standing is exactly #180's class. Correct it in this branch. And write
`docs/flow.md`'s 0.9.3 section — a `- [ ]` row for #272 at the top of the
list saying what it is and why it is first, and the corrected count with the
sentence that makes the grouping legible, since the method the section is
named for is what the other four share and this one is here for a different
reason. Only that section; another branch's row is what makes the file
conflict.

## What this phase found

**Eight documents stated the old footing, not one.** Enumerated by grep over
`docs/`, `skills/`, `templates/`, `CONTRIBUTING.md` and both READMEs for the
checker's name and for `base revision`: `docs/release-checklist.md`,
`docs/one-root-by-lifetime.md` and its Korean mirror, `README.md` and
`README.ko.md`, `skills/verify/SKILL.md`, `.github/workflows/hygiene.yml`,
`templates/hygiene.yml`. The module's own `--baseline` help text was a ninth
and is part of phase 1. `CONTRIBUTING.md` describes the arm without naming the
revision and needed nothing.

**Removing the workaround would have removed the never-rebase rule.**
`docs/branch-and-release.md` does not state it — `CLAUDE.md`'s merge table
implies it and does not say it — so step 0's workaround paragraph was the only
place in `docs/` that did. It is kept and rewritten as a standing rule with
its own grounds. This is the inverse of the class the phase was asked to
close: a rule surviving only inside a paragraph about something else is one
edit from gone, and that edit was this one.

**The 0.9.3 count had been wrong since #265 joined, and the fix is not a
number.** Four of the five items share the method the section is named for and
#272 does not, so the prose says which four and why the fifth is there. Left
as a corrected count alone, a reader would take #272 for a fifth instance of
enumeration-by-reading, which it is not.

**`docs/flow.md`'s preamble was left alone deliberately.** Its sizing sentence
says a release here is three or four work items and 0.9.3 now holds five. It
is outside this branch's section, that boundary is what keeps the file
mergeable, and the sentence already coexists with 0.9.1's seven. Named in the
overview's `## Not done` rather than silently passed over.

**`tests/test_release_hygiene.py` refuses a shipped file that names the
running version.** Two of the corrected paragraphs named 0.9.2, which is the
version in `plugin.json` today, and the check is right: such a line goes red
on the day that version ships. Both now say *the release that found it*. The
same sentence in `docs/flow.md` is fine, because a tracker document is
exempt — the check knows the difference and the author does not have to.

**The change drifted four rows in `seal/ledger.md`, and `--strict` fails on
drift.** The anchors were not removed, so the rule is re-read rather than
remove: `hygiene.yml`'s step anchor covers the comment above it, and so does
`templates/hygiene.yml`'s, and `unverified_check.py#main` is cited by two
rows. All four claims still hold — two were re-executed, one of them
(`--baseline … seal/spces/` still exit 2 with *no such path*) against the real
repository — and the rows carry today's date and a sentence saying what
drifted them. The new claims are in this work item's fragment, where two
branches cannot queue at one file.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/release-checklist.md` step 0's workaround: squash back to back, expect the second item to need the release branch merged in, re-run its gate, push its pull request again | Nowhere — the code no longer requires it. What it recorded that is worth keeping is in the same bullet: the never-rebase rule, restated as a standing rule, and one sentence of what the old footing cost |
| Nothing else. The `settle` scoping note in `docs/one-root-by-lifetime.md` is corrected where it named the compared revision and left standing where it names the `settle` problem, because the merge base does not answer that one | `questions.md` Q3, and the overview's `## Not done` |
