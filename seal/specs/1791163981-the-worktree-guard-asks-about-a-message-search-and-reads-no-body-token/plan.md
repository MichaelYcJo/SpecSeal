# Implementation Plan: 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-05 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

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

Two reads in `hooks/worktree-guard.py` stop disagreeing with the program that
runs the command, each built so it can only make the guard stricter.
`is_ref` looks a `checkout`'s name up the way `git checkout` resolves it — a
message search, a merge-base shorthand, a guess from any remote — OR-ed with
today's lookup (#790). `has_token` reads a consent token only where the
command as written AND the command without its here-document bodies both
carry it, through #773's `tokens.without_bodies` (#780). `hooks/cmdline_base.py`
is untouched (`spec.md` §*The frozen reading, and what this work does not
reopen*).

## Technical context

Read 2026-10-05 at `860d77da` (the routing commit on `a3aa139a`).

- `hooks/worktree-guard.py#is_ref` — one `git rev-parse --verify --quiet
  <name>^{commit}`, run in `cwd`, no timeout, any exception read as "no".
  Its only callers are `classify`'s `checkout` arm: the first name, then
  `origin/<first>`, then the `)` peel, which calls both again per character
  peeled.
- `hooks/worktree-guard.py#classify`, `checkout` arm — `read_switch_words`
  first (a creating option → `create+switch`; a word after `--` → restore;
  `-` → switch), then the path test (skipped for a bare `--`), then the
  lookups. `switch` arm — any name is a switch; no lookup.
- `hooks/worktree-guard.py#switch_kind` and `#wider_only_kinds` — tree-blind;
  `switch_kind` reads every `checkout` name but `.` as a switch, so a name
  `classify` fails to resolve is subtracted by candidate C. Nothing here
  changes either.
- `hooks/worktree-guard.py#has_token` — `_tokenize(command)` (the frozen
  splitter, Windows backslashes doubled), any token equal to the wanted one
  or equal once `()` are stripped. Called at `guard_worktree_creation` for
  `[worktree-ok]` and in `main`'s switch ladder for `[shared-tree-ok]`.
  `_judgment_text` already drops bodies through
  `cmdline_base.drop_heredoc_bodies` for the judgment read.
- `hooks/tokens.py#without_bodies` — `one_heredoc.reduce`'s text where the
  one shape matches, else `hooks/cmdline.py#drop_heredoc_bodies`; imports
  both lazily, so it raises where `hooks/cmdline.py` cannot load. `given` is
  the AND this work copies.
- `tests/test_guard_resolves_the_tree_it_judges.py` — `KINDS`, `_shapes`,
  `_read_apart`/`_kinds_read`, the `a_branch_and_a_file` fixture (which
  replaces `is_ref` with a set lookup, so the C1–C3 cases need a fixture of
  their own with a real git), `test_the_guard_policy_says_what_it_reads_past_the_base`,
  `test_a_broken_wider_reader_costs_only_the_question`,
  `test_the_retry_token_survives_a_closing_parenthesis`.
  `tests/test_worktree_guard.py` holds the other `has_token` cases.
  `tests/conftest.py#repo` is the repository the guard tests build on.
- Git's grammar: `git help checkout` (the `<branch>`/`<start-point>`
  entries: `@{-N}`, `<a>...<b>`, the guess) and `gitrevisions(7)`, git 2.54.0.

**What breaks in six months.** Git adds a single-revision syntax. Where it
survives the `^{commit}` suffix the base already reads it; where it does not,
the second step (resolve, then peel by object name) still reads it, because
no suffix is appended to the name at all. A syntax that `rev-parse --verify`
cannot read the way `<a>...<b>` cannot would be silent until the guard
learns it, which is today's behaviour for every such form; A1's construction
is the place a later run re-measures. On the token side: a body reader
change in `hooks/cmdline.py` moves what `has_token` drops, and the AND keeps
any such move on the strict side.

**Cost, stated.** The OR runs the new lookup only where today's fails. A
name that is a ref costs the one call it costs today. A name that is no ref
and no path (a typo) costs today two calls and the build up to five
(the no-suffix resolve for the name and for `origin/<name>`, and one listing
of the remotes' branches); each is a local `git` of a few milliseconds. A
`...` name adds one `merge-base`. `has_token` adds one body-free tokenization
of the command, no process.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Read a `:/` word as a switch outright** (the issue's second option) | Tree-blind for a reader that has a tree: a pattern that matches nothing, which git refuses, is asked; and it fixes `:/` alone, leaving `<a>...<b>` and the non-`origin` guess silent — the class closed by an example | Rejected |
| **B. Special-case each syntax that breaks under the suffix** (`:/` → no suffix, `...` → merge-base) | Correct for the two members known today, but the next syntax that absorbs a suffix needs another case; the list is the enumeration that rots | Rejected for C1. C2 keeps a rule of its own because no `rev-parse --verify` reads it at all |
| **C. Replace the lookup with resolve-then-peel** (no OR) | Whether resolve-then-peel answers "yes" for every name `<name>^{commit}` does is a property of git, not of this code; one shape where they differ (a path in `<rev>:<path>` that itself ends in a suffix) turns a base question into silence | Rejected. The OR makes "never quieter" hold by construction, and A4 shows it |
| **D. One process: `git rev-list --no-walk -1 <name>`** | `rev-list` accepts the range forms `checkout` refuses and reads `<a>...<b>` as a symmetric difference, not a merge base, so it answers a different question | Rejected |
| **E. Keep the guess at `origin` only and name the rest a limit** | A repository whose remote is named anything else (`upstream`, a fork) switches unasked on every guessed branch, by the same cause as `:/` | Rejected; the default of `questions.md` P1 |
| **F. `has_token` over `tokens.without_bodies` alone, no AND** | Taking a body out can make a split succeed that failed on the raw text, and a token that split reads is one the command as written never offered (#773's reason for its AND) | Rejected |
| **G. On a broken wider reader, fall back to the base read** | The defect #780 closes comes back whenever `hooks/cmdline.py` fails to load | Rejected |
| **H. On a broken wider reader, read no token** | `[worktree-ok]` can no longer pass the single-stream creation deny, which has no `ask` behind it: a loop with no way out, the failure `has_token`'s parenthesis comment records | Rejected |
| **I. `tokens.without_bodies`, AND-ed with the base read, falling back to `cmdline_base.drop_heredoc_bodies`** — the frozen body reader the guard's judgment read already uses — where it cannot load | Two body readers can disagree on a body the frozen one does not see; the AND keeps that disagreement on the strict side, and it arises only with `hooks/cmdline.py` broken | **Chosen** for #780 |
| **J. Resolve-then-peel OR-ed onto the base lookup; a merge-base rule for `...`; the guess over every remote OR-ed onto `origin`** | Above (*What breaks in six months*, *Cost*) | **Chosen** for #790 |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The measurements the build tests against, and nothing in the tree but `phases/phase-1.md`: M1, the git truth table for every C1–C3 form × carrier and `a3aa139a`'s `classify` verdict on each (`spec.md` A1); M2, whether resolve-then-peel and the merge-base rule answer every form git moves on; M3 before-counts, both readers, over the two corpus cuts (A12) | Executed in a scratch repository and a scratch copy of `a3aa139a`'s `hooks/` outside the worktree, probes deleted (contract §7) | 5c7cf3ca |
| 2 | #790: `is_ref`'s second step and the `...` rule; the guess over every remote; the real-git fixture and the A2, A3, A5 cases; the generated A4 comparison; §*Which tree*'s first paragraph and §*Known limits* amended and the pin moved, in the same commit as the code (§14); the `KINDS` comment rewritten with round 2's words | Executed: each new case red at `a3aa139a` and green after (§15); the touched modules — `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_worktree_guard.py`, `tests/test_the_frozen_reading_never_grows.py`, `tests/test_one_word_one_meaning.py` | cc7344ca |
| 3 | #780: `has_token`'s AND over `tokens.without_bodies` with the frozen fallback; the A6, A7, A8 cases and the A9 implication case; the docstrings (`has_token`, `_judgment_text`, the module's retry-token paragraph, `hooks/tokens.py`'s rule list), §*Choice sites*' token paragraphs and both READMEs' token rows, pinned, in the same commit as the code | Executed: each new case red at `a3aa139a` and green after; the touched modules — `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_worktree_guard.py`, `tests/test_the_guard_asks_once_per_session.py`, `tests/test_the_old_spellings_reach_the_hook.py`, `tests/test_lease_liveness.py`, `tests/test_worktree_guard_signals.py` (every module that names a guard token, searched 2026-10-05). No module pins the READMEs' token rows today, so their new sentence is pinned beside the §*Choice sites* pin | |
| 4 | M3 after-counts over both cuts (A12); `changelog.md`; `seal/ledger/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token.md` with the new rows and a `Re-read ·` row for every released row the change drifts (`evidence-check --reverify --into`); `overview.md` | Executed: the corpus replay (deleted probe); `bin/evidence-check --strict .`; `bin/survivor-check` over the range; `tests/test_no_real_identifiers.py` | |

**The changelog fragment follows the behaviour, not the phase.** Phase 4
writes `changelog.md` for what phases 2 and 3 built. Any later fix pass whose
commits change what the guard does, or what a person reads, updates that
fragment in the same pass, so the entry the release gathers says what the
review rounds added (#797 is that lesson, and sibling item D is building the
check for it).

The two halves are independent. Phase 3 does not read phase 2's code, and
either can close first; they are ordered so the measurement that phase 2
leans on (M1, M2) is fresh when it starts.

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

No migration, environment variable or dependency. What a person meets
changes in one direction, and the pull request states it under
`CONTRIBUTING.md` §*What a change to a gate must carry*:

- **Failure direction — the guard asks more, never less.** A `checkout` git
  moves the tree on through a message search, a merge-base shorthand or a
  guess from any remote now reaches §A's rows. A consent token that sits
  only inside a here-document body is no longer read, so the cannot-tell
  switch rows put their choice and the single-stream creation row denies,
  each naming where to type the token. The OR and the AND are why nothing can
  go quiet; A4 and A9 check it.
- **Prompt budget.** Phase 4's after-count over both corpus cuts, per
  reader. A nonzero count is reported with its shapes, not absorbed.
- **Platform honesty.** The new lookups are `git` plumbing and read no
  process table; the real-git cases run on every platform CI runs. The token
  read follows the frozen splitter's Windows doubling, as `has_token` does
  today.
