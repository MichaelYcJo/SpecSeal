# 1790381329-the-deferred-sentences-and-pins — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 1e6cca3e |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#616. The round's case appended to
`test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points`, using
`%CD%` itself, seen red with `value`'s two branches swapped, and that case's
docstring clause corrected. The docstring class from spec.md's #616 table:
`as_cmd_expands` (the round's sentence, plus the defined-`CD`-wins
correction), `handed_to_shell`'s docstring and comment, `templates/config.md`
§*Broad gate* and its pinned needle, seen red with the old sentence. Where
`cmd.exe` resumes after an undefined name stays unverified (Q2).

## What this phase found

- **The frame holds, with one twin more and one pin more.**
  - The twin: the loop comment inside the variable case, *`CD` is computed
    by cmd.exe and is in no environment*, is the same false clause as the
    docstring's. It now says the case deletes `CD` first.
  - The pin: `templates/config.md` now tells the person typing a row that
    a substring or substitution keeps its `/`. That is a rendered statement
    of behaviour (contract §14), so the variable case gains a row,
    `%SPECSEAL_PROBE_TREE:~0,500%/bin/test -q` handed over as written
    although the variable names the tree.
- **The enumeration and its judgments.** Searched over `docs/ skills/
  agents/ templates/ hooks/ .github/ README.md README.ko.md CONTRIBUTING.md`:
  *the way `cmd`*, *as `cmd.exe` expands*, *expanded the same way*, *in no
  environment*, *computes*, *`cmd /c` replaces/leaves/does*, *`%CD%`*,
  *`__CD__`*, *`%VAR%`*, *`%NAME%`*, *expandvars*, Korean *`cmd.exe` 가
  펼치*, *`cmd.exe` 처럼*, *환경 변수 … cmd*. Beyond the four places fixed:
  every *computes* hit is another subject; `broad_gate.py#quoted_path`'s
  *What double quotes do NOT stop is `%VAR%` expansion* is true and claims
  no model; `templates/config.md:216`'s *`%VAR%` … reach the shell as
  written* is about arguments; `CHANGELOG.md`'s 0.15.3 entry is a released
  section and is not rewritten.
- **The model, executed rather than read.** `as_cmd_expands` run directly:
  `%X:~0,200%` and `%X:a=b%` come back as written, and `%UNDEF%Y%CD%` comes
  back as `%UNDEF%Y<dir>`, resuming after the undefined name's closing `%`.
  The docstring says that much of its own behaviour and claims nothing of
  `cmd.exe`'s there.
- **Seen red (§15).** Each file restored from a copy kept before the
  mutation:
  - the defined-`CD` assertion, with the environment lookup moved after the
    two computed names: `%CD%\bin\test -q` handed over;
  - the substring row, with the name cut at its `:` before the lookup;
  - the reader case, with the old config sentence restored:
    `test_the_template_says_which_positions_are_rewritten` failed.
- **Rows drifted.** On `templates/config.md` §*Broad gate* and the whole
  file (0.5.0 S8, 0.10.0 S4, 0.12.0 ×3), `handed_to_shell` (0.15.3 A1, A2)
  and the reader case: each has a dated `Re-read` note. **Two 0.15.4 S1 rows
  are corrected in place with `Corrected 2026-09-26` notes.** One said *any
  `%NAME%`* was expanded and gave `%CD%` the row's directory
  unconditionally. The other quoted the old config sentence. C5 in the
  fragment carries the precedence, the substring bound and the docstrings.
- **Verified by (executed, 2026-09-26):** `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`
  and `tests/test_docs_line_wrap.py`, 130 passed, 1 skipped (the
  real-platform case, which runs only on Windows). `evidence-check .`: 0
  drifted, 0 broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *`CD` and `__CD__` are in no environment* (`as_cmd_expands`) and *which `cmd.exe` computes and no environment holds* (the case's docstring) | nowhere: both were false once `CD` is defined; the docstrings now say a defined one wins |
| *expanded the way `cmd.exe` expands it* / *expanded the same way* (`handed_to_shell`) | a pointer to `as_cmd_expands`' docstring, which states what is modelled |
