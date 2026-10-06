# Implementation Plan: a fix of a fix twice sends the chain back to its framer

<!-- seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.
Approved 2026-10-06 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned for the redesign after round 3.

## Summary

Four vertical slices. The reading first, because everything else reads what
it writes: `round_record.py new` derives a `Fix of a fix` row from the
previous record's `Fix range` and `New units` and the report's open
`Location`s, prints the stop at the second landing, and refuses a record
after an unreframed `second`. Then the gate: `chain_check.py` reads the row on
every record behind `REFRAME_FROM`, counts per run, and holds a record after a
`second` to a `Reframed … after round <N>` line at `spec.md`'s foot; the
floor's walks stop at the boundary. Then the owner and the carriers — the
rule stated once in `skills/code-review/orchestration.md`, linked from
everywhere else, the acts table and the one-owner test grown. Last the
fragments, the re-reads of released rows the moved anchors owe, and the
executed replay of the two 0.18.3 chains.

**Reframed after round 3.** The run stopped at its own rule: rounds 2 and 3
each found their finding inside what the previous fix pass had written to
decide, from the prose of a `Location` cell, when a backticked name is a
mention rather than a place. Phases 5 and 6 remove that reading instead of
narrowing it a fourth time — a landing needs a `.py` path — and bring the
records with it. `spec.md` §*What round 3 moved* holds the three rounds'
table and the measurement of what the narrowing loses.

## Technical context

**Where the pieces already are.** `skills/code-review/scripts/round_record.py`:
`location_units` resolves a `Location` cell to `(path, unit)` against a tree
(`path:line` through `parse_module` + `enclosing_unit`; `path#unit`,
`path::unit`, backticked and bare identifiers); `measure(reader, root, a, b,
paths)` parses both ends of a range and returns `at_a`/`at_b` as
`{path: {unit: (contract, first, last)}}`; `top_units` keeps line spans but
not the node, so the AST comparison needs the node or `ast.dump` kept per
unit; `verdict_rows`/`build` already hold the report's keyed rows and
`open_rows`; `earlier_records` lists `round-K.md` below N; `floor_and_fixes`
and `bound_line` print the run's bound at `new`; `units_named_earlier` reads
`New units` and carries a `RIDER` about `chain.EMPHASIS` stripping
underscores from unit names — the new reader strips emphasis at the ends of
an entry only, and does not inherit that bug. `skills/code-review/scripts/chain_check.py`:
`stopping_floor(reader, root, rel, later)` takes the later records from
`main`'s `records[index + 1:]`; `fix_surface` is the model for an arm with an
absent-row cutoff and a malformed-fails-always split; `frame_mark` reads the
LAST non-empty line of `spec.md` through `MARK_RE`, and `frame` compares
`<who>` with `routing.md`'s `Planning` row; `item_began` keys every cutoff;
`CAPPED_EXIT` is the one spelling of an exit a refusal names;
`closed_with_a_fix`/`FIX_WORDS` is how a record is known to have written
fixes.

**The measured instances**, read from the committed records and git at the
pull request heads (2026-10-06, this clone):

| Chain | Round K-1's fix range touched | Round K's open finding landed in | Reading |
|---|---|---|---|
| #814 (`1791180640`) | r1 `165a6ca8..36e5fb46`: `compare_at_base`, `proof_refused`, `MULTI_RUNNER` | r2 🔴 1 `broad_gate.py:2362` → `compare_at_base`; 🟡 2 `:2035` → `proof_refused` | `first` at round 2 |
| | r2 `275cd1a0..d9ce4e1a`: `compare_at_base`, `proof_refused`, … | r3 🟡 1 `broad_gate.py:2058` → `proof_refused` | `second` at round 3 — the record that filed #815, which begot #816 |
| #801 (`1791163980`) | r1 `fa8a5c3c..b5dbc88c`: `reverify`, `left_alone` | r2 🟡 1 `evidence_check.py:3596` → `reverify` | `first` at round 2 |
| | r2 `930078de..4d510880`: `reverify` | r3 🟡 1 `evidence_check.py:3599` → `reverify` | `second` at round 3 — the record that filed #808, which begot #809 |

**What the three rounds left in the tree** (read at `9c32e7f6`). `landings`
(`round_record.py:2396`) filters the pairs `location_units` returns to the
path-placed ones only when `names_a_file` says the cell names a tracked file
(`:2474`), and otherwise lands a bare name where `range_carriers` finds exactly
one touched Python file defining it (`:2484`). `location_units` (`:4015`)
returns `(None, unit)` for an `IDENTIFIER_RE` or `BARE_IDENTIFIER_RE` match,
and `close`'s depth walk reads the same function. `CELL_WORD_RE`,
`PATH_TAIL_RE`, `names_a_file` and `range_carriers` have no caller outside
`landings`; `TRACKED_FILES` has none outside two of the four bare-name cases.
The ledger fragment anchors no row on `names_a_file` or `range_carriers` — A1
names them in its claim text — and anchors one row each on the four
bare-name cases. `docs/round-record-spec.md` is at 994 lines of the same
1000-line ceiling, so the sentence phase 5 rewrites there has to shrink or
hold its length.

**Constraints.** `docs/review-chain-spec.md` is at 999 of a 1000-line ceiling
with no exemption, so it cannot own the rule and takes a link of at most three
lines. `templates/sdd-spec.md` is pinned to END with the `Framed` line
(`tests/test_chain_check_at_the_pull_request.py`), so the `Reframed` line is
never in the template and `frame_mark` has to accept a foot block rather than
one line. `tests/test_the_pull_request_language_is_the_repositorys.py#_literal_strings`
lists the checker constants the governs list must carry by hand, so the new
labels are added there as well as in `templates/config.md`.
`conftest.cutoff_item_is_traceable` requires `REFRAME_FROM` to name a work
item directory under `seal/specs/` or a fold marker in `docs/`, which this
item's own id satisfies. `reach_back` sets the previous record's `Fixes
checked by` to `round-N` when `new` writes round N; phase 2 reads what it does
to a previous record reading `no fixes to check`, because the redesign's first
record follows exactly such a record (`questions.md` Q3).

**What breaks in six months.** The grain is the top-level unit. A repository
whose functions are long will see `first` more often than the ticket's two
chains suggest, and a run that writes `second` because two unrelated findings
fell in one 600-line function spends a framer segment on a redesign nobody
needed. The row names the unit, so the reader can see it happened; the trade
is recorded under Alternatives so it can be overturned with the measurement
`questions.md` Q1 asks for.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. The orchestrator judges a fix-of-a-fix from the report | It is the one participant who would have to notice, and it noticed once in four chances (#804 by hand; not #814, #801). A judgment nobody counts fires when somebody is awake | Rejected — the ticket's own ask, and `CLAUDE.md`'s first goal |
| B. A `Changed units` row written by `close`, read by `new` | A second statement of what the `Fix range` already says; after a squash the checker could re-verify neither; one more template row, protocol row and arm to keep in step | Rejected — `new` runs where `close` ran, so the range's ends resolve and the units are derived when needed. The `Fix of a fix` row names the unit and the round, which is what a reader opens |
| C. Hunk-level overlap: the finding's line inside a hunk the range changed | Needs the diff at read time; CI has it only through pull request heads and a squash removes it; a `Location` with no line (`path#unit`) has no hunk to meet | Rejected — the unit is the grain `New units` and the ledger already use, and it fired correctly on both chains |
| D. Any earlier fix pass of the run, not only the previous | Round K-2's units that round K-1 left alone were read by round K-1; a finding there is K-1's miss, which the verifying round's rules already answer. Counting it inflates `first` on long runs | Rejected — the ticket says *the previous fix pass*, and the reason holds |
| E. Mark the reframe in the stopping record (a cell `new` fills later) | A record is written once and corrected in place; a cell filled by a later act is the shape `Fixes checked by` already has, and that cell is set by the NEXT record's `new`. Here the next record is the thing being permitted, so the permit cannot live in it or in the record before it | Rejected — the permit is the framer's write, and the framer writes `spec.md`. The `Reframed` line sits where the `Framed` line already proves a framer ran |
| F. Three landings, matching the 3+ Fix Rule's count | Both chains in the ticket filed their third fix as an issue (#815, #808) and each begot another (#816, #809). A third fix pass is the cost the rule exists to spend on a redesign instead | Rejected — two: the first is the signal, the second the confirmation. The relation to the 3+ Fix Rule is stated at the owner |
| G. Stop the run `capped` at the second landing and file the findings | Capped is the reopening bound's exit, and it files findings where nobody schedules from. The ticket's point is that the frame is not reopened; filing reopens nothing | Rejected — the exit is the framer, and the run continues after the redesign in the same work item |
| **H. The chosen approach** — `new` derives a `Fix of a fix` row per record from the previous `Fix range` and `New units`; the second landing in a run stops the fix passes, closes the record on `deferred the frame`, and the framer is spawned with the records as input; a `Reframed … after round <N>` line at `spec.md`'s foot permits the records after; `chain_check.py` counts the declared rows per run and holds the resumption to the line | The grain (above). And a `first` that was really a `second` — the generator miscounting because a record between was hand-edited — is caught by the gate's count, which reads the rows as written | **Chosen** |

**After round 3**, on the one question the run could not close — when a
backticked name in a `Location` cell is the finding's place:

| Approach | Failure scenario | Verdict |
|---|---|---|
| I. Round 3's paste-ready fix: a basename the tree holds twice, an untracked path ending in an extension and a quoted path each count as a file | A fourth prose heuristic. The next shape — a directory, a path in angle brackets, a path broken across a wrapped line — is one round away, and `docs/round-record-spec.md` §*The depth in `New units`* already declines the enumeration | Rejected — it is the third fix pass the rule exists to stop |
| J. Keep the bare-name reading for a cell that is one bare identifier and nothing else | Still a reading of prose, one shape narrower; it keeps `range_carriers` and the one-file rule round 2 found wrong; and no fix-owing row at `v0.18.1`, `v0.18.2`, `v0.18.3` or this branch has that shape | Rejected — it saves nothing measured and keeps the mechanism |
| K. `new` refuses a record whose open owing row has no path | A wall at the keyboard for a reviewer's prose, a prompt budget the frame set at zero, and a refusal of a record correct by every other rule | Rejected — `agents/warden.md` is told to write the path, and the row reads `no` |
| **L. The reframe's approach** — a landing needs a `.py` path: `landings` keeps only the path-placed pairs `location_units` returns, and the units rounds 1 and 2 added to decide the rest leave the tree | A reviewer who locates a finding by bare name alone is not counted. Measured by reading the records: no such fix-owing row at the three later tags and this branch, at most seven cells at `v0.18.0`; `questions.md` Q6 confirms by replay | **Chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The reading and the row.** `chain_check.py` constants `FIX_OF_A_FIX`, `FOF_NO`/`FOF_FIRST`/`FOF_SECOND`, `REFRAME_FROM`, `REFRAME_RE`, `fix_of_a_fix_count`; `round_record.py`: `top_units` keeps enough of each node to compare ASTs between ends; `landings(...)` derives the row from the previous record's `Fix range` and `New units` and the report's open rows at the target, refusing an unresolvable range; `build` writes the row between `New units` and `Needs a fix`; `new` prints the stop line on `second` and refuses a record after an unreframed `second`; `templates/sdd-round.md` gets the field row; `docs/round-record-spec.md` gets §*A fix of a fix — `Fix of a fix`* in the shape of §*The depth in `New units`*; `docs/review-handoff-protocol.md`'s field table gets the row; `templates/config.md` §*What no row governs* and `_literal_strings` gain the labels | S1–S7 as `tests/test_a_fix_of_a_fix_is_counted.py`, each case seen red before the derivation (§15) and the red shown in the phase record; the narrow run of that module plus `test_the_record_is_generated.py`, `test_the_fixes_name_their_surface.py`, `test_the_pull_request_language_is_the_repositorys.py` | `27756646` |
| 2 | **The gate and the boundary.** `chain_check.py`: `runs_of(records)`; `main` hands `stopping_floor` and the new arm `fix_of_a_fix` the current run; the arm's eight rows from the spec's gate table; `frame_mark` reads the foot block and `frame` holds the `Reframed` line's `<who>` to `Planning`; `round_record.py`'s `floor_and_fixes`/`bound_line` read the current run; what `reach_back` does to a `no fixes to check` predecessor settled and pinned; `docs/round-record-spec.md`'s section gets the gate table | S8–S11 in the same module or `tests/test_the_chain_goes_back_to_its_framer.py`: planted repositories driven from Python (§8), exit codes read directly (§1), each refusal seen red before the arm, `cutoff_item_is_traceable(REFRAME_FROM)`; the narrow run plus `test_the_reopening_is_one.py`, `test_the_record_is_held_to_the_floor_and_the_depth.py`, `test_chain_check_at_the_pull_request.py` | `44c3058b` |
| 3 | **The owner and the carriers.** `skills/code-review/orchestration.md`: `### A fix of a fix twice sends the work item back to its framer` under *the run ends with a verifying round*, stating the rule, the two-against-three relation to the 3+ Fix Rule, the stop, the reframe and the exit; `docs/review-chain-spec.md`: a link of at most three lines beside the `stop regardless` row; `agents/framer.md`: the hand-back paragraph rewritten (the route back exists, from the chain), what a re-spawned framer reads and writes, the `Reframed` line among its writes; `agents/warden.md`: one sentence; `skills/implement/SKILL.md` §3's `spec.md` row names the reframe line; `templates/sdd-spec.md`'s comment says the line exists and is never in the template; `skills/implement/orchestration.md`'s acts table gets the heading's row (`check: skills/code-review/scripts/chain_check.py`); `tests/test_the_rules_have_one_owner.py` gets rule 11 with owner `ORCH` and link carriers; `docs/issues-and-milestones.md` names `chain: reframed` in one sentence | S13: `test_every_orchestrator_act_names_its_delivery.py`, `test_the_rules_have_one_owner.py` (the new rule's sentence seen red with it stashed), `test_a_section_marked_for_one_role_reaches_only_that_role.py`, `test_a_document_has_room_for_the_next_fold.py`, `test_docs_line_wrap.py`; `wc -l docs/review-chain-spec.md` ≤ 1000 | `a8d3482f` |
| 4 | **The fragments and the replay.** `seal/specs/1791240747-…/changelog.md` (one `### Changed` entry a reader of the release notes can act on, no file list); `seal/ledger/1791240747-….md` with one row per acceptance scenario's claim and the `Re-read ·` rows the moved anchors owe, written by `evidence-check --reverify --into seal/ledger/1791240747-….md --checked <date>`; S12 executed as a probe (`test_tmp_*`, deleted) replaying the two chains at `v0.18.3` with the fix ranges from the pull request heads, the result in `phases/phase-4.md` and `overview.md` labelled `executed`; `overview.md` closed | S12, S14: `evidence-check --strict .` exit 0 read directly; `git diff --stat origin/release/v0.19.0...HEAD -- seal/releases seal/ledger.md` empty; `survivor-check --range` over the branch | `093ccd3d` |
| 5 | **The reading narrows to a path** (the reframe). `round_record.py#landings` keeps, of the pairs `location_units` returns, only those with a path — unconditionally, where round 1's fix made it conditional on `names_a_file` — and its docstring and the comment block above `CELL_WORD_RE` say so; `names_a_file`, `range_carriers`, `CELL_WORD_RE` and `PATH_TAIL_RE` leave the tree. `tests/test_a_fix_of_a_fix_is_counted.py`: `TRACKED_FILES` and the four bare-name cases (`test_a_bare_name_two_files_of_the_range_carry_does_not_land`, `test_a_bare_name_a_touched_file_carries_unchanged_does_not_land`, `test_a_name_beside_a_tracked_file_of_any_kind_does_not_land`, `test_a_name_beside_a_tracked_py_file_lands_only_through_it`) replaced by S5's one parametrized case over every shape the three rounds met and S5b's; `test_every_location_shape_the_depth_walk_reads_lands` loses the `` `u` `` and `` `u()` `` parameters, which move to S5. The carriers of the tracked-file and carrier sentence rewritten: `docs/round-record-spec.md` §*A fix of a fix — `Fix of a fix`* (shorter or equal; the file is at 994 lines), the disclosure paragraph of the owner in `skills/code-review/orchestration.md` (a name with no path among what counts as none), `agents/warden.md`'s one sentence (the `Location` that counts carries the `.py` path) | S5, S5b: the alone shape and round 3's three shapes seen red with `round_record.py` at `6ceb7d46` (§15), the red shown in `phases/phase-5.md`; the narrow run of the module plus `test_the_record_is_generated.py`, `test_the_fixes_name_their_surface.py`, `test_the_chain_goes_back_to_its_framer.py`; `survivor-check --range 9c32e7f6..HEAD` for the removed wording; `test_docs_line_wrap.py`, `test_a_document_has_room_for_the_next_fold.py`, `test_the_rules_have_one_owner.py` | `ba4957f9` |
| 6 | **The records and the replay.** `seal/ledger/1791240747-….md`: A1's claim corrected in place to the path-only reading (the fragment is this work item's own and above the freeze), the four rows anchored on the removed cases REMOVED and the new cases' claims written as new rows; `changelog.md`'s paragraph on what never counts rewritten (a name with no path, in place of the tracked-file and carrier clauses); `overview.md`'s *Fed back* paragraph and divergence table carry the reframe; `survivors.md`'s rows that quote the removed wording re-read; round 3's ⬜ 2 answered by removal — the three sentences it corrects no longer exist. Q6 executed: the reviewer's round-1 method (`refs/pull/*/head` fetched in a scratch clone) over the four `v0.18.x` tags with the path-only `landings`, the stop count beside Q1's 26 of 64, and #814 and #801 still `first` at round 2 and `second` at round 3 | S12, S14, Q6: `evidence-check --strict .` exit 0 read directly (§1); `git diff --stat origin/release/v0.19.0...HEAD -- seal/releases seal/ledger.md` empty; the replay as a `test_tmp_*` probe run once and deleted (§7), its numbers in `phases/phase-6.md`, `overview.md` and Q6 labelled `executed` | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **A new parsed field in `round-N.md`**, required of work items begun at or
  after `1791240747`; earlier records print. Every record the generator writes
  from this release carries it.
- **A new refusal at the pull request** (`chain_check.py`, run by
  `.github/workflows/hygiene.yml`), behind the same cutoff. Failure direction
  blocks more; prompt budget zero.
- **A new refusal at the keyboard**: `round-record new` refuses a record after
  an unreframed `second`, exit 2, nothing written.
- **A new line at the foot of `spec.md`** for a work item the chain sent back,
  and a second `Approved` line in its `plan.md`. The template is unchanged.
- **A new label** `chain: reframed`; nothing reads it.
- **After the reframe, a finding located by a bare name is never a fix of a
  fix.** Only a `Location` carrying a `.py` path counts. The warden writes
  it; a record whose reviewer did not reads `no` where it might have read
  `first`.
- No new dependency, no migration, no environment variable. Git and the
  standard library's `ast` only.
