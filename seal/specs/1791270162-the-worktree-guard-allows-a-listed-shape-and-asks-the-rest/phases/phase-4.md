# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 610feed8 |
| Ran by | smith on Opus 5.5 (named by the spawn prompt) |

## What this phase was asked

Phase 4 by `plan.md`, after phase 3 in the same spawn: the policy document,
the changelog fragment, the ledger rows, and the overview. Run
`survivor-check` over the whole range at the phase boundary. Stop when phase
4 closes and report; do not push or open the pull request, which the
orchestrator opens. Run only the slices the plan names.

## What this phase found

**The policy had a fourth stale section.** `spec.md` In 6 names §A,
§*Which tree* and §*Known limits*. §*Creation consent* also said what
candidate C did with a hidden creation (put it to the person, silent under
consent) and how #790's lookups took the first switch's place, and
survivor-check named the second. Both are corrected, and the released rows
resting on them, K7 and I9, took `Corrected ·` rows; G17 and K6, whose
claims hold over the rewritten §*Known limits*, were re-read.

**S10 and S11 were phase 3's and were planted here.** Phase 3's
Verified-by command ran the module and the frozen-reading pin, which
neither case is in, so nothing caught their absence at its close. S10 binds
`LEAVES_THE_TREE` to phase 1's counted table (`RECORDED` in
`tests/test_worktree_guard.py`) and keeps the movers off it; S11 asserts the
removed symbols are gone and the switch arm spawns no `rev-parse`. Each was
red under a break through `bin/mutation-check` before it was committed:
`rebase`'s count changed and its row removed (S10), `classify` defined
again and `rev-parse` written into `_finding_tree` (S11).

**Two of the scenarios cannot take a ledger row.** S13's subject is this
work item's own fragment, which a citation may not name, and S14's is the
pull request body, which is no file; a record under `seal/specs/` would
anchor one, and leaves at `settle`. S1–S12 have rows. S2's own case, a diff
of every ladder reason against fixtures taken at the base, was not planted:
the ladder's code and texts are unchanged but for reading the tree once,
and its existing reason pins pass unchanged.

**A heading holding a `/` cannot be cited.** `evidence-check` could not
locate `### A. Branch switch (`git switch` / branch-form `checkout`)` under
either quoting, so S12 cites its parent, `## Decision matrix`.

**The new policy sentences are pinned.**
`test_the_guard_policy_says_which_shapes_reach_the_rows_and_who_reads_the_stop`
and `test_the_guard_policy_says_nothing_is_read_past_the_base` replace the
two pins phase 3 retired; each is red against the policy at `9c03ae85` (it
lacks the new sentences and still says "Two rules are read past the base.")
and under a break of a pinned word.

**Survivors.** After the two corrections, `survivor-check --range
a9d7b0e5...HEAD` reports 105 places, each read and none a defect: the
released ledger, the records of the work items that built the readings,
`hooks/cmdline.py`'s own redirection reader, three policy sentences that
stay true, and phrase coincidences. `survivors.md` holds one row for the
range in each spelling, and with it the check excuses all 105, and 136 over
`origin/release/v0.20.0...HEAD`, which also reaches #841's records of the
sampler and `.test_durations`.

**For the pull request body: the prompt budget.** Under the person's
`automation` press the change asks no person anything new: every new stop
is a `deny` to the model, which rewrites in the plain spelling and retries.
Without the press each unrecognised shape in a tree that matters is one
`ask`. Over this repository's recorded runs, on phase 1's pair definition
and tree-blind, so each figure is an upper bound on stops where the tree
matters:

| | Cut 1, before 2026-10-03 | Cut 2, to 2026-10-06 |
|---|---|---|
| distinct (command, directory) pairs | 31,193 | 33,239 |
| pairs holding a git segment | 8,960 | 9,707 |
| pairs stopped by an unrecognised shape | 315 | 333 |
| of them, a `checkout` with no `-- <path>` | 280 | 297 |
| an unlisted subcommand (`update-ref`, `symbolic-ref`, one in a variable) | 14 | 14 |
| a string handed to a shell | 13 | 13 |
| a command that would not split | 5 | 5 |
| a substitution body | 3 | 3 |
| a redirection read as the subcommand | 1 | 2 |
| pairs stopped that the guard before #826 did not stop, at its most cautious | 55 | 57 |
| pairs the guard before #826 stopped and this one neither stops nor sends to the ladder | 0 | 0 |
| person-stops added under the press | 0 | 0 |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| §*Which tree*'s two rules read past the base and candidate C's paragraph | gone with their code; §*Which tree* says so in one paragraph |
| §*Known limits*' option-table, lookup and #790-slot bullets | gone with their code; the new limits replace them |
| §*Creation consent*'s #678 and #790 sentences | the sentences that say what §A does now |
