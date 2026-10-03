# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — review round 1

| Field | Value |
|---|---|
| Target SHA | 150b40e1c3b5a7c8093b470c94ea6ff1eb804b11 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 745 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `b4bd4ea1d2d1ad497735c1fe210fd51b8bca734d..36ddfb75725155c98a467e80b8aff16ee17dd858`, 4 commits |
| Contract changes | none |
| New units | HIDDEN_FILE_CHECKOUTS (depth 1); test_a_file_checkout_hidden_from_the_frozen_reader_is_asked_as_a_switch (depth 1); test_the_guard_policy_says_a_hidden_file_checkout_is_asked (depth 1) |
| Needs a fix | yes — 🟡 1, the policy sentence in `docs/worktree-guard-spec.md` §*Which tree* that promises silence for restores the guard still asks about |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 targets `150b40e1`, the build `2b1dcb1f..420cfcfc` plus a merge of #742. It was asked to check #737 against the frame and the approved plan, then quality, rebuilding the build's generated comparison rather than trusting its counts. Named for close checking:
- whether C asks anything bash runs as neither a switch nor a creation where `2b1dcb1f` did not, or goes silent on a real switch or creation;
- the orchestrator's reading of S5 (a), and whether the policy sentence states the tree-blind questions truthfully;
- env's two walks against the GNU and BSD sources;
- the owner's corpus count;
- the untouched files and the ledger.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the policy says a restore carrying a redirection is not asked, and names one exception; five positions still ask *switches a branch*, `git checkout &>/dev/null README.md` among them | `docs/worktree-guard-spec.md:627` | **fixed** `4a07ecec` | fixed at 4a07ecec; executed at function level at the build and at `2b1dcb1f`; the sentence's general clause is wider than the behaviour and its exception narrower than the tree-blind class |
| ⬜ 2 | N1 and phase 1 say C adds no question on a shape bash runs as nothing apart from 24; 60 commands (`2>&<file>`, `{fd}>&<file>` before `add` or `-C`'s value) are added, which bash refuses and zsh runs | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | answered | corrected at `870c3149`; executed: bash 3.2.57 and 5.2.37 refuse as an ambiguous redirect, zsh 5.9 hands git `worktree add ../wt b`; asking is right for zsh, so only the record's figure is wrong |
| ⬜ 3 | the changelog says the gate stops more and never less; 132 `env` and 357 `genv` finds of `2b1dcb1f` are dropped where no env runs the string | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md` | answered | corrected at `1b72b2c6`; executed against macOS `env`; the GNU half read through a model of `src/env.c`; zero misses either way |
| ⬜ 4 | phase 2 says `genv` and every GNU reading return what they did at `2b1dcb1f`; `genv` reads BSD's `-` letter and the two new rows | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/phases/phase-2.md` | answered | corrected at `36ddfb75`; executed: 1,930 finds gained, 357 lost over my shapes; N2's row stays true |
| 🟢 | C drops no question on a shape bash runs as a switch or a creation | `hooks/worktree-guard.py#_bare_words` | confirmed | executed: 1,473 dropped commands, every one refused, restore, detach or nothing under bash 5.2 and 3.2; the frozen decisions are identical at all three commits on all 65,460 commands |
| 🟢 | the 24 shapes bash 3.2 cannot run are creations under bash 4.1 or later | `phases/phase-1.md` | confirmed | executed under bash 5.2.37 with a recording `git`, then real git on the argv |
| 🟢 | the env walk misses nothing either env runs | `hooks/cmdline.py#_env_walk` | confirmed | executed: 0 of 322 macOS `env` runs missed; read: 0 of 5,806 GNU-model runs missed; `src/env.c`'s `longopts` read and matching `ENV_OPTIONS` |
| 🟢 | the owner's count is 0 over 27,351 pairs, and env's reading changes on none of D1's 1,858 env lines | D1's corpus | confirmed | executed: 0 at the build and at `2b1dcb1f` |
| 🟢 | `hooks/cmdline_base.py` and `docs/commit-review-gate-spec.md` are byte-identical to `2b1dcb1f` | `hooks/cmdline_base.py` | confirmed | executed: an empty `git diff --stat 2b1dcb1f 150b40e1` |
| 🟢 | the ledger edits read clean and the survivors are excused | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` | confirmed | executed: `evidence-check` 0 drifted and 0 broken on both fragments, 0 names refused; `survivor-check` exit 0 |
| ❓ | whether 0.18.0 ships the tree-blind questions `233f0455` never asked (D6's "should not ship a question the base did not ask"); the orchestrator's reading of S5 (a) is sound for this item and does not answer the release | `questions.md` D6 | ❓ out of verified scope | a decision, not a check: #733's D3 put them in the release, and #737's §*Out* keeps them. 2,136 commands over my shapes are asked at both `2b1dcb1f` and the build where bash runs neither and `233f0455` was silent. Who answers it: the repository owner |

## Paste-ready fixes

```
redirection's word is never read as a branch name, and a restore or a detach
that carries one (`git checkout . &>/dev/null`, `git switch
--detach>/dev/null`) is not asked about (#737). The reading still looks up no
tree, so a checkout of a file the frozen reader cannot see, behind a
redirection in front of `git` (`2>/dev/null git checkout README.md`), is
asked as a switch, as it has been since #678. Measured before it was wired:
```
```
redirection's word is never read as a branch name, and a restore of `.` or of
a path after `--`, or a detach, that carries one (`git checkout .
&>/dev/null`, `git switch --detach>/dev/null`) is not asked about (#737). The
reading still looks up no tree, so a file's name reads as a branch's: a
checkout of a file is asked as a switch wherever a redirection hides
`checkout` from the frozen reader, in front of `git`, between `git` and
`checkout`, glued to either, or as an `&>` before the name (`2>/dev/null git
checkout README.md`, `git checkout>/dev/null README.md`, `git checkout
&>/dev/null README.md`), as it has been since #678. Measured before it was
wired:
```
```
no stop added over `2b1dcb1f` on a shape bash ran as nothing, apart from 24 shapes bash 3.2 cannot run and bash 4.1 runs as a creation, and a numbered `>&` with a file before `add` or `-C`'s value (`git worktree 2>&/dev/null add ../wt b`), which bash refuses as an ambiguous redirect and zsh runs as the creation (warden round 1)
```
```
  `env`'s options are now read both ways, and every string either reading
  finds is judged, so the gate stops on every spelling either `env` runs. A
  prefix of `--env0-from` or `--quoting-style` now takes the next word as its
  value, as GNU reads it, so a string behind one is no longer read where no
  `env` runs it. `genv` is read as GNU's alone.
```
```
so `genv` takes GNU's walk alone. That walk is not `2b1dcb1f`'s: it reads the
two new rows, which GNU's prefixes now reach, and BSD's `-` letter, which
`_ENV_SHORT` shares between the walks. `genv -i-S '…'` is found although GNU
refuses the word, which is #733's merged-table over-read (`plan.md` E4).
```

## Executed probes

| What was run | Result |
|---|---|
| C: 16,365 core shapes from `_REDIRECTION`'s alternation, argv captured under `/bin/bash` 3.2.57 and bash 5.2.37 (container), 330 distinct argvs run under real git in fresh repository copies | 3.2: 3,372 switch, 1,523 creation, 2,470 not run; 5.2: 4,574 switch, 2,011 creation, 1,680 not run; the two bashes hand git different argv on 3,260 shapes, every one an `{fd}` or `&>>` form |
| C: `main()` at `233f0455`, `2b1dcb1f`, build over 65,460 commands (four prefixes), dirty `w` under a clean session | C's question 0 / 12,885 / 12,972; frozen decisions identical; dropped 1,473 (none a switch or creation); added 1,560 (1,500 run as a switch or creation under 5.2, 60 refused by bash) |
| zsh 5.9 and bash 3.2 on `git worktree 2>&/dev/null add ../wt b` and its neighbours, with a recording `git` | zsh hands git `worktree add ../wt b`; bash: ambiguous redirect, not run |
| function level: the five tree-blind positions and `git -C 2>/dev/null . checkout feature/x` at the build and `2b1dcb1f` | the five asked at both; the `-C` shape asked at the build only (bash runs it as a switch) |
| env: 30,894 shapes, macOS `env` executed, GNU model read, readers at `233f0455`, `2b1dcb1f`, build, for `env` and `genv` | build misses 0 / 0; `2b1dcb1f` 175 / 326; over-reads 11,423 vs 7,432; dropped 132 (`env`) and 357 (`genv`), none run |
| D1's corpus: `wider_only_kinds` at build and `2b1dcb1f`; `reparsed_texts` diff on env lines | 0 and 0 of 27,351 pairs; 0 of 1,858 env lines differ |
| `bin/evidence-check --ledger` on both touched fragments; `bin/survivor-check --range 2b1dcb1f...HEAD --exempt …/survivors.md` | 21 ok and 25 ok, 0 drifted, 0 broken; exit 0, two excused |
| `bin/test` on the two touched modules | 798 passed |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet: not run by this round, the sealer's (contract §2) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a checkout whose name has a redirection before it or glued to it is never asked (#738's class); already deferred by `questions.md` Q2. Over my shapes: 608 commands into `w` that bash 5.2 runs as a switch, silent at the build and at `233f0455`, none newly silent | #738, in its backlog milestone | the orchestrator, who carries the count to #738 |
