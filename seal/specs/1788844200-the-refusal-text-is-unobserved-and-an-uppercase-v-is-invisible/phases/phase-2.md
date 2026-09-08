# 1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | f6ad622 |
| Ran by | specseal:smith on claude-opus-5[1m] — the harness's own model identifier; the spawn prompt named none |

## What this phase was asked

#203. A case beside `test_the_message_has_a_route_for_every_token_the_check_refuses`
that reads the text `refusal` returns and asserts the offender lines, the
running version and the explanatory paragraph are in it — and, explicitly, one
that does not stop a separator short: three consecutive attempts on the
original branch each enumerated the separators and each missed a different one.
Enumerate by construction from the function's own source. Record the residual
as the survivor of the measured set, never as unpinnable.

## What this phase found

**Enumerating by construction is what put the count at seven, and reading
would not have.** `refusal` is a single parenthesised expression: an f-string
literal, `+ "\n  ".join(offenders)`, `+ "\n\n"`, `+ what_to_write_instead()`.
The separator three attempts kept missing is not an operand at all — it is the
`"\n  "` that CLOSES the first literal, so it reads as part of the paragraph
and is invisible to anyone listing the operands. Counting sub-parts rather than
operands is what makes it the fifth of seven instead of a footnote.

> **Corrected by review round 1: that paragraph is a reading of the source
> presented as a construction, and the count is six.** `ast.parse` flattens
> the `+` chain to four operands and the first is one `JoinedStr` of three
> parts — six leaves. Seven was reached by splitting the third part into a
> paragraph and the separator closing it, and by counting the join's `"\n  "`
> argument as an element, which is an argument to an operand rather than a
> leaf. What that cost is the thing the phase was spawned to prevent: the
> paragraph itself went read at its two ends only, with 86 characters between
> the two assertions read by nothing, and two deletions inside it left the
> module at 32 passed. Listing operands by eye and calling it construction is
> the same act as reading, one level down.

**Two offenders in the fixture, not one.** The separator the join contributes
cannot be observed with a single offender, and the tree has had zero offenders
for its whole life — so nothing about a real run would ever have shown it.

**The survivor is measured rather than asserted.** Replacing the message
expression in `assert not offenders, refusal(running, offenders)` with a
literal leaves the module at 32 passed. That is the same shape as the claim
this ticket exists to correct, so it was executed rather than repeated: it is
what these seven mutations left standing, and it stays a survivor rather than
becoming a limit.

> **Corrected by review round 1: the sentence beside it made the survivor a
> limit anyway.** The docstring said pinning that line *"would mean reading
> this file's own source"*. The round disproved it by writing the pin —
> `tracked` and `timers_in` are module globals, and swapping them raises the
> check with a message comparing equal to `refusal(running, offenders)`. The
> survivor is real and the impossibility beside it was not measured.

**What the next phase needs.** The neighbouring docstring's false sentence has
a twin in `seal/ledger.md`'s R3 note, folded there at the 0.9.1 release. Phase
3 owns it, and the correction has to say what the mutations measured rather
than swapping one confident sentence for another.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence claiming the only unpinned thing was the check's own `assert` line, from `test_the_message_has_a_route_for_every_token_the_check_refuses`'s docstring | the same docstring, restated as what three mutations disproved; and `seal/ledger.md`'s R3 note in phase 3 |
