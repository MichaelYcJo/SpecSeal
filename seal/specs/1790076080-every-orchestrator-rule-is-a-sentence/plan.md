# Implementation Plan: every orchestrator rule is a sentence

<!-- seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-22 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

#330 reports an asymmetry: a rule reaches an agent by mechanism and reaches the
orchestrator as a sentence. The frame reads the tree and finds the ticket's
evidence has moved under it — two of its three measured misses were closed
while it sat, by two different shapes, and the neighbouring ticket that shipped
(#343) shows that delivery was never the missing half.

So this work does two things and refuses the third. It **counts the class**,
by construction, and pins the count with a test; it **arms the one act of the
three still left as a sentence**; and it declines to arm the sixteen acts with
no measured miss, on the ticket's own grounds.

## Technical context

**What the enumeration is built on.**
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` already
reads both orchestration files' headings at `##` and `###` and already knows
the `Orchestrator:` marker; its docstring records that a `##`-only reader
*"came out short"*. The new test reuses that reading rather than writing a
second heading parser — two parsers of one marker is how half of them keep the
old answer (`hooks/routing.py`'s own reason for being a module).

The heading counts, read 2026-09-22:

| File | `##` marked | `###` beneath one |
|---|---|---|
| `skills/implement/orchestration.md` | 4 (lines 34, 44, 226, 243) | 3 (256, 279, 306) |
| `skills/code-review/orchestration.md` | 5 (18, 114, 475, 550, 562) | 7 (182, 216, 261, 286, 336, 370, 448) |

Nineteen rows.

**What the table is modelled on.** `skills/verify/scripts/broad_gate.py`'s
`PARTITION` (#468) holds every step of `.github/workflows/hygiene.yml`'s
release job against the arm that mirrors it or the reason none does, and a case
holds the table against the workflow from both sides. That list *"went three
releases at five while the workflow went to thirteen steps, and no case went
red for it"* before the partition existed. This is the same repair one subject
over.

**What `--post` is built on.** `skills/verify/scripts/session_cost.py` already
has `--segments`, `--spawns` and `--json`, and
`skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* already
enumerates the four label states and the two logs. The mode implements a
procedure that is written out in full; nothing about it is being designed, only
moved from prose into code.

**Constraints that shaped this.**

- Nothing lands under `hooks/` or `.github/workflows/`, so
  `CONTRIBUTING.md` §*What a change to a gate must carry* is read and found not
  to apply. The alternative that would have triggered it is in the table below
  with its failure scenario.
- `tests/test_release_hygiene.py` refuses a loaded document naming the running
  version, so no file this work writes names a version at or above the one this
  branch is preparing.
- `tests/test_one_word_one_meaning.py` holds one word to one meaning. The word
  this work uses is **delivery**; `arm` is left to the meaning `arm_check.py`
  and the commit gate give it, and `seal` is not reused.
- Editing `skills/verify/SKILL.md` removes wording, which the survivor sweep
  reads at the pull request. Where it reports a place still carrying removed
  wording, the exemption goes in this work item's own `survivors.md`.

**The failure scenario of the chosen approach, in six months.** The table is
true because a test holds it true, but the test reads the *marker*, not the
meaning — the same limit its neighbour states for itself. An act written for
the orchestrator under a heading carrying no marker has no row and nothing
notices, exactly as a paraphrase escapes
`test_a_moved_rule_leaves_its_definition.py`. What breaks, then, is not the
table rotting but the table quietly being incomplete: somebody adds a twentieth
act without the prefix, the count stays at nineteen, and the next work item
picks its subject from a list that is missing one. The mitigation is that the
marker is already load-bearing for a different reason — it is what keeps the
orchestrator's half out of every agent's payload — so a heading without it
costs something immediately and visibly.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A `PostToolUse` notice at each segment boundary**, telling the orchestrator the segment it just closed has not been measured | Deciding whether to print needs to know the repository has an open measurement log, which is a `gh` network call. On the hot path of every `Agent` call, that is a price paid on every spawn of every run for a reminder — against `CLAUDE.md`'s first goal, which judges a design by what it costs when nobody is at the keyboard. A local cache of the answer is a second piece of state to invalidate, for a notice | **rejected**, and it is the strongest rejected option. Named here because it is the one shape that would make the act HAPPEN rather than make it cheaper, and the next work item on this class should start from it |
| **A `SessionStart` line carrying the orchestrator's rules** | This is the channel that structurally matches the agents' `skills:` frontmatter — it arrives before the first tool call with nothing typed. It is refused anyway: what it can carry is prose, which is what `templates/claude-md-block.md` already carries, and the routing rule was in that block. The ticket's own *Not this* names *"another sentence"* as the failure with one more instance in it | **rejected**. Recorded so the channel is not rediscovered as though it were new |
| **A bigger `CLAUDE.md` block** | Same class, with a worse cost profile: the block is in every session's context in every project on the machine, so a rule that concerns one repository's review chain is paid for by every unrelated session. Its routing bullet is already the longest thing in the file | **rejected** |
| **A `PreToolUse` notice on `AskUserQuestion`**, firing when the orchestrator opens the routing batch | The act it would guard is closed. `templates/claude-md-block.md` carries the question's exact shape and `chain_check.py` reads the answer at the pull request — both since 2026-09-16. Whether the harness even matches that tool name is unverified, so building it would start with a probe for a gate nothing needs | **rejected**, obsolete |
| **One new command with a subcommand per orchestrator act** — the ticket's shape 2 | *"The steps have nothing in common but their owner, and a command whose subcommands share no code is a directory with a lid"* — the ticket's own words. The tree agrees from the other side: the two acts that closed did so as a command on one hand and a delivery channel plus a check on the other | **rejected**, and the question it belongs to is recorded as wrongly posed rather than answered |
| **Arm all nineteen acts** | Sixteen have no measured miss. The ticket: *"the rest are unmeasured, and building for them is building for a guess"*. It is also not one branch's work | **rejected** |
| **Ship the table alone, with no second phase** | Honest but incomplete: a branch whose whole output is a list is the state the ticket is reporting, and the ticket's *Not this* names a seventh document that says to read the other six | **rejected** |
| **Ship `--post` alone, with no table** | Closes one instance and answers nothing about the class, which is what makes #330 a design ticket. It also leaves the ticket's fourth decision — *whether the orchestrator's acts should be enumerated anywhere at all* — untouched, and that decision's own condition, *"unless something reads it"*, is satisfiable for the cost of one test | **rejected** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The nineteen-row table in a new `## Orchestrator: which of these acts runs itself` section of `skills/implement/orchestration.md`, and `tests/test_every_orchestrator_act_names_its_delivery.py` holding it against both files from both sides | The new test, shown red first four ways (a heading with no row; a row naming a heading no file carries; a row naming `bin/does-not-exist`; a `still a sentence` row with empty grounds) — acceptance A1–A4 | `61cd0dad` — twenty rows, not nineteen: the section holding the table is itself a marked heading, which this row's own bullet in `spec.md` anticipated. `phases/phase-1.md` §*What this phase found* has the measurement |
| 2 | `session_cost.py --post`, with `--says` and `--label`, implementing the four label states and refusing to open an issue; `tests/test_session_cost_post.py` with `gh` stubbed | The new test, red first against the unimplemented mode — acceptance A5–A9 | `598663e7` — five states, not four: the lookup that could not run is a fact about the machine rather than the tracker, and it no-ops. `phases/phase-2.md` §*What this phase found* has the grounds |
| 3 | `skills/verify/SKILL.md` §*Measure the segment* names the command in place of the steps it replaces; the phase-1 table's row for that act flips to the command **and** keeps the sentence that nothing makes it run; `changelog.md` and the ledger fragment | Acceptance A10 and A11; the survivor sweep and `evidence-check` at the pull request | `c58a05b4` — there is no row to flip: that act's heading carries no marker and its file is not one the row rule reads, so the sentence went into the table's section as prose. `phases/phase-3.md` §*What this phase found* has the grounds and names the follow-up |

Phase 1 comes first because it is what makes phase 2's row exist to flip, and
because it is the phase that answers the ticket. Phase 2 is the smaller of the
two and depends on nothing in phase 1 but the row.

**Where this work's fragments go**, because this repository overrides the
plugin's default: the changelog entry is
`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/changelog.md`, never
an append to `CHANGELOG.md`; every ledger row is
`seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md`, never an
append to `seal/ledger.md`. No two work items share an id, so no two branches
share a file.

## Operational impact

- **No migration, no env var, no dependency, no compatibility break.**
- **`--post` is the plugin's first arm that writes over the network.**
  `CONTRIBUTING.md` counts the plugin's network touches and names the existing
  two as allowed exceptions — `uvx ruff`'s fetch and `version-check.py`'s
  `git ls-remote`. This one differs in kind: it writes rather than reads. Three
  things keep it honest and all three are in scope — it runs only when typed,
  it writes only through the `gh` binary the session already holds, and it
  posts only text a person handed it. It fires on no hook and no schedule. The
  pull request body states this, because it is the change a reviewer of this
  branch has to judge.
- **Prompt budget: zero.** Nothing here asks anybody anything, on any path.
  Nothing lands under `hooks/`, so no gate's question count moves.
- **Failure direction, for `--post`:** it refuses rather than posts. A wrong
  refusal costs one reading a person can post by hand, which is what they do
  today. A wrong post writes into a repository's issue tracker, where the
  repair is a person deleting a comment.
