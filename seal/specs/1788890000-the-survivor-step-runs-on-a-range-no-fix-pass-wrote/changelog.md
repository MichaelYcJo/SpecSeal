- **The survivor check no longer runs on a release pull request, and says so
  rather than being silently skipped.** The check reports every place still
  carrying wording a range removed, and its unit is a **fix pass's range** —
  the floor it ships with was calibrated over 77 of them. A pull request into
  `main` carries the union of every work item the release holds, which is a
  range no fix pass ever writes: one item's removed wording is scored against
  four other items' prose, and each of those items was already checked at its
  own pull request. The release that shipped the check found this the only way
  it could be found, by failing its own release pull request with 72 places
  reported, none of them a survivor of the range that removed the wording. So
  the step now passes on a base of `main` and prints why, in the shape the two
  steps above it already use — a job-level skip reads as *did not run*, and
  that is the state where the next reader deletes a guard nobody can explain.
  (#180)
