<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A meter says what each agent's startup payload is made of, and what it
  costs.** `payload-meter`, on PATH beside `session-cost`, reads every
  `agents/*.md`, resolves its `skills:` list to files, and reports the
  definition, each injected `SKILL.md` and the two `CLAUDE.md` files the
  harness adds, in bytes, characters and tokens, per file and in total;
  `--sections` splits each file at its headings, `--json` writes the same as
  data, `--baseline <run.json>` prints the delta against an earlier run, and
  `--calibrate <main transcript>` reads the measured prefix of every agent
  that transcript spawned. **Every token figure carries a basis** —
  `measured (<transcript>)` where it came from a spawn's first `usage`
  block, `estimated (<ratio> B/token, from <agent>)` otherwise — because
  bytes do not track tokens at one ratio: the three agents measured at 2.87,
  3.41 and 3.44 B/token over the bytes their spawns read. Two things the
  measuring found that the issue had not. A payload IS cached across spawns
  of one agent for five minutes, and is re-written on every spawn further
  apart than that — which in a review chain is every one, so the cost stands
  and the sentence is narrower than it was. And a skill name resolves to
  `~/.claude/skills/<name>/SKILL.md` when the user has one, shadowing the
  plugin's; the meter reports the tree's file and says on the row what the
  spawn read instead. A spawn read the tree as it stood when it was made, so
  calibrating against a transcript after the tree changed keeps the earlier
  run's ratio, labels the agent estimated and says to take a spawn after the
  change. (#292)
- **A section written for the orchestrator no longer rides every `smith`
  spawn, and a test keeps it out.** A heading prefixed `Orchestrator:` marks
  a section addressed to the session that spawns agents, and
  `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` fails
  when such a heading sits in any file an agent's `skills:` list injects, or
  when an `orchestration.md` is itself listed. The `implement` skill splits
  the way `code-review` already had: its Bootstrap, its parity setup and the
  whole routing question — three axes, one `multiSelect` question, one
  `routing.md` — move to `skills/implement/orchestration.md`, headings and
  text unchanged, and `skills/implement/SKILL.md` opens with the pointer
  that sends an orchestrator there. What stays in the implementer's half is
  the per-command waiver, because the implementer is who types the
  command. Measured on this tree with no new spawn: 13,727 bytes left the
  smith's payload, an estimated 4,783 tokens at the 2.87 B/token its spawn
  paid; the `CLAUDE.md` pair grew 265 bytes (an estimated 92) for the
  Bootstrap pointer and a comment, so the smith's payload is 13,462 bytes
  and an estimated 4,691 tokens smaller, summed over its files. The rider
  that asked for an arm to be named in one sentence is answered — the
  sentence names the PARITY arm and a migration repository — and deleted.
  (#292)
- **The `CLAUDE.md` block has one source, and what `/specseal:update`
  shows you is a diff against it.** `templates/claude-md-block.md` is the
  block; `install.sh` reads it from there, `.github/scripts/claude_block.py
  --write` regenerates the copy inside this repository's `CLAUDE.md` and
  `--check` fails a pull request where the two differ, so the copy the
  installer used to read and the copy a contributor sees cannot drift again
  (they had, by one sentence). One sentence of the block changed with it —
  a fresh repository is sent to *the Bootstrap section of
  `skills/implement/orchestration.md`* — so every installed block shows
  that one-line diff at the next `/specseal:update`, against the template
  rather than against a `CLAUDE.md`. (#292)
