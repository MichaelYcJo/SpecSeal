# 1788789329-a-git-call-that-fails-reads-as-no-remote — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 4a6e7d4 |
| Ran by | unknown — the spawn prompt named no model, and the template forbids a segment sourcing this from its own idea of what it is. The orchestrator that spawned this segment is the party that can fill it |

## What this phase was asked

Deliver the receiving machine's half. `:947` distinguishes the two facts and
an unreadable remote **refuses**, with a message naming the git failure's own
cause rather than a generic sentence; the escape is a new flag, argued in
`spec.md`, so `--allow-other-repo` keeps meaning only what it says; `:948`'s
side handles an absent manifest field. The owner answered *refuse* before the
first edit and left the flag's name and message to this session.

`:1476`'s sentence moved into this phase from phase 3 — see `plan.md`.

## What this phase found

**The ticket's `:953` is the fifth call site, and removing it is what closes
the class rather than shrinking it.** The refusal for another repository asked
git a second time for the URL it had just read and printed whatever that call
answered, so a failure between the two put a blank where the message promises
this clone's URL — this ticket's own failure inside the message reporting it.
Reading once and printing what was compared deletes the call outright, and it
is the only one of the four that goes away rather than changing shape.

**After this phase `git()` has exactly one call site left**, `other_worktrees`
at `:1599`, which is the member of the class concluded safe. The
re-enumeration is the same grep the spec ran — nine hits at the base, five
call sites; one call site now — with
`grep -nE '=\s*git\s*$|=\s*git\s*[,)]'` as the cross-check for a call reached
through a reference, which returns nothing. **The fix pass added no new
member of the class**: `git_asked`, `remote_url` and `head_sha` all return
`(value, why)`, so a caller cannot read a value as a fact without also being
handed the reason it is not one. The class is structurally empty for them
rather than empty by inspection, which is the difference between an
enumeration that holds and one that has to be re-run after every edit.

**The refusal gathers reasons into a list rather than picking one**, which
matches `refusals` and `unsafe` elsewhere in the same file. Both sides can be
unanswerable at once — this clone's git failed AND the zip records no remote —
and naming only the first would send a person to fix a machine that is not the
only problem.

**A zip missing the `remote` key refuses, and that is an assumption worth
stating.** An older build always wrote the key, so a zip without it either
came from a build that could not look or was not written by `seal export` at
all. Neither answers the question, and `questions.md` A2 records the reasoning:
the ticket's instruction to make the field absent has no purpose unless the
receiving machine acts on the absence.

**Eleven mutations, all killed.** One unit at a time, restored from bytes held
in the driver rather than from HEAD — the tree was uncommitted, and `git
checkout --` here would have taken every phase-2 and phase-3 edit with it.
`tests/__pycache__` cleared between mutations. The two cases that were green
when first written — a clone with no remote, and a zip recording `""` — were
seen red by the `remote_url` and manifest mutations, which is the only way a
case pinning existing behaviour can be shown to bite.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The second `git()` call inside the other-repository refusal message (`:953` at the base commit) | Nowhere — the fact it re-read is the one already read for the comparison, and `test_the_refusal_prints_the_url_it_compared` pins that it is asked once |
| `git()`'s last four call sites that read `""` as a fact | `remote_url` and `head_sha`, cited by the ledger fragment's R1. `other_worktrees` keeps the one call site that is right to read it that way, and its docstring now says so |
