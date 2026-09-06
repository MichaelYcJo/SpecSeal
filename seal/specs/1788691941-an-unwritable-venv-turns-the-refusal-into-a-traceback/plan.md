# Implementation Plan: a refusal stays a sentence when the virtualenv cannot be written to

## Summary

Round 2 of #156's chain moved `hide_from_git` into `ensure`'s `finally`, which
was the right repair — it is what makes the guarantee an exit-level one rather
than a list of remembered paths. It also means the call now runs on the two
exits whose entire product is a sentence. `hide_from_git` writes
`.venv/.gitignore` with no error handling, so an unwritable `.venv` turns the
refusal into a `PermissionError` traceback after the sentence has printed.

## Technical context

- `.github/scripts/run_tests.py#hide_from_git` — `ignore.write_text("*\n", …)`,
  unguarded. It is the only place this module writes to the working tree, which
  is what closes the class by construction.
- `.github/scripts/run_tests.py#ensure` — the `finally` that calls it, and the
  two refusals above it that return one line.
- `.github/scripts/run_tests.py#venv_version` — already catches `OSError` around
  its read, which makes the unguarded write the odd one out rather than the
  house style. The repair matches a habit the file already has.
- `seal/ledger.md` R2 — the guarantee, and the row this change makes partly
  false. The row is not removed: the code it cites still stands and the claim
  holds on every exit where the write succeeds. It gains the caveat.

**What breaks in 6 months.** Somebody adds a second write to the working tree
and does not guard it, because the guard reads as belonging to `hide_from_git`
rather than to the module. The docstring is where that is answered, and the
class being one function is why a sentence can carry it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Catch `OSError` and say nothing | The directory stays in `git status` and nobody is told why — the silent half of the very defect R2 exists against | **No** |
| Move the call out of the `finally` back onto the successful paths | Round 1 of #156 measured exactly this: the run that ends in a sentence is the run that leaves a half-built directory | **No** |
| Test the directory for writability before writing | A check that can pass and then fail, and one more thing to keep true. The write already answers the question | **No** |
| Catch `OSError` around the write and print a sentence naming the path and what it means for `git status` | An operator on a read-only `.venv` reads two sentences instead of one | **Yes** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The guard, its sentence, and the case that pins the wording — seen red first against the unguarded write, on a real `chmod 555` fixture | The new case plus the six existing `hide_from_git` cases; `uvx ruff` | |
| 2 | R2's caveat in `seal/ledger.md`, and the reach-vocabulary case reaching `call_sites`' own returnable set — or the limit written down beside it with grounds | `./bin/evidence-check .` unscoped; the fixes-surface module; the records | |

## Operational impact

None. No migration, no new dependency, no environment variable. An operator
whose `.venv` is writable sees no change at all.
