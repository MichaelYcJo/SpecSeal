# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — phase 4

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `cb38e54` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#408. The severity is read from the `#` cell, and a verdict word outside the
vocabulary gets its own arm with its own sentence — naming the verdict word,
naming the vocabulary, and **not naming 🔴**. §14: both sentences pinned in
this commit.

Verified by `bin/test tests/test_chain_check_at_the_pull_request.py`, red-first
with two mutations — the whole-row join restored, and the vocabulary clause
deleted from the new sentence — plus the case asserting the old sentence is
absent from the new arm's output.

## What this phase found

**The repair is a message split, and the set of refused rows is unchanged.**
That is not what the ticket's title suggests and it is what the ticket's body
asks for: *failing the row is correct*, and `open_blocking`'s selection —
a 🔴 anywhere in the row, beside a verdict the vocabulary does not close — is
what keeps an unrecognised verdict from counting as closed. Only the fourth
field is new, and only it is read from the `#` cell. Reading the SELECTION
from the `#` cell was the rejected alternative, and it is rejected for the
reason the plan gives.

**Two neighbouring cases say why the selection could not widen either.**
`test_a_checked_pass_beside_an_open_NON_blocking_finding_passes` pins a 🟡 row
reading `open` as a pass, so an arm keyed on *any* unrecognised verdict would
turn that red — and the corpus walk at the foot of the same module, which runs
every committed last record through these functions, would have gone with it.
The narrow reading is the only one that leaves both standing.

**The mutated run printed the defect verbatim**, which is the clearest thing
this phase produced:

```
`Pass` is checked, and this 🔴 row reads `verified` — a blocking finding
that is not fixed, answered or withdrawn: 🟢
```

One sentence, two severities, on a row whose `#` cell is 🟢. Both new cases
went red on it; the second mutation turned the §14 pin red on `` `fixed` ``
missing from the vocabulary list.

**Q6's sentence, drafted here for the round that reads it.** The new arm
reads:

> `Pass` is checked, and this row's verdict reads `<word>`, which is outside
> the vocabulary — `agreed, fixed`, `answered`, `deferred`, `fixed`, `not a
> defect`, `out of verified scope`, `withdrawn`. Nothing here says the finding
> was closed, and an unrecognised verdict counted as closed is the tolerant
> read this file exists to refuse. Write one of those words, or leave `Pass`
> unchecked: `<the # cell>`

Three things it does on purpose. The vocabulary is **rendered from
`CLOSED_WORDS`** rather than written out, so a word added to the set cannot go
missing from the message. The closing clause offers the two ways out — change
the word, or stop claiming the round passed — because a refusal that names
neither leaves the reader to guess which. And **the 🔴 is absent**, which the
case asserts on the line rather than on the output, since other arms of the
same run legitimately print one.

**A7 of `spec.md` does not hold as written, and the phase built the reading
that does.** A7 says a 🟢 row quoting a 🔴 *and whose verdict is closed* says
nothing, and calls that case *red against the whole-row join*. Both halves
cannot be true at once: the whole-row join also requires the verdict to be
open, so a closed verdict was already silent before this change and no fixture
of that shape can be red. What is red against the join is the same row with
`verified` — refused either way, and called a blocking finding only by the
join. The case is written that way, and a second case carries the
closed-verdict half as the silence it actually is.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The single-sentence refusal for an open row — the caller no longer formats it inline | `open_row_reason`, which holds both arms and is where §14's pins point |
