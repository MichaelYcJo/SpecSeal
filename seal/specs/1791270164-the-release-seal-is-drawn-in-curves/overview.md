# 1791270164-the-release-seal-is-drawn-in-curves — overview

The seal's emblem becomes one vector source that the terminal stamp and the release PNG both rasterise, so the release image stops being a staircase of terminal cells (#832).

## Where the run stopped (2026-10-06, after phase 1)

**Phase 1 is closed at `88070eac` and green**: the two phase-1 modules and the five that read `seal_stamp.py` beside them, 804 passed, `-p no:xdist`, no `-x`. `phases/phase-1.md` holds what it found, how each new case was seen red, and which constants and cases the owner's emblem and a smaller disc will touch. Phases 2, 3 and 4 have not started.

The red case was the emblem, not the narrower 0.90 disc: the interim ring changes colour less often than the lily, so every stamp is shorter and two of them fit where the lily's did not. A second case was red behind `-x`. Both now derive their rungs and their premise from the drawing's sizes, so neither moves again when the emblem lands (`phases/phase-1.md`).

## Where spec and implementation diverged

| Spec says | Code does | Grounds |
|---|---|---|
| `spec.md` S2: *the footprint each rung has today — (43, 44) at 1.0, (39, 40) at 0.90, (35, 36) at 0.80, (33, 34) at 0.75*. `plan.md` adds that `R0_CELLS = 15.5 / 0.74` *reproduces all four* | `R0_CELLS = 15.5 / 0.74` gives (43, 44), (39, 40), (35, 36), (33, 34). But today's `build(0.9)` gave **(40, 40)**, measured on the base before any edit. So the spec's figure for 0.90 was never today's | A width interval check shows no single constant gives 43, 40, 35 and 33 together. `int(2r)+2 = 40` needs `R0 ≥ 21.11`, and `= 43` needs `R0 < 21`. The plan's constant was kept, because it holds every height and the heights are the line counts the ladder and the budget cases are about. The 0.90 disc is one cell narrower. That was suspected of turning a hook case red and was measured not to: forced back to 40 × 40, the rungs did not move (`phases/phase-1.md`) |
| `spec.md` Data & interfaces: `build(scale)` *as today*, with a named radius constant | `build(scale=1.0, r0_cells=R0_CELLS)`. `margin`, which only the chart's reach used, is gone | The owner wants the disc smaller than today's, *like a real seal*. That was handed to this run as context, not as an answer. So the diameter is a keyword with the old value as its default, and no rung changes size. Shrinking the disc for real changes the budget measurements and the footprint pins, so it waits for the owner's choice |
| `spec.md` S4 and `plan.md`: *the budget cases A2–A4 green unchanged* | `test_several_files_come_out_as_one_message_oldest_first` and `test_two_files_in_one_turn_are_under_the_budget_together` are amended: the first derives its two rungs from the blocks' sizes, the second adds deferral homes to its second run until the pair does not fit at 0.75 | Both pinned sizes the lily gave, and a block's size is a property of the emblem, which the frame leaves open. Under the interim ring the pair of small stamps went from 0.80/0.75 to 0.90/0.90 and two real runs fit one message at 0.75 (8,976 of 9,000). Shrinking the disc to restore the old sizes is the owner's call, not this run's. Under the lily both cases reduce to what #717 wrote |
| `spec.md` Data & interfaces: a path is a tuple of `("L", …)` / `("C", …)` segments *from the previous point* | Each path starts with `("M", x, y)`, and `svg_path` returns a tuple of paths, one per `M` | A path needs a start point, and an SVG `d` with a hole has more than one subpath |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ Phase 1's two test modules all green after the edits | `bin/test` over both modules and five neighbours, `-p no:xdist`, no `-x`, at `88070eac`: 804 passed (2026-10-06) |
| ✅ Each new case shown red (§15) | one `mutation-check` per break, every verdict `red`, listed case by case in `phases/phase-1.md` |
| `seal-stamp`'s block form looked at by eye on a terminal. The `--shape` twin was printed and read at 0.75 and at 0.90; no segment has seen the colour form on a screen | the orchestrator, at phase 2's rendering on a dark and a light background |
| The production emblem. `EMBLEM_D` is an interim ring, and the pull request must not open with it (questions.md Q1 (c)) | the owner, through the orchestrator |

## Fed back into the spec

none — nothing was added to `spec.md` in this segment.

## Measured

- Q6: `build` plus sampling every cell takes 2–4 ms per disc at each rung with the interim ring at `n = 16` (`python3 -c` with `time.perf_counter`, 2026-10-06). Nothing needs lowering.
