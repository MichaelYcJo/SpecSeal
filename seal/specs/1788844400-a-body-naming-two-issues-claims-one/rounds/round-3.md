# 1788844400-a-body-naming-two-issues-claims-one — review round 3

| Field | Value |
|---|---|
| Target SHA | b0884ca |
| Ran by | warden on claude-opus-5 |
| PR | 261 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A verifying round, spawned after round 2's corrections were committed and
targeted at the diff of those corrections: `d99b66d..6054165`, plus `b0884ca`,
which only closes round 2's record. Its job was stated as round 2's three ⬜
answers rather than new findings, with one surface exempt — what the fix pass
itself created. The cap's last round, and it was told so.

Four checks, in the order the prompt set them.

1. **⬜ 8 — the deferral now has a destination, and the destination has to be
   the right one.** Round 1's finding 5 verdict cell and the record's own
   `Deferred` row had pointed at each other; both now name #266. The round was
   asked to read that issue and judge three things: whether it states the item
   round 1 actually deferred, whether its enumeration of the five shapes is
   correct against `FENCE` and `SPAN` — measured by constructing one input per
   shape rather than by reading — and whether editing a closed round record was
   the right way to point the cell outward, given the reviewer's own
   alternative was a `# RIDER:` comment at both patterns.
2. **⬜ 9 — `plan.md`'s caveat.** The bullet now states what a numeric fragment
   beside a claim earns, and why the alternative was refused. The round was
   asked to verify the behaviour against `issue_claims_check.py` by feeding it
   such a body, not by reading the code.
3. **⬜ 10 — the paragraph pointer**, and whether the section's opening
   paragraph is in fact the one that says *acted on*.
4. **The exempt surface, with a question this branch's own subject makes
   sharp**: the fix pass wrote #266 into two record cells and a commit message,
   and this branch ships a check that reads issue numbers out of a pull request
   body. The round was asked whether anything the fix pass wrote is itself an
   instance of what the branch checks for, and whether this branch's own pull
   request body would now report a warning — and if so, whether that warning
   would be right.

Carried as not the round's to close: the records arm and the ledger arm, which
the orchestrator takes at the closing commit; `docs/flow.md`'s box; and the
broad gate under contract §2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 8 | The deferral had no destination outside the record | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md` §Deferred | answered | Closed. #266 states the item round 1 deferred, and states it more accurately than round 1's own title did. Executed: one input per shape through `keywords_in` — all five of #266's shapes are let through, and the two controls are masked, so its table is correct by measurement. Executed: `chain_check.verdict_of` reads both the old cell and `deferred #266` as a closed `deferred`, so the edit changed the reader's destination and nothing mechanical. The record edit is round 2's own prescription; the destination deviates from it, and rightly — see row 12 |
| 9 | `plan.md`'s caveat described the fragment in terms of the mention list alone | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:81` | answered | Closed on the substance. Executed: five bodies through `read()` and `report()` — a claim and a numeric fragment in one segment warns, in two segments does not, `#L45` never does, and the hex-colour case the bullet names warns. The bullet now teaches that and gives the reason the alternative was refused, and it kept the closing sentence the paste-ready form had dropped. One word in it is wrong, which is row 11 |
| 10 | *the paragraph above* pointed at the wrong paragraph | `docs/issues-and-milestones.md:130` | answered | Closed. Read: the section opens at `:112`, its opening paragraph is `:114-118`, and *acted on* sits at `:117`. The phrase occurs exactly twice in the file — the referent and the reference — and none of the section's other three paragraphs carries it, so the pointer resolves uniquely. The old wording pointed at `:122-128`, the hygiene-workflow paragraph, as round 2 said |
| 11 | A numeric fragment beside a claim earns a warning **and** a mention, where two prose sites say *rather than* a mention | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:85` | deferred #268 | #268 |
| 12 | Nobody editing `FENCE` or `SPAN` will find #266, which `seal/follow-up.md` names as the cost of choosing an issue over a rider | `.github/scripts/close_issues_on_release.py:69` | deferred #268 | #268 |
| 13 | Round 1's finding title says *four* well-formed shapes where its own table, its Deferred row, #266 and this round's measurement all say five | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md:66` | deferred #268 | #268 |

## Paste-ready fixes

```markdown
  the mention list. **A numeric fragment sitting in the same segment as a
  claim earns a warning as well as its place in that list**, which is the same
  syntax read the same way: the alternative, excluding a `#N` preceded by a
  URL character, would be a second syntax to be wrong about. It is a report,
  not a verdict, and the warning arm needs a closing keyword in the same
  segment before it says anything.
```
```python
        # The candidate is any `#N`, which is what the mention list already
        # says: a hex colour or a link ending `#22` reads as an issue number
        # here too, and beside a claim in the same sentence it earns a warning
        # as well as its place in that list -- the mention line is still true
        # of it, because nothing closes it. The alternative -- excluding a
        # `#N` preceded by a URL character -- is a second syntax to be wrong
        # about.
```
```python
# RIDER: Verified 2026-09-08 against FENCE@<hash>
# Review round 1 of work item 1788844400 measured five well-formed shapes
# these two patterns give up: a tilde fence, a four-space indented block, a
# fence indented inside a list item, an HTML comment, and a double-backtick
# span. A closing keyword inside any of them is read as a claim, so a release
# closes the issue. Widening them changes what a RELEASE closes and not only
# what issue_claims_check.py reports, which is the decision issue #266
# carries. If you open these two patterns, answer it there first.
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository into a scratch path; `git rev-parse HEAD` before and after every step | `b0884ca` throughout; the clone ended clean with 0 modified files |
| Five shapes plus three controls, one constructed input each, through `close_issues_on_release.keywords_in` | all five let the keyword through; triple-backtick fence and single-backtick span masked; bare prose let through. #266's table is correct row for row |
| Five bodies through `issue_claims_check.read()` and `report()`: claim plus numeric fragment in one segment, in two segments, hex colour, fragment with no claim, `#L45` anchor | warning on the two that put a claim and a `#\d+` in one segment; none on the other three. The warned number appears in `mentioned only` as well as in the annotation |
| `issue_claims_check.py` over PR #261's live body (`gh pr view 261 --json body`, 5,088 characters) | `claimed: #167` · `mentioned only: none` · `no sentence claims one number and names another beside it`. #266 is absent from the body |
| `issue_claims_check.py` over five candidate pull request bodies naming #266 | warning on the two that name it inside the claiming sentence; clean when it sits in its own sentence or its own block |
| `issue_claims_check.py` over the four documents the branch touches: `docs/issues-and-milestones.md`, `plan.md`, `round-1.md`, `round-2.md` | no warning on any; `round-1.md` mentions `#261, #266, #162` and claims none |
| `issue_claims_check.py` and `keywords_in` over the FULL commit messages of `6054165` (2,399 characters) and `b0884ca` | `claimed: none` · no warning on either; `keywords_in` returns `[]` for both. `MERGED_PR` matches `(#167)` in each subject, which is the squash-subject reader |
| Round 2's paste-ready `# RIDER:` inserted verbatim above `FENCE` at `close_issues_on_release.py:69`, with the substitution asserted before the run, then reverted | `rider_check.py` exit 2 · `BROKEN … no verification stamp` · `23 ok · 0 drifted · 1 broken`. The clone reverted clean. Without the insertion: `23 ok · 0 drifted · 0 broken` |
| `chain_check.verdict_of` on `deferred #266`, on the old record-internal cell, on a bare `deferred`, and on `**fixed** `6054165`` | `deferred` (closed), `deferred` (closed), `deferred (no home)` (open), `fixed` (closed) — the checker accepted the old cell too |
| `./bin/test tests/test_a_body_naming_two_issues_claims_one.py tests/test_docs_line_wrap.py -q`, exit code read directly | 68 passed, exit 0. Every `__pycache__` cleared before the run |
| `.github/workflows/hygiene.yml` trigger and step conditions, read | `pull_request:` at `:4` carries no `branches:` filter and the check step at `:40-46` no `base_ref` condition, so the check runs on every pull request — the prompt's *into `main`* does not hold |
| `docs/issues-and-milestones.md` section structure and every occurrence of *acted on*, read | section opens `:112`; opening paragraph `:114-118` with *acted on* at `:117`; the phrase occurs twice in the file, the referent and the reference |
| `seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md` grepped for anchors into either round record, read | none — every coordinate points at `issue_claims_check.py` or the branch's test module, so editing `round-1.md` drifts no anchor in this fragment |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/issue_claims_check.py:107` | round 1's 1 — fixed |
| round-1 | `docs/issues-and-milestones.md:117` | round 1's 2 — fixed |
| round-1 | `.github/scripts/issue_claims_check.py:208` | round 1's 3 — fixed |
| round-1 | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/overview.md:27` | round 1's 4 — answered |
| round-1 | `.github/scripts/issue_claims_check.py:123` | round 1's 5 — deferred |
| round-1 | `.github/scripts/issue_claims_check.py:199` | round 1's 6 — fixed |
| round-2 | `.github/scripts/issue_claims_check.py:116` | round 2's 1 — answered |
| round-2 | `.github/scripts/issue_claims_check.py:240` | round 2's 3 — answered |
| round-2 | `.github/scripts/issue_claims_check.py:130` | round 2's 5 — answered |
| round-2 | `.github/scripts/issue_claims_check.py:229` | round 2's 6 — answered |
| round-2 | `.github/scripts/issue_claims_check.py:224` | round 2's 7 — answered |
| round-2 | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md` §Deferred | round 2's 8 — fixed |
| round-2 | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:81` | round 2's 9 — fixed |
| round-2 | `docs/issues-and-milestones.md:130` | round 2's 10 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Row 11 — the phrase *earns a warning rather than a mention* is wrong in two places, `plan.md:85` and the code comment at `.github/scripts/issue_claims_check.py:227`. The number earns a warning AND keeps its place in the mention list | this report's paste-ready fixes, for the orchestrator to place; the code comment is outside this fix range and carried | the repository owner |
| Row 12 — no `# RIDER:` at `FENCE` or `SPAN`, so #266 reaches only whoever browses the tracker, which `seal/follow-up.md` names as the cost of that choice. A correctly stamped rider is in the paste-ready fixes and needs a real anchor hash | **#266**, which already carries the item and names an answerer; the rider is the arrival it lacks | the repository owner |
| Row 13 — round 1's finding title says four shapes where five is right | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md:66`, round 1's own prose | the repository owner |
| The two documents disagree about where a coordinate-tied leftover goes: `seal/follow-up.md` says a rider and that an issue is no better; `docs/review-chain-spec.md:1090` and §*The bound has a floor* name the tracker as a home | neither document was changed, and this round did not settle it | the repository owner |
