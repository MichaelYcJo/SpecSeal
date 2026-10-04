# 1791119073-a-pact-row-outside-the-config-table-is-refused — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | cf4be3a7 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The reader. In `hooks/config.py`: an index-carrying walk with `config_rows`
projected from it, byte-identical output; the shape constant, word for word
the vendored `NOTIFY_ROW_SHAPE`; stray detection on both cuts inside
`pact_declaration`, before its `not value` return; the refusal sentence;
`notify=None`. A stray `Pact notify` refuses only where a `Pact` value stands,
and a stray `Pact` always refuses. Cases S1–S8 and S14 in
`tests/test_a_signatory_declares_its_pact.py`, each seen red at the base
first, and the census entry updated. Q2 measured here.

## What this phase found

**The frame holds.** Every coordinate `spec.md` and `plan.md` name was
opened before the first edit: `config_rows`' arms (W1–W9 read off them as
the table says), `unfenced` and `hidden_lines`, `pact_declaration` and its
`not value` return, the vendored branch's `NOTIFY_ROW_SHAPE` and its
`said.splitlines()`, `blocks.gfm_lines`, and the census row for
`config_rows`. Nothing in them disagrees with the frame.

**The walk is `indexed_config_rows`, and the stray finder is
`stray_pact_rows`.** `config_rows` keeps its docstring and becomes one line.
The census entry for `config_rows` moved to `indexed_config_rows`, and
`stray_pact_rows` takes a new one with two calls, both reason `F`: the
reader's cut, and each GFM line split into the reader's pieces of it.
`text.splitlines()` is the concatenation of every `gfm_lines(keepends=True)`
line's own `.splitlines()`, because LF, CR and CRLF end a line for both, so
counting each GFM line's pieces gives every piece its reader index with no
offset arithmetic.

**A GFM line is hidden only where every piece of it is.** `walk_text` gives
the pieces of one GFM line one answer except where the walk is unsure, so the
two readings differ only there, and the cautious one is the one that refuses
more.

**The refusal sentence, and the one thing it adds to the frame's shape.**

`` `<line>` is shaped as a `<item>` row and is not read as one, because it
stands outside the `| Item | Value |` table, spells the item another way, or
holds a character that cuts the line. Write it as `| <item> | … |` inside
that table ``

It names the line stripped, and shows every whitespace character other than a
space as `<U+XXXX>`. Without that, W9's no-break space and every W11 line
print as a correct row next to a sentence saying the row is wrong. The
sentence avoids a dash and a semicolon of its own because the writer's `LEFT`
line puts ` — ` and `; ` after it (Q3, phase 2).

**`len(pieces) < 2` was a guard nothing stood behind.** A one-piece GFM line
is the reader's own line: it was taken, was already a stray, or does not
match. Its mutant would survive, so `cf4be3a7` removed it.

**Q2: no.** The phase-boundary run of the four pact modules,
`test_the_mode_question_is_asked_once.py`,
`test_the_seal_is_taken_once_by_the_sealer.py` and the census module passed,
862 cases, with no fixture changed, at `4cfd4a7e`. At `cf4be3a7` the four
modules `plan.md` names for this phase passed again, 713 cases. `templates/config.md` and this
repository's `seal/config.md` read with no refusal, and a case now holds that
(`test_the_shipped_configs_hold_no_stray_pact_row`).

**Seen red.** Against `94d7b2e0`'s `hooks/config.py`, 32 of the new reader
cases fail. S1–S5 fail on the assertion, and S14 and the walk's projection
case fail because the names do not exist yet. The 15 that pass there (S6,
S7, S8 and the shipped configs) are guards, and each was seen red by a
`mutation-check` break instead: M1 (refuse a stray notify with no pact)
turns S6 red; M2 and M12 (hidden lines read) turn S7's fence and comment red;
M3 (the GFM pass ignores taken pieces) and M9 (pieces never advance) turn S8
red. In all, thirteen breaks of phase 1's units went red and none survived.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `config_rows`' own walk | `hooks/config.py#indexed_config_rows`, which `config_rows` now projects, docstring unchanged |
| The census row `("hooks/config.py", "config_rows")` | `("hooks/config.py", "indexed_config_rows")` in the same table |
