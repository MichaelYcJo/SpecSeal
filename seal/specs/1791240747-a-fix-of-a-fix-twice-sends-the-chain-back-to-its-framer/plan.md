# Implementation Plan: a fix of a fix twice sends the chain back to its framer

<!-- seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

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

**Constraints.** `docs/review-chain-spec.md` is at 994 of a 1000-line ceiling
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

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The reading and the row.** `chain_check.py` constants `FIX_OF_A_FIX`, `FOF_NO`/`FOF_FIRST`/`FOF_SECOND`, `REFRAME_FROM`, `REFRAME_RE`, `fix_of_a_fix_count`; `round_record.py`: `top_units` keeps enough of each node to compare ASTs between ends; `landings(...)` derives the row from the previous record's `Fix range` and `New units` and the report's open rows at the target, refusing an unresolvable range; `build` writes the row between `New units` and `Needs a fix`; `new` prints the stop line on `second` and refuses a record after an unreframed `second`; `templates/sdd-round.md` gets the field row; `docs/round-record-spec.md` gets §*A fix of a fix — `Fix of a fix`* in the shape of §*The depth in `New units`*; `docs/review-handoff-protocol.md`'s field table gets the row; `templates/config.md` §*What no row governs* and `_literal_strings` gain the labels | S1–S7 as `tests/test_a_fix_of_a_fix_is_counted.py`, each case seen red before the derivation (§15) and the red shown in the phase record; the narrow run of that module plus `test_the_record_is_generated.py`, `test_the_fixes_name_their_surface.py`, `test_the_pull_request_language_is_the_repositorys.py` | `27756646` |
| 2 | **The gate and the boundary.** `chain_check.py`: `runs_of(records)`; `main` hands `stopping_floor` and the new arm `fix_of_a_fix` the current run; the arm's eight rows from the spec's gate table; `frame_mark` reads the foot block and `frame` holds the `Reframed` line's `<who>` to `Planning`; `round_record.py`'s `floor_and_fixes`/`bound_line` read the current run; what `reach_back` does to a `no fixes to check` predecessor settled and pinned; `docs/round-record-spec.md`'s section gets the gate table | S8–S11 in the same module or `tests/test_the_chain_goes_back_to_its_framer.py`: planted repositories driven from Python (§8), exit codes read directly (§1), each refusal seen red before the arm, `cutoff_item_is_traceable(REFRAME_FROM)`; the narrow run plus `test_the_reopening_is_one.py`, `test_the_record_is_held_to_the_floor_and_the_depth.py`, `test_chain_check_at_the_pull_request.py` | `44c3058b` |
| 3 | **The owner and the carriers.** `skills/code-review/orchestration.md`: `### A fix of a fix twice sends the work item back to its framer` under *the run ends with a verifying round*, stating the rule, the two-against-three relation to the 3+ Fix Rule, the stop, the reframe and the exit; `docs/review-chain-spec.md`: a link of at most three lines beside the `stop regardless` row; `agents/framer.md`: the hand-back paragraph rewritten (the route back exists, from the chain), what a re-spawned framer reads and writes, the `Reframed` line among its writes; `agents/warden.md`: one sentence; `skills/implement/SKILL.md` §3's `spec.md` row names the reframe line; `templates/sdd-spec.md`'s comment says the line exists and is never in the template; `skills/implement/orchestration.md`'s acts table gets the heading's row (`check: skills/code-review/scripts/chain_check.py`); `tests/test_the_rules_have_one_owner.py` gets rule 11 with owner `ORCH` and link carriers; `docs/issues-and-milestones.md` names `chain: reframed` in one sentence | S13: `test_every_orchestrator_act_names_its_delivery.py`, `test_the_rules_have_one_owner.py` (the new rule's sentence seen red with it stashed), `test_a_section_marked_for_one_role_reaches_only_that_role.py`, `test_a_document_has_room_for_the_next_fold.py`, `test_docs_line_wrap.py`; `wc -l docs/review-chain-spec.md` ≤ 1000 | `a8d3482f` |
| 4 | **The fragments and the replay.** `seal/specs/1791240747-…/changelog.md` (one `### Changed` entry a reader of the release notes can act on, no file list); `seal/ledger/1791240747-….md` with one row per acceptance scenario's claim and the `Re-read ·` rows the moved anchors owe, written by `evidence-check --reverify --into seal/ledger/1791240747-….md --checked <date>`; S12 executed as a probe (`test_tmp_*`, deleted) replaying the two chains at `v0.18.3` with the fix ranges from the pull request heads, the result in `phases/phase-4.md` and `overview.md` labelled `executed`; `overview.md` closed | S12, S14: `evidence-check --strict .` exit 0 read directly; `git diff --stat origin/release/v0.19.0...HEAD -- seal/releases seal/ledger.md` empty; `survivor-check --range` over the branch | `093ccd3d` |

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
- No new dependency, no migration, no environment variable. Git and the
  standard library's `ast` only.
