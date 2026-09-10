# 1789034970-the-contract-is-settled-against-the-agents-that-exist — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `63d013d` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

<!-- The model name is the one the spawning session gave, in the attribution
block of its own prompt. It is not this segment's idea of what it is, which
is the one filler the template refuses. -->

## What this phase was asked

`plan.md`'s row 1 and nothing past it. §2 and §6 of
`skills/agent-contract/SKILL.md` rewritten in place, keeping their numbers.

§2 must still say: narrow and often, broad once; the slice while you work and
the module plus its neighbours at a phase boundary; the broad gate is the full
suite, the repository-wide lint and the typecheck; it fires once, after the
review rounds settle; a round is edits already scheduled, so a broad run taken
before it is spent rather than banked; and the handover carries the suite
labelled, never omitted. It must stop saying the run is the orchestrator's.

§6 must keep *post nothing, push nothing, open no pull request, and spawn no
agent* verbatim, keep the report as the final output, and replace *you write
no durable record* with *what you write is named in your own definition and
nothing else*. The exception-carving paragraph goes.

The binding constraint on both: **no agent name inside a conditional.** The
file's own opening says a section that would need a per-role exception is a
sign the rule is not universal, and this work item is the one that has to pass
that test on its own two sentences.

## What this phase found

**Naming an owner and carving an exception are not the same act, and §2 needs
the first.** The obvious universal form — *whether the gate is yours is what
your definition says* — is true of a fifth agent and says nothing a reader can
check. On its own it would have left §2 in the state #30 opens on: a rule with
no holder in the room, which both readers reasoned past. So the section states
the universal form as the rule and then points, as a fact rather than as a
condition, at where the one assignment currently lives. `assert "orchestrator"
not in body` is the new guard, and it is scoped to §2's body because the word
is legitimate in the contract's opening paragraph, which is about the prompt a
round arrives in.

**§6's pin decided the first word of the rewrite.** `PINS[6]` is
*post nothing, …* in lower case, matched as a substring, so any rewrite that
started that list at a sentence boundary would have capitalised the `p` and
broken a pin the frame requires to survive unchanged. The list therefore stays
mid-sentence, after a clause that says which half is conditional. That is
worth knowing before §6 is next reworded.

**§2's pin had to move; §6's had to not.** The old §2 pin was the handover
label, which names the orchestrator — it would have survived the rewrite by
pinning the one sentence the rewrite was about to make false. The label is
still asserted, one module over, in `tests/test_broad_gate_rule.py`, so
nothing lost a check by the move.

**Measured margin, after the rewrite** (`test_a_moved_rule_leaves_its_
definition.py`'s own functions, run over the tree): the widest run any agent
definition shares with any section is still 10 words —
`agents/smith.md` against §8, *a bare word is a pathspec and git rejects it*.
The next is `agents/warden.md` at 9 against §6, and `agents/sealer.md` reaches
6 against §6. `LONGEST_KEPT_APPLICATION` is 10, so the margin under the
15-word window is unchanged by this phase. Phase 3 edits both of those
definitions and has to re-measure.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| §2's sentence *is the orchestrator's, run once, after the review rounds settle* | Nowhere. The orchestrator was never the agent; the act's owner is now named in §2 and assigned in `agents/sealer.md`, and `agents/smith.md` / `agents/warden.md` already carry *the full suite is the sealer's* as their own application |
| §6's paragraph *An exception is one agent's, and it is named in that agent's definition — never here* | Replaced in place by the default it implied: a definition that names no write names none. The mechanism it described is not lost — it is now the rule rather than the exception, so `agents/sealer.md` and `agents/warden.md` need re-pointing, which is phase 3 |
| The old `PINS[2]` phrase, *Hand over with the suite labelled `unverified` and the orchestrator named* | `tests/test_broad_gate_rule.py::test_the_prohibition_itself_has_one_home_and_it_is_the_contract`, which still asserts the label |
