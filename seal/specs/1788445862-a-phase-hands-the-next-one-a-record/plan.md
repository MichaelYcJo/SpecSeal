# Implementation Plan: a phase hands the next one a record

<!-- seal/specs/1788445862-a-phase-hands-the-next-one-a-record/plan.md — HOW,
in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

The review chain has a counter and the build does not: `rounds/round-N.md` is
committed, read by the next round, and carries what a segment was asked and
what it found. A build phase has none of that — what phase 3 discovers
reaches phase 4 only if the orchestrator retypes it into the next spawn
prompt, and it goes missing without a trace when it doesn't (#107, #121).
Separately, neither a round record nor a build phase says what it was *asked*
to do — only what it found (#119).

This work gives builds the same committed record reviews already have:
`templates/sdd-phase.md`, wired into `templates/sdd-plan.md` and
`agents/smith.md`, plus a "what was asked" section added to both the phase
record and the existing round record, wired into the two orchestrator
skills. Enforcement is level 2 of the three the repository owner considered:
a template blank and a skill instruction, not a gate — see Alternatives.

The work changes what an agent's own instructions say and what a session
reads and acts on at every phase and round boundary from here forward, which
is the top rung of the `implement` skill's ladder, so `spec.md` and this plan
come before the first line of implementation.

## Technical context

- `docs/review-handoff-protocol.md` §Files, `round-N.md — what this round
  did` (offset ~106–304) — the field table and its prose are the model:
  `Target SHA`, `Fixes checked by`, the fix-surface rows, each bought by a
  measured failure and each with its own subsection. `phases/phase-N.md`
  copies the shape, not the fields — a phase has no `Target SHA` to squash
  away and no `Pass` checkbox to answer.
- `docs/review-handoff-protocol.md` §Non-goals (offset ~457–463) — "Structured
  handoff for one workflow (review), nothing broader." Grounds for not
  touching this document at all; see Alternatives.
- `templates/sdd-round.md:1–127` — the file this work's round-side section is
  added to; `## Verdicts` at line 91 is the anchor the new section is
  inserted before.
- `templates/sdd-plan.md:20–51` — the Phases section the pointer sentence is
  added to, right of the existing Status-column explanation.
- `agents/smith.md:105–132` — phase 3, "Implement", where the phase-N.md
  write instruction is added; `:109–112` already carries a comment about
  §9 landing harder on smith than any other agent, which is the same
  "smith edits its own record" pattern this work extends.
- `skills/implement/SKILL.md:27–60` — "The language the records are written
  in", the governed-file list `phase-N.md` joins; `:557–641` — "3. The SDD
  file set", the file-set table `phase-N.md` joins as a new row, right after
  the "middle column is not decoration" paragraph that is this row's own
  justification for existing.
- `skills/code-review/SKILL.md:143–204` — "Cross-session records", especially
  `:165–174` ("A round record starts from `templates/sdd-round.md`") — the
  instruction to copy the spawn prompt's specific content into the new
  section is added beside it.
- `tests/test_the_fixes_name_their_surface.py` — the pattern to follow for
  the new test module(s): prose-pinning assertions plus a `CARRIERS` tuple
  checked for identical vocabulary across every document that names a field.
  `tests/test_review_axes.py` is the second model, for shorter substring
  pins across skill files.
- `tests/test_docs_line_wrap.py:47–74` (`COVERED`) — neither
  `templates/sdd-phase.md` nor `templates/sdd-round.md` nor `agents/smith.md`
  is in this list today (`agents/smith.md`'s own two over-limit lines are a
  named, deferred item in `seal/follow-up.md`, unrelated to this work). This
  work does not add any of the touched files to `COVERED` — doing so is the
  sweep that follow-up row already reserves for a separate change with its
  own argument.
- `seal/follow-up.md` — read in full. Its one open row (bringing
  `agents/smith.md`/`agents/scribe.md` under the line-wrap check) is
  unrelated to this work and not a prerequisite for it.

**What breaks in six months if this is built wrong.** A phase record that
restates `plan.md`'s Status/Delivers cells is a second copy of state that can
disagree with the first the way two rules in two agent files already have
(#107's own opening problem, one layer up). The defence is the same one
`round-N.md` uses: the new file holds only what the existing table cannot —
what was asked, what was found, what was removed — never the commit or the
one-line delivery description `plan.md` already owns.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A column in `plan.md`'s Phases table instead of a new file | "What this phase removes" is naturally a multi-row table (item, destination) and "what was asked" can run to several sentences; squeezed into one cell of the task-list table it either truncates or turns the table into unreadable wrapped text, and it mixes narrative discovery into a row `plan.md` itself keeps to a Status *commit* on purpose — "a past state that someone can open", never prose | rejected — the repository owner already chose the file shape (#121, "ALREADY DECIDED") |
| A `chain_check.py` refusal for a phase record missing the new fields (enforcement level 3) | Needs a red test, a stated failure direction, a prompt budget, and platform honesty per `CONTRIBUTING.md`'s own requirement for any gate change — real cost for a mechanism that has shipped zero records yet to learn a cutoff or a grandfather boundary from, the way `SURFACE_FROM` only exists because `Contract changes`/`New units` shipped first and were measured against real rounds | rejected — owner chose level 2; a gate is revisitable once real phase records exist to measure against (#119, "ALREADY DECIDED") |
| Template blank only, no skill instruction (enforcement level 1) | The blank exists but nothing tells a spawning session to copy the phase-specific prompt content into it — the exact gap `docs/review-handoff-protocol.md`'s own history names for round records before the instruction existed, and the same one #81's cheapest-round evidence is cited against in the issue body | rejected — owner chose level 2 |
| Extend `docs/review-handoff-protocol.md` to cover build-phase handoffs as well as review handoffs | Its own §Non-goals states "Structured handoff for one workflow (review), nothing broader" — extending it contradicts a boundary the document sets for itself. A project adopting *that* protocol is adopting the review convention; a build phase record has no such cross-tool conformance audience, and `plan.md`'s Status column already sets the precedent that build-side conventions live in this plugin's own templates and skills, not in the protocol doc | rejected — `templates/sdd-phase.md` + `agents/smith.md` + `skills/implement/SKILL.md` carry it instead, at the same status the Status column already has |

## Phases

Vertical slices — each phase ends with something runnable and verified. One
smith spawn per phase; this table is the handoff between them, and each
phase's own record (once phase 1 lands) is the other half of that handoff.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `templates/sdd-phase.md`, new, shaped after `templates/sdd-round.md`: a field table (`Phase`, `Commit`), then `## What this phase was asked`, `## What this phase found`, `## What this phase removes` (a table: removed item → where it must land, `none` a valid row), each with an HTML comment stating the measured failure it answers — the #107 dropped-rule story for the removal table specifically. `templates/sdd-plan.md` gains one pointer sentence naming `seal/specs/<work-item-id>/phases/phase-N.md`, written when a phase closes. New `tests/test_a_phase_hands_the_next_one_a_record.py`: the template ships all three sections outside HTML comments, each a placeholder (`<...>`) rather than a filled claim (mirrors `test_the_template_rows_are_rows_a_session_can_copy`'s check via `strip_comments`); `templates/sdd-plan.md` names the path `phases/phase-N.md` | `uvx --with pytest python3 -m pytest tests/test_a_phase_hands_the_next_one_a_record.py -q` — each new case shown red first (delete the section, or comment it out, and watch the assertion fail) | `d7c323c` |
| 2 | `agents/smith.md` phase 3 ("Implement") gains one instruction: at each phase's close, also write `phases/phase-N.md` from `templates/sdd-phase.md` — what "What this phase found" and "What this phase removes" hold, which `plan.md`'s Status/Delivers cells cannot. `skills/implement/SKILL.md` gains: a row for `phase-N.md` in the SDD file-set table (§3, "Starts from" `templates/sdd-phase.md`, "Holds" what was asked/found/removed, "When" phase close); the instruction that the phase-specific content of the spawn or task — never the boilerplate the contract, this skill, and `agents/smith.md` already carry — is copied into "What this phase was asked"; `phases/phase-N.md` added to the `Record language`-governed file list alongside `rounds/round-N.md`. Cases added to phase 1's test module: `agents/smith.md` and `skills/implement/SKILL.md` carry the required phrases; a carrier-consistency check (`CARRIERS`-style) that `phases/phase-N.md` is spelled identically across all four files phase 1 and 2 touch | `uvx --with pytest python3 -m pytest tests/test_a_phase_hands_the_next_one_a_record.py -q` — new cases shown red first | `a59a9c2` |
| 3 | `templates/sdd-round.md` gains `## What this round was asked`, placed after the field table's closing HTML comment and before `## Verdicts`, with its own comment: the spawn prompt's specific content, not the boilerplate `agent-contract` and `agents/warden.md` already carry — what this round was told to attack, in what order, and which facts arrived as coordinates vs. which were left to verify. `skills/code-review/SKILL.md` gains the instruction, beside "A round record starts from `templates/sdd-round.md`", that the orchestrator copies the round-specific spawn content into that section when it writes `round-N.md` right after posting. New `tests/test_a_segments_record_says_what_it_was_asked.py`: the round template's new section exists outside comments as a placeholder; `skills/code-review/SKILL.md` carries the copy instruction; a cross-file consistency case comparing the round-side and phase-side section headings and instruction wording, so the two do not drift into two different conventions for one behavioral guarantee | `uvx --with pytest python3 -m pytest tests/test_a_segments_record_says_what_it_was_asked.py -q` — new cases shown red first | `c5ad90e` |
| 4 | `seal/specs/1788445862-…/changelog.md` and `seal/ledger/1788445862-….md` in this directory; `overview.md` closed (purpose line, any spec/implementation divergence, what was not verified, what fed back). Narrow verification of every module the branch touched, run together: `tests/test_a_phase_hands_the_next_one_a_record.py`, `tests/test_a_segments_record_says_what_it_was_asked.py`, plus the pre-existing modules the touched files already had (`tests/test_docs_line_wrap.py` — confirming none of the four touched files newly needs `COVERED`, since none of them shrank or grew wrapped; `tests/test_review_axes.py`; `tests/test_the_fixes_name_their_surface.py`'s `CARRIERS` cases, to confirm this work did not disturb the existing `Contract changes`/`New units` rows it edits `templates/sdd-round.md` beside). Hand to the review chain | `uvx --with pytest python3 -m pytest tests/test_a_phase_hands_the_next_one_a_record.py tests/test_a_segments_record_says_what_it_was_asked.py tests/test_docs_line_wrap.py tests/test_review_axes.py tests/test_the_fixes_name_their_surface.py -q` | `118af25` |

**Why this order.** Phase 1 before phase 2, because `agents/smith.md` and
`skills/implement/SKILL.md` cite a template that has to exist to be cited.
Phase 2 before phase 3, because the two issues share no code dependency but
phase 3's cross-file consistency case compares its own wording against phase
1/2's, which has to exist first. Phase 4 last, because the carrier-consistency
sweep and the closing artifacts both need every prior phase's files in place.

**Every phase commits.** This branch is routed `smith` · `through the review
chain` · `open the pull request` into `release/v0.7.0`
(`seal/specs/1788445862-…/routing.md`), so the review arm of the commit gate
is silent and an intermediate commit costs nothing. An uncommitted change is
invisible to the reviewer.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`. Fill it in as each phase closes.

## Verification scope, per phase

Narrow and often, broad once. Each phase runs the modules its own diff can
break, named in the table above. **No phase runs the full suite,
repository-wide lint, or a typecheck** — the broad gate runs once, after the
review rounds settle, and the orchestrator owns it. Every phase hands over
with the suite labelled `unverified` and the orchestrator named as its
answerer.

Exit codes are read directly: `cmd >/dev/null 2>&1; echo $?`, never
`cmd | tail; echo $?`.

## Operational impact

- **No migration, no new environment variable, no new dependency.**
- **Nothing changes for an existing work item's already-committed records.**
  `round-N.md` files that predate phase 3 have no "What this round was asked"
  section and are not retrofitted — the same grandfathering shape
  `Fixes checked by` and the fix-surface rows already use, except here there
  is no check to grandfather *against*: an old record simply lacks the
  section, and nothing reads it to complain.
- **The first user-visible effect is at the next release a repository
  installs.** A shared-mode repository's `implement` skill copy updates at
  its next first-setup or explicit upgrade; nothing retroactively rewrites a
  repository's existing templates.
- **Prompt budget: zero.** Nothing here adds a question to any session; the
  instruction is read, not asked.
- **Compatibility.** Fully additive — no hook, gate, or checker reads
  `phases/phase-N.md` or the new round section, so an older installed plugin
  version keeps working unchanged, and a repository that never writes the new
  file or section loses nothing it had.
