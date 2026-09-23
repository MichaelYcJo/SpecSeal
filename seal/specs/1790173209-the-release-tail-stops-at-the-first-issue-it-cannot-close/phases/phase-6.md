# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — phase 6

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/phases/phase-6.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 72afd030 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

#198. The roll reads the log's comment count before closing; zero means the
close comment, the successor's body and a printed line say the cycle closed
with no measurement; a count that cannot be read leaves the roll unchanged
and prints a line; exit 0 in every case; `docs/issues-and-milestones.md`
§*flow-measurement* says what an empty cycle produces. Verified by S13 and
S14 (cases with the module's fakes, seen red) and the module's existing 30
cases green.

## What this phase found

**Q2 answered: the list call's `--json`.** Every fake that reaches `main`
already answers `list_open_issues`, and a case that mocks `close_issue` and
`open_issue` but not `try_run` (`test_one_open_issue_after_the_retry_succeeds`)
would have reached the network through a `gh api` read. So the one list call
asks for `number,title,comments` and `comment_count(issue)` reads the array's
length; a listing without the field answers `None`.

**The count travels as a keyword with a default, and seven fakes widened.**
`close_issue`, `open_issue` and `issue_body` take `comments=None`; `main`
passes what it read. The module's cases replace those three with lambdas of
the old arity in seven places, and each took `comments=None` — the only edit
to the 30 cases that were there, and all 30 pass unchanged otherwise.

**Zero is the only count that speaks.** A sentence about emptiness on a log
whose count could not be read would be a false record on the tracker, so
`None` produces one printed line (*could not read #N's comment count from the
listing — rolling as before*) and nothing on either issue. The mutation
turning a missing field into zero is caught by S14 for exactly that reason.

**Red at `6d55e1d9`, quoted:**

```
E       AssertionError: the close comment does not say the log was empty: 'Closed by the release that just shipped 0.7.0. The next flow-measurement issue opens as `chore: flow measurement — after 0.7.0` …'
E       AssertionError: the job log does not say the comment count was unreadable: "rolled: closed #89, opened 'chore: flow measurement — after 0.7.0'\n"
E       assert 'number,title' == 'number,title,comments'
3 failed, 32 passed in 0.10s
```

The fourth new case — a log with comments gains no sentence — was green
there, pinning the reading that did not change. Green at `1ea20391`:
`89 passed` over `tests/test_a_release_rolls_the_flow_measurement_issue.py
tests/test_a_declared_label_reaches_the_tracker.py
tests/test_a_segment_feeds_the_flow_log.py`.

**Mutations**, nine, each red on exactly one case; the list is in the ledger
fragment's P6 row. The last one — the count read from an empty listing
rather than from the log `main` holds — is the shape where the read moves
after the close by accident and reads the successor.

**The shared ledger.** Twelve rows drifted: seven anchored on the roll's
units (G6, F4, F1, F2, F6, G1, G3), four on the document section the
sentence joined (G5, S4, T1, C5), and F6 again through the recovery case
whose fake widened. Every claim holds and every row carries a
`Re-read 2026-09-24` note. `evidence-check --strict` was red after this
phase's commit for a reason outside it — phase 5's record named `gh`'s
`GH_CONFIG_DIR` (NAME NOT IN TREE) without the marker the records arm asks
for — and is green once the marker is written.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
