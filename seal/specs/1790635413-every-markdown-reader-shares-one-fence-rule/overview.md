# 1790635413-every-markdown-reader-shares-one-fence-rule — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this work item; `docs/the-evidence-ledger.md` §*A marker counts only on a live line*; `docs/the-broad-gate.md` §*A fenced example in a config file is not a config row*; `CLAUDE.md` §*a change writes fragments*; `CONTRIBUTING.md` §*What a change to a gate must carry* (read through the plan's grounding)
· evidence: `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` F1–F3, G1, R1, C1, M1, H1, H2, B1; three rows corrected in place in `seal/releases/0.4.0.md` (`demote`'s fence, a fenced marker as a mark, a gathered marker as a substring), and re-read notes on the rest the edits drifted, across `seal/releases/`
· verified: executed — each phase's module and its neighbours, every new case red first, a mutation per unit; read — the drifted rows' claims against the edits

## Why this work exists

Nine markdown readers decided by rules of their own whether a line was quoted, so a fenced example, a commented-out draft or a code span could change a release fold, a changelog check, a rider verdict, a lost-correction report, a meter's sections or the command the sealer runs; they now ask one rule.

## Where spec and implementation diverged

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
| The new cases on the Windows and Linux legs — S18's two new rows print a path, and S13 carries a CRLF shape | CI's test matrix at the pull request |

## Not done

The readers `spec.md` puts out of scope are untouched, and `fence_opener`'s docstring now names each with its reason. `evidence_check.py`'s comment saying that docstring "names the readers #584 has not brought over yet" is left standing for work item C, as `questions.md` D4 decided; the pointer still resolves. `hooks/routing.py#table_rows` and the other readers with no fence state at all are a different class, which `spec.md` gives the orchestrator to file.

## Fed back into the spec

none — `spec.md` is unchanged; the comment-run reading is recorded as a divergence above rather than written back as a clause.
