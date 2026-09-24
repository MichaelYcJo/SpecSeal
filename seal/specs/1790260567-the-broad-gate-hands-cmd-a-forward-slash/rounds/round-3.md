# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — review round 3

| Field | Value |
|---|---|
| Target SHA | 5732e9af3482f9cee0d291088458a8132c6be9e0 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 595 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 of work item 1790260567 is the last, verifying round: the diff of round 2's fixes, 1cbae560..473892da, at 5732e9af. Round 2 closed on a fix and spent the one reopening, so this record ends the run.

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/conftest.py:324` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1375` | round 1's 🟡 2 — fixed |
| round-1 | `templates/config.md:201` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/releases/0.10.0.md:62` | round 1's ⬜ 4 — answered |
| round-1 | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:150` | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:1204` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1236` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1922` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.10.0.md` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | round 1's ❓ — out of verified scope |
| round-2 | `skills/verify/scripts/broad_gate.py:1298` | round 2's 🟡 1 — fixed |
| round-2 | `seal/releases/0.12.0.md:109` | round 2's ⬜ 2 — answered |
| round-2 | PR #595 body | round 2's ⬜ 3 — answered |
| round-2 | `tests/conftest.py:341` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:114` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:157` | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.5.0.md:107` | round 2's 🟢 — verified |
| round-2 | `tests/conftest.py:335` | round 2's 🟢 — verified |
| round-2 | `skills/verify/scripts/broad_gate.py:1434` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `/` written straight after a program other than a `cmd.exe` built-in is still rewritten, so such a row stops running on `cmd.exe` (the behaviour half of round 2's finding 1) | #596, milestone `backlog: gates & hooks` | the maintainer who triages that milestone; already deferred in round 2's fix pass |
