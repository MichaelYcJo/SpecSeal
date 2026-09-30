# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — phase 2

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 4f22852e |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 2: P1–P7, a name written as `path#name` is checked.
The coordinate-form reader over `claim_lines`, `place` for the path, the
token rule in the named file, and the bare-name fallback where the path does
not resolve. D2's lines about the form. Re-run Q1's measurement over the live
records and `seal/follow-up.md`.

## What this phase found

- **`ANCHOR_RE` is now built from two named pieces, `ANCHOR_PATH` and
  `ANCHOR_NAME`,** and `RECORD_COORD_RE` from the same two. The plan asked
  for the coordinate form to take `ANCHOR_RE`'s path and unquoted-locator
  grammar; a copy of the two strings would be two grammars after the first
  edit to either. The compiled `ANCHOR_RE.pattern` is byte-equal to
  `56e53c90`'s (executed, a comparison of the two modules' patterns), so no
  ledger row reads differently. Rows citing `ANCHOR_RE` drift on the edit and
  are phase 4's.
- **A dotted name is split into segments on both branches.** Where the path
  resolves, every segment has to be a token of the file. Where it does not,
  each segment is read as a bare name, because a bare backticked span holds
  no dot and `RECORD_NAME_RE` would never have seen `Class.method` whole; the
  spec's "read exactly as the bare backticked name would be" is taken
  segment by segment.
- **The refusal names the path as the record wrote it**, not the path
  `place` resolved to. A `--map` or `--default-repo` path would otherwise
  print absolute, and the reader is looking for the span they wrote.
- **A path resolving to a directory, or to a file that cannot be read,
  falls back.** The plan says "resolves … to a readable file"; `read`
  answers None for both, and that is the test.
- **One read per cited file per run.** `file_tokens` is filled by
  `coordinate_misses` and threaded from `check_records`, so a module cited
  from forty lines is tokenised once.
- **Q1 at the end of phase 2: 1 refused, and it was this work item's own
  plan.** With the reader in place, `bin/evidence-check .` refused
  `plan.md:55`, the frame's `tests/test_release_hygiene.py#overwide_rows` · NAME NOT IN TREE,
  which phase 1 recorded as stale. It is corrected in the
  phase 2 commit, in place, with a dated note. After it: `2 work items read ·
  24 unread · 322 names read · 0 stamps read · 0 refused · 0 drifted · 0
  external · seal/follow-up.md read`. The 26 coordinate-form names read split
  as: `seal/follow-up.md` 10 resolved and 1 unresolved (`ungathered`, no
  underscore, so not read); A's records 3 resolved and 8 unresolved, all
  carried; this work item's 5 resolved (one the refusal above) and 2
  unresolved with one-word names.
- **How each case was seen red.** Against `56e53c90` through the probe
  plugin: 13 of 19 failed. The 6 that passed there are P5 (a stamped span
  counted once, which the base also does) and P6 (three claim-rule
  exemptions, which a reader that reads nothing also passes); P5 went red
  with `@hash` admitted into `RECORD_COORD_RE`, and P6 with the lines read
  past `claim_lines`. Seven mutants in all, each restored with `git status`
  clean afterwards: the two above, the file's tokens swapped for the corpus
  (the other-file case red), the underscore rule applied under a resolved path
  (the one-word case red), the underscore rule dropped from the fallback (the
  three unresolved cases red), a dotted name left whole (three red), and the
  count dropped (13 red).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `ANCHOR_RE`'s inline path and unquoted-locator strings | `ANCHOR_PATH` and `ANCHOR_NAME`, from which both `ANCHOR_RE` and `RECORD_COORD_RE` are built |
| the frame's `tests/test_release_hygiene.py#overwide_rows` in `plan.md` *Technical context* · NAME NOT IN TREE | corrected in place to `evidence_check.py#overflow_rows` with a dated note |
