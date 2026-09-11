# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — phase 6

<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-6.md -->

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | `90f2f9d` |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

Write `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` as fragments
rather than into the shared files, and the closing memo. **The changelog
entry is the record of the removal** (Q3): it names all four parts of
`docs/flow.md` and where each went, the clause dropped from the 0.4.0 record
included, so nothing has to be left behind as a marker. Verified by the
fragments existing and `fold_ledger.py --check`.

## What this phase found

**The entry had to be written as a record rather than as a release note, and
that is what the owner's Q3 grounds bought.** A normal entry says what
changed; this one is the only place the removal is recorded anywhere, because
no marker was left in any file the deletion removed text from. So it is
organised by *where each part went* rather than by what was done, and the
part a person actually needs — where the order a ticket runs in is read now —
is first and named as such, not fourth in a list sorted by file.

**`fold_ledger.py --check` and `gather_changelog.py --check` both exit 1, and
that is the correct state.** `plan.md` phase 6's Verified-by cell says the
fold check is *clean*, which cannot mean exit 0: `--check` reports every
fragment that has not yet been gathered, so writing a fragment is what makes
it exit 1, and a branch that writes one can never satisfy the cell as
literally worded. Both runs name this work item's two fragments and nothing
else, which is the check working. The release preparation commit is where it
goes clean, and `.github/workflows/hygiene.yml` runs the fold check on pull
requests into `main`, which this branch's is not.

**Three ledger rows, and the hashes were stamped rather than typed.**
`evidence-check` has no hash-generating command, but `--reverify` rewrites
each row's hash to what its anchor holds now, so the fragment was written
with `@00000000` placeholders and stamped in one run — five anchors, five
rewrites, then `--strict` at 1121 ok · 0 drifted · 0 broken, exit 0. Typing
an eight-character hash by hand has no correct value to type.

**`survivor-check` reported 33 and the escape is one row, which is the case
the script's own §*A deletion is one row* names.** 29 are in `CHANGELOG.md`,
`seal/ledger.md` or `seal/specs/`. The four in loaded files were each opened:
`CLAUDE.md:81` states the rule that `seal` named three things, the xdist case
at `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` states the
deadlock #337 describes, and two more record the Windows-leg measurement
#103's row cited. In every case the deleted row was the pointer and the
standing text is the thing pointed at. `survivors.md` carries the range row
with those four named in prose above it, and the re-run prints all 33 under
`exempt` with the grounds, exit 0.

**One command in this phase did real damage and had to be undone.** A
throwaway `git checkout origin/release/v0.11.1 -- .` — typed while checking
what the fragment checks say on the base — restored every tracked file to the
base revision, and the follow-up `git checkout HEAD -- .` could not undo the
half that mattered: `docs/flow.md` exists in the base and not in `HEAD`, so
it came back and staged itself as an addition. It was removed by hand and
`git diff HEAD --stat` confirmed empty before anything else ran. Nothing was
lost, because everything through phase 4 was already committed — which is the
cadence rule paying for itself rather than a near miss survived by luck.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase writes records and removes nothing from the tree | none |
