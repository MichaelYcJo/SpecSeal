# Implementation Plan: four shipped work items wait unfolded

<!-- seal/specs/1790119502-four-shipped-work-items-wait-unfolded/plan.md — HOW,
in phases. This is the Design Gate's artifact. -->

Approved 2026-09-23 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

Five phases for four work items. The first records what the frame measured
and closes the red the frame itself opens; the second resolves every
reference into the four directories while they still exist; two write the
prose, grouped so that each touches as few anchored ledger units as possible;
the last retires the four and re-runs everything the removal could break.

The references come before the prose and the prose before the removal for the
reason #497's order was fixed: a rewrite has to be checkable against the file
it points at, and a removal is only a fold once the marker covering it is in
`docs/`.

## Technical context

- `skills/settle/scripts/settle.py` — `settle` groups; `settle --retire`
  removes `marked & present & released` minus anything an open
  `evidence-todo.md` row holds. The keep-list is enforced by **not writing
  those ids as markers**, never by editing the script.
- `skills/verify/scripts/unverified_check.py#folded_items`, `#live_lines` —
  the fold record: a whole-line `<!-- specs/<id> -->`, live, at the top level
  of `docs/`.
- `skills/code-review/scripts/chain_check.py` — prints `retired: …` for a
  removed `routing.md` whose marker `docs/` carries (#497's repair,
  documented in `docs/review-chain-spec.md` beside the declaration table).
- `.github/workflows/hygiene.yml` — hands every `seal/specs/*/survivors.md`
  to `survivor_check.py` on a pull request into a release branch.
- `seal/ledger.md` — the anchored units `spec.md` G1 lists; nothing anchors
  inside the four directories (G3).
- `b0cbd34` — `main`'s merge of the release that shipped the four, and
  `origin/release/v0.13.2`'s tip. Every file of the four resolves there.

**What breaks in six months.** A folded sentence that a later work item had
already overturned becomes a rule nobody can trace, because the argument
left with its directory. The four are one release old and none overturns
another; the phase record names what was dropped rather than folded, so a
reader can find the difference in git history under the work item's id.

**The second thing that breaks**, and the reason for G4: an open
`## Not verified` row inside a retired `overview.md` is read as folded and
disappears. L2 is the measured instance — the only record that the label was
never created sits in a file this branch removes.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| One phase per work item | four prose commits for three destination files, and two of them edit the same anchored document for different reasons | rejected — prose grouped by how much ledger each touches |
| One phase for all prose | one commit re-verifying rows from two documents and adding markers to four; a reviewer cannot tell which drift came from which statement | rejected |
| 1790076050 into `docs/release-checklist.md` §6, its most literal home | §6 is an anchored unit, and the checklist is steps rather than rules; the item's rule is about who performs the release's acts, which `docs/branch-and-release.md` already owns with no anchored heading | rejected — `spec.md` G1 |
| 1790076050 into `docs/issues-and-milestones.md`, the segment's subject | the label is one of three acts, and the section carries four anchored rows | rejected |
| Rewrite a retired path as the fold marker alone | the marker says a work item was folded, not which file held the measurement; a reader loses the file | rejected at the frame, in favour of a pin to a commit on `main`. **Corrected 2026-09-23 in round 1's fix pass:** the pin was itself replaced during the build (`spec.md` G2), and the citation names the work item and the `docs/` section carrying its marker — the marker says which work item, and the id is what a reader traces through history |
| Cite `v0.13.1` or `0.13.1` instead of `b0cbd34` | the loaded-file timer refuses a version at or above the running one, and the running one is `0.13.1` | rejected |
| Repair the 26 older citations in the same pass | 15 files, three of them shipped scripts and one a hook, for a class the ticket did not name and `settle` §2 already answers with git history | rejected — `spec.md` O3 |
| Fix `tracker_labels.py`'s description here | a workflow behaviour change under `CONTRIBUTING.md` §*What a change to a gate must carry*, in a chore branch, without a ticket | rejected — `questions.md` Q1 |
| Leave the open overview rows to disappear with their directories, as #497 did | L2 — a red workflow and a skipped flow-log roll — would have no record anywhere once this branch merges | rejected — `spec.md` G4 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `overview.md` opened; `phases/phase-1.md` carrying the measurements `spec.md` states (settle's list by name, the corpus counts, the floor table, the #511 grep, L1–L11 with their evidence) re-derived rather than copied. L2 goes into `overview.md` §*Not verified* with the orchestrator as its answerer, because raising an issue is posting and `agent-contract` §6 withholds that from every agent | `test_every_spec_directory_that_reached_the_ladder_has_an_overview` green again; every figure in the phase record re-derived by the command that produced it | b80aaac |
| 2 | the six references resolved — four docstrings and `docs/branch-and-release.md:101` name their work item instead of a retired path (the `b0cbd34` pin this row first said was replaced during the build — `spec.md` G2), and `docs/release-checklist.md` §6's pointer names the repository owner (L5). `docs/release-checklist.md#"## 6. After the merge"` re-read and re-verified | `git cat-file -e b0cbd34:<path>` for each cited path; the four test modules and `tests/test_the_release_tail_does_not_end_at_the_tag.py` green; `tests/test_docs_line_wrap.py`; `bin/evidence-check --strict .` | 05a1c7e |
| 3 | the two statements whose destinations carry **no** anchored heading: 1790076050 → `docs/branch-and-release.md`; 1790076070 → `docs/the-evidence-ledger.md`, including #497's rule for the ungrouped and the grounds for keeping `1788184145` | `./bin/settle` no longer lists those two; `tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py`, `tests/test_the_release_tail_does_not_end_at_the_tag.py`; `bin/evidence-check --strict .` shows no new drift | b0e76ae |
| 4 | 1790076060 → markers on `docs/review-chain-spec.md`'s own sentences plus L6's sentence, with the drifted rows re-read and re-verified; 1790076080 → `docs/measuring-a-run.md` §*Where a reading goes* (with L10's rule) and one sentence in `docs/the-agent-set.md` | as phase 3, plus `tests/test_the_rules_have_one_owner.py`, `tests/test_a_segment_feeds_the_flow_log.py` and `tests/test_every_orchestrator_act_names_its_delivery.py`; `./bin/settle` reports 0 unfolded | dcbe48a |
| 5 | `settle --retire` in a commit of its own; `survivors.md`; `changelog.md`; the post-retirement re-run of the floor table and of A2–A10 | `spec.md`'s acceptance table, every exit code read directly | fb682a0 |

**Phase 5's order is fixed**, as #497's was:

1. `./bin/settle` — the waiting list compared **by name** against the four,
   and the 11 kept ids checked present and absent from that list. Three
   directories named anywhere else are a stop, not a count to reconcile.
2. The #511 re-check, immediately before the removal:
   `grep -nE 'seal/specs/17900760[5-8]0' seal/ledger.md seal/ledger/*.md` —
   the fragment glob too, since this branch may have written one. Any hit
   stops the phase and keeps that directory: the row holds it until the
   repository owner trades it the other way (`docs/the-evidence-ledger.md`
   §*The fold*). `CLAUDE.md`'s REMOVED rule decides only what the grep missed.
3. `settle --retire`, then `git add -A` and commit **in the next command**.
   The deletions are in the index before any check runs, which keeps #368 off
   this branch.
4. `bin/unverified-check --baseline origin/release/v0.13.2 seal/specs/`;
   `chain_check.py --baseline origin/release/v0.13.2` and `--baseline
   origin/main`; `bin/evidence-check --strict .`; `bin/survivor-check --range
   origin/release/v0.13.2...HEAD` with this branch's `survivors.md`; the
   modules in `spec.md`'s floor table and every module `grep -rln
   "seal/specs" tests/` names that reads the real tree. Each exit code read
   directly, never through a pipe.
5. Only then the hand-off. The broad gate is the sealer's single act.

**Where a destination turns out wrong**, the phase that reads the spec moves
it and says so in its record. Not open to that: a file below `docs/`'s top
level, a new document for an area one already covers, or a marker on the
anchored units `spec.md` O6 rules out.

**What each phase record says it dropped.** Every `## Out` clause, every
measurement whose number is a moment rather than a rule, and every rule
already stated in the destination — named, one line each, so the difference
between *not true* and *already there* is on the page.

## Operational impact

- **71 files and four directories leave the tree** in one commit; 16
  directories become 12 (11 kept by name, and this one).
- `seal/ledger.md` gains and loses no row. Rows whose anchored unit phases 2
  and 4 edit change hash and gain a dated `Re-read` note, and nothing else.
- No new `docs/` file. Three existing ones gain standing statements, one
  gains markers, one sentence in the checklist changes its answerer.
- L2's issue is the only thing that leaves the tree, and it records a red
  production workflow: the release-tail job has stopped at the label step
  since the release this fold follows, so the flow log was not rolled.
