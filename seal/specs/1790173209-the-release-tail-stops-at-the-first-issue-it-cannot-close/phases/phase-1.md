# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — phase 1

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/phases/phase-1.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 10c44097 |
| Ran by | unknown — the spawn prompt handed over no value; the spawning session fills this row |

## What this phase was asked

#536, first in the plan's order because a partial close is the failure the
previous release paid for by hand. Deliver `close_issue(repo, number,
comment)` in the closer: `gh issue close`, and on refusal `gh api -X PATCH …
-f state=closed` then `gh api …/comments -f body=…`; the loop collects
failures, attempts every issue, still spends the label per closed issue, and
exits non-zero at the END naming each failure with both errors. Rewrite the
docstring's *It fails loudly* paragraph. `docs/branch-and-release.md` and
`docs/release-checklist.md` §6 say so and say how a partial close is repaired
(a re-run with `BEFORE`/`AFTER`/`REPO`). Verified by S1 and S2 (a fake that
refuses one route, then both — seen red at `HEAD`), S3 (the existing AST case
stays green), S4 (one `DRY_RUN=1` run against the previous release's inputs,
its output recorded here), with the closer's fakes extended.

## What this phase found

**Whether the frame holds.** Every coordinate the frame named for this phase
was opened and is where it said: `run` at line 103 exits on any non-zero
`gh`, the close loop called it once per issue, `_issue_api` shows the other
shape, and the AST case sits at line 1051 of `tests/test_release_hygiene.py`.
One aggregate did not hold: S4 says the dry run prints *the seven pull
requests of that push*; the tracker answered six (533, 531, 528, 527, 525,
524). Nothing in the phase depended on the number.

**The close goes through a new `attempt`, not through `run` with the exit
caught.** `run` is what `arrived` and `gh_json` need — a read the rest of
the run depends on — so it keeps exiting. `attempt` returns `(ok, stderr)`
and is the third door into the tracker; the fakes in
`tests/test_a_declared_label_reaches_the_tracker.py` and
`tests/test_release_hygiene.py#_offline` each gained it, because a fake that
does not answer it lets the close reach `subprocess.run`, which the hygiene
module's `_offline` turns into *this case reached the network*.

**A comment the REST route cannot post does not un-close the issue.** The
PATCH is the act and the comment says why; the failure is printed with
`the issue is closed either way`, the shape `drop_label` already has. A
refused PATCH is the real failure: both errors are collected and the label
stays, because a spent label on an open issue would say the release finished
with it.

**Red at `2fda77e8`, quoted.** S1 (and the two cases beside it) died inside
the loop:

```
E   SystemExit: gh issue close 2 --repo example/repo --comment Closed by #100, …
    failed: GraphQL: Something went wrong while executing your query
----------------------------- Captured stdout call -----------------------------
pull requests in this push: [100]
closed #1, named by #100
removed 'size: now' from #1
```

S2 reported the state the exit left behind:

```
E   AssertionError: #3 is sorted after the refused #2 and had to be closed anyway: {1: 'closed', 2: 'open', 3: 'open'}
```

and the source case read `the fallback posts no comment at all`. Seven of
seven red. Green at `0a4e1194`: `136 passed` over the five modules that
drive the closer (`bin/test tests/test_the_closer_carries_on_past_a_refusal.py
tests/test_a_declared_label_reaches_the_tracker.py tests/test_release_hygiene.py
tests/test_a_merged_ticket_says_so_on_the_tracker.py
tests/test_a_body_naming_two_issues_claims_one.py -q`).

**Mutations, one at a time, `tests/__pycache__` cleared between, the file
restored from a copy kept in the script rather than from `HEAD`.** Seven of
eight went red on the first run; the eighth — `attempt` reporting every write
as refused — stayed at 63 passed because every case fakes `attempt`. The
case `test_attempt_answers_the_exit_code_and_the_error_rather_than_exiting`
drives the real function against a fake `subprocess.run` and turns that
mutation red (1 failed, 7 passed). The full table is in the ledger fragment's
P1 row.

**S4, the dry run, executed once against the real tracker with
`DRY_RUN=1`.** Inputs `BEFORE=1bafeb78143bf05430177e33927905205018d9d4
AFTER=cbb58091fddb9a02e3136156d7963dcd66798d1b REPO=<owner>/<repo>`, from
this clone, which has both commits. It printed:

```
DRY_RUN — nothing will be written
pull requests in this push: [533, 531, 528, 527, 525, 524]
#511 already closed (named by #525) — leaving it
#515 already closed (named by #524) — leaving it
#517 already closed (named by #525) — leaving it
#518 already closed (named by #528) — leaving it
#519 already closed (named by #531) — leaving it
#520 already closed (named by #527) — leaving it
```

and exited 0. Nothing was written; no `would close` line, because the hand
repair had already closed every one.

**Q3 of `questions.md` — why GraphQL refused #515 — was not found here**, and
the record says so: the fallback is built for the class (one route refusing)
and the phase spent nothing chasing the cause.

**The ledger.** `seal/ledger.md`'s T1 row anchors on `#main` and drifted; the
claim (the label comes off after the close and only after it) still holds
and the row carries a `Re-read 2026-09-23` note. The fragment opens with P1,
P1b and P1c. `evidence-check --strict` exits 0 after `--reverify`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the inline `run("gh", "issue", "close", …)` in `main`, with its comment literal | `close_issue` and `closing_comment` in the same file; the argv is still the one `gh issue close` the AST case counts |
