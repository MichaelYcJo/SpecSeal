# 1788501054-a-check-reports-clean-while-something-is-missing — phase 5

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-5.md
— what this phase of the build did, written by the implementer when the phase
closes. It is not in `plan.md`'s original four: round 1's fixes are work the
plan did not contain, and the phase row was added beside them. -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | b87ba49 |
| Ran by | specseal:smith on opus |

## What this phase was asked

Round 1's four 🟡, with the record as the agenda. In the order the fix pass
took them, which is the order they depend on rather than the order they were
raised:

- **🟡 9** — the skipped-ledger comparison folds case on Windows alone, so
  `--ledger SEAL/ledger.md` names a file it just read.
- **🟡 8** — `added_on_branch` takes `found[-1]`, its docstring documents that
  choice, and mutating it left all twenty cases green.
- **🟡 7** — the refusal's reach is the SHA a verdict cell happens to carry,
  and 19 of the repository's fix-word cells carry none.
- **🟡 6** — three `seal/ledger.md` rows assert a `Checked` date two days
  before the content their new hash covers.

Two constraints came with it: run `evidence_check.py .` **unscoped**, and do
not run an unscoped `--reverify`, because S8 is `45edf260` and its claim is
false. The fix-surface rows were asked for with the depth checked rather than
assumed.

## What this phase found

**The record carried no fix to paste.** The message commissioning this pass
said `round-1.md` carries the reviewer's paste-ready replacements for all four
findings. It does not: the file has **zero fenced blocks**, and `grep -c` for
one returns 0. The record is not in breach of the rule phase 4 added — its
probe rows name commands and mutations, not proposed replacements — so what
this is instead is the ticket's own failure met from the other side, in the
prose commissioning the work rather than in the record. Every fix below was
written here.

**Round 1's count is off by four, and the direction of its finding is not.**
The record says 231 fix-word verdict cells, 212 with a SHA, 19 without.
Measured through the checker's own `verdict_table`, `verdict_of`, `FIX_WORDS`
and `SHA_RE` over every `seal/specs/*/rounds/round-*.md` git carries: **235 ·
215 · 20**, identical at the round's target `15278db` and at HEAD. So the
finding stands and its number does not, and 235/215/20 is what went into
`templates/sdd-round.md` and `docs/review-chain-spec.md`. An aggregate is not
a coordinate, which is the rule the handoff protocol carries and the reason
this was re-measured rather than copied.

**🟡 8 changes what 🟡 8's own neighbour means, and a ledger row went stale
with it.** Under `found[-1]`, dropping `--diff-filter=A` was separable only by
a base that moves under a long branch — the case phase 3 wrote after the
mutation survived. Under `found[0]` it also refuses every correctly updated
record, because the newest commit that TOUCHED a record is the one that
updated its verdicts. The fragment's R1 claimed the narrow reading and is now
rewritten to name the pair; nothing but re-running the battery would have
caught that, and the mutation count moved from 1 red to 2 for the same
mutation.

**🟡 9's fix drops the platform rather than fixing the platform's case.**
`os.path.normcase` folds case on Windows and is the identity everywhere else;
`realpath` canonicalises case nowhere. Folding by `st_dev`/`st_ino` answers
case, hard links and symlinks with one rule and no platform in it — and the
hard link is what makes the case red on **every** platform, where the case
spelling is red only where the filesystem folds. Both cases are in the file
and the second skips itself after probing the filesystem, so this file does
not assume the guarantee its own finding was about.

**🟡 7 is answered with a template sentence rather than a sixth refusal.**
Refusing a `fixed` cell with no commit would refuse a spelling 20 existing
cells already use, and would need its own cutoff and its own subsection — a
third rule on a branch the risk statement already calls doubly exposed. What
shipped instead asks for the commit where a person writes the cell, with the
reason, so the reach grows as records land and nothing red is inherited. The
spec now says outright that *this record passed* means *no cell in it named a
commit the record descends from*, never *this record was written on time*.

**🟡 6 is eight rows, not three, and five of them cannot be told apart by the
date at all.** The three the round found carried `2026-09-02`; the other five
already carried `2026-09-04`, and were re-stamped without a re-read in exactly
the same way. All eight claims were re-read against current content and all
eight hold. The three impossible dates are corrected with what the re-read
found, `:102`'s note said `Draft 0.6` where this branch moved the protocol to
1.2, and `phases/phase-4.md`'s sentence now names which rows were re-read
when. **The general fact is R6 in the fragment**: a `--reverify` landing on
the same day as the row's existing date leaves no trace, so the date is
necessary and not sufficient, and no column can close that.

**`seal/ledger.md:359` was re-stamped by hand from a one-row scratch ledger.**
A `--reverify` over that file re-stamps S8 with it, which is the churn R6
records; a scratch ledger holding the single row prints the new hash and
touches nothing. S8 still reads `45edf260`, checked by grep after the edit.

**The depth question the fix pass was told to check does not bite either
way.** No top-level unit was added to either checker: `skipped_by_narrowing`
gained a loop and `added_on_branch` one index. The six new units are all in
test files. And the rule's own words are about a unit a FIX PASS added — *a
fix answering a finding inside that helper* — where both units here were added
by the build phases and were read in full by round 1, so a helper beside them
is depth 1 rather than depth 2. Stated because the two readings differ and the
fix pass was asked to check rather than assume.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `added_on_branch`'s documented choice of the EARLIEST add, and the paragraph explaining it | The docstring now documents the latest add and why, and the fragment's R1 carries what the old index cost. The reverted choice is a mutation in the battery (`C1`), so it stays executable rather than only described |
| `skipped_by_narrowing`'s path-spelling comparison and its *normalized case* clause | The inode fold and its docstring; the fragment's R3, which names the three spellings that break the old rule; `skills/evidence-check/SKILL.md`, which now tells a reader that two names for one file are one ledger |
