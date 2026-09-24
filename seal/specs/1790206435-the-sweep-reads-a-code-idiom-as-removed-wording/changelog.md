### Fixed

- `survivor-check` reads a Python file's prose — its comments, docstrings
  and string literals — and nothing else (#543). Every other token is a
  separator, so a code token between two literals ends the sentence and two
  literals across a line break are still one; a file the tokenizer refuses
  is read whole, as before. A generic list walk used to normalise to the
  same words in every module that has one, so a branch rewriting one loop
  was told every other loop still stood: four of one branch's five
  exemption rows, and six of the twenty-one places the 0.15.0 release's four
  ranges reported, were function bodies. Over those four ranges the sweep
  now reports 4, 0, 8 and 1 places, every one of them prose.
- A released changelog section and a gathered fragment are records the
  sweep leaves out on both sides (#307): every line under a heading naming a
  version in the root `CHANGELOG.md`, up to the next `## ` heading, and a
  `seal/specs/<id>/changelog.md` whose marker stands in `CHANGELOG.md` at
  the range's tip. An `## Unreleased` section and an ungathered fragment
  stay in, because they are this release's own prose. A released entry is
  not rewritten, so being reported against one cost a `survivors.md` row for
  a sentence nobody may correct; two of the four measured ranges carried
  that report.
- An unresolved `survivors.md` declaration prints only to the run it
  addresses (#439). Every shipped work item's declaration names a release
  branch deleted at the release, and the line for it printed on every pull
  request into a release branch and every seal — three per run for one
  release — for a declaration that could never have applied. The second
  anchor is now asked first: a declaration owned by a work item the range
  touches nothing of prints nothing and silences nothing; one with no owner,
  or owned by a work item the range touches, prints under `unresolved` as
  before.
- `survivor-check` reads a renamed file as a deletion plus an addition
  (#551). With git's rename detection on, a file moved whole was listed
  under its new path alone, so the range removed nothing the sweep could
  see — right for a pure move, and identical for a move with one sentence
  reworded, which git calls a rename too: the reworded sentence never became
  a source and its copy standing in another file was never reported. Now
  the old path's sentences are removed, a pure move stays silent because
  every one of them is written back verbatim, and the reworded one is
  looked for.
