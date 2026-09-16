# Implementation Plan: three checks that do not see what they are named for

<!-- seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-16 by the repository owner, when `smith` was spawned.

## Summary

Six phases. Four repair a check, one repairs two cells of a committed record,
and the last brings the records up to what the five before them did.

**The order is one repair per phase, smallest blast radius first.** Phase 1
touches one case in one module and nothing reads it. Phase 2 moves three
string literals into constants two other cases read, so it is the only phase
that changes a line no ticket named. Phases 3 and 4 are the two halves of
#422 in the order the issue measured them — the boundary first, because a
stem matching inside a longer word makes every later measurement of the
finder ambiguous. Phases 5 and 6 touch no check at all.

**Each phase is proven by the mutation its own issue already measured**, and
where a phase has no such mutation the row says so and says what stands in
its place. Two phases adopt their issue's paste-ready patch changed rather
than verbatim; the Alternatives table holds the failure scenario that changed
each one.

## Technical context

**#413 — `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
`test_both_ampersand_cells_name_both_shells`.** The case already slices the
refused and allowed tables apart and reads each `&` row from the list that row
is in, so the attribution assertions go where the presence loop already
stands. The two cells are single lines in `templates/config.md` today, at
`:206` and `:225`, and the sentences the assertions pin are *`/bin/sh`
backgrounds the whole line*, *`cmd.exe` separates two commands*, *That is
`/bin/sh`* and *`cmd.exe` sequences*.

The issue's patch asserts over the raw row. The case's own presence loop
flattens each cell first, and the two tail assertions do not; asserting over
the flattened row is what makes a later hand-rewrap of a 300-column cell
harmless, and it costs nothing.

**#418 — `tests/test_one_word_one_meaning.py`.** `flat` folds the
string-literal seam for `.py` members only. Two sweeps search four folded
members between them, and the phrases they search for live in three places:
the constant listing what may legitimately follow a bare `the seal`, which is
live; and three string literals written inside the sweep cases themselves,
which the seam-safety case copies. Making those three literals module
constants that the sweep cases read is not a derivation from the sweeps — it
is the same rule the divergence row of work item `1789455558-…` states, that
the thing pinned is what the production path calls.

```python
# the shape, not the final wording
SEAL_BARE = "the seal"
SEGMENT_LOOSE = ("segments are spawn cycles", "orchestrator's segments")
```

The member half stays as the issue wrote it: the four folded members pinned
as a list, so a `.py` member joining either sweep turns the case red and says
its phrases belong in the set.

**#422 — `tests/test_chain_hooks_hardening.py`,
`test_the_questions_are_collected_before_the_work_not_during_it`.** The stems
anchor `\b` at the front and nothing at the back. `user` stays in the set with
both ends anchored: the anchor is what stops `users`, and a definition telling
an agent to collect in one batch what the user answers is exactly what this
guard exists to refuse. No batch phrase in `agents/*.md` today is within the
window of any occurrence of `user`, so keeping the stem refuses nothing that
stands.

The finder is the second half. Emphasis markers come out before the search,
because `CLAUDE.md:39` states this very rule as *go in **one batch** before
the first edit* and a literal search never sees it; and the preposition and
article are read as a small set, because the issue measured *as a single
batch* passing at exit 0 and the issue's own patch does not cover it.

```python
# the shape, not the final wording
PHRASE = re.compile(r"\b(?:in|as) (?:one|a single|a) batch\b", re.IGNORECASE)
```

**The record cells** are `seal/specs/1789445605-…/rounds/round-2.md:39` and
`:40`. Both Grounds cells read `fixed at 6233b769 — . ` where they should read
`fixed at 6233b769 — `. The cause was #414 and is already removed; the shape
of the repair is the hand repair at `9919b265`, which took `— at  — ` down to
`— ` in nine cells of the sibling record.

**The ledger.** `seal/ledger/1789518345-….md` carries a row anchored on the
unit phases 3 and 4 change, and its claim — that the check decides by what a
sentence claims rather than by the phrase it uses — is true of the refusal
and not yet of the finder. Phase 4 is what makes the whole claim true, so the
row is re-read and corrected in place rather than superseded; `questions.md`
Q2 is where that judgment is recorded if the phase finds otherwise. No row in
`seal/ledger.md` anchors a unit this work changes: the shared file's one row
naming the wrap module anchors its covered list, which stays untouched.

**What breaks in six months.** Phase 2's constants are the risk. A session
adding a phrase to a sweep now edits a constant rather than a case body, and
if it writes the literal inline instead, the seam case silently stops covering
it — the same failure this work repairs, one level up. What stands against
that is the member assertion beside it, which goes red whenever the set of
folded members moves, and the comment that says why the set is closed.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| One shared check over all three modules — *a case that names a thing asserts its attribution* | To judge whether a case sees its subject, the checker has to know that subject, which makes it a second implementation of each case. #418 refuses exactly this for its own phrase set, and this repository has refused it before | **Rejected.** Three assertions in three modules, and the shared thing is the procedure in `agent-contract` §12 and §15 |
| #418's paste-ready patch verbatim — the folded-member list alone | The issue measured two mutations, and this closes one. A seam-carrying phrase added to a sweep leaves the member list unchanged, so the case stays green against the first thing the issue measured | **Rejected.** The member assertion is kept and the phrases are made live, so both measured mutations are red |
| #418, deriving the phrase set from the sweep cases automatically | A derivation would re-implement the sweep inside its own test module, and a bug shared by both would be invisible | **Rejected**, and the issue says so. Hoisting a literal into a constant two readers share is not a derivation — there is one definition, read twice |
| #422's paste-ready patch verbatim — dropping the `user` stem | A definition instructing an agent to collect in one batch what the user answers passes silently. The patch drops the stem to stop `users`, which the anchor it adds in the same breath already stops | **Rejected on the stem, adopted on the anchors.** `user` stays, anchored at both ends |
| #422's finder pattern verbatim — `in one`, `in a single`, `in a` | *as a single batch* is one of the spellings the issue measured passing at exit 0, and the patch's pattern does not match it | **Rejected.** The preposition is read as a set too |
| #413's assertions over the raw table row | A hand rewrap of a 300-column cell turns the case red for a reason that has nothing to do with attribution, and the case's own loop already flattens | **Rejected.** Asserted over the flattened row |
| Bounding #422's window at a heading boundary | An instruction whose sentence straddles a heading passes. It is a third change the ticket did not ask for, with a failure direction of its own | **Rejected**, recorded as residue beside the case |
| Leaving the two record cells to `seal/follow-up.md` | That file refuses a row that cannot name who answers with no condition attached, and Q1 of work item `1789455558-…` already refused both other homes. `release/v0.12.0` would ship two records that read wrong, with nobody holding the item | **Rejected.** Phase 5 |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #413: the two `&` cells' attribution asserted per cell, over the flattened row, beside the presence loop that stays; and what the case still cannot see written beside it | `bin/test tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py -q`, exit code read directly. Green at HEAD; **red under each of the issue's two measured swaps separately** — `/bin/sh` and `cmd.exe` exchanged in the refused row, then in the allowed row | `9d90db85` |
| 2 | #418: the three search phrases hoisted into constants the sweep cases read, the folded members pinned, the reason the set is closed written where a reader meets it, and the residue beside the case | `bin/test tests/test_one_word_one_meaning.py -q`, exit read directly. Green at HEAD; **red under both measured mutations** — a seam-carrying phrase added to a sweep's phrase constant, and `chain_check.py` added to the seal sweep | `0b55b06c` |
| 3 | #422 half one: both ends of every stem anchored, `user` kept | `bin/test tests/test_chain_hooks_hardening.py -q`, exit read directly. **Red at HEAD and green after, with the issue's measured sentence planted** — `agent-contract`'s own wording with `persona` one clause away in a throwaway edit to a definition; and **still red after the repair** with *collect what a person answers* planted, so the narrowing did not buy silence | |
| 4 | #422 half two: emphasis normalised out, the preposition and article read as a set, and the residue — what the window still cannot tell apart, and that it crosses headings — written beside the case | the same command, exit read directly. **Red with each of the three spellings the issue measured passing at exit 0** — `CLAUDE.md:39`'s emphasised form, *in a single batch*, *as a single batch* — each planted beside a person answering; green over `agents/*.md` untouched | |
| 5 | The two cells of `rounds/round-2.md` in work item `1789445605-…` repaired to the shape `9919b265` used, the prose untouched | `bin/test tests/test_chain_check_at_the_pull_request.py -q`, exit read directly — its `_real_records` case runs the checker over this repository's own committed records. **No mutation from the three, and the reason is that this phase repairs a record rather than a check**: the cause was removed by #414 and that work item's own cases hold it, so what this phase owes is that the corrected cells still parse, which is what the command above measures | |
| 6 | The documented widths in the wrap module's docstring re-derived; the drifted ledger row re-read and its claim judged; the ledger and changelog fragments written | `bin/test tests/test_docs_line_wrap.py -q` and `bin/evidence-check .`, both exits read directly, with the widths re-derived using that module's own helpers. **No mutation, because nothing in the tree reads a docstring** — planting a reader is new mechanism aimed at the file `seal/follow-up.md` already holds open for the owner, so re-derivation from the module's own measurement stands in its place | |

This table is also where the work records how far it got. **Status is empty, or
the commit that closed the phase.**

## Operational impact

**No migration, no new environment variable, no new dependency, and nothing a
deployer touches.** Everything this work changes is read by the test suite or
by a person.

**What changes for whoever writes the documents these checks read**, which is
the compatibility surface that exists here:

| | Before | After |
|---|---|---|
| The two `&` cells of `templates/config.md` | either cell can state one platform's semantics as the other's with the suite green | the swap is red, naming which cell lost its attribution |
| A phrase joining either sweep of `tests/test_one_word_one_meaning.py` | unchecked for seam safety | checked, because the set and the sweeps read one definition |
| A `.py` member joining either sweep | unchecked, silently | red, naming the member whose phrases are unaccounted |
| `persona` or `users` near a batch phrase in an agent definition | refused, and the definition has to be reworded | allowed |
| An instruction to collect what a person answers, written with emphasis or as *a single batch* | passes at exit 0 | refused, naming the words in the window |

**Failure direction, per `CONTRIBUTING.md` §*What a change to a gate must
carry*.** Three of the four changes make a check block more, and that is the
cheaper mistake here: every one of them blocks a document that misstates
something a person acts on, and the cost of a wrong block is one reworded
sentence in a file somebody is already editing. The fourth — anchoring the
stems — makes the guard allow more, in one narrow way: two words that were
never a person answering stop firing. That direction is safe because the
refusal itself is untouched; what shrinks is a false refusal that
`agents/smith.md` already meets.

**Prompt budget: zero.** None of the four is a hook or a gate that asks
anybody anything. They are test cases, so being wrong costs a red suite and
never an interruption, and this work item puts no new question in front of a
person at any point after the batch in `questions.md`.

**Platform honesty.** The `cmd.exe` half of the two `&` cells is unmeasured
and is recorded as unmeasured in work item `1789445605-…`'s own records, with
the `windows-latest` job named. This work does not measure it and does not
need to: what phase 1 asserts is that the document attributes each behaviour
to the shell it belongs to, which is a property of the document. If the
`cmd.exe` claim is ever measured false, the cells change and this case is what
makes the change visible instead of silent.
