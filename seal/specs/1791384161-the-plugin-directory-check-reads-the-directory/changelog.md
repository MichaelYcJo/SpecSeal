### Fixed

- The plugin directory check no longer tells you the plugin is *not listed*
  or to submit it, about a directory it never read (#858). The command reads
  the two marketplace files on GitHub, which are outputs of the directory's
  review pipeline and not the directory, and on 2026-10-07 it said *not
  listed* in both while the owner's Console page showed the plugin
  published. It now says per file whether this plugin has an entry, over how
  many entries, which commit an entry pins and whether that commit is on
  `main`, and an absent entry is one line that names no act. The run ends by
  saying the directory itself was not read, since no script can reach it,
  and prints the page a person opens: the developer portal's Submissions
  page for a portal listing, the Console page for a Console listing. The
  short link it used to send readers to answered with a documentation page,
  not a form, and is gone. The exit code is unchanged: 0 for every outcome.

- The release checklist's last box no longer says to resubmit (#858). On the
  developer portal a new version reaches the directory from the tracked
  branch on its own, and a listing made through the earlier Console form
  takes no new version until a person moves it to the portal, so the
  instruction was wrong for both. The box now says what the command reads,
  that the directory is readable from nowhere a script can reach, which page
  answers for each kind of listing, and that SpecSeal's listing is a Console
  listing by the owner's reading of 2026-10-07, with where the move is
  documented. `docs/branch-and-release.md`'s release-tail bullet says the
  same of the command, and its third-reader paragraph names a marketplace
  file as the reader that pins a commit.
