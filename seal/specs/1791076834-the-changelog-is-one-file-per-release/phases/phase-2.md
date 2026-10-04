# 1791076834-the-changelog-is-one-file-per-release — phase 2

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | baa731bc |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The publisher: `publish_release_note.py` reads `changelog/<version>.md` and
links to it (scope 4, S9), `tests/test_a_release_publishes_its_note.py` moved to
the new layout, and `publish-release.yml`'s header comment reworded. Verified
by that module and one probe calling `section_body` on `changelog/0.18.0.md`
and on the base's `CHANGELOG.md` for 0.18.0 — not by a real-tree `DRY_RUN=1`,
which exits before reading the body where a release already exists.

## What this phase found

**The body is unchanged by the move** (executed). The probe, a `test_tmp_*`
file run once and deleted, printed `old 14746 new 14746 equal True` for
`section_body(git show e141980a:CHANGELOG.md, "0.18.0")` against
`section_body(changelog/0.18.0.md, "0.18.0")`.

**`CHANGELOG = "CHANGELOG.md"` left the publisher.** Nothing outside it read
the constant (`git grep` for `mod.CHANGELOG` and `publish_release_note.py#`
citations, read), and the module now names `RELEASES = "changelog"` and a
`release_file(version)` the message and the link both use, so the two cannot
name different files. `section_body` keeps its name and its body (D4).

**A missing file and a file with no heading are one refusal.** The message
reads `<tag> was pushed and changelog/X.Y.Z.md is not there or carries no
`## X.Y.Z` section …` and names the gather command, pinned for both shapes by
the A3 case, now parametrized over them.

**Seen red (§15), executed.** The module against `e141980a`'s publisher: 20
failed, 5 passed — the 5 are the title and workflow cases, which read no
release file. Then through `mutation-check`, each red: the link pointing back
at `CHANGELOG.md`; the missing-file guard removed (the no-file case raises);
the message naming `CHANGELOG.md`; `release_file` returning `CHANGELOG.md`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `publish_release_note.py#CHANGELOG` | `publish_release_note.py#RELEASES` and `#release_file` |
