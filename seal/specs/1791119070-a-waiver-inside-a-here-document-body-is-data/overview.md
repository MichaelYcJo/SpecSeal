# 1791119070-a-waiver-inside-a-here-document-body-is-data — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` of this work item; `docs/commit-review-gate-spec.md` §*Which repository, and what happens when it cannot be read* (the paragraph on what the shell executes) and §*A file edit goes through the `Edit` tool*; `docs/the-commit-gate-inside-git.md` §*The commit gate inside git* (the paragraph on how a stop is put); `seal/config.md`; `templates/sdd-phase.md`, `templates/sdd-overview.md`
· evidence: `seal/ledger/1791119070-a-waiver-inside-a-here-document-body-is-data.md`: W1–W6 added, and 15 `Re-read ·` rows for every released row phase 1 drifted
· verified: executed: the new cases red at the base hooks and green after, seven mutations (M2 survived and is recorded below), the two host modules with `tests/test_the_waiver_can_be_typed.py`, the eight modules Q2 names, the docs checkers, `evidence-check --strict`, ruff on the touched files. Read: the 31 released rows before re-stamping. Unverified: the full suite, which is the sealer's

## Why this work exists

A waiver token that a command only carried inside a here-document body could
silence the commit gate. Now both consent reads skip bodies, and they can
only refuse a waiver the base honoured, never grant a new one.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The `reduce` half of the shared function | `spec.md` §*Data & interfaces*: "`one_heredoc.reduce`'s text where it matches, else `cmdline.drop_heredoc_bodies`". The build found that bypassing `reduce` changes no verdict. Over 756 admitted strings of the agreement corpus, each with the token on a body line, `drop_heredoc_bodies` alone kept no body token, so the mutation that skips `reduce` stays green | the spec: the branch stays | The orchestrator kept the frame's decisions. The branch keeps the consent reads reading the text the commit reading reads for that shape, and it holds if the splitter's boundaries move. No case can pin it today (`phases/phase-1.md`, M2) |
| A module the plan did not name | `plan.md` phase 1 named the two host modules, the waiver module and eight modules with a heredoc and a token. `tests/test_a_gate_that_fails_says_so.py` also went red: `answer-write.py` now imports `cmdline.py` through `given` | the code: the expected list names `answer-write.py` | A broken `cmdline.py` really does skip that gate now, and a skipped answer writer carries no token, so the git hook refuses. That is the closed direction (`phases/phase-1.md`) |
| Two coordinates in `plan.md` | §*Operational impact* placed `classify` in `hooks/cmdline_base.py`, which does not hold it (the `classify` beside `switch_kind` is `hooks/worktree-guard.py#classify`), and wrote G6's anchor with its old hash, so `evidence-check --strict` exited 2 on this work item's own records | corrected in place, the sentences' point unchanged | `evidence-check`'s record check names both. Its text asks for the record to be corrected (`phases/phase-2.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| A body token carried end to end through `hooks/answer-write.py` and `hooks/answers.py` to a real git hook. Executed only at `tokens.given`; `tests/test_the_commit_gate_decides_at_the_commit.py` passed whole but has no body case | the review chain (`warden`) |
| `spec.md` case 5, text the splitter takes for a body and the shell does not: no case pins the stop it now gets | the review chain (`warden`) |

## Not done

- The worktree guard's consent read, `hooks/worktree-guard.py#has_token`,
  still reads here-document bodies for `[worktree-ok]` and `[shared-tree-ok]`.
  `questions.md` Q1 was answered (b). The read is filed as #780 by the
  orchestrator, and that file belongs to sibling item D.
- `has_marker` and `tokens.given` still disagree on a command that does not
  split cleanly: one falls back to a substring test, and the other reads
  nothing. `spec.md` §*Out* keeps that choice out of this item.

## Fed back into the spec

none — the two policy sentences this work changed were planned in `spec.md`
§*Grounding*, not inferred while building.
