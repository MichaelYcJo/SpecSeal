# spec-to-code map

> Maps spec clauses to the code coordinates that ground them, so the next
> session opens a coordinate instead of re-searching — locating the code is the
> expensive half, and this file exists so it is paid once. Written and checked
> by machines (`evidence-check`); committed so it follows worktrees and other
> machines.
>
> Group rows by area with `##` headings. Split into `.specseal/map/<area>.md`
> only if one file stops being workable — the checker finds both.

## Baseline

| Item | Value |
|---|---|
| Baseline commit | `<SHA>` (<YYYY-MM-DD>) — the fallback for rows with no baseline of their own; open with `git show <SHA>:<path>` when in doubt |
| Coordinate notation | `<path>:<line>` from the repo root |
| Trust exceptions | <paths whose coordinates need re-verification, and why — or "none"> |

Each row's **Checked** column carries the date AND the commit SHA it was read
at — `2026-08-24 \`a1b2c3d\`` — and drift for that row is measured from
there. Rows without one fall back to the baseline above. Re-verify row by
row; bumping the header instead re-dates every claim without re-reading one.

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
stamp the "Checked" column with the date and the HEAD SHA you read it at.
Only rows in your work's scope — the ledger fills as tickets accumulate,
never by speculative bulk audits.
-->
