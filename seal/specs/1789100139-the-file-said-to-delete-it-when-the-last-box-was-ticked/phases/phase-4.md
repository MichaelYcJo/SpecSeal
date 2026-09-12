# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — phase 4

<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `89f4f8a` |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

Delete `docs/flow.md`. Check `seal/ledger.md` for a row whose anchor this
removes and mark it REMOVED if one exists. Verified by `grep -rn "flow\.md"`
over the tracked tree returning only records, and by `bin/evidence-check`.

## What this phase found

**No ledger row is anchored on the deleted file, so nothing is marked
REMOVED.** `grep -n "flow\.md#"` over `seal/ledger.md` returns nothing: all
five mentions sit in a Notes cell, and a Notes cell is not what
`CLAUDE.md` §*a change writes fragments* means by a row a change *cites* —
an anchor is `path#unit@hash`, and none of the five is one. The rule's own
words are *a row whose anchor a change removes*, and there is no such row.

**Two anchors drifted, and neither is the deleted file's.** They are units
this branch edited in phase 3: `tests/test_release_hygiene.py#test_no_loaded_
file_names_a_version_at_or_above_the_running_one` (cited by two rows, R1 and
R3 of the release-hygiene work item) and `skills/verify/scripts/broad_gate.
py#quote` (S15 of the sealer's). Both were re-read, both claims still hold —
the exemption count R1 states is three MECHANISMS rather than four entries,
and `quote`'s argument is about a platform branch that did not change — so
each was re-verified with `bin/evidence-check --reverify` and its Checked
date moved to 2026-09-11 with a sentence saying what was re-read.

**`--reverify` recomputes the hash and does not touch the date, and the two
are different acts.** The command reported `08730484 -> 98c5bec1` and
`b6b2caf6 -> 147ff2d4` and left both `Checked` cells where they were, at
2026-09-08 and 2026-09-10. `CLAUDE.md` says that column holds the date
somebody read the code, so a row re-verified by the command alone carries a
fresh hash and a stale reading date — which reads as *this was checked on the
8th* about text that did not exist then. The dates were moved by hand.

**One ledger Notes cell was a survivor and the other four are not.** S15's
note quoted *`docs/flow.md` #103's class made out of the fix for it* — the
same sentence phase 3 corrected in `broad_gate.py`'s own docstring, standing
in a second place, which is exactly #180's class and exactly what
`survivor-check` exists to find. It is corrected to *#103's class*. The other
four mentions are dated observations about a past state — the subject of a
commit, a corpus count taken at `86e140f`, what a file held on 2026-09-08 —
and a dated observation does not stop being true when its subject is
deleted. They are left standing, which is the same reason `CHANGELOG.md` and
`seal/specs/` are out of scope.

**The exemption entry and the deletion are one commit, which is a divergence
from `plan.md`.** Phase 3 was to remove `"docs/flow.md"` from
`RECORDS_OF_A_MOMENT`; the measurement in phase 3's record is why it is here
instead. Seven offending lines live in that file, so a commit dropping the
entry while the file is still tracked leaves the check red, and a commit that
does not stand on its own is what `skills/implement/SKILL.md` §2 refuses.

**Removing the entry made a count in the comment beside it wrong, and
nothing would have caught that.** The `docs/experiments/` comment reads *the
same argument the three exact paths above already carry*; there are two now.
No case reads that comment, no check counts the entries, and the sentence
would have sat there being wrong — the same class as the step-2 heading in
phase 2, a number describing a list that shrank underneath it.

**S6 holds with one survivor the spec does not list, and `plan.md` predicted
it.** `git grep -l "flow\.md"` returns `CHANGELOG.md`, 150-odd files under
`seal/specs/`, and `seal/ledger.md` — four mentions in the last. `spec.md`
S6 names only the first two; `plan.md` §Technical context names all three
and calls the ledger a record. The more specific reading was taken. Nothing
loaded names the path.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/flow.md`, 120 lines | Split four ways by this work item: the three numbered steps to `skills/implement/orchestration.md`, the sizing rule to `docs/issues-and-milestones.md`, the 18 checkbox rows and their grounds to the tracker (phase 5, already closed), and the two rules about maintaining the file itself to nowhere — they end with it. The changelog fragment is the record of all four |
| `"docs/flow.md"` from `tests/test_release_hygiene.py#RECORDS_OF_A_MOMENT` | Nowhere. Measured: no other loaded file needs it. Two exact paths and one prefix remain, each with its own argument beside it |
| The phrase *`docs/flow.md` #103's class* from `seal/ledger.md`'s S15 note | Corrected in place to *#103's class*, matching the docstring phase 3 repaired |
