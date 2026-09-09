# 1788938400-the-shipped-section-goes-and-the-plan-is-renumbered — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | docs/0.10.0-is-next-and-the-shipped-section-goes |

Answered 2026-09-10 by the owner, before the first edit.

## Why this way

This is the housekeeping `docs/flow.md` names as its own — *deleting a shipped
version's section, or moving items between releases* — and the owner decided
both halves in conversation: 0.9.5 shipped, and 0.10.0 goes next because it is
the main line of the work.

It exists as a work item for one reason beyond the declaration: a branch that
deletes a shipped section needs a `survivors.md`, CI globs those at
`seal/specs/*/survivors.md`, and `survivor_check.py` anchors a whole-range row
on the work item the file lives in. `templates/sdd-routing.md` already names
this shape — below the SDD ladder this may be the only file a work item ever
gets, and it is what gives such a change a place to exist at all.
