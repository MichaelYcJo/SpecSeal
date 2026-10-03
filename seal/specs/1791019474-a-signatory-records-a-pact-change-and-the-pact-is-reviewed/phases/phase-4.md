# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | b9623ffd |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 4: `pact-check` reads each signatory's record (`NOT TAKEN`,
`NOTED`, the read filter, `REFUSED`, `UNREADABLE`); the pact-reviews reader on
the walker; taking by content hash; the four review refusals;
`templates/pact-review.md`; the docs and skill text for the reader and the
pact review; every new sentence pinned. Verified by S12–S17 each seen red,
`bin/mutation-check` over each refusal and over the hash comparison, and
`test_pact_check.py` green.

## What this phase found

**The frame holds.** The reader is two functions beside `check`:
`pact_check.py#pact_reviews` reads the pact's `seal/pact-reviews/*.md` once
and refuses a row that cannot be true where the pact alone can say so (an
unlisted signatory, a change not written `<id>@<hash>`, a verdict outside
the two); `pact_check.py#pact_changes` reads one signatory's records and asks
the two questions only the signatory can answer, whether it holds the record
a review names and whether `amended` is true of the clauses the record cites.

**A row citing only another pact is neither read nor refused.** A signatory
of two pacts records changes under both into one work item's file, so a row
whose clause names `pact:billing/…` is skipped here rather than called a
`Clause` cell that will not parse. A `Clause` cell that holds no pact anchor
at all and is not `—` is refused.

**The record's lines are counted on the file as the writer writes it**: the
header the writer begins a record with puts the first row on line 7, which is
what the `NOT TAKEN` line names. A record a person begins without that header
is read the same way, by the walker, wherever its table is.

**`NOTED` sits in no exit class**, and a case holds that: adding it to
`EXIT_ONE` turns one red. Its sentence says the row *reads noted until* a pact
review takes it.

**The `READ` line and the summary each gained a count** (*N pact changes
read, M taken* and *· N pact changes read · M taken*). Every existing
pinned summary was a prefix of the new one, so no earlier case moved.

**Mutation: 17 breaks, each red** — each of the five review refusals, taking
at any hash and at none, the earlier hash dropped, another signatory's review
counted, another record's review counted, `amended` never checked and always
refused, a held record not checked, a `—` row read under the default, `never`
not honoured, another pact's row refused and read, the taken count, and
`NOTED` moving the exit. Four survived the first pass and each got the case it
named.

**Seen red against `2b1dcb1f`'s `pact_check.py`**: all 15 cases the module
had before the four survivor cases were added.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
