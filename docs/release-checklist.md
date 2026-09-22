# Release checklist

The sequence in `docs/branch-and-release.md`, as the list to work down on the
day. That document says why each step exists; this one says what to type and
what to look at before the next step, in the order the failures arrived. Every
line here was bought by a release that re-learned it.

`X.Y.Z` is the release. Nothing below names a real version, because
`tests/test_release_hygiene.py` refuses a loaded document that names the one
running.

## 0. Before starting

- [ ] Every work item of the release is squash-merged into `release/vX.Y.Z`
      and its pull request's CI was green **at the commit that merged**. A
      merge pressed while a later push was still on its way takes the earlier
      commit; the corrections then need a pull request of their own.
- [ ] **Squash the work items back to back. A squash no longer makes the
      others red.** `unverified_check` resolves its baseline to
      `git merge-base <the base ref> HEAD`, so a work item squashed into the
      release branch after a sibling forked is not that sibling's removal
      (#272). Nothing has to be merged into a stale branch for that reason and
      nothing has to be re-gated. Merge the release branch in only when a
      branch actually needs something the release branch holds; the squash
      discards the merge commit either way.
      **Never rebase a work item's branch, for any reason** — every round
      record names its branch's commits by `Target SHA` and every `# RIDER:`
      carries a `Verified … at <sha>` stamp, a rebase orphans both, and that
      is the class this repository has a patch release about. That rule
      predates the baseline repair and outlives it; it used to be written
      here as a footnote to a workaround, which is the wrong place for a
      standing rule.
      What the old footing cost, so the paragraph is not simply gone: on the
      release that found it, three of four branches each paid a release-branch
      merge, a re-run broad gate, a re-pushed pull request and a conflict in
      the release checklist every branch ticked a box in, and the cost was
      roughly quadratic in the items a release carries. That last cost is not
      payable any more — the shared checklist is gone (#351), the third file
      cured of being written by every branch.
- [ ] **The milestone `release: X.Y.Z` holds what this release is actually
      carrying, and nothing else.** Every open issue in it that is not
      shipping moves to another milestone now — a release-planning act that
      needs no code and costs a handful of edits. Leave it and the release
      pull request goes red at step 5: `release_completeness_check.py`
      refuses while the milestone claims an open issue the release branch does
      not carry, and names each one. That is the check working, and the moment
      it fires is the worst moment to do the planning. This is what
      `docs/flow.md` used to ask as *is everything in*; the file is gone
      (#351) and the question is the machine's now.
- [ ] No other Claude session is working in this checkout, and the editor is
      not about to pull. An IDE pull once switched the checkout to the release
      branch between two commands, and the preparation commit landed there.
      `git status -sb` after every `switch` is the cheap check.

## 1. The preparation branch

```bash
git fetch origin
git switch -c chore/the-fragments-become-X.Y.Z origin/release/vX.Y.Z
git status -sb          # the branch you asked for, tracking the release
```

The `release/*` ruleset takes no direct push, so the preparation commit needs
this branch and a squash merge like any other work.

## 2. Gather, fold, bump

```bash
python3 .github/scripts/gather_changelog.py --dry-run --version X.Y.Z
python3 .github/scripts/fold_ledger.py --dry-run --version X.Y.Z
```

Read both. Then:

```bash
python3 .github/scripts/gather_changelog.py --version X.Y.Z
python3 .github/scripts/fold_ledger.py --version X.Y.Z
sed -i '' 's/"version": "A.B.C"/"version": "X.Y.Z"/' .claude-plugin/plugin.json
```

The fold refuses while any `seal/specs/<id>/evidence-todo.md` has an open
row; that is a review that never drained, not a release problem, and the
row's work item is where it is closed.

## 2b. Settle what the release leaves behind — by hand, and not in that commit

```bash
settle
```

It names the released work items whose `spec.md` no `docs/` policy has
absorbed yet, grouped by the file their ledger rows anchor in. Read it, write
one standing statement per segment into `docs/`, and then:

```bash
settle --retire
```

**This is a separate branch and a separate pull request from step 2.** Writing
policy prose is a judgment act, and step 2 is two dry runs somebody reads
followed by one mechanical commit; a release that stops for a person to write
documentation is a release that stops. Nothing fails a build for an unsettled
work item, so the honest answer on a busy release is to skip this step and run
it on its own later.

`skills/settle/SKILL.md` is the procedure and carries the two things a fold
branch owes that nothing else will tell you: a `survivors.md` range-row,
because deleting shipped sections makes the survivor sweep report every
sentence of them, and an answer for every check in this repository carrying a
population floor over `seal/specs/`.

## 3. Verify before committing — all of it, here

The preparation commit is the first time a fragment's prose is read by the
tests that scan `CHANGELOG.md`, and the first time `seal/ledger/` is empty.
Both found something the first time. So the whole gate runs on this tree, and
every exit code is read directly rather than through a `| tail`.

It is also a tree where git lists tracked files the disk does not have: the
fold removes each fragment and nothing has staged the removal yet. The sweeps
that walk a git listing judge what remains instead of stopping at the first of
them, and a case whose verdict needs the whole corpus says so — so a count line
reading `… passed, N skipped` with reasons naming paths is that state rather
than something to debug. A fold alone produces no skipped case, because the
paths it removes are under `seal/ledger/` and no such case reads a corpus that
reaches there; one appears when the tree is also mid-edit somewhere a check
like that reads, under `docs/`, `skills/`, `templates/`, `tests/` or a shipped
`.py`.

```bash
python3 .github/scripts/gather_changelog.py --check
python3 .github/scripts/fold_ledger.py --check
python3 skills/evidence-check/scripts/evidence_check.py --strict .
uvx ruff check . && uvx ruff format --check .
uv run --quiet --with pytest --with pytest-xdist pytest tests/ -q -n auto
python3 skills/verify/scripts/unverified_check.py --baseline origin/main seal/specs/
git fetch origin '+refs/pull/*/head:refs/remotes/pull/*/head'
python3 skills/code-review/scripts/chain_check.py --baseline origin/main
```

What each one has caught, so a failure is recognised rather than debugged:

| Check | What it found at a release |
|---|---|
| `evidence-check --strict` | rows anchored on units the preparation edited read as drifted; `--reverify` after re-reading them, in the same commit. The total can drop across a fold: two fragments citing one coordinate identically fold into one row, and the unique-anchor count is what stays equal |
| the full suite | a gathered entry prescribed a `git mv` whose destination nothing creates; a layout test asserted `seal/ledger/` exists, and git keeps no empty directory once the fold removes the last fragment |
| `test_no_loaded_file_names_a_version_at_or_above_the_running_one` | living prose that named the release by number the moment it became the running one. Since #179 it also names one written *ahead* of the release, which used to be green until the day it shipped — a document had carried an unshipped version for three releases that way. Records of a moment are listed in the test; everything else is reworded to name the change, or to the illustrative version the test's own message points at |
| `chain_check --baseline origin/main` | exit 1 in a checkout that never fetched `refs/pull/*/head` — the fetch line above is the fix, not a lost commit. CI fetches it itself |

## 4. Commit, push, open the first pull request

The commit belongs to no work item, so the gate is waived for the one command,
in front of it and in quotes:

```bash
: '[no-review]'; git commit -m "chore: release X.Y.Z — <what the fragments say>"
git push -u origin chore/the-fragments-become-X.Y.Z
gh pr create --base release/vX.Y.Z --head chore/the-fragments-become-X.Y.Z \
  --title "chore: release X.Y.Z — <the same line>" --body-file <file>
```

The title's count of fragments is the count `--version` gathered, not the count
`--check` reports: the latter includes every fragment of every earlier release.

- [ ] **Wait for CI on the pull request head before pressing *Squash and
      merge*.** Read `gh pr checks <n>` and compare the head SHA to the one
      just pushed.
- [ ] A body edit goes through `gh api -X PATCH repos/<owner>/<repo>/pulls/<n>
      -F body=@<file>`; `gh pr edit` fails on a deprecated Projects query in
      some `gh` versions and leaves the body unchanged without saying so.

## 5. The release pull request

```bash
gh pr create --base main --head release/vX.Y.Z \
  --title "release: X.Y.Z — <the symptoms the release answers>" --body-file <file>
```

Its hygiene checks fail until step 4 is squashed in, by design. Then they go
green without a push. Press ***Create a merge commit***, never squash: the
review records and rider stamps name the release branch's commits by SHA, and a
squash discards them.

## 6. After the merge

```bash
git tag vX.Y.Z <merge commit> && git push origin vX.Y.Z
git describe --tags     # names the release, not "<tag>-N-g<sha>"
```

The version hook reads tags and nothing else; an untagged release is one no
installed session is ever told about.

**This section used to stop here, and that is what #386 measured.** Two acts
come after the tag, and neither was written down anywhere: publishing the
release note, which three consecutive releases skipped, and telling the plugin
directory, which had no step at all because until 2026-09-16 there was no
directory to tell. Both are boxes now, and each carries the command that
answers it — a box a reader cannot act on is the same defect one layer up.

```bash
gh release view vX.Y.Z                              # did the note publish
python3 .github/scripts/plugin_directory_check.py   # what the directory has
```

- [ ] **A GitHub Release exists at `vX.Y.Z`** — `gh release view vX.Y.Z`.
      The tag push fires `.github/workflows/publish-release.yml`, which
      publishes it from the `## X.Y.Z` section step 2 already gathered, with
      the title taken from the `release: X.Y.Z — <symptoms>` line step 5
      prescribes. **This box confirms the workflow fired; it is not where the
      note gets written.** Nothing there means the job went red or never ran,
      and `gh run list --workflow publish-release.yml` says which. The one
      direction that job fails in is a tag whose version `CHANGELOG.md`
      carries no section for, which is step 2 not having happened.
- [ ] **The plugin directory's answer has been read** —
      `python3 .github/scripts/plugin_directory_check.py`. It says, per
      directory, whether this plugin is listed, which commit the entry pins,
      and whether that commit is an ancestor of `main`. **It reports and never
      fails**, deliberately: the directories sync on somebody else's schedule,
      one of the two has gone twenty-eight days without a commit, and a red
      nobody can act on is what `CLAUDE.md`'s first goal is against. Not
      listed means submitting it through the form the command names, which is
      a person's act, once. Listed while pinning an older commit means the
      directory has not caught up — resubmit through the same form. Whether an
      update reaches a listed plugin on its own is readable from nowhere
      public — the work item that built this box carries it as an open
      question — and resubmitting is unnecessary under one answer and never
      wrong under either.

The close-issues workflow has already run by now. It fires when `main` moves,
which is the merge above rather than anything you do here, and it reads the
**pull request bodies** the release carries — every `Closes #N` a feature
pull request wrote, acted on at last, because GitHub reads a closing keyword
only for a pull request whose base is the default branch. It does not read
the changelog section. This paragraph said the opposite of both halves until
#359, which is how a sentence nobody could act on survived for several
releases.

Leave the `merged: X.Y.Z` labels where they are. They accumulate, one per
release, and that is deliberate: deleting a label deletes it from every issue
that ever carried it, which falsifies the record the label was created to
leave.

- [ ] Local `release/vX.Y.Z` and `main` fast-forwarded; the preparation
      branch deleted or left, either is fine.
- [ ] The next release branch is cut from `main`, not from this one.
