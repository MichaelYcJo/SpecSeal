# Survivors — a records-level finding closes once at the run's end

`survivor-check --range e10a7c35..HEAD`, over round 1's fix pass, named two
places still carrying wording the pass removed. One was corrected in the same
pass (`chain_check.carried_notes`' docstring). The other is true where it
stands and is excused below. Over round 2's fix pass (`be3c452a..HEAD`) it
named two more, both true where they stand.

| Path | Quote | Grounds |
|---|---|---|
| `agents/smith.md` | A correction — a finding located in a record — closes `answered` with `corrected at <sha>` as its grounds, never `fixed` | the fix-table case: a record-located finding the reviewer grades 🟡 still closes in its round's fix table this way, which is what the reworded `docs/review-chain-spec.md` sentence says too (*a 🟡 in its fix table*); the same paragraph's next sentence says a ⬜ takes no row and closes through `notes`. The removed sentence shares only *never `fixed`* and *commissions the reader* with it, and `tests/test_the_rules_have_one_owner.py` pins this spelling in both files |
| `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/routing.md` | The owner pressed `automation` for every 0.21.0 work item in one batch | a record of the routing answer the owner gave on 2026-10-07, true of that batch; it shares *every 0.21.0 work item* with the changelog clause round 2 removed and says nothing about the cutoff |
| `skills/code-review/scripts/chain_check.py` | rule, so the first records held to it are the ones written under it. | another cutoff's comment, whose value is the id of the work item that added its rule, so the sentence is true of it; `NOTES_FROM` is the one cutoff that is not its own item's id, and its comment now says why |
