# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — round 1, fix pass

Every 🔴 was reproduced before it was fixed, and none of the paste-ready fixes
was taken on reading. What the reproduction changed: it found two members of
finding 2's class the report did not name (`git switch feature/x; …` and
`git checkout feature/x && …`), a **second** silent exit with the same hole in
it (`if not top`, reached when the shell is outside any repository while a
`git -C <repo> worktree add` in the same command is not), and two checks in the
paste-ready fix that no case could pin.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `86c4ddb` — `only_creates_a_worktree` now asks two things of each SEGMENT rather than one thing of the compound: `git` is the segment's own command word, and no token carries `$`, a backtick, `<` or `>`. All eleven shapes fall to `ask`. Seen red first: `bin/test tests/test_tmp_round1_red.py` printed `allow` for every one of them, and the shell half printed `marker exists: True` and `victim holds: ''` |
| 2 | fixed | `86c4ddb` — the walk records where a creation ANYWHERE in the command acts, and the guard's two silent exits fall through to `judge_creation`. The switch ladder keeps every verdict it had; the report's paste-ready fix, which makes the creation outrank the earlier verdict, turns a switch denied under an ACTIVE session into an `ask` and was refused for that. Seen red first: `git switch feature/x && git worktree add ../wt f`, `… ; …` and `git checkout feature/x && …` were all **silent** with the record written |
| 3 | fixed | `86c4ddb` — the command-word test is the same line as finding 1's first. `sudo`, `env VAR=…`, a bare `VAR=…` and `command git …` all answer `ask`; `git -C <repo> worktree add`, `-b <branch> <start>`, a `~` path and a glob path still allow. Seen red first: all four answered `allow` |
| 4 | deferred `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md` | Whether a `permissions.deny` rule outranks a hook `allow` is a harness property and is not executable from this repository. The `Not verified` row now carries the repository owner as its answerer and says round 1 widened what rides on it; `pr-notes.md` §4 says what the guard does if the answer is the unfavourable one — the consented row answers `ask` rather than `allow`, a one-word edit at one site that costs the whole prompt budget. Two of the three shapes that made it urgent are closed either way: `sudo` and `env LD_PRELOAD=…` no longer get an allow at all (`20553cb`) |
| 5 | deferred `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md` | `pr-notes.md` §4 no longer states the auto-answered `ask` in the future tense — `--dangerously-skip-permissions` exists today, so the honest form of the claim is that the record means *the harness permitted the call*, which is what `docs/worktree-guard-spec.md` already said. The `overview.md` row closed with *the same standing every gate in this repository has*, which names nobody; it names **the repository owner** now (`20553cb`) |
| 6 | fixed | `20553cb` — the three `seal/ledger.md` rows at `:269`, `:337` and `:379` were re-read at `dispatch.py#GROUPS` and their `Checked` moved to `2026-09-08`, each with the re-read written into `Notes` in the shape the row above them uses. The branch's edit added `worktree_consent.py` to `post-bash` and a `post-agent` group beside it, and touches no group those three rows claim about, so all three claims hold |

## What was executed

| What was run | Result |
|---|---|
| `tests/test_tmp_round1_red.py` at `d82a02c` — eleven single-segment shapes with a record present | **all eleven `allow`**; the predicate answered `True` for each. Finding 1 and 3 red |
| the same probe's shell half | `git worktree add /nonexistent/x $(touch <marker>)` left the marker; `… > <victim>` left a file holding `important` holding `''` |
| the same probe, finding 2 — clean single-stream tree, no record | `git worktree add …` **deny**, `git status && …` **deny**, `git switch feature/x && …` **silent**, `git switch feature/x; …` **silent**, `git checkout feature/x && …` **silent** — and `creation_directory` resolved a repository for all five, so the writer records for each. Two of these five are not in the report |
| re-enumeration probe: the shell outside any repository, `git switch feature/x && git -C <repo> worktree add ../wt f` | guard **silent**, writer records — a **second** silent exit, at `if not top`, which the report's fix does not reach |
| the same probe after the fix | every shape non-silent; the differential over 24 command/cwd pairs found no command the writer records for that the guard is silent on |
| `bin/test` on the five guard modules after the fix | **165 passed, 1 skipped** |
| the six new cases against `HEAD:hooks/worktree-guard.py`, restored from a copy taken first | **4 failed, 2 passed** — findings 1, 3, 2 and the differential red |
| the two that passed, against the change each refuses: the report's own paste-ready fix for finding 2, and a predicate that refuses a trailing `&` | **1 failed** each — both pin a decision rather than the old defect, and both go red under the alternative |
| seven mutations of the fix, one at a time, restored from a copy each time | five turned a case red; **`cmdline.understood` and the `Unresolved` test survived**, so both were removed — a check nothing can make false is a check no case can pin, which is the rule `guard_worktree_creation` states about its own missing `session_id and`. The command-word test subsumes them and is strictly stronger: executed, `understood` answers True for `time git worktree add …` where it answers False |
| the six mutations after the removal | all six turned a case red |
| the budget, six `git worktree add ../wt f` calls in one session, clean single-stream tree | **deny, allow, allow, allow, allow, allow.** `git switch feature/x && …` and `cd /tmp && …` answer `ask` |
| `uvx ruff format --check` and `uvx ruff check` on the two files touched | `2 files already formatted`, `All checks passed!` |
| `bin/evidence-check --strict .` | `772 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, up one row |

Probes were three `test_tmp_*` files; all three are deleted and the tree is
clean. Every mutation and every revert-to-`HEAD` restored from bytes saved to a
temp file before the swap, never from git, and each printed `restored: True`;
`tests/__pycache__` was cleared between mutations.

## Not run, and who answers it

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the orchestrator's broad gate, once, after the rounds settle (`agent-contract` §2) |

## What went somewhere else

| Item | Where | Who answers it |
|---|---|---|
| `evidence-check` ignores a ledger row whose coordinate is malformed instead of naming it — found writing a row here, and outside this work item | `seal/follow-up.md` | the repository owner |
