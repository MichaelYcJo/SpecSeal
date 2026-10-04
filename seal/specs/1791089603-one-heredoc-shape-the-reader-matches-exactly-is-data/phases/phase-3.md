# 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | fe2bcdd0 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The words: the two policy paragraphs in `docs/commit-review-gate-spec.md`
(*A file edit goes through the `Edit` tool* and *Two readings that prompted
that run stay as they are*) and contract §9 rewritten, with `Enforced by:`
lines; the changelog fragment; the ledger fragment with the re-reads. No
literal command string that passes the old or the new gate in a record or a
commit message. Before handing back, `bin/survivor-check` over the build
range and `bin/evidence-check --strict .`.

## What this phase found

**The policy statement keeps one `Enforced by:` line, extended.** The shape
went into the statement it narrows rather than a statement of its own,
because the rule it changes ("asked of every body") is that statement's
sentence. Its line now names, beside the two old targets, S1's case, both
halves of S4, #760's must-stop list and S6's agreement case. The grammar is
in prose with its slots named, and no line of it is a command.

**Contract §9 carries no `Enforced by:` line**, which `spec.md`'s S10 asks
for. The contract has none anywhere and `fold-check` reads `docs/` only, so
the line would be a pin nothing reads. §9 names the policy statement that
holds the grammar, and
`tests/test_edits_go_through_the_edit_tool.py::test_the_rule_names_the_one_heredoc_shape_it_does_not_read`
pins both carriers; it went red with the contract sentence deleted and with
the policy sentence put back to the old one (executed). `overview.md` records
the divergence.

**An apostrophe nearly put §8's waiver example in command position.** The
first draft of §9's new paragraph said "a file's terminator". The contract's
own case asks the commit reading whether the whole file hides a commit, and
an odd apostrophe flips its quote state. The sentence was rewritten without
one before it was committed.

**Three wrap slips, one cause.** Each `Edit` that ended a replacement
mid-line left the rest of the old line joined to it, and
`tests/test_docs_line_wrap.py` caught each at 97 to 105 columns. The
paragraph was rewrapped whole.

**Two more released rows moved with the policy text**, both anchored on the
document's headings: E9 (0.16.0, the policy records #662's and #665's
readings as staying) and C1 (0.18.0, the policy is three documents). Both
re-read and hold: #665's reading still stays, now with its one exception
named. The writer also wrote two rows this branch did not read, C4 and S8,
whose drift is the base's (`tests/test_release_hygiene.py`,
`templates/config.md`); both were taken back out of the fragment.

**The hand-over checks (executed).** `bin/survivor-check --range
1c67ec37..HEAD`: 12 removed sentences, none still standing. `bin/evidence-check
--strict .`: exit 2, on ten drifted rows, every one on a coordinate this
branch does not touch and that drifts on `release/v0.18.1` at `edee5ca2`;
no row of this branch's is drifted, broken or refused. The phase's narrow set
with the six hygiene modules the spawn named: 1,121 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The sentence that left skipping a written body open as the owner's trade | `docs/commit-review-gate-spec.md` §*A file edit goes through the `Edit` tool*, which now records the trade as made for one shape |
