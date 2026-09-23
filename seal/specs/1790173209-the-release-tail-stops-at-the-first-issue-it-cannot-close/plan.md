# Implementation Plan: the release tail stops at the first issue it cannot close

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-23 by the orchestrating session, on the owner's `automation` answer, when `smith` was spawned.

## Summary

Seven tickets, seven phases, one branch. Each phase is one ticket end to end:
the code or prose, the cases seen red first, the `docs/` sentence that
changes, and the phase's rows drafted for `seal/ledger/<id>.md`. The eighth
ticket, #368, shipped in `fc3e1175` and takes no phase.

The order is the order of harm at a release. The closer first (#536, then
#266 in the same file), because a partial close is the failure 0.14.0 paid
for by hand. Then the two checks the preparation commit meets (#289's gather,
#363's version rule), then the docstrings (#362), the roll (#198), and the
skill (#157), which no release step runs.

Nothing here touches `round_record.py`, `chain_check.py`, the survivor sweep
or the review record — the files work items A and B hold.

## Technical context

- `.github/scripts/close_issues_on_release.py#run` — `sys.exit` on any
  non-zero `gh`; `#main`'s close loop calls it once per issue, so the first
  refusal ends the run with every later issue open. `#_issue_api` already
  shows the other shape: a 404 is input, anything else exits. The AST case
  `tests/test_release_hygiene.py#test_the_script_closes_and_takes_off_one_named_label_and_nothing_else`
  (line 1051) pins exactly one `gh issue close` argv, one `gh issue edit`
  with `--repo --remove-label`, and none of `reopen delete create comment
  transfer`. A REST fallback through `gh api` is outside what it counts, on
  purpose: the case reads verbs after `gh issue`.
- `FENCE`/`SPAN` (closer, lines ~88–92) with a `# RIDER:` naming #266.
  `.github/scripts/issue_claims_check.py:90` imports them, and
  `tests/test_a_body_naming_two_issues_claims_one.py:353–356` asserts identity.
- `.github/scripts/gather_changelog.py#insert` — first `## ` line, no
  version lookup. `#section` writes the heading. `publish_release_note.py#section_body`
  reads the first `## <version>` to the next `## `.
- `tests/test_release_hygiene.py#timers_in` (line 196) — ceiling is
  `as_release(running)`; `#shipped_versions` (line 191) reads `CHANGELOG.md`
  and must NOT be the shipped source (the preparation commit writes the
  heading and bumps `plugin.json` together, so it would wave the cut version
  through — #363's trap). `#timer_offenders` (line 480) takes a root;
  `conftest.git_listing(root, *args)` is the one spelling for a git listing.
- `.github/scripts/release_completeness_check.py:48–52` docstring;
  `tests/test_a_release_cannot_ship_an_untrue_milestone.py:476–497`
  (`test_every_input_the_script_reads_is_handed_to_it_by_the_step`);
  `.github/workflows/hygiene.yml:327–337` passes all five.
- `.github/scripts/roll_flow_measurement_issue.py#list_open_issues` (`--json
  number,title`), `#close_issue`, `#issue_body`, `#main`. The module's cases
  fake `run`/`try_run` by argv prefix.
- `skills/update/SKILL.md` steps 2 and 3; `seal/ledger.md:1518` pins its
  `## Procedure` heading by hash, so the row drifts and is re-read.
- Recorded 0.14.0 inputs, read from this clone: `BEFORE=1bafeb78143bf05430177e33927905205018d9d4`,
  `AFTER=cbb58091fddb9a02e3136156d7963dcd66798d1b`, `REPO=<owner>/<repo>`.
  Run 35871516188 is the failed run; its log names #511 closed, #515 refused
  by GraphQL, exit 1.

**What breaks in six months.** The REST fallback hides a GraphQL route that
fails on every issue: a release where every close took the fallback prints
seven fallback lines and exits 0, and nobody reads a green job's log. The
plan accepts that because the alternative (exit non-zero after a successful
fallback) is a red release for a repair that already happened; the fallback
line is printed per issue so the log says how many took it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #536 · REST from the start (`gh api -X PATCH` for every close) | The four fakes and the AST case pin `gh issue close` as the one close; switching routes rewrites every fake for a route nobody measured across a release, and the comment then always needs a second call. | **Rejected.** Fallback on failure keeps the pinned shape and adds one route taken only when the first refused. |
| #536 · carry on, no fallback, exit non-zero naming the failures | 0.14.0's #515 refused GraphQL twice and took REST at once; without the fallback the repair is still a hand run. | **Rejected.** Carry on AND fall back; the run exits non-zero only when both routes refused. |
| #536 · exit non-zero whenever any fallback was taken | A red job for a close that landed; the person opens the log to find nothing to repair. | **Rejected**, printed per issue instead (see *What breaks*). |
| #266 · mask all five shapes | A four-space block is a bullet continuation in this repository's bodies; masking it drops real claims (closes fewer — the safe direction, but a real loss). GitHub's reading of an HTML comment is unmeasured. | **Rejected for two shapes.** Tilde fence, indented fence, double-backtick span are masked; the other two stay, stated at the pattern; HTML comment is a measurement row in `questions.md`. |
| #266 · leave the closer, widen only `issue_claims_check.py` | It imports the closer's patterns and a case asserts identity; two definitions is the drift the import exists to prevent. | **Rejected.** One definition, widened once. |
| #266 · treat the widening as a behaviour change needing a person's yes | The closer's docstring already states the premise (GitHub reads none of these); moving toward the premise is a fix. Direction: masks more → closes fewer → an open issue is visible and re-runnable; a wrong close is a false record. | **Decided from the tree.** The changelog fragment states the direction. |
| #289 · refuse a second gather for a present version unless `--append` | Costs a flag at the moment somebody is fixing a red release, and `test_gathering_twice_writes_one_copy` already pins the no-new-fragment run as exit 1. | **Rejected.** Append into the section, keep the first date; the hygiene case is what keeps it closed. |
| #289 · append, but re-date the section to today | The release date is the first gather's; a re-date moves a published date on a red-release fix. | **Rejected.** First date kept. |
| #363 · derive *shipped* from `CHANGELOG.md` | The preparation commit writes the heading and the bump together, so the version being cut would pass — the timer the rule exists to catch. | **Rejected**, per the ticket; tags only. |
| #363 · exempt via `RECORDS_OF_A_MOMENT` / `ILLUSTRATIVE_VERSION` | None is a truthful home (the ticket enumerates why). | **Rejected.** |
| #363 · silently allow everything when no tag is readable | A shallow checkout would then refuse nothing above running. | **Rejected.** No tags → the widening does not apply (old behaviour), and a real-tree case asserts tags exist, so a tagless CI checkout is red with a message naming `fetch-depth`. |
| #362 · make a missing `HEAD_BRANCH` loud | A gate change for a state `hygiene.yml` never produces; carries the four items for nothing. | **Rejected.** Prose only; the table is re-measured, not copied. |
| #198 · refuse the roll when the log is empty | Stops a release for bookkeeping; the ticket's *Done when* says the release must still ship; `CLAUDE.md` first goal. | **Rejected.** Say it in three places (old log's close comment, new log's body, the job's output), exit 0. |
| #198 · read the log's comments for a `Ran by` row | Parsing prose in a workflow; the ticket measured by comment count and that is what the tracker answers. | **Rejected.** Count only. |
| #157 · have the skill re-extract the stale directory itself | Deleting a directory a live `.in_use/` PID holds, or the one `installPath` names, is destructive and the skill runs in the user's session; `checkpoint` territory. | **Rejected.** The skill reads, compares, refuses the summary, and prints the repair for the user to type. |
| #157 · a hook that checks the installed copy at session start | `hooks/version-check.py` deliberately reads `plugin.json` and not `installed_plugins.json`; a notice is not an installer. | **Rejected.** Skill only. |
| Split #157 and #198 into their own item | Both are small, both are release-tail surfaces, both are old, and each is one file plus cases. Splitting costs two routing declarations and two pull requests for no reviewer benefit. | **Rejected.** All seven here; #368 dropped as shipped. |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #536 · `close_issue(repo, number, comment)` in the closer: `gh issue close`, on refusal `gh api -X PATCH … -f state=closed` then `gh api …/comments -f body=…`; the loop collects failures, attempts every issue, still spends the label per closed issue, exits non-zero at the END naming each failure with both errors; docstring's *It fails loudly* rewritten; `docs/branch-and-release.md` and `docs/release-checklist.md` §6 say so and how a partial close is repaired (re-run with `BEFORE/AFTER/REPO`) | S1, S2 (fake refuses one route / both routes; seen red at `HEAD`), S3 (existing AST case green), S4 (one `DRY_RUN=1` run against the 0.14.0 inputs, output in `phases/phase-1.md`); the closer's fakes extended | 10c44097 |
| 2 | #266 · `FENCE` covers `~~~` and an indented opening; `SPAN` covers double backticks; the `# RIDER:` is retired; a comment at the patterns names the two unmasked shapes and why; changelog fragment states the direction (masks more, closes fewer) | S5 (three cases seen red), S6 (two cases pinning the unmasked shapes), `tests/test_a_body_naming_two_issues_claims_one.py` identity case green, `issue_claims_check.py`'s own cases green | 7977de1a |
| 3 | #289 · `insert(text, block, version)` appends into an existing `## <version>` section keeping its date; a `tests/test_release_hygiene.py` case refuses a duplicated `## X.Y.Z`; `docs/release-checklist.md` §2 says a second gather appends | S7 (seen red: two headings at `HEAD`), S8 (fixture seen red), `test_gathering_twice_writes_one_copy` still green | 451fd955 |
| 4 | #363 · `shipped_tags(root)` via `conftest.git_listing`; `timers_in(…, shipped=frozenset())` keeps a tagged version; `timer_offenders` passes the root's tags; a real-tree case asserts tags are readable; the refusal text's *A version BELOW the running one is history* sentence widens to *below, or tagged*; `docs/release-checklist.md` §3 table row updated; R1/R3 rows re-read and `--reverify` | S9 (seen red), S10 (fixture + real tree), S11 (0.15.0 still refused), `test_a_version_below_the_running_one_is_history_and_is_kept` unedited and green, `evidence-check --strict` green after `--reverify` | |
| 5 | #362 · both docstrings state *the inputs are the five the step must pass*, carry the re-measured table, drop the superlative and the count | S12 (table executed by the phase, one input removed at a time, exit codes read directly; recorded as an executed ledger row) | |
| 6 | #198 · the roll reads the log's comment count before closing; zero → the close comment, the successor's body and a printed line say the cycle closed with no measurement; count unreadable → roll unchanged, line printed; exit 0 in every case; `docs/issues-and-milestones.md` §*flow-measurement* says what an empty cycle produces | S13, S14 (cases with the module's fakes, seen red), the module's existing 30 cases green | |
| 7 | #157 · `skills/update/SKILL.md` step 2b reads `installed_plugins.json`'s `installPath`, compares the installed `CHANGELOG.md`'s top heading to the version the installer reported, stops before the summary on mismatch, and prints the repair with the `.in_use/` and `installPath` cautions; changelog fragment; `seal/ledger.md:1518` re-read and `--reverify` | S15 (a case pinning the step, seen red at `HEAD`) | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- No new permission, dependency, env var or workflow trigger. The closer's
  fallback uses the `issues: write` the job already holds; `gh api -X PATCH`
  on `/issues/<n>` is the REST route that closed #515 by hand.
- The version rule now reads `git tag`. CI already checks out with
  `fetch-depth: 0` in every job that runs the suite; a contributor running
  the suite in a clone without tags meets the real-tree case's message, not a
  silent pass.
- A second `gather_changelog.py --version X.Y.Z` on a red release now appends
  instead of writing a second heading; the release date stays the first
  gather's.
- `/specseal:update` gains one file read and no network call; on a mismatch
  it stops and prints a repair the user types.
- The flow-measurement roll gains one read (a comment count) and no write it
  did not already make.
