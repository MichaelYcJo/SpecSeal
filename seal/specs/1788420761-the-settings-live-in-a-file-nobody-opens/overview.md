# The settings live in a file nobody opens — overview

## Rung

**A skill's instructions.** One markdown file a person invokes by name, plus a
line in the bootstrap and a row in each README's cheat sheet. Nothing here
runs; the one thing that does — moving a folder — is `seal mode`, which #104
built and this routes to.

## What was verified

**Executed** — `tests/test_the_settings_have_a_front_door.py`, the full
suite, `ruff check .`, `ruff format --check .`, `evidence_check.py --strict .`.

**Read** — nothing load-bearing. Every claim about what the skill says is
asserted by a case that reads it as text.

## Not verified

| Item | Who must answer |
|---|---|
| Whether a session invoking the skill actually routes rather than editing the mode row itself. The instruction says so and a case asserts the instruction; what a model does with it is not checkable here | the repository owner, on the first run against a real repository |
| Whether the bootstrap should call this skill instead of asking its own questions. It cannot today — the bootstrap asks before there is a root to write into. Both name the same rows and a case asserts it | the repository owner, as a later change |
| The full suite, `ruff check .` and a repository-wide format check | the review orchestrator's broad gate, once the rounds settle |

## Fed back into the spec

Nothing. The design came out of a conversation with the owner and did not move
while it was being written.
