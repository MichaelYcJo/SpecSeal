# Round 2 review report — 1791119073-a-pact-row-outside-the-config-table-is-refused

- Target: PR #784 (draft), branch `fix/759-a-pact-row-outside-the-config-table-is-refused`, SHA 425b6298, base `release/v0.18.2` at 94d7b2e0
- Ran by: specseal:warden on claude-opus-5-5
- Round kind: the verifying round. Its target is round 1's fix range `8e63ea91..fc07acdd` (six files of code and tests, five of documents), not the branch.
- Where: a `git clone --no-local` of the worktree, checked out at 425b6298, under the round's scratch directory. Nothing was written in the worktree except this file. The clone, its probe and the probe's temporary test files were deleted before handover.
- Earlier rounds: round 1 (`round-1.md`, closed at 425b6298). Its coordinates were carried. Its verdicts on what the fixes touch were re-derived here.

## Summary

Round 1's three fixes close what they were written for, and none of them regresses anything I could find.

- **The optional leading pipe (round 1's yellow 1).** Every pipe-less row I wrote directly under the live table is refused. On the other side, I ran the new shape over every line of all 641 tracked `.md` files and over the 23 tracked files that carry an `| Item | Value |` table, comparing it with the old shape. It shapes exactly one new line, which is a quoted example in round 1's report, and it changes no declaration.
- **The Cf strip (round 1's yellow 2).** The two `shape_line` copies agree for all 170 Cf characters. The vendored copy is blind wherever the plugin refuses. Stripping a format character can make a line pact-shaped only when the line without it is already pact-shaped.
- **The new clause in the refusal (round 1's white 5).** It is pinned in all four places. Removing it turns every pin red.

Two new findings belong to the class round 1's yellow 2 opened. The fix enumerated one member of that class, so the same loss is still open for other members:

1. **🟡 1 — markup and character references.** An item written as `**Pact notify**`, `[Pact notify]()`, `<b>Pact</b> notify` or `Pact&#32;notify` inside the live table renders as `Pact notify`. The reader still treats it as the default and gives no refusal. Fix 1's own reasoning in `shape_line` applies to these spellings word for word: GFM shows the item without them, and a person reads the row without them.
2. **🟡 2 — a code span.** `` | `Pact notify` | always | `` has the same loss. It cannot be fixed in the shape, because the template's own documentation table writes exactly that line.

Neither finding is new on this branch: the base reads both the same way. Both lose the record #759 exists to keep. I ran the writer, and it re-stamped a moved row citing no clause and wrote no `seal/pact-changes/` record.

## The fixes, verified (stage 1)

### Round 1's yellow 1: the leading pipe is optional (6d35a1be)

**Pipe-less rows that must refuse (executed).** I put nine rows directly under the live table. All nine are refused, with `notify` None: `Pact notify | always |`, `Pact notify | always`, `   Pact notify|always`, mixed case, a tab or a U+00A0 between the words, a value in a code span, a second `Pact` row, and a block-quoted one. A pipe-less line holding no pipe at all is also a GFM row, but it is a one-cell row with an empty value, which is the default anyway. Nothing is lost there.

**Lines that must stay silent (executed).** I wrote 25 lines, each once directly under the table and once after a blank line. All 50 stayed silent. They were:

- prose that starts with `Pact notify`
- `## Pact | notify` and `# Pact notify | always`
- `Pact:`, `Pact notify:` and `Pact notify —` lines
- the four list markers
- `Pacts`, `Impact`, `Pact name`, `Pact-notify` and `Pact notify me` as items
- empty values with and without a leading pipe
- a closed fence, a closed comment, and an indented fence line
- an escaped leading pipe, and a whole line in a code span

**This repository's own files (executed).** Across every tracked `.md`, the new shape matches one line the old shape did not: `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/rounds/round-1-report.md:62`, a quoted example that is not in any config. The new shape loses no line the old one matched. `pact_declaration` returns the same value at base and target for all 23 files that carry the live table's header. That includes `templates/config.md` and `seal/config.md`, which both return `([], None, [])`.

**The cases are red without the fix (executed).** With the leading pipe made required again in both shapes, the four pact modules fail exactly four cases: the two new `STRAY_WAYS` rows, the no-pipe S9 row and the no-pipe vendored row. 433 pass.

### Round 1's yellow 2: format characters are removed before the shape (a92db6af)

**The two readers stay equal (executed).** Python 3.12 has Unicode 15.1 and 170 Cf characters. For each of them, `hooks/config.py#shape_line` and `evidence_check.py#shape_line` return the same string on two lines that carry the character at every slot. S14 now pins the same thing. Both bodies are the same expression.

**Plugin refuses ⇒ vendored copy is blind (executed).** I placed each Cf character in three places: inside `Pact`, between the words, and before a pipe-less row. Over all 510 inputs there is no case where the plugin refuses and the vendored `named` set is not blind.

**Can stripping make a non-pact line pact-shaped? (executed and read)** Removing a character makes a line equal to the same line without it. So the strip shapes a line only where the line, minus its Cf characters, is already shaped. The question becomes whether any Cf character is visible to a reader. Thirteen are. The prepended concatenation marks (U+0600–U+0605, U+06DD, U+070F, U+0890, U+0891, U+08E2, U+110BD, U+110CD) render as a glyph. `| Pact<U+06DD> | x |` is refused as a `Pact` row although a person sees `Pact` followed by a mark. That is the loud direction, and nothing is lost. But `shape_line`'s docstring says GFM renders none of them, which is not true for these thirteen. That is ⬜ 3.

**The letters-only item name (read and executed).** `_shaped_item` and the vendored `named` set both remove every `\s` character and compare against `pactnotify`. A tab, an NBSP or an empty separator all reach `Pact notify`, and nothing else does: `Pactnotify-ish | x` stays silent.

**The `<U+XXXX>` display (executed).** S3 pins it for every Cf character. With `shape_line` reduced to returning its argument in both readers, all 170 S3 cases fail.

### Round 1's white 5: the refusal's fourth cause (37f50c61)

The clause "is not written as a two-cell row" is in `stray_refusal` and in all four pins: the reader's `refused_as`, the writer's `stray_refusal`, S10 in `tests/test_pact_check.py` and S11 in `tests/test_a_signatorys_ci_prints_its_pact.py`. I grepped the tree for the old wording. It survives only in `spec.md`'s quoted draft, which `overview.md`'s divergence table already records, and in round 1's report.

I removed the clause, together with the identity `shape_line`, and ran the four modules. 209 failed, including every sentence pin: S1, S2, S3, S4, S5, S9, S10 and S11. The clause also covers a pipe-less row reasonably well. The remedy, `| Pact notify | … |`, shows the leading pipe.

### Round 1's two answered whites

- **White 3, indented rows refused (read).** `spec.md:64` says "any indentation", and `templates/config.md:419` says an indented row is refused. The grounds hold.
- **White 4, "may be `always`" (read).** The vendored `LEFT` line is at `skills/evidence-check/scripts/evidence_check.py:3850` and `:3879` at the base 94d7b2e0. `git log -S` puts it in d671a43 (#756). This branch changed no word of it. The grounds hold.

### Carried, not re-derived

Round 1 had two green verdicts that no fix touches: the new cases are red at the base, and fa4ddfe1 carries four files. I carried both. Round 1's deferral, a misplaced `Ledger frozen from` row, is already deferred in round 1, and the orchestrator of this run answers it. This round does not raise it again.

## Findings from execution

### 🟡 1 — markup or a character reference around the item is read as the default

`hooks/config.py:663` (`shape_line`), and its copy at `skills/evidence-check/scripts/evidence_check.py:3753`.

**What is wrong.** Each of these was written as a row inside the live table:

- `| **Pact notify** | always |`, and the same with `*…*`, `__…__` or `~~…~~`
- `| *Pact* *notify* | always |`
- `| [Pact notify]() | always |`
- `| <b>Pact</b> notify | always |`
- `| Pact&#32;notify | always |`, `| Pact&nbsp;notify | always |` and `| Pact&#x200B;notify | always |`

The reader returns `notify` = `when the pact is touched` with no refusal for every one. The vendored copy is not blind for them either. cmark-gfm renders `<strong>Pact notify</strong>` and a plain `Pact notify` for the bold and `&#32;` rows, inside the live table.

**Why it matters.** I ran `evidence-check --reverify` under `always` with a moved row citing no clause. With `**Pact notify**` and `Pact&#32;notify` the run exited 0, re-stamped the row, and wrote no `seal/pact-changes/`. Spelled plainly, the same run writes the record. This is #759's loss. Nobody needs to attack anything to get here: the rendered file shows a correct row, and that is all a person reviewing it sees.

**Why it is this round's.** Fix 2's docstring gives the reason a Cf character is removed: "GFM renders none of them and a person reads the row without them". Markup and character references meet the same test. The fix enumerated one member of the class and not the class (contract §12).

**The fix.** Extend both `shape_line` copies. A character reference becomes its character. Then the Cf characters are removed. Then emphasis, strikethrough, link and inline-HTML markup touching `Pact` or `notify` is removed. No new unit is added, and S14 keeps the two copies equal. The fix leaves code spans alone, which is 🟡 2.

I applied the fix in the clone and ran it over every guard above, the whole tree and the four pact modules with the new cases (executed). Results:

- No guard line was refused.
- No tracked config's declaration changed.
- The only newly shaped line in the tree is the same quoted line from round 1's report.
- 451 passed.

One line that was silent is now refused: `*Pact notify | always`, an unmatched `*` that GFM shows literally. It is refused loudly, which is the safe direction.

### 🟡 2 — an item in a code span is read as the default

`hooks/config.py:819` (`pact_declaration`, where the strays are gathered).

**What is wrong.** With `` | `Pact notify` | always | `` or `` | `Pact` | https://example.com/org/other | `` as a row of the live table, the walk takes the row under the item `` `Pact notify` ``. That item is neither pact item, and the shape does not see past the backtick. The result is the default with no refusal. cmark-gfm renders `<code>Pact notify</code>` in the live table. The repository's own documents write the item this way everywhere, so this is the spelling a person copying from `docs/the-pact.md` is most likely to produce.

**Why it matters (executed).** The writer re-stamped a moved row citing no clause under `always` and wrote no record. That is the same loss as 🟡 1.

**Why it is not fixed in the shape (executed).** I removed code-span backticks in `shape_line` as a probe. Seven lines became pact-shaped, including `templates/config.md:396` and `:397` and `skills/config/SKILL.md:47` and `:48`. Those lines are the `| Row | Value | Absent |` documentation tables, which name both items in code spans. The template's declaration also changed. A shipped template that refuses itself is the regression round 2 of #756 warned about.

**The fix (executed in the clone).** Refuse only rows the walk itself took whose item is a pact item in a code span with a value. The documentation tables are never the walk's table. With this applied, the template, `seal/config.md` and `skills/config/SKILL.md` stay silent, an empty value stays silent, and the four modules pass.

**What is left for a decision.** The vendored copy has no walk. The same change to the line shape there would make it blind on every template-derived config. Leaving it unchanged breaks the invariant that `test_a_vendored_copy_leaves_where_the_plugin_refuses_a_stray_notify` holds, for this one spelling. So one of two things is needed:

- (a) the vendored copy finds the first `| Item | Value |` table itself and reads a code span only on its rows, or
- (b) `docs/the-pact.md` names this spelling as the vendored copy's known limit, and the vendored case leaves it out.

The orchestrator of this run answers it. A small cosmetic point also comes with this fix: the refusal sentence quotes the line in backticks, so a line that holds a code span nests backticks. The sentence is still readable in a terminal.

### ⬜ 3 — `shape_line`'s docstring says GFM renders no format character

`hooks/config.py:664`, and the vendored docstring's "as GFM renders it" at `skills/evidence-check/scripts/evidence_check.py:3755`. Thirteen Cf characters render as a glyph (executed above). The behaviour is right, because those rows are refused loudly. The sentence is wrong. The docstring in 🟡 1's fence states it correctly, so applying that fix closes this one too. `docs/the-pact.md` says "such as U+200B", which stays true.

## Findings from reading

None beyond the grounds above.

## Regression tests to plant

- `tests/test_a_signatory_declares_its_pact.py`: the markup/reference cases and the code-span cases (fences below). S14's equality loop extended to markup lines.
- `tests/test_a_signatory_records_a_pact_change.py`: a writer row under `always` with `**Pact notify**`. Whether the vendored list takes the code-span row depends on the answer to 🟡 2's decision.

Seen red: the inputs of every case below were executed silent at the target (probe 10). The cases themselves were run only against the patched clone, where they pass.

## Facts for the evidence ledger

- `hooks/config.py#shape_line` is the one place a line's rendering is normalised before the shape reads it. `evidence_check.py#shape_line` is its copy. Both are pinned equal by S14 over every Cf character.
- `templates/config.md:394`–`:397` and `skills/config/SKILL.md:47`–`:48` write `` `Pact` `` and `` `Pact notify` `` as items of a documentation table. Any shape that reads past a code span refuses them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An item spelled with emphasis, strikethrough, a link, inline HTML or a character reference (`**Pact notify**`, `Pact&#32;notify`) in the live table renders as the item, and is read as the default with no refusal; `--reverify` re-stamps a moved row citing no clause unrecorded | `hooks/config.py:663` | open | executed: eleven spellings silent at base and target, vendored not blind; cmark-gfm renders them as `Pact notify` in the live table; the writer re-stamped under `always` with no `seal/pact-changes/`. Same class and same reasoning as round 1's yellow 2, whose fix enumerated Cf only. The fence for both copies passes every guard and the four pact modules |
| 🟡 2 | An item in a code span (`` `Pact notify` ``, `` `Pact` ``) in the live table is read as the default with no refusal; `--reverify` re-stamps unrecorded | `hooks/config.py:819` | open | executed: reader silent at base and target, cmark-gfm renders `<code>Pact notify</code>` in the live table, the writer re-stamped with no record. Not fixable in the shape: `templates/config.md:396`–`:397` and `skills/config/SKILL.md:47`–`:48` become pact-shaped. The fence refuses only the walk's own rows. The vendored half is a choice, and the orchestrator of this run answers it |
| ⬜ 3 | `shape_line`'s docstring says GFM renders no Cf character, and thirteen (the prepended concatenation marks) render as a glyph | `hooks/config.py:664` | open | executed: `\| Pact<U+06DD> \| x \|` and the other twelve are refused as `Pact`. The behaviour is loud and right, and the sentence is wrong. Closed by 🟡 1's docstring |
| 🟢 | round 1's yellow 1 is closed — a pact row with no leading pipe directly under the table is refused in both readers | `hooks/config.py:660` | confirmed | executed: nine pipe-less rows refused; 50 must-not placements silent; one newly shaped line across 641 tracked `.md` files (a quoted example), no lost line, no declaration change across 23 config-shaped files; with the pipe required again, exactly the four new cases fail |
| 🟢 | round 1's yellow 2 is closed — a Cf character in or around the item is removed before the shape, in both readers alike, and shown as its code point | `hooks/config.py:663` | confirmed | executed: both `shape_line` copies equal over all 170 Cf characters; plugin refuses ⇒ vendored blind over 510 inputs; with `shape_line` as identity all 170 S3 cases fail. Its class is wider, which is this round's findings 1 and 2 |
| 🟢 | round 1's white 5 is closed — the refusal names the row's own shape, in all four pins | `hooks/config.py:938` | confirmed | executed: the clause removed with the identity `shape_line`, 209 failed, every sentence pin among them; read: the old wording survives only in `spec.md`'s quoted draft (recorded divergence) and round 1's report |
| 🟢 | round 1's white 3 answer holds — an indented row is refused by the spec's choice | `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/spec.md:64` | confirmed | read: `spec.md:64` "any indentation", `templates/config.md:419` |
| 🟢 | round 1's white 4 answer holds — the vendored "may be `always`" line predates the branch | `skills/evidence-check/scripts/evidence_check.py:3866` | confirmed | read: present at 94d7b2e0 lines 3850 and 3879, introduced by d671a43 (#756), unchanged by this branch |
| carried | round 1's green verdicts on the base-red cases and on fa4ddfe1's file list | `tests/test_a_signatory_declares_its_pact.py` | confirmed | carried from round 1, not re-derived; no fix touches either |

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

## Paste-ready fixes

### 🟡 1 and ⬜ 3 — both `shape_line` copies

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

### 🟡 2 — a code-spanned item on the walk's own rows

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

Needs a fix: yes — 🟡 1 (markup or a character reference around the item) and 🟡 2 (an item in a code span), both still read as the default with no refusal

Loses a record or crashes: yes — under 🟡 1 and 🟡 2, `evidence-check --reverify` re-stamps a moved row citing no clause under `always` and records no pact change (executed through the writer for a code span, bold, and `&#32;`). Both predate this branch.

## Unverified

- The full suite, repository-wide lint and typecheck: not run (contract §2). The sealer answers it, after the rounds settle.
- The vendored half of 🟡 2: no fence, by design. The orchestrator of this run answers which of (a) or (b).

## Proof — files opened

- `hooks/config.py` (the fix diff; lines 330–420, 640–680, 790–960 at 425b6298)
- `skills/evidence-check/scripts/evidence_check.py` (the fix diff; 3836–3880; the import block at 425b6298; the `LEFT` lines at 94d7b2e0)
- `tests/test_a_signatory_declares_its_pact.py`, `tests/test_a_signatory_records_a_pact_change.py` (930–990, the fixtures at 24–82), `tests/test_a_signatorys_ci_prints_its_pact.py`, `tests/test_pact_check.py` (fix-range diffs)
- `docs/the-pact.md`, `templates/config.md` (fix-range diff; 1–12, 385–400), `skills/config/SKILL.md` (grep), `seal/config.md` (grep)
- `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/`: `rounds/round-1.md`, `rounds/round-1-report.md` (1–40), `spec.md` (55–75), `overview.md` (fix-range diff)
- `bin/test`, `.github/scripts/run_tests.py` (grep)
