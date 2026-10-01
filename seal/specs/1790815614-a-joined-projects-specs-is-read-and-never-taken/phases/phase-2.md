# 1790815614-a-joined-projects-specs-is-read-and-never-taken — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8f84d66a |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

The bootstrap paragraph in `skills/implement/orchestration.md` sends a bare
`specs/` to the shared/local question and keeps *told, not asked* for the
marked case; both READMEs' *Coming up from 0.3.x* say a marked directory
moves and the rest stays, the by-hand block untouched; one dated section in
both editions of `docs/one-root-by-lifetime.md`; a `KEEP` entry only if the
wording spells `specs/<`. Re-read the Bootstrap-heading and README rows. A1
seen red with the sentence deleted.

## What this phase found

**Q1 answered by the work: spelled around, and one `KEEP` entry anyway.**
The marks are written `<unix-seconds>-<slug>`, so nothing spells `specs/<`.
But `OLD_ROOT` has two halves, and the row asked about one. The rewrapped
paragraph moved `.specseal/` onto a line with a comma after it, which the old
`KEEP` key `` `.specseal/` or a top-level `specs/` `` no longer matched. The
old key stays in use through `templates/seal-README.md` and `seal/README.md`
line 51, which phase 5 rewords — **phase 5 must check that key still occurs
somewhere, or retire it with the line it carried**
(`test_every_keep_entry_is_still_in_use` fails otherwise).

**A row anchored on a ledger section drifts with the notes written into
that section.** `seal/releases/0.13.1.md`'s row cites
`seal/releases/0.4.0.md#"### 1788331011-two-roots-hold-three-lifetimes"`, and
every dated note this work item appends to a row under that heading moves
its hash. Phase 1 missed it: the check ran before the notes were written.
Phase 2 caught it and covered both phases in one note, with the two-pass
re-stamp its earlier notes describe — the 0.4.0 notes first, then the 0.13.1
re-stamp. **Any later phase that edits a row in that section owes the same
two passes.**

The design record's new section corrects two places above it and rewrites
neither: the *first-setup question's shape* row and §*What happens to the
existing directories at the switch*. The second row of the section
(*whose a `specs/` outside the root is*) names the `Reference specs` row,
which phase 3 builds, so the record ran ahead of the tree for one phase;
phase 3's commit is where it becomes true.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The bootstrap's "a top-level `specs/` is on the 0.3.x layout", which read the layout off a directory name | `skills/implement/orchestration.md` §*Orchestrator: Bootstrap*, the 0.3.x paragraph and the one after it; row A1 of `seal/ledger/1790815614-….md` |
