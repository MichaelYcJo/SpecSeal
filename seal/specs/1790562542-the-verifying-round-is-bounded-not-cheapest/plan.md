# Implementation Plan: the verifying round is bounded, not the cheapest (#639)

<!-- seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-28 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

Four sentences that sessions read and act on say the verifying round is the
cheapest round, or is affordable because its target is a diff. The
measurements say otherwise. This work removes those cost claims and keeps
what is true: the diff target bounds the round's surface. The measured cost
goes in the one document that owns the rule, with its sources. The needle is
updated, and a gone/stands pin is added so the claim cannot come back. The
seven ledger rows the edits drift are re-read and re-stamped. No rule
changes, and no code path changes.

## Technical context

- **C1** `skills/code-review/orchestration.md` §*Orchestrator: the run ends
  with a verifying round*, the three-row table (`When` / `Target` / `Job`).
  The `Target` cell is pinned whole by
  `tests/test_the_last_rounds_fixes_are_checked.py#WHAT_IT_TARGETS` through
  `#test_the_verifying_rounds_target_is_the_previous_rounds_fixes`, which
  reads the file through `flat` (whitespace collapsed). The needle ends in
  ` |`, so the new needle takes the cell up to its closing pipe.
- **C2** `docs/review-handoff-protocol.md` §*After the run — the per-segment
  bars*, row `verifying`. `tests/test_the_handoff_before_round_one.py`
  pins only `| verifying | exempt |`, so the Grounds cell is currently
  unpinned.
- **C3** `docs/review-chain-spec.md` §*The last round verifies, and what it
  verifies is a diff*, the paragraph after the one ending "because the run
  ends at it." No test pins its cost sentence. `docs/review-chain-spec.md`
  is in `tests/conftest.py#REVIEW_CHAIN_DOCS`. So `TARGETED_BACKWARDS` is
  checked against the concatenated review-chain text, and the new wording
  must not contain `target is the branch`, `targeted at the branch`, `the
  whole branch` or `the diff of those fixes rather than the branch, or the
  branch`. "rather than a branch" is fine: it matches none of those four.
- **C4** `agents/warden.md` §*Role*, the bullet **A verifying round has a
  diff for a target**, its second paragraph. `WHAT_IT_TARGETS` and
  `WHEN_SPAWNED` pin the bullet's first paragraph, and nothing pins the
  second.
- **C5** the docstring of
  `test_the_verifying_rounds_target_is_the_previous_rounds_fixes`.
- The precedent for the new module is
  `tests/test_the_broad_gate_cell_keeps_every_run.py`: a `CARRIERS` tuple of
  `(parts, stands phrase, gone phrase)`, a `flat()` reader, one case per
  half.
- `survivor-check` reads Python string literals as wording
  (`docs/review-chain-spec.md` §*What the sweep reads*). The new module's
  gone halves are the removed sentences, verbatim, in string literals, so
  the check may name them as survivors. They are deliberate carriers, and
  `seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/survivors.md`
  is the exemption the section provides. Whether it is needed is the work's
  to find (questions.md Q2).

**Failure scenario, six months out.** A later sweep publishes a new median,
and the chain-spec paragraph's figure goes stale. No test pins the number,
on purpose, so nothing turns red. The failure is a stale figure with its
sources printed beside it: a reader can open them and see the date. The
other outcome would be a figure copied into three documents that drift
apart, which is how this issue began. A second scenario: a new document
repeats "cheapest" in different words ("the least expensive round"). The
tree-wide case catches only the exact phrase. The meaning is guarded by the
four gone/stands pairs, and a fifth carrier in new wording is a reviewer's
catch. That limit is stated in the new module's docstring.

## Alternatives considered

| # | Approach | Failure scenario | Verdict |
|---|---|---|---|
| A1 | #639 option 2: delete the cost clause and add nothing | The protocol row is left with *exempt* and no grounds, and the chain-spec paragraph with *one extra spawn* and no statement of what the spawn costs. The next reader rediscovers the question #456 already answered | rejected, as the issue recommends |
| A2 | #639 option 1 as its example words it: the median figure in every carrier | Three copies of a number the next sweep will move. One claim in three documents is exactly the shape of this issue. `orchestration.md` already defers the rule to the chain spec | rejected: the figure lives in C3 only, and C1 points there |
| A3 | Option 1, figure in C3 only, C1 points at it | A reader of C1 who wants the number follows one pointer | **chosen** |
| A4 | Ground C2's exemption on "the segment size", as #639's option 1 suggests | #456 measured verifying rounds at 46–58 calls, twice the nuance's 23-call round, so a size ground is false in the other direction. It would also keep the clause "a segment that small is the nuance below in its every case", which is already false | rejected on #456's numbers. C2 is grounded on target and job, which is #51 observation 1's own ground for the exemption |
| A5 | Leave `agents/warden.md` alone, since the issue's phrase sweep did not name it | "the whole reason the round is affordable" survives as a fourth carrier in the file a reviewer actually obeys. The fix would cover the phrase and not the class (§12) | rejected |
| A6 | Pin the new text by extending `test_the_last_rounds_fixes_are_checked.py` rather than a new module | The file already exceeds a thousand lines, and its constants are organised by rule axis (when, target, cap), not by correction. A gone/stands table there has no neighbour of its kind | rejected. A new module, `tests/test_the_verifying_round_is_bounded_not_cheapest.py`, is the default. The builder may merge it into the existing file if the review asks |
| A7 | Also correct the #81 "cheapest round on record" sentence | It is a different claim about a finding round, its truth is unestablished (spec *Out*), and the issue puts it out of scope | rejected here. It is routed to the orchestrator |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The sentences and their pins, in one commit.** C1–C5 edited per spec *In* 1–5. C6's needle replaced with C1's new text. New module `tests/test_the_verifying_round_is_bounded_not_cheapest.py`: a carriers table for C1–C4 (stands phrase and gone phrase, the gone half verbatim from `1fa25931`), a stands case, a gone case, and the tree-wide `cheapest round of the run` case over `agents/`, `skills/`, `docs/`, `templates/`, `README.md` and `README.ko.md` (not `tests/`, which holds the gone halves). The changelog fragment `seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/changelog.md` rides this commit | `bin/test tests/test_the_verifying_round_is_bounded_not_cheapest.py tests/test_the_last_rounds_fixes_are_checked.py tests/test_the_handoff_before_round_one.py -q`, with its exit code read directly (contract §1). Each pin seen red: restore one old sentence for each gone half, delete one new phrase for each stands half, and restore C1's old cell for C6. The way each was shown red goes in `phases/phase-1.md`. `grep -rn "cheapest round of the run" agents skills docs templates README.md README.ko.md` returns nothing | 32b5886f |
| 2 | **The records.** First, `evidence-check .` on the phase-1 tree, to name what drifted. Each of the seven rows below is re-read against the edit and re-stamped with `--reverify`, with a dated `Re-read 2026-09-28` note in the row. One new row in `seal/ledger/1790562542-the-verifying-round-is-bounded-not-cheapest.md`: *the four carriers say the verifying round is bounded by its diff and cost about a finding round, and none says it is the cheapest*, anchored on C1–C4's units and the new module's cases. Then `survivor-check --range origin/release/v0.15.7..HEAD`, with every survivor corrected or exempted in `survivors.md` with a reason | `evidence-check .` exits 0 after the re-stamp (executed). `survivor-check` output read in full (executed). Both results go in `phases/phase-2.md` | b2b1de06 |

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

### Ledger rows this edit drifts

The list comes from reading every row in `seal/ledger.md` and
`seal/releases/*.md` that anchors one of the five edited files
(`seal/ledger/` does not exist at the base). A markdown unit runs from its
heading to the next heading at the same or a higher level
(`skills/evidence-check/scripts/evidence_check.py#file_units`). So an H1
unit is the whole file, and a `##` unit includes its `###` subsections.
**This list was read, not executed.** Phase 2's `evidence-check` is the
executed answer, and it wins if the two disagree.

| Row (file, first cell) | Anchor that drifts | Edited by | Claim still true after the edit? |
|---|---|---|---|
| `seal/releases/0.9.3.md`, "The verifying round treats what `New units` names as a finding surface, not a verification surface" | `skills/code-review/orchestration.md#"## Orchestrator: the run ends with a verifying round"` | C1 | yes. The `New units` paragraph is not touched. The row's second anchor, `agents/warden.md#"## Role">"judge them as code — …"`, is narrowed to a sentence C4 does not edit, so it should not drift |
| `seal/releases/0.9.3.md`, "The seam is the one the file's own headings drew, and it is contiguous" | `skills/code-review/orchestration.md#"# code-review — the orchestrator's half"` (H1, the whole file) | C1 | yes. No heading moves |
| `seal/releases/0.11.4.md`, "The fix pass's Verdict cell holds the word alone …" | `docs/review-chain-spec.md#"### The last round verifies, and what it verifies is a diff"` | C3 | yes. The *Two cells, not one* paragraph is not touched |
| `seal/releases/0.4.0.md`, "The bars are written beside the meter they interpret, one per segment kind … a verifying segment exempt" | `docs/review-handoff-protocol.md#"### After the run — the per-segment bars"` | C2 | yes. `exempt` stays |
| `seal/releases/0.8.2.md`, "R4 · `docs/review-handoff-protocol.md` §*After the run — the per-segment bars* says the bars judge a segment against its kind …" | same anchor | C2 | yes |
| `seal/releases/0.15.0.md`, "A11 · the eight documents that describe the `Broad gate` cell …" | `agents/warden.md#"## Role"` | C4 | yes. The `Broad gate` sentence is not touched |
| `seal/releases/0.15.1.md`, "D1 · a finding whose coordinates sit at two depths …" | `agents/warden.md#"## Role"` | C4 | yes. The one-depth-per-finding paragraph is not touched |

The anchors above carried the hashes they held at `97a30dc6` when this
table was framed. Phase 2 took the hashes out, because `evidence-check`
reads a stamp in a live work item's records as a claim about the tree now,
and each of these was exactly the unit this branch edits. The executed list,
with twelve drifted anchors in eleven rows where this table has seven rows,
is in `phases/phase-2.md`.

Expected **not** to drift, because each is narrowed to a sentence no edit
touches: `seal/ledger.md` "The answer a run ends on had no field …"
(`agents/warden.md#"## Role">"Say plainly whether you opened anything …"`),
and `seal/releases/0.15.1.md` "S2 · each of the three documents opens saying
what it is the authority for …"
(`docs/review-chain-spec.md#"# review chain — behavior spec">"Authority for
the cycle contract the"`). The three rows on
`tests/test_the_last_rounds_fixes_are_checked.py` anchor functions that C5
and C6 do not edit (`test_pass_beside_nobody_…` ×2,
`test_a_draft_is_excused_…`).

**`--reverify` re-stamps every resolvable row, not only this branch's.** Run
`evidence-check .` before the first edit as well. The base was sealed at
0.15.6, so it should report nothing drifted. If it does report drift, those
rows are not this branch's to re-stamp, and the builder re-stamps its seven
rows by hand or stops and says so.

### A parallel branch shares a file

Work item D (#400, `feat/400-the-stamp-reaches-the-person-it-is-drawn-for`)
also edits `skills/code-review/orchestration.md`, according to milestone
50's description. Any edit to that file drifts the H1 row in
`seal/releases/0.9.3.md`. Both branches will therefore re-stamp the same row
to different hashes, and whichever merges second into
`release/v0.15.7` meets a conflict in `seal/releases/0.9.3.md`. The
repository's CLAUDE.md prescribes the resolution: hunk by hunk. The
`Re-read` notes are a union, and the hash is recomputed by `evidence-check
--reverify` against the merged file, never taken from either side. D's frame
was not yet written when this was read, so whether D also touches the
`## Orchestrator: the run ends with a verifying round` unit is unknown.
Answerer: the orchestrating session, which sets the merge order.

## Operational impact

None. No migration, no environment variable, no dependency, no compatibility
break. What a reader of three documents and one agent definition is told
changes, and what any gate, hook or script does does not.
