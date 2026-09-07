# Round 1 — the derivation misreads and the record refuses the id

| Field | Value |
|---|---|
| Work item | `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` |
| Branch | `fix/211-194-227-the-derivation-misreads-and-the-record-refuses-the-id` |
| Target SHA | `ffd1d05` |
| Base | `86e140f` |
| Worktree | `/Users/x/orca/workspaces/SpecSeal/main-worktrees/wi-211` |
| Runner | `.venv/bin/python -m pytest` (`bin/test` builds the same environment; the `.venv` was already present) |

## What this round was asked

Attack the six claims the hand-back rests on rather than read them: #227's
corpus measurement, #211's class enumeration and the boundary it draws,
#211's stated hook limit, #194's stated hole and the case that guards it,
#194's historical cross-check, and the one mutation recorded as equivalent.
Then the five re-verified ledger rows, the noise the wider `Contract changes`
row adds, and whether the two committed records that stop the strict parse
block anything.

Every one of the six was re-derived here rather than taken from the account.
**All six reproduce exactly.** What this round opens is elsewhere: two places
where the shipped code draws a line one step short of where its own prose
puts it, one place where the refusal that names the format hangs instead of
naming it, and two records that claim more than what was built.

## The shape of it

The branch chose a boundary and argued for it well. `plan.md`'s alternatives
table rejects *anything under `tests/`* on the grounds that it would say *the
runner covers this* about a unit nothing covers, and `docs/review-chain-spec.md`
§*The fix surface* repeats that as the rule that keeps the row honest. Findings
1 and 2 are the same defect in two directions: the shipped predicate says
`pytest only` about a unit pytest never collects, and says `no call site found`
about one pytest does reach. Finding 3 is the parser one file over. Findings 4
and 5 are records.

---

## 1 · 🟡 `pytest only` is now said about a unit pytest never collects

`skills/code-review/scripts/round_record.py:1868`

```python
        if name.startswith(TEST_PREFIX):
            return True
```

The arm asks only for the def's own name and the directory the file sits in.
Pytest's collection is two rules, and this is one of them: `python_files =
test_*.py *_test.py` decides which FILE becomes a test module, and
`python_functions = test_*` decides which def inside it is a case. A `test_*`
def in `tests/helpers.py` satisfies the second and not the first, so pytest
never runs it.

**Executed.** A repository built in a temporary directory, holding
`tests/helpers.py` with one uncalled `def test_thing()` beside a real
`tests/test_real.py`, gives `call_sites` → `['pytest only']`.

Why it matters is the branch's own sentence. `plan.md` §*Alternatives
considered* rejects the wider rule because *the row would then say the runner
covers this about a unit nothing covers*, and `docs/review-chain-spec.md:757`
carries the same reasoning. That is exactly what this arm now does for one
shape. It is the sentence #211 opened for, pointing the other way — which is
the thing the phase record says the boundary exists to prevent.

Nothing in this repository triggers it today: `tests/` holds only `test_*.py`
files and `conftest.py`, and my enumeration at `ba22b28` found no member. But
`round_record.py` ships to every install, and `tests/helpers.py` with a
`test_*` name inside it is an ordinary shape. There is also no case for it —
`test_a_test_shaped_def_outside_tests_is_not_collected` covers a def outside
`tests/`, and no case covers a def inside `tests/` in a file pytest does not
import.

## 2 · And a `conftest.py` outside `tests/` still reads `no call site found`

`skills/code-review/scripts/round_record.py:1858`

```python
    if not rel.endswith(".py") or not under_tests(rel):
        return False
```

`under_tests` gates the whole predicate, so the conftest arm reaches only a
`conftest.py` that sits under `tests/`. Pytest's own most common placement is
the repository root, where a `conftest.py` holds the fixtures and hooks that
every test module in the tree sees.

**Executed.** Two repositories built in temporary directories, one with a
root `conftest.py` holding `@pytest.fixture def sample()` requested by
parameter name, one with a root `conftest.py` holding `pytest_configure`:
both give `call_sites` → `['no call site found']`.

That is #211's own reported defect, unrepaired for the placement pytest
documents first. The gap is also not among the limits the branch wrote down:
`docs/review-chain-spec.md:765` records one limit — the hook arm reads
`conftest.py` alone, where pytest also dispatches hooks from collected test
modules — and says nothing about where that `conftest.py` may sit.

The two arms are separable from the `tests/` gate on the caller side, so this
does not force `under_tests` open for the `pytest`/`pytest only` collapse: a
`conftest.py` is a conftest wherever it sits, and that is the only widening
the fix needs.

## 3 · The refusal that names the format hangs on one shape it should refuse

`skills/code-review/scripts/round_record.py:1514`

```python
FINDING_ID_RE = re.compile(r"^(?:[^\w\s]+\s*)*(\d+)$")
```

`[^\w\s]+` inside a `*` group means a run of punctuation can be split into
groups in exponentially many ways, and on a cell that ends in a non-digit the
engine tries all of them before failing.

**Executed**, against the shipped pattern:

| punctuation characters before a non-digit | time to refuse |
|---|---|
| 22 | 0.177 s |
| 24 | 0.705 s |
| 26 | 2.928 s |
| 28 | 11.432 s |

Each further character doubles it, so a 40-character cell is hours. What a
person sees is `close` or `new` producing nothing and never returning — the
one failure mode worse than the confusing message #227 opened for, on the
tool that gates every record.

The repair is one character, and it accepts and keys exactly the same set:
`(?:[^\w\s]\s*)*` matches the same language because each repetition already
takes one punctuation character. Checked over 16 shapes including every one
the new cases and the corpus carry — no disagreement — and it refuses a
4000-character run in 0.00014 s.

## 4 · ⬜ The cross-check called independent is a transcription of the code it checks

`tests/test_a_new_returnable_value_is_a_contract_change.py:52` against
`skills/code-review/scripts/round_record.py:1715`

`literals_of` in the test file is the shipped `return_literals` loop
character for character, apart from the order of one assignment and a
`list()` around `n.value.elts`. Same explicit stack, same `stack.pop()`, same
boundary tuple, same `ast.iter_child_nodes` descent.

Two copies of one algorithm agree by construction, so
`test_the_derivation_agrees_with_an_independent_one_over_the_whole_tree` can
only catch a later edit to one copy. It cannot catch a blind spot, which is
what the records claim it does:

- `seal/ledger/1788817290-…md`, R3 — *Cross-checked against an INDEPENDENT
  implementation of the same rule.*
- `phases/phase-3.md` — *The independent cross-check is a second
  implementation, not a list of examples.*

Why it matters: the ledger is where a later session goes to find out what was
actually verified, and this repository has a measured instance of a false
strength claim reaching three files before one command falsified it
(`seal/ledger.md` R6, the `.github/` concealment claim). The claim here
should say what it is — a second copy that pins the shipped derivation
against drift.

The genuinely independent half is the 21 constructed pairs, whose expected
boolean column is a hand-written statement of intent rather than a reading of
the code, and it covers the nested-scope boundaries and the bare `return`.
That is what should carry the weight the wording gives the whole-tree case.

## 5 · ⬜ The #211 deferral landed as a bullet under a table for a different kind of item

`seal/follow-up.md:44`

The `floor_record` item was written as a bullet, under the heading *Riders
waiting on a file another branch holds*, whose table (`| Target | Who must
answer |`) is left with a header, a separator and no rows. Three things do
not line up:

- **The section is the wrong one.** No other branch holds
  `tests/test_the_reopening_is_one.py`; nothing is waiting on anything.
- **The shape is not the section's.** Both sections in this file are tables,
  and `overview.md` §*Not verified* says the answerer is *whoever opens the
  follow-up row*. There is no row.
- **The file's own rule sends it elsewhere.** `seal/follow-up.md:15` reads
  *Anything tied to a coordinate is a `# RIDER:` comment at the line it is
  about*, and this item names
  `tests/test_the_reopening_is_one.py:164`.

The answerer is named in the prose, so nothing is lost to nobody. What is
lost is that `grep -rn "RIDER:"` — the repository-wide list the file says
needs no keeping in sync — does not reach it.

---

## What reproduced, claim by claim

Every one of these was re-derived in this worktree. None was taken from the
prompt, the phase records or the changelog.

**#227's corpus.** 131 records on disk, 130 parse through the module's own
`table_body` path, 82 pass under both rules, 46 already refuse today, 2 pass
today only by miscounting, 0 pass under the new rule that the old one
refused, and the 82 key identically under both. The two are exactly the ones
named: `1788420761-…/rounds/round-4.md`'s `r3 🟡 2` keys as 3 where the last
run is 2, and `1788433011-…/rounds/round-3.md`'s `🟢 round 2's finding (🟡 4)`
keys as 2 where the last run is 4. **The new rule takes only wrong answers.**

**#211's class.** `call_sites` run over every top-level def under `tests/` at
`ba22b28`, old module and new, side by side:

| Kind | Total | `no call site found` OLD | NEW |
|---|---|---|---|
| `test_*` function | 1947 | 1892 | 0 |
| fixture | 42 | 8 | 0 |
| other helper | 483 | 1 | 1 |
| class | 2 | 0 | 0 |

The ticket's own proposal — `test_*` only — would indeed have left the 8
fixtures behind. The one survivor is `tests/test_the_reopening_is_one.py#floor_record`,
which is the boundary the prose claims, so the predicate draws the line where
the prose puts it **for every unit this repository holds**. Findings 1 and 2
are about units it does not hold and other installs will.

**#194's historical instance.** `chain_check.py#read_record` across
`v0.8.0..v0.8.3`: signature identical, arities `{1}` at both ends, literals
`frozenset()` → `frozenset({('NoneType', 'None')})`. The two-element contract
reads it unchanged; the three-element one reports it. It is the only unit the
literal half adds over that whole range.

**#194's hole, and that the case really guards it.** I widened
`return_literals` to key on the `ast.dump` of every enclosing `if` test —
which is what *reaching the input→value mapping* means — and
`test_the_hole_is_a_hole_and_not_a_claim` went red on the assertion that says
so. The guard is real, not merely green today.

**The surviving mutation is equivalent.** Dropped `n.value is not None` and
the module stayed green at 8 passed. The reason checks out directly: for a
bare `return`, `n.value` is `None`, `isinstance(None, ast.Tuple)` is False,
`isinstance(None, ast.Constant)` is False, and `ast.iter_child_nodes` yields
nothing. The loop adds no literal either way.

**The five re-verified ledger rows.** `bin/evidence-check` reads 776 rows,
0 drifted, 0 broken. Each claim opened: `## Findings format` still carries
the ⬜ line, the 🟡 threshold and the paste-ready OS-boundary paragraphs, so
the two rows anchored there stand; both opt-in headings still name `seal/`;
`call_sites` still hands out exactly five reach values, which
`test_the_section_names_every_reach_value_the_generator_fixes` confirms by
deriving them from its source. **The re-verifications are honest.**

## The noise question

Widening `Contract changes` to returnable literals adds **one entry across
three real ranges**, and that one is the true positive #194 was opened for.

| Range | Entries, old rule | Entries, new rule | Added by literals |
|---|---|---|---|
| `86e140f..ffd1d05` (this branch) | 0 | 0 | 0 |
| `v0.8.0..v0.8.3` | 5 | 6 | 1 — `chain_check.py#read_record` |
| `v0.8.3..v0.9.0` | 1 | 1 | 0 |

So the row is usable now, and `questions.md` Q3's worry is not yet supported
by anything measurable. Two things sharpen the answer for the owner. A
returned list, dict or f-string carries no `ast.Constant` at the return, so
the shapes the plan expects to be noisy — *a fix that swaps a returned
message string* — only enter the row when the message is a bare literal. And
this branch is its own illustration: `call_sites` changed behaviour and does
not enter the row, because every one of its returns is a list.

## The two committed records that stop the strict parse

**They block nothing.** `verdict_rows` has exactly one caller, `close`, which
reads the record named by `--round` and no other; `fix_table` likewise reads
the file `--fixes` names. Nothing walks earlier records through either.
`chain_check.py` — the arm CI and `--worktree` run over the whole tree — does
not read the `#` column with this rule at all. The two records would refuse
only if somebody re-ran `close` on them, and `close` runs on a record `new`
has just written.

Who answers whether they are corrected in place: the repository owner, as
`overview.md` §*Not verified* already says.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `tests/test_the_reopening_is_one.py#floor_record` reads `no call site found` for a second cause this branch does not repair | `seal/follow-up.md` — already deferred by the branch; finding 5 is about the row's shape and section, not about reopening the decision | the repository owner |
| Whether `Contract changes` needs the narrowing to non-string literals once 0.9.1's records land | `questions.md` Q3 — already deferred; this round's measurement (1 added entry across three real ranges) is the first evidence and does not answer it | the repository owner |
| Whether the two committed records that miscount their ids are corrected in place | `overview.md` §*Not verified* — already deferred; this round confirms nothing is blocked | the repository owner |
| The full suite, the repository-wide lint and the typecheck | contract §2 — the broad gate is one run after the rounds settle | the orchestrator |

## Paste-ready fixes

Finding 1 — `skills/code-review/scripts/round_record.py`. Add the constant
beside the three it joins, add the helper below `runner_reached`, and gate
the `test_*` arm on it.

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

Finding 2 — the same file. The whole of `runner_reached`'s gate and arms,
carrying finding 1's change as well, since the two touch adjacent lines. `base`
is computed once and both arms read it.

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

Both fixes need cases, and both need to be seen red first (contract §15). The
two that are missing from
`tests/test_a_runner_reached_unit_reads_pytest_only.py`:

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

`docs/review-chain-spec.md` §*The fix surface* needs its table row and its
limits paragraph to match. The row at line 755 and the sentence around it:

```markdown
| The unit | How pytest reaches it |
|---|---|
| a `test_*` def in a module `python_files` collects | collected by name pattern, file and function both |
| a fixture under `tests/` or in a `conftest.py` | injected by parameter name, so `name(` never occurs |
| a `pytest_*` def in a `conftest.py` | dispatched by the plugin manager |
```

Finding 3 — `skills/code-review/scripts/round_record.py:1514`. One character,
and the comment gains the sentence that says why it is one.

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

And the case, in `tests/test_a_finding_id_is_a_bare_integer.py`, which goes
red against the shipped pattern by timing out rather than by asserting:

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

Finding 4 — the two records. Say what the whole-tree case is, and let the 21
pairs carry the weight the wording gave it.

`seal/ledger/1788817290-…md`, R3's *Verified behavior* cell, replacing
*Cross-checked against an INDEPENDENT implementation of the same rule twice*:

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

`phases/phase-3.md`, replacing *The independent cross-check is a second
implementation, not a list of examples*:

```markdown
**The cross-check is two halves, and only one of them is independent.** The
whole-tree comparison runs a transcription of the shipped loop over every
top-level def in every tracked `.py` file; two copies of one algorithm agree
by construction, so what it catches is a later edit to one of them. The half
that could have caught a blind spot is the 21 constructed pairs, whose
expectation column is hand-written rather than derived, and which is where
the nested-scope boundaries and the bare `return` are pinned.
```

Finding 5 — `seal/follow-up.md`. The item is tied to a coordinate, so the
file's own rule puts it at that line. Delete the bullet at `:47-56`, leave
the *Riders waiting* table as it was, and write the rider at
`tests/test_the_reopening_is_one.py:164`, above the `def`:

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

If the item is kept in `seal/follow-up.md` instead, it belongs in
*Schedulable items with nowhere else to go* as a row, not under *Riders
waiting on a file another branch holds* as a bullet:

```markdown
| `no call site found` has a second cause, and #211 repaired only the first. `tests/test_the_reopening_is_one.py#floor_record` is passed by name as a value at five call sites and never called, so the `name(` the reach walk greps for occurs nowhere but its own `def` line — 1 of 483 helpers under `tests/`, enumerated at `ba22b28`. Reading a bare `name` in an argument position would reach it and would also name every mention of the word, so the repair is not the one #211 took. The decision is whether a reach walk should follow a callable passed as a value at all | the repository owner |
```

## Inherited coordinates

No `rounds/round-*.md` exists for this work item, so nothing was carried from
an earlier round. What was carried rather than re-derived:

| Carried | From | Why it was not re-derived |
|---|---|---|
| `seal/ledger.md` R8's and R2's coordinates for the reach vocabulary, and the `## Findings format` anchors | the ledger's own rows | `bin/evidence-check` passes at 776 ok, 0 drifted, so each anchor still names its content; the claims themselves were opened |
| `token_thirds` returning 0 for a mean it cannot compute, and the call site that reads the 0 as a baseline | `seal/specs/1788700685-…/rounds/round-3.md` and round 4, cited by `plan.md` | It is #194's motivating instance rather than a claim about this branch's code, and the branch's own derivation was checked against a different instance (`read_record`) that I re-derived |
| `is_a_record_of_a_moment`'s fix being an input→value remap | `seal/specs/1788735085-…/rounds/round-2.md` finding 11 | The case rebuilds both ends from source, and I checked the guard by widening the check rather than by trusting the citation |

## What I could not verify

| Item | Who answers it |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Contract §2 reserves the broad gate for one run after the rounds settle, and no spawn instruction asked for it. What ran here is the three new modules and eight neighbouring ones, 372 cases | the orchestrator |
| Whether `tests/test_the_records_can_be_carried_out_and_in.py`'s 4 failures are gone once `fix/111-…` merges | out of this round's scope by instruction; the orchestrator |
| Whether findings 1 and 2 have members in installs other than this repository. The class was enumerated here and holds none; the shapes were built rather than found | the repository owner, when the fix lands |

## For the record

| Field | Value |
|---|---|
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |

Both surface rows carry the *not yet written* form because this round
commissions fixes and none exist. Measured over the branch range
`86e140f..ffd1d05` for the orchestrator's information: 0 units changed
contract under either rule, and 70 top-level units added, of which the
generator's own are `finding_number (depth 1)`, `return_literals (depth 1)`,
`decorated_as (depth 1)`, `runner_reached (depth 1)`, `FINDING_ID_RE
(depth 1)`, `BARE_ID (depth 1)`, `RECORD_LABEL (depth 1)`, `FIX_TABLE_LABEL
(depth 1)`, `TEST_PREFIX (depth 1)`, `HOOK_PREFIX (depth 1)`, `CONFTEST
(depth 1)` and `FIXTURE (depth 1)`.

Needs a fix: yes — 1, 2, 3
Loses a record or crashes: no

Finding 3 stops `close` and `new` from returning, which is neither. No record
is lost — nothing has been written when the pattern starts backtracking — and
nothing raises; the operator interrupts a command that is still running.
Findings 1 and 2 write a wrong reach value into a record that is otherwise
complete.

## Proof — the files opened

`seal/specs/1788817290-…/spec.md` · `plan.md` · `questions.md` · `overview.md` ·
`routing.md` · `changelog.md` · `phases/phase-1.md` · `phases/phase-2.md` ·
`phases/phase-3.md` · `seal/ledger/1788817290-…md` · `seal/follow-up.md` ·
`seal/ledger.md` (the five changed rows) ·
`skills/code-review/scripts/round_record.py` ·
`skills/code-review/scripts/chain_check.py` (`EMPHASIS`, the id patterns) ·
`skills/verify/scripts/unverified_check.py` (`readable`) ·
`skills/code-review/SKILL.md` §*Findings format* ·
`docs/review-chain-spec.md` §*The finding id* and §*The fix surface* ·
`docs/review-handoff-protocol.md` (the added paragraph) ·
`templates/sdd-round.md` (the `#` comment) ·
`tests/test_a_finding_id_is_a_bare_integer.py` ·
`tests/test_a_runner_reached_unit_reads_pytest_only.py` ·
`tests/test_a_new_returnable_value_is_a_contract_change.py` ·
`tests/conftest.py` · `tests/test_the_record_is_generated.py` (the loaders) ·
`tests/test_the_reopening_is_one.py` (`floor_record`) · `bin/test`
