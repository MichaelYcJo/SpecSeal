# Implementation Plan: the broad gate re-runs the test command at the base

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

#748 first, because it is one test and stands alone. Then #747 in three
slices: the cut (a pure scanner with its own cases), the comparison that
tries prefixes and reads the base run strictly, and the documents that name
the words. `spec.md` holds the WHAT and the acceptance; this file holds the
order and the choices.

## Technical context

Coordinates are read at e141980a (the branch is cut from it, plus the routing
commit d617e78f).

- `skills/verify/scripts/broad_gate.py#first_command` (line 1820) —
  `command.split("&&", 1)[0].strip()`: a raw split that ignores quotes and
  knows one operator. Removed by this work.
- `skills/verify/scripts/broad_gate.py#compare_at_base` (1826–1900) — the
  scratch worktree, the `absent` split (keep it as it is), the one
  `run("suite-at-base", runner, scratch, keep, shell=True)` call, and
  `failing_files(check.text)` read off it. The prefix loop goes here, and
  **its `run(...)` call stays in this function's own body**:
  `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  asserts the callers of `run(..., shell=…)` are exactly `compare_at_base`
  and `gate`, so a helper that calls `run` turns it red.
- `skills/verify/scripts/broad_gate.py#failing_files` / `FAILED_RE` (317,
  1786) — branch-side; unchanged. The base-side reading is a separate unit.
- `skills/verify/scripts/broad_gate.py#suite_counts` (2313) — the "pytest
  ran" signal: counts followed by a wall clock. Reused as is.
- `skills/verify/scripts/broad_gate.py#handed_to_shell` (1519) — holds the
  `windows`/`comspec` → `cmd.exe`-or-not decision. Factor that decision out
  so the scanner's grammar and the rewrite read one answer.
- `skills/verify/scripts/broad_gate.py#command_names_backslashed` (1620) — the
  existing `cmd.exe` position scan: the model of `"`, `^`, `&&`/`||`/`&`/`|`
  and `(` to copy for the `cmd.exe` grammar. Its docstring's "a position scan
  over the string, never a tokenise-and-re-render" is the rule the cut
  follows too.
- `skills/verify/scripts/broad_gate.py#gate`, the comment above
  `not_as_written(home, command)` (≈2848) — names `compare_at_base →
  first_command` and argues a refusal there closes it by reachability. Every
  prefix is a substring of a row that already passed the refusal, so the
  argument still holds; reword the comment to say so.
- `NEW, ON_BASE` (258) and the existing `f"{NEW}? the base could not be
  checked out for comparison"` (1848) — the `new?` shape already exists.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py#build_repo`,
  `#config`, `SUITE_ROW` (≈748–800) — the fixture the end-to-end cases build
  on; `set_row` replaces the row.
- `tests/test_the_commit_gate_decides_at_the_commit.py#_run_bounded` (334) and
  `#test_a_row_that_does_not_end_is_named_and_leaves_nothing_behind` (416).
- Precedent for a poll with a deadline in this suite:
  `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py#gone_within`.

**What breaks in six months.** A pytest release that rewords the
collection-interrupt or maxfail banner makes an interrupted base run read as
complete, and an unnamed file then reads `new` where it should read `new?` —
the failure #747 is about, by a different road. The case for A6 is what
catches it, which is why the banners are matched against what the installed
pytest prints (Q3) rather than typed from memory. Second: a row author who
puts the runner in a `( … )` group gets `new?` on every failure; the outcome
table in `spec.md` and rule 3's rewrite are where they learn why.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Try each prefix of the row at the base, take the first whose output carries pytest's summary** | Earlier parts are re-run per prefix (quadratic in parts before the runner; this repository's row runs ruff 3 times — seconds). A runner inside a group is not found → `new?` | **Chosen.** Measures; a wrong cut costs a measurement and never fakes one; no question to anyone |
| B. Try each part ALONE (not a prefix) | `export PYTHONPATH=src && pytest`: the part alone loses the export, the base cannot import, every file `ERROR`s and reads `failing on base too` — a measured-looking word that is false, in the lenient direction | Rejected: fakes a word, which is the defect being fixed |
| C. Pick the part whose command name looks like a test runner (`pytest`, `tox`, `bin/test`…) | `bin/test` names no runner; a list of names is the enumeration-by-example the prompt forbids, and it rots | Rejected |
| D. A new `config.md` row naming the base runner | A question added to every repository for something a run can answer; a wrong value is silent | Rejected on `CLAUDE.md`'s first goal |
| E. Run the WHOLE row at the base with the files in `PYTEST_ADDOPTS` | The variable is inherited by every pytest the suite starts — this repository's own sealer cases run pytest in fixture repositories — so the base run's results are polluted; and the whole row (lint, typecheck) runs at the base | Rejected |
| F. Reorder this repository's row runner-first and change nothing else | Every repository whose row is lint-first still gets `new` on every failure; the owner's #634 reason is undone | Rejected; not even as a companion change |
| G. Split with `hooks/cmdline.py#split_segments_with_separators` | It returns de-quoted tokens; re-rendering them loses `$VAR`, quoting and `cmd.exe` semantics, and it models POSIX only | Rejected; the cut keeps the row's own substrings |
| H (#748). Poll the loop shell's PID until gone, as `gone_within` does | Needs the loop to write its PID; a shell slow to start under load has written none when the bound falls, which is a new load-sensitive branch | Rejected for the marker poll in `spec.md` Scope 7, which needs nothing from the loop |
| I (#748). Keep one fixed sleep and raise it to several seconds | Still a guess about load; a `touch` in flight at the kill still recreates the marker after the one unlink | Rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #748: the row-bound case polls per `spec.md` Scope 7–8 (B1) | the case alone, three runs; the group-kill mutation run once and seen red, then reverted | |
| 2 | #747, the cut: a pure scanner returning the prefixes of a row for a grammar, the shell decision factored out of `handed_to_shell`, and parametrised cases over `spec.md`'s outcome table in both grammars (A7) | the new unit cases, plus `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` (the factored decision is read there) | |
| 3 | #747, the comparison: `compare_at_base` tries prefixes, keeps `suite-at-base-<k>.txt`, reads `FAILED`/`ERROR` and the two banners at the base, gives `new?` with a reason where nothing measured; `first_command` removed; end-to-end cases A1, A2, A4, A5, A6, each seen red against e141980a where the spec says so; the S2 cases' `new\b` assertions tightened where touched (A2, A3, A8) | those cases by `-k`, the three existing S2 cases, and the one-shell-site case | |
| 4 | The documents and the record: `spec.md` Scope 5's eight files, a case pinning the rule-3 sentence and the `new?` reason; `changelog.md` fragment; ledger fragment rows for the new units and the re-read of `seal/releases/0.10.0.md` S5 (A9) | the pinning case; the text-reading hygiene modules over the touched files (`tests/test_one_word_one_meaning.py`, `tests/test_no_real_identifiers.py`); `evidence-check` over the fragment | |

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.** What a phase discovers that the next
needs goes in `phases/phase-N.md`, from `templates/sdd-phase.md`.

## Operational impact

- **Cost on the failure path only.** Nothing changes when the suite passes.
  When it fails, a lint-first row now re-runs its earlier parts once per
  prefix tried before the runner is found: for this repository, `uvx ruff
  check .` three times and `uvx ruff format --check .` twice, in the scratch
  worktree. A runner-first row costs exactly what it did (one run).
- **Failure direction.** The change moves verdicts from `new` toward `new?`
  and `failing on base too`. `new?` blocks nothing new — the gate already
  exits 1 on any failing check, and the word is a reading for the person,
  not a gate input. `failing on base too` is now given for a file the base
  cannot collect: that is the lenient direction, and it is given only from a
  run whose output names the file.
- **Prompt budget: zero.** No question, no config row.
- **Platform honesty.** The `cmd.exe` grammar is driven from any machine as a
  pure function. The end-to-end cases run on whatever CI runs, which includes
  `windows-latest`; #748's assertion is POSIX-only, as it is now.
- No migration, no new dependency, no new environment variable.
