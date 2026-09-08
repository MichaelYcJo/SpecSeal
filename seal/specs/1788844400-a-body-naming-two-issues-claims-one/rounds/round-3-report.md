# 1788844400-a-body-naming-two-issues-claims-one — review round 3

| Field | Value |
|---|---|
| Target SHA | b0884ca50056cfe71e8a6902afad144a819867e2 |
| Ran by | warden on claude-opus-5 |
| PR | 261 |
| Broad gate | not yet — and it is now due |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | none — the fix range touches three `.md` files and no test file |

## What this round was asked

A verifying round, spawned after round 2's three `⬜` corrections were fixed
and targeted at the diff of those fixes, `d99b66d..6054165`. `b0884ca` only
closes round 2's record. Four checks, in the order the prompt set them: the
deferral's new destination, `plan.md`'s caveat, the paragraph pointer, and the
surface the fix pass itself created.

All three inherited corrections are closed. Two new `⬜` corrections and one
carried `⬜` are open, none of which needs a fix — and the exempt surface
produced the round's sharpest result, which is a note for whoever writes the
pull request body rather than a defect in the tree.

### The account, and where it did not survive contact

The fix commit's own message is a claim, and one part of it did not hold. It
declines round 2's prescribed `# RIDER:` comment on the grounds that a rider is
*"mechanism a fix pass may not add"*. That reason is not the one that matters.
The reason that matters is measurable: round 2's paste-ready rider, pasted
verbatim, turns `rider_check.py` **BROKEN** — it carries `read 2026-09-08`
where `NEW_STAMP` requires `Verified <date> against <anchor>@<hash>`. Had the
fix pass followed the prescription literally, the branch would have shipped a
broken rider. The deviation was right; the recorded reason for it was not the
one that justifies it.

### One fact the prompt handed me does not hold

The prompt states that `.github/workflows/hygiene.yml` *"runs the check on
pull requests into `main`"*. It does not. The `pull_request:` trigger at
`.github/workflows/hygiene.yml:4` carries no `branches:` filter, and the
`issue_claims_check.py` step at `:40-46` carries no `base_ref` condition —
unlike the version step immediately below it, which does test
`github.base_ref`. So the check runs on **every** pull request, including
#261, which targets `release/v0.9.2`. Round 1's own probe of the live run at
`38cea82` is the confirming measurement.

This matters for the fourth check rather than being trivia: the question *would
this branch's own pull request body report a warning* has to be asked about
#261 as it stands, not about a hypothetical release pull request.

## Findings

### 8 — the deferral now has a destination, and it is the right one

`seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md`
§Deferred

**Closed.** Both cells now name #266, and the circle round 2 found is gone.

**Does #266 state the item round 1 actually deferred?** Yes, and more
accurately than round 1 did. Round 1's Deferred row asked whether `FENCE` and
`SPAN` should cover five named shapes, and whether widening them is safe given
that it changes what a release closes. #266's title, body and *question this
needs answered before it is built* section carry exactly that, and add the
direction-of-error question round 1 left implicit.

One inherited inconsistency travelled with it, and it is row 13 below: round
1's finding title says *four* well-formed shapes while its own table, its
Deferred row and #266 all enumerate *five*.

**Is #266's enumeration correct?** Measured, not read. One input constructed
per shape, driven through `close_issues_on_release.keywords_in`, with three
controls:

| Shape | `keywords_in` result | #266 says masked |
|---|---|---|
| control — triple-backtick fence | masked | (not listed) |
| control — single-backtick span | masked | (not listed) |
| control — bare prose | let through `['150']` | (not listed) |
| a tilde fence | let through `['150']` | no |
| a four-space indented block | let through `['150']` | no |
| a fence indented inside a list item | let through `['150']` | no |
| an HTML comment | let through `['150']` | no |
| a double-backtick span | let through `['150']` | no |

All five rows of #266's table are correct, and the two controls confirm the
masking works for the two shapes it does cover. The double-backtick case is
worth naming: `SPAN` is `` `[^`\n]*` ``, so ` ``Closes #150`` ` is read as two
*empty* spans with the keyword exposed between them — the masking does not
merely miss it, it steps over it.

**Was editing a closed round record the right way to point the cell outward?**
On the mechanism, the edit changed nothing: `chain_check.verdict_of` reads both
the old cell and the new one as a closed `deferred`, because it checks only
that something follows the word. What changed is where a human reader is sent,
and that was the whole point.

On the destination, two ratified documents disagree and the fix pass engaged
with neither. `docs/review-chain-spec.md:1090` names `deferred #170` as a valid
closing form and §*The bound has a floor* sends a leftover to follow-up "or an
issue", so the tracker is an accepted home. But `seal/follow-up.md` says
**"Anything tied to a coordinate is a `# RIDER:` comment at the line it is
about"** and then, in its own words, **"An issue is no better for that purpose.
It reaches whoever browses the tracker; nobody greps the issue list before
editing a hook."** This item is tied to two coordinates.

My verdict is that #266 is the right *primary* home — the item's core is a
decision that has to be answered before any code is touched, and a decision is
what a tracker is for, where a rider is for *"if you open this file, do this
too"*. What the choice loses is the arrival, and nothing recovers it: row 12.

### 9 — `plan.md`'s caveat now states the behaviour, with one word wrong

`seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:81`

**Closed on the substance.** Round 2's `⬜ 9` was that a reader of the plan
alone did not learn that a numeric fragment beside a claim earns a warning. The
bullet now says so, and gives the reason the alternative was refused. The added
sentence also keeps the original closing sentence the paste-ready form dropped,
which is an improvement on what was prescribed.

Verified against the code rather than read. Five bodies driven through
`read()` and `report()`:

| Body | Result |
|---|---|
| `Closes #167. See https://example.com/a/b#150 for the note.` | no warning — the full stop ends the segment, so the fragment is in the next one |
| `Closes #167 as described at https://example.com/x#150 above.` | **warning**, naming `#167` and `#150` |
| `Closes #167 and the swatch is #123456 now.` | **warning** — the hex-colour case the bullet names |
| `The note is at https://example.com/a/b#150 only.` | no warning — no claim in the segment |
| `Closes #167 as described at https://example.com/x#L45 above.` | no warning — `#L45` is not `#\d+` |

The sentence describes what the code does, with one exception, which is row 11:
the fragment does not earn a warning *rather than* a mention. It earns both.

### 10 — the paragraph pointer is now correct, and uniquely so

`docs/issues-and-milestones.md:130`

**Closed.** Verified by reading the section as it stands at the target.

The section `## A keyword claims the one number after it` opens at `:112`. Its
opening paragraph is `:114-118`, and *acted on* is at `:117` — *"the 0.8.0
release acted on #153 alone"*. So the new pointer resolves to the paragraph
that says *acted on*.

No other paragraph of the section is a better referent. The section holds four
paragraphs, and the phrase occurs exactly twice in the whole file — at `:117`,
the referent, and at `:132`, the reference itself:

| Paragraph | Says *acted on* |
|---|---|
| `:114-118` the opening paragraph | yes — the referent |
| `:120` write the keyword in front of every number | no |
| `:122-128` the hygiene workflow | no — and this is what *the paragraph above* used to point at |
| `:130-134` the paragraph doing the pointing | it is the reference |

The referent is unique, so the pointer cannot be misread.

### 11 — the fragment earns a warning *and* a mention, not one instead of the other

`seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:85`, and
`.github/scripts/issue_claims_check.py:227`

A record correction, not a code defect. The bullet's emphasised sentence reads
*"earns a warning rather than a mention"*, immediately after a sentence that
puts such a number *"in the mention list"* — so a reader takes it to mean the
number leaves the mention list. It does not.

Executed. For `Closes #167 as described at https://example.com/x#150 above.`
the check prints all three lines:

    claimed (closed when the release reaches `main`): #167
    mentioned only (nothing closes these): #150
    ::warning::this sentence claims #167 and NOT #150: …

Read, at the cause: `read()` builds `mentioned` in its own loop over every
`ISSUE_REF` match, filtered only by `if number in claimed or number in
mentioned`, before the segment loop that builds `warnings` ever runs. A warned
number is never removed from `mentioned`. Nothing in the module's own docstring
claims otherwise — the docstring is silent on the interaction, so only these
two prose sites assert the exclusivity.

The output itself is honest: `mentioned only (nothing closes these)` is true of
a warned number. Only the word *rather* is wrong, and it is wrong in two
places, because the fix pass copied the phrase out of the code comment at
`:227`, where round 1's paste-ready fix first wrote it. The comment is outside
this round's fix range and carried; the plan bullet is inside it.

This is `⬜`. Behaviour is right, the release ships nothing defective, and the
location is the run's own paperwork plus a comment.

### 12 — nobody editing `FENCE` or `SPAN` will find #266

`.github/scripts/close_issues_on_release.py:69`

A `⬜` the fix pass's own choice creates, and the one thing that choice loses.

`seal/follow-up.md` states the rule and states the cost of ignoring it in the
same breath: a coordinate-tied item goes to a `# RIDER:` at the line, and *"an
issue is no better for that purpose … nobody greps the issue list before
editing a hook"*. `grep -rn "RIDER:"` at the target finds nothing in
`close_issues_on_release.py`; `rider_check.py` reports `23 ok · 0 drifted · 0
broken` over the tree, so #266 rides on nothing.

The fix pass was right not to paste round 2's rider. Executed: inserted
verbatim above `FENCE` at `:69`, with the substitution asserted before the run,
`rider_check.py` exits 2 and reports

    BROKEN   .github/scripts/close_issues_on_release.py:69: no verification
    stamp. A rider with none cannot be told from a spent one … Add
    `Verified <date> against <anchor>@<hash>`

`23 ok · 0 drifted · 1 broken`. The clone was reverted and confirmed clean.

So the gap is real and the prescribed repair was malformed. A correctly stamped
rider is row 12's paste-ready fix below, and it needs a real anchor hash, which
is why it is handed over rather than commissioned: a fix pass adding a stamped
rider to a file this branch otherwise does not touch is a code change for a
paperwork correction, and #266 already names an answerer.

This is `⬜`: no behaviour changes, no fact is wrong, and the item is filed.

### 13 — round 1's finding title still says four shapes where everything else says five

`seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md:66`

Carried, and now visible because the fix pass edited that row's other two
cells. The title reads *"four well-formed shapes the plan does not enumerate"*.
Round 1's own report tables five, its Deferred row lists five, round 1's probe
row says *"five masking gaps"*, #266 tables five, and my own measurement above
found five. The arithmetic that produces *four* is *five total, minus the
unclosed fence the plan does enumerate* — but the unclosed fence is not one of
the five listed shapes, so the subtraction does not land anywhere.

A reader who opens the row and then opens #266 sees four against five. `⬜`,
paperwork, and it is round 1's prose rather than this fix range's.

## The exempt surface — what the fix pass created

Nothing the fix pass created is an instance of what this branch checks for.
The range adds no test unit and no code; it touches three `.md` files.

**#266 written into two record cells.** Executed, over both records at the
target: `round-1.md` reports `claimed: none`, `mentioned only: #261, #266,
#162`, and the clean-body line. `round-2.md` the same with `#261` alone. No
closing keyword precedes #266 anywhere, so nothing reads it as a claim.
Nothing runs this check over round records in any case.

**#266 written into a commit message.** Executed, over the full message of
`6054165` (2,399 characters, not only the subject): `claimed: none`, `mentioned
only: #167, #266`, no warning. `close_issues_on_release.keywords_in` returns
`[]` for both messages of the range. `MERGED_PR` matches `(#167)` in each
subject, which is the squash-subject reader doing its job and not a claim.

**Would this branch's own pull request body report a warning?** No — and this
is the answer the fourth check wanted. Executed against #261's live body
(`gh pr view 261 --json body`, 5,088 characters): `claimed: #167`, `mentioned
only: none`, `no sentence claims one number and names another beside it`. #266
does not appear in the body at all.

**But a warning is one sentence away, and the chain spec asks for that
sentence.** `docs/review-chain-spec.md:177` requires a deferred finding to be
*named in the PR body*. Executed, over five wordings:

| Pull request body | Warning |
|---|---|
| `Closes #167.` — as #261 stands | no |
| `Closes #167 and defers the masking question to #266.` | **yes** |
| `Closes #167. The masking question is deferred to #266.` | no |
| `Closes #167.` then a blank line, then `Deferred: … #266.` | no |
| `Closes #167, with the FENCE and SPAN masking question deferred to #266 for the owner.` | **yes** |

**Would that warning be right or a false positive?** Right, and the check's own
message already handles it. The annotation's literal claim is true — nothing
closes #266 and it will stay open, which is exactly what should happen — and
its text offers two repairs, not one: *"Write `closes #266` in front of it, or
move it out of the sentence if it was never a claim."* The second clause is the
correct advice here, and it is there because round 1's finding 3 pinned that
string. So this is the check working, not the false-positive direction the
design forbids itself.

The practical consequence is a note for whoever writes the pull request body:
name #266 in a sentence of its own and the body stays clean.

## What I did not run

Carried as not this round's, per the prompt and contract §2, and none of it was
run: the records arm and the ledger arm of `evidence_check` (no `--reverify`),
`docs/flow.md`'s box for this branch, the full suite, unscoped
`evidence-check`, repository-wide lint and typecheck, `unverified_check.py` and
`chain_check.py` over the tree. `chain_check.verdict_of` was called as a pure
function on three cell strings, which reads no tree.

The broad gate is now due: this round leaves nothing needing a fix.

One thing I read rather than ran, and it belongs to the orchestrator. The fix
range edits `round-1.md`, a committed record. No row of
`seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md` anchors into
either round record — every coordinate in the fragment points at
`.github/scripts/issue_claims_check.py` or
`tests/test_a_body_naming_two_issues_claims_one.py` — so the edit drifts no
ledger anchor in this work item's fragment. The records arm is still the
orchestrator's to take at the closing commit.

`❓ out of verified scope` — whether the records arm of `evidence_check` hashes
round-record content, and so whether editing `round-1.md` moves its one
standing refusal at `round-1-report.md:228`. Answerer: the orchestrator, at the
closing commit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 8 | The deferral had no destination outside the record | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md` §Deferred | answered | Closed. #266 states the item round 1 deferred, and states it more accurately than round 1's own title did. Executed: one input per shape through `keywords_in` — all five of #266's shapes are let through, and the two controls are masked, so its table is correct by measurement. Executed: `chain_check.verdict_of` reads both the old cell and `deferred #266` as a closed `deferred`, so the edit changed the reader's destination and nothing mechanical. The record edit is round 2's own prescription; the destination deviates from it, and rightly — see row 12 |
| 9 | `plan.md`'s caveat described the fragment in terms of the mention list alone | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:81` | answered | Closed on the substance. Executed: five bodies through `read()` and `report()` — a claim and a numeric fragment in one segment warns, in two segments does not, `#L45` never does, and the hex-colour case the bullet names warns. The bullet now teaches that and gives the reason the alternative was refused, and it kept the closing sentence the paste-ready form had dropped. One word in it is wrong, which is row 11 |
| 10 | *the paragraph above* pointed at the wrong paragraph | `docs/issues-and-milestones.md:130` | answered | Closed. Read: the section opens at `:112`, its opening paragraph is `:114-118`, and *acted on* sits at `:117`. The phrase occurs exactly twice in the file — the referent and the reference — and none of the section's other three paragraphs carries it, so the pointer resolves uniquely. The old wording pointed at `:122-128`, the hygiene-workflow paragraph, as round 2 said |
| 11 | A numeric fragment beside a claim earns a warning **and** a mention, where two prose sites say *rather than* a mention | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:85` | open | Record correction, not a code defect. Executed: the warned number is printed in `mentioned only` and in the annotation, both. Read, at the cause: `read()` fills `mentioned` in its own loop before the segment loop builds `warnings`, and never removes a warned number. The phrase came from the code comment at `.github/scripts/issue_claims_check.py:227`, outside this fix range, so it is now wrong in two places. Behaviour and output are right; only the word *rather* is not |
| 12 | Nobody editing `FENCE` or `SPAN` will find #266, which `seal/follow-up.md` names as the cost of choosing an issue over a rider | `.github/scripts/close_issues_on_release.py:69` | open | Read: `seal/follow-up.md` sends a coordinate-tied item to a `# RIDER:` at the line and says in its own words that an issue is no better, because nobody greps the tracker before editing a file. Executed: `rider_check.py` reports `23 ok · 0 drifted · 0 broken` and no rider exists at either pattern. Executed: round 2's paste-ready rider, inserted verbatim with the substitution asserted, turns `rider_check.py` BROKEN for a missing `Verified <date> against <anchor>@<hash>` stamp — so declining it was right and the recorded reason was not the one that justifies it. Handed over rather than commissioned: the repair needs a real anchor hash, and #266 already names an answerer |
| 13 | Round 1's finding title says *four* well-formed shapes where its own table, its Deferred row, #266 and this round's measurement all say five | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md:66` | open | Carried from round 1, and visible now because the fix pass edited that row's other two cells. Read: the subtraction that produces *four* takes the unclosed fence off five, but the unclosed fence is not one of the five shapes listed. A reader who opens the row and then #266 sees four against five. Paperwork, and round 1's prose rather than this fix range's |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Row 11 — the phrase *earns a warning rather than a mention* is wrong in two places, `plan.md:85` and the code comment at `.github/scripts/issue_claims_check.py:227`. The number earns a warning AND keeps its place in the mention list | this report's paste-ready fixes, for the orchestrator to place; the code comment is outside this fix range and carried | the repository owner |
| Row 12 — no `# RIDER:` at `FENCE` or `SPAN`, so #266 reaches only whoever browses the tracker, which `seal/follow-up.md` names as the cost of that choice. A correctly stamped rider is in the paste-ready fixes and needs a real anchor hash | **#266**, which already carries the item and names an answerer; the rider is the arrival it lacks | the repository owner |
| Row 13 — round 1's finding title says four shapes where five is right | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md:66`, round 1's own prose | the repository owner |
| The two documents disagree about where a coordinate-tied leftover goes: `seal/follow-up.md` says a rider and that an issue is no better; `docs/review-chain-spec.md:1090` and §*The bound has a floor* name the tracker as a home | neither document was changed, and this round did not settle it | the repository owner |

## Paste-ready fixes

Row 11 — `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md`,
replacing the emphasised sentence:

```markdown
  the mention list. **A numeric fragment sitting in the same segment as a
  claim earns a warning as well as its place in that list**, which is the same
  syntax read the same way: the alternative, excluding a `#N` preceded by a
  URL character, would be a second syntax to be wrong about. It is a report,
  not a verdict, and the warning arm needs a closing keyword in the same
  segment before it says anything.
```

Row 11 — `.github/scripts/issue_claims_check.py`, the same correction in the
comment the phrase came from:

```python
        # The candidate is any `#N`, which is what the mention list already
        # says: a hex colour or a link ending `#22` reads as an issue number
        # here too, and beside a claim in the same sentence it earns a warning
        # as well as its place in that list -- the mention line is still true
        # of it, because nothing closes it. The alternative -- excluding a
        # `#N` preceded by a URL character -- is a second syntax to be wrong
        # about.
```

Row 12 — `.github/scripts/close_issues_on_release.py`, above the `FENCE`
pattern. `<hash>` is the eight hex characters `rider_check.py --reverify`
computes for the anchor; the rider is BROKEN until a real one is written, which
is why this is handed over rather than pasted blind:

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

Row 12 — the alternative, if the owner would rather not add a rider: nothing to
paste, and #266 stays a tracker-only item. Recording the choice is what row 12
asks for either way.

## Proof

Files opened in the clone at `b0884ca`:

- `.github/scripts/issue_claims_check.py`
- `.github/scripts/close_issues_on_release.py`
- `.github/scripts/rider_check.py`
- `.github/workflows/hygiene.yml`
- `docs/issues-and-milestones.md`
- `docs/review-chain-spec.md`
- `bin/test`
- `seal/follow-up.md`
- `seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md`
- `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md`
- `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md`
- `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1-report.md`
- `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-2.md`
- `skills/code-review/scripts/chain_check.py`
- `tests/test_a_rider_reaches_its_file.py`

Read outside the clone: issue #266 (`gh issue view 266`), PR #261's body
(`gh pr view 261 --json body`).

Needs a fix: no
Loses a record or crashes: no
