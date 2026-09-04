- **A measurement that only meant something across versions was being written
  to the issue the next release deletes.** Two issues collect the same shape
  of comment — the rolling `flow-measurement` log, which
  `.github/scripts/roll_flow_measurement_issue.py` closes and replaces every
  time a release reaches `main`, and a durable ledger that is kept across
  versions — and `skills/verify/SKILL.md`'s "Measure the segment, and feed the
  flow log" named only the first. So a rate held against a previous version's
  baseline went where it would be discarded, which happened on 2026-09-04 and
  is what #136 opened for. The section now says which reading goes to which: a
  segment's own numbers to the rolling log, readings that span versions to the
  durable one. **A repository declares its durable log with a `flow-baseline`
  label** — the same lookup shape as the rolling one, a label rather than a
  number, and the same exactly-one-open invariant. A repository that never
  creates it is unaffected, because an absent label is the no-op it already
  was.
  **Zero open used to be one fact and is now two.** A repository that never
  measured and one whose log stopped both read zero, and only the second is a
  broken invariant. `gh issue list --label flow-measurement --state all` tells
  them apart for one call. A session that finds the second **names it and
  opens nothing**: two sessions finishing segments at the same moment would
  both read zero and both create, and the next release then fails on two or
  more, which is the same invariant broken from the other side.
  **Every rolling log used to be born empty.** The roll passed `--body ""`, so
  a new log said nothing about what it was for and carried no path back to the
  one it replaced. It now opens carrying the issue it rolls from, the version
  it closes on, and the durable ledger — found by the `flow-baseline` label
  rather than hardcoded, and left out of the sentence entirely where a
  repository has none.
  **The same create asks for this repository's index label and its `log:`
  milestone, and neither can fail a release.** A milestone is repository state
  that gets renamed and deleted, and `gh issue create` fails the whole call on
  a name it cannot resolve, while the invariant this script protects is the
  one-open rule that no milestone touches. The create is attempted with both,
  then with the label alone, then with neither, and each fallback writes into
  the body of the issue it opens what the attempt above it could not set — the
  body, because that is the artifact a person opens and a workflow log is not.
  A failed attempt re-reads the open-issue list before retrying, so a create
  that reported failure after it had actually landed ends the ladder instead
  of opening a second issue.
  **This repository's own durable log (`#51`) carries the new label**, so the
  0.9.0 log opens pointing at it without anything further being done by hand.
  (#136)
