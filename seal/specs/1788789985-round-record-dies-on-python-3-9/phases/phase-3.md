# 1788789985-round-record-dies-on-python-3-9 — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `5ed5fe7` |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Write the records the repository's conventions ask for, at the addresses those
conventions name rather than the ones the skill names: the changelog entry to
`seal/specs/<work-item-id>/changelog.md` and never `CHANGELOG.md`, the ledger
rows to `seal/ledger/<work-item-id>.md` and never `seal/ledger.md`, with
`path#major@hash` coordinates and no line numbers. Write every other member of
the class into `seal/follow-up.md` with an answerer named, because a deferral
to nobody is how *someone will look at it* becomes nobody did.

## What this phase found

**The record checkers caught two defects in the records, and both were mine.**
`evidence_check` refused three `round_record.py:761-766`-shaped citations in
the ledger fragment's prose as unmigrated coordinates — correctly, since a
coordinate names content here and a line number is the thing this repository
spent three review rounds getting rid of. It also refused a bare backticked
`` `py_compile` `` — NAME NOT IN TREE, and that is the sentence's whole point —
in three records, as a compound identifier nothing outside
`seal/` carries. The second is the more interesting one, and this record was
itself refused twice for quoting the offending name while explaining it, which
is the check working and the marker doing its job on the line rather than on
the name. The same name inside a
longer backticked span, `` `/usr/bin/python3 -m py_compile` ``, passes, because
a span with spaces reads as a command rather than as a claim about a unit in
this tree. So the fix for both was to name the command or the unit instead of
the position, which is what the rows were trying to say anyway.

Neither would have been caught by reading. Running the checkers on the records
is as much a part of closing a phase as running the suite on the code.

**`gather_changelog.py --check` exits 1 on this branch and that is correct.**
It reports the fragment as ungathered, which is what a pre-release feature
branch should look like: the fragment lives from the work item's first row
until the release that gathers it. Worth saying because a red check at the end
of a run reads as a failure unless somebody has written down that it is not.

**The deferral has a home problem the handoff could not have known about.**
`seal/follow-up.md` opens by saying that a repository with a tracker should
normally hold none of these rows, and that anything tied to a coordinate is a
`# RIDER:` at the line it is about. Both rules point away from this file. A
rider was weighed and rejected on its merits — the finding is about a class of
five files and a rider at one line cannot say *and four others*, and nobody
opens `gather_changelog.py` before running it — but the tracker question is a
person's, so it is `questions.md` Q1 rather than a decision taken quietly. The
row went where the handoff asked, because a row in the wrong file is
recoverable and a deferral to nobody is not.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
