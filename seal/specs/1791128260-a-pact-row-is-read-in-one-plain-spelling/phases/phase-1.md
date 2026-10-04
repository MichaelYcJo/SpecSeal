# 1791128260-a-pact-row-is-read-in-one-plain-spelling — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 7a5aca9e |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The reader. In `hooks/config.py`: `PACT_WORD`, the predicate, #784's
`indexed_config_rows` ported with `config_rows` as its projection, and the
scan and refusal sentence inside `pact_declaration`. The accepted spelling is
a walked row whose item is byte-exactly `Pact` or `Pact notify`; the refusal
is any other `gfm_lines` line naming a pact (raw or `NFKC(html.unescape)`)
with a `|`, fences and comments read through, and only the item of a walked
row read. No GFM emulation. Reader cases S1–S5, the S2 corpus generated from
#784's generators (`STRAY_WAYS`, the S3 rows, `FORMAT_CHARACTERS`,
`SPLITLINES_ONLY`, `MARKUP` = `WRAPS` × items + `JOINS` + `SPLITS`, the
code-span rows) plus round 4's spellings, with no cmark oracle case. The
census entry. Q2 and Q3 measured and recorded, Q4 decided.

## What this phase found

**The frame holds.** Every coordinate the spec and plan name was opened
before the first edit: `config_rows` and `unfenced` at the base,
`pact_declaration`'s returns, `blocks.gfm_lines`, the vendored branch and
`NOTIFY_ROW_SHAPE`, the three callers' prefixes (`chain_check.py`,
`pact_check.py`'s `REFUSED … seal/config.md — `, the writer's `LEFT` line),
and #784's branch at `b16cee46`. Nothing in them disagrees with the frame.

**The units.** `PACT_WORD`; `names_a_pact(text, piped=True)`, one predicate
for both readings, where `piped=False` is the walked-row item check the plan's
pseudocode calls `word(item)`; `indexed_config_rows`; `pact_lines_not_read`,
the scan; and `pact_line_refusal`, #784's `stray_refusal` rendering under the
new sentence. The scan counts each GFM line's `str.splitlines` pieces to find
its walk index, the way #784 did, so it needs no offset arithmetic. The two
standard-library imports sit inside the two functions that use them:
measured with `python3 -X importtime`, `html` costs about 1 ms beyond `re`
(which this module already loads) and `unicodedata` 0.5 ms, and a `PreToolUse` hook that loads
this module never reads a pact.

**Q2: the pipe condition stands.** Through `tests/gfm_table_oracle.py#rows_under`
at the pinned cmark-gfm, `Pact notify always`, `Pact notify: always` and
`Pact notify` directly under a two-column table each render a second cell of
`''`. So did `Pact notify &#124; always`, `Pact notify \| always` and
`Pact notify ｜ always` (fullwidth): one cell, the value empty. Those three
are refused here anyway, by the decoded union or the raw `|`. That is the
loud direction, and it costs a person nothing they meant to write. A
`` `Pact notify | always` `` line renders two cells, and it is refused too.

**Q3: no existing case changed verdict.** The four pact modules,
`test_the_mode_question_is_asked_once.py`,
`test_the_seal_is_taken_once_by_the_sealer.py`, the census module, and the
other modules that build a `seal/config.md` naming a pact
(`test_a_pact_review_takes_a_pact_change.py`,
`test_the_settings_have_a_front_door.py`,
`test_a_reference_root_is_read_and_never_taken.py`) all passed at `b0207eaa`
with no fixture changed: 1807, 154, 617 and 51 cases. No fixture holds a line
naming a pact with a pipe that is not a plain walked row.

**Q4: the sentence.** The frame's text with one change. "the one spelling
read" became the whole of the claim, and the sentence keeps the frame's two
remedies:

`` `<line>` names a pact and is not a `Pact` or `Pact notify` row in the one spelling read: write it as `| Pact | … |` or `| Pact notify | … |` inside the `| Item | Value |` table, or take it out of this file ``

It opens with the quoted line and ends with no full stop, so it reads after
`chain-check`'s "a `Pact` row this CI does not verify: " (which appends
". Printed rather than refused"), after `pact-check`'s `REFUSED <url>
seal/config.md — `, and after the writer's "the `Pact` rows will not read: ".
Phase 2 pins it in all three.

**Every spelling #784 found refuses here.** The S2 corpus is 1,751 cases of
the reader module: `STRAY_WAYS`, 41 (#784's 25 and its S1 row, plus round
4's five backtick rows off the walk, #784's S8 two-plain-rows line at each
of the eight `str.splitlines`-only characters, which #784 read and this
reader refuses whole, and the two decoded-pipe lines); `SPLITLINES_ONLY` inside a row, 8; and
`OTHER_ITEMS`, 1,702, in the table and below a blank line: #784's S3 rows, its
code-span rows, every Cf character at three places, and `MARKUP`. `WRAPS`
gained round 4's seven link spellings (yellow 1), its two empty comments
(yellow 2), and `JOINS` its legacy-entity joins `&`, ` &` and `&nbsp `
(yellow 3). `SPLITS` gained `P&#x61;ct notify`. #784's must-not spellings
(`Pact notify 2`, `Pacts notify`, …) refuse as well, which is the rule: they
name a pact.

**Seen red (§15).** With `94d7b2e0`'s `hooks/config.py` in place, the new
cases at `b0207eaa` gave 1,755 failed and 8 passed. Every S2, S3-with-no-pact, S5 and
ordering case failed, and the projection case failed on the missing name.
The 8 that pass at the base are S1, S3's plain notify with no pact, and S4:
guards that must keep passing. Each was seen red by a `mutation-check`
break instead. Thirteen breaks of this phase's units, each red, none
survived:

| Break | Cases run | Red |
|---|---|---|
| M1 `PACT_WORD` without its look-behind | S4 lines | 1 |
| M2 `PACT_WORD` with nothing allowed between the letters | S2 items | 340 |
| M3 the decoded line not searched | S2 items | 4 |
| M4 the pipe condition off | S4 lines | 2 |
| M5 a decoded pipe not counted | `STRAY_WAYS` | 2 |
| M6 a cut line read as a walked row | `STRAY_WAYS` | 8 |
| M7 the plain items not exempt | S1 | 1 |
| M8 a walked item read with the pipe condition | S2 items | 849 |
| M9 `notify` kept where a line is refused | `STRAY_WAYS` | 40 |
| M10 Cf characters not shown as code points | S2 items | 1022 |
| M11 the walk's index off by one | the projection case | 1 |
| M12 no refusal added | `STRAY_WAYS` | 41 |
| M13 a line off the walk not read | `STRAY_WAYS` | 41 |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `config_rows`' own walk | `hooks/config.py#indexed_config_rows`, which `config_rows` now projects; the stop rule's docstring stays on `config_rows` |
| The census row `("hooks/config.py", "config_rows")` | `("hooks/config.py", "indexed_config_rows")` in the same table, beside the new `pact_lines_not_read` row |
