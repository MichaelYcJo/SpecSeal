# 1791076834-the-changelog-is-one-file-per-release — phase 0

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 0 |
| Commit | e509d033 |
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
the files that section names.

**At the hand-back the release branch had moved** to `edee5ca2`: #756, #757
and #758 squashed. It was merged in at `e509d033` (a merge, no rebase) with
no conflict. The greps were run again over what the merge brought, every
added or removed line outside the records naming `CHANGELOG`, `changelog`,
`section_body`, `live_markers`, `gathered_fragments` or `gathered_entry`:
none (executed). **Q6: none** — no wave-1 branch added a reader or writer.
`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`,
which #757 added, passed on the merged tree with the build's other narrow
modules: 1236 passed (executed).

**The merge left the evidence for two units in three readings.**
`CONTRIBUTING.md#"## House rules"` and `skills/update/SKILL.md#"## Procedure"`
were edited by #757 and by this work, and each side's re-read recorded the
content its own branch had. This work's re-reads were taken again against
the merged content, and #757's own row E5, a fragment row whose claim (the
encoding bullet) the merge did not touch, was re-stamped in place in its
fragment with a note saying so. `evidence-check --strict .` then reads 10
drifted rows, every one of them drifted at `origin/release/v0.18.1` on its
own (read from a `git archive` of that tip: `templates/config.md`,
`tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT` and
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py#fake_venv`, in the
fragments of #756 and #758 and the released rows they re-read), and none of
this work's. Why those three drift is not this work's to answer; it is
unread here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
