---
name: settle
description: |
  Retire a released work item by folding what is still true out of its
  `spec.md` into a `docs/` policy document, then removing the directory.
  Use when: preparing a release and the work items have accumulated; a
  session asks what `seal/specs/` is still holding, or runs `settle`.
  NOT for: gathering changelog or ledger fragments, which release
  preparation already does; judging whether a ledger coordinate still
  holds (`evidence-check`); anything in a work item that has not shipped.
---

# settle — the fold a shipped spec has been waiting for

A work item's directory is written to be read while its pull request is open.
After the merge nothing mechanical reads it and people rarely do, and it stays
on disk forever: 98 work items, 1,338 files, 15M on the tree this shipped
from. `seal/README.md` has said each one "waits until a later `settle` folds
it" since the root existed, and until now nothing folded anything.

**The command reads and groups; you judge and write.**
`docs/one-root-by-lifetime.md` §*What keeps `settle` light* fixes the split —
the step "moves and does not verify" — and folding *only what is still true*
is a judgment about truth. So `settle` supplies the corpus and never writes a
sentence into `docs/`; every standing statement below is written by the
session, and the command's second arm removes only what one of them already
absorbed.

```
settle                            what would fold, grouped by segment
settle --retire                   remove the directories whose fold docs/ records
settle --released-at REF          what counts as released (default origin/main)
```

The script is `skills/settle/scripts/settle.py`, and `bin/settle` is on the
Bash tool's PATH while the plugin is enabled. It needs python 3.12 or newer
and says so at entry rather than dying partway through.

**It refuses to run in local mode, and that is the one layout it will not
touch.** A `seal/` root under the common git directory is never committed, so
no ref holds the work item directories, nothing in them reads as released, and
nothing removed from them could be recovered. `seal mode shared` moves the
root into the tree and `settle` works from there. Every other command in this
plugin reads both places; this is the one that stops, because it is the one
that deletes.

## When it runs

**By hand, named as a step in the release checklist.** It is invoked, never
triggered: no hook runs it, no gate refuses a branch over an unfolded work
item, and it is not part of the release-preparation commit that gathers the
changelog and ledger fragments. Folding writes policy prose, which is a
judgment act, and a release that stops for somebody to write documentation is
a release that stops.

## The procedure

### 1. Read what is waiting

```
settle
```

It prints the released, unfolded work items grouped by **segment** — the file
their ledger coordinates anchor in — and three lists beside them: the ones it
cannot group, the ones an open `evidence-todo.md` row is holding, and the ones
already folded and waiting to be retired.

A work item is **released** when its directory is present on the branch the
release merges to. `--released-at` names that branch.

A `tests/` anchor rolls up to the code the case pins, by majority over the
work item's own code anchors: a case pinning a checker's behaviour is evidence
about the checker. An item whose anchors are all under `tests/`, or which
wrote no ledger row at all, is **named rather than guessed at** — the link
from a case to the code it pins is nowhere a machine reads. Those are yours to
place, or to leave.

### 2. Write one standing statement per segment

For each segment, read the `spec.md` of every work item in it and write **what
is still true** into `docs/`.

- **Only what is still true.** A spec is the spec of one change, and what a
  later work item overturned goes nowhere. Deciding which sentence is which is
  the whole reason this half is yours.
- **One standing statement, not spliced sentences.** The output is a rule a
  reader can act on, not 97 quoted fragments under their provenance comments.
- **Merge into a document that already exists**; create one only for an area
  that has none. `docs/` is flat — there is no `docs/policy/` directory — and
  the file is named for the segment where a new one is needed.
- **The newest work item wins** where two say different things.
- **Every folded sentence carries its work item's comment**, on a line of its
  own:

```markdown
<!-- specs/1788302682-the-release-check-never-watched-bin -->
`bin/` ships, so a change to a wrapper moves the version like a change to a
skill does.
```

That comment is the provenance a reader traces back through git history once
the directory is gone, and it is **also the fold's record**: `settle` reads it
to know what has been folded, so there is no second file to keep in step and a
run interrupted between writing the prose and removing the directory picks up
where it left off. It is the same marker `.github/scripts/fold_ledger.py` and
`.github/scripts/gather_changelog.py` already write, and it is read on a line
of its own — a marker quoted inside a sentence is a description, not a fold.

### 3. Answer every check that reads the corpus

**A fold is not finished until every check in your own repository that carries
a population floor over `seal/specs/` has been answered.** This is the step
that is easy to skip and expensive to skip, and it is general rather than one
repository's circumstance: any project running this methodology accumulates
checks over its own records, and a floor is exactly the shape a check takes
when its author worried about a vacuous pass.

`docs/one-root-by-lifetime.md` §*The dependency rule* names two such readers.
**That list is not the whole list**, and it was never meant to be read as one:
it was written when the repository had thirteen work items and most of the
cases did not exist. Measured on this repository before the mechanism shipped,
**fourteen test modules read the real corpus and at least six carry a
population floor a fold turns red** — assertions of the shape
`assert len(records) > 200` over a walk of `seal/specs/`, and non-empty
assertions over globs of `routing.md`, `evidence-todo.md` and `pr.*.md`. Eight
more read it with no floor and would silently assert less.

So before anything is removed, find them:

```bash
grep -rn "seal/specs" tests/
```

Each one gets one of three answers, and the answer is written down:

| Answer | When it fits |
|---|---|
| **retire the case** | it was about a shape the fold removes, and nothing is left for it to be about |
| **re-point it at a fixture corpus** | the property is still worth checking, and a built tree checks it better than whatever the repository happens to hold |
| **decline** | the case is right and the floor is right, and the fold waits for that population to exist again |

A fourth answer — lowering the floor until the run passes — is the one that
turns a check into a comment.

### 4. Retire what the policy absorbed

```
settle --retire
```

It removes the directory of every released work item whose fold is recorded,
and nothing else. An item the evidence-todo guard is holding is kept even when
the marker is there: the record says the prose landed, and the row says a fact
the reviewer verified has not reached the ledger yet.

**The retirement is the second half of the fold and never its own act.** A
directory removed before a policy document absorbed it takes the reasoning
with it, and that is the one loss nothing can undo. The marker is what makes
the order enforceable rather than remembered.

## What a fold branch owes

**A `survivors.md` range-row.** `seal/specs/` outside `rounds/` is in the
survivor sweep's corpus, and that step runs on every pull request into a
release branch. A branch that deletes a shipped section leaves every sentence
of it standing in the durable copies that are supposed to survive a deletion,
so the sweep reports all of them — one real range reported 153, every one
correct as a report and none of them a defect. Writing 153 rows is not an
escape anybody takes; the row shape for a whole range exists so that the
alternative is not turning the check off:

```markdown
| Range | Grounds |
|---|---|
| `origin/release/vX.Y.Z...HEAD` | a fold removes shipped sections whole, and
  their sentences stand in the durable copies by design |
```

That row is anchored on the range **and** on the work item whose
`seal/specs/<id>/survivors.md` holds it, so it cannot become a standing
*check nothing*.

**Nothing in `seal/ledger.md` moves.** A ledger row is a content anchor and
survives the fold untouched. The fold is about the spec's prose, not about the
rows the work item wrote.

## What this does not do

- It does not verify. Whether a coordinate still holds is `evidence-check`'s
  job, and folding that in would re-read the whole ledger at every release.
- It does not judge whether a sentence is still true, and it cannot: that is
  step 2, and it is why this ships as a skill with a command beside it rather
  than as a script alone.
- It does not fail a build. No gate refuses a branch for an unfolded work
  item, and a repository that never runs this is in exactly the state every
  repository was in before it shipped.
