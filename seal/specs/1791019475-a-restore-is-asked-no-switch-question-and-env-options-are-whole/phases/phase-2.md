# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a5aa6437 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Close 🟡 14 by decisions E and F and Q1. Add the rows `--env0-from` and
`--quoting-style`, put BSD's `-` in `_ENV_SHORT`, have `_env_option` read
under a named grammar, and have the env arm walk once per grammar (BSD's for
`env` only) and dedupe. Name the table's two sources by file and commit.
Plant the `HANDED`, `ENV_SPELLINGS` and `CONTROLS` rows of S7 to S9, and
correct K3 in place. Hold the walk to the generated env comparison (S10),
with macOS `env` executed for BSD's half and a model of `src/env.c` for
GNU's. Answer M1 and W1 here.

## What this phase found

**W1: a keyword parameter.** `_env_option(t, own, grammar="gnu")`. The walk
moved out of `reparsed_texts` into `_env_walk(word, rest, grammar,
env_words)`, unchanged in its steps. The env arm calls it for "gnu" and, for
`env` alone, for "bsd". It appends only the BSD walk's strings that the GNU
walk did not already find, so `genv` takes GNU's walk alone. That walk is
not `2b1dcb1f`'s: it reads the two new rows, which GNU's prefixes now reach,
and BSD's `-` letter, which `_ENV_SHORT` shares between the walks.
`genv -i-S '…'` is found although GNU refuses the word, which is #733's
merged-table over-read (`plan.md` E4).

**Corrected 2026-10-03 by round 1's fix pass (white 4).** The sentence above
said `genv` and every GNU reading return exactly what they returned at
`2b1dcb1f`. Over round 1's shapes, `genv` gained 1,930 finds and lost 357.
326 of the gains are strings the GNU model runs, and most of the rest are
`genv -i-S '…'`. The 357 losses are prefixes of `--env0-from` and
`--quoting-style` taking the next word, where no `env` runs the string.

**Every new case was seen red.** At `2b1dcb1f`'s `hooks/cmdline.py`, all six
S7 shapes failed in both `test_a_commit_in_a_string_or_a_substitution_is_read_as_unreadable`
and `test_the_gate_stops_it`. `--env0-from` and `--quoting-style` failed in
`test_a_cluster_behind_env_s_own_options_is_read`. S8 was red twice. First,
with the spellings and without the rows, at `2b1dcb1f`. Then the spec's way,
with the rows in place and a scratch copy of the module lacking the two
spellings: `{'--env0-from', '--quoting-style'}`. S9 passed at `2b1dcb1f`. It
was red against the mutant that gives `genv` the BSD walk too.

**Each unit was broken once with `bin/mutation-check`, over the wrapper
module.** These breaks were red:

| Break | Failed |
|---|---|
| the BSD walk | 8 |
| the GNU walk | 29 |
| the `genv` restriction | 2 |
| `_ENV_SHORT["-"]` | 6 |
| the `--env0-from` row | 4 |
| the `--quoting-style` row | 2 |
| the BSD cluster arm | 8 |
| the dedupe | 6 |
| the grammar not passed down | 8 |

**Two clauses survived, and they are gone.** The first version read a `--`
word as a BSD cluster only among env's own options and only where it was not
`--` alone. Breaking either clause left all 672 cases green. Each is
equivalent under the union of the two walks. `--` alone spells nothing
either way, and the walk ends the options there. Outside the options, the
GNU walk keeps the split string's spellings that are read anywhere. The
condition is now `grammar != "bsd"` (`a5aa6437`), and breaking it was red
again (8 failed).

**S10, the generated comparison.** 64,519 shapes. The words were built from
every short letter of either grammar, `-` included, alone and in two-letter
clusters, with values glued and spaced. They also include every GNU long name
in every prefix from `--x`, with `=v` and a spaced value, and `--` followed by
every BSD letter and two-letter cluster. Add `--`, `-`, a redirection, an
assignment, and the words `FOO` and `x`. Each shape is one to three such
words (all 473 words alone, a set of 55 in pairs and a set of 18 in
triples),
then one of seven split-string words, then the string. macOS `env` ran 8,485
of them (executed through `/bin/sh`, looking for the marker on standard
output). The GNU model ran 11,170 (read: GNU env is not installed). 17,717
ran under one or the other.

| | `233f0455` | `2b1dcb1f` | build |
|---|---|---|---|
| found | 18,434 | 30,701 | 41,613 |
| missed where macOS `env` runs the string | 6,788 | 4,022 | 0 |
| missed where the GNU model runs it | 6,702 | 1,374 | 0 |
| found where neither runs it (over-reads) | 12,915 | 18,380 | 23,896 |

**M1: macOS `env` and the BSD reading agree wherever `env` runs the
string.** No shape it runs is missed. Where they disagree, `env` refuses
and the reader over-reads. The build adds 6,056 over-reads over
`2b1dcb1f`, all behind a split word only one grammar reads (`-i-S` 3,380,
`--S` 1,858) or behind a word one grammar refuses:

| What runs nothing in either env | Shapes |
|---|---|
| a `--` word one grammar refuses, which the other walk reads past (`--env0-from -i-S`: GNU takes `-i-S` as the value, BSD refuses `e`) | 4,411 |
| the same, together with a letter one grammar lacks | 411 |
| a letter one grammar lacks (`-a` in BSD; `-L`, `-U` in Apple's and GNU's) | 348 |
| `--help` or `--version`, which GNU answers and exits, and BSD refuses | 366 |
| `-0` with a command, which both refuse | 404 |
| a value refused at run time (`-Ca`, a directory that does not exist) | 132 |

Each is #733's settled over-read applied to the second walk: a refused letter
or an unknown name is read past, and a letter one grammar lacks is read from
the merged table. The plan calls this cost a stop only where no env runs
anything (`plan.md` E2 and E4). The rows above overlap in their tags, and
together they cover all 6,056.

**The corpus delta.** Over D1's 27,351 pairs, 1,858 mention `env`. For none
of them do `reparsed_texts` or the commits `commit_invocations` finds differ
between `2b1dcb1f` and the build. That count is information, not the owner's
rule (`questions.md` D4).

**`docs/commit-review-gate-spec.md` needs no edit.** Its `env -S` sentence
names no option and no table, so it stays true. It was not edited (#727).

The probe, its result files and the three hooks snapshots it read were made
under the session scratchpad. They are deleted before the hand-back.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the env walk's body inside `reparsed_texts` | `_env_walk`, unchanged in its steps |
| the comment's claim that the table was built from the two synopses | the comment now names `src/env.c` and `usr.bin/env/env.c` by commit |
