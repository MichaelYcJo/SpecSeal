# 1791270164-the-release-seal-is-drawn-in-curves — overview

The seal's emblem becomes one vector source that the terminal stamp and the release PNG both rasterise, so the release image stops being a staircase of terminal cells (#832).

## Where the run stopped (2026-10-06, after phase 2)

**Phase 2 is closed at `108f549c` and green**: the two phase-2 modules and the seven hygiene modules beside them, 915 passed, `-p no:xdist`. The terminal draws the owner's § by area on a 24-cell disc, and the hook's ladder is one rung. `phases/phase-2.md` holds the measurements (Q3, Q6), the three places the frame did not hold, how each case was seen red, and the ledger anchors phase 4 must correct. Phases 3 and 4 have not started.

Phase 1 closed at `88070eac` (`phases/phase-1.md`). Its two divergence rows about the 0.90 footprint and `r0_cells` describe a constant phase 2 removed: the disc's size is `DISC_CELLS` now, and phase 4 brings those rows up to date as `plan.md` says.

## Where spec and implementation diverged

| Spec says | Code does | Grounds |
|---|---|---|
| `spec.md` S2: *the footprint each rung has today — (43, 44) at 1.0, (39, 40) at 0.90, (35, 36) at 0.80, (33, 34) at 0.75*. `plan.md` adds that `R0_CELLS = 15.5 / 0.74` *reproduces all four* | `R0_CELLS = 15.5 / 0.74` gives (43, 44), (39, 40), (35, 36), (33, 34). But today's `build(0.9)` gave **(40, 40)**, measured on the base before any edit. So the spec's figure for 0.90 was never today's | A width interval check shows no single constant gives 43, 40, 35 and 33 together. `int(2r)+2 = 40` needs `R0 ≥ 21.11`, and `= 43` needs `R0 < 21`. The plan's constant was kept, because it holds every height and the heights are the line counts the ladder and the budget cases are about. The 0.90 disc is one cell narrower. That was suspected of turning a hook case red and was measured not to: forced back to 40 × 40, the rungs did not move (`phases/phase-1.md`) |
| `spec.md` Data & interfaces: `build(scale)` *as today*, with a named radius constant | `build(scale=1.0, r0_cells=R0_CELLS)`. `margin`, which only the chart's reach used, is gone | The owner wants the disc smaller than today's, *like a real seal*. That was handed to this run as context, not as an answer. So the diameter is a keyword with the old value as its default, and no rung changes size. Shrinking the disc for real changes the budget measurements and the footprint pins, so it waits for the owner's choice |
| `spec.md` S4 and `plan.md`: *the budget cases A2–A4 green unchanged* | `test_several_files_come_out_as_one_message_oldest_first` and `test_two_files_in_one_turn_are_under_the_budget_together` are amended: the first derives its two rungs from the blocks' sizes, the second adds deferral homes to its second run until the pair does not fit at 0.75 | Both pinned sizes the lily gave, and a block's size is a property of the emblem, which the frame leaves open. Under the interim ring the pair of small stamps went from 0.80/0.75 to 0.90/0.90 and two real runs fit one message at 0.75 (8,976 of 9,000). Shrinking the disc to restore the old sizes is the owner's call, not this run's. Under the lily both cases reduce to what #717 wrote |
| `spec.md` S4: `test_several_files_come_out_as_one_message_oldest_first` *derive[s] [its] premise as phase 1 left [it]* | Renamed `test_several_files_come_out_one_stop_each_oldest_first`; it asserts the pair is over the budget and pins one stamp per `Stop`, oldest first, the broken file left pending | Under the § no two stamps share a message at the real budget: the four-line pair is 12,128 units at 0.90 and 9,784 at 0.75. The premise cannot be derived because it is false (`phases/phase-2.md`) |
| `spec.md` S2a: *the centroid of the cells' shadow weight lies below and to the right of the centroid of their mark weight* | The lighting case pairs each cell's shadow weight with the mark weight one cell up-left and one cell down-right, and asserts the first is over four times the second | Measured on the §, the shadow's centroid is right of the mark's and 1.0 to 1.9 cells above it, because the shadow falls into the upper counter. The pairing is the rule cell by cell; the centroid is a property of the shape |
| `spec.md` S2b: *the field's cells nearer `LILY_LIGHT` than `FIELD`* over the enclosed area | Counted over cells whose centre is inside the rim | The rim's light end is nearer the mark than the field, and counted with it the ratio was 1.28; inside the rim it is 0.94–1.01 |
| `spec.md` Data & interfaces: a path is a tuple of `("L", …)` / `("C", …)` segments *from the previous point* | Each path starts with `("M", x, y)`, and `svg_path` returns a tuple of paths, one per `M` | A path needs a start point, and an SVG `d` with a hole has more than one subpath |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ Phase 1's two test modules all green after the edits | `bin/test` over both modules and five neighbours, `-p no:xdist`, no `-x`, at `88070eac`: 804 passed (2026-10-06) |
| ✅ Each new case shown red (§15) | one `mutation-check` per break, every verdict `red`, listed case by case in `phases/phase-1.md` |
| `seal-stamp`'s block form looked at by eye on a terminal. Phase 2 looked at its half-cells drawn as a picture on a dark and a light ground, and the twin at 0.90 and 0.75; no segment has seen a terminal render the block form. A real-run stamp at 0.90 is in the orchestrating session's scratchpad as `stamp-0.90.ans` | the owner, through the orchestrator |
| ✅ The production emblem. `EMBLEM_D` is an interim ring, and the pull request must not open with it (questions.md Q1 (c)) | the owner answered Q1 with the § on 2026-10-06; `EMBLEM_D` holds it verbatim at `bcba578b`, pinned by `test_the_emblem_is_the_owners_section_sign_inside_the_field` |

## Fed back into the spec

none — nothing was added to `spec.md` in this segment.

## Measured

- Q6, phase 1: `build` plus sampling every cell took 2–4 ms per disc at each rung with the interim ring at `n = 16` (`python3 -c` with `time.perf_counter`, 2026-10-06).
- Q6, phase 2: the § by area, `build` alone, medians of five: 0.045 s at 1.0, 0.036 s at 0.90, 0.029 s at 0.80, 0.027 s at 0.75; a real-run stamp at 0.90, 0.044 s. Per-point `inside` would have been about 1.6 s per disc.
- Q3, phase 2: UTF-16 units at 0.90 with the label — a real run 7,180, the cases' `ROWS` 6,903, `SMALL_ROWS` 6,063, the widest panel 7,885 — all under 9,000; two never share a message (`phases/phase-2.md`).
