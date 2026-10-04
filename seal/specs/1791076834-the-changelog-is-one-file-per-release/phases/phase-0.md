# 1791076834-the-changelog-is-one-file-per-release — phase 0

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 0 |
| Commit | none — the base had not moved, so there was nothing to merge; the hand-back's fetch is recorded below |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build from the current base while the three wave-1 pull requests of 0.18.1
(#757, which adds an AST check that every file read or write names its
encoding, then #758 and #756) wait for the owner's squash. Before handing
back, fetch, merge `origin/release/v0.18.1` in if it moved (a merge, never a
rebase), then rerun the spec's two by-construction greps, and
`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` if it
exists.

## What this phase found

At the start of the build `origin/release/v0.18.1` was `e141980a`, the
branch's base, so there was nothing to merge. The two greps of `spec.md`
§*The readers and writers, by construction* (`git grep -n CHANGELOG` and
`git grep -n -i changelog` over the tree less the records, and the importer
grep for `section_body`, `live_markers`, `gathered_fragments` and
`gathered_entry`) were run on the worktree at `c083bb51` and listed exactly
the files that section names. Q6 is answered `none` at the start; the
hand-back fetch answers it again.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
