# Survivors — a bare `yes` sets the run length, and a session review has no row

<!-- What the hygiene workflow's form reports for this branch —
`survivor_check.py --range origin/release/v0.15.0...HEAD` with every
`seal/specs/*/survivors.md`, the range CI reads — and why the report is not a
defect. Measured at the round 1 fix pass (2026-09-24): two places. One is the
F4 note in `seal/ledger.md`, which was false and is CORRECTED with a dated
marker rather than excused (round 1's 🟡 1). The other is below.

This file used to carry six rows, measured over the build's own range
`659b4229..HEAD`, which starts after the frame commit and is a range CI never
reads. Five of them quoted sentences that share words with the removed F8
(`seal/ledger.md` line 822 before this branch) and anchored nothing at the
target SHA; they are dropped rather than kept, because a quote is an anchor
and an anchor that no report reaches excuses nothing. The quote is the
anchor: an exemption stops holding when the standing text changes. -->

| Path | Quote | Grounds |
|---|---|---|
| `skills/code-review/scripts/chain_check.py` | cell = field(table_rows(reader, reader.readable(text)), WRITTEN_LATE) if cell is None: | `written_late_reason`'s body, which shares the shape of `run_reopened`'s old body — the shape its own docstring says it copied. It reads `Written late`, treats a bare `yes` as None already, and is deliberately left reading through `yes_or_no` rather than `says_reopened` (`overview.md` §Not done): folding it in would widen a #138 change into that row's unit |
