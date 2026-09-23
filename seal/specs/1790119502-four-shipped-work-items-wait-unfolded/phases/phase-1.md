# 1790119502-four-shipped-work-items-wait-unfolded — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b80aaac |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Open `overview.md`, which turns
`tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview`
green again, and record the measurements `spec.md` states — settle's list by
name, the corpus counts, the floor table, the #511 grep, and L1–L11 with their
evidence — re-derived by the command that produced each, not copied. L2 goes
into `overview.md` §*Not verified*; Q1 was already answered as #515 before the
spawn, so the row names that issue rather than waiting for it.

## What this phase found

**The overview test was red before this phase, as the frame said.** Run at
`8798435`: `1 failed` — `work items with no closing overview:
['1790119502-four-shipped-work-items-wait-unfolded']`. Green after
`overview.md` is written (the commit closing this phase).

**`./bin/settle`, read whole at `8798435`, exit 0:** 4 released and unfolded
in 4 segments, 11 ungrouped, 0 skipped, 1 unreleased. By name:

| Segment | Work item |
|---|---|
| `.github/scripts/close_issues_on_release.py` | `1790076050-the-release-tail-is-three-acts-no-document-names` |
| `docs/review-chain-spec.md` | `1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys` |
| `seal/ledger.md` | `1790076070-the-fold-ships-and-the-corpus-is-still-on-disk` |
| `skills/verify/scripts/session_cost.py` | `1790076080-every-orchestrator-rule-is-a-sentence` |

The 11 ungrouped are `1788177600`, `1788184145`, `1788217118`, `1788220055`,
`1788276387`, `1788395377`, `1788425222`, `1788824000`, `1788938400`,
`1789024700` and `1789053786`, each `(no ledger row)` — the same 11 #497 kept.

**The corpus, by `find` and `git ls-tree`:** 16 directories and 109 files
under `seal/specs/`; the four hold 71 files. `spec.md` says 106 files at
`cb07876`, and the difference is the three frame files `c0e7bf9` added after
that moment — the same number measured at two moments, not a divergence.
Committed round records at HEAD: 17, of which the four hold 10; 7 remain.

**The floor table, each figure re-counted:**

| # | Now → after the four go | How it was counted |
|---|---|---|
| F1, F2, F5, F11, F12 | 17 → 7 records | `git ls-tree -r --name-only HEAD -- seal/specs`, paths matching `/rounds/round-[0-9]+\.md$` |
| F3 | 10 → 0 records carrying `\| Fix range \|` | `grep -l '^\| Fix range \|'` over the same list |
| F4 | 6 → 2 work items with rounds (`1788184145`, `1788395377`) | the same list, cut at the directory |
| F6 | `1788395377`'s rounds 1–4, kept | unchanged by this branch; phase 5 runs the case |
| F13, F14 | 16 → 12 `routing.md` | `ls seal/specs/*/routing.md` |
| F15 | 4 → 4 `pr.*.md` | `ls seal/specs/*/pr.*.md` — `1788184145`, `1788217118`, `1788220055`, `1788395377`, none in the four |
| F16 | 113 markers, unchanged | `grep -c '<!-- specs/' seal/ledger.md`; the floor is `>= 90` |
| survivor corpus | 5 → 2 `survivors.md` (then 3 with this branch's own) | `ls seal/specs/*/survivors.md` |
| the class | 160 hits in 49 modules | `grep -rn "seal/specs" tests/` and `grep -rln` |

No `evidence-todo.md` or `tests-todo.md` exists anywhere under `seal/specs/`,
so the retirement's guard holds nothing back.

**#511, re-checked.** `grep -nE 'seal/specs/17900760[5-8]0' seal/ledger.md`
exits 1 and `seal/ledger/` does not exist. Narrowed to anchors — every
backticked `seal/specs/…#…@hash` in `seal/ledger.md` — the only one is
`1788184145-…/rounds/round-3.md`, a kept directory. Phase 5 re-runs it
immediately before the removal.

**L1–L11, each opened:**

| # | Evidence read in this phase | State |
|---|---|---|
| L1 | `gh run view 35796549648`: `publish the release note`, event `push`, ref `v0.13.1`, conclusion `success`; `gh release view v0.13.1` returns the release | closed by observation |
| L2 | `gh run view 35796513013`: `close issues on release` on `main`, step *create the labels the documents specify and the tracker lacks* `failure`, step *roll the flow-measurement issue to the next version* `skipped`; `gh label list --search size` returns nothing | open — `overview.md` §*Not verified* names #515, which the orchestrator filed (`gh issue view 515`: open, `release: 0.13.2` milestone) |
| L3 | the last round record of each chain: `1790076050` round 3 `Broad gate` = `59a72d91 against 6d410023`; `1790076060` round 2 = `e62b5864 against 756b7b35`; `1790076070` round 2 = `49ee16ad against 64036785`. `1790076080`'s row is already ✅ in its own overview | closed by those cells |
| L4 | `gh issue view 499`: open, backlog — the case that reads `release` out of its own interpreter path | homed at #499 |
| L5 | `1790076050`'s overview names the repository owner; `docs/release-checklist.md` §6 states the unknown | phase 2 rewrites the pointer |
| L6 | `1790076060`'s overview carries two rows — `CAPPED_EXIT` and `DEPTH_EXIT` — as one pair owed the same act | phase 4 writes the sentence |
| L7 | `1790076070`'s overview row; that fold's two rounds closed with `no fixes to check` | closed |
| L8 | `1790076070`'s overview names the owner and `seal/ledger.md` §1788354065's S12 row; #511 open | homed there |
| L9 | the four files exist: `docs/the-evidence-ledger.md`, `docs/the-broad-gate.md`, `docs/measuring-a-run.md`, `docs/the-agent-set.md` | closed — they stand |
| L10 | `1790076080`'s overview row on Q3 | phase 4 writes the rule |
| L11 | `gh issue view 506`: open, backlog — the three enumerations | homed at #506 |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
