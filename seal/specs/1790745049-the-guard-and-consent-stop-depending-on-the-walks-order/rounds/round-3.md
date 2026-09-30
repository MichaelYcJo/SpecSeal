# 1790745049-the-guard-and-consent-stop-depending-on-the-walks-order — review round 3

| Field | Value |
|---|---|
| Target SHA | 28199afc8e26c6c71fe86e45d68832af85d20a97 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 691 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 reopened the run once. It targets `28199afc` over round 2's fix range `00ed11be..9f5261c5`. It was asked two things:
1. Whether round 2's five verdicts are closed: the policy line naming the next release, the §*Creation consent* reference, `foreach` in the cost lists, S6 parameterised per module, and the stale import comments.
2. Whether the fix pass's in-place corrections to two unshipped specs and I9 are true.

It also re-confirmed three things narrowly: the frozen copy's byte identity, the gate files' identity to `542f920b`, and a sample of the guard's and consent's decisions against `86256492`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's blocking finding is closed — the policy names no release, and the hygiene case passes | `docs/worktree-guard-spec.md#"### Which tree, when the command walks to it"` | confirmed | Executed: `tests/test_release_hygiene.py` in a 23-module run, exit 0; `git grep` over the loaded roots finds no `0.16`–`0.19` version |
| 🟢 | round 2's ⬜ 2 is closed — the cost paragraph cites §*Creation consent*, which holds the command-word groups | `docs/worktree-guard-spec.md:583` | confirmed | Read: the groups at line 262 sit under the heading at line 88 |
| 🟢 | round 2's ⬜ 3 is closed — the five cost lists name `foreach`, and its `ZSH_PREFIXED` row pins it | `tests/test_guard_resolves_the_tree_it_judges.py#ZSH_PREFIXED` | confirmed | Executed: the five rows red at `542f920b`'s hooks, green at `86256492`'s and the target's; zsh 5.9 ran the shape |
| 🟢 | round 2's ⬜ 4 is closed — S6 is parametrised per reader, and each row is red under a mutant of its own | `tests/test_a_gate_that_fails_says_so.py#test_a_broken_shared_module_names_every_gate_that_imports_it` | confirmed | Executed: seven mutants on a copied `hooks/`; see the table in the findings |
| 🟢 | round 2's ⬜ 5 is closed — the four test sentences name the reader each module imports | `tests/test_what_the_reader_understands.py#test_the_guard_reads_the_same_answer` | confirmed | Read against `hooks/worktree-guard.py:130` |
| 🟢 | The corrections to 1790635415's S6 and fact table and to 1790660768's grounding and §*What the worktree guard sees* are true | `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/spec.md` | confirmed | Read the import lines of `hooks/`; executed through the S6 mutants and the differential |
| 🟢 | I9's re-read is true — the section's only change in the fix range is the `foreach` word | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` | confirmed | Read the fix range's diff; `bin/evidence-check` 0 drifted, 0 broken |
| 🟢 | The frozen copy equals `86256492:hooks/cmdline.py` below its rider | `hooks/cmdline_base.py` | confirmed | Executed, byte comparison |
| 🟢 | The commit gate's two files equal `542f920b` | `hooks/commit-review-gate.py` | confirmed | Executed: empty diff |
| 🟢 | The guard's and the consent writer's answers equal `86256492`'s | `hooks/worktree-guard.py#main` | confirmed | Executed: 0 of 784 commands differ; the same probe finds 317 at `542f920b` |
| ⬜ 1 | The commit gate's comment says both gates import `hooks/cmdline.py`, and the rider that marks frozen comments as `542f920b`'s names only `cmdline.py`'s | `hooks/commit-review-gate.py:93` | deferred #692 | Read; the class of round 2's ⬜ 5; no behaviour depends on it |
| ⬜ 2 | The gate's policy lists zsh's words without `foreach`, which `hooks/cmdline.py` reads as it reads `for` | `docs/commit-review-gate-spec.md:392` | deferred #692 | Read; present at `542f920b`, from work item 1790660768; incomplete, not false |
| ❓ | The guard's Windows backslash doubling on a Windows machine | `hooks/worktree-guard.py#_tokenize_with_separators` | ❓ out of verified scope | Carried from rounds 1 and 2; the repository owner answers it on a Windows machine |

## Paste-ready fixes

```text
# Comments in `cmdline.py` that name the guard or the consent writer as its
# readers describe `542f920b`, and so does the comment above the commit gate's
# imports that says both gates import `cmdline.py`; #692 reconciles them.
```
```text
- **zsh's precommand words and short loops** — `noglob`, `nocorrect`, `repeat
  N`, `for i (…) cmd` and `foreach i (…) cmd; end` — are read past as runners,
  the count and the word list as operands.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over 23 modules: release hygiene, the record modules (generated, floor and depth, reviewer's report, fixes close, last round's fixes, reopening), the document checks (evidence, content anchors, line wrap, no real identifiers, one word, survivors, merge corrections, old roots, rule owners, riders) and the six test modules the fix range touched | 1986 passed, 1 skipped, exit 0 |
| `bin/evidence-check` | exit 0; every ledger file 0 drifted, 0 broken; the work item's fragment 14 ok |
| `bin/correction-check --range 542f920b...28199afc` | no merge commit in the range, exit 0 |
| `bin/survivor-check --range 00ed11be..9f5261c5 --exempt` the work item's `survivors.md` | exit 0; one survivor, excused |
| The frozen copy against `git show 86256492:hooks/cmdline.py`, as bytes | Equal: the shebang plus lines 20 onward |
| `git diff 542f920b 28199afc -- hooks/cmdline.py hooks/commit-review-gate.py` | 0 bytes |
| A deleted differential over 784 generated commands, each hook set in its own process | Target against `86256492`: 0 differences, 0 exceptions. `542f920b` against `86256492`: 317 differences |
| The five `ZSH_PREFIXED` rows at `542f920b`'s and at `86256492`'s hooks | 5 failed, exit 1; 5 passed |
| A deleted probe replaying S6's three rows under seven import mutants | Each row red under at least one mutant of its own |
| `zsh -f -c 'foreach i (1) echo ran-$i; end'` | `ran-1`, exit 0 |
| Broad gate: full suite, repository-wide lint and typecheck | not yet — nothing has run it on this branch. With nothing open that needs a fix, it comes due now, through the sealer's spawn |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:2086`, `hooks/worktree_consent.py:437` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/cmdline.py:2617` | round 1's 🟡 2 — fixed |
| round-1 | `docs/worktree-guard-spec.md:559` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/changelog.md:20` | round 1's ⬜ 4 — answered |
| round-1 | `hooks/cmdline.py#walk_directories` | round 1's 🟢 — confirmed |
| round-1 | `hooks/` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/cmdline.py#base_directories` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py#_tokenize_with_separators` | round 1's ❓ — out of verified scope |
| round-2 | `docs/worktree-guard-spec.md:585` | round 2's 🔴 1 — fixed |
| round-2 | `docs/worktree-guard-spec.md:582` | round 2's ⬜ 2 — answered |
| round-2 | `docs/worktree-guard-spec.md:581` | round 2's ⬜ 3 — answered |
| round-2 | `tests/test_a_gate_that_fails_says_so.py:302` | round 2's ⬜ 4 — fixed |
| round-2 | `tests/test_what_the_reader_understands.py:791` | round 2's ⬜ 5 — answered |
| round-2 | `hooks/worktree-guard.py#walk_command` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline_base.py#walk_directories` | round 2's 🟢 — confirmed |
| round-2 | `docs/worktree-guard-spec.md:560` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order.md` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline_base.py` | round 2's 🟢 — confirmed |
| round-2 | `hooks/dispatch.py#run_gate` | round 2's 🟢 — confirmed |
| round-2 | `hooks/commit-review-gate.py` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the guard should read zsh-prefixed and redirected segments rather than leave them to the user's settings | already deferred in round 1 to #692, the owner's redesign of how the gates learn where a command acts | the repository owner |
