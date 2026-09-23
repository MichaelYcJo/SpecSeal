# 1790119502-four-shipped-work-items-wait-unfolded — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b0e76ae |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Write the two standing statements whose destinations carry no anchored
heading: `1790076050` into `docs/branch-and-release.md` §*Cutting a release*,
and `1790076070` into `docs/the-evidence-ledger.md` §*The fold, and what tells
it from a deletion*, including #497's rule for the ungrouped and the grounds
for keeping `1788184145`. Re-read each source `spec.md` in full first; the
judgment of what is still true is this phase's, and the newest work item wins.

## What this phase found

**`1790076050` — what was folded.** One standing statement, placed after the
tag paragraph it extends. **Corrected 2026-09-23 in round 1's fix pass:** as
built here its headline gave all three acts to the tag push; the fix states
that the merge to `main` fires the label acts, the tag push fires the note,
and a person runs the directory check. Each of the three acts is stated with
the property that makes it safe — the note never republishes and fails only
for a missing changelog section; the directory reader exits 0 whatever it
finds; a declared label is created and spent by the close-issues workflow. Each
was checked against the tree before it was written:
`.github/workflows/publish-release.yml` triggers on `tags: ['v*']`;
`publish_release_note.py`'s docstring and `main` return 0 for an existing
release and 1 only for a bad tag or a missing section;
`close-issues-on-release.yml` runs `tracker_labels.py --apply` and
`close_issues_on_release.py#spend_label` removes `SPENT_ON_CLOSE`. The same
marker went on the third-reader paragraph the item had already written into
the file, which carries the fixed-name paragraph after it; both were the item's
own sentences and no second copy was made.

**`1790076050` — what was dropped, and why.**

| Dropped | Why |
|---|---|
| that `size: now` exists on the tracker | measured false (L2); the statement asserts the design and points at `gh label list` for the state, and #515 owns the repair |
| the title-source measurement — merge subject, changelog heading and the twenty-three hand-written names each rejected | a measurement of a moment; the rule it produced (the `release:` line of §5) is folded |
| the directory's four entry shapes, the 22- and 28-day sync gaps, the 310 / 2,282 entry counts | measurements; the third-reader paragraph already carries the one that is a rule's grounds |
| `size: now`'s meaning, the no-sweep rule, the colour | already stated in `docs/issues-and-milestones.md`, which owns the label and is named, not restated (`spec.md` O6 keeps its anchored section unmarked) |
| Out items: no gate on the directory, no check on a missing note, no submission automation | the statement's *never fails* and *a person's act* carry the first and third; the second's condition is removed by the workflow and needs no rule |

**`1790076070` — what was folded.** Four rules, each a paragraph under its own
marker: (a) an ungrouped released item with no `spec.md` states no rule and is
kept by name, and a permanent ledger row anchored inside a directory holds it
until the row is answered — the grounds for all 11 kept today, `1788184145`
being the one kept for its row; (b) a retirement breaks every ledger row
anchored inside the directory; a hit the grep finds before the removal
keeps the directory by (a), and `CLAUDE.md`'s REMOVED rule decides only what
the grep missed (**corrected 2026-09-23 in round 2's fix pass** — as built
here (b) said REMOVED decides each, which contradicted (a)); the multi-anchor
case is the owner's (L8), and #511 is the missing refusal; (c) a
population floor is replaced by an independent listing, never lowered, and a
repair is green before and after; (d) a fold marker alone on its line is exempt
from the wrap limit. The chain checker's retirement arm is linked to
`docs/review-chain-spec.md` rather than restated. Checked against the tree:
`tests/test_docs_line_wrap.py` skips `FOLD_MARKER.fullmatch(line)`;
`tests/test_chain_check_at_the_pull_request.py#_the_walk_found_every_committed_record`
compares the walk against `git ls-tree HEAD`; #511 is open.

**`1790076070` — what was overturned and dropped.** The spec's G3 said one
ledger row anchors into a work item directory and that `seal/ledger.md` would
stay byte-identical; its own build found six and edited the ledger (its
overview's divergence table). The spec's A7 and O3 were built on G3 and fall
with it. **What folded is the corrected rule (b)**, not the spec's sentence —
the newest statement of the same item wins over its frame. Also dropped: the
corpus counts at `6d410023` and the per-floor after-values (moments); the rule
for placing the five ungrouped items it folded (their markers already stand in
`docs/`); `docs/the-gates-a-session-meets.md`, which the build never wrote.

**The one judgment worth naming.** Rule (a)'s *kept by name* could have been
written as a list of the 11 ids. It was not: a list goes stale at the next
release and the rule does not. `phases/phase-1.md` carries the 11 by name.

**Run for this phase, each exit read directly.** `./bin/settle` exit 0:
`2 work items in 2 segments, 11 ungrouped`, and `1790076050` and `1790076070`
listed under *folded already, waiting to be retired*.
`tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py`,
`tests/test_one_word_one_meaning.py` and
`tests/test_the_release_tail_does_not_end_at_the_tag.py`: `89 passed`, exit 0.
`bin/evidence-check --strict .`: `1468 ok · 0 drifted · 0 broken`, exit 0 — no
new drift, as G1 predicted for two unanchored destinations. The two lines over
88 columns in `docs/branch-and-release.md` are the base's, not this phase's,
and that file is not in `COVERED`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none — both statements are additions; the directories go in phase 5 |
