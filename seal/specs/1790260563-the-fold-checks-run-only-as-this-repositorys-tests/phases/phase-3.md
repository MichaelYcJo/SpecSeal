# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 0f4c6f4d |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The values become rows. `Fold shape from`, `Document line ceiling` and
`Over the ceiling` are read through `hooks/config.py#config_rows` from the
resolved root. An absent row prints that nothing was checked for it, and an
unparseable value exits 2 naming the row. This repository's `seal/config.md`
carries the three, the prose pin reads the rows, and the constants go.
`templates/config.md` gains the section, and `skills/config/SKILL.md`'s table
the three rows. Verified by planted-root cases for S4 and S5 with each
message pinned, the prose pin seen red by editing the config value alone and
then the prose alone (S10), `bin/fold-check; echo $?` at 0 with no flags, and
the config-template modules narrow.

## What this phase found

- **The root comes from `hooks/optin.py#home_at`,** as phase 2 recorded. A
  bare directory with no root prints
  `neither … is declared in <dir>, which has no seal/ root at either place, so nothing was checked`
  and exits 0, which is the spec's *the flags alone decide*.
- **An empty cell is not declared.** The template writes a row left open with
  an empty value (`Mode`, `Broad gate`), and `broad_gate.py#broad_command`
  reads an empty value as no value, so `row_value` does the same. The
  mutation pass found nothing pinned it: with the `or None` gone, the suite
  stayed green, because an empty cutoff was refused at exit 2 and no case
  planted one. `test_a_row_with_an_empty_value_is_not_declared` was added,
  and it goes red under that mutation.
- **Numbers are ASCII digits.** `str.isdigit` accepts a superscript two,
  which `int` then refuses with a traceback. `WHOLE` is `[0-9]+`, and the
  entry pattern's count uses the same class.
- **The two ceiling messages changed, and are pinned anew (§14).** They
  named the `FROZEN_IDS_DIGEST` constant, which no longer exists. They now
  name the `Over the ceiling` row and print the digest the file has now, so
  a person copies it rather than computing it. Printing the entry's stale
  digest instead reddens 3 cases and 1 case.
- **The prose pin was renamed** from `…_these_constants_hold` to
  `…_the_config_rows_hold`, because no constant is left for it to hold. It
  reads the rows through `fold_check.declared`, the command's own reader,
  so a row the command would refuse fails the pin as well. Its comparison
  moved into `prose_disagreements`, and a second case asks that helper
  about each side moved alone.
- **S10 seen red on the real files.** Each edit was made on its own and
  restored from kept bytes: the config cutoff, the config ceiling, the
  config listing one document, the prose cutoff and the prose ceiling. Each
  reddened the pin.
- **`skills/config/SKILL.md` said *print all four*.** It says seven now,
  and `tests/test_the_settings_have_a_front_door.py` pins the new count
  and the three new rows.
- **Four rows outside the fragment drifted and still hold.** They are
  0.12.0's front-door row and 0.5.0's S8, S1 and S2. Each was re-read,
  noted `Re-read 2026-09-25` and re-stamped. 0.15.1's S1 was REMOVED,
  because its anchors went, and its claim is F6 in the fragment.
- **The phase crossed midnight,** so records written after it carry
  2026-09-25.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `SHAPE_CUTOFF` in `tests/test_a_folded_statement_names_what_enforces_it.py` | `seal/config.md`'s `Fold shape from` row; the planted cases keep their own `CUTOFF`, one below `BOUND` and one above `OLD`, commented as not this repository's value · NAME NOT IN TREE |
| `LINE_CEILING`, `OVER_CEILING`, `FROZEN_IDS_DIGEST` in `tests/test_a_document_has_room_for_the_next_fold.py` | `seal/config.md`'s `Document line ceiling` and `Over the ceiling` rows · NAME NOT IN TREE |
| `test_the_evidence_ledger_states_the_values_these_constants_hold` | `test_the_evidence_ledger_states_the_values_the_config_rows_hold`, same module · NAME NOT IN TREE |
| `test_this_repository_has_the_shape_through_the_command` | `test_this_repository_passes_the_command_with_no_flags` in the ceiling module, which runs both checks from the rows · NAME NOT IN TREE |
| `seal/releases/0.15.1.md` row S1 | fragment row F6, and a note in 0.15.1's comment |
