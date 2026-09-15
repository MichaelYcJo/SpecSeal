# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — review round 2

| Field | Value |
|---|---|
| Target SHA | 3b45bde8 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 416 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Contract changes | none |
| New units | test_flat_is_what_folds_the_seam_and_it_folds_python_only (depth 1) |
| Needs a fix | yes — 🟡 1, the seam fold that no case holds |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round. Its target is the diff of round 1's fixes —
`f41927ff..3b45bde8` — and its job is the answers rather than new findings:
are round 1's two numbered verdicts actually closed, and are its four
`answered` corrections true.

The seven units round 1's record names under `New units` are exempt from that
rule and were read as a finding surface, because nobody has reviewed them.

Three claims the fix pass made about its own work were checked rather than
trusted: that folding the literal seam reaches the live anonymous instance it
found in `round_record.py`, that the row restored to `seal/ledger.md` is true
and does not duplicate the fragment's, and that the eight drifted anchors were
re-read rather than only re-stamped — round 1's own ⬜ 7 was a row re-stamped
while its enumeration had gone stale.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the seam fold is held by no case — reverting `flat` to its pre-fix body leaves all 17 cases in the module green, and round 1's 🟡 2 is open again with the suite silent | `tests/test_one_word_one_meaning.py#flat` | **fixed** `4a372f60` | fixed at 4a372f60 — `test_flat_is_what_folds_the_seam_and_it_folds_python_only` goes through `flat` rather than through the pattern beside it. Three assertions: the joined phrase is in `flat("…round_record.py")`; the same phrase is not in the unfolded flatten, which asserts the seam it reads is really there so the case cannot pass against a rewrapped source; and a shell command in `README.md` survives, which pins the `.py` guard. Both mutations the round measured at 17 passed, exit 0 now exit 1, each killed by a different assertion; Executed in the clone at `3b45bde8`: `flat` back to `" ".join(read(*parts).split())` → 17 passed, exit 0; the `.endswith(".py")` guard dropped → 17 passed, exit 0. Both new cases call `LITERAL_SEAM.sub` and neither calls `flat`. The proposed case is green as shipped and red under each mutation |
| ⬜ 2 | the fold's comment claims a folded seam *can only create a hit, never hide one*; the prefix class sits between the quotes, so a short literal is deleted rather than joined, and the case named for the claim asserts three examples instead | `tests/test_one_word_one_meaning.py#LITERAL_SEAM` | **fixed** `4ea9829e` | fixed at 4ea9829e — the fold's comment no longer claims it can only create a hit and never hide one. It states the guarantee that holds: the prefix class sits between the quotes, so a short literal is deleted, and a deletion joins its neighbours — it can cut a phrase in half only where the phrase itself carries a foldable seam. The case now asserts that over the whole swept phrase set rather than three examples, and records the two shapes the fold does not reach. `seal/ledger.md`'s narrow form of the same over-claim is corrected to say SAME quote character; Executed: `seal_stamp.py`'s `GOLD` dict loses its `"R"` key and `test_session_cost.py` loses `call("b", …)`, both swept files; `open(p, "rb")` → `open(p, )`. Nothing is hidden today because every swept phrase is quote-free. `seal/ledger.md:2203` carries the narrow form of the same over-claim: a mixed-quote seam is still invisible, since the pattern requires `\1` |
| ⬜ 3 | the second arm tells every row it fires on that a cell *quotes a blocking finding an earlier round opened*; the selection routes rows whose marker is this round's own, or is in the Finding or Location cell and quotes no finding at all | `skills/code-review/scripts/chain_check.py#open_row_reason` | **fixed** `4ac3d9ab` | fixed at 4ac3d9ab — the sentence says *carries a blocking marker* instead of *quotes a blocking finding an earlier round opened*, and offers *drop the marker*. That is what the selection actually tests, so the arm describes the condition it can check rather than the usual cause of it. The docstring's premise is corrected with it, since it rested the arm's silence about the marker on the quote being what selected the row; Executed against the real selection: three rows reach the arm and get that sentence, including the fix's own `OPEN_ROW_QUOTING_A_BLOCKER` fixture, which sits in a `round-1.md` and says round 1 opened it. The remedy offered still works in all three, so the clause misattributes rather than misdirects — but the docstring rests the arm's silence about the marker on that premise |
| ⬜ 4 | the same sentence still calls the author's verdict *an unrecognised verdict*, one clause after dropping *outside the vocabulary* for saying that about `open` | `skills/code-review/scripts/chain_check.py#open_row_reason` | **fixed** `4ac3d9ab` | fixed at 4ac3d9ab — the same sentence stops calling the author's verdict an unrecognised verdict; it reads *a verdict counted as closed without being one of those words*. A case asserts the old phrase is absent, and that assertion is independently load-bearing: with only that clause restored, the two `open`-row cases go red on it while the marker clause stays green; Read: the message ends *an unrecognised verdict counted as closed is the tolerant read this file exists to refuse*. True of the class, and `open` is the word `agents/warden.md` prescribes. The clause before it, `not one of the words that close a row`, is the accurate spelling and is already there |
| 🟢 | round 1's 🟡 1 is repaired: the selection is unchanged and both new cases are load-bearing | `skills/code-review/scripts/chain_check.py#open_blocking`, `#open_row_reason` | verified | Executed, two mutations killed: the arm reverted to its pre-fix sentence turns 3 cases red including the new `open` case; the selection widened so the quote is not required turns the new control red alone. `open_blocking` is unchanged in the fix range |
| 🟢 | round 1's 🟡 2 is repaired: mutation C is dead, the live instance is reachable, and single-literal coverage is intact | `skills/code-review/scripts/round_record.py#seal`, `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | verified | Executed, three mutations, all exit 1: the seam-split second instance, the broad-gate refusal reverted to its shipped wording, and a single-literal instance. Read: `round_record.py` holds three mentions of the word and all three name whose |
| 🟢 | the removed `seal/ledger.md` row is restored and true, and the fragment does not claim the same thing | `seal/ledger.md:2203`, `seal/ledger/1789455558-the-record-chain-disagrees-with-itself-in-five-places.md:13` | verified | Read: clause (a) holds — the refusal names the subcommand in both sentences and the module carries no bare instance. The fragment's row 5 claims which check holds the rule and which pins remain, which is a different clause, and its Notes now say the shared row is restored rather than superseded |
| 🟢 | the re-stamped anchors were read, not just refreshed | `seal/ledger.md:1945`, `seal/ledger.md:2201` | verified | Executed: `seal` holds 6 `raise Refused` sites against S6's **six**, and `reach_forward` holds 3 against the corrected row's **three**. `bin/evidence-check --strict .` exit 0 read directly — 1276 ok · 0 drifted · 0 broken, records arm 0 refused |
| 🟢 | round 1's ⬜ 4 closure is true of the code | `tests/test_the_fixes_close_the_record.py#one_finding_inside_one_earlier_unit` | verified | Read: the fixture asserts `fields(text)["New units"] == "alpha (depth 1)"` at line 1404 before returning, and the case asserts the same equality on the same cell with nothing between them writing it |
| 🟢 | round 1's ⬜ 3 and ⬜ 5 closures stand in the records | `seal/specs/1789455558-…/overview.md`, `seal/specs/1789455558-…/changelog.md` | verified | Read, not re-measured: the divergence table carries the A5 row with 48 of 124 and 65, and the changelog carries the symmetric strip's one cost with the rendering shown and the condition that makes it visible |
| ❓ | the broad gate — the full suite, the repository-wide lint, the typecheck | `seal/config.md` | out of verified scope | `agent-contract` §2 assigns it to `agents/sealer.md`, once, after the rounds settle. It has not run. Answered by the orchestrating session's sealer spawn, which ① makes due only after the fix lands |

## Paste-ready fixes

```python
def test_flat_is_what_folds_the_seam_and_it_folds_python_only():
    """The two cases above call `LITERAL_SEAM.sub` and neither calls `flat`,
    so nothing in this module holds the repair round 1's 🟡 2 asked for.
    Round 2 measured it: with `flat` back to `" ".join(read(*parts).split())`
    all seventeen cases here stay green and 🟡 2 is open again with the suite
    saying nothing -- which is #406's hole with a different lid on it.

    Red with the fold removed: the first assertion fails, because the source
    reads `... cannot see. The " "sealer's mark ...`.
    Red with the `.py` guard dropped: the third fails, because `README.md` is
    a swept file carrying a shell command whose two quoted arguments are not
    a seam and would be cut together.
    """
    joined = "The sealer's mark names a commit"
    assert joined in flat("skills", "code-review", "scripts", "round_record.py"), (
        "`flat` no longer reads across a string-literal seam, so the sweep "
        "below is blind to an instance split over two literals again"
    )
    assert joined not in " ".join(
        read("skills", "code-review", "scripts", "round_record.py").split()
    ), "the seam this pins has been rewrapped; point it at another one"
    assert '--git-common-dir)/seal" "$(git' in flat("README.md"), (
        "`flat` folded a markdown file, which has no literals to join -- the "
        "cut lands inside a shell command a reader copies"
    )
```
```python
# Folding the seam here keeps ONE implementation of the rule reading two kinds
# of input, which is what that work item's alternatives table rejected a second
# check in favour of. **The error direction is safe for the phrases these
# sweeps look for, and that is narrower than "can only create a hit"**: the
# prefix class sits BETWEEN the two quotes, so a literal whose whole content is
# one or two of those letters is deleted rather than joined -- `seal_stamp.py`
# loses its `GOLD` key `"R"` and `test_session_cost.py` loses `call("b", ...)`.
# A deletion can only ever join its neighbours, and every phrase swept below is
# quote-free, so no swept phrase can be cut in half. Two shapes the fold does
# NOT reach, for the same reason it is cheap: a seam between literals of
# DIFFERENT quote characters, which `\1` refuses, and a seam where both
# literals carry the space, which Python itself joins to a double space.
# Applied to `.py` members only, because a markdown file has no literals to
# join and a fold there would cut through quoted shell commands.
```
```python
    return (
        "`Pass` is checked, and this row is read as open because one of its "
        "cells carries a blocking marker, while its own verdict reads "
        f"`{verdict or 'empty'}` — not one of the words that close a row: "
        f"{named}. Nothing here says the finding was closed, and a verdict "
        "counted as closed without being one of those words is the tolerant "
        "read this file exists to refuse. Write one of those words, drop the "
        f"marker, or leave `Pass` unchecked: {what}"
    )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test`'s four touched modules in the clone at `3b45bde8` — `test_one_word_one_meaning.py`, `test_chain_check_at_the_pull_request.py`, `test_the_seal_is_taken_once_by_the_sealer.py`, `test_the_fixes_close_the_record.py` | 266 passed, exit 0 read directly |
| `flat` reverted to `" ".join(read(*parts).split())`, module re-run | 17 passed, exit 0 — the fold is held by nothing (🟡 1) |
| `flat`'s `.endswith(".py")` guard dropped, module re-run | 17 passed, exit 0 — the guard is held by nothing (🟡 1) |
| the proposed case, on the tree as shipped and under each of those two mutations | exit 0, then exit 1 and exit 1 |
| mutation C — pinned spelling kept, a second anonymous instance added across two adjacent literals in `round_record.py#seal` | sweep **exit 1** — round 1's surviving mutation is dead |
| the broad-gate refusal reverted to *The seal names a commit this repository holds* | sweep **exit 1** — the fold reaches the live defect it found |
| an anonymous instance in a single literal | sweep **exit 1** — pre-fold coverage intact |
| `LITERAL_SEAM` against `tokenize` over the four swept `.py` files | 130 real adjacent-literal joins in `round_record.py` against 462 regex folds; 0 against 301 in `test_session_cost.py` |
| `LITERAL_SEAM.sub` on `open(p, "rb")`, `sep = "b"`, `GOLD = { "D": …, "R": … }` | the literal is deleted, not joined (⬜ 2) |
| `open_blocking`'s selection and `open_row_reason` on three rows whose marker is outside the `#` cell | all three reach the second arm and are told an earlier round opened it (⬜ 3) |
| `open_row_reason`'s second arm reverted to its pre-fix sentence, the six chain-check cases re-run | 3 failed, 3 passed — the new `open` case is load-bearing |
| the selection widened to drop `BLOCKING in "".join(seen)`, the same six re-run | 1 failed — `test_the_same_open_row_without_the_quote_is_a_pass` alone |
| `raise` sites counted by `ast` in `round_record.py#seal` and `#reach_forward` | 6 and 3, against S6's **six** and the corrected row's **three** |
| `bin/evidence-check --strict .` in the clone, exit read directly | exit 0 — 1276 ok · 0 drifted · 0 broken · 0 external, records arm 0 refused |
| `uvx ruff format --check` on the six Python files the fix range touched | 6 files already formatted, exit 0 |
| `chain_check.py --baseline origin/release/v0.12.0` in the clone | exit 1 on the two expected rows — `Broad gate` is `not yet`, and `Fixes checked by` reads `nobody`, which this round exists to change |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet** — it has not been run, by this round or by anything before it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/chain_check.py#open_row_reason` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | round 1's 🟡 2 — fixed |
| round-1 | `seal/specs/1789455558-…/spec.md` §A5 | round 1's ⬜ 3 — answered |
| round-1 | `tests/test_the_fixes_close_the_record.py#test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#fix_table` | round 1's ⬜ 5 — answered |
| round-1 | `seal/ledger.md` at `release/v0.12.0:2204`, superseded by `seal/ledger/1789455558-….md:13` | round 1's ⬜ 6 — answered |
| round-1 | `seal/ledger.md:2201` | round 1's ⬜ 7 — answered |
| round-1 | `skills/code-review/scripts/round_record.py#close`, `#inherited_rows` | round 1's 🟢 — verified |
| round-1 | `skills/code-review/scripts/round_record.py#reach_forward` | round 1's 🟢 — verified |
| round-1 | `seal/ledger.md`, `seal/ledger/1789455558-….md` | round 1's 🟢 — verified |
| round-1 | `seal/config.md` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
