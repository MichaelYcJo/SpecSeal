# 1788912166-red-for-following-the-documents-green-for-ignoring-one — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `178fd44` |
| Ran by | unknown — the spawn prompt named no runner, and the value is the spawning session's rather than a value this segment decides about itself |

## What this phase was asked

#296 — the record-count arm becomes draft-aware in the way the `Pass` arm
already is: on a draft it prints the state instead of appending an error.
Verified by three cases: draft plus no record passes, ready plus no record
still fails with the message unchanged, and `unknown` stays strict.

The trap named in the spawn prompt: `pull_request_state` has a third answer,
and `unknown` must stay strict — otherwise the fix for #296 becomes a way
past #295 and past the record requirement itself.

## What a change to a gate must carry

`CONTRIBUTING.md` asks four things of a gate change, and this branch changes
three gates, so each phase answers them for its own arm.

- **A test seen red.** `test_a_draft_pull_request_has_not_had_its_rounds_yet`
  was run against the unfixed arm and failed with `assert 1 == 0`, the
  message being the very error the fix removes — *declares `through the
  review chain` and … holds no `round-N.md`* printed under a header reading
  `judged as a draft pull request`. The six sibling cases were green before
  the fix and stayed green after it, which is what they are for: they pin the
  direction the fix must not move.
- **A stated failure direction.** The gate **allows more**. A draft pull
  request may now lack a round record. That is the cheaper mistake here
  because a draft cannot merge and `ready_for_review` is already in the
  workflow's trigger list, so the arm re-applies before anything can reach
  `main`. The mistake it removes is not a cost but an outage of a different
  kind: the arm was red for a session that had done exactly what
  `orchestration.md` §*The draft pull request opens at the end of the build,
  before round 1* ordered, and a check whose first production act is red on
  obedience is a check people learn to route around.
- **A prompt budget: zero.** No interactive path, no hook, no question. This
  runs in CI on a pull-request event and its whole output is two exit codes
  and a printed line.
- **Platform honesty.** No process inspection. One environment variable
  (`GITHUB_EVENT_PATH`), one file read, and `json.load`. Nothing here behaves
  differently across macOS, Linux or Windows, and the cases run on the
  platform CI runs on.

## What this phase found

**The draft state had already been computed for every run since `strict` was
added; nothing carried it the hundred lines down the same walk.** `strict =
state != "draft"` sits at what is now `chain_check.py:2977` and was passed
to `check_round` alone. The fix is that value reaching one more arm — no new
input, no new read, no new argument threaded through anything. That is worth
recording because it is the reason phase 2 is cheap in the same way: the
declaration walk already opens the last round record and already has `strict`
in hand.

**The notice channel was the right shape and it was already there.** `main`
accumulates `notices` beside `errors` and prints them through the same
`reader.annotate`, so a draft prints the state rather than swallowing it. A
draft excused in silence would read exactly like a work item whose rounds are
done, which is the failure `pull_request_state`'s own docstring rules out for
the `unknown` state and the same one applies here.

**`unknown` needed no new code and does need its own cases.** All four shapes
of it — no payload, a payload that will not parse, one naming no pull
request, one whose `draft` is the string `"true"` — reach `strict` as ready
because `state != "draft"` is a comparison rather than a truthiness test. The
cases are parametrised over the four and were green before the fix, so what
they pin is that the fix did not re-decide the direction. That matters more
than it looks: the string case is the one where a truthy read would have
inverted the answer, and `"draft": "false"` inverting it is a defect this
function has already had once.

**What the next phase inherits.** The module docstring's summary of what a
draft is excused now names all three things (`Pass`, the record's existence,
the `Broad gate` cell) and says `strict` is what excuses them. Phase 2's arm
is the third item in that list and the sentence is already written for it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the module docstring's claim that a draft is excused *"the checked `Pass`, and nothing else"* | the same sentence, which now enumerates the three things `strict` excuses — the claim is corrected in place rather than deleted, because it is the summary a reader meets first |
