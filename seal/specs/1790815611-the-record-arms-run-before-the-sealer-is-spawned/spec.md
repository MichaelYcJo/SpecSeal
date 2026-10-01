# Feature Specification: the record arms run before the sealer is spawned

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between two designs that catch the same refusal, the cheaper one wins. A refusal on a record arm found before the sealer is spawned costs seconds; the same refusal found by the sealer costs a spawn and a suite. The ticket measured 24 minutes of one release on that difference |
| `docs/the-broad-gate.md` §*One act, one owner, and the owner is an agent* | The sealer judges nothing and takes the one broad run. This work adds nothing to the sealer: the preflight is the orchestrator's, runs no suite, lint or typecheck, and seals nothing |
| `docs/the-broad-gate.md` §*What the gate runs, and how the list is kept true* | Every arm is declared in `broad_gate.py#PARTITION` and held against `hygiene.yml`. The preflight adds no arm and names no second list: it runs the arms the gate already declares, with the repository's row left out |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget, platform honesty. S7 below is the red-first case; the direction is *block more, earlier* (a refusal the sealer would have given arrives before the spawn, and nothing that would have sealed is refused); the prompt budget is zero, because the preflight asks nobody; the arms are Python subprocesses and the row is not run, so no shell quoting is reached on either platform |
| `docs/review-chain-spec.md` §*Then the `sealer` takes the broad gate once* | The sealer is still spawned once, after the rounds settle, and its run still writes the cell. The preflight does not replace that run and must not be mistaken for it — which is why its output carries no `SEALED` line |
| `skills/agent-contract/SKILL.md` §2, §15 | §2: the broad gate is suite, lint and typecheck together; the preflight runs none of the three, so it is not a broad run and the orchestrator may take it. §15: every new case is shown red before it is planted |
| `routing.md` §*Why this way* | The owner's answer of 2026-10-01: `templates/config.md`'s example row goes lint-first, like this repository's own |

## Scope

The ticket is #638, item B of the 2026-09-28 flow-log sweep for release 0.17.0.
The measured cost: `broad-gate` runs the repository's `Broad gate` row first and
its own record arms after it, so a refusal on a record arm — a DRIFTED ledger
row, a chain refusal over `fixed at` in a verifying round, a survivor — arrives
only after a full suite, and nothing runs those arms before the sealer is
spawned. Six instances across five releases are listed in the ticket, each read
from a flow log.

In:

- **`broad-gate --preflight`**, a flag on the existing command. It resolves the
  base, reads the `Broad gate` row and applies every refusal the full run
  applies to it, and then runs the record arms — every arm `gate()` runs
  except the repository's row — in the same order and with the same arguments.
  It writes no cell, no values file and no stamp, runs no `round_record.py
  seal`, adds no worktree, and prints no line beginning `SEALED` or
  `NOT SEALED`. Exit 0 when every arm passed, 1 when any arm failed, 2 on a
  refusal with nothing run.
- `--preflight` together with `--record` is a refusal: exit 2, nothing run, a
  sentence naming both flags and saying the preflight writes no cell.
- `skills/code-review/orchestration.md` §*Orchestrator: the pull request opens
  before round 1, and a phase is re-run* names the preflight as the step
  before `spawn \`sealer\``: the orchestrator runs it, reads the exit code
  directly, and spawns only on 0. No new heading — a paragraph inside the
  section that already holds the spawn, so the acts table in
  `skills/implement/orchestration.md` needs no new row; its row for that
  section gains the preflight in its `Grounds` cell. Where
  `skills/implement/orchestration.md` §*Orchestrator: the order inside a ticket*
  sequences the sealer's spawn, the preflight is written in as the step before
  it.
- `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare
  against the base*: one sentence saying the preflight is the orchestrator's,
  runs before the spawn, runs no suite and seals nothing.
- `templates/config.md`: the example `Broad gate` row changes to the lint-first
  order, `uvx ruff check . && uvx ruff format --check . && bin/test -q`
  (the owner's answer, 2026-10-01). The sentence beside it that lists the
  plugin's own checks is corrected to point at `broad_gate.py`'s docstring
  rather than naming four of the six arms by hand, and says that
  `broad-gate --preflight` runs those arms alone.
- `skills/verify/scripts/broad_gate.py`'s module docstring: the usage line and
  one paragraph for the flag.
- The cases, in `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the
  gate's fixture repositories live there) and `tests/test_broad_gate_rule.py`
  (the document pins). Every new case is seen red first (§15).
- The ticket's verification: a fixture record with `fixed at` in a verifying
  round's table makes `broad-gate --preflight` exit 1 without invoking the row,
  and the wall clock is measured once and written down.
- `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`, the builder's.

Out:

- `agents/sealer.md`. The sealer's four acts and its one write are unchanged;
  `tests/test_broad_gate_rule.py::test_only_one_definition_assigns_the_broad_gate`
  keys on that file alone carrying `spawned for exactly that`, and the sealer
  never preflights (plan.md §*Alternatives considered*, C).
- Reordering the gate's own arms. The ticket rejects it, and the tree agrees:
  the report's *every check that failed* property (`broad_gate.py` module
  docstring, *A check that fails does not stop the ones after it*) is what a
  reader acts on.
- A dry run of `round_record.py seal`'s three record refusals (an unchecked
  `Pass`, a `Fixes checked by` outside the one value, a spent SHA). The
  ticket scopes the preflight to arms 2–7, and that function's contract counts
  its refusals by its own `raise` sites. #456's first refusal, an unchecked
  `Pass` box, therefore still reaches the sealer; plan.md §*Alternatives
  considered*, E, names it for the owner as a possible follow-up.
- A new command or `bin/` wrapper pair. The flag rides `bin/broad-gate` and
  `bin/broad-gate.cmd` as they stand (`"$@"` and `%*` pass it through), and
  the tree-copy redirect in `broad_gate.py#main` already hands a flag only the
  tree's copy knows to that copy.
- `docs/the-broad-gate.md`. A policy document is ratified by a person, and
  `settle` folds this spec into it after the release; nothing in it is made
  false by this work.
- `README.md` and `README.ko.md`. Both describe the sealer's run, which is
  unchanged. Named here so the omission is a decision rather than a gap:
  if a phase finds either README stating the gate's arm order or the
  template's example row, both move together.
- `hooks/`, `hygiene.yml`, `PARTITION`, `SKIPPED_AT_MAIN`. Untouched by
  construction (S5).
- The orchestrator's narrow run at each phase boundary and the review
  rounds' own `evidence-check`/`survivor-check` runs. The preflight is a step
  at one moment, before the sealer's spawn, and replaces none of them.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a green tree preflights green and seals nothing | Given the sealer-test fixture with every arm green, when `broad-gate --preflight --base base --root <repo> --keep-output <dir>` runs on a pipe, then exit 0; `<dir>` holds one `<arm>.txt` per record arm, each opening `$ ` and carrying `exit 0`, in the gate's order; no `suite.txt`; no line of stdout begins `SEALED` or `NOT SEALED`; stdout names the preflight, the tree and the resolved base; no values file under `.git/specseal-stamp/`; no disc, no colour | a case in `tests/test_the_seal_is_taken_once_by_the_sealer.py` beside `test_a_green_tree_is_sealed_with_every_check_run_in_order` |
| S2 the row is not run | Given the fixture's row set to `exit 1` (`set_row`), when the preflight runs, then exit 0 — the full gate over the same tree is exit 1 and `NOT SEALED` | the same module; this is the case that shows the flag does something: with the flag ignored the row runs and the exit is 1 |
| S3 a failing record arm is named and the row is still not run | Given the fixture with its overview's `## Not verified` row deleted (the shape `test_a_plugin_check_that_fails_is_named_and_the_suite_is_not_compared` uses) and the row set to `exit 1`, when the preflight runs, then exit 1; stdout names `unverified` with its exit code and first lines in the gate's failure words; `suite.txt` absent; no worktree added; no `NOT SEALED` | the same module |
| S4 `--record` is refused | Given a settled item, when `broad-gate --preflight --record <item>` runs, then exit 2, nothing run (the output directory is empty or absent), no cell written, and stderr names both flags and says the preflight writes no cell | the same module, beside `test_a_refused_row_runs_no_check_and_adds_no_worktree` |
| S5 the arm list is the gate's | `PARTITION`, `SKIPPED_AT_MAIN` and the `checks[...] = run(...)` assignments `gate()` carries are unchanged; `args.base` is still read once | `tests/test_the_gate_names_every_step_ci_runs.py` (both sides), `tests/test_the_gate_asks_the_range_ci_will_ask.py::test_the_gate_reads_the_given_base_exactly_once`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` — all green unchanged |
| S6 the row's refusals still apply | Given a fixture with no `Broad gate` row, when the preflight runs, then exit 2 with the absent-row sentence and nothing run; the same for a row wrapped in backticks | the same module, beside `test_without_the_row_the_gate_names_it_and_runs_nothing` |
| S7 the ticket's verification | Given a fixture item whose verifying round's record carries a `fixed at` verdict in a shape `chain_check.py` refuses under the draft payload (Q1 of `questions.md` says which), when the preflight runs, then exit 1 with `chain` named, and the row was not invoked. Seen red first: with the flag absent the command is refused by argparse before anything runs, and with the flag ignored the fixture's row runs. The wall clock is measured once and written to `phases/phase-2.md` (Q2) | the same module |
| S8 the orchestrator is told, in order | `skills/code-review/orchestration.md` names `broad-gate --preflight` inside §*Orchestrator: the pull request opens before round 1, and a phase is re-run*, before the words `spawn \`sealer\``; the section gains no heading; the acts table's row for it still reads `still a sentence` with the preflight in its grounds | a case in `tests/test_broad_gate_rule.py` asserting the order by index; `tests/test_every_orchestrator_act_names_its_delivery.py` green unchanged |
| S9 the example row is lint-first | `templates/config.md`'s fenced example reads `| Broad gate | uvx ruff check . && uvx ruff format --check . && bin/test -q |`, and the sentence listing the plugin's checks names no arm by hand | a case in `tests/test_broad_gate_rule.py`; `tests/test_the_seal_is_taken_once_by_the_sealer.py::test_this_repositorys_own_config_is_answered_exactly_as_before` green |
| S10 the preflight is not the broad gate | `skills/verify/SKILL.md` §*The broad gate* says the preflight runs no suite and seals nothing; `agents/sealer.md` is byte-identical to the release base | a case in `tests/test_broad_gate_rule.py`; `git diff cd24f516 -- agents/sealer.md` empty, recorded in `overview.md` |

## Data & interfaces

**The flag.** `broad-gate --preflight --base <ref> [--root DIR] [--keep-output DIR]`.
`--base` is required as before and resolved the same way; `--record` is
refused beside it (S4); `--shape` and `--scale` are accepted and change
nothing, because nothing is drawn.

**What a preflight run does, in order**, from the repository root:

1. The same refusals as the full run, before anything runs: no repository, no
   `seal/` root, the row absent, malformed, fenced, commented or unrunnable as
   written, a base that does not resolve, `--record` given. Exit 2.
2. The stderr lines every run carries: the running copy's path, the moved-base
   line where resolving moved the answer, the line naming the row — suffixed
   so a reader can see the row was read and not run — and the skipped-at-main
   line where it applies. The coverage line is not printed: it says what *this
   seal* answers, and a preflight seals nothing.
3. The record arms, with the same names, arguments and environment `gate()`
   gives them: `ledger`, `unverified`, `chain` (draft-judged), `survivors` and
   `corrections` unless skipped at `main`, `mode`. Each arm's output is kept
   under `--keep-output` as `<arm>.txt` exactly as today.
4. The verdict. On any failure, the failing arms in the failure form's words
   (`failure_lines`: exit, first lines, the file holding the rest) under a
   first line that names the preflight, the tree and the resolved base — and
   never `NOT SEALED`. Exit 1. The reactive base comparison is not reached,
   because it exists for a failing test and no test ran. On success, one line
   naming the preflight, the tree and the base and saying nothing was sealed.
   Exit 0.

**What a preflight run never does:** run the row, call `round_record.py seal`,
write a `Broad gate` cell, write a values file, draw a stamp, add a worktree.

**Exit codes**, unchanged in meaning: 0 every arm passed · 1 an arm failed ·
2 refused with nothing run.

**The arms are not a second list.** `gate()` keeps its `checks[SUITE] =
run(...)` assignment; the preflight skips it by condition, so the AST readers in
`tests/test_the_gate_names_every_step_ci_runs.py#arms_the_gate_runs` and
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py#failure_loop`
read the same tree they read today.

**Documents touched**, each by one bounded edit: `skills/verify/scripts/broad_gate.py`
(docstring, flag, the preflight branch of `gate()`),
`skills/code-review/orchestration.md` (one paragraph),
`skills/implement/orchestration.md` (one `Grounds` cell; the order section
where it names the spawn), `skills/verify/SKILL.md` (one sentence),
`templates/config.md` (the example row; the arms sentence),
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_broad_gate_rule.py`,
`seal/specs/<id>/changelog.md`, `seal/ledger/<id>.md`, `seal/specs/<id>/overview.md`,
`seal/specs/<id>/phases/phase-N.md`.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. The owner's answer on
the template row is recorded there as answered; the four rows that remain are
two for the work and two for a measurement, and none blocks the build.

Framed 2026-10-01 by framer, before the build.
