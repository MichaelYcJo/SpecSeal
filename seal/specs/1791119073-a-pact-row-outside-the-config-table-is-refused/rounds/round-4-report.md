# Round 4 review report — 1791119073-a-pact-row-outside-the-config-table-is-refused

- Target: PR #784 (draft), branch `fix/759-a-pact-row-outside-the-config-table-is-refused`, SHA 9501cbc4, base `release/v0.18.2` at 94d7b2e0
- Ran by: specseal:warden on claude-opus-5-5
- Round kind: the verifying round, and the last round of this run. Its target is round 3's fix range `180d22b2..92a6a90a`, not the branch. The units round 3's `New units` row names, `RAW_HTML` and `TAG_END`, were judged as code.
- Where: a `git clone --no-local` of the worktree at 9501cbc4, under `<scratchpad>/<work-item-id>/round-4/`. Nothing was written in the worktree except this file. The clone, the probe files, the extracted copies of `hooks/` at 180d22b2 and 94d7b2e0, and the patched readers were all deleted before handover. No worktree or branch was made. The clone's one stash entry lived in the clone's own repository and went with it.
- Earlier rounds: `round-1.md` to `round-3.md` and their reports. Their coordinates were carried. Every verdict below on what round 3's fixes touch was re-derived.

## Summary

Round 3's fixes hold for what they enumerated. All five raw-HTML kinds that the corpus generates are removed. An autolink is kept. A quoted `>` and a `)` inside a quoted title no longer end their construct early. GFM's whitespace set replaced `\s`. A code span anywhere in an item on the walk's own rows refuses. The two `shape_line` copies are equal, and `letters` now keeps digits so the must-not branch runs. No declaration and no shaped line changed in any of the 646 tracked `.md` files between 180d22b2 and the target.

The construct axis list is still not complete, and one of round 3's own changes went backwards:

1. **🟡 1 — round 3's link change made four spellings silent that 180d22b2 refused.** The new title pattern parses a destination or title strictly. When it cannot parse one, the code falls back to removing only the brackets and leaves the destination in place, so its letters follow the item and the shape no longer matches. The four spellings are a destination holding an apostrophe (`[Pact notify](it's)`), a destination holding a double quote, two levels of parentheses, and a title holding an escaped quote. Three more members of the same cause were already silent at 180d22b2: an escaped `)` in the destination, an angle-bracket destination holding `)`, and an image whose alt text holds brackets.
2. **🟡 2 — an empty comment hides the item from the shape.** `&lt;!-->` and `&lt;!--->` are whole comments in the pinned cmark-gfm (CommonMark 0.31). `shape_line` looks for the closer only after the four-character opener, so it removes everything up to the next comment's closer, the item included.
3. **🟡 3 — `html.unescape` decodes references GFM shows as text.** It follows HTML5's legacy rule, which decodes names such as `&not` with no `;`. So `Pact&notify` becomes `Pact¬ify` and is silent, while cmark-gfm shows `Pact&notify`, which is the item by its letters.
4. **🟡 4 — round 3's yellow 1 is closed on the walk's rows, and the live table has more rows than the walk.** A row GFM keeps in the live table but `CONFIG_ROW` does not take still reads as the default when its item holds a backtick. Five such rows were tested: no leading pipe, no pipe at either end, no trailing pipe, one space of indentation, and a third cell. The same rows without the backtick already refuse.

All four lose the record #759 exists to keep. I ran the writer at the target on five spellings, one or more from each finding. Each time `evidence-check --reverify` exited 0, re-stamped `src/orders.py#serialize 57f678c6 -> 7069baf7` under `always`, and recorded no pact change. The vendored copy did the same for the three spellings from findings 1–3.

The fences below close all four with no new unit. With them applied, the seven touched modules pass (1009), the probe set has no miss in either direction, and the 646-file sweep shows no change in any declaration or shaped line.

A ❓ row asks about one axis outside the oracle's reach: what github.com adds after cmark-gfm, which is emoji shortcodes.

## The fixes, verified (stage 1)

### Round 3's yellow 2 — raw HTML through the tree's reader (3ed2649f, 1d75e86b)

Claimed: `RAW_HTML` is the comment opener plus `hooks/blocks.py#INLINE_HTML`, and `TAG_END` is `blocks.TAG_END`. Found: `hooks/config.py#RAW_HTML` at `hooks/config.py:673` is built from `blocks.INLINE_HTML.pattern` (`hooks/blocks.py:208`), and `TAG_END` is the same object as `hooks/blocks.py:210`. The vendored copies at `skills/evidence-check/scripts/evidence_check.py:3757-3758` are equal as text, and S14 asserts that equality.

The loop at `hooks/config.py:702-719` handles the four kinds with closers correctly. For a tag, the lookahead after the name needs whitespace, `/` or `>`. So `<https://…>` and `<a@…>` are kept: the name `https` is followed by `:`, so `re.match` returns None, `tail` is None, and the text stays. An opener with no closer is kept and scanning resumes after it, which is the reading GFM gives.

A tag is removed even when CommonMark would show it as text (`<a/b>`, `</b x>`, `<x =>`). Shown as text, each of these holds letters from its own name, so it cannot be the item, and removing it can only cause a refusal. That is the loud direction.

The gap is the comment branch, which is 🟡 2.

Claimed: images go whole and a link title may hold `)`. Found: true for the members the corpus generates. The new strict pattern then lost four members the old one refused, which is 🟡 1.

Claimed: GFM's whitespace set replaces `\s` in both shapes. Found: true at `hooks/config.py:662` and `evidence_check.py:3751`. A value cell holding only U+00A0 is now shaped as a value. That only adds refusals, it is loud, and no tracked file has one: the sweep shaped no new line.

### Round 3's yellow 1 — a backtick on the walk's rows (3ed2649f, c61ffc5b)

Claimed: every row the walk took is read through the shape with its backticks removed, the documentation tables stay silent, and the vendored limit covers any backtick. Found: the loop at `hooks/config.py:963-967` does that. S7's two guards and the shipped-configs case pass. `docs/the-pact.md:336` names the vendored limit as "an item holding a backtick, a code span included", and its pin matches.

But the walk's rows are `CONFIG_ROW` matches (`hooks/config.py:99`), which need a leading pipe at column 0, two cells and a trailing pipe. GFM's live table has more rows than that, so round 3's finding ("on the live table's own rows") is closed only in part. That is 🟡 4.

### Round 3's white 3 — `letters` keeps digits (3ed2649f, 92a6a90a)

Executed: with `letters` changed back to `isalpha`, the oracle test fails 66 cases at the target. Every one is a non-pact spelling in the must-not direction, such as `Pact notify 2` and `Pact 2 notify` under each construct. So that branch runs, and it fails when it should.

### Round 3's white 4 — answered

Executed at the target: `Pact\|notify` and `Pact&#124;notify`, with no `Pact` row anywhere, each give `([], None, [one refusal naming Pact])`. The answer's grounds hold. The refusal is loud, it quotes the line as written, and no fix in the range touches the pipe branch.

## Findings (stage 2)

### 🟡 1. A link destination or title the new pattern cannot parse leaves the destination behind, so the row is silent — four of these refused at 180d22b2

`hooks/config.py:724` and `skills/evidence-check/scripts/evidence_check.py:3790`, in `shape_line`, a unit round 1's fixes created. Round 3's fix wrote the line.

**What is wrong.** At 180d22b2 the pattern was `\]\([^)]*\)`. It removed `](` up to the first `)`, so whatever was left after the item was punctuation, and the shape admits punctuation. The new `title` pattern only allows `'` or `"` as the start of a matched quoted string, and only one level of nesting. When it fails, the `[\[\]]` branch removes the brackets alone. The destination text, `(it's)`, stays after `notify`, and its letters stop the shape.

Executed with cmark-gfm 2025.10.22, the version the suite pins:

| Spelling | cmark-gfm shows | 180d22b2 | target |
|---|---|---|---|
| `[Pact notify](it's)` | `Pact notify` | refused | silent |
| `[Pact notify](a"b)` | `Pact notify` | refused | silent |
| `[Pact notify](a(b(c)))` | `Pact notify` | refused | silent |
| `[Pact notify](x "a\"b")` | `Pact notify` | refused | silent |
| `[Pact notify](a\)b)` | `Pact notify` | silent | silent |
| `[Pact notify](<a)b>)` | `Pact notify` | silent | silent |
| `![a [b] c](x)Pact notify` | `Pact notify` | silent | silent |

**Why it matters.** Executed: the writer under `always` with `[Pact notify](it's)` exits 0, re-stamps the moved row citing no clause, and records no pact change. The vendored copy does the same. A URL with an apostrophe in it is the most ordinary of these spellings.

**The fix.** Parse the destination properly first: an angle-bracket destination, backslash escapes, and quotes with escapes. Where that still fails, remove everything up to the last `)` in the cell. That way a link errs toward a refusal and never toward silence. The image alt text gets one level of brackets and escapes. With the fix applied, all seven spellings refuse in both copies, and the must-not spellings in the corpus stay silent.

### 🟡 2. An empty comment hides the item: `&lt;!-->Pact notify&lt;!-- -->` is silent

`hooks/config.py:706-711` and `evidence_check.py:3772-3777`, in `shape_line`.

**What is wrong.** The pinned cmark-gfm follows CommonMark 0.31, where `&lt;!-->` and `&lt;!--->` are whole comments. Executed: `Pact&lt;!-- a -- b -->notify` renders as `Pactnotify`, so the renderer uses the 0.31 rules. `shape_line` searches for `-->` from `found.end()`, which is after the opener's two dashes. For `&lt;!-->` it finds the next comment's closer and removes everything in between, the item included. 180d22b2's regex had the same blind spot, so this predates round 3. Round 3 put the raw-HTML axis's edge cases in scope, and the corpus has no empty comment.

**Why it matters.** Executed: the writer re-stamps unrecorded for `&lt;!-->Pact notify&lt;!-- -->`, and so does the vendored copy.

**The fix.** Search for the closer from `found.start() + 2`, so the closer may share the opener's dashes. Executed: `&lt;!-->`, `&lt;!--->` and the ordinary comments all read correctly.

### 🟡 3. A bare `&` before a legacy entity name is decoded, so `Pact&notify` is silent

`hooks/config.py:722` and `evidence_check.py:3788`, in `shape_line`.

**What is wrong.** `html.unescape` applies HTML5's rule for legacy names, which decodes `&not`, `&amp`, `&nbsp` and about a hundred others when they have no `;`. CommonMark decodes a reference only when it ends in `;`. So `Pact&notify` and `Pact &notify` become `Pact¬ify`, and the shape misses them. cmark-gfm shows `Pact&notify`, which is the item by its letters. The same rule caused the over-refusal of `&nbsp notify` that round 3 recorded. That was the loud direction, and the fix ends it as well.

**Why it matters.** Executed: the writer re-stamps unrecorded for `Pact&notify`, and so does the vendored copy. This one predates round 3, and the corpus's entity axis has no member of it.

**The fix.** Decode only what CommonMark decodes: `&` followed by a name, `#digits` or `#x hex`, then `;`. Pass each match through `html.unescape`.

### 🟡 4. A backtick in the item of a live-table row the walk does not take is silent

`hooks/config.py:963`, in `stray_pact_rows`, a unit the build created (depth 0).

**What is wrong.** Round 3's yellow 1 named the class as "a backtick anywhere in an item on the live table's own rows". The fix reads `rows`, which holds the `CONFIG_ROW` matches. GFM keeps more lines in the live table than that: one with no leading pipe, one with no trailing pipe, one indented up to three spaces, and one with a third cell, until the first blank line. The general loop reads those lines with backticks intact, and the shape refuses a backtick there by design.

Each of these rows, written directly under the live table, renders in it as `Pact notify` and is silent at the target:

- `` `Pact notify` | always | `` (no leading pipe)
- `` `Pact notify` | always `` (no pipe at either end)
- `` | `Pact notify` | always `` (no trailing pipe)
- `` | `Pact notify` | always | `` indented one space
- `` | `Pact notify` | always | x | `` (a third cell)

The same five rows without the backtick refuse at the target.

**Why it matters.** Executed: the writer re-stamps unrecorded for the pipe-less row and for the three-cell row. The documentation tables are not affected. Their rows are separated from the live table by a blank line or a heading, and S7's "outside the walk's table" guard sits under a blank line.

**The fix.** Read with backticks removed every non-blank line that is contiguous with a walk row, in both directions, through `shown`. A gap left by `unfenced` ends the run, as it ends the table in `gfm_table`. Executed: all five rows refuse, S7 stays silent, and the 646-file sweep shows no change.

## The questions this round was asked

**Is the construct axis list complete for what a person reads as `Pact notify` in a rendered GFM cell?** No. Each axis was enumerated by example, and each of findings 1–3 is an axis member the examples did not reach: link destination punctuation, an image alt holding brackets, an empty comment, and a reference with no `;`. Those are the gaps within cmark-gfm. github.com also renders emoji shortcodes after cmark-gfm, which the oracle cannot see. The ❓ row asks about that.

**Does anything in a tracked config-shaped file or prose line now change declaration?** No. Executed: `pact_declaration` over all 646 tracked `.md` files is identical at 94d7b2e0, 180d22b2 and the target. No file refuses at the target. The lines `PACT_ROW_SHAPE` matches through `shape_line` are identical at 180d22b2 and the target. With the four fences applied, both comparisons are still identical.

## Regression tests to plant

- `tests/test_a_signatory_declares_its_pact.py`: `WRAPS["a link"]` gains six members, `WRAPS["an image"]` two, and `WRAPS["raw HTML"]` two. `SPLITS` gains `Pact&notify`, `Pact &notify` and `Pact&nbsp notify`. `test_s3_a_pact_item_in_a_code_span_is_refused_on_the_walks_rows` gains the five live-table rows and compares against `row.strip()`, because the refusal sentence strips the line. All are in the fences below.
- `tests/test_a_signatory_records_a_pact_change.py`: `test_s9_a_notify_row_below_the_table_leaves_a_row_citing_no_clause` gains five rows. `test_a_vendored_copy_leaves_where_the_plugin_refuses_a_stray_notify` gains three.
- Seen red (§15): at the target, these rows give 36 failed and 718 passed across the two modules. Every one of the eight writer and vendored rows fails on `assert code == 1` with exit 0 and the re-stamp line. With the fences applied, all pass.

## Facts for the evidence ledger

- If the fences land, `hooks/config.py#shape_line`, `skills/evidence-check/scripts/evidence_check.py#shape_line` and `hooks/config.py#stray_pact_rows` change content, so any ledger row anchored on them needs re-verifying and re-stamping. I did not open this branch's ledger fragment for those anchors.
- The pinned cmark-gfm (2025.10.22) uses CommonMark 0.31's comment rule. `Pact&lt;!-- a -- b -->notify` renders as `Pactnotify`, and `&lt;!-->` is a whole comment. Executed through `tests/gfm_table_oracle.py`.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1–4 of this round | not placed by this round: the run is capped, so the orchestrator places each one, or rules it the branch's under `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped* — 🟡 1–3 sit in `shape_line` (round 1's unit, and 🟡 1 is round 3's own line), 🟡 4 in `stray_pact_rows` (the build's) | the orchestrator of this run, which decides the home; the smith of #759 if it rules them this branch's |

## Paste-ready fixes

### 🟡 1, 🟡 2, 🟡 3 — `shape_line`, both copies

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

### 🟡 4 — `stray_pact_rows`

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

### The cases, all four

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

Needs a fix: yes — 🟡 1 (a link destination or title the new pattern cannot parse; four spellings regressed from 180d22b2), 🟡 2 (an empty comment), 🟡 3 (a reference with no `;`), 🟡 4 (a backtick on a live-table row the walk does not take)
Loses a record or crashes: yes — under each of 🟡 1–4, `evidence-check --reverify` exits 0 and re-stamps a moved row citing no clause under `always` with no pact change recorded; executed through the writer for `[Pact notify](it's)`, `&lt;!-->Pact notify&lt;!-- -->`, `Pact&notify`, a pipe-less code-span row and a three-cell code-span row, and through the vendored copy for the first three

## Proof block

Files opened this round, at 9501cbc4 unless named:

- `hooks/config.py` — lines 640-760 (`PACT_ROW_SHAPE`, `RAW_HTML`, `TAG_END`, `shape_line`), 800-1010 (`pact_declaration`, `stray_pact_rows`, `_letters`), 74-102 (`CONFIG_HEADER`, `CONFIG_ROW`), `indexed_config_rows`, the head of `gfm_table`; and the fix-range diff `180d22b2..92a6a90a`
- `hooks/blocks.py` — lines 208-210
- `skills/evidence-check/scripts/evidence_check.py` — the fix-range diff (`NOTIFY_ROW_SHAPE`, `RAW_HTML`, `TAG_END`, `shape_line`)
- `docs/the-pact.md` — the fix-range diff
- `tests/test_a_signatory_declares_its_pact.py` — the fix-range diff, lines 180-210 and 455-560
- `tests/test_a_signatory_records_a_pact_change.py` — the fix-range diff, lines 945-1010 and 1555-1612
- `tests/gfm_table_oracle.py` — lines 1-80
- `tests/conftest.py` — `load_hook_module`
- `bin/test`, `.github/scripts/run_tests.py` — the runner and the `CMARKGFM` pin
- `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/rounds/round-3.md` — whole; `round-3-report.md` — the head; `round-1.md` and `round-2.md` — their `New units` rows
- `docs/review-chain-spec.md` — §*The reopening — one, and then the run is capped*
- `seal/config.md` — no `Record language` row, so this report is in English
