# 1791270164-the-release-seal-is-drawn-in-curves — questions for the planner

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**This run is `automation`** (`routing.md`), and the framer cannot ask
anybody. The owner's final seal decisions of 2026-10-07 (`spec.md`
decisions 5 and 6) settled every point of the disc's frame and of the
stamp's layout, named the mark a placeholder whose design is #857,
archived the candidates, moved the gallery, retired the parchment sheet,
and said **nobody is to be asked again**. No row blocks a phase. Q2, Q9,
Q12 and Q15 are a person's and block nothing; Q9 is a default the session
proposed and the owner has not answered, and Q15 is a judgment the tree
made from the owner's own stated reason. Every other judgment the
decisions left open was answered from the tree and is listed first, so
nobody reopens it.

**What the owner's decisions left open, and the tree answered.**

- **Where the rows change.** In `broad_gate.panel` and nowhere else: the
  values file is `panel`'s rows, read by whichever hook draws it, so a
  drawing that joined or re-spelled rows would claim rows nothing wrote.
  `seal_stamp` formats what it is given. An older file draws its old rows
  in the new layout and nothing converts it.
- **Which rows return.** `chain ✓ exit <code>`, the ledger's drifted and
  broken counts and the suite's ✓ — all taken off at #717 as saying what
  `SEALED` says, all in the owner's design of 2026-10-07; the newer owner
  choice wins, and `panel`'s docstring says both happened.
- **The `CI also` row's label.** Kept (Q15): the real panel has no
  `workflow` row to rename; `CI also` is seven columns, the owner's own
  wording from #717, and pinned in two instructing documents. It gains the
  dim `·` the design puts on a row that is not a pass.
- **The separators on a non-UTF-8 console.** `panel` writes the owner's
  `·`, `✓`, `─` and `→`; the twin, which exists for that console, maps
  them to `.`, `+`, `-` and `>` where it writes them — one character for
  one, so the footprint holds — and every twin line is ASCII (`spec.md`
  S4). The values stay data; only the twin rewrites.
- **The value width without a frame.** `PANEL_VALUE_WIDTH = 41`, because
  `28 + 3 + 8 + 41 = 80`: the widest value that keeps the stamp's widest
  line inside an 80-column terminal, which is the floor a CLI's output is
  held to. `fit` and `wrapped` stay for a value past it.
- **The blank line between the groups.** A `None` row from `panel`, drawn
  blank by `text_lines`; the drawing does not know which label starts the
  result rows.
- **The title rule's length.** As wide as the widest row line, and at
  least the mock's thirty, so a short panel keeps the reference's look.
- **Where the chart lives.** A text file beside the module,
  `skills/verify/scripts/seal-mark.txt`, read at import by `read_chart`
  with its encoding named — because the decision says changing the mark is
  changing *that chart alone*, and a candidate's chart in the gallery is
  the same `.M` text, so #857's chart becomes the mark by replacing one
  file. A malformed file is refused with a sentence (`spec.md` S1).
- **What a case may pin about the mark.** Nothing of the S's shape. Cases
  pin the frame — the ring counts no chart moves, the lighting rule, the
  layout — and derive the mark's cells from `CHART` as data, so #857 goes
  red only at the owner's-picture case, which is the one re-transcribed on
  purpose (`plan.md` constraint 7).
- **A text block shorter than the disc.** Each is centred on the taller
  one's height (decision 6); `SMALL_ROWS` (four rows, six text lines) draws
  14 lines with the text starting on the disc's fifth, and a real run's 15
  or so text lines set the height themselves. The sheet rules of decisions
  4 and 5 are history.
- **What `GAP` means now.** The clear columns between the disc's last
  column and the text block's first, three; nothing can clash because
  nothing is drawn under the disc or over the text.
- **The twin's letters for nine colours.** The framer's choice, capitals
  lit and lower case shadow, #30's `m`/`.` and #717's `Y`/`y` kept where
  the role survives (`spec.md` §*Data & interfaces*): the twin is for a
  console that cannot draw half-blocks, and nobody has looked at it.
- **The colours' names.** `seal28.py`'s, since the owner's decision names
  that file as the rule: `WAX_EDGE`, `RIM_LIT`, `RIM_MID`, `RIM_DARK`,
  `FIELD`, `FACE`, `LIGHT`, `INNER`, `DROP`. `WAX_M` leaves by name; it had
  named #30's middle wax band since the first disc. Every comment says
  *the disc's mark*, for the one-word check.
- **How the hook encodes the stamp.** The lean writer of `spec.md` S11,
  after `frames.py#encode`: one SGR per change with every part in it, no
  reset inside a line, the terminal's own colours as `39`/`49` and styles
  as `1`/`2`/`32`, no 256-colour code anywhere. The reference is 5,119
  characters; the orchestrating session's 10,361 was the mock's
  reset-everything encoding on the old sheet and never the hook's.
- **Whether the ladder needs a rung.** No. One real run fits with about
  3,800 units to spare, two (10,240) do not fit under any encoding, and a
  smaller chart is the scaling #857's own lesson refuses. `SCALE_LADDER =
  (0.90,)` stays.
- **The letter's layout.** Decision 6 settled it, and this plan builds it
  (phases 5 and 6): the rows in `panel`, the lines in `text_lines`, the
  placement in `compose`.
- **Whether `docs/seals/README.md` stays in `tests/test_docs_line_wrap.py#COVERED`.**
  No. The list is opt-in and only `README_PAIR` constrains it (read
  2026-10-07); nothing else requires the entry, and keeping it at the new
  path would make `assets/` a place the docs checks read, which the move
  exists to avoid.
- **How the candidates' `.ans` files are archived.** As the sheet alone,
  their caption or label line dropped, like the gallery's two lily files;
  the README says the 28-cell ones were drawn by the reference renderer
  over a sample panel and cannot be redrawn from a tag.
- **What `scale` does to the drawing.** Nothing, as phase 3 left it; the
  band, `check_scale`, `--scale` and the files' `scale` field stay.
  Retiring them is a work item of its own (`plan.md` §Alternatives).
- **Whether `Letter.disc` stays.** Yes: the layout case reads it.
- **Where the SVG lives, what rasterises it, whether Pillow leaves, the
  PNG's size on the page.** As the earlier reframe answered: beside its one
  reader, `rsvg-convert` from `librsvg2-bin`, Pillow stays for the suite,
  `SEAL_PX = 160` at `DENSITY = 2`; all kept from the held phase-5 work.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Which mark is the emblem, how is it drawn, how big is the disc, and where does it sit? | a person (the owner, through the orchestrator) | Answered 2026-10-06 (the § by area, 24 cells, the corner), superseded 2026-10-07 by decision 4 (a hand-drawn § on 14 cells), and **superseded again the same day by decision 5** in `spec.md`: a 28-cell frame of nine colours, a placeholder S as one chart, right of the text and centred | — | ✅ the owner, 2026-10-06, 2026-10-07 twice; written into `spec.md` decisions 3–5 and S1–S4 by the framer |
| Q2 | Are the 0.18.0–0.19.0 release images redrawn with the new seal? | a person (the owner) | **(a) From 0.20.0 on only.** Earlier notes keep their cell-for-cell PNGs. **(b) Redraw by hand**: a checkout at each tag, the suite run there for `SUITE_XML`, `DRY_RUN=1` on a machine with `rsvg-convert`, `gh release upload --clobber`, `gh release edit --notes-file`. Nothing in the tree does it unattended, and nothing in this work item changes for either answer | **(a)**. Different answers build the same code, so the build does not wait | ⬜ |
| Q3 | How many UTF-16 units is the hook's message at 0.90 with the 28-cell seal in the open layout, over `full_values()`, `ROWS`, `SAMPLE_ROWS`, `SMALL_ROWS` and the widest panel, and how many real runs share one message? | a measurement | Re-opened by decisions 5 and 6. The owner's reference `~/Desktop/specseal-frame-3-open.ans` is **5,119** units for rows of a real run's length at 77 columns (`read`), so one real run per message with about 3,800 to spare, as in the lily's day, two (10,240) over the budget. The frame's probe over the parchment layout of decision 5 (5,699) is history. Phase 6 measures the built drawing through `stamp` and the real `fitted` message for one `full_values()` block, and the fragment's `Corrected · L1`, `B1` and `B2` rows record it; `test_the_hooks_message_is_under_the_budget_for_one_file` pins one real-size stamp under the budget through the real hook. If the built size differs from the reference by more than the label's length and the real rows' difference, the phase record says why | the reference's figure; one real run per message | ⬜ phase 6 (the 14-cell figures of 35277597 — one run 3,055, two per message — are history) |
| Q4 | Does GitHub's Markdown sanitiser keep `width` on an `<img>` in a release body? | a measurement | `gh api /markdown -f mode=gfm` returns the rendered HTML; the attribute is there or it is not | Kept | ✅ kept, measured 2026-10-07 by smith (phase 5's first act, before the hold): `gh api /markdown -f mode=gfm` over the line alone, and over the whole sealed glance block with its heading and counts line, returned `<img … alt="…" width="160" data-canonical-src="https://example.com/s.png" style="max-width: 100%;">` both times, the source rewritten through GitHub's image proxy. Measured on the API's renderer, not on a published release page. Kept by decision 5 |
| Q5 | The sheet edge's width in the PNG | the work | Moot: the PNG is the SVG and carries no sheet (Q9) | — | ✅ closed by decision 4, 2026-10-07 — nothing to decide |
| Q6 | How long does one terminal disc take to draw? | a measurement | Measured by phase 2 at `108f549c`: 0.036 s per disc for the § by area. A chart on a computed frame is 784 cells of arithmetic and takes no measuring | — | ✅ phase 2; moot after decision 4 |
| Q7 | How the PNG draws the rim's angular gradient | the work | Moot: librsvg draws the owner's SVG gradients; Pillow draws nothing | — | ✅ closed by decision 4, 2026-10-07 |
| Q8 | Does the real 14-cell stamp read on the owner's terminal? | a person (the owner, through the orchestrator) | **(a) Accepted**: phase 5 starts. **(b) Changed**: the owner's new value, folded into `spec.md` | none; blocked the PNG phase by the owner's instruction | ✅ (a) Accepted, 2026-10-07, carried by the orchestrator. The owner printed `~/Desktop/specseal-stamp-14.ans` in their terminal and raised only the mark's colour. They compared it with the red lily's three tones, with and without the drop shadow, at the same chart and place, and kept (240,130,118) with its shadow: the lily's tones lose the § into the field at 14 cells ("확 깨지네"). **Superseded later the same day by decisions 5 and 6**: the owner then looked at marks from 14 to 32 cells and settled the 28-cell frame, the lily's tones on it, and a placeholder S, and then chose a layout with no parchment sheet at all; the 14-cell light-red § is archived as a candidate with a note that it stood on the sheet |
| Q9 | Is the release PNG the owner's SVG alone, with its mark following the terminal's? | a person (the owner) | **(a) The PNG is the SVG with the placeholder S as paths** — the owner's SVG as the held phase-5 work converted it, its § layers replaced by Georgia Bold's S at the same anchors, fills and opacities, rasterised at 2×, the counts on the line under the image as today. This is **a default the session proposed on 2026-10-07; the owner has not answered it.** **(b) The sheet with the counts drawn as an image, the SVG seal on it** — a second renderer for the sheet's text. **(c) Keep the § in the PNG while the terminal shows the S** — two marks for one seal | **(a)**, recorded as the session's proposal. Does not block: (b) is a later work item, not a change to (a)'s code, and (c) is one glyph swap in one file | ⬜ |
| Q10 | Does `sudo apt-get install -y --no-install-recommends librsvg2-bin` succeed on `ubuntu-latest`, and does `rsvg-convert` then draw the tree's SVG? | a measurement | The `seal` job runs only at a tag, so the first measurement is 0.20.0's: the job log shows the install and `drew <path>`, or one `::warning::` naming the call. If it fails, the by-hand `DRY_RUN=1` path draws the seal from a machine that has it, as `docs/release-checklist.md` §6 already says | succeeds: apt and `sudo` are on every `ubuntu-latest` image, and `librsvg2-bin` is in Ubuntu's main archive | ⬜ the first tag that runs the job |
| Q11 | The display size of the seal in the note, and the pins' tolerances on the real render | the work | Phase 8 renders at `SEAL_PX = 160`; if the seal reads too small or too large beside the counts line in `DRY_RUN`'s printed note, the phase changes the number, records a divergence row in `overview.md`, and the pins (alpha at the corners and centre, a pixel within 8 per channel of `#c42830`, darker lower right) are set from what the real render shows and seen red by one fill changed | 160 px | ⬜ |
| Q12 | What is the seal's mark? | a person (the owner) | **#857 (0.21.0).** The owner supplies a reference image, a named motif, or a rough fill on the 28 × 28 grid; a chart is drawn from it, replaces `skills/verify/scripts/seal-mark.txt`, and the release SVG's three layers follow. Two candidates are archived at 28 cells (the § and the key) and one at 14 (the light-red §), in `assets/seals/candidates/` | the placeholder S, by the owner's decision 5. **Does not block this work item**: the frame, the loader and every case are the same for any chart | ⬜ #857 |
| Q13 | Does anything in the tree enumerate the files the plugin ships under `skills/verify/scripts/` — a manifest, a packaging list, a case over the directory — that `seal-mark.txt` has to join? | the work | The frame found none by name on 2026-10-07 but did not grep for a listing; phase 6 greps (`seal_stamp.py` as a literal in `.claude-plugin/`, `tests/`, `hooks/`) and adds the file where a list names its siblings, recording a divergence row if so | nothing enumerates them | ⬜ phase 6 |
| Q14 | How many units is the widest panel the tree can produce with the 28-cell disc in the open layout, and does `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` stay green unchanged at `PANEL_VALUE_WIDTH = 41`? | a measurement | The reference is 5,119 for 14 lines; the widest panel has about six more text lines at up to 80 columns, so about 5,600–5,900 by arithmetic, under the budget by about 3,000. Phase 6 measures it through `stamp` as it measures the others, and reads the widest line's column count against 80 (constraint 10) | about 5,800; the case stays green; the widest line is 80 columns or fewer | ⬜ phase 6 |
| Q15 | Is the `CI also` row renamed `flow`, as the owner's mock labelled the fixture's `workflow` row? | a person (the owner) | **(a) Keep `CI also`** — seven columns already, the owner's wording from #717, named in `skills/verify/SKILL.md` and `agents/sealer.md`; it gains the dim `·`. **(b) Rename to `flow`** — one word in `panel`, two documents and `test_the_documents_name_the_ci_also_row` move. The real panel has no `workflow` row; the mock's `flow` renamed a fixture row the panel stopped carrying at #717, and the reason the owner gave for the rename (the label has to fit seven columns) is met by (a) | **(a)**, decided from the tree. Does not block: (b) is the same code with one label changed, and the owner can say the word at any time | ⬜ |

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
column is ticked by whoever answered, never by whoever asked. Q1's and Q8's
ticks are the owner's answers as the orchestrator relayed them, written by
the framer and the orchestrator because the owner has no pen in this file.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
