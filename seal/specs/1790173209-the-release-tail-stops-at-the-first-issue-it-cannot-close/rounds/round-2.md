# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — review round 2

| Field | Value |
|---|---|
| Target SHA | 8ab72d814c509b5155fcf2e57e94dc71c96a13ec |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 538 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of the release tail, the verifying round at round 1's fixes: the range `50734814..3ba12d83` on `fix/536-the-release-tail-stops-at-the-first-issue-it-cannot-close`, three commits, plus the record commit that closed round 1. It asked whether 🟡 1 is closed as the record says — `comments_on` reads the count through `_issue_api` before and after the first route, `close_issue` skips the REST comment only when the count grew by one and posts it when the read cannot say, the fake now records the comment before it refuses so the same-comment case was red first, and the AST case still counts exactly one `gh issue close` and no `gh issue comment` — and whether the two ⬜ corrections in `gather_changelog.py` hold: the append arm leaves one blank line and one trailing newline, and `section_heading` is the one predicate `main` and `insert` ask, with the undated-heading case red first. It also asked whether the six new units the record lists are pinned by cases that would go red under the mutations the hand-back names, whether the two `survivors.md` rows judged from the build's range (`CHANGELOG.md`'s released entry and `fold_ledger.py`'s date line) are excused on grounds that hold, and whether the corrected ledger rows P1 and P3 and the added P1d and P3b state what the landed code does. A round that opens nothing needing a fix does not consume the cap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | 🟡 1 (round 1): the REST fallback posts the closing comment a second time | `.github/scripts/close_issues_on_release.py#close_issue`, `#comments_on`; `tests/test_the_closer_carries_on_past_a_refusal.py#Tracker.attempt` | verified | fixed at 611df55b, verified this round — Executed: the same-comment case red against the closer at `50734814` (1 failed, 9 passed) and green at the target; four mutations of the new unit red on 1, 1, 2 and 1 cases as the P1d row records, the other-order case among the 2; the hygiene module's AST case green in the 81; `DRY_RUN=1` against the previous release's inputs exit 0 with six `already closed`. Read: the five sentences carry the clause; `gh`'s comment-then-close order carried from round 1 |
| 🟢 | ⬜ 2 (round 1): the append arm re-joined the blank lines it walked back over | `.github/scripts/gather_changelog.py#insert` | verified | fixed at 611df55b, verified this round — Executed: the append case and the last-section case red against the gatherer at `50734814`, green at the target; *tail's blank lines kept* red on 1, *no strip at the file's end* red on 1 |
| 🟢 | ⬜ 3 (round 1): `existing_date` and `insert` answered *is there a section* with two predicates | `.github/scripts/gather_changelog.py#section_heading`, `#existing_date`, `#main` | verified | fixed at 611df55b, verified this round — Executed: the undated-heading case red against the gatherer at `50734814`, green at the target; `main` asking `existing_date` for existence red on 4, `section_heading` never finding red on 4, the dry run printing the block's heading red on 1 |
| 🟢 | The six new units are each pinned by a case that goes red under mutation | `.github/scripts/close_issues_on_release.py#comments_on`; `.github/scripts/gather_changelog.py#section_heading`; the four new cases in `tests/test_the_closer_carries_on_past_a_refusal.py` and `tests/test_the_changelog_is_gathered_at_release.py` | verified | Executed: ten mutations, each restored from `HEAD`, the table in the prose; the clone's tree clean after |
| 🟢 | The corrected P1 and P3 rows and the added P1d and P3b state what the landed code does | `seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md` P1, P1d, P3, P3b; `seal/ledger.md` the two re-read rows | verified | Read: each clause against `close_issue`, `comments_on`, `section_heading`, `existing_date`, `insert` and `main`. Executed: `bin/evidence-check --strict` exit 0, 1614 ok · 0 drifted · 0 broken |
| 🟢 | The two `survivors.md` rows are excused on grounds that hold | `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/survivors.md` | verified | Read: the changelog quote sits in a shipped section (heading at line 2106) and the fold's date line is code; #540 open on the tracker with the fold's class. Executed: both places reported at `611df55b` and `c175a118`, none at `3ba12d83` — see ⬜ 7 for why |
| ⬜ | `insert` finds the heading's line by counting `\n` while `lines` came from `splitlines()`, which breaks on more characters | `.github/scripts/gather_changelog.py#insert` | correction | Read: `CHANGELOG.md` carries none of the extra separators and `section()` writes none; the one-predicate per-line form is in the prose |
| ⬜ | The happy path reads the same issue three times through `_issue_api` before closing it, each read under the exit-on-failure contract | `.github/scripts/close_issues_on_release.py#main`; `#close_issue` | correction | Read: `issue_labels`, `issue_state`, then `comments_on`; one read could serve all three; the contract is round 1's recorded call |
| ⬜ | The `== before + 1` predicate reads a stranger's comment posted inside the window as the refused route's own | `.github/scripts/close_issues_on_release.py#close_issue` | correction | Read: seconds wide, and a stale count fails toward the duplicate; the sharper predicate is a second endpoint |
| ⬜ | `survivors.md`'s exemption is never consulted over the range CI reads; the rows' own quotes lowered the weights under the floor | `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/survivors.md` | correction | Executed: exit 1 with two places at `611df55b` and `c175a118`; exit 0 and no `exempt` line at `3ba12d83`, with and without `--exempt`; `3ba12d83` adds that file alone. Already filed as #308; deferred there |
| ❓ | The broad gate — full suite, repository-wide lint, typecheck | the sealer | out of verified scope | Not run here; the hand-back's `unverified` label is honest and the sealer answers it now that nothing is open |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `test_the_closer_carries_on_past_a_refusal.py`, `test_the_changelog_is_gathered_at_release.py`, `test_release_hygiene.py` at `8ab72d81`, exit read directly | exit 0, 81 passed |
| The two scripts checked out at `50734814` under the cases at `HEAD`, each module run once, then both restored to `HEAD` | closer: 1 failed, 9 passed (the same-comment case); gather: 3 failed, 23 passed (the append, last-section and undated-heading cases) |
| Ten mutations one at a time through a probe script (NAME NOT IN TREE: the script was `test_tmp_probe_r2_536.py`, deleted), each restored with `git checkout HEAD --`, `git status --porcelain` empty after | 1, 1, 2, 1 red over the closer; 1, 1, 4, 4, 2, 1 red over the gatherer — the table in the prose |
| `bin/evidence-check --strict` in the clone | exit 0; total 1614 ok · 0 drifted · 0 broken |
| `survivor_check.py --range cbb58091...HEAD` with every `seal/specs/*/survivors.md` as `--exempt`, the form `hygiene.yml` types; then the same range with no exemption | exit 0 both, *no removed wording is still standing*, no `exempt` line |
| `survivor_check.py` over `cbb58091..611df55b` and `cbb58091..c175a118`, no exemption | exit 1 both: `CHANGELOG.md:2252` at 3.42 and `.github/scripts/fold_ledger.py:358` at 2.00 |
| `survivor_check.py` over `cbb58091..3ba12d83` and `cbb58091...3ba12d83`, no exemption | exit 0 both, nothing reported |
| `git diff --stat c175a118 3ba12d83`; `git diff --stat 3ba12d83 8ab72d81` | one file each: `survivors.md`; `rounds/round-1.md` |
| The closer with `DRY_RUN=1`, `BEFORE=1bafeb78143bf05430177e33927905205018d9d4`, `AFTER=cbb58091fddb9a02e3136156d7963dcd66798d1b`, the real repository (a read) | exit 0; six pull requests; six issues `already closed`; nothing written |
| `ruff check` over the four edited files | exit 0, all checks passed |
| `gh issue view 540` and `gh issue view 308` on the tracker (read only) | both OPEN; #540 titled for the fold's second heading, #308 for a `survivors.md` row removing its own quote from the search |
| The clone itself: the first clone, under a generic directory name in a scratchpad other agents of this session share, was replaced mid-round by another work item's clone; this round moved that clone's HEAD once by mistake and put it back at once, then rebuilt its own clone under a distinct name and re-ran the control | control 81 passed at `8ab72d81` in the rebuilt clone; every result above that reads a commit is unaffected, and the module runs before the collision were on the first clone at the target SHA |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet; the sealer's, and due now |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/close_issues_on_release.py#close_issue`; `tests/test_the_closer_carries_on_past_a_refusal.py#Tracker.attempt` | round 1's 1 — fixed |
| round-1 | `.github/scripts/gather_changelog.py#insert` | round 1's ⬜ — correction |
| round-1 | `.github/scripts/gather_changelog.py#existing_date`; `#main` | round 1's ⬜ — correction |
| round-1 | `.github/scripts/close_issues_on_release.py#main` | round 1's 🟢 — verified |
| round-1 | `.github/scripts/close_issues_on_release.py#FENCE`, `#SPAN`; `.github/scripts/issue_claims_check.py#prose_only` | round 1's 🟢 — verified |
| round-1 | `tests/test_release_hygiene.py#shipped_tags`, `#timers_in`, `#timer_offenders` | round 1's 🟢 — verified |
| round-1 | `.github/scripts/release_completeness_check.py#main` | round 1's 🟢 — verified |
| round-1 | `.github/scripts/roll_flow_measurement_issue.py#comment_count`, `#main` | round 1's 🟢 — verified |
| round-1 | `skills/update/SKILL.md` §*Procedure*, step 2b | round 1's 🟢 — verified |
| round-1 | `seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md`; `seal/ledger.md` R1 and S4 | round 1's 🟢 — verified |
| round-1 | `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/overview.md` §*Where spec and implementation diverged* | round 1's 🟢 — verified |
| round-1 | the sealer | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `survivors.md` row's own quote lowers the weights of the phrases it quotes, so the sweep goes silent before the exemption is consulted — measured here at `3ba12d83` against `c175a118` | #308 on the tracker, already filed; the branch `fix/308-survivors-md-silences-what-it-quotes` is in flight | the #308 work item's smith and warden |
| A second `fold_ledger.py --version X.Y.Z` writes a second heading in `seal/ledger.md`, #289's class one file over | #540 on the tracker, already filed by the fix pass | the repository owner, through #540 |
