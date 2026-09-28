# Round 1 report — 1790562543, the stamp reaches the person it is drawn for

Round 1, a first round against the whole branch
`feat/400-the-stamp-reaches-the-person-it-is-drawn-for` at 69ad5e31, base
origin/release/v0.15.7 (1fa25931), draft PR #650. Spec compliance was judged
first, against spec.md (Scope In 1–6, S1–S17), the owner's two 2026-09-28
comments on #400 and the build's one divergence. Quality came second. The
class enumerated covers every path by which a stamp reaches a screen or a
transcript, every way it can be drawn twice, drawn from a sample or drawn over
a run that did not seal, and every sentence in agents/, skills/, docs/,
templates/ and both READMEs that says where or how the stamp is drawn.

No earlier round exists, so nothing was inherited. The implementer's account
(spec, plan, overview, phases, the spawn prompt) was read in full and treated
as claims. Each claim below is paired with what the code does.

## How the findings relate

```
the gate writes values only over a written cell    (holds — 🟢)
  └─ the hook draws them at the main Stop, once    (holds for the cases — 🟢)
       ├─ where the hook cannot draw, nobody is told how to recover   🟡 1
       ├─ one bad file takes the good ones claimed before it           🟡 2
       └─ drawing by hand names a file that does not exist             🟡 3
the hook exists, and the hook inventory a user reads does not list it  🟡 4
sentences and paperwork the change made slightly false                 ⬜ 5–8
```

## Spec compliance

**The divergence holds.** A terminal run without `--record` now draws nothing
(`skills/verify/scripts/broad_gate.py:2383`, `if terminal and item is not
None`). spec.md §Scope In 2 says "as today", and today drew on any green run.
The build followed #400 §*Done when*, bullet 4: "Drawing a stamp requires the
gate's exit 0 and the written cell; no other path draws one." I read the
issue body and the owner's two 2026-09-28 comments. Neither comment carves out
a terminal, and S10 is already stated for "a green `--record` run". The issue
outranks the frame, so the divergence stands.
`test_a_terminal_run_with_no_record_draws_nothing` pins it. The paperwork
still states the old rule, which is ⬜ 8.

**Scope In 1–6 and S1–S16 are met in code (read), and the cases for them pass
(executed, see the probes).** Where each path leads:

| Path | What reaches the screen or transcript | Coordinate |
|---|---|---|
| gate, pipe, `--record`, green | one `SEALED` line naming the file; no disc, no twin, no SGR | `broad_gate.py:2394`, `signal` |
| gate, pipe, no `--record`, green | `SEALED … nothing was recorded`; no file | `NOTHING_RECORDED` |
| gate, terminal, `--record`, green | the disc once, no file | `broad_gate.py:2383-2393` |
| gate, terminal, no `--record` | as the pipe; the divergence | same |
| gate, red | `NOT SEALED`, returns 1 before the draw branch | `broad_gate.py:2341-2346` |
| gate, refused record or chain failing after the write | returns 2 before `panel` is built | `broad_gate.py:2348-2381` |
| `seal-stamp` bare | the sample, unchanged apart from the scale | `seal_stamp.py#main` |
| `seal-stamp --from` | the file's rows, claimed before print; the second call is refused | `seal_stamp.py:674` |
| Stop, no `agent_id`, own session | one `systemMessage`, oldest first, each file claimed | `hooks/sealer-stamp.py:109` |
| Stop with `agent_id`, SubagentStop, other event | nothing | `hooks/sealer-stamp.py` `main` |
| Stop, zero files, or another session's file | nothing, and the other file is left alone | `values_dir` keyed by `session_key` |
| Stop from a subdirectory, or from a linked worktree of the clone | drawn; the common dir is shared | `toplevel`, `git_common_dir` |

No route draws twice. The terminal path writes no file, and both drawers
rename the file before they print. No route draws a sample as a run: the hook
reads values files only. No route draws over a run that did not seal, because
the write sits after `seal_record` returned 0. The one exception is a values
file somebody writes by hand, which spec.md §*What cannot be checked* puts
outside the defence.

**S17, and what a case can reach.** A case can reach the bytes the hook prints
for a given payload, the `Stop` registration in `hooks/hooks.json`, and the
dispatcher passing one JSON object through unchanged. A case cannot reach any
of these:

- whether the harness invokes the `Stop` hook with this payload shape in the
  version the owner runs;
- whether the message renders unfolded, in colour and after the text;
- whether several stamps in one message still render whole, given that probe D
  drew one;
- whether the message enters the model's context (Q1);
- which `python3` the harness resolves.

Probe D answered the second of those once, by screenshot. The rest is the
owner's to read on the first real run (❓ row).

## Quality — findings

### 🟡 1 — Where the hook cannot draw, the `SEALED` line promises a drawing and names no way to make one

*From reading, with probe A executed.* On a sealed piped run with a session
set, the line reads `… the stamp is drawn at the end of the turn of session
<id>, from <path>` (`DRAWN_AT_TURN_END`, `broad_gate.py:2413`). Only the
no-session line (`NO_SESSION_FOUND`, `broad_gate.py:2409`) names `seal-stamp
--from`.

The hook draws nothing, and says nothing, in at least three states the gate
cannot see:

- **The main session's `python3` is under 3.12.** Probe A ran the hook through
  `dispatch.py stop` under `/usr/bin/python3` 3.9.6 with one pending file. It
  exited 0 with empty stdout and stderr, and the file stayed pending.
- **The main session's `cwd` is outside the clone the run sealed.** An example
  is a workspace directory above several repositories.
- **The main session's plugin predates the hook.** This is the state the
  branch itself is built in (overview §Not verified, S17).

The account says otherwise. The hook's docstring says that in the floor case
"the `SEALED` line in the sealer's report, which names the file and
`seal-stamp --from`, is what remains" (`hooks/sealer-stamp.py:40-42`), and
overview.md §Not done says the same. For the common case, a line with a
session, both are false.

The documents a person would open to find out why no stamp appeared are
`docs/the-broad-gate.md` §*Where the stamp is drawn*,
`skills/code-review/orchestration.md:539-550` and `agents/sealer.md:152-161`.
None of them mentions the floor or the other two states. README's
Requirements paragraph does state 3.12 for every gate, and that is the only
place the silence is explained.

Why it matters: the person sees no stamp. The sealer's report says one will be
drawn, and the recovery command exists but is printed only in the one state
where it is least needed. The file stays pending, so it can still be drawn,
but nobody is told how.

Fix: name the recovery on every sealed line. Widen the orchestrator's sentence
so the command stays the person's in every case. State the silence in the
policy paragraph. After this, the docstring's sentence becomes true as
written. The paste-ready blocks are below.

### 🟡 2 — One malformed values file makes the hook lose the drawings it already claimed

*Executed, probe C.* `drawings` (`hooks/sealer-stamp.py:92-106`) catches only
`ValueError` around `read_values` and `stamp`, then claims the file, and only
then calls `stamp.label(values)`. `read_values` does not check `item` or
`tree`, and `label` calls `os.path.normpath(item)`.

Probe C wrote two files: an older, well-formed one and a newer one whose
`item` is `5`. The main `Stop` printed nothing and exited 0, and both files
had been renamed `.drawn.json`. A later `seal-stamp --from` on the good file
was refused with "was drawn already".

The good stamp was claimed and never drawn. That breaks two claims in the
docstring. One is "silent on every failure" with "a file that is not a run's
values is left where it is". The other is the spec's at-most-once *with the
values kept for `--from`*. It also takes down files the bad one did not
touch.

Why it matters beyond hand-written files: the file is written by the gate the
TREE ships (#475) and read by the hook the INSTALLED plugin ships. So a branch
that changes the values format meets an older hook, and every pending stamp of
that session is lost silently. `test_several_files_come_out_as_one_message_oldest_first`
covers a non-JSON file only, which fails before the claim.

Fix: build the whole block, label included, before the claim, and skip a file
on any exception. The paste-ready block is below.

### 🟡 3 — `seal-stamp --from <X.drawn.json>` says the values stay in a file that does not exist

*Executed, probe B.* `drawn_from` (`skills/verify/scripts/seal_stamp.py:683`)
formats the refusal with `drawn=drawn_path(path)`. Where `path` already ends
`.drawn.json`, that gives `X.drawn.drawn.json`. Probe B got exactly that
sentence, and the named file does not exist. The refusal itself is right
(exit 2, nothing drawn). The fact it states is false, and it is the one path a
person has to recover the values from (contract §14).

`test_a_values_file_is_drawn_by_hand_once_and_then_refused` asserts only the
exit code for this call, which is why the case did not catch it.

### 🟡 4 — The hook inventory in both READMEs does not list the new `Stop` hook

*From reading.* `README.md` §*The gates* (the table from line 181) lists every
registered hook, and `sealer-stamp` is not in it. The opt-in list at
`README.md:107` names the hooks that read `seal/` and omits it. "Seven of the
ten gates wake only under a condition" (`README.md:390`) is now eight of
eleven. "Three side effects are worth stating outright" (`README.md:221`) does
not name the new directory under the git common dir.

`README.ko.md` has the same four gaps: line 102, the table from line 179,
line 216 and line 383.

spec.md §Scope Out checked the READMEs for a sentence saying *where the stamp
is drawn* and found none. That is true. The gap is the hook inventory, which a
user reads to learn what runs on their machine at every turn's end. Every
opted-in session now starts one Python process there (plan.md §Operational
impact), and the README is where that cost is disclosed for the other hooks.

### ⬜ 5 — The no-session line prints the path unquoted inside a command

`NO_SESSION_FOUND` (`broad_gate.py:2409`) formats `` `seal-stamp --from
{path}` ``. A checkout path with a space in it gives a command that fails when
typed as printed. The behaviour and the path are right, and the command is
not. `shlex.quote(path)` in the format call fixes it, and the S14 case's
assertion would need the same quoting.

### ⬜ 6 — Two sentences still say a gate *drew* the stamp, and one says the gate draws on any terminal run

`agents/sealer.md:81-86` ends "the one place a reader learns which gate drew
the stamp". `docs/the-broad-gate.md:88-89` says "the stamp says which copy
drew it". In a sealer, no gate draws now, and the `gate` row says which copy
*measured* the tree and wrote the values. The facts are right, but the verb is
not.

`docs/the-broad-gate.md` §*Where the stamp is drawn* says "So the gate draws
on a terminal only". Read alone, that sounds as if every terminal run draws.
The divergence means only a recorded one does. "Draws only on a terminal, and
only over a written cell" says it.

### ⬜ 7 — The `close --broad-gate` path seals a cell with no stamp, and the orchestrator's rule says one is drawn

`skills/code-review/orchestration.md:539` says, without condition, "The stamp
is drawn for you at the end of your turn". The paragraph after it
(`orchestration.md:552-558`) describes the one path where the cell is written
by `round_record.py close --broad-gate` instead of by the gate. No values file
exists there, because the gate ran without `--record` and printed "nothing was
recorded". That is what #400 asks for, and no stamp is drawn. The rule should
say so in one clause, for example: "…at the end of your turn (a cell written
by `close --broad-gate` is sealed with no stamp)".

### ⬜ 8 — correction, paperwork: the frame still states the terminal rule the build diverged from

- spec.md:48 (§Scope In 2) says "draws exactly once, as today".
- questions.md:25 says "Whether a hand-run in a real terminal draws. It does,
  once."
- plan.md:94 says "Rejected. S10 draws once".
- overview.md §*Fed back into the spec* says "none", and §*Not done* says the
  `SEALED` line "still names the file and `seal-stamp --from`" (see 🟡 1).

Under `seal/specs/`, so a correction and not a fix: each needs one clause
saying a terminal draws only over a written cell, and the overview row should
say the rule was fed back. `docs/review-chain-spec.md` §*The last round
verifies* owns the rule that keeps these out of `Needs a fix`.

## Regression tests to plant

Each one is to be seen red against the code at 69ad5e31 before the fix lands
(contract §15).

```
tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py
  test_a_malformed_later_file_does_not_take_the_earlier_ones      (🟡 2)
    write a good file (now=1) and one with item=5 (now=2); Stop prints the
    good file's block, the good file is .drawn.json, the bad file is still
    pending under its own name.
  test_the_drawn_refusal_names_the_file_the_values_are_in          (🟡 3)
    draw once, then --from the .drawn.json path: stderr names that path,
    and every path the refusal names exists.
tests/test_the_seal_is_taken_once_by_the_sealer.py
  in test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing       (🟡 1)
    assert f"`seal-stamp --from {path}`" in said[0]
  in test_the_orchestrator_is_told_the_stamp_is_drawn_for_it        (🟡 1)
    pin "that command is the person's to type, and never yours"
```

## Facts for the evidence ledger

- `hooks/sealer-stamp.py#drawings`: a file is claimed before it is printed,
  and after the fix for 🟡 2, only after its whole block was built. Executed
  here as probe C against the unfixed code.
- `hooks/sealer-stamp.py#main`: under `python3` 3.9.6 the hook exits 0 with
  no output, and the pending file stays pending. Executed, probe A.
- `skills/verify/scripts/broad_gate.py#gate`: the values write is reached only
  after `seal_record` returned 0, and the terminal draw only with `item`
  set. Read.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The early-draw window, made likely rather than rare by a release that seals several items in one session: another item's completion notification starts a main turn after one gate wrote its file and before that sealer reported. The label names the item, so the stamp is identifiable, but it sits under another item's text. The plan gave two reasons to defer arming at `SubagentStop`; the second (`SubagentStop`'s `session_id` unmeasured) was answered by Q2 on 2026-09-28 | already deferred in this work item's questions.md Q3 | the orchestrating session, by watching this release's sealer runs |

## Paste-ready fixes

### 🟡 1

`skills/verify/scripts/broad_gate.py`:

```python
DRAWN_AT_TURN_END = (
    " · the stamp is drawn at the end of the turn of session {session}, from "
    "{path}; where none appears, `seal-stamp --from {path}` draws it"
)
```

`skills/code-review/orchestration.md`, the last two sentences of the closing
rule:

```markdown
`NOT SEALED` lines, and nothing is drawn. Wherever the `SEALED` line names
`seal-stamp --from`, quote it as it stands: that command is the person's to
type, and never yours.
```

`docs/the-broad-gate.md`, in the second paragraph under this work item's
marker, before its `Enforced by: nothing` line:

```markdown
Nor is the hook's silence where it cannot draw. It draws nothing and says
nothing where the main session's `python3` is under 3.12, the floor
`seal_stamp.py` refuses below (macOS ships 3.9); where that session's working
directory is outside the clone the run sealed; or where its plugin predates
the hook. So every sealed `SEALED` line names `seal-stamp --from <path>`, and
a stamp that did not appear is drawn by hand from it, once.
```

### 🟡 2

`hooks/sealer-stamp.py`:

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

### 🟡 3

`skills/verify/scripts/seal_stamp.py`, in `drawn_from`:

```python
    if path.endswith(DRAWN) or (
        not os.path.exists(path) and os.path.exists(drawn_path(path))
    ):
        drawn = path if path.endswith(DRAWN) else drawn_path(path)
        raise ValueError(VALUES_DRAWN.format(path=path, drawn=drawn))
```

### 🟡 4

`README.md`, a row in the gate table after `version-check`:

```markdown
| sealer-stamp | when the main session's turn ends (`Stop`) | draws, once and after the turn's text, each sealed run's stamp the broad gate left for this session under `<git-common-dir>/specseal-stamp/<session>/`, and renames the file `.drawn.json`. Nothing at a subagent's end, for another session's file, or under a `python3` older than 3.12; `seal-stamp --from <file>` draws one by hand | `seal/` at the root, or under the common git dir in local mode — silent elsewhere |
```

`README.md:107`, the opt-in list: "…the two implementer hooks, the stamp hook
and the version check."

`README.md:390`:

```markdown
Eight of the eleven gates wake only under a condition: the commit gate, the
mode gate, the review-history reminder, the two implementer hooks, the
review-skill gate, the stamp hook and the version check act in a
```

`README.md:221`, the side effects: "Four side effects are worth stating
outright", adding: "a sealed broad-gate run writes its stamp's values under
`<git-common-dir>/specseal-stamp/`, which the stamp hook renames once drawn and
nothing prunes".

`README.ko.md`, the same row in the table after `version-check`:

```markdown
| sealer-stamp | 메인 세션의 턴이 끝날 때 (`Stop`) | 광역 관문이 이 세션 앞으로 `<git-common-dir>/specseal-stamp/<session>/` 에 남긴 봉인 도장을, 턴의 글이 다 나온 뒤에 한 번 그리고, 그 파일의 이름을 `.drawn.json` 으로 바꾼다. 서브에이전트가 끝날 때, 다른 세션의 파일, 3.12 보다 낮은 `python3` 에서는 그리지 않는다. 손으로 그리려면 `seal-stamp --from <file>` 이다 | 루트에 `seal/` 이 있는 레포, 또는 local 모드로 공통 git 디렉터리 아래에 있는 레포. 그 밖에서는 아무것도 하지 않는다 |
```

`README.ko.md:383`:

```markdown
게이트 열하나 중 여덟은 조건이 맞아야 깨어납니다. 커밋 게이트와 모드 게이트,
리뷰 이력 알림, 구현자 훅 둘, 리뷰 스킬 게이트, 도장 훅, 버전 확인은 레포 루트에, 또는
```

`README.ko.md:102` adds "도장 훅" to the opt-in list, and `README.ko.md:216`
becomes "네 가지 부수 효과" with the same clause about
`<git-common-dir>/specseal-stamp/`.

Needs a fix: yes — 🟡 1 (the SEALED line and the policy do not say how to recover a stamp the hook cannot draw), 🟡 2 (one malformed file loses the drawings claimed before it), 🟡 3 (the drawn refusal names a file that does not exist), 🟡 4 (both READMEs omit the new hook)
Loses a record or crashes: no

The hook exception in 🟡 2 is swallowed by `dispatch.py`'s `run_gate`, so
nothing visible crashes. What it loses is a drawing, and spec.md §Data &
interfaces says the values file is not a record. If the orchestrator reads a
swallowed exception as a crash, 🟡 2 is the finding that flips this line.

## Proof block

Opened: `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/`
(spec.md, plan.md, questions.md, overview.md, changelog.md, routing.md head,
phases/phase-1.md, phases/phase-2.md); `hooks/sealer-stamp.py`;
`hooks/dispatch.py` (diff, `run_gate`, `merge`); `hooks/hooks.json` (diff);
`hooks/optin.py` (`git_common_dir`, `opted_in`); `bin/seal-stamp`;
`skills/verify/scripts/broad_gate.py` (diff, `gate`, `main`'s hand-off);
`skills/verify/scripts/seal_stamp.py` (diff); `agents/sealer.md` (lines
60-230); `docs/the-broad-gate.md` (diff, lines 84-92);
`skills/code-review/orchestration.md` (lines 515-560); `skills/verify/SKILL.md`
(diff, 338-348); `templates/config.md` (190-198);
`docs/commit-review-gate-spec.md` (384-392); `README.md` (104-108, 170-235,
296-306, 386-396); `README.ko.md` (grep lines, 214-219, 383-386);
`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` (whole);
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (diff, 2293-2440);
`bin/test`; issue #400's body §*Done when* and its last two comments.
Executed: the two `bin/test` runs and probes A–E above, in a scratch clone
since deleted. Read, not executed: everything else. Unverified: the broad
gate (the sealer), S17 (the owner).
