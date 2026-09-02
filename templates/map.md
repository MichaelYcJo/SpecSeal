# spec-to-code map

> Maps spec clauses to the code that grounds them, so the next session opens a
> coordinate instead of re-searching — locating the code is the expensive half,
> and this file exists so it is paid once. Written and checked by machines
> (`evidence-check`); committed so it follows worktrees and other machines.
>
> Group rows by area with `##` headings. A work item's own rows go in
> `.specseal/map/<work-item-id>.md` rather than being appended here, so two
> branches never queue at one file — the checker reads both addresses. The
> release folds each fragment into this file, under a heading for the release
> and one for the work item, and removes the fragment: after the merge there
> is no branch left to queue.

## Coordinates

A coordinate names **content**, never a position:

```
path#anchor@hash
```

The major level is the enclosing unit: a function or class for code, a heading
path for a document (`"## Verify / ### Scope"`). An optional minor level after
`>` narrows to the statement a claim is about. The hash is eight hex characters
over whichever region applies. Escape a pipe inside a quoted anchor as `\|`, or
the row splits the table it lives in.

**An anchor degrades to DRIFTED, never to BROKEN.** Only the major level can be
BROKEN. A minor anchor that stops matching means that place changed, so the row
widens to its unit and says re-read — never *go edit the ledger*.

**The minor level is an escape hatch, not a habit.** Reach for it only where a
unit is large enough that whole-unit hashing has been MEASURED to drift rows on
unrelated edits.

| Item | Value |
|---|---|
| Coordinate notation | `path#anchor@hash` from the repo root |
| Trust exceptions | <paths whose coordinates need re-verification, and why — or "none"> |

**A row carries no line number and no commit SHA.** A line number moves for
edits that have nothing to do with the claim, so a coordinate built from one
rots on contact, and everything that used to compensate for that — a baseline,
a stamp, a re-anchoring — is gone with it. `evidence-check` calls git for
nothing.

The **Checked** column carries the date somebody read the code. Re-verifying a
row is re-reading it and then running `evidence-check --reverify`, which
recomputes the hash and says which rows it changed.

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
something to settle a judgment, record the outcome on the row you used and put
the date you read it in the "Checked" column. Only rows in your work's scope —
the ledger fills as tickets accumulate, never by speculative bulk audits.

A row whose anchor a change removes is REMOVED, not re-pointed at something
else: its claim went with the code. Write the new claim as a new row.
-->
