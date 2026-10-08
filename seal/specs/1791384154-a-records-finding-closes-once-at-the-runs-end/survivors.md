# Survivors — a records-level finding closes once at the run's end

`survivor-check --range e10a7c35..HEAD`, over round 1's fix pass, named two
places still carrying wording the pass removed. One was corrected in the same
pass (`chain_check.carried_notes`' docstring). The other is true where it
stands and is excused below.

| Path | Quote | Grounds |
|---|---|---|
| `agents/smith.md` | A correction — a finding located in a record — closes `answered` with `corrected at <sha>` as its grounds, never `fixed` | the fix-table case: a record-located finding the reviewer grades 🟡 still closes in its round's fix table this way, which is what the reworded `docs/review-chain-spec.md` sentence says too (*a 🟡 in its fix table*); the same paragraph's next sentence says a ⬜ takes no row and closes through `notes`. The removed sentence shares only *never `fixed`* and *commissions the reader* with it, and `tests/test_the_rules_have_one_owner.py` pins this spelling in both files |
