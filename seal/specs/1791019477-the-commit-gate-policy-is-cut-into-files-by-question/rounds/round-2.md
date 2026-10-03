# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — review round 2

| Field | Value |
|---|---|
| Target SHA | b779daf233f5a166c71efd338c5e362c5983d468 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 744 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `70680f16cd75bbe20a1b4e716ca0e918c7838dbe..f7b31c42bf9c7ad8d55b4fa264e27f2bf4db42f6`, 3 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 4, F1's new sentence gives a false reason for `none`. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round. It targets `b779daf2` over round 1's fix range `8410e123..35a6d822`, the release merge `e8b487f0` (#742 only) and the close commit. It was asked:
- whether each of round 1's fixes holds, and whether any other live sentence says the `Over the ceiling` row goes away;
- whether the merge left the ledger, the corrections, the survivors and the fold checks clean;
- whether the close commit's dated citation at `round-1-report.md:141` is the right repair for a reviewer's coordinate into a unit the fix had to change.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 4 | F1's new reason is false: *the row stays and reads `none`, so `fold-check` still holds every document to the ceiling*; an absent row reads as an empty listing and the ceiling check runs on `Document line ceiling` alone | `docs/the-record-layout.md:179` | **fixed** `9a3db2eb` | fixed at 9a3db2eb; executed: with the row deleted, `fold-check` exits 0 on the tree and 1 on a padded arms file, the same output as with `none`; read: `fold_check.py#parse_over`, `#run`, `templates/config.md`'s *Absent* column |
| ⬜ 5 | ledger row C2's note says an absent row turns that half of the check off | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C2) | answered | corrected at `8d68574a`; executed: finding 4's probe. A record, so a correction |
| ⬜ 6 | the fix for ⬜ 3 split the K3 divergence row: K3 has three cells and its Grounds is a fifth cell on the D5 row | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/overview.md:27` | answered | corrected at `f7b31c42`; executed: cell count per table line; read: lines 27–28 against the diff of `35a6d822`. A record, so a correction |
| 🟢 | round 1's finding 1 is closed — F1 no longer says the `Over the ceiling` row goes away; it says the row stays at `none` | `docs/the-record-layout.md:177` | confirmed | read at `ac858e6c` and at `b779daf2`; `seal/config.md:13` is `none`. The sentence added beside it is finding 4 |
| 🟢 | C5 re-stamped in place with a dated Corrected note, its claim extended to the row | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C5) | confirmed | executed: `evidence-check --strict` exit 0, 0 drifted; `correction-check` exit 0; read: the note |
| 🟢 | the `survivors.md` row for 1790993138's `spec.md:116` is added and its quote stands there | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/survivors.md` | confirmed | executed: survivor-check with `--exempt` exit 0; without it, exit 1 naming only 1790815613's overview line 49, so this row excuses a place the check does not name today |
| 🟢 | no other live sentence says the `Over the ceiling` row goes away | live tree outside `seal/specs/`, `seal/releases/`, `CHANGELOG.md` | confirmed | executed: `git grep` over every *over the ceiling* line and nine removal phrasings; the one removal line, `fold_check.py:419`, says *Remove its entry* |
| 🟢 | round 1's finding 2 is closed — C1 and phase 1 name base 153 and say four of the seven lines name the file alone | ledger row C1; `phases/phase-1.md:68-76` | answered | read: base 152–153 against `docs/the-commit-gate-inside-git.md:127-130`, base 91, 199, 273, 274 against lines 66, 176, 251, 252; both carry a dated Corrected note; no anchor moved |
| 🟢 | round 1's finding 3 is closed — `overview.md` records D5's citation shape for the four lines | `overview.md:28` | answered | read: the row's text against D5 and the four lines. The table damage the edit caused is finding 6 |
| 🟢 | the merge `e8b487f0` touches no file this branch edits | `e8b487f0` | confirmed | executed: `git diff --name-status 35a6d822 e8b487f0`, six paths, all other work items' |
| 🟢 | the four checks over the merged tree pass | `b779daf2` | confirmed | executed: `correction-check --range origin/release/v0.18.0...HEAD` exit 0; `evidence-check --strict .` exit 0, 0 drifted, 0 refused; `survivor-check --range 2b1dcb1f...HEAD --exempt survivors.md` exit 0; `fold-check --root .` exit 0 |
| 🟢 | the close commit's rewrite of round 1's report line 141 is the right repair | `rounds/round-1-report.md:141` | confirmed | executed: the old line in place makes `evidence-check --strict` exit 2 with that line DRIFTED; read: a pin to the report's own target SHA, where a re-stamp would claim a reading nobody did. The records arm reads 0 stamps now |

## Paste-ready fixes

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
```
Corrected again <date> in round 2's fix pass (🟡 4): the sentence round 1's fix added said the row reading `none` is what keeps the ceiling check running; an absent row reads the same, and the paragraph now names `Document line ceiling` as the ceiling.
```
```
`none` rather than a deleted row, as `spec.md` D8 decided: `none` states the empty listing. **Corrected <date> in round 2's fix pass (⬜ 5):** this note said an absent row turns that half of the check off. It does not; `fold-check` reads an absent `Over the ceiling` row as an empty listing and still holds every document to the `Document line ceiling` (executed in round 2 with the row deleted). No anchor moved
```
```
| K3's `Re-read ·` count for the document's own anchors | Spec K3: "2 `Re-read ·` rows for the document's own anchors" (E9 and S2). Only E9 drifted. S2's `"Authority for"` minor anchor hashes the line it names, and D4 kept that line | one `Re-read ·` row for the document's own anchors, 12 for what K5 drifted | `evidence-check` named no drift on S2 before or after the `--reverify`; M1's row carries the whole count |
| D5's citation shape | Spec D5: "A positional reference that crosses the cut becomes a citation by file and section". Base 91, 199, 273 and 274 name the file alone — at `docs/the-commit-gate-inside-git.md:65-66` (91), and `:176`, `:251` and `:252` (199, 273, 274), which cite the parent by path only; 152 and 283–284 name file and section | the file alone for those four | 91 means the whole arms file. 199, 273 and 274 say *the PreToolUse reading*, which is what the parent chiefly holds, and 199 sits inside the unit G17 anchors, so a section there would move G17's re-pointed hash again. Recorded in round 1's fix pass (⬜ 3) |
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/the-record-layout.md:177` | round 1's 🟡 1 — fixed |
| round-1 | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C1) | round 1's ⬜ 2 — answered |
| round-1 | `docs/the-commit-gate-inside-git.md:176` | round 1's ⬜ 3 — answered |
| round-1 | `docs/the-commit-gate-inside-git.md`, `docs/the-review-and-parity-arms.md`, `docs/commit-review-gate-spec.md` | round 1's 🟢 — confirmed |
| round-1 | the three files | round 1's 🟢 — confirmed |
| round-1 | live tree | round 1's 🟢 — confirmed |
| round-1 | `skills/settle/scripts/fold_check.py#ceiling_problems` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/`, `seal/releases/` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-record-layout.md` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
