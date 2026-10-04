# 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 5ce9ecd2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#775's documents and this item's records. D4: `templates/config.md` §*Pact*'s
`Pact notify` paragraph points at `docs/the-pact.md` §*A signatory records a
pact change* rather than pasting round 3's text, and that pointer is pinned;
the section comment over `record_pact_changes` names the refused stale row,
in round 3's paste-ready wording. D5: round 3's two paste-ready parameters
(the usage sentence and the skill clause), each seen red by breaking its
sentence. D7: re-read `seal/releases/0.18.0.md:79` against `reverify_into`,
`reverify` and the *Without the row* paragraph, and write the `Corrected ·`
row (questions Q3's default). This item's fragment rows, the `Re-read ·`
rows through `evidence-check --reverify --into seal/ledger/<id>.md --checked
2026-10-04` after reading each released row, written with the writer as
built at this phase's head, corrections as `Corrected ·` rows under the
freeze, and the `changelog.md` fragment. Edit only the `Pact notify`
paragraph of `templates/config.md`, because sibling F edits the refused-row
paragraph of the same section.

## What this phase found

**The frame holds, with one more released claim made false.** The pointer
replaced the two-case sentence without a pasted run: the paste ratchet passed
with no pair's count rising. The section comment took round 3's text as
written. But the tree held a second released claim this work item made
false, which the frame did not list: `seal/releases/0.18.1.md:416`, #771's F3,
said that without the freeze *a second run clears* a citation the same run
moved, and cited the case phase 2 renamed. `--strict` named that coordinate
BROKEN. A re-read cannot clear a BROKEN coordinate, so it took a `Corrected
·` row, which narrows the fifth thing to the freeze, adds the one-run and
narrowed behaviour, and carries every coordinate the claim still rests on
with the renamed case in place of the old one. A `grep` of every released
file for *second run* beside *citation* or *re-stamp* found no other row of
that class.

**D7, read.** `reverify_into` writes `Re-read <checked> by work item <item>`
into the Notes of each `Re-read ·` row; `reverify` splices `dated_cell` into
the date cell and writes no Notes cell; the *Without the row* paragraph of
`docs/the-evidence-ledger.md` says an unfrozen repository re-stamps *with a
dated note*; and `skills/evidence-check/SKILL.md` §*Re-verifying is
recomputing the hash*, the section the released row cited, names no Notes
trace. The `Corrected ·` row says those four things and cites the first three.

**The writer that wrote this item's re-reads is the one this item built.**
The fragment's own rows were written with placeholder hashes and filled by
`bin/evidence-check --reverify --ledger <the fragment> --checked
2026-10-04 .`, 47 coordinates in 8 rows. A run without `--into` then named
29 released rows a re-read owed. Each claim was read against the code and
documents as this branch leaves them, and each holds: none states the order
of the walk, the old hash of a recorded move, a citation's pact part, or a
second run. `bin/evidence-check --reverify --into <the fragment> --checked
2026-10-04 .`, run on `795d4aff`, whose code is this item's final code,
wrote the 29 `Re-read ·` rows, exit 0, `0 released rows left`. No `Pact`
row is declared here, so nothing was recorded.

**A record must not quote a coordinate from a test's scratch tree.**
`phases/phase-2.md` quoted the citation S7 recorded, a coordinate into
`seal/releases/0.1.0.md`, and the records arm read it as a claim about this
tree and named it BROKEN. It now gives the two hashes alone.

**Run at the phase boundary, executed:** `bin/test` over
`tests/test_no_passage_is_pasted_into_a_second_file.py`,
`tests/test_the_ledger_rules_have_one_home.py`,
`tests/test_no_real_identifiers.py`, `tests/test_docs_line_wrap.py`,
`tests/test_one_word_one_meaning.py`,
`tests/test_every_reader_ends_a_line_where_gfm_does.py`,
`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`,
`tests/test_a_folded_statement_names_what_enforces_it.py` and the three
evidence-check modules, 869 passed; `bin/evidence-check --strict .` exit 0,
5364 ok and nothing else; `bin/evidence-check --strict --ledger <the
fragment> .` exit 0; `bin/correction-check --range 94d7b2e0..HEAD`, no
released ledger file changed. The suite as a whole is `unverified`, answerer
the sealer.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
