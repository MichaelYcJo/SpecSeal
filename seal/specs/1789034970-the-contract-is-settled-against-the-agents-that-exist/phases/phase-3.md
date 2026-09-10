# 1789034970-the-contract-is-settled-against-the-agents-that-exist — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `2821f6d` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

<!-- Two commits, because the documents had to land before the cases could be
seen red against them: `841ef4a` is the document edits, `2821f6d` the cases and
the ledger. The Status cell names the second, which is the phase's head. -->

## What this phase was asked

`plan.md`'s row 3. `agents/sealer.md` loses §*§2 as it stands, and #120* and
re-points §*The one write, and why it is yours* at §6 as rewritten;
`agents/warden.md:199` stops saying *§6's two exceptions*;
`skills/code-review/orchestration.md:62` stops saying *§2 reserves the broad
gate for you*; and
`tests/test_the_seal_is_taken_once_by_the_sealer.py:1626` is rewritten to pin
that the window is CLOSED — not deleted, because a deleted case is a paragraph
that can come back.

## What this phase found

**Deleting the window paragraph is not, on its own, correct.** The frame asks
for a deletion and a re-pointing. But phase 1's §2 now says the assignment
lives in the definition rather than in the contract — *One definition in this
plugin does hand them over — the sealer's* — and after a bare deletion
`agents/sealer.md` would not have contained that assignment anywhere. Its
frontmatter and its procedure describe the run; nothing in it said *this act
is mine under §2*. §2's pointer would have named a file that does not answer,
which is #30's opening one release later. So the deleted section is replaced
by §*The one run, and why it is yours*, and `spawned for exactly that` — a
phrase carried over from the paragraph that went — is what the case holds it
to. **This is the one thing built here that the frame did not settle.**

**Both cases were renamed, and one of them passed against both trees.**
`test_the_sealer_states_the_contradiction_and_the_ticket_that_settles_it` <!-- NAME NOT IN TREE -->
became `test_the_window_the_sealer_shipped_under_is_closed`, assertions
inverted, red at `8204533`.
`test_the_sealer_names_its_one_write_as_its_own_exception` <!-- NAME NOT IN TREE -->
became `test_the_sealer_names_the_one_write_its_definition_is_allowed`,
assertions
untouched: §6 stopped calling the mechanism an exception and started calling it
the rule, so the grounds moved and nothing the case checks did. It passed
against both trees, and it is recorded that way rather than counted as a case
seen red. Contract §15 is about a new case; this is a rename.

**A rename is a REMOVED anchor, and two of them were cited.** Row S8 of
`seal/ledger/1789002694-…md` cited both case names and the deleted section.
Three of its four coordinates went BROKEN at once, which is what a removal
looks like — so S8 was removed there and R1 of this work item's fragment
carries the successor claim, per the repository's own rule. The fragment's
header note was updated too: it said *Eleven rows* and the count is now ten.

**Two records outside this work item name a unit the tree no longer has.**
`evidence-check`'s `records` arm caught
`seal/specs/1789002694-…/phases/phase-3.md:134` and, after the rename, this
work item's own `spec.md:111` and `plan.md:57`. All three are records of what
was true when written, so each takes `<!-- NAME NOT IN TREE -->` on the line
rather than being rewritten to name the new case. `evidence-check .` then
reads `1111 ok · 0 drifted · 0 broken`, exit 0.

**A rewritten section can tie the duplication margin without failing.** The
first draft of §*The one run, and why it is yours* quoted §2's list verbatim —
*the full suite, the repository-wide lint, the typecheck* — which is a 10-word
run and made `agents/sealer.md` a second file sitting exactly at
`LONGEST_KEPT_APPLICATION`. `test_the_window_sits_between_what_was_measured`
asserts `<=`, so it was green and the margin had quietly halved. Reworded to
*suite, lint and typecheck together*, and the measured table is back to the
base: 10 (`smith.md`/§8), 9 (`warden.md`/§6), 8 (`smith.md`/§3).

**Two pins were added that the frame did not ask for**, both under §14 —
`agents/warden.md`'s two named writes and `orchestration.md`'s re-derived
grounds. Neither sentence had a case, and both are rule-carrying prose a
person reads and acts on. They went into the modules that already read those
files rather than into a new one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `agents/sealer.md` §*§2 as it stands, and #120*, the whole section | Nowhere as a contradiction — it does not exist any more. Its positive half, that the sealer runs the broad gate once spawned for exactly that, lands in the new §*The one run, and why it is yours* in the same file |
| The name `test_the_sealer_states_the_contradiction_and_the_ticket_that_settles_it` <!-- NAME NOT IN TREE --> | `test_the_window_the_sealer_shipped_under_is_closed`, same module. Three records that name the old one carry `<!-- NAME NOT IN TREE -->` |
| The name `test_the_sealer_names_its_one_write_as_its_own_exception` <!-- NAME NOT IN TREE --> | `test_the_sealer_names_the_one_write_its_definition_is_allowed`, same module, same assertions |
| Row S8 of `seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md` | R1 of `seal/ledger/1789034970-the-contract-is-settled-against-the-agents-that-exist.md`, and a note in the fragment it left saying which work item removed it and why |
| `agents/warden.md`'s phrase *§6's two exceptions*, and *the whole of the second exception* | Nowhere — §6 carves none. The two writes are named in the same bullet, now with a bound (`there is no third`) that the word `exceptions` used to carry, pinned by `test_the_warden_counts_its_writes_rather_than_its_exceptions` |
| `skills/code-review/orchestration.md`'s grounds *§2 reserves the broad gate for you* | The same paragraph, re-derived: the gate goes to whichever definition assigns it and no reviewer's does. Pinned by `test_the_reason_no_round_can_run_it_survives_the_rewrite_of_s2` |
