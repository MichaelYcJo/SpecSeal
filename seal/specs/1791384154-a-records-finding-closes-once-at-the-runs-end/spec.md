# Feature Specification: a records-level finding closes once at the run's end (#837)

<!-- seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | the closing of a note is a command and a check, never a judgment an orchestrator has to remember |
| `docs/review-chain-spec.md` §*The last round verifies, and what it verifies is a diff* — *A finding located in a record is a correction, not a round* | the owner of rule 1 stays where it is: a correction owes no fix pass and no reader, and closes `answered` with `corrected at <sha>` as its grounds, never `fixed`. This work gives that closing one moment and one command; it moves no sentence out of that section, which sits at 999 of 1,000 lines |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* | the bound a ⬜ closed `fixed` spends today, measured below on #822's run |
| `docs/review-chain-spec.md` §*Where a leftover goes — the ladder, and why a new issue is not the default* | `deferred <home>` stays the word for a note that is filed; the ladder decides the home |
| `skills/code-review/SKILL.md` §*Findings format* | ⬜ is the reviewer's own mark for *reads badly while the behaviour and the fact stay right*, and `Needs a fix` counts 🔴 and 🟡 only. The marker is the owned form this work reads |
| `skills/code-review/orchestration.md` §*A fix of a fix twice sends the work item back to its framer* | a ⬜ never lands (`round_record.py`'s `COMMISSIONS_NOTHING`); a run ends at a `second`, and the stopped run's notes close there |
| `docs/round-record-spec.md` §*The finding id — a bare integer, behind an optional severity marker* and §*A verdict row that commissions nothing* | a numbered ⬜ is a finding somebody owes an answer, and a bare ⬜ commissions nothing. Both readings are unchanged; the corpus writes only the first |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | a test seen red, a failure direction, a prompt budget and platform honesty, stated in `plan.md` |
| `docs/the-record-layout.md` §*A commit after the build brings its changelog fragment along* | the notes commit changes nothing a release note states, so it owes the fragment nothing; the rule binds whoever writes it |
| #834, `seal/specs/1791382684-every-reader-and-record-is-inventoried/inventory/8-evidence.md` (branch `chore/834-every-reader-and-record-is-inventoried`) §*Observations* | 18 of the 33 review-filed issues since 0.18.0 came from a capped run's last round (14) or the post-review check after one (4); 21 of 63 carry record drift. Read, not re-counted here |

## What stands today, measured

Every ⬜ in the corpus is numbered, every numbered row is closed by the
round's own fix pass, and a ⬜ closed `fixed` is a fix the chain owes a reader.
Three places make that so, and none of them is a sentence.

| Where | What it does to a ⬜ today | Measured (executed, 2026-10-07) |
|---|---|---|
| `skills/code-review/scripts/round_record.py#close`, the `missing` refusal (*every open finding takes a row*) | demands a fix-table row for every open numbered row, ⬜ included, so each round's fix pass answers its notes then and there | 33 round records (11 at `v0.19.0`, 22 at HEAD): 73 numbered ⬜ rows, 0 bare ⬜ rows. Closed `fixed` 35, `answered` 22, `deferred` 16 |
| `skills/code-review/scripts/chain_check.py#closed_with_a_fix` and `#wrote_fixes` | read `FIX_WORDS` on every verdict row whatever its marker, so a ⬜ closed `fixed` makes the record one that closed on a fix: `Fixes checked by` must name a later round, and the floor's count walk and the reopening walk count it | 14 of the 33 records closed a ⬜ `fixed`. In one, #822's `round-2.md` (`1791239490-…`), the ⬜ rows were the only fix words: 5 ⬜ `fixed`, 0 🔴/🟡 `fixed`, `Needs a fix | no`, `Fixes checked by | round-3`. Round 1's floor row reads `no`, so that record was the run's one reopening; round 3 then ended the run capped and deferred 5 more ⬜ to #830 |
| the capped exit (`docs/review-chain-spec.md` §*The reopening*): a terminal record commissions nothing, so a ⬜ still open takes the ladder | a records-level leftover is filed as an issue or ridden into one | 16 of 73 ⬜ rows closed `deferred #N`; #830 and #831 are the issue's own example. The post-review check that found #831 has no carrier in `docs/`, `skills/`, `agents/` or `templates/` (grep, 0 hits); 8 `post-review-check*.md` files stand under `seal/specs/`, process records nothing reads |

So a ⬜ opens a fix pass by being owed a row, opens a reader and spends the
reopening by being closed `fixed`, and opens an issue by reaching a capped
record open. The rule the issue asks for has to reach all three.

## Scope

**In.**

1. **The rule, owned by `skills/code-review/orchestration.md`**, as a `###`
   under §*Orchestrator: the run ends with a verifying round*: **a ⬜ commissions
   nothing before the run ends, and closes once at its end** — in one commit,
   `answered` with `corrected at <sha>` as its grounds, `answered` with the
   grounds it stands on, or `deferred <home>`; never `fixed`. No fix pass, no
   reader and no check follows the notes commit: the broad gate reads it, and
   what the gate does not read stands or is filed.
2. **What a records-level finding is, in the form a script reads: the ⬜ marker
   in the `#` cell.** Not the `Location` path. The marker is the reviewer's own
   vocabulary (`skills/code-review/SKILL.md` §*Findings format*, five markers),
   `agents/warden.md` already tells the reviewer to report a records-located
   finding as ⬜, and `round_record.py` already reads the marker for the id and
   for the landing. A `Location` test would be a second reader of a cell #866
   is making single-reader, and would miss a note located in code (a message's
   wording) while catching a 🟡 located in a ledger row that `evidence-check`
   refuses. Prose is read nowhere.
3. **One reader, in `chain_check.py`, imported by `round_record.py`**:
   `NOTE` (the glyph) and `note_rows(rows, col)` — the numbered rows of a
   verdict table whose `#` cell carries ⬜, each with whether its verdict is
   open. Built from the readers that exist (`verdict_table`, `verdict_of`), not
   beside them. `round_record.py`'s `COMMISSIONS_NOTHING` is built from
   `chain.NOTE`.
4. **`round_record.py close --round N` leaves a ⬜ open and refuses a row for
   one.** The `missing` demand narrows to rows whose marker is not ⬜; a fix
   table carrying a ⬜ row under any verdict is refused, naming the rule and
   `notes`. `Pass` is derived as today, so a record with a note carried stays
   unticked until the run's end. `new --round N+1` prints how many notes the
   run carries open.
5. **`round_record.py notes --item <dir> --fixes <table> --at <sha>`** closes
   them once. It refuses before the run's end — the last record of the current
   run does not read `Fixes checked by | no fixes to check`, which is the test
   `seal` already keys on and which holds at every exit: a verifying round that
   opened nothing, the reopening bound, the round cap's verifying round, and a
   `second`. It takes one `## Fixes` table in the shape `close` takes, read by
   `fix_table` with the notes vocabulary: `corrected` (written into the record
   as `answered` with `corrected at <sha>` and the row's note as grounds),
   `answered <grounds>`, `deferred <home>`; `fixed` refused with the rule's
   sentence. Every open numbered ⬜ of every record of the run needs a row; a
   row for a 🔴 or 🟡, or for a ⬜ the reviewer closed in the report, is
   refused. `--at` must resolve, be an ancestor of HEAD, and not be an ancestor
   of the run's last `Target SHA`; it is required while any row reads
   `corrected`. It writes the verdict and grounds cells the way `close` does
   (joined, never overwriting the reviewer's grounds, the close-prefix guard
   kept), re-derives `Pass` on every record it touched, reaches forward into
   every later record's `## Inherited coordinates` so no `Why` cell goes on
   saying `open`, touches no other row, and runs the chain check.
6. **`round_record.py seal` and `seal --check` refuse while a numbered ⬜ of the
   run is open**, naming each by record and id and naming `notes`. Today `seal`
   reads the last record's `Pass` alone, so a note carried on an earlier record
   would pass it.
7. **`chain_check.py` holds the rule at the pull request**, keyed to
   `NOTES_FROM = 1791384154` the way every other row's cutoff is: a numbered ⬜
   closed on a fix word is an error on a work item begun at or after the cutoff
   and a notice before it (35 rows of the corpus are before it); an open
   numbered ⬜ on any record of the current run is an error at a ready pull
   request and a notice naming `notes` on a draft.
8. **The carriers link to the owner**: the ⬜ line of `skills/code-review/SKILL.md`
   §*Findings format* (the phrase *never counted by Needs a fix* kept — it is
   pinned), `agents/warden.md` (a note carried from an earlier round is not
   re-reported, and the ⬜ line names the owner), `agents/smith.md` and
   `skills/implement/SKILL.md` §5 (a ⬜ takes no row in a round's fix table),
   `templates/sdd-round.md`'s `#`-cell comment, the acts table in
   `skills/implement/orchestration.md` §*Orchestrator: which of these acts runs
   itself* (one row: delivered by `bin/round-record` and `chain_check.py`), and
   `tests/test_the_rules_have_one_owner.py`'s `RULES` (one entry).
9. **The two fixtures that close a ⬜ through `close`** move to `notes`:
   `tests/test_the_fixes_close_the_record.py:935` and the record fixture at
   `tests/test_the_seal_is_taken_once_by_the_sealer.py:4072` (read, the only
   two lines in `tests/` carrying a numbered ⬜ row).

**Out.**

- **Regrading.** A 🔴 or 🟡 whose `Location` is a record is the reviewer's
  grade and closes as today. `agents/warden.md` already says such a finding is
  ⬜; the generator does not second-guess the reviewer.
- **The verdict vocabulary of the record.** No new word enters `CLOSED_WORDS`,
  `FIX_WORDS` or `HOME_WORDS`. `corrected` is a word of the notes table, an
  input `fix_table` owns, and the record carries `answered`, which every reader
  of a verdict cell already reads. A new record word would reach `chain_check`,
  `broad_gate.py#rounds_rows` and `release_seal.py` at once, which is #866's
  table growing a row.
- **A new record cell** (`Notes closed at | <sha>`). A cell is a reader in every
  script that walks fields; the commit goes into each row's grounds in the
  spelling rule 1 already prescribes, and `--at` is checked at the moment of
  writing. What this gives up: nothing at the pull request re-reads that
  commit, because nothing machine-reads a SHA out of an `answered` cell by
  design (`docs/review-chain-spec.md` §*Two cells, not one*).
- **`CAPPED_EXIT` and `REFRAME_EXIT`'s wording.** Both say *every finding still
  open* closes a certain way, and both already lag the ladder;
  `docs/review-chain-spec.md` §*Two refusal messages still say a refused finding
  becomes an issue* says rewording the pair is the repository owner's decision.
  Phase 4 names the lag one more way and changes neither.
- **The post-review check as a mechanism.** None exists to remove: it is a hand
  act whose only trace is a process record. The owner's sentence is what ends
  it; nothing in the tree can stop a session spawning a reader by hand.
- **Text in `docs/review-chain-spec.md` (999 lines) or `docs/round-record-spec.md`
  (994 lines).** Both sit at the 1,000-line ceiling `seal/config.md` declares.
  The owner is `skills/code-review/orchestration.md` (704 lines). The fold of
  this spec at a later `settle` will not fit either document; `plan.md`
  §*Operational impact* says so.
- **#866's readers** — `verdict_of`, `says_reopened`, `terminal_value`,
  `deferred_home`, `landings`, `location_units`, `pull_request_state` — are not
  touched. **#860's `touched`** is never called by `notes`, which has no range.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a note is carried | Given round N's record holds `⬜ 3 … open` and the fix table has no row for it, when `close --round N` runs, then it closes the 🔴 and 🟡 rows, leaves `⬜ 3` open, leaves `Pass` unticked, and prints that one note is carried | case in `tests/test_a_note_closes_once_at_the_runs_end.py`; seen red against the `missing` refusal at `round_record.py:4286` |
| S2 a note takes no fix row | Given the fix table carries `\| 3 \| fixed \| <sha> \|` or `\| 3 \| answered \| … \|` for a ⬜, when `close` runs, then it refuses naming the rule and `notes`, and no cell is written | case; §14 pins the sentence |
| S3 notes close only at the end | Given the run's last record reads `Fixes checked by \| round-3` or `nobody — …`, when `notes` runs, then it refuses saying the run has not ended and what the last record reads | case |
| S4 notes close once | Given the run ended (`no fixes to check`) with notes open on rounds 1 and 2, when `notes --at <sha> --fixes <table>` runs with a row per note, then round 1's and round 2's cells read `answered \| corrected at <sha> — <note>`, `answered \| <grounds>` or `deferred <home>`, `Pass` is ticked on both, round 3's `## Inherited coordinates` `Why` cells for those coordinates no longer read `open`, and the chain check exits 0 | case; a second case with a missing row refuses naming it; a third with `fixed` refuses with the rule's sentence |
| S5 `--at` is the run's end | Given `--at` names a commit the last `Target SHA` descends from, or one HEAD does not, when `notes` runs, then it refuses before writing | case |
| S6 the seal waits for the notes | Given round 1 holds an open ⬜ and the last record's `Pass` is ticked, when `seal` or `seal --check` runs, then it refuses naming `round-1.md`'s `⬜ 3` and `notes` | case; the preflight pin in `tests/test_the_seal_is_taken_once_by_the_sealer.py` (R1) holds |
| S7 the gate holds the rule | Given a work item begun after `NOTES_FROM` whose record closes a ⬜ `fixed`, when `chain-check` runs, then it is an error; given one begun before, a notice. Given an open ⬜ on any record of the run, then an error at a ready pull request and a notice naming `notes` on a draft | cases; the 7 work items with `rounds/` in this tree (all before the cutoff) exit 0 |
| S8 the owner states the rule | Given the tree, when `tests/test_the_rules_have_one_owner.py` runs, then the owner's sentence is in `orchestration.md` and every carrier links to it; `test_every_orchestrator_act_names_its_delivery.py` finds the heading's row | the two test modules |
| S9 a stopped run closes its notes | Given a record reads `Fix of a fix \| second`, when `notes` runs before the framer is spawned, then it closes the stopped run's notes and refuses nothing about the `Reframed` line | case; `current_run` cuts the run at the `second` as `new` does |

## Data & interfaces

- `chain_check.py`: `NOTE = "⬜"`, `NOTES_FROM = 1791384154`, `note_rows(rows, col) -> [(line_no, id, open)]`, two arms in `main`'s per-work-item walk (after the per-record loop, as `fragment_left_behind` is wired), each with the refusal text `plan.md` names.
- `round_record.py`: `fix_table(reader, path, notes=False)` — the `notes` vocabulary admits `corrected` and refuses `fixed`; `reach_forward(reader, rounds, n, rows, into=None)` — `into` names the later record to fill, default `n + 1`; `open_notes(reader, run)` over `current_run`'s records, shared by `close`'s print, `notes`, `seal` and `seal --check`; the `notes` subcommand registered in `main`; `COMMISSIONS_NOTHING = (chain.NOTE, …)`.
- The notes table: `## Fixes` with `| # | Verdict | Commit or grounds |`, verdicts `corrected` (third cell: a note, may be empty), `answered <grounds>`, `deferred <home>`.
- Record cells written: `Verdict` and `Grounds` of ⬜ rows, `- [x] Pass`, and later records' `## Inherited coordinates` `Why` cells. Nothing else.
- Readers' input class, stated as #835 asks: the `#` cell's marker (owned, the skill's five-marker vocabulary), the verdict word (owned, `CLOSED_WORDS`), the `## Fixes` table (owned by the generator), `Fixes checked by` (owned), `--at` against git (observed). No reader of prose is added.

## Judgments the tree answered

Listed so nobody reopens them; the grounds are in the rows above or in `plan.md`'s Alternatives.

1. Records-level means the ⬜ marker, not the `Location` path (Scope 2).
2. A note is carried open in the record that holds it and closed there; it is not renumbered, re-reported or copied forward (Scope 4, 5; `inherited_rows` already carries the coordinate with its verdict word).
3. The run's end is the last record of the current run reading `no fixes to check` — the test `seal` already applies, true at all four exits (Scope 5).
4. No new record vocabulary and no new cell (Out).
5. The cutoff grandfathers the corpus: 35 rows closed `fixed` print, never fail (Scope 7).
6. New text goes to `orchestration.md`; nothing into the two documents at the ceiling (Out).
7. The subcommand is `notes`, the skill's own word for ⬜ (*⬜ note*).
8. `notes` runs at a `second` too, before the framer is spawned, so the framer reads corrected records (S9).
9. The notes commit is bounded by the ⬜ definition, not by path, and the broad gate is its reader — the default `questions.md` Q1 states, with the alternative that is one arm.

## Open questions → questions.md

One row a person answers (Q1, the default is built), two a measurement settles, two the work settles.

Framed 2026-10-07 by framer, before the build.
