# 1790635413-every-markdown-reader-shares-one-fence-rule — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this work item; `docs/the-evidence-ledger.md` §*A marker counts only on a live line*; `docs/the-broad-gate.md` §*A fenced example in a config file is not a config row*; `CLAUDE.md` §*a change writes fragments*; `CONTRIBUTING.md` §*What a change to a gate must carry* (read through the plan's grounding)
· evidence: `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` F1–F3, G1, G2, C1, M1, P8-2, P8-3 (R1, H1, H2, B1 and P8-1 were removed with the code they anchored, in the revert after round 3); three rows corrected in place in `seal/releases/0.4.0.md` (`demote`'s fence, a fenced marker as a mark, a gathered marker as a substring), and re-read notes on the rest the edits drifted, across `seal/releases/`
· verified: executed — each phase's module and its neighbours, every new case red first, a mutation per unit; read — the drifted rows' claims against the edits

## Why this work exists

Nine markdown readers decided by rules of their own whether a line was quoted, so a fenced example, a commented-out draft or a code span could change a release fold, a changelog check, a rider verdict, a lost-correction report, a meter's sections or the command the sealer runs. The release scripts, the correction check, the meter, the role-section test, the survivor exemptions and two test walks now ask one rule; the config reader's comment half, the routing reader and the rider check were built too and taken back out after round 3 (*Not done*).

## Where spec and implementation diverged

The first three rows below describe code the revert after round 3 took out; they stand as the record of what was built and why, and none of them describes the tree.

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What *a comment that closes* means for a line inside it | Spec: "a line inside an HTML comment **that closes** is not shown", held to "`comment_scan` over the lines `blank_fences` leaves, with a line hidden only where its comment closes". Code: a line is hidden when it begins inside a comment and its run of such lines returns to a line that begins outside, or the file ends outside one | the code | The oracle the spec chose reports only the state a line BEGINS in, so it cannot tell a comment that closed and reopened on one line from one that never closed. The two readings differ only there, and the chosen one reads more rows, the direction the spec gives. Parity shape 10 pins it |
| Whether a fenced line inside an open rider block ends it | Spec: in a `.md` file "a line inside a fence span opens no rider and changes no comment state". Code: a rider block already open runs to its own `-->` through any fenced lines | the code | Inside a comment nothing is markdown, and `fence_spans` has no comment state. The spec is silent on a fence inside a rider block; the case pins the reading (`phases/phase-3.md`) |
| Which generator the three config walks read | Spec: "The three table walks … keep reading through ONE generator, and that generator hides commented lines as well as fenced ones". Code: a new generator, `table_lines`, reads `unfenced` and drops commented lines; `unfenced` stays fence-only | the code | Spec: "Names and shapes are the work's to choose", and "`broad_gate.py#fenced_row_at` stays a question about fences alone" — it takes `unfenced`'s complement, so widening `unfenced` would have called a commented row fenced |
| Phase 7's reach | Plan: phase 7 edits `fence_opener`'s docstring. Code: it also rewrites one sentence of `skills/evidence-check/SKILL.md`, which said "#584 tracks them" of readers that keep their own rule | the code | Contract §12: that sentence became false with this work, and it sits in a shipped skill a session reads |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and format check, run once after the review rounds settle | the sealer, spawned by the orchestrator with the base and this work item |
| The new cases on the Windows and Linux legs — S18's two new rows print a path (S13's CRLF shape went with the revert after round 3) | CI's test matrix at the pull request |

## Not done

The readers `spec.md` puts out of scope are untouched, and `fence_opener`'s docstring now names each with its reason. `evidence_check.py`'s comment saying that docstring "names the readers #584 has not brought over yet" is left standing for work item C, as `questions.md` D4 decided; the pointer still resolves. The readers `spec.md` called a different class, with no fence state at all, were brought in by phase 8 at the owner's request (#658), except `tests/test_release_hygiene.py#overwide_rows`, which is work item A's (#585); `hooks/routing.py#table_rows` was then taken back out, below. (NAME NOT IN TREE: the unit was removed or reverted after this was written)

**Reverted after round 3, at the owner's decision.** `hooks/config.py`, `hooks/routing.py` and `.github/scripts/rider_check.py` are byte for byte `release/v0.16.0`'s again, and so is everything that existed only because of them: `broad_gate.py`'s commented-row arm and its sentence, `seal.py`'s alias change, the comment sentences in `docs/the-broad-gate.md`, `templates/config.md` and the hook's docstring, their cases and parity shapes, and their ledger rows and changelog entries. Rows those edits had drifted in `seal/releases/` are back to their release text. The config reader's comment-before-fence reading, which the routing reader and the rider check had both taken on, reopened a finding in every round: each round's fix created the unit the next round found wrong, and the run was capped with round 3's 🟡 1, 🟡 2 and ⬜ 3 open against those units. Taking the units out closes those findings by removing their subject; it fixes nothing they described, so the three readers ship with the fence behaviour the release already had. A new work item redoes them from a clean frame, and #658 stays open for its routing half.

Round 1's 🟡 1 and 🟡 2 — the gather and the fold writing a marker below a fragment that leaves a block open — were built as phase 9 after `questions.md` Q5 was answered (a).

## Fed back into the spec

none — `spec.md` is unchanged; the comment-run reading is recorded as a divergence above rather than written back as a clause.
