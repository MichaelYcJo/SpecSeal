# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — review round 3 report

Verifying round, and the last: round 2 closed on a fix and spent the one
reopening. Target SHA `5732e9af`; target diff `1cbae560..473892da` (round 2's
fixes, three commits after the pipe repair), read in a `git clone --no-local`
at `5732e9af` under the session scratchpad. Nothing was written in the
worktree except this file.

## What round 2's verdicts come to

- **Round 2's finding 1 (a non-builtin's switch) is closed as it was
  commissioned.** Round 2's paste-ready fixes were documentation, and every
  one landed: `templates/config.md:207` states that a `/` straight after
  any other program's name is rewritten, that `xcopy/e` becomes `xcopy\e`,
  that a blank before the switch avoids it, and that #596 holds the
  behaviour fix. The `command_names_backslashed` docstring
  (`skills/verify/scripts/broad_gate.py:1387`), `spec.md:163`, `plan.md:139`
  and the changelog fragment say the same (read). Executed: each of the
  three new template sentences, cut in turn, turns
  `test_the_template_says_which_positions_are_rewritten` red; and what the
  scan hands over for nine neighbours of the bound (`XCOPY/E`, `@xcopy/e`,
  `xcopy.exe/e`, `timeout/t`, `(xcopy/e …)`, `xcopy /e`, a built-in then
  `xcopy/e` after `&&`, `tools/xcopy /e`, `if 1==1 xcopy/e`) is what the
  documents now say: the switch is rewritten in every spelling with no
  blank, and left as written after a blank or after `if`. The behaviour
  itself is not fixed on this branch. It has a home, #596 (open, milestone
  `backlog: gates & hooks`), and sits in Deferred below rather than here.
- **Round 2's finding 2 (the lost `\|`) is closed.** `1cbae560` puts the
  escaped pipe back in `seal/releases/0.12.0.md:109` and
  `seal/releases/0.5.0.md:107`, one character each, and changes nothing
  else (read, word-level diff). `evidence-check` is clean over the tree
  (executed).
- **Round 2's finding 3 (the PR body) is not closed.** It was recorded as
  `answered` on the grounds that the orchestrator rewrites the body before
  the pull request goes ready. At `5732e9af` the body is unchanged: it
  still lists "a redirection" among the positions that open a command name,
  still says the conftest "removes the GitHub token variables", and still
  carries no A7 answer. It now also misses the bound round 2 documented. The
  pull request is still a draft, so the promise is not yet due; the finding
  is carried as ⬜ 2 below, with the orchestrator as its answerer.

## The unit round 2's fixes created

`test_a_switch_against_another_program_is_rewritten_the_documented_bound_not_the_goal`
(`tests/test_the_gate_hands_cmd_a_path_it_can_run.py:208`) is correct. Its
three rows are exactly what `handed_to_shell` returns with `windows=True`
and `comspec` set to `cmd.exe` (executed, the module passed). With `xcopy`
and `findstr` added to `CMD_BUILTINS` — the shape #596's fix would take —
the two no-blank rows go red and the blank row stays green, which is the
split the case is written to hold (executed, 2 failed and 1 passed). Its
docstring says it pins a bound and will go red on purpose when #596 lands,
so the red #596 produces reads as intended rather than as a regression.
The three new needles in the template case are each load-bearing (the
cutting probe above).

## The ledger

A2's **Corrected 2026-09-25** note makes two execution claims: the template
case red without the new sentences, and the bound case red with `xcopy` and
`findstr` added to `CMD_BUILTINS` (2 red). Both match what this round
executed independently. The five rows re-read against the new template text
(0.5.0 S8, and four rows in 0.12.0 and 0.10.0 citing `## Broad gate`) each
carry a dated `Re-read` note, and `evidence-check` reports 0 drifted and 0
broken. `correction-check` over `1cbae560^..5732e9af` found no merge in the
range, so no correction can have been dropped at one.

## New in this round, from reading

- **⬜ 1 — `plan.md` contradicts itself inside one bullet.** Operational
  impact, `plan.md:135`, still says a row with `/` in its command words
  "could not run on `cmd.exe` at all, so no row that works today changes
  behaviour". Four lines later the correction round 2's fix pass appended
  says a `/` after any other program "runs today, and is rewritten, so that
  row does change: it stops running". The correction was appended and the
  sentence it overturns was left standing, so the bullet asserts both. The
  same shape sits in `spec.md:154`, whose bullet opens "#448's rewrite
  **allows more**" and later says a row is **denied**. The failure
  direction the contract asks for is now both, and the lead sentence names
  one. This is the run's paperwork, so it is a correction and not a fix.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Operational impact keeps "so no row that works today changes behaviour" while the correction appended to the same bullet says a non-builtin's switch row stops running; `spec.md:154` likewise opens with "allows more" over a bullet that now names a deny | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/plan.md:135` | open | read; a record correction under `seal/specs/`, so not counted in `Needs a fix` |
| ⬜ 2 | PR #595's body at `5732e9af` still says a name after a redirection is a command name, still says the conftest removes the token variables, carries no A7 answer, and does not name the documented bound or #596 | PR #595 body | open | read via `gh pr view` at head `5732e9af`; round 2 closed it as `answered` on a promise the orchestrator rewrites the body before ready, and the pull request is still a draft |
| 🟢 | round 2's finding 1 is closed as commissioned — the template, the scan's docstring, `spec.md`, `plan.md` and the changelog fragment name the non-builtin switch bound, the blank that avoids it, and #596 | `templates/config.md:207` | confirmed | executed: each of the three new template sentences cut in turn, the template case red each time; nine neighbouring rows through `handed_to_shell` match the documents; the behaviour is deferred to #596, below |
| 🟢 | round 2's finding 2 is closed — both notes have their escaped pipe back | `seal/releases/0.12.0.md:109` | confirmed | read: `1cbae560`'s word diff restores one character in each row and nothing else; also `seal/releases/0.5.0.md:107`; executed: `evidence-check` 2221 ok |
| 🟢 | The new unit pins the documented bound correctly and can fail | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:208` | verified | executed: the module, 54 passed; with `xcopy` and `findstr` added to `CMD_BUILTINS`, 2 failed and the blank-spelling row passed |
| 🟢 | A2's correction and the five re-read rows are true to the tree | `seal/ledger/1790260567-the-broad-gate-hands-cmd-a-forward-slash.md` | verified | executed: `evidence-check` 2221 ok, 0 drifted, 0 broken; `correction-check` exit 0; A2's two execution claims reproduced independently |
| ❓ | Whether `cmd.exe` ends a command name at `=`, `,` or `;` (carried from round 1) | `skills/verify/scripts/broad_gate.py:1437` | ❓ out of verified scope | no `cmd.exe` here; the `windows-latest` leg or a person on Windows answers it |
| ❓ | Whether `cmd.exe` resolves `bin\probe` to `bin\probe.cmd` (Q1, A4; carried from round 1) | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | ❓ out of verified scope | the `windows-latest` leg answers it at the pull request; it was pending at `5732e9af` when this round looked |

## Paste-ready fixes

```markdown
seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/plan.md,
Operational impact, second bullet — replace "Before this change such a row
could not run on `cmd.exe` at all, so no row that works today changes
behaviour." with:

  Before this change such a row could not run on `cmd.exe` at all, so a
  row whose command words are paths changes only from failing to running.
  A row whose command word carries a switch is the exception below.
```
```markdown
seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md,
Failure directions, first bullet — replace "#448's rewrite **allows more**:
a row that failed on `cmd.exe` now runs." with:

  #448's rewrite **allows more**, and in one spelling **blocks more**: a row
  that failed on `cmd.exe` now runs, and a switch written straight after a
  program other than a built-in (below) no longer does.
```
```markdown
PR #595 body — replace the #448 and #510 bullets' two false clauses, and
add the bound and A7:

- #448: "…the first word after `&&`, `||`, `&`, `|` or a `(` that opens a
  block, are command names. A name after a redirection is left as written."
  Then: "A `/` straight after one of `cmd.exe`'s own commands (`rd/s/q`) is
  left as written; after any other program (`xcopy/e`) it is rewritten and
  that row stops running — write `xcopy /e`. #596 holds the behaviour fix."
- #510: "…points `GH_CONFIG_DIR` at an empty directory, sets `GH_TOKEN` and
  `GH_ENTERPRISE_TOKEN` to a placeholder no server accepts, and removes
  `GITHUB_TOKEN` and `GITHUB_ENTERPRISE_TOKEN`…"
- A7, per fix: the test seen red and how; the failure direction (#448 allows
  more and blocks the non-builtin switch; #510 blocks more); prompt budget 0;
  what ran on macOS and what only `windows-latest` executes.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_gate_hands_cmd_a_path_it_can_run.py -q` in the clone at `5732e9af` | exit 0, 54 passed |
| The new bound case with `xcopy` and `findstr` added to `CMD_BUILTINS`, from a script that restored the bytes it read | exit 1, 2 failed, 1 passed (the blank-spelling row) |
| The template case with each of the three new `## Broad gate` sentences cut in turn, same script | exit 1 each time, 1 failed |
| `handed_to_shell` with `windows=True` over nine rows neighbouring the bound | every no-blank non-builtin switch rewritten; `xcopy /e` and `if 1==1 xcopy/e` left as written; `tools/xcopy /e` gives `tools\xcopy /e` |
| `bin/evidence-check` in the clone | exit 0; 2221 ok, 0 drifted, 0 broken |
| `bin/correction-check --range 1cbae560^..5732e9af` | exit 0; no merge commit in the range |
| `git status --porcelain` in the clone after the mutations | clean |
| The full suite, lint and typecheck (the broad gate) | not yet — nobody has run it on this branch, and it is the sealer's |

Read, not run: the `hygiene` workflow's `release` job is red at `5732e9af`
because `round-2.md` ticks `Pass` beside `Fixes checked by: nobody`. That is
the state a verifying round exists to end, and it should clear once this
round's record names round 3 as the checker. The `windows-latest` pytest leg
was pending.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `/` written straight after a program other than a `cmd.exe` built-in is still rewritten, so such a row stops running on `cmd.exe` (the behaviour half of round 2's finding 1) | #596, milestone `backlog: gates & hooks` | the maintainer who triages that milestone; already deferred in round 2's fix pass |

## Summary for the gate

This round leaves nothing that needs a fix on this branch. Both open items
are corrections: one in the work item's own paperwork, one in the pull
request body the orchestrator owns. With them answered or carried, the
broad gate comes due, and what comes due is the sealer's spawn.

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened: `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/rounds/round-2.md`,
`seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/rounds/round-2-report.md`
(head), `templates/config.md` (§Broad gate), `skills/verify/scripts/broad_gate.py`
(`command_names_backslashed`), `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`
(the bound case and the template case), `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md`
(acceptance and failure directions), `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/plan.md`
(platform table and Operational impact), `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/changelog.md`,
the word diffs of `1cbae560` and `ee085b9b`, the diff `473892da..5732e9af`,
`skills/code-review/scripts/chain_check.py` (verdict vocabulary), and
`CONTRIBUTING.md` §*What a change to a gate must carry*. Read through `gh`:
PR #595's body and checks, issue #596, and the `hygiene` run's failed log.
