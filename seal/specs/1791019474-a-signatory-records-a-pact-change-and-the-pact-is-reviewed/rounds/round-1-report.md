# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — round 1 report

Reviewer: `specseal:warden on claude-opus-5-5`. Target: `31910204` on
`feat/647-a-signatory-records-a-pact-change-and-the-pact-is-reviewed`, base
`2b1dcb1f` (the branch carries the merge of the release branch at `9511f6cd`,
made at `dae83db3`). First round; no earlier `round-N.md` exists, so the
account (`overview.md`, the phase records, the commit messages, the spawn
prompt) was the only other voice, and every claim in it below was checked
against the code.

Every probe ran in the round's scratch clone (`git clone --no-local` of the
worktree at `31910204`), with a `uv` venv carrying `cmarkgfm==2025.10.22` and
the suite's other pins. Nothing was written in the worktree except this file.

## How the findings relate

The writer (step C) and the reader (step D) are each sound on the paths the
spec's scenarios name, and the five pact modules are green (777 cases). The
findings sit one step past those scenarios:

1. **A pact change the writer cannot record is lost for good** (🔴 1). The
   ledger is re-stamped before the record is attempted, so every `LEFT` path
   of the writer — and one silent path — erases the very drift that would
   have triggered it on the next run. The remedy the `LEFT` line prints
   cannot work.
2. **Once written, a record can grow without a new change** (🟡 2): a BROKEN
   coordinate is recorded again, and a coordinate holding `\|` is recorded
   again on every run. Each growth changes the content hash, which is the
   key a pact review took the record by.
3. **The reader re-judges a historical pact review against the present**
   (🟡 3, and ⬜ 7 in the same class): an `amended` that was true at the hash
   it took is refused at exit 2 forever once the record grows.
4. **The two acceptance properties that are stated as closed by
   construction are not**: the anchor grammar passes three one-mark typos
   (🟡 4), and the walker reads tables cmark-gfm does not render (🟡 5) and
   splits a cell cmark-gfm does not (⬜ 6).

## Findings from execution

### 🔴 1 — An owed pact change that cannot be recorded is lost: the ledger is re-stamped first, and the printed remedy finds nothing to record

`skills/evidence-check/scripts/evidence_check.py:4728` and `:4749` (where
`main` calls `record_pact_changes` after `reverify` has already written the
ledger), with the four exits of `record_pact_changes` at `:3477`.

`main` runs `reverify` (or `reverify` then `reverify_into`), which writes the
new hashes into the ledger, and only then calls `record_pact_changes`. Every
path on which the writer declines to record returns 1 after that write:

| Path | What it prints | Exit |
|---|---|---|
| no `--into`, and no `routing.md` declares the branch | `LEFT … a pact change is owed and no work item names its record: name the work item with --into …, or run it on a branch a … routing.md declares` | 1 |
| a vendored copy (no `hooks/` beside it) | `LEFT … no pact change was recorded; run the plugin's evidence-check --reverify where the signatory is checked out` | 1 |
| the record exists and will not read | `LEFT … the record could not be read — nothing recorded` | 1 |
| the record exists and will not parse (an empty file included) | `LEFT … restore it from its history` | 1 |
| the signatory's `Pact` row will not parse, or `seal/config.md` is not UTF-8 | nothing at all | **0** |

The last row is the silent member of the same class: `declared_pacts`
returns refusals (or None), the writer reads that as "no pact declared"
(`:3526`, `or ([], None, [])`, refusals discarded), records nothing and says
nothing, while the ledger row's hash has moved. `pact_declaration`'s own
docstring names this as the silence that reader exists to end.

Executed, each in a temporary signatory built as the build's cases build it:

- no work item: run 1 exits 1 with the `LEFT` line and the ledger
  re-stamped; run 2, following the printed remedy with
  `--into seal/ledger/<id>.md`, prints `0 rows re-verified` and exits 0. No
  record exists, and none ever will.
- vendored copy, then the plugin's own `--reverify --into`: the same, exit 0,
  nothing recorded.
- an empty record file: `LEFT … holds no … table … restore it from its
  history`; restoring it and re-running finds no drift.
- `| Pact | orders api |` (a space in the URL): exit 0, the ledger
  re-stamped, no record, no line naming the pact.
- `seal/config.md` holding one non-UTF-8 byte: the same.

Why it matters: this is the question the step exists to answer — whether a
drifted row citing a clause can go unrecorded — and the answer is yes, on
five paths. The pact's repository is never told; `pact-check` reads nothing
because nothing was written. An unattended session that sees exit 1 and
follows the printed remedy gets exit 0 and believes the change recorded.

`test_s9_with_no_work_item_nothing_is_recorded_and_the_row_is_left` and
`test_a_vendored_copy_says_it_recorded_nothing` both assert the re-stamp
(`f"@{new}" in ledger`), so the defect is pinned. `spec.md` item 5 says
*"The ledger is written exactly as before"*, and S9 says the undeclared run
*"records nothing, names the row on a LEFT line, and exits 1"*; neither
foresaw that the re-stamp is what erases the trigger. The spec's own
principle for the writer, *"a step somebody must remember is a step that
gets skipped"* (`docs/the-pact.md`), is what the `LEFT` remedy then asks of
the person.

The fix (fenced below, run in the clone): snapshot every file the run may
write, and put them back byte for byte whenever `record_pact_changes`
returns 1, so a run that cannot record re-stamps nothing and the drift
stays for the run that can. The silent row joins the class through a
refusal check that returns 1 when any moved row cites a pact and the
`Pact` rows will not read. With it applied in the clone, the left-then-into
sequence records one row, and the five modules fail only in the two cases
that pin the re-stamp. Each `LEFT` sentence then says *nothing was
re-stamped*, which makes its remedy true.

### 🟡 2 — A second run records a change again: per-row strings instead of per-coordinate, and the escaped form compared with the parsed one

`skills/evidence-check/scripts/evidence_check.py:3576` (`held`).

The idempotence key is `(Clause, Row, Code)` as one string triple. Two
shapes break it, both executed:

- **A row with one moved and one BROKEN coordinate.** Run 1 records
  `` `…#serialize@57f678c6` → `@7069baf7`, `…#evict@9ce55934` BROKEN ``. Run 2 has
  no move left, only the BROKEN, so its `Code` is `` `…#evict@9ce55934` BROKEN ``,
  which is a different string. A second row is appended for the same BROKEN
  coordinate.
- **Any cell holding an escaped pipe.** The writer writes the ledger's raw
  text (`\|`) into `Code` and escapes `Row` itself, while the parsed rows it
  compares against come back through `table_cells`, which reduces `\|` to
  `|`. A BROKEN coordinate `` docs/x.md#"## A \| B"@… `` was appended on each of
  three runs; a row labelled `O2 \| B` likewise. Coordinates of exactly that
  shape stand in this repository's own ledger today (three minor anchors
  quoting `| Field | Value |` table lines), so a signatory citing a clause
  beside one is a real configuration.

Why it matters: `spec.md` item 5 says *"Running it twice records nothing
twice"*, and `docs/the-pact.md` says the same. Every appended row changes
the record's content hash, and the content hash is the key a pact review
took the record by: a record a pact review took reads `NOT TAKEN` again
after nothing but a re-run of `--reverify` — which a session runs again
precisely because a BROKEN coordinate keeps reporting.

The fix (fenced below, run in the clone) keys the held set per coordinate,
parsed out of each existing `Code` cell, and compares in the reader's form
(`unescaped`). With it, both shapes record once.

### 🟡 3 — A pact review's `amended`, true when written, is refused at exit 2 once its record grows, and stays refused after a new review takes the record

`skills/evidence-check/scripts/pact_check.py:823`.

The `amended` check walks every review row that names the item, whatever
hash it took, and tests it against every clause the record cites now.
Executed with the build's own fixture: the record cites the clause at v1,
the pact amends it to v2, and a pact review takes the record `amended` at
its hash (accepted; the build's
`test_s16_amended_is_taken_where_the_clause_moved` is this state). The
signatory then records a second change citing the clause at v2, the
current one. A second review row takes the grown record at its new hash with
`holds`. `pact-check` now exits 2:

```
REFUSED seal/pact-reviews/1791030000-the-pact-review.md:5 — the pact review says `amended` for work item 1791020000-a-field-is-added from https://example.com/org/orders-web, and the clause pact:orders-api/"## Order response shape / ### Fields"@0610e631 still has the hash the record recorded: amend the clause, or say `holds`
```

The row it refuses was true: when it was written, the record held only the
v1 row, and the clause had been amended. The grown row it is judged against
did not exist yet. The only ways out are to rewrite a pact review's
historical verdict to `holds`, which is false, or delete it.

Why it matters: the pact's repository is stuck at exit 2 after doing exactly
what the orchestration section tells it to do (*"a record that gained rows
since reads `NOT TAKEN` again … takes a new row here"*).

The fix (fenced below, run in the clone) judges `amended` only for a review
at the record's current hash: an older review took a record this one has
since added to. ⬜ 7 is the same class for the `Signatory` side.

### 🟡 4 — `.`, `-` or `_` in place of the `/` passes silently: the name pattern swallows the mark, inside the grammar's own "one mark"

`skills/evidence-check/scripts/pact_check.py:611` (with `PACT_MENTION_RE` at
`:210`).

The stated grammar (`docs/the-pact.md` §*The pact anchor*, and the code
comment) refuses the rest of an anchor with its `/` missing *"at once or
after one mark or one space"*. The four shapes round 3 of #735 named are
refused at exit 2, and the mentions round 2 kept are left alone (both
executed). But the name class is `[A-Za-z0-9_.-]+`, so when the mark is `.`,
`-` or `_` it becomes part of the name: `pact:orders-api."## …"@1a2b3c4d`
matches with the name `orders-api.`, and the loop at `:611` skips it as
another pact's. Executed over the shapes in the table below, each the only
citation of a ledger row:

| Shape | Read |
|---|---|
| the four of round 3 (no slash, `:`, a space, no heading path) | refused |
| `.`, `-` or `_` for the `/` | **silent** |
| `.` then `@<hash>` | **silent** |
| `\` for the `/`; `:` and a space; a slash with a space before `@` | refused |
| two spaces, two marks, a space before `@` | silent, and outside the stated rule |
| a sentence's end, a comma, a code span, the placeholder | silent, as intended |

The same swallowing hides `pact:orders-api-/"## …"@<hash>` (a mark *before* a
slash): it is a whole anchor naming `orders-api-`, and the mention loop
skips everything inside a graded span whatever pact it names.

Why it matters: 🟡 19 was this exact defect, a likely typo graded by nobody
at exit 0, and the fix is stated as closing it by a rule that these three
shapes satisfy.

The fix (fenced below, run in the clone, the three marks red at the target
and exit 2 with it) treats a name that is this pact's plus one trailing
`.`, `-` or `_` as this pact's attempt, in both loops. The shapes outside the
stated rule stay mentions; that is the rule as written.

### 🟡 5 — The walker reads tables cmark-gfm does not render, in shapes the corpus does not reach

`hooks/config.py:1044` (`gfm_table`'s line-above check) and `:942`
(`absorbs_a_header`). · NAME NOT IN TREE

S1 says *"No shape yields cells cmark-gfm does not"*, and `gfm_table`'s
docstring says it *"reads what cmark-gfm renders, or refuses"*. The build's
corpus puts one kind at a time at each position. An independent generator
— random documents of 2–9 lines from a vocabulary of 60 line kinds, three
headers, 300,000 documents — found two mechanisms by which the walker reads
a table, with no refusal, where cmark-gfm renders none:

- **A line directly above the header that `absorbs_a_header` reads wrong.** · NAME NOT IN TREE
  Measured shapes: a table directly above (`| Name |`, `|---|`, `| x |`, then
  the header — cmark-gfm reads the header as a row of the first table);
  `Intro`, `-`, `2. second` (the `-` is a setext underline, so `2.` opens a
  list whose paragraph takes the header lazily; the walker reads `-` as an
  empty list item and `2.` as more paragraph); `1) one`, `<a>`, `___`, `>`
  (after a list item a seventh-kind tag does start an HTML block, so the
  header is inside it); paragraph lines holding pipes that cmark-gfm's
  multi-line header scan rejects (`\| escaped`, `|---|---|`). 219 of 20,000
  documents at the first pass.
- **An HTML block of kinds 1–5 left open above, across a blank line.**
  `&lt;!--` with no `-->`, `<pre>`, `<?php`: no blank line ends these, so
  everything under them is raw text and GitHub shows nothing. `unfenced`
  hides only a comment block that closes, and the walker's look upward stops
  at the first blank line. Executed through `pact_signatories`:

  ```
  # Pact
  
  &lt;!-- old list, being retired
  
  | Signatory |
  |---|
  | https://example.com/org/a |
  ```

  reads one signatory and no refusal; cmark-gfm renders no table.

Why it matters: S1 is the spec's acceptance criterion for item 1 and the
reason the corpus exists. The rows read are text the author typed, so this
is not 🟡 18's silent drop; it is the opposite direction, a pact read as
listing signatories the rendered page does not show. The commented-out case
is the plausible one: a person retiring a list, who forgot the close.

The fix (fenced below, run in the clone): refuse any non-blank line directly
above the header (*leave a blank line above the header* is already the
remedy the walker prints), which closes the first mechanism by construction
rather than by mirroring more of cmark-gfm's block parser, and deletes
`absorbs_a_header`; and refuse a header under an open kind 1–5 block. Re-run · NAME NOT IN TREE
over 300,000 documents, the disagreements fall from 315 to 15, every one a
fence `unfenced` hides that cmark-gfm reads inside an HTML block — a
property of `unfenced`, shared with `config_rows`, and named below as the
remaining limit. The fix turns red the build's
`test_a_line_above_the_header_is_refused_only_where_gfm_renders_no_table`, · NAME NOT IN TREE
which pins the opposite choice (refuse only where GFM renders no table),
and the one pinned sentence in `tests/test_a_signatory_declares_its_pact.py`.
The trade is stated plainly: a pact written with a paragraph directly over
its `Signatory` header, which GitHub does render, is refused with the
blank-line remedy. Every template and the writer already leave that blank
line.

### ⬜ 6 — A cell is split at `\\|`, where cmark-gfm does not split

`hooks/config.py:893` (`CELL_PIPE`, through `CELL`).

`CELL` reads `\\` as one escape and then splits at the `|`; cmark-gfm's cell
scanner treats `\|` as an escaped pipe wherever it stands, so `\\|` does not
split there. Executed: `| a \\| b | c | 2026-10-04 |` under the four-column
header reads `('a \\', 'b', 'c', '2026-10-04')` with no refusal, and
cmark-gfm renders `('a | b', 'c', '2026-10-04', '')`. A row of three real
cells reads as four, silently. The corpus leaves cell content out by design,
so nothing covered it. Only a backslash run of even length before a pipe
does this, which nothing the writer emits contains, so it is ⬜; the fenced
fix refuses such a row rather than guessing.

## Findings from reading

### ⬜ 7 — A pact review row naming a signatory the pact has since dropped is refused at exit 2 for good

`skills/evidence-check/scripts/pact_check.py:688`. A pact review record is
permanent (both READMEs' drawings say so), and a row naming a signatory the
`Signatory` table does not list is refused. So taking a signatory out of the
pact turns every historical pact review row naming it into an exit 2 that
can only be cleared by editing a permanent record. A typo and a departed
signatory are the same text, so the refusal itself is right; what is missing
is the sentence. Same class as 🟡 3, a historical row judged against the
present. The fenced fix states it in §*What this does not see*.

### ⬜ 8 — A pact review takes a whole record, so a mixed record can only be taken with a verdict that is false for part of it

`skills/evidence-check/scripts/pact_check.py:823` and
`skills/evidence-check/scripts/evidence_check.py:3477`. The record is per
work item and the verdict per record. A record citing two clauses, one the
pact amended and one it kept, is refused as `amended` (a cited clause is
unmoved) and accepted only as `holds`, which is false for the amended one.
The same granularity makes a record's rows that are not this pact's re-open
this pact's taken rows: under `always` every drift appends a `—` row, and a
signatory of two pacts appends rows citing the other, and each changes the
hash this pact's review took. `spec.md` item 9 states the `amended` refusal
as written (*"a clause the taken record cites"*), so the code follows its
spec; the frame decided the granularity in `questions.md` Q5 without
weighing either consequence. Reported for the record and a sentence, not as
a defect of the build.

### ⬜ 9 — The fragment's `Re-read · P1-1` says the claim holds, while its subject is no longer the suite's only test-only parser (paperwork)

`seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md`,
the row `Re-read · P1-1`. The released claim opens *"the suite's test-only
parser is markdown-it-py"*; this branch's own W2 pins `cmarkgfm` as a second
test-only package beside it. Every operative part of the claim still holds,
so this is a `Corrected` note on the re-read row rather than a new claim.
A correction to the run's paperwork, not counted in `Needs a fix`.

## What was checked and stands

- **Tab indentation.** cmark-gfm 2025.10.22 ends the table at a row indented
  by a tab (an indented code block) and renders no table for a tab before the
  header or the delimiter; the walker ends the table and refuses the row as
  unread. Round 3's ⬜ 22 sentence does not reproduce at this version, as
  `overview.md` says. Executed.
- **A row of another width.** cmark-gfm pads a short row and drops a long
  row's extra cells; the walker refuses both, loud, with the cause. S1
  permits a refusal, and `overview.md` records the divergence with grounds.
  Executed.
- **After the header, the walker ends where cmark-gfm ends.** Across the
  300,000 documents, with the line-above shapes set aside, the only
  body-side disagreement was ⬜ 6. P8's corrected claim, which is about where
  the table ends, holds.
- **Exit classes.** `NOT TAKEN` from a record exits 1, `NOTED` alone exits 0,
  every `REFUSED` and `UNREADABLE` exits 2, and `amended` over an unmoved
  clause is refused. Executed (probes and the module).
- **A review cannot keep a grown record taken.** The content hash covers the
  whole record through `gfm_lines`; only blank lines and trailing whitespace
  leave it unchanged. Read, and S15's case executed.
- **The wrong work item.** The id is `--into`'s file name or the single
  `routing.md` naming the checked-out branch; a detached HEAD and two
  declarations of one branch both give "" and a `LEFT`. No path picks
  another item. Read.
- **Windows.** An AST scan of every added line finds no `open`,
  `read_text` or `write_text` without `encoding=`; every path line in
  `pact_check.py` goes through `shown`, and the writer's through
  `built_name`. CI's three pytest legs at `31910204` installed
  `cmarkgfm==2025.10.22` (the Windows leg's install step succeeded) and
  passed. Executed (scan) and read (CI).
- **The ledger.** Sampled against the code: the 0.8.3 `display_name` row
  (`built_name` calls `display_name`, holds), 0.16.0's R2 (a BROKEN-only
  ledger is not rewritten — `kept` is empty, so nothing is written; holds),
  0.16.0's H1, 0.13.1's O1 (the new act has its row; holds), P8's
  correction. Only ⬜ 9 needs a note. #743's overlap on L4 is the known merge
  the prompt names and is not reported.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | An owed pact change that cannot be recorded is lost: the ledger is re-stamped before the record is attempted, so the four `LEFT` paths (no work item, vendored copy, record unreadable, record unparseable) and the silent one (a `Pact` row or config that will not read, exit 0) erase the drift, and the printed remedy finds nothing to record | `skills/evidence-check/scripts/evidence_check.py:4728` | open | executed: no-work-item then `--into` records nothing (exit 0); vendored then plugin the same; empty record; unparseable `Pact` row and non-UTF-8 config exit 0 with no record. Fix run in the clone: left-then-into records one row |
| 🟡 2 | A second run records a change again: a BROKEN coordinate beside a moved one, and any coordinate or label holding `\|`, on every run, each changing the hash a pact review took | `skills/evidence-check/scripts/evidence_check.py:3576` | open | executed: two rows after two runs; three rows after three runs with `\|`. Fix run in the clone: one row |
| 🟡 3 | An `amended` pact review, true at the hash it took, is refused at exit 2 once the record grows, and stays refused after a new `holds` review takes the grown record | `skills/evidence-check/scripts/pact_check.py:823` | open | executed with the build's fixture: exit 2. Fix run in the clone: no refusal |
| 🟡 4 | `.`, `-` or `_` in place of the `/` (and before it) passes silently, inside the grammar's own "one mark" | `skills/evidence-check/scripts/pact_check.py:611` | open | executed over 21 shapes: the four of round 3 refused, these silent. Fix run in the clone: exit 2 |
| 🟡 5 | The walker reads tables cmark-gfm does not render: a line above the header `absorbs_a_header` misjudges, and an HTML block of kinds 1–5 left open above a blank line | `hooks/config.py:1044` | open | executed: 300,000 random documents, 315 disagreements; with the fix, 15, all a fence inside an HTML block | · NAME NOT IN TREE
| ⬜ 6 | A cell is split at a pipe after two backslashes, where cmark-gfm does not split; a three-cell row reads as four, silently | `hooks/config.py:893` | open | executed against cmarkgfm |
| ⬜ 7 | A pact review row naming a dropped signatory is refused at exit 2 for good, and no document says so | `skills/evidence-check/scripts/pact_check.py:688` | open | read |
| ⬜ 8 | A pact review takes a whole record: a mixed record can only be taken as `holds`, and rows that are not this pact's re-open its taken rows | `skills/evidence-check/scripts/pact_check.py:823` | open | read; the code follows `spec.md` item 9 |
| ⬜ 9 | `Re-read · P1-1` says the claim holds while *"the suite's test-only parser"* is now one of two | `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md` | open | read; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | Round 3 of #735's 🟡 19 four shapes are refused at exit 2 and round 2's mentions stay exit 0 | `skills/evidence-check/scripts/pact_check.py:210` | confirmed | executed |
| 🟢 | Tab before a row, header or delimiter: the walker follows cmark-gfm 2025.10.22; a row of another width is refused loud, the recorded divergence | `hooks/config.py:993` | confirmed | executed against cmarkgfm |
| 🟢 | `NOT TAKEN` exit 1, `NOTED` exit 0, `REFUSED` and `UNREADABLE` exit 2; `amended` over an unmoved clause refused; a grown record reads `NOT TAKEN` again with both hashes | `skills/evidence-check/scripts/pact_check.py:726` | confirmed | executed: probes and the module |
| 🟢 | Every added file read and write names its encoding; every printed path goes through `shown` or `built_name`; `cmarkgfm` installs from a wheel on CI's three legs | `skills/evidence-check/scripts/pact_check.py:116` | confirmed | executed (AST scan); read (CI run at `31910204`, three pytest legs green) |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `31910204` | ❓ out of verified scope | the broad gate is the sealer's, once the rounds settle; the smith handed it over labelled `unverified`, and that label is honest |

## Executed probes

| What was run | Result |
|---|---|
| The five pact modules (`test_one_table_walker_reads_what_gfm_renders`, `test_a_pact_review_takes_a_pact_change`, `test_a_signatory_records_a_pact_change`, `test_pact_check`, `test_a_signatory_declares_its_pact`) at `31910204` | 777 passed |
| An independent random-document generator, walker against `cmarkgfm`, 20,000 then 300,000 documents | 219 then 315 tables read that cmark-gfm does not render (two mechanisms, 🟡 5); body side: only ⬜ 6 |
| Targeted walker shapes through `gfm_table` and `pact_signatories` | unclosed comment and `<pre>` above, table above, setext `-` read with no refusal; a pipe after two backslashes splits; tab, width, NBSP refused |
| Writer sequences in temporary signatories (no work item then `--into`; vendored then plugin; BROKEN beside a move, twice; `\|` coordinate and label, three runs; unparseable `Pact` row; non-UTF-8 config; empty record) | 🔴 1 and 🟡 2 reproduced as described |
| `amended` at v1, record grown with a v2 row, a new `holds` review | exit 2, 🟡 3 |
| 21 anchor shapes through `PACT_MENTION_RE` and `PACT_ANCHOR_RE` as `pact-check` filters them | 🟡 4 table |
| The paste-ready fixes for 🔴 1, 🟡 2, 🟡 3, 🟡 4 and 🟡 5 applied together in the clone, the probes and the five modules re-run, then the clone reverted | probes inverted (each defect gone); 771 passed, 6 failed — exactly the six cases that pin the old behaviour, each named in the fixes below |
| An AST scan of every added line for file I/O without `encoding=` | none |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

## Paste-ready fixes

### 🔴 1 — `skills/evidence-check/scripts/evidence_check.py`

Beside `record_pact_changes`, two helpers:

```python
def snapshot(paths):
    """{path: its bytes, or None where it is absent} for each of PATHS."""
    out = {}
    for path in paths:
        try:
            with open(path, "rb") as handle:
                out[path] = handle.read()
        except OSError:
            out[path] = None
    return out


def restore(before):
    """Put each file BEFORE holds back as it was, byte for byte, through a
    rename beside the real file as `write_atomic` does; remove one that was
    absent and now exists."""
    for path, data in before.items():
        if data is None:
            if os.path.isfile(path):
                os.remove(path)
            continue
        target = os.path.realpath(path)
        fd, tmp = tempfile.mkstemp(
            dir=os.path.dirname(target) or ".", prefix=os.path.basename(target) + "."
        )
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        try:
            os.chmod(tmp, stat.S_IMODE(os.stat(target).st_mode))
        except OSError:
            pass
        os.replace(tmp, target)
```

In `main`'s reverify branch:

```python
        # What the re-read moved, for the pact changes it owes (#647, C).
        moves = []
        # Every file this run may write, as it stands: put back where a pact
        # change is owed and cannot be recorded, because the re-stamp is what
        # clears the drift, and a re-stamp without its record loses the
        # trigger for good -- the next run finds nothing moved.
        before = snapshot(ledgers + ([into] if into else []))
        if into is None and cutoff is None:
            ...
            recorded = record_pact_changes(moves, root, into, args.checked)
            if recorded:
                restore(before)
            return max(code, 1 if owed else 0, recorded)
        ...
        recorded = record_pact_changes(moves, root, into, args.checked)
        if recorded:
            restore(before)
        return max(code, written, recorded)
```

In `record_pact_changes`, replace the `declared` line with a refusal check
that joins the silent path to the class:

```python
    declared = config.declared_pacts(seal_home(root))
    refused = (
        ["seal/config.md could not be read"] if declared is None else declared[2]
    )
    if refused and any(e[3] for e in entries):
        for where, _row, _parts, _anchors in (e for e in entries if e[3]):
            print(
                f"  LEFT  {where}  cites a pact clause, and the `Pact` rows will "
                f"not read: {refused[0]} — no pact change was recorded and "
                "nothing was re-stamped; fix the row and run it again"
            )
        return 1
    declared = declared or ([], None, [])
    pacts, notify = declared[0], declared[1] or config.NOTIFY_DEFAULT
```

and end each of the other four `LEFT` sentences with *— no pact change was
recorded and nothing was re-stamped* (the record-unreadable and
record-unparseable sentences: replace *nothing recorded* with it; the
vendored sentence: replace *no pact change was recorded* with it). Every
return of 1 in the function is an owed change left, which is what lets
`main` restore on `recorded` alone; keep it that way.

`tests/test_a_signatory_records_a_pact_change.py`: in
`test_s9_with_no_work_item_nothing_is_recorded_and_the_row_is_left` and
`test_a_vendored_copy_says_it_recorded_nothing`, replace
`assert f"@{new}" in ledger.read_text(encoding="utf-8")` with the bytes
check, keep the rows list in a variable, and update the pinned sentence:

```python
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
```

and add:

```python
def test_a_change_left_is_recorded_by_the_remedy_it_names(repo):
    """The run that cannot name a work item re-stamps nothing, so the drift
    is still there for the run its LEFT line names (round 1, red 1)."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    new = move_serialize(repo)
    code, out = run(repo, "--checked", "2026-09-04")
    assert code == 1 and "nothing was re-stamped" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `src/orders.py#serialize@{old}` "
        f"→ `@{new}` | 2026-09-04 |"
    ], out


@pytest.mark.parametrize(
    "config_bytes",
    [
        b"| Item | Value |\n|---|---|\n| Pact | orders api |\n",
        b"| Item | Value |\n|---|---|\n| Pact | git@example.com:org/orders-api.git |\n"
        b"| Note | caf\xe9 |\n",
    ],
    ids=["a Pact row that will not parse", "a config that is not UTF-8"],
)
def test_a_pact_row_that_will_not_read_leaves_the_row(repo, config_bytes):
    (repo / "seal" / "config.md").write_bytes(config_bytes)
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "the `Pact` rows will not read" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
```

The two `docs/the-pact.md` statements (§*A signatory records a pact change*:
*"with neither, nothing is recorded, the row is named on a `LEFT` line …"*,
and *"The ledger is written exactly as it would be without the record"*)
take one clause each: where a change is owed and cannot be recorded, nothing
is re-stamped either. The same sentence goes in
`skills/evidence-check/SKILL.md` (*"The ledger is written exactly as before
in every case"*).

### 🟡 2 — `skills/evidence-check/scripts/evidence_check.py`

Beside `PACT_CHANGE_REPAIR`:

```python
# One coordinate of a record's `Code` cell, as `record_pact_changes` writes
# it: moved to a new hash, or BROKEN.
CODE_PART = re.compile(
    r"`(?P<coord>[^`]*)@(?P<old>[0-9a-f]{6,12})`"
    r"(?: → `@(?P<new>[0-9a-f]{6,12})`| BROKEN)"
)
```

In `record_pact_changes`, keep the coordinates rather than a rendered
string when building `entries`:

```python
        parts = list(dict.fromkeys(coords))
        where = f"{built_name(ledger, root)}:{number}"
        row = f"{built_name(ledger, root)} · {label or number}".replace("|", "\\|")
        entries.append((where, row, parts, list(PACT_ANCHOR_RE.finditer(line))))
```

(the `owed` loop passes `parts` through where it passed `code`), and replace
the `held` block:

```python
    # Held per coordinate and compared as the reader reads a cell (`\|` a
    # pipe), so a row is not recorded again because one of its coordinates
    # was recorded with another, or because its text holds an escaped pipe.
    held = {
        (clause, row, *part.group("coord", "old", "new"))
        for _l, clause, row, code, _c in rows
        for part in CODE_PART.finditer(code)
    }
    date = checked or datetime.date.today().isoformat()
    new = []
    for where, clause, row, parts in owed:
        key = (config.unescaped(clause), config.unescaped(row))
        fresh = [
            (coord, old, nw)
            for coord, old, nw in parts
            if (*key, config.unescaped(coord), old, nw) not in held
        ]
        if not fresh:
            continue
        held.update((*key, config.unescaped(c), o, n) for c, o, n in fresh)
        code = ", ".join(
            f"`{coord}@{old}` → `@{nw}`" if nw else f"`{coord}@{old}` BROKEN"
            for coord, old, nw in fresh
        )
        new.append((where, f"| {clause} | {row} | {code} | {date} |"))
```

`tests/test_a_signatory_records_a_pact_change.py`:

```python
def test_a_broken_coordinate_beside_a_moved_one_is_recorded_once(repo):
    s = unit_hash(repo, "src/orders.py", "serialize")
    e = unit_hash(repo, "src/orders.py", "evict")
    cite(repo, [
        f"| O1 · x | `{CLAUSE}`, `src/orders.py#serialize@{s}`, "
        f"`src/orders.py#evict@{e}` | read | 2026-10-01 | |\n"
    ])
    src = SOURCE.replace("'id': order.id", "'id': order.id, 'tax': 0")
    (repo / "src" / "orders.py").write_text(
        src.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    first = (repo / RECORD).read_text(encoding="utf-8")
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert (repo / RECORD).read_text(encoding="utf-8") == first, out


def test_a_coordinate_holding_an_escaped_pipe_is_recorded_once(repo):
    doc = repo / "docs" / "x.md"
    doc.parent.mkdir()
    doc.write_text("# T\n\n## A | B\n\ntext one\n", encoding="utf-8")
    h = unit_hash(repo, "docs/x.md", '"## A \\| B"')
    cite(repo, [
        f"| O1 \\| x · y | `{CLAUSE}`, `docs/x.md#\"## A \\| B\"@{h}` "
        "| read | 2026-10-01 | |\n"
    ])
    doc.write_text("# T\n", encoding="utf-8")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert len(record_rows(repo)) == 1
```

### 🟡 3 — `skills/evidence-check/scripts/pact_check.py`

```python
        for review in reviewed:
            # Judged against the record it takes, and only that one: a review
            # at an older hash took rows this record has since added to, and
            # re-judging its verdict against them refuses one that was true.
            if review[5] != config.VERDICT_AMENDED or review[4] != digest:
                continue
```

`tests/test_a_pact_review_takes_a_pact_change.py`:

```python
def test_an_amended_review_at_an_older_hash_is_not_judged_again(world):
    """An `amended` that was true at the hash it took stays true after the
    record grows with a row citing the amended clause (round 1, yellow 3)."""
    _anchor, first = record(world, cites=V1)
    _anchor, now = record(world, cites=V2, label="O2", step=2)
    review(
        world,
        (SIGNATORY_URL, f"{ITEM}@{first}", "amended"),
        (SIGNATORY_URL, f"{ITEM}@{now}", "holds"),
    )
    code, out = run(world)
    assert "REFUSED" not in out, out
    assert "2 pact changes read, 2 taken" in out, out
```

`docs/the-pact.md` §*A pact review takes a pact change* (second statement)
and `templates/pact-review.md`: *"and `amended` where a clause the record
cites still has the hash the record recorded"* becomes *"and `amended`, at
the record's current hash, where a clause it cites still has the hash the
record recorded"*.

### 🟡 4 — `skills/evidence-check/scripts/pact_check.py`

Beside `load`:

```python
def near_miss(said, name):
    """True where SAID is NAME and one more mark the name class holds -- a
    `.`, `-` or `_` -- standing where an anchor's `/` went missing, as in
    `pact:orders-api."## A"@1a2b3c4d`: the name pattern takes the mark
    in, so without this the token names another pact and nobody reads it."""
    said = said.lower()
    return len(said) == len(name) + 1 and said.startswith(name) and said[-1] in "._-"
```

and in `check`:

```python
            graded = [
                m.span()
                for m in checker.PACT_ANCHOR_RE.finditer(view)
                if not near_miss(m.group("name"), name)
            ]
            for near in PACT_MENTION_RE.finditer(view):
                inside = any(s <= near.start() < e for s, e in graded)
                said = near.group("name")
                if not (said.lower() == name or near_miss(said, name)) or inside:
                    continue
```

`tests/test_pact_check.py`, beside `test_an_anchor_missing_its_slash_is_refused`:

```python
@pytest.mark.parametrize(
    "shape",
    [
        "pact:orders-api.{loc}@{h}",
        "pact:orders-api-{loc}@{h}",
        "pact:orders-api_{loc}@{h}",
        "pact:orders-api.@{h}",
        "pact:orders-api-/{loc}@{h}",
    ],
    ids=["a dot", "a hyphen", "an underscore", "a dot, no heading path", "a mark before the slash"],
)
def test_a_mark_the_name_holds_is_not_a_second_name(world, shape):
    """`.`, `-` and `_` are marks the grammar's "one mark" covers and the
    name pattern also takes in (round 1, yellow 4)."""
    anchor = shape.format(loc=LOCATOR, h=clause(V2))
    write(world["web"], "seal/ledger/1790000000-x.md", ledger_row(anchor))
    code, out = run(world)
    assert code == 2, out
    assert "does not parse" in out, out
```

`docs/the-pact.md` §*The pact anchor*: after *"at once or after one mark or
one space"*, add *"— a `.`, `-` or `_` included, which the name itself could
otherwise hold"*.

### 🟡 5 — `hooks/config.py`

Beside `gfm_table`:

```python
def raw_html_open(lines):
    """True where an HTML block of CommonMark 4.6's kinds 1-5 -- the kinds no
    blank line ends -- is still open after LINES, so everything under it is
    the block's raw text and GFM renders no table there."""
    end = None
    for line in lines:
        if end is not None:
            if end.search(line):
                end = None
            continue
        if blocks.columns(line) >= 4:
            continue
        content = line.lstrip(" ")
        number, closer = html_start(content)
        if number is not None and number <= 5 and not closer.search(content, 1):
            end = closer
    return end is not None
```

In `gfm_table`, replace the `top` loop, `run` and the `absorbs_a_header` · NAME NOT IN TREE
refusal with:

```python
    above = shown[at - 1] if at > 0 else None
    if above is not None and above[0] == head_index - 1 and above[1].strip():
        return [], [
            f"has a `| {name} |` header directly under `{above[1].strip()}`, "
            "and GFM renders a table under a line only in some of the shapes "
            "that line can take — leave a blank line above the header"
        ]
    if raw_html_open([line for _i, line in shown[:at]]):
        return [], [
            f"has a `| {name} |` header inside an HTML block opened above it "
            "and never closed, so GFM renders no table there — close the block"
        ]
```

delete `absorbs_a_header`, and in `gfm_table`'s docstring replace the · NAME NOT IN TREE
paragraph on `absorbs_a_header` with: *A header with a line directly above · NAME NOT IN TREE
it is refused, because whether GFM renders a table there depends on block
state no reader here tracks, and so is a header under an HTML block of
kinds 1-5 left open. **What this cannot see** is a fence `unfenced` hides
that GFM reads inside an HTML block, and a header taken lazily into a list
item two blocks up.*

`tests/test_one_table_walker_reads_what_gfm_renders.py`: replace
`test_a_line_above_the_header_is_refused_only_where_gfm_renders_no_table` · NAME NOT IN TREE
(it pins the choice this fix reverses) with:

```python
@pytest.mark.parametrize("which", sorted(HEADERS))
def test_a_line_directly_above_the_header_is_refused(which):
    """Whether cmark-gfm renders a table under a line depends on the block
    state above it, which the walker does not track, so any non-blank line
    directly above a header is refused with the blank-line remedy
    (round 1, yellow 5)."""
    header = HEADERS[which]
    for kind, lines in KINDS.items():
        if not any(line.strip() for line in lines):
            continue
        text = document(header, lines, "before the header", "")
        rows, refusals = config.gfm_table(text, header)
        assert refusals and "blank line above the header" in refusals[0], kind


def test_the_shapes_round_1_measured_are_refused():
    u = "https://example.com/org/a"
    opener = "<" + "!-- old list, being retired"
    for text in (
        f"| Name |\n|---|\n| x |\n| Signatory |\n|---|\n| {u} |\n",
        f"Intro\n-\n2. second\n| Signatory |\n|---|\n| {u} |\n",
        f"1) one\n<a>\n___\n>\n| Signatory |\n|---|\n| {u} |\n",
        f"# Pact\n\n{opener}\n\n| Signatory |\n|---|\n| {u} |\n",
        f"<pre>\nexample\n\n| Signatory |\n|---|\n| {u} |\n",
    ):
        assert oracle.rows_under(text, ("Signatory",)) is None, text
        rows, refusals = config.gfm_table(text, ("Signatory",))
        assert refusals, text
```

`tests/test_a_signatory_declares_its_pact.py:340`, the pinned sentence:

```python
        "has a `| Signatory |` header directly under `- a note`, and GFM "
        "renders a table under a line only in some of the shapes that line "
        "can take — leave a blank line above the header",
```

### ⬜ 6 — `hooks/config.py`, `table_cells`

```python
# A pipe after an even run of backslashes: `CELL` splits there and cmark-gfm
# does not (its cell scanner reads `\|` as an escaped pipe wherever it stands).
EVEN_ESCAPED_PIPE = re.compile(r"(?<!\\)(?:\\\\)+\|")


def table_cells(line):
    """..."""
    match = TABLE_ROW.match(line)
    if not match or EVEN_ESCAPED_PIPE.search(line):
        return None
    ...
```

A row so written is then refused as *not a … row written `| … |`*, loud.

### ⬜ 7 — `docs/the-pact.md` §*What this does not see*

```markdown
A pact review row names a signatory by the URL the pact lists, so taking a
signatory out of the `Signatory` table refuses every pact review row that
names it, at exit 2: take those rows out with the signatory, in the same
change.
```

### ⬜ 8 — `docs/the-pact.md` §*A pact review takes a pact change*

```markdown
A pact review takes a whole record, one verdict for every row in it. A
record citing a clause the pact amended beside one it kept is taken as
`holds`, the amendment written in the pact itself; and a row that is not
this pact's -- a `—` row, or one citing another pact -- still changes the
record's hash, so a record this pact took reads `NOT TAKEN` again when one
is added.
```

### ⬜ 9 — the fragment row `Re-read · P1-1`, its Notes cell

```markdown
**Corrected 2026-10-03 by work item 1791019474:** the claim says *"the suite's test-only parser"*; since W2 `cmarkgfm` is a second test-only package beside it, pinned in `CMARKGFM`. Every operative part of the claim -- the pin, both build strategies, the adopted-environment step, the failure sentence, CI's and `CONTRIBUTING.md`'s strings -- still holds for markdown-it-py.
```

## Regression tests to plant

| Finding | Destination | Case |
|---|---|---|
| 🔴 1 | `tests/test_a_signatory_records_a_pact_change.py` | the left-then-remedy case and the two `Pact`-row ids, fenced above; the two existing cases' ledger assertions turned to the bytes check |
| 🟡 2 | `tests/test_a_signatory_records_a_pact_change.py` | the BROKEN-beside-a-move and escaped-pipe cases, fenced above |
| 🟡 3 | `tests/test_a_pact_review_takes_a_pact_change.py` | the older-hash `amended` case, fenced above |
| 🟡 4 | `tests/test_pact_check.py` | the five-id mark case, fenced above (the three marks were silent at `31910204`) |
| 🟡 5 | `tests/test_one_table_walker_reads_what_gfm_renders.py` | the line-above case replacing the over-refusal case, and the measured shapes, fenced above |
| ⬜ 6 | `tests/test_one_table_walker_reads_what_gfm_renders.py` | the row in ⬜ 6's prose (three cells, the first holding a pipe after two backslashes) under the four-column header: refused |

## Facts for the evidence ledger

- cmark-gfm 2025.10.22 does not split a cell at `\\|` (its cell scanner reads
  `\|` as an escaped pipe wherever it stands); `CELL` does. Measured this
  round; for the row that lands with ⬜ 6's fix.
- After a list item's paragraph, a line holding only a seventh-kind tag
  (`<a>`) starts an HTML block in cmark-gfm, though the same tag cannot
  interrupt a paragraph: the lazy-continuation position is not inside the
  paragraph's container. Measured this round; for whichever row records the
  walker's line-above rule.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A fence `unfenced` hides that cmark-gfm reads inside an HTML block (15 documents of 300,000 after 🟡 5's fix) | 🟡 5's docstring sentence names it as a limit; `unfenced` is shared with `config_rows` and older than this work item | the orchestrator, who decides whether it earns an issue |

Needs a fix: yes — 🔴 1 (an owed pact change that cannot be recorded is lost, the ledger re-stamped first), 🟡 2 (a second run records again), 🟡 3 (a true historical `amended` refused at exit 2), 🟡 4 (three one-mark typos silent), 🟡 5 (the walker reads tables cmark-gfm does not render)

Loses a record or crashes: yes — 🔴 1: a pact change owed by a drifted row citing a clause is never recorded on five paths, one of them at exit 0, and the re-stamp removes the drift that would record it later

## Proof block

Files opened this round:

- `seal/specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed/spec.md`, `questions.md`, `overview.md`
- `hooks/config.py` (the walker, the two record readers, `pact_declaration`, `declared_pacts`, `remote_entries`, `unfenced`, `CELL`, `unescaped`)
- `hooks/routing.py` (`item_dir`, `current_branch`)
- `skills/evidence-check/scripts/pact_check.py` (whole)
- `skills/evidence-check/scripts/evidence_check.py` (the branch's diff; `PACT_ANCHOR_RE`, `gfm_lines`, `unquoted`, `content_hash`, `read`, `write_atomic`, `seal_home`, `built_name`, the end of `reverify`, `main`'s reverify branch)
- `tests/gfm_table_oracle.py`, `tests/test_one_table_walker_reads_what_gfm_renders.py` (head, the over-refusal case), `tests/test_a_signatory_records_a_pact_change.py`, `tests/test_a_pact_review_takes_a_pact_change.py` (fixtures, S15–S17), `tests/test_a_signatory_declares_its_pact.py:330`, `tests/test_pact_check.py:624`, `tests/test_every_reader_ends_a_line_where_gfm_does.py` (the census diff), `tests/conftest.py` (`load_hook_module`)
- `docs/the-pact.md` (the diff), `templates/pact-review.md`, `templates/config.md` (the diff), `skills/implement/orchestration.md` (the diff), `skills/evidence-check/SKILL.md` and `README.md` (the diffs)
- `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md`; the fragment rows of `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md`, `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` and `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md` this branch touched; the released rows P1-1 and R2 (0.16.0), H1 (0.16.0), the `display_name` row (0.8.3), P1 (0.15.1)
- `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-3-report.md` (🟡 19, ⬜ 20–23, its paste-ready case)
- CI run 37121542972 at `31910204` (check states, the Windows leg's install step)

Executed: everything under *Executed probes*. Read: everything else in the
findings, labelled per row. Unverified: the full suite, the repository-wide
lint and the typecheck — the sealer's, after the rounds settle.
