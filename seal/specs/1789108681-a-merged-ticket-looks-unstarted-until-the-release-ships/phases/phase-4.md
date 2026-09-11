# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — phase 4

<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `db029b1` |
| Ran by | specseal:smith on Opus 5 — the model the orchestrator chose at the spawn, filled in by the orchestrating session as the template requires |

## What this phase was asked

The three documents: `docs/release-checklist.md` step 0's new line and §6's
corrected sentence, and `docs/issues-and-milestones.md` §*Nothing automated
reads a milestone* rewritten. Verified by S9, S10, S11 and by
`tests/test_one_word_one_meaning.py` and `tests/test_docs_line_wrap.py`.

## What this phase found

**The section's heading was the claim, so the heading changed too.**
*Nothing automated reads a milestone* is now *One thing reads a milestone, and
it can stop a release*. Rewriting the body under a heading that asserts the
opposite would have left the one line a reader skimming for the answer
actually sees still saying the false thing.

**Nothing live cites the old heading, and what does cite it must not be
touched.** Executed: `grep -rn "Nothing automated reads a milestone" docs/
skills/ agents/` returns nothing (exit 1), which is S10's own verification
method. The phrase survives in three places, all of them earlier work items'
`seal/specs/*/spec.md` and `overview.md` — records of a moment, which state
what was true when they were written and are not rewritten, the same rule
that governs a `# RIDER:` stamp and a round record. `survivor_check.py
--range origin/release/v0.11.1...HEAD` agrees: 874 files examined against 8
removed sentences, **no removed wording still standing**, so no
`survivors.md` row is owed.

**Q9's default did not survive reading the section it is about.** The default
was *the milestone document alone; `branch-and-release.md` untouched*. Every
sentence in §*So a workflow reads the keywords instead* is still true of the
closer. What stops being true is the conclusion the section as a whole
invites — that a closing keyword written into a release base does nothing
until `main` moves — because the same keyword is now read on the
release-branch push to write the label. One paragraph was added and no
sentence was edited. `spec.md` §*Out* excludes this file, and Q9 is what
authorises the exception: the SDD hands this judgment to phase 4, and the
added paragraph is a statement about a workflow rather than about the
sequence, which is the line the Out entry itself draws.

**The correction in §6 says that the paragraph used to say the opposite.**
A reader who acted on *the close-issues workflow runs on the tag and closes
every issue the changelog section names* has no other way to learn they were
wrong; a silent replacement repairs the document and not the reader. S9's
verification method — `grep -n "on the tag" docs/release-checklist.md`
returns nothing — is met by the false clause being gone rather than by being
worded around it: the replacement states the trigger and the input
positively and never mentions a tag.

**Step 0's new box is first in the list, and the placement is the point.**
The act it asks for is release planning, and the gate that enforces it fires
at step 5 — after the preparation commit, after the fragments are gathered,
after the broad gate has run on the preparation tree. Anywhere later in the
checklist and the box is ticked after the cost has already been paid.

**Both edited documents are in `tests/test_docs_line_wrap.py`'s `COVERED` at
88 columns**, which `plan.md` names, and both new sections were wrapped from
their first line. Executed: that module plus `test_one_word_one_meaning.py`,
`test_release_hygiene.py`, `test_no_real_identifiers.py`,
`test_the_rules_have_one_owner.py` and
`test_a_question_says_who_can_answer_it.py` — 121 passed, exit 0. Every
version in the new prose is `X.Y.Z`, so S11 holds.

**The new prose claims no issue number.** Executed:
`issue_claims_check.py` over the whole of `docs/branch-and-release.md` reports
`claimed: none` and `mentioned only: … #359` — the paragraph names the ticket
without a closing keyword in front of it, which is what keeps a document that
quotes closing keywords from closing something.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/issues-and-milestones.md` §*Nothing automated reads a milestone* — the heading and its claim | §*One thing reads a milestone, and it can stop a release* in the same file states what now reads one and what a wrong one costs. Nothing else needed it: no live document cited the heading |
| `docs/release-checklist.md` §6's sentence *"The close-issues workflow runs on the tag and closes every issue the changelog section names"* | The same section, which now states the trigger (`main` moving) and the input (pull request bodies) the tree actually has, and says the paragraph used to say the opposite |
