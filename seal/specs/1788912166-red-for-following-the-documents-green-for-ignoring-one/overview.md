# 1788912166-red-for-following-the-documents-green-for-ignoring-one — overview

📋 implement applied
· spec:     `spec.md` (Grounding, Scope, all nine acceptance scenarios, Data & interfaces), `plan.md` (Technical context, Alternatives, Phases, Operational impact), `questions.md` (assumptions 1–3, Q4); `CONTRIBUTING.md` §*What a change to a gate must carry* and §*House rules*; `CLAUDE.md` §*verification that runs unattended*, §*A change writes fragments, never the shared file*, §*Verification Scope*; `agent-contract` §§1–4, 8, 9, 10, 12, 14, 15; `implement` §§1–4; `templates/sdd-phase.md`, `templates/sdd-overview.md`, `templates/ledger.md` §Coordinates
· evidence: `seal/ledger/1788912166-red-for-following-the-documents-green-for-ignoring-one.md` — six rows added, G1 (#296), G2–G4 (#295), G5–G6 (#297); and eleven pre-existing rows in `seal/ledger.md` re-read and re-stamped, none of them a claim this branch changed
· verified: **executed** — `test_chain_check_at_the_pull_request.py` 78 passed; `test_a_corrected_sentence_survives_elsewhere.py` 40 passed; the six fixture modules 388 passed; every module that reads either touched script, 1129 passed at the point the fixture class was still open; 14 mutations across both scripts, all killed, both files restored byte-for-byte; `evidence-check .` 1017 ok · 0 drifted · 0 broken; `survivor-check` over this branch's own range; `ruff check` and `ruff format --check` clean over the 11 touched Python files. **read** — `round_record.py#bound_line`, the seven existing cutoffs and their reasoning at `STRICT_FROM`, `hygiene.yml`'s survivor step. **unverified** — the full suite, the repository-wide lint and the typecheck; see the table below

## Why this work exists

Three pull-request checks were wrong about what they were reading: two failed a
session for obeying a document, and the third — the `Broad gate` cell — was
written on every round record and read by nothing at all, so the one
full-suite run the whole design turns on could be skipped or spent early with
no gate noticing.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| An ABSENT `Broad gate` row, above the cutoff, at a ready pull request | spec silent. `spec.md` §Scope names `not yet` and a premature SHA and says nothing about a missing row | it FAILS, read as the same state as `not yet` — the cell names no run | The cell's question is *did the run happen*, and an absent row answers it the same way `not yet` does. Reading it as *nothing to check* would make deleting one line the way past the whole arm, and above the cutoff it cannot arise honestly: `round_record.py new` writes the row on every record it generates. Flagged in `phases/phase-2.md` as the one decision in the branch a reviewer should weigh rather than check |
| An `--exempt` range spec that no longer resolves | spec silent; `questions.md` assumption 1 covers the row's shape and not its resolution | reported under `unresolved`, never exit 2 | A `survivors.md` lives from the work item's first row until the release that ships it, and the release branch its range names gets deleted. Exit 2 would then refuse every later range's check over a row unrelated to it — the landmine direction. Recorded in `phases/phase-3.md` as this phase's own decision |
| Where the changelog entry and the ledger rows go | `implement` §2 and `agents/smith.md` say the entry accumulates unreleased under a shared heading | the work item's own `changelog.md` and `seal/ledger/<id>.md` fragments | `CLAUDE.md` §*A change writes fragments, never the shared file* states the override in as many words: *"This overrides the `implement` skill and `agents/smith.md`."* `CONTRIBUTING.md` §House rules says the same |
| `\| Ran by \|` in the three phase records | `templates/sdd-phase.md` requires the row | `unknown — <why>` in all three | The template forbids the one filler that is available to a segment: *"What must not happen is the segment sourcing the value from its own idea of what it is."* The spawn prompt named no runner, so the honest answer is the `unknown` form the template provides, and the orchestrator can fill it by reach-back |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint, and the typecheck | the orchestrator, at the broad gate after the rounds settle — `agent-contract` §2 reserves all three, and a spawn prompt cannot widen that (§3) |
| the three arms running inside a real GitHub Actions pull-request event, rather than against a written `event.json` | the pull request itself, on the `release` leg. `pull_request_state` reads `GITHUB_EVENT_PATH` off disk, which is what the cases write, so what is unproven is the workflow wiring rather than the reading |
| the platform legs — the suite on the operating systems this session is not on | the pull request's platform legs. Nothing in this change inspects a process or a path in a platform-dependent way, so the exposure is the general one |
| whether the `Broad gate` cell should be validated where it is WRITTEN, now that something reads it | the repository owner — `questions.md` Q4, recorded before the first edit and unchanged by the build. Assumption 3 is the reading either answer permits, so nothing here blocks on it |
| this branch's own last round record needs a real broad-gate SHA before the pull request goes ready | the orchestrator. `GATE_FROM` is this work item's own id and the cutoff is `>=`, so this pull request is the first one the new arm applies to — see *Not done* |

## Not done

**The 1.6 similarity floor was not touched**, though #297's 153 survivors
scored 1.60–1.62 and so implicate it. `spec.md` §Scope records it as out:
moving the floor changes every future run's verdict, and it was calibrated
over 77 real ranges. The whole-range row is the answer that leaves the
calibration alone.

**The seal block's `broad gate:` line was not made the source** for #295. The
round record already carries the cell, which is why the arm was cheap;
whether the seal block should become load-bearing is a separate question and
`spec.md` records it as out.

**`orchestration.md`'s sequence was not changed.** The document is right — a
reviewer needs a pull request to review — and the check was the thing that was
wrong. What did change there is the paragraph that documented the resulting
red window as *the window's expected state, not a failure to chase*, because
#296 removes the window that sentence described.

**One consequence is deliberately left for the orchestrator to act on rather
than worked around here.** `GATE_FROM` is this work item's own id and the
cutoff is `>=`, exactly as the seven before it are keyed, so the new arm
applies to this branch's own pull request. Before it leaves draft, the last
round record's `Broad gate` cell has to carry the SHA of the one full-suite
run and the base it was compared against. Setting the cutoff one second later
to exempt this branch was available and refused: a gate whose author exempts
their own change from it is the version of this rule nobody downstream would
trust.

## Fed back into the spec

**None as a clause.** Two decisions the specification did not cover were
settled during the build and are recorded in the divergence table above and in
the phase records rather than written back into `spec.md`: an absent
`Broad gate` row fails, and an unresolvable range declaration is reported. Both
are inferred during implementation and a planner may overturn either.
