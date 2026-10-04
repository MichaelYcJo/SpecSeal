# 1791076833-the-reverify-writer-records-before-it-restamps — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing here blocks the build.** This run is unattended and nobody is asked
anything during it. The owner's answers of 2026-09-28 and 2026-10-03 on #647
are inputs, recorded in `spec.md`'s Grounding.

**Inherited, not reopened.** `1791019474`'s `questions.md` (read at
`b4c9deb2`, on PR #749's branch) decided Q1–Q11 from the tree and answered
Q12, Q13, Q15, Q16 and Q17 by measurement or by the work: the names *pact
change* and *pact review*, the record's place, what each notify value records,
taking by content hash with `holds` / `amended`, no pact review for a clause
change, the pact review as an ordinary work item, `cmarkgfm` as the oracle and
its pin, the grammar standing, the exit classes, no CI print, the vendored
copy's `LEFT` line, `pact_check.py#shown`, and the walker's two callers. This
work item carries their code unchanged in intent, so those answers stand. A
reviewer overturns one by opening that file.

**What the tree answered for this frame, so nobody reopens it:**

| Judgment | Answered by |
|---|---|
| Merge the old branch, or carry its work | `chain_check.py#main` judges a `routing.md` the pull request adds; `#check_round` refuses an unchecked `Pass` and an open 🔴 at a ready pull request; `round_record.py`'s depth-2 refusal keeps `1791019474`'s round 2 from closing. Carry (`spec.md` §*Decision 1*) |
| Whether the redesign's units may be fixed freely here | `skills/code-review/orchestration.md` §*A fix pass adds the unit…*: depth counts inside one chain. In this chain every carried unit predates round 1, so it is depth 0 |
| Which of #735's round-3 deferrals ride | all six. #647's comment of 2026-10-03 assigns them to this frame, and they are built in the carry set and share its units |
| What happens to the old markers and comments | `unverified_check.py#folded_items` reads a `docs/` marker as a fold, so the markers name this item. The comments name PR #749, because this item's rounds restart at 1 under the same "#647 C and D" |
| Whether the shipped `1790993137` records keep the `NAME NOT IN TREE` marks | `evidence_check.py#unshipped`: a shipped item's records are not read. Not carried |
| How released rows the carry drifts are read again | `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, under `Ledger frozen from \| 1790993141` |
| Whether the carried code ran on Windows | CI at `b4c9deb2` (`gh run view 37129036019`): pytest green on macOS, Ubuntu and Windows. Read from GitHub, not re-run |

**The rows below are the frame's own decisions and the residue.** Q1–Q4 are
values a person would be accountable for, so their answerer is `a person`.
The frame chose each with grounds, and each Status reads `decided by framer`.
Q5 goes to a measurement and Q6–Q7 to the work.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | How does this branch receive C and D? | a person | **Carry the code, leave the records, close PR #749 unmerged**: `chain_check` can pass, and every record on the tree is true. **Merge with records**: `chain_check` cannot pass without a false close. **Merge then `git rm`**: same end state as the carry, with 44 commits in the range closing another chain's findings. *Why the tree could not settle it alone: closing a pull request and keeping a branch are the owner's acts* | carry; PR #749 closed unmerged after this pull request opens; its branch kept | ✅ decided by framer — carry |
| Q2 | Does the writer's contract add W8–W10 to what was built? | a person | **Add them**: the output stops claiming writes that did not happen, a lenient read stops rewriting bytes, and a write failure stops being a traceback. Each is a behaviour change every `--reverify` user sees. **Leave them**: ship the carried writer and state the three as limits. *Why: W9 and W10 also change `--reverify` for repositories with no pact, which is scope a person owns* | add them, in phase 2; the fallback cut line drops them to one issue | ✅ decided by framer — add, with the cut line |
| Q3 | Does the record `fsync` before the ledger is applied? | a person | **No**: the order is promised against the process dying, and a power loss is a stated limit in `docs/the-pact.md` §*What this does not see*. `write_atomic` serves every writer in the plugin, and none `fsync`s. **Yes**: the record and its directory are `fsync`ed before step 3, so the order survives a machine crash. That is a new I/O path, with a Windows directory-handle question, for a failure nobody has measured. *Why: it trades a rare silent loss against platform code, which is an accountable value* | no; the limit stated | ✅ decided by framer — no, stated as a limit |
| Q4 | Is W9 scoped to the files the run writes, or to every `read()`? | a person | **The files the run writes** — planned ledgers and the record (`--into` is already read strictly at step 0): no byte the run would not write is lost, and a code file in another encoding under a coordinate keeps today's lenient read. **Every read**: a code file that will not decode turns its coordinate `BROKEN`, a verdict change in the check mode too, which is #741's ground. *Why: the encoding policy for read-only inputs is #741's to set* | the files the run writes | ✅ decided by framer — the files the run writes |
| Q5 | Which released rows does the carry drift, and which of them does the change make false? | a measurement | `bin/evidence-check` after phase 2 names the drifted rows. The smith reads each and writes a `Re-read ·` row, or a `Corrected ·` row where the claim no longer holds | none assumed. `1791019474`'s fragment held 33 `Re-read ·` rows and no `Corrected ·` row against the pre-fold layout, which is the expected order of magnitude | ✅ measured at `b67c2bbb`: `bin/evidence-check .` named 57 released rows, 56 DRIFTED and 0.18.0's P8, whose `hooks/config.py#TABLE_BREAK` was BROKEN. Each was read; P8 took a `Corrected ·` row and `--reverify --into … --checked 2026-10-04` wrote 50 `Re-read ·` rows, the rest being 0.18.0 members answered through their family's root. None other was made false. 0.15.1's L1 drifted on the base already (#752). `evidence-check --strict .`: 4352 OK, exit 0 |
| Q6 | Which unit takes W8's deferred printing, W9's strict read and W10's `LEFT` line? | the work | W8 could hold printed lines in the plan beside each file, or return them to `main` to print after apply. W9 could add a strict flag to `read` or a writer-side reader beside it. W10 could live in `apply_plan` or in `recorded_then_applied`. Each changes a carried unit, which this chain reviews at depth 0 | phase 2 decides each and names the unit in `phases/phase-2.md` | ✅ answered by the work at `4a9bdd06`: W8 in a `told` list `reverify` and `reverify_into` fill through `told_now` and `recorded_then_applied` prints after `apply_plan`, filtered by `landed_at`; W9 as a `strict` flag on `read`, taken by `reverify` and `record_pact_changes`; W10 in `apply_plan`, which returns the files it could not write, named by `recorded_then_applied` (`phases/phase-2.md`) |
| Q7 | Does #741's encoding check, once it lands, find anything in the carry set? | the work | merge `release/v0.18.1` in when #741 squashes, run its check, and fix what it names | every carried and new `open`, `fdopen` and `read_text` already names `encoding="utf-8"`; the check confirms it | ⬜ half measured: #741 had not landed on `release/v0.18.1` by the end of phase 3. An AST scan of every `open`, `fdopen`, `read_text` and `write_text` call on a line `git diff e141980a b67c2bbb` adds found 0 without an encoding, and none in a product file the branch touches; the check itself is still owed at the merge |

**Who closes the open rows.** Q5 is closed by the smith in phase 3, Q6 by the
smith in phase 2, and Q7 by the smith at the merge after #741 squashes. Each
closing names its evidence in this table's `Status` cell.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
