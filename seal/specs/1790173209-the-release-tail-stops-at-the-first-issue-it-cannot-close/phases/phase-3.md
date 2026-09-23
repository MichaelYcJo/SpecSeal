# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — phase 3

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/phases/phase-3.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 451fd955 |
| Ran by | unknown — the spawn prompt handed over no value; the spawning session fills this row |

## What this phase was asked

#289. `insert(text, block, version)` appends into an existing `## <version>`
section keeping its date; a `tests/test_release_hygiene.py` case refuses a
duplicated `## X.Y.Z`; `docs/release-checklist.md` §2 says a second gather
appends. Verified by S7 (seen red: two headings at `HEAD`), S8 (the fixture
seen red), and `test_gathering_twice_writes_one_copy` still green.

## What this phase found

**The date is decided in `main`, not in `insert`.** `existing_date(text,
version)` reads the heading the file already has, and `main` builds the
block with that date, so the dry run prints the heading the entries will
actually join and `insert` only has to drop the block's first two lines. The
alternative — `insert` rewriting the heading — would have the preview and
the write disagree.

**`insert` gained a third argument, and one caller outside its own test
module had the old shape.** `tests/test_a_release_publishes_its_note.py`
calls `gather.insert(...)` to prove the release-note reader reads what the
gatherer writes; it passes the version now. Found by running the module,
not by grep: it was the fourth module in the narrow run for this phase.

**Red at `1a3e65d8`, quoted.** The append case:

```
E       AssertionError: the second gather wrote a second heading, or re-dated the first: ['0.2.0 — 2026-09-16', '0.2.0 — 2026-09-15', '0.1.0 — 2026-09-01']
```

The dry-run case, at the same commit, printed `## 0.2.0 — 2026-09-16`, a
heading dated the day it ran. The hygiene reader's fixture case is green
from its first run, because the reader and the case landed together; the
real-tree case was seen red by planting a second heading for the running
version in this repository's own `CHANGELOG.md` and restoring the file from
a copy kept in the script:

```
E       AssertionError: CHANGELOG.md heads <the running version> twice, at lines [3, 7]. One release, one section: merge the later heading's entries into the first and delete it
```

Green at `9657bcd0`: `83 passed` over `tests/test_the_changelog_is_gathered_at_release.py
tests/test_release_hygiene.py tests/test_a_release_publishes_its_note.py
tests/test_the_release_tail_does_not_end_at_the_tag.py`.

**Mutations**, six, each red on exactly one case; the list is in the ledger
fragment's P3 row.

**Two shared-ledger rows drifted** — the one on gathering being idempotent
and ordered (anchored on `insert`) and the one on `--check` refusing an
empty corpus (anchored on `main`). Both claims hold and both rows carry a
`Re-read 2026-09-23` note; `evidence-check --strict` exits 0 after
`--reverify`.

**The spec's S8 named `tests/test_release_hygiene.py` for the duplicate
case and the frame said the fixture is where it is seen red.** The fixture
case exercises the reader; the real-tree case is the one that fails a
release, so that is the one shown red, on the real file, as above.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
