# Round 1 — a here-document body is data to the commit gate (#739)

Target `f75ef84b`, base `release/v0.18.1` at `e141980a`, draft PR #760.
Reviewed in a `git clone --no-local` of the worktree at the target. Record
language: English (no `Record language` row in `seal/config.md`).

## What the account claimed, and what the code showed

The build frames this as a narrowing built the same way as `is_plain`: a
positive shape, reusing `is_plain`'s sets, with everything unlisted read as
before. `spec.md` §Grounding (the row citing `hooks/tokens.py#is_plain`) says
R2c "is built the same way and reuses the same sets", and R2f says a sink's
body is data only when "nothing on the line can run" the file it wrote.

I confirmed, by opening the code rather than trusting the account:

- The frozen reader is untouched: `git diff e141980a f75ef84b --
  hooks/cmdline_base.py` is empty. `cmdline.py`'s `drop_heredoc_bodies` and
  `heredoc_bodies` are now views over `_heredoc_split`'s records and return
  the same lists (pinned by `test_the_two_old_views_are_views_of_the_records`,
  and H1's 24,304-constant comparison).
- The three changed test modules pass at the target: 172 passed (105 + 51 +
  16), run narrow through `bin/test`. Executed.
- Q1's one corpus row (`test_no_shape_the_base_stops_reads_silent.py`) moved
  to `test_the_one_row_that_left_the_corpus_reads_silent`, which asserts the
  opposite; the automation module's `test_the_four_measured_shapes...` now
  asserts that same shape silent with the press and without. Both as the
  account states.
- Q2's strict `python3 -` form is enforced: `_plain_on_a_data_line` for a
  `STDIN_PROGRAM` returns False unless the first word past redirections is
  `-` or absent, and `CONSUMERS_READ` pins `python3 -c`, `python3 x.py`,
  `python3 $X`, `python3 <<'EOF' -c` as still read. Confirmed.

But the reused-construction claim does not hold in two places, which is the
finding below.

## The finding — `_plain_on_a_data_line` does not carry two of `is_plain`'s per-word guards

`is_plain` (`hooks/tokens.py`) rejects a command when any word begins
`--output` (it writes a file) and when `printf` takes a leading-`-` option
(`-v` assigns a variable). The new `_plain_on_a_data_line` reimplements the
per-command check and drops both. For `git` it returns at the subcommand
(`return args[k] in PLAIN_GIT`) and never inspects the later words, so
`git diff --output=<path>` reads as plain; and `printf` falls through the
final `return True`.

The failure this opens is the one R2f names. `git diff --no-index
--output=<path> -` writes a file, and `_writes_a_file` recognises only `tee`
with an operand and the `_WRITES` redirection operators — not `--output`. So
on a line such as

    cat <<'EOF' | git diff --no-index --output=.git/hooks/pre-commit - /dev/null
    <body>
    EOF
    git commit -m y

the sink's body is called data (verified: `heredoc_data` returns `[True]` at
the target), although the pipeline writes a file and a `git commit` on the
line runs hooks. R2f's own words — "nothing on the line can run that file" —
are violated, and the Grounding row promising R2c "reuses the same sets" as
`is_plain` is not met.

I could not drive this to a silent *executed* commit: `git diff --output`
emits diff-formatted text, not the body verbatim, so the written hook is not
valid shell and does not execute the body. That is why this is 🟡 (a
divergence from the rule's stated invariant and from `is_plain`, to fix or
justify) and not 🔴 (a demonstrated hole carrying an executed commit). The
`printf -v` gap is the same class with lower reach: it cannot re-point where a
commit lands, but it is the second `is_plain` guard the reimplementation drops.

The class (contract §12) is exactly these two: I enumerated `is_plain`'s
per-word checks against `_plain_on_a_data_line` / `_commands` — `steps_around_
hooks`, substitution/backtick/`${`/`$[`, `(){}`, program membership, the
`git -C/-c/PLAIN_GIT` rule, and the `${…=}` assignment are all carried (the
last two stricter); only `--output` and `printf -`option are missing.

Fix (validated in the clone: the probe's `git diff --output` and `printf -v`
cases flip to `heredoc_data=[False]`, and all 105 cases of
`test_a_heredoc_body_nothing_runs_is_data.py` still pass):

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_plain_on_a_data_line` drops two of `is_plain`'s per-word guards — `--output` (writes a file R2f/`_writes_a_file` then misses) and a `printf` leading-`-` option — so a data line can hold `git diff --output=<path>` writing a file a later `git commit` runs as a hook, against R2f's "nothing on the line can run that file" and the Grounding claim that R2c reuses `is_plain`'s construction | `hooks/tokens.py:396` (`_plain_on_a_data_line`), with `hooks/tokens.py:432` (`_writes_a_file`) | open | Verified in the clone: at the target `heredoc_data("cat <<'EOF' \| git diff --no-index --output=h - /dev/null\n…\nEOF")` is `[True]`; `is_plain` rejects both shapes (`--output`, `printf -`). Not driven to an executed commit because `git diff --output` emits diff text, not the verbatim body |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the 3 changed modules (`test_a_heredoc_body_nothing_runs_is_data`, `test_no_shape_the_base_stops_reads_silent`, `test_an_automation_run_meets_no_commit_prompt`), narrow, at the target | 172 passed |
| `bin/test` on `test_edits_go_through_the_edit_tool`, `test_one_word_one_meaning`, narrow | 29 passed |
| Parser probe `heredoc_data`/`commit_invocations`/`is_plain` over constructed strings (`git diff --output`, `printf -v`, CRLF, `\|& tee`, `git commit -F -`, `<<- 'EOF'`): no shell, no body executed | `git diff --output` and `printf -v PATH` both returned data=True at the target (the finding); flip to data=False with the paste-ready fix |
| `git diff --no-index --output=<f> -` fed a body, in a temp dir | exit 1, wrote `<f>` with the stdin as diff deletion lines — confirms `--output` writes a file that no redirection names |
| Broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Deferred

nothing to drain

## Paste-ready fixes

```python
# hooks/tokens.py, in _plain_on_a_data_line, immediately after the docstring
# and before `if program == "git":`
    program, args = command.program, command.args
    # Two of `is_plain`'s clauses, carried here so this stays its construction
    # (spec §Grounding): an `--output` option writes a file no redirection
    # names (`git diff --no-index --output=<f> -` puts its output there), and
    # `printf -v` assigns a variable, `PATH` included.
    if any(word.startswith("--output") for word in args):
        return False
    if program == "printf" and args and args[0].startswith("-"):
        return False
    if program == "git":
```

A case to plant (seen red against the target first, contract §15), in
`tests/test_a_heredoc_body_nothing_runs_is_data.py`, extending
`test_the_rule_answers_per_body`'s parametrize list:

```python
        # R2c carries is_plain's file-writing guards: `git --output` writes a
        # file no redirection names, and `printf -v` assigns a variable.
        ("cat <<'EOF' | git diff --no-index --output=h - /dev/null\nbody\nEOF", [False]),
        ("printf -v PATH %s .; cat <<'EOF'\nbody\nEOF", [False]),
```

Needs a fix: yes — 🟡 1 (`hooks/tokens.py:396`, with `:432`)

Loses a record or crashes: no

## Proof

Files opened at the target (clone of the worktree at `f75ef84b`):
`hooks/tokens.py`, `hooks/cmdline.py`, `hooks/cmdline_base.py` (unchanged,
verified by diff), `hooks/commit-review-gate.py`,
`skills/agent-contract/SKILL.md`, `docs/commit-review-gate-spec.md`,
`tests/test_a_heredoc_body_nothing_runs_is_data.py`,
`tests/test_no_shape_the_base_stops_reads_silent.py`,
`tests/test_an_automation_run_meets_no_commit_prompt.py`,
and the work item's `spec.md`, `overview.md`, `questions.md`, `survivors.md`,
`plan.md`, `phases/phase-2.md`, `phases/phase-3.md`,
`seal/ledger/1791076831-…md`, `seal/config.md`, `ruff.toml`, `CONTRIBUTING.md`.
Executed: the five `bin/test` / probe runs above, read in full.
Read, not executed: `gh` help for Q4 (the account's claim; unverified, carried
to the owner in `overview.md` §Not verified).
