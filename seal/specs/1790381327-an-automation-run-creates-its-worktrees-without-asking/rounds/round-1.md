# 1790381327-an-automation-run-creates-its-worktrees-without-asking — review round 1

| Field | Value |
|---|---|
| Target SHA | 8fe503484257e112ef14fb40699b319e42adcd8c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 622 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `cc48effe2b6af6a7736b1f40f2658e46dc9522dd..c6ee7a3ce36cdb2e01dd55f1315e90803e6c6c78`, 3 commits |
| Contract changes | consent → guard_worktree_creation, main, round-1-report.md, round-1.md, pytest |
| New units | test_a_typed_answer_that_qualifies_the_preset_is_not_consent (depth 1); test_a_sidechain_entry_is_not_consent (depth 1); dispatch_pre_bash (depth 1); test_a_shape_the_reader_did_not_expect_keeps_the_guards_deny (depth 1); test_the_reader_itself_answers_both_shapes_without_raising (depth 1); test_consent_fails_closed_on_any_exception (depth 1); test_the_token_rows_count_sentence_is_said_only_where_a_count_was_taken (depth 1) |
| Needs a fix | yes — 1 (typed answer read as the preset), 2 (the consent read raises and the deny is dropped), 3 (README guard row), 4 (the `[worktree-ok]` sentence in the unusable state) |
| Loses a record or crashes | yes — 2: the consent read raises on a list-valued `tool_use_id` or a NUL in `transcript_path`, and the guard's deny is lost through `dispatch.py` |

- [x] Pass

## What this round was asked

Round 1 of work item 1790381327 reviews the build at 8fe50348 against spec.md and plan.md (frame 693f1bf6, approved a0eaeea9). It covers #604, where the guard takes the owner's routing answer in the session transcript as consent to create a worktree, and #8, where an isolated Agent is judged as concurrent work. The weight is on forgeability: every shape of transcript entry the model could write that the reader might mistake for a harness-written `automation` click. Then failing closed on every read error, the decision table row by row against the code, and every sentence in the tree stating when the guard asks.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A typed `Other` answer that qualifies the preset (*automation - but ask me first*) is read as the person pressing `automation` | `hooks/worktree_consent.py:220` | **fixed** `7edc628bf4627153d41346aacddaa0cad20ac86a` | fixed at 7edc628bf4627153d41346aacddaa0cad20ac86a; P1: three typed answers read as consent. 184/184 pressed answers on disk equal a label, so requiring a label match loses no measured case |
| 🟡 2 | The consent read raises on an unhashable `tool_use_id` or a NUL in `transcript_path`, and the guard's deny becomes no decision through `dispatch.py` | `hooks/worktree_consent.py:299` | **fixed** `7edc628bf4627153d41346aacddaa0cad20ac86a` | fixed at 7edc628bf4627153d41346aacddaa0cad20ac86a; P2, P3 raise. P8: `deny` → none for the same command. Contradicts the docstring, spec S8 and ledger A1 |
| 🟡 3 | The README guard row says the Agent path is denied or offered options and names neither consent source | `README.md:188` | **fixed** `7edc628bf4627153d41346aacddaa0cad20ac86a` | fixed at 7edc628bf4627153d41346aacddaa0cad20ac86a; Agent path now always asks without consent (A5). The row predates the change, and this branch made its Agent clause false. Same row in `README.ko.md:184` |
| 🟡 4 | The `[worktree-ok]` row's first sentence asserts *no other Claude session is working* in the detection-unusable state, where nothing was counted | `hooks/worktree-guard.py:1757` | **fixed** `7edc628bf4627153d41346aacddaa0cad20ac86a` | fixed at 7edc628bf4627153d41346aacddaa0cad20ac86a; Worktree-ok probe with `reliable=False`. The row's own comment says that state reaches it |
| ⬜ 5 | Reader docstring says a long transcript costs a substring test per line; nearly every tool-result line is parsed | `hooks/worktree_consent.py:261` | **fixed** `7edc628bf4627153d41346aacddaa0cad20ac86a` | fixed at 7edc628bf4627153d41346aacddaa0cad20ac86a; P9: 0.09 s on 17.3 MB, so a sentence fix only |
| ⬜ 6 | Ledger row A1 says *nothing raises*, which finding 2 shows false | `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md` | answered | corrected at 2eb566c1e58bd8489eebdf521eb072884036e26b: after 🟡 2's fix, A1's *nothing raises* and its *answered `automation`* were both false; the clause is corrected in place with a `Corrected 2026-09-26` note; Correction to the run's paperwork. It follows finding 2's resolution |
| 🟢 | Forgery shapes the prompt named are refused: assistant look-alike, pasted block, unlinked result, fourth option, multiSelect, absent multiSelect, another clone, another session's file | `hooks/worktree_consent.py:238` | confirmed | P5a–c, P6a–c, P7, plus the suite's cases for order and clone |
| 🟢 | Failure closed on a missing file, a directory in place of the file, and truncated or non-object lines; cost on 17.3 MB is under 0.1 s | `hooks/worktree_consent.py:267` | confirmed | P3b, P9, suite. The two exceptions are finding 2 |
| 🟢 | The switch direction reads neither consent; §B's table matches the code row for row | `hooks/worktree-guard.py:1648` | confirmed | Two call sites only; seven rows compared |
| 🟢 | Removing the session count opens nothing but the Agent path | `hooks/worktree-guard.py:1972` | confirmed | The removed parameters had no Bash caller; `judge_creation` passes two keywords |
| 🟢 | The six corrected 0.9.1 rows, 0.9.4 S3/S4 and A2–A5 say what the code does | `seal/releases/0.9.1.md` | confirmed | Read against the target SHA |
| ❓ | Whether the harness can ever write a linked `AskUserQuestion` result marked `isSidechain: true` into a main transcript. The reader accepts one (P4) | `hooks/worktree_consent.py:297` | ❓ out of verified scope | 0 sidechain entries in 67 main transcripts, and a subagent has no `AskUserQuestion`. A live-harness measurement answers it: the orchestrator |

## Paste-ready fixes

```python
    for q in questions:
        if not isinstance(q, dict) or q.get("multiSelect") is not False:
            continue
        options = q.get("options")
        if not isinstance(options, list):
            continue
        labels = [o.get("label") if isinstance(o, dict) else None for o in options]
        phrases = sorted(leading_phrase(label) for label in labels)
        if phrases != sorted(ROUTING_LABELS):
            continue
        text = q.get("question")
        if not isinstance(text, str):
            continue
        # A pressed option's answer IS its label; an `Other` answer is the
        # person's own text, written verbatim, and cutting it at a decoration
        # would read "automation - but ask me first" as the preset.
        answer = answers.get(text)
        if isinstance(answer, str) and answer in labels and leading_phrase(answer) == PRESET:
            return True
    return False
```
```python
def test_the_routing_preset_is_consent(projects, repo):
    """The measured answer, and the three decorations measured beside it --
    each on the pressed option's label, which is where a decoration lives."""
    for answer in (
        "automation",
        "automation (Recommended)",
        "automation (권장)",
        "automation — 안 멈추고 끝까지",
    ):
        options = (answer, "per axis", "no work item")
        write_transcript(projects, "me", ask_entries(repo, answer=answer, options=options))
        assert wc.automation_answered(str(repo), "me"), answer
        assert wc.consent(str(repo), "me") == "answer", answer


def test_a_typed_answer_that_qualifies_the_preset_is_not_consent(projects, repo):
    """An `Other` answer is the person's own text, written into `answers`
    verbatim. Only a pressed option's label is an answer the guard reads."""
    for typed in (
        "automation - but ask me before each worktree",
        "automation (stop before creating worktrees)",
        "automation — 단, worktree 는 물어봐",
    ):
        write_transcript(projects, "me", ask_entries(repo, answer=typed))
        assert not wc.automation_answered(str(repo), "me"), typed
```
```python
                linked = any(
                    isinstance(item, dict)
                    and item.get("type") == "tool_result"
                    and isinstance(item.get("tool_use_id"), str)
                    and item["tool_use_id"] in asked
                    for item in _content(entry)
                )
```
```python
    except (OSError, ValueError):
        return False
    return False
```
```python
def consent(top: str, session: str, transcript_path: str = "") -> str:
    """Which consent this session holds for splitting this clone, or "".

    ...docstring unchanged...
    """
    if granted(top, session):
        return "record"
    # `hooks/dispatch.py` skips a gate that raises, so a read that raises
    # drops the guard's verdict altogether and a deny becomes silence. Every
    # exception here is therefore "no consent", the verdict before the answer
    # was read.
    try:
        answered = automation_answered(top, session, transcript_path)
    except Exception:
        answered = False
    return "answer" if answered else ""
```
```python
def test_a_shape_the_reader_did_not_expect_never_raises(
    monkeypatch, capsys, projects, repo
):
    """A gate that raises is skipped by `dispatch.py`, which turns the
    single-stream deny into no decision at all."""
    use, result = ask_entries(repo)
    result["message"]["content"][0]["tool_use_id"] = ["toolu_01routing"]
    write_transcript(projects, "me", [use, result])
    assert wc.consent(str(repo), "me") == ""
    assert wc.consent(str(repo), "me", "/x/\x00y/me.jsonl") == ""
    decision, reason = decide(monkeypatch, capsys, repo, "git worktree add ../wt f")
    assert decision == "deny" and "git switch" in reason
```
```text
one rule in two directions: denies a switch while another session is actively working this tree, and denies a Bash `git worktree add` when yours is the only live stream. Where the tree holds only idle sessions, or the environment cannot be read at all, a Bash creation is offered the two ways on as options instead — switch here, or split into a worktree — **once per session per repository per direction**, then the plain confirmation. An Agent call with `isolation: "worktree"` counts no sessions: the agent runs beside this session, so the call is concurrent work and asks once. A creation is not asked again once one has run in the session, and not at all where you pressed `automation` on the routing question. The two directions are counted apart, so one session can legitimately meet the question twice. `[worktree-ok]` and `[shared-tree-ok]` carry your answer back through on the retry. The reason names the other session's host app, how long each signal has been quiet, and its last message
```
```text
한 규칙의 두 방향이다. 다른 세션이 이 트리에서 작업 중이면 전환을 막고, 반대로 혼자 작업 중이면 Bash 의 `git worktree add` 를 막는다. 멈춘 세션뿐이거나 판정 자체가 불가능한 환경에서는 Bash 생성에 갈 수 있는 두 길을 선택지로 띄운다 — 이 트리에서 전환하거나, worktree 로 분리하거나. **세션·레포·방향당 한 번**만 이렇게 묻고 그 다음부터는 일반 확인창이며, 고른 답은 `[worktree-ok]` 와 `[shared-tree-ok]` 가 재시도 때 그대로 실어 나른다. `isolation: "worktree"` 로 부른 Agent 는 세션을 세지 않는다. 이 agent 는 이 세션과 나란히 도는 동시 작업이므로 확인창을 한 번 띄운다. 한 세션에서 생성이 한 번 실행된 뒤에는 다시 묻지 않고, 라우팅 질문에서 `automation` 을 눌렀다면 처음부터 묻지 않는다. 두 방향을 따로 세므로 한 세션이 이 질문을 두 번 만나는 것은 정상이다. 사유에는 상대 세션의 호스트 앱, 신호별 경과 시간, 마지막 메시지가 함께 나온다
```
```python
    if user_ok:
        respond(
            "ask",
            (
                f"{origin}\n"
                # Reached before the choice rows, detection-unusable included,
                # so the count is named only where one was taken.
                + (
                    tr(
                        "No other Claude session is working in this tree, but ",
                        "이 트리에서 작업 중인 다른 Claude 세션은 없지만 ",
                    )
                    if reliable
                    else ""
                )
                + tr(
                    "[worktree-ok] was given — treating this as the user's explicit "
                    "intent. Confirm the worktree creation. Declining withdraws "
                    "[worktree-ok] and proceeds in the shared tree instead:\n",
                    "[worktree-ok] 가 지정되어 사용자 의사로 판단합니다. worktree 를 "
                    "생성할지 확인해 주세요. 거부하면 [worktree-ok] 선언을 철회하고 공유 "
                    "트리에서 그대로 진행합니다:\n",
                )
                + steer_to_switch()
            ),
        )
```

## Executed probes

| What was run | Result |
|---|---|
| P1 — three typed `Other` answers that qualify the preset, against `automation_answered` | all three `True` (finding 1) |
| P1b — a model-written option label *automation — ask before every worktree*, pressed | `True` (outside the stated threat model; noted in finding 1) |
| P2 — a user entry whose `tool_use_id` is a list, after a real ask | `TypeError` raised from `automation_answered` and from `consent` |
| P3 — `transcript_path` with a NUL byte and a matching basename | `ValueError` raised |
| P3b — `transcript_path` naming a directory called `<session>.jsonl` | `False` |
| P4 — a linked routing result with `isSidechain: true` | `True` (the ❓ row) |
| P5 — fourth option / `multiSelect: true` / `multiSelect` absent | `False` ×3 |
| P6 — unlinked result / assistant text quoting a full result / user pasted block after a real ask | `False` ×3 |
| P7 — `transcript_path` naming another session's file that holds an answer | `False` |
| P8 — `dispatch.py pre-bash`, single-stream `git worktree add`, no answer: well-formed / list id / NUL path | `deny` / none / none, exit 0 each |
| P9 — cost: largest local transcript (17.3 MB); synthetic 17.3 MB, 4378 tool-result lines, no answer | 0.089 s / 0.071 s, both `False` |
| Worktree-ok probe — `[worktree-ok]` creation with `reliable=False`, then with only an idle session | `ask`, both reasons open *No other Claude session is working in this tree* |
| Transcript shape census over 67 local transcripts (aggregates only) | 184 pressed answers equal a label; 16 free-text single-select answers; 0 sidechain entries in main files; 0 foreign `sessionId`; 0 model-supplied `answers` in 137 asks |
| Sentence-class sweep: `git grep` for creation-asking and Agent-path statements in English and Korean (*without isolation*, *first creation*, *once per session*, *single-stream*, *세션마다*, *처음 한 번*, *worktree 생성*, *isolation 없이*, and others) over `README*`, `CONTRIBUTING.md`, `CLAUDE.md`, `templates/`, `skills/`, `agents/`, `hooks/`, `docs/` | finding 3; nothing else stale |
| `bin/test tests/test_the_guard_asks_once_per_session.py tests/test_worktree_guard.py tests/test_worktree_guard_signals.py -q` | 164 passed, 1 skipped (the three modules the diff touched) |
| Full suite, lint and typecheck (the broad gate) | not yet — the sealer's, once, after the rounds settle |
| `evidence-check` over the new fragment | not yet — not run this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A switch written after a creation in one command is never judged when consent is present | already filed as #620 before this round (spec Q3) | the owner, in the milestone that takes #620 |
