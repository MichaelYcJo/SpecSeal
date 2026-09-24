# Feature Specification: the older statements name what enforces them (#565)

<!-- seal/specs/1790263216-the-older-statements-name-what-enforces-them/spec.md
     WHAT this work delivers. docs/ outranks this file; it cites, it does not
     restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/settle/SKILL.md` §*2. Write one standing statement per segment*, the shape paragraph and its four bullets | The shape every statement gets: a bold rule sentence first, grounds as prose, exactly one `Enforced by:` line written last. A target is a repository path, optionally `::<name>` for a `def` or `class`, several separated by commas. `Enforced by: nothing — <why>` with a non-empty reason is always possible. `Enforced by:` is a field name and stays English in every edition. **Whether a target really enforces the rule is not read by any check** — that is this work item's judgment and review's to audit |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*, the first two statements | The cutoff and the ceiling are stated in prose here and as `seal/config.md` rows, and `tests/test_a_document_has_room_for_the_next_fold.py#prose_disagreements` holds the two to the same numbers. The cutoff is read from the phrase ``from work item `N` on`` |
| `docs/the-evidence-ledger.md` §*A correction a merge dropped*, **A bound over the corpus is stated with its instrument and the moment it was taken** | The count the rewritten cutoff sentence states carries the command that took it and the commit it was taken at |
| `templates/config.md` §*The fold's values*; `skills/config/SKILL.md` row table | `Fold shape from` = `0` binds every statement. An absent row is *not declared* and runs no check, so `0`, not deleting the row, is how every statement is bound |
| `CLAUDE.md` §*a change writes fragments, never the shared file*, the *Appended is the word* paragraph | An edit to a document section a ledger row anchors drifts that row; the row is re-read against the edit and re-stamped **in the file it is in**, with a dated note, and corrected there first where the edit made it false |
| `CONTRIBUTING.md` §*House rules*, *Both READMEs move together, and so does every document with a `.ko.md` edition* | `docs/one-root-by-lifetime.ko.md` takes every decision `docs/one-root-by-lifetime.md` takes, in the same heading positions |
| `docs/the-evidence-ledger.md` §*The fold …*, the ceiling statement; `seal/config.md` `Document line ceiling` = 1000 | No edited document may cross 1000 lines |
| `skills/implement/SKILL.md` §1, judgment precedence | policy > SDD > ticket > code. A statement the code contradicts is not rewritten to match the code by default; see `questions.md` Q1 |
| `seal/specs/1790260563-the-fold-checks-run-only-as-this-repositorys-tests/spec.md` §*Data & interfaces*, *What #565 can rely on* | The worklist is `fold-check --shape-from 0`. An `Enforced by:` line with targets is exempt from the 88-column wrap in a covered document. Lowering the cutoff is one row plus the prose sentence, held by the pin |

## Scope

### The measured worklist

Executed 2026-09-25 at `701a878a` (this branch's head; the docs are those of
`e9dfe623`): `bin/fold-check --shape-from 0` reads **136 statements in 14
documents**. The configured cutoff `1790154761` binds 21, and `bin/fold-check`
with no flag exits 0. At `--shape-from 0` it exits 1 with 141 problem lines:

- **115 statements carry no `Enforced by:` line.** 9 of them are the Korean
  edition of 9 English ones, so the English decisions number **106** and the
  Korean edition repeats them.
- **26 of those 115 also do not open with a bold rule sentence** — 23
  English, 3 Korean. At cutoff `0` they are bound, so their openings are in
  scope.

Per document, statements without the line (bold-opening failures in
brackets): `the-evidence-ledger` 16 · `round-record-spec` 16 [2] ·
`the-broad-gate` 11 · `measuring-a-run` 10 · `review-chain-spec` 9 [2] ·
`one-root-by-lifetime` 9 [3] and its `.ko.md` 9 [3] · `commit-review-gate-spec`
8 [4] · `release-checklist` 6 [2] · `the-agent-set` 6 · `issues-and-milestones`
5 [3] · `branch-and-release` 4 [2] · `review-handoff-protocol` 4 [3] ·
`worktree-guard-spec` 2 [2].

**The 101 in the prose and the ticket is a different count, not a wrong
one.** It is the statements folded before #520; the other 14 belong to work
items released with it or waiting from before it, which the same prose
sentence also excludes (`seal/specs/1790260563-…/phases/phase-2.md`, Q1 of
that item's `questions.md`). This work item binds all 115, and the prose it
rewrites states 115 with its instrument. The milestone description of
`release: 0.15.3` also says 101; correcting a tracker text is a post, which
no agent makes — it is the orchestrating session's.

### In

1. **Every one of the 115 statements carries exactly one live `Enforced by:`
   line**, chosen by the criteria in §*What a decision is* below.
2. **Every one of the 26 opens with a bold rule sentence.** An existing
   sentence that states the statement's rule is bolded, and moved first
   where it is not first. A new sentence is written only where none states
   it, and then it restates what the statement already says — it adds no
   rule. A table or a fence that opens a statement gets the bold sentence
   on the line before it.
3. **`Fold shape from` is lowered to `0`**, and every sentence that states
   or relies on the old cutoff is rewritten in the same commit:
   - `docs/the-evidence-ledger.md` §*The fold …*, the first statement. It
     must still contain ``from work item `0` on`` (the pin's regex) and the
     settle link with its line break exactly as
     `` `skills/settle/SKILL.md` §*2. Write one standing statement per\nsegment* ``
     (`test_the_evidence_ledger_states_the_values_the_config_rows_hold`
     asserts that substring). It states what the cutoff was, that #565
     lowered it, and the 115 with `fold-check --shape-from 0` and the date
     it was taken beside it — a date and not a SHA, because this branch
     squashes and a SHA written into prose would stop resolving at the
     merge (`CLAUDE.md` §*the merge method is fixed per direction*). Its
     `Enforced by:` line names
     `skills/settle/scripts/fold_check.py::bound` and
     `tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape`,
     because the real-tree case at cutoff `0` is now what holds every
     statement.
   - The second statement's *29 of the 101 statements* becomes *29
     statements*: once the first statement states 115, a bare 101 beside it
     is an aggregate with no instrument and reads as a contradiction.
   - The module docstrings of `tests/test_a_folded_statement_names_what_enforces_it.py`
     (lines 10–14: *binds only markers …; retrofitting them is #565*) and
     `tests/test_a_document_has_room_for_the_next_fold.py` (line 8, *29 of
     the 101*). The planted-marker constant `CUTOFF = 1790154761` in the
     first stays: it is the planted fixtures' cutoff, and its comment
     already says it is not this repository's value.
4. **`tests/test_both_editions_carry_the_same_folds.py` also compares each
   paired statement's `Enforced by:` value**: the same targets in both
   editions, or `nothing` in both. The reason after `nothing — ` is prose
   and is not compared. The test's docstring already states its principle —
   compare what is language-neutral — and `settle` §2 makes the field and
   its targets language-neutral. Without it, the nine Korean lines have no
   reader.
5. **Every ledger row whose anchored unit these edits change is re-read and
   re-stamped in the file it is in**, with a dated `Re-read` note, or
   corrected there first with a `Corrected` note where the edit made its
   claim false. That includes rows in the stacked item's fragment
   `seal/ledger/1790260563-….md`, which phase 7 drifts.
6. **A changelog fragment**, `seal/specs/<this id>/changelog.md`.

### Out, and why

- **No new check for a rule nothing reads.** Such a rule gets
  `Enforced by: nothing — <why>` naming what would hold it. #565 asks for a
  decision per statement, not for new checks. Building them would multiply
  the review surface of a work item that is already 115 decisions wide. The
  line itself is the durable record: `grep -rn 'Enforced by: nothing' docs/`
  lists every one, in the document a reader opens. So nothing is filed.
- **No statement is split, and no marker is added, moved or removed.**
  `settle` §2 lets a statement run across paragraphs up to the next marker
  or heading, so a long statement is valid. The markers are the fold's
  record: a marker added changes the count `fold-check` holds and the
  multiset `test_both_editions_carry_the_same_folds.py` pairs. The line is
  judged against the statement's opening rule (below), which is what makes
  one line per statement honest.
- **No statement's meaning changes**, except by `questions.md` Q1's route.
- **`templates/config.md`'s example block** (`| Fold shape from | 1790154761 |`)
  is a shipped example of the row's shape, not this repository's value, and
  nothing pins it to `seal/config.md`. It stays.
- **`skills/settle/SKILL.md`'s *statements folded before it will not carry
  the line*** is the plugin's general sentence about any repository's
  cutoff, and stays true.
- **Whether each target really enforces its rule is not made mechanical.**
  `fold-check` checks resolution only, by design (`fold_check.py` docstring,
  *What it cannot read*). The builder's record and review audit it.

## What a decision is

This section is the acceptance for item 1. A target that resolves is not
enough; `fold-check` already proves that.

**The line is judged against the statement's bold rule sentence**, not
against every sentence of its grounds. A statement of 183 lines still has
one rule it opens with, and the line names what reads that rule. Extra
targets for a second bold rule inside the same statement are allowed, never
required.

**A target is right when the builder can name the edit that breaks the rule
and the target is what catches that edit.** Name it by kind:

| The rule is about | The right target | Not the right target |
|---|---|---|
| what a shipped script, hook or gate does — it refuses, reports, writes | the test case that plants the violating input and asserts the behaviour, as `tests/<file>.py::<test_name>`; add the function whose refusal *is* the rule where a reader would open it, as the tree already does (`chain_check.py::direct_seal`) | a text pin on the sentence; a module named whole when one case holds the rule |
| the state of this repository's tree — every row escaped, no document over the ceiling | the real-tree case that walks the tree | a planted-fixture case alone |
| what a document or an agent's instruction says — a text a session reads and acts on | the pin on that text | a behaviour case |
| what CI runs at a pull request | the script or case the workflow runs, plus the workflow file where *that CI runs it* is the rule (a path with no `::`) | the workflow file alone for a rule about the script's behaviour |

**Wrong whatever the kind:** a unit found by searching for a word the rule
uses; a case that imports the function but asserts something else; a case
that is skipped or expected to fail; the document itself.

**`nothing — <why>` is the honest answer in four cases, and the reason says
which:**

1. **A person's or a session's act that no file records** — the owner
   squashes, a question is asked in one batch. Reason names the act and
   that review reads it.
2. **Enforced outside the tree** — a GitHub ruleset, a platform setting.
   The reason names where, so a reader can open it.
3. **A record rather than a rule** — a measured run, a design thread's
   history. The reason says so and, where the rule it led to is stated
   elsewhere, names that statement.
4. **A rule a check could hold and none does.** The reason says `no case
   reads it yet` and what would. **A target invented to avoid writing this
   is the failure this work item exists to end.**

In `docs/one-root-by-lifetime.ko.md`, `Enforced by:` and `nothing` stay
English (a checker reads both literally: `fold_check.py#names_targets`), the
targets are byte-identical to the English edition's, and the reason after
`nothing — ` is written in Korean.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The retrofit is complete | Given the finished branch, when `bin/fold-check --shape-from 0` runs, then it exits 0 and reads 136 statements, binds 136 | executed, in phase 7 |
| S2 | The cutoff binds every statement | Given `seal/config.md`, when `bin/fold-check` runs with no flag, then its first line says the cutoff `0` binds 136, and it exits 0 | executed |
| S3 | The prose and the row agree | Given the rewritten first statement, when the prose pin runs, then `test_the_evidence_ledger_states_the_values_the_config_rows_hold` and `test_the_prose_pin_fails_when_either_side_moves_alone` pass | `bin/test tests/test_a_document_has_room_for_the_next_fold.py -q` |
| S4 | Every statement stays bound in CI | Given a later edit that deletes any statement's `Enforced by:` line, when the suite runs, then `test_every_bound_statement_in_docs_has_the_shape` fails naming it | a mutation in phase 7: delete one retrofitted line, see the case red, restore |
| S5 | A target is the one that catches the rule | Given a statement and its target, when the rule is broken by the edit the phase record names, then the target goes red | per phase: every decision's breaking edit and catching unit in `phases/phase-N.md`; at least three per phase executed as mutations, plus every one whose tie the builder could not state in one sentence |
| S6 | Every named test target runs | Given the targets a phase wrote, when their node ids run in one command, then each is collected and passes | `bin/test <node ids> -q`, per phase |
| S7 | The two editions agree on enforcement | Given `one-root-by-lifetime.md` and `.ko.md`, when one edition's `Enforced by:` targets differ from the other's under the same markers, then the editions test fails naming the markers | the new case, shown red first (§15) by editing one planted edition |
| S8 | `nothing` is a reason, not an escape | Given a `nothing` line, when it is read, then its reason says which of the four cases it is | read, by review; `fold-check` only checks the reason is non-empty |
| S9 | No document crosses the ceiling | Given the finished branch, when `bin/fold-check` runs, then 14 documents are held to 1000 lines, 0 listed over | executed |
| S10 | Covered documents still wrap | Given the six covered documents under `docs/`, when `tests/test_docs_line_wrap.py` runs, then every prose line, the bold openings and `nothing — ` lines included, is at most 88 columns | `bin/test tests/test_docs_line_wrap.py -q`, per phase touching one |
| S11 | The ledger is true after the edits | Given the finished branch, when `bin/evidence-check .` runs, then nothing is DRIFTED or BROKEN, and each re-stamped row carries a dated note | executed per phase |

## Data & interfaces

**The line.** One line, at column 0, live (outside any fence, HTML comment
or code span), inside the statement's span — after its markers and before
the next marker, the next heading or the end of the file — and written
last, after the statement's final paragraph. Where the statement ends in a
table, a list or a fence, a blank line goes before it: a plain line directly
after a table row is read as a row by GFM, and after a list item as a lazy
continuation of the item.

```
Enforced by: tests/test_x.py::test_y, skills/a/scripts/b.py::c
Enforced by: nothing — a person's act: the owner squashes; review reads it
```

**Width.** In the six covered documents (`tests/test_docs_line_wrap.py`
`COVERED`: `issues-and-milestones`, `the-evidence-ledger`, `the-broad-gate`,
`measuring-a-run`, `the-agent-set`, `release-checklist`) a line with targets
may be any width (`fold_check.py#enforced_lines`). A `nothing — ` line is
prose and is not exempt: it fits 88 columns with at least one word of its
reason on it, and the reason may continue on the next lines.
`review-chain-spec` and `round-record-spec` are not covered.

**Line budget against the 1000-line ceiling** (read 2026-09-25, `wc -l`):

| Document | Now | Lines added at most | After |
|---|---|---|---|
| `review-chain-spec.md` | 950 | 9 lines + 2 bold openings | ≤ 963 |
| `round-record-spec.md` | 925 | 16 + 2 | ≤ 945 |
| `review-handoff-protocol.md` | 839 | 4 + 3 | ≤ 848 |
| `one-root-by-lifetime.md` / `.ko.md` | 688 / 660 | 9 + 3 each | ≤ 702 / ≤ 674 |
| every other document | ≤ 555 | ≤ 16 + 4 | far under |

A bold opening costs no line where an existing sentence is bolded, and at
most two where one is written before a table or fence, which the column
counts. One line per statement fits every document with at least 37 lines
to spare.

**Ledger rows these edits can drift** (read 2026-09-25). Rows with an
anchor into `docs/`: 43 coordinates in `seal/ledger.md` and
`seal/releases/*.md`, 1 in the stacked fragment. They are listed by
heading, so only the rows whose section holds an edited statement drift, and
`bin/evidence-check .` names them after each phase; the build does not work
from a list. **Three rows anchor a quoted opening line rather than a
heading**, and rewording that line BREAKS them rather than drifting them:

- `seal/releases/0.4.0.md` → `docs/branch-and-release.md#"**The fold refuses while a verified fact has not reached the ledger.** A"`
- `seal/releases/0.8.2.md` → `docs/review-handoff-protocol.md#"- **A runner the repository ships is found, not typed into every prompt.**"`
- `seal/releases/0.8.2.md` → `docs/round-record-spec.md#"**Five values can stand in the reach half, and only the first is a unit"`

A bold-opening edit never rewrites a line a ledger anchor quotes. Before
rewording any line, the build searches the ledger files for it.

Phase 7 edits `tests/test_a_document_has_room_for_the_next_fold.py`'s and
`tests/test_a_folded_statement_names_what_enforces_it.py`'s module docstrings
only, which drift no function-anchored row. It edits
`docs/the-evidence-ledger.md` §*The fold …*, which rows anchored by heading
there may cite; `evidence-check` names them.

**No ledger row per decision.** The `Enforced by:` line is the record of
the decision, in the document itself, and `fold-check` resolves it; a row
restating it would be a second copy. A mutation the builder executed is
recorded in `phases/phase-N.md`. The fragment
`seal/ledger/1790263216-the-older-statements-name-what-enforces-them.md`
takes a row only for a fact the build verified beyond that — expected none,
and the builder decides.

**Siblings in `release: 0.15.3`.** Chains C (#563, #564, #554: the survivor
sweep), D (#568, #501, #569: a ledger row's shape), E (#444, #491, #487,
#220: fences and comment state) and F (#448, #510: the broad gate) run in
parallel, and their subjects sit in `review-chain-spec`,
`the-evidence-ledger` and `the-broad-gate`. They may edit statements this
branch edits, and rename a function this branch names as a target. What
catches the second is `fold-check --shape-from 0` over the merged tree
(phase 7's check, re-run after any merge of the release branch).

## Open questions → questions.md

Answered from the tree and not reopened: the count (115, measured), the
cutoff (lowered to `0`), the bold openings (in scope), splitting (none),
new checks (none), filing for rule-case 4 (none: the line is the record),
the Korean reason (Korean, field English), the edition comparison (in
scope), the template example (stays). The rows that remain are in
`questions.md`.

Framed 2026-09-25 by framer, before the build.
