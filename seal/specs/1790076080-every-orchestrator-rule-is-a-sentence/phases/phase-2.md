# 1790076080-every-orchestrator-rule-is-a-sentence — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `598663e7` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

`session_cost.py --post`, with `--says` and `--label`, implementing the four
label states `skills/verify/SKILL.md` §*Measure the segment, and feed the flow
log* already enumerates, refusing to open an issue, and refusing to post
without a reading. `tests/test_session_cost_post.py` with `gh` stubbed, shown
red first against the unimplemented mode. Acceptance A5–A9.

Two constraints came with it. The mode's behaviour on a non-zero exit from the
label lookup is **silent no-op, never post** — Q1's failure direction. And
running it against the live tracker is not part of the build: the cases stub
`gh`, and this phase touched no network except Q1's one probe, which phase 1
already took.

## What this phase found

**There is a fifth state, and the spec names four.** `spec.md` enumerates no
history at all, a history with nothing open, exactly one open, more than one
open. All four are facts about the tracker. The fifth is a fact about the
machine: **the lookup could not run** — no `gh` on PATH, no authentication, no
repository, or a `gh` that answered something other than the JSON it was asked
for. Q1's own default anticipated it without naming it, by saying a non-zero
exit must fall to silent no-op rather than to post.

It is implemented as its own state rather than folded into *no history*,
because the two are different facts and a reader acting on them acts
differently. Both exit 0 with nothing posted, and the message says which
happened. **Exiting non-zero there was considered and rejected**: most
installed repositories never create the label, and a machine with no `gh` on
it is the same shape, so a command that went red in the ordinary case would be
red for following the document beside it. This repository has already measured
what that costs once, in the draft-pull-request window `chain_check` now reads
— *a check that is red for following the document beside it is a check people
learn to skip*.

**One lookup answers both of the skill's questions.** The prose describes
`--state open` and `--state all` as two calls, which they are as questions.
`--state all --json number,state` answers both, because every open issue is in
it, and the partition is done locally. Two consequences, both pinned: the
default `--limit` of 30 had to be raised, since the history reading counts
closed logs and a label with more than thirty of them would read as one that
never existed; and `test_the_lookup_reads_the_label_and_the_whole_history`
asserts `--state all` and a limit above 30, so a later edit cannot quietly go
back to the open-only reading.

**`--post` and `--json` are refused together.** They ask for different things:
one posts a reading to the log, the other prints it for a program to read.
Silently preferring either is a reading somebody asked for and does not get.

**Every printing path now runs through one seam.** `--post` has to post the
same text the command would have printed, and `main` had three exits that
printed — `--spawns`, `--segments`, and the plain report. `emit` is that seam:
it renders, and either prints or captures and posts.
`test_main_without_post_still_prints_the_report` is what keeps the refactor
from having moved the printing path, and
`test_main_posts_the_report_it_would_have_printed` is what keeps the posted
body from being an empty fence with a sentence above it — a mode that posted
nothing would satisfy every argv assertion in the file.

**The body file is the command's leaving, and it is removed.** `--body-file`
rather than `--body`, because the body carries a fenced report and an argv has
a length a comment does not; `delete=False` with an explicit unlink, because
`gh` is a separate process and has to open the path while this one holds it.
`test_the_body_file_is_removed_after_the_post` holds it. A temp file per
segment boundary left behind is the leaving `agent-contract` §7 is about, and
this one is the command's rather than a probe's, so nothing else would ever
clean it.

**`opening no issue` is asserted as a property, not in the one case about
it.** `test_no_state_ever_opens_an_issue` drives all four tracker states and
asserts no `gh issue create` reaches the seam in any of them. The one-case
version would pass over a mode that opened one in a state the case did not
enumerate, which is exactly the shape §12 is about.

**One thing deliberately not fixed, and it is already written down.**
`seal/follow-up.md` names `session_cost.py` among five scripts that die below
the supported interpreter floor with a bare traceback, and says what needs a
person is not the fix but whether those belong in the tracker instead. That
row is the repository owner's and this phase left it alone. What was checked
is that the mode does not make it worse: nothing added here uses syntax above
the floor the file already needs.

**How each case was shown red (contract §15).** Every one of the 22 cases
written before the end-to-end pair was run against `session_cost.py` as it
stood at the phase's parent commit, with the mode's source held in memory and
restored from those bytes: **22 failed, 0 passed**, and the run printed the
name of each. Then the mode landed and they went green. The two `main` cases
were added after that and are covered by the mutation pass instead, which
broke each new unit one at a time and re-ran the module: **fourteen
mutations, all red** — `open_log` reading a failed lookup as an empty one,
losing the no-history/closed split, reading many opens as one, asking for the
open issues alone, and falling back to the default limit; `post` posting on a
closed log, posting on a lookup that could not run, dropping the
comment-failed report, and leaving the body file behind; `comment_body`
dropping the judgment; `emit` printing instead of posting; `main` letting
`--post` run without `--says` and letting `--post` and `--json` both apply;
and `read_says` dropping stdin. The tree was restored from kept bytes and is
green.

**What was run**, executed, output read: `tests/test_session_cost_post.py` (24
passed), the eight other modules that cover `session_cost.py` or sweep the
shipped documents for script reachability (349 passed, 7 skipped), and `uvx
ruff check` plus `uvx ruff format --check` on the two changed files (exit 0,
exit 0, after one `SIM115` was repaired by moving the temp file into a context
manager). No network call was made by any case: `run_gh` is replaced in every
one. The full suite is `unverified` and is the sealer's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The three direct report calls in `main` that printed and returned — `report_spawns`, `report_segments`, and the `report`/`report_tokens` pair | `emit` in the same module, which renders through the same functions and either prints or captures. Nothing left the tree: every reading the script took before it takes now, in the same words, and `test_main_without_post_still_prints_the_report` is the case that says so |
