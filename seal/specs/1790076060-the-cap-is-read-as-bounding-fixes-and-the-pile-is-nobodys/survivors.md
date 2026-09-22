<!-- seal/specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys/survivors.md
— survivors a person opened and judged legitimate. The quote is the anchor, so
each row stops holding the moment that text changes.

Round 1's fix pass rewrote the capped exit in seven live sites, and
`survivor-check --range 4ddfde2e..9f8efea4` — the fix commit alone, before
this file existed — reports three places still carrying the wording it
removed. All three are correct where they stand, and for two different
reasons: two are records of a past release, which is where a behaviour change
is supposed to survive, and one is a runtime message this work item is scoped
out of changing.

**THE RANGE MATTERS, AND THESE GROUNDS ARE NOT BEING READ: #507.** Over any
range that INCLUDES this file — `4ddfde2e..9d9180f8`, or
`origin/<base>...HEAD`, which is the form the hygiene workflow runs — the
check reports zero candidates rather than three, with `--exempt` and without
it. A survivors row quotes the standing wording verbatim, because the quote is
the anchor, so adding this file writes the removed sentence back into the
range and `wanted` subtracts it. What that costs whoever reads these rows:
**the check that appears to be holding them is not.** The grounds below are
never printed at the pull request, and a row whose quoted text later changes
cannot rot loudly the way the third row's grounds assume. The degradation
property was probed and is real at the tree these rows were written against;
the defect is one tree further on. #507 carries it, and until it is repaired
these three rows are read by people rather than enforced by a check. -->

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | in one spelling (`CAPPED_EXIT`): every finding still open becomes an issue, its verdict reads `deferred #N` | A shipped changelog entry, under `## 0.8.1 — 2026-09-05`. It describes what the reopening bound's refusal message said **when that release shipped**, which was true then and is the whole point of a released entry: this repository's rule is that a behaviour change survives in a record of the release that made it. Correcting it would rewrite history to say 0.8.1 shipped a message it did not ship, and the entry would then describe no release at all. The wording it quotes is `CAPPED_EXIT`'s, which still reads exactly that way — see the third row |
| `seal/specs/1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records/changelog.md` | in one spelling (`CAPPED_EXIT`): every finding still open becomes an issue, its verdict reads `deferred #N` | The same sentence one work item over, and the same class: this is the fragment the 0.8.1 entry above was gathered from, so the two are one text in two lifetimes. A fragment is a record of what its work item shipped, and a work item that shipped is not edited by a later one — `settle` retires the directory, nothing rewrites it. Correcting it would also put the fragment and the gathered entry out of step, which is the one thing the gather step cannot detect |
| `seal/specs/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks/questions.md` | So whatever silences it is earlier in the file and not the example | A past work item's `questions.md` Q4, and the survivor of a different removal: the broad gate's refusal fired the `# RIDER:` on `agents/smith.md` §Phases, re-reading it showed its measured half no longer reproduces, and correcting the rider removed that sentence from the live file. This copy is a record of a moment — that work item measured it at its own branch tip and at `release/v0.9.3` and wrote down what it found, which is what a `questions.md` row is for. Correcting it would rewrite what a past run measured, and the row is still OPEN with the repository owner as its answerer, so the measurement in it is the evidence the question rests on. **My re-measurement is new evidence for that row, not a replacement of it**: at this tree the line with everything above it gives one invocation rather than zero, and the rider now says so and points here |
| `skills/code-review/scripts/chain_check.py` | the run is `capped` — every finding still open becomes an issue, its | `CAPPED_EXIT`, the refusal message the reopening walk prints. **This row and the disclosure are the same sentence.** Under the ladder a finding at that exit may take rung 2 or rung 4 instead of becoming a new issue, so the message is now imprecise where it was exact — but it is a line a person reads and acts on, and rewording one is a gate change carrying `CONTRIBUTING.md` §*What a change to a gate must carry*, which `spec.md` §Out scopes this work item away from: a comment or docstring in this file may be corrected and nothing it computes may change. The docstring two lines above the walk was corrected and names the ladder's owner; the message was not. **Who answers whether it should be reworded: the repository owner, through the review chain**, and it is open in `overview.md` §*Not verified* rather than only here. Two pins also read this constant's text — `tests/test_the_reopening_is_one.py` asserts `deferred #N` in the refusal's output — so the reword is a change to a checker's output and its cases together, which is what makes it somebody's decision rather than a tidy-up |

| Range | Grounds |
|---|---|
| `origin/release/v0.13.1...HEAD` | **The range is a merge resolution over `seal/ledger.md` and it removed nothing.** Two sibling work items of this release re-read overlapping rows for different reasons, so the resolution is the union of both sides' notes; every row the release branch carries is present here and **all thirty of its `Re-read 2026-09-22` sentences are present verbatim**, measured rather than argued. What the sweep reports is a consequence of that union: touching a row rewrites its line, so every sentence the old line held reads as removed, and those sentences are the ledger's most duplicated boilerplate — *This claim is about a different part of the section and is untouched*, and the two `for #450` notes. Nineteen of the twenty-eight places are other rows of `seal/ledger.md` itself and the rest are the sibling work item's own records of the same reading. Correcting any of them would delete a note recording that somebody read a claim, which is the opposite of what this sweep exists to protect. **The row is anchored on this range and stops holding at any other**, so a later branch that genuinely removes one of these sentences is reported. |
