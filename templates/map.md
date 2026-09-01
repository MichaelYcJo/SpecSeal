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
comes from `git blame` of its own line, so nothing has to be typed that a
rebase or a squash could orphan, and re-verification drains row by row.
A SHA written into a row still wins, which is how rows stamped under the older
rule go on working.

**What blame gives up.** It answers for the row's LINE, so an edit that only
re-words a Notes cell moves the baseline forward with nobody re-reading the
code. The date is what makes that visible: a row read in August and re-worded
in September still says August, and the gap against `git log` is the tell.
Bumping the header instead re-dates every claim at once without re-reading one.

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
