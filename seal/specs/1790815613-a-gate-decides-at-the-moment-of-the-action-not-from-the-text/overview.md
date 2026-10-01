# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — overview

📋 implement applied
· spec:     `spec.md` (Grounding, What the tree answered 3–11, Scope, the candidates table, Migration, S1–S15), `plan.md` (Alternatives, Phases 1–6), `questions.md` (P1–P4, M1–M11, W1–W6), `routing.md`
· evidence: none — phase 1 changed no file a ledger row anchors on; the build stopped before the phases that move rows (W4)
· verified: executed — the M1/M2/M3/M11 probes on git 2.34.1, 2.39.5, 2.43.0 and 2.50.1, M4 and M10 on 2.50.1, the M7/M8 transcript count, the P3 count, the new pin module on all four gits and each of its six cases seen red; read — the spec chain, `.github/workflows/*.yml`

## Why this work exists

The gates should decide inside git rather than from the command's text. Phase 1
measured that git cannot refuse a switch before its tree moves on any of four
versions, so the build stopped there for the owner's design call.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The pin's file name | `plan.md` phase 1: "`tests/test_the_hook_surface_is_what_the_design_assumes.py`" / written as `tests/test_the_hook_surface_git_offers.py` | the new name | The measured surface is not what the design assumes, and a file named for an assumption that failed would assert the opposite of its first case |
| M1's two branches | `questions.md` M1: "**Tree already moved, or no `HEAD` line** → S10's undo branch, and `plan.md` row U becomes the switch arm's own answer" / the build stopped instead | stop | The spawn prompt names this exact outcome as a stop: "if … M1/M3 say `reference-transaction` cannot refuse before the tree moves on any supported git … stop there". The prompt is the later and the narrower instruction, and undo is not prevention, which is what the guard's switch arm is for |
| `GIT_DIR` in a hook | spec §*What the tree answered* 3: "Hooks run with the working directory at the root of the working tree and `GIT_DIR` exported" / measured empty in `pre-commit`, `post-commit` and `post-checkout` on 2.50.1 | the measurement | `phases/phase-1.md` M4; it was set only in the `reference-transaction` git runs inside a new worktree |
| The recorded run's denies | spec §*What the tree answered* 7: "at least **3 `deny`s**" / 0 `deny` decisions in the `PreToolUse:Bash` `permissionDecision` records | recorded both | The 15 `ask`s and 102.2 minutes match the memory note exactly; where the denies were recorded, if not there, is open below |

## Not verified

| Item | Who must answer |
|---|---|
| The suite, repository-wide lint and typecheck — none of the three was run (§2); only `bin/test tests/test_the_hook_surface_git_offers.py` and ruff on that file | the orchestrator, through the sealer |
| M4: the harness version that first exports `CLAUDE_CODE_SESSION_ID`, `CLAUDECODE` and `CLAUDE_PID`, and what `CLAUDE_CODE_SESSION_ATTENDED` reads in a headless run | the orchestrator |
| M5: whether an `isolation: "worktree"` spawn runs `git worktree add` | the orchestrator — it needs an `Agent` spawn, which contract §6 withholds from `smith` |
| M6: stops lost and added per candidate over the corpora | the owner's answer for the switch arm first, then phase 1 resumed |
| M9: the stub and the pin module on Windows | the CI Windows leg |
| Which git CI's `ubuntu-latest` runner carries, so that the floor the pin runs on is known | the orchestrator, from a CI log |
| Where the recorded run's "at least 3 denies" were recorded, given 0 in the `permissionDecision` records | the orchestrator |

## Not done

Phases 2–6 were not built. M1 is the stop condition the spawn prompt named,
and the switch arm's design is the owner's call (`phases/phase-1.md` §*P4*
lists the four options as measured, with this agent's recommendation
labelled as one). P4 was therefore left undecided. P3 was decided (a), and
that binds only once phase 4 is reached. No changelog fragment was written,
because phase 1 changes nothing a user meets.

## Fed back into the spec

none — the corrections above are recorded as divergences rather than
written into `spec.md`, which is the framer's
