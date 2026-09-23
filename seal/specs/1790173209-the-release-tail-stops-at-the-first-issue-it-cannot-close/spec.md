# Feature Specification: the release tail stops at the first issue it cannot close

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Step C of the `release: 0.15.0` milestone: the release tail. Eight tickets
were named for it, seven are built here and one is already shipped. Every
fix here is met for real only at the next release, so every scenario below
names how it is verified BEFORE that — a case, a fake tracker, or a dry run
against the inputs the 0.14.0 run was given.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask a person is the more expensive. Nothing here adds a question; #198's refusal shape is rejected on this clause and on the ticket's own *Done when*. |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | #363, #266 and #289's hygiene case change what a check refuses. Each carries a test seen red, a stated failure direction, a prompt budget (zero for all three), and a platform note. |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | This item's changelog entry goes to `seal/specs/<id>/changelog.md`, its rows to `seal/ledger/<id>.md`. It touches no `seal/ledger.md` row unless it removes cited code (see Data & interfaces). |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | Every fixture the phases plant uses `<owner>/<repo>`, `example.com`, `/Users/x/`. The 0.14.0 inputs are named by SHA, not by a user path. |
| `docs/branch-and-release.md` §*Cutting a release* → *So a workflow reads the keywords instead* | The closer's premise: it acts on the keywords GitHub itself would have acted on. #266 widens the masks toward that premise, never away from it. |
| `docs/issues-and-milestones.md` §*Closing one of these by hand breaks the next release* | The invariant of exactly one open `flow-measurement` issue is what #198's check must not disturb: it reads the log it is about to close and writes nothing that changes the count. |
| `docs/release-checklist.md` §2, §3, §6 | The three places the sequence is typed. #289 changes what §2's second gather does; #363 changes what §3's version check refuses; #536 and #198 change what §6's *has already run by now* paragraph can assume. |
| `skills/agent-contract/SKILL.md` §14, §15 | A fix that changes what a person sees pins the text; a new case is seen red before it is planted. Both apply to every phase. |
| `tests/test_release_hygiene.py#test_the_script_closes_and_takes_off_one_named_label_and_nothing_else` | The closer may carry exactly one `gh issue close` argv, one `gh issue edit --remove-label`, and no `issue reopen/delete/create/comment/transfer`. #536's fallback must not add a second `gh issue close` and must not comment through `gh issue comment`. |

## Scope

Judged per ticket from the tree, 2026-09-23, at `92a7e6fe` on the branch.
Every *read* claim below was read; nothing here was executed.

| Ticket | Verdict | Grounds (read) |
|---|---|---|
| #536 the closer stops at the first `gh` failure | **in scope** | `close_issues_on_release.py#run` calls `sys.exit` on any non-zero `gh`, and `main`'s close loop calls `run(...)` per issue. Run 35871516188 (2026-09-23T14:04Z, at `cbb58091`) closed #511 and died on #515 with a GraphQL error; #517–#520 stayed open. |
| #266 five masked shapes the closer gives up | **in scope, narrowed to three shapes** | `FENCE = ^```.*?^```` (column 0 only) and `SPAN = `[^`\n]*``. `issue_claims_check.py:90` already imports `CLOSING, FENCE, KEYWORDS, SPAN` from the closer, so the ticket's *should they share one pattern* question is answered by the tree: they do, and widening the closer widens the check. |
| #289 a second gather writes a second heading | **in scope** | `gather_changelog.py#insert` finds the first `## ` line and never asks whether `## <version>` exists. `test_gathering_twice_writes_one_copy` covers the no-new-fragment case only (exit 1, one copy); a NEW fragment after the first gather is unpinned. `CHANGELOG.md` at `92a7e6fe` carries no duplicate heading (measured: `grep '^## ' | uniq -d` is empty), so the 0.9.3 repair held. |
| #368 the release suite needs the fold's deletions staged | **already shipped** — drop | `fc3e1175` (#432, #282, #440; released in 0.12.1) gave `tests/conftest.py#on_disk` and `tests/test_no_real_identifiers.py#tracked_text_files` returns what is on disk. `docs/release-checklist.md` §3 now carries the paragraph *It is also a tree where git lists tracked files the disk does not have … the sweeps judge what remains*. Shape (b) of the ticket shipped; shape (a) is no longer needed. The caller closes the ticket naming that commit. |
| #363 a shipped version cannot be named until the next bump | **in scope** | `tests/test_release_hygiene.py#timers_in` refuses every token `>= as_release(running)`; `shipped_versions()` reads `CHANGELOG.md` and is used only by the illustrative-version case. No `git tag` read exists in the file. At `92a7e6fe`: `plugin.json` = `0.14.0`, `git tag --list` has `v0.14.0`, and `docs/` may not write `0.14.0`. |
| #362 three documents draw the gate's input boundary differently | **in scope** | `release_completeness_check.py:48–52` still reads *`HEAD_SHA` is the one entry whose absence is silent rather than loud* and names four inputs; `tests/test_a_release_cannot_ship_an_untrue_milestone.py:492–496` loops over five (`GH_TOKEN` included) and repeats the superlative. `main` reads `HEAD_BRANCH` with `.get(..., "")` (line 254) and `version_of("")` takes the *not a release branch* exit at line 260. |
| #198 a release closes an empty measurement log and nothing notices | **in scope** | `roll_flow_measurement_issue.py#close_issue` closes with a comment and reads nothing about the log's contents; `list_open_issues` asks `--json number,title` only. Live: #535 (after 0.14.0) has 0 comments and was opened today; #496 (after 0.13.0) had 28. |
| #157 `/specseal:update` reports the installer's line; a version dir already present is never re-extracted | **in scope** | `skills/update/SKILL.md` step 2 stops on *already current* and step 3 reads `~/.claude/plugins/marketplaces/specseal/CHANGELOG.md`, the clone; nothing reads the installed copy. `hooks/version-check.py` deliberately does not read `installed_plugins.json` and says so, which is right for a notice and is not this skill's constraint. |

**Out of scope, each with why.**

- The four-space indented block and the HTML comment, #266's other two shapes. A four-space block is the same indentation this repository's pull request bodies use for a bullet's continuation line, so masking it would drop a real `Closes #N` (the wrong direction for a closer). Whether GitHub reads a keyword inside an HTML comment is unmeasured, and a measurement needs a scratch pull request on the tracker, which is a write nobody asked for. Both stay unmasked, with the reason at the pattern, and `questions.md` carries the HTML-comment row as a measurement.
- Making a missing `HEAD_BRANCH` loud in `release_completeness_check.py` (#362). `hygiene.yml:328` always passes it; a gate change for a state no workflow produces would carry the four items of the gate rule for nothing. The docstring gets the measured table instead.
- Reading the flow log's *contents* for a `Ran by` row or a segment table (#198). The ticket's *Done when* asks that an empty cycle be said somewhere a person reads; a comment count is what the tracker can answer without parsing prose, and it is what the ticket's own table measured.
- Extraction of the installed copy by `/specseal:update` itself (#157). The skill compares and refuses the summary; the repair it names (`mv <version> <version>.stale.bak && rsync …`) is typed by the user after the skill has said why, because deleting a directory a live `.in_use/` PID holds is a person's act.
- The run at `1bafeb78` (35813340079, 03:11Z the same day) failed on `git log a78bd149..1bafeb78: Invalid revision range` — `a78bd149` is unreachable from this clone. That is `arrived()`'s documented force-push direction and a different class from #536; none of the eight tickets names it. Flagged in the report for the caller to file, not fixed here.
- The 0.14.0 interpreter-version incident the milestone names (#363's class). `VERSIONS_OF_ANOTHER_PRODUCT` is the documented route and the refusal text names it; widening `VERSION_TOKEN` or reading a product name before a number is what #363 itself puts out of scope.
- Anything in `round_record.py`, `chain_check.py` or the survivor sweep: work items A and B hold those files, and no ticket here touches them.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how (before the next release) |
|---|---|---|
| S1 · #536 one refusal does not leave the rest open | Given a push whose bodies claim #a, #b, #c and the tracker refuses `gh issue close #b` on the GraphQL route; when the closer runs; then #a and #c are closed, #b is closed through the REST route (`gh api -X PATCH repos/<owner>/<repo>/issues/<n> -f state=closed`) with the same comment posted through `gh api …/issues/<n>/comments`, and the run exits 0. | Case in `tests/test_a_declared_label_reaches_the_tracker.py`'s `Tracker` fake (or a sibling module): the fake refuses `("gh","issue","close")` for one number and accepts the PATCH; assert every state is `closed` and the exit is 0. Seen red first: at `HEAD` the fake's refusal ends the run at #b. |
| S2 · #536 a failure on both routes is named and the run finishes | Given both routes refuse #b; when the closer runs; then #a and #c still close, the label removal for each closed issue still runs, the output names #b with both errors, and the exit is non-zero **at the end**. | Same fake, both routes refusing one number. Assert the order of `calls` (close #a, close #c both attempted) and `returncode != 0`. |
| S3 · #536 the closer still carries one `gh issue close` and no `gh issue comment` | Given the fallback is in; then the AST case in `tests/test_release_hygiene.py` that counts `gh issue <verb>` argvs still passes: one `close`, one `edit`, none of the forbidden verbs. | Executed by the existing case; the phase reads it before writing the fallback, because the REST comment goes through `gh api`, not `gh issue comment`. |
| S4 · #536 dry run against the 0.14.0 inputs | Given `DRY_RUN=1 BEFORE=1bafeb78143bf05430177e33927905205018d9d4 AFTER=cbb58091fddb9a02e3136156d7963dcd66798d1b REPO=<owner>/<repo>`; when the closer runs from a clone that has both commits; then it prints the seven pull requests of that push and, for every claimed issue, `already closed` — and nothing is written. | Executed once by the phase on the real tracker with `DRY_RUN=1` (the script's own docstring is why it exists). The read is a live one; the output is recorded in the phase record, not asserted by a case. |
| S5 · #266 a tilde fence, an indented fence and a double-backtick span mask a keyword | Given a body with `Closes #1` inside `~~~ … ~~~`, `Closes #2` inside a ``` fence indented under a list item, `Closes #3` inside ` ``…`` `, and `Closes #4` in prose; when `keywords_in` reads it; then only `4` is returned. | Cases in `tests/test_release_hygiene.py` beside `test_only_a_keyword_before_a_number_closes_anything`, one per shape, each seen red at `HEAD`. `issue_claims_check.py` is checked by its own module's cases with the same bodies, because it imports the patterns. |
| S6 · #266 the two unmasked shapes are stated | Given a four-space indented block and an HTML comment each holding a keyword; then both are still read as claims, and the comment at `FENCE`/`SPAN` says so and why. The `# RIDER:` above them is retired (its question is answered here). | Two cases asserting the current reading, so a later widening is a deliberate red rather than a drift. |
| S7 · #289 a second gather for the same version appends into the existing section | Given `CHANGELOG.md` already holds `## 0.2.0 — <date A>` with one entry; when a new fragment appears and `--version 0.2.0` runs on `<date B>`; then the file holds ONE `## 0.2.0` heading, dated `<date A>`, with both entries under it in work item order, and `--check` passes. | Case in `tests/test_the_changelog_is_gathered_at_release.py` beside `test_gathering_twice_writes_one_copy`, seen red at `HEAD` (two headings). |
| S8 · #289 a duplicated heading is refused by hygiene | Given a `CHANGELOG.md` with two `## 0.2.0` headings; then a case in `tests/test_release_hygiene.py` fails naming the version and both line numbers. | The case runs against a fixture root (the file already has fixture-root cases) and against this repository's own file. Seen red with the fixture. |
| S9 · #363 a tagged version is history in a loaded file | Given the running version `0.14.0`, a tag `v0.14.0`, and no tag `v0.15.0`; when `timers_in` reads `docs/x.md` naming `0.14.0` and `0.15.0`; then `0.14.0` is kept and `0.15.0` is refused. | A sibling of `test_a_version_below_the_running_one_is_history_and_is_kept`, with a `shipped` set passed explicitly. Seen red at `HEAD`. The existing boundary case is not edited. |
| S10 · #363 the shipped set comes from tags of the root being swept, and a tagless checkout is loud | Given a fixture root with `plugin.json` at `0.2.0`, a tag `v0.1.0`, and a loaded file naming `0.1.0`, `0.2.0`, `0.3.0`; then `timer_offenders(root)` names `0.2.0` and `0.3.0` only. Given this repository's own tree; then a case asserts `git tag --list 'v*'` is non-empty, so a shallow or tagless checkout fails with a message naming `fetch-depth: 0`, never by refusing every version silently. | Fixture case (the file's `test_the_running_version_comes_from_the_root_being_swept` is the pattern). The non-empty-tags case runs on the real tree; `test.yml:49,87` and `hygiene.yml:30` set `fetch-depth: 0`. |
| S11 · #363 the release preparation commit still cannot name the version it cuts | Given the preparation commit bumped `plugin.json` to `X.Y.Z` and no `vX.Y.Z` tag exists; then `X.Y.Z` in `docs/` is still refused. | Covered by S9's `0.15.0` half; `docs/release-checklist.md`'s sentence *Nothing below names a real version* stays true and is re-read. |
| S12 · #362 both places state one boundary and the measured table | Given the module docstring and the test docstring; then both say *the inputs are what the step must pass — five*, both carry the table (`REPO` removed → `KeyError`; `HEAD_SHA` removed → range collapses, exit 0; `HEAD_BRANCH` removed → the *not a release branch* line, exit 0; `BASE` removed → default `origin/main`; `GH_TOKEN` removed → `gh` fails), and neither carries a superlative or a count. | The table is **re-measured** by the phase, one input removed at a time, exit codes read directly (§1 of the contract), against a fixture branch name — not carried from the ticket. Recorded as a ledger row with the executed label. |
| S13 · #198 an empty log is said where a person reads | Given the open `flow-measurement` issue has zero comments when the release rolls it; when `close_issue` runs; then the close comment on the old log says it closed with no measurement written, the successor's body carries one line naming the empty predecessor, the workflow prints a line, and the exit is 0. Given it has one or more comments; then nothing new is said. | Cases in `tests/test_a_release_rolls_the_flow_measurement_issue.py` with the module's `run` fake: the comment count is read through `gh issue list --json number,title,comments` (already the one list call) or `gh api …/issues/<n>` — the phase picks the one the fakes already intercept. Seen red at `HEAD`: the current comment has no such sentence. |
| S14 · #198 the count read cannot change the invariant | Given the count read fails; then the roll proceeds exactly as today and prints that the count was unreadable. | Case: the fake refuses the count read; assert close and open still happen and exit is 0. |
| S15 · #157 the update procedure reads the installed copy before it summarises | Given `installed_plugins.json` names an `installPath` whose `CHANGELOG.md` top heading is not the version the installer just reported; when the procedure runs; then it stops before step 3's summary, says the install did not land, names the two versions, and gives the repair (`mv`, `rsync` from the clone, `mkdir -p <version>/.in_use`) with the two `.in_use`/`installPath` cautions from the ticket. | A case pinning `skills/update/SKILL.md`'s text (the pattern of the row that pins its *Procedure* heading): the step exists between 2 and 3, names `installed_plugins.json`, `installPath`, the heading read, and the word *mismatch* as a stop. §14 of the contract is why prose is pinned. Seen red at `HEAD`. |
| S16 · `docs/` says what changed | `docs/branch-and-release.md` §*So a workflow reads the keywords instead* and `docs/release-checklist.md` §6's closer paragraph say the closer carries on past a refusal and how a partial close is repaired; §2 says a second gather appends; §3's table row for the version check says a tagged version is history. | Read by the reviewer against the scenarios above; pinned where an existing case already reads the sentence (`test_the_release_sequence_names_the_gather_step`, the §6 cases in `tests/test_the_release_tail_does_not_end_at_the_tag.py`). |

## Data & interfaces

- **`close_issues_on_release.py`**: `main` gains a failure list; the close
  loop no longer calls `run` (which exits) for the close itself but a
  `close_issue(repo, number, comment)` that tries `gh issue close` and, on a
  non-zero exit, `gh api -X PATCH repos/<owner>/<repo>/issues/<n> -f state=closed`
  followed by `gh api repos/<owner>/<repo>/issues/<n>/comments -f body=…`.
  Both routes are the same two writes the docstring already names. The
  docstring's *It fails loudly* paragraph is rewritten: loud at the end,
  naming every failure, after every issue was attempted. `FENCE` widens to
  ```` ^[ \t]*(```|~~~).*?^[ \t]*\1 ```` (or two patterns, the phase decides
  — one is easier to keep equal with `issue_claims_check.py`, which imports
  it); `SPAN` gains the double-backtick form. Every fake in
  `tests/test_a_declared_label_reaches_the_tracker.py`,
  `tests/test_a_merged_ticket_says_so_on_the_tracker.py` and
  `tests/test_a_release_rolls_the_flow_measurement_issue.py` that intercepts
  `("gh","issue","close")` is extended to answer the two `gh api` routes
  where the closer is the module under test (the roll's fakes are for
  #198's phase). `tests/test_a_body_naming_two_issues_claims_one.py:353–356`
  asserts `check.FENCE is closer.FENCE` and `check.SPAN is closer.SPAN`, so
  the widened patterns must stay the objects the check imports.
- **`gather_changelog.py#insert`** takes the version and, where
  `^## <version>\b` exists, appends the new entries at the end of that
  section (before the next `## `) without a second heading; `section()`'s
  heading is written only when none exists. `publish_release_note.py#section_body`
  reads from the first heading to the next `## `, so one section is what the
  release note gets.
- **`tests/test_release_hygiene.py`**: `timers_in(rel, text, running, shipped=frozenset())`;
  `shipped_tags(root)` reads `git -C <root> tag --list 'v*'` through
  `conftest.git_listing`; `timer_offenders(root, running)` passes it. The
  `seal/ledger.md` rows R1 (line 1363) and R3 (line 2040) cite
  `timers_in@a31fd794`; both claims still hold after the change (R1's *three
  exemptions and no fourth* is about exemptions, and a tagged version is
  history, not an exemption) — re-read and `--reverify`, never re-pointed.
  R3's grounds sentence *one of the two has already shipped* becomes the
  reason the number may now be written; the row is not edited, and the
  phase's own fragment carries the new claim.
- **`roll_flow_measurement_issue.py`**: `list_open_issues` asks
  `--json number,title,comments` (a comments array; its length is the count)
  or a `comment_count(repo, number)` through `try_run` — the phase picks the
  one the fakes intercept with the least change. `close_issue` and
  `issue_body` take the count. Exit codes unchanged.
- **`skills/update/SKILL.md`**: a step *2b. Read the installed copy* between
  2 and 3. Paths in it are `~/.claude/...`; no user path.
- **Fragments this item writes**: `seal/specs/<id>/changelog.md`,
  `seal/ledger/<id>.md`. It edits `seal/ledger.md` only if a phase removes a
  unit a row cites; none of the phases above removes one.

## Open questions → questions.md

`questions.md` holds no row only a person can answer. It lists the six
judgments the tickets left open that this file decided from the tree, one
measurement row (#266's HTML-comment shape), and two rows for the work.

Framed 2026-09-23 by framer, before the build.
