# Implementation Plan: the ledger grows, and what its size actually costs (#519)

<!-- seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/plan.md -->

Approved 2026-09-23 by the orchestrating session, under the owner's `automation` preset, when `smith` was spawned.

## Summary

The checker re-parses a Python file once for every row that cites it: 1,328
parses of 126 files, about 94 % of a 15.8 s run. Every `git commit` in this
repository pays that run through the PostToolUse advisor. Parse each file
once per process, and correct the advisor's "about 114 ms" to a measured
number with its instrument. Leave the ledger's rows as they are, because
nothing measured gives one a reason to leave (`spec.md` §Measurements).

## Technical context

- `skills/evidence-check/scripts/evidence_check.py#py_spans` — `ast.parse`
  plus a recursive walk, returns `{name: [(start, end)]}` or `None`.
- `skills/evidence-check/scripts/evidence_check.py#resolve_unit` calls it once
  per row (`spans = py_spans(text)`, then `spans.get(locator, [])`).
- `skills/evidence-check/scripts/evidence_check.py#file_units` calls it in the
  repo-wide scan, and `.github/scripts/rider_check.py` calls
  `checker.py_spans(text)`. A memo inside `py_spans` serves all three.
- `skills/evidence-check/scripts/evidence_check.py#check_text` dedupes on
  `(coord, hash)`, not per file, which is why 1,468 unique anchors meant
  1,328 parses.
- `hooks/evidence-advisor.py#failing_rows` imports the checker fresh at each
  commit (`exec_module`), so a module-level memo lives exactly one commit.
- Callers that pay the whole run: the advisor, the `ledger` job in
  `.github/workflows/test.yml`, and `skills/verify/scripts/broad_gate.py`
  (`LEDGER`, `--strict`).
- The framing probe memoised by the exact text and returned a deep copy:
  1.81 s, identical findings. Whether the copy is needed (does any caller
  mutate the returned lists?) is for phase 1 to settle by reading, per
  `questions.md` Q2.

**Failure scenario of the chosen approach, six months out.** The memo is
keyed on file text, so a stale answer needs a hash collision on a Python
`str` key, which a dict does not have. The two ways it can go wrong are
memory, because every distinct text is held for the process lifetime, and a
caller mutating a shared list. The first is bounded by the files the ledger
cites (126 today, a few MB). A long-lived process could grow it, and no such
caller exists; the advisor re-imports per commit. The second is closed by
returning something a caller cannot mutate into the cache, or by the read
in phase 1. What stays linear after this is the per-row work other than
parsing: 1.8 s today, projected 4.6 s at four times the rows. Past that, the
next lever is the residual profile phase 1 records, not the ledger's rows.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Memoise `py_spans` on the file's text** | Memory held for the process; a caller mutating a shared list (closed by phase 1's read or an immutable return) | **Chosen.** 8.4× on today's ledger, identical findings, and it scales with distinct files, not rows |
| Memoise on path (or `(path, mtime)`) | A path read twice with different content in one process, which `--reverify` and tests with `tmp_path` fixtures do, serves stale spans. It is a silent wrong answer, which is the failure the checker exists to prevent | Rejected |
| Group anchors by file in `check_text` and resolve per file | Restructures the one function that carries eight rounds of tie-breaking logic (`check_text`'s comments), for the same saving the memo gives from outside it | Rejected: the saving is equal and the risk is not |
| Ledger `settle`: compress rows whose work item is folded into `docs/` to the anchor alone | All 642 work-item rows qualify by marker, but the median Clause word overlap with the folded prose is 0.21. The compression would drop the evidence (71 % of the bytes) and keep almost nothing `docs/` holds. It also needs a retirement rule `CLAUDE.md` does not have | Rejected on the measurement |
| Split release sections into `seal/ledger/<release>.md` | `seal/ledger/*.md` means "unshipped work item" (`docs/the-evidence-ledger.md`); the checker reads every file anyway, so no time is saved; conflicts come from in-place edits, which a split does not remove | Rejected |
| Change nothing | Every commit keeps paying 15.7 s, rising linearly with every fold: 2.3× in sixteen days by the issue's table | Rejected: the cost is now, and a one-function change removes most of it |
| Move the advisor off the commit path (async, or only on `.py` changes) | Changes when a person hears about a broken anchor, which is the advisor's stated purpose, to save what the memo already saves | Rejected for this work; the memo makes it unnecessary |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `py_spans` parses each distinct text once per process, and a case in `tests/test_a_row_points_by_content.py` (the file that already holds the `py_spans` and advisor cases) pins one parse for N rows citing one file. It is shown red against the current code. The phase record carries: before/after wall time of `evidence_check.py --strict .` and of the advisor on a commit payload, the byte diff of the full checker output before/after (empty), and the residual profile's top three functions | the new case, red then green; `tests/test_evidence_check.py` and `tests/test_a_row_points_by_content.py` as the slice; `diff` of the two outputs; `; echo $?` read directly | |
| 2 | `hooks/evidence-advisor.py`'s docstring states the measured cost with instrument and date. The changelog fragment `seal/specs/1790154760-…/changelog.md`, the ledger fragment `seal/ledger/1790154760-the-ledger-grows-and-nothing-takes-a-row-out.md` with the new claims, and the drifted shared rows re-read and `--reverify`d (`evidence_check.py#py_spans`, plus any unit phase 1 changed). The overview names the measurement that answers #519's three questions | `evidence_check.py --strict .` exit 0 read directly; `tests/test_a_row_points_by_content.py`, `tests/test_dispatch.py` and `tests/test_local_mode_resolves_under_the_git_dir.py` (the advisor's cases) as the slice | |

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.**

## Operational impact

None to deploy: no migration, no new env var, no new dependency. What a
person notices is that a `git commit` in an opted-in repository with a large
ledger stops hanging for about fifteen seconds after it returns. The
`flow-measurement` issue and #51 (performance baselines) are where the
before/after numbers would be useful. Posting them is the orchestrator's act,
not the build's.
