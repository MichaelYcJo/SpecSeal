# 1788501054-a-check-reports-clean-while-something-is-missing — review round 9

| Field | Value |
|---|---|
| Target SHA | 3937727 |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | `3937727`, against `origin/release/v0.8.0` — **2091 passed · 4 failed · 1 skipped**, `ruff check .` and `ruff format --check .` clean; the four are issue #160's macOS-only export cases. Spent by this round's fixes and re-taken after them |
| Fixes checked by | nobody — round 10 is the round that opens these fixes and it is not written yet; this cell becomes `round-10` the moment that record is committed |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1, the pin round 8 commissioned is live for one of its five carriers and vacuous on an empty tuple; 🔴 2, `stopping_floor`'s failure message states one stop and instructs the reader to write a false `Needs a fix: yes`; 🟡 3, the spec's exits table states a failure condition the checker no longer has; 🟡 4, the skill's own count-rule paragraph still states the first stop as the whole rule; 🟡 5, `round-8.md`'s `Fixes checked by` reason false at HEAD; 🟡 6, three records claim the pin catches copies it cannot see |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE STRUCTURE SIGNAL FIRED HERE, in the spec's own words: *a round opens
a new 🔴 at the same site as the one it was closing — that is the structure
signal, whatever the count.* Round 9's 🔴 1 sits inside the pin round 8's fix
pass wrote to close round 8's 🔴 1. It is the fifth verifying round in a row
to find its finding inside the previous fix, and it is the loop issue #161
records.

The repository owner chose the smaller of two fixes: the pin is NARROWED to
the one carrier where it was live — the normative protocol — with a guard
against an empty tuple, rather than rebuilt as an eight-entry anchored
window search, which would be one more mechanism written by a fix pass. The
other four carriers keep their corrected sentences and lose their pin, and
the records say so instead of claiming otherwise. 🔴 2 is fixed outright: it
is the one copy of the rule a person reads at the moment of failure, and it
told them the way out was to write a false record.

Written and committed before the fixes it commissions, so both fix-surface
rows start pending. -->

## What this round was asked

The verifying round at `git diff 6c1cf64..3937727` — **two commits**, the
orchestrator's, given as a count the round re-took: 2.

Round 8 had found three of the count rule's six copies stating one stop; the
fix corrected them and pinned all five carriers in one case. This round was
asked to break six things: whether six is the count; the pin's enumeration
and its behaviour on an empty tuple; the docstring's claim that `wrote_fixes`
sits above the walk; the three re-stamped anchors and the AST claim behind
them; the orchestrator's cells at `3937727`, parsed; and the terminal state
and the squash, rebuilt.

The first and second found the two 🔴. Six was wrong: **eight**.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The pin is live for one carrier of five and vacuous on an empty tuple. `flat()` returns the whole file, and `SECOND_STOP`'s spellings occur in four of the five carriers for reasons unrelated to the count rule | `tests/test_the_run_stops_at_the_last_finding.py:104`, `:59`, `:66` | open | **Executed** by the round, one carrier at a time in a clone with only that carrier's second-stop sentence removed: spec GREEN, template GREEN, skill GREEN, **protocol RED**, `chain_check.py` GREEN with both docstrings reverted. `COUNT_RULE_CARRIERS = ()` leaves the case green. **Orchestrator re-verified**: the spellings occur 3·3·1·1·6 times across the five files. Two of round 8's own three 🔴 coordinates are invisible to the case written to close that finding |
| 🔴 2 | The failure message `chain_check` prints states one stop and steers the reader into a false record — *with none of them saying the run reopened … says so in its own `Needs a fix`, and the count stops there.* For a run whose fixes were written over a `no`, the only way out it names is to rewrite the row | `chain_check.py:2521-2530`, inside `stopping_floor` | open | **Executed** by the round on a three-record fixture — printed verbatim. **Orchestrator re-read the lines.** It is the eighth copy of the rule, the one a person reads at the moment of failure, and §14 asks that a changed line a person reads be pinned; round 7 changed the walk two lines above it and left it |
| 🟡 3 | The spec's exits table states a failure condition the checker no longer has — *two or more later round records and none of them saying the run reopened → fails* | `docs/review-chain-spec.md:743` | open | **Executed counterexample** by the round: floor `no`, two later records, none reopening, the first closing on a fix → `stopping_floor` returns 0 errors; the same with `answered` → 1 error. Written by `f187b39`, the commit that wrote all eight copies |
| 🟡 4 | The skill's count-rule paragraph still states the first stop as the whole rule — verbatim the shape round 8 called 🔴 on the protocol, one file over. Round 7's fix added the second stop 47 lines above in a different subsection and `phase-10.md` records all three documents as corrected | `skills/code-review/SKILL.md:334-336` | open | **Read**, and orchestrator re-read the three lines. The two-answers-in-one-document shape `tests/test_one_word_one_meaning.py` exists for |
| 🟡 5 | `round-8.md`'s `Fixes checked by` reason is false at HEAD beside a verdict column reading `**fixed**` three times — round 8's own 🟡 3 one record on. `3937727` reopened the record to fill two of the three reach-back rows and left the third | `rounds/round-8.md:9` | open | **Executed**: `chain_check` prints it verbatim. The template says the three rows are one reach-back |
| 🟡 6 | Three records claim the pin catches copies it cannot see: *the two docstrings would have been named in turn*, *a sixth copy in a fourth spelling would go red*, *pins all five carriers so the next copy left behind goes red* | `phases/phase-11.md:48`, `:56-57`; `rounds/round-8.md` Deferred; `plan.md:47` | open | **Executed** by the round: reverting either or both docstrings never turns the case red. True for the protocol only |
| 🟢 7 | `wrote_fixes` above the walk; the two docstrings agree | `chain_check.py` | answered | **Read**: 2317 vs 2348; same claim in different words |
| 🟢 8 | `Contract changes | none` | `chain_check.py` | answered | **Executed** AST comparison, `293a761` vs `3937727` and vs `cd4fec2`, docstrings stripped: identical |
| 🟢 9 | The three re-stamped anchors | R11, F1, F9 | answered | **Executed**: `evidence_check.py .` unscoped → `537 ok · 1 drifted · 0 broken`, S8 alone |
| 🟢 10 | Every parsed cell of all eight records | the eight records | answered | **Executed** through six checkers — zero problem rows; the only `check_round` error is the unchecked `Pass`, correct mid-run |
| 🟢 11 | Module constants as `New units`, and their depth | `rounds/round-8.md:11` | answered | **Read**: the template says *definitions and constants*; all five answer findings in documents predating the run — depth 1 |
| 🟢 12 | The terminal state, rebuilt | a `--no-local` clone | answered | **Executed**: `round-9.md` with `no fixes to check` / `no` / `no` / `Pass` ticked and `round-8.md`'s cell set to `round-9` → `chain_check` **exit 0** |
| 🟢 13 | The squash | a `--no-local` clone | answered | **Executed**: `merge --squash 3937727`, five suites **176 passed**, identical two notices |
| ❓ 14 | `questions.md` Q2, Q3, Q4 | `questions.md` | out of verified scope | **Read**, unchanged. The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count 6c1cf64..3937727` | **2** |
| the pin, one carrier reverted at a time, in a clone | GREEN · GREEN · GREEN · **RED** (protocol) · GREEN — 🔴 1 |
| the pin with `COUNT_RULE_CARRIERS = ()` | GREEN — vacuous |
| the failure message on a three-record fixture | printed verbatim with one stop — 🔴 2 |
| the exits-table counterexample: floor `no`, two later, first closing on a fix | `stopping_floor` → 0 errors; with `answered` → 1 error — 🟡 3 |
| `git log -L 743,743:docs/review-chain-spec.md` | `f187b39` — the same commit as all seven other copies |
| AST comparison of `chain_check.py`, docstrings stripped, three revisions | identical |
| every parsed cell of eight records through six checkers | zero problem rows |
| the terminal state with `round-9.md` written, in a clone | `chain_check` **exit 0** |
| `merge --squash 3937727`, five suites in the squashed clone | **176 passed** |
| `evidence_check.py .` **unscoped** | `537 ok · 1 drifted · 0 broken` — S8 |
| `uvx ruff check` on the two changed Python files · `bin/unverified-check` | clean · exit 0 |
| spelling occurrences per carrier, by the orchestrator | 3 · 3 · 1 · 1 · 6 — why four carriers stay green with the rule reverted |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 7, 8, 9 | every copy of the floor's count rule — now known to be **eight** | Six was a count the last round carried and this round re-took. `f187b39` wrote all eight; three rounds have corrected them three at a time |
| rounds 8, 9 | `tests/test_the_run_stops_at_the_last_finding.py`'s carrier pin | Written by round 8's fix, found hollow by round 9, narrowed by round 9's fix. The next reader opens it to see the narrowing is honest |
| rounds 4–9 | the cell the orchestrator last filled | Every round since the fourth has opened one |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **The structure signal.** The spec says stop regardless when a round opens a 🔴 at the site of the one it was closing; this round did. The repository owner chose to close the two 🔴 with the smaller fix — narrow the pin rather than rebuild it — and take one verifying round at that diff, which the same documents say costs nothing if it opens nothing. Issue #161 carries the loop with this branch's counts | this row, `overview.md` §Not done, issue #161 | the repository owner, who answered it |
| The four carriers that keep a corrected sentence and lose their pin — spec `:760`, template `:162`, skill `:334`, and both `chain_check.py` docstrings | `phases/phase-12.md` and the pin's own comment, which say so | nobody yet — a pin that works for them is a design question, and #161 says a fix pass is not where to build one |
| The count rule has **eight** carriers from `f187b39`, not six — worth a ledger row | this round's fix pass, as a row in this item's fragment | the orchestrator |
| ❓ from round 6 — a ledger coordinate with no `@hash` is counted in no bucket | `rounds/round-6.md` Deferred | the repository owner |
| `questions.md` Q2, Q3, Q4 · issues #158–#161 · the Windows leg | as before | the repository owner; the windows CI leg |
