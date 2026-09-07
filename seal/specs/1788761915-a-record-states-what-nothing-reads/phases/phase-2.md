# 1788761915-a-record-states-what-nothing-reads — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `b5ed944` |
| Ran by | unknown — the spawning session named no model in the prompt, and the row is the orchestrator's to fill |

## What this phase was asked

Build the identifier arm: a record of a live work item naming a backticked
identifier the tree does not have is refused, naming file, line and name; a
line carrying the invented-name marker is not. Cases seen red first, **the
tree's own four `chain_module` occurrences red before phase 3 corrects them**, <!-- NAME NOT IN TREE -->
and the 129 in shipped work items green throughout.

## What this phase found

**The arm is red on the tree's own four, and on nothing else.** `check_records`
over this repository names `rounds/round-2.md:62` twice and
`rounds/round-3.md:53` and `:58` of work item `1788749195` — the instance that
work item's own round 3 found by reading, three weeks of records later. 176
names are read to find them, and every other one passes.

**A single word in backticks is not read as a claim, and that narrowing was
forced by measuring rather than chosen.** Of the 55 distinct names that appear
nowhere outside `seal/specs/`, the 19 without an underscore are `cmp`,
`rpartition`, `divmod`, `pow`, `Starred`, `NameError`, `TypeAlias`, `EACCES`,
`PYTHONHASHSEED`, `RUF002`, `bin2`, `fixedly`, `monitors`, `resurrect`,
`themes`, `ASK`, `UNMEASURED`, `AMBIGUOUS` and `CITATION` — a shell command,
six stdlib names, an errno, an environment variable, a lint code, a probe
value, five words of ordinary prose, and three verdict words a checker used to
emit. Not one is a claim about a unit; all 36 compound names are. The
narrowing removes 56 of 146 occurrences and loses no true positive.

This is `plan.md`'s own repair for the false positive it predicts — *narrow
the pattern, do not widen the exemption* — arriving three years early. Without
it the first live record mentioning `str.rpartition` would be asked to mark it
`NAME NOT IN TREE`, which is marker noise attached to a name that is real.

**The spot-check of shipped records confirms `plan.md`'s boundary.** Six names
were opened at their coordinates. `header_of`, `row_baseline`, <!-- NAME NOT IN TREE -->
`_correction_traces` and `test_ledger_stamps_resolve` are units that existed <!-- NAME NOT IN TREE -->
when the record was written and were renamed or removed since; `cmp` and
`rpartition` are the false-positive class above. None is a live defect, which
is what the plan assumed and drew the boundary on.

**One existing case had to learn about the new output.** `evidence-check` now
prints a second section, and
`tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`'s
`test_the_printed_header_names_the_ledger_that_was_read` counted ledger
headers as *every unindented line that is neither blank nor the total*. It
reads `RECORDS_HEADING` from the checker now rather than carrying a second
copy of the sentence.

**Eleven mutations, all killed, and one of them only after a case was
written.** Dropping the binary sniff from the name corpus left all cases green
— nothing observed that a `.pyc` outside a cache directory must not supply a
name — so `test_a_binary_file_does_not_supply_a_name` was added and the
mutation re-run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the premise that a ledger header is the only unindented line `evidence_check.py` prints | `RECORDS_HEADING`, read by the case that counted them |
