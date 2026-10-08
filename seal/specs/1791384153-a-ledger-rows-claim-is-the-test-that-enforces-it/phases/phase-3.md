# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 4b5eef0c |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

One resolver (`spec.md` D6): `fold_check.py#target_problem` loads
`evidence_check.py` through `load` and asks it; its `ast.walk` branch is
removed; S10's method spelling; the pins in
`tests/test_a_folded_statement_names_what_enforces_it.py` updated in the
same commit; the targets under `docs/` measured green by `fold-check`, and
that module red with the old resolver restored.

## What this phase found

**The resolver `fold_check.py` asks is `named_unit`, phase 1's**, loaded
lazily through a fourth loader beside `reader()`, `optin()` and
`config_reader()`, so a copy of the script taken alone still names the
sibling it misses first (`hooks/optin.py`), which
`test_a_script_copied_on_its_own_says_which_sibling_it_misses` pins. What
`fold-check` accepts stays its own: any `def` or `class`; a constant, which
`named_unit` also knows, is refused as before.

**One `ast.parse` stays, and it resolves nothing.** `named_unit` answers
None for a file that will not parse, and `fold-check`'s refusal names the
line (`SyntaxError at line 1`, pinned by
`test_a_target_file_that_will_not_parse_exits_2_naming_it`). The line
number is the exception's, so the parse runs only on that path, to name it.
`test_the_target_is_resolved_by_the_ledgers_reader` pins that no `ast.walk`
is left in the script.

**Measured over the tree:** `bin/fold-check` read 171 statements in 18
documents under `docs/`, bound all 171, and exited 0 — the same answer it
gave before, which is what `spec.md`'s "0 are nested" predicted: the move
from *a name anywhere in the file* to *a qualified name where it is
defined* changes no target the tree holds.

**What the move does change, stated:** a bare name that only exists nested
(`path::test_b` for a method) no longer resolves for `fold-check` either,
which is S10's other half and the ledger's rule; the detail is unchanged,
*no def or class named test_b in tests/test_x.py*.

**Seen red (§15), through `bin/mutation-check` against 4b5eef0c:** the old
`ast.walk` resolver put back in place of `named_unit` turned both method
cases red; accepting any kind turned the constant case red; dropping the
parse that names the line turned the SyntaxError case red.

Executed, output read: the fold module, 34 passed; the eight modules that
load or name `fold_check.py`
(`test_a_document_has_room_for_the_next_fold`,
`test_a_reference_root_is_read_and_never_taken`,
`test_a_script_copied_alone_exits_2`,
`test_a_script_says_which_interpreter_it_needs`,
`test_both_editions_carry_the_same_folds`, `test_docs_line_wrap`,
`test_every_reader_ends_a_line_where_gfm_does`,
`test_the_settings_have_a_front_door`), 314 passed; `uvx ruff check` and
`uvx ruff format --check` on both files.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `fold_check.py#target_problem`'s `ast.walk` over every node of a target file | `skills/evidence-check/scripts/evidence_check.py#named_unit`, the one resolver of `path::name` |
