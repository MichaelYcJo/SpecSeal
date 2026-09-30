# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — phase 1

<!-- seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | a94e22bc |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 1: a program word behind a redirection or glued to
`(` (`spec.md` P5, P10, W1). One recognizer for every redirection form in P5
and P6, glued and spaced. `command_word` reads past leading redirections for
`git`, `eval` and the string's command word; `_git_options` reads past a
redirection before the subcommand; `understood` refuses a `cd`, a relocator, a
reserved word or an expanding word reached past a leading redirection;
`_is_the_program` reads past redirections and a glued `(`; host words glued
to `(` are recognized in `reparsed_texts` and `command_strings`.

The spawn set the terms for every phase. The base for every "silent at base"
judgement is `86256492`. No shape may read silent where that gate judges it:
each changed reader keeps the base answer and only adds, OR for a boolean and
AND for `understood`. S7 stays green through every phase. Round 1's
non-commit controls, and their relocated copies, stay unasked in attended
sessions. The gate-change lines for `CONTRIBUTING.md` are drafted here. Q3's
redirection half and Q6 are this phase's to answer.

## What this phase found

**The frame holds, measured before building.** Every shape `spec.md` marks
*silent at base* was run through the gate's `main()` at `86256492`, 42 of
them across S1 to S6 and P4, and each was silent there. The two controls the
frame names deny there: a plain `git commit` from an undeclared repository,
and `2>/x/git commit`. Nothing in the frame needed a *no*.

**How decision 1 is built.** No existing reader was changed in place. Each
asks the reading it had at `86256492` first and asks the reading past
redirections only where the first found nothing:

| Unit | Base answer kept by | What is added |
|---|---|---|
| `command_word` | a new `redirections` flag, off by default | reading past a redirection, with a spaced target and a process-substitution target |
| `parse_git` | the base command word first; the second one only where it is not `git` | a `git` behind a redirection; a subcommand behind one (see below) |
| `_git_options` | the same flag | reading past a redirection before the subcommand |
| `_eval_argument` (gate) | the base reading first | an `eval` behind a redirection |
| `names_an_unknown_command` | OR over the two readings of each segment | an expanding word behind a redirection |
| `_is_the_program` | the base loop, unchanged, returns first | redirections, and a runner glued to `(` on the first word |
| `understood` | AND: a False from the base returns at once | a `cd`, relocator, reserved or expanding word reached past a leading redirection |
| the walk's unplaced flag | OR over the two readings | `2>/dev/null nice -n 5 git commit` stands behind a runner's options |
| `reparsed_texts`, `command_strings` | `host_word` only adds a host (its docstring says why) | `(sh`, `(watch`, `(su` and the rest |

The one place an answer is replaced rather than kept is `parse_git`'s
subcommand when the first scan lands on a redirection. `overview.md` records it
as a divergence, with the grounds.

**Q3, the redirection half.** How the splitter hands each spelling back, and
where it is read:

| Spelling | Tokens | Read by |
|---|---|---|
| `2>f`, `>f`, `>>f`, `<f`, `<>f`, `<<<w`, `<<-EOF`, `{fd}>f`, `>!f`, `>>!f` | one word | the recognizer, target glued |
| `2> f`, `<<< w`, `<< EOF`, `<< 'EOF'`, `>! f`, `>>! f` | operator, then target | the recognizer, target spaced |
| `2> >(tee log)` | `2>`, `>(tee`, `log)` | the recognizer, which follows the target to the `)` that closes it |
| `&>f`, `&>>f` at the start of a command | `&` as a separator, then `>f` | the recognizer, because the segment begins with `>f` |
| `>&2`, `2>&1`, `<&0`, `>&-`, `>\|f`, and `&>f` after a word | cut at `&` or `\|` | phase 4's merged view |

None of the redirection spellings is left to a stand-in. The header spellings
are phase 2's.

**Q6: no guard pin moves.**
`tests/test_the_guard_asks_once_per_session.py#COMMAND_WORD_GROUPS` names no
redirected git and no word glued to `(`, and the 26 modules that load the
reader, either gate or the consent writer pass unchanged. So
`docs/worktree-guard-spec.md` has nothing to correct for this phase. What the
guard now does is the stricter reading `spec.md` §*What the worktree guard
sees* describes: it classifies `2>/dev/null git switch x`.

**Executed in real shells** (bash 3.2.57, zsh 5.9, a scratch repository, each
command built in Python):

- Each of these landed a commit: `2>/dev/null`, `2> /dev/null`, `<<<x`,
  `<< EOF`, `2> >(cat)` and `X=1 2>/dev/null` in front of `git commit`, and
  `git 2>/dev/null commit`, all in bash. In zsh, `>!`, `>>!`, `>! f` and
  `>>! f` in front of `git commit`.
- `2>/dev/null cd W && git commit` committed in W and not where the shell
  began.
- zsh answers a leading `{fd}>` with a parse error, and bash 3.2 has no
  `{fd}>`. `overview.md` carries that row to the orchestrator.

**A mutant found a hole in the planted rows, not in the code.** Glued, `>!f`
also reads as the operator `>` with the target `!f`, so dropping zsh's
operators from the pattern changed nothing the rows could see. Spaced, `>!
/dev/null git commit` reads `/dev/null` as the program unless `>!` is known.
The two spaced rows were added, zsh was run on them first, and the mutant is
killed.

**One of phase 3's rows is closed already.** `watch -g 2>/dev/null "$CMD"`
and its spaced twin deny at the end of this phase. `watch`'s joined string is
`2>/dev/null $CMD`, and `names_an_unknown_command` now reads it past the
redirection. Phase 3 decides what that leaves for its `watch` row.

**Seen red.** The cases were committed at `4e5335b3` before the reader
changed, and 61 failed against the reader as it stood there, which is
`86256492`'s reader. The rows that passed are the controls, the declared-silent
pair and the `2>/x/git` edge, and each of those has to pass at the base. The
pins added after the change were each seen red by the mutant named below.

**Mutants.** Each was applied alone under `PYTHONDONTWRITEBYTECODE=1` and
restored from bytes kept in the driver, never from HEAD. `tests/__pycache__`
was cleared between them, and the tree was clean after the run.

| # | Branch mutated | Killed by |
|---|---|---|
| 1 | the recognizer answers 0 | a string glued to `(`, then every redirected row |
| 2 | a spaced target is not consumed | `2> /dev/null git` |
| 3 | a process-substitution target is not followed | `2> >(tee log) git` |
| 4 | no `{fd}` prefix | `{fd}>f git` |
| 5 | no zsh `>!` and `>>!` | the spaced zsh rows, once added |
| 6 | no herestring or heredoc operators | the `<<<` and `<<` rows |
| 7 | `command_word` ignores its flag | a redirected commit in `$( )` |
| 8 | `parse_git` asks no second command word | the same |
| 9 | `parse_git` asks no second options scan | `git 2>/dev/null commit` |
| 10 | `parse_git` replaces even when nothing follows | `test_a_redirection_with_nothing_after_it_keeps_the_base_subcommand` |
| 11 | `_git_options` ignores its flag | `git 2>/dev/null commit` |
| 12 | `names_an_unknown_command` asks one reading | `sh -c '2>/dev/null $CMD'` |
| 13 | `_eval_argument` asks one reading | `2>/dev/null eval "$X"` |
| 14 | `_is_the_program` has no second loop | `2>/dev/null watch` |
| 15 | no glued `(` on the first word there | `(nice watch)` |
| 16 | a redirection target past `watch` still counts | the `watch as a redirection's target` control |
| 17 | `understood` asks no second reading | W1 |
| 18 | a `cd` past a redirection is understood | W1 |
| 19 | the prefixes are not kept in front of it | `time 2>/dev/null cd U`, added for it |
| 20 | the walk's unplaced flag from one reading | `2>/dev/null nice -n 5 git` |
| 21 | `host_word` takes nothing off | `(sh -c)` |
| 22 | `reparsed_texts` back to `basename` | `(sh -c)` |
| 23 | `command_strings` back to `basename` | `(sh -c "$CMD")` |

**Verification.** Executed at `a94e22bc`: the 26 test modules that load
`hooks/cmdline.py`, either gate, the consent writer or the implementer notice,
1255 passed and 1 skipped, exit 0.
`tests/test_no_shape_the_base_stops_reads_silent.py` passed before the change
and after it. The frame's 42 shapes through `main()` at `86256492` and at the
head of the phase: 12 moved from silent to deny, none moved from deny to
silent, and the controls were unchanged. The rider on `_git_options` drifted
with the edit, and was re-read and re-stamped. Its claim is untouched,
because the values of `--git-dir` and `--work-tree` are still discarded. The
full suite is not run here. It is the sealer's.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.**

- *A test seen red.* 61 cases failed at `4e5335b3` against `86256492`'s
  reader, before the change. Every changed branch has a mutant a case kills.
- *Failure direction: it blocks more, never allows more.* Every reader asks
  its `86256492` reading first and adds. `understood` only adds a False. A
  wrong read costs a stop and never a silence.
- *Prompt budget.* A commit, an `eval`, a `watch` or a shell string behind a
  redirection, or glued to `(`, now meets the gate: one refusal, then a prompt
  per re-issue in an attended session, and a refusal under `automation`. A
  command that commits nothing meets a new stop in one shape only. That is W1
  into a declared repository, `2>/dev/null cd W && git commit` with both
  declared (`spec.md` (d)). Phase 6 counts it over the recorded commands.
- *Why nothing cheaper.* Leaving these unread is a commit nobody judges, and
  bash landed each one. Changing the splitter moves every segment (`plan.md`
  Alternatives B).
- *Platform honesty.* String reading only. bash 3.2.57 and zsh 5.9 were run.
  bash 4.1's `{fd}>` was read, not run. Windows is CI's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
