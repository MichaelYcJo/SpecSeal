# 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | aeff7326 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Scope 4 of `spec.md`: where the first prefix whose report settled the walk
is not the whole row, each later prefix runs once more under
`PYTEST_ADDOPTS` with ` --collect-only` added, nothing appended but its own
`--junitxml`, kept as `runners-at-base-<j>.txt` and `.xml`; any report there
makes every failing file read `MULTI_RUNNER`, naming the two parts. Once per
comparison, through the one existing `run(...)` call. Rule 3's two-runner
sentence is replaced, and the pass's cost and Axis B's limit are added, with
pins. S7 (p1, p1b and p1c, plain and xdist) and S8 are planted and seen red
first, and the one-shell-site case stays unchanged.

## What this phase found

**Seen red at a3aa139a's gate and at the phase-1 gate, the same words in
both.** S7 read `tests/test_x.py` `new` (p1), `tests/test_y.py` `failing on
base too` (p1b) and `tests/test_z.py` `new` (p1c), plain and under `-n 2`,
taken by a probe file (`tests/test_tmp_c_s7.py`, deleted) that printed the
words with a3aa139a's `broad_gate.py` checked out in place and again at
39b96a9d's parent. The planted S7 is red at both through `MULTI_RUNNER`
being absent, which is why the words were taken by the probe. S8 is red at
both on its kept-file assertion alone (no `runners-at-base-2.txt`), as the
spec expected; its words hold at both.

**The branch's root runner has to pass for S7 to exist.** With `&&`, a
branch whose root suite fails never reaches the runner in `sub`, so no
failing file of p1b or p1c is named at all. The fixture makes the branch
pass its root `tests/test_y.py`, which the base fails, so the base keeps the
p1b shape and the branch reaches `sub`.

**Collection under xdist writes the report too.** S7's xdist parameter
passes: `-n 2` beside `--collect-only` from `PYTEST_ADDOPTS` still wrote
`runners-at-base-3.xml`, so the pass needs no case of its own for xdist.

**The pass rides the one loop as a last group.** `None` in place of a group
marks it; it starts after the smallest prefix any group settled at, appends
nothing but its report's path, and stops at the first report it finds. A
comparison where no group settled runs no pass, since there is no first
runner to count after. The shell-site case
(`test_the_one_shell_site_is_run_and_it_applies_the_rewrite`) passes
unchanged.

**An existing case's claim became false, and it now says what it costs.**
`test_a_runner_first_row_runs_once_at_the_base` said the parts after the
runner "cost the base comparison nothing". They now cost one collection run
each. Its docstring says so, and it asserts the one
`runners-at-base-2.txt`. Rule 3's "runner first costs one run at the base"
gained the same clause, pinned.

**Mutations at aeff7326, fourteen, each red through `bin/mutation-check`:**
the pass re-running the settled prefix, the environment dropped, the second
report never found, the first part named wrongly, the replacement of the
words skipped, ` --collect-only` dropped, `MULTI_RUNNER`'s text, the
**New?** bullet's clause, and each of the five rule-3 sentences or clauses
this phase added. One of them, letting the pass run where no group settled,
is red by a crash (`min` of an empty list) rather than by a word, so the
guard's case is that crash.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Rule 3's two-runner sentence ("is asked about every failing file by the first runner a prefix reaches …") and its advice to read either word as the row's claim | rule 3's sentence that such a row reads `new?`, and its limit sentence, which keeps the old words for the rows collection alone does not reach; both pinned in `test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written` |
| `compare_at_base`'s paragraph saying a two-directory row is not measured | the same docstring's paragraphs on the collection pass and on what it does not reach |
