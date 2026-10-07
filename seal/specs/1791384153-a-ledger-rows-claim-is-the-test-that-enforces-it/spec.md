# Feature Specification: a ledger row's claim is the test that enforces it

<!-- seal/specs/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate.
Issue #836 and its reopen comment. Record language: English (seal/config.md
has no `Record language` row). Every coordinate below was opened by the
framer at 5623d728 (0.20.0 as shipped) unless it says otherwise; every count
is labelled with how it was taken. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | A coordinate is `path#major[>minor]@hash`, it degrades to DRIFTED and never to BROKEN below the major level, and a row with no coordinate cites nothing. This work adds a second row form beside that one and changes nothing in it: a row held by a test carries no hash, so nothing in it can drift |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | A `Corrected ·` row supersedes the family of the row it cites, whose coordinates are not checked again, and starts a family of its own; a released row is never removed. That is the whole migration mechanism (D5): a `Corrected ·` row whose grounds hold the citation and the test, and no code coordinate, is a family nothing can drift. No new verb and no new reader is needed to supersede |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file*; `templates/config.md` §*The ledger freeze* | A released file never changes, so no released row is rewritten into the new form. Every row this work writes goes to `seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md` |
| `skills/settle/SKILL.md` §*2. Write one standing statement per segment* (the `Enforced by:` line) and `skills/settle/scripts/fold_check.py#target_problem` | The grammar `path::name` and its resolution — the file exists, `::name` is a `def` or `class` in it — already exist for a folded statement. This work gives a ledger row the same grammar and gives the two readers one resolver (D6). The issue's sentence *`Enforced by:` already names that test* is this clause |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `evidence-check` is a gate: the broad gate runs it with `--strict`, CI's evidence job runs it, and the post-commit advisor prints it. Each verdict this work changes carries a case seen red (§*Scenarios*), a failure direction (§*What drifting means*: every new refusal blocks more), and a prompt budget of zero — nothing here asks a person anything |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | A row held by a test is verified by the suite with nobody at the keyboard. A hashed row is verified by a person re-reading the claim, and #834 part 7 measured that reading at 84 % of the rows landed since 0.18.0. Between the two forms, this goal decides |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Each defect is fixed across its class; every changed sentence a person reads is pinned in the same commit; every new case is seen red before it is committed |
| #834's inventory, part 7 (`seal/specs/1791382684-every-reader-and-record-is-inventoried/inventory/7-records.md`, read on the `chore/834-…` branch) and the framer brief's three rules | The input is owned (pytest's own node-id spelling), the unknown is refused (a mixed row, a name no test runner collects, a method not spelled the way pytest spells it), and what goes is named (D6: `fold_check.py`'s own `ast.walk` resolver) |

## What the inventory measured, re-read for this frame

Every number here is `read` from part 7 or re-derived by the framer with the
command beside it, at 5623d728. None was executed as a test.

- **84 % of the ledger rows landed since 0.18.0 are bookkeeping.** Of 993
  rows in `seal/releases/0.18.1.md` through `0.20.0.md`, 712 are `Re-read ·`
  and 123 `Corrected ·`; 158 are new claims (part 7, footnote [d]).
- **A re-read re-triggers itself.** A `Re-read ·` row is anchored on the
  unit it re-read, so the next edit to that unit drifts the family again.
  `evidence_check.py#reverify` is cited by 84 bookkeeping rows and 21 claim
  rows; `templates/config.md#"## Broad gate"` by 57 coordinates in all
  (part 7 §*Observations*; re-derived: `grep -c 'evidence_check.py#reverify@'`
  over the claim rows of every released file → 21).
- **The claims already name their tests.** Of 1,308 claim rows in
  `seal/ledger.md` and `seal/releases/*.md` (rows that are neither
  `Re-read ·` nor `Corrected ·`), 1,048 cite a `tests/*.py#<unit>@<hash>`
  coordinate, and 139 cite nothing but test units (framer's count, a
  `re.split` on unescaped pipes over the Code grounds cell). So for most rows
  the test that holds the claim is already in the row — as a hash that drifts
  whenever the test is edited.
- **The cheapest record drifts nothing by construction.** `# RIDER:` comments
  share the ledger's anchor and hash with no families and no freeze: 20 at
  0.18.0, 20 now, 0 drifted (part 7 row 11). What they show is not that a
  hash is cheap — a rider's drift is the rider firing, which is its purpose —
  but that a record whose purpose is served by one stamp costs one stamp. A
  ledger row's purpose is the claim holding, and the instrument for that is
  a test, not a reading.
- **`Enforced by:` is held by name only and has cost nothing.** 451 targets
  under `docs/` (framer's count: every comma-separated target on an
  `Enforced by:` line that is not `nothing`): 431 are a top-level `def` or
  `class` with a unique name, 20 name a file alone, 24 name a unit that is
  not a test (`fold_check.py::bound` and the like), 0 are nested, 0 are
  missing. Zero issues since 0.18.0 are about it (part 7, the by-mechanism
  table).
- **The `path::name` spelling already appears in 16 claim rows, and in no
  Code grounds cell.** 9 sit in Verified behavior and 7 in Notes (framer's
  count). D3's reading of the grounds cell alone therefore changes no
  existing row's verdict.

## Scope

**In.** Eight decisions, each from the tree.

**D1. A second row form: the claim is held by a test.** A ledger row's Code
grounds cell may hold, instead of coordinates, one or more test node ids in
pytest's own spelling — `tests/test_x.py::test_y` for a function,
`tests/test_x.py::TestA::test_b` for a method — each in backticks, comma
separated, and nothing else. The Clause is then a description that nothing
holds to the code, which is what the issue asks for and what `Enforced by:`
already is under `docs/`. The Verified behavior cell holds how the test was
seen red (`skills/agent-contract/SKILL.md` §15), and Checked holds the date
it was seen red then green. The row's claim is the test passing. A hashed
row is still written for a claim no test holds.

**D2. What the checker reads of such a row, and what it says.** Each node id
is resolved through `evidence_check.py#resolve_unit`'s Python branch: the
path is a `.py` file in a checkout the run reads, and the name — the parts
after the path, joined with `.`, which is the qualified name `py_spans`
already keys on — is a `def` or `class` there. It is **OK** when it resolves
to one unit whose name pytest collects by default (a function beginning
`test`, a class beginning `Test`); **BROKEN** when the file or the unit is
not there, naming which, and for a method written bare (`path::test_b` where
`test_b` lives only inside a class) saying that a method is spelled
`path::Class::method`; **MALFORMED** when the token parses but names a unit
no test runner collects, with a remedy naming the two forms. It is never
DRIFTED: there is no hash. A resolved node id counts among `ok` on the
totals line; nothing new is printed there.

**D3. Where it is read: the Code grounds cell, and nowhere else.** The node
ids are read per row through `grounds_cells`, the one table walk, never over
the whole body the way `ANCHOR_RE` is read, because `a::b` is a spelling
prose uses — a C++ scope, a Rust path, a quoted `Enforced by:` line — and a
coordinate is unambiguous by its `#…@hex` shape where a node id is not. The
16 tokens that already sit in Verified behavior and Notes stay prose.

**D4. A row is one form or the other.** A Code grounds cell holding both a
node id and a code coordinate — any `ANCHOR_RE` match other than a citing
row's citation — is MALFORMED, with a remedy naming the two forms. Allowing
the mix would let a row say *held by a test* while still owing a re-read on
every edit, which is the half-form that keeps the bookkeeping while looking
migrated. A grounds cell holding node ids and no coordinate is no longer the
*cites no coordinate* MALFORMED of `malformed_rows`. The citation a
`Corrected ·` or `Re-read ·` row opens with is a ledger line, not code, and
is not a coordinate for this rule — `family_view` already grades it apart.

**D5. A released row migrates by one `Corrected ·` row, on demand, and
never in bulk by a feature branch.** Under the freeze a released row is
never edited. Its claim moves onto its test by a `Corrected ·` row in the
branch's fragment whose grounds hold the citation and the node ids and no
code coordinate, and whose Notes carry `Corrected <date> by work item <id>:
held by its test from here on`. Nothing in the checker changes for this to
work: `family_view` supersedes the cited family (its coordinates are not
checked again), and the correcting row's own family carries no code
coordinate, so no later edit drifts it. It is written by the branch whose
edit drifted the row, at the moment `--reverify --into` would otherwise
write a `Re-read ·` row for it, and the smith chooses per row by reading: a
claim the cited test holds takes the `Corrected ·` test row; a claim no test
holds takes the `Re-read ·` row as today. `--reverify --into` names the
option once per run, in its summary line, unconditionally — it does not
guess which test holds a claim. A bulk pass over the 1,042 released rows
that cite a test is a person's decision (`questions.md` Q1), and its
vehicle, if taken, is a fold fragment at a release
(`docs/the-evidence-ledger.md` §*A fold is not a work item*), because two
feature branches correcting one released row in one release are each
DRIFTED at the fold by the existing rule.

**D6. One reader for `path::name`, and `fold_check.py`'s own goes.**
`fold_check.py#target_problem` loads `evidence_check.py` the way it already
loads `unverified_check.py` and `hooks/config.py` through `fold_check.py#load`,
and asks it to resolve the target. Its own `ast.walk` resolver is removed:
that is the copy this frame names as going. What each caller accepts stays
the caller's: `fold-check` accepts a file alone, any `def` or `class`, as
it does today (the 451 targets resolve exactly as before — 0 are nested,
so the move from `ast.walk` to `py_spans`'s top-level and qualified names
changes no answer); the ledger accepts a test. Grammar and resolution are
one function; acceptance is one line in each caller.

**D7. The documents.** A new section in `docs/the-evidence-ledger.md`, placed
after §*A released row is read again in the branch's fragment* and before
§*What the checker refuses*, so that no existing section's region changes
(`heading_path` ends a region at the next heading of its level or higher;
inserting a section between two leaves both regions byte-identical — 9 and
3 released rows cite the two neighbouring sections). It states D1–D5 as the
rule, with `Enforced by:` lines naming the cases. `templates/ledger.md` shows
both row forms. `skills/evidence-check/SKILL.md` §*Verdicts and what to do*
gains the test row's verdicts and §*Re-verifying is recomputing the hash*
says what the run leaves alone (4 and 2 released rows cite those sections;
the re-reads are this item's). `skills/evidence-ci/SKILL.md` §*Updating
later* says that an older vendored copy refuses a test row as MALFORMED, so
a repository updates the copy before writing one, and that the step reads
whether the test exists while the repository's own test job judges whether
it passes.

**D8. This item's own records are the first test rows.** Its fragment holds
a test row per scenario below. The released rows its edits drift
(`evidence_check.py#malformed_rows`, `#grounds_cells`, `#malformed_remedy`,
`#check_ledger`, `#reverify_into`, `fold_check.py#target_problem`, and the
two skill sections — 2, 3, 1, 0, 6, 2, 4 and 2 claim rows at 5623d728, the
bookkeeping rows citing them on top) get, per row, the `Corrected ·` test
row or the `Re-read ·` row of D5, chosen by reading (`questions.md` Q3).

**Out, each with its grounds.**

| Cut | Grounds |
|---|---|
| A hash-less code pointer beside the test (`path#unit` with no `@hash`) | A grammar change: `ANCHOR_RE` requires the hash, `refused_coordinate` names a bare `path#unit` MALFORMED today, and the coordinate grammar's five copies are #867's. A pointer that only resolves would also be bookkeeping again: a rename breaks it and owes a `Corrected ·` row. The test names the code it reads, which is one hop |
| A third citing verb (`Held ·`) | `Corrected ·` already supersedes a family, and its readers — `correction_check.py#dropped_corrections`, `survivor_check.py#corrected`, `settle.py#anchored_rows`, `family_view` — stay unchanged. A new verb is a new copy of the supersede judgment in each of them, which #834's brief refuses |
| `evidence-check` running the named tests | The post-commit advisor runs the checker in about 1.7 s; a run that spawns pytest is a different tool. The suite judges a test; the broad gate here runs `bin/test -q` and `--strict` together, and a consuming repository's test job does the same |
| A bulk re-homing of the released rows | `questions.md` Q1; D5 says why a feature branch never does it |
| Reading pytest's naming configuration (`python_functions`, `python_classes`) | Reading a config to decide what is a test is a guess from text this checker does not own; the default names are pytest's own. A repository with other names writes a hashed row, and the new section says so as a known limit. This repository declares no override (read: `pyproject.toml`) |
| A parametrised node id (`::test_y[case]`) | Not a `def`; the row names the function |
| `CONTRIBUTING.md` §*House rules*, `seal/README.md`, `CLAUDE.md` | Each links to `docs/the-evidence-ledger.md` as the home and states no rule this changes; 6 and 2 released rows cite the first two, and an edit would drift them for nothing |
| `correction_check.py`, `settle.py`, `rider_check.py`, `survivor_check.py`, `fold_ledger.py` | None reads a node id; a `Corrected ·` row holding one is to each of them what one holding prose is. The coordinate grammar copies in the first three are #867's |
| The totals line gaining a word (`N held by tests`) | A new word on a line two wrappers and the CI job read is a change to what a gate prints with no reader asking for it; `grep -c '::'` over the ledgers is the count |
| `hooks/evidence-advisor.py` | It prints the checker's output. Whether it carries a repair sentence of its own that must learn the form is `questions.md` Q4, the work's |

## What drifting means after this work

The failure direction of every new verdict is *blocks more*: a MALFORMED or
BROKEN finding where today's checker finds nothing, at exit 1 leniently and
2 under `--strict` for MALFORMED, and 2 either way for BROKEN, as
`exit_code` already grades them. No new verdict reads a mixed, mis-spelled
or non-test row as OK.

| | A hashed row (today's form, unchanged) | A row held by a test (D1) |
|---|---|---|
| OK | every coordinate's hash matches its unit, or a newer reading in its family holds it | every node id resolves to one test |
| DRIFTED | a cited unit changed; a person re-reads the claim | never — there is no hash |
| BROKEN | a unit or file is gone; a `Corrected ·` row re-points or retires | a test or file is gone, or a method is spelled bare; a `Corrected ·` row re-points |
| MALFORMED | a coordinate nothing parses, or a grounds cell citing nothing | a node id naming a unit no test runner collects, or a row mixing the two forms |
| The claim turning false | found by a person re-reading after a drift, or by a review round | found by the suite: the test is red. The prose may lag the test, as an `Enforced by:` sentence may; review reads it |
| `--reverify` | re-stamps a drifted hash; `--checked` dates the row | writes nothing, dates nothing; leaves a BROKEN node id named |
| `--reverify --into` under the freeze | writes a `Re-read ·` row per drifted released row | writes none for a superseded family; its summary names the `Corrected ·` test row as the other repair |
| The fold | moves the row whole | moves the row whole |
| A consuming repository with no node id in its ledger | every finding identical before and after (S11) | — |
| A consuming repository whose vendored copy predates this | — | reads a test row as MALFORMED, *cites no coordinate*; `skills/evidence-ci/SKILL.md` says to update the copy first |

## User scenarios & acceptance *(mandatory)*

Each scenario is a case seen red before it is committed. *Verifiable how*
names the module by its purpose; the build names the file.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | A test row resolves | Given a fragment row whose grounds hold one backticked node id naming a top-level `test_` function that exists, when `evidence-check` runs, then the row is OK, counted among `ok`, exit 0 | the new module, red against the unfixed checker, which names the row MALFORMED *cites no coordinate* |
| S2 | A renamed test breaks the row | Given S1 with the function renamed, then the finding is BROKEN naming the file and the missing name, exit 2 | the new module |
| S3 | A method is spelled pytest's way | Given a node id `path::TestA::test_b` for a method, then it resolves; given `path::test_b` for the same method, then BROKEN, and the detail says a method is written `path::Class::method` | the new module |
| S4 | A unit no test runner collects | Given a node id naming a `def helper`, then MALFORMED with a remedy naming the case and the hashed form | the new module |
| S5 | A mixed row is refused | Given a grounds cell holding a node id and a `path#unit@hash`, then MALFORMED naming both forms; given a `Corrected ·` row holding its citation and a node id, then not | the new module |
| S6 | A node id outside the grounds cell is prose | Given `path::name` in Verified behavior or Notes beside a hashed grounds cell, then no finding about it | the new module, over a fixture copying one of the 16 existing shapes |
| S7 | A migrated released row never drifts again | Given a released row citing a unit, a `Corrected ·` row in a fragment with the citation and a node id, and an edit to that unit, when `evidence-check --strict` and `--reverify --into` run, then no finding names the released row and no `Re-read ·` row is written; the correcting row is OK | `tests/test_a_released_row_is_read_again_in_a_fragment.py`, red when the superseding is removed from `family_view` |
| S8 | `--reverify` leaves a test row alone | Given a test row and `--reverify --checked <date>`, then the row's text and date are unchanged; given a BROKEN node id, then a `left` line names it | the new module |
| S9 | The summary names the other repair | Given `--reverify --into` writing at least one `Re-read ·` row, then its summary says once that a `Corrected ·` row naming the test that holds a claim retires its hashes | the new module, pinned on the sentence |
| S10 | One resolver for `Enforced by:` | Given `fold-check` over `docs/`, then every one of the 451 targets resolves as before; given a doc target `path::TestA::test_b`, then it resolves; given `fold_check.py` with its `ast.walk` branch, then the suite is red | `tests/test_a_folded_statement_names_what_enforces_it.py`, its pins updated in the same commit |
| S11 | A ledger with no node id is unchanged | Given a fixture ledger of hashed rows, citing rows and a fenced example, then the findings before and after this work are identical, line for line | the new module, over the fixture the existing cases already use |
| S12 | The vendored copy reads it alone | Given the checker copied alone into `tools/`, then S1–S5 hold there | `tests/test_evidence_check.py`'s `vendored_copy` fixture |
| S13 | The documents state it and are pinned | Given the new section, then its `Enforced by:` lines name S1–S9's cases and `fold-check` is green; given `templates/ledger.md`, then both forms are shown; given `skills/evidence-ci/SKILL.md`, then the update sentence is there | `fold-check`; a pin per changed sentence |
| S14 | This item's ledger is the first | Given the fragment, then every row of it is a test row or a citing row; `evidence-check --strict .` is 0 drifted at the head; every released row an edit drifted has a citing row | `evidence-check --strict .`, executed by the build and the sealer |

## Data & interfaces

- **The token.** `path::name(::name)*` inside backticks in a Code grounds
  cell, `path` ending `.py`. The parts after the path, joined with `.`, are
  the qualified name looked up in `py_spans`. This is `fold_check.py`'s
  grammar extended by pytest's own nesting; no new regular expression for a
  coordinate is added anywhere, and `ANCHOR_RE` is not touched.
- **The findings.** The same `(status, coordinate, detail)` triples
  `check_ledger` returns, with the node id in the coordinate slot. Statuses:
  OK, BROKEN, MALFORMED. `exit_code` is unchanged.
- **One sentence** in `--reverify --into`'s summary, printed once per run
  that writes a `Re-read ·` row, pinned.
- **`fold_check.py`** gains a loader constant for `evidence_check.py` beside
  its three existing ones and loses the body of its resolver.

## The seam with the sibling frames

- **#867 (the coordinate grammar's five copies).** This work adds no
  coordinate grammar and edits no copy: `ANCHOR_RE`, `correction_check.py`'s
  `ANCHOR` and `CITATION`, `settle.py`'s `COORDINATE_RE` and
  `rider_check.py`'s stamp are untouched. The node id is a different token,
  read in one new function in `evidence_check.py` through the existing table
  walk. If #867 moves `grounds_cells` or `ledger_table_rows`, phase 1
  rebases one call site; if it lands second, it finds one more caller of the
  walk and no second reader of a coordinate.
- **#870 (`generic_units`).** D2 resolves through `resolve_unit`'s Python
  branch only, which calls `py_spans`; the non-Python branch is #870's and
  is never reached by a node id, because a token whose path is not `.py` is
  refused before resolution.
- **`evidence_check.py` units this work changes:** `malformed_rows`,
  `malformed_remedy`, `check_ledger`, `reverify_into` (one sentence), and
  one new function with its constants. **Units it reads and does not
  change:** `resolve_unit`, `py_spans`, `grounds_cells`, `family_view`,
  `judge`, `classify`, `exit_code`. `fold_check.py`: `target_problem` and a
  loader constant.

## Judgments the tree answered

Listed so nobody reopens them; each is overturnable by opening what is named.

1. *Test alone, or test plus a code anchor?* Test alone — the Out table's
   first row.
2. *Which verb migrates a released row?* `Corrected ·` — the Out table's
   second row, and D5.
3. *May a row mix the forms?* No — D4.
4. *Does the checker run the test?* No — the Out table's third row.
5. *Any `def`, or a test?* A test, by pytest's default names — D2 and the
   Out table's fifth row. A row naming a unit that merely exists is a claim
   nothing holds, which is what *cites no coordinate* already refuses.
6. *Does a new section or an edit carry the rule?* A new section, inserted
   where it drifts no neighbour — D7, with the counts.
7. *Does the ledger's reader or `fold_check.py`'s become the one?*
   `evidence_check.py`'s, because `evidence-ci` ships it alone and
   `fold_check.py` already loads its readers — D6.

## Open questions → questions.md

Four rows: one a person's (the bulk pass, which does not block the build),
two measurements, one the work's.

Framed 2026-10-07 by framer, before the build.
