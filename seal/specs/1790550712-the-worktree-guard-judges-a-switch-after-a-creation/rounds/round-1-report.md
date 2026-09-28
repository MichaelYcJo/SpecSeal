# Round 1 report — 1790550712-the-worktree-guard-judges-a-switch-after-a-creation

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 77ad1751ada622ead45ac94391714cbb6c0e4f6c |
| Base | origin/release/v0.15.6 (= main 2037cf0) |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at the target, a second at the base, a third for mutations; all removed |

## Summary

The #620 fix holds. I ran it against every shape the prompt named, and no cell
is looser than the base or weaker than either half, and none reaches `allow`.
#624 and #243 hold as well. Every sentence the spec document now states about
them is true under execution, and each case it cites turns red when its
mutation is applied.

There is one 🟡, and this branch did not cause it. The switch ladder's
tracked-changes row, which this branch edited for #624, checks the session's
own directory for uncommitted changes rather than the tree the switch acts on.
The base behaves the same way, byte for byte. There is also one ⬜ about the
wording of the policy document.

## Findings

### 🟡 1 — The dirty-tree row asks about the session's directory, not the tree the switch is in

`hooks/worktree-guard.py:2319` reads `entries = tracked_changes(cwd)`, and
`:2323` reads `phantom_entries(entries, cwd)`. Every other part of the ladder
judges the switch's own tree (`eff_cwd`, which is `switch_at` whenever a switch
was found): `repo_paths(eff_cwd)` and `sessions_in_tree(top, …)`. Only this row
uses the shell's starting directory.

Executed, identical at the base and at the target:

- `git -C <repo> switch feature/x`, from a directory outside any repository,
  with `<repo>` dirty, is **silent**. §A says `ask`.
- `cd <repo> && git switch feature/x`, from the same place and with the same
  dirty tree, is **silent**.
- `git -C <other clone> switch feature/x` from a dirty session tree, where
  `<other clone>` is clean, **asks**. It lists the session tree's changes and
  says *They will follow you onto the target branch*, which is false.
- `git -C <other clone> switch feature/x` from a clean session tree, where
  `<other clone>` is dirty, is **silent**.

Why it matters: §A promises that a switch over tracked changes asks. The row
keeps no tree safe, so this is not a concurrency hole. The harm is that the
person is not told the changes will ride along. This work item's own
`spec.md` decision 2, last row, says a command whose halves sit in different
repositories is judged by *the same rows, each judged against its own tree*.
Row 3 is the one row where that is not so.

The class, enumerated: the only readers in `main` below the walk that take
`cwd` instead of the judged tree are `tracked_changes` and `phantom_entries`
(read). `judge_creation(command, cwd, …)` passes `cwd` on purpose, and its
comment says why: it is where `walk_command` starts, not a tree being judged.

The orchestrator decides where this goes. The fix sits inside a unit this
branch already edited, and it is two arguments plus a case. Alternatively it
goes to a new issue answered by the orchestrator. It is not #630's shape,
because #630 is a second tree and this is the first tree read from the wrong
directory.

### ⬜ 2 — "An expansion" is placed in the silent group, and two expansions deny

`docs/worktree-guard-spec.md:258` lists *an expansion* among the command words
that `cmdline.parse_git` does not read as git, which the guard is silent on
without consent. Executed at the target, without consent: `~/git worktree add
../wt f` and `*/git worktree add ../wt f` **deny**. The tilde and the glob
expand to a path, and `parse_git` reads it as git. `gi*`, `$GIT`, backticks and
`$(which git)` are silent, as the sentence says. The paragraph's own first half
already files `~/git` under *every path*, so a careful reader can recover the
right reading. The sentence alone cannot give it.

The behaviour is right and conservative, which is why this is ⬜.

## Confirmed, with grounds

- **#620, order independence (executed).** A test_tmp probe ran 58 command
  shapes. They cover all 5 creation spellings × 8 switch spellings joined by
  `&&`, and three pairs under `;`, `||`, `|`, a newline and a subshell on
  either side. Each ran in both orders × 5 tree states × {no consent, record,
  routing answer} × {no token, `[worktree-ok]`, `[shared-tree-ok]`}, with a
  second shell directory outside any repository for the `&&` grid, and 3
  attempts on one session id per cell. That is 4410 cells, at the target and
  at the base.
  - The two orders gave the same decision and the same reason byte for byte
    in 4362 of the 4410 cells.
  - The other 48 differ, and all of them are one shape:
    `cd <repo> && git switch feature/x` as the switch half, run from outside
    any repository with no consent. These are two different commands, not
    one command in two orders. In switch-first, the `cd` moves the creation
    into the repository. In create-first, the creation runs from outside,
    where git refuses it and `&&` never reaches the switch.
  - At the base the same probe found 1808 order-differing cells.
- **Never weaker, never `allow` (executed).** At attempt 1, no combined verdict
  ranked below the switch alone or the creation alone as a compound, under
  `deny` > `ask` > `silent` > `allow`. No combined cell answered `allow`. No
  cell at any attempt was looser than the base, and every cell that moved was
  create-first and moved stricter.
- **#624.1, malformed transcripts (executed).** A JSON string line, `null`, a
  list line, an assistant entry with no keys, a non-dict `message` and a
  non-list `content` all return False or skip without raising. So do
  `isSidechain` as `"false"`, `None`, `0`, `True`, `"true"`, `1` or absent.
  The assistant half reads no `isSidechain` at all, so nothing new is
  accepted: the condition only narrows (read, `hooks/worktree_consent.py`,
  in `automation_answered`).
- **#624.2 and #624.3 (read and executed).** Row 3 is reached only in
  single-stream or under `[shared-tree-ok]`, because `choose` and `respond`
  both exit. So `single_stream = not idle and reliable` names what was
  counted. The `[worktree-ok]` opening is reached only after the ACTIVE row,
  so *can be shown to be working* is true in both reliable states.
- **Mutations (executed, each restored from kept bytes).** Each ran over the
  two guard modules:
  - The base walk (a switch after a creation ignored): the five new #620
    cases.
  - Row 3 always single-stream: `test_the_dirty_tree_row_names_what_was_measured`.
  - Row 3 single-stream from `reliable` alone: the same case.
  - The English token lead replaced by the old one: the same case.
  - `is True` restored: `test_a_sidechain_entry_is_not_consent`.
  - `before_ask` removed from row 1-b only: the sweep and the spent-budget
    case.
  - `before_ask` removed from row 2 only: the same two.
  - The basename comparison: the command-word case and the path-qualified
    case.
  - The old `[worktree-ok]` wording: both reason cases.
  - Heredoc bodies kept: `test_a_git_command_inside_a_heredoc_body_is_not_judged`.
  - The `judge_creation` call above row 3 removed: four cases, the sweep
    among them.

  All eleven were killed. Each cited case is one that holds its sentence. The
  spec document's *Removing `before_ask` from either choice row turns the
  sweep red* is true.
- **The class sentences (executed).** The command-word paragraph was run over
  22 words, with and without a record. With a record, only the lexer's
  spelling of the word `git` allows (`\git` included), and everything else is
  silent, with no `ask` anywhere. Without a record, every word `parse_git`
  reads is `deny`, and every word it does not read is silent, except as ⬜ 2
  notes.
- **Copies (executed grep, read).** Old phrases found outside past records:
  - *is working in this tree* survives only at `hooks/worktree-guard.py:1851`.
    That is the single-stream deny, which is reached with nobody counted, so
    it is true there.
  - *exactly five*, *falls to `ask`* and *IS exactly a git command* survive
    only as quotations of what was corrected.
  - `README.md` and `README.ko.md`'s worktree-guard and `[shared-tree-ok]`
    rows stay true, because the dirty-tree row still asks.
- **Ledger (executed).** `bin/evidence-check --strict`, unscoped, exits 0:
  2479 ok, 0 drifted, 0 broken, 0 malformed. `bin/correction-check --range
  2037cf0...HEAD` finds no merge commit to have dropped a correction. The
  re-read notes on 0.15.5 A1, A3, A4 and A5, the six 0.9.1 rows and 0.9.4
  S3 and S4 were each read against the diff of their anchor, and each says
  what changed. Two parts rest on the smith's own runs and were not
  re-executed here: W1–W8's mutation counts (M1′, M4, M6's *eleven*), and
  the *twelve more quoting spellings* credited to an earlier round.

## Regression tests to plant

- `tests/test_worktree_guard.py`: the dirty-tree row reads the switch's tree
  (finding 1, in the fence under *Paste-ready fixes*). Show it red against the
  target first.

## Facts for the evidence ledger

- If finding 1 is absorbed, a row in
  `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md`
  saying that the tracked-changes row reads the tree the switch acts on,
  anchored on `hooks/worktree-guard.py#main` and the new case.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The switch ladder's tracked-changes row reads `cwd`, not the switch's tree, so a dirty tree reached by `git -C` or `cd` is silent and a clean one is asked about the session tree's changes | `hooks/worktree-guard.py:2319` | open | Executed, identical at base and target. Not caused by this branch; the unit is one it edited, and `spec.md` decision 2's last row says each half is judged against its own tree |
| ⬜ 2 | *an expansion* is filed under the no-consent silent group, but `~/git` and `*/git` deny | `docs/worktree-guard-spec.md:258` | open | Executed: 22 command words with and without a record |
| 🟢 | #620: both orders get the same decision and reason, the combined verdict is never weaker than either half and never `allow`, and nothing is looser than the base | `hooks/worktree-guard.py:2053` | confirmed | Executed over 4410 cells at target and base; the 48 differing cells are one shape that is not the same command in two orders |
| 🟢 | #624.1: `isSidechain` must be literally `false`, and no malformed line raises | `hooks/worktree_consent.py:315` | confirmed | Executed, eight malformed shapes and seven values |
| 🟢 | #624.2 and #624.3: both openings name what was counted, both languages | `hooks/worktree-guard.py:2338` | confirmed | Read against the ladder's exits; three mutations killed |
| 🟢 | #243: the class paragraph, the property paragraph and the heredoc removal are held by the cases they cite | `docs/worktree-guard-spec.md:245` | confirmed | Executed, eleven mutations each killed by its cited case |
| 🟢 | Ledger re-read notes and anchors | `seal/releases/0.9.1.md:144` | confirmed | `bin/evidence-check --strict` exit 0; notes read against each anchor's diff |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the two guard modules, in the target clone | 159 passed, exit 0 |
| Order and strictness sweep, 58 shapes, 4410 cells, at target and at base | 0 looser than base, 0 weaker than a half, 0 `allow`; 48 order differences, all the `cd`-in-switch-half shape from outside a repository |
| Eleven single mutations over the two guard modules | 11 killed, each by the case the document cites |
| Row 3 directory probe, `-C` and `cd` switches with the dirty tree on either side | silent where §A says ask, ask about the wrong tree; identical at base |
| Command-word probe, 22 words × {no record, record} | with a record only the word `git` allows; without, `~/git` and `*/git` deny |
| Transcript reader, eight malformed shapes | none raised; none counted as consent |
| `bin/evidence-check --strict`, unscoped | exit 0, 2479 ok |
| `bin/correction-check --range 2037cf0...HEAD` | exit 0, no merge commit |
| The full suite, repository-wide lint, typecheck (the broad gate) | not yet — no run exists; it belongs to the sealer, after the rounds settle |

## Paste-ready fixes

### 🟡 1

```python
    # 3) 단건이지만 추적 중인 변경이 있으면 사용자에게 확인.
    #
    # Read from the tree the switch acts on, not from where the shell started:
    # `git -C <repo> switch x` or `cd <repo> && git switch x` from elsewhere
    # carries <repo>'s changes, not the session directory's.
    entries = tracked_changes(eff_cwd)
    if entries:
        single_stream = not idle and reliable
        listing = "\n".join(f"    {xy}  {path}" for xy, path in entries)
        phantoms = phantom_entries(entries, eff_cwd)
```

```python
def test_the_dirty_tree_row_reads_the_tree_the_switch_is_in(
    monkeypatch, capsys, repo, tmp_path
):
    """The tracked-changes row asks about the tree the switch acts on. Seen
    red at 77ad175: silent from outside a repository, and an ask about the
    session tree's changes for a `-C` switch into a clean clone."""
    outside = tmp_path / "outside"
    outside.mkdir()
    other = tmp_path / "other"
    subprocess.run(["git", "clone", "-q", str(repo), str(other)], check=True)
    (repo / "f.txt").write_text("changed on purpose\n")
    for n, command in enumerate(
        (f"git -C {repo} switch feature/x", f"cd {repo} && git switch feature/x")
    ):
        decision, reason = decide(
            monkeypatch, capsys, repo, command, session_id=f"t{n}", cwd=outside
        )
        assert decision == "ask", (command, decision, reason)
        assert "f.txt" in reason, reason
    decision, reason = decide(
        monkeypatch,
        capsys,
        repo,
        f"git -C {other} switch feature/x",
        session_id="t-other",
        cwd=repo,
    )
    assert decision == "silent", (decision, reason)
```

The `phantom_entries` note prints `git restore --staged <path>` lines to run.
Where `eff_cwd` is not the shell's directory, those lines want `git -C
<tree>` in front, or the lead should name the tree.

### ⬜ 2

```markdown
like any other. One it does not read as git — an expansion the lexer leaves
unexpanded (`$GIT`, `gi*`, a command substitution), a different case, a
trailing slash, a wrapper it does not read past such as `nice` — is not a git
invocation to this guard, and it says nothing. `~/git` and `*/git` are paths
once expanded, and belong to the first group.
```

Needs a fix: yes — 🟡 1, the dirty-tree row reading the session directory; it predates this branch, and absorbing it here or deferring it to a new issue is the orchestrator's call

Loses a record or crashes: no

## Out of scope, and said so

- `#630` shapes (a second tree, a second clone) were not probed; they are
  deferred there already.
- The prompt ordered nothing broad; nothing was declined.

## Proof block

Files opened: `hooks/worktree-guard.py` (the module docstring, `_judgment_text`,
`walk_command`, `only_creates_a_worktree`, `judgeable`, `classify`,
`tracked_changes`, `respond`, `repo_paths`, `choose`, `guard_worktree_creation`,
`judge_creation`, `main`), `hooks/worktree_consent.py` (`automation_answered`,
`consent`, `creation_directory`), `hooks/cmdline.py` (`adds_a_worktree`,
`apply_chdir`), `docs/worktree-guard-spec.md` (§A, §*Creation consent*,
§*Known limits*), the diff of `tests/test_the_guard_asks_once_per_session.py`
and `tests/test_worktree_guard.py` with the helpers `decide`, `grant`,
`ask_entries`, `write_transcript`, `projects`, and the sweep case read whole,
`seal/releases/0.15.5.md`, `0.9.1.md` and `0.9.4.md` (the changed rows),
`seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md`,
this work item's `spec.md`, `overview.md`, `changelog.md`, `plan.md`
(§*Enumerated copies* and the walk shape), `phases/phase-1.md`, `README.md` and
`README.ko.md` (the worktree-guard and token rows), and `CONTRIBUTING.md`'s
runner lines.
