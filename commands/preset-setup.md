---
description: Merge the specseal CLAUDE.md block into the user's CLAUDE.md with semantic dedup — propose, get approval, then apply.
---

# /preset-setup — reviewed CLAUDE.md merge

Merge the preset's CLAUDE.md block into the user's global `~/.claude/CLAUDE.md`
(or the target the user names). Unlike `install.sh`, which only inserts the
marker block mechanically, this command deduplicates — and every deletion goes
through the user first.

## Procedure

0. **Ask the scope first** (unless the user already said): global
   (`~/.claude/CLAUDE.md` — every project on this machine) or this project
   (`./CLAUDE.md` — committed, so teammates receive it via git). Recommend
   project scope for team repos, global for personal machines. Warn if the
   preset block already exists in the *other* scope — both files load, so the
   block should live in exactly one.

1. **Back up.** Copy the target file to `CLAUDE.md.bak` before touching anything.
   If the target does not exist, just write the preset block and stop.

2. **Read both.** The preset block is the content between
   `<!-- specseal:start -->` and `<!-- specseal:end -->` in this
   plugin's CLAUDE.md. Read the user's file in full.

3. **Classify each overlap** between the user's existing content (outside any
   preset markers) and the preset block:

   | Finding | Proposal |
   |---|---|
   | Exact duplicate — same rule, same meaning | Propose removing the user's copy (the block now owns it) |
   | Partial overlap — user's rule is more specific | Propose **keeping the user's rule** and note it overrides the block's general form |
   | Conflict — different values for the same concern (e.g. response language) | Ask which side wins. Never decide silently |

4. **Present the result as a diff** — the full proposed file, with each change
   annotated by its classification above. Do not apply anything yet.

5. **Apply only after approval.** If the user amends the proposal, re-present
   the diff. After applying, confirm the marker block is intact and nothing
   outside it changed except approved deletions.

## Rules

- Never delete or rewrite user content without an approved diff line covering it.
- Never modify anything when the user rejects the proposal — the `.bak` and the
  untouched original must both survive.
- If the user's file already has a preset marker block from an older version,
  treat its contents as preset-owned: replace it without asking, and diff only
  the user-owned remainder.
