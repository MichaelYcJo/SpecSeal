# 1788491830-a-segments-record-says-what-it-cost — phase 2

<!-- seal/specs/1788491830-a-segments-record-says-what-it-cost/phases/phase-2.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 2a36737 |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build phase 2 only: `chain_check.py` reads the row. Absent is refused after a
fourth cutoff and printed before it; present and unreadable is refused at any
age; `unknown — <why>` is an answer and a bare `unknown` is not. Every refusal
seen red at a named SHA, mirroring the three cutoffs already in the file —
`STRICT_FROM` at `:333`, `SURFACE_FROM` at `:373`, `NEEDS_FROM` at `:459`,
three cutoffs of one shape.

## What this phase found

**The absent-row refusal was seen red by twenty-one existing cases before one
new case existed.** Three test files build round records for work items whose
ids sit after every cutoff — `1799000000` in
`test_the_fixes_name_their_surface.py`,
`test_the_record_is_held_to_the_floor_and_the_depth.py` and
`test_the_last_rounds_fixes_are_checked.py` — so wiring `ran_by` into the main
loop turned all three red at once, with the refusal's own message quoted in
the failure. That is the same blast radius the floor row had, and each of
those files already carries a comment saying why its fixture holds the
previous row. This phase added the fourth such comment to each.

**`ON_RE` needs whitespace on both sides, and the obvious case does not pin
it.** `test_the_on_must_stand_alone` was written with `carbon`, and the
mutation that strips the whitespace from the pattern left it green: `carbon`
splits into `carb` and an empty tail, and the empty half is refused by the
very next clause. The word that catches the mutation is one splitting into two
NON-empty halves — `monitor`. The case that looked like it pinned the boundary
was pinning the clause after it.

That is the one survivor of twelve mutations, and it is worth carrying
forward: a refusal with two clauses in sequence needs a case that reaches the
second one without tripping the first, and a plausible-looking input often
trips the first.

**The `unknown` branch is tried before the split, and this phase recorded
that as load-bearing. It is not — round 1's 🟡 4.** The claim is left standing
here with its correction beside it, because what this phase concluded is part
of what the record is for.

The reviewer compared the two orders over constructed cells and found zero
verdict mismatches, and reversing the arms in the file left the suites green.
It is true by construction: the `unknown` arm refuses when nothing follows the
separator, and nothing following means there is no ` on ` in the tail either,
so every cell that would split is one the `unknown` arm accepts anyway. What
the order settles is the READING, not the verdict — `unknown — the model was
not recorded on this run` is an unknown with a reason under this order and a
pair under the other, and both accept.

The mistake underneath it is worth more than the correction: **this phase
reasoned about a tolerant read and never ran the comparison that would have
told it whether one existed.** A parser argument that is not differentially
executed is a story about the code.

The consequence of the chosen order stands as recorded: `unknown on Opus` is
an unknown with a reason rather than a half-named pair, nothing is lost since
the model is still written where a reader sees it, and telling the two apart
would mean a rule about whether an English reason may begin with `on`.

**A no-op control ran beside the mutations.** One entry in the loop changes
nothing observable and must stay green; without it a loop where every case is
red for an unrelated reason reports twelve catches and proves nothing.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
