# 1789211172-a-round-record-disarms-survivor-check — review round 1

| Field | Value |
|---|---|
| Target SHA | dc1e93a |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #372 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 1, the enumeration case's unit is the function rather than the call site, so two of the three shapes the plan names as its own failure scenario pass it; and finding 2, the pull request body's red count. |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

# round 1 — the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `dc1e93a` — every measurement below was taken there, and HEAD had not moved when the round ended |
| Base | `release/v0.11.2` = `bc5248c`, identical to `main` |
| Draft pull request | #372, opened before this round |
| Ran by | specseal:warden on claude-opus-5 |
| Earlier rounds | none — this is round 1, so no verdict was inherited |

## Scope

Issue #365 — `survivor_check.py` filters a work item's round records out of
the pool it searches and not out of the range it measures, so a record quoting
a defective sentence counts as wording the fix wrote and the survivor it quotes
is subtracted. Eight commits, `18f99df` through `dc1e93a`: the routing
declaration, the frame, and the smith's six.

One filter line in `skills/code-review/scripts/survivor_check.py`, two docstring
passages, three cases and four AST helpers in
`tests/test_a_corrected_sentence_survives_elsewhere.py`, a new ledger fragment,
an `seal/ledger.md` S3 re-verify, one corrected clause in `seal/follow-up.md`,
and this work item's records.

## What the reviewer was asked to weigh

Spec compliance first, then quality, against the committed frame — `spec.md`'s
six acceptance rows A1–A6, `plan.md`'s five phases, and `CONTRIBUTING.md`
§*What a change to a gate must carry*, which the acceptance was written against.

Seven things by name:

1. **Phase 1's two cases, claimed seen red before the fix.** A case that has
   never failed is what this repository calls a counterfeit seal — check that
   the quoted output is what the unedited module actually produces.
2. **Whether A4's enumeration case measures or restates.** The claim is that it
   goes red when a fourth unfiltered path-list call is added, and that it names
   the functions the walk found rather than a hardcoded list.
3. **`whole_range()`'s deliberately unfiltered list** — judge the ownership
   argument, not just its presence.
4. **The real-range measurement** `7e17f5e..941dab5`, reproducible only while a
   local branch survives.
5. **Q1 answered `out`, #371 carrying the deferred half** — the records must not
   claim the exemption path is re-armed, which is acceptance row A6.
6. **The smith's two corrections to its own frame**, recorded rather than sent
   back.
7. **The smith's named overrun** — one repository-wide `ruff check .`.

## What was withheld

The broad gate. `agent-contract` §2 makes it one act and the sealer owns it,
after the rounds settle. The reviewer was told not to run the full suite, the
repository-wide lint or the format check, and its probe table records the cell
as `not yet`.

Pushing and committing, per `agent-contract` §6. The report was written to a
file for the orchestrating session to verify before any of it was posted.

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

## Paste-ready fixes

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
```python
    assert derivers == PATH_LIST_CALLS, (
        f"the module derives path lists at {derivers} and this case accounts "
        f"for {PATH_LIST_CALLS}. A second list inside a scope that already "
        "holds one is classified nowhere -- the grounds above are about the "
        "call this case counted, not about the one just added"
    )
```
```
A case pins the enumeration, so a fourth call site added later cannot silently
miss the predicate. It was seen red two ways, one of them reporting
`['corrected', 'tracked', 'whole_range']` — the proof that it walks the module
rather than restating a list. The docstring sentence is pinned by a second
case, seen red two ways of its own.
```
```
`uvx ruff check` and `uvx ruff format --check` on the changed files. The lint
was also run once repository-wide, which `agent-contract` §2 reserves for the
one broad act and §3 asks be named here: it passed, edits followed it, so the
run is spent rather than banked and the broad gate below is still the
sealer's.
```
```
| `seal/follow-up.md`'s clause *out of the ADDED side of `corrected`* — the candidate fix the row proposes | Widened in the same row to *out of `corrected`'s path list*, because Q1's *in* option and #361's round 3 both argue for the whole list. The row's own eleven-to-one measurement is of the added side, so the evidence for the wider half lives on #371 and not in this row |
```
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
```python
    assert "both sides" in flat, (
        "the paragraph names the pool and the range without saying the "
        "exclusion holds on both SIDES of the range's path list, which "
        "leaves the added-side-only reading that was already true and "
        f"already wrong:\n{flat}"
    )
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The exemption path — a `survivors.md` row still silences its own survivor through the diff | Already deferred by this work item: Q1 answered *out*, `plan.md` phase 4 closes `deferred #371`, `seal/follow-up.md:62` carries the row | the repository owner, on #371 |
| Whether any branch in flight now reports a survivor it did not report before | Already deferred: `overview.md` `## Not verified` | the first pull request into a release branch after this merges |
| Windows | Already deferred: `overview.md` `## Not verified` | CI, or whoever next runs the check on Windows |

## Verified by the orchestrating session, before the record was committed

A reviewer's report is a claim. The heaviest finding's coordinates were opened
and its measurement re-taken here, at `dc1e93a`, each mutation applied to the
working tree and the file restored with `git checkout --` afterwards.

| What was re-taken | Result |
|---|---|
| A second unfiltered path list added **inside `corrected` itself** | `test_every_path_list_this_module_derives_from_git_is_filtered_or_named` — **1 passed**. The case does not see it |
| A path list added at **module scope**, outside every function | **1 passed**. The walk only descends into `FunctionDef` nodes, so it is not found at all |
| `_derives_a_path_list` read at `tests/test_a_corrected_sentence_survives_elsewhere.py:620` | Keys the mapping by `node.name`, so two call sites in one function collapse to one entry |
| `phases/phase-3.md`'s mutation table | **Two** rows, not four. The pull request body's *seen red four ways* adds the docstring case's two to the enumeration case's two, and attributes all four to the enumeration case |

**Finding 1 is confirmed, and it is confirmed as a spec divergence rather than
as a missing test.** `spec.md`'s class table is headed `Call site` and gives
`corrected` and `whole_range` separate rows for what is the same spelling of
the same command; the case's unit is the function. The ledger fragment's S2 row
says *every function*, which is honest about the code and unaligned with the
frame the case was written to hold. Two of the three shapes `plan.md:46-50`
names as this change's own six-month failure scenario — a second range, a
changed-file cache — pass the case as written.

**Finding 2 is confirmed by reading the two documents against each other**, and
it is the orchestrating session's own error rather than the smith's: the
handover report gave four mutations across two cases and the pull request body
attributed them to one.

Nothing else in the report was contradicted. The module's own suite was re-run
here before the round was commissioned — 47 passed — and `ruff check` and
`ruff format --check` on the two changed Python files, which is the narrow run
a phase boundary owes and not the broad gate.
