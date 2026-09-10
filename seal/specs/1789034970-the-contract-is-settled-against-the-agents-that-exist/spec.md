# Feature Specification: the contract is settled against the agents that exist

<!-- seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #120. The last work item of 0.10.0: the two sections of
`skills/agent-contract/SKILL.md` that the fourth agent contradicts are
rewritten against the four agents that exist, and §7 stops being silent about
a probe whose leavings are not a file.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §*How the sections are numbered* | A section number is never reused and never re-ordered. §2, §6 and §7 keep their numbers and are rewritten in place; nothing new is appended |
| `skills/agent-contract/SKILL.md` opening — *nothing here is one agent's own*, *a section that would need a per-role exception is a sign the rule is not universal* | The test this work applies to its own two sentences. A §2 that reads *unless you are the sealer* would fail it; a §2 that says the gate is one act with one owner passes for all four |
| `CLAUDE.md` §*Verification Scope* | Narrow and often, broad once. §2 keeps that; what it stops saying is who takes the broad one |
| `CONTRIBUTING.md` §*Name a module* | Already says *the full suite is the sealer's, run once after the review rounds settle*, and cites §2 as what forbids it to smith and warden. §2 is the last file in the tree that still names the orchestrator |
| `agents/sealer.md` §*The one write, and why it is yours*, §*§2 as it stands, and #120* | The first is the exception §6 prescribes and keeps. The second is the paragraph this work item deletes — its own last line says so |
| `docs/flow.md` §*0.11.0 — the framer*, §*0.10.0 — the agent set* | Settled against four, not five. §6's new sentence is true of any agent including one that does not exist; §2's contradiction is the sealer's alone |
| #120's comment of 2026-09-10 (`smith`'s scope) | `smith`'s §-by-§ scoping is NOT frozen here. What lands instead is the criterion, in `templates/sdd-routing.md`, so the next release measures the `Implementation` row against something |
| #120's comment of 2026-09-10 (§7 and the stray worktree) | Answer: widen the sentence. A probe leaves nothing behind, whatever kind of thing it made |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Every case this work item changes is shown red before it is committed (contract §15), and the reason each pinned phrase moved is written where the pin lives |

## The defect, stated as three sentences that are false today

1. **§2 forbids the broad gate and assigns it to the orchestrator.** Both
   halves are now wrong. `agents/sealer.md` exists and its whole procedure is
   that run, so the prohibition has an agent it must not reach; and
   `CONTRIBUTING.md`, `docs/review-handoff-protocol.md`, `agents/smith.md`,
   `agents/warden.md` and `skills/verify/scripts/broad_gate.py` all name the
   sealer as the owner while §2 still names the orchestrator. §2 is the last
   file in the tree carrying the old owner, and it is the file every agent
   reads first.
2. **§6 says you write no durable record.** Two of four write one — the
   warden's `rounds/round-<n>-report.md`, the sealer's `Broad gate` cell — and
   §6 handles that by carving exceptions elsewhere. A rule with two exceptions
   today and four at five agents is a rule that stops being read.
3. **§7 says a probe is one file, run once, deleted.** A probe that creates a
   git worktree satisfies every word of that and still leaves something
   behind. One did, during #30's review chain: the worktree outlived the
   round and surfaced two work items later, when `git switch` refused a
   branch a worktree already held. The reviewer had followed §7 to the letter.

## Scope

**In.**

1. **§2 rewritten.** The gate becomes one act with one owner rather than a
   prohibition with a default holder. What it must keep: narrow and often
   while you work; the module and the ones it touches at a phase boundary;
   broad once, after the rounds settle; a round is edits already scheduled, so
   a broad run taken before it is spent rather than banked; and the handover
   label — a suite that is simply not mentioned reads as a suite that passed.
   What changes: the owner is named as the sealer rather than the
   orchestrator, and the sentence is put so that the agent the gate belongs to
   is not forbidden its own act. **No per-role exception.** The universal form
   is that the gate is a single act, taken once, and whether it is yours is
   what your own definition says — which is true of all four and of a fifth.
2. **§6 rewritten**, to #120's own proposal: *what you write is named in your
   own definition and nothing else*. The report stays the final output; the
   list that is universal — post nothing, push nothing, open no pull request,
   spawn no agent — stays intact and stays the pinned sentence. What goes is
   the shape where a durable write is an exception: a definition that names a
   write permits it, a definition that is silent permits none. The paragraph
   that says *an exception is one agent's, and it is named in that agent's
   definition — never here* is replaced by the default, because with the new
   sentence there is nothing left to except.
3. **§7 widened.** The `test_tmp_*` file rule stays — it is what the reviewer
   who left the worktree did follow, and it is still the right form for the
   common case. What is added is that the rule is about leavings rather than
   about files: a worktree, a branch, a checkout, a venv is the same act, and
   the probe is not over until it is gone. The story goes in as the sections
   around it carry theirs — this is the repository's convention and it is what
   keeps a rule from being re-litigated by someone who has not paid for it.
4. **`agents/sealer.md`: the window closes.** §*§2 as it stands, and #120* is
   deleted, its own last line having said it would be. §*The one write, and
   why it is yours* stays and is re-pointed at §6 as rewritten: it stops
   reading as *an exception §6 permits to be named* and starts reading as
   *the write §6 says my definition names*. `Everything else §6 withholds
   stays withheld` keeps its meaning under the new sentence and stays.
5. **`agents/warden.md`: two exceptions become two named writes.** The bullet
   §*§6's instances are yours by name, and the record is not the report* is
   the same content under a different rule — what it must stop saying is
   `§6's two exceptions`, because under the rewrite they are not exceptions.
   The distinction it draws between the record and the report is untouched.
6. **`skills/code-review/orchestration.md`: the orchestrator's own sentence.**
   §*No round can run it* reads *§2 reserves the broad gate for you*, and
   under the rewrite §2 reserves it for the sealer. The fix-pass step it
   describes is still the orchestrator's; what changes is the reason given.
   The same file's *The broad gate still runs once, after the rounds settle
   (`agent-contract` §2)* is true as it stands and is not touched.
7. **`templates/sdd-routing.md`: the `Implementation` row gains a criterion.**
   The row asks `smith` · `the session` and has never said how to answer,
   which is why it is answered by habit — and #263 measured what that habit
   costs. The criterion, from #120's comment: *finding out goes to `scribe`;
   writing down stays with the session — unless the expected diff is large
   enough to threaten what the orchestrator still has to hold, which is the
   one case `smith` answers.* It goes in the row's comment block, where the
   rest of that row's guidance already sits, and it is written as a criterion
   rather than as a default so that neither answer becomes the silent one.
8. **The cases.** Every check that pins a sentence this work moves is
   re-pinned in the same commit, with the reason at the pin rather than in a
   commit message: `tests/test_the_agent_contract_holds_the_universal_rules.py`
   (PINS §2, and §7 if its pinned phrase moves),
   `tests/test_broad_gate_rule.py`
   (`test_the_prohibition_itself_has_one_home_and_it_is_the_contract` asserts
   the orchestrator is the owner and is the case that must now assert the
   sealer), and `tests/test_the_seal_is_taken_once_by_the_sealer.py`
   (`test_the_sealer_states_the_contradiction_and_the_ticket_that_settles_it` <!-- NAME NOT IN TREE -->
   pins the window this work closes — it is rewritten to pin that the window
   is closed, not deleted, because a deleted case is a paragraph that can
   come back).

**Out.**

- **Splitting the contract into more than one file.** The owner's answer, in
  the batch before the first edit. The defect is contradiction, not
  irrelevance: §12–§15 are vacuous for the sealer rather than false about it,
  a line drawn at four agents is redrawn when the framer arrives in 0.11.0,
  and a `§N` citation that no longer names one file is a cost every existing
  round record would have to pay retroactively. #120's own body asked for the
  same thing in different words — *the line gets drawn when there is
  something to draw it against* — and one contradicted agent is not yet that.
- **`smith`'s §-by-§ scoping.** #120's first comment asks explicitly that it
  not be frozen here, and three answers are live. What lands is the criterion
  in `templates/sdd-routing.md`, which is what makes the next release able to
  measure rather than to re-argue.
- **A new section.** Nothing here needs a §17. Every change is to a section
  that exists, which is what keeps every `§N` in every round record readable.
- **The payload number.** #292's meter is in the tree and its before-number is
  recorded; this work item shrinks the contract by a little or grows it by a
  little, and either is fine. Trimming was never this ticket's job — that
  reading came from #292's row in `docs/flow.md`, and the owner settled it.

## How we'll know

| Claim | The check |
|---|---|
| §2 no longer contradicts the agent whose one act it describes | `tests/test_broad_gate_rule.py::test_the_prohibition_itself_has_one_home_and_it_is_the_contract` asserts the contract names the sealer, and the old orchestrator sentence is asserted absent |
| §2 still forbids the broad run to the three agents that must not take it | `tests/test_broad_gate_rule.py` keeps its smith and warden cases; `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` keeps its narrow-form cases |
| The rewrite needs no per-role exception | The rewritten §2 and §6 contain no agent name in a conditional — read at review, and pinned by the sentence that states the general form |
| §6's universal list survived the rewrite | The §6 pin in `tests/test_the_agent_contract_holds_the_universal_rules.py` is unchanged: *post nothing, push nothing, open no pull request, and spawn no agent* |
| §7 covers a leaving that is not a file | A pin on the widened sentence, shown red against the old §7 |
| The sealer's window is closed rather than forgotten | `tests/test_the_seal_is_taken_once_by_the_sealer.py` asserts `agents/sealer.md` no longer carries the window paragraph, and still names §6 and its one cell |
| No definition picked up the contract's new sentences | `tests/test_a_moved_rule_leaves_its_definition.py` runs over the rewritten sections and every definition, including `test_the_window_sits_between_what_was_measured` |
| The routing template's criterion is readable where the row is answered | A pin in the template's own test, if one covers it; otherwise the review round is what reads it |
