# Implementation Plan: two agents are forbidden the seal and nobody is assigned it

<!-- seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

Four things, in the order they can be verified. A stamp module that draws the
seal from a chart and prints it on success only, with an ASCII twin for a
console that cannot render blocks. A gate command that runs the repository's
broad command and the plugin's own checks, reads every exit code directly,
compares a failing test against the base only when one fails, and on success
prints the stamp and writes the last record's `Broad gate` cell through a new
`round_record.py seal` subcommand. A fourth agent definition whose whole
procedure is that command, with `agent-contract` as its only preloaded skill.
And the rule given its owner in every document that stated it without one —
two agent definitions, five documents, three pinned sentences.

The work adds an agent, changes two, adds a command to every user's PATH and
a row to `seal/config.md` — all things a session reads and acts on — which is
the top rung of the `implement` skill's ladder. `spec.md` and this plan come
first; the gate was passed in the owner's one batch on 2026-09-10.

## Technical context

Every coordinate below was opened by the session that wrote this plan; the
smith opens them again before building on them (§5).

- `~/Documents/pixelart-fleur/{chart.txt,seal.py,stamp.py}` — the chart
  (29×32, `D R y Y .`), the computed disc (`build`, `shrink`, `row` with
  colour at transitions, `KEY` for the letter form), the panel (`letter`,
  `beside`). Outside the tree; the smith reads it once and the module in
  the tree is the only copy afterwards. **Nothing in the tree may name that
  path** — `tests/test_no_real_identifiers.py` refuses a home path.
- `hooks/console.py#to_utf8` — how the streams are reconfigured; the stamp
  picks its twin from `sys.stdout.encoding` and `isatty()` after that call,
  so a cp949 console gets letters and a UTF-8 pipe gets blocks.
- `skills/verify/scripts/session_cost.py`'s and `payload_meter.py`'s
  interpreter-floor guard (copied from `round_record.py#below_floor`) — the
  two new scripts carry it; `tests/test_a_script_says_which_interpreter_it_needs.py`
  is the module that reads it.
- `bin/session-cost` + `.cmd` — the wrapper pair to copy;
  `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#test_every_bin_entry_has_a_windows_twin`
  pins the pairing. The same module pins, at `:153` and `:764`, *the full
  suite is the orchestrator's* in `bin/test` and in
  `docs/review-handoff-protocol.md` — both sentences move to *the
  sealer's*, and both cases are re-pointed and seen red.
- `skills/code-review/scripts/round_record.py` — `main` at `:2890` builds
  the two subparsers; `cell(BROAD_GATE, …)` at `:1705` and the `close` path
  at `:2816-2861` are how the cell is written; `chain_check.broad_gate` at
  `chain_check.py:2850` is the test the `seal` subcommand applies to its own
  argument before writing (premature SHA). `reach_back` at `:1356` is the
  pattern for editing one cell of an existing record.
- `skills/implement/scripts/seal.py:1416-1472` — how the `Mode` row is
  found and written; the `Broad gate` row is read the same way, by
  `broad_gate.py`, without importing `seal.py` (103 KB) — a small reader of
  the table is enough, and it is the shape `hooks/config.py` already has for
  the language rows; read that first.
- `templates/config.md` §*Mode* — the shape a row's section takes; the new
  section says what an absent row means (a refusal, exit 2) and why not a
  default. `skills/config/SKILL.md:31-41` — the table the skill prints; a
  fourth row. `tests/test_the_settings_have_a_front_door.py` reads that
  skill — run it.
- `agents/smith.md:187` and `agents/warden.md:50-51` — the two sentences
  that name the orchestrator as owner. `agents/warden.md:224-230` — the
  *carry the broad-gate state* bullet, which gains *what comes due is the
  sealer's spawn*. `agents/smith.md:269-277` — *Then the broad gate runs
  once* and the three-returns rule, which gain who runs it.
- `tests/test_every_agent_reads_the_contract.py#PINS` and
  `#test_the_line_is_identical_in_every_definition` — the paragraph the
  sealer's definition opens with, byte for byte;
  `tests/test_a_moved_rule_leaves_its_definition.py` (15-word window over
  the contract's sections) — the sealer's definition may cite §2 and §6 by
  number and say what each means for it, and may not carry their sentences;
  `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` —
  the fourth `skills:` list is read by it;
  `tests/test_chain_hooks_hardening.py:618-700` — the preloaded-skill
  counts derive from `agents/*.md`, and `agent-contract` is already
  preloaded, so the counts do not move; the README agent tables are read
  for every preloaded skill's name.
- `README.md:36-45` and `README.ko.md:35-40` — the agent tables;
  `README.md:46-60` — the chain diagram's `broad gate` line.
- `skills/code-review/orchestration.md:439-447` — the paragraph that tells
  the orchestrator to run the pass and write the cell with `close
  --broad-gate`; it now says to spawn the sealer, and names both
  subcommands. `skills/verify/SKILL.md:249-300` — §*The broad gate*.
  `docs/review-chain-spec.md:181`. `templates/sdd-round.md:33` — the
  `Broad gate` row's comment. `docs/flow.md:95` — the row to tick, and
  `:177` already names the sealer in the order.
- `tests/test_the_rules_have_one_owner.py:487` pins the flow's order line
  as it stands — it does not change.

**What breaks in six months.** A repository writes a `Broad gate` row that
exits 0 without running anything (`true`, or a linter aimed at a directory
with no files), and the stamp prints over it. The sealer cannot judge a
command, so the panel's `suite` row shows what the command's last line said
and `verify`'s *the narrow command still has to be able to fail* is the
reader's rule; the plugin's own checks still run behind it. The second
failure: #120 rewrites §2 and §6 and the sealer's definition keeps its
*until #120* paragraph, now stale. `tests/test_release_hygiene.py` refuses a
loaded document naming a shipped version, not a ticket; so the phase-4 record
names that paragraph as the one #120 deletes, and #120's frame reads it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| The orchestrator keeps the gate; only the documents change | the act stays with the one participant a release cannot replace, hundreds of output lines land in its context, and #30's measurement — the warden running it unprompted — is unanswered | rejected — the issue's opening argument |
| The sealer reads `CONTRIBUTING.md` for the command | the sealer judges prose, and a wrong reading is a seal over the wrong command; judging is the one thing #30 says it does not do | rejected (Q2) |
| The sealer returns the cell value and the orchestrator writes it | no durable trace of the sealer at all, and the reach-back is one more thing an orchestrator forgets — five such were forgotten on one branch | rejected (Q3) |
| Preload `verify` into the sealer | 35 KB per spawn for four conditions the definition states in four lines; #292's meter is what made this a number | rejected (Q5) |
| Run the suite at base on every gate | measured waste in `verify` §*The broad gate*: a 19,000-test suite run serially for a baseline before any failure existed | rejected (Q6) |
| A seven-row crown | superseded inside the issue by the fleur with the panel; the checklist names the fleur's chart | rejected (Q1) |
| Edit contract §2 in this work item | #120's, and its pin phrase would move outside its own work item; the flow orders #120 last on purpose | rejected (Q4) |

## Phases

Vertical slices — each phase ends with something runnable and verified. One
smith spawn per phase; this table and `phases/phase-N.md` are the handoff
between them.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `skills/verify/scripts/seal_stamp.py`: the chart as data, `build(scale)`, the colour row writer emitting at transitions, the letter twin, `letter(rows)`, `beside`, `stamp(rows, scale, shape)`, the failure form `not_sealed(tree, base, failures)`, and `pick_shape(stream)`; `bin/seal-stamp` + `.cmd` for a person to see it (`--shape`, `--scale`). `tests/test_the_seal_is_taken_once_by_the_sealer.py` part 1: twin and block dimensions equal; colour sequences per row < cells; panel rows and blanks; 0.75 accepted, 0.5 refused; `not_sealed` has no disc | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py tests/test_a_script_says_which_interpreter_it_needs.py tests/test_no_real_identifiers.py -q`; each case seen red first; `bin/seal-stamp --shape` run and read | `205ac78` |
| 2 | `skills/verify/scripts/broad_gate.py` + `bin/broad-gate` + `.cmd`: the `Broad gate` row read from `seal/config.md` (refused when absent, exit 2), the repository command then the four plugin checks in order, exit codes read directly, outputs kept, the reactive base comparison in a scratch worktree, the stamp on success and `NOT SEALED` on failure, `--record <item>`; `round_record.py seal` (last record's cell alone; refuses `Needs a fix: yes`, unchecked `Pass`, a premature SHA); `templates/config.md`'s new section; `skills/config/SKILL.md`'s fourth row; `seal/config.md`'s row here. Tests part 2: S1–S4 on fixture repositories driven from Python (§8) | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_record_is_generated.py tests/test_the_settings_have_a_front_door.py tests/test_the_mode_is_a_row_and_a_command.py tests/test_the_pull_request_language_is_the_repositorys.py -q`; each case seen red first; the real repository: `bin/broad-gate --base origin/release/v0.10.0` run once at the phase's head and its output read — this is a narrow verification of the command, not the work item's gate, which the sealer takes after the rounds | `0c04bc3` |
| 3 | `agents/sealer.md`; `agents/smith.md` and `agents/warden.md` name the owner and carry the probe sentence; `skills/code-review/orchestration.md`, `skills/verify/SKILL.md`, `docs/review-chain-spec.md`, `docs/review-handoff-protocol.md`, `CONTRIBUTING.md`, `bin/test`'s comment, `templates/sdd-round.md` name the sealer; both READMEs' tables and diagram; the two pinned sentences re-pointed and seen red; tests part 3: S6, S7 | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_every_agent_reads_the_contract.py tests/test_a_moved_rule_leaves_its_definition.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py tests/test_chain_hooks_hardening.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py tests/test_broad_gate_rule.py tests/test_the_rules_have_one_owner.py tests/test_docs_line_wrap.py -q`; `payload-meter --agent sealer` run and read (the fourth agent's payload) | `d515213` |
| 4 | `changelog.md`, `seal/ledger/<id>.md`, `overview.md`, the tick in `docs/flow.md`, the phase records complete, the narrow verification of every module the branch touched; hand to the review chain | `bin/test <every touched module> -q`; `evidence-check --ledger 'seal/ledger/<id>.md' --reverify .` then `evidence-check .` read unscoped; `survivor-check --range <base>..HEAD` read; `rider_check.py` | `26f5277` |
| 5 | The five items `phases/phase-4.md` carried. `round_record.py seal` drops its `Needs a fix` refusal, which made a CAPPED run unsealable, and the `Pass` message says which row it does not read; *after the rounds settle* becomes the last record's `Pass` box in `skills/verify/SKILL.md` and the four carriers that act on it; the warden's opening names the review mark; the rule that one seal is final is stated by `skills/verify/SKILL.md`, linked from `agents/sealer.md` and `agents/warden.md`, and takes a row in `tests/test_the_rules_have_one_owner.py`; every bare instance of the word names whose, swept by `tests/test_one_word_one_meaning.py`'s sixth word; the general rule goes in `skills/writing-style/SKILL.md` with a link from `CLAUDE.md`; #331 takes a row in `docs/flow.md`'s 0.10.1 | `bin/test` over the ten modules the diff can break; each of the twelve new cases seen red first, against code and documents restored from held bytes; `survivor-check` over `0eae75b..HEAD` **and** `origin/release/v0.10.0...HEAD`; `evidence-check .` read unscoped | `bf16087` |

**Why this order.** The stamp first because it depends on nothing and the
gate prints it. The gate second because the definition's whole procedure is
the command, so the command has to exist before the agent that runs it. The
definitions and documents third, once there is a command to name. Records
last.

**Every phase commits.** This branch squashes into `release/v0.10.0` and
`routing.md` is on disk, so the review arm of the commit gate is silent.

**Status is empty, or the commit that closed the phase.** Re-read after any
rebase.

## Verification scope, per phase

Narrow and often, broad once. Each phase runs the modules its own diff can
break, named in the table. **No phase runs the full suite, repository-wide
lint or a typecheck** — and phase 2's one real-tree run of `broad-gate` is
the command being verified as a command, at that phase's head, not the work
item's gate; the work item's gate is taken by the sealer once the last
round record's `Pass` box is checked — phase 5's wording, and the first time
the sealer does its job on the branch that creates it.

## Operational impact

- **A new agent, `sealer`, and two new commands on every user's PATH**,
  `broad-gate` and `seal-stamp`, plus a third `round_record.py` subcommand.
  The release moves the version.
- **A new `seal/config.md` row, `Broad gate`.** A repository without it gets
  a refusal from `broad-gate` naming the row, and nothing else changes — the
  orchestrator's own gate as it stands keeps working until the row exists.
- **Contract §2 and the sealer's definition disagree until #120 lands**, on
  the same release branch, before the release ships. The definition says so.
- **No migration, no new environment variable, no new dependency.**
- **Prompt budget: zero.** The sealer asks nothing; a missing row is a
  refusal with the row's name, not a question.
