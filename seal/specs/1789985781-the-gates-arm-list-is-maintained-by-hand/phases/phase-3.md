# 1789985781-the-gates-arm-list-is-maintained-by-hand — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 0ec4571 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The stamp saying what the seal did not answer. A6 over the rendered output,
red when the branch that prints it is deleted; W1's choice recorded.

## What this phase found

**W1 is answered both ways, and it had to be.** The question offered a count
or the names. `seal_stamp.letter` gives a panel value 23 columns and cuts at
the frame with no marker, so thirteen step names cannot go there — but A6 asks
that a reader can tell **which** steps the seal did not answer, and a number
alone sends them back to the two files this work item exists to stop them
opening. So the panel carries `workflow  8 of 13 not answered` and the names
go to stderr, on the same stream and beside the line that already names the
repository's own command. Neither alone satisfies both rows.

**The line prints before the checks rather than after them.** A run that comes
back `NOT SEALED` needs it as much as a sealed one: what the seal would not
have covered is a fact about the run, not about its verdict, and the failure
form draws no panel.

**A run that answers every step says so.** The first spelling returned nothing
when there was nothing to report, and the case that caught it is the one that
says why: silence there is indistinguishable from a gate that stopped looking,
which is exactly the state this work item found the gate in.

**The rendered assertion and the width assertion cannot be the same
assertion.** A value one column too wide is cut at the frame with no marker,
so on the drawing it reads as a shorter true statement. The case asserts the
whole value is present in the rendered line — a cut value would not carry its
tail — and measures the width against `PANEL_VALUE_WIDTH` off the panel data,
where the frame has not yet touched it.

**`panel()` takes the workflow text rather than reading the file.** Its three
existing callers in `tests/test_the_gate_asks_the_range_ci_will_ask.py` pass
four positional arguments and are untouched; the fifth is optional and
defaults to no workflow, which is also A7's state.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the reader's need to open `hygiene.yml` and `broad_gate.py` side by side to learn what a seal covered | the stamp's `workflow` row and the stderr line beside the command |
