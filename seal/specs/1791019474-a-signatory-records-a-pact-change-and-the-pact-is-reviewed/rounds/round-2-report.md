# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — round 2 report

Reviewer: `specseal:warden on claude-opus-5-5`. Target: `ed1476aa` on
`feat/647-a-signatory-records-a-pact-change-and-the-pact-is-reviewed`. This
is a verifying round. Its target is round 1's fix range
`594e1007..fc5d8e61`, the merge of `origin/release/v0.18.0` at `aa7fb285`
(`2b25dc86`), and the close commit `ed1476aa`.

Every probe ran in the round's own scratch clone (`git clone --no-local` of
the worktree, checked out at `ed1476aa`, the release branch fetched beside
it), with the suite's `.venv` that `bin/test` built there. Every trial fix
was applied in the clone, measured and reverted with `git checkout`. Nothing
was written in the worktree except this file.

Round 1's record and report were read for coordinates. Every verdict below
was derived again at `ed1476aa`.

## How the findings relate

Round 1's nine findings are closed at their commits, and each fix's own cases
go red when that fix alone is taken back. The new findings sit in two places.

1. **The transaction that answers round 1's red 1 can itself lose a record.**
   - 🔴 10: `restore` removes a ledger file that `snapshot` could not read.
     A unit round 1's fixes created.
   - 🟡 11: a SIGTERM or SIGHUP between the re-stamp and the record erases
     the drift with nothing recorded. The window measures about ten seconds
     on this repository, and the policy says a run that dies is put back.
2. **The writer still has paths where an owed pact change goes unrecorded.**
   They sit beside round 1's fixes, not inside them.
   - 🟡 12: a change re-landed after its revert is re-stamped and not
     recorded. The idempotence key is "ever recorded", where it needs to be
     "last recorded".
   - 🟡 13: the silent arm of round 1's red 1 survives under an intended
     `Pact notify | always`.
   - 🟡 14: a coordinate the re-read leaves records nothing at exit 0. The
     row stays DRIFTED, so this is not lost on the run itself.
3. **The walker** (🟡 15) still reads tables cmark-gfm does not render.
   - Two of the shapes are not stated anywhere.
   - The docstring states a list-item limit in a shape the walker now
     refuses.
   - Checking the raw line above the header closes the stated kind 6–7
     limit along with them.

The merge stands. #743's grid and this item's modules pass together.
`correction-check` and `evidence-check --strict` are clean. #736's L4 is
true of the merged code.

## Round 1's findings, at their commits

| Round 1 | Commit | Executed |
|---|---|---|
| red 1 | `26a3199b` | Disabling `restore` and the `Pact`-row refusal turns 11 cases of the writer module red. Probes: no work item, an empty record, a record that is a directory, a vendored copy, a frozen run with `--into`, a fragment the run created, an exception at the record step, an unparseable `Pact` row, a non-UTF-8 config. Each prints `LEFT … nothing was re-stamped` and `PACT_CHANGE_UNDONE`, exits 1, and leaves the ledger byte for byte. The pre-run state is kept: every case writes its ledger before the run and asserts those bytes after. |
| yellow 2 | `26d4ef53` | Reversing the hunk turns 5 cases red. This repository's three real `\|` coordinates were cited beside a clause, with one row carrying a move and a BROKEN together, through six runs with two template edits between them. No row was recorded twice. |
| yellow 3 | `881e6005` | Reversing turns its case red. |
| yellow 4 | `06264ade` | Reversing turns 7 cases red. |
| yellow 5 | `2e550f45` | Reversing turns 6 cases red. Round 2's own generator at 300,000 documents (fenced below) found no table read under a line directly above it and none under an open kind 1–5 block. 🟡 15 holds what remains. |
| white 6 | `ba5ebee3` | Reversing turns 2 cases red. |
| white 7, 8 | `4f0bf885`, `2a88a3f1` | Read: the two paragraphs stand in `docs/the-pact.md`, and white 7's case passes in the module. |
| white 9 | `72042988` | Read: the `Corrected` note stands on the `Re-read · P1-1` row, and `CMARKGFM` is the pin it names. |

## Findings from execution

### 🔴 10 — The restore removes a ledger file the snapshot could not read

`skills/evidence-check/scripts/evidence_check.py:3519` (`snapshot`), with
`restore` at `:3537`.

`snapshot` answers every `OSError` with `None`, which `restore` reads as
*absent before the run*. `restore` then removes the file:
`if os.path.isfile(path): os.remove(path)`. A file that exists and will not
read is therefore deleted. Removing a file needs write permission on its
directory, not on the file.

Executed, in a signatory built as the module builds one:

- A second fragment with mode 0 stood beside the drifted fragment. A run
  with no work item printed `LEFT  …  ledger unreadable` for it, then the
  owed-change `LEFT` line and `PACT_CHANGE_UNDONE`, and exited 1. **The
  unreadable fragment no longer exists.**
- Under the freeze, `--into` named a fragment with mode 0 and the record was
  unparseable. The run printed `ledger unreadable`, then `wrote …:1 Re-read ·
  O1`: `reverify_into` reads `read(into) or ""` and writes the new row over
  the file it could not read. Then the restore removed it. That overwrite is
  older than this item (#736). Before this branch it replaced the fragment's
  rows with one row. Now the file is deleted outright.

Any exception between the snapshot and the return takes the same path,
because `except BaseException` calls `restore`.

Why it matters: the transaction exists so that a run which cannot record
loses nothing. Here it removes a whole ledger file. In local mode `seal/` is
not committed, so nothing can bring it back. The trigger is narrow: a file
in scope that will not read, plus a run that fails to record. The result is
the worst one this feature can produce.

The fix (fenced below; applied in the clone, both probes inverted, the writer
module green) changes two things.

- **Snapshot.** It tells *absent* (`not os.path.lexists`) apart from *there
  and unreadable* (a sentinel), and `restore` leaves the second alone.
- **`--into`.** A run whose `--into` is there and will not read is refused
  before anything is written. That also ends the older overwrite.

### 🟡 11 — A SIGTERM or SIGHUP between the re-stamp and the record erases the drift unrecorded

`skills/evidence-check/scripts/evidence_check.py:4858` (`main`'s
transaction).

`except BaseException` sees exceptions and `KeyboardInterrupt`. It does not
see a signal whose default action ends the process: SIGTERM, which a timeout
sends, and SIGHUP, which a closed terminal sends. SIGKILL and a power cut are
out of reach of any handler.

The window opens at `reverify`'s first `write_atomic` and closes at the
record's `write_atomic`. Between them sits `released_drift` over every ledger
file. Measured on this repository: 9.83 s over 46 files.

Executed: a wrapper replaced `record_pact_changes` with
`os.kill(os.getpid(), SIGTERM)`.

- The process ended with status -15, and the ledger was re-stamped.
- A second run, as the remedy would have it, printed `0 rows re-verified`
  and exited 0. Nothing was ever recorded.

That is red 1's failure exactly, on a narrower trigger. The code says
otherwise: `main`'s comment reads *"A run that dies part way is no
different"*. So does the policy, in `docs/the-pact.md:132` (*"or a run that
dies part way"*) and `skills/evidence-check/SKILL.md:338` (*"or where the run
dies"*).

The fix (fenced below; applied in the clone, the probe exits 143 with the
ledger intact, and the next run records the one row) turns SIGTERM and
SIGHUP into `SystemExit` for the run, so the `except` puts the ledger back.
The two sentences then name the limit that remains, SIGKILL and a power
cut. Windows has no SIGHUP, and the fix guards it with `hasattr`.

### 🟡 12 — A change re-landed after its revert is re-stamped and not recorded

`skills/evidence-check/scripts/evidence_check.py:3699` (`held`).

`held` is the set of every `(clause, row, coordinate, old, new)` ever
recorded. A move is skipped wherever it appears anywhere in the file.
Executed:

1. Run 1, A→B: the move is recorded.
2. Run 2, the revert B→A: recorded.
3. Run 3, the re-land A→B: the ledger is re-stamped to B and dated
   `2026-09-06`, and **nothing is recorded**. `A→B` is already in the file,
   from run 1.

The record's last word for the coordinate is now `B→A`, while the code is at
B. A content hash that does not move means `pact-check` sees nothing new,
and the pact's repository is never told the change came back. Reverting a
change and landing it again later is an ordinary workflow, and each step is
a `--reverify`.

Round 1's yellow 2 fix did not cause this. The row-level key before it
skipped identical rows the same way. But the fix rewrote this block, and
the property it states, *"running it twice records nothing twice"*, needs
only the last recorded state. The fix (fenced below; applied in the clone,
the probe records the third row, and every idempotence case stays green)
keys each `(clause, row, coordinate)` on the last thing recorded for it.

### 🟡 13 — Under an intended `always`, a declaration that will not read is still silent at exit 0

`skills/evidence-check/scripts/evidence_check.py:3635`.

Round 1's fix refuses a declaration that will not read only where a moved
row cites a pact anchor: `if refused and any(e[3] for e in entries)`. A row
that cites none is owed under `Pact notify | always`. A refused declaration
cannot say whether `always` was meant: `pact_declaration` returns `notify`
None for a bad value, and `pacts` [] for a bad `Pact` row. Executed, with a
drifted row citing no clause:

| `seal/config.md` | Exit | Ledger | Record | Line |
|---|---|---|---|---|
| `Pact notify \| allways` | 0 | re-stamped | none | none |
| `Pact \| orders api`, `Pact notify \| always` | 0 | re-stamped | none | none |
| both rows valid, `always` (control) | 0 | re-stamped | one `—` row | `recorded` |

That is red 1's fifth path, the silent one, for the rows `always` owes. The
fix (fenced below; applied in the clone, both rows exit 1 with the ledger
intact and the control unchanged) treats such a row as unknown wherever the
declaration cannot rule `always` out, and words the `LEFT` line for a row
that cites no clause.

### 🟡 14 — A coordinate the re-read leaves records nothing, at exit 0

`skills/evidence-check/scripts/evidence_check.py:3040` and `:3050`
(`reverify`), and `:3426` (`reverify_into`).

`reverify` appends a pending entry for a coordinate it leaves BROKEN, but
not at two sibling `left` exits. One is *the file could not be read*: a file
deleted or renamed under a `path#unit>"claim"` coordinate, which the check
calls BROKEN, `file not found`. The other is *the anchored statement is
gone*, which the check calls DRIFTED. `reverify_into`'s *no one place to
hash* is the same exit under the freeze. Executed, each with the coordinate
cited beside a clause:

| Edit | `--reverify --into` | Record | Plain check |
|---|---|---|---|
| the quoted statement removed | exit 0, `… left` | none | exit 1, DRIFTED |
| the file deleted | exit 0, `… left` | none | exit 2, BROKEN |
| (the same coordinate after either, with the fix) | exit 0 | one `BROKEN` row | — |

A major-only coordinate whose unit is gone **is** recorded as `BROKEN`
(`test_s11_a_broken_coordinate_is_recorded_and_the_row_left`). So two
coordinates the check grades alike are recorded differently.

The row is not re-stamped, so the drift stays visible. The usual repair also
records: edit the locator, keep the hash, and run `--reverify`. The loss
comes where the person re-points the row with a hash typed by hand, or
removes it. Removing a row is what the repository's own rule asks for when
an anchor's code is gone. Either way the pact change is never recorded, and
the run that saw the change printed nothing about a pact.

The fix (fenced below; applied in the clone, both cases record one `BROKEN`
row, and a second run adds nothing) appends the same pending entry at the
three exits. The record's word for them is `BROKEN`, which
`reverify`'s own docstring already uses for *"a coordinate it leaves because
no one place holds it"*.

### 🟡 15 — The walker still reads tables cmark-gfm does not render, in two shapes the docstring does not state

`hooks/config.py:1020` (`gfm_table`'s check of the line above), with the
docstring's limit sentence at `:999`.

Round 2's generator, fenced under *Executed probes*, has its own vocabulary
of 88 line kinds, three headers, and indented headers. It reads cmark-gfm's
raw-HTML-omitted output with a regex rather than `html.parser`. At
`ed1476aa`, over 300,000 documents for each of two seeds, it found 70 tables
the walker reads with no refusal where cmark-gfm renders none:

| Mechanism | Seed 11 | Seed 23 | Stated in the docstring |
|---|---|---|---|
| a fence inside an HTML block of kind 6–7 (49 and 58; 24 and 28 with rows) | 49 | 58 | yes |
| a header indented 1–3 spaces under a list item, across a blank line | 19 | 12 | **no** |
| a line `unfenced` hides directly above the header (a comment holding a fence, over a list item) | 2 | 0 | **no** |

- **The indented header.** Take `- x`, a blank line, then `  | Signatory |`
  with `|---|` at column 0. The header becomes the list item's paragraph,
  and no table renders. The walker reads one row.
- **The docstring's list-item limit names the wrong shape.** It names
  `- x`, a blank line, *an indented paragraph, then the header*. The
  line-above rule now refuses that shape (executed). The shape that still
  reads is the indented header.
- **The hidden line.** Take a comment opened with `&lt;!--` that holds a
  fence, then `-->`, then `- note`, then the header. `unfenced` hides
  `- note` under its fence-only reading, so the walker sees a gap above the
  header where cmark-gfm sees a list item's lazy paragraph. Executed by
  hand: one row read, no table rendered.

The stated kind 6–7 limit has the same root. In each such document the line
directly above the header is a non-blank line inside the HTML block. A kind
6–7 block ends at the first blank line, so a header inside one always has a
non-blank line above it. `unfenced` hides that line as a fence, and the
check reads the line the walk shows, not the line as written.

The fix (fenced below) makes two changes.

- **The line above.** It checks the raw line directly above the header,
  hidden or not.
- **The indent.** It refuses an indented header where a list item stands
  above it since the last heading or thematic break.

Applied in the clone, round 2's generator found **0 disagreements over
600,000 documents** (seeds 11 and 23). The five pact modules gave 818 passed
and 2 failed.

**The trade.** The two failing ids pin a table directly under a closed fence
and under a closed comment, which GFM does render:
`test_a_table_under_a_block_that_has_ended_is_read[a closed fence directly
above, under a paragraph]` and `[… a closed comment …]`. The fix refuses
both with the blank-line remedy, as round 1's yellow 5 fix already does for
a paragraph. S3's indented tables, a heading above them and no list,
stay read. `test_a_table_indented_as_gfm_permits_is_read_and_not_refused`
and `an indented header, delimiter and row` stay green. Round 1 deferred the
kind 6–7 limit to the orchestrator, and this fix closes it.

## The oracle's switch hides no table

Round 2 checked the switch to `CMARK_OPT_DEFAULT` without `html.parser`, by
reading the rendered HTML directly.

- **Table counts.** Across each 300,000-document run, the count of
  `<table>` followed by `<thead>` is the same in the raw-HTML-kept and the
  raw-HTML-omitted renders, in every document. A raw `<table>` line in the
  vocabulary is not counted, because cmark writes no `<thead>` after it.
- **Readings.** Round 2's regex reading of the omitted render equals the
  build oracle's `rows_under` in every document.

cmark parses the block the same way under both options, and the safe
render's `&lt;!-- raw HTML omitted -->` is a comment `html.parser` skips. The
switch also removes a second case of the same kind: a raw `<script>` or
`<textarea>` in a cell, which `html.parser` reads as text running to its end
tag.

## The merge, `2b25dc86`

- **The modules together.** `tests/test_a_released_row_is_read_again_in_a_fragment.py`
  with the five pact modules: 1028 passed, run together.
- **The resolution.** `released_drift` keeps #740's member-keyed filter and
  the `pick` loop, and both `broken.append` sites take this branch's
  5-tuple. Its only consumers are `reverify_into`, which unpacks five, and
  `main`, which discards it. `main` passes `ledgers`, #740's whole narrowed
  list, to `reverify_into` inside this branch's transaction. Read.
- **L4.** Each clause of #736's fragment row L4 was read against the merged
  `main`, `reverify_into` and `released_drift`, and each holds. The clauses
  covered: the `--into` and `--checked` refusals at `:4724` and `:4730`, the
  freeze's LEFT path, #740's narrowing, and the transaction's exception. The
  Notes cell keeps both sides' markers. Read. The exception clause says
  *"every ledger file it wrote … is put back as it was"*. That is true, and
  🔴 10 is a file it did not write.
- **`bin/correction-check --range origin/release/v0.18.0...HEAD`**: exit 0.
  Two merge commits examined, no correction marker dropped, no released
  ledger file changed.
- **`bin/evidence-check --strict .`**: exit 0, 4272 ok, 0 drifted, 0 broken.
  The records arm read 8 work items, with 0 refused and 0 drifted.

## What else was checked

- **What the restore puts back.** The snapshot is taken after the person's
  edits and before any write, so a pre-run edit to a ledger is kept. Every
  case writes its ledger with no commit and asserts those bytes. The restore
  rewrites every file in scope, including files the run never wrote, with
  the snapshot's bytes. A save made to one of those files during the
  ten-second window would be reverted. That was read, not executed, and it
  is not reported.
- **Encoding.** An AST scan of every file I/O call added in the fix range
  found none without `encoding=`. `snapshot` and `restore` use bytes.
- **The close commit `ed1476aa`.** Read. It appends `· NAME NOT IN TREE`
  after the closing pipe of ten verdict rows. `chain_check.py --baseline
  origin/release/v0.18.0` read the record and named only two things. One is
  the expected `Broad gate | not yet`. The other is `Pass` beside `Fixes
  checked by: nobody`, which this round answers.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 10 | The restore removes a ledger file the snapshot could not read (`snapshot` reads `OSError` as absent), and an unreadable `--into` is overwritten first (older, #736) | `skills/evidence-check/scripts/evidence_check.py:3519` | open | executed: an unreadable sibling fragment and an unreadable `--into` are both gone after a run that could not record; fix run in the clone: both kept, `--into` refused at exit 2 |
| 🟡 11 | A SIGTERM or SIGHUP between the re-stamp and the record erases the drift with nothing recorded; the policy says a run that dies is put back | `skills/evidence-check/scripts/evidence_check.py:4858` | open | executed: SIGTERM at the record step, status -15, ledger re-stamped, the next run records nothing; the window is `released_drift`, 9.83 s on this repository; fix run in the clone: status 143, ledger intact, next run records one row |
| 🟡 12 | A change re-landed after its revert is re-stamped and not recorded: the key is ever-recorded, not last-recorded | `skills/evidence-check/scripts/evidence_check.py:3699` | open | executed: A→B, B→A, A→B gives two rows, ledger at B; fix run in the clone: three rows, every idempotence case green |
| 🟡 13 | Under an intended `always`, a `Pact` row or `Pact notify` that will not read is silent at exit 0, the ledger re-stamped | `skills/evidence-check/scripts/evidence_check.py:3635` | open | executed: both shapes exit 0 with no record and no line; fix run in the clone: exit 1, ledger intact |
| 🟡 14 | A coordinate the re-read leaves (statement gone, file deleted under a minor anchor, no one place under the freeze) records nothing at exit 0, while a major-only BROKEN is recorded | `skills/evidence-check/scripts/evidence_check.py:3050` | open | executed: both cases exit 0 with no record; fix run in the clone: one `BROKEN` row each, a second run adds nothing |
| 🟡 15 | The walker reads tables cmark-gfm does not render in two unstated shapes, and the docstring's list-item limit names a shape it now refuses | `hooks/config.py:1020` | open | executed: 70 of 300,000 per seed at the target; fix run in the clone: 0 of 600,000, two pinned ids invert (named in the fix) |
| 🟢 | round 1's blocking finding is closed — an owed change that cannot be recorded re-stamps nothing on the five paths it named | `skills/evidence-check/scripts/evidence_check.py:4851` | confirmed | executed: 11 cases red with `restore` and the refusal disabled; each path prints `LEFT … nothing was re-stamped`, exits 1, ledger byte for byte. The `always` arm of its silent path is 🟡 13 |
| 🟢 | round 1's yellow 2 is closed — a second identical run adds nothing, per coordinate and in the reader's form | `skills/evidence-check/scripts/evidence_check.py:3699` | confirmed | executed: 5 cases red reversed; this repository's three `\|` coordinates, six runs over two edits, no duplicate. 🟡 12 is the reland the same key suppresses |
| 🟢 | round 1's yellow 3 is closed — `amended` is judged at the record's current hash only | `skills/evidence-check/scripts/pact_check.py:848` | confirmed | executed: its case red reversed |
| 🟢 | round 1's yellow 4 is closed — `.`, `-`, `_` for or before the slash are refused | `skills/evidence-check/scripts/pact_check.py:240` | confirmed | executed: 7 cases red reversed |
| 🟢 | round 1's yellow 5 is closed for the two mechanisms it measured — a line directly above, an open kind 1–5 block | `hooks/config.py:1021` | confirmed | executed: 6 cases red reversed; round 2's generator finds neither mechanism in 300,000. What remains is 🟡 15 |
| 🟢 | round 1's white 6 is closed — a pipe after an even backslash run is refused | `hooks/config.py:906` | confirmed | executed: 2 cases red reversed |
| 🟢 | round 1's white 7 is closed — a review row naming a dropped signatory stays refused, and the policy says so | `docs/the-pact.md` | confirmed | read; its case green in the module |
| 🟢 | round 1's white 8 is closed — a pact review takes a whole record, stated | `docs/the-pact.md` | confirmed | read |
| 🟢 | round 1's white 9 is answered — the `Re-read · P1-1` row carries its `Corrected` note | `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md` | answered | read |
| 🟢 | the merge keeps #740's narrowing and this item's transaction; L4 holds of the merged code | `skills/evidence-check/scripts/evidence_check.py:3278` | confirmed | executed: #743's grid with the five pact modules, 1028 passed; `correction-check` exit 0; `evidence-check --strict` 0 drifted, 0 broken. L4 read |
| 🟢 | the oracle's switch to the raw-HTML-omitted render hides no table | `tests/gfm_table_oracle.py` | confirmed | executed: table counts equal across both renders, and round 2's regex reading equals `rows_under`, in every one of 600,000 documents |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `ed1476aa` | ❓ out of verified scope | the broad gate is the sealer's, once the rounds settle; nothing here ran it, and the `unverified` label it carries is honest |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_one_table_walker_reads_what_gfm_renders.py`, `tests/test_a_pact_review_takes_a_pact_change.py`, `tests/test_a_signatory_records_a_pact_change.py`, `tests/test_pact_check.py`, `tests/test_a_signatory_declares_its_pact.py`, `tests/test_a_released_row_is_read_again_in_a_fragment.py` at `ed1476aa` | 1028 passed |
| Each fix's code hunk reversed on HEAD, its module run, then restored: `881e6005`, `06264ade`, `ba5ebee3`, `2e550f45`, `26d4ef53`; for `26a3199b` (which does not reverse cleanly) `restore` made a no-op and the `Pact`-row refusal disabled | 1, 7, 2, 6, 5 and 11 cases red, each exactly the fix's own cases |
| `bin/correction-check --range origin/release/v0.18.0...HEAD` | exit 0; 2 merge commits, no marker dropped, no released ledger file changed |
| `bin/evidence-check --strict .` | exit 0; 4272 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| `chain_check.py --baseline origin/release/v0.18.0 --root .` | exit 0; names `Broad gate` `not yet` and `Pass` beside `Fixes checked by: nobody`, both expected |
| Writer probes in temporary signatories: an unreadable sibling fragment; an unreadable `--into` under the freeze; SIGTERM at the record step; A→B, B→A, A→B; `always` with a bad `Pact notify` and a bad `Pact` row; a piped label; this repository's three `\|` coordinates over six runs; a statement gone and a file deleted under a minor anchor | 🔴 10, 🟡 11, 🟡 12, 🟡 13, 🟡 14 reproduced as described; the piped label and the six runs record nothing twice |
| `released_drift` timed over this repository's 46 ledger files | 9.83 s, the window 🟡 11 measures |
| Round 2's generator (fenced below), 300,000 documents, seeds 11 and 23, at `ed1476aa` | 70 and 70 tables read where none renders: kind 6–7 fence 49 and 58, indented header under a list item 19 and 12, a hidden line above 2 and 0; oracle checks 0 and 0 |
| The fixes for 🔴 10, 🟡 11, 🟡 12, 🟡 13 and 🟡 14 applied together in the clone, then reverted | every probe inverted; writer module, #743's grid and the probes 251 passed; `test_pact_check.py` and `test_a_pact_review_takes_a_pact_change.py` 109 passed |
| The fix for 🟡 15 applied in the clone, then reverted | generator 0 of 300,000 for each seed; the five pact modules 818 passed, 2 failed (the two ids the fix names) |
| An AST scan of every file I/O call added in the fix range for a missing `encoding=` | none |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

### Round 2's generator

```python
# Round 2's generator: walker against cmark-gfm, independent of the build's
# corpus. Run from a clone with the suite's venv:
#   .venv/bin/python gen.py <clone> <documents> <seed>
import collections, html, importlib.util, os, random, re, sys

CLONE, N, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path[:0] = [os.path.join(CLONE, "hooks"), os.path.join(CLONE, "tests")]
spec = importlib.util.spec_from_file_location("cfg", os.path.join(CLONE, "hooks", "config.py"))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)
import cmarkgfm  # noqa: E402
from cmarkgfm.cmark import Options  # noqa: E402
import gfm_table_oracle as build_oracle  # noqa: E402

C = "<" + "!--"
HEADERS = {"sig": ("Signatory",), "rec": ("Clause", "Row", "Code", "Checked"),
           "rev": ("Signatory", "Change", "Verdict")}
BODY = {"sig": ["| https://example.com/o/a |", "| https://example.com/o/b |", "|x|"],
        "rec": ["| c | r | k | 2026-01-01 |", "|c|r|k|2026-01-02|"],
        "rev": ["| s | i@abcdef12 | holds |", "|s|i@abcdef12|amended|"]}
VOCAB = [
    "", "", "", "text", "more text here", "a | b", "x \\| y", "Intro",
    "# Heading", "## Two", "###### six", "#notheading",
    "===", "---", "-", "--", "***", "___", "- - -", "* * *",
    "- item", "* item", "+ item", "1. one", "2. two", "1) one", "3) three", "-", "1.", "*",
    "> quote", ">", "> | Signatory |", ">> deep",
    "    indented", "\tindented tab", "  two spaces", "   three spaces",
    "```", "```python", "~~~", "~~~~", "````",
    C + " c -->", C, "-->", C + " open", "end -->",
    "<pre>", "</pre>", "<script>", "</script>", "<style>", "</style>", "<textarea>", "</textarea>",
    "<?php", "?>", "<!DOCTYPE html>", "<!X", ">", "<![CDATA[", "]]>",
    "<div>", "</div>", "<table>", "</table>", "<p>", "<details>", "<a>", '<a href="x">',
    "<span>", "</a>", "<h1", "<br>", "<b>bold</b>",
    "[ref]: https://example.com", "[^1]: note",
    "| Name |", "|---|", "| x |", "| a | b |", "|---|---|", ":-:", "| --- |",
    "|", "||", "| |", "\\|", "\\\\|", "|\\\\| x |",
    "&#124;", "<https://example.com>", "https://example.com",
]
FENCE_START = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def my_tables(out):
    """[(header, rows)] by regex over cmark's own raw-HTML-omitted output."""
    def cells(s, tag):
        return tuple(html.unescape(re.sub(r"<[^>]*>", "", c)).strip()
                     for c in re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", s, re.S))
    found = []
    for t in re.finditer(r"<table>(.*?)</table>", out, re.S):
        head = re.search(r"<thead>(.*?)</thead>", t.group(1), re.S)
        tb = re.search(r"<tbody>(.*?)</tbody>", t.group(1), re.S)
        rows = [cells(tr, "td") for tr in re.findall(r"<tr>(.*?)</tr>", tb.group(1), re.S)] if tb else []
        found.append((cells(head.group(1), "th") if head else (), rows))
    return found


def doc(rng):
    kind = rng.choice(list(HEADERS))
    header = HEADERS[kind]
    head_line, delim = "| " + " | ".join(header) + " |", "|" + "---|" * len(header)
    pre = [rng.choice(VOCAB) for _ in range(rng.randint(0, 6))]
    body = [rng.choice(BODY[kind]) if rng.random() < 0.6 else rng.choice(VOCAB)
            for _ in range(rng.randint(0, 4))]
    v = rng.random()
    if v < 0.1:
        head_line = " " * rng.randint(1, 3) + head_line
    elif v < 0.15 and len(header) == 1:
        delim = "| :-- |"
    lines = pre + [head_line, delim] + body
    if rng.random() < 0.2:
        lines += [rng.choice(VOCAB) for _ in range(rng.randint(1, 3))]
    return header, "\n".join(lines) + "\n"


def cause(text, header):
    lines = text.split("\n")
    k = next(i for i, ln in enumerate(lines) if ln.strip() == "| " + " | ".join(header) + " |")
    html_seen = False
    for ln in lines[:k]:
        if config.blocks.columns(ln) < 4 and config.html_start(ln.lstrip(" "))[0] in (6, 7):
            html_seen = True
        if FENCE_START.match(ln) and html_seen:
            return "a fence inside an HTML block of kind 6-7"
    if lines[k].startswith(" ") and any(re.match(r"^ {0,3}([-+*]|\d+[.)])( |$)", ln) for ln in lines[:k]):
        return "an indented header under a list item"
    return "other"


rng, stats, first = random.Random(SEED), collections.Counter(), {}
for _ in range(N):
    header, text = doc(rng)
    safe = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_DEFAULT)
    unsafe = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE)
    if safe.count("<table>\n<thead>") != unsafe.count("<table>\n<thead>"):
        stats["oracle: a table only one render has"] += 1
    mine = next((r for h, r in my_tables(safe) if h == header), None)
    if mine != build_oracle.rows_under(text, header):
        stats["oracle: the build's reading differs from this one"] += 1
    rows, refusals = config.gfm_table(text, header)
    got = [c for _n, c in rows]
    if refusals:
        stats["refused"] += 1
    elif mine is None:
        key = f"DISAGREE, read where none renders ({'rows' if got else 'empty'}): {cause(text, header)}"
        stats[key] += 1
        first.setdefault(key, text)
    elif got != mine:
        stats["DISAGREE, rows differ"] += 1
        first.setdefault("DISAGREE, rows differ", text)
    else:
        stats["agree"] += 1
for k, v in sorted(stats.items()):
    print(f"{v:8d}  {k}")
for k, v in first.items():
    print(f"first of {k}: {v!r}")
```

## Paste-ready fixes

### 🔴 10 — `skills/evidence-check/scripts/evidence_check.py`

Replace `snapshot`, and add the sentinel above it:

```python
# A file `snapshot` found there and could not read: `restore` leaves it alone,
# because a file it never read is one it cannot put back, and reading it as
# absent removed it (round 2 of #647 C and D, red 10).
UNREAD = object()


def snapshot(paths):
    """{path: its bytes; None where nothing is there; `UNREAD` where a file is
    there and will not read} for each of PATHS."""
    out = {}
    for path in paths:
        if not os.path.lexists(path):
            out[path] = None
            continue
        try:
            with open(path, "rb") as handle:
                out[path] = handle.read()
        except OSError:
            out[path] = UNREAD
    return out
```

In `restore`, first thing in the loop:

```python
    for path, data in before.items():
        if data is UNREAD:
            continue
        if data is None:
```

In `main`, directly under `before = snapshot(...)`:

```python
        if into and before[into] is UNREAD:
            sys.stderr.write(
                f"evidence_check: `--into {args.into}` is there and will not "
                "read, and the run would write over it — nothing was written\n"
            )
            return 2
```

`tests/test_a_signatory_records_a_pact_change.py`:

```python
UNREADABLE = pytest.mark.skipif(
    os.name == "nt" or (hasattr(os, "geteuid") and os.geteuid() == 0),
    reason="a mode of 0 stops no read on Windows or as root",
)


@UNREADABLE
def test_a_ledger_that_will_not_read_is_not_removed_by_the_restore(repo):
    """The snapshot read an unreadable ledger as absent, and the restore
    removed it (round 2, red 10)."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    other = cite(
        repo,
        [row("X1", "", "src/orders.py#evict@00000000")],
        where="seal/ledger/1790000000-other.md",
    )
    os.chmod(other, 0)
    try:
        move_serialize(repo)
        code, out = run(repo, "--checked", "2026-09-04")
        assert code == 1 and UNDONE in out, out
        assert os.path.lexists(other), out
    finally:
        if os.path.lexists(other):
            os.chmod(other, 0o644)


@UNREADABLE
def test_an_into_that_will_not_read_is_refused_before_anything_is_written(repo):
    """`reverify_into` wrote its rows over an `--into` it could not read."""
    frag = cite(repo, ["| F9 · kept | `src/orders.py#evict@00000000` | read | 2026-10-01 | |\n"])
    os.chmod(frag, 0)
    try:
        move_serialize(repo)
        code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
        assert code == 2 and "will not read" in out, out
    finally:
        os.chmod(frag, 0o644)
    assert "F9 · kept" in frag.read_text(encoding="utf-8")
```

### 🟡 11 — `skills/evidence-check/scripts/evidence_check.py`, `docs/the-pact.md`, `skills/evidence-check/SKILL.md`

`import signal` beside `import stat`. In `main`, after the 🔴 10 refusal and
before `try:`:

```python
        # A signal no `except` sees -- SIGTERM from a timeout, SIGHUP from a
        # closed terminal -- killed the run between the re-stamp and the
        # record, and the drift was gone (round 2 of #647 C and D, yellow
        # 11). Raised here as SystemExit, the `except` below puts the ledger
        # back. A SIGKILL or a power cut stays out of reach of any handler.
        def interrupted(signum, _frame):
            raise SystemExit(128 + signum)

        for name in ("SIGTERM", "SIGHUP"):
            if hasattr(signal, name):
                signal.signal(getattr(signal, name), interrupted)
```

and `main`'s comment above `try:` becomes:

```python
        # A run stopped part way -- an exception, an interrupt, SIGTERM or
        # SIGHUP -- is no different: what it wrote is put back, so no
        # re-stamp outlives the record it owed.
```

`docs/the-pact.md:131-132`, *"a copy of the checker with no `hooks/`, or a
run that dies part way."* becomes:

```markdown
`Pact` rows that will not read, a copy of the checker with no `hooks/`, or a
run stopped part way by an exception, an interrupt, SIGTERM or SIGHUP. A
SIGKILL or a power cut between the re-stamp and the record is out of reach
of any handler and still loses the drift.
```

`skills/evidence-check/SKILL.md:338`, *"or where the run dies"* becomes:

```markdown
`Pact` rows will not read, or where the run is stopped by an exception, an
interrupt, SIGTERM or SIGHUP (a SIGKILL or a power cut is out of reach) —
```

`tests/test_a_signatory_records_a_pact_change.py`:

```python
@pytest.mark.skipif(os.name == "nt", reason="SIGTERM ends a Windows process before any handler")
def test_a_sigterm_between_the_restamp_and_the_record_puts_the_ledger_back(repo, tmp_path):
    """A signal `except` does not see erased the drift unrecorded (round 2,
    yellow 11)."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    wrapper = tmp_path / "killed.py"
    wrapper.write_text(
        "import importlib.util, os, signal, sys\n"
        f"spec = importlib.util.spec_from_file_location('ec', {SCRIPT!r})\n"
        "ec = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(ec)\n"
        "ec.record_pact_changes = lambda *a: os.kill(os.getpid(), signal.SIGTERM)\n"
        f"sys.argv = ['evidence_check.py', '--reverify', '--into', {FRAGMENT!r}, "
        f"'--checked', '2026-09-04', {str(repo)!r}]\n"
        "sys.exit(ec.main())\n",
        encoding="utf-8",
    )
    done = subprocess.run(
        [sys.executable, str(wrapper)], cwd=str(repo), capture_output=True, encoding="utf-8"
    )
    assert done.returncode != 0, done.stdout + done.stderr
    assert ledger.read_text(encoding="utf-8") == "".join(rows)
```

### 🟡 12 — `skills/evidence-check/scripts/evidence_check.py`, `record_pact_changes`

Replace the `held` block and its two uses:

```python
    # The last thing recorded for each coordinate of each clause and row, in
    # the form the record's reader reads a cell in (`\\|` a pipe). A
    # coordinate is recorded again only where what it did now is not what it
    # was last recorded doing: a second identical run adds nothing, and a
    # change re-landed after its revert is recorded (round 2 of #647 C and
    # D, yellow 12).
    last = {}
    for _l, clause, row, code, _c in rows:
        for part in CODE_PART.finditer(code):
            last[(clause, row, part.group("coord"))] = part.group("old", "new")
    date = checked or datetime.date.today().isoformat()
    new = []
    for where, clause, row, parts in owed:
        key = (config.unescaped(clause), config.unescaped(row))
        fresh = [
            (coord, old, nw)
            for coord, old, nw in parts
            if last.get((*key, config.unescaped(coord))) != (old, nw)
        ]
        if not fresh:
            continue
        last.update(((*key, config.unescaped(c)), (o, n)) for c, o, n in fresh)
```

The docstring sentence *"A coordinate already recorded for the same clause
and row, with the same move or the same BROKEN, is not recorded again"*, and
`docs/the-pact.md:146-149` the same, become:

```markdown
A coordinate whose last recorded row for the same clause and ledger row says
the same move or the same `BROKEN` is not recorded again, compared as the
record's reader reads a cell, so a second identical run leaves the record
byte for byte as it was and its content hash with it; a change that comes
back after its revert is recorded, because the record's last word for it was
the revert.
```

`tests/test_a_signatory_records_a_pact_change.py`:

```python
def test_a_change_relanded_after_its_revert_is_recorded(repo):
    """A→B, B→A, A→B: the third is a change the pact's repository has not
    seen since the revert (round 2, yellow 12)."""
    a = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{a}")])
    b = move_serialize(repo)
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    (repo / "src" / "orders.py").write_text(SOURCE, encoding="utf-8")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-06")
    assert code == 0, out
    rows = record_rows(repo)
    assert len(rows) == 3, rows
    assert rows[-1].endswith(
        f"`src/orders.py#serialize@{a}` → `@{b}` | 2026-09-06 |"
    ), rows
```

### 🟡 13 — `skills/evidence-check/scripts/evidence_check.py`, `record_pact_changes`

Replace the refusal block:

```python
    # A row citing a pact is owed under any `Pact notify`; a row citing none
    # is owed under `always`, and a declaration that will not read cannot
    # say it is not `always` (round 2 of #647 C and D, yellow 13).
    blind = declared is None or declared[1] in (None, config.NOTIFY_ALWAYS)
    unread = [e for e in entries if e[3] or blind]
    if refused and unread:
        # Silent before: a row that will not read reads as no pact declared,
        # and the drift went unrecorded at exit 0.
        for where, _row, _parts, anchors in unread:
            why = (
                "cites a pact clause"
                if anchors
                else "moved, and `Pact notify` may be `always`"
            )
            print(
                f"  LEFT  {where}  {why}, and the `Pact` rows will not read: "
                f"{refused[0]} — {NOT_RESTAMPED}; fix the row and run it again"
            )
        return 1
```

`tests/test_a_signatory_records_a_pact_change.py`:

```python
@pytest.mark.parametrize(
    "rows",
    [
        (("Pact", PACT_URL), ("Pact notify", "allways")),
        (("Pact", "orders api"), ("Pact notify", "always")),
    ],
    ids=["a Pact notify that will not read", "a Pact row that will not read, always"],
)
def test_under_always_a_declaration_that_will_not_read_leaves_the_row(repo, rows):
    """A row citing no clause is owed under `always`, and a refused
    declaration cannot say `always` was not meant (round 2, yellow 13)."""
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), *rows), encoding="utf-8"
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger_rows = [row("O1", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, ledger_rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "`Pact notify` may be `always`" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(ledger_rows), out
```

### 🟡 14 — `skills/evidence-check/scripts/evidence_check.py`, `reverify` and `reverify_into`

At *the file could not be read*:

```python
            if body is None:
                print(f"  {left_as}  the file could not be read — left")
                pending.append((m.start(), left_as, m.group("hash"), None))
                continue
```

At *the anchored statement is gone*:

```python
                    print(
                        f"  {left_as}  the anchored statement is gone from "
                        f"{locator} — the check calls this DRIFTED; left"
                    )
                    pending.append((m.start(), left_as, m.group("hash"), None))
                    continue
```

In `reverify_into`, at *no one place to hash*:

```python
            if new is None:
                left.append((where, f"{coord} — no one place to hash, so not re-read"))
                if moves is not None:
                    moves.append((path, key[1], coord, m.group("hash"), None))
                continue
```

`docs/the-pact.md:143-144`, *"(each coordinate from its recorded hash to its
current one, or `BROKEN`)"* becomes:

```markdown
coordinate from its recorded hash to its current one, or `BROKEN` where the
re-read leaves it because no one place holds it -- its unit, its file or its
quoted statement gone)
```

`tests/test_a_signatory_records_a_pact_change.py`:

```python
@pytest.mark.parametrize("how", ["the anchored statement is gone", "the file is gone"])
def test_a_coordinate_the_reread_leaves_is_recorded(repo, how):
    """Recorded as a major-only BROKEN is; it was left at exit 0 with
    nothing recorded (round 2, yellow 14)."""
    text = (repo / "src" / "orders.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/orders.py", "serialize", text)
    a, b = ec.minor_region("src/orders.py", text, places[0], '"return"')[0]
    h = ec.content_hash(ec.gfm_lines(text)[a - 1 : b])
    coord = f'src/orders.py#serialize>"return"@{h}'
    cite(repo, [row("O1", f"`{CLAUSE}`, ", coord)])
    if how == "the file is gone":
        (repo / "src" / "orders.py").unlink()
    else:
        (repo / "src" / "orders.py").write_text(
            SOURCE.replace("    return {'id': order.id}", "    pass"), encoding="utf-8"
        )
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `{coord}` BROKEN | 2026-09-04 |"
    ], out
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert len(record_rows(repo)) == 1
```

### 🟡 15 — `hooks/config.py`, `gfm_table`

Beside `raw_html_open`:

```python
def a_list_above(lines):
    """True where a list item stands in LINES since the last heading or
    thematic break at the start of a line, so an indented header under it can
    be more of that item: a blank line does not end a list item, and the
    header's indent decides (round 2 of #647 C and D, yellow 15)."""
    seen = False
    for line in lines:
        if blocks.columns(line) >= 4:
            continue
        content = line.lstrip(" ")
        if line[:1] != " " and (ATX_HEADING.match(line) or THEMATIC_BREAK.match(line)):
            seen = False
        elif LIST_ITEM.match(content):
            seen = True
    return seen
```

In `gfm_table`, replace the `above` lines and the line-above refusal's
condition:

```python
    head_index = shown[at][0]
    # The line as written, hidden or not: a line `unfenced` hides directly
    # above the header is a line GFM may read the header into -- a fence
    # inside an HTML block of kinds 6-7, or a list item the fence-only
    # reading hid (round 2 of #647 C and D, yellow 15).
    above = text.splitlines()[head_index - 1] if head_index > 0 else ""
    if shown[at][1][:1] == " " and a_list_above([ln for _i, ln in shown[:at]]):
        return [], [
            f"has a `| {name} |` header indented under a list item, which GFM "
            "reads as more of that item where the indent reaches its text — "
            "write the header at the start of its line"
        ]
    if above.strip():
        return [], [
            f"has a `| {name} |` header directly under `{above.strip()}`, "
            "and GFM renders a table under a line only in some of the shapes "
            "that line can take — leave a blank line above the header"
        ]
```

The docstring's paragraph from *"A header with a line directly above it is
refused"* to the end of *"What this cannot see"* becomes:

```python
    **A header with a line directly above it is refused**, with the
    blank-line remedy, whether or not `unfenced` hides that line, because
    whether GFM renders a table there depends on block state no reader here
    tracks -- a paragraph, a list item's lazy paragraph, a table above, a
    setext underline, an HTML block, a fence inside one -- and the first
    walker, which mirrored those rules line by line, read tables GFM does
    not render (round 1 of #647 C and D, yellow 5; round 2, yellow 15). So
    is a header indented under a list item, which a blank line does not end
    (`a_list_above`), and a header under an HTML block of kinds 1-5 left
    open above it (`raw_html_open`), which no blank line ends. **What this
    cannot see** is block state none of those three lines carries; round 2's
    generator found none over 600,000 documents.
```

`tests/test_one_table_walker_reads_what_gfm_renders.py`: take the two ids
`a closed fence directly above, under a paragraph` and `a closed comment
directly above, under a paragraph` out of
`test_a_table_under_a_block_that_has_ended_is_read`'s parameters (both now
refused, the trade round 1 already made for a paragraph), and add:

```python
@pytest.mark.parametrize(
    "text",
    [
        "- x\n\n  | Signatory |\n|---|\n| {u} |\n",
        "1) one\n\n   | Signatory |\n|---|\n| {u} |\n",
        "{c} open\n```\n-->\n- note\n| Signatory |\n|---|\n| {u} |\n",
        "<div>\n```\nx\n```\n| Signatory |\n|---|\n| {u} |\n",
    ],
    ids=[
        "a header indented into a bullet item",
        "a header indented into an ordered item",
        "a list item hidden under a comment holding a fence",
        "a fence inside a kind-6 block directly above",
    ],
)
def test_the_shapes_round_2_measured_are_refused(text):
    text = text.format(u="https://example.com/org/a", c="<" + "!--")
    assert oracle.rows_under(text, ("Signatory",)) is None, text
    rows, refusals = config.gfm_table(text, ("Signatory",))
    assert refusals, text


@pytest.mark.parametrize(
    "above",
    ["text\n```\nx\n```\n", "text\n" + "<" + "!-- c -->\n"],
    ids=["a closed fence directly above", "a closed comment directly above"],
)
def test_a_hidden_line_directly_above_the_header_is_refused(above):
    """GFM renders these; the walker refuses with the blank-line remedy,
    because the same hidden line is what hides a header GFM does not render."""
    text = f"# Pact\n\n{above}| Signatory |\n|---|\n| https://example.com/org/a |\n"
    rows, refusals = config.gfm_table(text, ("Signatory",))
    assert refusals and "blank line above the header" in refusals[0], refusals
```

## Regression tests to plant

| Finding | Destination | Case |
|---|---|---|
| 🔴 10 | `tests/test_a_signatory_records_a_pact_change.py` | the unreadable sibling ledger and the unreadable `--into`, fenced above |
| 🟡 11 | `tests/test_a_signatory_records_a_pact_change.py` | the SIGTERM wrapper, fenced above |
| 🟡 12 | `tests/test_a_signatory_records_a_pact_change.py` | A→B, B→A, A→B, fenced above |
| 🟡 13 | `tests/test_a_signatory_records_a_pact_change.py` | the two `always` declarations, fenced above |
| 🟡 14 | `tests/test_a_signatory_records_a_pact_change.py` | the statement and the file gone under a minor anchor, fenced above |
| 🟡 15 | `tests/test_one_table_walker_reads_what_gfm_renders.py` | the four measured shapes and the two hidden-line ids, fenced above |

Each case was seen red at `ed1476aa`: its probe reproduced the defect there.
Each was then green with its fix applied in the clone, and every fix was
reverted afterwards.

## Facts for the evidence ledger

- `released_drift` takes 9.83 s over this repository's 46 ledger files at
  `ed1476aa`. Measured. It is the window between `reverify`'s write and the
  record's, for whichever row lands with 🟡 11's fix.
- cmark-gfm 2025.10.22 reads a header indented 1–3 spaces, under a list item
  and across a blank line, with its delimiter at column 0, as the item's
  paragraph, and renders no table. With no list above, the same indented
  table renders. Measured. For the row that lands with 🟡 15's fix.
- With raw HTML kept and with it left out (`CMARK_OPT_DEFAULT`), cmark-gfm
  renders the same tables. Only the HTML it prints for a raw block differs. Measured over
  600,000 documents. For the oracle's row.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🔴 10 (the restore removes a ledger file it could not read), 🟡 11 (a SIGTERM or SIGHUP between the re-stamp and the record erases the drift unrecorded), 🟡 12 (a change re-landed after its revert is not recorded), 🟡 13 (under an intended `always`, a declaration that will not read is silent at exit 0), 🟡 14 (a coordinate the re-read leaves records nothing at exit 0), 🟡 15 (the walker reads tables cmark-gfm does not render in two unstated shapes)

Loses a record or crashes: yes — 🔴 10 removes a whole ledger file; 🟡 11, 🟡 12 and 🟡 13 each re-stamp the ledger with the owed pact change never recorded, so the drift that would record it is gone

## Proof block

Files opened this round:

- `seal/specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed/rounds/round-1.md` and `round-1-report.md`
- `skills/evidence-check/scripts/evidence_check.py`: `reverify` whole, `released_drift` and `reverify_into` (combined merge diff and HEAD), `read`, `write_atomic` head, `snapshot`, `restore`, `plugin_module`, `pact_change_item`, `record_pact_changes` whole, `main`'s reverify branch, `PACT_ANCHOR_RE`, `ledger_table_rows` head; the fix-range diff
- `hooks/config.py`: `unescaped` head, `pact_declaration`, `declared_pacts`, `table_cells`, `html_start`, `table_end`, `raw_html_open`, `gfm_table`, `pact_signatories`, `pact_changes`, `pact_reviews`, `hidden_lines`, `unfenced` head, the constants `NOTIFY_ALWAYS` and its siblings, `ATX_HEADING`, `THEMATIC_BREAK`, `LIST_ITEM`; the fix-range diff
- `skills/evidence-check/scripts/pact_check.py`: the fix-range diff, `PACT_MENTION_RE` and its comment
- `tests/gfm_table_oracle.py` whole; `tests/test_a_signatory_records_a_pact_change.py` head and the fix-range diff; `tests/test_one_table_walker_reads_what_gfm_renders.py` (`test_a_table_indented_as_gfm_permits_is_read_and_not_refused`, `test_a_table_under_a_block_that_has_ended_is_read`); `tests/test_a_signatory_declares_its_pact.py:323-333`; `tests/conftest.py` (`load_hook_module`)
- `docs/the-pact.md`, `skills/evidence-check/SKILL.md`, `templates/pact-review.md`, `skills/implement/orchestration.md`: the fix-range diffs and the lines cited
- `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` row L4; `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md` row `Re-read · P1-1`
- `bin/test`, `.github/scripts/run_tests.py` (the venv lines, `CMARKGFM`)
- the merge commit `2b25dc86` (message, file list, combined diff of `evidence_check.py`), the close commit `ed1476aa` (the record diff)

Executed: everything under *Executed probes*. Read: everything else, labelled
per row. Unverified: the full suite, the repository-wide lint and the
typecheck. They are the sealer's, after the rounds settle.
