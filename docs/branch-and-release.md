# Branching and releasing

Where a branch is cut from, how it merges back, and what carries the
version. Split out of `CONTRIBUTING.md` because the merge method has to be
read before a merge, and nobody opens a contribution guide at that moment.

## Cutting a release

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

Two checks enforce the half that can be: `tests/test_chain_hooks_hardening.py`
binds the changelog to whatever `plugin.json` says, and the `hygiene` workflow
fails a release PR — one whose base is `main` — that changes `skills/`,
`agents/`, `hooks/`, `templates/` or `.claude-plugin/` without moving the
version. The tag is still yours to push — nothing in CI can do it for you.

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
discards every commit the release branch wrote, and two things point at those
commits by SHA: the `Verified … at <sha>` stamp on every `# RIDER:` comment,
and the `Target SHA` field in every `round-N.md`. After the squash the stamp
resolves for nobody, which removes the one way a reader has to tell a live
rider from a spent one; `tests/test_a_rider_reaches_its_file.py` went red for
exactly that, and the patch release after it exists to fix one line. The
round records survived only
because their feature branches had been restored to the remote first.

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
  a default clone has none of it.

  Keeping the branch is still worth something and is no longer load-bearing:
  it leaves the rounds and the verdict readable on a branch nobody merged,
  which is the only place the reason it was not merged is written down.
- **The release branch merges into `main` as a merge commit**, carrying one
  commit of its own: the one that gathers the changelog fragments into
  `## X.Y.Z — <date>` and moves `plugin.json`. Then the tag. It is also the moment every
  issue this release closes gets closed, by a workflow rather than by
  anybody's hand — the paragraphs below say how, and what to keep writing in
  a feature pull request so it has something to read.
- Feature PRs write their entry to `specs/<work-item-id>/changelog.md` and
  leave both `CHANGELOG.md` and `plugin.json` alone. The hygiene workflow asks
  for the bump only when the base is `main`, which is what makes that
  enforceable instead of habitual.

**The changelog entries arrive as fragments, and the release gathers them.**
Three branches ran in parallel on 2026-09-01 and touched 34 files. They shared
exactly one, in all three pairs, and it was `CHANGELOG.md` — nothing else
overlapped at all. The conflict is three lines and always resolvable; what it
costs is when it arrives. Nothing may be edited between the broad gate and the
pull request, so resolving one buys a second run of the whole broad gate.

So a change writes `specs/<work-item-id>/changelog.md` and leaves the shared
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
