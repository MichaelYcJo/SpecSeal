# 1790260564-a-moved-file-counts-as-written — questions for the planner

**Decided from the tree, and not reopened here.** `spec.md` §*The judgments
the tickets left open, decided from the tree* gives the grounds for each:

- Whether moved text counts as written (#563's design question). #563's
  comment names the owner as the one who answers for gathered text. Since
  that comment, the folded statement in `docs/review-chain-spec.md`
  §*What the sweep reads, and what it counts as written* has ratified the
  gathered half (*held and never written, because the fragment's own branch
  wrote it*). Its rule sentence (*only wording the range itself wrote is
  subtracted*) decides the moved half the same way. → held, never written,
  paired across paths by key and count.
- #563's whole-file rule against pairing that also covers a split. → pairing,
  because the split is the shape #563 names as reachable here.
- #564 ⬜5, which of the two spellings wins. → the predicate, and the reader
  asks it.
- #564 ⬜6, marker-bounded or heading-bounded. → heading-bounded, where
  `Unreleased` and version headings are the only headings that change the
  region after a version.
- #564 ⬜7, one pattern or the read boundary. → the read boundary.
- #554, which of the issue's two candidates. → the `Branch` row, tested as
  the range tip's ancestry, and local mode only.
- Whether the docs sentences are corrected in this branch or left for the
  fold. → corrected in place with no marker, as `00adf8c6` (#558) did.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | May a changelog fragment carry a `## ` line? If not, should `.github/scripts/gather_changelog.py` refuse one? `gather_changelog.py#insert` and `publish_release_note.py#section_body` both end a released section at any `## `. So a fragment carrying one also breaks the second gather into that version and the published release note, not only the sweep (#564 ⬜6's class, outside `survivor_check.py`). **Why the tree cannot answer:** no document states a fragment's format beyond *a file per work item*. What the release automation accepts is a convention somebody has to own, and it is outside this branch's scope | a person (the repository owner) | **(a) Refuse at the gatherer**: `--check` and the gather both reject a fragment with a line matching `^## `, and one refusal covers all three readers. **(b) Teach the two release readers the sweep's region rule**: three readers keep one rule in step. **(c) Leave it**: unreachable today (`grep` over the fragments in the tree finds no such line, per #564's report, not re-run here) | This branch changes the sweep alone (phase 1) and touches neither release script. The orchestrator files an issue for (a) against the next release. The build does not wait on this | ⬜ |
| Q2 | Does #526's split of `docs/review-chain-spec.md` (`82928fc6`, #567) report survivors under phase 2's reading that it did not report before? #563 says that item's sweep *is blind there until this lands*. **Why the tree cannot answer:** only running the sweep over that range settles it | a measurement (`survivor-check --range 82928fc6^..82928fc6` at the base and at phase 2's commit) | Nothing new: the claim was cautious, record it. Something new: each report is judged. A real survivor goes to `seal/follow-up.md` with an answerer. It is not corrected in this branch (`spec.md` §*Out*) | Phase 2 runs it and records both outputs in `phases/phase-2.md` | ✅ measured by phase 2 (executed): nothing new. `82928fc6^..82928fc6` reports the same three places at the same scores at `c52e8350` and at `ed5748ff`, exit 1 both; the removed count drops from 1291 to 245. The claim that item's sweep *is blind there* was cautious; `phases/phase-2.md` carries the places |
| Q3 | Do the pinned counts in `RELEASE_RANGES` (`test_the_four_real_ranges_report_their_prose_and_none_of_their_code`) change under phase 2? Any of those four commits that moves text now counts fewer removed sentences, and it may score its survivors differently (`plan.md`'s run-merge failure scenario). **Why the tree cannot answer:** the four ranges have to be re-run | a measurement (the one case, run in phase 2) | Unchanged: nothing to do. Changed: the pin is updated coordinate for coordinate, with each moved coordinate explained in `phases/phase-2.md`. A survivor that disappears is judged: a run merge is the expected cause, and anything else is a finding | Phase 2 runs it | ✅ measured by phase 2 (executed): unchanged. The four ranges report the same coordinates at the same scores and the case is green unedited; only the removed counts move, 60/61/35/156 → 48/60/35/120 |
| Q4 | Does the `CHANGELOG.md` arm of `corrected` need to see the cross-path pairing? Its `lost` guard and `split` set are computed per file, before pairing. A sentence `CHANGELOG.md` lost that is paired with a copy in another file stops being a source, and its `split` n-grams then subtract nothing. That should be harmless. **Why the tree cannot answer:** it depends on where the builder puts the pairing step | the work (phase 2) | Leave the arm per-file (the default) while the existing release and gathered cases (the `#307` and `#557` blocks of the test file) stay green. If one goes red, the phase records the divergence and decides it there | Per-file, untouched | ✅ answered by phase 2's work: the arm stays per-file. The pairing runs after every path is counted, so the `lost` guard and `split` see each file's own loss; the `#307` and `#557` blocks re-run green (the module 112 passed) |

**`Who can answer` takes one of three values and nothing else.**

- **a person**: what the product should be, or a value somebody has to be
  accountable for. Only this kind blocks the build, and Q1 does not block,
  because its default touches nothing this branch builds.
- **a measurement**: a probe, a command or a count settles it.
- **the work**: it cannot be known at framing time. The phase that meets it
  decides it there and records a divergence row.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
