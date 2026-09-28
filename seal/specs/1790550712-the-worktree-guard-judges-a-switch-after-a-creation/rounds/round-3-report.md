# Round 3 report — 1790550712-the-worktree-guard-judges-a-switch-after-a-creation

| Field | Value |
|---|---|
| Round | 3 (verifying, the run's last) |
| Target SHA | 04d431ddf7bfacbc41305f82856d7f2f66137c42 |
| Target | the fix range `e6435da5eee9074d3e6f011f813b317dfc31e97f..1c5dc5cf865129727ef9cc3282199d65c585a254` (3072f2f, 64d2e21, 1c5dc5c), not the branch |
| Base | origin/release/v0.15.6; the comparison side for the new cases is fe24f07 |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at the target under the session scratchpad; probes, mutation scripts and the clone removed before handover |

## Summary

Round 2's four fixes hold for what each one named. The force-staged check
now runs at the tree's root, and reverting it turns its case red. The note's
two `git restore` lines name the root from every shell position I tried.
`git_at` gives the right answer in all thirteen shell positions I put it in,
symlinks, a case variant, a submodule and a linked worktree included.

Round 2's finding 1 was closed as a class, and the class is one member
short. The worktree steer ends with `` `git worktree list` shows worktrees ``,
and that line never got the command word. The spec paragraph and W10 both
say every printed command names the tree, so both are false for that line.
The class case cannot see it, because its pattern has no alternative for
`worktree list`.

- 🟡 1: `git worktree list`, and the creation ladder's `use git switch`
  fallback, still run in the shell's own repository. Executed.
- 🟡 2: the worktree root is spliced into the same printed lines unquoted, so
  a repository path with a space or a quote gives a command that does not
  parse. This is older than the work item. Executed.
- ⬜ 3: the class case reads four of the six call sites. Two creation-ladder
  steers can go back to a bare `git` and every case stays green. Executed.
- ⬜ 4: `git_at` runs one more `git rev-parse` on every switch, including the
  silent row where nothing it returns is printed. Read.

## Round 2's four verdicts

**🟡 1, the phantom note's commands — closed for the instance, open as a
class.** Executed: with the tree dirty from a force-staged path, the note's
two commands carry `git -C <root>` from another repository, from a
subdirectory and from the root. M19 (the note without `-C`) turns
`test_the_dirty_tree_row_reads_the_tree_the_switch_is_in` alone red. The
class it was widened to is not complete; see 🟡 1 below.

**🟡 2, the force-staged check from a subdirectory — closed as a class.**
Executed: M18 (`phantom_entries(entries, eff_cwd)`) turns
`test_the_force_staged_check_reads_from_the_root_of_the_tree` alone red, and
fe24f07's hook turns it red too. Read: nothing else in the switch ladder
hands a root-relative path to a command that runs somewhere else.
`tracked_changes` runs `git status --porcelain`, whose paths are relative to
the root wherever it runs, and the `AD` branch of `phantom_entries` does not
touch the filesystem.

**⬜ 3, the command-word sentence — closed.** Read: `parse_git` compares
`os.path.basename` of the command word, as written (`hooks/cmdline.py:1837`),
which is what the corrected sentence at `docs/worktree-guard-spec.md:258`
and the test comment at `tests/test_the_guard_asks_once_per_session.py:389`
now say. Executed only as part of the three guard modules passing at the
target; I did not re-run round 2's six-word lexer probe.

**⬜ 4, W9's figures — closed.** Read: the 3,168 / 141 / 45 figures are gone,
the force-staged clause names the root, and the row cites the new case.
Executed: W9's M18 claim reproduces exactly (that case alone red). Its claim
about the four cells at `77ad175` is unverified; I did not check out that
commit.

## The new units

**`git_at` is sound.** Executed, with `top` the fixture repository: it
returns bare `git` for the root, a subdirectory, a symlink to the root, a
symlink into a subdirectory, and an upper-cased spelling of the root. It
returns `git -C <top>` for the `.git` directory, a nested repository, a
submodule, a linked worktree of the same repository, another repository, a
directory outside any repository, a path that does not exist, and an empty
`cwd`. The symlink and case cells agree because `git rev-parse
--show-toplevel` canonicalises both sides on this machine; `normcase` does
nothing on POSIX and is not what makes them agree. A `-C` spelled with the
wrong case also resolves to the canonical root, so `git_at` returns bare `git`
from the real root. `top` is `shlex.quote`d in every line that carries it.

**The contract changes are passed correctly.** Read: `steer_to_switch` has
three callers and `steer_to_shared` has two, all in
`hooks/worktree-guard.py`, and each passes the `git` its own ladder
computed from `git_at(top, cwd)`. Every `judge_creation` call site passes the
session's `cwd`, which is where the shell stands, and never `eff_cwd`. No
module outside the hook calls either function. Both still default to
`git="git"`, so a future caller that forgets the argument prints the bare
form silently. That is ⬜ 3's fix territory and I did not number it.

**The advice goes back through the guard.** Executed from another
repository: `git -C <top> switch feature/x  # [shared-tree-ok]` passes both
choice rows and reaches row 3, and `git -C <top> worktree add <wt>/b b  #
[worktree-ok]` reaches the token row of the creation ladder.

**`survivors.md`'s grounds are true in substance.** Executed:
`survivor_check.py` over the fix range exits 1 without the exemption and
names `tests/test_the_guard_asks_once_per_session.py:1516`, `MEASURED_RUN`,
with two shared phrases: `\ngit switch` and `\ngit switch -c`. The grounds
name only the first, which is the same fragment extended by `-c`. With the
exemption it exits 0. Read: `MEASURED_RUN` is a command handed to the guard as
input, not text the guard prints. Whether it is #604's command verbatim is
unverified; I did not open #604.

## 🟡 1 — `git worktree list` still names the shell's repository

`hooks/worktree-guard.py:2144` and `:2151` end the worktree steer with
`` `git worktree list` ``, a plain string with no command word. The steer is
printed by the ACTIVE deny and by both choice rows' fallbacks. From a shell in
another repository, every other command in that steer carries `-C <top>`,
and this one lists the shell's own worktrees. It sits on the same lines the
fix edited.

Executed: from another repository, the ACTIVE deny and both choice fallbacks
print `git -C <top> fetch`, `git -C <top> worktree add …`, and a bare `git
worktree list`. `docs/worktree-guard-spec.md:541` says that where the shell
is not in the judged tree each command carries `git -C <root>`, and it names
the worktree steer. W10 (`seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md:12`)
says every command a guard reason tells the person to run names its tree.
Both are false for this line. ML (the line given `{git}`) left all 185 cases
green, so nothing pins it either way. `PRINTED_COMMAND` has no `worktree
list` alternative, which is why the class case passes over it.

A second member sits in the creation ladder at `:1859`. The
detection-unusable row's fallback ends *if single-stream, cancel and use
`git switch`*. Executed: from another repository, that reason carries no
`-C` command at all. The other bare `git switch` mentions (`:1813`, `:1828`)
describe a choice and are followed by `steer_to_switch(git)`, so I read them
as prose and not as commands.

Why it matters: this is the defect round 2 closed, on the line next to the
fixed ones. The spec and the ledger now claim the class is complete.

## 🟡 2 — the worktree root is not quoted where the lines print it

`{wt_root}` is interpolated raw into eight printed lines
(`hooks/worktree-guard.py:2139`–`:2179`, both languages): the steer's two
`worktree add` lines and the split option's two. `git_at` quotes `top` in
the same lines, so a repository path with a space or a quote now gives a
line whose first half is quoted and whose second is not.

Executed, with the judged repository at a path containing a space and an
apostrophe: the `fetch origin` line splits into the right five words, and
both `worktree add` lines fail `shlex.split` with *No closing quotation*.
With only a space, the path splits into two arguments and `git worktree add`
gets one argument too many.

This is older than the work item. The base's lines carried the same raw
`{wt_root}`. It is not in a unit the run's fixes created. I report it because
the round was asked whether every printed line is quoted, and it is the same
line class. Whether it is the branch's or a deferral is the orchestrator's
cap test.

## ⬜ 3 — the class case reads four of six call sites, and one alternative contradicts its rule

`test_every_printed_command_names_the_tree_it_is_about`
(`tests/test_guard_resolves_the_tree_it_judges.py:616`) drives four rows,
each on a fresh session, so it reads only the first attempt of each choice
row. Executed: reverting `steer_to_switch(git)` to `steer_to_switch()` at
the creation ladder's token row (MU) or its idle fallback (MI) leaves all 185
cases in the three guard modules green. The code is right today. Executed:
from another repository both rows print `-C <top>`. So this is a missing pin
and not a defect.

`PRINTED_COMMAND` (`:606`) also matches `restore`. None of the four rows
reaches row 3 on the clean fixture, so the alternative never matches in this
case. If it did, the rule *from inside, none carries `-C`* would fail on it,
because the note's `restore` lines carry `-C` always, by design.

The paste-ready case below adds the three missing rows, reads two attempts
per row, drops `restore`, and adds `worktree list` and `` switch`. `` for
🟡 1. Executed: it is green on the fixed hook, red on the target hook at
`git worktree list`, and red under MU and MI.

## ⬜ 4 — one more `git` process per switch, where the silent row prints nothing

Read: `main` computes `git = git_at(top, cwd)` at `:2128`, before row 1, and
`git_at` runs `git rev-parse --show-toplevel` for the shell's directory. The
clean single-stream switch, the commonest one, exits at row 4 and never
prints `git`. Row 3 builds its own `-C` string. The cost is one subprocess
per guarded switch. Computing it inside the rows that print, or reusing
`top` when `cwd` resolves to it, removes it. Not measured.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The worktree steer's `git worktree list`, and the creation ladder's detection-unusable fallback *use `git switch`*, carry no command word. From another repository they act on the shell's tree, and the spec paragraph and W10 say every printed command names the judged tree | `hooks/worktree-guard.py:2144` | open | Executed: from another repository, the ACTIVE deny and both choice fallbacks print every other command with `-C <top>` and this one bare. The creation fallback's reason carries no `-C` command at all. ML left every case green, and `PRINTED_COMMAND` has no `worktree list` alternative. Inside units the run's fixes edited (the steer, W10, the spec paragraph) |
| 🟡 2 | `{wt_root}` is spliced unquoted into the eight printed `worktree add` lines while `top` beside it is quoted, so a path with a space or a quote prints a command that does not parse | `hooks/worktree-guard.py:2139` | open | Executed: with the repository at a path holding a space and an apostrophe, the `fetch` line splits correctly and both `worktree add` lines fail `shlex.split`. Older than the work item and not in a unit the run's fixes created; reported because this round was asked about quoting in every printed line |
| ⬜ 3 | The class case reads four of six `git_at` call sites and only the first attempt of each choice row; its `restore` alternative never matches and would contradict its inside rule if it did | `tests/test_guard_resolves_the_tree_it_judges.py:606` | open | Executed: MU (token row) and MI (idle fallback) reverted to bare `git` leave all 185 cases green, and both rows print `-C` today, so this is a missing pin. The paste-ready case is red under MU, MI and the target hook, and green on the fixed hook |
| ⬜ 4 | `git_at` spawns `git rev-parse` before row 1 on every switch, including the silent row that prints nothing | `hooks/worktree-guard.py:2128` | open | Read: rows 3 and 4 do not use `git`. Not measured |
| 🟢 | round 2's finding 1 is closed for the note's two commands and for the steers the fix named | `hooks/worktree-guard.py:2364` | confirmed | Executed: the note carries `-C <root>` from another repository, a subdirectory and the root; M19 turns the tracked-changes case alone red. The class remainder is 🟡 1 |
| 🟢 | round 2's finding 2 is closed as a class — the force-staged check runs at the root | `hooks/worktree-guard.py:2355` | confirmed | Executed: M18 turns the new case alone red, and fe24f07's hook turns it red. Read: no other root-relative path in the ladder runs elsewhere |
| 🟢 | round 2's finding 3 is closed — the sentence states what `parse_git` compares | `docs/worktree-guard-spec.md:258` | confirmed | Read: `hooks/cmdline.py:1837` compares the basename as written. The six-word lexer probe was not re-run |
| 🟢 | round 2's finding 4 is closed — W9 states what the committed cases hold | `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md:11` | confirmed | Read, and W9's M18 claim executed. Its claim about the cells at `77ad175` is unverified |
| 🟢 | `git_at` answers right in thirteen shell positions | `hooks/worktree-guard.py:1413` | confirmed | Executed: bare for the root, a subdirectory, two symlinks and a case variant; `-C <top>` for `.git`, a nested repository, a submodule, a linked worktree, another repository, a non-repository, a missing path and an empty `cwd` |
| 🟢 | every caller of `steer_to_switch` and `steer_to_shared` passes its own ladder's `git` | `hooks/worktree-guard.py:1707` | confirmed | Read: five call sites in the hook, none outside it; every `judge_creation` passes the session's `cwd`. Executed: the printed `-C` advice goes back through both token rows |
| 🟢 | `test_the_force_staged_check_reads_from_the_root_of_the_tree` is sound | `tests/test_guard_resolves_the_tree_it_judges.py:576` | confirmed | Executed: red under M18 and against fe24f07's hook |
| 🟢 | `survivors.md`'s exemption grounds are true | `seal/specs/1790550712-the-worktree-guard-judges-a-switch-after-a-creation/survivors.md:5` | confirmed | Executed: `survivor_check.py` over the range exits 1 without it and 0 with it; the two shared phrases are `\ngit switch` and its `-c` extension. Whether the fixture is #604's command verbatim is unverified |

## Paste-ready fixes

### 1

```python
        "Then work in that folder from a separate Claude Code session. "
        f"`{git} worktree list` shows worktrees.",
```
```python
        "그런 다음 그 폴더에서 별도의 Claude Code 세션으로 작업하세요. "
        f"worktree 목록은 `{git} worktree list`.",
```
```python
            tr(
                "Confirm if this really is concurrent work; if single-stream, cancel and "
                f"use `{git} switch`.",
                f"정말 동시 작업이면 확인해 주시고, 단건이면 취소하고 `{git} switch` 로 진행하세요.",
            ),
```

### 2

```python
    git = git_at(top, cwd)
    # Every printed line splices this path into a command, so it is quoted
    # the way `git_at` quotes `top`: unchanged for a plain path, and one shell
    # word for a path with a space or a quote in it.
    wt_root = shlex.quote(wt_root)
```

### 3

```python
PRINTED_COMMAND = re.compile(
    r"git(?P<at> -C \S+)? (fetch origin|switch -c <|switch <branch>|worktree add [^`]"
    r"|worktree list|switch`\.)"
)
```
```python
    rows = (
        ("switch", "ACTIVE", (ACTIVE, [], True)),
        ("switch", "idle", ([], idle, True)),
        ("worktree add ../wt f", "single", ([], [], True)),
        ("worktree add ../wt f", "idle", ([], idle, True)),
        ("switch", "unreliable", ([], [], False)),
        ("worktree add ../wt f", "unreliable", ([], [], False)),
        ("worktree add ../wt f  # [worktree-ok]", "token", ([], [], True)),
    )
    for n, (verb, state, sessions) in enumerate(rows):
        tail = "feature/x" if verb == "switch" else ""
        for shell in (other, repo):
            command = f"git -C {repo} {verb} {tail}".rstrip()
            # A choice row denies once per session and asks on the attempt
            # after, and the two print different commands: read both.
            for _ in range(2):
                monkeypatch.setattr(wg, "sessions_in_tree", lambda t, o="", s=sessions: s)
                monkeypatch.setattr(
                    wg,
                    "load_input",
                    lambda command=command, shell=shell, n=n: {
                        "tool_name": "Bash",
                        "session_id": f"p{n}-{shell.name}",
                        "tool_input": {"command": command},
                        "cwd": str(shell),
                    },
                )
                try:
                    wg.main()
                except SystemExit:
                    pass
                out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
                reason = out["permissionDecisionReason"]
                found = printed_commands(reason)
                assert found, (verb, state, reason)
                for m in found:
                    if shell == repo:
                        assert m.group("at") is None, (verb, state, m.group(0))
                    else:
                        assert m.group("at"), (verb, state, m.group(0))
                        assert os.path.samefile(m.group("at").split()[1], repo), m.group(0)
```

The case's docstring then names the rows it reads: both ladders' deny, both
attempts of every choice row, and the creation ladder's token row. The note's
`restore` lines are pinned by the tracked-changes case, which is why the
pattern no longer carries them.

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_worktree_guard.py` and `tests/test_the_guard_asks_once_per_session.py`, at the target | exit 0, 185 passed |
| `git_at` over thirteen shell positions, `top` the fixture repository | as listed under *The new units*: five bare, eight `-C <top>` |
| Every `git <word>` in the reasons of eight rows × three shell positions × up to two attempts | from another repository, bare: `git worktree list` (ACTIVE deny, both switch choice fallbacks), `use git switch` (creation detection-unusable fallback), and the prose mentions at `:1813`, `:1828` and the creation origin line |
| Row 3 with a force-staged anchored path, shell in another repository, a subdirectory and the root | ask each time; both `restore` lines carry `-C <root>` |
| The printed `-C` advice run back through the guard from another repository | `[shared-tree-ok]` passes both choice rows; `[worktree-ok]` reaches the creation token row |
| The judged repository at a path with a space and an apostrophe, ACTIVE deny | `fetch` line splits correctly; both `worktree add` lines fail `shlex.split` |
| M18, force-staged check back to `eff_cwd`, three modules | exit 1; the force-staged case alone red |
| M19, the note's command word back to bare `git`, three modules | exit 1; the tracked-changes case alone red |
| MU, the creation token row's `steer_to_switch()` bare, three modules | exit 0, 185 passed: survives |
| MI, the creation idle fallback's `steer_to_switch()` bare, three modules | exit 0, 185 passed: survives |
| ML, `git worktree list` given the command word, three modules | exit 0, 185 passed: nothing pins the line |
| fe24f07's hook against the target's cases, three modules | exit 1; the three new or extended cases red, 182 passed |
| Paste-ready fixes 1–2 with the paste-ready case 3 | exit 0, 185 passed. The same case on the target hook: exit 1 at `git worktree list`. Under MU and under MI: exit 1. Fixes 1–2 with the committed case: exit 0 |
| `survivor_check.py --range e6435da..1c5dc5c`, without and with `--exempt survivors.md` | exit 1 (one survivor, two shared phrases), then exit 0 |
| `bin/evidence-check . --strict` at the target | exit 0, 0 drifted |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: no run exists, and it belongs to the sealer. This round leaves 🟡 1 and 🟡 2 open, and the run is capped, so what follows is the orchestrator's filing and then the sealer's spawn |

Needs a fix: yes — 🟡 1 (`git worktree list` and the creation fallback's `git switch` name the shell's tree, against the spec paragraph and W10) and 🟡 2 (the worktree root unquoted in the printed `worktree add` lines, older than the work item)
Loses a record or crashes: no

## Regression tests to plant

- `tests/test_guard_resolves_the_tree_it_judges.py`: replace the class case's pattern and row loop with paste-ready fix 3. It covers 🟡 1 and ⬜ 3.
- `tests/test_guard_resolves_the_tree_it_judges.py`: for 🟡 2, a case that puts `repo` under a directory whose name has a space and an apostrophe, drives the ACTIVE deny from another repository, and asserts every line holding `worktree add` survives `shlex.split` with the path as one word. Not written or run here.

## Facts for the evidence ledger

- W10's clause *every command a guard reason tells the person to run names the tree it is about* is false at the target for `git worktree list` (`hooks/worktree-guard.py#main`) and for the creation detection-unusable fallback (`hooks/worktree-guard.py#guard_worktree_creation`). It becomes true with fix 1; re-read it then.
- `git_at` returns bare `git` through a symlink and through a case variant on macOS because `git rev-parse --show-toplevel` canonicalises both; `os.path.normcase` is the identity on POSIX. Executed on one machine.

## Proof block

Files I opened: `hooks/worktree-guard.py` (whole), `hooks/cmdline.py` (`parse_git`),
`tests/test_guard_resolves_the_tree_it_judges.py`,
`tests/test_the_guard_asks_once_per_session.py` (the diff and `MEASURED_RUN`),
`tests/conftest.py` (the `repo` fixture and transcript isolation),
`docs/worktree-guard-spec.md` (the diff),
`seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md`,
`seal/specs/1790550712-the-worktree-guard-judges-a-switch-after-a-creation/rounds/round-2.md`,
the head of `rounds/round-2-report.md`, the diffs of `plan.md` and `survivors.md`,
`bin/test`, `bin/survivor-check`.
