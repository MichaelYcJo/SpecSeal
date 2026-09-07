# 1788789985-round-record-dies-on-python-3-9 — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `c67a210` |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Make `round_record.py` exit at entry on an interpreter below the floor with a
sentence naming the floor and the interpreter it found, before argument parsing
does any work a reader could mistake for progress; change nothing above the
floor; leave `strict=True` where it is; and plant a regression test that was
**seen red** against the current code. The hard part named in the prompt: a
version guard tested from an interpreter that satisfies it, and *do not settle
for a test that only asserts the constant exists*.

## What this phase found

**The guard's placement is the finding, and only one case can see it.** Seven
mutations were run against the eleven cases. Six of them — the boundary, the
version dropped from the sentence, the exit code, the write, the *nothing was
written* clause, the floor itself — are caught by the end-to-end cases, which
is what one would hope. The seventh moved the guard out of module level and
into the first line of `main()`, which is where a version guard is naturally
written, and **every end-to-end case stayed green.** Only
`test_the_guard_precedes_every_other_module_level_act`, which reads the
module's AST, went red.

That is not a quirk of the test suite. `chain = load(CHAIN,
"specseal_chain_check")` at `round_record.py:128` reads and executes a second
file at import, before `main()` is called at all, and it was measured to
succeed on 3.9.6 — so a guard in `main()` really would let the operator watch
the script open and run another file before telling them the interpreter is
wrong. That is the ticket's complaint reproduced by the fix for it.

**Two ways to test a version guard from an interpreter that satisfies it, and
each needs the other.** Copying the real script into a temporary directory and
raising `FLOOR` above whatever is running exercises every shipped line of the
guard from any interpreter, so CI stands on it and it never skips — but on its
own it proves only that the code behaves when the constant is moved. Finding a
genuinely old interpreter and running the real file at its real path is the
honest article and skips on every CI runner. The pair is what makes either one
worth having, and the second is what would catch the first lying.

**One assertion was passing for the wrong reason, and the shape of it is worth
carrying forward.** `assert python in out.stderr`, with `python` being
`/usr/bin/python3`, held while the message named
`/Applications/Xcode.app/Contents/Developer/usr/bin/python3` — because macOS
resolves the system stub to a shim inside Xcode whose path *ends with* the
string being searched for. A green assertion about a path is not an assertion
about the file. It now asks the named path what version it is and compares
that, which is the claim a reader of the message actually depends on.

**A control case earns its place beside the refusal cases.** A guard that
refused everything would satisfy every assertion about the refusal.
`test_above_the_floor_the_same_arguments_get_past_the_guard` runs the same junk
arguments with the floor left alone and requires the script to reach its own
argument handling and complain about the work item instead.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The docstring's claim that exit 2 means *the input was unusable and nothing was written* — exit 2 now also covers a refused interpreter | the same line, rewritten: the code is documented as covering both, because a code whose written meaning is quietly widened is a code nobody can read. `tests/test_a_script_says_which_interpreter_it_needs.py#test_the_docstring_says_what_exit_2_now_covers` pins it |
