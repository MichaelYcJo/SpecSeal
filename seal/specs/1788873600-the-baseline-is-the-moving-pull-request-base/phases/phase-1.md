# 1788873600-the-baseline-is-the-moving-pull-request-base — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `21b5e98` (opened at `8af68df`) |
| Ran by | smith on `claude-opus-5[1m]` — the spawn prompt named no model; this is the harness's own model line, not a value the segment decided about itself |

## What this phase was asked

Take the repair the ticket's *What would close it* section names, and where
that section leaves a choice open, take the narrower option and record the
wider one in `questions.md` with the repository owner as its answerer.
Rebasing is out and nothing may propose it. The ticket's own gate: *does any
arm want the moving base?* — to be **read rather than assumed** — and the case
has to be **seen red**, a base moved forward with a work item the branch never
had, green under the merge base and red under the base today, because without
that control the change is indistinguishable from making the arm inert.

## What this phase found

**The ticket's repair section is wrong about one arm, and reading it is what
the ticket asked for.** It says *"the other two arms already read only this
branch's own files"*. `show(root, args.baseline, rel)` reads the base
revision, so the row-count arm calls the base exactly as the file-is-gone arm
does; a base that gains a row in this branch's own overview after the fork
reports rows the branch never had, and
`test_a_row_the_base_gained_after_the_fork_is_not_a_deletion` is red against
the pre-fix module. So there are **three** reads of the base and not one — the
missing-path arm is the third, and it made a work item only the base's tip
ever had read as a work item this branch deleted.

**That turns the narrow/wide choice around.** Applying the merge base at the
arm the finding names is the *larger* change, because it puts two arms of one
refusal on two revisions and prints both in one report. The narrow change is
one substitution where the ref is resolved. `check_text`'s own docstring
prices the alternative: two readers of one thing, *"four pairs drifted apart
across three review rounds — and each fix on one side opened a gap on the
other."*

**The message needed a rule, not a second shape.** Naming the ref after the
change would send a reader to a commit the run never opened; naming the merge
base always would rewrite the text of every case written before this change.
The rule that resolves it is *the shortest name that is true*: where the merge
base is the ref's own commit — `--baseline HEAD`, and CI — the ref names the
compared revision exactly. So `base_label` is one rule and not a conditional
message, and both of its mutations die.

**Where the arm actually fires is the local gate, not CI.** `actions/checkout@v4`
on a `pull_request` event checks out the merge of the head into the base, so
the squashed sibling's `overview.md` is in the working tree and the set
comparison finds nothing missing — and the merge base of the base ref with
that commit is the base tip, so the repair is a no-op there. That is **read,
not executed**, and it is in the overview's `## Not verified` with an answerer.
The repair is correct under both checkout shapes, which is what makes the
reading safe to build on rather than load-bearing.

**Two branches cannot be driven by a fixture, and the mutation loop is what
found them.** `git merge-base` exiting 0 with an empty line, and
`rev-parse --verify --quiet` doing the same — no git this repository requires
answers either way. Both are induced with `monkeypatch`, the way this module's
`relpath` cases already are, so they run on every leg; the second is what keeps
an empty answer from travelling out through `resolves` to `chain_check.py` as
a resolved ref. Eleven mutations, ten dead on the first pass, and the survivor
dead once its case existed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Nothing from the tree. `resolves`'s rev-parse call moved into `commit_of` and `resolves` kept its name, signature and predicate shape, because `chain_check.py` loads this module and calls it by that name | none — `seal/ledger/…#R2` carries the claim and the 303 cases that hold it |
