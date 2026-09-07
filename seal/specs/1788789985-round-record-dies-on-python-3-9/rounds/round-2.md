# 1788789985-round-record-dies-on-python-3-9 — review round 2

| Field | Value |
|---|---|
| Target SHA | ea2aa70 |
| Ran by | warden on claude-opus-5 |
| PR | 235 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of `1788789985-round-record-dies-on-python-3-9` (ticket #226, PR #235), at target `ea2aa70`, base `86e140f`. The verifying round: round 1's seven findings were answered across `1e24566 ed7f577 cedc58e 00bc9b0 fb45bc1 362cdd6`, plus `011beb1` and `ea2aa70` from the orchestrator, and the diff of those fixes is what this round was pointed at.

Round 1's verdicts were inherited rather than re-litigated. The highest-value targets were the two paste-ready fixes the fix pass REFUSED after measuring them, because a refusal that is wrong ships a defect the round had already caught. First, it kept the shipped `zip\(.*strict=` half of `ABOVE_THE_FLOOR` and moved only the UTC half, on the grounds that the report's balanced-paren rewrite is blind to `zip(xs, f(g(y)), strict=True)`; both candidate patterns were to be built and run over the tree, and then the harder question asked — is there a construct in the class that BOTH miss. Second, it found that finding 2's row was already failing `tests/test_a_rider_reaches_its_file.py::test_no_schedulable_row_carries_a_coordinate`, contradicting the report's *"Nothing in the tree parses this file"*; that was to be verified red before the fix pass touched it.

Three further axes were named. The two blind spots the fix pass deliberately did NOT close under the 3+ Fix Rule — a `zip(` whose `strict=` is on a later line, and a bare `from datetime import UTC` — were to be judged for whether the refusal is right and whether both are genuinely absent from the tree. Finding 4's disposition was to be judged: it was fixed rather than answered, and measuring it turned up `load`'s missing-checker path raising `FileNotFoundError` as a bare traceback at exit 1, left as a stamped `# RIDER:` in a work item whose whole complaint is that a bare traceback is the defect. And finding 3's own fix has a stated edge — the widened AST check sees module-level statements that CALL something, so an `ImportFrom` above the guard goes unseen.

The orchestrator's three `NAME NOT IN TREE` markers on round 1's record lines were to be checked for exempting only the lines they sit on.

The bound was stated: round 1 met the reopening floor, a round that opens nothing needing a fix does not consume the cap, and an unfounded finding here costs the run its last round. The report was to be written to a file under the work item, finding ids bare integers.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A sixth member of the class ships and the case written to stop a sixth cannot see it | `tests/test_a_script_says_which_interpreter_it_needs.py:466` (`:410` at round 1) | answered | Executed at `ea2aa70`: the shipped pattern and the report's rewrite each return the same six files, and an AST re-derivation against the real 3.9.6 returns the same six with no file that neither pattern finds. `session_cost.py` is in `CLASSIFIED`. The zip half was kept on measured grounds and the measurement reproduces — the rewrite misses `zip(xs, f(g(y)), strict=True)`, which the shipped half catches |
| 2 | The `seal/follow-up.md` deferral row is separated from its table, and its text says four | `seal/follow-up.md:41` | answered | Executed: `test_no_schedulable_row_carries_a_coordinate` exits 1 at `2b8a50a` and 0 at `ea2aa70`, so round 1's *"nothing in the tree parses this file"* was false and the report's own fix would have kept the case red. Read: the blank line is gone, the row is inside the table, the count is five |
| 3 | `test_the_guard_precedes_every_other_module_level_act` asserts against one act | `tests/test_a_script_says_which_interpreter_it_needs.py:374` (`:350` at round 1) | answered | Executed: `_EARLY = os.path.abspath(__file__)` above `FLOOR` is now red on that case (`module level calls abspath()`), where the shipped case was green against the same mutation |
| 4 | The rewritten exit-code paragraph reads as exhaustive for pre-write failures | `skills/code-review/scripts/round_record.py:99` | answered | Executed: the real script with `chain_check.py` deleted exits 1 with `FileNotFoundError`, and `spec_from_file_location` returns a spec with a loader for a path that does not exist — the rider's claim is exact. Both docstrings now say 1 and both are true. `argparse` exits 2 on bad arguments, measured, which lands on the code the paragraph already documents |
| 5 | `spec.md` cites pre-guard line numbers into `round_record.py` | `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:28` | answered | Read against the AST: `#swallowed` is line 871, `#inherited_rows` 1039, `#signature` 1691 and 1695. The unit names resolve. One bullet in the same file was missed — finding 12 |
| 6 | The ledger fragment's R3 states a count that is wrong | `seal/ledger/1788789985-round-record-dies-on-python-3-9.md` | answered | Read: R3 now says six and five, names both surviving blind spots, and records the declined rewrite. Executed: `bin/evidence-check` exits 0, `777 ok · 0 drifted · 0 broken` |
| 7 | `BELOW_FLOOR`'s `§` is written before `__main__` reconfigures stderr | `skills/code-review/scripts/round_record.py:165` (`:158` at round 1) | answered | Executed: with the `§` put back, `test_the_refusal_is_ascii_because_it_is_written_before_stderr_is_set_up` exits 1 naming `['§']`. The new case is seen red against the defect it pins |
| 8 | The widened AST check cannot see an `ImportFrom` above the guard, as it cannot see an `Import` | `tests/test_a_script_says_which_interpreter_it_needs.py:374` | answered | Executed: `from datetime import UTC` and `import tomllib` above `FLOOR` each turn `test_the_script_refuses_at_entry_on_a_below_floor_interpreter` red and each makes the real script exit 1 on 3.9.6, so the module does catch them — on a machine that has a below-floor interpreter, which its docstring says no CI runner does. Read: E402 forces imports above the guard, so the exemption is not a placement the check could demand instead. Every module-level import of all six members of the class was run under 3.9.6 and none fails on the version |
| 9 | `overview.md` says the class is five files and *and four others* where `questions.md` says six and five | `seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:21` | open | Read: the same sentence in two records with different numbers. Finding 1's count fix reached `spec.md`, `changelog.md`, `questions.md`, the ledger fragment and `seal/follow-up.md`, and not this one |
| 10 | `overview.md` labels *eleven cases* as executed; the module has twelve | `seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:6` | open | Executed in the clone at `ea2aa70`: `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` reports `12 passed`, exit 0 |
| 11 | `overview.md` says the ledger fragment carries twelve coordinates; it carries thirteen | `seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:5` | open | Executed: `bin/evidence-check` reports `13 ok · 0 drifted · 0 broken` for that fragment at `ea2aa70` |
| 12 | `spec.md`'s `removesuffix` bullet cites `round_record.py:982`; the call is at `:1086` in `reach_back` | `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:42` | open | Read against the AST: `removesuffix` is at 1086 now and was at 1054 at `2b8a50a`. The other coordinates in the same file were converted to units in the same commit |

## Paste-ready fixes

```
`seal/follow-up.md`'s own opening says a repository with a tracker "should normally hold none of those", and that anything tied to a coordinate is a `# RIDER:` at the line. A rider was weighed and rejected: the finding is about a class of six files, a rider at one line cannot say *and five others*, and nobody opens `gather_changelog.py` before running it. Q1 leaves the tracker-versus-file call to the owner, and it changes where the row lives rather than what it says
```
```
· verified: **executed** — the new module's twelve cases, `tests/test_the_record_is_generated.py`'s 94, seven mutations of the guard, `python3 -m py_compile` at 3.9.6 over every shipped `.py`, the real script under 3.9.6 before and after, `ruff check` and `ruff format --check` on the two changed files. **Unverified** — the full suite, the repository-wide lint and the typecheck, which `agent-contract` §2 reserves for the orchestrator
```
```
· evidence: three rows in `seal/ledger/1788789985-round-record-dies-on-python-3-9.md`, thirteen coordinates, all resolved by `evidence_check --reverify`
```
```
- **`round_record.py#reach_back`'s `removesuffix`** is 3.9 and is not part of this.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py tests/test_a_rider_reaches_its_file.py -q` in the clone at `ea2aa70`, exit read with `; echo $?` and not through a pipe | `20 passed`, exit **0** |
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` alone | `12 passed`, exit **0** — eleven at `804f14b`, twelve now |
| `bin/test tests/test_a_rider_reaches_its_file.py -q` at `2b8a50a`, before the fix pass | exit **1** — `test_no_schedulable_row_carries_a_coordinate`, `coordinate-tied rows in the schedulable list`. Round 1's *"nothing in the tree parses this file"* is disproved |
| The same at `ea2aa70` | exit **0** |
| Both candidate patterns compiled and run over the 30 shipped `.py` | shipped: 6 files · the report's balanced-paren rewrite: **the same 6**. The fix pass's claim reproduces |
| The two patterns against nine synthetic constructs | `zip(xs, f(g(y)), strict=True)` — shipped **matched**, rewrite **missed**. Multi-line `zip(` — shipped missed, rewrite matched. `from datetime import UTC` used bare — **both missed** |
| Class re-derived from the AST: every `alias.attr` resolved to its stdlib module and asked of 3.9.6, plus every `zip(…)` with any keyword at any depth | **six** members, the same six. No file the AST finds that neither pattern finds; no file a pattern finds that the AST does not |
| Shipped tree grepped for `tomllib`, `pairwise`, `StrEnum`, `ExceptionGroup`, `TaskGroup`, `file_digest`, `bit_count`, `contextlib.chdir`, `sys.stdlib_module_names` | no hit — no other above-floor name the text scan would miss |  <!-- NAME NOT IN TREE -->
| Every module-level import of all six members of the class run under `/usr/bin/python3` (3.9.6) | the only failures are `import console` and `import optin`, sibling modules failing on `sys.path` rather than on the version |
| Mutation in the clone: `from datetime import UTC` inserted above `FLOOR` | suite exit **1**, `test_the_script_refuses_at_entry_on_a_below_floor_interpreter`; the real script on 3.9.6 exits **1** with `ImportError`. Restored byte-identical |
| Mutation: `import tomllib` above `FLOOR` | suite exit **1**, the same case; real script exits **1** with `ModuleNotFoundError`. Restored byte-identical |
| Mutation: `_EARLY = os.path.abspath(__file__)` above `FLOOR` (round 1's control) | suite exit **1** on the widened AST case; the real script still exits **2** with the refusal. Restored byte-identical |
| Mutation: the `§` put back into `BELOW_FLOOR` | exit **1** — `the refusal carries ['§'], which prints as an escape under an ASCII stderr`. The one new case is seen red against its own defect |
| The real script with `chain_check.py` deleted, at 3.13 | exit **1**, `FileNotFoundError` traceback. `chain_check.py` restored byte-identical |
| `spec_from_file_location('x', '/nope/does_not_exist.py')` | `spec: True · loader: True` — the `SystemExit` branch in `load` is unreachable from this call site |
| `round_record.py --no-such-flag` and with no subcommand, exits read directly | exit **2** both times — `argparse`'s exit is a fourth process exit the module's AST cannot see, and it lands on the code the docstring documents |
| Exit sites enumerated from `round_record.py`'s own AST | `raise SystemExit(2)` at 191, `raise SystemExit(<f-string>)` at 226, `sys.exit(main())` at 2284 — the docstring's three |
| `bin/evidence-check` at `ea2aa70` | exit **0** — `777 ok · 0 drifted · 0 broken`; the work item's fragment `13 ok` |
| The three `NAME NOT IN TREE` markers stripped, `bin/evidence-check` re-run | exit **2**, exactly three refusals, all `py_compile`, one per marked line; names read 50 against 47 with the markers. Markers restored, exit **0** |
| `bin/test tests/test_a_record_states_what_the_tree_has.py -q` at `ea2aa70` | `58 passed`, exit **0** — the checker the fix pass reported red is green with the markers in |
| The four `zip(…, strict=)` sites mapped to enclosing units from the AST | 871 `swallowed` · 1039 `inherited_rows` · 1691 and 1695 `signature` — `spec.md`'s new unit citations resolve |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_script_says_which_interpreter_it_needs.py:410` | round 1's 1 — fixed |
| round-1 | `seal/follow-up.md:41` | round 1's 2 — fixed |
| round-1 | `tests/test_a_script_says_which_interpreter_it_needs.py:350` | round 1's 3 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:99` | round 1's 4 — fixed |
| round-1 | `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:27` | round 1's 5 — fixed |
| round-1 | `seal/ledger/1788789985-round-record-dies-on-python-3-9.md` | round 1's 6 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:158` | round 1's 7 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Closing the pattern's two remaining blind spots with an AST walk | `seal/ledger/1788789985-round-record-dies-on-python-3-9.md` R3, `spec.md` §*The class, enumerated by construction*, and the pattern's own comment | the repository owner |
| The five remaining members of the class, still dying below the floor with a bare traceback | `seal/follow-up.md` §*Schedulable items with nowhere else to go* | the repository owner |
| Giving `load` a sentence instead of a `FileNotFoundError` traceback | `# RIDER:` at `round_record.py#load`, stamped `2026-09-08 at cedc58e` | whoever next opens `round_record.py#load` |
