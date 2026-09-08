# Round 1 — fixes · `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` (#211, #194, #227)

The fix pass is four commits from `29e0460`: `a77ef92` for finding 3,
`824bfca` for findings 1 and 2, `4dfde1d` for the case that closes a surviving
mutation of the unit those two added, and this record last. No terminal SHA is
written here, because the commit carrying this line cannot name itself.

Every finding was reproduced against the tree as it stood before anything was
edited, including the timed hang, and every case was seen red before its fix.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `824bfca` |
| 2 | fixed | `824bfca` |
| 3 | fixed | `a77ef92` |
| 4 | fixed | see `## The records` below |
| 5 | fixed | see `## The records` below |

## The red I saw before each fix

**Finding 3 — the hang, timed, twice.** The shipped `FINDING_ID_RE` against
`"!" * n + "x"`: `n=20` 0.043 s, `n=22` 0.171 s, `n=24` 0.702 s, `n=26`
2.844 s, `n=28` 11.178 s. The round's numbers reproduce. Then the case as
committed, which uses 4000 characters, run against the shipped pattern under
`timeout 90`: **exit 124**, killed while still running. That is the failure a
person meets — `close` producing nothing and never returning — rather than an
assertion.

The repair is one character: `[^\w\s]+` inside the `*` group becomes
`[^\w\s]`. **The language is unchanged, and that was measured rather than
argued.** Both patterns over every `#` cell in every committed round record —
6245 cells — and over 4368 constructed shapes built from markers, spaces,
digits and letters at lengths 1 to 3: **zero disagreements**, on acceptance
and on the captured id alike. Timed after: `n=28` 0.000003 s, `n=4000`
0.000132 s, `n=100000` 0.003008 s. Linear.

**Findings 1 and 2 — both from the record's own fixture repository.** Two
files were added to the built tree, `tests/helpers.py` holding a `test_*` def
and a root `conftest.py` holding one fixture and one `pytest_configure`, and
the two new cases were run against the unfixed predicate:

    test_shaped_but_uncollected  ->  pytest only          (wanted no call site found)
    a_root_fixture               ->  no call site found   (wanted pytest only)
    pytest_configure             ->  no call site found   (wanted pytest only)

Both findings, in the shape the round describes, out of the repository's own
test fixture rather than a scratch build.

## The boundary now, in a sentence that matches the code

**A unit is the runner's when pytest's own loading reaches it, and the file's
placement answers two different questions.** `python_files` decides which file
becomes a test module and `python_functions` which def inside it is a case, so
a `test_*` def is the runner's only in a file named `test_*.py` or `*_test.py`.
A `conftest.py` is loaded by name rather than by directory, so its fixtures and
its `pytest_*` hooks are the runner's wherever it sits. A fixture under
`tests/` is the runner's as before. Nothing else outside `tests/` is a member
however it is named.

That is `runner_reached`'s docstring and `docs/review-chain-spec.md`
§*The fix surface* word for word, which is the point — the two findings were
that the prose said this and the code said less.

*Corrected by round 2's fix pass, finding 1.* The third sentence is false of
pytest and this pass wrote it in three places. A conftest is loaded by name,
but the DIRECTORY still decides whether pytest loads it at all: rootdir down
to each collected test file. So a conftest with nothing collected under it is
imported by nobody, and calling its fixtures the runner's is round 1's own
finding 1 pointing the other way. The sentence now reads *wherever pytest
loads it*, and `conftest_is_loaded` is the code that asks.

## The re-enumeration

`runner_reached`, old and new, over **every top-level def in every tracked
`.py` file at HEAD** — 3052 defs in 114 files, not only the ones under
`tests/`:

*Corrected by round 2's fix pass, finding 3.* This read `3051` and named no
commit, so nobody could tell which tree it counted. 3051 was true at
`824bfca`, where the enumeration was run, and stopped being true one commit
later at `4dfde1d`, which added the case closing the surviving mutation below.
Counted per commit: `ffd1d05` 3003 · `824bfca` 3051 · `4dfde1d` 3052 ·
`a283e64` 3052 · `59dc0e4` 3052. The number here is the branch's, re-derived
at `59dc0e4`, and the conclusion is unchanged at either count.

| Where | File | Kind | Defs | OLD | NEW |
|---|---|---|---|---|---|
| outside `tests/` | any | other helper | 489 | 0 | 0 |
| under `tests/` | collected module | fixture | 46 | 46 | 46 |
| under `tests/` | collected module | other helper | 497 | 0 | 0 |
| under `tests/` | collected module | `test_*` name | 2006 | 2006 | 2006 |
| under `tests/` | `conftest.py` | fixture | 2 | 2 | 2 |
| under `tests/` | `conftest.py` | other helper | 11 | 0 | 0 |

**Not one verdict in this repository moves.** Every `tests/` module here is a
`test_*.py` or a `conftest.py`, so `collected` is true for all 2006 test defs
and there is no root conftest. The findings are about installs, which is what
the round said.

So the placements were built, in a repository made for the purpose, and each
was put through both predicates:

| File | Unit | OLD | NEW |
|---|---|---|---|
| `tests/helpers.py` | `test_shaped_but_uncollected` | `pytest only` | **`no call site found`** |
| `tests/helpers_test.py` | `test_in_a_suffix_module` | `pytest only` | `pytest only` |
| `tests/test_real.py` | `test_real` | `pytest only` | `pytest only` · NAME NOT IN TREE |
| `conftest.py` (root) | `pytest_configure` | `no call site found` | **`pytest only`** |
| `conftest.py` (root) | `a_root_fixture` | `no call site found` | **`pytest only`** |
| `conftest.py` (root) | `test_in_a_conftest` | `no call site found` | `no call site found` · NAME NOT IN TREE |
| `conftest.py` (root) | `a_root_helper` | `no call site found` | `no call site found` · NAME NOT IN TREE |
| `src/conftest.py` | `a_nested_fixture` | `no call site found` | **`pytest only`** · NAME NOT IN TREE |
| `src/mod.py` | `test_looks_like_one` | `no call site found` | `no call site found` |
| `src/mod.py` | `pytest_looks_like_a_hook` | `no call site found` | `no call site found` · NAME NOT IN TREE |
| `tests/pytest_named_helper.py` | `pytest_not_a_hook` | `no call site found` | `no call site found` · NAME NOT IN TREE |

Four move and all four are the two findings. Three of the unmoved rows are the
boundary holding: a `test_*` def **inside** a conftest is not collected, an
undecorated helper in a conftest is not a member, and a `pytest_*` def in a
collected test module is still the recorded limit.

**What the conftest widening costs, stated because it is a real cost.**
`src/conftest.py#a_nested_fixture` now reads `pytest only` even though pytest
never collects `src/`. The trade is that a fixture in a file named
`conftest.py` is pytest's by construction wherever it sits, against leaving
#211's own defect standing at the placement pytest documents first.

*Corrected by round 2's fix pass, finding 1.* The grounds are false and the
cost was read one instance wide. `src/conftest.py` was the only placement
built, and the members are every conftest in a directory nothing is collected
under, at any depth and inside `tests/` as well as outside it — executed over
seven of them. It was not a trade to accept; it was the same false sentence
arriving from the other side, and the round was right to open it.

## The mutation run, and the one that survived

`collected` is the only unit this pass added. Six mutations, one at a time,
`tests/__pycache__` cleared between, bytes saved in the mutating script and
restored from those bytes — never from `HEAD`, which would have taken the
uncommitted record edits with it. `restored byte-identical: True` after every
run.

| Mutation | First run | After |
|---|---|---|
| the `_test.py` half of `collected` dropped | **SURVIVED** — 12 passed | killed |
| the `test_*` half dropped | killed | killed |
| `collected` always true — the pre-fix behaviour | killed | killed |
| `collected` always false | killed | killed |
| the arm stops calling `collected` | killed | killed |
| the conftest escape hatch closed again | killed | killed |

The survivor is the fix's own blind spot: `python_files` is two patterns and
the built repository held a module matching only the first, so nothing was
holding the second half of the unit's own boundary.
`test_the_second_python_files_pattern_collects_too` and a
`tests/helpers_test.py` in the fixture close it, and all six are caught now.

## The records

**Finding 4.** The ledger fragment's R3 said *cross-checked against an
INDEPENDENT implementation … twice* and `phases/phase-3.md` said *a second
implementation, not a list of examples*. Both now say what the two halves
are: the whole-tree comparison runs a transcription of the shipped loop and
holds it against later drift, and the 21 constructed pairs are the
independent statement because their expectation column is hand-written.

**Finding 5.** The `floor_record` deferral moved out of `seal/follow-up.md`,
where it was a bullet under an empty table in the section for items another
branch holds, and became a `# RIDER:` above
`tests/test_the_reopening_is_one.py#floor_record`. `overview.md` §*Not
verified* names the repository owner directly rather than *whoever opens the
follow-up row*, which pointed at a row that did not exist.

**The rider names no commit of this branch.** It is stamped `2026-09-08 at
00e63c3`, a commit of `release/v0.9.1` that the squash keeps, and it says so
— #239 is a stamp on a feature-branch commit that stopped resolving the
moment the branch squashed.

## Two things fixed that no finding named

**A real user path in the round's own report.** `round-1-report.md:9` carried
the operator's real home directory in its `Worktree` field, which
`tests/test_no_real_identifiers.py::test_only_fixture_user_paths` refuses —
red on this branch from the moment the record was committed, and it is the
repository rule two history rewrites exist for. Rewritten to `/Users/x/…`.
Only that one cell moved; nothing a reviewer wrote was touched.

**A rider for finding 3's class.** Every regex literal in every shipped
script — 61 patterns across 30 files — was parsed and checked mechanically
for a repetition nested inside another repetition, which is the shape that
lets one input be split exponentially many ways. Four carry one. Three were
timed against inputs built to make them backtrack: `fold_ledger.py:83` and
`evidence_check.py:65` are flat, and
`skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` is **cubic** —
0.71 s at 1000 characters, 15.6 s at 4000, 54 s at 6000, on a run shaped like
a path with no `:<digits>` to finish on.

It was **not** fixed, and that is the judgment. It is polynomial where finding
3 was exponential; nothing this repository holds comes near it (the slowest of
1520 real ledger lines is 0.009 s, on a 1213-character row); and repairing it
means changing which paths a coordinate may name, which 805 ledger rows depend
on — a change with its own argument to make, which a fix pass does not get to
make on the side. It is a `# RIDER:` at the pattern with the measurement in it.

## What I ran

Every exit code was read with `; echo $?`, never through a pipe.

| What was run | Result |
|---|---|
| `FINDING_ID_RE` against `"!" * n + "x"`, shipped pattern | `n=20` 0.043 s · `n=22` 0.171 s · `n=24` 0.702 s · `n=26` 2.844 s · `n=28` 11.178 s |
| `pytest …::test_a_long_punctuation_cell_is_refused_without_hanging` under `timeout 90`, shipped pattern | exit **124** — killed while still running |
| Both patterns over 6245 committed `#` cells and 4368 constructed shapes | **0 disagreements**, acceptance and captured id |
| The repaired pattern against `"!" * n + "x"` | `n=28` 0.000003 s · `n=4000` 0.000132 s · `n=100000` 0.003008 s |
| The two new reach cases against the unfixed predicate | **2 failed, 10 passed** — `pytest only` for the uncollected def, `no call site found` for both root-conftest units |
| `runner_reached` old and new over 3052 top-level defs in 114 tracked files (3051 as run at `824bfca`; see the correction above) | 0 verdicts move in this tree; 4 move among the 11 built placements, all correct |
| Six mutations of `collected`, one at a time | 1 survived, then 0; `restored byte-identical: True` each time |
| `pytest` — the seven generator modules | `282 passed, 2 warnings`, exit **0** |
| `pytest` — `test_evidence_check`, `test_the_reopening_is_one`, `test_a_rider_reaches_its_file`, `test_docs_line_wrap`, `test_no_real_identifiers`, `test_release_hygiene`, `test_a_record_states_what_the_tree_has` | `176 passed, 1 skipped` and **1 pre-existing failure**, exit 1 — see the open items below |
| 61 regex literals across 30 shipped scripts, parsed for nested repetitions | 4 carry one; 3 timed, 1 cubic and unreachable, 1 was finding 3 |
| `bin/evidence-check` before | `805 ok · 4 drifted · 0 broken`, exit **0** |
| `bin/evidence-check --reverify` | 4 rows re-verified, each claim re-read first |
| `bin/deferral-check` | resolves, exit **0** |
| `uvx ruff check` and `uvx ruff format --check`, the changed `.py` only | exit **0** and exit **0** |

## What is open, and who answers it

| Item | Who must answer |
|---|---|
| **`tests/test_a_rider_reaches_its_file.py::test_every_rider_stamp_names_a_commit_this_branch_can_reach` fails**, on a rider at `round_record.py#load` stamped `cedc58e`. That commit lives only on the unmerged `fix/226-round-record-dies-on-python-3-9` and is an ancestor of neither `HEAD`, `origin/release/v0.9.1` nor `origin/main` — it was squashed away as `00e63c3`. Executed. It is **#239 exactly**, it arrived here through the merge at `29e0460`, the release branch is red on it too, and `fix/239-a-stamp-names-content-not-a-commit` is rewriting that very line. Not re-stamped here, because that branch owns the rule and this would collide with it on one comment line | the orchestrator |
| The full suite, the repository-wide `ruff check` and the typecheck — **unverified**. `skills/agent-contract/SKILL.md` §2 reserves the broad gate for one run after the rounds settle. What ran is the table above: fourteen modules, narrowly | the orchestrator |
| `OLD_COORD_RE`'s cubic path half, carried as a `# RIDER:` with its measurement. Repairing it changes which paths a coordinate may name, which 805 ledger rows depend on | the repository owner |
| Whether a reach walk should follow a callable passed as a value at all — `floor_record`'s second cause. Moved from `seal/follow-up.md` to a `# RIDER:` at the line, which is finding 5 | the repository owner |
| Whether `Contract changes` wants the narrowing to non-string literals. `questions.md` Q3, now carrying round 1's measurement: **one entry added across three real ranges**, and that one is the true positive | the repository owner |
| Whether the two committed records that miscount their ids are corrected in place. Round 1 confirmed nothing is blocked | the repository owner |

Nothing in the prompt asked for a check §2 excludes, so there is no declined
instruction to name.
