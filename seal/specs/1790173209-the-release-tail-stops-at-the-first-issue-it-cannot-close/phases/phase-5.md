# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — phase 5

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/phases/phase-5.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | fe9882fd |
| Ran by | unknown — the spawn prompt handed over no value; the spawning session fills this row |

## What this phase was asked

#362. Both docstrings — `release_completeness_check.py`'s and the one on
`tests/test_a_release_cannot_ship_an_untrue_milestone.py#test_every_input_the_script_reads_is_handed_to_it_by_the_step`
— state *the inputs are the five the step must pass*, carry the re-measured
table, and drop the superlative and the count. Verified by S12: the table
executed by the phase, one input removed at a time, exit codes read
directly, recorded as an executed ledger row.

## What this phase found

**The frame contradicted itself on the count, and the ticket's reason
decided it.** `plan.md` says *drop the superlative and the count*; `spec.md`
S12 says both texts *say the inputs are what the step must pass — five* and
*neither carries a superlative or a count*. The ticket's grounds are that a
count rots the next time an input is added, which is how the previous
sentence reached round 3 in the first place. So neither text writes a
number: the table is the enumeration, and the case that reads both texts
asserts each of the five names rather than a count word.

**The measurement, executed 2026-09-24**, against `HEAD_BRANCH=release/v1.2.3`
(a fixture name; no such milestone exists, so the gate's own *verified
NOTHING* warning is what the control run prints), `HEAD_SHA` the branch tip,
`BASE=origin/main`, the real repository, and `gh`'s config directory pointed
at an empty scratch directory (`GH_CONFIG_DIR`, NAME NOT IN TREE — it is
`gh`'s own variable) so that removing `GH_TOKEN` removes the only credential
the command could find. Exit
codes read from `$?`, never through a pipe:

| Removed | Exit | What happened |
|---|---|---|
| nothing (control) | 0 | the *no milestone … verified NOTHING* warning |
| `REPO` | 1 | `KeyError: 'REPO'` |
| `HEAD_SHA` | 0 | output identical to the control; nothing says the range fell back to `HEAD` |
| `HEAD_BRANCH` | 0 | `'' is not a release/vX.Y.Z branch — nothing to judge` |
| `BASE` | 0 | output identical to the control; the default is `origin/main` |
| `GH_TOKEN` | 1 | `gh api --paginate repos/<owner>/<repo>/milestones… failed: To get started with GitHub CLI, please run: gh auth login` |

Two absences are silent, which is what the ticket measured and what the
superlative denied.

**A case holds the two texts to each other**, because the ticket's own
history is one text being corrected while the other kept the old sentence:
`test_the_script_and_this_file_draw_the_input_boundary_the_same_way` reads
the module docstring and the pinning case's docstring, whitespace collapsed
— the superlative sat across a line break, and the first spelling of the
case missed it for exactly that reason — and asserts the superlative is gone
from both, the boundary sentence is in both, and each names the five
entries. Red at `ac5d6da7`:

```
E           AssertionError: the module docstring does not say which boundary it draws
```

(the first spelling; with whitespace collapsed the same run fails one
assertion earlier, on the superlative). Green at `7ae8855a`: `30 passed` in
the module, `54 passed` with `tests/test_a_merged_ticket_says_so_on_the_tracker.py`.
Putting the old superlative back into either text, wrapped as it was, reds
the case: `1 failed` both times.

**The sibling `label_merged_on_release_branch.py` was left alone.** Its one
Environment line draws an `os.environ` boundary (`BRANCH`, `BEFORE`,
`AFTER`, `REPO`) and no case disagrees with it; the ticket's fix surface is
the two texts that disagreed with each other.

**One anchor the checker could not resolve was written and then removed**: a
workflow step's `name:` is not a heading, so P5 names the step in prose and
anchors on the case that reads it. Found by `evidence-check --strict`
exiting 2 after the phase's first commit; corrected in `fe9882fd`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence *`HEAD_SHA` is the one entry whose absence is silent rather than loud* and the four-name enumeration in the module docstring; the same superlative in the case's docstring and its assertion message | the measured table in both docstrings, and the case that holds them together |
