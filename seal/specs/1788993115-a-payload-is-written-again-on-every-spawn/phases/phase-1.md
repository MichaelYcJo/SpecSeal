# 1788993115-a-payload-is-written-again-on-every-spawn — phase 1

<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/phases/phase-1.md
— what this phase of the build did, written by the implementer when the
phase closed. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `2c05517` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build phase 1 of `plan.md`'s Phases table and nothing past it: the meter
(`skills/verify/scripts/payload_meter.py`, `bin/payload-meter` and its
`.cmd` twin) with the composition table per agent, a basis on every token
figure, `--sections`, `--json`, `--baseline` and `--calibrate`; the test
module `tests/test_the_payload_meter_says_what_it_measured.py` with a
fixture tree, a fixture transcript pair, the basis label, the
missing-baseline refusal and the delta; and `payload-before.json` written
from this session's main transcript before the first edit to any skill file.

The spawn prompt labelled its facts. Executed: the six calibration spawns
of `spec.md` §*Measured before the first edit* are the `agent-*.jsonl`
files under the session's `subagents/`, and the main transcript's `Agent`
tool_use blocks carry `subagent_type` while the matching tool_result carries
`agentId: <id>`. Read: `session_cost.py#spawn_labels`,
`#subagent_transcripts` and `#load` are the helpers to import, and the
`bin/session-cost` pair is the wrapper shape to copy. Unverified, with this
phase as answerer: whether `general-purpose`'s own built-in prompt is small
enough to treat its prefix as the harness constant.

## What this phase found

**The bytes the spawn read are not the bytes in the tree, and that closes
most of the spread `spec.md` could not explain.** `agents/smith.md` and
`agents/warden.md` list `writing-style`; the harness resolved that bare name
to `~/.claude/skills/writing-style/SKILL.md` (25,834 B) on this machine, not
to the plugin's `skills/writing-style/SKILL.md` (19,762 B). The evidence is
this spawn's own context, where the skill arrived with that base directory.
Over the bytes actually read the ratios are smith 2.87, warden 3.41, scribe
3.44 B/token, against 2.71 / 3.16 / 3.44 over tree bytes. The meter reports
the tree's file, notes the shadow on the row, and divides by the bytes the
spawn read (`ratios.<agent>.over_bytes`, `shadowed`). What the shadow does
not close: swapping `implement` + `agents/smith.md` for `code-review` +
`agents/warden.md` still costs 11,593 tokens for 20,080 B, and Q4's probe is
what settles that.

**The general-purpose question, read side by side.** The baseline prefix is
39,488 tokens; the two `CLAUDE.md` files (16,461 B) are roughly 5,000 of
those at any of the three ratios, and the rest is the harness's system
prompt, tool schemas, the skills listing and `general-purpose`'s own text.
Nothing in the six transcripts separates that last part from the others, so
the assumption stands unverified: the meter treats the whole baseline as
constant. The error it could carry is bounded by the size of that built-in
prompt — on the order of a few hundred to two thousand tokens by reading
the harness's own description of the agent, which is 3–30 % of the scribe's
6,568-token delta and under 6 % of the smith's. Q4's probe definition with
an empty `skills:` list measures it directly: its prefix minus the baseline
is the definition's bytes at the ratio minus the built-in prompt's tokens.

**`load` cannot pair a spawn with its `agentId`.** It keeps a call's spawn
labels and drops the `tool_use` id and the result text, so the meter reads
the main transcript itself, using `spawn_labels` at the block and
`subagent_transcripts` for the directory; `count` is imported for the usage
fields. `load` is not imported.

**Of several spawns of one agent, the smallest prefix.** A first message
carries the spawn prompt as well as the payload, so this smith spawn
(prompt-laden, the third of the transcript) was seen and not taken; the
count is reported beside the figure. The three `tmp-probe-*` spawns whose
result carried no `agentId` are listed under `calibration.unread` rather
than ending the run.

**The `CLAUDE.md` pair sits inside the baseline.** A calibrated delta
never covers it, so a calibrated total is measured for the agent's own files
plus an estimate for the pair, and the total's basis says so. Phase 4's
delta over the `implement` split lands entirely in the own-files region.

**`payload-before.json` is file-level**, no `--sections`: the delta compares
files, and the spec's JSON shape names files. Its `root` is `.`, its
transcript references are basenames, and it carries no `/Users/` path.

**`plan.md:94` failed `tests/test_no_real_identifiers.py` at `0bd135f`**,
before this phase's first edit: its placeholder for a home path matches
the user-path pattern. Corrected in the commit that closes this phase.

**Pinned elsewhere, not here.** The `.cmd` pairing is
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py#test_every_bin_entry_has_a_windows_twin`;
the new module pins only that the pair runs this script. `README.md` does
not name `payload-meter` yet; that is phase 4's document pass (Q6).

**Seen red.** All fifteen cases ran red before the script existed (3 failed,
12 errors). Then twelve mutations, one at a time with the original bytes
restored after each: dropping the pre-heading section, dropping the word
`estimated`, taking the largest prefix, subtracting a missing baseline as
zero, dividing by tree bytes under a shadow, reporting a file's size as its
delta, counting chars as bytes, leaving `cache_read` out of the prefix,
dropping a spawn with no `agentId` silently, filing the `CLAUDE.md` pair as
the agent's own, forgetting the pair in a calibrated total, ignoring a lent
ratio — each turned at least one case red, and the module is green again
on the restored file.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
