# Survivors — a bare `yes` sets the run length, and a session review has no row

<!-- What the hygiene workflow's form reports for this branch —
`survivor_check.py --range origin/release/v0.15.0...HEAD` with every
`seal/specs/*/survivors.md`, the range CI reads — and why each report is not a
defect. Six places, measured at the round 1 fix pass (2026-09-24) on the
committed tree: five share words with `seal/ledger.md`'s F8, which this branch
REMOVED (its claim went with the code) and re-founded as the fragment's B2; the
sixth shares the shape of `run_reopened`'s old body. A seventh, the F4 note in
`seal/ledger.md`, was false and is CORRECTED with a dated marker rather than
excused (round 1's 🟡 1).

Round 1 read this file as excusing six reports where the range produced one,
and the fix pass first dropped the five. That reading was the check's own
artefact, not a fact about the tree: `survivor_check.py#corrected` collects the
n-grams of every sentence the range ADDED and `wanted` subtracts them, and a row here quotes
the standing sentence it excuses, so the quotes themselves silenced the five
reports whether or not this file was handed over as `--exempt`. With the rows
removed, the CI form reports all five again (exit 1); with them present, it
reports each as `exempt` (exit 0). So the rows stay, and the mechanism is
named in the fix pass's hand-back for whoever owns the check. The quote is
the anchor: an exemption stops holding when the standing text changes. -->

| Path | Quote | Grounds |
|---|---|---|
| `docs/review-chain-spec.md` | A reason after `no` is an answer too, and 30 of this repository's own records are written that way | The `Needs a fix` table's `no` row, unchanged and still true. F8 quoted the same count as evidence for the `no — <why>` case; what this branch removed from F8 is its bare-`yes` reading, which this sentence does not carry |
| `skills/code-review/scripts/chain_check.py` | The tail after `yes` is required by the caller that wants it and never here, which is the shape the template and `agents/warden.md` both show | `yes_or_no`'s docstring, and the sentence is still exact: the parser leaves the reason to its callers, and `says_reopened` and `stopping_floor` are now the callers that want it for both rows. F8 built its *why the floor refuses and `Needs a fix` does not* on this sentence; the sentence was never the false half |
| `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` | def test_yes_with_a_separator_and_nothing_after_fails(repo): | A case name F8 cited as an anchor, not a sentence F8 stated. The case still pins the floor row's `yes —` and B2 does not cite it because it is about the floor, not `Needs a fix` |
| `seal/ledger.md` | **Executed** 2026-09-04 at `46a70f0`: both cases green. | F1's own Verified cell, which shares *both cases green* with F8's. F1's claim is the floor's grandfathering and was re-read by this branch with a dated note |
| `skills/code-review/scripts/chain_check.py` | cell = field(table_rows(reader, reader.readable(text)), WRITTEN_LATE) if cell is None: | `written_late_reason`'s body, which shares the shape of `run_reopened`'s old body — the shape its own docstring says it copied. It reads `Written late`, treats a bare `yes` as None already, and is deliberately left reading through `yes_or_no` rather than `says_reopened` (`overview.md` §Not done): folding it in would widen a #138 change into that row's unit |
| `skills/code-review/scripts/chain_check.py` | One reader for both, because two would be two hand-kept spellings of one vocabulary -- the drift this file closes everywhere else. | `yes_or_no`'s docstring; F8's Notes repeated the sentence as its grounds. It is still true of the parser, and `says_reopened` does not add a second spelling — it reads through this one |
