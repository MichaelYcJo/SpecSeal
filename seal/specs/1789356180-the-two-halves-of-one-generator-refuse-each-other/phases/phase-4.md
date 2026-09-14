# 1789356180-the-two-halves-of-one-generator-refuse-each-other — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 26c7696 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

`Fixes checked by` after a fix table applies. The cell stops carrying *the
fixes are not yet written* about fixes that are written and named in its own
verdict cells, without turning `chain_check`'s fix-surface arm red on the
pairing it refuses (#273 part 1). Q4 answered (a): it ships here. Q5 is a
measurement this phase takes before it writes the reason text.

## What this phase found

**Q5 is answered `no arm turns red`, and the reason is that neither arm reads
the reason text at all.** The question assumed the fix-surface arm might,
because it refuses `none — the fixes are not yet written`. Measured before
anything was written:

| What was measured | Result |
|---|---|
| `says_not_yet` over the checker row's value | never called on it — the arm applies it to the **surface** row, which `close` fills from the diff |
| `CHECKER_RE` over `nobody — the fixes are not yet written` | no match — so `fixes_exist` is False and the pending arm is silent |
| `CHECKER_RE` over the new reason | no match — identical, so the arm cannot tell the two apart |
| `chain_check.checked_by`'s source for `NOT_YET` | absent — it splits `nobody` from its reason and requires only that a reason exist |

So the reason is free text behind a vocabulary word, and changing it is a
change to a sentence rather than to a gate. The end-to-end confirmation the
question asked for — one fixture record, both arms, before and after — is
`tests/test_the_fixes_close_the_record.py#test_neither_chain_check_arm_turns_red_on_the_new_reason`.

**`nobody` is right and the reason was wrong, which is narrower than the
ticket reads.** #273 part 1 reads as though the whole cell were false. It is
not: the ordering rule requires a checker to be a LATER round, and at the
moment `close` runs there is none — so `nobody` is the only legal value. What
is false is *not yet written*, beside commits the same pass just wrote into
the verdict cells two rows below. The repair keeps the word and replaces the
reason.

**`close` corrects only the landing value it recognises.** It compares the
standing cell against `PENDING_CHECKER` before rewriting, so a cell already
naming a `round-N` — a later round's reading, set by the reach-back — is not
this pass's to touch. Without that guard the correction would overwrite a fact
with a weaker one on any second application.

**`landing_values`' docstring was the design statement Q4 called a reversal,
and it is rewritten rather than contradicted.** It said the cell *stays at the
landing value for `new` of the next round to set, because a fix was written and
a later round owes it a reading*. That is true of WHO and false of WHAT, and
the docstring now says so — a reader who finds the old sentence quoted in
`questions.md` Q4 can see what replaced it and why.

**This phase and phase 3 were committed together by mistake and split back
apart.** `plan.md`'s alternatives table rejects one commit carrying two rules
on the grounds that neither can be shown failing alone. The combined commit was
reset, phase 4's five code edits and three cases were reverted, phase 3 was
verified standing alone (56 cases green) and committed, and phase 4's case was
then seen red **again** on that committed tree before being re-applied. So the
red-first evidence for phase 4 exists against phase 3's tree rather than only
against `e387bff`, which is the stronger of the two readings.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `landing_values`' statement that `close` leaves the pending cell for the next round's `new` | the same docstring, which now says `close` writes both of the function's answers and why the old grounds were half right |
| the reason `the fixes are not yet written` from a closed record's `Fixes checked by` | `WRITTEN_CHECKER`, the second reason. `new`'s landing value is unchanged and still says *not yet written*, because while the round runs it is true |
