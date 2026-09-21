# 1789956662-the-gate-and-ci-ask-about-different-ranges — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | d1b6b757 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The gate says what it compared against: the panel's ref row, the moved-line,
and the failure form's base. A4, A5, A6, A7 — each red when its branch is
deleted (§14). A6 asserts the rendered panel, not only `panel`'s rows,
because a value is cut at 23 columns.

## What this phase found

**Two of the four rows would have passed against the tree they were written
for, and only a mutation says otherwise.** A4 asserts the ABSENCE of the
moved-line, so before the line existed it passed for the wrong reason; A7's
wiring landed in phase 2, because `base` is a `Base` from the resolution
onward and the failure form needs a string. Both are shown red by the
mutation their own phase names — the line printed unconditionally, and the
failure form handed `base.given` — which is `agent-contract` §15's second
spelling, *with the sentence it pins deleted*.

**W1 is answered, and the answer is narrower than its default.**
`questions.md` W1 expected the printed line to be the authoritative statement
with the panel carrying a short form. The printed line is authoritative only
where resolving moved the answer, because A4 requires silence where the two
agree. Recorded as a divergence in `overview.md` rather than closed by
printing on every run, which A4 refuses.

<!-- CORRECTED at round 1, finding 5. Two sentences stood here and both are
gone rather than reworded, because both were about a cost this phase left
open and round 1 closed.

The first said a ref longer than 23 columns *is cut there with nothing
printed beside it*. It was: `seal_stamp.letter` cut at the frame with no
marker, so `origin/release/2026-09-21-hotfix` rendered as
`origin/release/2026-09-` and read as a whole ref. The gate now elides before
the frame does and keeps the tail — `...se/2026-09-21-hotfix`.

The second said *The reader still has the commit, which is what the seal
asserts*, which was this phase's argument for accepting the cut. The reader
now has the elided ref as well, so the argument is not merely weaker, it is
about a state that no longer arises.

Corrected in place with the round and the finding named, never deleted
silently, the same way `phases/phase-4.md`'s over-strong sentence is: a
record of a past state that quietly becomes true is a record nobody can
audit, and the two phase records are meant to read alike on this. -->

**The panel's cut was this phase's open cost, and it did not stay open.**
`broad_gate.PANEL_VALUE_WIDTH` now states where the frame cuts and a case
measures `seal_stamp.letter` to hold it there.

**The distance is read with `rev-list --count --left-right`, not with two
counts.** One call gives both sides of the symmetric difference, and the
order is *what the given spelling holds that the resolved one does not*, then
the reverse — so `ahead` is the second field. The line drops the distance
rather than the whole sentence where that call comes back unusable, because
the two SHAs are the part a reader acts on.

**The panel's contract moved from a string to the `Base`.** `panel` had one
caller in the whole tree, so the change costs nothing, and handing it the
object is what lets the row name the ref without a second argument that a
later caller could fill inconsistently — the same reasoning `seal_record`'s
docstring already gives for taking one `base` and not two.

**§14's documents are phase 5's, on purpose.** The rule asks that a change to
what a person reads ship with its documentation and its pin in the same
commit. The pin is here; `agents/sealer.md` and `skills/verify/SKILL.md` are
phase 5, and the branch squashes into one commit, which is the unit this
repository actually merges.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the panel's bare `base <sha>` with nothing saying which ref it came from | the `from` row beside it, and the printed line where resolving moved the answer |
