# 1790076080-every-orchestrator-rule-is-a-sentence — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` of this work item · `CLAUDE.md` §*A change writes fragments, never the shared file*, §*a thing more than one party can have is named with whose*, §*The goal a design is chosen against* · `CONTRIBUTING.md` §*What a change to a gate must carry* (read, found not to apply — nothing lands under `hooks/` or `.github/workflows/`) and its network-touch list · `skills/implement/SKILL.md` §1–§4 · `skills/agent-contract/SKILL.md` §1, §2, §5, §9, §12, §15 · `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* · `seal/follow-up.md`
· evidence: `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md`
· verified: see `## Not verified` below, and each phase record's own closing paragraph

## Why this work exists

#330 reports that a rule reaching an agent arrives by mechanism while a rule
reaching the orchestrator is a sentence it has to remember; this counts the
class the ticket could not name, holds the count with a test, and gives the
one act of its three measured misses that is still a sentence a command to
type.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The table's row count | `spec.md` §Scope says *"The orchestrator has nineteen acts"* and, in the same bullet, that the new section *"makes the section a row of its own table"*. The table as built carries twenty rows | twenty | Nineteen is the count of the class before this work writes anything, and the rule the same paragraph states produces twenty once the section exists. Measured both ways in `phases/phase-1.md`. Exempting the section holding the table would be a special case that hides an act, which is the state the ticket reports |
| What `Delivered by` answers | `spec.md` names four values and does not say what question they answer. Several sections carry more than one act, so *what delivers this section* has no single answer | *when the orchestrator forgets this act, what notices?* | Decidable per heading, and it is the ticket's own question. Paired with a discipline the spec demands of one row and this work applies to all: the grounds of a row whose delivery reaches only part of its act name the part it does not reach |
| The row phase 3 was to flip | `spec.md` and `plan.md` both name *the row for the flow-log act*. There is none: that act lives in `skills/verify/SKILL.md` under a heading carrying no `Orchestrator:` marker, in a file the row rule does not read, and the test refuses a row naming a heading no file carries | the sentence goes into the table's section as prose, naming the act, its file, its delivery and that nothing makes it run | Marking the heading would not turn the marker test red — `skills/verify` is in no agent's `skills:` list — and is refused on the repository's one-word-one-meaning rule: the marker means *keep this out of an agent's payload*, and asserting that about a file no payload holds gives it a second meaning. **Twelve files outside `CHANGELOG.md` and `seal/specs/` name that heading**, four of them test modules that would go red on a rename, and `seal/ledger.md` carries nine live rows anchored on the heading text. Two of the twelve are reachable only by tolerating a line wrap — `.github/scripts/roll_flow_measurement_issue.py` and `skills/commit-pr-convention/SKILL.md`. **Corrected twice.** Round 1's fix pass replaced *eight documents*, which had counted nothing, with *thirty-three files*, which did not say what it counted — a single-line search with this work item's own files dropped, understating in the same direction as the claim it repaired. Round 2 re-derived it both ways, and the number above is the one that does not drift as records accumulate; the whole-tree total is in `phases/phase-3.md` with its tree and its method. The repair is mechanism and belongs in an issue, named in the hand-back |
| What the class actually looks like | The ticket's premise is that every rule reaching the orchestrator is a sentence. Reading all twenty sections: 8 are delivered by a check, 5 by a command, 5 are still a sentence, 2 are part of a parent | recorded, not argued | Every one of the twenty is still described in prose; what **thirteen** have is something that refuses when the act did not happen — the 8 checks and the 5 commands. **Corrected 2026-09-22 in round 2's fix pass**, which is the third place this denominator had to be repaired: it read *fourteen*, and the count beside it in the same cell already said 8 and 5. The tree has been closing this class one act at a time since the ticket was filed and nobody counted. `phases/phase-1.md` has the split |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ The full suite, the repository-wide lint and the typecheck | **SEALED at `e339586d` against `6d410023`**, taken by the sealer after the rounds settled — contract §2 left it to the definition that assigns it, and this one did not. **4121 passed, 9 skipped.** The `Broad gate` row is `bin/test -q && uvx ruff check . && uvx ruff format --check .`, so a single exit 0 cannot on its own say which of the three ran: **both `ruff` commands ran after the suite and printed their own result**, which is what makes the one exit code stand in for nothing. Beside it, ledger 1451 ok, and chain, corrections, survivors and mode all exit 0. Written into `rounds/round-3.md`'s `Broad gate` cell and committed at `af599dc1`; not run by this segment at any point |
| Whether a network-WRITING arm needs a row of its own in `CONTRIBUTING.md`'s list of the plugin's network touches (Q3) | the repository owner, who owns that list. Shipped as the framer's default (a): stated in the pull request body and `plan.md` §*Operational impact*, `CONTRIBUTING.md` edited not at all. **Grounds corrected 2026-09-22 in round 1's fix pass, after the reviewer opened the section.** They used to read *both existing entries are touches that fire without anybody asking*, which generalises the wrong way: read as *this list is for unasked touches*, a future hook firing only when a person types something would be argued out of a list that exists for hooks. The section's own scoping is narrower and settles it cleanly — the bullet is **Hooks stay local and quiet**, its sentence is *"Two hooks reach the network"*, and the three conditions it sets for a third are hook-shaped (an opt-in condition so unrelated repos are untouched, a throttle so it is not per-session, silence on every failure). `--post` is not a hook and fires on no hook, so the list does not reach it whether or not it is asked for. The bullet's last sentence — *anything that would send repository contents, paths, or prompts is not on the table* — binds hooks too, so round 1's 🔴 was a defect rather than a rule violation, which is why that rule is now written into `emit`'s own docstring rather than cited. The reviewer can still overturn the default by opening the section |
| ✅ `session-cost --post` against a live tracker | **Run by the orchestrator at this run's segment boundary, posting the framing-and-build reading to #496** — the first time the act this log exists for was performed by a command rather than by a session remembering the procedure. Opened the comment rather than taking the account: it has the `comment_body` shape, judgment first and the reading fenced beneath it, and the label resolved to exactly one open log, which is the only state that posts. **Two claims, and only the first is evidenced by this post.** It is evidence the command works end to end — lookup, one open log, body composed, comment posted. It is **not** evidence that round 1's path leak was absent: the leaking line is `report_spawns`' EMPTY branch, and this reading was non-empty, `8 spawns found, and the run slices into 10 rows`. So the basename substitution round 1 added was never reached live, and the state that held here is the state that held before the fix. Scanned anyway — **zero `/Users/` and zero absolute paths of any shape** — which says the body is clean, not that the guard fired. The empty branch is covered by `test_the_posted_body_does_not_carry_the_transcripts_path` and its `--spawns` twin, with `gh` stubbed |

## Not done

Sixteen of the twenty acts keep the delivery they already had and none is
armed further, on the ticket's own grounds: only those with a measured miss
get one, and *the rest are unmeasured, and building for them is building for
a guess*. The five rows reading `still a sentence` are what a next work item
picks from, and the table is what makes them findable.

`session-cost --post` does not make anybody run it, and both the skill and
the table's section say so rather than reading closed. The miss #330 measured
for the flow log is that the meter sat unreferenced through a full day of
measurements nobody took — the measurement was not taken, not that the
posting failed. The shape that would close that half is a `PostToolUse`
notice at each segment boundary, rejected in `plan.md` on cost and named
there as where a next work item on this class should start.

**Three things left for an issue rather than built here**, all mechanism and
all for the repository owner. They are one shape said three times: an
enumeration the tree does not hold in step.

1. **The table cannot reach an act addressed to the orchestrator outside the
   two orchestration files**, which the flow-log act is. The repair is either
   a row rule that takes a named list of sections elsewhere, or splitting the
   `Orchestrator:` marker into one meaning *keep this out of an agent's
   payload* and one meaning *this is the orchestrator's act*. Choosing between
   the two shapes is a person's, which is why it is not a commit here.
2. **The table reads the marker rather than the meaning**, so a **twenty-first**
   act written without the prefix costs nothing and is counted by nobody.
   **Corrected 2026-09-22 after round 3:** this said *a twentieth act*, and the
   table already carries twenty rows for twenty acts, so the next one without a
   prefix is the twenty-first. It matters because this sentence is what the
   issue gets scoped from, and round 2's own deferred row already states it the
   corrected way.
3. **Nothing pins the module docstring's enumeration to the module.**
   `tests/test_every_orchestrator_act_names_its_delivery.py`'s docstring lists
   the eight planted trees that carry a defect and the two that do not; it is
   correct at this commit and a case added next month makes it wrong silently.
   Round 2's 🟡 was an instance of exactly that — the list said four where five
   stood and named a case in no file — and round 3 confirmed against the
   checker that nothing reaches it: `evidence_check.py`'s records arm reads
   `.md` under a live work item, so a Python docstring is outside everything
   that runs. A case comparing the block's names against the module's own AST
   would close it. **Round 3 judges this the cheapest of the three** — a small
   case rather than a design choice. It is here rather than committed because
   a case is mechanism a fix pass may not add, which is the rule
   `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins
   it* states.

## Fed back into the spec

none
