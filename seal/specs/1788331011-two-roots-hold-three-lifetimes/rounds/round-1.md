# 1788331011-two-roots-hold-three-lifetimes — review round 1

<!-- seal/specs/1788331011-two-roots-hold-three-lifetimes/rounds/round-1.md — what
this round of the review chain did, written by the review orchestrator right
after the report was verified. The first round of the run: it judged all three
phases of plan.md, since no earlier record existed. -->

| Field | Value |
|---|---|
| Target SHA | 4516166 (HEAD did not move during the round) |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — the fix pass had not run when this record was written; round-2 is the verifying round and sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (an ignored file directly under `.specseal/` stops the move for good); 🟡 2–6 land in the same pass |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | an ignored file directly under `.specseal/` (`.DS_Store` is the macOS default) passes `dirty()` but `git mv` refuses it, so every session start stops at the same unit, no marker is stamped, and the tree is left half-moved with `seal/` present and `routing.md` still at the old path — the message's "The next session start continues" is false | `hooks/root-migrate.py#moves` (`os.listdir(old)` builds the `other` units), `#git_mv`, `#main` (the `error is not None` line) | open | spec §"The move, in order" step 4: every step is a `git mv`, so the unit is what git tracks; probe P1 executed at 4516166: two starts, both `stopped at .specseal/.DS_Store`. Orchestrator opened `moves()`/`git_mv()`: confirmed. Fix: enumerate units from `git ls-files`, and spec step 4 says *tracked* |
| 🟡 2 | `seal` present as a FILE: `os.makedirs(..., exist_ok=True)` sits outside `git_mv`'s `try`, so `FileExistsError` escapes `main()`; under `dispatch.py` that reads as silence every session start. Same shape at `repoint()`'s `open(..., "w")`: an `OSError` after the moves leaves the rows un-pointed and the next start stamps over it | `hooks/root-migrate.py#git_mv`, `#repoint`, `#main` | open | spec §"The move, in order": a failing step stops the run and prints what moved and what did not; probe P2 executed: `FileExistsError` out of `main()`, nothing printed. Orchestrator opened both sites: confirmed |
| 🟡 3 | a destination that already holds the file (`seal/ledger.md` beside `.specseal/map.md`, the shape a merge of a bootstrapped branch leaves) fails with `destination exists` on every start, and the message promises a continuation that never comes | `hooks/root-migrate.py#move` | open | probe P3 executed: same line on both starts, no stamp. Fix: decide before `git_mv` and name the destination; refusal table gains the line |
| 🟡 4 | `repoint_path` rewrites every anchor under `specs/` to `seal/specs/`, but §"Which entries of `specs/` are SpecSeal's" leaves an entry that fails `ITEM_RE` where it is, so a row citing a foreign `specs/` entry becomes BROKEN and S8's equal-totals promise breaks; the spec's step 6 contradicts its own §"Which entries" | `hooks/root-migrate.py#repoint_path`, `#PREFIXES` | open | probe P5 executed: `5 ok` → `4 ok · 1 broken`. Orchestrator opened `repoint_path`: no `ITEM_RE` test. Fix in code and spec step 6 |
| 🟡 5 | the commit the hook stages is refused by the commit gate inside a session (deleted `.specseal/` paths lie outside `DOC_ROOTS`, and the parity arm asks too where `seal/parity.md` exists), and neither README nor changelog says so where they say "review the diff and commit" | `README.md` §"Coming up from 0.3.x", `README.ko.md` same section, `changelog.md` | open | probe P10 executed: `deny` with the three-way prompt. Orchestrator's decision: docs-only — add the `: '[no-review]'; git commit …` line (`[no-parity]` beside it where parity is declared); `DOC_ROOTS` keeps no old path, S15 stands |
| 🟡 6 | the branch re-verified one row of another work item's fragment but left the row above it, whose claim now reads "no `.specseal/` gets no file written" while `implementer-mark.py#main` asks `optin.opted_in`, which reads `seal/` now | `seal/ledger/1788310269-the-implementer-leaves-a-mark.md` (second row of "The mark") | open | orchestrator opened the fragment and `implementer-mark.py:55`: confirmed. Fix: the claim says `seal/`, `Checked` updated, anchor and hash unchanged |
| 🟢 7 | spec S1 (`--follow` on any moved file) and S10 (never a renamed one) still read against the code; only overview.md's divergence table says so | `spec.md` S1, S10 | answered — feed back in the same pass | orchestrator's decision: one clause each ("except `seal/README.md`, rewritten from the template (Q5)"; "an exact rename; one carrying an edit is judged") |
| 🟢 8 | the README's by-hand block ends with `evidence-check .`, which only names the broken rows; `--reverify` re-points them | `README.md`, `README.ko.md` by-hand block | answered — fix in the same pass | probe P6 executed: tracked sets identical hook vs hand; hand leaves 3 broken rows, `--reverify` closes them |
| 🟢 9 | on the resume path an `.specseal/map/` holding only ignored files stays on disk and the hook stamps success; harmless, gates read `seal/` | `hooks/root-migrate.py#move` | answered — refusal table's *clean, moved* row says `.specseal/` may remain holding only ignored files | probe P8 executed |
| 🟢 10 | Q1–Q8 of questions.md are all ⬜ while plan.md says they were approved as defaults; questions.md wants the defaults named in the PR body | `questions.md`, `plan.md:3` | deferred to the PR body | orchestrator memo: the PR body names the eight defaults |
| ❓ a | Windows: `dirty()`'s two-column porcelain and `/` pathspecs | `hooks/root-migrate.py#dirty` | out of verified scope | CI's windows leg is where this is measured |
| ❓ b | a symlinked `.specseal/`, case-insensitive filesystems | `hooks/root-migrate.py#moves` | out of verified scope | reading says a symlink fails like 🔴 1; not executed |

Axes judged clean this round (grounds in the reviewer's report, reproduced by the orchestrator where marked executed): S1–S6, S9–S16, opt-in reach (7 code readers at base, all re-pointed), by-hand = hook on tracked set (P6), release scripts (`gather_changelog.py --check`, `fold_ledger.py --check` executed), `chain_check.py --baseline` judging this item alone with 14 `R100` renames excluded (executed), rename-with-edit judged (test read).

## Executed probes

| What was run | Result |
|---|---|
| P1 `.specseal/.DS_Store` (excluded) + clean tree, two session starts | stopped at `.DS_Store` both times; `seal/ledger.md` moved, the work item not, no stamp |
| P2 `seal` a committed file | `FileExistsError` out of `main()`, nothing moved, nothing printed |
| P3 `seal/ledger.md` committed beside `.specseal/map.md` | `destination exists` on both starts, no stamp |
| P4 `.specseal/scratch` + an untracked file | the throwaway line (scratch is tested before dirty) |
| P5 a row citing `specs/notes/todo.md` | re-pointed to `seal/specs/notes/…`; `4 ok · 1 broken` |
| P6 README by-hand sequence vs the hook, same fixture | tracked sets identical; hand leaves 3 broken rows, hook 0 |
| P7 `hooks/dispatch.py session-start`, HOME redirected | message delivered, marker written, `.specseal/` gone |
| P8 `.specseal/map/.DS_Store` on the resume path | moved + stamped; `.specseal/map/` left on disk |
| P10 commit gate on the staged move | `deny` with the three-way prompt |
| `evidence_check.py --strict .` at 4516166 | 208 ok · 0 drifted · 0 broken |
| `chain_check.py --baseline origin/release/v0.4.0` | 1 judged (this item), 14 `R100` excluded |
| `unverified_check.py --baseline origin/release/v0.4.0 seal/specs/` | 13 overviews · 29 open · 12 closed · 0 unreadable |
| `gather_changelog.py --check`, `fold_ledger.py --check` | exit 1 naming only the unreleased fragments (expected on a release branch) |
| `uvx ruff check` / `format --check` on the changed `.py` | clean |
| 12-file slice, `-n auto` | 271 passed |

Probe P9 (a row citing a README) did not run — fixture locator error; not a finding.

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

first round — nothing inherited.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟢 10 the eight defaults of questions.md | the PR body, at opening | the orchestrator |
| ❓ a Windows porcelain / pathspec | CI's windows leg on the PR | CI |
| ❓ b symlinked `.specseal/`, case-insensitive FS | `seal/follow-up.md` is NOT written for it: reading says it fails like 🔴 1 and the 🔴 1 fix (units from `git ls-files`) covers the symlink case by construction; round-2 opens it | round-2 |
