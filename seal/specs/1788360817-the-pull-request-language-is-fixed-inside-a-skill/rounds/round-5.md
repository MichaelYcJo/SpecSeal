# 1788360817-the-pull-request-language-is-fixed-inside-a-skill — review round 5

<!-- The verifying round for round 4's fixes (target: the diff be1cf33..68cae4c).
It confirmed the no-new-unit constraint held and opened two things needing a
fix, neither of which is the pattern the cap exists to stop — see "Why this is
not the loop" below. Written by the review orchestrator. -->

| Field | Value |
|---|---|
| Target SHA | 68cae4c (the fix diff from be1cf33); HEAD 4b2200f at review time, record-only |
| PR | none yet |
| Broad gate | not yet |
| Fixes checked by | round-6 |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written, and this pass adds none either |
| Needs a fix | yes — 대조 코퍼스 쪽 `git ls-files` 가 여전히 비ASCII 이름을 C-이스케이프하고 공백에서 쪼개므로 그 문서가 코퍼스에서 조용히 빠집니다 (`tests/test_the_pull_request_language_is_the_repositorys.py:810-828`), 그리고 `check=True` 의 주석이 이 인자가 닫지 않은 두 상태를 닫은 것처럼 나열합니다 (같은 파일 `:744-749`). 둘 다 새 유닛 없이 닫힙니다 |

- [ ] Pass

## The constraint held

| | `be1cf33` | `68cae4c` |
|---|---|---|
| top-level `def` | 46 | 46 |
| module constants | 11 | 11 |
| `def test_` | 37 | 37 |

Sorted name lists differ on exactly one line, and it is a rename in place with
the assertion unchanged. The ledger's anchor moved with it and
`evidence_check` answers 0 broken, so no anchor points at the old name. Round
4's `New units: none` is true, and the surface this round was expected to
yield from is empty as designed.

## Why this is not the loop

The cap exists to stop a run that is not converging, and rounds 2 to 4 were
exactly that: each fix added a helper, and the helper carried the next
finding. This round's main finding is a different shape and it is worth
naming, because the two would otherwise be counted together.

**Round 4 applied three arguments to one of two sibling calls.**
`shipped_templates` and the corpus listing beside it both shell out to
`git ls-files`, and both had the quoting defect round 4 found. The fix
reached the first. The second still C-escapes a non-ASCII name and splits a
name with a space, and `unreachable_templates`'s `except OSError: continue`
then drops that document from the corpus in silence — so a template only that
document names is reported unreachable.

That is an incomplete fix, not a new surface. Nothing was created for it to
live in; the same three arguments close it, on a call that already exists.
The measure that matters: this round's fixes add no unit either, so round 6's
yield surface is empty by the same construction that emptied round 5's.

**The run therefore takes one more pass and one more verifying round**, past
a cap that is already spent, with the reason recorded here rather than in a
session that ends. If round 6 opens anything, the branch goes to a pull
request with the finding named. It does not go into a seventh round.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r4 1 | the templates listing read silence as an answer | `tests/…#shipped_templates` | answered — the fix is round 4's, this round reproduced its closure, and narrowed what it closed (this round's 1) | reviewer executed eight states: a non-repository and a missing path raise at exit 128; a worktree, a bare repository, an absent `templates/`, an empty one and one holding only untracked files all answer `[]` at exit 0 |
| r4 3 | `git ls-files` C-escaped a non-ASCII template name | `tests/…#shipped_templates` | answered for this call; the sibling call still has it — this round's 3 | reviewer executed four quoting variants: `-z` turns the quoting off by itself |
| r4 2 | three places called a hand-copied list the fields the skill names | the failure message, the ledger row, `tests-todo.md:19`, and the case's name | answered | reviewer executed the census again (five spelled, four absent, two substring matches) and grepped the tree: the wider claim survives nowhere but in the sentence explaining that it used to be there |
| r4 abandoned check | the skill-side drift of `ROUND_RECORD_FIELDS` is now explicitly unpinned | `skills/code-review/SKILL.md:141-146` | pass — and the reviewer's grounds are stronger than the record's | the record gave cost as the reason; the reviewer found the real one by opening the skill: it describes the fields in prose ("broad-gate state", "executed probe results") rather than spelling them, so a reverse check is not a second list but a prose-to-heading correspondence table in code — a new drift source of exactly the shape this run spent four rounds on |
| 1 | the comment at `check=True` lists three states it closed, and it closed one. A repository with no tracked `templates/` still answers `[]` at exit 0, and that is the true answer; a stubbed helper reports nothing to git at all and is caught by the existence assertion at `:973`, whose own docstring says so. The overclaim is the shape this whole run has been narrowing, in the comment written to narrow it | `tests/test_the_pull_request_language_is_the_repositorys.py:744-749` | open | reviewer executed all eight states. No runtime effect; the cost is the next reader believing an empty `templates/` now goes red. Fix: the reviewer's replacement comment |
| 2 | `-z` turns the quoting off by itself and `core.quotePath=false` changes nothing while it is there, where the comment credits the second and calls `-z` what makes it safe. (**Round 6 re-measured: the config argument alone turns the escaping off as well; what `-z` alone does that it does not is turn off the escaping of control characters. Issue #98.**) Keeping the argument is harmless; the comment sends whoever prunes one of them at the wrong one | `tests/…:751-756` | open, comment only | reviewer executed four variants: no arguments C-escapes, `-z` alone does not, `core.quotePath=false` alone does not, both together do not. `split("\0")` leaves one empty trailing entry and `if name.strip()` drops it |
| 3 | the corpus listing beside `shipped_templates` still runs `git ls-files` without `-z`, so a non-ASCII document name comes back C-escaped and a name with a space is split in two; `unreachable_templates`'s `except OSError: continue` drops both from the corpus silently, and a template only that document names is reported unreachable. Round 4 rejected the "this repository's paths are all ASCII" argument for the sibling call and closed it; there is nothing in this diff that makes the same argument sufficient twenty lines above | `tests/…:810-828` | open | reviewer executed it on a scratch repository whose prose is `docs/안내.md` and `docs/two words.md`: both templates reported unreachable, and `[]` with `-z`. The direction is a false red rather than a false green, so it is the milder of the two. Fix: the same three arguments, no new unit; `check=True` is not needed because the assertion on the next line already turns silence red |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the test file | 66 passed, the same number as round 4 |
| reviewer: `evidence_check.py --strict .` unscoped | `357 ok · 0 drifted · 0 broken` |
| reviewer: `fold_ledger.py --check`, `gather_changelog.py --check` | both name the two unreleased fragments; the pre-release state |
| reviewer: the unit and constant census at both commits | 46 / 46, 11 / 11, 37 / 37; one renamed line |
| reviewer: `check=True` against eight repository states | two raise, six answer `[]` at exit 0 |
| reviewer: four `git ls-files` quoting variants | `-z` alone turns the quoting off. **Corrected by round 6, which re-measured against the arguments as they then stood: `core.quotePath=false` alone turns it off too. This cell said it does not, and that sentence reached a comment and a ledger row — issue #98** |
| reviewer: the corpus listing against a Korean-named and a space-named document | both templates reported unreachable; `[]` with `-z` |
| reviewer: the isolation case against three helpers | the fix green, a stubbed helper red at the existence assertion, the pre-fix glob red at `.DS_Store` — pinned both ways |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 3–4 | `tests/…#shipped_templates`, `#unreachable_templates`, `#ROUND_RECORD_FIELDS` | the units every fix of this run has touched; round 6 opens the fix diff again |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 7 of round 1 — the release guard's blind spot | issue #96, on the 0.5.0 milestone and in `docs/flow.md` before the release line | the orchestrator, before the release |
| ❓ 9 of round 1 — the design record still calls `pr.ko.md` a per-user setting | `docs/one-root-by-lifetime.md:449-450`, named in the pull request body | the repository owner |
| The pattern rounds 2–4 measured, and what bounds what a finding may create | issue #97, on 0.6.0, opened by the repository owner's reading of round 4's record | the repository owner, at 0.6.0 |
| The measurements themselves | issue #89 | the repository owner, at 0.6.0 |
