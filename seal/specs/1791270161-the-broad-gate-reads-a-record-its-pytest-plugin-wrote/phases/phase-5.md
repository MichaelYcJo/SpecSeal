# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | d97c83cf |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The redesign of the recorder after round 3 (`spec.md` Scope 1 as reframed,
`plan.md` Alternative N). First `questions.md` Q-M3, a measurement: whether
a string attribute a module-level hookwrapper sets on a report reaches the
xdist controller's `pytest_runtest_logreport` and `pytest_collectreport`
under `-n 2` on pytest 9.1.1 with xdist 3.8.0, and whether pytest 7.4, 8.0
and 8.1 carry the attribute and `item.path` plain; a `no` on the carriage
sends the work item back to the framer. Then the two hookwrappers; `write`
keeping a `test` line only where it carries a path that is not a directory
and a `collect` line only where it carries a path, counting the rest on the
`end` line; `absolute`, the guard and `an_argument_lies_outside_the_rootdir`
retired with the docstring's rootdir paragraphs. In the same commit (§14):
rule 3's rootdir paragraph and its "no third way is known" limit, the
`compare_at_base` docstring paragraph and the changelog fragment's bullet
replaced, pins moved and retired sentences asserted gone; the eight refusal
cases of the recorder module and the two gate cases flipped (S24), S23, S25
and S26 planted, the corpus row `("Q3b", "own")` re-derived from its base.
Every new or flipped case seen red at 0c5b9b2c's recorder, a mutant per new
branch through `bin/mutation-check`.

## What this phase found

**Q-M3: yes on every build, so the frame holds.** Executed in a scratch
project outside the tree with a probe module of the same two hookwrappers,
loaded through `PYTHONPATH` and `-p` in `PYTEST_ADDOPTS` as the gate loads
the recorder, over a passing test, two failing ones (one a class method)
and a module that fails to collect, run with `--continue-on-collection-errors`:

| Build | Plain | `-n 2`, pytest-xdist 3.8.0 |
|---|---|---|
| pytest 9.1.1 (the worktree's `.venv`) | 10 lines, 0 without the attribute | 10 lines, 0 without it, all written by one pid |
| pytest 8.1.2 (`uvx --with pytest==8.1.2 --with pytest-xdist==3.8.0`) | 10, 0 | 10, 0, one pid |
| pytest 8.0.2 (the same, `==8.0.2`) | 10, 0 | 10, 0, one pid |
| pytest 7.4.4 (the same, `==7.4.4`) | 10, 0 | 10, 0, one pid |

Under `-n 2` on 9.1.1 the probe also stamped the pid of the process that set
the attribute: the record was written by pid 33367 (the controller) and
every attribute was set by 33368 or 33369 (the workers), the failed
collection's by 33368. So the path is read on the worker and arrives on the
controller's copy of the report, and `item.path` exists on every build
measured. Python was 3.14.3 throughout; `item.fspath` below pytest 7 is read
only and is in `overview.md`'s *Not verified*.

**A failed collection under `-n 2` arrived once here**, where phase 1 saw
it once per worker. The reader treats a file's lines as a set either way.

**The count is per node, not per report.** `spec.md` Scope 1 says the
`end` line's `unplaced` is "the count of lines not written", and S27 says
a session-parented item gives 1. A test's three phases are three reports,
so a count of lines gives 3; and xdist hands a failed collection once per
worker, so a count of reports grows with `-n`. The recorder counts each
`(kind, nodeid)` once, which is S27's number and says how many tests or
collections a person will not find in the list. `overview.md` holds the
divergence row; the `count per report` mutant below is red against S27.

**A failed collection of a directory has the directory's path**, which is
the thing that failed (Scope 1). pytest 9 reports a package whose
`__init__.py` raises as a failure of the module beneath it, not of the
package, so the case for a directory uses a `conftest.py` that raises at
import, which pytest reports as `tests/sub`'s collection failing.

**The hookwrapper reads the report inside a `try`.** Where another
`pytest_runtest_makereport` raised, `outcome.get_result()` raises again
inside the wrapper, and pluggy adds a warning naming
`specseal_pytest_record`'s teardown to pytest's own INTERNALERROR (probed:
exit 3 either way, one warning without the `try`, none with it).
`test_a_report_hook_that_raises_is_not_laid_at_the_recorders_door` holds
it.

**Two cases were added beyond the plan's list, one per branch that no
planned case reached:** a conftest that logs a test report and a collect
report it built itself (the "no path" branch of both hooks, `plan.md`
Alternative S), and a directory whose collection fails (the `kind == "test"`
restriction on the directory check).

**Seen red at 0c5b9b2c's recorder (executed).** The recorder module's
new and flipped cases, run with this phase's module in place and 0c5b9b2c's
recorder: 12 failed — S1 (no `unplaced` on the `end` line), S23 plain and
xdist, the six flipped S24 cases (each `expected exactly one record file,
found []`), S25 (exit 1, `assert None == '1'`: the package imported before
the conftest's hook), and both S27 layouts (no record). The gate's cases,
run through a script that put 0c5b9b2c's recorder, `templates/config.md`,
`broad_gate.py` and the changelog fragment in place and restored them from
the bytes it read first: 6 failed — the two flipped S24 cases and S26 (the
first two read `NO_RECORD_AT_HEAD`), `Q3b-own` (`NO_RECORD_AT_HEAD`), the
rule-3 pin and the new S28 pin.

**Mutants (executed, `bin/mutation-check`, each `red`):** the makereport
wrapper's body deleted and the collect-report wrapper's body deleted (S23,
both parametrizations); the `try` around `get_result` re-raising (the
hook-raises case); the no-path check removed (the built-reports case); the
directory check removed (S27); the directory check widened to `collect`
lines (the directory case); `isdir` replaced by `not isfile` (the
self-removing module, Alternative U); the node not counted, the `end`
line's count fixed at 0, and the count made per report (S27); the
`if path is None: return` of each hook removed (the built-reports case).

**`Q3b` under its own row reads `new?` naming exit 1 now**, where it read
`NO_RECORD_AT_HEAD` while the refusal stood: the base's
`a/b/tests/test_two.py` holds no test, and its row fails
`a/tests/test_two.py`. `word_for` lost its `no-record-at-head` kind, which
no row of the corpus spells any more.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `Recorder.absolute`, the rootdir join | none: the node's own path replaces it (`_node_path`, the two hookwrappers) |
| `Recorder.an_argument_lies_outside_the_rootdir`, its `find_spec` and its `exists` skip | none: nothing is refused, so nothing locates an argument |
| the guard in `Recorder.write` that abandoned a whole record | `Recorder.path_of`, which leaves one node out and counts it |
| rule 3's refusal sentence and its "no third way is known" limit | rule 3's two sentences on what a line names a file by and what it leaves out |
| the changelog fragment's bullet "A pytest that names a file outside its rootdir writes no record" | the bullet "Each failing file is named by the path pytest holds for it" |
| `word_for`'s `no-record-at-head` kind | none: no corpus row spells it |
| the `../no_such_thing` half of the `--pyargs` case (round 2's ⬜ 4, which pinned the refusal's `exists` skip) | none: the skip retired with the refusal; the case keeps its `--pyargs` half, renamed `test_a_pyargs_module_inside_the_rootdir_is_recorded_under_its_own_path` |
