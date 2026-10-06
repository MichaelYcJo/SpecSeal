# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 27365f10 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Phase 1 only, in a segment of about 25 minutes before the session moved
machines: measurements Q-M1 and Q-M2 first, then the recorder
(`spec.md` Scope 1) in `skills/verify/scripts/pytest_record/`, its
subprocess cases S1–S5 in
`tests/test_the_recorder_writes_what_its_process_ran.py`, and the three
structure modules a new shipped `.py` meets. Routing is `automation`, but
this segment stopped after smith: no warden, no sealer, no pull request, no
push, no full suite, no broad gate. Phases 2–4 belong to the next session.

## What this phase found

**Q-M1, measured: yes on all four.** A throwaway probe built a scratch
project (one passing and one failing test in `tests/test_a.py`, a module
that raises at import in `tests/test_b.py`), handed pytest the environment
of `spec.md` Scope 2 and ran
`python -m pytest -p no:cacheprovider --continue-on-collection-errors tests`
under `uvx --python 3.12 --with pytest==<v>` for `7.4.4`, `8.0.2` and
`8.1.2`, and under `--with pytest==9.1.1 --with pytest-xdist==3.8.0`. On each
build the `-p` in `PYTEST_ADDOPTS` loaded the recorder, exactly one record
file was written, `config.rootpath` and `config.invocation_params.dir` were
present, and every `test` and `collect` line's `path` existed on disk. The
recorder's `getattr` fallbacks (`config.rootdir`, `os.getcwd()`) are for
builds below 6.1 and were not exercised.

**Q-M2, measured: yes.** The same probe under `-n 2` on `9.1.1` with xdist
`3.8.0` wrote one record file, from the controller, holding every test line
and the collection error. **The collection error arrives once per worker**:
two identical `collect` lines for `tests/test_b.py` under `-n 2`. The reader
of phase 2 must treat a file's lines as a set, never count them. S4 asserts
the set, not the count.

**The rootdir pytest reports is already resolved.** On macOS the probe's
`mkdtemp` directory was `/var/folders/…` and every `rootdir` and `path`
pytest gave was `/private/var/folders/…`. `spec.md` Scope 3's `realpath` on
both sides is required, as it says; the cases compare `realpath`s for the
same reason.

**Exit codes and collection errors.** Without
`--continue-on-collection-errors`, a collection error interrupts the run
before any test runs. The cases pass the flag only where they need both
kinds of line (S4); phase 2's `NOT_REACHED` row is what covers a row that
does not pass it.

**Seen red (§15), each through `bin/mutation-check` against the committed
file, every verdict `red`:**

| Case | Break |
|---|---|
| S2 (`-s`, `-q`, `-n 2`) | `os.environ.pop(KEY_VARIABLE, None)` → `os.environ.get(KEY_VARIABLE)` |
| S3 | the claim-once swap `key, _unclaimed_key = _unclaimed_key, None` → `key = _unclaimed_key` |
| S1 | the test line's `path` → `""` |
| S4 | `pytest_collectreport` returns before writing |
| S5 (no directory) | the guard `if not key or not _directory` → `if not key` |

**Structure modules.** `shipped_python` and `LOADED` pick the recorder up
once it is tracked, and all three modules stay green. The recorder's
docstring names pytest builds by two components only (`7.4, 8.0, 8.1 and
9.1`), so no `VERSIONS_OF_ANOTHER_PRODUCT` exemption is needed for it. The
exact builds are in this record, under `seal/`, which `LOADED` does not read.
Q-W2 — whether the two `broad_gate.py` exemptions move or go — is therefore
still phase 2's, and the default "moved, keyed on the recorder's path" no
longer fits: the recorder carries no three-part token for an exemption to
name.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
