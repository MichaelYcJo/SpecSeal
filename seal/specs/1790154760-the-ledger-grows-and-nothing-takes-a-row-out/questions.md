# 1790154760-the-ledger-grows-and-nothing-takes-a-row-out — questions for the planner

<!-- seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/questions.md -->

**Decided from the tree while framing, so nobody reopens them.** Each has its
grounds in `spec.md` §Measurements or `plan.md` §Alternatives.

- *Is the size a cost now or later?* Now. Every `git commit` pays 15.7 s in
  the PostToolUse advisor, and the check runs in CI and in the broad gate.
- *Is it the row count that costs?* No. It is one parse per row instead of
  one per file (1,328 parses of 126 files). A memo gives 1.81 s with
  identical findings.
- *Is any row dead?* No. All 1,468 anchors resolve and none drifted. No rule
  lets a row leave except with its code.
- *Do the release sections repeat `docs/`?* Mostly not. The median Clause
  word overlap with the folded prose is 0.21, and 71 % of a row's bytes are
  evidence cells no policy sentence carries.
- *Split by release into `seal/ledger/`?* No. That glob means "unshipped",
  and a split saves no time.
- *Conflict frequency?* Four hand-resolved merges in the history, all on
  2026-09-22 against the 0.13.1 release branch, each 1–3 hunks. They come
  from in-place corrections and removals, which size does not drive.

Nothing below blocks the build. No row needs a person before phase 1.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does this work close #519, or does #519 stay open for a row-retirement design? | a person | **close** — the PR says `Closes #519` and states that the measurement chose the checker, not the rows · **keep open** — the PR says `Refs #519`, and the issue waits for a retirement rule argued on some other ground (for example, reading cost) | close. The issue listed "Nothing, if the measurement says the size costs nothing" as a candidate, and after the memo the size costs 1.8 s. The build is identical either way; only the PR's closing keyword differs. Why the tree cannot answer it: whether the owner wants a retirement rule anyway is a product call, not a fact | ⬜ |
| Q2 | Does any caller mutate the dict or lists `py_spans` returns, so that a shared cached object needs copying or freezing? | the work | **none mutates** — return the cached object · **some do** — return a copy, or freeze to tuples and adjust the one caller | read the three callers (`resolve_unit`, `file_units`, `rider_check.py`) in phase 1. Framing read `resolve_unit`'s use (`spans.get(locator, [])`, then reassignment only) and found no mutation, but did not read the others to the end. Why framing did not close it: it is a code read the builder does anyway at the same site | ✅ none mutates, read 2026-09-23 in phase 1 (`check_text`, `reverify`, `file_units`, `rider_check.py#region_lines` and `#inferred_anchor` all rebind or read). The build copies anyway, and a case pins it (`phases/phase-1.md`) |
| Q3 | What is the advisor's cost after the memo, on this tree, for the docstring sentence? | a measurement | one timing, as in `spec.md` §2 | the number phase 1 records. The framing probe measured 1.81 s for the ledger arm alone; the advisor adds its own import | ✅ measured 2026-09-23: 1.73 / 1.74 / 1.77 s per commit on this tree, `/usr/bin/time -p`, down from 15.16–15.44 s. The advisor's docstring states it (`9374d402`) |
| Q4 | What does the remaining ~1.8 s go to? | a measurement | one `cProfile` run after the memo | recorded in phase 1's record, and it goes no further in this work (`spec.md` §Scope, out). Why framing did not close it: the profile is only meaningful after the change | ✅ measured 2026-09-23 with `cProfile`: the 126 remaining parses (`compile` 0.33 s, the walk 0.30 s internal) and `str.splitlines` per row (0.29 s), of 2.63 s under the profiler (`phases/phase-1.md`) |
