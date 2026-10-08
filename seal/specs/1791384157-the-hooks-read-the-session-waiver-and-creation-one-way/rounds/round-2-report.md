# Round 2 report — the hooks read the session, the waiver and a creation one way

Work item 1791384157 (#868, #856), draft PR #881 into `release/v0.21.0`.
A verifying round. Target SHA `e0c5a19169bf60283456aaf663593d4352196430`;
the target is round 1's fix range `2f0d14b3..acc52a6a` (six commits) and
the close at `e0c5a191`. Reviewed in a `--no-local` clone at the target SHA.

Carried from round 1 as coordinates, not re-derived: where the brace rule
lives (`hooks/worktree-guard.py#_BRACE`, `_unquoted_brace`), where the lease
writer reads its pid (`hooks/session-lease.py`), and the CI log that showed
the Windows failure at `test_no_listed_form_moves_head_under_git`. Every
verdict below is this round's own.

## How the findings relate

```
Round 1's verdicts
  ├─ red 1, red 2, yellow 4, white 5, white 6   closed, each checked below
  └─ yellow 3  closed for the two shapes it named, and its class is not
       ├─ 🟡 1  nested, sequence and `${…}`-adjacent braces still make a
       │        silent `git switch` (inside `_brace_spells_git`, a new unit)
       └─ 🟡 2  the new arm's finding is judged in the tree the command was
                typed from, not the one its `-C` names
Round 1's paperwork and comments
  ├─ ⬜ 3  survivors.md excuses the branch's whole range with one row
  ├─ ⬜ 4  the lease writer reads `CLAUDE_PID` where both ids are absent
  └─ ⬜ 5  the lease writer's module docstring still states the old rule
```

The two 🟡 are why this round says `Needs a fix: yes`. Both sit in the arm
round 1's yellow 3 added, and both have a fix that was applied in the clone
and seen green after its case was seen red.

## Round 1's verdicts, answered

**Red 1 — closed.** The braced half of
`test_no_listed_form_moves_head_under_git` now asserts the guard's reading
first and calls `shell_probe("bash")` only before the part that runs bash
(read: `tests/test_worktree_guard.py:2199`). The smith's account matches the
code. The final assertion changed from `sorted(acted) == sorted(BRACED)` to
`len(acted) == len(BRACED)`; `acted` is built only from the braced texts,
one per form, so the two are equivalent. Executed, read from
`gh pr checks 881`: the Windows `--group 4` job, the one that failed in
round 1, passed at the target.

**Red 2 — closed, with ⬜ 3 below.** Executed in the clone: survivor-check
over `5623d728...HEAD` with no exemption names 11 places, exit 1. I opened
each one. None states a retired reading in the present tense:

- two are work item 1791163981's `spec.md`, another item's record;
- six tell a reading's history in the past tense;
- `tests/test_worktree_guard.py:781` says `main()` asks `segment_cwd`, and
  it still does, through `worktree_consent.place` on the segment's tokens;
- `tests/test_the_waiver_can_be_typed.py:130` and
  `tests/test_guard_resolves_the_tree_it_judges.py:353` say the judgment
  read drops comments and strips a subshell opener, both still true.

So the range row hides no live sentence today. What it does to the next
fix pass is ⬜ 3.

**Yellow 3 — closed for `{git,}` and `{,git}`.** Executed: both stop in an
ACTIVE tree; `cat {.gitignore,README.md}` stays silent. The smith's account
that the rule reads comma alternatives rather than the text `git` matches
the code. The class is not closed, which is 🟡 1 and 🟡 2.

**Yellow 4 — closed for the case it named.** Executed against the hook as a
process: with the environment's `CLAUDE_CODE_SESSION_ID` naming another
session, or absent, the lease records the walk's pid and not `CLAUDE_PID`.
The new case covers both. Two edges remain. Where both ids are absent the
comparison is `None == None` and the variable is read (⬜ 4). Where the
hook's own id is right but `CLAUDE_PID` is inherited, the variable is read
too, and whether that happens depends on what the harness hands a hook,
which is the ❓ row below.

**White 5 — closed, as answered.** Read: round 1 executed that bash makes
`git rebase main 'feature x'` of the quoted-space brace, which git refuses.
Nothing in round 1's fixes touched `_BRACE`.

**White 6 — closed.** Read: `hooks/tokens.py:45` now names ANSI-C quoting as
where the splitter and bash disagree, in both directions, and the example
matches how a POSIX shlex closes a single quote at the backslash.

## 🟡 1 — Three brace shapes bash makes `git` of are still silent

`hooks/worktree-guard.py:2292` (`_brace_spells_git`, with `_ONE_BRACE` at — NAME NOT IN TREE since the reframe
`:2289`).

`_ONE_BRACE` takes one comma brace with no brace in the text around it. NAME NOT IN TREE since the reframe.
`_BRACE`, which decides that the command holds a brace at all, accepts
more: a sequence, a brace inside a brace, and a brace beside `${…}`. A word
that `_BRACE` sees and `_ONE_BRACE` cannot read returns `False`, so the (NAME NOT IN TREE since the reframe)
segment is no git and stops nothing.

Executed, each through bash and through the guard's own segment reading:

| Command | bash runs | Guard |
|---|---|---|
| `{{git,},} switch x` | `git switch x` | silent |
| `{,{git,}} switch x` | `git switch x` | silent |
| `{g..g}it switch x` | `git switch x` | silent |
| `${HOME}/bin/{git,} switch x` | `/Users/x/bin/git switch x` | silent |

Why it matters: this is the same silence yellow 3 was raised for, one
spelling over, in an ACTIVE tree where the guard exists to deny. The
spec's own rule for an unsure reader is that it costs a stop and never a
silence (`hooks/worktree-guard.py:2026`), and this arm inverts it.

The fix keeps the one-brace reading where it applies and, where the word
holds a brace it cannot take apart, stops where the word's letters hold
`g`, `i` and `t` in that order. Executed in the clone: the four commands
added to the existing case are red at the target (4 failed, 5 passed) and
green with the fix (25 passed over the brace and git-binding cases).

## 🟡 2 — The new arm judges a braced `git -C W` in the wrong tree

`hooks/worktree-guard.py:2470` (`_finding_tree`), reached from the arm
round 1 added to `_segment_finding`.

The new arm returns a finding for `{git,} -C W switch x`, but the tree it is
judged in comes from `_finding_tree`. That reads the segment's `-C` through
the frozen reading or the wider reader, and neither reads `{git,}` as git.
So the finding is judged in the tree the command was typed from.

Executed in the clone, with the session's tree clean and `W` dirty:

| Command | Verdict |
|---|---|
| `git -C W rebase {main,feature/x}` (control) | ask |
| `{git,} -C W switch feature/x` | silent |
| `{git,} -C W rebase main feature/x` | silent |

Why it matters: a branch switch in a dirty or ACTIVE `W` goes through
without a word, and this is not one of the named limits.
`docs/worktree-guard-spec.md` names a string handed to a shell as judged in
the typed tree; it says nothing of this shape. The fix reads the `-C` from
the words after the brace word. Executed: both rows red at the target and
ask with the fix; `tests/test_worktree_guard.py` and
`tests/test_guard_resolves_the_tree_it_judges.py` pass with both fixes in
place (287 passed, the probe's three cases included).

## ⬜ 3 — One range row excuses every survivor the next fix pass leaves

`seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md:24`.

A correction of the run's paperwork, not of the tool. The `| Range |` row
is the escape `skills/code-review/scripts/survivor_check.py` documents for
a branch that deletes a shipped section and would need 153 rows. This
branch needed 11. The range is a relation, `origin/release/v0.21.0...HEAD`,
and it re-resolves to the branch's whole range at every run, so a survivor
the round 2 fixes leave is excused too, printed under `exempt` with exit 0.
Per-place rows anchor each excuse on its quote, which stops holding when
the text changes. Executed: the eleven rows in the paste-ready block,
handed to survivor-check over the same range, excuse all 11, exit 0.

## ⬜ 4 — The lease writer reads `CLAUDE_PID` where neither id exists

`hooks/session-lease.py:98`.

`own` compares the environment's id with the payload's. Executed: with
neither present, or both empty, the comparison is true and the lease named
`pid-<ppid>` records the inherited `CLAUDE_PID`. A second lease naming the
same pid makes the lease route answer no session for the outer session
too (`hooks/hooksession.py#from_lease`). The harness always sends a
`session_id`, so no release ships this; a non-empty test closes it.

## ⬜ 5 — The lease writer's docstring states the reading it no longer does

`hooks/session-lease.py:25`.

The module docstring says the pid is `CLAUDE_PID` where the harness exports
it. Since `cd7027df` that holds only beside the payload's own session id;
the comment in `main` says so, the docstring a reader opens first does not.

## Questions this round could not settle

- Whether a hook process sees `CLAUDE_CODE_SESSION_ID` at all. The yellow 4
  fix reads `CLAUDE_PID` only where it does. If an extension host hands its
  hooks `CLAUDE_PID` and not the session id, the lease writer walks, finds
  no `claude`, and records no pid there again — the case
  `test_the_lease_records_the_pid_the_harness_exports` was written for, and
  which now sets the session id itself to pass. If a nested session's
  harness hands its hooks its own id and the inherited `CLAUDE_PID`, the
  outer pid is recorded. Both turn on round 1's open M1 hook half. The
  repository owner answers.
Round 1's other question, the Windows branches it left to CI, is answered:
all four Windows pytest jobs passed at the target.

## Regression tests to plant

- `tests/test_worktree_guard.py`: the four 🟡 1 commands as parameters of
  `test_a_brace_that_makes_the_command_word_is_unrecognised`. Seen red at
  the target.
- `tests/test_worktree_guard.py`: the 🟡 2 case in the paste-ready block.
  Seen red at the target.
- `tests/test_guard_resolves_the_tree_it_judges.py`: pin the new
  `docs/worktree-guard-spec.md` sentence in
  `test_the_guard_policy_names_the_brace_shape_and_its_costs` (§14).

## Facts for the evidence ledger

- `docs/worktree-guard-spec.md` §A, the command-word brace sentence: add the
  🟡 2 case's id to its `Enforced by` line once planted.
- bash 3.2 and later expand `{{git,},}`, `{,{git,}}` and `{g..g}it` to
  `git`; executed with the macOS system bash in this round.

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

One probe ran in the wrong directory. The 26-command brace probe passed
`echo $({git,} switch x)` to bash with the session's own checkout as the
working directory, so bash ran `git switch x` there. Git refused it, since
no branch `x` exists. Executed afterwards: that checkout is still on `main`
at `5623d728`, clean, and its reflog has no new entry.

## Paste-ready fixes

### 🟡 1

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

### 🟡 2

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

### ⬜ 3

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

### ⬜ 4

```python
        sid = os.environ.get(hooksession.SESSION_VARIABLE) or ""
        own = bool(sid) and sid == payload.get("session_id")
```

### ⬜ 5

```python
`hooks/hooksession.py#claude_pid`'s answer: `CLAUDE_PID` where the harness
exports it beside this session's own `CLAUDE_CODE_SESSION_ID`, else the
nearest ancestor whose name is `claude`. That is the
```

Needs a fix: yes — 🟡 1 (braces `_brace_spells_git` cannot read stay silent; NAME NOT IN TREE since the reframe) and 🟡 2 (the command-word brace is judged in the typed tree)
Loses a record or crashes: no

## Proof

Files opened this round:

- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-1.md`
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-1-fixes.md`
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-1-report.md` (head)
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md`
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-1.md` (lines 85–100)
- `hooks/worktree-guard.py` (lines 340–372, 1990–2060, 2178–2320, 2420–2490, 2955–3000)
- `hooks/session-lease.py`, `hooks/hooksession.py`
- `tests/test_worktree_guard.py` (lines 776–792, 1112–1143, 1671–1701, 1918–1950, 2140–2240)
- `tests/test_guard_resolves_the_tree_it_judges.py` (lines 348–362, 1572–1582)
- `tests/test_the_waiver_can_be_typed.py` (lines 124–140)
- `tests/conftest.py` (`shell_probe`)
- `skills/code-review/scripts/survivor_check.py` (lines 236–300, 1888–1930, 2101–2120)
- `.github/workflows/hygiene.yml` (lines 225–270)
- the diff `2f0d14b3..acc52a6a` over `hooks`, `tests` and `docs`
