# Implementation Plan: a changelog fragment a fix range left behind is named (#797)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-05 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

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

One notice-only arm in `chain_check.py` names every commit after the build that
changed a behaviour path after the work item's `changelog.md` last changed.
One rule, owned by a new section of `docs/the-record-layout.md`, says such a
commit brings the fragment along; the smith's definition, the implement skill
§5 and the review orchestration link to it. `spec.md` §*The measurement* is
why it prints rather than refuses.

## Technical context

- `skills/code-review/scripts/chain_check.py#main` — the per-declaration loop.
  The new arm is called beside the record walk for a `through the review
  chain` declaration, after `records` is known, and its notices join
  `notices`. `#pact_notices` is the shape to copy: findings are notices only
  and the exit status is untouched.
- `chain_check.py#fix_range` and `FIX_RANGE_RE` already read and resolve a
  record's `Fix range`; reuse them rather than re-parse (a second reader of
  one row is the split this file's docstrings keep closing). `#resolves_to`,
  `#field`, `#table_rows`, `#read_record` and `TARGET` give round 1's
  `Target SHA`. `#local_root` exists, but the arm needs no mode test: a
  fragment git does not track at HEAD is the silent case, and local mode
  tracks none.
- `skills/code-review/scripts/round_record.py#run_check` (end of `close` and of
  `seal`) runs `chain_check --worktree` and prints its output — the close-time
  and seal-time moments come with no change to the generator.
  `round_record.py#under_tests` and `TESTS_DIR` are the test-path predicate to
  match; `chain_check` cannot import `round_record` (the import runs the other
  way), so the arm states the same predicate and its docstring names the twin.
- `skills/verify/scripts/broad_gate.py` is NOT touched. Arm 4 runs
  `chain_check` and a passing `--preflight` prints one line, so the notice
  reaches a person through the `seal` output that follows, not the preflight.
- Tests: `tests/test_chain_check_at_the_pull_request.py` holds the repository
  fixture (`_build_chain_repo`, `repo`) a new module can import; drive git
  from Python (contract §8).
- Box 2's carriers and their pins: `agents/smith.md` (fix-pass paragraph,
  around the `## Fixes` table rule), `skills/implement/SKILL.md` §5,
  `skills/code-review/orchestration.md` §*Orchestrator: a fix pass resumes the
  implementer*; `tests/test_the_rules_have_one_owner.py` `RULES` (rule 14 is
  the last number today), `tests/test_no_passage_is_pasted_into_a_second_file.py`
  (a link shares fewer than 25 consecutive words with its owner),
  `tests/test_one_word_one_meaning.py` (the word `seal` keeps one meaning —
  the new sentences have no reason to use it), and whatever else under
  `tests/` names those three files: `grep -l` before phase 2's edits.

**What breaks in six months.** A repository whose tests live outside a
`tests` directory sees a notice for a test-only fix; one line, no stop. A
behaviour change made only inside a merge commit's conflict resolution is not
named. And the notice is read by whoever reads `close`, `seal` and CI
annotations: an orchestrator that reads none of them ships the lagging
fragment exactly as before — the rule in box 2 is the half that reaches the
writer before the commit.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Refuse in `chain_check` (exit 1) where the fragment is behind | Measured: 24 of 42 branch tips would fail, at least 9 of them for a fragment that needed no change; each is a stop in an unattended run, and the honest answer has no spelling short of a new record field | rejected |
| A notice per fix range — the ticket's literal reading | 11 of the 66 flagged ranges had the fragment brought along in a later range or before the squash; a per-range notice keeps printing for them on every CI run after the fact. The per-item question clears itself the moment the fragment changes | rejected; ranges are kept only to attribute each named commit |
| The arm in `round_record.py close` | runs only at a close, so a fix written after the last round and an integration commit — two of the three kinds #797 names — are never read; CI never runs it | rejected |
| The arm in `broad-gate --preflight` | a passing preflight prints one line, so the notice would go to a `--keep-output` file nobody opens; it does not run at a close; it shares `broad_gate.py` with sibling C (#789) | rejected |
| A positive list of behaviour directories (`hooks/`, `skills/*/scripts/`, `bin/`, `templates/`, `docs/`) | `chain_check` ships to every opted-in repository and the list is this repository's layout; the ticket's own list had already omitted `bin/` and `agents/` | rejected for "outside `seal/` and outside a `tests` directory" |
| An acknowledgment row in the round record (`Changelog | unchanged — <why>`) that silences an honest notice | a new record field, a template change, a generator change and a checker arm, to silence a line that stops nothing | deferred — revisit only if a measurement shows the notice being ignored |
| A check at the release's gather | the feature branches are squashed by then and none of their commits resolve | rejected |
| **One notice-only arm in `chain_check`, per work item, post-build commits after the fragment's last change, attributed to rounds** | the limits in *What breaks in six months* above | **chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The arm in `chain_check.py` (S1–S8, S10) and the section of `docs/the-record-layout.md` that owns the rule and that the notice names, ending `Enforced by:` the arm and its cases; the module docstring's *What it reads* row | a new test module, every case seen red before the arm or with its condition reverted (contract §15); `tests/test_chain_check_at_the_pull_request.py` and the `docs/` hygiene modules that read the touched files | 1b1a1ed2 |
| 2 | The three links (`agents/smith.md`, `skills/implement/SKILL.md` §5, `skills/code-review/orchestration.md`) and a `RULES` row in `tests/test_the_rules_have_one_owner.py` (S9) | `tests/test_the_rules_have_one_owner.py` seen red with the owner's sentence removed; `tests/test_no_passage_is_pasted_into_a_second_file.py`, `tests/test_one_word_one_meaning.py`, and every other module that names one of the three files | 8b83fbcf |
| 3 | This item's ledger fragment rows, `overview.md`, and its `changelog.md` fragment | `evidence-check --strict .` narrowed to this item's fragment; `tests/test_no_real_identifiers.py` | 1752792c |

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

None a deployer must act on: no flag, no record field, no template, no
migration. CI, `round-record close` and `round-record seal` print one more
kind of notice for a chain work item, at one `git log` per declared item, and
no exit status moves.

**This item's own rounds are the first the arm reads, and only in CI.**
`round-record` on the PATH is the installed plugin (0.18.2), which has no arm,
so a close run through it prints nothing new; the pull request's CI runs the
tree's `chain_check` and does. An orchestrator that wants the notice at this
item's own closes runs the tree's `skills/code-review/scripts/round_record.py`
instead. This item's fix passes follow its own rule either way: a fix that
changes what the arm prints updates this item's `changelog.md`.
