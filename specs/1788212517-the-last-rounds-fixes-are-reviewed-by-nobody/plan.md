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

- `skills/code-review/scripts/chain_check.py` — `checked_by`, called on EVERY
  record in the loop after `check_round`. `check_round` still reads `Pass` and
  the verdict table on `records[-1]` alone, and the two scopes are different
  on purpose. This bullet said the field is read in `check_round` while that
  function's own docstring said it is not; round 1 of this work item's review
  found the pair, and this is the corrected half.
- `skills/code-review/scripts/chain_check.py` — `verdict_of`, the one
  normalizer `open_blocking` and `closed_with_a_fix` share. It has to see
  through markdown emphasis and the commit citation after the word, because
  `**fixed** \`sha\`` is how every verdict cell in this repository is spelled
  and the bare-word version recognised none of them.
- `skills/code-review/scripts/chain_check.py:234` — `CLOSED_WORDS`, and the
  comment above it stating the direction an unreadable cell takes. The new
  vocabulary follows that rule rather than inventing a second one, and
  `VOCAB` is derived from it rather than written out a second time.
- `skills/code-review/scripts/chain_check.py:595` — `field`, which already
  pulls a labelled row out of the record. Nothing new is needed to read the
  cell.
- `hooks/routing.py:231` — `round_number`, the one place the `round-N.md`
  ordering rule lives. The new check resolves `round-N` through it rather
  than writing the pattern a third time.
- `docs/review-chain-spec.md:34-56` — the bound, and `:157-159`, the paragraph
  that closes the findings and is silent about the answers. Both are amended
  at their own coordinates rather than by a new section that contradicts them.
- `docs/review-handoff-protocol.md:110-119` — the record's field table, and
  `:163-166` the paragraph the spec quotes. The protocol is tool-agnostic, so
  the field goes in as a shape rather than as this plugin's implementation.
- `templates/sdd-round.md:10-32` — the field table and the `Pass` comment. A
  session bootstraps from this file and never reads the argument.
- `skills/code-review/SKILL.md:99` — the cross-session records heading still
  names `.specseal/handoff/PR-<n>/`, a directory
  `docs/review-handoff-protocol.md` says was never once created. That is the
  section option A is written into, so it is corrected in the same edit; a
  heading naming a dead path above new instructions is worse than either
  alone.
- `specs/1788184145-…/rounds/round-3.md:8` — the one of this repository's
  three existing records whose honest value is `nobody`. Rounds 1 and 2 name
  the round that followed them, so all three gain the row and only this one
  discloses a gap. Their declaration is added relative to `main`, so the
  release pull request reads all three.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **B + A, as scoped** | A run that legitimately reaches the cap with unopened fixes still ships, because `nobody — <why>` passes everywhere. The gap is visible on every CI run rather than closed | Taken first, and superseded in phase 7 by the row below. It was the issue's own framing of B — *makes the gap legible without closing it* — with A as the thing that closes it in practice |
| **B + A, with `Pass` beside `nobody` failing everywhere** | The three merged records this repository already carries go red, and there is no honest repair: writing a `round-4.md` for a review nobody ran is fabricating one, and unchecking `Pass` fails the ready-pull-request rule instead. The release pull request would be red until someone spawned a round for work that has already merged | Not taken. It was Q1's first option and the reason the question existed |
| **B + A, with `Pass` beside `nobody` failing for work items begun after the rule lands** | An old work item reopened years from now still writes records under its original id and stays excused. Nothing dates a work item except its own directory name | **Taken**, in phase 7, and it is the repository owner's answer to Q1 — a third option neither the row nor round 1's review had put on the table. A check whose first production act is red on merged history nobody can repair is a check people learn to skip; a check whose strongest statement is a print does not stop a failure mode measured at a 100% hit rate |
| **C — the chain ends at a round with no findings** | Unbounded in the bad case, and at the cap it stops with the same gap one step later. A round closing a 🟡 with grounds would be forced to continue | Rejected by the repository owner before this work started |
| **A alone** | The verifying round is prose, and prose is what the incident report says was already there. Nothing in git would say whether a run had one | Rejected — B is what makes A checkable |
| **B alone** | The record names the gap and nothing closes it. Round 2's seven defects would have been recorded as unfound rather than found | Rejected — the issue says A is the one that would have caught them |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **B.** The field: `docs/review-handoff-protocol.md` (draft 0.5), `docs/review-chain-spec.md`'s two-claims paragraph, `templates/sdd-round.md`, the reminder in `hooks/review-history-guard.py`, `chain_check.py`'s reader and its refusals, `tests/test_the_last_rounds_fixes_are_checked.py`, and the migrated rows on `specs/1788184145-…/rounds/round-{1,2,3}.md` | the new test file with every case shown red under a mutation, plus `test_chain_check_at_the_pull_request`, `test_handoff_outlives_the_merge`, `test_release_hygiene`, `ruff` | `607362b`, and the per-record read at `edbf994` |
| 2 | **A.** The verifying round: `docs/review-chain-spec.md`'s bound and its new section, `skills/code-review/SKILL.md`, `agents/warden.md`, `agents/smith.md` | the new test file's A cases, plus `test_docs_line_wrap`, `test_one_word_one_meaning`, `test_the_set_a_work_item_always_has`, `test_review_axes`, `test_broad_gate_rule`, `test_edits_go_through_the_edit_tool` | `edbf994` |
| 3 | The outward-facing prose: `README.md`, `README.ko.md`, `.specseal/README.md`, `templates/specseal-README.md` | `test_docs_line_wrap`, `test_the_set_a_work_item_always_has`, `test_no_real_identifiers`, `test_what_the_reader_understands` | `dba039e` |
| 4 | The `## Unreleased` changelog entry, the ledger rows and the closing memo. (`questions.md` was written with the rest of the SDD set, before implementing) | `test_release_hygiene`, `test_ledger_stamps_resolve`, `evidence_check.py`, `unverified_check.py` | `5eecb45` |
| 5 | **Round 1's 🔴 1.** `verdict_of` sees through markdown emphasis and the commit citation, so `open_blocking` and `closed_with_a_fix` fire on the spelling every record in this repository uses | four new cases in the test file, each red under one of two mutations — the old normalizer, and a reader that looks for a fix word anywhere in the cell | `ef1cfba` |
| 6 | **Round 1's 🔴 2, and 🟡 4 and 🟡 6.** Option A's three axes pinned as whole rows and sentences with the inversions refused beside them; the `nobody` trade pinned by a needle unique to its own section; the template row counted outside comments and its value pinned | the same file, nine mutations across four carriers, the template and the check's docstring | `60e4cb8` |
| 7 | **Q1, answered.** `Pass` beside `nobody` fails on the last record of a work item begun on or after `STRICT_FROM`, and the policy clause goes back into `docs/review-chain-spec.md`, `docs/review-handoff-protocol.md`, both READMEs, the template, the skill and `agents/smith.md` | five new cases, two mutations (the cutoff inverted, the two claims dropped), plus the twelve narrow prose files | `6f0db50` |
| 8 | **Round 1's 🟡 5, 🟡 9 and 🟡 10.** A named checker's own `Target SHA` has to be later; the three uncovered branches get cases; `Needs a fix` gives the run's terminal condition a field in the record, the reviewer's report and the protocol | eight new cases, six mutations, and `test_edits_go_through_the_edit_tool` for the apostrophe parity the added prose had to keep | `225b9b7` |
| 9 | **Round 1's 🔴 3, 🟡 7 and 🟡 8.** The memo says what the code does, the spec and the plan stop contradicting each other and the code, the citations name a file that exists, and Q2 carries the merged-record cost | `test_the_set_a_work_item_always_has`, `test_docs_line_wrap`, `evidence_check.py`, `unverified_check.py`, `test_release_hygiene` | `851fa90` |
| 10 | **Round 2's 🔴 1, and the two real holes under its six surviving mutations.** `verdict_of` matches the vocabulary as a prefix of the cell and `CITATION` is deleted; `reviewed_later` reads both records at their newest `Target SHA` | seven mutations, each shown red and the tree restored green: the citation cut restored, the prefix anchor dropped, the word boundary dropped, either side of `reviewed_later` read at its first SHA, the squash path deleted, and the cutoff narrowed to `>` so the item that wrote the rule excuses itself | `8a5628a` |
| 11 | **A malformed ledger row, found by the orchestrator.** Two rows in `.specseal/map.md` quoted a table row by name with its pipes and split into seven cells; on one the `Checked` column landed on prose and the row was silently measuring from the header baseline | a per-section shape parse — 19 rows, 0 malformed, every `Checked` cell carrying a SHA — plus `test_ledger_stamps_resolve` and `evidence_check.py` | `3002dbb` |
| 12 | **Round 2's prose findings.** The refusal table and the skill carry the checker's-own-`Target SHA` condition; both READMEs tell one story about `nobody`; the spec's introduction stops contradicting its own table; the memo, the plan and the spec agree on how many records exist; six prose coordinates re-aimed; the reviewer's line is copied without its label | the twelve narrow prose files, and the protocol's `Needs a fix` row shown red under a rename to `\| Needs fixing \|` that left the phrase case green | `9b5501d` |
| 13 | Q3's first measurement recorded, the ledger rows and stamps, the changelog and the memo | `evidence_check.py`, `unverified_check.py`, `test_release_hygiene`, `test_ledger_stamps_resolve`, and the check run against a fresh clone in both directions | this commit |

Phase 1 is one vertical slice: a record with the field, written by a session
from the template, refused by the check when it lies, and the one existing
record migrated in the same commit. Phase 2 is the second slice — the same
rule stated where the sessions that run the chain read it.

Phase 1 before phase 2 deliberately. The field is what a verifying round has
to write into, so building the procedure first would describe a cell that does
not exist.

Phase 1 shipped reading the field on the last record alone and phase 2's
commit changed it to every record. That was not a change of plan: mutation
testing showed the first scope made `round-N` unreachable, so a third of the
vocabulary could never be used. The memo's divergence table carries it, and
what it costs a repository updating the plugin is Q2.

Phases 5 to 9 are round 1 of this work item's own review, and they are phases
rather than an appendix because three of them change what ships. The rounds
are the reason phases 1 to 4 are not the whole plan: the review found that
neither refusal reading a verdict cell had ever fired, and that option A's
rules could be written backwards with the suite green.

Phases 10 to 13 are round 2, the first verifying round this repository has
run, and its target was `617d0c0..2ea13da` — the diff of round 1's fixes. It
opened a 🔴 at the same site round 1 was closing, which
`docs/review-chain-spec.md:34-56` calls the structure signal whatever the
count, so the repository owner was asked and answered: change the structure,
do not add a second special case to the pattern. Phase 10 is that answer.

## Operational impact

**A behaviour change in CI, and it is the point of the work.** A pull request
whose declaration routes through the review chain now fails when **any** round
record in a touched work item carries no `| Fixes checked by |` row. Every
round record written before this release lacks it. This repository carries
three, all in `specs/1788184145-…/rounds/`, and all three are migrated in
phase 1; a repository that installed the plugin and updates it gets a failure
naming the row and the three values it accepts, which is the same trade
`docs/review-handoff-protocol.md` records for the `rounds/` move — no
fallback, bought back with a message.

**And a second one, from phase 7.** A checked `Pass` beside `Fixes checked by:
nobody — <why>` on the last record now fails, for work items whose directory
name begins with a unix second at or after `chain_check.py`'s `STRICT_FROM`.
Earlier work items print instead. Nothing is configured: the cutoff is one
constant compared against a number already in every work item's directory
name.

No migration script, no new environment variable, no new dependency.
`.claude-plugin/plugin.json` stays at `0.0.1`; the pull request lands on
`release/v0.0.2`, so the entry goes under `## Unreleased`.
