# 1790835050-the-delegated-note-compares-what-it-prints — phase 2

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8fb65924 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 2: the records. The seven rows anchored at `report_spawns`
re-read against the diff and re-stamped by `evidence-check --reverify
--checked 2026-10-01`, row 13 of `seal/releases/0.9.5.md` with a `Re-read
2026-10-01` note on what moved; the ledger fragment with the new claim
anchored at the fixed unit and the case; `changelog.md` naming the band
(57.0, 60), that every other threshold comparison in the module was checked,
and the batching line's `tools_per_turn <= 1.0` as checked and left with the
reason; this record and the Status cells. The spawn prompt added: re-stamp
with `--ledger <that file>`, and write `overview.md`.

## What this phase found

**`questions.md` Q2: seven, exactly.** Before re-stamping, the whole-tree
check reported one drifted coordinate in each of `seal/releases/0.9.5.md` and
`seal/releases/0.11.3.md` — it names a coordinate once per file, not once per
row. `--reverify --checked 2026-10-01 --ledger <file>`, run on each file
alone, moved the hash in seven rows and no other (`git diff` counted seven
removals of the old hash and seven additions of `cd336642`). Each row was read
against the diff before the run; none of the seven claims became false, so
none takes a `Corrected` note.

**Every drifted row got a dated note, not only row 13.** `CLAUDE.md`'s repo
rule says a drifted row is re-stamped *with a dated note*, and the plan named
a note for row 13 alone. Policy outranks the plan, so all seven carry a
`Re-read 2026-10-01 by work item 1790835050 (#701)` sentence saying which
part of `report_spawns` they are about and that the edit left it alone. Row
13's says what moved: the disclosure now prints on the printed minute, its
sentence is unchanged, and its presence moves only for a maximum in (57.0, 60)
seconds. Rows 16 and 45 already carried 2026-10-01 in their `Checked` cell
from #640's phase 4; the tool left the cell as it was. `overview.md` records
the divergence.

**Writing the fragment made this work item live to the records arm, and two
lines of the frame then failed it.** `evidence-check` reads an unshipped work
item's `spec.md`, `plan.md`, `overview.md` and phase records once its ledger
fragment exists. `spec.md` §*Grounding* and `plan.md` §*Technical context*
spelled the old anchor as a stamp with a bare file name, and the check
refused both at exit 2 (`file not found — same name at
skills/verify/scripts/session_cost.py (content differs)`). Each line now names
the full path without a hash and gives `15595f59` as the hash when framed, so
the sentence says what it said without asserting a stale anchor. This
phase's own records avoid the stamp form for the same reason.

**The new claim, D1**, anchors at `report_spawns` and at the case
`test_the_delegated_note_follows_the_minute_the_column_prints`, both stamped
by `--reverify` on the fragment alone (the case's hash went in as a
placeholder and the tool wrote it). The row names no line number.

**Verified, executed:** `evidence_check.py .` over the tree before this
phase's commit, exit 0 read directly, `3312 ok · 0 drifted · 0 broken`, and
the records arm `5 work items read · 0 refused`; `correction_check.py --range
origin/release/v0.17.0...HEAD`, exit 0, no merge commit in the range;
`survivor-check --range e83db346..HEAD`, exit 0, 13 removed sentences and no
removed wording still standing. Read: the changelog fragment against
`seal/specs/1790815612-…/changelog.md`'s shape — one bullet, a bold
symptom-first lead with the issue number, then what moved, the band, and the
class sweep's result.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the old hash `15595f59` on the seven rows | replaced in place by `cd336642`, each row with a dated re-read note |
| the frame's two stamps of the old hash in `spec.md` and `plan.md` | respelled in place as a full path and a hash when framed; `overview.md` §*Where spec and implementation diverged* |
