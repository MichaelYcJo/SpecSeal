# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 7ef26033 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

`plan.md`'s phase 3: `agents/smith.md` step 4 and the Boundaries sentence,
`skills/verify/SKILL.md`'s new section, S9 seen red at the base then green,
S10 green; the four `## Phases` ledger rows re-read against the edit and
re-stamped with a dated note, the rider read and re-stamped, `evidence-check`
clean, and `payload-meter` before and after (C6). The spawn delegated
`questions.md` Q2, the README cheat sheet, to this build, to be decided from
the tree and recorded here.

## What this phase found

**The spec's suggested step-4 text broke two existing pins, and the pins
won.** Both are ratified, and the suggestion was a suggestion.

- `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#test_no_agent_definition_names_this_repositorys_own_command`:
  `agents/smith.md` ships to repositories with no `bin/test`, so the example
  may not name it. The command reads `--tests "<the runner> <module> -k
  <cases>"`, and `-p no:xdist` is conditional on a runner that starts
  xdist workers by default. S9 was written against the spec's `--tests
  "bin/test ` and was loosened to `--tests "` with a comment saying why.
- `tests/test_the_set_a_work_item_always_has.py#test_the_top_rung_names_behaviour_rather_than_a_count`
  refuses the phrase *one file* in the definition, which the suggestion
  carried (*removes that one file's cached bytecode*). It reads *the mutated
  file's* now.

`skills/verify/SKILL.md` is under neither pin, so its example keeps the
repository's own `bin/test`, as `arm-check`'s section beside it does.

**Q2, decided: not listed in the README cheat sheet.** The ground is the
tree's own pattern, measured over `README.md` §*Cheat sheet* (lines 268-302 at
`7ef26033`). Of the thirteen hyphenated `bin/` commands other than this one, seven have a
row:
`deferral-check`, `evidence-check`, `fold-check`, `payload-meter`,
`session-cost`, `settle` and `unverified-check`, which a person types to ask
the repository something. The six without one, `arm-check`, `broad-gate`,
`correction-check`, `round-record`, `seal-stamp` and `survivor-check`, are
each typed by an agent or a hook inside a run. `mutation-check` is the
smith's loop and joins the second group. Its readers find it in
`agents/smith.md`, which every smith receives at startup, and in
`skills/verify/SKILL.md`. `README.ko.md` moves with `README.md`, and neither
changes.

**The rider was re-read and its claim re-taken before the re-stamp.** It is
about the waiver example at the head of `## Phases`, and step 4 is nowhere
near it. `_hides_a_commit`, loaded from this tree's
`hooks/commit-review-gate.py`, reads True for `agents/smith.md` at `cd24f516`
and at the edit, so the rider's standing sentence holds. `rider_check.py`
then reported 20 ok and 0 drifted.

**Five ledger rows drifted, not four.** The four on `agents/smith.md#"##
Phases"` (`0.6.0.md` L5, `0.8.1.md` R8, the `0.12.0.md` second-copy row,
`0.15.1.md` N1), and `0.9.5.md`'s row pinned at
`tests/test_arm_check.py#test_no_arm_runs_while_cached_bytecode_for_the_module_exists`,
which phase 1's plant fix moved. Each was re-read against its edit and given
a dated note, then re-stamped file by file with `evidence-check --reverify
--checked 2026-10-01 --ledger <file>`. The total afterwards was 3152 ok and 0
drifted. `0.15.1.md` N2, on the `arm-check` heading, did not drift: the
hasher's unit for that `####` ends where the new sibling begins. One note
went in wrong first: the replacement for the `0.12.0.md` row dropped its
`#598` re-read note, and it was put back before the re-stamp. A marker count
taken against `HEAD` afterwards shows each of the five files one marker up
and none lost.

**C6, the payload.** `payload-meter --agent smith`, before the edit and after:
`agents/smith.md` 24,307 → 25,310 bytes (7,596 → 7,909 estimated tokens), and
the smith's whole startup payload 121,863 → 122,866 bytes (38,082 → 38,395).
That is +1,003 bytes, and the estimate is the meter's assumed 3.2 B/token,
not a calibration.

**Mutated with the command, the documents this time.** Seven breaks, six
red. Removing the Boundaries sentence, the `-p no:xdist` sentence, or the
`--tests` shape from the definition, or putting `tests/__pycache__` back,
each reddens S9 or the Boundaries case. Changing the bound's figure or the
`red` verdict's spelling in the SKILL section reddens that section's case.
**Survived:** deleting `with PYTHONDONTWRITEBYTECODE=1` from the section's
first paragraph, because the paragraph after it says the cases inherit the
variable, so the section still says it once. That removal keeps what the
section says, and it is reported rather than pinned.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `agents/smith.md` step 4's *clear `tests/__pycache__` between mutations* | replaced by the `mutation-check` command in the same paragraph; S9 pins its absence |
| `agents/smith.md` step 4's *Restore it from bytes you kept, per Boundaries below* | the Boundaries bullet, which now says `mutation-check` holds that copy |
