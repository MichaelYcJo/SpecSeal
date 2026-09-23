# 1790154760-the-ledger-grows-and-nothing-takes-a-row-out — review round 1

| Field | Value |
|---|---|
| Target SHA | be4e091737feb6aa99c8a623bb0858da1de52c27 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 531 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `e554d21cd3253e601e7fb41d6e52ff1f0e2bb36a..7b0e9b75d60b4530c75084ff5bf5b105435eeb07`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1, `hooks/ledger-migrate.py` still states the checker's full run as ~130 ms, the stale-cost class this work item exists to correct |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #519, PR #531, over the whole branch `f8f1c9de..be4e0917`. Stage 1 asked whether the decision follows from the framer's measurements (no ledger row leaves; `py_spans` is memoised by file text). It also asked whether the output is truly unchanged, re-measured in a clone on `--strict`, `--reverify` and the advisor path. Stage 2 attacked the memo:

- staleness within one process: `--reverify`, a file edited between two reads, identical text at two paths
- whether callers still get independent mutable copies
- whether the unbounded `functools.cache` matters for this corpus
- whether `rider_check.py` or any other caller depends on parsing per call

It also asked whether every place stating the old cost was corrected, and whether the new sentence names its instrument and date. Finally it judged the smith's two edits outside the code: the reworded stamp in the framer's `spec.md` and `phases/phase-2.md`, and the raw test docstring.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `hooks/ledger-migrate.py` still states the checker's full run as "~130 ms", undated and with no instrument, now wrong by 14x. It is a fourth instance of the stale-cost class that the branch enumerated by the literal "114 ms" | `hooks/ledger-migrate.py:32-35` | **fixed** `7b0e9b75` | fixed at 7b0e9b75 — the class enumerated by what a sentence claims; `hooks/ledger-migrate.py` and `skills/evidence-check/SKILL.md` re-measured and dated; three sentences left with grounds in ledger row C3; Read and `git log -S` (`117d37fe`, 2026-09-01). The full check measured 1.90 s at the target (executed) |
| 2 | ⬜ `py_spans`'s docstring and the parse-count case's docstring state "1,328 parses of 126 files, about 94 % of a 15.8 s run" with no instrument | `skills/evidence-check/scripts/evidence_check.py:169-172`, `tests/test_a_row_points_by_content.py:126-128` | **fixed** `7b0e9b75` | fixed at 7b0e9b75 — the `py_spans` docstring and the parse-count case's docstring carry the instrument and the date; Read. The sentences are past-tense motivation, so no behaviour or current fact is wrong |
| 🟢 | The decision (memoise the parse, remove no row) follows from `spec.md`'s three measurements | `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md` §1–§3, Scope | not a defect | Read |
| 🟢 | Output unchanged: `--strict`, plain, `--reverify` and the advisor are identical old vs new on one tree, clean and perturbed. The only difference is the `SyntaxWarning` collapsing on stderr, which is disclosed | `skills/evidence-check/scripts/evidence_check.py:152-222` | not a defect | Executed. `diff -r` after `--reverify` is empty |
| 🟢 | No staleness within one process: the key is the text, and the path's influence stays outside the memo | `skills/evidence-check/scripts/evidence_check.py:186-222`, `:363-371`, `:638-641` | not a defect | Read, and the `--reverify` comparison was executed |
| 🟢 | Callers get independent dicts and lists, and each case goes red against its mutant | `skills/evidence-check/scripts/evidence_check.py:180-183` | not a defect | Executed: three mutants, one red each; the old checker gives `10 parses` |
| 🟢 | The memo's size is bounded by what one run reads: 127 texts, 4.88 MB of keys, and the advisor rebuilds it on every commit | `skills/evidence-check/scripts/evidence_check.py:186`, `hooks/evidence-advisor.py:118-120` | not a defect | Executed (the memo's cache statistics, `tracemalloc`) |
| 🟢 | The memo freezes an answer computed under the process's warnings filter. No caller changes the filter mid-process | `skills/evidence-check/scripts/evidence_check.py:186-195` | not a defect | Executed: under `error` the result is `None` and the same text is served `None` under `ignore`. Read: no `filterwarnings` or `-W` in the repository |
| 🟢 | `rider_check.py` and the other callers never mutate the result and do not depend on parsing per call | `.github/scripts/rider_check.py:331`, `:555` | not a defect | Read |
| 🟢 | The advisor's new cost sentence names its instrument, runs, date, platform and the before figure | `hooks/evidence-advisor.py:6-14` | not a defect | Read, plus one run executed at 1.69 s |
| 🟢 | The reworded framing-time stamp in `spec.md` Scope 4 and `phases/phase-2.md` keeps its meaning and is disclosed | `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md` Scope 4 | not a defect | Read `git diff afb0f136..be4e0917`, and `--strict .` exit 0 was executed |
| 🟢 | The raw docstring keeps its value byte for byte | `tests/test_a_row_points_by_content.py:822` | not a defect | Executed an `ast.get_docstring` comparison at base and target |

## Paste-ready fixes

```
  - **silent when there is nothing to migrate** — the every-session scan
    reads `old_format_rows` alone and never runs the full check. Measured
    2026-09-01 at ~24 ms in-process on this repository's own ledgers and
    ~60 ms wall for the whole session-start group; the full check it skips
    took about 1.9 s on the same repository on 2026-09-23
    (`/usr/bin/time -p` over `evidence_check.py --strict .`, macOS, #519)
```
```
    **One parse per distinct text, for the life of the process** (#519). The
    ledger cites one file from many rows, and parsing it once per row was
    1,328 parses of 126 files, about 94 % of a 15.8 s `--strict` run that
    every `git commit` paid through `hooks/evidence-advisor.py` (`cProfile`
    over `--strict .`, 2026-09-23). The memo is
```

## Executed probes

| What was run | Result |
|---|---|
| Old checker file (`f8f1c9de`) vs new (`be4e0917`) on the same clean tree: `--strict .` and a plain run | stdout, stderr and exit identical, exit 0. 16.75 s → 1.90 s and 15.50 s → 1.87 s |
| The same on a perturbed copy (renames, an edit, a moved file, a deleted file, a `SyntaxWarning` file): `--strict .` | stdout identical, exit 2 both, `1459 ok · 1 drifted · 22 broken`. Stderr 22 warning lines old, 1 new |
| `--reverify .` on two identical perturbed copies, old and new | stdout identical, exit 0 both, `21 rows re-verified`. `diff -r` of the two trees afterwards is empty |
| `hooks/evidence-advisor.py` with a `git commit` payload, old and new plugin copies, clean and perturbed trees | clean: empty stdout both, 15.13 s → 1.69 s. Perturbed: the same 24 lines both |
| `bin/test tests/test_a_row_points_by_content.py -k` the three new cases plus the two `py_spans` cases, new checker and then old checker file | new: 5 passed. Old: 1 failed (`10 parses of one file for five rows`), 4 passed |
| The three new cases against three mutants (stored dict returned, dict copied without its lists, `@functools.cache` removed) | each is 1 failed and 2 passed, exit 1. The file was restored and byte-compared |
| In-process full check, reading the memo's cache statistics and `tracemalloc` | 127 misses, 1,212 hits, 4.88 MB of key text, 22.7 MB traced (40.6 MB peak) |
| The same text under `simplefilter("error")` and then `"ignore"`, one module, and a fresh module under `"ignore"` | `None`, then `None` from the memo, then spans from the fresh module |
| `ast.get_docstring` of `test_an_old_format_ledger_is_loud_never_invisible` at `f8f1c9de` and at the target | identical |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and it comes due when the rounds leave nothing open. This round leaves 🟡 1 open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `hooks/ledger-migrate.py`'s "~24 ms in-process" and "~60 ms wall for the whole session-start group" still hold (`spec.md` §2 measured the hook at 0.32 s wall) | this round's 🟡 1 fix dates them rather than re-measuring them | the smith taking 🟡 1, who re-measures them or leaves them dated |
| The `ledger` CI job's wall time on Linux after the change | `overview.md` §Not verified, already deferred by the smith | the orchestrator, reading PR #531's CI run |
