# Implementation Plan: 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

The work has three parts.

- **Candidate C.** Read each of C's views with every redirection taken off,
  so a redirection word is never read as a branch name.
- **The two `&>` cases**, so the merged-self mutant is killed through
  pytest.
- **`env`'s two grammars.** Read env's words under GNU's grammar and under
  BSD's, and keep every string either finds.

The paste-ready fences in #733's round-3 report are where each change starts.
Each change is held to a comparison over generated shapes, not to a list of
examples, because a list of examples is what let each earlier fence miss the
shapes next to the ones it named.

## Technical context

Every coordinate below was read at `2b1dcb1f`. The two hooks files are
byte-identical to `a575739f`, round 3's target (`git diff --stat a575739f
2b1dcb1f -- hooks/` touches neither).

- **`hooks/worktree-guard.py#wider_only_kinds`.** The loop at its end reads
  each view `v` as `wide.parse_git(v)` and as `wide.parse_git(wide.unglued(v))`.
  It hides a kind the frozen parser reads from one of `v`'s source segments.
  The frozen side, `switch_kind(parse_git(tokens))` over the sources, does
  not change.
- **`hooks/worktree-guard.py#switch_kind`.** Every argument that does not
  start with `-` counts as a name, other than `.` for `checkout`. That rule is
  correct for a word bash hands git, and it is what turns a redirection word
  into a name. So the fix is to the words handed to it, not to
  `switch_kind`.
- **`hooks/cmdline.py`.**
  - `_REDIRECTION` is at the top of the module. Its alternation is the
    operator list S4's generator is derived from.
  - `redirection_width` and `unglued` follow it. `unglued` cuts at the first
    `<` or `>` and leaves an `&` on the word before it. Bash ends a word at
    `&>`, so the `&` must go too. The fence does that.
  - `merged_view` glues back the groups the splitter cut at `&`, `|` or `;`
    inside a redirection.
  - `_without_redirections` removes every redirection, a spaced target with
    its operator.
- **`hooks/cmdline.py#reparsed_texts`**, the env arm (`elif word in ("env",
  "genv")`). It walks env's words with OWN, VALUE and SKIP. It reads
  `_env_option(t, own and not value)`. It keeps the base's rule: an
  unabbreviated `-S` or `--split-string` is read anywhere, even as another
  option's value.
- **`hooks/cmdline.py#_env_option`.** Its long arm reads a `--word` through
  `_env_long`. An unknown or ambiguous name is read as a flag, and the walk
  goes on, which is a deliberate over-read. Its short arm reads a cluster
  letter by letter. An unknown letter is refused with `(None, False)`, and
  the walk also goes on.
- **The tests.**
  - `tests/test_guard_resolves_the_tree_it_judges.py`: `WIDER_ONLY`,
    `run`, `_a_dirty_w_under_a_clean_session`, `KINDS`.
  - `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`:
    `HANDED`, `CONTROLS`, `ENV_SPELLINGS`, `ENV_GRAMMAR`,
    `test_every_row_of_the_env_grammar_has_a_case`.

**What breaks in six months.**

- **C.** The risk is a redirection operator the reader learns later, which
  `_bare_words` does not take off. S4's generator is derived from
  `_REDIRECTION`, so that operator becomes a new case, and it fails the day
  it is added.
- **env.** The risk is a third grammar: a BusyBox or a future GNU option
  whose value swallows a word. The table names its two sources by file and
  commit. The next reader re-derives from those files, not from a synopsis,
  and the comment says so.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| C1 — the round-3 fence for 🟡 13: one reading per view, a glued redirection cut, the `&` that `unglued` leaves taken off, then every redirection taken out | Its named shapes passed in the reviewer's clone. Its neighbours are unproven, and that is the failure three rounds share. So it is held to S4 and S5 before it is kept | **chosen**, under S4 and S5 |
| C2 — keep the two readings (raw view and `unglued` view) and take redirections out of each | The raw view of `git checkout . &>/dev/null` still holds `&>/dev/null` until it is taken out. The `unglued` view of `.&>/dev/null` holds `.&`, which `switch_kind` reads as a name. The `&` trim is needed either way, and two readings of one view are two places to keep in step | rejected |
| C3 — C1 plus #738's `_names_anew` | `cd w && git checkout README.md>/dev/null` asks *switches a branch* (the round-3 report's own run, 124 passed and 1 failed). That is a restore asked about, 🟡 13's class, inside the work item that removes it | rejected (Q2) |
| E1 — the round-3 fence for 🟡 14: `-` as a short letter, `--env0-from` added, and a `--word` read as a BSD cluster only where it names no GNU long option | `env --unset -iS 'git commit -m x'` and `env --un -vS '…'` run the commit on macOS (executed with `echo`, 2026-10-03). BSD reads `--unset` as `-i -u nset`. The fence reads it as GNU's `--unset`, takes `-iS` as its value, and finds nothing | rejected |
| E2 — two walks over env's words, one per grammar, with the texts unioned. GNU: a `--word` is a long name. BSD (for `env` only): a `--word` other than `--` is a cluster led by `-`. The merged short table and everything else stay as #733 built them | It finds everything E1 finds, because the GNU walk is E1's long arm and the BSD walk takes E1's fallback for every `--word`. On top of that it finds the `--u…` shapes. Cost: one more pass over a handful of words, and a dedupe | **chosen** (decision E) |
| E3 — two strict getopt emulations, stopping at the first error as env does | It removes #733's settled over-reads: an unknown long name read as a flag, a lone `-` read as an option, a refused letter walked past. Each costs a stop only where no env runs anything, and each was argued through #733's rounds. It is also the largest change, to the unit with the most rounds behind it | rejected |
| E4 — separate short tables per grammar inside E2 | Nothing is found that E2 misses. A letter one grammar lacks (`-a` in BSD, `-P`, `-L` and `-U` in GNU) is that grammar's error, so env runs nothing, and the merged table can only over-read there | rejected |
| F1 — BSD's `-` as an `ENV_OPTIONS` row `("-", None, None)` | `test_every_row_of_the_env_grammar_has_a_case` turns a short row into the spelling `f"-{short}"`, which is `--`, the end of the options. The row would need a case whose spelling means something else | rejected. `-` goes into `_ENV_SHORT` beside the table, as the fence does (decision F) |

## The generated comparison for C

This is the builder's method for every change to C, in phase 1 and in any
fix pass after it. It is a `test_tmp_*` probe under
a `g2-737-*` directory under the session's scratchpad (the spawn prompt
names the path),
run in the background and deleted afterwards (contract §7).

**The generator.** Each axis is derived from the code, never typed out as a
list of shapes.

- **Verbs.** `switch feature/x`, `switch -c y`, `switch -`,
  `switch --detach`, `checkout feature/x`, `checkout -b y`, `checkout -`,
  `checkout .`, `checkout -- README.md`, `checkout README.md`,
  `checkout -q`, `worktree add ../wt b`, `worktree list`. These are
  `KINDS`' verbs plus the two restores round 3 found.
- **Operators.** Every alternative in `_REDIRECTION`'s operator group that
  bash accepts. Give each a file descriptor where one is optional, and add
  bash 4.1's `{fd}` once. Give each a target that works under bash (`/dev/null`,
  `&2`, `&1`, an existing input file for `<`, a word for `<<<`). Use zsh's
  `>!` only where bash is not the oracle.
- **Positions.** Before `git`, between `git` and the subcommand, between any
  two words after that, and last.
- **Spacing.** Glued to the word before it or spaced, with the target glued
  to the operator or spaced.
- **Prefix segment.** None, `cd w && `, `git checkout README.md && cd w && `
  (round 1's yellow 3), and `git switch feature/x; ` (a judged switch).

**The ground truth.** Run each shape under bash in a fresh copy of a scratch
repository. The repository has branches `main` and `feature/x`, a modified
`README.md`, and an input file. Record whether HEAD moved or detached, and
whether `git worktree list` grew. Drive git from Python (contract §8). Run
each copy from a template rather than `git init` for each one.

**The variants.**

- At function level, `wider_only_kinds` at `f1629706`, at `2b1dcb1f` and in
  the build.
- Through `main()`, over a dirty `w` under a clean session, at `233f0455`,
  `f1629706`, `2b1dcb1f` and the build. Only `main()` exists at
  `233f0455`, because C was wired by #733.

Extract the hooks of each commit with `git -C … show <sha>:hooks/…` into the
scratch directory. Never check out another commit in the worktree.

**What passes.**

- (a) No shape that bash ran as neither a switch nor a creation is asked by
  the build unless `233f0455` asked it.
- (b) Every shape bash ran as a switch or a creation where both `233f0455`
  and the build are silent is listed by class with its count. #738's class
  is expected there, and it gives that issue a number.
- (c) Every shape on which the build and `2b1dcb1f` differ is listed by
  class, as dropped or added.

A shape failing (a) is a defect of the build, not a limit.

**The corpus count.** Run it as #733 phase 3 did, over D1's cut: every
`*.jsonl` under `~/.claude/projects/<this repository's slug>/`,
Bash tool uses timestamped before 2026-10-03T11:06:22+09:00. Count how many
of the 27,351 distinct pairs the built C fires on. The round-3 fence fired on
0. Where the build differs from the fence in logic, the count is the owner's
rule's input. Where it does not, record that, and run it anyway, as round 3
did.

## The generated comparison for env

This is the builder's method for every change to the env walk. It is a probe
like the one above.

**The generator.**

- **Words**, built from `ENV_OPTIONS` and from BSD's letter string
  `-0C:iL:P:S:U:u:v`:
  - every short letter of either grammar, alone and in two-letter clusters,
    `-` included;
  - a value glued to its letter and spaced;
  - every GNU long name, whole and in every prefix from `--x`, with `=v` and
    with a spaced value;
  - `--` followed by every BSD letter and two-letter cluster;
  - `--` and `-` alone;
  - `2>/dev/null`, glued and spaced;
  - an assignment `FOO=1`, and the values `FOO` and `x`.
- **Shapes.** Sequences of one to three such words, then a split-string word
  (`-S`, `-iS`, `-vS`, `--split-string`, `--spl`, `--S`, `-i-S`), then the
  string.

**The ground truth.**

- **BSD.** Run macOS `env <words> 'echo MARK'` and look for `MARK`. Every
  value used is harmless: `-C /tmp`, `-P /bin`, `-u FOO`. A program word left
  over (`FOO`, `x`) does not exist.
- **GNU.** A model of `getopt_long` with `+`, written from `src/env.c` and
  gnulib's rules. An exact name wins. A unique prefix names its option. A
  prefix of two options that differ is an error. A whitespace letter is an
  error. Getopt stops at the first word that is not an option. After the
  loop, a lone `-` is taken as `-i`. Then come the assignments, then the
  program.
- The model is labelled `read`, because GNU env is not installed here.

**The variants.** Use `cmdline.reparsed_texts` and `commit_invocations` at
`233f0455`, `2b1dcb1f` and the build. Substitute `git commit -m x` for
`echo MARK` in the string the reader sees.

**What passes.**

- (a) Every shape either ground truth runs is found by the build. A miss is
  a defect, or else a named limit with its count in `phases/phase-2.md` and
  in `overview.md` §*Not verified*.
- (b) Count the shapes found where neither runs, which are over-reads. Set
  the count beside `233f0455` and `2b1dcb1f`. An over-read the build adds
  over `2b1dcb1f` is listed by class.

**The corpus delta.** Over D1's cut, count the pairs whose `reparsed_texts`
differ between `2b1dcb1f` and the build, and record the shapes, rewritten to
`/Users/x/`. This is information, not the owner's rule (questions.md D4).

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | 🟡 13 and ⬜ 16. C reads each view's words with every redirection taken off. The S1 case, the S4 generated case, and three `WIDER_ONLY` rows (two `&>` switches and the `worktree 2>/dev/null add` creation). `wider_only_kinds`' docstring. One sentence and the re-stated count in `docs/worktree-guard-spec.md` §*Which tree*'s #678 paragraph. K5 corrected in place in `seal/ledger/1790993140-….md` | S1–S4 seen red at `2b1dcb1f`, or against the named mutant. `bin/mutation-check` breaks each step of the new helper (the glued cut, the `&` trim, the removal) and the merged-view sources, and a case kills each. S5 and S6 by the probes above. Narrow run of `tests/test_guard_resolves_the_tree_it_judges.py` | |
| 2 | 🟡 14 by decisions E and F, and Q1. Rows `--env0-from` and `--quoting-style`. `-` in `_ENV_SHORT`. `_env_option` reads under a named grammar, and the env arm walks once per grammar (BSD for `env` only) and dedupes. The table's comment names its two sources by file and commit. The `HANDED`, `ENV_SPELLINGS` and `CONTROLS` rows of S7–S9. K3 corrected in place | S7–S9 seen red. `bin/mutation-check` breaks the BSD walk, the GNU walk, the `genv` restriction, `_ENV_SHORT["-"]` and each new row, and a case kills each. S10 by the probe above. Narrow run of the wrapper module and the guard module, both of which import `hooks/cmdline.py` | |
| 3 | The records. New claims in `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md`. E14, E16, I5 and I6, and any other released row the change drifts, re-read through `bin/evidence-check --reverify --into <that fragment> --checked 2026-10-03`, with a `Corrected ·` row where a claim became false. `changelog.md`, `overview.md` | S11. `bin/evidence-check` reads 0 drifted and 0 broken on every ledger file touched. `bin/survivor-check --range 2b1dcb1f...HEAD` passes, with a `survivors.md` here as `--exempt` only for a quote that is defended | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

### What the builder carries through every phase

- **File I/O and paths.** Every file read and write passes
  `encoding="utf-8"`, in hooks, tests and probes alike. A printed path that
  names a documented location is POSIX-form.
- **No `git stash`.** Commit at each step that stands on its own, with
  `git -C <the worktree's absolute path> commit …`
  in a command of its own.
- **Probes.** A probe that commits drives git from Python. A long probe runs
  with `run_in_background: true`. Every leaving is deleted before hand-back,
  meaning extracted trees, scratch repositories and worktrees (contract §7).
- **No broad gate.** Not the full suite, not repository-wide lint, not the
  typecheck. That run is the sealer's, after the rounds settle (contract §2).
- **Before hand-back, over the whole range.** Run `bin/survivor-check --range
  2b1dcb1f...HEAD`.
- **`docs/commit-review-gate-spec.md` is not edited.** Where a sentence
  there must change, say so in the hand-back. The orchestrator sequences it
  with #727.

## Operational impact

- No migration, no new environment variable and no new dependency.
- **The worktree guard asks less.**
  - It stops asking about a restore or a detach that carries a redirection.
  - It asks one more kind of question: a worktree creation with a redirection
    between `worktree` and `add`, with no consent on record.
  - The prompt budget is the net count S5 and S6 measure. Both go in the
    pull request body.
- **The commit gate stops more `env` lines.** These are commits that BSD's or
  GNU's grammar runs and the reader missed. A declared work item still
  commits silently, as before. The corpus delta is in the pull request body.
- **Platform honesty.** BSD's half was executed on macOS. GNU's half is read
  from `src/env.c` and modelled, because GNU env is not installed. The planted
  cases test the reader and never run `env`, so no CI leg checks GNU's half
  either. `overview.md` §*Not verified* names that, with its answerer.
