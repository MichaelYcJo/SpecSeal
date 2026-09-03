# 1788360817-the-pull-request-language-is-fixed-inside-a-skill — review round 6

<!-- The verifying round for round 5's fixes (target: the diff e0874cd..eb18a40).
It answered all three and opened two, both of them sentences in a comment and
a record with no runtime effect. The run ends here, three rounds past the cap:
the two go to issue #98 and are named in the pull request body, which is what
`docs/review-chain-spec.md` prescribes at the bound. Nothing in this record's
table closed with a fix, so `Fixes checked by` is `no fixes to check` and it
is true. Written by the review orchestrator. -->

| Field | Value |
|---|---|
| Target SHA | eb18a40 (the fix diff from e0874cd); HEAD f0dc0e2 at review time |
| PR | none yet |
| Broad gate | taken after this record, once, at the branch head |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no — the two this round opened are a comment and a docstring with no runtime effect, deferred to issue #98 and named in the pull request body; the run ends at the bound rather than in a seventh round |

- [x] Pass

## Why the run ends here

The cap is three rounds and it was spent at round 3. Rounds 4, 5 and 6 each
ran with a reason recorded in its own file: round 4 because a 🔴 had to be
answered, round 5 to verify a pass constrained to add no unit, round 6 to
verify the pass that answered it. Each of those passes was smaller than the
one before, and this round found no defect in what the code does.

What it did find is two sentences that are false about arguments that are
right. `docs/review-chain-spec.md` says what to do with a finding at the
bound that is neither fixed nor answered: it goes to a durable home and is
named in the pull request body. Issue #98 is that home, and it carries the
measurement, the three places, and the true reason `-z` has to stay.

**The alternative was a seventh round**, and it is worth writing down why it
was refused. Fixing the comments here would make this record's verdicts read
`fixed`, which makes `Fixes checked by: no fixes to check` false and demands
a later round to open them — the interlock that has pulled this run past its
cap three times. Two comments with no runtime effect are not worth a seventh
spawn, and the loop is the thing this work item's own record has spent three
rounds naming.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r5 3 | the corpus listing still ran `git ls-files` without `-z` | `tests/…:810-828` | answered — the fix is round 5's, this round reproduced its closure | reviewer executed both calls against a repository holding a non-ASCII name and a name with a space: the two lists are identical, and the NUL split drops the empty trailing entry in both |
| r5 1 | the `check=True` comment listed three states and closed one | `tests/…:744-752` | answered — reproduced | reviewer executed four repository states: a non-repository and a missing path raise at 128, an absent `templates/` and one holding only untracked files answer `[]` at exit 0, which is what the comment now says |
| r5 2 | the quoting comment credited the wrong argument | `tests/…:754-762` | answered for the direction; the sentence that replaced it is false in the other direction — this round's 1 | reviewer executed the four variants again against the arguments as they now stand |
| r5 row 14 | `planted in part` rather than planted | `tests-todo.md:20` | pass — an honest close, and the gap is wider than the smith reported | reviewer executed four reverts: `-z` alone removed turns one case red at the blindness assertion, and reverting the whole of round 5's fix leaves all 66 green. The record says which half is pinned, in three places, and the row is not ticked |
| 1 | `tests/…:757-758` says `core.quotePath=false` alone does not turn the quoting off, and it does — measured on git 2.50.1, and `git-config`'s own documentation says so. The same comment contradicts itself at `:761`, which says the argument would be needed if `-z` were dropped. The instruction the comment gives is right and its grounds are wrong. The same sentence is the section name at `seal/ledger/1788360817-…md:86`, and its source is this run's own `round-5.md`, whose grounds cell recorded the four variants correctly and whose summary recorded the opposite | `tests/…:757-758`, `seal/ledger/1788360817-…md:86` | deferred — issue #98, named in the pull request body | reviewer executed the four variants and a fifth for control characters: `core.quotePath=false` leaves a newline in a name quoted, which is the true reason `-z` has to stay |
| 2 | `tests/…:884-886` says two fixture documents carry the only mention of one template; they carry the only mention of one template each — `안내.md` names `templates/sub/buried.md`, `two words.md` names `templates/.hidden.md`. The conclusion holds and the reason given for it is true of one document | `tests/…:884-886` | deferred — issue #98 | reviewer read both fixtures |
| ❓ 3 | `round-5.md` records the four quoting variants correctly in its grounds cell and their opposite in its summary. The reviewer would not edit a record and left it to the orchestrator | `rounds/round-5.md` | answered by the orchestrator: corrected in place, and issue #98 records that this record is where the error travelled from | orchestrator |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the test file at the branch head | 66 passed |
| reviewer: both `git ls-files` calls against a non-ASCII and a spaced name | identical lists; the NUL split's empty trailing entry dropped by both |
| reviewer: the four quoting variants | `-z` alone and `core.quotePath=false` alone each turn the escaping off; both together do too |
| reviewer: a name holding a newline | `core.quotePath=false` alone leaves it quoted; `-z` does not — the reason `-z` stays |
| reviewer: `check=True` against four repository states | two raise at 128, two answer `[]` at exit 0 |
| reviewer: four reverts of round 5's fix against the whole file | `-z` alone removed → 1 red at the blindness assertion; the whole fix reverted → 66 green |
| reviewer: the unit census at both commits | 46 defs, 37 tests, 11 constants, sorted names identical |
| reviewer: `evidence_check.py --strict .` unscoped | `357 ok · 0 drifted · 0 broken` |
| reviewer: `fold_ledger.py --check`, `gather_changelog.py --check` | both name the two unreleased fragments; the pre-release state |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 3–5 | `tests/…#shipped_templates`, `#unreachable_templates` | the unit every fix of this run has touched; issue #98 opens it next |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| This round's 1 and 2 — two sentences false about arguments that are right | issue #98, on 0.6.0, and named in the pull request body | the repository owner |
| 🟡 7 of round 1 — the release guard's blind spot | issue #96, on 0.5.0 and in `docs/flow.md` before the release line | the orchestrator, before the release |
| ❓ 9 of round 1 — the design record still calls `pr.ko.md` a per-user setting | `docs/one-root-by-lifetime.md:449-450`, named in the pull request body | the repository owner |
| What bounds what a finding may create — the pattern rounds 2 to 5 measured | issues #97 and #89, on 0.6.0 | the repository owner |
| The unpinned half of tests-todo row 14 — the listing helper that would close it is a new unit | issue #97, which is the axis it belongs to | the repository owner |
