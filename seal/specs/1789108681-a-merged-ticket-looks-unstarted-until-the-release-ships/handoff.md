# Handoff — SpecSeal 0.11.1, session of 2026-09-11

## Start here — what to say to the next session

Paste this as the first message of a fresh session in this repository:

> Read `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/handoff.md`
> and pick up where it stops. The branch
> `feat/359-a-merged-ticket-looks-unstarted-until-the-release-ships` is pushed
> at `3b1eb6a` with draft pull request #360 open into `release/v0.11.1`, round
> 1 closed, and the verifying round 2 spawned but not recorded. Take it from
> there through `sealer` to a ready pull request. Do not re-ask the routing
> question — `routing.md` on that branch answers all four axes — and do not
> re-ask `questions.md` Q1 or Q2, both of which the owner answered.

**Four things that session should not have to discover.**

- **`ruff` is not in this checkout.** `uvx ruff check .` and
  `uvx ruff format --check .` are the form that works, and they are two thirds
  of the broad gate. `bin/test -q` is the third.
- **Read exit codes directly, never through a pipe.** `cmd > /tmp/x 2>&1;
  echo $?` — this shell is `zsh`, `${PIPESTATUS[0]}` is not it, and a
  newline-separated variable does **not** word-split on expansion. Both cost
  this session a wrong reading.
- **`round_record.py` has no `bin/` wrapper** (that is #318). Invoke it as
  `.venv/bin/python skills/code-review/scripts/round_record.py`.
- **The issues that are merged and still open are correct.** #351 is merged
  into `release/v0.11.1` and stays open until the release reaches `main`.
  Closing one by hand breaks the next release.

Everything below was executed in this session unless labelled otherwise.

## Where the release stands

`release/v0.11.1` is at `f9c6907`. The milestone holds three issues and that
is the whole release — it is true as planned, which the new gate requires.

| Item | State |
|---|---|
| **#351** — `docs/flow.md` deleted, its four parts placed where they are read | **merged** at `f9c6907` (PR #358, squash). Labelled `merged: 0.11.1` by hand. Two review rounds, sealed at `af37b37`, CI green on all five jobs including Windows |
| **#359** — the `merged: X.Y.Z` signal and the release completeness gate | **in the chain.** Branch pushed at `3b1eb6a`, draft PR #360. Round 1 closed (6 fixed · 1 answered · 1 deferred). Round 2 spawned; see below |
| **#361** — a release's size is decided by urgency, not by a count; a `now` label | **not started.** No branch, no `routing.md` |

## #359 — exactly where it stopped

| | |
|---|---|
| Branch | `feat/359-a-merged-ticket-looks-unstarted-until-the-release-ships`, pushed, clean |
| HEAD | `3b1eb6a` — the round-2 paragraph, nothing after it |
| Draft PR | #360 into `release/v0.11.1`, body written, `Closes #359` |
| Round 1 | closed at `ab069b1`. Target `9a010fd`, 15 verdicts, `Needs a fix: yes` on findings 1–4 |
| Fix pass | `076d691..6ed1689`, table at `rounds/round-2-fixes.md` |
| Round 2 | **spawned, not recorded.** Target is the fix diff `076d691..ab069b1`; the paragraph is committed at `rounds/round-2-asked.md` |
| Broad gate | **not run.** `sealer`'s, after round 2 closes |

**The first thing to check is whether `rounds/round-2-report.md` exists.**

- **It exists** → the verifying round finished. Verify its highest-severity
  coordinates yourself, then
  `round_record.py new --item <dir> --round 2 --target ab069b1e58c0c0278f6a9cf6f078f8b24a4777fa --asked <dir>/rounds/round-2-asked.md --ran-by "specseal:warden on Opus 5" --pr "#360" --baseline origin/release/v0.11.1`,
  commit it, and close any open rows the way round 1 was closed.
- **It does not exist** → the round did not finish. Spawn a fresh `warden`
  with `rounds/round-2-asked.md` as the prompt's spine; it is written to be
  the whole paragraph.

**Round 2 has a finding surface, which a verifying round usually does not.**
`round-1.md`'s `New units` names four cases the fix pass created, all depth 1:
`test_the_range_is_measured_to_the_head_the_pull_request_names`,
`test_without_a_named_head_the_range_ends_at_HEAD`,
`test_the_milestone_list_is_read_past_the_first_page`,
`test_every_input_the_script_reads_is_handed_to_it_by_the_step`. Those are
*is this correct*, not *did this close something*.

**Then, and only then:** spawn `sealer` with
`--base origin/release/v0.11.1 --record <the work item directory>`, read what
it returns, commit the sealed record, `gh pr ready 360`, and watch CI.

## What the owner decided today, so none of it is re-asked

| Decision | Answer | Where it lives |
|---|---|---|
| #351 routing | chain · open the PR · smith · the session | that item's `routing.md` |
| #351 Q1 · Q2 · Q3 | milestone descriptions + ticket comments · this session writes them · **delete the clause outright**, no marker left behind | that item's `questions.md` |
| #351 Q6 | **(a)** — *a branch writes its own rows* ends with the file it was about | that item's `questions.md` |
| #359 routing | chain · open the PR · smith · **framer** | this item's `routing.md` |
| #359 Q1 | **(c)** — `L \ D` fails, `D \ L` reports | this item's `questions.md` |
| #359 Q2 | **(a)** — the milestone was made true rather than the gate excepted | this item's `questions.md` |
| Release sizing | **urgency, not a count** — what has to be in effect before the next work item starts. This is #361 | issue #361's body |

## What changed on the tracker, and none of it is in the tree

Tracker state is not committed anywhere, so this table is the only record.

- **`merged: 0.11.1` label created by hand** and applied to #351, as a bridge
  until #359's signal does it. Green, described as *"Squash-merged into
  release/v0.11.1; closes when the release reaches main"*.
- **The 0.11.x line shifted back one number.** The old `release: 0.11.2`
  (11 issues) is now `0.11.3`; the old `0.11.3` (8) is now `0.11.4`; a new
  `release: 0.11.2` was created holding the seven that left 0.11.1 —
  #103, #198, #330, #343, #345, #350, #354. `release: 0.12.0` did not move:
  it is the next minor, not part of the patch line.
- **Four release milestones gained descriptions** stating purpose and the
  grounds for their order (0.11.1, 0.11.2, 0.11.3, 0.12.0). The 0.12.0
  description's sentence about why it is a minor bump rather than a patch is
  **this session's inference, not the owner's** — the owner's original
  description named the theme only.
- **#103 and #330 gained comments** carrying the grounds `docs/flow.md` held
  and their own bodies did not.
- **#359 and #361 were opened** by this session.

## Open, with an answerer, and none of it blocks

| Item | Who answers |
|---|---|
| Whether `issues: read` reaches a pull request body through the issues endpoint — #359's finding 8 | the repository owner, at the 0.11.1 release pull request, which is the first CI run of that step |
| Whether the workflow token's `issues: write` covers label *creation* — #359's Q3. `merged: 0.11.1` already exists, so this branch's squash exercises the add and skips the create; the create path first runs at the next release's first squash | the repository owner, watching that squash |
| Whether the signal fires as specified | the same squash |

## One thing this session proposed and did not open

**A ticket for the class *a document describing a mechanism goes stale and
only a reader catches it*.** Measured: `seal/ledger.md` plus `seal/ledger/`
hold **480** rows with a coordinate; **20** anchor a `docs/*.md` claim and
**14** of those pin a doc claim to executable code. So the mechanism exists
and works — `evidence-check` drifts the row when the code moves — and it is
used on 14 of 480. Three instances surfaced today: the release checklist's
sentence about the close-issues workflow (wrong about its trigger **and** its
data source), the sizing sentence (#361 takes it), and §*Nothing automated
reads a milestone* (#359 takes it). Nothing sweeps for the fourth. Under the
sizing criterion #361 states, this is **not** `now`.

## What this session got wrong, so it is not repeated

- **Read a ceiling as a target.** Proposed moving eighteen issues out of the
  release milestones to "bring them down to size", and separately read a
  two-item release as under the rule with room for a third. The owner stopped
  both. A milestone here is a pool a release is cut from, and nothing
  automated reads it — an over-size one costs a fuzzier answer and nothing
  else. #361 is the repair.
- **Wrote prose inside `## Not verified`**, which `unverified_check` reads as
  a table. Exit 1, three times, `a line inside the table that is not a table
  row`. That is the class round 1 of #351 had just found in `plan.md`'s phase
  table, reproduced in the commit closing it.
- **Put a count in a spawn prompt without naming the set it was counted over**,
  which cost #351's round 2 a finding and three irreconcilable figures for one
  act.
