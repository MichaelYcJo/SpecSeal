# 1788501054-a-check-reports-clean-while-something-is-missing — review round 8

| Field | Value |
|---|---|
| Target SHA | 293a761 |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | `293a761`, against `origin/release/v0.8.0` — **2090 passed · 4 failed · 1 skipped**, `ruff check .` and `ruff format --check .` both clean; the four are issue #160's macOS-only export cases, failing identically on `origin/main` where CI is green. Spent by 🔴 1's fix and re-taken after it |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1, three copies of the floor's count rule still state the old rule as the whole rule, two of them in the file this diff changed and one in the normative protocol, so a tool built to the protocol refuses the sequence this branch exists to make writable; 🟡 2, `round-7.md`'s `Contract changes` names `check_round` where `main` is the only caller; 🟡 3, `round-7.md`'s `Fixes checked by` reason is false at HEAD |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE TERMINAL STATE IS REACHABLE NOW — 🟢 9 below built it in a clone and
`chain_check` exited 0 for the first time in this run. What this round opened
is the class the branch has fought since round 2: a correction reaching some
copies and not the rest. The commit that wrote the count rule (`f187b39`)
wrote it in SIX places; round 7's fix updated three and `phase-10.md`'s
removal table named those three as the whole set. The prose suite pins the
FLOOR in four carriers and the count rule in two, and the protocol is in
neither, which is why nothing went red.

The run is past its bound and the prompt said a finding here goes to the
repository owner. The owner's standing instruction for this run is that the
orchestrator writes the fixes; all three findings are prose and record cells,
so the fix adds no unit and no contract, and the reader it owes is one
verifying round at a prose diff, which by the same documents consumes nothing
if it opens nothing.

Written and committed before the fixes it commissions, so both fix-surface
rows start pending. -->

## What this round was asked

The verifying round at `git diff 9bf9584..293a761` — **four commits**, all the
orchestrator's, written on the repository owner's instruction rather than by a
smith, given as a count the round was told to re-take. It did: 4.

Round 7 had opened a 🔴 in the checker — the floor's walk read `Needs a fix`,
the reviewer's answer, where the bound needs whether fixes were written — and
three 🟡 that were the orchestrator's own stale cells and a fragment paragraph.

**Eight specific things to try to break**: the gate change against all four of
`CONTRIBUTING.md`'s requirements; whether the new case's three-commit fixture
exercises the ordering rule or passes for an unrelated reason; `wrote_fixes`
on what it cannot read, and whether the ALLOW stays bounded; the four rows
re-read in two other ledgers; **every copy of the floor rule**, since the
class had recurred inside its own fix four rounds running; the orchestrator's
cells at `293a761`, parsed rather than read; **the terminal state this round
creates, built in a clone** — the check that mattered most; and the squash.

The fifth found 🔴 1. The seventh passed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | Three copies of the floor's count rule still state the old rule as the whole rule. `phase-10.md`'s removal table names three documents as the complete set; the commit that created the rule wrote six copies, and this diff updated three | `chain_check.py:2353` (`stopping_floor`'s docstring, in bold four lines above a walk with two stops), `chain_check.py:208` (module docstring), `docs/review-handoff-protocol.md:318-319` | open | **Executed** by the round: `git log -L 319,319:docs/review-handoff-protocol.md` → `f187b39`, the same commit that wrote the sentence into the spec, the template, the skill and both docstrings. **Orchestrator re-verified**: grep finds the old wording standing alone at `chain_check.py:208` and `:2353`, and the protocol at `:318-319` reads *a conforming tool counts later records only up to the first whose `Needs a fix` says the run reopened* — the normative document specifies one stop where the shipped checker implements two. Nothing went red because `tests/test_the_run_stops_at_the_last_finding.py`'s `STATES_THE_RULE` is `(SPEC, SKILL)` and the protocol is in no carrier tuple |
| 🟡 2 | `round-7.md`'s `Contract changes` names the wrong reach — `stopping_floor … → check_round`. `check_round` never calls it | `rounds/round-7.md:10`, and the trailing comment's grep claim | open | **Executed** by the round and **re-verified by the orchestrator** with the enclosing definition located: the module's only call is at line 2860, inside `main`; `check_round` is 2541–2641 and its docstring records that per-record questions are not asked there. The previous work item's `round-1.md` names the same reach correctly as `main`. The orchestrator's grep found the call and misread which function it sat in — the eighth instance on this branch of prose about a record being wrong, and this one about the record's own reach |
| 🟡 3 | `round-7.md`'s `Fixes checked by` gives a reason that is false at HEAD — *this round's fixes are not yet written* — beside its own verdict column reading `**fixed**` four times. Verbatim the shape of round 7's own 🟡 3 | `rounds/round-7.md:9` | open | **Executed**: `chain_check` prints the cell verbatim on every run. Unlike round 6's case the reader genuinely does not exist yet, so `round-8` was not writable at `293a761`; the reason is false either way, and the cell becomes `round-8` the moment this record is committed |
| 🟢 4 | The gate change against `CONTRIBUTING.md` — all four requirements | `phase-10.md`, the diff | answered | **Executed**: reverting only the `or wrote_fixes(...)` clause turns `test_a_round_that_fixed_over_a_no_is_where_the_count_stops` red with the floor's own sentence and it is the **only** case that goes red (1 failed, 65 passed); separately, at `9bf9584` the repository-records case fails naming `round-5.md`. Direction ALLOW stated in five places; prompt budget zero, because `chain_check.py` is a CI step at `hygiene.yml:147` and prompts nobody; no OS boundary |
| 🟢 5 | The three-commit fixture — required or decorative | `tests/…floor_and_the_depth.py:475` | answered | **Executed by probe**: the two-commit shape (fix first, record added already filled) is refused by `written_late` — *this record was ADDED by a commit which descends from the one its own verdicts name as the fix*. The three commits are required, and the case dies to the walk clause alone |
| 🟢 6 | `wrote_fixes` on what it cannot read | `chain_check.py#wrote_fixes` | answered | **Executed by probe**, three states: record absent → False; no verdict table with `**fixed**` in prose → False; verdict column header renamed with `**fixed**` in a cell → False. Every unreadable state fails toward *blocks more*, consistent with `run_reopened`'s None; the widening is confined to a readable table holding a `FIX_WORD`, and the walk stops at the **first** such record |
| 🟢 7 | The four rows re-read in two other ledgers | `seal/ledger.md:197`, `:359`; `1788472135` F1, F9 | answered | **Read**: each clause says what the re-read found. F9's claim changed and it says so, points at R11, and lists what it still refuses. **Executed**: all three cases F9 cites green, and three quiet rounds still red under both walks |
| 🟢 8 | Every parsed cell of all seven records | the seven records | answered | **Executed**: `fix_surface`, `stopping_floor`, `ran_by`, `verdict_table`, `open_blocking`, `written_late` called directly over each — zero problem rows. `New units` names exactly the four definitions the two fix commits added, all depth 1 |
| 🟢 9 | **The terminal state this round creates** | a `--no-local` clone | answered | **Executed**: `round-8.md` with `no fixes to check` / `no` / `no` / `Pass` ticked, `round-7.md`'s cell set to `round-8`, committed, `chain_check --baseline origin/release/v0.8.0` → **exit 0**. The run can reach a state a ready pull request opens from. This was the check that mattered most and it passes |
| 🟢 10 | The squash | a `--no-local` clone | answered | **Executed**: `merge --squash 293a761` from the release branch, one commit; floor, checker and ordering suites there **162 passed**; `chain_check` raises the identical two notices. Nothing keys on git history |
| 🟢 11 | Round 7's three 🟡 reach-backs and the fragment paragraph | `round-5.md`, `round-6.md`, the fragment header | answered | **Read** and **executed**: `round-5.md` reads `round-6` / `none` / `none`, `round-6.md` reads `round-7`; the fragment's six are R1, R2, R3, R4, R7, R8 with R6 set apart; the file carries ten rows and the header says ten |
| ❓ 12 | `questions.md` Q2, Q3, Q4 | `questions.md` | out of verified scope | **Read**, unchanged, still written as questions with labelled options. The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count 9bf9584..293a761` | **4** |
| `git log -L 319,319:docs/review-handoff-protocol.md` | `f187b39` — the commit that wrote all six copies |
| grep for the old wording standing alone, by the orchestrator | `chain_check.py:208`, `:2353`; the protocol at `:318-319` read directly |
| `stopping_floor` callers with the enclosing definition, by the orchestrator | one, line 2860, in `main` |
| the `or wrote_fixes(...)` clause reverted alone | 1 failed (the planted case, the floor's sentence) · 65 passed |
| the repository-records case at `9bf9584` | fails naming `round-5.md` |
| the two-commit fixture shape, by probe | refused by `written_late` |
| `wrote_fixes` on three unreadable states, by probe | False · False · False |
| every parsed cell of seven records through six checkers | zero problem rows |
| **the terminal state, built in a clone** | `chain_check` **exit 0** |
| `merge --squash 293a761`, three suites in the squashed clone | **162 passed**, two notices identical to HEAD |
| `evidence_check.py .` **unscoped**, no `--reverify` | `537 ok · 1 drifted · 0 broken` — S8 alone |
| `bin/unverified-check` | exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 2–8 | every copy of whichever sentence the last fix changed | The class has now recurred in six of eight rounds. This round found three copies of one sentence; the carrier tuple that would have caught it lists two of the six |
| round 7 | `chain_check.py#stopping_floor` and its two docstrings | The walk has two stops and the docstring above it states one, in bold |
| rounds 4, 6, 7, 8 | the cell the orchestrator last filled | Round 4's 🔴, round 6's two, round 7's three, round 8's two — every one the orchestrator's own cell or clause |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **The run is past its bound and this round opened a 🔴.** The prompt said a finding here goes to the repository owner. The owner's standing instruction for this run is that the orchestrator writes the fixes; all three are prose and cells, adding no unit, and the reader they owe is one verifying round at a prose diff | this row, `overview.md` §Not done | the repository owner, who has answered the first half; round 9 reads the diff |
| A pin for every carrier of the count rule — `STATES_THE_RULE` extended to the protocol, so the existing case catches the next copy left behind | the fix this record commissions, as a tuple extension and not a new unit | the orchestrator |
| ❓ from round 6 — a ledger coordinate with no `@hash` is counted in no bucket | `rounds/round-6.md` Deferred | the repository owner |
| Whether `st_ino == 0` arrives on `windows-latest`, and the `normcase` pairing | `overview.md` §Not verified | the windows CI leg at this pull request |
| `questions.md` Q2, Q3, Q4 | `questions.md` | the repository owner |
| Issues #158, #159, #160, #161 | the tracker | the repository owner |
