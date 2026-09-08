# 1788817290-the-derivation-misreads-and-the-record-refuses-the-id — review round 3

| Field | Value |
|---|---|
| Target SHA | fcb0421 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed after `release/v0.9.1` was merged in — 2661 passed, 2 skipped; `ruff check .` and `ruff format --check .` both exit 0 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 1 and 2 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` (tickets #211, #194, #227), at target `fcb0421`, base `origin/release/v0.9.1`. The verifying round over round 2's fixes, whose substance is `69a3967`, `df9a3d0` and `1742dcf`, and the last round this work item gets: rounds 1 and 2 both closed on fixes, so the record after this one ends the run whatever it finds.

Round 2's fix pass had found more than the round handed it, and each of those was named as a target. Seven conftest placements read `pytest only` where pytest imports nothing, not the two round 2 named, and one of the seven passes round 2's own paste-ready shape — so the report's fix was insufficient and the seven were to be re-derived with an eighth looked for. The boundary it wrote — a conftest is loaded by name, and the directory decides whether pytest loads it at all — was to be verified against real pytest behaviour rather than against the sentence. One mutation had survived the first sweep, a directory prefix losing its trailing slash, invisible because no two fixture directories had names where one extends the other. `RIDER_ROOTS` widened by one word had exposed three offenders, the first being the check's own file, whose prose about the marker enters the corpus it walks; the other two were a module with no stamp at all and one stamped at a commit the squash had already dropped, which is #239 arriving as a corpus rather than an argument. And #239 replaces that whole block over six roots, so the cross-run of its checker against this tree was to be verified, because a wrong answer there is a merge conflict resolved in the wrong direction.

The interesting one nothing had named: the `floor_record` rider claimed the repaired predicate had been re-run and still found that def the only survivor, and it had not been — the survivor moved, because this work item's own records quote its `def` line and `call_sites` greps every tracked file, so a committed record quoting code invents a call site.

Two further findings were handed over mid-round by round 1's warden, which had woken on a stale replay of its own prompt and re-derived them at this SHA: a unit whose name is not unique getting the whole repository as its reach, `hooks/dispatch.py#main` returning 44 entries of which six were documents this branch wrote; and #211's own *Not verified* naming a fourth candidate that no record answers. Both were to be judged rather than accepted, with `deferred #N` the disposition since the cap was spent.

The report was to be a file, finding ids bare integers, one row per finding, no real user path, `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry, and no literal HTML comment marker outside a real one.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `pytest_*` def in a conftest with nothing collected under it now reads `no call site found`, and pytest registers that conftest and calls its session hooks on every run — #211's own sentence at a third placement, inside the repair for the second | `skills/code-review/scripts/round_record.py:2033` | deferred #247 | executed — real pytest called `pytest_configure` and `pytest_collection_modifyitems` from three conftests with no collected test under them; four `pytest_*` defs read `True` at `a283e64` and `False` at `fcb0421`; a probe case planting one hook in `tests/vendor/conftest.py` is red at HEAD and green under the repair, sixteen other cases green in both |
| 🟡 2 | The new sibling case asserts `NO_SITE` for a module pytest collects, and the assertion kills no mutation — deleting it, and deleting the whole case, both leave the trailing-slash mutation killed | `tests/test_a_runner_reached_unit_reads_pytest_only.py:456` | deferred #247 | executed — `src_extra/test_in_a_sibling.py::test_in_a_sibling` is in pytest's collect list; the mutation is killed by the fixture FILE, not by the case |
| 🟡 3 | The non-conftest arm gates on `under_tests`, where `docs/review-chain-spec.md:752` keys the same row on `python_files` collection — every test function in a colocated repository reads `no call site found` | `skills/code-review/scripts/round_record.py:2035` | deferred #247 | executed — `pkg/test_beside_the_code.py::test_beside_the_code` collected and read `False` at both SHAs; no instance in this tree, `git ls-files` finds no collected module outside `tests/` |
| 🟡 4 | `call_sites` greps bare text, so a unit whose name is not unique gets the whole repository as its reach and the number rises when somebody writes a document | `skills/code-review/scripts/round_record.py:2076` | deferred #247 | executed — `hooks/dispatch.py#main` 38 entries at `ffd1d05`, 44 at `fcb0421`, the six added all documents this branch wrote; 12 of 44 are prose basenames; all 13 tracked `hooks/*.py` defining `main` return the identical set. `questions.md` Q3 asks about row count and the cost is inside one cell |
| ⬜ 5 | #211's *Not verified* named a hook module's `main` as a fourth candidate; `plan.md`'s class table has no row for it and no round record answers it | `seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/plan.md:60` | deferred #247 | executed — it is not a member, and the reason is finding 4 rather than anything about the class; grepped the work item, the ledger fragment, `spec.md` and `docs/review-handoff-protocol.md` for an answer and found none |
| ⬜ 6 | 3052 stopped being true at the first fix commit, and three of the four sites carrying it name no tree — round 2's finding 3 recurring inside its own fix | `tests/test_the_reopening_is_one.py:174` | answered | executed — 3052 at `a283e64` and `59dc0e4`, **3056** at `69a3967` through `fcb0421`; only `round-1-fixes.md` names the tree it counted. The conclusion is unaffected: re-derived at `fcb0421`, no verdict in this repository moves |
| ⬜ 7 | `RIDER_ROOTS` gained `tests` and left `.github` out, where a real stamped rider sits unwatched for the same reason | `tests/test_a_rider_reaches_its_file.py:117` | deferred #247 | executed — `.github/scripts/fold_ledger.py:163` carries a rider stamped `881fb0f`, an ancestor of HEAD; adding `".github"` leaves the module green at `8 passed`, exit 0. Grounds for leaving it are stated and hold: #239 covers six roots and every hunk sits inside the block it replaces |
| ⬜ 8 | The `call_sites` deferral is stated in three documents and `call_sites` itself carries no marker, where the rule round 1 established puts a coordinate-tied deferral at the line | `skills/code-review/scripts/round_record.py:2064` | deferred #247 | read — the rider, the ledger fragment's R2 Notes and `overview.md` §*Not verified* all name it with the repository owner as answerer; executed — `bin/deferral-check` resolves, exit 0. The disposition is right; only its placement is short |
| ⬜ 9 | `conftest_is_loaded` calls the uncached `tracked_at` once per conftest unit, so each one spawns a full `git ls-tree -r` over the tree | `skills/code-review/scripts/round_record.py:2017` | deferred #247 | read — the module's only other `tracked_at` call is once per record at `:2284`, and no `functools` import exists; not measurable in this tree, which holds one conftest |
| 🟢 10 | Round 2's finding 1 is closed for the fixture arm, the conftest class re-derived at seventeen placements in two layouts, and the mutation sweep reproduces | `skills/code-review/scripts/round_record.py:1995`, `tests/test_a_runner_reached_unit_reads_pytest_only.py:423` | answered | executed — see *Executed probes*; the eighth placement asked for is `other/conftest.py` beside a colocated `pkg/`, and it is handled |
| 🟢 11 | Round 2's finding 2 is closed, `STAMP` accepts both forms with the anchor skipped by the ancestry case, no stamp line carries a path, and #239's checker agrees at four | `tests/test_a_rider_reaches_its_file.py:137`, `tests/test_the_reopening_is_one.py:188` | answered | executed — `4 ok · 0 drifted · 18 broken`, exit 2, from #239's checker at `d069d54`; the 18 are pre-#239 commit stamps and `round_record.py:200`'s was written by `2138c98`, not this branch |
| 🟢 12 | Round 2's finding 4 is closed and the corrected worst case reproduces independently | `skills/evidence-check/scripts/evidence_check.py:98` | answered | executed — worst 0.000527 s at `seal/ledger.md:1356`, 8831 chars; the 19 rows of 1150–1280 chars top out at 0.000167 s; `bin/evidence-check` 815 ok, 0 drifted, exit 0 |
| ❓ 13 | The full suite, the repository-wide lint and the typecheck | the branch as a whole | answered | `agent-contract` §2 — the orchestrator answers it. Five narrow modules ran here: `176 passed, 1 skipped`, exit 0 |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:1868` | round 1's 🟡 1 — open |
| round-1 | `skills/code-review/scripts/round_record.py:1858` | round 1's 🟡 2 — open |
| round-1 | `skills/code-review/scripts/round_record.py:1514` | round 1's 🟡 3 — open |
| round-1 | `tests/test_a_new_returnable_value_is_a_contract_change.py:52` | round 1's ⬜ 4 — open |
| round-1 | `seal/follow-up.md:44` | round 1's ⬜ 5 — open |
| round-1 | `skills/code-review/scripts/round_record.py`, `tests/` | round 1's 🟢 6 — answered |
| round-1 | `seal/ledger.md`, `skills/code-review/scripts/round_record.py:2156` | round 1's 🟢 7 — answered |
| round-1 | the branch as a whole | round 1's ❓ 8 — open |
| round-2 | `skills/code-review/scripts/round_record.py:2011` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_a_rider_reaches_its_file.py:109` | round 2's 🟡 2 — fixed |
| round-2 | `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md:4` | round 2's ⬜ 3 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:77` | round 2's ⬜ 4 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:1646`, `:1980`, `:2011` | round 2's 🟢 5 — answered |
| round-2 | `tests/test_a_runner_reached_unit_reads_pytest_only.py:370` | round 2's 🟢 6 — answered |
| round-2 | `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md`, `seal/follow-up.md:44`, `tests/test_the_reopening_is_one.py:164` | round 2's 🟢 7 — answered |

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
