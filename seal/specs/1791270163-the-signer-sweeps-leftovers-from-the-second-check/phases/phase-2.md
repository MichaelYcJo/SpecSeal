# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 94f22603 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 2: `read_table` quotes a glued old header as written (#831 finding 3), and the S4 case's glued loop expects the as-written quote and gains finding 2's shape at its end. Red first twice: the S4 case against the reader before the fix, and the new assertions with the `rows = […]` filter moved back inside the `if holds_old and not any(…)` branch. Then the six modules that read `read_table`.

## What this phase found

- The test edit went in first and the S4 case ran red against the unchanged reader, on the first glued shape (`|Signatory|` quoted as `| Signatory |`). After the two-line reader change it was green.
- The second red was taken through `bin/mutation-check` with the filter's guard widened to the branch's condition, which is what "moved back inside the branch" does to behaviour. The new assertions failed at their first line: the glued header came back as an entry that is not a remote URL, beside the stray-row refusal.
- **`.strip()` on the quoted line had nothing behind it.** Removing it SURVIVED over the signer, `pact-check` and pact-review modules. GFM lets a table row carry up to three spaces of indent, and the line is then quoted with them. An indented glued shape was added to the same loop, with `quoted` stripped, and the same mutation went red. It is a shape in an existing loop, not a new `def`.
- `named` stays: the "beside" sentence still uses it, as `spec.md` §*Out* says.
- Six modules, 3447 passed — the second check's figure, so the extra shape added no case.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the boolean `glued` in `read_table` | the list of glued lines as written, in the same unit; its truth is the same test |
