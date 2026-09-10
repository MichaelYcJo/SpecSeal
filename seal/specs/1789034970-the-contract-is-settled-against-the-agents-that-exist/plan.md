# Implementation Plan: the contract is settled against the agents that exist

<!-- seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

Three sections of one file, and the four documents and three test modules
that read them. §2 stops naming the orchestrator as the broad gate's owner
and stops forbidding the act to the agent whose whole procedure it is; §6
stops carving exceptions and says instead that what an agent writes is what
its own definition names; §7 stops being about files and becomes about
leavings. `agents/sealer.md` loses the paragraph that says it ships under a
contract contradicting it, because after this it does not. And
`templates/sdd-routing.md` gains the criterion that decides its
`Implementation` row, which is the one thing #120's first comment asks for
instead of freezing `smith`'s scope.

No section is added, renumbered or retired. Every `§N` in every round record
this repository has written still means what it meant — which is the whole
value of the numbering rule, and the reason a split was refused in the
question batch.

The change is to the file every agent receives before its first tool call, so
a wrong sentence is paid on every spawn of every agent. That is the top rung
of the `implement` skill's ladder: `spec.md` and this plan come first, and the
gate was passed in the owner's one batch on 2026-09-10.

## Technical context

Every coordinate below was opened by the session that wrote this plan. Open
them again before building on them (§5) — what is written here is a claim with
a coordinate, not evidence.

- `skills/agent-contract/SKILL.md` — `## §2` at `:57`, `## §6` at `:126`,
  `## §7` at `:138`. The file's opening paragraph (`:19-25`) is the test each
  rewrite has to pass: *nothing here is one agent's own*, and *a section that
  would need a per-role exception is a sign the rule is not universal*.
  §*How the sections are numbered* (`:39-45`) is why nothing moves.
- `tests/test_the_agent_contract_holds_the_universal_rules.py` — `PINS` at
  `:36`, one phrase per section taken from the BODY. §2's phrase at `:38`
  names the orchestrator and moves with the rewrite; §6's at `:42` is the
  universal list and must survive the rewrite unchanged; §7's at `:43` is
  *it runs once, and it is deleted before you hand over*, which the widened
  sentence must either keep or replace deliberately. `without_pin` at `:227`
  is how each pin is shown red.
- `tests/test_broad_gate_rule.py:211` —
  `test_the_prohibition_itself_has_one_home_and_it_is_the_contract` asserts
  at `:220` that the contract says *is the orchestrator's, run once, after
  the review rounds settle*. **This is the case that pins the defect.** It is
  re-pointed at the sealer, and the old sentence is asserted absent — the
  second half matters, because a contract that names both owners is the
  state `test_the_definition_names_the_sealer_as_the_suites_owner` already
  refuses one file over.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py:1626` —
  `test_the_sealer_states_the_contradiction_and_the_ticket_that_settles_it` <!-- NAME NOT IN TREE -->
  pins the window paragraph. `section(number)` at `:1505` reads §2 and §6
  from the contract rather than typing them, so
  `test_the_sealer_cites_the_section_without_carrying_it` (`:1661`) checks
  the rewritten sections automatically — the sealer's definition must not
  pick up a 15-word run of the new §2 or §6.
- `agents/sealer.md:107-119` — §*§2 as it stands, and #120*, whose last line
  is *When #120 lands, this section is the paragraph it deletes*.
  `:86-105` is §*The one write, and why it is yours*, which stays and is
  re-pointed at §6 as rewritten.
- `agents/warden.md:180-199` — the §6 bullet. `:199` reads *§6's two
  exceptions*, which is the phrase the rewrite makes false.
- `skills/code-review/orchestration.md:62` — *§2 reserves the broad gate for
  you*, addressed to the orchestrator. `:468` says *The broad gate still runs
  once, after the rounds settle (`agent-contract` §2)*, which stays true and
  is not touched.
- `templates/sdd-routing.md:19` (the row) and `:24-38` (its comment block).
  `tests/test_waiver_decided_at_start.py:120` parses the template through
  `hooks/routing.py` and asserts `implementation is None` — the criterion goes
  in the comment, and the row's placeholder is not touched.
  `:286` asserts the template ships every word the parser accepts.
- `tests/test_a_moved_rule_leaves_its_definition.py` — derives its section
  list from the contract, so the three rewritten bodies are checked against
  every definition on the day they land. `test_the_window_sits_between_what_
  was_measured` prints the margin; a rewrite that lands a 10-word phrase in
  common with a definition narrows it.

## Phases

| # | What it delivers | Verified by | Status |
|---|---|---|---|
| 1 | §2 and §6 rewritten, with their pins re-measured and seen red | `bin/test tests/test_the_agent_contract_holds_the_universal_rules.py tests/test_broad_gate_rule.py tests/test_a_moved_rule_leaves_its_definition.py -q`; both moved pins seen red against the contract as it stood; the 15-word margin re-measured | `63d013d` |
| 2 | §7 widened, with its pin | `bin/test tests/test_the_agent_contract_holds_the_universal_rules.py tests/test_a_probe_that_commits_says_so.py -q`; the widened pin seen red against the old §7 | `94a2451` |
| 3 | The four documents that read those sections follow | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_a_moved_rule_leaves_its_definition.py tests/test_every_agent_reads_the_contract.py tests/test_docs_line_wrap.py -q`; each re-pointed case seen red first; the ledger anchors this phase removes re-verified | `2821f6d` |
| 4 | The routing template's criterion | `bin/test tests/test_waiver_decided_at_start.py tests/test_routing_is_recorded.py -q` | `c4e1bfc` |

<!-- The `Verified by` column was added while phase 1 closed. `skills/implement/
SKILL.md` §3 requires it — a phase cannot be called done the way a checkbox is
ticked — and the frame shipped the table without it. Nothing about the scope of
any row changed. -->

Phase records: `phases/phase-N.md`, written as each phase closes.

### Phase 1 — §2 and §6

The two sentences the ticket is about. Both are rewritten in place, and
neither may contain an agent name inside a conditional: the general form is
what a fifth agent inherits, and *unless you are the sealer* is the shape
this file's own opening calls a sign the rule is not universal.

**§2.** What it must still say: narrow and often, broad once; the tests for
the slice while you work, and your module and the ones it touches at a phase
boundary; the broad gate is the full suite, the repository-wide lint and the
typecheck; it fires once, after the review rounds settle; a round is edits
already scheduled, so a broad run taken before it is spent by the first fix
rather than banked; and the handover carries the suite labelled, never
omitted, because a suite that is simply not mentioned reads as a suite that
passed. What it must stop saying is that the run is the orchestrator's. The
owner is the sealer, and the universal form is that the gate is one act with
one owner and it is not yours unless your own definition assigns it.

The section's closing paragraph — *this rule sat in two agent definitions in
near-identical words, and a third agent inherited neither copy* — is the
story that bought the rule and stays. What may be added beside it is the
second failure the same sentence produced: a prohibition with no owner is one
every reader reasons past, which is #30's opening sentence and the reason the
sealer exists.

**§6.** The heading stays a report; the sentence about durable records
becomes *what you write is named in your own definition and nothing else*.
The universal list — post nothing, push nothing, open no pull request, and
spawn no agent — is unchanged, and so is the pin on it. The paragraph at the
end that carves exceptions goes, replaced by the default it implies: a
definition that is silent names no write, so an agent whose file says nothing
writes no durable record at all.

Cases: `tests/test_the_agent_contract_holds_the_universal_rules.py` PINS §2
re-pinned on a phrase from the new body, shown red by `without_pin`; §6's pin
unchanged and shown still to hold. `tests/test_broad_gate_rule.py:211`
re-pointed at the sealer with the orchestrator sentence asserted absent, and
shown red against the contract as it stands today.

Narrow run for this phase: `bin/test tests/test_the_agent_contract_holds_the_
universal_rules.py tests/test_broad_gate_rule.py tests/test_a_moved_rule_
leaves_its_definition.py -q`.

### Phase 2 — §7

The file rule stays: one file named `test_tmp_*`, run once, deleted. What is
added is that the rule is about what a probe leaves rather than about files —
a worktree, a branch, a checkout, a scratch clone is the same act and the
probe is not over until it is gone. The story is the one the ticket's second
comment records: a review round's probe added a worktree to check that the
broad gate's base comparison cleans up after itself, the worktree outlived the
round, and it surfaced two work items later when `git switch` refused a branch a
worktree already held — by a reviewer that had followed §7 to the letter and whose
report said so.

The alternative the owner refused is worth one clause in the section, because
the next reader will reach for it: the shapes are not enumerated. Every
enumeration in this repository has rotted, and the sentence has to hold for a
kind of leaving nobody has met yet.

Case: the §7 pin in `tests/test_the_agent_contract_holds_the_universal_rules.py`
moved to the widened sentence and shown red against the old §7.

Narrow run: `bin/test tests/test_the_agent_contract_holds_the_universal_
rules.py tests/test_a_probe_that_commits_says_so.py -q`.

### Phase 3 — the documents that read those sections

- `agents/sealer.md`: §*§2 as it stands, and #120* deleted. §*The one write,
  and why it is yours* re-pointed — it stops reading as an exception §6
  permits and starts reading as the write §6 says a definition names. The
  final paragraph of that section, *everything else §6 withholds stays
  withheld*, keeps its meaning and stays.
- `agents/warden.md:199`: *§6's two exceptions* is no longer true; the report
  and the parity mark are two writes its definition names. The distinction
  between the record and the report, which is the bullet's actual content, is
  untouched.
- `skills/code-review/orchestration.md:62`: *§2 reserves the broad gate for
  you* becomes what §2 now says — the gate is the sealer's, and the fix pass's
  step is still the orchestrator's for the reason the paragraph already gives
  (the range is already typed).
- `tests/test_the_seal_is_taken_once_by_the_sealer.py:1626`: rewritten to pin
  that the window is CLOSED — the definition no longer carries the
  contradiction paragraph, and still names §6 and its one cell. **Not
  deleted.** A deleted case is a paragraph that can come back, and this one
  came with an expiry written into it.

Narrow run: `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py
tests/test_a_moved_rule_leaves_its_definition.py tests/test_every_agent_reads_
the_contract.py -q`.

### Phase 4 — the routing template

`templates/sdd-routing.md`'s `Implementation` comment gains the criterion:
finding out goes to `scribe`; writing down stays with the session — unless
the expected diff is large enough to threaten what the orchestrator still has
to hold, which is the one case `smith` answers. Written as a criterion and not
as a default: the row is optional and its placeholder must keep parsing as
unanswered, which `tests/test_waiver_decided_at_start.py:120` holds it to.

The threshold in the last clause is a number nobody has, and the comment says
so rather than inventing one. The case for a delegate there is
replaceability — the orchestrator is the single participant a release cannot
replace mid-run — which is a different axis from the token cost #263
measured, and saying which axis is what makes the next release able to
measure it.

Narrow run: `bin/test tests/test_waiver_decided_at_start.py
tests/test_routing_is_recorded.py -q`.

## What this work item does not do

- It does not split the contract. The owner's answer, with the grounds in
  `routing.md`.
- It does not scope `smith` section by section. #120's first comment asks
  that it not be frozen while three answers are live.
- It does not add a §17, retire a section, or renumber one.
- It does not chase the payload number. #292's meter has its before-number
  recorded; whether this rewrite is a few hundred bytes up or down is not
  what it was built to answer.

## Records this work item writes

- `seal/specs/1789034970-…/changelog.md` — the fragment, gathered at the
  release. Never `CHANGELOG.md` itself.
- `seal/ledger/1789034970-….md` — a row for any claim this work leaves that
  a later reader would otherwise have to re-derive. A rewrite of three
  sections is a claim about what those sections now say, and the pins are
  where that is enforced; write a row only where a pin does not already
  carry it.
- `rounds/round-N.md` per review round, and the last one's `Broad gate` cell,
  written by the sealer.
