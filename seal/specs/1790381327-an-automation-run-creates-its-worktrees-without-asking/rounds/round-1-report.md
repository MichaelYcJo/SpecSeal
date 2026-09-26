# Round 1 report — an automation run creates its worktrees without asking (#604, #8)

- Target SHA: `8fe50348` · Base: `origin/release/v0.15.5` = `47e32d57` · Range `47e32d57..8fe50348`
- Ran by: specseal:warden on claude-opus-5-5
- Worked in a `git clone --no-local` at the target SHA under the session scratchpad; nothing was written in the user's checkout except this file.
- The implementer's account (spec, plan, overview, phase records, ledger rows, commit messages) was read in full and treated as claims. Where a claim is confirmed or contradicted below, the coordinate says which.

## Summary

The change is sound where it was weighed hardest. Every forgery shape the prompt named is refused: an assistant look-alike, a pasted block, an unlinked `tool_result`, a fourth option, a multiSelect, an absent `multiSelect`, an answer from another clone, and another session's transcript named by the payload. The switch direction reads neither consent, the doc's §B table matches the code row for row, and removing the session count reaches the Agent path only. The scan costs 0.09 s on the largest local transcript (17.3 MB).

Four things need a fix or grounds. They are ordered by cause.

1. **The reader treats a person's typed answer as a pressed option.** An `Other` answer is free text, which the harness writes verbatim into `answers`. The leading-phrase rule cuts that text at ` -` or ` (`. So *automation - but ask me before each worktree* is read as the preset.
2. **The reader can raise, and a gate that raises loses its verdict.** `hooks/dispatch.py` skips a gate that raises. Two malformed inputs make the consent read raise, and the single-stream `deny` then becomes no decision at all (executed, P8b/P8c). The docstring and ledger row A1 both say *nothing raises*.
3. **The README row for the guard is now false for the Agent path**, and it says nothing about either consent source. The sentence-class sweep found this one. The smith's list did not include it.
4. **The rewritten `[worktree-ok]` sentence asserts a measurement that was not made.** In the detection-unusable state, which the row's own comment names as a state that reaches it, the guard says *No other Claude session is working in this tree*.

Two ⬜ corrections follow: the reader docstring's cost sentence, and ledger row A1's *nothing raises*.

## Findings from execution

### 🟡 1 — a typed `Other` answer that qualifies the preset is read as consent

`hooks/worktree_consent.py:220-222` (`_routing_preset`), with `leading_phrase` at `:146-159`.

`leading_phrase` is applied to the **answer** as well as to the options. For a pressed option the answer is the label verbatim. I measured this over the local transcripts: 184 of 184 pressed single-select answers equal one of their question's labels. The harness also writes an `Other` answer into `answers` verbatim, and 16 single-select answers on disk are free text that matches no label. So a person who types a qualified answer has their own words cut at the first decoration mark:

| Typed in `Other` | Read as |
|---|---|
| `automation - but ask me before each worktree` | consent (P1.0) |
| `automation (but stop before creating worktrees)` | consent (P1.1) |
| `automation — 단, worktree 는 물어봐` | consent (P1.2) |

Why it matters: the guard's claim is that it acts only on *which option the person pressed*. Here the person pressed none, and wrote the opposite of what the guard concludes. The first creation then gets `allow`, which bypasses the person's own permission settings for the whole call.

The fix is to require that the answer *is* one of that question's option labels before its leading phrase is read. That is what "pressed" means. It also keeps every measured decoration, because each one is on the label. The existing case `test_the_routing_preset_is_consent` pairs decorated answers with a fixed `automation (Recommended)` option. That shape is impossible for a pressed option, so the case has to pass matching options, and the fix block updates it too.

A related residue that the fix does not close: the model writes the option labels. An option reading *automation — ask before every worktree* is read as the preset when it is pressed (P1b). That is deception rather than habit, which is outside the threat model `spec.md` states, so it is not a finding. It is recorded here so the next reader does not rediscover it.

### 🟡 2 — the consent read raises on two malformed inputs, and the guard's verdict is dropped

`hooks/worktree_consent.py:299-304` and `:275-314`, reached from `hooks/worktree-guard.py:1648` and `:1977`.

- A `tool_result` whose `tool_use_id` is not hashable (a list) raises `TypeError: unhashable type` at `item.get("tool_use_id") in asked` (P2).
- A `transcript_path` whose basename is `<session>.jsonl` but which contains a NUL byte is returned by `transcript_for`. `open` then raises `ValueError: embedded null byte`, and only `OSError` is caught (P3).

Through `dispatch.py pre-bash`, in a clean single-stream repository with no answer, the same Bash `git worktree add` gets these decisions (P8):

| Transcript input | Decision |
|---|---|
| well-formed, no answer | `deny` |
| list-valued `tool_use_id` | **none** |
| NUL in `transcript_path` | **none** |

Why it matters: the prompt's *failure closed* axis requires every read error to fall back to the verdict before the change. `dispatch.py`'s docstring makes a raising gate fail **open** by design, so any exception in this read turns a deny into silence. Neither input is one the harness is known to write. That is why this is 🟡 rather than 🔴. The same claims are made in `automation_answered`'s docstring (*nothing here raises*), in spec S8 (*no traceback*) and in ledger row A1 (*nothing raises*), and all three are false as written.

This is a class, and there are two instances because the read has more than one place to raise. The fix has two layers. The two narrow repairs cover the instances found. A catch-all in `consent`, the one function both call sites use, closes the class by construction, so the next unexpected shape also answers *no consent*.

### 🟡 4 — the `[worktree-ok]` row's new first sentence claims a count that was not taken

`hooks/worktree-guard.py:1757-1766`.

The rewrite's stated purpose (`spec.md` §Scope) is that the sentence *names what was measured*. The row is reached after the ACTIVE check and **before** the idle and detection-unusable choice sites. The row's own Korean comment at `:1732-1734` says that ordering exists for the detection-unusable case. In that state nothing was counted, yet the reason reads *No other Claude session is working in this tree* (executed, the worktree-ok probe: `reliable=False` → `ask` with that sentence). The old *Single-stream work* sentence was wrong in the same state. What is new is that the sentence now presents itself as a measurement. §14 applies because a person reads it.

## Findings from reading

### 🟡 3 — the README's guard row no longer describes the Agent path or the creation budget

`README.md:188`, `README.ko.md:184`.

The row's trigger column includes *Agent calls with `isolation: "worktree"`*. It then says the guard *denies creating a worktree when yours is the only live stream*, and that where only idle sessions remain, or detection is unusable, *it offers the two ways on as options*. After this branch the Agent path is never denied and never offered options (A5, `hooks/worktree-guard.py:1972-1998`). Before it, the Agent path did reach both choice sites, so this branch is what makes that clause false. The row also names neither consent source. The most visible change in this release is that a person who pressed `automation` is not asked at all, and this row, which is the user's description of the gate, does not say so.

`README.md:289` and `README.ko.md:280` (*an Agent call … asks outright instead*) are still true, and so are `CLAUDE.md:15` and `templates/claude-md-block.md:15`, which are Q2 and stay at its default. No other sentence in `README*`, `CONTRIBUTING.md`, `templates/`, `skills/`, `agents/` or the hook docstrings states when the guard asks for a creation or how the Agent path is judged. That was searched in English and Korean with the phrasings in the probes table. `skills/implement/orchestration.md` §*`Automation` is an audit trail, not a gate* and `hooks/routing.py`'s `AUTOMATION` comment speak of the `routing.md` row, and the row still gates nothing.

### ⬜ 5 — the reader's cost sentence is not what the prefilter does

`hooks/worktree_consent.py:261-262`: *A line is parsed only when it could matter to one of the two roles, so a long transcript costs a substring test per line.* Every harness tool-result line carries the key `toolUseResult`, so nearly every user line reaches `json.loads`. The behaviour is fine: 0.089 s on the largest local transcript and 0.071 s on a synthetic 17.3 MB one with no answer (P9). The sentence overstates what the prefilter skips.

### ⬜ 6 — ledger row A1 says *nothing raises* (correction)

`seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md`, row A1. This is false as of the target SHA (finding 2). It should be corrected in place when finding 2 is fixed, or reworded if finding 2 is answered with grounds instead. This is paperwork and does not count toward `Needs a fix`.

## Axes confirmed

- **Forgeability.** Each of the four reading rules was probed with a crafted transcript (P5–P7): an assistant message quoting a whole result, a user entry that pastes a result after a real ask, a result whose `tool_use_id` names no ask, a result before its question (covered by the suite), a fourth option, `multiSelect: true`, `multiSelect` absent, and a `transcript_path` naming another session's file. All answer *no consent*. A `user` entry marked `isSidechain: true` **is** accepted (P4). That entry cannot arise from what was measured: across 67 local transcripts there are 0 sidechain entries in main files, and a subagent has no `AskUserQuestion`. It is the ❓ row below.
- **Other sessions and resumes.** 0 of 67 local transcripts hold an entry whose `sessionId` differs from the file's name. So no copied-in answer from another session was found to reach the reader. `AskUserQuestion` inputs carry no model-supplied `answers` in 137 of 137 calls.
- **The switch direction.** `worktree_consent.consent` has exactly two call sites, `hooks/worktree-guard.py:1648` (row 0 of the creation ladder) and `:1977` (the Agent block). The switch ladder reads neither (A4, read and covered by the suite).
- **The §B table against the code, row by row.** The rows checked were the consent row (allow when the call only creates, silent when it does more, silent on the Agent path), ACTIVE → ask, IDLE → choice, unusable → choice, `[worktree-ok]` → ask, single-stream Bash → deny, and Agent without consent → ask. All seven match `guard_worktree_creation` and `main`. One precedence note is not new to this diff: the code tests `[worktree-ok]` before the two choice rows, while the table lists it after them.
- **#8.** The three removed parameters were set only by the Agent path; `judge_creation`, the Bash path's one caller, passes `consented` and `transcript_path` and nothing else. Removing the count loosens only the Agent path: idle and unusable go from choice deny to `ask`. That is spec S4.
- **Ledger.** The six corrected rows of `seal/releases/0.9.1.md` and S3/S4 of `seal/releases/0.9.4.md` were checked against the code, and each corrected claim holds. A2–A5 hold. A1 holds except for *nothing raises* (finding 6).

## Regression tests to plant

In `tests/test_the_guard_asks_once_per_session.py`, with both cases in the fenced blocks below:

- For finding 1: a typed `Other` answer that qualifies the preset is not consent. It is red against the target SHA (P1 shows the reader answering `True`).
- For finding 2: a shape the reader did not expect never raises, and the guard still denies. It is red against the target SHA (P2/P3 raise, and P8 shows the verdict dropped).

## Facts for the evidence ledger

- The harness writes an `Other` answer to `AskUserQuestion` verbatim into `toolUseResult.answers`. A pressed option's answer equals its label verbatim. Measured over 67 local transcripts on 2026-09-26: 184 pressed single-select answers match a label, 16 free-text answers match none. This belongs as a note on A1 once finding 1 is fixed.
- `toolUseResult.annotations` exists beside `questions` and `answers` (118 of 118 dict results), and it holds only `preview` in every instance on disk.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A typed `Other` answer that qualifies the preset (*automation - but ask me first*) is read as the person pressing `automation` | `hooks/worktree_consent.py:220` | open | P1: three typed answers read as consent. 184/184 pressed answers on disk equal a label, so requiring a label match loses no measured case |
| 🟡 2 | The consent read raises on an unhashable `tool_use_id` or a NUL in `transcript_path`, and the guard's deny becomes no decision through `dispatch.py` | `hooks/worktree_consent.py:299` | open | P2, P3 raise. P8: `deny` → none for the same command. Contradicts the docstring, spec S8 and ledger A1 |
| 🟡 3 | The README guard row says the Agent path is denied or offered options and names neither consent source | `README.md:188` | open | Agent path now always asks without consent (A5). The row predates the change, and this branch made its Agent clause false. Same row in `README.ko.md:184` |
| 🟡 4 | The `[worktree-ok]` row's first sentence asserts *no other Claude session is working* in the detection-unusable state, where nothing was counted | `hooks/worktree-guard.py:1757` | open | Worktree-ok probe with `reliable=False`. The row's own comment says that state reaches it |
| ⬜ 5 | Reader docstring says a long transcript costs a substring test per line; nearly every tool-result line is parsed | `hooks/worktree_consent.py:261` | open | P9: 0.09 s on 17.3 MB, so a sentence fix only |
| ⬜ 6 | Ledger row A1 says *nothing raises*, which finding 2 shows false | `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md` | open | Correction to the run's paperwork. It follows finding 2's resolution |
| 🟢 | Forgery shapes the prompt named are refused: assistant look-alike, pasted block, unlinked result, fourth option, multiSelect, absent multiSelect, another clone, another session's file | `hooks/worktree_consent.py:238` | confirmed | P5a–c, P6a–c, P7, plus the suite's cases for order and clone |
| 🟢 | Failure closed on a missing file, a directory in place of the file, and truncated or non-object lines; cost on 17.3 MB is under 0.1 s | `hooks/worktree_consent.py:267` | confirmed | P3b, P9, suite. The two exceptions are finding 2 |
| 🟢 | The switch direction reads neither consent; §B's table matches the code row for row | `hooks/worktree-guard.py:1648` | confirmed | Two call sites only; seven rows compared |
| 🟢 | Removing the session count opens nothing but the Agent path | `hooks/worktree-guard.py:1972` | confirmed | The removed parameters had no Bash caller; `judge_creation` passes two keywords |
| 🟢 | The six corrected 0.9.1 rows, 0.9.4 S3/S4 and A2–A5 say what the code does | `seal/releases/0.9.1.md` | confirmed | Read against the target SHA |
| ❓ | Whether the harness can ever write a linked `AskUserQuestion` result marked `isSidechain: true` into a main transcript. The reader accepts one (P4) | `hooks/worktree_consent.py:297` | ❓ out of verified scope | 0 sidechain entries in 67 main transcripts, and a subagent has no `AskUserQuestion`. A live-harness measurement answers it: the orchestrator |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A switch written after a creation in one command is never judged when consent is present | already filed as #620 before this round (spec Q3) | the owner, in the milestone that takes #620 |

## Paste-ready fixes

### 🟡 1 — `hooks/worktree_consent.py`, `_routing_preset`

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

### 🟡 1 — `tests/test_the_guard_asks_once_per_session.py`, the existing case updated and the new one

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

### 🟡 2 — `hooks/worktree_consent.py`, the two instances and the class

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

### 🟡 2 — `tests/test_the_guard_asks_once_per_session.py`

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

### 🟡 3 — `README.md:188`, the third cell

```text
one rule in two directions: denies a switch while another session is actively working this tree, and denies a Bash `git worktree add` when yours is the only live stream. Where the tree holds only idle sessions, or the environment cannot be read at all, a Bash creation is offered the two ways on as options instead — switch here, or split into a worktree — **once per session per repository per direction**, then the plain confirmation. An Agent call with `isolation: "worktree"` counts no sessions: the agent runs beside this session, so the call is concurrent work and asks once. A creation is not asked again once one has run in the session, and not at all where you pressed `automation` on the routing question. The two directions are counted apart, so one session can legitimately meet the question twice. `[worktree-ok]` and `[shared-tree-ok]` carry your answer back through on the retry. The reason names the other session's host app, how long each signal has been quiet, and its last message
```

### 🟡 3 — `README.ko.md:184`, the third cell

```text
한 규칙의 두 방향이다. 다른 세션이 이 트리에서 작업 중이면 전환을 막고, 반대로 혼자 작업 중이면 Bash 의 `git worktree add` 를 막는다. 멈춘 세션뿐이거나 판정 자체가 불가능한 환경에서는 Bash 생성에 갈 수 있는 두 길을 선택지로 띄운다 — 이 트리에서 전환하거나, worktree 로 분리하거나. **세션·레포·방향당 한 번**만 이렇게 묻고 그 다음부터는 일반 확인창이며, 고른 답은 `[worktree-ok]` 와 `[shared-tree-ok]` 가 재시도 때 그대로 실어 나른다. `isolation: "worktree"` 로 부른 Agent 는 세션을 세지 않는다. 이 agent 는 이 세션과 나란히 도는 동시 작업이므로 확인창을 한 번 띄운다. 한 세션에서 생성이 한 번 실행된 뒤에는 다시 묻지 않고, 라우팅 질문에서 `automation` 을 눌렀다면 처음부터 묻지 않는다. 두 방향을 따로 세므로 한 세션이 이 질문을 두 번 만나는 것은 정상이다. 사유에는 상대 세션의 호스트 앱, 신호별 경과 시간, 마지막 메시지가 함께 나온다
```

### 🟡 4 — `hooks/worktree-guard.py`, the `[worktree-ok]` row

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

Needs a fix: yes — 1 (typed answer read as the preset), 2 (the consent read raises and the deny is dropped), 3 (README guard row), 4 (the `[worktree-ok]` sentence in the unusable state)
Loses a record or crashes: yes — 2: the consent read raises on a list-valued `tool_use_id` or a NUL in `transcript_path`, and the guard's deny is lost through `dispatch.py`

## Proof block

Files opened this round, at `8fe50348` unless noted:

- `hooks/worktree_consent.py` (whole), `hooks/worktree-guard.py` (diff, and lines 1676-1830, 1960-2000), `hooks/dispatch.py` (head), `hooks/optin.py` (`repo_root`, `git_common_dir`), `hooks/hooks.json`, `hooks/routing.py` (`AUTOMATION` comment)
- `docs/worktree-guard-spec.md` (diff, and a scan of §B, §Creation consent, §Choice sites)
- `seal/specs/1790381327-an-automation-run-creates-its-worktrees-without-asking/`: `spec.md`, `questions.md`, `overview.md`, `survivors.md`
- `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md`, `seal/releases/0.9.1.md` and `seal/releases/0.9.4.md` (diffs)
- `tests/conftest.py` (diff), `tests/test_worktree_guard_signals.py` (diff), `tests/test_the_guard_asks_once_per_session.py` (diff: fixtures and the reader cases)
- `README.md:183-190, 289`, `README.ko.md:184-186, 280`, `CLAUDE.md:15`, `templates/claude-md-block.md:15`, `CONTRIBUTING.md:185-195`, `skills/implement/orchestration.md:250-345`, `skills/implement/SKILL.md:300-315`, `bin/test` (head)
