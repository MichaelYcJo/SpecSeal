# a second fold writes a second heading — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the goal, the merge table, the fragment rule, the ledger's REMOVED and re-read rules), `CONTRIBUTING.md` §*What a change to a gate must carry*, `docs/release-checklist.md` §2, `docs/branch-and-release.md` §*The ledger fragments fold in the same commit*, `docs/one-root-by-lifetime.md` §*What happens at a release*, `docs/review-chain-spec.md` §*The depth in `New units`*, §*Where a leftover goes*, `docs/review-handoff-protocol.md` §*The handoff before round 1* and the record-fields table, `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it*, `templates/sdd-round.md`'s `Broad gate` row, `templates/sdd-phase.md`, `skills/agent-contract/SKILL.md` §1–§15, `seal/specs/1790206437-…/{routing,spec,plan,questions}.md`, `seal/specs/1790174138-…/rounds/round-3-report.md` §Paste-ready fixes, `seal/specs/1790173209-…/survivors.md`, `seal/follow-up.md`, MichaelYcJo/SpecSeal#540, #542, #366, #289, #174
· evidence: `seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md` F1–F3, B1–B2, D1 (25 coordinates, stamped by `evidence-check --reverify`); in `seal/ledger.md`: the second `## 0.9.3` heading removed, A11 corrected in place, and fourteen rows whose anchors this work moved re-read with dated notes and re-stamped (four on `fold_ledger.py#main`/`#section`, A9 on `kept_broad_gate`, A5 on `new_broad_gate_file`, the orchestration seam row, seven on the three convention carriers' sections and one on the ledger section that holds one of them)
· verified: executed — the hygiene module (46), the fold, gather and hygiene modules together (120), the seal and cell modules (130), `test_the_fixes_close_the_record.py -k broad_gate` (1), the report-standard, line-wrap and floor-and-depth modules (114), the one-owner, one-word, moved-rule and survives modules (314), the line-wrap and correction modules (81), every module that reads an edited document or script (the run in `phases/phase-5.md`), eleven mutations across the four phases, the real-tree `--check` over a copy of `9f846733`'s ledger, `evidence-check --strict .` at every phase close, `correction-check`, `survivor-check`, `unverified-check`, ruff over every edited `.py`; read — the ledger rows' claims against the edited units, the two further #542 carriers against the template's clause; unverified — the broad gate, the sealer's

## Why this work exists

Three sentences the 0.15.0 run found and could not fix: the fold wrote a
second `## 0.9.3` and nothing refused it, every `broad-gate.md` was written
with a comment describing a rule the code no longer follows, and a finding
straddling two depths had its depth-1 units refused. Now the fold joins and
`--check` refuses, the written comment says what the writer does and a case
reads it, and the reviewer splits the finding.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `skills/code-review/orchestration.md` | `spec.md` §Data & interfaces lists it under *Unchanged on purpose*, while S11b and judgment 10 send phase 3 to reword its sealer paragraph | reworded, in one clause each for the two sentences that stated the replaced rule | the spawn prompt repeats S11b; the unchanged list is wrong by one file (`phases/phase-3.md`) |
| The kept date in `main` | `plan.md` and `spec.md` §Data & interfaces have `main` keep a found date beside the date line | no override: `insert` drops the block's heading and `main` prints the file's own, so the kept date is theirs | measured dead by mutation — both kept-date cases green with the override disabled (`phases/phase-2.md`); the date line stays byte-identical as asked |
| The frame's ledger coordinates | `spec.md` S15 and `plan.md` §Technical context wrote four rows as a short path beside a hash | the stamps dropped, the units named with full paths | `evidence-check --strict`'s records arm refuses a short-path stamp as a file not found once the work item has a fragment — the same finding `1790174138`'s phase 1 met |
| `--dry-run --version 0.15.1` over this tree | `plan.md`'s phase 2 verification expects a fresh heading | exit 1, *nothing to fold*: this branch holds no fragment until phase 5 writes its own | executed and recorded (`phases/phase-2.md`); the fresh-heading path is the fixture's `test_dry_run_writes_and_removes_nothing` |

## Not verified

| Item | Who must answer |
|---|---|
| the broad gate — the full suite, the repository-wide lint and format check — over the settled branch | the sealer, spawned by the orchestrator after the review rounds settle |

## Not done

**Two folded work items stand in `seal/ledger.md` with their marker line
twice.** `1790173106`'s and `1790174138`'s fragments each began with their
own `<!-- specs/<id> -->` line, and the 0.15.0 fold copied it under the
marker it writes, so `fold_ledger.py --check` counts 118 work items marked
where the folded sections number fewer (executed: `grep -c` of each marker
line reads 2). This item's fragment carries no marker line and its comment
says why; the two standing duplicates, and whether the fold should drop a
marker line from a fragment's body, are outside the three tickets and are
named in the hand-back for the reviewer.

**Q4 measured none.** `survivor-check --range origin/release/v0.15.1...HEAD`
at `1c6e82d4` examined 396 files against 30 removed sentences and found no
removed wording standing, so no `survivors.md` is written; the gatherer's
date line was not reported.

## Fed back into the spec

none — the three sentences were already in the round records that found
them; `docs/release-checklist.md` §2 and `docs/review-chain-spec.md` §*The
depth in `New units`* each gained the one sentence the spec asked for.
