# Branching and releasing

Where a branch is cut from, how it merges back, and what carries the version.
The commands for the day are `docs/release-checklist.md`.

## Cutting a release

**Two things carry the version, and a release has both.**
`.claude-plugin/plugin.json` is what a session reports as loaded and what
`claude plugin update` installs. A pushed `vX.Y.Z` tag on the release commit
is what `hooks/version-check.py` reads, through `git ls-remote --tags` alone,
so an untagged release is one no installed session is told about.

```
git tag vX.Y.Z <release commit> && git push origin vX.Y.Z
git describe --tags   # must name the release, not "<tag>-N-g<sha>"
```

<!-- specs/1788302682-the-release-check-never-watched-bin -->
**A release pull request that changes what the plugin ships moves the
version.** `tests/test_chain_hooks_hardening.py` binds the changelog to
`plugin.json`, and the `hygiene` workflow fails a release PR — one whose base
is `main` — that changes `skills/`, `agents/`, `hooks/`, `templates/`, `bin/`
or `.claude-plugin/` without moving the version. Nothing in CI pushes the tag.
Enforced by: tests/test_the_release_check_watches_what_ships.py::test_every_shipping_root_is_watched, tests/test_the_release_check_watches_what_ships.py::test_the_refusal_still_fails_the_run, .github/workflows/hygiene.yml

<!-- specs/1790076050-the-release-tail-is-three-acts-no-document-names -->
**Every act the release performs once it reaches `main` belongs to a machine or
to a command that answers it, and none of them waits on somebody remembering.**
The merge to `main` fires the close-issues workflow, so the label is created
and spent before any tag exists; the tag push fires the note, because a note
names a tag.

- **The release note publishes itself.** `.github/workflows/publish-release.yml`
  fires on the `v*` tag push and publishes `changelog/X.Y.Z.md`, titled from
  the tagged commit's `release: X.Y.Z — <symptoms>` line
  (`docs/release-checklist.md` §5) or else from the tag name. It never
  republishes a release that exists, and goes red on a tag with no release
  file or no section for it. The note opens with a summary of the pull
  requests merged into `release/vX.Y.Z` — counts, one line per pull request
  under its conventional-commit type with the issues it closed, a
  `### 🙌 Thanks to` line for every author but the owner and bots — over the
  gathered section, folded, so a pull request title is a line of the note.
  **Then the release's seal is attached.** A second job runs only when this
  run created the release: it runs the suite at the tag, draws the owner's
  seal from `.github/scripts/release-seal.svg` with `rsvg-convert`, which the
  job installs, attaches it as `seal.png`, and puts the image and one line of
  counts where the glance table stood — only to one whose glance table is
  still exactly as it was generated. Any failure is a `::warning::` that
  leaves the note as published, so the seal can never turn the release red.
- **The marketplace files are read by a command that never fails a release, and
  the plugin directory by a person.** `.github/scripts/plugin_directory_check.py`
  reads the two marketplace files on GitHub — a curated catalog and a nightly
  mirror of the directory's review pipeline — and says per file whether the
  plugin has an entry and which commit it pins. The directory's own state is
  not among its answers, because no script can reach the directory. Nothing
  fires it; a person runs it at the checklist's box.
- **A label a document specifies is created and spent by a workflow.** On the
  merge to `main` the close-issues workflow runs
  `.github/scripts/tracker_labels.py --apply`, which creates every declared
  label the tracker lacks, and takes `size: now` off each issue it closes;
  `docs/issues-and-milestones.md` owns what the label means.

`docs/release-checklist.md` §6 carries a box for each of the first two.
Enforced by: tests/test_a_release_publishes_its_note.py::test_the_workflow_fires_on_the_tag_and_writes_one_release_one_asset_one_edit, tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag, tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_directory_check_reads_the_marketplace_files_and_not_the_directory, tests/test_the_release_seal_is_drawn.py::test_any_failure_leaves_the_note_as_it_was_published

### Work accumulates on a release branch

**`main` moves once per release, and work collects on a branch cut for that
release.** The marketplace clone tracks `main`, so merging is shipping and the
tag only decides whether anyone is told.

```
main ──cut──▶ release/vX.Y.Z ──cut──▶ feature branches
                    ▲                        │
                    └────── squash ──────────┘
                    │
              merge commit
                    ▼
                  main ──▶ tag
```

**Which button, for each direction.** The method is not a preference. Pick the
other one and something downstream stops resolving, so this table is the whole
rule and the paragraphs below are why.

| From | To | How | The button on GitHub |
|---|---|---|---|
| `main` | `release/vX.Y.Z` | cut a branch | — |
| `release/vX.Y.Z` | a feature branch | cut a branch | — |
| a feature branch | `release/vX.Y.Z` | **squash** | *Squash and merge* |
| the release-prep branch | `release/vX.Y.Z` | **squash** | *Squash and merge* |
| `release/vX.Y.Z` | `main` | **3-way merge** | *Create a merge commit* |
| a hotfix branch | `main` | **3-way merge** | *Create a merge commit* |

The last two rows are one rule: **anything reaching `main` is a merge commit.**

**What breaks when the last row is squashed**: a squash discards every commit
the release branch wrote, and anything naming one by SHA stops resolving.
<!-- specs/1788826000-a-stamp-names-content-not-a-commit -->
**A `# RIDER:` comment's stamp names content, never a commit, and the
`Target SHA` field in every `round-N.md` is what still names one.** So the
round records are what the merge commit keeps resolvable.
Enforced by: tests/test_a_rider_reaches_its_file.py::test_no_rider_stamp_names_a_commit, tests/test_a_rider_reaches_its_file.py::test_every_rider_stamp_resolves_and_reproduces_its_hash

<!-- specs/1790076050-the-release-tail-is-three-acts-no-document-names -->
**A third reader points at those commits now, and it is outside this
repository.** A marketplace file lists an outside plugin by pinning a commit
of its source repository, and the plugin directory serves a plugin from a
scanned commit of the branch or tag its submission tracks
(`claude.com/docs/plugins/submit`). A squash would break a consumer nobody
here can reach; `docs/release-checklist.md` §6 carries the box that reads what
is pinned.

**The plugin's name is fixed.** Everybody running it installed it under its
slug, so a rename breaks their install, and a marketplace file keys its entry
on the same name, so a rename reads there as the plugin vanishing.
`.claude-plugin/plugin.json` holds the one copy, and
`plugin_directory_check.py` reads the name from it.
Enforced by: nothing — held outside the tree: the `main` ruleset requires the merge commit, and a marketplace file pins a commit of each outside plugin's source repository on a schedule nobody here sets.

**Two rulesets enforce the method**, because the repository-wide setting is
one switch for every branch. GitHub hides the methods a ruleset excludes; both
require a pull request and have no bypass actors, so the preparation commit
takes a branch and a squash like any other work.

| Ruleset | Targets | `allowed_merge_methods` |
|---|---|---|
| Main | `main` | `merge` |
| Release branches | `release/*` | `squash` |

- **`release/vX.Y.Z` is cut from `main`**, never from the previous release
  branch: a branch that outlives its release has to be brought back to
  `main`, and nothing enforces that.
- **Feature branches are cut from the release branch** and squash back into
  it, one commit each, so the release branch reads as its changelog.
- **A squashed feature branch can be deleted, and the review still
  resolves**: `chain_check.py` reads the commits `Target SHA` names from
  `refs/pull/<N>/head`, which neither a squash nor a deletion touches, and
  `.github/workflows/hygiene.yml` fetches that namespace. The step and the two
  checks it serves ship to user repositories as `templates/hygiene.yml` at a
  shared-mode first setup; local mode installs none, because it commits
  nothing those checks read.
- **The release branch merges into `main` as a merge commit** carrying one
  commit of its own, which gathers the changelog fragments, folds the ledger
  fragments and moves `plugin.json`; then the tag. The issues the release
  closes are closed then, by a workflow rather than by anybody's hand (below).
- Feature PRs write `seal/specs/<work-item-id>/changelog.md` and leave
  `CHANGELOG.md`, `changelog/` and `plugin.json` alone; the hygiene workflow
  asks for the bump only when the base is `main`.

**The changelog entries arrive as fragments, and the release gathers them**,
because a shared changelog is the one file parallel branches all touch, and
its conflict arrives after the broad gate:

```
python3 .github/scripts/gather_changelog.py --version X.Y.Z
```

concatenates every fragment no release file carries yet into
`changelog/X.Y.Z.md`, which opens with its dated `## X.Y.Z — <date>` line, and
heads the index `CHANGELOG.md` with that line and a link. Each entry sits under
an HTML comment naming its work item. `--check` reports fragments that never
arrived, on every pull request into `main`; `--dry-run` writes nothing. There
is no accumulation section any more: the fragments replace `## Unreleased`.

**A fragment carries no line starting `## `**, which would end the released
section for the gather and the note, and **closes every fenced block and HTML
comment it opens**, which would hide the next work item's marker. The gather
refuses either, with or without `--dry-run`, naming the fragment and the line:
fix it in a pull request into the release branch, then gather again. The
ledger fold refuses an unclosed ledger fragment the same way.

**The ledger fragments fold in the same commit.**

```
python3 .github/scripts/fold_ledger.py --version X.Y.Z
```

moves each `seal/ledger/<work-item-id>.md` into the release's own
file under `## X.Y.Z — <date>`,
one `###` section per work item marked with `<!-- specs/<work-item-id> -->`,
and removes the fragment; `seal/ledger.md` keeps the rows from before the
fragments. Every row is copied byte for byte, so `evidence-check` reports the
same before and after. `--check` reports a fragment left behind, on every pull
request into `main`. A marker counts only on a live line, never in a fence, a
comment or a code span, and a `## X.Y.Z` line inside a fence heads nothing.

**The fold refuses while a verified fact has not reached the ledger.** A
reviewer lists such facts in `seal/specs/<work-item-id>/evidence-todo.md`
(`docs/one-root-by-lifetime.md` §*What happens at a release*, step 3), and the
fold and `--check` stop while any such file in the tree has an open row,
naming it. A row is open unless the file carries a live line beginning
`drained` or its first cell begins with ✅; a row inside a closed fenced
example is not a row. Every work item in the tree is read, so one released
earlier and never drained stops this release too, until a commit drains it.

**The two merge shapes are not interchangeable.** Squash into the release
branch keeps one entry per change; a merge commit into `main` keeps
`git log --first-parent main` at one line per release.

**A closing keyword does nothing when the base is `release/vX.Y.Z`.** GitHub
acts on `Closes #N` only when the pull request merges into the repository's
default branch, and that branch is `main`. The base is what decides this, not
the kind of branch: a hotfix into `main` gets the close. **Such a pull request
leaves no LINK either, though the mention survives**: no
`closingIssuesReferences` entry and no `connected` event, only the
cross-reference. **The squash commit message does not carry the keyword
either**, so the release merge closes nothing as a side effect.

**So a workflow reads the keywords instead, when the release reaches `main`.**
`.github/workflows/close-issues-on-release.yml` takes the `(#N)` out of each
squash-commit subject that arrived on `main`, reads those pull request bodies,
and closes what their keywords name; keep writing `Closes #N` in a feature pull
request body. `.github/workflows/label-merged-on-release-branch.yml` reads the
same bodies on a push to `release/*` and writes `merged: X.Y.Z` instead of a
close; `docs/issues-and-milestones.md` owns both. The closer only ever closes,
and an issue already closed is skipped rather than re-announced, so a re-run
changes nothing. A force-push is a different case and not a safe one: the
displaced SHA may be unreachable, and the run stops. `DRY_RUN=1` writes
nothing.

<!-- specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close -->
**One issue the tracker refuses does not leave the rest open.** Every issue
is attempted; a refused `gh issue close` falls back to the REST route
(`gh api -X PATCH …/issues/<n> -f state=closed`, and the comment through
`…/issues/<n>/comments` where it was not posted), each fallback is printed,
and the run exits non-zero only at the end, naming each issue both routes
refused with both errors. Re-running it with the run's `BEFORE`, `AFTER` and
`REPO` reaches the rest.
Enforced by: tests/test_the_closer_carries_on_past_a_refusal.py

```
Closes #88
```

One keyword, one number. Where one pull request answers several, the keyword
repeats before every number: GitHub's documentation asks for the full syntax
before each issue and sanctions no shorter form. `Part of #N` remains the form
for a pull request that advances an issue without finishing it.

**The version is provisional until the content settles.** Release when the
accumulated changes read as one changelog entry, not on a commit count, so
whether the number is a minor or a patch is known at the end, not at the cut;
rename the branch if the answer changes.

**`main` stays the default branch.** A fresh marketplace clone lands on the
default branch, so a release branch as the default would hand every user the
unreleased tree.
