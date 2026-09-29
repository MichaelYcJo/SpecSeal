# Implementation Plan: follow-up names are checked, and a re-read is dated

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned. Phase 1's rebase was done as a merge of `release/v0.16.0` at `3911a8cf` (A's squash) into this branch, at `56e53c90`: the frame's commits keep the SHAs its measurements cite, and the branch squashes into the release anyway.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. -->

## Summary

The records arm of `evidence_check.py` gains two readings.
`seal/follow-up.md` is read on every run and taken out of the name corpus. A
backticked name written as `path#name` is checked against the file its path
resolves to, or read as a bare name where the path does not resolve.
`--reverify` gains `--checked DATE`, which appends the date to the date cell
of each row whose hash it moved. Without the flag, `--reverify` names those
rows and leaves their dates alone. The RIDER that asked this is removed, and
every document describing either behaviour moves in the same commit as the
behaviour it describes.

## Technical context

All coordinates are in `skills/evidence-check/scripts/evidence_check.py`
unless named otherwise. They were read at `1f218ae6`, before A's squash, and
are **re-read after the rebase** (phase 1).

- **`check_records`** reads the live work items and returns early when there
  are none. The follow-up read has to happen before that return (F3). Every
  finding there is `(status, coordinate, detail)` and is printed by `main`.
- **`tree_names`** builds the corpus and leaves out `<home>/specs/` and
  `<home>/ledger/` by directory. `seal/follow-up.md` is one file, so it is
  left out as a file, in both walks (shared and local, F6).
- **`claim_lines`, `stated_names`, `stated_stamps`** are the claim rules. The
  follow-up file goes through them unchanged (F5). The coordinate form is a
  third reader beside `stated_names`, over the same `claim_lines` output.
- **`RECORD_NAME_RE`** matches a backticked span only where the whole span is
  an identifier. That is why `path#name` is invisible today. The coordinate
  form should take its path and locator grammar from **`ANCHOR_RE`** (its
  `path` group and its unquoted `locator` alternative), with no hash. Then a
  name "written the way a coordinate is written" means the same thing in both
  arms.
- **`place`** resolves a raw path against the root, `--map` and
  `--default-repo`, and refuses an escape. P1 resolves through it, so a record
  and a ledger row cannot disagree about where a path points.
- **`reverify`** walks every `ANCHOR_RE` match in `unquoted(text)` and
  splices hashes into `text`. It has no notion of a row. Dating needs one: the
  row a match sits in, that row's date cell, and a splice point in the raw
  line. **`grounds_cells`** already knows a table's header and the header-less
  fragment row (column 1 for `Code grounds`), and it splits cells with the
  shared `cell_rule`. The date-cell finder is its sibling, and it follows the
  same header rule, and the same five-column rule for a row under no header
  that `skills/evidence-check/scripts/evidence_check.py#overflow_rows` counts
  against `LEDGER_COLUMNS`. A header cell is `Checked`, else `Date` (M6).
  *Corrected 2026-09-29 in phase 2: the frame named the test helper A's
  squash replaced with that arm, and phase 2's reader refused the name.*
- **Splicing.** A cell boundary is an unescaped `|`, and `\|` inside a cell
  is text. The date splice must find the fourth boundary by that rule and
  never by a plain split, or a Notes cell holding `\|` moves the date. A case
  with an escaped pipe before the date cell pins it.
- **`main`**: `--checked` goes beside `--reverify`, and is validated before
  `ledgers` are resolved (R5). The precedent is
  `.github/scripts/rider_check.py`'s refusal of `--only` without `--reverify`.
- **The RIDER** at the head of `reverify` (dated `Verified 2026-09-25 against
  reverify@90289e25`) is deleted.
- **Item A (#585)** adds an overflow-cell arm to this file. If A's arm
  carries a row or header reader, phase 3 uses it instead of a second one
  (`questions.md` Q2).

**What breaks in six months.** A `path#name` whose name lives only in a
comment of the named file passes under the token rule, so a function deleted
while a comment still mentions it goes unnoticed. That is the price of the
token rule (Alternatives, row 1). A bare-file-name span is read against the
whole corpus, so a bare file name paired with a name that lives in a
different file passes (Alternatives, row 2). And `--checked` makes an unread re-stamp write a date
instead of leaving a stale one. D1's sentence and `--reverify`'s naming block
are what stand against that. The naming block is not a guard: a session can
still type the flag without reading.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **`path#name` checked by token in the named file** | A name that survives only in a comment of that file passes | **Chosen.** It is the arm's own claim (*the tree carries this name*) narrowed to the file the record points at. Over every record in the tree, the unit rule's extra refusals were both a nested function the file does define (M4) |
| `path#name` resolved as a unit (`resolve_unit`), the ledger's meaning | Refuses nested functions and locals that a record names correctly: two lines, both `block_ends_at`, among 424 resolved spans (M4). A record has no hash to break the tie with, and the ledger's grading of ambiguity (BROKEN) has no meaning for a name | Rejected |
| `path#name` checked against the whole corpus, ignoring the path | A case named under the wrong test file passes, which is the shape of #508's own instance (a case named under a file that has no such case) | Rejected |
| **An unresolved path falls back to the bare-name rule** | A bare file name paired with a name that another file carries passes | **Chosen.** 356 of 367 unresolved spans are bare file names (M4), the form `seal/follow-up.md` and the RIDERs use. The fallback checks them at least as strictly as the same name written bare, and refused 2 of 367 across all records, shipped included |
| An unresolved path is refused as not in the tree | 356 refusals of a spelling this repository uses deliberately (bare file names), shipped or not, including a RIDER's own style | Rejected |
| An unresolved path is skipped, as today | The half of the form most used in `seal/follow-up.md` rows stays unchecked, which is #508's gap left open | Rejected |
| **No underscore needed once the path resolves** | A one-word name that is prose but happens to follow `path#`. None was found: all 140 underscore-free names in 791 spans resolve (M4) | **Chosen.** The narrowing in `compound` exists because a single backticked word is usually prose, and a word after a resolving `path#` is not prose |
| **`seal/follow-up.md` out of the corpus** | A record naming something that only a follow-up row mentions is refused. No live record exists today to measure (M1) | **Chosen.** Kept in, the row that names a name is the evidence the name exists, and F1's red direction cannot be shown. It is the line `tree_names` already draws for a work item's own fragment |
| **Read `seal/follow-up.md` on every run, not only while a work item is live** | None found | **Chosen.** The file is permanent and its rows are live until removed. The shipped/unshipped boundary protects history, and a follow-up row is not history |
| Grade a follow-up refusal at exit 1 (warn) | One verdict word, `NOT-IN-TREE`, would carry two gradings, which is what `tests/test_one_word_one_meaning.py` exists to stop | Rejected |
| **`--checked` appends ` · D`** | A cell grows over years of re-reads | **Chosen.** 29 rows already hold date lists, and all 34 separators are ` · ` (M5). The history of readings is information |
| `--checked` replaces the cell with D | Deletes the record of earlier readings in 29 rows at their next re-stamp | Rejected |
| **Refuse a date later than the local date** | A reader east of CI's clock, just past midnight, is fine: the check is local and runs on their own clock. No legitimate future reading exists | **Chosen.** It is the typo class `2027-…` that the shape check cannot catch |
| Accept `today` as a value | A convenience that makes the date not a statement typed by whoever read it. The owner's answer is `--checked <date>` | Rejected |
| **A moved row with no date cell is left whole under `--checked`, named, exit 1** | The row stays DRIFTED until someone fixes its table | **Chosen.** Writing the hash alone recreates the exact state #387 reports: a row whose two halves disagree. Zero such anchors exist today (M6) |
| The date cell is `Checked` alone | 203 anchors under `Date` headers (M6) would be `LEFT` on every `--checked` run that reaches them | Rejected |
| **Dating the heal path (`identical content`)** | Dates a row nobody re-read, though its content is proven identical | **Chosen.** It is the owner's rule taken literally (*every row whose hash it moved*), and a rename's re-anchor moves the hash. Without the flag the row is named, so the reader sees it. A file moved whole keeps its hash, so its row is re-pointed and neither dated nor named. *Corrected 2026-09-29 by round 1's fix pass (🟡 1): this cell said every re-anchor moves the hash* |
| **RIDER deleted** | None | **Chosen.** Its question is answered, and `seal/follow-up.md`'s header says a rider whose ask is done is deleted |

## Phases

Vertical slices. Each phase writes its own ledger rows into the fragment and
commits them with the phase, and moves its documents in the same commit as
its behaviour (§14). **Phase 1's first step is the rebase.**

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **Rebase, then `seal/follow-up.md` is read.** First, rebase this branch onto `release/v0.16.0` once A's squash is on it. Re-read A's diff to `evidence_check.py` (for Q2) and every coordinate in *Technical context*. Write the fragment's first row, so the arm reads this work item's own records from the start (M1). Then F1–F8: the follow-up read before the early return; the file out of the corpus in both walks; `UNREADABLE`; the heading, summary line and refusal detail. Documents: D2's lines about `seal/follow-up.md`. Measure Q1 on the rebased tree and record it in `phases/phase-1.md` | F1–F7 cases, each seen red first. F8's existing case green. `tests/test_a_record_states_what_the_tree_has.py` and `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py` as the module's narrow run | 18ac24e9 |
| 2 | **`path#name` is checked.** P1–P7: the coordinate-form reader over `claim_lines`, `place` for the path, the token rule in the file, and the bare fallback. Documents: D2's lines about the form. Re-run Q1's measurement over live records and `seal/follow-up.md` | P1–P5 cases, each seen red first. The same two modules | 4f22852e |
| 3 | **`--reverify --checked`.** R1–R9: argument validation, the date-cell finder beside `grounds_cells`, splicing by unescaped pipe, the no-flag naming block, `LEFT` for R4, the RIDER removed. Documents: D1 whole, and D3 | R1–R7 cases, each seen red first. R8's existing case green. `tests/test_a_row_points_by_content.py` as the module's narrow run | bad06402 |
| 4 | **The ledger is true, re-stamped with the new flag.** Re-read every shared row that phases 1–3 drifted (M7 lists the units; the lenient check lists the rows), reading every row that cites each drifted coordinate. Re-stamp them in their own files with `--reverify --checked <date>` and a dated note, narrowed with `--ledger` to the files read. Correct any claim the edits made false (`Corrected <date>`). Write `changelog.md` | the lenient check over the tree (the drift it names is only this work's). `correction-check --range origin/release/v0.16.0...HEAD` reads clean | 7b7b70e8 |
| 5 | **The hash side ends a line where `ast` and GFM do (#664).** Added 2026-09-29 by the orchestrating session: round 2 of work item A (#585) found that `evidence_check.py` slices the region a hash covers out of `str.splitlines()`, so below a form feed, NEL, U+2028 or the other five characters `splitlines` also ends a line at, a `.py` anchor hashes a region that is not the unit `ast` names, and an edit to that unit passes without DRIFTED (executed by that round's reviewer). Round 3 of A then established that a markdown anchor is not shifted, and that a character at a line end or on a blank line moves no hash because `normalise` drops it; #664's comment carries both. Every hash-side and anchor-span split in `evidence_check.py` moves to the line ends `ast` and GFM use (`gfm_lines`, which A added), and `gfm_lines`' docstring, which A's run ended capped with two false sentences in, is rewritten to say what is true after the move. Then the class outside the checker is enumerated and each reader moved or recorded out with a reason: `correction_check.py#rows`, `round_record.py`'s report copy (which turned a U+2028 in a round report into a line break), `survivor_check`, `fold_check`, `hooks/config.py`, `gather_changelog`. | (1) The form-feed case through a `.py` anchor, **seen red** at `56e53c90`: an edit to the unit below the character reads DRIFTED. (2) `bin/evidence-check .` over this tree: no row's hash moves (none of the eight characters sits mid-line in a tracked anchored region). (3) One mutant per changed call site. (4) `bin/test` over the checker's modules and each moved reader's. | 3dd2cbfd |

Nothing broad runs in any phase (`agent-contract` §2). The suite, lint and
typecheck are the sealer's, once, after review.

## Operational impact

- **A consuming repository's build can go red at upgrade.** A stale backticked
  name in its `seal/follow-up.md`, or a wrong `path#name` in a live work
  item's records, is now `NOT-IN-TREE`: exit 2 in every reader, including
  CI's lenient `ledger` job and `--strict` in `broad-gate`. The repair is to
  correct the row or write `NAME NOT IN TREE` on its line. `changelog.md`
  says so first, because this is why the release is a minor one.
- **Vendored CI** (`tools/evidence_check.py`, from `evidence-ci`) picks this
  up only when it is vendored again. The template comment says what the
  records arm reads (D2).
- **`--reverify` prints more** (the naming block), and its exit codes are
  unchanged without the flag. A script that greps `N rows re-verified` still
  finds it.
- No migration, no new dependency, no environment variable. Python floor
  unchanged.
