# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | bb543259 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The prefix. `clear_bytecode_cache(path, cwd=None)` joining a relative
`PYTHONPYCACHEPREFIX` to `cwd`, with `None` keeping today's behaviour for a
caller that passes nothing (`mutation_check.py`, S11); `run_arms` passing
`cwd=cwd` at all three sites; the docstring naming which directory a relative
prefix is read against and citing `cache_from_source`. S9 parametrised over a
relative and an absolute prefix, the relative parameter seen red against
`a340221b`. S10's syntax half: `tests/test_a_script_says_which_interpreter_it_needs.py`
and `tests/test_release_hygiene.py`. `mutation_check.py` is not in this tree
and is not created.

## What this phase found

**Phase 1 had left an existing unit unwatched, and this phase is where it
was found.** The first run clears the module's cache before anything else,
so the cache that `test_no_arm_runs_while_cached_bytecode_for_the_module_exists`
plants was gone before any arm ran. Deleting the clear before each arm's run
left that case green (measured, mutation P0). At `a340221b` that clear was the
first one, so the case watched it then. The repair is in the probe:
`SEES_CACHE` now takes the cache directory, logs what it sees, and leaves a
`.pyc` behind, the way a command that ignores `PYTHONDONTWRITEBYTECODE` would.
The case also asserts nothing is left once the run is over. With that, the
clear before each run (P6) and the clear after each restore (P7) each turn it
red, and the second was watched by nothing at `a340221b` either.

**The join has no `isabs` test.** `os.path.join(cwd, prefix)` returns an
absolute `prefix` unchanged, so `if cwd: prefix = os.path.join(cwd, prefix)`
moves only a relative one. On Windows a drive-relative prefix such as
`\cache` joined to `C:\work` becomes `C:\cache`, which is where CPython would
resolve it too. The guard is `if cwd`, not `cwd or os.getcwd()`, so a caller
passing nothing gets the old code path rather than an equivalent one.

**S9 asks CPython where the file is.** The planted path is
`importlib.util.cache_from_source` with `sys.pycache_prefix` set to the
prefix as a process in `other/` resolves it, so the case does not repeat the
clear's own join. During the clear `sys.pycache_prefix` is `None` and the
prefix comes from the environment, which is where a session's comes from.
Red at the unchanged clear (executed): the relative parameter saw `cache` at
all five runs. The absolute parameter's run half was green there, and its
direct call stopped only on the new keyword. It also calls the clear with no
`cwd`, which is the shape `mutation_check.py` has.

**S10 executed beyond the narrow pair.** `/usr/bin/python3` (3.9.6) loads
the script, prints `--help` and refuses a run with exit 2. The module passed
with pytest alone on 3.13 and 3.14 (`uvx --python 3.1x --with pytest`), the
two `arm-check-grammar` legs' shape. The legs themselves are the pull
request's.

**Mutations**, one at a time, restored from kept bytes with the sha256
compared and `__pycache__` cleared beside the script and the cases:

| # | Mutation | Red |
|---|---|---|
| P1 | the join removed | S9 relative |
| P2 | the join taken when `cwd` is `None` | S9 absolute (the no-`cwd` call raises) |
| P3 | the first run's clear without `cwd` | S9 relative |
| P4 | the clear before each arm's run without `cwd` | S9 relative |
| P5 | the clear after each restore without `cwd` | S9 relative, on the after-run glob |
| P6 | the clear before each arm's run deleted | the cache case |
| P7 | the clear after each restore deleted | the cache case, on the after-run glob |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `SEES_CACHE` reading the module path from `argv[1]` and deriving `__pycache__` from it | the caller passes the cache directory, so S9 can point the same probe at a prefix mirror |
