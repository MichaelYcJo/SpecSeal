# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 6bc99584 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Records. `seal/ledger/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge.md`
with one row per new claim: the two flags and why, the restoration
predicate and its two callers, and the draft arm. Every row
`evidence_check.py` reports DRIFTED because of phases 1 to 3 is re-read
against the edit and re-stamped in its own file with a dated note, and its
claim is corrected in place where the edit made it false.
`seal/specs/…/changelog.md` written. Settle `questions.md` Q1 and Q4.

## What this phase found

**Q1: fifteen rows drifted, in seven files over twelve anchors, and every
claim still holds.** `evidence_check.py .` named the anchors. Each was re-read against the edit, given a
dated `Re-read 2026-09-25` note saying what moved and why the claim holds,
and re-stamped with `--ledger <that file> --reverify`. None needed a
`Corrected` note.

| File | Row | Anchor that drifted |
|---|---|---|
| `seal/ledger.md` | *Reading `Fixes checked by` on the last record alone makes `round-N` unreachable* | `chain_check.py#main` |
| `seal/ledger.md` | *A cell inside an HTML comment is not the row* | `chain_check.py#checked_by` |
| `seal/ledger.md` | *An unrecognised value is refused rather than read as a checker* | `chain_check.py#checked_by` |
| `seal/ledger.md` | *`Pass` beside `nobody` is grandfathered* | `chain_check.py#checked_by` |
| `seal/ledger.md` | *The boundary is `>=`* | `chain_check.py#checked_by` |
| `seal/releases/0.11.3.md` | R2, R5 | `chain_check.py#written_late` |
| `seal/releases/0.13.1.md` | the retired-declaration row | `chain_check.py#main` |
| `seal/releases/0.14.0.md` | G4 | `docs/review-chain-spec.md` §*Two records* |
| `seal/releases/0.14.0.md` | G5 | `chain_check.py#main` |
| `seal/releases/0.4.0.md` | *An unreadable round record cannot read as "no rows required"* | `chain_check.py#main` |
| `seal/releases/0.4.0.md` | the review-chain spec's two opt-in headings | `docs/commit-review-gate-spec.md` §*Review arm* |
| `seal/releases/0.8.0.md` | R1 | `chain_check.py#added_on_branch` and the delete-and-re-add case |
| `seal/releases/0.8.0.md` | R2 | `chain_check.py#written_late` |
| `seal/releases/0.9.3.md` | *The seam is the one the file's own headings drew* | `orchestration.md`, the whole file |

The `seal/ledger.md` row on the grandfathering (the fourth above) is the
one closest to false. Its evidence cell says a work item at or after
the cutoff *fails* on the pair, which is now true at ready and at an
unreadable state and not in a draft. The fixture it cites runs with no
payload, which is judged as ready, so the cell is still true of what was
executed. The note says so.

**A thirteenth row drifted from this phase's own notes.** `seal/releases/0.13.1.md`'s
row on five rows anchored into a retired `spec.md` anchors the
`### 1788331011` section of `seal/releases/0.4.0.md`, and the two notes
written into that section moved it. Re-stamping `0.13.1.md` before
`0.4.0.md` left it drifted again, so it took its own note and a second
`--reverify`. Re-stamp a file whose section another ledger anchors last.

**`spec.md`'s list of drifting rows was a guess, as it said.** It named
`seal/releases/0.9.5.md`, and no row there drifted. It did not name
`0.9.3.md`, the second `0.4.0.md` row, or the cross-ledger row above.

**Two records this work item wrote were refused by the records arm once the
fragment existed**, because the arm reads only work items carrying one:

- `spec.md` named two drifting rows as `chain_check.py#checked_by` and
  `chain_check.py#main`, each followed by `@` and its pre-edit hash, which
  read as stamps and are broken (the path is short). The two hashes were dropped from that bullet and the
  text is otherwise the framer's. The pre-edit hashes stand in the ledger's
  history.
- `phases/phase-3.md` names the renamed pin's old name, which the tree no
  longer carries. The line now carries `NAME NOT IN TREE`.

After both, `evidence_check.py .` and `evidence_check.py --strict .` exit 0:
2241 ok, 0 drifted, 0 broken; the records arm read 1 work item and 76 names.

**Q4: no textual collision in `chain_check.py`, one likely in a ledger
file.** Read at `fix/602-settle-retires-a-directory-main-has-not-seen-closed`
`127dbe64`: work item C has not edited `chain_check.py` against `7b557144`.
It does edit `seal/releases/0.14.0.md` lines 36, 39 and 45. This work item
edits lines 35 and 42 of the same file, and 35 and 36 are adjacent, so git
is likely to report a conflict there when C merges the release branch in.
It resolves hunk by hunk with both rows' notes kept, and `evidence_check.py`
run after the resolution (`CLAUDE.md`, the ledger paragraph).

**The ledger fragment** carries five rows, A1 to A5: the two flags, the
predicate, its two callers, the draft arm, and the orchestration sentence.
Each was stamped by `--ledger <fragment> --reverify` from placeholder
hashes.

**Narrow result, executed:** every module reading a ledger file this phase
edited, the fragment, or a work item's records (51, with
`test_a_row_points_by_content.py`): 2746 passed, 1 failed. The failure was
`test_a_record_states_what_the_tree_has.py::test_this_repositorys_own_records_state_nothing_the_tree_lacks`,
on this very record, which had quoted `spec.md`'s two short stamps whole.
Reworded, that module: 66 passed. `evidence_check.py --strict .` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the two `@hash` suffixes in `spec.md`'s *Data & interfaces* list of drifting rows | the ledger's own history, and the table above |
