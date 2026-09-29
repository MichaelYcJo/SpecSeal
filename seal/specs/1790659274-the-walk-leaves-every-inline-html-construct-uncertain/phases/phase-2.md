# 1790659274-the-walk-leaves-every-inline-html-construct-uncertain — phase 2

<!-- seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | dc1facb7 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md`'s phase 2, #667 round 3's 🟡 1: the walk calls a piece, and the
paragraph after it, uncertain inside any inline HTML. In `hooks/blocks.py`,
`INLINE_HTML`, `TAG_END` and `leaves_html_open`; `walk`'s sticky state;
`walk_text`'s check asking both predicates; the module docstring and
`walk_text`'s docstring. `hooks/config.py#hidden_lines`' docstring.
`templates/config.md` §*Broad gate*'s list of contexts read as before, pinned
(S10). Cases S3 (five openers × eight breaks), S4, S5; seven `FOUND`
documents; `ALPHABET` untouched. Each case red at `3fc0c5bd`, the new `FOUND`
documents red with the base walk and phase 1's oracle. Q2's count and Q3's
corpus measurement. Ledger: P2-1 and R1-1 corrected, rows for the new units.

## What this phase found

- **The frame's no-under-report argument did not hold for the draft, and the
  walk asks every opener instead.** The frame said an opener the parser does
  not honour "errs only toward uncertain" and that reading left to right,
  skipping what each construct holds, "is also what the parser does". The
  first is false once the second is applied: an opener in a code span, after
  a backslash, or a `<b` that never becomes a tag can find its end inside a
  real construct, and reading on from that end steps over the real opener.
  Executed (`<scratchpad>/1790659274/nest.py`): `x` + `` `<?` `` +
  ` <![CDATA[ a ?> b` + LS + a fence run and a config table + `]]>` gives
  `[("Mode", "shared")]` with the round 3 draft, at LS and FF, for all three
  kinds of unhonoured opener, while the oracle hides every piece.
  `leaves_html_open` now answers open where any opener has no end after it.
  That is a superset of the draft's answer, so it only adds uncertainty.
  The overview's first divergence row quotes both sides.
- **The same hole one level up, in `walk`'s pending state.** The draft asked
  only the text after a comment's `-->`. When the `<!--` that made the
  paragraph pending is one the parser never formed, a real opener before the
  `-->` on a later line is stepped over too (`x` + `` `<!--` `` + ` a`,
  `b <? c --> d`, `e ?> f`: the parser hides the third line, the draft claimed
  it). Now every pending line is asked for a non-comment opener, and one that
  has one is sticky. Overview, second row.
- **Nine `FOUND` documents, not seven.** The seven of the frame's case column
  and the two above. Measured per document (`<scratchpad>/1790659274/measure.py`):
  each of the nine disagrees with the oracle on a claimed line under the walk
  from `3fc0c5bd`, and six of them also leave both readings for the config
  reader. Under the draft the two nesting documents still disagree, and the
  first of them still leaves both readings. At HEAD none does either.
- **Q2: above the floor.** `test_the_walk_is_exact_somewhere` claims 24,019 of
  68,855 corpus lines, floor 22,951; `3fc0c5bd`'s walk would claim 24,044 of
  the same corpus, the draft 24,024. No document had to be dropped.
- **Q3: no committed file reads a different row, and the claimed-line half of
  S8 does not hold as the frame wrote it.** 577 tracked `.md` files, 4 with
  config rows, 0 reading differently through `config_rows` at `3fc0c5bd` and
  at HEAD. Claimed lines over those files: 72,440 at `3fc0c5bd`, 72,155 at
  HEAD, in 23 files, the largest `CHANGELOG.md` and a round 3 report
  (43 and 31), which quote openers in prose. The frame's figure of 24,009 of
  68,819 was the reviewer's count on the property corpus, not on the tracked
  files. The prompt budget for committed files is empty. Overview, fourth row.
- **Q4: formed.** Every shape the cases use forms an `html_inline` token at
  every break: the S1 whole-line rows and the S2 assertions pass against the
  widened oracle, and all 40 S3 shapes are hidden by it. The one gap was the
  oracle's mark for H7, closed in phase 1.
- **The template edit drifted seven release rows.** `templates/config.md#"## Broad gate"`
  is an anchor in `seal/releases/0.10.0.md` (S4), `0.12.0.md` (three rows),
  `0.15.3.md` (A2) and `0.15.4.md` (S1), and `#"# Repository config"` in
  `0.5.0.md` (S8). Each claim was re-read against the one sentence this phase
  changed, none rests on it, and each carries a dated re-read note and a new
  hash. `hooks/config.py#hidden_lines` drifted P3-1 of work item 1790645290
  the same way, docstring only.
- **The records pass.** The rename of phase 1 left `_comment_lines` and · NAME NOT IN TREE
  `_starts_in_a_comment` in three of work item 1790645290's records and in · NAME NOT IN TREE
  this work item's `spec.md`, `plan.md` and `phases/phase-1.md`, and this
  frame's `spec.md` and `questions.md` name two identifiers of
  markdown-it-py's source. Each such line carries ` · NAME NOT IN TREE`, 24
  lines in seven files, among them work item 1790645290's `rounds/round-3.md`
  and `round-3-report.md`, where the marker sits inside a table row's last
  cell. `bin/evidence-check .` exits 0:
  2,906 ok, 0 drifted, 0 broken, 0 refused.
- **Mutations, one unit at a time, each red** (`<scratchpad>/1790659274/m_walk.py`):
  each of `INLINE_HTML`'s five openers removed; `TAG_END` ignoring quotes
  (red only after a quoted `>` assertion was added to S4, commit `dc1facb7`);
  the closer never looked for; left to right with stepping over; `walk`'s
  entry ignoring other inline HTML; the entry never sticky (red only after the
  `-->` assertion was added to S5, same commit); a pending line never making
  it sticky; `-->` ending a sticky paragraph; `walk_text` asking the comment
  alone. Thirteen, all red.
- **Red at the base** (`<scratchpad>/1790659274/swap.py`): with
  `hooks/blocks.py` from `3fc0c5bd`, 49 failed: the 40 S3 cases, S4, the six
  S5 cases, half 2 and the config reader's half 1. With `templates/config.md`
  from `3fc0c5bd`, the S10 case failed. Then the property, config, routing
  and rider modules at HEAD: exit 0, 307 passed; the template cases, 2
  passed. S9 holds: the routing and rider modules pass unedited.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
