# 1788686494-the-printed-ledger-name-collapses-through-relpath — review round 2

| Field | Value |
|---|---|
| Target SHA | 5c325d8 |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 186 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item `1788686494`, the **verifying round**. Target `5c325d8`, base `origin/release/v0.8.3`, draft pull request #186, issue #163.

The surface is the **diff of round 1's fixes**, `c04977b..5c325d8`, not the branch. Round 1's own verdicts were reached at `c04977b` and are not re-walked. The job is the answers: for each verdict round 1 recorded as closed, is it actually closed.

`round_record.py close` derived `Contract changes | none` and `New units | none` from that range, so there is no new-unit finding surface to treat as a finding surface — verify that derivation is true rather than inheriting it.

Round 1 recorded three findings closed on a fix, all at `d42ad74`:

1. **The class guard under-reached in six constructible shapes**, and five records claimed it could not false-pass. The pass widened `carriers` with a bare-alias rule that also reads tuple targets, and widened `relpath_on_a_ledger` to accept any carrier name anywhere in the first argument, to match a bare call as well as an attribute call, and to cover `normpath` beside `relpath`. It reports the carrier sets stay byte-identical on the current source and offenders stay at zero, and that it declined `abspath` because `file_identity` calls it to build an inode key no person reads. **Ask:** are all six shapes now named; did the widening bring in a false alarm the count hides; is the `abspath` exclusion right, or does it leave a rendering site reachable; and does a seventh shape exist that neither the reviewer nor the pass constructed — the two-step wrapper, a bare `from os.path import relpath`, an f-string, a `%` format, a dict value, a comprehension over a carrier-bearing container.
2. **The separator set built without `altsep` survived all 43 cases.** The pass added one boundary assertion and reports the checker's source is byte-identical to `c04977b`. **Ask:** does the new assertion actually die on that mutation for the reason it names, and does it close the crossing or only the one instance — is there a second boundary spelling the axis grid still prunes.
3. **The drive comparison was unpinned in both directions.** The pass kept the shipped answer and added the assertion. **Ask:** the same question.

And two the pass raised itself, which a verifying round owns because nobody else has read them:

4. **It corrected a fifth claim site the record did not cite** — `test_no_ledger_path_reaches_relpath`'s own docstring. **Ask:** are all five corrected sites now true statements about the widened detector, or has one of the five been narrowed to something the detector still does not do. The four the reviewer named are `changelog.md`, `overview.md`, `phases/phase-2.md` and the ledger fragment's fourth row.
5. **It reports its first reproduction of the shipped gate was unfaithful** — it accepted a bare-name call — and that it then imported `relpath_on_a_ledger` from the test module and re-ran. **Ask:** whether the corrected reproduction is faithful, since every one of finding 1's grounds rests on it.

Facts, labelled:

- **executed by the orchestrator at `d42ad74`** — `git diff --stat c04977b..d42ad74` touches six files and **not** `skills/evidence-check/scripts/evidence_check.py`, so the fix pass's byte-identical claim holds. `./bin/test` over the four evidence-check modules → 170 passed, exit 0. `uvx ruff check skills/ tests/` → All checks passed. `uvx ruff format --check` on the two changed files → clean.
- **read** — `.venv` carries no `ruff` module; use `uvx ruff`. The suite runs through `./bin/test`.
- **unverified** — everything in the five items above; the full suite, repository-wide lint and typecheck, which stay the orchestrator's.

Run the ledger check unscoped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's finding 1 — the class guard's six under-reaching shapes | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:489-533`, `:416-487` | answered | Verified closed. Executed: the `c04977b` detector and the `5c325d8` detector loaded side by side over the checker source; carrier sets identical function by function, both report zero offenders, and all six shapes go `[] → ['main']`. Nine further shapes constructed (`realpath`, `abspath`, dict value, keyword first arg, two-step helper, `%` format, f-string, list append, `dirname` then `relpath`) are still uncaught, which the corrected records now state rather than deny. `abspath`'s exclusion is measured right |
| 2 | Round 1's finding 2 — the separator set built without `altsep` | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:305-307` | answered | Verified closed. Executed: `seps = tuple(s for s in (flavour.sep,) if s)` → 1 failed, 42 passed, on the new assertion, `assert 'C:/proj/seal/ledger.md' == 'seal/ledger.md'`. Dies at the named boundary, not incidentally |
| 3 | Round 1's finding 3 — the drive comparison unpinned in both directions | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:343-345` | answered | Verified closed. Executed: `root_drive.lower() != path_drive.lower()` → 1 failed, 42 passed, on the new assertion, `assert 'seal\\ledger.md' == 'C:\\proj\\seal\\ledger.md'` |
| 4 | Round 1's finding 5 — the fix pass's first reproduction was unfaithful | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:489` | answered | Verified. Re-derived independently rather than re-reading: the `c04977b` module imported and its own `relpath_on_a_ledger` called. It returns `[]` for all six shapes and `['main']` for the direct one, so the shipped gate did NOT accept a bare-name call and every ground of finding 1 holds |
| 5 | The record's derived rows `Contract changes = none` and `New units = none` | `seal/specs/1788686494-…/rounds/round-1.md:10-11` | answered | Verified rather than inherited. No top-level `def`, `class` or module constant added in `c04977b..5c325d8` (`bound` is nested inside `carriers`, and `round_record.py:58` counts top-level only); no signature or return arity changed. Both true, so this round had no new-unit surface |
| 6 | ⬜ `phases/phase-2.md` still says four propagation rules and lists the pre-widening four | `seal/specs/1788686494-…/phases/phase-2.md:60-68` | answered | Correction, paperwork, corrected in the closing commit. Measured: item 2 says *four propagation rules* and lists the four the code had before round 1's widening, which contradicts `carriers`' docstring at five. Not counted in `Needs a fix` — the location is under `seal/specs/`, so it owes no fix pass and no reader |
| 7 | ⬜ `changelog.md`'s replacement list names two movements the rules do not model | `seal/specs/1788686494-…/changelog.md:23-27` | answered | Correction, paperwork, corrected in the closing commit. Measured: `d = os.path.dirname(ledger)` then `relpath(d, root)` is an assignment and goes unreported; passing to a function the module does not define does not propagate. The sentence after it already carries the disclaimer. Not counted in `Needs a fix` — under `seal/specs/` |
| 8 | ⬜ `relpath_on_a_ledger`'s docstring announces three gates and lists two | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:494` | answered | Correction, corrected in the closing commit. Two bullets follow — **Which call** and **Which first argument**. Prose in a docstring: no behaviour and no fact changes, which is why it closes the way a record-located correction does rather than on a fix word that would commission a reader for a sentence |
| 9 | ⬜ The exclusion paragraph explains `abspath` and is silent on `realpath`, and undercounts `abspath`'s cost | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:507-510` | answered | Correction, corrected in the closing commit. Executed: adding `abspath` to the call list flags TWO lines, `file_identity:918` and `main:1677`, not the one the paragraph names; adding `realpath` flags one, `write_atomic:712`, a legitimate resolve-before-rename. Prose in a docstring, closed the same way as 8 |
| 10 | ⬜ The alias and tuple-unpack shapes hardcode the header's eight-space indentation | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:616,621` | deferred seal/follow-up.md | Not prose and not paperwork: it is a robustness change to test code, and closing it on a fix word would commission a reader for a change nothing needs today. The failure needs `main`'s header re-indented, which nothing on this branch does. Deferred with a named answerer rather than fixed in the closing commit, and named in the pull request body |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` at `5c325d8`, `uv venv` + `pytest 9.1.1` inside it | clone and the user's checkout both left clean; every `test_tmp_*` file deleted |
| `pytest` over the two changed modules in the clone | 43 passed, exit 0 |
| Mutation `seps = tuple(s for s in (flavour.sep,) if s)` over both modules | 1 failed, 42 passed — `test_a_windows_pattern_typed_with_forward_slashes_keeps_them`, on the new second assertion |
| Mutation `root_drive.lower() != path_drive.lower()` over both modules | 1 failed, 42 passed — `test_a_path_on_another_drive_keeps_its_own_spelling`, on the new second assertion |
| The `c04977b` and `5c325d8` detectors loaded as modules, `carriers()` compared over the checker source | identical function by function; both `relpath_on_a_ledger` return `[]` on the shipped source |
| Sixteen shapes put back into `main`'s header, both detectors | six go `[] → ['main']` (alias, subscript, inline wrapper, tuple unpack, bare import, `normpath`); `posixpath.relpath` and a comprehension were already caught; nine remain uncaught by both — `realpath`, `abspath`, dict value, keyword first arg, two-step helper, `%` format, f-string, list append, `dirname` then `relpath` |
| `realpath`, `abspath`, `normcase`, `resolve`, `relative_to` each added to the call list over the shipped source | `realpath` → one flag (`write_atomic:712`); `abspath` → two (`file_identity:918`, `main:1677`); `normcase` → one; `resolve` and `relative_to` → none |
| Top-level unit and signature diff over `c04977b..5c325d8` | no top-level `def`, `class` or module constant added; no signature or return arity changed |
| `./bin/evidence-check .` unscoped in the clone | 685 ok · 6 drifted · 0 broken · 0 external, exit 1 — the same six as round 1, and both re-anchored fragment rows (`@11087e2c`, `@8e0a246a`) resolve; fragments 10 ok · 0 drifted |
| Repository-wide sweep for the retired over-claims | every live occurrence is a correction narrating its own retirement; the one stale statement is `phases/phase-2.md:60` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:441`, `:405`; claims at `changelog.md:23`, `overview.md:57`, `phases/phase-2.md:98`, `tests/…:370`, `seal/ledger/1788686494-…md:10` | round 1's 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:999`; case at `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:295` | round 1's 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1002` | round 1's 3 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1131`, `:1389`, `:1514`, `:1708`, `:1741` | round 1's 4 — answered |
| round-1 | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:642` | round 1's 5 — answered |
| round-1 | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:91`, `:119`, `:687`, `:703` | round 1's 6 — answered |
| round-1 | `seal/ledger.md:121`, `:123`, `:125`, `:132`, `:133`, `:135`, `:149`, `:161`, `:162`, `:169`, `:170`, `:296`, `:381` | round 1's 7 — answered |
| round-1 | `.github/workflows/test.yml:37`; `skills/evidence-check/scripts/evidence_check.py:959` | round 1's 8 — answered |
| round-1 | `skills/evidence-check/SKILL.md:186` | round 1's 9 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:999-1031` | round 1's 10 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 10 — the alias and tuple-unpack shapes hardcode `main`'s eight-space header indentation | `seal/follow-up.md` | whoever next re-indents or moves `main`'s per-ledger header, which is when it bites |
| Four rows in `seal/ledger.md` left DRIFTED, plus the two from the base (`templates/config.md#"# Repository config"`, `round_record.py#swallowed`) | round 1's Deferred rows, unchanged by this range | the orchestrator or the release step, by `--reverify` with every branch in flight in view |
| The full suite, repository-wide lint and typecheck | `agent-contract` §2 | the orchestrator, once — and this report leaves nothing open, so the broad gate is the next step |
