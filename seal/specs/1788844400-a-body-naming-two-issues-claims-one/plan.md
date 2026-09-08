# Implementation Plan: a body naming two issues claims one

<!-- seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md — HOW, in phases.
The Design Gate's artifact; the routing batch that approved it is
`routing.md`, answered before the first edit. -->

## Summary

`Closes #153 and #150` claims one issue. Nothing malfunctioned: GitHub reads
the number immediately after a keyword and nothing else, and
`close_issues_on_release.py` says so in a comment two lines above its own
regex. The rule is written in the one file whose author needs it least at the
moment the prose is written.

So the repair is a check that reports the split at the pull request, where the
author is still looking, and not another sentence and not a wider regex.

## Technical context

**The hygiene workflow reads no pull request body today.** The ticket and the
handoff both say to reuse where the body is already read; opened and measured,
`.github/workflows/hygiene.yml` reads `github.base_ref`, the git history and
files in the tree — `github.event.pull_request.body` appears nowhere in the
repository. So this is a first read rather than a reuse, and what is reused is
the *job*: the step is added to the workflow that already runs on every pull
request, with no new workflow, no new trigger and no new token scope.

Existing code this builds on:

- `.github/scripts/close_issues_on_release.py#KEYWORDS`, `#CLOSING`, `#FENCE`,
  `#SPAN`, `#keywords_in` — what GitHub reads and what it does not. Imported,
  not restated.
- `.github/scripts/gather_changelog.py`, `.github/scripts/fold_ledger.py` —
  the shape a checker in this directory has: a module docstring that argues
  the design from the incident, a `--check`-style flag, stated exit codes,
  `console` imported from `hooks/` for output that is not UTF-8-dependent.
- `tests/test_release_hygiene.py#_closer` — how a `.github/scripts/` module is
  loaded into a test by path, and `#test_only_a_keyword_before_a_number_closes_anything`,
  the case that already pins the fence and span behaviour.

**What breaks in six months.** The segmentation is a heuristic over prose, so
the shape it can miss is a body that spells the two numbers further apart than
one sentence — `Closes #153. And #150 too.` reports nothing. That is the
deliberate direction (below). The failure that would actually hurt is the
opposite one, a warning on a body that is correct, because a check people
learn to scroll past is a check that is not there.

## The sentence, and what the choice gives up

The check turns on *within the same sentence*, and sentence segmentation over
prose holding `#150.`, `e.g.`, `0.9.2` and fenced code is where it would be
wrong. What was chosen:

**A segment ends at the first of:**

1. `.`, `!`, `?` or `;` **followed by whitespace or the end of the text**;
2. a **blank line**;
3. the start of a new markdown block — a line whose first non-space character
   is `-`, `*`, `+`, `#`, `>`, `|`, or a `1.`-style list marker.

Code is removed before any of that: fenced blocks and inline spans are
replaced **character for character with spaces**, so offsets and line
structure survive the masking. `close_issues_on_release.py` collapses each to
a single space, which is correct for a `findall` and wrong here — a fence
collapsing to one space would join the line above it to the line below.

**A single newline is not a boundary.** Every body in this repository is
hard-wrapped, so a sentence spans lines routinely, and `Closes #1 and\n#2` is
the defect wrapped at column 88. Treating a line as a sentence would miss it,
which was measured on PR #162's own body: its `Closes` sentence runs across
three lines.

What it gives up, stated rather than left to be found:

- **Every abbreviation splits early.** `e.g.` and `i.e.` end a segment,
  because the rule cannot tell them from a full stop without a dictionary.
  The cost is a missed warning, never an invented one — the split can only
  put two numbers in different segments, so the check under-reports.
- **`0.9.2` and `#150.` are safe**, because a full stop inside a token is not
  followed by whitespace.
- **A trailing `#N` in a table cell or a URL fragment.** A markdown table row
  starts a segment (rule 3) and `#L45`-style anchors do not match `#\d+`, but
  a six-digit hex colour outside a code span would read as issue `#123456` in
  the mention list. It is a report, not a verdict, and the warning arm needs a
  closing keyword in the same segment before it says anything.
- **A `https://github.com/o/r/issues/150` link.** GitHub reads a full URL
  after a keyword as a closing reference; this check reads only `#N`, so it
  neither claims nor mentions one. Named here rather than handled: this
  repository writes `#N`, and adding a second syntax adds a second way to be
  wrong about it.
- **An unclosed fence** masks nothing, because the fence regex needs both
  ends. The body would have to be malformed markdown to reach it.

Only a number **after** the claim is a candidate for the warning. `Part of #1,
and this closes #2` is not the shape and is not reported — which is the
false-positive direction the whole design is spending on.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Widen `CLOSING` to read `Closes #1, #2` as two | The script would then close issues GitHub does not, so the two disagree about what a body means. A person reading the body on github.com sees one linked issue and the release closes two, and nothing says which is right | **rejected** — the ticket says so and so does the script's own comment |
| The stricter version: fail a release pull request whose constituent bodies claim fewer issues than the milestone holds | Needs the milestone to be trustworthy. `docs/issues-and-milestones.md` states in as many words that nothing automated reads a milestone and that a wrong one costs a person a wrong answer and costs automation nothing. Making a release depend on it turns a field one person maintains by hand into a release gate, and the first wrong milestone is a red release nobody can fix in the pull request | **rejected — out of scope by the ticket**, and this is the reason it is out of scope |
| A rule in `CONTRIBUTING.md` or the commit-pr-convention skill instead of a check | This IS the shape of the defect: the rule is already written down, in `close_issues_on_release.py`, and the session writing a pull request body is not reading it. A second copy in a second document is the same bet at higher cost | **rejected** — one prose sentence is still added, to `docs/issues-and-milestones.md`, because that is the file a person writing a body would open; it is a signpost to the check rather than the repair |
| Fail the workflow on the warning | A false positive on prose stops a release, and the ticket's cost argument — one issue closed by hand, noticed late — does not buy that. `CONTRIBUTING.md` asks a gate to say which mistake is cheaper; here the cheap mistake is obviously the missed warning | **rejected** |
| Add `edited` to the workflow's `pull_request` trigger, so a corrected body re-runs the check | It re-runs every OTHER step of the job too — the version check, the chain check, the mode check — on every prose edit to a title or body. Those are gates; this is a warning. Paying for four gate runs so a warning can refresh is backwards | **rejected** — the warning is a report the author reads once, and correcting the body needs no green |
| Ship the step in `templates/hygiene.yml` so user repositories get it | The template's steps all call `skills/…` scripts from the plugin clone; `.github/scripts/` is this repository's own automation, and `tests/test_first_setup_asks_once.py#test_the_rows_that_read_this_repository_do_not_travel` already pins `gather_changelog` and `fold_ledger` as staying home. Shipping this means first deciding it belongs under `skills/`, which is a wider change than one measured occurrence asks for | **rejected for now**, named here so the next person does not read the absence as an oversight |
| Restate `KEYWORDS` in the new module | Two lists of what GitHub reads, drifting apart the first time one is widened. This repository has a whole test module about one word having one meaning | **rejected** — the sibling is imported |

## What this change owes as a gate

`CONTRIBUTING.md` §*What a change to a gate must carry*, answered:

- **A test seen red.** Every case in `tests/test_a_body_naming_two_issues_claims_one.py`
  is shown failing against a mutated module before it is committed, one
  mutation at a time. The record is in `phases/phase-2.md`.
- **A stated failure direction.** The check **cannot deny anything**. It has
  no verdict a pull request reads; it prints. Its only non-zero exit is 2, for
  a workflow that handed it no body at all — which is a misconfiguration the
  author can always fix, and the alternative is a step that is green having
  examined nothing, the exact failure `templates/hygiene.yml`'s own header
  argues against.
- **A prompt budget: zero.** It runs in CI and puts no question in front of
  anybody. It adds no hook, no `AskUserQuestion`, and nothing a session waits
  on.
- **Platform honesty.** No process inspection, no filesystem walk, no
  subprocess — stdlib `re` over a string. The workflow step runs on
  `ubuntu-latest` only, and the test module is pure text with no path
  assertions, so the Windows leg exercises it the same way.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `.github/scripts/issue_claims_check.py` — the reader, the segmentation, the two lists, the warning | `bin/test tests/test_a_body_naming_two_issues_claims_one.py -q`, and the check run against PR #162's live body and against a fenced quote of the failure shape | |
| 2 | Every case seen red, one mutation at a time | The mutation log in `phases/phase-2.md` | |
| 3 | The workflow step, the prose signpost in `docs/issues-and-milestones.md`, the changelog and ledger fragments | `bin/test tests/test_a_body_naming_two_issues_claims_one.py tests/test_docs_line_wrap.py tests/test_release_hygiene.py tests/test_no_real_identifiers.py -q`, `evidence_check.py --strict` on this work item's fragment | |

## Operational impact

One new step in `.github/workflows/hygiene.yml`. No new workflow, no new
trigger, no new permission — the job's token is unchanged and the check makes
no network call. Nothing to migrate, no new dependency: stdlib only, on the
supported floor.
