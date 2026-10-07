# 1791270164-the-release-seal-is-drawn-in-curves — phase 8

| Field | Value |
|---|---|
| Phase | 8 |
| Commit | 2753ce1d |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md`'s phase 8 row: the held patch applied from `p5-held/phase5-tracked.patch` (`rasterise`, `SVG`, `SEAL_PX`, `DENSITY`, `sealed_glance`'s `<img width>` with escaping, the retired Pillow units, the cases of S6, S7 and S9); `.github/scripts/release-seal.svg` from `p5-held/release-seal.svg` with its three § paths replaced by Georgia Bold's S at the same anchors, fills and opacities, taken with `uvx --from fonttools` and compared against a `<text>S</text>` version through `rsvg-convert` before committing; the `seal` job's `librsvg2-bin` step, `continue-on-error`, before the suite; `docs/branch-and-release.md`'s bullet and `run_tests.py`'s sentence amended; the docstrings saying the S.

The spawn added: the thirteen release-seal cases red since phase 6 green; every new case shown red, then green; `bin/mutation-check` on each new unit.

## What this phase found

**The S's paths draw what the font draws.** `p8/glyph.py`, the held conversion with the S for the §, wrote three outlines from `/System/Library/Fonts/Supplemental/Georgia Bold.ttf` (glyph `S`, 2,048 units to the em, advance 1,329) at font-size 20, each anchored at the middle of its advance and its baseline. Drawn by `rsvg-convert` 2.58.4 at 320 × 320, the path version against the owner's SVG with `S` in its three `<text>` layers differs in 1,399 pixels by at most 8 in a channel, none by more; the same SVG set in Helvetica differs in 6,707 pixels by more than 8 and in 5,043 by more than 32. The held § compared the same way at one pixel by 9. The PNG `DRY_RUN=1` drew for `v0.19.0` was looked at once: the S in three red layers on the owner's wax, round and clear outside.

**The held patch's stand-in for `rsvg-convert` answered every command.** The patch was written at `200fedf1` and applied cleanly here, but nine cases failed with `'-o' is not in list`: `monkeypatch.setattr(mod.subprocess, "run", …)` replaces `subprocess.run` for the whole process, and the round-record readers ask `git rev-parse --git-common-dir` where the `seal/` root is. A `test_tmp_` probe, run once and deleted, listed the calls. `rsvg_convert` in the test module now hands every command but `rsvg-convert` to the real `subprocess.run`, and its docstring says why.

**The install step refreshes apt's lists first.** The plan's line is `sudo apt-get install -y --no-install-recommends librsvg2-bin`; the step runs `sudo apt-get update && ` before it, because a runner image's lists can name a version the mirror has since dropped, and that failure would cost the image at the first tag. The case reads the plan's command inside the step's line, so it holds either way. Whether the install works on `ubuntu-latest` is still Q10, measured at the first tag.

**Three more places said Pillow draws the seal.** Beside the runner's docstring and its `PILLOW` comment, which the plan named, `CONTRIBUTING.md` §*Running the checks*, `.github/workflows/test.yml`'s comment and `tests/test_release_hygiene.py`'s reason for the `12.3.0` pin said so; each now says Pillow decodes it. `docs/release-checklist.md` §6 named the reasons the `seal` job gives and the by-hand route; it now names `rsvg-convert` in both, pinned by `test_the_checklist_box_says_where_a_missing_seal_is_explained`, which was red against the box as #718 left it. `release_seal.py`'s comment over `LABELS` and the rows case's docstring named `seal_stamp.letter`, which phase 6 deleted; both now name the column a dry run prints.

**The new cases were red against the code before the phase.** With `release_seal.py`, `publish_release_note.py`, the workflow and `docs/branch-and-release.md` stashed and the SVG moved aside, the two release modules ran 18 failed: the SVG case, the rasteriser case, the pixel case, the three `rsvg-convert` failure parameters, the release-tail bullet, `sealed_glance`, the six-step count and the install step among them. Restored, the release slice is 120 passed with the pixel case run, not skipped.

**Every new unit was broken once with `bin/mutation-check`, and every break was red:**

| Unit broken | Verdict |
|---|---|
| `rasterise` without its SVG check; its density dropped from the size; a missing binary caught as another error; its exit code not read | red |
| `SVG` naming another file; `seal_release` not calling `rasterise`; the note given `SEAL_PX * DENSITY` as the width | red |
| `sealed_glance`'s alt unescaped; its URL unescaped | red |
| the SVG's face fill `#c42830` as `#d42830`; its highlight layer moved by 0.1 | red |
| the workflow without the install; the install without `continue-on-error` | red |
| `docs/branch-and-release.md`'s old sentence put back | red |
| the test helper without its pass-through | red |

The face fill was caught by the SVG case alone: the pixel case's tolerance of 8 found a pixel near `#c42830` where the layers blend, so a shift of 16 in one channel does not turn it red by itself.

**What was run.** `bin/test tests/test_the_release_seal_is_drawn.py tests/test_a_release_publishes_its_note.py tests/test_the_gate_names_every_step_ci_runs.py` with the line-wrap, release-hygiene, one-word, line-reader, interpreter, encoding and runner modules beside them, `-p no:xdist`: 654 passed. `ruff check` and `ruff format --check` over the changed Python, clean. `DRY_RUN=1 SEAL_PNG=… TAG=v0.19.0` drew the PNG and then refused, as it should, because 0.19.0's note no longer holds its glance table.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `release_seal.stamp`, `CELL_W`, `CELL_H`, `FONT_SIZE`, `CUBE_LEVELS`, `rgb`, `size`, `paint`, `FACES`, `font`, `png` | `SVG`, `SEAL_PX`, `DENSITY`, `rasterise`; the fragment's `Corrected · R1` and `Corrected · R2` |
| `test_rgb_is_xterms_table_and_a_triple_passes_through`, `test_paint_lays_every_cell_in_the_colours_block_gives_it`, `test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted`, `test_the_seal_module_imports_without_pillow`, `expected`, `painted`, `XTERM`, `broken_compose` | `test_the_release_seal_svg_is_the_owners_with_its_text_as_paths`, `test_the_rasteriser_runs_rsvg_convert_at_two_times_the_display_size`, `test_rsvg_convert_draws_the_seal_transparent_round_and_in_its_colours`, `rsvg_convert` <!-- NAME NOT IN TREE --> |
| the `failure` cases *Pillow does not import*, *compose raises*, *compose exits*, *the PNG writer exits* | *rsvg-convert is not installed*, *rsvg-convert fails*, *the SVG is not there* |
| `sealed_glance`'s Markdown image | an `<img>` with `width` |
