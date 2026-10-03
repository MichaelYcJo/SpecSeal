# Round 3 report — work item 1790993140 (#716, #678's guard half, #686)

| Field | Value |
|---|---|
| Round | 3, verifying, the run's last |
| Target SHA | `a575739f` |
| Fix range | `e74efba8..40214e98` (six commits), then round 2's close commit `a575739f` |
| Earlier rounds | `rounds/round-1.md`, `rounds/round-2.md`, `rounds/round-2-report.md` |
| Ran by | specseal:warden on claude-opus-5-5 |

This round reads round 2's fixes and the units they created, not the branch.
Round 1's and round 2's records were read for coordinates; every verdict below
was re-derived at `a575739f`. The fix pass's account (the commit messages, the
ledger notes, the code comments, and the build's claim in the spawn prompt that
the one surviving mutant is equivalent) was read whole and treated as claims.

## Summary

Round 2's three yellow findings and two white ones are closed as round 2 named
them. Two of the fixes opened new defects in the units they changed, and a
third defect sits under all of them:

1. **🟡 8's fix made restores with a redirection ask "switches a branch"**
   (🟡 13). The fix compares a view with the segments it was made from. A cut
   or merged view carries a redirection word that its segments do not, and
   `switch_kind` reads any word as a branch name. So
   `cd w && git checkout . &>/dev/null` asks the person about a switch. It was
   silent at `233f0455` and at `f1629706`.
2. **`ENV_OPTIONS` misses two rows its own sources have** (🟡 14). BSD's
   getopt has `-` among its letters, as `-i`. Executed: macOS `env -i-S '…'`
   and `env --S '…'` run the string. GNU coreutils 9.12 added `--env0-from`,
   which takes a value. A commit behind any of these is found by nothing.
3. **A checkout whose name carries a redirection is never asked** (🟡 15).
   `git checkout feature/x>/dev/null` and `git checkout 2>/dev/null
   feature/x` switch branches in bash, and the guard says nothing at every
   commit from `233f0455` to `a575739f`. This is not a regression: the frozen
   `classify` looks the redirection up as part of the name, and C reads the
   name tree-blind, so it calls the switch already seen.

The build's claim that the mutant "merged group compared to itself" is
equivalent is false (⬜ 16). On `git switch &>/dev/null feature/x` the built C
asks and the mutant is silent. No case pins that shape.

The fences for 🟡 13 and 🟡 14 were applied together in the round's clone.
The two touched modules pass with them (793 passed), the new cases fail at
`a575739f` (18 failed), and the fixed C fires on 0 of the 27,351 corpus pairs,
the same as the built C.

## Round 2's fixes, each at its commit

- **🟡 8, `07b67ac3` — confirmed for the shapes it named.** Executed through
  `main()`: `git switch>/dev/null feature/x`, `git checkout>/dev/null -b y`
  and `git worktree add>/dev/null ../wt b` ask at `a575739f` and are silent at
  `f1629706`. The comparison the fix introduced is 🟡 13.
- **🟡 9, `49f27f09` and `043f3153` — confirmed.** Executed through
  `commit_invocations`: `env --un FOO -iS "$CMD"` is found at `a575739f` and
  found by nothing at `f1629706`. The three abbreviation shapes in `HANDED`
  pass. GNU env is not installed, so getopt's prefix rule is read, not run.
- **🟡 10, `49f27f09` — confirmed.** Executed: `env -u FOO 2>/dev/null -iS
  'git commit -m x'` is found and denied in a declared repository at
  `a575739f`; it was found by nothing at `f1629706` and `233f0455`.
- **⬜ 11, `49f27f09` — confirmed.** Executed: `env -- -iS 'git commit -m y'`
  is silent in a declared repository at `a575739f`, as at `233f0455`; it was a
  deny at `f1629706`. macOS `env -- -S 'echo x'` tries to run a program named
  `-S` (exit 127), so `--` ends the options there too.
- **⬜ 12, `aa3bbf21` — answered.** Read: both rows of `overview.md` are round
  2's fence in substance. The `env -S` row repeats the "one table built from
  both synopses" claim that 🟡 14 shows is short two rows, so it drifts with
  that fix.
- **Round 1's findings** carry forward as round 2 confirmed them. Round 1's
  finding 4 is still deferred to #734: `ask_what_only_the_wider_reading_finds`
  has no diff in `e74efba8..a575739f` (read).

## 🟡 13 — a redirection word is read as a branch name, and restores now ask

`hooks/worktree-guard.py:364` (`wider_only_kinds`, the loop over `sourced`).

**What is wrong.** Neither `parse_git` takes a redirection out of the
arguments. `switch_kind` then counts every argument that does not start with
`-` as a name. Before 🟡 8's fix, a cut or merged view was compared with the
frozen parser reading the same tokens, so the redirection word stood on both
sides and cancelled out. Since `07b67ac3` the frozen side reads the source
segments, which do not carry that word:

- `git checkout . &>/dev/null`: the splitter cuts at `&`, and `merged_view`
  glues back `git checkout . &>/dev/null`. Its kind is `switch` (the name is
  `&>/dev/null`). The parts read `None`.
- `git switch --detach>/dev/null`: `unglued` cuts the word into `--detach`
  and `>/dev/null`. The cut view reads `switch`, while the raw segment reads
  `None`.

**Executed.** Through `main()`, over a dirty `w` and a clean tree alike:

| Command | `233f0455` | `07a3dc7f` | `f1629706` | `a575739f` |
|---|---|---|---|---|
| `cd w && git checkout . &>/dev/null` | silent | ask | silent | **ask** |
| `cd w && git checkout .&>/dev/null` | silent | ask | silent | **ask** |
| `cd w && git checkout -q &>/dev/null` | silent | ask | silent | **ask** |
| `cd w && git switch --detach &>/dev/null` | silent | ask | silent | **ask** |
| `cd w && git switch --detach>/dev/null` | silent | ask | silent | **ask** |
| `cd clean && git checkout . &>/dev/null` | silent | ask | silent | **ask** |
| `cd w && git checkout README.md &>/dev/null` | silent | silent | silent | silent |

Bash, in a scratch repository: `git checkout . &>/dev/null` restored
`README.md` and stayed on `main`; `git checkout -q &>/dev/null` stayed on
`main`. The question says "This command switches a branch", which is false
for each of them. Over 854 generated shapes (seven git verbs, eleven
redirections, each position, glued and spaced), the fixed C below drops 114
asks, every one on `checkout .`, `checkout -- f` or `switch --detach`, and adds
18, every one a `git worktree <redirection> add`, which bash runs as a
creation.

**Why it matters.** `docs/worktree-guard-spec.md` says the wider reading
replaces only silences, and the base was silent on every row above. Each ask
stops an unattended run on a restore. The owner's count does not see it,
because no recorded pair has these shapes (the corpus re-count is 0 for both
codes). Round 1's original build asked these too; round 1's fix silenced them
by accident, and round 2's fix brought them back.

**Fix.** Read each view as the program is handed it: a glued redirection cut
off, then every redirection taken out, before `switch_kind`. `unglued` cuts
`.&>f` at `>` and leaves `&` on the word, while bash ends the word at `&>`, so
that `&` goes too. This one reading replaces the view and its cut view. Fenced
below. Executed with the fence: the two touched modules pass, the corpus count
stays 0 of 27,351, and every shape in the table above is silent.

## 🟡 14 — `ENV_OPTIONS` misses BSD's `-` and GNU's `--env0-from`

`hooks/cmdline.py:1783` (`ENV_OPTIONS`) and `hooks/cmdline.py:1831`
(`_env_option`'s long-name arm).

**What the table was held against.**

- GNU coreutils, `src/env.c` on its master branch (read): `shortopts` is
  `"+a:C:iS:u:v0"` plus the whitespace characters. `longopts` has `argv0`,
  `ignore-environment`, `env0-from` (required), `null`, `unset`, `chdir`,
  `default-signal`, `ignore-signal`, `block-signal` (each optional),
  `list-signal-handling`, `debug`, `quoting-style` (required), `split-string`,
  `help` and `version`. Its NEWS dates `--argv0` to 9.5, `--env0-from` to
  9.12 (2026-09-14, the latest release), and `--quoting-style` to the
  unreleased section. A whitespace letter is an error that runs nothing.
  After getopt, a lone `-` sets `-i` and is consumed, and getopt has already
  stopped at it.
- FreeBSD, `usr.bin/env/env.c` (read): `getopt` with `"-0C:iL:P:S:U:u:v"`, and
  `case '-':` shares `case 'i':`.
- macOS env(1) on this machine (read), and macOS `env` itself (executed).

Every row the table has is right, and so is the unambiguous-prefix rule:
`--i` and `--d` are ambiguous in GNU, and `--e` would name `--env0-from`
alone. A redirection anywhere among the options, `--`, and a value pending
across a redirection all behave as the fixes say (executed through the
cases). Two rows are missing.

**BSD's `-` letter.** Executed on macOS:

- `env -i-S 'echo ran-i-dash-S'` printed `ran-i-dash-S`.
- `env -v-S 'echo …'` printed the debug lines and ran `echo`.
- `env --S 'echo dd'` printed `dd`: BSD's getopt ends at `--` alone and reads
  `--S` as the letters `-` and `S`.

In `_env_option`, `-` is an unknown letter, so the cluster is refused. `--S`
takes the long-name arm, names no long option and is read as a flag.

**GNU's `--env0-from`.** Read, not run: GNU env is not installed. An unknown
long name is read as a flag, so its value `f` ends env's own options.

**Executed** through `commit_invocations` and `main()` in a declared
repository. Each is found by nothing and silent at `233f0455`, `f1629706` and
`a575739f`:

- `env -i-S 'git commit -m x'`
- `env -v-S 'git commit -m x'`
- `env --S 'git commit -m x'`
- `env -u FOO --S 'git commit -m x'`
- `env --env0-from f -iS 'git commit -m x'`

**Why it matters.** Contract §12: this is round 2's 🟡 9 and 🟡 10 class, a
spelling env's getopt accepts that the reader does not parse. With `-i` in
the cluster, the git hook stub sees no session either (`spec.md`'s table,
y09), so a commit runs that no gate judges. The table's comment, K3 and E14
each say it holds every option of both synopses. It is a unit round 2's fixes
created, so it is the branch's to fix.

**Also read.** The comment says a lone `-` is `-i` in both synopses, and the
walk keeps reading options after it. For GNU that is half true: getopt has
stopped at the `-`, so in `env - -iS 'git commit -m y'` the program is `-iS`.
Executed: this shape is a deny in a declared repository at `a575739f` and was
silent at `233f0455`. macOS runs the commit, because BSD reads `-` as an
option and keeps going. The stop is right on macOS, and it is ⬜ 11's kind on
GNU (no real program is called `-iS`). The fence rewords the comment.

**Fix.** Add `--env0-from` as a required row, give `-` a short entry with no
value, and read a `--` word that names no long option as a BSD cluster.
`--quoting-style` is not added, because no release has it yet. Fenced below.

## 🟡 15 — a checkout whose name carries a redirection is never asked

`hooks/worktree-guard.py:364` (`wider_only_kinds`), against
`hooks/worktree-guard.py:756` (`classify`'s first positional).

**What is wrong.** `classify` looks the first positional up as a ref, and
that word still holds the redirection: `feature/x>/dev/null`, or
`2>/dev/null` itself when the redirection stands before the name. So the
frozen loop judges no switch. C reads the same segment tree-blind, and
`switch_kind` calls it a switch, so the kind is in the frozen set and is
subtracted. Neither reading ever looks up `feature/x`.

**Executed.** Bash, in a scratch repository: `git checkout feature/x>/dev/null`
and `git checkout 2>/dev/null feature/x` each left the repository on
`feature/x`. Through `main()` over a dirty `w`, each of these is silent at
`233f0455`, `07a3dc7f`, `f1629706` and `a575739f`:

- `cd w && git checkout feature/x>/dev/null`
- `cd w && git checkout feature/x>&2`
- `cd w && git checkout 2>/dev/null feature/x`
- `cd w && git checkout -q 2>/dev/null feature/x`

`git checkout feature/x 2>/dev/null` and `git switch feature/x>/dev/null` are
judged by the frozen loop and ask.

**Why it matters, and why it is not a regression.** C's question names "a git
behind a redirection", and these are switches over a dirty tree that run
unasked. But the base shipped the same silence. The frozen `classify` is
`86256492`'s by construction (#689), and D3 has C count a checkout's name
tree-blind. Under that rule, the frozen reading "finds" this switch, so C is
doing what K5 says. It is round 1's 🟡 3 mechanism (`classify` judges fewer
than `switch_kind`) inside one view rather than across two.

**Fix.** A tree-blind fence is below: ask where a checkout's name, with its
redirection taken off, is a word no source segment's checkout names. It goes
on top of 🟡 13's fence. Executed with it: the four shapes above ask, the
corpus count stays 0 of 27,351, and the guard module passes except one case.
That case is the trade: `cd w && git checkout README.md>/dev/null`, a glued
restore, asks too, because only a tree can tell `README.md` from `feature/x`.
A tree-aware fix needs each segment's directory inside C, which C does not
have. I judge this answerable with grounds and fit for a deferral, not a fix
this capped run has to make.

## ⬜ 16 — the merged-group mutant is not equivalent

The spawn prompt carries the build's claim that the one surviving mutant,
"merged group compared to itself", is equivalent. It is not. Executed at
function level: on 32 of 854 generated shapes the built C and the mutant
differ, and on each the mutant is the silent one:

- `git switch &>/dev/null feature/x`
- `git checkout &>/dev/null -b y`
- `git checkout &>/dev/null feature/x`

The splitter cuts `&>` at `&`. The merged view is the only one holding the
switch, and the frozen parser reads the same switch from the glued group but
not from either part. Bash runs each, executed for the checkout one. Through
`main()`, `cd w && git switch &>/dev/null feature/x` asks at `a575739f`, was
silent at `f1629706`, and asked at `07a3dc7f`.

The code is right. The mutant survives because no case has an `&>` between
the subcommand and its name. The fence under 🟡 13 adds two, and with them
the mutant is killed (read from the function-level result; the mutant was not
re-run through pytest). This is ⬜ because the release ships no defect while
it stands.

## ⬜ 17 — K3 and E14 say the table holds every option of both synopses

`seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md`
K3 and `seal/releases/0.16.0.md` E14. K3's corrected clause says the table
covers "every option GNU coreutils env's and BSD/macOS env's synopses give".
E14's round 2 re-read note says "one table of both synopses' options". 🟡 14
shows two rows missing. Both should be re-read and corrected with 🟡 14's
fix. This is paperwork, outside `Needs a fix`.

## The ledger

- **K3 and K5** are corrected in place. Each describes `a575739f`'s code,
  apart from K3's "every option" (⬜ 17; read). K5's clause, *a view whose
  kind the frozen parser reads from one of the segments the view was made
  from*, is what 🟡 13's fix narrows. Its anchor drifts with that fix.
- **E14, I6, E16 and I5** were re-read at `a575739f` (read, word by word
  against `e74efba8`). Only the anchor hashes and one dated note in each
  changed. E16 and I5 count three new no-commit `CONTROLS`, and the diff adds
  three: two after `--`, one with a letter no synopsis has. I6 names only the
  env arm as changed, which matches the diff. E14's claim stands, and its note
  repeats K3's overclaim.
- **Executed:** `bin/evidence-check --ledger` on the fragment and on
  `seal/releases/0.16.0.md`, `0.15.6.md`, `0.15.5.md` and `0.9.1.md`: 0
  drifted and 0 broken in each.
- **`survivors.md`'s two new rows hold.** Executed: `bin/survivor-check
  --range e74efba8..a575739f` names exactly two places, both case docstrings
  in `tests/test_guard_resolves_the_tree_it_judges.py` that cite round 1's
  yellow 3. With the work item's `survivors.md` as `--exempt`, it passes
  (exit 0). Each docstring still pins the finding it cites (read).

## Whether a silent `env` line now stops, or a stopped shape goes silent

Executed through `main()` in a declared repository, at `233f0455`,
`f1629706` and `a575739f`:

- **Silent at the base, a deny now:** `env -iS "$CMD"`, `env --un FOO -iS
  "$CMD"`, `env 2>/dev/null -iS "$CMD"` and `env -u 2>/dev/null FOO -iS
  "$CMD"`. Each hands env an unreadable string through a spelling the branch
  now reads. `env -S "$CMD"` was a deny at the base, so these take the base's
  answer for the same string. That is the class working, not a new kind of
  stop. `env - -iS 'git commit -m y'` is covered under 🟡 14.
- **Silent at all three:** `env -C /tmp 2>/dev/null ls`, `env -u FOO
  2>/dev/null -vS "echo $X"`, and `env -- -iS 'git commit -m y'`.
- **No stopped `env` shape went silent.** `env -S "$CMD"` and `env
  2>/dev/null -i PATH="$P" sh -c "$X"` deny at all three.
- **In the guard,** the only shapes that go from asked to silent are among
  round 1's target's false asks, which `f1629706` had already silenced.
  Nothing `233f0455` asked can go silent, because C runs only at the guard's
  silent exits.

## The owner's count

The built C is round 2's fence, line for line (read: `07b67ac3` against the
fence in `round-2-report.md`). The count did not have to be repeated, and it
was repeated anyway, because the fences below change C. Executed over D1's
cut, re-derived from the transcripts: 27,351 distinct pairs, none raised. The
built C fires on 0, 🟡 13's fence on 0, and 🟡 15's fence on 0. The pairs
match round 2's count.

## Regression tests to plant

All are fenced under *Paste-ready fixes*. Each new case was seen to fail at
`a575739f` (contract §15), 18 failed in all, apart from the two `&>` entries
under ⬜ 16, which pass at `a575739f` and are there to kill the mutant:

- `tests/test_guard_resolves_the_tree_it_judges.py`: the parametrized case
  for 🟡 13's six false asks, failing on all six. In `WIDER_ONLY`, the
  `git worktree 2>/dev/null add` creation, failing twice, and the two `&>`
  switches.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`:
  four `HANDED` shapes, each failing in `test_the_gate_stops_it` and in
  `test_a_commit_in_a_string_or_a_substitution_is_read_as_unreadable`. An
  `ENV_SPELLINGS` row for `--env0-from`, which fails in
  `test_a_cluster_behind_env_s_own_options_is_read` and in the row-coverage
  case once the table row exists.

## Facts for the evidence ledger

- K5 drifts with 🟡 13's fix. A view's kind is read from its words with every
  redirection taken off, a glued one cut first, and is hidden only where no
  segment it was made from reads that kind.
- K3 drifts with 🟡 14's fix, and E14's note with it. The table holds GNU
  coreutils 9.12's options (`--env0-from` included) and FreeBSD's, with BSD's
  `-` read as `-i` inside a cluster and in a `--` word that names no long
  option. Executed 2026-10-03 on macOS: `env -i-S` and `env --S` run the
  string.
- Over D1's corpus, C with 🟡 13's fence fires on 0 of 27,351 pairs, executed
  2026-10-03, round 3. It re-runs K5's measurement, and needs no new anchor.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 13 | 🟡 8's fix compares a cut or merged view with segments that lack its redirection word, which `switch_kind` reads as a branch name, so `git checkout . &>/dev/null` and other non-switch shapes ask "switches a branch" | `hooks/worktree-guard.py:364` | open | executed: six shapes silent at `233f0455` and `f1629706`, ask at `a575739f`; bash runs each without switching; the fence passes the two modules and fires on 0 of 27,351 pairs |
| 🟡 14 | `ENV_OPTIONS` misses BSD's `-` letter and GNU 9.12's `--env0-from`, so `env -i-S`, `env --S` and `env --env0-from f -iS` hide a commit from every reading | `hooks/cmdline.py:1783` | open | executed: macOS `env -i-S`, `-v-S` and `--S` run the string, and five shapes are found by nothing at three commits; read: GNU's and FreeBSD's sources |
| 🟡 15 | a checkout whose name carries a redirection (`git checkout feature/x>/dev/null`, `git checkout 2>/dev/null feature/x`) switches unasked, because `classify` looks the redirection up as part of the name and C reads the name tree-blind | `hooks/worktree-guard.py:364` | open | executed: bash switches; silent through `main()` at `233f0455`, `07a3dc7f`, `f1629706` and `a575739f`; not a regression; a tree-blind fence asks on a glued restore too |
| ⬜ 16 | the merged-group mutant the build calls equivalent is not: it silences `git switch &>/dev/null feature/x`, and no case pins an `&>` before the name | `hooks/worktree-guard.py:361` | open | executed at function level: 32 of 854 shapes differ, the mutant silent on each; the code is right |
| ⬜ 17 | K3's corrected clause and E14's round 2 note say the table holds every option of both synopses | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K3 | open | read; paperwork correction, outside `Needs a fix`; drifts with 🟡 14's fix |
| 🟢 | round 2's finding 8 is closed for the shapes it named — a redirection glued to the subcommand is asked again | `hooks/worktree-guard.py:364` | confirmed | executed: the three glued shapes ask at `a575739f` and are silent at `f1629706`; the comparison it introduced is this round's finding 13 |
| 🟢 | round 2's finding 9 is closed — an abbreviated long option's value no longer ends env's own options | `hooks/cmdline.py:1813` | confirmed | executed: `env --un FOO -iS` is found at `a575739f`, by nothing at `f1629706`; the abbreviation cases pass; GNU env read, not run |
| 🟢 | round 2's finding 10 is closed — a redirection among env's options is read past | `hooks/cmdline.py:1742` | confirmed | executed: `env -u FOO 2>/dev/null -iS 'git commit -m x'` is found and denied at `a575739f`, found by nothing at `f1629706` |
| 🟢 | round 2's finding 11 is closed — `--` ends env's options | `hooks/cmdline.py:1749` | confirmed | executed: `env -- -iS 'git commit -m y'` is silent in a declared repository at `a575739f` and `233f0455`, a deny at `f1629706` |
| 🟢 | round 2's finding 12 is closed — `overview.md`'s two rows describe the code | `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/overview.md` | answered | read: round 2's fence in substance; the env row's "one table" claim drifts with finding 14 |
| 🟢 | round 1's finding 4 stays deferred — the fix range does not touch the consent read | `hooks/worktree-guard.py:373` | deferred #734 | already deferred in round 1; read: no diff to `ask_what_only_the_wider_reading_finds` in `e74efba8..a575739f` |
| 🟢 | the ledger rows round 2's fixes drifted hold — K3 and K5 corrected, E14, I6, E16 and I5 re-read, two `survivors.md` rows | `seal/releases/0.16.0.md`, `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/survivors.md` | confirmed | executed: evidence-check 0 drifted, 0 broken on five ledger files; survivor-check names two places and passes with the exemption; read: each row against the diff, apart from finding 17 |

## Executed probes

| What was run | Result |
|---|---|
| Narrow run at `a575739f`: the guard and wrapper modules | 768 passed |
| `main()` over three sets of guard shapes at `233f0455`, `07a3dc7f`, `f1629706` and `a575739f`, dirty `w` under a clean session | 🟡 13: six shapes silent, ask, silent, ask; 🟡 15: four shapes silent at all four; round 2's glued shapes ask at `a575739f` only |
| Candidate C as built, the merged-self mutant and `f1629706`'s rule, at function level, over 854 generated shapes | built and mutant differ on 32, the mutant silent on each; built asks where `f1629706` did not on 82 |
| Bash in a scratch repository: the checkout shapes of 🟡 13, 🟡 15 and ⬜ 16 | glued and spaced-before names switch; `checkout . &>/dev/null` restores and stays on `main` |
| macOS `env -i-S`, `env -v-S`, `env --S`, `env - -S`, `env -- -S`, `env -x` | the first four run the string; `--` makes `-S` the program (exit 127); `-x` is refused |
| 20 `env` shapes through `commit_invocations` and `main()` in a declared repository, at `233f0455`, `f1629706` and `a575739f` | five commit shapes found by nothing at all three (🟡 14); four `"$CMD"` shapes newly denied, as `env -S "$CMD"` was at the base; no stopped shape went silent |
| Corpus count over D1's cut: built C, 🟡 13's fence, 🟡 15's fence | 27,351 pairs, none raised; 0, 0 and 0 |
| 🟡 13's and 🟡 14's fences applied in the round's clone, then the two modules | 793 passed; `ruff check` clean; `ruff format` reflows two lines, already reflowed in the fences |
| The new cases against `a575739f`'s hooks | 18 failed, 775 passed |
| 🟡 15's fence on top, then the guard module | 124 passed, 1 failed: the glued restore, the trade named under 🟡 15 |
| `bin/evidence-check --ledger` on the fragment and four release files | 0 drifted, 0 broken in each |
| `bin/survivor-check --range e74efba8..a575739f`, with and without `survivors.md` | passes with it; without, two places, both round 1 yellow 3 citations |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet: the sealer's, after the rounds settle |

The probe files, the trees extracted at three earlier commits, the scratch
repositories and the round's clone were deleted before hand-over.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 15, a checkout whose name carries a redirection switches unasked; a tree-aware C needs each segment's directory | proposed: a new issue beside #686 and #734, if the orchestrator does not take the fence | the orchestrator, then the owner, who decided D3's tree-blind count |

## Paste-ready fixes

### 🟡 13 — read a view as the program is handed it

```python
# hooks/worktree-guard.py, wider_only_kinds: the loop over `sourced`
    wider = set()
    for view, sources in sourced:
        frozen = {switch_kind(parse_git(tokens)) for tokens in sources}
        # The view as the program reads it: a cut or merged view carries a
        # redirection word its segments do not, and `switch_kind` reads any
        # word as a name, so `git checkout . &>/dev/null` read as a switch
        # (round 3 of 1790993140).
        kind = switch_kind(wide.parse_git(_bare_words(view)))
        if kind and kind not in frozen:
            wider.add(kind)
    return wider - set(judged)


def _bare_words(tokens):
    """TOKENS with a redirection glued to a word's end cut off, and every
    redirection taken out: the words the program is handed."""
    cut = wide.unglued(tokens) or list(tokens)
    # `unglued` cuts `.&>f` at `>`, and bash ends the word at `&>`.
    cut = [
        t[:-1]
        if t.endswith("&") and i + 1 < len(cut) and cut[i + 1].startswith(">")
        else t
        for i, t in enumerate(cut)
    ]
    return wide._without_redirections([t for t in cut if t])
```

```python
# hooks/worktree-guard.py, wider_only_kinds' docstring: replace "The wider
# reading is its splitter's segments, `merged_view`'s groups and the words a
# redirection glued to a word's end, each read by its `parse_git`" with:
    The wider reading is its splitter's segments and `merged_view`'s groups,
    each read by its `parse_git` with every redirection taken off, a glued
    one cut first, so a redirection word is never read as a branch name
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py, WIDER_ONLY, after
# "a redirection glued to add"
    # Round 3 of 1790993140: bash runs each; the splitter cuts `&>` at `&`,
    # and only the merged view holds the switch. The mutant comparing the
    # merged view with itself is silent on both.
    "&> between switch and its name": (
        "cd w && git switch &>/dev/null feature/x",
        "switch",
    ),
    "&> between checkout and its name": (
        "cd w && git checkout &>/dev/null feature/x",
        "switch",
    ),
    # A redirection between `worktree` and `add`: silent at `a575739f`.
    "a redirection between worktree and add": (
        "cd w && git worktree 2>/dev/null add ../wt b",
        "creation",
    ),
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py, before
# test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it
@pytest.mark.parametrize(
    "command",
    [
        "cd w && git checkout . &>/dev/null",
        "cd w && git checkout .&>/dev/null",
        "cd w && git checkout -q &>/dev/null",
        "cd w && git switch --detach &>/dev/null",
        "cd w && git switch --detach>/dev/null",
        "cd w && git checkout>/dev/null .",
    ],
)
def test_a_redirection_word_is_not_read_as_a_branch_name(
    monkeypatch, capsys, repo, tmp_path, command
):
    """Round 3 of 1790993140. A cut or merged view carries the redirection
    word its segment does not, and `switch_kind` reads any word as a name.
    Each asked at `a575739f`, and was silent at `f1629706`."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, _ = run(monkeypatch, capsys, command, session)
    assert decision == "silent", (command, decision, reason)
```

### 🟡 14 — the two rows, and BSD's reading of a `--` word

```python
# hooks/cmdline.py, ENV_OPTIONS: after the --list-signal-handling row
    (None, "--env0-from", "required"),
```

```python
# hooks/cmdline.py, after ENV_OPTIONS: replace the _ENV_SHORT line
_ENV_SHORT = {short: value for short, _long, value in ENV_OPTIONS if short}
# BSD's getopt has `-` among its letters, as `-i`: `env -i-S '…'` and `env
# --S '…'` run the string on macOS (executed, round 3 of 1790993140).
_ENV_SHORT["-"] = None
```

```python
# hooks/cmdline.py, the comment above ENV_OPTIONS: replace the sentence on a
# lone `-` with
# What the table does not need a row for: a lone `-`, which GNU takes as `-i`
# and the end of the options, and BSD as `-i` among them; the walk reads it as
# one of env's own options, which costs a stop only where GNU's program is
# named like an option. And `--`, which ends them. BSD's `-` inside a word is
# `_ENV_SHORT`'s, below the table.
```

```python
# hooks/cmdline.py, _env_option: replace the long-name arm
    if t.startswith("--"):
        name, eq, attached = t.partition("=")
        long = _env_long(name, own)
        if long is not None or not own or t == "--":
            value = _ENV_LONG.get(long)
            if value == ENV_STRING:
                return (("here", attached) if eq else ("next", None)), False
            return None, own and value == "required" and not eq
        # No GNU long name: BSD's getopt reads the word as a cluster whose
        # first letter is `-`, so `--S` is `-i -S` there.
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# HANDED, after "env -vS behind a cut redirection"
    # Round 3 of 1790993140: BSD's getopt reads `-` as `-i`, inside a cluster
    # and as the first letter of a word no GNU long name matches; macOS `env`
    # runs each string (executed). Each found nothing at `a575739f`.
    "env -i-S": f"env -i-S '{C}'",
    "env --S": f"env --S '{C}'",
    "env --S behind an option's value": f"env -u FOO --S '{C}'",
    # GNU coreutils 9.12's `--env0-from` takes a value (read, not run).
    "env -iS behind --env0-from's value": f"env --env0-from f -iS '{C}'",
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# ENV_SPELLINGS, after "--argv0"
    "--env0-from": "--env0-from f",
```

### 🟡 15 — a checkout's name with its redirection taken off (on top of 🟡 13)

```python
# hooks/worktree-guard.py, wider_only_kinds: replace 🟡 13's three lines
# from `kind = …` with
        parsed = wide.parse_git(_bare_words(view))
        kind = switch_kind(parsed)
        if kind and (kind not in frozen or _names_anew(parsed, sources)):
            wider.add(kind)


def _names_anew(parsed, sources):
    """True where a checkout's name, its redirection taken off, is a word no
    source segment's checkout names: `classify` looked `feature>/dev/null`
    up as a ref, and only the bare `feature` is one. Tree-blind, so a glued
    restore (`git checkout README.md>/dev/null`) is asked too."""
    if not parsed or parsed[0] != "checkout":
        return False
    names = [a for a in parsed[1] if not a.startswith("-")]
    if not names or names[0] == ".":
        return False
    for tokens in sources:
        theirs = parse_git(tokens)
        if theirs and theirs[0] == "checkout":
            words = [a for a in theirs[1] if not a.startswith("-")]
            if words[:1] == names[:1]:
                return False
    return True
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py, WIDER_ONLY
    # Round 3 of 1790993140, yellow 15: `classify` looks the redirection up
    # as part of the name. bash switches each (executed); silent at every
    # commit from `233f0455` to `a575739f`.
    "a redirection glued to checkout's name": (
        "cd w && git checkout feature/x>/dev/null",
        "switch",
    ),
    "a redirection before checkout's name": (
        "cd w && git checkout 2>/dev/null feature/x",
        "switch",
    ),
```

Needs a fix: yes — 🟡 13 (a redirection word read as a branch name makes `git checkout . &>/dev/null` ask "switches a branch", silent at the base and at `f1629706`) and 🟡 14 (`ENV_OPTIONS` misses BSD's `-` and GNU 9.12's `--env0-from`, so a commit behind `env -i-S` or `env --S` is found by nothing); 🟡 15 is a silence the base shipped too, which I judge answerable with grounds and deferrable

Loses a record or crashes: no

The broad gate has not come due: two findings need a fix first, and the run
is capped.

## Proof block

Files opened in this round:

- `hooks/worktree-guard.py` at `a575739f`: the import block, `walk_command`,
  `switch_kind`, `wider_only_kinds`, `ask_what_only_the_wider_reading_finds`,
  `classify`, and `main`'s loop and `quiet`. Also the copies at `233f0455`,
  `07a3dc7f` and `f1629706`, run beside it.
- `hooks/cmdline.py` at `a575739f`: `redirection_width`, `unglued`,
  `split_segments`, `split_segments_with_separators`, `merged_view`,
  `merged_segments`, `reparsed_texts`, `ENV_STRING`, `ENV_OPTIONS`,
  `_env_long`, `_env_option`, `_env_words`, `_without_redirections`.
  `hooks/cmdline_base.py`: a source comparison of the splitter, `drop_comments` and
  `drop_heredoc_bodies` with `hooks/cmdline.py`'s.
- `tests/test_guard_resolves_the_tree_it_judges.py` (`run`,
  `_a_dirty_w_under_a_clean_session`, `WIDER_ONLY` and the candidate C cases),
  `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`
  (`HANDED`, `CONTROLS`, `found`, the env grammar cases),
  `tests/conftest.py` (`repo`), `tests/test_no_real_identifiers.py`.
- The fix range's diff of the hooks, the tests, the ledger fragment,
  `seal/releases/0.16.0.md`, `survivors.md` and `overview.md`; the full K3,
  K5, E14, E16, I5 and I6 rows.
- The work item's `rounds/round-1.md`, `rounds/round-2.md`,
  `rounds/round-2-report.md`, `phases/phase-3.md` and `questions.md` (D1, D3).
- macOS env(1) on this machine; GNU coreutils' `src/env.c` and NEWS, and
  FreeBSD's `usr.bin/env/env.c`, fetched read-only.
- `.github/scripts/run_tests.py`.
