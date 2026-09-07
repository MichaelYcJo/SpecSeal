# Round 1 — `1788789985-round-record-dies-on-python-3-9` (#226, PR #235)

Target `804f14b3a8ab34b0b01de6f03bc2a7856d1d9508`, unchanged throughout the
round; the worktree was clean at start and at finish. No `rounds/` directory
existed, so nothing was carried from an earlier round — every verdict below is
derived in this round.

All mutation work was done in a `git clone --no-local` of the worktree at the
target SHA, under the scratchpad, deleted at the end. Nothing was written in
`/Users/yc/Documents/GitHub/SpecSeal-worktrees/wi-226` except this report.

## What the acceptance criteria came out as

**AC1, the guard fires at entry — holds, executed.** The real script on the
real 3.9.6 (`/usr/bin/python3`, an Xcode shim), exit code read directly and not
through a pipe:

```
run exit: 2
round-record: needs python 3.12 or newer, and this is python 3.9.6 at /Applications/Xcode.app/Contents/Developer/usr/bin/python3.
Nothing was read and nothing was written.
`python3` is not always the newest interpreter installed -- macOS ships python 3.9 under that name -- so name one explicitly, `python3.12 <this script> ...`, or see CONTRIBUTING.md §Running the checks.
```

The orchestrator's correction is answered: the exit code is **2**, and the
hand-back was right about it.

**The guard is early enough, which the handoff asked to be attacked rather than
assumed.** Everything above it is the module docstring and ten stdlib imports —
`argparse ast importlib.util json os re shutil subprocess sys tempfile` — all
of which exist in 3.9, and the run above proves it by reaching the guard rather
than by argument. The whole module also compiles under 3.9
(`/usr/bin/python3 -m py_compile`, exit 0), which is the condition that matters
more than import order: Python compiles the entire file before executing the
first line, so a 3.10+ *syntax* construct anywhere below the guard would keep
the guard from ever running. There is none.

**AC2, nothing changes above the floor — holds.** `py_compile` clean, the  <!-- NAME NOT IN TREE -->
module's own 11 cases green at the target, and
`test_above_the_floor_the_same_arguments_get_past_the_guard` is the control
that keeps the refusal cases honest.

**AC3, a regression test seen red that does more than assert a constant —
holds, and I re-ran the two mutations that would have hurt most had they
survived.**

- The decisive one the branch claims: the guard moved out of module level into
  `main()`. Re-run, and the claim is exactly right — `10 passed, 1 failed`, and
  the single failure is `test_the_guard_precedes_every_other_module_level_act`.
  Every end-to-end case stayed green, because on 3.9 `chain = load(CHAIN, …)`
  succeeds and `argparse` parses the junk arguments before the relocated guard
  speaks. The AST case is load-bearing, not decoration.
- The floor pin: `FLOOR` in `.github/scripts/run_tests.py` raised to `(3, 13)`
  with the guard's literal left at `(3, 12)`. Red, on
  `test_the_floor_is_the_number_the_runner_and_the_linter_hold`, naming both
  numbers. The pin can fail, so the branch's argument for retyping the floor
  rather than importing it rests on something real.

**AC4, `strict=True` stays and `spec.md` says why — holds.** Four `zip(…,
strict=)` sites survive in `round_record.py` (839, 1007, 1659, 1663 — confirmed
from the AST, not from a text scan), and `spec.md` §*Scope* argues the
invariant rather than asserting it.

**The corrected scan pattern does find all four `zip` sites.** I re-derived them
from the AST, which cannot be fooled by a parenthesis, and got the same set the
branch's `zip\(.*strict=` gets. That half of the correction is sound.

**What is not sound is the other half of the same pattern**, and it is finding 1.

## The class, re-derived rather than read

I did not read `spec.md`'s table for this. I built the set from the tree:

1. **Entry points.** `git ls-files '*.py'`, less `tests/` and `seal/`, grepped
   for `__name__ == "__main__"` — **25 files**, the same 25.
2. **Syntax below the floor.** `/usr/bin/python3 -m py_compile` (3.9.6) over
   all 111 tracked `.py` — **one failure, `tests/test_the_root_migrates_itself.py`**,
   a test file. So no shipped script carries 3.10+ syntax, and the branch's
   third construction reproduces.
3. **Runtime API below the floor, by AST rather than by regex.** For every
   shipped file I resolved each `alias.attr` back to the stdlib module the
   alias imports, then asked the 3.9 interpreter itself whether that attribute
   exists — and separately collected every `zip(…)` call carrying any keyword,
   at any parenthesis depth. This is the construction that does not depend on
   how the import was spelled.

That third construction returns **six** members, not five:

| File | Construct | Needs |
|---|---|---|
| `skills/code-review/scripts/round_record.py` `:839 :1007 :1659 :1663` | `zip(…, strict=)` | 3.10 |
| `hooks/root-migrate.py:425` | `zip(…, strict=)` | 3.10 |
| `.github/scripts/gather_changelog.py:151` | `datetime.UTC` | 3.11 |
| `.github/scripts/fold_ledger.py:358` | `datetime.UTC` | 3.11 |
| `skills/implement/scripts/seal.py:324,436` | `datetime.UTC` | 3.11 |
| **`skills/verify/scripts/session_cost.py:89`** | **`dt.UTC`, behind `import datetime as dt`** | **3.11** |

The sixth is finding 1. `spec.md`'s row 9 places it out of the class with the
words *nothing found*, and its `Count:` line, the ledger fragment's R3 and the
`seal/follow-up.md` row all say five and four.

## Findings

### 🔴 1 · A sixth member of the class ships, and the case written to stop a sixth cannot see it

`tests/test_a_script_says_which_interpreter_it_needs.py:410` ·
`skills/verify/scripts/session_cost.py:89`

`ABOVE_THE_FLOOR = re.compile(r"zip\(.*strict=|datetime\.UTC")` matches the
text `datetime.UTC`. `session_cost.py` writes `import datetime as dt` and then
`dt.UTC`, so the pattern cannot match it, `shipped_python()` walks straight
past the file, and
`test_no_shipped_script_needs_more_than_the_floor_without_saying_so` is green
while a shipped script carries a 3.11 construct.

This is the same shape of blind spot as the `zip\([^)]*strict=` one the branch
recorded and corrected — one construct over. The first spelling was blind to a
nested parenthesis; the corrected spelling is blind to an import alias.

`session_cost.py` is a shipped entry point (`__main__`), it is what
`docs/review-handoff-protocol.md:497` points at for measuring a run, and it is
run with whatever `python3` is on PATH — which is the class's own stated
property.

**Executed, not read.** On 3.9.6, end to end, against a transcript whose
timestamps carry no zone — the "mixed transcript this normalisation was written
for", in its own docstring's words:

```
--- 3.9.6 ---
exit: 1
    return stamp if stamp.tzinfo is not None else stamp.replace(tzinfo=dt.UTC)
AttributeError: module 'datetime' has no attribute 'UTC'
--- this suite's python ---
exit: 0
```

A bare interpreter traceback, mid-run, on a shipped script — which is #226's
complaint, at a second coordinate.

The `dt.UTC` sits *outside* the `try/except (ValueError, AttributeError)` two
lines above it, so the surrounding tolerance does not catch it.

**The fix is the pair, and it has to be the pair.** Adding the row to
`CLASSIFIED` alone is refused by the case's own `gone` assertion, because the
pattern still cannot find what the row classifies — I ran that and got
`AssertionError: ['skills/verify/scripts/session_cost.py'] no longer carry the
construct they were classified for`. With both applied: `11 passed`.

Then the count follows into `spec.md` row 9 and its `Count:` line, the ledger
fragment's R3, `overview.md`, `changelog.md`, `questions.md` and the
`seal/follow-up.md` row — five members, four deferred, becomes six and five.

### 🟡 2 · The deferral row is not in the table it was written for, and it says four

`seal/follow-up.md:41-42`

Line 41 is blank, so the new row does not join the table at lines 38-40. GFM
ends a table at the first blank line: the row renders as a paragraph beginning
with a literal `|`, not as a row of *Schedulable items with nowhere else to go*,
and its `Who must answer` value stops being a column.

That matters more than layout here. `seal/follow-up.md`'s own opening makes the
answerer column the thing that admits a row at all — *"A row that cannot name
who answers it does not belong in this file"* — and the round's whole defence
of the deferral is that an answerer was named. A person scanning the table does
not see this row in it.

The row's text also says **Four more scripts**, which finding 1 makes five, and
names four coordinates where there are five.

Nothing automated reads this file, so nothing catches either half.

**On whether the deferral is real, which the handoff asked me to judge
separately:** it is. `questions.md` Q1 records the tension against the file's
own opening honestly, names the repository owner as answerer, and states the
default. That is a question with an answerer, not a deferral to nobody, and
where the four (five) rows finally live is the owner's call and not this
branch's. I am not asking for them to move.

### 🟡 3 · `test_the_guard_precedes_every_other_module_level_act` checks one act

`tests/test_a_script_says_which_interpreter_it_needs.py:345,350-355`

The case is named for every other module-level act and asserts against exactly
one: the first `x = load(…)` assignment. Anything else placed above the guard —
an `open`, a `subprocess.run`, a constant read off the disk — is invisible to
it.

**Executed.** With `_EARLY = os.path.abspath(__file__)` inserted immediately
above `FLOOR = (3, 12)` in `round_record.py`, the shipped module is **fully
green, 11 passed**. The widened check in the paste-ready fix below reports
`module level calls abspath() at line 150, above the guard at line 183`.

Today the file has nothing there but imports, so this is a pin that is weaker
than its name rather than a defect on disk. It matters because the guard block
is documented as *the spelling to copy* into four (five) other files, and this
case is the only thing that says where the copy has to go.

### 🟡 4 · The rewritten exit-code paragraph is exhaustive about a path that exits 1

`skills/code-review/scripts/round_record.py:99-101`, against `:194`

The paragraph now reads *"0 and 1 are `chain_check`'s own, after the record is
written · 2 the input was unusable, or the interpreter is below the floor —
either way nothing was read and nothing was written."*

`load` at `:194` raises `SystemExit` with a string, which exits **1** (executed:
`raise SystemExit('boom')` → exit 1), and it does so before anything is read or
written — a missing `chain_check.py`. So the one failure most literally
described by *nothing was read and nothing was written* is the one the same
paragraph files under "after the record is written". `load`'s own docstring
says *"a missing checker is exit 2"*, which is wrong for the same reason.

Both are pre-existing lines the diff did not author. What puts it in scope is
that this diff is the edit that re-states the exit-code contract, and
`test_the_docstring_says_what_exit_2_now_covers` pins only the word
`interpreter` in it. If the smith answers with grounds — that the contract's
1-vs-2 line predates #226 and belongs to its own change — that is an answer I
would accept.

Nothing automated branches on this script's exit codes. I checked every
reference to `round_record.py` in the tree: `chain_check.py` does not invoke it,
`hooks/hooks.json` does not, no workflow does. The only consumers of `2` are
the suite's own `assert code == 2` lines, which all run above the floor and so
never meet the new source.

### ⬜ 5 · `spec.md`'s coordinates into `round_record.py` are pre-guard line numbers

`seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:27,79`

§*Scope* cites *"the comment at `round_record.py:761-766`"* and the table cites
`:767 :935 :1587 :1591`. The guard adds 72 lines above all four, so in the file
as shipped those sites are at 833-838 and `:839 :1007 :1659 :1663`. A reader
opening `:767` lands in unrelated docstring prose.

A correction to the run's paperwork, so it is not in `Needs a fix`.

### ⬜ 6 · The ledger fragment's R3 states a count that is wrong

`seal/ledger/1788789985-round-record-dies-on-python-3-9.md`, row R3

Its *Verified behavior* cell is labelled **Executed** and says *"Five files
carry a runtime construct above the floor; one is fixed here and four are in
`seal/follow-up.md`"*. Six, and five. The row's own Notes cell already states
the limit that caused it — *"it matches two constructs by text, so a 3.10+
construct nobody has thought of is invisible to it"* — and this is that limit
firing on a construct the row had thought of, spelled differently.

Same coordinate class as 5, so not in `Needs a fix`.

### ⬜ 7 · The one non-ASCII character in the message is in the message for the worst-configured machine

`skills/code-review/scripts/round_record.py:158`

`BELOW_FLOOR` ends with `CONTRIBUTING.md §Running the checks`. The module-level
guard writes it before `__main__`'s `reconfigure(errors="backslashreplace")`
block runs, since that block is at the bottom of the file. Under
`PYTHONIOENCODING=ascii` the line prints as `CONTRIBUTING.md \xa7Running the
checks` — degraded, not fatal, and I confirmed the exit code stays 2. Worth a
`§` → `section ` swap only because this block is documented as the one to copy
into a hook, whose stderr nobody is watching.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A sixth member of the class ships and the case written to stop a sixth cannot see it — `dt.UTC` behind an aliased import defeats `ABOVE_THE_FLOOR`, and `session_cost.py` dies with a bare traceback on 3.9 | `tests/test_a_script_says_which_interpreter_it_needs.py:410` | open | Executed: `session_cost.py` under 3.9.6 exits 1 with `AttributeError: module 'datetime' has no attribute 'UTC'` at `:89`, end to end on a zone-less transcript; the module's own 11 cases are green at the same time; an AST re-derivation returns six members where the branch's pattern returns five |
| 2 | The `seal/follow-up.md` deferral row is separated from its table by a blank line, so it is not a row of *Schedulable items with nowhere else to go* and its `Who must answer` value is not a column; its text also says four where finding 1 makes five | `seal/follow-up.md:41` | open | Read: line 41 is blank and lines 38-40 are the table; GFM ends a table at the first blank line. Nothing in the tree parses this file, so nothing catches it |
| 3 | `test_the_guard_precedes_every_other_module_level_act` asserts against one act, the `load(…)` assign, not against every module-level act as its name says | `tests/test_a_script_says_which_interpreter_it_needs.py:350` | open | Executed: with `_EARLY = os.path.abspath(__file__)` inserted above `FLOOR`, the shipped module reports `11 passed`; the widened check reports `module level calls abspath() at line 150, above the guard at line 183` |
| 4 | The rewritten exit-code paragraph reads as exhaustive for pre-write failures, but `load`'s refusal at `:194` exits 1 and the same paragraph files 1 under *after the record is written* | `skills/code-review/scripts/round_record.py:99` | open | Executed: `raise SystemExit('boom')` exits 1. Read: no caller in the tree branches on this script's exit code, so the blast radius is the documented contract only. Pre-existing wording; answerable with grounds |
| 5 | `spec.md` cites `round_record.py:761-766` and `:767 :935 :1587 :1591`, which are the pre-guard line numbers — 72 lines short of where those sites now are | `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:27` | open | Read against the file: the comment is at 833-838 and the four `zip` sites are at 839, 1007, 1659, 1663, confirmed from the AST |
| 6 | The ledger fragment's R3 states, under an **Executed** label, that five files carry a construct above the floor and four are deferred | `seal/ledger/1788789985-round-record-dies-on-python-3-9.md` | open | Same executed enumeration as finding 1: six and five |
| 7 | `BELOW_FLOOR`'s `§` is written before `__main__` reconfigures stderr, so under an ASCII stderr the sentence ends `CONTRIBUTING.md \xa7Running the checks` | `skills/code-review/scripts/round_record.py:158` | open | Executed: `PYTHONIOENCODING=ascii /usr/bin/python3 …` prints the escape and still exits 2 |

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

## Deferred

*(nothing to drain)*

## Paste-ready fixes

**Finding 1 — the pattern and the row, together.** `tests/test_a_script_says_which_interpreter_it_needs.py`, replacing the `ABOVE_THE_FLOOR` line and its comment:

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

and, in `CLASSIFIED`:

```python
    "hooks/root-migrate.py": "deferred, seal/follow-up.md (#226)",
    "skills/verify/scripts/session_cost.py": "deferred, seal/follow-up.md (#226)",
}
```

and the docstring sentence in the same case, which states the count:

```python
    `skills/agent-contract/SKILL.md` §12: the finding named one coordinate and
    what was owed was every instance the same cause produces. Six files
    carried one, and five of them are somebody else's branch or somebody
    else's release. This is what keeps a seventh from arriving as a traceback
    on a stranger's mac.
```

**Finding 2 — the blank line, the count, and the fifth coordinate.** `seal/follow-up.md`: delete the blank line at 41 so the row joins the table, and amend the row's opening and its coordinate list:

```
| Bring `agents/smith.md` and `agents/scribe.md` under `tests/test_docs_line_wrap.py`, together. … | the repository owner |
| **Five more scripts die below the supported floor with a bare traceback, the way `round_record.py` did before #226.** Enumerated by construction in `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md` §*The class, enumerated by construction*, and re-enumerated on every suite run by `tests/test_a_script_says_which_interpreter_it_needs.py#test_no_shipped_script_needs_more_than_the_floor_without_saying_so`, so this row is a decision waiting rather than a fact that can go stale. `.github/scripts/gather_changelog.py:151` and `.github/scripts/fold_ledger.py:358` use `datetime.UTC` (3.11) and are named after a literal `python3 ` in `CONTRIBUTING.md:128-131` and `docs/release-checklist.md` §3 — so a release run on a 3.9 or 3.10 `python3` fails at the moment it writes the dated heading. `skills/verify/scripts/session_cost.py:89` is the same construct behind `import datetime as dt`, and it ends the run report `docs/review-handoff-protocol.md` §*After a run* points at. `skills/implement/scripts/seal.py:324,436` is the same construct and **was not touched because another work item in this release holds that file**. `hooks/root-migrate.py:425` uses `zip(..., strict=True)` and is reached through `hooks/hooks.json`'s session-start dispatch, so it fails while migrating a 0.3.x layout, in a hook, where nobody is reading. The fix is fifteen lines each, copied from `skills/code-review/scripts/round_record.py#below_floor`, which was written to be copied and says so. **What needs a person is not the fix, it is whether these belong in the tracker instead**: this file's own opening says a repository with a tracker should normally hold none of these, and the handoff for #226 asked for them here | the repository owner |

## Riders waiting on a file another branch holds
```

**Finding 3 — the AST case, widened.** `tests/test_a_script_says_which_interpreter_it_needs.py`, appended to `test_the_guard_precedes_every_other_module_level_act` after the existing `assert refusal < acts` block. Verified green at the target and red against an act inserted above the guard:

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

**Finding 4 — the exit-code paragraph.** `skills/code-review/scripts/round_record.py`, the docstring's last paragraph:

```
Exit codes: 0 and 1 are `chain_check`'s own, after the record is written · 2
the input was unusable, or the interpreter is below the floor — either way
nothing was read and nothing was written · a sibling script that will not load
is `SystemExit` with a sentence, which is 1 before anything is read.
```

and `load`'s docstring at `:194`, which says 2 for a code that is 1:

```python
    """Import a sibling script by path, or die — a missing checker is exit 1."""
```

**Finding 5 — the stale coordinates.** `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md`, §*Scope*:

```
- **The four `strict=True` sites stay exactly as they are.** The comment at
  `round_record.py:833-838` says what the first one states: both of the
```

and the table's row 1 coordinate:

```
| 1 | `skills/code-review/scripts/round_record.py` `:839 :1007 :1659 :1663` | `zip(..., strict=True)` → `TypeError: zip() takes no keyword arguments`, after the report has been read | 3.10 | the orchestrator's `python3` | **fixed here** |
```

**Finding 6 — the ledger count.** `seal/ledger/1788789985-round-record-dies-on-python-3-9.md`, R3's *Verified behavior* cell, last sentence:

```
Six files carry a runtime construct above the floor; one is fixed here and five are in `seal/follow-up.md`
```

**Finding 7 — the section sign.** `skills/code-review/scripts/round_record.py`, the last line of `BELOW_FLOOR`:

```python
    "<this script> ...`, or see CONTRIBUTING.md section 'Running the checks'."
```

## What I did not verify, and who answers it

- **The full suite, the repository-wide lint and the typecheck** — `unverified`.
  `skills/agent-contract/SKILL.md` §2 forbids them to me; the **orchestrator**
  answers. I ran one module, `tests/test_a_script_says_which_interpreter_it_needs.py`,
  in a clone at the target, and the paste-ready fixes above are green in that
  same module. The two runs the handoff labelled executed — the 105-passed pair
  and `ruff` — I left to the orchestrator's re-run as instructed and did not
  repeat.
- **`hooks/root-migrate.py:425`'s reachability while migrating a 0.3.x layout**
  — `read`. I confirmed the dispatch (`hooks/dispatch.py:48` lists
  `root-migrate.py` under `session-start`) and the construct, not that a 0.3.x
  tree reaches that line. It changes nothing about the classification; the
  **repository owner** answers it as part of the deferral.
- **Behaviour on an interpreter older than 3.9.6** — `unverified`, and the
  ledger fragment already says so. This machine has nothing older.

**Broad gate: not yet.** No run of it exists at any SHA on this branch.

Nothing in my prompt asked for a check §2 excludes, so there is no declined
instruction to name.

Needs a fix: yes — findings 1, 2 and 3; finding 4 is answerable with grounds
Loses a record or crashes: yes — `skills/verify/scripts/session_cost.py:89` exits 1 with a bare `AttributeError` traceback on python 3.9, and finding 1 is that the branch's enumeration and its regression test both place that file out of the class

## Proof block

Opened, in the worktree at `804f14b`:

- `skills/code-review/scripts/round_record.py` (docstring, guard block, `load`, `main`, the four `zip` sites)
- `tests/test_a_script_says_which_interpreter_it_needs.py` (whole file)
- `skills/verify/scripts/session_cost.py` (imports, `parse_time`, the transcript reader)
- `seal/follow-up.md` (opening and the table)
- `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md` (whole file)
- `seal/specs/1788789985-round-record-dies-on-python-3-9/questions.md`
- `seal/ledger/1788789985-round-record-dies-on-python-3-9.md`
- `.github/scripts/run_tests.py` (`FLOOR`), `bin/test`
- `hooks/dispatch.py:48`, `hooks/hooks.json`
- `docs/review-handoff-protocol.md` §*After a run*
- `CONTRIBUTING.md:12,15,128-131`, `docs/release-checklist.md` §3, `docs/branch-and-release.md:163,184`
- `seal/config.md`
- `skills/code-review/scripts/chain_check.py:303,626,2737`
- `tests/test_release_hygiene.py:1075-1100`, `tests/test_docs_line_wrap.py` (`COVERED`)
- the diff `86e140f..804f14b` for `skills/code-review/scripts/round_record.py` and `seal/follow-up.md`
