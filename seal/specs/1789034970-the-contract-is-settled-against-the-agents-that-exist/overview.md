# 1789034970-the-contract-is-settled-against-the-agents-that-exist — overview

📋 implement applied
· spec:     `seal/specs/1789034970-…/{spec.md, plan.md, questions.md, routing.md}`; `skills/agent-contract/SKILL.md` §*How the sections are numbered*, §2, §6, §7; `CLAUDE.md` §*Verification Scope*, §*Routing, decided at the start*, §*a change writes fragments, never the shared file*, §*a ledger coordinate names content*; `CONTRIBUTING.md` §*Name a module*; `skills/implement/SKILL.md` §§1–4; #120's body and its two comments, read with `gh issue view 120`
· evidence: `seal/ledger/1789034970-the-contract-is-settled-against-the-agents-that-exist.md` — R1, R2, R3 added; row S8 REMOVED from `seal/ledger/1789002694-…md`; thirteen rows re-verified across `seal/ledger.md` and the two fragments
· verified: **executed** — `bin/test` over eleven modules, narrowly, at every phase boundary, with each moved or added pin seen red first; `bin/evidence-check .` (1111 ok · 0 drifted · 0 broken, exit 0); `bin/survivor-check --range origin/release/v0.10.0...HEAD --exempt …` (exit 0, 15 exempt); `uvx ruff check` and `uvx ruff format --check` on the changed Python files only. **Unverified** — the full suite, the repository-wide lint and the typecheck, which `agent-contract` §2 leaves to the sealer

## Why this work exists

The file every agent receives before its first tool call told the one agent
built for the broad gate that the gate was somebody else's, and told two
agents that write durable records that they write none — so this settles §2,
§6 and §7 against the four agents that exist rather than the three that
existed when the contract was written.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether `agents/sealer.md` gains a section where the deleted one stood | `spec.md` §Scope 4: *§*§2 as it stands, and #120* is deleted* — and nothing about a replacement | A replacement section, `## The one run, and why it is yours`, in the same place | §2 as rewritten says the assignment lives in the definition rather than in the contract — *One definition in this plugin does hand them over — the sealer's* — and after a bare deletion no sentence in that file assigned the act. §2's pointer would name a file that does not answer, which is #30's own opening one release later. Phase 3's record carries the reasoning |
| Whether the two cases in `tests/test_the_seal_is_taken_once_by_the_sealer.py` keep their names | `plan.md` phase 3: the window case is *rewritten to pin that the window is CLOSED* — silent on the name, and the other case is not mentioned at all | Both renamed | A case named `…states_the_contradiction_and_the_ticket_that_settles_it` that asserts the contradiction is absent is a name a reader trusts over its body. The rename is what forced row S8 out of the other work item's fragment — a renamed unit is a REMOVED anchor — and `spec.md`'s own reason for rewriting rather than deleting is preserved: the case still exists and still fails if the paragraph comes back |
| `plan.md`'s Phases table had no `Verified by` column | `plan.md` shipped `\| # \| What it delivers \| Status \|` | The column added while phase 1 closed | `skills/implement/SKILL.md` §3: *Each phase carries a **Verified by** column, so it cannot be called done the way a checkbox can be ticked*. No row's scope changed |
| The §7 story's last clause | `spec.md` and `plan.md`: `git switch` refused *a branch it still held* | *a branch a worktree already held* | #120's comment of 2026-09-10 is the primary source and says *another worktree already held*. *It still held* invites a reader to look for the same branch twice |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. `agent-contract` §2 leaves the broad gate to the definition that assigns it, which is `agents/sealer.md`'s. Eleven modules were run narrowly instead, 350 cases in the largest single run | the sealer, spawned once the review rounds settle |
| Whether the `Implementation` criterion changes how the row is answered. It is a documentation change and its whole value is measurable only on the next release, which is what #120's first comment asks for | the release after this one, against `routing.md` files written under the new template |
| That the widened §7 actually stops a probe leaving a worktree. It names no mechanism, by the owner's answer to Q3, so nothing in the tree can check it — the objection was weighed and accepted | a review round, and then the next probe that makes one |
| Whether the 15-word duplication guard should reach the skills a definition preloads. Round 2 measured three pairs at or over the window across `skills/**/*.md`; this branch trimmed the one it wrote, from 16 words to 10, and the other two predate it — `skills/implement/SKILL.md` against §5 at 30 and §9 at 15 — so widening the glob is a sweep that would go red on content nobody here authored | the repository owner, at the release that takes the sweep |
| Whether `terminal_value` should refuse a wrapped terminal line rather than join it. Round 2's fix pass chose to join: truncation reads as a finished sentence so nobody looks, a swallowed line reads as wrong at a glance, and a refusal would stop `round_record.py new` on a report that broke no written rule. The guard against over-joining is four lines and cheap to reverse | the repository owner, if a report ever loses a line to the join |

## Not done

**`smith`'s §-by-§ scoping.** #120's first comment asks explicitly that it not
be frozen while three answers are live, and `questions.md` Q4 records the
owner's agreement. What landed instead is the criterion in
`templates/sdd-routing.md`, which is what makes the next release able to
measure the row rather than re-argue it.

**Splitting the contract.** Refused in the question batch, with the grounds in
`questions.md` Q2: the defect is contradiction rather than irrelevance, a line
drawn at four agents is redrawn at five, and a `§N` citation that no longer
names one file is a cost every round record already written would pay
retroactively.

**The payload number.** #292's meter has its before-number recorded and this
work item did not chase it. For the record rather than as a claim about the
meter: `skills/agent-contract/SKILL.md` went from 13,765 B to 16,238 B, which
is a rise of about 18%. Every section this work item touched gained the story
that bought its rule, which is this repository's convention and is what keeps
a rule from being re-litigated by someone who has not paid for it. `spec.md`
§Out says either direction is fine.

**A pin on `§2 contains no agent name inside a conditional.**` The frame calls
this the binding constraint and says it is *read at review*. Nothing here
checks it, and nothing could without deciding what a conditional is; what is
pinned instead is the universal sentence's presence and the old owner's
absence. The review round is the reader.

## How the run ended, and what left with it

**The review chain capped at round 3, and three findings left as issues rather
than as fixes.** `chain_check`'s rule: after the record that met the floor, at
most one later record may close on a fix — round 2 was that one — and the
record that reads its fixes ends the run whatever it finds. Round 3 was that
record. Its three findings are `deferred #339`, `#340` and `#344`.

**The fixes for all three were written and verified before the cap was read,
and were then reverted.** They are on `backup/120-before-rewrite` at `3b228f4`
and `8fd2f59`: the join's guard pinned (103 cases green before the pin, 4 red
after), the protocol's §14 half, and a corrected count. Each issue carries the
fix in full so that nothing is re-derived. Reverting good work is the cost the
bound charges, and it is charged on purpose — a run that keeps fixing past its
bound is the state the bound exists to end, and this one had already produced
one regression while closing another.

**A fourth round ran and has no record**, which is why
`rounds/round-4-report.md` sits beside three records rather than four. It was
spawned before the cap was read, it reviewed the reverted fixes, and its
findings are in #339, #341, #342, #343, #344 and #345. Its report is kept
because the work is real and the issues cite it; a fourth `round-N.md` is not
written because the run ended at the third.

**What this branch therefore ships is `ce0f9fe`** — the contract's three
sections, the four documents that read them, the routing criterion, and rounds
1 and 2 with their fixes. What it does not ship is the parser repair that
round 3 asked for, and #339 is where that lives.

## Fed back into the spec

None. Every clause this work item executed against was written before the
first edit, and the two judgments it had to make on its own — the sealer's
replacement section and the two renames — are recorded in the divergence table
above and in `seal/ledger/1789034970-…md` rows R1 and R3 rather than as new
clauses.
