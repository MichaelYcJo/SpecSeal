# Round 1 report — a round record disarms survivor-check

| Field | Value |
|---|---|
| Work item | `1789211172-a-round-record-disarms-survivor-check` |
| Issue · PR | #365 · #372 (draft) |
| Branch | `fix/365-a-round-record-disarms-survivor-check` |
| Target SHA | `dc1e93a` |
| Base | `release/v0.11.2` at `bc5248c` |
| Round | 1 — no earlier round, nothing inherited |

HEAD was still `dc1e93a` and the working tree clean when this report was
finished.

Reviewed in a `git clone --no-local` of the repository checked out at the
target SHA, inside this session's scratchpad. The clone is deleted; nothing
was written in the working checkout except this file.

## The verdict in one paragraph

**The fix is right and it is minimal.** One filter, on the whole path list,
placed before the blobs are read, with the pool side untouched. I reproduced
phase 1's failing run against the unedited module and the output matches the
record verbatim, so the two cases are not counterfeit seals. The real defect I
found is one level up: **the case that pins the enumeration counts functions,
not call sites**, so two of the three shapes `plan.md` names as the six-month
failure scenario pass it. Everything else is paperwork.

## Findings

### 🟡 1 · the enumeration case measures functions, so a second unfiltered path list inside an existing one passes

`tests/test_a_corrected_sentence_survives_elsewhere.py:615`
(`_derives_a_path_list`) and `:676` (the set-equality assertion).

`_derives_a_path_list` returns a set of function NAMES, and the only assertion
over it is `set(derivers) == declared`. A fourth path-listing call turns the
case red exactly when it lands in a function nothing has declared yet. When it
lands inside a function that is already declared, the set does not move and
`_mentions(tree, "corrected", PREDICATE)` is still true because the first call
still applies the filter — so the case stays green.

**Executed**, four mutations of the module in the clone, restored
byte-identical after each:

| Mutation | Case |
|---|---|
| the filter removed from `corrected` | **red** — as `phases/phase-3.md:57` records |
| a fourth unfiltered path-list function added | **red** — naming `['corrected', 'tracked', 'whole_range']`, as recorded |
| a **second, unfiltered** `git diff --name-only -z` added *inside* `corrected` | **green** |
| a path list at **module scope** (`CACHED = git(".", "ls-files", "-z")`) | **green** |

Why it matters rather than being a quibble. `plan.md:46-50` names the scenario
this case exists against: *somebody adds a fourth place that derives a path
list from git — a `--since` flag, a second range, a cache of changed files*.
The case's own comment at `:588-596` repeats those three words for words. A
second range inside `corrected` and a cache built at import are two of the
three, and neither turns it red. `spec.md` §*The class, enumerated by
construction* heads its column **Call site**; the case's unit is the function.

The ledger fragment's S2 row is honest about this — it claims *every
**function** in the module* — so the claim and the code agree. What disagrees
is the class the spec and the plan enumerate.

Paste-ready fix below. I ran it: the module stays at 47 passed at `dc1e93a`,
and all four mutations above go red, the third with
`{'corrected': 2} != {'corrected': 1}`.

### 🟡 2 · the pull request body says the enumeration case was seen red four ways; the record says two

PR #372 body, §*The class, enumerated by construction*, final paragraph: *A
case pins the enumeration … It was seen red four ways, including one that
reports `['corrected', 'tracked', 'whole_range']`.*

`phases/phase-3.md:57` records that case seen red **two** ways, and its table
has two rows. Four is the total across two different cases — the docstring
case's two mutations in `phases/phase-2.md` and the enumeration case's two.
The sentence attributes all four to the enumeration case.

**Executed**: M1 and M2 above are the only two mutations that turn
`test_every_path_list_this_module_derives_from_git_is_filtered_or_named` red;
M3 and M4 do not.

This matters because acceptance row A5 is answered in that body and nowhere
else, and `CONTRIBUTING.md` §*What a change to a gate must carry*'s first
bullet is the red evidence. An evidence count that overstates by a factor of
two, in the document that is the only answer to the row, is the direction the
bullet exists to refuse.

### ⬜ 3 · the memo's executed line does not disclose the one repository-wide lint run

`seal/specs/1789211172-a-round-record-disarms-survivor-check/overview.md:10`.

The `verified: **executed**` line ends *`uvx ruff check` and `uvx ruff format
--check` on the changed files*. The smith disclosed to the orchestrator that
it also ran the lint repository-wide once, which `agent-contract` §2 reserves
for the one broad act, and that edits followed it. That disclosure is in no
record. The memo is the durable handover, and §3 asks for the instruction and
the rule in it.

The cost here is nothing: the broad gate is unrun and unclaimed, the memo's
`## Not verified` table still names the repository-wide lint as the sealer's,
so the spent run was not banked as a pass. What is missing is the sentence.

### ⬜ 4 · phase 5's removal table names one changed clause in the follow-up row and the edit changed two

`seal/follow-up.md:62`, and the *What this phase removes* table of
`phases/phase-5.md`.

Word-diffed against `bc5248c`. The edit made two changes, not one:

- *the way `rounds/` is left out **of the corpus** by construction* → *left
  out by construction*. This is the stale clause the phase was asked to
  correct, and the removal table names it.
- *leave `seal/specs/*/survivors.md` out of **the ADDED side of** `corrected`*
  → *out of **`corrected`'s path list***. This widens the candidate fix the
  row proposes, and the removal table does not name it.

The widening is grounded — `questions.md` Q1's *in* option argues for the
whole list, and #361's round 3 measured the corpus half — but the row's own
executed measurement (eleven places to one over `7355201..a18754c`) is a
measurement of the added side. A row that proposes more than its own evidence
covers, with the change unrecorded, is the shape `evidence-check` exists
against.

### ⬜ 5 · two AST helpers accept only `FunctionDef` while two accept `AsyncFunctionDef` as well

`tests/test_a_corrected_sentence_survives_elsewhere.py:634` (`_mentions`) and
`:717` (`_function`).

`_derives_a_path_list` and `_callers_of` both match
`(ast.FunctionDef, ast.AsyncFunctionDef)`. `_mentions` and `_function` match
`ast.FunctionDef` alone. So an `async def` that derives a path list is found by
the first pair and then raises `f"{function} is no longer a function in this
module"` from the second — red in the safe direction, with a message that says
the function was deleted when it was made async. **Read**, not executed.

### ⬜ 6 · one half of the `foreign` grounds assertion cannot fail on the module

`tests/test_a_corrected_sentence_survives_elsewhere.py:709`:
`assert "foreign" in grounds and "foreign" in body`.

`grounds` is the string constant declared at `:598-607` in this same file and
it contains the word literally, so the left conjunct is a tautology over test
data. The real assertion is the right one, which I confirmed: `whole_range`'s
body holds `foreign` five times. If somebody reworded the grounds and dropped
the word, the failure message would say *that mechanism is not in the function
any more* — blaming the module for an edit to the test.

### ⬜ 7 · the docstring case's message conflates two different "both"s

`tests/test_a_corrected_sentence_survives_elsewhere.py:574`. The assertion is
`"both sides" in flat`, and the docstring's *both sides* means the two sides
of the range's path list (before and after). The message reads *names the pool
and the range without saying the exclusion holds on both*, which is a
different pair. The assertion is right; the sentence a reader meets when it
fires points at the wrong pair.

## What I checked and found sound

- **The fix itself.** `corrected` filters before `read_blobs`, so the narrowing
  is cheaper as well as correct, and the pool path is byte-identical.
  `corrected` has one caller (`:691`) and `whole_range` one (`:1026`); neither
  needs the unfiltered list.
- **Phase 1's quoted red output is real.** Reproduced at `392da83` with the
  module unedited: two failures, opposite directions, exit 0 and exit 1, text
  matching `phases/phase-1.md` apart from the probe repository's own SHAs.
  `agent-contract` §15 satisfied.
- **`whole_range`'s exception is argued, not asserted.** Read the function:
  `changed` feeds only `any(path.startswith(owner + "/") …)`. A fix-pass range
  whose only files under the work item directory are round records would, with
  the filter applied, produce an empty `changed` for that directory and push a
  legitimate declaration into `foreign`. The argument holds on the code.
- **The predicate's shape has no false positives in this tree.** All 324 paths
  at `dc1e93a` matching `rounds` inside `specs` sit under `seal/specs/`.
- **A6.** The changelog fragment, the memo's `## Not verified` row and the
  corrected follow-up row all say the exemption path is still open and name
  #371. None of them claims re-arming.
- **The records resolve.** `bin/evidence-check .` exit 0 — 1149 ok, 0 drifted,
  0 broken, the new fragment 6 ok, `0 refused`. `bin/unverified-check` on the
  memo exit 0, 5 open rows each with an answerer.
- **The seven record-guard modules phase 5 names are green**, and so is
  `tests/test_a_rider_reaches_its_file.py`, which guards `seal/follow-up.md`
  rows and which phase 5 did not name.
- **A5's other three bullets** are answered in the body: direction (stricter,
  with the cheap-mistake argument), prompt budget (zero), platform honesty
  (no Windows run claimed).

## Regression cases to plant

One, and it is finding 1's fix rather than a separate case: the count
assertion goes into
`tests/test_a_corrected_sentence_survives_elsewhere.py`, in
`test_every_path_list_this_module_derives_from_git_is_filtered_or_named`.

## Facts for the evidence ledger

Row S2 of `seal/ledger/1789211172-a-round-record-disarms-survivor-check.md`
claims *every function in the module …*. If finding 1's fix lands, the unit
becomes the call site and the row's verified behavior gains the third and
fourth mutations. Re-read and re-verify it rather than re-pointing it — the
anchor names the same case.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The enumeration case measures function names, so a second unfiltered path list inside an already-declared function, or one at module scope, passes it | `tests/test_a_corrected_sentence_survives_elsewhere.py:615`, `:676` | open | Executed: four module mutations in the clone, restored byte-identical. Two red as recorded, two green. `plan.md:46-50` names *a second range* and *a cache of changed files* as the scenario; neither is caught |
| 2 | 🟡 The pull request body attributes four red mutations to the enumeration case; `phases/phase-3.md:57` records two | PR #372 body, §*The class, enumerated by construction* | open | Executed: only M1 and M2 turn that case red. A5 is answered in the body alone, and the red evidence is `CONTRIBUTING.md`'s first bullet |
| 3 | ⬜ The memo's executed line omits the one repository-wide `ruff` run the smith disclosed | `seal/specs/1789211172-…/overview.md:10` | open | Read. `agent-contract` §3 asks the overrun be named in the handover; the memo is the durable one. Nothing was banked as a pass, so the cost is the missing sentence |
| 4 | ⬜ Phase 5's removal table names one changed clause; the follow-up edit changed two | `seal/follow-up.md:62`, `phases/phase-5.md` removal table | open | Executed word-diff against `bc5248c`: the candidate fix moved from *the ADDED side of `corrected`* to *`corrected`'s path list*, unrecorded |
| 5 | ⬜ `_mentions` and `_function` accept only `FunctionDef` while `_derives_a_path_list` and `_callers_of` also accept `AsyncFunctionDef` | `tests/test_a_corrected_sentence_survives_elsewhere.py:634`, `:717` | open | Read. An async path-list function would fail with *is no longer a function in this module* |
| 6 | ⬜ `"foreign" in grounds` is a tautology over a constant in the same file, and its failure message blames the module | `tests/test_a_corrected_sentence_survives_elsewhere.py:709` | open | Read; `whole_range`'s body holds `foreign` five times, executed via AST |
| 7 | ⬜ The docstring case's message names the pool-and-range pair where the assertion pins the two sides of the path list | `tests/test_a_corrected_sentence_survives_elsewhere.py:574` | open | Read |
| — | The fix on `corrected` | `skills/code-review/scripts/survivor_check.py:525` | answered | Correct, minimal, filtered before the blobs are read; both callers checked; phase 1's red reproduced verbatim at `392da83` |
| — | `whole_range` left unfiltered | `skills/code-review/scripts/survivor_check.py:833` | answered | The argument holds on the code: `changed` feeds only the ownership test, and a paperwork-only range under the work item directory would become `foreign` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -k "round_record_the_range"` at `392da83`, module unedited | 2 failed, 43 deselected — exit 0 and exit 1, matching `phases/phase-1.md` verbatim apart from the probe repository's SHAs |
| Same module, whole, at `dc1e93a` | 47 passed |
| `bin/test tests/test_a_rider_reaches_its_file.py` with the above at `dc1e93a` | 76 passed |
| Mutation: the filter removed from `corrected` | 3 failed — the enumeration case red with the message `phases/phase-3.md` quotes |
| Mutation: a fourth unfiltered path-list function `since` | 1 failed — names `['corrected', 'since', 'tracked', 'whole_range']` against `['corrected', 'tracked', 'whole_range']`, so the walk measures rather than restates |
| Mutation: a **second** unfiltered `git diff --name-only -z` inside `corrected` | **1 passed** — the gap in finding 1 |
| Mutation: a path list at **module scope** | **1 passed** — the same gap |
| Finding 1's paste-ready fix applied, then all four mutations re-run | 47 passed at `dc1e93a`; all four mutations red, the third with `{'corrected': 2} != {'corrected': 1}` |
| `bin/evidence-check .` at `dc1e93a` | exit 0 · 1149 ok · 0 drifted · 0 broken; fragment 6 ok; records arm `0 refused` |
| `bin/unverified-check` on the memo | exit 0 · 5 open · 0 closed, each with an answerer |
| The seven record-guard modules `plan.md` phase 5 names | 205 passed |
| Every tracked path at `dc1e93a` matching the predicate's shape | 324, all under `seal/specs/` — no false positive in this tree |
| The broad gate — the full suite, the repository-wide lint, the format check | **not yet.** Unrun and unclaimed at `dc1e93a`; the memo's `## Not verified` assigns it to the sealer, and `agent-contract` §2 keeps it out of this round |

The module was restored byte-identical after every mutation, and the clone was
deleted. No probe file was left in either tree.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The exemption path — a `survivors.md` row still silences its own survivor through the diff | Already deferred by this work item: Q1 answered *out*, `plan.md` phase 4 closes `deferred #371`, `seal/follow-up.md:62` carries the row | the repository owner, on #371 |
| Whether any branch in flight now reports a survivor it did not report before | Already deferred: `overview.md` `## Not verified` | the first pull request into a release branch after this merges |
| Windows | Already deferred: `overview.md` `## Not verified` | CI, or whoever next runs the check on Windows |

## Paste-ready fixes

**Finding 1** — replace `_derives_a_path_list` entirely. Verified: green at
`dc1e93a` at 47 passed, red on all four mutations.

```python
# How many path-listing calls each scope is allowed. The unit of the class is
# the CALL SITE, not the function that holds one.
PATH_LIST_CALLS = {"corrected": 1, "tracked": 1, "whole_range": 1}


def _derives_a_path_list(tree):
    """`{scope: how many path-listing calls it makes}`.

    The unit of the class is the CALL SITE, not the function that holds one,
    and module scope is a scope. A second unfiltered list inside a function
    that already filters one -- `plan.md`'s own *a second range*, *a cache of
    changed files* -- is this defect one line over rather than one function
    over, and a set of function NAMES cannot see it."""
    scope = {}

    def visit(node, name):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit(child, child.name)
                continue
            if isinstance(child, ast.Call):
                words = {
                    const.value
                    for const in ast.walk(child)
                    if isinstance(const, ast.Constant)
                    and isinstance(const.value, str)
                }
                if words & LISTS_PATHS:
                    scope[name] = scope.get(name, 0) + 1
                    continue
            visit(child, name)

    visit(tree, "<module>")
    return scope
```

and add the count assertion immediately after the existing set-equality
assertion in
`test_every_path_list_this_module_derives_from_git_is_filtered_or_named`:

```python
    assert derivers == PATH_LIST_CALLS, (
        f"the module derives path lists at {derivers} and this case accounts "
        f"for {PATH_LIST_CALLS}. A second list inside a scope that already "
        "holds one is classified nowhere -- the grounds above are about the "
        "call this case counted, not about the one just added"
    )
```

**Finding 2** — the sentence in PR #372's body:

```
A case pins the enumeration, so a fourth call site added later cannot silently
miss the predicate. It was seen red two ways, one of them reporting
`['corrected', 'tracked', 'whole_range']` — the proof that it walks the module
rather than restating a list. The docstring sentence is pinned by a second
case, seen red two ways of its own.
```

**Finding 3** — the tail of `overview.md`'s `verified: **executed**` line:

```
`uvx ruff check` and `uvx ruff format --check` on the changed files. The lint
was also run once repository-wide, which `agent-contract` §2 reserves for the
one broad act and §3 asks be named here: it passed, edits followed it, so the
run is spent rather than banked and the broad gate below is still the
sealer's.
```

**Finding 4** — add a second row to `phases/phase-5.md`'s *What this phase
removes* table:

```
| `seal/follow-up.md`'s clause *out of the ADDED side of `corrected`* — the candidate fix the row proposes | Widened in the same row to *out of `corrected`'s path list*, because Q1's *in* option and #361's round 3 both argue for the whole list. The row's own eleven-to-one measurement is of the added side, so the evidence for the wider half lives on #371 and not in this row |
```

**Finding 5** — both helpers:

```python
def _mentions(tree, function, name):
    """True when `function`'s body names `name` anywhere."""
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function
        ):
```

```python
def _function(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
```

**Finding 6** — drop the tautology and keep the message on the module:

```python
        body = ast.get_source_segment(source, _function(tree, name))
        assert "foreign" in grounds, (
            f"the grounds recorded here for leaving {name} unfiltered no "
            "longer rest on `foreign`, so this assertion is checking the "
            "module against an argument that has been rewritten"
        )
        assert "foreign" in body, (
            f"the grounds for leaving {name} unfiltered rest on `foreign` -- "
            "a declaration refused and PRINTED rather than silently dropped. "
            "That mechanism is not in the function any more, so the grounds "
            "are an argument about code that is gone"
        )
```

**Finding 7** — the message only:

```python
    assert "both sides" in flat, (
        "the paragraph names the pool and the range without saying the "
        "exclusion holds on both SIDES of the range's path list, which "
        "leaves the added-side-only reading that was already true and "
        f"already wrong:\n{flat}"
    )
```

Needs a fix: yes — finding 1, the enumeration case's unit is the function
rather than the call site, so two of the three shapes the plan names as its
own failure scenario pass it; and finding 2, the pull request body's red count.

Loses a record or crashes: no

## Proof block

Opened and read in full: `skills/code-review/scripts/survivor_check.py`
(`tracked`, `records_a_past_round`, `corpus`, `corrected`, `whole_range`, the
docstring section and the `rows` caller),
`tests/test_a_corrected_sentence_survives_elsewhere.py` (the added block and
its helpers), `seal/follow-up.md`, `seal/ledger.md` row S3,
`seal/ledger/1789211172-a-round-record-disarms-survivor-check.md`,
`CONTRIBUTING.md` §*What a change to a gate must carry*,
`.github/workflows/hygiene.yml:225-244`, `bin/test`, `bin/broad-gate`, and
every file under
`seal/specs/1789211172-a-round-record-disarms-survivor-check/` —
`spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`,
`changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`,
`phases/phase-5.md`. Read through the GitHub CLI: issue #365, pull request
#372's body.
