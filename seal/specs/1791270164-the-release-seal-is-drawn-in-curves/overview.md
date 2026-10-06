# 1791270164-the-release-seal-is-drawn-in-curves — overview

The seal's emblem becomes one vector source that the terminal stamp and the release PNG both rasterise, so the release image stops being a staircase of terminal cells (#832).

## Where the run stopped (2026-10-06, smith on Opus 5.5)

**Phase 1 is in progress and NOT green. No phase is closed; `plan.md`'s Status column is empty on purpose.**

Committed in phase 1 so far:

- `seal_stamp.py`: `EMBLEM_D` (an INTERIM geometric ring, labelled so in its comment), `svg_path`, `flatten`, `inside`, `shade`, `EMBLEM`, `EMBLEM_POLYGONS`, `R0_CELLS`; `build(scale, r0_cells=R0_CELLS)` samples the source at cell centres; `ART` and `shrink` are removed; `SCALE_REFUSED` and `SCALE_TOO_LARGE` are reworded.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the lighting case now also checks every field cell against `shade` over `inside`; new cases pin the four footprints, the fixture emblem (even-odd, the viewBox mapping, `Q` raised to `C`, refusals of `m`, `A`, `H`), `shade` on the fixture, the area fidelity at every rung, and an import with Pillow blocked; the floor case pins both reworded refusals.

**The one known red case.** `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py::test_several_files_come_out_as_one_message_oldest_first` fails. It expects two small stamps at 0.80 and 0.75, and the hook now draws them at different rungs. The likely cause is the narrower 0.90 disc (see the divergence below), which leaves the ladder more room. That is unverified. The run used `-x`, so the cases after it in that module did not run.

**Next step, in order.**

1. Run `python3 -c` over `seal_stamp.admitted` with two `SMALL_ROWS` blocks to read which rungs it now picks. Then decide: amend the case's expected rungs (its docstring says the rungs are what fits, so new sizes legitimately move them), or choose a different `R0_CELLS`.
2. Re-run `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -p no:xdist -q` WITHOUT `-x`. The two modules took 5 min 50 s together.
3. Show each new case red (§15). Not done yet: delete the sentence each one pins, or break the unit through `mutation-check`, and record how.
4. Finish phase 1's document class (S8): the module docstring (it still says *fleur-de-lis* and *29x32 counted-stitch chart*), the comments over `SCALE_FLOOR` and `DEFAULT_SCALE`, the `KEY` comment, and the stale case names that still say *lily*. Then write `phases/phase-1.md` and put the closing commit in `plan.md`.
5. Phases 2, 3 and 4 have not started.

## Where spec and implementation diverged

| Spec says | Code does | Grounds |
|---|---|---|
| `spec.md` S2: *the footprint each rung has today — (43, 44) at 1.0, (39, 40) at 0.90, (35, 36) at 0.80, (33, 34) at 0.75*. `plan.md` adds that `R0_CELLS = 15.5 / 0.74` *reproduces all four* | `R0_CELLS = 15.5 / 0.74` gives (43, 44), (39, 40), (35, 36), (33, 34). But today's `build(0.9)` gave **(40, 40)**, measured on the base before any edit. So the spec's figure for 0.90 was never today's | A width interval check shows no single constant gives 43, 40, 35 and 33 together. `int(2r)+2 = 40` needs `R0 ≥ 21.11`, and `= 43` needs `R0 < 21`. The plan's constant was kept, because it holds every height and the heights are the line counts the ladder and the budget cases are about. The 0.90 disc is one cell narrower, which is the likely cause of the red case above |
| `spec.md` Data & interfaces: `build(scale)` *as today*, with a named radius constant | `build(scale=1.0, r0_cells=R0_CELLS)`. `margin`, which only the chart's reach used, is gone | The owner wants the disc smaller than today's, *like a real seal*. That was handed to this run as context, not as an answer. So the diameter is a keyword with the old value as its default, and no rung changes size. Shrinking the disc for real changes the budget measurements and the footprint pins, so it waits for the owner's choice |
| `spec.md` Data & interfaces: a path is a tuple of `("L", …)` / `("C", …)` segments *from the previous point* | Each path starts with `("M", x, y)`, and `svg_path` returns a tuple of paths, one per `M` | A path needs a start point, and an SVG `d` with a hole has more than one subpath |

## Not verified

| Item | Who must answer |
|---|---|
| Phase 1's two test modules all green after the edits. One case is red, and the cases after it in that module did not run | the next smith session |
| Each new case shown red (§15) | the next smith session |
| `seal-stamp` and its `--shape` twin looked at by eye on a terminal. Only the 0.75 twin was printed and read in this session | the next smith session |
| The production emblem. `EMBLEM_D` is an interim ring, and the pull request must not open with it (questions.md Q1 (c)) | the owner, through the orchestrator |

## Fed back into the spec

none — nothing was added to `spec.md` in this segment.

## Measured

- Q6: `build` plus sampling every cell takes 2–4 ms per disc at each rung with the interim ring at `n = 16` (`python3 -c` with `time.perf_counter`, 2026-10-06). Nothing needs lowering.
