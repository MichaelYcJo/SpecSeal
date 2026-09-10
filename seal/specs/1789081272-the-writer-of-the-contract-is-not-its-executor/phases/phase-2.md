# 1789081272-the-writer-of-the-contract-is-not-its-executor — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `dcfd693` — the moves and their five cases; the records follow it |
| Ran by | smith on Opus 5 (1M context) |

## What this phase was asked

Four deliveries, on top of what phase 1 handed over.

1. The two utility skills move off `agents/smith.md`'s design gate onto the
   framer — the paragraph beginning *Two skills are yours to call when the
   gate needs them* is what leaves. The smith keeps the whole of the rest of
   that gate: the questions batch, `routing.md`, the SDD rung, the waiver.
   Read `agents/framer.md` first, so it is a move rather than a duplication.
2. The smith's first act on a frame becomes *say whether it holds*, written
   down for the first time. The home was left to this phase's judgment — the
   top of **Implement** or the head of **Requirements** — with the reason
   owed to this record. Q3's default is the answer for where a *no* goes:
   `phases/phase-N.md`'s `## What this phase found` and the hand-back, never
   back to the framer.
3. `agents/sealer.md`'s *the three definitions that stay silent* follows the
   agent set (S11).
4. `docs/flow.md` step 2 loses its second clause, `once #84 exists; the
   session until then`. S12 is a hard constraint over the same step and none
   of its three pins may move. 0.11.0's checkbox and its section are phase
   6's and were not touched.

Three cases, each shown red first per §15. S4 — the two skills named as
callable in `agents/framer.md` and in no other `agents/*.md`, counted from
the glob, red against `agents/smith.md` as it stood. S5 — the drawing-holds
sentence and where a *no* goes. S11 — the silent-definition count derived
from the glob, in the shape
`test_only_one_definition_assigns_the_broad_gate` already has.

Phase 1 also handed over that
`tests/test_chain_hooks_hardening.py:851 test_the_design_gate_belongs_to_the_smith`
asserts both things this phase breaks, and that fixing it is part of the
phase rather than a casualty of it: rewrite it to read the gate's owner from
the tree instead of from the name `smith`, and keep what it was written to
prevent.

## What this phase found

**Row 2 holds. Three things sit outside it, and each is written down rather
than carried.**

- **The `docs/flow.md` edit is in two phase rows at once.** `plan.md` row 6
  still lists *step 2 loses `once #84 exists`* beside 0.11.0's checkbox, and
  the prompt assigns the clause to this phase. The prompt is right and the
  plan cannot be followed as written: S11's scenario names the flow sentence
  as well as the sealer's count, so the S11 case — phase 2's, by row 2's own
  Verified-by cell — is red until step 2 is edited. What stays with phase 6
  is the checkbox and the section around it. Recorded as a divergence in
  `overview.md` rather than fixed by editing row 6, because the Delivers
  column is the framer's writing and only the Status column is mine.
- **The home of the drawing-holds sentence is the Requirements phase, not
  Implement, and `plan.md`'s technical-context table says Implement.** The
  prompt hands the judgment to this phase, so this is a judgment made rather
  than a bound broken — but the plan reads the other way and a later reader
  deserves the reason. Requirements is where the frame has just been read
  and where nothing has been spent yet. Below it sits the design gate, which
  is the one interruption of the whole run: a frame judged after that gate
  is a frame judged after its questions have already been put to a person.
  The check is also the same act §5 already asks for one level down — *open
  the coordinates before you build on them* — so it belongs beside it, and
  the case pins the home for that reason rather than only the sentence.
- **Row 2's Delivers cell does not mention the two stand-down clauses or the
  case that pins them.** Phase 1's record does, under *Phase 2 also owns the
  third axis of this*. The clauses are the reason the move is three files
  and not one: a skill that stands down for an agent that no longer calls it
  is a skill with no stand-down at all.

**The case that pinned the old owner was pinning a typed name, and that is
why it went stale silently.** `test_the_design_gate_belongs_to_the_smith`
read `smith` out of its own source in both directions — the definition it
opened by name, and the literal `smith is driving` it looked for. Nothing in
it could notice the gate moving. It is now two cases, and neither types an
owner:

- `test_each_utility_skill_is_callable_from_exactly_one_definition` walks
  `agents/*.md` and asserts each skill has one home. A sixth definition
  picking one up is red on the day it lands.
- `test_the_skills_stand_down_for_whichever_definition_calls_them` takes that
  one home, strips `.md`, and requires the SKILL.md frontmatter to say
  `<that name> is driving`. The clause now follows the definition that holds
  the skill, whichever it is.

The direction this still misses, stated rather than left to be found: a
definition that calls a skill in words that never spell its name is invisible
to the glob, which is the same verbatim-versus-semantic trade
`test_a_moved_rule_leaves_its_definition.py` states for itself.

**S11's count is spelled in words, so a word table is needed, and a word
table is not a list of agents.** `SILENT_IN_WORDS` maps a number to its
English spelling for sizes one to seven; the number itself comes from
`len(glob) - len(assigning)`, with the same `ASSIGNS_THE_GATE` marker
`test_only_one_definition_assigns_the_broad_gate` uses. An agent set larger
than seven fails on the guard with a message saying to change the sentence
rather than to extend the table — a sentence naming a count in words has
outgrown itself by then.

**One sentence had to go that no row asked for.** The design gate's opening
read *you own this decision; the utility skills do not make it for you, and
they should not fire on their own while you are driving*. With the skills
gone it names two skills the section no longer has, and its second half
contradicts the clause this phase wrote into both of them — they stand down
for the framer now, so a smith telling them to stand down for the smith is
the drift the pair of cases exists to catch, in prose. It reads *you own this
decision, and no skill makes it for you*, which is the claim that survives
the move.

**Neither README moves, and that was checked rather than assumed.** Both
editions list `confidence-check` and `feature-planner` in the eleven a
session loads on demand. Nothing about that changes: neither skill was ever
preloaded and neither is now, and Q4's measurement — the one that would move
5/11 to 7/9 — is about a `skills:` frontmatter list nobody wrote.

**The mutation loop found one weak pin and it stayed weak on purpose.**
`assert "never back to the framer" in requirements` survives appending a word
to `framer`, because a substring pin cannot tell `the framer` from `the
framer's inbox` — and that mutation leaves the sentence's meaning intact, so
a green is the right answer to it. The mutation that changes the meaning,
`never back to` → `or back to`, is red. Recorded because the next reader
should know which of the two was tried.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `agents/smith.md`'s design-gate paragraph naming `confidence-check` and `feature-planner` as the smith's to call | `agents/framer.md` §*What you are*, the paragraph beginning *Two more skills are yours to call* — written in phase 1, which is what made this a move. `agents/smith.md` keeps a three-sentence pointer at it in the same place, so a smith reading the gate learns where the skills went rather than that they vanished |
| `agents/smith.md`'s design-gate opening clause *the utility skills do not make it for you, and they should not fire on their own while you are driving* | nowhere, and nothing needs it. The stand-down it asserted is stated in each skill's own `NOT for` clause, which is the copy the skill loader reads and the copy `test_the_skills_stand_down_for_whichever_definition_calls_them` pins. The half worth keeping — that the gate is a judgment no skill makes — stays in the rewritten sentence |
| `tests/test_chain_hooks_hardening.py`'s `test_the_design_gate_belongs_to_the_smith` | split into the two cases above, both reading the owner out of the glob. What it was written to prevent — the two skills self-triggering beside the phase that already calls them — is asserted by the second of them, and by the first that there is a single phase to be beside |
| `docs/flow.md` step 2's clause `once #84 exists; the session until then` | nowhere. It described the interval before `agents/framer.md` existed, and that interval closed with `77e0ae5`. Nothing in the sentence said which side of the arrival a reader was on, which is what made it read as a standing permission for the session to frame its own work |
| `agents/sealer.md`'s word `three` in *the three definitions that stay silent* | `four`, and the count is now derived — `test_the_sealer_counts_the_silent_definitions_from_the_glob` computes it from the same glob and marker rather than from a list of names |
