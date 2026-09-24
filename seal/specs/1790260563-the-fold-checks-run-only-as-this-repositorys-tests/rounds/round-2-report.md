# Round 2 report — 1790260563, the verifying round

Target SHA `ff3d26cd`. The surface is round 1's fix range `f181e30a..d32c365a`:
`0bbf219f` is code and tests, and `d32c365a` is the ledger fragment and one
`Enforced by:` line in `docs/the-evidence-ledger.md`. `ff3d26cd` adds the closed
round 1 record and nothing else. The work was done in a `git clone --no-local`
at the round directory under the scratchpad. Nothing in this round widened
beyond the fix range, and the new units named in the record's `New units`
row were judged as code.

## Summary

All eight of round 1's verdicts are closed. Each of the four yellows was
re-run against the fixed command and now gives the answer the orchestrator
decided: exit 2 for an unreadable target or document, exit 0 with one of two
sentences for a run with no rows, and a named reason at each `load` site.
All seven new cases, eight parametrised instances, fail against
`e9dfe623`'s `fold_check.py` and pass at the target. The no-root pin passes
both before and after, which is what it is meant to hold.

The new units opened four notes and nothing that needs a fix. Two are
sentences that come out wrong on an unusual input: `why` prints `line None`,
and the new "exists" arm is wrong on a case-insensitive filesystem. One is an
exit code that the module docstring, as this diff reworded it, now covers:
a missing sibling script exits 1. The last is a doubled "so" in the
opted-out sentence, which the new case pins as it stands.

## Round 1's verdicts — each re-derived

**Finding 1, a subdirectory run passes having checked nothing: closed.**
`main` at `skills/settle/scripts/fold_check.py:638` resolves the root through
`hooks/optin.py#repo_root` when `--root` is absent, and falls back to the
directory it was typed in where there is no repository. Executed: `bin/fold-check`
typed in the clone's `docs/` printed the same two lines as at the root (136
statements, 21 bound, 14 documents) and exit 0. It was typed in `docs/deep/` of a
planted repository whose rows live at the toplevel, and read those rows. An
explicit `--root docs/` stays literal, which matches the help text.

**Finding 2, a crash at exit 1 on an unparseable target or an undecodable
document: closed.** `target_problem` (`:271`) catches `OSError`, `ValueError`
and `SyntaxError` and raises `Unusable`. `shape_problems` (`:312`) prefixes
the statement. `read` (`:365`) raises `Unusable` for a document. `main` (`:666`)
holds the run's lines in a buffer and writes one stderr line at exit 2.
Executed, each exit 2 with nothing on stdout and no traceback: a target with
a syntax error, a target in Latin-1, a target with a null byte, a target
nested 5000 parentheses deep, a Latin-1 document from each check, and a
document at mode 000 (`PermissionError`).

**Finding 3, an opted-out repository is told it has no root: closed.**
`located` (`:451`) splits the two states `home_at` answers `""` for. Executed:
opted out with a `seal/` root present, with no flag, with `--ceiling 5` (the
not-declared line uses the opted-out sentence), and typed in `docs/`, each
with the opted-out sentence. A directory in no repository keeps the no-root
sentence.

**Finding 4, a listed file that exists is reported missing: closed.** The arm
at `:384` names an existing path as not a top-level `docs/*.md`. Executed with a
listed directory, `docs/deep`, which got the new sentence. It uses
`os.path.exists` rather than the `isfile` the paste-ready fix proposed, so a
listed directory is also named truthfully. That is an improvement on the
fence. See note 3 for the one input where the sentence is false.

**Note 5: closed.** The docstring at
`tests/test_a_folded_statement_names_what_enforces_it.py:16` now says "against
that row", and "that row" refers to the `Fold shape from` row named at `:11`.

**Note 6: closed.** `docs/the-evidence-ledger.md` names the real-tree case beside
`fold_check.py::bound`. Executed: `bin/fold-check` resolves both targets (the
statement is bound at the cutoff and reports no problem), and the line is an
`Enforced by:` line of targets, which the wrap skip covers.

**Note 7: closed.** All three `load` call sites pass their own purpose:
`reader` for the markers, `optin` for the root, and `config_rows` for the
rows. There are no other callers in the tree. Executed: the copied-alone case
names the resolver. See note 2 for its exit code.

**Note 8: closed.** The real-tree case walks `fold_check.documents(ROOT)` at
`:76`, and the removed module-level `DOCS` constant has no remaining reader.
Executed: the two modules pass.

## The new units, judged as code

- **`why`** returns `SyntaxError at line None` for a source holding a null
  byte, because Python 3.12's `ast.parse` raises that `SyntaxError` with no
  line. This is note 1. An `IndentationError` is reported as a `SyntaxError`,
  which is true because it is a subclass.
- **`optin`** loads the resolver once, and `main` and `located` share it.
  Nothing is wrong with it.
- **`located`** makes one `git_common_dir` call and passes it to `home_at`,
  so the answer and the opted-out test read the same directory. Its
  opted-out sentence is note 4.
- **`git_init`** follows the pattern the other `git init` cases in `tests/`
  use. `tests/conftest.py` empties the template directory and turns off
  auto-maintenance for every case, and this helper inherits both.
- **The seven new cases** were each red against `e9dfe623`'s script (executed:
  8 failed, 1 passed, the pass being the no-root pin). One is pinned more
  weakly than its neighbours: the copied-alone case asserts
  `returncode != 0` where the others assert a code (note 2).

Checked and not raised: a `seal/config.md` that is not UTF-8 is read as
declaring no rows, so the run says neither row is declared and exits 0. That
is the sentence the module's own docstring describes, and it is also how
`hooks/config.py` (`:403`) and `broad_gate.py` (`:600`) treat an unreadable
config. It is a convention of the tree, and this diff did not change it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed: typed in a subdirectory, the command reads the repository | `skills/settle/scripts/fold_check.py:638` | confirmed | executed: `bin/fold-check` in the clone's `docs/` gives 136 / 21 / 14 and exit 0; a planted repository typed in `docs/deep/` reads the toplevel's rows; the case is red at `e9dfe623` |
| 🟢 | round 1's finding 2 is closed: an unreadable target or document stops at exit 2 with one line and no traceback | `skills/settle/scripts/fold_check.py:271` | confirmed | executed: syntax error, Latin-1, null byte, deep nesting and mode 000 all give exit 2 with an empty stdout; three instances red at `e9dfe623` |
| 🟢 | round 1's finding 3 is closed: an opted-out repository is told so | `skills/settle/scripts/fold_check.py:451` | confirmed | executed with a `seal/` root present, with a flag, and typed in `docs/`; the case is red at `e9dfe623` |
| 🟢 | round 1's finding 4 is closed: a listed path that exists is not called missing | `skills/settle/scripts/fold_check.py:384` | confirmed | executed with a listed directory; the case is red at `e9dfe623`; note 3 is the one false input |
| 🟢 | round 1's note 5 is closed: the docstring names the row | `tests/test_a_folded_statement_names_what_enforces_it.py:16` | confirmed | read |
| 🟢 | round 1's note 6 is closed: the cutoff statement names the real-tree case | `docs/the-evidence-ledger.md:193` | confirmed | executed: `bin/fold-check` reports no problem for it |
| 🟢 | round 1's note 7 is closed: each `load` site names its purpose | `skills/settle/scripts/fold_check.py:141` | confirmed | read at three call sites; the case is red at `e9dfe623` |
| 🟢 | round 1's note 8 is closed: the real-tree case walks the command's own listing | `tests/test_a_folded_statement_names_what_enforces_it.py:76` | confirmed | executed: the two modules pass 60 cases |
| ⬜ 1 | `why` prints `SyntaxError at line None` for a target holding a null byte | `skills/settle/scripts/fold_check.py:361` | open | executed; exit 2 and the file are right, and only the reason reads badly |
| ⬜ 2 | a missing sibling script exits 1, which the reworded docstring now covers as exit 2, and the new case pins only `!= 0` | `skills/settle/scripts/fold_check.py:146` | open | executed: exit 1 with and without `--root`; the same `SystemExit(str)` is in `settle.py`, `chain_check.py` and `round_record.py`; only a copy taken out of the plugin reaches it |
| ⬜ 3 | on a case-insensitive filesystem a listing spelled `docs/A.md` for `docs/a.md` is called "not a top-level docs/*.md" | `skills/settle/scripts/fold_check.py:384` | open | executed on this macOS volume; the old "does not exist" was false there too |
| ⬜ 4 | the opted-out sentence reads "so its seal/config.md is not read, so nothing was checked" | `skills/settle/scripts/fold_check.py:469` | open | read; the new case pins the doubled "so" at `tests/test_a_document_has_room_for_the_next_fold.py:472` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_a_folded_statement_names_what_enforces_it.py` and `tests/test_a_document_has_room_for_the_next_fold.py`, `-p no:xdist`, in the clone | exit 0, 60 passed |
| the same two modules with `fold_check.py` replaced by `e9dfe623`'s, `-k` on the seven new cases, then restored with `git checkout` | 8 failed, 1 passed (the no-root pin) |
| `bin/fold-check` at the clone root, and typed in the clone's `docs/` | exit 0 both; 136 statements in 14 documents, the cutoff 1790154761 binds 21; 14 held to 1000, 0 listed |
| `bin/fold-check --shape-from 0` at the clone root | exit 1; 143 lines, 2 summaries and 141 problems, as round 1 recorded |
| `bin/evidence-check .` in the clone | exit 0; 2101 ok, 0 drifted, 0 broken |
| one probe script under the round directory, run once and deleted, over planted directories deleted in its `finally`: `why` over four sources; a null-byte target, a deeply nested target, a mode 000 document; the script copied alone; opted out three ways; no repository; a subdirectory with a listed directory; `--root docs/`; a case-mismatched listing; a Latin-1 `config.md` | see the verdicts and notes 1 to 4 |
| broad gate (full suite, repository-wide lint, typecheck) | not yet: the sealer's, after the rounds settle |

## Paste-ready fixes

None of these are needed for a fix. They are here so a smith who takes a
note has something to paste.

### Note 1

```python
    if isinstance(error, SyntaxError):
        if error.lineno:
            return f"SyntaxError at line {error.lineno}"
        return f"SyntaxError ({error.msg})"
```

### Note 2

The class is four scripts, not one, so fixing it only here would be a
special case. The narrower repair is the docstring. The fuller one is the
refusal in each of the four scripts' `load`, pinned by code:

```python
    if not os.path.isfile(path):
        sys.stderr.write(
            f"fold-check: cannot read {path}, and {purpose}. This command "
            "ships beside it in the plugin; a copy of one script taken on its "
            "own is not a plugin.\n"
        )
        raise SystemExit(2)
```

```python
    assert done.returncode == 2 and "Traceback" not in done.stderr, done.stderr
```

### Note 3

```python
    folded = {name.casefold(): name for name in names}
    for rel in sorted(set(over) - set(names)):
        if rel.casefold() in folded:
            problems.append(
                f"{rel} is listed over the ceiling, and the tree spells it "
                f"{folded[rel.casefold()]}"
            )
        elif os.path.exists(os.path.join(root, *rel.split("/"))):
```

### Note 4

```python
        return "", (
            f"{root}, which has opted out — `{resolver.SCRATCH}` is under its "
            "git directory, and its seal/config.md is not read"
        )
```

```python
        "its git directory, and its seal/config.md is not read, so nothing was "
```

## Regression tests to plant

None are owed. If note 2 is taken, the copied-alone case at
`tests/test_a_folded_statement_names_what_enforces_it.py:357` becomes the pin
for its exit code.

## Facts for the evidence ledger

None new. Row G1's red-before claim (8 red, and the no-root pin green before
and after) was re-executed and holds. Its mutation counts were not re-run.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: no

Loses a record or crashes: no

Broad gate: `not yet`. With nothing open that needs a fix, the gate is now
due. That means the sealer's spawn, not a run for the session that reads
this.

## Proof block

Files opened: `skills/settle/scripts/fold_check.py` (at `ff3d26cd`, and
`e9dfe623`'s copy run against the cases),
`tests/test_a_folded_statement_names_what_enforces_it.py`,
`tests/test_a_document_has_room_for_the_next_fold.py` (via the diff and the
runs), `hooks/optin.py` (`repo_root`, `git_common_dir`, `home_at`, `SCRATCH`),
`hooks/config.py` (`:403`), `skills/verify/scripts/broad_gate.py` (`:600`),
`tests/conftest.py` (git environment lines), `bin/fold-check`, `bin/test`,
`docs/the-evidence-ledger.md` (`:180`–`:193`),
`seal/ledger/1790260563-the-fold-checks-run-only-as-this-repositorys-tests.md`
(via the diff), and `rounds/round-1.md` and `rounds/round-1-report.md` of this
work item.
