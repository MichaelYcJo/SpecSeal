# 1788789330-the-update-notice-names-the-expensive-move — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `4bdb05f` |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

The notice at `hooks/version-check.py:151` and the same claim one level up at
`:18` name `/reload-plugins` and say what it does that a restart also does —
refresh what a spawned agent is handed. The hooks and agent-definitions half is
stated at whatever confidence it actually has, never asserted as measured.
`tests/test_version_check.py` pins the new wording and is seen red against the
old text first, with the hand-back saying how it was made to fail.

The handoff drew one boundary explicitly: run 6 of
`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` establishes
that a **preloaded skill body** handed to a **spawned agent** refreshes at a
reload, and the experiment measured nothing about hooks or agent definitions.
Silence there is not a claim either way.

## What this phase found

**The boundary is one axis tighter than the handoff drew it, and the extra axis
changes the wording.** Run 6 placed its sentinel in the version cache directory
of the **running** version and then reloaded, so what it measured is a re-read
of the copy already in force. The experiment record carries that without naming
a plugin version: its §*Method* installs no second version, and runs 1–4 failed
**because** they edited the marketplace clone rather than the copy that loads.
The path with a version in it is at
`seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/questions.md`
Q1 (round 1, finding 5 — this record cited it to the experiment, which does not
carry it).
It measured nothing about a session picking up a **newly installed** version
directory — which is the case a user is actually in when this notice fires.

That makes the ticket's own summary — *"a full restart is not required to get
it"* — broader than its evidence. Writing that sentence would have been an
inference labelled as measured, which is the one thing the handoff forbids
outright. So the notice names three unmeasured things rather than two: hooks,
agent definitions, and moving a running session onto the new version.

**A prose assertion over the whole message is not a pin.** The first draft
asserted `"measured" in msg`, and the mutation that dropped the source label
from the reload's own clause **survived**: the word was still present in the
sentence about what nobody has measured. The case now splits the message into
sentences and holds each claim to its own — the reload's clause must carry
`measured`, and the gap's clause must carry both halves and a negation. Six
mutations, six killed. Recorded because the surviving mutation is the finding:
a substring test over a multi-sentence message pins the message's vocabulary,
not any of its claims.

**What the next phases inherit.** The three-part boundary above is the sentence
`skills/update/SKILL.md` and both READMEs have to carry too, at the length each
has room for. The notice carries the short form because it competes for a
user's first screen; the skill is where the run that would settle it gets
named.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `"Either way, restart to load it."` — the notice's closing sentence | replaced in place by the longer close naming both moves; nothing else carried that sentence |
| The docstring's `keeps what it loaded until a restart` as an unqualified claim | narrowed in place at `hooks/version-check.py:18`. The claim it was making about `$CLAUDE_PLUGIN_ROOT` survives; only the part the measurement contradicts is gone |
