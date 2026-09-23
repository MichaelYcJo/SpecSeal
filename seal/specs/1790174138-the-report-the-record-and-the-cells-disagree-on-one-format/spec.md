# Feature Specification: the report, the record and the cells disagree on one format

<!-- seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Step A of the `release: 0.15.0` milestone. The warden's report, `round_record.py`
and the record's cells have to agree on one format, on the meaning work item 0
(`1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row`)
settles for the two terminal rows. Eight of the nine tickets the milestone
lists are in scope; #159 is deferred, and §Scope says why.

**Everything in this file is `read`.** The framer executed nothing; the
measurements over the record corpus were counts taken with `grep` over the
committed tree at cbb58091, and each one names what it counted.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The finding id — a bare integer, behind an optional severity marker* | The `#` cell has four readings and they are already policy. This work does not add a fifth: it puts the readings in front of the reviewer as example rows, at the place the reviewer copies from |
| `docs/review-chain-spec.md` §*A verdict row that commissions nothing* | The three kinds of no-id row, and the measured shapes (`carried`, `🟢 fix-surface`). The worked carried-closure row (#437) lands here and in the two files the reviewer holds |
| `docs/review-chain-spec.md` §*The record generator* > *What it copies, and what copying costs* | Every fence under `## Paste-ready fixes` reaches the record. A section organised under `###` subheadings currently loses all of them (#505); the clause is the promise this work restores |
| `docs/review-chain-spec.md` §*The bound has a floor, and a quiet round is where it stops*, the `What new prints` table | The `one reopening remains` row's condition, *and the count walk has not already spent a record*, is the sentence #218 measured false. The row is rewritten with the code |
| `docs/review-handoff-protocol.md` §record fields, the `Broad gate` row | The cell is load-bearing: `chain_check.py` reads it on the last record at a ready pull request. #174 changes its shape so that a re-seal keeps the earlier run, and the reader keeps reading the newest |
| `skills/agent-contract/SKILL.md` §2 | The broad gate is one act taken once. A second run is the exception, and the exception is what the cell has no room for today |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | #436 adds a refusal to `chain_check.py`, #217 widens what `evidence-check` reads, #382 changes a cell `chain_check.py` reads. Each carries the four answers in the pull request body |
| `CLAUDE.md` §*The goal a design is chosen against* | Between the two shapes for the `Broad gate` cell, the one that records the second run costs a template line and no question; the one that does not sends the fact to a pull request body nobody parses. Same goal decides against code-span-aware comment parsing: a rule for the reviewer costs one sentence, a parser costs a class of edge cases the tree has declined twice |
| `skills/code-review/SKILL.md` §*Findings format* | Already states the id rule and the no-id row, and the reviewer holds it (`agents/warden.md` lists `code-review` under `skills:`). Two of three reviewers still wrote an empty `#` cell (#503), so the repair is an example where the reviewer copies from, not another rule |
| Work item 0's `plan.md` §Alternatives, *What work item A inherits* items 1–5 | The terminal rows' vocabulary, the one reopening reader, two `Review` answers, `broad-gate.md` as the direct route's whole record, and the pinned gone/stands pairs. Each is restated below where it binds |

## Scope

### In: eight tickets, in four groups

**The reviewer-facing standard — #503, #437, and the comment-opener rule.**
What a report has to look like for `round_record.py new` to accept it first
time, written where the reviewer copies from: `agents/warden.md` §Report's
fenced skeleton, `skills/code-review/SKILL.md` §Findings format, and
`templates/sdd-round.md`'s comment beside the verdict table. The standard is
stated in §*The report standard* below; the documents show it as example rows.

**The generator's reading of the report — #505, #382.** `section_body` ends a
section at the first heading of the same level or above, so a
`## Paste-ready fixes` organised under `###` subheadings carries its fences.
`build` writes the resolved commit into `Target SHA` instead of the revision
as typed.

**The checker's reading of the record — #436, #217.** `chain_check.fix_range`
refuses a `Fix range` still saying the fixes are not yet written once
`Fixes checked by` names a later round, the arm `fix_surface` already runs on
its own rows. `evidence_check.claim_lines` reads the lines after an HTML
comment the record never closes, the way it already reads the lines of a
fence never closed.

**The two cells whose meaning work item 0 settled — #218, #174.** `bound_line`
reports a stopped count walk that already reached two, reading the reopening
question through the reader 0 adds. The `Broad gate` cell holds one entry per
full-suite run, newest first, so a re-seal keeps the run it replaced.

### Out, and why

| Left out | Why |
|---|---|
| **#159** — a record cell corrected in place leaves no trace | Deferred to the release after this one. Its design question has an answer in the tree now that did not exist when it was filed: the ledger's `Corrected <date>` marker and `correction-check --range origin/<base>...HEAD`, which reads the feature branch's history *before* the squash, on every pull request into a release branch (`CLAUDE.md` §*a change writes fragments*). The same shape for round records is a new checker, a template section, a hygiene step and the four gate-change answers, which is a work item of its own. What this work item does take from #159 is its one principle the generator itself violates: `seal` overwrites a landed value. #174's shape ends that for the one cell the generator rewrites (`plan.md` §Alternatives carries the sketch for the rest) |
| Code-span-aware parsing of `<!--` in a report | Declined twice in the tree already: `chain_check.says_none`'s docstring (*inventing a rule about backticks would be the code-span parsing the limits below already decline*) and the rider at `round_record.py#inherited_rows` (*take the whole class or none of it*). The reviewer writes `&lt;!--`; two committed reports already do |
| Refusing `✅` in the `#` cell | `finding_number` admits it today as a row that commissions nothing, the same as a bare `🟢`, and no committed record carries one (`docs/review-chain-spec.md` §*A verdict row that commissions nothing*). The standard says `🟢` is the word; a new refusal for a glyph that already reads correctly is a gate change with nothing red behind it |
| Moving `--target`'s signature, or refusing a revision that is not a full SHA | The refusal for an unresolvable revision already shipped (`round_record.py#build`, *does not resolve in*). A resolvable revision is a legitimate spelling (`tests/test_new_says_when_head_is_not_the_target.py::test_a_target_given_as_a_revision_is_named_by_its_sha`); what changes is what the cell records |
| Dropping `fix_range`'s `says_none` early return | `none` is the honest value of a terminal record; #436 says so itself |
| A third `Review` answer, or a `Ran by` shape for a session as its own reviewer | Work item 0's decision (inheritance item 3). Nothing here adds a cell shape for it |
| A count column in `skills/verify/SKILL.md`'s run-level table | #174's narrow half already made that row ask for what the cell holds. With the cell a list, the row reads the count off the cell; the table's wording moves, the column does not return |
| `bin/round-record` | #382 cites #318 for its absence. It exists at cbb58091 |

### What this work assumes from work item 0's landed code

A is built after 0 squashes into `release/v0.15.0`; the smith rebases first
(`plan.md` phase 1 re-reads before anything is edited).

1. `Needs a fix` and `Loses a record or crashes` take `no`, `no — <why>`,
   `yes — <what>`; a bare `yes` is refused by `round_record.py new` and by
   `chain_check.py`. The report standard below writes the terminal lines
   with the reason as part of the value.
2. `chain_check.py` carries one function answering *does this cell say the
   run reopened* (`True` / `False` / `None`), used by `stopping_floor` and
   `run_reopened`; `round_record.py#bound_line` reads through it. Its name is
   read off the landed code, not off this file. #218's change touches the
   count walk in `floor_and_fixes` and the branch `bound_line` prints from,
   and reintroduces no `== chain.FLOOR_YES`.
3. `broad-gate.md` is the whole record of a `straight to the PR` work item,
   read by `direct_seal` through `broad_gate`. #174's shape applies to both
   homes through the one writer, `round_record.py seal`.
4. The seven sentences 0 rewrites are pinned as gone/stands pairs. This work
   edits neither the declaration table nor the four-combination table; if a
   phase finds it must, the stands half moves with the edit.

## The report standard

What `round_record.py new` accepts, in the order a reviewer writes the report.
Every line of it is a reading of the generator at cbb58091, and the `Verifiable
how` column of §Acceptance says which case executes it.

| Element | The standard | Where the reviewer sees it |
|---|---|---|
| Section headings | `## Verdicts`, `## Executed probes`, `## Deferred`, `## Paste-ready fixes`, spelled exactly. Under `## Paste-ready fixes` and `## Executed probes` the reviewer may group with `###` subheadings, one per finding; the generator takes the fences and nothing else | `agents/warden.md` §Report skeleton |
| The `#` cell of a finding | severity marker, then the bare integer: `🔴 1`, `🟡 2`, `⬜ 3`. A 🔴 or 🟡 without a number is refused. The severity goes in the `#` cell and never at the head of the Finding cell | example rows in the skeleton |
| The `#` cell of a row that commissions nothing | a bare marker or the word: `🟢`, `⬜`, `❓`, `carried`. Never empty — an empty cell is the one shape refused | example rows in the skeleton; `templates/sdd-round.md` comment |
| The marker vocabulary | 🔴 · 🟡 · ⬜ · 🟢 · ❓, the five `skills/code-review/SKILL.md` §Findings format names. `✅` is not one of them; the generator admits it as a no-id row and no document names it, so a reviewer who writes it is writing a sixth vocabulary | the skeleton, one sentence |
| A carried closure (an earlier round's finding this round confirmed closed) | `\| 🟢 \| round N's blocking finding is closed — <what> \| <location> \| confirmed \| <grounds> \|`. Three requirements in one row: a bare marker in `#`; the verdict word `confirmed`, never `fixed` (`chain_check.closed_with_a_fix` reads `FIX_WORDS` across every row, so a carried `fixed` makes the record one that closed on a fix, which the cap refuses); and no 🔴 anywhere in the row (`chain_check.open_blocking` selects on `BLOCKING in "".join(seen)`, every cell) — the inherited severity is written in words | `agents/warden.md` beside *Write that row with no id in its `#` cell*; `skills/code-review/SKILL.md` §Findings format; `docs/review-chain-spec.md` §*A verdict row that commissions nothing* |
| A comment opener | never the literal `<!--` anywhere in the report, a code span included: `swallowed` reads the report with comments stripped, so an opener inside backticks opens a comment and takes the rest of the report with it. Write `&lt;!--` | `agents/warden.md` §Report, one sentence |
| Paste-ready fixes | one fenced block per 🔴 and per 🟡, under `## Paste-ready fixes`, optionally under a `###` per finding. Prose there stays in the report | already stated; the subheading permission is new |
| The two terminal lines | `Needs a fix: no` · `Needs a fix: yes — <the findings that do>` · `Loses a record or crashes: no` · `Loses a record or crashes: yes — <what does>`; a blank line under the pair | already stated; the bare `yes` refusal is 0's |

## User scenarios & acceptance *(mandatory)*

One row per scenario — these become the review's stage-1 checklist and the
regression tests' skeleton. `R1`, `R2`… are round records of one fixture work
item; a row's case lives in the module named, beside the existing cases of its
kind, and is seen red first (contract §15).

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · a subheaded fixes section is carried | Given a report whose `## Paste-ready fixes` holds six `### <n> — <file>` entries each with a fence, when `new` runs, then the record's section carries six fences in the reviewer's order | a case in `tests/test_the_record_is_generated.py` beside `test_two_paste_ready_fixes_stay_apart_and_in_the_reviewers_order`; red at cbb58091 (`no paste-ready fix in the report`) |
| A2 · a section still ends at its own level | Given `## Paste-ready fixes` followed immediately by `## Executed probes`, when `new` runs, then the first section's body is empty and the probes table is read from the second | the existing paste-ready cases stay green; one new case with a `###` under the probes table and a fence under it, carried |
| A3 · the class is every reader of a section's end | `section_body` and the section-end scan inside `swallowed` (`round_record.py`, the `next(... startswith("#") ...)` at the `REPORT_TABLES` loop) both end a section at a heading of the same level or above, or the phase record says why the second must not | read by the reviewer; `phases/phase-2.md` names both |
| A4 · `Target SHA` names a commit | Given `new --target HEAD~1`, when the record is written, then the cell holds the full 40-hex commit `HEAD~1` resolved to, and `chain_check` reports no *row naming a commit* error | the existing `test_a_target_given_as_a_revision_is_named_by_its_sha` extended to pin the cell (its docstring says it deliberately did not); red at cbb58091 |
| A5 · an unresolvable `--target` is still refused | the existing refusal (`does not resolve in`) stays, and its case stays green | `tests/test_the_fixes_close_the_record.py` and `tests/test_chain_check_at_the_pull_request.py` cases naming *does not resolve* executed |
| A6 · `Fix range` cannot stay pending beside a named round | Given a record with `Fixes checked by \| round-2` and `Fix range \| none — the fixes are not yet written`, when `chain_check` runs, then it errors naming `Fix range` on that record, under `RANGE_FROM`'s grandfathering; `none` alone on a terminal record stays accepted, and the pending value beside `nobody — <why>` or `no fixes to check` is untouched | a case in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` or the module that holds `fix_range`'s cases; red at cbb58091 (`fix_range -> ([], [])`) |
| A7 · an unclosed comment silences nothing | Given a `plan.md` of `# p`, a blank line, `<!-- note`, a blank line, and `` `gone_helper` `` in prose, when the records arm runs, then one `NOT-IN-TREE` is reported | a case beside `test_a_fence_the_record_never_closes_does_not_silence_what_follows` in `tests/test_a_record_states_what_the_tree_has.py`; red at cbb58091 (exit 0, `0 names read`) |
| A8 · a closed comment is still an aside | the three existing aside cases stay green | `tests/test_a_record_states_what_the_tree_has.py` executed |
| A9 · a stopped count walk that reached two is reported | Given `R1` floor `no` / needs `no`, `R2` the same, `R3` needs `yes — 🔴 1`, when `new --round 4` prints its bound, then the line is *this record ends the run* naming `round-1.md` and the count `2`, never `one reopening remains`; `chain_check.stopping_floor` errors at `round-1.md` for the same sequence | a case beside the existing `bound_line` cases (`tests/test_a_record_precedes_the_fixes_it_commissions.py` or where 0's phase 2 put A6); red at 0's landed code |
| A10 · the running walk's line is unchanged | Given `R1` floor `no`, `R2` quiet, when `new --round 3` prints, then *this record ends the run … reaches 2 here* as today; and `test_the_floor_record_is_the_earliest_and_not_the_latest` still holds | existing cases executed |
| A11 · the reopening is read through 0's reader | `bound_line` and `floor_and_fixes` carry no `== chain.FLOOR_YES` and no local parse of `Needs a fix` after this work | `grep -n 'FLOOR_YES' skills/code-review/scripts/round_record.py` executed and recorded in `phases/phase-1.md`; the differential of `bound_line` against `stopping_floor` over the sequences #218 enumerated, re-run as a probe and deleted (contract §7) |
| A12 · a re-seal keeps the earlier run | Given a last record whose `Broad gate` reads `<sha1> against <base>`, when `seal --broad-gate '<sha2> against <base>'` runs with `sha2` descending from `Target SHA`, then the cell reads the `sha2` entry first and the `sha1` entry after it, and `chain_check.broad_gate` at a ready pull request reads `sha2` as the run | a case in `tests/test_the_seal_is_taken_once_by_the_sealer.py` beside the seal cases; red at cbb58091 (the cell holds `sha2` alone) |
| A13 · a first seal is byte-identical to today | Given a record at `not yet`, when `seal` runs once, then the cell is exactly `<sha> against <base>` — no separator, no second entry | the existing seal cases executed unchanged |
| A14 · `broad-gate.md` takes the same shape | Given a `straight to the PR` work item already sealed, when `broad-gate --record` re-seals it, then its `broad-gate.md` cell holds both entries and `direct_seal` passes on the newest | a case beside the existing `broad-gate.md` cases; `direct_seal` unchanged |
| A15 · the reviewer's skeleton is a report the generator accepts | Given a report assembled from `agents/warden.md` §Report's own fenced skeleton with its example rows — a `🟡 1` finding, a bare `🟢 … confirmed` carried closure, a `❓` row — and the two terminal lines, when `new` runs, then it exits 0 and the record's verdict table carries the three rows as written | a case in `tests/test_the_record_is_generated.py` that reads the skeleton out of `agents/warden.md` rather than copying it, so the two cannot drift |
| A16 · the three documents say one thing | `agents/warden.md`, `skills/code-review/SKILL.md` §Findings format and `docs/review-chain-spec.md` §*A verdict row that commissions nothing* each carry the worked carried-closure row with `confirmed`, and `agents/warden.md` carries the `&lt;!--` sentence and the five-marker list | a pinning case in the style of `tests/test_a_folded_statement_names_what_enforces_it.py`; red by deleting the row from one file |
| A17 · the exits table matches the code | `docs/review-chain-spec.md`'s `What new prints` table gives `one reopening remains` the condition the code implements after #218 — no earlier floor record's count walk has fired, running or stopped | read by the reviewer; the row is quoted in `phases/phase-1.md` |

## Data & interfaces

**Cells that change what they hold** (`templates/sdd-round.md` is the schema;
every reader named is in `skills/code-review/scripts/chain_check.py` unless
said otherwise):

| Cell | Before | After | Readers |
|---|---|---|---|
| `Target SHA` | `--target` as typed (`HEAD~1` survives) | the resolved 40-hex commit, or the two commits when HEAD moved, as today | `target_shas`, `broad_gate` (descends-from), `written_late`, `close` |
| `Fix range` | pending value never read against `Fixes checked by` | pending value beside `round-N` is an error at or after `RANGE_FROM` (1789621028); no new cutoff — the row has carried the pending value from birth since it shipped, and zero committed records at or after `RANGE_FROM` hold the pair (read: 23 records) | `fix_range` |
| `Broad gate` | one `<sha> against <base>`, replaced by every `seal` | one entry per run, newest first, each `<sha> against <base>`; `seal` writes the new entry in front and keeps what was there; a first seal is the old shape exactly | `broad_gate` reads `SHA_RE.findall(cell)[0]` as the run, so the newest-first order is what keeps its read unchanged; `says_gate_not_yet`; `direct_seal` through `broad_gate` |

The separator between `Broad gate` entries is the work's to choose
(`questions.md` Q4), under three constraints the readers impose: it holds no
`|`, no SHA-shaped word and no `<!--`, and the newest run's SHA stays the
first SHA-shaped word of the cell.

**Readers that change what they read:**

- `round_record.py#section_body`: ends at the first heading whose level is
  the section heading's or shallower. Callers: `table_body`, `fenced_after`.
  The section-end scan inside `swallowed` is the same class (A3).
- `evidence_check.py#claim_lines`: an unclosed HTML comment holds its lines
  and reads them at the end, symmetric with `held`; the ticket's paste-ready
  is the shape, and the name #217 proposes for the held list is
  `aside_held` <!-- NAME NOT IN TREE --> (until phase 3 lands).
- `chain_check.py#fix_range`: a pending arm keyed on `Fixes checked by`
  naming a round, mirrored from `fix_surface`'s `fixes_exist and
  says_not_yet(value)`, before the `says_none` early return.
- `round_record.py#floor_and_fixes` / `#bound_line`: a stopped walk that
  reached two fires with `running = False` and prints the gate's own error
  as the bound; the inner `break` becomes load-bearing (the ticket's ninth
  mutation survivor closes with it).

**Ledger rows this work re-reads or replaces** (`seal/ledger.md`, coordinates
as they stand; a row whose anchor this work removes is REMOVED there and
re-founded in `seal/ledger/1790174138-….md`): R3 and R4 on
`round_record.py#floor_and_fixes` and `#bound_line`; R5 on
`evidence_check.py#claim_lines`; G2 and the `direct_seal` row on
`chain_check.py#broad_gate`; R6 on `chain_check.py#fix_range` and
`round_record.py#close`; R7 on `#says_not_yet` /
`#fix_surface` stays and gains a sibling row for `fix_range`. No row cites
`section_body` or `fenced_after`; those claims are new rows in the fragment.
(The rows' hashes are not repeated here: a stamp in a record is read by
`evidence-check`'s records arm against the tree, and a short path beside one
is refused as a file not found — the frame carried four such stamps, corrected
in phase 1.)

**Documents that describe the `Broad gate` cell** and move with it:
`templates/sdd-round.md` (the cell's comment), `docs/review-handoff-protocol.md`
(the field row), `skills/verify/SKILL.md` (the run-level table row and three
sentences), `agents/sealer.md` (two sentences), `skills/code-review/orchestration.md`
(§*The last record's `Broad gate` cell is read at a READY pull request* and the
refusal paragraph), `docs/review-chain-spec.md` (three mentions), and the
comment `new_broad_gate_file` writes into `broad-gate.md`.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline. The
judgments the tickets left open and this frame took are listed at the head of
that file; the residue is seven rows, one for a person and the rest for a
measurement or the work.

Framed 2026-09-23 by framer, before the build.
