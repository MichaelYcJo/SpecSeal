# Feature Specification: the broad gate re-runs the test command at the base

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Two defects found at #743's first seal (2026-10-03), one work item because
both are about what a seal's verdict can be trusted to say:

- **#747** — `broad-gate`'s base comparison re-runs the failing test files
  with the row's FIRST `&&`-segment. This repository's row is
  `uvx ruff check . && uvx ruff format --check . && bin/test -q`, so the base
  re-run is ruff, no `FAILED` line can appear, and every failing file reads
  `new` whatever the base does. The word reads as measured and is not.
- **#748** — `tests/test_the_commit_gate_decides_at_the_commit.py::test_a_row_that_does_not_end_is_named_and_leaves_nothing_behind`
  sleeps a fixed 0.5 s after the bound and asserts the loop's marker is gone;
  on a loaded machine it fails with nothing wrong.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The fix measures; it does not add a config row or a question. A design that asks the row's author which segment is the runner (a new `config.md` row) is rejected on this ground — see `plan.md` Alternatives |
| `templates/config.md` §*Broad gate* §*What is refused, and what stays allowed* | The universe of row shapes the gate accepts: any one-line shell command except three refused forms (whole-line backticks, whole-line `$(…)`, trailing `&`). "Stays legal": `$(…)` inside a line, `;`, `\|\|`, quotes, redirection, variables, globs, an escaped pipe, a non-trailing `&`. The enumeration below is over exactly this set, under both shells the same section names (`/bin/sh`; `cmd.exe` where `%COMSPEC%` names it) |
| `templates/config.md` §*Broad gate* §*Choosing a value — the criterion*, rule 3 | Says *the suite runner comes first* because the gate re-runs the row's first command. **This work rewrites rule 3** — its *Why* stops being true. The section calls itself the rules' one home, so the rewrite happens there and nowhere else restates it |
| `templates/config.md` §*Broad gate*, the example row (line 187 at e141980a) | Already lint-first and so already contradicting rule 3 in the same section. It stays; after the rewrite it is consistent |
| `seal/config.md` `Broad gate` row; commit `7a39f2f7` (#634) | The owner reordered this repository's row lint-first on 2026-09-28 so a lint refusal stops costing a suite run. That decision stands; this work does not reorder the row |
| `skills/verify/scripts/broad_gate.py` module docstring (§*On a failing test the comparison against the base is reactive and mechanical*) and `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare against the base* | The comparison's own promise — "measured, never inferred" (`compare_at_base` docstring). The fix keeps the promise by refusing to give `new` or `failing on base too` from any run that did not measure it |
| `agents/sealer.md` §*Boundaries* ("`new` and `failing on base too` are the gate's words"), `agents/smith.md` (the three-returns paragraph), `README.md` and `README.ko.md` (sealer row, chain diagram) | Every place that tells a reader what the words mean. A third word, `new?`, already exists (`new? the base could not be checked out for comparison`) and none of them names it; this work makes it reachable from a second cause, so they name it |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A case seen red, a stated failure direction, a prompt budget (zero), platform honesty (`cmd.exe` grammar driven from any machine, as `quote` and `handed_to_shell` already are) |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Enumerate the class; pin the new text in the same commit; see each new case red |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from` | `seal/releases/0.10.0.md` row S5 cites `broad_gate.py#compare_at_base`, `#first_command`, `#failing_files` and says "What it re-runs is what stands before the row's first `&&`". That claim becomes false; its re-read and correction go in this work item's fragment, never into the released file |

## Scope

### In

**#747 — the base re-run runs the part of the row that ran the tests, and
says so when it cannot find one.**

1. **The runner is found by measurement, not by name or position.** The row
   is cut into its top-level parts (below). For k = 1, 2, … the gate runs, in
   the scratch worktree at the base, **the row up to and including part k,
   with the failing files the base carries appended to part k**, and stops at
   the first such prefix whose output carries pytest's summary line —
   `suite_counts(text)` is not `None`, the same reading `NO_SUMMARY` already
   rests on. That prefix's run is the measurement. A prefix keeps every
   earlier part (a `cd`, an `export`, a `source`, a lint), so the runner runs
   in the context the row gave it; the cost is that earlier parts run once per
   prefix tried (named under *Operational impact* in `plan.md`).
2. **Where no prefix prints a pytest summary, every present file reads
   `new?` with a reason that says the comparison was not measured** — never
   `new`. This is #747's second checkbox.
3. **A word is given only from a run that measured it.** In the identified
   run's output:
   - `failing on base too` — a pytest short-summary line `FAILED <file>::…`
     **or `ERROR <file>`/`ERROR <file>::…`** names the file. (A file the base
     cannot collect fails at the base. Decided here; `questions.md` Q1.)
   - `new` — the summary is there, no such line names the file, AND the
     output carries neither pytest's collection-interrupt banner nor its
     maxfail banner. Either banner means not every collected test ran, so an
     unnamed file was not shown passing — round 1's 🟡 4 of 0.10.0 in a new
     shape: one file's collection error costing every other file its
     measurement.
   - `new?` with the reason — otherwise.
   The exact banner texts are a measurement against the pinned pytest
   (`questions.md` Q3), not a recollection.
4. **The cut, enumerated by construction** (the class the prompt asked for).
   Every row the gate accepts is a one-line string the shell reads as a list
   of commands joined by operators. The cut points are the **top-level
   operators** of the grammar of the shell the row is handed to — the same
   shell decision `handed_to_shell` makes:
   - `/bin/sh`: `&&`, `||`, `;`, `|`, `&`.
   - `cmd.exe`: `&&`, `||`, `&`, `|` (the separators
     `command_names_backslashed`'s docstring already models; `;` is not a
     separator there).

   "Top-level" means outside: single quotes (POSIX), double quotes (both),
   a backslash escape (POSIX) or `^` escape (`cmd.exe`), a backtick pair
   (POSIX), a `$(…)` (POSIX, nested), and a `( … )` group (both). In both
   grammars an `&` written straight after `>` or `<` (`2>&1`, `>&2`, `<&0`)
   is a redirection, not a cut. A prefix is a **contiguous substring of the
   row as written** — no tokenise-and-re-render, for the reason
   `command_names_backslashed`'s docstring gives — with trailing blanks
   dropped, and it goes through `run(..., shell=True)` like every other shell
   string, so `cmd.exe` still gets its rewrite.

   Every accepted shape falls in exactly one of three outcomes, and **no
   outcome gives a word a run did not measure**, because a word comes only
   from a prefix whose output carries pytest's summary:

   | Shape (the "stays legal" list, plus `&&`) | Outcome |
   |---|---|
   | one command; parts joined by `&&`, `\|\|`, `;`, `&`; a pipeline (`runner \| tee x`) — the runner is cut before the `\|`; `$(…)`, backticks, quotes, variables, globs, redirection inside a part | **measured** where some prefix prints a pytest summary at the base |
   | the runner inside a `( … )` group, or a `{ …; }` brace group (`{`/`}` are not modelled, so the cut falls inside it) | **not measured** (`new?`): the prefix is not valid shell or runs no pytest. Named here, not repaired |
   | an earlier part fails at the base and `&&` stops the prefix before the runner; or the runner's output goes to a file (`> out.txt`); or the runner is not pytest | **not measured** (`new?`) |

   A wrong cut can only cost a measurement, never fake one. That is the
   property the cases hold, rather than a promise that the scanner models
   every shell.
5. **What a person sees changes, and is documented and pinned in the same
   commit (§14):** `templates/config.md` rule 3; the module docstring of
   `broad_gate.py`; the comment above `not_as_written` in `gate` that names
   `compare_at_base → first_command`; `skills/verify/SKILL.md` §*The broad
   gate* (the two-word list gains `new?`); `agents/sealer.md`;
   `agents/smith.md`; `README.md` and `README.ko.md` (the sealer row and the
   chain diagram). The fixture comment in
   `tests/test_the_seal_is_taken_once_by_the_sealer.py#config` ("The suite
   runner first, so the base comparison can re-run it") is corrected too.
6. **`first_command` is removed.** Nothing else calls it (grep, read at
   e141980a: its only caller is `compare_at_base`).

**#748 — the row-bound case waits for the condition it needs.**

7. After the bound, the case polls rather than sleeping once: in each window
   it unlinks the marker, waits **1.0 s** (ten of the loop's 0.1 s periods),
   and passes the first time the marker is still absent at the window's end;
   it fails when **5 s** after the bound have passed with the marker
   reappearing in every window. Re-unlinking each window is what makes a
   `touch` already in flight when the group was killed harmless: it can
   recreate the marker once, never twice.
8. **The arithmetic that keeps it red with the group kill removed.** The loop
   is `seq 1 100` × `sleep 0.1`, so an orphaned loop lives at least 10 s from
   its start; the bound is 1 s and the deadline 5 s after it, so a loop the
   kill missed is still touching when the deadline falls — and under load it
   runs slower, which only lengthens its life. The `< 8 s` assertion on the
   bound itself is unchanged. The loop's length is unchanged, so the
   docstring's Windows sentence ("gone ten seconds later") stays true.

### Out, and why

| Left out | Why | Who answers |
|---|---|---|
| A failing file the BRANCH reports only as `ERROR` (collection or setup error, no `FAILED` line) gets no base comparison at all | `failing_files` decides which files are asked about, and this work is about whether the answer is measured. No false word is printed for such a file — it is an absence, not a counterfeit | the repository owner — whether to file it; recorded by the smith in `overview.md` §*Not done* |
| Modelling `{ …; }` brace groups and running a runner inside `( … )` | Outcome is `new?`, which is honest; modelling a group's interior needs the shell parser `templates/config.md` §*What is refused* says the gate avoids | nobody needs to — the outcome table above is the record |
| Reordering this repository's `Broad gate` row runner-first | The owner chose lint-first in #634; after this work both orders measure | the repository owner, already answered |
| A config row naming the runner | A question added to every repository for something measurement answers (`CLAUDE.md` goal) | decided here; `plan.md` Alternatives |
| `skills/verify/SKILL.md` §*The broad gate*'s "`git stash`, that one file, `git stash pop`" sentence | Describes the manual baseline, not the gate; unrelated to which command the gate runs | nobody — not a defect this work found |
| The other fixed sleeps in the suite | Enumerated (grep `sleep(` over `tests/*.py`, read at e141980a): every other one is a child process's body (`time.sleep(30)`) or the step of a loop already bounded by a deadline (`gone_within`, the pid-file wait in `test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`). #748's is the only fixed sleep followed by an assertion about an asynchronous effect | — |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | A lint-first row and a failure the base shares | Given a row `<lint stand-in> && <format stand-in> && <python -m pytest …>` whose two stand-ins print a linter-like line and exit 0, and a test file failing at both base and branch; when `broad-gate` runs; then that file reads `failing on base too` | executed — case in `tests/test_the_seal_is_taken_once_by_the_sealer.py` beside the S2 cases; **seen red against e141980a**, where it reads `new` (§15) |
| A2 | A lint-first row and a failure the branch introduced | As A1, the base passes the file; then it reads exactly `new` — not `new?` | executed — assert the word followed by end of line. The existing `{gate.NEW}\b` regexes match `new?` too and cannot tell them apart; tighten them in the cases this work touches |
| A3 | A runner-first row is unchanged | The fixture's `SUITE_ROW`; the existing S2 cases (`…is_new_when_the_base_passes`, `…labelled_failing_on_base_too`, `…base_lacks_does_not_cost_the_others_their_verdict`) pass unchanged, and only one base run is kept (prefix 1) | executed — those three cases |
| A4 | No part of the row runs pytest | Given a row that is a script printing a `FAILED tests/x.py::t - …` line with no clock'd summary and exiting 1; then each present file reads `new?` with a reason containing `not measured`, and no `new`/`failing on base too` is printed for it | executed — case; red against e141980a (reads `new`) |
| A5 | An earlier part fails at the base | Given a lint-first row whose lint stand-in fails at the base only; then the failing files read `new?` — the prefix stopped before the runner | executed — case |
| A6 | The base run is interrupted | Given two failing files where the base fails to collect one of them; then that one reads `failing on base too` (its `ERROR` line) and the other reads `new?`, not `new` | executed — case; banner texts from Q3 |
| A7 | The cut, over every accepted shape, in both grammars | A parametrised unit over the outcome table: operators inside quotes, `$(…)`, backticks, `( … )`, an escaped `^&`, and `2>&1` are not cut; each top-level operator is; a pipeline is cut before `\|`; the `cmd.exe` grammar is driven from any machine | executed — new unit cases; each mutation of the scanner's quote/depth handling turns one red |
| A8 | Still one shell site | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite` stays green: every prefix runs through `run(...)` called **directly from `compare_at_base`** | executed — that case |
| A9 | The words are documented where they are read | Every file in Scope item 5 names `new?` / states the new rule 3, and a case pins the new rule-3 sentence and the `new?` reason text | executed — the pinning case; read — the prose |
| B1 | #748 passes under load and is red without the group kill | The case polls per Scope item 7; it passes three runs out of three alone; with `os.killpg(proc.pid, signal.SIGKILL)` in `_run_bounded` replaced by `proc.kill()`, it fails with `the row's loop outlived the bound` | executed — the case alone ×3, and the mutation run once, reverted, and said so in the hand-back (§15) |

## Data & interfaces

- `compare_at_base(root, base, command, files, keep)` — signature and return
  shape (`{file: word}`) unchanged; it is still the one caller beside `gate`
  that hands `run` a shell string.
- The cut is a pure function of `(command, the shell's grammar)` returning
  the prefixes (or their end offsets); the grammar is chosen by the same
  `windows`/`comspec` decision `handed_to_shell` makes, factored so both read
  one answer and a case can drive either branch from either machine.
- The base-side reading (`FAILED` or `ERROR` naming a file; the two banners)
  is separate from `failing_files`, whose branch-side behaviour is unchanged.
- Kept outputs: one file per prefix tried, `suite-at-base-<k>.txt`, so a
  `new?` reader can open what was tried.
- New I/O names `encoding="utf-8"` (the #741 sibling lands first and checks
  every file I/O call).
- Ledger: rows for the new units in `seal/ledger/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base.md`;
  the re-read of `seal/releases/0.10.0.md` row S5 through
  `evidence-check --reverify --into <that fragment>`, with the false sentence
  corrected there.

## Open questions → questions.md

`questions.md` beside this file: the judgments this frame made that a person
may overturn, a measurement row, and a row for the work.

Framed 2026-10-04 by framer, before the build.
