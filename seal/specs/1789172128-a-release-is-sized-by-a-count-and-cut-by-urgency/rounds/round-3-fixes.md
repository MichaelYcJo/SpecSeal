# round 2's fix pass — the table `round_record.py close` applies

Range: `405fe9d..34beebb`. Two commits; the round record they answer is
`rounds/round-2.md`. Spelled parent-of-first-fix to last, because `a..b`
excludes `a`.

The builder's session was resumed a second time rather than replaced.

Finding 7 takes no row: the reviewer closed it `answered` — `hits()`'s
two-boundary escape is unreachable at 88 columns, and the reachable residual is
a statement split across string literals, which `flat()` cannot see either.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `95b3d83`, `docs/issues-and-milestones.md:150-158`. **Written once from the coordinates rather than adjusted a third time**, which is what the round asked: this clause was wrong in the build (two moments conflated) and wrong again in round 1's fix (*a release earlier*). It now says `size: now` comes off when the release reaches `main` and the issue closes, and that `merged: X.Y.Z` goes on **earlier inside that same release** at the squash, naming the gap as exactly the interval §*A label says a ticket is already in* exists to fill. Read by the orchestrating session against all three coordinates — `:208`'s title, `:210-211`'s *for the length of a release*, and `docs/branch-and-release.md:256-258` — and it is now true of both mechanisms and names the other label's mechanism rather than its distance |
| 2 | deferred #366 | **`round_record.py close` refused this fix at exit 2, and the gate's exit was taken on the repository owner's answer.** The pass took two cases and refused a third: the third would have pinned `hits()`, created by round 1's fix pass, which is depth 2. The two it took pinned `STATES_A_SIZE` and `SCANNED`, both created by build phase 4, so by what they pin they are depth 1 — and `depth_two` refused them anyway, because it keys on the **finding's `Location`** and then refuses every unit the range adds in that file. Finding 2's Location named three coordinates, one of them `hits()`, because the finding was one observation about three fixes. So the two depth-1 cases were refused beside the depth-2 one. `docs/review-chain-spec.md` §*The depth in `New units`* says depth is a declaration the verifying round checks and does not say what a check owes a finding whose Location spans two depths. **Both cases were written, run, and measured before being reverted** — each red under exactly its own mutation and the only failure, the module green at 9 — and the orchestrating session re-derived that before the revert: dropping the pattern's three noun alternatives turned `test_the_pattern_catches_the_noun_forms_and_not_only_the_verb` red and only it (NAME NOT IN TREE), dropping `CLAUDE.md` from `SCANNED` turned `test_the_scanned_set_reaches_the_file_a_rule_gets_restated_in` red and only it (NAME NOT IN TREE). **The three widenings stay and ship unpinned**; only the two cases and their `NOUN_FORMS` constant were reverted, the module is 7 passed, and `uvx ruff check` and `uvx ruff format --check` are exit 0 after it. Two coordinates were removed from ledger row R1 rather than re-pointed, and R1's claim is unchanged on the five that remain. **#366** is the named home the depth rule's exit requires, and it carries the drafted cases, the measurement, and the open question about a Location spanning two depths |
| 3 | deferred #365 | The checker is the plugin's own gate, not this work item's code, and changing it pulls `CONTRIBUTING.md`'s four requirements onto a prose ticket — the same split #363 got. **#365 is filed**, with the measurement at three tips and all four requirements answered. What was this work item's is the disclosure, at `34beebb`: every `survivor-check exit 0` recorded here as *every survivor excused* excused nothing. Re-derived by the orchestrating session — `--range 7e17f5e..HEAD` exits 0 **with and without** `--exempt`, the identical line both times, so `survivors.md`'s four rows are consulted by nothing. Corrected in `overview.md`'s proof block and a new `## Not verified` row, `phases/phase-5.md`'s section and table row, `rounds/round-2-fixes.md`, and `survivors.md`'s header. The four rows are **kept** — they become correct again when #365 lands. One sentence of *another* work item's ledger row, `seal/ledger/1789108681-…md`'s S10, was qualified without touching its claim, which rests on a grep and is unaffected |
| 4 | fixed | `95b3d83` for the docstring and `34beebb` for the ledger row. `:31-32` now reads *excludes only this module, **by basename rather than by path***, and says what that buys — a copy of the module anywhere in the scanned set is excluded with it. The same wording was corrected in R1, which folds into `seal/ledger.md` at the release and is why this was not just a comment |
| 5 | fixed | `34beebb` |
| 6 | fixed | `34beebb` |
| 8 | fixed | `95b3d83` |

## What was run over the fix range

Executed by the fix pass, exit codes read directly with no pipe: `uvx ruff
check` and `uvx ruff format --check` on the module (0 each); five modules
narrowly (79 passed); three mutations one at a time, each restored and asserted
(1 / 1 / **0** — the third being the refusal's evidence); a per-alternative
census over the scanned set confirming every `is the size` match still lies
inside the two excluded files; `test_a_rider_reaches_its_file` (29 passed, so
the new `seal/follow-up.md` row does not trip the no-coordinate rule);
`bin/evidence-check .` before, `--reverify`, and after; `bin/unverified-check`
(5 open · 1 closed); and seven further record modules (357 passed).

**Re-run by the orchestrating session at `34beebb`**, because a hand-back's
verification claim is a claim: eight modules one per call — the module 9,
wrap 23, release-hygiene 32, one-word-one-meaning 13, no-real-identifiers 2,
row-points-by-content 102, record-states-the-tree 58, rider-reaches-its-file
29 — **exit 0 each**; `uvx ruff check` and `uvx ruff format --check` on the
module, **exit 0** each; both new cases mutated alone and each red for its own
mutation and no other; the finding-1 sentence read against its three
coordinates; `bin/survivor-check` with and without `--exempt`, identical.
`bin/evidence-check .` exits 1 with the ledger arm at **1147 ok · 0 drifted ·
0 broken** and the records arm's one drift at `spec.md:159`, which round 1
decided stays.

**No unit added, and that is the gate's doing rather than the pass's.** The pass added two cases at what it read as depth 1 and refused a third at depth 2. `round_record.py close` refused all three at exit 2, keying on finding 2's `Location` rather than on what each case pins, and wrote no cell. The owner's answer was to take the gate's exit, so the two cases and their `NOUN_FORMS` constant were reverted, two now-dead coordinates came out of ledger row R1, and the work went to **#366**. The three widenings those cases would have pinned are still in the tree and ship unpinned — which is the cost of the exit, stated rather than absorbed.

**Contract changes: none.**

**Not run: the broad gate.** `agent-contract` §2 assigns it to the sealer, once,
after the rounds settle — which is when round 3 closes.
