# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — phase 2

<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

`docs/issues-and-milestones.md` gains the one standing rule that survives
`docs/flow.md` — *a release is sized in work items, and three or four is the
size* — and loses the sentence making scheduling a second act.
`docs/release-checklist.md` loses its four `docs/flow.md` steps, the
conflict-resolution bullet included, and the quadratic-cost measurement
survives without naming the file. Verified by `grep -c "flow\.md"` reading 0
in both and the modules that scan them staying green.

## What this phase found

**Writing the unshipped version into prose is the defect this repository has
a check for, and this phase committed it three times before the check
caught it.** `test_no_loaded_file_names_a_version_at_or_above_the_running_one`
refused `docs/issues-and-milestones.md:34`, `docs/release-checklist.md:38`
and `skills/implement/orchestration.md:11`, all three carrying *deleted in
0.11.1* — a sentence that is a timer, right for exactly one release and red
on that release's own preparation commit.

The class is wider than the three the check named, and enumerating it is
what §12 asks for here. The same phrase was also in
`tests/test_the_rules_have_one_owner.py` twice, in a comment and a docstring
that phase 1 wrote; `tests/` is outside the scanned set, so the check was
never going to report them and they would have sat there until somebody
read them. All five say *(#351)* or *that file was deleted* now. **An issue
number is the durable way to date a change in prose** — it does not move
when the release it ships in is renumbered, which this work item's own
release has already been twice.

**One instruction in the spec was followed rather than improved on, and the
first attempt improved on it.** Step 0's bullet *`docs/flow.md` has every
item of the release ticked except the release line itself* was first
replaced with a milestone-based equivalent — check that every issue the
milestone holds is closed or has moved. That is a new step, and the spec
says the four steps are **lost**. It was reverted to a plain deletion for
two reasons: the bullet immediately above it already carries the substance
(*every work item of the release is squash-merged into `release/vX.Y.Z` and
its CI was green at the commit that merged*), so the replacement was a
second statement of one check; and a step nobody asked for arrives in the
review rounds as an unreviewed instruction.

**The step-2 heading counted the deleted act and nothing pins it.**
`## 2. Gather, fold, bump, tick` named four acts, and the tick was the box
in `docs/flow.md`. `git grep` finds no other file citing that heading, so it
is `## 2. Gather, fold, bump` now. A heading naming an act the section no
longer contains is the same rot as a path naming a file that is gone, one
level up.

**The sizing rule went to the `release:` paragraph rather than to a section
of its own**, because it is a fact about what a `release:` milestone may
hold and the document already has the paragraph that says what one holds.
Its evidence sentence — *0.8.3 shipped three of eight, and carrying five
forward was the call rather than the failure* — moved with it: 0.8.3 is
below the running version, so it is history the check keeps, and a rule
shipped without the measurement behind it is the shape this repository
keeps having to repair.

**Scheduling is one act now, and the sentence says which.** The old text
made a schedule the milestone *and* a line in the checklist, with *neither
act alone is a schedule* spelled out. What replaced it says the milestone is
the act and that the milestone's **description** carries the release's
purpose and the grounds for its order — which is Q1's answer (a) stated as a
standing rule rather than as a thing this work item did once.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/release-checklist.md` step 0's *`docs/flow.md` has every item ticked* bullet | Nowhere. The bullet above it already checks that every work item merged with green CI, and the file whose boxes this one counted is gone |
| `docs/release-checklist.md` step 0's *`docs/flow.md` conflicts even when the branches touch different lines* bullet, and its resolution procedure | Nowhere — this is the conflict the deletion exists to end. The cost it recorded survives one bullet up, in the quadratic-cost paragraph, which now names the conflict without naming the file |
| `docs/release-checklist.md` step 2's *and tick the release's last box in `docs/flow.md`* | Nowhere. The heading dropped `tick` with it |
| `docs/issues-and-milestones.md`'s *scheduling is two acts rather than one* | Replaced in place: scheduling is the milestone, and the milestone's description carries what the checklist line used to (Q1 (a)) |
| `docs/issues-and-milestones.md`'s *`docs/flow.md` says the same thing from the ticket's side* | `skills/implement/orchestration.md` §*Orchestrator: the order inside a ticket*, named there instead |
