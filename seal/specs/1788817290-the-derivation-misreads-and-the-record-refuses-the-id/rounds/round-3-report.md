# Round 3 — report · `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` (#211, #194, #227)

| | |
|---|---|
| Target SHA | `fcb0421` |
| Diff under review | `git diff a283e64..fcb0421`, substance `69a3967`, `df9a3d0`, `1742dcf` |
| Kind | verifying round, and the last one this work item gets |
| Ran by | warden on claude-opus-5 |

## The one thing to read first

`runner_reached` decides whether pytest reaches a unit by asking **where the
file sits**. pytest decides it two different ways, and neither is a directory
question in the way the fix assumed:

| The unit | What pytest actually keys on |
|---|---|
| a `test_*` def | whether `python_files` matches the file NAME, anywhere in the tree |
| a fixture in a `conftest.py` | whether a collected test sits at or below that conftest's directory |
| a `pytest_*` def in a `conftest.py` | whether pytest registered the conftest as a plugin, which it does for every directory it recurses into |

Round 2's finding 1 was that the conftest arm ignored the middle row. The fix
added that question and applied it to **both** conftest rows, so the third row
is now wrong: a hook in a conftest with nothing collected under it reads `no
call site found`, and pytest calls it on every run. That is #211's own
sentence, at a third placement, arriving inside the repair for the second.

Findings run in that causal order. 1 is what the fix introduced, 2 is the case
that pins it in place, 3 is the same confusion on the first row and predates
the branch, 4 is what the reach column costs once a unit's name is not unique.

## What this round was asked

Round 3, the verifying round over round 2's fixes, at `fcb0421`, with the cap
spent: rounds 1 and 2 both closed on fixes, so the record after this one ends
the run and anything opened here becomes an issue rather than a fix. Rounds 1
and 2, their reports and their fix records were inherited, and the broad gate
had already passed at this SHA — `2624 passed, 2 skipped`, `ruff` clean.

The named targets were the seven conftest placements the fix pass found rather
than the two round 2 handed it, with an eighth to look for; `conftest_is_loaded`
against real pytest behaviour rather than against the sentence; the
trailing-slash mutation that survived the first sweep; whether the `RIDER_ROOTS`
widening is complete and `STAMP` accepts both stamp forms; the cross-run of
#239's own checker for `ok=4, drifted=0`, because a wrong answer there is a
merge conflict resolved in the wrong direction; and the disposition of the
`floor_record` finding no round named — that this work item's own records quote
a `def` line and `call_sites` greps every tracked file, so a committed record
invents a call site. Also: that the three totals now agree at 3052, the
`OLD_COORD_RE` rider's corrected worst case, and that round 2's paste-ready
stamp lines — which carried a path #239's pattern does not take — were not
pasted in.

Mid-round the orchestrator added two claims from round 1's warden, both
re-derived at this SHA and both reproduced here as findings 4 and 5.

## Findings

### 1 🟡 A hook in a conftest with no tests under it now reads `no call site found`, and pytest calls it every run

`skills/code-review/scripts/round_record.py:2033`

`69a3967` put `conftest_is_loaded` in front of the whole conftest arm. It
belongs in front of the fixture arm only. pytest registers every `conftest.py`
it recurses into as a plugin and calls that plugin's session and collection
hooks, whatever is collected under the directory — so a `pytest_*` def there is
dispatched exactly as one in `tests/conftest.py` is.

Executed, real pytest 9.1.1, hooks writing to a log on call:

    other_NO_TESTS:pytest_configure
    src_NO_TESTS:pytest_configure
    tests_vendor_NO_TESTS:pytest_configure
    tests_vendor_NO_TESTS:pytest_collection_modifyitems  items=1
    src_NO_TESTS:pytest_collection_modifyitems  items=1
    other_NO_TESTS:pytest_collection_modifyitems  items=1

Only the item-scoped hooks respect the directory: `pytest_runtest_setup` was  <!-- NAME NOT IN TREE -->
called on the root and `tests/` conftests alone. Four `pytest_*` defs moved the
wrong way through the fix — `other/conftest.py#pytest_other_configure`,
`tests/vendor/conftest.py#pytest_vendor_configure`,
`vendor/pkg/conftest.py#pytest_vendored_hook` and
`examples/conftest.py#pytest_addoption` all read `True` at `a283e64` and `False`
at `fcb0421`.

Nothing in the module holds the difference, which is why the regression is
invisible: `NESTED_CONFTEST` and `VENDORED_CONFTEST` each carry a fixture and no
hook, so the two new cases exercise only the arm the fix got right. A probe case
planting one hook in `tests/vendor/conftest.py` is **red at `fcb0421`** and
green under the repair below, with the other sixteen cases green in both runs.

The same paragraph is now false in prose, in four places that say a conftest
with nothing collected under it *is imported by nobody*:
`docs/review-chain-spec.md:768`, `round_record.py#conftest_is_loaded`'s
docstring, `runner_reached`'s third paragraph, and the ledger fragment's R2
Notes. Executed against the sentence: a plain `pytest` run from the rootdir
imported all nine conftests in the built tree, including `src/`, `other/`,
`a/b/`, `examples/`, `vendor/pkg/` and `tests/vendor/`. pluggy then refused the
run — `PluginValidationError: unknown hook 'pytest_vendored_hook' in plugin
<module 'conftest' from '…/vendor/pkg/conftest.py'>` — which only happens to a
plugin pytest has registered. The fixture half of the sentence holds; the import
half does not.

### 2 🟡 The case round 2's fix pass planted asserts a value that is false about pytest, and it kills no mutation

`tests/test_a_runner_reached_unit_reads_pytest_only.py:456`

`test_a_sibling_whose_name_extends_the_directory_is_not_below_it` makes two
assertions. The first is the property it was written for. The second,
`reach["test_in_a_sibling"] == generator.NO_SITE`, says pytest does not reach
`src_extra/test_in_a_sibling.py#test_in_a_sibling` — and pytest collects that
file, because `python_files` matches its name and collection starts at the
rootdir. Executed:

    src_extra/test_in_a_sibling.py::test_in_a_sibling
    4 tests collected in 0.00s

The second assertion also does no work. Executed, the trailing-slash mutation
re-applied three ways:

| What was in place | Killed by |
|---|---|
| the case as committed | `test_a_conftest_nothing_is_collected_under_is_not_loaded`, `test_a_sibling_whose_name_extends_the_directory_is_not_below_it` |
| the second assertion deleted | the same two |
| the whole case deleted, `src_extra/` kept in the fixture repo | `test_a_conftest_nothing_is_collected_under_is_not_loaded` |

What closed the surviving mutation is the fixture FILE, not the case. The
assertion's only effect is to pin finding 3's value, so a later correct repair
of the collected-module arm turns a green case red and the case's own docstring
argues for keeping the defect. That is the shape round 2 named in its own
prompt — a case written to kill a mutation pinning the mutation rather than the
property — one file over.

### 3 🟡 A collected test module outside `tests/` reads `no call site found`, which the spec's own row contradicts

`skills/code-review/scripts/round_record.py:2035`

The non-conftest arm gates on `under_tests(rel)`. `docs/review-chain-spec.md:752`
keys the same row on collection instead: *a `test_*` def in a file
`python_files` collects — collected by name pattern, the file and the function
both*. Where the two disagree, pytest agrees with the document. Executed:
`pkg/test_beside_the_code.py::test_beside_the_code` and
`src_extra/test_in_a_sibling.py::test_in_a_sibling` are both collected, and both
read `False` through the predicate at `a283e64` and at `fcb0421` alike.

This predates the branch and this tree holds no instance — `git ls-files` finds
no tracked `test_*.py` or `*_test.py` outside `tests/`. What makes it this
round's business is that a colocated layout is the common one outside this
repository, and the review chain's generator runs on any repository: there, every
test function in the tree reads `no call site found`, which is #211 unfixed.
Round 2's fix pass taught the conftest arm about the colocated layout —
`pkg/conftest.py` with `pkg/tests/` reads loaded, executed — and left the arm
beside it keyed to a directory name.

Deferred candidate rather than a fix to commission, because the cap is spent.

### 4 🟡 A unit whose name is not unique gets the whole repository as its reach, and the number grows when somebody writes a document

`skills/code-review/scripts/round_record.py:2076`

`call_sites` greps the bare text `name(` with no name resolution, so every
module that defines its own `main` and every document whose prose contains
`main(` lands in one unit's reach. Reproduced at both ends of the branch:

| Ref | `hooks/dispatch.py#main` |
|---|---|
| `ffd1d05` | 38 entries |
| `fcb0421` | **44 entries** |

The six that arrived are all documents this branch wrote — `changelog.md`,
`round-1-fixes.md`, `round-1-report.md`, `round-2-report.md`, `spec.md` and
another work item's ledger fragment. Twelve of the 44 are prose basenames, and
the first entry is `main` itself, another module's `def main():` line resolving
to its own enclosing unit (the def-line skip only fires when `path == rel`).

A reach column whose value rises because somebody wrote a document is not
measuring reach. It predates the branch; what ties it here is that #194 runs the
walk over strictly more units, so the cost grows with the widening — and this is
the concrete cost behind `questions.md` Q3.

**Q3 as written points at the wrong thing.** It asks whether the widened
`Contract changes` row becomes *noisy*, and offers *non-string literals* as the
narrowing. Narrowing which units enter the row does nothing about what a row
says once a unit is in it, and a 44-entry cell is unreadable at any row count.
The question Q3 should carry is whether the reach half is worth having without
name resolution. Executed as its answer: 13 of 13 tracked `hooks/*.py` that
define a top-level `main` return the identical 44-entry set.

Deferred candidate. What the issue needs: the two measurements above, the
observation that the reach set is identical across all thirteen callers so the
column distinguishes nothing among them, and the trade any repair makes —
restricting the grep to `*.py` makes the column mean *Python callers* and drops
a call from a workflow or a shell script, which is the same walk that currently
counts a committed record as a call site (finding 8's subject).

### 5 ⬜ #211's *Not verified* named a fourth candidate and no record answers it

`seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/plan.md:60`

The ticket asks about "a fixture, a `conftest` hook, a hook module's `main`".
`plan.md`'s class table has rows for the first two and none for the third, and
no round record on this work item carries an answer either. Grepped the work
item, the ledger fragment, `spec.md` and `docs/review-handoff-protocol.md`.

The answer is that it is not a member, and it is worth writing down because of
*why*: all thirteen hook modules' `main` escape the symptom by falling into
finding 4 instead. A candidate that avoids `no call site found` by collecting 44
false call sites is not the same as a candidate that was never a member.

### 6 ⬜ The count the fix pass made agree at 3052 stopped being true one commit later, and three of the four places name no tree

`tests/test_the_reopening_is_one.py:174`

Round 2's finding 3 was that one enumeration carried three totals, and its
grounds were that *a bare number with no tree beside it is what went stale*. The
fix made every site read 3052 and, in `round-1-fixes.md`, named the tree —
*re-derived at `59dc0e4`*. The other three sites carry the number alone.
Executed, top-level defs in tracked `.py` files:

    a283e64: 3052 in 114      69a3967: 3056 in 114
    59dc0e4: 3052 in 114      df9a3d0: 3056 in 114
                              1742dcf: 3056 in 114
                              fcb0421: 3056 in 114

`69a3967` added four defs, so 3052 stopped being true at the first fix commit —
the same one-commit lag, in the fix for it. The rider is the site that matters,
because a rider is what outlives the round: its stamp anchors the *code* it sits
above and says nothing about the count in its prose. `overview.md:26` reads
*measured over all 3052 top-level defs: this tree holds no instance*, where
*this tree* is now 3056. `round-1-fixes.md:77` still opens *at HEAD — 3052 defs*
three lines above the correction that names `59dc0e4`.

The conclusion each site carries is unaffected — re-derived at `fcb0421`, no
verdict in this repository moves — so this is a correction, not a fix.
`overview.md` and the ledger fragment are the run's own paperwork.

### 7 ⬜ The sixth rider root was left out, and it would have passed

`tests/test_a_rider_reaches_its_file.py:117`

`df9a3d0` widened `RIDER_ROOTS` by `tests` on the grounds that a rider nothing
walks is watched by nobody. `.github/scripts/fold_ledger.py:163` carries a real
comment-opening rider, stamped `Verified 2026-09-02 at 881fb0f`, and no check in
this tree walks `.github`. Executed: `881fb0f` is an ancestor of `HEAD` (exit
0), and adding `".github"` to the list leaves the module green — `8 passed`,
exit 0. So the one-word addition costs nothing and would have closed the class.

The grounds for leaving it are stated in the comment and they hold: `#239`'s
`rider_check.py` · NAME NOT IN TREE walks six roots including `.github`, every
hunk here sits inside the block it replaces, and this branch ships no regression
— `.github`'s rider is exactly as unwatched as it was before. §12 is met by
disclosure rather than by enumeration, which is the weaker of the two.

### 8 ⬜ The deferral names three documents and the code it is about carries no marker

`skills/code-review/scripts/round_record.py:2064`

The disposition of the `floor_record` finding is right and it is reachable.
`call_sites` inventing a call site out of a committed record is stated in the
rider at `tests/test_the_reopening_is_one.py:174`, in the ledger fragment's R2
Notes, and in `overview.md` §*Not verified* with the repository owner named as
its answerer. Executed: `bin/deferral-check` resolves, exit 0. Not closing it is
the right call — deciding which files a reach walk may name is a rule, and a fix
pass that adds one ships it unread.

The gap is where the three documents point. Round 1's finding 5 established the
rule that a coordinate-tied deferral belongs in a rider AT the line, and
`overview.md` quotes it. This defect's coordinate is `call_sites`, and
`call_sites` carries nothing: whoever next opens it gets no warning, and the
rider that explains it sits in a test module about reopening. One rider at
`call_sites` would put it where a reader will find it.

### 9 ⬜ Every conftest unit spawns a full `git ls-tree -r` over the tree

`skills/code-review/scripts/round_record.py:2017`

`conftest_is_loaded` calls `tracked_at(root, b)`, which is an uncached
`git ls-tree -r --name-only` over the whole tree, and it is called once per
conftest unit in the record. The module's only other call site is `:2284`, once
per record. One conftest here, so nothing is measurable in this repository; a
repository with a conftest per package pays one full tree listing per unit on
top of the `git grep` the reach walk already costs.

### 10 🟢 Round 2's finding 1 is closed, and the conftest class is wider than either round named

`skills/code-review/scripts/round_record.py:2033`, `tests/test_a_runner_reached_unit_reads_pytest_only.py:423`

Re-derived rather than read. Seventeen placements in two layouts through both
predicates: ten verdicts move, and the six fixture placements all move the right
way — `src/`, `a/b/`, `examples/`, `vendor/pkg/`, `other/` and `tests/vendor/`
go from `pytest only` to `no call site found`, while the root conftest,
`tests/conftest.py` and the colocated `pkg/conftest.py` stay reached. The eighth
placement asked for is `other/conftest.py`, a sibling of a colocated `pkg/`,
and it is handled. The four that move the wrong way are finding 1.

The mutation sweep reproduces. The trailing-slash mutation is killed by two
cases; the name-alone mutation by three; round 2's own paste-ready shape, run as
a mutation, by `test_the_directory_decides_inside_tests_as_well` alone — which
is why the gate was restructured rather than pasted, and the fix record says so.

### 11 🟢 Round 2's finding 2 is closed, both stamp forms are accepted, and #239's checker agrees at four

`tests/test_a_rider_reaches_its_file.py:137`, `tests/test_the_reopening_is_one.py:188`

`STAMP` accepts `at <sha>` and `against <anchor>@<hash>`, and `m.group("sha")`
is `None` for the second, which the ancestry case skips. The empty-corpus
assertion is real: three commit-form stamps remain in the walked roots, so the
case cannot pass over nothing. Executed: `3f8f846` and `4581fe1` are ancestors
of neither `HEAD` nor `origin/release/v0.9.1`, so neither of those two riders
could have carried a commit at all.

The two paste-ready stamp lines round 2 supplied carried a path, and #239's
pattern takes none. They were not pasted in — the tree holds
`# Verified 2026-09-08 against floor_record@bba5c7a1` and
`# Verified 2026-09-08 against OLD_COORD_RE@1ca5aff0`, and a grep for any stamp
with a `/` before its anchor returns nothing.

The cross-run reproduces exactly. #239's `rider_check.py` · NAME NOT IN TREE,
taken from `origin/fix/239-a-stamp-names-content-not-a-commit` at `d069d54` and
run against this tree: **`4 ok · 0 drifted · 18 broken`**, exit 2. The four are
the four anchors this branch writes and all four hashes recompute. Every one of
the 18 is a pre-#239 `at <sha>` stamp, and I checked the one that looked like
this branch's: `round_record.py:200`, stamped `Verified 2026-09-08 at 00e63c3`,
was written by `2138c98` and arrived with the `release/v0.9.1` merge. So the fix
record's *none of them this branch's* holds. Whichever branch merges second
takes #239's version, and the resolution is one decision.

### 12 🟢 Round 2's finding 4 is closed and the `OLD_COORD_RE` measurement reproduces

`skills/evidence-check/scripts/evidence_check.py:98`

Timed independently over all 1521 lines of `seal/ledger.md` and the
`seal/ledger/*.md` fragments, three runs each: the worst is **0.000527 s** at
`seal/ledger.md:1356`, 8831 characters — the longest row in the corpus — and the
19 rows of 1150–1280 characters top out at **0.000167 s**. The rider's 0.000533 s
and 0.000178 s reproduce within noise, and the judgment it carries is
unreachability, which holds with the margin it now states. `bin/evidence-check`:
`815 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0.

### 13 ❓ The full suite, the repository-wide lint and the typecheck — out of verified scope

the branch as a whole

`agent-contract` §2 reserves the broad gate for one run after the rounds settle,
and this round ran nothing broad. What was executed is the table below, plus the
five narrow modules this diff touches: `176 passed, 1 skipped`, exit 0. The
orchestrator answers this row. Nothing in the prompt ordered a check §2
excludes, so there is no declined instruction to name.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `pytest_*` def in a conftest with nothing collected under it now reads `no call site found`, and pytest registers that conftest and calls its session hooks on every run — #211's own sentence at a third placement, inside the repair for the second | `skills/code-review/scripts/round_record.py:2033` | open | executed — real pytest called `pytest_configure` and `pytest_collection_modifyitems` from three conftests with no collected test under them; four `pytest_*` defs read `True` at `a283e64` and `False` at `fcb0421`; a probe case planting one hook in `tests/vendor/conftest.py` is red at HEAD and green under the repair, sixteen other cases green in both |
| 🟡 2 | The new sibling case asserts `NO_SITE` for a module pytest collects, and the assertion kills no mutation — deleting it, and deleting the whole case, both leave the trailing-slash mutation killed | `tests/test_a_runner_reached_unit_reads_pytest_only.py:456` | open | executed — `src_extra/test_in_a_sibling.py::test_in_a_sibling` is in pytest's collect list; the mutation is killed by the fixture FILE, not by the case |
| 🟡 3 | The non-conftest arm gates on `under_tests`, where `docs/review-chain-spec.md:752` keys the same row on `python_files` collection — every test function in a colocated repository reads `no call site found` | `skills/code-review/scripts/round_record.py:2035` | open — deferred candidate | executed — `pkg/test_beside_the_code.py::test_beside_the_code` collected and read `False` at both SHAs; no instance in this tree, `git ls-files` finds no collected module outside `tests/` |
| 🟡 4 | `call_sites` greps bare text, so a unit whose name is not unique gets the whole repository as its reach and the number rises when somebody writes a document | `skills/code-review/scripts/round_record.py:2076` | open — deferred candidate | executed — `hooks/dispatch.py#main` 38 entries at `ffd1d05`, 44 at `fcb0421`, the six added all documents this branch wrote; 12 of 44 are prose basenames; all 13 tracked `hooks/*.py` defining `main` return the identical set. `questions.md` Q3 asks about row count and the cost is inside one cell |
| ⬜ 5 | #211's *Not verified* named a hook module's `main` as a fourth candidate; `plan.md`'s class table has no row for it and no round record answers it | `seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/plan.md:60` | open | executed — it is not a member, and the reason is finding 4 rather than anything about the class; grepped the work item, the ledger fragment, `spec.md` and `docs/review-handoff-protocol.md` for an answer and found none |
| ⬜ 6 | 3052 stopped being true at the first fix commit, and three of the four sites carrying it name no tree — round 2's finding 3 recurring inside its own fix | `tests/test_the_reopening_is_one.py:174` | open | executed — 3052 at `a283e64` and `59dc0e4`, **3056** at `69a3967` through `fcb0421`; only `round-1-fixes.md` names the tree it counted. The conclusion is unaffected: re-derived at `fcb0421`, no verdict in this repository moves |
| ⬜ 7 | `RIDER_ROOTS` gained `tests` and left `.github` out, where a real stamped rider sits unwatched for the same reason | `tests/test_a_rider_reaches_its_file.py:117` | open | executed — `.github/scripts/fold_ledger.py:163` carries a rider stamped `881fb0f`, an ancestor of HEAD; adding `".github"` leaves the module green at `8 passed`, exit 0. Grounds for leaving it are stated and hold: #239 covers six roots and every hunk sits inside the block it replaces |
| ⬜ 8 | The `call_sites` deferral is stated in three documents and `call_sites` itself carries no marker, where the rule round 1 established puts a coordinate-tied deferral at the line | `skills/code-review/scripts/round_record.py:2064` | open | read — the rider, the ledger fragment's R2 Notes and `overview.md` §*Not verified* all name it with the repository owner as answerer; executed — `bin/deferral-check` resolves, exit 0. The disposition is right; only its placement is short |
| ⬜ 9 | `conftest_is_loaded` calls the uncached `tracked_at` once per conftest unit, so each one spawns a full `git ls-tree -r` over the tree | `skills/code-review/scripts/round_record.py:2017` | open | read — the module's only other `tracked_at` call is once per record at `:2284`, and no `functools` import exists; not measurable in this tree, which holds one conftest |
| 🟢 10 | Round 2's finding 1 is closed for the fixture arm, the conftest class re-derived at seventeen placements in two layouts, and the mutation sweep reproduces | `skills/code-review/scripts/round_record.py:1995`, `tests/test_a_runner_reached_unit_reads_pytest_only.py:423` | answered | executed — see *Executed probes*; the eighth placement asked for is `other/conftest.py` beside a colocated `pkg/`, and it is handled |
| 🟢 11 | Round 2's finding 2 is closed, `STAMP` accepts both forms with the anchor skipped by the ancestry case, no stamp line carries a path, and #239's checker agrees at four | `tests/test_a_rider_reaches_its_file.py:137`, `tests/test_the_reopening_is_one.py:188` | answered | executed — `4 ok · 0 drifted · 18 broken`, exit 2, from #239's checker at `d069d54`; the 18 are pre-#239 commit stamps and `round_record.py:200`'s was written by `2138c98`, not this branch |
| 🟢 12 | Round 2's finding 4 is closed and the corrected worst case reproduces independently | `skills/evidence-check/scripts/evidence_check.py:98` | answered | executed — worst 0.000527 s at `seal/ledger.md:1356`, 8831 chars; the 19 rows of 1150–1280 chars top out at 0.000167 s; `bin/evidence-check` 815 ok, 0 drifted, exit 0 |
| ❓ 13 | The full suite, the repository-wide lint and the typecheck | the branch as a whole | out of verified scope | `agent-contract` §2 — the orchestrator answers it. Five narrow modules ran here: `176 passed, 1 skipped`, exit 0 |

## Executed probes

| What was run | Result |
|---|---|
| Real pytest 9.1.1 over a built tree of nine conftests, each writing to a log on import; plain run from the rootdir | all nine imported — the root, `tests/`, `tests/vendor/`, `src/`, `a/b/`, `examples/`, `vendor/pkg/`, `pkg/` and `other/`. pluggy then refused the run: `PluginValidationError: unknown hook 'pytest_vendored_hook' in plugin <module 'conftest' from '…/vendor/pkg/conftest.py'>` |
| The same tree with `pytest src` instead | `ROOT`, `src` — a targeted run loads a conftest a plain run's collection does not reach |
| Five conftests carrying `pytest_configure`, `pytest_collection_modifyitems` and `pytest_runtest_setup`, one test under `tests/` | the first two called from `other/`, `src/` and `tests/vendor/` — none of which has a collected test at or below it — with `items=1`; `pytest_runtest_setup` called from the root and `tests/` only |  <!-- NAME NOT IN TREE -->
| `runner_reached` at `a283e64` and at `fcb0421` over 23 defs in 17 placements, two layouts | **10 verdicts move.** Six fixtures move correctly; four `pytest_*` defs move wrongly — finding 1. `conftest.py`, `tests/conftest.py` and the colocated `pkg/conftest.py` stay reached; `other/conftest.py` and `src_extra/` stay unreached |
| A probe case for a hook in `tests/vendor/conftest.py`, against `fcb0421`'s predicate | **1 failed, 16 passed**, exit 1 |
| The same probe case with the repair from *Paste-ready fixes* | **17 passed**, exit 0. Restored byte-identical, `git status` clean |
| `prefix` loses its trailing slash | killed — `2 failed, 14 passed`, exit 1: `test_a_conftest_nothing_is_collected_under_is_not_loaded`, `test_a_sibling_whose_name_extends_the_directory_is_not_below_it` |
| The same mutation with the sibling case's second assertion deleted | killed — the same two |
| The same mutation with the whole sibling case deleted, `src_extra/` kept | killed — `test_a_conftest_nothing_is_collected_under_is_not_loaded` alone |
| The gate stops asking, so the name alone lets a conftest through | killed by 3 |
| Round 2's own paste-ready shape — the conftest arm BESIDE the `tests/` gate | killed by `test_the_directory_decides_inside_tests_as_well` alone |
| Real pytest `--collect-only` over a tree with tests under `tests/`, `src_extra/`, `pkg/` and `pkg/tests/` | 4 collected, including `src_extra/test_in_a_sibling.py::test_in_a_sibling` and `pkg/test_beside_the_code.py::test_beside_the_code` |
| Top-level defs in tracked `.py` files, per SHA | `ffd1d05` 3003/113 · `824bfca` 3051/114 · `4dfde1d` 3052 · `f8180f4` 3052 · `59dc0e4` 3052 · `a283e64` 3052 · **`69a3967` 3056** · `df9a3d0` 3056 · `1742dcf` 3056 · `fcb0421` 3056 |
| `call_sites` for `hooks/dispatch.py#main` at `ffd1d05` and `fcb0421` | 38 entries, then 44. The six added are `changelog.md`, `round-1-fixes.md`, `round-1-report.md`, `round-2-report.md`, `spec.md` and `1788789985-round-record-dies-on-python-3-9.md`; 12 of the 44 are prose basenames; the first entry is `main` |
| `call_sites` for `main` in every tracked `hooks/*.py` that defines one | 13 modules, **44 entries each, identical set** |
| `measure` over `a283e64..fcb0421` | 0 contract changes, 9 new units, 0 heuristic files |
| `git merge-base --is-ancestor` for `881fb0f`, `00e63c3`, `3f8f846`, `4581fe1` | `881fb0f` HEAD 0 · `00e63c3` HEAD 0 · `3f8f846` HEAD 1, release 1 · `4581fe1` HEAD 1, release 1 |
| `git log -S` for `round_record.py`'s `00e63c3` stamp | `2138c98 fix: a rider stamp named the commit its own squash discarded (#239) (#240)` — not this branch |
| `".github"` added to `RIDER_ROOTS`, nothing else | `8 passed`, exit 0. Restored byte-identical |
| Every `RIDER:` in the tracked tree, by top-level directory | `.github` 1 · `agents` 1 · `CLAUDE.md` 1 · `docs` 3 · `hooks` 7 · `seal` 40 · `skills` 3 · `templates` 1 · `tests` 5. The `docs` and `CLAUDE.md` hits are prose about the convention and open no comment; `.github/scripts/fold_ledger.py:163` is a real one |
| #239's `rider_check.py` · NAME NOT IN TREE, from `origin/fix/239-a-stamp-names-content-not-a-commit` at `d069d54`, over this tree | **`4 ok · 0 drifted · 18 broken`**, exit 2 |
| `OLD_COORD_RE` over 1521 lines of `seal/ledger.md` and the `seal/ledger/*.md` fragments, three runs each | worst **0.000527 s**, `seal/ledger.md:1356`, 8831 chars; the 19 rows of 1150–1280 chars top out at **0.000167 s** |
| `bin/evidence-check` | `815 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit **0** |
| `bin/deferral-check` | resolves, exit **0** |
| `bin/test` — the rider, reach, reopening, printed-ledger and records-carried modules | `176 passed, 1 skipped`, exit **0** |

Every exit code was read with `; echo $?`, never through a pipe. Probes ran in
a `git clone --no-local` of this worktree at `fcb0421`; every mutation was
restored from bytes kept in the mutating script and `git status --porcelain`
came back empty after each. The probe case was deleted with the clone.

## Paste-ready fixes

Finding 1. The directory question belongs to the fixture arm alone, so the
conftest arm reaches the arms unconditionally and the fixture arm asks. The
name is wrong for what it computes and moves with it.

```python
def conftest_fixtures_reach_a_test(root, b, rel):
    """True when a fixture in this `conftest.py` can be injected into a test.

    A conftest's fixtures are visible to the test files collected at or below
    its OWN directory — rootdir down to each collected file, `confcutdir`
    defaulting to rootdir — so one in a directory nothing is collected under
    injects into nothing. Round 2's finding 1 is that accepting the name alone
    said `pytest only` about all of them: `src/`, `a/b/`, a vendored tree, an
    examples directory, and `tests/vendor/` one gate over.

    This is NOT the question of whether pytest imports the file, which round
    2's fix asked in its place. pytest registers every `conftest.py` it
    recurses into as a plugin and calls that plugin's session and collection
    hooks whatever is collected under it — measured, `pytest_configure` and
    `pytest_collection_modifyitems` are called from a conftest in a directory
    with no test at or below it — so the hook arm asks nothing about the
    directory. Only the item-scoped hooks follow it.

    The question is asked of the tracked file list rather than of the
    filesystem, so it answers for the tree at `b` the way every other walk
    here does. The repository root passes it in any tree that has tests at
    all, which is the placement round 1's finding 2 was raised for;
    `src/conftest.py` passes it in a colocated layout and fails it in a
    segregated one, which is what pytest does.
    """
    here = os.path.dirname(rel)
    prefix = f"{here}/" if here else ""
    return any(
        p.startswith(prefix) and collected(os.path.basename(p))
        for p in tracked_at(root, b)
        if p.endswith(".py")
    )
```

```python
    Where the file sits decides two different things, and they are not the
    same gate. A conftest is loaded by NAME rather than by directory, so it is
    a member from anywhere — pytest registers every one it recurses into as a
    plugin, and its hooks are dispatched whatever is collected under it. What
    the directory decides is narrower: a fixture there can only be injected
    into a test at or below that directory, which is
    `conftest_fixtures_reach_a_test`. Nothing else outside `tests/` is a
    member however it is named.
    """
    base = os.path.basename(rel)
    if not rel.endswith(".py"):
        return False
    if base != CONFTEST and not under_tests(rel):
        return False
    module = parse_module(reader.show(root, b, rel))
    if module is None:
        return False
    for node in module.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name != name:
            continue
        if name.startswith(TEST_PREFIX) and collected(base):
            return True
        if name.startswith(HOOK_PREFIX) and base == CONFTEST:
            return True
        return decorated_as(node, FIXTURE) and (
            base != CONFTEST or conftest_fixtures_reach_a_test(root, b, rel)
        )
    return False
```

The regression case, planted beside the two the fix pass wrote. Seen red at
`fcb0421` and green under the two hunks above. It needs a hook in the fixture
repository's uncollected conftest, which is why the two literals move too.

```python
VENDORED_CONFTEST = (
    "import pytest\n\n\n@pytest.fixture\ndef a_vendored_fixture(x):\n    return x\n"
    "\n\ndef pytest_vendored_configure(config):\n    return None\n"
)
```

```python
    "tests/vendor/conftest.py": (
        "import pytest\n\n\n@pytest.fixture\n"
        "def a_vendored_fixture(x, extra=None):\n    return x\n"
        "\n\ndef pytest_vendored_configure(config, extra=None):\n    return None\n"
    ),
```

```python
def test_a_hook_in_an_uncollected_conftest_is_still_dispatched(reach):
    """Round 3's finding 1, and the half of round 2's repair that went one
    arm too far. pytest registers every `conftest.py` it recurses into as a
    plugin and calls that plugin's session and collection hooks whatever is
    collected under the directory — measured: `pytest_configure` and
    `pytest_collection_modifyitems` are called from a conftest with no test
    at or below it, and only the item-scoped hooks follow the directory. So
    the directory question belongs to the fixture arm alone, and asking it of
    the hook arm put #211's own sentence at a third placement. Nothing held
    the difference before this case: both uncollected conftests in the
    fixture repository carried a fixture and no hook."""
    generator = generator_module()
    assert reach["pytest_vendored_configure"] == generator.PYTEST_ONLY, reach
```

The prose §14 asks for, since a reader acts on it.
`docs/review-chain-spec.md:768`, replacing the *imported by nobody* sentence:

```markdown
The directory decides which of a conftest's units pytest reaches, and it
decides only one of them. pytest registers every `conftest.py` it recurses
into as a plugin, so a `pytest_*` def there is dispatched whatever is
collected under the directory — measured, `pytest_configure` and
`pytest_collection_modifyitems` are called from a conftest with no test at or
below it, and only the item-scoped hooks follow the directory. A fixture is
the one that does not travel: it can only be injected into a test collected
at or below the conftest's own directory, so a fixture in a vendored tree, a
package directory, an examples directory or `src/` in a segregated layout is
injected into nothing, and that is true inside `tests/` as well as outside it
— `tests/vendor/conftest.py` with no test module under it reaches no test any
more than `src/conftest.py` does. Round 2's finding on this section was that
the name gate alone said `pytest only` about all of them; round 3's was that
the repair applied the directory question to the hook arm as well.
```

Finding 2. The assertion the case does not need, and cannot keep once the
collected-module arm is right.

```python
def test_a_sibling_whose_name_extends_the_directory_is_not_below_it(reach):
    """*At or below `src/`* is a question about path SEGMENTS, and a prefix
    test without the separator answers a different one. `src_extra/` is a
    sibling of `src/` holding a collected test module, so a walk asking
    `startswith("src")` would find it, call `src/conftest.py`'s fixture
    reachable and put the false sentence back. A mutation dropping the
    trailing slash survived the first sweep of this unit for want of exactly
    this placement — the same blind spot, one release on, as the `_test.py`
    half of `collected`.

    What this case does NOT assert is the reach of `test_in_a_sibling`
    itself. `python_files` matches its name, so pytest collects it and reads
    it as a case; the predicate says otherwise, and that is round 3's finding
    3 rather than a property to pin here."""
    generator = generator_module()
    assert reach["a_nested_fixture"] == generator.NO_SITE, reach
```

Finding 3, as the deferred candidate's shape rather than a fix to commission.
Collection is keyed on the file name, so the arm is too, and `under_tests`
narrows only the fixture-and-nothing-else tail. `docs/review-chain-spec.md`'s
*Nothing else outside `tests/` is a member however it is named* and the same
sentence in `runner_reached`'s docstring both move with it, and
`test_a_sibling_whose_name_extends_the_directory_is_not_below_it`'s second
assertion has to be gone first.

```python
    for node in module.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name != name:
            continue
        if name.startswith(TEST_PREFIX) and collected(base):
            return True
        if name.startswith(HOOK_PREFIX) and base == CONFTEST:
            return True
        if base != CONFTEST and not under_tests(rel):
            return False
        return decorated_as(node, FIXTURE) and (
            base != CONFTEST or conftest_fixtures_reach_a_test(root, b, rel)
        )
    return False
```

Finding 4, as the deferred candidate's shape. Two hunks, and the second is the
one that carries a trade: restricting the grep to Python makes the column mean
*Python callers*, which drops a call from a workflow or a shell script and also
stops a committed record from inventing a call site.

```python
    out = git(root, "grep", "-n", "-F", "-e", f"{name}(", b, "--", "*.py") or ""
```

```python
            units = at_b[path]
            site = enclosing_unit(units, number)
            # A `def name(` line is a definition, not a call, in whatever file
            # it sits. Skipping it only in `rel` made every other module that
            # defines the same name resolve to its own enclosing unit, so
            # `hooks/dispatch.py#main` opened its reach with `main`.
            if site == name and name in units and number == units[name][1]:
                continue
            site = site or os.path.basename(path)
```

Finding 8, so the deferral reaches whoever opens the code it is about:

```python
    # RIDER: this walk greps EVERY tracked file, so a committed document that
    # quotes a `def` line is counted as a call site for the unit it quotes.
    # Executed on this repository's own records: `tests/test_the_reopening_is_
    # one.py#floor_record` read `no call site found` at `ffd1d05` and reads
    # `round-1-report.md, round-1.md` from `824bfca` on, with nothing about
    # the code changed. Deciding which files a reach walk may name is a rule
    # rather than a repair, so it is deferred; the answerer is the repository
    # owner. `seal/specs/1788817290-the-derivation-misreads-and-the-record-
    # refuses-the-id/overview.md` §*Not verified* holds the decision and the
    # ledger fragment's R2 Notes hold the measurement. The related cost is
    # that a name which is not unique collects the whole repository: measured,
    # `hooks/dispatch.py#main` returns 44 entries, 12 of them prose files.
    # Verified 2026-09-08 against call_sites@REPLACE_WITH_THE_COMPUTED_HASH
```

## Inherited coordinates

| From | Coordinate | Why it was still worth opening |
|---|---|---|
| round-2 | `skills/code-review/scripts/round_record.py:2011` | round 2's 🟡 1 — the fix is here, and finding 1 is the arm it went one too far on |
| round-2 | `tests/test_a_rider_reaches_its_file.py:109` | round 2's 🟡 2 — closed; finding 7 is the sixth root it left |
| round-2 | `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md:4` | round 2's ⬜ 3 — closed at 3052; finding 6 is that 3052 aged one commit later |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:77` | round 2's ⬜ 4 — closed, and the measurement reproduces independently |
| round-1 | `seal/follow-up.md:44` | round 1's ⬜ 5 — the rule that sends a coordinate-tied deferral to a rider at the line, which finding 8 applies to `call_sites` |
| round-1 | `tests/test_the_reopening_is_one.py:164` | round 1's rider — carried, not re-derived: the value-passing cause is unchanged and the fix pass corrected which unit shows it |

Carried rather than re-established: what round 1 measured about the
value-passing cause of `no call site found`, and round 2's corpus measurement
that the accepted finding-id language is unchanged over 7768 strings. Both have
a check that would fail if they had gone stale, and neither did.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 3 — a collected test module outside `tests/` reads `no call site found`, which the spec row contradicts | `deferred #N` candidate, with the paste-ready shape above; no instance in this tree | the repository owner |
| 4 — a unit whose name is not unique collects the whole repository, and the count rises with the number of documents | `deferred #N` candidate; the issue's contents are named in finding 4 | the repository owner |
| 5 — #211's fourth candidate, a hook module's `main` | folded into finding 4's issue: it is not a member, and the reason is finding 4 | the repository owner |
| `call_sites` counting a committed record as a call site | already deferred — the rider at `tests/test_the_reopening_is_one.py:174`, the ledger fragment's R2 Notes, `overview.md` §*Not verified*. Finding 8 is about placement, not about reopening the decision | the repository owner |
| Whether a reach walk should follow a callable passed as a value at all | already deferred — the same rider | the repository owner |
| Whether `Contract changes` wants the narrowing to non-string literals | already deferred — `questions.md` Q3. Finding 4 argues the question points at the wrong thing | the repository owner |
| Whether the two committed records that miscount their finding ids are corrected in place | already deferred — `overview.md` §*Not verified*; nothing is blocked | the repository owner |
| Which of `fix/239-a-stamp-names-content-not-a-commit` and this branch rewrites the other's rider block | already handed over; verified here that #239's version is strictly wider and every hunk sits inside it, so the resolution is to take #239's | the orchestrator |
| The full suite, the repository-wide lint and the typecheck | `agent-contract` §2 — one run after the rounds settle. Already passed at this SHA per the prompt | the orchestrator |

Needs a fix: yes — 1 and 2
Loses a record or crashes: no

Contract changes: none
New units: conftest_is_loaded (depth 1); MARKER (depth 1); NESTED_CONFTEST (depth 1); VENDORED_CONFTEST (depth 1); EXTRA_MOD (depth 1); test_the_fixture_repository_only_widens_signatures (depth 1); test_a_conftest_nothing_is_collected_under_is_not_loaded (depth 1); test_the_directory_decides_inside_tests_as_well (depth 1); test_a_sibling_whose_name_extends_the_directory_is_not_below_it (depth 1)

## Proof

Opened: `skills/code-review/scripts/round_record.py`,
`skills/evidence-check/scripts/evidence_check.py`, `docs/review-chain-spec.md`,
`tests/test_a_rider_reaches_its_file.py`,
`tests/test_a_runner_reached_unit_reads_pytest_only.py`,
`tests/test_the_reopening_is_one.py`,
`tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`,
`tests/test_the_records_can_be_carried_out_and_in.py`,
`.github/scripts/fold_ledger.py`, `bin/test`, `CONTRIBUTING.md`, `CLAUDE.md`,
`seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md`,
and this work item's `overview.md`, `plan.md`, `rounds/round-2.md`,
`rounds/round-2-fixes.md`. Read from `origin/fix/239-a-stamp-names-content-not-a-commit`:
`.github/scripts/rider_check.py`.
