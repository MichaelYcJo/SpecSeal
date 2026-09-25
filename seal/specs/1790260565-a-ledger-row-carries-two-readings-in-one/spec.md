# Feature Specification: a ledger row carries two readings in one, and the rules' cases

<!-- seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issues: #568, #501, #569. Three defects in the shape of a ledger row and in
the cases that hold the ledger's rules. None of them changes a shipped script.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A correction a merge dropped*, the halves paragraph (1790208643's marker) | A conflicted row's `Re-read <date>` and `Corrected <date>` notes are a **union**, because each records a reading somebody performed. This answers #568's open question from the tree: the two pairs in each row are the two sides of one merge, so neither pair is "the row's" alone. |
| `docs/the-evidence-ledger.md` §*A row is a content anchor*, the edit-arm paragraph | A branch keeps an existing claim true **in the file the row is in**: re-stamped with a dated note where it holds, corrected in place first with a `Corrected <date>` note where it is false. This is the licence for every edit this work makes to `seal/releases/*.md`. New claims go to `seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md`. |
| `docs/the-evidence-ledger.md` §*A row is a content anchor*, the escaped-pipe paragraph, `Enforced by: tests/test_release_hygiene.py::overwide_rows` | The rule #501 asked for already stands: a row wider than its table's header fails, and the case "reads the shared file, every release file and every fragment". This work makes the last clause true (see *What #501 still lacks*). The `Enforced by:` line names `overwide_rows`, so the function keeps that name. |
| `docs/the-evidence-ledger.md` §*A correction a merge dropped*, the marker-check paragraph | The marker check reads fragments "because … a check that skipped fragments would go blind exactly while the rows are being written". The same argument decides #501's gap. |
| `CLAUDE.md` §*Repo rule — a change writes fragments*: "A ledger fragment needs no header of its own" | A fragment has no header **by rule**, so a width check that needs a header can never count a fragment row. The rule stays; the check supplies the width instead. |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Each defect is enumerated as a class. A changed sentence is pinned in the same commit. Every new case is seen red before it is committed. |
| `CLAUDE.md` is the owner's | No agent edits it. Judged: no sentence in it becomes false (plan §*Technical context*). |

## Scope

### In

1. **#568: three ledger rows each state one reading.** Enumerated by
   construction rather than taken from the issue. The instrument was every
   `\|` outside a code span, in any table row of `seal/ledger.md` and
   `seal/releases/*.md`, over the tree at `ca1f683c`. Its answer is the
   issue's three rows exactly:
   - `seal/releases/0.9.2.md`, row **S4**, section
     `1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible`;
   - `seal/releases/0.8.2.md`, row **G5**, section
     `1788661274-the-roll-names-the-next-version-by-guessing`;
   - `seal/releases/0.9.3.md`, the row that begins *The eleven modules that pin
     the path*.

   **What the tree says about #568's question.** In S4 and G5 the second
   pair's Notes begins with the first pair's opening text, word for word.
   Each carries markers the other lacks: the first runs to 2026-09-22, and
   the second holds 2026-09-23 and 2026-09-24. That is one merge's two sides,
   both kept whole. By the halves rule the notes are a union. So the repair
   is one Checked cell and one Notes cell holding the shared opening once and
   every marker from both sides in date order. It is not a choice between
   the two pairs.

   **The third row has a different shape.** It never had a second date.
   Read at `31937b9f` (#562's base) with the file split on unescaped pipes,
   it had six cells: one date, and a Notes cell split into two. Today it has
   one date and a Notes cell broken by two escaped separators. So #568's
   phrase "two Checked-and-Notes readings" fits S4 and G5 only. The third
   row only needs its Notes joined. The policy sentence that says "three of
   them a second date-and-notes pair" is false for this row, and C2's note
   (`seal/releases/0.15.1.md`) repeats it. Both are corrected in phase 2.

2. **#501: what `overwide_rows` still lacks.** It was measured, not assumed.
   `overwide_rows` sets its width from the header row above the table. A row
   with no header above it is skipped by
   `if TABLE_RULE.fullmatch(line.strip()) or header is None: continue`.
   Every fragment is headerless by rule (`CLAUDE.md`; the fragment template
   comment "No header"). The fold copies a fragment into its release file
   byte for byte (`.github/scripts/fold_ledger.py` module docstring, *A fold
   is a move*). So:
   - **every fragment row goes uncounted.** That covers every row a branch
     writes, during the whole life of the branch;
   - **25 released rows go uncounted today**: 5 in `seal/releases/0.15.0.md`
     and 20 in `seal/releases/0.15.1.md`. That number is the output of a
     script I wrote that copies the function's header logic. It is not the
     case's own output, so it is labelled **read**. All 25 have five cells.
     The shared file and the release files hold 767 table body rows in all;
   - the policy's "The case reads … every fragment" and C2's claim "over the
     shared file, every release file and every fragment" are therefore true
     of *reading* and false of *counting*.

   The repair: a row with no header above it is counted against the ledger
   row's width, which `templates/ledger.md` declares as
   `| Clause | Code grounds | Verified behavior | Checked | Notes |`. The
   case reads that width from the template, so it is not a literal. The
   policy paragraph and C2 are corrected to say so.

   #501's other halves are already done, and this work leaves them alone:
   the cell count (#562), the `\|` escape convention (#562), and the
   invisible `Re-verified 2026-09-16` marker. That marker is on the
   eleven-modules row, which phase 1 joins.

3. **#569 ⬜ 1: the clauses #567's review added are held by a case.**
   `CONFLICT_SENTENCES` gains the three needles the reviewer ran:
   `` `Corrected <date>` note ``, "to neither side where both did" and
   "re-read against every edit the merged unit carries". `OWNED_SENTENCES`
   becomes `CONFLICT_SENTENCES[-7:]`. The owner's case gains its
   third-outcome assertion, "the edit made false is corrected there first".
   The stale comment "the checker says which after the fact" is replaced. The
   tree was read on 2026-09-24, each document with its whitespace collapsed:
   every needle is already present in `CLAUDE.md`, `CONTRIBUTING.md` and
   `docs/the-evidence-ledger.md`, and the owner-only sentence is in the
   policy document alone. So the case goes in green and no document changes.
   E1 and E2 (`seal/releases/0.15.1.md`) say "held by no case yet — #569
   carries the case". Each gets a re-read note in place.

4. **#569 ⬜ 2: one exception, one rule named.** `docs/round-record-spec.md`
   §*The fix surface*, paragraph "Its direction is `allow`…", says the
   exception is to "the `blocks more` direction `docs/review-chain-spec.md`
   §*The reopening* states". That section's only `blocks more` is the
   reopening check's own failure direction (`docs/review-chain-spec.md`,
   "**Failure direction: blocks more.**"). The code names a different rule:
   `chain_check.py#says_not_yet`'s docstring says the exception is to "this
   file's `blocks more` direction. Every other refusal here treats what it
   cannot read as the failing case." The code is right. The document takes
   the reviewer's sentence, and a case holds the document and the docstring
   to the same referent.

### Out, and why

- **The cell count as a shipped check for consumer repositories.**
  `evidence_check.py` counts no cells, so a repository that installs the
  plugin gets no width refusal. #501 is written about this repository's
  files. Shipping the count would be a new refusal in other people's builds,
  and the parallel chain is editing `evidence_check.py` right now. →
  `questions.md` Q1.
- **The fence toggle in `overwide_rows`.** It recognises only a line
  starting with three backticks, and misses `~~~` and indented fences. That
  is the class the parallel chain `1790260566-a-row-inside-a-fence-reads-as-live`
  (#444, #491) owns in the readers. If that chain lands a shared fence
  helper, adopting it here is a later step. Answerer: the orchestrator, when
  it sequences the two branches.
- **A row that ends in an escaped pipe with no terminator.** `cells()` tests
  `endswith("|")` without looking for the escape, so such a row is counted
  one cell short. That produces a false **refusal**: loud, and it names the
  line. No ledger row has this shape (a `\|` at end of line was searched for
  on 2026-09-24 and none was found). It is not #501's failure, which is
  a silent pass.
- **A case that refuses a second Checked date inside a Notes cell.** It would
  stop #568's shape from coming back, but it is new mechanism with no clear
  spelling. The unescaped form is already refused loudly by `overwide_rows`.
  Escaping a second pair was a deliberate act by #562, which left the
  decision open because the decision was not the escape's to make.
- **`Re-verified` is not a marker verb.** `correction_check` reads
  `Corrected` and `Re-read` only, and
  `test_a_verb_that_is_not_a_marker_is_not_read_as_one` holds that on
  purpose. The eleven-modules row keeps its `Re-verified 2026-09-16` text as
  written, and phase 1 rewrites no note's verb. 18 other `Re-verified`
  occurrences stand in release files (counted by `grep -c` on 2026-09-24).
  Nobody has filed them, and this work does not.
- **Narrowing the two `Enforced by:` lines** over the edit-arm and halves
  paragraphs, which currently name the module, to the owner's case. They are
  valid as they are. The change would edit two folded statements for no
  finding.
- **`seal/follow-up.md` rows 72 and 79.** Both are about the ledger's edit
  rules. Row 72: `--reverify` re-stamps rows nobody read. Row 79: code a
  branch added can falsify a claim. This work is the prerequisite of neither.
  Row 72 is a hazard phase 1 steps around (plan, phase 1).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · one reading per row | Given the three rows, when a person opens each, then it has one `Checked` cell and one `Notes` cell, holds no `\|` outside a code span, and keeps every `Corrected <date>` / `Re-read <date>` marker it carried before | The phase-1 instrument, which searches for `\|` outside code spans in every ledger file, returns no row. A marker-multiset comparison of each row before and after uses `correction_check.py`'s own marker reader and finds nothing lost |
| A2 · the rows' claims were re-read | Given S4, G5 and the eleven-modules row, when the branch closes, then each carries a `Re-read <date> by work item 1790260565 (#568)` note (or `Corrected <date>` where the re-read found the claim false), its Checked date is the re-read date, and its anchors are `ok` | `bin/evidence-check --ledger <file> .` over the three files names no drifted row among the three |
| A3 · a fragment row is counted | Given a headerless table whose row splits into six cells, when `overwide_rows` reads it, then it names the row against five cells | A new case in `tests/test_release_hygiene.py`, seen red against the current `overwide_rows` (which returns `[]`) |
| A4 · the corpus still passes | Given the tree, when `test_no_ledger_row_splits_into_more_cells_than_its_header` runs, then it is green, and the 25 headerless released rows are now among the rows it counts | The module run narrowly; the case's docstring states the new count with its instrument and date |
| A5 · the policy says what the case counts | Given `docs/the-evidence-ledger.md`'s escaped-pipe paragraph, when a person reads it, then it says a row under no header is counted against the template's five columns, and it no longer calls the third #562 row a second date-and-notes pair | Read; `Enforced by:` still resolves (`tests/test_a_folded_statement_names_what_enforces_it.py`) |
| A6 · every clause has a pin | Given the three carriers, when any one of #569's clauses is deleted from any one carrier, then `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` or `test_the_policy_document_owns_the_exception_and_the_halves` goes red | Deletions made one at a time. `CLAUDE.md` is mutated only in a scratch copy, never in place. The case is shown red once per deletion |
| A7 · E1 and E2 say the clauses are pinned | Given E1 and E2 in `seal/releases/0.15.1.md`, when read, then a dated note says the clauses are now held and names the two cases | Read; the rows' hashes re-stamped after re-reading |
| A8 · one exception names one rule | Given `docs/round-record-spec.md` and `chain_check.py#says_not_yet`, when a person reads either, then both name the exception to the direction every other refusal in `chain_check.py` takes, and the document no longer points at §*The reopening* | A new case reads both texts. It is seen red against the current document |
| A9 · no claim goes stale | Given every row whose anchor this branch drifted, when the branch is handed to review, then each has been re-read and re-stamped (or corrected) in the file it stands in, and the two new claims stand in the fragment | `bin/evidence-check --ledger` over each touched ledger file, lenient, names no drifted row this branch caused |

## Data & interfaces

- `tests/test_release_hygiene.py#overwide_rows`: the name stays, because
  the policy's `Enforced by:` line names it. It gains a width to use for a
  row with no header above it. The corpus case passes that width, read from
  `templates/ledger.md`'s ledger-row header. How the width is passed (a
  keyword argument or a constant) is the builder's call.
- `tests/test_a_merge_cannot_silently_drop_a_correction.py#CONFLICT_SENTENCES`,
  `#OWNED_SENTENCES` and
  `#test_the_policy_document_owns_the_exception_and_the_halves` change as
  #569's paste-ready block says.
- `tests/test_a_record_precedes_the_fixes_it_commissions.py` gains one case.
- No script under `skills/`, `hooks/` or `.github/scripts/` changes, and no
  shipped behaviour changes.
- Ledger rows touched in place: S4 (`0.9.2.md`), G5 (`0.8.2.md`), the
  eleven-modules row (`0.9.3.md`), and C2, E1 and E2 (`0.15.1.md`). Rows
  drifted as a side effect are re-read wherever they stand. Candidates found
  by grep: D1 (`0.15.1.md`, on the edit-arm section) and R4 (`0.9.1.md`, on
  §*The fix surface*). Rows added: two, in the fragment.

## Open questions → questions.md

One row needs a person. It does not block the build, and it has a default.
The other rows are the work's and a measurement's.

Framed 2026-09-24 by framer, before the build.
