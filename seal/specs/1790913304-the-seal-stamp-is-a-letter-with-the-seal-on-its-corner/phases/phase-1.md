# 1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e81b6138 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Measure the harness's threshold for a `Stop` hook's `systemMessage` with a
scratch project's hook and one headless `claude -p` turn at 9,990 and at
10,010 characters, outside this repository and the user's settings, and
delete everything the probe made. Then `seal_stamp.py` gains
`MESSAGE_LIMIT` (the measured value), `MESSAGE_BUDGET` (the limit less a
reserve of at least 1,000, the reserve's reason in the comment),
`SCALE_LADDER` and one fitting function over the blocks and a budget;
`hooks/sealer-stamp.py#main` prints the fitted message, `drawings` keeping
its contract; the hook's docstring gains the budget paragraph and
`docs/the-broad-gate.md` §*Where the stamp is drawn* the rule under this
item's marker with its `Enforced by:` line. Cases A2, A3 (one file and two,
through `dispatch.py stop`), A4, A15's byte comparisons made against the
fitted message, the policy pin, and S9 of `test_a_gate_that_fails_says_so.py`
green unchanged.

## What this phase found

**The frame holds for this phase.** `hooks/sealer-stamp.py#drawings` and
`#main`, `hooks/dispatch.py#report` (the prepend after the hook prints),
`MESSAGE_CAP` and `seal_stamp.py#stamp` stand where `plan.md` §*Technical
context* puts them.

**Q1 is measured, and the limit is 10,000 characters.** Claude Code 2.1.287,
a scratch directory under the session's scratchpad with a
`.claude/settings.json` registering one `Stop` hook that printed
`{"systemMessage": <N characters>}`, and one `claude -p` turn per size with
`CLAUDECODE` unset for the child. The scratch project's directory under
`/Users/x/.claude/projects/<scratch project>/` was listed after each run:

| N | Content | Bytes | A `hook-*-systemMessage.txt` in that session's `tool-results/` |
|---|---|---|---|
| 9,990 | `x` | 9,990 | none, and no `tool-results/` directory |
| 10,000 | `x` | 10,000 | none, and no `tool-results/` directory |
| 9,990 | `▀` | 29,942 | none, and no `tool-results/` directory |
| 10,001 | `x` | 10,001 | `hook-<uuid>-2-systemMessage.txt`, 10,001 characters |
| 10,010 | `x` | 10,010 | `hook-<uuid>-1-systemMessage.txt`, 10,010 characters |
| 12,000 | `x` | 12,000 | `hook-<uuid>-2-systemMessage.txt`, 12,000 characters |

So a message of more than 10,000 characters is persisted, and the unit is
characters: 29,942 bytes of `▀` were shown. The plan's two sizes became six,
because 9,990 and 10,010 alone leave the limit anywhere in twenty characters
and say nothing about the unit. `MESSAGE_LIMIT = 10000`, labelled executed in
its comment. The probe's scratch directory, the scratch project's directory
with its six transcripts and three persisted files, and the six sessions'
empty `/Users/x/.claude/session-env/<session>/` directories were removed;
a search of `/Users/x/.claude` for the six session ids then found nothing.

**The reserve is 1,000, and it covers two failed gates.** Measured over
`dispatch.describe` with every gate in `GROUPS` failing to load and its
message at `MESSAGE_CAP`: the longest report for one gate is 533 characters
with its separator, for two 909, for three 1,274. The comment says the
third would pass the limit beside a stamp at the budget.

**The fitting function is `seal_stamp.fitted(blocks, budget)`**, `blocks`
being `(label, rows, scale)` per file (Q4). The rungs are the files' own
scales, then `SCALE_LADDER` capped at each file's scale so no file is drawn
larger than it asked, then `stamp(rows, None)`, which is the panel with no
disc. `stamp` takes `scale=None` for that last rung rather than a second
function, so the twin and the block form keep one entry point.

**Today's drawing steps down already.** Over #702's values file the stamp
under its label is 11,248 characters at 1.0, 10,171 at 0.90, 9,165 at 0.80
and 8,113 at 0.75, so the hook now prints it at 0.75. The stamp test's own
`ROWS` is 9,887 at 0.90 in this drawing and steps to 0.80, which is why its
byte comparisons were moved to the fitted message rather than to the 0.90
rendering; phase 3's drawing is what brings them back to 0.90.

**`drawings` hands `fitted` the rows rather than a finished block, and still
draws each file whole before the claim.** That call is what proves a file
draws at all, and its first mutation (the call deleted) SURVIVED every
case: no case had a file that `read_values` accepts and the band refuses.
`test_a_file_at_a_scale_the_band_refuses_is_left_pending` is that case, a
file at 0.5 beside a good one, and the same mutation is red against it.

**Red, as shown.** Before any code, all five new cases and the three moved
byte comparisons were red against the unchanged tree (`fitted` and the
constants absent, the marker absent). With the constants added and the hook
still printing every block whole, A3 was red on size: 10,176 characters for
one file and 20,354 for two, against a budget of 9,000 — the one-file
message over the measured limit itself. Twelve mutations through
`bin/mutation-check`, each red: `<=` to `<` in `fitted`; the cap removed
from `min(scale, rung)`; the files' own scale dropped from the rungs; the
last rung returning the 0.75 message; the no-disc rung returning one line;
`MESSAGE_RESERVE` 999; `MESSAGE_LIMIT` 10,091 and 10,050; a rung removed
from `SCALE_LADDER`; the hook printing `fitted` with an unbounded budget;
and the pre-claim drawing deleted, red only once the band case existed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/sealer-stamp.py#main` joining the blocks with `"\n\n"` itself | `seal_stamp.py#fitted`, which joins them at one rung |
