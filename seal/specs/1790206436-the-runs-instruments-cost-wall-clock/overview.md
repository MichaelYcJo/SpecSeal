# the run's instruments cost wall clock — overview

📋 implement applied
· spec:     this work item's `routing.md`, `spec.md`, `plan.md`, `questions.md`;
            `CLAUDE.md` §*The goal a design is chosen against*, §*a change
            writes fragments*, §*commit early*, §*no real identifiers*;
            `docs/review-handoff-protocol.md` §*The handoff before round 1*;
            `CONTRIBUTING.md` §*Running the checks*; `seal/follow-up.md`
            (the row on *a figure about a corpus, stated with no moment*);
            `templates/sdd-phase.md`, `templates/sdd-overview.md`;
            `seal/config.md` has no `Record language` row, so these records
            are English
· evidence: `seal/ledger/1790206436-the-runs-instruments-cost-wall-clock.md`,
            seven rows (P1–P3 the runner, G1–G3 the gate, N1 the scratch
            names); `seal/ledger.md`: 18 rows re-read and re-stamped with a
            dated re-read note, none added, removed or re-pointed
· verified: **executed** — the plan's `Verified by` modules at each phase
            (`75 passed` / `191 passed` / `3 passed`, exit 0), five and nine
            mutations in phases 1 and 2 each turning its case red, the cold
            build in a scratch clone, the M2 and W1 probes, `ruff check` and
            `ruff format --check` over every edited Python file (0), the 43
            modules reading the three edited definitions (`2071 passed`, one
            red that this file turns green), `evidence-check --strict` (0,
            1702 ok), `survivor-check` (0, no removed wording standing).
            **read** — the claims of the 18 drifted rows, before each was
            re-stamped. **unverified** — below

## Why this work exists

Three instruments of a run cost wall clock in the 0.15.0 run and none of the
costs was the work's own: the suite runner was serial while CI was parallel,
the gate measured a branch with the installed copy rather than the copy the
branch ships, and parallel agents overwrote each other's scratch files. Now
`bin/test` is parallel by default in every environment it builds or adopts,
the gate runs the tree's own copy and stamps which copy ran, and the clone
and capture names carry the work item id.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `broad_gate.py#gate` is touched | `spec.md` §*Data & interfaces*: *before `gate()` is entered, so `gate@084b7e9f` … is untouched and none of the five drifts*; the code adds one argument, `gate_copy(root)`, to `gate`'s call of `panel` | the argument | `panel` has no way to learn the gated root — `Base` carries ref and commit only — and a module global set by `main` would print `plugin` for a caller driving `gate()` in process. The five rows were re-read and re-stamped (`phases/phase-2.md`) |
| the reason `--pdb` is withheld | `spec.md` A4: *pytest refuses it under distribution*; measured: xdist 3.8.0 refuses `-n 2 --pdb` and collapses `-n auto --pdb` to zero workers itself | the flag stays on the list, the docstring states the measurement | withholding and passing reach the same serial run; withholding is the shorter route and passes the arguments as typed (`phases/phase-1.md`) |
| `bin/test`'s R6 anchor moves | `spec.md` §*Data & interfaces*: the R6 row's `bin/test` anchor (the *Typed as* comment line) *anchors a line that does not move* | the row drifted and was re-stamped | the anchor's unit is the whole comment block (lines 1–35), not the one line; the last paragraph of the block is what phase 1 reworded |
| M1's first reading | `plan.md` phase 1 / `questions.md` M1: the suite alone, cold, in the scratch clone | not taken; the cold build measured one module | the spawn prompt keeps the whole suite off this segment and gives it to the sealer once; §3 of the contract reads that as a narrowing and follows it. The reading the frame wanted is the sealer's, over this branch |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over this branch — and with them M1's second reading, the suite's wall clock beside the six arms under `-n auto` | the `sealer`, in its one run after the review rounds settle, spawned with this tree's absolute `bin/broad-gate` (`plan.md` §*Operational impact*); the orchestrator reads the wall clock off `outputs kept under broad-gate-<random>/` and the panel |
| The Windows paths of phase 1 and phase 2 — `Lib/site-packages/xdist` as the marker, the `.cmd` twin passing `%*` into a runner that appends `-n auto`, `os.path.commonpath` across drives in `under()` — were built for and not executed here | CI's `windows-latest` leg at the pull request (`.github/workflows/test.yml`), which runs the same modules |
| That the installed 0.15.1 copy, once released, redirects to a later branch's tree copy in a real sealer run rather than in the fixture — the first release is the only place a redirect from an installed copy can be measured | the orchestrator of the first work item sealed after 0.15.1 ships, reading the sealer's `broad-gate: … ships its own gate; running …` line |

## Not done

**`seal/ledger.md`'s R6 row of `1788632199` still says *five-minute suite*
in its clause cell.** It is a record's wording; a correction to the shared
file is not a removal, which is the one edit `CLAUDE.md` sanctions there;
and the claim it makes — the shell builtin is the guard, not the location —
is untouched. It stands as written, and the repository owner's open row in
`seal/follow-up.md` on figures stated with no moment is where that class is
already being decided.

**The `uvx --with pytest` no-write fallback in `CONTRIBUTING.md` is still
serial**, as `spec.md` §*Out* decided: it is labelled with its cost, it is
not the sealer's command, and a second command carrying flags is a second
place to drift.

## Fed back into the spec

*Inferred during implementation*, so a planner may overturn either:

1. **`--pdb` is on the withholding list for the shorter route, not for a
   refusal**: xdist collapses `-n auto --pdb` to zero workers itself and
   refuses only an explicit count. `caller_decided`'s docstring carries the
   measurement (`questions.md` W1).
2. **`gate` carries one argument for the stamp's `gate` row**, and the
   stamp's row sits between `from` and the first blank
   (`phases/phase-2.md`; `questions.md` W2).
