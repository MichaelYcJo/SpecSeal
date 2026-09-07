# 1788761915-a-record-states-what-nothing-reads — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `8b82c39` |
| Ran by | unknown — the spawning session named no model in the prompt, and the row is the orchestrator's to fill |

## What this phase was asked

#207 — `new` prints the bound it can already compute, from the previous
record's floor row and the walk `chain_check` implements. Round 1 prints
nothing. Cases for the three states, each seen red first.

## What this phase found

**Which floor record the bound is keyed to is the whole of the design, and
`plan.md` did not name it.** It is the **earliest** earlier record whose floor
row reads `no`, not the latest. Keyed to the latest, the walk restarts at
every record it stops at — because every record it stops at is itself a record
that met the floor — which is exactly the *unbounded by construction* failure
`chain_check.stopping_floor` records in its own docstring for the count. The
discriminating case is round 1 met the floor · round 2 closed on a fix ·
round 3 met the floor again: from the earliest, writing round 4 ends the run;
from the latest, it reads as having a reopening left.

**Three states and no fourth, which is what *round 1 prints nothing* is
really about.** A run whose floor has not been met yet is the same silence as
round 1: the cap governs there and the cap is not this line's subject. So is
a record that cannot be read and a floor row outside the vocabulary —
`stopping_floor` reports both at the gate, and a second reader inventing a
sentence about them here would be #207's own failure one file over.

**The bound is read from disk, where `chain_check` reads from `HEAD`.** The
two are not inconsistent. `read_record` asks git because it is enforcing at a
pull request, where the working tree is precisely what CI cannot see; this
line is printed to whoever just ran the command, and the records in front of
them are the ones on disk — including a record written by a `new` that has
not been committed yet.

**The message carries `chain.CAPPED_EXIT` verbatim.** A line saying the run
ends and not what to do with what is still open is the wall the refusal at
the gate already refuses to be, and one spelling of the exit is what keeps
the two from drifting. A mutation dropping it turns a case red.

**Eight mutations, all killed**, including the latest-floor reading, a floor
of `yes` counting as met, and printing the reopening line where no record met
the floor at all.

**A round 2 and later cannot assert `code == 0` in this suite's `generate`.**
The exit code is `chain_check`'s over a scratch fixture whose earlier records
carry the starting `Contract changes` and `New units` values, so it is 1 for
reasons that have nothing to do with what `new` printed. The existing
multi-round cases in that file already assert on the record rather than the
code; these do the same and read the printed line.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
