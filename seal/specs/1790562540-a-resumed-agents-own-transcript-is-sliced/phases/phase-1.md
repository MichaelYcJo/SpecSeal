# 1790562540-a-resumed-agents-own-transcript-is-sliced — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 162b3754 |
| Ran by | unknown — the spawn prompt named neither the agent nor the model, and this row is the spawning session's to fill |

## What this phase was asked

`--segments` slices an own file. The own-file branch in `measure_segments`
(`own_file`, `unnamed` 0, rows from `segment_slices`), the own-file header and
legend in `report_segments`, and `report_breaches` leaving out its
reconciliation line when `own_file` is set. Cases S1, S2, S2b, S3, S4, S5, S6,
S7 and S9, and S11's pin for D1. The sentences this phase makes false, in the
same commit: D1 and D3–D11. The changelog fragment's entry, naming the
published readings (`spec.md` In 6). Stay out of `FAMILIES`, `family`,
`analyse`, `report` and the two comparability lines at the end of
`report_segments`, so item B (#642) rebases cleanly.

## What this phase found

**The frame holds on the code and not on In 6's grouping.** Opened with `gh
issue view` on 2026-09-28: #535's four fix-pass comments each say the numbers
are the whole transcript, so #535 belongs with #577 and #601 rather than with
the harness-notice readings. Six of #601's comments say whole transcript, not
ten; its four round-2 passes quote the harness's figures. #496 (four) and #619
(three) are the harness-figure readings. The changelog fragment groups them as
read. Nothing was sent back to the framer.

**The class had three more members than the table.** `SKILL.md`'s *Read the
counts above the table* paragraph says the mode prints the join counts even
when they agree, and the own-file page does not print them. `#measure_segments`'
docstring said a row is *exactly what a person running this script against
that one transcript gets*, which has been false for a slice since slicing
shipped. `#emit`'s residual said every row label is a relpath, and the own
file's is a basename. `#main`'s comment said *The other transcripts of this
run, one row each*. All four are narrowed in phase 1's commit, and none of
them is in B's column of `plan.md` §*Technical context*.

**The legend's `agent` line is the one line that changes shape in the walked
route's code, and not in its output.** It became a variable so the own-file
branch can print its own. The walked page's bytes are unchanged, which
`test_the_printed_segment_table_names_each_agent_and_its_own_span` and the rest
of the segment block hold.

**The header counts messages apart from slices.** Two adjacent messages cut a
file into two slices, not three (S2b), so the header reads *cut at 2
coordinator messages into 2 slices*. `resume_cuts` is read again for the count
in `report_segments`; `own_file` stays a bare `true`, as `spec.md` §*Data &
interfaces* asks.

**The resumed paragraph prints unchanged on the own-file page**, as `spec.md`
In 2 asks. Its sentence *only the file's opening could be joined* is still
true in general, and on this page nothing was joined at all, which the legend
line above it says.

**Red first (executed).** The seven cases for S1, S2, S2b, S3, S5, S6 and S7
were appended before any code changed and run against the base code: seven
failed (`0 segments found`, and `KeyError: 'own_file'` for S7). S9 and the D1
pin failed at the base the same way (the body carried the empty branch; the
section had no such sentence). S4 passed at the base, as the ticket's *must not
break* requires.

**Mutation (executed).** `mutate.py` in the session scratchpad, each mutant
applied to kept bytes, `tests/__pycache__` cleared between, the file verified
byte-identical after. Nine mutants over `tests/test_session_cost.py` and
`tests/test_session_cost_post.py`:

| Mutant | Red |
|---|---|
| M1 trigger on the `subagents/` directory, not the marker | S4 |
| M2 drop the nothing-beside half of the trigger | **none** — see below |
| M3 never set `own_file` | S2b, S5, S6, S7, S9 |
| M4 count the own file in `unnamed` | S5, S7 |
| M5 print the reconciliation for an own file | S6 |
| M6 never take the own-file header | S2b, S5, S9 |
| M7 label rows with the absolute path | S7 |
| M8 count slices where the header counts messages | S5 |
| M9 skip `emit`'s substitution | S9 and the two existing path cases |

M2 survived, so `test_a_file_with_transcripts_beside_it_is_walked_whatever_its_markers`
was added in 162b3754: red under M2, green restored.

**Narrow run (executed, at 8f885186 plus the overview).** `bin/test` over the
session-cost modules and every module that opens `README.md`, `README.ko.md` or
`skills/verify/SKILL.md` by path (43 modules): 2,115 passed, 7 skipped, 1
failed — `test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
because this work item had no `overview.md` yet. It was written, and that
module and `tests/test_unverified_rows_close.py` re-ran: 229 passed, exit 0.
`ruff check` and `ruff format --check` on the four touched Python files: exit
0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
