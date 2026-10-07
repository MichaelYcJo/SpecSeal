# 1791270164-the-release-seal-is-drawn-in-curves — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 21089fa7 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md`'s phase 5 row as re-planned at `62f1b47d` and approved at `c85be7af`: the panel's rows in the owner's shape, in `broad_gate.panel` alone — `PANEL_VALUE_WIDTH = 41`, `SEP`, `ARROW`, `TICK`, `DOT`, `base` joined with its ref, `item_value` and `rounds_rows` on `·` and `→`, a `None` row before the result rows, the suite's pieces behind `✓`, the ledger's three counts, `chain ✓ exit <code>`, `CI also · <n> more steps`; `panel`'s docstring rewritten; `SAMPLE_ROWS` re-shaped; the `CI also` sentences in `skills/verify/SKILL.md` and `agents/sealer.md` given the dim `·`.

The spawn added: Q15 stays at its default (a), `CI also` keeps its label; every new case seen red at `c85be7af` first, then green; `bin/mutation-check` on each changed unit; only the panel and stamp slices run, never the full suite.

## What this phase found

**Three test modules the frame did not list pinned the old rows**, and one pinned the old width across two files.
- `tests/test_the_gate_asks_the_range_ci_will_ask.py` read the ref on the row under `base` in three places, and `test_the_documents_name_the_panel_row_the_gate_actually_prints` pinned `agents/sealer.md`'s *the row under `base` carries the ref*. Re-aimed to the joined row; `ref_row_of` reads the ref after the commit and its two spaces, and the long-ref case's fixture grew to 46 characters, because 32 now fits.
- `tests/test_the_gate_names_every_step_ci_runs.py` pinned `HISTORICAL_ROWS`, `CI also  1 more steps` in the drawing and `4 more steps` / `8 more steps` as values. Re-aimed to the new labels and the dim `·`.
- `tests/test_the_release_seal_is_drawn.py` held `release_seal.PANEL_VALUE_WIDTH == broad_gate.PANEL_VALUE_WIDTH == 23`. The release's rows are out of scope (`spec.md` §*Out*: `release_rows` unchanged), so the release keeps 23 and the case now holds the two apart; `release_seal.py`'s comment says so.
- `skills/verify/SKILL.md` said the panel *names the ref on the row under the commit* and that *a panel value is 23 columns*. Both now say what the panel does, pinned in `test_the_documents_say_where_the_panel_now_carries_each_name` and `test_the_documents_name_the_ci_also_row`.

**The old sheet did not draw the new rows whole at 36 columns.** `plan.md` says *the old sheet still draws the new rows, so this phase stands alone*. At `seal_stamp.PANEL_WIDTH = 36` the frame cut a value at 23, so `✓ 768 passed · 1 skipped` (24) and the joined `base` lost their tails, and `test_the_panel_value_width_is_what_the_stamp_actually_gives` went red. The phase set `PANEL_WIDTH = 54`, the frame that gives 41, and the claim held; phase 6 removed `PANEL_WIDTH` with the sheet.

**`wrapped` changed its rule after all.** `spec.md` says `wrapped(label, pieces)` is *unchanged in rule*. A row broken before a ` · ` piece keeps ` ·` at its end, which is two columns where a comma was one, so `wrapped` holds two back on every piece but the last and strips `·` from the next row's lead. A row reaching 40 before a ` · ` piece would otherwise have been 42 and cut by `fit`. A case pins it (`["a" * 36, " · b", " · c"]`).

**The ref is elided to the room its commit leaves.** `fit` takes a `width`, and `panel` hands the ref `PANEL_VALUE_WIDTH - len(commit) - 2`. Fitting the ref at 41 and then the joined value at 41 would have cut the joined value at its head and lost the ref's tail, the one part #666 keeps.

**The drawing's fixtures moved in phase 6, not here.** The hook module's `FULL_ROWS`, `ROWS` and `SMALL_ROWS` feed the sheet cases this phase did not touch; re-shaping them with the drawing kept phase 5's slice green on the old sheet.

**Each changed case was seen red** at the old panel before the change: 29 of the 34 cases selected failed, `bin/test` over the four modules with `-k` (the five that passed are unchanged parametrisations and the widest-panel case, whose change only tolerates `None`). Every changed unit was then broken once with `bin/mutation-check`, 20 breaks, every verdict `red`:

| Unit broken | Verdict |
|---|---|
| `fit` ignoring `width`; `wrapped` holding back one column; its lead strip without `·` (two places) | red |
| `rounds_rows`' `->` back; ` . capped` back; `item_value`'s ` . ` back | red |
| `base` joined by one space; the ref's room the whole width; the `None` row removed | red |
| the suite without `✓`; its pieces joined by `, `; the ledger without `✓`; drifted and broken swapped | red |
| `chain` reading the suite's exit; the `chain` row removed; `CI also` without `·`; `SEP` back to ` . ` | red |
| `PANEL_VALUE_WIDTH = 40`; `seal_stamp.PANEL_WIDTH = 53`; `SAMPLE_ROWS` without `chain` | red |

`bin/test` over the nine modules the plan and this phase name, after the change: 792 passed (4 failed on the first run, each a case of the new ones written wrong and corrected); the hygiene modules and `ruff` clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| ` . ` and `->` as the panel's separators; `panel`'s *Separators are ASCII* and *No row is `None` since #717* paragraphs | `SEP`, `ARROW` and `panel`'s *The values are the owner's characters* paragraph; the twin maps them (phase 6) |
| `panel`'s *A drawn panel says only what a `SEALED` stamp can say* paragraph | *The result rows carry a `✓`, and the blank before them is a row*, which says #717 took them off and decision 6 put them back |
| the `""` row carrying the base's ref under `base` | the `base` row, two spaces after the commit |
| `test_the_ledger_carries_its_ok_count_and_nothing_beneath` <!-- NAME NOT IN TREE --> | `test_the_ledger_carries_its_three_counts_on_one_row`; 0.17.0 cites the old name, which phase 9 corrects |
| the equality of the release's and the gate's value widths | `release_seal.py`'s comment over its own 23 |
