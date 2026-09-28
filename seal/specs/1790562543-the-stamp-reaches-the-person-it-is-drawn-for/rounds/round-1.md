# 1790562543-the-stamp-reaches-the-person-it-is-drawn-for — review round 1

| Field | Value |
|---|---|
| Target SHA | 69ad5e314022596314baa5e6b8cb6bb91e9c7451 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #650 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the SEALED line and the policy do not say how to recover a stamp the hook cannot draw), 🟡 2 (one malformed file loses the drawings claimed before it), 🟡 3 (the drawn refusal names a file that does not exist), 🟡 4 (both READMEs omit the new hook) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790562543 (#400), a first round against the whole branch `feat/400-the-stamp-reaches-the-person-it-is-drawn-for` at 69ad5e31, base origin/release/v0.15.7 (1fa25931), draft PR #650. Judge spec compliance against spec.md first (Scope In 1–6, S1–S17, the owner's 2026-09-28 comments on #400), including the build's one divergence (a terminal run without `--record` draws nothing, following the issue's *no other path draws one* over the spec's "as today") and whether it holds. Then quality. The class to enumerate: every path by which a stamp can reach a screen or a transcript (the gate on a terminal, on a pipe, with and without `--record`, red, refused; `seal-stamp` bare and `--from`; the Stop hook with and without `agent_id`, with zero, one and several undrawn files, another session's file, a subdirectory cwd, a worktree of the same clone) and every way it can draw twice, draw a sample as if it were a run, or draw a run that did not seal. And every sentence in agents/, skills/, docs/, templates/ and both READMEs that says where or how the stamp is drawn. The hook's rendering on a real screen (S17) cannot be observed by a case; say what a case can and cannot reach.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Where the hook cannot draw (python3 under 3.12, cwd outside the clone, plugin predating the hook), the `SEALED` line promises a drawing and names no recovery; the docstring and overview say it names `seal-stamp --from`, which only the no-session line does | `skills/verify/scripts/broad_gate.py:2413`, `hooks/sealer-stamp.py:40`, `docs/the-broad-gate.md:124` | open | probe A executed (3.9.6: exit 0, silent, file pending); `DRAWN_AT_TURN_END` read |
| 🟡 2 | A malformed values file raises after earlier files were claimed, so their drawings are lost and `--from` then refuses them | `hooks/sealer-stamp.py:92` | open | probe C executed: both files renamed, stdout empty, `--from` on the good file exit 2 |
| 🟡 3 | `seal-stamp --from X.drawn.json` says the values stay in `X.drawn.drawn.json`, which does not exist | `skills/verify/scripts/seal_stamp.py:683` | open | probe B executed |
| 🟡 4 | Neither README lists the `Stop` hook in its gate table, opt-in list, gate count or side effects | `README.md:107`, `README.md:181`, `README.md:390`, `README.ko.md:102`, `README.ko.md:383` | open | read |
| ⬜ 5 | The no-session line's `seal-stamp --from {path}` is unquoted | `skills/verify/scripts/broad_gate.py:2409` | open | read |
| ⬜ 6 | "which gate drew the stamp" and "which copy drew it" are now wrong in a sealer; "draws on a terminal only" omits the written cell | `agents/sealer.md:86`, `docs/the-broad-gate.md:88` | open | read |
| ⬜ 7 | The orchestrator's rule says a stamp is drawn; the `close --broad-gate` path draws none | `skills/code-review/orchestration.md:539` | open | read |
| ⬜ 8 | correction: spec, questions, plan and overview still state the terminal rule the build diverged from, and the overview says nothing was fed back | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/spec.md:48` | open | read; paperwork, not counted in Needs a fix |
| 🟢 | The divergence (terminal without `--record` draws nothing) holds against #400 §*Done when* bullet 4 | `skills/verify/scripts/broad_gate.py:2383` | confirmed | issue body and both 2026-09-28 comments read; neither comment names a terminal exception; S10 is stated for `--record` |
| 🟢 | No red, refused or chain-failing run reaches the values write or a draw | `skills/verify/scripts/broad_gate.py:2341` | confirmed | read: returns 1 and 2 precede `panel`; the S7 and S8 absences read `values_files` |
| 🟢 | No path draws one run twice: the terminal leaves no file, and hook and `--from` both claim before they print | `skills/verify/scripts/seal_stamp.py#claim` | confirmed | read; probes B and C show the rename happens before output |
| 🟢 | The hook draws nothing at a subagent's end, another event, another session's file or a repository not opted in, and draws from a subdirectory and a linked worktree | `hooks/sealer-stamp.py#main` | confirmed | the stamp module executed, 19 passed; probe E: a `cwd` that no longer exists below a worktree still draws |
| ❓ | S17: the stamp on the owner's screen after the orchestrator's text, unfolded, in colour, once; and several stamps in one message rendering whole | the harness | ❓ out of verified scope | no case can observe a screen; the owner answers on the first real run after merge |

## Paste-ready fixes

```python
DRAWN_AT_TURN_END = (
    " · the stamp is drawn at the end of the turn of session {session}, from "
    "{path}; where none appears, `seal-stamp --from {path}` draws it"
)
```
```markdown
`NOT SEALED` lines, and nothing is drawn. Wherever the `SEALED` line names
`seal-stamp --from`, quote it as it stands: that command is the person's to
type, and never yours.
```
```markdown
Nor is the hook's silence where it cannot draw. It draws nothing and says
nothing where the main session's `python3` is under 3.12, the floor
`seal_stamp.py` refuses below (macOS ships 3.9); where that session's working
directory is outside the clone the run sealed; or where its plugin predates
the hook. So every sealed `SEALED` line names `seal-stamp --from <path>`, and
a stamp that did not appear is drawn by hand from it, once.
```
```python
def drawings(stamp, directory):
    """The message block for every undrawn file in `directory`, oldest
    first. Each block is built whole before its file is claimed, so a file
    that is not a run's values, whatever it fails on, is left where it is
    and takes no other file's drawing with it."""
    blocks = []
    for path in stamp.pending(directory):
        try:
            values = stamp.read_values(path)
            block = "\n".join(
                [
                    stamp.label(values),
                    *stamp.stamp(values["rows"], values["scale"], shape=False),
                ]
            )
        except Exception:
            continue
        if stamp.claim(path) is None:
            continue
        blocks.append(block)
    return blocks
```
```python
    if path.endswith(DRAWN) or (
        not os.path.exists(path) and os.path.exists(drawn_path(path))
    ):
        drawn = path if path.endswith(DRAWN) else drawn_path(path)
        raise ValueError(VALUES_DRAWN.format(path=path, drawn=drawn))
```
```markdown
| sealer-stamp | when the main session's turn ends (`Stop`) | draws, once and after the turn's text, each sealed run's stamp the broad gate left for this session under `<git-common-dir>/specseal-stamp/<session>/`, and renames the file `.drawn.json`. Nothing at a subagent's end, for another session's file, or under a `python3` older than 3.12; `seal-stamp --from <file>` draws one by hand | `seal/` at the root, or under the common git dir in local mode — silent elsewhere |
```
```markdown
Eight of the eleven gates wake only under a condition: the commit gate, the
mode gate, the review-history reminder, the two implementer hooks, the
review-skill gate, the stamp hook and the version check act in a
```
```markdown
| sealer-stamp | 메인 세션의 턴이 끝날 때 (`Stop`) | 광역 관문이 이 세션 앞으로 `<git-common-dir>/specseal-stamp/<session>/` 에 남긴 봉인 도장을, 턴의 글이 다 나온 뒤에 한 번 그리고, 그 파일의 이름을 `.drawn.json` 으로 바꾼다. 서브에이전트가 끝날 때, 다른 세션의 파일, 3.12 보다 낮은 `python3` 에서는 그리지 않는다. 손으로 그리려면 `seal-stamp --from <file>` 이다 | 루트에 `seal/` 이 있는 레포, 또는 local 모드로 공통 git 디렉터리 아래에 있는 레포. 그 밖에서는 아무것도 하지 않는다 |
```
```markdown
게이트 열하나 중 여덟은 조건이 맞아야 깨어납니다. 커밋 게이트와 모드 게이트,
리뷰 이력 알림, 구현자 훅 둘, 리뷰 스킬 게이트, 도장 훅, 버전 확인은 레포 루트에, 또는
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -q`, in a `git clone --no-local` at 69ad5e31 | 19 passed, exit 0 |
| `bin/test` over the stamp module and the gate module, `-k` on stamp, values, terminal, signal, session, drawn, `pick_shape`, `is_terminal`, stop and scale | 40 passed, exit 0 |
| Probe A: `dispatch.py stop` under `/usr/bin/python3` 3.9.6, one pending file | exit 0, stdout empty, stderr empty, file still pending |
| Probe A2: `dispatch.py post-bash` under the same interpreter | exit 0, stderr empty |
| Probe B: `seal-stamp --from` on a file's `.drawn.json` name after one draw | exit 2; the refusal names `….drawn.drawn.json`, which does not exist |
| Probe C: two pending files, the newer with `item` 5, then `Stop` | exit 0, stdout empty, both renamed `.drawn.json`; `--from` on the older one then exit 2, "drawn already" |
| Probe D: `dispatch.py stop` with no session directory, ten runs | median 24.1 ms, against 22.1 ms for an empty payload; the stamp module loads in about 0.1 ms. No efficiency finding |
| Probe E: `Stop` with a `cwd` that does not exist, below a linked worktree | drawn |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's, once, after the rounds settle |
| The orchestrator's `evidence_check.py .` and `--strict` at 69ad5e31 | not run in this round; relayed as exit 0 by the orchestrator |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The early-draw window, made likely rather than rare by a release that seals several items in one session: another item's completion notification starts a main turn after one gate wrote its file and before that sealer reported. The label names the item, so the stamp is identifiable, but it sits under another item's text. The plan gave two reasons to defer arming at `SubagentStop`; the second (`SubagentStop`'s `session_id` unmeasured) was answered by Q2 on 2026-09-28 | already deferred in this work item's questions.md Q3 | the orchestrating session, by watching this release's sealer runs |
