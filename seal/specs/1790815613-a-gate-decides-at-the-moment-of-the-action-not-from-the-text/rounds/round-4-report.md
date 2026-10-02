# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — review round 4

| Field | Value |
|---|---|
| Target SHA | ac7da148f3d1a5aefbfbe7c507d5b5c71a88ea03 |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 705 |
| Fix range | `b34b5401225b3196c9ab4e7dca5bcb848c0acc6b..a4692a0b9e086248c0054b2b661edd840ad0ef5a`, 6 commits |
| Needs a fix | no |
| Loses a record or crashes | no |

## What this round was asked

Round 4 verifies round 3's fix range. Round 3 recorded two open findings, both
`fixed` by one change: on the owner's answer `questions.md` P7 (2026-10-02) the
condition was flipped. Before P7 the PreToolUse commit reading stood aside for
every command but one carrying a word on a list of hook-bypass spellings;
after P7 it stands aside only for a command whose shape `hooks/tokens.py#is_plain`
calls plain, and judges everything else with 0.16.0's reading.

The job was, for each `fixed` verdict, whether the finding and its class are
closed; whether any command `is_plain` accepts can keep git's hooks from
running (the only way the class stays open under the new rule); and whether the
cost lands where the owner intended, with no command 0.16.0 let through now
refused.

This is the run's last round: round 3 spent the one reopening, and the
generator caps the run here. The open items below are carried for the
orchestrator to defer, not reopened.

## What I found

Round 3's two findings are closed, and their classes are closed by a stronger
mechanism than the list that preceded them. The direction of the new rule is
sound: `is_plain` returning true forces `steps_around_hooks` to be false first,
so the set of commands the reading stands aside for strictly shrank against
0.16.0 — no command newly stands aside, which is the only direction that could
ship an unjudged commit. I examined each allowlisted program, each git
subcommand, each config key, the redirection handling and the re-parsing
guards, and could not construct a plain command that keeps git's installed
hooks from running.

The cost the owner chose in P7 is real and bounded. A command 0.16.0 left to
git — the default `git commit -m "$(cat <<'EOF' … EOF)"` message shape among
them — is no longer plain, so the reading judges it. In a clone where the
reading can place the commit, its verdict turns on the review state, which is
what 0.16.0's git hooks turned on too, so a declared worktree still lands and
an undeclared checkout is still refused; only the stage and the wording of the
refusal move earlier. A command the reading cannot place costs one refusal
that fails closed and is recoverable through the waiver — the P7 trade,
written into the policy as "a misread costs the one judgment 0.16.0 made".

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

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_commit_gate_decides_at_the_commit.py -q` in the round's clone at the target | 265 passed, 62 skipped, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone at the target | exit 0; total 3501 ok, 0 drifted, 0 broken, 0 external, 0 malformed |
| a 46-command battery through `tokens.is_plain` and `tokens.steps_around_hooks` in the clone: round 3's 🟡 1 and 🟡 2 shapes, the stub-removal and `--no-verify` shapes, config/env-bypass shapes, and attempts to find a plain command that runs another program, writes a file, sets git config or empties the environment | every bypass shape `plain=0`; zero commands with `is_plain ∧ steps_around_hooks`; `grep -f`, `cat` reading a file/FIFO, `printf` with no option, `cat < f`, `git -C`, `git -c commit.gpgsign`, and quoted heredoc message shapes stay plain; `git -c diff.external`, `git -c core.pager`, `git … --output`, `git <alias>`, `printf -v`, and every `env`/`exec`/`sh -c`/`eval`/`$( )`/`( )`/`{ }` shape are non-plain |
| the two #716 spellings and the default `git commit -m "$(cat <<'EOF' … EOF)"` shape through `is_plain` | both #716 spellings `plain=0`; the default message shape `plain=0` (judged as before); a quoted-heredoc `-F -` message shape `plain=1` |
| a `test_tmp_*` probe asserting a now-judged command is silent at the declared worktree and judged at the undeclared one, via the module's `pre_bash` | not conclusive — the standalone file could not pull the module's autouse fixtures, so `world` setup failed before the assertions ran; the claim is carried as reasoned from the `judge` path, not executed. Probe file removed; clone status clean |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — none of the three was run here; it is the sealer's, and with nothing open it comes due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the two #716 spellings (`git --config-env core.hooksPath=…` with a space, `env -S '-i git commit'`) | #716 (already deferred in round 3) | the owner |

Needs a fix: no

Loses a record or crashes: no

## Proof

Files opened in the clone at `ac7da148`:
- `hooks/tokens.py`, `hooks/commit-review-gate.py`, `hooks/githooks.py`, `hooks/cmdline.py`
- `docs/commit-review-gate-spec.md`
- `skills/agent-contract/SKILL.md`
- `tests/test_the_commit_gate_decides_at_the_commit.py`
- `seal/ledger/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text.md`
- `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/`: `survivors.md`, `changelog.md`, `questions.md`, `overview.md`
- `seal/releases/0.16.0.md`
- round records `rounds/round-3.md`

Executed: `bin/test` on the gate module (265 passed), `bin/evidence-check .`
(exit 0), the `is_plain`/`steps_around_hooks` battery, and a removed
`test_tmp_*` probe. Read, not executed: the ledger's red-seen and mutant-kill
claims; the declared-worktree-lands direction (reasoned from the `judge` path).
