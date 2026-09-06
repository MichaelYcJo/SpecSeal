# 1788632199-the-repository-ships-no-way-to-run-its-own-suite — overview

📋 implement applied
· spec:     CLAUDE.md §The goal a design is chosen against, §a change writes fragments never the shared file, §no real identifiers, §Routing decided at the start; seal/specs/1788632199-…/spec.md, plan.md, questions.md, routing.md and phases/phase-1.md (including its `## Correction`) and phases/phase-2.md; skills/agent-contract/SKILL.md §1, §2, §3, §4, §5, §9, §10; skills/implement/SKILL.md §2, §3, §4; skills/writing-style/SKILL.md; templates/sdd-overview.md, templates/sdd-phase.md, templates/ledger.md; CONTRIBUTING.md §Running the checks; docs/review-handoff-protocol.md §The handoff before round 1; docs/flow.md §0.8.2; issue #156's own body; seal/config.md (no `Record language` row, so English)
· evidence: `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md`, six rows (R1–R6), every hash stamped by `evidence-check --reverify` scoped to that fragment and never by an unscoped run
· verified: executed — the nine modules that read what phase 3 wrote, both `evidence-check` forms, and two facts this phase measured rather than inherited (both venv tools' `.gitignore` behaviour, and the standard-library fallback building a usable environment end to end); output in `phases/phase-3.md`. read — the two earlier phase records, the runner and both wrappers, the four cited documents. **unverified** — the full suite, the repository-wide lint and the typecheck; see below

## Why this work exists

Every session that ran a test here first had to work out how, and the one
command the repository did name rebuilt its environment on every call at 55–58
seconds; `bin/test` builds that environment once and every call after the first
costs 0.6 s.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The issue's premise | #156's headline is **"The repository ships no way to run its own suite."**, and it offers as one of four answers *"A line in `CONTRIBUTING.md` naming the command, whatever it is. Cheapest, and it only helps a reader."* — a line to be added. That line was already in the tree at `dcbf404`: `CONTRIBUTING.md` §*Running the checks* held `` uvx --with pytest python3 -m pytest tests/ -q   # or: pip install pytest && python3 -m pytest tests/ ``, with the 3.12 floor sentence beside it | the tree | The work changed from **supplying** a command to **replacing an expensive one**. What the issue got right is narrower than what it claimed: its literal sentence, *"There is no `pyproject.toml`, no dev-requirements file, and nothing in either README that names a command"*, is true — `CONTRIBUTING.md` is not a README — but the headline and the proposed answer both fail against it. And the command that was there is the one the same issue measured at 55–58 s of setup on all seventeen test calls of one segment, so a session that found it landed in the cost this work item exists to remove. `skills/implement/SKILL.md` §1: a ticket ranks above the code as it happens to be and below what the repository actually contains — so the premise was corrected in `spec.md` before the first edit rather than built to |
| The placement's reason | `phases/phase-1.md` claimed, labelled **[executed]**, that the plugin cache ships `tests/` and `skills/` *"while `.github/` is absent from it"*, and put the runner under `.github/scripts/` on that ground. **[executed]** `ls -a` on the cached releases: `0.5.0`, `0.7.0`, `0.8.0` and `0.8.1` each hold `.github/scripts/` and `docs/`, and `.claude-plugin/marketplace.json` declares `"source": "./"` with no `export-ignore` in `.gitattributes`, so the plugin ships from the repository root and withholds nothing | the location, on a different reason | The decision stands and its stated ground was false. What actually keeps a plugin user out of this five-minute suite is the other fact phase 1 established: **`test` is a shell builtin, so PATH never offers `bin/test`** however many copies sit on it, and reaching the runner means typing a path into a versioned cache directory on purpose. `.github/scripts/` is then simply where this repository's own automation already lives — a placement argument that needs no concealment. The false fact had reached `.github/scripts/run_tests.py`, `bin/test` and a test docstring before phase 2 opened it; §5 is what caught it, and one `ls -a` is what it cost. `test_the_placement_stands_on_what_it_actually_buys` now refuses the old sentence and requires the new one |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the orchestrator, at the broad gate after the review rounds settle. `skills/agent-contract/SKILL.md` §2 forbids all three to a build segment, and §3 refuses a prompt that orders them. `plan.md` records four failures at the base of this branch — #160's macOS-only export cases — so the gate is read against that number, not against zero |
| `bin/test.cmd` on Windows — that the wrapper resolves the runner, prefers `py -3`, and falls back to `python` | the repository owner. No Windows machine was available here, and `.github/workflows/test.yml`'s Windows leg runs `pytest` directly rather than through any `bin/` entry, so CI executes no `.cmd` file. The five sibling pairs (`evidence-check`, `unverified-check`, `session-cost`, `deferral-check`, `seal`) are in exactly the same state, which makes this a standing gap in the repository rather than one this work item opened — closing it is a change to CI |
| What a genuinely cold first call costs — one with an empty `uv` wheel cache and no 3.12-or-newer interpreter installed | the first contributor to run `bin/test` on a fresh machine. Phase 1's 5.24 s cold figure was taken where uv's cache and a 3.13 interpreter were already present, so it measures the reuse and not the acquisition. The claim this work item actually makes does not depend on it: the first call pays whatever the environment costs, and it is the only call that does |
| Whether a deliberate invocation of the runner out of a plugin cache needs a guard of its own | the repository owner — `questions.md` question 7, raised in phase 2 and still open. Neither answer changes anything built here: adding a guard is mechanism on phase 1's surface, and a plugin user cannot reach the command by typing it |

## Not done

**No guard against running the suite out of a plugin cache.** Both of the
runner's existing guards — no runner beside the wrapper, no `tests/` directory
— are unreachable in a cache, because 0.8.2 ships `.github/scripts/` and
`tests/` there beside `bin/`. Phase 2 found this while correcting the
placement's reason and deliberately left it: a third guard is mechanism on a
surface phase 1 owns, and the fix pass rule in `agents/smith.md` puts a finding
closable only by mechanism into an issue rather than into the change that found
it. It is question 7 for the owner.

**No `pyproject.toml`, and CI still installs its own pytest.** Both are
`spec.md` §Scope's *Out*, chosen by the owner as question 1. Declaring the
package is a larger change than 0.8.2 is measuring, and making
`.github/workflows/test.yml` call `bin/test` is an argument about CI rather
than about a session.

**`README.md` was not touched.** `spec.md` §Scope's third in-item made this
conditional on the repository's own convention, and the convention refuses it:
the cheat-sheet table lists commands a plugin user types, and `bin/test` is the
one command there that PATH cannot offer. `test_the_cheat_sheet_does_not_offer_the_runner`
pins the absence.

## Fed back into the spec

None. Two claims were **removed** rather than added, both in phase 2: the
placement argument that `.github/` does not reach a user's machine, replaced in
place by what the location actually buys, and `CONTRIBUTING.md`'s instruction
to check `python3 -V` for every command in the block, narrowed to the fallback
because `bin/test` now holds the floor itself. `phases/phase-2.md`'s removal
table records where each landed.
