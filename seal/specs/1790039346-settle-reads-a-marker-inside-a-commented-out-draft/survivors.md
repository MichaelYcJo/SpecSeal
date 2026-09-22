# Wording this branch removed that still stands elsewhere

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

`survivor-check --range origin/release/v0.13.0...HEAD` reports three places,
and round 3's fix range adds one more. Each was opened and judged; none is a
claim this branch made false.

| Path | Quote | Grounds |
|---|---|---|
| `seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md:7` | a span quoting a COMPLETE comment holds an opener, so blanking it whole took the quoted closer with it and a real section marker below was still lost | R5's evidence cell, and the sentence is dated and already superseded inside its own file. It records what round 2's fix pass found and did, which was true then and is still true of that formulation; round 3 narrowed *which* openers are blanked and R8 carries that with its own date. The sweep pairs it with the body comment round 3 rewrote, on the shared phrases `complete comment holds` and `blanking it whole took`. Rewriting the earlier note would delete the record of what was true at round 2, which is the one thing a re-read chain exists to keep — the same grounds as the parent-fragment row below. The one place this wording was a live claim rather than history, `blank_code_spans`'s docstring, was corrected in the same commit rather than exempted (NAME NOT IN TREE) |
| `skills/verify/scripts/unverified_check.py:195` | `return [kept for _, kept in comment_scan(lines)]` | This is the design, not a survivor. It is the one view left over the single scan, which `test_strip_comments_reads_through_the_one_comment_scanner` pins — round 4 replaced `live_lines` with a scan carrying its own comment state, so the second view and the case named for the pair are both gone, and what still deserves pinning is that this reader keeps no private copy of the walk — the shape #487 is open about having in two files, deliberately kept in one here. The sweep pairs it with that case's docstring, which this branch reworded, on the shared n-grams `comment scan lines` and the comprehension form. An n-gram sweep cannot tell an implementation it was told to keep from a sentence that was removed |
| `skills/verify/scripts/unverified_check.py:217` | `return [began for began, _ in comment_scan(lines)]` | The other view of the same scan, same grounds. Round 1's finding 4 asked for this spelling to be unified with its sibling and was answered with grounds in that round's record: asked of the phase 2 stub, a filter form answers `[]`, which is byte-identical to a `live_lines` that yields nothing, and that weakens the very pin round 3 finding 4 asked for |
| `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:5` | The file carries no fence today, so no figure above moves, and the reader is the `blank_fences` this module already loads rather than a third copy of the rule. | The sentence is dated and already superseded inside its own cell. A ledger row's evidence cell is an append-only chain of re-reads, each marked with when it happened; this one carries **Re-read 2026-09-22 in round 2's fix pass**, and the sentence immediately after it is **Re-read 2026-09-22 in #489's build (work item `1790039346`)**, which states that `coordinates` now reads the comment half through the same `live_lines`. Rewriting the earlier note would delete the record of what was true at the parent's round 2, which is the one thing a re-read chain exists to keep |

## A range that deletes a shipped section takes one row

The range is spelled the way CI passes it and `survivor_check.py` recommends,
and the second anchor is this directory: a range row holds only over a range
that touches its own work item, so it cannot excuse a later branch cut from
the same base.

`CLAUDE.md` §*Once the fixes are committed, ask what they left standing* names
this shape: a range that removes a shipped section reports every durable copy
of every sentence it removed, all correct as reports and none of them a
defect. Round 4's fix range deleted two shipped functions and their docstrings
— `blank_code_spans` and `opens_outside_a_comment`, about nine thousand (NAME NOT IN TREE)
characters — so 168 sentences left the tree at once and 84 places still carry
wording from them.

**Six of the 84 were live claims and were corrected in the range rather than
exempted here**: `overview.md`'s purpose paragraph and its round-3 divergence
row, this work item's `changelog.md`, two case docstrings in
`tests/test_settle_reads_before_it_removes.py` and one in
`tests/test_unverified_rows_close.py`, each of which described the three-pass
composition as the shipped design. The row below covers the remainder.

| Range | Grounds |
|---|---|
| `origin/release/v0.13.0...HEAD` | The remaining 78 places are dated records of what each round did — `plan.md`, `spec.md`, `questions.md`, `phases/phase-2.md` and `phases/phase-3.md` carry the correction chain rounds 1 to 3 wrote, and rewriting any of them would delete what was true at that round, which is the one thing a re-read chain exists to keep. The rest are other work items' ledger rows matching on generic phrases (`seal/ledger.md`, three), the parent's own dated re-read chain (five), this fragment's dated notes (three), `agents/warden.md`'s unrelated sentence about fences in a review report (one), and this file's own exemption quotes (two). Where the removed wording was a live claim about the shipped design rather than a record of a past round, it was corrected in the same range — the six named above |
