# Round 1 — the record chain disagrees with itself in five places

Target SHA `4a5a32cf`, confirmed as the branch head with a clean working tree
when this round started. Reviewed in a `git clone --no-local` at that SHA; the
probes below ran there and nothing was left behind.

## What this round found, in one picture

The branch's own records are unusually self-critical, and most of what a
reviewer would reach for is already written down in `phases/phase-N.md`. So
this round spent its budget on the one thing those records cannot do — testing
the claims they make about coverage.

```
the repairs themselves
  ├─ #404  first-wins on both sides        → verified, and the two readers
  │                                          checked one level down: clean
  ├─ #405  the accounting                  → measurement reproduced exactly
  ├─ #414  the two cut sites               → verified; one disclosed cost
  ├─ #407  the fixture guards              → verified
  └─ #406  the deleted pin                 → COVERAGE LOST (🟡 2)

the message the repair writes
  └─ #408  the second arm                  → names the wrong cause (🟡 1)

the paperwork the repairs moved
  ├─ the removed shared-ledger row          → half its claim went with it (⬜ 6)
  └─ the fifteen re-stamped anchors         → one enumeration grew a member
                                              and nobody re-read it (⬜ 7)
```

Two findings need an answer, and both are the work item's own shape one level
down: a reader that answers about the wrong thing and says nothing about it.
Two more are corrections to the run's own records, which commission nothing.

---

## 🟡 1 — The second refusal arm blames the verdict word, and the word it blames can be `open`

`skills/code-review/scripts/chain_check.py#open_row_reason`, the `else` branch
(the arm added at `cb38e54`).

#408 split one message into two and left the selection alone. The split is
keyed on `BLOCKING in seen[0]` — whether the row's own `#` cell carries a 🔴 —
but the *selection* is still `BLOCKING in "".join(seen)`, a 🔴 anywhere in the
row. So the second arm fires on rows that were selected by something it never
mentions, and it explains them with a rule the file does not enforce.

**What the reader is told.** Executed, calling `open_row_reason` directly:

```
`Pass` is checked, and this row's verdict reads `open`, which is outside the
vocabulary — `agreed, fixed`, `answered`, `deferred`, `fixed`, `not a defect`,
`out of verified scope`, `withdrawn`. Nothing here says the finding was closed,
and an unrecognised verdict counted as closed is the tolerant read this file
exists to refuse. Write one of those words, or leave `Pass` unchecked: 🟡 3
```

`open` is the word `agents/warden.md` prescribes for a finding this round
opened, and this same file's first arm prints it back as
`` this 🔴 row reads `open` ``. One run, one word, two explanations.

**Why a reader meets it.** In
`tests/test_chain_check_at_the_pull_request.py`,
`test_a_checked_pass_beside_an_open_NON_blocking_finding_passes` pins a 🟡 row
reading `open` beside a checked `Pass` as a **pass**. Add to that row's Grounds
the thing a verifying round is asked to write — a quote of an earlier round's
🔴 — and the row flips from pass to refusal, and the refusal blames the word.
Executed, `open_blocking` on that row returns `[(5, '🟡 3', 'open', False)]`:
selected, and routed to the second arm.

**The second half: the rule the arm states is not the rule the file holds.**
The arm says *an unrecognised verdict counted as closed is the tolerant read
this file exists to refuse*. Executed: a row whose `#` cell reads 🟢, whose
verdict reads `verified`, and which quotes no 🔴 anywhere returns `[]` from
`open_blocking` — not refused at all. `check_round` has exactly one
verdict-related check and that is it. So the same word passes on the row above
and is refused on the row below, and the difference is the quote the message
never names. `test_a_verdict_word_it_does_not_recognise_counts_as_open` looks
like it covers this and does not: its fixture uses the default `finding="🔴 1"`,
so the row carries a 🔴 in its `#` cell.

**Why it matters.** A reader stopped by this arm has two ways out — change the
word, or drop the quote — and the message names one of them while asserting a
general rule about the other. That is #408's own complaint, moved one cell
over: the sentence sends the reader somewhere the cause is not.

## 🟡 2 — Deleting the output pin lost coverage the sweep cannot replace, and a mutation survives to prove it

`tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous`,
with the deletion at `tests/test_the_seal_is_taken_once_by_the_sealer.py`
(`test_the_refusal_says_which_value_the_last_record_may_hold`, commit `f119f72`).

The branch states the claim flatly in three places — `phases/phase-5.md`
(*"The deletion loses no coverage"*), the case's own new docstring (*"nothing is
uncovered by the deletion"*), and row 5 of
`seal/ledger/1789455558-….md` (*"Deleting it loses no coverage"*). The grounds
are that `SEAL_SWEPT` lists `skills/code-review/scripts/round_record.py`, so the
sweep reads the refusal's sentence.

The sweep reads that module's **source text**, flattened by
`" ".join(read(*parts).split())`. The deleted assertion read the run's
**output**. Python joins adjacent string literals at parse time and `flat` does
not, so a phrase split across two literals is in the output and not in the
flattened source.

**Executed — three mutations of the same sentence at
`round_record.py#seal`:**

| Mutation | `test_one_word_one_meaning.py` | What the output says |
|---|---|---|
| A — `before the seal is taken`, one literal | **red**, naming the module and quoting the span | anonymous |
| B — the same words, split as `"before the "` `"seal is taken"` | **green** | anonymous |
| C — keep `before the sealer runs`, add `"so the "` `"seal covers this round too"` | **green**, and the seal module green too — **86 passed** | anonymous |

Mutation A is phase 5's own red-first and it reproduces exactly. Mutation C is
the one that matters: both modules pass while the refusal a person reads
carries a bare, anonymous `the seal`. Before `f119f72`,
`assert "the seal" not in out` caught it.

**What survives and what went.**

- **Kept** — an anonymous seal written inside a single string literal, anywhere
  in the two `.py` members of `SEAL_SWEPT`.
- **Lost** — an anonymous seal whose phrase straddles an implicit
  concatenation. That is not an exotic shape: every long refusal in
  `round_record.py` is built from wrapped literals, and where the wrap falls is
  decided by line length.
- **To restore it** — fold the literal seam inside `flat` for `.py` members.
  That is one implementation reading two inputs, which is what the plan's
  rejection of the alternative asked for (*"two checks then claim one rule with
  two implementations"*), rather than a second check.

`CLAUDE.md` §*a thing more than one party can have is named with whose* names
this sweep as the check that holds the rule, so the gap is in the check the
repository points at.

## ⬜ 3 — `spec.md` A5's "Then" does not hold on the corpus, and no divergence row says so

`seal/specs/1789455558-…/spec.md`, scenario A5.

A5 reads: *Given every committed `round-N.md` pair in `seal/specs/`, when the
new accounting predicate is applied, then **no pair is unaccounted***.

Executed, re-measuring independently against the shipped predicate rather than
reading the figure (`agent-contract` §5 — an aggregate is not a coordinate).
My numbers reproduce the branch's exactly:

| Shape | Pairs |
|---|---|
| stopped by the standing *coordinate the table lacks* refusal | 15 |
| `filled > 0`, every coordinate accounted — silent | 74 |
| `filled > 0`, some unaccounted — refused by the unconditional rule alone | 2 |
| `filled == 0`, some unaccounted — **refused by the shipped rule** | 48 |
| `filled == 0`, every coordinate accounted | 0 |

So 48 of 124 readable pairs are unaccounted under the predicate that shipped,
and 65 under the one A5 was written about. A5's "Then" is false either way.

**The decision it was meant to gate was still made correctly**, which is why
this is a correction and not a defect. The 2-pair discriminator is what chose
`filled == 0`, and I checked phase 2's explanation for the 48 rather than
taking it: every refused pair belongs to a work item id between `1788212517`
and `1788501054`, and their sections are in a different spelling entirely —
`| From | Coordinate | Why it is still worth opening |`, with `| rounds 12–15 |`
in the first cell. They predate the generator, and nobody re-runs `close`
against a merged record.

What is missing is the paperwork: `overview.md`'s divergence table names
`plan.md` §*Operational impact*, `spec.md` A7 and the ledger, and does not name
A5. A reader checking the acceptance scenarios finds one whose "Then" is false
with no row admitting it.

## ⬜ 4 — #407's case-level positive assertion cannot fire in the state it names

`tests/test_the_fixes_close_the_record.py#test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one`.

The assertion added there reads round-1.md's `New units` cell and requires
`alpha (depth 1)`. The fixture it calls,
`one_finding_inside_one_earlier_unit`, gained a guard in the **same commit**
asserting the same equality on the same content, and nothing between the two
touches that cell. So in the defect state #407 names — a substitution that
misses — the fixture fires first and the case assertion is never reached.

`phases/phase-6.md` records this in as many words: *"The second mutation only
proves anything applied INSIDE the case. Round 1 has to be renamed to `none`
**after the fixture returns**… Applied inside the fixture, the guard fires
first and the case is never reached."*

So A12 is met by its letter and the vacuity is genuinely closed — by the
fixture guard. The case-level assertion is a duplicate of it. Recorded so a
later reader does not take the case as asserting the judgment it is named for;
phase 6 is clear that nothing in `close`'s output can.

## ⬜ 5 — The symmetric strip drops a sentence-final stop, and the Grounds cell decides whether anyone sees it

`skills/code-review/scripts/round_record.py#fix_table`, both widened cuts
(`chain.SEPARATORS + "."`).

`strip` takes both ends, so a note that ends in a full stop loses it.
`phases/phase-3.md` records the cost and argues the trade — a one-sided strip
would spell the two members differently from their three neighbours.

What the record does not say is when it is visible. `close` renders
`grounds + ("; " + old if old else "")`, so the note is mid-sentence whenever
the reviewer wrote a Grounds cell, and sentence-final only when that cell is
empty. Executed, with an empty Grounds cell and a third cell of
`` `<sha>`. it reads the cell now. ``:

```
fixed at 1cf3cac — it reads the cell now
```

Small, and disclosed. Noted because the disclosure lives only in
`phase-3.md`: neither `overview.md`'s divergence table nor `changelog.md`
mentions it, and `changelog.md` is what a release reader opens.

## ⬜ 6 — The shared-ledger row was removed wider than the clause that went false, and half its claim is now claimed by nobody

`seal/ledger.md` at `release/v0.12.0:2204`, removed at `3194525e`; the
superseding row is `seal/ledger/1789455558-….md:13`.

The removed row carried two clauses joined by *and*:

- **(a)** *`seal`'s last-record refusal names the subcommand rather than reading
  `the seal`, in both of the sentences that left the instance anonymous* —
  **still true.** `round_record.py:4060` reads *the only value `seal` accepts*
  and `:4064` reads *`seal` runs with `Pass` ticked*, and both positive pins on
  them survive in the case.
- **(b)** *and the case that pins it asserts the whole output holds no bare
  `the seal`* — **false**, which is what #406 deleted and what the branch's
  grounds name.

No anchor was removed. `round_record.py#seal` moved `626b7dfa → a55302cd` and
the case moved `44b07904 → 593d53be`; the sweep's own anchor, at hash
`981c6b9c`, did not move at all. So `CLAUDE.md`'s *a row whose
anchor a change removes is REMOVED* does not reach this row, and
§*a change writes fragments* compels touching the shared file — not deleting
the whole row.

**The file's own two precedents point the other way**, and one of them states
the criterion: `seal/ledger.md:1951` (S13) — *"The clause is corrected in place
rather than the row removed, because the capped-run claim is the row's subject
and is untouched"*. Here the subject is (a) and it is untouched.

`grep` for the clause returns **0** in `seal/ledger.md` and **0** in the
fragment. The fragment's row 5 claims the arrangement of the checks — one
owner, two positive pins remaining, the new exit naming the sealer — and not
the code's own text. Restoring it costs one sentence and no code.

## ⬜ 7 — A row enumerating two refusals now stands over a function with three, and the re-verify re-stamped it silently

`seal/ledger.md:2201`, citing `round_record.py#reach_forward`.

Its clause reads *"It refuses rather than guesses where the table is unreadable
or a coordinate names no row, and says nothing where round N+1 does not
exist"*. Phase 2 added a third refusal at `round_record.py:1591` — the
unaccounted-coordinates arm. The enumeration is now two of three.

I am calling it incomplete rather than false: unlike S6, this row is not marked
*counted rather than described*, so it may have been a list of examples.

**What makes it worth a row of its own is that this repository already wrote
the failure mode down.** `seal/ledger.md:1945` (S6), one work item ago:

> The claim above was corrected by re-reading `#seal` rather than by
> re-stamping it — **a re-stamp recomputes a hash and reads nothing, so a row
> enumerating three refusals over a function that now has two would have passed
> silently.**

That is this row, with the numbers the other way round. `--reverify` moved its
hash, `--strict` now reads exit 0, and nothing asked whether the enumeration
still closed. `phases/phase-7.md` says thirteen rows were re-read and twelve
held; this is one of the thirteen, and the re-read did not catch that its list
had grown a member.

One more thing the same act obscured: `overview.md`'s *Not verified* table says
`--reverify` *"refreshed 15 rows"*. Twelve rows changed; fifteen anchor stamps
inside them did, because `:2198`, `:2201` and `:2202` carry two each.

---

## What I confirmed

Separated from the findings above on purpose, and separated again by whether I
ran it or read it.

**Executed.**

- **#404 holds, and the two sides agree on more than the plan claims for them.**
  `inherited_rows` skips a `Location` already emitted; `close` now uses
  `setdefault`. I then tested the claim *"the two now agree BY CONSTRUCTION"*
  one level down, where the two sides use **different cell readers** —
  `split_row` in `inherited_rows` against `row_cells` in `close`. On a raw row
  the two do disagree (`'b` helper drops b'` against `` '`mod.py#helper`' ``),
  so the hypothesis was worth testing. It is refuted: `table_of` re-serialises
  every row through `copied_row` before `inherited_rows` sees it, so the
  escaping is already done. A pipe inside a code span in the Finding cell and a
  pipe inside the Location cell both round-trip to exit 0.
- **#405's measurement reproduces exactly** — the table in ⬜ 3, computed from
  the shipped predicate against the committed corpus.
- **#406's red-first reproduces** — mutation A above, red with the module named
  and the span quoted.
- **The four touched modules and the fixes module are green at this SHA** —
  `test_the_fixes_close_the_record.py` 82 passed; the four others 299 passed;
  `test_no_real_identifiers.py` and `test_the_rules_have_one_owner.py` 56
  passed. These are narrow module runs, not the gate.
- **`bin/evidence-check --strict .` is exit 0** — `1274 ok · 0 drifted ·
  0 broken`, and the records arm `0 refused`. `overview.md`'s claim about the
  re-verify checks out.

**Read, not executed.**

- The `reach_forward` refusal's text is pinned by
  `test_a_truncated_inherited_table_is_refused_naming_what_it_no_longer_holds`,
  and the `chain_check` arms by three cases — §14 is met for all three changed
  messages.
- The narrowing that shipped (a table that lost some rows but kept one of round
  N's still passes) is what the code does: the accounting sits inside
  `if not filled`. It matches `overview.md`'s first divergence row and is
  narrower than `spec.md`'s *Data & interfaces* row, which is what that
  divergence row exists to say.

## What I did not judge

- **The broad gate.** `agent-contract` §2 assigns the full suite, the
  repository-wide lint and the typecheck to `agents/sealer.md`, once, after the
  rounds settle. Not run here, and nothing above should be read as standing in
  for it. It has **not** come due: this round leaves two findings open.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the second refusal arm blames the verdict word, and the word can be `open`; the vocabulary rule it states is not the rule the file enforces | `skills/code-review/scripts/chain_check.py#open_row_reason` | open | Executed: `open_row_reason("🟡 3", "open", False)` returns the *outside the vocabulary* sentence; `open_blocking` selects that row as `(5, '🟡 3', 'open', False)`; a 🟢/`verified` row quoting no 🔴 returns `[]`. Read: `check_round` holds one verdict check; `test_a_checked_pass_beside_an_open_NON_blocking_finding_passes` pins the open 🟡 as a pass |
| 🟡 2 | the sweep cannot see a bare `the seal` split across two adjacent string literals, so #406's *nothing is uncovered* is false | `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | open | Executed: three mutations of `round_record.py#seal`. One literal → sweep red. The same words across two literals → green. The pinned spelling kept plus a second anonymous instance across two literals → **86 passed** in both modules with an anonymous seal in the output |
| ⬜ 3 | `spec.md` A5's *no pair is unaccounted* is false — 48 of 124 under the shipped rule, 65 under the one A5 describes — and no divergence row names A5 | `seal/specs/1789455558-…/spec.md` §A5 | open | Executed: the predicate re-applied to the committed corpus independently, reproducing 74 / 2 / 48 / 0. Read: `overview.md`'s divergence table names §*Operational impact*, A7 and the ledger, not A5 |
| ⬜ 4 | the case-level positive assertion duplicates the fixture guard added in the same commit, so it cannot fire in the state #407 names | `tests/test_the_fixes_close_the_record.py#test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one` | open | Read: the fixture asserts the same equality on the same cell and nothing between them writes it. `phases/phase-6.md` records the same fact — the mutation had to be applied after the fixture returned |
| ⬜ 5 | the symmetric strip drops a sentence-final stop; visible whenever the reviewer's Grounds cell is empty, and disclosed only in `phase-3.md` | `skills/code-review/scripts/round_record.py#fix_table` | open | Executed: with an empty Grounds cell, `` `<sha>`. it reads the cell now. `` renders `fixed at 1cf3cac — it reads the cell now` |
| ⬜ 6 | the shared-ledger row was removed although only one of its two clauses went false; the surviving clause is now claimed by no row in either file | `seal/ledger.md` at `release/v0.12.0:2204`, superseded by `seal/ledger/1789455558-….md:13` | open | Read: `round_record.py:4060` and `:4064` still name the subcommand, so clause (a) holds; all three anchors survive, only their hashes moved; `grep` for the clause returns 0 in both files. `seal/ledger.md:1951` (S13) states the in-place criterion and this row meets it |
| ⬜ 7 | `seal/ledger.md:2201` enumerates two `reach_forward` refusals over a function that now has three, and `--reverify` re-stamped it without anyone re-reading the list | `seal/ledger.md:2201` | open | Read: the third refusal is `round_record.py:1591`. `seal/ledger.md:1945` (S6) wrote this exact failure mode down one work item ago — *a re-stamp recomputes a hash and reads nothing, so a row enumerating three refusals over a function that now has two would have passed silently*. Also: `overview.md` says `--reverify` refreshed 15 rows; 12 rows moved, carrying 15 anchor stamps |
| 🟢 | #404's first-wins holds, and the two sides agree at the cell-reading level too | `skills/code-review/scripts/round_record.py#close`, `#inherited_rows` | verified | Executed: the raw readers do disagree (`'b` helper drops b'` vs `` '`mod.py#helper`' ``), and `table_of` re-serialises through `copied_row` first, so both piped shapes round-trip to exit 0 |
| 🟢 | #405's corpus measurement is the branch's own figure, independently reproduced | `skills/code-review/scripts/round_record.py#reach_forward` | verified | Executed: 74 / 2 / 48 / 0 with 15 stopped by the standing refusal; the 48 all predate the generator, in a different section spelling |
| 🟢 | the ledger and records arms are clean at this SHA | `seal/ledger.md`, `seal/ledger/1789455558-….md` | verified | Executed: `bin/evidence-check --strict .`, exit 0 read directly — `1274 ok · 0 drifted · 0 broken`, records arm `0 refused` |
| ❓ | the broad gate — the full suite, the repository-wide lint, the typecheck | `seal/config.md` | out of verified scope | `agent-contract` §2 assigns it to `agents/sealer.md`, once, after the rounds settle. Answered by the orchestrating session's sealer spawn, which this round does not make due |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py` in the clone at `4a5a32cf` | 82 passed, exit 0 |
| `bin/test` on `test_chain_check_at_the_pull_request.py`, `test_the_record_is_generated.py`, `test_one_word_one_meaning.py`, `test_the_seal_is_taken_once_by_the_sealer.py` | 299 passed, exit 0 |
| `bin/test tests/test_no_real_identifiers.py tests/test_the_rules_have_one_owner.py` | 56 passed, exit 0 |
| `bin/evidence-check --strict .` in the clone, exit read directly | exit 0 — `1274 ok · 0 drifted · 0 broken · 0 external`, records arm `0 refused` |
| `open_row_reason("🟡 3", "open", False)` | returned the *outside the vocabulary* sentence for `open` — 🟡 1 |
| `open_blocking` on a 🟡/`open` row quoting a 🔴 in its Grounds | `[(5, '🟡 3', 'open', False)]` — selected, routed to the second arm |
| `open_blocking` on a 🟢/`verified` row quoting no 🔴 | `[]` — not refused at all; the second arm's stated rule is not enforced |
| mutation A: `round_record.py#seal` reworded to `before the seal is taken`, one literal | `test_one_word_one_meaning.py` **red**, naming the module and quoting the span — phase 5's red-first reproduced |
| mutation B: the same words split across two adjacent literals | `test_one_word_one_meaning.py` **green** — the sweep cannot see the seam |
| mutation C: pinned spelling kept, second anonymous instance added across two literals | **86 passed** in both modules with an anonymous seal in the refusal's output — 🟡 2 |
| the `filled == 0` accounting re-applied to every committed `round-N`/`round-N+1` pair | 15 stopped by the standing refusal; 74 silent; 2 refused by the unconditional rule alone; **48 refused by the shipped rule**; 0 in the fourth cell |
| `close` with a verdict row carrying a raw `\|` inside a code span, and with a `\|` inside the Location cell | both round-trip; `inherited_rows` and `close`'s map name the same coordinate — hypothesis refuted |
| `close` with an empty reviewer Grounds cell and a note ending in a full stop | rendered `fixed at 1cf3cac — it reads the cell now` — ⬜ 5 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

🟡 1 — `skills/code-review/scripts/chain_check.py`, the `else` arm of
`open_row_reason`. It must not name 🔴 (that is #408's own constraint, pinned
by `test_a_confirmation_quoting_an_earlier_blocker_is_not_called_a_blocking_finding`),
so the quote is named without the glyph, and the word is described by what it
fails to do rather than by a vocabulary it is not outside of.

```python
    named = ", ".join(f"`{word}`" for word in sorted(CLOSED_WORDS))
    return (
        "`Pass` is checked, and this row is read as open because one of its "
        "cells quotes a blocking finding an earlier round opened, while its "
        f"own verdict reads `{verdict or 'empty'}` — not one of the words "
        f"that close a row: {named}. Nothing here says the finding was "
        "closed, and an unrecognised verdict counted as closed is the "
        "tolerant read this file exists to refuse. Write one of those words, "
        f"drop the quote, or leave `Pass` unchecked: {what}"
    )
```

§14: four assertions in `tests/test_chain_check_at_the_pull_request.py` pin the
old phrase and move with it — `"outside the vocabulary"` becomes
`"not one of the words that close a row"` in
`test_a_confirmation_quoting_an_earlier_blocker_is_not_called_a_blocking_finding`
(twice), `test_an_unrecognised_verdict_is_refused_by_its_own_name` (twice),
`test_a_row_the_vocabulary_closes_is_silent_even_while_it_quotes_a_blocker`
(once) and `test_a_row_that_carries_a_blocker_keeps_the_blocking_sentence`
(once). The new shape gets its own case:

```python
def test_a_row_reading_open_is_not_told_its_word_is_unrecognised(repo):
    """`open` is the word `agents/warden.md` prescribes for a finding this
    round opened, and the first arm of this same function prints it back as
    `this 🔴 row reads `open``. The second arm must not tell the author the
    word is outside any vocabulary — what selected the row is the quote.

    Red against the arm as written: *…reads `open`, which is outside the
    vocabulary…* on a row whose `#` cell reads 🟡.
    """
    code, out = confirmation(repo, "open")
    assert code == 1, out
    (line,) = [ln for ln in out.splitlines() if "close a row" in ln]
    assert "outside the vocabulary" not in line, line
    assert "quotes a blocking finding an earlier round opened" in line, line
    assert "drop the quote" in line, line
```

🟡 2 — `tests/test_one_word_one_meaning.py`. Fold the literal seam inside
`flat` for the `.py` members of `SEAL_SWEPT`, so one implementation reads both
the prose files and the modules. `import re` joins `import os` at the head.

```python
# Python joins adjacent string literals at parse time and `flat` does not, so
# a phrase split across two of them reads `... the " "seal ...` in the source
# and the sweep goes straight past it. That is the shape the output assertion
# deleted by #406 used to catch, and the reason the deletion was not
# coverage-neutral. Folding the seam here keeps ONE implementation of the rule
# reading two kinds of input, which is what the alternatives table rejected a
# second check in favour of. A seam folded where Python would not join only
# ever creates a hit, never hides one, so the error direction is the safe one.
LITERAL_SEAM = re.compile(r"([\"'])\s*(?:[fFrRbBuU]{0,2})\1")


def flat(*parts):
    text = " ".join(read(*parts).split())
    return LITERAL_SEAM.sub("", text) if parts[-1].endswith(".py") else text
```

And the case that would have caught it, which is mutation C stated as a case:

```python
def test_the_sweep_reads_across_a_string_literal_seam():
    """The shape the deleted output pin caught and the file sweep did not.
    `round_record.py` builds every refusal out of wrapped literals, and where
    the wrap falls is decided by line length, so an anonymous instance
    straddling a seam is an ordinary edit rather than an exotic one.

    Red before the seam fold: the flattened source reads `... the " "seal ...`
    and `find("the seal")` returns -1.
    """
    seamed = ' "Spawn the verifying round first, so the " "seal covers it; " '
    assert "the seal" in LITERAL_SEAM.sub("", " ".join(seamed.split())).lower()
```

---

## Proof block

Opened in the working tree at `4a5a32cf`: `spec.md`, `plan.md`, `overview.md`,
`questions.md`, `routing.md`, `changelog.md`, `phases/phase-1.md` …
`phase-7.md`, `seal/ledger/1789455558-….md`,
`skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`,
`skills/verify/scripts/unverified_check.py`, `seal/ledger.md` (the removed row
at `release/v0.12.0:2204`, and rows `:980 :981 :1945 :1948 :1951 :2172 :2173
:2174 :2198 :2201 :2202 :2203`),
`tests/test_the_fixes_close_the_record.py`,
`tests/test_the_record_is_generated.py`,
`tests/test_chain_check_at_the_pull_request.py`,
`tests/test_one_word_one_meaning.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/conftest.py`,
`bin/test`, `CLAUDE.md`, and the diff
`git diff release/v0.12.0...4a5a32cf`.

Executed in the clone at `4a5a32cf`: the runs in the probe table above. The
probe module and the measurement script were deleted; both trees are clean at
`4a5a32cf`.

Not opened: `handoff.md` (excluded by the spawn), the six issue reports on
GitHub, and any file outside the diff not named above.

Needs a fix: yes — 🟡 1 and 🟡 2

Loses a record or crashes: no

