# Implementation Plan: the report, the record and the cells disagree on one format

<!-- seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-23 by the orchestrating session, on the owner's `automation` answer, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. -->

## Summary

Eight tickets in five phases, built after work item 0 lands on
`release/v0.15.0`. Phase 1 rebases and finishes the cell 0 left half-done
(#218). Phases 2 and 3 fix what the generator reads out of a report (#505,
#382) and what the checkers read out of a record (#436, #217). Phase 4 gives
the `Broad gate` cell room for a second run (#174). Phase 5 writes the
reviewer-facing standard last, so it describes the generator as it then stands
(#503, #437, the `&lt;!--` rule), and pins the three documents against each
other and against the generator. #159 is deferred, with its design sketched
below so the next framer starts from it.

## Technical context

**Where the eight tickets land, at cbb58091.** All coordinates were read;
line numbers are for the reader's `sed -n` and are not anchors.

- `skills/code-review/scripts/round_record.py`: `section_body` (~995,
  `if lines[i].startswith("#"): break`), its callers `table_body` (~1023) and
  `fenced_after` (~1205), and the section-end scan inside `swallowed` (~1184,
  the same `startswith("#")`); `build` (~2023) refuses an unresolvable
  `--target` and then writes `cell(chain.TARGET, args.target)` raw (~2119);
  `floor_and_fixes` and `bound_line` (~1942–2022, the `if counted and
  running:` branch); `seal` (~4112) with six refusals, none of which is *the
  cell already holds a run*, and `new_broad_gate_file` (~4088);
  `finding_number` (~2570) admits a bare marker and refuses an empty cell.
- `skills/code-review/scripts/chain_check.py`: `fix_range` (~1706, the
  `says_none` early return), `fix_surface` (~2428, the pending arm at
  `fixes_exist and says_not_yet(value)`, cutoff `ORDER_FROM`), `RANGE_FROM =
  1789621028`, `broad_gate` (~3438, `named = SHA_RE.findall(written)` and
  `named[0]` as the run), `direct_seal` (~3826), `closed_with_a_fix` (~1688,
  `FIX_WORDS` over every row), `open_blocking` (~1586, `BLOCKING in
  "".join(seen)`).
- `skills/evidence-check/scripts/evidence_check.py#claim_lines` (~2003):
  `aside = True` with nothing symmetric to `held`.
- Documents: `agents/warden.md` §Report (the fenced skeleton at ~72–96 shows
  the headers and no example row; the no-id sentence at ~181–193);
  `skills/code-review/SKILL.md` §Findings format (~170–208, states the rule
  since #248 on 2026-09-08 — present during the rounds #503 measured);
  `templates/sdd-round.md` (~379–429 comment; the `Broad gate` row at 39);
  `docs/review-chain-spec.md` §*The finding id* (~905), §*A verdict row that
  commissions nothing* (~921), the `What new prints` table (~1474–1478);
  `docs/review-handoff-protocol.md:171`; `skills/verify/SKILL.md:750`;
  `agents/sealer.md`; `skills/code-review/orchestration.md` ~521–545.
- Tests: `tests/test_the_record_is_generated.py` (paste-ready and fence
  cases ~1944–2042), `tests/test_new_says_when_head_is_not_the_target.py`
  (~287, pins the printed line and deliberately not the cell),
  `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `tests/test_a_record_states_what_the_tree_has.py` (~617–667, the aside and
  unclosed-fence cases), `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`,
  `tests/test_a_record_precedes_the_fixes_it_commissions.py` (`bound_line`).

**Corpus measurements, read at cbb58091 with `grep` over
`seal/specs/*/rounds/`.** 23 committed round records and 16 committed
reports. Ten of the sixteen reports use `###` subheadings (the shape #505
loses); five records read `no paste-ready fix in the report`. Two reports
already write `&lt;!--`. No record at or after `RANGE_FROM` holds `Fix range`
pending beside a `round-N` in `Fixes checked by` (five records before it have
no row, which the absent-row grandfathering already excuses). Every sealed
cell holds exactly one run; none shows the re-seal the milestone describes,
which is what `seal` replacing the cell predicts.

**What breaks in six months.** Phase 4: a document that says *the SHA the
run happened at* reads one run where the cell may hold two; A16's pin and the
list in `spec.md` §Data & interfaces are what make that a red test rather
than an eighth stale sentence. Phase 2: a reviewer who nests `####` under a
`###` under `## Paste-ready fixes` is carried, because the rule is *same level
or shallower ends it*, not *one level deeper is allowed*. Phase 3: a custom
`Fix range` reason that starts with the template's words is refused beside a
`round-N`, exactly as `fix_surface` already refuses it — a reason that does
not start with them passes (`says_not_yet`'s stated exception). Phase 1: 0's
reader is renamed and `bound_line` still calls it, because A11's grep is the
pin and the differential is the proof.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **All nine tickets as one work item** | nine fix tables in one review chain; the reviewer-facing standard (three documents) and the checker arms (three scripts) are reviewed by one round each, and a finding in one holds the other seven | rejected — one ticket out |
| **Eight in, #159 deferred** | #159's design answer arrives one release later; until then a corrected cell stays traceless, as it has since 0.8. The cost is bounded: `seal` stops rewriting the one cell the generator itself corrects (phase 4), which is the in-place rewrite 0.14.0 measured | **chosen** |
| Split further — the standard (#503/#437) as its own item after the generator work | the documents would describe a generator that a second work item then changes (`###` under the fixes section), and the pin in A15 could not be written until both landed; two chains for one format | rejected |
| Pull #159 in as a design-only phase (write the design, build nothing) | a phase that ships no code and no case is a `docs/` change with nobody to verify it; the design belongs in the frame of the work item that builds it | rejected — the sketch is below, for that framer |
| **#174 option 2 — the cell is a list, newest first, `seal` keeps what it replaces** | a reader who takes *the SHA* to mean the whole cell reads two; every document naming the cell moves (seven places, listed in `spec.md`); a separator has to be chosen | **chosen**. The milestone names the one-entry cell as the defect (*held only one seal when a branch was re-sealed*), `chain_check.broad_gate` already reads `SHA_RE.findall(...)[0]`, so newest-first costs the reader nothing, and a first seal is byte-identical to today, so no committed record and no fixture moves |
| #174 option 1 — one entry, the second run recorded in the pull request body | the run-level table in `skills/verify/SKILL.md` is filled from memory for a re-sealed branch, which is the failure the ticket measured; the fact lives in a body nothing parses | rejected |
| #174 newest LAST (append) | `broad_gate`, `seal`'s descends-from refusal and `direct_seal` all read `named[0]`; every reader changes for an ordering nobody reads | rejected |
| #174 mark the replaced entry `spent` | whether a run was spent (an edit after it) or red (a pre-existing failure) is the sealer's report's to say, and the cell cannot know which; a word the cell cannot verify is a claim | rejected — the entry is kept as written |
| **#436 under `RANGE_FROM`, no new cutoff** | a record between `ORDER_FROM` and `RANGE_FROM` has no `Fix range` row and is excused by the absent-row grandfathering already there; zero records at or after `RANGE_FROM` hold the pair | **chosen**; the ticket's own judgment call, measured |
| #436 under `ORDER_FROM`, matching `fix_surface` | `fix_surface`'s cutoff is later than its row because the pending value only became structural then; `Fix range` was born with the pending value, so `ORDER_FROM` would excuse nothing `RANGE_FROM` does not | rejected |
| **#505 `section_body` ends at a heading of the same level or shallower** | a reviewer's `##` inside a section is still an end, as today; the one shape that changes is the deeper heading. The same rule reaches `swallowed`'s section-end scan (A3), or the phase says why it must not | **chosen**; every caller wants it — `table_body` reads a table that a `###` cannot interrupt, `fenced_after` reads fences a `###` labels |
| #505 give `fenced_after` its own walk that skips `###` | two definitions of *a section* in one module; the swallowed-table check reads the other one | rejected |
| **#382 write the resolved commit into the cell** | a person reading the record no longer sees the spelling they typed; `head_moved` already resolves it for its printed line, so the record and the line agree | **chosen**; the refusal half already shipped |
| #382 refuse anything but a full SHA | breaks the spelling the existing case pins as legitimate, for no verdict gained | rejected |
| **#503 an example row set in the skeleton, not another rule** | a reviewer who copies the skeleton copies the shape; the rule stays where it is in `skills/code-review/SKILL.md`. A15 executes the skeleton through `new` so it cannot rot into a shape the generator refuses | **chosen**; the control round in #503 was a one-sentence example |
| #503 soften `new` to accept an empty `#` cell | an empty cell says nothing; admitting it ticks `Pass` over an open finding (`docs/review-chain-spec.md` §*A verdict row that commissions nothing*) | rejected |
| `✅` refused as a marker | a gate change with nothing red behind it; the glyph reads as a no-id row today and no committed record carries it | rejected — the standard says `🟢` |
| **The `&lt;!--` rule for the reviewer** | a reviewer who forgets writes a literal opener and `swallowed` refuses at `new`, as today; the sentence is where the refusal sends them | **chosen**; code-span parsing declined twice in the tree |
| **#217 the ticket's paste-ready, symmetric `aside_held` (NAME NOT IN TREE until phase 3)** | inside a never-closed comment a fence is not recognised, so a fenced name is read — the mirror of the fence half's stated limit; the record is malformed there and the direction is to read | **chosen** |
| **#218 on 0's reader** | 0's phase 2 changes the same function; building #218 on cbb58091 and rebasing would resolve the conflict by hand. Phase 1 rebases first, re-reads, then edits | **chosen**; the differential over #218's sequences is re-run against the landed reader as the proof of inheritance item 2 |
| #218 before 0 lands, on cbb58091 | the `== chain.FLOOR_YES` read #218's paste-ready still contains is the one 0 removes; A would reintroduce what 0 took out | rejected |

**#159's sketch, for the framer of the release after this one** (read, not
decided): the ledger's `Corrected <date>` marker and `correction-check
--range origin/<base>...HEAD` already read a feature branch's own history on
every pull request into a release branch, before the squash destroys it — so
*not git history* is narrower than the ticket states, and the failing
placement was `test.yml` on `push` to `main`. The same shape for a round
record is a trailing `<!-- Corrected <date>: <field> was `<old>` -->` under
the field table, excluded for a pending fill (both spellings), read by a
range check in `hygiene.yml` on pull requests into `release/*` only. What A
settles of it: the generator's own rewrite (`seal`) becomes an append.

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **Rebase onto `release/v0.15.0` with 0 landed, re-read, then #218.** Re-read `chain_check.py`'s reopening reader (name off the tree), `stopping_floor`, `run_reopened`, `round_record.py#floor_and_fixes` and `#bound_line` as 0 left them, and record the names in `phases/phase-1.md`. Then: a stopped count walk that reached two fires with `running = False`; `bound_line` prints the gate's own error as the bound; the inner `break` becomes load-bearing. `docs/review-chain-spec.md`'s `What new prints` row for `one reopening remains` rewritten (A17). Cases A9, A10, A11; the differential over #218's sequences as a `test_tmp_*` probe, run once, deleted. Ledger R3, R4 re-read | `tests/test_a_record_precedes_the_fixes_it_commissions.py` and the floor-and-depth module executed; the probe's count recorded in `phases/phase-1.md` | 14ab81c8 |
| 2 | **What the generator reads out of a report — #505, #382.** `section_body` ends at a heading of the same level or shallower; `swallowed`'s section-end scan takes the same rule or the phase record says why not (A3). `build` writes the resolved commit into `Target SHA`. Cases A1, A2, A4, A5; the existing `HEAD~1` case's docstring rewritten to say the cell is now pinned. New ledger rows for `section_body` and `fenced_after` in the fragment | `tests/test_the_record_is_generated.py`, `tests/test_new_says_when_head_is_not_the_target.py`, `tests/test_the_fixes_close_the_record.py` executed | |
| 3 | **What the checkers read out of a record — #436, #217.** `fix_range`'s pending arm under `RANGE_FROM`, mirrored from `fix_surface`; `claim_lines` holds an unclosed comment's lines the way it holds an unclosed fence's (#217's `aside_held` — NAME NOT IN TREE until this phase lands). Cases A6, A7, A8. Ledger R5, R6 re-read; a sibling of R7 for `fix_range` in the fragment. Both are gate changes: the four answers drafted into `overview.md` for the pull request body | the floor-and-depth module (or wherever `fix_range`'s cases live), `tests/test_a_record_states_what_the_tree_has.py` executed; `evidence-check --strict` executed | |
| 4 | **The `Broad gate` cell holds every run — #174.** `seal` writes the new entry first and keeps the cell's earlier entries, for both homes; `new_broad_gate_file`'s comment, `templates/sdd-round.md`'s cell comment, and the six documents listed in `spec.md` §Data & interfaces say *newest first, one entry per run*. `chain_check.broad_gate`'s docstring says why `named[0]` is the run. Cases A12, A13, A14. Ledger G2 and the `direct_seal` row re-read. `skills/verify/SKILL.md`'s run-level row reads the count off the cell | `tests/test_the_seal_is_taken_once_by_the_sealer.py` and `tests/test_chain_check_at_the_pull_request.py` executed | |
| 5 | **The reviewer-facing standard — #503, #437, `&lt;!--`.** `agents/warden.md` §Report: example rows in the skeleton (`🟡 1`, bare `🟢 … confirmed`, `❓`), the five markers and `✅` not among them, the `&lt;!--` sentence, `###` allowed under the two fenced sections, the three requirements of a carried closure beside the no-id sentence. `skills/code-review/SKILL.md` §Findings format and `docs/review-chain-spec.md` §*A verdict row that commissions nothing*: the worked row. `templates/sdd-round.md`'s comment: the same row. Cases A15 (the skeleton executed through `new`) and A16 (the three documents pinned). `changelog.md` fragment; `overview.md` closed; every ledger row of the fragment written | `tests/test_the_record_is_generated.py` and the pinning case executed; `evidence-check --strict` executed | |

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
earlier: **phase 1 begins with a rebase, so re-read this column after it.**

## Operational impact

No migration, no new dependency, no environment variable. Three verdict
changes, each `blocks more`: a record at or after `RANGE_FROM` whose
`Fix range` still reads the template's pending words beside a `round-N` fails
at the pull request (zero committed records affected, read 2026-09-23); the
records arm of `evidence-check` reads the lines after an unclosed HTML
comment, so a name there that the tree lacks is now reported (no live record
ends inside a comment, read by #217 and not re-measured here — a measurement
row in `questions.md`); `bound_line` prints *this record ends the run* for a
stopped walk that reached two, where it printed *one reopening remains*. One
cell shape widens: `Broad gate` may hold more than one entry, newest first; a
plugin user's existing records are the one-entry shape and stay valid. One
cell narrows: `Target SHA` holds a resolved commit, which every reader of it
already wanted. The prompt budget is zero: nothing here asks a person
anything; every refusal arrives at the keyboard of the session that wrote the
cell or at the pull request, with the repair named.
