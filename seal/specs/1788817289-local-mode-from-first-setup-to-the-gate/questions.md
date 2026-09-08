# 1788817289-local-mode-from-first-setup-to-the-gate — questions for the planner

<!-- The batch was collected before the first edit. Both rows below were
answered in it, in the same call as the routing question; the third arrived
during the build and is a decision this work deliberately did not take. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Where does an untracked declaration land — does `chain_check` report *declared* in local mode? | **Say which root was searched** — the verdict does not move, and a defect in it is a sentence rather than a wrong pass · **Read the untracked file** — removes the friction and teaches a CI-facing check to trust what CI cannot see | say which root was searched | ✅ answered in the opening batch: say which root |
| Q2 | Does `seal/config.md` become the opt-in signal, replacing the directory? | **No** — the gate and the preset pointer together · **Yes** — reopens `docs/one-root-by-lifetime.md` §*The opt-in signal is the root itself* | no | ✅ answered in the opening batch: no |
| Q3 | Should `--worktree` read routing declarations from the working tree, so `round_record.py`'s own chain-check reports *declared* in local mode? | **Yes** — removes the residual friction; the local run then asserts a chain verdict CI can never reproduce, which is a second guarantee to keep true · **No** — the notice from Q1 is the whole answer, and local mode's documented trade is that CI checks nothing | no — this work took the notice only | ⬜ raised as a follow-up rather than decided here; answerer: the repository owner |

Q3 is written into `seal/follow-up.md` as well, because a row that lives only
in a work item's `questions.md` is not schedulable after the work item closes.
