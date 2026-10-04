# Implementation Plan: 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

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

The worktree guard's two readers of a `checkout` or `switch` segment —
`classify` with a tree, `switch_kind` without one — read one word reader
that sees what git's option parser sees after bash has taken the
redirections off. A creating option in any spelling git accepts is a switch,
an option's value is never a name, and a redirection is never a word.
`hooks/cmdline_base.py` is untouched; the per-subcommand rule in `classify` is
what the owner reopened on 2026-10-04 (`spec.md` §*The frozen reading, and
what the owner reopened*).

## Technical context

- `hooks/worktree-guard.py#classify` — the `switch` arm tests
  `a in ("-c", "-C")` and "any word not starting with `-`"; the `checkout`
  arm tests `a in ("-b", "-B")`, then `--`, then `-`, then the first word not
  starting with `-` against the tree (path → restore; ref or `origin/<name>`
  → switch; the `)` peel). Byte-identical to `86256492`'s (read 2026-10-04).
- `hooks/worktree-guard.py#switch_kind` — the same order with no tree; #750's
  docstring states it.
- `hooks/worktree-guard.py#wider_only_kinds` — candidate C. Each view's kind
  is `switch_kind(wide.parse_git(_bare_words(view)))`; each frozen source's
  is `switch_kind(parse_git(tokens))` on the raw words. A raw `2>/dev/null`
  or `feature/x>/dev/null` reads as a name there, which is how #738's
  shapes are subtracted.
- `hooks/worktree-guard.py#_bare_words` — the reduction C's views get today,
  through `wide.unglued` and `wide._without_redirections`.
- `hooks/worktree-guard.py#main`, the loop over `walk_command` — judges the
  first segment of each kind by `classify`, then `quiet()` hands the judged
  kinds to C.
- `hooks/cmdline_base.py#split_segments_with_separators` — `shlex` with
  `punctuation_chars=";|&"`: `<` and `>` stay inside words, `&` and `|` cut
  segments. So R1–R5 arrive in one frozen segment, and R& arrives cut.
- `tests/test_guard_resolves_the_tree_it_judges.py` — `KINDS`, `RESTORES`,
  `ASKABLE`, `_redirections()` (derived from `cmdline._REDIRECTION`),
  `_shapes(verb)` (every operator at every position, stuck and separate),
  `POLICY_RULE`, and the sentence pin in
  `test_the_guard_policy_says_a_hidden_file_checkout_is_asked`. The
  generators exist; the build extends their verbs along `spec.md`'s Axis 1 and
  Axis 2 instead of writing a second generator.
- Git's grammar: `git help cli` §*Enhanced option parser*, and the option
  lists from `git checkout -h` and `git switch -h` on git 2.54.0.

**What breaks in six months.** Git adds a value-taking option to `checkout`
or `switch`. Until the table learns it, its separate value reads as a name:
`classify` looks it up as a ref, and `switch_kind` counts a switch. That is
today's behaviour for every value-taking option, so it is no regression, and
A7 fails on the first machine whose git lists the new option. The other
drift is abbreviation: a prefix unique in 2.54's table may be ambiguous in a
later git, which then refuses the command — the reading asks where nothing
moved, the cheap direction.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Round 3's fence in C** (`_names_anew`, on 🟡 15 of 1790993140), plus glued values in `switch_kind` | Fixes no #764 shape: once `switch_kind` reads `-bNAME`, the frozen side holds the switch and C subtracts it, so the fence would need a second exception for every Axis-2 spelling. And a stuck restore (`checkout README.md>/dev/null`) asks, the trade the fence's own run measured | Rejected. With `classify` reopened, the tree can tell `README.md` from `feature/x`, which is what the fence could not |
| **B. Name #738 as a known limit with its count** (the issue's second option) | The 128 R1/R3 shapes #737's build counted keep switching unasked over a dirty tree, and the owner has already opened the reader that fixes them | Rejected; kept as the default if the owner answers `questions.md` P1 the other way |
| **C. `classify` reduces through `hooks/cmdline.py`** (`unglued`, `_without_redirections`) | The guard's per-segment answer then moves whenever the commit gate's reader does — the coupling #689 cut — and `classify` loses its answer when the wider reader fails to load, where today it keeps its rows | Rejected. One local reduction, bound to `_REDIRECTION` by a test (A8) |
| **D. Read the option table from the installed git at hook time** | A `git <sub> -h` per event, on every Bash call that holds a checkout, and its text is not an interface | Rejected; a static table bound by a test (A7) |
| **E. Teach `hooks/cmdline_base.py`** | Deletes the S11 case and breaks P4's *byte-pinned, with no rule added*; every reader of the frozen file moves, the consent writer included | Rejected; not what the owner reopened |
| **F. A tree inside C**, so R& restores stay silent | C works on the wider splitter's segments; the frozen walk's directories are per frozen segment, and the two splitters cut differently, so the mapping is a design of its own (round 3 of 1790993140 named it) | Rejected for this ticket; R& is named in §*Known limits* with its corpus count |
| **G. Only the separate and stuck short forms** (`-b N`, `-bN`) | Leaves S3, S4, L1–L4 and V silent — the class enumerated by an example, which is how an earlier run spent a reopening | Rejected |
| **H. One local word reader, read by `classify` with its tree and by `switch_kind` and C without one** | Above (*What breaks in six months*); and a quoted `>` in a name is cut, named as a limit | **Chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The measurements the build tests against, and nothing in the tree but `phases/phase-1.md`: the git truth table for `spec.md`'s Axis 1 × Axis 2 (A1); the count of generated Axis 1 × 2 × 3 shapes silent at `94d7b2e0` (function level: `classify` per frozen segment, then C), by axis; the corpus counts of the quoted-`>` and R& shapes and of base questions over the 27,351 pairs (A11, before) | Executed in a scratch repository and a scratch copy outside the worktree, under bash, probes deleted (contract §7); the commands and counts in `phases/phase-1.md` | 7b69bdf4 |
| 2 | The word reader and its table; `classify`'s `switch`/`checkout` arms, `switch_kind`'s and `_bare_words` reading through it; §*Which tree*'s first paragraph, the #678 sentence and §*Known limits* rewritten, the pin moved, in the same commit as the code (§14); `KINDS` rows, `classify` cases, the generated A4/A5 property, A7, A8 | Executed: each new case red at `94d7b2e0` and green after (§15); A6's comparison (a deleted probe); the touched modules — `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_worktree_guard.py`, `tests/test_the_guard_asks_once_per_session.py`, `tests/test_the_frozen_reading_never_grows.py`, `tests/test_a_creation_is_judged_before_git_runs.py`, `tests/test_one_word_one_meaning.py` | |
| 3 | The after-count over the corpus (A11); `changelog.md`; `seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md` with the new rows and the `Re-read ·` rows for every released row the change drifted; `overview.md` | Executed: the corpus replay (deleted probe); `bin/evidence-check --strict .`; `bin/survivor-check` over the range; `tests/test_no_real_identifiers.py` | |

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

## Operational impact

No migration, environment variable or dependency. The behaviour a person
meets changes in two directions, and the pull request states both under
`CONTRIBUTING.md` §*What a change to a gate must carry*:

- **Failure direction — the guard asks more.** Every constructed shape git
  switches on reaches §A's rows, or C's question for an R& shape; an R&
  restore of a file name is asked, as §*Which tree* already says of `&>`.
  The guard goes quiet only where git's parser takes the word as an option's
  value (`checkout --conflict merge`), or as a pathspec after `--` (a `-b`
  written after `--`), and A6 is what has to show git switches on none of
  those.
- **Prompt budget.** Phase 3's after-count over the 27,351 recorded pairs.
  Round 3's fence, which asked on a superset of the R1/R3 restores, fired on
  0 of them; a nonzero count here is a finding to report, not to absorb.
- **Platform honesty.** The reduction follows bash's grammar, which the
  guard already assumes. The git half is measured on the one git this machine
  has (2.54.0); CI's git version answers A7 on its own run.
