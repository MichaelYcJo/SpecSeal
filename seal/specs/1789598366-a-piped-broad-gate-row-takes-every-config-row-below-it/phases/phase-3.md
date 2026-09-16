# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | <pending> |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

Close the fourth copy of the loop. `tests/test_the_pull_request_language_is_the_repositorys.py`
reimplemented `hooks/config.py#config_rows` rather than calling it, and its
callers now read through the one reader. The identity assertion is
`__code__.co_filename`, the way
`tests/test_the_mode_question_is_asked_once.py#test_the_command_and_the_gate_read_one_parser`
already asserts it for `seal.py`: a module loaded under a name of its own is
a different module object with the same code, so an import check alone would
not see a copy return.

## What this phase found

**The copy agreed with the production reader right up to the commit that
moved one.** Phase 1 taught `config_rows` markdown's escape; the copy in that
test file did not learn it, and from that commit until this one the two
readers answered differently about the same input. Nothing in the suite would
have said so — which is the case this phase adds, and it is why closing the
copy belongs in this branch rather than staying the standing deferral it was.

**The deferral is closed where it was opened.**
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/overview.md`'s
`## Not verified` table carried it with the repository owner as answerer. The
row is marked ✅ with what closed it and stays in place; the count
`unverified-check` reads is the number of rows, so a closed row is marked and
never deleted.

**Two ledger rows anchor on `#items`, and both were re-read rather than
re-pointed.** `seal/ledger.md`'s S8 and the `🟡 6 / 🟡 5` row cite it as a code
ground. The anchor still resolves — the name is now an alias — and both
claims are about the parser's BEHAVIOUR, which is unchanged and still covered
by every case cited beside them. So each carries a re-read note saying the
implementation moved, rather than a new coordinate. Nothing was swept: the
only rows touched are the ones this phase actually drifted.

**The two stop rules moved into the implementation's docstring.** They were
documented in the copy, in comments written by the two review rounds of #82
that found them — round 1 🟡 6, a row of a different shape skipped as though
it were not there; round 2 🟡 5, a header and a separator stepped past
wherever they appeared. Removing the copy would have removed the only written
record of why either rule exists, so both are now in
`hooks/config.py#config_rows`. A third ledger row's Notes cell said *a third
copy of the loop exists … out of scope here*; that sentence is now history and
says so.

**`re` left the test module's imports.** Nothing else in the file used it, so
the copy going took the import with it. Worth recording only because it is
what made the phase's own mutation fail as a collection error the first time:
putting the copy back needs its import back too.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tests/test_the_pull_request_language_is_the_repositorys.py`'s `HEADER`, `ROW`, `SEPARATOR` and the body of `items` — the fourth copy of the loop | `hooks/config.py#config_rows`, which the name `items` now aliases. The two stop rules' reasoning moved into that function's docstring |
| the `import re` at the top of that module | nowhere — nothing else in the file used it |
