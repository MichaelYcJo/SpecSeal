<!-- specs/1788826000-a-stamp-names-content-not-a-commit -->

### Fixed

- **A rider comment's verification stamp names the content it was checked
  against, not a commit.** Every `# RIDER:` in the tree carried a
  `Verified <date> at <sha>` line, and a feature branch squashes into its
  release branch — which keeps none of the branch's own commits, so the check
  failed on the release branch with nobody who caused it looking, and every
  pull request into that branch failed until somebody re-pointed it by hand.
  A stamp now reads `Verified <date> against <anchor>@<hash>`, using the same
  anchors the evidence ledger uses, and the check makes no git call at all: a
  squash, a rebase and a shallow clone are invisible to it.
  A drifted rider names the unit that changed and says to re-read the comment,
  which is what a rider is for. `.github/scripts/rider_check.py` checks them
  and `--reverify` re-stamps them — rewriting the hash wherever it moved, and
  the date only beside a hash that moved, because a stamp whose content has
  not changed records a reading nobody repeated. `--reverify --only` takes a
  file rather than a rider, and the drift message now says so.
- **A `## RIDER:` heading in a markdown file no longer breaks the build.** `#`
  opens a comment in Python, YAML and shell, and in markdown it opens a
  heading — so a heading naming the marker was read as a rider carrying no
  stamp, and the check exited 2 on a line nobody wrote as a rider. Markdown's
  rider form is the HTML comment, and that is now the only form read there.
  Every other thing this check gives up loses an alarm; this was the one place
  it invented one.
- **`--only` no longer reports success for a run that ignored it.** A path no
  rider carries printed `0 restamped · 0 refused` at exit 0, so a typo in the
  path read as *nothing needed doing* — and exit 0 is the answer a script
  reads. It is now refused by name. `--only` without `--reverify`, and beside
  `--migrate`, were ignored the same way and read the whole tree; both are
  refused before anything is read.
- **Three riders were held by nothing.** The scanned roots covered four
  directories and riders live in six, so the one in
  `.github/scripts/fold_ledger.py` and two under `tests/` were checked by no
  case at all — and one of those had never carried a stamp in any form.
- **A round record's `Target SHA` stays as it is, and `templates/sdd-round.md`
  now says why.** It records a moment rather than pointing at live content, a
  reviewed tree has no anchor to write, and the record check already falls
  back to `refs/remotes/pull/<N>/head` — the copy of GitHub's pull-request
  refs that CI fetches — which a squash does not touch.
