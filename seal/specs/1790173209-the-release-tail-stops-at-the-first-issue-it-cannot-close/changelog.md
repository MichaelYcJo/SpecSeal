- **The release closer attempts every issue, falls back to the REST route
  where `gh issue close` is refused, and goes red only at the end (issue
  #536).** It used to exit on the first refused `gh` call, so one GraphQL
  refusal at the release before this one left four shipped issues open and
  the repair was a hand run. Now a refusal takes `gh api -X PATCH
  …/issues/<n> -f state=closed` and posts the same closing comment through
  `gh api …/issues/<n>/comments`; each fallback is printed so the job log says
  how many took it; an issue both routes refuse keeps its `size: now` label
  and is named at the end with both errors, after every other issue was
  attempted. `docs/branch-and-release.md` and `docs/release-checklist.md` §6
  say so, and the checklist gains the box that repairs a partial close by
  re-running the script with the run's `BEFORE`, `AFTER` and `REPO`.
- **The closer masks a tilde fence, a fence indented under a list item and a
  double-backtick span, so a closing keyword quoted inside any of them no
  longer closes the issue at the release (issue #266).** This changes what a
  release closes, in one direction: masking more closes fewer, and an issue
  left open is visible on the tracker and closed by a re-run where an issue
  closed on a quoted example is a false record. `issue_claims_check.py`
  imports the same two patterns, so the pull request check widens with them.
  Two shapes stay as they were, each with a case pinning it and the reason at
  the pattern: a four-space indented block, because that is also how this
  repository's pull request bodies continue a bullet, and an HTML comment,
  because whether GitHub acts on a keyword inside one is unmeasured. The
  `# RIDER:` that carried the question is retired.
- **A second `gather_changelog.py --version X.Y.Z` appends into the section
  that version already has, keeps the first gather's date, and a hygiene
  case refuses a `CHANGELOG.md` that heads one version twice (issue #289).**
  A release pull request going red and a fragment landing after the
  preparation commit is the ordinary shape, and the second gather used to
  write a second heading for it, so one release's entries read as two
  releases with the same number. The dry run says which section the entries
  join. `docs/release-checklist.md` §2 says a second gather appends.
