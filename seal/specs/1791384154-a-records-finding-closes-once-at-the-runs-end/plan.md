# Implementation Plan: a records-level finding closes once at the run's end (#837)

<!-- seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

A ⬜ (a note, `skills/code-review/SKILL.md` §*Findings format*) stops being
owed a row in each round's fix table, can never close on a fix word, and is
closed once at the run's end by one new subcommand, `round_record.py notes`,
at one commit. `seal` and `chain_check.py` refuse a run whose notes are still
open, and `chain_check.py` refuses a note closed `fixed` on a work item begun
at or after this one. `skills/code-review/orchestration.md` owns the sentence.
Every reader this adds reads an owned cell or an observed commit; none reads
prose. What it removes: the per-round demand in `close` that a ⬜ take a row,
and the sentence *fixed in passing or not at all*.

## Technical context

Coordinates at 5623d728 (0.20.0 as shipped), read 2026-10-07.

- `skills/code-review/scripts/round_record.py` (5,094 lines): `close` at
  4244 — `open_now` at 4281 reads every numbered row's verdict, the `missing`
  refusal at 4286 demands a row for each; `fix_table` at 3662 (three words;
  the suffixed-cell refusal at 3786 names *the three a fix pass may hand
  over*); `verdict_rows` at 3825; `finding_number` at 3085 with
  `OWED_MARKERS` at 3020 (🔴, 🟡); `COMMISSIONS_NOTHING` at 2227 (⬜, 🟢, ❓;
  its comment quotes *fixed in passing or not at all*); `current_run` at 2264
  (the run's records, cut at a `second`); `reach_forward` at 1635 (opens
  `round-{n+1}.md` only); `inherited_rows` at 1576 (first-seen-wins across
  rounds, so a coordinate of round K sits under round K in every later
  record's table); `landing_values` at 1525; `seal` at 4728 — refuses an
  unticked `Pass` on the last record (lines 136–146 of the function) and
  reads `Fixes checked by` for `no fixes to check` (173–211); `last_record` at
  4598; `new` at 2821 prints `bound_line` and the stop; `main` at 5007.
- `skills/code-review/scripts/chain_check.py` (5,477 lines): `CLOSED_WORDS`
  429, `FIX_WORDS` 475, `MARKER` 501, `BLOCKING` 399, `CAPPED_EXIT` 802,
  `REFRAME_EXIT` 838; `verdict_table` 1541, `verdict_of` 1653,
  `open_blocking` 1706 (selects on 🔴 in any cell), `closed_with_a_fix` 1808,
  `wrote_fixes` 3496, `stopping_floor` 3527, `runs_of` 3819, `check_round`
  4911 (the last record, `strict` off on a draft), `main` 5006 — the
  per-record loop at 5368 and the once-per-item `fragment_left_behind` at 5442;
  the cutoff pattern `REFRAME_FROM = 1791240747` at 831 and `item_began` at
  2207.
- Documents: `skills/code-review/orchestration.md` (704 lines) — §*Orchestrator:
  the run ends with a verifying round* at 122, its rule-1 link at 191, the
  reframe table's *The record* row at 252, the fix-pass paragraph at 38 (*one
  row per open finding*); `skills/code-review/SKILL.md:271` (the ⬜ line);
  `agents/warden.md:157–163` and `:453–456`; `agents/smith.md:186–197`;
  `skills/implement/SKILL.md:593` (*every unresolved (⬜) row must move out* —
  a different ⬜, the overview's; unchanged); `templates/sdd-round.md:312–330`;
  `skills/implement/orchestration.md:636–661` (the acts table);
  `tests/test_the_rules_have_one_owner.py:143` (`RULES`), `:353` (pins
  *never counted by Needs a fix*), `:391` (pins the `corrected at <sha>`
  spelling in the owner and `agents/smith.md`).
- Tests that build records: `tests/test_the_fixes_close_the_record.py` (`repo`
  fixture; `:935` the one numbered ⬜ row, closed `answered` through `close` in
  `test_a_correction_closed_answered_lands_on_no_fixes_to_check`),
  `tests/test_the_seal_is_taken_once_by_the_sealer.py:4072` (a `⬜ 2 …
  deferred #664` row in a fixture record), `tests/test_the_reopening_is_one.py`,
  `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`,
  `tests/test_a_fix_of_a_fix_is_counted.py:405` (a docstring quoting the
  phrase; no assertion on it).
- Ledger rows anchored on units this touches (`grep` over `seal/releases/*.md`,
  executed): `round_record.py#close` and `#fix_table` are cited by rows in
  0.10.0, 0.11.4, 0.11.5, 0.12.0, 0.12.1, 0.19.0 among others (41 anchors over
  13 release files for the five units `close`, `fix_table`, `seal`,
  `closed_with_a_fix`, `wrote_fixes`). Every edit to one drifts its family;
  the re-reads go into this item's fragment with `--reverify --into`.

**Constraints.** `docs/review-chain-spec.md` is at 999 and
`docs/round-record-spec.md` at 994 of the 1,000-line ceiling: no line is added
to either. A record is committed before the fixes it commissions, so `notes`
cannot run inside a round. The corpus holds 35 ⬜ rows closed `fixed` on 14
records (executed, 2026-10-07): the gate's new arm grandfathers them by cutoff
or it fails every open pull request's history.

**Failure scenario of the chosen approach.** A reviewer grades a defect ⬜ to
keep the run short; the note is closed `answered` at the end with no reader,
and the defect ships. The control is the reviewer's grade, which is what it is
today, and `agents/warden.md` §*would the release ship a defect* is the line.
The other way it fails: `notes` is run with `--at` naming a commit that
touches behaviour, and the broad gate is the only reader of it — `questions.md`
Q1 holds the one-arm alternative.

**Failure direction: blocks more.** A `fixed` on a ⬜ and a seal or a ready
pull request over an open note are refused where they passed. A wrong deny
costs one `notes` run; a wrong allow is today's state. **Prompt budget: zero.**
No question reaches a person; one command per run replaces one row per note
per round. **Platform honesty:** the subcommand reads git through the same
`git()` wrapper the others use; nothing process-level.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. The orchestrator files ⬜ at the end, by rule in prose | the issue's own measurement: #822's loop was ended by a judgment written nowhere, and #823's and #824's rounds each closed their notes in the round's fix pass. Nothing in the tree makes it | rejected — the issue asks for `round_record.py` and `chain_check.py` to hold it |
| B. A ⬜ takes no number, the *commissions nothing* shape that already exists | nothing collects or closes it; *not at all* becomes a silent drop. 0 of 73 ⬜ rows in the corpus are written that way, and the id is what says somebody owes the row an answer (`docs/round-record-spec.md` §*The finding id*) | rejected |
| C. Records-level read from `Location` (a path under `seal/`) | a second reader of `Location` while #866 makes the cell single-reader; misses a note located in code; catches a 🟡 located in a ledger row and overrules the reviewer's grade | rejected — the marker is the owned form |
| D. Close carried notes by re-running `close --round K` per record at the end | one command per record, each re-measuring `Fix range`, `Contract changes` and `New units` over a range that must be retyped; `close`'s close-prefix guard refuses a re-close; nothing says the run is over | rejected |
| E. A new record cell `Notes closed at \| <sha>` | a new cell is a new reader in every script that walks fields, and `broad_gate.py#rounds_rows` and `release_seal.py` already read records — #866's table grows a row | rejected — the commit goes in each row's grounds, in rule 1's spelling, checked by `--at` at the write |
| F. A fourth record verdict word `corrected` | reaches `verdict_of`, `CLOSED_WORDS`, the panel and the release seal at once | rejected — `corrected` is a word of the notes table only, rendered as `answered` |
| G. Chosen: carry ⬜ open; `close` refuses ⬜ rows; `notes` closes them once at the run's end at one commit; `seal` and `chain_check.py` refuse open notes; `chain_check.py` refuses a ⬜ closed on a fix word after the cutoff | a mis-graded ⬜ ships without a reader (above); a `notes` commit touching behaviour is read by the gate alone (Q1) | chosen |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The reader and the gate.** `chain_check.py`: `NOTE`, `NOTES_FROM = 1791384154`, `note_rows(rows, col)` built on `verdict_table`/`verdict_of`; arm A — a numbered ⬜ closed on a fix word is an error at or after the cutoff, a notice before; arm B — an open numbered ⬜ on any record of the current run is an error at a ready pull request and a notice naming `notes` on a draft; both wired once per work item after the per-record loop. `round_record.py`'s `COMMISSIONS_NOTHING` built from `chain.NOTE`. The owner's `###` in `skills/code-review/orchestration.md` under §*the run ends with a verifying round*, and its row in the acts table (`check: chain_check.py`, `command: bin/round-record`), because the heading without the row is red | `tests/test_a_note_closes_once_at_the_runs_end.py`: arm A red with the arm deleted, green with it; the cutoff case (an item at `1791384153` prints, at `1791384154` fails); arm B on a draft and on a ready pull request; the 7 work items in this tree exit 0 under `chain-check --baseline origin/release/v0.21.0`; `test_every_orchestrator_act_names_its_delivery.py` green | 61721ab6 |
| 2 | **`notes`, and the seal that waits for it.** `round_record.py notes --item --fixes --at [--baseline]`: the run's-end test shared with `seal` (one function over `last_record`'s `Fixes checked by`); `fix_table(…, notes=True)` admits `corrected`, refuses `fixed` with the rule's sentence; `--at` resolved, ancestor of HEAD, not an ancestor of the run's last `Target SHA`, required while a row reads `corrected`; every open numbered ⬜ of every record of `current_run` needs a row, a 🔴/🟡 row and a reviewer-closed row are refused; cells written the way `close` writes them (join, close-prefix guard); `Pass` re-derived per record; `reach_forward(…, into=K)` for every later record; `run_check`. `seal` and `seal --check` refuse while `open_notes` is non-empty, naming each. Nothing in `close` changes yet, so every existing case stays green | cases for S3, S4 (three), S5, S6, S9 in the new module; `seal --check` R1 pin green; `test_the_fixes_close_the_record.py` untouched and green | 45077c75 |
| 3 | **`close` carries a note, and `new` says so.** The `missing` demand excludes ⬜ rows; a ⬜ row in the fix table is refused naming the rule and `notes`; `close`'s print and `new`'s output carry `N notes open across the run — closed once at its end by notes`. The two fixtures move: `test_a_correction_closed_answered_lands_on_no_fixes_to_check` closes its ⬜ through `notes`; the `⬜ 2 … deferred #664` fixture row in the sealer test is closed through `notes` or regraded in the fixture. The `COMMISSIONS_NOTHING` comment and `close`'s *One row per OPEN finding* comment reworded | cases for S1, S2 (seen red against phase 2's `close`); `tests/test_a_finding_id_is_a_bare_integer.py` (pins the `left with no row` message) green with the message's new clause | 1e9d98f0 |
| 4 | **The carriers, the fragment and the ledger.** `skills/code-review/SKILL.md:271` (the ⬜ line keeps *never counted by Needs a fix*, drops *fixed in passing or not at all*, links the owner); `agents/warden.md` (a carried note is not re-reported; the ⬜ line names the owner); `agents/smith.md:186–197` and `skills/implement/SKILL.md` §5 (*one row per open 🔴 or 🟡*; a ⬜ closes through `notes`); `templates/sdd-round.md:312–330`; `skills/code-review/orchestration.md:38–41` and the reframe table's *The record* row (a ⬜ through `notes`, at the same moment); `tests/test_the_rules_have_one_owner.py` gains a `RULES` entry (owner `ORCH`, carriers `SKILL`, `WARDEN`, `SMITH`, `TEMPLATE`); `survivor-check` over the range for the removed wording; `changelog.md`; the ledger fragment: claims for `note_rows`, arm A, arm B, `notes`, `seal`'s refusal, `close`'s exemption, and `--reverify --into` for every released row the edits to `close`, `fix_table`, `seal`, `closed_with_a_fix` drifted | the five text-hygiene modules the framer brief names; `test_the_rules_have_one_owner.py`; `evidence-check .` reads 0 drifted | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

**Re-read the Status column after any rebase** — a squash or a rebase orphans
the commits it names, and nothing measures from this column.

## Seams with the sibling frames of 0.21.0

- **#866 (`1791384155-a-round-record-cell-has-one-reader`)** touches
  `verdict_of`, `says_reopened`/`terminal_value`, `fix_table`'s deferred-home
  reading, `landings`/`location_units`, `pull_request_state`. This item adds
  exactly one reader, `note_rows`, in `chain_check.py` and imports it from
  `round_record.py`; it changes `fix_table` by a parameter, not a copy; it
  reads no cell #866 names except through #866's reader where one lands first.
  Either order builds. If #866 lands first, phase 2's `notes=True` goes on the
  reader #866 left; if this lands first, #866 folds `note_rows` into its table
  as the one reader of the `#` cell's marker beside `finding_number` and
  `open_blocking`'s `BLOCKING in seen[0]`, which it may then import.
- **#860 (`1791384160-…`)** changes `touched` and `walk_tip`; `notes` calls
  neither (no range, no surface).
- **#869** reads `Needs a fix` in `broad_gate.py#rounds_rows`; unchanged here.
- **#835** asks every new reader to declare its input class: `spec.md` §*Data
  & interfaces* states it for the five this adds.

## Operational impact

- A new subcommand `round-record notes`, reached through the existing `bin/`
  wrapper; a new cutoff `NOTES_FROM`; no new dependency, no env var.
- **The fold at `settle`.** This spec's rule folds into `docs/` when the work
  item is retired after release, and the two documents it belongs beside are
  at 999 and 994 of a 1,000-line ceiling. The fold session splits one of them
  or opens a third; that decision is the release's, and this item adds no line
  to either.
- **Compatibility.** Records written before `NOTES_FROM` are read as before:
  a ⬜ closed `fixed` prints a notice and the floor's walks count it as they
  did, so no shipped run turns red. A run in flight at the plugin update that
  carries an open ⬜ meets `seal`'s new refusal and runs `notes` once.
- **What a session sees.** `close` refuses a ⬜ row; `new` and `close` print
  the carried count; `seal` names open notes; `chain-check` prints two new
  notices or errors. Each sentence is pinned in the phase that writes it (§14).
