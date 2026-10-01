# Feature Specification: the preflight asks seal's own refusals

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between two designs that catch the same refusal, the cheaper one wins. `round_record.py seal` refuses an unchecked `Pass`, a `Fixes checked by` outside `no fixes to check`, and a spent SHA AFTER every check has passed, so each costs a spawn and a suite. Asking the same refusals in the preflight costs one subprocess before the spawn |
| `docs/the-broad-gate.md` §*One act, one owner, and the owner is an agent* | The sealer still takes the one broad run and still makes the one write. The preflight asks `seal`'s questions and writes nothing; `agents/sealer.md` is unchanged |
| `docs/the-broad-gate.md` §*What the gate runs, and how the list is kept true* | `PARTITION` mirrors CI's steps. The ask mirrors no CI step — it is the sealer's own pre-write question asked early — so it is NOT a `checks[...] = run(...)` arm of `gate()` and `PARTITION` gains no row (S7) |
| `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped* | "`round_record.py seal` refuses to write `Broad gate` on a last record whose cell reads anything else, so the reader is required by the generator and not by this document alone." The generator stays the authority: the preflight runs the same subcommand with a flag that stops it before the write, and restates no predicate |
| `docs/review-handoff-protocol.md` §*The Fixes checked by field — who opened the closing* | The last record may read only `no fixes to check` or `nobody — <why>`, and `seal` accepts the first alone. `nobody` on the last record is #535's shape as `new` and `close` write it today (1790815611 `phases/phase-2.md`) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Red first (S-cases, each seen red); direction *block more, earlier* — the preflight now exits 1 where the sealer would have exited 2 after a suite, and nothing that would have sealed is refused, because the predicates are `seal`'s own; prompt budget zero, the preflight asks nobody; platform: a Python subprocess with no shell |
| `skills/agent-contract/SKILL.md` §1, §12, §14, §15 | §1: the ask's exit code is read off its subprocess, never a pipe. §12: the class is every refusal `seal` raises before the write, not the two instances the ticket names. §14: every new printed line is pinned. §15: every case is seen red first |
| `routing.md` §*Why this way* | The owner's answer of 2026-10-01: `automation`, and a framer draws the frame because a command's verdict changes |

## Scope

The ticket is #702. `broad-gate --preflight` (#638, PR #697) runs the record
arms before the sealer is spawned, and `round_record.py seal` raises three
refusals that are not record arms — they fire when the sealer writes the
`Broad gate` cell, after the suite. Round 1 of work item `1790815611` executed
it: #535's shape as `new` writes it today (`Pass` ticked beside `nobody — the
fixes are not yet written` on the last record) passes the preflight, exit 0,
and the full gate with `--record` refuses it at `seal`, exit 2, after every
check passed. That work item's `plan.md` alternative E names this change and
left it unbuilt.

In:

- **`round_record.py seal --check`.** The `seal` subcommand gains one flag.
  With it, `seal` resolves the home, reads the last record and raises every
  refusal it raises today — the six `raise Refused` sites of `seal()` plus
  `seal_home`'s — then stops: it writes no cell, runs no `chain_check`, prints
  one line naming the record it asked and saying nothing was written, and
  exits 0. A refusal exits 2 with the sentence `seal` prints today, unchanged.
  The line never begins `round-record: sealed`, because `broad_gate.py#gate`
  reads that prefix as *the cell WAS written*. `--check` is the name every
  verify-and-exit flag in this repository takes (`seal.py mode --check`,
  `fold_ledger.py --check`, `claude_block.py --check`).
- **The preflight asks it.** Under `--preflight`, after the record arms have
  run, `gate()` finds the work item declared for the checked-out branch —
  `hooks/routing.py#item_dir(root, branch)`, the key `routing.for_branch`
  reads at the commit and `chain_check.declared_for_this_branch` reads in the
  chain arm — and runs `round_record.py seal --check --item <item>
  --broad-gate "<tree> against <base commit>" --root <root>` through
  `seal_record(..., check=True)`, the same function the full run calls to
  seal. The subprocess's output is kept as `<keep>/seal.txt` exactly as a
  full run keeps it, and its exit code is read directly. Non-zero joins
  `failures` under the name `seal`, so the verdict is `PREFLIGHT FAILED` with
  `seal   exit 2` and the refusal's first lines in the failure form's words,
  exit 1. The ask runs AFTER the arms and does not stop on an arm's failure,
  so a chain refusal and a `seal` refusal are both named in one run.
- **Where nothing is asked, the preflight says so.** No single declaration
  names the branch — none, two, a detached HEAD — and the ask is skipped: one
  stderr line names the branch and says `seal`'s refusals were not asked, no
  `seal.txt` is written, and the exit is the arms' own. A work item that
  declares `straight to the PR` is asked and `seal --check` answers that no
  round record is read for it (`seal_home` returns the `broad-gate.md` home),
  exit 0. A `through the review chain` declaration with no round record is a
  `seal_home` refusal today and is a `seal` failure in the preflight.
- **The orchestrator types nothing new.** `broad-gate --preflight --base
  <base>` is the whole command, as `skills/code-review/orchestration.md` and
  `skills/implement/orchestration.md` already say; `--preflight --record` stays
  refused (#638's S4, unchanged). What changes in the documents is what the
  preflight is said to ask and what to do when `seal` is named: the paragraph
  *The preflight is yours, and it is not the broad gate* in
  `skills/code-review/orchestration.md` gains the ask and the two acts a
  `seal` refusal sends a reader to — spawn the verifying round where the cell
  reads `nobody`, fix the open finding where `Pass` is unchecked, which are
  `seal`'s own sentences — and its last sentence stops saying the sealer
  refuses the same way *after a suite* as the only remedy. The acts-table
  `Grounds` cell for that section in `skills/implement/orchestration.md`
  names the ask. `skills/verify/SKILL.md` §*The broad gate*'s preflight
  sentence and `templates/config.md` §*Broad gate*'s preflight sentence each
  gain the clause. The ticket-order line in `skills/implement/orchestration.md`
  is unchanged (its arrows are pinned verbatim).
- **The verdict lines.** The `PREFLIGHT PASSED` / `PREFLIGHT FAILED` heads
  keep #638's `<tree> against <base>` shape (1790815615 §*Not done* records
  that #666's names do not reach them). `PREFLIGHT_TAIL` says what the run
  did: the record arms and `seal`'s refusals, the row not run, nothing
  sealed. One stderr line per run says which record `seal` was asked about,
  or why none was.
- **`broad_gate.py`'s module docstring**: the `--preflight` paragraph and the
  exit-code sentence gain the ask; `round_record.py`'s header and `seal`'s
  docstring gain `--check`.
- **The cases**, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
  (the gate's and `seal`'s fixtures live there) and
  `tests/test_broad_gate_rule.py` (the document pins). Every case is seen red
  first; the two mutations that matter are `--check` ignored (the preflight
  writes a cell) and the ask dropped (#535's shape preflights green).
- **The sibling's changelog fragment.** `seal/specs/1790815611-…/changelog.md`
  says *A refusal that `round_record.py seal` raises … still reaches the
  sealer.* Both fragments ship in 0.17.0, gathered in id order, so the
  released section would assert the boundary and its removal in consecutive
  entries. One sentence is appended to that fragment naming #702 as the entry
  that closes it, dated. The fragment is unreleased text nobody has read yet;
  #638's `overview.md` and `phases/phase-2.md` are past-state records and are
  left as they stand.
- **The records**: `seal/specs/<id>/changelog.md`, `seal/ledger/<id>.md`,
  `overview.md`, `phases/phase-N.md`, and the re-read of every ledger row
  whose anchor this work drifts — `round_record.py#seal@0cfc9d4e` (eleven
  rows: 0.10.0 S10 and S13, 0.11.5, 0.13.1 C3, 0.15.0 A5 and A9, 0.15.1 N4,
  0.16.0 G2 among them), `broad_gate.py#seal_record@4d582ed3` (0.10.0 S12),
  and `broad_gate.py#gate@51ce700f` (fifteen rows across 0.10.0, 0.12.0,
  0.12.2, 0.15.4, 0.15.7 and the 1790815611 fragment's P1–P6) — 26 rows in
  eleven files, counted 2026-10-01 at `e83db346`. Each is read against the
  edit and re-stamped with `--checked 2026-10-01`, its claim corrected in
  place where the edit made it false.

Out:

- **`agents/sealer.md`.** The sealer's four acts, its command and its one
  write are unchanged; `tests/test_broad_gate_rule.py::test_the_skill_says_the_preflight_is_not_the_broad_gate`
  asserts `--preflight` is not in that file, and
  `::test_the_sealers_definition_names_the_narrowed_row` in the sealer module
  pins *refuses outright on three things*, which stays true.
- **`seal` without `--check`.** Byte-for-byte the same behaviour: the same
  refusals in the same order, the write, then `chain_check --worktree`. The
  sealer's `broad-gate --base <base> --record <item>` is unchanged.
- **Lifting the `--preflight --record` refusal** or adding a second
  item-naming flag. `plan.md` §*Alternatives considered* A and B say why: a
  flag a session can forget is a check that arrives only when typed, and the
  branch is a key three readers already share.
- **`chain_check.py`.** No new arm, and the draft/ready asymmetry on `Pass`
  beside `nobody` (#598) stays: on a draft that pair prints, and the preflight
  judges a draft. The ask reaches the sealer's refusal through the sealer's
  own subcommand, not by judging the chain arm as ready.
- **A `checks[...] = run(...)` arm, a `PARTITION` row, `SKIPPED_AT_MAIN`,
  `hooks/`, `hygiene.yml`.** Untouched by construction (S7).
- **`docs/the-broad-gate.md`, `docs/review-chain-spec.md`,
  `docs/review-handoff-protocol.md`.** Policy, ratified by a person; `settle`
  folds this spec after the release. Nothing in them is made false.
- **`README.md`, `README.ko.md`.** Their chain diagram reads `sealer → broad
  gate` and names no step before the spawn; #638's round 1 (⬜ 4) enumerated
  them as not false, and this work makes them no less true. Named here so the
  omission is a decision: if a phase finds either README stating what the
  preflight runs, both move together.
- **`--record ""` beside `--preflight`** (#638 round 1 ⬜ 2, answered as left).
- **The `n is None` branch of `seal`** (a `straight to the PR` item): its two
  SHA refusals are asked under `--check` as today and cannot fail for a value
  the gate composed from `rev-parse HEAD`; nothing is added for that home.
- **A timing assertion.** The ask's wall clock is measured once and written
  down (`questions.md` Q3), never pinned.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 `seal --check` refuses what `seal` refuses, and writes nothing | Given the sealer module's fixtures — `generate(repo, 1, OPEN_ROW, "no")` (an unchecked `Pass`), `fixed_but_unread_item` (`nobody` on the last record), `settled_item` with `--broad-gate "<base sha> against base"` (a spent SHA), and a chain declaration with an empty `rounds/` — when `run_seal(repo, value, ("--check",))` runs, then exit 2 for each, the sentence `seal` prints today on stdout+stderr (`` `Pass` is unchecked ``; `read by no LATER round`; `descends from`; `holds no round-N.md`), the record byte-identical, no `chain-check` output | four cases in `tests/test_the_seal_is_taken_once_by_the_sealer.py` beside `test_seal_refuses_while_pass_is_unchecked`, each red first with the flag absent (argparse exit 2) |
| S2 `seal --check` passes what `seal` would seal, and still writes nothing | Given `settled_item`, `capped_item` and a `straight to the PR` declaration with no rounds, when `--check` runs with `"<HEAD> against base"`, then exit 0, the record (or the absent `broad-gate.md`) byte-identical, no `chain-check` line, one stdout line naming the record asked (or saying no round record is read for this home) and saying nothing was written, and no line beginning `round-record: sealed` | three cases in the same module; red first with `--check` ignored (the cell is written — the byte comparison fails) |
| S3 #535's generated shape fails the preflight at `seal` | Given `fixed_but_unread_item` (round 1 closed on a fix by `close`, no round 2 — `Pass` ticked beside `nobody — the fixes are not yet written`, exactly as `new` and `close` write it, no hand edit) and the row set to a marker-writing command that exits 1, when `broad-gate --preflight --base base --keep-output <dir>` runs, then exit 1; stdout opens `PREFLIGHT FAILED` and has a line matching `^\s+seal\s+exit 2`; `<dir>/seal.txt` opens `$ ` and carries `Fixes checked by` and `read by no LATER round`; no `suite.txt`, the marker absent; no line begins `SEALED` or `NOT SEALED`; the record byte-identical; no values file | a case in the same module beside `test_a_fixed_at_verdict_in_a_verifying_round_fails_the_preflight`; red first against the unedited gate (exit 0 — the case round 1 of 1790815611 drafted, first assertion flipped) |
| S4 an unchecked `Pass` fails the preflight at `seal` | Given `declared(repo)` then `generate(repo, 1, OPEN_ROW, "no")`, when the preflight runs, then exit 1 with `seal` named and `` `Pass` is unchecked `` in `seal.txt`; the record byte-identical | the same module; red first against the unedited gate |
| S5 a spent SHA fails the preflight at `seal` | Given a declared item whose last record's `Target SHA` names a commit that DESCENDS from HEAD (a commit made on a side branch from HEAD and handed to `generate(..., target=X)`), when the preflight runs at HEAD, then exit 1 with `seal` named and `descends from` in `seal.txt` | the same module; `questions.md` Q2 leaves the fixture's construction to the phase, and the predicate is already covered at the subcommand by S1 |
| S6 a settled item preflights green and names the record it asked | Given `settled_item` (round 2 reads `no fixes to check`, `Pass` ticked) with every arm green, when the preflight runs, then exit 0, `PREFLIGHT PASSED` first, `seal.txt` present with `exit 0`, the record byte-identical, stderr naming `round-2.md` as the record asked, no values file, no `SEALED` line | the same module beside `test_a_green_tree_preflights_green_and_seals_nothing`; red first with the ask dropped (no `seal.txt`) |
| S7 the ask is not an arm | `tests/test_the_gate_names_every_step_ci_runs.py#arms_the_gate_runs` and `::test_the_gate_runs_no_arm_the_partition_does_not_account_for` read every `checks[...] = run(...)` inside `gate()`; `record_arms()` in the sealer module reads the same; the ask is made through `seal_record` and appears in neither; `PARTITION` and `SKIPPED_AT_MAIN` unchanged; the one loop over `checks.items()` unchanged; `args.base` read once | `tests/test_the_gate_names_every_step_ci_runs.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_the_gate_asks_the_range_ci_will_ask.py::test_the_gate_reads_the_given_base_exactly_once`, and `test_a_green_tree_preflights_green_and_seals_nothing` (which asserts the kept `.txt` files are exactly the record arms' on an undeclared fixture) — all green unchanged |
| S8 no declaration, nothing asked, said so | Given the plain fixture (`build_repo`, no `routing.md`) with every arm green, when the preflight runs, then exit 0, no `seal.txt`, and one stderr line naming the branch `feature` and saying `seal`'s refusals were not asked. The same line and exit for two declarations naming `feature` | two cases in the same module; red first with the line dropped |
| S9 `--preflight --record` is still refused | #638's S4 case `test_a_preflight_with_record_is_refused_and_writes_no_cell` | green unchanged |
| S10 the full gate is unchanged | `test_the_gate_with_record_seals_the_item_and_counts_its_rounds`, `test_the_gate_with_record_prints_no_stamp_when_the_record_refuses`, `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed`, `test_the_gate_reads_the_real_seals_two_endings_apart`, and every `test_seal_*` case of the sealer module | green unchanged; `seal_record`'s existing call site passes no `check` |
| S11 the orchestrator is told what the preflight asks, and types nothing new | `skills/code-review/orchestration.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run* still names `broad-gate --preflight --base <base>` before `spawn \`sealer\`` and now says the preflight asks `seal`'s refusals of the branch's work item and what a `seal` line under `PREFLIGHT FAILED` sends the reader to; the acts-table `Grounds` cell in `skills/implement/orchestration.md` names the ask and the row still reads `still a sentence`; `skills/verify/SKILL.md` §*The broad gate* and `templates/config.md` §*Broad gate* each say the preflight asks `seal`'s refusals; the order line's arrows are unchanged | cases in `tests/test_broad_gate_rule.py` beside `test_the_orchestrator_runs_the_preflight_before_it_spawns_the_sealer`, each red against the unedited documents; `tests/test_every_orchestrator_act_names_its_delivery.py`, `tests/test_the_rules_have_one_owner.py::test_the_order_opens_the_draft_between_the_build_and_the_rounds`, `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py` green |
| S12 the sealer's definition is untouched | `git diff e83db346 -- agents/sealer.md` empty, recorded in `overview.md` | `tests/test_broad_gate_rule.py::test_the_skill_says_the_preflight_is_not_the_broad_gate` green |

## Data & interfaces

**`round_record.py seal`** gains `--check` (`store_true`): *ask every refusal
and write nothing*. Order inside `seal(args)`: `where`, `seal_home`, the
record read, the `Pass` box count, the `Pass` state, `Fixes checked by`, the
SHA-shaped word, the SHA resolving, the ancestry — all as today — then, where
`args.check`, print one line and `return 0` before `kept_broad_gate`, the
write and `run_check`. The refusal count the docstring states by `raise` site
is unchanged. The success line names the record's path relative to the root
(or says no round record is read for a `broad-gate.md` home), says that
nothing was written and that this was `--check`, and does not begin
`round-record: sealed`.

**`broad_gate.py`**:

- `seal_record(item, tree, root, base, keep, check=False)` — with `check`
  the argv gains `--check`; the kept file is `seal.txt` as today.
- in `gate()`, under `args.preflight`, after the arms and before the failure
  loop's result is judged: `item = routing.item_dir(root, branch)` where
  `branch` is the `branch_name(root)` #666 already computes and `routing` is
  `hooks/routing.py` loaded the way `round_record.where` loads it
  (`chain_check.ROUTING`); where `item` is non-empty,
  `code, text = seal_record(item, tree, root, base.commit, keep, check=True)`
  and on `code != 0` the `seal` entry joins `failures` with
  `failure_lines(Check(...))`'s shape — `exit <code>`, first lines, `full
  output: <keep>/seal.txt`; where `item` is empty, one stderr line. The
  `checks` dict and its loop are untouched (S7).
- `PREFLIGHT_TAIL` names the ask; one new stderr line names the record asked
  (`broad-gate: asked \`seal\`'s refusals of <relpath>`) or why none was.
  Exact wording is the phase's (Q1), pinned by the case that reads it.

**What a preflight run does, in order**, from the repository root — #638's
list with one step added:

1. The same refusals as the full run; `--record` given is still a refusal.
2. The stderr lines every run carries.
3. The record arms, kept as `<arm>.txt`.
4. **`seal --check` of the branch's declared work item, kept as `seal.txt`;
   or one line saying why none was asked.**
5. The verdict: `PREFLIGHT FAILED` with every failing arm and, where it
   refused, `seal`, exit 1; else `PREFLIGHT PASSED`, exit 0.

**What a preflight run never does**, unchanged: run the row, write a cell,
write a values file, draw a stamp, add a worktree, print `SEALED` or
`NOT SEALED`.

**Exit codes**, unchanged in meaning: 0 every arm passed and `seal` would
seal · 1 an arm failed or `seal` would refuse · 2 refused with nothing run.

**Documents touched**, each by one bounded edit:
`skills/code-review/scripts/round_record.py` (header, `seal`'s docstring,
the flag, the early return), `skills/verify/scripts/broad_gate.py`
(docstring, `seal_record`, the preflight step in `gate()`, the tail and the
line), `skills/code-review/orchestration.md` (the preflight paragraph),
`skills/implement/orchestration.md` (one `Grounds` cell),
`skills/verify/SKILL.md` (one sentence), `templates/config.md` (one sentence),
`seal/specs/1790815611-…/changelog.md` (one appended sentence),
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_broad_gate_rule.py`, this work item's records and ledger
fragment, and the release files whose rows the edits drift.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. No row there needs a
person: two are the work's, two are measurements, and none blocks the build.

Framed 2026-10-01 by framer, before the build.
