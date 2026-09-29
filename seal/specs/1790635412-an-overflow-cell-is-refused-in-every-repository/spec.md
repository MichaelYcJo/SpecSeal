# Feature Specification: an overflow cell is refused in every repository

<!-- seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issue: #585. Milestone 49 (0.16.0), item A. The repository owner answered the
issue's question **(b), ship it**, in the batch before the first edit
(`routing.md` §*Why this way*). So the shipped `evidence-check` gains an arm
that refuses a ledger row with more cells than its table's header, and a
header-less fragment row is counted against the columns `templates/ledger.md`
declares. Today only this repository's own test refuses such a row, so a
repository that installs the plugin can hold a row whose overflow cell, and
any marker written there, no reader sees.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit*, the paragraph under 1790208643's marker that opens "**A `\|` inside a ledger cell is escaped, and a row with more cells than its table's header fails.**" | The rule already stands, and it says **more** cells. A row under no header is counted against the five columns `templates/ledger.md` declares, because a fragment has no header by rule and the fold copies it as it stands (#501). This work changes who enforces the rule, not the rule. The paragraph's last sentence and its `Enforced by:` line change to name the shipped arm (phase 3). |
| `docs/the-evidence-ledger.md` §*What the checker refuses, and what it says while refusing*, "One ledger, two readings, and the lenient one says so" | A run whose answer is exit 1 says that the strict reading would refuse this tree. A new verdict graded like `DRIFTED` is a new cause of exit 1, so the notice has to name it. |
| `skills/evidence-check/SKILL.md` §*Which reader graded your tree*, and the owner's answer of 2026-09-26 recorded there (work item 1790297087, `questions.md` Q1) | The grading for a row the checker cannot read as written is already decided for the sibling verdict: `MALFORMED` exits 1 on a lenient run and 2 under `--strict`. The reason given was that a repository's lenient run should not start refusing rows on update, while the readers that decide (`broad-gate` and the vendored CI template, both `--strict`) still refuse. That reason applies unchanged to this verdict, so it takes the same grading. |
| `skills/evidence-check/SKILL.md` §*Known limits*, "Every row the check calls `BROKEN`, `DRIFTED` or `MALFORMED` gets a line back from `--reverify` … Silence there reads as a heal that happened" | A new verdict joins that list, so `--reverify` names an overflowing row and leaves it. |
| `hooks/evidence-advisor.py` module docstring: "Three verdicts name something a person must touch either way and all three are printed" | An overflowing row is something a person must touch either way. It is not a branch mid-flight. So the advisor prints it, and the docstring's count moves. |
| `skills/verify/scripts/unverified_check.py#fence_opener` docstring: the one place the fence rule is written | The arm reads through `evidence_check.py`'s `unquoted`, which already asks that rule through `fence_rule` (and the vendored pair where the shared reader is absent). No new fence reading is written. |
| `CLAUDE.md` §*Repo rule — a change writes fragments*, and §*A row whose anchor a change removes is REMOVED* | Rows whose anchors this work removes are taken out of the release files they stand in. Their claims are written anew in `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md`. Rows this work drifts are re-read and re-stamped where they stand. The changelog entry goes to this directory's `changelog.md`. `plugin.json` and `CHANGELOG.md` are not touched. |
| `CLAUDE.md` §*Repo rule — a thing more than one party can have is named with whose*, and `tests/test_one_word_one_meaning.py` | One verdict word keeps one meaning. `MALFORMED` means a `Code grounds` cell nothing can check, and an overflowing row is a different defect with a different remedy. It gets its own word. |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `hooks/evidence-advisor.py` is a hook. The pull request states a case seen red, a failure direction and a prompt budget for it. |
| `CONTRIBUTING.md`: "Both READMEs move together" | The owner's answer asks for a README row. `README.md` and `README.ko.md` both change. |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Each gap is enumerated as a class. A changed sentence a person reads is pinned in the same commit. Every new case is seen red before it is committed. |

## Scope

### In

1. **The arm.** `skills/evidence-check/scripts/evidence_check.py` gains a
   verdict, **`OVERFLOW`**: a table row in a ledger file that splits into more
   cells than its table's header. A row under no header is counted against
   the ledger row's columns. The verdict is graded like `DRIFTED` and
   `MALFORMED`: exit 1 on a lenient run, exit 2 under `--strict`.
   - **Why a verdict of its own, and not `MALFORMED`.** Folding it in would
     make three shipped sentences false at once. The advisor's header says
     "N malformed Code grounds texts — nothing checks what they stand for".
     The skill says "`MALFORMED` reads one cell of a row". The vendored
     template says "MALFORMED — a coordinate that does not parse". The
     coordinate in an overflowing row usually parses fine. What is wrong is
     that text past the last column is in no column. The remedy differs too:
     escape a pipe, not rewrite a coordinate. A new word costs one totals key,
     one field on the summary line and one word in the notice. Folding costs
     the same documents plus a word with two meanings.
   - **Why this grading.** See the third grounding row. The tree has already
     answered this for the sibling verdict, and the milestone being a minor
     release does not change the reason the owner gave.
   - **The word.** `OVERFLOW` is the issue's own term ("an overflow cell")
     and this work item's id. It is used nowhere else in the shipped tree
     (searched 2026-09-29 over `hooks/`, `skills/`, `docs/`, `agents/`,
     `templates/`, `tests/` and both READMEs). It is exactly eight
     characters, the width `main` pads a status to.
   - **Only more cells are refused.** A row with fewer cells hides nothing.
     GitHub renders every cell of a short row, and the rule, the issue, the
     owner's answer, and the old case's own name and docstring all say
     *more*. The old case compared with `!=`, which also refused a short row.
     That was broader than anything the case or the policy stated, and this
     work does not carry it into other people's builds (see *Out*).

2. **One table walk, shared.** The header logic in `grounds_cells`, which
   the `MALFORMED` arm uses, moves into a walker, `ledger_table_rows`. It yields each
   body row with its line number and its header's cells (or `None` under no
   header). `grounds_cells` and the new `overflow_rows` both read through
   it. `MALFORMED`'s behaviour does not change. The walker is the surface
   work item C (#387, which needs a row's `Checked` cell) can build on
   without writing a third walk.

3. **The ledger row's columns as a constant.** `LEDGER_COLUMNS` is the
   template's header cells, `("Clause", "Code grounds", "Verified behavior",
   "Checked", "Notes")`. `overflow_rows` counts a header-less row against its
   length, and `grounds_cells` takes a header-less row's `Code grounds` index
   from it rather than from a literal `1`. A case holds the constant against
   `templates/ledger.md`'s `| Clause |` header. The constant is not read from
   the template at run time, because `evidence-ci` puts this file alone in a
   user repository's `tools/`, where no template is beside it. The
   `MALFORMED` arm already rests on the same five-column premise, in its
   section comment.

4. **Every reader of the verdicts says the new one.**
   - `main`: a totals key, and both summary lines end `· N overflow`,
     printed at zero too. The new field goes after `malformed`, so the text
     every reader matches today is unchanged. `broad_gate.py#LEDGER_RE`
     reads only up to `broken` (read).
   - `exit_code`: `OVERFLOW` joins the `DRIFTED` / `MALFORMED` branch, below
     `BROKEN`.
   - `LENIENT_NOTICE` names `OVERFLOW` beside `DRIFTED` and `MALFORMED`.
   - `reverify`: an overflowing row gets a `LEFT` line naming the ledger, the
     line and the verdict, and the run exits 1, as a `MALFORMED` row does.
     The line must name the ledger, because `reverify` prints no per-ledger
     heading. The hashes in the row are still rewritten where their anchors
     resolve, because the hash is not what is wrong with the row.
   - `hooks/evidence-advisor.py`: `failing_rows` keeps `OVERFLOW`, and `main`
     prints it as its own block with the per-row detail.

5. **The documents that state the grading or list the verdicts.**
   - `skills/evidence-check/SKILL.md`: the `--strict` row of the flags table,
     the reader table under *Which reader graded your tree*, a row in
     *Verdicts and what to do*, and *Known limits* (the `--reverify` bullet,
     and a bullet saying the arm reads every table in a ledger file, not only
     tables with a `Code grounds` column).
   - `skills/evidence-ci/SKILL.md`, the "**1 is not only drift.**" paragraph.
   - `templates/evidence-check.yml`, the comment above the run line.
   - `.github/workflows/test.yml`, the `ledger` job's comment and its
     `::warning::` text.
   - `README.md` and `README.ko.md`, the `evidence-check . [--strict]` row of
     the command table. This is the README row the owner's answer asks for.
     Neither README states a verdict list anywhere else (searched
     2026-09-29).
   - `docs/the-evidence-ledger.md`, the paragraph in the first grounding row.

6. **This repository's case becomes a caller of the shipped arm.**
   `tests/test_release_hygiene.py#test_no_ledger_row_splits_into_more_cells_than_its_header`
   keeps its name, because the replacement ledger claim will cite it. It
   calls `evidence_check.overflow_rows` over the files the checker reads. The
   case's own implementation of the rule is removed:
   `overwide_rows`, `cell_count`, `TABLE_RULE`, `ledger_row_width`, `ledger_overwide` · NAME NOT IN TREE
   Its two unit cases are removed too, and their shapes move into the arm's
   own cases (the #562 split row, the #501 header-less row, and the
   header-less row beside a two-column table that keeps its own width).
   - **Why a caller, not a removal.** CI's `ledger` job is the lenient
     reader, so an overflowing row there is a warning, not a failure. The
     pytest case is what refuses one on a contributor's pull request today.
     Removing it would soften this repository's own CI, and the owner did not
     ask for that.
   - **Why not keep both implementations.** They already disagree in four
     places, and the shipped reading is the right one in each:
     - the old case compares with `!=`;
     - it toggles fences only on a line opening with three backticks at
       column 0, so a `~~~` block is read and an unclosed block hides the
       rest of the file;
     - it requires the `|` at column 0, so an indented row is skipped;
     - its cell count reads a row ending in `\|` one cell short.
   - The corpus case is not red-able by the tree, because no row in it
     overflows. So the walk moves into a helper that takes a root, and a
     second case plants a tree holding one overflowing fragment row. That is
     the case shown red.

7. **The ledger stays true.** Rows whose anchors this work removes are
   REMOVED from the files they stand in: C2 in `seal/releases/0.15.1.md` and
   L1 in `seal/releases/0.15.3.md` both cite units phase 3 deletes. Their
   claims, which still hold, are written anew in this work item's fragment
   against the shipped arm and the corpus case. Every row this work drifts is
   re-read where it stands (`plan.md` lists the candidates).

8. **The old question closes.** `questions.md` Q1 of work item
   1790260565-a-ledger-row-carries-two-readings-in-one is ticked with the
   owner's answer and date and the commit that built it. That is the
   precedent 1790381328 set for 1790297087's Q1.

### Out, and why

- **Refusing a row with fewer cells than its header.** Nothing is hidden
  in such a row, and no document states the rule. This repository loses the
  `!=` half of its old case. That half finds nothing in today's tree: over
  the 36 ledger files at `11e3104c`, a throwaway instrument
  using the shared `split_row`, `unquoted` and the header rule found 891 body
  rows (67 of them under no header), and none has fewer or more cells than
  its width. That is my instrument's reading, not the arm's output, and
  `questions.md` Q2 has the arm confirm it.
- **Fence and comment reading in other readers.** Work item B (#584) owns
  those, in parallel. This work adds no fence walk. `evidence_check.py`
  already asks the shared rule.
- **`--reverify`'s `Checked` date and the records arm.** Work item C (#387,
  #508) edits both after this one squashes. This work touches `reverify`
  only to add the `LEFT` line, beside the existing `MALFORMED` one.
- **A table whose header is wider than the ledger row's five columns.** Its
  rows are measured against its own header. That is the rule as written, and
  round 1 of 1790260565 recorded it as a limit of the rule, not of a fix.
- **A GFM table whose delimiter row has a different cell count from its
  header**, which GitHub does not render as a table at all. The walker keeps
  `grounds_cells`' header rule, a row followed by a rule row, and changes
  nothing else.
- **An indented code block (four spaces or more).** `split_row` strips
  indentation, so such a line is read as a row. The `MALFORMED` arm already
  reads it that way, and nobody has reported a case.
- **Moving the policy statement to §*What the checker refuses*.** The
  paragraph is edited where it stands. Moving it would re-anchor every row
  that cites either section for no change of meaning.
- **`seal/follow-up.md` row 69** (`--reverify` re-stamps every row citing a
  coordinate) is a hazard phase 4 steps around, not a prerequisite. No other
  follow-up row is about this checker's cells.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · a split row is named | Given a ledger table with a five-cell header and a row whose unescaped `\|` splits it into six, when `evidence-check .` runs, then the row is named `OVERFLOW` with its line number, both counts and the remedy (write a `\|` inside a cell as `\\|`). The run exits 1, prints the lenient notice naming `OVERFLOW`, and exits 2 under `--strict` | A new case, seen red against the tree at `11e3104c` (exit 0, no finding) |
| A2 · a header-less row is counted | Given a fragment with no header whose row splits into six, then it is named against `len(LEDGER_COLUMNS)`. Given the same rows after a blank line under a two-column table, then the table keeps its own width and the fragment row is still named | A new case, seen red as A1 |
| A3 · the reading is the shared one | Given an overflowing row inside a closed ```` ``` ```` block, a closed `~~~` block and an indented (≤ 3 spaces) closed fence, then none is named. Given one inside an unclosed fence or an HTML comment, then it is named. Given `\|` inside a cell, or a row ending `\|` with no closing pipe, then the cell count is exact | Parametrised shapes in the arm's case |
| A4 · a short row is not refused | Given a row with fewer cells than its header, then nothing is named | The same case |
| A5 · a vendored copy refuses the same row | Given the checker copied alone into `tools/`, with no shared reader beside it, when it runs over A1's ledger, then it names the same row | A case in the shape of `test_a_vendored_copy_skips_a_fenced_example_too` |
| A6 · the columns are the template's | Given `LEDGER_COLUMNS`, when compared with the cells of `templates/ledger.md`'s `\| Clause \|` header split by `split_row`, then they are equal | A case, seen red with one column renamed in the constant |
| A7 · `MALFORMED` is unchanged | Given every existing `MALFORMED` case, after `grounds_cells` reads through `ledger_table_rows`, then all pass unchanged | Narrow run of `tests/test_a_row_points_by_content.py` and `tests/test_evidence_check.py` before and after |
| A8 · the totals say it at zero | Given a clean ledger, then both summary lines end `· 0 malformed · 0 overflow`, and `broad_gate.py#LEDGER_RE` still matches the total line | A case, plus the existing S9 case |
| A9 · `--reverify` does not go quiet | Given A1's ledger, when `--reverify` runs, then it prints a `LEFT` line naming the ledger, the line and `OVERFLOW`, and exits 1 | A new case, seen red (exit 0, no line) |
| A10 · the commit hears it | Given a commit in an opted-in repository whose ledger holds A1's row, when the advisor runs, then it prints an `OVERFLOW` block naming the row | A case in `tests/test_dispatch.py` beside `test_a_commit_with_a_malformed_ledger_row_is_told_so`, seen red |
| A11 · every page states the grading the code returns | Given `SKILL.md`'s verdict row and reader table, then each states what `exit_code` returns for `OVERFLOW` and is held against `exit_code`, as `MALFORMED`'s already are. Given the notice, then `test_the_notice_borrows_the_word_the_failing_gate_prints` requires `OVERFLOW` in it | The existing cases in `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, extended and seen red against the page before its edit |
| A12 · this repository still refuses on a pull request | Given this repository's ledgers, when the corpus case runs, then it calls `overflow_rows` over the files the checker reads and is green. Given a planted tree holding one overflowing fragment row, then the planted case names it | Narrow run of `tests/test_release_hygiene.py`. The planted case is seen red with the helper's call to the arm removed |
| A13 · a new ledger is clean | Given `templates/ledger.md` copied as a repository's `seal/ledger.md`, then the run names no `OVERFLOW` | A case |
| A14 · the policy names what enforces it | Given `docs/the-evidence-ledger.md`'s paragraph, then it says the shipped checker names such a row `OVERFLOW` in every repository, and its `Enforced by:` line resolves | `tests/test_a_folded_statement_names_what_enforces_it.py`, `tests/test_a_document_has_room_for_the_next_fold.py` |
| A15 · the ledger stays true | Given the branch's tip, then C2 and L1 are gone from their files and their claims stand in this work's fragment, every row this branch drifted carries a dated `Re-read` (or `Corrected`) note, and `evidence-check --strict .` names nothing this branch caused | The checker run unscoped at phase 4, and `survivor-check` over the branch |

## Data & interfaces

Three names are the interface work item C builds on. Their names are part of
this contract. A builder who renames one records the divergence in
`overview.md` and corrects this file, because the records arm reads the names
stated here.

- `evidence_check.py#LEDGER_COLUMNS`: a tuple of the five header cell texts.
- `evidence_check.py#ledger_table_rows(text)`: yields `(line_number, header, cells)`
  for every body row of every table in `unquoted(text)`. `header` is the
  header row's cells, or `None` for a row in a run with no header. Rule rows
  and header rows are not yielded. Line numbers are 1-based, into the text as
  given (`unquoted` keeps every offset). The name is not the shorter one
  because `hooks/routing.py` and `skills/code-review/scripts/chain_check.py`
  each already define a function of that name with another signature, and the
  records arm reads a backticked name as present if any file has it.
- `evidence_check.py#overflow_rows(text)`: `[("OVERFLOW", coord, detail)]`,
  the same shape as `malformed_rows` and `old_format_rows`. `coord` names
  the line (`line <n>`). `detail` says the row's count, the header's count
  (or that no header stood above it and what it was counted against) and the
  remedy. The exact wording is the builder's, and it is pinned (§14).
- `check_ledger` extends its findings with `overflow_rows(text)`.
- `totals` gains `"OVERFLOW"`. Both summary lines gain `· {n} overflow` last.
- `grounds_cells` keeps its signature and its yield.

No other shipped interface changes. Test modules touched:
`tests/test_release_hygiene.py`, `tests/test_evidence_check.py`,
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`,
`tests/test_dispatch.py`, and one new module for the arm, named for the
behaviour in this repository's style.

## Open questions → questions.md

No row needs a person. The owner answered the one product question before
the build. The judgments the ticket left open were answered from the tree,
and `questions.md` lists them. Its rows are measurements and the work's.

Framed 2026-09-29 by framer, before the build.
