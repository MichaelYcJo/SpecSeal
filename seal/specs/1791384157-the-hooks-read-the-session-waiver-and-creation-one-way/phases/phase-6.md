# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | efb73268 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The fragments and the closures: the ledger fragment with a row per scenario
and the `Re-read ·`/`Corrected ·` rows for G3, G6 (0.17.0), W1 (0.18.2), T1
(0.18.3), F3 and R1 (0.20.0), written in one pass; `changelog.md` naming
#868 and #856 and carrying phase 1's two figures; `overview.md` with the
divergences, the `Not verified` table and what was fed back; `plan.md`'s
Status column closed. Verified by `bin/evidence-check . --strict`,
`bin/correction-check`, and the text-hygiene modules, with the eight
suite-wide guard modules the orchestrator added.

## What this phase found

**The class was wider than the modules the phases named.** Before writing
the released rows, every module touching a changed hook was run (45
modules): `tests/test_the_waiver_can_be_typed.py` still pinned `# don't
[no-review]` and `# it's [no-review], deliberately` as waiving. They are the
same form phase 5 rewrote in the heredoc module, so they were rewritten the
same way at 38b2cdde: the apostrophe-before rows stop and name the waiver
typed in front, and two apostrophe-after rows waive (§12).

**Seven released rows are corrected, and the rest re-read.** Of the 89
released rows citing a coordinate this branch drifted or broke, seven make a
claim the branch changed or cite a unit it removed: W7 (`judgeable`), G3
(the lease route reads `CLAUDE_PID` first, and the stub one variable), W1
(`_reads_marker`), W3 (the apostrophe comment form), W4 (the one reader's
base is both base reads), T1 (`has_token`'s own read and `_without_bodies`)
and `Corrected · M1` (the clone consent is filed under is the guard's now,
not `86256492`'s). Each claim of the rest was read against the change and
holds, and `evidence-check --reverify --into` wrote 51 `Re-read ·` rows for
them.

**Of the six rows the plan named, four are re-read and two corrected.** G3
and T1 are corrected; G6, W1's sibling rows, F3 and R1 hold. R1 already says
`--root` is read "off the words once their redirections are off"; the
phrase S14 meant was the docstring's, which phase 3 corrected, so R1 takes a
`Re-read ·` row.

**What each check said, executed:** `bin/evidence-check . --strict` 7,043
ok and nothing drifted, broken or malformed; `bin/correction-check --range
5623d728..HEAD` exit 0, no merge in the range and no released ledger file
changed; `bin/unverified-check .` reads this overview's three open rows; the
eleven suite-wide and text-hygiene modules and the eight that read changelog
fragments pass.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
