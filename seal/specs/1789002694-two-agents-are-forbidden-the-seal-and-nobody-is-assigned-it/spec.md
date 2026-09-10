# Feature Specification: two agents are forbidden the seal and nobody is assigned it

<!-- seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #30. The second work item of 0.10.0: the fourth agent, `sealer`, and
the rule that the one broad run is taken by it, once, after the rounds settle.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The sealer asks nobody anything: it runs, reads, reports, and writes one cell. A refusal names what to write; a failure names what failed |
| `CLAUDE.md` §*Verification Scope* and `skills/verify/SKILL.md` §*Scope — cheap and often, broad and once* | The gate fires once, after the rounds settle; a run followed by an edit was spent. The sealer is the owner that rule never named |
| `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare against the base* | The comparison is reactive: a baseline is taken once a failure appears, for the failing tests only. The sealer reports both facts and decides neither |
| `skills/verify/SKILL.md` §*The four conditions* (the Seal Test) | The sealer's whole procedure: name the command before running it, show the check can fail, bind the result to a tree state, label every claim |
| `skills/code-review/orchestration.md` §*Orchestrator: the pull request opens before round 1* — *The last record's `Broad gate` cell is read at a READY pull request* | The cell the sealer writes, and the moment: after the last record's `Needs a fix: no`, before the draft goes ready |
| `docs/review-chain-spec.md` §*The last round verifies* — *Then the broad gate runs once, and the change opens as a pull request* | The step this work gives an owner |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a failure direction, a prompt budget of zero, platform honesty — the stamp has two encodings for the last of these |
| #30 §*The rule, once it has an owner* and §*What it prints* | The rule's wording, and the stamp: on success only, the numbers beside the disc as data, colour at transitions, the chart in the repository, an ASCII twin |
| #30's comment of 2026-09-03 13:22 — *"Records" means three different things* | The sealer writes ONE row and judges nothing; the order is record, rounds, then seal — the seal stamps a tree state, never a row |
| #120 and its comment | Contract §2 forbids the sealer's one act and §6 its one write. #120 settles both before the release ships; this work ships the sealer under the contract as it stands and says so in the definition |
| `docs/flow.md` §*0.10.0 — the agent set* | The order: #292's meter · #30 · #84 · then #120. This is the second |

## Scope

**In.**

1. **The stamp, as a module.** `skills/verify/scripts/seal_stamp.py`: the
   29×32 counted-stitch chart as module data (it lived outside the tree at
   `~/Documents/pixelart-fleur/chart.txt` and does not ship — this is the
   move #30's checklist asks for); the disc computed from it (`hypot` for the
   bands, `sin` for the rope's twist), so it cannot be off centre; a panel
   beside it driven by `(label, value)` rows with `None` for a blank; colour
   emitted at transitions only; and an **ASCII twin** — the same disc as
   letters (`o O` rope, `l m` wax, `G W y Y` the lily's golds, `.` field),
   the same width and height — chosen when stdout is not a UTF-8 terminal,
   or on `--shape`. `scale` is a parameter with 0.75 as the floor the issue
   measured. **Printed on success only**: the failure form is the word `NOT
   SEALED`, the tree and base, and the failing checks with their first
   lines — no drawing.
2. **The gate, as a command.** `skills/verify/scripts/broad_gate.py` with
   `bin/broad-gate` and its `.cmd` twin. It runs, in order, the
   repository's own broad command from `seal/config.md`'s new row `Broad
   gate` (a shell command line — for this repository `bin/test -q -n auto
   && uvx ruff check . && uvx ruff format --check .`), then the plugin's own
   checks every opted-in repository carries: `evidence-check --strict .`,
   `unverified-check --baseline <base> seal/specs/`, `chain_check.py
   --baseline <base>`, `survivor-check --range <base>...HEAD` with every
   `seal/specs/*/survivors.md` as `--exempt`. It reads each exit code
   directly (§1), keeps each output in a file, and on success prints the
   stamp with the panel: `tree`, `base`, `suite` (the counts read from the
   repository command's last line), `lint`, `ledger` (`N ok · 0 broken`),
   `chain` (`exit 0`), `rounds` (the count of `round-N.md`). **A missing
   `Broad gate` row is a refusal, not a default**: the sealer says which
   row to write and exits 2 — a seal taken over nothing is the counterfeit
   `verify` names. **On a failing test, the comparison is reactive and
   mechanical**: the failing test files are re-run at `<base>` in a
   scratch worktree of the repository (`git worktree add`, removed
   afterwards), and each failure is reported as `new` or `failing on base
   too`. The sealer decides nothing about either; both words go in the
   report and the reader acts.
3. **The one write.** `round_record.py seal --item <dir> --broad-gate
   '<sha> against <base>'` — a third subcommand that sets the LAST record's
   `Broad gate` cell and touches nothing else; it refuses while the last
   record's `Needs a fix` reads `yes` (the rounds have not settled) and
   while `Pass` is unchecked, and it refuses a `--broad-gate` whose SHA the
   record's `Target SHA` descends from (the run was spent before the round
   it seals — the same test `chain_check.broad_gate` applies). `broad-gate
   --record <item>` runs it on success. `close --broad-gate` stays for the
   case where fixes and the gate land together.
4. **The agent.** `agents/sealer.md`, opening with the contract paragraph
   every definition carries (`tests/test_every_agent_reads_the_contract.py`
   holds it to identity), `skills:` listing `agent-contract` and nothing
   else — the sealer's procedure is the command, so no skill body rides its
   spawn. It reads nothing of the work item: not `spec.md`, not the code. It
   runs `broad-gate --base <base> --record <item>`, reads the full output,
   and returns it with the three labels (`executed` for every check, and
   `unverified` for nothing — a sealer that could not run a check reports
   `NOT SEALED`). It judges nothing: a failure is reported with its lines and
   its `new` / `failing on base too` word, never with a cause or a fix. Its
   one durable write is the cell above, named in the definition as its own
   exception to §6 — the shape §6's last paragraph already prescribes
   (*an exception is one agent's, and it is named in that agent's
   definition*). And the definition says plainly that §2 as it stands
   forbids its one act, that #120 is where §2 is rewritten before this
   release ships, and that until then the sealer's definition is the
   narrower document and the contract the wider one.
5. **The rule, with its owner, in the two definitions that used to forbid
   and not assign.** `agents/smith.md`'s *the full suite is the
   orchestrator's, once, after the rounds* and `agents/warden.md`'s copy
   read *the sealer's, once, after the rounds settle*, and both gain the
   coverage-probe sentence: *a coverage probe — nothing in the suite catches
   this — is a different act: run it, and report it as a probe, never as a
   seal*. The warden's *You are also what can say the gate has come due*
   paragraph names what comes due: the sealer's spawn.
6. **Who spawns the sealer, and when — in the documents the orchestrator
   reads.** `skills/code-review/orchestration.md`'s *The last record's
   `Broad gate` cell is read at a READY pull request* paragraph: the
   orchestrator spawns `sealer` after the last record's `Needs a fix: no`
   and before the draft goes ready, with the base and the item; the sealer
   writes the cell. `skills/verify/SKILL.md` §*The broad gate* names the
   sealer as the owner and the Seal Test as its procedure. `docs/flow.md`
   already places `sealer` in the order inside a ticket; the row's box is
   ticked. `docs/review-chain-spec.md`'s *Then the broad gate runs once*
   names who. `docs/review-handoff-protocol.md:503`, `CONTRIBUTING.md:18`
   and `bin/test`'s comment say *the sealer's* where they said *the
   orchestrator's* — three sentences two test modules pin
   (`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:153, :764`),
   re-pointed and seen red. `templates/sdd-round.md`'s `Broad gate` comment
   names the subcommand that writes it.
7. **The README pair.** A fourth row in both editions' agent tables
   (`sealer` · `agent-contract` · runs the one broad gate, writes the cell,
   judges nothing), the chain diagram's `broad gate` line names the sealer,
   and `payload-meter`'s row is untouched. `tests/test_chain_hooks_hardening.py`
   derives the preloaded-skill counts from `agents/*.md`, and a definition
   listing only `agent-contract` changes none of them — confirm rather than
   assume.
8. **The tests.** `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the
   stamp module (success only; the twin's dimensions equal the block form's;
   the number of colour sequences in a row is below the number of cells;
   the panel renders its rows and blanks; 0.75 is the floor and 0.5 is
   refused), the gate (refuses without the row, exit 2; a failing repository
   command → `NOT SEALED`, exit 1, no disc, the check named; a passing run
   → the disc, exit 0; the reactive base comparison on a fixture repository
   whose base already fails one test → `failing on base too`), the
   subcommand (writes the last record's cell alone; refuses on `Needs a
   fix: yes`, on an unchecked `Pass`, and on a premature SHA), and the
   definitions (the sealer opens with the contract line — the identity case
   covers it; the two owner sentences and the probe sentence in `smith.md`
   and `warden.md`). Every case seen red first.
9. `templates/config.md` gains the `Broad gate` row's section (what it is,
   what an absent row means — a refusal, and why not a default); the
   `config` skill shows the row with the other three; `seal/config.md` here
   gets the row.
10. `changelog.md`, `seal/ledger/<id>.md`, `overview.md`, a
    `phases/phase-N.md` per phase, and the tick in `docs/flow.md`.

**Out.**

- **Rewriting contract §2 and §6.** #120's, and it lands last in the
  release; this work ships the sealer's definition stating the exception
  in the shape §6 already permits and naming the ticket that settles §2.
- **`agents/scribe.md`.** It carries no broad-gate sentence.
- **A typecheck step.** This repository runs none, and the row's command is
  the repository's to write; the plugin's own checks are fixed.
- **Colour in an agent's report.** The sealer's returned text carries the
  ASCII twin; the colour form is for a person's terminal, printed when
  `broad-gate` is run there.
- **The `flow-measurement` log posting.** The sealer's segment is measured
  by the orchestrator like every other segment; nothing here changes that.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 sealed | Given a repository with the `Broad gate` row and a green tree, when `broad-gate --base <base>` runs, then every check runs in order, each exit code is read directly, and the disc prints with the panel carrying tree, base, suite counts, lint, ledger, chain, rounds; exit 0 | a fixture repository with a one-test suite and a config row; the real repository run once at the branch head, output read |
| S2 not sealed | Given one failing test, when it runs, then `NOT SEALED <tree> against <base>`, the failing check and its first lines, the `new` / `failing on base too` word per failing file, no disc; exit 1 | the fixture with a planted failure; the fixture with the failure also at base |
| S3 no row | Given no `Broad gate` row, then the sealer names the row to write and exits 2 without running anything | the fixture without the row |
| S4 one write | Given the last record reads `Needs a fix: no` and `Pass` checked, when `round_record.py seal` runs, then only the `Broad gate` cell changes; given `yes`, or an unchecked `Pass`, or a SHA the target descends from, then a refusal naming the reason and no write | a fixture item with two records; byte comparison of every other line |
| S5 the twin | Given stdout is not a UTF-8 terminal or `--shape` is passed, then the disc prints as letters with the same width and height as the block form; given colour, then a row's colour sequences are fewer than its cells | the module's cases over the rendered rows |
| S6 the owner | Given `agents/smith.md` and `agents/warden.md`, then each names the sealer as the suite's owner once, after the rounds, and carries the coverage-probe sentence; no definition carries §2's sentences verbatim | the new module; `tests/test_a_moved_rule_leaves_its_definition.py` green |
| S7 the fourth definition | Given `agents/sealer.md`, then it opens with the identical contract paragraph, lists `agent-contract` alone, names its one write and #120 | `tests/test_every_agent_reads_the_contract.py`, `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, `tests/test_chain_hooks_hardening.py` all green with the fourth file present |
| S8 nothing asks | Given all of the above, no new question reaches a person in any session | `grep -rn AskUserQuestion` over the new files returns nothing; the pull request body's prompt-budget line |

## Data & interfaces

**`broad-gate`** — `broad-gate --base <ref> [--root DIR] [--record <item>]
[--shape] [--scale 1.0] [--keep-output DIR]`. Exit 0 sealed · 1 not sealed ·
2 refused (no row, no repository, base does not resolve) — nothing ran on 2.

**`seal/config.md`** row — `| Broad gate | <one shell command line> |`. Run
through the shell from the repository root; the plugin's own checks follow it
and are not part of the row.

**`round_record.py seal`** — `seal --item <dir> --broad-gate '<sha> against
<base>' [--root DIR] [--baseline REF]`; runs `chain_check --worktree`
afterwards the way `new` and `close` do; commits nothing.

**The panel rows** — `("SEALED", "")`, `None`, `("tree", sha)`, `("base",
sha)`, `None`, `("suite", "N passed, M skipped")`, `("lint", "clean")`,
`("ledger", "N ok · 0 broken")`, `("chain", "exit 0")`, `None`, `("rounds",
"N")` — the shape the issue drew, and `seal_stamp.stamp(rows, scale, shape)`
returns the lines.

**`agents/sealer.md`** — frontmatter `name: sealer`, `skills: [agent-contract]`
in the block form the other three use; body: the contract paragraph, *what you
are* (runs the named commands, reads the full output, returns the verdict,
writes one cell, judges nothing), *the command*, *the one write and why it is
yours*, *§2 as it stands and #120*, *Report*.

## Open questions → questions.md

Anything a planner must answer lives in `questions.md`, not inline.
