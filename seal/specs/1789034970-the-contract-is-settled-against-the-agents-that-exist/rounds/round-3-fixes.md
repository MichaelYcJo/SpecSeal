# Round 3's close — the contract is settled against the agents that exist

Range `ce0f9fe..ce0f9fe`, empty. **This round wrote no fixes, and that is the run's designed end
rather than an omission.** `chain_check` capped the run at this record — round 1
met the floor, round 2 closed on a fix, and at most one later record may close
on a fix — so every finding still open becomes an issue and its verdict reads
`deferred #N`. Read by `round_record.py close`.

The fixes for all three WERE written and verified, on the branch
`backup/120-before-rewrite` at `3b228f4` and `8fd2f59`, before the cap was
read. They were reverted rather than kept: a run that keeps fixing past its
bound is the state the bound exists to end, and the fixes are carried into the
issues below in full so that nothing is re-derived.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | deferred #339 | The join's guard, in both directions. The verified fix and the pattern it comes from are in the issue |
| 2 | deferred #340 | The protocol's §14 half. One paragraph, written and verified; the anchored-row trap is named in the issue |
| 3 | deferred #344 | A fix table naming a moving range — third instance of the class in this work item, so the issue takes the class rather than the line |
