# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 925216d7 |
| Ran by | smith on Opus 5.5 (filled by the orchestrating session, which spawned it with `model: opus`) |

## What this phase was asked

`plan.md` phase 2, in `round_record.py`: `touched` reads `own_commits`;
`own_units` per owned commit; `close` filters `measure`'s `added` and
`changed` to owned units before `depth_two` and `call_sites`;
`fix_pass_units` takes the same filter; `unit_adders` reads `own_units` for
the `fixed` commits; `parse_range` refuses a start that does not reach its
end; the `fixed` guard asks `own_commits` and its message is rewritten. See
S1–S6 red first. `skills/code-review/orchestration.md` §*And name the fix
surface* links the home, and `tests/test_the_rules_have_one_owner.py` gains
the rule's entry (Q5).

## What this phase found

**`own_units` says how, not only who.** `spec.md` §*Data & interfaces* gives
it the shape `{(path, unit): {full, …}}`. It returns `{(path, unit): {full:
"added" or "changed"}}` instead, because `unit_adders` answers which `fixed`
commit ADDED a unit. A later fix that only changed the unit is not that
answer. With a set of commits, the unit would gain a second candidate finding
and the depth refusal would fall back to its file-level message. The case
`test_a_unit_one_fix_added_and_the_next_only_changed_is_the_first_fixs` pins
it. `overview.md` records the divergence.

**`touched` filters by what the end carries, not by status letter.** The spec
says "deletions left out". A path an own commit deleted is not at `b`, and a
path only a sibling deleted after an own change is not at `b` either. One
intersection with `tracked_at(root, b)` covers both, where a status filter
would let the second through as a file the heuristic read. Phase 3 makes
`tracked_at` verbatim; until then a name git quotes falls out of `touched`,
which S10 measures.

**Two mutations survived the cases as first written, and each now has a
case.**

| Mutation | Why it survived | The case that turns it red |
|---|---|---|
| `fix_pass_units` keeping every unit | S4 put the sibling's unit in a file of its own, and `touched` already drops that file | S4's `the-fixed-file` parameter: `s` merged into the top of the very file round 1's fix rewrote |
| `unit_adders` counting a commit that only changed a unit | no depth case had a later fix change an earlier fix's unit | `test_a_unit_one_fix_added_and_the_next_only_changed_is_the_first_fixs` |

**`touched`'s path filter shows only in the heuristic note.** The per-unit
filter is what keeps a merged-in unit out of both rows, so dropping the path
filter changes no row. It changes which files the record's comment says the
diff-line heuristic read. S1 now merges a sibling's `.js` file in as well,
and the record must not name it.

**`commit_units` reads every changed path, a deleted or prose one included.**
A skip for either was an equivalent mutant: neither adds a unit the range's
ends hold, and `measure` decides what reaches a row. Taking both skips out
left no branch that no case can reach.

**Q5, answered.** The entry is rule 17, owned by `docs/the-record-layout.md`
§*A range owns the commits that descend from its start*. It has four
carriers: `chain_check.py` (`own_commits`' docstring), `round_record.py`
(the module docstring), `skills/code-review/orchestration.md` §*And name the
fix surface, in the same record*, and `docs/round-record-spec.md`. Each
sentence was seen red by `bin/mutation-check` except the spec's link in
§*The fix range*. That one survived because the file names the section a
second time, in §*A fix of a fix*.

**0.19.0's `A1` is corrected, not re-read.** `plan.md` and `spec.md` say a
re-read. Its claim says a finding lands in "a top-level unit the previous
record's `Fix range` added … or changed", and a unit a merge brought in no
longer lands. A `Re-read ·` row cannot restate a claim, so the row is a
`Corrected ·` one that carries every coordinate the claim rests on.
`overview.md` records the divergence.

**Seen red first (§15)**, all against 38d96e95:

| Case | Red at 38d96e95 |
|---|---|
| S1 | `New units` read `added_unit (depth 1); ADDED (depth 1); sibling_unit (depth 1)`, `sibling.py` after `mod.py` |
| S2 | `New units` read `sibling_unit (depth 1); added_unit (depth 1); ADDED (depth 1)`, the merged unit first in its file |
| S3 | `Contract changes` read `helper → caller, pytest; caller → no call site found` |
| S4, its own file | `first — 🟡 1 at sib.py#s, a unit round-1's fixes added` |
| S5 | exit 0, and the record written |
| S6, both parameters | exit 0, and the record written |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `touched`'s `git diff --name-status -M` between the range's ends | `chain_check.own_commits`, read in `touched` and intersected with the paths the end carries |
| `unit_adders`' own `measure` per `fixed` commit | `own_units` over the `fixed` commits |
| the two `is_ancestor` calls of `close`'s `fixed` guard | membership in the `own_commits` list the surface also reads |
| the `fixed` guard's message *lies outside --range* as the whole reason | the rewritten message, which keeps the phrase and adds the merge and a commit a merge brought in |
| 0.19.0's `A1` claim | a `Corrected ·` row in this item's ledger fragment |
