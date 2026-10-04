# a pact row outside the config table is refused — questions for the planner

<!-- seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The judgments #759 and the spawn left open
were decided from the tree. Each is listed here so nobody reopens it, with
the grounds in `spec.md`:

- **Every row, or the pact rows only?** The pact rows only. Of every reader
  of `config_rows`, the pact reader alone loses a record that cannot be
  recovered, and it is already the module's one refusing reader
  (`spec.md` §*The decision #759 left open*).
- **A stray `Pact notify` where no `Pact` value stands?** Ignored, as an
  in-table one is. Refusing it would leave every moved row in a repository
  that holds no pact (round 2 of #756, 🟡 2).
- **A stray `Pact` row with no `Pact` row in the table?** Refused. Under
  the default it is the case that loses a clause-citing record.
- **A pact row inside a fence or a closed HTML comment?** Not refused, by
  #429 and #667's rule.
- **A block-quoted pact row?** Refused. It is the vendored grammar, held
  once and pinned equal.
- **A list-marked one?** Not refused. Neither grammar reads it as a row.
- **An empty value?** Not refused. It means the default, and the template
  ships such rows.
- **W11, a pact row cut by a `str.splitlines`-only character?** In scope,
  on GFM's cut. A row the reader read on either cut is never refused.
- **The vendored copy?** It gains GFM's cut. Its shape is pinned equal to
  the reader's.
- **`vendored_config_rows`?** No rule. It carries no pact value.
- **The `notify` wording in `chain-check` and `pact-check`?** Kept. The new
  refusal sentence printed beside it names the cause.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Which released ledger rows drift, and does each claim still hold after the edit? | the work | Only `evidence-check` after phases 1–3 names them for certain. Seen at framing, read: `seal/releases/0.18.0.md` rows 6 and 8, `seal/releases/0.18.1.md` rows 168, 170, 175, 201 and 228 | re-read each against the edit and write its `Re-read ·` row into this item's fragment with `--reverify --into`; correct a claim the edit made false first | ⬜ |
| Q2 | Does any existing case, or any `seal/config.md` this repository's tests build, hold a pact-shaped line the new rule refuses, which would turn an existing case red? | a measurement | Run the pact modules after phase 1. A red case is either a fixture that was always ambiguous (fix the fixture and say so in `phases/phase-1.md`) or a scope error (stop and record a divergence in `overview.md`) | expect none. The one fixture helper read at framing, `table()` in `tests/test_a_signatory_declares_its_pact.py`, builds every row inside one table. `config_text()` in `tests/test_a_signatory_records_a_pact_change.py` was not opened | ⬜ |
| Q3 | Is the refusal sentence readable after all three callers' lead-ins? | the work | The text in `spec.md` §*Data & interfaces* is a shape, not a pin. Phase 2's cases print it through each caller | the builder words it once in phase 1, reads the three prints in phase 2, and pins the final text in phase 4 | ⬜ |
