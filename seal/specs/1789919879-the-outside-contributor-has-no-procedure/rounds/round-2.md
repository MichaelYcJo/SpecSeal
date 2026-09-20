# 1789919879-the-outside-contributor-has-no-procedure — review round 2

| Field | Value |
|---|---|
| Target SHA | dc81224f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | not yet opened |
| Broad gate | 5ed42e31 against origin/release/v0.12.1 |
| Fixes checked by | no fixes to check |
| Fix range | `c8e7a9d0ee4ce67cb9629b2c888771b725d64afa..54cff03817955dc2dded239da9f066fc339507fd`, 6 commits |
| Contract changes | none |
| New units | CONVENTION_SURFACES (depth 1); test_no_contributor_facing_surface_names_a_concrete_release_branch (depth 1) |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item `1789919879-the-outside-contributor-has-no-procedure` is the verifying round after round 1's fix pass, at the diff of those fixes, `c8e7a9d0..dc81224f` (four commits), not the branch. Its job is the answers: for each of round 1's seven rows — six `fixed` and one `answered` — is it actually closed, re-derived by reverting the fix the way the grounds describe rather than by reading the diff. Three were weighted above the rest. 🔴 1's repair chose the `NAME NOT IN TREE` marker over stripping the backticks, and what needed establishing was not that the symptom is gone — the orchestrator re-ran that — but whether the marker sits on the right lines and says something true on each, because a marker over a name the tree does have is a silenced check rather than a repair. 🟡 5's fix pass widened the prompt budget by a case rather than deferring, and the question was whether that was the right call and whether the new case binds all three surfaces it claims. ⬜ 7 was declined, and the round was asked to judge the argument rather than the refusal, since a round is not a list of orders and `answered` is a legitimate verdict whose reasoning still has to hold. Then the surface round 1 never reviewed: everything the fix pass created — three new cases, a new `survivors.md`, a `seal/follow-up.md` entry, and the edits to `spec.md`, `plan.md` and `overview.md` — judged as code, with `plan.md`'s filled-in approval line checked for stating what is true rather than a signature nobody gave. **This round is bounded but the reopening is NOT spent**: round 1 met the floor and closed on a fix, and this is the verifying round that clears `Fixes checked by`, so a round that opens nothing needing a fix consumes no cap and is the cheap way out — anything opened was to be weighed as a fix here against a `deferred #N` candidate, explicitly either way. A finding located in a record is a correction — ⬜ with the coordinate — and stays out of `Needs a fix`. Facts handed over as executed by the orchestrator at the target: `evidence_check.py .` exit 0 with `0 refused` and anchors `1368 ok · 0 drifted · 0 broken`. One further fact was handed over wrongly and the round caught it: `chain_check.py --baseline origin/release/v0.12.1` was reported exit 0 and is exit 1, the orchestrator having read `$?` after a pipe. The full suite, repository-wide lint and the typecheck are the sealer's one act and this round ran none of them. Runner: `bin/test tests/<module> -q`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The three refused record lines | `seal/specs/1789919879-…/overview.md:19`, `…/phases/phase-5.md:69`, `…/phases/phase-5.md:114` | answered | **Actually closed.** Executed: markers stripped → exit 2 with exactly 3 refusals of the one retired name at exactly those 3 coordinates; restored → exit 0, `0 refused`, porcelain empty. The markers silence 7 compound names, not 3 — the other 4 are all claimed unmarked elsewhere in the same work item, so nothing true is hidden |
| 2 | 🟡 A1 and the unrecorded divergence | `seal/specs/1789919879-…/spec.md` A1; `…/overview.md` | answered | **Actually closed.** A1 states what the message does, the divergence row exists, the pin is untouched and green. The A1 comment opens mid-line, so its names are read as claims — all resolve today; see finding D |
| 3 | 🟡 The exemption list's reason | `CONTRIBUTING.md` §*What a contribution is not asked for* | answered | **Actually closed.** Re-derived against `.github/workflows/hygiene.yml`: guards at lines 66, 116, 134; none at 52, 158, 199. Every clause true. Residual wording is correction 9 |
| 4 | 🟡 The ledger job is a second refusing check | `CONTRIBUTING.md` §*The two checks that can ask you for something you do not have* | answered | **Actually closed.** Heading, row and new paragraph all changed. Round 1's executed grounds carried; re-read `.github/workflows/test.yml`'s `-ge 2` exit and checked the repair sentence against `CLAUDE.md` §*a change writes fragments* |
| 5 | 🟡 The staleness guard covers two of four surfaces | `README.md`, `README.ko.md`, `.github/PULL_REQUEST_TEMPLATE.md` | answered | **Actually closed, and widening the budget was the right call.** Executed 6 mutations, 3 surfaces × 2 directions, each red alone, restored byte-identical. §12 names this shape, the surfaces are this branch's own, no new module, recorded as a divergence. The grounds wording is correction 8 |
| 6 | 🟡 The rationale promises an unconditional refusal | `.github/PULL_REQUEST_TEMPLATE.md`, `README.md`, `README.ko.md` | answered | **Actually closed.** Re-derived by reading every hygiene step for a `main`-based contribution touching nothing shipped, including the milestone step, which returns 0 for a non-release head branch. No step falsifies the new sentence |
| 7 | ⬜ The guard pin reads `fi` by exact equality | `tests/test_the_release_check_watches_what_ships.py:271` | answered | **The refusal stands; the recorded reasoning does not.** The gate bar's own scope at `CONTRIBUTING.md:36`–`38` is `hooks/` and `.github/workflows/`, which does not reach a file under `tests/`; and a red is constructible in two lines. What holds is that a careless widening matches a line opening `file=` and would be a false green — a judgment a fix pass should not make unasked. Correction 7 above |
| 8 | ⬜ The divergence row claims an intent S5 does not state | `seal/specs/1789919879-…/overview.md:22` | answered | corrected at `1140ea7e` — the clause now says the case went into phase 1's module and that S5 budgets two pins, which is the divergence, rather than asserting an intent `spec.md` does not state; Read `spec.md` S5: "Two pins", naming both. The row's "a third module is what S5 was really rationing" asserts more than the cited document says |
| 9 | ⬜ "The others run on every pull request and pass" is false read alone | `CONTRIBUTING.md:49` | answered | corrected at `54cff038` — three that pass for a different reason are split from the two that are always-on and can refuse, and the sentence points at the rows instead of standing for them; Read: the `ledger` job and the survivor check are also always-on and can refuse. The apposition after it names the three meant and the heading 24 lines below counts both refusing checks, which is why this is residue rather than the shape |
| 10 | ⬜ The handed-over `chain-check` exit code does not reproduce | `skills/code-review/scripts/chain_check.py`, against the spawn prompt | answered | corrected at `1140ea7e` — the round record and its commit message both state that the orchestrator read `$?` after a pipe and handed over `tail`'s status. The spawn prompt is spent; what outlives it is the record; Executed at `dc81224f`, exit code read directly: **1**, not 0, with exactly the two described messages. Unchecking `Pass` leaves it at 1, so the error is the broad-gate one. Expected state, cleared by this round's record and the sealer's run |
| 11 | ⬜ A blank line splits the divergence table into two | `seal/specs/1789919879-…/overview.md:20` | answered | corrected at `1140ea7e` — the blank line is gone and the five divergence rows render as one table again; Read: line 20 is empty, so rows 21–23 are a headerless table and render as literal pipes. No checker reads that section. Delete line 20 |
| 12 | ⬜ The approval line is true and silences the notice about that truth | `seal/specs/1789919879-…/plan.md:7` | answered | the line is true and claims no signature: it names the date, the preset and that nobody read the plan line by line. `APPROVED_RE` matching any filled line is the checker's, not this record's, and the notice it silences is about a trace this line does leave; Read against `routing.md` — the date, the preset and the owner all match, and no signature is claimed. `APPROVED_RE` matches any filled line, so the notice that calls the line "the only durable trace that a person read the plan" now prints nothing for a plan nobody read. Deferred candidate, not a fix here |
| 13 | ⬜ The two survivor exemptions currently match nothing | `seal/specs/1789919879-…/survivors.md` | answered | the two exemptions are a past-state account: `survivors.md` records what `--range c8e7a9d0..HEAD` reported at `57f1dacd` and why two of the three were not survivors. A later range reporting nothing does not make that account false, and the branch range is exit 0; Executed at `57f1dacd`: the range reports exactly the three places the file claims, quotes matching verbatim. At `dc81224f` it reports nothing, with or without `--exempt`, because the carrier text was rewritten again. Harmless; the record is honest about the run it describes |
| 14 | ⬜ A docstring names a case by its position | `tests/test_the_contributor_has_a_procedure.py:18` | answered | corrected at `1140ea7e` — the docstring names `test_no_contributor_facing_surface_names_a_concrete_release_branch` instead of its position; Read: "the last case in this file" becomes false silently when a case is appended below it |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_contributor_has_a_procedure.py tests/test_the_release_check_watches_what_ships.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_a_record_states_what_the_tree_has.py -q` | **139 passed** |
| `bin/test tests/test_the_contributor_has_a_procedure.py -q` | **17 passed** — the count the fix pass claims |
| `evidence_check.py .`, exit code read directly | **exit 0** — `705 names read · 0 refused · 0 drifted · 0 external` |
| The same with all three `NAME NOT IN TREE` markers stripped | **exit 2** — `712 names read · 3 refused`, one retired name at each of the 3 coordinates round 1 found |
| The same after restoring the three files from kept bytes | **exit 0**, `0 refused`; `git status --porcelain` empty |
| The new parametrized case, unmutated | 3 passed |
| The same, a concrete `release/v0.12.1` written into `README.md` alone | **1 failed**, 2 passed |
| The same into `README.ko.md` alone | **1 failed**, 2 passed |
| The same into `.github/PULL_REQUEST_TEMPLATE.md` alone | **1 failed**, 2 passed |
| The convention removed entirely from `README.md` alone | **1 failed**, 2 passed |
| The same from `README.ko.md` alone | **1 failed**, 2 passed |
| The same from `.github/PULL_REQUEST_TEMPLATE.md` alone | **1 failed**, 2 passed |
| All six restored from kept bytes, case re-run | 3 passed; porcelain empty |
| Aside probe — a compound backticked name in a mid-line HTML comment, inside a table row | **exit 2, REFUSED** |
| The same name bare on the same table row | exit 0, not read |
| The same mid-line comment on a PROSE line | **exit 2, REFUSED** |
| A comment OPENING the line, prose | exit 0, not read |
| A comment OPENING the line, inside a table row | exit 0, not read |
| The same name inside a fenced block | exit 0, not read |
| `chain_check.py --baseline origin/release/v0.12.1`, exit code read directly | **exit 1** — the two described messages and nothing else. Finding 10 |
| The same with the record's `Pass` box unchecked, then restored | exit 1 both times; the error is the broad-gate one |
| `unverified_check.py --baseline origin/release/v0.12.1 seal/specs/` | **exit 0** |
| `survivor_check.py --range origin/release/v0.12.1...HEAD` | **exit 0** |
| `survivor_check.py --range c8e7a9d0..HEAD` at `dc81224f`, with and without `--exempt` | **exit 0** both ways — 1107 files against 17 removed sentences, nothing standing, nothing exempt |
| The same at `57f1dacd` | **3 places still standing** — the two `phases/phase-5.md` quotes `survivors.md` exempts, and the test docstring that was corrected. Finding 13 |
| Broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** `agent-contract` §2 leaves all three to the sealer, and this round ran none of them. The rounds settle here, so what comes due is the sealer's spawn |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/specs/1789919879-…/overview.md:19`, `…/phases/phase-5.md:69`, `…/phases/phase-5.md:114` | round 1's 1 — fixed |
| round-1 | `seal/specs/1789919879-…/spec.md` §A1 vs `.github/workflows/hygiene.yml:96` | round 1's 2 — fixed |
| round-1 | `CONTRIBUTING.md` §*What a contribution is not asked for* | round 1's 3 — fixed |
| round-1 | `CONTRIBUTING.md` §*The one check that can ask you for something you do not have*, and its `seal/ledger/` table row | round 1's 4 — fixed |
| round-1 | `README.md:639`, `README.ko.md:631`, `.github/PULL_REQUEST_TEMPLATE.md:3` | round 1's 5 — fixed |
| round-1 | `.github/PULL_REQUEST_TEMPLATE.md:8`, `README.md:641`, `README.ko.md:634` | round 1's 6 — fixed |
| round-1 | `tests/test_the_release_check_watches_what_ships.py:271` | round 1's 7 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `chain_check.py` should tell a filled-but-negative approval line from an approval, or whether the rule should be that an unread plan keeps its placeholder — finding 12 | a `seal/follow-up.md` row or an issue of its own; it is a change to what a gate reads and carries `CONTRIBUTING.md`'s higher bar | the repository owner |
| The aside region's mid-line blindness — already filed at `3323e433`, and finding D narrows it | `seal/follow-up.md`, the row this branch added | the repository owner |
