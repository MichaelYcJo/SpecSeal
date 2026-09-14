# 1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed — review round 3

| Field | Value |
|---|---|
| Target SHA | 0d2066d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 388 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last round of the run, and told so at the spawn as a fact about the chain rather than a hope about its findings: round 1 met the floor and round 2 closed on a fix, so the reopening the chain allows was spent and this record ends the run whatever it found. The round was told what that costs — anything it opened would end the run `capped`, with every still-open finding becoming an issue reading `deferred #N` — and told to weigh it by writing each finding so it could be acted on without its author, not by lowering the bar.

Target is the diff of round 2's fixes, `74fb1aa..0d2066d`, four commits. Rounds 1 and 2 had reviewed everything before `74fb1aa`. Both records were committed and their verdicts inherited; the job was the answers rather than new findings.

The exempt surface, handed over as a finding surface because a unit the fixes created has been reviewed by nobody: `test_the_failure_message_offers_a_repair_that_actually_works` and the branched failure message it pins. The round was asked three specific things about it — whether the case can pass while the message is wrong, whether the `README.md` fixture choice holds if that file ever gains one of the strings, and whether the hyphenless arm tells the truth about what `reachable` accepts.

🟡 9 had been answered rather than fixed, and the round was told an answer is a verdict it may disagree with, with the grounds stated and an instruction to re-measure rather than accept them.

One number was named as having been wrong three times already — the wrapper pairs whose executable bit nobody asserts, reported as eight by round 1, four by the first fix pass and seven by round 2. The round was asked to count it once more from the tree and to check that what the ledger row names is what the tree holds.

What the orchestrator had already executed at `5e2c556`, handed over so the round would not repeat it: five modules — the pin plus `test_the_rules_have_one_owner.py`, `test_docs_line_wrap.py`, `test_the_record_is_generated.py` and `test_one_word_one_meaning.py` — 221 passed, 8 skipped, exit 0; `survivor-check --range 74fb1aa..5e2c556` exit 0; and the branched message read directly at its coordinates.

The broad gate was withheld by name as the sealer's single act after this round settles.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 8 | The locator failure message named a repair the guard made impossible | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:294-303` | answered | Closed. **Executed** 2026-09-14 in a clone at `0d2066d`: the message now names the path and says why, and the new case goes red against four separate ways of undoing it — the pre-fix message restored, the branch inverted, the hyphen guard deleted, the explanation dropped. The comment beside the guard no longer calls a wrapped script reachable by path only |
| 🟡 9 | The hyphen is not what separates a command from prose | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:147-160` | answered | The answer stands, re-measured rather than accepted. **Executed** 2026-09-14: 43 shipped documents; six hyphenated commands appear as bare words in documents naming no script (`arm-check` 1, `broad-gate` 9, `deferral-check` 1, `evidence-check` 6, `survivor-check` 3, `unverified-check` 4). **Read** 2026-09-14: `agents/warden.md:247` and `skills/code-review/orchestration.md:442` say what the comment quotes, and `orchestration.md` names `evidence_check.py` at 448-449 with no path, so a flag-demanding reader would red it. The bound is written at the guard and in `overview.md` |
| ⬜ 10 | The executable-bit residue is seven, not four | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:249` | answered | Closed in the tree. **Executed** 2026-09-14, counted from `bin/` before reading round 2's list: twelve pairs, five asserted (`evidence-check`, `deferral-check`, `round-record`, `unverified-check`, `session-cost`), seven not (`arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test`). The pin reaches exactly `evidence-check`, `round-record` and `session-cost`, so *newly covers exactly one* is right. The ledger row and the memo name the same seven. See finding 13 for where the old count survives |
| ⬜ 11 | *Every place that invokes it* read as a closed list | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:73-79` | answered | Closed. **Executed** 2026-09-14, walking the tree outside `tests/` and `seal/`: five invocations, all accounted for — `.github/workflows/hygiene.yml:191`, `templates/hygiene.yml:94`, `docs/release-checklist.md:100` by hand, `skills/verify/scripts/broad_gate.py:130` and `skills/code-review/scripts/round_record.py:207` in code. No sixth |
| ⬜ 12 | The correction note orphaned the last row of the alternatives table | `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/plan.md:76-83` | answered | Closed. **Read** 2026-09-14: seven contiguous rows, the comment below them, and it names the row it corrects |
| 🟡 13 | #389 carries the count round 2 discredited, and names three wrappers short | GitHub issue #389, pointed at by `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/overview.md:85` | answered | Repaired outside the tree, which is why the verdict is not `fixed` — the record asks a fix to be a commit somebody can open, and `gh issue edit 389` is not one. #389's title now reads *seven wrapper pairs* and its body names all seven — `arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test` — with a section recording that the count was wrong three times and how each wrong one was taken. The orchestrator measured the residue independently before editing: twelve pairs in `bin/`, five asserted, seven not, and the new pin newly covers exactly one, `session-cost` |
| 🟡 14 | The new case is green when the bad repair is offered in other words | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:361` | deferred #390 | #390 |
| ⬜ 15 | The hyphenless message ends *see `reachable`, once* | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:303` | deferred #390 | #390 |
| ⬜ 16 | `command_name`'s docstring says *all eleven existing pairs* | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:109` | deferred #390 | #390 |
| ⬜ 17 | A line number is used as a coordinate | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:150` · `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/overview.md:96` | answered | `agents/warden.md:247` is a line number inside a code comment and in the closing memo, and it is correct today. `CLAUDE.md` §*A ledger coordinate names content, never a position* governs ledger rows, and the rows this work item wrote carry content anchors. Extending that rule to prose would change what the repository asks of every comment, which is neither this record's to decide nor a fix pass's to make |

## Paste-ready fixes

```
test: seven wrapper pairs carry an executable bit nobody asserts, and the class pin cannot see them
```
```
A `bin/` wrapper pair is a POSIX script and a `.cmd` twin, and the POSIX half
has to carry the executable bit or it resolves on PATH and then refuses with a
permission error. Four modules assert that bit, and each asserts it of its own
wrapper only: `bin/evidence-check`, `bin/deferral-check`, `bin/round-record`
and `bin/unverified-check`.

After #318 planted one more pair and one more assertion, seven of the twelve
have nobody asking: `arm-check`, `broad-gate`, `payload-meter`, `seal`,
`seal-stamp`, `survivor-check` and `test`. The assertion #318 added covers
exactly one that was not already covered, `session-cost`. All seven are
`100755` in the tree today, so nothing is broken. What is missing is anything
that would notice a thirteenth pair committed `100644`, or one of these seven
losing the bit in a move.

The number is recorded as names because it has been wrong three times: round 1
of #318 said eight, its first fix pass said four, and both counted by matching
filenames in any module that mentions them rather than opening each
`os.access` call. Round 2 opened all twelve pairs against every exec-bit
assertion in `tests/` and got seven.
```
```python
    assert f"Add the path `{seal}`." in message, (
        "the message offers something before the path, so a reader meets a "
        "repair the rule rejects before the one it accepts. The bare command "
        f"is not one this rule reads as a locator -- {message}"
    )
```
```python
    forms = (
        f"the path `{script}`, once. `{command}` has no hyphen in it, so this "
        "rule does not read the bare command as a locator -- see `reachable`"
        if "-" not in command
        else f"either reachable form, once: the command `{command}`, or the "
        f"path `{script}`"
    )
    assert reachable(text, script), (
        f"{document} names {os.path.basename(script)} and never says where it "
        f"is. A reader who goes looking finds nothing, which is #318. Add "
        f"{forms}"
    )
```
```python
    Underscores to hyphens, which is what all twelve pairs in `bin/` do and
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_document_that_names_a_script_says_how_to_reach_it.py -q`, in a `git clone --no-local` at `0d2066d` | **exit 0** — 31 passed, 8 skipped |
| Five mutations of the message and the guard, one at a time, the file restored from bytes read before the first write, the case re-run for each | Four **red** (pre-fix message, branch inverted, guard deleted, explanation dropped); one **green and not caught** (the bare command offered in other words) — finding 14 |
| The proposed tightening for finding 14, against today's message and against the missed mutation | **holds** today, **red** against the mutation |
| Wrapper pairs in `bin/` counted against every exec-bit assertion in `tests/` | twelve pairs, five asserted, **seven not**: `arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test`. The pin newly covers exactly one, `session-cost` |
| Every wrapped command matched as a bare word across all shipped documents that name no script | 43 documents; **six** commands, `broad-gate` in **nine** |
| Every `chain_check.py` mention outside `tests/` and `seal/`, read for invocations | **five**, each carrying or building the full path |
| `python3 skills/evidence-check/scripts/evidence_check.py .` | **exit 0** — 1181 ok, 0 drifted, 0 broken; the fragment's 7 rows all resolve, including the two anchors this diff re-stamped |
| `python3 skills/code-review/scripts/survivor_check.py --range 74fb1aa..0d2066d` | **exit 0** — 16 removed sentences, no removed wording still standing |
| `python3 skills/code-review/scripts/chain_check.py --worktree --baseline origin/release/v0.11.4` | **exit 1** on two expected rows — `Broad gate: not yet`, and `Pass` checked beside `Fixes checked by: nobody`. Both are what this round and the sealer close |
| `gh issue view 389` | title and body carry **four**; `seal`, `survivor-check`, `test` absent — finding 13 |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet**, and not this round's. Contract §2 assigns it to the sealer, and nothing in this report needs a fix in the tree, so it is now due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:124` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:211` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` · `templates/config.md:165` | round 1's 🟡 3 — fixed |
| round-1 | `agents/warden.md:138` | round 1's 🟡 4 — fixed |
| round-1 | `skills/implement/SKILL.md:521` | round 1's 🟡 5 — fixed |
| round-1 | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | round 1's ⬜ 6 — fixed |
| round-1 | `seal/ledger.md` | round 1's ⬜ 7 — answered |
| round-2 | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:143` | round 2's 🟡 1 — answered |
| round-2 | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:231` | round 2's 🟡 2 — answered |
| round-2 | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:275` · `:142` | round 2's 🟡 8 — fixed |
| round-2 | `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/plan.md:83` | round 2's ⬜ 12 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Seven `bin/` wrapper pairs have no exec-bit assertion, and closing them needs a case walking `bin/` | #389 | whoever takes #389; finding 13 is that the ticket's own count is wrong |
| Eleven `seal/ledger.md` rows re-stamped with unmoved `Checked` dates | #387 | whoever takes #387; unchanged by this diff, as round 2 left it |
