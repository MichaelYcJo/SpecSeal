# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — overview

📋 implement applied
· spec:     CLAUDE.md §The goal a design is chosen against; docs/review-chain-spec.md §The review run has a bound … §The last round verifies; docs/review-handoff-protocol.md §round-N.md; templates/sdd-round.md; skills/code-review/SKILL.md §Orchestrator sections and §Findings format; agents/warden.md §Role, §Report; agents/smith.md :100-200; skills/implement/SKILL.md §2, §5; issue #161 body and three comments; the last item's rounds/round-4.md and round-12.md
· evidence: none yet — rows land at phase 5 in seal/ledger/1788597030-….md
· verified: executed — the inter-commit measurement over 3ef565d^..pull/162/head (70 commits, 12.8 h before docs commits, 3.6 h before fix commits, gaps capped at 2 h); read — everything above

## Why this work exists

The last branch spent 12.8 of its 18.8 active hours in front of record commits and half its findings were located in records, so the record is generated here rather than written, and the loop that reviewed the tool's own paperwork loses its habitat.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The landing value of `Fixes checked by` | Spec: *`Fixes checked by` at its landing value* — one value, `nobody — the fixes are not yet written`. Code: that value when a verdict is open or closed on a fix word; `no fixes to check` and a bare `none` in both surface rows when every verdict closed without one | code | `chain_check.py#fix_surface`: *"`no fixes to check` beside a pending row, which the TERMINAL record of every run carries. There the pair is not merely unrefused but wrong: a round that commissioned no fixes will never have any, so *not yet written* is false the moment it is written"*; and `checked_by` refuses `nobody` beside a checked `Pass` on the last record, so the spec's own scenario *A capped run has a legal end* needs `no fixes to check` written by the generator |
| How the check is told the pull request's state | Spec: *runs `chain_check --worktree` on the work item before it returns*. Code: the same, with a `draft` event payload handed to the check through `GITHUB_EVENT_PATH` unless `gh pr view --json isDraft` says the pull request is ready | code | `chain_check.py#pull_request_state`: outside a workflow the state is `unknown` and *judged as* ready, where an unchecked `Pass` is an error — every mid-run record has one, so the check the spec asks for would exit 1 on every round that found something. `phases/phase-1.md` carries the reasoning |

## Not verified

| Item | Who must answer |
|---|---|
| `gh pr view` answering for a real pull request — the `#N — url` cell and the draft/ready read. Pinned by injection only; a scratch repository has no remote | the orchestrator, at this branch's round 1, which is the generator's first real run |
| `worktree_files` and `read_record --worktree` on the Windows leg: the path is rebuilt from `/`-split parts with `os.path.join`, which is what the rest of the checker does, and no case ran there | the windows CI leg at the pull request |
| The full suite, the repository-wide lint and the typecheck after phase 1 (§2) | the orchestrator, at the broad gate |
| The three-hour target — build plus two rounds for a change under three hundred code lines. This branch is not under three hundred lines and is the item that builds the machine, so it cannot be its own reading | the next three 0.8.2 items, under the `flow-measurement` label |
| Whether one round per session holds without enforcement | the same three items |

## Not done

The verifying round as a probe re-execution script (a new field, against the moratorium); redesigning what a record carries; #145, #155, #156, #160, #163.

## Fed back into the spec

none yet
