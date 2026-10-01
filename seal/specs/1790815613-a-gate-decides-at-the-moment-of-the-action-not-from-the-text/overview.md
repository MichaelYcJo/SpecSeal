# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — overview

📋 implement applied
· spec:     `spec.md` (Grounding, What the tree answered 3–13, Scope, the candidates table, Migration, S1–S15), `plan.md` (Alternatives, Phases 1–6), `questions.md` (P1–P5, M1–M11, W1–W6), `routing.md`; `docs/commit-review-gate-spec.md`, `docs/worktree-guard-spec.md`, contract §9 and §17, `agents/smith.md`, `skills/implement/SKILL.md` §1
· evidence: `seal/ledger/1790815613-….md` G1–G13 (new); 30 rows in 16 `seal/releases/*.md` files re-read and re-stamped, five of them corrected in place
· verified: executed — phase 1's probes on git 2.34.1, 2.39.5, 2.43.0 and 2.50.1, M6 over 413 commands under bash and zsh, the M7/M8 transcript count, the new real-git modules on all four gits, every mutant listed in the phase records, `evidence-check --strict`, `survivor-check`; read — the spec chain, the policy documents, every drifted ledger row

## Why this work exists

The commit gate now decides inside git, where the commit happens, so no shell
construct moves a commit around it, and a commit into a declared worktree
stops costing a prompt. A worktree creation and a branch switch are still
decided before git runs, by 0.16.0's frozen reading (`questions.md` P4, P6).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The pin's file name | `plan.md` phase 1: "`tests/test_the_hook_surface_is_what_the_design_assumes.py`" / written as `tests/test_the_hook_surface_git_offers.py` | the new name | The measured surface is not what the design assumed, and a file named for an assumption that failed would assert the opposite of its first case |
| M1's two branches | `questions.md` M1: "**Tree already moved, or no `HEAD` line** → S10's undo branch" / the build stopped instead | stop, then the owner's answer | The spawn prompt named this exact outcome as a stop, and the owner answered on 2026-10-01: option 1, the switch arm keeps the frozen reading on every git |
| `GIT_DIR` in a hook | spec §*What the tree answered* 3: "Hooks run with … `GIT_DIR` exported" / measured empty in `pre-commit`, `post-commit` and `post-checkout` on 2.50.1 | the measurement | `phases/phase-1.md` M4; every hook asks `git rev-parse` instead |
| The recorded run's denies | spec §*What the tree answered* 7: "at least **3 `deny`s**" / 0 `deny` decisions in the `PreToolUse:Bash` `permissionDecision` records | recorded both | The 15 `ask`s and 102.2 minutes match the memory note exactly; where the denies were recorded is open below |
| Where the leases are | spec §*What the tree answered* 4: "lease file name under `<git-common-dir>/specseal-leases/`" / `hooks/session-lease.py#main` writes under each worktree's `--absolute-git-dir` | the code | The stub and `hooks/hooksession.py` read every worktree's lease directory of the clone |
| The text readers are not deleted | spec §*Scope* 6 and `plan.md` phase 6: delete `hooks/commit-review-gate.py`, reduce `hooks/cmdline.py` to a tokenizer / both kept, each standing aside where git decides | kept | P1's answer (a) keeps a foreign-slot clone on "0.16.0's behaviour" for every arm, and for the commit arm that behaviour is those two files. `questions.md` P5 states the trade and the alternative for the owner |
| `commit-review-gate.py` stays in `pre-bash` | `plan.md` phase 3: "removed from `GROUPS["pre-bash"]` in this same phase so the two never run together" / kept, standing aside per target where the stubs run | kept | The same P5 reading; the two never judge one clone, which is what the plan's sentence protected |
| The creation is decided before git runs | `plan.md` phase 4: "the creation refusal at `reference-transaction prepared` where M3 says the new `HEAD` is a transaction" / phase 4 decided it in `post-checkout`, which took the worktree back; the round-1 fix pass moved it back in front of git, through the frozen reading | the frozen reading | M13: nothing at `prepared` tells a creation from a switch. Round 1 found what `post-checkout`'s take-back cannot undo (`-B`'s branch reset, `--no-checkout`, `--orphan`, `--lock`, a Bash creation under `.claude/worktrees/`), and the owner answered P6 (a) on 2026-10-01. S7 and S8 hold for the text reading's shapes only, as in 0.16.0 |
| What steps around a hook in one command | spec §*The convergence argument*: "`core.hooksPath` pointing elsewhere, a stub deleted or made non-executable (the installer re-checks at every session start and every Bash call …)" / the installer cannot see a setting that lives in one command | the reading does not stand aside for one | Round 1's 🟡 2 and 🟡 8: `-c core.hooksPath`, `GIT_CONFIG_*` and `env -i` commits landed judged by nobody. On the owner's direction the commit reading treats those words, and a command that does not split, as a reason to judge (`hooks/tokens.py#steps_around_hooks`). Stubs removed inside the call stay a known limit in the policy |
| The convergence argument | spec §*The convergence argument*: no shell construct "can route a commit, a switch or a creation around the decision" / claimed for commits alone | commits alone | M1 for a switch, round 1 and P6 for a creation; both arms keep `86256492`'s reading. The policy's statement and the changelog fragment say the same |
| The installer's say-once channel | `plan.md` phase 2: "said once through the dispatcher's failure channel" / its own `systemMessage` and a once-per-session marker | its own | A foreign slot is not a gate failing, and the failure channel is drawn only at `Stop`; `dispatch.merge` now keeps a `systemMessage` beside a decision instead |
| Where the answer tokens live | `spec.md` §*Data & interfaces*: "`<common-dir>/specseal-answer/<session>/<token>`" / `~/.claude/specseal/answers/<session>/` | the plugin's own state directory | A command can act on a clone its text does not name, and finding which one is the reading this work removes; the directory is where the version check already keeps its state |
| Phase 5's switch work | `plan.md` phase 5: the switch at git, `shared-tree-ok` and `carry-changes` answers, the guard's Bash walk deleted / none of it | none | The owner's option 1 keeps the switch arm where 0.16.0 had it |
| The byte pin's module | `plan.md` phase 5: `test_the_guard_reads_the_same_answer` retargeted to bytes / kept, and a new `tests/test_the_frozen_reading_never_grows.py` | both | The existing case still asserts a true and wanted answer of the frozen reader |
| S2's modules | `plan.md` phase 3: retarget the three corpus modules to real commits / kept as the fallback's tests, and S2 replays their corpora against real git in the new module | both | Under P5 the PreToolUse reading still judges a foreign clone, so its tests stay true |

## Not verified

| Item | Who must answer |
|---|---|
| The suite, repository-wide lint and typecheck — none of the three was run (§2); every module this branch touched, and 41 that read the gate, the notice or the dispatcher, were | the orchestrator, through the sealer |
| The stubs under a real Claude Code session: hooks run from the installed plugin copy, which is 0.16.0 and carries no installer, so nothing in this branch has run as the harness runs it | the orchestrator, at the first session on a release carrying it |
| M4: the harness version that first exports `CLAUDE_CODE_SESSION_ID`, `CLAUDECODE` and `CLAUDE_PID`, and what `CLAUDE_CODE_SESSION_ATTENDED` reads in a headless run | the orchestrator |
| M5: whether an `isolation: "worktree"` spawn runs `git worktree add`; no git hook judges a creation since P6, so the answer moves nothing here | the orchestrator — it needs an `Agent` spawn, which contract §6 withholds from `smith` |
| ✅ M6: stops lost and added per candidate over the corpora | executed 2026-10-01 after the owner's answer, `phases/phase-1.md` §*Resumed* |
| M9: the stubs and the real-git modules on Windows | the CI Windows leg |
| Which git CI's `ubuntu-latest` runner carries | the orchestrator, from a CI log |
| Where the recorded run's "at least 3 denies" were recorded, given 0 in the `permissionDecision` records | the orchestrator |

## Not done

The text readers were not deleted, because P1's answer keeps a foreign-slot
clone on 0.16.0's behaviour (`questions.md` P5 holds the trade for the owner).
None of phase 5's switch work was built, on the owner's option 1. No global
`init.templateDir` or `core.hooksPath` is written, so a clone no session has
reached carries no stubs, as the spec's out-of-scope row says. #678 and #686
are answered for commits in the policy and stay open for the switch and
creation arms, which still read the command; nothing was posted to either
issue, because posting is the orchestrator's.

## Fed back into the spec

- *Inferred during implementation:* the backstop's criterion is
  `GIT_AUTHOR_DATE` (M12), and its mark is keyed by the old HEAD, the tree and
  that date. *Corrected in round 1's fix pass:* the mark is keyed by the
  `git commit` process too (🟡 10), and neither hook judges the commit git
  makes for its own sequencer — a sequencer state on disk and a `git commit`
  started by `git`, measured on four gits (🟡 7).
- *Withdrawn in the round-1 fix pass (P6):* the creation ladder deciding in
  `post-checkout`, and a worktree under `.claude/worktrees/` never being taken
  back. Both went with `hooks/creationgate.py`.
- These live in the two policy documents' new statements rather than in
  `spec.md`, which is the framer's.
