# the release guard globs one place — the closing memo

<!-- seal/specs/1788395377-the-release-guard-globs-one-place/overview.md —
only what the diff cannot show. The move itself alters no gate's verdict:
every evidence-todo file in the tree carries a `drained` line, so
`fold_ledger.py --check` prints the same bytes before and after it, which is
the second rung of the SDD ladder rather than the file count that ladder
excludes by name. Round 1's fixes then changed a hook's reminder text, a
skill's instructions and a spec table — three of the five clauses the ladder
puts on the rung ABOVE — and the grounds sentence was rewritten in the same
commit without being re-read against them. A plan cannot be written after the
fact, so this note is the record that they went in without one; round 2 is
what found it. -->

## What the diff does not show

**The defect was found by asking a question, not by reading a diff.** During
#82's round 1 the orchestrator asked what `fold_ledger.py`'s glob actually
reaches and ran it both ways: three files seen, two not. Nothing in the tree
was wrong to read — both misplaced files carry a `drained` line, so the guard
would have answered the same either way. What was wrong is that its silence
had stopped meaning anything for two of five work items, and no reading of
either file would have said so.

**The test pins the layout, not the glob.** The obvious test asserts the
glob's pattern. That pins the line least likely to move: the glob is one line
in one script, and the layout is written by hand once per work item, by
whoever creates the directory. So the case asserts that no `tests-todo.md` or
`evidence-todo.md` sits below the work item's own level, and asserts that at
least one sits at it — the second half so the case cannot pass by finding
nothing, which is the failure mode the defect itself was.

**Why the files were in the wrong place is worth knowing.** `round-N.md` is
plural and unbounded, so it earns a directory; the two todo files are one
each and do not. Two work items read `rounds/` as "the review's files" and
put all three there. That reading is reasonable, which is why a test is worth
more than a correction.

## Where spec and implementation diverged

Nothing. The ticket's three done-when rows are the whole of the work.

## Not verified

| Item | Who must answer |
|---|---|
| The guard refusing a real release with a real open row — every file in the tree is drained, so the refusal path is exercised only by fixtures | the repository owner, at the first release that meets one |
| The broad gate | the orchestrator, after the review round |

## Fed back into the spec

Nothing. `docs/review-handoff-protocol.md` already said where the two files
go; the tree disagreed with it and now does not.
