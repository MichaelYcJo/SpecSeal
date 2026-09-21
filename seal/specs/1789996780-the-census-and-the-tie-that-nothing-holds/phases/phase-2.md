# 1789996780-the-census-and-the-tie-that-nothing-holds — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a0606e94 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#469. Build the census case: an unbounded walk over the corpus read through
the module's own `LEDGER` and `FRAGMENTS`, asserting every candidate site is
one `MARKER` sees, asserting no count, refusing an empty corpus, failing with
the file, the row, the run length and the spelling, and saying in its
docstring how its number was taken and why the instrument cannot be `MARKER`.
Green as shipped, red with the bound narrowed to four, green with the bound
narrowed to four **and** the census taken with `MARKER` (A7).

## What this phase found

**The first census this phase wrote repeated the defect it exists to
prevent.** Written as one expression — `verb (.*?) date` over the whole file
with `finditer` — it found **423** candidate sites where `MARKER` matched
**425**. The instrument meant to be strictly wider than the pattern under test
was narrower than it.

The cause is consumption. `finditer` does not overlap, so a first verb whose
gap is *not* a lowercase run still consumes everything up to the next date —
including a second verb standing between them. `Corrected in review. Re-read
2026-09-05.` loses the `Re-read` site entirely, because the walk is already
past it. `MARKER` has no such hole: when it fails at one verb the scanner
advances one character and tries the next.

So the walk is verb by verb, and the gap is read from the verb's end to the
next date on the same line. Rewritten that way the census finds 425 sites
against `MARKER`'s 425 occurrences, and **0** of them are sites `MARKER` does
not see. This is written into the comment above the instrument rather than
left in a record, because the next person to widen the census will reach for
the one-expression form first.

**The bound's longest justification stands in prose, and nothing had said
so.** Splitting the census by whether the site sits on a table row:

| Where | run lengths and their counts | total |
|---|---|---|
| on table rows | 0: 382, 1: 23, 2: 8, 3: 9 | 422 |
| in prose | 2: 1, 3: 1, 5: 1 | 3 |

All three prose markers are qualified, they are the three longest spellings in
the file, and **no table row carries a qualifier longer than three words**.
The five-word run the bound exists to admit — `Re-read and re-stamped a third
time 2026-09-08` — is one of the three, so the survival test, which acts per
row, would return the same verdicts today at a bound of three.

That is not an argument for narrowing the bound and the census note says so:
the same authors who wrote a five-word qualifier into prose will write one
into a row, and `markers()` is applied to whole-file text as well as to rows.
It is an argument for stating what the bound is justified by, which is the
tree's longest spelling **wherever it stands** — and for the bound's grounds
never again being a count nobody split.

**The mutation pair came out exactly as A7 predicts, and the second half is
the one worth having.** With `{0,5}` narrowed to `{0,4}` the case fails at

```
1 of 425 candidate marker site(s) fall outside the bound on `MARKER`'s
qualifier. … seal/ledger.md: a run of 5 lowercase word(s) between the verb
and the date, which `MARKER` does not read as a marker -- `Re-read and
re-stamped a third time 2026-09-08`, on row '(prose, outside any row)'
```

With the same narrowed bound and `candidate_sites` rewritten to walk
`cc.MARKER.finditer`, the case **passes, exit 0**. The pattern under test
cannot see the spelling it misses, so the census justifying it agrees with the
mistake. That is round 1's and round 2's failure of #424 reproduced on demand,
and it is the whole reason the instrument choice is load-bearing rather than a
preference.

**The corpus is one file at this SHA, which is why it is read through the
constants.** `git ls-files -- seal/ledger.md seal/ledger` returns
`['seal/ledger.md']`: the 0.12.2 release folded all three fragments in and
`seal/ledger/` does not exist. A case with a hard-coded list of the three
fragments would have gone green over nothing at all.

**An edit that did not land, caught by the run rather than by the edit.**
`import re` was added before any use of it, and the repository's formatter
hook removed it again as unused — the file on disk did not carry the line the
edit reported writing. Collection failed with `NameError` on the next run.
`agent-contract` §9 argues for the `Edit` tool because a shell substitution
can miss silently; this is the same hazard arriving from the other side, where
a hook rewrites a landed edit. The defence is the same one: run the check.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the test module docstring's claim that every case here was seen red against *phase 1's, phase 2's or A3's* mutation — true of #424's cases, and silent about the two this work item adds | the same docstring, extended with this work item's two mutations and with what the second of them demonstrates |
