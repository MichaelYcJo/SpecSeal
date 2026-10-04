# Round 2 report — 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data

Target `d6096dec` on `fix/739-one-heredoc-shape-the-reader-matches-exactly-is-data`,
against `release/v0.18.1` at `edee5ca2`. This is the verifying round for
round 1's fixes, `dd555038..bcf841ee`. Round 1's report and record were read
for coordinates. Every verdict below is this round's own.

This report names shapes by unit, coordinate, clause letter and shell rule.
It holds no command string that passes either gate silently.

## Summary

All four of round 1's findings are closed. The new program arm of the
agreement test is sound. A shell that runs a body line cannot pass it, which
this round showed by making a shell do exactly that. The arm also goes red
under two reader mutations. Four ⬜ follow, and none of them needs a fix
before merge:

- The contract's new summary of the grammar still allows a spelling the
  reader refuses: a space between `<<` and the quoted delimiter. The policy
  has the same wording.
- The new `program_corpus` docstring says it builds a body of all the near
  lines. Clause A refuses that body, so it is never measured.
- Two paperwork corrections under the work item: the changelog fragment and
  `spec.md`.

## Round 1's findings

### 🟡 1 — closed

`hooks/commit-review-gate.py:1268-1273` now gives each reader its own
direction:

- `is_plain` keeps the command as written. Reading more text can only make
  a command less plain.
- The consent reads keep it too. That runs the other way: a waiver token
  inside the body still counts.

The comment says this is the base's behaviour and names #773 as its home.

The coordinates named in the comment were read:

- `has_marker` is called in `main` at line 1397.
- `has_marker` is called in `judge` at line 1103.
- `is_plain` is called at line 1353.

#773 is open. It describes the mechanism and carries a checkbox for the
sentence that this fix corrects.

Round 1 suggested a regression test that pins the waiver behaviour in
`tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`. It was not
planted. #773 now owns that case, and its checklist asks for it to be seen
red first. Carried, with no verdict row of its own.

### ⬜ 2 — closed

`tests/test_one_heredoc_shape_agrees_with_the_shell.py:201-271` adds the
program arm. The prompt asked whether its oracle could pass while the shell
ran a body line. It cannot, on this corpus.

**How the corpus is built (read).** Every body in the corpus is two lines:

- a near line, which is the first body line;
- a marker line, named `m<i>`. Suffix markers are named `s` and `t`.

**Why a run body line is always caught (read).** A near line can run only
if the shell ended the body before it. That would put the body's end at the
opener, which is impossible. If the shell ends the body early at the near
line, it runs the marker line that follows. That marker is not among the
reduced text's suffix markers, so the run disagrees. If the shell ends the
body late, the suffix becomes body text, and the missing `s` disagrees. A
shell that aborts on a later syntax error leaves no `s` either, so that case
fails loudly too.

Python's part cannot create a marker:

- every body holds `: > m<i>`, which Python refuses to compile;
- nothing in Python reads a marker line as shell.

**Executed.** A probe gave the shell a command whose trailing-blank near
line had been made an exact terminator, while the oracle kept the reader's
expectation for the real command. Every one of the 12 eligible rows was
caught.

**Seen red (§15, executed).** The arm went red under two reader mutations:

- a reader that strips trailing blanks before comparing: 12 of 192 rows
  disagree in zsh through `eval`;
- a reader that keeps only the first suffix line: 96 of 192 rows disagree in
  bash through `eval`.

One new ⬜ sits in the same unit (⬜ 2 below).

### ⬜ 3 — closed

The test is now `test_three_measured_shapes_are_refused_under_the_press`.
The S4 header says three of four. The docstring names the case that holds
the fourth. The ledger fragment's E3 row cites the new name, and
`evidence-check` resolves all 38 of this work item's ledger anchors with 0
drifted (executed). `spec.md` still names the old test name: ⬜ 4 below.

### ⬜ 4 — closed

`skills/agent-contract/SKILL.md:241-253` now names the WORDs after
`python3 -` and the WORD alphabet. The pin in
`tests/test_edits_go_through_the_edit_tool.py#test_the_rule_names_the_one_heredoc_shape_it_does_not_read`
goes red on the section as it stood at `dd555038`, failing on the first slot
phrase (executed).

## Stage 2 — new findings

### ⬜ 1 — the grammar's summaries allow a space between `<<` and the delimiter, which the reader refuses

The contract at `skills/agent-contract/SKILL.md:241-245` says three things:

- "one space between every two tokens";
- then "`<<` and a delimiter of letters, digits and underscores in single
  quotes";
- a word may be "one single-quoted word holding no quote and no newline".

`docs/commit-review-gate-spec.md:182-187` says the same with "one space
between tokens".

Read literally, `<<` and the quoted delimiter are two tokens, so the text
tells a session to put one space between them. Clause B's opener puts no
space there. The reader returns None for that spelling (executed), and the
gate then reads the body as shell. The contract also admits an empty quoted
word, which `_QUOTED` refuses with its `+`. That also returned None
(executed).

Both refusals fail closed. Each still costs an unattended run one stop, and
removing that cost is the reason #739 exists. This is the class of round 1's
⬜ 4. Its three carriers were enumerated: the contract, the policy, and the
changelog fragment. The fragment does not mention `<<` at all; see ⬜ 3.

### ⬜ 2 — `program_corpus` says it measures a body of all the near lines, and clause A refuses that body

The docstring at `tests/test_one_heredoc_shape_agrees_with_the_shell.py:213-215`
says the corpus holds "one body of all of them". That body contains two near
lines that clause A bans: the one ending in a carriage return and the one
ending in a backslash before its newline. So the reader admits none of the 12
combined rows (executed: 0 of 192 rows). `bodies` builds the sink arm's
combined body the same way, and it is likewise never admitted. The sink arm's
docstring does not claim it.

The combined body is the only place where near lines follow one another. A
reader that matched a terminator relative to the line before it would show up
only there. If the near lines that clause A bans are left out, the combined
body is admitted: 12 more rows, green in bash and zsh, both modes (executed).

### ⬜ 3 — correction: the changelog fragment's grammar sentence is looser than the reader

`seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/changelog.md:9-13`
says:

- "an optional `cd` and `&&`", which leaves out the cd's word;
- a plain word is letters, digits, `_`, `.`, `/` and `-`, without "not
  starting with `-`";
- it never mentions `<<` or the absence of a space before the quoted
  delimiter.

Line 13 is also left unwrapped. This is a correction to the run's paperwork,
and it is outside `Needs a fix`.

### ⬜ 4 — correction: `spec.md`'s S8 row names the test by its old name

`seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/spec.md:182`
still names `test_the_four_measured_shapes_are_refused_under_the_press`. NAME NOT IN TREE
The fix for round 1's ⬜ 3 renamed it to
`test_three_measured_shapes_are_refused_under_the_press`.

`evidence-check` did not refuse the line (executed: 0 refused across the
records it read). A reader who follows the S8 row still finds no case by that
name. This is a correction to the run's paperwork, and it is outside
`Needs a fix`.

## Regression tests to plant

- `tests/test_edits_go_through_the_edit_tool.py#test_the_rule_names_the_one_heredoc_shape_it_does_not_read`:
  the two slot phrases in ⬜ 1's fix. This round showed them red on the
  current section and green on the proposed one.
- `tests/test_one_heredoc_shape_agrees_with_the_shell.py`: the admitted
  combined body from ⬜ 2's fix. It adds 12 rows to `program_corpus`. The
  `len(rows) > 150` floor still holds.

## Facts for the evidence ledger

- `tests/test_one_heredoc_shape_agrees_with_the_shell.py#program_corpus`
  yields 192 admitted rows at `d6096dec`: 2 delimiters, 16 near lines that
  clause A admits, 3 heads and 2 suffixes. None of the rows holds the
  combined body (executed).
- `hooks/commit-review-gate.py#main` names `has_marker` "here and in
  `judge`", and those are its two callers in the hook: lines 1397 and 1103
  (read at `d6096dec`).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Contract section 9 and the policy say one space between every two tokens and then `<<` and a quoted delimiter, so a session can write a space the reader refuses; the contract also admits an empty quoted word | `skills/agent-contract/SKILL.md:241-245` | open | Executed: the reader returns None for the spaced operator and for an empty quoted word, and reduces the in-shape control. Fails closed, one stop each. The same wording is at `docs/commit-review-gate-spec.md:182-187` |
| ⬜ 2 | `program_corpus` docstring says it measures one body of all the near lines; clause A bans two of them, so that body is never admitted | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:213-215` | open | Executed: 0 of 192 rows hold it; with the banned near lines left out it is admitted (12 rows) and green in both shells, both modes |
| ⬜ 3 | Correction: the changelog fragment's grammar sentence drops the cd's word, the no-leading-dash rule and the heredoc operator, and leaves one line unwrapped | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/changelog.md:9-13` | open | Read against `hooks/one_heredoc.py:49-59`. Paperwork, outside Needs a fix |
| ⬜ 4 | Correction: the S8 row still names the measured-shapes case by its pre-rename name | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/spec.md:182` | open | Read; the case is now `test_three_measured_shapes_are_refused_under_the_press`. Paperwork, outside Needs a fix |
| 🟢 | round 1's fix-or-justify finding 1 is closed — the comment in `main` states the direction for `is_plain` and for the consent reads, and names #773 | `hooks/commit-review-gate.py:1268-1273` | confirmed | Read: the callers it names are at lines 1103, 1353 and 1397; #773 is open and holds the behaviour |
| 🟢 | round 1's finding 2 is closed — the agreement module runs the program arm, and its oracle cannot pass while the shell runs a body line | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:201-271` | confirmed | Executed: a shell made to run a body line was caught on 12 of 12 eligible rows; reader mutations went red (12 and 96 of 192); the module passed |
| 🟢 | round 1's finding 3 is closed — the case, its header and the ledger anchor say three measured shapes | `tests/test_an_automation_run_meets_no_commit_prompt.py:170-197` | confirmed | Executed: the module passed; this work item's ledger fragment 38 ok, 0 drifted |
| 🟢 | round 1's finding 4 is closed — contract section 9 names every slot, and its pin covers each one | `skills/agent-contract/SKILL.md:241-253` | confirmed | Executed: the extended pin is red on the section at `dd555038` and green at the target |
| ❓ | The program arm's agreement on bash 5.x | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:251-271` | ❓ out of verified scope | Only the macOS bash 3.2 ran here. Answered by the CI ubuntu leg at the pull request |

## Executed probes

| What was run | Result |
|---|---|
| Six narrow modules at `d6096dec` in a scratch clone through the repository's own runner: the three one-heredoc-shape modules, the edit-tool module, the automation module and the no-shape-reads-silent module | 484 passed in 57s, none skipped, so the program arm ran in both shells |
| Probe P1: the program corpus counted | 192 rows; 16 admitted near lines per delimiter; combined body admitted in 0 rows |
| Probe P2: bash run directly, with the trailing-blank near line turned into an exact terminator in what the shell received, and the reader's expectation for the real command | 12 of 12 eligible rows caught; the shell made the body's marker beside the suffix's |
| Probe P3: reader mutated to strip trailing blanks before the comparison, zsh through `eval` | 12 of 192 disagree, red |
| Probe P4: reader mutated to keep one suffix line, bash through `eval` | 96 of 192 disagree, red |
| Probe P5: the reader on a spaced heredoc operator, on an empty quoted word, and on the in-shape control, all with a harmless body | None, None, reduced |
| Contract pin at `dd555038`'s section 9 | Red on the first slot phrase |
| The ⬜ 1 fix: pin extended with two phrases, then the proposed paragraph | Red on the current section; green with the proposed paragraph (module 11 passed) |
| The ⬜ 2 fix applied to `program_corpus` | 204 rows, 12 of them combined; the program arm green in bash and zsh, both modes |
| `evidence-check` over the clone's tree, lenient | This work item's fragment: 38 ok, 0 drifted. 10 drifted rows sit in three other work items' fragments (1791076830, 1791076832, 1791076833), on files this branch does not touch, so they are the base's state. Under `--strict` they make the tree NOT SEALED |
| Broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Paste-ready fixes

### ⬜ 1

`skills/agent-contract/SKILL.md`, the lines from "word, `tee` or `tee -a`" to
"no quote and no newline.":

```markdown
word, `tee` or `tee -a` and one word, or `python3 -` followed by any number of
words; then `<<` and, with no space between them, a delimiter of letters,
digits and underscores in single quotes. A word is either letters, digits,
`_`, `.`, `/` and `-` that do not start with `-`, or one single-quoted word
holding no quote and no newline and not empty.
```

`docs/commit-review-gate-spec.md:183-187`, the same two slots:

```markdown
one word and `&&`; then the consumer; then `<<` and, with no space between
them, a delimiter of letters, digits and underscores in single quotes. The
consumer is `cat` with `>` or `>>` and one word, `tee` or `tee -a` and one
word, or `python3 -` and any number of words, where a word is a path of
letters, digits, `_`, `.`, `/` and `-` not starting with `-`, or one
single-quoted word that is not empty and holds no quote or newline. The body
```

`tests/test_edits_go_through_the_edit_tool.py`, two more slot phrases after
the delimiter's:

```python
            "letters, digits and underscores in single quotes",
            "`<<` and, with no space between them, a delimiter",
            "holding no quote and no newline and not empty",
```

### ⬜ 2

`tests/test_one_heredoc_shape_agrees_with_the_shell.py`, inside
`program_corpus`:

```python
        bodies_ = [[line, f": > m{i}"] for i, line in enumerate(near)]
        # Clause A refuses a body holding a carriage return or a backslash
        # before a newline, so the body of all of them keeps the rest.
        kept = [line for line in near if not any(b in line + "\n" for b in BANNED)]
        bodies_.append([x for i, line in enumerate(kept) for x in (line, f": > n{i}")])
```

Needs a fix: no

Loses a record or crashes: no

Nothing open needs a fix, so the broad gate comes due. That means the
sealer's spawn. Before it runs: `evidence-check --strict` will report the 10
drifted rows in the three other work items' fragments listed above. They
come from the base, not from this branch.

## Proof

Files opened this round: this round's asked paragraph; `rounds/round-1-report.md`,
`rounds/round-1.md`, `survivors.md`, `changelog.md` and `spec.md` (grep, line
182) of this work item; `hooks/one_heredoc.py`; `hooks/commit-review-gate.py`
(lines 340-356 and 1255-1300, plus grep of the `has_marker`, `is_plain` and
`judge` lines); `tests/test_one_heredoc_shape_agrees_with_the_shell.py`;
`tests/test_edits_go_through_the_edit_tool.py` (lines 43-49 and 255-300);
`tests/test_an_automation_run_meets_no_commit_prompt.py` (lines 168-200);
`skills/agent-contract/SKILL.md` (lines 236-262);
`docs/commit-review-gate-spec.md` (lines 176-200); the fix range's full diff;
`bin/test`; issue #773.
The scratch clone, its venv, the probe module and every output file were
deleted before handover. No file in the worktree was written but this report.
