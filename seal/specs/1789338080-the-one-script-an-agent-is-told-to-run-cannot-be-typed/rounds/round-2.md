# 1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed — review round 2

| Field | Value |
|---|---|
| Target SHA | 59dcffe |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 388 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 8 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round. Target is the diff of round 1's fixes — `246c65b..59dcffe`, three commits — and not the branch, because everything before `246c65b` had already been reviewed. Round 1's record was committed and its seven verdicts inherited; the job was the answers rather than new findings.

One surface in that diff was named exempt from that rule and handed over as a finding surface instead: `test_a_one_word_command_name_is_not_a_locator` and the change to `reachable` it pins, because a unit the fixes created has been reviewed by nobody. The round was asked to judge the hyphen guard rather than only whether it closes 🟡 1 — specifically what it does to a script whose command name legitimately has no hyphen but which a document does reach by path, and whether the guard can make an unreachable document read as covered from the other direction.

Three things that happened after the fix commit were handed over as facts rather than left to rediscover: `survivor-check` exiting 1 with three places still carrying the invoker-count claim, all corrected in `9a8f4fd`; the fourth copy at `plan.md:82` that `survivor-check` did not report because the corrected wording fell under its phrase threshold, corrected in `59dcffe`; and the invoker count itself having moved twice, from the reviewer's three to the fix pass's five with a mechanism named for each. The round was told to check the five rather than accept them, because two corrections in a row on one number is where a third error hides.

One number in round 1's own report was named as already wrong: it said eight of the twelve wrapper pairs have nobody asserting the executable bit, the fix pass measured five, and the round was asked to verify the residue of four the fix pass named.

What the orchestrator had already executed at `59dcffe`, handed over so the round would not repeat it: six modules — the pin plus `test_the_rules_have_one_owner.py`, `test_docs_line_wrap.py`, `test_the_record_is_generated.py`, `test_a_rider_reaches_its_file.py` and `test_one_word_one_meaning.py` — 249 passed, 8 skipped, exit 0 at `5a8f6ac`; `survivor-check --range 246c65b..HEAD` exit 0; and a probe of `reachable` for `skills/implement/scripts/seal.py` showing the guard false for the three documents that never name it and false for a locator-free synthetic line, true for a line carrying the path.

The broad gate was withheld by name as the sealer's single act after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The locator rule cannot fail for `seal.py` | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:143` | answered | Closed. **Executed** 2026-09-14 at `59dcffe`: `reachable` is false for `seal.py` against a locator-free line and true against the path. The new case is in the file and green |
| 🟡 2 | The class pin asserts the file and the twin and not the executable bit | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:231` | answered | Closed. **Executed** 2026-09-14: `chmod 644` on `bin/round-record` in a clone takes the module from exit 0 to `1 failed, 29 passed` naming the executable bit, and restoring the mode returns exit 0 — §15 for this assertion, which nothing in the tree had recorded |
| 🟡 3 | `NO_WRAPPER` claimed *invoked in none of them* where *followed by a flag* is what is asserted | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | answered | Closed. **Read** 2026-09-14: the reason now says *shown with a flag in none of them* and names `templates/config.md`. The user-facing half of the finding is `spec.md` §Out's standing refusal, not an omission |
| 🟡 4 | `agents/warden.md` named the generator 48 lines before it said where it is | `agents/warden.md:138` | answered | Closed. **Executed** 2026-09-14: the file's `round_record.py` mentions are at 138, 184, 292, 352 and 381, and the path now sits at 140, inside the first mention's own sentence (a second path was already at 188). `test_the_rules_have_one_owner.py` and `test_docs_line_wrap.py` were green at `5a8f6ac`, so the pinned phrase survived whole |
| 🟡 5 | *The generator both rows name* — one row names it | `skills/implement/SKILL.md:521` | answered | Closed. **Read** 2026-09-14: the line reads *The generator that row names* |
| ⬜ 6 | *All three places that DO invoke it* undercounts | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | answered | Closed. **Executed** 2026-09-14: all five verified individually — three by hand, `broad_gate.py:577` as a subprocess, `round_record.py:245` as a module load. The class of copies is four; I swept the work item for the claim in any wording and found no fifth |
| ⬜ 7 | Eleven `seal/ledger.md` rows re-stamped with unmoved `Checked` dates | `seal/ledger.md` | answered | Unchanged by this diff; the deferral to #387 stands as round 1 left it |
| 🟡 8 | The locator failure message names a repair that does not work for a one-word command, and the comment beside the guard calls a wrapped script *reachable by path only* | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:275` · `:142` | open | **Executed** 2026-09-14: `reachable` is false for `seal`, for `` `seal --record <item>` `` and for `` `seal` `` in prose, while the message the case prints offers the command as an accepted form. `bin/seal` and `bin/seal.cmd` both ship, so *reachable by path only* is false. `plan.md` §*Failure scenario* claims the message names both accepted forms |
| 🟡 9 | The hyphen is not what separates a command from prose, and `agents/warden.md:247` already carries `broad-gate` as an ordinary compound | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:143` | open | **Executed** 2026-09-14, every wrapped script against all 43 documents: `reachable(agents/warden.md, broad_gate.py)` is true today on the strength of line 247 alone. No case is wrong because that file does not name the script — which is what round 1 said about `seal.py`. Fix or justify: I measured the obvious alternative reader and it is either too loose or reds `skills/code-review/orchestration.md` for `evidence_check.py` |
| ⬜ 10 | The executable-bit residue is seven, not the four the handover named | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:231` | open | **Executed** 2026-09-14 over all twelve `bin/` pairs and every exec-bit assertion in `tests/`: `seal`, `survivor-check` and `test` are also unasserted. The new assertion newly covers exactly one wrapper, `session-cost`. Not a defect of the pin — the case skips any script no shipped document names, and that skip is its design |
| ⬜ 11 | *Every place that invokes it* reads as a closed list and omits at least twelve test modules that load it by full path | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | open | **Executed** 2026-09-14: `tests/test_the_reopening_is_one.py:30`, `tests/test_chain_check_at_the_pull_request.py:24`, `tests/test_the_record_is_generated.py:35` and nine more build the same path. The conclusion holds harder, not less; the enumeration needs a bound |
| ⬜ 12 | The correction note sits inside the *Alternatives considered* table and orphans its last row | `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/plan.md:83` | open | **Read** 2026-09-14: line 82 is a row, 83 blank, 84–93 the comment, 94 blank, 95 the last row. A table ends at the first blank line, so line 95 renders as literal pipes. Under `seal/specs/`, so a correction rather than a fix to commission |

## Paste-ready fixes

```python
    # A command name with no hyphen in it cannot be told from ordinary
    # English -- `seal.py` answers to `seal`, and this repository's prose is
    # made of that word -- so this reader does not take the bare form as a
    # locator for it. The command is real and `bin/seal` ships; what is
    # missing is a way to tell the command from the sentence, so for those
    # scripts the path is the form that counts.
```
```python
    document, script = pair
    command, text = command_name(script), read(os.path.join(ROOT, document))
    forms = (
        f"the path `{script}`. `{command}` has no hyphen in it, so this rule "
        "does not read the bare command as a locator -- see `reachable`"
        if "-" not in command
        else f"either reachable form: the command `{command}`, or the path "
        f"`{script}`"
    )
    assert reachable(text, script), (
        f"{document} names {os.path.basename(script)} and never says where it "
        f"is. A reader who goes looking finds nothing, which is #318. Add "
        f"{forms}, once"
    )
```
```python
    # The hyphen is a bound and not a rule: a hyphenated command reads as an
    # ordinary compound in prose too, and `agents/warden.md:247` writes
    # `broad-gate` that way today. That file names no script, so no case is
    # wrong -- but the day it names `broad_gate.py`, this reader calls it
    # covered on the strength of that sentence. Measured 2026-09-14: a reader
    # that accepts the bare command only where something follows it either
    # passes the same prose or turns `skills/code-review/orchestration.md`
    # red for `evidence_check.py`, so the bound stays and is written down.
```
```python
        "Every place outside `tests/` that invokes it carries its full path "
        "-- `.github/workflows/hygiene.yml`, `templates/hygiene.yml` and "
        "`docs/release-checklist.md` by hand, and "
        "`skills/verify/scripts/broad_gate.py` and this skill's own "
        "`round_record.py` in code; the test modules that load it build the "
        "same path -- so it is reachable everywhere it is reached. "
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_document_that_names_a_script_says_how_to_reach_it.py -q` in a clone at `59dcffe` | exit 0, 30 passed, 8 skipped |
| the same module with `bin/round-record` chmod'd to `644`, then restored | `1 failed, 29 passed, 8 skipped`, exit 1, the failure naming the executable bit; exit 0 again after restoring `0755` — §15 for the assertion 🟡 2 commissioned |
| every `bin/` pair cross-referenced against every executable-bit assertion in `tests/` | five asserted, seven not: `arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test`. The new assertion adds exactly one, `session-cost` |
| `reachable` for `skills/implement/scripts/seal.py` against the command, the command with a flag, the bare word, and the path | false, false, false, true — and the failure message the case prints offers the command as an accepted form |
| every wrapped script against all 43 shipped documents, for the command token present with no path | `broad-gate` in nine documents, `evidence-check` in eight, `unverified-check` in four, `survivor-check` in three, `arm-check` and `deferral-check` in one. `agents/warden.md:247` carries `broad-gate` as prose |
| an alternative reader accepting the bare command only where something follows it, over the thirteen live pairs | widened it still passes *the seal after the rounds*; narrowed to a flag alone it reds `skills/code-review/orchestration.md` for `evidence_check.py`. Not proposable |
| the five `chain_check.py` invokers, each opened | `broad_gate.py:577` runs it as a subprocess from the path at `:130`; `round_record.py:245` loads it as a module from the path at `:207`; three carry it by hand. All five carry the full path |
| the work item swept for the invoker claim in any wording | four copies, all corrected. No fifth |
| `tests/` swept for executable-bit idioms other than `os.access` | none guarding a `bin/` pair |
| the broad gate — the full suite, the repository-wide lint, the typecheck | not yet. It is the sealer's single act under `skills/agent-contract/SKILL.md` §2 and no segment in this round has taken it |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 7 — eleven `seal/ledger.md` rows re-stamped with unmoved `Checked` dates | #387, as round 1 deferred it | the repository owner |
