# Round 2 — the verifying round, against the diff of round 1's fixes

Target: `f41927ff..3b45bde8` on
`fix/404-405-406-407-408-414-the-record-chain-disagrees-with-itself-in-five-places`,
pull request 416, draft. HEAD confirmed at `3b45bde8` with a clean tree; it has
not moved. Everything below was read or run in a `git clone --no-local` of this
repository at that commit.

## How the four things this round found fit together

Both of round 1's numbered findings are repaired and both repairs work. What
the round found sits one level under each of them, in the same place both
times — **the repair does more than anything now holds it to.**

```
🟡 2  the sweep could not see a seam
        ↓ repaired: `flat` folds it, and the fold found a live instance
      ① nothing in the module holds the fold — delete it and all 17 cases pass
      ② the comment under it states an invariant the pattern does not have

🟡 1  the refusal blamed a word that was correct
        ↓ repaired: the second arm names the quote, and the selection is unchanged
      ③ the sentence says the quote belongs to an earlier round, which it need not
      ④ one clause later it still calls that same word an unrecognised verdict
```

Only ① needs a fix. ②③④ are wording, and the fix for ① is where ② belongs.

---

## ① 🟡 2 is repaired, and deleting the repair leaves every case green

`tests/test_one_word_one_meaning.py#flat` folds a string-literal seam for the
`.py` members of both sweeps. The fold works, and it found the live instance the
fix pass reported. Both of those are confirmed below.

What holds it is nothing. `test_the_sweep_reads_across_a_string_literal_seam`
and `test_folding_the_seam_cannot_hide_an_instance_it_would_have_found` both
call `LITERAL_SEAM.sub` directly and neither calls `flat`, so the fold can leave
`flat` without the suite noticing.

Executed, in the clone at `3b45bde8`:

| `flat` mutated to | `tests/test_one_word_one_meaning.py` |
|---|---|
| the pre-fix body, `" ".join(read(*parts).split())` | **17 passed, exit 0** |
| the `.endswith(".py")` guard dropped, every file folded | **17 passed, exit 0** |

The first row is round 1's 🟡 2 restored with the suite silent about it. That is
the shape this branch exists to close, and it is the second time this exact
coverage has gone missing on this work item — #406 removed an output assertion
and left the same hole, which is what 🟡 2 was.

The second row matters less but is real: `README.md` is a `SEAL_SWEPT` member
and carries a shell command whose two quoted arguments would be cut together if
markdown were ever folded.

The fix is one case in the file the fix pass already touched. It is in
`## Paste-ready fixes`, and it was run: green on the tree as shipped, red under
each of the two mutations above.

## ② And the invariant the fold states is not the one the pattern has

`tests/test_one_word_one_meaning.py#LITERAL_SEAM`'s comment says:

> **The error direction is the safe one**: a seam folded where Python would NOT
> have joined can only create a hit, never hide one — `" ".join(x)` folds to
> `.join(x)`, which no sweep matches.

The pattern is `([\"'])\s*(?:[fFrRbBuU]{0,2})\1`, and the prefix class sits
*between* the two quotes. So a whole short literal made only of those letters
matches, and is removed rather than joined. Measured on the swept files:

| Source | Python keeps | The fold leaves |
|---|---|---|
| `GOLD = { "D": (…), "R": (…) }` in `seal_stamp.py` | the `"R"` key | `{ "D": (…), : (…) }` |
| `call("b", 15, 23, …)` in `test_session_cost.py` | the `"b"` argument | `call(, 15, 23, …)` |
| `open(p, "rb")` | the mode | `open(p, )` |

That is a deletion, and the sentence says deletion cannot happen. Nothing is
hidden today, because every phrase these two sweeps look for is quote-free and
removing a quoted run can only join its neighbours — but that is a different
guarantee, and it is the one the comment should be making.

`test_folding_the_seam_cannot_hide_an_instance_it_would_have_found` carries the
same gap. Its name claims a universal property; its body asserts that one
source folds to something no sweep matches and that two others survive. It
cannot fail for the reason its name gives.

The narrow version of the same over-claim is in the ledger. `seal/ledger.md`
row 2203 reads *an anonymous instance split over two adjacent literals is
caught*. It is caught when both literals use the same quote character. The
pattern requires `\1`, so `"…the " '…seal…'` is still invisible — latent here
only because this repository formats with ruff and ruff normalizes quotes.

## ③ 🟡 1 is repaired, and its new sentence names a round that need not exist

`skills/code-review/scripts/chain_check.py#open_row_reason`'s second arm no
longer says the verdict word is outside a vocabulary, and the selection in
`open_blocking` is byte-for-byte unchanged — both confirmed by mutation below.
The rule the new sentence states is a rule the file holds: a row is refused
when a blocking marker appears in it and its verdict is not a closing word, and
`not one of the words that close a row` is exactly true of `open`.

What is not true of every row is the clause before it. The arm fires whenever
the marker is in any cell **but** the `#` cell, and the message says that cell
*quotes a blocking finding an earlier round opened*. Executed against the real
selection, three rows reach the arm and get that sentence:

| The row | Where the marker is | Is it an earlier round's finding? |
|---|---|---|
| `OPEN_ROW_QUOTING_A_BLOCKER`, the fix's own fixture in a `round-1.md` | Grounds: *round 1 opened this as … 2* | no — it is round 1's, in round 1's record |
| a finding whose text describes the refusal printing a marker | Finding | no — it is this round's own |
| a finding whose Location names a spec section about such a row | Location | no — it is not a finding at all |

The remedy the message offers still works in all three, so a reader is not sent
to change something correct — which is what separated this from 🟡 1's own
defect. It is the subordinate clause that is wrong, and the arm's docstring
rests its design on it: *the 🔴 in such a row belongs to a round that is over*.
Dropping four words settles it.

## ④ And one clause later it still calls that word an unrecognised verdict

The same sentence ends: *an unrecognised verdict counted as closed is the
tolerant read this file exists to refuse*. `open` is the word
`agents/warden.md` prescribes, and round 1's 🟡 1 was that the arm told its
author the word was not recognised. The phrase `outside the vocabulary` is
gone and the proposition it carried is still in the message, one clause down.

As a statement about the class of verdicts it is true, which is why this is a
correction and not a defect. It reads badly to the one author it is addressed
to.

---

## The three things the fix pass reported, opened rather than trusted

**The fold reaches the live defect, and mutation C is dead.** Executed, three
mutations of `skills/code-review/scripts/round_record.py#seal` against
`test_no_instructing_document_leaves_an_instance_anonymous`:

| Mutation | Before the fix | Now |
|---|---|---|
| round 1's mutation C — pinned spelling kept, a second anonymous instance added across two literals | green (the defect) | **exit 1** |
| the broad-gate refusal reverted to its shipped wording, *The seal names a commit this repository holds* | green | **exit 1** |
| an anonymous instance in a single literal — the coverage that already worked | red | **exit 1** |

The repair itself stands: `round_record.py` now carries three mentions of the
word and all three name whose — `the sealer's one write`, `before the sealer
runs`, `The sealer's mark names a commit`. No bare instance is left in the
module.

**The restored ledger row is true, and the two files do not say it twice.**
`seal/ledger.md:2203` is back with clause (b) rewritten. Clause (a) — that the
refusal names the subcommand in both sentences that left the instance anonymous
— is true at this SHA. The fragment's row 5
(`seal/ledger/1789455558-….md:13`) claims something else: which check holds the
rule, and which module-local pins remain. Its Notes now say the shared row is
restored rather than superseded. Read, not executed.

**The eight re-stamped anchors were read, not just refreshed.** Two
enumerations in the affected rows could have gone stale the way round 1's ⬜ 7
did, and both are correct at this SHA:

| Row | Claims | Counted |
|---|---|---|
| `seal/ledger.md:1945` (S6) | `seal` holds **six** `raise Refused` sites | 6 |
| `seal/ledger.md:2201` | `reach_forward` has **three** refusals, *counted rather than described* | 3 |

`seal/ledger.md:2201` is ⬜ 7's own repair, and it is the row that now carries
the guard S6 asks for. `bin/evidence-check --strict .` reads exit 0 in the
clone — 1276 ok, 0 drifted, 0 broken, records arm 0 refused.

## The seven new units, judged as code rather than as fixes

Five are sound. `QUOTED_SENTENCE` and `OPEN_ROW_QUOTING_A_BLOCKER` are
discriminators the three existing cases now find their line by, and
`test_a_row_reading_open_is_not_told_its_word_is_unrecognised` and
`test_the_same_open_row_without_the_quote_is_a_pass` are a case and its control
that differ in the quote and nothing else. Both were seen red here, not taken
on the docstring's word:

| Mutation of `chain_check.py` | What went red |
|---|---|
| the second arm reverted to its pre-fix sentence | the two rewritten cases **and** the new `open` case — 3 failed |
| the selection widened so the quote is no longer required | the new control alone — 1 failed |

The other two are ① and ② above.

## Round 1's four answered corrections

⬜ 3, ⬜ 5 read and standing: `overview.md` carries the A5 divergence row with
both figures, and `changelog.md` carries the symmetric strip's one cost with
the rendering shown. Neither was re-measured this round.

⬜ 4 verified: `one_finding_inside_one_earlier_unit` asserts
`fields(text)["New units"] == "alpha (depth 1)"` before it returns, and
`test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one` asserts
the same equality on the same cell with nothing between them writing it. The
corrected comment is true.

⬜ 6 and ⬜ 7 verified above.

## Whether ① is worth the one reopening left

It is. The fix is one case in a file the fix pass already opened, it is written
out below, and it was run green on the tree and red under both mutations. An
issue would carry the same risk this work item has already paid for once: the
hole #406 left is the hole 🟡 2 found, and the hole ① describes is that hole
with a different lid on it. Nothing here loses a record or crashes, so the run
ends on ① either way — the question is only whether the fold ships held or
unheld.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the seam fold is held by no case — reverting `flat` to its pre-fix body leaves all 17 cases in the module green, and round 1's 🟡 2 is open again with the suite silent | `tests/test_one_word_one_meaning.py#flat` | open | Executed in the clone at `3b45bde8`: `flat` back to `" ".join(read(*parts).split())` → 17 passed, exit 0; the `.endswith(".py")` guard dropped → 17 passed, exit 0. Both new cases call `LITERAL_SEAM.sub` and neither calls `flat`. The proposed case is green as shipped and red under each mutation |
| ⬜ 2 | the fold's comment claims a folded seam *can only create a hit, never hide one*; the prefix class sits between the quotes, so a short literal is deleted rather than joined, and the case named for the claim asserts three examples instead | `tests/test_one_word_one_meaning.py#LITERAL_SEAM` | open | Executed: `seal_stamp.py`'s `GOLD` dict loses its `"R"` key and `test_session_cost.py` loses `call("b", …)`, both swept files; `open(p, "rb")` → `open(p, )`. Nothing is hidden today because every swept phrase is quote-free. `seal/ledger.md:2203` carries the narrow form of the same over-claim: a mixed-quote seam is still invisible, since the pattern requires `\1` |
| ⬜ 3 | the second arm tells every row it fires on that a cell *quotes a blocking finding an earlier round opened*; the selection routes rows whose marker is this round's own, or is in the Finding or Location cell and quotes no finding at all | `skills/code-review/scripts/chain_check.py#open_row_reason` | open | Executed against the real selection: three rows reach the arm and get that sentence, including the fix's own `OPEN_ROW_QUOTING_A_BLOCKER` fixture, which sits in a `round-1.md` and says round 1 opened it. The remedy offered still works in all three, so the clause misattributes rather than misdirects — but the docstring rests the arm's silence about the marker on that premise |
| ⬜ 4 | the same sentence still calls the author's verdict *an unrecognised verdict*, one clause after dropping *outside the vocabulary* for saying that about `open` | `skills/code-review/scripts/chain_check.py#open_row_reason` | open | Read: the message ends *an unrecognised verdict counted as closed is the tolerant read this file exists to refuse*. True of the class, and `open` is the word `agents/warden.md` prescribes. The clause before it, `not one of the words that close a row`, is the accurate spelling and is already there |
| 🟢 | round 1's 🟡 1 is repaired: the selection is unchanged and both new cases are load-bearing | `skills/code-review/scripts/chain_check.py#open_blocking`, `#open_row_reason` | verified | Executed, two mutations killed: the arm reverted to its pre-fix sentence turns 3 cases red including the new `open` case; the selection widened so the quote is not required turns the new control red alone. `open_blocking` is unchanged in the fix range |
| 🟢 | round 1's 🟡 2 is repaired: mutation C is dead, the live instance is reachable, and single-literal coverage is intact | `skills/code-review/scripts/round_record.py#seal`, `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | verified | Executed, three mutations, all exit 1: the seam-split second instance, the broad-gate refusal reverted to its shipped wording, and a single-literal instance. Read: `round_record.py` holds three mentions of the word and all three name whose |
| 🟢 | the removed `seal/ledger.md` row is restored and true, and the fragment does not claim the same thing | `seal/ledger.md:2203`, `seal/ledger/1789455558-the-record-chain-disagrees-with-itself-in-five-places.md:13` | verified | Read: clause (a) holds — the refusal names the subcommand in both sentences and the module carries no bare instance. The fragment's row 5 claims which check holds the rule and which pins remain, which is a different clause, and its Notes now say the shared row is restored rather than superseded |
| 🟢 | the re-stamped anchors were read, not just refreshed | `seal/ledger.md:1945`, `seal/ledger.md:2201` | verified | Executed: `seal` holds 6 `raise Refused` sites against S6's **six**, and `reach_forward` holds 3 against the corrected row's **three**. `bin/evidence-check --strict .` exit 0 read directly — 1276 ok · 0 drifted · 0 broken, records arm 0 refused |
| 🟢 | round 1's ⬜ 4 closure is true of the code | `tests/test_the_fixes_close_the_record.py#one_finding_inside_one_earlier_unit` | verified | Read: the fixture asserts `fields(text)["New units"] == "alpha (depth 1)"` at line 1404 before returning, and the case asserts the same equality on the same cell with nothing between them writing it |
| 🟢 | round 1's ⬜ 3 and ⬜ 5 closures stand in the records | `seal/specs/1789455558-…/overview.md`, `seal/specs/1789455558-…/changelog.md` | verified | Read, not re-measured: the divergence table carries the A5 row with 48 of 124 and 65, and the changelog carries the symmetric strip's one cost with the rendering shown and the condition that makes it visible |
| ❓ | the broad gate — the full suite, the repository-wide lint, the typecheck | `seal/config.md` | out of verified scope | `agent-contract` §2 assigns it to `agents/sealer.md`, once, after the rounds settle. It has not run. Answered by the orchestrating session's sealer spawn, which ① makes due only after the fix lands |

## Paste-ready fixes

For 🟡 1 — the case that holds the fold. It goes at the foot of
`tests/test_one_word_one_meaning.py`, under the two cases the fix pass added.
<!-- NAME NOT IN TREE: the case below is proposed, so its name is not in the
tree yet; it is named only inside the fence. -->

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

For ⬜ 2 — the invariant, stated as the one the pattern has. It replaces the
paragraph beginning *Folding the seam here keeps ONE implementation*.

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

For ⬜ 3 and ⬜ 4 — the second arm's sentence. The clause the selection cannot
guarantee comes out, and the class statement stops being aimed at the row.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1, the seam fold that no case holds
Loses a record or crashes: no

⬜ 2, ⬜ 3 and ⬜ 4 are wording, and ⬜ 2 belongs in the same commit as 🟡 1.

## Proof block

Opened in the clone at `3b45bde8`: `skills/code-review/scripts/chain_check.py`,
`skills/code-review/scripts/round_record.py`,
`tests/test_one_word_one_meaning.py`,
`tests/test_chain_check_at_the_pull_request.py`,
`tests/test_the_fixes_close_the_record.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`skills/verify/scripts/seal_stamp.py`, `skills/verify/scripts/session_cost.py`,
`tests/test_session_cost.py`, `README.md`, `ruff.toml`, `bin/test`,
`seal/ledger.md`,
`seal/ledger/1789455558-the-record-chain-disagrees-with-itself-in-five-places.md`,
and under `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/`:
`rounds/round-1.md`, `rounds/round-1-fixes.md`, `overview.md`, `changelog.md`,
`survivors.md`, `phases/phase-5.md`.

Probes: three `test_tmp_*` files in the clone, all deleted; the clone itself is
under the session scratchpad and holds no branch, worktree or stash. Every file
it mutated was restored in a `finally`, and `git status` is clean in both the
clone and this repository.
