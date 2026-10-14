# Release checklist

The sequence in `docs/branch-and-release.md`, as the list to work down on the
day. `X.Y.Z` is the release.

## 0. Before starting

- [ ] Every work item is squash-merged into `release/vX.Y.Z`, its pull
      request's CI green **at the commit that merged**.
- [ ] **Squash the work items back to back.** `unverified_check` compares
      against `git merge-base <the base ref> HEAD`, so a sibling squashed
      after a branch forked is not that branch's removal. A ledger conflict
      at a merge of the release branch is resolved as
      `docs/the-evidence-ledger.md` §*A correction a merge dropped* says.
      **Never rebase a work item's branch**: its round records name its
      commits by `Target SHA`.
- [ ] **The milestone `release: X.Y.Z` holds what this release carries, and
      nothing else**, or `release_completeness_check.py` refuses the release
      pull request at step 5.
- [ ] No other session works in this checkout; `git status -sb` after every
      `switch`.
- [ ] **`.test_durations` is refreshed** by the recipe in `CONTRIBUTING.md`
      §*Running the checks*, from a branch cut from `release/vX.Y.Z`, into
      the preparation commit.

## 1. The preparation branch

```bash
git fetch origin
git switch -c chore/the-fragments-become-X.Y.Z origin/release/vX.Y.Z
git status -sb
```

## 2. Gather, fold, bump

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered -->
**The preparation commit gathers the changelog fragments and folds the ledger
fragments, both**, after the dry runs are read.

```bash
python3 .github/scripts/gather_changelog.py --dry-run --version X.Y.Z
python3 .github/scripts/fold_ledger.py --dry-run --version X.Y.Z
python3 .github/scripts/gather_changelog.py --version X.Y.Z
python3 .github/scripts/fold_ledger.py --version X.Y.Z
sed -i '' 's/"version": "A.B.C"/"version": "X.Y.Z"/' .claude-plugin/plugin.json
git add -A changelog/ CHANGELOG.md seal/ .claude-plugin/plugin.json
```

Stage it before §3: the suite lists files with `git ls-files`. The fold
refuses while any `seal/specs/<id>/evidence-todo.md` has an open row, a
review that never drained.
Enforced by: tests/test_the_ledger_fragments_fold_at_release.py::test_check_fails_while_a_fragment_is_left, tests/test_the_ledger_fragments_fold_at_release.py::test_the_release_pull_request_runs_the_check, .github/workflows/hygiene.yml

<!-- specs/1790208593-the-fold-writes-each-release-to-its-own-file -->
**The fold writes the release's own file, and never an older one.** It
refuses a `--version` older than the newest `seal/releases/` file, and
`--check` refuses a `seal/ledger.md` that heads a release or a work item
marked twice.
Enforced by: .github/scripts/fold_ledger.py::main, tests/test_release_hygiene.py, tests/test_the_ledger_fragments_fold_at_release.py::test_a_fold_into_an_older_release_is_refused_and_writes_nothing

<!-- specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close -->
<!-- specs/1790206437-a-second-fold-writes-a-second-heading -->
**A second gather or fold for the same version joins its section and keeps
its date**, so a fragment landing after this step is one more run; a file
heading a version twice is refused.
Enforced by: tests/test_release_hygiene.py, .github/scripts/fold_ledger.py::insert

## 2b. Settle what the release leaves behind — by hand, and not in that commit

**First, the process record. This part is never skipped.** `settle`, then
`settle --retire-process`, which removes the process record of every work item
already on `main`; no check reads that part after its release. It is a pull
request of its own, its commit carrying `: '[no-review]';` in front
(`skills/settle/SKILL.md` §*The process record leaves first, fold or no fold*).

**Then the fold**: one standing statement into `docs/` per segment `settle`
names, `fold-check` until it names nothing, then `settle --retire`. **This is a
separate branch and a separate pull request from step 2**, because policy prose
is a judgment act; a busy release skips it. **A fold is not a work item**: no
`seal/specs/` directory, and `: '[no-review]';` before each commit.

## 3. Verify before committing — all of it, here

**The whole gate runs here, every exit code read directly.**

<!-- specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep -->
**A sweep that walks a git listing judges what remains instead of stopping at
the first tracked file the disk lacks, and a case whose verdict needs the
whole corpus says so.** With fold removals unstaged, `N skipped` with reasons
naming paths is that state, not a defect.
Enforced by: tests/test_a_shrunken_corpus_declines_to_judge.py::test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard, tests/test_a_shrunken_corpus_declines_to_judge.py::test_declining_raises_the_skip_carrying_that_reason

```bash
python3 .github/scripts/gather_changelog.py --check
python3 .github/scripts/fold_ledger.py --check
python3 skills/evidence-check/scripts/evidence_check.py --strict .
uvx ruff check . && uvx ruff format --check .
bin/test -q
python3 skills/verify/scripts/unverified_check.py --baseline origin/main seal/specs/
git fetch origin '+refs/pull/*/head:refs/remotes/pull/*/head'   # chain_check needs it
python3 skills/code-review/scripts/chain_check.py --baseline origin/main
```

| Check | What its failure means here |
|---|---|
| `evidence-check --strict` | rows anchored on what the preparation edited drifted: write their re-reads with `--reverify --into seal/ledger/<unix-seconds>-fold.md --checked <date>` and fold them with a second `fold_ledger.py --version X.Y.Z` in the same commit |

## 4. Commit, push, open the first pull request

The commit is the routing question's `no work item` answer
(`skills/implement/orchestration.md` §*Question 1*), so it carries the waiver:

```bash
: '[no-review]'; git commit -m "chore: release X.Y.Z — <the fragments --version gathered>"
git push -u origin chore/the-fragments-become-X.Y.Z
gh pr create --base release/vX.Y.Z --head chore/the-fragments-become-X.Y.Z \
  --title "chore: release X.Y.Z — <the same line>" --body-file <file>
```

- [ ] CI is green on the pushed head SHA before *Squash and merge*. A body
      edit goes through `gh api -X PATCH repos/<owner>/<repo>/pulls/<n>
      -F body=@<file>`, because `gh pr edit` can fail silently.

## 5. The release pull request

```bash
gh pr create --base main --head release/vX.Y.Z \
  --title "release: X.Y.Z — <the symptoms the release answers>" --body-file <file>
```

Green once step 4 is in. Press ***Create a merge commit***.

### What a release pull request is not the right range for

<!-- specs/1788890000-the-survivor-step-runs-on-a-range-no-fix-pass-wrote -->
**The survivor check's unit is a fix pass's range, and a release is not
one**, so the step passes on that base and **prints why**: a silent skip
reads as *did not run*.
Enforced by: tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_workflow_step_skips_a_release_range_and_says_why, .github/workflows/hygiene.yml

<!-- specs/1788735085-a-loaded-file-naming-a-real-version-is-a-timer -->
**A loaded file naming a version at or above the running one, and not
tagged, is a timer**, red on the commit that writes it. The exemptions are
argued in the test.
Enforced by: tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one

<!-- specs/1789919879-the-outside-contributor-has-no-procedure -->
**A contributor whose base is wrong is told the base is wrong**, by the
guide's first section, the pull request template and the refusal itself.
Enforced by: tests/test_the_release_check_watches_what_ships.py::test_the_refusal_names_the_wrong_base_as_one_of_the_two_causes, tests/test_the_contributor_has_a_procedure.py::test_the_procedure_is_the_first_section_of_the_guide

## 6. After the merge

```bash
git tag vX.Y.Z <merge commit> && git push origin vX.Y.Z
git describe --tags     # names the release, not "<tag>-N-g<sha>"
```

**Two acts follow the tag, each a box**: the first runs the command that
answers it, the second reads what a script can and names the page that
answers the rest.
- [ ] **A GitHub Release exists at `vX.Y.Z`** — `gh release view vX.Y.Z`.
      **This box confirms the workflow fired; it is not where the note gets
      written.** If none, `gh run list --workflow publish-release.yml` says
      whether the job went red or never ran. After the note, the same
      workflow's `seal` job attaches `seal.png` in place of the glance table;
      where the table still shows, its log says why on a `::warning::` line:
      the suite at the tag did not pass, `rsvg-convert` was not installed or
      could not draw the SVG, a `gh` call failed, or the table was edited,
      published without one, or the pull requests moved between the two
      lists. That job never fails the release. By hand, from a checkout at the
      tag on a machine with `rsvg-convert`: run the suite with the broad
      gate's recorder loaded as the workflow loads it, then
      `DRY_RUN=1 python3 .github/scripts/release_seal.py` with `TAG`, `REPO`,
      `SUITE_RECORDS` and `SUITE_KEY`; attach the PNG with
      `gh release upload`, then apply the note it prints with
      `gh release edit --notes-file`.
- [ ] **The marketplace files and the directory's page have been read** —
      `python3 .github/scripts/plugin_directory_check.py`. **It reports and
      never fails**: the files sync on somebody else's schedule, and one once
      went twenty-eight days without a commit. The directory is readable from
      nowhere a script can reach. A portal listing is answered on its
      Submissions page and takes each version from its branch without a
      resubmission, live by its publish setting. A Console listing is
      answered on the Console page. SpecSeal's listing is a Console listing,
      by the repository owner's reading of the Console page on 2026-10-07,
      and takes no new version until moved to the portal
      (`claude.com/docs/directory/publish`).

- [ ] **Every issue the run named is closed** — `gh run list --workflow
      close-issues-on-release.yml --limit 1`. A red job names each issue both
      routes refused; re-run it with the run's inputs (`DRY_RUN=1` prints the
      plan):

      ```bash
      BEFORE=<github.event.before> AFTER=<github.event.after> REPO=<owner>/<repo> \
        python3 .github/scripts/close_issues_on_release.py
      ```
- [ ] The `merged: X.Y.Z` labels stay, and the next release branch is cut
      from `main`.

<!-- specs/1788789330-the-update-notice-names-the-expensive-move -->
**A notice telling somebody an update landed names the move it costs them**:
the reload, without which the update is not in force, what it is measured to
do, and what nobody has measured.
Enforced by: tests/test_version_check.py::test_the_warning_names_the_cheap_move_before_the_expensive_one, tests/test_version_check.py::test_the_warning_names_both_commands_in_order
