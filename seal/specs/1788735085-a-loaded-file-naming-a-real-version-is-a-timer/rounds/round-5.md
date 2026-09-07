# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — review round 5

| Field | Value |
|---|---|
| Target SHA | 7f9c9b3ad452c8d3cfda2a60bce47cdb69f6a9ab |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 201 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 5, deferred to #203 at the cap |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 5, the verifying round for round 4's four fixes and the last the cap
allows, spawned against `7f9c9b3` with the fix diff `83ba833..adc0b02`.

The prompt said what the cap means for how the round is spent: not the place to
start a new thread, and `docs/review-chain-spec.md`'s floor — *loses a record or
crashes* — is the only line that would justify going past five. Whatever stayed
open would go out as an issue named in the pull request body.

It carried the run's one class — **a case that cannot observe what its own guard
removes**, seven instances by then, moving every time a round declared it closed
— and one fact that made this round's question different from the four before
it: **the round-4 fix pass had found instance eight itself**, by mutating its own
new assertion, and had rewritten a weak `as_release` case after finding that
hard-coded spellings passed a `[vVrR]?` mutation. That was the first time in the
run the class was caught by the party that wrote the code. The round was asked
to judge whether it actually stopped there, and to say which it was: the class
ended, or it moved again.

Four axes: the four fixes against what they claim, including the two records
that moved; the new `as_release` case put to the question that had paid seven
times; the one residual, judged on whether its sentence is true rather than
reopened; and anything in the diff that would ship wrong, this being the last
look before the broad gate.

It was asked to end it plainly, and for each open finding to give the
issue-shaped things — what, where, what was measured, what would close it — plus
which single one it would spend a sixth round on and whether that one reaches
the floor.

The answer: the class moved again. `refusal` has three separators and the
enumeration stopped at two for the second round running.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | round 4 finding 5 — the separator before the first offender line, and the reordering mutation the fix pass found itself | `tests/test_release_hygiene.py#test_the_refusal_names_the_line_and_the_version_it_refused` | answered | executed: both mutations turn that case red, one at a time, exit 1 each |
| 2 | round 4 finding 6 — a ledger row credited itself with 58 cases where it names four | `seal/ledger.md#G5` | answered | executed: the row names four anchors; the two modules they sit in hold 27 and 31 cases, totalling 58. Both figures now stated apart |
| 3 | round 4 finding 7 — the lookbehind's `.` half had no written grounds | `tests/test_release_hygiene.py#VERSION_TOKEN` | answered | executed: `(?<!\w)` in its place turns a case red on `1.9.9.9`. Removing the lookbehind entirely, and `(?<!\.)` alone, each turn two cases red |
| 4 | round 4 finding 8 — `as_release` could not read a spelling its own module produces | `tests/test_release_hygiene.py#as_release` | answered | executed: reverting to `lstrip("v")` turns the new case red, and so does widening the pattern to `[vVrR]?` without touching the reader |
| 5 | 🟡 `refusal` has three separators and the third is observed by nothing — deleting the `\n\n` before the routes leaves all 32 cases green and renders the routes running into the last refused line | `tests/test_release_hygiene.py#refusal` | deferred #203 | executed: mutation survives at 32 passed, exit 0; rendered text confirms the collision. The proposed assertion is green unmutated and red with the separator deleted |
| 6 | ⬜ the new case derives its accepted prefixes over the 52 letters, so a non-letter widening is outside what it observes — the docstring states this scope and is true | `tests/test_release_hygiene.py#test_as_release_reads_every_spelling_the_token_regex_produces` | answered | executed: `[vV#]?` survives at 32 passed, exit 0. The stated scope is true, so this is the boundary rather than a hole |
| 7 | ✅ the ledger's anchors after four commits of re-anchoring | `seal/ledger.md`, `seal/ledger/1788735085-a-loaded-file-naming-a-real-version-is-a-timer.md` | answered | executed `./bin/evidence-check .` unscoped: 722 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py` at `7f9c9b3` | 32 passed, exit 0 |
| `./bin/evidence-check .` unscoped | 722 ok · 0 drifted · 0 broken, exit 0 |
| `uvx ruff check` / `format --check`, the one changed file | exit 0, exit 0 |
| the eight mutations R3's list names, one at a time on a copy | seven red, one green — the list is exactly right |
| `"\n\n"` before the routes deleted | 32 passed, exit 0 — **survived**, and the rendered message shows the collision |
| routes printed above the offender block | 1 failed, exit 1 — caught |
| `(?<!\w)`, `(?<!\.)`, and no lookbehind, on the compile line only | red, red, red — 1, 2 and 2 failures |
| `VERSION_TOKEN` widened to `[vVrR]?` / `as_release` reverted to `lstrip("v")` | red, red |
| `VERSION_TOKEN` widened to `[vV#]?` | 32 passed, exit 0 — survived |
| `assert not offenders, refusal(...)` replaced by a literal | 32 passed, exit 0 — the stated residual, confirmed |
| the proposed assertion, unmutated / with `"\n\n"` deleted | green / red |
| `grep -c '^def test_'` at `83ba833` and at `7f9c9b3` | 31 and 32 |
| case counts in the two modules G5 names | 27 and 31, totalling 58 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_release_hygiene.py:56` | round 1's 1 — fixed |
| round-1 | `tests/test_release_hygiene.py:82` and `:102-107` | round 1's 2 — fixed |
| round-1 | `tests/test_release_hygiene.py:196-215` | round 1's 3 — fixed |
| round-1 | `62287e9` and `86a6e20` | round 1's 4 — answered |
| round-1 | `tests/test_the_pull_request_language_is_the_repositorys.py:764-786`, `seal/ledger.md:562`, `rounds/round-5.md:68,80` | round 1's 5 — answered |
| round-1 | `seal/ledger.md:550,562` | round 1's 6 — answered |
| round-1 | the nine `LOADED` prefixes at `579a916` | round 1's 7 — answered |
| round-2 | `tests/test_release_hygiene.py:58` | round 2's 1 — answered |
| round-2 | `tests/test_release_hygiene.py:114-125` | round 2's 2 — answered |
| round-2 | `tests/test_release_hygiene.py:159-183` | round 2's 3 — answered |
| round-2 | `tests/test_release_hygiene.py:52-58` | round 2's 4 — fixed |
| round-2 | `tests/test_release_hygiene.py:58` and `:476-482` | round 2's 5 — fixed |
| round-2 | `tests/test_release_hygiene.py:152` and `:170-171` | round 2's 6 — fixed |
| round-2 | `tests/test_release_hygiene.py:196-206` and the fragment's R3 notes | round 2's 7 — fixed |
| round-2 | `tests/test_release_hygiene.py:117-125` | round 2's 8 — fixed |
| round-2 | `tests/test_release_hygiene.py:114` | round 2's 9 — fixed |
| round-2 | `rounds/round-1.md:9,50-52` | round 2's 10 — answered |
| round-2 | `docs/review-handoff-protocol.md:124`, `tests/test_release_hygiene.py:117` | round 2's 11 — answered |
| round-2 | `seal/ledger/1788735085-a-loaded-file-naming-a-real-version-is-a-timer.md` | round 2's 12 — answered |
| round-2 | the nine `LOADED` prefixes at `27c36fe` | round 2's 13 — answered |
| round-3 | `tests/test_release_hygiene.py:52-68` | round 3's 1 — answered |
| round-3 | `tests/test_release_hygiene.py:68` and `:591-600` | round 3's 2 — answered |
| round-3 | `tests/test_release_hygiene.py:175-179` and `:517-539` | round 3's 3 — answered |
| round-3 | `tests/test_release_hygiene.py:212-227` and `:270-273` | round 3's 4 — answered |
| round-3 | `tests/test_release_hygiene.py:127-144` and `:439-460` | round 3's 5 — answered |
| round-3 | `tests/test_release_hygiene.py:124` and `:504-514` | round 3's 6 — answered |
| round-3 | `tests/test_release_hygiene.py:210-225`, `:248-251`, the fragment's R3 notes | round 3's 7 — fixed |
| round-3 | `tests/test_release_hygiene.py:578-590` and `:68` | round 3's 8 — fixed |
| round-3 | `tests/test_release_hygiene.py:443-445` and `:131-132` | round 3's 9 — fixed |
| round-3 | `docs/issues-and-milestones.md:63-67` | round 3's 10 — fixed |
| round-3 | the five cases in `a48d27f..7349afc` | round 3's 11 — answered |
| round-4 | `tests/test_release_hygiene.py:293-324` | round 4's 1 — answered |
| round-4 | `tests/test_release_hygiene.py:78`, `:636-662` | round 4's 2 — answered |
| round-4 | `tests/test_release_hygiene.py:490-505`, `:138-144` | round 4's 3 — answered |
| round-4 | `docs/issues-and-milestones.md:63-70` | round 4's 4 — answered |
| round-4 | `tests/test_release_hygiene.py:309-312` against `:233` | round 4's 5 — fixed |
| round-4 | `seal/ledger.md:1137` | round 4's 6 — fixed |
| round-4 | `tests/test_release_hygiene.py:70-77` | round 4's 7 — fixed |
| round-4 | `tests/test_release_hygiene.py:119-121` | round 4's 8 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the `"\n\n"` between the offender block and the routes is observed by nothing | **#203**, opened at the cap and named in the pull request body | the session that takes #203 |
| `Contract changes` reads `none` for a unit whose meaning changed | **#194**, where this branch's instance is now recorded as a second shape — a mapping change with no change to the returnable set, which the proposed literal-set comparison would not catch | the session that takes #194 |
| the empty inline code span in a `fixed at <sha>` grounds cell | the `# RIDER:` at `skills/code-review/scripts/round_record.py#fix_table`, which owns the repair | the owner of that rider — it predates this branch |
