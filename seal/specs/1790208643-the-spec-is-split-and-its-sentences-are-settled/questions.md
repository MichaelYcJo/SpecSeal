# the spec is split and its sentences are settled — questions for the planner

<!-- seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. The run is `automation`: nobody is asked, so every row says why
the tree could not settle it, and every default continues. -->

## What the tickets left open and the tree answered — do not reopen

| Settled | Answer | Where the grounds are |
|---|---|---|
| Where the split's seam is | the thirteen `#####` subsections under `#### The declaration`, one per record row; the `##`-only split the ticket proposed leaves 1,544 lines whole | `spec.md` §*What was measured*, the heading table; judgment 1 |
| How many documents, and which keeps the name | three; `docs/review-chain-spec.md` keeps the run, the bound and the five owner rules that 18 link strings name | `spec.md` judgments 2 and 14; `plan.md` §*Alternatives* rows 3, 4, 7 |
| Whether the bound-checking subsections (floor, `Needs a fix`, reopening) go with the other arms | no — they stay with the bound they check, as `###` under it | judgment 2; `tests/test_the_run_stops_at_the_last_finding.py:14` |
| Whether headings are re-levelled | yes; the ledger is re-pointed by hand where the level changes (15 anchors) and healed by `--reverify` where it does not (3) | judgment 5; `spec.md` §*Data & interfaces*, the anchor table |
| Whether a moved anchor is REMOVED or re-pointed | re-pointed: a move is `CONTRIBUTING.md`'s rename paragraph, not `CLAUDE.md`'s removal rule | `spec.md` §Grounding, row 3 |
| Whether #331 is a prose edit plus a test extension, or a new gate | a new instrument (a census over the tree with a false-positive argument nobody has made) — DEFERRED | `spec.md` §*Out*, first row; judgment 6 |
| Whether #466 is a prose edit plus a test extension, or a new gate | a test extension: the hygiene tuple as the population, a named history allowlist, two illustrative spellings changed | judgment 7; `spec.md` §Scope, its row |
| Whether #55 copies the table into three definitions | no — one application sentence in the smith; §8 delivers the table by mechanism and the moved-rule check refuses the copy | judgment 8 |
| Whether #268 owes an edit | not unless a grep finds one of its three corrected statements standing | judgment 9 |
| Where #316's paragraph is drafted from | the ticket and `arm_check.py#run_arms`'s docstring; the round record it cites is retired | judgment 10 |
| Whether #222's paragraph describes the code as it stands after #333 | yes; the candidate walk is still by file | judgment 11 |
| How #474 item 1 is corrected in a released row | in place, `Corrected <date>`, the shape A9 and A11 of `1790174138` take | judgment 12 |
| How #488's sentence survives D | it names *the file the row is in* and no path; phase 3 writes it into the sections as D left them | judgment 13; `plan.md` §*What D changes that phase 3 reads* |
| Where #509's sentence goes beyond the two guides | the policy owner `docs/the-evidence-ledger.md` §*A correction a merge dropped*, and one linking sentence at the release checklist's squash step | `spec.md` §Scope; `plan.md` §*Alternatives*, last row |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does #331 move to the 0.16.0 milestone as a check of its own, as this frame judged, or does the owner want an edit pass now over the four longest-shared runs the ticket names? | a person — the repository owner. Why the tree cannot settle it: the ticket's own third open decision is whether the tree-wide check is this ticket or its own, and a milestone assignment is the owner's act. The frame's judgment is in `spec.md` §*Out*; nothing here builds differently under either answer, because the census is not built in this item either way | **defer** (the default): #331 keeps its body, gains a comment naming this frame's grounds, and the owner moves it to 0.16.0. **Edit pass now**: a later work item, not this branch — the ticket says an edit pass without the census is what it refuses | defer; this item's changelog names #331 as deferred and does not close it | ⬜ |
| Q2 | Should the release-branch pin's population widen past the hygiene tuple to `hooks/` and `bin/`, which is where the only other concrete names stand (`hooks/cmdline.py` names `release/v0.22.0` three times and `bin/correction-check` an illustrative `v1.2.3`)? | a person — the repository owner. Why the tree cannot settle it: the hygiene tuple excludes `hooks/` for the timer rule, and whether the branch-name rule's population should differ from the timer rule's is a product choice about which files are *surfaces*. M3 records what `release/v0.22.0` was | **the hygiene tuple** (the default, chosen in `spec.md` judgment 7): `bin/correction-check:10` is changed anyway beside `correction_check.py:23`, because the two spell one usage line. **Every tracked text file**: reaches the four `hooks/` and `tests/` names and every fixture that builds a `release/v9.9.9` branch, each needing an allowlist entry | the hygiene tuple | ⬜ |
| Q3 | Does #488's sentence — keeping an existing claim true happens in the file the row is in, whether the claim drifted by an edit, was falsified by code the branch added, or lost its anchor — close `seal/follow-up.md`'s row on a third arm for *a claim falsified by code a branch ADDED*? | a person — the repository owner, who that row names. Why the tree cannot settle it: the row asks whether §*House rules* gains a third arm, and this item writes the arm the milestone scheduled (#488, drift-by-edit) in words that cover the falsified case too; whether that answers the row is the owner's reading of their own row | **yes**: the owner ticks the row ✅ naming this pull request. **No**: the row stands and a later item narrows the wording | the row stays untouched by this item; the sentence is written to cover both | ⬜ |
| M1 | What are the three documents' line counts after phase 1? The estimates from heading spans are about 900 (run), 505 (gate) and 880 (record); a record document over 1,000 takes the four-file fallback | a measurement — `wc -l` at phase 1's close | — | the estimates | ⬜ |
| M2 | What does the survivor sweep report over the split range, and does the set match `plan.md` §*What the move has to reword*? | a measurement — `bin/survivor-check --range origin/release/v0.15.1...HEAD` at phase 1's close, every line matched to a table row or named as a finding | — | the table's rows and nothing else | ⬜ |
| M3 | Which branch did `hooks/cmdline.py`'s `release/v0.22.0` mean? `git log --oneline -S'release/v0.22.0' -- hooks/cmdline.py` answers *initial commit* at `716d8548` (executed 2026-09-24 by the framer), so the history before the import is where the answer is, if anywhere | a measurement — the framer's run is recorded; whether the name is corrected is Q2's population question | — | recorded, not corrected | ✅ measured 2026-09-24: `716d8548 Initial commit`, so the four mentions predate the repository and no branch of it was meant |
| W1 | Which assertions in the 28 modules go red on the split, and where does each re-point? The section map in `plan.md` says where; the run of each module says which | the work — phase 2, one module at a time, the list in `phases/phase-2.md` | — | the map | ⬜ |
| W2 | Do the two record subsections sit better under `## Two records` (the plan) or as a `##` of their own in the run document? Both keep them in the file the tests read | the work — phase 1 decides by reading the joined text; a `##` of its own costs no test constant | — | under `## Two records`, as `###` | ⬜ |
| W3 | Which release-checklist step meets the ledger conflict — §0's *Squash the work items back to back* or §1 *The preparation branch* — and so carries #509's linking sentence? | the work — phase 3 reads both steps against the 0.15.0 run's own record of where the conflict arrived | — | §0, line 18's bullet | ⬜ |
| W4 | Does #316's paragraph earn a case, and where? `tests/test_arm_check.py` reads the script and not the skill; #310 warns against a document clause pinned by substring | the work — phase 4 reads how that module pins the `--timeout` help and mirrors it if there is a shape to mirror; otherwise no case, with #310 as the grounds in the phase record | — | no case; said in `phases/phase-4.md` | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.

None of the three person rows blocks the build. Each has a default that
continues, and a different answer changes one phase's content without
changing the order of the phases.
