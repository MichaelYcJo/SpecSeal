# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — review round 2

| Field | Value |
|---|---|
| Target SHA | e0c5a19169bf60283456aaf663593d4352196430 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 881 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | first — 🟡 1 at hooks/worktree-guard.py#_brace_spells_git, a unit round-1's fixes added |
| Needs a fix | yes — 🟡 1 (braces `_brace_spells_git` cannot read stay silent) and 🟡 2 (the command-word brace is judged in the typed tree) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 2 of round 1's fixes: 2f0d14b3..acc52a6a (6 commits) plus the close at e0c5a191. The job was the answers to round 1's verdicts. The New units _ONE_BRACE, _brace_spells_git and the inherited-pid case were a finding surface, and the Contract changes row's callers of _segment_finding were followed. The spawn named three things to judge: _brace_spells_git against the brace shapes bash expands, in both directions; whether the CLAUDE_CODE_SESSION_ID comparison fails open when either side is missing; and whether a single range row in survivors.md hides a live sentence. It also ran the eight guard modules once. Facts arrived labelled. Read from the smith: the split guard for Windows, the brace-join rule, the session-id comparison, 1,123 passed and survivor-check at exit 0. The reviewer disclosed one probe run in the main checkout. The orchestrator executed a check afterwards: main at 5623d728, clean, no new reflog entry.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Nested, sequence and `${…}`-adjacent braces that bash makes `git` of are read as no git, so `{{git,},} switch x` is silent in an ACTIVE tree | `hooks/worktree-guard.py:2292` | open | executed: bash runs `git switch x` for four spellings and the guard returns no finding; the case is red at the target and green once the paste-ready change is applied |
| 🟡 2 | A command-word brace finding is judged in the tree the command was typed from, not the one its `-C` names | `hooks/worktree-guard.py:2470` | open | executed: `{git,} -C W switch feature/x` silent with `W` dirty, the `git -C W` control asks; ask once the paste-ready change is applied |
| ⬜ 3 | survivors.md excuses the whole branch range with one row where 11 per-place rows were writable | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md:24` | open | a correction of the run's paperwork; executed: the 11 per-place rows excuse all 11, exit 0 |
| ⬜ 4 | The lease writer reads `CLAUDE_PID` where neither the environment nor the payload carries a session id | `hooks/session-lease.py:98` | open | executed: lease `pid-<ppid>` records the inherited 4242 |
| ⬜ 5 | The lease writer's module docstring states the unconditional `CLAUDE_PID` reading | `hooks/session-lease.py:25` | open | read: the comment in `main` and the docstring disagree |
| 🟢 | round 1's blocking finding 1 is closed — the guard's half of the braced forms runs everywhere, bash's half only where bash is a shell | `tests/test_worktree_guard.py:2199` | confirmed | read: the diff; executed: Windows `--group 4` passed at the target |
| 🟢 | round 1's blocking finding 2 is closed — survivor-check passes in the release job | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md` | confirmed | executed: 11 places without exemption, each opened, none a live present-tense sentence; the release job passed |
| 🟢 | round 1's yellow 3 is closed for `{git,}` and `{,git}` | `hooks/worktree-guard.py:2282` | confirmed | executed: both stop in an ACTIVE tree, `cat {.gitignore,README.md}` silent; the class continues in 🟡 1 and 🟡 2 |
| 🟢 | round 1's yellow 4 is closed for an environment naming another session or none | `hooks/session-lease.py:98` | confirmed | executed: the hook as a process records the walk's pid in both |
| 🟢 | round 1's white 5 stays answered | `hooks/worktree-guard.py:2007` | confirmed | read: round 1's executed grounds; `_BRACE` untouched by the fix range |
| 🟢 | round 1's white 6 is closed | `hooks/tokens.py:45` | confirmed | read: the docstring names ANSI-C quoting in both directions |
| 🟢 | round 1's question on the Windows branches of In 1's adapter, In 2's lease route and the stub is answered | `hooks/worktree_consent.py:419` | confirmed | executed, read from `gh pr checks 881`: all four Windows pytest jobs passed at the target |
| ❓ | Whether a hook process sees `CLAUDE_CODE_SESSION_ID`, on which the yellow 4 change's extension-host and nested cases turn | `hooks/session-lease.py:98` | ❓ out of verified scope | no hook's environment can be printed without changing the installed configuration; the repository owner answers |

## Paste-ready fixes

```python
def _brace_spells_git(word) -> bool:
    """Whether bash makes the word `git`, or a path ending in `git`, out of
    WORD's one comma brace: `{git,}`, `{,git}`, `/usr/bin/{git,x}`."""
    match = _ONE_BRACE.fullmatch(word)
    if match:
        head, alternatives, tail = match.groups()
        return any(
            os.path.basename(head + alt + tail) == "git"
            for alt in alternatives.split(",")
        )
    # A brace this reading cannot take apart (nested, a sequence, two braces,
    # a `${…}` beside one) is one bash may still make `git` of: the word
    # stops where its letters hold `g`, `i` and `t` in that order, so a reader
    # that cannot tell costs a stop and never a silence.
    return bool(_BRACE.search(word)) and bool(re.search(r"g.*i.*t", word))
```
```python
@pytest.mark.parametrize(
    "command",
    [
        "{git,} rebase main feature/x",
        "{,git} switch feature/x",
        "{{git,},} switch feature/x",
        "{,{git,}} switch feature/x",
        "{g..g}it switch feature/x",
        "${HOME}/bin/{git,} switch feature/x",
    ],
)
```
```markdown
A brace this reading cannot take apart (nested, a sequence, two braces, or
a `${…}` beside one) stops where the word's letters hold `g`, `i` and `t` in
that order, and the segment is judged in the tree its own `-C` names.
```
```python
    here, target = worktree_consent.place(tokens, wheres, cwd)
    if parse_git(tokens) is None:
        # A brace that makes the command word (`{git,} -C W switch x`) is git
        # to bash from that word on, and its `-C` names where it runs.
        at = next((i for i, t in enumerate(tokens) if _brace_spells_git(t)), None)
        parsed = parse_git(["git", *tokens[at + 1 :]]) if at is not None else None
        if parsed and parsed[2]:
            return apply_chdir(here, parsed[2])
    if parse_git(tokens) is None and wide is not None:
```
```python
@pytest.mark.parametrize(
    "command",
    ["{{git,}} -C {w} switch feature/x", "{{git,}} -C {w} rebase main feature/x"],
)
def test_a_brace_command_word_is_judged_in_the_tree_its_c_names(
    monkeypatch, capsys, repo, tmp_path, command
):
    """Round 2 of work item 1791384157, yellow 2. The frozen reading reads
    no git in `{git,} -C W switch x`, so the brace finding was judged in the
    tree it was typed from and said nothing with `W` dirty. Red at
    `e0c5a191`."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    (w / "f.txt").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": ([], [], True))
    decision, reason = verdict(monkeypatch, capsys, repo, command.format(w=w))
    assert decision == "ask" and STOP in reason, reason
```
```markdown
| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/spec.md` | Where `tokens.without_bodies` cannot load or raises | another work item's record of what it framed |
| `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/spec.md` | `has_token` reads no body (#780) | another work item's record of what it framed |
| `tests/test_worktree_guard.py` | `main()` asks `segment_cwd` for the `-C` target | `main()` reaches `segment_cwd` through `worktree_consent.place`, on the segment's own tokens |
| `tests/test_the_waiver_can_be_typed.py` | The judgment read drops comments, so a command carrying an apostrophe | still true of the judgment read; the docstring tells the consent read's history as history |
| `tests/test_the_waiver_can_be_typed.py` | That answer used to be handed to the CONSENT read | history told as history |
| `tests/test_the_waiver_can_be_typed.py` | The waiver was honoured before the judgment read started dropping comments | history told as history |
| `tests/test_guard_resolves_the_tree_it_judges.py` | the rule `hooks/tokens.py#given` has kept for the commit gate since #773 | `given` is the one consent reader since #868 and still keeps that rule |
| `tests/test_guard_resolves_the_tree_it_judges.py` | holds no repository sent the guard to | history told as history |
| `tests/test_guard_resolves_the_tree_it_judges.py` | The judgment read strips a subshell opener | still true; `has_token`'s half is told in the past tense |
| `hooks/worktree-guard.py` | The commit gate learned this about | history told as history |
| `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` | `has_marker` as it stood at `94d7b2e0` | `base_marker` states the base on purpose |
```
```python
        sid = os.environ.get(hooksession.SESSION_VARIABLE) or ""
        own = bool(sid) and sid == payload.get("session_id")
```
```python
`hooks/hooksession.py#claude_pid`'s answer: `CLAUDE_PID` where the harness
exports it beside this session's own `CLAUDE_CODE_SESSION_ID`, else the
nearest ancestor whose name is `claude`. That is the
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the eight guard modules named in the spawn, in the clone at the target | exit 0, 435 passed |
| bash `set -- <command>; printf '[%s]'` and the guard's `_segment_finding` over 26 brace commands | four spellings run `git switch x` in bash and return no finding; listed in 🟡 1 |
| the 🟡 1 parameters added to `test_a_brace_that_makes_the_command_word_is_unrecognised`, at the target | exit 1, 4 failed, 5 passed |
| the same with the 🟡 1 fix, `-k "brace or no_listed_form"` | exit 0, 25 passed |
| a placement probe through the module's `verdict` helper, session tree clean, `W` dirty, at the target | exit 1, 2 failed (silent), the control passed (ask) |
| the same with the 🟡 2 fix | exit 0, 3 passed |
| `tests/test_worktree_guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py` and the placement probe with both fixes | exit 0, 287 passed |
| `hooks/session-lease.py` run as a process over five environment and payload pairs | other id or none in the environment: walk's pid; both absent or both empty: 4242; own id: 4242 |
| `survivor_check.py --range 5623d728...HEAD`, no exemption, in the clone | exit 1, 11 places |
| the same with the eleven per-place rows below as `--exempt` | exit 0, 11 excused |
| `gh pr checks 881` at the target | lint, ledger, release and both grammar jobs pass; all four Windows jobs, ubuntu, and macOS `--group 1` and `--group 3` pass; macOS `--group 2` pending at hand-over |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_worktree_guard.py:2178` | round 1's 🔴 1 — fixed |
| round-1 | `tests/test_worktree_guard.py:729` | round 1's 🔴 2 — fixed |
| round-1 | `hooks/worktree-guard.py:2270` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/session-lease.py:91` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/worktree-guard.py:2007` | round 1's ⬜ 5 — answered |
| round-1 | `hooks/tokens.py:33` | round 1's ⬜ 6 — fixed |
| round-1 | `hooks/hooksession.py:68` | round 1's ❓ — out of verified scope |
| round-1 | `hooks/worktree_consent.py:419` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
