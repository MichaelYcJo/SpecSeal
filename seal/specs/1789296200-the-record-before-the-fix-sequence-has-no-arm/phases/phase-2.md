# 1789296200-the-record-before-the-fix-sequence-has-no-arm — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `394a49f` |
| Ran by | specseal:smith on claude-opus-5[1m] — the spawn prompt named no model; the segment's own harness line is the source |

## What this phase was asked

Make `round_record.py new` observe whether the resolved `--target` is the
branch's HEAD, and say so in phase 1's verdict. The message names the commits
between, both meanings — the fix pass already ran · HEAD moved mid-review — and
what to do about each. `--target` still resolves as today, and the ordinary
equal case prints nothing new. Verified by A2 and A1 in a new case module, each
seen red first: by making the observation fire unconditionally (A1 goes red) and
by reverting the observation entirely (A2 goes red).

## What this phase found

### What was built

Two functions in `skills/code-review/scripts/round_record.py`, and three lines
in `new` that call them. `head_moved(root, target)` returns
`(reviewed, head, [subjects])` or `None`; `head_moved_line` builds the text.
The line prints beside `round-record: wrote`, because it is a fact about the
record just written and about the `--target` it was written from — the
reach-back and the bound below it are about other records.

`tests/test_new_says_when_head_is_not_the_target.py`, six cases.

### The listing is the deliverable, not the difference

Phase 1's two hand-opened records differ because the round's own paperwork
landed between the review and the record, and the distinguishing fact in both
was the commit's **subject**: `docs: round 1's paragraph is recorded before the
round runs`. A fix pass and a round paragraph are one line apart in
`git log --format='%h %s'` and indistinguishable in a count. So the line lists
the subjects, and `test_the_line_lists_the_subjects_and_not_a_count` is what
keeps a later edit from reducing it to a number.

### `--target` is resolved for the line and not for the record

`head_moved` returns the **resolved** target rather than the string `--target`
carried. `--target` legitimately takes a revision — `reader.resolves` accepts
anything git resolves — and a line reading *the round read HEAD~1* names
nothing anybody can open a week later.

Writing that case surfaced something the phase did not go looking for and did
not take: **`build` writes `--target` into the record's `Target SHA` cell
verbatim**, so `--target HEAD~1` produces `| Target SHA | HEAD~1 |` and
`chain_check` then reports *no `| Target SHA | … |` row naming a commit*. It
was observed executing, in this phase's own red run. It is loud rather than
silent — `new` ends in the check that reports it — and resolving the cell would
change what every record contains, which `spec.md` §Data & interfaces does not
authorise. `overview.md` §Not done carries the grounds and the case's own
docstring carries the same paragraph beside the line that found it.

### What phase 3 inherits

**The message does not yet name a flag, and that is deliberate.** `plan.md`
asks the message to name *the escape*; the escape is phase 3's, and a commit
whose output names a flag that does not exist is false of itself. So this
phase's text states both readings and the repair for each — `Target SHA` holds
both commits for the mid-review reading — and phase 3 **appends** the sentence
naming its flag. Nothing phase 2's cases pin is deleted by that; they assert
presence, never the end of the text.

### §15 — what the failure looked like

Both mechanisms `plan.md` named, driven from
`scratchpad/red_phase2.py` with each substitution asserted (§9) and the source
restored from a copy taken before the first mutation, never from HEAD — the
file was uncommitted, and `git checkout --` would have taken the phase with it.

| Mutation | Result |
|---|---|
| the three calling lines in `new` deleted | **5 failed, 1 passed.** Every A2 case red; A1 green, which is the half that proves A1 is not passing on the mutation |
| `head_moved`'s `head == reviewed` arm deleted, so it fires on every call | **1 failed, 5 passed.** A1 red on `is not the branch's HEAD` appearing over `the round read e4c6a76, HEAD is e4c6a76, and 0 commits stand between them` |

Restored, `6 passed`. `tests/test_the_record_is_generated.py` — the other module
that reads `new`'s output — is `103 passed` after the change.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
