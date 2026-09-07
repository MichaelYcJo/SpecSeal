# 1788761915-a-record-states-what-nothing-reads — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `6de1bca` |
| Ran by | unknown — the spawning session named no model in the prompt, and the row is the orchestrator's to fill |

## What this phase was asked

Correct the four `chain_module` occurrences phase 2 turned red, and write the <!-- NAME NOT IN TREE -->
marker where a reviewer will meet it. Verified by phase 2's check over the
tree, exit 0.

## What this phase found

**The marker has two meanings and only one of them was written down.**
`skills/code-review/SKILL.md` shows `NAME NOT IN TREE` beside a name a
paste-ready fix is *proposing*, and the four occurrences here are the other
kind: work item `1788749195` deleted `chain_module` on its own branch, and <!-- NAME NOT IN TREE -->
three of its round-record rows still name it. Round 3's own grounds cell says
it — *the name is simply gone from the tree*. Marking those lines is not a
concession, it is the record saying what is true, so the checker's message
was widened from *proposing the name rather than citing one* to *where the
record means a name the tree does not have*, and the skill now carries both
meanings under one marker.

**The three rows are corrected in place rather than rewritten.** A round
record is a record of a moment, and the rows are true about the moment they
were written; what was missing is the statement that the name is absent now.
Each keeps its sentence and gains the marker.

**Four occurrences on three lines.** `rounds/round-2.md:62` carries the name
twice — once in the Finding cell and once in the Grounds cell — so the marker
on that line closes two of the four. The exemption is per line, which is what
makes that arithmetic work and what
`test_the_marker_exempts_the_line_and_not_the_name` pins.

**The check reads 169 names over the tree and refuses none.** Exit 1 remains,
and it is the ledger arm reporting drift in three rows this branch's own
edits moved — `evidence_check.py#main`, `skills/code-review/SKILL.md#"##
Findings format"` and the header-counting case. Those are re-read and
re-stamped in phase 6.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the reading that `NAME NOT IN TREE` marks only a name a fix is proposing | `skills/code-review/SKILL.md` §Findings format, which now carries both meanings, and the checker's own refusal message |
