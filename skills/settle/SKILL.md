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
settle --released-at REF          what counts as released, and the base the rule is
                                  asked at (default origin/main)
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

## A fold is not a work item

**A fold opens no directory under `seal/specs/`** — no `routing.md`, no
`spec.md` or `plan.md`, no round records — and the routing question is not
asked for it. This skill is its spec. It runs outside the review chain: every
commit carries `: '[no-review]';` in front of the command, quotes included,
and the one judgment it makes — which `docs/` file a rule goes to, and whether
the rule is still true — is reviewed at its pull request.

That is what ends the regress. A fold that opened a work item left a
directory behind for the next fold to retire, and that fold opened one of its
own, so no fold could ever finish. Nor does a fold keep a log of folds, under
`seal/` or anywhere else: a log is a record of a moment that would need
folding in turn. What a fold has to leave already has a home — what went
where is the `<!-- specs/<work-item-id> -->` marker in `docs/`, who checked
the prose is the pull request, and the removed text is git history, reachable
from the marker's id.

## The procedure

### 1. Read what is waiting

```
settle
```

It prints the released, unfolded work items grouped by **segment** — the file
their ledger coordinates anchor in — and lists beside them: the ones it cannot
group, the ones an open `evidence-todo.md` row is holding, the ones already
folded and waiting to be retired, and every ledger row anchored inside a
released directory (§4).

**A released work item with no `spec.md` is not yours to place.** It states
no rule, so there is nothing to fold out of it, and `settle` prints it under
its own heading: *retired by the rule* when nothing in its record is open,
*kept by the rule* when something is, with every open `## Not verified` and
`evidence-todo.md` row named. Such a row is a claim with an answerer, not a
rule, so it leaves by being closed (✅ with what closed it) and never with the
directory. A row re-homed — to `seal/follow-up.md`, to an issue — is closed
the same way, ✅ naming where it went, because a row deleted from
`overview.md` is refused on any pull request.

**Close it in a pull request of its own, and let that one merge first.** The
CI readers ask the rule of the merge base, so a row closed and its directory
retired in one pull request is still open where they look, and
`unverified-check` and `chain-check` refuse the removal that `settle --retire`
just made. Merged first, the ✅ also stays in the release branch's history,
where a closure made and removed in one squash would leave nothing. Once the
closure has merged, the next `settle --retire` takes the directory.

**Merged first means merged to the branch the release merges to, and `settle`
holds you to it.** The CI readers on the release pull request ask the rule of
the merge base of that pull request's base and its merge ref, which is the
base's tip. A closure merged only into the release branch is not there yet, so
a retirement in the same release turns the release pull request red. That is
what happened in 0.15.3 (#602). So `settle` asks the predicate of the merge
base of `--released-at` and `HEAD` as well as of the working tree. That is the
same commit as CI's until `--released-at` moves past the commit this branch
forked from. Once it has, the heading says so, and where `--released-at`
already holds the closure, merging it into this branch and running `settle`
again is what lets the directory go. A directory whose record is closed in the
tree and open at that base is listed under *kept until the closure reaches
<base>*, with every row open there, and `settle --retire` keeps it and exits 1.
It goes in a later pull request, once the closure has reached the branch
`--released-at` names, which for a closure made on a release branch is the
next release. A `--released-at` that shares no commit with `HEAD` has no merge
base, and both arms refuse it at exit 2 rather than asking the tree alone.

For every directory a retirement would take, by either arm, the report also
lists what would go with it: the open `## Not verified` rows in its overview,
and the paths outside `seal/specs/` that cite into it, which stop resolving
when it goes. Once for the run it lists every `tests/` file that reads
`seal/specs`, which is §3's grep done for you.

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

**A standing statement has one shape: the rule, its grounds, and what enforces
it.** It opens with the rule as one bold sentence, and the grounds follow as
prose. It carries exactly one line of its own that names what reads the rule,
and that line is written last:

```markdown
<!-- specs/<work-item-id> -->
**A cell may carry an escaped pipe.** A reader that stopped at one silently
took every row below it out of the config.
Enforced by: tests/test_config_rows.py::test_an_escaped_pipe_is_content
```

- **A target is a repository path**, relative to the root, optionally followed
  by `::<name>` for a `def` or `class` in that file. Several are separated by
  commas, and each may be written in backticks.
- **A rule nothing reads says so:** `Enforced by: nothing — <why>`, and the
  reason is not empty. Writing it is always possible, so it is the line a
  reviewer reads first; a check can make the choice visible and cannot make it
  right.
- **Stacked markers share one statement.** Consecutive marker lines are one
  group, and a statement runs from its markers to the next marker, the next
  heading or the end of the file.
- `Enforced by:` is a field name, so it stays English in every edition of a
  document, like every other name a checker matches.

**What this plugin checks, and what it does not.** It ships
`fold-check` (`skills/settle/scripts/fold_check.py`), which reads the shape
over the top level of `docs/`: the bold opening, one `Enforced by:` line, and
that each target names a file, and a `def` or `class` where it says `::name`.
It sets no value. A repository says where the shape starts to bind, because
statements folded before it will not carry the line, as a `Fold shape from`
row in `seal/config.md`; `templates/config.md` §*The fold's values* says what
each row accepts, and a row a repository does not write is a check it does not
run. Whether a target really enforces the rule is not read, the same way
*only what is still true* is not. Nor can any check tell that two standing
statements contradict each other. That takes a reader who knows what both
mean, and it is review's to find.

**One subject, one document, and a document over its ceiling takes no new
statement.** A rule goes into the document that owns its subject, so a reader
looking for it, and a reviewer looking for what contradicts it, opens one
file. A repository may set a ceiling on how large a document grows. A document
above that ceiling takes no new standing statement: the fold either splits it
first, along the headings it already has, or places the rule in the document
for the rule's own sub-subject, created only where none exists. The plugin sets
no ceiling; the repository states its value as a `Document line ceiling` row,
which `fold-check` holds every top-level `docs/*.md` to, and says what the
value is in the document that describes its own fold. A document already over
it is listed in an `Over the ceiling` row with its fold markers frozen until
the home it names splits it.

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
and of every released one with no `spec.md` and nothing open in its record,
and nothing else. An item the evidence-todo guard is holding is kept even when
the marker is there: the record says the prose landed, and the row says a fact
the reviewer verified has not reached the ledger yet.

**A directory a ledger row anchors into is kept too**, and the row is named
with its file, its line and its claim. Removing the directory would leave the
row BROKEN, and the checker would say so only after the directory was gone.
Every ledger `evidence-check` reads is read — `seal/ledger.md`, every
`seal/ledger/*.md`, every `seal/releases/*.md` and any `docs/**/_evidence.md`
— and every line of each, the ones above the first section marker and the
ones inside a fence included. The checker skips a fence that closes (#444),
and the guard reads it anyway, because keeping a directory the checker would
not break is the cheaper mistake. `settle` alone names them for every
released directory before you write any prose. Each row carries what
`CLAUDE.md` requires of it: **REMOVED** when every anchor it cites goes, and
its claim written anew where
it still stands; **narrow** when it keeps a live anchor, with the dead one
dropped — and whether such a row is removed instead is the repository owner's
question. The command edits no row. Answer them, and the next
`settle --retire` takes the directory.

**The retirement is the second half of the fold and never its own act.** A
directory removed before a policy document absorbed it takes the reasoning
with it, and that is the one loss nothing can undo. The marker is what makes
the order enforceable rather than remembered. The rule arm is not an
exception: a directory with no `spec.md` holds no reasoning for a document to
absorb, which is the whole of why it needs no marker.

## What a fold branch owes

**No `survivors.md` row.** The survivor sweep leaves a directory the range
retired — folded, or retired by the rule — out of the range on both sides, the
way it already leaves round records out: its sentences stand in `docs/`
because that is what a fold is, and the removed spec is not a place that still
instructs anybody. A sentence the same branch removes from anywhere else is
measured as before, and a survivor reported there is answered the ordinary
way.

**An answer for every check that reads the corpus** (§3), and for every row
`settle` names as anchored (§4).

**A clean `fold-check` where either row is declared.** Run it after the prose
is written and before `settle --retire`: it reads the statements this fold
just wrote, and a statement out of shape or a document the fold took past its
ceiling is cheaper to fix while the spec it came from is still on disk. Where
the repository declares neither row, the command says so and checks nothing,
which is not a finding.

**`seal/ledger.md` changes only by removal and re-verification.** So does
every `seal/releases/<X.Y.Z>.md`, where this repository's fold writes a
release's rows. A fold
appends nothing: it has no work item, so it has no fragment to append under.
It removes a row the guard named REMOVED, drops the dead anchor from a row it
named narrow, and re-reads and re-verifies — `evidence-check --reverify` — a
row whose anchored unit its own prose edited. Every other row is a content
anchor and survives the fold untouched.

## What this does not do

- It does not verify. Whether a coordinate still holds is `evidence-check`'s
  job, and folding that in would re-read the whole ledger at every release.
- It does not judge whether a sentence is still true, and it cannot: that is
  step 2, and it is why this ships as a skill with a command beside it rather
  than as a script alone.
- It does not fail a build. No gate refuses a branch for an unfolded work
  item, and a repository that never runs this is in exactly the state every
  repository was in before it shipped.
