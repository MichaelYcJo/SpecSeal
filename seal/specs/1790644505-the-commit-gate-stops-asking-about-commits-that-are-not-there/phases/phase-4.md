# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — phase 4

<!-- seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 8c552f50 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 4, added by the orchestrating session at `d3e37312`
after phase 1 found the hole and the orchestrator confirmed it at `3911a8cf`:
#669, a commit after a reserved word on the same line (`for …; do git commit`,
`while …; do git commit`, `if …; then git commit`) is read as no commit. The
owner's standing rule puts the fix on this branch.

The message that started the phase set its terms. This is the one change to
`hooks/cmdline.py` in the item, and the only permitted direction is stricter:
after a reserved word that starts a command list, read the next word as the
command word, and where it cannot be certain, stop rather than read silent.
#669's shapes and their `else`/`elif`/`{ …; }`/`( … )`/`!` neighbours are
each seen red at `ade83e4e`. S7 is green before and after. One mutant per
changed branch, killed with `PYTHONDONTWRITEBYTECODE=1`. The ledger rows, the
changelog entry naming #669, rows it drifts re-read, and the gate-change lines
here. The phase record states why no shape the base judges becomes silent,
and `spec.md`'s and `overview.md`'s statements that `hooks/cmdline.py` is
byte-identical are corrected.

## What this phase found

**The multi-line spelling already had the answer.** The base judged every one
of these commands when it was written across lines: `do` stood on a line of
its own, `understood` refused it, and the commit on the next line was a
segment with an unresolved directory. So the fix does not invent a directory
for the one-line form. It gives the segment the one its multi-line spelling
already had, and `test_the_one_line_spelling_is_judged_as_the_multi_line_one`
holds the two spellings against each other, with the multi-line half passing
at the base.

**What the reading does now** (`hooks/cmdline.py#command_word`, called by
`parse_git` and `walk_directories`):

- After `do`, `then`, `else`, `elif`, `if`, `while`, `until` or `{`, the next
  word is the command word, with a leading `(` taken off the remainder. The
  segment's directory is unresolved. That covers loop and conditional bodies
  and also loop conditions, which run again after a body that may have moved
  the shell.
- `!` and `time` are read past with the directory kept, because they stand in
  front of a command without opening a list.
- Inside a `case` arm, a function definition (`f()`, `f ()`, `function f`) or
  a coprocess, no position names the command word. The first `git` word in the
  segment stands in for it, and the directory is unresolved. A wrong stand-in
  is a stop, never a silence. This is the "cannot be certain" branch.
- `for`, `select`, `case`'s word and `in` are followed by names and words,
  not commands, so `for d in git commit; do :; done` reads nothing. That was
  the base's answer too, and a case pins it.
- A directory the walk already could not read keeps its reason, so `cd "$WT"
  && if git commit …` still says to write the path out.

**Why no shape the base judges becomes silent.** There are two halves, and
both were read and then run.

1. *The invocations are a superset.* For a segment where the base found a
   `git` command word, every token before it was an assignment or a wrapper,
   and `command_word` reads past exactly those in the same order. It finds the
   same word, and `parse_git` returns the same tuple. The new reading only
   continues at words where the old loop broke with no `git` (a list opener,
   `!`, or an unplaced construct), and there the base returned `None`.
2. *The directories only change where the base found nothing.* The walk marks
   a segment's directories unresolved only when `command_word` read past an
   opener or into an unplaced construct. By point 1 those are exactly segments
   in which the base found no git command, so no invocation the base judged
   has a different directory. The states carried to later segments are
   untouched. An unresolved directory is itself a stop wherever the session's
   repository opted in, and it can be silent only where the session never
   opted in. There the base was silent for the same command, because it found
   no invocation at all.
   **Corrected 2026-09-29 by round 1's fix pass.** Both points hold for
   segments, and the conclusion drawn from them did not. The gate's fallback
   for a command the splitter could not finish is not a segment, and it ran
   only while nothing was found. So `for d in a; do git -C W commit -m x;
   done; echo $'it\'s'; git commit -m y`, with W declared, read silent where
   the base denied, because the newly found commit in W took the session's
   own directory out of the judgment. The fallback now stands beside what was
   found, and S7 carries that row.

The measured half: S7, the corpus of every shape the base stops, passed
before the change and after it. So did the 33 modules that load the gate, the
reader, the guard or the consent writer (1232 passed, 2 skipped, exit 0), with
no existing case edited.

**The guard reads more too.** `parse_git` is the one reading the worktree
guard and the consent writer use, so a `git switch` or `git worktree add` in a
loop body is now read by them as well. For the guard that is stricter
(judging a switch it did not see) or equal. For the consent writer, a creation
it now records is one the guard now also asked about. Their suites passed
unchanged, including
`test_a_command_with_both_is_never_weaker_than_either_alone`.

**Seen red.** Every shape was silent at `ade83e4e` (`94f22891` committed the
cases before the reader changed): 46 of the module's 47 cases failed there.
The one that passed was the control that reads nothing, which is its job.

**Mutants.** Each was killed, one at a time, under `PYTHONDONTWRITEBYTECODE=1`,
restored, and checked against the commit with `git diff`:

| Branch mutated | Killed by |
|---|---|
| the `!` prefix not read past | 6 cases (`a negated commit`, `a negation in a body`, the guard case, the declared case) |
| the list-opener branch removed | 33 cases |
| the remainder after an opener not stripped of `(` | the two subshell-in-a-body shapes and the declared case |
| an opener not marking the directory unplaced | `an if condition`, `a while condition`, the multi-line pairing, the declared case |
| `UNPLACED` not consulted | `a case arm`, `a coprocess`, `a function keyword` |
| the `)` test dropped | `a function body`, `a later case arm` |
| the spaced `()` test dropped | `a spaced function body` |
| the stand-in `git` not marking the directory | all five unplaced shapes |
| the walk's unplaced branch removed | 9 cases |
| an unresolved directory re-wrapped | `test_a_directory_already_unreadable_keeps_its_reason` |

**What the reading still does not reach** (`overview.md` §*Not done*).
`exec git commit`, `timeout 5 git commit`, `nice git commit`, `xargs git
commit`, and a commit inside `$( … )` or backticks each return no invocation
at this phase's reader (executed). None is behind a reserved word, so the
closed list does not reach them. They are the open list of wrappers the policy
refuses to chase. The base already had these silents; this branch did not
introduce them.

**Records.** Ledger rows E10–E12 were added. E2 and E7 were corrected in
place, because E7 claimed "what the gate stops is unchanged". E9 was re-read
because the policy edit drifted both of its anchors. No row outside the
fragment drifted: `bin/evidence-check .` read 2711 ok, 0 drifted, exit 0. No
ledger row anchors `parse_git` or `walk_directories`, and the `RIDER` in
`parse_git` that described this hole was removed with it. `rider_check.py`
exit 0. `survivor-check --range ade83e4e..HEAD`: no removed wording still
standing. `correction-check`: exit 0. The docs, fold, one-word and hygiene
modules: 187 passed.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.** These are for #669's change; phase 1's lines stay for the rest.

- *A test seen red.* Every new case was run against `ade83e4e`'s reader
  before the change, and 46 of 47 failed. Each changed branch has a mutant
  that a case kills.
- *Failure direction: it blocks more, never allows more.* The reader finds
  commits where it found none, and every segment it newly reaches gets an
  unresolved directory, which is a stop. The argument above shows that no
  invocation the base found is read differently. A wrong read (a `git` word
  in a case pattern, say) costs a stop, never a silence.
- *Prompt budget.* A commit written after `do` or `then` on one line now
  meets the gate. In an attended session that is one refusal and then a
  prompt, the same as its multi-line spelling always cost. In an automation
  session it is a refusal and no prompt. The expected volume is small: the
  shapes are the ones an orchestrator writes when it loops over work items,
  and contract §17 already tells it to write each commit out instead.
- *Why nothing cheaper reaches the same guarantee.* The alternative is to
  keep reading nothing, which is a real commit nobody judges. The multi-line
  spelling already pays this stop.
- *Platform honesty.* This is pure string reading, with no process
  inspection. The cases ran on macOS; Windows is CI's `windows-latest` leg.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the `RIDER` in `hooks/cmdline.py#parse_git` describing a reserved word the reader did not read past | none: the hole it recorded is closed, and `docs/commit-review-gate-spec.md` §*A `cd` the gate cannot read* now states the reading |
| `overview.md`'s *Not done* bullet on the reserved-word hole, rewritten as done | the same bullet, now saying phase 4 closed it, so phase 1's pointer still lands |
