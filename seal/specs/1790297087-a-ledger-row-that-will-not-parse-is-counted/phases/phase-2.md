# 1790297087-a-ledger-row-that-will-not-parse-is-counted — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d78a73ad |
| Ran by | unknown — the spawn prompt did not name the agent and model; the orchestrator fills this row |

## What this phase was asked

`plan.md` phase 2, the `MALFORMED` arm: a function beside `old_format_rows`,
called from `check_ledger`; the key in `totals` and `· N malformed` on both
totals lines, printed at zero; exit 2 in `exit_code` under both readings, on
`questions.md` Q1's default (a), as one branch a later answer can move; a
`LEFT` line from `--reverify` with exit 1. The `SKILL.md` verdict row and the
`--reverify` bullet. `seal/follow-up.md`'s #299 row goes. Cases S1–S10 of
`spec.md`, each seen red against the phase-1 checker. `ANCHOR_RE` and
`resolve_unit` stay unchanged, because work item B loads both. Verified by
the modules that run the checker over a fixture repository and every module
that reads a document this phase edits, by S12 over this tree, and by the arm
over the three ledger files as they stood at `ca2afdb9`. `questions.md` Q5 is
settled here.

## What this phase found

- **Every new case was red first**, executed against the phase-1 checker
  (`e1679906`, whose `evidence_check.py` this phase had not yet touched): 14
  failed, each on the silence itself. The five S1–S3 shapes printed
  `0 ok · 0 drifted · 0 broken · 0 external · 0 old-format` at exit 0 under
  both readings; S4, S5, S6 printed no `MALFORMED`; S7 and S9 lacked the
  `0 malformed` tail; S10 printed `0 rows re-verified` at exit 0; S8's unit
  case returned 0 for a malformed total and its behavioural case exited 0;
  the vendored cell-rule case raised on the missing `cell_rule`. All 15
  green after.
- **Mutation found five units with nothing behind them**, and each now has
  a case. Twenty-one mutations of the added units, run one at a time over the
  three case modules, restored from saved bytes with `tests/__pycache__`
  cleared between them. Five survived: the table header carried across a
  blank line, a code span needing both `#` and `@`, the clause for an
  unbackticked coordinate, the *some other cell* condition, and the count
  once per text. The cases for them are
  `test_what_is_left_of_a_cell_is_read_span_by_span`,
  `test_a_fragment_row_after_a_headed_table_is_still_read`,
  `test_the_same_malformed_text_is_counted_once`, and a row in S7's ledger;
  under their mutations each is red, and every mutation now turns a case
  red. A simpler code-span pattern is red as well, on the double-backtick
  span the live `EXPANDS` row used.
- **Rule (a) is narrower than `spec.md` words it**, and the overview records
  the divergence. What the arm reads after blanking the two patterns is
  code spans holding a `#` or `@`, plus words outside a span holding both.
  An issue number beside a good anchor, `` `a.py#f@…` (#299) ``, is prose,
  and read literally rule (a) would have made that cell `MALFORMED` and
  turned an installing repository's build red.
- **The row rule comes from the shared reader.** `shared_reader` now loads
  the reader once for `fence_rule` and the new `cell_rule`. The vendored
  `vendored_split_row` is a copy for a checker `evidence-ci` puts alone in a
  repository, and a case holds it in step with the shared one.
  `ANCHOR_RE`'s pattern and `resolve_unit` are untouched. Only the comment
  above `ANCHOR_RE` changed, and that was in phase 1.
- **Q5, one fixture.** `OLD_LEDGER` in `tests/test_a_row_points_by_content.py`
  wrote the 0.1.0 `Baseline commit` row with no header, so rule (b) read it
  as a claim citing nothing, and
  `test_migrate_rewrites_an_old_row_to_its_enclosing_unit` went red on
  `1 malformed`. 0.1.0's `templates/map.md` put that row under
  `| Item | Value |` (`git show v0.1.0:templates/map.md`), so the fixture now
  does too. It was never meant as a claim. No other fixture in the 39
  modules below changed verdict. `tests/test_dispatch.py` is phase 3's run.
- **The `reverify` rider fired** (`rider_check.py`: DRIFTED on `reverify`).
  It asks whoever opens the function to decide on the `Checked` column. That
  is outside this work item's scope, and nothing here changes the column,
  so it was read and re-stamped (`36d8a548` → `90289e25`).
- **Twelve ledger rows drifted** on the units this phase edited, and each
  was re-read against the edit and holds. Each has a dated `Re-read` note and
  a re-stamped hash, the list in `overview.md` §*evidence*. One more row
  (`seal/releases/0.13.1.md`, anchored on a `seal/releases/0.4.0.md` section)
  moved with the note written into that section.
- **S12**, executed at `d78a73ad`: `evidence_check.py --strict .` reads
  `total: 2245 ok · 0 drifted · 0 broken · 0 external · 0 old-format ·
  0 malformed`, exit 0. At `ca2afdb9` it was 2221 ok, so the rise is 24:
  seven coordinates phase 1 made readable and seventeen new anchors in this
  work item's fragment.
- **The arm's answer to #299's open question**, executed: the three ledger
  files as they stood at `ca2afdb9`, copied to a scratch root and read with
  `--ledger`, name **five** `MALFORMED` rows, the framer's probe count. They
  are the rider stamp, `EXPANDS`, `SEPARATORS`, `claude_block.py#<module>`
  and the hygiene step. The two Notes-cell coordinates phase 1 also repaired
  are not among them, because the arm reads the `Code grounds` cell only.
- **Boundary run**, executed at `d78a73ad`: 39 modules, 1894 passed and 8
  skipped, exit 0. They are the six `plan.md` names and every `tests/` file
  naming `skills/evidence-check/SKILL.md`, `seal/follow-up.md`,
  `evidence_check.py`, a release file this phase edited, `"releases"` or
  `seal/ledger/`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/follow-up.md`'s #299 row (*`evidence-check` ignores a ledger row whose coordinate is malformed*) | this work item: the `MALFORMED` verdict, and the live rows it measured, repaired in phase 1 |
