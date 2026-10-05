# 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 98f2651a |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#772 and D3. S4 (the pinned case rewritten to one run), S5, S6 and S7, each
seen red. Then D2's dependency order in `reverify`, so a citing file always
follows the file it cites, the narrowed `LEFT` in `main` naming a citing row
outside the narrowing whose citation the run moved, with exit 1, and D3's
skip of a citation's move. In `docs/the-evidence-ledger.md`, rewrite the
fifth item's unfrozen sentence and the lead-in's *except where the last
item says a second run clears it*, moving their pins in
`test_the_home_names_each_thing_no_re_read_clears` and replacing the *second
run* parameter rather than deleting it. Check the usage and the skill for a
*second run* claim. Run the Q2 churn probe once and record what it shows; do
not fix the churn in this item.

## What this phase found

**The frame holds.** `resolve_patterns` sorts, `reverify` hashes a citation
through `read`, and `read` answers from the open plan, exactly as the plan's
technical context says. S4, S5, S6 and S7 were each red at `f995fd89`, which
changes nothing these cases reach: S4 and S5 with `--strict` exit 2 and the
citation named DRIFTED, S6 with exit 0 and no `LEFT` line, and S7 with a
second record row for M carrying its citation of
R's line as a part, `@15ceb729 → @a9b719d7`.

**S7 runs twice, and the second run is what makes it red at the base.** At
the base the one run walks M before R, so M's citation is still OK and no
citation part is appended; the second run re-stamps the citation and records
it. With D2 alone the first run already re-stamps the citation, so without
D3 the part would land in run one. Two runs pin both.

**A citation is found once, by one helper.** `row_citation` is the first
coordinate of a citing row's `Code grounds`, matched on the line as
`family_view` matches it. `cited_first` reads it to order the walk, the D3
skip reads it to know which offsets are citations, and `citations_left`
reads it to find the rows a narrowed run left. `family_view`'s own lookup is
unchanged, to keep the edit off sibling F's ground and off a function this
item does not need to touch.

**The narrowed `LEFT` compares the citation before and after the plan.** It
reads each citing row in a file the narrowing left out whose citation names
a file the plan writes, grades the citation against the planned text, and
names it only where it is DRIFTED now and was OK against the file on disk.
`PLANNED` is cleared for the second reading and put back in a `finally`.

**The usage and the skill carry no *second run* claim.** `grep` over
`skills/evidence-check/SKILL.md` and the usage text found none, as the frame
said. The skill does not describe the unfrozen narrowed `LEFT` at all, so no
skill sentence changed.

**Mutations, one at a time through `bin/mutation-check`.** Red: the walk
order (`for ledger in ledgers`), the dependency edge, the self-citation
guard and the cycle fallback (both after
`test_the_walk_order_survives_a_self_citation_and_a_cycle` was added, since
nothing reached them before), the D3 skip, the narrowed `LEFT`, its exit,
its `was == "OK"` test, its `status != "DRIFTED"` test (after the third
shape of `test_a_narrowed_unfrozen_run_names_no_citation_it_did_not_move`
was added), and the three sentences of the evidence-ledger home. Two
survived, and both are short-circuits rather than rules:

- `planned_key(target) not in held`. Where the plan does not write the cited
  file, the citation reads the same before and after, so it is never DRIFTED
  now and OK before. The test skips a `cited_row` call and changes no
  answer.
- `file_identity(path) in read_here`. A file the run walked has its
  citations re-stamped by `cited_first`'s order. The one way its citation
  can still be left is a row `--checked` leaves whole for having no date
  cell, which the run already names as `undatable`; the skip keeps it from
  being named twice. No case builds that row.

**Q2's probe confirms the mechanism the frame read.** One file,
`test_tmp_churn.py`, run once at `6414f110` from a scratch directory outside
the tree, then deleted with the scratch repository it built. The tree: the
freeze; released R1 at `handler@h0`, read 2026-01-01; fragment A re-reading
R1 at `h1`, 2026-02-01; fragment B re-reading R1 at `h2`, 2026-03-01; the
code at `h2`. `--strict` before: exit 0, `5 ok · 0 drifted`. `--reverify
--checked 2026-04-01` without `--into`: exit 0, printed
`src/service.py#handler  96c68feb -> 20974dca`, `1 row re-verified`, and
dated `seal/ledger/2000000001-a.md:1` 2026-04-01. A's line changed from
`…handler@96c68feb` with `2026-02-01` to `…handler@20974dca` with
`2026-02-01 · 2026-04-01`. `--strict` after: exit 0. So the in-place walk
re-stamps and re-dates an outranked older `Re-read ·` row that `--strict`
read OK, and nobody re-read it. That is a different mechanism from #772's
and is not fixed here (questions Q2's default); `overview.md` §*Not done*
carries it for the orchestrator to file.

**Run at the phase boundary, executed:** `bin/test
tests/test_a_signatory_records_a_pact_change.py
tests/test_a_released_row_is_read_again_in_a_fragment.py
tests/test_evidence_check.py -q`, 489 passed at `98f2651a`; `uvx ruff check`
and `uvx ruff format --check` on the touched `.py` files. The suite as a
whole is `unverified`, answerer the sealer.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_an_unfrozen_restamp_of_a_released_row_moves_the_line_its_re_read_cites`, which pinned the two-run behaviour #772 removes | `test_one_unfrozen_run_restamps_the_citation_its_restamp_moves`, the same tree in one run |
| The `second run` pin of `test_the_home_names_each_thing_no_re_read_clears`, and the sentence it pinned | the `one unfrozen run`, `a narrowed unfrozen run` and `the lead: a person repairs each` pins, over the rewritten fifth item and lead-in |
