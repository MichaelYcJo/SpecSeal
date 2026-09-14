# 1789347354-a-wrapped-terminal-line-is-not-one-value — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | <this phase's commit> |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Write `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`, and the
re-stamps phases 2 and 3 earned. Verified by `evidence-check` over the
fragment: every row resolves, nothing drifted, nothing broken.

## What this phase found

**The re-stamps phases 2 and 3 were expected to earn do not exist**, and
`phases/phase-2.md` holds the reading. `spec.md` §*Data & interfaces* names
four anchors, predicts one DRIFTED and three unchanged, and the measured
answer is that all four are unchanged — the predicted one because the
checker's reader cannot see the paragraph that moved. Running `--reverify`
over them would have rewritten no hash while recording a re-read the anchor
cannot support, so none was run. The fragment's own eight anchors were stamped
by `--reverify` from `@00000000`, which is what that flag is for.

**The fragment is what made this work item visible to the records arm, and
that exposed a coordinate in `spec.md` that does not resolve.** Before the
fragment existed the arm read one work item; after it, two — and
`bin/evidence-check .` went from exit 0 to exit 2 on
`seal/specs/1789347354-…/spec.md:252`, whose `Data & interfaces` table
abbreviates the template anchor as `templates/sdd-round.md#"\| Needs a fix \|
…"`. The ellipsis is an abbreviation for a reader and the arm reads it as a
locator. CI runs the same command and fails on any exit of 2 or more
(`.github/workflows/test.yml:92-99`), so this would have opened the pull
request red.

The repair is the coordinate spelled in full, taken from `seal/ledger.md:89`'s
own spelling of the same row. **No claim in the table changed** — the
prediction it carries is still *Unchanged*, and it is still correct. This is
the builder editing the framer's contract, which is why it is recorded here,
in `overview.md` §*Where spec and implementation diverged*, and in the pull
request body rather than done quietly.

The sibling ellipsis on the row below, `agents/warden.md#"## Role">…`,
resolves and is left alone: its major level is a real heading, and only the
minor level is abbreviated.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `spec.md`'s abbreviated spelling of the template anchor | The same cell, spelled as `seal/ledger.md:89` spells it, so the arm can open what the table claims |
