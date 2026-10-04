# 1791076831-a-here-document-body-is-data-to-the-commit-gate — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 2d223ab4 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The words say it. Rewrite the two `docs/commit-review-gate-spec.md`
paragraphs (the one opening **A file edit goes through the `Edit` tool** and
the one opening **Two readings that prompted that run stay as they are**), and
the **What stays unread** paragraph if it needs a sentence; `skills/agent-
contract/SKILL.md` §9's "reads a heredoc body as shell, on purpose". Name the
new cases on `Enforced by:` lines. Write the changelog fragment per
`docs/the-record-layout.md`, and the ledger re-reads through `evidence-check
--reverify --into` this work item's fragment, because the ledger is frozen.

## What this phase found

**The rule got a paragraph of its own.** Rewriting the Edit-tool paragraph in
place would have buried a gate rule inside a paragraph about edits, so that
paragraph now ends where it did, less the sentence that left the trade to the
owner, and points at **A here-document body nothing can run is data**, which
states the rule, the boundary and the failure direction, with its own
`Enforced by:` line and work-item marker.

**Three released rows no longer held, and are corrected rather than
re-read.** `evidence-check --reverify --into` wrote 18 `Re-read ·` rows for
the released rows whose coordinates this range moved. Three claims had gone
with the code: 0.16.0's E3 (all four measured shapes stop), E7 (nothing the
base stops reads silent) and E9 (#665's reading stays). Each is now a
`Corrected ·` row saying what holds. I10's re-read says its generated corpus
was a deleted probe and was not run again. M4's and K4's say their claims are
about their own work items' diffs. H1–H4 are this work item's own rows.

**One drift in the tree is not this branch's.** `seal/releases/0.15.1.md`'s
L1 cites `tests/test_a_record_precedes_the_fixes_it_commissions.py#
test_the_declared_limit_names_what_escapes_with_the_words_unchanged`, which
`f19e2762` (#752) changed on the base before this branch was cut. It is
DRIFTED on every branch of `release/v0.18.1` and would make the strict broad
gate refuse the seal. It was not re-read here, because it belongs to no row
this work moved.

**`agents/smith.md` was left as it is.** Its §9 paragraph and the RIDER on its
waiver example say a patch to that paragraph is a shape the gate reads a
commit out of. That still holds for every patch outside R (an unquoted
delimiter, a shell fed the body, a sink beside a `git`), and the RIDER's
stamps are measurements this work did not repeat.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The policy sentence "Skipping a body that is only being written to a file would reopen #75, and that trade is the repository owner's to make." | `docs/commit-review-gate-spec.md`, the paragraph opening **A here-document body nothing can run is data**, which records the owner's answer |
