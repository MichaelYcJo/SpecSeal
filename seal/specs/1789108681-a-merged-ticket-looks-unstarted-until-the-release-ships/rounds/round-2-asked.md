# round 2 — the verifying round's paragraph

| | |
|---|---|
| Target | the **diff of round 1's fixes**, `076d691..ab069b1` — not the branch |
| Review at | `ab069b1e58c0c0278f6a9cf6f078f8b24a4777fa` |
| Base of the branch | `origin/release/v0.11.1` = `f9c6907` |
| Draft pull request | #360 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-1.md`, closed — 6 fixed, 1 answered, 1 deferred |

## The job, and the one surface that is not verification

**The answers, not new findings** — for each of round 1's fifteen verdicts, is
it actually closed.

**One exception, and it is a finding surface.** `round-1.md`'s `New units` row
names four cases the fix pass created, each at depth 1:

- `test_the_range_is_measured_to_the_head_the_pull_request_names`
- `test_without_a_named_head_the_range_ends_at_HEAD`
- `test_the_milestone_list_is_read_past_the_first_page`
- `test_every_input_the_script_reads_is_handed_to_it_by_the_step`

A unit the fixes created has been reviewed by nobody, so these are *is this
correct*, not *did this close something*. One fix commit in this repository's
history created eight new units and four carried defects.

## What the fix pass says it did, to be checked rather than inherited

- **Finding 1 — it did not paste the reviewer's fix.** The report justified
  `--jq` with *`--paginate` over an array endpoint concatenates arrays into
  something `json.loads` refuses*, and the pass measured that false on gh
  2.92: seventeen pages merged into one list of 33 and `json.loads` took it.
  It took `--paginate` alone. **The orchestrating session re-derived this** —
  `gh --version` is 2.92.0 and the same command returns 33. Judge the fix, not
  the premise.
- **Finding 2 — it made the range true rather than documenting the collapse.**
  The step now passes `HEAD_SHA: ${{ github.event.pull_request.head.sha }}`
  and measures to it, with a fallback to `HEAD` when no such variable exists.
  The merge-ref behaviour of `actions/checkout` remains **read**, not
  executed, by anyone: no case here runs a workflow.
- **Finding 3 — it declined the reviewer's replacement sentence** because it
  was positional in the same way the defect was, and it left the box where it
  is rather than moving it, arguing that boxes 1 and 2 confirm what arrived
  and a milestone cannot be judged before that. Judge both halves.
- **Finding 6 turned from a note into a case** because finding 2's fix added
  `HEAD_SHA`, which **fails silent**: absent, it falls back to the merge ref
  and reinstates finding 2 with nothing saying so.
- Three ledger anchors drifted and were re-verified with round 1's finding
  written beside them rather than removed.
- The suite caught one of the pass's own: a non-raw docstring raised
  `SyntaxWarning: invalid escape sequence`.

## Executed by the orchestrating session at `6ed1689`

Exit codes read directly, no pipe:

- `bin/test -q` over the two new modules and six they touch → **169 passed,
  exit 0**.
- `gh --version` → 2.92.0; `gh api --paginate "repos/<owner>/<repo>/milestones?state=all&per_page=2"`
  → `json.loads` accepts it, 33 milestones. The pass's correction of the
  report holds.
- `git status --porcelain` → empty.

## Still unverified, and they stay that way

Finding 8 — whether `issues: read` reaches a pull request body — is deferred
to `overview.md` §*Not verified* with the repository owner as answerer, at the
0.11.1 release pull request. Do not settle it by writing to the tracker. The
broad gate is the `sealer`'s; do not run it.

## Not a finding

The gate run against the live tracker refuses naming **#359 and #361**. #361
is in `release: 0.11.1` deliberately and ships in this release, so the
milestone is true as planned and the refusal is the gate seeing work that is
not merged yet. Do not report it and do not write the pair into anything.

## The line the run ends on

Answer the job in a line of its own — `Needs a fix: no`, or `yes` and what
does. A 🟡 answered with grounds is `no`. **The reopening is one**: if this
round opens something, its own fixes get one more verifying round and a
second is refused, after which the run ends `capped`.
