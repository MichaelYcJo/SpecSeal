# 1791270164-the-release-seal-is-drawn-in-curves — questions for the planner

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**This run is `automation`** (`routing.md`), and the framer cannot ask
anybody. One row is a person's and open — the emblem — and the orchestrator
supplies its answer; the frame is built so the mechanism does not wait on it.
Every other judgment the tickets left open was answered from the tree and is
listed first, so nobody reopens it.

**What the tickets and the update left open, and the tree answered.**

- **Curves, not an SDF.** Both were allowed. Pillow fills polygons in C and
  cannot fill a distance function; a per-pixel Python loop over the PNG at
  4× supersample and 2× density is on the order of 20 million samples. The
  same flattened polygons answer the terminal's ~1,500 centre samples in
  pure Python (`plan.md` §Alternatives).
- **Where the source lives.** In `seal_stamp.py`, where the chart was *the
  only copy*; four loaders already reach that file by path
  (`broad_gate.py#STAMP`, `hooks/sealer-stamp.py`, `bin/seal-stamp`,
  `release_seal.py#stamp()`).
- **What `scale` now means.** The disc's radius in cells, `R0_CELLS · scale`,
  with the four footprints `build` gives today kept exactly (43/44, 39/40,
  35/36, 33/34), so `SCALE_LADDER`, `admitted` and every budget case keep
  their meaning. The band's refusal sentences lose their *stitch* reason and
  are reworded; the band itself stays (a scale above 1.0 would enlarge the
  disc past what the budget cases measured).
- **The colours.** Unchanged: the owner's five #717 triples for the disc and
  the four 256-colour codes for the sheet. The mark is pressed into the wax
  in one colour, lit from the upper left, as the lily was — the rule is
  continuous now (`shade`), with `delta` one cell.
- **How the emblem arrives.** As an SVG path `d` string — absolute
  `M L C Q Z` in a 1000 × 1000 viewBox, centre (500, 500), the field's edge at
  radius 500 — parsed by `svg_path`. That is the format every vector editor
  exports and the one a case can refuse with the command named.
- **Where the disc sits inside the sheet.** Right of the text with `GAP`
  (2) clear cells on every line, vertically centred, one blank parchment
  line above and below the taller of text and disc. The owner said *inside,
  like a real seal pressed on paper* and no more; this is the least layout
  that satisfies it, and it is the work's to adjust if the rendering says so
  (Q5).
- **Whether the PNG keeps a transparent margin.** No. With the disc inside
  the sheet the image is the sheet, and nothing hangs past it to be
  transparent around.
- **`<img>` instead of `![]()`.** A Markdown image cannot carry a display
  width, and the ticket asks for a 2× PNG shown at its display size.
- **Whether `paint`'s cell-for-cell pin is kept beside the new drawing.**
  No. It pins the staircase the ticket removes; the new pins are S5 and S6.
- **Pillow's version and where it is pinned.** Unchanged (`run_tests.py#PILLOW`,
  12.3.0); the install-line case and the top-up stay as they are.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | **Which mark is the emblem?** The lily is withdrawn; the owner is choosing a mark that means SpecSeal from candidate renderings. What the frame needs is the mark as closed curves in the frame S1 names: an SVG path `d` string, absolute `M L C Q Z`, 1000 × 1000 viewBox, centre (500, 500), the field's edge at radius 500, the mark within radius 475 (0.95), filled even-odd, and **no stroke thinner than about 50 viewBox units** (≈ 1.5 cells at 0.75 — a thinner stroke is lost at a cell centre and the area-fidelity case is red). The orchestrator supplies the answer; the smith writes it into `EMBLEM` through `svg_path` in whichever phase it arrives | a person (the owner, through the orchestrator) | **(a) The answer arrives before phase 1 closes** — it goes in there and is seen in every rendering the smith looks at. **(b) It arrives during phases 2–3** — it goes in when it arrives; the interim ring is what phase 1–2 renderings show. **(c) It has not arrived by phase 4** — phase 4 cannot close; the smith hands back with `EMBLEM` openly labelled interim, and the pull request is not opened with an interim mark in a release stamp | None. The interim constant is a plain geometric ring, labelled interim in its comment, and it is **not** an answer | ⬜ |
| Q2 | Are the 0.18.0–0.19.0 release images redrawn with the new renderer? | a person (the owner) | **(a) From 0.20.0 on only.** Earlier notes keep their cell-for-cell PNGs. **(b) Redraw by hand**: a checkout at each tag, the suite run there for `SUITE_XML`, `DRY_RUN=1`, `gh release upload --clobber`, `gh release edit --notes-file`. Nothing in the tree does it unattended, and nothing in this work item has to change for either answer | **(a)**. Different answers build the same code, so the build does not wait | ⬜ |
| Q3 | How many UTF-16 units is the hook's message at 0.90, 0.80 and 0.75 with the disc inside the sheet, over `full_values()` and over the widest panel the cases build? | a measurement | The A3 cases print it; the oversized case says whether the sheet-alone rung still applies. If 0.90 passes `MESSAGE_BUDGET` for a real run's values, `admitted` steps the first block down and the cases say so; the budget constants do not move | 0.17.0's L1 figures (6,277 and 7,249) are assumed to grow by a few hundred units and stay under 9,000; the ledger fragment records what phase 2 measured | ⬜ |
| Q4 | Does GitHub's Markdown sanitiser keep `width` on an `<img>` in a release body? | a measurement | `gh api /markdown -f mode=gfm -f text='<img src="https://example.com/s.png" alt="a" width="400">'` returns the rendered HTML; the attribute is there or it is not. If it is dropped, the PNG is written at display size instead and `DENSITY` is 1, with the pixel case unchanged | Kept. GitHub documents `<img width>` in READMEs, and release bodies use the same renderer | ⬜ |
| Q5 | The sheet edge's width in the PNG, and whether the disc is vertically centred or bottom-aligned once the two are seen together | the work | Phase 3 draws the edge as a band half a cell wide (7 display px) and centres the disc; if the rendering reads wrong, the phase changes it, records a divergence row in `overview.md`, and the layout stays one rule in `compose` | half a cell; centred | ⬜ |
| Q6 | How long does one terminal disc take to sample at `n = 16` chords per cubic with the production emblem? | a measurement | `python3 -c` timing `build(0.90)` over its `w × h` cells, three probes per cell. Under 0.5 s: nothing. Over: lower `n` for the terminal sampler or cache the polygons per scale — the result is unchanged either way | under half a second for an emblem of a few dozen segments | ⬜ |

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
column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
