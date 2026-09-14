# Implementation Plan: the two halves of one generator refuse each other

<!-- seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-14 by the owner, when `smith` was spawned.

## Summary

Five phases, four of them unconditional, cut by the column of
`rounds/round-N.md` each ticket is about. Each phase changes one rule of one
column, states that rule in the documents a reviewer and a fixer read, and
plants a case seen red before the fix.

The order is forced by what each phase leaves for the next. Phase 1 decides
**which rows reach the fix table at all**, so it comes before phase 2, which
decides what those rows may say. Phases 3 and 4 are both `close`'s write pass,
and 3 comes first because 4's derivation reads the verdict words 3 leaves
standing. Phase 5 is conditional on Q3 and is the only one that may not run.

## Technical context

One module carries all of it: `skills/code-review/scripts/round_record.py`,
reachable as `round-record` from `bin/` since `34b556a`. Its sibling
`chain_check.py` holds the vocabulary constants and the arms that read the same
rows at the pull request, so a change on either side is a change to a gate.

The coordinates each phase opens, read at `e387bff`:

| Unit | What it does today |
|---|---|
| `round_record.py#copied_row` · `#table_of` | copies a report row into the record, validating nothing in any cell. The only call site is `table_of` |
| `round_record.py#finding_number` | the one `FINDING_ID_RE.match` site; refuses a non-numeric cell and a duplicate, quoting one row for the first and both for the second |
| `round_record.py#verdict_rows` · `#fix_table` | the only two callers of `finding_number`, both on the `close` path |
| `round_record.py#close` | computes `open_now` from `chain.verdict_of`, refuses a missing row and refuses a row for a finding already closed, then rewrites each row in a single write pass |
| `round_record.py#landing_values` | derives `Fixes checked by` and the surface row from the verdict words; called from both `new` and `close` |
| `chain_check.py#CLOSED_WORDS` · `#FIX_WORDS` · `#HOME_WORDS` · `#verdict_of` | the vocabulary, with two assertions holding the three sets in step at import |
| `chain_check.py`'s fix-surface arm | refuses `none — the fixes are not yet written` beside a `Fixes checked by` naming a later round |

Three constraints the phases inherit rather than choose:

- **One match site.**
  `tests/test_a_finding_id_is_a_bare_integer.py#test_the_rule_is_one_constant_both_tables_read`
  asserts `FINDING_ID_RE.match` occurs once in the module. Phase 1 goes through
  `finding_number` or it turns that case red.
- **The corpus invariant.**
  `#test_the_committed_records_only_lose_a_miscount` asserts that no record the
  old rule read correctly is refused by the new one. Phase 1 widens what is
  accepted, so the invariant holds by direction — but the case has to be re-run
  and its docstring re-read, because it also asserts the rule still has teeth.
- **The vocabulary's assertions.** `chain_check` fails at import if
  `HOME_WORDS` is not inside `CLOSED_WORDS`, or if a deferral becomes a fix
  word. Phase 2 adds to a set that is guarded from three directions.

**What breaks in six months.** The risk this plan accepts is that phase 1
creates a second kind of verdict row and nothing forces a reviewer to write the
right one. A row with no id is a row no fix table can reference, so a reviewer
who forgets an id on a row that **is** an open finding has written a finding
nobody will be asked to close, and `close` will exit 0 over it. That is the one
direction this change fails in, and it is why phase 1 carries the instruction
into `agents/warden.md`, `templates/sdd-round.md` and
`skills/code-review/SKILL.md` in the same commit, and why the acceptance row
for it is *`close` exits 0 and the six rows stand as written* rather than
*`close` exits 0*.

The cheaper mistake is the other direction — a reviewer numbering a
confirmation row costs an inflated count in one record, where a missed finding
costs a defect. Phase 1 states that trade in the pull request body as
`CONTRIBUTING.md`'s **stated failure direction**.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Six tickets, one change, one commit | A case goes red and nothing says which of six rules it was about. `CONTRIBUTING.md` asks for a test seen red **per rule**, and one commit carrying six of them cannot show any of them failing alone | rejected |
| The release notes' grouping — the `—` id, `fixed` outside the tree and the correcting SHA as one vocabulary change | The `—` id would be built in `fix_table`'s verdict branch, where it has no effect: the `#` cell is read by `finding_number` before any verdict word is looked at. The build would ship, the vocabulary would be wider, and the six confirmation rows would still be renumbered by hand | rejected — it is the grouping this frame was drawn to correct |
| #321 answer 1 alone — `new` validates what `close` will refuse | The refusal moves to where the author is, which is worth having, and nothing else changes: the six confirmation rows are still renumbered, the count still reads a six-finding round as twelve rows, and #341 and #353 are untouched. It answers where the message lands, not what the record means | folded into phase 1 as the guard for rows that **do** carry an id, not as the mechanism |
| #321 answer 3 alone — the documents name the rule | A report written before the sentence lands still refuses, and the tree already holds 54 records whose `#` cell carries no digit. Documentation cannot reach a report that is already written, which is the whole of why the refusal lands at the orchestrator | rejected as a mechanism; kept as phase 1's §14 obligation |
| #353 shape 3 — `❓` rows leave the verdict table for a section of their own | It changes what `new` parses out of a reviewer's report, which is the seam the sibling work item of this release just finished at `5bae06e`. Two branches reshaping the report grammar one release apart is how a conformance document goes stale, which is #340 | rejected; scope 1 reaches the same outcome inside the table |
| Widen `chain.SEPARATORS` to strip the backtick (#391 part 2) | That constant is shared with the `deferred` home reader and with `chain_check`'s readers. A home deliberately written as a code span would lose its backticks, and the repair would move the defect one reader over | rejected — the standing `# RIDER:` at `fix_table` says the repair is at the `note` line |
| A migration arm rewriting the 66 deferred rows and the 103 empty spans | A round record asserts a past state, which is what lets it live beside the contract. A row rewritten now asserts a state that was not true at its own `Target SHA`, and `#344` is open about exactly that class | rejected for history; Q6 leaves the question to the phase that meets it |
| Build #323 as a phase | Its answer 1 shipped at `c84f259` and its answer 3 shipped with it. What is left is one sentence in one refusal arm that offers a runnable order | deferred to Q3, as phase 5 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **A verdict row that commissions nothing.** A row with no finding id is copied into the record, never keyed, and never asked for a closure; a row whose verdict reads `❓ out of verified scope` is treated the same way; and a refusal for a malformed id names every offending row rather than the first. The rule is stated in `agents/warden.md`, `templates/sdd-round.md`, `skills/code-review/SKILL.md` and `docs/review-chain-spec.md` §*The finding id* in the same commit (#321 body, #341 body, #353, #303's merged sub-finding) | new cases in `tests/test_a_finding_id_is_a_bare_integer.py` and `tests/test_the_fixes_close_the_record.py`, each seen red at `e387bff` first; `#test_the_committed_records_only_lose_a_miscount` and `#test_the_rule_is_one_constant_both_tables_read` re-run; `tests/test_the_rules_have_one_owner.py` | |
| 2 | **What the fix pass's verdict vocabulary admits.** The fork Q2 answers is built — either `docs/review-chain-spec.md` is corrected to the spelling `agents/smith.md` already carries, or `fix_table` learns the `— corrected at <sha>` suffix and validates the SHA the way `fixed` does. A repair made outside the tree gets a spelling and a document that names it. `already deferred` is settled in the documents rather than in the vocabulary (#341 comment, #321 comment, #273 part 2) | `tests/test_the_rules_have_one_owner.py#test_a_correction_row_closes_answered_and_never_fixed` rewritten to pin one spelling in both documents, seen red against the current pair; a case over `fix_table` per admitted spelling, each seen red | |
| 3 | **What `close` preserves in the Grounds cell.** No verdict word discards a cell it was not asked to change: a `deferred` row keeps the fix pass's prose beside its home, an `answered` row keeps the reviewer's grounds the way a `fixed` row does, and the empty code span at `fix_table`'s `note` line is gone (#391 both halves, and the `answered` branch the ticket does not name) | one parametrised case over the three verdict words, seen red on two of them before the fix; a case asserting the rendered cell for the span, seen red; the 66-row and 103-row counts re-measured over the corpus after | |
| 4 | **`Fixes checked by` after a fix table applies.** The cell stops carrying *the fixes are not yet written* about fixes that are written and named in its own verdict cells, without turning `chain_check`'s fix-surface arm red on the pairing it refuses (#273 part 1) — conditional on Q4 | a case over `close` on a capped run's last record, seen red; `chain_check`'s fix-surface arm run against the same record, both arms; `tests/test_the_last_rounds_fixes_are_checked.py` | |
| 5 | **#323's residue** — the second broad-gate refusal arm names the order that is runnable, and `skills/code-review/orchestration.md` says which side of the last record the gate sits on. Runs only if Q3 says the ticket does not close as covered | `tests/test_broad_gate_rule.py` and `tests/test_the_seal_is_taken_once_by_the_sealer.py`; a case pinning the changed refusal text, seen red | |

**Every phase carries the same four obligations**, because every one of them
changes a gate: a case seen red before the fix
(`skills/agent-contract/SKILL.md` §15), the changed refusal text pinned in the
same commit (§14), the class enumerated rather than the instance fixed (§12),
and the narrow run at the phase boundary rather than the broad one (§2). The
broad gate is the `sealer`'s single act after the rounds settle and belongs to
no phase.

**Each phase writes `phases/phase-N.md` from `templates/sdd-phase.md` when it
closes**, carrying what building it found that this plan could not predict —
in particular, for phase 1, whether a row with no id needs a spelling of its
own in the `#` cell or whether an empty cell is enough.

## Operational impact

- **No migration, no new dependency, no new environment variable.** Nothing
  outside this repository reads the cells being changed.
- **A compatibility break in one direction, and it is the safe one.** Phase 1
  widens what `close` accepts, so every record that closes today still closes.
  Phase 2 may widen or narrow depending on Q2; if it narrows — `fix_table`
  learning a suffix it then validates — the narrowing applies to fix tables
  written after it, never to committed records, because a fix table is an input
  and not a stored artifact.
- **Phase 4 touches a gate on both sides.** `round_record.py` writes the row
  and `chain_check.py` refuses a pairing of it at the pull request. The case
  has to run both arms, or the repair ships a record that its own check will
  not accept — which is the failure `round_record.py#seal`'s docstring records
  paying once already.
- **`CONTRIBUTING.md` §*What a change to a gate must carry* is answered in the
  pull request body**, all four burdens, per phase: the test seen red, the
  failure direction, the prompt budget — which is **zero added interruptions**
  in every phase, since none of these changes puts a question in front of a
  person — and platform honesty, which is *not applicable, no process
  inspection*.
- **Fragments, not shared files.**
  `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/changelog.md`
  and
  `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md`.
