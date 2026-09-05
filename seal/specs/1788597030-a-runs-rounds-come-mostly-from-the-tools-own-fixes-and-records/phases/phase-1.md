# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | aa5864b |
| Ran by | specseal:smith on fable-5.1 |

The `Ran by` value: the spawn prompt named neither the agent nor the model.
The agent is the definition this segment was spawned from, and the model is
what the harness's own system prompt states — *Fable 5.1* — transcribed
rather than decided. Neither half is the segment's idea of what it is.

## What this phase was asked

Build phase 1 of `plan.md` and only phase 1, on branch
`feat/161-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records`,
with routing answered and the question batch closed — ask nobody anything.

1. `skills/code-review/scripts/round_record.py` with the `new` subcommand,
   every cell from a source that is not prose: `Target SHA` from `--target`
   (verified to resolve), `Ran by` and `Broad gate` from flags, `PR` from
   `--pr` else `gh pr view` else `not yet opened`, `Fixes checked by` at the
   landing value `ORDER_FROM` requires, the two surface rows at `NOT_YET`,
   `Needs a fix` and `Loses a record or crashes` from what stands after the
   colon in the report's two lines (a report lacking either refused), the
   round paragraph verbatim, the three tables copied row for row (Verdicts
   required, the other two filled when absent), inherited coordinates from
   every earlier record's `Location` cells deduplicated, `Pass` ticked when
   no verdict is open, round N-1's `Fixes checked by` set to `round-N`, then
   `chain_check --worktree` run and its exit code returned. Loaded reader and
   constants the way `chain_check.py` does; a cell carrying `|`, a newline,
   or a comma in the two surface rows refused. No command line carries a
   commit.
2. `chain_check.py --worktree`: `read_record` reads the working tree,
   `changed` includes uncommitted changes, `round_records` lists working-tree
   files; CI keeps the default; a one-line mention beside `read_record`'s
   docstring.
3. `agents/warden.md` §Report carries the three tables in the record's own
   headers under `## Verdicts`, `## Executed probes`, `## Deferred`, then the
   two lines; one sentence saying the generator copies them; under the
   line-wrap width.
4. `tests/test_the_record_is_generated.py`: one case per field derivation on
   a fixture repository, the reach-back read back, the Pass tick, the comma
   and pipe refusals, the missing-lines refusal, `--worktree` seen red in both
   directions before the flag exists, the warden headers pinned against the
   generator's constants.

Coordinates handed over and opened: `templates/sdd-round.md:24-36` and
`:190-265`; `chain_check.py` `read_record:703`, `round_records:724`,
`changed:584`, `main:2662`, `checked_by:1375`, `fix_surface:1718`,
`stopping_floor:2348`, `pass_checked:1346`, `verdict_of:1166`, and the
constants at `:307-540`; `unverified_check.py` `visible:95`, `readable:155`,
`split_row:74`, `repo_root:458`, `show:515`; the last item's `round-4.md` and
`round-12.md`; `skills/code-review/SKILL.md:339-497`; `conftest.py`
`declare_routing:214`, `rounds_dir:245`. Every line number named resolved to
the unit it was said to name.

## What this phase found

**The landing value of `Fixes checked by` is two values, not one.** The
prompt named `nobody — the fixes are not yet written` and sent the segment to
`templates/sdd-round.md:77-103` and `fix_surface`'s docstring for the pending
states. Both say the same thing about the terminal record: *`no fixes to
check` beside a pending row … is not merely unrefused but wrong: a round that
commissioned no fixes will never have any, so not yet written is false the
moment it is written*. And `checked_by` refuses `nobody` beside a checked
`Pass` on the last record. So a generated record whose every verdict closes
without a fix word — the verifying round's own terminal shape, and the capped
run's — would be refused by the check the generator runs, on the value the
prompt named. The generator derives: a verdict open or closed on a fix word →
`nobody — the fixes are not yet written` and both surface rows pending; every
verdict closed without a fix word → `no fixes to check` and a bare `none`.
`overview.md` carries the divergence with both sides quoted.

**`chain_check` judges a local run as a READY pull request**, because
`pull_request_state` reads GitHub's event payload and outside a workflow there
is none — and a ready pull request with an unchecked `Pass` is an error. Every
mid-run record has an unchecked `Pass`, so the generator's own check would
have exited 1 on every round that found something. The generator writes a
`{"pull_request": {"draft": true}}` payload to a temporary file and hands it
to the check through `GITHUB_EVENT_PATH` unless `gh pr view --json isDraft`
says the branch's pull request is already ready, in which case the check runs
as CI will run it. The platform is asked, never the session. This is the
input shape `chain_check` already documents, not a flag added to it.

**`git diff <base>` without `HEAD` does not see an untracked file**, and the
record the generator has just written is untracked until the orchestrator
stages it. `changed` under `--worktree` therefore appends
`git ls-files --others --exclude-standard` as added paths, so the new record
is in `touched`, gets `refs`, and has its `Target SHA` held to the branch —
`test_an_untracked_records_target_is_held_to_the_branch` is the case that
separates listing the file from diffing it. The merge base is taken
explicitly (`git merge-base <base> HEAD`) so the flag keeps the `...`
semantics of the default path; no fixture here moves the base, so that choice
is stated rather than pinned.

**The report's tables are copied and nothing else of the report is.** The
template asks a probes row that ran a proposed replacement to put the
replacement in a fenced block under the table. The generator copies rows,
so such a block stays in the report. `questions.md` A5 states the assumption
and the alternative.

**The generator's identity with the checker's strings is by loading, not by
`is`.** `round_record.py` loads `chain_check.py` under its own module name,
so a test comparing `generator.VERDICTS is chain.VERDICTS` across two loads
is false while `==` is true; the pin compares by value.

**Two cases passed before the generator existed** — the two that assert
exit 2 and no record, because Python exits 2 for a script it cannot find.
Both were shown red afterwards by mutation (the pipe guard and the empty
round-paragraph refusal removed), and are listed in the hand-back that way.

**Mutation loop: 29 mutations, 28 dead on the first pass; `cell`'s
empty-value guard survived and got its case (`aa5864b`), then died.** Two
units were not mutated on their own and are named rather than claimed: `git`
in `round_record.py`, whose only caller `default_baseline` is covered
directly, and the merge-base choice above.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
