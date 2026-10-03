# Round 1 report: #737, a restore is asked no switch question and env's options are whole

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | `150b40e1` (merge of `origin/release/v0.18.0` at `9511f6cd`); build diff `2b1dcb1f..420cfcfc` |
| Base | `2b1dcb1f` |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at `150b40e1` under the session scratchpad; this report is the one file written in the worktree |

This is the first round, so nothing was carried from an earlier one. Every
count below is mine, from my own generators and oracles. The build's counts
in `phases/phase-1.md` and `phases/phase-2.md` were read as claims and
checked against what I measured, not reused.

## What the account claimed, and what I found

**C after the change (executed).** I rebuilt the comparison from scratch.

- The shapes: 16,365 core shapes. The operators come from the alternation of
  `_REDIRECTION` in the build's `hooks/cmdline.py` (zsh's `>!` and `>>!`
  left out, because bash is the oracle). Each takes a bare, numbered and
  `{fd}` form, and `>&` takes `1`, `2` and a file. There are 25 verbs. They
  are the frame's 13, plus `checkout -B`, `checkout --detach`,
  `switch --detach feature/x`, `checkout feature/x -- README.md`,
  `checkout main`, `worktree add -b`, `worktree add --detach`,
  `worktree prune` and four forms with a global option (`--no-pager`,
  `-C .`). Every position is generated, glued and spaced, with the target
  glued and spaced. Each core shape runs under the frame's four prefixes,
  which makes 65,460 commands.
- The oracle has two steps. First, bash runs each shape with a fake `git`
  that records the argv it is handed. That ran under macOS `/bin/bash`
  3.2.57 and under bash 5.2.37 in a throwaway local container. Second, real
  git 2.x runs each distinct argv (330 of them) in a fresh copy of a scratch
  repository. That repository holds `main`, `feature/x`, `b`, an `@{-1}`
  and a modified `README.md`. The result is one of switch, creation,
  detach, restore, nothing, refused, or not run.
- The guard: `main()` at `233f0455`, `2b1dcb1f` and the build, over a dirty
  `w` under a clean session, built as the test fixture builds it. Sessions
  are stubbed to none, and `already_asked` is stubbed so that no marker is
  written. `wider_only_kinds` is also read at function level.

Results, with bash 5.2 as the ground truth:

| | `233f0455` | `2b1dcb1f` | build |
|---|---|---|---|
| `main()`: C's question | 0 | 12,885 | 12,972 |
| `main()`: the frozen reading's deny or ask | 10,272 | 10,272 | 10,272 |

- The frozen reading's decisions are identical across all three commits on
  every command. Every difference comes from C.
- **Silent direction: no regression.** The build drops C's question on 1,473
  commands that `2b1dcb1f` asked. Under bash 5.2, every one of them runs as
  refused (510), restore (450), detach (342) or nothing (171). Under bash
  3.2 the same holds, plus 144 that do not run.
- **Asking direction: 60 commands, 16 core shapes, are new.** The build adds
  C's question on 1,560 commands. Bash 5.2 runs 1,200 of them as a creation
  and 300 as a switch. The switches are `git -C <redirection> . checkout
  feature/x`, and `2b1dcb1f` was silent there. The other 60 are
  `2>&/dev/null`, `2>& /dev/null`, `{fd}>&/dev/null` and
  `{fd}>& /dev/null` written before `add` or before `-C`'s value. bash 3.2
  and 5.2 refuse each as an *ambiguous redirect*, and nothing runs. zsh 5.9
  hands git `worktree add ../wt b` and runs it (executed). So the question
  is right for zsh, and this guard already reads zsh's forms. The build's
  generator never produced a numbered `>&` with a file, so N1's sentence
  "no stop added … apart from 24 shapes bash 3.2 cannot run" holds over its
  shapes and not over these (⬜ 2).
- **The 24 shapes bash 3.2 cannot run are confirmed (executed).** Under bash
  5.2, `git worktree &>>/dev/null add …` and `git worktree {fd}>/dev/null
  add …` reach git as `worktree add …` and real git creates the worktree.
  This answers the second row of `overview.md` §*Not verified*.

**The frame's literal S5 (a), and the orchestrator's reading.**

- Read literally, (a) says the build asks no shape bash runs as neither a
  switch nor a creation unless `233f0455` asked it. Over my shapes it fails
  on 2,196 commands under bash 5.2.
  - 1,272 are tree-blind: `checkout README.md` and `checkout main` (already
    on `main`).
  - 864 are a descriptor glued into an option word, or a name tied to a tree
    in some other way.
  - 60 are the shapes above.
  - `2b1dcb1f` asks 2,136 of the 2,196.
- (a) cannot hold together with §*Out* ("A tree-aware C … #689 decided that
  the wider reading never picks a tree"). The verb list holds `checkout
  README.md`, and a C that reads no tree cannot tell that word from
  `feature/x`.
- The orchestrator read (a) as "adds no question the pre-build head did not
  ask". That reading is sound **as the regression test for this work
  item**. It is the only reading under which (a) and §*Out* both hold, and
  `overview.md` §*Where spec and implementation diverged* records the
  divergence with its grounds.
- What it does not answer is the release goal `questions.md` D6 quotes:
  "0.18.0 should not ship a question the base did not ask". 0.18.0 will
  still ask the tree-blind restores, and `233f0455` asked none of them. That
  is #733's D3 decision carried into the release. Whether the release ships
  it is the owner's to decide, so it is a ❓ below and not a finding against
  this build.

**The policy sentence and the 414 (executed at function level).**

- `docs/worktree-guard-spec.md` §*Which tree*, at lines 627 to 633, says a
  restore that carries a redirection "is not asked about". It then names one
  exception: a file checkout "behind a redirection in front of `git`".
- The build still asks, and so did `2b1dcb1f`, wherever the redirection
  hides `checkout` from the frozen reader:
  - `git 2>/dev/null checkout README.md`
  - `git>/dev/null checkout README.md`
  - `git checkout>/dev/null README.md`
  - `git checkout<<<word README.md`
  - `git checkout &>/dev/null README.md`
- The last of these is a restore carrying the very `&>` the sentence's own
  example carries. A person who reads the sentence expects silence and gets
  *switches a branch*. So the sentence does not state the tree-blind class
  truthfully. Its general clause is wider than the behaviour, and its
  exception is narrower than the class (🟡 1).

**env's two walks.**

- **What I read, not ran.** GNU coreutils `src/env.c` on the coreutils
  mirror, read on 2026-10-03: `shortopts` is `"+a:C:iS:u:v0"` plus the
  whitespace characters. `longopts` holds `env0-from` (required) and
  `quoting-style` (required) among the fifteen. A lone `-` after the loop
  sets the ignore-environment flag and is consumed. This matches the frame's
  account and `ENV_OPTIONS`. GNU env is not installed here, so GNU's half is
  read through a model I wrote from that source.
- **What I ran: BSD's half.** macOS `env` ran 30,894 generated shapes:
  every short letter of either grammar alone and in pairs, `-` included,
  with values glued and spaced; every GNU long name in every prefix from
  `--x`, with `=v` and spaced; `--` and `-` alone; a redirection; an
  assignment; 25,000 random sequences of two or three such words. Each was
  followed by one of twelve split words (`-S`, `-iS`, `-vS`,
  `--split-string`, `--spl`, `--S`, `-i-S`, `--iS`, `-0S`, `-uS`, `--uS`,
  `-CS`).
  - macOS `env` ran the string on 322 shapes. The GNU model runs it on
    5,806.
  - The build misses **0** of either. `2b1dcb1f` misses 175 and 326, and
    `233f0455` misses 268 and 4,173.
- **BSD's `--unset`-prefix reading holds** in the build:
  - `--u` takes the next word.
  - `--un…` is `-i -u <rest>`.
  - `-i-S` and `---S` are clusters through `-`.
  - `--env0-from` and `--quoting-style` are refused letters under BSD and
    take a value under GNU.
- **`genv` gets the GNU walk only**: `word == "env"` gates the BSD walk.
  But the GNU walk reads BSD's `-` letter, because `_ENV_SHORT["-"]` is
  shared. So `genv -i-S '…'` is now found, and GNU refuses that word as an
  invalid option.
  - This is the merged-table over-read #733's E4 accepts. D3's grounds
    rejected it for `genv`.
  - `phases/phase-2.md` says "`genv` and every GNU reading return exactly
    what they returned at `2b1dcb1f`". That is false. Over my shapes,
    `genv` gains 1,930 finds, 326 of them strings the GNU model runs, and
    loses 357 (⬜ 4).
- **The over-reads.** The build finds a string on 11,423 shapes where
  neither env runs it, and `2b1dcb1f` on 7,432. Every find the build adds
  is a word one grammar refuses that the other walk reads past, or a `-`
  letter GNU lacks: #733's settled over-read, applied to the second walk.
  - None is a line without a commit that stops in a declared repository.
  - A string's invocation carries `Unresolved(CONSTRUCT)` of its segment's
    own directory. It is judged there, and a declared repository is silent
    for it. `test_a_declared_repository_meets_no_new_stop` passed in my
    narrow run.
  - Over D1's corpus, `reparsed_texts` differs on **0** of the 1,858
    commands that mention `env`.
- **"Never less" is false (⬜ 3).** The build no longer finds 132 `env`
  shapes `2b1dcb1f` found, and 357 `genv` shapes. Each is a prefix of
  `--env0-from` or `--quoting-style` that now takes the next word as its
  value, such as `env --ax --quoti --spl '…'`. Neither macOS `env` nor the
  GNU model runs any of them, so nothing is missed. The changelog's "the
  gate stops more and never less" is still untrue.

**The owner's count (executed).** The cut and method are D1's: Bash tool uses
before 2026-10-03T11:06:22+09:00, giving 27,551 uses and 27,351 distinct
command and directory pairs. `wider_only_kinds` fires on **0** at the build
and **0** at `2b1dcb1f`. My comparison tested the build's own C, not a
rebuilt C with other logic, so this re-run confirms the build's count rather
than replacing it.

**Untouched files and the ledger (executed).**

- `git diff --stat 2b1dcb1f 150b40e1 -- hooks/cmdline_base.py
  docs/commit-review-gate-spec.md` is empty, so both files are
  byte-identical to the base.
- `bin/evidence-check --ledger <file>` reads 0 drifted and 0 broken for this
  item's fragment (21 ok) and for 1790993140's fragment (25 ok). Its records
  pass refuses 0 names, so the four NAME NOT IN TREE markers hold.
- `bin/survivor-check --range 2b1dcb1f...HEAD --exempt …/survivors.md`
  exits 0, with two survivors excused.
- **Read.** N1, N2, the five `Re-read ·` rows (E14, E16, I5, I6, M2), K3,
  K5 and K7 each state what the code holds now. E14's dated note in
  `seal/releases/0.16.0.md`, "all but two … deferred to #737", is a
  historical note in a frozen file. Its `Re-read · E14` row says the table
  now holds both, so a `Corrected ·` row is not owed.

**The narrow run (executed).** `bin/test
tests/test_guard_resolves_the_tree_it_judges.py
tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py -q`
gave 798 passed. The broad gate is the sealer's, and I did not run it.

## Findings

### 🟡 1 — The guard's policy says a restore with a redirection is not asked, and five positions still ask

`docs/worktree-guard-spec.md:627` to `:633`, in §*Which tree*'s #678
paragraph.

- **What is wrong.** "a restore or a detach that carries one (…) is not
  asked about (#737)" holds only where the redirection leaves `checkout`
  visible to the frozen reader, or where the restore names no file. The
  exception that follows names one position, "behind a redirection in front
  of `git`". These also ask *switches a branch*, at the build and at
  `2b1dcb1f` (function level, executed):
  - `git 2>/dev/null checkout README.md`
  - `git>/dev/null checkout README.md`
  - `git checkout>/dev/null README.md`
  - `git checkout<<<word README.md`
  - `git checkout &>/dev/null README.md`
- **Why it matters.** This is the paragraph a person reads to learn when the
  guard asks. The fifth shape is a restore carrying the same `&>` as the
  sentence's example, and the sentence promises silence there. Contract §14
  is why the sentence was added. It has to say what the person sees, and
  nothing pins the tree-blind half.
- **Fix.** Name what makes the reading tree-blind, not one position. The
  fence is below, with a case that pins the sentence under *Regression tests
  to plant*.

### ⬜ 2 — N1 and phase 1 say C adds no question on a shape bash runs as nothing, apart from 24; 16 more core shapes are added

`seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md`,
row N1, the Executed cell, and `phases/phase-1.md` §*What this phase found*.

- **What is wrong.** The build adds C's question on `git worktree
  2>&/dev/null add ../wt b`, on its spaced-target form, on the
  `{fd}>&/dev/null` form, and on the same forms in front of `-C`'s value.
  That is 60 commands over the four prefixes. bash refuses each as an
  ambiguous redirect, so nothing runs (executed under 3.2.57 and 5.2.37).
  zsh 5.9 runs each as the creation or the switch (executed).
- **Why it does not need a code change.** The guard reads zsh's forms on
  purpose (`ZSH_PREFIXED`, `>!`), and the shell this repository's sessions
  run is zsh. So asking is the right answer, and the defect is only the
  record's figure.
- **Fix.** The fence below corrects N1's sentence.

### ⬜ 3 — The changelog says the gate "stops more and never less"; it stops less where nothing runs

`seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md`,
the second bullet.

- **What is wrong.** The new rows make a prefix of `--env0-from` or
  `--quoting-style` take the next word in the GNU walk. Over my shapes,
  that drops 132 `env` finds and 357 `genv` finds that `2b1dcb1f` made.
  Neither macOS `env` (executed) nor the GNU model (read) runs any of them.
  `spec.md` states the same failure direction, "finds more and never less.
  A reading is only added", but that is the framer's file, so only the
  shipped line is fixed here.
- **Why it matters.** The line ships in the release note, and its claim is
  checkable and false. The behaviour is right.
- **Fix.** Fence below.

### ⬜ 4 — Phase 2 says `genv` reads exactly as it did; it reads BSD's `-` letter and the two new rows

`seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/phases/phase-2.md`,
§*What this phase found*, the W1 paragraph.

- **What is wrong.** "so `genv` and every GNU reading return exactly what
  they returned at `2b1dcb1f`" is false. `_ENV_SHORT["-"]` is shared by both
  walks, and the two rows change GNU's prefixes. Over my shapes, `genv`
  gains 1,930 finds and loses 357.
  - 326 of the gains are strings the GNU model runs, and those are the fix
    working.
  - 1,559 are over-reads, mostly `genv -i-S '…'`, which GNU refuses.
- **Why it is ⬜.** The over-read is #733's E4 direction: it costs a stop
  only where nothing runs. N2's row, "`genv` takes GNU's walk alone", stays
  true of the code. Only the phase record's sentence is wrong.
- **Fix.** Fence below. If D3's grounds are to hold for `genv` exactly, the
  alternative is to read `-` under the BSD grammar alone. That is a code
  change with a case to plant, and it is not proposed here.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the policy says a restore carrying a redirection is not asked, and names one exception; five positions still ask *switches a branch*, `git checkout &>/dev/null README.md` among them | `docs/worktree-guard-spec.md:627` | open | executed at function level at the build and at `2b1dcb1f`; the sentence's general clause is wider than the behaviour and its exception narrower than the tree-blind class |
| ⬜ 2 | N1 and phase 1 say C adds no question on a shape bash runs as nothing apart from 24; 60 commands (`2>&<file>`, `{fd}>&<file>` before `add` or `-C`'s value) are added, which bash refuses and zsh runs | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | open | executed: bash 3.2.57 and 5.2.37 refuse as an ambiguous redirect, zsh 5.9 hands git `worktree add ../wt b`; asking is right for zsh, so only the record's figure is wrong |
| ⬜ 3 | the changelog says the gate stops more and never less; 132 `env` and 357 `genv` finds of `2b1dcb1f` are dropped where no env runs the string | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md` | open | executed against macOS `env`; the GNU half read through a model of `src/env.c`; zero misses either way |
| ⬜ 4 | phase 2 says `genv` and every GNU reading return what they did at `2b1dcb1f`; `genv` reads BSD's `-` letter and the two new rows | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/phases/phase-2.md` | open | executed: 1,930 finds gained, 357 lost over my shapes; N2's row stays true |
| 🟢 | C drops no question on a shape bash runs as a switch or a creation | `hooks/worktree-guard.py#_bare_words` | confirmed | executed: 1,473 dropped commands, every one refused, restore, detach or nothing under bash 5.2 and 3.2; the frozen decisions are identical at all three commits on all 65,460 commands |
| 🟢 | the 24 shapes bash 3.2 cannot run are creations under bash 4.1 or later | `phases/phase-1.md` | confirmed | executed under bash 5.2.37 with a recording `git`, then real git on the argv |
| 🟢 | the env walk misses nothing either env runs | `hooks/cmdline.py#_env_walk` | confirmed | executed: 0 of 322 macOS `env` runs missed; read: 0 of 5,806 GNU-model runs missed; `src/env.c`'s `longopts` read and matching `ENV_OPTIONS` |
| 🟢 | the owner's count is 0 over 27,351 pairs, and env's reading changes on none of D1's 1,858 env lines | D1's corpus | confirmed | executed: 0 at the build and at `2b1dcb1f` |
| 🟢 | `hooks/cmdline_base.py` and `docs/commit-review-gate-spec.md` are byte-identical to `2b1dcb1f` | `hooks/cmdline_base.py` | confirmed | executed: an empty `git diff --stat 2b1dcb1f 150b40e1` |
| 🟢 | the ledger edits read clean and the survivors are excused | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` | confirmed | executed: `evidence-check` 0 drifted and 0 broken on both fragments, 0 names refused; `survivor-check` exit 0 |
| ❓ | whether 0.18.0 ships the tree-blind questions `233f0455` never asked (D6's "should not ship a question the base did not ask"); the orchestrator's reading of S5 (a) is sound for this item and does not answer the release | `questions.md` D6 | ❓ out of verified scope | a decision, not a check: #733's D3 put them in the release, and #737's §*Out* keeps them. 2,136 commands over my shapes are asked at both `2b1dcb1f` and the build where bash runs neither and `233f0455` was silent. Who answers it: the repository owner |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a checkout whose name has a redirection before it or glued to it is never asked (#738's class); already deferred by `questions.md` Q2. Over my shapes: 608 commands into `w` that bash 5.2 runs as a switch, silent at the build and at `233f0455`, none newly silent | #738, in its backlog milestone | the orchestrator, who carries the count to #738 |

## Paste-ready fixes

### 🟡 1

Replace these lines in `docs/worktree-guard-spec.md` (627 to 633):

```
redirection's word is never read as a branch name, and a restore or a detach
that carries one (`git checkout . &>/dev/null`, `git switch
--detach>/dev/null`) is not asked about (#737). The reading still looks up no
tree, so a checkout of a file the frozen reader cannot see, behind a
redirection in front of `git` (`2>/dev/null git checkout README.md`), is
asked as a switch, as it has been since #678. Measured before it was wired:
```

with:

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

### ⬜ 2

In N1's Executed cell, replace "no stop added over `2b1dcb1f` on a shape bash
ran as nothing, apart from 24 shapes bash 3.2 cannot run and bash 4.1 runs as
a creation" with:

```
no stop added over `2b1dcb1f` on a shape bash ran as nothing, apart from 24 shapes bash 3.2 cannot run and bash 4.1 runs as a creation, and a numbered `>&` with a file before `add` or `-C`'s value (`git worktree 2>&/dev/null add ../wt b`), which bash refuses as an ambiguous redirect and zsh runs as the creation (warden round 1)
```

### ⬜ 3

Replace the last two sentences of the changelog's second bullet with:

```
  `env`'s options are now read both ways, and every string either reading
  finds is judged, so the gate stops on every spelling either `env` runs. A
  prefix of `--env0-from` or `--quoting-style` now takes the next word as its
  value, as GNU reads it, so a string behind one is no longer read where no
  `env` runs it. `genv` is read as GNU's alone.
```

### ⬜ 4

In `phases/phase-2.md`, replace "so `genv` and every GNU reading return
exactly what they returned at `2b1dcb1f`." with:

```
so `genv` takes GNU's walk alone. That walk is not `2b1dcb1f`'s: it reads the
two new rows, which GNU's prefixes now reach, and BSD's `-` letter, which
`_ENV_SHORT` shares between the walks. `genv -i-S '…'` is found although GNU
refuses the word, which is #733's merged-table over-read (`plan.md` E4).
```

## Regression tests to plant

For 🟡 1, in `tests/test_guard_resolves_the_tree_it_judges.py`. The case
pins the sentence's tree-blind half, so a later change to C that silences
these has to change the policy too. It should pass at the build. Show it red
against a mutant whose `switch_kind` skips a name containing a `.`.

```python
@pytest.mark.parametrize(
    "command",
    [
        "2>/dev/null git checkout README.md",
        "git 2>/dev/null checkout README.md",
        "git checkout>/dev/null README.md",
        "git checkout &>/dev/null README.md",
    ],
)
def test_a_file_checkout_hidden_from_the_frozen_reader_is_asked_as_a_switch(
    tmp_path, command
):
    """`docs/worktree-guard-spec.md` §*Which tree*: C reads no tree, so a
    file's name reads as a branch's wherever a redirection hides `checkout`
    from the frozen reader (warden round 1 of #737)."""
    assert wg.wider_only_kinds(command, str(tmp_path)) == {"switch"}, command
```

## Facts for the evidence ledger

- GNU coreutils `src/env.c`, read 2026-10-03: `shortopts` is
  `"+a:C:iS:u:v0"` plus the whitespace characters. `longopts` holds
  `env0-from` and `quoting-style`, each with a required argument. A lone `-`
  after option parsing sets the ignore-environment flag and is consumed.
  This is read and not run.
- bash 5.2.37 hands git `worktree add ../wt b` for `git worktree
  &>>/dev/null add ../wt b` and for `git worktree {fd}>/dev/null add ../wt
  b`, and git creates the worktree. Executed on 2026-10-03.
- bash 3.2.57 and 5.2.37 refuse `2>&/dev/null` as an ambiguous redirect, and
  zsh 5.9 runs the command. Executed on 2026-10-03.

## Not verified

| Item | Who must answer |
|---|---|
| GNU's half run against a real GNU `env` 9.12 or later; mine is a model of the source, as the build's was | a reviewer or a CI leg with GNU coreutils 9.12+ |
| the full suite, lint and typecheck | the sealer, after the rounds settle |

Needs a fix: yes — 🟡 1, the policy sentence in `docs/worktree-guard-spec.md` §*Which tree* that promises silence for restores the guard still asks about

Loses a record or crashes: no

## Proof block

Files opened: `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/spec.md`,
`questions.md`, `plan.md`, `phases/phase-1.md`, `phases/phase-2.md`,
`phases/phase-3.md`, `overview.md`, `changelog.md`, `survivors.md`;
`hooks/cmdline.py` (`_REDIRECTION`, `redirection_width`, `unglued`,
`split_segments_with_separators`, `merged_view`, `reparsed_texts`,
`_env_walk`, `ENV_OPTIONS`, `_env_long`, `_env_option`, `_env_words`,
`command_strings`, `names_an_unknown_command`, `_without_redirections`,
`_string_at`); `hooks/worktree-guard.py` (`switch_kind`, `wider_only_kinds`,
`_bare_words`, `ask_what_only_the_wider_reading_finds`, `already_asked`,
`main`); `hooks/commit-review-gate.py` (`_hides_a_commit`,
`_string_hides_a_commit`, `_unresolved_base`, the string arm and the
unreadable decision); `tests/test_guard_resolves_the_tree_it_judges.py` (the
harness, `WIDER_ONLY` and the new cases);
`tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`
(`HANDED`, `CONTROLS`, `ENV_SPELLINGS`, `ENV_GRAMMAR`); `tests/conftest.py`
(`_build_repo`, `load_hook_module`);
`seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md`,
`seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md`,
`seal/releases/0.16.0.md` (E14, E16, I5, I6, M2);
`docs/the-evidence-ledger.md` (the released-row section);
`docs/worktree-guard-spec.md` (the #678 paragraph); `bin/test`.
