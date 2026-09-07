# 1788789985-round-record-dies-on-python-3-9 — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `99d4df0` |
| Ran by | specseal:smith on Opus 5 (1M context) |

<!-- The spawn prompt named no model. The value above is the one the harness
states in the segment's own system prompt, which is a value it was GIVEN
rather than one it decided about itself — but it is not the orchestrator's,
which is where the template says the answer properly lives. Worth a correction
if the orchestrator's record disagrees. -->

## What this phase was asked

Take the ticket's second repair — check `sys.version_info` at entry and exit
with a sentence naming the minimum — rather than dropping `strict=True`, on
the grounds that `CONTRIBUTING.md:24-26` names 3.12 as the supported floor and
`.github/scripts/run_tests.py:56` holds it as `FLOOR`. Reuse `FLOOR` rather
than retyping `(3, 12)`, and argue in `spec.md` how a stdlib-only script under
`skills/` reaches a constant under `.github/scripts/` — or say what was done
instead, because a copied literal needs the argument and not silence.

Enumerate by construction, never by reading, the class *every script in this
plugin that a documented command tells someone to invoke directly with
`python3 <path>`*, and put the table in `spec.md` with rows for the ones left
alone too. Scope: fix `round_record.py`; do not edit `chain_check.py` or
`seal.py`, which two other work items in this release hold; defer every other
member with an answerer named.

## What this phase found

**The class is bigger than the ticket and its members are not all the same
shape.** Twenty-five entry points ship. Five carry a construct above the floor,
and only one of them is a `zip(strict=)` like the ticket's — three use
`datetime.UTC`, which is 3.11 rather than 3.10, so the floor a member needs is
not one number either. One member, `hooks/root-migrate.py`, is not invoked by a
person at all: `hooks/hooks.json` runs every hook through `python3
"${CLAUDE_PLUGIN_ROOT}/hooks/dispatch.py"`, so the harness hands it whatever
`python3` is on PATH exactly as an operator does. The property the handoff
worded as *a documented command tells someone to invoke directly* had to widen
to *a person or the harness invokes with whatever `python3` resolves to*, or
that member falls outside a class it plainly belongs to.

**The enumeration's own first spelling was wrong, and the next phase inherits
the corrected one.** `zip\([^)]*strict=` answered three of `round_record.py`'s
four sites: `:935` has an inner `verdict_words(reader, rows)` whose closing
parenthesis the character class stops at. `zip\(.*strict=` finds all four. This
is the failure mode the spawn prompt warns about, arriving inside the very
command that was supposed to prevent it — a class enumerated with a pattern
that cannot match every instance is a class enumerated by reading, with a
command's clothes on.

**`/usr/bin/python3` on this machine is 3.9.6**, which is the ticket's own
platform. So the next phase can run the real script on the real interpreter
rather than simulating one, and the acceptance criterion about being *seen red*
has a genuine article behind it.

**Every shipped script compiles under 3.9.** `python3 -m py_compile` over `git ls-files
'*.py'` at 3.9.6 fails on exactly one file, and it is a test. So no shipped
script carries 3.10+ *syntax*, which is what makes it safe to put the guard
after the import block instead of after `import sys` — and that matters,
because `ruff.toml` selects `E4`, so code between imports would make every
later import an E402 failure.

**The floor number cannot be imported without still being typed.** The plugin
cache does ship `.github/scripts/`, so the import would work; the argument
against it is not reachability. It is that a fallback-safe read has to name a
floor in its `except` branch, so the second spelling survives the import
anyway — there is no version of the read that removes the second number, which
is what settles the question the handoff left open. The repository already
answers *one number, several carriers* with a test, twice, for this same
number.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
