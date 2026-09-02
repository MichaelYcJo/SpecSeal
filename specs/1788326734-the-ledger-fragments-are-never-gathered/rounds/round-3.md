# 1788326734-the-ledger-fragments-are-never-gathered — review round 3

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered/rounds/round-3.md —
the verifying round for round 2's fixes (target: the diff e2e01e0..ec3ffc1).
It opened nothing needing a fix, so the run ends here and this round does not
consume the cap. Written by the review orchestrator after opening the
coordinates. -->

| Field | Value |
|---|---|
| Target SHA | ec3ffc1 (the fix diff from e2e01e0); HEAD 66394fe at review time, record-only commits after it |
| PR | none yet |
| Broad gate | 7302852 against `origin/release/v0.4.0` (16c16c7): `pytest tests/ -q -n auto` 1243 passed · 1 skipped; `ruff check .` clean; `ruff format --check .` 75 files formatted; `evidence_check.py --strict .` 160 ok · 0 drifted · 0 broken; `unverified_check.py --baseline` 26 open · 12 closed · 0 unreadable |
| Fixes checked by | no fixes to check |
| Contract changes | none — 🟡 1 was answered in text: `demote`'s docstring and a rider, no signature or returns moved |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

Round 2's verdicts first, each answered on this round's grounds; then what this round opened.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r2 🔴 1 | the after-fold self-check copied `ROOT` and failed with `nothing to fold` on a folded tree | `tests/…fold_at_release.py:706-725` | fixed | reviewer executed: a `git archive` copy of HEAD folded with `--version 9.9.9` (7 fragments), then the fold test file on that copy → 43 passed; mutating `section` to write the marker on the `### <id>` line reddens the test at `:692`, so the else branch (fragment gone, marker present) is the one exercised after the fold |
| r2 🟡 2 | the same test's `specs/` copy made any open evidence-todo row fail it | same test | fixed | reviewer read: the test opens nothing under `ROOT`; the `tree` fixture's evidence-todo is `drained` |
| r2 🟡 3 | fragment row 14 said the backslash test fails on every leg | `.specseal/map/1788326734-…md:14` | fixed | reviewer read the rewritten cell against `test.yml:35-37`'s three-leg matrix |
| r2 🟡 4 | `demote`: whitespace-only first line before the title; `~~~` fences | `.github/scripts/fold_ledger.py#demote` | fixed | reviewer executed: HEAD's tests against the script at e2e01e0 → exactly the new tilde test red; probes for ``` inside `~~~` and the reverse, two blank lines above the title, a title-only fragment |
| r2 🟢 5 | fragment row 13 says "quoted inline" | `.specseal/map/1788326734-…md:13` | done | reviewer read; `is_marked` unchanged in this diff |
| r2 Contract changes | `demote` → `section` | `.github/scripts/fold_ledger.py#section` | pass | reviewer read the one call site |
| 🟡 1 | the fence-closing rule is looser than the docstring's "the way CommonMark reads them": a ```` ```python ```` line, or a ``` line inside a four-backtick block, closes the fence, so a `#` line after one is demoted where CommonMark copies it | `.github/scripts/fold_ledger.py:161-162` (before the rider) | answered — the docstring now states the actual rule, a `# RIDER:` at the closing line carries the CommonMark reading to apply if a fragment ever quotes a fenced block, and fragment row 12 says the same; no fragment and not `map.md` holds a fence line today (reviewer's grep 0 · 0), so a fold of this ledger is untouched | orchestrator at 7302852; the reviewer executed the paste-ready patch on a copy (43 passed, probes A–G CommonMark-consistent) and it is quoted in the rider for whoever next opens the line |
| 🟢 2 | an indented fence and an unclosed fence read as fences; bytes unchanged, only heading demotion suppressed | `.github/scripts/fold_ledger.py:158` | pass | reviewer executed |
| 🟢 3 | the two new tests: four assertions in the tilde test each catch a distinct wrong implementation; the after-fold test drives both branches of the shared body | `tests/…fold_at_release.py:363-381, 706-725` | pass | reviewer executed the mutation and the old-script run |
| 🟢 4 | fragment rows 12–14 against the code; `--strict` 160 ok | `.specseal/map/1788326734-…md:12-14` | pass | reviewer executed; the orchestrator re-verified row 12's hash after the docstring change (`a37e8a24 → 3ecaecde`) |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the fold test file on the real tree | 43 passed |
| reviewer: a `git archive` copy of HEAD folded with `--version 9.9.9`, then the fold test file on it | `folded 7 fragments` · 43 passed |
| reviewer: HEAD's tests against the script at e2e01e0 | 1 failed (the tilde test) / 42 passed |
| reviewer: mutation — `section` writes the marker on the `### <id>` line | 2 red, at `:692` and `:234` |
| reviewer: `demote` probes A–K (fence kinds, nesting, indentation, unclosed fence, blank lines, title-only) | as recorded; deviations F and G are 🟡 1 |
| reviewer: the paste-ready CommonMark patch applied to a copy | 43 passed · probes A–G consistent with CommonMark |
| reviewer: `evidence_check.py --strict .` | 160 ok · 0 · 0 |
| orchestrator: `evidence_check.py --reverify .` after the docstring change; fold tests + `test_a_rider_reaches_its_file.py` | 1 row re-verified; 51 passed |
| orchestrator: the broad gate at 7302852 | see the field above |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 2 | `.github/scripts/fold_ledger.py#demote` | the unit round 2's fix changed; this round opened it again and the orchestrator's answer touched its docstring |
| round 1 | `tests/…fold_at_release.py` "this repository" block | where both 🔴s of this run lived |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — CommonMark-exact fence closing | the `# RIDER:` at `.github/scripts/fold_ledger.py#demote`'s closing line, stamped 2026-09-02 at 16c16c7 | whoever next opens that line; a fragment that quotes a fenced block is the trigger |
| Whether the Windows leg is green after the slash fix | the pull request's first CI run | the repository owner reads the `windows-latest` job |
| `questions.md` Q1–Q3 | `specs/…/questions.md`, defaults taken and named in the pull request body | the repository owner |
