# 1790076050-the-release-tail-is-three-acts-no-document-names — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `1b92121d` |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The release note publishes itself. `.github/workflows/publish-release.yml` on
`push: tags: ['v*']` with `contents: write`, and
`.github/scripts/publish_release_note.py`: the `## X.Y.Z` section as the body,
the tagged commit's `release: X.Y.Z — <symptoms>` line as the title, an
existing release left alone, a missing section red. Verified by a new
`tests/test_a_release_publishes_its_note.py` carrying A1, A2, A3 and A4, each
seen red first, with `gh` stubbed and `CHANGELOG.md` fixtured.

The build was also asked, before anything was written, to say whether the
frame holds. Three of its facts did not, and they are the first section below.

## What this phase found

### Three facts the handoff and the frame state that the tree does not

**The handoff's five ledger rows are three.** The spawn prompt says five rows
anchor on the heading phase 4 edits, "at lines 1134, 1649, 2044 and two more
nearby". Measured over the worktree and the primary checkout, which hold a
byte-identical `seal/ledger.md`: exactly **three** rows carry
`docs/issues-and-milestones.md#"## A label answers *what it is about*, and
survives the move"@7d9851f7` — G5 at 1134, S4 at 1649, R2 at 2044. The two
further rows do not exist. What does exist nearby is three rows on two
*other* headings of the same document — `## A milestone answers *when*, and
takes three shapes` twice and `## One thing reads a milestone, and it can
stop a release` once — and phase 4 edits neither of those sections, so they
do not drift. Three is the number of claims phase 4 owes a re-read, and the
`overview.md` row says so.

**The directory file is `.claude-plugin/marketplace.json`, not
`marketplace.json`.** #417 says "the directory's `marketplace.json` is a
public file in both repositories" and `spec.md` §*Data & interfaces* inherits
that. Executed 2026-09-22 against both repositories: the root path is 404 in
each, and the file sits under `.claude-plugin/`. Phase 3 reads the corrected
path; the measurement is in that phase's record.

**An entry's `source` is not always an object.** `spec.md` states the entry
shape as "`source.url` plus `source.sha`". Executed 2026-09-22 over both
files: 52 of official's 310 entries and 5 of community's 2,282 carry a
`source` that is a plain string (`./plugins/<name>`, the in-repository shape),
with no `url` and no `sha` to read; 3 community entries carry `url` and `ref`
and no `sha`. The stated shape is right about the external majority and is not
a shape phase 3 may assume, so its reader tolerates all four.

Everything else in the frame held against the tree. The two counts it
measured on 2026-09-22 reproduce exactly — official 310, community 2,282 —
and `specseal` is in neither, by exact name match over both `plugins` lists.

### `gather_changelog.py` has no section reader to import

`plan.md` asks phase 1 to reuse its section reader rather than write a second
one, and to say so here if it is not importable as-is. **It is not: there is
no reader.** That module writes sections (`section`) and locates the first
`## ` line to insert above (`insert`); nothing in it takes a version and
returns that section's body. So `publish_release_note.py#section_body` is new
code, and what keeps it from being a second hand-checked copy of the format is
`test_the_reader_reads_what_the_gatherer_writes`: it runs the real
`gather_changelog.py#section` and `#insert`, then reads the result back. A
heading change in the gatherer fails at that seam instead of publishing a
release with empty notes.

### `release: X.Y.Z` with no symptoms exists, and it takes the fallback

A4's two branches are stated as "the line is readable" and "no such line is
readable". Measured over this repository's own tagged commits, there is a
third shape: `v0.12.3`'s line is `release: 0.12.3` with nothing after it.
Reading a title out of it yields the version alone, which is the tag name with
one character removed — so the two branches would differ by a `v` and the log
line saying which was taken would tell a reader nothing. The symptoms are
therefore **required**, and a line without them takes the fallback and says
so. A parametrised case pins all three shapes: absent, no symptoms, and a line
naming a different version.

### The title line is in the body, and the fixture carries that

`spec.md` §*Judgments* 3 records that #386's own sentence about the title is
wrong — the merge commit's *subject* is GitHub's `Merge pull request #N from
<owner>/release/vX.Y.Z`. Confirmed against the three most recent tags. The
reader takes `git log -1 --format=%B`, which is the raw body, so the line
reaches it wherever in the message it sits; and the test fixture is built with
GitHub's subject above the prescribed line rather than with a bare title line,
so a reader that only searched the subject would go red here.

### How each case was shown red (§15)

Each behaviour was removed from the script one at a time, the module re-run,
and the file restored from a byte copy kept outside the tree — never from
HEAD, which would have taken the phase's other uncommitted work with it. The
tree was `11 passed` before and after the whole run.

| Mutation | Case that went red |
|---|---|
| the body reader stops at the next `## ` heading — removed | `test_the_gathered_section_becomes_the_release_note` |
| the already-exists arm — removed, so it republishes | `test_an_existing_release_is_left_exactly_as_it_is` |
| the missing-section refusal — removed, so it publishes empty notes | `test_a_tag_with_no_changelog_section_goes_red` |
| `TAG_RE` widened from `v(\d+\.\d+\.\d+)$` to `v(.*)$` | `test_a_tag_that_is_not_a_version_goes_red` |
| the prescribed-line search — removed, so the title always falls back | `test_the_title_is_the_line_the_checklist_prescribes` |
| the symptoms made optional in `title_line_re` | `test_without_that_line_the_title_is_the_tag_and_the_log_says_so[no symptoms]` |
| the reader's heading pattern drifted from `## ` to `### ` | seven of the eleven, `test_the_reader_reads_what_the_gatherer_writes` among them |
| the workflow trigger moved from `tags: ['v*']` to `branches: [main]` | `test_the_workflow_fires_on_the_tag_and_writes_nothing_else` |

### What a gate change owes (`CONTRIBUTING.md`)

- **Test seen red**: the table above.
- **Failure direction**: the job goes red in exactly one direction — the tag
  exists and `CHANGELOG.md` carries no section for it, which is the release
  shipping unexplained. It never fails for a missing title line, because
  nothing in the tree holds that convention and a failed job at the tag is a
  release that stops after `main` has already moved.
- **Prompt budget: zero.** It runs on GitHub after a tag push, with nobody at
  a keyboard.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
