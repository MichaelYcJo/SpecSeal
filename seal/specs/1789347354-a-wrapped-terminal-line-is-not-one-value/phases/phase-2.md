# 1789347354-a-wrapped-terminal-line-is-not-one-value — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 02e4436 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Make the four descriptions of the stop rule true of the pattern that ships,
each naming what the guard does **not** cover, with the blank line stated as
the only stop that covers every shape. Pin the warden's sentence with a case
seen red with it stashed, keep `tests/test_the_rules_have_one_owner.py` green,
and run `evidence-check --reverify` to re-stamp
`agents/warden.md#"## Report"`, which `spec.md` predicts DRIFTED.

## What this phase found

**Q6's answer is that nothing drifted, and the reason is not that the edit
landed where it should.** `bin/evidence-check .` reports `1181 ok · 0 drifted ·
0 broken`, exit 0, with the warden's wrap paragraph rewritten. `spec.md`
§*Data & interfaces* predicted DRIFTED and said *if this anchor moves, the
edit went in the wrong place* of a different row — so a reading was owed
rather than a re-stamp.

**`evidence_check.py#file_units` does not skip fenced blocks when it looks for
markdown headings.** Measured by calling it on `agents/warden.md`:

| Unit it reports | Lines |
|---|---|
| `"## Report"` | 285–355 |
| `"## Verdicts"` | 356–360 |
| `"## Executed probes"` | 361–365 |
| `"## Deferred"` | 366–375 |
| `"## Paste-ready fixes"` | 376–436 |

The last four are not headings. They are the report's own example headings,
shown inside a fence in §*Report* so a reviewer can copy them. So
`agents/warden.md#"## Report"` covers 71 lines and stops at the fence, and the
wrap paragraph at 406 sits in a phantom unit. **R7's anchor does not cover
half of what R7 claims**: the row asserts the report carries the three tables
*plus the two terminal lines*, and the terminal lines are at 400–405, outside
it. An edit to either is invisible to the checker.

**The class, enumerated.** Thirty-six markdown files carry a ledger anchor and
three of them hold a heading inside a fence: `agents/warden.md`, `README.md`
and `README.ko.md`. In the two READMEs the phantom units come from shell
comment lines inside install fences, and they truncate the top-level unit at
line ~301 of a ~655-line file.

This is a gate's own reader and fixing it re-hashes rows across the whole
ledger, so it is out of this work item under `CONTRIBUTING.md` §*What a change
to a gate must carry*. It is handed over rather than carried: a row in this
work item's ledger fragment, `overview.md` §*Not verified*, and the pull
request body.

**No re-stamp was run.** `--reverify` rewrites a row's hash to what its anchor
holds now, and nothing this phase touched is inside any anchor, so it would
have rewritten nothing and asserted a re-read that the anchor cannot support.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `agents/warden.md`'s enumeration of the three stops — *stops at a blank line, at the other terminal label, or at a line opening a new markdown block* | `docs/review-handoff-protocol.md` §*The Needs a fix field — the answer a run ends on*, which phase 3 makes the owner. The warden keeps the operative half and names that section |
| The implication, in `test_prose_below_the_terminal_block_is_not_swallowed`'s docstring, that the case exercises the block-opener stop | The same docstring, which now says it exercises the blank-line stop and names the case below it that has no blank line in the way |
