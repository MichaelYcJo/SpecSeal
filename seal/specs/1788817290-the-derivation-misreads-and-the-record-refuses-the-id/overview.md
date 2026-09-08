# 1788817290-the-derivation-misreads-and-the-record-refuses-the-id — overview

`round_record.py` was saying three false things about a fix: that a pytest
test function is unreached, that a unit which began returning a new value
changed no contract, and — when a reviewer numbered findings with the round
in them — that a table held a duplicate it did not hold. All three are one
file, and two of them are one derivation.

## Where spec and implementation diverged

| The document | What was built | Which won, and why |
|---|---|---|
| #211: *"`call_sites` recognising a `def` under `tests/` whose name begins with `test_`"* | that, plus a fixture and a `conftest` hook | **The build.** The ticket's own *Not verified* section asks whether other kinds reach `no call site found` for the same reason, and running the derivation over every def under `tests/` answers yes: 8 of 42 fixtures. Shipping the ticket's literal proposal would have closed one member of a class of three (contract §12) |
| #227: *"The parser appears to take the last digit run"* | the fix for a parser that takes the FIRST | **The code.** `NUMBER_RE.search` matches leftmost. Both readings produce the collapse the ticket reports, so the repair is unchanged — recorded because a later reader comparing the two would otherwise have to re-derive it |
| #227: *"Accept an optional round prefix, **or** refuse with the format spelled out"* | refuse | **The corpus.** 130 committed records run through both rules: the strict rule refuses 2 that pass today, and both of those pass by keying a fix onto the wrong verdict row. Accepting a prefix would also make two rounds' findings legal in one table and turn `close`'s `{number: …}` key — threaded through `unknown`, `missing`, `already` and `depth_two` — into a two-part key for a shape no record uses |
| #194: *"Extend the derivation to flag a unit whose set of returned constant literals differs"* | that, with literals keyed by `(type name, repr)` | **The build, narrowly.** The ticket's wording is a set of values, and Python hashes `0` and `False` into one key. A unit that swapped a count for a flag would have read as unchanged under the literal reading of the ticket |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the orchestrator — contract §2 reserves the broad gate for one run after the rounds settle. What was executed here is the three new modules and the eight neighbouring ones, 361 cases at the last phase boundary |
| Whether `Contract changes` becomes noisy now that a changed returnable literal admits a unit and pulls a reach walk with it | the repository owner, after 0.9.1's own records show how many entries the wider rule adds. `questions.md` Q3, and the narrowing to reach for if it does is *non-string literals*, not a retreat to arities |
| Whether a reach walk should follow a callable passed by name as a value at all — the second cause of `no call site found`, which this branch does not repair | the repository owner. Round 1's finding 5: this was a bullet under an empty table in `seal/follow-up.md`, in the section for items another branch holds, where nothing was waiting on anything. It is tied to a coordinate, so that file's own rule sends it to a `# RIDER:` at the line, which is planted above `floor_record` and reaches whoever opens the file. Round 2's fix pass corrected the rider's evidence: `floor_record` is no longer the unit that shows the cause, and `tests/test_the_records_can_be_carried_out_and_in.py#timed_out` is |
| A committed round record that quotes a `def` line invents a call site for the unit it quotes, because `round_record.py#call_sites` greps every tracked file rather than the Python ones. Executed: `floor_record` read `no call site found` at `ffd1d05` and reads `round-1-report.md, round-1.md` from `824bfca` on, with nothing about the code changed | the repository owner. Found by round 2's fix pass while re-deriving the rider's claim, and not closed here: deciding which files a reach walk may name is a rule, and a fix pass adding one ships it unread |
| A fixture in an uncollected non-conftest module under `tests/` still reads `pytest only`, which is round 2's finding 1 one gate over | the repository owner. Not repaired because deciding it means asking whether a conftest or a collected module imports the name, which is a third question with its own argument. Measured over all 3052 top-level defs: this tree holds no instance |
| Whether the four `Verified … against <anchor>@<hash>` stamps this branch writes hold the hash they claim | `fix/239-a-stamp-names-content-not-a-commit`, whose `rider_check.py` is what recomputes them. This branch's own check verifies that a stamp EXISTS and that a commit-form stamp resolves; the four hashes were computed with that branch's checker and read 4 ok · 0 drifted here, but nothing in this tree recomputes them on a later edit |
| Whether the two committed records that stop parsing under the strict id rule should be corrected in place | the repository owner. Neither will be re-closed — `close` runs on the record `new` just wrote — so nothing is blocked; the rows are wrong in a file nobody will run the generator over again |

## What was fed back into the spec

Three clauses, all *inferred during implementation* and all overturnable:

1. **`docs/review-chain-spec.md` §*The finding id — a bare integer, behind an
   optional severity marker***, new. States the format, both refusals, the
   corpus measurement behind choosing refusal over a prefix, and that the
   round is already in the record's file name.
2. **§*The fix surface*, three paragraphs added.** That `pytest only` is also
   what a unit pytest itself reaches gets — a different condition from the
   *callers all under `tests/`* one already there — with the three member
   shapes and the `conftest`-only limit on the hook arm. And *What
   `Contract changes` does not see*: the changed input→value mapping, the
   measured instance, and the sentence that the residual is the reviewer's.
3. **`docs/review-handoff-protocol.md` §*`Contract changes` names the
   reach*,** one paragraph: both limits, stated for a conforming tool,
   because a protocol promising the row without them promises more than any
   implementation can give.

The second of these is a **stated hole and not a gap**, which is a
distinction a later session can erase by accident. It is pinned:
`test_the_hole_is_a_hole_and_not_a_claim` asserts the contract is unchanged
across the measured instance's two ends, so widening the check while leaving
the paragraph standing turns that case red.
