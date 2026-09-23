# 1790154761-folded-statements-pile-into-one-spec — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 24a001f1 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Add the placement rule to `skills/settle/SKILL.md` §2. Make
`docs/the-evidence-ledger.md`'s fold section link to settle §2 and state the
values. Write `tests/test_a_document_has_room_for_the_next_fold.py` with
`LINE_CEILING = 1000` and `OVER_CEILING` freezing `docs/review-chain-spec.md`
at 29 markers, its home MichaelYcJo/SpecSeal#526 (Q3, answered by the
orchestrator). Cover A8–A10 and pin the prose values against the constants.
If PR #525 had merged into `origin/release/v0.14.0` first, merge that base in
before starting.

## What this phase found

- **#525 had not merged.** `origin/release/v0.14.0` was still at `f8f1c9de`
  when fetched before this phase, so no merge was taken.
- **The values paragraph sits at the head of the fold section, not after the
  *top level of `docs/`* paragraph** as `spec.md` §*Overlap with PR #525*
  suggested. A statement's provenance runs from its marker to the next marker
  or heading, so a paragraph placed after that paragraph would read as part of
  `1790039346`'s fold, and it is not a fold. The section head has no marker
  above it, and it is further from the lines #525 rewrites (the section's
  tail). `overview.md` records the divergence.
- **The frozen count is compared for equality, not only for growth.** The
  spec says the check fails when the listed file gains a marker. A marker
  removed without lowering the count would leave room for the next fold to
  refill silently, so a removal fails too, and the message says to lower the
  count.
- **The placement rule is pinned in this module**
  (`test_settle_owns_the_placement_rule`), next to the values it governs. The
  shape rule's pin stayed in phase 2's module.
- **Red, executed:** the evidence ledger restored to `HEAD` (no link and no
  values), each of the four prose values edited by one digit, settle restored
  to phase 2's `HEAD` (no placement rule), and five mutations of the reader
  (ceiling check off, growth-only comparison, outlived entry not caught,
  missing listed file not caught, live filter off). Each turned at least one
  case red, and each was restored from a copy kept outside the tree.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
