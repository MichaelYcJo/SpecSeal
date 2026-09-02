# 1788331011-two-roots-hold-three-lifetimes — review round 4

<!-- seal/specs/1788331011-two-roots-hold-three-lifetimes/rounds/round-4.md — the
verifying round the run ends on: it opened round 3's fix (e19c9ee..9717028)
and nothing needing a fix, so it does not consume the cap. Written by the
review orchestrator after the report was verified and the broad gate ran. -->

| Field | Value |
|---|---|
| Target SHA | 4250a71 (the fix diff is e19c9ee..9717028; 4250a71 is round-3's record edit only) |
| PR | not yet opened |
| Broad gate | 4250a71 vs origin/release/v0.4.0 — `pytest tests/ -n auto` 1298 passed · 1 skipped, `ruff check .` clean, `ruff format --check .` 78 files formatted, `evidence_check.py --strict .` 220 ok · 0 drifted · 0 broken, `unverified_check.py --baseline` exit 0 (13 overviews · 30 open · 13 closed · 0 unreadable). The delta after the run is this record, round-2's separator cell, round-3's `Fixes checked by` cell and `pr.ko.md` — docs-only, the non-invalidating class |
| Fixes checked by | no fixes to check |
| Contract changes | none — this round wrote no fixes |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 3-H | round-3 🟡 H (a linked `specs/` half-moved under a stamp with a broken ledger) | `hooks/root-migrate.py#main` (the `specs/` link refusal), `spec.md` refusal table row and order sentence | answered — the fix is round-3's, this round reproduced its closure | planted test executed red against e19c9ee's hook with the half-move line (`seal/` present, stamped, checker `2 ok · 2 broken`, second start silent), green at 4250a71 on two starts (`seal/` absent, `.specseal/map.md` byte-identical, not stamped); the four orderings executed: a migrated repository keeping `specs → seal/specs` stays silent, a throwaway repository gets the scratch line, a linked `specs/` holding no item takes the normal path, a linked `specs/` with a dirty `.specseal/` gets the link line first |
| 🟢 3-I | round-3 🟢 I (the `.specseal/` link line on a migrated repository keeping a link) | `spec.md` refusal table, the `.specseal/` row | answered — record only | the clause is in the row and names the cost; read |
| 🟢 3-J | round-3 🟢 J (two extra `ls-files` in `dirty()`) | `overview.md` Not done | answered — record only | the new refusal adds no git process off the link path (`islink and any(…)` short-circuits); read |
| 🟢 K | no `.specseal/` at all and a linked `specs/` full of items is silent and unstamped, while the same tree with a real `specs/` moves and stamps | `hooks/root-migrate.py#main` (the "nothing old left" branch runs before the link check) | record only — no fix | executed both shapes; nothing of SpecSeal's is behind the link (no ledger exists), and the spec's *nothing old left* row covers it as written. Reading says the link line appears once a `.specseal/` shows up (a branch switch); not executed |
| 🟢 L | the item filter `ITEM_RE.match(n) and os.path.isdir(…)` is written twice, in `old_items` and in the link refusal | `hooks/root-migrate.py#old_items`, `#main` | nit, no fix | read; a drift between the two would make the refusal and the move disagree on what an item is |
| 🟢 3-fix-surface | round-3's `Contract changes: none` and `New units` (one test) | `rounds/round-3.md` | truthful | `old_items` has three uses, all inside the hook; `main` is reached from `hooks/dispatch.py` and the test's `start()` only (grep over `hooks tests skills`); the test fails against e19c9ee on its first assertion with the hook's line and writes only under `tmp_path` |
| ❓ 2-G, ❓ 1-a, 🟢 1-10 | the deferred items | — | still deferred | CI's legs; the PR body |

## Executed probes

| What was run | Result |
|---|---|
| the planted test against e19c9ee's `root-migrate.py` (scratch copy) | red on its first assertion with the half-move line; `seal/` present, stamped, `2 broken`, second start silent |
| the planted test and its `.specseal/` sibling at 4250a71 | both green, two starts each |
| a migrated repository (`seal/` present, nothing old) keeping `specs → seal/specs` as a link | silent, stamped by the "nothing old left" branch, link intact |
| `.specseal/scratch` committed + a linked `specs/` holding an item | the scratch line, not the link line; not stamped |
| a linked `specs/` holding only `notes/` | the normal path: `moved .specseal/ into seal/ (1 ledger row re-pointed; left specs/notes …)`, stamped |
| a linked `specs/` holding an item + an unstaged edit under `.specseal/` | the link line, not the dirty line; nothing moved, not stamped |
| no `.specseal/`, a linked `specs/` full of items; and the same with a real `specs/` | silent and unstamped; moved and stamped |
| `evidence_check.py --strict .`; the fragment alone | 220 ok · 0 drifted · 0 broken; 60 ok |
| `grep` for `old_items` and `main` callers over `hooks tests skills` | inside the hook; `dispatch.py` and the test's `start()` |
| the broad gate at 4250a71 (orchestrator) | see the field above |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-3 | `hooks/root-migrate.py#main` (the order of the seven checks) | 🟢 K's asymmetry lives in the order; anyone moving a check moves it |
| round-1 | `hooks/root-migrate.py#dirty` | ❓ 1-a (Windows) is answered by CI, and 🟢 J lives here |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟢 1-10 the eight defaults of questions.md | the PR body, at opening | the orchestrator |
| ❓ 1-a Windows porcelain / pathspec | CI's windows leg on the PR | CI |
| ❓ 2-G case-insensitive filesystems | CI's macOS / Windows legs on the PR | CI |
| 🟢 K the no-`.specseal/` asymmetry | this record only; the spec's *nothing old left* row covers it | nobody — recorded |
| 🟢 L the filter written twice | this record only | nobody — recorded |
