# 1791128260-a-pact-row-is-read-in-one-plain-spelling — review round 2 report

Ran by: specseal:warden on claude-opus-5-5
Target SHA: 8c33fad349b9b48fb9ac246c4d3670186c5a4c00 (PR #793, draft)
Base: `release/v0.18.2` at 94d7b2e0
Round 1's fix range: `182cde3a..1b159dd0`, four commits; New unit `HTML_CELL`
Kind of round: verifying. The target is round 1's fix diff, not the branch.

## What this round was asked

Open round 1's fixes and judge whether each closes its finding with no
regression: the template rewrite of yellow 1 against every reader of the
template whole, the file-wide `HTML_CELL` condition of yellow 2 for the shapes
it closes and what it newly refuses, the vendored copy's header rule of yellow
3 for transposed tables and the plugin-reads-`always`-implies-copy-blind
property, whites 4-6 and the YAML front matter clause, the survivors rows, the
re-stamped fragment rows and the new P3 re-read.

## How the round was run

The repository was cloned with `git clone --no-local` into this round's
scratch directory, the clone was checked out at 8c33fad3, and every probe ran
there. What follows separates what was executed from what was read.

The implementer's account was read in full. It is round 1's record, the four
fix commits' messages, the `overview.md`, `spec.md`, `plan.md` and
`questions.md` corrections, and the ledger fragment. Each claim in it was
checked against the code or a probe below. The commit messages add nothing
beyond their subjects ("Round 1 of PR #793, yellow 1-3"). The record's
Grounds cells are the account. Its executed claims were re-run where this
round could re-run them.

## Summary

Three causes, three outcomes:

1. Round 1's yellow 3 named one delimiter spelling, `|---|---|`, and the fix
   recognises only that one. GFM accepts a delimiter row without its outer
   pipes. Under those spellings the vendored writer still re-stamps a moved
   row with no record at exit 0. This is 🟡 1, and it is the same class as
   round 1's yellow 3.
2. Round 1's yellow 2 is closed for every HTML table shape I tried. Its
   condition is a token that applies to the whole file. A `<td>` in a comment
   or a code span therefore refuses every pipe-less sentence naming a pact,
   which is 32 lines of the template copied whole. The template still tells
   its reader that such a sentence is free, and no refusal names the tag that
   caused it. This is 🟡 2.
3. Two sentences of paperwork are wrong: the YAML clause (⬜ 3) and the O3
   ledger row's executed count (⬜ 4).

Round 1's yellow 1 and whites 4-6 are closed, and the property "the plugin
reads `always` ⇒ the copy is blind" still holds over 60,000 random configs.

## 🟡 1 — A transposed table whose delimiter row lacks an outer pipe still re-stamps unrecorded under the vendored copy

`skills/evidence-check/scripts/evidence_check.py:3798` decides that a line is
a table's header with `RULE_LINE_RE`, `^\|[\s:|-]+\|$`. That pattern requires
a pipe at both ends. GFM does not. Its delimiter row's outer pipes are
optional. Executed through `tests/gfm_table_oracle.py`: cmark-gfm renders
`| Mode | Pact notify |` over `---|---`, `--- | ---`, `|---|---`, `---|---|`
and `:--|--:` as a table, with header `Mode | Pact notify` and body
`shared | always`.

Under each of those five delimiter rows the vendored copy reads the header by
its item alone. The item, `Mode`, names no pact, so the copy is not blind. The
plugin refuses the header line, so the two readers diverge exactly where
round 1's yellow 3 said they did. Executed end to end with the S9 fixture: at
`---|---`, `--- | ---` and `:--|--:`, the vendored `--reverify` exits 0,
re-stamps the moved row citing no clause and creates no
`seal/pact-changes/`. The plugin's writer exits 1 with a `LEFT` line on all
four spellings tried. The `|---|---|` case, round 1's, exits 1 under both.

Why it matters: the rendered table tells a person that `Pact notify` is
`always`. Under the vendored checker a moved row is then stamped and no pact
change reaches the pact's repository. That is the record round 1 counted as
lost, under a spelling one character away.

The documents already describe the wider rule. `docs/the-pact.md:327`,
`skills/evidence-check/SKILL.md:339`, the C1 `Corrected ·` row and the
function's own docstring each say "a table's header" or "a delimiter row",
not "a delimiter row with both outer pipes". The fix below makes the code
match them, so no sentence needs to change.

Executed with the fix applied in the clone: all seven delimiter spellings
blind; the 60,000-config fuzz still has zero cases of the plugin reading
`always` with the copy not blind; the two pact modules 1962 passed; ruff check
and ruff format clean on the three files. The two proposed cases were seen
red at the target first: the S9 corpus case and the new end-to-end row
failed.

## 🟡 2 — A `<td>` anywhere in the file refuses every pipe-less sentence naming a pact, and the template still says such a sentence is free

`hooks/config.py#HTML_CELL` is searched over the whole text. Its comment says
it "fails closed, refusing more where it is wrong". That is the right
direction for the reader, and it is not where this finding sits. The finding
is about what the person writing a config is told.

Executed:

- `templates/config.md` whole reads silent, as yellow 1 asked. With a `<td>`
  inside an HTML comment appended, the plugin's reader returns 32 refusals
  and `notify` None. The refused lines include `## Pact`, the template's own
  bullets and its *What no row governs* entries.
- A config with a `Pact` value and a prose line "We never write a `<td>`
  here. The orders pact is held elsewhere." gives one refusal. So does a
  fenced `html` example holding `<td>x</td>` above a pipe-less sentence
  naming the pact.
- A config holding `<td>` and no prose naming a pact stays silent.

Each refusal names the pipe-less line and offers two remedies: write it as a
row, or take it out of the file. Neither remedy names the `<td>` that caused
it. The template, which `skills/commit-pr-convention/SKILL.md:78` says is the
document a config's author reads, says at `templates/config.md:432` that "A
sentence with no pipe in it may name the pact freely". In such a file that
sentence is false. `docs/the-pact.md:93` states the condition as "a file
that holds an HTML table cell". A reader does not take a code span or a
comment to be an HTML table cell.

Why it matters: such a person sees `pact-check` exit 2 and the writer leave
every moved row. They are told to delete lines the template wrote and
documented as free, and nothing points them at the one tag that matters.

Not a loss of record: the reader fails closed, and the writer leaves the rows
rather than re-stamping them.

The fix is to the two sentences and their pins, not to the code. **The
template must not spell the tag with its `<`**: `<td>` written into
`templates/config.md` would itself make every template copy refuse its own
§*Pact*. The fence below writes it as "a `td` or `th` opened with a `<`".
Executed with the fence applied: the template still reads silent in both
readers and `always` when filled; the two pact modules,
`tests/test_docs_line_wrap.py` and `tests/test_no_real_identifiers.py`, 2003
passed.

An alternative was not built. The refusal sentence could name the tag when
`HTML_CELL` is what dropped the pipe. That is a change to what a person sees,
so §14 asks for its pin. I left it to the smith's judgment, and the fence
does not depend on it.

## ⬜ 3 — The YAML front matter clause gives a reason that is not true of YAML

`docs/the-pact.md:347` says front matter "is not read either: … and no line
of it holds a `|`". A YAML block scalar is introduced by a `|`. Executed:
`Pact notify: |` over `  always` in front matter is refused by the plugin and
the copy is blind. `notes: |` in front matter beside `Pact notify: always` is
silent, which is the documented default. The behaviour is right and the
stated reason is wrong. That makes this ⬜, and the fix is a fence.

## ⬜ 4 — The O3 ledger row's executed count is the count before round 1's pins

`seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:14`, the
O3 row, was rewritten in the fix range to cover the NFKC fold, the HTML-cell
rule and the template's silence. Its Evidence cell still reads "each of the
eleven pinned sentences deleted once under `mutation-check`". The S12 case's
parameter list grew from 9 to 12 in the fix range (executed: counted at
182cde3a and 8c33fad3). This is the run's paperwork, a correction and not a
fix: update the count. Evidence for the three new pins exists. Executed in
this round: with `docs/the-pact.md` restored to 182cde3a, the NFKC, HTML-cell
and YAML pins all fail.

## Round 1's findings, answered

- **Yellow 1, closed.** Executed: the template whole gives `([], None, [])`
  to the plugin's reader and `False` to the copy, and `always` with the copy
  blind once both rows are filled. Read: the bullets carry every fact the two
  removed tables and the fence carried, which is the URL with its example,
  `;`, both Absent clauses, the refused-not-absent sentence and the three
  values with what each records and how it is read. The fence's two-row shape
  is now shown by the template's own top table, which the new sentence points
  at. Every other reader of the template whole was opened.
  `tests/test_the_pull_request_language_is_the_repositorys.py:294` copies it
  and reads only the language row. `seal mode` writes its own stub,
  `NEW_CONFIG`, which is executed silent, and does not copy the template.
  `skills/config/SKILL.md` points at the template and copies only the Broad
  gate block, which `test_s4_the_configs_this_plugin_writes_or_copies_are_silent`
  holds.
- **Yellow 2, closed for the shapes.** Executed: ten HTML shapes refused with
  `notify` None and the copy blind. They are one line, a cell per line, the
  item on a line of its own, `<TH>`/`<TD>` upper case, attributes, an
  attribute after a newline, an attribute after a tab, `<th/>`, unclosed
  cells, and Markdown inside a cell. `<thead>` and `<tdx>` stay silent. What
  it newly refuses is 🟡 2.
- **Yellow 3, not closed for the class.** That is 🟡 1.
- **Whites 4, 5 and 6, closed.** Read: both documents, the docstring and the
  C1 row state the item-alone rule with the header exception, and given 🟡
  1's fix they match the code. The blind-side paragraph names own-script
  look-alikes and the NFKC fold, and the small-capital row is in `BLIND_SIDE`.
- **Round 1's green verdicts.** The fuzz was re-run at the target: 60,000
  configs over 32 fragment lines, which include the transposed, HTML and
  pipe-less-delimiter shapes. The plugin read `always` with the copy not blind
  zero times. This repository's `seal/config.md` and `NEW_CONFIG` are silent.
  The #784 spellings and the walk-index mapping were carried and not
  re-executed. The fixes touch neither the word nor the walk, and their cases
  passed in this round's narrow run.
- **The survivors rows, the re-stamped rows and the new P3 re-read.**
  Executed: `evidence-check --strict` exit 0, and `survivor-check --range
  94d7b2e0..8c33fad3` exit 0, with and without `--exempt`. Read: both
  survivors quotes stand in the files they name, beside dated corrections.
  The new P3 re-read cites
  `tests/test_a_signatory_declares_its_pact.py#test_the_template_and_the_config_skill_carry_both_rows_and_the_vocabulary`.
  The released P3 claim ("documents both rows, their vocabulary and their
  defaults in `## Pact`") still holds of the bullets.
- **§15 for round 1's new cases.** Executed: with `hooks/config.py`,
  `evidence_check.py`, the template, `docs/the-pact.md` and the skill
  restored to 182cde3a, 18 cases of the two modules fail, and every new case
  of the fix range is among them or inside the S9 corpus case that failed.

## Regression tests to plant

- `tests/test_a_signatory_declares_its_pact.py`, `STRAY_WAYS`, the
  transposed-table generator: two rows with a delimiter row lacking an outer
  pipe. Seen red at the target through
  `test_s9_the_vendored_copy_cannot_rule_always_out_on_any_s2_text`.
- `tests/test_a_signatory_records_a_pact_change.py`,
  `test_s9_a_vendored_copy_leaves_where_the_plugin_refuses_a_pact_line`: one
  end-to-end row, `---|---`. Seen red at the target with exit 0.
- `tests/test_a_signatory_declares_its_pact.py`, the S12 pins: the template's
  new HTML-tag sentence, plus the two reworded `docs/the-pact.md` sentences.

## Facts for the evidence ledger

- GFM's delimiter row needs no outer pipe. cmark-gfm renders a two-cell header
  over `---|---`, `--- | ---`, `|---|---`, `---|---|` and `:--|--:` as a
  table. Executed 2026-10-05 through `tests/gfm_table_oracle.py`.
- `HTML_CELL` matches anywhere in the text, in a comment, a code span and a
  fence included. Executed 2026-10-05.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Round 1's yellow 3 holds only where a transposed table's delimiter row has both outer pipes: under `---\|---`, `--- \| ---`, `\|---\|---`, `---\|---\|` or `:--\|--:` the vendored copy reads the header by its item alone, is not blind, and its writer re-stamps a moved row at exit 0 with no pact change where the plugin refuses | `skills/evidence-check/scripts/evidence_check.py:3798` | open | executed: cmark-gfm renders all five as a table with `Pact notify` over `always`; the copy is not blind on any of the five; vendored writer exit 0, re-stamped, no `seal/pact-changes/` at three spellings; plugin writer exit 1 at four. With the fence applied all seven spellings are blind, the fuzz has zero cases of plugin `always` with the copy not blind, and the two modules pass (1962) |
| 🟡 2 | `HTML_CELL` is searched over the whole file, so a `<td>` in a comment, a code span or a fenced example refuses every pipe-less line naming a pact, which is 32 lines of the template copied whole. The template still says a sentence with no pipe may name the pact freely, `docs/the-pact.md` says "an HTML table cell", and no refusal names the tag | `templates/config.md:432` | open | executed: template plus a `<td>` in a comment gives 32 refusals and `notify` None; prose with a `<td>` code span gives one; a fenced `<td>` example gives one; `<td>` with no pact prose is silent. With the fence applied the template is silent and `always` when filled, and the pins, the wrap test and the identifier test pass (2003) |
| ⬜ 3 | The YAML front matter clause says no line of it holds a `\|`; a YAML block scalar's indicator is one, and such a line naming a pact is refused | `docs/the-pact.md:347` | open | executed: `Pact notify: \|` over `  always` refused by the plugin, copy blind; `notes: \|` beside `Pact notify: always` silent. The behaviour is right and the sentence is wrong |
| ⬜ 4 | The O3 row's Evidence still says "eleven pinned sentences" after the fix range grew the S12 pins from 9 to 12 | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:14` | open | a correction to the run's paperwork, not a fix. Executed: the pins counted at both ends of the range; the three new pins fail with `docs/the-pact.md` at 182cde3a |
| 🟢 | round 1's yellow 1 is closed — the template copied whole is silent in both readers and reads `always` once filled, and the bullets keep every fact the two tables and the fence carried | `templates/config.md:389` | confirmed | executed: `([], None, [])` and copy `False`; filled, `always` and copy blind. Read: the pull-request-language test reads only the language row, `seal mode` writes `NEW_CONFIG` (executed silent), and the config skill copies only the Broad gate block |
| 🟢 | round 1's yellow 2 is closed for every HTML table shape tried | `hooks/config.py:666` | confirmed | executed: ten shapes (one line, a cell per line, the item on its own line, upper case, attributes, attribute after a newline, attribute after a tab, `<th/>`, unclosed cells, Markdown inside a cell) refused and the copy blind; `<thead>` and `<tdx>` silent. What it newly refuses is yellow 2 of this round |
| 🟢 | round 1's white 4 is closed — the documents state the vendored rule as the code reads it | `skills/evidence-check/SKILL.md:339` | confirmed | read: both documents, the docstring and the C1 row say a two-cell row other than a table's header is read by its item alone; "a table's header" becomes exact under yellow 1's fence of this round |
| 🟢 | round 1's white 5 is closed — the C1 `Corrected ·` row carries the item-alone clause, the header exception and the HTML-cell clause | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:5` | confirmed | read; `evidence-check --strict` exit 0 at the target |
| 🟢 | round 1's white 6 is closed — own-script look-alikes, the NFKC fold and a small-capital row | `docs/the-pact.md:337` | confirmed | read; the three new pins fail against 182cde3a's document (executed) |
| 🟢 | the plugin reading `always` still implies the copy is blind | `skills/evidence-check/scripts/evidence_check.py:3761` | confirmed | executed: 60,000 random configs over 32 fragment lines, transposed, HTML and pipe-less-delimiter shapes among them; zero counterexamples |
| 🟢 | the survivors rows, the re-stamped fragment rows and the new P3 re-read stand | `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/survivors.md` | confirmed | executed: `evidence-check --strict` exit 0; `survivor-check --range 94d7b2e0..8c33fad3` exit 0 with and without `--exempt`. Read: both quotes stand beside dated corrections; the released P3 claim holds of the bullets |
| carried | round 1's confirmations of the #784 spellings, the must-not set and the walk-index mapping | `tests/test_a_signatory_declares_its_pact.py` | confirmed | carried from round 1: the fixes touch neither `PACT_WORD` nor the walk, and the S2 corpus passed in this round's narrow run; this repository's config and `NEW_CONFIG` executed silent |

## Executed probes

| What was run | Result |
|---|---|
| The repository's runner on `tests/test_a_signatory_declares_its_pact.py` alone, at the target | 1847 passed |
| `pact_declaration` and `notify_may_be_always` over transposed tables under seven delimiter spellings, two headers each | plugin refuses all 14; copy blind only under `\|---\|---\|` and `\| :-: \| --- \|` |
| cmark-gfm through `tests/gfm_table_oracle.py` on the five pipe-less or one-pipe delimiter spellings | each renders a second table, `Mode \| Pact notify` over `shared \| always` |
| The plugin's and the vendored writer end to end on four delimiter spellings, a moved row citing no clause | vendored: exit 1 at `\|---\|---\|`; exit 0, re-stamped, no `seal/pact-changes/` at `---\|---`, `--- \| ---`, `:--\|--:`. Plugin: exit 1 at all four |
| Ten HTML table shapes, plus `<thead>` and `<tdx>`, in both readers | ten refused with the copy blind; the two non-cells silent |
| The template whole, with a `<td>` in a comment, filled; prose with a `<td>` code span; a fenced `<td>` example; this repository's config; `NEW_CONFIG` | template silent and `always` when filled; with the comment, 32 refusals; prose 1; fence 1; repository config and stub silent |
| YAML front matter: a plain value, a block scalar naming a pact, a block scalar beside a plain value | default; refused with the copy blind; default |
| 60,000 random configs over 32 fragment lines, plugin against copy, at the target and with 🟡 1's fence applied | plugin `always` and copy not blind: 0 both times |
| The two pact modules with `hooks/config.py`, `evidence_check.py`, the template, `docs/the-pact.md` and the evidence-check skill restored to 182cde3a | 18 failed, among them every case the fix range added |
| 🟡 1's fence applied: its cases first against the target code, then with the code change | 2 failed (the S9 corpus case, the new end-to-end row), then 1962 passed; ruff check and format clean |
| 🟡 2's and ⬜ 3's fence applied, with the two pact modules, the docs wrap test and the identifier test | 2003 passed; template still silent |
| S12 parameter count at 182cde3a and 8c33fad3 | 9 and 12 |
| `evidence-check --strict`; `survivor-check --range 94d7b2e0..8c33fad3` with and without `--exempt` | exit 0; exit 0; exit 0 |
| The full suite, the repository-wide lint and the typecheck | not yet. That is the sealer's single run after the rounds settle, and nothing in this round stands in for it |

## Paste-ready fixes

```python
# 🟡 1 — skills/evidence-check/scripts/evidence_check.py, directly below HTML_CELL
# A GFM delimiter row, outer pipes optional: `RULE_LINE_RE` asks for both,
# and GFM renders a table under `---|---` too (round 2 of PR #793, yellow 1).
DELIMITER_ROW_RE = re.compile(r"^\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)+\|?$")


# notify_may_be_always: replace
        header = at + 1 < len(lines) and RULE_LINE_RE.match(lines[at + 1].strip())
# with
        header = at + 1 < len(lines) and DELIMITER_ROW_RE.match(lines[at + 1].strip())
```

```python
# 🟡 1 — tests/test_a_signatory_declares_its_pact.py, STRAY_WAYS, inside the
# transposed-table generator's tuple, after the "another item first" entry
            # Round 2 of PR #793, yellow 1: GFM asks for no outer pipe on a
            # delimiter row.
            (
                "a delimiter row with no outer pipes",
                "| Mode | Pact notify |",
                "| Mode | Pact notify |\n---|---\n| shared | always |\n",
            ),
            (
                "a delimiter row with one outer pipe and colons",
                "| Pact | Pact notify |",
                f"| Pact | Pact notify |\n|:-- | --:\n| {URL} | always |\n",
            ),


# 🟡 1 — tests/test_a_signatory_records_a_pact_change.py,
# test_s9_a_vendored_copy_leaves_where_the_plugin_refuses_a_pact_line:
# append to its `below` list
        "\n| Mode | Pact notify |\n---|---\n| shared | always |\n",
# and to its ids
        "round 2 of PR #793, yellow 1: a delimiter row with no outer pipes",
```

```markdown
🟡 2 — templates/config.md, §Pact, the paragraph ending "this file can be
copied whole." Replace its last line with these four (no `<` beside the tag
name, or the template would hold the tag it warns about):

this section is written without one: this file can be copied whole. A file
that also holds an HTML table cell's tag, a `td` or `th` opened with a `<`,
anywhere, a comment or a code span included, refuses such a sentence too, so
keep that tag out of this file.
```

```markdown
🟡 2 — docs/the-pact.md, §How a signatory names the pact: replace from
"with no `|` has no value cell" to the end of that paragraph with

with no `|` has no value cell, so the pact can be named in prose. In a file
that holds an HTML table cell's tag, `<td>` or `<th>`, anywhere, a code span,
a fence or a comment included, a line naming a pact is refused with or without
a `|`, because such a cell carries a value with no pipe beside it; take the tag
out to name the pact in prose again. A refusal leaves `Pact notify` with no
value, so `evidence-check --reverify` leaves every moved row it cannot rule
out, `pact-check` exits 2, and a signatory's CI prints a notice.
```

```markdown
⬜ 3 — docs/the-pact.md, §What this does not see: replace

not read either: github.com shows it as a table, cmark-gfm does not, and no
line of it holds a `|`. Catching these would need a grammar of GFM's markup or
a table of look-alike letters, and leaving both out is what keeps the rule one

with

not read either: github.com shows it as a table, cmark-gfm does not, and a
line of it naming a pact is refused only where it holds a `|`. Catching these
would need a grammar of GFM's markup or a table of look-alike letters, and
leaving both out is what keeps the rule one
```

```python
# 🟡 2 and ⬜ 3 — tests/test_a_signatory_declares_its_pact.py,
# test_s12_the_documents_say_a_pact_row_is_read_in_one_spelling's parameters.
# Replace the HTML-cell pin's sentence with
            "In a file that holds an HTML table cell's tag, `<td>` or `<th>`, "
            "anywhere, a code span, a fence or a comment included, a line naming a "
            "pact is refused with or without a `|`, because such a cell carries a "
            "value with no pipe beside it; take the tag out to name the pact in "
            "prose again.",
# the YAML pin's sentence with
            "YAML front matter is not read either: github.com shows it as a table, "
            "cmark-gfm does not, and a line of it naming a pact is refused only "
            "where it holds a `|`.",
# add after the "template: no pipe" entry
        (
            ("templates", "config.md"),
            "A file that also holds an HTML table cell's tag, a `td` or `th` opened "
            "with a `<`, anywhere, a comment or a code span included, refuses such a "
            "sentence too, so keep that tag out of this file.",
        ),
# and to the ids, after "template: no pipe"
        "template: an HTML table cell's tag, round 2 of PR #793",
```

```markdown
⬜ 4 — seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md,
the O3 row's Evidence cell: replace "each of the eleven pinned sentences" with
the count the row's three cited cases now pin, and cite round 2 of PR #793
for the three pins added in round 1's fix pass (seen red against 182cde3a's
`docs/the-pact.md`).
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (the vendored copy re-stamps unrecorded under a
transposed table whose delimiter row lacks an outer pipe), 🟡 2 (a `<td>`
anywhere refuses every pipe-less pact sentence while the template says they
are free)

Loses a record or crashes: yes — under 🟡 1 the vendored writer re-stamps a
moved row citing no clause at exit 0 and records no pact change, where the
rendered table says `Pact notify` is `always` (executed)

The broad gate has not come due: this round leaves two findings open.

## Proof block

Files opened at 8c33fad3 in the clone:

- `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/rounds/round-1.md`
- the fix-range diff of `hooks/config.py`, `skills/evidence-check/scripts/evidence_check.py`,
  `skills/evidence-check/SKILL.md`, `templates/config.md`, `docs/the-pact.md`,
  `tests/test_a_signatory_declares_its_pact.py`, `tests/test_a_signatory_records_a_pact_change.py`,
  `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/{overview,plan,questions,spec,survivors}.md`
  and `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md`
- `hooks/config.py` lines 640-960 (`PACT_WORD`, `HTML_CELL`, `names_a_pact`,
  `pact_declaration`, `pact_lines_not_read`, `pact_line_refusal`)
- `skills/evidence-check/scripts/evidence_check.py` lines 3305-3345 and 3700-3850
- `templates/config.md` lines 370-440
- `docs/the-pact.md` lines 86-96 and 343-352
- `tests/test_a_signatory_declares_its_pact.py` lines 175-215, 362-385, 690-710 and 880-905
- `tests/test_a_signatory_records_a_pact_change.py` lines 1612-1667
- `tests/test_the_pull_request_language_is_the_repositorys.py` lines 275-320 and 1200-1240
- `tests/test_the_mode_is_a_row_and_a_command.py` lines 1240-1270
- `skills/commit-pr-convention/SKILL.md` lines 70-90
- `tests/gfm_table_oracle.py` lines 1-110
- `seal/releases/0.18.0.md`, the P3 row

The probes, their fixtures and the clone were removed at the end of the
round.
