# Round 1 report — the release tail stops at the first issue it cannot close

Target `bdbe575ba0cde463f2b65dbaa1f818deb61057ee` on `fix/536-the-release-tail-stops-at-the-first-issue-it-cannot-close`, base `release/v0.15.0` at `cbb58091fddb9a02e3136156d7963dcd66798d1b`. Reviewed in a `git clone --no-local` of the worktree at the target SHA; nothing was written in the worktree but this file, and the clone and every probe were deleted before this report was handed over. Ran by specseal:warden on claude-fable-5-1, 2026-09-24.

## What the round did

Stage 1 read the seven phases against `spec.md` S1–S16 and the five divergences `overview.md` records. Stage 2 answered the five questions the prompt asked, by reading the landed code and by running it: the ten test modules the branch touches and six more the phases named, `evidence-check --strict`, the rider check, six of the fragment's mutations re-applied one at a time, a tagless scratch clone against the real-tree tag case, the completeness gate's five-input table re-measured, and three read-only reads of the live tracker.

The branch builds what the frame says, and the five divergences were each the right call. One thing the frame, the code and every fake agree on turned out to be false of the tracker, and it is the one finding that needs a fix: the REST fallback posts a closing comment that the refused route has, in the measured shape, already posted.

## Findings

### 🟡 1 · The fallback repeats the closing comment the refused `gh issue close` already posted

`.github/scripts/close_issues_on_release.py#close_issue` (the third `attempt`, the `gh api …/comments` write) and `tests/test_the_closer_carries_on_past_a_refusal.py#Tracker.attempt` (the `refuse_close` arm).

**What is wrong.** `close_issue` treats a refused `gh issue close --comment` as a route that wrote nothing, and posts the same comment through `gh api repos/<owner>/<repo>/issues/<n>/comments` after the PATCH. But `gh issue close --comment` posts the comment first and only then sends the close mutation, so when the close is what the tracker refuses — the shape measured at the previous release — the comment is already on the issue and the fallback writes it a second time.

**Executed, on the live tracker (read only).** `gh issue view 515 --json state,comments` answers `CLOSED` and three comments, all three beginning `Closed by #524, which shipped in the release that just reached …`: one at 14:04:41Z from the workflow account, which is the run that was refused on this issue and left it open, and two from the repository owner's hand repair at 14:06:51Z and 14:07:11Z — one per re-run of the same refused route, then one from the PATCH-and-comment pair. Every refused `gh issue close --comment` left its comment behind. The order inside `gh` (comment, then close) is read from its source and not executed here; the tracker record is the executed evidence.

**Why it matters.** The closing comment is the last thing written on an issue people go on reading, and the ticket's own docstring says so. With the fallback as built, every issue that takes it carries the same paragraph twice, and the job log's `closed #N through the REST route` line reads as if the comment had been missing. The frame's S1 says the fallback posts *the same comment*, and the ledger fragment's P1 row records that as verified; both are true of the code and false of what a person then sees on the issue, because no case models the order the tracker showed. This is the first Stage 2 question — *is the fallback reached by a real refusal shape and not only by the fakes* — and the answer is that `attempt` returns what `close_issue` branches on (`(False, stderr)`, executed by `test_attempt_answers_the_exit_code_and_the_error_rather_than_exiting`), but the fake's refusal happens before it records the comment, which is the one respect in which it is not the real shape.

**Fix.** Read the issue's comment count around the first route, through `_issue_api`, which every fake already answers, and skip the fallback comment when the count grew by one. Where the read does not say, post it: a duplicate is the smaller wrong answer than a close nobody explained. The fake records the comment before it refuses, which turns `test_the_fallback_posts_the_same_comment_the_first_route_carries` red against the current closer (two comments on #2) and green with the fix; a second knob keeps the other order — refusal before the comment landed — covered. The class (§12) is every sentence that says the fallback posts the comment: the closer's module docstring, the `close_issue` docstring, `docs/branch-and-release.md` §*One issue the tracker refuses does not leave the rest open*, the changelog fragment's first entry and the P1 ledger row; each gains *where the refused route did not already post it*. The paste-ready block is under `## Paste-ready fixes`.

### ⬜ 2 · A second gather leaves two blank lines before the next heading, and one extra at the end of the file

`.github/scripts/gather_changelog.py#insert`, the append arm.

`end` is walked back over the blank lines before the next `## ` heading, and then `lines[end:]` — which begins with exactly those blank lines — is joined after a fresh `""`. Executed with a body in the shape `fragments` reads (`f.read().strip()`): appending into a section followed by another leaves `- second\n\n\n## 0.1.0`; appending into the last section of a file leaves the file ending `\n\n\n`. Markdown renders both the same, `publish_release_note.py#section_body` still reads one section, and no case reads the spacing, so nothing ships wrong; the file gains one stray blank line per red-release repair. A three-line change is under `## Paste-ready fixes`.

### ⬜ 3 · `existing_date` and `insert` answer *does the section exist* with two different predicates

`.github/scripts/gather_changelog.py#existing_date` and `#main`.

`main` reads `existing_date(text, version)` and treats `None` as *no section*, while `insert` treats any line `heading_re(version)` matches as the section. Executed: a heading `## 0.2.0` with no date gives `existing_date` `None`, so `main` builds a block dated today and prints a fresh heading in the dry run and no `(appended into the existing section)` on the write — and `insert` then appends into the undated section anyway. The gatherer never writes an undated heading, so the shape is one a hand edit produces; the two readers should still be one. Suggested: have `main` ask `heading_re(args.version).search(text)` for existence and `existing_date` for the date alone.

## Stage 1 — the phases against the scenarios

| Scenario | Phase | Verdict (label) |
|---|---|---|
| S1 one refusal does not leave the rest open | 1 | built and executed; the comment half is finding 1 |
| S2 both routes refuse → named at the end, exit non-zero, label stays | 1 | built; executed by the module and by two re-applied mutations (label spent on an unclosed issue: 1 red; failures never exiting: 3 red) |
| S3 one `gh issue close`, no `gh issue comment` | 1 | executed: the AST case green in the module run; read: the REST comment is `gh api` |
| S4 dry run against the previous release's inputs | 1 | read as the smith's account; not re-run. The six-versus-seven divergence is right — a frame's count is an aggregate |
| S5 three masked shapes | 2 | executed: the three cases and the check's case green, and the `\1` mutation red on exactly one assertion |
| S6 two unmasked shapes stated and pinned | 2 | executed: `test_a_four_space_indented_block_is_still_read_as_a_claim` and `test_an_html_comment_is_still_read_as_a_claim` assert `["5"]` and `["6"]`, so masking either goes red |
| S7 second gather appends, first date kept | 3 | executed: the case green, the append arm's mutation red on that one case; finding 2 is the spacing |
| S8 duplicated heading refused | 3 | executed: the reader's fixture case and the real-tree case green. The divergence (red shown on the real tree, not the fixture) is right: the fixture case asserts `[("0.2.0", [3, 7])]`, so it can fail, and the real-tree case is the one that fails a release |
| S9 tagged version kept, next refused | 4 | executed: `shipped={"0.8.3"}` keeps `0.8.3` and refuses `0.9.0`; `shipped=set()` refuses both |
| S10 tags of the root being swept; tagless checkout loud | 4 | executed: fixture tags `v0.2.0` and `v-not-a-version`, offenders `0.3.0` alone; in a `--no-tags` scratch clone the real-tree case is red with the `fetch-depth: 0` sentence while the sweep case stays green, which is the silent reading S10 exists to make loud. The divergence (fixture tags the running version) is right: a tag below the running version changes no answer |
| S11 bumped and untagged still refused | 4 | executed: covered by S9's `0.9.0` half and the fixture's `0.3.0`; read: `docs/release-checklist.md:8` still says *Nothing below names a real version* |
| S12 one boundary, the measured table, no count | 5 | executed: the table re-measured (below); read: both docstrings carry it and `test_the_script_and_this_file_draw_the_input_boundary_the_same_way` holds them together. The divergence (no count word) is right on the ticket's grounds |
| S13 empty log said in three places | 6 | executed: the module's case green; read: `close_issue`, `issue_body` and `main` each carry `empty_log_note` |
| S14 unreadable count rolls as before | 6 | executed: the case green, and the *missing field read as zero* mutation red on exactly that case |
| S15 update reads the installed copy | 7 | executed: the case green; read: `installed_plugins.json` on this machine is keyed `specseal@specseal`, a list whose first entry carries `installPath`, so the one-liner in step 2b reads the shape that exists |
| S16 the documents say what changed | 1, 3, 4 | read: `docs/branch-and-release.md` and `docs/release-checklist.md` §2, §3, §6 carry the sentences; finding 1 qualifies the §*One issue the tracker refuses* paragraph |
| Data & interfaces on `close_issue` | 1 | the divergence (`attempt` beside `run`) is right: `run` is what `arrived` and `gh_json` need, and only one issue's close should not exit |

## Stage 2 — the five questions

1. **The fallback and a real refusal.** `attempt` returns `(False, stderr)` on a non-zero `gh`, and `close_issue` branches on it; a refused PATCH leaves the label on (`main` takes `continue` before `spend_label`) and both errors reach the `sys.exit` at the end. Executed by the module and by two mutations. What the fakes get wrong about the real shape is finding 1.
2. **`FENCE` and `SPAN` at the pull request.** `issue_claims_check.py#prose_only` calls `SPAN.sub(blank, FENCE.sub(blank, body))` with a callable, so the new capturing group changes nothing it reads, and the identity case still holds. Executed: 257 passed over the ten modules with the check's module among them. The two unmasked shapes are pinned by cases that assert the keyword is read.
3. **`shipped_tags` and the tagless checkout.** `git_listing(root, "tag", "--list", "v*")` runs `git -C <root>`, so the fixture's tags and not the developer's are read (executed: the fixture case). The tagless probe is in the table. The running version bumped and untagged is refused by the `shipped=set()` half of S9.
4. **The roll's count.** `main` reads `comment_count(issues[0])` off the listing `open_flow_measurement_issues` already holds — one read, no second call — and the three sentences are where the phase says. Executed on the live tracker (read only): `gh issue list --label flow-measurement --state open --json number,title,comments` answers one issue whose `comments` is an array of six, so the field the roll asks for has the shape `comment_count` reads.
5. **The 39 mutations and the two `Corrected` rows.** Six mutations re-applied, each red on the count the fragment records (table below); the other thirty-three are read as the smith's account, with the twenty-one commits the phase records name all ancestors of the target (executed: `git merge-base --is-ancestor`, 21 of 21). `evidence-check --strict` exits 0. R1's note — *at or above it and not tagged* — is true of `timers_in`, which skips `bare in shipped`; S4's note — both halves of the tracker document's paragraph carry the tagged clause — is true of `docs/issues-and-milestones.md` as landed.

## The broad gate

Not run here, and not this round's to run: the hand-back labelled it unverified with the sealer as its answerer, and that label is honest. Nothing in this report is a full-suite result. When finding 1 is fixed and verified, nothing else in this round is open, and the sealer's spawn comes due.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The REST fallback posts the closing comment a second time, because `gh issue close --comment` comments before it closes and the refused route has already left its comment on the issue | `.github/scripts/close_issues_on_release.py#close_issue`; `tests/test_the_closer_carries_on_past_a_refusal.py#Tracker.attempt` | open | Executed, read only: `gh issue view 515 --json state,comments` — closed, three identical closing comments, one from the refused workflow run and two from the hand repair. The fake refuses before it records the comment, so no case sees the duplicate |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The REST fallback closing a real issue after a real refusal — every case fakes both routes; this round's tracker read settles the comment order (finding 1) and not the PATCH | `overview.md` §*Not verified*, already deferred there | the repository owner, at the next release's close-issues run, reading the job log's fallback lines |
| The empty-log sentences on real issues — the live open log carries six comments today, so no real roll can show them yet | `overview.md` §*Not verified*, already deferred there | the repository owner, at the next release's roll |
| Whether GitHub acts on a closing keyword inside an HTML comment (`&lt;!-- Closes #N -->`), `questions.md` Q1 | `questions.md` Q1, already deferred there | the repository owner, by a scratch pull request into a scratch repository's default branch |
| Why the GraphQL route refused #515 twice while REST closed it at once, `questions.md` Q3 | `questions.md` Q3, already deferred there | the repository owner, when a reproduction exists |
| The earlier run's `git log a78bd149..1bafeb78: Invalid revision range` failure — `arrived()`'s force-push direction, a different class from #536, flagged by the frame for the caller to file | `spec.md` §*Out of scope* names it; no issue yet | the orchestrator, who files it |

## Paste-ready fixes

Finding 1. The closer, in `.github/scripts/close_issues_on_release.py`: a count read through the door every fake answers, taken around the first route, and the fallback comment skipped when the count grew.

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

Finding 1, the fake and the cases, in `tests/test_the_closer_carries_on_past_a_refusal.py`. The fake records the comment before it refuses, which is the order the tracker showed; `test_the_fallback_posts_the_same_comment_the_first_route_carries` then asserts one comment against the current closer and fails (two), which is the red-first run. A second knob keeps the other order covered.

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

Finding 1, the sentences. Each of these says the fallback posts the comment; each gains the clause *where the refused route did not already post it*: the closer's module docstring (*then the same comment through `gh api …/issues/<n>/comments`*), the `close_issue` docstring, `docs/branch-and-release.md` §*One issue the tracker refuses does not leave the rest open*, the changelog fragment's first entry, and the P1 row's clause and Notes in the ledger fragment, with the tracker read above as the row's executed grounds.

Finding 2 (⬜). In `insert`'s append arm, join the tail after its blank lines rather than before them:

```python
        entries = block.splitlines()[2:]
        tail = lines[end:]
        while tail and not tail[0].strip():
            tail.pop(0)
        return "\n".join([*lines[:end], "", *entries, "", *tail]).rstrip("\n") + "\n"
```

Needs a fix: yes — finding 1, the fallback's duplicate closing comment (🟡, with the fake's refusal order corrected so a case sees it)
Loses a record or crashes: no

## Proof block

Files opened, all in the clone at `bdbe575b` unless named otherwise: `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/{spec,plan,questions,overview,routing,changelog}.md`, its `phases/phase-1.md` through `phase-7.md`, `seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md`, the branch's diff of `.github/scripts/close_issues_on_release.py`, `gather_changelog.py`, `release_completeness_check.py`, `roll_flow_measurement_issue.py`, `docs/branch-and-release.md`, `docs/issues-and-milestones.md`, `docs/release-checklist.md`, `skills/update/SKILL.md`, `seal/ledger.md` and the ten test modules; the full `main` of the closer and of the roll, `keywords_in`, `attempt`, `section` and `insert` of the gatherer, `issue_claims_check.py#prose_only`, `tests/conftest.py#git_listing`, `bin/test`, the `fetch-depth` lines of the six workflows, `.claude-plugin/marketplace.json`, `skills/code-review/scripts/chain_check.py` lines 396–412, an earlier work item's `rounds/round-1-report.md` for the record's shape; on this machine, `/Users/x/.claude/plugins/installed_plugins.json` and the plugin cache's directory listing (read only). Executed as the table above says. The DRY_RUN run, the thirty-three mutations not re-applied, and the broad gate are read or unverified as labelled.
