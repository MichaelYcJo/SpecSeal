# Round 2 report — the release tail stops at the first issue it cannot close

The verifying round. Target `8ab72d814c509b5155fcf2e57e94dc71c96a13ec` on `fix/536-the-release-tail-stops-at-the-first-issue-it-cannot-close`, base the release branch at `cbb58091fddb9a02e3136156d7963dcd66798d1b`. The surface is the fix range `5073481487e055c88c8deb1db1693427bda3d6f2..3ba12d83cad25584c0527e98cc01edae186cd66a` — three commits (`611df55b` code, cases and sentences; `c175a118` ledger rows; `3ba12d83` `survivors.md`) — plus `8ab72d81`, which changes `rounds/round-1.md` alone. Reviewed in a `git clone --no-local` of the worktree at the target SHA; nothing was written in the worktree but this file, and the clone's working tree was `git status --porcelain` empty after every probe. Ran by specseal:warden on claude-fable-5-1, 2026-09-24.

## What the round did

Round 1's 🟢 verdicts are inherited: the fix range touches `close_issues_on_release.py#close_issue` and `gather_changelog.py#insert`/`#main`, and none of the 🟢 rows rests on either beyond S2, which the closer's module re-executes here. Everything else in this report is about the three fixes and the six units the fix pass created.

Executed, in the clone: the three modules the fix touches (81 passed); the fix range's new cases against the code at `50734814`, which is the red-first run the hand-back claims; ten mutations one at a time over the six new units; `evidence-check --strict`; the survivor sweep in the form `hygiene.yml` types, over the range CI reads and over four narrower ones; the closer in `DRY_RUN=1` against the previous release's own inputs; ruff over the four edited files. Read: the diff of every file in the range, the landed `close_issue`, `comments_on`, `section_heading`, `existing_date`, `insert` and `main`, the fake tracker and its four new-or-changed cases, the ledger rows P1, P1d, P3 and P3b, the two `survivors.md` rows against the text they quote, the tracker's #540 and #308 (read only).

The answer the run ends on: 🟡 1 is closed as the record says, the two ⬜ corrections hold, each of the six new units goes red under at least one mutation, the ledger rows state what the landed code does, and nothing opened here needs a fix. Four ⬜ observations follow, one of them about the run's paperwork rather than the tool.

## Round 1's finding, verified

### 🟡 1 · closed — the fallback no longer repeats the comment the refused route left

`.github/scripts/close_issues_on_release.py#close_issue`, `#comments_on`; `tests/test_the_closer_carries_on_past_a_refusal.py#Tracker.attempt`.

**Read.** `comments_on(repo, number)` reads `data.get("comments")` through the same `_issue_api` that `issue_state` uses and answers `None` unless the value is an `int`. `close_issue` takes `before = comments_on(...)` ahead of the first route, and after a successful PATCH asks `comments_on(...) == before + 1` only when `before is not None`; the skip prints one line and returns, and every other shape — `before` unreadable, count unchanged, count grown by more than one — falls through to the `gh api …/issues/<n>/comments` write, as the docstring says. The fake's `gh issue close` arm now appends the comment first and refuses second, with `refuse_before_comment` as the knob for the other order, and `Tracker.api` answers `"comments": len(self.comments[number])`.

**Executed — red first.** The cases at `HEAD` against the closer at `50734814`: `1 failed, 9 passed`, the one red being `test_the_fallback_posts_the_same_comment_the_first_route_carries` — the same-comment case, red on the corrected fake exactly as the hand-back says. Against the landed code the module is green.

**Executed — the six new units under mutation.** Each restored from `HEAD` between runs, the closer's module for the closer, the gather module (and the hygiene module where the predicate is shared) for the gatherer:

| Mutation | Red |
|---|---|
| the skip never taken | 1 — the same-comment case |
| `comments_on` never counting | 1 — the same-comment case |
| the skip taken when the count did NOT grow (`== before`) | 2 — the same-comment case and the other-order case |
| the before-count never read (`before = None`) | 1 — the same-comment case |
| the tail's blank lines kept | 1 — the append case (the `\n\n\n` assertion) |
| no strip at the file's end | 1 — the last-section case |
| `main` asking `existing_date` for existence | 4 — the three ⬜ cases and the dry-run case (`found` is a string, so `.group` raises; the fragment's narrower mutation reports 1) |
| `section_heading` never finding a section | 4 — the same four, the hygiene module untouched |
| the heading's line index wrong (`at = 0`) | 2 — the append case and the last-section case |
| the dry run printing the block's heading, not the file's | 1 — the undated-heading case |

The counts for the three closer mutations and the first two gather mutations are the fragment's; the third gather mutation is red on more cases here than the row records because the shape applied was wider, which does not contradict the row.

**Executed — the AST case and the dry run.** `tests/test_release_hygiene.py` is one of the 81 and is green, so the closer still carries one `gh issue close` and reaches no `gh issue comment`. `DRY_RUN=1` with `BEFORE=1bafeb78143bf05430177e33927905205018d9d4 AFTER=cbb58091fddb9a02e3136156d7963dcd66798d1b` against the live tracker (a read; the script writes nothing in that mode): exit 0, six pull requests, six issues `already closed`, nothing written — the same lines the build's run and the hand-back report, and a dry run reaches no close, so no count is read.

**Read, carried.** `gh issue close --comment` commenting before it closes is round 1's reading of `gh`'s source and the tracker's record on #515; nothing in this range changes what it rests on, so it is carried and not re-derived.

**The five sentences.** The module docstring, the `close_issue` docstring, `docs/branch-and-release.md` §*One issue the tracker refuses does not leave the rest open*, the changelog fragment's first entry and the P1 row each carry *where the refused route did not already post it*. Read, all five.

### ⬜ 2 and ⬜ 3 · the two corrections hold

`.github/scripts/gather_changelog.py#insert`, `#section_heading`, `#existing_date`, `#main`.

**Read.** The append arm walks `end` back over the blank lines before the next heading as before, then pops the tail's own leading blank lines before the join and returns `joined.rstrip("\n") + "\n"`, so the one blank line it re-adds is the only one, and the file ends with one newline whichever section took the append. `section_heading(text, version)` is `heading_re(version).search(text)`; `existing_date` reads `.group(1)` off it and answers the date alone; `insert` asks `section_heading` and turns the match's offset into a line index; `main` asks `section_heading` for existence, `existing_date` for the date, and prints `found.group(0)` — the file's own heading — in the dry run and the summary line.

**Executed.** The three gather cases at `HEAD` against the gatherer at `50734814`: `3 failed, 23 passed`, the reds being the append case, the last-section case and the undated-heading case — the hand-back's red-first run reproduced. Green at the target. The mutation rows above cover both corrections.

## Findings this round

### ⬜ 4 · `insert` counts newlines to find the heading's line, while `lines` was split on more than newlines

`.github/scripts/gather_changelog.py#insert`, the line `at = changelog_text.count("\n", 0, found.start())`.

`lines` is `changelog_text.splitlines()`, which also breaks on `\r`, `\x0b`, `\x0c`, `\x1c`–`\x1e`, `\x85`, ` ` and ` `; the count is over `\n` alone. A changelog carrying one of those characters above the version's heading would put `at` one line early, and the entries would land one line off. The arm it replaced enumerated `lines` with the same pattern and had no such gap. Read, not executed: `CHANGELOG.md` carries none of those today, and `section()` writes none. Nothing ships wrong. The one-predicate form without the gap is `at = next(n for n, line in enumerate(lines) if section_heading(line, version))` — the same function, asked per line — and it is a sentence for the next edit of this arm rather than a fix commissioned here.

### ⬜ 5 · the happy path now reads the same issue three times before it closes it

`.github/scripts/close_issues_on_release.py#main` and `#close_issue`.

`main` reads the issue through `_issue_api` twice per issue (`issue_labels`, then `issue_state`), and `close_issue` now reads it a third time (`comments_on`) before the first route, on every issue and not only on the fallback. Each is a `gh api repos/<owner>/<repo>/issues/<n>` GET, and each is under `_issue_api`'s contract that a non-404 failure exits the run — the contract round 1 recorded as the right call for reads. Read: one read could serve state, labels and count, and a fix pass is not where that restructuring belongs. A release closes a handful of issues, so the cost is a few calls; it is noted so the next person touching `main` sees the three as one.

### ⬜ 6 · the count predicate has a window a person could step into

`.github/scripts/close_issues_on_release.py#close_issue`, the `== before + 1` comparison.

Between the before-read and the refused `gh issue close`, a comment anybody else posts on the issue grows the count by one with nothing of ours on it; the fallback then reads the growth as its own sentence, skips the write, and the issue is closed without the comment that says why — the direction the docstring calls the larger wrong answer. The window is the seconds a release job takes on one issue, and a stale count fails the other way (a duplicate), so this is a shape rather than a defect the release ships. The sharper predicate — whether the newest comment's body is `comment` — is a second endpoint and a design change, not a fix. Read.

### ⬜ 7 · `survivors.md`'s two rows are correct as records, and the range CI reads never consults them

`seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/survivors.md`.

**Read.** Row 1 quotes `CHANGELOG.md:2253`, an entry under the heading at line 2106, a shipped section; its grounds — a released entry records the rule as that release wrote it and is not rewritten later — hold, and the wording phase 4 replaced lives in `docs/issues-and-milestones.md`, which the branch corrected. Row 2 quotes `fold_ledger.py:358`, the fold's own date line; the grounds say it is code that makes no claim about the gather and that the fold's `section` writes a `## X.Y.Z — <date>` heading the way the gatherer used to, which the fold's `section` at line 190 confirms. The class is filed: #540 is open on the tracker with that title (read only).

**Executed.** Over `cbb58091..611df55b` and `cbb58091..c175a118` — the fix range before `survivors.md` landed — the sweep reports exactly those two places, at 3.42 and 2.00, exit 1. Over `cbb58091..3ba12d83` and the CI form `cbb58091...HEAD`, with the `--exempt` file and without it, the sweep reports nothing, exit 0, and prints no `exempt` line. `3ba12d83` adds `survivors.md` and nothing else (`git diff --stat c175a118 3ba12d83`: one file). So the two places went silent because the rows' own quotes put their phrases in one more file and the weights fell under the floor — the exemption was never read. That is the class #308 names (open on the tracker, read only: *a survivors.md row removes its own quote from what survivor-check searches for, so the exemption is never consulted*), and it is the tool's defect, not this branch's. The rows are still right to exist: they are the record a reader opens to argue with the decision, and the day #308 lands they are what the check will read. Paperwork, under `seal/specs/`, so a correction and not a fix; the Deferred table names #308.

## The ledger rows

`seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md` P1, P1d, P3, P3b; `seal/ledger.md`'s two re-read rows.

Read against the landed code: P1's clause now says *where the refused route did not already post it* and its `Corrected` note names the tracker read as its grounds; P1d's clause — count read before and after, the REST comment posted only where the count did not grow by one, an unreadable count posts — is `close_issue` line for line, and its three mutations are the table above; P3's `Corrected` note names both ⬜ rows and points at P3b; P3b's clause — one predicate, `existing_date` for the date alone, one blank line before the next heading, one trailing newline, the file's own heading printed — is `section_heading`, `insert` and `main` as they stand. The red-first quotes in P1d and P3b are the outputs reproduced here. Executed: `bin/evidence-check --strict` exit 0, total 1614 ok · 0 drifted · 0 broken, so every anchor in the four rows and in the two re-read `seal/ledger.md` rows (`insert@8dabc919`, `main@6473835a`) resolves to the content it hashes.

## The broad gate

Not run here and not this round's to run: the hand-back labelled it unverified with the sealer as its answerer, and that label is honest. Nothing above is a full-suite result. Nothing in this round is open, so the sealer's spawn comes due.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | 🟡 1 (round 1): the REST fallback posts the closing comment a second time | `.github/scripts/close_issues_on_release.py#close_issue`, `#comments_on`; `tests/test_the_closer_carries_on_past_a_refusal.py#Tracker.attempt` | fixed at 611df55b | Executed: the same-comment case red against the closer at `50734814` (1 failed, 9 passed) and green at the target; four mutations of the new unit red on 1, 1, 2 and 1 cases as the P1d row records, the other-order case among the 2; the hygiene module's AST case green in the 81; `DRY_RUN=1` against the previous release's inputs exit 0 with six `already closed`. Read: the five sentences carry the clause; `gh`'s comment-then-close order carried from round 1 |
| 🟢 | ⬜ 2 (round 1): the append arm re-joined the blank lines it walked back over | `.github/scripts/gather_changelog.py#insert` | fixed at 611df55b | Executed: the append case and the last-section case red against the gatherer at `50734814`, green at the target; *tail's blank lines kept* red on 1, *no strip at the file's end* red on 1 |
| 🟢 | ⬜ 3 (round 1): `existing_date` and `insert` answered *is there a section* with two predicates | `.github/scripts/gather_changelog.py#section_heading`, `#existing_date`, `#main` | fixed at 611df55b | Executed: the undated-heading case red against the gatherer at `50734814`, green at the target; `main` asking `existing_date` for existence red on 4, `section_heading` never finding red on 4, the dry run printing the block's heading red on 1 |
| 🟢 | The six new units are each pinned by a case that goes red under mutation | `.github/scripts/close_issues_on_release.py#comments_on`; `.github/scripts/gather_changelog.py#section_heading`; the four new cases in `tests/test_the_closer_carries_on_past_a_refusal.py` and `tests/test_the_changelog_is_gathered_at_release.py` | verified | Executed: ten mutations, each restored from `HEAD`, the table in the prose; the clone's tree clean after |
| 🟢 | The corrected P1 and P3 rows and the added P1d and P3b state what the landed code does | `seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md` P1, P1d, P3, P3b; `seal/ledger.md` the two re-read rows | verified | Read: each clause against `close_issue`, `comments_on`, `section_heading`, `existing_date`, `insert` and `main`. Executed: `bin/evidence-check --strict` exit 0, 1614 ok · 0 drifted · 0 broken |
| 🟢 | The two `survivors.md` rows are excused on grounds that hold | `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/survivors.md` | verified | Read: the changelog quote sits in a shipped section (heading at line 2106) and the fold's date line is code; #540 open on the tracker with the fold's class. Executed: both places reported at `611df55b` and `c175a118`, none at `3ba12d83` — see ⬜ 7 for why |
| ⬜ | `insert` finds the heading's line by counting `\n` while `lines` came from `splitlines()`, which breaks on more characters | `.github/scripts/gather_changelog.py#insert` | correction | Read: `CHANGELOG.md` carries none of the extra separators and `section()` writes none; the one-predicate per-line form is in the prose |
| ⬜ | The happy path reads the same issue three times through `_issue_api` before closing it, each read under the exit-on-failure contract | `.github/scripts/close_issues_on_release.py#main`; `#close_issue` | correction | Read: `issue_labels`, `issue_state`, then `comments_on`; one read could serve all three; the contract is round 1's recorded call |
| ⬜ | The `== before + 1` predicate reads a stranger's comment posted inside the window as the refused route's own | `.github/scripts/close_issues_on_release.py#close_issue` | correction | Read: seconds wide, and a stale count fails toward the duplicate; the sharper predicate is a second endpoint |
| ⬜ | `survivors.md`'s exemption is never consulted over the range CI reads; the rows' own quotes lowered the weights under the floor | `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/survivors.md` | correction | Executed: exit 1 with two places at `611df55b` and `c175a118`; exit 0 and no `exempt` line at `3ba12d83`, with and without `--exempt`; `3ba12d83` adds that file alone. Already filed as #308; deferred there |
| ❓ | The broad gate — full suite, repository-wide lint, typecheck | the sealer | out of verified scope | Not run here; the hand-back's `unverified` label is honest and the sealer answers it now that nothing is open |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `survivors.md` row's own quote lowers the weights of the phrases it quotes, so the sweep goes silent before the exemption is consulted — measured here at `3ba12d83` against `c175a118` | #308 on the tracker, already filed; the branch `fix/308-survivors-md-silences-what-it-quotes` is in flight | the #308 work item's smith and warden |
| A second `fold_ledger.py --version X.Y.Z` writes a second heading in `seal/ledger.md`, #289's class one file over | #540 on the tracker, already filed by the fix pass | the repository owner, through #540 |

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened, in the clone at `8ab72d81` unless named otherwise: `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/rounds/round-1.md` and `round-1-report.md`, its `survivors.md` and `changelog.md`, the directory listing of the work item; the range's diff of `.github/scripts/close_issues_on_release.py`, `.github/scripts/gather_changelog.py`, `docs/branch-and-release.md`, `seal/ledger.md`, `seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md`, `tests/test_the_changelog_is_gathered_at_release.py`, `tests/test_the_closer_carries_on_past_a_refusal.py`; the landed `_issue_api`, `issue_state`, `comments_on`, `close_issue` and `main` of the closer; the landed `section`, `heading_re`, `section_heading`, `existing_date`, `insert` and `main` of the gatherer; the whole closer test module; `bin/test`; `.github/workflows/hygiene.yml` lines 215–262; `.github/scripts/fold_ledger.py#section` and its date line; `CHANGELOG.md` line 2253 and the headings above it; the `exempt`, floor and examined-files lines of `skills/code-review/scripts/survivor_check.py`; the verdict-word lines of `skills/code-review/scripts/round_record.py`. Executed as the table above says; carried from round 1 as labelled; the broad gate unverified and the sealer's.
