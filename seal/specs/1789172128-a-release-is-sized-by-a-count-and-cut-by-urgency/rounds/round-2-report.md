# round 2 — the verifying round's report

| | |
|---|---|
| Work item | `1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency` |
| Target | the diff of round 1's fixes, `a0f0e9a..941dab5` |
| Reviewed at | `941dab5` |
| Base of the branch | `origin/release/v0.11.1` = `7e17f5e` |
| Reviewed in | a `git clone --no-local` of the repository, checked out at `941dab5` |
| Ran by | specseal:warden on Opus 5 |
| Migration config | none — no `seal/parity.md`, so no parity comparison and no parity mark |

Where this report says a check was run, it was run in that clone and the exit
code was read directly with no pipe. Where it says something was read, it was
read.

## The answers to round 1's nine verdicts

Six are closed. Three are not what the record says.

| # | Round 1's verdict | This round's answer |
|---|---|---|
| 1 | fixed `ea4fc64` | **partly.** The conflation is gone and the operative instruction is now right. The replacement carries a new false claim about which release the other label goes on — finding 1 |
| 2 | fixed `ea4fc64` | **partly.** The wrap gap is closed for one line boundary and the owner is now skipped before the regex runs, both measured. The half that says the self-exclusion is by path was not applied — finding 4 — and nothing in the tree pins the fix — finding 2 |
| 3 | fixed `ea4fc64` | **closed as to the pattern**, and its disclosure re-derived rather than inherited. Unpinned, which is finding 2 |
| 4 | fixed `ea4fc64` | **closed.** The clause is at `docs/issues-and-milestones.md:138-141` and says what round 1 asked it to say |
| 5 | fixed `941dab5` | **closed.** The row now records what the command answers, and the phase record's treatment is right. One new false clause entered the same row — finding 4's second location |
| 6 | fixed `941dab5` | **closed.** Both records say two rows; the fragment carries S1 and S5b |
| 7 | fixed `941dab5` | **first half closed, second half is not what the record says.** The marking reads correctly in the released section. The exemption it is supposed to be anchored on is not engaged and would not match — findings 3 and 5 |
| 8 | answered | **closed and unchanged.** `seal/specs/…/spec.md:159` still quotes `@95e3a483`, and the drift reproduces exactly as round 1 recorded it |
| 9 | fixed `941dab5` | **closed.** `CLAUDE.md` is in the scanned set, 170 files, no offender. Unpinned, which is finding 2 |

## What the fix pass claimed, and what the code said

Five claims were re-derived rather than inherited. Three hold. Two do not.

- **Claimed** that the widened pattern catches the three noun forms round 1
  measured escaping, and that the replaced sentence is still caught.
  **Re-derived by execution.** All three match, and so does the replaced
  sentence.
- **Claimed** that nothing in the scanned set matches `is the size` today
  outside the module and the owner — the measurement with a shelf life.
  **Re-derived at `941dab5`, per alternative rather than as a whole.** Four
  lines match it, all inside `tests/test_a_release_is_sized_by_a_criterion.py`.
  `release's size` matches the owner once and the module seven times;
  `size of a release` matches the module twice. Both of those files are
  excluded. The claim holds, and the constant states it as *at the time it was
  added* rather than as a present fact, which is the honest form.
- **Claimed** that `git grep -n "is the size"` over the set the row names exits
  0 with every hit inside the module. **Re-derived**: exit 0, four hits, all in
  that module.
- **Claimed** that `bin/survivor-check` exits 0 with every survivor excused.
  **It exits 0 because nothing is reported at all.** Finding 3, and the
  measurement that produced it is the one thing in this round worth the
  orchestrator's own reading.
- **Claimed** that the three code-side fixes were closed by correcting the unit
  and that a probe stood in for a case. **Measured**: each of the three can be
  reverted and the module stays green. Finding 2.

## 🟡 1 · the new sentence puts the other label a release earlier than it goes on

`docs/issues-and-milestones.md:152-155`. The paragraph now reads *Not when
`merged: X.Y.Z` goes on, which §A label says a ticket is already in, before the
release ships puts at the **push to `release/*`, a release earlier***.

The section it cites says the opposite of *a release earlier*, and so does the
other document round 1 sent the fix to read.

- `docs/issues-and-milestones.md:208` is that section's own title: *A label
  says a ticket is already in, **before the release ships***. Before it ships,
  not a release before it.
- `docs/issues-and-milestones.md:210-211`: *An issue's state does not move
  until `main` moves, and `main` moves once per release. So **for the length of
  a release** a finished work item and one nobody has started look identical.*
- `docs/branch-and-release.md:256-258`: `merged: X.Y.Z` *is the answer to* is
  this in yet, *which the paragraph above leaves open **for the length of a
  release**; the answer to* is this done *is still the close, still when `main`
  moves.*

So both moments sit inside one release. A ticket squashed into
`release/v0.11.1` gets `merged: 0.11.1` at that push, and `size: now` comes off
when `release/v0.11.1` reaches `main`. Nothing ships in between. The gap is a
step inside one release, and the version in the other label's own value names
that same release.

What this costs: the sentence's instruction is right and its reason is wrong,
so a reader who uses the reason to work out anything else gets a wrong answer —
that `merged: 0.11.1` was applied during 0.11.0, and therefore that a ticket
carrying it is in the release before the one its value names. This is the
document that owns tracker conventions, it is the same class of defect round 1
opened as finding 1, and it entered in the commit that answered it. No check
reads either label, so nothing else will catch it.

Round 1's own report used the phrase *one release early* for the same relation,
so the wording was inherited rather than invented. That is why it is reported
here rather than treated as settled: the decision round 1 made was *anchor on
the later moment and name the other one*, and it did not include a claim about
the distance between them.

## 🟡 2 · all three code-side fixes revert with the module still green

`tests/test_a_release_is_sized_by_a_criterion.py`. `agent-contract` §15 — a new
case is not planted until it has been seen red — and the fix pass recorded the
opposite decision explicitly: *No case was added to pin findings 2 or 3 — both
were closed by correcting the unit, and the corrected unit is measured by the
probe rather than by a new test.* The probe is deleted, which is what §7
requires of it, so what is left in the tree is a module that answers the same
way with the fixes and without them.

Measured, one mutation at a time, each restored and the tree left
`git status --porcelain` empty:

| Mutation | Module |
|---|---|
| the three alternatives finding 3 added are deleted from the pattern | **exit 0 · 7 passed** |
| `hits()` is reverted to a plain line scan, undoing finding 2 | **exit 0 · 7 passed** |
| `CLAUDE.md` is deleted from the scanned set, undoing finding 9 | **exit 0 · 7 passed** |

Every one survives, and the reason is the same in all three: the sweep asserts
*no offender*, and no file in the tree carries any of these shapes, so removing
the reach that would find them changes no answer. The one control the module has
is the can-fail unit, and it passes on the owner's `release … sized` alone —
which is the alternative that was already there.

So the next edit takes all three fixes back silently, and the round record will
say they were fixed. Round 1's report claimed §15 was satisfied *by
construction*, which is true of the measurement it took and not of the tree it
left.

The patch below is three cases that pin the three fixes against the reader
itself rather than against the tree, so they do not depend on an offender
existing. Each was run at `941dab5` and against each of the three mutations:
green as committed, and red under exactly its own mutation and no other.

## 🟡 3 · posting a review round's record disarms the check on the survivor that round reported

`skills/code-review/scripts/survivor_check.py`, `corrected` — the line that
builds `paths` from the range's changed names. `corpus` filters
`records_a_past_round` out of the pool; `corrected` does not filter it out of
the range, so the sentences a round record *adds* are counted as wording the
range wrote. `wanted` then subtracts those from what the check looks for. A
round record quotes the defective wording verbatim, because that is what a
report is for, so posting it removes exactly the phrases the round reported.

Measured at four tips of this branch, same pool of 894 files and same 16
removed sentences throughout:

| Tip | What it adds | Survivors |
|---|---|---|
| `5ce162e` (build tip) | — | **1**, score 2.00 |
| `b46ff77` | round 1's paragraph | **1**, score 2.00 |
| `a0f0e9a` | round 1's record and report, and nothing else | **0** |
| `941dab5` (the fixes) | — | **0** |

The survivor is `seal/specs/1789100139-…/changelog.md:22`, and it scores on the
phrases *the paragraph that already says what* and *release milestone holds*.
At `b46ff77` one file in the tree carried the first of those; at `a0f0e9a`
three did, and the second is in the range's added wording and is subtracted.

Then the decisive measurement. With `records_a_past_round` applied to
`corrected`'s paths and nothing else changed, at `941dab5`: three round files
drop off the added side, the pool and the removed-sentence count do not move,
and the survivor is reported again at **2.00**.

The docstring at `:65` states the intent the code does not carry —
*Everything under a work item's `rounds/` is out* — and `:70-79` argues for the
exclusion on exactly this arithmetic, that dropping files which carry the
wording raises the rarity weight rather than lowering it. It is out of one of
the two sides.

Why this is not only this branch's problem: `hygiene.yml` runs this check on
every pull request, and every review chain posts a round record before the fix
pass commits. So the check is disarmed for precisely the ranges it was built
for, silently and in the direction of passing. The script's own opening says the
class it guards has been re-broken seven times.

The fix is one filter on one list, and it belongs on `paths` rather than on the
added side alone: a sentence removed from a round record is not corrected
wording either, and the pool already refuses a round record as a candidate, so
filtering both sides is what the stated design says. Verified in the same run —
the removed-sentence count stayed at 16.

A second thing this measurement settles, which is finding 5.

## 🟡 4 · the docstring still says the self-exclusion is by path, and the ledger row now says it too

Round 1's finding 2 named two sentences in the module docstring. One was
corrected. The other was not, and the fix pass applied every other sentence of
that same patch.

`tests/test_a_release_is_sized_by_a_criterion.py:31` reads *The sweep scans
`.md` and `.py` alike and excludes only this module **by path***.
`tracked()` at `:146` excludes by `os.path.basename(rel) != SELF`. Round 1's
paste-ready text for that sentence said *by basename*, and the commit took the
rest of the paragraph and left this clause as it was.

The difference is not only wording. Excluding by basename excludes any file in
the scanned set with that filename, wherever it sits — so a copy of the module
under `templates/` or a second tests directory is silently out of the sweep,
and a reader who trusts the docstring expects it to be swept. The docstring's
next sentence argues from the self-match, which makes the mechanism the thing
being described.

**The same false wording then entered the ledger.**
`seal/ledger/1789172128-…md`, row R1's `Verified behavior`, now reads *the one
file the sweep excludes **by path***. That clause was added by the commit that
was correcting a different false claim in that same row, and `fold_ledger.py`
moves the fragment into `seal/ledger.md` at the release, where nobody re-runs
it. Reported as a correction because its location is under `seal/ledger/`, and
flagged here because it is the second time this row has carried a statement
that does not match what the code does.

## ⬜ 5 · the survivor exemption is not engaged, and would not match if it were

`seal/specs/1789172128-…/survivors.md`. Two things the record asserts about the
exemption do not hold, and both follow from finding 3's measurement.

**It is not engaged.** The file's own header reads *All four survivors of this
range come from removing one ledger row*, and round 1's probe row records *16
removed sentences, 1 survivor, excused by a row*. At `941dab5` the check
reports **no survivors**, so none of the four rows excuses anything and none is
printed under `exempt`. The `exit 0` that both records offer as evidence is the
answer of a check that found nothing, not of a check whose finding was excused.
Those are different facts and the records state the first.

**It would not match.** With the survivor restored by finding 3's one-line
filter, the exemption was asked directly: `exempted` answers **None** for that
candidate. The quote has to appear as a contiguous run inside the candidate's
own words, and the candidate is the standing sentence at
`changelog.md:22-25`, while the marking clause the row quotes is a later
sentence at `:26-29`. So the mechanism the fix pass describes — *the exemption
dies the moment the marking goes* — is not the mechanism in force. If the check
were armed, the row as written would let the survivor be reported with its
grounds unread.

The marking itself is right and stands on its own. It is what makes the
released section read correctly, and that half was verified: `CHANGELOG.md`'s
top section is still `## 0.11.0`, both fragments are ungathered,
`gather_changelog.py` concatenates in work-item id order, and #351's bullet now
carries *That wording is what this work moved and not what the document says
today: the entry below replaces it in this same release* — so *the entry below*
is where `1789172128`'s entry actually lands. What fails is the claim about what
keeps the exemption honest, not the decision round 1 made.

Reported as a correction because the location is under `seal/specs/`. It is
worth the orchestrator's own reading because a survivors file that excuses
nothing is indistinguishable, in every record on this branch, from one that
excuses four things.

## ⬜ 6 · the ledger row cites the sweep unit but not the helper its claim now rests on

`seal/ledger/1789172128-…md`, row R1's `Code grounds`. It anchors
`test_one_document_states_a_releases_size@7bd4eb41`, re-stamped by the fix. The
correctness the row's `Verified behavior` now describes lives in `hits()`, and a
content anchor covers one unit, so an edit that reverts `hits()` to a line scan
moves no hash the row names. `evidence-check` answers `ok`, the `Checked` date
stands, and the claim the row makes is no longer true. Measured: the second
mutation in finding 2 is exactly that edit, and the ledger arm reads
1144 ok · 0 drifted · 0 broken before and after it.

This is the same gap as finding 2 on the other arm. The case in the patch below
closes it from the suite's side; anchoring `hits()` as a second coordinate in
R1's grounds would close it from the ledger's side, and one of the two is
enough.

## ⬜ 7 · what `hits()`'s one-boundary assumption actually costs, measured

`tests/test_a_release_is_sized_by_a_criterion.py:117-134`. The docstring states
the assumption as a fact — *A hand-wrapped sentence is split across exactly one
line boundary* — and the round's paragraph asked what it costs. Measured rather
than assumed, and the answer is that the residual is not where the assumption
points.

**The two-boundary escape is real.** A statement wrapped across two boundaries
answers `[]` while the same text flattened matches: `the size` / `of a` /
`release`, and `is` / `the` / `size` were both measured escaping. So the
assumption is load-bearing.

**It is not reachable by hand-wrapping.** For a statement to span two
boundaries the middle line has to sit wholly inside the phrase, and the longest
alternative in the pattern is 25 characters. The wrap cap is 88 columns, and the
shortest mid-paragraph line the fix's own edited paragraph produces is 49
(`docs/issues-and-milestones.md:152`, between lines of 74 to 83). A prose line
under 25 columns mid-paragraph is a paragraph's last line, and the line after
that one is blank, which `hits()` already refuses to join. I could not construct
a reachable instance in a `.md` file.

**Where the residual actually is, and it is not a regression.** The scanned set
includes `.py`, and a sentence split across adjacent string literals is
invisible to the pattern whatever reader runs it — the quote characters sit
between the words, so `\s+` does not match them, and flattening the whole file
does not remove them either. `survivor_check.py:38-46` names that exact shape as
the reason a line-oriented check failed in #269. So `flat()` shares the hole and
the sweep is no weaker than the halves that were already flattened.

Answerable with grounds, so it does not move `Needs a fix`. The form that
removes the assumption rather than bounding it: flatten the file once, keep a
cumulative index of where each line starts in the flattened text, and turn each
match offset back into a line number. That is the reader `flat()` already uses,
it needs no join, no skip rule and no assumption about how many boundaries a
sentence crosses, and it makes the guard in the current body unnecessary. Worth
saying because the guard is the part a later reader will not reconstruct: it
exists only to stop one wrapped sentence being reported twice, and an offset map
has nothing to stop.

## ⬜ 8 · the inserted clause left the paragraph unfilled

`docs/issues-and-milestones.md:152` is 49 columns where the surrounding lines
run 74 to 83, and `:141` is 83 where the paragraph it sits in runs 74 to 81.
Both are under the 88 cap, so `test_docs_line_wrap` passes and this is hygiene
rather than a defect. It is in the report because the module under review makes
its whole argument out of where a paragraph's wraps fall, and re-flowing the two
paragraphs the fix edited costs nothing now and moves the pinned sentences'
line numbers if it is done later.

## Regression cases to plant

Three, in `tests/test_a_release_is_sized_by_a_criterion.py`, and they are the
patch under finding 2. Destination file and the measurement behind each:

- the pattern against the three noun forms — red when the three alternatives
  finding 3 added are removed, green as committed.
- the sweep's reader against a statement whose wrap falls inside it — red when
  `hits()` is reverted to a line scan, green as committed, with the control
  asserting that a plain scan misses the same shape so the case cannot pass on
  the wrong reader.
- the scanned set against `CLAUDE.md` — red when the entry finding 9 added is
  removed, green as committed.

One more, owed to finding 3 and belonging to `skills/code-review`'s own test
module rather than to this work item: a range whose only added file sits under a
work item's `rounds/` must report the same survivors as the same range without
it. That is the case that would have caught this, and nothing in the suite
compares the two sides of the exclusion.

## Facts for the evidence ledger

- R1's `Verified behavior` needs the *by path* clause corrected to *by
  basename* before the fold, per finding 4. The rest of the sentence the fix
  wrote reproduces.
- R1's `Code grounds` should carry `hits()` as a second coordinate, or the
  planted case from finding 2 should be named there, so that the row's claim
  has something `evidence-check` can see move. Finding 6.
- If finding 3 is repaired here rather than filed, the claim is *the `rounds/`
  exclusion holds on both sides of the range*, and its grounds are `corpus`,
  `corrected` and the new case above.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the fix's new sentence puts `merged: X.Y.Z` *a release earlier* than `size: now` comes off; the section it cites, that section's title and `docs/branch-and-release.md` all put both moments inside one release | `docs/issues-and-milestones.md:152-155`, against `:208` and `:210-211` and `docs/branch-and-release.md:256-258` | open | read, in the clone at `941dab5`. Three coordinates state the two moments are one release apart in time within a single release, and the value of the other label names that same release |
| 2 | 🟡 each of the three code-side fixes reverts with the module still green, so nothing in the tree distinguishes the fixed module from the defective one — `agent-contract` §15 | `tests/test_a_release_is_sized_by_a_criterion.py`, the pattern at `:90-97`, `hits()` at `:117-134`, `SCANNED` at `:55-68` | open | **executed** — three mutations, one at a time, exit 0 · 7 passed each; each restored and the tree left clean. The three cases proposed were then run green as committed and red under exactly their own mutation |
| 3 | 🟡 `corrected` does not apply the `rounds/` exclusion the pool applies, so committing a review round's own record subtracts the wording that round reported and the survivor stops being reported | `skills/code-review/scripts/survivor_check.py`, `corrected` — the `paths` list built from `diff --name-only`; docstring at `:65` and `:70-79` | open | **executed** — 1 survivor at 2.00 at `b46ff77`, 0 at `a0f0e9a` which adds only two round records, same 894-file pool and same 16 removed sentences; with the filter applied at `941dab5` the survivor returns at 2.00 |
| 4 | 🟡 the docstring still says the self-exclusion is by path where `tracked()` excludes by basename — the one sentence of round 1's docstring patch that was not applied — and the same wording was written into the ledger row that folds into `seal/ledger.md` | `tests/test_a_release_is_sized_by_a_criterion.py:31`, against `:146`; and `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md` row R1 | open | **executed** — the filter is `os.path.basename`; read, round 1's paste-ready text for that sentence said *by basename* |
| 5 | ⬜ the survivors file excuses nothing — the check reports no survivors at `941dab5` — and the marking-clause quote does not exempt the candidate when the survivor is restored, so both claims the records make about the exemption are false | `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/survivors.md`, and `rounds/round-1.md`'s probe row | open | **executed** — `exempted` answers None for the restored candidate; the marking clause is a later sentence than the candidate's own. The marking itself verified correct in id order |
| 6 | ⬜ R1's grounds anchor the sweep unit but not `hits()`, so `evidence-check` answers ok after the edit that reverts the wrap-awareness the row's claim rests on | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md` row R1, `Code grounds` | open | **executed** — the ledger arm reads 1144 ok · 0 drifted · 0 broken with `hits()` reverted |
| 7 | ⬜ `hits()`'s one-boundary assumption is load-bearing and its two-boundary escape is not reachable by 88-column wrapping; the reachable residual is a statement split across string literals, which `flat()` cannot see either | `tests/test_a_release_is_sized_by_a_criterion.py:117-134` | answered | **executed** — two-boundary shapes measured escaping; shortest mid-paragraph line in the edited paragraph is 49 columns against a 25-column phrase. Answerable with grounds; does not move `Needs a fix` |
| 8 | ⬜ the inserted clauses left both edited paragraphs unfilled — `:152` at 49 columns, `:141` at 83 — under the cap, so hygiene rather than a defect | `docs/issues-and-milestones.md:141`, `:152` | open | **executed** — widths measured; `test_docs_line_wrap` exit 0 |

Stage 1, spec compliance, over the fix range only. S3 and S7 are the two clauses
the fix range touches, and both now hold **as far as the sweep reaches and for
as long as nobody edits it** — findings 2 and 6 are that second clause. S1, S2,
S8, S9 and S10 were re-run rather than re-read and are unchanged. The four owner
answers were not reopened: nothing here proposes editing
`tests/test_release_hygiene.py`, writing to the tracker, or touching a milestone
description. Round 1's two judgments were checked as asked rather than
relitigated — the marking landed and reads correctly, and `spec.md:159` is
untouched with its drift reproducing.

❓ **out of verified scope** — the broad gate. The full suite, the
repository-wide lint and the typecheck were not run, and their answerer is the
`sealer`. It has **not** come due: findings 1 to 4 are open, and a broad run
taken before their fixes is spent by the first one.

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_release_is_sized_by_a_criterion.py -q` | exit 0 · 7 passed |
| `bin/test` on `test_docs_line_wrap.py`, `test_release_hygiene.py`, `test_one_word_one_meaning.py`, `test_no_real_identifiers.py`, `test_a_row_points_by_content.py`, `test_a_record_states_what_the_tree_has.py`, `test_the_set_a_work_item_always_has.py`, one command | exit 0 · 246 passed |
| `uvx ruff check` and `uvx ruff format --check` on the module | exit 0 each |
| `bin/evidence-check .` | exit 1 · ledger arm 1144 ok · 0 drifted · 0 broken; records arm 1 DRIFTED at `spec.md:159` |
| `bin/survivor-check --range 7e17f5e..HEAD --exempt <this item>/survivors.md` | exit 0 · 894 files, 16 removed sentences, **no survivors reported** — nothing excused |
| `survivor-check` at `5ce162e`, `b46ff77`, `a0f0e9a`, `ea4fc64`, no exemption file | 1 survivor at 2.00 · 1 at 2.00 · **0** · 0 — the drop is at `a0f0e9a`, which adds only round 1's record and report |
| probe · `corrected`'s paths filtered through `records_a_past_round` at `941dab5` | 894 files, 16 removed sentences unchanged, **1 survivor at 2.00** restored; `exempted` answers None for it |
| probe · per-alternative match census over the scanned set | `is the size` 4 lines, all in the module; `release's size` owner ×1 and module ×7; `size of a release` module ×2; `release … sized` owner ×2 and module ×2 — the disclosure holds |
| probe · `hits()` exercised directly | one boundary reported; two boundaries `[]` against a flattened match; the guard reports an adjacent pair once; a join-only match on `is the size` fires, as the constant discloses |
| probe · `tracked()` | 170 files · `CLAUDE.md` present · the module excluded, and the filter is `os.path.basename` |
| probe · three mutations, one at a time, module re-run | exit 0 · 7 passed each — every one of the three fixes survives being reverted; tree restored clean after each |
| probe · the three proposed cases, at `941dab5` and against each mutation | 10 passed as committed; 1 failed under each mutation, and the failure is that mutation's own case in all three |
| probe · short mid-paragraph lines in the scanned set, and the widths of the two edited paragraphs | shortest mid-paragraph line the fix produced is 49 columns against a 25-column phrase |
| `git grep -n "is the size"` over the set R1 names | exit 0 · four hits, all in the module — what the corrected row now says |
| `git cat-file -t 7578e25` and its diffstat | the commit exists and is the one that planted the module, which is what `phases/phase-2.md`'s new clause names |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet**, and not run here. It is the `sealer`'s, and it has not come due: findings 1 to 4 are open |

Every probe file was named `test_tmp_*`, run once and deleted; the clone's tree
was `git status --porcelain` empty afterwards, checked after each mutation and
at the end. The virtual environment `bin/test` built is the repository's own
reused runner, not a probe's leaving. No commit was made in the clone and
nothing outside this file was written.

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1, finding 1 | `docs/issues-and-milestones.md:208-220` and `docs/branch-and-release.md:251-262` | carried rather than re-found, and re-read because finding 1 above rests on them. They are what say the two moments sit inside one release |
| round 1, finding 7 | `.github/scripts/gather_changelog.py`'s `fragments`, in id order | carried. Re-read once, to confirm *the entry below* is where this work item's entry lands |
| round 1, finding 8 | `.github/workflows/test.yml:84-92` | carried, not re-derived. The ledger job's exit-2 threshold has not changed and the drift is still a warning |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the version checker's off-by-one — a shipped version is refused in a loaded file for one release's length | **#363**, by Q1 | the repository owner. Already deferred; not re-opened here |
| `release: 0.11.1`'s milestone description, stale past its `Size.` line | the tracker, by Q4 | the repository owner. Already deferred; not re-opened here |
| whether `size: now` is the spelling the owner creates | `overview.md`'s `## Not verified` | the repository owner, after this merges. Already deferred; no check can see a label that does not exist |
| finding 3, if the orchestrator takes it out of this work item's scope rather than fixing it here | a new tracker issue, with `CONTRIBUTING.md`'s four gate items owed there — the defect is in a gate | the repository owner. **Not yet filed**, and Q3 says this work item writes nothing to the tracker, so somebody other than this branch has to. Filed or fixed, it must not be left as a report nobody acts on: the check is disarmed on every review chain until then |

## Paste-ready fixes

Finding 1 — `docs/issues-and-milestones.md`, replacing `:148-157`. The paragraph
is re-flowed at the same time, which is finding 8:

```markdown
**Nothing reads this label** — no workflow, no check, no script — so a stale
one costs a reader a wrong answer about what has to go next and costs no
automation anything. It comes off when the release that carried the ticket has
gone out — the moment `main` moves and the issue closes — and nothing enforces
that. **Not when `merged: X.Y.Z` goes on**, which §*A label says a ticket is
already in, before the release ships* puts at the push to `release/*`: that is
earlier in the same release, and it answers *is this in yet*, where this one is
spent only once the work is out. A label is the right home for the judgment for
exactly that reason: it makes the answer durable without making it a gate
anybody has to satisfy.
```

Finding 2 — `tests/test_a_release_is_sized_by_a_criterion.py`, three cases added
after `test_the_sweep_can_fail`. Run at `941dab5` — 10 passed with the module's
own seven — and each one red under its own mutation and green under the other
two. `uvx ruff check` and `uvx ruff format --check` clean:

```python
# The shapes round 1 measured escaping, kept as data rather than as prose.
# **The sweep's green answer cannot stand in for these.** It asserts *no
# offender*, and no file in the tree carries any of these today, so deleting
# the reach that finds them changes no answer: each of the three fixes round 1
# commissioned was measured reverting with this module still green. So they are
# pinned against the reader itself.
NOUN_FORMS = (
    "A release's size is three or four work items.",
    "Three or four work items is the size of a release.",
    "The size of a release is three work items.",
)


def test_the_pattern_catches_the_noun_forms_and_not_only_the_verb():
    """Round 1 measured all three escaping, on one line and with no wrap
    involved. `test_the_sweep_can_fail` cannot see them go: the owner matches
    on `release ... sized` alone, which was there before the widening."""
    for sentence in NOUN_FORMS:
        assert STATES_A_SIZE.search(sentence), (
            "a one-line restatement of a release's size escapes the sweep: "
            f"{sentence!r}"
        )


def test_the_sweep_reads_a_statement_whose_wrap_falls_inside_it():
    """The failure round 1 found, and the whole reason `hits()` exists rather
    than a line scan. The first assertion is the control: if a plain scan ever
    starts seeing this shape, the case has stopped measuring the reader."""
    wrapped = ["the paragraph says three or four is the", "size a release is cut to."]
    plain = [n for n, line in enumerate(wrapped, 1) if STATES_A_SIZE.search(line)]
    assert plain == [], (
        "the control moved: a plain line scan must miss this shape, or this "
        "case passes on a reader the sweep does not need"
    )
    assert hits(wrapped) == [1], (
        "a statement whose wrap falls inside it must be reported, at the line "
        "it starts on"
    )


def test_the_scanned_set_includes_the_file_a_rule_gets_restated_in():
    """`CLAUDE.md` is where a rule is restated for a session that never opens
    `docs/`, and `tests/test_one_word_one_meaning.py` — the module this sweep
    is modelled on — already reads it."""
    assert "CLAUDE.md" in tracked(), (
        "CLAUDE.md is outside the sweep, so a second answer stated there is "
        "invisible to it"
    )
```

Finding 3 — `skills/code-review/scripts/survivor_check.py`, in `corrected`,
replacing the line that builds `paths`. Measured at `941dab5`: the
removed-sentence count stays at 16, the pool stays at 894, and the survivor is
reported again at 2.00:

```python
    # The `rounds/` exclusion holds on BOTH sides of the range, not only on the
    # pool. A round record quotes the defective wording verbatim -- that is
    # what a report is for -- so counting it as wording the range WROTE
    # subtracts the phrases the round reported, and the survivor stops being
    # reported by the commit that posts the round. Measured on this
    # repository's own #361 branch: 1 survivor at 2.00 before the round record
    # was committed, 0 after, with nothing else in the range changed.
    paths = [
        path
        for path in names.split("\0")
        if path and not records_a_past_round(path)
    ]
```

Finding 4 — `tests/test_a_release_is_sized_by_a_criterion.py:31`, one word, and
the sentence after it says why the mechanism matters:

```markdown
The sweep scans `.md` and `.py` alike and excludes only this module, by
basename rather than by path, so a copy of it anywhere in the scanned set is
excluded too. Scanning one suffix would have been the cheaper way past the
self-match, and it would have left a comment in any other test module free to
state a second answer.
```

And `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
row R1's `Verified behavior`, replacing the clause that names the exclusion:

```markdown
the module that names the replaced wording in its own docstring and constants,
and the one file the sweep excludes — by basename, so a copy of it under
another directory would be excluded with it
```

Finding 5 — `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/survivors.md`.
The header and the third row both state something the check does not do. Two
changes, and which one is right depends on finding 3:

```markdown
All four rows below were written against a run that reported one survivor, at
`b46ff77`. **At `941dab5` the check reports none**, because the range now
carries round 1's own records and `corrected` counts their verbatim quotation
as wording this range wrote — round 2's finding 3. So these rows excuse
nothing today and none of them is printed under `exempt`. They are kept rather
than deleted: they are the judgments a person made, and repairing the checker
arms them again.
```

And that third row's `Quote`, which has to come from the candidate's own
sentence rather than from the marking clause, because the exemption matches a
contiguous run inside the surviving sentence and the marking is a later one:

```markdown
| `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md` | `the paragraph that already says what a `release:` milestone holds` | #351's changelog fragment, gathered into `CHANGELOG.md`'s `0.11.1` section by the release that also ships this work item. Its claim is what #351 did — the rule moved into that document — and that is still true, so the bullet stays. **Round 1 measured the second half of the original exemption away and it is withdrawn**: `gather_changelog.py` concatenates fragments in work-item id order, so `1789100139` lands ABOVE this one and the released section would have stated the replaced sentence in the present tense before correcting it far below. The bullet is therefore MARKED as well — it now says the wording is what #351 moved and not what the document says today, and points at the entry below that replaces it. **The quote above is the surviving sentence rather than that marking**, because the exemption matches a run inside the candidate's own words and the marking is a later sentence: round 2 measured the marking-clause spelling answering None |
```

Findings 6 and 8 need no snippet. Finding 6 is one coordinate added to R1's
`Code grounds` — `tests/test_a_release_is_sized_by_a_criterion.py#hits@<hash>`
— or nothing at all if finding 2's second case lands, since that case is what
makes the reverted helper visible. Finding 8 is re-flowing `:135-146` and
`:148-157`, which finding 1's snippet already does for the second of them.

Needs a fix: yes — findings 1, 2, 3 and 4. Finding 1 is the same document
making a new false claim about its own two labels in the commit that answered
the first one; finding 2 is all three code-side fixes reverting with the module
green; finding 3 is a gate on every pull request that the review chain's own
records disarm; finding 4 is the one sentence of round 1's docstring patch that
was not applied, now copied into the ledger row that folds into the shared file.

Loses a record or crashes: no.

## Proof

Files opened, in a `git clone --no-local` at `941dab5`:
`docs/issues-and-milestones.md`, `docs/branch-and-release.md`,
`tests/test_a_release_is_sized_by_a_criterion.py`, `tests/test_docs_line_wrap.py`,
`skills/code-review/scripts/survivor_check.py`, `bin/test`,
`bin/survivor-check`, `CHANGELOG.md`,
`seal/ledger.md`,
`seal/ledger/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked.md`,
`seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
`seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md`,
and this work item's `spec.md`, `questions.md`, `overview.md`, `changelog.md`,
`survivors.md`, `phases/phase-2.md`, `phases/phase-4.md`,
`rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-2-fixes.md`,
`rounds/round-2-asked.md`.
