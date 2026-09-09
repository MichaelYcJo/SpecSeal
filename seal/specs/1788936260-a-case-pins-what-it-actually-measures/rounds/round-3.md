# 1788936260-a-case-pins-what-it-actually-measures — review round 3

| Field | Value |
|---|---|
| Target SHA | 0cfc5e6 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 311 |
| Broad gate | 2cc1a18 against 0df9508 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 20, 21, 22 and 23. Findings 24, 25 and 26 are corrections and count toward nothing. |
| Loses a record or crashes | yes — `skills/verify/scripts/arm_check.py:1040`. `--timeout nan` and `--timeout inf` escape the arm loop as `ValueError` and `OverflowError`, `_report` is never reached, and the tool exits 1 with a traceback, which is the shape round 1 recorded here and round 2 closed for `OSError`. Nothing leaves the root: `run_arms`' outer `finally` restores the module on that path, the hash was verified back, and the clone's `git status --porcelain` was empty after every value. No verdict is discarded either, because the first command raises before any arm is measured. |

- [x] Pass

## What this round was asked

Round 3, and **the last round this run may have.** Target `0cfc5e6`; the diff
is `0c93614..984d585`, round 2's fixes and nothing else. Round 2 met the floor
and reopened the run once, which is the one reopening
`docs/review-chain-spec.md` allows — so whatever this round opens becomes an
issue rather than another fix pass, and the run ends either way. That changes
what a finding is *for* here, not how hard to look: a 🟡 this round raises is
a ticket somebody reads next week, so it needs the coordinate and the grounds
to survive without this session.

Round 2's own five verdicts are the agenda — 15 · 16 · 17 fixed, 18 · 19
answered — and its `New units` is the finding surface: `NO_VERDICT_COMMANDS`
and four cases, every one at depth 1, reviewed by nobody. `Contract changes`
is `none`, which is itself a claim to check: the labels moved inside
`_report`'s body, and a body is not a unit added.

**Five things this round was told to attack.**

1. **The four labels, and the third door the fix pass found on its own.** A
   pair spawned, waited for and killed at the bound was being printed under
   *pairs not asked*; only a pair `mutate` refuses was never asked. The
   distinction now lives in the reason beside each arm rather than in a label.
   Is that enough for a reader, and does every path reach the right one of the
   four?
2. **`--timeout`'s guard.** It refuses a negative at parse time and
   deliberately does not refuse a small positive, on the grounds that `0.001`
   is a value somebody could legitimately mean. Attack the boundary: `0`
   removes the bound and a negative is refused, so what does a value between
   them do, and what does `nan` do.
3. **Finding 16's corrected claim, in three places.** The docstring, the help
   text and the changelog fragment's user-facing sentence. The help is pinned
   by a case; the docstring deliberately is not, because pinning a docstring by
   substring is #310's own hazard. Judge that asymmetry, and check the third
   place says the same thing as the other two.
4. **The five survivor exemptions.** All five say *never tried* or *could not
   be asked* about the one door where nothing reaches disk, and are excused
   rather than reworded. Read each quote against the code it describes: is the
   door really the one where nothing is written, in all five.
5. **The recount.** `overview.md` now says 47 `^def test_` and 58 collected,
   and the sentence says which number is which and when it was taken. I
   measured 47 and 58. The line has now been wrong twice — 26 against 35, then
   51 against 53 — so read the class rather than the number: is the sentence
   now written so the next fix pass does not make it wrong a third time.

**Facts handed over as coordinates, each labelled. Executed by me** at
`984d585`: `86 passed` on `tests/test_arm_check.py` and
`tests/test_a_segment_feeds_the_flow_log.py`; 47 `^def test_` and 58
collected; `--timeout -1` exit 2 with the reason on stderr and the module
untouched; the all-timed-out run now printing `0 arms measured · 0 killed · 0
watched by no case` and `2 arms with no verdict from any operator`;
`evidence_check.py .` unscoped exit 0, `1063 ok · 0 drifted · 0 broken`;
`survivor-check` exit 0 with five excused on `0c93614..970e2e0` and clean on
the final range; the corrected `--timeout` help text. **Executed by the fix
pass and not re-run by me** — claims with coordinates, contract §5: `511
passed` across seventeen modules, eight mutation arms each seen red, and the
three ledger rows re-read and re-stamped.

**Out of scope.** #312 and #313 — the sidecar copy and the process group, both
mechanism, both the owner's. `questions.md` Q1 and Q2. #310's inherited sweep.
The broad gate is the orchestrator's, once, after this round — contract §2.

**One thing I want in a line of its own, beyond the two terminal lines.**
Whether anything on this branch should stop it merging into
`release/v0.9.5` as it stands. The run ends at this record whatever you find,
so that judgment is the one thing no later round will make.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 15 | The timeout and `OSError` paths route a mutated arm into a list the report called *enumerated and not mutated* | `skills/verify/scripts/arm_check.py:993` | answered | Closed at `b9a1af7` for the labels. Executed: all four labels print correctly on all three doors, and the per-arm line reads `no verdict`. The header's own promise about the reasons is not kept — finding 21 |
| 16 | The bound bounds the wait and not the work, and a per-command bound was called a per-arm one | `skills/verify/scripts/arm_check.py:788` | answered | Closed at `22fc414`. Read: the docstring, the `--timeout` help and `changelog.md:40` all now say *the wait, not the work*, *only the command's own process*, and *two operators, so twice the bound*. The fourth carrier, the document that prescribes the wrapper form, says nothing — finding 22 |
| 17 | `--timeout` accepted a negative and a whole run then reported a survivor count of zero at exit 0 | `skills/verify/scripts/arm_check.py:1040` | answered | Closed at `4243149` for the negative. Executed: `-1` exits 2 with the reason on stderr and the module untouched; `-inf` exits 2 from argparse's own option parsing. The guard tests `< 0` rather than the class — finding 20 |
| 18 | `overview.md` stated a collected-case count the tree did not have | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | answered | Corrected at `984d585`. Executed: 47 `^def test_` and 58 collected at the target, and the two numbers' stated relationship is arithmetically consistent. The class is narrowed rather than closed — finding 26 |
| 19 | `handoff.md` stated the pre-fix `invert` number in the present tense with no dated note | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md:86` | answered | Corrected at `984d585`. Read: the addendum is dated 2026-09-09, names the relabelled first line, and says why the argument the paragraph makes is unchanged. It carries the recount, which is finding 26's second coordinate |
| 20 | 🟡 `--timeout nan` and `--timeout inf` are accepted, escape the arm loop as `ValueError` and `OverflowError`, and end the run in a traceback at exit 1 | `skills/verify/scripts/arm_check.py:1040` | deferred #314 | #314 |
| 21 | 🟡 The no-verdict header says *the reason beside each says whether it was ever mutated*, and none of the three reason strings says it | `skills/verify/scripts/arm_check.py:993` | deferred #315 | #315 |
| 22 | 🟡 `skills/verify/SKILL.md` prescribes the `--tests "bin/test …"` form and never mentions `--timeout`, the 900-second default, or what the bound does not reach | `skills/verify/SKILL.md:68` | deferred #316 | #316 |
| 23 | 🟡 `Verdict`'s docstring still calls *this was never tried* the whole reason `refused` exists and calls `not_applicable`'s contents the *un-asked* operator | `skills/verify/scripts/arm_check.py:674` | deferred #317 | #317 |
| 24 | ⬜ The report tells a reader an arm *is not refused* and prints no label called refused anywhere | `skills/verify/scripts/arm_check.py:977` | deferred #315 | #315 |
| 25 | ⬜ `survivors.md`'s fifth grounds cell credits the exempted case with a section-header assertion it does not make | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/survivors.md:50` | answered | corrected at 7deb172 — the exemption holds; the grounds cell credited the exempted case with a sibling case's assertion |
| 26 | ⬜ The recount carries no date and no command, and its anchor is a phrase rather than the SHA round 2's own fix text proposed | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | answered | corrected at 7deb172 — the recount now carries the date, the SHA and both commands, which is round 1 finding 5's treatment |
| 27 | 🟢 Every path reaches the right one of the four labels | `skills/verify/scripts/arm_check.py:933` | answered | Executed: the all-timed-out door, the unspawnable door, the never-mutated door and the mixed one-measured-one-timed-out arm. Per-arm `no verdict`, `N arms measured`, `N operator/arm pairs with no verdict`, `N arms with no verdict from any operator`. `refused` arms never reach the pairs list, so nothing is counted twice, and the arm total equals measured plus no-verdict on every door |
| 28 | 🟢 The deliberate non-refusal of a small positive bound is honest output | `skills/verify/scripts/arm_check.py:1040` | answered | Executed: `--timeout 1e-9` gives exit 0, `0 arms measured · 0 killed · 0 watched by no case`, both arms in the no-verdict list with the bound quoted in each reason. Nothing reads as a clean sweep, which is what makes the asymmetry with the refused values defensible on grounds and not only on judgement |
| 29 | 🟢 The docstring, the help and the changelog fragment say the same thing | `skills/verify/scripts/arm_check.py:788` | answered | Read all three side by side: the wait rather than the work, the direct child only, two operators so twice the bound. The asymmetry in pinning is sound — the help is output and `test_the_help_says_the_bound_reaches_the_command_and_not_its_children` pins it whole-clause and whitespace-collapsed, where a docstring is not a rendered line and §14 does not reach it. The changelog fragment adds *a negative is refused*, which neither of the other two carries; that is a gap in the help's favour rather than a disagreement |
| 30 | 🟢 All five survivor exemptions sit on the door where nothing is written | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/survivors.md:44` | answered | Read each quote against its code: `mutate`'s docstring, whose raise precedes the write; the bare-`except:` case, both of whose arms `mutate` refuses; `phase-3.md`'s *either*, resolved by the two clauses before it; `phase-3.md`'s `gh_segments:176`, whose `remove` mutation was a `SyntaxError`, and `mutate` calls `ast.parse` before returning so nothing was written; and the fifth case's arm, a match pattern with no mutation for either operator. *Never tried* and *could not be asked* are exact in all five. One grounds cell misdescribes a case — finding 25 |
| 31 | 🟢 The four new units are correct, and the patching style follows the file's own precedent | `tests/test_arm_check.py:1035` | answered | Executed: 86 passed, exit 0, on `tests/test_arm_check.py` and `tests/test_a_segment_feeds_the_flow_log.py` in a clone at the target. `NO_VERDICT_COMMANDS` drives both mutated doors and its case asserts the module's hash is back before it reads the report, which is the premise. Read: the global `ARM.subprocess.run` assignment with a `finally` restore is the file's existing convention at two other cases, so the new one adds no hazard the file did not already carry |
| 32 | 🟢 `Contract changes: none` is true | `skills/verify/scripts/arm_check.py:773` | answered | Read: `run_arms`, `_report` and `main` all keep their signatures; the diff touches `run_arms`' docstring, one comment and one echo string inside its body, four echo strings and three comments inside `_report`, and the help text plus a new guard inside `main`. The only new module-level unit is `NO_VERDICT_COMMANDS` in the test file. A body is not a unit added, and the claim survives that reading |
| 33 | 🟢 This branch falsifies no ledger row elsewhere, and no removed wording still stands unexcused | `seal/ledger.md` | answered | Executed in the clone at the target, exit code read directly: `evidence_check.py .` unscoped, exit 0, `total: 1063 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, `652 names read · 0 refused`. Carried, not re-derived: the orchestrator's `survivor-check` clean on `0c93614..984d585` with the five excused on the pre-`survivors.md` range |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository, checked out at `0cfc5e6`, `uv venv` inside it | clone at the target, CPython 3.13.9, pytest 9.1.1. `git status --porcelain` empty at the end of the round |
| `.venv/bin/python -m pytest tests/test_arm_check.py tests/test_a_segment_feeds_the_flow_log.py -q`, exit code read directly | `86 passed`, exit 0 — the orchestrator's figure reproduced |
| `grep -c '^def test_' tests/test_arm_check.py` and `pytest tests/test_arm_check.py -q --collect-only` | 47 and 58. 47 functions, one parametrized eleven ways and one two ways: 47 + 10 + 1 = 58 |
| `arm_check.py <fixture> --tests … --timeout V` through the command line for `V` in `nan`, `inf`, `1e400`, `-inf`, and through `main` for `-1`, `0`, `1e-9`; exit codes read directly | `nan` exit 1 `ValueError: cannot convert float NaN to integer`; `inf` and `1e400` exit 1 `OverflowError: cannot convert float infinity to integer`; `-inf` exit 2 from argparse's option parsing; `-1` exit 2 from the guard; `0` unbounded and both arms measured; `1e-9` exit 0 with `0 arms measured · 0 killed · 0 watched by no case` and both arms in the no-verdict list |
| `run_arms` with `timeout=float("nan")` directly, then the module's sha256 | `ValueError` escapes `run_arms`; the outer `finally` restored the module, hash unchanged |
| `run_arms` then `_report` on a two-arm fixture, all four doors: every pair timed out, the command unspawnable, a bare `except:`, and one operator measured with the other timed out | every label correct — per-arm `no verdict`, `0 arms measured`, `N operator/arm pairs with no verdict`, `N arms with no verdict from any operator`. Module hash back after each |
| The reason strings printed under the no-verdict header, read against the header's claim | `TimeoutExpired: the command did not return within 0.3s, so this arm was not measured`; `FileNotFoundError: [Errno 2] No such file or directory: '…'`; `NoMutationDefined: h:4: a bare \`except:\` catches everything, …`. None contains *mutated*. One arm printed both doors joined by ` \| ` under a singular claim |
| `mutate`'s raise sites against the write, read | `ast.parse` runs at the end of `mutate` and the write happens after `mutate` returns, so `NoMutationDefined` and `SyntaxError` both precede any write — which is what makes the five exemptions exact |
| `grep -rln arm-check` over the tree, and `grep -n timeout` over `skills/verify/SKILL.md` | five files name `arm-check`, one of which is a document; the skill's §2 mentions no bound |
| `.venv/bin/python skills/evidence-check/scripts/evidence_check.py .` unscoped, exit code read directly | exit 0, `total: 1063 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, `652 names read · 0 refused` |
| `git status --porcelain` in the clone after every probe, and the probe file deleted | empty |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/arm_check.py:745` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:520` | round 1's 3 — fixed |
| round-1 | `tests/test_a_segment_feeds_the_flow_log.py:562` | round 1's 4 — fixed |
| round-1 | `skills/verify/SKILL.md:80` | round 1's 5 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:589` | round 1's 6 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:233` | round 1's 7 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:787` | round 1's 8 — fixed |
| round-1 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:5` | round 1's 9 — answered |
| round-1 | `tests/test_arm_check.py:744` | round 1's 10 — answered |
| round-1 | `skills/verify/scripts/arm_check.py:87` | round 1's 🟢 11 — answered |
| round-1 | `bin/arm-check.cmd:7` | round 1's 🟢 12 — answered |
| round-1 | `skills/verify/scripts/arm_check.py:767` | round 1's 🟢 13 — answered |
| round-1 | `seal/ledger.md` | round 1's 🟢 14 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:822` | round 2's 1 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:842` | round 2's 2 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:529` | round 2's 3 — answered |
| round-2 | `tests/test_a_segment_feeds_the_flow_log.py:566` | round 2's 4 — answered |
| round-2 | `skills/verify/SKILL.md:82` | round 2's 5 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:634` | round 2's 6 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:903` | round 2's 7 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:1013` | round 2's 8 — answered |
| round-2 | `tests/test_arm_check.py:869` | round 2's 10 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:88` | round 2's 🟢 11 — answered |
| round-2 | `bin/arm-check:16` | round 2's 🟢 12 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:867` | round 2's 🟢 13 — answered |
| round-2 | `skills/verify/scripts/arm_check.py:961` | round 2's 🟡 15 — fixed |
| round-2 | `skills/verify/scripts/arm_check.py:786` | round 2's 🟡 16 — fixed |
| round-2 | `skills/verify/scripts/arm_check.py:995` | round 2's 🟡 17 — fixed |
| round-2 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | round 2's ⬜ 18 — answered |
| round-2 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md:71` | round 2's ⬜ 19 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Findings 20, 21, 22 and 23 | **issues**, by the run's cap — round 2 spent the one reopening `docs/review-chain-spec.md` allows, so nothing here commissions a fix pass. 20 and 21 are one issue if the owner wants them together: both are a fix that changed the outward half of a pair and left the inward half | the repository owner |
| Findings 24, 25 and 26 | corrections. 24 rides on 21's edit to the same line; 25 and 26 are under `seal/specs/` and count toward nothing | the repository owner, or the release-preparation commit |
| A process group, so the bound reaches a wrapper's grandchildren | **#313** — already deferred in round 2's record. Finding 22 is the disclosure half and does not depend on it | the repository owner, at #313 |
| A run killed mid-arm loses uncommitted work in the module under check | **#312** — already deferred in rounds 1 and 2, and out of scope by this round's spawn prompt | the repository owner, at #312 |
| What `arm-check`'s exit code should mean | `questions.md` Q1 — already deferred, report-only today and pinned by a case. Finding 20 would give it a second non-zero exit to reason about | the repository owner |
| Whether the twelve `remove` survivors are gaps | `questions.md` Q2 — already deferred, with `phase-4.md`'s table of the twelve as the input | a later work item |
| A sweep of the tree for other cases pinning a document clause by substring | #310's inherited `Not verified` row — already deferred and out of scope by the spawn prompt | whoever builds that sweep; #310 stays open on it |
| `round_record.py new` accepting a `#` cell that `close` refuses | already deferred in round 2's record, coordinate `skills/code-review/scripts/round_record.py:2581` | the repository owner |
| The full suite, the repository-wide lint and the typecheck | contract §2 and §3: the broad gate is the orchestrator's, run once now that the rounds have settled. Handed over labelled **`unverified`**. `ruff` is absent from the clone's virtual environment; `uvx ruff check .` is the form that works | **the review orchestrator** |
| Windows and Linux | `overview.md` — already deferred. `bin/arm-check.cmd` has been run by nobody and this diff does not touch it | CI's windows and linux legs |
