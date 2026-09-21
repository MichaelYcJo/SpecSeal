# 1789985781-the-gates-arm-list-is-maintained-by-hand — questions for the planner

<!-- Decisions only a human can make. Rows the tree already answers are not
here; what the framing settled is listed under the table so nobody reopens
it. -->

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Where does the partition live? | a person | **(a)** in `broad_gate.py` — read at the coordinate the arms are at, and shipped to every repository that installs the plugin, including ones with no such workflow. **(b)** in the test module alone — the gate stays generic and the partition is this repository's own fact, but the gate can then say nothing about what it did not answer, which kills `spec.md` §Scope 4 and A6. **(c)** a data file beside the workflow that both read — one more file, and the honest home for a fact that is about this repository's CI | **(a)**, and A7 is the case that will say if it cannot hold: the partition is what the gate PRINTS from, and a gate that cannot say what it skipped is the defect one step smaller. If A7 goes red, the answer moves to (c) and `overview.md` carries the divergence | ⬜ |
| M1 | How many of the `release` job's thirteen steps could a gate mirror but does not? | a measurement | Phase 1 enumerates all thirteen by construction and classifies each. The answer may be one — #424's `correction-check` — or more. **The frame does not claim it is one**, and a build that assumes so repeats the error that cost the previous work item a 🔴 | the build measures it in phase 1 and records the number in `overview.md` whatever it is. Nothing waits on it | ⬜ |
| Q2 | Four steps have a local answer and are excluded because their check is this repository's own. Should the `Broad gate` row of `seal/config.md` run them, so the seal covers them after all? | a person | The four are `gather_changelog.py --check`, `fold_ledger.py --check`, `claude_block.py --check` and the inline version-bump shell. **(a)** leave them excluded — the reason is written and a reader can see it. **(b)** add the three scripts to the `Broad gate` row, which is the place a repository names checks of its own; the row then runs on every sealer run in this repository and three of the four steps stop being unanswered. **(c)** ship them as plugin checks, which is a much larger change and makes this repository's CI the plugin's business | **(a)**. Phase 1 measured the split and wrote the reasons; changing what every sealer run in this repository executes is a decision about the repository's own command, which `spec.md` §Scope puts outside this work item | ⬜ |
| W1 | What does the stamp print about steps the seal did not answer — a count, or the names? | the work | `seal_stamp.letter` gives a panel value 23 columns and cuts at the frame with no marker, which #424's sibling work item measured. A count fits; names do not | the phase that writes it follows `broad_gate.py#PANEL_VALUE_WIDTH` and the elision that work item shipped, and states which it chose | ✅ **both, on different streams.** The panel carries the count (`workflow  8 of 13 not answered`, 20 columns of the 23 it has) and `coverage_line` writes the names to stderr beside the line naming the repository's own command. A count alone fails A6, which asks that a reader can tell WHICH; names alone do not fit. Phase 3, `0ec4571` |

**What the framing settled from the tree, so nobody reopens it.**

- **The two lists, read at `3878566`:** the gate runs five arms — the declared
  row, `evidence_check --strict`, `unverified_check`, `chain_check`,
  `survivor_check`. The workflow's `release` job runs thirteen named steps.
- **The step #424 added** is *no merge on this branch dropped a correction the
  ledger had made*, and the gate does not mirror it.
- **Nothing goes red for the omission.** A coverage probe over the eight
  structural modules reading those files reported 243 passed and 8 skipped
  with the arm absent.
- **The prerequisite is already in.** An arm in the gate needs a base resolved
  the way CI resolves it, and #423 shipped that in this same release.
- **The partition is total or it is nothing.** A step with no row is the
  silence the work item exists to end, so *classified* includes *excluded*,
  and an exclusion carries prose rather than a category.
- **This is not the class of whether a mirrored arm asks its step's
  question.** That one is #473's; this one is whether the step is on the list
  at all. The frame wrote #423 here and review round 1 corrected it: #423 is
  about the base the gate resolves, and it ships in this release.
