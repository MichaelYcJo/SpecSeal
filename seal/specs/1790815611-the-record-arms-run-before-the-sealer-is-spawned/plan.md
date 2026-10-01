# Implementation Plan: the record arms run before the sealer is spawned

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-01 by the repository owner, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

`broad-gate` gains `--preflight`: the same command, the same resolved base, the
same row refusals, and then the record arms alone — no row, no cell, no stamp.
The orchestrator runs it before spawning the sealer and spawns only on exit 0,
so a refusal the sealer would have returned after a suite arrives in seconds
instead. The example `Broad gate` row in `templates/config.md` goes lint-first,
the order this repository's own row took in #634.

## Technical context

**The gate.** `skills/verify/scripts/broad_gate.py#gate` (line 2244 at
`cd24f516`) refuses before anything runs (root, `seal/` home, the row through
`missing_row` and `not_as_written`, HEAD, the base through `resolve_base`,
`--record` as a directory, the scale), then runs `checks[SUITE]` through
`run(..., shell=True)` and the six record arms in order, each through `run`
with its exit code read directly. Failures are collected in one loop over
`checks.items()`; a failing `suite` alone triggers `compare_at_base`. With
`--record` and every check green it calls `seal_record`; then `panel`, and
either a drawing on a terminal or `signal`, which writes the values file.
`main` (line 2524) parses with `parse_known_args` first so a tree that ships
its own gate is handed the whole argument vector, flags it alone knows
included — `tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_flag_only_the_trees_copy_knows_still_reaches_it`.

**What holds the shape.** Three structural cases read `gate()` as a syntax
tree and the preflight branch must leave them green:
`tests/test_the_gate_names_every_step_ci_runs.py#arms_the_gate_runs` collects
every `checks[<NAME>] = run(...)` assignment anywhere inside `gate()` and
holds the set against `PARTITION` from both sides;
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py#failure_loop`
finds the `for name, check in checks.items()` loop and reads its `if …:
continue` and its last `failures.append`;
`tests/test_the_gate_asks_the_range_ci_will_ask.py::test_the_gate_reads_the_given_base_exactly_once`
counts `args.base` attribute reads in the file and requires one. So: the
`checks[SUITE] = run(...)` assignment stays where it is under an `if not
args.preflight:`; the failure loop is untouched; `args.preflight` is a new
attribute and `args.base` is not read again.

**The row.** `broad_command`, `missing_row`, `not_as_written` are all reached
before the first `run`, so the preflight gets every row refusal for free by
keeping them in front of the branch. `first_command` and `compare_at_base` are
reached only from a failing `suite`, which a preflight never has.

**The verdict forms.** `seal_stamp.not_sealed(tree, base, failures)` prints
`NOT SEALED <tree> against <base>` and the failing checks;
`tests/test_the_seal_is_taken_once_by_the_sealer.py::test_not_sealed_carries_no_disc_and_names_every_failure`
and `::test_the_failure_form_lines_up_the_widest_check_name` call it
positionally. A preflight failure must carry the same per-check lines and a
different first line (spec S1, S3). Q4 of `questions.md` leaves the mechanism
to the phase: a keyword with the old default on `not_sealed`, or a form built
in `broad_gate.py` from `failure_lines`.

**The fixtures.** `build_repo`, `set_row`, `run_gate`, `settled_item`,
`generate`, `close_round` in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
build the repositories every gate case runs over; `run_gate(repo, *extra)`
passes extra flags, so `run_gate(repo, "--preflight", keep=…)` is the whole
invocation. `test_a_plugin_check_that_fails_is_named_and_the_suite_is_not_compared`
is the failing-record-arm shape S3 reuses.

**The documents.** `skills/code-review/orchestration.md` lines 524–537 hold the
spawn; the acts table in `skills/implement/orchestration.md` (line 483 on) has
a `still a sentence` row for that section whose `Grounds` cell is free text,
and `tests/test_every_orchestrator_act_names_its_delivery.py` reads the marker,
the four-value vocabulary and that a named path exists — a prose edit inside an
existing section and a grounds edit are both invisible to it; a new `###`
would need a row. `skills/verify/SKILL.md` lines 292–330 and
`tests/test_broad_gate_rule.py` pin phrases by presence, so a sentence added
beside them is safe. `templates/config.md` line 177 is the fenced example row;
`hooks/config.py#unfenced` makes a fenced row invisible to every reader, and
`tests/test_the_seal_is_taken_once_by_the_sealer.py::test_this_repositorys_own_config_is_answered_exactly_as_before`
reads this repository's own `seal/config.md`, which already reads lint-first.
`docs/release-checklist.md` lines 208–209 already list ruff before the suite.

**Failure scenario of the chosen approach, in six months.** A seventh arm
lands in `gate()` under a condition the preflight branch does not share — say
an arm added inside the `if not args.preflight:` block by mistake. The
partition cases still pass, because the assignment is inside `gate()`, and the
preflight silently runs one arm fewer than the sealer. What catches it: S1
asserts the kept output holds one file per record arm, read from the gate's
own constants rather than a typed list, so an arm the preflight skips is a
missing file in that case. Keep S1's list derived from the module (every arm
name but `SUITE`), never typed.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Reorder the gate's arms: record arms first, stop at the first refusal, the row last | The report loses its *every check that failed* property (`broad_gate.py` docstring), so a reader fixes one arm, re-runs a suite, and meets the next. The ticket rejects it for this reason | rejected |
| B. Reorder the arms but keep running all of them | The suite still runs on every refusal; nothing measured in the ticket improves | rejected |
| C. The sealer runs the record arms first itself and stops on a refusal | The spawn is already paid, the arms run twice on a green tree, and the sealer judges and fixes nothing, so every refusal still comes back to the orchestrator — one spawn later than the preflight returns it. The orchestrator has just closed the round that caused most of the measured refusals, so it is the party that can act | rejected |
| D. A separate command, `bin/preflight` | A second command needs both wrappers, a second name under the one-word rule, and a second arm list to keep true — the drift `PARTITION` was declared to end (#468). A flag on the gate runs the arms the gate declares by construction | rejected |
| E. `--preflight --record <item>` also runs `round_record.py seal`'s three record refusals as a dry run | Would catch #456's first instance (an unchecked `Pass`). Needs a `--check` on `seal`, whose contract counts its refusals by `raise` sites, and widens the ticket's stated scope (arms 2–7 only). Out of scope here; named for the owner as a possible follow-up in the report | not built |
| F. The flag on the gate, the orchestrator runs it before the spawn (chosen) | See §*Technical context*, failure scenario | chosen |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `--preflight` in `broad_gate.py`: the branch in `gate()`, the `--record` refusal, the verdict lines, the docstring and usage; cases S1, S2, S3, S4, S6 in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, each seen red first (the flag absent: argparse exit 2; the flag ignored: S2 exits 1) | the new cases; `tests/test_the_gate_names_every_step_ci_runs.py`, `tests/test_the_gate_asks_the_range_ci_will_ask.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` and the whole sealer module green (S5) | 3f4c34a6 |
| 2 | S7, the ticket's verification: a fixture item whose verifying round's record carries `fixed at` in the shape `chain_check` refuses on a draft (Q1), preflight exit 1 with `chain` named and the row not run; the wall clock measured once on the fixture and on this repository, written to `phases/phase-2.md` (Q2) | the new case in the sealer module; `tests/test_chain_check_at_the_pull_request.py` green unchanged | 4b061820 |
| 3 | The documents: the paragraph before `spawn \`sealer\`` in `skills/code-review/orchestration.md`; the `Grounds` cell and, where the order section names the spawn, the step in `skills/implement/orchestration.md`; one sentence in `skills/verify/SKILL.md`; the lint-first example row and the arms sentence in `templates/config.md`; pins S8, S9, S10 in `tests/test_broad_gate_rule.py`, seen red first against the unedited documents | the new cases; `tests/test_every_orchestrator_act_names_its_delivery.py`, `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py::test_this_repositorys_own_config_is_answered_exactly_as_before` | b0d5426f |
| 4 | The records: `seal/specs/<id>/changelog.md` (`### Added`), `seal/ledger/<id>.md` with one row per scenario the build verified, `overview.md` with the `agents/sealer.md` diff recorded empty, `phases/phase-N.md` for each closed phase | `evidence-check --strict` over the fragment; `tests/test_no_real_identifiers.py`; `tests/test_a_rider_reaches_its_file.py` | 55b4d617 |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- A new flag on a shipped command, additive. Every existing invocation —
  the sealer's `broad-gate --base <base> --record <item>`, the vendored CI
  template, the lenient ledger notice that names the gate — runs exactly as
  before.
- Nothing under `hooks/`, no workflow step, no new dependency, no new
  environment variable. The arms are the Python subprocesses the gate already
  spawns.
- `templates/config.md`'s example row changes order. A repository that copied
  the old example keeps the row it has; nothing reads the example, which is
  fenced and therefore invisible to every reader of the table
  (`hooks/config.py#unfenced`).
- The orchestration document gains a step. A session that skips it loses
  nothing but time: the sealer asks the same arms and refuses the same way,
  which is what the acts table's `still a sentence` row records.
