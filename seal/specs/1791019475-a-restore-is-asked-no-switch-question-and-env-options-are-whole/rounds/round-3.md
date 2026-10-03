# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — review round 3

| Field | Value |
|---|---|
| Target SHA | 5e4984b111a6c4904acf80e74e46c0fd593f0aba |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 745 |
| Broad gate | 2c23373d against 9511f6cd |
| Fixes checked by | no fixes to check |
| Fix range | `8f59851fd01eea8a5ad8f21b3db5fb365734ff1d..8f59851fd01eea8a5ad8f21b3db5fb365734ff1d`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 9, the list of words in `docs/worktree-guard-spec.md` §*Which tree*'s rule, which counts a checkout's name before `--` and leaves out a bare `-B`, and which no case pins |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is a verifying round and the run's last, since round 2 closed on fixes and spent the one reopening. It targets `5e4984b1` over round 2's fix range `6999b001..e8808af1`. It was asked whether the policy paragraph's rule matches the guard, tested by an independent generator in both directions; whether the rule's list of words that make a kind is complete against `switch_kind`; whether the new rule case and the policy case pin the rule; whether the build's surviving-mutant claim holds; and whether ⬜ 6–8 and the ledger hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 9 | the rule's list of words says a `checkout` naming a word before `--` is a switch and names `checkout -b` but not `-B`; the guard reads any `checkout` carrying `--` as nothing and a bare `-B` as a switch, and no case pins the list | `docs/worktree-guard-spec.md:631` | deferred #750 | #750 — The run is capped at the reopening bound, which commissions nothing. The guard behaves rightly in every case; the sentence word list is filed with the reviewer fix and pin; executed: my generator, 2,859 commands; the sentence's words in place of `switch_kind` differ on 37 shapes (a name before `--`, silent through `main()`) and 58 shapes (a bare `-B`, asked through `main()`); deleting the sentence leaves the module green; real git restores without moving HEAD and refuses a bare `-B`. The same class as yellows 1 and 5, in a unit round 2's fix created |
| ⬜ 10 | the new rule case's `own in frozen` half can never fire, because the function-level default already subtracts the same set; its docstring claims a check it does not make | `tests/test_guard_resolves_the_tree_it_judges.py:1226` | deferred #750 | #750 — The same paragraph and test module; filed beside 🟡 9; executed: the mutant dropping `kind not in frozen` leaves the case green, and only `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` fails; read: the default `judged` and the case's `frozen` are the same expression. Behaviour held, so not counted in `Needs a fix` |
| 🟢 | round 2's yellow-severity finding 5 is closed for what it named — the detach promise and the list of positions are gone, and the rule's condition matches the guard | `docs/worktree-guard-spec.md:628` | confirmed | executed: over 2,859 commands of my own generator, the condition with `switch_kind`'s words and the guard agree on every shape; under zsh-handed argv, the only other difference is `{fd}` in front of `git`, which bash 4.1 runs. The residual, in the list of words, is finding 9 |
| 🟢 | round 2's white 6 is closed — the changelog's first bullet states the condition, with no detach promise and no `-q` example | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:3` | confirmed | read against the executions above; the bullet names no list of words, so finding 9 does not reach it |
| 🟢 | round 2's white 7 is closed — the env sentence is narrowed to an abbreviated split string, and says a fully spelt `-S` is still read | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:25` | confirmed | executed: `reparsed_texts` reads nothing from `env --quoti --spl`, and reads the string from `env --e -S` and `env --e --split-string`; macOS `env` refuses all three |
| 🟢 | round 2's white 8 is closed — N1 and phase 1 say zsh runs the `-C` value shapes as a switch and bash 3.2 hands git `{fd}` | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | confirmed | executed under bash 3.2.57 and zsh 5.9 with a recording `git`, then real git on bash's argv: both refused |
| 🟢 | the build's report that the mutant dropping `kind not in frozen` survives the new case and is held through `main()` | `hooks/worktree-guard.py:368` | confirmed | executed: 131 passed, 1 failed, and the one is `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it`; one case holds it, not several |
| 🟢 | K7, M2 and N1 re-read and re-stamped; the ledger reads clean and the survivors are excused | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K7 | confirmed | executed: `evidence-check --strict .` exit 0, 4,049 ok, 0 drifted, 0 broken, 0 of 1,316 names refused; `survivor-check` exit 0, two excused; read: the three notes against the diff |
| ❓ | carried from rounds 1 and 2: whether 0.18.0 ships the tree-blind questions `233f0455` never asked (`questions.md` D6) | `questions.md` D6 | ❓ out of verified scope | a decision, not a check; nothing in the fix range changes it. Who answers it: the repository owner |

## Paste-ready fixes

```
side is read by its words alone: a `switch` or a `checkout` naming a word or
`-` (other than `checkout`'s `.` and anything after `--`), a `checkout -b`, or a
`worktree add`. The reading looks up no tree (#689), so it asks whether or not
```
```
side is read by its words alone: a `switch` naming a word or `-`, a `checkout`
carrying `-b` or `-B`, a `checkout` with no `--` among its words that names
`-` or a word other than `.`, or a `worktree add`. The reading looks up no
tree (#689), so it asks whether or not
```
```python
    assert (
        "a `switch` naming a word or `-`, a `checkout` carrying `-b` or `-B`, a "
        "`checkout` with no `--` among its words that names `-` or a word other "
        "than `.`, or a `worktree add`"
    ) in text
```
```python
    # §*Which tree*'s words: a `--` takes every name out of a checkout, and
    # `-B` is a switch with or without one (round 3 of #737).
    "checkout a name before --": (["git", "checkout", "x", "--", "f"], None),
    "checkout -B with no name": (["git", "checkout", "-B"], "switch"),
    "switch -- a name": (["git", "switch", "--", "x"], "switch"),
```
```python
            kinds = wg.wider_only_kinds(command, str(tmp_path))
            if not kinds:
                continue
            asked += 1
            frozen = {
                wg.switch_kind(wg.parse_git(tokens))
                for tokens, _wheres in wg.walk_command(command, str(tmp_path))
            }
```
```python
            # `judged=set()`: the function-level default subtracts what the
            # frozen walk's words hold, which is this case's own frozen half,
            # and would leave nothing for it to check.
            kinds = wg.wider_only_kinds(command, str(tmp_path), judged=set())
            if not kinds:
                continue
            asked += 1
            text = wg.wide.drop_heredoc_bodies(wg.wide.drop_comments(command))
            items, _clean = wg.wide.split_segments_with_separators(text)
            frozen = {wg.switch_kind(wg.parse_git(tokens)) for _sep, tokens in items}
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` at `5e4984b1` | 132 passed |
| my own generator, 2,859 single commands over 33 verbs, nine operators, every position, two at once, zsh prefixes, spaced `--config-env`, inside `-C`'s value; `wider_only_kinds` against the same with the sentence's words in place of `switch_kind` | guard asks 1,189; differ on 37 (a name before `--`: the sentence asks, the guard does not) and 58 (a bare `-B`: the guard asks, the sentence does not); 60 more under the reading where "after `--`" governs `switch` |
| the same 2,859 commands under zsh 5.9 with a `git` recording its argv, read with the sentence's words, frozen segments subtracted | the same two word cases, plus `{fd}>/dev/null` before `git` on 2 shapes per verb, which zsh does not run as a command |
| six commands through `main()` in a dirty `w` under a clean session (a probe case, deleted) | silent: three `checkout feature/x -- README.md` hides; ask: `checkout -B`, `switch -- feature/x`, `checkout README.md`, each behind `2>/dev/null` |
| real git 2.54 on `checkout feature/x -- README.md`, `switch -- feature/x`, `checkout -B`, `checkout -b` in fresh repositories | HEAD stays on `main`; switches to `feature/x`; exit 129; exit 129 |
| mutant: `kind and kind not in frozen` made `kind` in `wider_only_kinds`, the guard module run | 131 passed, 1 failed: `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` |
| mutant: the sentence "Each side is read by its words alone: …" deleted from the doc, the guard module run | 132 passed |
| the fences under 🟡 9 and ⬜ 10 applied in the clone; the five modules that read `docs/worktree-guard-spec.md` run; the rule case against the mutant; the new pin against the current sentence; the corrected words against `switch_kind` over my generator | 321 passed; the rule case red against the mutant; the pin red; 0 of 2,859 differ |
| `/bin/bash` 3.2.57 and zsh 5.9 on `2>&/dev/null` and `{fd}>&/dev/null` before `add` and inside `-C`'s value, with a recording `git`; real git on bash's argv | bash: ambiguous redirect, or `{fd}` handed to git, which refuses it; zsh: `worktree add ../wt b`, `-C . checkout feature/x`, `-C . switch feature/x` |
| `reparsed_texts` on three env shapes, macOS `/usr/bin/env` on each | `--quoti --spl` reads nothing; `--e -S` and `--e --split-string` read the string; env refuses all three |
| `bin/evidence-check --strict .` in the clone at `5e4984b1` | exit 0; 4,049 ok, 0 drifted, 0 broken; records: 5 work items, 1,316 names read, 0 refused |
| `bin/survivor-check --range 2b1dcb1f...HEAD --exempt …/survivors.md` | exit 0; 677 files, 42 removed sentences, two survivors excused |
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
| round-2 | `docs/worktree-guard-spec.md:628` | round 2's 🟡 5 — fixed |
| round-2 | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:3` | round 2's ⬜ 6 — answered |
| round-2 | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:26` | round 2's ⬜ 7 — answered |
| round-2 | `tests/test_guard_resolves_the_tree_it_judges.py` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:24` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K7 | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
