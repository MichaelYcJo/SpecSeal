# 1788789985-round-record-dies-on-python-3-9 — review round 1

| Field | Value |
|---|---|
| Target SHA | 804f14b3a8ab34b0b01de6f03bc2a7856d1d9508 |
| Ran by | warden on claude-opus-5 |
| PR | 235 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | test_the_refusal_is_ascii_because_it_is_written_before_stderr_is_set_up (depth 1) |
| Needs a fix | yes — findings 1, 2 and 3; finding 4 is answerable with grounds |
| Loses a record or crashes | yes — `skills/verify/scripts/session_cost.py:89` exits 1 with a bare `AttributeError` traceback on python 3.9, and finding 1 is that the branch's enumeration and its regression test both place that file out of the class |

- [x] Pass

## What this round was asked

Round 1 of `1788789985-round-record-dies-on-python-3-9` (ticket #226, PR #235), at target `804f14b`, base `86e140f`. No prior rounds.

Judged against four acceptance criteria: the guard fires at entry, before work a reader could mistake for progress; nothing changes above the floor; a regression test seen red that does more than assert a constant exists; `strict=True` stays with grounds.

Five targets were named in order. The guard's placement was to be attacked rather than accepted — the branch's mutation re-run, and then the harder question it did not ask: what executes ABOVE the guard, enumerated by reading the module top to bottom. Exit code 2 was to be checked against every other exit in the module and every caller that reads it. The `FLOOR` pin was to be mutated to see whether it can actually fail, since the branch's whole argument for retyping the number rests on it. The class was to be re-derived by `py_compile` at 3.9.6 rather than by text, and the corrected scan pattern checked for the same shape of blind spot one construct over. And the four deferrals in `seal/follow-up.md` were to be judged for whether the answerer is real and whether they belong on the tracker instead.  <!-- NAME NOT IN TREE -->

`7 mutations, all killed` was named as an aggregate to re-run rather than accept, at least for the two that would hurt most. One orchestrator correction was handed over: the hand-back's exit code 2 had been re-run through a pipe, so it was to be read directly.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A sixth member of the class ships and the case written to stop a sixth cannot see it — `dt.UTC` behind an aliased import defeats `ABOVE_THE_FLOOR`, and `session_cost.py` dies with a bare traceback on 3.9 | `tests/test_a_script_says_which_interpreter_it_needs.py:410` | **fixed** `1e24566` | fixed at 1e24566 — ``; Executed: `session_cost.py` under 3.9.6 exits 1 with `AttributeError: module 'datetime' has no attribute 'UTC'` at `:89`, end to end on a zone-less transcript; the module's own 11 cases are green at the same time; an AST re-derivation returns six members where the branch's pattern returns five |
| 2 | The `seal/follow-up.md` deferral row is separated from its table by a blank line, so it is not a row of *Schedulable items with nowhere else to go* and its `Who must answer` value is not a column; its text also says four where finding 1 makes five | `seal/follow-up.md:41` | **fixed** `cedc58e` | fixed at cedc58e — ``; Read: line 41 is blank and lines 38-40 are the table; GFM ends a table at the first blank line. Nothing in the tree parses this file, so nothing catches it |
| 3 | `test_the_guard_precedes_every_other_module_level_act` asserts against one act, the `load(…)` assign, not against every module-level act as its name says | `tests/test_a_script_says_which_interpreter_it_needs.py:350` | **fixed** `ed7f577` | fixed at ed7f577 — ``; Executed: with `_EARLY = os.path.abspath(__file__)` inserted above `FLOOR`, the shipped module reports `11 passed`; the widened check reports `module level calls abspath() at line 150, above the guard at line 183` |
| 4 | The rewritten exit-code paragraph reads as exhaustive for pre-write failures, but `load`'s refusal at `:194` exits 1 and the same paragraph files 1 under *after the record is written* | `skills/code-review/scripts/round_record.py:99` | **fixed** `00bc9b0` | fixed at 00bc9b0 — ``; Executed: `raise SystemExit('boom')` exits 1. Read: no caller in the tree branches on this script's exit code, so the blast radius is the documented contract only. Pre-existing wording; answerable with grounds |
| 5 | `spec.md` cites `round_record.py:761-766` and `:767 :935 :1587 :1591`, which are the pre-guard line numbers — 72 lines short of where those sites now are | `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:27` | **fixed** `fb45bc1` | fixed at fb45bc1 — ``; Read against the file: the comment is at 833-838 and the four `zip` sites are at 839, 1007, 1659, 1663, confirmed from the AST |
| 6 | The ledger fragment's R3 states, under an **Executed** label, that five files carry a construct above the floor and four are deferred | `seal/ledger/1788789985-round-record-dies-on-python-3-9.md` | **fixed** `fb45bc1` | fixed at fb45bc1 — ``; Same executed enumeration as finding 1: six and five |
| 7 | `BELOW_FLOOR`'s `§` is written before `__main__` reconfigures stderr, so under an ASCII stderr the sentence ends `CONTRIBUTING.md \xa7Running the checks` | `skills/code-review/scripts/round_record.py:158` | **fixed** `00bc9b0` | fixed at 00bc9b0 — ``; Executed: `PYTHONIOENCODING=ascii /usr/bin/python3 …` prints the escape and still exits 2 |

## Paste-ready fixes

```python
# The constructs that put a shipped script above the floor today, spelled so
# that neither hides. Two blind spots have been found in this pattern, one per
# review: `zip\([^)]*strict=` hid round_record.py's third site, where an inner
# `verdict_words(reader, rows)` closes a parenthesis before the keyword is
# reached; and `datetime\.UTC` hid session_cost.py:89, which spells the module
# `import datetime as dt`. So the zip half counts parentheses instead of
# stopping at the first one, and the UTC half matches whatever the module was
# named. Both halves are text, which is the limit `seal/ledger/…` R3 states:
# an AST walk is what would close it, and this is the cheaper thing that
# catches the two constructs that exist.
ABOVE_THE_FLOOR = re.compile(
    r"zip\([^()]*(?:\([^()]*\)[^()]*)*strict=|\b\w+\.UTC\b", re.S
)
```
```python
    "hooks/root-migrate.py": "deferred, seal/follow-up.md (#226)",
    "skills/verify/scripts/session_cost.py": "deferred, seal/follow-up.md (#226)",
}
```
```python
    `skills/agent-contract/SKILL.md` §12: the finding named one coordinate and
    what was owed was every instance the same cause produces. Six files
    carried one, and five of them are somebody else's branch or somebody
    else's release. This is what keeps a seventh from arriving as a traceback
    on a stranger's mac.
```
```
| Bring `agents/smith.md` and `agents/scribe.md` under `tests/test_docs_line_wrap.py`, together. … | the repository owner |
| **Five more scripts die below the supported floor with a bare traceback, the way `round_record.py` did before #226.** Enumerated by construction in `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md` §*The class, enumerated by construction*, and re-enumerated on every suite run by `tests/test_a_script_says_which_interpreter_it_needs.py#test_no_shipped_script_needs_more_than_the_floor_without_saying_so`, so this row is a decision waiting rather than a fact that can go stale. `.github/scripts/gather_changelog.py:151` and `.github/scripts/fold_ledger.py:358` use `datetime.UTC` (3.11) and are named after a literal `python3 ` in `CONTRIBUTING.md:128-131` and `docs/release-checklist.md` §3 — so a release run on a 3.9 or 3.10 `python3` fails at the moment it writes the dated heading. `skills/verify/scripts/session_cost.py:89` is the same construct behind `import datetime as dt`, and it ends the run report `docs/review-handoff-protocol.md` §*After a run* points at. `skills/implement/scripts/seal.py:324,436` is the same construct and **was not touched because another work item in this release holds that file**. `hooks/root-migrate.py:425` uses `zip(..., strict=True)` and is reached through `hooks/hooks.json`'s session-start dispatch, so it fails while migrating a 0.3.x layout, in a hook, where nobody is reading. The fix is fifteen lines each, copied from `skills/code-review/scripts/round_record.py#below_floor`, which was written to be copied and says so. **What needs a person is not the fix, it is whether these belong in the tracker instead**: this file's own opening says a repository with a tracker should normally hold none of these, and the handoff for #226 asked for them here | the repository owner |

## Riders waiting on a file another branch holds
```
```python
    # And not `load(...)` alone. This case is named for EVERY other
    # module-level act, and a check that names one call cannot see the second
    # one somebody adds above the guard -- an `open`, a `subprocess.run`, a
    # constant read off the disk. So every module-level statement that calls
    # anything sits below the refusal, less the guard's own three constants
    # and the assignment that runs it.
    OWN = {"FLOOR", "FLOOR_TEXT", "BELOW_FLOOR", "_refusal"}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import)):
            continue
        if isinstance(node, ast.Assign) and all(
            getattr(t, "id", None) in OWN for t in node.targets
        ):
            continue
        for inner in ast.walk(node):
            if not isinstance(inner, ast.Call):
                continue
            called = getattr(inner.func, "id", None) or getattr(
                inner.func, "attr", None
            )
            assert node.lineno >= refusal, (
                f"module level calls {called}() at line {node.lineno}, above "
                f"the guard at line {refusal}; the guard has to precede every "
                "act, not only the sibling checker's load"
            )
```
```
Exit codes: 0 and 1 are `chain_check`'s own, after the record is written · 2
the input was unusable, or the interpreter is below the floor — either way
nothing was read and nothing was written · a sibling script that will not load
is `SystemExit` with a sentence, which is 1 before anything is read.
```
```python
    """Import a sibling script by path, or die — a missing checker is exit 1."""
```
```
- **The four `strict=True` sites stay exactly as they are.** The comment at
  `round_record.py:833-838` says what the first one states: both of the
```
```
| 1 | `skills/code-review/scripts/round_record.py` `:839 :1007 :1659 :1663` | `zip(..., strict=True)` → `TypeError: zip() takes no keyword arguments`, after the report has been read | 3.10 | the orchestrator's `python3` | **fixed here** |
```
```
Six files carry a runtime construct above the floor; one is fixed here and five are in `seal/follow-up.md`
```
```python
    "<this script> ...`, or see CONTRIBUTING.md section 'Running the checks'."
```

## Executed probes

| What was run | Result |
|---|---|
| `/usr/bin/python3 skills/code-review/scripts/round_record.py new --help`, exit code read directly with `; echo $?` and not through a pipe | exit **2**, the guard's three-line sentence on stderr, nothing on stdout — the orchestrator's correction confirmed |
| `/usr/bin/python3 -m py_compile skills/code-review/scripts/round_record.py` | exit 0 — the whole module parses on 3.9, so the guard is reachable |
| `/usr/bin/python3 -m py_compile` over all 111 tracked `.py` | one failure, `tests/test_the_root_migrates_itself.py` (f-string); no shipped script carries 3.10+ syntax — the branch's third construction reproduces |
| AST re-derivation of the class: every `alias.attr` in every shipped `.py` resolved to its stdlib module and asked of the 3.9 interpreter, plus every `zip(…)` call with any keyword at any depth | **six** members, not five — `skills/verify/scripts/session_cost.py:89` (`dt.UTC`) added to the branch's list; the four `zip` sites in `round_record.py` and the one in `root-migrate.py` reproduce exactly |
| `session_cost.py` under `/usr/bin/python3` (3.9.6), whole script, on a transcript with zone-less timestamps | exit 1, `AttributeError: module 'datetime' has no attribute 'UTC'` at `:89`; the same transcript under 3.12 exits 0 clean |
| Mutation, in a clone at the target: the guard block moved from module level into `main()`, then `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` | `1 failed, 10 passed` — only `test_the_guard_precedes_every_other_module_level_act`. The branch's claim reproduces exactly |
| Mutation: `FLOOR` in `.github/scripts/run_tests.py` raised to `(3, 13)`, guard's literal left at `(3, 12)` | `1 failed, 10 passed` — `test_the_floor_is_the_number_the_runner_and_the_linter_hold`, naming both numbers. The pin can fail |
| Mutation: `_EARLY = os.path.abspath(__file__)` inserted above `FLOOR` in `round_record.py`, shipped test module unchanged | **`11 passed`** — an act above the guard is invisible to the shipped AST case (finding 3) |
| The same mutation against the widened AST check from the paste-ready fix | red: `module level calls abspath() at line 150, above the guard at line 183` |
| `skills/verify/scripts/session_cost.py` added to `CLASSIFIED` with the shipped pattern unchanged | red: `['skills/verify/scripts/session_cost.py'] no longer carry the construct they were classified for` — the fix has to be the pattern and the row together |
| The widened pattern plus the `CLASSIFIED` row plus the widened AST check, all three, `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` | **`11 passed`**, exit 0 — every paste-ready fix below is green at the target |
| Candidate patterns compared over the shipped tree | shipped pattern: 5 files · the widened one: the same 5 plus `session_cost.py:89`, and nothing else |
| Baseline before any mutation, in the clone at `804f14b` | `11 passed in 0.38s`, exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
