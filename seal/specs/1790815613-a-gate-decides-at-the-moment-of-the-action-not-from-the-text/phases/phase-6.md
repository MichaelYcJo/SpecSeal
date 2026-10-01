# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | c5f650c5 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

As planned: deletion, policy, contract, ledger. `hooks/cmdline.py` reduced
to `hooks/tokens.py` (W5), `hooks/commit-review-gate.py` deleted, and
`hooks/cmdline_base.py` deleted unless P4 keeps it. The two policy documents
rewritten around the action, with the migration table and #689's two whites
closed by deletion. Contract §9 and §17, `agents/smith.md`,
`skills/implement/SKILL.md` §1, the template comment, both READMEs and this
repository's `CLAUDE.md` rewritten to what is true. Ledger rows anchored on
removed units REMOVED, new claims in the fragment, drifted rows re-read
(W4). The changelog fragment with its operational note. S14, S15.

## What this phase found

- **Nothing was deleted, and P5 says why.** P1's answer keeps a foreign-slot
  clone on 0.16.0's behaviour, so `commit-review-gate.py` and `cmdline.py`
  stay as that clone's commit reading, and P4's answer keeps `cmdline_base.py`
  for the switch arm. `hooks/tokens.py` is new beside them (W5). Since no
  anchored unit went, no ledger row was REMOVED.
- **The policies describe two mechanisms, honestly.**
  - `docs/commit-review-gate-spec.md` gains §*The commit gate inside git*:
    seven folded statements, each with an `Enforced by:` line that
    `fold-check` resolves. A known-limits list and a table say where each
    repository state stands, and the PreToolUse section opens by saying it
    is the fallback.
  - `docs/worktree-guard-spec.md` gains *Where git decides: post-checkout*
    (four statements) and a note under §B. §*Which tree* says the switch arm
    keeps the frozen reading on every git, and §*Known limits* has three new
    entries.
- **#689's two whites closed by correction, not deletion,** because the text
  they sat in stays.
  - The commit gate's "both gates import it" comment now says the guard
    reads `cmdline_base.py`.
  - The zsh list gained `foreach i (…) cmd`, which `hooks/cmdline.py:1563`
    already read.
- **The contract and the definitions keep their pinned sentences.**
  - §9's second reason and both of §17's are about a reading of the command,
    and each section now says that reading judges only a foreign clone.
  - The routing paragraph in `CLAUDE.md` and `templates/claude-md-block.md`
    (one source, held by a test) no longer says the gate denies the whole
    Bash call everywhere.
  - The git-native waiver is named beside the old one in the contract, the
    smith, the implement skill and both READMEs.
  - The smith's §9 sentence was reworded once, because its first draft
    shared 15 words with §17 and `test_a_moved_rule_leaves_its_definition`
    refused it as a copy. Its RIDER was re-measured (True, one, one) and
    re-stamped.
- **The ledger.** `evidence-check --strict` named 32 drifted anchors on 30
  rows across 16 release files. Each was read against the edit, and five
  were corrected in place:
  - the implementer-notice rows of 0.4.0 and 0.11.0, whose "after a command
    that invokes `git commit`" holds only where the reading still runs;
  - 0.16.0's E7, "nothing the base stops reads silent", the invariant the
    owner replaced;
  - 0.16.0's M2, "the commit gate reads both";
  - 0.16.0's M4, "`commit-review-gate.py` is `542f920b`'s byte for byte".
  The rest hold and carry a dated re-read note. Every row was re-stamped
  with `--checked 2026-10-01`. The commit that did this, `cb756b18`, says
  "45 drifted rows" in its subject, which was an estimate and is wrong; 30
  is the count. G1–G13 went into this work item's fragment.
  `evidence-check --strict .` exits 0.
- **Two git names became tree names, so the records check could read them.**
  `GIT_DIR` and `GIT_REFLOG_ACTION` appeared in this work item's records
  only. Each now stands in the docstring that owns its fact: `commitgate.py`
  says why no hook reads `GIT_DIR`, and `githooks.py` why
  `GIT_REFLOG_ACTION` is no criterion. `AUTO_MERGE` carries the record's
  `NAME NOT IN TREE` marker.
- **`test_release_hygiene` refuses a loaded file naming a version at or above
  the running one,** and the policy names the four gits phase 1 measured on.
  They were added to `VERSIONS_OF_ANOTHER_PRODUCT`, keyed by file and
  token, as `seal.py`'s and `broad_gate.py`'s git builds already are.
- **Survivors.** `survivor-check --range cd24f516..HEAD` reported six places.
  Each states something still true or is an earlier work item's record of
  its own moment, and each is recorded in `survivors.md` with a quote.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the guard policy's "#692 … deletes the frozen copy" | `docs/worktree-guard-spec.md` §*Which tree*, which says the copy stays and why |
| `CLAUDE.md`'s unconditional "the gate … denies the WHOLE Bash call" | the same paragraph, scoped to a foreign clone |
