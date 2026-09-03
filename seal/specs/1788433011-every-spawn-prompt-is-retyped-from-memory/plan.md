# Implementation Plan: every spawn prompt is retyped from memory

<!-- seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

Three layers exist today in one place: the spawn prompt. This work moves two
of them out. The universal layer becomes one file every agent reads at spawn
with nothing typed; each agent's own layer moves into its own definition; the
prompt is left holding what is specific to the round.

The work alters what a session reads and acts on, which is the top rung of the
`implement` skill's ladder, so `spec.md` and this plan come before the first
line of implementation and approval of this plan is the gate.

## Technical context

- `docs/review-handoff-protocol.md:385` — *What every spawn prompt carries,
  until the definitions carry it*. It names itself an interim home and names
  #107 as what ends it. Its subsections at `:399`, `:414`, `:432`, `:444` and
  `:462` are the input to the split, and they are prose already agreed rather
  than something this work invents.
- `agents/warden.md:227` — the report format, already half carried.
- `agents/smith.md:82` and `agents/warden.md:50` — the suite prohibition, in
  two files, in near-identical words.
- `agents/warden.md:95` — the measured story of a prompt widening a scope,
  already written down inside one of the two files.
- `agents/scribe.md` step 4 — the probe rules and the git-from-Python rule,
  in a third file, again in near-identical words.
- `tests/test_the_release_check_watches_what_ships.py:52` — `docs` is
  `STAYS_HOME`, *"None of it reaches a user through the plugin"*. This is why
  the delivery vehicle is a question and not an assumption.
- `tests/test_docs_line_wrap.py` — 88 display columns, `COVERED` list, and its
  own stated precedent for a file joining at birth.
- `$CLAUDE_PLUGIN_ROOT` — **measured unset** inside this smith subagent
  (`echo` returned empty, this session, 2026-09-03).

**What breaks in six months.** The contract becomes a file people edit without
re-reading the definitions, and a rule ends up stated in both places with two
different wordings — the same failure one layer up. The defence is the section
numbering rule (a number is never reused or re-ordered) plus the phase-3 and
phase-4 rule that a test asserting a moved sentence is *re-pointed*, never
duplicated, so two copies of a rule show up as two cases asserting the same
phrase in two files.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Copy the invariant lines into each agent definition; no contract file | `agents/warden.md` and `agents/smith.md` each carry the exit-code rule, #84's framer and #30's sealer each need a fourth and fifth copy, and the next one inherits nothing. This is what #107 calls *the duplication just moves* | rejected — it is the failure, not the fix |
| Leave the rules in `docs/review-handoff-protocol.md` and have every prompt cite the section | the rule still reaches an agent only if the orchestrator remembers to type the citation, which is the exact mechanism that lost the exit-code rule for round 1 of one work item | rejected |
| Contract as `docs/agent-contract.md`, read by path at spawn | `$CLAUDE_PLUGIN_ROOT` measured unset in a subagent; a bare path resolves against the user's repository where the file does not exist; and `docs` is declared `STAYS_HOME` by a test whose stated reason stops being true | Q1 option A — buildable, but it needs the release-surface model changed with it |
| Contract as `skills/agent-contract/SKILL.md`, preloaded by frontmatter | it shows up in the user-facing skill listing as though it were an invocable procedure. That is a cosmetic cost against a mechanism already proven by three agents | Q1 option B — the default |
| One contract with per-role sections | two answers to *where does this rule go*, which is the ambiguity the three-layer split exists to remove | rejected in `spec.md` |
| Ship the contract with no test behind the opening line | #107's stated reason for landing before #84 and #30 is that a fifth agent should inherit the contract. Nothing would catch the fifth agent arriving without the line, and the miss is silent | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified. One
smith spawn per phase; this table is the handoff between them.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The contract file at the path Q1 settles, with every universal rule from `spec.md`'s first table as a numbered section, each carrying the measured failure that bought it. §1 is the exit-code rule with both forms written out. Added to `tests/test_docs_line_wrap.py`'s `COVERED`. New `tests/test_the_agent_contract_holds_the_universal_rules.py` pinning one phrase per section that cannot survive the drift it guards | `uvx --with pytest python3 -m pytest tests/test_docs_line_wrap.py tests/test_the_agent_contract_holds_the_universal_rules.py -q` — each new case shown red first by deleting the phrase it pins | 37f8c11 |
| 2 | Every agent definition opens with the contract line — `agents/warden.md`, `agents/smith.md`, `agents/scribe.md`, plus the frontmatter entry if Q1 answers B. New `tests/test_every_agent_reads_the_contract.py`: every `agents/*.md` carries the line, and the contract it names resolves to a file in the tree | `uvx --with pytest python3 -m pytest tests/test_every_agent_reads_the_contract.py -q` — shown red by writing a fourth agent file with no line, and shown red a second way by pointing the line at a path that does not exist | 8188f12 |
| 3 | `agents/warden.md` and `agents/scribe.md` absorb their own invariants and give up the universal ones (Q2). The warden gains the clone rule, the `uv` venv line and the report format completed; both lose whatever phase 1 now holds. Every case that asserted a moved sentence in these two files is **re-pointed at the contract, never deleted**, and each must still be able to fail | `uvx --with pytest python3 -m pytest tests/test_broad_gate_rule.py tests/test_edits_go_through_the_edit_tool.py tests/test_a_probe_that_commits_says_so.py tests/test_absence_claims.py tests/test_handoff_outlives_the_merge.py -q`, plus each re-pointed case shown red against the contract | 2b9d415 |
| 4 | `agents/smith.md` does the same: it keeps the SDD set, the design gate, routing, vertical slices, mutation testing, the hand-back shape and the 3+ Fix Rule, and gives up the universal ones. Its cases re-pointed on the same terms. Plus the gap phase 3's measurement opened: `tests/test_a_moved_rule_leaves_its_definition.py`, holding for all three definitions that a rule moved into the contract did not stay behind — derived from the contract's own sections and the `agents/*.md` glob, so a §17 and a fourth agent are both checked on the day they land | `uvx --with pytest python3 -m pytest tests/test_broad_gate_rule.py tests/test_the_set_a_work_item_always_has.py tests/test_one_word_one_meaning.py tests/test_a_probe_does_not_outlive_its_round.py tests/test_unverified_rows_close.py tests/test_the_last_rounds_fixes_are_checked.py -q`, plus `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_edits_go_through_the_edit_tool.py`, `tests/test_first_setup_asks_once.py`, `tests/test_the_pull_request_language_is_the_repositorys.py` and `tests/test_the_handoff_before_round_one.py` — the last of these is named in phase 5's row and not this one, and phase 4's removals are what break it. Each re-pointed case shown red, and the new module shown red by pasting a section body back into a definition | 4b85d80 |
| 5 | `docs/review-handoff-protocol.md` stops being the interim home: §385 becomes a pointer at the contract and the definitions; the *What a prompt is left holding* section gains the sentence that a prompt carries what is specific to the round and nothing else; the draft moves 0.8 → 0.9 with its paragraph in `## Status`. Q4's two lines in `skills/implement/SKILL.md` and `skills/code-review/SKILL.md` if it is answered `A` | `uvx --with pytest python3 -m pytest tests/test_the_handoff_before_round_one.py tests/test_the_fixes_name_their_surface.py tests/test_review_axes.py tests/test_chain_check_at_the_pull_request.py -q`, plus the new pinned sentence shown red | 72cbcda |
| 6 | `changelog.md` and `seal/ledger/1788433011-….md` in this directory, `overview.md` closed, and the narrow verification for every module the branch touched. Hand to the review chain | `uvx --with pytest python3 -m pytest tests/test_the_changelog_is_gathered_at_release.py tests/test_the_ledger_fragments_fold_at_release.py tests/test_a_row_points_by_content.py tests/test_no_real_identifiers.py tests/test_no_document_names_the_old_roots.py -q` | 5e610a3 · 5047442 |

**Why this order.** Phase 1 before phase 2, because the opening line has to
name a file that exists. Phase 2 before phases 3 and 4, because no
intermediate commit should leave a definition with a rule cut out and no
pointer to where it went — a review round reads the SHA it is given, and a
definition in that state is a definition that lost a rule. Phase 5 last among
the moves, because the protocol's §385 can only become a pointer once there is
something to point at.

**Every phase commits.** This branch squashes into `release/v0.6.0` and
`routing.md` is on disk, so the review arm of the commit gate is silent and an
intermediate commit costs nothing. An uncommitted change is invisible to the
reviewer.

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Phase 6 names two commits.** The first, `5e610a3`, repairs a rule this
work item deleted: `spec.md`:90 assigns *mutation-test every unit added,
one at a time, before handing over* to the smith's own layer, phase 4 did
not move it into `agents/smith.md`, and phase 5 removed its only home. It
is a commit of phase 6's rather than a seventh phase, because it is this
phase's own finding and the plan's phases are slices of the work rather
than of the calendar. The second is what closed the phase.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it. **Re-read this column after any rebase**, or it names
commits that resolve in one clone and nowhere else.

## Verification scope, per phase

Narrow and often, broad once. Each phase runs the modules its own diff can
break, named in the table. **No phase runs the full suite, repository-wide
lint or a typecheck** — the broad gate runs once, after the review rounds
settle, and the orchestrator owns it. Every phase hands over with the suite
labelled `unverified` and the orchestrator named as its answerer.

Exit codes are read directly: `cmd >/dev/null 2>&1; echo $?`, never
`cmd | tail; echo $?`. This plan is the first document in the repository that
has to obey the rule it is about.

## Operational impact

- **No migration, no new environment variable, no new dependency.**
- **If Q1 answers B**, a new skill appears in the user-facing skill listing.
  That is the one thing a user sees change, and it is named in the changelog
  entry rather than left to be noticed.
- **If Q1 answers A**, `tests/test_the_release_check_watches_what_ships.py`
  moves `docs` from `STAYS_HOME` to `SHIPS` and the hygiene workflow's pattern
  moves with it, which means every later edit to any `docs/` file requires a
  version bump. That is a change to what the release check watches and it
  belongs in the pull request body under its own heading.
- **Compatibility.** An older installed plugin version keeps working: the
  contract is additive to what an agent reads, and no hook, gate or checker
  reads it.
- **Prompt budget: zero.** Nothing here adds a question to any session.
