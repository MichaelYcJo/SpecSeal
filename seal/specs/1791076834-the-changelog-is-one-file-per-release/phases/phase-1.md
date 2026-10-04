# 1791076834-the-changelog-is-one-file-per-release — phase 1

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 51430aff |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The migration and the writer: the 44 sections of `CHANGELOG.md` written to
`changelog/<X.Y.Z>.md` by a throwaway script, `CHANGELOG.md` rewritten as the
index of spec D2, `gather_changelog.py` writing and checking the new layout
(scope 3), the gather's test module moved to it with S4–S8, S2 and the
file-exists half of S3 as standing real-tree cases, `conftest.py#gathered_entry`
and `test_handoff_outlives_the_merge.py` reading the release files (S13), and
`changelog` classified as staying home and excluded beside `CHANGELOG.md` from
the pact's tree-drawing grep (S14). Every new case seen red first; every I/O
added names `encoding="utf-8"`.

## What this phase found

**S1 holds on the tree the build stands on (Q5).** The throwaway script split
the base file at its 44 `## ` lines and wrote each part with its trailing
newlines cut to one. The probe, a `test_tmp_*` file run once and deleted, read
`git show e141980a:CHANGELOG.md` (the merge base with
`origin/release/v0.18.1`) and the 44 files joined newest first under
`# Changelog` and a blank line, and printed:
`base e141980a files 44 old bytes 577907 joined bytes 577907 identical True`
(executed).

**The marker count and the commands S13 counts did not move** (executed).
`gather_changelog.py --check` printed `53 changelog fragments, all gathered;
170 work items marked in CHANGELOG.md` before the migration and `53 changelog
fragments, all gathered; 170 work items marked in changelog/` after. The `git mv`
scan of `test_handoff_outlives_the_merge.py` examined 2 commands in
`CHANGELOG.md` before and 2 across `changelog/*.md` after, none of them
prescribing (a command named in a sentence, or elided).

**The index paragraph (Q7).** It says each release is `changelog/<X.Y.Z>.md`,
that the index heads each with the line its file opens with and a link, and
that a change writes its fragment and release preparation gathers it with
`gather_changelog.py --version X.Y.Z`. The index is 185 lines.

**The gather's printed lines (Q7).** `--check` prints
`changelog fragments that never reached a file under changelog/:`,
`N changelog fragments, all gathered; M work items marked in changelog/` and
`… no <!-- specs/<work-item-id> --> marker in any changelog/<X.Y.Z>.md …`;
a write prints `gathered N fragments into changelog/X.Y.Z.md, ## X.Y.Z — D`
and, where the index took the entry, `CHANGELOG.md now heads its index with
## X.Y.Z — D`; a dry run opens with `into changelog/X.Y.Z.md:`. Each is pinned
in the gather's module.

**Two branches the spec did not name, each with its case.** A first gather
into a root with no `changelog/` makes the directory and gives an index with
no `## ` line its first entry below its own text. A version the index already
heads while its file is missing takes the index's date for the new file, so
the two copies of the heading stay one line (S2).

**Each release file is read on its own.** `released_markers` reads the live
markers file by file, so a fence one release file leaves open hides nothing
in another; read as one joined text it would.

**The pact grep's `changelog/` exclusion cannot be seen red, and neither
could the `CHANGELOG.md` one it sits beside.** `git grep -l` for a tree line
naming `parity.md` finds nothing in `CHANGELOG.md` at `e141980a` and nothing
under `changelog/` now (executed), so the spec's *the moved text carries the
same drawings* does not hold of the tree. The exclusion is kept as the old
one was, a guard for a drawing a later entry quotes, and the mutation that
drops it survives by construction.

**Seen red (§15), executed.** The gather module run against `e141980a`'s
`gather_changelog.py`: 37 failed, every new case among them, and the
refusal cases (S8) passed, as re-pointed old cases whose behaviour did not
change. Then one mutation at a time through `mutation-check`, each red:
`indexed` placing the entry at the end, dropping the blank line on its
no-heading arm, and losing its early return; `released_markers` reading one
file, and reading one joined text; `release_files` keeping a `README.md`, and
sorting oldest first; `main` never writing the index, ignoring the index's
date, inserting into an empty file, making no directory, printing no file on
a dry run, and naming `CHANGELOG.md` in its missing line; `index_entry`
linking elsewhere; `gathered_entry` reading no release file; S2 against a
wrong link, a drifted heading and a second `## ` line in a release file; S3
with `changelog/0.18.0.md` moved away; S14 with `changelog` unclassified.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the released sections' text in `CHANGELOG.md` | `changelog/<X.Y.Z>.md`, byte for byte (S1) |
| `tests/test_the_changelog_is_gathered_at_release.py`'s assertion that a second gather's entry sits before `## 0.1.0` in the same file | the same case's assertion that the release file ends with that entry, and that the index is unchanged (S5) — the older release is a file of its own now |
