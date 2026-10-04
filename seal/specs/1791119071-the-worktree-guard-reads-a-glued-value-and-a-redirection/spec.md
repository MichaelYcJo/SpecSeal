# Feature Specification: the worktree guard reads a glued value and a redirection

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issues #764 and #738, milestone `release: 0.18.2`. Both are switches bash and
git run while the worktree guard says nothing, and both sit in the two
readers the guard uses for a `checkout` or a `switch`:
`hooks/worktree-guard.py#classify`, which reads the frozen segment's words
against a tree, and `hooks/worktree-guard.py#switch_kind`, which reads the
same words with no tree and is what candidate C (`wider_only_kinds`)
compares with.

- **#764.** Both readers test `a in ("-b", "-B")` and `a in ("-c", "-C")` and
  treat every word starting with `-` as no name. Git's option parser accepts
  more spellings of a value-taking option than the separate short one, so
  `git checkout -bNAME`, `git switch -cNAME`, `git checkout -qb NAME` and
  `git switch --create=NAME` create a branch and switch to it unasked.
  Found by #750's frame (`seal/specs/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks/spec.md`
  §*Out, and why*, the second bullet).
- **#738.** bash takes a redirection off the command line before git runs,
  so `git checkout feature/x>/dev/null` and `git checkout 2>/dev/null
  feature/x` switch. The frozen splitter keeps `<` and `>` inside a word
  (`hooks/cmdline_base.py#split_segments_with_separators`, `punctuation_chars=";|&"`),
  so `classify` looks up a ref named `feature/x>/dev/null`, or takes
  `2>/dev/null` as the first positional, and finds none. `switch_kind` reads
  the same word as a name, so C counts the switch as one the frozen loop
  found and subtracts it. Found by round 3 of work item
  `1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd`, 🟡 15,
  whose report is on `refs/backup/0.18.1/local/fix/716-the-gates-read-config-env-env-s-and-an-unresolved-cd`
  (`seal/specs/1790993140-…/rounds/round-3-report.md` §*🟡 15*).

The two are one defect at two depths: neither reader reads the words git is
handed. #737's build measured the class at 226 generated shapes silent at
`233f0455`, `2b1dcb1f` and its own build (#738's comment): 84 with a
redirection between `checkout` and the name, 44 with one glued to the name,
56 around `-b`, 42 around `-`. That count is nobody's finding here; phase 1
measures this tree's own.

## The frozen reading, and what the owner reopened

**How the tree says `classify` is frozen.** Three records, of two strengths:

| Record | What it freezes | Strength |
|---|---|---|
| `tests/test_the_frozen_reading_never_grows.py#test_the_bytes_below_the_rider_are_86256492s` and `hooks/cmdline_base.py`'s rider | `hooks/cmdline_base.py`, byte for byte, below its rider — the splitter, `parse_git`, `adds_a_worktree`, the walk | a test that fails |
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/questions.md` P4, the owner's answer of 2026-10-01 | "the switch arm keeps the frozen 0.16.0 text reading (`hooks/cmdline_base.py`) on every git, permanently and byte-pinned, with no rule added" | an owner's decision |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*, first paragraph | "The whole command is read the way the release base `86256492` read it … which segments are git, the `-C` values each names, where every `cd` lands" | ratified policy |

`classify` itself sits in `hooks/worktree-guard.py`, not in the pinned file.
Read today, its body is byte-identical to `86256492:hooks/worktree-guard.py`'s
(compared 2026-10-04 by extracting both function bodies), and no test pins
it. It is "frozen" by the P4 answer's *no rule added* and by the policy
paragraph above, which is how round 3 of 1790993140 could write "the frozen
`classify` is `86256492`'s by construction (#689)".

**The reopening.** The owner put #764 in milestone `release: 0.18.2` on
2026-10-04, and #764's own text says the fix reaches `classify` and that
"only the owner reopens it". That placement is the owner's agreement to add a
rule to `classify`, recorded in this work item's `routing.md` (*Why this
way*). It is recorded here as that, and three things follow from it honestly
rather than around it:

1. `hooks/cmdline_base.py` is **not** reopened. Its bytes, its pin and the
   S11 case stay exactly as they are; nothing in this work edits that file or
   that test. The reopening is the per-subcommand rule in `classify` (and its
   tree-blind twin `switch_kind`), not the splitter, the walk or the tree.
2. The policy paragraph that says the command is read as `86256492` read it
   is **changed** to say what is now read past the base: a `checkout`'s and a
   `switch`'s own words, as git's option parser and bash hand them, since
   #764 and #738 on the owner's answer of 2026-10-04. Which segments are git,
   which `-C` each names and where every `cd` lands stay the base's.
3. The #738 half rides the same reopening. That is the frame's reading of the
   owner's act, not something the owner said; `questions.md` P1 puts it to
   the owner with the default the build uses.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/worktree-guard-spec.md` §*A. Branch switch* | A switch over a tree with another session or uncommitted changes is denied, offered as a choice or asked. The defect is that these shapes never reach the table; the table itself does not change |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*, first paragraph | The base-reading statement this work amends (above, item 2) |
| `docs/worktree-guard-spec.md` §*Which tree*, the #678 paragraph, the sentence "Each side is read by its words alone: a `switch` naming a word or `-`, a `checkout` carrying `-b` or `-B`, a `checkout` with no `--` among its words that names `-` or a word other than `.`, or a `worktree add`" | #750's corrected sentence. It must still agree with `switch_kind` after this change, so it is rewritten to name the words as git is handed them (Scope, In 4) and its pin moves with it |
| `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* | A wrong deny costs one prompt; a wrong allow can break another session's tree. It decides the failure direction of every borderline below |
| `docs/worktree-guard-spec.md` §*Known limits* | Where what this work still does not read is named, with its count |
| `seal/specs/1790815613-…/questions.md` P4, P6 | The frozen reading's owner decisions (above) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget, platform honesty — each is an acceptance row below |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is enumerated by construction (below); the changed sentence is pinned in the same commit as the behaviour; every new case is seen red |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | The changelog entry goes in this directory's `changelog.md`, the ledger rows in `seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md` |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | `seal/config.md` declares `Ledger frozen from`, so the released rows this work drifts (at least K5 and N1 of `seal/releases/0.18.0.md`, G1 and the K5 re-read of `seal/releases/0.18.1.md`) are read again by `Re-read ·` rows in the fragment, never re-stamped in place |

## The class, enumerated by construction (§12)

A shape is one point in the product of three axes. The build generates the
product; it does not list examples.

**Axis 1 — the carrier: the word that makes the segment a switch.**

| Subcommand | Creating option (the value is the new branch) | Target |
|---|---|---|
| `checkout` | `-b`, `-B`, `--orphan` | the first name, or `-` |
| `switch` | `-c`, `-C`, `--create`, `--force-create`, `--orphan` | the first name, or `-` |

Read from git's own usage (`git checkout -h`, `git switch -h`, git 2.54.0,
2026-10-04). `-d`/`--detach` and `-t`/`--track` carry no new branch: a
detach moves the tree only through its target name, and `--track` takes its
value stuck or not at all.

**Axis 2 — the spelling git's option parser accepts** (`git help cli`
§*Enhanced option parser*: aggregated short options, abbreviated long
options, a mandatory value stuck or separate, an optional value stuck only).

| Spelling | Creating option | Read today by `classify` / `switch_kind` |
|---|---|---|
| S1 short, separate | `-b N` | yes / yes |
| S2 short, stuck | `-bN` | no / no |
| S3 aggregated, separate | `-qb N`, `-fb N` | no where `N` is no ref yet / reads `N` as a name |
| S4 aggregated, stuck | `-qbN` | no / no |
| L1 long, separate | `--orphan N`, `--create N` | `checkout --orphan N`: no where `N` is no ref; `switch`: read as a plain switch / yes |
| L2 long, stuck | `--orphan=N`, `--create=N` | no / no |
| L3, L4 abbreviated long, separate and stuck | `--orph N`, `--cre=N` | as L1, L2 |
| V a value-taking option that creates nothing, separate, before the target | `--conflict merge N`, `-U 3 N` | `classify` looks up the value (`merge`) instead of `N` / reads the value as a name |

**Axis 3 — a redirection inside the segment**, which bash takes off the
command line before git sees it. Every operator `hooks/cmdline.py`'s
`_REDIRECTION` names, with no descriptor, a number and `{fd}`, its target
stuck and separate (the generator `tests/test_guard_resolves_the_tree_it_judges.py#_redirections`
already derives these from the pattern), at each position:

| Position | Example | Reader today |
|---|---|---|
| R0 none | `checkout -bN` | — |
| R1 between the subcommand and the carrier | `checkout 2>/dev/null feature/x` | missed (#738) |
| R2 stuck to the subcommand | `checkout>/dev/null feature/x` | C's cut view (#737), kept |
| R3 stuck to the carrier's end | `checkout feature/x>/dev/null`, `checkout -b>/dev/null N` | missed (#738) |
| R4 between an option and its separate value | `checkout -b 2>/dev/null N` | missed |
| R5 after the carrier | `checkout feature/x 2>/dev/null` | read |
| R& any of the above with an operator holding `&` or `|` (`2>&1`, `>&2`, `&>`, `<&`, `>|`) | `checkout 2>&1 feature/x` | the frozen splitter cuts the segment there; only C's merged view holds the whole switch |

**Each shape has a restore twin**: the same spelling with the target a file
that exists (`README.md`), `.`, or a name after `--`. Bash and git restore and
the tree stays on its branch, so the twin must not become a new question
except where §*Which tree* already says a tree-blind reading asks it (the R&
row, below).

## Scope

### In

1. **One word reader for `checkout` and `switch`**, in
   `hooks/worktree-guard.py`, read by both `classify` and `switch_kind`. It
   takes a segment's arguments as git is handed them and returns what git's
   option parser would see: whether a creating option is present (with or
   without a value, as today: `checkout -B` alone still counts), the names
   left after every option has taken its value, and whether `--` was given.
   - **The words git is handed.** A redirection stuck to a word's end is cut
     off, an `&` left on a word's end before a `>`-led word goes with it, and
     every redirection is taken out with its separate target. This is the
     reduction `_bare_words` already makes for C's views (#737), and C's
     views read through the same local reduction, so the frozen side and the
     view side cannot reduce differently.
   - **The option table.** Static, for `checkout` and `switch`, read from
     git 2.54.0's usage text: every short and long option, whether it takes a
     value (none, mandatory, optional), and whether it creates. The parse
     follows `git help cli`: options are read up to `--`; a short word is
     read one character at a time, a mandatory-value character taking the
     rest of the word or else the next word, an optional-value one taking
     only the rest of the word; a long word resolves by exact name, then by
     unique prefix, `--no-` negating, a mandatory value taken after `=` or
     from the next word. A word git would refuse (an unknown or ambiguous
     option) reads as an option that takes nothing, which is today's reading
     of any `-` word.
   - **No dependency on `hooks/cmdline.py`.** `classify` keeps answering where
     the wider reader fails to load (`test_a_broken_wider_reader_costs_only_the_question`).
     The reduction's operator list is bound to `cmdline._REDIRECTION` by a
     test, not by an import.
2. **`classify` reads through it**, keeping its tree: a creating option in any
   spelling is `create+switch`; otherwise its existing order (`--` is a
   restore; `-` is a switch; the first name is a path → restore, a ref or
   `origin/<name>` → switch, the `)` peel) applies to the first name the
   reader leaves. So `checkout README.md>/dev/null` stays a restore, because
   the tree says `README.md` is a file — the trade round 3's fence paid is not
   paid here.
3. **`switch_kind` reads through it**, with no tree, in the `switch` and
   `checkout` arms only. Its `worktree` arm is unchanged (Out).
4. **The policy text**, in the same commit as the behaviour (§14):
   - §*Which tree*'s first paragraph names what is now read past the base, on
     whose answer and when (above, item 2);
   - the #678 paragraph's sentence names the words as git is handed them: an
     option's value is not a name, a creating option counts in any spelling
     git's parser accepts, a redirection is no word. The rest of the sentence
     — `-` or a word other than `.`, `--` taking every name out of a
     `checkout`, a `worktree add` — keeps #750's content;
   - §*Known limits* names what is left (Out) with its counts;
   - the pin in `test_the_guard_policy_says_a_hidden_file_checkout_is_asked`
     moves with the sentence.
5. **The checks**, each seen red at `94d7b2e0` before it is committed (§15):
   `KINDS` rows for every Axis-2 spelling and for V; `classify` cases against
   a repository holding a branch and a file; the generated property over the
   three axes (acceptance A4–A6); the two binding cases (A7, A8).
6. **The records**: `changelog.md`, the ledger fragment with its new rows and
   `Re-read ·` rows, `overview.md` (the builder's), `phases/phase-N.md`.

### Out, and why

- **`hooks/cmdline_base.py` and its S11 pin.** P4 keeps it byte-pinned, and
  nothing here needs it changed: the splitter's segments and words are read
  as they are, and the new reading happens in `hooks/worktree-guard.py`.
- **A tree inside candidate C.** The R& shapes (`checkout 2>&1 feature/x`)
  are cut into two frozen segments, and only C's merged view holds the
  switch. C reads no tree (#689), so a file behind the same operator
  (`checkout 2>&1 README.md`) is asked too. §*Which tree* already states that
  rule and pins `git checkout &>/dev/null README.md` as asked. Giving C each
  segment's directory needs the frozen walk's directories mapped onto the
  wider splitter's segments, which segment differently; round 3 of 1790993140
  named this and it is not this ticket. Named in §*Known limits* with the
  corpus count instead.
- **The `worktree` arm.** `classify` reads a creation through the frozen
  `cmdline.adds_a_worktree`, and `hooks/worktree_consent.py` files consent
  through the same call on the command that ran (§*Creation consent*: one
  reading, two readers). Reading the guard's side past redirections alone
  would split the two. A creation behind a redirection is already C's
  (#737's `git worktree 2>/dev/null add` row), and the class here is the
  switch.
- **A ref after `-p`/`--patch` or `--pathspec-from-file`.** `git checkout -p
  feature/x` applies hunks and keeps the branch, and the guard asks it today
  because the name is a ref. Making it silent is the quiet direction on a
  shape nobody reported; §*Unknowns resolve conservatively* keeps the ask.
- **An alias** (`git co -bNAME`). The guard reads no git config today, and
  that is not this class.
- **A quoted `<` or `>` inside a name** (`git checkout 'a>b'`). The frozen
  splitter removes the quotes, so the reduction cuts it like an unquoted one.
  A ref name may hold `>`; a cut name that is a ref asks, a cut name that is
  not falls to the restore reading. Named in §*Known limits*; phase 1 counts
  it in the corpus.
- **Reading the option table from the installed git at hook time.** One
  `git <sub> -h` per event, and its text format is not an interface. The
  table is static and bound by a test instead (A7).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1. Git switches on every constructed spelling | Given a scratch repository, when each Axis-1 × Axis-2 shape runs under bash, then git creates or switches; a spelling it refuses leaves the class and is listed | Executed in phase 1 against the installed git (2.54.0), in a scratch repository outside the tree, probe deleted; the table goes in `phases/phase-1.md` |
| A2. `classify` reads every spelling, with its tree | Given a repository with branch `feature/x` and file `README.md`, when `classify` reads each Axis-2 spelling of each creating option, then `create+switch`; each V shape naming `feature/x` → `switch`; each restore twin → `None` | Executed: parametrized cases in `tests/test_guard_resolves_the_tree_it_judges.py`, red at `94d7b2e0` |
| A3. `switch_kind` reads the same words | Given `KINDS`, when the new rows run, then each Axis-2 spelling is `switch`, each V shape is `switch` only where a name is left, `checkout --conflict merge` and `switch --conflict merge` are `None`, and #750's rows are unchanged | Executed: `test_switch_kind_reads_the_words_alone`, new rows red at `94d7b2e0` |
| A4. No constructed switch is silent | Given a dirty `w` under a clean session, when every Axis-1 × Axis-2 × Axis-3 shape git switches on (A1) is read, then the frozen loop's `classify` finds the kind in some segment or `wider_only_kinds` returns it | Executed: a generated case over `_shapes`-style construction, function level (`classify` per frozen segment, then C), plus one shape per Axis-3 position through `main()`; red at `94d7b2e0` with the silent count named |
| A5. No restore twin becomes a question, save the R& rule | Given the restore twins of A4's shapes, when they are read, then none is asked where no `&`- or `|`-led operator cuts the segment (`checkout README.md>/dev/null` and `checkout 2>/dev/null README.md` are silent), and where one does, the question follows §*Which tree*'s rule | Executed: generated; `test_no_restore_is_asked_whatever_the_redirection_and_wherever_it_stands` and `test_a_redirection_word_is_not_read_as_a_branch_name` still pass unchanged |
| A6. Nothing that switches goes quiet | Given the generated shapes, when the build's verdict is compared with `94d7b2e0`'s, then every shape the base asked and the build does not is one git does not switch on (an option's value read as a name, a `-b` after `--`) | Executed in phases 1–2 (a deleted probe); both counts and every newly silent shape in `phases/phase-2.md` |
| A7. The option table binds git | Given the installed git, when a case reads `git checkout -h` and `git switch -h`, then every option it lists as taking a mandatory value is in the table, and the case fails naming the option where one is not | Executed; red with one value-taking option deleted from the table |
| A8. The reduction binds the reader's operators | Given `_redirections()`, when each operator stuck and separate is reduced, then no redirection word is left | Executed; red with one operator removed from the local list |
| A9. The policy says what the guard reads | Given §*Which tree*, when a person reads the first paragraph and the #678 sentence, then they learn that a checkout's and a switch's words are read as git and bash hand them since #764/#738 (owner, 2026-10-04), and the sentence agrees with `switch_kind` clause by clause | Executed: the pin red against the current sentence; read: each clause against a `KINDS` row |
| A10. The frozen file did not move | Given the change, when `tests/test_the_frozen_reading_never_grows.py` runs, then it passes with no case deleted | Executed |
| A11. The prompt budget is counted | Given the corpus 1790993140's phase 3 fixed (27,351 distinct command and directory pairs before 2026-10-03T11:06:22+09:00), when the build's reading is replayed, then the count of new questions is recorded, and so is the count for the quoted-`>` and R& limits | Executed in phase 1 (before) and phase 3 (after), probe deleted; counts in the phase records and, where the policy states a count, in §*Known limits* |
| A12. The records hold | `bin/evidence-check --strict .` exits 0 after the `Re-read ·` rows; `bin/survivor-check` over the range reports none or rows with grounds; `tests/test_no_real_identifiers.py` passes | Executed |

## Data & interfaces

- `hooks/worktree-guard.py`: a static option table for `checkout` and
  `switch`; a reduction of a segment's words to what git is handed; a reader
  that returns (creates, names, has `--`). `classify`'s `switch` and
  `checkout` arms and `switch_kind`'s read through it; `_bare_words` reads
  through the same reduction. The names are the builder's.
- No change to `hooks/cmdline_base.py`, `hooks/cmdline.py`,
  `hooks/worktree_consent.py`, or the §A table's rows and messages. The
  reasons a person reads (`create+switch`, `switch`, C's *switches a branch*)
  are unchanged; what changes is which commands reach them.
- Ledger: the units this work changes are cited by
  `seal/releases/0.18.0.md` K5 and N1 and `seal/releases/0.18.1.md` G1 and
  its K5 re-read; `bin/evidence-check --strict .` names any others.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

Framed 2026-10-04 by framer, before the build.
