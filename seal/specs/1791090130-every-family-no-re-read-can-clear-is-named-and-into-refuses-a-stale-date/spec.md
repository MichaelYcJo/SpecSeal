# Feature Specification: every family no re-read can clear is named, and `--into` refuses a stale date

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issue #746, deferred from #743's round 2
(`seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/rounds/round-2-report.md`
§*Findings* ⬜ 11 and ⬜ 12, read on this branch's base `edee5ca2`). Two
findings, one class: a `--reverify` run that exits 0 while `--strict` over
the same ledgers, run right after, still exits 2.

- **⬜ 12** is a write that cannot clear what it was written to clear. Under
  the freeze, `--reverify --into <fragment> --checked <date>` writes a
  `Re-read ·` row dated `<date>`. Where `<date>` is older than the family's
  newest reading of a coordinate the row carries, that newer reading still
  outranks the new row, so the family stays DRIFTED and the run exits 0. This
  work refuses that row.
- **⬜ 11** is a sentence that names one of three such families. The others
  are left exiting 0, and this work names them in the ledger home and pins
  each with a case.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, 3rd paragraph (*Of the members that record a coordinate, only the readings with the newest `Checked` date count, and readings that tie on that date are a union*) | The rule that makes a stale row useless. It also fixes the boundary: a `--checked` EQUAL to the newest date ties, joins the union, and clears, so only a strictly older date is refused (S2) |
| the same section, the `--into` paragraph (*The `Checked` column holds the date somebody read the code*) and `skills/implement/SKILL.md` §2 | The date is a statement by the person who read the code. The refusal never suggests a later date as a way to pass. It says to read the code again and date that reading |
| `evidence_check.py#checked_refusal` docstring (*`today` is not taken: the value is a statement typed by whoever did the reading*) | The refusal does not rewrite or round the date. It names the row and leaves it |
| the same section, the last paragraph's last sentence (*A row corrected by two rows is not a re-read's to clear …*) | The sentence ⬜ 11 widens. The rewrite starts from the round-2 report §*Paste-ready fixes* ⬜ 11 and is checked against phase 2's enumeration |
| `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md` W1 (order: refuse, plan, record, apply), W2 (killed at any step), W4 (idempotence by the record's last word), W8 (a line that says a write happened prints after it lands), and W9's last paragraph (*a refusal #746 adds for a stale `--checked` goes in step 0 beside the `--into` refusal, or keeps the refused family out of both the plan and its moves. Either way, a refused row writes nothing and records nothing*) | The seam. This frame takes W9's second option. `plan.md`'s Alternatives table says why the first one over-refuses |
| `skills/agent-contract/SKILL.md` §12 (enumerate the class), §14 (a changed message is documented and pinned in the same commit), §15 (a case is seen red before it is planted) | The phases' verification rules |
| `CLAUDE.md` (project) *The goal a design is chosen against* | A per-row LEFT at exit 1 lets the rest of the run write. It does not stop the whole run for one family (`plan.md`, Alternatives) |

## The class, by construction

The class is **a `--reverify` run that exits 0 while `--strict` over the same
ledgers, run straight after, exits non-zero because of a coordinate graded in
a family** (DRIFTED or BROKEN). `--reverify` has three answers for such a
coordinate: re-stamp a row in place, write a `Re-read ·` row (`--into`, under
the freeze), or name the family on a `LEFT` line and exit 1. The class is
every configuration none of the three answers.

**⬜ 12's half: a write that adds a reading older than the one it must
outrank.** Read at `edee5ca2`:

- An in-place re-stamp is never in this half. `dated_cell` appends
  ` · <date>` to the row's own `Checked` cell, and `family_view`'s `checked`
  orders a row by the NEWEST date in that cell. So a re-stamp never lowers
  its row's date, and the row it re-stamps holds at that date. A newer
  reading in a file the narrowing left out is already named on the
  `still DRIFTED … run it without --ledger` line (`main`, unfrozen path) or
  owed a `Re-read ·` row (frozen path).
- A `Re-read ·` row is a NEW reading at exactly `--checked`, so it is the one
  write that can land below the reading it answers. Two configurations put
  that reading out of the run's reach:
  1. **it sits in a fragment the narrowing left out** (the report's P5, both
     carriers): nothing re-stamps it;
  2. **it sits in a released file** — the root itself, a folded `Re-read ·`,
     or a released row outside every family whose own `Checked` date is the
     newest. This happens narrowed or not, because a released file is never
     written under the freeze.

  `reverify_into` (`skills/evidence-check/scripts/evidence_check.py#reverify_into`)
  is the only writer of such a row. One check there covers both.

**⬜ 11's half: what no re-read clears.** Read against `released_drift`,
`reverify`'s return and the report's executed probes P6, P8, P10, P11
(`read`, not executed by this frame):

| Family | `--strict` | `--reverify` today |
|---|---|---|
| a released row corrected by two `Corrected ·` rows | 2, each correcting row DRIFTED naming the others | 0, narrowed or not (P8) |
| a BROKEN anchor (no place holds the unit, file or statement) | 2 | 0 where only fragment rows carry it, and 0 without the freeze; 1 under the freeze where a released row carries it (`released_drift`'s `broken`) (P6, P10) |
| a family rooted in a fragment (`Corrected ·` in a fragment) whose anchored statement is gone | 2 | 0: the in-place re-stamp leaves it, and `released_drift`'s fragment-root guard keeps it from being named (P11) |

After ⬜ 12 the stale `Re-read ·` row leaves this class: it is named at
exit 1. Phase 2 runs the enumeration as a measurement (questions.md Q1)
before the sentence is written, because this table is `read`.

## Scope

### In

**S1 — `--into` refuses a row its `--checked` date cannot make count.** In
`reverify_into`, for each released row it would write a `Re-read ·` row for:
when `--checked` is strictly older than the newest reading of ANY drifted
coordinate that row would carry, the whole row is refused.

- The row is not added to the rows to write.
- No move is appended for it, so the pact-change record gets nothing for it.
- It is named on a `LEFT` line, and the run exits 1.

The newest reading is the one `family_view` grades by. It is the newest
calendar date in a member's `Checked` cell, over the members that carry that
coordinate. For a released row outside every family, it is that row's own
`Checked` cell.

**S2 — a tie is not stale.** `--checked` equal to the newest date writes the
row as today. The row joins the union and clears the family.

**S3 — the `LEFT` line says what a person needs, and a case pins it (§14).**
It holds:
- where the row is, and its label;
- the `--checked` value;
- the newest date, and where the reading that holds it sits;
- that nothing was written or recorded for this row;
- the repair: read the code again and date that reading.

Where the newest date is later than today, no `--checked` can reach it,
because `checked_refusal` refuses a date after today. For that case the line
names a `Corrected ·` row as the repair. The wording is the work's
(questions.md Q3). These elements are the spec.

**S4 — the ledger home names every family no re-read clears (⬜ 11).**
`docs/the-evidence-ledger.md` §*A released row is read again in the branch's
fragment*:
- the trailing double-correction sentence of the last paragraph is replaced
  by a bold-led paragraph that names each family in the table above, with its
  `--strict` and `--reverify` exits, plus any further family phase 2's
  enumeration finds;
- the `--into` paragraph gains the S1 refusal, in one or two sentences.

The usage text at the head of `evidence_check.py` gains one clause for S1.

**S5 — each family is held by a case.** Every family the S4 paragraph names
has a case. The case asserts `--strict`'s exit and `--reverify`'s, narrowed
and not, under each mode where the paragraph states one. Existing cases are
extended where one already builds the family:
- `test_a_released_row_corrected_by_two_rows_names_both` asserts `--strict`
  only today;
- `test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read` asserts
  "no LEFT line" only.

**S6 — the record-first order is untouched.** The S1 check runs in step 1
(plan), inside `reverify_into`, before the row reaches `rows` and before its
moves reach `moves`. Step 0 is unchanged. The record and the plan never hold
anything for a refused row, so W1, W2 and W4 hold as written: a run killed
anywhere leaves nothing of the refused row on disk. A second identical run
refuses it again and records nothing (W4).

**S7 — evidence.** Rows for S1 and S4 go in this work item's fragment,
`seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md`.
Released rows whose code this work drifts are read again into that same
fragment with `--reverify --into`. The changelog entry goes in this
directory's `changelog.md`.

### Out, and why

| Left out | Why |
|---|---|
| Changing `--reverify`'s exit for the three ⬜ 11 families (making a BROKEN fragment row or a double correction exit 1) | The issue asks for them to be named and held by a case. The report says *only the sentence is this item's*. Changing a writer's exit for configurations it has always answered 0 is new behaviour no one has asked for. If someone wants it, it becomes its own issue |
| A whole-run refusal at step 0 (exit 2) | `plan.md`, Alternatives: step 0 runs before the in-place re-stamp, so it would refuse runs that write no stale row |
| Lowering or rewriting a cell's date in place | `dated_cell` appends, and the newest date in the cell wins, so an older `--checked` on an in-place re-stamp clears what it re-stamps. That is not in the class |
| Row-shape refusals (`MALFORMED`, `OLD-FORMAT`, `OVERFLOW`) and the records arm's `refused` | They are not a family's coordinate grading, which is what S4's paragraph is about. §*What the checker refuses* already names them, and their repair is an edit or `--migrate`, not a reading. If phase 2's enumeration shows one of them inside a family exiting 0, the work adds it (Q1) |
| The ten rows a parallel chore is re-reading after the wave-one squashes | That chore owns them (the spawn prompt). This work reads again only the rows its own edits drift |
| ⬜ 10 of the same report | It is #740's and was answered there |
| The Windows leg | CI's Windows job answers it, as for #740 |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 — stale date, newest reading in a fragment left out (P5) | Given `three_readings` with M and N in fragments (either carrier) and the freeze, when `--reverify --into <MEMBER_INTO> --checked 2026-02-15 --ledger <M's file>` runs, then it exits 1, prints S3's `LEFT` line naming N's date 2026-03-01 and N's place, writes no `Re-read ·` row, and prints no `wrote` line | new case, red at `edee5ca2` (exit 0, `1 citing row written`) |
| A2 — stale date, newest reading released | Given N folded into a release file, the freeze, no `--ledger`, when `--into --checked 2026-02-15` runs, then the same as A1 | new case, red at `edee5ca2` |
| A3 — a tie clears | Given A1's tree with `--checked 2026-03-01`, the row is written, and `--strict` over the same narrowing then exits 0 | new case. Its red: change the comparison to `<=` and it fails |
| A4 — the grid's invariant holds for a stale date | Given the narrowed grid (`test_a_narrowed_reverify_exits_0_only_where_the_narrowed_strict_does`) in mode `freeze with --into`, with `--checked` between M and N, a `--reverify` exiting 0 is followed by a `--strict` exiting 0 | grid extension or sibling, red at `edee5ca2` in the P5 cells (shape: questions.md Q4) |
| A5 — a refused row records nothing | Given a signatory whose drifted released row cites a pact clause, when `--into` runs with a stale date, then `seal/pact-changes/<id>.md` gains no row for it, and a second identical run leaves the record byte for byte | new case in `tests/test_a_signatory_records_a_pact_change.py`. Red: append the moves before the check |
| A6 — other rows of the same run still write | Given two drifted released rows, one stale and one not, then one `Re-read ·` row is written, one `LEFT`, exit 1 | new case |
| A7 — newest after today | Given a released row whose `Checked` date is after today, then the `LEFT` line names a `Corrected ·` row as the repair | new case (Q2 says whether `--strict` already refuses such a cell) |
| A8 — the double correction | `--strict` 2, `--reverify` 0 narrowed and not, in each mode the paragraph states | extend `test_a_released_row_corrected_by_two_rows_names_both` or a sibling |
| A9 — a BROKEN anchor | fragment-only carrier: `--reverify` 0; released carrier without the freeze: 0; released carrier under the freeze: 1, named with the `Corrected ·` repair; `--strict` 2 in each | new parametrized case |
| A10 — a fragment-rooted family whose statement is gone | `--strict` 2, `--reverify` 0, narrowed and not | extend `test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read` |
| A11 — the home says it | S4's paragraph and the `--into` sentence exist, the line-wrap and one-word checks pass on the doc | `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py`, read by the reviewer |

The cases for A8–A10 pin behaviour that already holds, so §15's red cannot
come from the old code. Each one is seen red by a mutation of the code under
test (for A10, deleting `released_drift`'s fragment-root guard turns the run
to exit 1), and the handover says which.

## Data & interfaces

- `family_view`'s namespace gains the newest date per coordinate, and where
  it sits, so `reverify_into` reads the same answer `--strict` grades by.
  The plan's Alternatives table chooses how.
- `reverify_into` gains one refusal branch and needs today's date for S3's
  after-today arm. It already receives `checked`.
- New output: S3's `LEFT` line. No other line changes. The closing count
  `N citing rows written · M released rows left` counts a refused row as
  left, which it already does for every `LEFT`.
- No new flag, no new exit code: exit 1 is `reverify_into`'s existing
  *a row was left*.
- New file I/O, if any, names `encoding="utf-8"` (#757).

## Open questions → questions.md

None blocks the build. `questions.md` holds two measurement rows, two rows
for the work, and the judgments the tree answered.

Framed 2026-10-04 by framer, before the build.
