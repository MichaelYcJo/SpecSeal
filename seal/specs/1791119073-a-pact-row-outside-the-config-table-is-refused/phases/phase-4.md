# 1791119073-a-pact-row-outside-the-config-table-is-refused — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | eeb6c043 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The records. `docs/the-pact.md` §*How a signatory names the pact*: the
clause and its `Enforced by:` cases. The vendored paragraph of §*What this
does not see*, where phase 3 changes what it says. `templates/config.md`
§*Pact*: the refused-row sentence. S16's pins. The ledger fragment: rows for
the new units, and the re-reads of released rows citing edited units through
`evidence-check --reverify --into`. `changelog.md` in this directory. Q1
answered by the run.

## What this phase found

**The vendored paragraph gained a sentence, and its pinned one is
unchanged.** `tests/test_a_signatory_records_a_pact_change.py#test_the_documents_say_what_the_writer_does`
pins the paragraph's existing sentence (*a `Pact` row and a `Pact notify`
row that both carry a value*). That sentence stays true after phase 3,
because both rows still carry a value on one cut or the other. So the change
is one sentence added after it and a fifth `Enforced by:` case. Neither that
pin nor the parallel sentence in `skills/evidence-check/SKILL.md` moved, and
both sit in the region sibling E edits.

**Q1: fourteen drifted coordinates, eight released claims, every claim
holds.** At
`eeb6c043`, `evidence-check .` named 14 DRIFTED coordinates, in eight
released rows:

- `seal/releases/0.9.1.md` row 120 and `0.12.0.md` row 105, through
  `config_rows`;
- `0.18.0.md` rows 6 (P1) and 8 (P3);
- `0.18.1.md` rows 168 (C1), 170 (D2) and 175 (W9);
- `0.5.0.md` row 107 (S8). The four `Re-read · S8` rows already citing it
  drift with it and read the same `# Repository config` hash, as do 0.18.1's
  rows 201 and 228.

The framer's list missed two of them: 0.9.1 row 120 and 0.12.0 row 105, the
two through `config_rows`, which this work drifted by moving its walk.
`--reverify --into` wrote eight `Re-read ·` rows. Each claim was read against
the edit. Two now go further than they said, and their notes say so: P1
(stricter, a stray row is a refusal) and C1 (wider, the vendored copy looks
on both cuts). The two `config_rows` rows note that it is now a projection
of `indexed_config_rows`. No claim was made false, so no row is a
correction.

**S16 seen red.** Each of the five pinned sentences was deleted once under
`mutation-check`, and the case went red each time.

**The ledger after the build.** `evidence-check .`: 5288 ok, 0 drifted, 0
broken. `evidence-check --strict .`: exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
