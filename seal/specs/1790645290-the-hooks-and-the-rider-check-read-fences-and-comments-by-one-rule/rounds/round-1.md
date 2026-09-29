# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — review round 1

| Field | Value |
|---|---|
| Target SHA | 9b52cf2517a36429662755d00c07ed871539d36d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #672 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1, 🟡 2 and 🟡 3 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1, the first finding round, over the work item's own diff `66b34a4e...9b52cf25`. Asked to find a document where the invariant `new(L) ∈ {base(L), renderer(L)}` fails in either direction, a shape where the markdown-it-py oracle is itself wrong, and whether `bin/test`'s dependency handling can break an adopted `.venv` or CI.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A line break that `str.splitlines` makes and CommonMark does not lets the walk hide a live routing declaration, a live `Mode` row and a live rider | `hooks/blocks.py:208` | open | executed: `routing.parse` gives None, `config_rows` gives nothing, the rider is gone, and the base read all three; the oracle cannot see it because it is handed the reader's split |
| 🟡 2 | `CONTAINER` needs a space after `>`, so `` >``` `` is claimed live and exact while a renderer hides it | `hooks/blocks.py:89` | open | executed: 1,599 of 1,888 half-2 disagreements reduce to that one line; half 1 fails for the config reader on 3 reduced shapes; the fix clears both and keeps the module green |
| 🟡 3 | With the parser missing, bin/test says the other cases still run, and pytest interrupts collection and runs none | `.github/scripts/run_tests.py:491` | open | executed: exit 2, `Interrupted: 1 error during collection`, zero cases run from the second module; the case at `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:799` pins the claim under a mock |
| ⬜ 4 | The oracle runs an inline comment past a `-->` that a `-` precedes, which CommonMark 0.31.2 excludes | `tests/commonmark_oracle.py:48` | open | executed: one `html_inline` token past the first closer; every remaining fuzz disagreement holds a `--->` line; no reader affected |
| ❓ | bin/test's parser-failure path under `-n auto` | `.github/scripts/run_tests.py:505` | ❓ out of verified scope | not run; the smith answers it in the slice that fixes 🟡 3 |
| ❓ | The per-reader case tables S5 to S8, S10, S12 and S15 were read in part and not run by this round | `tests/test_routing_is_recorded.py:717` | ❓ out of verified scope | only the property module was run here; the sealer's broad run answers the rest |

## Paste-ready fixes

```python
# The line breaks `str.splitlines` makes and CommonMark does not: CommonMark
# ends a line at "\n", "\r" or "\r\n" alone. Where a file holds one, a
# reader's line is not a renderer's line, and a fence or a comment opener the
# split put at a line's start is one no renderer sees there. So the walk
# claims nothing in such a file, and every reader keeps its base reading.
FOREIGN_BREAKS = frozenset("\x0b\x0c\x1c\x1d\x1e\x85

")


def walk_text(text, lines):
    """`walk(lines)` for LINES split from TEXT, or a walk that claims no
    line where TEXT holds a break CommonMark does not honour."""
    if FOREIGN_BREAKS.isdisjoint(text):
        return walk(lines)
    count = len(lines)
    return Walk([LIVE] * count, [True] * count, [])
```
```python
def shown(lines, text=None):
    """[(index, line)] for each of LINES `table_rows` reads, ending removed.
    TEXT, where the caller has it, is what LINES were split from."""
    walked = blocks.walk(lines) if text is None else blocks.walk_text(text, lines)
    hidden = walked.hidden()
    return [
        (index, raw.rstrip("\r\n"))
        for index, raw in enumerate(lines)
        if index not in hidden
    ]

# in table_rows:
    for _index, line in shown(text.splitlines(), text):
```
```python
def fence_map(lines, text=None):
    hidden, opened_at = hidden_lines(lines, text)
    ...

def hidden_lines(lines, text=None):
    walked = blocks.walk(lines) if text is None else blocks.walk_text(text, lines)
    base, base_opened = blocks.fence_only(lines)
    ...

def unfenced(lines, text=None):
    ...
    yield from fence_map(lines, text)[0]

# config_rows and refusal:
    for _index, line in unfenced(text.splitlines(), text):
```
```python
# skills/implement/scripts/seal.py, table_span (its lines keep their endings):
    for i, line in unfenced(lines, "".join(lines)):
# skills/implement/scripts/seal.py, the write guard:
        if fence_map(new.splitlines(), new)[1] is not None:
# skills/verify/scripts/broad_gate.py, hidden_row_at:
    hidden, _opened_at = config.hidden_lines(lines, text)
# skills/verify/scripts/broad_gate.py, fence_left_open:
    opened_at = config.fence_map(text.splitlines(), text)[1]
```
```python
def quoted_lines(lines, text=None):
    ...
    walked = _blocks.walk(lines) if text is None else _blocks.walk_text(text, lines)
    ...

def comment_blocks(lines, rel=None, text=None):
    ...
    quoted = (
        quoted_lines(lines, text)
        if (rel or "").endswith(".md") and any(MARKER in line for line in lines)
        else set()
    )

# both callers, which split `text` themselves:
    comment_blocks(text.splitlines(), rel, text)
```
```python
# tests/test_routing_is_recorded.py
@pytest.mark.parametrize("brk", ["
", "\x0c", "\x85"], ids=["ls", "ff", "nel"])
def test_a_break_commonmark_does_not_honour_hides_no_declaration(brk):
    """A line break `str.splitlines` makes and a renderer does not put the
    comment opener at no line's start, so the table under it is live and the
    base read it (#667, round 1 🟡 1)."""
    from block_shapes import OPEN, TABLE

    text = "\n".join([f"A note{brk}{OPEN}", "", *TABLE, "-->"]) + "\n"
    parsed = routing.parse(text)
    assert parsed is not None and parsed["review"] == CHAIN, parsed
```
```python
# tests/test_the_mode_question_is_asked_once.py
def test_a_break_commonmark_does_not_honour_hides_no_config_row():
    """#667, round 1 🟡 1: the same shape in config.md."""
    open_ = "<" + "!--"
    text = f"A note
{open_}\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n-->\n"
    assert config.config_rows(text) == [("Mode", "shared")]
```
```python
# tests/test_a_rider_reaches_its_file.py
def test_a_break_commonmark_does_not_honour_quotes_no_rider():
    """#667, round 1 🟡 1: a fence run after U+2028 opens no fence for a
    renderer, so the rider below it is live and is read."""
    open_ = "<" + "!--"
    lines = (
        "# doc\n\nA note
```\n\n"
        f"{open_} RIDER: real\nVerified 2026-01-01 against r@abcdef12. -->\n\n```\n"
    )
    assert len(rc.comment_blocks(lines.splitlines(), "doc.md", lines)) == 1
```
```python
# A container's marker run in front of a line: indentation, a block quote's
# `>`, a list item's bullet or number. What follows it is what the line is.
# A list marker needs a space, a tab or the line's end after it; a block
# quote's `>` needs nothing (CommonMark 5.1, the space after it may be
# omitted), so `>` followed by a fence run is a fence inside a quote.
CONTAINER = re.compile(r"^(?:[ \t]*(?:>|(?:[-+*]|\d{1,9}[.)])(?=[ \t]|$)))*[ \t]*")
```
```python
# ALPHABET, beside "> ```":
    ">```",
    ">" + OPEN,
    ">| a |",

# FOUND:
    # a block quote needs no space after its marker
    [">```"],
```
```python
    if subprocess.run(step).returncode != 0:
        return (
            f"bin/test: could not install {MARKDOWN_IT} into {venv} (the "
            "command above exited non-zero). The suite's CommonMark oracle "
            "imports it, so pytest stops at collection and runs no case. "
            "Remove that directory and run bin/test again to build it afresh "
            "with the parser in it."
        )
```
```python
    # The parser the oracle reads (#667). Its failure is a sentence and a
    # pytest run that stops at collection: the oracle's module cannot import,
    # and pytest runs no case while any module fails to collect. It decides
    # nothing about `-n auto`.
```
```python
    What a failed install costs is different, and the sentence says so: the
    run is not serial, it stops at collection, because the oracle's module
    cannot import and pytest runs nothing while one module fails to collect.
```
```python
    assert "stops at collection and runs no case" in err, err
```
```python
        # markdown-it-py 4.2.0 runs a comment past a closer a `-` precedes,
        # which CommonMark 0.31.2 §6.6 does not; pinned so a wider corpus
        # meets the divergence by name. The walk follows the specification.
        (
            ["x " + OPEN + " a", "b ---> c", "d " + CLOSE + " e", "f"],
            {1: "comment", 2: "comment"},
        ),
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` in the clone at `9b52cf25` | exit 0, 49 passed |
| Probe: the 🟡 1 shapes (U+2028, form feed, U+0085) through `routing.parse`, `config_rows` and `comment_blocks`, and the oracle on the real text | routing None, config `[]`, rider `[]`; the oracle on the real text hides nothing |
| Probe: 40 seeds × 5,000 documents, `ALPHABET` plus 37 lines, halves 1 and 2 for all three readers | 1,888 half-2 disagreements in 116 reduced shapes; config leaves both in 12 documents; routing 0; rider check 0 |
| Probe: the same fuzz with `CONTAINER` fixed | 61 reduced half-2 shapes, every one holding `--->`; module corpus 0; `test_the_walk_is_exact_somewhere` passes |
| Probe: pytest in a virtualenv without markdown-it-py, over two modules | exit 2, interrupted at collection, zero cases |
| `python3 skills/evidence-check/scripts/evidence_check.py .` in the clone, one run, read-only | exit 0; 0 drifted and 0 broken in every file. A probe, not a seal |
| The broad gate: the full suite, lint and typecheck | not yet |

```python
import importlib.util, os
root = "."  # the clone at 9b52cf25
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(root, path))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
routing = load("hooks/routing.py", "r")
OPEN = "<" + "!--"
text = ("A note
" + OPEN + "\n\n| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n| Branch | feature/x |\n-->\n")
print(routing.parse(text))  # None at 9b52cf25
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
