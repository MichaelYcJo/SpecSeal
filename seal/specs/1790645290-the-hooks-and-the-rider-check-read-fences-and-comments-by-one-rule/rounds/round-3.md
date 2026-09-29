# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — review round 3

| Field | Value |
|---|---|
| Target SHA | 8b1492aa7287fa718d30d7052a3a8cbf4f86c69e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #672 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 and 🟡 2 (branch-owned units, the inline-HTML class round 2's fix did not enumerate), and 🟡 3 on #664's ground |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 closed on its one reopening. Targets: round 2's fix diff `67746d05..d814848d`, and the merge of `release/v0.16.0` (`9de34fad`) with its adjustment (`8b1492aa`), at HEAD `8b1492aa`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A piece that starts inside inline raw HTML other than a comment (CDATA, a processing instruction, a tag's attribute value) that its GFM line opened is claimed live, so with a fence run earlier on the line the config reader reads a `Mode` row its base and a renderer both hide | `hooks/blocks.py:370` | open | executed: `config_rows` gives `[("Mode", "shared")]` for three openers × eight breaks at `8b1492aa`; base and an independent per-piece reading hide the line; 2,035 of 20,000 seeded documents leave both readings. Round 2's fix enumerated only `&lt;!--` (§12). The run is capped: this is a candidate for rung 1, since this work item created `hooks/blocks.py` |
| 🟡 2 | `_starts_in_a_comment` and `_comment_lines` keep only `html_inline` tokens that are comments, so the oracle cannot see 🟡 1 and agrees with the walk by construction on the rest of inline HTML | `tests/commonmark_oracle.py:154` | open | executed: with the proposed `FOUND` documents the HEAD walk passes the property module against this oracle (61 passed) and fails it against the widened one; this unit is new in round 2's fixes. Candidate for rung 1 |
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/blocks.py:208` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/blocks.py:89` | round 1's 🟡 2 — fixed |
| round-1 | `.github/scripts/run_tests.py:491` | round 1's 🟡 3 — fixed |
| round-1 | `tests/commonmark_oracle.py:48` | round 1's ⬜ 4 — fixed |
| round-1 | `.github/scripts/run_tests.py:505` | round 1's ❓ — out of verified scope |
| round-1 | `tests/test_routing_is_recorded.py:717` | round 1's ❓ — out of verified scope |
| round-2 | `hooks/blocks.py:362` | round 2's 🟡 1 — fixed |
| round-2 | `tests/commonmark_oracle.py:158` | round 2's 🟡 2 — fixed |
| round-2 | `hooks/blocks.py:338` | round 2's 🟢 — confirmed |
| round-2 | `hooks/blocks.py:98` | round 2's 🟢 — confirmed |
| round-2 | `.github/scripts/run_tests.py:231` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_hooks_hide_what_a_renderer_hides.py:97` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1, inline HTML other than a comment in the walk | candidate rung 1: this work item created `hooks/blocks.py`; the record commissions nothing, so the orchestrator places it | the smith of work item 1790645290 (#667) |
| 🟡 2, the oracle reads comments only | candidate rung 1, with 🟡 1; the unit is new in round 2's fixes | the smith of work item 1790645290 (#667) |
| 🟡 3, reader and hasher disagree on a rider after a break | #664, rung 2: open, and it owns the class of a region cut where `str.splitlines` breaks and GFM does not | the work item that takes #664 |
| ⬜ 4, the rider case's dropped region half | candidate rung 1 | the smith of work item 1790645290 (#667) |
| ⬜ 5, 0.9.1 S2's claim | with 🟡 3's fix, on #664 | the work item that takes #664 |
