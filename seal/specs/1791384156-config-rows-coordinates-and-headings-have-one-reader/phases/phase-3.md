# 1791384156-config-rows-coordinates-and-headings-have-one-reader — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 776f6370 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 3: one coordinate grammar — `ANCHOR_RE`'s locator and hash
pieces exported by name; `correction_check.py` loads the checker and reads
`ANCHOR_RE` for a row's anchors and its corrections, the shared
`split_row` for a row's key, its two patterns removed; `settle.py` reads the
checker's `ANCHOR_RE` in `coordinates` and `anchored_rows`, its own pattern
removed; `rider_check.py` builds its stamp from the checker's pieces at
`load_checker`. Verified by S6, S7 and S12's first grep, red first.

## What this phase found

**The pieces compile to the same pattern.** `ANCHOR_RE` is now built from
`ANCHOR_PATH`, `ANCHOR_LOCATOR` (`ANCHOR_QUOTED` or `ANCHOR_NAME`) and
`ANCHOR_HASH`, and its compiled pattern, `RECORD_COORD_RE`'s and
`PACT_ANCHOR_RE`'s equal 5623d728's byte for byte, as does the rider stamp
built from them (probes, deleted).

**The frame's identity count was over spans, and per row it is larger.**
Over `seal/ledger.md` and every `seal/releases/*.md`, running 5623d728's
`correction_check.py` beside this one: 58 row identities gained, 5 lost, 47
rows keyed differently, every `Corrected ·` citation the same. Of the 58, two
are the paths with no `.ext` the frame named (`bin/test`,
`bin/round-record`); the other 56 are quoted locators holding a code span
or `\|`, which the old pattern's `[^`@|]` refused. The 5 lost are the
MALFORMED examples quoted in 0.15.5's and 0.15.6's rows. The 47 match the
frame. The docstring of `identities` states these counts.

**A citation is read from the Code grounds cell.** The policy says the
citation is the first coordinate of Code grounds
(`docs/the-evidence-ledger.md` §*A released row is read again in the
branch's fragment*), and the old code searched the whole row for a quoted
locator first. With one grammar the order disappears; reading the second
cell is what keeps a coordinate a claim quotes from being taken for the row
it corrects. No released citation moved.

**S12's grep finds one shape outside the checker that the spec did not
name.** `skills/evidence-check/scripts/pact_check.py#CHANGE_RE` reads a pact
review's `<work-item-id>@<content hash>`, a record id, not a coordinate; the
case exempts it by name with that reason, and a second case keeps each
exemption honest by requiring the excused fragment still to be there.

**S7, measured.** `settle`'s copy and the checker's grammar matched the same
8,218 spans over the released ledgers, 0 lines differing (probe, deleted).
`coordinate_paths` loads the checker once, at the first line it reads.

**Direction and prompt budget.** `correction-check` names a dropped
correction of 58 more row identities and of 5 fewer; nothing else moves, and
nothing gains a stop. Budget 0.

**Seen red (§15).** The new cases ran against 5623d728's
`correction_check.py`, `settle.py` and `rider_check.py` (`git stash`): every
one failed except the citation case, a pin that held there because the old
code found the same citation by a different route. `mutation-check`, every
verdict `red`: the raw split put back, the citation read from the whole
row, the hash kept in an identity, `grounds_at` at 0, `coordinate_paths`
keeping one path, the stamp's locator narrowed to the name.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `correction_check.py#ANCHOR` and `#CITATION` · NAME NOT IN TREE | `evidence_check.py#ANCHOR_RE`, read by `correction_check.py#identities` |
| `settle.py#COORDINATE_RE` · NAME NOT IN TREE | `evidence_check.py#ANCHOR_RE`, read by `settle.py#coordinate_paths` and in `anchored_rows` |
| `rider_check.py#NEW_STAMP` · NAME NOT IN TREE | `rider_check.py#stamp_pattern` over the checker's pieces; 0.9.1's S1 row is corrected in the fragment |
