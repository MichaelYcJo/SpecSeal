# 1791270164-the-release-seal-is-drawn-in-curves — questions for the planner

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**This run is `automation`** (`routing.md`), and the framer cannot ask
anybody. The one row that was a person's — the emblem — was answered by the
owner on 2026-10-06, after phase 1 closed, and the answer was relayed by the
orchestrator and written into `spec.md`; no row is open with a person now.
Every other judgment the tickets and the answer left open was answered from
the tree and is listed first, so nobody reopens it.

**What the tickets, the update and the answer left open, and the tree
answered.**

- **Curves, not an SDF.** Both were allowed. Pillow fills polygons in C and
  cannot fill a distance function; a per-pixel Python loop over the PNG at
  4× supersample and 2× density is on the order of 20 million samples. The
  same flattened polygons answer the terminal's samples in pure Python
  (`plan.md` §Alternatives).
- **Where the source lives.** In `seal_stamp.py`, where the chart was *the
  only copy*; four loaders already reach that file by path
  (`broad_gate.py#STAMP`, `hooks/sealer-stamp.py`, `bin/seal-stamp`,
  `release_seal.py#stamp()`).
- **What `scale` now means, and what the ladder does.** `DEFAULT_SCALE`
  stays 0.90, and 0.90 is the rung that draws the owner's 24 cells: a values
  file an older gate wrote carries `0.9`, and `admitted` never draws above a
  file's own scale, so re-basing the owner's size to 1.0 would draw every
  pending file at 21.6 cells. The diameter is `round(DISC_CELLS · scale / <!-- NAME NOT IN TREE -->
  DEFAULT_SCALE)`. The ladder keeps one rung with a disc — the owner
  accepted nothing below 24 cells, having seen 20 fragment the mark — and
  then the sheet alone, which it already ended in. The band (0.75–1.0) stays
  for `--scale` by hand, where a size below 24 is a person's own choice.
- **The colours.** The owner's four #717 triples keep their values and
  names; the rim's two ends join the palette and the face colour leaves,
  because the owner's rendering draws the mark in one light colour with a
  shadow and no face. The sheet's four 256-colour codes are unchanged.
- **How the emblem arrives.** As an SVG path `d` string — absolute
  `M L C Q Z` in a 1000 × 1000 viewBox, centre (500, 500), the field's edge
  at radius 500 — parsed by `svg_path`. The owner's § is written in
  `spec.md` verbatim, so the build copies and never re-derives it.
- **The grid fit is part of the drawing, in both forms.** The offset
  (0, +0.375) cell and the scale 1.04 were searched on the terminal's grid,
  and the PNG applies the same so the two forms agree at a cell's centre
  (S6); a 5-pixel shift in the PNG is invisible, a disagreement is not.
- **The disc's edge against the sheet.** Blended by area where the sheet is
  under a cell (`under` is the sheet colour beneath), hard where the disc
  hangs off it, as the owner's reference drew it. `compose` knows which is
  which; `build` is told per cell rather than computing two grids.
- **The twin's letters for a blended cell.** The nearest palette colour's
  letter in linear light, with the parchment in the comparison so a cell
  that is mostly sheet stays the sheet's character; the rim's two ends take
  `M` and `n`. A per-cell class carried beside the colours would widen
  every reader of a cell for the twin alone.
- **The shadow in the PNG.** Painter's order — the shadow's polygons first,
  the mark's over them — gives exactly *shifted and not mark*, which is the
  rule; no mask offsets. The counter is cut by XORing the two contours'
  masks, because Pillow's polygon fill is not even-odd.
- **Whether the PNG keeps a transparent margin.** Yes. The disc hangs off
  the sheet's corner, so the image is transparent where neither is, as
  0.19.0's is today. (The earlier frame answered *no* for a disc inside the
  sheet; that placement is withdrawn.)
- **Whether the blended colours are quantised to keep the message short.**
  No. One real-run stamp at 0.90 measures about 7,300–7,600 of the 9,000
  units (`plan.md` §Technical context), and quantising changes what the
  owner looked at.
- **`<img>` instead of `![]()`.** A Markdown image cannot carry a display
  width, and the ticket asks for a 2× PNG shown at its display size.
- **Whether `paint`'s cell-for-cell pin is kept beside the new drawing.**
  No. It pins the staircase the ticket removes; the new pins are S5 and S6.
- **Pillow's version and where it is pinned.** Unchanged (`run_tests.py#PILLOW`,
  12.3.0); the install-line case and the top-up stay as they are.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | **Which mark is the emblem, how is it drawn, how big is the disc, and where does it sit?** The lily is withdrawn; the frame needs the mark as closed curves in the frame S1 names, an SVG path `d` string within radius 475, and the owner's reading of it at terminal resolution | a person (the owner, through the orchestrator) | Answered 2026-10-06, chosen from renderings the orchestrator drew and the owner looked at in their own terminal, in four parts. **(1) The mark is §**, Georgia Bold's outline at 820 units in the 1000-unit frame, centred on (500, 500), farthest point at radius about 417; the `d` string is in `spec.md` §*Data & interfaces* verbatim. The owner first chose §, saw the centre-sampled three-colour rendering break it into fragments, and chose the rendering below to fix that. **(2) The rendering**: each cell the area average of a 6 × 6 grid of samples, in linear light; the mark in `LILY_LIGHT` with a `LILY_SHADOW` where the point 0.7 cell up-left is inside the mark and the point is not, replacing the three colours; a cell wholly in the field tightened through a smoothstep of (coverage − 0.15) / 0.7; the mark offset by (0, +0.375) cell and scaled by 1.04, the fit that maximised how many field cells read clearly mark or clearly field at 24 cells; the rim — 1.15 cells inside the field's edge — lit continuously by angle from the upper left, `RIM_DARK` (104, 12, 16) to `RIM_LIGHT` (214, 70, 66) through a smoothstep of (1 + cos(θ − 225°)) / 2; the disc's edge area-averaged against the parchment where the sheet is under it, hard where it hangs off. **(3) The size**: 24 cells across at the wax edge at the default rung; the owner saw 20 fragment the §, asked whether a smaller disc would be sharper, saw it is worse (fewer cells per stroke), and chose 24. **(4) The placement**: over the sheet's lower right corner, half on and half off, the #717 shape, chosen over the disc inside the sheet; the release PNG follows it | — | ✅ the owner's answer, relayed by the orchestrator, 2026-10-06; written into `spec.md` decision 3, S1–S6 and *Data & interfaces* by the framer <!-- NAME NOT IN TREE --> |
| Q2 | Are the 0.18.0–0.19.0 release images redrawn with the new renderer? | a person (the owner) | **(a) From 0.20.0 on only.** Earlier notes keep their cell-for-cell PNGs. **(b) Redraw by hand**: a checkout at each tag, the suite run there for `SUITE_XML`, `DRY_RUN=1`, `gh release upload --clobber`, `gh release edit --notes-file`. Nothing in the tree does it unattended, and nothing in this work item has to change for either answer | **(a)**. Different answers build the same code, so the build does not wait | ⬜ |
| Q3 | How many UTF-16 units is the hook's message at 0.90 with the owner's rendering, over `full_values()` and over the widest panel the cases build, and does one real run still fit with its disc? | a measurement | The A3 cases print it; the widest-panel case says whether the first rung still holds it. Re-opened by the answer: the frame's probe over the owner's reference put one real-run stamp at about 7,300–7,600 (the disc 5,337 hard-edged to 6,610 blended, a 13-line sheet 1,270), so one fits and two do not; phase 2 measures the built sampler, and the ledger fragment records it. If a real run does not fit, the ladder's one step draws it as the sheet alone, which is the state the owner must then see; the budget constants do not move | fits, by the probe; the fragment records what phase 2 measured | ⬜ |
| Q4 | Does GitHub's Markdown sanitiser keep `width` on an `<img>` in a release body? | a measurement | `gh api /markdown -f mode=gfm -f text='<img src="https://example.com/s.png" alt="a" width="400">'` returns the rendered HTML; the attribute is there or it is not. If it is dropped, the PNG is written at display size instead and `DENSITY` is 1, with the pixel case unchanged | Kept. GitHub documents `<img width>` in READMEs, and release bodies use the same renderer | ⬜ |
| Q5 | The sheet edge's width in the PNG | the work | Phase 3 draws the edge as a band half a cell wide (7 display px); if the rendering reads wrong, the phase changes it, records a divergence row in `overview.md`, and the layout stays one rule in `compose`. The other half this row used to hold — whether the disc is centred or bottom-aligned — is closed by Q1's part 4: the disc is on the corner | half a cell | ⬜ |
| Q6 | How long does one terminal disc take to draw with the § by area? | a measurement | Re-opened by the answer: the owner's reference (36 point tests per cell through `inside` over 32 chords per cubic) took 0.95 s per disc on the framer's machine, over the 0.5 s bar. Phase 2 measures the built sampler at `flatten`'s 16 chords with each cell's points classified once; under 0.5 s, nothing; over, the scanline fill in `plan.md` constraint 3, held to the point rule by `test_a_cell_is_the_mean_of_its_samples_in_linear_light` | about half the reference's time, by the chord count; measured in phase 2 <!-- NAME NOT IN TREE --> | ⬜ |
| Q7 | How the PNG draws the rim's angular gradient | the work | Pillow has no angular gradient. **(a)** 360 one-degree `ImageDraw.arc` strokes at the ring's width, each in its angle's mix — Pillow draws them in C and the supersample hides the steps; **(b)** a per-pixel loop over the ring's pixels at the supersampled size, about a quarter of a million, in Python. Either satisfies S5's two rim pixels; (a) is cheaper and is the default | (a) | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked. Q1's tick is
the owner's answer as the orchestrator relayed it, written by the framer
because the owner has no pen in this file.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
