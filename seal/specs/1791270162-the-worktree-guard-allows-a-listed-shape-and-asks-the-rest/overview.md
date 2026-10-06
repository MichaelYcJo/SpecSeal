# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

## Why this work exists

The worktree guard stops predicting a branch switch from a command's text and
instead lets through only git commands it positively knows leave the branch
where it is, stopping the rest only in a tree where a switch would matter.

## How far it got

**Phase 1 is closed, and it is the only phase built.** It measured the
recorded runs with a deleted probe and put nothing in the tree but the record
(`phases/phase-1.md`, `questions.md` M1–M3):

- M1: 31,193 distinct (command, cwd) pairs in cut 1 and 33,220 in cut 2,
  8,960 and 9,695 of them holding git, 55 subcommand words. Cut 1 reads
  above 25,741, not below it, and the difference is not reconciled.
- M2: as written, the build stops 871 cut-2 pairs tree-blind, 570 of them
  pairs today's guard does not stop even at its maximum. Today's guard stops
  no pair the build lets through, and candidate C fires on none.
- **M3 is not zero.** 595 distinct cut-2 pairs stop with no plain rewrite
  the stop's text can name, and 575 of them are a `$( … )` body holding only
  listed git. With such a body read as listed, M3 is 34.

**The owner answered P1–P4 on 2026-10-06, all (a)** (`questions.md` at
707872aa), and phase 2 was built on those answers.

**Phase 2 is closed** (`phases/phase-2.md`). `main` reads each segment as
listed, a switch, a creation or unrecognised; an unrecognised shape stops
before the ladder only where the tree matters, a `deny` under the press or in
an ACTIVE tree and an `ask` otherwise; a substitution body is read through
the same shapes. `classify`, the option table, the lookups and candidate C
are still defined and no longer reached. 48 cases of
`tests/test_guard_resolves_the_tree_it_judges.py` assert those readings and
fail now; they are phase 3's to retire or rewrite, after the #841 rebase.
M3 after the owner's answers, by a phase-2 probe with the build's own
readers on its own pair definition: 16 pairs in cut 1 and 25 in cut 2 hold an
unlisted subcommand, `update-ref` 16 of the 25; every other stopped pair now
has a plain spelling the stop names.

**Phase 3 is closed** (`phases/phase-3.md`), after #841 landed and was
merged in (W4). The readings are gone from the guard, every case that
pinned one is retired with it or rewritten to the shape it now meets, and
18 released ledger rows took a `Corrected ·` row, D1 of 0.18.2 among them.
Settling the cases found three silences phase 2's build left where the
tree matters, and phase 3 closed each: a redirection hiding `worktree`'s
`add` or `stash`'s `branch`, only the first unrecognised shape's tree being
read, and a hidden git's own `-C`. On phase 1's pair definition, reproduced
exactly, the build stops 315 and 333 pairs tree-blind, 55 and 57 that
today's guard does not, and M3 is 14 in each cut.

**Phase 4 is next**: the policy document, the changelog fragment, the
ledger rows for S1–S14, and this memo.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A substitution body holding only listed git | `spec.md` In 1: a non-git segment "where its text holds a substitution body (`$( … )`, a backtick pair, `<( … )`) holding the bare word `git`" is unrecognised; phase 1 measured that clause as 575 of 595 no-rewrite pairs | nothing built; put to the owner as `questions.md` P2 | a nonzero M3 stops phase 2 for the owner's rows, as M3's own row says |
| `eval`'s string | `plan.md` names `hooks/cmdline.py#command_strings` for a shell string's words; it returns no string for `eval "git switch x"`, which the probe's first self-check caught | the probe joined `eval`'s words; phase 2 decides its own reader (W3) | the self-check line of `phases/phase-1.md` |
| The stop in an ACTIVE tree, without the press | `spec.md` In 3: "Without the press the stop is an **`ask`**", and S3 lists ACTIVE among the states that answer `ask` / phase 2 built a `deny` there whatever the press | the `deny`; `spec.md` In 3 and S3 changed and marked as inferred, and `questions.md` P5 opened for the owner | `docs/worktree-guard-spec.md` §A row 1: "ACTIVE session present \| deny — steer to a worktree", for "Branch switch (`git switch` / branch-form `checkout`)". Policy outranks the spec (`skills/implement/SKILL.md` §1), and an `ask` there lets one approval run `git checkout <branch>` over a working session, which the base never allowed. The deny costs nobody a prompt: the model rewrites, as under the press |
| A creation on the same line as an `ask` stop | `spec.md` In 3 names the stop's two readers and nothing about a creation beside it / phase 2 judges the creation first on the `ask` path (`stop_unrecognised`'s `before_ask`) | judged first, as `choose` does | `tests/test_the_guard_asks_once_per_session.py#test_the_guard_is_never_silent_where_the_writer_records` failed without it: `git worktree add ../wt f && git checkout feature/x` in an IDLE tree drew an `ask` about the checkout, and approving it would have created the worktree with the creation question never put |
| Where a substitution body is read | `spec.md` Data & interfaces: `shape_of(tokens)` returns None for a segment holding no "string, body or hidden git" / phase 2 reads bodies from the command's text (`_command_findings`), not per segment | the command's text | the frozen splitter takes the quotes off a segment's tokens and cuts a body at its `;` and `\|`, so a body read from one segment's tokens is not the body the shell runs. The cost: a body is judged in the session's own tree, not the tree of the segment around it (`Not verified` below) |
| A shell's string | W3's default names `command_strings` / phase 2 reads `reparsed_texts` | `reparsed_texts` | it returns every word that might be the string (`bash -o errexit -c '…'`), so a string it reads too widely costs a stop, while one `command_strings` misses costs a silence |
| Which unrecognised shape's tree is read | `plan.md` phase 2: "`main`'s walk keeps the first switch, the first creation and the first unrecognised shape with its tree" / `spec.md` In 2: "An unrecognised shape is judged only where **the tree matters** for the tree its segment names" | every shape's own tree, first one first, each tree looked up once (phase 3) | `git checkout README.md && cd w && 2>/dev/null git switch x`, `w` dirty and the session's tree clean, was silent at `9c03ae85`, where candidate C had asked at the base; the plan's sentence borrowed #630's first-switch rule, and In 2 speaks of each shape |
| The tree of a git only the wider reader reads | `spec.md` In 4: `judgeable` and `segment_cwd` "name the tree a segment acts on and do not change"; §*Which tree* keeps each `-C` the frozen reading's / phase 3 composes the wider reading's `-C` for such a segment (`_finding_tree`), onto the directory the frozen walk placed it in | composed | `2>/dev/null git -C W switch x` was judged in the tree it was typed from, so with `W` dirty or held by an ACTIVE session it was silent, where C had asked at the base. `judgeable`, `segment_cwd` and the walk are untouched, and only a segment the frozen reading reads no git in takes the wider `-C`; whether §*Which tree* names it is phase 4's, and the warden's to read |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ Why cut 1 reads 31,193 pairs where 1791119071's phase 1 read 25,741 over more transcripts | phase 3 reproduced phase 1's own definition, (command, the entry's `cwd`), at 31,193 exactly, so before and after compare on one count (`phases/phase-3.md`); 1791119071's 25,741 cannot be re-run and stays unreconciled, and no figure here rests on it |
| Which recorded subcommands leave HEAD's branch where it was, beyond the ones `spec.md` In 5 names (`clone`, `init`, `config`, `archive`, `apply`, `gc`, `update-index`, `format-patch`, `count-objects`, `help`): judged by reading what each does, not run against git | the warden's first round, reading `LEAVES_THE_TREE`'s 49 rows against what each subcommand does; phase 2 wrote the list with its counts and did not run the judgment either |
| Every count is tree-blind, so each is an upper bound on stops where the tree matters | phase 3's re-read, and the pull request's prompt budget, which says so |
| A substitution body and an untokenizable command are judged in the session's own tree, so `cd W && F=$(git checkout x)` with `W` dirty and the session's tree clean is silent | the warden's first round: whether that limit is named in `docs/worktree-guard-spec.md` §*Known limits* in phase 4, or a body takes the tree of the segment it sits in |
| Windows: every tree state there reads *detection unusable*, so every unrecognised shape stops there; read, not executed, as for every Windows claim in this guard | the repository owner, at the pull request |

## Not done

Phase 4. #841's fragment row S5 and its records still name cases and
helpers phase 3 retired; they are #841's to correct, not this work item's
(`phases/phase-3.md` §*The ledger*).

## Fed back into the spec

- `spec.md` In 1: a substitution body is read through the same shapes,
  recursively, and the clause that made any body holding `git` unrecognised
  is gone. The owner's answer P2 (a), fed back during phase 2.
- `spec.md` In 3: the plain spellings for an unlisted subcommand (P3 (a)),
  an untokenizable command (P4 (a)) and a redirection read as the
  subcommand (W3). Fed back during phase 2 from the owner's answers.
- `spec.md` In 3 and S3: the stop is a `deny` in an ACTIVE tree whatever the
  press, and a creation on the line is judged first on the `ask` path.
  *Inferred during implementation*; `questions.md` P5 puts the first to the
  owner.
- `spec.md` Data & interfaces: `shape_of` reads no body, `tree_matters`
  takes `seen`, `stop_unrecognised` takes the findings, the tree state and
  `before_ask`. *Inferred during implementation.*
