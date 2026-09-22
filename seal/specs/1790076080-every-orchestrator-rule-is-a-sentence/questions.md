# every orchestrator rule is a sentence — questions for the planner

<!-- seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. -->

**The run is `automation`: nobody is asked anything.** Every row below names
what it would take to close it, and every row carries a default that continues.

## What the tree answered, so nobody reopens it

The ticket leaves four decisions open. Three of them the tree settles, and a
reader cannot tell a judgment that was made from a question nobody met — so
they are listed here rather than left silent. The grounds are in `spec.md`
§*What the tree settled* and `plan.md`'s alternatives table.

| The ticket's open decision | Settled how |
|---|---|
| *Command per act, or one command with subcommands* | **Wrongly posed.** The two acts that closed since the ticket was written closed by different shapes — the broad gate became a command, the routing question became a delivery channel plus a check. The act's nature decided each. Recorded rather than answered |
| *Which acts get one* | **Only those with a measured miss**, which is the ticket's own answer. Three had one; two have closed; one is left, and it is the flow-log posting |
| *What the routing question becomes* | **Already closed, by #88.** `templates/claude-md-block.md` carried the question's exact shape from 2026-09-16, six days after the miss this ticket measures, and `chain_check.py` reads the answer at the pull request. Nothing is owed here |
| *Whether the orchestrator's acts should be enumerated anywhere at all* | **Yes, and the ticket's own condition — "unless something reads it" — is met by one test.** The class is enumerable by construction from the `Orchestrator:` heading marker, which is already a rule. Nineteen acts, counted 2026-09-22 |

Two smaller judgments, made from the tree and recorded so the build does not
re-derive them:

- **A `Delivered by` cell may name a `bin/` entry or a script path under
  `skills/*/scripts/`.** Not every command has a wrapper — `bin/round-record`
  exists and `chain_check.py` has none, and #318 was opened for exactly that
  gap. A test demanding `bin/<name>` would refuse a true row.
- **The word is `delivery`, not `arm`.** `arm` already means a gate's branch
  (`skills/verify/scripts/arm_check.py`) and a commit gate's review or parity
  half, and `tests/test_one_word_one_meaning.py` is the check that holds this.

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | In a repository whose `flow-measurement` label has never existed, what does `gh issue list --label flow-measurement --state all` do — exit 0 with empty output, or fail because the label is unknown? Phase 2's four states turn on telling *no history* apart from *a lookup that failed*, and `skills/verify/SKILL.md` describes the distinction without stating the exit code. The framer could not settle it: it is a fact about the `gh` binary's behaviour, not about this tree | **a measurement** — one command against any repository with no such label, about three seconds | (a) exit 0, empty: the no-history state is the empty-output branch. (b) non-zero: the branch must read the message, and a failed lookup and an absent label need separating some other way | **(a)**, with the code written so a non-zero exit falls to *silent no-op* rather than to *post*. The failure direction in `plan.md` already points that way, so a wrong guess costs a refusal and never a wrong post | ⬜ |
| Q2 | For each of the nineteen headings, which of the four `Delivered by` values is true, and what are the grounds for the ones that read `still a sentence`? The framer counted the class by construction from the headings and did not read all 1,048 lines of the two files. Deciding nineteen cells needs those sections read, which is the phase's own work | **the work** — phase 1 reads each section as it writes its row | (a) phase 1 decides each cell with the section open, as it goes. (b) a separate reading pass first, which is the same reading done twice | **(a)**. A cell decided without its section open would be the assertion §5 refuses, so the reading has to happen inside the phase either way | ⬜ |
| Q3 | `--post` is the plugin's first arm that WRITES over the network. `CONTRIBUTING.md` counts the plugin's network touches and names two read-only exceptions. Does a writing one need a row of its own in that document, or is stating it in the pull request body enough? This is a policy-document edit, and `CLAUDE.md` puts policy above the SDD set — the framer may not widen a ratified document on its own reading | **a person** — the repository owner owns `CONTRIBUTING.md`'s exception list | (a) state it in the pull request body and `plan.md` §*Operational impact*, edit nothing: the list keeps being the list of hooks that reach the network, which is what the bullet around it is about. (b) add a `CONTRIBUTING.md` row: a list written for hooks becomes a list of every network touch whatever fires it, and the three conditions the bullet sets for a third entry — an opt-in condition, a throttle, silence on failure — are hook-shaped and would have to mean something else. **Both cells corrected 2026-09-22 in round 1's fix pass**, which found the same misreading here as in the default's grounds: describing the list by what prompts a touch rather than by what it is a list OF | **(a)**. **Grounds corrected 2026-09-22 in round 1's fix pass, after the reviewer opened the section.** They read *the existing two entries are both touches that fire without anybody asking for them — a fetch during lint and a lookup at session start — and `--post` is not one of those*, which generalises the wrong way: a future hook firing only when a person types something would be argued out of a list that exists for hooks. The section's own scoping settles it — the bullet is **Hooks stay local and quiet**, its sentence is *"Two hooks reach the network"*, and the three conditions it sets for a third are hook-shaped. `--post` is not a hook, so the list does not reach it. The answer is unchanged and the reviewer can still overturn it by opening the section | ⬜ |

Answered rows feed back into `docs/` (policy clause or open-questions section)
before this directory's work merges.
