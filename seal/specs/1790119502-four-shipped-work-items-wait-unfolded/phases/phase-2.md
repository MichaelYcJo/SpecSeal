# 1790119502-four-shipped-work-items-wait-unfolded — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 05a1c7e |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Resolve the six references into the four directories while they still exist:
the four test docstrings and `docs/branch-and-release.md` gain
`at \`b0cbd34\`` after the path they cite (`spec.md` G2), and
`docs/release-checklist.md` §6's pointer to *the work item that built this
box* names the repository owner instead (L5). Re-read and re-verify the one
ledger row anchored on §6.

## What this phase found

**Every cited path resolves at `b0cbd34`, and `b0cbd34` is on `main`.**
`git cat-file -e b0cbd34:seal/specs/1790076050-…/phases/phase-N.md` exits 0
for N = 1 to 4, and `git merge-base --is-ancestor b0cbd34 origin/main` exits 0.
`b0cbd34` is also `origin/release/v0.13.2`'s tip, so the cited files are the
ones the fold removes, byte for byte.

**The SHA pin was then replaced, by the orchestrator's decision, in a
correcting commit after this phase closed.** The repository's history is to be
rewritten into a new repository after this release, which changes every
commit hash, so a SHA written into a file now dangles there — and before this
phase exactly one commit-resolving SHA stood in the tree outside the ledger,
inside a directory this fold retires. So no file outside `seal/specs/` names
`b0cbd34` any more. Each of the four docstrings now says the mutations *were
recorded in phase N of work item `1790076050-…`, whose rule
`docs/branch-and-release.md` §*Cutting a release* now carries*, and the
`docs/branch-and-release.md` sentence names the same work item and points at
its marker, which phase 3 put directly above that paragraph. The path is gone
from all five: a path into a retired directory resolves for nobody, and the id
is what `settle` §2 says a reader traces through git history. `spec.md` G2
carries the one-line record of the change. The measurement below — the four
files resolve at `b0cbd34` — is what this phase found before the change and is
kept as found.

**The references outside `seal/specs/`, recounted:** `CHANGELOG.md` 4,
`docs/branch-and-release.md` 1, `seal/follow-up.md` 4, `seal/ledger.md` 33,
`tests/` 4. That is the frame's table exactly; only the docstrings and the one
`docs/` line are paths, and the rest are markers or provenance naming an id.
The checklist's pointer names the work item by description, so the grep does
not see it, as the frame said.

**The pinned sentence is not the one this phase rewrote.**
`tests/test_the_plugin_directory_answers_the_box.py` asserts
`"readable from nowhere public"` — against the script's output, not the
checklist — so rewriting the checklist's clause moves no literal. The script's
own sentence (`plugin_directory_check.py`, *Whether a submission has been
ACCEPTED is readable from nowhere*) names no work item and is left alone.

**One ledger row drifted, and it is the one the frame named.**
`bin/evidence-check --strict .` after the edits: `1467 ok · 1 drifted`, the
drift being `docs/release-checklist.md#"## 6. After the merge"` — S9, at
`seal/ledger.md`'s row for 1788354065's close-issues trigger. Re-read: the
claim is that §6 states the trigger and the input the tree has, and its own
executed check still reproduces (`grep -c "on the tag"
docs/release-checklist.md` → 0). A dated `Re-read` note was appended to the
row's last cell, then `bin/evidence-check --reverify .` rewrote exactly one
hash, `73f935ed → 5fd6bcab`. After it: `1468 ok · 0 drifted · 0 broken`,
exit 0. No row was added, removed or re-pointed.

**Run for this phase, each exit read directly:** the four docstring modules,
`tests/test_the_release_tail_does_not_end_at_the_tag.py` among them, and
`tests/test_docs_line_wrap.py` — `80 passed`, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *the work item that built this box carries it as an open question* (`docs/release-checklist.md` §6) | the same box, naming the repository owner as who answers it |
