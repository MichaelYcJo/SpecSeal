# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 6909aa80 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The records, under the declared ledger freeze:

- ledger rows for the new and changed units in this work item's fragment;
- `Corrected ·` rows for `seal/releases/0.18.1.md` B3 and `Corrected · S5`;
- a re-read row for each other released coordinate the change drifts (Q2),
  through `evidence-check --reverify --into seal/ledger/<id>.md --checked 2026-10-04`;
- the changelog fragment.

`evidence-check` over the tree was to report no drifted row left unanswered.

## What this phase found

- **Q2: 39 coordinates drifted across 10 released files after phase 2, and
  4 more after this phase's own exemption row (below), in 18 families.**
  Every row citing one was read before the re-read was written.
  - **Corrected, two families.** B3 and `Corrected · S5` (0.18.1) stated the
    root split: a file the root's tree lacks reads `new` without a run. Their
    `Corrected ·` rows carry every coordinate the claims rest on now,
    including S1–S4's cases.
  - **Re-read, sixteen families.** Their claims are about other parts of
    the anchors that moved, and each holds:
    - `templates/config.md` §*Broad gate*, the whole of
      `templates/config.md`, and `skills/verify/SKILL.md` §*The broad gate*:
      S4, the one-owner criterion, the backgrounding `&`, the pipe documents,
      N3, A2, S1, C4 (0.15.4), P2-2, P10, P11, R9, P2, B4 and S8.
    - `tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT`: C4 (0.18.0).
  - A2's "`gate` and `compare_at_base` are its only two `shell=True` callers"
    holds because the candidates share the one `run` call (`phases/phase-2.md`).
  - B4's "the two reasons are pinned whole" holds with `NO_RUNNER`'s new
    parenthesis.
- **The fragment's placeholder hashes were filled by the same run.** Every
  coordinate was written `@00000000`, and `--reverify --into` re-stamped the
  fragment in place before it wrote the citing rows. The citations of the two
  released rows took their line hashes from it too.
- **The records arm started reading this work item once it had a ledger
  fragment.** It refused three backticked names in the frame, two pytest
  functions named in `spec.md` line 55 and `plan.md` lines 66–67, which
  live in pytest's own source and not in this tree. That also turned
  `test_this_repositorys_own_records_state_nothing_the_tree_lacks` red. Each
  of the three lines now carries ` · NAME NOT IN TREE`. This is the one write
  into the framer's files, and `overview.md` records it.
- **The gate's comment names pytest-xdist 3.8.0, and the release hygiene
  case refuses any version above the running one.** The class is already
  declared: a loaded file naming the tool build a measurement was taken on.
  `VERSIONS_OF_ANOTHER_PRODUCT` gained the row for this file and token. The
  case was seen red before the row was added (`broad_gate.py:1874 names 3.8.0`).
  The row drifted C4's anchor, which is the sixteenth re-read above.
- After this phase, `bin/evidence-check .`: 5303 ok · 0 drifted · 0 broken,
  and the records arm read this work item with 0 refused.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the released rows stay as they are; a `Corrected ·` row supersedes, and nothing is deleted | none |
