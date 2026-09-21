# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8311d7a2 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The check proper: merge commits in a range, both parents, both markers, every
lost marker named. A1, A2, A3 and A6, each red first, and a fixture builder
that makes two branches, a real conflict and a taken side.

## What this phase found

**The merge base is a third input the frame did not have, and M1 is what
found it.** `spec.md` §Scope 1 reads *either parent*, and phase 1 measured
that rule over this repository's reachable history: one merge, five markers,
and no defect. The shape it reported is a parent's own deliberate deletion
that the merge honoured, and it is indistinguishable from #424's incident
without a third reading — in both, the result equals one parent and the other
parent's marker is gone. `overview.md` carries the divergence row and the
docstring carries the table.

**What the base test costs is nothing the acceptance rows care about.** It
only narrows, and in every one of A1, A2, A3 and A6's fixtures the base
carries no marker at all, so none of them moved. That is a property of the
fixtures rather than luck: a correction is by definition something one side
ADDED, so the base is where it is absent.

**The fixture commits with `--allow-empty`, and that is load-bearing rather
than a convenience.** The side that reverts a correction is the side that
changed NOTHING — it forked before the correction and kept the old text. Git
refuses an empty commit, so without the flag the fixture died building the
very shape the ticket is about, three cases before the check was reached.

**The conflict is attempted and then overwritten, which is the act being
modelled.** `git merge --no-commit` is allowed to fail; what follows is the
resolution written over the file by hand and committed. That is what a person
does at a conflict, and building it any other way would model git's automatic
merge instead of the resolution.

**Both parents are read, and one case exists only to say so.** Which side a
conflict is resolved onto is whatever the person had checked out, and the
correction is as likely to be on the other one. The mutation that reads
`kin[:1]` leaves every other case green.

**Two units still had nothing behind them at this phase's close**, and both
are phase 3's subject rather than an oversight: the empty-range branch of the
report (A5) and the difference between a blob a rev does not carry and a blob
that could not be read.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
