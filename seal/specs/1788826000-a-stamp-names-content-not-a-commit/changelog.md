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
- **Three riders were held by nothing.** The scanned roots covered four
  directories and riders live in six, so the one in
  `.github/scripts/fold_ledger.py` and two under `tests/` were checked by no
  case at all — and one of those had never carried a stamp in any form.
- **A round record's `Target SHA` stays as it is, and `templates/sdd-round.md`
  now says why.** It records a moment rather than pointing at live content, a
  reviewed tree has no anchor to write, and the record check already falls
  back to `refs/remotes/pull/<N>/head` — the copy of GitHub's pull-request
  refs that CI fetches — which a squash does not touch.
