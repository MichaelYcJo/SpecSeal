# Survivors — survivors.md silences what it quotes

`bin/survivor-check --range origin/release/v0.15.0...HEAD`, run at phase 4,
reported nine places. Eight carry wording of the `seal/follow-up.md` row this
branch deleted — the range half of #507, discharged by phase 1 — and each is
right where it stands: a released changelog entry recording that the row was
once open, other rows' own closing sentences sharing a stock phrase, and two
files sharing a date or a fragment with no claim in common. The ninth is a
ledger row recording the red message a case printed on the day it was
written, which the case no longer prints in those words.

This file is the first `survivors.md` written on a range checked by the fix
it excuses: with it committed the nine are still reported without `--exempt`
and print under `exempt` with it, which is what a row was always supposed to
do.

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | Writing a `seal/specs/<id>/survivors.md` row silences its survivor a second way | A released changelog entry, a record of what that release did: it recorded the path as still open, and this branch is what closes it. A released entry is not rewritten |
| `seal/ledger.md` | is no longer the first exclusion stated | Row S3 of `1789211172` records the red message its case printed on 2026-09-12. The case now reads every exclusion as a list, says `is no longer an exclusion stated`, and asserts the order in a sentence of its own; what a row saw on the day is not rewritten to match |
| `seal/follow-up.md` | A fix pass may not add mechanism, which is why this is a row | Three other rows' own closing sentence, a stock phrase every row that a fix pass could not take ends with. The deleted row shared the phrase and none of the claim |
| `seal/follow-up.md` | and had no scope for the other two, which is why this is a row | The same stock phrase in a fourth row, with its own grounds in front of it |
| `seal/follow-up.md` | Found while writing a row during round 1's fix pass of | Another row's own account of where it was found, sharing `fix pass of` and `during round 1's fix` with the deleted row's measurement and nothing else |
| `tests/test_chain_check_at_the_pull_request.py` | the reachability requirement DISAPPEARED for a record new in the pull request | A docstring about the chain check's per-record membership test, sharing the words `exit 1 before the` and `existed, exit 0 after it` with the deleted row's account of a different reproduction. Two facts with one idiom |
| `skills/verify/scripts/broad_gate.py` | has no stopping line, so `below` is empty there whatever the file holds | A comment in the broad gate's reader, sharing a date and `and over the` with the deleted row. No claim in common |
