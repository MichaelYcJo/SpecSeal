# 1788501054-a-check-reports-clean-while-something-is-missing — review round 6

| Field | Value |
|---|---|
| Target SHA | ff22b34 |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | `ff22b34`, against `origin/release/v0.8.0` — the full suite **2088 passed · 4 failed · 1 skipped**, `ruff check .` and `ruff format --check .` both clean. All four failures are `tests/test_the_records_can_be_carried_out_and_in.py`'s zip-export cases, and all four reproduce identically on `origin/main` and on `origin/release/v0.8.0` in clean clones while `main`'s CI is green at that same commit — macOS-only, opened as issue #160 |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE REVIEWER'S ANSWER IS `no`, and it is copied here rather than
re-derived from the table below. Two 🟡 are open in that table and the round
judged both answerable with grounds, which `skills/code-review/SKILL.md` says
is still `no`: the condition is *this round wrote no code nobody read*, not
*this round found nothing*.

**The orchestrator fixed them anyway**, and the reason is only true of one of
them: 🟡 2 is a false row count in a ledger fragment, and `fold_ledger.py`
moves that comment verbatim into `seal/ledger.md` at the release, so the false
count ships. 🟡 1 is fixed in the same commit because it is one line and the
two are the same act of closing this directory truthfully.

That choice has a consequence and it is written down rather than absorbed:
edits were made, so somebody has to read them, and this record's `Fixes checked
by` cannot say `no fixes to check`. **Round 7 is the reader.** It is a
verifying round at a two-line diff, and `docs/review-chain-spec.md` and
`skills/code-review/SKILL.md` both say a round that opens nothing needing a fix
does not consume the cap — which is what makes this affordable at a bound that
is otherwise spent.

The alternative was to answer both with grounds and tick `Pass` here. It was
rejected for one sentence's worth of reason: the ledger header would then be
false in the shared file, and this work item is *a check reports clean while
something is missing*.

Written and committed before the fixes it commissions, so both fix-surface
rows start pending. -->

## What this round was asked

The verifying round at `git diff ccd10a8..ff22b34` — **three commits**, given
as a count the round was told to re-take, and it did: `git rev-list --count`
returns 3.

The diff is a **removal**. Round 5 opened a 🔴 — the correction-trace rule,
invented by round 4's fix pass to close a 🟡, keyed on git history that the
release squash destroys — and **the repository owner chose to revert the rule
rather than fix its reader.** Round 4's 🟡 7 went to the tracker as issue #159.

**Seven specific things to try to break**, named with coordinates: the
removal's completeness; the four calls the pass made about what to leave
standing; the ledger row removed rather than re-pointed, and whether the drop
from 535 to 533 is exactly its two coordinates; **the squash, reproduced
independently**; what still keys on this branch's commits; the orchestrator's
one-word template fix and whether any other instructing document names a record
without its directory; and the terminal condition itself, asked as *what would
a seventh round open in a diff that is a removal*.

**And the round was told what was at stake**, because it changes nothing about
the judgment and everything about the honesty of writing it down: the cap is
otherwise spent, so a finding here puts the run past its bound. The prompt said
so and said that neither fear of it nor eagerness to end the run belongs in the
answer.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `round-3.md`'s trace still asserts a branch-wide rule that no longer exists — *the trace the record itself owes … applied as one rule to every such correction on this branch*. At HEAD no rule requires a trace anywhere | `rounds/round-3.md:47` | open | **Read**, and orchestrator re-verified the line. Phase 9's table justifies leaving this record alone by quoting a sentence further down the paragraph — *marking it inside the cell is what the checker refuses* — which is true, because `chain_check.py` still parses `New units` per `;`-separated entry. The defence is sound about the sentence it addresses and never reaches the sentence above it. `round-2.md` was corrected for exactly this wording; all three paragraphs were written by one fix pass at one commit, two were corrected and one was not, and the criterion that separated them is narrower than the falsehood |
| 🟡 2 | The ledger fragment's header count is false, and the commit that changed the row count left it. The comment opens `**Eight rows.**` and accounts for eight; the file holds **nine**, and held ten before this diff | `seal/ledger/1788501054-…md:4` | open | **Executed** by the orchestrator: `grep -c '^| R[0-9]'` returns 9 and the rows are R1, R2, R3, R4, R6, R7, R5, R8, R10. The staleness predates this diff — round 4's fix pass added R9 and R10 without touching the header, so it read *Eight* over ten at `ccd10a8` — and **R10 has been unaccounted for since it was written**. The header is voluntary prose, which `CLAUDE.md` permits, but `fold_ledger.py` moves the comment verbatim into `seal/ledger.md` at the release, so the false count ships |
| 🟢 3 | The removal's completeness | the whole tree | answered | **Executed**: the tree grepped for every removed name plus `correction_trace`, `correction-trace` and the template heading. Every survivor is inside a record — `round-1` … `round-5`, `phase-8`, `phase-9` — and no code, skill, doc, template or test cites one. `uvx ruff check` on the changed test file and `templates/` passes, so the `glob` and `re` import removals are right. The deletion hunk is exactly two constants, two helpers and two cases; 39 cases remain in the file |
| 🟡 4 | The four calls about what to leave standing — three hold | four records | one open, three answered | `phase-8.md` left whole is right: a phase record is the account of one commit, and `phase-9.md` is where a reader learns it was reverted. `round-1.md` and `round-2.md` are correctly repaired, and `round-1.md`'s re-attribution of the reason to `chain_check.py` is true. The fourth is 🟡 1 |
| 🟢 5 | The ledger row — REMOVED rather than re-pointed | `seal/ledger/1788501054-…md` R9 | answered | **Executed** in a `--no-local` clone, unscoped at both SHAs: `535 ok · 26` in this fragment at `ccd10a8`, `533 ok · 24` at `ff22b34`. The whole drop is inside this work item's fragment. R9 carried three written coordinates of which **two** matched `ANCHOR_RE` — which is the ❓ below — and R9 was the only row citing anything removed. Orchestrator re-ran the unscoped check at HEAD: `533 ok · 1 drifted · 0 broken` |
| 🟢 6 | The squash, reproduced independently | the release merge | answered | **Executed**, driven from Python: clone, branch from the release branch, `git merge --squash ff22b34`, one commit. The squashed tree is byte-identical to the branch tree and all five records collapse to **1 commit each** — the state that was red. Fourteen record-, checker- and document-reading suites there: **588 passed, 4 failed**, and the four are #160's macOS-only export cases. Nothing red that this branch causes, and the round's suite selection is wider than the fix pass's six |
| 🟢 7 | What still keys on this branch's commits | three readers | answered | **Executed**: `test_a_rider_reaches_its_file.py` resolves stamps that live on `main`, `chain_check.py` reads a caller-supplied range and asserts nothing about an unresolvable SHA, and `close_issues_on_release.py` reads commit subjects at the release. All three green on the squashed tree, and the enumeration is complete |
| 🟢 8 | The orchestrator's one word, and the wider question under it | `templates/sdd-round.md:82` | answered | **Executed**: at `9553d58` the case's own predicate finds exactly **1** offender in that file; at HEAD the handoff and line-wrap suites give 52 passed, and the hunk differs only by the `rounds/` prefix and the wrap points, so the rewrap moved no meaning. The harder half closes clean: the round ran the case's regex over every tracked file outside the records and **no instructing document leaves a record without its directory**. One coverage note, not a defect — `test_a_phase_hands_the_next_one_a_record.py` requires `phases/phase-N.md` in three prose carriers and the round record's equivalent covers two files |
| ❓ 9 | A ledger coordinate written with no `@hash` is invisible to `evidence-check` — not `ok`, not `drifted`, not `broken`, not `old-format` | `evidence_check.py#ANCHOR_RE` | out of verified scope | **Read**, and orchestrator re-verified: `ANCHOR_RE` **requires** `@(?P<hash>[0-9a-f]{6,12})`. R9's first coordinate carried none, so for that row's whole life the checker resolved it as nothing at all. `old_format_rows` exists to stop exactly this silence for the sibling `path:line` shape, on the recorded grounds that a ledger full of them once read `0 ok · 0 drifted · 0 broken`, exit 0 — and the third shape falls through it. The instance left with R9, so this diff owes nothing. Deferred below |

## Executed probes

| What was run | Result |
|---|---|
| **the broad gate**, by the orchestrator at `ff22b34` — the full suite, `ruff check .`, `ruff format --check .` | **2088 passed · 4 failed · 1 skipped**; ruff clean both ways. The four are #160 |
| the same four cases at `origin/main` and `origin/release/v0.8.0`, each in a clean clone | **4 failed · 74 passed**, identically at both — and `main`'s CI is green at `10b0017`, so they are the platform and not the tree |
| **the release squash, reproduced by the round** — branch from the release branch, `merge --squash ff22b34`, one commit, 14 suites | five records at **1 commit each**; 588 passed · 4 failed, the four being #160 |
| the tree grepped for every removed name and the template heading | every survivor is inside a record; no code, skill, doc, template or test cites one |
| `evidence_check.py .` **unscoped** at `ccd10a8` and at `ff22b34`, in a clone | `535 ok · 26` in this fragment → `533 ok · 24`; the whole drop is R9's two matching coordinates |
| the same, re-run by the orchestrator at HEAD | `533 ok · 1 drifted · 0 broken` — S8 alone at `@45edf260` |
| `grep -c '^\| R[0-9]'` on the fragment, by the orchestrator | **9** rows against a header saying eight — 🟡 2 |
| the case's own predicate over `templates/sdd-round.md` at `9553d58`, then over every tracked file outside the records | 1 offender then, none anywhere now |
| `chain_check.py --baseline origin/release/v0.8.0` at HEAD | exit 1, two lines on `round-5.md` — the `nobody` notice, which does not fail, and the unchecked `Pass`, which does |
| `bin/unverified-check` · `uvx ruff check` on the changed test file and `templates/` | exit 0 · All checks passed |
| the doc, ledger and checker suites after the orchestrator's two corrections | **178 passed** |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 3, 4, 5 | whatever unit the last fix pass invented | Three verifying rounds, three reopenings, and every one of the three was inside a unit the previous fix pass had just created. This round is the first whose diff invents nothing, and it is the first that opens no code |
| round 6 | `evidence_check.py#ANCHOR_RE` | ❓ 9. A coordinate shape the checker counts in no bucket, in a work item whose subject is a check reporting clean while something is missing |
| round 6 | `seal/ledger/1788501054-…md`'s header comment | The count was wrong for two rounds before anyone read it, and `fold_ledger.py` ships the comment into the shared file |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 9 — a ledger coordinate with no `@hash` is counted in no bucket. `old_format_rows` closes the same silence for the `path:line` shape and this third shape falls through it | this row, and a candidate for issue #159's neighbourhood or an issue of its own | **the repository owner** |
| Whether `st_ino == 0` actually arrives on `windows-latest`, and the `normcase` pairing the corrected §13 limit describes | `overview.md` §Not verified | the windows CI leg at this pull request — carried from rounds 2 through 5 |
| Issue #160's four macOS-only export failures. They reproduce on `main`, on the release branch and in the round's squashed clone, and `main`'s CI is green at the same commit | issue #160, `release: 0.8.1` | the repository owner |
| `questions.md` Q2, Q3 and Q4, all confirmed written as questions with labelled options and `⬜ the repository owner` | `questions.md` | the repository owner |
| `test_a_phase_hands_the_next_one_a_record.py` requires `phases/phase-N.md` in three prose carriers; the round record's equivalent covers two files. No file is wrong today either way | this row | nobody yet — a coverage note, not a defect |
