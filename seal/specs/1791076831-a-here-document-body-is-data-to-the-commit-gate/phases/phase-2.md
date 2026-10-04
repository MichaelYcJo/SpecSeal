# 1791076831-a-here-document-body-is-data-to-the-commit-gate — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 33a8f1f3 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The gate reads only what can run. Build the R2c–f shape check as one function
beside `is_plain`, reusing its sets and leaving its output unchanged, then let
`commit_invocations`' top-level loop skip the bodies R makes data. Plant S1–S8,
each seen red at `101f9bd0` (S1–S4) or green before and after (S5–S8), and
move the one S10 corpus row with its docstring sentence. Every other r2 and r3
corpus row must still stop, and `test_a_heredoc_that_never_terminates_
swallows_the_rest` must still pass. Enumerate the shapes by construction: a
shape the rule lets through silently must be one that cannot carry an executed
commit. Answer Q4 (`gh`) and Q5 (opener counting) where the plan places them.

## What this phase found

**The rule as built is stricter than R2f in two places, and only there.** A
sink's body reaches a file when ANY stage of its pipeline writes one, not only
the sink itself: `cat <<'EOF' | tee f.sh` puts the body in `f.sh` through a
stage that owns no body. And the programs that can run such a file are any
`python3`/`python`, any `git`, and a `gh` subcommand outside the measured
remote-only set, where R2f named the Python consumer and `git … commit`:
`git add` runs the `post-index-change` hook, so "a commit runs hooks" holds
for more than `commit`. `overview.md` records both, with the stricter side
chosen.

**Q4, measured from `gh <group> <sub> --help` at gh 2.100.0.** Of the four
groups, these run local git and are not remote-only: `pr create` (pushes a
branch that is not pushed), `pr checkout`, `pr merge` and `pr close`
(`--delete-branch` deletes and switches the local branch), `issue develop`
(`--checkout`), and `release create` (`--notes-from-tag`). None of the four
groups runs a file it is handed or its stdin. R2c keeps all four groups, and
R2f counts those six subcommands, and any unknown one, as able to run a file
the line wrote. The help text is read, not executed: the enumeration below ran
`gh` as a stub.

**Q5: the count alone is not the right guard, the count and the words are.**
A fuzz of 400,000 random lines over 54 fragments, seed 739, admitted 738 that
R2c's other clauses accept. On 475 the reader and `shlex` agree on every
opener; on 18 the counts differ; on 245 the counts agree and the words do not
(`tee > tee <<- \` and a line continuation is one). So a count can match while
the owners differ, and R2d's check compares each opener's word on the line
with the delimiter of the body it claims. That is why the record carries
`delimiter` and `dashed` (phase 1). Every disagreement is rejected, so it
keeps a body read and opens nothing. No special handling was added.

**The shapes, enumerated by construction.** The axes are R's: 6 delimiter
spellings, `<<` and `<<-`, a terminator that arrives or not, 23 consumers, 11
output redirections, 9 pipeline tails and 21 followers on the line or after
the terminator, including a second body. That is 1,147,608 shapes holding
1,215,918 bodies. The rule calls 40,608 bodies data and reads 1,175,310. Every
shape with a body called data was then run with the delimiter spelled `'EOF'`
and `\EOF` in `/bin/bash` 3.2.57 and `/bin/zsh` 5.9, in a scratch repository
whose `f.sh`, `h.sh` and `g.txt` and whose `pre-commit` and
`post-index-change` hooks already existed and were executable, so a sink that
overwrote one kept the executable bit. Each body was a script that marks a run.
Of 35,616 runs, no body the rule called data ran: 0 holes. 32 runs hit the 15
s bound, and the marker was read at the bound in those too. A second run named
them, and all 32 are one zsh family: a sink writing `pre-commit` or
`post-index-change` and piped to `cat > f.sh`, which zsh's MULTIOS fills with
the same body, then a Python follower running `sh f.sh`. The body's commit
runs the hook, the hook is the body, and it commits again. In every one the
sink's body is read, because a Python program stands on the line; the body the
rule called data was the Python program's own.

**Mutation, one break per added unit, through `bin/mutation-check`.** Of 33
breaks on the first pass, 29 went red. Three survived (an unknown operator read as a
redirection, a `git -c` of any key, every pipeline merged into one), and the
parentheses check was refused because its line also occurs in `is_plain`.
`33a8f1f3` planted the cases those needed, and all four went red on the
second pass. Two units went with no case to hold them: `printf -v`,
since no `$X` may stand as a program on such a line, and the unreachable
`KeyError` for an unknown `gh` group, now a lookup that reads it as a runner.

**A second copy of the S10 shape.** `tests/test_an_automation_run_meets_no_
commit_prompt.py::test_the_four_measured_shapes_are_refused_under_the_press`
holds the same "a patch whose body loops over a commit string" command as the
corpus row. It went red with the fix and now asserts that one shape silent
with the press and without.

**Seen red.** The new module was copied into `git archive 101f9bd0` and run
there: every case asserting silence failed (29), and every case asserting a
stop passed. Breaking the gate's skip back to the base reading through
`mutation-check` turned the silent cases, the moved corpus row and the
automation case red at the head.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The corpus row "measured: a patch whose body loops over a commit string" | `tests/test_no_shape_the_base_stops_reads_silent.py::test_the_one_row_that_left_the_corpus_reads_silent`, asserting the opposite |
