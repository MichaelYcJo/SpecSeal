# Feature Specification: a release is sized by what has to be in effect next, and the count is named as a ceiling

<!-- seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #361. Milestone `release: 0.11.1`.

`docs/issues-and-milestones.md:24` states a release's size as a number — *three
or four is the size*. Read plainly that is a target, and on 2026-09-11 a
session read it as one twice: it proposed moving eighteen issues out of the
release milestones to bring them "down to size", and separately read a
two-item release as under the rule with room for a third. The repository owner
stopped both.

The practice the last two releases actually followed is not a count. Each was
cut at whatever had to be in effect before the next work item started. So the
repair has two halves: the sentence states that criterion and names the count
as a ceiling, and the tracker gains one signal saying which tickets meet it.

## The collision this work item is mostly about

**The ticket's own `## Done when` asks the rule to cite the two releases that
demonstrate it, and this repository's checker refuses to let a document in
`docs/` name either of them.**

Read, not executed — `tests/test_release_hygiene.py`, the constants opened:

- `.claude-plugin/plugin.json` says the running version is `0.11.0`.
- `LOADED` includes `docs`, and `timers_in` collects every version-shaped
  token whose `as_release` tuple is `>=` the running version's.
- The two releases #361 wants cited are 0.11.0 and 0.11.1. `(0, 11, 0) >=
  (0, 11, 0)` and `(0, 11, 1) >= (0, 11, 0)`, so both are refused.
- None of the three exemptions is a truthful home. `ILLUSTRATIVE_VERSION` is
  `1.2.3`, and writing it here would replace the evidence with a placeholder.
  `VERSIONS_OF_ANOTHER_PRODUCT` is for a number belonging to somebody else's
  product. `RECORDS_OF_A_MOMENT` is argued against for this exact file in the
  checker's own comment: *that is what makes a prefix defensible here where
  `docs/issues-and-milestones.md` — a standing document edited every release —
  is not (#179)*.

**The underlying defect is an off-by-one between *running* and *shipped*, and
it is worth stating because it outlives this ticket.** `timers_in`'s docstring
argues the ceiling from history: *Below `running` is history and is kept.* But
`plugin.json` is bumped at the release-preparation commit, so from that commit
until the next bump the running version is the version that **has already
shipped**. `v0.11.0` is tagged and on `main` and `CHANGELOG.md` records it as
released, and a loaded document still may not name it. The check's own reason
for the at-or-above ceiling — *it goes red on the day that version ships, on
the release's own preparation commit* — is about the interval **before** a
release, and it keeps refusing for the whole interval after.

Which route out of this is taken is `questions.md` Q1, and it is the owner's,
because one of the routes is a change to a gate and would pull
`CONTRIBUTING.md` §*What a change to a gate must carry* onto a prose ticket.
This specification is written so that the sizing rule lands either way.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/issues-and-milestones.md` §*A milestone answers* when*, and takes three shapes* | Holds the sentence being rewritten, at lines 24–30. The rewrite is in this section rather than a new one, because the rule is a fact about what a `release:` milestone may hold |
| `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move* | **The proposed label contradicts it.** That section spends the milestone field on *when* and gives a label to a concern that **outlives a schedule**; `now` is entirely a schedule answer and is spent when the release ships. The document cannot state both without reconciling them — `questions.md` Q2 |
| `docs/review-chain-spec.md:53` — *Five is a ceiling, not a target* | The in-tree model for the sentence #361 asks for. The sizing rule is brought to that wording rather than a new one being invented |
| `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | `docs/` is `LOADED`. Every version in the rewritten prose is either below the running one, the illustrative `1.2.3`, or not written as a number at all. This is the constraint the whole frame turns on |
| `tests/test_docs_line_wrap.py` | `LIMIT = 88` display columns, and `docs/issues-and-milestones.md` is not on its exempt list. A spliced sentence that is not re-wrapped fails |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Applies **only if** Q1 is answered with the checker correction. If it is, all four are owed: a test seen red, a stated failure direction, a prompt budget, platform honesty |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`. Neither `CHANGELOG.md` nor `seal/ledger.md` is appended to |
| `CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not re-pointed* | This work edits the unit an existing ledger row cites — see *The ledger row this edit moves* below |
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here may add a question a person answers per release. The criterion is a judgment a person already makes once per release; the label is where that judgment is written down so it is not made again from scratch, which is #331's class |
| `skills/writing-style/SKILL.md` §*English prose rules* | The rewritten paragraph is read and acted on by a person planning a release. No minimizers, and the ceiling half is stated as plainly as the criterion half |

## Scope

### In

**The sizing rule rewritten**, in
`docs/issues-and-milestones.md` §*A milestone answers* when*, at lines 24–30.
Four things change in that paragraph:

- the criterion replaces the count as the thing that decides a release's size
  — *what has to be in effect before the next work item starts*;
- the count is named as a **ceiling**, on
  `docs/review-chain-spec.md:53`'s wording;
- the two releases that demonstrate it are cited, in whichever form Q1
  settles, so the rule reads as a description of practice rather than a
  proposal;
- the paragraph says what does **not** change: a milestone stays a pool a
  release is cut from, `backlog:` stays the unscheduled pool, and nothing
  automated reads either for scheduling.

`0.8.3` stays. It is below the running version, so the checker keeps it as
history, and it is the third piece of evidence the paragraph already had.

**The label defined in the document**, name per Q2. Two states and no tier
list: carrying it means *this has to be in effect before the next work item
starts*, and its absence means the ticket rides the next release that carries
it. The definition has to be applicable by a reader without asking anybody,
which is the `## Done when` row it answers.

**The reconciliation with §*A label answers what it is about***. The document
cannot state that a label is for a concern that outlives a schedule and then
add one that is purely a schedule answer. The precedent is in the same
section: `flow-measurement` is already named there as *a label that is not an
index*, so the shape of the exception exists and this is the second one.

**The sweep**, which is the last `## Done when` row and is a class rather than
a coordinate (`agent-contract` §12). Nothing else in the tree may state a
release's size, and the sweep is a named command whose output is recorded,
plus a case that holds the result.

**The ledger row this edit moves.** See below.

**This work item's own fragments** — `changelog.md`, `seal/ledger/<id>.md`,
and the closing memo.

### Out, and why

- **Creating the label on the tracker, and applying it to any ticket.** Both
  are writes to the tracker and both are the owner's. The `## Done when` row
  reads *exactly the tickets that meet it carry it*, and applying a criterion
  to thirty-five open issues is the same class of act the owner stopped on
  2026-09-11 — #361 exists because of it. This work item defines the
  criterion so a reader can apply it; who applies it and when is
  `questions.md` Q3.
- **The `Size.` paragraphs in the release milestone descriptions.** Two of
  them state a size as a count of issues and work items, and `release: 0.11.1`'s
  is already false — it reads *Eight issues, about five work items* while the
  milestone holds three. They are on the tracker rather than in the tree, so
  the sweep's own wording does not reach them, and editing them is a tracker
  write. `questions.md` Q4.
- **Moving any issue between milestones.** Not this work item's act under any
  answer.
- **A priority scale, tier list, or second urgency label.** Rejected in the
  ticket and the rejection holds; `plan.md`'s alternatives table carries the
  argument so it is not re-opened.
- **Anything automated reading the new label.** Nothing reads it, and the
  document says so. A workflow that scheduled from a label would be a gate,
  with `CONTRIBUTING.md`'s four requirements and a prompt budget to answer.
- **How a release is cut, merged or tagged.** `docs/branch-and-release.md`
  owns that sequence and no sentence in it is edited.
- **`docs/release-checklist.md` step 0.** Its milestone box asks whether the
  milestone holds what the release is carrying, which is true under the new
  criterion exactly as it was under the count. Nothing in it states a size.
- **Widening the version-token regex in `tests/test_release_hygiene.py`.**
  Narrowing or widening that pattern for a single shape is what took another
  shape with it in #179's round 1. If Q1 takes the checker route, the change
  is to what counts as **history**, never to what counts as a **token**.
- **#362's milestone.** The criterion is applied to it as the rule's own
  falsifiable test and the answer is recorded, but assigning it a milestone is
  a tracker write and is out.

## The ledger row this edit moves

`seal/ledger/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked.md`
row **S3** claims *the rule that a release is sized in work items, three or
four, is stated in exactly one document, and it is the one that owns tracker
conventions*, anchored at
`docs/issues-and-milestones.md#"## A milestone answers *when*, and takes three shapes"@95e3a483`.

This work item edits that unit, so the hash moves. Two facts bound what has to
be done about it, and both were read rather than assumed:

- the **heading survives**, so the row DRIFTS and is not REMOVED —
  `CLAUDE.md`'s *An anchor degrades to DRIFTED, never to BROKEN* holds;
- drift does **not** fail CI. `.github/workflows/test.yml:70-93` runs
  `evidence_check.py .` without `--strict`, treats exit 1 as a warning
  annotation and fails only at exit 2 or above, and the job's own comment says
  why: drift on a branch mid-flight would be red by construction.

So the repair is hygiene rather than a blocker. What makes it a decision is
that the claim's **wording** goes with the change — after this work the rule is
not *three or four is the size* — while its **substance** survives and is
exactly what the sweep asserts. `plan.md` phase 4 carries the two candidate
acts and `questions.md` Q8 is where the choice between them is recorded.

## User scenarios & acceptance *(mandatory)*

One row per scenario — these become the review's stage-1 checklist. The five
`## Done when` bullets map to S1, S2, S4, S5 and S7.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the rule states a criterion | Given a person sizing a release · When they read `docs/issues-and-milestones.md` · Then it says the size is decided by what has to be in effect before the next work item starts, and a release of one work item is named as legitimate | read; `git grep -n "in effect before the next work item"` over `docs skills agents templates tests` returns the one owner |
| S2 · the count is a ceiling and reads as one | Given the same paragraph · When the count is read · Then it is named a ceiling in `docs/review-chain-spec.md:53`'s wording, with what the ceiling is for — a section a reader can hold — and not as a number to fill | read; `git grep -n "ceiling, not a target" -- docs` returns both that file and this one |
| S3 · no reader can take the old sentence | Given the tree after this work · When the replaced wording is searched for · Then *three or four is the size* survives nowhere that instructs anybody | `git grep -n "three or four is the size" -- docs skills agents templates tests` exits 1. Earlier work items' `seal/specs/*` are records of a moment and are not rewritten |
| S4 · the label is applicable without asking | Given the label's definition in the document · When a reader holds an unlabelled ticket against it · Then the definition alone decides, in two states, with no tier and no second label | read, plus the live test: the criterion is applied to **#362** and the answer recorded in `phases/phase-N.md`. #362 is prose that costs no behaviour today, so nothing has to start with it in effect — it takes no label and rides the next release that carries it. A criterion that cannot answer it is the wrong criterion |
| S5 · the document says what does not change | Given the rewritten paragraph · When it is read · Then a milestone is still a pool a release is cut from, `backlog:` is still the unscheduled pool, and nothing automated reads either for scheduling | read; the three clauses present in one paragraph rather than scattered |
| S6 · the label does not contradict the label section | Given §*A label answers what it is about, and survives the move* · When it is read against the new label · Then the section states the exception rather than leaving two rules disagreeing, and names `flow-measurement` as the precedent for a label that is not a topic | read. A document that states both without reconciling them is the defect, not the fix |
| S7 · nothing else in the tree states a release's size | Given the whole tree · When the sweep command runs · Then `docs/issues-and-milestones.md` is the one owner, and a case holds it | **executed**, output recorded; a case in `tests/test_one_word_one_meaning.py`'s shape, asserting the new wording present AND the old absent, **seen red** before the edit (`agent-contract` §15) |
| S8 · no documentation edit starts a timer | Given every file this work edits under `docs/` · When the release hygiene case runs · Then no version at or above the running one is named | `tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one`, exit code read directly |
| S9 · the edit stays inside the wrap | Given the rewritten paragraph · When the wrap case runs · Then no line exceeds 88 display columns | `tests/test_docs_line_wrap.py` |
| S10 · the ledger stays true | Given S3's row cites the edited unit · When `bin/evidence-check .` runs · Then the row's state is named and acted on per Q8, and the exit code is read against `test.yml`'s own thresholds — 1 warns, 2 fails | **executed**, exit code read directly, before and after the act Q8 chooses |
| S11 · if the checker changes, it changes as a gate | Given Q1 is answered with the correction · When the change ships · Then the four `CONTRIBUTING.md` items are answered in the pull request body, and the case that pins the new boundary was seen red first | `CONTRIBUTING.md` §*What a change to a gate must carry*. **Not applicable** under Q1's other answers, and `plan.md` phase 1 says so rather than leaving it ambiguous |

## Data & interfaces

No schema, no endpoint, no script. Three surfaces.

**Edited:** `docs/issues-and-milestones.md` — the sizing paragraph in
§*A milestone answers* when*, and a reconciliation in §*A label answers what it
is about*.

**New:** one case holding S3 and S7, in the style of
`tests/test_one_word_one_meaning.py` — the pinned phrasing present and the
loose one absent, which is what makes those cases worth having.

**Conditionally edited, only under Q1's checker route:**
`tests/test_release_hygiene.py`'s notion of history. The change would be to
what counts as shipped, never to `VERSION_TOKEN`. The signal for *shipped*
that this repository has already ratified is the tag —
`docs/issues-and-milestones.md` §*Reconstructing a missing milestone* says
*the signal is the tag, not the branch* — and a CHANGELOG-derived exemption
has a hole: the release-preparation commit adds `## X.Y.Z` and bumps
`plugin.json` together, so the version being cut would read as shipped in the
same commit, which is the timer the check exists to catch.

**Not touched:** the tracker. No label created, none applied, no milestone
description edited, no issue moved.

## Open questions → questions.md

Four rows need the repository owner, and the first of them decides the shape of
the work rather than a detail of it. Everything else is a measurement or the
work, and is sorted that way so neither is queued behind a person.
</content>
</invoke>
