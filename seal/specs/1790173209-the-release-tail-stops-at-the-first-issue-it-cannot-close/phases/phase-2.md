# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — phase 2

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/phases/phase-2.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 7977de1a |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

#266. `FENCE` covers `~~~` and an indented opening; `SPAN` covers double
backticks; the `# RIDER:` above them is retired; a comment at the patterns
names the two unmasked shapes and why; the changelog fragment states the
direction (masks more, closes fewer). Verified by S5 (three cases seen red),
S6 (two cases pinning the unmasked shapes), the identity case in
`tests/test_a_body_naming_two_issues_claims_one.py` green, and
`issue_claims_check.py`'s own cases green.

## What this phase found

**One pattern each, not two.** The spec left open whether `FENCE` becomes
one pattern or two; one, because `issue_claims_check.py` takes the object
from the closer's module and a second name would need a second import and a
second identity assertion. The backreference `\1` is what a single pattern
buys: a tilde fence closes on a tilde line, not on the first backtick line
inside it, and the mutation that let either delimiter close it went red on
exactly one assertion.

**The double-backtick case had to hold an UNPAIRED inner backtick.** The
first spelling, `` `` `Closes #3` `` ``, was green against a mutant double
form that forbids any backtick inside, because the one-backtick arm then
masks `` `Closes #3` `` on its own. `` ``Closes #3 ` x`` `` is what tells the
two forms apart: the mutant reads the lone backtick as opening a span that
runs to the closing pair, and the keyword before it stays in prose.

**Red at `e99b88e9`, quoted.** The three masked-shape cases:

```
E       AssertionError: a keyword inside a tilde fence closes the issue it names
E       assert ['1', '4'] == ['4']
E       AssertionError: a keyword inside a fence indented under a list item closes the issue
E       assert ['2', '4'] == ['4']
E       AssertionError: a double-backtick span around the number leaves the keyword read
E       assert ['3', '4'] == ['4']
```

and the check's case, for a tilde-fenced `Closes #11, #22`:

```
E           assert (['11'], ['22...1, #22 ~~~')]) == ([], [], [])
```

The two unmasked-shape cases were green there, as they should be: they pin
the reading that was not changed. Green at `0025d851`: `172 passed` over
`tests/test_release_hygiene.py tests/test_a_body_naming_two_issues_claims_one.py
tests/test_a_merged_ticket_says_so_on_the_tracker.py
tests/test_the_closer_carries_on_past_a_refusal.py
tests/test_a_declared_label_reaches_the_tracker.py
tests/test_a_rider_reaches_its_file.py`, and
`python3 .github/scripts/rider_check.py` at `25 ok · 0 drifted · 0 broken`
with the rider gone.

**Mutations**, in the ledger fragment's P2 row: six, five red on the first
run, the sixth red once the case was reworded as above.

**A docstring in `tests/test_a_merged_ticket_says_so_on_the_tracker.py`
named the rider and the open decision.** Reworded in the same commit, so no
sentence in the tree says the question is still open.

**No ledger row anchors on `FENCE` or `SPAN`** (`grep` over
`seal/ledger.md`), so nothing drifted; the fragment's P2 row is the claim.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the `# RIDER: Verified 2026-09-08 against FENCE@53c82b1e` comment and its seven lines naming the five shapes and the decision #266 carries | the comment above the two patterns, which now records the decision taken — three shapes masked, two not, each with the reason — and `tests/test_release_hygiene.py`'s five cases, one per shape |
