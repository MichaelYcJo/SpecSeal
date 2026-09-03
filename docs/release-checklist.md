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
- [ ] `docs/flow.md` has every item of the release ticked except the release
      line itself.
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

## 2. Gather, fold, bump, tick

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

and tick the release's last box in `docs/flow.md`. The fold refuses while any
`seal/specs/<id>/evidence-todo.md` has an open row; that is a review that
never drained, not a release problem, and the row's work item is where it is
closed.

## 3. Verify before committing — all of it, here

The preparation commit is the first time a fragment's prose is read by the
tests that scan `CHANGELOG.md`, and the first time `seal/ledger/` is empty.
Both found something the first time. So the whole gate runs on this tree, and
every exit code is read directly rather than through a `| tail`.

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
| `test_no_loaded_file_hardcodes_the_running_version` | living prose that named the release by number the moment it became the running one. Records of a moment are listed in the test; everything else is reworded to name the change |
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
installed session is ever told about. The close-issues workflow runs on the
tag and closes every issue the changelog section names.

- [ ] Local `release/vX.Y.Z` and `main` fast-forwarded; the preparation
      branch deleted or left, either is fine.
- [ ] The next release branch is cut from `main`, not from this one.
