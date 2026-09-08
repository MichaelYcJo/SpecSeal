# 1788817290-the-derivation-misreads-and-the-record-refuses-the-id — review round 2

| Field | Value |
|---|---|
| Target SHA | a283e64 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed under round 3 |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | conftest_is_loaded (depth 1); MARKER (depth 1); NESTED_CONFTEST (depth 1); VENDORED_CONFTEST (depth 1); EXTRA_MOD (depth 1); test_the_fixture_repository_only_widens_signatures (depth 1); test_a_conftest_nothing_is_collected_under_is_not_loaded (depth 1); test_the_directory_decides_inside_tests_as_well (depth 1); test_a_sibling_whose_name_extends_the_directory_is_not_below_it (depth 1) |
| Needs a fix | yes — 1 and 2 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` (tickets #211, #194, #227), at target `a283e64`, base `origin/release/v0.9.1`. The verifying round over round 1's fixes, whose substance is `824bfca`, `a77ef92`, `4dfde1d` and `f8180f4`.

Round 1's verdicts were inherited. It had reproduced every one of the build's six load-bearing claims and opened only where the code stopped short of its own prose: a `test_*` def in a file pytest never collects reading `pytest only`, a root `conftest.py` reading `no call site found`, and `FINDING_ID_RE` backtracking exponentially so `close` hangs instead of refusing.

The named targets. Finding 3 was a hang and the repair is one character, so the claim that the accepted LANGUAGE is unchanged — measured over 6245 `#` cells in every committed record and 4368 constructed shapes — was to be re-derived and both patterns re-timed, since a one-character regex change that is obviously equivalent is exactly the claim worth a second measurement. Findings 1 and 2 moved the boundary, and the re-enumeration over 3051 defs in 114 files reporting that not one verdict in this repository moves was to be re-derived, then the stated cost attacked: `src/conftest.py#a_nested_fixture` now reads `pytest only` though pytest never collects `src/`, and whether that is an acceptable price or a new instance of #211's own defect pointing the other way. The one mutation that survived the first sweep — the `_test.py` half of `collected`, because the built repository had no suffix-named module — was to be re-run, since a case written to kill a mutation sometimes pins the mutation rather than the property. Finding 3's class was enumerated mechanically over 61 regex literals in 30 shipped scripts, with `evidence_check.py#OLD_COORD_RE` reported cubic and deliberately not repaired because 805 ledger rows depend on which paths a coordinate may name; that disposition and its unreachability claim were both to be judged. A record had carried a real home directory and was corrected, to be checked for completeness. Any `# RIDER:` must not name a commit of this branch, and the round was told that `fix/239-a-stamp-names-content-not-a-commit` migrates every stamp to a content anchor on the same release, so the two branches touch one convention. And `seal/ledger.md`'s four re-verified anchors were to be opened claim by claim.

The bound was stated: round 1 met the floor, a round that opens nothing needing a fix does not consume the cap, and neither manufacturing nor softening a finding was acceptable. The report was to be a file, finding ids bare integers, one row per finding, no real user path, and `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Letting a `conftest.py` through from anywhere makes the predicate say `pytest only` about a fixture in a directory pytest never loads a conftest from — round 1's finding 1 pointing the other way, at every depth rather than at the one placement the fix pass built | `skills/code-review/scripts/round_record.py:2011` | **fixed** `69a3967` | fixed at 69a3967 — ``; executed — `src/conftest.py#a_nested_fixture` and `a/b/conftest.py#deep_fixture` both move to `pytest only` through the shipped predicate; pytest loads a conftest only for tests collected at or below its own directory, so neither is imported in a tree whose tests live under `tests/`. The grounds the ledger fragment and `round-1-fixes.md` give — *pytest's by construction wherever it sits* — are false of pytest |
| 🟡 2 | The rider that closed round 1's finding 5 sits under `tests/`, which the rider checks do not walk, so neither the stamp check nor the ancestry check can see it — the failure the list's own comment records for `templates` | `tests/test_a_rider_reaches_its_file.py:109` | **fixed** `df9a3d0` | fixed at df9a3d0 — ``; executed — the roots are `hooks`, `skills`, `agents`, `templates`; `grep -rn "RIDER:" tests/` returns four files, one of them the rider this branch planted. Adding `tests` turns the stamp check red on an unstamped rider at `tests/test_the_records_can_be_carried_out_and_in.py:1415` and on the literal `"# RIDER:"` inside an assertion at `tests/test_the_root_migrates_itself.py:442`, so the repair is three parts |
| ⬜ 3 | One enumeration is reported with three different totals — 3048 in `824bfca`'s message, 3051 in the fixes record, the ledger fragment and the rider, 3052 in the tree the rider was written against | `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md:4` | **fixed** `1742dcf` | fixed at 1742dcf — ``; executed — top-level defs per SHA: `ffd1d05` 3003, `824bfca` 3051, `4dfde1d` 3052, `f8180f4` 3052, `a283e64` 3052. 3051 was true when `824bfca` was written and stopped being true when `4dfde1d` added a case; 3048 was never true on this branch. The conclusion the numbers carry — no verdict moves — reproduces at 3052 |
| ⬜ 4 | The `OLD_COORD_RE` rider's reachability measurement does not reproduce: it records 0.009 s on a 1213-character row as the worst the tree holds, and the worst is 0.000537 s on an 8831-character row | `skills/evidence-check/scripts/evidence_check.py:77` | **fixed** `1742dcf` | fixed at 1742dcf — ``; executed — 1520 real ledger lines timed three times each; the 19 rows in the 1150–1280 character band top out at 0.000172 s. The claim the rider makes is unreachability and that direction holds with a wider margin than stated, so what is wrong is the number rather than the judgment |
| 🟢 5 | Round 1's findings 1, 2 and 3 are closed, each re-derived rather than read: the language is unchanged over 7768 strings, both patterns re-timed, and no verdict in this repository moves under the widened predicate | `skills/code-review/scripts/round_record.py:1646`, `:1980`, `:2011` | answered | executed — see *What reproduced, claim by claim* |
| 🟢 6 | The mutation that survived the fix pass's first sweep is killed, and the case that kills it pins the property rather than the mutation | `tests/test_a_runner_reached_unit_reads_pytest_only.py:370` | answered | executed — both halves of `collected` dropped separately, each killed by exactly one case, and the new case asserts pytest's second `python_files` pattern as a property |
| 🟢 7 | Round 1's findings 4 and 5 are closed, both riders name a commit the squash keeps, no record carries a real user path, and the four re-verified anchors hold their claims | `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md`, `seal/follow-up.md:44`, `tests/test_the_reopening_is_one.py:164` | answered | executed — `bin/evidence-check` 809 ok, 0 drifted, 0 broken, exit 0; `00e63c3` an ancestor of `origin/release/v0.9.1` and not of `origin/main`; `tests/test_no_real_identifiers.py` green and the tree carries no real home directory |
| ❓ 8 | The full suite, the repository-wide lint and the typecheck | the branch as a whole | answered | The broad gate, which `agent-contract` §2 reserves for the orchestrator. Run at this SHA after `release/v0.9.1` was merged in: **`2623 passed, 2 skipped`**, `ruff check .` and `ruff format --check .` both exit 0. One record check was red beforehand and is not this fix pass's — `round-1.md`'s `Contract changes` and `New units` still read *the fixes are not yet written* while `Fixes checked by` already named round 2; the orchestrator filled both cells from round 2's own report in the closing commit |

## Paste-ready fixes

```python
def conftest_is_loaded(root, b, rel):
    """True when pytest loads this `conftest.py` at all.

    A conftest is loaded for the test files collected at or below its own
    directory — rootdir down to each test file, with `confcutdir` defaulting
    to rootdir — so one in a directory nothing is collected under is never
    imported and its fixtures are injected into nothing. Saying `pytest only`
    about a unit there is round 1's finding 1 pointing the other way: the
    repository root passes this in any tree that has tests at all, which is
    finding 2's placement, and `src/conftest.py` passes it in a colocated
    layout and fails it in a segregated one, which is what pytest does.
    """
    here = os.path.dirname(rel)
    prefix = f"{here}/" if here else ""
    return any(
        p.startswith(prefix) and p.endswith(".py") and collected(os.path.basename(p))
        for p in tracked_at(root, b)
    )
```
```python
    base = os.path.basename(rel)
    if not rel.endswith(".py"):
        return False
    if not under_tests(rel) and not (
        base == CONFTEST and conftest_is_loaded(root, b, rel)
    ):
        return False
```
```python
    Where the file sits decides two different things, and they are not the
    same gate. A conftest is loaded by name rather than by directory, so the
    `tests/` gate lets one through from anywhere pytest would actually load
    it — the directories with a collected test module at or below them, which
    is the repository root in any tree that has tests. A conftest nothing is
    collected under is not loaded, so it is not a member either. Nothing else
    outside `tests/` is a member however it is named.
```
```python
# The other half of finding 2's repair. pytest loads a conftest for the tests
# collected at or below its own directory, so one under `src/` in a tree whose
# tests live under `tests/` is never imported — and `pytest only` about its
# fixture is finding 1's false sentence at a second placement.
NESTED_CONFTEST = (
    "import pytest\n"
    "\n"
    "\n"
    "@pytest.fixture\n"
    "def a_nested_fixture(x):\n"
    "    return x\n"
)
```
```python
    "src/conftest.py": (
        "import pytest\n"
        "\n"
        "\n"
        "@pytest.fixture\n"
        "def a_nested_fixture(x, extra=None):\n"
        "    return x\n"
    ),
```
```python
def test_a_conftest_nothing_is_collected_under_is_not_loaded(reach):
    """Round 2's finding 1. `conftest.py` is a name pytest loads by, but the
    directory still decides whether it is loaded at all: rootdir down to each
    collected test file. `src/` holds no test module, so this conftest is
    never imported and its fixture is injected into nothing — the row would
    say the runner covers a unit nothing covers, which is the sentence
    `plan.md`'s alternatives table rejected the wider rule to avoid."""
    generator = generator_module()
    assert reach["a_nested_fixture"] == generator.NO_SITE, reach
```
```markdown
| a fixture under `tests/`, or in a `conftest.py` pytest loads | injected by parameter name, so `name(` never occurs |
| a `pytest_*` def in a `conftest.py` pytest loads | dispatched by the plugin manager |
```
```markdown
`conftest.py` is the opposite case: pytest loads it by name and documents the
repository root placement first, so a fixture or a hook there is reached from
outside `tests/` exactly as one inside it is. It is still the directory that
decides whether the file is loaded at all — rootdir down to each collected
test file — so a `conftest.py` with no test module at or below it is loaded by
nobody, and calling its fixtures the runner's is the same false sentence one
directory over. Both directions were round 1's findings on the change that
introduced this section, and the second one came back in the repair.
```
```markdown
**What letting a conftest through costs, and where the line now sits:** a
conftest is loaded for the tests collected at or below its own directory, so
the reach walk asks that question of the tracked file list rather than
accepting the name alone. The repository root passes it in any tree that has
tests, which is the placement #211's own defect stood at; `src/conftest.py`
in a tree whose tests live under `tests/` does not, because pytest never
imports it. Round 2's finding 1 is that accepting the name alone put finding
1's false sentence back at every uncollected directory.
```
```python
# Where riders are allowed to live. `templates` was missing, so the rider in
# `templates/evidence-check.yml` was never checked by anything at all —
# `follow-up.md` names it as planted and nothing here could see it. `tests`
# was missing for the same reason and one release longer: four files under it
# carry riders, one of them planted by the branch that fixed #239's instance,
# and neither the stamp check nor the ancestry check could see any of them.
RIDER_ROOTS = ["hooks", "skills", "agents", "templates", "tests"]
```
```python
    for rel in {line.split(":", 1)[0] for line in out.splitlines()}:
        block = read(os.path.join(ROOT, rel))
        # A `# RIDER:` inside a string literal is a case asserting that a
        # rider exists somewhere else, not a rider. `tests/test_the_root_
        # migrates_itself.py` carries one, and splitting on the bare text
        # read it as a rider with no stamp.
        for chunk in re.split(r"^\s*# RIDER:", block, flags=re.M)[1:]:
            head = chunk.split("\n\n", 1)[0]
            m = STAMP.search(head)
            assert m, f"{rel}: a rider with no verification stamp"
            found.append((rel, m.group(1)))
```
```python
# Verified 2026-09-03 at 3f8f846.
```

## Executed probes

| What was run | Result |
|---|---|
| `FINDING_ID_RE` at `ffd1d05` and at `a283e64` against `"!" * n + "x"` | old `n=20` 0.042883 s · `n=22` 0.171534 s · `n=24` 0.695899 s · `n=26` 2.836958 s · `n=28` 11.392153 s; new 0.000006–0.000009 s at every one, 0.000141 s at 4000, 0.003217 s at 100000 |
| Both patterns over 6305 record cells from 149 committed records, 1463 constructed shapes, and an exhaustive marker-prefix sweep | **0 disagreements** over 7768 strings, on acceptance and on the captured id |
| `runner_reached` at `ffd1d05` and at `a283e64` over 3052 top-level defs in 114 tracked `.py` files at `a283e64` | **0 verdicts move** |
| Thirteen built placements through both predicates | 5 move: the three round 1 opened, plus `src/conftest.py#a_nested_fixture` and `a/b/conftest.py#deep_fixture` — finding 1 |
| `collected` mutated to `base.startswith(TEST_PREFIX)`, `tests/__pycache__` cleared | `1 failed, 12 passed` · `test_the_second_python_files_pattern_collects_too` alone, exit 1 |
| `collected` mutated to `base.endswith(TEST_SUFFIX)`, `tests/__pycache__` cleared | `1 failed, 12 passed` · `test_a_pytest_test_function_reads_pytest_only` alone, exit 1 |
| `git status --porcelain` after both mutations were restored | empty |
| `bin/test tests/test_a_runner_reached_unit_reads_pytest_only.py tests/test_a_finding_id_is_a_bare_integer.py tests/test_no_real_identifiers.py tests/test_a_rider_reaches_its_file.py tests/test_the_reopening_is_one.py -q` | `87 passed, 1 skipped in 33.14s`, exit **0** |
| `OLD_COORD_RE` against `"a." + "b/" * n` | len 502 0.0315 s · 1002 0.2521 s · 2002 1.9545 s · 4002 15.7004 s — eight times the work per doubling, cubic |
| `OLD_COORD_RE` over all 1520 lines of `seal/ledger.md` and the `seal/ledger/*.md` fragments | slowest **0.000537 s**, `seal/ledger.md:1356`, 8831 characters; the 19 rows of 1150–1280 characters top out at 0.000172 s |
| The five compiled patterns in `hooks/review-history-guard.py` against adversarial input at four lengths | linear, 0.00006 s or less at 6424 characters |
| Independent scan of the 30 shipped scripts for a repetition nested in a repetition | 47 plain literals found against the record's 61; concatenated patterns are outside this scanner, so the count of 4 is neither confirmed nor contradicted |
| Top-level def counts per SHA | `ffd1d05` 3003 · `824bfca` 3051 · `4dfde1d` 3052 · `f8180f4` 3052 · `a283e64` 3052 |
| `measure` and `call_sites` over `29e0460..f8180f4` and over `ffd1d05..a283e64` | branch-only: 0 contract changes, 9 new units. Whole range: 2 contract changes, both `seal.py` units the merge brought, and 69 new units |
| `git merge-base --is-ancestor 00e63c3 …` against `HEAD`, `origin/release/v0.9.1`, `origin/main` | 0, 0, 1 — a release-branch commit the squash keeps, absent from `main` |
| `evidence_check.content_hash` over the two riders' anchored regions | `floor_record` at lines 179–181 hashes to bba5c7a1; `OLD_COORD_RE` at lines 91–94 hashes to 1ca5aff0 |
| `grep -rn` for the operator's home directory across the worktree | one hit, the untracked `.git` worktree pointer; no tracked file carries one |
| `bin/evidence-check` | `809 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit **0** |
| `bin/deferral-check` | resolves, exit **0** |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `OLD_COORD_RE`'s cubic path half — repairing it changes which paths a coordinate may name, and 805 ledger rows depend on that | a `# RIDER:` at the pattern with its measurement, `skills/evidence-check/scripts/evidence_check.py:77` — already deferred by the fix pass; finding 4 corrects the measurement inside it, not the judgment | the repository owner |
| Whether a reach walk should follow a callable passed as a value at all | a `# RIDER:` at `tests/test_the_reopening_is_one.py:164` — already deferred; finding 2 is about the rider being unwatched, not about reopening the decision | the repository owner |
| Whether `Contract changes` wants the narrowing to non-string literals | `questions.md` Q3 — already deferred, carrying round 1's measurement of one added entry across three real ranges | the repository owner |
| Whether the two committed records that miscount their finding ids are corrected in place | `overview.md` §*Not verified* — already deferred; nothing is blocked | the repository owner |
| Which of `fix/239-a-stamp-names-content-not-a-commit` and this branch rewrites the other's two rider stamps, since both touch the convention on the same release | named here, with the anchor each rider should carry | the orchestrator |
| The full suite, the repository-wide lint and the typecheck | `skills/agent-contract/SKILL.md` §2 — the broad gate is one run after the rounds settle | the orchestrator |
