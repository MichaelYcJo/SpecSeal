# Implementation Plan: a pact row is read in one plain spelling (#759, redesigned)

<!-- seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-05 by the orchestrator under the owner's `automation` routing and the owner's redesign choice, when `smith` was spawned.

## Summary

`hooks/config.py#pact_declaration` reads a pact row in one spelling: a row
the table walk takes whose item is exactly `Pact` or `Pact notify`. Any other
line that names a pact is refused. On a row the walk took, only the item is
read. On any other line, the whole line is read, and it must hold a `|` to be
refused. "Names a pact" is one regular expression, `PACT_WORD`, read over the
line as written and as two standard-library calls decode it. No GFM grammar
is emulated. The vendored copy uses the same constant and predicate.
The three callers gain a case each. Three documents say it.

## Technical context

Read at framing at the base `94d7b2e0` and on #784's branch
`origin/fix/759-a-pact-row-outside-the-config-table-is-refused` (`b16cee46`).
Coordinates are units, not lines.

- `hooks/config.py#config_rows` is the walk (#82). It runs `unfenced`
  (#429, #667) over `text.splitlines()`, `CONFIG_ROW` per line, and stops at
  the first non-row after a row. `#pact_declaration` filters its rows by
  exact item and refuses a doubled `Pact`, a doubled notify, a bad entry and
  an out-of-vocabulary notify. `#declared_pacts` is the strict file read for
  `pact-check`.
- `hooks/blocks.py#gfm_lines` is the GFM line cut, held to GFM's line endings
  by `tests/test_every_reader_ends_a_line_where_gfm_does.py`.
  `evidence_check.py#gfm_lines` is its copy.
- `evidence_check.py#record_pact_changes`, plugin branch.
  `blind = declared is None or declared[1] in (None, NOTIFY_ALWAYS)`, and
  `refused and unknown` leads to `LEFT` and exit 1. So a refusal with
  `notify` None already leaves every moved row, and no code changes there.
- The same function's vendored branch (`config is None`) matches
  `NOTIFY_ROW_SHAPE` over `said.splitlines()`. It is blind where both
  `pact` and `pact notify` were named.
- `chain_check.py` prints each refusal after "a `Pact` row this CI does not
  verify: ". `pact_check.py` prints `REFUSED <url> seal/config.md <refusal>`.
- On #784's branch, two pieces are worth porting:
  - `hooks/config.py#indexed_config_rows`, with `config_rows` as its
    projection;
  - `#stray_refusal`'s rendering of a line, with non-space whitespace and Cf
    characters shown as `<U+XXXX>`.

  Its tests hold the corpora: `STRAY_WAYS`, `SPLITLINES_ONLY`,
  `FORMAT_CHARACTERS`, `WRAPS`, `JOINS`, `SPLITS`, `MARKUP` and the
  code-span rows in `tests/test_a_signatory_declares_its_pact.py`, and the
  writer, vendored, `pact-check` and `chain-check` cases in the three other
  pact modules. Round 4's spellings were never planted. They are in
  `rounds/round-4-report.md`, under findings 🟡 1–4.

**The scan, as pseudocode.** The builder owns the code.

```
rows  = indexed_config_rows(text)                 # [(index, item, value)]
taken = {index: item for index, item, _ in rows}
for each GFM line L of text (gfm_lines), with the splitlines indices it covers:
    if L holds no splitlines-only character and its one index is in taken:
        item = taken[index]
        if item in (PACT_ROW, PACT_NOTIFY_ROW):  continue        # the plain spelling
        if word(item):                            refuse(L)       # a walked row, item read alone
    elif names_a_pact(L):                         refuse(L)       # any other line, whole
names_a_pact(L) = ("|" in L or "|" in D) and (word(L) or word(D))
word(s)         = PACT_WORD.search(s) is not None
D               = unicodedata.normalize("NFKC", html.unescape(L))
PACT_WORD       = re.compile(r"(?<![^\W\d_])p[\W\d_]*a[\W\d_]*c[\W\d_]*t", re.I)
```

For a walked row, `word(item)` reads the item raw and decoded, as
`names_a_pact` does. The pipe condition does not apply there, because a
walked row has its pipes.

**What breaks in six months.**

- **A spelling of the blind side** (`spec.md` §*What this does not catch*)
  reaches somebody's config. It reads as the default, as today. The
  document names it, so it is a known limit and not a surprise. Q1 is where
  the owner can widen it.
- **A signatory writes a commented-out pact row with a pipe.** It is
  refused, and `--reverify` leaves every moved row until the comment goes.
  The refusal names the line, so the cost is one edit.
- **A future row's item or a user's own row's item starts with the word.**
  Such an item is refused. Today no item the plugin reads does. A new
  plugin row named that way would meet S4's silent set and the shipped
  configs' case first.
- **Someone ports a markup rule "to be more precise".** That brings back the
  #784 loop. S2's "every member refuses" is easy to keep green with
  fail-closed rules and hard to keep green with a grammar. That asymmetry
  is the guard.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #784: emulate GFM's rendering of the item (`shape_line`, NAME NOT IN TREE) and hold it to cmark-gfm | Four rounds each found more spellings missed: no leading pipe, Cf, markup, entities, code spans, five raw HTML kinds, link destinations, `<!-->`, legacy entities. The class is GFM's whole inline grammar | rejected by the owner, 2026-10-05 |
| The spawn's example: any line whose letters (non-alphanumerics removed) contain `pact` | `impact` and `compact` refuse anywhere in the file, values of walked rows included. `P&#97;ct` is missed, because the reference leaves digits | rejected; the look-behind, the decode union and the item-only read on walked rows fix all three |
| No `\|` condition: refuse every line naming a pact | A signatory's comment or paragraph mentioning its pact refuses, and `--reverify` leaves every moved row | rejected. GFM gives a pipe-less line no value cell, so excluding it loses nothing. Q2 measures that |
| Exempt fenced and commented lines, as #784 did | The refusal then depends on `hidden_lines` matching GFM's block grammar. That is modelling again, and an unclosed fence hides everything below it | rejected; read through, and the example refuses |
| Refuse a mangled `Pact notify` line only where a `Pact` value stands, as #784 did | Telling a mangled notify line from a mangled `Pact` line needs the item read through markup | rejected; both refuse. A plain notify row with no pact is still ignored |
| Strip `<…>` and `(…)` crudely before matching, to catch `P<b></b>act` | Each crude strip is a union, so it can only add refusals. But it is a third and fourth transform for spellings no round found, and it starts the grammar again | not built; the blind side is documented, and Q1 can ask for it |
| Keep the vendored constant's name `NOTIFY_ROW_SHAPE` so the released anchor 0.18.1 C1 resolves | The name then says "row shape" over a word pattern, in the one file a vendoring repository reads | rejected; the constant is renamed `PACT_WORD`, and a `Corrected ·` row re-points C1 |
| Make the plugin's reader silent on `templates/config.md` | It needs a code-span exemption, which is the very rule #784 rounds 2–4 kept re-opening, for a file no code reads as a config | rejected |

## Phases

Vertical slices. Each phase ends with something runnable and verified. The
narrow runs are each phase's own modules. The broad gate is the sealer's.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The reader.** `PACT_WORD`, the predicate, `indexed_config_rows` (ported) with `config_rows` its projection, and the scan and refusal sentence in `pact_declaration`. Reader cases S1–S5 in `tests/test_a_signatory_declares_its_pact.py`, the S2 corpus generated from #784's generators plus round 4's spellings. The census entry. Q2 and Q3 measured and recorded | `tests/test_a_signatory_declares_its_pact.py` and the census module at the head. S2, S3's first case and S5 seen red against the base's `pact_declaration` (§15) | 7a5aca9e |
| 2 | **The callers.** S6 writer case, S7 `pact-check` case, S8 `chain-check` case, each end to end and seen red at the base. No caller code changes | the three modules at the head; red at the base | e2f81bdb |
| 3 | **The vendored copy.** `PACT_WORD` and the predicate in `evidence_check.py` replace `NOTIFY_ROW_SHAPE`. The vendored branch reads `gfm_lines` and applies the blind rule (`spec.md` Scope 2). S9 and S10 | `tests/test_a_signatory_records_a_pact_change.py`'s vendored cases and S10. The corpus members the old shape misses are seen red at the base. Every base vendored case passes unchanged | 829cc442 |
| 4 | **The documents and the ledger.** The `docs/the-pact.md` §*How a signatory names the pact* paragraph and `Enforced by:` line. The vendored paragraph's rule and blind side. `templates/config.md` §*Pact*'s refused-row paragraph and `Absent` cell. S12 pins. The ledger fragment's re-reads and the `Corrected ·` row for 0.18.1 C1. The changelog fragment | S12 pins seen red with each sentence deleted. `evidence-check` names no unread drift in this item's scope. S11's modules at the phase boundary | bc2cd870 |

**Phase 1 is the whole decision. Phases 2–4 are its consequences.** That
order is deliberate. Q2 or Q3 can only change phase 1, and both are answered
inside it.

## Operational impact

- **Newly refused** in any signatory, and in any repository whatever:
  - a line of `seal/config.md` that names a pact, holds a `|`, and is not a
    walked row with the plain item. That includes fenced and commented
    examples, and a plain row written below the table's end;
  - a walked row whose item names a pact in another spelling.

  In each case `pact-check` exits 2 at the pact's repository, `chain-check`
  prints a notice, and `evidence-check --reverify` leaves every moved row at
  exit 1 until the line is fixed.
- **No longer refused**, compared with #784's unmerged branch only (the base
  never refused these): nothing. Every spelling #784 refused is refused
  here.
- **The vendored copy** is blind on more configs: any with a mangled pact
  line. Every config it re-stamped on before still re-stamps.
- No migration, no new dependency, no new environment variable. `html` and
  `unicodedata` are the standard library. `hooks/config.py` is loaded by a
  `PreToolUse` hook, so the two imports belong inside the function that uses
  them, or at module level only if measured cheap (the builder's call).
