# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — review round 2

| Field | Value |
|---|---|
| Target SHA | 6fc9bb71 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 412 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 1; finding 2 is fix-or-justify and justifying it means writing the grounds into the two cells. |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round. Its target is the diff of round 1's fixes —
`96c88c9f..6fc9bb71` — and its job is the answers rather than new findings: for
each of round 1's nine verdicts recorded as `fixed`, is it actually closed.

The ten units round 1's record names under `New units` are exempt from that
rule and were treated as a finding surface, because nobody has reviewed them.

Four claims the fix pass made about its own work were checked rather than
trusted: that finding 6's first repair was insufficient and its second holds
where the first did not, that a partition case asserting something false was
removed rather than weakened and left no hole, that adding the gate script to
`SEAL_SWEPT` repaired a second ownerless instance nobody had reported, and that
`rows()` is dead. The round also read the two decisions taken since round 1 —
`questions.md` Q6, and the corrected pull request body.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The case planted for round 1's 🟡 4 reads the whole section, so the clause it pins can be deleted with every case green | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:275` | open | Executed: `#401` deleted from the paragraph — 17 passed; the whole new clause deleted — 17 passed. `#401` stands twice in `## Broad gate`. `agent-contract` §12; round 1's 🟡 7 is the same class, repaired in the sibling module by the same fix pass |
| 🟡 2 | The `&`'s platform hedge reached the message, `overview.md` and the pull request, and not the two cells of the list that owns the form | `templates/config.md:206` and `:225` | open | Read: `:206` says *the shell answers 0*, and `:225` — added by this fix pass — says the command before the `&` is backgrounded and may still be running. Under `cmd.exe` neither is what happens. `CONTRIBUTING.md` §*What a change to a gate must carry*; `agent-contract` §12 |
| 🟢 | Round 1's 🟡 1 — the mid-line `&` is in the allowed list with its cost, and the boundary is pinned | `templates/config.md:225`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:801` | **fixed** `9a52268c` | Executed: widening `not_as_written` to refuse any `&` outside `&&` reddens three of the four parametrised values. Q6 answers the code route and the criterion and the code draw one boundary |
| 🟢 | Round 1's 🟡 2 — the pipe's file-wide cost, and the bootstrap's refusal to propose one | `templates/config.md:224`, `skills/implement/orchestration.md:152` | **fixed** `9a52268c` | Executed: deleting the measurement reddens the pipe case; each of the warning's three needles reddens the new bootstrap case separately |
| 🟢 | Round 1's 🟡 3 — rule 3 is no longer restated and neither carrier copies the lists down | `skills/implement/orchestration.md:144`, `skills/config/SKILL.md:63` | **fixed** `9a52268c` | Read both carriers; the negatives are section-wide, which is the strong direction, and the two positive needles occur once each. A checker for a fourth copy is mechanism a fix pass may not add |
| 🟢 | Round 1's 🟡 4 — the module header names both refusals and the template paragraph no longer argues from the removed sentence | `skills/verify/scripts/broad_gate.py:12-20`, `templates/config.md:173` | **fixed** `9a52268c` | Executed: the header reverted is red. The template half is repaired in the document and its case is 🟡 1 above — the prose is right, the pin is not |
| 🟢 | Round 1's 🟡 5 — the refusal message names `/bin/sh` and `cmd.exe`, and `overview.md` records the claim as unmeasured | `skills/verify/scripts/broad_gate.py:333-341`, `overview.md` §*Not verified* | **fixed** `9a52268c` | Executed: dropping the `cmd.exe` clause reddens the ampersand case. The two cells the fix did not reach are 🟡 2 above |
| 🟢 | Round 1's 🟡 6 — one table's rows, and a row found by its name cell | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66` and `:89` | **fixed** `5d893171` | Executed: the pipe row moved into the refused table, the two reason cells swapped, and each name cell renamed alone — red every time. The second repair holds where the first did not |
| 🟢 | Round 1's 🟡 7 — all three Bootstrap cases bounded | `tests/test_first_setup_asks_once.py:163`, `:230`, `:287` | **fixed** `9a52268c` | Executed: `#151` removed from the decline paragraph alone is red; a candidate source moved out of the bounded slice is red. `paragraph()` raises when its opening is gone, so the decline case cannot pass on a missing heading |
| 🟢 | Round 1's 🟡 8 — the config skill's bullet is bounded and the three forms are asserted | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:349` | **fixed** `9a52268c` | Executed: the clause deleted from `skills/config/SKILL.md` is red |
| 🟢 | Round 1's 🟡 9 — both ownerless instances repaired, and the sweep reaches the file | `skills/verify/scripts/broad_gate.py:251` and `:530`, `tests/test_one_word_one_meaning.py:184` | **fixed** `9a52268c` | Executed: reverting either instance reddens the sweep. No bare instance is left in the file |
| 🟢 | The partition case was removed rather than weakened, and the comment left in its place is true | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:196` | confirmed | Read: `$(…)` is named in both tables and must be. What the case would have caught is caught by the per-table pairing, which is red under the mutation that motivated it |
| 🟢 | `rows()` is removed and nothing calls it | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` | confirmed | Read: the only `rows(` left in the tree is another module's own helper |
| 🟢 | The pull request body now says what the tree says, for findings 2 and 5 | pull request #412 | confirmed | Read the body against the tree: the *Platform* section, the pipe's file-wide cost with its measurement, and *an `&` that is not last* in the legal list |
| ⬜ | Nine `fixed` rows read `fixed at <sha> — at  —`, a doubled preposition and an empty gap | `rounds/round-1.md` | correction | The fix table's third cell opened with ``at `<sha>` —`` and `skills/code-review/scripts/round_record.py:3697` prepends `fixed at <sha> — ` after cutting the commit's code span |
| ⬜ | No `rounds/round-1-fixes.md`; the fix pass's table lives only in a session scratch directory | `rounds/` | correction | 29 such files stand elsewhere in the tree; `skills/code-review/SKILL.md:198` names the convention. Every claim about the fix pass reached this round as prose (`agent-contract` §5) |
| ⬜ | `spec.md`'s allowed list still omits the mid-line `&`, which is round 1's 🟡 1 at the coordinate its grounds cited | `spec.md` §*What is refused, and what stays allowed* | correction | Read: three allowed forms, and the form is in neither of the spec's two lists |
| ⬜ | `questions.md` orders its rows Q1, Q2, Q3, Q4, Q6, Q5 | `questions.md:21` | correction | Q6 was inserted above Q5 rather than after it |
| ⬜ | Round 1's three ledger-prose corrections are done; its S14, fixture and `;`-cost corrections stand | `seal/ledger.md:1885`, `:1942`, `:1943` | correction | Read all three corrected cells against the code they describe. S14's replacement still covers one of four claims, and the other two were correct to leave |

## Paste-ready fixes

```python
def refusal_paragraph():
    """The paragraph that argues a refusal over a prompt, bounded at the blank
    line — not the section.

    Round 2's 🟡 1. `#401` stands twice under `## Broad gate` — once here and
    once in the criterion's closing prose, where it has been since before this
    branch — so a section-wide slice cannot fail by losing it from the
    paragraph the case is named for. Deleting the whole clause left 17 cases
    green."""
    body = broad_gate_section()
    opening = "**An absent row is a refusal, not a default.**"
    assert opening in body, "the refusal paragraph is gone from the template"
    return flat(body[body.index(opening) :].split("\n\n", 1)[0])


def test_the_paragraph_above_the_lists_no_longer_says_it_names_what_to_write():
    """*A refusal that names what to write is answered by the next person to
    read it* was half the stated reason for preferring a refusal to a prompt,
    and the refusal no longer does that. The paragraph sits inside the very
    section this branch rewrote."""
    assert "names what to write is answered" not in flat(broad_gate_section()), (
        "the template still argues from the sentence the message dropped"
    )
    paragraph = refusal_paragraph()
    assert "names whose the row is and where it is answered" in paragraph
    assert "does **not** name a command to write" in paragraph, (
        "the paragraph no longer says what the message stopped doing"
    )
    assert "#401" in paragraph, (
        "the paragraph asserts the change without the report behind it"
    )
```
```markdown
| a trailing `&` that is not part of `&&` | `bin/test -q &` | `/bin/sh` backgrounds the whole line and answers 0 before any check has finished. `cmd.exe` separates two commands instead, so what the gate reads is the second one's status. Two different wrong answers, refused for the same half of the criterion |
```
```markdown
| an `&` anywhere but at the end | the command before it is backgrounded and its status discarded, exactly as a `;` discards one — and unlike a `;`, it may still be running when the gate stamps, writing into the tree the stamp is about. That is `/bin/sh`; `cmd.exe` sequences the two commands instead, so nothing is left running and the status read is the second command's. Telling an operator `&` from a `2>&1` or a quoted `&` needs the shell parser this list exists to avoid, so it stays the row author's own composition. The **trailing** form is refused, because nothing composes after it and the whole line goes to the background |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` over the four modules the fix diff touches, at `6fc9bb71` in a `git clone --no-local` | exit 0, 177 passed |
| Thirteen mutations behind round 1's nine findings, each restored from the original bytes before the next | every named case red; the table above lists which |
| The clause added for round 1's 🟡 4 deleted in full from `templates/config.md` | exit 0, 17 passed — the finding above |
| `#401` replaced in the rewritten paragraph alone, leaving the section's second occurrence | exit 0, 17 passed |
| Each of the bootstrap pipe warning's three needles, separately | exit 1 each — the new case reddens on all three |
| `evidence-check --strict .` in the clone | exit 0 — 1273 ok, 0 drifted, 0 broken |
| `survivor-check --range 96c88c9..6fc9bb7` against this work item's `survivors.md` | exit 0 — 47 sentences removed, 2 survivors, both excused |
| `deferral-check` in the clone | exit 0 — resolves |
| `grep` for the bare ownerless phrase across `skills/verify/scripts/broad_gate.py` | no match |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** `agent-contract` §2 makes it the sealer's one act; no round has run it and this round did not. It comes due when nothing is left open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py#not_as_written` | round 1's 1 — fixed |
| round-1 | `templates/config.md` §*What is refused, and what stays allowed*, the `a pipe` row | round 1's 2 — fixed |
| round-1 | `skills/implement/orchestration.md:145` | round 1's 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:13-17` | round 1's 4 — fixed |
| round-1 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66` | round 1's 6 — fixed |
| round-1 | `tests/test_first_setup_asks_once.py:234` | round 1's 7 — fixed |
| round-1 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:210` | round 1's 8 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:248` | round 1's 9 — fixed |
| round-1 | `seal/ledger.md:1942` | round 1's ⬜ — correction |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:819` | round 1's ⬜ — correction |
| round-1 | `templates/config.md` §*Choosing a value — the criterion*, rule 3 | round 1's ⬜ — correction |
| round-1 | `skills/verify/scripts/broad_gate.py#gate` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `Broad gate` row can ever carry a pipe, and whether `config_rows` should learn to unescape one | `questions.md` Q5, already deferred by the work item, routed to an issue. Round 1's measurement about the rows below is now recorded in Q5's own cell | the repository owner |
| Whether the gate behaves on Windows as the refusal's message says | `overview.md` §*Not verified*, already deferred and rewritten by the fix pass. 🟡 2 above is about two document cells, not about this measurement | the repository owner, at the next `windows-latest` run |
