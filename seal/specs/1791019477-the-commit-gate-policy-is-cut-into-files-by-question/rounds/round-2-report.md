# Round 2 report — the commit gate's policy is cut into files by question (#727)

| Field | Value |
|---|---|
| Round | 2, verifying round 1's fixes |
| Target SHA | b779daf2 |
| Fix range | `8410e123..35a6d822`, three commits; then the merge `e8b487f0` of `origin/release/v0.18.0` at `9511f6cd`; then the close commit `b779daf2` |
| Ran by | specseal:warden on claude-opus-5-5 |

This round's target is the diff of round 1's fixes, the merge after them and
the close commit, not the branch. Every probe ran in a `git clone --no-local`
of the worktree at `b779daf2`, under the round's scratch directory. Nothing
was written in the worktree but this file. Carried from round 1, not
re-established: the S1 move probe's result, the citation resolver's 21
citations, and the 9 rows #742 re-stamps. Re-derived: every verdict below.

## What the account claimed, and what the code showed

- **🟡 1: F1 now says the row stays at `none`** (commit `ac858e6c`). True.
  `docs/the-record-layout.md:177-181` says the entry went with the cut and the
  row stays and reads `none`, and `seal/config.md:13` holds `none`. The
  sentence that said the row goes away is gone. But the replacement adds a
  reason, *so `fold-check` still holds every document to the ceiling*, and
  that reason is false. Finding 4.
- **C5 is re-stamped with a dated Corrected note.** True. Its first anchor
  moved to the hash of the edited section, `evidence-check --strict` names it
  ok, and the note reads *Corrected 2026-10-03 in round 1's fix pass (🟡 1)*.
  The claim gained the clause about the row, which holds.
- **The `survivors.md` row for 1790993138's `spec.md:116` was added.** True,
  and the quote stands at that line. Round 1 predicted that survivor-check
  would name the place. It does not: without `--exempt`, survivor-check over
  `2b1dcb1f...HEAD` names only 1790815613's overview line 49, as before the
  fix. The spec line shares one run of words with the removed sentence, and
  the floor of 1.6 needs two independent phrases. The row is accurate and
  inert; nothing is wrong with keeping it.
- **No other live sentence says the row goes away.** Re-derived by
  `git grep` outside `seal/specs/`, `seal/releases/` and `CHANGELOG.md`: every
  line naming *over the ceiling* (30 lines), and the phrasings *row goes
  away*, *row went*, *row is removed*, *remove/delete/drop the row*, *entry
  goes away*, *goes away in the same change*, *take the row out*, and
  *de-list* or *off the list* near *ceiling*. None says the `Over the
  ceiling` row goes away. The one line about removal,
  `skills/settle/scripts/fold_check.py:419`, says *Remove its entry*, which
  is right.
- **⬜ 2: C1 and phase 1 now name base 153 and the four file-only lines.**
  True. I read base 152–153 against `docs/the-commit-gate-inside-git.md:127-130`
  and base 91, 199, 273 and 274 against lines 66, 176, 251 and 252. 153's
  words are kept, and the four name the file alone. Both records carry a
  dated Corrected note, and C1's anchors did not move.
- **⬜ 3: `overview.md` records the D5 divergence.** The row's text is right.
  The edit that added it split the K3 row: K3's Grounds cell moved to the end
  of the new D5 row. Finding 6.
- **The merge is clean.** `e8b487f0` against its first parent touches only
  other work items' files (1790993137, 1790993138, 1790993139, 1791019421).
  None of them is a file this branch edits.
- **The close commit's edit to round 1's report.** Executed: with the old
  line 141 put back in the clone, `evidence-check --strict` exits 2 and names
  that line DRIFTED. The coordinate pointed into the unit the 🟡 1 fix had to
  edit, so a repair was owed. My judgement is below.

### The close commit's edit to round 1's report

The repair is the right kind. Round 1's reviewer pointed at the section as it
stood at `e2f5270f`, and three repairs were possible.

- **A re-stamp to the new hash.** This makes the report claim its author
  read text written after the round ended. It is the one repair that makes
  the report false.
- **An exemption marker.** The checker's exemptions cover names, not stamps,
  and a marker would hide the coordinate rather than keep it.
- **A citation by file and section pinned to the report's own target SHA.**
  This is what `b779daf2` wrote. The report's header and its proof block
  already name `e2f5270f` as the state everything was read at, so the pin
  says nothing the report did not already say. Nothing re-hashes it.

One thing is missing. The file does not say that someone other than its
author rewrote that line; only the commit message does. A reader of the
report alone cannot tell. That is not worth a finding. `round-1.md` copies
no prose from that paragraph, so the record and the report do not disagree.
The class is closed by construction: the records arm reads 0 stamps in this
work item's records at `b779daf2`, so no other coordinate in them points into
a unit the fixes changed. This report writes no stamp, for the same reason.

## Findings from execution

### 🟡 4 — F1's new reason is false: an absent `Over the ceiling` row holds every document to the ceiling too

`docs/the-record-layout.md:179-181`: *The row stays and reads `none`, so
`fold-check` still holds every document to the ceiling.*

The *so* says the row reading `none` is what keeps the ceiling check running.
It is not. `skills/settle/scripts/fold_check.py#parse_over` returns an empty
listing for an absent row exactly as it does for `none`. The ceiling check in
`skills/settle/scripts/fold_check.py#run` runs whenever the
`Document line ceiling` row is declared, whatever the `Over the ceiling` row
says. No line is printed about the absent row, either.
`templates/config.md`'s table gives the absent value as *nothing is listed*,
which matches the code.

Executed in the clone. With the `Over the ceiling` row deleted from
`seal/config.md`:

- `fold-check` on the real tree exits 0 and prints the same two lines as
  with `none`;
- with `docs/the-review-and-parity-arms.md` padded to 1,450 lines it exits 1
  and names that document over the ceiling of 1000, the same output as with
  `none`.

Both files were restored by `git checkout`.

Why it matters: this paragraph is the policy the next split reads, and it is
marked built. It teaches a mechanism the code does not have. The ceiling
lives in `Document line ceiling`, and a reader who takes this sentence at its
word looks for the guarantee in the wrong row. The defect came in through
round 1's paste-ready fix, which carried round 1's own grounds for 🟡 1. Those
grounds said an absent row *turns that half of `fold-check` off with one
printed line*. That was never true of this row. Round 1's finding still
needed its fix: the old sentence said the row was gone, and it was not.

The same false reason stands in three records. Ledger row C2's note is
finding 5. `spec.md` D8's grounds and round 1's 🟡 1 grounds record the
decision and the round as they were made, so I leave them.
`templates/config.md:437-441` and the docstring at
`skills/settle/scripts/fold_check.py:35-38` say that an absent row turns its
check off. That is true of the two rows that govern a check, and those
sentences predate this branch.

The fix edits the section C5 anchors again, so C5 is re-stamped in place in
the same commit. The round 1 report's citation at line 141 is pinned to
`e2f5270f` and does not move.

## Findings that are corrections to the records

### ⬜ 5 — Ledger row C2 gives the same false reason for `none`

`seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md`,
row C2, note cell: *`none` rather than a deleted row, because an absent row is
not declared and turns that half of the check off (`spec.md` D8).* Finding 4's
probe shows an absent row turns nothing off. The claim cell is right, because
it says only that `none` lists nothing and the check runs. This row folds into
a released file that is never edited again, so the correction is cheapest
now. No anchor moves, because the note is not hashed.

### ⬜ 6 — The fix for ⬜ 3 split the K3 row of the divergence table

`seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/overview.md:27-28`.
The table has four columns. Line 27, the K3 row, now has three cells; its
Grounds, *`evidence-check` named no drift on S2 before or after the
`--reverify`; M1's row carries the whole count*, sits as a fifth cell at the
end of line 28, the new D5 row. A markdown renderer drops a fifth cell, so the
rendered page shows K3 with an empty Grounds and loses that sentence. Counted
by `awk` with the pipe as separator: lines 22–26 hold 4 cells (line 24 counts
one more, its quoted pipe), 27 holds 3, 28 holds 5.

## Regression tests to plant

None owed. Finding 4 is a sentence about a mechanism. A pin of its wording
holds one phrasing, and the mechanism is already held by
`tests/test_a_document_has_room_for_the_next_fold.py`, whose case that runs
with an empty `Over the ceiling` value is the code's own statement that an
empty row lists nothing.

## Facts for the evidence ledger

One, which ⬜ 5's paste carries into C2's note: an absent `Over the ceiling`
row and `none` read the same to `fold-check`. Executed in round 2; the anchor
is `skills/settle/scripts/fold_check.py#parse_over`, which C2 does not cite
today. Whether to add it is the fixer's call. C2 already cites
`skills/settle/scripts/fold_check.py#ceiling_problems`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 4 | F1's new reason is false: *the row stays and reads `none`, so `fold-check` still holds every document to the ceiling*; an absent row reads as an empty listing and the ceiling check runs on `Document line ceiling` alone | `docs/the-record-layout.md:179` | open | executed: with the row deleted, `fold-check` exits 0 on the tree and 1 on a padded arms file, the same output as with `none`; read: `fold_check.py#parse_over`, `#run`, `templates/config.md`'s *Absent* column |
| ⬜ 5 | ledger row C2's note says an absent row turns that half of the check off | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C2) | open | executed: finding 4's probe. A record, so a correction |
| ⬜ 6 | the fix for ⬜ 3 split the K3 divergence row: K3 has three cells and its Grounds is a fifth cell on the D5 row | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/overview.md:27` | open | executed: cell count per table line; read: lines 27–28 against the diff of `35a6d822`. A record, so a correction |
| 🟢 | round 1's finding 1 is closed — F1 no longer says the `Over the ceiling` row goes away; it says the row stays at `none` | `docs/the-record-layout.md:177` | confirmed | read at `ac858e6c` and at `b779daf2`; `seal/config.md:13` is `none`. The sentence added beside it is finding 4 |
| 🟢 | C5 re-stamped in place with a dated Corrected note, its claim extended to the row | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C5) | confirmed | executed: `evidence-check --strict` exit 0, 0 drifted; `correction-check` exit 0; read: the note |
| 🟢 | the `survivors.md` row for 1790993138's `spec.md:116` is added and its quote stands there | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/survivors.md` | confirmed | executed: survivor-check with `--exempt` exit 0; without it, exit 1 naming only 1790815613's overview line 49, so this row excuses a place the check does not name today |
| 🟢 | no other live sentence says the `Over the ceiling` row goes away | live tree outside `seal/specs/`, `seal/releases/`, `CHANGELOG.md` | confirmed | executed: `git grep` over every *over the ceiling* line and nine removal phrasings; the one removal line, `fold_check.py:419`, says *Remove its entry* |
| 🟢 | round 1's finding 2 is closed — C1 and phase 1 name base 153 and say four of the seven lines name the file alone | ledger row C1; `phases/phase-1.md:68-76` | answered | read: base 152–153 against `docs/the-commit-gate-inside-git.md:127-130`, base 91, 199, 273, 274 against lines 66, 176, 251, 252; both carry a dated Corrected note; no anchor moved |
| 🟢 | round 1's finding 3 is closed — `overview.md` records D5's citation shape for the four lines | `overview.md:28` | answered | read: the row's text against D5 and the four lines. The table damage the edit caused is finding 6 |
| 🟢 | the merge `e8b487f0` touches no file this branch edits | `e8b487f0` | confirmed | executed: `git diff --name-status 35a6d822 e8b487f0`, six paths, all other work items' |
| 🟢 | the four checks over the merged tree pass | `b779daf2` | confirmed | executed: `correction-check --range origin/release/v0.18.0...HEAD` exit 0; `evidence-check --strict .` exit 0, 0 drifted, 0 refused; `survivor-check --range 2b1dcb1f...HEAD --exempt survivors.md` exit 0; `fold-check --root .` exit 0 |
| 🟢 | the close commit's rewrite of round 1's report line 141 is the right repair | `rounds/round-1-report.md:141` | confirmed | executed: the old line in place makes `evidence-check --strict` exit 2 with that line DRIFTED; read: a pin to the report's own target SHA, where a re-stamp would claim a reading nobody did. The records arm reads 0 stamps now |

## Executed probes

| What was run | Result |
|---|---|
| `bin/correction-check --range origin/release/v0.18.0...HEAD` | exit 0: one merge examined, no correction marker dropped, no released ledger file changed |
| `bin/evidence-check --strict .` | exit 0: 4080 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| `bin/survivor-check --range 2b1dcb1f...HEAD --exempt` this item's `survivors.md` | exit 0: one exempt place, 1790815613's overview line 49 |
| `bin/survivor-check --range 2b1dcb1f...HEAD`, no exemption | exit 1: the same one place; 1790993138's `spec.md:116` is not named |
| `bin/fold-check --root .` | exit 0: 157 statements, 18 documents, 0 listed over the ceiling |
| a one-file probe, run once and deleted: `Over the ceiling` row deleted from `seal/config.md`, `fold-check` on the tree, then with the arms file padded to 1,450 lines, then with the row restored | absent row: exit 0 and the same two lines; padded: exit 1 naming the arms file, absent row and `none` alike; both files restored, clone clean |
| round 1's report at `35a6d822` put back in the clone, `bin/evidence-check --strict .` | exit 2: line 141 DRIFTED, the only drift; file restored |
| `awk` cell count over `overview.md`'s tables, the pipe as separator | 4 cells on lines 22–26 (24 counts its quoted pipe), 3 on 27, 5 on 28 |
| `git grep` over the live tree for the row going away, nine phrasings | no live sentence says the `Over the ceiling` row goes away |
| `bin/test -q` over the line-wrap, fold-room, no-real-identifiers, ledger-rules and ledger-fold modules | 159 passed |
| the broad gate: full suite, repository-wide lint, typecheck | not yet. It is the sealer's, run once after the rounds settle, and nothing in this round ran it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 4

In `docs/the-record-layout.md`, replace the paragraph after F1's table:

```
Each part answers one question — what git decides, what the text reading
decides, what each arm wants. Built, the parent is 586 lines, the commit gate
inside git 254 and the arms 250, each under the ceiling of 1,000. Fold markers
went across whole, and the `Over the ceiling` entry went with the cut in the
same change. The row stays and reads `none`, which says the listing is empty.
The ceiling itself is the `Document line ceiling` row, which `fold-check`
holds every unlisted document to (`docs/the-evidence-ledger.md` §*The fold,
and what tells it from a deletion*).
```

Then re-stamp C5 in place (`bin/evidence-check --reverify --ledger
seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md
--checked <date>`), and extend its Corrected note with one sentence:

```
Corrected again <date> in round 2's fix pass (🟡 4): the sentence round 1's fix added said the row reading `none` is what keeps the ceiling check running; an absent row reads the same, and the paragraph now names `Document line ceiling` as the ceiling.
```

### ⬜ 5

In row C2 of this item's ledger fragment, replace the note cell's second
sentence:

```
`none` rather than a deleted row, as `spec.md` D8 decided: `none` states the empty listing. **Corrected <date> in round 2's fix pass (⬜ 5):** this note said an absent row turns that half of the check off. It does not; `fold-check` reads an absent `Over the ceiling` row as an empty listing and still holds every document to the `Document line ceiling` (executed in round 2 with the row deleted). No anchor moved
```

### ⬜ 6

In `overview.md`, replace lines 27 and 28 with:

```
| K3's `Re-read ·` count for the document's own anchors | Spec K3: "2 `Re-read ·` rows for the document's own anchors" (E9 and S2). Only E9 drifted. S2's `"Authority for"` minor anchor hashes the line it names, and D4 kept that line | one `Re-read ·` row for the document's own anchors, 12 for what K5 drifted | `evidence-check` named no drift on S2 before or after the `--reverify`; M1's row carries the whole count |
| D5's citation shape | Spec D5: "A positional reference that crosses the cut becomes a citation by file and section". Base 91, 199, 273 and 274 name the file alone — at `docs/the-commit-gate-inside-git.md:65-66` (91), and `:176`, `:251` and `:252` (199, 273, 274), which cite the parent by path only; 152 and 283–284 name file and section | the file alone for those four | 91 means the whole arms file. 199, 273 and 274 say *the PreToolUse reading*, which is what the parent chiefly holds, and 199 sits inside the unit G17 anchors, so a section there would move G17's re-pointed hash again. Recorded in round 1's fix pass (⬜ 3) |
```

Needs a fix: yes — 🟡 4, F1's new sentence gives a false reason for `none`.

Loses a record or crashes: no

The broad gate has not come due: finding 4 is open. Once it is fixed and
closed, the sealer's spawn is what comes due.

## Proof block

Opened in this round, at `b779daf2` unless said otherwise:

- `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/`: `rounds/round-1.md`, `rounds/round-1-report.md` (and its line 141 at `35a6d822`), `overview.md` (lines 1–40), `survivors.md`, `spec.md` (D8, items 4–8 of the scope, K5 table rows 124–135), the diff of `phases/phase-1.md`
- `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` rows C1, C2, C5 (in the fix diff)
- `docs/the-record-layout.md` (lines 172–182, and every *ceiling* line), `docs/the-evidence-ledger.md` (lines 290–312), `docs/the-commit-gate-inside-git.md` (lines 60–70, 126–131, and the lines naming the parent or the arms file), base `docs/commit-review-gate-spec.md` lines 91, 151–154, 199, 273–274
- `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/spec.md` lines 110–120
- `skills/settle/scripts/fold_check.py` (module docstring 30–45, `ceiling_problems` 405–425, `row_value`, `parse_over`, `declared`, `run`), `skills/code-review/scripts/survivor_check.py` (pool notes 120–135, 168–180, `records_a_past_state`), `templates/config.md` (420–450), `skills/settle/SKILL.md` (224–236), `skills/config/SKILL.md` (118–128)
- the diffs of `8410e123..35a6d822`, of `e8b487f0` against its first parent (the two shared-file hunks read), and of `b779daf2`
