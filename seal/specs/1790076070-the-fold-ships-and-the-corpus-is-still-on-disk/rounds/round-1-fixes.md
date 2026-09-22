# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — round 1 fixes

Fix range `7f38ca1a..34a31f27`, seven commits, answering
`rounds/round-1.md` at `07b7dc1b`.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | 11b45013fa99d3d306913866b8a5d6f459416948 — the paragraph under the 1789347354 marker now names the stops `round_record.py#BLOCK_START` has (a heading marker followed by a space, list, quote or table markers, a fence, a thematic break, a setext underline) and says `#120`, `**bold**`, an HTML tag and an indented run are joined. No other copy of the old list stands: `docs/review-handoff-protocol.md` already said this |
| 2 | fixed | 11b45013fa99d3d306913866b8a5d6f459416948 — the paragraph under the 1789338080 marker now says a named script has a wrapper pair or is classified in the pinning case, and names `chain_check.py` as the one classified, per `NO_WRAPPER` in `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` |
| 3 | fixed | 8249982870e5f9ec78862328b862e641dc3d916c — 51 files, the ledger edited (three rows removed and two narrowed), nine red floors with three moved to fixtures, and a paragraph for `chain_check`'s `retired:` arm. 40919f38dfe2fd10d3368030b3c59db257f6e063 then brings the guard's wording to *a committed record*, to match finding 5's fix |
| 4 | fixed | 2bdf4be061ccbe274b55b3c7c79eecc351726702 — the memo is read through `flat`, and a missing memo passes only where `docs/` carries the item's fold marker. Executed: green at HEAD; red with the marker removed; with the memo restored from `6d410023` green, and red with one pinned phrase edited. The restored file was then deleted. `seal/ledger.md` R3 re-read and re-verified |
| 5 | fixed | 40919f38dfe2fd10d3368030b3c59db257f6e063 — a work item counts as lost only when one of its records is at HEAD (`git cat-file -e` per path), and the message says *committed at HEAD*. New case `test_a_work_item_whose_records_are_all_uncommitted_was_not_lost`, red with the filter removed and red with the message reverted. Executed on the real tree: an uncommitted-only work item planted, red at the old guard and green at the new one |
| 6 | fixed | 841536744aecfc40290928431a63cf4c0423d11e — the row now anchors at `skills/code-review/scripts/survivor_check.py#whole_range@aeae8cd7`, Checked 2026-09-23, and a note says why. Every ledger anchor into `seal/specs/` was enumerated, and the one left is `seal/ledger.md:78`, whose directory is kept. The cause, that `settle --retire` does not stop when a ledger row anchors into a directory it removes, is new mechanism: deferred #511 |
| 7 | fixed | 9922e543d478cb6c57fc148867ddabfc89ed7094 — `prose_lines` matches the raw line, as `unverified_check.py#FOLD_MARKER` does. The marker-in-a-sentence case gained an indented-marker arm, which was red with the skip matching the stripped line. The fragment's row 1 was re-read and re-verified |
| 8 | fixed | 34a31f274367025f7afd5a628c5a361ac9897f49 — `gathered_entry` counts a line as a heading only when `#` to `######` is followed by a space. New case `test_a_gathered_body_line_opening_with_an_issue_number_is_kept`, red when the check is `startswith("#")` |
