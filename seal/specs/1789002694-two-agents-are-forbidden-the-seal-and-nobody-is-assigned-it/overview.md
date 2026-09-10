# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `spec.md` (Scope 1–10, S1–S8), `plan.md` (Technical context, the Phases table, Verification scope per phase), `questions.md` Q1–Q7, `routing.md`, `phases/phase-1.md` · `phase-2.md` · `phase-3.md`; `CLAUDE.md` §*The goal a design is chosen against*, §*Verification Scope*, §*a change writes fragments, never the shared file*, §*A ledger coordinate names content*; `docs/flow.md` §*0.10.0 — the agent set* and §*0.10.1*; `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*; `CONTRIBUTING.md` §*Running the checks*; `templates/ledger.md`, `templates/sdd-overview.md`, `templates/sdd-phase.md`; `skills/agent-contract/SKILL.md` §1–§16
· evidence: nine rows written to `seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md` (S1–S9, 35 coordinates); `seal/ledger.md`'s R4 lost the coordinate this branch's rename removed and R4 and R5 both had a stale owner corrected in their claims; eighteen `seal/ledger.md` rows re-read and re-stamped, `Checked` moved to 2026-09-10
· verified: **executed** — `evidence-check .` unscoped, 1089 ok · 0 drifted · 0 broken · 0 old-format, exit 0; `evidence-check` at the base commit, 1055 ok · 0 drifted, which is what made the unscoped re-stamp safe; the nine touched modules plus the four named in the handoff; `survivor-check --range 6f09a3f..HEAD`; one deleted `test_tmp_*` probe that measured the capped-run chain end to end. **read** — the phase records' own findings, inherited rather than re-run. **unverified** — the two rows below

## Why this work exists

The rule that the full suite runs once, after the review rounds settle, named
who was forbidden it and never named who takes it; this work makes that owner
an agent, its procedure a command, and its trace one cell.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Two coordinates the frame verified against do not exist on this branch | `spec.md` S7 verifies the fourth definition by *"`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` … green with the fourth file present"*, and `plan.md`'s phase-3 Verified-by ends *"`payload-meter --agent sealer` run and read"* | Neither was run; phase 3 measured the payload by hand from the definition and the skill bodies its `skills:` list injects, and said so in its own record | Both belong to #292, whose pull request (#329) is open and unmerged — `ls` finds no such module and `command -v payload-meter` finds no such command. `docs/flow.md:86` orders #292's meter FIRST in this release, so the frame was written against the release branch's future rather than its present. The hand count is a byte count of what is written into a spawn, which is a different measurement from the meter's `cache_creation` reading, and only the second answers #292's question |
| Where the shape of the drawing is decided | `plan.md`'s Technical context: *"the stamp picks its twin from `sys.stdout.encoding` and `isatty()` **after** that call"* | Before it | Measured in phase 1: `sys.stdout` and `sys.__stdout__` are one object, and `reconfigure(encoding="utf-8")` moves both — under `PYTHONIOENCODING=cp949` the encoding reads `cp949` before the call and `utf-8` after. `hooks/console.py#to_utf8` exists to make the stream claim a capability the terminal may not have, so this is the one question that has to be asked before it |
| What a UTF-8 pipe gets | The same bullet: *"a UTF-8 pipe gets blocks"*; `spec.md` §Scope 1 and S5: the twin is chosen *"when stdout is not a UTF-8 **terminal**"* | The spec — a pipe gets letters | `spec.md` §Out settles it: *"the sealer's returned text carries the ASCII twin"*, and an agent's stdout is a pipe. Pinned by `test_the_command_piped_prints_the_twin`, which asserts the piped wrapper prints the same bytes as `--shape` |
| How many sentences the two test modules pin | `spec.md` §Scope 6: *"three sentences two test modules pin (`…:153, :764`)"* — a count of three against two coordinates | Three, and the third was found and re-pointed | The third is the case that reads `CONTRIBUTING.md` §*Running the checks*, which reads that section the way `:153` reads `bin/test`. All three were seen red against the file each left, in one run, before any was re-pointed |
| What is in the class *what names the owner of the broad run* | `spec.md` §Scope 6 lists seven documents and `bin/test`'s comment | Two printed failure messages in `chain_check.py` as well | `survivor-check` found them, not the spec. They are a script rather than a document, and they are the one place a person reads the instruction — at the moment a pull request is refused. Contract §12 is the rule: the finding names an instance and the fix is owed to every instance the same cause produces |
| Which record keeps the fix-pass rule for a phase that is not a phase | — | The `Broad gate` cell's writer is named in `templates/sdd-round.md`, not only in the skills | Phase 2's own finding: the template's row comment said only who READ the cell, so a reader of the record had no way back to the command that writes it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at this branch's head. Contract §2 forbids all three to this agent, and the phases ran only the modules their own diffs could break | **The sealer**, which is what this work item creates: `broad-gate --base release/v0.10.0 --record seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it`, spawned by the orchestrator after the last round record reads `Needs a fix: no` |
| `payload-meter --agent sealer` — the fourth agent's payload as the meter reads it, which is a `cache_creation` reading rather than the byte count `phases/phase-3.md` took by hand | #292, whose pull request (#329) is open. It is fourth in this release's order, so the reading can only be taken once that branch merges |

## Not done

**Contract §2 and §6 are left contradicting `agents/sealer.md`, deliberately.**
§2 forbids the broad run to every agent and §6 forbids every agent a durable
write, and the sealer does both. `questions.md` Q4 chose to ship under the
contradiction rather than edit §2 here: that is #120's work, its pin phrase
would move inside a work item that is not its own, and `docs/flow.md` orders
#120 last in this release precisely so the contract is settled against all
five agents at once. The sealer's definition states the contradiction in its
own words and names #120, in the shape §6's last paragraph already prescribes
for a one-agent exception. The section saying so is written to be deleted, and
its last line says so.

**A capped run has no path to a sealed pull request, and the repair is phase
5's.** Measured with a fixture rather than read: a run that reaches the
reopening bound turns every open finding into an issue, so its verdicts read
`deferred #N` and `Pass` comes out checked — but `Needs a fix` is the
reviewer's answer, copied by `round_record.py new` and rewritten by nothing,
so it stays `yes — <what>`. `seal` refuses on exactly that, and `chain_check`
then fails the ready pull request on the cell nothing can now write. The
repair is `seal`'s condition, not the documents, and it is written up in
`phases/phase-4.md`.

**The phrase *after the rounds settle* is left as prose in five places.** It
does not say which rounds — a work item has build phases and review rounds —
where the condition is exact and is a row: the last record's `Needs a fix`
reads `no`. `seal` already refuses anything else, so the mechanism is right
and only the words are vague. Phase 5's, with the coordinates in
`phases/phase-4.md`.

## Fed back into the spec

Three clauses, all inferred during implementation and all open to a planner
overturning them.

- **A scale above 1.0 is refused, not silently ignored.** `spec.md` names 0.75
  as the floor and says nothing about a ceiling, and `shrink` returns the
  chart unchanged for any factor at or above 1.0 — so `--scale 1.5` would have
  drawn the 1.0 figure while saying nothing. The chart is one cell per stitch
  and does not enlarge, and the refusal says so.
- **The gate judges the chain check as a DRAFT pull request.** The gate runs
  before the cell it will write exists, so at that moment the last record
  honestly reads `not yet`; judged as ready, the run fails on the one row it
  exists to fill. A payload GitHub itself wrote is left alone.
- **The base comparison re-runs what stands before the row's first `&&`.** The
  `Broad gate` row is one shell line and nothing in it says which part is the
  suite runner. `templates/config.md` and the config skill both now say to put
  the runner first, which makes it a convention a reader keeps rather than a
  fact the parser can check.
