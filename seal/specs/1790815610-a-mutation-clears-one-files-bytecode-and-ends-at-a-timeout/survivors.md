# Survivors — a mutation clears one file's bytecode and ends at a timeout

Round 1's fix pass (`survivor-check --range d6ce226a..f0bce32e`) reported one
place. The range corrected L1's claim in the ledger fragment, because the
command now runs the cases against the file as it is first and clears the
bytecode before that run as well. The approved plan's Ledger table quotes L1
as it was planned, and it is left as written: it records what the build was
asked to claim when the plan was approved, and rewriting an approved plan
afterwards would misstate what the owner read. The claim the plan quotes is
also still true of the mutated run, which is the run it describes.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/plan.md` | One mutated run removes exactly the mutated file's cached bytecode, for every interpreter tag and wherever the file lives, before the cases run and after the restore, and writes none | the approved plan's own record of the claim it asked for; L1 in the fragment carries the corrected claim with a `Corrected 2026-10-01` note, and what the plan quotes still holds for the mutated run |
