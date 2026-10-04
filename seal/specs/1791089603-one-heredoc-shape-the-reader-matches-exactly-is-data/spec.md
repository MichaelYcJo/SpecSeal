# Feature Specification: one heredoc shape the reader matches exactly is data (#739, #763)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

**On purpose, this file holds no command string that passes the gate, old or
new.** The shape is given as a grammar with named slots, the refusals and the
review findings are named by mechanism, and the tests named in the acceptance
table are where the shapes are pinned as fixtures.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/commit-review-gate-spec.md`, the paragraph opening **A file edit goes through the `Edit` tool** | States the rule this work narrows: every body is asked, as shell, whether it commits, and "skipping a body that is only being written to a file would reopen #75, and that trade is the repository owner's to make". The owner made it twice: #739 asks for it, and the redesign comment on PR #760 (2026-10-04) chose this construction. The paragraph is rewritten to name the one shape, with an `Enforced by:` line. |
| `docs/commit-review-gate-spec.md`, the paragraph opening **Two readings that prompted that run stay as they are** | Says every shape `1790635415`'s rounds measured still stops. Each of those still stops under this rule except one corpus row, which moves (Q1). The paragraph says which row moved and on whose decision. |
| `docs/commit-review-gate-spec.md`, the paragraph opening **What stays unread is a program whose operands are a script** | Running a script file is unread at the base. This is why a Python program read from stdin is the same class, and why the line after it can be read the base's way. The class is a program, not data. |
| `docs/commit-review-gate-spec.md` §*Only what the shell would EXECUTE is read as commands* | Bodies are dropped before the walk already. That half is untouched. |
| `hooks/cmdline_base.py`, its RIDER, and `tests/test_the_frozen_reading_never_grows.py` | The frozen reader. It is never edited. |
| `tests/test_no_shape_the_base_stops_reads_silent.py`, module docstring | The owner's constraint for `1790644505`: no shape `release/v0.16.0` stops may read silent. Every row keeps stopping except the one Q1 names. |
| `tests/test_gate_judges_the_repo_it_commits_to.py::test_an_interpreter_fed_heredoc_body_that_commits_stops`, docstring | Legacy #75 rejected a list of shells that run a body, with everything else data. This work names the opposite: one exact shape that is data, and every other body read as today. |
| `skills/agent-contract/SKILL.md` §9 | Tells every agent "the gate reads a heredoc body as shell, on purpose". It changes with the rule (contract §14). |
| `skills/agent-contract/SKILL.md` §12, §13, §15 | The disagreement class is enumerated by construction below. No defence rests on a platform guarantee: no tty, no exec bit, no installed tool. Each new case is seen red first. |
| `CLAUDE.md` §*The goal a design is chosen against* | Unattended verification comes first. Each refusal #739 recorded cost an orchestrator the whole Bash call. |
| PR #760's records on `fix/739-a-here-document-body-is-data-to-the-commit-gate`, under `seal/specs/1791076831-…/`: `rounds/round-1..3-report.md`, `post-review-check.md`; and #763 | The history this design answers. Four passes found that every rule trusting `hooks/cmdline.py`'s body boundaries (`_heredoc_split`, `_quoted_delimiter`, and `drop_comments` before them) fails open wherever that splitter and the shell disagree. Read 2026-10-04. |

## Scope

**In.**

1. A new reader for ONE heredoc shape, written fresh in a module of its own. It shares no code with `hooks/cmdline.py` and uses no shell lexer. It returns the command with the body taken out (the *reduced text*), or *no match*.
2. `hooks/commit-review-gate.py`: where the reader matches, every reading the gate makes **for a commit** reads the reduced text instead of the command. That is the segment walk, the body and substitution readings, and the unparsed-command fallback's substring test. Where it does not match, nothing changes.
3. The moved corpus row (Q1), in `tests/test_no_shape_the_base_stops_reads_silent.py` and in `tests/test_an_automation_run_meets_no_commit_prompt.py`'s four measured shapes.
4. The policy and contract text named in Grounding, each with an `Enforced by:` line.
5. Tests in both directions, plus an agreement test that runs real shells (S6).
6. The changelog fragment and the ledger fragment that `docs/the-record-layout.md` names.

**Out, one line each.**

- **Every code path of PR #760.** The reader is fresh (see *Carry or fresh*).
- **`hooks/cmdline.py`.** No edit, so `drop_heredoc_bodies`, `heredoc_bodies`, `drop_comments` and their four other callers keep their outputs byte for byte. Their boundary disagreements with the shell stay the base's, and they cost nothing there because the base reads every body.
- **`hooks/cmdline_base.py`.** Frozen.
- **`hooks/tokens.py`.** `is_plain` and the consent reads (`given`, `has_marker`) keep reading the command as written. `is_plain` decides whether the reading stands aside for git's hooks (the owner's P7), and reading the full command can only keep the reading in. The consent reads are unchanged at the base and are not this ticket.
- **The worktree guard.** It already drops every body and never reads one back.
- **A body anywhere below the top level**: inside a substitution, a host's string, an `eval` argument, or another body. This includes the commit-message idiom that wraps a quoted heredoc in a substitution. It keeps today's reading, and its false stop is not fixed here. Nothing in #739's three refusals needs it.
- **Unquoted, double-quoted and partly quoted delimiters, and the tab-stripping operator.** Each moves the terminator comparison or the expansion of the body away from a byte-for-byte rule.
- **Refusals 2 and 3 in the forms recorded.** See *#739's three refusals*. Q2 records the trade.
- **What a background reader does with a written file**: a FIFO, a socket path, a watched file, or an executable hook overwritten in place. The base never guarded this class, because writing the same text with `echo` or `printf` is silent there, and so is the Write tool. Naming hook paths would be a list that rots (#760's Q3).
- **Aliases and functions in the user's shell snapshot that rename a consumer word.** The base already assumes a command word means itself.
- **`agents/warden.md` and `agents/smith.md`.** Neither says a body is read as shell. The warden's sentence says a heredoc gives the gate something to read, which stays true, because the line around the body is read. The smith's rider is a dated measurement record.

## The shape

The reader admits a command only when **every** clause below holds. Any clause
that fails means *no match*, and then the whole command is read exactly as at
the base.

**A. Characters.** The command contains no carriage return, no NUL, and no
backslash immediately followed by a newline, anywhere, body included.

**B. The opener is the first line.** The command's first line, from its first
byte to the first newline, is exactly:

```
[ LEAD ] CONSUMER  <one space>  "<<"  "'" D "'"
```

There is no space before LEAD, a single space between every two tokens, and
nothing after the closing quote of the delimiter. The rest of the first line
is empty, so the body starts at the byte after that first newline.

| Slot | Exactly |
|---|---|
| `D` | one or more of `A–Z a–z 0–9 _` |
| `WORD` | a PLAIN word, `[A-Za-z0-9_./][A-Za-z0-9_./-]*`, or one single-quoted word: a quote, one or more characters other than a quote or a newline, then a quote |
| `LEAD` | the word `cd`, one `WORD`, then the `&&` operator and one space |
| `CONSUMER`, a sink | `cat`, the `>` operator, one `WORD` · `cat`, the `>>` operator, one `WORD` · `tee`, one `WORD` · `tee`, the word `-a`, one `WORD` |
| `CONSUMER`, a program | `python3`, the word `-`, then zero or more `WORD`s |

**C. The body ends at the first exact line.** Split the text after the first
line on newlines. The first line exactly equal to `D` is the terminator, and
everything before it is the body. If no line equals `D`, there is no match.
The text is never passed through `drop_comments`, and no tab, space or
carriage return is stripped before the comparison.

**D. Exactly one heredoc.** Outside the body, which means the first line, the
terminator and everything after it, the two-character sequence `<<` occurs
exactly once.

**E. What may follow the terminator.**

- After a **sink**: nothing but newlines. A sink writes a file, and nothing
  else on the command may run anything after that.
- After the **program**: anything. It is the *suffix*, and the base reads it.

**F. The reduced text** is the first line with its trailing space, `<<` and
quoted delimiter removed, then, where a suffix exists, a newline and the
suffix. The body and the terminator are gone, so no reader below this one
meets a heredoc on this command at all.

## Why this shape, clause by clause, against the shell

The places a reader and a shell can disagree about a heredoc are enumerated by
construction (`post-review-check.md` §*The questions the caller asked*, item 2,
extended with three of its own). Each one either cannot arise in the shape or
fails closed.

| # | Where they can disagree | What the shape does | Fails |
|---|---|---|---|
| 1 | Whether a `<<` opens a body at all, given quotes, comments, `$((…))`, a here-string, or an earlier line still open | The opener is on line 1 at byte 0, and line 1's alphabet holds no quote except inside a single-quoted word, no `$`, no backtick, no `#`, no backslash, no parenthesis and no brace. Clause D rejects a second `<<`, a here-string, and an arithmetic shift | closed |
| 2 | Where the delimiter word ends, through word concatenation or a backslash-newline inside the word | A single-quoted `D` followed directly by the newline. Clause A rejects any backslash-newline | closed |
| 3 | Whether it is quoted | The whole word is single-quoted. The double-quoted, partly quoted, ANSI-C and backslash forms do not match | closed |
| 4 | Where the body starts, after a quote, `$(` or continuation spanning line 1's newline, or a trailing operator | Nothing on line 1 can span a newline, and nothing follows the delimiter on line 1 | closed |
| 5 | Which line ends the body: a trailing CR, a `#` tail cut by `drop_comments`, tab stripping, trailing blanks | A byte-exact comparison on the raw text. CR and backslash-newline are banned outright, and `D`'s alphabet holds no blank | closed |
| 6 | What consumes the body | One simple command from a closed grammar. It has no redirection but the sink's own, no pipe and no wrapper | closed |
| 7 | What else on the command can reach the body | The LEAD is only a `cd`. A sink allows nothing after it. The program's suffix is read the base's way | closed for sinks. For the program, the class the base already leaves unread (Grounding row 3) |
| 8 | Reader text against shell bytes: encoding, NUL truncation | `D` is ASCII, so a line equals it as text exactly when it equals it as bytes. NUL is banned | closed |
| 9 | Text the harness adds around the command | Text appended to the last line can only stop the terminator from matching. The shell then reads the rest as body, and nothing extra runs | closed |

Clause 1's "an earlier line still open" is why the opener must be line 1. Any
earlier line would need a quote-aware reader to show it closed, and that is
the shared splitter this design refuses to trust.

### Every finding of #760's passes, against this shape

| Finding (by mechanism) | Why it cannot reach a data verdict here |
|---|---|
| A second, unquoted body whose `$(` is split by a backslash-newline (round 2, red 1) | A second `<<` fails D, and a backslash-newline fails A |
| A backslash-newline inside the delimiter word (round 3, red 1; #763 red 1) | Fails A and B |
| A line equal to the delimiter plus a carriage return, then a second opener (post-review red 1) | Fails A. A second opener also fails D |
| A `#` tail cut by `drop_comments` under a delimiter ending in a blank (post-review red 2) | `D` holds no blank, the cut is never made, and a second opener fails D |
| A file written over a program the line later runs from `PATH`; `gh` running `git` and `ssh` from `PATH`; `ssh -G` running a `Match exec` (round 3 yellow 2, post-review yellow 3) | Nothing may follow a sink, and the LEAD is only a `cd` |
| Flags after the `<<`, a bundled `-c`, `$(…)` or `${…;…}` before the program, a `#` glued to the delimiter (1790635415's rounds 2 and 3, the corpus) | Nothing on line 1 follows the delimiter, the program grammar admits no flag, and the alphabet holds no `$` or `#` |

## #739's three refusals

Each was read from the 0.18.0 session's transcript on 2026-10-04 (the first
line, the suffix, and whether CR or backslash-newline occurred). They are
described here by form, and the tests rebuild them as fixtures.

| # | Recorded form | Covered as recorded | What covers it |
|---|---|---|---|
| 1 | A LEAD `cd` to a plain path, a Python program on stdin appending to a memory file, and a `grep` count after the terminator | **yes** | The shape. The suffix is read the base's way and holds no commit |
| 2 | An assignment of a scratch path, a sink writing to that parameter, then `cd` and `gh pr edit` and `gh pr ready` after the terminator | **no.** The LEAD is an assignment, the target is a parameter, and programs follow a sink | Two calls: the sink to a written-out path alone, then the `gh` line, which holds no heredoc and was silent at the base already |
| 3 | An assignment from a `$(ls …)` substitution, the Python program given that parameter, then `git -C <abs> add` and `git -C <abs> commit` after the terminator | **no.** The LEAD runs a substitution and the argument is a parameter | One call: a LEAD `cd`, the path found inside the Python program, and the same `git -C` lines after the terminator. The commit is then judged where it lands, as before |

The cost of 2 and 3 is accepted in Q2. Covering either recorded form needs a
reader of assignments, substitutions or parameters that is exact, and that is
the problem this work exists to stop having.

## Carry or fresh

**Fresh, for the code.** #760's phase-1 reader record (`Heredoc`: `quoted`,
`terminated`, `delimiter`, `dashed`) is produced inside `_heredoc_split`'s
pass, the unit whose boundaries failed four times. `heredoc_data` (265 lines
in `hooks/tokens.py`) rests on a positive line shape read through `shlex` and
`is_plain`'s sets, which is the construction the passes broke. The new reader
is a grammar over line 1, a line split and a count. Carrying either piece
would bring back the trust this design removes, and a larger unit to review.

**Carried, as test fixtures only.** The shape lists in #760's
`tests/test_a_heredoc_body_nothing_runs_is_data.py` that pin a stop
(`CONSUMERS_READ`, `FILE_RUNNERS`, `NESTED`) are rebuilt as must-stop rows of
the new module. So are #739's own body fixtures (`PR_BODY`, `PY_BODY`). They
pin readings this rule must not loosen, whichever reader is underneath.

## User scenarios & acceptance *(mandatory)*

"Silent" is the gate's `main()` in an opted-in, undeclared session directory
with no git hooks installed. "Stops" means not silent, with and without the
`automation` press where the module already checks both.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1: refusal 1 | Given refusal 1's recorded form, with a body that mentions a commit in backticks and on a line of its own. When the gate reads it, then it is silent | new gate case, red at `e141980a` |
| S2: refusals 2 and 3, restated | Given the restated forms from the table above. Then the sink call is silent. The program call's commit is judged at its `-C` target: silent where that target is declared, and stopped for that repository, not as unreadable, where it is not | new gate cases; red at `e141980a` for the silent ones |
| S3: refusals 2 and 3, as recorded | Given each recorded form with a commit-bearing body. Then each stops as at the base. This pins the cost Q2 accepts | new gate case, green before and after |
| S4: the shape's edges | For each clause A–E there is a string that fails exactly that clause and holds a commit-bearing body, and each stops. Each slot of B (each sink form, the program with and without arguments, a PLAIN and a single-quoted `WORD`, with and without LEAD) has a matching string, and each is silent | reader unit cases plus gate cases |
| S5: #760's findings | Every row of the findings table above, rebuilt as a fixture, stops | gate cases; each green at `e141980a` and after |
| S6: the shell agrees | For every string a generated corpus makes the reader admit, run with a sink and harmless lines under each available shell (bash and zsh, directly and through `eval`): the written file is the reader's body, and no marker a body line would create exists. The corpus is built over clause C's axes: terminator variants with a trailing blank, a tab, a CR or a `#` tail, a body line containing `D`, an empty body, and a terminator at end of input with no newline | new test; skipped per shell where that shell is absent, and the skip names the shell |
| S7: the suffix is the base's | Given the program shape with each suffix of `tests/test_no_shape_the_base_stops_reads_silent.py`'s "a heredoc edit, then a commit on the next line" row. Then the decision equals the base's decision on the same line with the body taken out | that module, narrow, plus one equality case |
| S8: the corpus holds | Every row of `tests/test_no_shape_the_base_stops_reads_silent.py` stays non-silent with and without the press, except the row Q1 moves, which is pinned silent in a case of its own. `test_the_four_measured_shapes_are_refused_under_the_press` keeps its other three rows. `tests/test_the_commit_gate_decides_at_the_commit.py`'s S2 corpus follows by import | those three modules, narrow |
| S9: nothing else moves | `tests/test_what_the_reader_understands.py`, `tests/test_the_frozen_reading_never_grows.py`, `tests/test_gate_judges_the_repo_it_commits_to.py` (unterminated body, a commit after a body, an interpreter-fed body, nested bodies, here-string), `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py` and `tests/test_worktree_guard.py` pass unchanged | narrow runs |
| S10: the words a person reads | The two policy paragraphs and contract §9 state the shape in prose a reader can apply without opening code, and say what stays read. Each carries an `Enforced by:` line naming S1, S4 and S6's cases | `tests/test_edits_go_through_the_edit_tool.py` and the docs hygiene modules, narrow |

## Data & interfaces

- **New module** `hooks/one_heredoc.py`. Its one public function returns the reduced text, or `None` for no match. It imports nothing from `cmdline`, `cmdline_base` or `tokens`, and nothing beyond the standard library's `re`.
- **`hooks/commit-review-gate.py`**: `main` computes the reduced text once and hands it to `commit_invocations` and to the `unparsed` substring test in place of the command. `is_git_commit` does the same if it still has a caller; the work checks. `is_plain`, the consent reads and everything that writes a record keep the command as written. `commit_invocations` itself and `_reads_a_commit`'s recursion are unchanged.
- **I/O**: any file a new test writes or reads names `encoding="utf-8"`, because #741's encoding check lands first.
- **Ledger**: rows a re-read moves for `commit-review-gate.py#main` or `#commit_invocations` sit in released files (`Ledger frozen from | 1790993141`). Their re-reads go into `seal/ledger/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data.md` through `evidence-check --reverify --into`.

## Open questions → questions.md

The judgments the tickets left open that the tree answered are listed at the
head of `questions.md`. Q1 (the moved row) carries the owner's answer from
#760. Q2 (the recorded forms of refusals 2 and 3 stay refused) is decided at
the frame's default, and the owner can overturn it at approval.

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

Framed 2026-10-04 by framer, before the build.
