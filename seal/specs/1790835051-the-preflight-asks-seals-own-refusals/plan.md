# Implementation Plan: the preflight asks seal's own refusals

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-01 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

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

`round_record.py seal` gains `--check`: every refusal it raises before the
write, then one line and exit 0 with nothing written and no chain check.
`broad-gate --preflight` runs it, after the record arms, for the work item
declared for the checked-out branch, keeps its output as `seal.txt` and
names `seal` under `PREFLIGHT FAILED` when it refuses. The orchestrator
types the same command as today. `seal` without the flag, the sealer's run,
and `agents/sealer.md` are unchanged.

## Technical context

**`seal` today.** `skills/code-review/scripts/round_record.py#seal` (line
4322 at `e83db346`): `where(args)` → `seal_home(routing, item, rounds)` (a
`Refused` for a chain declaration with an empty `rounds/`; `(None,
broad-gate.md)` for `straight to the PR`) → the record read → six `raise
Refused` sites in order: `Pass` box count, `Pass` unchecked, `Fixes checked
by` outside `no fixes to check` (both branches of `why`), no SHA-shaped
word, the SHA not resolving, `is_ancestor(root, ran_at, reviewed)` → then
`kept_broad_gate`, `write_record`, the `round-record: sealed …` print, and
`return run_check(root, baseline)`. The docstring counts the refusals by
`raise` site ("Six refusals … the number is the `raise Refused` sites in
this function"); an early `return 0` after the ancestry loop adds no site.
`main` maps `Refused` to `round-record: <why>` on stderr and exit 2.
`argparse` for `seal` is at `main` (line 4568): `--item`, `--broad-gate`,
`--root`, `--baseline`; `--check` is a `store_true` beside them.

**The gate's call.** `skills/verify/scripts/broad_gate.py#seal_record` (line
2690) builds the argv `[py, RECORD, "seal", "--item", item, "--broad-gate",
f"{tree} against {base}", "--root", root, "--baseline", base]` and runs it
through `run("seal", …)`, which keeps `<keep>/seal.txt` opening `$ <argv>`
and `exit <code>`, and reads the exit code off the subprocess. The full run
reaches it only after every check is green (`gate`, line 2922
`if item is not None:`), and tells its two non-zero endings apart by the
`round-record: sealed` prefix — which is why `--check`'s success line must
not carry that prefix.

**The preflight branch of `gate()`** (`def gate` at line 2745): `args.record`
with `args.preflight` is refused at line 2803 before anything runs, so `item`
is `None` throughout a preflight. The arms run into `checks`; `failures` is
built by the one loop over `checks.items()` (line 2897); then `if failures:`
(line 2907) prints `not_sealed`'s form with its head replaced by
`PREFLIGHT_FAILED` (line 2915) and returns 1, else `PREFLIGHT_PASSED` and 0. The
ask goes between the loop and the `if failures:`, as
`failures.append(("seal", failure_lines(check)))` — `failure_lines` takes a
`Check`, which `run` returns, so `seal_record` returning `(code, text)` is
one option and returning the `Check` is another; the phase picks, and the
loop stays the one loop.

**Which readers constrain the shape**, all AST readers of `gate()`:
`tests/test_the_gate_names_every_step_ci_runs.py#arms_the_gate_runs`
collects every `checks[<NAME>] = run(...)` and
`::test_the_gate_runs_no_arm_the_partition_does_not_account_for` requires
each to be a `PARTITION` arm — so the ask is NOT written as
`checks[...] = run(...)` and gets no `PARTITION` row;
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py#failure_loop`
requires exactly one `for … in checks.items()` loop;
`tests/test_the_gate_asks_the_range_ci_will_ask.py::test_the_gate_reads_the_given_base_exactly_once`
counts `args.base` reads (one). `record_arms()` in the sealer module reads
the same assignments and
`test_a_green_tree_preflights_green_and_seals_nothing` asserts the kept
`.txt` files equal exactly those arms — on the undeclared `build_repo`
fixture, where nothing is asked and no `seal.txt` is written, so it stays
green by construction and is the case that shows S8's skip.

**The branch → item key.** `hooks/routing.py#item_dir(root, branch)` (line
355) returns the directory of the ONE declaration whose `Branch` row names
`branch`, or `""` for none or two; `declarations(root)` reads the home
`optin.home_at(root)` finds, so local mode works. `broad_gate.py#branch_name`
(line 343, #666) already gives `gate()` the branch (`None` detached). Loading
`routing` from the gate: `round_record.where` does it as
`load(chain.ROUTING, "specseal_routing")`, and `broad_gate.sealed_record`
already loads `round_record` as `generator` — so either
`generator.load(generator.chain.ROUTING, …)` or a direct
`load(os.path.join(PLUGIN, "hooks", "routing.py"), …)`; `hooks/routing.py`
imports `optin` by plain name, which `chain_check.load` arranges for, so
reuse that loader rather than a second one. The phase names which in
`phases/phase-2.md`.

**The fixtures.** In `tests/test_the_seal_is_taken_once_by_the_sealer.py`:
`declared(repo)` writes the chain declaration naming `feature`, the branch
`build_repo` leaves checked out, so `item_dir(root, "feature")` resolves to
`<repo>/seal/specs/1799000000-a-sealed-work-item`; `fixed_but_unread_item`
is #535's generated shape; `settled_item`, `capped_item` are the passing
shapes; `generate(repo, 1, OPEN_ROW, "no")` is the unchecked `Pass`;
`declaration(review="straight to the PR")` is the direct home; `run_seal(repo,
value, extra)` passes extra flags; `run_gate(repo, "--preflight", keep=…)`
and `set_row` drive the preflight; `read_bytes`, `values_files`,
`no_seal_line` are the no-write assertions. The ask's `--broad-gate` value in
a preflight is `"<short HEAD> against <base commit>"`, so the ancestry refusal
fires only where `Target SHA` descends from HEAD (S5): a commit made on a
side branch from HEAD, the feature branch switched back to, and
`generate(repo, 2, …, target=<that sha>)` — `build` refuses only a target
that does not resolve.

**The documents.** `skills/code-review/orchestration.md` lines 524–553: the
bold step at 526–528 and the paragraph *The preflight is yours* at 541–553;
`tests/test_broad_gate_rule.py::test_the_orchestrator_runs_the_preflight_before_it_spawns_the_sealer`
reads the section by phrase and index (presence pins, so sentences added
inside are safe). `skills/implement/orchestration.md` line 559 is the acts
row whose `Grounds` cell is free text; line 40 is the order line, pinned
verbatim by `tests/test_the_rules_have_one_owner.py:736` — do not touch.
`skills/verify/SKILL.md` lines 400–402 and `templates/config.md` lines
167–169 carry the preflight sentence; `test_the_skill_says_the_preflight_is_not_the_broad_gate`
and `test_the_example_row_goes_lint_first_and_the_arms_are_not_listed_by_hand`
pin them by presence. `seal/specs/1790815611-…/changelog.md` lines 8–10 carry
the sentence the appended one answers.

**The ledger.** `evidence-check --strict .` is the preflight's own `ledger`
arm and this repository's rows anchor on the units this work edits.
`round_record.py#seal@0cfc9d4e` is cited by eleven rows (0.10.0 S10 and S13,
0.11.5, 0.13.1 C3, 0.15.0 A5 and A9, 0.15.1 N4, 0.16.0 G2 among them);
`broad_gate.py#seal_record@4d582ed3` by 0.10.0 S12;
`broad_gate.py#gate@51ce700f` by fifteen rows across 0.10.0, 0.12.0, 0.12.2,
0.15.4, 0.15.7 and the 1790815611 fragment (P1–P6) — 26 rows in eleven files
at `e83db346` (`grep -rn` over `seal/ledger.md`, `seal/releases/*.md`,
`seal/ledger/*.md`, counted 2026-10-01).
Every one drifts. The rule is `CLAUDE.md` §*Repo rule — a change writes
fragments*: re-read each against the edit, correct the claim in place with a
`Corrected 2026-10-01` note where the edit made it false, and re-stamp with
`evidence-check --reverify --checked 2026-10-01`, naming every row. Read
S12's claim with care — *`broad-gate` reads BOTH of `seal`'s non-zero exits
as unsealed* stays true of the full run and says nothing about `--check`.

**Failure scenario of the chosen approach, in six months.** A refusal is
added to `seal` after the ancestry loop — say a check that the `--broad-gate`
base matches the declaration's branch — and lands AFTER the `--check` return.
`seal` refuses it at the sealer, after a suite, and the preflight passes it:
exactly the gap this work closes, reopened one refusal at a time. What
catches it: the `--check` return is the LAST statement before
`kept_broad_gate`, and `seal`'s docstring says the early return sits after
the last refusal; a structural case can hold that — the `return` under
`args.check` is the statement immediately before the `kept_broad_gate` call
in `seal`'s body, read as a syntax tree the way `failure_loop` reads
`gate()`. Phase 1 plants it, so a refusal added below the return is red
rather than quiet. Second scenario: a session renames the fixture branch or
`declared()`'s `Branch` row and the preflight cases go green by asking
nothing — S6 and S3 both assert `seal.txt` exists, so a skipped ask is a
missing file, never a pass.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Lift #638's `--preflight --record` refusal: `--record <item>` under `--preflight` means *ask, do not write* | The documents, the changelog and ledger row P4 say the pair is refused, one release after they shipped. A session typing the command as every document says today — without `--record` — asks nothing and is told nothing, so the check arrives only when remembered. The guarantee *a preflight can never seal* moves from a refusal at parse time to `--check` being honoured in the child | rejected |
| B. A second flag, `--item <item>` or `--ask <item>`, valid only with `--preflight` | Two flags that take the work item directory, one named for the write and one for the ask — a second name for one thing, and the same forgettable-flag cost as A | rejected |
| C. Derive the item from the checked-out branch's declaration, `routing.item_dir(root, branch)` (chosen) | Where no single declaration names the branch the ask is skipped, and a skipped ask is one stderr line a reader has to see. Bounded: the commit gate refuses a commit on an undeclared branch without `[no-review]`, so a branch that reaches the preflight with no declaration is one no sealer is coming for; two declarations naming one branch already make the chain arm refuse. Pinned: S8 asserts the line and the absent `seal.txt` | chosen |
| D. Run the chain arm a second time under a READY payload, which fails `Pass` beside `nobody` and a premature `Broad gate` SHA | A ready payload also fails `Broad gate | not yet`, which is the honest cell before the sealer runs, so every preflight fails; and it never reaches the `seal_home` refusal, which lives in the generator | rejected |
| E. Extract the refusals into a predicate `seal_refusals(...)` and call it in process from the gate, as `sealed_record` calls `seal_home` | Also the same statements; what it loses is `run`'s kept file and an exit code read off a subprocess (§1), and it adds a second caller of `where` inside the gate that must swallow nothing while `sealed_record` swallows everything — two loaders of one module with opposite error rules in one file. `--check` keeps `seal`'s CLI the one surface, which is what the sealer, the gate and the cases already drive | not built |
| F. Make the ask a `checks[SEAL_NAME] = run(...)` arm | `test_the_gate_runs_no_arm_the_partition_does_not_account_for` requires a `PARTITION` row, and the ask mirrors no CI step; `test_a_green_tree_preflights_green_and_seals_nothing` would demand `seal.txt` on an undeclared fixture | rejected |
| G. Reorder the full gate so `seal`'s refusals come before the suite | The sealer's run and its report change; #638 rejected reordering for the *every check that failed* property, and the preflight already runs first | rejected |
| H. Leave #638's changelog fragment as written | The 0.17.0 release section would say in one entry that `seal`'s refusals still reach the sealer and, in the next, that they do not; `gather_changelog.py` concatenates fragments in id order and never re-reads one. One appended, dated sentence in a fragment nobody has read yet is the proportionate correction (`docs/the-broad-gate.md` §*A document that its own work item's fixes disproved is corrected in the same work item*, applied one item over) | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `round_record.py seal --check`: the flag in `main`, the early `return 0` after the ancestry loop with its one line, the header and `seal`'s docstring; S1's four refusing cases and S2's three passing cases in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, each red first (the flag absent: argparse exit 2; `--check` ignored: the cell written); the structural case holding the `--check` return as the last statement before `kept_broad_gate` | the new cases; every `test_seal_*` and `test_the_gate_*` case of the sealer module green; `tests/test_the_record_is_generated.py` and `tests/test_the_fixes_close_the_record.py` green unchanged | 9b9220ff |
| 2 | The preflight asks: `seal_record(..., check=True)`, the item from `routing.item_dir(root, branch)`, the `seal` entry in `failures`, the stderr line for the record asked and for none asked, `PREFLIGHT_TAIL`, the docstring; S3, S4, S5, S6, S8 in the sealer module, each red first against phase 1's tree (S3 and S4 exit 0; S6 and S8 missing the line), then red under the ask dropped and under `--check` dropped from the argv (the cell written, S6's byte comparison); the wall clock measured once (Q3) | the new cases; S7's three AST modules and `test_a_green_tree_preflights_green_and_seals_nothing` green unchanged; S9, S10 green unchanged; the whole sealer module | 569db6af |
| 3 | The documents: the preflight paragraph in `skills/code-review/orchestration.md`; the `Grounds` cell in `skills/implement/orchestration.md`; one sentence each in `skills/verify/SKILL.md` and `templates/config.md`; the appended sentence in `seal/specs/1790815611-…/changelog.md`; pins S11 in `tests/test_broad_gate_rule.py`, red first against the unedited documents | the new cases; `tests/test_every_orchestrator_act_names_its_delivery.py`, `tests/test_the_rules_have_one_owner.py`, `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py`, `tests/test_broad_gate_rule.py` whole | 6c690d51 |
| 4 | The records: `seal/specs/<id>/changelog.md` (`### Added` for `--check` and the ask, `### Changed` for the tail), `seal/ledger/<id>.md` with one row per scenario the build verified, `overview.md` with S12's empty diff, Q3's number and the drifted-row re-read recorded, `phases/phase-N.md` per closed phase; the re-read and re-stamp of every row the edits drifted (§*Technical context*, *The ledger*), claims corrected in place where false; a `survivors.md` row where `survivor-check --range e83db346...HEAD` reports wording this branch removed still standing | `evidence-check --strict .` exit 0 over the whole ledger; `survivor-check`; `tests/test_no_real_identifiers.py`; `tests/test_a_rider_reaches_its_file.py`; `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview` | |

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

- A new flag on a shipped subcommand, additive: `round-record seal` without
  `--check` runs exactly as before, and the sealer's `broad-gate --base <base>
  --record <item>` is unchanged.
- `broad-gate --preflight` gains one subprocess after the arms where the
  branch has a declaration (about the cost of one `round_record.py` start;
  measured once, Q3), one kept file `seal.txt`, one stderr line, and a longer
  `PREFLIGHT_TAIL`. A session reading the head's first words sees nothing new.
- The direction is *block more, earlier*: a preflight that passed #535's and
  #456's shapes now fails them, where the sealer's run would have refused them
  after the suite. Nothing that the sealer would have sealed is refused,
  because the preflight asks the sealer's own subcommand.
- Nothing under `hooks/`, no workflow step, no new dependency, no new
  environment variable, no `PARTITION` row. CI never runs the preflight.
- The 0.17.0 release notes carry #638's entry with one appended sentence and
  this item's entry after it.
