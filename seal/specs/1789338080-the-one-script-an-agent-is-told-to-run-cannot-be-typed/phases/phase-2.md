# 1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8dfde46 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Write `bin/round-record` and `bin/round-record.cmd`, modelled on
`bin/survivor-check`, and plant the wrapper-pair case with them. Touch no
document — the respelling of the two typed command forms is phase 3's, behind
the pin that proves it was owed.

Answer Q3 at the top of the phase: is `round-record` free as a bare-word
command, on this machine and in the tree.

## What this phase found

**Q3 is answered and the name is free.** **Executed** 2026-09-14:
`command -v round-record` exits 1, `grep -rn 'round' .claude-plugin/` exits 1,
and `ls bin/ | grep round` exits 1. Nothing on this machine's PATH and nothing
in the plugin manifest answers to the name. The wrapper ships as planned.

**The platform case needed the presence assertions the plan's model already
carries.** Written first without them — the pair is asserted one case up —
it passed against a `bin/` holding neither file, because constructing an argv
touches no filesystem. Green on the tree this work item exists to fix is the
shape `skills/agent-contract/SKILL.md` §15 refuses, so
`test_the_wrapper_pair_is_run_through_the_twin_the_platform_can_execute` now
opens with the two `isfile` assertions its sibling in
`tests/test_the_seal_is_taken_once_by_the_sealer.py` opens with, and the
docstring says why. That is the sibling's shape arrived at by measurement
rather than by copying.

**Two cases, not one, for the command's behaviour.** A wrapper that swallowed
its arguments entirely would still print `usage: round-record` and exit 0,
because that is what argparse does with nothing. So
`test_the_wrapper_passes_a_subcommand_through` runs `new --help` and reads
`--item` out of it.

**`bin/`'s two enumerating cases pick the pair up with no edit.**
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py` reads `bin/` off
the filesystem — `test_every_bin_entry_has_a_windows_twin` and
`test_every_posix_wrapper_resolves_its_own_directory` — so the new pair was
already held to the twin rule and the self-resolving rule before this phase
planted anything. **Executed**: both modules green, exit 0, 165 passed.

**The usage comment was written wrong and corrected against the script.** The
first draft showed `round-record new --item <dir> --round N --report <file>`;
`new` in fact requires `--target`, `--asked` and `--ran-by`, and `--report`
has a default. Read out of `--help` for all three subcommands, and the
wrapper's comment now shows what each one actually takes. No argument, output
or verdict of `round_record.py` was touched.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
