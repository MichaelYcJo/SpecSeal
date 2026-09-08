# 1788817290-the-derivation-misreads-and-the-record-refuses-the-id — review round 1

| Field | Value |
|---|---|
| Target SHA | ffd1d05 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed at 31329cc — see round 2, finding 8 |
| Fixes checked by | round-2 |
| Contract changes | none from this branch's own commits (`29e0460..f8180f4`) |
| New units | TEST_SUFFIX (depth 1); collected (depth 1); HELPERS (depth 1); SUFFIX_MOD (depth 1); ROOT_CONFTEST (depth 1); test_a_long_punctuation_cell_is_refused_without_hanging (depth 1); test_a_conftest_at_the_repository_root_is_still_a_conftest (depth 1); test_a_test_shaped_def_in_an_uncollected_module_is_not_the_runners (depth 1); test_the_second_python_files_pattern_collects_too (depth 1) |
| Needs a fix | yes — 1, 2, 3 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` (tickets #211, #194, #227), at target `ffd1d05`, base `86e140f`. No prior rounds, and no pull request open — the orchestrator opens it after this round.

The branch answers three tickets on one derivation in one file. #227 replaced `NUMBER_RE` with one `finding_number` serving both `fix_table` and `verdict_rows`, and made the refusal name the format, quote the cell, quote the whole row, and quote both rows on a real duplicate. #211 added `runner_reached` and `decorated_as`, asked at `call_sites`' empty-reach branch, so a unit the runner reaches reads `pytest only`. #194 added `return_literals` and widened the contract tuple to `(signature, return_arities, return_literals)`, with literals keyed by type as well as value because Python hashes `0`/`False` and `1`/`True` together.

Six load-bearing claims were named to re-derive rather than read. #227's corpus measurement — 130 committed records, 82 passing either rule, 46 already refused, and 2 passing today while mis-keyed — with the claim that the new rule takes only wrong answers and no right ones, so a single right one taken would be a finding. #211's class, enumerated by running `call_sites` over every top-level def under `tests/` rather than by reading, and the claim that the ticket's own suggested repair would have left eight fixtures behind. The boundary #211 deliberately did not cross, where `floor_record` is passed as a value and never called so `no call site found` is correct for it. #211's stated limit, that the hook branch reads `conftest.py` only, judged for whether a limit is the right disposition or a hole wearing a limit's clothes. #194's hole, guarded by a case asserting the contract does NOT change across the measured example, verified by actually widening the check and watching the case go red. #194's historical instance, `chain_check.py#read_record` returning an explicit `None` between v0.8.0 and v0.8.3 with signature and arity unchanged. And the one surviving mutation recorded as equivalent rather than killed, verified rather than accepted.

Also named: the five `seal/ledger.md` rows re-verified after re-reading, which the repository rule permits only where a branch changes cited code and the claim still holds; the noise question, since widening `Contract changes` to returnable literals makes the row fire more often, with the count on this release's own diffs asked for; and the two committed records the strict parse stops on, for whether they block anything and who answers.

`tests/test_the_records_can_be_carried_out_and_in.py`'s four failures were named as not this branch's — #111's timezone defect, already fixed on the branch that merges first — and were not to be opened.

The report was to be written to a file, finding ids bare integers, every verdict row carrying one, and no finding carrying two rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `pytest only` is written for a `test_*` def in a file pytest never collects, which is the row saying the runner covers a unit nothing covers — the sentence `plan.md`'s alternatives table rejected the wider rule to avoid | `skills/code-review/scripts/round_record.py:1868` | open | executed — a built repository with `tests/helpers.py#test_thing` uncalled gives `['pytest only']`; pytest's `python_files` default is `test_*.py *_test.py` and the arm reads only the def name and the directory |
| 🟡 2 | A `conftest.py` outside `tests/` reaches neither the fixture arm nor the hook arm, so a root-level fixture and a root-level `pytest_configure` still read `no call site found` — #211's own defect at pytest's most common placement, and not among the limits the branch wrote down | `skills/code-review/scripts/round_record.py:1858` | open | executed — two built repositories with a root `conftest.py`, one fixture and one hook, both give `['no call site found']`; `docs/review-chain-spec.md:765` records only the collected-test-module limit |
| 🟡 3 | `FINDING_ID_RE` backtracks exponentially, so a `#` cell of punctuation ending in a non-digit hangs `close` and `new` instead of refusing with the format named | `skills/code-review/scripts/round_record.py:1514` | open | executed — 0.177 s at 22 characters, 2.928 s at 26, 11.432 s at 28, doubling per character; the one-character repair keys 16 shapes identically and refuses 4000 characters in 0.00014 s |
| ⬜ 4 | The whole-tree cross-check is called an INDEPENDENT implementation in the ledger fragment and a second implementation in the phase record, and `literals_of` is the shipped `return_literals` loop character for character | `tests/test_a_new_returnable_value_is_a_contract_change.py:52` | open | read — the two bodies differ only in the order of one assignment and a `list()` call; the genuinely independent half is the 21 constructed pairs' hand-written expectation column |
| ⬜ 5 | The `floor_record` deferral is a bullet under an empty table, in the section for items another branch holds, where the file's own rule sends a coordinate-tied item to a `# RIDER:` comment | `seal/follow-up.md:44` | open | read — the section's table has a header, a separator and no rows; `overview.md` names the answerer as *whoever opens the follow-up row* and no row exists; `seal/follow-up.md:15` states the rider rule |
| 🟢 6 | #227's corpus measurement, #211's class enumeration and its `floor_record` boundary, #194's `v0.8.0..v0.8.3` instance, the hole's guard under a real widening, and the equivalent mutation | `skills/code-review/scripts/round_record.py`, `tests/` | answered | executed — all six re-derived here and reproduced exactly; see *What reproduced, claim by claim* |
| 🟢 7 | The five re-verified rows of `seal/ledger.md` still hold their claims, and the two committed records that stop the strict parse block nothing | `seal/ledger.md`, `skills/code-review/scripts/round_record.py:2156` | answered | executed — `bin/evidence-check` reads 776 rows with 0 drifted and 0 broken; each claim opened; `verdict_rows` has one caller and `chain_check.py` does not read the `#` column with this rule |
| ❓ 8 | The full suite, the repository-wide lint and the typecheck | the branch as a whole | open | unverified — contract §2 reserves the broad gate for one run after the rounds settle. Executed here: the three new modules and eight neighbouring ones. The answerer is the orchestrator |

## Paste-ready fixes

```python
TEST_PREFIX = "test_"
TEST_SUFFIX = "_test.py"
HOOK_PREFIX = "pytest_"
CONFTEST = "conftest.py"
FIXTURE = "fixture"
```
```python
def collected(base):
    """True when pytest's default `python_files` patterns import this file.

    Collection is two rules, not one: `python_files = test_*.py *_test.py`
    decides which FILE becomes a test module, and `python_functions = test_*`
    decides which def inside it is a case. A `test_*` def in
    `tests/helpers.py` satisfies the second and not the first, so pytest
    never runs it — and `pytest only` would then say the runner covers a unit
    nothing covers.
    """
    return base.startswith(TEST_PREFIX) or base.endswith(TEST_SUFFIX)
```
```python
        if name.startswith(TEST_PREFIX) and collected(base):
            return True
```
```python
def runner_reached(reader, root, b, rel, name):
    """True when pytest reaches `rel`'s `name` with no call site in the tree.

    The three members are the constants above, and each is a rule of pytest's
    own collection rather than a convention of this repository: a def that
    `python_files` collects and `python_functions` names is a case, a fixture
    is injected by parameter name, and a `pytest_*` def in a `conftest.py` is
    dispatched as a hook. A conftest is a conftest wherever it sits — pytest
    documents the repository root first — so the `tests/` gate lets one
    through from anywhere; nothing else outside `tests/` is a member however
    it is named.
    """
    base = os.path.basename(rel)
    if not rel.endswith(".py"):
        return False
    if not under_tests(rel) and base != CONFTEST:
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
        return decorated_as(node, FIXTURE)
    return False
```
```python
def test_a_test_shaped_def_in_an_uncollected_module_is_not_the_runners(reach):
    """`python_files` is the other half of collection. A `test_*` def in
    `tests/helpers.py` is never imported as a test module, so saying `pytest
    only` about it is the row claiming the runner covers a unit nothing
    covers — the sentence the wider rule was rejected for."""
    assert reach("tests/helpers.py", "test_thing") == ["no call site found"]


def test_a_conftest_at_the_repository_root_is_still_a_conftest(reach):
    """pytest documents the root placement first, and a fixture there is
    injected by parameter name exactly as one under `tests/` is."""
    assert reach("conftest.py", "a_root_fixture") == ["pytest only"]
    assert reach("conftest.py", "pytest_configure") == ["pytest only"]
```
```markdown
| The unit | How pytest reaches it |
|---|---|
| a `test_*` def in a module `python_files` collects | collected by name pattern, file and function both |
| a fixture under `tests/` or in a `conftest.py` | injected by parameter name, so `name(` never occurs |
| a `pytest_*` def in a `conftest.py` | dispatched by the plugin manager |
```
```python
# A finding id is a bare integer, optionally behind a severity marker. #227:
# the id used to be the FIRST digit run anywhere in the cell, so `R2-1` and
# `R2-2` both read as `2` and eight round-prefixed findings collapsed toward
# one key. The refusal that followed reported a duplicate the table did not
# visibly have. The marker is what the group skips and the digits are the id;
# `[^\w\s]` reaches every marker the records carry — 🔴 🟡 🟢 ⬜ ❓ ✅ — and
# reaches no letter, so `r3 🟡 2`, `1-1`, `1b` and `A2` are refused rather
# than silently keyed to whichever digits came first.
#
# The repetition takes ONE marker character, not a run of them. `[^\w\s]+`
# inside the `*` group let a run of punctuation be split in exponentially
# many ways, and a cell ending in a non-digit made the engine try all of
# them: 22 characters took 0.18 s to refuse, 26 took 2.9 s, 28 took 11.4 s,
# and each further character doubles it. The language is unchanged — every
# repetition already consumes one marker — and a 4000-character run now
# refuses in 0.00014 s.
FINDING_ID_RE = re.compile(r"^(?:[^\w\s]\s*)*(\d+)$")
```
```python
def test_a_long_punctuation_cell_is_refused_without_hanging():
    """The refusal is the deliverable, so it has to arrive. A `#` cell of
    punctuation ending in a non-digit used to send the pattern exponential:
    11.4 s at 28 characters, doubling per character, with `close` producing
    nothing and never returning."""
    generator = generator_module()
    start = time.monotonic()
    assert generator.FINDING_ID_RE.match("!" * 4000 + "x") is None
    assert time.monotonic() - start < 1.0, "the pattern is backtracking"
```
```markdown
Cross-checked twice, and the two halves are not the same kind of check. A
second copy of the rule in the test file is compared unit by unit over every
top-level def in every tracked `.py` file — a transcription of the shipped
loop, so what it holds is the shipped derivation against later drift, not a
blind spot — and the count of units actually carrying a literal is asserted
beside it, so an always-empty derivation could not pass. The independent
statement is the 21 constructed before/after pairs, whose expectation column
is a hand-written judgment of what should be reported per shape rather than a
reading of the code, and it is what covers the nested-scope boundaries and
the bare `return`.
```
```markdown
**The cross-check is two halves, and only one of them is independent.** The
whole-tree comparison runs a transcription of the shipped loop over every
top-level def in every tracked `.py` file; two copies of one algorithm agree
by construction, so what it catches is a later edit to one of them. The half
that could have caught a blind spot is the 21 constructed pairs, whose
expectation column is hand-written rather than derived, and which is where
the nested-scope boundaries and the bare `return` are pinned.
```
```python
# RIDER: `no call site found` has a second cause and #211 repaired only the
# first. This def is passed by name as a value at five sites and never
# called, so the `name(` that `round_record.py#call_sites` greps for occurs
# nowhere but the line below — 1 of 483 helpers under `tests/`, enumerated at
# ba22b28. Reading a bare `name` in an argument position would reach it and
# would also name every mention of the word, so the repair is not the one
# #211 took. If you open this file, decide whether a reach walk should follow
# a callable passed as a value at all. Verified 2026-09-08 at ffd1d05.
def floor_record(sha):
```
```markdown
| `no call site found` has a second cause, and #211 repaired only the first. `tests/test_the_reopening_is_one.py#floor_record` is passed by name as a value at five call sites and never called, so the `name(` the reach walk greps for occurs nowhere but its own `def` line — 1 of 483 helpers under `tests/`, enumerated at `ba22b28`. Reading a bare `name` in an argument position would reach it and would also name every mention of the word, so the repair is not the one #211 took. The decision is whether a reach walk should follow a callable passed as a value at all | the repository owner |
```

## Executed probes

| What was run | Result |
|---|---|
| `.venv/bin/python -m pytest tests/test_a_finding_id_is_a_bare_integer.py tests/test_a_runner_reached_unit_reads_pytest_only.py tests/test_a_new_returnable_value_is_a_contract_change.py -q` | `46 passed, 2 warnings in 39.11s`, exit 0 |
| `.venv/bin/python -m pytest tests/test_the_fixes_close_the_record.py tests/test_the_record_is_generated.py tests/test_the_fixes_name_their_surface.py tests/test_the_rules_have_one_owner.py tests/test_review_axes.py -q` | `240 passed in 71.14s` |
| `.venv/bin/python -m pytest tests/test_docs_line_wrap.py tests/test_release_hygiene.py tests/test_no_real_identifiers.py tests/test_the_reopening_is_one.py -q` | `86 passed, 1 skipped in 9.38s` |
| Corpus probe — 131 committed `round-*.md` through `table_body` under both id rules | `parsed 130 · both 82 · old-only 2 · new-only 0 · neither 46`; the two old-only cells are `r3 🟡 2` (old key 3, last run 2) and `🟢 round 2's finding (🟡 4)` (old key 2, last run 4) |
| Class probe — old and new `call_sites` over every top-level def under `tests/` at `ba22b28` | `test 1947/1892→0 · fixture 42/8→0 · other 483/1→1 · class 2/0→0`; the survivor is `tests/test_the_reopening_is_one.py#floor_record` |
| Boundary probe — five built repositories through `call_sites` at `ffd1d05` | `tests/helpers.py#test_thing → ['pytest only']` · root `conftest.py` fixture → `['no call site found']` · root `conftest.py` hook → `['no call site found']` · `tests/test_real.py#test_real → ['pytest only']` · helper passed as a value → `['no call site found']` |
| The same five repositories with findings 1 and 2 applied | `['no call site found']` · `['pytest only']` · `['pytest only']` · `['pytest only']` · `['no call site found']` — all five correct |
| The six modules with findings 1, 2 and 3 applied | `236 passed, 2 warnings in 94.50s` — no existing case moves |
| Widening probe — `return_literals` given the `ast.dump` of every enclosing `if` test, then `pytest -k hole_is_a_hole` | `1 failed` — `AssertionError: the check caught it, so the documented hole is now false`. The guard is real |
| Equivalence probe — `n.value is not None` dropped, then the #194 module | `8 passed`; and directly: for a bare `return`, `n.value` is `None`, `isinstance(None, ast.Tuple)` and `isinstance(None, ast.Constant)` are both False, `ast.iter_child_nodes` yields `[]` |
| Historical probe — `top_units` over `chain_check.py` at `v0.8.0` and `v0.8.3` | `read_record`: signature equal, arities `{1}` equal, literals `frozenset()` → `frozenset({('NoneType', 'None')})`; old contract equal, new contract different |
| Noise probe — old and new contract over three real ranges | `86e140f..ffd1d05` 0→0 · `v0.8.0..v0.8.3` 5→6 (`chain_check.py#read_record`) · `v0.8.3..v0.9.0` 1→1 |
| ReDoS probe — `FINDING_ID_RE` against `"!" * n + "x"` | `n=22 0.177s · n=24 0.705s · n=26 2.928s · n=28 11.432s`; the proposed pattern: `0.000006 s` at each, `0.000139 s` at n=4000, and no disagreement over 16 id shapes |
| `bin/evidence-check` | `776 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0 |
| `bin/deferral-check` | resolves; exit 0 |
| `git status --porcelain` after every probe edit was reverted | empty |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `tests/test_the_reopening_is_one.py#floor_record` reads `no call site found` for a second cause this branch does not repair | `seal/follow-up.md` — already deferred by the branch; finding 5 is about the row's shape and section, not about reopening the decision | the repository owner |
| Whether `Contract changes` needs the narrowing to non-string literals once 0.9.1's records land | `questions.md` Q3 — already deferred; this round's measurement (1 added entry across three real ranges) is the first evidence and does not answer it | the repository owner |
| Whether the two committed records that miscount their ids are corrected in place | `overview.md` §*Not verified* — already deferred; this round confirms nothing is blocked | the repository owner |
| The full suite, the repository-wide lint and the typecheck | contract §2 — the broad gate is one run after the rounds settle | the orchestrator |
