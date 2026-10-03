# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — review round 2

| Field | Value |
|---|---|
| Target SHA | 72c8f5a46e2f352af2890f4dca10f57beb7f49b3 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 745 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `6999b001b90a09f4d11b67eb028501e6caf0eedd..e8808af1603aeeb6ff87f5f8785d756e88773fbe`, 4 commits |
| Contract changes | none |
| New units | _shapes (depth 1); _policy_text (depth 1); POLICY_RULE (depth 1); ASKABLE (depth 1); test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers (depth 1) |
| Needs a fix | yes — 🟡 5, the policy sentence in `docs/worktree-guard-spec.md` §*Which tree* that still promises silence for a detach carrying a redirection and omits three hides the guard asks about |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round. It targets `72c8f5a4` over round 1's fix range `b4bd4ea1..36ddfb75`. It was asked whether the policy sentence in `docs/worktree-guard-spec.md` §*Which tree* now states truthfully which tree-blind restores are still asked, run against round 1's positions and its generator; whether the two new cases pin it; whether the corrected N1, phase-1, changelog and phase-2 figures hold against what can be executed; and whether the ledger and survivor checks are clean.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 5 | the policy still promises silence for a detach carrying a redirection, which C asks when the detach names a commit, and its list of asked file checkouts misses `&>>` before the name, a zsh prefix and a spaced `--config-env` | `docs/worktree-guard-spec.md:628` | **fixed** `fdb342df` | fixed at fdb342df; executed: `switch --detach feature/x` and `checkout --detach feature/x` asked on 226 of 492 shapes each, and through `main()`; `&>>` 2 shapes; `noglob`, `nocorrect`, `repeat 2` and `--config-env` file checkouts asked through `main()`; at the build and at `2b1dcb1f`. Same class as round 1's yellow 1, at the half round 1 did not enumerate |
| ⬜ 6 | the changelog's first bullet promises the same detach silence, and `git checkout -q &>/dev/null` is in none of the three categories it names | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:3` | answered | corrected at `336b20fa`; executed: the detach shapes above asked at the build and at `2b1dcb1f`; bash 3.2 hands git `checkout -q`. A correction, not counted in `Needs a fix` |
| ⬜ 7 | the changelog says a string behind a prefix of `--env0-from` or `--quoting-style` is no longer read where no `env` runs it; `env --e -S '…'` still is | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:26` | answered | corrected at `074c9e69`; executed: read at the build and at `2b1dcb1f`, refused by macOS `env`; read: GNU takes `-S` as the value. A correction |
| ⬜ 8 | N1 and phase 1 say zsh runs the numbered `>&` shapes as the creation and bash refuses each; zsh runs the `-C` ones before `checkout` or `switch` as a switch, and bash 3.2 hands git `{fd}` | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | answered | corrected at `e8808af1`; executed under bash 3.2.57 and zsh 5.9 with a recording `git`; the build asks the `-C` forms as a switch. From round 1's own fence. A correction |
| 🟢 | round 1's yellow 1 is closed for what it named: the five positions are named and asked, and a restore of `.` or a path after `--` is silent | `docs/worktree-guard-spec.md:628` | confirmed | executed: 0 of 388 generated shapes at a named position silent; `checkout .`, `checkout -- README.md` and `checkout feature/x -- README.md` asked on 0 shapes; the residual is finding 5 |
| 🟢 | the two new cases and `HIDDEN_FILE_CHECKOUTS` are correct and were seen red as their docstrings say | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | executed: the mutant `switch_kind` turns 4 of 4 red; the policy assertions fail 3 of 4 against `b4bd4ea1`'s doc; 12 passed at `72c8f5a4` |
| 🟢 | round 1's white 2 is closed: N1 and phase 1 now name the numbered `>&` with a file, which bash refuses and zsh runs | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | confirmed | executed: build against `2b1dcb1f` adds 50 of 380 shapes, drops 0; `2>&` and `3>&` refused by bash 3.2 and run by zsh; the residual wording is finding 8 |
| 🟢 | round 1's white 3 is closed: "never less" is gone from the changelog | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:24` | confirmed | executed: `env --quoti --spl '…'` dropped at the build, refused by macOS `env`; `env -i-S`, `env ---S`, `env --unset -iS` gained and run by macOS `env`; the residual is finding 7 |
| 🟢 | round 1's white 4 is closed: phase 2 says `genv`'s walk reads the two new rows and the shared `-` letter | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/phases/phase-2.md` | confirmed | executed: `genv -i-S` gained and `genv --quoti --spl` dropped against `2b1dcb1f`; read: GNU's `shortopts` carry no `-`; the counts are round 1's, carried |
| 🟢 | K7 and M2 re-read and re-stamped; the ledger reads clean and the survivors are excused | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K7 | confirmed | executed: `evidence-check --strict .` exit 0, 4,049 ok, 0 drifted, 0 broken, 0 names refused; `survivor-check` exit 0, two excused; read: both notes against the diff |
| ❓ | carried from round 1: whether 0.18.0 ships the tree-blind questions `233f0455` never asked (`questions.md` D6) | `questions.md` D6 | ❓ out of verified scope | a decision, not a check; nothing in the fix range changes it. Who answers it: the repository owner |

## Paste-ready fixes

```
redirection's word is never read as a branch name, and a restore of `.` or of
a path after `--`, or a detach that names no commit, that carries one (`git
checkout . &>/dev/null`, `git switch --detach>/dev/null`) is not asked about
(#737). A detach that names a commit moves the tree as a switch does, and is
asked as one (`2>/dev/null git switch --detach feature/x`). The reading still
looks up no tree (#689), so a file's name reads as a branch's: a checkout of a
file is asked as a switch wherever a redirection hides `checkout` from the
frozen reader, in front of `git`, between `git` and `checkout`, glued to
either, or as an `&>` or `&>>` before the name (`2>/dev/null git checkout
README.md`, `git checkout>/dev/null README.md`, `git checkout &>/dev/null
README.md`), and wherever a zsh prefix hides `git` or a spaced
`--config-env` hides `checkout` (`noglob git checkout README.md`), as it has
been since #678. Measured before it was wired: over the 27,351 distinct
command and directory pairs recorded in this
```
```
- The worktree guard no longer asks "This command switches a branch" about a
  restore of `.` or of a path after `--`, a checkout naming nothing, or a
  detach naming no commit, that carries a redirection, such as
  `git checkout . &>/dev/null`, `git checkout -q &>/dev/null` or
  `git switch --detach>/dev/null` (#737). The question added for #678 read
  the redirection's word as a branch name. It now reads each command as git
  is handed it, with every redirection taken off. It still reads no tree, so
  a checkout of a file whose `checkout` a redirection hides from the guard's
  own reading (`git checkout &>/dev/null README.md`) is still asked, as it
  was before this change. A detach that names a commit moves the tree and is
  asked as a switch (`2>/dev/null git switch --detach feature/x`). It now
  also asks about a
```
```
  runs. A prefix of `--env0-from` or `--quoting-style` now takes the next
  word as its value, as GNU reads it, so an abbreviated split string behind
  one (`env --quoti --spl '…'`) is no longer read where no `env` runs it.
  `-S` and `--split-string` spelt in full are still read wherever they
  stand, as before. `genv` is read as GNU's alone.
```
```
which bash runs nothing for (it refuses a numbered `>&` as an ambiguous redirect, and bash 3.2, which has no `{fd}`, hands git `{fd}` as a word git refuses) and zsh runs as the creation, or as the switch before `-C`'s value with `checkout` or `switch` (warden rounds 1 and 2)
```
```
which bash runs nothing for and zsh 5.9 runs as the creation or, behind `-C`, the switch
```
```
bash runs nothing: 3.2 and 5.2 refuse a numbered `>&` with a file as an
ambiguous redirect, and 3.2, which has no `{fd}`, hands git `{fd}` as a word
git refuses. zsh 5.9 runs each, as the creation, or as the switch where
`checkout` or `switch` follows `-C`'s value.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q -k` over the two new cases and three neighbours | 12 passed |
| `bin/evidence-check --strict .` in the clone at `72c8f5a4` | exit 0; 4,049 ok, 0 drifted, 0 broken; records: 5 work items, 1,285 names read, 0 refused |
| `bin/survivor-check --range 2b1dcb1f...HEAD --exempt …/survivors.md` | exit 0; 677 files, 42 removed sentences, two survivors excused |
| function level: the case module's `_redirections()` generator at every position, glued and spaced, over `git checkout README.md` and eight more verbs | `checkout README.md` 212 of 388 asked, every named position asked, 2 asked outside (`&>>` before the name); `switch --detach feature/x` and `checkout --detach feature/x` 226 of 492 each; `checkout feature/x README.md` 212 of 492; bare `--detach`, `-q`, `.`, `-- README.md`, `feature/x -- README.md` 0 each |
| `main()` through the case module's harness, a dirty `w` under a clean session, ten commands | ask: `checkout &>` and `&>>` before a file, `2>/dev/null git switch --detach feature/x`, `noglob` and `--config-env` file checkouts; silent: `checkout 2>/dev/null README.md`, `checkout -q &>/dev/null`, `checkout . &>/dev/null`, plain `checkout README.md` |
| the red claims: a mutant `switch_kind` skipping a name holding `.`; the policy case's assertions against `b4bd4ea1`'s doc | 4 of 4 red; 3 of 4 assertions fail |
| numbered and bare `>&` with a file, 380 shapes over seven verbs, build against `2b1dcb1f`; added shapes run under `/bin/bash` 3.2.57 and zsh 5.9 with a `git` that records its argv to a file | 50 added, 0 dropped; `2>&` and `3>&`: bash ambiguous redirect, zsh runs; `{fd}>&`: bash 3.2 hands git `{fd}`, zsh runs; `1>&` and `>&`: both run; `-C` forms before `checkout` or `switch` run as a switch under zsh |
| env: 16 shapes through `reparsed_texts` at the build and at `2b1dcb1f`, the `env` ones run by macOS `/usr/bin/env` | `env --quoti --spl` dropped and refused; `env --e -S` and `env --quoti x -S` read at both, refused; `env -i-S`, `env ---S`, `env --unset -iS` gained and run; `genv -i-S` gained, `genv --quoti --spl` dropped |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet: not run by this round; the sealer's, once the rounds settle (contract §2) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/worktree-guard-spec.md:627` | round 1's 🟡 1 — fixed |
| round-1 | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | round 1's ⬜ 2 — answered |
| round-1 | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md` | round 1's ⬜ 3 — answered |
| round-1 | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/phases/phase-2.md` | round 1's ⬜ 4 — answered |
| round-1 | `hooks/worktree-guard.py#_bare_words` | round 1's 🟢 — confirmed |
| round-1 | `phases/phase-1.md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/cmdline.py#_env_walk` | round 1's 🟢 — confirmed |
| round-1 | D1's corpus | round 1's 🟢 — confirmed |
| round-1 | `hooks/cmdline_base.py` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` | round 1's 🟢 — confirmed |
| round-1 | `questions.md` D6 | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
