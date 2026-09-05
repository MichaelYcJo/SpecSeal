# 1788501054-a-check-reports-clean-while-something-is-missing — phase 9

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-9.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 9 |
| Commit | cd7998e |
| Ran by | specseal:smith on opus |

## What this phase was asked

**Carry out the repository owner's answer to round 5's Deferred row: revert
the correction-trace rule.** That answer is option (c) in that table and it is
none of the two fixes the round proposed, so this phase was given an
instruction rather than a finding to judge.

The reasoning was handed over so that the edges could be judged rather than
guessed: no spec asked for the rule — round 4's fix pass invented it to close
a 🟡 — it is the only thing on this branch keying on git history, a feature
branch squashes into its release branch so that history is destroyed at the
merge, this repository has already paid a patch release for exactly that class
(`tests/test_a_rider_reaches_its_file.py`), and the rule had by then produced
the run's second 🔴 plus a 🟡 with two unheld bounds. Round 4's 🟡 7 goes to
the tracker as issue #159.

What to remove was named: `FIELD_ROW`, `_field_cells`, `CORRECTION_MARKER`,
`_correction_traces`, the two cases over them, and the `CORRECTED IN PLACE`
section of `templates/sdd-round.md`. Three edges were left to this phase to
settle by reading — what else references any of them, which record prose has
gone false, and which ledger rows lose their anchor.

One correction was handed over with the instruction: `round-5.md`'s Deferred
table described option (b) as *run a sixth round over the cap*, and
`skills/code-review/SKILL.md` says the verifying round **costs no round**. The
orchestrator asked for that sentence to be corrected in the record and for the
count of its own wrong prose to be kept honest. It is the seventh instance on
this branch.

## What this phase found

**The removal reaches six files beyond the two it was told about, and the
grep is what found them.** Deleting the two cases and the template section
leaves the rule cited from four more places, each of which would have become
a reference to something that no longer exists — which is the class this
branch has now spent three rounds on, *a correction reaches one copy and not
the rest*, arriving one last time from the removal meant to end it:

| Where | What it said | What it is now |
|---|---|---|
| `seal/ledger/1788501054-…md` row R9 | claimed the rule, anchored on the two deleted cases and on the template heading | **REMOVED.** `CLAUDE.md` §*a ledger coordinate names content*: a row whose anchor a change removes goes with the code. There is no replacement claim to write into the fragment — the rule is gone, not moved |
| `changelog.md` | a bullet announcing the rule to the release | removed. It never ships, so an entry for it would be false at the moment it is gathered |
| `round-1.md`'s trace | *"The rule **is** `templates/sdd-round.md`'s"* | says the rule **was** the template's, that phase 9 reverted it, and that #159 carries it. The reason the trace sits in the comment rather than in the cell is kept and re-attributed to `chain_check.py`, where it is still true |
| `round-2.md`'s trace | *"the trace `templates/sdd-round.md` **now requires**"* | the same correction, and the trace stays |
| `round-3.md`'s trace | *"Marking it inside the cell is what the checker refuses"* | **left alone.** That sentence is about `chain_check.py` parsing `New units`, which this phase does not touch, so it did not go false |
| `phases/phase-8.md` | what phase 8 built, including the marker and its mutation | **left alone.** A phase record asserts a past state, the same way a round record does — it was true at `73ee5a1` and this record is where a reader learns it was reverted |

`docs/review-chain-spec.md`, `skills/code-review/SKILL.md`, `overview.md` and
`spec.md` were checked and cite the rule nowhere. It was written in round 4's
fix pass and never reached them.

**Nothing else in the tree keys on the commits of this branch.** Grepping
every `git log`, `git show <sha>:` and `merge-base` under `tests/`, `skills/`,
`bin/` and `.github/` leaves three, and none is of the removed unit's kind:
`tests/test_a_rider_reaches_its_file.py:176` resolves rider stamps, which name
commits on `main` and which this branch does not touch; `chain_check.py`
reads a caller-supplied `<baseline>..HEAD` range rather than this repository's
own history, and an unresolvable SHA makes no claim there, which is the
rebase hole `docs/review-chain-spec.md` declares; and
`.github/scripts/close_issues_on_release.py` reads commit subjects at a
release. **Executed rather than argued**: the whole point was whether they
survive the merge method, and the squashed tree runs them green.

**The squash reproduction — the check that was red — is clean.** Branch from
`origin/release/v0.8.0` in a `--no-local` clone, `git merge --squash cd7998e`,
one commit: all **five** round records go to 1 commit each, which is the exact
state that failed at `111a6df`, and the six suites that read the records, the
checkers or this branch's documents return **152 passed**. Driven from Python
(`agent-contract` §8) so no commit reached the gate from a Bash command line.

**This phase adds nothing, so `agent-contract` §15 has nothing to hold.** No
unit, no case, no constant. Saying so is the requirement — a pass that
invents a case in order to have one seen red is the counterfeit this branch
has already caught twice.

**A red suite was found that this branch has carried since phase 6, and it is
not this phase's to fix.** `test_the_instructing_documents_name_rounds_as_the_destination`
fails on `templates/sdd-round.md`: the paragraph phase 6 added at
`c528161` writes *Measured: `round-1.md` of the work item…* with no
`rounds/` in front of it, and the check refuses a record name with no
directory. Bisected across all 34 commits of the branch — 0 offenders through
`47e6ebf`, 1 from `c528161` onward — so it is red at HEAD as it was at
`111a6df`, and five review rounds never ran that suite. Named in the handover
with the one-word repair rather than made here: the requested change is a
removal, and round 6 reads this diff for one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `FIELD_ROW`, `_field_cells`, `CORRECTION_MARKER` and `_correction_traces` from `tests/test_a_record_precedes_the_fixes_it_commissions.py` | Nowhere. Issue #159 carries the finding they enforced, with the measurement a replacement design has to answer — chiefly that a reader of this repository's record history is reading a history the merge method destroys |
| `test_a_cell_corrected_after_the_record_landed_says_so_in_the_record` and `test_the_template_puts_the_correction_trace_where_no_checker_reads_it` | Issue #159. Both were round 4's 🟡 7 answered as a rule; the finding is unanswered again and now says so in one place instead of being enforced by a reader that goes red on the release branch |
| The `CORRECTED IN PLACE` section of `templates/sdd-round.md`, five paragraphs | Issue #159. The template no longer asks for the trace, and the four records that already carry one keep it |
| Ledger row R9 | Nothing — its claim went with the code. `CLAUDE.md` forbids re-pointing it, and the new claim it would carry does not exist |
| The changelog fragment's bullet for the rule | Nothing. The rule does not ship, so the release has nothing to announce |
| `round-5.md`'s description of option (b) as *a sixth round over the cap* | The same row, saying the verifying round costs no round, per `skills/code-review/SKILL.md`. The seventh piece of the orchestrator's prose this branch has had to correct |
| The imports `glob` and `re` from the test file | Nothing — the removed units were their only callers, and `uvx ruff check` is what says so |
