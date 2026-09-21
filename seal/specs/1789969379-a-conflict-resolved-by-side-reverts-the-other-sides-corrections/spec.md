# Feature Specification: a conflict resolved by taking a side reverts the other side's corrections (#424)

<!-- seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## What is wrong, in the order the causes run

```
two branches each correct rows of seal/ledger.md that the other did not touch
        ↓ the fragment rule's EXCEPTION requires this — a branch that
          falsifies a row must repair it in the shared file
seal/ledger.md conflicts, and the two hunks resolve in OPPOSITE directions,
because each side is the superset in one of them
        ↓ a side is taken wholesale
three corrections are reverted — each had turned a false claim true
        ↓
a row reverted to a superseded state is BYTE-IDENTICAL to a row nobody
touched, so nothing has anything to notice
        ↓ --reverify is the obvious next step after a merge drifts anchors
the restored rows are re-stamped: "somebody read this" is written over three
claims that had been read, found false and repaired
```

It was caught by one accident: the reviewer grepped for the marker the
corrections carried and found **0** occurrences of `Corrected 2026-09-15` in a
file that had had three.

## The ticket's second direction is wrong about the tree, and the correction
## changes what that direction costs

#424 offers *a row whose `Checked` date goes backwards across a merge, which
is the same signal in a column a machine already reads*.

**No machine reads that column.** Executed — `grep -n "Checked"
skills/evidence-check/scripts/evidence_check.py` returns exactly two lines,
`1577` and `1587`, and both are inside a `# RIDER:` comment. The column is
written by people and read by nobody. `templates/ledger.md` §48 states the
convention in prose and nothing enforces it.

So that direction is not *read one more column*. It is **teach something to
read a column for the first time**, and it lands on a question this repository
has already written down and deliberately left open. The rider at
`evidence_check.py#reverify` says so in its own words:

> this rewrites the hash and never the `Checked` column, so the claim that
> somebody re-read the code is made by a person and recorded by nobody. …
> If you open this function, decide whether it should refuse a row whose
> `Checked` still predates the hash it is about to replace, or print the ones
> it left; the fix pass that found this could add neither without adding
> mechanism.

Round 1 of #120 measured the gap it names: six rows got new hashes on one
branch and all six kept dates from before the content moved, one of them
anchored on the very section that branch rewrote.

## What the markers actually look like, measured before anything is built

The ticket's first direction counts *correction markers*. Counted in the tree:

| Marker | `seal/ledger.md` | the one live fragment | Spellings seen |
|---|---|---|---|
| `Corrected <date>` | 10 | 0 | at least three — `…by issue #98.`, `…by review round 3, finding 3`, `…(#205):` |
| `Re-read <date>` | 185 | 4 | — |

Two things follow and both are scope decisions rather than details.

**`Re-read` is the common marker and `Corrected` is the rare one.** A check
that counts only `Corrected` would watch 10 rows and ignore 189. The work item
that merged immediately before this one, `1789956662`, re-read and widened
four rows of the shared file and wrote `Re-read` on every one of them — losing
one of those to a merge is the same loss the ticket is about.

**No marker has one spelling.** Anything matching on the sentence rather than
on the leading `<verb> <date>` is pinned to prose somebody will reword.

**CORRECTED at round 1, finding 1.** The table above and the sentence before
it measured the spellings **after** the date, found three, and stated that
with a count — which made *the variation lives after the date* read as
measured when only one side of the date had been looked at. It varies before
it too, and by more:

| | occurrences in `seal/ledger.md` when round 2 measured it |
|---|---|
| markers a `<verb> <date>` pattern matches | 365 |
| markers the file actually carries | 404 |
| **markers such a pattern cannot see** | **39** |

Ten qualifier spellings sat between the verb and the date when round 2
measured it — `again` 19 times, `and re-executed` 5, `a third time` 4, `a
fourth time` 3, `and re-stamped` 2, `a fifth time` 2, and one each of `and
re-stamped again`, `and re-stamped a third time`, `and widened` and `and
re-measured`. One row, `R4 ·
the printed bound reads BOTH of the gate's walks …`, carries no other
spelling, so it was invisible to the check entirely. Nine commits in this
repository's history have introduced `Re-read again` into that file, measured
at the tip of the branch for #469, #470 and #471 with `git log -S`; it was
stated as six here, with no moment and no instrument.

**CORRECTED at round 2, finding 6.** The middle row of that table read `403`
and the last `38`, and the paragraph said nine spellings. Those numbers were
measured **with the widened pattern itself**, so a spelling the pattern could
not see was invisible to the census justifying it — the same circle this
section was written to correct, one layer down. The tenth spelling is `Re-read
and re-stamped a third time <date>`, five lowercase words where the bound was
four, and it stands in `seal/ledger.md`'s prose rather than on any row.

<!-- CORRECTED 2026-09-22 by work item 1789996780 (#470 and #469). Two things
stood here. The table had no moment on it, and the figures in it are over a
corpus that moves: a8bf2a86 folded three ledger fragments into that file and
this branch wrote a marker into it, so the header now names when they were
taken. And the tenth spelling was addressed as "seal/ledger.md:1172", a
position where CLAUDE.md requires content, so it is named by its spelling and
by the fact that it stands in prose rather than on a row -- which is itself
worth knowing, since the survival test acts per row and never reaches it.
Corrected in place with the issue named, never deleted silently: a record of
a past state that quietly becomes true is a record nobody can audit. -->

The figures above are now taken by an instrument that is **not** the pattern
and has no bound: for every verb, the next date on the same line, counting the
words between. Measured that way the run lengths are 0, 1, 2, 3 and 5 words —
**there is no run of four**, so the bound that shipped matched exactly what a
bound of three would have and bought nothing.

So the sentence `<verb> <date>` names is right about where the identity
lives and wrong about where the variation does. What ships reads a short run
of lowercase words between the verb and the date as part of the same marker;
the identity is still the verb and the date, so the two spellings of one
reading compare equal. Also note that the counts in the table above are
**rows**, not occurrences — `grep -c` gives one line per row, and a row can
carry a marker in more than one cell.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*a change writes fragments, never the shared file* and its exception | The exception is the whole cause. This is the ordinary state of every parallel release cycle, not one bad merge, so the answer has to survive being routine |
| `CLAUDE.md` §*The goal a design is chosen against* | The act being protected — reading both sides of a hunk — is irreducibly a person's. What a check can buy is telling them they lost something; it cannot do the reading. Every candidate is weighed on which of those two it is |
| `CLAUDE.md` §*A ledger coordinate names content, never a position* | A row is content. Whatever is built compares text, never line numbers, and survives `fold_ledger.py` moving a fragment into the shared file |
| `CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not re-pointed* | The legitimate way a marker disappears. A check that cannot tell this from a reverted correction is a check that fires on correct work |
| `skills/verify/SKILL.md` §*The Seal Test* | The defect is a state nothing can report. Nothing added here may be a check that cannot fail |
| `skills/agent-contract/SKILL.md` §12 | The fact *a correction was silently lost* has more than one statement: the checker, the two rule documents, and the contribution guide. The class is enumerated below |
| `skills/agent-contract/SKILL.md` §15 | Every case is seen red first, against a merge constructed to lose a marker |

## Scope

### In

1. **A check that names a correction lost at a merge.** For every merge commit
   in the range, a marker present in **either parent's** ledger text and
   absent from the merge result, **while the row carrying it survives**, is
   reported with the file, the marker and the parent it came from.
2. **Row survival is what separates a loss from a removal.** A marker that
   vanishes with its whole row is `REMOVED` and correct; a marker that vanishes
   while its row stands is the defect. This is the one distinction the check
   exists to draw.
3. **Both markers count** — `Corrected` and `Re-read` — matched on the leading
   verb and date rather than on the sentence after it.
4. **It reads `seal/ledger.md` and every `seal/ledger/*.md` fragment**, because
   a fragment becomes part of the shared file at the release and a check that
   watches only one of them goes blind at the fold.
5. **The sentence at the conflict.** Where `CLAUDE.md` and `CONTRIBUTING.md`
   state the fragment rule's exception, they gain what to do when the file
   conflicts: resolve per hunk, read both sides, never `--ours` or `--theirs`
   — with the reason, which is that the two hunks of the measured instance
   resolved in opposite directions because each side was the superset in one.

### Out, and why each

| Out | Why |
|---|---|
| A merge driver for `seal/ledger.md` | #424 §*Not this*. A driver would have to understand what a row claims, which is the judgment the ledger exists to have a person make |
| Forbidding corrections to the shared file | #424 §*Not this*. The exception exists because a branch that falsifies a row must repair it; removing it leaves the ledger stating what the tree contradicts |
| Teaching `--reverify` to read `Checked` | The rider at `evidence_check.py#reverify` owns that question and states that the pass which found it could add neither answer without adding mechanism. `questions.md` Q1 is where it is put; it is a neighbouring surface, not this work |
| Backfilling `Checked` dates, or any repair of the three reverted rows | The incident's rows were repaired when it was found. This work is about the next one |
| Making the check read anything about what a row CLAIMS | It compares markers and row survival. Judging a claim is a person's |

## The class, enumerated by construction

Every place the tree today tells somebody what to do when the shared ledger
conflicts, found by reading the two rules and the guide rather than by recall:

| Statement | Says today | After this work |
|---|---|---|
| `CLAUDE.md` §*a change writes fragments…* | that a removal must touch the shared file | and what to do when that file conflicts |
| `CONTRIBUTING.md`'s matching sentence | the same, and the two used to disagree | the same addition, and the two are pinned against each other |
| `evidence_check.py#reverify`'s docstring | that re-verifying is a person's claim | unchanged — the rider above it owns the open question |
| the new check's own refusal | — | names the marker, the parent it came from, and that the row survived |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given a merge whose result drops a `Corrected <date>` marker that one parent carried, while the row carrying it still exists, when the check runs over that range, then it reports the marker, the file and the parent | a case building that merge with two branches and one taken side; red against the check's absence |
| A2 | The same for a `Re-read <date>` marker | a case; red separately, so a check watching one verb only cannot pass both |
| A3 | Given a merge that removes a whole row, marker and all, when the check runs, then it reports nothing | a case; this is `REMOVED`, and a check that fires here fires on correct work |
| A4 | Given a merge that loses a marker from a `seal/ledger/*.md` fragment, when the check runs, then it reports it | a case; the fold makes fragments and the shared file one file later, so both are watched from the start |
| A5 | Given a range with no merge commit in it at all, when the check runs, then it exits 0 and says it looked at none | a case; the common case must be cheap and must say so |
| A6 | Given a merge that loses a marker *and* the other parent's side of an unrelated hunk, when the check runs, then every lost marker is named rather than the first | a case with two losses; a check reporting one teaches a reader to fix one and re-run |
| A7 | Given a marker whose sentence was reworded but whose verb and date stand, when the check runs, then it reports nothing | a case; matching the prose after the date is what pins a check to wording somebody will change |
| A8 | Given `CLAUDE.md` and `CONTRIBUTING.md`, when the suite runs, then a case holds their conflict sentences against each other | a structural case, red when either side stops saying it. The two have disagreed before, which is why they are pinned rather than trusted |
| A9 | Given the check wired into CI for a pull request into `release/*`, when a branch carries such a merge, then the leg is red with the marker named | read at the workflow, and a case over the workflow's own text; whether the leg ships red-blocking is Q2 |

**A3 is the one that can come back inconvenient.** It asks the check to stay
silent on a legitimate removal, and the tree today has no instance of a
removal to build the fixture from — it has to be constructed. If it turns out
that row survival cannot be decided cheaply, that is a divergence row in
`overview.md` naming what was tried, not a reason to drop A3: without it the
check refuses correct work, and a check that refuses correct work is one
people learn to skip.

## Data & interfaces

| Coordinate | What changes |
|---|---|
| a new script under `skills/evidence-check/scripts/` | the check: a range in, lost markers out, exit 1 while one stands |
| `bin/` | its wrapper, the way the sibling checks have one |
| `.github/workflows/hygiene.yml` | one leg on pull requests into `release/*` |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | the conflict sentence |
| `CONTRIBUTING.md` | the same sentence, pinned against it |
| `skills/evidence-check/SKILL.md` | what the new command is for and when it runs |
| `tests/` | the new module, and the structural case for A8 |
| `skills/evidence-check/scripts/evidence_check.py` | **unchanged.** The rider's question is not this work |

## What this repair cannot see

- **A correction that carries no marker at all.** The check is exactly as good
  as the convention, and the convention is prose. That is why the count above
  is in this document: 10 and 189 are what it watches, and a correction
  written without either word is invisible to it.
- **A correction lost anywhere but a merge.** Someone editing a row back to a
  superseded state in an ordinary commit produces the same byte-identical row
  with no parent to compare against.
- **Whether the surviving side was the right one.** Both sides can carry
  markers; the check reports what was dropped, and which resolution was
  correct stays a person's reading.
- **A squash.** A feature branch squashes into its release branch, so the
  merge commits this check reads exist only before that. It has to run at the
  pull request or not at all.

## Open questions → questions.md

Two rows need a person — whether the rider's `Checked` question is answered
here or stays where it is, and whether the new leg blocks a pull request or
reports. Both carry the assumption the build proceeds under.

Framed 2026-09-21 by the session, before the build.
