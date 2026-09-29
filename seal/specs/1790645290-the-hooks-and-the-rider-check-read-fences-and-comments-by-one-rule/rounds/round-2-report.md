# Round 2 report: 1790645290, the hooks and the rider check read fences and comments by one rule

Round 2 is a verifying round. Its target is round 1's fix diff,
`faec1812..1cc892cc`, read in a `--no-local` clone of the work item's tree at
`47f436aa`. The commit on top, `47f436aa`, touches records only.

## How the findings relate

```
round 1, finding 1 (a break str.splitlines makes and CommonMark does not)
   |  fixed by walk_text: a reader line takes the answer of the GFM line it starts in
   v
🟡 1  a piece that starts inside an inline comment its own line opened takes
      the line's answer, "shown", while a renderer hides it; with a fence run
      earlier on that line the config reader reads a Mode row that neither
      its base nor a renderer shows
   |  and it was not caught because
   v
🟡 2  hidden_text, the oracle's new split, maps pieces by the same rule, so the
      property agrees with the walk by construction; it is also wrong the
      other way round, a piece just past a closing --> read as hidden
```

Round 1's four closed verdicts hold for the shapes they named. Both new
findings sit in units round 1's fixes created (`walk_text` and `hidden_text`),
so they are this branch's to fix.

## Findings

### 🟡 1 A piece that starts inside an inline comment is read as shown, and the config reader reads a Mode row nobody can see

`hooks/blocks.py:362-364` (`walk_text`). A reader line that begins in the
middle of a GFM line takes that GFM line's kind and its `uncertain` flag.
`walk` never calls the line that opens a mid-line `&lt;!--` uncertain. Only the
lines after it are, through `pending`. So every later piece of that same GFM
line is claimed as exact and live. A renderer disagrees: the piece starts
inside the inline comment and is hidden.

For the routing reader and the rider check this does no harm, because their
base hides nothing, so "shown" equals the base. The config reader's base is
the fence rule over the reader's split, and a fence run after the break is a
fence to that base. The executed shape is one GFM line, `x &lt;!-- a`, then
U+2028, a fence run, U+2028, a header row, U+2028, a separator row, U+2028,
`| Mode | shared |`, and then a line holding `-->`.

- At `47f436aa`, `config_rows` returns `[("Mode", "shared")]`.
- At `faec1812`, before the fix, it returns `[]`.
- The base (`config_base`) hides reader lines 1 to 5.
- An independent per-piece reading of markdown-it-py hides reader lines 1
  to 5 too.

So new(L) is in neither base(L) nor renderer(L) on reader lines 1 to 4. That
is the invariant the work item exists to hold, broken by the fix for round
1's finding 1. The same walk reaches `refusal`, the writer's `table_span` and
`broad-gate`'s `hidden_row_at`. By reading, not by running: `seal mode` would
then overwrite the row inside the comment and read it back as written.

This is not a record lost or a crash. It is a live `Mode` answer invented
from text a renderer hides, in a file shape that needs a line-separator
character inside an inline comment.

The fix makes such a piece uncertain, so it keeps its reader's base reading.
A piece is uncertain when its GFM line is LIVE and the text of that line
before the piece leaves an inline comment open (`leaves_open`). I ran it in
the clone:

- the reduced shape gives `[]`;
- an 80,000-document fuzz over the alphabet plus inline-comment pieces shows
  no invariant break in any of the three readers, and no disagreement on any
  line the walk claims;
- the property module and round 1's 29 new cases stay green.

### 🟡 2 The oracle's new split maps pieces by the walk's own rule, so the property cannot see finding 1

`tests/commonmark_oracle.py:158-159` (`hidden_text`). The oracle answers each
reader line with the answer of the CommonMark line it starts in, which is the
rule `walk_text` uses. The module's own docstring names the result: "The
oracle cannot catch this, because it is built the same way." It is wrong in
both directions.

- **Shown where a renderer hides it.** This is finding 1's direction. On the
  reduced shape `oracle.hidden_text` answers `{5: "comment"}`, which agrees
  with the walk, so `leaves_both` against the oracle is empty while against
  an independent reading it is `[1, 2, 3, 4]`.
- **Hidden where a renderer shows it.** Take a GFM line that begins inside a
  comment opened on the line above, `b -->`, then U+2028, then a fence run.
  The oracle calls the fence-run piece `comment`, and a renderer shows it,
  because it starts after the `-->`. Today no walk hides that piece, since the
  line is `pending` and so uncertain. But a walk that wrongly hid it would
  pass the property.

The alphabet shares the blind spot: no line of it holds a break inside an
inline comment, so the fuzz never builds finding 1's shape. Across 80,000
widened documents the oracle and an independent per-piece reading differ on
18,882, and the config property against the oracle reports none of the 3,815
breaks.

The fix asks each piece where it starts. A piece of a line inside a block the
renderer hides (fence, code or HTML block) takes the line's kind. A piece of
any other line is parsed again with a run of letters put at its start, and it
is `comment` when an inline comment token holds that run. This shares nothing
with the walk. Checked in the clone:

- with the fixed walk, the property module is green, 60 passed;
- with the old walk and the new oracle, cases and alphabet lines, 10 cases
  fail: the named config case under all 8 breaks, half 1 for the config
  reader, and half 2;
- with the fixed walk and the old oracle, the two new oracle assertions fail
  under all 8 breaks.

### Round 1's closed verdicts

- **Finding 1 (a break `str.splitlines` makes)** is closed for the shape it
  named. The 29 cases round 1 planted pass at `47f436aa`, and all 29 fail with
  the fix's code files put back to `faec1812`, so each was seen red. Every
  caller of the walk now passes the text: `config.py` (three walks),
  `routing.py#shown`, `rider_check.py` (both callers), `seal.py` (writer and
  write guard) and `broad_gate.py` (two questions). I enumerated them with
  one grep. `walk_text` also keeps the same indices as `text.splitlines()`,
  as `hidden_lines` expects. Finding 1 above is a new defect in the unit that
  fix created, not a reopening of this one.
- **Finding 2 (`>` without a space)** is closed. `CONTAINER` takes `>` with no
  following space, `[">```"]` is in `FOUND`, and the widened fuzz, which
  holds `` >``` `` and `>` followed by an opener or a row, has no disagreement
  on a claimed line once finding 1 is corrected.
- **Finding 3 (the parser-failure sentence)** is closed. I measured it again
  with the clone's pytest 9.1.1 and pytest-xdist 3.8.0 on two scratch modules,
  one of which imports a missing module. `-n 2` exits 1 with `2 passed, 1
  error`. `-p no:xdist` exits 2 with `Interrupted: 1 error during
  collection`. The sentence says both. The case is red at `faec1812`.
- **Finding 4 (`--->`)** is closed as a pin. The case named `past the first
  closer` is in the property module, which passes.

Round 1's question on the `-n auto` path is answered by the finding 3
measurement above. Its question on the S5 to S15 case tables stays with the
sealer's broad run.

## Regression tests to plant

- `tests/test_the_mode_question_is_asked_once.py`: a config case, all 8
  breaks, for finding 1's shape: `config_rows` gives `[]`. It is in the
  paste-ready fix, and it went red under all 8 breaks on the unfixed walk.
- `tests/test_the_hooks_hide_what_a_renderer_hides.py`: two assertions in
  `test_the_oracle_reads_the_text_not_a_readers_split`, one per direction of
  finding 2; four alphabet lines holding a break inside an inline comment or
  just past one; and one `FOUND` document.

## Facts for the evidence ledger

- `hooks/blocks.py#walk_text`: after the fix, a reader line that starts in
  the middle of a LIVE GFM line whose text before it leaves an inline comment
  open is uncertain. Today it is claimed as exact and live.
- `tests/commonmark_oracle.py#hidden_text`: after the fix, a piece of a line
  not in a hidden block is answered by where the piece starts, not by where
  its line starts.
- Editing `walk_text` drifts any row of this work item's ledger fragment that
  anchors it. The fixer re-reads those rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A reader line that starts inside an inline comment its own GFM line opened takes the line's "shown", so the config reader reads a `Mode` row that neither its base nor a renderer shows | `hooks/blocks.py:362` | open | executed: `config_rows` gives `[("Mode", "shared")]` at `47f436aa` and `[]` at `faec1812`; base and an independent reading both hide reader lines 1 to 5; 3,815 of 80,000 widened documents break the config invariant, and routing and rider break 0 because their base hides nothing |
| 🟡 2 | `hidden_text` maps a piece by the line it starts in, the walk's own rule, so the property cannot see finding 1, and it reads a piece past a closing `-->` as hidden | `tests/commonmark_oracle.py:158` | open | executed: on the reduced shape the oracle gives `{5: "comment"}` and `leaves_both` against it is empty; 18,882 of 80,000 widened documents differ from an independent per-piece reading; with the proposed oracle, the unfixed walk fails 10 cases |
| 🟢 | round 1's finding 1 is closed — a fence run or opener after a break CommonMark does not honour hides no declaration, row or rider | `hooks/blocks.py:338` | confirmed | executed: round 1's 29 cases pass at `47f436aa` and all fail with the code files at `faec1812`; every walk caller passes the text (read, one grep) |
| 🟢 | round 1's finding 2 is closed — a block quote needs no space after its marker | `hooks/blocks.py:98` | confirmed | executed: the property module passes with `[">```"]` in `FOUND`; the widened fuzz disagrees on no claimed line once finding 1 is corrected |
| 🟢 | round 1's finding 3 is closed — the parser-failure sentence says what pytest does | `.github/scripts/run_tests.py:231` | confirmed | executed: `-n 2` exits 1 with 2 passed and 1 error, `-p no:xdist` exits 2 interrupted at collection; the case fails at `faec1812` |
| 🟢 | round 1's finding 4 is closed — the oracle's `--->` divergence is pinned by name | `tests/test_the_hooks_hide_what_a_renderer_hides.py:97` | confirmed | executed: the case `past the first closer` passes in the property module, 60 passed |
| 🟢 | round 1's question on bin/test's parser-failure path under `-n auto` | `.github/scripts/run_tests.py:505` | answered | executed: a parallel run with a collection error runs the other cases and exits 1, as the sentence now says |
| ❓ | The per-reader case tables S5 to S8, S10, S12 and S15 beyond round 1's new cases were not run | `tests/test_routing_is_recorded.py:717` | ❓ out of verified scope | carried from round 1; the sealer's broad run answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` in the clone at `47f436aa` | exit 0, 60 passed |
| `bin/test` over the five touched modules, `-k` on round 1's new cases, at `47f436aa` | exit 0, 29 passed |
| The same 29 cases with `hooks`, `.github/scripts` and `skills` checked out at `faec1812` | exit 1, 29 failed, 8+8+8+2+2+1 by case; clone restored |
| Probe: the reduced shape through `config_rows`, `config_base`, `oracle.hidden_text` and a sentinel per-piece reading, at `47f436aa` and at `faec1812` | new `[("Mode", "shared")]`, old `[]`; base and independent reading hide 1 to 5; oracle `{5: "comment"}` |
| Probe: 20 seeds × 4,000 documents, `ALPHABET` plus 15 inline-comment-piece lines, all three readers against the independent reading | config 3,815 documents break the invariant, routing 0, rider 0; 14,680 documents disagree on a claimed line; oracle and independent reading differ on 18,882 |
| The same fuzz with the proposed `walk_text` fix | config 0, routing 0, rider 0, claimed-line disagreements 0 |
| The proposed fixes in the clone: property module plus the named cases across five modules | exit 0, 96 passed |
| Proposed oracle, cases and alphabet with the walk unfixed | exit 1, 10 failed: the named config case ×8, config half 1, half 2 |
| Proposed walk fix with the old oracle | exit 1: the oracle assertions ×8 fail (and `test_the_walk_is_exact_somewhere`, only while the alphabet held 20 new lines; 4 lines keep it green) |
| pytest 9.1.1 and xdist 3.8.0 on two scratch modules, one importing a missing module | `-n 2` exit 1, 2 passed 1 error; `-p no:xdist` exit 2, interrupted at collection |
| `bin/evidence-check .` in the clone at `47f436aa`, read-only | exit 0; 2,815 ok, 0 drifted, 0 broken. A probe, not a seal |
| The broad gate: the full suite, lint and typecheck | not yet |

### 🟡 1

```python
# the reduced shape; hooks loaded from the clone
LS, OPEN = chr(0x2028), "<" + "!--"
shape = ("x " + OPEN + " a" + LS + "```" + LS + "| Item | Value |" + LS
         + "|---|---|" + LS + "| Mode | shared |\n-->\n")
config.config_rows(shape)   # [("Mode", "shared")] at 47f436aa, [] at faec1812
```

### 🟡 2

```python
# an independent per-piece reading: the parser is asked where the piece starts
SENT = "QqZzSENTzZqQ"
def piece_hidden(text, offset):
    doc = text[:offset] + SENT + text[offset:]
    for tok in oracle._PARSER.parse(doc):
        if tok.type in ("fence", "code_block", "html_block") and SENT in tok.content:
            return True
        if tok.type == "inline":
            for child in tok.children or []:
                if (child.type == "html_inline" and child.content.startswith(OPEN)
                        and SENT in child.content):
                    return True
    return False
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1

```python
# hooks/blocks.py, in walk_text, the loop over the reader's lines:
    for start in _starts(text.splitlines(keepends=True)):
        while line + 1 < len(renderer_starts) and renderer_starts[line + 1] <= start:
            line += 1
        at_start = start == renderer_starts[line]
        # A piece that starts inside an inline comment its own line opened
        # is hidden by a renderer while the line is shown (#667 round 2), so
        # the walk is not sure of it and the reader keeps its base reading.
        inside = (
            not at_start
            and walked.kinds[line] == LIVE
            and leaves_open(renderer[line][: start - renderer_starts[line]])
        )
        kinds.append(walked.kinds[line])
        uncertain.append(walked.uncertain[line] or inside)
        of.append((line, at_start))
```

```python
# hooks/blocks.py, walk_text's docstring, the sentence that states the rule:
    reader line takes the answer of the GFM line it starts in: a piece of a
    hidden line is hidden, a piece of a shown line is shown unless the line
    opened an inline comment before it and left it open -- then a renderer
    hides the piece, and the walk calls it uncertain (#667 round 2) -- and a
    piece of a line the walk is not sure of keeps its reader's base reading.
```

```python
# tests/test_the_mode_question_is_asked_once.py, beside
# test_a_break_commonmark_does_not_honour_hides_no_config_row:
@pytest.mark.parametrize("name", ["LS", "PS", "NEL", "FF", "VT", "FS", "GS", "RS"])
def test_a_piece_inside_an_inline_comment_is_no_config_row(config, name):
    """#667 round 2. A table written after a break inside an inline comment
    its line opened is inside that comment to a renderer, and the fence run
    before it is fenced to the base. Read by the line it starts in, the piece
    took the line's answer, shown, and a `Mode` row neither reading shows was
    read."""
    from block_shapes import BREAKS, OPEN

    brk = BREAKS[name]
    text = (
        f"x {OPEN} a{brk}```{brk}| Item | Value |{brk}|---|---|{brk}"
        "| Mode | shared |\n-->\n"
    )
    assert config.config_rows(text) == []
```

### 🟡 2

```python
# tests/commonmark_oracle.py, above hidden_text, and hidden_text itself:
SENTINEL = "QzxSENTINELxzQ"


def _starts_in_a_comment(text, offset):
    """Whether the text from OFFSET, in the middle of a CommonMark line, is
    inside an inline HTML comment: the parser reads TEXT with a run of
    letters put at OFFSET, and a comment it finds holds that run."""
    marked = text[:offset] + SENTINEL + text[offset:]
    for token in _PARSER.parse(marked):
        if token.type != "inline":
            continue
        for child in token.children or []:
            if (
                child.type == "html_inline"
                and child.content.startswith("<" + "!--")
                and SENTINEL in child.content
            ):
                return True
    return False


def hidden_text(text):
    """{index: kind} for every line of `text.splitlines()` a renderer hides.

    **The renderer reads TEXT, not a reader's split of it** (#667 round 1,
    🟡 1). `str.splitlines` also ends a line at U+2028, NEL, a form feed and
    five more characters, and CommonMark does not, so a reader's line can be a
    piece of a renderer's line. The parser is given CommonMark's lines. A
    reader line that starts a CommonMark line takes that line's answer, and so
    does a piece of a line in a block the renderer hides. **A piece of any
    other line is asked where it starts** (#667 round 2): an inline comment
    can open before it or close before it on the same line, so the line's
    answer is not the piece's.
    """
    commonmark = commonmark_lines(text)
    found = _hidden_commonmark([line.rstrip("\r\n") for line in commonmark])
    renderer_starts = _starts(commonmark)
    out = {}
    line = 0
    for index, start in enumerate(_starts(text.splitlines(keepends=True))):
        while line + 1 < len(renderer_starts) and renderer_starts[line + 1] <= start:
            line += 1
        kind = found.get(line)
        if start == renderer_starts[line] or kind in (FENCE, CODE, HTML):
            if kind:
                out[index] = kind
        elif _starts_in_a_comment(text, start):
            out[index] = COMMENT
    return out
```

```python
# tests/test_the_hooks_hide_what_a_renderer_hides.py,
# test_the_oracle_reads_the_text_not_a_readers_split, after its two asserts:
    # round 2: a piece is asked where it starts, not where its line does
    assert oracle.hidden_text(f"x {OPEN} a{brk}| b |\n{CLOSE}\n") == {
        1: "comment",
        2: "comment",
    }
    assert oracle.hidden_text(f"x {OPEN} a\nb {CLOSE}{brk}| c |\n") == {1: "comment"}
```

```python
# ALPHABET, after the f"{brk}{CLOSE}" lines. Four lines, not one per break:
# twenty pushed test_the_walk_is_exact_somewhere under its third.
    # The same break inside an inline comment its line opened, and after one
    # a line closed, so a piece can start inside a comment or just past one
    # (#667 round 2). Two breaks, so the lines a mid-line opener leaves
    # uncertain do not crowd out the lines the walk claims.
    f"x {OPEN} a{BREAKS['LS']}```",
    f"x {OPEN} a{BREAKS['FF']}| a |",
    f"x {OPEN} a{BREAKS['NEL']}{CLOSE}",
    f"b {CLOSE}{BREAKS['LS']}```",

# FOUND, last:
    # round 2: a piece that starts inside an inline comment its line opened
    ["x " + OPEN + " a" + BREAKS["LS"] + "```" + BREAKS["LS"] + "| a |", CLOSE],
```

Needs a fix: yes — 🟡 1 and 🟡 2

Loses a record or crashes: no

## Proof

Files opened this round, all at `47f436aa` in the clone, unless the line says
otherwise:

- `seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/rounds/round-1.md` and `round-1-report.md`, in the work item's tree
- the fix diff `faec1812..1cc892cc` for `hooks/`, `.github/scripts/`, `skills/` and `tests/`, and for the work item's `changelog.md`; the commit messages of `2b108716`, `34682327` and `45d6eb4d`
- `hooks/blocks.py` and `tests/commonmark_oracle.py`, whole
- `hooks/config.py` lines 180–300
- `.github/scripts/rider_check.py` lines 235–345
- `.github/scripts/run_tests.py` lines 440–520
- `tests/test_the_hooks_hide_what_a_renderer_hides.py` lines 140–500
- `tests/conftest.py` lines 486–511
- the grep over `hooks`, `skills` and `.github` for every caller of the walk and its readers
