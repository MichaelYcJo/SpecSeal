# Feature Specification: 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#737 carries what #733's capped round 3 deferred. Two defects are in this
release's branch and nowhere in 0.17.0, and one test gap sits beside them:

- **🟡 13.** The worktree guard asks *switches a branch* of commands that
  switch nothing, such as `git checkout . &>/dev/null`. The shipped base
  `233f0455` never asked them.
- **🟡 14.** `env`'s option table misses BSD's `-` letter and GNU's
  `--env0-from`. So `env -i-S '…'` and `env --S '…'` run a string on macOS
  that the commit gate finds nothing in.
- **⬜ 16.** No case has an `&>` between the subcommand and its name, so the
  mutant that compares the merged group with itself survives.

The round-3 report (`seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/rounds/round-3-report.md`)
holds a paste-ready fence for each finding. The fences are the starting point
here, not the answer. Candidate C has opened a defect in itself three rounds
running. Each time the fence was right about the shapes it named and wrong
about the shapes next to them. So this frame fixes the method as well as the
code (§*Acceptance*, S5 and S10).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | A question that stops an unattended run is the expensive outcome. A restore that asks *switches a branch* stops a run for nothing, and the base never asked it. That makes 🟡 13 a defect this release must not ship (#737's body) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget, platform honesty. The failure direction of each change is stated under *Scope*. The prompt budget is the guard's net question count over the generated shapes and the corpus (S5, S6) |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*, the paragraph opening "Since #678" | C asks only at an exit where the guard was about to say nothing. It asks about a switch or a creation *that only the commit gate's reading finds*. A restore is neither. The paragraph's measurement sentence names the corpus count, so a change to C re-states that count |
| `docs/worktree-guard-spec.md` §*Known limits* | Where a silence stays, it is named here with its count. This work adds no entry (Q2) |
| `docs/commit-review-gate-spec.md` §*A `cd` the gate cannot read*, the sentence on `env -S` (around its line 564) | It says only that `env -S`'s string is read as a command and as `env`'s own words. It makes no claim about which options the table holds, so it stays true after this work, and **no edit to it is planned**. #727 is splitting that file in parallel |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, with `seal/config.md` `Ledger frozen from` = `1790993141` | This work item's id, `1791019475`, is above the cutoff. A released row (`seal/releases/0.16.0.md` E14, E16, I5, I6) is re-read as a `Re-read ·` or `Corrected ·` row in this item's own fragment and is never edited in place. K3 and K5 sit in `seal/ledger/1790993140-….md`, a fragment not yet folded. The same section says a citation into a fragment is refused, so those two rows are re-stamped and corrected **in place** |
| `skills/agent-contract` §12, §15 | A defect belongs to a class, and the class is enumerated by construction rather than from examples. Every new case is seen red before it is planted |
| `hooks/cmdline.py#reparsed_texts`, its docstring | The reader's own direction rule: "reading an extra word as a command costs a stop, and missing the string costs a silence." Where GNU's and BSD's grammars disagree about a word, both readings are taken (§*Scope*, decision E) |

**Sources of `env`'s grammar.** These were read from the sources, not from
the synopses. Synopses are what missed `-` and `--env0-from`.

- GNU coreutils `src/env.c`, last changed in commit `f799b2f48a61`
  (2026-09-17). `shortopts` is `"+a:C:iS:u:v0"` plus the six C-locale
  whitespace characters, and each of those is an error. `longopts` holds
  `argv0`, `ignore-environment`, `env0-from` (required), `null`, `unset`,
  `chdir`, `default-signal`, `ignore-signal`, `block-signal` (each optional),
  `list-signal-handling`, `debug`, `quoting-style` (required), `split-string`,
  `help` and `version`. After `getopt_long`, a lone `-` sets `-i` and is
  consumed. Because of the `+`, getopt has already stopped at it. GNU's NEWS
  dates `--env0-from` to 9.12 (2026-09-14) and lists `--quoting-style` under
  the unreleased section.
- FreeBSD `usr.bin/env/env.c`, last changed in commit `c2d93a803ace`. It
  calls `getopt(argc, argv, "-0C:iL:P:S:U:u:v")`, and `case '-':` shares
  `case 'i':`. FreeBSD `lib/libc/stdlib/getopt.c` handles two cases this
  work depends on. `--` alone ends the options. A word starting `--` with
  more after it is read as a cluster whose first letter is `-`.
- Apple `shell_cmds` `env/env.c` uses `"-0C:iP:S:u:v"`, without `L` or `U`.
- Read on 2026-10-03 from the sources, fetched read-only. GNU env is not
  installed here, so GNU's half is read and not run.

**Executed on macOS on 2026-10-03, by the framer, with `echo` as the
string.** In each line below, macOS `env` ran the string:

- `env --unset -S 'echo …'`, `env --unset -iS 'echo …'`
- `env --un -S 'echo …'`, `env --un -vS 'echo …'`
- `env --i -S 'echo …'`, `env --v -S 'echo …'`
- `env -i-S 'echo …'`, `env -u FOO- -S 'echo …'`

Two did not run it:

- `env --u -S 'echo RAN-u'` took `-S` as `-u`'s value and failed as a
  program named `echo RAN-u` (exit 127).
- `env --unset=FOO -iS '…'` failed at `unsetenv` (exit 1).

That first list is the round-3 fence's neighbour. BSD reads `--unset`, and any
prefix of it of four characters or more, as `-i -u <rest of the word>`. GNU
reads the same word as `--unset` taking the next word. The fence reads a word
that names a GNU long option only as GNU does. So in
`env --unset -iS 'git commit -m x'` it takes `-iS` as `--unset`'s value and
finds nothing, while macOS runs the commit. (That last step is read: the
fence was not applied and run.)

## Scope

**In.**

1. **🟡 13 — read each view of C as the program is handed it.** Take off a
   redirection glued to a word's end, take out every redirection, and then
   read the kind. This replaces the pair of readings
   `wider_only_kinds` takes today, the view and its `unglued` view. The
   round-3 fence `_bare_words` is the starting point. Failure direction: the
   guard asks less. The questions it stops asking are restores and
   detaches, which switch no branch. It also asks one kind of question the
   base did not: a creation with a redirection between `worktree` and `add`
   (`git worktree 2>/dev/null add ../wt b`). Bash runs that as a creation,
   so it is C's own class, and consent is read before it as before.
2. **⬜ 16 — the two `&>` cases.** `git switch &>/dev/null feature/x` and
   `git checkout &>/dev/null feature/x` go into `WIDER_ONLY` with the
   creation above. With them, the merged-group-compared-to-itself mutant is
   killed through pytest. The round-3 report saw it killed only at function
   level.
3. **🟡 14 — `env`'s grammar as both sources give it.**
   - The missing rows: `--env0-from` (required) and `--quoting-style`
     (required, Q1).
   - BSD's `-` letter, entered as a short letter with no value outside
     `ENV_OPTIONS` (decision F).
   - **Decision E.** The env arm of `reparsed_texts` reads env's words twice
     and keeps every string either reading finds. One reading uses GNU's
     grammar: a `--word` is a long name, exact or a unique prefix. The other
     uses BSD's grammar: a `--word` other than `--` is a cluster whose first
     letter is `-`. The BSD reading is taken for `env` alone, because `genv`
     is GNU's by name.
   - Everything else in the walk stays as #733 built it: the merged short
     table, a redirection read past, `--` ending the options, a lone `-` read
     as an option.
   - Failure direction: the gate finds more and never less. A reading is
     only added, and every added find is a spelling one of the two sources
     accepts.
4. **The method, for every change to C and to the env walk** (S5, S10). This
   is a comparison over generated shapes. The generators are derived from the
   reader's own grammar (`_REDIRECTION`'s operators and `ENV_OPTIONS`'s rows),
   not listed by hand. Each is checked against a ground truth that is run
   where it can be: bash in a scratch repository for C, macOS `env` for BSD's
   half. A model written from `src/env.c` stands in for GNU's half. Each
   result is set beside `233f0455`, `f1629706` and `2b1dcb1f`.
5. **The policy sentence and the ledger.**
   - A sentence in `docs/worktree-guard-spec.md` §*Which tree*'s #678
     paragraph: a redirection's word is taken off before a kind is read, so a
     restore with a redirection is not asked about. The corpus count there is
     re-stated for the built C. This is contract §14, because the change
     alters what a person sees.
   - K3 and K5 corrected in place in their fragment. E14, E16, I5 and I6 are
     re-read or corrected in this item's fragment.
   - New claims go in `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md`.

**Out, each with its reason.**

- **#738 (🟡 15)**, a checkout whose name carries a redirection never being
  asked. This is Q2: its only fence asks on a glued restore
  (`git checkout README.md>/dev/null`), which is 🟡 13's class under another
  name. It stays in the backlog milestone it is in. The generated
  comparison gives it a count (S5), which the orchestrator can carry to the
  issue.
- **A tree-aware C.** Telling `feature/x` from `README.md` needs a tree
  inside C. #689 decided that the wider reading never picks a tree.
- **#734**, the consent read in `ask_what_only_the_wider_reading_finds`.
  It is already deferred, and nothing here touches that function.
- **A strict getopt emulation** (plan alternative E3). It would drop #733's
  deliberate over-reads, such as an unknown long name read as a flag and a
  lone `-` read as an option. Those cost a stop only where no env runs
  anything, and taking them out is a change to what #733's rounds settled.
- **`docs/commit-review-gate-spec.md`.** The grounding row says why no
  sentence there changes. If the build finds one that must, it is reported
  to the orchestrator and not edited (#727).
- **`overview.md` of work item 1790993140.** Its `env -S` row says the table
  was "built from … synopses". That is a closed work item's account of its
  own build at its own commit, so it is not rewritten. K3, the live claim,
  is what gets corrected.
- **The question's text.** `ask_what_only_the_wider_reading_finds` is
  unchanged. It still names the shapes it reads, and none of them is a
  restore.
- **`README.md` and `README.ko.md`.** Neither describes the guard's
  question shapes or `env`'s options. A search on 2026-10-03 for
  `env -S`, `switches a branch` and the question's opening found only
  `docs/commit-review-gate-spec.md`.

## User scenarios & acceptance *(mandatory)*

Every case named here is seen red before it is planted (contract §15). "Red"
means it failed at `2b1dcb1f`, or failed against the named mutant where it
passes at `2b1dcb1f`. "A dirty `w`" means
`tests/test_guard_resolves_the_tree_it_judges.py#_a_dirty_w_under_a_clean_session`.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a restore with a redirection is not asked about | Given a dirty `w` under a clean session. When any of `cd w && git checkout . &>/dev/null`, `git checkout .&>/dev/null`, `git checkout -q &>/dev/null`, `git switch --detach &>/dev/null`, `git switch --detach>/dev/null` or `git checkout>/dev/null .` runs. Then the guard is silent | The round-3 parametrized case, red at `2b1dcb1f` on all six |
| S2 an `&>` before the name is still asked | When `cd w && git switch &>/dev/null feature/x` or `git checkout &>/dev/null feature/x` runs. Then `wider_only_kinds` is `{"switch"}` and `main()` asks | `WIDER_ONLY` rows. They pass at `2b1dcb1f`, and are red against the merged-self mutant, run through `bin/mutation-check` |
| S3 a redirection between `worktree` and `add` | When `cd w && git worktree 2>/dev/null add ../wt b` runs. Then `main()` asks *creates a worktree* with no consent, and is silent under consent | `WIDER_ONLY` row. Red at `2b1dcb1f` in both the function case and the `main()` case. The consent case already parametrizes over the creation rows |
| S4 no restore verb asks, whatever the redirection and wherever it stands | For every operator `_REDIRECTION` names, at every position (before `git`, between `git` and the subcommand, between any two words after it, last), glued to the word before it and spaced, with its target glued and spaced, and for each verb that switches nothing (`checkout .`, `checkout -- README.md`, `checkout -q`, `switch --detach`, `worktree list`). Then `wider_only_kinds` is empty | A planted function-level test whose operator list is taken from, or checked against, `_REDIRECTION`. A new operator in the reader is then a new case. Red at `2b1dcb1f` |
| S5 the build asks nothing new that bash does not run as a switch or a creation | Over the generated shapes of plan §*The generated comparison for C*, the build's asks are a subset of `233f0455`'s asks plus the shapes bash ran as a switch or a creation. Every shape bash ran as one where both the base and the build are silent is listed by class | The builder's probe, deleted after the run. Counts for each of `233f0455`, `f1629706`, `2b1dcb1f` and the build go in `phases/phase-1.md` |
| S6 the owner's count | C as built fires on no more of D1's 27,351 pairs than the round-3 fence did, which was 0 | Re-counted, using #733's D1 cut and phase-3 method, wherever the built C differs in logic from the round-3 fence. Recorded in `phases/phase-1.md` either way |
| S7 a commit behind BSD's and GNU's missed spellings is found | `env -i-S '{C}'`, `env --S '{C}'`, `env -u FOO --S '{C}'`, `env --env0-from f -iS '{C}'`, `env --unset -iS '{C}'` and `env --un -vS '{C}'` are each found, stop in an undeclared opted-in repository, and are silent in a declared one | `HANDED` rows. Red at `2b1dcb1f` in `test_the_gate_stops_it` and in `test_a_commit_in_a_string_or_a_substitution_is_read_as_unreadable`. The last two are also red against the round-3 fence's choose-one long arm |
| S8 every row has a case | `ENV_SPELLINGS` gains `--env0-from` and `--quoting-style` | `test_every_row_of_the_env_grammar_has_a_case` is red once the rows exist and before the spellings do |
| S9 `genv` is read as GNU only | `genv --unset -iS '{C}'` runs `git commit -m x` as one program word under GNU, so it is read as no hidden commit | A `CONTROLS` row. It holds at `2b1dcb1f` and is red against a mutant that takes the BSD reading for `genv` too |
| S10 the env walk against both sources | Over the generated env shapes of plan §*The generated comparison for env*, every shape in which macOS `env` or the GNU model runs the commit is found. Every shape found where neither runs is counted, and the count is compared with `233f0455` and `2b1dcb1f` | The builder's probe, deleted after the run. Counts and the misses, where there are any, go in `phases/phase-2.md` |
| S11 the records hold | K3 and K5 describe the built code. E14, E16, I5 and I6 are re-read in this item's fragment. `bin/evidence-check` reads 0 drifted and 0 broken on every ledger file the branch touched. `bin/survivor-check --range 2b1dcb1f...HEAD` passes, with a `survivors.md` here as `--exempt` only where a surviving quote is defended | Executed by the builder before hand-back |

## Data & interfaces

- `hooks/worktree-guard.py#wider_only_kinds`: its loop over `sourced` and its
  docstring. A module-level helper is added beside it (`_bare_words` in the
  fence). `switch_kind`, `ask_what_only_the_wider_reading_finds` and `main`
  are not changed.
- `hooks/cmdline.py`:
  - `ENV_OPTIONS` gains two rows, and the comment above it names the two
    sources.
  - `_ENV_SHORT` gains `-`.
  - `_env_option` takes the grammar it reads under.
  - The env arm of `reparsed_texts` walks once per grammar and removes
    duplicate texts without changing their order.
  - `_env_long` is not changed.
- `tests/test_guard_resolves_the_tree_it_judges.py`: `WIDER_ONLY`, the S1
  case and the S4 case.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`:
  `HANDED`, `ENV_SPELLINGS`, `CONTROLS`.
- Ledger coordinates the change drifts:
  - In `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md`,
    K3 (`hooks/cmdline.py#reparsed_texts`) and K5
    (`hooks/worktree-guard.py#wider_only_kinds`).
  - In `seal/releases/0.16.0.md`, E14, E16, I5 and I6, each of which cites
    `hooks/cmdline.py#reparsed_texts`. The builder lists the full set with
    `bin/evidence-check`, not from this list.

## Open questions → questions.md

Q1 (`--quoting-style`), Q2 (#738), Q3 (whether the comparisons stay as
probes) and the D rows are decided by this frame and listed there. No row
needs a person.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-03 by framer, before the build.
