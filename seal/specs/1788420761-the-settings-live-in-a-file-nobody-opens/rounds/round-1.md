# the-settings-live-in-a-file-nobody-opens — review round 1

<!-- The first round on #105, reviewed on one branch with #106 because the
failure that matters is the two disagreeing. This record carries #105's
findings. Target: the whole branch from 022e466. Written by the review
orchestrator, which implemented this work item — the routing says why, and the
round was a fresh warden reading it. -->

| Field | Value |
|---|---|
| Target SHA | the whole branch from its base 022e466, reviewed at 9a28262 |
| PR | none yet |
| Broad gate | not yet — the shared branch had 🔴 open |
| Fixes checked by | round-2 |
| Contract changes | none — no unit changed |
| New units | none; two existing assertions were replaced |
| Needs a fix | yes — 🟡 8 (two assertions are satisfied by words the file has for another reason), 🟡 9 (the template-copy branch cannot fire in any repository that has set its mode) |

- [ ] Pass

## What this round was asked to attack

Whether the skill **routes rather than reimplements** — that it spells no move
of its own and that everything it tells a person about the mode is what `seal
mode` actually prints, checked by running the command. And which of its
assertions are satisfied by a substring that would still be there if the claim
were false.

## The claim held

The reviewer ran `seal mode` through shared, the documented rollback, local
and `--check` in a scratch repository, and reports every side effect and the
output format matching what the skill says — including that `seal mode shared`
prints the one-way-door warning before acting, which the skill also carries.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 8 | two assertions pass on words the file has for another reason. `assert "absent" in text or "not carry" in text` and `assert "default" in text` are both satisfied by the file's opening paragraph, so deleting the instruction they were written to pin left them green. And `assert "mv " not in text` reads one literal — a rewrite using `cp -a` and a delete stayed green, and that assertion is the one the file's own docstring calls *the one thing worth stating twice* | `tests/test_the_settings_have_a_front_door.py` | fixed at 2b9f43b — both assert the instruction, and the move one asserts the sentence that forbids doing it by hand | reviewer ran seven mutations of the skill: five red, these two green |
| 🟡 9 | the skill copies `templates/config.md` when the file does not exist. After `seal mode`, it always exists — as a stub carrying only `Mode` and a comment — so the copy branch cannot fire in any repository that has set its mode, and a language row lands in a file with no documentation beside it | `skills/config/SKILL.md` | fixed at 2b9f43b — the condition is a missing language ROW rather than a missing file, and the fix takes the row *and its section* | reviewer ran `seal mode shared` in a scratch repository and read the file it wrote |
| 🟢 10 | the skill spells no move of its own, and `seal mode`'s output matches what it describes | — | pass | reviewer executed the whole sequence |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `seal mode` shared → rollback → local → `--check` in a scratch repository | four side effects, the rollback, and the output format all as the skill says |
| reviewer: seven skill mutations against 124 cases | five red, two green — 🟡 8 |
| reviewer: the file `seal mode shared` writes when there is none | a stub with `Mode` and a comment, no language row and no documentation — 🟡 9 |
| orchestrator: the two replaced assertions, each against the mutation that had survived | both redden |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | 1630 passed · 1 skipped; clean; 455 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| — | none; this is the first round | — |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the bootstrap should route its questions through this skill rather than asking its own | `questions.md` Q2 | the repository owner |
