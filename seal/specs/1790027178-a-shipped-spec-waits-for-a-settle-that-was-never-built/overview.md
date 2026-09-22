# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — overview

📋 implement applied
· spec:     `seal/specs/1790027178-…/{routing,spec,plan,questions}.md`; `CLAUDE.md`
            §*a change writes fragments, never the shared file* and §*The goal a
            design is chosen against*; `docs/one-root-by-lifetime.md`
            §*What happens at a release*, §*The dependency rule*, §*What keeps
            `settle` light*, §*Order*, §*Decided after the thread*;
            `seal/README.md`; `docs/release-checklist.md`;
            `skills/implement/SKILL.md` §*Document layout*; `seal/follow-up.md`
            in full; `skills/agent-contract/SKILL.md`
· evidence: `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`
· verified: **executed** — the modules each phase touched, per phase; Q3's
            probe against the shipped `gather_changelog.py`; the dry run and
            the retirement arm over this tree; 22 mutations, each turning one
            case red alone; every new behaviour case shown red before it was
            committed and every new document case shown red with its sentence
            removed; `survivor-check` and `correction-check` over
            `origin/release/v0.13.0...HEAD`; `evidence-check --strict .`;
            `ruff check` and `ruff format --check` over the branch's Python.
            **read** — the six population floors `spec.md` names.
            **unverified** — the broad gate and three more rows below

## Why this work exists

A shipped spec had nowhere to go: `seal/README.md` named a `settle` step from
the day the root existed and nothing was ever built, so 98 work items and 15M
of records accumulated with no check reading any of them after the merge. This
ships the mechanism — a reader that says which released work items a policy
document has yet to absorb, and a skill that says how a session turns that
into one standing statement per segment.

## Q1 ran on its default

`questions.md` Q1 asks whether this release also folds this repository's own
97 released work items. The owner pressed `automation` in the routing batch,
so the run does not come back to ask, and the default continues: **the fold is
a work item of its own.** The mechanism ships; nothing is removed on this
branch, and phase 6's dry run is the input to that later item. Q1's Status
stays ⬜ because the row is still the owner's to answer.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether `seal/ledger.md` is touched | The spawn prompt: "Do not touch `CHANGELOG.md` or `seal/ledger.md`." Eleven rows in that file were annotated and twelve coordinates re-stamped | touch it, re-read first | The instruction is the fragment rule, whose word is **appended** — no row was appended, and `CHANGELOG.md` was not touched at all. What happened is that this branch edited the content of seven units existing rows cite, which drifts a row by construction: `evidence-check --strict` reported `7 drifted`, and its own line says `broad-gate` runs that check with `--strict`, "where drift is exit 2, and this tree would come back NOT SEALED". So leaving them would have failed the sealer's gate. `CLAUDE.md` §*a change writes fragments* already contemplates a branch touching the file where leaving the ledger true requires it, and the file's header fixes what re-verifying is: re-reading the claim and then running `--reverify`. Each of the eleven was re-read against this branch's edit and carries a dated note saying what moved and why the claim still holds; one, S7, was re-verified by execution. The rows this work item ADDS are in `seal/ledger/1790027178-….md` |
| Where the evidence-todo guard's rule lives | `plan.md` §*Technical context*: "`.github/scripts/fold_ledger.py#marker`, `#is_marked`, `#open_items` — … `settle` reuses all three rather than inventing a second spelling of each". The code carries `open_rows`/`open_items` inside `skills/settle/scripts/settle.py` instead | carry it in the shipped script | `.github/` is not on the list of what the plugin ships (`tests/test_the_release_check_watches_what_ships.py#SHIPS` is `skills · agents · hooks · templates · bin · .claude-plugin`), so a shipped command may not depend on a script a user's repository does not have. The other direction — making `fold_ledger.py` import the shipped copy — is a change to release tooling that no phase of this plan covers. The marker half of the sentence DOES hold and is reused rather than re-spelled: `settle.py` loads `skills/verify/scripts/unverified_check.py#folded_items`, which is the one reader of the fold record |

## The dry run over this repository's own 97 — A10

Executed 2026-09-22 at the tip of this branch, with `bin/settle` and nothing
else. **Nothing was removed**; the retirement arm was run too and reports
`nothing to retire` at exit 1, because no work item carries a fold marker in
`docs/`. Every figure below is read off that run.

| | |
|---|---|
| work item directories under `seal/specs/` | **98** · 1,347 files · 15M |
| released — present at `origin/main` | **97** (the 98th is this work item) |
| grouped, and into how many segments | **81 in 37 segments** |
| named rather than grouped | **16** — 14 wrote no ledger row, **2** are anchored only under `tests/` |
| skipped for an open `evidence-todo.md` row | **0** |
| segments holding exactly one work item | **21** of 37 |
| the largest segments | `round_record.py` 13 · `session_cost.py` 7 · `broad_gate.py` 6 · `chain_check.py` 6 · `evidence_check.py` 4 |
| what the run costs | **0.10 s** real, on this tree |

Two of those numbers are worth more than the rest to whoever opens the fold's
own work item. **37 segments is the number of standing statements somebody has
to write**, and 21 of them cover a single work item — so the judgment act is
wide and shallow rather than deep. And **16 named items have no segment at
all**, which is where the fold's real open question sits: 14 of them wrote no
ledger row, so nothing in the tree says what they were about.

## Not verified

| Item | Who must answer |
|---|---|
| the broad gate — the full suite, `uvx ruff check .` and `uvx ruff format --check .` over the whole tree. Every phase ran its own modules and the files it changed; nothing broad was run, because a broad run with an edit after it is spent rather than banked | the orchestrating session, which spawns the sealer after the review rounds settle |
| whether the six population floors `spec.md` §*The ticket's headline claim is false* names are still six. Nothing here re-measured them: no fold ran, so no floor was reached, and the figures reached this build as the framer's reading | the work item that folds this repository's own 97 — `skills/settle/SKILL.md` §3 is the procedure it follows, and the enumeration is its first act |
| `settle` on a repository other than this one. Every arm was exercised against fixture roots built by the cases and against this tree; no second real repository was tried. **This row said something else and round 1 disproved it**: it claimed local mode's refusal was *read from the code and its message was written for it*, and finding 3 showed the message was unreachable — the `seal/specs/` check fired first and always, so a local-mode repository holding work items was told it had none. That is fixed and executed against a fixture with the root under the git directory, and `test_local_mode_is_refused_rather_than_read_as_an_empty_repository` pins it. What is still untried is a second real repository | the repository owner, the next time the plugin is used somewhere else |
| ✅ the `Ran by` cell of all six phase records, which read `unknown — <why>`. The spawn prompt named no `agent on model` value, and `templates/sdd-phase.md` forbids a segment sourcing one from its own idea of what it is | closed by the orchestrating session at `0adf3ed3`, the round's own target SHA: all six now read `` `specseal:smith` on Opus 5 (1M context) `` with the grounds for the model beside it. Read 2026-09-22 — a grep for the `Ran by` row across `phases/*.md` returns six identical cells and no `unknown` |

## Not done

- **Nothing is removed from `seal/specs/`.** `settle --retire` exists and was
  exercised against fixture roots; on this repository it reports `nothing to
  retire`, because no work item carries a fold marker in `docs/` yet. Writing
  the nine segments' policy prose is the judgment act Q1 defers to its own
  work item.
- **`settle` is not wired into anything.** No hook, no CI step, no
  `skills:` list entry, and no line in the CLAUDE.md block — `spec.md` G5 and
  G8. It is invoked, never triggered.

## Fed back into the spec

- `skills/settle/SKILL.md` carries the population-floor rule (A11), which is
  general rather than this repository's: a fold is not finished until every
  check carrying a population floor over `seal/specs/` has been answered.
  `spec.md` §*The ticket's headline claim is false* is its worked example, and
  the rule is marked as inferred during this work item — `docs/one-root-by-lifetime.md`
  §*The dependency rule* names two readers and the real list is longer.
