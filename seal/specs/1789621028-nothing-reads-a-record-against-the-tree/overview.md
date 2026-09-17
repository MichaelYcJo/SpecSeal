# 1789621028-nothing-reads-a-record-against-the-tree — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `seal/specs/1789621028-…/{routing.md, spec.md, plan.md, questions.md}`; `skills/agent-contract/SKILL.md` §§1–4, §6, §7, §9, §12, §14, §15; `skills/implement/SKILL.md` §§1–4, §6; `CLAUDE.md` §*a change writes fragments, never the shared file*, §*a ledger coordinate names content*, §*a thing more than one party can have is named with whose*, §*no real identifiers*, §*The goal a design is chosen against*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it*; `docs/review-chain-spec.md` §*The fix surface*; `templates/{sdd-round.md, sdd-phase.md, sdd-overview.md, ledger.md}`; `seal/follow-up.md` in full; #344, #426 and #427 read with `gh issue view`
· evidence: `seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md` — R1 through R8 added; 22 rows of `seal/ledger.md` re-read, re-verified and re-stamped to 2026-09-17, because this branch changed content under twelve of their anchors
· verified: **executed** — every module this branch touches, run narrowly at each phase boundary, with every added case seen red against the mutation it actually pins; `bin/evidence-check .` and `--strict` (1340 ok · 0 drifted · 0 broken, exit 0); `.github/scripts/rider_check.py` exit 0; `chain_check.py` over this repository. **Unverified** — the full suite, the repository-wide lint and the typecheck, which `agent-contract` §2 leaves to the sealer

## Why this work exists

A round record is written once and the tree keeps moving, and nothing read one
against the other the way `evidence-check` reads the ledger — so this pins a
fix range in the record where a generator writes it and a checker reads it,
and closes the two instances of the class that live inside that generator.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Phase 1's acceptance assumes a green baseline for `tests/test_chain_hooks_hardening.py` | `plan.md` Phases row 1: "exit 0 untouched". Executed at `5adaffef`, the frame's own commit: **exit 1**, `test_every_spec_directory_that_reached_the_ladder_has_an_overview` naming this work item | Open `overview.md` before phase 1 and take the baseline from there | Writing `spec.md` and `plan.md` is what puts a directory on the SDD ladder, and that case demands the closing memo the builder owns. The claim was true of the tree the framer read and false of the tree the framer left. The memo was due at the first divergence and this is it |
| Three of the frame's corpus counts | `spec.md` and `plan.md`: **223** round records with a verdict table, **11** fix-table files stating a range in **eleven** spellings, **2** naming `HEAD` | The measured figures: **227** of 229 `round-N.md` files, **15** of 39 fix-table files, and — after round 1's 🟡 3 — **12** distinct sentence forms with **5** ending `HEAD` at `56945007`, 4 at this tip. Those are what shipped into `docs/review-chain-spec.md`, the changelog and the ledger, **with the command that produces them named beside them** | Re-measured 2026-09-17 at the branch tip, because the class this work item is about is a record asserting what nobody measured. None of them changes a decision — 15 files in 8 spellings refuses the prose-parsing alternative more firmly than 11 in eleven did, and the **zero** surviving doubled prefixes that phase 3's disclosure rests on reproduced exactly. `spec.md` and `plan.md` are left unedited: a frame is another party's record of a moment, and the correction belongs in the build's records and in what the build ships |
| `#344`'s five bullets, against the tree | The ticket names five coordinates | Two do not resolve as written, one is right for the wrong reason, one describes a state the squash destroyed, and one names no coordinate at all | `phases/phase-5.md` holds the bullet-by-bullet table. The ticket was written from `rounds/round-4-report.md`, which names three commits — `3b228f4`, `8fd2f59`, `bab5c7d` — that **no longer resolve in this repository**. The ticket's evidence is itself a record naming commits a merge destroyed, which is the class one level above the one it filed |
| Where the read half of #427 can reach | `spec.md` scope item 3 asks for an arm naming a record whose `Grounds` carries its own close-prefix twice | Built for `fixed` alone, and the arm says so | Only one of the three fix words leaves a recognisable shape: `close` writes `fixed at <sha>` for `fixed` and the author's own words for `answered` and `deferred`, so a standing duplicate of either is indistinguishable from prose that repeats itself. The write guard covers all three at the moment of writing. Stating the limit beats an arm that implies three and finds one |
| `seal/ledger.md` was re-stamped, and `spec.md` §Out excluded it | `spec.md` §Out: *Re-anchoring or re-stamping anything in `seal/ledger.md` — nothing here removes code an existing row cites*. Twelve anchors in that file nonetheless drifted under this branch's edits, and 22 row-anchors were re-verified and re-stamped, with the `Checked` date moved by hand | Re-stamp, and record the divergence here | The exclusion's own grounds are about REMOVAL, and nothing here removes code a row cites — the rows' claims were re-read and all twelve still hold. But a drifted row fails `evidence-check` and `--strict` takes the tree to NOT SEALED, so leaving them was not available: the scope line anticipated the wrong verb. **Round 1's 7 is that the act was required and the record of it was missing**, which is right — this row is that record |
| `verdict_table`'s return arity | It returned `(rows, col, errors)` and the header was parsed and discarded | `(rows, col, header, errors)`, with three call sites updated | The cell has to be located by the name at the top of its column. That function's own docstring settled it: *a second walk of the same markdown is exactly the split this file spends its docstrings closing everywhere else, so the walk happens here and the questions are asked of what it returns*. A private helper walking again would have contradicted the sentence directly above it |

## Not verified

| Item | Who must answer |
|---|---|
| The full test suite, the repository-wide `ruff check .` and `ruff format --check .` | the sealer, after the review rounds settle. Every module this branch touches is green narrowly and the changed Python files are lint- and format-clean; a broad run taken before the rounds is spent by the first fix |
| Whether `chain_check.fix_range` behaves correctly on a record whose fix range is read AFTER a squash in a real repository, rather than in a fixture with unresolvable SHAs | the repository owner, at the first release that merges a work item carrying the new row. The notice path is pinned by a case using two SHAs the fixture cannot resolve, which is the same code path and not the same event |
| Whether the `Fix range` row is actually filled correctly by a review run end to end. Every measurement here drives `close` directly; no complete chain has yet written one | the repository owner, at this work item's own review rounds — they are the first run to write the row |
| That a hex-shaped branch name pointing at a commit whose SHA starts with that name is accepted by `parse_range`. The coincidence is reasoned about and recorded in the code, not reproduced | the repository owner. Closing it would mean asking git which refs exist, which makes the rule depend on what somebody else created — the trade is stated at `PINNED_RE` |
| Whether refusing a doubled close-prefix ever blocks a repair nobody anticipated. The documented repair is pinned green and the half-restored one pinned red; a third shape would be found by use | the repository owner, at the first fix pass that meets the refusal in a real run |

## Not done

**No `Location` was re-pointed, and that is deliberate.** #344's third bullet
is that record Locations are `file:line` where this repository's coordinates
are content anchors. It is true, and `rounds/round-2.md`'s finding 8 was wrong
on the day it was written. Correcting it to today's line number restarts the
same rot; migrating all of them is `questions.md` Q1, which the frame refused
and which the branch's default builds around. What phase 5 did instead is
record the finding beside the cell.

**`seal/follow-up.md` is untouched.** All eleven rows were read at framing and
again here. The two nearest — `evidence-check` ignoring a malformed
coordinate, and seven ledger rows anchored on a whole heading path — are about
the **ledger's** anchors and about `evidence_check`; this work item changes
neither, so nothing here unblocks them and no row is deleted.

**The prose header of a fixes file is left exactly as it stands**, and the
grounds are the 8 spellings measured across 15 files. A parser over that is a
guess that fails open on the 24 files carrying no header at all. Only the
three ranges that had actually stopped meaning what they said were pinned.

**No `answered` or `deferred` duplicate is findable**, and nothing in this
branch pretends otherwise. A record whose `answered` grounds were doubled
before the write guard landed stays unreadable, which is written into the
arm's own docstring rather than left for a reader to discover.

## Fed back into the spec

Two clauses, both **inferred during implementation** and both open to being
overturned:

- **A measurement is reproducible only against a named range AND a named
  version of the thing that measured it.** `docs/review-chain-spec.md` §*The
  fix range* now carries the fix-range half; the version half is recorded in
  `seal/ledger/1789621028-…md` R7 and in `phases/phase-5.md`, and it is not
  yet a rule anywhere. It came out of Q3: the same pinned range reports three
  under the old checker and two under the current one.
- **A `*_FROM` cutoff belongs to an ABSENT row, not to a malformed one.**
  `fix_surface` already drew that line in its docstring and nothing stated it
  as a rule; `doubled_grounds` ships with no cutoff on exactly that reasoning,
  and `docs/review-chain-spec.md` §*The fix range* now states it in a table row
  for the other direction. A future record rule has a precedent to cite either
  way.
