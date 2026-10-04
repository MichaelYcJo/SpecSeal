# Feature Specification: the reverify writer records before it re-stamps (#647 steps C and D)

<!-- seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

#647 steps C and D, reviewed from round 1. A signatory's `evidence-check
--reverify` records a **pact change** when it moves code a cited pact clause
binds, and `pact-check` at the pact's repository reads it until a **pact
review** takes it. The work was built once, as work item `1791019474-a-signatory-
records-a-pact-change-and-the-pact-is-reviewed` on
`feat/647-a-signatory-records-a-pact-change-and-the-pact-is-reviewed` (draft
PR #749, tip `b4c9deb2`). Its round 2 found that the writer's
snapshot-and-restore transaction could itself lose a record. The owner chose
a redesign — plan the ledger writes, write the records, write the ledger only
after — and it was built in `f9469ad8..b4c9deb2`. `round_record close` then
refused round 2 at depth 2, because a fix pass may not add a unit inside a
unit an earlier fix created. The owner's decision (2026-10-03, #647's last
comment): the record-first writer is framed as its own work item and reviewed
from depth 1. This is that work item.

**What is new in this frame is decision 1 and the writer's contract (§*The
writer's contract*).** The rest of the scope — the deferred fixes, the record,
`pact-check`'s reading, the pact review — was framed by `1791019474`'s
`spec.md` (read at `b4c9deb2`), and this file carries it forward rather than
re-arguing it. Where this file and that one differ, this one holds.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | the trigger is mechanical and the record is written by a tool. Nobody is asked whether a change touched the pact |
| #647, the owner's comments of 2026-09-28 (*"Touched the contract" needs no judgment*; *Notifying means leaving a record, not pushing one*) and of 2026-10-03 (decisions 2, 4, 5; names `pact`, `signatory`, `pact-check`) | the trigger is a drifted signatory ledger row citing a clause. The record is left in the signatory, and no CI token reads across repositories |
| #647's comment *Moved to 0.18.1* (2026-10-03), also on PR #749 | the writer records first and re-stamps after. This work item is reviewed from depth 1 |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed* | why the redesign could not close inside `1791019474`'s chain, and why every unit carried here is depth 0 to this chain: round 1 reads all of it as a finding surface |
| `skills/code-review/scripts/chain_check.py#main` (`changed_routing` united with `declared_for_this_branch`) and `#check_round` | a `routing.md` this pull request adds is judged. A last round whose `Pass` is unchecked, or which holds an open blocking row, is an error at a ready pull request. This decides decision 1 |
| `skills/code-review/scripts/round_record.py` (`DEPTH_EXIT`, the depth-2 refusal in `close`) | `1791019474`'s round 2 cannot be closed as it stands, and ticking it by hand would falsify it |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/spec.md`, items 7 and 8 | the trigger row's shape (a local coordinate plus a `PACT_ANCHOR_RE` match), and an untaken pact change as a second source under `NOT TAKEN`, exit 1 |
| `seal/specs/1790993137-…/rounds/round-3.md` (🟡 18, 🟡 19, ⬜ 21, ⬜ 22, ⬜ 23 deferred to #647) and #647's comment after `1a60896c` | the deferrals and the separator note this item owns |
| `docs/the-pact.md` (base) §*How a signatory names the pact* | *"Nothing acts on that value until the record of a pact change exists"* — this work is that record, so the sentence changes |
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | a pact review takes a record by its content hash, never a commit SHA |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from \| 1790993141` | 0.18.0 folded every fragment `1791019474` re-stamped into `seal/releases/0.18.0.md`. Those rows are read again here as `Re-read ·` rows in this item's fragment, never edited in place |
| `skills/evidence-check/scripts/evidence_check.py#unshipped` | a shipped work item's records are not read by the records arm. `1790993137` shipped in 0.18.0, so the `· NAME NOT IN TREE` marks `1791019474` added to its records are not carried |
| `skills/verify/scripts/unverified_check.py#folded_items` | a `<!-- specs/<id> -->` marker in `docs/` reads as that item folded. A marker naming `1791019474`, whose directory this tree never holds, would read as a fold that never happened |
| `skills/settle/SKILL.md` | `settle --retire` removes `seal/specs/<id>/`, so a record that outlives its work item sits directly under `seal/` |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | one record file per work item, one ledger fragment per work item |
| `tests/commonmark_oracle.py` and `.github/scripts/run_tests.py#MARKDOWN_IT` (#667) | the precedent for a pinned test-only parser. `cmarkgfm` follows it |
| `skills/agent-contract/SKILL.md` §12–§15 | the separator note is a class; its case removes the POSIX guarantee; every changed sentence is pinned in its commit; every new case is seen red |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | `example.com`, `/Users/x/` |
| `CLAUDE.md` §*Repo rule — a thing more than one party can have is named with whose* | *review* has several owners here. The new one is always *the pact review* |
| #746 (open, a later work item of this release) | `--reverify --into` will refuse a stale `--checked`. Not taken here; its seam is W9 below |
| #741 (open, lands first) | an encoding check over all file I/O. Every I/O this item adds or carries names `encoding="utf-8"` |

## Decision 1 — how this branch receives the work

**The whole of C and D is carried into this work item as code, tests and
policy, and `1791019474`'s directory, records and ledger fragment stay on its
branch.** PR #749 is closed unmerged once this item's pull request opens, with
a comment naming it. Its branch is kept, because it is where `1791019474`'s
round records live and the code comments below cite them.

**Why not merge the old branch in.** A merge brings
`seal/specs/1791019474-…/routing.md` into this pull request's diff, so
`chain_check.py#main` judges it beside this item's own. Its last record,
`rounds/round-2.md`, has an unchecked `Pass` and an open 🔴 10, which
`#check_round` refuses at a ready pull request. Closing that round is what
`round_record close` refused at depth 2, and ticking it by hand writes a record
nothing verified. Its `Branch` row also names a branch that is not this one.
So the merge cannot reach a green `chain_check` without one false record.

**What is true after the carry.** Every record on this tree describes this
work item or an earlier one, and none of them claims `1791019474` closed. Its
round 2 stays "written and not closed" on its own branch, which is exactly
what PR #749's comment says. Nothing on `release/v0.18.1` names `1791019474`
today (`git grep` at `0004f126`: only this item's `routing.md`).

**The carry set**, measured: the paths `1791019474`'s own commits touched
(`git log --first-parent --no-merges b9824454^..b4c9deb2`) outside `seal/`.
The base changed none of them since the old branch's merge base `aa7fb285`
(`git diff --name-status aa7fb285 e141980a`: `plugin.json`, `CHANGELOG.md`,
the seven folded fragments, `seal/releases/0.18.0.md` and
`tests/test_a_record_precedes_the_fixes_it_commissions.py`, none in the set).
`git merge-tree e141980a b4c9deb2` conflicts only on five folded ledger
fragments. So each carried path takes its `b4c9deb2` content whole. Four
things change on the way in, and nothing else:

| On the way in | Why |
|---|---|
| the nine `<!-- specs/1791019474-… -->` markers in `docs/the-pact.md` name this item | `folded_items` reads a marker as a fold |
| the 17 code and test comments citing `round N of #647 C and D` (`hooks/config.py` 4, `evidence_check.py` 9, `pact_check.py` 3, `tests/gfm_table_oracle.py` 1) name PR #749's round instead | this item's rounds restart at 1 and are also "#647 C and D". The citation must open the record it means |
| `1791019474`'s fragment rows are rebuilt in this item's fragment (phase 3) | a fragment is named for its work item, and its `Re-read ·` rows cite fragments 0.18.0 has since folded |
| `1791019474`'s `changelog.md` becomes this item's `changelog.md`, reworded where phase 2 changes behaviour | the changelog fragment is gathered from the work item's own directory |

**Not carried:** `1791019474`'s directory, its edits to `1790993137`'s shipped
records and changelog, and its re-stamps of the five fragments 0.18.0 folded.

## Scope

### In: carried, framed by `1791019474` and reviewed here from round 1

Items 1–13 of `1791019474`'s `spec.md` §*Scope* at `b4c9deb2`, unchanged in
intent. In one line each:

1. **One GFM table walker held to cmark-gfm** (`hooks/config.py#gfm_table`),
   reading the `Signatory` table and both new records. It closes 🟡 18
   (autolink row), ⬜ 22 (indented header, delimiter or row) and ⬜ 21 (the
   census comment). `cmarkgfm==2025.10.22` is pinned test-only.
2. **The anchor grammar stated in policy.** 🟡 19: an anchor missing its `/`
   is refused at exit 2. ⬜ 23: the grammar stands, and the refusal names a
   fenced example as the second remedy.
3. **Every path `pact-check` prints is in POSIX form**
   (`pact_check.py#shown`), which closes the `{their_home}/{CONFIG_FILE}`
   note.
4. **The trigger**: a signatory ledger row citing a clause of a pact its
   `Pact` row declares, with a coordinate that reads DRIFTED or BROKEN.
5. **The writer is `evidence-check --reverify`**, in place and under
   `--into`, under the contract below.
6. **The record**: `seal/pact-changes/<work-item-id>.md`, permanent, one per
   work item, never folded, never edited by hand.
7. **`pact-check` reads every signatory's pact changes**: `NOT TAKEN` (exit 1),
   `NOTED` (exit 0, `always` rows citing no clause), `REFUSED` and
   `UNREADABLE` (exit 2).
8. **A pact review** is an ordinary work item at the pact's repository. It
   writes `seal/pact-reviews/<work-item-id>.md` from `templates/pact-review.md`,
   with verdict `holds` or `amended`.
9. **A record is taken at its current content hash**. One that grew after its
   review reads `NOT TAKEN` again, naming both hashes.
10. **A clause change at the pact's repository owes no pact review**;
    `SUPERSEDED` already sends every citing signatory to re-read.
11. **`docs/the-pact.md`** carries all of it as fold-shape statements under
    this item's marker.
12. **The shipped text**: `templates/config.md` §*Pact*,
    `templates/pact-review.md`, `skills/evidence-check/SKILL.md`, the
    orchestration act `### A pact review at the pact's repository`, the
    `seal/` drawings, and both READMEs' `pact-check` row.
13. **`tests/test_one_word_one_meaning.py`** sweeps the new sections and
    refuses `contract-changes` and *contract review*.

**All of #735's round-3 deferrals ride here** — 🟡 18, 🟡 19, ⬜ 21, ⬜ 22,
⬜ 23 and the separator note. They are already built in the carry set, they
share units with C and D (the walker reads both new records; `shown`'s class
holds every new output line), and #647's comment of 2026-10-03 assigns them
to this frame. Leaving one out would mean reverting a built unit.

### In: the writer's contract — what round 1 judges the writer against

The clauses are numbered so a finding can cite one. W1–W7 describe the
carried writer as built in `cbea5e99..b4c9deb2`, read for this frame. W8–W10
are what that writer does not do yet, and phase 2 builds them.

**W1 — Order.** One `--reverify` run is four steps, and nothing is written
before step 3.

| Step | What happens | What is on disk if the process dies here |
|---|---|---|
| 0. Refuse | an `--into` that exists and will not read is refused at exit 2 | nothing changed |
| 1. Plan | every ledger write the run would make — re-stamps in place, `Re-read ·` rows into `--into` — is computed and held in the plan; later reads in the run answer from the plan | nothing changed |
| 2. Record | the pact changes the plan's moves owe are appended to `seal/pact-changes/<id>.md` in one atomic replace | the record as it was, or the record with every new row; a temporary sibling `<name>.md.<random>` may remain, and no reader globbing `*.md` reads it |
| 3. Apply | each planned ledger file is replaced atomically, in plan order | the record complete; each ledger file either as it was or fully re-stamped |

A run that cannot complete step 2 writes no ledger file (W5). Nothing is ever
put back and no file is ever removed, so no signal handler is needed.

**W2 — Killed at any step, the next run finishes the work and records
nothing twice.** After step 2, the record holds every owed move and the
ledger holds the old hashes. The next run plans the same moves, finds each
one the record's last word already (W4), appends nothing, and applies. Killed
partway through step 3, the files already applied show no drift and the
others plan the same moves again. SIGTERM, SIGKILL and SIGINT all fall here.
SIGINT unwinds through `write_atomic`'s `except BaseException` and removes its
temporary file; the other two can leave it.

**W3 — Unreadable input.** A ledger file that cannot be opened is named on a
`LEFT … ledger unreadable` line, its rows are neither planned nor recorded,
and it is never written or removed (the 🔴 10 class closes by construction:
no step deletes). A record file that exists and will not read or parse is
named on a `LEFT` line, nothing is appended, and the run writes no ledger
file (W5).

**W4 — Idempotence, per coordinate, by the record's last word.** A move is
appended unless the record's last row for the same clause, ledger row and
coordinate says the same move (old hash → new hash) or the same `BROKEN`,
compared as the record's reader reads a cell (`\|` unescaped). So a second
identical run leaves the record byte for byte as it was, with the same
content hash, and a pact review that took it stays taken (🟡 2). A change
re-landed after its revert is recorded, because the record's last word for it
was the revert (🟡 12). Over-recording is the safe direction: a move recorded
by a run killed before step 3, whose code then reverted, stays in the record,
and a pact review takes it as `holds`.

**W5 — A change owed and not recordable re-stamps nothing.** Where a change is
owed and any of these holds, the run names each owed row on a `LEFT` line
ending in the shared sentence (`NOT_RESTAMPED`), prints `PACT_CHANGE_UNDONE`,
exits 1, and writes no ledger file at all:
- no work item names the record (no `--into`, and no `routing.md` declares
  the branch);
- the record will not read, will not parse, or cannot be written;
- the `Pact` or `Pact notify` row will not read (W6);
- this copy of `evidence_check.py` has no `hooks/` beside it.

The drift stays on disk for the run that can record it.

**W6 — An unreadable declaration cannot rule out `always` (🟡 13).** Where
`seal/config.md` exists and will not read, or its `Pact` or `Pact notify` row
will not parse, a moved row citing a pact clause is owed. A moved row citing
none is unknown unless the notify value was read and is not `always`. Owed
and unknown rows are both W5's case. A `seal/config.md` that does not exist
declares no pact, and nothing is owed. The cost is stated rather than hidden:
in a repository with a broken `Pact notify` row, no row whose code moved is
re-stamped until the row is fixed, citing or not.

**W7 — A coordinate the re-read leaves is recorded `BROKEN` (🟡 14).** The
unit gone, the file gone under a minor anchor, the quoted statement gone, or
no one place under the freeze — each is a move to `BROKEN` in the record, at
all three exits that leave a coordinate (`reverify`, and both of
`reverify_into`'s). The ledger row is left as today. A second run appends
nothing (W4).

**W8 — A line that says a write happened is printed after the write lands.**
*(phase 2)* Today `reverify`'s per-row lines and `N rows re-verified`, and
`reverify_into`'s `wrote …` and `N citing rows written`, are printed during
step 1, before anything is written. A run that then fails W5 prints
`PACT_CHANGE_UNDONE` after them, so the output both claims the writes and
denies them (read at `b4c9deb2`, `evidence_check.py` `reverify` and
`reverify_into`). After this item, those lines print only once step 3 wrote
their file. A run that writes no ledger prints none of them, and its `LEFT`
lines and the closing line are the whole account.

**W9 — A file the run writes is read strictly.** *(phase 2)* `read()` opens
with `errors="replace"`, so a ledger or a record holding bytes that are not
UTF-8 is read with U+FFFD in their place and written back that way: the run
destroys bytes it never meant to touch. For a record this also changes its
content hash, so a pact review that took it reads `NOT TAKEN` again for
nothing. After this item, a file the run would write — a ledger it plans,
`--into`, the record — that will not decode is unreadable under W3. A file it
only reads, such as the code under a coordinate, keeps today's lenient read.
This is also **#746's seam**: a refusal #746 adds for a stale `--checked`
goes in step 0 beside the `--into` refusal, or keeps the refused family out of
both the plan and its moves. Either way, a refused row writes nothing and
records nothing.

**W10 — A ledger file step 3 cannot write is named, not a traceback.**
*(phase 2)* `apply_plan` lets an `OSError` from `write_atomic` escape today, as
the base's in-place `--reverify` always did. After the record is written,
that leaves the run's account as a traceback. After this item, step 3 names
each file it could not write on a `LEFT` line with the cause, still writes
the rest, and exits 1. The record already holds the moves, so the next run
finishes them (W2).

**What the contract does not promise.** The order holds against the process
dying. It is not a promise against the machine losing power: `write_atomic`
does not `fsync`, so after a power loss the ledger's rename could persist
while the record's data did not. That is stated in `docs/the-pact.md`
§*What this does not see*, and `questions.md` Q3 records why no `fsync` is
added. Two runs at once over one `seal/` root are not serialised, as before.

### Out, and why

| Left out | Why |
|---|---|
| Merging `1791019474`'s branch in | decision 1 |
| #746 (a stale `--checked` under `--into`) | its own work item in this release. W9 names the seam |
| #741's encoding check | lands first on its own branch. This item names `encoding="utf-8"` on every I/O and merges the release branch in when #741 squashes |
| Lenient reading of a code file under a coordinate | a file the run only reads is not written, so no byte is lost. W9 is scoped to what the run writes |
| `fsync` before step 3 | the stated limit above; `questions.md` Q3 |
| A serialising lock over one `seal/` root | no writer in the plugin takes one, and two concurrent `--reverify` runs in one root were never a supported shape |
| The `NAME NOT IN TREE` marks on `1790993137`'s shipped records | `evidence_check.py#unshipped`: a shipped item's records are not read |
| The pull-request half of the checks, a CI token, a new agent, `chain-check` printing a signatory's changes, a check-mode refusal of an unrecorded drift, recording from a vendored copy, deleting a record | `1791019474`'s §*Out, and why*, each still true. Not re-argued here |

## User scenarios & acceptance *(mandatory)*

S1–S18 are `1791019474`'s scenarios, carried with their cases in
`tests/test_one_table_walker_reads_what_gfm_renders.py`,
`tests/test_pact_check.py`, `tests/test_a_signatory_declares_its_pact.py`,
`tests/test_a_signatory_records_a_pact_change.py` and
`tests/test_a_pact_review_takes_a_pact_change.py`, which round 1 judges again.
In short: S1–S6 the deferred fixes, S7–S11 the writer and its record, S12–S17
`pact-check` and the pact review, S18 the words. The rows below are the
writer's contract, one per clause, and the carried case is named wherever one
exists.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| W1 | Nothing is written before the record | Given a citing row whose code moved, when the run is stopped after step 1, then no ledger file and no record changed | carried `test_a_run_killed_after_its_record_is_finished_by_the_next` covers after step 2. Phase 2 adds the step-1 stop, seen red by applying the plan before recording |
| W2 | Killed between record and apply | Given the record written and the ledger unstamped, when the run is repeated, then the record is byte-identical and the ledger is re-stamped | the carried kill case, plus a case stopping inside step 3 between two ledger files |
| W3 | An unreadable ledger is never removed | Given a sibling fragment with mode 000 and an owed change elsewhere, when the run cannot record, then the fragment still exists with its bytes | carried `test_an_into_that_will_not_read_is_refused_before_anything_is_written`. Phase 2 adds the sibling case if none carries it (POSIX only: a mode-000 file is readable as root, and the case skips there) |
| W4 | Idempotence and reland | A second identical run appends nothing; A→B, B→A, A→B gives three rows | carried `test_s11_a_second_run_records_nothing_twice`, `test_a_second_identical_run_leaves_the_record_byte_identical`, `test_a_change_relanded_after_its_revert_is_recorded`, `test_this_repositorys_own_piped_coordinates_are_recorded_once` |
| W5 | Not recordable, nothing re-stamped | Each of the four causes exits 1, prints `LEFT … NOT_RESTAMPED` and `PACT_CHANGE_UNDONE`, and leaves every ledger byte for byte | carried `test_s9_with_no_work_item_…`, `test_a_pact_row_that_will_not_read_leaves_the_row`, `test_a_record_that_will_not_parse_is_left_and_named`, `test_a_change_left_is_recorded_by_the_remedy_it_names` |
| W6 | An unreadable declaration under a possible `always` | A malformed `Pact notify`, and a `config.md` that will not read: a moved row citing no clause is `LEFT`, exit 1. A missing `config.md`: nothing owed, re-stamped, exit 0 | carried `test_under_always_a_declaration_that_will_not_read_leaves_the_row`. Phase 2 adds the missing-file arm if no case holds it |
| W7 | A left coordinate is recorded `BROKEN` | At each of the three exits, one `BROKEN` row; a second run appends nothing | carried `test_a_coordinate_the_reread_leaves_is_recorded`, `test_s11_a_broken_coordinate_is_recorded_and_the_row_left` |
| W8 | No line claims a write that did not happen | Given a run that fails W5 under `--into`, then its output holds no `wrote` line, no `citing rows written` line and no `re-verified` line, and a successful run prints them after the write | new case, red against the carried print order |
| W9 | A file the run writes is read strictly | Given a ledger fragment holding a byte that is not UTF-8, and a moved row in it, then the fragment is byte-identical after the run, it is named `LEFT` as unreadable, and the exit is 1. The same for the record | new cases, red against `errors="replace"` |
| W10 | An unwritable ledger at step 3 | Given the record written and a ledger whose directory refuses the replace, then the file is named on a `LEFT` line with its cause, the others are written, no traceback, exit 1 | new case, red against the bare `apply_plan`. POSIX only, skipped as root |
| K1 | The carry is the carry set and four changes | `git diff b4c9deb2 HEAD -- <carry set>` shows only the marker renames and the comment citations | read by the reviewer; phase 1's record lists the command and its output |
| K2 | The tree names no work item it does not hold | `git grep 1791019474` outside this item's own records matches only citations of PR #749's history | the command, in phase 1's record |

## Data & interfaces

Unchanged from `1791019474`'s §*Data & interfaces* at `b4c9deb2`: the record
`| Clause | Row | Code | Checked |`, the pact review `| Signatory | Change |
Verdict |` with `Change` as `<work-item-id>@<content hash>`, the walker in
`hooks/config.py`, and `pact-check`'s `NOT TAKEN` and `NOTED` lines.

**The writer's units**, as carried (`evidence_check.py` at `b4c9deb2`):
`PLANNED`, `planned_key`, `read`, `put`, `apply_plan`, `write_atomic`,
`record_pact_changes`, `pact_change_item`, `plugin_module`, `CODE_PART`,
`NOT_RESTAMPED`, `PACT_CHANGE_UNDONE`, and `main`'s `recorded_then_applied`.
Phase 2 changes `read` or its writer-side callers (W9), `apply_plan` (W10),
and where `reverify` and `reverify_into` print (W8). Its record says which
unit took each one.

**New output** is limited to W10's `LEFT` line and W9's reuse of the
unreadable `LEFT` line. Exact sentences are the build's, pinned in their
commits (§14).

## Open questions → questions.md

None blocks the build. The owner's answers of 2026-09-28 and 2026-10-03 cover
what only a person could answer. `questions.md` lists the judgments this
frame made from the tree, with grounds, and the rows a measurement or the
work settles.

Framed 2026-10-04 by framer, before the build.
