# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — review round 2

| Field | Value |
|---|---|
| Target SHA | 5ca4077d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 421 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, three shipped lines that still name the framer as the party that asks the routing batch. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round. Its target is the diff of round 1's fixes —
`6edfb71f..5ca4077d` — and its job is the answers: are round 1's five verdicts
actually closed, and are its two ⬜ corrections true.

The six units round 1's record names — three new, three rewritten — are exempt
from that rule and were read as a finding surface.

Four claims the fix pass made about its own work were checked by running them
rather than by reading: that the seal's home closed in **both** directions
where the round had reproduced one, that no shipped document or hook still
hands the routing batch to the framer, that the line it drew in declining a
tool sweep was the right one, and that the `survivor-check` range row's claim
holds against the durable copies rather than against the count.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Three shipped lines still say the routing act is the framer's, which the fix reversed; two of them are the stated grounds for an absence assertion | `tests/test_waiver_decided_at_start.py:148`, `tests/test_waiver_decided_at_start.py:885`, `tests/test_chain_hooks_hardening.py:967` | **fixed** `ef5c607d` | fixed at ef5c607d — all three lines corrected: the comment that is the stated grounds for the absence assertion, the docstring beside it, and the line naming a phase this branch deleted. Then the class rather than the three coordinates — a six-pattern sweep over the whole tree for any wording giving the routing act to the framer. One hit remains and is correct: it is about the file-set table handing `overview.md` to the framer, which is a different act; Read, and reached by a paraphrase sweep rather than by `survivor-check`, which matches removed sentences verbatim. `agents/framer.md` now carries §*You have no interactive phase, and you ask nobody anything*, so line 967 names a phase the diff deleted |
| 🟢 | 🟡 1 of round 1 is closed in both directions, and the restored refusal fires for exactly one state | `skills/code-review/scripts/round_record.py:3825`, `hooks/routing.py:51` | verified | Executed over ten declaration states; both new cases seen red against the disk-based version, and no other case in the module moved |
| 🟢 | The disk fallback for an unreadable declaration is sound — no arm reads either home for one | `skills/code-review/scripts/chain_check.py:1135` | verified | Read: `tracked_declarations` keeps a work item only `if parsed` |
| 🟢 | 🟡 2 is closed and the phrase stands nowhere else | `tests/test_a_moved_rule_leaves_its_definition.py:278` | verified | Executed in the 32-module run, plus a sweep of six trees |
| 🟢 | 🟡 3 is closed, and the round's own mutation now fails two cases in two modules | `tests/test_waiver_decided_at_start.py:905`, `tests/test_review_axes.py:130` | verified | Executed: old paragraph restored in both files, 2 failed; `claude_block.py --check` still exit 0 |
| 🟢 | 🟡 4's documents are closed — no shipped document or hook hands the batch to the framer, and the framer's persona is intact | `agents/framer.md:209`, `skills/implement/orchestration.md:287`, `skills/implement/SKILL.md:399` | verified | Read every hit of a six-phrase sweep; the only survivals are 🟡 1's three lines |
| 🟢 | `test_no_agent_definition_tells_an_agent_to_ask_a_person` refuses the original defect, not a stand-in | `tests/test_waiver_decided_at_start.py:619` | verified | Executed against `git show 6edfb71f:agents/framer.md`: line 232 is refused |
| 🟢 | 🟡 5 is closed | `seal/ledger.md`, `seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md` | verified | Executed: 1269 ok, 0 drifted, 0 broken |
| 🟢 | The `NAME NOT IN TREE` markers are true and the record still states round 1's finding | `rounds/round-1.md:46`, `rounds/round-1-report.md:194`, `:259` | verified | Executed and read: the old name is nowhere in the tree, and the records arm refuses none of 94 names |
| 🟢 | The `survivor-check` claim holds — every survivor stands where the session still performs the act | `skills/implement/orchestration.md:316`, `hooks/commit-review-gate.py:892` | verified | Read each durable copy; `survivor-check` exit 0, all excused |
| 🟢 | No other module sits where `tests/test_review_axes.py` sat | — | verified | 32 modules, 1367 passed, plus a removed-phrase sweep over seven trees |
| ⬜ | `survivors.md` records 28 places; `survivor-check` reports 29 at HEAD | `survivors.md:20` | correction | Executed at HEAD. The range row excuses all of them, so nothing turns on the number |
| ⬜ | A 104-column prose line landed in `agents/smith.md`, which `test_docs_line_wrap.py` lists as a file whose prose does not yet fit | `agents/smith.md:61` | correction | Read. The module's rule is to add a file once its prose fits rather than to raise the limit, and this line moves that file further from fitting |
| ⬜ | The new glob refuses `in one batch` in every `agents/*.md` with a message naming the question batch, and the phrase has a second, legitimate meaning | `tests/test_chain_hooks_hardening.py:814` | correction | Read. `agent-contract` §10 tells every agent to batch independent reads, so a future definition writing *open every coordinate in one batch* goes red under a message about a question nobody asked |
| ❓ | The full suite, the repository-wide lint and the typecheck | — | out of verified scope | `agent-contract` §2 assigns the broad gate to the sealer, and `agents/warden.md` hands it to no reviewer. Answered by the orchestrator, by spawning the sealer |

## Paste-ready fixes

```python
    # `agents/smith.md` used to state the same axis in prose, because it used
    # to ask the question. It does not any more — the act is the SESSION's
    # that spawns the work, because no agent this plugin spawns has
    # `AskUserQuestion` (#419, round 1) — and the vocabulary travels with the
    # act. Asserting the answers here again would put the moved rule back in
    # the definition it left, which is what
    # `tests/test_a_moved_rule_leaves_its_definition.py` exists to refuse.
```
```python
def test_the_smith_carries_its_own_half_and_not_the_questions():
    """The agent file is always in front of the smith; the skill may not be.

    **What its own half IS moved, which is why this case is rewritten rather
    than deleted.** It used to carry the routing question's whole vocabulary,
    because it used to ask it — three axes, the four answers, the path it
    wrote them to. That act is the SESSION's now, not any agent's: round 1
    measured that no agent this plugin spawns has `AskUserQuestion`, so the
    batch went to the party that spawns the work rather than to the framer.
    A definition that keeps the words of an act it no longer performs is a
    session's instruction to perform it.

    What stays is what a smith still does with the answer somebody else
    wrote: run to the pull request without coming back, and name an answerer
    for anything it could not close.
    """
```
```python
    A `no` needs a destination or it becomes a second interruption. The one
    the sentence names is the phase record and the hand-back -- never a route
    back to the framer, which has no interactive phase to route back TO: the
    one moment of human contact belongs to the session that spawns the work,
    before the framer is spawned at all."""
```

## Executed probes

| What was run | Result |
|---|---|
| 12 modules covering the routing documents, the block, the seal and the chain check | 570 passed, exit 0 |
| 20 modules covering the round records, the agent definitions and the identifier rule | 797 passed, 1 skipped, exit 0 |
| `seal_home` over ten declaration states, in a temporary directory | one refusal, nine homes, no crash — the table above |
| `seal_home` reverted to the disk-based version, whole module | exactly 2 failed, 73 passed — both new cases, nothing else |
| The old three-checkbox paragraph restored in `CLAUDE.md` and `templates/claude-md-block.md` | 2 failed, 54 passed — `test_the_preset_block_carries_it_too` and `test_implement_and_the_preset_block_do_not_drift` |
| `claude_block.py --check` under the same mutation | exit 0 — the command holds neither copy against the question |
| The draft early return removed from `direct_seal` | 1 failed — `test_a_direct_declaration_with_no_seal_is_SILENT_on_a_draft` |
| `git show 6edfb71f:agents/framer.md` against the new agent-definition case | line 232 refused — the case catches the original defect |
| `bin/evidence-check --strict .` | exit 0 — 1269 ok, 0 drifted, 0 broken; records arm 94 names, 0 refused |
| `bin/survivor-check --range 6edfb71f..HEAD --exempt <this work item>/survivors.md` | exit 0 — 29 survivors, every one excused by the range row |
| Removed-phrase sweep over `tests/ docs/ skills/ agents/ templates/ hooks/ .github/` | no module asserts a deleted phrase; three paraphrases found, which are 🟡 1 |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet** — not run in this round, and not this agent's to run. It comes due now: spawn the sealer |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:3843` | round 1's 🟡 1 — fixed |
| round-1 | `agents/smith.md:113`, `tests/test_a_moved_rule_leaves_its_definition.py:266` | round 1's 🟡 2 — fixed |
| round-1 | `templates/claude-md-block.md:16`, `tests/test_waiver_decided_at_start.py:841` | round 1's 🟡 3 — fixed |
| round-1 | `agents/framer.md:228`, `skills/implement/orchestration.md:286` | round 1's 🟡 4 — fixed |
| round-1 | `seal/ledger.md`, `skills/evidence-check/scripts/evidence_check.py:1577` | round 1's 🟡 5 — fixed |
| round-1 | `tests/test_chain_check_at_the_pull_request.py:658` | round 1's ⬜ — correction |
| round-1 | `spec.md:392`, `plan.md:183` | round 1's ⬜ — correction |
| round-1 | `skills/code-review/scripts/chain_check.py:3270` | round 1's 🟢 — verified |
| round-1 | `hooks/routing.py:164` | round 1's 🟢 — verified |
| round-1 | `templates/claude-md-block.md`, `CLAUDE.md` | round 1's 🟢 — verified |
| round-1 | `skills/code-review/scripts/chain_check.py:696` | round 1's 🟢 — verified |
| round-1 | `tests/test_waiver_decided_at_start.py:147`, `:696`, `:815`, `tests/test_chain_hooks_hardening.py:789`, `:969` | round 1's 🟢 — verified |
| round-1 | `skills/code-review/scripts/chain_check.py:1638` | round 1's 🟢 — verified |
| round-1 | — | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A sweep over `agents/*.md` for every tool an agent cannot reach | already deferred by `overview.md` §*Not done* as the third ticket, on the grounds that a per-agent tool inventory is mechanism | the repository owner, at the ticket |
| The `Checked` column records no re-read, so `--reverify` cannot report the half that was skipped | already deferred by round 1, to `skills/evidence-check/scripts/evidence_check.py`'s standing `# RIDER:` and #120 | the repository owner |
| A durable record that a person chose `no work item` | already deferred by `overview.md` §*Not done* | the repository owner, at the ticket |
| Promoting the approval-line notice to a refusal | already deferred by `overview.md` §*Not done* | the repository owner, after two or three releases carry the notice |
