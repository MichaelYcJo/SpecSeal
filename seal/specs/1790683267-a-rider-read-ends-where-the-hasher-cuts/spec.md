# Feature Specification: a rider read ends where the hasher cuts

<!-- seal/specs/1790683267-a-rider-read-ends-where-the-hasher-cuts/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Milestone 49 (0.16.0), item K: #682. Round 3 of work item G
(`1790655302-every-reader-ends-a-line-where-gfm-does`, #664, PR #675) found
it, and G's run had already spent its reopening, so the finding came here
with its fix unapplied. G has landed in `release/v0.16.0` at `6321dbdc`,
where this branch was cut.

**The class.** The rider check has two readers of one file. The **hasher**,
`.github/scripts/rider_check.py#region_lines`, cuts every rider block out of
the anchored region before it hashes, and it finds those blocks with
`#comment_blocks` over GFM lines, which end at LF, CR and CRLF alone. The
**reader**, `#riders_in`, finds the riders whose stamps are compared, and it
reads `str.splitlines` pieces, which also end at U+2028, U+2029, NEL, a form
feed, VT and `\x1c`–`\x1e` (the eight characters). Round 2 of G made the
reader ask the hasher *whether* a marker piece is read. It did not make it ask
the hasher *where the block ends* or *what kind of comment it is*: from that
piece on, the reader runs the block over pieces by its own `-->` test and its
own comment-kind test. Where one of the eight sits inside a line the hasher
cuts, the two blocks part, the reader reads a stamp on a line the hasher does
not cut, the stamp is hashed into the region it names, and `--reverify`
rewrites it on every run without the rider ever reading ok.

The class is **a reader that decides a rider's extent by a rule the hasher
does not share**. It closes by construction rather than by a third patch to
the reader's rule: the reader takes its blocks from the hasher, so **every
piece of every rider the reader reads lies on a GFM line inside a block that
`comment_blocks` over GFM lines returns, which is exactly what `region_lines`
cuts**. That sentence is this item's acceptance. The two shapes below are its
instances, not its definition.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #682's body and its one comment (the ticket) | The two shapes, the invariant, the reviewer's fix, and the constraint the fix as pasted does not meet (the comment) |
| `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/rounds/round-3-report.md` §*🟡 1*, §*⬜ 2*, §*Paste-ready fixes* | The finding, the reviewer's measurements (labelled below as theirs), the fix this frame builds from, and the case it starts from. It is a closed record and is not edited |
| `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md`, row G13 | Its clause "so every rider the reader reads is one `region_lines` cuts" is false for the two shapes until this item lands. The row is re-read here against the fix (plan.md, ledger) |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` and `#test_no_shipped_script_needs_more_than_the_floor_without_saying_so` | `rider_check.py` is run with whatever `python3` is on PATH, so it carries no `zip(` with `strict=` on its line, in code or in a comment. `ruff.toml` selects `B`, so a bare `zip` is refused by B905. `rider_check.py#write_block` at `7ffa520c` is the accepted shape: an index comprehension over `range(len(…))` |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | §12: the class above is enumerated over the eight characters, both comment kinds and both directions of disagreement, not over the two shapes. §14: the verdict a person sees changes for the two shapes, so it is pinned (S5). §15: every new case is seen red at `6321dbdc`, or against a named mutant where the case is about agreement that already held |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Red test, failure direction, prompt budget and platform honesty (§*Failure direction and prompt budget* below). The rider check is a gate: `tests/test_a_rider_reaches_its_file.py` runs it over the tree in CI |
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here asks a person anything. The prompt budget is zero |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | New rows go to `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md`. Rows elsewhere whose anchored unit this item edits, or whose claim it makes false, are re-read or corrected where they stand (plan.md §*Ledger*) |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | Fixtures use neutral paths and the stamp shape the existing cases use. Each of the eight characters is built from its code point, never typed |
| `skills/implement/SKILL.md` §6, "The records themselves stay" | G's records, its spec and its changelog fragment are not rewritten. This item's fragment says what changes |

## What was measured before the frame, and by whom

Taken in this framer at `dd9026eb`. Nothing of the repository's ran here: the
rows labelled *read* are this framer's reading, and the rows labelled *the
reviewer's* were executed by G's round 3 warden at `c7fef45f` and are carried
as nobody's finding at this base until the build re-runs them.

| # | Fact | Label |
|---|---|---|
| M1 | `.github/scripts/rider_check.py` at `6321dbdc` is byte-identical to the file at `7ffa520c`, and `7ffa520c` differs from `c7fef45f` in `#write_block` alone. So the reviewer's measurements at `c7fef45f` are of the reader this branch starts from | executed (`git diff`, `git show --stat`) |
| M2 | The markdown shape: a closed HTML comment, one of the eight, then the rider's opener, with the stamp on the next line. At `c7fef45f` `check` reads 1 drifted, and after each of two `--reverify` runs it reads 1 drifted again. At `7c339169` the rider was not read at all | the reviewer's, for U+2028 only |
| M3 | The `.py` shape: `# note`, one of the eight, then an HTML opener carrying the marker. The reader takes the piece for an HTML block, leaves the comment state open, and reads the next line, `b = 2  # …` with a marker, as a second rider the hasher never cuts | the reviewer's, for U+2028 only |
| M4 | A fuzz over 13,237 generated texts found a read rider with a piece off the hasher's cut in 0 texts at `7c339169` and 4 at `c7fef45f`, all four one of the two shapes. The fix below brings it to 0 and changes no rider in a text without the eight characters | the reviewer's. The fuzz is not in the tree and is not reproduced by count (S6 says what is run instead) |
| M5 | The 576-prefix differential: six whitespace prefixes, the eight characters and six whitespace suffixes before a marker, in `.yml` and `.md`. At `c7fef45f` and with the fix, 0 riders are read and not cut, and 0 differ from `7c339169` | the reviewer's. It is agreement that already held, so it is a guard rather than a defect (S4) |
| M6 | Every one of the eight characters is whitespace to `str.lstrip`, so the hasher cuts a GFM line whose text before the marker is whitespace and those characters alone | executed (a Python one-liner over the eight code points) |
| M7 | No file in the tree has either shape. The 25 files under the rider roots that carry the marker gave the same riders at `7c339169` and with the fix, and `rider_check.py --root .` printed `19 ok · 0 drifted · 0 broken` | the reviewer's, at `c7fef45f`. S7 re-runs it at this base |
| M8 | After the fix, `#comment_blocks`' TEXT path (its `text` parameter, the `gfm_places` step-over and round 2's `cut` set) has no caller in shipped code, and no test passes `comment_blocks` a text. Every test call passes one or two positional arguments | read (`grep` over `tests/` and `.github/scripts/`), and the reviewer's |
| M9 | After the fix, the second element of each `#gfm_places` pair, whether only whitespace stands before a piece, has no reader: `#inferred_anchor` and the tests read `[0]` alone, and the step-over that read it is removed with the TEXT path | read |
| M10 | Rows whose anchored unit this item edits: `#comment_blocks@9d5e074b` in G13, P5-1 (`seal/ledger/1790645290-…md`) and S3 (`seal/releases/0.9.1.md`); `#gfm_places@49809c43` and `#inferred_anchor@073c5225` in G13. Rows whose claim this item makes false with no anchor to drift: R1-1 (`seal/ledger/1790645290-…md`), which lists `#comment_blocks` and `#riders_in` among the callers that hand the walk the text. S2 (`seal/releases/0.9.1.md`) anchors `#region_lines`, which is not edited, and its last note describes the reader's step-over | read (`grep` of every `rider_check.py#…@` anchor in `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md`, and of R1-1's text) |
| M11 | `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS` names `riders_in` with one `.splitlines(` call and `gfm_places` with one. The fix keeps both counts | read |

## Scope

**In.**

- `#riders_in` takes its blocks from the hasher: `comment_blocks` over GFM
  lines. It gathers the `str.splitlines` pieces that start inside each block
  and splits them at every piece carrying the marker. A piece before the
  block's first marker piece (`# note`, a closed comment) belongs to no rider.
  Riders are still numbered on `str.splitlines` pieces, so `Rider`,
  `#write_block`, `#reverify` and `#migrate` read them as before.
- `#comment_blocks` loses its TEXT path, because the fix leaves it with no
  caller and it is the second rule the class is about (plan.md
  §*Alternatives*). `#gfm_places` returns the GFM line number alone, because
  its second value's only reader goes with that path. `#inferred_anchor` and
  the one case that index the pair follow.
- Every docstring in the units above states what its code does after the
  change.
- The class case and the verdict case below, in
  `tests/test_every_reader_ends_a_line_where_gfm_does.py` after round 2's
  cases.
- The ledger: new rows in this item's fragment, and G13, P5-1, S3, S2 and
  R1-1 re-read or corrected where they stand.
- This item's changelog fragment, with the intent given below.

**Out, each with its reason.**

- **The `-->` test's own reach.** A block ends at a line holding `-->`
  anywhere, so a closed comment before the rider's opener on one line ends
  the rider there. With the fix, the markdown shape reads BROKEN "no
  verification stamp", and the same text with a space in place of the break
  reads the same BROKEN at every version (the reviewer's). The break no longer
  changes the verdict, which is this class. The `-->` rule is older than #664
  and is not about line ends. Whether it is worth an issue is the
  orchestrator's call.
- **`#quoted_lines`' TEXT parameter.** After the fix no shipped caller passes
  it one, but it is `quoted_lines`' own contract, which
  `tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_rider_check_never_leaves_both_readings`
  drives against the CommonMark oracle and R1-1 cites. Removing it reopens
  work item F's oracle case, which is not this class. The unit is not edited.
- **`#region_lines`.** It is the hasher, and it is the side the reader now
  agrees with. It is not edited.
- **G's changelog fragment.** Its rider bullets describe the shapes G fixed,
  and they stay true. This item's fragment names the two shapes G's fix
  opened. One fragment per work item.
- **The fuzz's 13,237 texts.** They are not in the tree, and an aggregate is
  not a coordinate. S6 names the corpus that is run and records its size.

## User scenarios & acceptance *(mandatory)*

The case names are suggestions. The builder may rename them, and the ledger
names what was planted.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The markdown shape is read inside the cut | Given a `.md` text `x`, then a line holding a closed HTML comment, one of the eight, and the rider's opener with the marker, then the stamp and `-->` on the next line, when `riders_in` reads it, then every piece of every rider read is on a GFM line that `comment_blocks(gfm_lines(text), rel)` returns inside a block | the class case, one parameter per character. Red at `6321dbdc` for each of the eight |
| S2 | The `.py` shape is read inside the cut | Given a `.py` text `a = 1`, then `# note`, one of the eight and an HTML opener with the marker, then `b = 2  # ` with a marker and a stamp, when `riders_in` reads it, then the same holds, and the `b = 2` line is no rider | the class case, the same parameters. Red at `6321dbdc` for each of the eight |
| S3 | Every marker piece the hasher cuts is still read | Given any text in S1, S2, S4 or round 2's three shapes, then every piece carrying the marker that starts inside a block the hasher returns starts exactly one rider read, so two riders on one GFM line stay two | the class case's second assertion. `test_a_rider_the_hasher_cuts_is_read` stays green unedited except for S10's index |
| S4 | Whitespace around a break changes nothing (the 576-prefix differential) | Given `a: 1`, then a line of `{prefix}{char}{suffix}` and a rider with its stamp, then `b: 2`, in `.yml` and `.md` (the markdown form closing its comment), over six whitespace prefixes including the empty one, the eight characters and six whitespace suffixes, then the reader reads exactly one rider on the second line, and S1's and S3's properties hold on all 576 texts | inside the class case, per character. Green at `6321dbdc` (M5), so it is seen red against a mutant: `riders_in` starting riders only at a piece that begins its GFM line, which drops every rider behind a leading break. The phase record names the mutant and its count |
| S5 | A break inside a cut line changes no verdict | Given S1's and S2's texts under a rider root in a temporary tree, each stamp naming an anchor that resolves in its file (a heading in the markdown file, a unit in the Python one, as the reviewer's probe did), and each text again with a space in place of the character, when `check()` reads each, then the two give the same `ok` and `drifted` counts and the same severity and sentence for each problem, the location aside. The markdown shape does not read drifted, before or after `--reverify` | the verdict case, one parameter per character and shape. Red at `6321dbdc`: the markdown shape reads drifted where its space twin reads BROKEN, and the `.py` shape carries a second problem its twin does not. This pins what a person sees (§14) |
| S6 | Nothing moves for a text without the eight characters | Given a corpus holding none of the eight, when `riders_in` reads each text at `6321dbdc` and after, then every rider's `(start, end, body)` is the same | executed probe (`test_tmp_*`, deleted): the tree's rider files, the existing cases' texts, and a generated corpus of the builder's making over both comment kinds, back-to-back riders, fences, and markers in prose and strings. Its size is recorded in the phase record. By construction, without the eight a piece is a GFM line and a block holds one marker line, so the split adds nothing |
| S7 | The tree's own riders are unchanged | Given this tree, when `rider_check.py --root .` runs at `6321dbdc` and after, then it prints the same summary line and exits the same way, and every file under the rider roots yields the same riders | executed |
| S8 | The rider cases already in the tree hold | The rider cases of `tests/test_every_reader_ends_a_line_where_gfm_does.py`, `tests/test_a_rider_reaches_its_file.py` and `tests/test_the_hooks_hide_what_a_renderer_hides.py` pass, with S10's index edit the only change to an existing case | executed, those three modules |
| S9 | The fix runs on the interpreter a user has | `rider_check.py` carries no `zip(` with `strict=` on its line, in code or in a comment, no bare `zip`, and no `itertools.pairwise` (3.10, the same class, which the floor case's pattern does not see) | executed: `test_no_shipped_script_needs_more_than_the_floor_without_saying_so`, and `ruff check` with `ruff format --check` on the files this item touches |
| S10 | One rule, stated where it runs | `comment_blocks` takes no `text`; `gfm_places` returns a list of GFM line numbers; `inferred_anchor` and the round 2 case index it without `[0]`; no docstring in `rider_check.py` says `riders_in` passes a text or that `comment_blocks` steps over a mid-line piece | read, and S8 green. `grep` for `text=` and `, text)` at `comment_blocks`' call sites finds none |
| S11 | The ledger is true | G13, P5-1, S3, S2 and R1-1 carry a dated note against this item's change, a `Corrected` one where the change made a claim false. The new rows resolve | executed: `evidence_check.py .` exits 0, and each re-stamped anchor is re-read against the edit |

## Data & interfaces

- `riders_in(rel, text)` keeps its signature and its result type. Each
  `Rider` is still numbered on `str.splitlines` pieces, so `start` and `end`
  mean what they meant.
- `comment_blocks(lines, rel=None)` drops `text=None`. Its lines are GFM
  lines, or `str.splitlines` lines of a text holding none of the eight, which
  are the same lines.
- `gfm_places(gfm_lines, text)` returns `[number]`, the 1-based GFM line
  each `str.splitlines` piece starts in, where it returned
  `[(number, head)]`.
- No output format changes. A verdict changes only for a rider whose line,
  as GFM ends it, holds one of the eight inside a block the hasher cuts. No
  tracked file has one (M7).

## Failure direction and prompt budget

| Shape | At `6321dbdc` | After | Direction |
|---|---|---|---|
| markdown, closed comment then a break then the rider (S1) | 1 drifted, and every `--reverify` leaves it drifted | BROKEN "no verification stamp", which the same text with a space reads at every version | the same count of alarms, now one an edit can clear. A drifted alarm that `--reverify` cannot settle becomes the verdict the hasher's cut supports |
| `.py`, `# note` then a break then an HTML opener (S2) | the HTML piece is read as a rider, and the `b = 2` line after it is read as a second rider with a stamp that is hashed | the HTML piece alone, as the hasher cuts its line; `b = 2` is code and no rider | one alarm fewer. The dropped one was on a line the hasher never cuts, so no edit could have cleared it |
| any text without the eight characters (S6, S7) | — | unchanged | none |

The rider check blocks through `tests/test_a_rider_reaches_its_file.py` in
CI. Neither shape is in the tree, so nothing changes for this repository.

The prompt budget is zero. Nothing here puts a question in front of a person.

**Platform.** The change is string handling over text already read. CR is
translated on the read in `all_riders` on every platform, and `write_block`'s
`newline=""` is not touched. Only macOS runs this item's cases here. Linux and
Windows are CI's legs.

## What the changelog fragment says

The builder writes `seal/specs/1790683267-a-rider-read-ends-where-the-hasher-cuts/changelog.md`.
Its intent, under `### Fixed`, one bullet ending `(#682)`:

- the rider check reads a rider only on the lines its hash leaves out;
- before, a rider behind a closed HTML comment and a U+2028, form feed or
  one of the six others on its line, or behind `# note` and one of them in a
  Python file, was read past the line the hash cut, so its own stamp was
  hashed and `--reverify` never made it read ok;
- such a rider now reads what it reads with a space in place of the
  character, which for the markdown shape is "no verification stamp", since
  the comment closed on that line ends the rider there.

It names no function, as G's fragment does not.

## Open questions → questions.md

No row needs a person. The judgments the tree answered are listed at the head
of that file. Three rows are left open: one for a measurement and two for the
work.

Framed 2026-09-29 by framer, before the build.
