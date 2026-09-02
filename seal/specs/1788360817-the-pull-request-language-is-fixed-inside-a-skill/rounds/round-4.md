# 1788360817-the-pull-request-language-is-fixed-inside-a-skill — review round 4

<!-- The verifying round for round 3's fixes (target: the diff b64d1a6..85602b6).
It opened two things needing a fix, so it consumes the cap — and the cap was
already spent at three. What that means is written under "The cap, and what
this run does about it" below: the run does not take a fifth finding round.
It takes one fix pass that adds NO new unit, and one verifying round at that
diff, which is the only exit the record format leaves open. Written by the
review orchestrator. -->

| Field | Value |
|---|---|
| Target SHA | 85602b6 (the fix diff from b64d1a6); HEAD 2d610c2 at review time, record-only |
| PR | none yet |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written; round 5 verifies them and this cell is set to it then |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written, and this pass is required to add none |
| Needs a fix | yes — 발견 1 (`shipped_templates` 의 subprocess 에 `check=True` 가 없어 저장소를 읽지 못하는 상황이 "템플릿 없음"으로 읽히고, `test_an_untracked_file_under_templates_is_not_a_template` 은 단언이 `== []` 뿐이라 그 방향으로 실패하지 못함 — 라운드 3 발견 7 이 통과 근거로 적은 guard 가 사라짐) 과 발견 2 (`ROUND_RECORD_FIELDS` 가 템플릿에서 손으로 베껴져 템플릿에 대조되므로, 테스트·근거 대조표 `r3 3` 행·tests-todo 13행이 모두 "스킬이 명명한 필드"라고 부르는데 열한 개 중 네 개는 스킬에 없고, 스킬 쪽 표류를 이 pin 은 볼 수 없음) |

- [ ] Pass

## The cap, and what this run does about it

Rounds are capped at three, and at five only while a 🔴 is open
(`docs/review-chain-spec.md`). No 🔴 has been open since round 2 closed one.
This is the fourth round that found something, so the cap is spent and then
some, and the reason the spec gives for the bound is the one that applies:
a fourth round is normally not another finding, it is the loop failing to
converge.

**What is not converging, named.** Three rounds running, the finding has been
the same shape: a helper written to pin the last round's prose fix is new
code nobody has reviewed, and it carries the next round's finding.

| Round | Its fix added | The next round found |
|---|---|---|
| 1 | `configured_language`, the templates check | both of them reproducing the defect they closed |
| 2 | `mirror_to_refuse`, a widened glob | the glob out of step with the corpus it is compared against |
| 3 | `as_language_name`, `ROUND_RECORD_FIELDS`, a `git ls-files` helper | a missing `check=True`, a list hand-copied from the file it is checked against |

The findings shrink each time and they do not stop, because the surface that
produces them grows with every fix. That is the architecture to change rather
than the individual defect to fix again, which is what this repository's own
3+ Fix Rule asks for at exactly this point.

**So the fix pass that answers this round adds no new unit.** Both findings
close by correcting what exists: three arguments to a subprocess call that is
already there, one assertion line in a case that is already there, and three
claims narrowed to what actually runs. A pass that adds nothing new leaves
the verifying round's main yield surface — the units the fixes created —
empty, which is the only way this run reaches a round that opens nothing.
Round 5 is that round; if it opens something anyway, the loop has not
converged and the branch goes to a pull request with the finding named rather
than into a sixth round.

## Verdicts

Round 3's four items first, then what this round opened.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r3 1 | `shipped_templates` globbed the working tree while its corpus read git | `tests/…#shipped_templates` | answered — the fix is round 3's, this round reproduced its closure | reviewer executed: an untracked `templates/.DS_Store` in a scratch repository leaves `unreachable_templates` at `[]`, and swapping the pre-fix glob helper back turns it red |
| r3 2 | `mirror_to_refuse` skipped a language it knows | `tests/…#as_language_name`, `#mirror_to_refuse` | answered — reproduced | reviewer executed 17 values: six spellings of a known language answer a code; `French`, `Korean (KR)`, `ko`, `""` and `"***"` answer `None`. No non-language leaks through |
| r3 3 | the skill claimed an order the template does not have | `skills/code-review/SKILL.md:143-147` | answered for the order claim; the sentence that replaced it makes a new overclaim — this round's 2 | reviewer read the deletion and executed the field census |
| r3 4 | the ledger bullet said "no rows" | `skills/implement/SKILL.md:90-94`, `templates/ledger.md` | answered — reproduced | reviewer read the template: its clause tables carry placeholder rows only, so "clause tables arrive empty" is true |
| r3 6 | the ledger clause claimed more than the check runs | `seal/ledger/1788360817-…md` | answered — reproduced | reviewer read the narrowed clause and the census in its Notes |
| r3 drift | the five ledger rows the Bootstrap bullet moved a second time | `seal/ledger.md` S14, `seal/ledger/1788354065-…md:31, 32, 33, 62` | answered — re-read independently | reviewer opened `skills/implement/SKILL.md:36-165` against each claim: all five hold, and the re-read note is honest — the bullet that moved changed no claim's own text. Executed `evidence_check.py --strict .`: `355 ok · 0 drifted · 0 broken` |
| r3 glob | keeping `glob` for the mirror files | `tests/…:226` | pass, on narrower grounds than the smith gave | reviewer: "the directory rather than what is committed" was equally true of the defect round 3 found. What actually makes it safe is that `seal/specs/` is not gitignored, so no file can sit where the two readings differ |
| 1 | `shipped_templates`'s `subprocess.run` has no `check=True`, so a path that is not a repository, a repository with no `templates/`, and a helper replaced by `lambda root: []` all answer `[]` in silence. `test_an_untracked_file_under_templates_is_not_a_template` asserts only `== []` twice, so it cannot fail in the direction where the helper stops seeing anything — which is half of what it exists to pin, and it is the guard round 3 explicitly passed the file on | `tests/test_the_pull_request_language_is_the_repositorys.py:743-751, 917-940` | open | reviewer executed all three cases. The repository-wide case at `:816` still carries `assert shipped_templates(ROOT)`, so nothing passes vacuously today; the cost is one regression test doing half its job. Fix: `check=True`, and one existence assertion in the case — no new unit |
| 2 | `ROUND_RECORD_FIELDS` is hand-copied from `templates/sdd-round.md` and checked against `templates/sdd-round.md`, so it cannot fail in either direction. Three places call it the fields the skill names: the failure message, the ledger's `r3 3` row, and `tests-todo.md` row 13. Executed census: five of the eleven are spelled in `skills/code-review/SKILL.md`; `Broad gate`, `## Executed probes`, `## Inherited coordinates` and `## Deferred` are not, and `PR` and `## Verdicts` match only as substrings — `PR` anywhere, `## Verdicts` inside `### Verdicts that close too early`. Round 3's own finding said the template carries `PR` and the skill's row does not list it, and `PR` went into the list anyway | `tests/…:871-901`, `seal/ledger/1788360817-…md` `r3 3`, `tests-todo.md:19` | open | reviewer executed the census. Fix: narrow the three claims to what runs — the fields the template is expected to carry — exactly as round 3 closed its own finding 6. Adding the reverse-direction case would be a new unit and this pass adds none; the claim goes where the check is |
| 3 | `git ls-files` quotes a non-ASCII path by default (`core.quotePath`), so `shipped_templates` returns a C-escaped string no prose can name and the check reports it unreachable. Reproduced in a scratch repository whose prose names all three files | `tests/…:743-751` | open, and closed by the same three arguments as 1 | reviewer executed. The counter-argument the reviewer offered and this round accepts as insufficient: the helper only ever runs over this plugin's own twelve ASCII templates. It costs nothing to close here, and this work item is about repositories that do not write in English |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the test file | 66 passed |
| reviewer: `evidence_check.py --strict .` unscoped | `355 ok · 0 drifted · 0 broken` |
| reviewer: `fold_ledger.py --check`, `gather_changelog.py --check` | both name the two unreleased fragments; the pre-release state |
| reviewer: `as_language_name` / `mirror_to_refuse` over 17 values | six spellings of a known language answer a code; five non-languages answer `None` |
| reviewer: `shipped_templates` on a non-repository, a repository without `templates/`, and with the helper stubbed to `[]` | `[]` in all three, silently |
| reviewer: the new isolation case against the pre-fix glob helper | red, as it should be — that direction is pinned |
| reviewer: `shipped_templates` over a space path and a non-ASCII path | the space survives; the non-ASCII path comes back C-escaped and is reported unreachable |
| reviewer: the eleven `ROUND_RECORD_FIELDS` against the skill's prose | five spelled, four absent, two substring matches |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 3 | `tests/…#shipped_templates`, `#as_language_name`, `#ROUND_RECORD_FIELDS` | the units round 3's fixes created; round 5 opens the fix diff again |
| rounds 1–3 | `skills/commit-pr-convention/SKILL.md:46-80, 145-160` | where every prose fix of this work item lives |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 7 of round 1 — the release guard's blind spot | issue #96, on the 0.5.0 milestone and in `docs/flow.md` before the release line | the orchestrator, before the release |
| ❓ 9 of round 1 — the design record still calls `pr.ko.md` a per-user setting | `docs/one-root-by-lifetime.md:449-450`, named in the pull request body | the repository owner |
| The pattern this run measured — a fix's new units carry the next finding, three rounds running | issue #89, where the flow's measurements live, and the pull request body | the repository owner, at 0.6.0 |
