# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — review round 2

| Field | Value |
|---|---|
| Target SHA | ff3d26cdd3f3f913550548dd6d1c326f9ae982eb |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 587 |
| Broad gate | 778c26e1 against 7a7d3ae9; earlier run: 8d34718f against 7a7d3ae9; earlier run: 9bf8e371 against c52e8350 |
| Fixes checked by | no fixes to check |
| Fix range | `ff3d26cdd3f3f913550548dd6d1c326f9ae982eb..ff3d26cdd3f3f913550548dd6d1c326f9ae982eb`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790260563 is the verifying round: the diff of round 1's fixes, f181e30a..d32c365a, at ff3d26cd. Its job is whether each of round 1's eight verdicts is closed, and whether the units the fixes created (why, optin, located, git_init and seven cases) are correct.

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
| ⬜ 1 | `why` prints `SyntaxError at line None` for a target holding a null byte | `skills/settle/scripts/fold_check.py:361` | answered | Python 3.12 gives a null-byte SyntaxError no line number; the exit code (2) and the named file are right, and the line is what the interpreter knows; executed; exit 2 and the file are right, and only the reason reads badly |
| ⬜ 2 | a missing sibling script exits 1, which the reworded docstring now covers as exit 2, and the new case pins only `!= 0` | `skills/settle/scripts/fold_check.py:146` | deferred #590 | #590 — the missing-sibling exit is shared by settle.py, chain_check.py and round_record.py, so the fix belongs to the class across four scripts, not to this file; executed: exit 1 with and without `--root`; the same `SystemExit(str)` is in `settle.py`, `chain_check.py` and `round_record.py`; only a copy taken out of the plugin reaches it |
| ⬜ 3 | on a case-insensitive filesystem a listing spelled `docs/A.md` for `docs/a.md` is called "not a top-level docs/*.md" | `skills/settle/scripts/fold_check.py:384` | answered | on a case-insensitive filesystem a listing spelled with another case names a path the tree does not hold; the old message was false there too, and the listing is written by the repository, which spells its own files; executed on this macOS volume; the old "does not exist" was false there too |
| ⬜ 4 | the opted-out sentence reads "so its seal/config.md is not read, so nothing was checked" | `skills/settle/scripts/fold_check.py:469` | answered | the doubled 'so' is style in a pinned message; the reviewer judged it needs no fix, and rewording a pinned line reopens the run for no reader's benefit; read; the new case pins the doubled "so" at `tests/test_a_document_has_room_for_the_next_fold.py:472` |

## Paste-ready fixes

```python
    if isinstance(error, SyntaxError):
        if error.lineno:
            return f"SyntaxError at line {error.lineno}"
        return f"SyntaxError ({error.msg})"
```
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
```python
        return "", (
            f"{root}, which has opted out — `{resolver.SCRATCH}` is under its "
            "git directory, and its seal/config.md is not read"
        )
```
```python
        "its git directory, and its seal/config.md is not read, so nothing was "
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/settle/scripts/fold_check.py:547` | round 1's 🟡 1 — fixed |
| round-1 | `skills/settle/scripts/fold_check.py:254` | round 1's 🟡 2 — fixed |
| round-1 | `skills/settle/scripts/fold_check.py:553` | round 1's 🟡 3 — fixed |
| round-1 | `skills/settle/scripts/fold_check.py:337` | round 1's 🟡 4 — fixed |
| round-1 | `tests/test_a_folded_statement_names_what_enforces_it.py:15` | round 1's ⬜ 5 — fixed |
| round-1 | `docs/the-evidence-ledger.md:195` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/settle/scripts/fold_check.py:137` | round 1's ⬜ 7 — fixed |
| round-1 | `tests/test_a_folded_statement_names_what_enforces_it.py:58` | round 1's ⬜ 8 — fixed |
| round-1 | `skills/settle/scripts/fold_check.py`, the six touched test modules | round 1's 🟢 — confirmed |
| round-1 | `skills/settle/scripts/settle.py:447` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_docs_line_wrap.py:186` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
