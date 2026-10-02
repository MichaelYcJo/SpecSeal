# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — review round 4

| Field | Value |
|---|---|
| Target SHA | ac7da148f3d1a5aefbfbe7c507d5b5c71a88ea03 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 705 |
| Broad gate | aaf47348 against e4399b65; earlier run: 2ac372ec against e4399b65 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 4 is the run's last record: a verifying round at `ac7da148` over round 3's fix range `b34b5401..a4692a0b`. That range carries the owner's P7 change, under which the text reading stands aside only for a command `is_plain` accepts. It was asked three things. First, whether round 3's shapes are now judged where 0.16.0 judged them. Second, whether any command `is_plain` accepts can still keep git's hooks from running, checked across each allowlisted program, git subcommand and config key. Third, whether any command 0.16.0 let through is now refused. It also took the depth-1 units round 3 added as a finding surface.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 3's 🟡 1 is closed — a string a shell parses again | `hooks/tokens.py#is_plain` | confirmed | `is_plain` is false for every re-parsing shape, not only the listed ones: `sh`/`bash` are not in `PLAIN_PROGRAMS`, `eval` is not, `substitution_bodies` rejects a `$( )` or backtick body, and the bare-text scan rejects `( )` and `{ }`. Executed: the five 🟡 1 shapes each `plain=0`; the module's `test_a_command_that_can_step_around_the_hooks_keeps_the_text_reading` denies each through the gate |
| 🟢 | round 3's 🟡 2 is closed — the environment emptied, `exec -c` | `hooks/tokens.py#is_plain`, `PLAIN_PROGRAMS` | confirmed | `env` and `exec` are not in `PLAIN_PROGRAMS`, so every `env …` and `exec …` commit is non-plain and judged — wider than enumerating `env`'s options. Executed: `env -v -i`, `env -u FOO -i`, `env -vuCLAUDECODE`, `env -S'…'`, `(exec -c …)` each `plain=0`; the module table denies each |
| 🟢 | round 3's ⬜ 4 is closed — the conflicted-merge sentence has a case | `tests/test_the_commit_gate_decides_at_the_commit.py#test_concluding_a_conflicted_merge_is_judged` | confirmed | the case exists and is among the 265 that pass at the target; the ledger's G16 records it was seen red with `_sequencer_commit` answering true for every commit (read, not re-executed here) |
| 🟢 | the rule cannot be stood aside for a hook-bypassing command — the class is closed | `hooks/tokens.py#is_plain` | confirmed | `is_plain` runs `steps_around_hooks` first and returns false on any hit, so `is_plain` true implies `steps_around_hooks` false, and the stand-aside set strictly shrank vs 0.16.0. A bypass needs config (`-c` key rejected unless in `PLAIN_CONFIG`), an env assignment (rejected — no assignment in a program's place), `env`/`exec` (not allowlisted), removing the stubs (`rm`/`chmod` not allowlisted), a write to a hook file (output only to `/dev/null` or a descriptor), or `--no-verify` (met at `reference-transaction`). Executed: a 46-command battery, zero `is_plain ∧ steps_around_hooks` |
| 🟢 | the cost lands as P7 intended and nothing regresses in the dangerous direction | `hooks/commit-review-gate.py#main` | confirmed | `around = not is_plain`; when `around` is true the reading judges through 0.16.0's own `judge`/`git_decides`/`commit_targets` path, whose verdict turns on review state, not on how `around` became true. The default `$(…)` message shape is `plain=0` (executed) and is judged as 0.16.0's reading judged it; no command 0.16.0 let through is newly refused except a misread, which fails closed and costs one refusal (owner-accepted, P7) |
| 🟢 | the new units are correct | `hooks/tokens.py#is_plain`, `PLAIN_PROGRAMS`, `PLAIN_GIT`, `PLAIN_CONFIG` | confirmed | the three constants hold only read-only filters, no-ops, `git`, and hook-safe git subcommands and config keys (`commit.gpgsign` runs gpg but the hooks still run; `specseal.waive`/`specseal.answer` are the sanctioned waiver). Executed: `STILL_PLAIN` all `plain=1`, `NO_LONGER_PLAIN` all `plain=0`, matching the module's two negative tests |
| 🟢 | the module the fixes touched passes at the target | `tests/test_the_commit_gate_decides_at_the_commit.py` | confirmed | executed: 265 passed, 62 skipped, exit 0 |
| 🟢 | the ledger holds unscoped at the target | `seal/` | confirmed | executed: `bin/evidence-check .` exit 0; total 3501 ok, 0 drifted, 0 broken, 0 malformed |
| 🟢 | the fix range's records are true — G8 corrected, G16 added, survivors and changelog re-stated | `seal/ledger/1790815613-…​.md`, `seal/specs/1790815613-…/survivors.md`, `…/changelog.md`, `…/questions.md` (P7), `docs/commit-review-gate-spec.md`, `skills/agent-contract/SKILL.md` | confirmed | read: P7 records the owner's answer; G8 carries the 2026-10-02 correction and G16 is added with coordinates `evidence-check` resolves; the agent-contract §9 and the policy paragraph describe the flipped condition; the release rows carry dated `Re-read`/`Corrected` notes rather than overwrites |
| ⬜ | a test pinning that a now-judged command still lands in a declared worktree would make the "nothing regresses" claim executable | `tests/test_the_commit_gate_decides_at_the_commit.py#test_a_plain_agent_commit_stands_aside_and_one_word_more_is_judged` | confirmed | the boundary test checks the non-plain form only against the undeclared main checkout (`deny`); a sibling assertion that the same non-plain form is `silent` at the declared worktree (`world.w`) would pin the regression-cost direction directly. Reasoned sound here from the `judge` path; not a defect, and `Needs a fix` does not count it |
| ⬜ | the two #716 spellings | `hooks/cmdline.py#_git_options` | deferred #716 | already deferred in round 3; carried. Under P7 both are non-plain (`git --config-env core.hooksPath=…` hits `steps_around_hooks`; `env -S '…'` is outside the allowlist), so the stand-aside no longer reaches them, but whether the reading places them end to end is the #716 placement question, unchanged. The owner answers it |
| ❓ | whether a `systemMessage` from the installer reaches the model or only the person | `hooks/hook-install.py#main` | ❓ out of verified scope | carried from rounds 1–3; nothing here ran the harness's renderer; the orchestrator answers it |
| ❓ | whether a command typed with `!` is "a person's own commit" under P2 | `hooks/githooks.py#_P2` | ❓ out of verified scope | carried from rounds 1–3; the owner answers it |
| ❓ | M4's version floor and M5 | `overview.md` §*Not verified* | ❓ out of verified scope | carried from rounds 1–3; this round ran no git below the floor; the orchestrator answers it |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_commit_gate_decides_at_the_commit.py -q` in the round's clone at the target | 265 passed, 62 skipped, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone at the target | exit 0; total 3501 ok, 0 drifted, 0 broken, 0 external, 0 malformed |
| a 46-command battery through `tokens.is_plain` and `tokens.steps_around_hooks` in the clone: round 3's 🟡 1 and 🟡 2 shapes, the stub-removal and `--no-verify` shapes, config/env-bypass shapes, and attempts to find a plain command that runs another program, writes a file, sets git config or empties the environment | every bypass shape `plain=0`; zero commands with `is_plain ∧ steps_around_hooks`; `grep -f`, `cat` reading a file/FIFO, `printf` with no option, `cat < f`, `git -C`, `git -c commit.gpgsign`, and quoted heredoc message shapes stay plain; `git -c diff.external`, `git -c core.pager`, `git … --output`, `git <alias>`, `printf -v`, and every `env`/`exec`/`sh -c`/`eval`/`$( )`/`( )`/`{ }` shape are non-plain |
| the two #716 spellings and the default `git commit -m "$(cat <<'EOF' … EOF)"` shape through `is_plain` | both #716 spellings `plain=0`; the default message shape `plain=0` (judged as before); a quoted-heredoc `-F -` message shape `plain=1` |
| a `test_tmp_*` probe asserting a now-judged command is silent at the declared worktree and judged at the undeclared one, via the module's `pre_bash` | not conclusive — the standalone file could not pull the module's autouse fixtures, so `world` setup failed before the assertions ran; the claim is carried as reasoned from the `judge` path, not executed. Probe file removed; clone status clean |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — none of the three was run here; it is the sealer's, and with nothing open it comes due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/creationgate.py:118-126`, `:161-169`, `:271-281` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/commit-review-gate.py:1344-1347`, `docs/commit-review-gate-spec.md:144-161` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/hook-install.py:116-122`, `hooks/githooks.py:237-241` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/worktree-guard.py:1629`, `docs/worktree-guard-spec.md:386` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/creationgate.py:109-115`, `:271-277` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/creationgate.py:125`, `:155-156` | round 1's 🟡 6 — fixed |
| round-1 | `hooks/commitgate.py:179-199`, `hooks/githooks.py:37-42`, `docs/commit-review-gate-spec.md:106-118` | round 1's 🟡 7 — fixed |
| round-1 | `hooks/hooksession.py:102-111`, `hooks/githooks.py:109-118` | round 1's 🟡 8 — fixed |
| round-1 | `hooks/answers.py:76-109`, `hooks/answer-write.py:28` | round 1's 🟡 9 — fixed |
| round-1 | `hooks/commitgate.py:77-79`, `:107-118` | round 1's 🟡 10 — fixed |
| round-1 | `hooks/githooks.py:109-118`, `docs/commit-review-gate-spec.md:156-159` | round 1's 🟡 11 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:241`, `:345` | round 1's ⬜ 12 — fixed |
| round-1 | `hooks/hook-install.py:145-181` | round 1's ⬜ 13 — fixed |
| round-1 | `hooks/cmdline_base.py`, `hooks/worktree-guard.py:1629` | round 1's 🟢 — confirmed |
| round-1 | `seal/` | round 1's 🟢 — confirmed |
| round-1 | `hooks/commitgate.py:129-199` | round 1's 🟢 — confirmed |
| round-1 | `hooks/hooksession.py:102-111` | round 1's 🟢 — confirmed |
| round-1 | `hooks/hook-install.py:184-195` | round 1's ❓ — out of verified scope |
| round-1 | `hooks/githooks.py:109-118` | round 1's ❓ — out of verified scope |
| round-1 | `overview.md` §*Not verified* | round 1's ❓ — out of verified scope |
| round-2 | `hooks/tokens.py:55-87` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/tokens.py:63-87`, `docs/commit-review-gate-spec.md:189-194` | round 2's 🟡 2 — fixed |
| round-2 | `docs/commit-review-gate-spec.md:216-217`, `hooks/answers.py:147-181` | round 2's ⬜ 3 — fixed |
| round-2 | `docs/commit-review-gate-spec.md:218-226` | round 2's ⬜ 4 — fixed |
| round-2 | `docs/commit-review-gate-spec.md:112-143` | round 2's ⬜ 5 — fixed |
| round-2 | `hooks/worktree-guard.py`, `docs/worktree-guard-spec.md:376-398` | round 2's 🟢 — confirmed |
| round-2 | `hooks/tokens.py#steps_around_hooks`, `docs/commit-review-gate-spec.md:189-194` | round 2's 🟢 — confirmed |
| round-2 | `hooks/hook-install.py#write_stubs`, `hooks/githooks.py#decides` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py`, `hooks/worktree_consent.py` | round 2's 🟢 — confirmed |
| round-2 | `hooks/commitgate.py#_sequencer_commit` | round 2's 🟢 — confirmed |
| round-2 | `hooks/tokens.py#steps_around_hooks` | round 2's 🟢 — confirmed |
| round-2 | `hooks/answers.py#given`, `hooks/hooksession.py#call_args` | round 2's 🟢 — confirmed |
| round-2 | `hooks/commitgate.py#_key` | round 2's 🟢 — confirmed |
| round-2 | `hooks/githooks.py:117-126` | round 2's 🟢 — confirmed |
| round-2 | `skills/agent-contract/SKILL.md:241-251`, `:349-357` | round 2's 🟢 — confirmed |
| round-2 | `docs/commit-review-gate-spec.md:228-233` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline_base.py:1-22` | round 2's 🟢 — confirmed |
| round-2 | `tests/` | round 2's 🟢 — confirmed |
| round-2 | `hooks/hook-install.py#main` | round 2's ❓ — out of verified scope |
| round-3 | `hooks/tokens.py#_empties_the_environment` | round 3's 🟡 2 — fixed |
| round-3 | `hooks/cmdline.py#_git_options` | round 3's ⬜ 3 — deferred |
| round-3 | `docs/commit-review-gate-spec.md` §*A commit git makes for its own rebase, cherry-pick or revert* | round 3's ⬜ 4 — fixed |
| round-3 | `hooks/tokens.py#steps_around_hooks`, `docs/commit-review-gate-spec.md` | round 3's 🟢 — confirmed |
| round-3 | `docs/commit-review-gate-spec.md`, `hooks/answers.py#_squash` | round 3's 🟢 — confirmed |
| round-3 | `docs/commit-review-gate-spec.md`, `hooks/githooks.py#_NARROW` | round 3's 🟢 — confirmed |
| round-3 | `docs/commit-review-gate-spec.md` | round 3's 🟢 — confirmed |
| round-3 | `skills/verify/` | round 3's 🟢 — confirmed |
| round-3 | `tests/test_the_commit_gate_decides_at_the_commit.py` | round 3's 🟢 — confirmed |
| round-3 | `hooks/githooks.py#_P2` | round 3's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the two #716 spellings (`git --config-env core.hooksPath=…` with a space, `env -S '-i git commit'`) | #716 (already deferred in round 3) | the owner |
