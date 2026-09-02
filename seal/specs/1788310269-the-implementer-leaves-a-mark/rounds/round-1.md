# 1788310269-the-implementer-leaves-a-mark — review round 1

<!-- The reviewer opened nothing needing a fix, so this round ends the run and
does not consume the cap. Its two 🟡 were sentences in the records, answered
by the orchestrator in the same commit as this file; no code moved. -->

| Field | Value |
|---|---|
| Target SHA | 6d02403 |
| PR | none yet |
| Broad gate | not yet — the one full run follows this record |
| Fixes checked by | no fixes to check |
| Contract changes | none — no unit's signature or returns moved; `dispatch.py#GROUPS` gained one entry in two tuples, read by `dispatch.main` alone |
| New units | `hooks/implementer.py#MARK`, `#git_dir`, `#write`, `#stands`, `#is_smith`; `hooks/implementer-mark.py#main`; `hooks/implementer-notice.py#NOTICE_DIR`, `#commits`, `#already_told`, `#main`; `tests/test_the_implementer_is_recorded.py` — eight helpers and seventeen tests |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 0 | Stage 1: the mark prints nothing and the notice prints one line, never a `permissionDecision`, never a non-zero exit; `spec.md` quotes issue #26 as it reads; Q1 gives the owner a real choice; CONTRIBUTING's four items are answered in `plan.md:63-74` | `hooks/implementer-mark.py:43-61`, `hooks/implementer-notice.py:86-126`, `specs/1788310269-the-implementer-leaves-a-mark/questions.md:9` | pass | executed: dispatch probes below, rc 0, empty stderr, no decision in the notice's output |
| 🟡 1 | The records say every file open names `encoding="utf-8"`; the empty session marker is created with `open(path, "w").close()` | `hooks/implementer-notice.py:80`, `plan.md:73`, `overview.md:57` | answered — the sentence was the defect: the marker writes no bytes, so the code stands and both sentences now name the exception | orchestrator amended the two sentences |
| 🟡 2 | `commits()` does not see a commit under `eval`, `bash -c`, a heredoc body, or as the first statement of a loop/conditional body, and the ledger row and the spec section read as if it saw every one | `hooks/implementer-notice.py:45-60`, `.specseal/map/1788310269-the-implementer-leaves-a-mark.md:20` | answered — deliberate for a reminder (missing one costs a reminder, never a decision); the ledger row's Notes now say so, with the reserved-word case tied to `parse_git`'s rider | reviewer's 18-shape `commits()` table |
| 🟢 3 | `is_smith` accepts `smith`, `specseal:smith`, `other:smith`, `a:b:smith`; rejects `smithy`, `Smith`, empty, `None`, non-strings | `hooks/implementer.py:92-102` | pass | executed; recorded in ledger row 1's Notes |
| 🟢 4 | The mark's home and branch: `--absolute-git-dir`, so a linked worktree gets its own mark and the notice reads the same one; detached HEAD writes nothing and the notice stays silent; no `cwd`, a non-repository, a missing path — no output, no file; a repository without `.specseal/` gets neither `.specseal/` nor a mark | `hooks/implementer.py:41-90`, `hooks/implementer-mark.py:54-61` | pass | executed (probes B, C) |
| 🟢 5 | The notice's fail direction: unreadable `routing.md`, no row, `the session`, an answer outside the vocabulary — all silent; `already_told` basenames the session id, keeps state under the repository's git dir, treats `None` as already told; it also fires once for a commit whose `tool_response` failed | `hooks/implementer-notice.py:63-83, 97-108` | pass | executed (probe E); the failed-commit fact recorded in ledger row 4's Notes |
| 🟢 6 | Dispatch: the worktree guard's verdict is identical with and without the mark gate for smith, non-smith and non-opted-in payloads (`ask` with `isolation: "worktree"`, silent without); the mark appears only for smith in an opted-in repository; the RIDER's text matches; `console.to_utf8()` in both `__main__`s | `hooks/dispatch.py:37, 41, 77-93` | pass | executed (probe B) |
| 🟢 7 | Tests: 330 passed, 0 skipped across the new file, `test_routing_is_recorded`, `test_review_axes` and the dispatch tests; two mutations under `PYTHONDONTWRITEBYTECODE=1` reddened exactly their own tests | `tests/test_the_implementer_is_recorded.py` | pass | executed |
| 🟢 8 | Ledger 141 ok · 0 broken; rows 1, 4, 6 opened against the code; fragments only, no legacy issue numbers, no real identifiers, commit subjects in form; the new spec section and the README rows agree the notice is a reminder | `.specseal/map/1788310269-the-implementer-leaves-a-mark.md` | pass | executed and read |
| ❓ 9 | Whether a plain `print()` from a PostToolUse hook is shown to the person in the live harness — the same channel `review-history-guard.py:172` already uses, so not this branch's to prove | `hooks/implementer-notice.py:120-126`, `overview.md:56` | could not be judged here | the owner's first live session on a declared branch, together with the `ls .git/specseal-implementer` check the overview already names |

## Executed probes

| What was run | Result |
|---|---|
| pytest (3.12, xdist) — new file + `test_routing_is_recorded` + `test_review_axes` + `grep -l dispatch tests/*.py` | 330 passed · 0 skipped |
| mutations `is_smith` → `"smith" in name` and `opted_in` check removed, `PYTHONDONTWRITEBYTECODE=1` | 2 failed / 15 passed — each its own test; restored, `git diff --quiet` |
| `evidence_check.py --strict .` | 141 ok · 0 drifted · 0 broken (27 in this fragment) |
| `dispatch.py pre-agent` × {smith, smith+worktree, warden+worktree} opted-in, {smith, smith+worktree} not opted-in | rc 0, stderr empty; guard verdicts silent / ask / ask / silent / ask; mark only in the first two |
| `pre-agent` with no `cwd`, a non-repository, a missing path | `(0, '')`, no file |
| smith spawn in a linked worktree; detached HEAD spawn and commit | mark in the per-worktree git dir only; nothing on detached HEAD |
| `commits()` on 18 shapes | 10 True (plain, `-C`, `cd &&`, heredoc message, chains, `--amend`, `sudo`, `VAR=x`, subshell, `-c k=v`); 8 False (`eval`, `bash -c`, heredoc body, `for … do`, `if … then`, `git status`, prose, comment) |
| notice: baseline / second time same session / second declared branch same session / `git -C` from elsewhere / failed commit / `chmod 000 routing.md` | printed / silent / silent / silent / printed / silent (rc 0) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 9 — the live channel of a PostToolUse `print()` | `overview.md` Not verified (the live-session row) | the repository owner, first session after the merge |
| Q1–Q3 (`questions.md`): issue #26's disposition, a mark on a guard-blocked spawn, the notice not following `git -C` | `questions.md` | the repository owner |
