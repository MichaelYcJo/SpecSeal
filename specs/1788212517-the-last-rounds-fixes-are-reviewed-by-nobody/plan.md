# Implementation Plan: the last round's fixes are reviewed by nobody

<!-- specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

## Approval

**Approval was given in advance**, by the repository owner, on 2026-09-01, for
options B and A of issue #33 together, and not for option C. The session that
implements it does not stop for a go; anything that would otherwise be raised
becomes a `questions.md` row or a `# RIDER:` comment at the coordinate it is
about.

This work sits on the top rung twice over — it changes a CI check's verdict
and it changes the instructions two agents read and act on — so `spec.md` and
this file are owed whether or not anyone is waiting to approve them.

## Summary

A review run ends with the orchestrator fixing what the last round found,
checking `- [x] Pass` on that round's record, and opening the pull request.
Nobody opens those fixes. Measured on `1788137177-the-axis-nobody-was-asked`:
round 2 found seven defects inside round 1's fixes, a hit rate of 100% on the
one set anybody looked at, and round 2's own fixes then went in unread. The
same thing happened one work item later, on this branch's own base —
`specs/1788184145-…/rounds/round-3.md` records four findings fixed at
`d3fe44d` and says so in a comment nothing reads.

Two changes, and they meet at one cell.

**B** gives the record a `| Fixes checked by |` row with a three-value
vocabulary, and gives `chain_check.py` a set of refusals for a claim git can
contradict. That is what moves the state out of a transcript and into the
tree.

**A** makes the last round a **verifying round**: spawned after the previous
round's fixes are committed, targeted at the diff of those fixes, and asking
whether each closed finding is actually closed. A verifying round that opens
nothing needing a fix does not consume the round cap, because the cap counts
rounds that found something and a round that finds nothing is the loop having
converged.

They meet because only a later round may be named as a checker. So the last
record in a finished run reads `no fixes to check` — the verifying round's
terminal state — and any other honest ending reads `nobody — <why>`, in git,
printed by CI, instead of in nobody's memory.

## Technical context

- `skills/code-review/scripts/chain_check.py:730` — `check_round`, called on
  `records[-1]` alone at `:1018`. The new field is read here, beside the
  `Pass` claim and the verdict table, and nowhere else.
- `skills/code-review/scripts/chain_check.py:169` — `CLOSED_WORDS`, and the
  comment above it stating the direction an unreadable cell takes. The new
  vocabulary follows that rule rather than inventing a second one.
- `skills/code-review/scripts/chain_check.py:450` — `field`, which already
  pulls a `| label | value |` row out of the record. Nothing new is needed to
  read the cell.
- `hooks/routing.py:231` — `round_number`, the one place the `round-N.md`
  ordering rule lives. The new check resolves `round-N` through it rather
  than writing the pattern a third time.
- `docs/review-chain-spec.md:34-56` — the bound, and `:115-119`, the paragraph
  that closes the findings and is silent about the answers. Both are amended
  at their own coordinates rather than by a new section that contradicts them.
- `docs/review-handoff-protocol.md:110-119` — the record's field table, and
  `:161` the paragraph the spec quotes. The protocol is tool-agnostic, so the
  field goes in as a shape rather than as this plugin's implementation.
- `templates/sdd-round.md:10-32` — the field table and the `Pass` comment. A
  session bootstraps from this file and never reads the argument.
- `skills/code-review/SKILL.md:99` — the cross-session records heading still
  names `.specseal/handoff/PR-<n>/`, a directory
  `docs/review-handoff-protocol.md` says was never once created. That is the
  section option A is written into, so it is corrected in the same edit; a
  heading naming a dead path above new instructions is worse than either
  alone.
- `specs/1788184145-…/rounds/round-3.md:10` — the one record in this
  repository the new requirement reaches. Its declaration is added relative to
  `main`, so the release pull request reads it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **B + A, as scoped** | A run that legitimately reaches the cap with unopened fixes still ships, because `nobody — <why>` passes. The gap is visible on every CI run rather than closed | **Taken.** It is the issue's own framing of B — *makes the gap legible without closing it* — with A as the thing that closes it in practice |
| **B + A, with `Pass` beside `nobody` failing** | The one merged record this repository already carries goes red, and there is no honest repair: writing a `round-4.md` for a review nobody ran is fabricating one, and unchecking `Pass` fails the ready-pull-request rule instead. The release pull request would be red until someone spawned a round for work that has already merged | Not taken here. It is Q1, priced, with the repository owner as its answerer |
| **C — the chain ends at a round with no findings** | Unbounded in the bad case, and at the cap it stops with the same gap one step later. A round closing a 🟡 with grounds would be forced to continue | Rejected by the repository owner before this work started |
| **A alone** | The verifying round is prose, and prose is what the incident report says was already there. Nothing in git would say whether a run had one | Rejected — B is what makes A checkable |
| **B alone** | The record names the gap and nothing closes it. Round 2's seven defects would have been recorded as unfound rather than found | Rejected — the issue says A is the one that would have caught them |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **B.** The field: `docs/review-handoff-protocol.md` (draft 0.5), `docs/review-chain-spec.md`'s two-claims paragraph, `templates/sdd-round.md`, the reminder in `hooks/review-history-guard.py`, `chain_check.py`'s reader and its six refusals, `tests/test_the_last_rounds_fixes.py`, and the migrated row on `specs/1788184145-…/rounds/round-3.md` | the new test file with every case shown red under a mutation, plus `test_chain_check_at_the_pull_request`, `test_handoff_outlives_the_merge`, `test_release_hygiene`, `ruff` | |
| 2 | **A.** The verifying round: `docs/review-chain-spec.md`'s bound and its new section, `skills/code-review/SKILL.md`, `agents/warden.md`, `agents/smith.md` | the new test file's A cases, plus `test_docs_line_wrap`, `test_one_word_one_meaning`, `test_the_set_a_work_item_always_has`, `test_review_axes`, `test_broad_gate_rule`, `test_edits_go_through_the_edit_tool` | |
| 3 | The outward-facing prose: `README.md`, `README.ko.md`, `.specseal/README.md`, `templates/specseal-README.md` | `test_docs_line_wrap`, `test_the_set_a_work_item_always_has`, `test_no_real_identifiers`, `test_what_the_reader_understands` | |
| 4 | The `## Unreleased` changelog entry, the ledger rows and the closing memo. (`questions.md` was written with the rest of the SDD set, before implementing) | `test_release_hygiene`, `test_ledger_stamps_resolve`, `evidence_check.py`, `unverified_check.py` | |

Phase 1 is one vertical slice: a record with the field, written by a session
from the template, refused by the check when it lies, and the one existing
record migrated in the same commit. Phase 2 is the second slice — the same
rule stated where the sessions that run the chain read it.

Phase 1 before phase 2 deliberately. The field is what a verifying round has
to write into, so building the procedure first would describe a cell that does
not exist.

## Operational impact

**A behaviour change in CI, and it is the point of the work.** A pull request
whose declaration routes through the review chain now fails when its last
round record carries no `| Fixes checked by |` row. Every round record written
before this release lacks it. This repository carries exactly one such record
and it is migrated in phase 1; a repository that installed the plugin and
updates it gets a failure naming the row and the three values it accepts,
which is the same trade `docs/review-handoff-protocol.md` records for the
`rounds/` move — no fallback, bought back with a message.

No migration script, no new environment variable, no new dependency.
`.claude-plugin/plugin.json` stays at `0.0.1`; the pull request lands on
`release/v0.0.2`, so the entry goes under `## Unreleased`.
