# 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | dac51971 |
| Ran by | unknown — the spawn prompt did not name the agent and model, and the orchestrator that chose them is the one to fill this row |

## What this phase was asked

Widen the repository case to `tests/` and fix every test site it names, 302
by the census, with `Image.open` classified in `ALLOWED` plus whatever W2
finds. Apply the edits with a script written by the `Write` tool and run by
path, never a heredoc, then `ruff format` the touched files. The walker at
zero is the proof. See the widened case red first, run each edited module
narrowly, and measure M1's test half.

## What this phase found

**M1, test half: 302, equal to the census.** Widened at `eba7ed15`, the
repository case went red naming 302 sites in 45 files: 236 `.write_text()`,
33 `.read_text()`, 18 `subprocess.run(text=)`, 13 `open()`, 1
`subprocess.Popen(text=)`, 1 `<expr>.open()` with a mode that is not a
literal. M1 is answered in both halves, 29 and 302, so the census's
name-matching approximation and the walker's import resolution counted the
same tree the same way.

**W2: none.** No test site uses the locale's default on purpose. Every module
that exercises a console or a locale (`test_console_is_not_utf8.py`,
`test_the_ledger_cases_hold_under_a_latin_1_locale.py`, `test_arm_check.py`'s
cp1252 case) drives it through a subprocess environment and names its own
reads, and none of their calls was among the 302.

**The edit script took its positions from the walker's own AST**, by byte
offset (an AST column is a UTF-8 byte count, and these files carry `—` and
`·`). It inserted `, encoding="utf-8"` after a call's last argument, or into
an empty argument list, and replaced a literal `text=True` keyword's span
with `encoding="utf-8"`, as phase 1 did under `.github/scripts/`. It asserted
each `text=` value was a literal `True` and each span read back as
`text=True`, and that every file's edit count equalled the walker's site
count for it. It refused any other shape. 301 edits in 44 files, then
`ruff format` reformatted 20 of them where a call crossed 88 columns.

**One `ALLOWED` row**:
`tests/test_the_release_seal_is_drawn.py#test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted`,
PIL's `Image.open`, which has no text mode and no encoding to name.

**`conftest.py` was one of the 44**, at `_build_repo`'s fixture write, so
every module in the suite imports an edited file. The narrow run covered the
44 edited modules (2324 passed, 79 skipped), and the suite as a whole is
`unverified`, answerer the sealer.

**Mutated once each, all red**: re-excluding `tests/` from the corpus (the
`ALLOWED` row's liveness half catches it, since its unit leaves the corpus),
pointing the `ALLOWED` row at another unit (the repository case names the
site again), and un-naming one test site (`conftest.py`'s fixture write).

**No rider drifted.** `rider_check.py` over the tree: 20 ok, 0 drifted, 0
broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the module's `NOT_YET_JUDGED` constant and the `skip` parameter, which kept `tests/` out of phase 1's corpus | none — the corpus is every tracked `.py`, which `tracked_python`'s docstring now says |
