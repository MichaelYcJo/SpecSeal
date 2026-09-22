- **The release tail is three acts, and no document named any of them.**
  Publishing the release note, telling the plugin directory, and the
  `size: now` label the sizing rule specifies — each an act assigned to
  whoever was at the keyboard, written into no document and read by no
  machine. Three consecutive releases shipped with no release note; the
  checklist ended at the tag and had never had a step that looked at the
  directory; and the label was specified in 0.11.1 and never created, so
  three releases were cut by re-reading issue bodies the label exists to make
  unnecessary. A person has no queue this repository can read, which is why
  all three went missing the same way.

- **A `v*` tag push now publishes the GitHub Release.**
  `.github/workflows/publish-release.yml` takes the `## X.Y.Z` section the
  preparation commit already gathered and reviewed as the body, and the
  `release: X.Y.Z — <symptoms>` line `docs/release-checklist.md` §5
  prescribes as the title, read from the tagged commit's own message. A
  release already at the tag is left exactly as it is, so a re-pushed tag and
  a re-run job write nothing — the note may have been edited by hand after
  publication. Where no title line is readable the title is the tag name and
  the job log says which it used, because nothing in the tree holds that
  convention and a failed job at the tag is a release that stops after `main`
  has already moved. The one red direction is a tag whose version
  `CHANGELOG.md` carries no section for.

- **`docs/release-checklist.md` §6 stops at the tag no longer.** Two boxes
  follow it, each carrying the command that answers it: `gh release view` for
  the note, and `plugin_directory_check.py` for the directory. That command
  reads both public directory files and says, per directory, whether this
  plugin is listed, which commit the entry pins, and whether that commit is
  an ancestor of `main`. **It reports and never fails** — the directories
  sync on somebody else's schedule, one of the two has gone twenty-eight days
  without a commit, and a red nobody can act on is what this repository's
  first goal is against. Measured while building it: the manifest is at
  `.claude-plugin/marketplace.json` rather than at the repository root, an
  entry's `source` has four shapes of which two pin no commit at all, and a
  commit the local clone does not have is a third ancestry answer rather than
  an unreachable one.

- **`docs/branch-and-release.md` names the reader that arrived from outside.**
  Its squash rule enumerated the rider stamps and the round records, both of
  which this repository can repair. A plugin directory pins a commit of the
  source repository, so breaking that rule now also breaks a consumer nobody
  here can reach, for people the owner cannot name. Beside it, the sentence
  saying the plugin's name is fixed: people are already running it under that
  slug, and a rename reads to a directory as the plugin having vanished.

- **`size: now` is created by the workflow that already runs when `main`
  moves, and comes off the issue it was spent on.**
  `.github/scripts/tracker_labels.py` holds what the documents specify — name,
  colour, description and **the document that specifies each** — and creates
  what the tracker lacks, only after a read says the name is absent.
  `close_issues_on_release.py` removes the label from each issue it closes,
  after the close rather than before: an issue that closed and kept a stale
  label is a wrong answer on a tracker, and an issue left open because a label
  write failed is a release that did not finish. A gate failing a pull request
  for a missing label was rejected — it would be red on the very branch that
  adds one, since no agent in this repository's chain may write to the tracker.

- **`docs/issues-and-milestones.md` says the three things it never said**:
  where the sizing judgment is made, what removes a spent label, and that no
  sweep of the standing backlog is owed. The sentence reading *nothing reads
  this label* is now *nothing schedules from this label*, naming the one
  workflow that reads it only to spend it — the old literal had become false
  while the thing it protected was still true, and the case pinning it moved
  in the same commit.
