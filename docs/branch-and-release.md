# Branching and releasing

Where a branch is cut from, how it merges back, and what carries the
version. Split out of `CONTRIBUTING.md` because the merge method has to be
read before a merge, and nobody opens a contribution guide at that moment.

## Cutting a release

The day-of list, in the order the steps run and with what each check has
caught before, is `docs/release-checklist.md`. This section is the why.

Two things carry the version and they are read by different code. Both, or the
release is invisible to the people already running the plugin.

1. `.claude-plugin/plugin.json` — the version a session reports as loaded, and
   what `claude plugin update` installs from the marketplace clone.
2. **A `vX.Y.Z` git tag on the release commit, pushed.** `hooks/version-check.py`
   asks `git ls-remote --tags` and nothing else. An untagged release is one no
   installed session is ever told about, and a user already on the previous
   version stays silent forever — the exact state the hook exists to prevent.

```
git tag vX.Y.Z <release commit> && git push origin vX.Y.Z
```

This happened: a release shipped to the marketplace untagged. Sessions on the
version before it were told a different release was out — a real one, and the
wrong one — and sessions already on that release were told nothing at all.

Check both agree before announcing anything:

```
git describe --tags   # must name the release, not "<tag>-N-g<sha>"
```

<!-- specs/1788302682-the-release-check-never-watched-bin -->
**A release pull request that changes what the plugin ships moves the
version.** Two checks enforce the half that can be: `tests/test_chain_hooks_hardening.py`
binds the changelog to whatever `plugin.json` says, and the `hygiene` workflow
fails a release PR — one whose base is `main` — that changes `skills/`,
`agents/`, `hooks/`, `templates/`, `bin/` or `.claude-plugin/` without moving
the version. The tag is still yours to push — nothing in CI can do it for you.
Enforced by: tests/test_the_release_check_watches_what_ships.py::test_every_shipping_root_is_watched, tests/test_the_release_check_watches_what_ships.py::test_the_refusal_still_fails_the_run, .github/workflows/hygiene.yml

<!-- specs/1790076050-the-release-tail-is-three-acts-no-document-names -->
**Every act the release performs once it reaches `main` belongs to a machine or
to a command that answers it, and none of them waits on somebody remembering.**
Three acts used to follow the merge that were assigned to whoever was at the
keyboard, written into no document and read by nothing — publishing the release
note, telling the plugin directory, spending the `size: now` label — and a step
a person can skip is a step that gets skipped: the note was missed three
releases running. Two different pushes fire two of them, and the difference is the
point. The merge to `main` fires the close-issues workflow, so the label is
created and spent before any tag exists. The tag push, the maintainer's last
act, fires the note, because a note has to name a tag.

- **The release note publishes itself.** `.github/workflows/publish-release.yml`
  fires on the `v*` tag push and publishes the `CHANGELOG.md` section the
  preparation commit already gathered, titled from the tagged commit's
  `release: X.Y.Z — <symptoms>` line (`docs/release-checklist.md` §5). It never
  republishes a release that exists, and falls back to the tag name when that
  line is missing or carries no symptoms. The red it exists to raise is a
  changelog with no section for the tag, which is the release shipping
  unexplained. The note opens with a summary read from the pull requests
  merged into `release/vX.Y.Z` — counts, one line per pull request under its
  conventional-commit type with the issues it closed, a `### 🙌 Thanks to`
  line for every author other than the repository owner and bots, how to
  update — and keeps the gathered section beneath it, folded (#572). A
  pull request title is therefore a line of the release note: write it as
  one.
- **The plugin directory is read by a command that never fails a release.**
  `.github/scripts/plugin_directory_check.py` says, per directory, whether the
  plugin is listed, which commit the entry pins and whether that commit is on
  `main`, and it exits 0 whatever it finds: the directories sync on somebody
  else's schedule, and a red nobody here can act on is what `CLAUDE.md`'s first
  goal is against. Nothing fires it; a person runs it at the checklist's box.
  Submitting or resubmitting is a person's act.
- **A label a document specifies is created and spent by a workflow.** When
  the release reaches `main`, the close-issues workflow runs
  `.github/scripts/tracker_labels.py --apply`, which creates every declared
  label the tracker lacks, and takes `size: now` off each issue it closes.
  `docs/issues-and-milestones.md` owns what the label means; this says only who
  performs the acts. It states the design and not the tracker's state — whether
  the label exists is what `gh label list` says.

`docs/release-checklist.md` §6 carries a box for each of the first two. The
first confirms the workflow fired and is not where the note gets written; the
second is where the command is run.
Enforced by: tests/test_a_release_publishes_its_note.py::test_the_workflow_fires_on_the_tag_and_writes_nothing_else, tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag

### Work accumulates on a release branch

The marketplace clone tracks `main`, so `claude plugin update` installs
whatever `main` holds. Merging is shipping and the tag only decides whether
anyone is told — which is why batching tags is not the way to release less
often. It would ship the content and announce nothing, the same silence as an
untagged release.

So `main` moves once per release, and work collects on a branch cut for that
release.

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
A hotfix was squashed in once, and it cost nothing only because no rider stamp
and no round record named its commits — which is a condition nobody should
have to check at the merge button, so the ruleset does not offer the choice.

**What breaks when the last row is squashed** — measured. A squash
discards every commit the release branch wrote, and anything naming one of
them by SHA stops resolving.
<!-- specs/1788826000-a-stamp-names-content-not-a-commit -->
**A `# RIDER:` comment's stamp names content, never a commit, and the
`Target SHA` field in every `round-N.md` is what still names one.** The stamp
used to read `Verified … at <sha>`, and after a squash it resolved for nobody,
which removed the one way a reader has to tell a live rider from a spent one;
`tests/test_a_rider_reaches_its_file.py` went red for exactly that, and the
patch release after it exists to fix one line. Work item `1788826000` moved
every stamp to an anchor and a hash, so a squash can no longer orphan one.
The round records survived only
because their feature branches had been restored to the remote first.
Enforced by: tests/test_a_rider_reaches_its_file.py::test_no_rider_stamp_names_a_commit, tests/test_a_rider_reaches_its_file.py::test_every_rider_stamp_resolves_and_reproduces_its_hash

<!-- specs/1790076050-the-release-tail-is-three-acts-no-document-names -->
**A third reader points at those commits now, and it is outside this
repository.** A plugin directory lists an external plugin by pinning a commit
of its source repository — measured 2026-09-22 over one directory's 310
entries, 258 point outward and **every one of them carries a `sha`**, while
the other 52 name a path inside the directory's own repository and pin nothing
at all. Ninety-six of the 258 also carry a `ref`, and 91 of those name `main`
or `master`, so the `sha` is what a reader resolves. The counts and the
command that produced them were recorded in phase 3 of work item
`1790076050-the-release-tail-is-three-acts-no-document-names`, whose marker
stands above this paragraph.
So the rule above stopped being only about readers this repository can fix.
Breaking it now also breaks a consumer nobody here can reach, and the people
it reaches are people the owner cannot name — which is the same failure as
the release that shipped untagged, with the half that made that one visible
removed.
`docs/release-checklist.md` §6 carries the box that reads what is pinned.

**The plugin's name is fixed, and that is not a style question.** Everybody
already running it installed it under its slug, so renaming it breaks their
install — and a directory listing is keyed on the same name, so a rename reads
there as the plugin having vanished rather than as the plugin having moved.
`.claude-plugin/plugin.json` holds the one copy; nothing else in the tree
should spell it, which is why the directory check reads the name out of that
file instead of carrying a literal.

**This is enforced, and it was not always.** Two rulesets do it, because the
repository-wide merge-method setting cannot: that setting is one switch for
every branch, so it can never allow a squash into the release branch while
requiring a merge commit into `main`. A ruleset targets a branch pattern, so
two of them can disagree on purpose.

| Ruleset | Targets | `allowed_merge_methods` |
|---|---|---|
| Main | `main` | `merge` |
| Release branches | `release/*` | `squash` |

The wrong button is not offered any more — GitHub hides the merge methods a
ruleset excludes. Both rulesets also require a pull request, so neither branch
takes a direct push, and there are no bypass actors: the rule applies to the
owner too.

**What that costs, and it is a real change.** The release-preparation commit
goes through a pull request as well. Gathering the changelog entries and moving
`plugin.json` used to be a commit pushed straight onto the release branch; now
it needs a branch of its own and a squash merge, like any other work. Nothing
else about the sequence below changes.

- **`release/vX.Y.Z` is cut from `main`.** Not from the previous release
  branch, and not from a long-lived branch that outlives its release. An
  accumulation branch that survives a release has to be brought back to `main`
  afterwards, and nothing enforces that — this repository ran two commits
  behind for a full release cycle before anyone noticed.
- **Feature branches are cut from the release branch** and squash back into
  it. One squashed commit per branch, so the release branch reads as the
  changelog it is about to become.
- **A squashed feature branch can be deleted, and the review still resolves.**
  The squash discards the commits its review rounds reviewed and `round-N.md`'s
  `Target SHA` still names them, so for three releases this said "do not delete
  the branch until the release reaches `main`" — a rule living in one paragraph
  and in no code. Five branches were deleted by hand anyway and a
  release pull request went red naming six commits. `chain_check.py` reads
  `refs/pull/<N>/head` now: GitHub writes it, a squash does not touch it,
  deleting the branch does not touch it, and every one of those six commits was
  sitting there. `.github/workflows/hygiene.yml` fetches the namespace, because
  a default clone has none of it. That step and the two checks it serves ship
  to user repositories as `templates/hygiene.yml`, run from a clone of this
  repository at the release installed when the `implement` skill wrote the
  file at a shared-mode first setup; local mode installs none, because the
  checks read committed files and local mode commits none.

  Keeping the branch is still worth something and is no longer load-bearing:
  it leaves the rounds and the verdict readable on a branch nobody merged,
  which is the only place the reason it was not merged is written down.
- **The release branch merges into `main` as a merge commit**, carrying one
  commit of its own: the one that gathers the changelog fragments into
  `## X.Y.Z — <date>`, folds the ledger fragments into
  `seal/releases/X.Y.Z.md`, and
  moves `plugin.json`. Then the tag. It is also the moment every
  issue this release closes gets closed, by a workflow rather than by
  anybody's hand — the paragraphs below say how, and what to keep writing in
  a feature pull request so it has something to read.
- Feature PRs write their entry to `seal/specs/<work-item-id>/changelog.md` and
  leave both `CHANGELOG.md` and `plugin.json` alone. The hygiene workflow asks
  for the bump only when the base is `main`, which is what makes that
  enforceable instead of habitual.

**The changelog entries arrive as fragments, and the release gathers them.**
Three branches ran in parallel on 2026-09-01 and touched 34 files. They shared
exactly one, in all three pairs, and it was `CHANGELOG.md` — nothing else
overlapped at all. The conflict is three lines and always resolvable; what it
costs is when it arrives. Nothing may be edited between the broad gate and the
pull request, so resolving one buys a second run of the whole broad gate.

So a change writes `seal/specs/<work-item-id>/changelog.md` and leaves the shared
file alone. Two branches cannot collide there, because no two work items share
an id. Release preparation runs:

```
python3 .github/scripts/gather_changelog.py --version X.Y.Z
```

which concatenates every fragment that is not in the file yet into a dated
section at the top. Each entry is written under an HTML comment naming its work
item — invisible to a reader, and the only link from a released entry back to
the work that produced it. `--check` reports fragments that never arrived, and
the hygiene workflow runs it on every pull request into `main`, so a release
cannot go out with a change that ships unexplained. `--dry-run` prints the
section and writes nothing.

There is no accumulation section any more. `## Unreleased` was the shared
region, and the fragments are what replaced it.

**The ledger fragments fold in the same commit.** A work item's evidence rows
go to `seal/ledger/<work-item-id>.md` for the same reason, and until the fold
existed nothing gathered those: the directory gained one file per work item forever,
and almost every pull request touched it (issue #78). After the merge there is
no branch left to queue at the file, so release preparation also runs:

```
python3 .github/scripts/fold_ledger.py --version X.Y.Z
```

which moves every fragment into `seal/releases/X.Y.Z.md`, the release's own
file under `## X.Y.Z — <date>`,
one `###` section per work item marked with `<!-- specs/<work-item-id> -->`,
and removes the fragment. `seal/ledger.md` keeps the notation and the rows
from before the fragments existed, and stops growing; the sections folded into
it before #547 move once, by `fold_ledger.py --split` at the release that
ships that change (`docs/release-checklist.md` §2). Every row is copied byte
for byte; a row is a content anchor, so `evidence-check` reports the same
thing before and after. `--dry-run` prints the section and writes nothing;
`--check` reports a fragment left behind, and the hygiene workflow runs it
beside the changelog check on every pull request into `main`.

**The fold refuses while a verified fact has not reached the ledger.** A
reviewer lists such facts in `seal/specs/<work-item-id>/evidence-todo.md`, and a
sentence that must outlive the release has to have moved into a `docs/` policy
or a ledger row before the merge (`docs/one-root-by-lifetime.md`, "What
happens at a release", step 3). So the fold, and `--check`, stop while any such
file in the tree has an open row, naming the file. A row is open unless the
file carries a live line beginning `drained` — not one quoted in a fence, a
comment or a code span — or the row's first cell begins with ✅. A row inside
a fenced example that closes is not a row (#487). Every work item in the tree is read: the step runs on a branch cut from the
release branch, which holds merged work only, so "released" and "present" are
the same set — and a work item released earlier whose file was never drained
stops this release too. The remedy is one commit that drains it.

**The two merge shapes are not interchangeable.** Squash into the release
branch keeps one entry per change; a merge commit into `main` keeps
`git log --first-parent main` at one line per release. Reversing them buries
the release history under every review round.

**A closing keyword does nothing when the base is `release/vX.Y.Z`.** GitHub
acts on `Closes #N` only when the pull request carrying it merges into the
repository's default branch, and that branch is `main`. A branch cut from the
release branch merges back into it, so nothing reads the keyword, the merge
goes through, and the issue is still open afterwards.

The base is what decides this, not the kind of branch. A hotfix taken straight
into `main` had its `Closes #N` fire — so a hotfix that goes to `main` writes
the keyword and gets the close. What follows is about everything that goes to
the release branch first, which is nearly everything.

Three pull requests wrote one into a release base and none of them fired. #37
wrote one, #38 and #39 wrote the others. All three merged, and all three were closed by hand afterwards — the first two when
somebody noticed, the third by a hand run of the very script below, during its
development. A rule that needs somebody to notice is the one this replaces.

**They left no LINK either, though the mention survives.** The formal link —
the one in an issue's sidebar, and the one `gh pr view --json
closingIssuesReferences` reports — is not created at all outside the default
branch: `[]` for all three, against a populated list for the two that went
straight to `main`, and no `connected` event on any of the three issue
timelines. What does survive is the cross-reference, so the issue still shows
the pull request mentioning it. The issue knows a pull request talked about it
and does not know one answered it.

**The squash commit message does not carry the keyword either**, so the release
merge does not fire one as a side effect. GitHub builds that message from the
branch's commit subjects, and none of the three squashes carries a closing
KEYWORD. All three do reference issues, by
bare number, which reads to a person and to nothing else. A release closes
nothing on its own.

**So a workflow reads the keywords instead, when the release reaches `main`.**
`.github/workflows/close-issues-on-release.yml` runs on a push to `main`, takes
the `(#N)` out of each squash-commit subject that arrived, reads those pull
request bodies, and closes what their keywords name. The answer was always
written down — by the session that knew which issue it was answering — and
nothing acted on it.

**A second workflow reads the same keywords earlier, and writes no close.**
`.github/workflows/label-merged-on-release-branch.yml` runs on a push to
`release/*` and puts `merged: X.Y.Z` on the issues those same bodies name, so
that a ticket already in the release stops looking like one nobody has
started (#359). It is the answer to *is this in yet*, which the paragraph
above leaves open for the length of a release; the answer to *is this done*
is still the close, still when `main` moves.
`docs/issues-and-milestones.md` owns both mechanisms and the reason the two
moments are different.

Collecting the numbers into the release pull request's own body works too, and
it is a step somebody has to remember. Three releases show what remembering is
worth. The workflow is the same act with nobody to forget it, and it needs no
new writing at all: keep putting `Closes #N` in a feature pull request body,
where it has always belonged.

It only ever closes, and an issue already closed is skipped rather than
re-announced, so a re-run changes nothing. A force-push is a different case
and not a safe one: GitHub sends the SHA the push displaced, and where the
runner cannot reach it the range fails and the run stops — which is the right
direction, and not the same as being harmless. `DRY_RUN=1` prints what it
would do and writes nothing.
Enforced by: nothing — a record rather than a rule: it measures that a plugin directory pins a commit of this repository. The rule it supports, that anything reaching `main` is a merge commit, is held outside the tree by the `main` ruleset.

<!-- specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close -->
**One issue the tracker refuses does not leave the rest open.** The run used
to die on the first `gh issue close` that failed, with every issue sorted
after it still open — measured on the release before #536, where one GraphQL
refusal left four shipped issues open. Every issue is attempted now; a
refusal on `gh issue close` falls back to the REST route (`gh api -X PATCH
…/issues/<n> -f state=closed`, then the same comment through `gh api
…/issues/<n>/comments` where the refused route did not already post it —
`gh issue close --comment` comments before it closes, so it usually did),
each fallback is printed so the job log says how
many took it, and the run exits non-zero only at the end, naming each issue
both routes refused with both errors. A partial close is repaired by
re-running the script with the run's `BEFORE`, `AFTER` and `REPO`: it skips
what is already closed and reaches the rest.
Enforced by: tests/test_the_closer_carries_on_past_a_refusal.py

```
Closes #88
```

One keyword, one number, in the body of the pull request that answers that
issue — the shape everybody already writes. Where one pull request answers
several, the keyword repeats before every number, because GitHub's
documentation asks for the full syntax before each issue and sanctions no
shorter form. What GitHub does with `Closes #88, #92` is written down nowhere,
and the workflow above does not read it as two either.

`Part of #N` remains the form for a pull request that advances an issue without
finishing it. It links for a reader and asks nothing to close.

**The version is provisional until the content settles.** Release when the
accumulated changes read as one changelog entry, not on a commit count — so
whether the number is a minor or a patch is known at the end, not at the cut.
Rename the branch if the answer changes; while it is unpushed that costs
nothing.

**`main` stays the default branch.** A fresh marketplace clone lands on the
default branch, so making a release branch the default would hand every user
the unreleased tree.
