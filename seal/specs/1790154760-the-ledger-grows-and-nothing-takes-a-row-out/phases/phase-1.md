# 1790154760-the-ledger-grows-and-nothing-takes-a-row-out — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b7591519 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Memoise `skills/evidence-check/scripts/evidence_check.py#py_spans` on the
file's TEXT, never its path, so each file parses once per process, with every
finding the checker prints unchanged. Pin "N rows citing one file cost one
parse" in `tests/test_a_row_points_by_content.py`, shown red on the current
code first. Answer `questions.md` Q2 (does any caller mutate what `py_spans`
returns) by reading the callers, and return copies or immutable values if one
does. Record before/after wall time of `evidence_check.py --strict .` and of
`hooks/evidence-advisor.py` on a commit payload, the diff of the full output
before and after (must be empty), and the top three entries of the profile
of what remains.

## What this phase found

**The frame holds.** Every coordinate `plan.md` §Technical context names is
where it says: `py_spans`, its three callers (`resolve_unit`, `file_units`,
`.github/scripts/rider_check.py#inferred_anchor`), and the advisor's
per-commit `exec_module`. One thing the frame did not list: "114 ms" is
stated in two more places than the advisor's docstring,
`evidence_check.py#scan_candidates`'s docstring and the docstring of
`tests/test_a_row_points_by_content.py#test_past_the_file_cap_the_scan_degrades_and_says_so`.
Phase 2 corrects all three, because the sentence is one fact written three
times.

**Q2, answered by reading, 2026-09-23: no caller mutates.** Every consumer
of the places `resolve_unit` returns rebinds the name rather than changing
the list: `check_text` (`places = hit[:1]`, `unsure, places = places, []`),
`reverify` (`places = []`), `rider_check.py#region_lines` (reads only).
`file_units` iterates, and `inferred_anchor` iterates. The build still hands
each caller a fresh dict of fresh lists. The copy costs 0.155 s of tottime
under the profiler for 1,334 calls. What it buys is that the next caller
that does mutate cannot rewrite the answer for everyone after it, and a
case pins that. A tuple freeze of the stored value was built first and then
removed (`b7591519`): only `py_spans` calls the memo, `py_spans` already
copies, and a mutant that dropped the freeze stayed green.

**The design as built.** `py_spans(text)` keeps its signature and its
`None`-for-SyntaxError answer. It calls `parsed_spans(text)`, a
`functools.cache` over the old body, and copies the result. Exceptions other
than `SyntaxError` are not cached, as before they propagate.

**Measurements, executed 2026-09-23, Python 3.12.11, macOS, `/usr/bin/time -p`:**

| Reading | Before (`f8f1c9de` checker) | After (`b7591519`) |
|---|---|---|
| `evidence_check.py --strict .`, three runs | 16.29 / 16.52 / 16.28 s | 2.00 / 2.02 / 1.98 s |
| `hooks/evidence-advisor.py` on a `git commit` payload, clean tree, three runs | 15.16 / 15.39 / 15.44 s | 1.77 / 1.74 / 1.73 s |
| Advisor's `failing_rows` on a home with one broken anchor, in process | 16.78 s | 1.95 s |
| Every finding of every ledger, plus a perturbed copy of `seal/ledger.md` (every 7th anchor's hash altered, every 11th locator renamed), in process | 15.59 s + 180.19 s | 1.65 s + 43.47 s |
| Parses of one fixture file for five rows (the new case) | 10 | 1 |

"Before" for the first two rows was taken on the tree before the edit. The
advisor ran with its stdout empty in all six runs.

**The output is byte-identical**, measured three ways, each on the SAME tree
so that the edit's own drift of the `py_spans` row cannot stand in for a
difference:

- `evidence_check.py --strict .` run by the old checker file and the new one
  on the tree at `b7591519`: stdout identical (`cmp`), stderr identical
  (both empty), exit 2 from both (the `py_spans` row drifts until phase 2
  re-verifies it).
- The full findings dump above, 3,058 lines, with 143 BROKEN and 234 DRIFTED
  findings in the perturbed part: identical (`cmp`).
- The advisor's rows on the one-broken-anchor home: identical.

**One thing is not identical, and it is on stderr only.** When the BROKEN
path's repo-wide scan parses a file whose source raises a `SyntaxWarning`,
Python prints the warning at each parse. The old code printed it 143 times in
the perturbed run and the new code prints it once, because the file is parsed
once. The file is `tests/test_a_row_points_by_content.py`, whose
`test_an_old_format_ledger_is_loud_never_invisible` docstring holds a `` \` ``
escape. That predates this work, and fixing it is not in scope. `overview.md`
records the divergence.

**What the remaining time goes to**, `cProfile` over `--strict .` at
`b7591519`, 2.632 s under the profiler. Top three by internal time:

| Function | Calls | tottime | cumtime |
|---|---|---|---|
| `builtins.compile` (inside `ast.parse`) | 126 | 0.329 s | 0.331 s |
| `evidence_check.py#parsed_spans>walk` | 371,752 (126 primitive) | 0.303 s | 0.902 s |
| `str.splitlines` | 2,975 | 0.285 s | 0.285 s |

So the 126 parses that remain are still about half the run (`parsed_spans`
cumulative 1.270 s), and splitting each file's text once per row in
`resolve_unit` and `content_hash`'s callers is the next item. Neither is in
this work's scope (`spec.md` §Scope, out).

**The mutation check, executed.** Each new case was run against a mutant of
the unit it covers and went red; the file was restored from bytes kept
before the first mutant, and `tests/__pycache__` cleared between runs:

| Mutant | Case | Result |
|---|---|---|
| the checker as it was at `f8f1c9de` (no memo) | `test_rows_citing_one_file_cost_one_parse` | red, `10 parses of one file for five rows` |
| the memo keyed on `len(text)` | `test_a_file_edited_between_two_reads_gets_its_new_spans` | red, `{'aa': …} == {'bb': …}` |
| `py_spans` returns the stored dict | `test_changing_the_returned_spans_does_not_reach_the_next_caller` | red |
| `py_spans` copies the dict and not the lists | the same case | red |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
