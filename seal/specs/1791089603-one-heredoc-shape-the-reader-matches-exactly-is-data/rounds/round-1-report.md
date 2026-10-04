# Round 1 report — 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data

Target `68eaf258` on `fix/739-one-heredoc-shape-the-reader-matches-exactly-is-data`,
against `release/v0.18.1` at `edee5ca2`. First round: no earlier
`round-N.md` exists, so nothing is carried and every verdict below is this
round's own.

This report names shapes by unit, coordinate, clause letter and shell rule.
It holds no command string, old or new, that passes either gate silently.

## Summary

The shape holds against the shell. Every slot of clause B, the terminator
rule of clause C and the program suffix of clauses E and F were attacked by
construction, and bash 3.2 and zsh 5.9 agreed with the reader on every
admitted string, run directly and through `eval`. #760's five recorded
classes are each closed by a named clause. One new comment in `main` makes a
safety claim about the consent read that a measurement contradicts. That is
the one 🟡. The behaviour under it is the base's, unchanged, and is handed
on as a deferral candidate. Three ⬜ follow.

## Stage 1 — spec compliance

**Clauses A–F as built (read).** `hooks/one_heredoc.py#_match` implements
each clause as `spec.md` §*The shape* states it:

- A is the `_BANNED` scan over the whole text, body included.
- B is a full match of `_OPENER` over the text before the first newline. The slots
  `_D`, `_PLAIN`, `_QUOTED`, `_LEAD`, `_SINK` and `_PROGRAM` match the slot
  table character for character.
- C is a list `index` over `rest.split("\n")`. It uses a plain newline split,
  not `splitlines`, so U+2028, NEL and form feed never end a line.
- D counts `<<` over the first line, the terminator and the suffix.
- E is the `strip("\n")` test, with the sink refused when anything else is
  left.
- F is the returned `head`, or `head` plus a newline plus the suffix.

**No splitter unit (read and executed).** The module imports `re` and
nothing else. `tests/test_one_heredoc_shape_is_read_exactly.py#test_the_reader_imports_nothing_but_re`
pins this, and it passed in this round's run.

**What `main` hands below (read).** `hooks/commit-review-gate.py:1271-1288`
computes the reduced text once and passes it to `commit_invocations` and to
the `unparsed` substring test. The raw command still reaches three places:
`is_plain` (the `around` flag), `has_marker` in the unreadable branch,
and `judge`, whose only use of the command is `has_marker` at line 1103. So
`is_plain` and the consent read do see the raw text, as the asked paragraph
requires. `is_git_commit` has no caller in `hooks/`, `tests/`, `bin/` or
`skills/` (grep, read), which answers Q5 as the spec predicted.

**Spec drift, minor (read).** `spec.md` §*Scope*, the `hooks/tokens.py` bullet,
places `has_marker` in `hooks/tokens.py`. It is defined in
`hooks/commit-review-gate.py`. The behaviour is unaffected.

## Stage 1 — the shape attacked by construction

For each slot, these are the inputs the clause admits and what each shell
does with them.

- **The `cd WORD` slot.** A PLAIN word draws on letters, digits, `_`, `.`,
  `/` and `-`, and cannot start with `-`. No character in that set triggers
  globbing, tilde, brace, parameter, `=`-expansion (zsh), history or
  arithmetic expansion in bash or zsh. A single-quoted WORD holds no quote
  and no newline, and both shells take everything inside single quotes
  literally: backslash, `$`, backtick and `!` alike. A quoted WORD that holds
  `<<` fails D. Two adjacent quoted words, or a PLAIN word glued to a quoted
  one, do not match `_WORD` followed by a space, so zsh's RC_QUOTES doubling
  cannot arise. When the `cd` fails, `&&` skips the consumer, but the shell
  still consumes the body while parsing and still runs the program's suffix.
  The reduced text keeps the same LEAD, so the base reads the same thing.
- **The consumer slot.** After a sink, E leaves nothing for the shell to run.
  A digit WORD after `python3 -` is separated from `<<` by the required
  space, so the shell takes it as an argument and never as a descriptor. Any
  WORD after `-` goes to `sys.argv` and never to Python's own options, and a
  leading `-` is impossible in PLAIN anyway.
- **The delimiter.** It is ASCII alphanumeric or underscore, wholly quoted,
  and followed directly by the newline. Partly quoted, ANSI-C, backslash and
  tab-stripping forms all fail B
  (`tests/test_one_heredoc_shape_is_read_exactly.py#FAILS`).
- **The terminator line.** C compares exact bytes, so both shells end the
  body on the same line. The agreement module's corpus (696 strings, 18 near
  lines) passed in bash and zsh, run directly and through `eval`.
- **What follows a python terminator.** The agreement module runs no program
  heads, so this round measured it with a probe, described under
  `## Executed probes`. The shells ran exactly the suffix the reduced text
  holds, and no body line. For refusal 1's own grep-after-the-terminator
  form, the reduced text is the head line and the same suffix, and the base
  reads that suffix as it did.

**#760's recorded classes (read and executed).**

- **Split substitution.** A backslash-newline fails A, and a second opener
  fails D.
- **Continuation in the delimiter.** Fails A and B.
- **CR before the terminator.** Fails A.
- **Comment tail on a terminator line.** `_D` holds no blank and no `#`, and
  the comparison is exact.
- **`gh` running `ssh` and `git`.** E allows nothing after a sink.

Each is a row of `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py#FINDINGS`,
and every row of `test_what_760_found_still_stops` passed in this round.

**The program class, measured against the base.** The approved frame puts a
Python program on stdin in the unread class (Grounding row 3, Q2 of #760).
This probe measured what that costs. A program-shape command whose Python
text runs a commit through the `os` module, and one that runs it through
`subprocess` with a list, were both silent at `edee5ca2` already. The
reduction therefore removes no stop the base had for a Python program that
really commits. What it removes are stops on Python text that looks like a
shell commit, which is #739's refusal 1.

## Stage 2 — findings

### 🟡 1 — `main`'s new comment says the consent read is safe on the raw text, and a waiver token inside a data body silences a commit in the suffix

`hooks/commit-review-gate.py:1268-1270` gives the reason the consent read
keeps the raw command: "reading more of it can only keep the reading in, and
a waiver is written where the person wrote it". That reason holds for
`is_plain`, where more text can only make a command less plain. For a consent
read it runs the other way. More text can only find more waiver tokens.

The probe (executed) built a program-shape command whose body is a Python
assignment of a string literal holding the review waiver token, followed by a
suffix that commits with `-C` into an opted-in, undeclared repository. The
gate was **silent**. The same command with no token in the body was **deny**.
`has_marker` reads the raw command through `split_segments`, which tokenises
the body lines, so a token inside Python text counts as the person's waiver.

The decision is identical at `edee5ca2`, which was silent on the same
string, so the change creates no new silent commit. Two things make the
sentence worth fixing in this round anyway.

- The comment is new code in this diff. It states as fact a safety property
  that a measurement contradicts, in the function a reader opens first.
- `spec.md` §*#739's three refusals* recommends refusal 3's restated form: a
  Python program, then the commit after the terminator. This repository's
  own Python patches often carry the waiver example as text, because its
  docs teach it. On an undeclared target, that recommended form now meets
  this read.

The behaviour is out of this ticket by `spec.md` §*Scope* ("The consent reads
are unchanged at the base and are not this ticket"), so the fix asked here is
the sentence. The behaviour goes to `## Deferred`.

### ⬜ 2 — the agreement module says a program body cannot carry the oracle's lines, and so the program's suffix has no shell measurement

`tests/test_one_heredoc_shape_agrees_with_the_shell.py:24-26` gives two
reasons for running only sinks. The first holds: the cut is fixed at parse
time, before any consumer runs. The second does not: "a Python program's
body cannot hold the harmless shell lines the oracle needs." It can. Python
rejects the program as a syntax error, but the shell still decides where the
body ends, and a marker line that the shell ran would still appear. The
probe did exactly this.

What goes unmeasured as a result is clause E's program arm and clause F:
does the shell run the lines after a program's terminator, and only those?
The probe says yes, with no disagreement. Nothing in the tree pins it. The
regression test to plant is listed below.

### ⬜ 3 — a test named for four measured shapes now checks three

`tests/test_an_automation_run_meets_no_commit_prompt.py:188`
(`test_the_four_measured_shapes_are_refused_under_the_press`) and the section
header at line 170 still say four. `measured` now returns three rows. The
docstring explains the move, but the name is what a failure prints.

### ⬜ 4 — the contract's summary of the shape leaves out the program's words

`skills/agent-contract/SKILL.md:241-245` describes the consumer as
"`python3 -`" and then the delimiter. The grammar admits any number of WORDs
after `python3 -`, which `docs/commit-review-gate-spec.md` states. The
summary also says "one word" without the WORD alphabet. Both gaps make an
agent write a non-matching string, which then gets read as shell. That fails
closed, but each such string costs one stop in an unattended run, and #739
exists to remove exactly that cost. The section does point to the policy
"for the whole grammar".

## Regression tests to plant

- `tests/test_one_heredoc_shape_agrees_with_the_shell.py`: add program heads
  with no argument, with a quoted argument, and with a LEAD. Each body is a
  near-terminator line followed by a marker line. The suffix is one marker
  line. Run bash and zsh, directly and through `eval`. Assert that only the
  suffix marker exists, in the directory the LEAD names. Show it red by
  making the probe's reader strip trailing blanks from lines before the
  comparison. (Written by mechanism here, on purpose: the strings are shapes
  the gate passes.)
- `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`: pin 🟡 1's
  measured behaviour as a known, named cost, so that whichever answer the
  deferral gets is a visible change. The case is a program shape whose body
  holds the waiver token inside a Python string literal, with a suffix commit
  into an undeclared repository. Today that case is silent.

## Facts for the evidence ledger

- `hooks/commit-review-gate.py#main` reads the reduced text for
  `commit_invocations` and the `unparsed` test, and the raw command for
  `is_plain`, `has_marker` and `judge` (read at `68eaf258`, lines 1271-1288).
- `hooks/commit-review-gate.py#is_git_commit` has no caller in the tree (read,
  grep at `68eaf258`).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `main`'s comment claims the consent read on the raw text is safe ("can only keep the reading in"), but a waiver token inside a data body silences a suffix commit | `hooks/commit-review-gate.py:1268-1270` | open | Executed: the program shape with the token in a Python string literal and a suffix commit to an undeclared repository was silent, and deny without the token. Identical at `edee5ca2`. The behaviour is deferred; the sentence is this diff's |
| ⬜ 2 | Agreement module claims a program body cannot carry the oracle's lines, so clauses E and F (program arm) have no shell measurement | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:24-26` | open | Executed probe: program heads with markers ran in bash and zsh, both modes, with no disagreement, which shows the oracle is possible |
| ⬜ 3 | Test name and section header say four measured shapes; three remain | `tests/test_an_automation_run_meets_no_commit_prompt.py:170` | open | Read: `measured` returns three rows |
| ⬜ 4 | Contract §9's summary omits the WORDs after `python3 -` and the WORD alphabet | `skills/agent-contract/SKILL.md:241-245` | open | Read against `docs/commit-review-gate-spec.md`'s paragraph and `_PROGRAM`. Fails closed, at the cost of a stop |
| 🟢 | Clauses A–F built as `spec.md` §*The shape* states, with no import beyond `re` | `hooks/one_heredoc.py:45-106` | confirmed | Read, and the unit module passed |
| 🟢 | `main` hands the reduced text to `commit_invocations` and the `unparsed` test; `is_plain` and the consent read see the raw text | `hooks/commit-review-gate.py:1271-1288` | confirmed | Read |
| 🟢 | Every admitted sink string is cut where bash 3.2 and zsh 5.9 cut it, directly and through `eval` | `tests/test_one_heredoc_shape_agrees_with_the_shell.py` | confirmed | Executed: 400 passed across the three new modules |
| 🟢 | The program's suffix runs exactly as the reduced text says, and no body line runs | `hooks/one_heredoc.py:91-95` | confirmed | Executed probe: 4 heads, 11 near lines, 2 shells, 2 modes, no disagreement |
| 🟢 | #760's five recorded classes are each closed by a named clause | `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` | confirmed | Read per clause, and `test_what_760_found_still_stops` passed |
| 🟢 | The program class removes no stop the base had for a Python program that commits | `hooks/one_heredoc.py:91-95` | confirmed | Executed: the `os` and `subprocess` forms were silent at `edee5ca2` and at the target; a shell-fed body stayed deny at both |
| ❓ | Bash 5.x agreement (Q3) | `tests/test_one_heredoc_shape_agrees_with_the_shell.py` | ❓ out of verified scope | Only bash 3.2 exists on this machine. Answered by the CI ubuntu leg at the pull request |
| ❓ | The moved row reaches the shape on Windows (Q4) | `tests/test_no_shape_the_base_stops_reads_silent.py` | ❓ out of verified scope | No Windows host here. Answered by the CI Windows leg at the pull request |

## Executed probes

| What was run | Result |
|---|---|
| The three new modules, narrow, in a scratch clone at `68eaf258` with a `uv` venv | 400 passed in 21s (bash 3.2.57, zsh 5.9 present) |
| Probe A: program heads (no argument, quoted plus PLAIN arguments, quoted LEAD, PLAIN LEAD), each with 11 near-terminator body lines followed by a marker line, and a suffix marker. Run in bash and zsh, directly and through `eval`; harmless colon-redirect markers only | No disagreement: only the suffix marker existed, in the LEAD's directory. Reduced text equals head plus suffix in every case |
| Probe B: 13 constructed strings handed as JSON to the gate hook at the target and at `edee5ca2` (extracted with `git archive`). Session declared; commit targets opted in and undeclared. No string was run by a shell | Program with the token as a body shell word, suffix commit: silent / silent. Token in a Python string literal: silent / silent. No token: deny / deny. Sink whose body commits: silent / deny (the intended change). Near-terminator then commit, sink: silent / deny (the intended change). Quoted WORD holding `<<`: deny / deny. Sink followed by spaces: deny / deny. Python `os` and `subprocess` commits: silent / silent. Shell-fed body: deny / deny |
| Broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A waiver token in a heredoc body the gate now treats as data still waives the commit arm for a commit elsewhere on the command (🟡 1's behaviour, the same at `edee5ca2`) | Candidate for a new issue: the consent reads, which `spec.md` §*Scope* puts outside this ticket | the repository owner |

## Paste-ready fixes

### 🟡 1

```python
    # Where the command is the one heredoc shape `hooks/one_heredoc.py`
    # matches byte for byte, every reading for a COMMIT reads it with the body
    # taken out (#739, #763): a file's text, or a Python program on stdin,
    # which `docs/commit-review-gate-spec.md` already leaves unread as a
    # program whose operands are a script. Everywhere else it is the command
    # as written, exactly as before. Nothing below is asked where a body is,
    # because the reduced text holds none. `is_plain` keeps the command as
    # written, because reading more of it can only keep the reading in. The
    # consent reads (`has_marker`, here and in `judge`) also keep it, as at
    # the base, and that runs the other way: a waiver token inside the body
    # still counts, although the body is data to the commit reading. That is
    # the base's behaviour, left to the consent reads' own work item.
```

Needs a fix: yes — 🟡 1, the sentence in the comment in `main` that calls the consent read on the raw text safe

Loses a record or crashes: no

The gate comes due when the rounds settle: that is the sealer's spawn, after
🟡 1 is answered.

## Proof

Files opened this round: `hooks/one_heredoc.py`,
`hooks/commit-review-gate.py` (lines 1064-1120 and 1230-1420, plus the
`has_marker` definition), `hooks/tokens.py` (`given`, `is_plain`),
`hooks/cmdline_base.py` (`split_segments` docstring),
`tests/test_one_heredoc_shape_agrees_with_the_shell.py`,
`tests/test_one_heredoc_shape_is_read_exactly.py`,
`tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`,
`tests/test_gate_judges_the_repo_it_commits_to.py` (the interpreter-fed
case), `tests/conftest.py` (the hook helpers), the diffs of
`docs/commit-review-gate-spec.md`, `skills/agent-contract/SKILL.md`,
`tests/test_no_shape_the_base_stops_reads_silent.py`,
`tests/test_an_automation_run_meets_no_commit_prompt.py` and
`tests/test_edits_go_through_the_edit_tool.py`, and this work item's
`spec.md`, `questions.md` and the phase records (grep only).
The scratch clone, its venv, the probe file and the base extraction were
deleted before handover.
