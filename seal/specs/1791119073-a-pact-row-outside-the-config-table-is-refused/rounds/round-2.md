# 1791119073-a-pact-row-outside-the-config-table-is-refused — review round 2

| Field | Value |
|---|---|
| Target SHA | 425b62984c6d5779a4acb52cf1cf20111c86116a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #784 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `2f35e2f73eb404d7851539ae05574a34b871653c..27af657e3dfa98ecf24fdfb28785887ba8f90e25`, 6 commits |
| Contract changes | stray_pact_rows → pact_declaration, round-2-report.md, round-2.md |
| New units | _letters (depth 1); PACT_ITEMS (depth 1); WRAPS (depth 1); JOINS (depth 1); SPLITS (depth 1); MARKUP (depth 1); rendered_item (depth 1); letters (depth 1); test_s3_an_item_is_refused_exactly_where_gfm_shows_a_pact_item (depth 1); test_s3_a_pact_item_in_a_code_span_is_refused_on_the_walks_rows (depth 1); test_s7_a_code_spanned_item_off_the_walks_rows_or_empty_is_not_refused (depth 1); test_a_vendored_copy_reads_no_code_spanned_item (depth 1) |
| Needs a fix | yes — 🟡 1 (markup or a character reference around the item) and 🟡 2 (an item in a code span), both still read as the default with no refusal |
| Loses a record or crashes | yes — under 🟡 1 and 🟡 2, `evidence-check --reverify` re-stamps a moved row citing no clause under `always` and records no pact change (executed through the writer for a code span, bold, and `&#32;`). Both predate this branch. |

- [x] Pass

## What this round was asked

Round 2 of #759 (PR #784), the verifying round, at 425b6298: open round 1's fixes (range 8e63ea91..fc07acdd) and judge whether each closes its finding with no regression — the optional leading pipe in both shapes, the Cf strip in both readers enumerated over every Cf character, the refusal sentence's new clause and its pins — and the two answered whites' grounds.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An item spelled with emphasis, strikethrough, a link, inline HTML or a character reference (`**Pact notify**`, `Pact&#32;notify`) in the live table renders as the item, and is read as the default with no refusal; `--reverify` re-stamps a moved row citing no clause unrecorded | `hooks/config.py:663` | **fixed** `329f8ff7` | fixed at 329f8ff7 — 3902a349 — both `shape_line` copies now read a line as GFM shows it: inline HTML tags and comments removed, character references decoded, Cf removed, a link's text kept, emphasis and strikethrough delimiters removed. A run of `*`, `_` or `~` standing between spaces is kept as a list marker. Both shapes read the item by its letters alone (`P…a…c…t(…n…o…t…i…f…y)`, any run of non-word characters but a pipe or a backtick between the letters). The class is held by `test_s3_an_item_is_refused_exactly_where_gfm_shows_a_pact_item`, over a corpus generated from 14 wraps × 2 items, 11 joins and 6 split spellings. It is held to cmark-gfm's rendered cell through `tests/gfm_table_oracle.py`, in both directions: refused exactly where the rendered item reduces to `pact` or `pactnotify`. 43 corpus spellings were red at 425b6298. The writer and vendored rows (bold, a character reference, a link, a hyphen) were red against 425b6298's readers. S14 now holds the two `shape_line` copies equal over the corpus. Guards were added for list markers, a heading, an escaped pipe and another item; the S7 block-start exclusions were dropped at 3902a349 because they guarded nothing and blocked `-Pact \| x`. No declaration changed across the 24 tracked config-shaped files. G1–G13 were red under `mutation-check`; executed: eleven spellings silent at base and target, vendored not blind; cmark-gfm renders them as `Pact notify` in the live table; the writer re-stamped under `always` with no `seal/pact-changes/`. Same class and same reasoning as round 1's yellow 2, whose fix enumerated Cf only. The fence for both copies passes every guard and the four pact modules |
| 🟡 2 | An item in a code span (`` `Pact notify` ``, `` `Pact` ``) in the live table is read as the default with no refusal; `--reverify` re-stamps unrecorded | `hooks/config.py:819` | **fixed** `329f8ff7` | fixed at 329f8ff7 — `stray_pact_rows` refuses a row the walk itself took whose item is a pact item in a code span with a value. An empty value, and a code span outside the walk's table, stay silent (S7 rows). The template, `seal/config.md` and `skills/config/SKILL.md` are not refused, and a case holds all three. The four code-span cases were red at 425b6298. For the vendored copy (option b), `test_a_vendored_copy_reads_no_code_spanned_item` states the one exception, and the leaves-where case's docstring points to it. `docs/the-pact.md` names the limit at 79ad70f7. Both sentences are pinned in S16, and deleting either turns S16 red; executed: reader silent at base and target, cmark-gfm renders `<code>Pact notify</code>` in the live table, the writer re-stamped with no record. Not fixable in the shape: `templates/config.md:396`–`:397` and `skills/config/SKILL.md:47`–`:48` become pact-shaped. The fence refuses only the walk's own rows. The vendored half is a choice, and the orchestrator of this run answers it |
| ⬜ 3 | `shape_line`'s docstring says GFM renders no Cf character, and thirteen (the prepended concatenation marks) render as a glyph | `hooks/config.py:664` | **fixed** `329f8ff7` | fixed at 329f8ff7 — `shape_line`'s docstring no longer says GFM renders no Cf character. It names the thirteen prepended concatenation marks that render as a glyph, and says that removing them, like removing a backslash-escaped or unmatched delimiter, refuses a row and never reads one as the default; executed: `\| Pact<U+06DD> \| x \|` and the other twelve are refused as `Pact`. The behaviour is loud and right, and the sentence is wrong. Closed by 🟡 1's docstring |
| 🟢 | round 1's yellow 1 is closed — a pact row with no leading pipe directly under the table is refused in both readers | `hooks/config.py:660` | confirmed | executed: nine pipe-less rows refused; 50 must-not placements silent; one newly shaped line across 641 tracked `.md` files (a quoted example), no lost line, no declaration change across 23 config-shaped files; with the pipe required again, exactly the four new cases fail |
| 🟢 | round 1's yellow 2 is closed — a Cf character in or around the item is removed before the shape, in both readers alike, and shown as its code point | `hooks/config.py:663` | confirmed | executed: both `shape_line` copies equal over all 170 Cf characters; plugin refuses ⇒ vendored blind over 510 inputs; with `shape_line` as identity all 170 S3 cases fail. Its class is wider, which is this round's findings 1 and 2 |
| 🟢 | round 1's white 5 is closed — the refusal names the row's own shape, in all four pins | `hooks/config.py:938` | confirmed | executed: the clause removed with the identity `shape_line`, 209 failed, every sentence pin among them; read: the old wording survives only in `spec.md`'s quoted draft (recorded divergence) and round 1's report |
| 🟢 | round 1's white 3 answer holds — an indented row is refused by the spec's choice | `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/spec.md:64` | confirmed | read: `spec.md:64` "any indentation", `templates/config.md:419` |
| 🟢 | round 1's white 4 answer holds — the vendored "may be `always`" line predates the branch | `skills/evidence-check/scripts/evidence_check.py:3866` | confirmed | read: present at 94d7b2e0 lines 3850 and 3879, introduced by d671a43 (#756), unchanged by this branch |
| carried | round 1's green verdicts on the base-red cases and on fa4ddfe1's file list | `tests/test_a_signatory_declares_its_pact.py` | confirmed | carried from round 1, not re-derived; no fix touches either |

## Paste-ready fixes

```python
# hooks/config.py, at the imports, sorted (before `import os`)
import html


# hooks/config.py — shape_line, replacing the whole function
def shape_line(line):
    """LINE as `PACT_ROW_SHAPE` reads it: the item as GFM shows it. A
    character reference becomes its character, every format character
    (Unicode category Cf) is removed, and emphasis, strikethrough, link and
    inline-HTML markup against `Pact` or `notify` is removed, because a
    person reading the rendered row sees the item without any of them
    (round 1 of PR #784, yellow 2; round 2, yellow 1). Thirteen Cf
    characters -- the prepended concatenation marks U+0600-U+0605, U+06DD,
    U+070F, U+0890, U+0891, U+08E2, U+110BD and U+110CD -- render as a
    glyph; removing them refuses a row that shows one, the loud direction.
    A code span is not removed here, because the template's
    `| Row | Value | Absent |` table names both items in one;
    `pact_declaration` reads a code span on the walk's own rows instead.
    `evidence_check.py#shape_line` is its copy, held equal by
    `tests/test_a_signatory_declares_its_pact.py`."""
    shown = html.unescape(line)
    shown = "".join(ch for ch in shown if unicodedata.category(ch) != "Cf")
    return re.sub(
        r"[*_~\[]+(?=pact|notify)"
        r"|(?:(?<=pact)|(?<=notify))(?:[*_~]+|\]\([^)]*\))+"
        r"|<[^<>:@|]*>",
        "",
        shown,
        flags=re.I,
    )
```
```python
# skills/evidence-check/scripts/evidence_check.py — shape_line, replacing
# the whole function (`html` and `re` are already imported there)
def shape_line(line):
    """`hooks/config.py#shape_line`, copied for a copy with no `hooks/`:
    LINE as GFM shows the item -- character references decoded, format
    characters (Unicode category Cf) removed, and emphasis, strikethrough,
    link and inline-HTML markup against `Pact` or `notify` removed (round 1
    of PR #784, yellow 2; round 2, yellow 1)."""
    shown = html.unescape(line)
    shown = "".join(ch for ch in shown if unicodedata.category(ch) != "Cf")
    return re.sub(
        r"[*_~\[]+(?=pact|notify)"
        r"|(?:(?<=pact)|(?<=notify))(?:[*_~]+|\]\([^)]*\))+"
        r"|<[^<>:@|]*>",
        "",
        shown,
        flags=re.I,
    )
```
```python
# tests/test_a_signatory_declares_its_pact.py — beside the S3 cases
@pytest.mark.parametrize(
    "item",
    [
        "**Pact notify**",
        "*Pact notify*",
        "__Pact notify__",
        "~~Pact notify~~",
        "*Pact* *notify*",
        "[Pact notify]()",
        "<b>Pact</b> notify",
        "Pact&#32;notify",
        "Pact&nbsp;notify",
        "Pact&#x200B;notify",
    ],
)
def test_s3_a_notify_row_spelled_with_markup_is_refused(item):
    """Round 2 of PR #784, yellow 1. GFM renders each as `Pact notify`, so
    the row is read without its markup, as a format character is."""
    row = f"| {item} | always |"
    assert config.pact_declaration(CONFIG + row + "\n")[1:] == (
        None,
        [refused_as(row)],
    ), row


# tests/test_a_signatory_declares_its_pact.py — in S14, after the Cf loop
    for line in ("| **Pact notify** | x |", "| Pact&#32;notify | x |",
                 "| [Pact]() | x |", "| <b>Pact</b> notify | x |"):
        assert config.shape_line(line) == ec.shape_line(line), line
```
```python
# tests/test_a_signatory_records_a_pact_change.py — beside S9
def test_s9_a_notify_row_spelled_in_bold_leaves_a_row_citing_no_clause(repo):
    """Round 2 of PR #784, yellow 1: `**Pact notify**` renders as the item,
    so under `always` the moved row is left, not re-stamped unrecorded."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("**Pact notify**", "always")
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger_rows = [row("O1", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, ledger_rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert ledger.read_text(encoding="utf-8") == "".join(ledger_rows), out
    assert not (repo / "seal" / "pact-changes").exists(), out
```
```python
# hooks/config.py — pact_declaration, directly after
#     strays = stray_pact_rows(text, taken)
    # A row the walk took whose item is `Pact` or `Pact notify` in a code
    # span renders as that item and is read as neither (round 2 of PR #784,
    # yellow 2). Only the walk's own rows are looked at: the template's
    # `| Row | Value | Absent |` table names both items in code spans, and
    # the walk never reads it.
    lines = text.splitlines()
    strays += [
        (named, lines[index])
        for index, item, value in rows
        if value
        and item not in (PACT_ROW, PACT_NOTIFY_ROW)
        and item.startswith("`")
        and item.endswith("`")
        for named in (PACT_ROW, PACT_NOTIFY_ROW)
        if " ".join(shape_line(item).strip("`").split()).lower() == named.lower()
    ]
```
```python
# tests/test_a_signatory_declares_its_pact.py
@pytest.mark.parametrize(
    "row, item",
    [
        ("| `Pact notify` | always |", "Pact notify"),
        ("| ` Pact notify ` | always |", "Pact notify"),
        ("| `Pact` | https://example.com/org/other |", "Pact"),
    ],
)
def test_s3_a_pact_item_in_a_code_span_is_refused(row, item):
    """Round 2 of PR #784, yellow 2. GFM renders `<code>Pact notify</code>`
    in the live table; the walk took the row under another item."""
    declared = config.pact_declaration(CONFIG + row + "\n")
    assert declared[1] is None and refused_as(row, item) in declared[2], declared


def test_s7_a_code_spanned_item_with_no_value_is_the_default():
    assert config.pact_declaration(CONFIG + "| `Pact notify` |  |\n")[2] == []
```

## Executed probes

| What was run | Result |
|---|---|
| 1. Every line of the 641 tracked `.md` files, old shape vs the new shape over `shape_line` | 1 newly shaped (round-1-report.md:62, a quoted example), 0 lost |
| 2. `pact_declaration` at base vs target on the 23 tracked files carrying the live table's header | 0 differ; `templates/config.md` and `seal/config.md` both `([], None, [])` |
| 3. Nine pipe-less rows directly under the live table | all refused, `notify` None |
| 4. 25 must-not lines, directly under the table and after a blank | all 50 silent |
| 5. Both `shape_line` copies over 170 Cf characters; plugin refusal vs vendored `named` set at three places each | equal for all; 0 cases where the plugin refuses and the vendored copy is not blind |
| 6. The 13 prepended concatenation marks in `\| Pact<mark> \| x \|` | each refused as `Pact` (⬜ 3) |
| 7. Mutation: leading pipe required in both shapes; the four pact modules | 4 failed (the new pipe-less cases), 433 passed |
| 8. Mutation: `shape_line` as identity in both readers, the S3 format-character cases selected by keyword | 170 failed |
| 9. Mutation: identity `shape_line` plus the new clause removed; the four pact modules | 209 failed, 228 passed; every sentence pin and both vendored Cf rows red |
| 10. Eleven markup, reference and code-span spellings in the live table, reader at base and target, vendored set | all read the default with no refusal at both; vendored not blind (🟡 1, 🟡 2) |
| 11. cmark-gfm (the `cmarkgfm` package under `uv run --with`) on the code-span, bold and `&#32;` rows | each a row of the live table showing `Pact notify` |
| 12. Writer `--reverify` under `always`, moved row citing no clause, item spelled plain, as a code span, bold, and with `&#32;` | plain: exit 0, `seal/pact-changes/` written; the other three: exit 0, re-stamped, no `seal/pact-changes/` |
| 13. A code-span strip in `shape_line`, over the tree | 7 lines newly shaped incl. `templates/config.md:396`–`:397` and `skills/config/SKILL.md:47`–`:48`; the template's declaration changes (why 🟡 2 is not in the shape) |
| 14. Both paste-ready fixes applied in the clone, 14 new cases plus the four pact modules; ruff on the touched files | 451 passed; ruff flagged only the import order where the probe placed `import html`, which the fence places correctly |
| 15. The full suite, the repository-wide lint and the typecheck | not yet — the sealer's single run after the rounds settle; nothing in this round stands in for it |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
