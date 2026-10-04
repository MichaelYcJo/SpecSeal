# 1791128260-a-pact-row-is-read-in-one-plain-spelling — review round 1

| Field | Value |
|---|---|
| Target SHA | 91c4a2c8958640365a2d62222ddd6e1bb846911d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #793 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the template refuses itself on a path a shipped skill prescribes), 🟡 2 (an HTML table row is read as the default and the documented sentence is false), 🟡 3 (the vendored copy re-stamps under a transposed table) |
| Loses a record or crashes | yes — under 🟡 2 the plugin's writer, and under 🟡 3 the vendored writer, re-stamp a moved row citing no clause at exit 0 and record no pact change (executed). Both predate the branch and sit in units it owns. |

- [ ] Pass

## What this round was asked

Round 1 of the #759 redesign (PR #793), at 91c4a2c8 against `release/v0.18.2` (94d7b2e0): spec compliance first, then quality. Judge whether every spelling #784's four rounds found refuses under the one-plain-spelling rule and whether any spelling a person reads as a pact item, outside the documented blind side, still reads as the default; whether the predicate refuses anything it must not (this repository's config, what `seal mode` writes, the copied Broad gate block, `impact`, a walk row's value, pipe-less prose) and whether its stated cost is true; the vendored copy against the plugin; the callers, the refusal sentence, the docs and pins, the `Corrected ·` C1 row and the re-reads.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `templates/config.md` read whole now gives seven refusals, two of them the paragraph this branch added; the spec accepts it on the premise that nothing copies it whole, which `skills/commit-pr-convention/SKILL.md:78`, the template's preface and the pull-request-language test contradict; in such a repository with no pact, `--reverify` leaves every moved row at exit 1 | `templates/config.md:389` | open | executed: `pact_declaration` base `([], None, [])`, head seven refusals; writer base exit 0 re-stamped, head exit 1 `LEFT`; filled template base `always`, head `None`. The pipe-free rewrite in the fence reads silent in both readers and keeps the S12 template pins |
| 🟡 2 | A pact row in an HTML table (`<td>Pact notify</td><td>always</td>`) is a value cell with no `\|`, read as the default by both readers; `docs/the-pact.md:91` says a line with no `\|` has no value cell | `hooks/config.py:922` | open | executed: cmark-gfm renders the cells; reader default with no refusal and the copy not blind on three shapes; the writer re-stamped at exit 0 with no `seal/pact-changes/`; same at the base. The file-level HTML-cell condition in the fence refuses all three and leaves the silent set unchanged |
| 🟡 3 | The vendored copy reads a transposed table's header (`\| Pact \| Pact notify \|` over `\| <url> \| always \|`) by its item alone and re-stamps unrecorded where the plugin refuses; its docstring says nothing can mean `always` there | `skills/evidence-check/scripts/evidence_check.py:3781` | open | executed: copy not blind on three transposed shapes; vendored writer exit 0, re-stamped, no `seal/pact-changes/`; plugin writer exit 1. The base's shape behaved the same. The header condition in the fence makes all three blind, keeps S9 (b)'s verdicts and misses none of the 1,751 S2 texts |
| ⬜ 4 | The vendored rule is stated wider than the code: a two-cell row off the table whose item names no pact is refused by the plugin and re-stamped by the copy, while `skills/evidence-check/SKILL.md:339`, `docs/the-pact.md:327` and spec Scope 2 say the copy leaves there | `skills/evidence-check/SKILL.md:339` | open | executed: `\| Note \| the orders pact \|` below the table, plugin `None` with one refusal, copy not blind. The behaviour is safe, and S9 (b) needs it; the sentence is what is wrong |
| ⬜ 5 | The `Corrected ·` row for 0.18.1 C1 states ⬜ 4's over-claim | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:5` | open | read; a correction to the run's paperwork, reworded with ⬜ 4's sentence |
| ⬜ 6 | The blind-side paragraph names a look-alike "from another script", and small capitals (Latin) are blind too; the rule paragraph omits the NFKC fold that catches fullwidth and mathematical letters | `docs/the-pact.md:337` | open | executed: small capitals and the Hangul fillers read the default; fullwidth, mathematical bold and a combining accent refuse |
| 🟢 | Every spelling #784's four rounds named refuses, in the table and below it, and the vendored copy is blind on each | `tests/test_a_signatory_declares_its_pact.py` | confirmed | executed: 352 placements typed from the four reports, plus every splitlines-only character at every position of a row; no miss once my own mistranscription is set aside |
| 🟢 | The must-not set is silent: `impact`, `compact`, a walked row's value, pipe-less prose and comments, a no-break space beside a pipe, this repository's config | `hooks/config.py:686` | confirmed | executed through `pact_declaration` and `notify_may_be_always`; the `seal mode` stub and the copied Broad gate block are read in `test_s4_the_configs_this_plugin_writes_or_copies_are_silent`, which the orchestrator's narrow run executed |
| 🟢 | Wherever the plugin reads `always` the vendored copy is blind, and the stated difference (a plain `Pact` row off the table with no notify row) is safe | `skills/evidence-check/scripts/evidence_check.py:3757` | confirmed | executed: 60,000 random configs, no counterexample; the stated difference executed; the U+2028 guard read and pinned at all eight characters |
| 🟢 | The GFM-line-to-walk-index mapping in `pact_lines_not_read` agrees with `text.splitlines()` | `hooks/config.py:913` | confirmed | executed: 20,000 random texts over the terminators, the eight characters, pipes and letters, no mismatch |
| 🟢 | The `Corrected ·` row re-points 0.18.1 C1 from `NOTIFY_ROW_SHAPE` to the three new vendored units and keeps every other coordinate | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:5` | confirmed | executed: a cell-by-cell diff against `seal/releases/0.18.1.md:168` |
| ❓ | Whether github.com's rendering of YAML front matter as a table is a spelling the rule owes a refusal: `---` / `Pact notify: always` / `---` at the top of `seal/config.md` is silent in both readers | `docs/the-pact.md:91` | ❓ out of verified scope | executed: silent in both readers; not executable here: github.com's rendering is not reachable from this round, and cmark-gfm renders it as a rule and a heading. The orchestrator answers it, as it answers #784 round 4's question about github.com's emoji |

## Paste-ready fixes

```markdown
templates/config.md — replace the fenced two-row example and the
`| Row | Value | Absent |` table below it, through its `Pact notify` row, with:

Both rows are written in the table at the top of this file, and nowhere
else in it:

- **`Pact`**: the origin remote URL of the pact's repository, such as
  `git@example.com:org/orders-api.git`; a signatory of pacts held in more
  than one repository lists them separated by `;`. Absent: no pact is held
  elsewhere.
- **`Pact notify`**: `always` · `when the pact is touched` · `never`.
  Absent: `when the pact is touched` where a `Pact` row stands, and ignored
  where none does. Written anywhere but the table above, or spelled any
  other way, it is refused, not absent.
```
```markdown
templates/config.md — replace the `| Value | Recorded here | Read there |` table with:

- **`when the pact is touched`** records a row citing a clause of a pact
  the `Pact` row names, and the pact's repository reads it as `NOT TAKEN`,
  exit 1, until a pact review takes it.
- **`always`** records that, and every other row whose code moved, with `—`
  for its clause; the pact's repository reads a `—` row as `NOTED`, which
  moves no exit.
- **`never`** records nothing, and the pact's repository reads nothing,
  whatever an earlier value recorded.
```
```markdown
templates/config.md — in the paragraph "**Both rows are read only where the
table above holds them …", replace its last five lines with:

pact and holds a pipe is refused the same way: one written under the
table, a fenced or commented example, or a row of the table whose item says
`pact notify`, `**Pact notify**` or `` `Pact` ``. Keep both rows in that
table. A sentence with no pipe in it may name the pact freely, which is why
this section is written without one: this file can be copied whole.
```
```python
# tests/test_a_signatory_declares_its_pact.py —
# test_the_template_and_the_config_skill_carry_both_rows_and_the_vocabulary:
# the template now documents each row as a bullet, the skill as a table cell
    for row in (config.PACT_ROW, config.PACT_NOTIFY_ROW):
        assert f"**`{row}`**" in template, row
        assert f"| `{row}` |" in skill, row


# test_s12_the_documents_say_a_pact_row_is_read_in_one_spelling: replace the
# "template: no pipe" sentence with
            "A sentence with no pipe in it may name the pact freely",


# after test_s9_the_vendored_copy_reads_the_silent_set_as_the_table_says
def test_s4_the_template_copied_whole_is_silent():
    """Round 1 of PR #793, yellow 1. `skills/commit-pr-convention/SKILL.md`
    tells a session to copy `templates/config.md` into the root whole, and
    the file the plugin ships a template for must not be the file that
    breaks the check: no pact and no refusal, to either reader."""
    with open(os.path.join(ROOT, "templates", "config.md"), encoding="utf-8") as f:
        text = f.read()
    assert config.pact_declaration(text) == ([], None, [])
    assert ec.notify_may_be_always(text) is False
```
```python
# hooks/config.py — directly above PACT_WORD
# An HTML table cell, which GFM passes through and github.com renders as a
# cell: a file holding one may carry a value on a line with no `|`, so there
# every line naming a pact is read without the pipe condition (round 1 of
# PR #793, yellow 2). `evidence_check.py` holds the same pattern.
HTML_CELL = re.compile(r"<t[dh][\s/>]", re.I)


# hooks/config.py — pact_lines_not_read: after
#     taken = {index: item for index, item, _value in rows}
    piped = HTML_CELL.search(text) is None
# and replace `elif names_a_pact(line):` with
        elif names_a_pact(line, piped):
```
```python
# skills/evidence-check/scripts/evidence_check.py — directly above PACT_WORD
# `hooks/config.py#HTML_CELL`, copied for a copy with no `hooks/`.
HTML_CELL = re.compile(r"<t[dh][\s/>]", re.I)
# notify_may_be_always: its loop is in 🟡 3's fence, which carries `piped`.
```
```markdown
docs/the-pact.md, after "A line with no `|` has no value cell, so the pact
can be named in prose." — add:

In a file that holds an HTML table cell, `<td>` or `<th>`, a line naming a
pact is refused with or without a `|`, because such a cell carries a value
with no pipe beside it.
```
```python
# tests/test_a_signatory_declares_its_pact.py — after `ec = _vendored_checker()`
@pytest.mark.parametrize(
    "below, lines",
    [
        (
            "\n<table><tr><td>Pact notify</td><td>always</td></tr></table>\n",
            ["<table><tr><td>Pact notify</td><td>always</td></tr></table>"],
        ),
        (
            "\n<table>\n<tr>\n<td>\nPact notify\n</td>\n<td>always</td>\n</tr>\n</table>\n",
            ["Pact notify"],
        ),
    ],
    ids=["one line", "the item on a line of its own"],
)
def test_s2_a_pact_row_in_an_html_table_is_refused(below, lines):
    """Round 1 of PR #793, yellow 2. cmark-gfm passes an HTML table through,
    and its cell carries a value with no `|` beside it."""
    assert config.pact_declaration(CONFIG + below) == (
        ORDERS,
        None,
        [refused(x) for x in lines],
    )
    assert ec.notify_may_be_always(CONFIG + below) is True
```
```python
# skills/evidence-check/scripts/evidence_check.py — notify_may_be_always:
# replace from `valued = set()` through `if names_a_pact(line):` with
    valued = set()
    lines = gfm_lines(said)
    piped = HTML_CELL.search(said) is None
    for at, line in enumerate(lines):
        # A row-shaped line directly above a delimiter row is a table's
        # header: a transposed table names the item there and the value
        # below, so it is read whole (round 1 of PR #793, yellow 3).
        header = at + 1 < len(lines) and RULE_LINE_RE.match(lines[at + 1].strip())
        plain = line.splitlines() == [line] and not header
        match = CONFIG_ROW_RE.match(line) if plain else None
        if match is None:
            if names_a_pact(line, piped):
                return True
            continue


# and in its docstring replace the paragraph beginning "Where the plugin
# refuses and this copy does not" with
    Where the plugin refuses and this copy does not, nothing can mean
    `always`: a plain `Pact` row outside the table, a plain row with no
    value, a `Pact` row written twice, a plain `Pact notify` row with no
    `Pact` value, or a two-cell row whose item names no pact, whose value
    this copy does not read as the plugin does not read a walked row's. A
    table's header is read whole, because a transposed table puts the item
    there. An empty value is the default, and a notify row with no `Pact`
    value is ignored (round 2 of PR #756, yellow 2; round 1 of PR #793,
    yellow 3).
```
```python
# tests/test_a_signatory_declares_its_pact.py — after `ec = _vendored_checker()`
@pytest.mark.parametrize(
    "below",
    [
        f"\n| Pact | Pact notify |\n|---|---|\n| {URL} | always |\n",
        "\n| Mode | Pact notify |\n|---|---|\n| shared | always |\n",
    ],
    ids=["Pact first", "another item first"],
)
def test_s9_a_transposed_table_is_read_whole_by_the_vendored_copy(below):
    """Round 1 of PR #793, yellow 3. A table whose header names the rows and
    whose body holds the values is refused by the plugin; the copy reads its
    header whole, so it cannot rule `always` out either."""
    header = below.split("\n")[1]
    assert config.pact_declaration(CONFIG + below)[1:] == (None, [refused(header)])
    assert ec.notify_may_be_always(CONFIG + below) is True
```
```markdown
skills/evidence-check/SKILL.md:339 — replace "or carries any other line the
plugin's reader refuses for naming a pact outside its one spelling" with
"or carries a line naming a pact that is neither plain row, a two-cell row
other than a table's header being read by its item alone"

docs/the-pact.md:327 — replace "holds a line that names a pact by the
plugin's word and is neither row in the one spelling" with "holds a line
that names a pact by the plugin's word and is neither row in the one
spelling, reading a two-cell row other than a table's header by its item
alone, as the plugin reads a walked row"

The `Corrected ·` row for C1 takes the same clause in place of "and is
neither a plain … nor a plain … row by `CONFIG_ROW_RE`".
```

## Executed probes

| What was run | Result |
|---|---|
| `pact_declaration` (head and base) and `notify_may_be_always` over `templates/config.md` whole, and filled with a `Pact` URL and `always` | head: seven refusals, `notify` None, copy blind; base: `([], None, [])`; filled: base `always`, head `None` with seven |
| The writer end to end, a moved row citing no clause, `seal/config.md` = the template, base checker and head checker | base exit 0, re-stamped; head exit 1, `LEFT … may be always … will not read` |
| 352 placements of every spelling in #784's four round reports, plus the eight splitlines-only characters at every position of a plain notify row | every one refused or read `always`, and the copy blind on every refusal; two defaults were my mistranscription of `Pact&nbsp notify` |
| Spellings outside #784: fullwidth, mathematical bold, a combining accent, Cyrillic `а`, small capitals, three Hangul fillers, `P<b></b>act` | first three refused; the rest read the default (⬜ 6 and the documented side) |
| HTML table, three shapes, both readers; cmark-gfm with raw HTML kept | default and copy not blind on all three; cmark-gfm renders a second table with the cells |
| The writer end to end with an HTML table row under a `Pact` value | exit 0, re-stamped, no `seal/pact-changes/` (🟡 2) |
| Transposed tables, four shapes, both readers; the vendored writer and the plugin writer end to end on the first | plugin refuses all four; copy not blind on three; vendored writer exit 0 re-stamped with no record, plugin writer exit 1 (🟡 3) |
| Must-not lines under a `Pact` value, and this repository's `seal/config.md` | all silent; piped prose naming `pact-check`, `pacts` or `seal/pact.md` refuses, as designed |
| 60,000 random configs from 21 fragment lines, plugin against the copy | plugin `always` and copy not blind: 0; plugin refuses and copy re-stamps: six refused-line kinds, only the transposed header able to show `always` |
| 20,000 random texts, summed `splitlines` pieces per GFM line against `text.splitlines()` | 0 mismatches |
| The three fences applied in-process: the template rewrite, the HTML-cell condition, the header condition; the silent set, S9 (b)'s verdicts and the 1,751 S2 texts | template silent in both readers and `always` when filled; HTML shapes refused and blind; transposed shapes blind; S9 (b) unchanged; 0 of 1,751 missed |
| The full suite, the repository-wide lint and the typecheck | not yet — the sealer's single run after the rounds settle; nothing in this round stands in for it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
