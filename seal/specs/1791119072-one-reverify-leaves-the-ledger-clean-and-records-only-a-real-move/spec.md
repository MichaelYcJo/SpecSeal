# Feature Specification: one `--reverify` leaves the ledger clean and records only a real move

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issues #774, #772 and #775, all raised by #771's review rounds (work item
`1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date`,
read at `refs/backup/0.18.1/local/fix/746-…`, `rounds/round-2-report.md` and
`rounds/round-3-report.md`). The writer they are about is #756's (work item
`1791076833-the-reverify-writer-records-before-it-restamps`, whose `spec.md`
W1–W10 still stand in this tree).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-pact.md` §*A signatory records a pact change* | A pact change is recorded where `--reverify` **moves the hash** of a row citing a clause, refuses a stale row whose code moved, or leaves a coordinate BROKEN. A move from a hash to the same hash is not a move, so #774's `h1 → h1` row is outside the trigger. |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, the `--into` paragraph: *a pact change is never lost* | Decides #774's old hash (D1 below). Dropping P3's row outright would lose the real move `h2 → h1`, so the fix changes which old hash is recorded and does not just suppress the row. |
| `skills/evidence-check/scripts/evidence_check.py#record_pact_changes` docstring: *a change that comes back after its revert is recorded* | A return to an earlier hash counts as a move. That is exactly P3's case seen from its newest reading. |
| `skills/evidence-check/scripts/evidence_check.py#family_view` docstring: `readings` are *every code coordinate on a member's line*; a citing row's citation is graded on its own | A citation is not a code coordinate. That is the ground for D3: re-stamping a citation is not a pact change. |
| `docs/the-evidence-ledger.md` §*A released row is read again…*, *Without the row, a released row is kept true where it stands*, and *Five things `--reverify` leaves at exit 0 while `--strict` exits 2*, fifth item | Without the freeze, `--reverify` re-stamps in place. Today the fifth item states the second-run behaviour #772 removes, so that sentence changes. A narrowed run names what it could not clear and exits 1, and D2's narrowed half follows that principle. |
| `skills/settle/SKILL.md` §*A standing statement has one shape*: the `Enforced by:` line *names what reads the rule* | Decides #775's `Enforced by:` question for this item (D6). |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file*, and the one-home rule `tests/test_no_passage_is_pasted_into_a_second_file.py` enforces | Decides D4. `templates/config.md` points at the pact doc rather than pasting its trigger. The round-3 paste-ready text would share a 15-word run with `docs/the-pact.md`, and that pair is not in `BASELINE`. |
| `seal/config.md` `Ledger frozen from` | This repository's own re-reads go into this item's fragment through `--into`. A released row is never re-stamped in place, so the 0.18.0:79 repair is a `Corrected ·` row (D7). |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Each defect is fixed across its class (enumerated below). Every changed sentence a person reads is pinned in the same commit, and every new case is seen red before it is committed. |

**One departure from the ticket, decided from the tree.** #774's checkbox asks
for *no record* where *a family whose newest reading is outranked and whose
code is unchanged*. Its own body says *nothing moved*. P3 (round 2 of #771,
executed) shows that something did move: the released row read `57f678c6`, a
newer re-read read `7069baf7`, and the code went back to `57f678c6`. The
ticket's fix would leave that revert unrecorded, which is the loss the policy
row above forbids. So P3's shape records `7069baf7 → 57f678c6`, and only a
move whose two hashes agree records nothing. Policy outranks the ticket
(`skills/implement/SKILL.md` §1).

## Scope

**In.**

- **D1 (#774): each move takes its old hash from the newest reading.** Every
  move `reverify_into` appends takes its old hash from the coordinate's newest
  reading (`family_view`'s `newest`). A row outside every family is its own
  newest reading. Today the old hash is the released member's
  `m.group("hash")`. This covers all four append sites: the written arm, the
  refusal arm, the `new is None` arm, and the BROKEN list `released_drift`
  returns.
- **D1 guard.** `record_pact_changes` drops any part whose old and new hashes
  agree. A ledger row with no part left records nothing and prints no
  `recorded` line.
- **D2 (#772): one unfrozen run re-stamps every citation it moves.** The
  in-place walk (`reverify`) visits each ledger after every released file its
  citing rows cite, in dependency order with ties kept in the default order.
  So a citation is hashed against the line the open plan will write, and one
  unnarrowed run leaves `--strict` at 0 drifted.
- **D2, narrowed run.** A run narrowed with `--ledger` may move a released
  line that a citing row outside the narrowing quotes. That run names the
  citing row on a `LEFT` line and exits 1, the way it already names a family
  it could not clear.
- **D3: a citation is not code.** Re-stamping a citing row's citation appends
  no move. So the citation re-stamp that D2 now makes inside one run never
  becomes a pact-change part. Under `Pact notify | always`, a row whose only
  move was its citation is not recorded.
- **D4 (#775): the two incomplete trigger statements are completed.**
  `templates/config.md` §*Pact*: the `Pact notify` paragraph stops restating
  when a change is recorded and points at `docs/the-pact.md` §*A signatory
  records a pact change*. Its table of values stays, because that table is
  this template's own content. The section comment above `record_pact_changes`
  in `evidence_check.py` names the refused stale row, in the round-3
  paste-ready wording. The ratchet reads no `.py` file.
- **D5 (#775): every changed sentence is pinned.**
  - The usage sentence (*A row `--into` refuses a `Re-read ·` row for a stale
    --checked is recorded too, by the run that refuses it (#746).*) and the
    skill clause (`skills/evidence-check/SKILL.md` §*Re-verifying is
    recomputing the hash*) join
    `test_the_home_and_the_usage_say_a_stale_row_is_left`, as round 3's two
    paste-ready parameters.
  - The new `templates/config.md` pointer is pinned.
  - D1's new sentence in `docs/the-pact.md` is pinned through
    `test_the_documents_say_what_the_writer_does`.
  - The rewritten fifth item and its lead-in in `docs/the-evidence-ledger.md`
    are pinned through `test_the_home_names_each_thing_no_re_read_clears`.
- **D6 (#775): the `Enforced by:` line names the new cases.** The line under
  `docs/the-pact.md` §*A signatory records a pact change*'s first paragraph
  gains `test_a_row_refused_for_a_stale_date_records_its_move_once`,
  `test_a_row_dated_after_today_has_its_move_recorded_before_its_correction`,
  and the case D1 plants.
- **D7 (#775): the 0.18.0:79 row is corrected, not re-read.**
  `seal/releases/0.18.0.md:79` claims *the trace goes in the Notes, on every
  row a re-stamp touched*. That claim gets a `Corrected ·` row in this item's
  fragment.
  - What holds: `reverify_into` writes `Re-read <date>` into the Notes of every
    `Re-read ·` row. Without the freeze, the policy re-stamps a released row in
    place *with a dated note* (`docs/the-evidence-ledger.md`, the *Without the
    row* paragraph).
  - What does not hold: the in-place `reverify` writes the date cell alone. The
    cited skill section names no Notes trace.
  - The build re-reads both and writes the narrowed claim (questions Q3).
- **This item's records.** Its fragment `seal/ledger/<this item's id>.md`, its
  `changelog.md` fragment, and `Re-read ·` rows (through `--into`) for the
  released rows whose cited units this item's edits drift.

**The class each defect belongs to, enumerated (§12).**

| Class | Instances | In scope |
|---|---|---|
| A pact-change part whose move is not a code move under the row | (a) `reverify_into` takes the released member's hash where the newest reading holds another: `h1 → h1` (#774, P3). (b) A citation re-stamp recorded as a part (unfrozen, in place). (c) Any writer passing old == new. | (a) D1 · (b) D3 · (c) the D1 guard |
| A re-stamp moves a line a citation quotes, and the run leaves the citation | (i) A fragment walked before the released file it cites (#772's pinned case). (ii) Without the freeze, a release file citing an older release file walked before it: `glob` sorts `0.10.0.md` before `0.9.0.md`. (iii) A narrowed run whose narrowing leaves the citing file out. | (i), (ii) D2's order; a fixed kind order would miss (ii) · (iii) D2's `LEFT` |
| The trigger stated without the refused row | `templates/config.md` §*Pact*, and the section comment in `evidence_check.py`. Round 3 enumerated these by `git grep`, and the other hits are true as written. | D4 |
| A sentence of the trigger unpinned | the usage, the skill | D5 |

**Out, each with its reason.**

- **The 0.18.1 hash churn.** `--reverify --checked` re-stamped about 13 rows in
  4 fragments that `--strict` read ok. It is not #772's mechanism. Read, not
  executed: the in-place `reverify` re-stamps every anchor whose own hash
  differs from the code, family-blind, while `--strict` grades a family member
  OK where a newer reading in its family holds the code. An outranked older
  `Re-read ·` row is therefore re-stamped and re-dated although no reader
  opened it. `seal/releases/0.18.1.md` holds three `Re-read · C4` rows at three
  hashes of `VERSIONS_OF_ANOTHER_PRODUCT`, which is that shape. Fixing it
  changes which rows the in-place writer touches, so it needs its own frame.
  Questions Q2 holds the default and the probe that confirms the mechanism.
  `seal/follow-up.md`'s row on *`--reverify` re-stamps every row that cites
  it* is the neighbouring class.
- **The note the in-place re-stamp does not write.** The *Without the row*
  paragraph says an unfrozen repository re-stamps *with a dated note*, and the
  checker writes none. D7 states this. Building the note changes the in-place
  writer's output for every unfrozen repository. That is a finding for the
  orchestrator to file, not this item's.
- **Codifying the `Enforced by:` rule in `skills/settle/SKILL.md`.** D6 applies
  the reading to this item's edit. Writing it down for every future edit is a
  rule change (questions Q1).
- **The five-things lead sentence's count.** It stays five. The fifth item's
  freeze half (a folded citing row whose cited release file was edited) still
  exits 0 under `--strict` 2. Only its unfrozen half changes.
- **`hooks/config.py`.** Sibling F (#759) owns the declaration reader. This
  item calls `declared_pacts` and does not change it.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1: an outranked unchanged coordinate (#774, P3) | **Given** a freeze. Released O1 dated 2026-09-01 at `serialize@h1` cites a pact clause. Another item's fragment re-reads it 2026-09-10 at `h2`. The code is back at `h1`. **When** `--reverify --ledger <release> --into F` runs with `--checked` 2026-09-12 (written arm) and 2026-09-04 (refusal arm). **Then** each records `serialize@h2 → @h1`, and neither records `@h1 → @h1`. | New case in `tests/test_a_signatory_records_a_pact_change.py`, parametrised over both arms. Red at the base, which records `@h1 → @h1` (P3). |
| S2: a part whose two hashes agree | **When** `record_pact_changes` is handed a move with old == new. **Then** no row is recorded and no `recorded` line is printed. With one such part beside a real part, only the real part is written. | New unit case, red at the base |
| S3: a BROKEN coordinate under an outranked reading | **Given** S1's family, with the unit then removed. **Then** the record names the newest reading's hash before `BROKEN`. | New case, red at the base. Read, not executed: a removed unit is BROKEN for every member, so `released_drift` picks the first released member and appends its own hash to the BROKEN list. |
| S4: one unfrozen run (#772) | **Given** no freeze. R and its fragment re-read M both read `handler` as it was. The code moves. **When** one `--reverify --checked` runs over every ledger. **Then** exit 0 and `--strict` exits 0. | `test_an_unfrozen_restamp_of_a_released_row_moves_the_line_its_re_read_cites` is rewritten to one run and renamed for what it now holds. It is red against the base, whose `--strict` exits 2. |
| S5: a release file citing an older one, unfrozen | **Given** a citing row folded into `seal/releases/0.10.0.md` that cites a row of `seal/releases/0.9.0.md`. The code moves. **When** one unnarrowed run. **Then** `--strict` exits 0. | New case. Red at the base, because the glob order walks 0.10.0 first. |
| S6: a narrowed run that leaves the citing file out | **Given** S4's tree. **When** `--reverify --ledger <the release file>`. **Then** a `LEFT` line names M's file and line and the repair (run it without `--ledger`), and the exit is 1. | New case, red at the base (exit 0, silent) |
| S7: a citation re-stamp is not a pact change | **Given** S4's tree, under `Pact notify | always`, on a branch with a `routing.md`. **When** one run. **Then** M's record row carries its code part and no part for its citation. R's row is recorded as before. | New case. Red at the base's second run, which records a citation part. |
| S8: the trigger, completed and pinned | The usage, the skill clause, the config pointer and the pact doc's new sentence are each pinned. Each pin fails with its sentence deleted. | `test_the_home_and_the_usage_say_a_stale_row_is_left`, `test_the_documents_say_what_the_writer_does`, and a config pin. §15 by deletion. |
| S9: no new pasted passage | `tests/test_no_passage_is_pasted_into_a_second_file.py` passes, and no pair's count rises | the module, run narrow |
| S10: the fold shape holds | The pact paragraph's `Enforced by:` line names D6's targets, and each one resolves | `tests/test_a_folded_statement_names_what_enforces_it.py` |
| S11: the ledger reads clean | `bin/evidence-check --strict --ledger seal/ledger/<id>.md` exits 0. The `Corrected ·` row over 0.18.0:79 names the narrowed claim's coordinates. | executed at the last phase |

## Data & interfaces

- **`reverify_into`'s `moves` tuples keep their shape:** `(ledger, row,
  coordinate, old, new-or-None)`. Only `old` changes, from the released member's
  recorded hash to the hash its newest reading carries. The record's
  `CODE_PART` shape is unchanged, so `pact-check` and `pact_changes` read the
  file exactly as before.
- **`reverify`'s signature is unchanged.** The order is computed from the
  ledgers it is handed, using the citations their rows carry. The `LEFT` line
  for S6 is printed by `main` after the walk, beside the existing narrowed-family
  `LEFT`.
- **Moves recorded before this release keep their old hash.** No migration
  runs: a record is permanent and never edited.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

Framed 2026-10-04 by framer, before the build.
