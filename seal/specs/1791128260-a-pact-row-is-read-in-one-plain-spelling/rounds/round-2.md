# 1791128260-a-pact-row-is-read-in-one-plain-spelling — review round 2

| Field | Value |
|---|---|
| Target SHA | 8c33fad349b9b48fb9ac246c4d3670186c5a4c00 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #793 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `ec5d32377ab4367166736b3fd99d625f90be7cde..e6173ed68762d8555f14e928b1ad253cc73b60aa`, 3 commits |
| Contract changes | pact_line_refusal → pact_declaration; refused → round-1-report.md, round-1.md, pytest |
| New units | DELIMITER_ROW (depth 1); DELIMITERS (depth 1); WALKER_DELIMITERS (depth 1); IN_A_CELL_FILE (depth 1) |
| Needs a fix | yes — 🟡 1 (the vendored copy re-stamps unrecorded under a transposed table whose delimiter row lacks an outer pipe), 🟡 2 (a `<td>` anywhere refuses every pipe-less pact sentence while the template says they are free) |
| Loses a record or crashes | yes — under 🟡 1 the vendored writer re-stamps a moved row citing no clause at exit 0 and records no pact change, where the rendered table says `Pact notify` is `always` (executed) |

- [x] Pass

## What this round was asked

Round 2 of the #759 redesign (PR #793), the verifying round, at 8c33fad3: open round 1's fixes (range 182cde3a..1b159dd0) and judge whether each closes its finding with no regression — the template's §Pact rewritten pipe-free (silent read whole, `always` when filled, every reader of the template whole); `HTML_CELL` dropping the pipe condition in both readers and what it newly refuses; the vendored copy reading a header line whole and the plugin-always-implies-copy-blind property re-fuzzed; the wording fixes and the YAML-front-matter clause; the survivors rows and re-reads.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Round 1's yellow 3 holds only where a transposed table's delimiter row has both outer pipes: under `---\|---`, `--- \| ---`, `\|---\|---`, `---\|---\|` or `:--\|--:` the vendored copy reads the header by its item alone, is not blind, and its writer re-stamps a moved row at exit 0 with no pact change where the plugin refuses | `skills/evidence-check/scripts/evidence_check.py:3798` | **fixed** `8f64f7c4` | fixed at 8f64f7c4 — the vendored header test reuses the GFM walker's own rule, `hooks/config.py#DELIMITER_ROW` plus a pipe in the line (outer pipes each optional, at most three spaces in), copied as `evidence_check.py#DELIMITER_ROW` and held equal in S10; `DELIMITERS`, 320 delimiter lines built by construction (outer pipe each side optional, one or two cells, `-`/`---`/`:--`/`--:`/`:-:`, padded or not, indent none/three/four/tab), holds the copy blind exactly where the walker reads a delimiter row (S9 (b), both directions), every walker-accepted one is a transposed `STRAY_WAYS` row, and the vendored writer runs `---\|---` end to end. Round 1's 60,000-config property re-run: 0 cases of plugin `always` with the copy not blind; with the property widened to cmark-gfm's rendered cells (a rendered `Pact` value beside a rendered `Pact notify`/`always`), 0 at the head and 142 at 8c33fad3; executed: cmark-gfm renders all five as a table with `Pact notify` over `always`; the copy is not blind on any of the five; vendored writer exit 0, re-stamped, no `seal/pact-changes/` at three spellings; plugin writer exit 1 at four. With the fence applied all seven spellings are blind, the fuzz has zero cases of plugin `always` with the copy not blind, and the two modules pass (1962) |
| 🟡 2 | `HTML_CELL` is searched over the whole file, so a `<td>` in a comment, a code span or a fenced example refuses every pipe-less line naming a pact, which is 32 lines of the template copied whole. The template still says a sentence with no pipe may name the pact freely, `docs/the-pact.md` says "an HTML table cell", and no refusal names the tag | `templates/config.md:432` | **fixed** `8f64f7c4` | fixed at 8f64f7c4 — `templates/config.md` and `docs/the-pact.md` say an HTML table cell's tag anywhere, a comment, code span or fence included, refuses a pipe-less sentence (the template writes it as a `td` or `th` opened with a `<`), pinned; the refusal sentence adds "this file holds an HTML table cell's tag, so a line with no `\|` is refused too" on exactly the lines the pipe condition alone would not refuse, pinned in S2's HTML rows and the S6 writer row; 25215898 adds the mixed row that holds the clause to those lines only; executed: template plus a `<td>` in a comment gives 32 refusals and `notify` None; prose with a `<td>` code span gives one; a fenced `<td>` example gives one; `<td>` with no pact prose is silent. With the fence applied the template is silent and `always` when filled, and the pins, the wrap test and the identifier test pass (2003) |
| ⬜ 3 | The YAML front matter clause says no line of it holds a `\|`; a YAML block scalar's indicator is one, and such a line naming a pact is refused | `docs/the-pact.md:347` | **fixed** `8f64f7c4` | fixed at 8f64f7c4 — the YAML clause reads "a line of it naming a pact is refused only where it holds a `\|`", pin moved; executed: `Pact notify: \|` over `  always` refused by the plugin, copy blind; `notes: \|` beside `Pact notify: always` silent. The behaviour is right and the sentence is wrong |
| ⬜ 4 | The O3 row's Evidence still says "eleven pinned sentences" after the fix range grew the S12 pins from 9 to 12 | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:14` | answered | corrected at e6173ed6: O3's evidence counts the pins it rests on (13 in S12, 2 in the writer's documents case) and says which were seen red against which commit; O2 and the C1 `Corrected ·` row state the round-2 rules; the moved rows were re-read with `--reverify --into`; a correction to the run's paperwork, not a fix. Executed: the pins counted at both ends of the range; the three new pins fail with `docs/the-pact.md` at 182cde3a |
| 🟢 | round 1's yellow 1 is closed — the template copied whole is silent in both readers and reads `always` once filled, and the bullets keep every fact the two tables and the fence carried | `templates/config.md:389` | confirmed | executed: `([], None, [])` and copy `False`; filled, `always` and copy blind. Read: the pull-request-language test reads only the language row, `seal mode` writes `NEW_CONFIG` (executed silent), and the config skill copies only the Broad gate block |
| 🟢 | round 1's yellow 2 is closed for every HTML table shape tried | `hooks/config.py:666` | confirmed | executed: ten shapes (one line, a cell per line, the item on its own line, upper case, attributes, attribute after a newline, attribute after a tab, `<th/>`, unclosed cells, Markdown inside a cell) refused and the copy blind; `<thead>` and `<tdx>` silent. What it newly refuses is yellow 2 of this round |
| 🟢 | round 1's white 4 is closed — the documents state the vendored rule as the code reads it | `skills/evidence-check/SKILL.md:339` | confirmed | read: both documents, the docstring and the C1 row say a two-cell row other than a table's header is read by its item alone; "a table's header" becomes exact under yellow 1's fence of this round |
| 🟢 | round 1's white 5 is closed — the C1 `Corrected ·` row carries the item-alone clause, the header exception and the HTML-cell clause | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:5` | confirmed | read; `evidence-check --strict` exit 0 at the target |
| 🟢 | round 1's white 6 is closed — own-script look-alikes, the NFKC fold and a small-capital row | `docs/the-pact.md:337` | confirmed | read; the three new pins fail against 182cde3a's document (executed) |
| 🟢 | the plugin reading `always` still implies the copy is blind | `skills/evidence-check/scripts/evidence_check.py:3761` | confirmed | executed: 60,000 random configs over 32 fragment lines, transposed, HTML and pipe-less-delimiter shapes among them; zero counterexamples |
| 🟢 | the survivors rows, the re-stamped fragment rows and the new P3 re-read stand | `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/survivors.md` | confirmed | executed: `evidence-check --strict` exit 0; `survivor-check --range 94d7b2e0..8c33fad3` exit 0 with and without `--exempt`. Read: both quotes stand beside dated corrections; the released P3 claim holds of the bullets |
| carried | round 1's confirmations of the #784 spellings, the must-not set and the walk-index mapping | `tests/test_a_signatory_declares_its_pact.py` | confirmed | carried from round 1: the fixes touch neither `PACT_WORD` nor the walk, and the S2 corpus passed in this round's narrow run; this repository's config and `NEW_CONFIG` executed silent |

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `templates/config.md:389` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/config.py:922` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3781` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/SKILL.md:339` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:5` | round 1's ⬜ 5 — answered |
| round-1 | `docs/the-pact.md:337` | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_a_signatory_declares_its_pact.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:686` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3757` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:913` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-pact.md:91` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
