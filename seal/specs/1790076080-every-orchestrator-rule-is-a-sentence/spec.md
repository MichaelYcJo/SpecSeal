# Feature Specification: every orchestrator rule is a sentence

<!-- seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

#330. Every rule that reaches an agent is delivered by mechanism — the `skills:`
frontmatter, injected at startup before the first tool call, with nothing typed
and no path to resolve. Every rule that reaches the orchestrator is a sentence
it has to remember, because the orchestrator has no spawn for a preload to
attach to.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between two designs that catch the same thing, the one that stops to ask is the more expensive. It is why the mechanism this work ships is a command and not a gate, and why no arm here adds a prompt |
| `skills/implement/SKILL.md` §1, *the cost of a question is not its difficulty, it is when it arrives* | The same clause one level up: a procedure a session reconstructs from a hundred lines of prose at minute ninety costs what a late question costs. Collapsing it into a command is the same saving |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Governs anything under `hooks/` or `.github/workflows/`. **Nothing this work ships lands in either**, and the section is cited to record that the obligation was read and found not to apply — the rejected alternative that would have triggered it is in `plan.md` |
| `skills/agent-contract/SKILL.md` §6 — *post nothing* | Withheld from every agent whatever its definition says. So the act this work arms is structurally the orchestrator's and can never be delegated to an agent, which is what makes it the right subject |
| `skills/agent-contract/SKILL.md` §12 — a defect belongs to a class, enumerate the class | The class here is *the orchestrator's acts*. This work enumerates it by construction rather than by listing what comes to mind |
| `skills/agent-contract/SKILL.md` §15 — a new case is not planted until it has been seen red | Both phases' cases are shown failing first |
| `CLAUDE.md` §*A change writes fragments, never the shared file* | The changelog entry goes to `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/changelog.md` and every ledger row to `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | *The orchestrator's acts*, never *the acts*; and the word `arm` is left to the meaning `arm_check.py` and the commit gate already give it. This work's word is **delivery** |
| `docs/one-root-by-lifetime.md` — three lifetimes | The enumeration is procedure, so it lives in a skill file rather than under `seal/` or in `docs/` |

## What the tree settled, so nobody reopens it

The ticket was raised on 2026-09-10 and lists three acts with a measured miss.
**Two of them have since been closed, by two different shapes**, and the
ticket's framing does not know it. Opened and read:

| The act | State today | Coordinate |
|---|---|---|
| take the broad gate | **closed** — it is one command a named agent types, and which arms it runs is declared rather than remembered | `skills/verify/scripts/broad_gate.py`, `bin/broad-gate`, `agents/sealer.md`; the declared-arms property is `broad_gate.PARTITION` |
| ask the routing question in one batch | **closed** — the question's exact shape reached the delivery channel that arrives in every session with nothing typed, and a check reads the answer at the pull request | `templates/claude-md-block.md`, added by `5bb975ee` on 2026-09-16, six days after the miss the ticket measures; `hooks/routing.py`, `skills/code-review/scripts/chain_check.py` |
| post the segment's reading to the flow log | **open. Still a sentence.** | `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* |

A second coordinate says the same thing from a different work item:
`seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/spec.md`
§*Out* names *"the rest of #330 — the broad gate's spelling, posting a
segment's reading to the flow log, asking the routing question in one batch"*.
Two of that list of three are gone.

**Three more judgments the tree answered, recorded so they are not re-argued.**

1. **Delivery is not the missing half.** #343 — closed and shipped — is two
   review rounds spawning agents against §6 with §6 in their payload, in the
   work item that rewrote §6. The rule arrived by mechanism and the act went
   the other way. So the repair the repository has actually measured is not
   *deliver the sentence better*, it is *take the act away from memory*. The
   ticket's title names delivery; its evidence names performance.
2. **Neither of the ticket's first two shapes won.** The broad gate became a
   command; the routing question became a channel plus a check. The act's own
   nature decided each. So *a command per act* and *one command with
   subcommands* is a false choice, and this work item does not settle it —
   it records that the question was wrong.
3. **The class is enumerable by construction.** Every act addressed to the
   orchestrator sits under a heading carrying the `Orchestrator:` prefix, in
   one of two files, and that marker is already a rule rather than a
   convention — `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`
   derives the agents and their preloaded files and fails when a marked
   heading reaches one, at `##` and `###` both. Counted 2026-09-22:
   `skills/implement/orchestration.md` has 4 marked `##` headings with 3 `###`
   beneath them, and `skills/code-review/orchestration.md` has 5 with 7. **The
   orchestrator has nineteen acts and no list of them.**

## Scope

**In. Two things ship, and the second is the smaller.**

1. **The orchestrator's nineteen acts are enumerated, each against its
   delivery, and a test holds the table against the tree from both sides.**
   - The table lives in a new `## Orchestrator: which of these acts runs
     itself` section of `skills/implement/orchestration.md` — which makes the
     section a row of its own table, and keeps it out of every agent's payload
     by the marker rule above.
   - One row per heading, keyed by the heading text. The row set is *every `##`
     heading whose text begins `Orchestrator:` in either orchestration file,
     plus every `###` heading directly beneath one*.
   - Each row's `Delivered by` cell holds one of four values and nothing else:
     a **command** (named, and it must exist), a **check** (named, and it must
     exist), **part of its parent's act**, or **still a sentence** — the last
     carrying grounds in its own cell.
   - `tests/test_every_orchestrator_act_names_its_delivery.py` fails when a
     marked heading has no row, when a row names a heading that is not in
     either file, when a row names a command with no `bin/` entry, or when a
     row names a check with no file. Red-first against the table with a
     heading removed and against a row naming a command that does not exist.

2. **The one act of the ticket's three that is still a sentence gets a
   command**: `session_cost.py` gains a `--post` mode that resolves the right
   measurement log, applies the invariant the prose states, and posts the
   reading as a comment.
   - It refuses to post without a reading. The numbers are the script's; *what
     they say* is the orchestrator's judgment, and a command that invented one
     would be posting a sentence nobody wrote. `--says -` reads it from stdin.
   - It resolves the label rather than a number, and implements all four states
     `skills/verify/SKILL.md` already enumerates: no history at all (silent
     no-op, exit 0), a history with nothing open (name it, post nothing, exit
     non-zero), exactly one open (post), more than one open (name it, post
     nothing, exit non-zero).
   - **It never opens an issue.** The skill says opening one is not a session's
     act, and a command that opened one would break the same invariant from the
     other side.
   - `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*
     names the command in place of the steps it replaces.

**Out, with the grounds beside each.**

- **Every act the table will mark *still a sentence* except the one above.**
  The ticket's own answer to *which acts get one*: only those with a measured
  miss, because *"the rest are unmeasured, and building for them is building
  for a guess"*. The table is what makes the next one findable; closing them is
  not this branch's.
- **A `PostToolUse` notice at a segment boundary.** It is the one shape that
  would make the measurement happen rather than making it cheaper, and it is
  rejected on cost: deciding whether to print requires knowing the repository
  has an open measurement log, which is a network call, and putting one on the
  hot path of every spawn is a price paid on every run for a reminder. In
  `plan.md`'s alternatives with its failure scenario.
- **Anything that stops the orchestrator.** The ticket's own *Not this*, and
  `CLAUDE.md`'s first goal. Nothing here lands under `hooks/` or
  `.github/workflows/`, so §*What a change to a gate must carry* has nothing
  to judge.
- **Another sentence delivered by a `SessionStart` line or a bigger `CLAUDE.md`
  block.** Both channels exist and both already carry orchestrator rules. The
  routing rule was in the block and the ticket's own §*Not this* refuses a
  seventh document. Recorded in `plan.md` so the channel is not rediscovered as
  though it were new.
- **Settling *command per act* against *one command with subcommands*.**
  Judgment 2 above: the observation is that the act's nature decided, twice,
  and there is nothing left to choose between.
- **Every other hygiene step** — issue claims, the version bump, the changelog
  and ledger folds, `unverified_check`, `survivor_check`, release completeness,
  `seal mode`, the `CLAUDE.md` block, both READMEs. Named as out by
  `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/spec.md`
  on the same grounds, and that reasoning is not re-argued here.
- **`round_record.py new` committing the record itself.** Deferred with written
  grounds in
  `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/plan.md`
  — `new` returns `run_check`'s exit code and that code is legitimately
  non-zero mid-run. It stays deferred.
- **Promising a saving.** Nothing here claims fewer tool calls or a shorter
  run. The one clause of this class that was measured came out flat, and a
  number nobody has produced is the counterfeit `CONTRIBUTING.md` refuses.

## The limit this work does not close, stated rather than left to be found

**A command does not make anybody run it.** The miss the ticket measured for
the flow log is that the meter *"sat unreferenced through a full day of
measurements nobody took"* — the measurement was not taken, not that the
posting failed. `--post` removes the hundred lines of prose a session
reconstructs each time; it does not remove the remembering. The table's row for
that act must therefore read its delivery as the command **and** say that
nothing makes it run, so the next work item inherits a true statement rather
than a closed-looking one.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 The class is complete | Given both orchestration files · When the test runs · Then every `##` heading beginning `Orchestrator:` and every `###` beneath one has exactly one row | `tests/test_every_orchestrator_act_names_its_delivery.py`, red-first with one heading's row deleted |
| A2 The table cannot outlive a rename | Given a row naming a heading no file carries · When the test runs · Then it fails naming that row | same test, red-first with a heading renamed in a temp tree |
| A3 A named command must exist | Given a row whose `Delivered by` names a command · When the test runs · Then it fails unless `bin/<name>` exists | same test, red-first with a row naming `bin/does-not-exist` |
| A4 `still a sentence` carries grounds | Given a row whose delivery is `still a sentence` and an empty grounds cell · When the test runs · Then it fails | same test, red-first |
| A5 The flow-log post refuses without a reading | Given `--post` with no `--says` · When run · Then exit non-zero, nothing posted, and the refusal says where the reading comes from | `tests/test_session_cost_post.py`, exit code read directly per contract §1 |
| A6 No open log is not a failure | Given a repository whose `flow-measurement` label has no history · When `--post` runs · Then exit 0, nothing posted, and it says the repository does not run this log | same test, `gh` stubbed |
| A7 A closed log is named, not reopened | Given the label has a history and nothing is open · When `--post` runs · Then exit non-zero, nothing posted, nothing opened, and the message says opening one is not a session's act | same test, `gh` stubbed |
| A8 More than one open is named | Given two open issues carry the label · When `--post` runs · Then exit non-zero, nothing posted, both named | same test, `gh` stubbed |
| A9 Exactly one open posts once | Given one open issue carries the label and a reading is supplied · When `--post` runs · Then one comment is posted to that issue and exit 0 | same test, `gh` stubbed, asserting the `gh` argv |
| A10 The skill names the command | Given `skills/verify/SKILL.md` §*Measure the segment* · When read · Then it names `session-cost … --post` in place of the steps it replaces | `tests/test_docs_*` and the survivor sweep at the pull request |
| A11 Nothing lands in a gate | Given the branch's diff · When read · Then no file under `hooks/` or `.github/workflows/` is touched | `git diff --stat origin/release/... ...HEAD -- hooks .github/workflows` is empty |

## Data & interfaces

**No schema, no endpoint, no payload.** Two surfaces change:

- `skills/implement/orchestration.md` gains one `## Orchestrator:` section
  holding a markdown table of nineteen rows, columns `Act` (the heading text),
  `File`, `Delivered by`, `Grounds`.
- `skills/verify/scripts/session_cost.py` gains one mode. Its interface:
  `session-cost --segments <transcript> --post --says <path|->`, plus
  `--label <name>` defaulting to `flow-measurement` so the durable
  `flow-baseline` log is reachable with the same code.

Neither adds a network call to any path that runs unasked. `--post` is the
plugin's first arm that WRITES over the network, and it writes only when typed,
only through `gh`, and only what a person handed it. `CONTRIBUTING.md` counts
the plugin's network touches; `plan.md` §*Operational impact* states this one.

Ledger rows this work adds go in
`seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md`, anchored on
content the way every row is.

## Open questions → questions.md

Three rows, none of them blocking, and each says why the tree could not answer
it. The run is `automation`, so no row waits for a person: see `questions.md`
for which judgments the tree DID settle.

<!-- The framer's mark. `<who>` matches routing.md's `Planning` row. -->

Framed 2026-09-22 by framer, before the build.
