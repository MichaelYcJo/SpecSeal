# 1790297085-settle-retires-a-directory-main-has-not-seen-closed — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this work item; `docs/one-root-by-lifetime.md` §*Decided when the fold stopped being a work item (2026-09-23)*; `docs/the-evidence-ledger.md`'s rule-arm statement; `skills/settle/SKILL.md` §1; `docs/branch-and-release.md` §*The changelog entries arrive as fragments, and the release gathers them*
· evidence: `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md`; re-read rows are named in each `phases/phase-N.md`
· verified: executed and read are labelled in each `phases/phase-N.md`

## Why this work exists

`settle --retire` could remove a directory CI then refuses at the release pull request, three shipped scripts reported a missing sibling as a finding, and the changelog gatherer let a fragment's own `## ` line cut the released section short; each now refuses at the point the rule already stated.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How `settle.py#load` and `round_record.py#load` learn what a missing sibling is for | `plan.md` §*Phase 1*: "Give it `fold_check.py`'s `purpose` parameter". The code keeps `load(path, name)` and looks the purpose up in a module-level `PURPOSES` table | the table | 22 call sites in `tests/` pass two arguments, and two cases monkeypatch `settle.load` with a two-argument lambda; a table keyed by the path cannot be handed the wrong purpose by a call site. `round_record.py` keys it by file name because two of its siblings' paths are `chain_check.py`'s. `phases/phase-1.md` has the measurement |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck over the whole branch | the sealer, once, after the review rounds settle |

## Not done

`questions.md` Q3, catching a fragment's `## ` line at the fragment's own pull request, is not built: the milestone adds no gate.

`skills/verify/scripts/payload_meter.py#_session_cost` still dies with a traceback at exit 1 when its sibling is missing. `spec.md` §Scope *Out* puts it outside #590's class, because the meter's 1 already means *could not measure* rather than a finding; the orchestrator files it or leaves it.

`chain_check.py` was not edited (work item A owns it this release); its exit 2 for a missing reader is pinned by this work item's class case alone.

## Fed back into the spec

none
