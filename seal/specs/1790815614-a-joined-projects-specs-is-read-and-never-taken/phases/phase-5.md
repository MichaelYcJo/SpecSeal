# 1790815614-a-joined-projects-specs-is-read-and-never-taken — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 8bbf70dc |
| Ran by | specseal:smith on claude-opus-5-5 — set by the orchestrator, which spawned it with that model and did not name it in the prompt |

## What this phase was asked

One bullet in `agents/framer.md` §*What you read*, one sentence in
`agents/smith.md` §Phases step 1, one in `agents/warden.md` §Role for stage 1
(a `spec.md` citation into a reference root is opened like any other
coordinate), one paragraph in `skills/settle/SKILL.md` §2, one sentence after
the roots table in `skills/implement/SKILL.md` §*Document layout*, and
`templates/seal-README.md:51` and `seal/README.md:51` reworded to *nothing
writes*. Each points at `templates/config.md` §*Reference specs* rather than
restating the grammar. C2 red with the sentence absent.

## What this phase found

**An apostrophe moved the commit gate's reading of two files.** The first
drafts of the smith's and the implement skill's sentences said *a project's
own `specs/`*. Each file carries the waiver example — the token in front of
a commit — below that sentence, and a heredoc patch of either is read by the
gate as shell, so one more apostrophe flipped the quote state: measured on
`agents/smith.md`, `commit_invocations` over the waiver line with everything
above it went from one invocation to none, and `_hides_a_commit` over the
file from True to False; `skills/implement/SKILL.md` flipped the same way.
Both sentences were reworded with no apostrophe (*a `specs/` the project
kept before the plugin*), and every file the branch changed was measured
against `cd24f516` with no flip left. The mechanism is already named in
`tests/test_edits_go_through_the_edit_tool.py` for the contract and the
warden; nothing pins these two files, and that case says on purpose that
`agents/smith.md`'s tripping is a defect not to be pinned as a requirement.
This branch restores the base's reading and changes nothing about which
reading is right.

**The smith's rider was first re-stamped on the false reading.** One
command ran the measurement and the re-stamp together, so the stamp landed
before the numbers were read. The numbers said the rider's claim had become
false; the sentence was reworded, the numbers re-measured (one, one, True —
the rider's own), and the rider re-stamped again on them. Only the second
stamp is in any commit.

**The rider's pointer is stale, and not by this branch.** It names
`seal/specs/1788873640-…/questions.md` Q4 as where its open question lives;
that directory is not in the tree. What this phase measured is direct
evidence for the question it asks — why a reading of this file once gave
zero: an odd number of apostrophes above the example is enough. Handed back
for whoever owns the rider; nothing here edits it beyond its stamp.

**A pin that matched two words apart was weak.** C2 first asserted
`never` and `writ` anywhere in the paragraph, and *you may write there, and
never move* passed it. It now matches `never writ` as one phrase; ten
mutations across the seven files, ten red.

**`KEEP` needed no change.** The seal README's reworded line still carries
`` `.specseal/` or a top-level `specs/` ``, the key phase 2 noted, so the
entry stays in use.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The seal README's "Nothing reads `.specseal/` or a top-level `specs/` any more" | `templates/seal-README.md` and `seal/README.md`, reworded to *nothing writes*; row C2 of `seal/ledger/1790815614-….md` |
