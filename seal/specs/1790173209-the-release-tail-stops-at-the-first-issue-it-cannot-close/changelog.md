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
