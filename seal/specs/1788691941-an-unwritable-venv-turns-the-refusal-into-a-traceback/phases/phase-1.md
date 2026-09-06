# 1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback — phase 1

<!-- seal/specs/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 8be39a9 |
| Ran by | <left for the orchestrator — the spawn prompt named no model, and the template's own rule is that a segment transcribes this value or leaves it, never sources it from its own idea of what it is> |

## What this phase was asked

The guard, its sentence, and the case that pins the wording. Phase 2 — R2's
caveat in `seal/ledger.md` and the reach-vocabulary case — belongs to a
different segment and must not be started here.

1. **The guard.** `.github/scripts/run_tests.py#hide_from_git` writes
   `.venv/.gitignore` unguarded. Round 2 of #156's chain moved that call into
   `ensure`'s `finally`, which is right — it is what makes the guarantee
   exit-level rather than a list of remembered paths — and it means the call
   now runs on the two exits whose entire product is a sentence. Guard the
   write so an unwritable `.venv` produces a sentence, not a `PermissionError`
   traceback after the refusal has already printed.
2. **The sentence** names the path and says what it means for `git status`. It
   goes where the module's other refusals go; read the file for that rather
   than assuming. `venv_version` already catches `OSError` around its read, so
   the repair matches a habit the file has.
3. **The case that pins the wording**, per `agent-contract` §14. Seen red
   first against the unguarded write, on a real fixture: a `.venv` holding an
   interpreter and a `pytest` script, `pyvenv.cfg` reading `version = 3.11.9`,
   the directory made unwritable. Report both runs with their output.

Handed over as **unverified, and it decides whether the case is worth
anything**: a `chmod 555` fixture does not stop a write when the process runs
as root, and Windows does not honour it the way POSIX does, while the suite
runs on `ubuntu-latest`, `macos-latest` and `windows-latest`. Settle what the
case does on each before writing it — a case that silently passes because the
write succeeded is worse than no case — and make it impossible for the case to
pass without the guard having run.

## What this phase found

**The class claim holds, and reading is what settles it.** The handoff's
`read` label was checked rather than trusted. `.github/scripts/run_tests.py`
contains exactly three statements that put anything in the working tree:
`hide_from_git`'s `ignore.write_text`, and two `subprocess.run` calls — the
builder's steps in `build`, and pytest itself in `main`. The two subprocess
calls do write to the tree, and neither is in this class: their failure is
already a return code the caller reads, which is the whole of `build`'s
existing refusal. So the class of *unguarded Python-level writes from this
module* has one member, closed by construction rather than by a list — which
is what lets a sentence in the module docstring carry it. The docstring now
carries that sentence, and says the guard belongs to the module rather than
to the function, because the class is one write only for as long as nobody
adds a second.

**The unverified platform fact is true, and its consequence is the opposite
of the one the handoff worried about.** Settled by reading, not by running —
this machine is POSIX and non-root, and neither of the two cases in question
can be executed here:

| Platform | What `chmod 555` on the `.venv` does | What the case would do |
|---|---|---|
| POSIX, non-root | the write is refused with `EACCES` | passes, for the right reason |
| POSIX, as root | root bypasses the permission bits, the write succeeds | see below |
| Windows | `os.chmod` sets the read-only flag and ignores every other bit, and that flag does not stop a file being created inside a directory | see below |

The handoff's worry was a **silent pass**. That is what a case asserting only
*no traceback* would have done, and it is why this one does not assert only
that: it asserts the sentence, and on root or Windows the sentence never
prints because the write succeeded. So the shape converts the silent pass into
a **red case for a reason unrelated to the guard**, which is a different
failure and no better — a suite that goes red on `windows-latest` for a
platform's `chmod` semantics teaches the next reader to weaken the assertion.

So both halves were taken, deliberately:

- `test_an_unwritable_venv_leaves_the_refusal_a_sentence` builds the real
  fixture and is **skipped** where `chmod` does not stop a write, with the
  reason written into the `skipif` rather than into a comment beside it — the
  reason travels with the skip into pytest's own report. The predicate is
  `CHMOD_STOPS_A_WRITE`, named once at module level with the reasoning above
  it.
- `test_the_unwritable_sentence_is_the_same_on_every_platform` makes the
  **write** refuse instead of the directory, by monkeypatching
  `pathlib.Path.write_text` to raise `PermissionError` for `.gitignore` alone.
  It runs on all three platforms, and it cannot pass without the guard —
  without it, `ensure` raises and the case errors.

Neither can pass on a write that succeeded, which is the property that was
asked for.

**Where the sentence goes was read off the file rather than chosen.** Every
refusal in this module prints to `sys.stderr` and opens with `bin/test: `, and
one of the existing cases asserts that prefix on the grounds that *the reader
typed `bin/test` and the runner it reaches has a name they never saw*. The new
sentence follows both.

**The reason is `problem.strerror or problem`.** `strerror` alone reads
cleanly — `(Permission denied)` — but it is `None` for some `OSError`
subclasses, and a sentence that degrades to `(None)` tells the reader less
than the exception's own text would. Pinned by the platform-independent case,
which asserts `Permission denied` appears, on the grounds that a full disk and
a read-only directory otherwise read identically.

**The sentence is true at the moment it prints, and the case proves it rather
than trusting it.** The fixture case runs `git status --porcelain` after the
run and asserts `.venv` is in it. That is the half of #177 that is not about
tracebacks: the sentence promises the directory will appear in `git status`,
and a promise a case does not check is a wording change away from being false.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

## Runs

**Red, at `aabb30c` (the unguarded write), executed.** Both cases fail with
`PermissionError` escaping `ensure`'s `finally`, after the floor refusal has
already printed to stderr — which is the shape #177 reports, reproduced here
rather than inherited from the issue:

```
E   PermissionError: [Errno 13] Permission denied: '<tmp>/.venv/.gitignore'
.github/scripts/run_tests.py:244: in ensure
    hide_from_git(venv)
.github/scripts/run_tests.py:141: in hide_from_git
    ignore.write_text("*\n", encoding="utf-8")
----------------------------- Captured stderr call -----------------------------
bin/test: the virtualenv at <tmp>/.venv was built with Python 3.11.9, below
the 3.12 floor this repository supports. Remove that directory and run
bin/test again to build it afresh.

2 failed, 49 deselected in 0.13s
```

**Green, at `8be39a9`, executed.** `./bin/test
tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` → `51 passed in
0.83s`, exit `0` read directly rather than through a pipe. The six existing
`hide_from_git` cases are among them and are unchanged.

**What an operator sees**, executed against the fixture through a probe that
was deleted after it ran (contract §7) — two sentences, exit code `2`, no
traceback, and `git status` showing the directory the second sentence names:

```
bin/test: the virtualenv at <tmp>/.venv was built with Python 3.11.9, below
the 3.12 floor this repository supports. Remove that directory and run
bin/test again to build it afresh.
bin/test: could not write the ignore at <tmp>/.venv/.gitignore (Permission
denied). The virtualenv at <tmp>/.venv stays visible to git status until you
remove that directory or make it writable.

--- exit code: 2
--- git status: '?? .venv/'
```

`uvx ruff check` and `uvx ruff format --check` on both changed files: exit `0`
and `2 files already formatted`.

## What phase 2 must know

- **The sentence phase 2 has to cite exists and is pinned twice.** R2's
  guarantee — *invisible to git on every exit of `ensure`* — is now false on
  one path in a different way from before: the exit is reached, the ignore is
  still not written, and the runner says so instead of raising. The caveat
  belongs on the row, and the fragment it cites is `could not write the ignore
  at`, held by both new cases.
- **The work item still owes a changelog fragment.** `seal/specs/<id>/changelog.md`
  is not written yet; the hygiene workflow's check is release-only, so nothing
  on this branch will ask for it. Phase 2 is where it belongs, beside the
  ledger fragment.
- **The suite is unverified**, labelled per contract §2 with the orchestrator
  as its answerer. Only the one module was run.
