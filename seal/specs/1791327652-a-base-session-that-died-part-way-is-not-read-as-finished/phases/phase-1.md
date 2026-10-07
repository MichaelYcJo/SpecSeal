# 1791327652-a-base-session-that-died-part-way-is-not-read-as-finished — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 57eb5307 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The plan's one phase, from work item 1791270161's round-6 report. Fix 🟡 1 and ⬜ 2 by the report's paste-ready fixes, adapted where the tree needs it, with rule 3's sentence and its pin. Plant S1–S6 and show each new case red at 6de64c19 first; for S5, say so where a replaced worker cannot be provoked and state the read. Run `bin/mutation-check` on each new unit. Add ⬜ 3's row to work item 1791270161's `overview.md` divergence table, edited in place because that item is merged and unreleased. Write this item's changelog fragment, ledger fragment rows, `overview.md` and this record. `bin/evidence-check --strict .` and `survivor-check --range origin/release/v0.20.0...HEAD` must exit 0. Run only the slices the plan names, not the full suite or the broad gate, and do not push.

## What this phase found

- **S1 and S2 were red for the right reason.** At 6de64c19's gate both gate cases read `tests/test_two.py  new`, with a base record holding no `end` line, exactly as round 6's probe recorded. The two unit cases (S4 and the `read_record` case) were red only on the missing `unended` attribute, so their logic was shown red afterwards by mutation: the count not taken, the check removed, the count read from `sessions`, and the two checks swapped.
- **Keying on the worker needs it to be hashable.** `id()` accepted any object; the object itself does not. xdist 3.8.0's `WorkerController` defines no `__eq__` or `__hash__` · NAME NOT IN TREE, so it is keyed by identity, but a plugin that sets `report.node` to something unhashable would have raised out of a report hook. `path_of` now reads such a `node` as no sender.
- **S5 depends on the allocator in one direction only.** On CPython 3.13 a freed plain `object()` gives its address to the very next one, so at 6de64c19's recorder the case is red on the first object made. An instance of a class the case defines did not reuse the address within a thousand objects, so the case uses `object()`. With the fix the recorder holds the old worker, so no later object can take its address, and the case cannot pass by luck.
- **One mutation survived the new case alone.** Keying only the setter on `id()` leaves the getter finding nothing, so the S5 case, which asserts only that nothing is inherited, stays green. Round 5's `test_a_crash_report_takes_a_path_only_from_its_own_workers_report_of_it` turns red on it, so the unit is covered by the two cases together.
- **Three rows of 1791270161's ledger fragment went stale by omission.** W5, W8 and `Corrected · D1` each listed every way `new` turns into `new?`; each now names the unended session, with this item's U1 or U3 row cited. The other 27 rows citing a coordinate this phase moved were read and re-stamped; no released row was owed a `Re-read ·` row, because the 1791270161 fragment's own re-reads hold their families.
- `survivor-check` found no removed wording still standing, so this item needs no `survivors.md`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `Recorder.path_of`'s map keyed on `id(sender)` | `none` — replaced by the map keyed on the worker itself (ledger U2) |
