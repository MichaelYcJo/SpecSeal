# 1791119073-a-pact-row-outside-the-config-table-is-refused — review round 4

| Field | Value |
|---|---|
| Target SHA | 9501cbc445eed3761725e42c2f84cd26fd8ad114 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #784 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a link destination or title the new pattern cannot parse; four spellings regressed from 180d22b2), 🟡 2 (an empty comment), 🟡 3 (a reference with no `;`), 🟡 4 (a backtick on a live-table row the walk does not take) |
| Loses a record or crashes | yes — under each of 🟡 1–4, `evidence-check --reverify` exits 0 and re-stamps a moved row citing no clause under `always` with no pact change recorded; executed through the writer for `[Pact notify](it's)`, `&lt;!-->Pact notify&lt;!-- -->`, `Pact&notify`, a pipe-less code-span row and a three-cell code-span row, and through the vendored copy for the first three |

- [ ] Pass

## What this round was asked

Round 4 of #759 (PR #784), the verifying round after the round cap and the run's last, at 9501cbc4: open round 3's fixes (range 180d22b2..92a6a90a) and judge whether each closes its finding with no regression — the five raw-HTML kinds read through the tree's own inline reader, images, link titles, GFM's whitespace set, the code-span strip on the walk's rows, the corpus generated per CommonMark inline construct and held to cmark-gfm both ways — and whether the construct list is complete for what a person reads as `Pact notify` in a rendered table cell.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A link destination holding an apostrophe or a double quote, two levels of parentheses, or a title holding an escaped quote is silent at the target and refused at 180d22b2; an escaped or angle-bracketed `)` in the destination and an image alt holding brackets are silent at both | `hooks/config.py:724` | open | executed: the probe at 180d22b2 and at the target with cmark-gfm 2025.10.22 shows the item for all seven; the writer and the vendored copy each exit 0 and re-stamp unrecorded for `[Pact notify](it's)`. Round 3's fix wrote the line, inside `shape_line` (round 1's unit); the vendored copy at `evidence_check.py:3790` is identical |
| 🟡 2 | An empty comment, `&lt;!-->` or `&lt;!--->`, before the item removes the item from what the shape reads, so the row is silent | `hooks/config.py:706` | open | executed: cmark-gfm renders the item; the closer search starts after the opener's dashes; the writer and the vendored copy re-stamp unrecorded. Silent at 180d22b2 too; this is the raw-HTML axis round 3 took on, and its corpus has no empty comment |
| 🟡 3 | `html.unescape` decodes a legacy name with no `;`, so `Pact&notify` reads as `Pact¬ify` and is silent where cmark-gfm shows `Pact&notify` | `hooks/config.py:722` | open | executed: the writer and the vendored copy re-stamp unrecorded; silent at 180d22b2 and at the base. The same rule causes round 3's recorded over-refusal of `&nbsp notify` |
| 🟡 4 | Round 3's yellow 1 still has members: a backtick in the item of a live-table row `CONFIG_ROW` does not take (no leading pipe, no trailing pipe, indented, a third cell) is silent | `hooks/config.py:963` | open | executed: five rows that cmark-gfm renders in the live table as `Pact notify` are silent at the target, and the same rows without the backtick refuse; the writer re-stamps unrecorded for the pipe-less and three-cell rows. `stray_pact_rows` is the build's unit |
| 🟢 | round 3's yellow 1 finding is closed on the walk's rows — a backtick anywhere in the item of a row the walk took refuses, and the documentation tables stay silent | `hooks/config.py:963` | confirmed | executed: the round 3 code-span cases and S7's guards pass in the seven-module run; read: `docs/the-pact.md:336` names the vendored limit as any backtick. The rows the walk does not take are 🟡 4 |
| 🟢 | round 3's raw-HTML finding is closed for what it built — the five kinds through `hooks/config.py#RAW_HTML` and `TAG_END`, autolinks kept, a quoted `>` and a `)` in a quoted title handled, GFM's whitespace set, the copies equal | `hooks/config.py:673` | confirmed | read: `RAW_HTML` is built from `hooks/blocks.py#INLINE_HTML` and `TAG_END` is `blocks.TAG_END`; executed: the corpus and S14 pass; no declaration or shaped line changed across 646 files. The remaining members are 🟡 1–3 |
| 🟢 | round 3's white 3 is closed — `letters` keeps digits and the must-not branch runs | `tests/test_a_signatory_declares_its_pact.py:474` | confirmed | executed: with `isalpha`, 66 must-not cases fail at the target |
| 🟢 | round 3's white 4 answer holds — an escaped pipe or `&#124;` in the item refuses loudly, as a `Pact` row | `hooks/config.py:662` | confirmed | executed: `([], None, [one refusal naming Pact])` for both spellings at the target; no fix in the range touches that branch |
| carried | rounds 1–3's green verdicts: the pipe-less rows, the Cf strip, the refusal clause's pins, the indented-row answer, the vendored "may be `always`" line, the deliberate widening, the removed block-start exclusion, round 2's corpus and S14 | `hooks/config.py:660` | confirmed | carried from round 3's record and not re-derived, except where the seven-module run and the 646-file sweep re-executed them |
| ❓ | Whether the criterion should cover what github.com adds after cmark-gfm. An emoji shortcode between the words shows as an emoji there, which is the item by its letters, while the oracle shows the shortcode's letters | `tests/gfm_table_oracle.py` | ❓ out of verified scope | not executable here: github.com's rendering is not reachable from this round. The orchestrator answers it when it decides whether the oracle is cmark-gfm or github.com |

## Paste-ready fixes

```python
# hooks/config.py#shape_line, and the same hunk in
# skills/evidence-check/scripts/evidence_check.py#shape_line (S14 holds them
# equal). Replace the body from `kept, at = [], 0` through the return.
    kept, at = [], 0
    while (found := RAW_HTML.search(line, at)) is not None:
        cdata, instruction, declaration = found.groups()
        # A comment's closer may share the opener's dashes, so an empty
        # comment of four or five characters is whole (CommonMark 0.31, 6.6).
        if found.group(0).startswith("<!-"):
            closer, after = "-->", found.start() + 2
        else:
            closer = "]]>" if cdata else "?>" if instruction else None
            closer = ">" if declaration else closer
            after = found.end()
        if closer is not None:
            stop = line.find(closer, after)
            end = stop + len(closer) if stop != -1 else None
        else:
            name = re.match(
                r"[A-Za-z0-9-]*(?=[ \t\n\x0b\x0c\r/>])", line[found.end() :]
            )
            tail = name and TAG_END.match(line, found.end() + name.end())
            end = tail.end() if tail else None
        kept.append(line[at : found.end() if end is None else found.start()])
        at = found.end() if end is None else end
    kept.append(line[at:])
    # Only a reference GFM decodes, which ends in `;`: `html.unescape` also
    # reads HTML5's legacy names with none, so `&notify` became `¬ify`.
    shown = re.sub(
        r"&(?:#[0-9]{1,7}|#[xX][0-9A-Fa-f]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});",
        lambda m: html.unescape(m.group(0)),
        "".join(kept),
    )
    shown = "".join(ch for ch in shown if unicodedata.category(ch) != "Cf")
    # A destination or title this cannot parse still goes, to the last `)`
    # in its cell, so a link errs toward refusing, never toward silence.
    quoted = r'"(?:[^"\\]|\\.)*"' + r"|'(?:[^'\\]|\\.)*'"
    title = (
        r"\((?:[^()\"'<\\]|\\.|<(?:[^<>\\]|\\.)*>|"
        + quoted
        + r"|\([^()]*\))*\)|\((?:[^|\\]|\\.)*\)"
    )
    alt = r"!\[(?:[^\[\]\\]|\\.|\[(?:[^\[\]\\]|\\.)*\])*\]"
    shown = re.sub(alt + "(?:" + title + ")", "", shown)
    shown = re.sub(r"\](?:" + title + r")|\]\[[^\]]*\]|[\[\]]", "", shown)
    return re.sub(r"(?<=\S)[*_~]+|[*_~]+(?=\S)", "", shown)
```
```python
# hooks/config.py#stray_pact_rows: replace the comment's last line and the
# loop header `for index, _item, _value in rows:`
    # rows are read with their backticks removed. The live table is the run
    # of lines around them that GFM keeps in it until a blank line or a gap:
    # a row with no outer pipe, indented, or with a third cell is still
    # one of its rows though the walk does not take it (round 4 of PR #784).
    live = {index for index, _item, _value in rows}
    for index in sorted(live):
        for step in (1, -1):
            at = index + step
            while at in shown and shown[at].strip() and at not in live:
                live.add(at)
                at += step
    for index in sorted(live):
        line = shape_line(shown[index]).replace("`", "")
```
```python
# tests/test_a_signatory_declares_its_pact.py — WRAPS["a link"]: append
        "[{}](it's)",
        '[{}](a"b)',
        "[{}](a(b(c)))",
        "[{}](a\\)b)",
        "[{}](<a)b>)",
        '[{}](x "a\\"b")',
# WRAPS["an image"]: becomes
    "an image": ["![{}]()", '![{}](x "t")', "![a [b] c](x){}", "![a\\]b](x){}"],
# WRAPS["raw HTML"]: insert after the comment member holding the item
# (\x3c is "<", written so the opener never appears literally here)
        "\x3c!-->{}\x3c!-- -->",
        "\x3c!--->{}\x3c!-- -->",
# SPLITS: insert after "Pact `notify`",
    "Pact&notify",
    "Pact &notify",
    "Pact&nbsp notify",

# test_s3_a_pact_item_in_a_code_span_is_refused_on_the_walks_rows — append
# to the parametrize list
        ("`Pact notify` | always |", "Pact notify"),
        ("`Pact notify` | always", "Pact notify"),
        ("| `Pact notify` | always", "Pact notify"),
        (" | `Pact notify` | always |", "Pact notify"),
        ("| `Pact notify` | always | x |", "Pact notify"),
# to its ids
        "a live-table row with no leading pipe",
        "a live-table row with no pipe at either end",
        "a live-table row with no trailing pipe",
        "an indented live-table row",
        "a live-table row with a third cell",
# and its last assertion compares the stripped line, as the sentence does
        [refused_as(row.strip(), item)],


# tests/test_a_signatory_records_a_pact_change.py —
# test_s9_a_notify_row_below_the_table_leaves_a_row_citing_no_clause: append
        ("| [Pact notify](it's) | always |\n", "| [Pact notify](it's) | always |"),
        (
            "| \x3c!-->Pact notify\x3c!-- --> | always |\n",
            "| \x3c!-->Pact notify\x3c!-- --> | always |",
        ),
        ("| Pact&notify | always |\n", "| Pact&notify | always |"),
        ("`Pact notify` | always |\n", "`Pact notify` | always |"),
        ("| `Pact notify` | always | x |\n", "| `Pact notify` | always | x |"),
# to its ids
        "a link whose destination holds an apostrophe, in the table",
        "an empty comment before the item, in the table",
        "an ampersand GFM shows as itself, in the table",
        "a code span on a pipe-less row of the live table",
        "a code span on a three-cell row of the live table",

# test_a_vendored_copy_leaves_where_the_plugin_refuses_a_stray_notify: append
        "| [Pact notify](it's) | always |\n",
        "| \x3c!-->Pact notify\x3c!-- --> | always |\n",
        "| Pact&notify | always |\n",
# to its ids
        "as a link whose destination holds an apostrophe",
        "with an empty comment before the item",
        "with an ampersand GFM shows as itself",
```

## Executed probes

| What was run | Result |
|---|---|
| 1. 22 spellings in the live table at the target, at 180d22b2 and at 94d7b2e0: `pact_declaration`, and cmark-gfm's rendered cell reduced to its letters and digits | target: 19 silent where cmark-gfm shows the item (findings 1–4), 3 refused correctly. 180d22b2: 4 of the link spellings refused there and are silent at the target. 94d7b2e0: all 22 silent |
| 2. Every tracked `.md` file (646), `pact_declaration` and the lines `shape_line` plus `PACT_ROW_SHAPE` match, under the target, 180d22b2 and 94d7b2e0 | 0 declarations differ; 0 shaped lines differ between 180d22b2 and the target; 0 files refuse at the target |
| 3. Both copies of `shape_line` on six probe spellings | equal output; `NOTIFY_ROW_SHAPE` matches none of them |
| 4. The planted rows against the target code, the two pact modules | 36 failed (exactly the new rows), 718 passed |
| 5. The planted writer and vendored rows at the target, read one by one | all 8 fail on `assert code == 1`: exit 0, re-stamp `57f678c6 -> 7069baf7` |
| 6. The fences applied: the seven touched modules (the six pact modules and `tests/test_every_reader_ends_a_line_where_gfm_does.py`) | 1009 passed. The first try left the angle-bracket destination silent and had a test-expectation slip on the indented row; both were corrected before this run |
| 7. With the fences: probe 1 again, and the 646-file sweep | 0 misses either way; 0 declarations or shaped lines differ from the target |
| 8. ruff check and ruff format --check on the four fenced files | clean |
| 9. `letters` changed to `isalpha` at the target, the oracle test | 66 failed, 208 passed |
| 10. The notify item with a backslash-escaped pipe, and with `&#124;`, between the words, with no `Pact` row, at the target | each refused as a `Pact` row, `notify` None |
| 11. The full suite, the repository-wide lint and the typecheck | not yet — the sealer's single run after the rounds settle; nothing in this round stands in for it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/config.py:657` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/config.py:906` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/config.py:888` | round 1's ⬜ 3 — answered |
| round-1 | `hooks/config.py:851` | round 1's ⬜ 4 — answered |
| round-1 | `hooks/config.py:911` | round 1's ⬜ 5 — fixed |
| round-1 | `tests/test_a_signatory_declares_its_pact.py` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/plan.md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:858` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3836` | round 1's 🟢 — confirmed |
| round-2 | `hooks/config.py:663` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/config.py:819` | round 2's 🟡 2 — fixed |
| round-2 | `hooks/config.py:664` | round 2's ⬜ 3 — fixed |
| round-2 | `hooks/config.py:660` | round 2's 🟢 — confirmed |
| round-2 | `hooks/config.py:938` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/spec.md:64` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3866` | round 2's 🟢 — confirmed |
| round-3 | `hooks/config.py:929` | round 3's 🟡 1 — fixed |
| round-3 | `hooks/config.py:690` | round 3's 🟡 2 — fixed |
| round-3 | `tests/test_a_signatory_declares_its_pact.py:408` | round 3's ⬜ 3 — fixed |
| round-3 | `hooks/config.py:951` | round 3's ⬜ 4 — answered |
| round-3 | `tests/test_a_signatory_declares_its_pact.py:413` | round 3's 🟢 — confirmed |
| round-3 | `hooks/config.py:667` | round 3's 🟢 — confirmed |
| round-3 | `hooks/config.py:661` | round 3's 🟢 — confirmed |
| round-3 | `docs/the-pact.md:336` | round 3's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1–4 of this round | not placed by this round: the run is capped, so the orchestrator places each one, or rules it the branch's under `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped* — 🟡 1–3 sit in `shape_line` (round 1's unit, and 🟡 1 is round 3's own line), 🟡 4 in `stray_pact_rows` (the build's) | the orchestrator of this run, which decides the home; the smith of #759 if it rules them this branch's |
