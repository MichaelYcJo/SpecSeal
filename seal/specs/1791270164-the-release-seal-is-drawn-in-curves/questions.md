# 1791270164-the-release-seal-is-drawn-in-curves — questions for the planner

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**This run is `automation`** (`routing.md`), and the framer cannot ask
anybody. The owner's decision of 2026-10-07 settled every point of the
terminal seal and offered the release PNG, through the orchestrator, and
the reframe wrote it into `spec.md` decision 4. **One row is open with a
person and blocks a phase: Q8, the owner's look at the real 14-cell stamp
before the PNG phase — a stop the owner asked for.** Q2 and Q9 are a
person's and block nothing. Every other judgment the decision left open was
answered from the tree and is listed first, so nobody reopens it.

**What the owner's decision left open, and the tree answered.**

- **What `scale` does to the drawing.** Nothing, from now on: a hand-drawn
  chart has one size, so `build(scale)` draws 14 cells at every scale in
  the band. The band, `check_scale`, `--scale` and the files' `scale` field
  stay, because fifteen parametrised cases, `admitted`'s `min(scale, rung)`
  and every values file an older gate wrote read them, and a knob that
  draws the same thing stops nobody. Retiring it is a work item of its own
  (`plan.md` §Alternatives). The two refusal sentences stop giving a disc
  size as their reason.
- **Whether the ladder needs a second rung again.** No. A real-run stamp is
  about 2,900 units (`plan.md` §*Technical context*), so two and three share
  a message at 0.90; a lower rung would only draw a disc nobody drew a chart
  for. `SCALE_LADDER = (0.90,)` stays, and `admitted` lays several blocks as
  it always could.
- **A sheet shorter than the disc.** The owner's rule keeps the sheet's
  height, and a 6-line sheet (the four-row `SMALL_ROWS` fixture) cannot hold
  a 7-line disc. No gate writes one — a real run has twelve rows or more —
  so the sheet takes the lines the disc needs there and only there
  (`spec.md` S3), and a real run's sheet is exactly as tall as today.
- **What `GAP` means now.** The owner's rule is global — widen past the
  first clash-free width by three columns, the disc moving with the right
  edge — so `GAP = 3` with that meaning replaces *two clear cells on every
  line*; on the tightest line it is three cells.
- **What a cell of the disc's square outside the circle shows.** The
  sheet's own cell beneath it, as the mock drew it: parchment, or a
  character where one reaches under a corner. The sheet widens until no
  cell inside the circle stands on a character, and the corners are outside
  the circle.
- **The colours' names.** `MARK` (240, 130, 118) and `MARK_SHADOW`
  (96, 10, 14) replace `LILY_LIGHT` and `LILY_SHADOW`: the lily left two
  phases ago, the mark's triple changes, and the comment that kept the
  names said it kept them for readers that now go. Every comment says
  *the disc's mark*, for the one-word check.
- **Whether the twin keeps `nearest`.** No. Every cell is exactly one
  palette colour, so a letter is a lookup and `nearest`'s case could not
  fail.
- **Whether `Letter.disc` stays with no PNG reading it.** Yes: the layout
  case reads it (`spec.md` S3), and it is one tuple.
- **Where the SVG lives and what it carries.** `.github/scripts/release-seal.svg`,
  beside its one reader. Its three `<text>` layers become `<path>`s of
  Georgia Bold's § once, on the owner's machine, because the runner image
  has no Georgia (`plan.md` §*Technical context*) and a fallback serif is
  not the mark the owner looked at.
- **What rasterises it, and why.** `rsvg-convert` from `librsvg2-bin`,
  installed by an `apt-get` step of the `seal` job: one system package,
  draws gradients, gradient strokes and opacity in C, no Python package
  added anywhere. Pillow cannot read SVG; CairoSVG is a pip package over
  the cairo shared library with the same font problem.
- **Whether Pillow leaves.** No. `release_seal.py` stops importing it, but
  the suite reads the PNG's pixels with it and the pin case holds the
  install line; the pin stays untouched (`spec.md` Out).
- **The PNG's size on the page.** `SEAL_PX = 160` display, `DENSITY = 2`,
  so a 320-px PNG shown through `<img width="160">` — the earlier frame's
  2× rule kept, the display size the work's to adjust (Q11).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Which mark is the emblem, how is it drawn, how big is the disc, and where does it sit? | a person (the owner, through the orchestrator) | Answered 2026-10-06 (the § by area, 24 cells, the corner) and **superseded 2026-10-07** by decision 4 in `spec.md`: a hand-drawn 7 × 10 chart on a 14-cell computed disc, four flat colours, inside the sheet against its right edge | — | ✅ the owner, 2026-10-06, then 2026-10-07 after comparing renders in their own terminal; written into `spec.md` decision 4 and S1–S4 by the framer |
| Q2 | Are the 0.18.0–0.19.0 release images redrawn with the new seal? | a person (the owner) | **(a) From 0.20.0 on only.** Earlier notes keep their cell-for-cell PNGs. **(b) Redraw by hand**: a checkout at each tag, the suite run there for `SUITE_XML`, `DRY_RUN=1` on a machine with `rsvg-convert`, `gh release upload --clobber`, `gh release edit --notes-file`. Nothing in the tree does it unattended, and nothing in this work item changes for either answer | **(a)**. Different answers build the same code, so the build does not wait | ⬜ |
| Q3 | How many UTF-16 units is the hook's message at 0.90 with the 14-cell seal, over `full_values()`, `ROWS`, `SMALL_ROWS` and the widest panel, and how many real runs share one message? | a measurement | Re-opened by decision 4. The frame's probe over this tree's `colour_row` and the owner's layout rule: one real run about 2,901, two 5,804, three 8,707, four over `MESSAGE_BUDGET`; `SMALL_ROWS` about 1,490. Phase 3 measures the built drawing through `stamp` as phase 2 did and the fragment's correction of 0.17.0 L1 records it. If the built sizes differ by more than the label's length from the probe's, the phase record says why | the probe's figures; three real runs per message | ⬜ phase 3 measures; phase 2's 7,180 at `108f549c` is history |
| Q4 | Does GitHub's Markdown sanitiser keep `width` on an `<img>` in a release body? | a measurement | `gh api /markdown -f mode=gfm -f text='<img src="https://example.com/s.png" alt="a" width="160">'` returns the rendered HTML; the attribute is there or it is not. If it is dropped, the PNG is written at display size and `DENSITY` is 1 | Kept. GitHub documents `<img width>` in READMEs, and release bodies use the same renderer | ⬜ phase 5 |
| Q5 | The sheet edge's width in the PNG | the work | Moot: the PNG is the SVG and carries no sheet (Q9) | — | ✅ closed by decision 4, 2026-10-07 — nothing to decide |
| Q6 | How long does one terminal disc take to draw? | a measurement | Measured by phase 2 at `108f549c`: 0.036 s per disc for the § by area. The hand chart is 196 cells of arithmetic and takes no measuring | — | ✅ phase 2; moot after decision 4 |
| Q7 | How the PNG draws the rim's angular gradient | the work | Moot: librsvg draws the owner's SVG gradients; Pillow draws nothing | — | ✅ closed by decision 4, 2026-10-07 |
| Q8 | **Does the real 14-cell stamp read on the owner's terminal?** The owner asked to see the hook's real stamp — the message `fitted` prints for one `full_values()` block, written to a `.ans` file by phase 3 — before the PNG phase starts. The orchestrator copies the file to `~/Desktop/specseal-stamp-14.ans` and asks the owner to `! cat` it | a person (the owner, through the orchestrator) | **(a) Accepted**: phase 5 starts. **(b) Changed**: the chart, a colour or the layout is the owner's new value; the orchestrator writes it into `spec.md` §*Data & interfaces* and re-spawns phase 3 against it — a value, not a reframe | none; **this row blocks phase 5 by the owner's instruction** | ⬜ |
| Q9 | Is the release PNG the owner's SVG alone, with no sheet and no counts drawn in it? | a person (the owner) | **(a) The PNG is the SVG** — the owner's offer, which the session proposed on 2026-10-07 and nobody objected to: the 32 × 32 seal rasterised at 2×, the counts on the line under the image as today. **(b) The sheet with the counts drawn as an image, the SVG seal on it** — the earlier frame's phase 3, redrawn around the SVG; a second renderer for the sheet's text | **(a)**, recorded as the owner's offer. Does not block: (b) is a later work item, not a change to (a)'s code | ⬜ |
| Q10 | Does `sudo apt-get install -y --no-install-recommends librsvg2-bin` succeed on `ubuntu-latest`, and does `rsvg-convert` then draw the tree's SVG? | a measurement | The `seal` job runs only at a tag, so the first measurement is 0.20.0's: the job log shows the install and `drew <path>`, or one `::warning::` naming the call. If it fails, the by-hand `DRY_RUN=1` path draws the seal from a machine that has it, as `docs/release-checklist.md` §6 already says | succeeds: apt and `sudo` are on every `ubuntu-latest` image, and `librsvg2-bin` is in Ubuntu's main archive | ⬜ the first tag that runs the job |
| Q11 | The display size of the seal in the note, and the pins' tolerances on the real render | the work | Phase 5 renders at `SEAL_PX = 160`; if the seal reads too small or too large beside the counts line in `DRY_RUN`'s printed note, the phase changes the number, records a divergence row in `overview.md`, and the pins (alpha at the corners and centre, a pixel within 8 per channel of `#c42830`, darker lower right) are set from what the real render shows and seen red by one fill changed | 160 px | ⬜ |

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
because the owner has no pen in this file; Q8's will be the orchestrator's,
for the same reason.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
