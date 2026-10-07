# 1791384156-config-rows-coordinates-and-headings-have-one-reader — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 456aa0af |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 1: `hooks/config.py` reads the file once and tells absent
from unreadable, and answers one item with a value, nothing, or a refusal
naming a doubled item; `declared_mode`, `reference_roots`, `declared_pacts`
and `pact_declaration` read through it, the pact reader's own doubled-row
sentences becoming the generic one's; `hooks/mode-gate.py#unreadable` · NAME NOT IN TREE
removed; `hooks/routing.py#parse` reads a doubled strict label as no
declaration and a doubled optional one as unanswered. Verified by S1's hook
half and S5, red first.

## What this phase found

**The names.** The file reader is `config_text(home)` → `(text, refusal)`;
the item reader is `config_value(text, item)` over text and `value_of(rows,
item)` over rows already walked, so `pact_declaration` walks once for two
items; `declared_value(home, item)` is the two together. The refusal
sentences are `unreadable_config(path, exc)` and `doubled_row(item, count)`.
`doubled_row` is the sentence `pact_declaration` already refused a doubled
`Pact notify` in, "`<item>` appears N times — one value", so the pinned
`Pact notify` sentences in `tests/test_pact_check.py` and
`tests/test_a_signer_records_a_pact_change.py` did not move. Phase 2's
command callers read through `config_text` and `value_of` (or their twins in
the vendored checker) and prefix the path themselves.

**`declared_mode` grew a fourth kind, `refused`, and that reached `seal mode`
at once.** `seal.py` re-exports `declared_mode`, and its report fell through
to the *they disagree* arm on the new kind. So the `seal.py` half of phase 2
— `table_span` returning every `Mode` row, `with_row`/`write_row` refusing
two of them by line, the refusal before a switch moves the folder, and
`mode_report`/`--check`/`--apply` reporting at exit 2 — was built here, in
the same commit as the reader. Phase 2 has the checker, `correction-check`,
`fold-check` and `broad-gate` left.

**Direction and prompt budget.** The hooks say nothing on a refusal: the
mode gate is silent on a doubled `Mode` row and on an unreadable file
(budget 0). The commit gate asks on a doubled strict `routing.md` label;
none of the 86 committed declarations holds one (measured by the existing
`test_the_template_and_the_committed_declarations_still_parse`, green), so
the budget on every existing work item is 0. `seal mode` refuses more, at
exit 2.

**Two older cases were superseded, not kept.**
`test_two_mode_rows_converge` · NAME NOT IN TREE (round 1 🟡 5 of #104) pinned that two runs over two `Mode` rows reach
agreement by setting the first; it is replaced by
`test_two_mode_rows_are_refused_naming_both_lines`. `test_a_row_that_cannot_be_written_still_reports`
(S2c of #104) pinned exit 0 for an unreadable `config.md`; it keeps its
report and now asserts exit 2 and the path. Both follow `spec.md` §*Scope* 1.
The bare-pipe limitation case, `test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe`,
still holds as it was: the person's row below a bare pipe is past the
table's end, so no walk counts it and nothing doubles.

**`reference_roots` reads a refusal as the default**, as an unreadable file
always read there. Its callers, `unverified-check` and the survivor sweep,
are not among the commands `spec.md` names as refusing, and no record is
written or lost on it. A mutation keeping the refusal out of the branch
survived as an equivalent mutant (a refusal carries no value), so the branch
went.

**Seen red (§15).** Every new case was run against 5623d728's three hooks and
`seal.py` with the new tests in place — `git stash push` of the source, run,
`git stash pop` — and failed: 15 in the first batch, the reference-root case
on its own, 7 in `tests/test_the_mode_is_a_row_and_a_command.py`.
`mutation-check`, every verdict `red` but one: `value_of`'s `len > 1` arm,
`config_text`'s `lexists` arm and its unreadable arm, `declared_mode`'s
refused arm, the gate's `"refused"` member, `parse`'s count filter,
`declared_pacts`' refusal arm, the doubled-`Pact` refusal, `doubled_modes`'
threshold, `write_row`'s own refusal (it SURVIVED the first pass, since every
command refuses before it; `test_the_writer_itself_refuses_two_mode_rows`
was added and it went red), the pre-move refusal, `mode_report`'s and
`--apply`'s refused arms, `table_span` keeping one row.

**The ledger.** `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md`
is the fragment's full name: the fold names a work item by its fragment's
file name (`.github/scripts/fold_ledger.py`), and every fragment in the
history carries the directory's whole id. Rows K1–K6 are this phase's; the
`Corrected · S7–S10` row re-points 0.9.1's mode-gate row, whose
`mode-gate.py#unreadable` coordinate went BROKEN; sixteen `Re-read ·` rows
were written by `--reverify --into` after each cited claim was read against
the unit it moved. 0.12.0's bare-pipe row still holds for its shape.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/mode-gate.py#unreadable` · NAME NOT IN TREE — the gate's second opening of `config.md` | `hooks/config.py#config_text` and `declared_mode`'s `refused` kind; the 0.9.1 row citing it is corrected in the fragment |
| `tests/test_the_mode_is_a_row_and_a_command.py::test_two_mode_rows_converge` · NAME NOT IN TREE | `test_two_mode_rows_are_refused_naming_both_lines` and `test_check_exits_2_on_two_mode_rows`, the rule reversed by `spec.md` §*Scope* 1 |
| `pact_declaration`'s own sentence for a doubled `Pact` (*list every pact in one row, separated by `;`*) | `hooks/config.py#doubled_row`, the one sentence, as `plan.md` phase 1 says |
