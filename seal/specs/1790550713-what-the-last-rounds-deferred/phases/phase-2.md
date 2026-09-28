# 1790550713-what-the-last-rounds-deferred — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 756926a |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Close #625. Re-run `spec.md`'s pair-class enumeration first. Rewrite the
comment above the first `close` in
`test_re_closing_a_half_restored_record_is_refused_for_every_word` (S7). It
has to be true of all three parameters: a draft judgment and exit 0 for all
three, the pair's notice under `fixed` alone, and exit 1 only at a ready pull
request. Write it from what the code does, not from round 2's paste-ready
text, which says the pair prints for all three. Reword the "Not
`code == 0`:" opener in `test_a_fix_commit_carries_no_empty_code_span` the
same way (S8). The assertion stays `in (0, 1)`.

Re-wrap the ragged lines the #623 range left under 88 columns with no word
changed, and show it by diffing before and after. `unverified_check.py
--help` must stay byte-identical (S10). Re-read and re-stamp every row
`evidence-check` names. Stay off the files items A and C edit.

## What this phase found

- **The pair-class enumeration found the same two instances.** A `git grep`
  for *`close` exits*, *still exits*, *exits 1 on*, *notice about* and
  *Not `code == 0`*, rounds excluded, gives the two test comments and nothing
  else that states `close`'s exit. Two hits in
  `1790297083-…/phases/phase-3.md` are a record of a past state. The window
  count (`nobody` within three lines of the context words) came to 199, 123
  in live prose, where `spec.md` says 164 and 109. The context words were
  spelled differently, and that count is not a coordinate. Nothing it turned
  up is a third instance (executed 2026-09-28).
- **S7's measurement, executed with the assertion tightened to
  `code == 0` and the output printed, then restored from kept bytes:**
  - judged as a draft, all three words exit 0, and so does the sibling case;
  - `Pass` beside `nobody` appears in the output for `fixed` and the sibling
    case only. For `answered` and `deferred` no `:0` notice line prints.
- **The mutant `plan.md` names could not isolate `close`.** With
  `run_check`'s draft payload removed, `new` inside `round_one` also judges
  the fixture as ready. It fails there, on the unticked `Pass` and on
  `Broad gate: not yet`, before the case reaches `close`, so all four went
  red for a reason the comment is not about. The mutant was narrowed to
  `close`'s own call: the check is called with no payload, which is how a
  ready pull request is judged. Then all three words exit 1, because the
  fixture's `Broad gate` still reads `not yet`, and `fixed` also fails on the
  pair.
- **So S7's wording "exit 1 only at a ready pull request" is true of the
  pair, but in this fixture it is not only `fixed`'s.** The comment says
  what was measured: exit 0 for all three as a draft, the notice for `fixed`
  alone, and exit 1 for all three as ready, `fixed` on the pair as well. The
  S8 comment says the same for its one `fixed` run.
- **Six ragged lines, not five.** The #623 range also left "pull request — a
  reader" as a mid-paragraph line in
  `tests/test_the_rules_have_one_owner.py#test_a_correction_row_closes_answered_and_never_fixed`.
  A search for short prose lines among the range's additions found it. Two
  other short lines are not ragged: `chain_check.py`'s "refuses that today"
  ends its paragraph, and `rendered` in `test_unverified_rows_close.py` is
  formatter layout. Of the range's Python lines over 88 columns, the frame's
  four are all there are.
- **The re-wraps, measured by a `test_tmp_*` probe that ran once from the
  scratchpad and was deleted** (executed):
  - each of the five docstrings is whitespace-split equal before and after,
    and its layout changed;
  - the `--baseline` help string's value is byte-equal, and
    `unverified_check.py --help` is byte-identical at 1432 bytes;
  - no Python line the #623 range added that is over 88 columns, or is one of
    the two fragments, is left at the tip.
- **The ledger: 14 rows over both phases, as the frame estimated, but not
  the same 14.** Phase 2 drifted twelve rows: S13 (`0.10.0`), three in
  `0.11.4` (one of them from the sixth re-wrap, which the frame did not list),
  R2 (`0.12.1`), G5 (`0.14.0`), C3 and C5 (`0.15.5`), the fix-pass-checker
  row (`0.4.0`), S7 (`0.5.0`), R2 (`0.8.1`) and R1 (`0.9.3`). `0.15.4`'s S1
  under 1790297086 did not drift. A thirteenth row, in `0.13.1.md`, hashes
  the `0.4.0` section the fix-pass-checker row sits in, and took the second
  `--reverify` pass its own notes describe. Every claim holds; each row has a
  dated `Re-read` note. The first `--reverify` also re-stamped that
  section-anchored row before its note was written. That row was then read,
  and given its note, before the second pass.
- **Phase 1's close left one refusal standing.** `evidence-check`'s records
  arm refused `phases/phase-1.md`, which names the renamed case, from
  `08940e2` until this phase marked the line `NAME NOT IN TREE`. Phase 1's
  check ran before that file existed. At `756926a`: 2469 ok, 0 drifted,
  0 broken, 0 malformed, 0 refused, exit 0 (executed).
- **Verified by** (executed):
  - `bin/test` over `tests/test_the_fixes_close_the_record.py`,
    `tests/test_a_script_copied_alone_exits_2.py`,
    `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`,
    `tests/test_unverified_rows_close.py` and
    `tests/test_the_rules_have_one_owner.py`: 440 passed, 1 skipped;
  - after the ledger edits, `tests/test_a_merge_cannot_silently_drop_a_correction.py`,
    `tests/test_no_real_identifiers.py` and
    `tests/test_one_word_one_meaning.py`: 75 passed;
  - `uvx ruff check` and `uvx ruff format --check` on the six Python files,
    clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the comment claiming "a green `close` still exits 1 on the chain-check notice" | the rewritten comment at the same place, which says what a draft and a ready judgment each produce, measured |
| the "Not `code == 0`:" opener in `test_a_fix_commit_carries_no_empty_code_span` | the reworded comment at the same place |
