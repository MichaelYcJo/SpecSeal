# verified facts to merge into the work item's ledger fragment

| Claim | Grounds | Label |
|---|---|---|
| the four doc tests (28 cases) and `evidence_check.py --strict` (69 ok · 0 drifted) pass at b80c2a5 — the two fragment rows' "Verified behavior" cells can move from Read to Executed once the round record lands | warden round 1's own runs | Executed |
| the Checked cell of the re-stamped `.specseal/map.md` row moves to the date it was actually re-read (rides 🟡 3's fix) | `.specseal/map.md:97` | Read |

drained — both rows applied by the round-1 fix pass (cells moved Read→Executed on executed grounds; the Checked date rode 🟡 3's fix).
