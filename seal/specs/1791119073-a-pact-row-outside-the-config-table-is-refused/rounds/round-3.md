# 1791119073-a-pact-row-outside-the-config-table-is-refused — review round 3

| Field | Value |
|---|---|
| Target SHA | 168b0c9ba6374cf7991e9ac73e1229b061541a8f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #784 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a backtick anywhere in an item on the live table's own rows) and 🟡 2 (raw HTML other than a tag or comment, a quoted `>`, a titled link, and a Unicode space after a marker character), each still read as the default with no refusal |
| Loses a record or crashes | yes — under 🟡 1 and 🟡 2, `evidence-check --reverify` re-stamps a moved row citing no clause under `always` and records no pact change; executed through the writer for `` `Pact` notify ``, `` **`Pact notify`** ``, `Pact<?x?>notify` and a link whose title holds `)`. All predate this branch |

- [ ] Pass

## What this round was asked

Round 3 of #759 (PR #784), the verifying round and the round cap, at 168b0c9b: open round 2's fixes (range 2f35e2f7..27af657e) and judge whether each closes its finding with no regression — the rendered-item normalization in both `shape_line` copies and its cmark-gfm-held corpus, the deliberate widening, the removed block-start exclusion, the code-span rule on the walk's own rows and the vendored copy's documented limit, and the corrected docstring.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Round 2's yellow 2 is closed only where the whole item is one code span: a backtick anywhere else in an item on the live table's own rows (`` `Pact` notify ``, `` **`Pact notify`** ``, a lone or `&#96;` backtick) is read as the default with no refusal, and `--reverify` re-stamps a moved row citing no clause unrecorded | `hooks/config.py:929` | open | executed: six spellings cmark-gfm shows as `Pact notify` in the live table are silent at 168b0c9b; the writer exited 0, re-stamped and wrote no `seal/pact-changes/` for two of them; the fence reads the walk's rows through the shape with backticks removed, all six refuse, the template's documentation table and the S7 rows stay silent, and no declaration in 644 files changes. The base read these the same way |
| 🟡 2 | Round 2's yellow 1 class has members its construction did not generate: CDATA, a processing instruction, a declaration, a tag whose quoted attribute holds `>`, and a link whose title holds `)` are kept by `shape_line`; and `-`, `*`, `#` or `+` followed by U+00A0 directly under the table is a GFM row the shape's `\s` passes by | `hooks/config.py:690` | open | executed: five corpus wraps and five marker lookalikes silent at 168b0c9b while cmark-gfm renders the item in the live table; the writer re-stamped unrecorded for `Pact<?x?>notify` and the titled link; `hooks/blocks.py#INLINE_HTML` already reads all five raw HTML forms. With the fence, ten corpus cases and the `STRAY_WAYS` row refuse, S14 holds both copies equal, and no tracked line is newly shaped or lost |
| ⬜ 3 | The oracle test's "not refused" branch never runs — none of the 45 corpus spellings renders as anything but the item — and `letters` drops digits, so `Pact 2 notify` counts as the item to the criterion | `tests/test_a_signatory_declares_its_pact.py:408` | open | executed: 0 of 45 negatives; with `letters` keeping digits and `Pact 2 notify` in `SPLITS`, the second branch runs and passes, and fails with `letters` reverted. No shipped behaviour is wrong |
| ⬜ 4 | An item with a pipe between the words, written as `&#124;` or backslash-escaped, one cell in GFM, is refused as a `Pact` row — the sentence names the wrong item, and a config with no pact is refused where S6 says such a notify row is ignored | `hooks/config.py:951` | open | executed: `([], None, [one refusal naming Pact])` with no `Pact` row anywhere; loud, and nobody types it on purpose |
| 🟢 | round 2's 45 corpus spellings, the writer and vendored rows, and the S14 equality hold | `tests/test_a_signatory_declares_its_pact.py:413` | confirmed | executed: the four pact modules at 168b0c9b plus the new rows ran 503 passed outside the 18 new rows |
| 🟢 | round 2's white 3 is closed — `shape_line`'s docstring names the thirteen marks that render and says which way each removal errs | `hooks/config.py:667` | confirmed | executed: the thirteen marks beside the item, 13 refused; read: every removal the docstring lists can only refuse, because the shape admits any non-word character between the letters |
| 🟢 | the deliberate widening (`Pact-notify`, `Pact.notify`, `(Pact)`) refuses where GFM shows the item, and moves no declaration | `hooks/config.py:661` | confirmed | executed: 644 tracked `.md` files, 4 newly shaped lines, all quoted examples in round 1's records, none lost; `pact_declaration` identical over all 644 between 2f35e2f7 and 168b0c9b |
| 🟢 | 3902a349's removed block-start exclusion guarded nothing, as its message says: an ASCII space or a tab after a marker keeps list items and headings out | `hooks/config.py:661` | confirmed | executed: `- ` and a dash and a tab render as a list and stay silent; the Unicode-space remainder is 🟡 2 |
| 🟢 | the vendored copy's documented code-span limit is accurate for an item that is one code span, and stated where a reader looks | `docs/the-pact.md:336` | confirmed | read: `test_a_vendored_copy_reads_no_code_spanned_item` and its S16 pin; the option was the orchestrator's in round 2 and is carried |
| carried | rounds 1 and 2's green verdicts on the pipe-less rows, the Cf strip over 170 characters, the refusal clause's four pins, the indented-row answer and the vendored "may be `always`" line | `hooks/config.py:660` | confirmed | carried from round 2's record, not re-derived; no fix in this range touches the pipe branch, the Cf strip or the clause |

## Paste-ready fixes

```python
# hooks/config.py — stray_pact_rows: replace the comment and the loop that
# begin "# A row the walk took whose item is a pact item in a code span"
    # A row the walk took whose item holds a backtick -- a code span, part of
    # one, or a backtick GFM shows as itself -- renders as the item without
    # it, and the walk reads it as neither (round 2 of PR #784, yellow 2;
    # round 3, yellow 1). The shape cannot read past a backtick, because the
    # template's `| Row | Value | Absent |` table names both items in code
    # spans; the walk never reads that table, so only its own rows are read
    # with their backticks removed.
    for index, _item, _value in rows:
        match = PACT_ROW_SHAPE.match(shape_line(shown[index]).replace("`", ""))
        if match and index not in taken:
            strays[index] = (_shaped_item(match), shown[index])
```
```markdown
docs/the-pact.md, line 91-93 — replace
  "An item in a code span is refused on the
   table's own rows only, because a documentation table names both items in
   code spans."
with
  "An item holding a backtick, in a code span or not, is refused on the
   table's own rows only, because a documentation table names both items in
   code spans."

docs/the-pact.md, line 336 — replace
  "one exception: it does not read an item in a code span, because it has no"
with
  "one exception: it does not read an item holding a backtick, a code span
   included, because it has no"
```
```python
# tests/test_a_signatory_declares_its_pact.py — S16's pin for docs/the-pact.md,
# the vendored-copy sentence: replace its last string piece
            "refuses a notify row it does not reach, with one exception: it does "
            "not read an item holding a backtick, a code span included",


# tests/test_a_signatory_declares_its_pact.py —
# test_s3_a_pact_item_in_a_code_span_is_refused_on_the_walks_rows: append to
# the parametrize list, after ("| `Pact` | https://example.com/org/other |", "Pact"),
        ("| `Pact` notify | always |", "Pact notify"),
        ("| **`Pact notify`** | always |", "Pact notify"),
        ("| `Pact notify`. | always |", "Pact notify"),
        ("| Pact notify` | always |", "Pact notify"),
        ("| &#96;Pact notify&#96; | always |", "Pact notify"),
# and replace its ids with
    ids=[
        "a code span",
        "padded",
        "a doubled space",
        "a code-spanned Pact",
        "part of the item",
        "in bold",
        "a mark after it",
        "a lone backtick",
        "a backtick reference",
    ],


# tests/test_a_signatory_records_a_pact_change.py —
# test_s9_a_notify_row_below_the_table_leaves_a_row_citing_no_clause: append
# to the parametrize list
        ("| `Pact` notify | always |\n", "| `Pact` notify | always |"),
# and to its ids
        "part of the item in a code span, in the table",
```
```python
# hooks/config.py — PACT_ROW_SHAPE, and skills/evidence-check/scripts/
# evidence_check.py — NOTIFY_ROW_SHAPE: the same one-place change in both, the
# pipe-less branch stops at a space or a tab, as GFM's list marker does
    r"[\s>]*(?:\|[^\w|`]*|[^\w|` \t]*)(P[^\w|`]*a[^\w|`]*c[^\w|`]*t(?:[^\w|`]*n[^\w|`]*o[^\w|`]*t[^\w|`]*i[^\w|`]*f[^\w|`]*y)?)[^\w|`]*\|\s*[^\s|]",


# hooks/config.py — shape_line, and the same lines in
# skills/evidence-check/scripts/evidence_check.py#shape_line: replace the
# first `shown = re.sub(...)` and the link `shown = re.sub(...)`
    shown = re.sub(
        r"<!-{2}.*?-{2}>|<!\[CDATA\[.*?\]\]>|<\?.*?\?>|<![A-Za-z][^>]*>"
        r"""|</?[A-Za-z][A-Za-z0-9-]*(?:\s(?:[^<>"']|"[^"]*"|'[^']*')*)?/?>""",
        "",
        line,
    )
    shown = html.unescape(shown)
    shown = "".join(ch for ch in shown if unicodedata.category(ch) != "Cf")
    shown = re.sub(
        r"""\]\((?:[^()"']|"[^"]*"|'[^']*'|\([^()]*\))*\)|\]\[[^\]]*\]|[\[\]]""",
        "",
        shown,
    )
    return re.sub(r"(?<=\S)[*_~]+|[*_~]+(?=\S)", "", shown)


# hooks/config.py — shape_line's docstring, first sentence after the summary:
# replace "Inline HTML tags and comments go," with
    Inline raw HTML goes -- a tag, a comment, CDATA, a processing
    instruction or a declaration (CommonMark 6.6), a quoted attribute value
    holding `>` included --
# and in evidence_check.py#shape_line's docstring replace "inline HTML gone"
# with "inline raw HTML gone, all five kinds"
```
```python
# tests/test_a_signatory_declares_its_pact.py — WRAPS: append after "({})",
    "<?x?>{}",
    "<![CDATA[]]>{}",
    "<!X y>{}",
    '<span title="a>b">{}</span>',
    '[{}](x "a)b")',


# tests/test_a_signatory_declares_its_pact.py — STRAY_WAYS: insert after the
# "W8 no leading pipe, punctuation before the item" entry
    (
        "W8 no leading pipe, a dash and a no-break space before the item",
        CONFIG + "-\u00a0Pact notify | always |\n",
        "-<U+00A0>Pact notify | always |",
    ),


# tests/test_a_signatory_records_a_pact_change.py —
# test_s9_a_notify_row_below_the_table_leaves_a_row_citing_no_clause: append
# to the parametrize list
        ("| Pact<?x?>notify | always |\n", "| Pact<?x?>notify | always |"),
# and to its ids
        "with a processing instruction, in the table",
```
```python
# tests/test_a_signatory_declares_its_pact.py
def letters(text):
    return "".join(ch for ch in text.lower() if ch.isalnum())


# SPLITS: append after "P&#97;ct notify",
    "Pact 2 notify",
```

## Executed probes

| What was run | Result |
|---|---|
| 1. 37 item spellings in the live table: the target reader's refusal and named item, the vendored copy's named set, and cmark-gfm's rendered cell reduced to its letters | 15 silent where GFM shows the item (six code-span, three backtick, three raw HTML, one quoted `>`, one link title, and `Pact 2 notify`, which is the criterion's artefact); 3 refused where GFM shows something else (image, undefined reference, `&nbsp` with no `;`); 2 refused under the wrong item (escaped and `&#124;` pipe) |
| 2. `MARKUP` spellings whose rendered cell is not the item | 0 of 45 |
| 3. `-`, `*`, `#`, `+` with U+00A0 and `-` with U+2003, then with a space and with a tab, directly under the table | the five Unicode-space lines render as rows of the live table and are silent; the space and tab lines render as a list and are silent |
| 4. The writer, `--reverify` under `always`, a moved row citing no clause, for `` `Pact` notify ``, `` **`Pact notify`** ``, `Pact<?x?>notify` and `[Pact notify](x "a)b")` | each exit 0, re-stamped, no `seal/pact-changes/` |
| 5. The notify row with a backslash-escaped pipe, and with `&#124;`, between the words, with no `Pact` row anywhere | each refused as a `Pact` row |
| 6. The thirteen prepended concatenation marks beside `Pact` | 13 refused |
| 7. The new test rows against 168b0c9b's code, the four pact modules | 18 failed (exactly the new rows), 503 passed |
| 8. The code fences applied, the four pact modules; probe 1 again | 521 passed; 0 silent where GFM shows the item, the three deliberate over-refusals remain |
| 9. With the fences, `letters` reverted to `isalpha`, the oracle test | 1 failed (`Pact 2 notify`), 55 passed |
| 10. Every line of the 644 tracked `.md` files and `pact_declaration` over each, under 2f35e2f7, 168b0c9b and the fenced reader | 4 lines newly shaped at 168b0c9b (quoted examples in round 1's records), 0 lost; 0 newly shaped or lost with the fences; 0 declarations differ either step |
| 11. ruff check and ruff format --check on the four files the fences touch | clean, once the test's U+00A0 is written as an escape, as the fence writes it |
| 12. The comment alternative spelled with `-{2}` against the target spelling, five inputs | identical output |
| 13. The full suite, the repository-wide lint and the typecheck | not yet — the sealer's single run after the rounds settle; nothing in this round stands in for it |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
