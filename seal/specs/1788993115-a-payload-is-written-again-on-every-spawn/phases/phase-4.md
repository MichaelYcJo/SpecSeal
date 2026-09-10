# 1788993115-a-payload-is-written-again-on-every-spawn — phase 4

<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/phases/phase-4.md
— what this phase of the build did, written by the implementer when the
phase closed. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `26e4236` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build phase 4 of `plan.md`'s Phases table, the last: `payload-after.json`
from the same transcript as the before-run, with no new spawn, and the delta
at the smith's own ratio, said in those words in the changelog; the twelve
`seal/ledger.md` rows anchored on `skills/implement/SKILL.md` sorted into
removed-and-restated (the anchor moved with the Bootstrap section) or left
(re-verified where the hash drifted), the fragment scoped for the write and
the read unscoped, ending at 0 broken; `changelog.md` in the shape of
`1788433011`'s, four entries with the five-minute finding inside the meter's;
`overview.md` closing the one red case in the tree; the `docs/flow.md` tick
for #292 with one sentence for #120 naming the five-minute finding and Q4's
probe, nothing else in that file; `README.md` and `README.ko.md` naming
`payload-meter` where they name `session-cost`; every remaining pointer to a
moved section, fixing only those that point at a section that moved; the
narrow verification set plus every module the branch touched; `survivor-check`
over `0bd135f..HEAD`, corrected or excused with a quote; this record, the
Status cell, and the hand-back to the review chain.

The spawn prompt labelled its facts. Executed: phase 3's verification re-run
at `9e7bc89` (165 passed over eight modules, `claude_block.py --check` exit 0,
the block byte-identical to the template, ruff clean), and the one red case
being the overview one. Read: the transcript for `--calibrate` is phase 1's,
and the meter's smallest-prefix rule keeps the measured totals the same
spawns; the fragment rule and the two `--reverify` commands; the flow, README
and pointer coordinates; the memo's and the changelog's shapes. Unverified
with this phase as answerer: what `survivor-check` reports once the records
are written.

## What this phase found

**The read fact *only the byte composition changes* was false in one
respect, and the meter was wrong with it.** Calibrated against the same
transcript after the cut, the meter divided the smith spawn's 36,295 measured
tokens by the 90,534 bytes the tree holds now instead of the 104,261 that
spawn read, printed 2.49 B/token where the spawn paid 2.87, and reported +979
tokens on `agents/smith.md` with 0 bytes changed; its total-delta row then
subtracted an estimated after-total from a measured before-total, −6,773
where the files summed to −4,691. Both are fixed in `6ddfa69`. With
`--baseline` given, an agent whose smallest spawn is the one the baseline was
calibrated from, over a different byte count, keeps the baseline's ratio, is
labelled estimated throughout, and its row says to take a spawn after the
change for a measured after-number; a delta whose two totals rest on
different bases sums the per-file token deltas and says so. Each case was
red before the fix (`assert -5802 == -5300` for the second), and three
mutations — the detection returning `None`, the bases never differing, the
removed files not subtracted — each turned exactly its own case red, the
module green again on the restored bytes. Without `--baseline` the meter
still cannot tell; the docstring says so and Q8 carries it.

**The after-number, in the changelog's words.** `payload-after.json` at
`ff71c51`: 13,727 bytes left `skills/implement/SKILL.md`, an estimated 4,783
tokens at the 2.87 B/token the smith's spawn paid; the `CLAUDE.md` pair grew
265 bytes (an estimated 92) for the Bootstrap pointer and the comment under
the block; the smith's payload is 13,462 bytes and an estimated 4,691 tokens
smaller, summed over its files. scribe and warden are measured as before —
their own files did not move — and pay the same +265 bytes. S3's sum clause
does not hold literally: 32,522 + 16,545 = 49,067 bytes against 46,249
before, the excess being the new file's header, `SKILL.md`'s pointer section
and this phase's reworded bullet; the moved text is what equals.

**Eight rows moved, six were re-read, and the unquoted anchor was never
counted.** Of the twelve `seal/ledger.md` rows naming
`skills/implement/SKILL.md#`, eight anchor on the Bootstrap section (S14,
S4/S12, Q7, S5/🟡 4, 🟡 1/🟡 4/r3 1, r3 4, S7, S11/S12); they are removed
there and re-stated in the fragment at
`skills/implement/orchestration.md#"## Orchestrator: Bootstrap — create
what's missing"@8d418684`, `Checked` set to today and a note saying why the
coordinate moved. Row S11/S12's second coordinate was spelled unquoted
(`#Bootstrap — create what's missing@00000000`), which the checker's anchor
grammar never parsed — it was reported neither OK nor BROKEN across two
phases of drift — and it is quoted now. The four rows anchored on sections
that stayed (L6, L10, P2, the orchestrator-binding row) are left; L10 drifted
because the layout section lost the Bootstrap from under its heading, and it
is re-read with the five other drifted rows (`test_the_skill_names_where_the_answer_is_written`,
`skills/update/SKILL.md#"## Procedure"`, both READMEs' *Updating*, `COVERED`).
`--reverify` scoped to the fragment rewrote 12 hashes, unscoped 6 more; the
unscoped read at the end is 1,059 ok · 0 drifted · 0 broken.

**The fragment's existence woke the records arm on this work item's own
documents.** `evidence-check .` reads a work item's records once it has a
fragment, and it refused four names the spec documents use that nothing in
the tree carries: `ANTHROPIC_API_KEY` in `plan.md`'s alternatives (NAME NOT IN TREE),
and, in `spec.md` and `questions.md`, the two usage fields
`ephemeral_5m_input_tokens` / `ephemeral_1h_input_tokens` (NAME NOT IN TREE),
which are the transcript's and which the meter does not read. Each such line carries the
marker; it is one line by construction, and a first attempt that wrapped it
onto the next line was still refused, which is how that rule was learned —
and why this paragraph carries it twice.

**Pointers.** None of the four documents the spec and the prompt named
pointed at a moved section (`overview.md`'s third divergence row). Three
places did: `hooks/mode-gate.py`'s docstring twice, a docstring in
`tests/test_the_mode_question_is_asked_once.py`, and the moved bullet *They
fill through the feedback rule below*, which phase 2 flagged and which now
names `skills/implement/SKILL.md` §2. That bullet edit sits inside the
section the eight restated rows anchor on, so the hash they carry is the
edited section's.

**Survivor-check reports one place, and it is a record.**
`tests/test_routing_is_recorded.py:214`'s docstring says *a session read the
missing option as a chicken-and-egg the design does not have and put it to
the user twice* — the event the deleted rider described, in the test's own
words. `survivors.md` excuses it with that quote as the anchor; with the
exemption the check exits 0 over `0bd135f..26e4236`.

**Measured at `26e4236`, all executed.** The plan's narrow set plus the
twelve modules the branch touched plus `test_the_suite_has_a_command_that_is_cheap_twice`,
`test_routing_is_recorded` and `test_a_corrected_sentence_survives_elsewhere`:
553 passed, 1 failed — the overview case, closed by this record's commit.
`evidence-check .` exit 0. `rider_check.py` and `claude_block.py --check`
exit 0. `ruff check` and `ruff format --check` clean on
`payload_meter.py`, its test module, `hooks/mode-gate.py` and
`test_the_mode_question_is_asked_once.py`. One pre-existing `SyntaxWarning`
at `tests/test_a_row_points_by_content.py:763`, not this branch's, named in
the memo. The full suite, repository-wide lint and typecheck: unverified,
the orchestrator's after the rounds.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the eight `seal/ledger.md` rows anchored on `skills/implement/SKILL.md#"### Bootstrap — create what's missing"` (and the `## Document layout / ### Bootstrap` spelling) | `seal/ledger/1788993115-a-payload-is-written-again-on-every-spawn.md`, the same eight claims at `skills/implement/orchestration.md#"## Orchestrator: Bootstrap — create what's missing"@8d418684` |
| the unquoted coordinate `skills/implement/SKILL.md#Bootstrap — create what's missing@00000000` in row S11/S12 | the quoted coordinate above, in the same restated row |
| the Bootstrap bullet's *the feedback rule below* | *the feedback rule in `skills/implement/SKILL.md` §2*, same bullet |
| the ratio a `--calibrate` derived over bytes the spawn did not read, and the total delta subtracted across two bases | the baseline's ratio, kept and labelled; the sum over the files — `payload_meter.py`, pinned by two cases |
