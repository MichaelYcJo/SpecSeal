# 1790297087-a-ledger-row-that-will-not-parse-is-counted — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | a77eed92 |
| Ran by | unknown — the spawn prompt did not name the agent and model; the orchestrator fills this row |

## What this phase was asked

`plan.md` phase 1: the five live rows of `spec.md` §*The live instances*
parse. Each is re-read against its code; a claim that holds gets its
coordinate corrected (`\"` for the four quoted locators, a real unit in place
of `<module>`), `--reverify` fills the hash, and the row takes a
`Corrected 2026-09-25` note in the file it lives in (`seal/ledger.md`,
`seal/releases/0.4.0.md`, `seal/releases/0.12.0.md`). A claim that no longer
holds is corrected or taken out under `CLAUDE.md`'s rules. The `\"` escape is
written into `templates/ledger.md`, `skills/evidence-check/SKILL.md` and the
comment above `ANCHOR_RE`, leaving `ANCHOR_RE` and `resolve_unit` themselves
unchanged. `questions.md` Q3 and Q4 are settled here. Verified by
`evidence-check --strict .` before and after, and by every test module that
reads a document this phase edits.

## What this phase found

- **The frame holds.** A scratch probe applying `spec.md`'s rules (a) and
  (b) to every `Code grounds` cell, through the module's own `unquoted` and
  the shared reader's `split_row`, named exactly the five rows `spec.md`
  lists, and nothing else.
- **Two more coordinates never parsed, both in a Notes cell.** Scanning every
  cell of every table row for a backticked `…#…@…` that neither pattern
  matched named, besides the five and the shapes `spec.md` §*Must not be
  refused* lists: `seal/ledger.md`'s eval row cites
  `tests/test_what_the_reader_understands.py` with bare `"` inside its quoted
  locator, and its separator row cites `chain_check.py`'s one-line
  `CLOSED_WORDS = {…}` the same way. `check_text` reads anchors in every
  cell, so each was meant to be checked. Both are repaired here. **The arm
  phase 2 builds will not see a Notes cell**, by `spec.md`'s design, so a
  malformed coordinate there stays silent after this work; the overview's
  *Not done* names it.
- **Q3, per row.**
  - Rider stamps (`seal/ledger.md`): does not hold. The quoted line
    `STAMP = re.compile(…)` is now `OLD_STAMP`, kept only so a case can name
    the pre-#239 form, and a stamp has named a content anchor rather than a
    commit since #239. Removed, section heading included, because it was the
    section's only row. The current claim is the fragment's row, anchored on
    `test_every_rider_carries_a_verification_stamp` and
    `test_no_rider_stamp_names_a_commit` (both run: 2 passed).
  - `EXPANDS` (`seal/ledger.md`, eval row): holds; `_eval_hides_a_commit`
    still answers True for any argument holding a character of `EXPANDS`.
    Escaped. The hash `--reverify` wrote, `6d56a043`, is the one the row
    first recorded, and so is the fixture coordinate's `770c7def`: neither
    unit has changed since 2026-08-31.
  - `SEPARATORS` (`seal/ledger.md`): holds; the set still opens with the
    space. Escaped; the hash moved `9750da73` → `3a4ffca3`, because a text
    locator in a `.py` file owns its contiguous block and the comment above
    the line grew. `CLOSED_WORDS` in the same row's Notes cell is cited by
    the constant's name, since the one-line form is gone.
  - hygiene step (`seal/releases/0.4.0.md`): holds; the step exits 0 on any
    base but `main` and runs `gather_changelog.py --check` on `main`.
    Escaped; `0cb0ca06` → `6fa69569` (the block's comment changed, as the
    row's own 2026-09-24 re-read note says).
  - `claude_block.py` (`seal/releases/0.12.0.md`): holds; see Q4.
- **Q4.** `TEMPLATE`, the constant naming `templates/claude-md-block.md`,
  carries *the block's one source*, and `write` carries *CLAUDE.md is a
  generated copy*. `claude_block.py --check` exit 0, 2026-09-25.
- **`Checked` moves to 2026-09-25** on every corrected row: the column is the
  date somebody read the code, and each was read today.
- **`evidence-check --strict .`**, executed: before, at `0abfb371`,
  `total: 2221 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0.
  After, `total: 2230 ok · 0 drifted · 0 broken · 0 external · 0 old-format`,
  exit 0. The +9 is the seven coordinates made readable and the fragment's two
  new anchors. The fragment's existence also turns the records arm on for
  this work item: `1 work item read · 47 names read · 0 refused`.
- **The modules that read an edited document**, executed: 38 modules (every
  `tests/` file naming `templates/ledger.md`, `skills/evidence-check/SKILL.md`,
  `seal/ledger.md`, `releases/0.4.0.md`, `releases/0.12.0.md`,
  `evidence_check.py` or `seal/ledger/`), 1926 passed, 7 skipped, 1 failed:
  `test_every_spec_directory_that_reached_the_ladder_has_an_overview`, red
  for this work item's missing `overview.md`. It fails at the base too (read,
  not run: the framer's commits wrote `spec.md` and no overview). This
  phase's commit opens the overview, and the case run alone afterwards is
  1 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md` §*Rider stamps*, its one row (*the SHA is an ancestor of HEAD*) | the current claim: `seal/ledger/1790297087-a-ledger-row-that-will-not-parse-is-counted.md`'s rider-stamp row; `seal/releases/0.9.1.md`'s S1 row states the checker's side |
