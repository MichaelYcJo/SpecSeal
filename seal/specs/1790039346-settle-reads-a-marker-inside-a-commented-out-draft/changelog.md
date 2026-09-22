- **`settle` no longer reads a marker inside a commented-out draft, and the
  opt-out arm no longer takes a directory for the marker.** Round 3 of #458's
  chain found that *a line stops being live two ways* had reached the fold
  reader in full and `settle`'s ledger reader by half: a section marker inside
  a commented-out draft in `seal/ledger.md` still opened a section and took
  the draft's coordinate with it, so the segment the report printed was wrong
  for two work items at once. The obvious closure loses three real sections,
  because ledger anchors quote `<!--` inside backticks — so the rule now has
  one owner, `unverified_check.py#live_lines`, and both readers ask it. It
  carries fence, comment and code-span state in one pass, and for the one
  question markdown will not answer without a block model — whether a
  backtick run with no partner on its own line is a code span — it computes
  both readings and parks the line wherever they disagree. Five review
  rounds each found the shape the previous guess got wrong, four of them
  removing a work item's directory at exit 0; computing both readings is
  what ends that class, because there is nothing left to guess. A marker
  inside a multi-line code span is no longer read as a fold record either.
  Beside that: `settle` reads the scratch marker as a FILE the way
  `hooks/optin.py` does and resolves the git common directory once on its
  refusal path, the fragments loop of `coordinates` has the case it never had,
  and the single-scan case pins a single scan rather than two views agreeing.
  Nothing this repository prints changes: the dry run still reads
  `81 work items in 37 segments, 16 ungrouped, 0 skipped`. (#489)
