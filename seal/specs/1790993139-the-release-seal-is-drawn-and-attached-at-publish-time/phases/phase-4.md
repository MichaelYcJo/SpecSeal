# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | fa3705e1 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Publishing. In `publish_release_note.py`, `glance` and `sealed_glance` are
split out of `release_body`, and `created` is written to `$GITHUB_OUTPUT`.
`release_seal.main` draws, uploads, reads the body, replaces the table
exactly once and edits. Every failure exits 0 with a line and a
`::warning::`. `DRY_RUN` is supported. `publish-release.yml` gets its `seal`
job. The docs change in three places: `docs/branch-and-release.md`'s
release-tail bullet and its `Enforced by:` line, `docs/release-checklist.md`
§6's box, and the workflow's header comment. The changelog fragment and the
ledger fragment are written. Cases S1, S2 (the fallback case #718 asks
for), S3, S4, S5 and S12. The existing `tests/test_a_release_publishes_its_note.py`
stays green, apart from the workflow case rewritten under S5.

## What this phase found

**The frame holds for this phase.** `publish_release_note.py#release_body`,
`#main` and `#merged_pulls`, and `publish-release.yml#jobs.publish`, are as
`plan.md` §*Technical context* describes them.

**Settled while building.**

- **`tally` joins `glance` and `sealed_glance`.** The seal must find the
  glance block by the exact text the note wrote. That means counting the
  release the way the note counts it, so the loop that built `closed` inside
  `release_body` became `tally(pulls, owner)`. The note calls it and the
  seal calls it. The note's bytes are unchanged, and every earlier case
  passed unedited.
- **The note is read as JSON, not through `--jq`.** `gh release view --json
  body` is parsed, so the body is the stored string with no trailing newline
  added by `jq`. A body GitHub returns with CRLF line endings, as an edit in
  the web form can leave it, does not contain the LF glance block. It falls
  to S3, the safe direction.
- **The upload always names the file `seal.png`.** `gh release upload` names
  the asset after the file. A run that uploads writes `seal.png` in a
  directory of its own, and `SEAL_PNG` applies to a dry run only. A first
  version also copied a differently named `SEAL_PNG` before uploading.
  Mutation showed that branch could not be reached, and it was removed.
- **A re-run cannot double-edit.** A re-run of the `seal` job reuses the
  `publish` job's `created=true`. The note it reads no longer holds the
  glance table, so S3 stops it before the upload, and no `--clobber` is
  needed.
- **Where modules load from and which tree is read are two names.** `CODE`
  is where `release_seal.py` loads its modules from, and `ROOT` is the tree
  the chain rows read. They are the same checkout at the tag. A case points
  `ROOT` at a fixture without moving `CODE`.
- **The workflow case was renamed.** It is now
  `test_the_workflow_fires_on_the_tag_and_writes_one_release_one_asset_one_edit`.
  `docs/branch-and-release.md`'s `Enforced by:` line names it, and nothing in
  the ledger cited the old name. `seal/specs/1790263216-…/phases/phase-5.md`
  still names the old case. It is a record of that day and is left as it is.
- **A dry run against 0.17.0's published release, read-only, on
  2026-10-03.** It drew the rows 10 · 27 · 6 · 12 and a PNG with Menlo.
  Then it refused with S3's reason, because that note was edited by hand
  when its seal was attached. So the S3 path was seen on a real note.

**Verified.**

- Red first (executed): the publisher's four new cases failed before the
  functions and the output existed. The seal's publishing cases failed
  before `main` existed. The two document pins failed with both documents
  stashed back.
- Mutations through `bin/mutation-check` (executed), each red:
  - in `release_seal.py`, the guards and wrappers listed in ledger row W2;
  - in `publish_release_note.py`, the five listed in W1;
  - in `publish-release.yml`, the three listed in W3.
  
  The catch-all in `main` first survived being narrowed to `Refused`, until
  S2 gained the case "a module will not load". The dead copy branch also
  survived, and was removed.
- The modules that read the phase's documents (executed): every module
  whose source names the publisher, the workflow, the seal script, either
  policy document, an `Enforced by:` line, `docs/` or the workflows, 71
  modules: `bin/test <71> -q` gave 3765 passed and 76 skipped, exit 0.
- `uvx ruff check` and `uvx ruff format --check` on the touched files
  (executed): clean.

**Not executed here.** The `seal` job itself, at a tag on GitHub's
runners. The cases drive `release_seal.main` with `gh` and `git` stubbed,
and the dry run reads GitHub without writing. The first live run is
0.18.0's tag push, and `overview.md` names who answers it.

**Ledger.** W1–W4 are in the fragment. `seal/releases/0.11.1.md` S9 and
`seal/releases/0.15.0.md` P1c, which cite `docs/release-checklist.md` §6,
are re-read and stamped in place.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The glance table and the closed-issue loop inline in `release_body` | `publish_release_note.py#glance` and `#tally`, which `release_body` calls |
| `test_the_workflow_fires_on_the_tag_and_writes_nothing_else` | `test_the_workflow_fires_on_the_tag_and_writes_one_release_one_asset_one_edit`, and the `Enforced by:` line that names it · NAME NOT IN TREE |
