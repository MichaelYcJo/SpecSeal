# the broad gate row runs unchecked and is never asked for (#402, #401) — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `seal/specs/1789445605-…/plan.md` (the Phases table, the
            alternatives table, the failure scenario), `spec.md` (§*What is
            refused, and what stays allowed*, §*The class, enumerated by
            construction*, §*The criterion for choosing a value*, §*Data &
            interfaces*), `questions.md` (Q1–Q4), `routing.md`; `CLAUDE.md`
            §*a change writes fragments*, §*no real identifiers*, §*a thing
            more than one party can have*; `CONTRIBUTING.md` §*House rules*;
            `agent-contract` §§1, 2, 5, 9, 12, 14, 15; `templates/config.md`
            §*Broad gate*; `skills/config/SKILL.md`;
            `skills/implement/orchestration.md` §*Orchestrator: Bootstrap*,
            §*Orchestrator: Parity setup*; `agents/sealer.md`; #402 and #401
            in full
· evidence: six rows added in
            `seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md`,
            which this work item opens; one row REMOVED from `seal/ledger.md`
            (S14 of 1788354065, whose claim ended *and nothing else*); sixteen
            anchor citations re-read and `--reverify`'d
· verified: **executed** — `tests/test_the_seal_is_taken_once_by_the_sealer.py`
            whole (88 passed), the new document module, and the slices named
            per phase, each exit code read directly; every new case seen red
            first, by reverting the call in `gate()` and by deleting each
            pinned sentence one at a time (25 mutations across four loops, one
            of which stayed green and is recorded below); then every unit the
            branch added, mutation-tested on its own — 10 more, one of which
            had nothing behind it and now does; `bin/evidence-check --strict .`
            and `bin/survivor-check` over the branch range. **read** — nothing
            was judged by reading alone. **unverified** — the full suite, the
            repository-wide lint and the typecheck, which are the sealer's one
            run; answerer: the orchestrating session

## Why this work exists

One row of `seal/config.md` decides what the project's final seal covers, and
it could be written in a form that made a failing suite exit 0 — while nothing
in the whole flow ever asked a person to write it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether a pipe can be written into the `Broad gate` row | `spec.md` §*What is refused, and what stays allowed*: "A pipe, `\|` — #402 settles it: a pipe is a normal thing in a broad command… a row written that way is a claim the repository made about itself". A5 asks for it as an executed case, "sealed exactly as today" | The refusal leaves a pipe alone, as the spec says. The end-to-end case pins what the tree actually does instead: `hooks/config.py#CONFIG_ROW` matches a cell as `[^\|]*?`, so a value containing `\|` — escaped or not — stops the line being a row of that table, and `broad-gate` reports the row as ABSENT. `templates/config.md` carries the measurement beside the promise | Executed 2026-09-15 against `config_rows`: `bin/test -q \| tee out.txt` → `[]`, the backslash-escaped spelling → `[]`, `bin/test -q && ruff check .` → the row. The spec's claim is true about the refusal and false about the row, and a template that promises a form nobody can write is the shape this work item exists to end. `config_rows` is not repaired here because `spec.md` §*Data & interfaces* lists it **Unchanged** — it is the shared reader for three callers, one a `PreToolUse` hook |
| How many ledger rows this work drifts | `spec.md` §*Data & interfaces*: fifteen rows, counted by anchor on 2026-09-15 | Eight drifted anchors across sixteen citations, measured; one row removed and the rest re-verified | `bin/evidence-check --strict .`, run in phase 5. `broad_command` and `first_command` never drifted; the Bootstrap's eight rows report as one anchor; four anchors nobody predicted did drift. `agent-contract` §5 on an aggregate — the number could be checked while the claim behind it could not |
| Which carriers link the criterion in phase 3 | `plan.md` phase 3: "`skills/config/SKILL.md` and `skills/implement/orchestration.md` point at it" | Phase 3 links the config skill only; the orchestration link lands in phase 4 with the question that needs it | The orchestration file has no reason to mention the row until the bootstrap asks for it, so a link written in phase 3 would name a section with nothing in it to link from. Both carriers are in the `RULES` table by the end of phase 4 |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over this branch | the orchestrating session, by spawning `sealer` once the review rounds settle — `agent-contract` §2 makes that one act the sealer's |
| Whether a `Broad gate` row can ever carry a pipe, and whether `hooks/config.py#config_rows` should learn to unescape one | the repository owner, at `questions.md` Q5. Out of scope by `spec.md` §*Data & interfaces*, which lists `config_rows` Unchanged. It is a schedulable item and this repository has a tracker, so it wants an issue rather than a `seal/follow-up.md` row — opening one is the orchestrator's act, and the hand-back names it |
| What the refusal SAYS a shell does, on Windows | unmeasured on this branch, and round 1 corrected this row: the refusal itself is a string test over the row's value and reaches no shell, so it raises the same way everywhere — but the message's reason is `/bin/sh` semantics. Under `cmd.exe` a trailing `&` separates commands rather than backgrounding, and backticks and `$(…)` are literal characters. The message now says both. The `windows-latest` job is where one run settles it; answerer: the repository owner, at the next CI run |

## Not done

**`hooks/config.py` is untouched, on purpose.** The pipe finding sits in it and
not in this work's refusal. `spec.md` lists it Unchanged with the reason — it
is the generic `| Item | Value |` reader for three callers and one of them is
a `PreToolUse` hook, so a change there is a change about every row, and one
row's shell semantics are not its business. The finding is recorded in the
ledger fragment, in the template beside the promise it corrects, in a case
that pins what the tree does, and as Q5 of `questions.md`.

**`first_command` is not hardened separately.** `spec.md` closes it by
reachability and phase 1's record says why: it runs only after the run the
refusal precedes, so a guard there could not fire, and a guard that cannot
fire is the counterfeit `verify` names.

**No trace is written for a knowing decline at bootstrap.** Decided in
`spec.md` §Scope with the mode row's own history as the argument rather than
against it.

**The `Checked` column of the sixteen re-verified citations was not retyped.**
`--reverify` recomputes the hash and leaves the date, measured; the re-read is
recorded in `phases/phase-5.md` and in the fragment instead of by hand-editing
fifteen cells in the shared file.

## Fed back into the spec

**A case can pin a whole file while claiming to pin one bullet** — inferred
during implementation, phase 5. `test_the_sealer_is_told_the_row_refusal_is_a_
persons_and_not_its_own` asserted a phrase against `flat(read(sealer))` and
stayed green when the phrase was deleted from the bullet it was about, because
a paragraph added lower down carried the same words. Only the mutation loop
found it. Any document case asserting a phrase that also appears elsewhere in
its file has to slice the region it means first.

**A literal needle in a mutation driver has to match the hand-wrap**, not the
flattened phrase the case reads. Three of phase 4's ten needles spanned a line
break and the driver stopped rather than silently skipping them — which is the
right failure, and is worth knowing before writing the next one.

**A case can be found by the prose of the row it is reading.** Round 1's 🟡 6
was that one helper returned the rows of both tables, so a form's reason could
be paired with another form's. Repairing it with a per-table helper was not
enough: the allowed-list case matched `a pipe` anywhere in the row, and the
pipe row's own cost cell says *and a pipe cannot reach this row at all* — so
renaming its first cell left the case green. A row is identified by its NAME
cell. Found by the fix pass's own mutation loop, not by reading.

**A case that asserts something false is worse than a missing case.** A
partition check over the two lists was written in this pass and went red on
its first run: `$(…)` belongs in both, because the whole command wrapped in it
is refused and one inside a longer line is legal. It came out rather than
being weakened into something that passes.

**A defensive `.strip()` inside a unit whose only caller already strips is a
line claiming a defence it never performs** — inferred during implementation,
after the phases closed. `not_as_written` strips before it reads, and nothing
reaching it through the gate can exercise that: `config_rows` strips every
cell and `broad_command` turns an all-whitespace value into `None`. Removing
the strip left every other case green. It is kept — a module-level function's
correctness should not turn on which caller reaches it — and a case now
exercises it, which is what makes keeping it honest rather than decorative.

**What `survivor-check` reported over this branch is all one deletion**, and
`survivors.md` holds the range row that says so: 88 places, 85 of them rows of
`seal/ledger.md` that share the removed row's Notes boilerplate and three of
them other work items' closed records. Nothing under `skills/`, `templates/`,
`agents/`, `tests/` or `docs/` was reported at all, which is the half that
would have mattered.
