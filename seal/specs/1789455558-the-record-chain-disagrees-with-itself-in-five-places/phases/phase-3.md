# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — phase 3

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `1f098fd` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#414. The fix-table note cut strips a trailing period **at the call site**,
never in `chain.SEPARATORS`, which five readers share. The class is
enumerated rather than assumed (Q5): every `strip(chain.SEPARATORS)` site in
`round_record.py` is read, and each is either repaired or recorded as leaving
nothing behind.

Verified by `bin/test tests/test_the_record_is_generated.py
tests/test_the_fixes_close_the_record.py`, red-first by stripping back to
`chain.SEPARATORS` alone, with the case asserting the **whole** rendered
Grounds cell so it cannot pass on a cell the fixture failed to build.

## What this phase found

**Q5's answer is two, not one, and the second member is in the same
function.** The default in `questions.md` said one — *the other sites read a
whole cell rather than cutting a span out of one* — and that is true of three
of the four but not of the fourth.

| Site | What it cuts | Verdict |
|---|---|---|
| `written_late_cell`, the `reason` line | the whole flag value, both ends | leaves nothing behind, and a trailing period there is a sentence's |
| `fix_table`, the `note` line | the commit's code span, out of the middle of a cell | **member** — repaired |
| `fix_table`, the `home` line | the word `deferred` off the front | leaves nothing behind: `verdict` has had `rstrip(".")` applied one screen above, and the arm's own test requires the character after the word to be a separator |
| `fix_table`, the `rest` line | the home off the front of the third cell | **member** — repaired |
| `fix_table`, the suffixed-verdict refusal | the matched head off the front, into a printed row | leaves nothing behind, for the same two reasons as the `home` line |

**The second member was executed before it was repaired**, through
`fix_table` directly rather than read: a third cell of `#309. the parity arm
is out of scope` came back as `('deferred', '#309', '. the parity arm is out
of scope')` and rendered `#309 — . the parity arm is out of scope`. The same
run reproduced the reported shape at the note line, `fixed at 6233b769 — .
\`refusal_paragraph()\` bounds the slice`. Both went red against the
un-widened strip afterwards, in the predicted direction.

**What makes the two members members and the other three not** is not the
direction of the cut, which is what the default reasoned from. It is whether
the character at the cut boundary is one the code has already tested. At the
`home` line and at the refusal, the arm above matched on `word[len(w)] in
chain.SEPARATORS`, so the remainder begins with a separator and `strip` takes
the whole run. At the two members, the boundary is wherever somebody happened
to end a code span, and a full stop after it is ordinary prose.

**What the symmetric strip costs, stated rather than left to be found.** The
widening is `strip`, not `lstrip`, so a note that ends in a full stop loses
it too — `| 1 | fixed | \`abc1234\`. it reads the cell now. |` renders
`fixed at abc1234 — it reads the cell now`. That is the shape #414 prescribed
verbatim and the shape every other site in the function uses, and a one-sided
strip would leave the two members spelled differently from their three
neighbours for a stop nobody has yet written. Recorded because it is a real
loss and nothing measured it.

**`chain.SEPARATORS` is unchanged, and a case now says so for the period the
way one already said it for the backtick.** The new case asserts both halves:
no period in the shared constant, and exactly two `chain.SEPARATORS + "."`
inside `fix_table`. The second half is what keeps a later widening from
quietly moving to one site and leaving the other.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the widening adds a character at two sites and takes nothing out | none |
