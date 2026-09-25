# Implementation Plan: the broad gate says what CI says

<!-- seal/specs/1790297086-the-broad-gate-says-what-ci-says/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-25 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

Four vertical slices, one per subject, ordered so that the shared reader
exists before the case that needs it:

1. **#596.** The `cmd.exe` rewrite asks whether a command name starts in a
   directory.
2. **#482, #462, #463.** One reader for the workflow's text, in
   `tests/conftest.py`, and the six sites that slice on a bare token moved
   onto it.
3. **#473.** The gate skips the two arms CI skips on a `main` base, where the
   gated repository carries those steps. Pinned against the workflow through
   phase 2's reader.
4. **#499.** The no-workflow case asserts on the release job's names.

`spec.md` holds the WHAT. This file holds the order, the alternatives and what
each phase is verified by.

## Technical context

- **#596.** `skills/verify/scripts/broad_gate.py#command_names_backslashed`
  is a single position scan. The decision point already exists: the branch
  `if c == "/" and in_name:` asks `CMD_BUILTINS` about `command[start:i]`.
  `start` is set today only for a bare name ("a name opened by `\"` or `^`
  never needs it set"). Under the directory rule every name needs its start,
  so the builder sets it for quoted and `^`-opened names too. The part is then
  computed with `"` and `^` removed. `handed_to_shell` is the only caller
  that reaches the scan, and `run` is the only caller of `handed_to_shell`
  that runs a shell. The case
  `tests/test_the_gate_hands_cmd_a_path_it_can_run.py#test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  holds that.
- **The platform probe** in `test_the_row_runs_on_the_real_platform`
  (`gate.handed_to_shell("bin/probe") != "bin/probe"`) is how that case tells
  `cmd` from `sh`. Under the directory rule, with no root and a working
  directory without `bin/`, it would read `sh` on Windows. It has to pass the
  fixture repository as `root`. This is the one existing line whose meaning
  changes silently rather than going red.
- **#473.** `gate` builds the `survivors` and `corrections` checks
  unconditionally (`checks[SURVIVORS_NAME] = run(...)`,
  `checks[CORRECTIONS_NAME] = run(...)`). `workflow_text(root)` is already
  read before the checks, for `coverage_line`. `base.given` is the caller's
  spelling (`Base.__init__`). `panel` does not read either check, and
  `failures` iterates `checks`, so an arm that is not built is absent from
  both without further change.
- **#482, #462, #463.** No YAML parser is available. The repository has no
  `pyproject.toml`, and CI installs a test runner only
  (`tests/test_ci_gives_the_checks_what_they_need.py#jobs` docstring). Every
  reader here is hand-written over text, which is why a shared one is worth
  having: each hand-written reader re-derives the comment rule, and #462 is
  one that forgot.
- **#499.** `tests/test_the_gate_names_every_step_ci_runs.py` strips
  `str(tmp_path)`, `os.path.realpath(GATE)` and `sys.executable`. The last two
  were added by 1404b3a7 after the ticket was filed.

**What breaks in six months.**

- **#596.** A repository with a top-level directory named like a program it
  also calls with a glued switch. The bound is named in the template, and the
  output for that tree matches `cmd.exe`'s own ambiguity.
- **#473.** A contributor adds a base guard to a third mirrored step and
  forgets the gate. C3's pin fails the suite, which is the point of it.
- **Shared reader.** A step layout it does not model, such as a step with no
  `name:`. It asserts exactly one match, so it fails loudly and never reads
  the wrong region.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#596: rewrite only where the part before the first `/` is an existing directory, with the directory question passed into the scan as a predicate** | A directory made earlier in the same row, or a `cd` in the row, is not seen, so that name is handed over as written. That is the pre-#448 behaviour, and no worse than the row itself. A root directory named like a program reads as a path. | **Chosen.** It is the review's proposal and the milestone's stated fix. Passing the predicate in answers the ticket's objection ("adds a filesystem read to a pure function"): the scan stays pure and drivable, as `windows`/`comspec` already are. The read happens in `handed_to_shell`, which already reads `COMSPEC` from the environment. |
| #596: the same check done inside the scan with `os.path.isdir` | Every scan case needs a real directory tree, and the A2 table (29 rows) is driven through the filesystem instead of a predicate | Rejected. Same behaviour, with a worse instrument. |
| #596: ask `PATH` (`shutil.which(part)`) and leave the `/` where the part is a program | The answer depends on the machine running the gate. `bin` could be on `PATH` somewhere, and CI and a laptop would hand the same row over differently. | Rejected. The gate exists to say the same thing wherever it runs. |
| #596: tell a program from a directory by spelling (short suffix, known program list) | `bin/a` versus `xcopy/e` cannot be told apart by spelling, and a list of Windows programs is an enumeration that rots, as `CMD_BUILTINS` would have without being `cmd.exe`'s fixed set | Rejected. |
| #596: keep the documented bound and close the ticket | A row that runs today still stops running under the gate. The milestone names the behaviour fix as the work. | Rejected. |
| **#473: skip both arms at a `main` base, only where the gated repository's `release` job carries their steps** | A repository that copied `hygiene.yml` but removed the guard from one step: the gate still skips while its CI runs. C3 pins this repository's own copy only. | **Chosen.** It keeps A7: a repository without the workflow runs exactly as before. |
| #473: skip at `main` in every repository | A plugin user whose feature branches merge into `main` loses two arms on every run: the gate under-asks. | Rejected. That is the unsafe direction. |
| #473: parse each step's shell guard out of the workflow and mirror whatever it says | A shell reader inside shipped code, over a language the gate does not otherwise read. Every guard spelling it does not model is silently not mirrored. | Rejected. The constant plus C3's pin gives the same agreement for this repository, with a failure that goes red. |
| #473: keep over-asking and write it into the partition | The broad gate's run can refuse a release pull request that CI would pass, and the gate's stated purpose is to say what CI says | Rejected. #473 offered it. The policy clause decides against it. |
| **Shared workflow reader in `tests/conftest.py`** | A test module that keeps its own slicing. The class is enumerated in `spec.md`, and nothing structural stops a seventh. | **Chosen.** `from conftest import` is the suite's existing mechanism for shared helpers. |
| A reader added to `broad_gate.py` and imported by the cases | Shipped code gains helpers it does not use, and a test-only shape leaks into what every plugin user installs | Rejected. |
| A case that forbids bare-token slicing across `tests/` | A check over the suite's own source, which is a new gate by another name | Rejected. Out of scope for a patch release. |
| **#499: assert on the release job's names (`` `release` ``, `WORKFLOW`, every `PARTITION` step name)** | A future stderr line that names the release job by some fourth spelling | **Chosen.** The needles are the names the gate prints, and a path cannot hold them by accident. |
| #499: add each echoed path to the strip list | The next echoed path (a kept-output directory outside `tmp_path`, a plugin path not in realpath form) reopens it | Rejected. That is the list the ticket is about. |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#596.** The scan takes `is_directory`, `handed_to_shell` takes `root`, and `run` passes it. `handed_line` is reworded. The scan's docstring and `templates/config.md` §*Broad gate* state the directory rule and both bounds, and drop "Telling the two apart is #596". Cases: A1 (the bound case inverted and renamed), A2 driven with directories present, the new table for the other side (A3, A4), A6's real-platform case (`where/q cmd`, skipped off `cmd.exe`), the template case's needles (A7), and every `handed_to_shell` call in the module given a root. Ledger: the rows anchored on the edited units re-read, `seal/releases/0.15.3.md` A2 corrected in place with its dead anchor dropped, and the new claim in this work item's fragment. Changelog fragment opened. | `bin/test tests/test_the_gate_hands_cmd_a_path_it_can_run.py -q`. A1 and A4 shown red at the frame commit. Each new template needle shown red with its sentence cut (§15). `evidence-check` over the ledger for the drifted rows. | f01a37ae |
| 2 | **#482, #462, #463.** The comment rule, `workflow_step` and `step_running` in `tests/conftest.py`. The six enumerated sites moved onto them (three in `test_a_merge_cannot_silently_drop_a_correction.py`, one each in `test_a_body_naming_two_issues_claims_one.py`, `test_the_changelog_is_gathered_at_release.py` and `test_the_ledger_fragments_fold_at_release.py`). `test_ci_gives_the_checks_what_they_need.py#strip_comments` uses the shared rule. `base_spellings` reads code lines and `env:`'s `BASE:` only, and returns `""` for an empty value. The spelling check lifted into a helper that asserts. Reader cases B1–B4 over one fixture workflow. | The seven modules named in this row, each alone. B1, B2 and B4 shown red with comment stripping or the `env:` rule removed from the reader. B3 shown red (`TypeError`) at the frame commit. | |
| 3 | **#473.** The constant beside `PARTITION`, the guard in `gate` (both conditions), and the stderr line. `skills/verify/SKILL.md` §*What the count does not say* rewritten. Cases C1 (with its non-`main` red twin), C2 and C3 (through phase 2's `workflow_step`). The line's text pinned. Ledger rows on `#gate` and `#PARTITION` re-read, and the new claim in the fragment. Changelog fragment extended. | `bin/test tests/test_the_gate_names_every_step_ci_runs.py tests/test_the_gate_asks_the_range_ci_will_ask.py -q`. C1 shown red at the frame commit. C3 shown red with one arm removed from the constant. | |
| 4 | **#499.** The no-workflow case asserts on `` `release` ``, `gate.WORKFLOW` and every `PARTITION` step name. The strip list goes. M2 measured before the edit and after it. Changelog fragment closed. `overview.md` written. | The module alone, run from a scratch copy of the tree under a directory whose name holds `release`, before and after. The red direction: `coverage_line` forced to return a line, and the case goes red. | |

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
`seal/specs/1790297086-the-broad-gate-says-what-ci-says/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
**Re-read the column after any rebase.** Nothing measures from this column.

## Operational impact

- **No new dependency, no new flag, no new exit code, no new refusal.**
- **On Windows with `cmd.exe`,** a row with a switch glued to a program
  (`xcopy/e`) now runs as written. A row whose command name starts in a
  directory that does not exist at the row's working directory is now handed
  over as written, where before it was rewritten. For such a row neither
  spelling runs, so nothing that ran stops running.
- **With `--base main` in a repository whose `hygiene.yml` carries the two
  steps,** the gate runs two fewer arms and prints one line saying so. That
  means only SpecSeal itself, or a copy of its workflow. Everywhere else,
  nothing changes.
- **Sibling work items in this release:**
  - A (`chain_check.py`), B (`survivor_check.py`) and E (`evidence-check`)
    edit different files.
  - C edits `settle` and the release scripts.
  - None of them edits `broad_gate.py`, `tests/conftest.py` or the six sites
    above, as the milestone description reads on 2026-09-25. If one squashes
    first, the release branch is merged in, never rebased, as the 0.15.0 run
    recorded.
