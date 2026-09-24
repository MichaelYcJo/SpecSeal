# Survivors — the fold writes each release to its own file

`bin/survivor-check --range 9f5902e5...HEAD`, run at phase 6 over this
branch's own range (it is cut from step C's tip), reported twenty places.
Each was opened. One was corrected: the evidence-ledger policy's conflict
paragraph, which is a copy of the rule this branch widened in
`CONTRIBUTING.md`. One `seal/ledger.md` row was narrowed by a dated
`Corrected` note and is no longer reported. The rest are right where they stand, for one of four
reasons: the changelog gather's own code, which this branch was told to
leave alone and which shares shapes with the fold; a sibling's record; the
owner's `CLAUDE.md`; or a marker line whose duplicate #553 removed while the
original stays.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_changelog_is_gathered_at_release.py` | `text = changelog(tree)` | the gather's own fixture helper, which reads `CHANGELOG.md`; the fold's twin of it was re-pointed at the release file, and the gather is on the spec's unchanged list |
| `.github/scripts/gather_changelog.py` | `pass --version to gather, or --check to verify` | the gather's argument check; the fold's gained `--split` and the gather has no such flag |
| `.github/scripts/gather_changelog.py` | `marked = len(MARKER_LINE_RE.findall(text))` | the gather counts markers in its one file; the fold now counts across files, and the changelog stays one file by design |
| `.github/scripts/gather_changelog.py` | `Where the file already heads` | the gather's `insert` docstring, true of `CHANGELOG.md` |
| `tests/test_the_changelog_is_gathered_at_release.py` | `def test_a_second_gather_into_the_last_section_ends_the_file_with_one_newline(` | the gather's case; the fold's retired case shared a phrase with it |
| `tests/test_release_hygiene.py` | `for number, line in enumerate(text.splitlines(), 1):` | `duplicated_version_headings`, the hygiene module's own reader, deliberately a copy of the fold's (C's F2 row says why); the fold's body moved into `version_headings` |
| `.github/scripts/fold_ledger.py` | `Where the ledger already heads` | `insert`'s docstring, unchanged by S18: over a release file its input text is the file, and every sentence of it holds there |
| `tests/test_the_ledger_fragments_fold_at_release.py` | `text = ledger(tree).replace(` | the prose-marker case seeds its quoted marker in `seal/ledger.md`'s header, which is where the header's prose lives after this change too |
| `tests/test_settle_reads_before_it_removes.py` | `the areas above the folded sections are the rows from before the fragments existed` | the fixture case's docstring; `seal/ledger.md`'s header still says the areas are the rows from before the fragments, in new words |
| `seal/specs/1790206437-a-second-fold-writes-a-second-heading/spec.md` | `with an area heading appended after the version section` | step C's frame, a record of C's S4 as it was framed; this branch retired the case and says so in `phases/phase-2.md` |
| `CLAUDE.md` | ``When `seal/ledger.md` conflicts, resolve it hunk by hunk`` | the owner's file, not edited (`agents/smith.md`); paste-ready text in `phases/phase-5.md`, named in `overview.md` §*Not verified* |
| `CLAUDE.md` | ``an existing `seal/ledger.md` row cites must touch that file`` | the same: the owner's file |
| `seal/ledger.md` | ``its text moved into `ledger.md` under `## X.Y.Z — <date>` `` | a §0.4.0 row's claim as it was verified; the dated *Re-read 2026-09-24 … phase 2* note on the same row says the text now moves into the release file |
| `seal/ledger.md` | `<!-- specs/1788761915-a-record-states-what-nothing-reads -->` | the one marker line that stays for that work item; #553 removed its duplicate |
| `seal/ledger.md` | `### 1788761915-a-record-states-what-nothing-reads` | that work item's heading, under its one remaining marker |
| `CHANGELOG.md` | `<!-- specs/1788761915-a-record-states-what-nothing-reads -->` | the gathered changelog's marker for the same work item; nothing doubled it there |
| `docs/the-evidence-ledger.md` | `<!-- specs/1788761915-a-record-states-what-nothing-reads -->` | a folded statement's provenance marker, `settle`'s; unrelated to the ledger's doubled line |
| `skills/implement/scripts/seal.py` | `if kind == "none" and not args.check:` | unrelated code sharing two words with the fold's old argument check |
| `seal/ledger.md` | `<!-- specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row -->` | the one marker line that stays for that work item; #553 removed its duplicate. Reported only after `release/v0.15.1` (#550's sweep) was merged in at 1ec9f040, which scores this pair above the floor where the branch's earlier sweep did not; excused by the orchestrator at that merge |
| `seal/ledger.md` | `### 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row` | that work item's heading, under its one remaining marker |
| `docs/review-chain-spec.md` | `<!-- specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row -->` | the policy document's own origin marker for the section that work item folded in; it names the work item, not the removed duplicate line |
| `tests/test_a_runner_reached_unit_reads_pytest_only.py` | `of \`1788749195-the-record-drops-the-fix-and-a-pipe-` | a docstring naming that work item's round record as where the case was seen; it names the work item, not the removed duplicate line |
