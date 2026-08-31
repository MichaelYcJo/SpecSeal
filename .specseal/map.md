# spec-to-code map

> Maps spec clauses to the code coordinates that ground them, so the next
> session opens a coordinate instead of re-searching — locating the code is the
> expensive half, and this file exists so it is paid once. Written and checked
> by machines (`evidence-check`); committed so it follows worktrees and other
> machines.
>
> This is SpecSeal's ledger for SpecSeal. It opens with the tree's first
> commit as its baseline, which is the only commit every row here can measure
> from.

## Baseline

| Item | Value |
|---|---|
| Baseline commit | `BASELINE_SHA` (2026-08-31) — the fallback for rows with no baseline of their own; open with `git show BASELINE_SHA:<path>` when in doubt |
| Coordinate notation | `<path>:<line>` from the repo root |
| Trust exceptions | none |

Each row's **Checked** column carries the date AND the commit SHA it was read
at, and drift for that row is measured from there. Rows without one fall back
to the baseline above. Re-verify row by row; bumping the header instead
re-dates every claim without re-reading one.

## Scope decisions

Judgments that don't follow from code or documents alone.

| Decision | Content | Grounds |
|---|---|---|
| The ledger opens at one commit | Every row below is stamped at this tree's first commit rather than left to the header alone | A row with no stamp of its own measures from the header, and a header nobody re-reads re-dates every claim at once. Stamping them all at the baseline costs nothing today and makes the first genuine re-verification visible |

## Routing declarations

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The Review and Destination axes are strict; a value outside the vocabulary makes the file not a declaration | `hooks/routing.py:45`, `hooks/routing.py:49` | Read, not run. `parse` returns `None` unless both answers are members | 2026-08-31 `BASELINE_SHA` | The Implementation axis is deliberately lenient at the same coordinate |

## Rider stamps

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| Every `# RIDER:` carries the date and SHA it was verified at, and the SHA is an ancestor of HEAD | `tests/test_a_rider_reaches_its_file.py:111` | Executed: the suite passes on this tree, and the eleven riders are stamped at the baseline commit | 2026-08-31 `BASELINE_SHA` | The stamps were re-cut for this tree; the commits they named before do not exist here |

## Evidence drift

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A row reads DRIFTED when its range was touched since the row's own baseline | `skills/evidence-check/scripts/evidence_check.py:202` | Read, not run | 2026-08-31 `BASELINE_SHA` | Every row here shares the baseline, so nothing can drift until the second commit |
