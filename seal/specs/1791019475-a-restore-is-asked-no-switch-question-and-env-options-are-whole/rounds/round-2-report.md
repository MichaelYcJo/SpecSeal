# Round 2 report: #737, a restore is asked no switch question and env's options are whole

| Field | Value |
|---|---|
| Round | 2, a verifying round |
| Target SHA | `72c8f5a4` (round 1's close commit); fix range `b4bd4ea1..36ddfb75`, four commits |
| Base | `2b1dcb1f` |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at `72c8f5a4` under the session scratchpad; this report is the one file written in the worktree |

This round's target is the fix diff, not the branch. I read `rounds/round-1.md`
and `rounds/round-1-report.md` for coordinates and re-derived every verdict
below from the code at `72c8f5a4`. Round 1's own counts (65,460 commands,
16,365 core shapes, the GNU model's 5,806 runs) are carried as round 1's and
not re-run; where I re-measured, the row says so. The new units the record's
`New units` row names (`HIDDEN_FILE_CHECKOUTS` and its two cases) were judged
as code.

## What the account claimed, and what I found

**Yellow 1, the policy sentence (executed at function level and through
`main()`).** The fix commit `4a07ecec` says the sentence "names every position
at which a file checkout is still asked".

- Round 1's five positions are now named, and each is asked: before `git`,
  between `git` and `checkout`, glued to `git`, glued to `checkout` (which
  covers `checkout<<<word`), and `&>` before the name.
- I ran the case module's own generator, `_redirections()`, over `git checkout
  README.md`: 388 shapes, 212 asked. Every shape at a position the sentence
  names is asked, so the sentence claims no question the guard does not put.
- Two shapes outside the named positions are asked: `git checkout
  &>>/dev/null README.md`, target glued and spaced. bash 3.2 cannot parse it;
  bash 4 and zsh run it as `checkout README.md`.
- A file checkout with no redirection at all is also asked as a switch where
  a zsh prefix hides `git` or a spaced `--config-env` hides `checkout`:
  `noglob git checkout README.md`, `nocorrect …`, `repeat 2 …` and `git
  --config-env k=v checkout README.md`. All four ask *switches a branch*
  through `main()`, at the build and at `2b1dcb1f`. The paragraph's opening
  sentence says C covers those prefixes, but the tree-blind clause attributes
  the file's question to a redirection alone.
- **The sentence's first clause still promises a silence C does not keep.**
  "a restore of `.` or of a path after `--`, or a detach, that carries one
  … is not asked about". A detach that names a commit is asked as a switch:
  `switch --detach feature/x` and `checkout --detach feature/x` are each
  asked on 226 of 492 generated shapes, and `2>/dev/null git switch --detach
  feature/x` asks *switches a branch* through `main()`. bash hands git
  `switch --detach feature/x`, which moves the tree, so asking is right and
  the sentence is wrong. Only a detach naming nothing (`git switch
  --detach>/dev/null`, 0 of 388 asked) is silent. Round 1 enumerated the
  restore half of this sentence and not the detach half, so this is the same
  class as yellow 1 (contract §12), at a coordinate round 1 did not name (🟡 5).
- The changelog's first bullet carries the same detach promise, and an
  example (`git checkout -q &>/dev/null`) that is none of the three things
  the bullet names (⬜ 6).

**The two new cases (executed).** Both were seen red as their docstrings say.

- A `switch_kind` that returns nothing for a `checkout` naming a word holding
  `.` turns all four `HIDDEN_FILE_CHECKOUTS` red.
- The policy case's assertions, run against `b4bd4ea1`'s text of the doc,
  fail three of four. The fourth, `2>/dev/null git checkout README.md`, was in
  the old sentence.
- What the policy case does not pin is the first clause, the one that
  promises silence. A later edit back to "a restore or a detach" keeps it
  green. The planted case under 🟡 5 closes that.

**White 2, N1 and phase 1 (executed under bash 3.2.57 and zsh 5.9).** I
generated a numbered and bare `>&` with a file at every position of seven
verbs (380 shapes) and compared the build with `2b1dcb1f`: 50 added, 0
dropped.

- `2>&/dev/null` and `3>&/dev/null` before `add` or `-C`'s value: bash 3.2
  refuses each as an ambiguous redirect and zsh runs it. This matches N1.
- `1>&/dev/null` and a bare `>&/dev/null`: bash and zsh both run the creation
  or the switch. Those questions are right, and N1 does not claim otherwise.
- `{fd}>&/dev/null`: bash 3.2 does not refuse it. It has no `{fd}`, so it
  hands git `worktree {fd} add ../wt b` or `-C {fd} . checkout feature/x`,
  and git runs nothing. The outcome is round 1's, but the stated reason is
  not true of 3.2. Round 1 records bash 5.2 refusing it; I have no bash 5
  here and carry that.
- Before `-C`'s value, with `checkout` or `switch` as the verb, zsh runs
  each as a **switch** (`-C . checkout feature/x`), and the build asks it as
  one. N1 and phase 1 both say "zsh runs as the creation". Round 1's prose
  said "the creation or the switch"; its fence, which the fix pasted,
  dropped the second half (⬜ 8).

**White 3, the changelog's env sentence (executed against macOS `env`; GNU
read).** "never less" is gone. The new sentence says a string behind a
prefix of `--env0-from` or `--quoting-style` "is no longer read where no
`env` runs it".

- `env --quoti --spl 'echo RAN'`: read at `2b1dcb1f`, not read at the build;
  macOS `env` refuses it. This matches.
- `env --e -S 'echo RAN'` and `env --quoti x -S 'echo RAN'`: read at both the
  build and `2b1dcb1f`. In the first, GNU takes `-S` as `--e`'s value and runs
  no string; macOS refuses `e`. So a string behind a prefix is still read
  where no `env` runs it, because `_env_walk` reads `-S` and
  `--split-string` spelt in full anywhere, as the base did. The sentence is
  true of an abbreviated split string only (⬜ 7).
- "stops on every spelling either `env` runs": `env -i-S`, `env ---S` and
  `env --unset -iS` are found at the build and not at `2b1dcb1f`, and macOS
  `env` runs each. Round 1's zero-miss count is carried.

**White 4, phase 2's `genv` paragraph (executed sample; GNU read).** `genv
-i-S 'echo RAN'` is found at the build and not at `2b1dcb1f`, and `genv
--quoti --spl 'echo RAN'` is found at `2b1dcb1f` and not at the build. Those
are the shared `-` letter and the two new rows, as the paragraph now says.
That GNU refuses `-i-S` is read from its `shortopts`, which carry no `-`. The
1,930 and 357 are round 1's counts, attributed to round 1, and carried.

**The ledger (executed).** `bin/evidence-check --strict .` exits 0: 4,049 ok,
0 drifted, 0 broken, and its records pass refuses 0 of 1,285 names.
`bin/survivor-check --range 2b1dcb1f...HEAD --exempt …/survivors.md` exits 0
over 677 files and 42 removed sentences, with the same two survivors
excused. **Read:** K7's and M2's new `Re-read` notes against the diff. K7
states the guard chooses no tree through the wider reader, asks it one
question and puts what only it finds to the person, consent first. M2
states that a git behind a redirection is still not git to the frozen
reading. The fix changed neither, so both notes are true.

**The narrow run (executed).** `bin/test
tests/test_guard_resolves_the_tree_it_judges.py -q -k` over the two new
cases and their three neighbours gave 12 passed. The broad gate is the
sealer's, and I did not run it.

## Findings

### 🟡 5 — The policy still says a detach carrying a redirection is not asked, and its list of asked file checkouts misses three hides

`docs/worktree-guard-spec.md:628` to `:637`, §*Which tree*'s #678 paragraph.

- **What is wrong.** "a restore of `.` or of a path after `--`, or a detach,
  that carries one … is not asked about" is false for a detach that names a
  commit. `2>/dev/null git switch --detach feature/x`, `git switch --detach
  &>/dev/null feature/x` and `2>/dev/null git checkout --detach feature/x`
  each ask *switches a branch*, at the build and at `2b1dcb1f`. Separately,
  the list of positions where a file checkout is asked omits `&>>` before
  the name, a zsh prefix in front of `git`, and a spaced `--config-env`.
- **Why it matters.** This is the paragraph a person reads to learn when the
  guard asks, and the reason round 1's yellow 1 was 🟡. A person who reads
  "a detach … is not asked about" and runs a detach to `feature/x` behind a
  redirection gets *switches a branch*. The behaviour is right: the detach
  moves the tree, and the frozen reading treats the same command as a
  switch when it can see it. Only the sentence is wrong.
- **Fix.** Split the detach by whether it names a commit, and name the three
  missing hides. The policy case keeps its phrase and gains the detach. The
  fence is below, with a case to plant.

### ⬜ 6 — The changelog's first bullet promises the same detach silence, and its `-q` example is in none of its categories

`seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:3`
to `:12`. This is paperwork under `seal/specs/`, so it is a correction and
is not counted in `Needs a fix`.

- **What is wrong.** "no longer asks … about a restore of `.` or of a path
  after `--`, or a detach, that carries a redirection". A detach naming a
  commit is still asked, and was at `2b1dcb1f`. The example `git checkout -q
  &>/dev/null` is neither a restore of `.`, nor of a path after `--`, nor a
  detach. bash hands git `checkout -q`, which names nothing.
- **Also noted, not fixed here.** "is still asked, as it was before this
  change" compares with `2b1dcb1f`, which no release shipped. 0.17.0 asked
  none of these, which is round 1's ❓ for the owner, carried below.
- **Fix.** Fence below.

### ⬜ 7 — The changelog says a string behind a prefix of the two new options is no longer read; a fully spelt `-S` behind one still is

`seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:26`
to `:28`. Paperwork, so a correction.

- **What is wrong.** `env --e -S 'echo RAN'` and `env --quoti x -S 'echo
  RAN'` are read at the build, as at `2b1dcb1f`. GNU takes `-S` as the
  prefix's value in the first, and macOS refuses `e`, so no `env` runs that
  string. The change stopped only an abbreviated split string behind one
  (`env --quoti --spl '…'`), because `-S` and `--split-string` spelt in full
  are read wherever they stand.
- **Why it is ⬜.** The over-read is #733's settled direction, a stop where
  nothing runs, and the code is right. The release-note line overstates
  what changed.
- **Fix.** Fence below.

### ⬜ 8 — N1 and phase 1 say zsh runs the numbered `>&` shapes as the creation and bash refuses each; zsh runs the `-C` ones as a switch, and bash 3.2 does not refuse `{fd}>&`

`seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md`
row N1, the Executed cell and the `Corrected` note, and
`seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/phases/phase-1.md:105`.
Paperwork, so a correction.

- **What is wrong.** `git -C 2>&/dev/null . checkout feature/x` and its
  `switch` and `{fd}` neighbours are asked by the build as a switch, and zsh
  hands git `-C . checkout feature/x`. So "zsh runs as the creation" is half
  the class. bash 3.2 refuses `2>&/dev/null` as an ambiguous redirect, but
  it hands git `{fd}` as a word for `{fd}>&/dev/null`, and git then refuses
  `worktree {fd} add`. Either way nothing runs, so the question is right in
  zsh and costs nothing in bash. Only the record's wording is off.
- **Where it came from.** Round 1's fence for white 2, which the fix pasted
  verbatim. Round 1's prose had "the creation or the switch".
- **Fix.** Fences below.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 5 | the policy still promises silence for a detach carrying a redirection, which C asks when the detach names a commit, and its list of asked file checkouts misses `&>>` before the name, a zsh prefix and a spaced `--config-env` | `docs/worktree-guard-spec.md:628` | open | executed: `switch --detach feature/x` and `checkout --detach feature/x` asked on 226 of 492 shapes each, and through `main()`; `&>>` 2 shapes; `noglob`, `nocorrect`, `repeat 2` and `--config-env` file checkouts asked through `main()`; at the build and at `2b1dcb1f`. Same class as round 1's yellow 1, at the half round 1 did not enumerate |
| ⬜ 6 | the changelog's first bullet promises the same detach silence, and `git checkout -q &>/dev/null` is in none of the three categories it names | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:3` | open | executed: the detach shapes above asked at the build and at `2b1dcb1f`; bash 3.2 hands git `checkout -q`. A correction, not counted in `Needs a fix` |
| ⬜ 7 | the changelog says a string behind a prefix of `--env0-from` or `--quoting-style` is no longer read where no `env` runs it; `env --e -S '…'` still is | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:26` | open | executed: read at the build and at `2b1dcb1f`, refused by macOS `env`; read: GNU takes `-S` as the value. A correction |
| ⬜ 8 | N1 and phase 1 say zsh runs the numbered `>&` shapes as the creation and bash refuses each; zsh runs the `-C` ones before `checkout` or `switch` as a switch, and bash 3.2 hands git `{fd}` | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | open | executed under bash 3.2.57 and zsh 5.9 with a recording `git`; the build asks the `-C` forms as a switch. From round 1's own fence. A correction |
| 🟢 | round 1's yellow 1 is closed for what it named: the five positions are named and asked, and a restore of `.` or a path after `--` is silent | `docs/worktree-guard-spec.md:628` | confirmed | executed: 0 of 388 generated shapes at a named position silent; `checkout .`, `checkout -- README.md` and `checkout feature/x -- README.md` asked on 0 shapes; the residual is finding 5 |
| 🟢 | the two new cases and `HIDDEN_FILE_CHECKOUTS` are correct and were seen red as their docstrings say | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | executed: the mutant `switch_kind` turns 4 of 4 red; the policy assertions fail 3 of 4 against `b4bd4ea1`'s doc; 12 passed at `72c8f5a4` |
| 🟢 | round 1's white 2 is closed: N1 and phase 1 now name the numbered `>&` with a file, which bash refuses and zsh runs | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | confirmed | executed: build against `2b1dcb1f` adds 50 of 380 shapes, drops 0; `2>&` and `3>&` refused by bash 3.2 and run by zsh; the residual wording is finding 8 |
| 🟢 | round 1's white 3 is closed: "never less" is gone from the changelog | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:24` | confirmed | executed: `env --quoti --spl '…'` dropped at the build, refused by macOS `env`; `env -i-S`, `env ---S`, `env --unset -iS` gained and run by macOS `env`; the residual is finding 7 |
| 🟢 | round 1's white 4 is closed: phase 2 says `genv`'s walk reads the two new rows and the shared `-` letter | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/phases/phase-2.md` | confirmed | executed: `genv -i-S` gained and `genv --quoti --spl` dropped against `2b1dcb1f`; read: GNU's `shortopts` carry no `-`; the counts are round 1's, carried |
| 🟢 | K7 and M2 re-read and re-stamped; the ledger reads clean and the survivors are excused | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K7 | confirmed | executed: `evidence-check --strict .` exit 0, 4,049 ok, 0 drifted, 0 broken, 0 names refused; `survivor-check` exit 0, two excused; read: both notes against the diff |
| ❓ | carried from round 1: whether 0.18.0 ships the tree-blind questions `233f0455` never asked (`questions.md` D6) | `questions.md` D6 | ❓ out of verified scope | a decision, not a check; nothing in the fix range changes it. Who answers it: the repository owner |

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

## Paste-ready fixes

### 🟡 5

Replace `docs/worktree-guard-spec.md` lines 628 to 638, from "redirection's
word is never read" through "recorded in this", with the block below. The
line after it, "repository's transcripts on the maintainer's machine …",
stays. The policy case's phrase and its three quoted commands survive the
rewrap.

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

### ⬜ 6

Replace `changelog.md` lines 3 to 12, through "It now also asks about a",
with:

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

### ⬜ 7

Replace `changelog.md` lines 26 to 28, from "runs. A prefix of", with:

```
  runs. A prefix of `--env0-from` or `--quoting-style` now takes the next
  word as its value, as GNU reads it, so an abbreviated split string behind
  one (`env --quoti --spl '…'`) is no longer read where no `env` runs it.
  `-S` and `--split-string` spelt in full are still read wherever they
  stand, as before. `genv` is read as GNU's alone.
```

### ⬜ 8

In N1's Executed cell, replace "which bash refuses as an ambiguous redirect
and zsh runs as the creation (warden round 1)" with:

```
which bash runs nothing for (it refuses a numbered `>&` as an ambiguous redirect, and bash 3.2, which has no `{fd}`, hands git `{fd}` as a word git refuses) and zsh runs as the creation, or as the switch before `-C`'s value with `checkout` or `switch` (warden rounds 1 and 2)
```

In N1's `Corrected 2026-10-03 by round 1's fix pass (white 2)` note, replace
"which bash refuses and zsh 5.9 runs as a creation" with:

```
which bash runs nothing for and zsh 5.9 runs as the creation or, behind `-C`, the switch
```

In `phases/phase-1.md`, replace "bash 3.2 and 5.2 refuse each as an ambiguous
redirect and run nothing; zsh 5.9 runs each as the creation." with:

```
bash runs nothing: 3.2 and 5.2 refuse a numbered `>&` with a file as an
ambiguous redirect, and 3.2, which has no `{fd}`, hands git `{fd}` as a word
git refuses. zsh 5.9 runs each, as the creation, or as the switch where
`checkout` or `switch` follows `-C`'s value.
```

## Regression tests to plant

For 🟡 5, in `tests/test_guard_resolves_the_tree_it_judges.py`, after the
policy case. The function-level case should pass at `72c8f5a4`. Two mutants
of `switch_kind` turn every row red between them: one that returns nothing
when `--detach` is among the words (the three detach rows), and the one
round 1's case was shown red with, which returns nothing for a `checkout`
naming a word holding `.` (the three `README.md` rows). The policy lines
should fail at `72c8f5a4`, where the sentence lacks both, and pass after the
fence above.

```python
DETACH_AND_GIT_HIDDEN = (
    "2>/dev/null git switch --detach feature/x",
    "git switch --detach &>/dev/null feature/x",
    "2>/dev/null git checkout --detach feature/x",
    "git checkout &>>/dev/null README.md",
    "noglob git checkout README.md",
    "git --config-env k=v checkout README.md",
)


@pytest.mark.parametrize("command", DETACH_AND_GIT_HIDDEN)
def test_a_detach_naming_a_commit_and_a_hidden_git_file_checkout_are_asked(
    tmp_path, command
):
    """`docs/worktree-guard-spec.md` §*Which tree*: a detach that names a
    commit moves the tree and is asked as a switch, and a file checkout is
    asked wherever the frozen reader cannot see it, a zsh prefix and a
    spaced `--config-env` included (warden round 2 of #737)."""
    assert wg.wider_only_kinds(command, str(tmp_path)) == {"switch"}, command
```

and at the end of the policy case:

```python
    assert "a detach that names no commit" in text
    for command in (
        "2>/dev/null git switch --detach feature/x",
        "noglob git checkout README.md",
    ):
        assert f"`{command}`" in text, command
```

## Facts for the evidence ledger

- bash 3.2.57 refuses `git worktree 2>&/dev/null add ../wt b` and its `3>&`
  form as an ambiguous redirect, runs `1>&/dev/null` and `>&/dev/null` as
  `worktree add ../wt b`, and hands git `worktree {fd} add ../wt b` for the
  `{fd}>&/dev/null` form. zsh 5.9 hands git `worktree add ../wt b` for all
  of them, and `-C . checkout feature/x` for `git -C 2>&/dev/null . checkout
  feature/x`. Executed on 2026-10-03.
- macOS `/usr/bin/env` refuses `env --e -S '…'` (illegal option `e`) and
  runs `env -i-S '…'`, `env ---S '…'` and `env --unset -iS '…'`. Executed on
  2026-10-03.

## Not verified

| Item | Who must answer |
|---|---|
| bash 4.1 or later on the `&>>` and `{fd}` shapes; I have bash 3.2 only, and round 1's container runs are carried | a reviewer with bash 4.1 or later, if wanted |
| GNU's half against a real GNU `env`; read here, as in round 1 | a reviewer or a CI leg with GNU coreutils 9.12 or later |
| the full suite, lint and typecheck | the sealer, after the rounds settle |

Needs a fix: yes — 🟡 5, the policy sentence in `docs/worktree-guard-spec.md` §*Which tree* that still promises silence for a detach carrying a redirection and omits three hides the guard asks about

Loses a record or crashes: no

## Proof block

Files opened: `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/rounds/round-1.md`,
`rounds/round-1-report.md`, `changelog.md`, `survivors.md`, `overview.md`
(§*Not verified*), `phases/phase-1.md` and `phases/phase-2.md` (the fix
hunks); `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md`
(N1, M2) and
`seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md`
(K5, K7), through the fix diff; `docs/worktree-guard-spec.md` lines 600 to
660; `hooks/worktree-guard.py` (`switch_kind`, `wider_only_kinds`,
`_bare_words`, `walk_command`); `hooks/cmdline.py` (`reparsed_texts`,
`_env_walk`, `ENV_OPTIONS`, `_ENV_SHORT`);
`tests/test_guard_resolves_the_tree_it_judges.py` (`run`,
`_a_dirty_w_under_a_clean_session`, `ZSH_PREFIXED`, `WIDER_ONLY`, the restore
cases, `_redirections`, `RESTORES`, `HIDDEN_FILE_CHECKOUTS` and its two
cases); `bin/test`; `seal/config.md` (no `Record language` row).
