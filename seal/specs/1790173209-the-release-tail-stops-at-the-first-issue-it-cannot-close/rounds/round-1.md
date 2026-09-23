# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — review round 1

| Field | Value |
|---|---|
| Target SHA | bdbe575ba0cde463f2b65dbaa1f818deb61057ee |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 538 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `5073481487e055c88c8deb1db1693427bda3d6f2..3ba12d83cad25584c0527e98cc01edae186cd66a`, 3 commits |
| Contract changes | Tracker → round-1-report.md, round-1.md, pytest |
| New units | comments_on (depth 1); section_heading (depth 1); test_a_second_gather_into_the_last_section_ends_the_file_with_one_newline (depth 1); test_a_second_gather_into_an_undated_heading_says_what_the_write_does (depth 1); test_a_refusal_before_the_comment_landed_still_gets_it_from_the_fallback (depth 1); test_a_tracker_that_does_not_count_comments_gets_the_comment_posted (depth 1) |
| Needs a fix | yes — finding 1, the fallback's duplicate closing comment (🟡, with the fake's refusal order corrected so a case sees it) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the release tail, the whole branch `fix/536-the-release-tail-stops-at-the-first-issue-it-cannot-close` against `release/v0.15.0`: seven tickets in seven phases, #536, #266, #289, #363, #362, #198, #157. Stage 1 asked whether each phase builds what `spec.md`'s scenarios S1–S16 say and whether the five divergences `overview.md` records were the right call — the dry run's six pull requests against the frame's seven, S10's fixture tagging the running version, S12 carrying no count word, S8's red seen on the real tree, and `close_issue` built on a new `attempt` beside `run`. Stage 2 asked five things:

- whether the closer's fallback path is reached by a real refusal shape and not only by the fakes: does `attempt` return what `close_issue` branches on when `gh issue close` exits non-zero, and does a fallback that also fails leave the `size: now` label and name both errors at the end
- whether the widened `FENCE` and `SPAN` change what `issue_claims_check.py` reads at the pull request, and whether the two shapes left unmasked are pinned by a case that would go red if somebody masked them
- whether `shipped_tags` reads the tags of the root under test and not of the developer's clone, whether the real-tree case fails on a tagless checkout with the `fetch-depth: 0` sentence, and whether the version-rule refusal still catches the running version when it is bumped and untagged
- whether the roll's comment count comes from the one list call and the three empty-log sentences appear where the phase says, with the unreadable path unchanged
- whether the 39 mutations in the ledger fragment's P1–P7 rows and the two `Corrected` rows in `seal/ledger.md` (R1's timer rule, S4's tracker sentence) are true of the landed code

The hand-back labelled the broad gate unverified; the sealer answers that after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The REST fallback posts the closing comment a second time, because `gh issue close --comment` comments before it closes and the refused route has already left its comment on the issue | `.github/scripts/close_issues_on_release.py#close_issue`; `tests/test_the_closer_carries_on_past_a_refusal.py#Tracker.attempt` | **fixed** `611df55b` | fixed at 611df55b — `comments_on(repo, number)` reads the count through `_issue_api` before and after the first route; `close_issue` skips the REST comment when the count grew by one and posts it when the read cannot say; the fake records the comment before it refuses (the tracker's order) plus a `refuse_before_comment` knob; the same-comment case seen red at `50734814` and green after; two new cases; the five sentences gained *where the refused route did not already post it*; P1 corrected and P1d added. The two ⬜ rows went in the same commit: `insert`'s append arm drops the tail's blank lines and `rstrip`s the join (two cases seen red), and `section_heading(text, version)` is the one predicate `main` and `insert` ask, with `existing_date` answering the date alone (undated-heading case seen red; P3 corrected, P3b added). `c175a118` carries the ledger rows and `3ba12d83` the `survivors.md` judging two survivors of the build's range. The orchestrator re-ran at `3ba12d83`: three modules 81 passed, CI-form sweep clean, `evidence-check --strict` exit 0, tree-wide ruff clean; Executed, read only: `gh issue view 515 --json state,comments` — closed, three identical closing comments, one from the refused workflow run and two from the hand repair. The fake refuses before it records the comment, so no case sees the duplicate |
| ⬜ | The append arm re-joins the blank lines it walked back over, leaving two before the next `## ` and one extra at the end of the file | `.github/scripts/gather_changelog.py#insert` | correction | Executed with a stripped body: `- second\n\n\n## 0.1.0`, and `\n\n\n` at the end of a file whose last section took the append. Renders the same; no case reads the spacing |
| ⬜ | `existing_date` answers `None` for an undated heading that `insert` still appends into, so the dry run and the summary line disagree with the write on that shape | `.github/scripts/gather_changelog.py#existing_date`; `#main` | correction | Executed: `## 0.2.0` with no date — `existing_date` `None`, `insert` appends. The gatherer never writes that heading |
| 🟢 | S2: a refusal on both routes leaves the `size: now` label, closes every other issue, and exits non-zero at the end naming both errors and the re-run | `.github/scripts/close_issues_on_release.py#main` | verified | Executed: the module green; *label spent on an unclosed issue* 1 red, *failures never exiting* 3 red, as the P1 row records |
| 🟢 | S5/S6: three shapes masked, two stated and pinned, and the check reads the same two patterns through a callable substitution | `.github/scripts/close_issues_on_release.py#FENCE`, `#SPAN`; `.github/scripts/issue_claims_check.py#prose_only` | verified | Executed: 257 passed over the ten touched modules; the `\1` mutation red on `test_a_tilde_fence_masks_a_keyword` alone; the rider check at 25 ok |
| 🟢 | S9–S11: the shipped set is the root's `v*` tags, a tagged version is kept, a bumped untagged one refused, and a tagless checkout is loud rather than silent | `tests/test_release_hygiene.py#shipped_tags`, `#timers_in`, `#timer_offenders` | verified | Executed: the fixture case; the *shipped set empty* mutation 2 red with the real-tree case among them; in a `--no-tags` clone the real-tree case red naming `fetch-depth: 0` and the sweep case green |
| 🟢 | S12: the five-input table is true of the landed script | `.github/scripts/release_completeness_check.py#main` | verified | Executed, exit codes read from `$?`: control 0; `HEAD_BRANCH` removed 0 with the *not a release/vX.Y.Z branch* line; `REPO` removed 1 `KeyError`; the token removed 1 with `gh`'s login sentence; `HEAD_SHA` removed 0 with output identical to the control |
| 🟢 | S13/S14: the count comes off the one list call, zero speaks in three places, `None` prints one line and rolls as before | `.github/scripts/roll_flow_measurement_issue.py#comment_count`, `#main` | verified | Executed: the module green, the *missing field read as zero* mutation red on S14's case alone; the live listing's `comments` is an array |
| 🟢 | S15: step 2b reads the file and field that exist on an installed machine | `skills/update/SKILL.md` §*Procedure*, step 2b | verified | Read: `installed_plugins.json` here is keyed `specseal@specseal`, a list, first entry carrying `installPath`; the case pins the step's words |
| 🟢 | The ledger fragment's rows resolve and the two corrected rows are true of the code | `seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md`; `seal/ledger.md` R1 and S4 | verified | Executed: `bin/evidence-check --strict` exit 0, 1606 ok · 0 drifted · 0 broken. Read: `timers_in` skips `bare in shipped`; the tracker document's paragraph carries the tagged clause in both halves |
| 🟢 | The five divergences `overview.md` records are each the right call | `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/overview.md` §*Where spec and implementation diverged* | verified | Read against the phases: an aggregate measured, a fixture that could not go red, a count that rots, a red shown where it fails a release, and a runner that must keep exiting for reads |
| ❓ | The broad gate — full suite, repository-wide lint, typecheck | the sealer | out of verified scope | Not run here; the hand-back's `unverified` label is honest and the sealer answers it after the rounds settle |

## Paste-ready fixes

```python
# beside issue_state, in .github/scripts/close_issues_on_release.py
def comments_on(repo, number):
    """How many comments `number` carries, or None where the read did not say.

    The same read `issue_state` makes; taken before and after the first
    route so the fallback can tell whether that route's comment landed
    before its close was refused.
    """
    data, exists = _issue_api(repo, number)
    count = data.get("comments") if exists and isinstance(data, dict) else None
    return count if isinstance(count, int) else None


# in close_issue, replace the body from the first `attempt` to the end with:
    before = comments_on(repo, number)
    ok, first = attempt(
        "gh",
        "issue",
        "close",
        str(number),
        "--repo",
        repo,
        "--comment",
        comment,
    )
    if ok:
        return []
    ok, second = attempt(
        "gh",
        "api",
        "-X",
        "PATCH",
        f"repos/{repo}/issues/{number}",
        "-f",
        "state=closed",
    )
    if not ok:
        return [f"gh issue close: {first}", f"gh api PATCH: {second}"]
    print(
        f"closed #{number} through the REST route after `gh issue close` "
        f"was refused: {first}"
    )
    # `gh issue close --comment` posts the comment and THEN closes, so the
    # refused route usually leaves its comment behind -- measured on the
    # tracker after the previous release: the issue that run could not close
    # carries one identical comment per refused run. Where the count grew,
    # the sentence is already there. Where the read did not say, post it: a
    # duplicate is the smaller wrong answer than a close nobody explained.
    if before is not None and comments_on(repo, number) == before + 1:
        print(
            f"#{number} already carries the closing comment from the refused "
            f"`gh issue close` — not posting it again"
        )
        return []
    ok, third = attempt(
        "gh",
        "api",
        f"repos/{repo}/issues/{number}/comments",
        "-f",
        f"body={comment}",
    )
    if not ok:
        print(
            f"could not post the closing comment on #{number} through the REST "
            f"route: {third} — the issue is closed either way"
        )
    return []
```
```python
# Tracker.__init__: one more knob
    def __init__(
        self, issues, pulls, refuse_close=(), refuse_rest=(), refuse_before_comment=()
    ):
        ...
        self.refuse_before_comment = set(refuse_before_comment)

# Tracker.api, the issue arm: the count the closer reads
            return {
                "labels": [{"name": name} for name in self.issues[number]],
                "state": self.states[number],
                "comments": len(self.comments[number]),
            }, True

# Tracker.attempt, the `gh issue close` arm
        if args[:3] == ("gh", "issue", "close"):
            number = int(args[3])
            if number in self.refuse_before_comment:
                return False, GRAPHQL_REFUSAL
            # `gh issue close --comment` comments first and closes second:
            # the refused issue at the previous release carried the
            # workflow's comment, so a refusal here leaves it too.
            self.comments[number].append(args[args.index("--comment") + 1])
            if number in self.refuse_close:
                return False, GRAPHQL_REFUSAL
            self.states[number] = "closed"
            return True, ""


def test_a_refusal_before_the_comment_landed_still_gets_it_from_the_fallback(
    monkeypatch,
):
    """The other order: the comment mutation is what the tracker refused, so
    nothing is on the issue yet and the fallback has to say why it closed."""
    tracker = Tracker(THREE, CLAIMS, refuse_before_comment={2})
    mod = wire(monkeypatch, tracker)

    mod.main()

    assert tracker.states[2] == "closed"
    assert tracker.comments[2] == tracker.comments[1], tracker.comments
```
```python
        entries = block.splitlines()[2:]
        tail = lines[end:]
        while tail and not tail[0].strip():
            tail.pop(0)
        return "\n".join([*lines[:end], "", *entries, "", *tail]).rstrip("\n") + "\n"
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the ten touched modules at `bdbe575b`, in the clone (first run's exit read through a pipe, so it was re-run with the exit read directly) | exit 0, 257 passed |
| `bin/test` over `test_the_release_tail_does_not_end_at_the_tag`, `test_a_rider_reaches_its_file`, `test_no_real_identifiers`, `test_first_setup_asks_once`, `test_a_segment_feeds_the_flow_log`, `test_the_rules_have_one_owner` | exit 0, 182 passed |
| `bin/evidence-check --strict` in the clone | exit 0; 1606 ok · 0 drifted · 0 broken |
| `python3 .github/scripts/rider_check.py` | exit 0; 25 ok · 0 drifted · 0 broken |
| `git merge-base --is-ancestor` for the twenty-one commits `phases/phase-{1..7}.md` and `plan.md` name | all twenty-one are ancestors of the target |
| Six mutations from the fragment's P1, P2, P3, P4 and P6 rows, one at a time through a probe script (NAME NOT IN TREE: the script was `test_tmp_probe_536.py`, deleted), each restored with `git checkout --`, `git status --porcelain` empty after | label spent on an unclosed issue: 1 failed; failures never exiting: 3 failed; fence closed by either delimiter: 1 failed; append arm never taken: 1 failed; shipped set empty: 2 failed (the real-tree case among them); missing field read as zero: 1 failed — every count as the fragment records |
| `git clone --no-local --no-tags` of the clone, then `test_release_hygiene.py -k` the tag cases and the sweep (scratch clone deleted) | 1 failed, 3 passed: the real-tree case red with *CI checks out with `fetch-depth: 0`*; the sweep case green |
| `gather_changelog.py#insert` through the module: a stripped body appended into a non-last section, into the last section, and into an undated heading | `- second\n\n\n## 0.1.0`; file ending `\n\n\n`; `existing_date` `None` while the append happens |
| `release_completeness_check.py` against `HEAD_BRANCH=release/v1.2.3`, the clone's tip, `BASE=origin/main`, the real repository, `gh`'s configuration directory pointed at an empty scratch directory, one input removed at a time, `$?` read directly | control 0 (the *verified NOTHING* warning); `HEAD_BRANCH` removed 0; `REPO` removed 1 `KeyError: 'REPO'`; token removed 1 (`gh auth login` sentence); `HEAD_SHA` removed 0, output identical to the control |
| `gh issue view 515 --repo <owner>/<repo> --json state,comments` (read only) | `CLOSED`; 3 comments, all beginning `Closed by #524, …`, at 14:04:41Z (workflow account), 14:06:51Z and 14:07:11Z (owner) |
| `gh issue list --repo <owner>/<repo> --label flow-measurement --state open --json number,title,comments` (read only) | one issue, `comments` an array of 6 |
| `installed_plugins.json` on this machine, read through the same one-liner shape step 2b types | key `specseal@specseal`, a list, `installPath` under the plugin cache |
| The `DRY_RUN=1` closer run and the thirty-three mutations not re-applied here | not re-run: the smith's account, read as claims; the six re-applied are the sample |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet; the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The REST fallback closing a real issue after a real refusal — every case fakes both routes; this round's tracker read settles the comment order (finding 1) and not the PATCH | `overview.md` §*Not verified*, already deferred there | the repository owner, at the next release's close-issues run, reading the job log's fallback lines |
| The empty-log sentences on real issues — the live open log carries six comments today, so no real roll can show them yet | `overview.md` §*Not verified*, already deferred there | the repository owner, at the next release's roll |
| Whether GitHub acts on a closing keyword inside an HTML comment (`&lt;!-- Closes #N -->`), `questions.md` Q1 | `questions.md` Q1, already deferred there | the repository owner, by a scratch pull request into a scratch repository's default branch |
| Why the GraphQL route refused #515 twice while REST closed it at once, `questions.md` Q3 | `questions.md` Q3, already deferred there | the repository owner, when a reproduction exists |
| The earlier run's `git log a78bd149..1bafeb78: Invalid revision range` failure — `arrived()`'s force-push direction, a different class from #536, flagged by the frame for the caller to file | `spec.md` §*Out of scope* names it; no issue yet | the orchestrator, who files it |
