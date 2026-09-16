# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | c0ad3fdd |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`changelog.md` and `seal/ledger/1789518345-….md` in this repository's fragment
convention, and `overview.md` carrying every divergence, what was not verified
with who answers it, and the two tickets this work opens. The `Framed` line
added to this `spec.md`, with `plan.md` rule 2's exception recorded in
`overview.md`.

## What this phase found

**`bin/evidence-check --reverify .` is a whole-tree command, and its first run
re-stamped 27 rows — 21 of them in the shared `seal/ledger.md` and belonging to
earlier work items.** A re-verified row asserts that somebody re-read the code
on that date. Twenty-one of those nobody had opened. They were reverted, and
each of the nine rows this branch actually drifted was read one at a time.

**Two of the nine had been narrowed by this branch and were corrected rather
than re-stamped.** `round_record.py#seal`'s row said the subcommand *sets the
LAST record's `Broad gate` cell and touches nothing else* — true where a round
record exists and not otherwise since phase 5. `chain_check.py#broad_gate`'s
row counted *`chain_check.py`'s three fatal refusals*, which is that FUNCTION's
count; `direct_seal` beside it now adds a fourth of the same shape. Re-stamping
either would have left a false claim in the ledger carrying a fresh date, which
is the one thing a ledger must not do.

**One row went BROKEN because this branch renamed a case it cites**, and it
kept its other four coordinates rather than being removed whole. The rule is
that a row whose anchor a change removes is REMOVED — one anchor of five went,
and the claim holds for the rest, so the dead coordinate was dropped and the
new claim written into this work item's own fragment. Removing the row entire
would have discarded four still-true coordinates to enforce a rule about one.

**`evidence-check`'s records arm refused three lines of this work item's own
phase records**, for naming cases this branch renamed —
`test_the_skill_asks_every_axis_in_the_first_batch` and
`test_the_smith_carries_both_halves_rather_than_only_citing_them`. Both are
named in the records precisely BECAUSE they no longer exist, which is what
`NAME NOT IN TREE` is for. Marked rather than reworded: a phase record that
cannot name the case it replaced cannot say what it did.

**`survivor-check` over the build range reported ten places, and exactly one
was a defect.** This work item's own `spec.md` still said *a chosen somebody
may be asked* where the row's value had become `no` — the rename's last
survivor, in the document that specifies it. The other nine are records
asserting a past state, a generated copy of a template, and three sentences
that are LANDING rather than surviving: the batch's reason moved to
`agents/framer.md` with the act, and the destination's reason moved to
`skills/implement/orchestration.md` with the question. `survivors.md` carries
each with the standing quote, so an exemption stops holding the moment that
text changes.

**The frame arm was exercised against this branch's real tree, not only
against fixtures** (`plan.md` rule 4). With the mark in place the arm is
silent for this work item; with the mark changed to `the session` by a probe,
it names the disagreement and the probe was reverted. What `chain_check` still
reports locally is the absent round record, which is correct — the rounds have
not run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md`'s coordinate for `test_the_smith_carries_both_halves_rather_than_only_citing_them` | `seal/ledger/1789518345-….md`, as a new row for the new claim. The four other coordinates of that row stay where they are, because the claim still holds for them |
| The phrase *a chosen somebody may be asked* from this work item's `spec.md` | nowhere — the value is `no`, and the sentence now says so. `survivor-check` is what found it, after the rename had been applied everywhere a reader would think to look |
