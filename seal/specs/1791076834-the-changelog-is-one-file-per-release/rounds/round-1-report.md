# Round 1 report — the changelog is one file per release (#728)

Target `516ed1d1` on `feat/728-the-changelog-is-one-file-per-release`, against
`release/v0.18.1` at `edee5ca2`. Reviewed in a `git clone --no-local` at the
target, under the session scratchpad; nothing was run in the worktree.

## What was asked, and the answer in brief

The round asked for spec compliance first: the byte-for-byte migration of the
44 sections, the index's shape and what 0.18.0's installed update skill reads
from it, `gather_changelog.py` writing and checking the release's own file,
`publish_release_note.py` reading it, the survivor sweep reading both shapes,
and every reader and writer of the changelog enumerated by construction. The
risk named was the release this ships in: 0.18.1 is gathered and published by
the new tooling, so a defect would surface at the tag.

That risk was exercised rather than read. In the scratch clone the new
gather wrote 0.18.1 from the four fragments on the branch, `--check` then
passed, `section_body` read the new file back, and the hygiene and gather
modules passed on that post-gather tree with `plugin.json` at 0.18.1 and
everything staged as the checklist now says. Nothing found needs a fix. The
three findings below are wording and wrap, each ⬜.

## Stage 1 — spec compliance

**S1, the lossless migration (executed).** The 44 files under `changelog/`,
read newest first by version and joined by one blank line under
`# Changelog` and a blank line, are byte-identical to `CHANGELOG.md` at
`edee5ca2`: 577,907 bytes both, compared in Python. `CHANGELOG.md` is the
same at `e141980a` and `edee5ca2` (`git diff --quiet`, exit 0), so the
smith's probe base and this round's agree. For four releases (0.18.0, 0.17.0,
0.9.1, 0.0.1) `section_body` of the release file equals `section_body` of the
old one-file changelog at `edee5ca2`.

**S2 and D2, the index (read, and executed through the gather below).** The
index is `# Changelog`, one paragraph, then per release its heading line, a
blank line and the link, newest first. Its first `## ` line is
`## 0.18.0 — 2026-10-03` at the target and `## 0.18.1 — 2026-10-05` after the
probe gather. So 0.18.0's step 2b, `grep -m1 '^## ' "$p/CHANGELOG.md"`, names
the new version after an update into 0.18.1. D7's cost (0.18.0's step 3 meets
the index) is as the spec states it, and the new step 3 in
`skills/update/SKILL.md:72-78` reads the release files.

**Scope 3, the writer (executed).** At the target, `--check` exits 1 and
names the four fragments on the branch, which is correct for a feature
branch. `--dry-run --version 0.18.1` exits 0, prints `into
changelog/0.18.1.md:`, and writes nothing. The real gather exits 0, writes
`changelog/0.18.1.md` ending in one newline, puts the index entry above
0.18.0, and prints both lines. `--check` then exits 0 with
`57 changelog fragments, all gathered; 174 work items marked in changelog/`.
I read `released_markers`, `ungathered`, `indexed`, `index_entry` and the
write path in `main` at `.github/scripts/gather_changelog.py:168-206, 336-366,
476-520`. The append arm keeps the file's date. Where the file is missing it
falls back to the index's date. The index is rewritten only when it changed.
Every refusal (#586, #584, nothing to gather, nothing to check) is still
there.

**Scope 4, the publisher (executed for `section_body`, read for `main`).**
`section_body` of the gathered `changelog/0.18.1.md` returns 9,162
characters, from the first entry's marker to the last entry's last line.
`main` at `.github/scripts/publish_release_note.py:515-530` refuses both a
missing file and a file with no section, and names `changelog/<version>.md`
and the gather command. The closing link at `:479` is
`blob/<tag>/changelog/<version>.md`. I did not run `main` itself, because its
dry run still calls `gh`; the fake-tracker module covers it, and that module
passed (below).

**Scope 5, the survivor sweep (executed).** `a_changelog` is now the one
predicate in `sentences`, `gathered_fragments`, `corrected` and `score`.
I grepped for `== CHANGELOG` and found no comparison left. Over the build
range `edee5ca2..516ed1d1` the sweep reports four places, all in
`seal/releases/`. With the work item's `survivors.md` as `--exempt` it exits
0, `every survivor is excused by a row above (4)`. Over the probe's gather
range (target to a commit holding the gathered 0.18.1) it reports `no
removed wording is still standing`. So a release preparation in the new
layout is clean.

**Readers and writers, by construction (executed grep, then read).**
`git grep -n CHANGELOG` and `git grep -n -i changelog` over `.github`,
`hooks`, `bin`, `skills/**.py`, the workflows and `tests/` at the target find
no reader of a released section beyond the four the spec names. The ones I
added to the spec's table:

- `.github/scripts/release_seal.py`, the tag's second job, reads no
  changelog.
- `hooks/` names none.
- `broad_gate.py` holds the hygiene step by name only.
- `test_chain_hooks_hardening.py` reads a version substring, which the index
  keeps.

The 17 test files of D8 are all accounted for in the diff. The moved files
carry no markdown link at all (0 `](` occurrences), so moving them one
directory down broke no relative link.

## Stage 2 — quality

The three ⬜ below are the whole of it. I looked for a 🟡 in the edge shapes
of `indexed`: an index with no `## ` yet, an index already heading the
version, a file with no date, a file missing while the index heads it. Each
is handled, and each but the undated-in-the-index one is a planted case.

### ⬜ 1 — eight added lines were spliced into a wrapped paragraph without re-wrapping

`.github/scripts/fold_ledger.py:69` (99 columns), `:131` (96);
`.github/scripts/publish_release_note.py:20` (114);
`docs/branch-and-release.md:59` (102), `:64` (89), `:259` (101);
`skills/code-review/scripts/survivor_check.py:165` (112);
`tests/test_a_record_precedes_the_fixes_it_commissions.py:1156` (115).

Each sits in a block that wraps at 75 to 80 columns, and each is the line an
edit of this branch lengthened. `tests/test_docs_line_wrap.py` passes because
none of these files is in its scope, and nothing measures a comment line
(`seal/follow-up.md` already has the row for that class). Nothing ships
wrong. The next reader reflowing the paragraph has no band to follow. Reflow
each paragraph at its neighbours' width.

### ⬜ 2 — §3 of the release checklist still describes the unstaged tree that §2 now stages away

`docs/release-checklist.md:84` now runs `git add -A changelog/ CHANGELOG.md
seal/ .claude-plugin/plugin.json`, and `:89` says both are staged before §3
runs anything. `:184-187` in §3 still says *the fold removes each fragment
and nothing has staged the removal yet*, and tells the reader that skipped
cases naming paths are *that state rather than something to debug*. Followed
as written, §2 removes the state §3 explains. A skipped case that does appear
at §3 is then something else, and the paragraph tells the reader not to look
into it. Reword §3's paragraph so it says what happens when §2's staging was
skipped, or drop the clause.

### ⬜ 3 — the comment above `CHANGELOG` in the sweep says another name is read as any document

`skills/code-review/scripts/survivor_check.py:579-581`: *The changelog the
gatherer writes, at the repository root and under this name. A changelog
kept elsewhere or under another name keeps the reading every other document
has (#307's Out).* Since this branch the gatherer writes
`changelog/<version>.md`, and `RELEASE_FILE` right below reads exactly that
other name as a changelog. The module docstring at `:154-165` was
rewritten. This comment was not. Reword it to say that the root file and
the `RELEASE_FILE` shape are read as a changelog, and that any other place
or name keeps the ordinary reading.

## The implementer's account, checked

- *The 44 files joined are byte-identical to the old file* (ledger C1).
  Confirmed by my own probe, against `edee5ca2` rather than `e141980a`; the
  two blobs are the same.
- *`section_body` of `changelog/0.18.0.md` equals the old one for 0.18.0,
  14,746 characters* (ledger C4). Confirmed: 14,746, equal. Also equal for
  three more releases.
- *The sweep over the build range reported no sentence of `CHANGELOG.md` or
  `changelog/`* (ledger C5). Confirmed: four places, all in `seal/releases/`,
  all four excused by `survivors.md`.
- *The orchestrator verified the changed modules plus hygiene, 995 passed,
  and ruff on the changed Python files.* Carried as a claim, not re-run. I
  ran narrower sets (below), and ruff not at all.
- *Each new case was seen red* (ledger C1, C4, C5, C6). Not re-checked this
  round. It is the smith's account and is labelled here as read.

## Regression tests to plant

None owed by a finding. One I would add: a real-tree case asserting that
`gather_changelog.py --dry-run --version <next>` on the repository itself
names `changelog/<next>.md`. The release is the first time this tree runs
the new gather, and today only fixtures exercise it. Destination
`tests/test_the_changelog_is_gathered_at_release.py`. Optional; this round's
probe did that once.

## Facts for the evidence ledger

- Executed 2026-10-04 in a scratch clone at `516ed1d1`: gather for 0.18.1
  wrote 4 fragments into `changelog/0.18.1.md`, `--check` then reported 57
  fragments all gathered and 174 work items marked; `section_body` of that
  file returned 9,162 characters; the hygiene, gather and chain-hardening
  modules passed on that tree (161 passed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | eight added lines spliced into wrapped paragraphs without re-wrapping, 89 to 115 columns | `docs/branch-and-release.md:59` | open | read; the other seven coordinates are in the prose above; no check covers these files |
| ⬜ 2 | release checklist §3 still describes the unstaged tree that §2 now stages | `docs/release-checklist.md:184` | open | read against `:84` and `:89` of the same file |
| ⬜ 3 | the comment above `CHANGELOG` says a changelog under another name is read as any document, which `RELEASE_FILE` now contradicts | `skills/code-review/scripts/survivor_check.py:579` | open | read; the docstring at `:154-165` was updated and this comment was not |
| 🟢 | S1 holds: the release files joined reproduce the old changelog byte for byte | `changelog/` | confirmed | executed, 577,907 bytes both, against `edee5ca2` |
| 🟢 | the new gather writes 0.18.1 and its index line, and `--check` passes after it | `.github/scripts/gather_changelog.py:476` | confirmed | executed in the scratch clone; hygiene and gather modules green on the post-gather tree |
| 🟢 | the publisher's `section_body` reads the gathered release file | `.github/scripts/publish_release_note.py:151` | confirmed | executed on the gathered 0.18.1 file and on four migrated releases |
| 🟢 | the survivor sweep reads both shapes; build range excused, gather range clean | `skills/code-review/scripts/survivor_check.py:591` | confirmed | executed over both ranges |
| 🟢 | 0.18.0's update step 2b still names the landed version from the index | `CHANGELOG.md:11` | confirmed | read; the first `## ` line is the newest release's heading, before and after the probe gather |

## Executed probes

| What was run | Result |
|---|---|
| Python byte compare: `changelog/*.md` newest first, joined under `# Changelog`, against `git show edee5ca2:CHANGELOG.md` | equal, 577,907 bytes both, 44 files |
| `git diff --quiet e141980a edee5ca2 -- CHANGELOG.md` | exit 0, identical |
| `gather_changelog.py --check` at the target | exit 1, names the four branch fragments (expected off a release) |
| `gather_changelog.py --version 0.18.1 --dry-run --date 2026-10-05` | exit 0, `into changelog/0.18.1.md:`, 4 markers, nothing written |
| `gather_changelog.py --version 0.18.1 --date 2026-10-05`, then `--check` | exit 0 both; index headed with `## 0.18.1 — 2026-10-05`; `57 changelog fragments, all gathered; 174 work items marked in changelog/` |
| `section_body` on `changelog/0.18.1.md`, and old-vs-new for 0.18.0, 0.17.0, 0.9.1, 0.0.1 | 9,162 characters; all four equal |
| `bin/test` on the release hygiene, gather and chain-hooks-hardening modules, post-gather tree, `plugin.json` at 0.18.1, all staged | 161 passed |
| `bin/test` on the publisher, survivor, GFM-reader and handoff modules at the target | 385 passed |
| `bin/test tests/test_docs_line_wrap.py` at the target | 38 passed |
| `survivor-check --range edee5ca2..516ed1d1` | exit 1, 4 places, all in `seal/releases/` |
| same with `--exempt` the work item's `survivors.md` | exit 0, all 4 excused |
| `survivor-check` over the target-to-gather probe commit | exit 0, no removed wording standing |
| 0.18.0's sweep (the `edee5ca2` blob, run once as a probe file and deleted) over `edee5ca2..516ed1d1` | exit 1, 3 places, none under `changelog/` |
| Python scan of `changelog/*.md` and every fragment for relative markdown links | 0 links of any kind |
| the full suite, repository-wide lint and typecheck | not yet; the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Not verified

- ruff over the changed Python files. Not run this round, and the
  orchestrator's claim is carried. Answerer: the sealer.
- `evidence-check --strict` over this work item's ledger fragment. Not run.
  Answerer: the sealer.
- `publish_release_note.py#main` end to end at a real tag. It cannot run
  before the tag exists. Answerer: the 0.18.1 tag push, read in its job log.

Nothing is left open that needs a fix, so the broad gate has come due: the
sealer's spawn.

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, at `516ed1d1` in the scratch clone unless noted:

- the round's ask (scratchpad)
- `seal/specs/1791076834-the-changelog-is-one-file-per-release/spec.md`
- `seal/specs/1791076834-the-changelog-is-one-file-per-release/survivors.md`
- `seal/ledger/1791076834-the-changelog-is-one-file-per-release.md` (by grep)
- `CHANGELOG.md`
- `.github/scripts/gather_changelog.py`
- `.github/scripts/publish_release_note.py`
- `.github/scripts/fold_ledger.py` (diff)
- `.github/workflows/hygiene.yml` and `publish-release.yml` (diff and grep)
- `skills/code-review/scripts/survivor_check.py`
- `skills/update/SKILL.md` (diff)
- `skills/verify/SKILL.md` and `skills/verify/scripts/session_cost.py` (diff)
- `skills/settle/scripts/settle.py` (diff and grep)
- `skills/verify/scripts/broad_gate.py` (grep)
- `agents/sealer.md:74-100`
- `docs/release-checklist.md:60-100, 170-200`
- the diffs of `docs/branch-and-release.md`, `docs/the-record-layout.md`,
  `docs/review-chain-spec.md`, `docs/issues-and-milestones.md`,
  `CONTRIBUTING.md` and `seal/follow-up.md`
- `tests/test_the_changelog_is_gathered_at_release.py:1-640`
- `tests/test_the_release_check_watches_what_ships.py:1-120`
- `tests/test_release_hygiene.py:40-70`
- `tests/test_docs_line_wrap.py:1-60`
- the diffs of `tests/conftest.py`, `tests/test_a_release_publishes_its_note.py`,
  `tests/test_every_reader_ends_a_line_where_gfm_does.py`,
  `tests/test_handoff_outlives_the_merge.py`,
  `tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py`,
  `tests/test_session_cost.py`, `tests/test_one_word_one_meaning.py`,
  `tests/test_no_document_names_the_old_roots.py` and
  `tests/test_a_record_precedes_the_fixes_it_commissions.py`
