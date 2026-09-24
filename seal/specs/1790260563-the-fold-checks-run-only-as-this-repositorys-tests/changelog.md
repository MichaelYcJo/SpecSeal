- **The fold's two checks ship as `fold-check`, and a repository states their
  values as `seal/config.md` rows (issue #566).** The statement shape and the
  document line ceiling were checked only by this repository's own tests, so
  a repository folding with `settle` had the rules and nothing that read
  them. `fold-check` reads the top level of `docs/` and names every statement
  from the cutoff on that does not open with a bold rule sentence or does not
  carry one `Enforced by:` line whose targets exist, and every document over
  the ceiling that is not listed with its fold markers frozen. The values are
  three optional rows: `Fold shape from`, `Document line ceiling` and
  `Over the ceiling`. An absent row is a check that does not run, and the
  output says so in one line. A value that will not parse exits 2 naming the
  row. `--shape-from` and `--ceiling` replace a row for one run, and
  `--shape-from 0` lists every statement still missing the shape. This
  repository declares `1790154761`, `1000` and `none`, and its two test
  modules now pin the shipped command, reading the same rows as the policy
  prose. When a listed document's markers move, the message prints the
  digest the file has now, to be copied into the row. `settle`'s procedure
  and the release checklist run it after the prose is written and before
  `settle --retire`.
- **A folded statement's `Enforced by:` line may be as wide as its targets
  (issue #583).** The wrap limit on the hand-wrapped documents left room for
  one short target, while most `path::test` targets in this repository are
  wider than 88 columns on their own. The limit now skips exactly the lines
  `fold-check` reads as a statement's line of targets. A
  `nothing — <why>` line, whose reason is prose, and an `Enforced by:` line
  outside any statement are still held to it.
- **`settle` names a ledger row written inside a blockquote or a list by its
  claim (issue #530).** A row written behind `>` or `-` was reported by its
  marker, because only a comment opener was dropped from before the first
  pipe. Any run of blockquote, bullet, ordered-list and comment markers is
  dropped now, in any combination and spaced or not. A prefix that holds
  anything else is kept as the label, as before.
