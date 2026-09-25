# 1790297086-the-broad-gate-says-what-ci-says — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | <the phase's closing commit, as `plan.md`'s Status cell for phase 2 names it> |
| Ran by | unknown — the spawn prompt did not name the agent and model, and this segment does not source that value from its own idea of itself |

## What this phase was asked

#482, #462 and #463. Phase 2 had four parts:

- Put the comment rule, `workflow_step` and `step_running` in
  `tests/conftest.py`.
- Move the six sites that slice `hygiene.yml` on a bare token onto them.
  Three are in `test_a_merge_cannot_silently_drop_a_correction.py`, and one
  each in `test_a_body_naming_two_issues_claims_one.py`,
  `test_the_changelog_is_gathered_at_release.py` and
  `test_the_ledger_fragments_fold_at_release.py`.
- Make `test_ci_gives_the_checks_what_they_need.py#strip_comments` use the
  shared rule.
- Make `base_spellings` read code lines and `env:`'s `BASE:` only, return
  `""` for an empty value, and lift the spelling check into a helper that
  asserts.

Reader cases B1 to B4 run over one fixture workflow. The seven modules are
each run alone. B1, B2 and B4 are shown red with comment stripping or the
`env:` rule removed from the reader, and B3 red at the frame commit. The
spawn prompt added one instruction: run every module that imports what
changes, which for `tests/conftest.py` is every module that imports from it.

## What this phase found

- **The reader needed a list model, not a `- name:` splitter.**
  `workflow_steps` reads each job's `steps:` list. A step runs from its `- `
  at the list's own indentation to the next item there, or to the first
  shallower code line. A step with no name (`- uses: …`) is a step of its
  own, so the unnamed checkout step can no longer end up at the head of the
  next named step's region. The first draft ended the list at the first
  blank line, which cut `hygiene.yml` to one step. Blank lines now pass
  through.
- **An indented whole-line comment is caught twice.** The trailing rule
  ends a line at a `#` that follows a blank, and an indented comment's `#`
  follows its indentation. So removing only the whole-line branch leaves
  B4 green. The branch is still needed for a `#` in column 0, where no blank
  comes before it, and that row pins it. B4's red is shown with all comment
  stripping removed, which is the spec's wording.
- **A trailing comment exists in `templates/hygiene.yml`**
  (`fetch-depth: 0 # both checks diff against the base branch`), outside the
  frame's measurement of `.github/workflows/`. No case reads that template
  through the rule, and over `.github/workflows/*.yml` the rule removes
  exactly the lines the whole-line rule removed. A case holding that was
  drafted and then removed, because it would refuse a trailing comment added
  later. That is a new rule, and this patch adds none.
- **One existing fixture row changed its input, not its expectation.**
  `WORKFLOW_SHAPES`'s bare `BASE: origin/…` line is not a base under
  #462's rule, because nothing above it is `env:`. The row now carries the
  `env:` line, and its expected spelling is unchanged.
- **The frame's reader, run as it stood,** read `origin/other`, `bar` and a
  `with:` `BASE:` as bases. It returned `[None]` for `--baseline ""`, and its
  check raised `TypeError`.
- **`overview.md` had to open here, not in phase 4.**
  `tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview`
  refuses a work item with phase records and no overview. The implement
  skill opens it at the first unverified item anyway, and M1 was one. The
  same run found that the renamed case was still named in `spec.md` and
  `phase-1.md`. Both lines now carry `NAME NOT IN TREE`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the six bare-token slices of `hygiene.yml` in four test modules | `tests/conftest.py#workflow_step` and `#step_running` |
| `strip_comments`'s own whole-line rule | `tests/conftest.py#code_line` |
