# The evidence ledger — what a row claims, and what reads it

A ledger row pairs a claim with the code that makes it true. `seal/ledger.md`
holds the rows a release has gathered; `seal/ledger/<work-item-id>.md` holds
the rows one branch is still writing. This document is the standing account
of what a row is, what each checker over it refuses, and what a merge can
take out of one without anybody noticing.

It is a policy document: it outranks the SDD set, and a work item that finds
it wrong corrects it rather than working around it.

## A row is a content anchor, and it names no commit

<!-- specs/1788229400-every-branch-appends-to-the-same-two-files -->
**A coordinate names content, never a position:** `path#major@hash`, or
`path#major>minor@hash` where a claim needs narrowing. The major level is the
enclosing unit — a function or a class for code, a heading path for a
document. A row carries no line number and no commit SHA, and the check calls
git for nothing.

That removes a whole chain rather than one rule from it. A line number moves
for edits unrelated to the claim, so the coordinate rotted, so the row was
re-anchored, so its baseline reset, so a stamp was needed, so a squash
orphaned the stamp. The measured instance: a commit seven rows named was not
an ancestor of the default branch after a rewrite, so a fresh clone and CI
both read those rows as broken — for a history operation none of the seven
claims was about.

**An anchor degrades to `DRIFTED`, never to `BROKEN`.** Only the major level
can be broken. A stale minor anchor widens to its unit and says re-read,
because `BROKEN` means *go edit the ledger* and that is the bookkeeping this
removes. **A row whose anchor a change removes is `REMOVED`, not re-pointed**
— its claim went with the code, and the new claim is a new row.

**A change writes a fragment, never the shared file.** Two files used to take
an append from every branch, and both cost a conflict at the worst moment,
after the broad gate has run, which forces it to run again. No two work items
share an id, so no two branches share a fragment. The checker reads
`seal/ledger.md` and the `seal/ledger/*.md` glob alike, and a row is a
content anchor, so the release that folds a fragment into the shared file
changes nothing either one measures.

**Appended is the word, and a removal is not one.** A branch that removes
code an existing shared-file row cites must touch that file to leave the
ledger true: the row is removed there, and the new claim goes in the branch's
own fragment.

<!-- specs/1788761915-a-record-states-what-nothing-reads -->
**A work item whose ledger fragment still exists has not shipped.** The fold
removes the fragment at the release, so the fragment's presence is the
boundary — and it is the one a check over unshipped work items uses, rather
than a date or a branch name. A released work item's records are records of a
moment, and holding them to a rule written later is holding them to nobody's
rule.

## What the checker refuses, and what it says while refusing

<!-- specs/1789296100-the-seal-and-ci-read-one-ledger-differently -->
**One ledger, two readings, and the lenient one says so.** The checker's
default reading is lenient and the broad gate runs it with `--strict`. A run
whose answer is exit 1 — and only then — says that the strict reading would
refuse this tree, so every reader gets it: both wrappers, the CI job, and a
bare invocation of the script. A tool whose two callers disagree about the
verdict, and which tells neither caller so, is a tool that reports clean to
whoever asked first.

<!-- specs/1788686494-the-printed-ledger-name-collapses-through-relpath -->
**A name a person reads is the file that was actually opened.** Turning a
ledger path into a display name goes through one helper, at every site that
prints one. A relative path computed against the wrong base collapses to
something that names no file, and a header naming a file nobody read is worse
than no header: the reader takes the rows below it for that file's rows.

**What a narrowed read did not look at is part of its answer.** A scoped read
is right for writing — it keeps a re-verify off a row somebody else owns —
and a silent partial answer is not right for reading. The checker names what
it skipped, because guidance binds a session that reads the guidance and a
session that narrows on its own initiative still gets an answer it will
believe.

## A correction a merge dropped

<!-- specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections -->
**When the shared ledger conflicts, resolve it hunk by hunk and read both
sides.** Never *ours* and never *theirs*. A whole-file choice is wrong by
construction once both branches have been correcting: the measured instance
resolved two hunks in opposite directions, because each side was the superset
in one of them, and taking a side reverted three corrections that had each
turned a false claim true.

**Nothing downstream can see that, which is why the reading is a person's.**
A row reverted to a superseded state is byte-identical to a row nobody
touched. There is no marker on it, and the hash the checker reads is correct
for the restored text.

So a second check reads the markers instead. For every merge commit in a
range, a `Corrected <date>` or `Re-read <date>` marker present in **either
parent's** ledger text and absent from the result, **while the row carrying
it survives**, is reported with the file, the marker and the parent it came
from. Row survival is the one distinction that check exists to draw: a marker
that vanishes with its whole row is a removal and is correct; a marker that
vanishes while its row stands is the defect. It reports the loss after the
fact and cannot prevent it.

It reads the shared file and every fragment, because a fragment becomes part
of the shared file at the release and a check that skipped fragments would go
blind exactly while the rows are being written.

<!-- specs/1789996780-the-census-and-the-tie-that-nothing-holds -->
**A bound over the corpus is stated with its instrument and the moment it was
taken.** A case that asserts a bound covers every candidate site takes its own
census over the real corpus, says how the number was taken, and says what it
does when the corpus grows past it — the property, never a spelling and never
a bare number. A sentence stating a count with no instrument beside it is a
claim nobody can re-derive, and two such sentences in one module were
arithmetically false about the module's own corpus.

**Where a merge has two parents and both could be named, the tie falls to the
first.** A rule that leaves a tie unstated is a rule with a case nobody wrote.

## The unverified record, and the baseline it is read against

<!-- specs/1788873600-the-baseline-is-the-moving-pull-request-base -->
**A baseline reference is resolved once, to a merge base, and every arm reads
that commit.** A branch name is not a commit: it moves while the pull request
is open, so two arms reading it a second apart can compare against two
different trees. The report names the revision it actually compared against,
and a reference sharing no history with the head is exit 2 — a comparison
against nothing is not a comparison.

## The fold, and what tells it from a deletion

<!-- specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built -->
**A released work item's directory is folded into a policy document and then
removed, and the removal is the second half of the fold, never its own act.**
A directory removed before a document absorbed it takes the reasoning with
it, and that is the one loss nothing can undo. The command reads and groups;
the session judges and writes. Folding *only what is still true* is a
judgment about truth, so the tool writes no sentence into a policy document
and its second arm removes only what one of them already absorbed.

**The marker is the fold's record, and there is no second file.** A folded
sentence carries `<!-- specs/<work-item-id> -->` on a line of its own, and
that comment is read to know what has been folded — so nothing has to be kept
in step, and a run interrupted between writing the prose and removing the
directory picks up where it left off. The removal of a directory and a branch
deleting one are otherwise byte-identical to every reader; the marker is what
tells them apart, which is why a reader of removed work reports a fold rather
than a deletion.

<!-- specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft -->
**A marker counts only on a live line, and one function decides what live
means.** A line begins live when it begins outside a fenced block, outside an
HTML comment and outside a code span. A marker quoted inside a fence is a
description; one inside a commented-out draft is a parked one; neither
records a fold, and both used to excuse a removal nothing had absorbed. Every
reader of the fold record and of the ledger's own sections asks the same
function, so the rule cannot be spelled twice and drift.

Where markdown will not answer without a block model — a backtick run with no
partner on its own line is literal text if the paragraph ends first and a code
span if it does not — **both readings are computed and a line is live only
where both call it live.** Nothing decides where the block ends; the
disagreement is resolved toward keeping a work item's directory. The cost is
a fold reported as a deletion, which a person sees at exit 1 and can act on,
and that is the cheaper of the two mistakes.

**The fold reads the top level of `docs/` and no deeper.** A fold writes into
a flat policy directory — merge into a document that exists, create one only
for an area with none — so a marker below the top level is somebody's notes,
and a scratch file quoting one excused a removal nothing had absorbed.

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
**A released work item that wrote no `spec.md` states no rule, and it is
retired by that rule, with no marker.** Such an item was below the SDD
ladder: a release entry, a renumbering, a CI repair, a pull request's record.
Those are records of a moment, and a moment states nothing to fold — which is
also why nothing has to be carried out of one, so `settle` prints these under
their own heading and `settle --retire` removes them without writing a marker
into `docs/` (#517). **One condition narrows it: nothing in the record may
still be open.** An open `## Not verified` row or an open `evidence-todo.md`
row is a claim with an answerer rather than a rule, so a directory holding one
is kept and named with its rows, and closing each row or re-homing it is what
lets the next retirement take the directory. That condition is a judgment the
repository owner may overturn. An ungrouped item that did write a `spec.md` is
folded where that spec's rule belongs. One more reason keeps a directory: **a permanent
ledger row anchored inside it**, which holds the directory until the row is
answered — so a work item with a row anchored in its `rounds/` stays on disk,
and the fold does not remove it to tidy the list. Keeping the directory rather
than removing the row is a default, and the repository owner is who can trade
it the other way: remove the row, carry its claim into the prose it evidences,
and let the next `settle --retire` take the directory. For `1788184145`, the
one directory held this way when the guard below shipped, that trade was
taken (#517): the row was removed, and its claim stands in
`docs/review-chain-spec.md` §*Two records, and what each of them says*.

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
**A retirement would break every ledger row anchored inside the directory it
removes, so the retirement refuses that directory first.** An anchor into a
work item's `spec.md` or its round records is a file path like any other, and
after a removal the checker reports it broken. So `settle` reads every live
row of `seal/ledger.md` and of every `seal/ledger/*.md` — the rows above the
first section marker included — and names each one anchored inside a released
directory, and `settle --retire` keeps every directory such a row anchors
into, removes the rest, and exits 1 naming each row (#511). It says per row
what `CLAUDE.md` requires: a row whose every anchor goes is REMOVED, never
re-pointed, and its claim is written anew where a work item still holds it; a
row that keeps a live anchor beside the dead one loses only the dead one, and
whether it should be removed instead is the repository owner's question,
recorded against the ledger row that first met it. The command names the rows
and edits none of them, because which row goes is a judgment about a claim.

**A fold is not a work item, and it adds nothing to the ledger.** It opens
no directory under `seal/specs/`, so it has no fragment to append under, and
`seal/ledger.md` changes on a fold branch only by removal and re-verification:
a row the guard named REMOVED goes, a row it named narrow loses its dead
anchor, and a row whose anchored unit the fold's own prose edited is re-read
and re-verified. Its commits are waived one command at a time and its
judgment is reviewed at its pull request (#517). What it leaves already has a
home — the marker, the pull request, git history — so it keeps no log of its
own.

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
**A population floor over the records is replaced, never lowered.** A check
asserting that a sweep of `seal/specs/` read *enough* — `len(records) > 200` —
is answering *did the walk read anything* with a literal that stops being true
the moment the corpus shrinks, and a fold shrinks it by design. The repair
compares the walk against an independent listing of the same tree —
`git ls-tree HEAD` — which holds at any size, and a property the real corpus no
longer exercises moves to a record built in `tmp_path`. A repair is green
before the fold and after it; one green only once the directories are gone is
a lowering. `skills/settle/SKILL.md` §3 gives the three answers.

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
**A fold marker on a line of its own is exempt from the wrap limit.** The
marker is matched whole, so wrapping a long work item id stops it being a fold
record, and `tests/test_docs_line_wrap.py` skips a line that is exactly one
marker rather than asking a document to choose between the two. The chain
checker's reading of a retired declaration is `docs/review-chain-spec.md`'s,
under *The declaration, and where the check went instead*.
