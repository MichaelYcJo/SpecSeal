# 1790645290 — review round 3, the report

Round 3 is a verifying round and the run's last: round 2 closed on a fix, the
one reopening, so this record ends the run whatever it finds. It had two
targets at HEAD `8b1492aa`, read in a `git clone --no-local` under
`<scratchpad>/1790645290/round-3/`:

1. Round 2's fix diff `67746d05..d814848d`: whether 🟡 1 and 🟡 2 are closed,
   with the new units (the uncertainty in `walk_text`, the sentinel re-parse in
   `hidden_text`, the new cases) as a finding surface.
2. The merge of `release/v0.16.0` (`9de34fad`) and its adjustment
   (`8b1492aa`): whether any reading, pin or ledger row is wrong after it.

## How the findings relate

```
round 2, 🟡 1: a piece that starts inside an inline comment its own line opened
   |  fixed for the comment, and only for the comment
   v
🟡 1  the same piece inside CDATA, a processing instruction or a tag's
      attribute value is still claimed live; with a fence run earlier on the
      line the config reader reads a Mode row its base and a renderer both hide
   |  and it was not caught because
   v
🟡 2  the oracle asks only about html_inline tokens that are comments, so on
      the rest of the class it agrees with the walk by construction again

the merge: #668's GFM lines meet #667's walk in rider_check.py
   |  the adjustment is right: region_lines walks GFM lines as given
   v
🟡 3  but riders_in still opens a rider at a marker after a break GFM does
      not honour, and region_lines never cuts it, so that rider's own stamp is
      in the region it hashes. Arrived with #668, not with this branch
⬜ 4  the re-pinned rider case dropped the half that asked the hasher this
      case's own question
⬜ 5  a ledger row re-read at the merge says every block is removed; 🟡 3 is
      the rider it is not true of
```

Both of round 2's closed verdicts hold for the shape they named. The merge's
code, test and ledger resolutions hold too. What is open is the class round
2's fix did not enumerate (§12), and one disagreement the merge carried in
from #668.

## Round 2's 🟡 1 is closed for the comment, and the rest of inline HTML still breaks it

Round 2 reported that a piece starting inside an inline comment its own line
opened took the line's "shown". The fix at `hooks/blocks.py:370` calls such a
piece uncertain, using `leaves_open`, which looks for `&lt;!--` alone. The
instance is closed. Executed: the new config case fails for all eight breaks
with `hooks/blocks.py` from `67746d05` and passes at HEAD, and my probe gives
`config_rows` of `[]` on the comment shape for every break.

A comment is one of five kinds of inline raw HTML (CommonMark 6.6), and CDATA,
a processing instruction and an open tag's attribute value hide what they
hold in the same way. The walk models none of them. Executed on
`x <![CDATA[ a` + break + a fence run + a config table + `]]>`, and on the
same shape with `<? a` … `?>` and `<span title="a` … `">`, all eight breaks:

- `config_rows` returns `[("Mode", "shared")]`;
- the base reading (`fence_only` over the reader's lines) hides the Mode line;
- an independent per-piece reading (markdown-it asked whether any
  `html_inline` token holds a sentinel put where the piece starts) hides it;
- `walk_text` calls it live and certain.

That is round 2's 🟡 1 exactly, a third reading that neither the base nor a
renderer gives, reached through a different opener. The declaration form
(`<!DOCTYPE`) did not reproduce, because my probe's closing `>` stood at a
line start and opened a block quote. I did not try it further.

The fix belongs where the question is asked, not in another special case
beside the comment. A second predicate reads the other four kinds of inline
HTML, each to its own closer, left to right. `walk_text`'s piece check and
`walk`'s paragraph-pending state both ask it. Where the opener is not a
comment, the paragraph stays pending until a blank line or a block start,
because the walk does not look for that opener's end on later lines. The
paste-ready fix is below. Executed in the clone:

- the four touched modules pass, exit 0, 278 passed;
- the same tests with the HEAD walk fail 26: the 24 new config cases, half 1
  for the config reader and half 2;
- on the repository's own corpus the walk still claims 24,009 of 68,819 lines,
  the same count as HEAD, so nothing it claimed before is given up.

**The new shapes go in `FOUND`, not in `ALPHABET`.** Six alphabet lines pushed
`test_the_walk_is_exact_somewhere` under its third (22,166 of 69,084), which is
the same wall round 2 met. Three lines without their closers never form inline
HTML to the parser, so they tested nothing: 61 passed with the HEAD walk.

## And the oracle cannot see it, because it asks about comments alone

Round 2's 🟡 2 is closed as reported. The oracle now asks the parser where a
piece starts, so a piece just past a closing comment and a piece inside one
are told apart. Executed: the two new oracle assertions fail for all eight
breaks with `tests/commonmark_oracle.py` from `67746d05` and pass at HEAD.

The new unit `_starts_in_a_comment` (`tests/commonmark_oracle.py:154`) and the · NAME NOT IN TREE
older `_comment_lines` (`:84`) both keep only `html_inline` tokens whose · NAME NOT IN TREE
content starts with `&lt;!--`. On CDATA, a processing instruction or an
attribute value the oracle says "shown", which is the walk's own answer, so
the property agrees with the walk by construction on that part of the class.
It is the failure round 2's 🟡 2 named, one token kind over. Executed: with
the proposed `FOUND` documents, the HEAD walk passes the property module
against the HEAD oracle (61 passed) and fails it against the widened oracle.
Over 20,000 seeded documents drawn from an alphabet that holds all four
openers, the HEAD walk leaves both readings for the config reader in 2,035
documents and disagrees with the widened oracle on a claimed line in 3,123.
The proposed walk scores 0 and 0.

The widened oracle labels those lines `comment`. The kind is the oracle's
name for "inside inline HTML", and its docstring has to say so; the fix
below does.

## The merge: the adjustment is right, and a rider after a break is read by one side only

**`region_lines` walks GFM lines as given, which is correct.** After #668 it
slices `checker.gfm_lines(text)`, and handing `comment_blocks` the text as
well made the walk answer by `str.splitlines`, one line off past the break.
Executed: the re-pinned region half fails for all eight breaks with
`rider_check.py` from `9de34fad` and passes at HEAD. `riders_in` still hands
over the text with `str.splitlines` lines, which is the pairing the walk
expects.

**The reader and the hasher still disagree on one shape.** `comment_blocks`
opens an HTML rider at a line that starts with `&lt;!--`. On the reader's split, a
marker written after a U+2028 or a form feed starts such a line. On GFM lines,
the hasher's, it sits mid-line and opens nothing. So `riders_in` returns a
rider that `region_lines` never cuts, and the rider's own stamp line sits
inside the region its hash covers. Executed with `# doc`, a paragraph, then
`body text` + break + a rider with a stamp:

| At | reader's riders | stamp line inside the hashed region |
|---|---|---|
| HEAD `8b1492aa`, LS and FF | `[(4, 5)]` | yes |
| #668's tip `2e392d4` | `[(4, 5)]` | yes |
| merge base `66b34a4e` | `[(4, 5)]` | no |

It arrived with #668 and the merge carried it here. What it costs: a rider
whose hash covers its own stamp moves every time `--reverify` writes it, so
it can never read ok. `comment_blocks`' docstring states the design that
rules this out: *without it the reader and `region_lines` disagree about what
a block is*. #664, still open, owns this class, a region cut where
`str.splitlines` breaks and GFM does not. So the finding is filed there and is
not this branch's to fix.

The drafted fix steps over a marker line that starts inside a GFM line, in the
reader, the way a quoted one is stepped over. Executed in the clone: the
mid-line rider is no longer read, a whole-line rider in the same file still
is, the rider and property modules pass (110), and `rider_check.py` over the
clone's tree says `19 ok · 0 drifted · 0 broken` both at HEAD and with the fix.

## The re-pinned rider case no longer asks the hasher its own question

`test_a_break_commonmark_does_not_honour_quotes_no_rider` is about a fence run
after a break that GFM does not honour. The adjustment replaced its region
half (`tests/test_a_rider_reaches_its_file.py:613`) with a document whose
break has no fence run after it, `A note{brk}more`. The new half is the right
pin for the merge's defect. The old half was the only one that asked the
hasher the case's own question, and it was deleted rather than kept beside the
new one. Executed: the old half still holds at HEAD for all eight breaks.
Against a `region_lines` mutant that walks the reader's split, the old half
fails and the new half passes. ⬜: no defect ships while the code stands, and
the fix is to keep both halves.

## The merge's ledger rows

Read row by row across base, ours, theirs, merge and adjustment by a probe
over the four conflicted files (`seal/releases/0.15.1.md`, `0.15.3.md`,
`0.5.0.md` and `0.9.1.md`):

- Every cell that only one side changed takes that side's text.
- Every anchor that only one side moved takes that side's hash.
- The two cells both sides edited (0.15.1 P3's notes, 0.9.1 S2's notes) hold
  both sides' notes. No note either side added is missing.
- The one anchor both sides moved, 0.9.1 S2 on `rider_check.py#region_lines`,
  is re-stamped by the adjustment, which also adds a re-read note.
- 0.9.1 S3 gains the adjustment's re-read, which covers the `comment_blocks`
  docstring edit.
- 0.15.3's P1-2 row is this branch's replacement, and #668 did not touch the
  row it replaced.

`bin/evidence-check .` at HEAD: exit 0, 2,889 ok, 0 drifted, 0 broken. That is
a probe, not a seal.

One row is now false in a shape. 0.9.1 S2 claims **every** rider block in the
anchored region is removed, and the merge's re-read repeats it: *every rider
block is still removed from the one list before the hash*. 🟡 3 is a rider
block in the region that is not removed. #668's own re-read made the same
claim first. This is a correction to the paperwork (⬜), and it is true again
once 🟡 3 is fixed.

## Carried, and what I did not run

- Ledger coordinates and where each unit lives were carried from the fragment
  and round 2's record. `evidence-check` confirmed none drifted.
- Round 1's four closures: the modules holding their cases pass at HEAD
  (executed). None of `hooks/`, the oracle or `run_tests.py` changed in the
  merge or its adjustment (read, `git diff --stat a297ae37 8b1492aa`).
  Finding 3's case lives in a module I did not run; I carried round 2's
  execution of it.
- Round 2's ❓, the per-reader case tables: the routing and config modules
  pass at HEAD in full (executed, 144 passed). The rest is the sealer's.
- The broad gate: not yet. The run ends with this record. Once the
  orchestrator has filed what is open, the sealer's spawn is what comes due.

## Regression tests to plant

- `tests/test_the_mode_question_is_asked_once.py`: the config case over three
  openers and eight breaks (fence below).
- `tests/test_the_hooks_hide_what_a_renderer_hides.py`: three `FOUND`
  documents (fence below), not alphabet lines.
- `tests/test_a_rider_reaches_its_file.py`: the old region half restored
  beside the new one.
- For #664: a rider marker after a U+2028 inside a paragraph is read by
  neither the reader nor the hasher (the drafted case sits in its fix's
  comment).

## Facts for the evidence ledger

- `hooks/blocks.py#walk_text`: a piece is uncertain where the text before it
  on its GFM line leaves an inline comment open. Other inline raw HTML is not
  looked for (read at `8b1492aa`; executed, the probe above).
- `.github/scripts/rider_check.py#riders_in` and `#region_lines` read
  different lines. The reader opens a rider at a marker after a break
  `str.splitlines` makes, and the hasher does not cut it (executed at
  `8b1492aa` and `2e392d4`).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A piece that starts inside inline raw HTML other than a comment (CDATA, a processing instruction, a tag's attribute value) that its GFM line opened is claimed live, so with a fence run earlier on the line the config reader reads a `Mode` row its base and a renderer both hide | `hooks/blocks.py:370` | open | executed: `config_rows` gives `[("Mode", "shared")]` for three openers × eight breaks at `8b1492aa`; base and an independent per-piece reading hide the line; 2,035 of 20,000 seeded documents leave both readings. Round 2's fix enumerated only `&lt;!--` (§12). The run is capped: this is a candidate for rung 1, since this work item created `hooks/blocks.py` |
| 🟡 2 | `_starts_in_a_comment` and `_comment_lines` keep only `html_inline` tokens that are comments, so the oracle cannot see 🟡 1 and agrees with the walk by construction on the rest of inline HTML | `tests/commonmark_oracle.py:154` | open | executed: with the proposed `FOUND` documents the HEAD walk passes the property module against this oracle (61 passed) and fails it against the widened one; this unit is new in round 2's fixes. Candidate for rung 1 · NAME NOT IN TREE |
| 🟡 3 | `riders_in` opens a rider at a marker after a break GFM does not honour, and `region_lines` (GFM lines since #668) never cuts it, so that rider's own stamp is inside the region its hash covers | `.github/scripts/rider_check.py:345` | deferred #664 | executed: reader `[(4, 5)]` and the stamp line in the hashed region at `8b1492aa` and at #668's tip `2e392d4`, not at the merge base `66b34a4e`. It arrived with #668, and #664 (open) owns the class, so rung 2 |
| ⬜ 4 | The re-pinned rider case dropped the region half that put a fence run after the break, so a hasher walking the reader's split passes it | `tests/test_a_rider_reaches_its_file.py:613` | open | executed: the old half holds at HEAD for eight breaks; under a splitlines mutant of `region_lines` the old half fails and the new half passes |
| ⬜ 5 | 0.9.1 S2's merge re-read says every rider block is removed from the one list before the hash; 🟡 3's rider is not | `seal/releases/0.9.1.md` | open | a paperwork correction, left out of `Needs a fix`; it becomes true again with 🟡 3's fix |
| 🟢 | round 2's blocking finding 1 is closed for its shape — a piece inside an inline comment its line opened is uncertain | `hooks/blocks.py:370` | confirmed | executed: the eight config cases and the `walk_text` case fail with `hooks/blocks.py` from `67746d05` (9 failed) and pass at HEAD |
| 🟢 | round 2's blocking finding 2 is closed for its shape — the oracle asks the parser where a piece starts | `tests/commonmark_oracle.py:180` | confirmed | executed: the two new oracle assertions fail for all eight breaks with the oracle from `67746d05` and pass at HEAD |
| 🟢 | the merge's adjustment — `region_lines` hands `comment_blocks` GFM lines and no text | `.github/scripts/rider_check.py:415` | confirmed | executed: the re-pinned half fails for all eight breaks with `rider_check.py` from `9de34fad`, passes at HEAD |
| 🟢 | the merge's ledger and test resolutions | `seal/releases/0.9.1.md` | confirmed | executed: row-by-row probe over four files; `evidence-check` 2,889 ok, 0 drifted; the merge added exactly #668's lines to the rider test module |
| 🟢 | round 1's findings 1, 2 and 4 are closed | `hooks/blocks.py:338` | confirmed | executed: the property, rider, routing and config modules pass at HEAD, and none of `hooks/` or the oracle changed in the merge |
| 🟢 | round 1's finding 3 is closed | `.github/scripts/run_tests.py:231` | confirmed | carried from round 2's execution; `run_tests.py` is untouched from `47f436aa` to `8b1492aa` (read) |
| ❓ | The per-reader case tables beyond the routing and config modules were not run | `tests/test_routing_is_recorded.py:717` | ❓ out of verified scope | the routing and config modules pass in full at HEAD (executed); the rest is the sealer's broad run |

## Paste-ready fixes

```python
# 🟡 1 — hooks/blocks.py, directly after leaves_open:

# Inline raw HTML other than a comment (CommonMark 6.6), and what ends each:
# CDATA at `]]>`, a processing instruction at `?>`, a declaration at `>`, a
# tag at a `>` outside its quoted attribute values. Each can run past a break
# inside its paragraph and hide what it holds, as a comment can (#667 round 3).
INLINE_HTML = re.compile(r"<(?:(!\[CDATA\[)|(\?)|(![A-Za-z])|/?[A-Za-z])")
TAG_END = re.compile(r"""(?:[^>"']|"[^"]*"|'[^']*')*>""")


def leaves_html_open(text):
    """Whether TEXT ends inside inline raw HTML other than a comment that
    began in it, read left to right, each opener to its own end.

    Like `leaves_open`, nothing here knows a code span, so an opener quoted
    in one counts, which errs only toward calling more lines uncertain.
    """
    at = 0
    while True:
        found = INLINE_HTML.search(text, at)
        if found is None:
            return False
        cdata, instruction, declaration = found.groups()
        if cdata or instruction or declaration:
            closer = "]]>" if cdata else "?>" if instruction else ">"
            end = text.find(closer, found.end())
            at = -1 if end == -1 else end + len(closer)
        else:
            tag = TAG_END.match(text, found.end())
            at = -1 if tag is None else tag.end()
        if at == -1:
            return True
```
```python
# 🟡 1 — hooks/blocks.py, in walk: the state, then the pending branch.
    all_from, live_from = None, None
    # STICKY: what left the paragraph open is inline HTML other than a
    # comment, whose end is not looked for below, so only a blank line or a
    # block start ends it.
    pending, indented, sticky = False, False, False

            if pending:
                uncertain[index] = True
                if CLOSER in line and not sticky:
                    rest = line[line.index(CLOSER) + len(CLOSER) :]
                    sticky = leaves_html_open(rest)
                    pending = sticky or leaves_open(rest)
            elif leaves_open(line) or leaves_html_open(line):
                pending, sticky = True, leaves_html_open(line)
```
```python
# 🟡 1 — hooks/blocks.py, in walk_text:
        before = renderer[line][: start - renderer_starts[line]]
        inside = walked.kinds[line] == LIVE and (
            leaves_open(before) or leaves_html_open(before)
        )
```
```python
# 🟡 1 — hooks/blocks.py, the module docstring's list of uncertain contexts,
# replacing its third bullet:
  - the paragraph lines after inline raw HTML a line leaves open -- a
    comment, CDATA, a processing instruction, a declaration or a tag -- and
    a piece of a line that starts inside it (#667 rounds 2 and 3);
```
```python
# 🟡 1 — tests/test_the_mode_question_is_asked_once.py, after
# test_a_piece_inside_an_inline_comment_is_no_config_row:
@pytest.mark.parametrize("name", ["LS", "PS", "NEL", "FF", "VT", "FS", "GS", "RS"])
@pytest.mark.parametrize(
    "opener, closer",
    [("<![CDATA[ a", "]]>"), ("<? a", "?>"), ('<span title="a', '">')],
    ids=["cdata", "instruction", "attribute"],
)
def test_a_piece_inside_other_inline_html_is_no_config_row(
    config, name, opener, closer
):
    """#667 round 3. A comment is one kind of inline raw HTML of five; CDATA,
    a processing instruction and a tag's attribute value hide what they hold
    too, and the fence run before the table is fenced to the base. The walk
    looked only for a comment opener, so the piece was claimed shown and a
    `Mode` row neither reading shows was read."""
    from block_shapes import BREAKS

    brk = BREAKS[name]
    text = (
        f"x {opener}{brk}```{brk}| Item | Value |{brk}|---|---|{brk}"
        f"| Mode | shared |\n{closer}\n"
    )
    assert config.config_rows(text) == []
```
```python
# 🟡 2 — tests/commonmark_oracle.py. In _comment_lines, the skip condition:
        if child.type != "html_inline":
            continue

# In _starts_in_a_comment, the match:
            if child.type == "html_inline" and SENTINEL in child.content:
                return True

# The module docstring's `comment` entry, replacing its first line:
  comment  inline raw HTML (6.6) -- a comment, CDATA, a processing
           instruction, a declaration or a tag -- that the line BEGINS inside
           (#667 round 3). The line where it opens begins outside it and is
           not hidden; every later line up to and including its closer is
```
```python
# 🟡 1 and 🟡 2 — tests/test_the_hooks_hide_what_a_renderer_hides.py, FOUND,
# last. In FOUND and not in ALPHABET: six alphabet lines push
# test_the_walk_is_exact_somewhere under its third, and an opener without
# its closer never forms inline HTML to the parser.
    # round 3: the same piece inside inline raw HTML other than a comment --
    # CDATA, a processing instruction, a tag's attribute value -- and a line
    # after it, inside the same paragraph
    ["x <![CDATA[ a" + BREAKS["LS"] + "```" + BREAKS["LS"] + "| a |", "]]>"],
    ["x <? a" + BREAKS["FF"] + "```" + BREAKS["FF"] + "| a |", "| b |", "?>"],
    ['x <span title="a' + BREAKS["NEL"] + "```", "| a |", '">'],
```
```python
# 🟡 3 (#664's ground) — .github/scripts/rider_check.py, above comment_blocks:
def mid_line(text):
    """0-based indices of `text.splitlines()` that start inside a GFM line,
    after a break `str.splitlines` makes and GFM does not."""
    global _blocks
    if _blocks is None:
        _blocks = load_blocks()
    heads, at = set(), 0
    for line in _blocks.gfm_lines(text, keepends=True):
        heads.add(at)
        at += len(line)
    out, at = set(), 0
    for index, piece in enumerate(text.splitlines(keepends=True)):
        if at not in heads:
            out.add(index)
        at += len(piece)
    return out


# In comment_blocks, directly after `quoted = (...)`:
    # A reader line that starts inside a GFM line is not the head of anything
    # to `region_lines`, which cuts blocks out of GFM lines; opening a rider
    # there hashed the rider's own stamp into its region (#664, #667 round 3).
    # Case: f"# doc\n\nbody{brk}" + HTML_MARK + " mid -->\n" gives no rider.
    if text is not None and any(MARKER in line for line in lines):
        quoted = quoted | mid_line(text)
```
```python
# ⬜ 4 — tests/test_a_rider_reaches_its_file.py,
# test_a_break_commonmark_does_not_honour_quotes_no_rider, directly after the
# riders_in assertion and before `region = (`:
    kept, why = riders.region_lines(CHECKER, "doc.md", '"# doc"', text)
    assert kept is not None, why
    assert not any("RIDER:" in line for line in kept), kept
```
```text
⬜ 5 — seal/releases/0.9.1.md, row S2, appended to its notes once 🟡 3 is fixed:
**Corrected <date> by the work item that takes #664:** from #668 until then a
rider marker written after a break `str.splitlines` makes and GFM does not was
read by `riders_in` and not cut by `region_lines`, so "every rider block" was
not true of that one; the reader now steps over such a marker and the claim
holds.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the property and rider modules at `8b1492aa`, `-p no:xdist` | exit 0, 110 passed |
| `bin/test` over the config module, `-k` on the break and inline-comment cases, at `8b1492aa` | exit 0, 18 passed |
| `bin/test` over the routing and config modules in full at `8b1492aa` | exit 0, 144 passed |
| The rider case with `rider_check.py` from `9de34fad` | exit 1, 8 failed (one per break); clone restored |
| Round 2's `walk_text` and config cases with `hooks/blocks.py` from `67746d05` | exit 1, 9 failed; clone restored |
| Round 2's oracle assertions with the oracle from `67746d05` | exit 1, 8 failed; clone restored |
| Probe: four openers × eight breaks through `config_rows`, the base, `walk_text`, the oracle and an independent per-piece reading, at `8b1492aa` | comment: `[]`. CDATA, processing instruction, attribute: `[("Mode", "shared")]`, base hides, walk live and certain, oracle shows, independent reading hides. Declaration: not reproduced; the probe's closing `>` opened a block quote |
| Probe: 20,000 seeded documents, all four openers, the HEAD walk against the widened oracle | config leaves both readings in 2,035; a claimed line disagrees in 3,123 |
| The same with the proposed walk | 0 and 0; claimed lines 39,942 of 166,932 (HEAD 105,164) on that opener-heavy alphabet |
| Claimed lines on the repository's own corpus, HEAD walk and proposed walk | 24,009 of 68,819 for both |
| The proposed 🟡 1 and 🟡 2 fixes in the clone, four modules | exit 0, 278 passed |
| The proposed tests and oracle with the HEAD walk | exit 1, 26 failed: 24 new config cases, half 1 for config, half 2 |
| The proposed walk and tests with the HEAD oracle; and the HEAD walk with the HEAD oracle and the new `FOUND` | exit 0, 61 passed for both: the HEAD oracle cannot see the class |
| The shapes as six `ALPHABET` lines instead of `FOUND`, with the proposed walk | exit 1, `test_the_walk_is_exact_somewhere` 22,166 of 69,084 |
| Probe: reader against hasher on a rider after LS and FF, at `8b1492aa`, `2e392d4` and `66b34a4e` | reader `[(4, 5)]` at all three; stamp line inside the hashed region at the first two, not at the merge base |
| The drafted 🟡 3 fix in the clone | mid-line rider not read, whole-line rider `(3, 4)` read; rider and property modules exit 0, 110 passed; `rider_check.py --root .` 19 ok, 0 drifted, 0 broken, as at HEAD |
| Probe: the rider case's old region half at HEAD, and a `region_lines` mutant walking the reader's split | old half holds for eight breaks; under the mutant the old half fails and the new half passes |
| Probe: the four conflicted ledger files row by row across base, ours, theirs, merge and adjustment | every one-sided cell and anchor takes its side; two-sided notes are unions with nothing missing; S2's two-sided anchor re-stamped |
| `bin/evidence-check .` at `8b1492aa`, read-only | exit 0; 2,889 ok, 0 drifted, 0 broken. A probe, not a seal |
| The broad gate: the full suite, lint and typecheck | not yet |

```python
# The reduced 🟡 1 shape; hooks loaded from the clone at 8b1492aa.
LS = chr(0x2028)
shape = ("x <![CDATA[ a" + LS + "```" + LS + "| Item | Value |" + LS
         + "|---|---|" + LS + "| Mode | shared |\n]]>\n")
config.config_rows(shape)             # [("Mode", "shared")]
blocks.fence_only(shape.splitlines())  # hides reader lines 1 to 4
```
```python
# The independent per-piece reading: any inline HTML, not only a comment.
SENT = "QqZzSENTzZqQ"
def piece_hidden(text, offset):
    doc = text[:offset] + SENT + text[offset:]
    for tok in oracle._PARSER.parse(doc):
        if tok.type in ("fence", "code_block", "html_block") and SENT in tok.content:
            return True
        if tok.type == "inline":
            for child in tok.children or []:
                if child.type == "html_inline" and SENT in child.content:
                    return True
    return False
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1, inline HTML other than a comment in the walk | candidate rung 1: this work item created `hooks/blocks.py`; the record commissions nothing, so the orchestrator places it | the smith of work item 1790645290 (#667) |
| 🟡 2, the oracle reads comments only | candidate rung 1, with 🟡 1; the unit is new in round 2's fixes | the smith of work item 1790645290 (#667) |
| 🟡 3, reader and hasher disagree on a rider after a break | #664, rung 2: open, and it owns the class of a region cut where `str.splitlines` breaks and GFM does not | the work item that takes #664 |
| ⬜ 4, the rider case's dropped region half | candidate rung 1 | the smith of work item 1790645290 (#667) |
| ⬜ 5, 0.9.1 S2's claim | with 🟡 3's fix, on #664 | the work item that takes #664 |

Needs a fix: yes — 🟡 1 and 🟡 2 (branch-owned units, the inline-HTML class
round 2's fix did not enumerate), and 🟡 3 on #664's ground
Loses a record or crashes: no

## Proof

Files opened for this round, in the clone at `8b1492aa` unless named:
`hooks/blocks.py`, `tests/commonmark_oracle.py`,
`.github/scripts/rider_check.py` (lines 200–720),
`tests/test_the_hooks_hide_what_a_renderer_hides.py` (lines 255–470 and the
round 2 diff), `tests/test_the_mode_question_is_asked_once.py` (lines
860–890), `tests/test_a_rider_reaches_its_file.py` (lines 570–620),
`hooks/config.py` (lines 145–240),
`seal/specs/1790645290-…/rounds/round-2.md`, the head of `round-2-report.md`,
`docs/review-chain-spec.md` (the reopening and the ladder),
`git show 8b1492aa`, `git diff 67746d05..d814848d -- hooks tests`, the merge's
diffs of `rider_check.py`, the rider test module and the four ledger files
against both parents and the merge base, and the fragment diffs of
`d814848d` and `8b1492aa`. Issue states for #658, #664, #667 and #668 were read
with `gh issue view`.
