# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a64971d4 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#747, the cut: a pure scanner returning the prefixes of a row for a grammar,
the shell decision factored out of `handed_to_shell`, and parametrised cases
over `spec.md`'s outcome table in both grammars (A7). Verified by the new unit
cases, plus `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, where the
factored decision is read.

## What this phase found

- **The scanner is `row_prefixes(command, cmd_exe)`, and it returns the
  prefixes as strings**, shortest first and the whole row last. The shell
  decision is `cmd_exe_reads(windows, comspec)`; `handed_to_shell` now asks
  it, and phase 3 asks it once for the grammar.
- **Two branches were removed because nothing could hold them**, found by
  mutation rather than by reading. The first draft deduplicated prefixes and
  deduplicated the whole row against them, and a mutation removing either
  survived. Neither can ever fire: a prefix ends before its operator and the
  next one includes that operator, so no two are equal. The `i and` guard in
  front of the redirection check went the same way, replaced by a slice that
  reads `""` at position 0. The tuple `("<", ">")` matters there, because
  `"" in "<>"` is `True`.
- **The first round of mutations found two quote branches unheld**: dropping
  the single-quote skip, and dropping the `pass` that makes `'` and `(`
  inert inside double quotes. Four cases were added for them — a `\` and a
  `"` inside single quotes, and a `'` and a `(` inside double quotes — plus
  an operator before any command.
- **Seen red, executed:** every branch of `row_prefixes` and of
  `cmd_exe_reads` was broken one at a time with `bin/mutation-check` against
  `-k "cut_where or cut_for_is"`. 29 mutations in all; after the four cases
  above every one reported `red`. The cases are also red at `e141980a`,
  where neither function exists, which is the weaker proof and not the one
  relied on.
- **Green, executed:** the 41 cases of the slice, and
  `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` whole, `96 passed, 1
  skipped`, after the factoring.
- **A formatter runs after every edit in this session**, and it removed
  `import ntpath` the moment one edit left the module briefly without a use
  of it. The next run named the `NameError`; it is said here because the
  next edit that moves code between functions meets the same thing.
- **Phase 1's push was the last.** `skills/agent-contract/SKILL.md` §6
  withholds pushing from every agent whatever its file says, and the spawn
  prompt ranks below the contract (§3), so this phase and the ones after it
  are committed and not pushed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `handed_to_shell`'s inline `windows`/`COMSPEC` decision | `broad_gate.py#cmd_exe_reads`, which `handed_to_shell` now calls |
