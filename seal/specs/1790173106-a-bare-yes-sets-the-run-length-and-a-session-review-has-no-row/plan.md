# Implementation Plan: a bare `yes` sets the run length, and a session review has no row

<!-- seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-23 by the orchestrating session, on the owner's `automation` answer, when `smith` was spawned.

## Summary

Two decisions, three phases. #138: `Needs a fix` takes the floor row's
vocabulary in full — a bare `yes` is refused at the reader and at the writer,
and every reader of the cell goes through one function. #241: no third
`Review` answer; the record a session's own check leaves is the sealer's
`broad-gate.md`, which `straight to the PR` has owed since 0.12.0, and the
seven places still saying that answer requires nothing are rewritten and
pinned. Both ship in this work item; nothing from work item A is pulled in.

## Technical context

**#138, the readers of one cell.** `skills/code-review/scripts/chain_check.py`:
`yes_or_no` (one parser for both terminal rows; returns `("yes", "")` for a
bare `yes` and leaves the reason to the caller), `stopping_floor` (reads the
record's own `Needs a fix` as `word_needs` (NAME NOT IN TREE: phase 1 replaced
the local with `says_reopened`'s answer) only, then the floor row with
`if word == FLOOR_YES and not reason` — the branch the other row lacks),
`run_reopened` (`word == FLOOR_YES`, so a bare `yes` stops the count).
`skills/code-review/scripts/round_record.py`: `terminal_value` (refuses only
`word is None`), `bound_line` (its own `== chain.FLOOR_YES` at the reopening
read), `written_late_cell` (the precedent for refusing a bare `yes` at the
writer: *carries no reason*). Cutoffs: `NEEDS_FROM = FLOOR_FROM = 1788472135`;
`NEEDS_FROM` grandfathers the row WHOLE (`needs_excused`), and the new refusal
sits under it — no new cutoff, because no committed record at or after it
carries a bare `yes` (read: 20 live records; the fixture corpora under
`tests/` carry none either). Tests:
`tests/test_the_record_is_held_to_the_floor_and_the_depth.py` (fixtures
`record(sha, floor=…, needs=…)`, `declared`, `run`), and for the generator
`tests/test_the_record_is_generated.py` and
`tests/test_a_record_precedes_the_fixes_it_commissions.py` (both name
`terminal_value`/`bound_line`). Documents the checker's tests already pin:
the module docstring must name `Needs a fix`
(`test_the_module_docstring_names_what_the_checker_refuses`); the
`NO_CHECK_READS` pattern is the shape for a *gone / stands* sentence pair.

**#241, the seven sentences.** `hooks/routing.py` (`CHAIN`, `DIRECT`,
`REVIEW_ANSWERS`, strict in `parse`); `chain_check.py#direct_seal` (the
requirement: `broad-gate.md` at a ready pull request, `DIRECT_GATE_FROM =
1789518345`, excused before it); `chain_check.py#main`'s `routing.DIRECT`
branch (prints *no round record required; the broad gate's cell is read from
broad-gate.md* — the one place in the tree that already says it right);
`hooks/commit-review-gate.py#judge`, option 1's text, pinned by
`tests/test_routing_is_recorded.py` (`USER'S answer`, both spellings — keep
them); `docs/review-chain-spec.md` §*Review arm* declaration table;
`skills/implement/orchestration.md` four-combinations table and the routing
section's last paragraph; `templates/sdd-routing.md` `Review` comment;
`docs/release-checklist.md` §4. `agents/sealer.md` and `CHANGELOG.md` §0.12.0
are where the requirement is described today; no `docs/` policy names
`broad-gate.md`.

**What breaks in six months.** #138: a reviewer whose report says
`Needs a fix: yes` with the detail only in the verdict table gets a refusal at
`round_record.py new` naming the line — the same refusal the floor line
already gives — and adds the phrase. That is the cost the ticket's option 1
names, and it is paid once at the keyboard, not at the pull request. #241: a
later change to what `straight to the PR` owes (say #174 makes the seal a
list) has to move the pinned sentence in seven files; the pinning case says
which, so it fails loudly rather than leaving an eighth stale sentence.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#138 option 1 — refuse a bare `yes`, matching the floor row** | a reviewer writing `yes` alone is stopped at `new` and at the pull request; the one refusal that already exists two functions away is reused | **chosen** |
| #138 option 2 — keep it permissive and say why in the row's comment | the two rows keep disagreeing about the same three characters under one parser whose docstring says *one reader for both*; the cell that buys a round stays writable, and §14 is about exactly a line a person reads and acts on | rejected |
| #138 option 3 — refuse a bare `yes` only where later records exist | the same cell is right on the last record and wrong the moment one more is written; no other refusal in this checker depends on how many files follow | rejected |
| #138 refuse at the reader only | the writer keeps producing records the reader refuses, one command later than the author is at the keyboard; `written_late_cell` already refuses at the writer for the same reason | rejected — both ends |
| #138 refuse `Loses a record or crashes` at the writer too, as part of the class | none: the reader already refuses it, so the writer refusing it earlier changes no verdict and saves a round trip | **chosen** with option 1 (§12: the class is both terminal lines) |
| #138 a bare `yes` still stops the count in the walk, only the record itself fails | the earlier record's count stays quiet on the strength of a cell the checker refuses — the direction `run_reopened`'s docstring forbids | rejected — reads as `None` |
| #138 a new cutoff (`NEEDS_REASON_FROM` — NAME NOT IN TREE: a rejected alternative, never written) for the refusal | a ninth cutoff for a rule that is red on zero committed records; the row's own grandfathering (`NEEDS_FROM`, WHOLE) already excuses everything written before anything read it | rejected |
| **#241 — no third answer; document what `straight to the PR` requires, and pin it** | a session that checked its own change reads the declaration table, sees the seal is what it owes, and declares direct; CI reads `broad-gate.md` | **chosen** |
| #241 a third answer, `reviewed by the session`, requiring a round record written by the session | the record's writer is its subject: `Fixes checked by` cannot name a later round, `Ran by` names the session that is also the author, and the chain's own table refuses *the session that wrote them*. The answer records a reading nobody can verify and catches nothing `broad-gate.md` does not; a vocabulary change touches `routing.py`, the gate prompt, `chain_check.py`, the template, the `CLAUDE.md` block, the orchestration tables and every test enumerating two spellings | rejected |
| #241 a third answer as an alias of `straight to the PR` with the same requirements | two spellings of one requirement — the drift `routing.py`'s `BY_SESSION` comment refuses for the same reason | rejected |
| #241 rename `straight to the PR` to say what it owes | `parse` is strict on `Review`; every committed declaration stops being one and the commit gate reopens on each | rejected |
| #241 make the release-preparation commit a declared `straight to the PR` work item, sealed by `broad-gate --record` | every release leaves a `seal/specs/` directory that `settle` cannot retire — #517's regress, decided against in D1 for the fold, and the preparation commit is the same class | rejected — name the class in §4 instead |
| **Ship #138 and #241 here, alone** | A's nine tickets are about the report's and record's *shape*; this item fixes what two cells *mean*. #218 (`bound_line` considers only running walks) is the nearest: this item changes how `bound_line` reads one cell, #218 changes which walks it reports, and the two edits are in different lines of one function | **chosen** |
| Pull #218 in, since both touch `bound_line` | #218 carries its own 584-sequence differential and a report-side sentence change; folding it here makes this item's fix table the place that measurement lands, and A's framer loses the row that owns it | rejected |
| Pull #174 in, since `broad-gate.md` is the record this frame leans on | #174 is a template question (one entry or a list) with a migration row; this item does not change the cell's shape, only which documents say it exists | rejected |

**What work item A inherits from these two decisions**, for its framer:

1. `Needs a fix` and `Loses a record or crashes` take three readable values
   each — `no`, `no — <why>`, `yes — <what>` — and a bare `yes` is refused at
   `round_record.py new` and at `chain_check.py`. A's report-format standard
   (#503, #505, #437) keeps the terminal line as `Needs a fix: yes — <the
   findings that do>`; the reason is part of the value, not a courtesy.
2. One reader for the reopening question, in `chain_check.py`. `bound_line`
   (#218) reads through it; A must not reintroduce a local
   `== chain.FLOOR_YES` on that cell, and #218's differential is the way to
   prove it did not.
3. `Review` stays two answers, and `Ran by` stays `agent on model` /
   `unknown — <why>`. A's record cells do not gain a shape for a session as
   its own reviewer.
4. `broad-gate.md` is the whole record of a `straight to the PR` work item.
   #174's answer for the `Broad gate` cell (one entry or a list) governs both
   homes, because `direct_seal` reads through `broad_gate`.
5. The seven sentences this item rewrites are pinned as *gone / stands*
   pairs. A's edits to `docs/review-chain-spec.md`'s declaration table and
   `skills/implement/orchestration.md`'s four-combinations table keep the
   *stands* half, or move the pin with them.

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#138 at the reader.** `chain_check.py`: one function answering *does this cell say the run reopened* (`True` / `False` / `None`), used by `stopping_floor`'s own-row read and `run_reopened`; a bare `yes` refused on its record under `NEEDS_FROM`'s grandfathering, in the floor row's words; the module docstring's `Needs a fix` row names it. `docs/review-chain-spec.md` §*`Needs a fix`* table row and `templates/sdd-round.md`'s comment. Cases A1–A4, A7 in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`, each seen red first | the floor-and-depth module executed; the mutations named in `phases/phase-1.md` | ee555887 |
| 2 | **#138 at the writer and the printed bound.** `round_record.py#terminal_value` refuses a bare `yes` for both labels in `written_late_cell`'s shape; `bound_line` reads the reopening through phase 1's function. Cases A5, A6 in the round-record suites, seen red first. Ledger: rows on `stopping_floor`, `run_reopened`, `yes_or_no`, `bound_line`, `terminal_value` re-read; F8 REMOVED from `seal/ledger.md` and re-founded in `seal/ledger/<id>.md`; `changelog.md` fragment for #138 | the two round-record modules executed; `evidence-check --strict` executed | e852f49c |
| 3 | **#241.** The seven sentences rewritten (spec items 7–9): declaration table row, checker docstring, orchestration table and closing paragraph, gate prompt option 1, `test_routing_is_recorded.py` docstring, `templates/sdd-routing.md` comment; the paragraph beside the declaration table saying why two answers; `docs/release-checklist.md` §4's sentence. Case A8 as a *gone / stands* pinning test, seen red by restoring one old sentence; A9, A10 green. Ledger rows on the moved headings re-read; `changelog.md` fragment for #241; `overview.md` closed | `tests/test_routing_is_recorded.py`, `tests/test_waiver_decided_at_start.py`, `tests/test_chain_check_at_the_pull_request.py` and the new case executed; `evidence-check --strict` executed | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. What a phase discovers while
it is being built, and needs the next phase to know, goes to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes. Where feature branches squash, these commits stop
resolving at the merge, and a rebase during the work does the same thing
earlier: re-read the column after any rebase.

## Operational impact

No migration, no new dependency, no environment variable. One verdict change:
a record at or after `NEEDS_FROM` carrying `Needs a fix: yes` with no reason
fails at the pull request where it passed before, and `round_record.py new`
refuses the report that would produce it. Zero committed records are affected
(read, 2026-09-23). A repository that updated the plugin and carries such a
record on an unmerged branch repairs it by copying the reviewer's reason into
the cell, which is what `agents/warden.md` already asks the reviewer to write.
