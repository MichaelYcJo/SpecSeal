# 1790119502-four-shipped-work-items-wait-unfolded — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | fb682a0 (the retirement); 7a1e453 (survivors and changelog); this record's commit closes the phase |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Run `plan.md`'s fixed order: `./bin/settle` compared by name; the #511 grep
immediately before the removal; `settle --retire` and then `git add -A` and the
commit in the next command, nothing else in that commit; then
`unverified-check --baseline`, `chain_check.py` on both bases,
`evidence-check --strict`, `survivor-check` with this branch's `survivors.md`,
and every module that reads the real `seal/specs/`, each exit read directly.
Write `survivors.md` and `changelog.md`. Answer Q2 and Q3 by measurement.
The broad gate is not this phase's.

## What this phase found

**Step 1 — `./bin/settle`, by name.** `0 work items in 0 segments, 11
ungrouped, 0 skipped`; under *folded already, waiting to be retired* exactly
`1790076050`, `1790076060`, `1790076070` and `1790076080`. The 11 kept ids are
the ungrouped list and none of them is in the waiting list.

**Step 2 — #511.** `seal/ledger/` does not exist, and
`grep -nE 'seal/specs/17900760[5-8]0' seal/ledger.md` exits 1. No row anchors
under the four; the retirement went ahead.

**Step 3 — the retirement.** `settle --retire` exit 0: `removed` for each of
the four and `retired 4 work items; 0 kept`. The next command staged and
committed it as `fb682a0`: 71 files, every one a deletion, all under the four
directories. `ls seal/specs` → 12: the 11 kept by name and this one (A2).

**Step 4, each exit read directly.**

| Check | Exit | What it said |
|---|---|---|
| `bin/unverified-check --baseline origin/release/v0.13.2 seal/specs/` | 0 | `5 overviews · 7 open · 2 closed · 0 unreadable · 4 folded`; each of the four removed overviews reported *folded*, none as a deletion (A5) |
| `chain_check.py --baseline origin/release/v0.13.2` | 1 | four `retired:` lines, one per removed `routing.md`; the only error is this work item's own `rounds/` holding no `round-N.md` (A6) |
| `chain_check.py --baseline origin/main` | 1 | the same four `retired:` lines and the same single error |
| `bin/evidence-check --strict .` | 0 | `1468 ok · 0 drifted · 0 broken` (A8) |
| `bin/correction-check --range origin/release/v0.13.2...HEAD` | 0 | no merge commit in the range |
| `bin/survivor-check --range origin/release/v0.13.2...HEAD --exempt …/survivors.md` | 0 | every survivor excused by the range row (686) (A7) |
| the 44 test modules `grep -rln "seal/specs" tests/` names, `conftest.py` aside | 0 | `2315 passed, 1 skipped` (A9) |

**Q2 is answered: green.** Every module in the floor table and every
real-corpus reader passes on the folded tree, and no floor needed an answer
beyond *decline*: `git diff origin/release/v0.13.2 -- tests/` is the four
docstring citations and nothing else, so no literal moved. The class is 44
modules and not the frame's 49 because the four docstrings no longer name a
`seal/specs/` path, and `conftest.py` is imported rather than run.

**Q3 is answered: yes.** Both bases print `retired:` for all four
declarations. The arm #497 built on 88 removals holds on four against a
different base.

**A3.** Outside this work item, the four ids now stand only in fold markers
(`docs/`, 14 lines across five files), in the five citations that name
`1790076050` as provenance (four docstrings, one `docs/` sentence), in
`CHANGELOG.md`'s four gathered markers, in `seal/follow-up.md`'s four
provenance notes, and in `seal/ledger.md` (36: the frame's 33 plus the three
`Re-read` notes phase 4 wrote). No file outside this work item names
`b0cbd34`.

**A8.** `git diff origin/release/v0.13.2 -- seal/ledger.md` is four rows, each
a hash and an appended `Re-read` note: S9 (phase 2) and C1, C3, C4 (phase 4).
No row was added, removed or re-pointed.

**No ledger fragment was written.** Every fact this work opened is either a
re-read of an existing row or a measurement of a moment recorded in these
phase records; none is a new claim about code, so `seal/ledger/<id>.md` would
have had nothing to hold.

`gather_changelog.py --check` exits 1 on this branch because this fragment is
not gathered yet, which is what a feature branch into a release branch looks
like; the hygiene workflow runs that check only into `main`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/` | `docs/branch-and-release.md` §*Cutting a release*, two markers |
| `seal/specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys/` | `docs/review-chain-spec.md` — the cap and ladder subsections, four markers |
| `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/` | `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*, four markers |
| `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/` | `docs/measuring-a-run.md` §*Where a reading goes* (two markers) and `docs/the-agent-set.md` (one) |
| the open `## Not verified` rows of the four overviews | L1–L11 as `phases/phase-1.md` homes them; L2 is this work item's open row naming #515 |
