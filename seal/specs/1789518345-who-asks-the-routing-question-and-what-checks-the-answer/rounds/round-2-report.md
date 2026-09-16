# Round 2 — the verifying round

Target: `git diff 6edfb71f..HEAD`, the diff of round 1's fixes. HEAD is
`5ca4077d` on `feat/88-399-419-who-asks-the-routing-question-and-what-checks-the-answer`,
confirmed unmoved at the start of this round. Pull request 421, draft.

## What this round found, in one paragraph

All five of round 1's answers hold, and each was checked by running the thing
the fix pass claimed rather than by reading its claim. Two of them are
stronger than the fix record says: the seal's misfiling is closed in both
directions with the refusal firing for exactly one state, and the new
agent-definition case would have caught the original defect rather than only a
second phrasing of it. One thing is open. The fix moved the routing act from
the framer to the session, and **three lines in two shipped test modules still
say the act is the framer's** — which is the same class as 🟡 4, one file layer
down, and `survivors.md` asserts the opposite.

## 🟡 1 — three shipped files still say the routing act is the framer's

**Where.** `tests/test_waiver_decided_at_start.py:148`,
`tests/test_waiver_decided_at_start.py:885`,
`tests/test_chain_hooks_hardening.py:967`.

The first two state the false fact outright. Line 148 is a comment explaining
why the module asserts the routing vocabulary is *absent* from `agents/smith.md`:

    # `agents/smith.md` used to state the same axis in prose, because it used
    # to ask the question. It does not any more — the act is the framer's, and
    # the vocabulary travels with the act.

Line 885 is the docstring of `test_the_smith_carries_its_own_half_and_not_the_questions`
and says *That act is the framer's now*. Line 967 names a phase the fix pass
deleted: *never a route back to the framer, which is the trip the framer's own
phase exists to spend once*. `agents/framer.md` now carries §*You have no
interactive phase, and you ask nobody anything*, so the framer has no phase
that spends an interruption.

**Why it matters.** Both of the first two lines are the stated grounds for an
absence assertion. A session that later wonders whether the routing vocabulary
belongs back in `agents/smith.md` reads these lines to find out where the act
went, and is told the framer. That is the move 🟡 4 exists to prevent, and the
case planted for 🟡 4 would only partly refuse it:
`test_the_framer_asks_nobody_and_writes_no_declaration` refuses the two exact
sentences round 1 removed, so a restoration worded differently reaches
`agents/framer.md` past it.

**Why nothing caught it.** `survivor-check` matches the sentences a range
removed, verbatim. These three are paraphrases written earlier in the branch,
so they were never in the removed set. That is why `survivors.md`'s claim —
*no hook and no shipped document still says the batch is the framer's* — was
true of everything the tool reported and false of the tree.

**What is not wrong.** Every assertion in all three cases is correct and every
one passes. What is wrong is the explanation beside them.

## The five answers

### 🟡 1 of round 1 — the seal's home, both directions

**Closed, and closed wider than the round asked.** `seal_home`
(`skills/code-review/scripts/round_record.py:3825`) now reads the `Review` row
before it looks at the disk. Executed, by calling the function over ten
declaration states:

| Declaration on disk | `rounds/` | Home chosen |
|---|---|---|
| `through the review chain` | empty | **refused** |
| `through the review chain` | one record | `round-1.md` |
| `straight to the PR` | empty | `broad-gate.md` |
| `straight to the PR` | **two records** | `broad-gate.md` |
| unparseable prose | empty | `broad-gate.md` |
| unparseable prose | one record | `round-1.md` |
| `Review` answered, `Branch` row missing | empty | `broad-gate.md` |
| no `routing.md` at all | empty | `broad-gate.md` |
| invalid UTF-8 bytes | empty | `broad-gate.md` |
| backticked `Review` answer | empty | `broad-gate.md` |

Row 4 is the second direction, the one round 1 named without a case. Rows 5
through 10 are the refusal's boundary: nothing crashes, and the refusal fires
in row 1 alone.

**The refusal fires only for the state it is right about, and this is provable
from the vocabulary rather than from the ten rows.** `hooks/routing.py:51`
defines `REVIEW_ANSWERS` as exactly two answers, and `parse` returns `None` for
anything else, so a parsed declaration is `through the review chain` or
`straight to the PR` and the second returns one branch earlier. There is no
third answer for the refusal to catch.

**The fallback to the disk is sound.** Rows 5 through 10 all end in
`broad-gate.md` for a work item whose declaration does not parse, and the
docstring justifies that by saying no arm of `chain_check` walks such a work
item. Verified: `tracked_declarations`
(`skills/code-review/scripts/chain_check.py:1135`) keeps a work item only `if
parsed`, so neither home is read for one that declared nothing readable.

**Seen red, both cases.** Reverting `seal_home` to the disk-based version and
running the module: exactly the two new cases fail and the other 73 pass.

### 🟡 2 — the design gate's second copy

Closed. `wait for an explicit go` is in `MOVED_OUT_OF_SMITH`'s design-gate
entry (`tests/test_a_moved_rule_leaves_its_definition.py:278`), and the phrase
appears nowhere in `tests/`, `skills/`, `agents/`, `docs/`, `templates/` or
`hooks/`. Executed in the passing run below.

### 🟡 3 — the block and its template

Closed, and the round's own mutation was re-run. Restoring the old
three-checkbox paragraph in both `CLAUDE.md` and `templates/claude-md-block.md`
now fails two cases in two modules — `test_the_preset_block_carries_it_too` and
`test_implement_and_the_preset_block_do_not_drift`. `claude_block.py --check`
still exits 0 under the mutation, which confirms round 1's reading of why that
command never held the paragraph: it compares the template with its generated
copy and neither with the question.

### 🟡 4 — who asks the routing batch

Closed in the documents, with one exception, which is 🟡 1 above.

**No shipped document or hook still hands the act to the framer.** Swept for
every phrasing the range removed and for the paraphrases around them:
*Both questions go in one*, *framer's to ask*, *Yours is the one interactive
phase*, *The four writes*, *before you write anything else*, *asks the batch
and writes the declaration*. Every hit is either an absence assertion
(`tests/test_waiver_decided_at_start.py:611`) or the new wording. The only
survivals are the three lines of 🟡 1, which no sweep for a removed sentence
reaches.

**The framer's persona survived intact.** `agents/framer.md` still opens on
gather, judge, plan; the writes table still holds `spec.md`, `plan.md` and
`questions.md` from their own templates; the residue sentence and *You never
answer a person's row for them* are both there. What left is the interactive
phase and the `routing.md` row, which is what had to leave.

**The new case is stronger than its own record claims.** The fix record says
`test_no_agent_definition_tells_an_agent_to_ask_a_person` *went red immediately
on a second phrasing in `agents/smith.md`*. Executed against the real pre-fix
state: `git show 6edfb71f:agents/framer.md` carries `AskUserQuestion` on line
232, on a line that does not say the tool is absent — so the case refuses the
original defect itself, not a stand-in for it.

**The line the fix pass drew on the sweep is the right one.** A per-agent
inventory of reachable tools has to be kept in step with a harness no file in
this repository can read, and a check that silently falls out of step is worse
than no check. Holding one measured name over the `agents/*.md` glob costs
nothing to maintain and catches a fourth definition on the day it lands. The
general sweep belongs in the ticket `overview.md` opens, and it is there.

### 🟡 5 — the ledger's `Checked` dates

Closed. `bin/evidence-check --strict .` exits 0: 1251 rows in `seal/ledger.md`
and 18 in this work item's fragment, 0 drifted and 0 broken, and the records
arm reads 94 names with 0 refused.

## The four things worth checking rather than trusting

### The third module, and whether there is a fourth

**The repair holds and there is no other module in the same position.** The
stated lesson — *a module that reads a file belongs to that file's set* — was
tested two ways.

- **By phrase.** Every sentence this diff removed or reworded was searched for
  across `tests/`, `docs/`, `skills/`, `agents/`, `templates/`, `hooks/` and
  `.github/`. No module asserts the presence of a phrase this diff deleted.
- **By running.** 32 modules — every module that reads one of the six documents
  or the one script this diff changed, plus the record-validating modules,
  since `rounds/round-1.md` itself was edited. 1367 cases passed, 1 skipped,
  both runs exit 0.

`tests/test_review_axes.py` was red for seven phases because both the build and
round 1 picked their narrow set by which files they had edited. The set above
was picked by which files the diff *touches*, which is the lesson applied.

### The declined sweep

Judged above, under 🟡 4. The line is right.

### The `survivor-check` claim

**Verified against the durable copies, not against the count.** Each sentence
the two deleted sections carried was opened where it is supposed to stand:

- *in a command of its own, never batched with the commit*, with the
  `PreToolUse` reasoning — `skills/implement/orchestration.md:316`
- the same rule, in the gate's own two prompts —
  `hooks/commit-review-gate.py:892` and `:937`
- the block and its generated copy — `templates/claude-md-block.md:16` and
  `CLAUDE.md:16`

The session still performs every act those sentences describe, so every one is
correct to leave standing. The range row is a supported shape rather than a
shortcut: `survivor_check.py`'s own header documents it as the second row form,
anchored on the range and the work item.

**The count is 29 at HEAD, not 28.** The fix pass measured before its last
commit. Nothing turns on it — one range row excuses the whole range — but the
record carries a number the tool no longer prints.

### The `NAME NOT IN TREE` markers

**True, and the record still says what round 1 found.** The old case name
appears nowhere in the tree outside the records that quote it, so the marker
states a fact. The three marked lines
(`rounds/round-1.md:46`, `rounds/round-1-report.md:194` and `:259`) keep round
1's finding word for word; the marker is an HTML comment beside the row and
changes nothing the row asserts. The records arm of `evidence-check` reads 94
names and refuses none, which is the marker working.

The renamed case also binds now, which its predecessor did not. Removing the
draft early return from `direct_seal`
(`skills/code-review/scripts/chain_check.py:3445`) fails
`test_a_direct_declaration_with_no_seal_is_SILENT_on_a_draft`; the old case
asserted exit 0 alone and would have stayed green.

## The exempt surface — six cases nobody had reviewed

| Case | Verdict |
|---|---|
| `test_seal_refuses_a_chain_declaration_with_no_round_record` | correct, seen red |
| `test_a_direct_declaration_seals_into_its_own_home_even_with_rounds` | correct, seen red |
| `test_no_agent_definition_tells_an_agent_to_ask_a_person` | correct, and catches the original defect |
| `test_the_framer_asks_nobody_and_writes_no_declaration` | correct; its absence half covers two sentences and not the class, which is why 🟡 1 can reach `agents/framer.md` past it |
| `test_a_direct_declaration_with_no_seal_is_SILENT_on_a_draft` | correct, seen red |
| `test_the_preset_block_carries_it_too` | correct, mutation re-run red |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Three shipped lines still say the routing act is the framer's, which the fix reversed; two of them are the stated grounds for an absence assertion | `tests/test_waiver_decided_at_start.py:148`, `tests/test_waiver_decided_at_start.py:885`, `tests/test_chain_hooks_hardening.py:967` | open | Read, and reached by a paraphrase sweep rather than by `survivor-check`, which matches removed sentences verbatim. `agents/framer.md` now carries §*You have no interactive phase, and you ask nobody anything*, so line 967 names a phase the diff deleted |
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

All runs were made in a `git clone --no-local` of the repository at
`5ca4077d`, in a virtual environment the repository's own runner builds and
reuses. Every mutation was reverted with `git reset --hard` and the clone left
clean; the clone and the probe script are deleted.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A sweep over `agents/*.md` for every tool an agent cannot reach | already deferred by `overview.md` §*Not done* as the third ticket, on the grounds that a per-agent tool inventory is mechanism | the repository owner, at the ticket |
| The `Checked` column records no re-read, so `--reverify` cannot report the half that was skipped | already deferred by round 1, to `skills/evidence-check/scripts/evidence_check.py`'s standing `# RIDER:` and #120 | the repository owner |
| A durable record that a person chose `no work item` | already deferred by `overview.md` §*Not done* | the repository owner, at the ticket |
| Promoting the approval-line notice to a refusal | already deferred by `overview.md` §*Not done* | the repository owner, after two or three releases carry the notice |

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

Needs a fix: yes — 🟡 1, three shipped lines that still name the framer as the
party that asks the routing batch.
Loses a record or crashes: no

## Proof block

Files opened in this round:

- `seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/rounds/round-1.md`, `rounds/round-1-fixes.md`, `rounds/round-1-report.md`, `survivors.md`, `overview.md`, `spec.md`, `plan.md`
- `agents/framer.md`, `agents/smith.md`, `CLAUDE.md`, `templates/claude-md-block.md`, `skills/implement/SKILL.md`, `skills/implement/orchestration.md`
- `skills/code-review/scripts/round_record.py`, `skills/code-review/scripts/chain_check.py`, `skills/code-review/scripts/survivor_check.py`, `hooks/routing.py`, `hooks/commit-review-gate.py`
- `tests/test_waiver_decided_at_start.py`, `tests/test_chain_hooks_hardening.py`, `tests/test_review_axes.py`, `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_chain_check_at_the_pull_request.py`, `tests/test_docs_line_wrap.py`, `tests/test_the_set_a_work_item_always_has.py`
- `bin/test`, `seal/ledger.md`, `seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md`
