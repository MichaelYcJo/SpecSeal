# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — overview

📋 implement applied
· spec:     (filled when the work item closes)
· evidence: (filled when the work item closes)
· verified: (filled when the work item closes)

## Why this work exists

A repository folding with `settle` had the statement shape and the document
ceiling as rules and nothing that reads them, because both checks lived in
this repository's tests; now they ship as `fold-check`, read their values from
`seal/config.md`, and this repository's tests pin the shipped command.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How the command finds the `seal/` root | `spec.md` §*Data & interfaces*: "The root is resolved the way `broad_gate.py` resolves it"; `plan.md` §*Technical context*: "Copy the shape, not the code … a second root resolver is a copy `agent-contract` §16 already names." The code loads `hooks/optin.py#home_at` by path | the code | `home_at` is the one resolver, answering the same two places in the same order, and `settle.py#main` already loads it by path from the same directory. Loading it writes no second resolver, which is the thing the plan's sentence warns against. It also honours the opt-out marker, which `broad_gate.py#seal_home` does not read |
| Which phase removes `seal/releases/0.15.1.md`'s S1 | `plan.md` phase 2: "The three release-file rows whose anchors left `tests/` are REMOVED there". After phase 2, every anchor of 0.15.1's S1 still stood | phase 3 | A row is REMOVED when a change removes its anchor (`CLAUDE.md` §*commit early*). `OVER_CEILING`, `FROZEN_IDS_DIGEST` and the prose pin leave in phase 3 |
| The prose pin's name | `spec.md` §*Scope* item 3: "The prose pin (`test_the_evidence_ledger_states_the_values_these_constants_hold`) reads the three values from `seal/config.md`". The case is now `test_the_evidence_ledger_states_the_values_the_config_rows_hold` | the rename | The spec names the case in order to say what it will read, and the old name says it holds constants that the same item removes. Nothing outside this work item's own ledger rows named it: 0.15.1's S1 anchored it, and that row is removed · NAME NOT IN TREE |
| What the ceiling messages say about the digest | `spec.md` §*Scope* item 1: "Their messages are pinned as they stand; a changed message is a §14 change and is pinned anew." Two of them named `FROZEN_IDS_DIGEST`, which item 3 removes | changed, pinned anew | A message naming a constant that no longer exists is false. The new wording names the `Over the ceiling` row and prints the current digest, which is `spec.md` §*Data & interfaces*' "printed by the command itself when the count or the ids disagree" |

## Not verified

none — every claim this work item makes was executed or is labelled read in the phase record that makes it.

## Not done

- **`marker_digest`'s `sorted` is pinned by nothing.** Removing it leaves the
  suite green, because no fixture holds a listed document whose markers are
  reordered without being swapped. The unit was moved by this work item, not
  added, and the mutation record 0.14.0's P1 carried did not list it either.
  A case that reorders two markers in a listed document and expects no
  problem would pin it.

## Fed back into the spec

none
