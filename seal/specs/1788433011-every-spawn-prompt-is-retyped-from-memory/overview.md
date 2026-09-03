# 1788433011-every-spawn-prompt-is-retyped-from-memory — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the goal a design is chosen against; fragments, never
             the shared file), `CONTRIBUTING.md` §What a change to a gate must
             carry, `docs/review-handoff-protocol.md` §§385–467, issue #107 and
             its two comments, this work item's `routing.md`
· evidence: `seal/ledger/1788433011-every-spawn-prompt-is-retyped-from-
             memory.md`, ten rows (L1 the single home · L2 the 15-word
             window and both measured bounds · L3 the protocol as a pointer
             · L4 the two orchestrator lines · L5 the rule the pointer
             deleted · L6 the record-language instruction's two homes · L7
             the probe rules as §7/§8 · L8 the contract-override refusal as
             §3 · L9 the batching rule as §10 · L10 the `seal/…` root
             sentence as §16). L6–L10 are the direct replacements for the
             five rows `seal/ledger.md` gave up when this branch's last
             commit (`5f5d071`) removed them. Twenty-three coordinates,
             all OK — `evidence_check.py` exit 0
· verified: read — every coordinate named in `plan.md`'s Technical context.
             executed — `$CLAUDE_PLUGIN_ROOT` is unset in this subagent;
             `tests/test_the_handoff_before_round_one.py` passes at 623487f
             (9 passed)

## Why this work exists

Half of every spawn prompt was identical to the last one and was retyped from
memory, so a rule that failed to be recalled went missing with nothing
recording that it had; this work moves the universal half into one file every
agent reads and each agent's own half into its own definition, leaving the
prompt holding only what is specific to the round.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The contract's home | #107 item 1 says `docs/agent-contract.md`, beside `docs/review-handoff-protocol.md` | raised as Q1 rather than built | `tests/test_the_release_check_watches_what_ships.py:52` classifies `docs` as `STAYS_HOME` — *"None of it reaches a user through the plugin"* — which an agent reading it at runtime contradicts; and `$CLAUDE_PLUGIN_ROOT` was measured unset inside this subagent, so the path an agent would resolve is not one this work can promise. A ticket is a request, not an authority (`implement` §1) |
| Which layer *no writes into `rounds/`* belongs to | #107's own table puts it in the right-hand column as universal; its comment's Layer 2 puts it under the warden | split: the general form (*you return a report; you write no durable record*) is universal, the warden's instances stay in `agents/warden.md` | the issue contradicts itself, so the split had to be decided rather than copied. The general form is what a fourth agent inherits; `rounds/` and the review mark exist only for one agent |
| What phase 1 touches | `plan.md`'s phase-1 row names the contract, its test and the wrap list | both READMEs' skills row edited too (22 → 23, on-demand 11 → 12, `agent-contract` listed) | `tests/test_chain_hooks_hardening.py` derives the README's skill count from the `skills/*/SKILL.md` glob, so a new skill is red in both editions until the row moves. Phase 2 moves the name again, into the agents column, and the preloaded group becomes five — a spelling that test does not yet carry |
| The opening line's first clause | `spec.md` decided *Read the agent contract before your first tool call* | rewritten to *The agent contract binds you, and you already have it* — `agent-contract` is in the `skills:` list above, so it arrived at startup | Q1 answered B′, where nothing is read and no path is resolved. An imperative to go and read it describes a delivery this work item measured and did not build, and it contradicts the contract's own first paragraph — *You received this file at startup*. `spec.md` carries the new text, so the decided sentence and the three definitions are one string, which is what `test_every_agent_reads_the_contract.py`'s identity case holds them to |
| What a pin is | `plan.md` phase 1: *one phrase per section that cannot survive the drift it guards* | the pin is a sentence from the section's BODY, matched inside that section only; the heading is excluded by construction | the first draft pinned eight headings, and the move check was red for the wrong reason: a heading that outlives its rule satisfied the pin. `tests/test_the_agent_contract_holds_the_universal_rules.py`'s docstring records it |
| Where the `seal/…` root rule lives | `spec.md`'s universal table has no row for it, and phase 1 declined to add a section because the split is decided in the spec rather than by an implementer | **contract §16**, appended as the next number; `agents/warden.md` gives its copy up | §11 is already in the contract and sends an agent to `config.md` *under the `seal/` root* without saying where the root is, so the contract could not be followed as it stood. The rule needs no per-role exception, which is the universality test the contract applies to itself. And the definition that carried no copy — `agents/scribe.md` — is the one that reads `seal/parity.md` through `legacy-parity`, which is §11's own missing-copy failure one file over. `spec.md` is left as written: a divergence row is how a difference between spec and tree is recorded, and editing the table would erase the thing being recorded. Phase 4 follows this for `agents/smith.md` |
| §9's account of what the gate counts | phase 1 condensed the two agent paragraphs into §9 | the phrase *command position* restored, with the sentence that a whole fixture file is clean and a fragment of one is not | found by re-pointing `test_edits_go_through_the_edit_tool.py` at the contract: the case went red because the condensation had dropped the half that explains why only some fragments trip. Without it a reader cannot apply the command-word rule to their own patch |
| The warden's paste-ready fix | `agents/warden.md` said *a paste-ready fix for blocking items* | *each 🔴 and each 🟡* | narrower than the format the same sentence points at. `skills/code-review/SKILL.md:345` makes 🟡 *fix or justify* rather than blocking, and `:351` already asks for a paste-ready fix for both — read, this session |
| What §7 and §8 cost the smith | phase 3's handover, and this phase's prompt, list §7 and §8 among the sections `agents/smith.md` gives up | nothing was removed for either | the file never carried them. `spec.md`'s universal table names both as living in `agents/scribe.md` and `agents/warden.md`, and its own line for §7 says *"The smith writes probes too, and nothing says so anywhere"* — which is the missing-copy failure, not a duplicate one. The move is still real for the smith: §7 and §8 now reach it at startup, where before this work nothing did. Recorded because a handover naming nine sections and a diff removing seven reads as an unfinished phase |
| Which module phase 4 had to fix | `plan.md`'s phase-4 row names six test modules and does not name `tests/test_the_handoff_before_round_one.py`; phase 5's row does | phase 4 re-pointed two of its cases | that module asserts the smith's copies of §5 and §10, so phase 4's removals are what break it — a row cannot be left red for a later phase to find. Phase 5 still owns the module's protocol-side cases, which this phase did not touch. The plan's per-phase module lists are an estimate written before the moves; the rule that decides what to run is *every module the diff can break* |
| Nothing tested that a moved rule LEFT | `plan.md`'s *What breaks in six months* says the defence is the numbering rule plus *"a test asserting a moved sentence is re-pointed, never duplicated, so two copies of a rule show up as two cases asserting the same phrase in two files"* | a new module, `tests/test_a_moved_rule_leaves_its_definition.py`, checking every section against every definition | the stated defence needed somebody to notice two cases asserting one phrase, which is a reading rather than a check. Measured by the orchestrator at `e51fd0b`: §9's body pasted back into `agents/warden.md` left `test_broad_gate_rule`, `test_edits_go_through_the_edit_tool`, `test_every_agent_reads_the_contract` and `test_the_agent_contract_holds_the_universal_rules` all green — 81 passed, exit 0 — because every assertion in the two new modules is a presence check. Re-measured this phase and confirmed green under the same paste. Q2 answered `full`, and half of `full` had nothing behind it |
| The two wording splits phase 3 left | the contract says *Two reasons point the same way* where `agents/smith.md` said *for two reasons that point the same way*; contract §3 says *ask* where the smith said *ASK* | both settled by removal, not by choosing a spelling | each split existed only because two files stated one rule, which is the state Q2 answered `full` to end. §9's sentence and §3's are the contract's alone now, so there is no second spelling to reconcile. The first split was costing something measurable: with two carriers, `test_edits_go_through_the_edit_tool.py` could pin only the shared fragment *point the same way*, and a rewrite that kept the fragment while losing the count would have passed. Phase 4 tightened it to the whole clause. The second cost nothing — nothing pinned `ASK` in either spelling — and it now has one home in lower case |
| A file outside phase 4's scope | phase 4 is `agents/smith.md` and the new duplication case | `tests/test_every_agent_reads_the_contract.py:161` edited too, one docstring line | `.github/workflows/test.yml:25` runs `ruff check .` over the whole tree, and phase 2 shipped `Q1 answered B′` in that docstring — U+2032 PRIME, which `RUF002` reads as an ambiguous character. The branch has failed that CI step since `8188f12` and nothing in the phase-2 or phase-3 verification would have caught it, because both ran pytest only. It is this work item's own defect rather than one that predates the branch, so the rule about a pre-existing failure does not apply: left alone it fails this work item's pull request. Fixed as one line, with the answer written out and the records' spelling named beside it |
| One rule the pointer would have deleted | `spec.md` puts *mutation-test every unit added, one at a time, before handing over* in the smith's own layer, and phase 5's job is to remove the protocol's interim list | the list is removed; the rule goes to `seal/follow-up.md` rather than into `agents/smith.md` | measured at `28a1400`: the protocol's `:440` was the only statement of it anywhere outside `tests/` and this directory. `agents/smith.md` presupposes the practice without mandating it, and contract §15 is the narrower rule about a new case being seen red. So the pointer deletes a rule with no other home — which is #107's own failure arriving from the fix. It is not fixed in place because `plan.md`'s phase-5 row does not name `agents/*.md` and the spawn prompt forbids touching them; a request ranks below the ratified plan and above nothing here, so the phase discloses instead of widening. `tests/test_the_handoff_before_round_one.py` pins the rule's absence from the protocol, which stays true under either repair |
| The section was renamed, not only emptied | `plan.md` and `spec.md` both say §385 *becomes a pointer* and neither mentions its title | `## What every spawn prompt carries, until the definitions carry it` → `## What every spawn prompt used to carry` | the old title asserts an interim state that stopped being true in the same commit, and a heading is what a reader scanning the document acts on. One document named the old title — `skills/code-review/SKILL.md`, whose paragraph told an orchestrator to read that section before writing a prompt — and that paragraph is rewritten in this phase anyway, because what it sent a reader to fetch now arrives without being fetched. The historical mention in another work item's `round-4.md` is left as written: a round record names what it read at the time |
| Where Q4's two lines went | `questions.md` Q4 says *one line in each of those two skills* and does not place them | `skills/implement/SKILL.md` immediately under the intro line; `skills/code-review/SKILL.md` inside *Orchestrator: a fix pass resumes the implementer*, replacing the paragraph that pointed at the removed section | the two skills are read differently. `implement` is loaded whole by a session that is about to build, so the binding belongs where the file says who loads it. `code-review` already had a paragraph about what a spawn prompt carries, and leaving it pointing at a section that no longer holds the rules would have been the one stale reference this phase created. Both are worded as pointers: neither states an exit-code form, a broad-gate boundary or a label, and the longest run either shares with any contract section is 8 words against the 15-word window `tests/test_a_moved_rule_leaves_its_definition.py` measures |
| Where the smith's prose maximum landed | the `seal/follow-up.md` row phase 3 left open, on whether the scribe and the smith join `tests/test_docs_line_wrap.py`'s `COVERED` | left open, unchanged | phase 3's argument holds and this phase strengthens it in one direction only. `agents/smith.md` lost eight long paragraphs, so its prose maximum fell — but adding a path to `COVERED` changes what a test guards, which `CONTRIBUTING.md` asks a separate argument for, and the two definitions were deliberately paired so that doing one alone reads as an oversight. The row still names both, and it is still the right shape |
| A rule this work item deleted | `spec.md`:90 puts *mutation-test every unit added, one at a time, before handing over* in the smith's own layer; phase 4 did not move it and phase 5 removed its only home, filing a `seal/follow-up.md` row | restored to `agents/smith.md` in that file's own words, pinned by a case in `tests/test_the_handoff_before_round_one.py`, and the follow-up row removed | the home was decided in `spec.md` and never open, so a row naming the repository owner was a question nobody had to answer — and `seal/follow-up.md`'s own preamble asks that every row name a person with **no condition attached**, which an item with a written answer and a written home does not. Where it went is the smith's Verify step, because the act is a verification and its timing is the handover. Measured against every contract section before writing: the longest run it shares with any is 10 words, the bound `test_a_moved_rule_leaves_its_definition.py` recorded at phase 4, and it creates no 15-word copy. §15 is named in the prose as the neighbour it is not, because *a new case is seen red* and *every unit added is broken* read as one rule until someone puts them side by side |
| Why the pin sits beside an absence check | nothing in `plan.md` or `spec.md` places it | `tests/test_the_handoff_before_round_one.py`, immediately under `test_the_protocol_no_longer_states_the_rules_it_points_at` | that case asserts five phrases have LEFT the protocol and names, for each, the file that now carries it. Four name contract sections, which `test_the_agent_contract_holds_the_universal_rules.py` pins from the other side. The fifth named `agents/smith.md` and nothing pinned it, so the case went green over a rule that had left the repository altogether. The general claim is that an absence check with no presence check beside it cannot tell a rule that MOVED from a rule that was DELETED, and it is written into the new case's docstring and into ledger row L5 rather than left in this memo alone |
| Phase 5's measurement of its own two lines | this memo's phase-5 row says *the longest run either shares with any contract section is 8 words against the 15-word window* | **4 words**, re-measured this phase | the claim is a number a later session would take rather than re-derive, so it was re-run before being written into ledger row L4. Each added paragraph's longest run against any section is 4. The conclusion phase 5 drew is unchanged and the margin is wider than it claimed; what changed is that the number in the ledger is one that was measured rather than one that was inherited |
| What the same re-measurement turned up | `spec.md` scopes the single-home rule to the three agent definitions, and Q2 answered `full` for those | left alone, recorded under *Not done* and in L4's notes | measured over the WHOLE of `skills/implement/SKILL.md` rather than the paragraph phase 5 added, the file shares a 30-word sentence with contract §5 — the aggregate-is-not-a-coordinate sentence. It predates the contract, no case is red, and bringing the skills under the definition check is a change to what a test guards, which `CONTRIBUTING.md` asks a separate argument for. Recorded because the next reader who measures the file rather than the paragraph finds the same 30 and has no way to tell it was seen |
| Q4's own edit drifted a pre-existing ledger row | phase 5 inserted the two orchestrator paragraphs into `skills/code-review/SKILL.md`'s *Orchestrator: a fix pass resumes the implementer* section, and `seal/ledger.md` already anchored an unrelated, older claim — *a fix pass is obtained by resuming the implementing session* — to that whole section by content hash | re-verified: `evidence_check.py . --ledger seal/ledger.md --reverify` recomputed that row's hash (and, in the same pass, a second pre-existing drifted row's, `tests/test_no_document_names_the_old_roots.py#KEEP`, unrelated to this branch) | the underlying claim still holds — nothing the row cites was removed, only the section's hash changed because new prose was inserted inside it. `--reverify` has no per-row scope, so it recomputed every drifted row in the file in one pass; confirmed the diff touched exactly those two rows (`git diff --stat`: 3 lines changed) and nothing else. Before: `seal/ledger.md` 411 ok · 2 drifted (this row and the pre-existing one) · 0 broken, `--strict` exit 2. After: 413 ok · 0 drifted · 0 broken, `--strict` exit 0. The fragment (`seal/ledger/1788433011-….md`) was untouched throughout, 23 ok · 0 drifted · 0 broken both before and after |
| `docs/flow.md`'s roadmap restructuring rode this branch | none of `spec.md`'s Scope table, `plan.md`'s six phases, or this file names `docs/flow.md` | `96aa3d2` and `28a1400` move issues between milestones and add a milestone carrying #30, #84 and #120; `e0d3d27` is unrelated to milestone structure — it answers this work item's own Q1–Q4 batch and corrects a technical claim in the same 0.6.0 section (marketplace clone vs. version cache) that the Q1 probe found wrong | orchestrator bookkeeping, decided in conversation with the repository owner as GitHub milestones were restructured. `96aa3d2` predates phase 1 (it narrows 0.6.0 to #107 before any phase measurement exists); `28a1400` follows phase 4 and is grounded in its own stated reason — the contract's §2/§6 conflicting with the two agents 0.8.0 adds — not the phase-2 CI-lint miss or phase-split cost data. No phase's Verified-by column covers any of the three, and none should: none changes a test, a code path, or an agent's behavior |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite and typecheck at this branch head | the orchestrator, once, after the review rounds settle |
| ✅ The repository-wide lint and format check | re-run in phase 6 at the phase-6 tree — `ruff check .` exit 0 (*All checks passed!*) and `ruff format --check .` exit 0 (*88 files already formatted*). **This is wider than `plan.md`'s per-phase scope allows**, which says no phase runs the repository-wide lint, and the spawn prompt asked for it: run and disclosed rather than run quietly, which is the failure contract §3 names. The grounds are phase 4's finding — the branch failed CI's lint step for two phases because three consecutive verifications ran pytest only — and the cost is under two seconds. Phase 6's own Python diff is one file and it is clean narrowly too. Before that, re-run in phase 5 — `ruff check .` exit 0 (*All checks passed!*) and `ruff format --check .` exit 0 (*88 files already formatted*). First run in phase 4 — both exit 0 at `4b85d80` plus the phase-4 doc commit. This was a widening of phase 4's stated scope and it is recorded rather than left to be inferred: the narrow run over the seven changed files came first and was clean, `ruff check tests/` was the run that surfaced the phase-2 `RUF002`, and `ruff check .` confirmed the fix. The seal is void the moment anything edits, so the orchestrator's one broad run still stands as owed |
| That a `skills:` frontmatter entry preloads for a **newly added** skill name in an installed plugin build (observed only for skills that already ship) | the orchestrator, with `/reload-plugins` and one spawn once this branch is installed. Phase 2 could not: the copy in force is the 0.5.0 version cache, which holds no `agent-contract/` at all, and neither a reload nor a spawn is an agent's to make |
| ✅ That `$CLAUDE_PLUGIN_ROOT` is unset for every agent kind and not only this one | moot — Q1 answered B′, and phase 1 (37f8c11) reads no path |
| That the user's `/` menu omits `agent-contract` under `user-invocable: false` (the experiment's stated gap; the cost if not is a listed entry nobody should run, not a contract that fails to arrive) | the repository owner, at the first 0.6.0 install |

## Not done

- **`agents/scribe.md` does not load `writing-style`.** It is the only agent
  without it, and its report is prose a person reads. Out of #107's scope and
  left deliberately rather than folded in — it is a change to what a third
  agent reads, and this work item is already changing that surface for all
  three. It belongs in its own item so its own review round can judge it.
- **`agents/smith.md` and `agents/scribe.md` are not brought under
  `tests/test_docs_line_wrap.py`.** Their prose maxima are 148 and 160
  columns; bringing them under is a sweep that would bury this diff. The
  contract itself is written wrapped and joins `COVERED` at birth.

  Phase 3 measured the ground under that sentence and it has shrunk. After
  the move `agents/scribe.md` has exactly **one** prose line over the limit
  (`:22`, 160 columns) — not a sweep, a rewrap. `agents/warden.md` is already
  covered and its two long lines are table rows, which the check excludes.
  The decision still stands, for a different reason than the one `spec.md`
  gave: *at birth* is the precedent for a file written wrapped from its first
  line, this file is not being born, and adding a path to `COVERED` changes
  what a test guards — which `CONTRIBUTING.md` asks a separate argument for.
  Doing it for the scribe while `agents/smith.md` stays out would also read
  as an oversight rather than a decision. The row is in `seal/follow-up.md`
  so the two definitions can be taken together, once.

  Phase 4 closed the measurement the row was waiting on. `agents/smith.md`
  keeps **two** prose lines over the limit (`:22`, 148 columns; `:95`, 109),
  both of them older than this work item and neither of them in a paragraph
  phase 4 touched — the eight paragraphs it removed were already wrapped.
  Three lines across the two files is a rewrap, so the size argument
  `spec.md` gave is spent and the row now rests only on the second reason
  above. That is deliberate rather than an omission: this branch is already
  changing what all three agents read, and folding a change to a test's scope
  into it buries the argument `CONTRIBUTING.md` asks for. The row's answerer
  is now the repository owner with no condition attached, which is what
  `seal/follow-up.md` requires of every row.
- **The contract and `skills/implement/SKILL.md` still share a 30-word
  sentence.** Measured this phase over the whole skill rather than the
  paragraph phase 5 added: §5's *is not a coordinate: the number can be
  checked while the claim it stands for cannot, and one such fact reached
  five documents before a review round found it false* stands in both files.
  Nothing is red — Q2 scoped the single-home rule to `agents/*.md`, and
  `tests/test_a_moved_rule_leaves_its_definition.py` globs that directory
  alone. Left because widening that glob to `skills/*/SKILL.md` changes what
  a test guards, which `CONTRIBUTING.md` asks a separate argument for, and
  because the skills are procedures a session loads rather than definitions
  an agent is spawned with — whether the same rule applies to them is the
  argument, and it is not this work item's.
- **The presence-beside-absence rule is not a contract section.** It is
  written into a docstring and a ledger row instead. Making it §17 would
  change what every agent reads, on the strength of one measurement, in a
  branch already changing that surface for all three of them.
- **`chain_check.py` gains no required field.** That is #119's, and it is a
  change to a gate needing the argument `CONTRIBUTING.md` asks for.

## Fed back into the spec

Three clauses this work added that `spec.md` did not decide. Each is marked
**inferred during implementation**, which is a planner's permission to
overturn it: none of the three was argued in front of a person before it was
built, and each was settled by a measurement or by a document that turned out
to be already binding.

| Clause | Where it now lives | Inferred from |
|---|---|---|
| **The contract carries §16, where a `seal/…` path resolves.** `spec.md`'s universal table has no row for it | `skills/agent-contract/SKILL.md` §16 | §11 sends an agent to `config.md` *under the `seal/` root* and never says where the root is, so the contract could not be followed as it stood. Two definitions carried the sentence and the third — the one that reads `seal/parity.md` — carried none, which is §11's own missing-copy failure one file over. Phase 1's divergence row above holds the argument |
| **The duplication check is a 15-word verbatim window, with both ends of its margin asserted.** `plan.md` said the defence was *the numbering rule plus a test asserting a moved sentence is re-pointed, never duplicated* — which needed a person to notice two cases asserting one phrase | `tests/test_a_moved_rule_leaves_its_definition.py`, and ledger row L2 | the stated defence was a reading rather than a check, and the orchestrator's paste at `e51fd0b` proved it: four modules green under §9 pasted whole into a definition. The number is measured at both ends — 10 words is the longest legitimate shared run, 25 the smallest real duplication — because a window chosen by taste is one a later edit widens to quiet a failure |
| **An absence check needs a presence check beside it.** Nothing in either document says so, and this work item is the case that proves it | the new case's docstring in `tests/test_the_handoff_before_round_one.py`, and ledger row L5 | phase 5 asserted a rule had left the protocol without anything asserting it had arrived anywhere, and the rule was gone from the repository for two commits with a green suite. Written as a claim rather than as a contract section: making it §17 changes what every agent reads, which is a change to a gate's neighbourhood needing the argument `CONTRIBUTING.md` asks for, and this work item is already changing that surface for all three agents. Named in the pull request body so the decision is somebody's rather than nobody's |
