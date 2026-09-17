# 1789621028-nothing-reads-a-record-against-the-tree — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 24e62b36 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#344, in one slice: `close --range` refuses an end that is not a commit
somebody can open — SHA-shaped and resolving to itself, so `HEAD`, `@`, a
branch and a tag all refuse; `close` writes the resolved range and its commit
count into the record as a field; `templates/sdd-round.md` and
`docs/review-chain-spec.md` document it; `chain_check` re-reads it behind a
cutoff of the `STRICT_FROM` shape. Acceptance: the moving end refused with no
cell written, a pinned range writing a count equal to
`git rev-list --count <a>..<b>`, a planted record whose count disagrees at
exit 1, and the records already in the tree printing rather than failing.

## What this phase found

**The refusal reaches both ends, not only the second.** `HEAD` is the end
#344 measured, and a branch name at the start moves exactly as far — a rule
aimed at the word that happened to be reported closes the instance and not the
class (§12). Measured: with the refusal narrowed to `ref == b`, the four
start-end cases go red and the four finish-end cases stay green, which is what
that narrowing costs written out.

**The test for an end is two halves, and the second is what makes the first
true.** Seven to forty hex characters AND resolving to a commit it is a prefix
of. Hex-shape alone would accept a branch named `abcdefg`; prefix-resolution
alone has nothing to compare against for `HEAD`. One coincidence stands and is
recorded in the code rather than parsed away: a branch whose name is hex and
which happens to point at a commit starting with that name. Closing it would
mean asking git which refs exist, and the rule would then pass or fail on what
somebody else had created.

**`new` writes the row and `close` replaces it, because `close` replaces rows
and does not insert them.** `field_index` locates an existing row, so a record
`new` wrote without the row would make `close` raise. The value `new` writes
is the same pending sentence the two surface rows take —
`none — the fixes are not yet written` — for the same reason: a record is
committed before its fixes exist, so the range they were measured over does
not exist either.

**The count is derived, never typed, and that is what makes the row
checkable.** `close` runs `git rev-list --count <a>..<b>` over the two ends it
has already resolved. A reader can then check the row against the tree without
opening anything, which is the property the prose header never had.

**Thirty-nine fixture records in six modules owed the new row, and finding
them was the phase's own acceptance running.** The first full neighbourhood
run was 41 failures, every one a hand-written record under a work-item id
above the cutoff with no `Fix range`. That is the arm working: those fixtures
are records of work items begun after the rule, and the rule says they owe the
row. Six helpers gained `| Fix range | none |`, each with the reason beside it.

**`verdict_table`'s header return from phase 3 is unrelated to this phase and
did not conflict.** Two contract changes landed in one branch on the same
function family; the round record for this work item's own review will carry
both.

**The counts in the frame were corrected here rather than copied.** The
documentation this phase writes — `docs/review-chain-spec.md` §*The fix
range* — states 39 fix-table files, 15 stating a range in their first eight
lines, 8 spellings and 5 naming `HEAD`, which is what was measured at this
branch tip on 2026-09-17.

<!-- Round 1's 🟡 3, 2026-09-17: the two figures in this table that are counts over PROSE — the spellings and the `HEAD` tally — were taken with a method this record did not name, and three readers then produced three answers from it. The named command is in `docs/review-chain-spec.md` §*The fix range*; against it the figures are 12 distinct sentence forms and 5 ending `HEAD` at `56945007`, 4 at this branch's tip. The file counts, 39 and 15, reproduce under every reading. The record is left as it was written and this comment is the correction, the way `rounds/round-1.md:12` of 1789034970-… already does it. --> `spec.md` and `plan.md` say 11 spellings and 2
naming `HEAD`. Phase 3's record holds the full comparison; the divergence does
not change the decision, and writing the framed numbers into a shipped
document would have been this work item's own class one more time.

**The measurements, executed 2026-09-17.** Exit codes read from
`subprocess.run().returncode`; both scripts mutated from bytes kept in the
driver and restored from those bytes.

| Run | Exit | What it printed |
|---|---|---|
| The 15 generator cases, rule in place | **0** | 15 passed, 86 deselected |
| The `--range` refusal deleted | **1** | all 8 `test_a_range_end_that_moves_is_refused` cases failed |
| The refusal narrowed to the second end | **1** | the 4 `start-*` cases failed, the 4 `finish-*` passed |
| `close` writing a count one too high | **1** | the two count cases failed |
| The 9 reader cases, arm in place | **0** | 9 passed, 118 deselected |
| The reader's count comparison removed | **1** | `test_a_fix_range_the_tree_contradicts_is_named` failed |
| `RANGE_FROM` moved to `1` | **1** | the boundary case AND the repository-wide case failed — the failure mode `plan.md` named for this phase, reproduced |
| An absent row failing below the cutoff | **1** | the same two failed — the other failure mode `plan.md` named |
| Neighbourhood — 20 modules, every one that drives either script or reads the documents | **0** | 1001 passed, 1 skipped |
| `uvx ruff check skills/ tests/` · `ruff format --check` | **0** · **0** | |
| `chain_check.py --baseline release/v0.12.1 --root .` | **1** | one complaint, this work item's own missing round records. No existing record was named by either new arm |

**The repository's own records, read by the new arm directly**:
`test_the_records_in_this_repository_are_not_failed_by_the_new_row` walks every
`round-N.md` in the tree, asserts more than 200 were found, and asserts every
one produces a notice and no error. <!-- Corrected in round 1's fix pass,
2026-09-17: that held only while NO record carried the row. This work item's
own `round-1.md` is the first that does, so the case now asserts that a record
WITHOUT the row prints and never fails, and that the two groups account for
every record. `seal/ledger/1789621028-…md` R6 carries the corrected claim. --> That is the grandfathering pinned as a
fact about this tree rather than as a claim about the constant.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `--range`'s acceptance of any ref git can resolve | `docs/review-chain-spec.md` §*The fix range* records the narrowing, `templates/sdd-round.md` states it in the row, and `skills/code-review/orchestration.md` tells the party that types the command. A caller passing `<a>..HEAD` stops working, which is the fix |
