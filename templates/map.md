# spec-to-code map

> Maps spec clauses to the code coordinates that ground them, so the next
> session opens a coordinate instead of re-searching — locating the code is the
> expensive half, and this file exists so it is paid once. Written and checked
> by machines (`evidence-check`); committed so it follows worktrees and other
> machines.
>
> Group rows by area with `##` headings. A work item's own rows go in
> `.specseal/map/<work-item-id>.md` rather than being appended here, so two
> branches never queue at one file — the checker reads both addresses.

## Baseline

| Item | Value |
|---|---|
| Baseline commit | `<SHA>` (<YYYY-MM-DD>) — the fallback for rows `git blame` cannot answer for; open with `git show <SHA>:<path>` when in doubt |
| Coordinate notation | `<path>:<line>` from the repo root |
| Trust exceptions | <paths whose coordinates need re-verification, and why — or "none"> |

Each row's **Checked** column carries the **date** somebody read the code —
`2026-08-24` — and nothing else. The commit that row's drift is measured from
is **the commit the row first appeared in**, derived from its own line's
history, so nothing has to be typed that a rebase or a squash could orphan and
re-verification drains row by row. A SHA written into a row still wins, which
is how rows stamped under the older rule go on working.

**First appearance, not last touch.** Last touch is what one `git blame` would
answer for free, and it resets a row's baseline on any edit to the line — a
typo in a Notes cell included. Measured on this plugin's own ledger, a single
release commit that rewrote stamps in bulk held the baseline for 16 rows of 36
that way, and for none of them by first appearance. Bumping the header does
the same thing to the whole file at once, which is why it is the last resort
rather than the cheap way out.

**A row names no commit in prose where it can be helped**, and a row's
baseline has to be a date and a SHA together for exactly that reason. A bare
hex word in a row is prose, not a stamp. In the header the same word IS read
as the file's baseline, so a fragment's prose names no commit at all.

**Moving a row between ledger files keeps its stamp, verbatim.** `git log -L`
does not follow a row out of a file that stays — the row reports the MOVE as
its first appearance in its new file — so a migration that stripped stamps
would reset every window it touched and report the result green. A stamp
written in the row wins over anything derived, which is what makes the move
cost nothing. A derived baseline is for rows born where they live. Renaming a
whole ledger file is a different case: git detects that and follows it.

**A fragment carries no Baseline section at all.** It has no need of one —
every row in it measures from its own line's history — and the two cases the
header still answers for (a ledger line not committed yet, a coordinate that
resolves in another checkout) belong to the ledger this template opens.

## Scope decisions

Judgments that don't follow from code or documents alone.

| Decision | Content | Grounds |
|---|---|---|
| | | |

## <spec area>

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| | | | | |

<!--
Feed-back rule (from the implement skill): when you open a coordinate or run
something to settle a judgment, record the outcome on the row you used and
put the date you read it in the "Checked" column — the date alone.
Only rows in your work's scope — the ledger fills as tickets accumulate,
never by speculative bulk audits.
-->
