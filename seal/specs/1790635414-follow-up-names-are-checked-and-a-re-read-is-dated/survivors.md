# Survivors — follow-up names are checked, and a re-read is dated

The sweep after phase 5 (`survivor-check --range origin/release/v0.16.0..HEAD`,
3911a8c..59e0cf8) reported three places. None presents a removed rule as
current: one is a dated note in a released ledger row, and two are regular
expressions carrying the path class `ANCHOR_RE` now builds from
`ANCHOR_PATH`, whose compiled pattern is byte-equal to the one it replaced.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.4.0.md` | A `# RIDER:` was added inside `reverify`, which moved the unit's hash and changed no code: it records that the function rewrites the hash and never the `Checked` column | a dated note in a released row's Notes cell, recording the state on 2026-09-10; this work item's `Re-read 2026-09-29 … phase 4` note on the same row follows it and says `reverify` gained `--checked` |
| `skills/evidence-check/scripts/evidence_check.py` | r":(?P<start>\d+)(?:-(?P<end>\d+))?\b" | `OLD_COORD_RE`, the pre-anchor shape, whose path half is the same class as a coordinate's by design; this range spelled `ANCHOR_RE`'s path through `ANCHOR_PATH` without changing its pattern, and left this unit alone because the `# RIDER:` above it is stamped against its content |
| `skills/settle/scripts/settle.py` | r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?)" | `settle.py`'s own copy of the anchor grammar, unchanged by this range; the pattern the range re-spelled is byte-equal to it, so nothing the copy says went stale |
