# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — review round 2

| Field | Value |
|---|---|
| Target SHA | 47f436aaeb3ac8be0f732cf792699d7672bd474e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #672 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `67746d05a5b32502bebcee382e95da7f86fd7aac..d814848dc214f01677ec9387eec036b8cc739a22`, 4 commits |
| Contract changes | none |
| New units | SENTINEL (depth 1); _starts_in_a_comment (depth 1); test_a_piece_inside_its_lines_open_comment_is_the_only_piece_unsure (depth 1); test_a_piece_inside_an_inline_comment_is_no_config_row (depth 1) |
| Needs a fix | yes — 🟡 1 and 🟡 2 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, verifying, over round 1's fix diff `faec1812..1cc892cc` at HEAD `47f436aa`. Asked whether each verdict round 1 closed is closed, with `walk_text`, the `gfm_lines` copy, `hidden_text` and the new cases as a finding surface, and whether a piece that begins mid-GFM-line, the widened alphabet, or the oracle's own split breaks the invariant.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A reader line that starts inside an inline comment its own GFM line opened takes the line's "shown", so the config reader reads a `Mode` row that neither its base nor a renderer shows | `hooks/blocks.py:362` | **fixed** `aa156990` | fixed at aa156990 — pinned in `311e6af6`: a piece is uncertain when its GFM line is live and the text before the piece leaves an inline comment open; executed: `config_rows` gives `[("Mode", "shared")]` at `47f436aa` and `[]` at `faec1812`; base and an independent reading both hide reader lines 1 to 5; 3,815 of 80,000 widened documents break the config invariant, and routing and rider break 0 because their base hides nothing |
| 🟡 2 | `hidden_text` maps a piece by the line it starts in, the walk's own rule, so the property cannot see finding 1, and it reads a piece past a closing `-->` as hidden | `tests/commonmark_oracle.py:158` | **fixed** `66daa3a3` | fixed at 66daa3a3 — the oracle asks the parser where each piece starts, by a sentinel re-parse, so it no longer agrees with the walk by construction; executed: on the reduced shape the oracle gives `{5: "comment"}` and `leaves_both` against it is empty; 18,882 of 80,000 widened documents differ from an independent per-piece reading; with the proposed oracle, the unfixed walk fails 10 cases |
| 🟢 | round 1's finding 1 is closed — a fence run or opener after a break CommonMark does not honour hides no declaration, row or rider | `hooks/blocks.py:338` | confirmed | executed: round 1's 29 cases pass at `47f436aa` and all fail with the code files at `faec1812`; every walk caller passes the text (read, one grep) |
| 🟢 | round 1's finding 2 is closed — a block quote needs no space after its marker | `hooks/blocks.py:98` | confirmed | executed: the property module passes with `[">```"]` in `FOUND`; the widened fuzz disagrees on no claimed line once finding 1 is corrected |
| 🟢 | round 1's finding 3 is closed — the parser-failure sentence says what pytest does | `.github/scripts/run_tests.py:231` | confirmed | executed: `-n 2` exits 1 with 2 passed and 1 error, `-p no:xdist` exits 2 interrupted at collection; the case fails at `faec1812` |
| 🟢 | round 1's finding 4 is closed — the oracle's `--->` divergence is pinned by name | `tests/test_the_hooks_hide_what_a_renderer_hides.py:97` | confirmed | executed: the case `past the first closer` passes in the property module, 60 passed |
| 🟢 | round 1's question on bin/test's parser-failure path under `-n auto` | `.github/scripts/run_tests.py:505` | answered | executed: a parallel run with a collection error runs the other cases and exits 1, as the sentence now says |
| ❓ | The per-reader case tables S5 to S8, S10, S12 and S15 beyond round 1's new cases were not run | `tests/test_routing_is_recorded.py:717` | ❓ out of verified scope | carried from round 1; the sealer's broad run answers it |

## Paste-ready fixes

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

```python
# the reduced shape; hooks loaded from the clone
LS, OPEN = chr(0x2028), "<" + "!--"
shape = ("x " + OPEN + " a" + LS + "```" + LS + "| Item | Value |" + LS
         + "|---|---|" + LS + "| Mode | shared |\n-->\n")
config.config_rows(shape)   # [("Mode", "shared")] at 47f436aa, [] at faec1812
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/blocks.py:208` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/blocks.py:89` | round 1's 🟡 2 — fixed |
| round-1 | `.github/scripts/run_tests.py:491` | round 1's 🟡 3 — fixed |
| round-1 | `tests/commonmark_oracle.py:48` | round 1's ⬜ 4 — fixed |
| round-1 | `.github/scripts/run_tests.py:505` | round 1's ❓ — out of verified scope |
| round-1 | `tests/test_routing_is_recorded.py:717` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
