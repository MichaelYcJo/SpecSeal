# 1790659274-the-walk-leaves-every-inline-html-construct-uncertain — review round 1

| Field | Value |
|---|---|
| Target SHA | 7a6f2d3e37cf33ac000f683024295a852cfdb6a8 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #676 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `c0d9045b953dee6a50f2ca9638528a9dc29fffd9..c041b5edb8fdf837ce81f43a2b30b20815b7170b`, 2 commits |
| Contract changes | none |
| New units | _behind_markers (depth 1) |
| Needs a fix | yes — 🟡 1 (the oracle's line count behind a list marker) and 🟡 2 (three readings of `leaves_html_open` no case pins) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first finding round, over the work item's own diff `3fc0c5bd...7a6f2d3e`. Asked to test F's invariant hardest: a piece still claimed live inside inline HTML, a sticky state hiding a declaration the base read, and an oracle agreeing with the walk by construction through its second sentinel or its token depth.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The oracle counts inline HTML lines one line too early in a list item whose first line holds only a Unicode space, because its count of stripped lines skips a `>` and not a list marker | `tests/commonmark_oracle.py:96` | **fixed** `7095f343` | fixed at 7095f343 — the oracle's line count reads past list and quote markers (`_behind_markers`), pinned by four rows; executed: `["- " + NBSP, "x <? a", "b ?>", "c"]` gives `{1: ...}` where a renderer hides line 2; all 12 fuzz disagreements are this shape, and 0 remain with the fix · NAME NOT IN TREE |
| 🟡 2 | Three readings the spec states are pinned by no case: the closer after the opener, `<?>` not closing, and a `>` inside a single-quoted value | `hooks/blocks.py:231` | **fixed** `7095f343` | fixed at 7095f343 — S4 pins the closer searched after the opener, `<?>` not closing, and a `>` inside a single-quoted value; executed: mutants m1, m2 and m3 each pass both modules (exit 0) and each reads `[("Mode", "shared")]` on its shape; HEAD reads `[]` |
| ⬜ 3 | Asking every tag opener scans to the tag's end once per opener, and `walk_text` asks again for every piece | `hooks/blocks.py:233` | answered | Measured over every tracked `.md`: 583 files in 0.158 s at HEAD against 0.133 s at the base, the slowest 7.6 ms; the quadratic shape exists in no file any reader opens, and bounding it would add mechanism; executed: 0.17 s, 0.70 s and 3.1 s at 10,001, 20,001 and 40,001 characters |
| 🟢 | The widening only adds uncertainty, and no claimed line is inside inline HTML | `hooks/blocks.py:213` | confirmed | read: pending is a superset of the base's per line; executed: 0 half-2 and 0 half-1 failures over 240,000 documents with 🟡 1's fix |
| 🟢 | Every opener asked, where the spec said left to right | `hooks/blocks.py:213` | confirmed | read against `html_re.py`, and executed by the fuzz |
| 🟢 | The rider case's region half is restored byte for byte | `tests/test_a_rider_reaches_its_file.py#test_a_break_commonmark_does_not_honour_quotes_no_rider` | confirmed | read: `8b1492aa^` lines 601-603 |
| 🟢 | 49 new cases fail with the base walk | `tests/test_the_hooks_hide_what_a_renderer_hides.py` | confirmed | executed: exit 1, 49 failed, 2 passed |
| ❓ | The eight breaks on Windows | `hooks/blocks.py` | ❓ out of verified scope | not run on Windows; CI's `windows-latest` leg at the pull request answers it |

## Paste-ready fixes

```python
# tests/commonmark_oracle.py -- a new helper directly above `_inline_html_lines`
def _behind_markers(line):
    """Where LINE's own text starts behind its containers' markers: a block
    quote's `>`, a bullet, an ordered number (CommonMark 5.1, 5.2), each with
    the spaces and tabs before it. A bullet or a number is a marker only
    where a space, a tab or the line's end follows it."""
    at = 0
    while True:
        rest = line[at:]
        text = rest.lstrip(" \t")
        skip = len(rest) - len(text)
        if text.startswith(">"):
            at += skip + 1
            continue
        digits = len(text) - len(text.lstrip("0123456789"))
        if text[:1] in ("-", "+", "*"):
            marker = 1
        elif 0 < digits <= 9 and text[digits : digits + 1] in (".", ")"):
            marker = digits + 1
        else:
            return at
        if text[marker : marker + 1] not in ("", " ", "\t"):
            return at
        at += skip + marker


# tests/commonmark_oracle.py#_inline_html_lines -- replaces the two-line loop
    while (
        first < inline.map[1] - 1
        and not lines[first][_behind_markers(lines[first]) :].strip()
    ):
        first += 1


# tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_oracle_names_each_kind_it_hides
# -- a row after the "between attributes" row
        # a list item whose first line holds only a Unicode space, which the
        # parser's strip drops: its marker is not text, so the lines are
        # counted from the next one
        (["- " + NBSP, "x <? a", "b ?>", "c"], {2: "inline html"}),
# -- and its id, after "between attributes"
        "behind a list marker",
```
```python
# tests/test_the_hooks_hide_what_a_renderer_hides.py#test_a_piece_inside_other_inline_html_its_line_left_open_is_unsure
# -- after the `quoted` assertion
    # `<?>` does not close a processing instruction: the `?` is the opener's
    instruction = blocks.walk_text(f"a <?>{ls}| r |\n?>\n\nd\n")
    assert instruction.uncertain[:2] == [False, True], instruction.uncertain
    # a closer before its opener closes nothing
    early = blocks.walk_text(f"a ?> <? b{ls}| r |\n?>\n\nd\n")
    assert early.uncertain[:2] == [False, True], early.uncertain
    # a `>` inside a single-quoted value does not end the tag either
    single = blocks.walk_text(f"a <span title='b>c{ls}d'>\n\ne\n")
    assert single.uncertain[:2] == [False, True], single.uncertain
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` at HEAD | exit 0, 74 passed |
| Fuzz probe: 4 seeds of 60,000 documents (seed 1: 5,000), one to six lines of openers, closers, code spans, backslashes, fence runs, table rows, list and quote markers and links, joined by spaces and all eight breaks; half 2 against the base walk and the new walk, half 1 for the config, routing and rider readers | new walk: 12 half-2 documents, all 🟡 1's shape; 0 half-1 failures. Base walk: 3,642 to 3,766 half-2 documents per 60,000 |
| The same four seeds with 🟡 1's oracle fix applied in the clone, then restored | new walk 0 half-2 and 0 half-1; property module exit 0, 74 passed |
| Mutants m1 to m4 of `hooks/blocks.py`, one at a time, restored from kept bytes, against the property module and the mode module (`-k "renderer or inline or comment or break"`) | m1, m2 and m3 exit 0, 136 passed; m4 exit 1, 2 failed |
| `config_rows` on each mutant's shape, under HEAD and under m1, m2 and m3 | HEAD `[]` on all three; each mutant `[("Mode", "shared")]` on its own shape (m1 on two) |
| 🟡 2's three assertions under HEAD and each mutant | `[False, True]` at HEAD; `[False, False]` under the mutant each one targets; the oracle hides each piece |
| `hooks/blocks.py` from `3fc0c5bd` over the new cases and the property halves, restored with `git checkout` | exit 1, 49 failed, 2 passed |
| `bin/evidence-check --ledger` on this work item's ledger fragment | exit 0 |
| `leaves_html_open` and `walk_text` timing on long lines | 8,000 tag openers in 40,001 characters: 3.1 s; `walk_text` over 2,000 pieces: 0.55 s |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet — no run has been made, and it is the sealer's once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
