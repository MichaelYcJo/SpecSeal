# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d87da322 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

Give `hooks/config.py` a pure reader that reports the first line refused after
the header, and have `skills/verify/scripts/broad_gate.py#missing_row` use it:
where the refused line's first cell is `Broad gate`, say the line will not
parse and quote it, in place of *has no `Broad gate` row*. Same exit 2, same
moment, a different sentence. `hooks/mode-gate.py` is not touched, and a case
pins that it still denies nothing.

Phase 1 had to come first, and `plan.md` says why: this phase's fixture is a
line that still will not parse after the escape is taught, which is the
**unescaped** pipe. Written the other way round the fixture would have been an
escaped pipe, phase 1 would have made it parse, and the case would have gone
green for a reason nobody intended.

## What this phase found

**The rename `plan.md` puts in phase 4 had to happen here, and it pulled the
ledger with it.** `tests/test_the_seal_is_taken_once_by_the_sealer.py`'s
`test_a_piped_row_is_refused_by_the_table_and_not_by_this_refusal` <!-- NAME NOT IN TREE: this phase renamed it; the new name is two sentences below. --> asserted
the message this phase changes, so the phase could not close with that case
standing — and its own name states the behaviour that stopped being true. It
is now `test_an_unescaped_pipe_is_named_as_a_line_that_will_not_parse`, and
its docstring keeps the sentence the old one ended on: *so that the day
`config_rows` learns to carry a pipe, this case is what says so.* This is
that day.

Renaming it removes an anchor rather than drifting one, and
`seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md`
cited it. So this phase carries the ledger work `plan.md` scheduled for
phase 4: the falsified row removed where it stood, four new rows written into
this work item's own fragment, and the three drifted rows elsewhere re-read
rather than swept. What is left for phase 4 is the documents.

**A third refusal joined the gate's header, and a case name said there were
two.** `broad_gate.py`'s module docstring enumerates what the gate does in
order, and its first item read *a row is refused two ways*. A header that
keeps saying two teaches the next reader that a refusal they will actually
meet does not exist, so it now reads three and names this one.
`test_the_module_header_names_both_refusals_and_neither_names_a_command` <!-- NAME NOT IN TREE: renamed on this line; the new name follows it. -->
became `test_the_module_header_names_every_refusal_and_none_names_a_command`
— a second rename, and this one reached a round record.
`seal/specs/1789445605-.../rounds/round-2-report.md:191` names the old case,
and a record naming a unit the tree lacks takes even the non-strict
`evidence-check` to exit 2. That line now carries `NAME NOT IN TREE` with the
new name beside it, which is what the arm's own rule prescribes for a record
that is history: the round read what it read.

**W1 is decided: the whole line, quoted.** A refusal that shows only the first
cell sends the reader back to the file to guess which line it meant, and the
line comes from the person's own file at runtime, so nothing about it reaches
a fixture. The refusal also names the escape and shows the row that runs the
command, because *this will not parse* with no way forward is half a message.

**The branch reads the refused line's first cell, and that narrowing is
load-bearing.** A refused line naming some other item leaves the `Broad gate`
row genuinely unread, and the absent-row refusal is the true one there. Red
without it: a config whose unparseable line reads `| Record language | a | b |`
came back quoted as though it were the `Broad gate` row.

**`refused_row` reports and refuses nothing, which is what keeps
`hooks/mode-gate.py` out of it.** Nothing in the new unit raises, so importing
it makes no caller able to deny. The hook is left exactly as it was and a case
pins that: a config whose `Mode` row is hidden below an unparseable line still
reads as undeclared, and the gate still simply asks the mode question again.
That is the stated cost of keeping a `PreToolUse` hook silent, and it is in
`spec.md` §*What this repair cannot see* rather than being discovered later.

**A5's guard was added to an existing case rather than written as a new one.**
`test_the_absent_row_refusal_sends_the_question_to_a_person` already reads the
message a genuinely absent row gets; it now also asserts the new sentence is
**not** in it. Without that, the new branch could take every refusal and that
case would still pass on its four original sentences.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_a_piped_row_is_refused_by_the_table_and_not_by_this_refusal` <!-- NAME NOT IN TREE: removed by this phase's rename. --> — renamed, so its anchor is removed rather than drifted | `test_an_unescaped_pipe_is_named_as_a_line_that_will_not_parse`, in the same file. The ledger row citing the old name was removed from `seal/ledger/1789445605-...md` and the new claim written into this work item's fragment |
| `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py#test_the_module_header_names_both_refusals_and_neither_names_a_command` <!-- NAME NOT IN TREE: removed by this phase's rename. --> — renamed for the same reason | `test_the_module_header_names_every_refusal_and_none_names_a_command`. No ledger row cited it; the round record that did carries `NAME NOT IN TREE` |
| the `Broad gate` row's file read, duplicated in `broad_command` | `skills/verify/scripts/broad_gate.py#config_text`, which both readers of the file now call |
