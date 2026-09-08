# 1788826000-a-stamp-names-content-not-a-commit — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `cbdd66e` (planted red) · `e2076cc` (hardened, and what closed the phase) |
| Ran by | `smith on unknown — the spawn prompt named the agent and not the model` |

## What this phase was asked

Replace the ancestry case with one that guards the new form, and see it red
against the unmigrated corpus before any stamp moves.

## What this phase found

**Four corpus cases went red at `cbdd66e`, before the corpus moved**, naming
every one of the 20 riders: every rider carries a stamp, no stamp names a
commit, every stamp resolves and reproduces its hash, and the check reaches
git for nothing.

**Two of the nine fixture cases were verifying nothing, and only mutation
found it.** This is the phase's real finding, and both failures are worth
carrying forward because neither is visible by reading.

- *A second rider in a unit does not drift the first* built its fixture by
  inserting the second rider **directly after** the first. The two merged into
  one comment run, so there was only ever one block, and the case passed with
  the exclusion rule narrowed to `blocks[:1]` — precisely the thing it claims
  to pin. The rider now goes below the code between them, and the case asserts
  its own fixture has two blocks before it asserts anything else.
- *The check asks git for nothing* used a tripwire `git` that returned a
  failing exit code and nothing read it. `subprocess.run` with
  `capture_output` does not raise, so a `git status` added to the check path
  left the exit code untouched and the case stayed green. The tripwire now
  **records** being called and the case reads the record.

The general shape: **a tripwire whose signal the code under test is free to
ignore is not a tripwire.** The third survivor was a bad mutation rather than
a bad case — loosening the stamp regex cannot unstamp a rider that is
stamped — and deleting a real stamp turns it red.

All eleven cases red under a mutation aimed at each, 17 green unmutated, and
the tree restored from bytes held in memory rather than from HEAD.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_every_rider_stamp_names_a_commit_this_branch_can_reach` — NAME NOT IN TREE | replaced by `test_no_rider_stamp_names_a_commit` and `test_every_rider_stamp_resolves_and_reproduces_its_hash`, in the same file |
| `is_shallow` and the shallow-clone assertion — NAME NOT IN TREE | nowhere — the fact it protected is gone with it. A check that makes no git call cannot be silenced by clone depth, and `test_the_check_asks_git_for_nothing` is what now says so. `tests/test_ci_gives_the_checks_what_they_need.py` still pins `fetch-depth: 0`, for a reason phase 6 re-measured |
| `test_every_rider_carries_the_date_and_sha_it_was_verified_at` — NAME NOT IN TREE | replaced by `test_every_rider_carries_a_verification_stamp`, in the same file |
| `STAMP` — NAME NOT IN TREE | replaced by `NEW_STAMP` in `.github/scripts/rider_check.py`, which the test file imports rather than restating |

<!-- The last two rows were added in round 1's fix pass (finding 8). An AST
comparison of `tests/test_a_rider_reaches_its_file.py` across this phase's
range removes four units and the table named two. Both of the missing ones
have live replacements, so nothing was lost; the table was what was
incomplete, and an incomplete removes table is exactly what the records arm
of `evidence-check` exists to catch. -->
