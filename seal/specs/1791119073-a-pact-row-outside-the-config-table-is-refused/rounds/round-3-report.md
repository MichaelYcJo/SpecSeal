# Round 3 review report — 1791119073-a-pact-row-outside-the-config-table-is-refused

- Target: PR #784 (draft), branch `fix/759-a-pact-row-outside-the-config-table-is-refused`, SHA 168b0c9b, base `release/v0.18.2` at 94d7b2e0
- Ran by: specseal:warden on claude-opus-5-5
- Round kind: the verifying round, and the third round of the run. Its target is round 2's fix range `2f35e2f7..27af657e`, not the branch. The units round 2's `New units` row names were judged as code, not as fixes.
- Where: a `git clone --no-local` of the worktree at 168b0c9b, under `<scratchpad>/<work-item-id>/round-3/`. Nothing was written in the worktree except this file. The clone, the probe files and the patched copies of the readers were deleted before handover; no worktree or branch was made.
- Earlier rounds: `round-1.md` and `round-2.md` and their reports. Their coordinates were carried. Every verdict this round gives on what round 2's fixes touch was re-derived.

## Summary

Round 2's fixes hold for everything they enumerated. The 45 corpus spellings refuse, the writer and vendored rows leave, the two `shape_line` copies agree, and no declaration changed in any of the 644 tracked `.md` files. ⬜ 3's docstring is now true. The deliberate widening and the removed block-start exclusion are both sound.

The class is not closed, though. It was enumerated by construct, and two of the constructs were enumerated only in part:

1. **🟡 1. Round 2's yellow 2 is closed only where the whole item is one code span.** A backtick anywhere else in an item on the live table's own rows still reads as the default with no refusal. The six cases are `` `Pact` notify ``, ``Pact `notify` ``, `` **`Pact notify`** ``, `` `Pact notify`. ``, a lone backtick, and `&#96;Pact notify&#96;`. cmark-gfm shows each of them as the item.
2. **🟡 2. Round 2's yellow 1 still has members.** Five spellings read as the default although cmark-gfm shows the item:
   - inline raw HTML other than a tag or a comment: CDATA, a processing instruction, a declaration;
   - a tag whose quoted attribute holds `>`;
   - a link whose title holds `)`.

   A list-marker character followed by a no-break space, directly under the table, is a GFM row that the shape also passes by.

Both of them lose the record #759 exists to keep. I ran the writer on four of the spellings, and each time `evidence-check --reverify` exited 0, re-stamped a moved row citing no clause under `always`, and wrote no `seal/pact-changes/`. Neither finding started on this branch, because the base reads every one of these rows as the default too. Both sit inside units the branch owns, though, and the fences below close them without adding a unit.

There are also two ⬜ findings. The oracle test's "both directions" never runs its second direction, and an escaped pipe in the item is refused under the wrong item's name.

## The fixes, verified (stage 1)

### Round 2's yellow 1 — the item as GFM shows it (329f8ff7, 3902a349)

**What holds (executed).** All 45 `MARKUP` spellings refuse with the right item name. The bold, character-reference, link and hyphen rows leave in the writer and in the vendored copy. Both `shape_line` copies are equal over the corpus. I re-ran the 13 prepended concatenation marks beside the item, and all 13 refuse.

**Corpus axes, judged one by one (executed against cmark-gfm through `tests/gfm_table_oracle.py`, the `cmarkgfm` package the worktree's environment holds).**

| Axis the prompt names | At 168b0c9b |
|---|---|
| nested emphasis (`***Pact** notify*`, `*__Pact__ notify*`, `~~*Pact*~~ notify`) | refused, as GFM shows |
| backslash escapes (`Pact\ notify`, `\_Pact notify\_`, `Pact\-notify`) | refused, as GFM shows |
| `<br>` between the words | refused, as GFM shows |
| autolink (`<https://example.com/Pact>`) | silent, and GFM shows a URL; agrees |
| image (`![Pact notify]()`) | refused; GFM shows no text. Over-refusal, the loud direction |
| reference link, collapsed (`[Pact notify][]`) | refused, as GFM shows |
| reference link, undefined label (`[Pact notify][r]`) | refused; GFM shows `[Pact notify][r]`. Over-refusal |
| a pipe between the words, written as `&#124;` or backslash-escaped | refused, but named as `Pact` — ⬜ 4 |
| raw HTML: tag, comment | refused, as GFM shows |
| raw HTML: CDATA, processing instruction, declaration | **silent** — 🟡 2 |
| raw HTML: a tag whose quoted attribute holds `>` | **silent** — 🟡 2 |
| a link whose title holds `)` (`[Pact notify](x "a)b")`) | **silent** — 🟡 2 |
| raw HTML block vs inline | inline is what a cell holds. A line opening with a block-level tag directly under the table is an HTML block in GFM, and the reader removes the tag and refuses it. That is the loud direction, and a person reads the text as a row anyway |
| `&nbsp` with no semicolon | refused; GFM shows it literally. Over-refusal, because the standard library's unescape accepts legacy names with no `;` |

The corpus's own axis list (`WRAPS`, `JOINS`, `SPLITS`) is complete for emphasis, strikethrough, links without titles, tags with unquoted or `>`-free attributes, comments, character references and format characters. Raw HTML has five inline forms (CommonMark 6.6), and the corpus has two of them. This repository already reads all five: `hooks/blocks.py#INLINE_HTML` and `TAG_END` exist for #673, and `hidden_lines`' docstring lists them. That is 🟡 2.

**Can the normalization make a non-pact line pact-shaped where it matters (executed).** I compared every line of the 644 tracked `.md` files under the pre-round-2 shape (2f35e2f7) and under the target shape. Four lines are newly shaped, and all four are quoted examples in `rounds/round-1-report.md` and `rounds/round-1.md`. No line was lost. I also ran `pact_declaration` over all 644 files, of which 24 carry the `| Item | Value |` header text. No declaration differs between 2f35e2f7 and 168b0c9b. For prose below a config's table to be shaped now, a line has to open, after optional punctuation, with the item's letters, then non-word characters, a pipe and a value. No prose in the tree does that, and ordinary prose does not.

**The deliberate widening (read and executed).** `Pact-notify`, `Pact.notify` and `(Pact)` now refuse. GFM shows each as text a person reads as the item. The refusal is the loud direction, and no tracked declaration moved. Confirmed.

**The removed block-start exclusion, 3902a349 (executed).** The commit message is right that the exclusion guarded nothing. With an ASCII space or a tab after the marker, a list item or a heading is excluded by the branch's `\s`. I executed `- ` and a dash with a tab; the S7 guards for `* `, `+ ` and `# ` pass in the module run; `1. ` is excluded by its digit, which I read rather than ran. The `\s` is wider than GFM's marker separator, though. GFM's marker separator is a space or a tab. Five lookalikes directly under the table render as rows of the live table and are silent: `-`, `*`, `#` or `+` followed by U+00A0, and `-` followed by U+2003. That belongs to 🟡 2. It is not a regression, because before 3902a349 these were not shaped either.

### Round 2's yellow 2 — an item in a code span (329f8ff7, 79ad70f7)

**What holds (executed).** All four round-2 code-span cases refuse. `test_s7_a_code_spanned_item_off_the_walks_rows_or_empty_is_not_refused` holds: an empty value is not refused, and neither is a span off the walk's rows. The template, `seal/config.md` and `skills/config/SKILL.md` are not refused.

**What does not.** The rule reads an item only when its first and last characters are both backticks. A code span that is part of the item is not read, and neither is a backtick that opens no span. The shape excludes every backtick, so nothing else reads them either. That is 🟡 1. The same check feeds the item into `_letters`, which keeps letters only. So `` `Pact 2` `` on the walk's row is refused as `Pact`, and `` `Pact notify 1` `` as `Pact notify`. Those are over-refusals, the loud direction, and the fence for 🟡 1 replaces that path.

**The vendored copy's documented limit (read and executed).** `docs/the-pact.md:336` and `test_a_vendored_copy_reads_no_code_spanned_item` state it, and the statement is accurate for an item that is one code span. The copy also reads none of 🟡 1's other spellings, because its shape excludes the backtick too. The fence for 🟡 1 widens the sentence to say so. The choice itself (option b) was the orchestrator's in round 2, and I carried it.

### Round 2's white 3 — the docstring (329f8ff7)

`shape_line`'s docstring no longer says GFM renders no Cf character. It names the thirteen marks, and it says which way each removal errs. I executed the thirteen and all refuse. Every removal it lists can only refuse, because the shape allows any non-word character between the letters. Confirmed.

## Findings

### 🟡 1 — a backtick anywhere in an item on the live table's own rows reads it as the default (`hooks/config.py:929`)

**What is wrong.** `stray_pact_rows` reads a walk row's item as a pact item only when `item[0] == item[-1] == "`"`. `PACT_ROW_SHAPE` excludes the backtick everywhere, so no other path reads such a row. Six spellings that cmark-gfm renders as `Pact notify` in the live table are read as the default with no refusal:

- `` `Pact` notify ``
- ``Pact `notify` ``
- `` **`Pact notify`** ``
- `` `Pact notify`. ``
- ``Pact notify` ``
- `&#96;Pact notify&#96;`

`` [`Pact notify`]() `` and `` <b>`Pact notify`</b> `` behave the same way.

**Why it matters.** It is round 2's yellow 2 again, one spelling over. I ran the writer for `` `Pact` notify `` and `` **`Pact notify`** `` under a `Pact` value. It exited 0, re-stamped the moved row citing no clause, and wrote no `seal/pact-changes/`. The re-stamp clears the drift that was the only trigger for the record. `` `Pact` notify `` is the likeliest of these to be typed, because this repository's documents write the item name in a code span inside prose.

**The fix.** Read every row the walk took, but did not take as a pact row, through the shape with its backticks removed. The walk never reads the template's `| Row | Value | Absent |` table, so the reason the shape keeps backticks does not reach these rows. Using the shape instead of `_letters` also drops the digit over-refusal described above. I applied it in the clone. All six spellings refuse, `test_s7_a_code_spanned_item_off_the_walks_rows_or_empty_is_not_refused` still holds, and nothing in the tree moves.

### 🟡 2 — five inline constructs GFM renders away are kept by `shape_line`, and one marker separator is read too widely (`hooks/config.py:690`)

**What is wrong.** `shape_line` removes a tag only when its attributes hold no `<` or `>`, and it removes an HTML comment. It does not remove CDATA, a processing instruction or a declaration. Its link pattern `\]\([^)]*\)` stops at the first `)`, including one inside a quoted title. Both copies have the same gaps. With the raw HTML left out, cmark-gfm renders each of these as the item, and the reader reads the row as the default:

- `Pact<?x?>notify`
- `Pact<!X y>notify`
- `Pact<![CDATA[]]>notify`
- `<span title="a>b">Pact</span> notify`
- `[Pact notify](x "a)b")`

Separately, `PACT_ROW_SHAPE`'s pipe-less branch stops at `\s`, which in Python's Unicode mode includes U+00A0 and U+2003. GFM's list-marker separator is only a space or a tab, so `-`+U+00A0+`Pact notify | always |` directly under the table is a row of the live table, and it is silent.

**Why it matters.** Round 2's record says the class was closed by construction. These constructs are members of it that the construction did not generate. `docs/the-pact.md` names "inline HTML" as a spelling that is refused. I ran the writer for `Pact<?x?>notify` and for the link with a `)` in its title, and both re-stamped unrecorded. A person is unlikely to type these spellings. The defect is that the reader does not do what its own document says, on the path that loses a record.

**The fix.** Spell all five raw HTML forms in `shape_line`, with a quoted attribute value allowed to hold `>` as `hooks/blocks.py#TAG_END` already allows. Let the link pattern step over a quoted title and one level of parentheses. Narrow the pipe-less branch's `\s` to a space and a tab in both shapes. The comment alternative is spelled `<!-{2}.*?-{2}>` in the fence below. It matches exactly what the target's spelling matches (executed), and it keeps the four-character comment opener out of this report, which the round-record generator would otherwise strip. The smith may keep either spelling. I applied all of it in the clone: the new corpus members refuse, S14 holds the two copies equal, the four pact modules pass, and no line in the 644 files is newly shaped or lost.

### ⬜ 3 — the oracle test's second direction never runs, and its criterion drops digits (`tests/test_a_signatory_declares_its_pact.py:408`)

`test_s3_an_item_is_refused_exactly_where_gfm_shows_a_pact_item` asserts `refusals == []` where cmark-gfm shows something other than the item. None of the 45 `MARKUP` spellings renders as anything else, so that branch never executes (executed: 0 of 45). The test cannot catch an over-refusal, which leaves round 2's "in both directions" claim unbacked. The criterion `letters` keeps only `isalpha`, so `Pact 2 notify` counts as the item to the oracle. Over the 45 spellings the release ships nothing wrong. The test's claim is wider than what it checks. The optional fence adds one negative, `Pact 2 notify`, and makes `letters` keep digits, which runs the second branch. With `letters` reverted, that case fails (executed). The reader's deliberate over-refusals (an image, an undefined reference label, `&nbsp` with no `;`) cannot join the corpus as negatives, because the reader refuses them on purpose. So "exactly where" can only ever describe the corpus, and the docstring may want to say so.

### ⬜ 4 — an escaped or entity-encoded pipe in the item is refused under the wrong item's name (`hooks/config.py:951`)

GFM shows `| Pact\|notify | always |` and `| Pact&#124;notify | always |` as one cell, `Pact|notify`. The shape reads the decoded or escaped pipe as the cell's end, so the row is refused as a `Pact` row and the sentence says "Write it as `| Pact | … |`". In a config with no `Pact` row anywhere, it is still refused. S6 says a notify row with no pact is ignored (executed: `([], None, [one refusal naming Pact])`). The direction is loud and the sentence misleads, and nobody types this on purpose. No fix is commissioned. If it is wanted, `shape_line` can turn `\|` and the pipe references into a non-word, non-pipe character before the shape reads the line.

## Regression tests to plant

All of these are rows in existing lists or parametrizations, so no unit is added. They are in the fences under `## Paste-ready fixes`.

- `tests/test_a_signatory_declares_its_pact.py`: five rows in `test_s3_a_pact_item_in_a_code_span_is_refused_on_the_walks_rows` (🟡 1). Five `WRAPS` entries and one `STRAY_WAYS` entry (🟡 2). Optionally, one `SPLITS` entry and `letters` keeping digits (⬜ 3).
- `tests/test_a_signatory_records_a_pact_change.py`: two rows in `test_s9_a_notify_row_below_the_table_leaves_a_row_citing_no_clause`, one per finding.

**Seen red (executed).** With the test rows in place and the code at 168b0c9b, the four pact modules ran 18 failed and 503 passed. The failures were exactly the new rows: five code-span, ten corpus, one `STRAY_WAYS` and two S9. With the code fences applied, all 521 passed.

## Facts for the evidence ledger

- `hooks/config.py#stray_pact_rows` and `hooks/config.py#shape_line` change content under these fences, along with `evidence_check.py#shape_line` and both shapes. Any ledger row citing them will be flagged changed by `evidence-check` and needs re-reading in the branch's fragment. The behaviour those rows state does not change, only its reach.
- `docs/the-pact.md`'s `Enforced by:` lines need no new entry. Every new case is a row of a test already listed there.

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

## Paste-ready fixes

### 🟡 1

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

### 🟡 2

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

### ⬜ 3 (optional)

```python
# tests/test_a_signatory_declares_its_pact.py
def letters(text):
    return "".join(ch for ch in text.lower() if ch.isalnum())


# SPLITS: append after "P&#97;ct notify",
    "Pact 2 notify",
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (a backtick anywhere in an item on the live table's own rows) and 🟡 2 (raw HTML other than a tag or comment, a quoted `>`, a titled link, and a Unicode space after a marker character), each still read as the default with no refusal

Loses a record or crashes: yes — under 🟡 1 and 🟡 2, `evidence-check --reverify` re-stamps a moved row citing no clause under `always` and records no pact change; executed through the writer for `` `Pact` notify ``, `` **`Pact notify`** ``, `Pact<?x?>notify` and a link whose title holds `)`. All predate this branch

## What this round's verdicts mean for the run

- **The round cap.** This is round 3. No 🔴 has been open in any round, so the cap is three (`docs/review-chain-spec.md` §*The review run has a bound, and an end*). No further finding round is spawned. The floor was not met in this round either, so the floor is not what ends the run. The cap is.
- **The cap does not decide the two 🟡.** §*The cap bounds rounds, and not the fixes of the round it stopped* decides them by who owns the unit. Both 🟡 sit in units this branch wrote:
  - `shape_line` is round 1's depth-1 unit.
  - The code-span loop is round 2's change to `stray_pact_rows`.
  - `PACT_ROW_SHAPE`, `NOTIFY_ROW_SHAPE` and `stray_pact_rows` are the branch's own build.
  - `WRAPS`, `SPLITS` and `letters` are round 2's depth-1 units.

  By that rule the branch fixes them. The fences add no unit (regex edits, one loop body, and rows in existing lists and parametrizations), so no depth-2 refusal applies. One verifying round then reads that fix diff, and that record ends the run.
- **The reopening bound is not engaged.** No record has met the floor yet (`docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*).
- **The two ⬜ commission nothing.** ⬜ 3's fence is optional. ⬜ 4 has none.
- **The broad gate is not due yet.** This report leaves two 🟡 open, so the sealer's spawn waits for the verifying round that reads their fixes.

## Proof block

Files opened (read): `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/rounds/round-1.md`, `rounds/round-2.md`, `rounds/round-2-report.md` (opening sections); `skills/code-review/orchestration.md` lines 120–319; `docs/review-chain-spec.md` lines 41–180; `hooks/config.py` lines 99–103, 183–378, 655–700, 800–980; `hooks/blocks.py` lines 196–260; `skills/evidence-check/scripts/evidence_check.py` lines 3745–3770, 3820–3900; `tests/gfm_table_oracle.py`; `tests/test_a_signatory_declares_its_pact.py` lines 1–60, 189–300, 348–480, 555–650; `tests/test_a_signatory_records_a_pact_change.py` lines 945–1000, 1481–1625; `docs/the-pact.md` lines 80–100 and 328–342; `.github/scripts/run_tests.py` (the pin lines); the full diff `2f35e2f7..27af657e` of the code, test and document files; `git show 3902a349`.

Executed: probes 1–12 above, in the clone at 168b0c9b, with the worktree's existing virtual environment as the interpreter (no bytecode written) and `uvx ruff`. Unverified: the full suite, the repository-wide lint and the typecheck, which the sealer answers.
