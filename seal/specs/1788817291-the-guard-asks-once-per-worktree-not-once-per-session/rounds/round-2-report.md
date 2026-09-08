# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — review round 2, report

## What this round was asked

Round 2 is the verifying round, at target `62b2d2e`, base `origin/release/v0.9.1`,
in the worktree for branch `fix/237-the-guard-asks-once-per-worktree-not-once-per-session`.
Round 1 is recorded and closed at `d82a02c`; its verdicts are inherited. The
surface is the diff of its fixes, `d82a02c..62b2d2e`, whose substance is
`86c4ddb`, `20553cb`, `a9e76c2` and `3cf979b`. The `release/v0.9.1` merge that
follows is not this branch's work.

The round was pointed at three things the fix pass did beyond what it was
handed, each a target: its refusal of round 1's paste-ready fix for finding 2,
with `test_the_switch_ladder_keeps_every_verdict_it_had` reported red under the
reviewer's alternative; the three further escapes its own re-enumeration found,
one of them a dirty tree deciding whether the creation question was put at all;
and its removal of the `cmdline.understood` and `Unresolved` checks on the
grounds that the command-word test strictly dominates them. It was also told to
re-derive the sweep rather than accept it, to verify the prompt budget and judge
whether the third residual is honestly stated, to check that three things have
not changed, to check both `❓` have an answerer, to check the `evidence-check`
finding reached a home outside this work item, and to check that no `# RIDER:`
this branch plants names a commit of this branch.

## What was found, in the order the causes run

The fix moved the creation question up into the switch ladder and put it below
three rows. **The reason it gives for those three is that all of them deny**,
and a `deny` stops the creation along with the rest of the command — written in
as many words at `docs/worktree-guard-spec.md:168` and at
`hooks/worktree-guard.py:2049`.

**Two of the three do not always deny.** They are `choose` sites, and `choose`'s
own first line says what it does: *Deny once and hand the user the two options;
ask on every attempt after* (`hooks/worktree-guard.py:1368`). On the second
attempt in the same session the verdict is `ask`, the question is about
switching branches in a shared tree, and approving it runs the whole command —
so the worktree is created and session-wide consent is minted with the creation
question never put. That is finding 1, and it is the un-enumerated remainder of
the class the fix pass closed for row 3.

Separately, the new bound's first test is `os.path.basename(tokens[0]) != "git"`
(`hooks/worktree-guard.py:436`), under a docstring that calls it *`git` is the
segment's OWN command word* (`:401`). A basename is not an identity: executed,
`/tmp/evil/git worktree add ../wt f` answers `allow`. That is finding 2.

Everything else the round was asked to attack held, and the two refusals the fix
pass made against round 1 are correct — the mutation that applies the reviewer's
alternative turns the shipped case red exactly as reported.

---

### 1 · 🟡 Two of the three rows kept above the creation do not deny, and the second attempt asks about the switch

`hooks/worktree-guard.py:2049` (the ordering comment) · `:1368` (`choose`) ·
`docs/worktree-guard-spec.md:168` (the ladder table) ·
`seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:73`

The ladder table's first row groups *ACTIVE session · only IDLE · detection
unusable* and justifies their precedence with **every one of them denies**. Only
the ACTIVE row is a plain `respond("deny", …)`. The other two call `choose`,
which spends one deny per session per direction and answers `ask` afterwards.

**Executed**, clean tree, no consent record, the same command twice in one
session:

| Tree state | Attempt 1 | Attempt 2 | Was the creation question put? |
|---|---|---|---|
| only idle sessions | `deny` | **`ask`** | no, on either attempt |
| detection unusable | `deny` | **`ask`** | no, on either attempt |

The `ask` a person sees at attempt 2 is the switch site's own fallback, printed
in full by the probe: *Approve — switch branches in this shared tree*. Nothing
in it says a worktree is about to be created. `worktree_consent.creation_directory`
resolves a repository for that command, so approving mints the record and every
later creation in the session answers `allow`.

Compare the same session state with the creation written on its own: `git
worktree add ../wt f` answers `deny` **with** the creation question put. So
composing the creation behind a `git switch` downgrades the creation question to
a switch question — round 1's finding 2 one prompt weaker instead of zero
prompts.

**Why this is the same class the fix pass already closed.** Row 3 was moved
below the creation because *its own text says the switch is ALLOWED* and
approving it created the worktree too. Rows 1-b and 2 have that property on
their second attempt, and the fix pass's stated ground — they are the
concurrency protections, and they deny — is true of row 1 alone.

**Scale.** A sweep of 18 commands × 4 tree states × 2 shell directories × 2
attempts, with one session id per (state, directory) so the `choose` budgets are
spent, gives **288 pairs, 0 silent, and 64 where the writer records, the guard
answers `ask`, and the creation question was never put** — every one of them in
the idle or detection-unusable state. Two of the 64 are worse than a plain
creation: `git switch feature/x && git worktree add ../wt f $(touch /tmp/m)` and
`… && sudo git worktree add ../wt f` reach the same switch `ask`, whose approval
covers the substitution and the wrapper.

The fix below moves the creation question above the two `choose` rows and leaves
the ACTIVE deny where it is. Executed with it applied: the creation question is
put on both attempts in both states, and
`tests/test_the_guard_asks_once_per_session.py`,
`tests/test_worktree_guard.py`, `tests/test_worktree_guard_signals.py` and
`tests/test_guard_resolves_the_tree_it_judges.py` stay green.

### 2 · 🟡 The command-word test reads a basename, so any executable named `git` collects the allow

`hooks/worktree-guard.py:436` · `:401` (the docstring that states the bound)

The new test is `if os.path.basename(tokens[0]) != "git": return False`. The
docstring calls it *`git` is the segment's OWN command word*, and gives the
reason: *a user's own `permissions.deny` on `Bash(sudo:*)` must not be spoken
over by a hook that was reasoning about worktrees*. That reason does not stop at
`sudo`.

**Executed**, with a consent record present:

| Command | `only_creates_a_worktree` | Guard |
|---|---|---|
| `./git worktree add ../wt f` | True | **`allow`** |
| `/tmp/evil/git worktree add ../wt f` | True | **`allow`** |
| `../git worktree add ../wt f` | True | **`allow`** |
| `bin/git worktree add ../wt f` | True | **`allow`** |
| `sudo git worktree add ../wt f` | False | `ask` |

`permissionDecision: "allow"` covers the whole tool call, so a session that has
had one worktree creation approved can run an arbitrary executable with no
prompt by giving it the filename `git`. How much that is worth is the second
`❓` this branch already carries — if a user's `permissions.deny` outranks a
hook `allow`, the damage is bounded by that rule; if it does not, nothing is
between the model and the binary.

This shape was allowed at `d82a02c` too, so it is not introduced by the fix. It
is the part of round 1's finding 3 class the fix did not enumerate, in a line the
fix wrote (`agent-contract` §12).

The fix below asks for `git` itself rather than for a filename. What it costs is
one prompt on `/usr/bin/git worktree add …`, which is the same trade
`pr-notes.md` §3 already made for `$`, a backtick, `<` and `>` — *one prompt on a
shape nobody writes a worktree creation as*. Executed with it applied, the four
rows above fall to `ask`, `git -C <repo> worktree add …` and `git worktree add
../a -b feature/x origin/main` still allow, and the four guard modules stay
green.

### 3 · 🟢 Refusing round 1's paste-ready fix for finding 2 was right

**Executed**, as a mutation: the reviewer's alternative (`if reason is None or
found == "worktree-add"`) applied to `hooks/worktree-guard.py`, the shipped
module run, source restored from bytes saved first.

```
FAILED tests/test_the_guard_asks_once_per_session.py::test_the_switch_ladder_keeps_every_verdict_it_had
E           AssertionError: ([(111, '/tree', 1.0, 0.5, 'VS Code')], [], True)
E           assert 'ask' == 'deny'
1 failed, 32 passed
```

The row that breaks is the ACTIVE one, which is the protection the fix pass
named. Asked directly, `judge_creation` on `git switch feature/x && git worktree
add ../wt f` under an ACTIVE session with no record answers `ask` — so the
branch would be taken out from under the other session one approval later,
exactly as the refusal says. `restored: True`.

### 4 · 🟢 The shape shipped instead judges a creation wherever it sits

The walk records `creation_at` for a `git worktree add` in any segment while
`reason` still takes the first segment that classifies, and both silent exits —
`if not top` at `:1884` and the ladder's end at `:2067` — call `judge_creation`
before they take.

**Executed**, re-derived rather than accepted: 18 command shapes × 4 tree states
× 2 shell directories, a fresh session id per cell, comparing the guard's
verdict against whether `worktree_consent.creation_directory` resolves a
repository. **144 pairs, 64 silent, 0 holes.** The shared-session sweep in
finding 1 adds 288 more with the same result on silence. The shapes round 1
found (`&&`, `;`, `git checkout … &&`) and the one the fix pass added (the shell
outside any repository with a `git -C <repo> worktree add` inside the command)
are all in the enumeration.

### 5 · 🟢 The dirty-tree escape is closed, and the new ordering moves no other verdict

**Executed.** `git switch feature/x && git worktree add ../wt f` on a dirty tree
answers `deny` with the creation question put, where before the fix it asked
about the uncommitted changes. `test_a_dirty_tree_does_not_decide_whether_the_creation_is_questioned`
pins it. Nothing else in the ladder moved: the four guard modules plus
`tests/test_dispatch.py` are **166 passed, 1 skipped** at `62b2d2e`, and the
five invariant probes in finding 10 answer as they did before the branch.

### 6 · 🟢 The command-word test does dominate `cmdline.understood` and the `Unresolved` check

**Executed** over 18 shapes, comparing the shipped predicate against what the two
removed checks would have answered on the same walk. **No shape where the removed
checks refuse and the shipped one allows.** Four go the other way, which is the
domination claimed: `time git worktree add …`, `sudo git worktree add …`, `! git
worktree add …` and `cd /tmp && git worktree add …` are all `understood`-clean
and shipped-refused.

Read, and it is why the enumeration comes out that way: `cmdline.understood`
returns False only for a subshell or brace group, an assignment-only segment, a
reserved word, a relocator, a function definition, or a command word carrying an
expansion character. Every one of those puts something other than `git` in
`tokens[0]`, or puts a character `ELSEWHERE` already refuses. Finding 2 is the
one place the shipped test is weaker than its own docstring, and `understood`
would not have caught that either — it reads past nothing on `/tmp/evil/git`.

### 7 · 🟢 The prompt budget holds, and the third residual is honestly stated

**Executed**, clean single-stream tree, six `git worktree add ../wt f` calls in
one session with the record written after the first: **deny, allow, allow,
allow, allow, allow.**

The residuals, same session:

| Shape | Verdict |
|---|---|
| `git worktree add ../wt f` again | `allow` |
| `git switch feature/x && git worktree add ../wt f` | `ask` |
| `cd /tmp && git worktree add ../wt f` | `ask` |
| `git worktree add "$HOME/wt" f` | `ask` |
| `git worktree add ../wt f > /tmp/x` | `ask` |
| `sudo git worktree add ../wt f` | `ask` |

`pr-notes.md` §3 states the third residual as *the budget catching up with the
bound rather than the bound being widened*, and that reading is the right one:
the eleven shapes it names were allowed at `d82a02c` while the docstring already
claimed they were not, so refusing them restores a bound rather than adding one.
It also names what stays allowed. The one omission is finding 2's shape, which
belongs in that list either way the finding is settled.

### 8 · ⬜ The 576 in two documents cannot be reconstructed from what they say

`seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:77`
· `docs/worktree-guard-spec.md:176`

Both say *576 command/tree-state/directory combinations*, and neither says what
576 factors into. The enumeration this round ran with those three axes is
18 × 4 × 2 = 144. The property is confirmed — 0 holes at 144, and 0 again at
288 — so nothing about the guard is in question; what a reader cannot do is
reproduce the figure. `agent-contract` §5: a count can be checked while the
claim it stands for cannot. Paperwork, not counted in `Needs a fix`.

### 9 · 🟢 Both `❓` have an answerer, and the unfavourable answer has a stated cost

Read. `overview.md` §*Not verified* carries both rows with **the repository
owner** named, and the `permissions.deny` row records that round 1 widened what
rides on it. `pr-notes.md` §4 answers both: the auto-answered `ask` is stated in
the present tense with `--dangerously-skip-permissions` named, and the
`permissions.deny` row says what the guard does if the answer is unfavourable —
`guard_worktree_creation`'s consented row answers `ask` rather than `allow`, one
word at one site, costing the whole budget.

### 10 · 🟢 Nothing that must not change has changed

**Executed**, no consent record in any row:

| | Verdict |
|---|---|
| creation, single-stream clean tree | `deny`, steered to `git switch` |
| creation, ACTIVE session | `ask` |
| creation, detection unusable | `deny` (the `choose` first attempt) |
| plain `git switch feature/x`, clean single-stream | silent |
| plain `git switch feature/x`, ACTIVE session | `deny` |

And no path lets a session with no prior approval create a worktree silently:
432 pairs across the two sweeps, 0 silent where the writer would record.

### 11 · 🟢 The `evidence-check` finding reached a home with an answerer

Read. `seal/follow-up.md` carries it as a schedulable row with **the repository
owner** named, with the executed evidence in the row (the total stayed at 771,
`--strict` reported `0 broken`, `--reverify` reported `0 rows re-verified`) and
the judgment it needs stated.

### 12 · 🟢 No `# RIDER:` on this branch names a commit of this branch

Read and executed. The branch's own diff against `origin/release/v0.9.1` adds no
`# RIDER:` and no `Verified … at <sha>` line. Every stamp in the tree names
`9829412`, `4f78074`, `5a831e8`, `4581fe1`, `70c272c`, `9241a8b` or `00e63c3`;
`git merge-base --is-ancestor 00e63c3 origin/release/v0.9.1` exits 0, so the one
recent SHA is on the release branch and survives the merge into `main`. #239's
failure mode is absent here.

### 13 · ⬜ A record this branch committed carries a real user path, and it makes a shipped test red

`seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-report.md:8`

The `Worktree` field of round 1's report holds the absolute path of the machine
it ran on. `CLAUDE.md` §*Repo rule — no real identifiers in examples or
fixtures* says fixtures and docs use `/Users/x/` only, and
`tests/test_no_real_identifiers.py::test_only_fixture_user_paths` enforces it.

**Executed** at `62b2d2e`: that case is **red**, and this line is the only
violation in the whole of `seal/`. The file was committed at `86c4ddb`, so it is
this branch's; `origin/release/v0.9.1` carries nothing like it.

Its location is under `seal/specs/`, so it is a correction to the run's
paperwork rather than a defect in the tool, and it is out of `Needs a fix`. It
is written up anyway because the orchestrator's broad gate will hit it, and a
red case with no explanation costs a round to trace.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 Two of the three switch-ladder rows kept above the creation do not deny — `choose` denies once per session and asks after — so on the second attempt a person is asked about the switch, approving creates the worktree, and session-wide consent is minted with the creation question never put | `hooks/worktree-guard.py:2049` · `:1368` · `docs/worktree-guard-spec.md:168` | open | **Executed.** Same command twice in one session: idle → `deny`, then `ask`; detection unusable → `deny`, then `ask`; the creation question put on neither. The bare creation at the same state denies WITH it put. 288-pair sweep with the `choose` budgets spent: 64 pairs where the writer records, the guard answers `ask`, and `judge_creation` never ran. The fix below is executed and leaves the four guard modules green |
| 2 | 🟡 `os.path.basename(tokens[0]) != "git"` is the whole command-word test, so any executable whose filename is `git` collects the `allow` that covers the tool call | `hooks/worktree-guard.py:436` · `:401` | open | **Executed** with a record present: `./git`, `/tmp/evil/git`, `../git` and `bin/git worktree add ../wt f` all answer `allow`, `sudo git …` answers `ask`. The docstring's own reason for the test — a user's `permissions.deny` must not be spoken over — does not stop at `sudo`. Present at `d82a02c` too, so it is the unenumerated part of round 1's finding 3 class, in a line the fix wrote. Fix executed: the four fall to `ask`, `git -C <repo> worktree add …` and `-b <branch> <start>` still allow, modules green |
| 3 | 🟢 The refusal of round 1's paste-ready fix for finding 2 | `hooks/worktree-guard.py:1655` · `tests/test_the_guard_asks_once_per_session.py:408` | answered | **Executed** as a mutation, source restored from bytes saved first (`restored: True`): the alternative turns `test_the_switch_ladder_keeps_every_verdict_it_had` red on the ACTIVE row, `assert 'ask' == 'deny'`, 1 failed 32 passed. `judge_creation` under an ACTIVE session with no record answers `ask`, which is the protection the refusal names |
| 4 | 🟢 The shape shipped instead judges a creation wherever it sits, at both silent exits | `hooks/worktree-guard.py:1884` · `:2067` | answered | **Executed.** 18 commands × 4 tree states × 2 shell directories, fresh session id per cell: 144 pairs, 64 silent, **0** where the writer records and the guard is silent. Round 1's three shapes and the fix pass's `if not top` shape are in the enumeration |
| 5 | 🟢 The dirty-tree escape is closed and the new ordering moves no other verdict | `hooks/worktree-guard.py:2067` · `tests/test_the_guard_asks_once_per_session.py:434` | answered | **Executed.** Dirty tree, `git switch feature/x && git worktree add ../wt f` → `deny` with the creation question put. Five guard modules at `62b2d2e`: **166 passed, 1 skipped** |
| 6 | 🟢 The command-word test strictly dominates the removed `cmdline.understood` and `Unresolved` checks | `hooks/worktree-guard.py:401` · `hooks/cmdline.py:1282` | answered | **Executed** over 18 shapes: no shape where the removed checks refuse and the shipped one allows; four where the shipped one is stronger (`time`, `sudo`, `!`, `cd &&`). **Read**: every input `understood` refuses puts something other than `git` in `tokens[0]` or a character `ELSEWHERE` refuses |
| 7 | 🟢 The prompt budget is unchanged and the third residual is honestly stated | `pr-notes.md` §3 | answered | **Executed.** Six creations in one session, clean single-stream: deny, allow, allow, allow, allow, allow. Compound, `cd` prefix, expansion, redirection and wrapper each `ask`; a plain repeat still `allow`. §3's framing is right — the eleven shapes were allowed while the docstring already claimed they were not. Its still-allowed list omits finding 2's shape |
| 8 | ⬜ The `576 command/tree-state/directory combinations` in two documents cannot be reconstructed — the three axes stated give 144 | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:77` · `docs/worktree-guard-spec.md:176` | open | **Executed**: the property holds at 144 and again at 288, so nothing about the guard is in question. `agent-contract` §5 — a count can be checked while the claim it stands for cannot. Paperwork; not counted in `Needs a fix` |
| 9 | 🟢 Both `❓` carry an answerer, and `pr-notes.md` says what the guard does if the answer is unfavourable | `overview.md` §*Not verified* · `pr-notes.md` §4 | answered | **Read.** Both rows name the repository owner. §4 states the auto-answered `ask` in the present tense with `--dangerously-skip-permissions` named, and gives the fallback for `permissions.deny`: the consented row answers `ask` rather than `allow`, one word at one site |
| 10 | 🟢 A session with no consent record still asks, the single-stream site still denies and steers to `git switch`, and no path creates a worktree silently without prior approval | `hooks/worktree-guard.py:1655` | answered | **Executed.** Creation with no record: `deny` on a clean single-stream tree with the `git switch` steer, `ask` under an ACTIVE session, `deny` at the first detection-unusable attempt. Plain switch unchanged in both directions. 432 pairs across the two sweeps, 0 silent where the writer would record |
| 11 | 🟢 The `evidence-check` finding was recorded outside this work item with an answerer | `seal/follow-up.md` | answered | **Read.** A schedulable row naming the repository owner, carrying the executed evidence and the judgment it needs |
| 12 | 🟢 No `# RIDER:` this branch plants names a commit of this branch | `hooks/worktree-guard.py:1760` | answered | **Executed.** The branch's diff against `origin/release/v0.9.1` adds no rider and no stamp. `git merge-base --is-ancestor 00e63c3 origin/release/v0.9.1` exits 0, so the newest stamp in the tree sits on the release branch |
| 13 | ⬜ Round 1's report states the machine's own absolute path in its `Worktree` field, which turns `tests/test_no_real_identifiers.py::test_only_fixture_user_paths` red | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-report.md:8` | open | **Executed** at `62b2d2e`: that case fails, naming this line, and it is the only real user path anywhere under `seal/`. Committed at `86c4ddb`, so it is this branch's; the base carries none. `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* is the rule. Under `seal/specs/`, so it is a correction and out of `Needs a fix` — written up because the broad gate will hit it |

## Paste-ready fixes

Finding 1 — move the creation question above the two `choose` rows. Delete the
block that currently sits between row 2 and row 3 of the switch ladder
(`hooks/worktree-guard.py:2045`–`:2068`) and put this immediately before the
`# 1-b) 살아 있으나 입력이 끊긴 세션뿐` comment:

```python
    # A creation later in the same command has not been judged yet, and this is
    # where it gets its verdict. The ACTIVE row above keeps its precedence
    # because it is a plain deny: it stops the creation along with the rest of
    # the command, and making the creation outrank it would turn that deny into
    # an `ask` about the creation while the branch is still taken out from
    # under the other session, one approval later.
    #
    # Every row BELOW yields, and the reason is one property they share rather
    # than three separate ones: each of them ends in an `ask` whose approval
    # runs the WHOLE command line, creation included, while its own text asks
    # about something else. Rows 1-b and 2 are `choose` sites, and `choose`
    # denies ONCE per session per direction and asks on every attempt after --
    # executed, `git switch feature/x && git worktree add ../wt f` under only
    # idle sessions answered `deny` then `ask`, and the `ask` reads "Approve --
    # switch branches in this shared tree" while creating the worktree and
    # minting session-wide consent. Row 3 asks about uncommitted changes riding
    # along and its own text says the switch is ALLOWED. Row 4 says nothing at
    # all. Reading "these three deny" off the row above was the mistake: only
    # one of them does.
    #
    # The creation's own repository, not this switch's: they are not always the
    # same tree, and `guard_worktree_creation` refuses an empty one.
    if creation_at:
        judge_creation(command, cwd, repo_paths(creation_at)[0], session_id)

```

Finding 1's case, to plant in `tests/test_the_guard_asks_once_per_session.py`
beside `test_a_dirty_tree_does_not_decide_whether_the_creation_is_questioned`.
Seen red against the shipped guard: attempt 2 answers `ask` in both states.

```python
def test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned(
    monkeypatch, capsys, repo
):  # NAME NOT IN TREE — proposed here, not cited
    """`choose` denies ONCE per session per direction and asks on every attempt
    after, so "the three rows above the creation all deny" is true of one of
    them. On the second attempt the person is asked *Approve -- switch branches
    in this shared tree*, approving runs the whole command line, and the
    worktree is created with session-wide consent minted. Executed before this
    case: `deny` then `ask` under only-idle sessions and again under unusable
    detection, with the creation question put on neither."""
    for name, sessions in (("idle", ([], IDLE, True)), ("blind", ([], [], False))):
        for _ in range(2):
            decision, reason = decide(
                monkeypatch,
                capsys,
                repo,
                "git switch feature/x && git worktree add ../wt f",
                sessions=sessions,
                session_id=name,
            )
        assert decision == "deny", (name, decision)
        assert "Attempting to create a worktree" in reason, (name, reason)
```

Finding 2 — ask for `git`, not for a filename. At
`hooks/worktree-guard.py:436`, replace the one line and extend the docstring
paragraph that states the first test:

```python
        # `git` itself, not a path whose last component is spelled that way.
        # `os.path.basename` was the whole test, and executed with a consent
        # record present `./git worktree add ../wt f`,
        # `/tmp/evil/git worktree add ../wt f`, `../git …` and `bin/git …` all
        # answered `allow` -- which covers the tool call, so a session that had
        # one creation approved could run any executable at all by naming it
        # `git`. The docstring's own reason for this test is that a user's
        # `permissions.deny` must not be spoken over by a hook that was
        # reasoning about worktrees, and that reason does not stop at `sudo`.
        # What it costs is one prompt on `/usr/bin/git worktree add …`, which
        # is the trade `pr-notes.md` §3 already made for `$` and `>`.
        if tokens[0] != "git":
            return False
```

Finding 2's case, to plant beside
`test_a_wrapper_in_front_of_the_creation_carries_no_allow`. Seen red against the
shipped guard: all four answer `allow`.

```python
def test_a_path_qualified_git_carries_no_allow(monkeypatch, capsys, repo):  # NAME NOT IN TREE — proposed here, not cited
    """`allow` covers the whole tool call, so vouching for a filename rather
    than for `git` hands the model an executable of its own choosing. Executed
    with a record present, all four of these answered `allow` before this
    case."""
    grant(repo)
    for command in (
        "./git worktree add ../wt f",
        "/tmp/evil/git worktree add ../wt f",
        "../git worktree add ../wt f",
        "bin/git worktree add ../wt f",
    ):
        assert decide(monkeypatch, capsys, repo, command)[0] == "ask", command
    # ...and ordinary git is untouched.
    assert wg.only_creates_a_worktree("git -C /elsewhere worktree add ../wt f", str(repo))
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../a -b feature/x origin/main")[0]
        == "allow"
    )
```

Finding 13 — the `Worktree` row of
`seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-report.md:8`:

```
| Worktree | `/Users/x/orca/workspaces/SpecSeal/main-worktrees/wi-237` |
```

Finding 8 — either drop the figure or say what it ranges over. The sentence at
`docs/worktree-guard-spec.md:176` and
`seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:77`:

```
Measured after the change over every combination of the command shapes below,
four tree states and two shell directories: no command the writer would record
for leaves the guard silent.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `test_the_guard_asks_once_per_session.py`, `test_worktree_guard.py`, `test_worktree_guard_signals.py`, `test_guard_resolves_the_tree_it_judges.py`, `test_dispatch.py` at `62b2d2e` | **166 passed, 1 skipped** in 7.30s |
| `git switch feature/x && git worktree add ../wt f` twice in one session, only-idle and detection-unusable states | `deny` then **`ask`** in both; the creation question put on neither attempt; `worktree_consent.creation_directory` resolves a repository for the command — finding 1 |
| The `ask` text at that second attempt, printed in full | *Approve — switch branches in this shared tree*; no mention of a worktree being created |
| `git worktree add ../wt f` alone, same two states, same session | `deny` in both, **with** the creation question put — finding 1's control |
| Sweep with one session id per (state, directory) so the `choose` budgets are spent: 18 commands × 4 states × 2 directories × 2 attempts | **288 pairs · 0 silent · 64 where the writer records, the guard answers `ask`, and `judge_creation` never ran** — all in the idle and detection-unusable states |
| The same 18 × 4 × 2 with a fresh session id per cell | **144 pairs · 64 silent · 0 holes** — finding 4 |
| `only_creates_a_worktree` and the guard's verdict for `./git`, `/tmp/evil/git`, `../git`, `bin/git` and `sudo git worktree add ../wt f`, record present | `allow` for the first four, `ask` for `sudo` — finding 2 |
| The shipped predicate against what `cmdline.understood` and an `Unresolved` in `wheres` would have answered, over 18 shapes | no shape where the removed checks refuse and the shipped one allows; four where the shipped one is stronger — finding 6 |
| Mutation: the reviewer's round-1 alternative (`if reason is None or found == "worktree-add"`), module run, bytes restored | **1 failed, 32 passed** — `test_the_switch_ladder_keeps_every_verdict_it_had`, ACTIVE row, `assert 'ask' == 'deny'`; `restored: True` — finding 3 |
| `judge_creation` on `git switch feature/x && git worktree add ../wt f` under an ACTIVE session, no record | `ask` — the verdict the alternative would substitute for the deny |
| Six `git worktree add ../wt f` calls in one session, clean single-stream tree, record written after the first | **deny, allow, allow, allow, allow, allow** — finding 7 |
| The five residual shapes in that same session | compound `ask`, `cd` prefix `ask`, `"$HOME/wt"` `ask`, `> /tmp/x` `ask`, `sudo` `ask`, plain repeat `allow` |
| The five invariants, no record: creation on a clean single-stream tree · creation under ACTIVE · creation with detection unusable · plain switch clean · plain switch under ACTIVE | `deny` · `ask` · `deny` · silent · `deny` — finding 10 |
| Dirty tree, `git switch feature/x && git worktree add ../wt f` | `deny`, creation question put — finding 5 |
| Mutation: fix 1 applied · fix 2 applied · both, each with the four guard modules and the probes re-run, bytes restored | all three **green**; with fix 1 the creation question is put at both attempts in both states, with fix 2 the four path-qualified shapes fall to `ask`; `restored: True` |
| Empty-segment shapes (`; git worktree add …`, `&& git worktree add …`, a leading blank line, `&&  &&`) through the new walk | `deny` for all four, nothing raised |
| `bin/evidence-check --strict .` at `62b2d2e` | `total: 805 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0 |
| `git merge-base --is-ancestor 00e63c3 origin/release/v0.9.1` | exit 0 — finding 12 |
| `bin/test tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py -q` at `62b2d2e`, this report present | **1 failed, 20 passed** — `test_only_fixture_user_paths`, naming `rounds/round-1-report.md:8` and nothing else — finding 13 |
| `bin/test tests/test_a_record_states_what_the_tree_has.py -q` with this report present | **58 passed** — every backticked name here is one the tree carries, or carries the marker |

Probes were three `test_tmp_*` files and two mutation scripts in the scratch
directory. All three test files are deleted, every mutation restored the guard
from bytes saved before the swap and printed `restored: True`,
`tests/__pycache__` was cleared between mutations, and `git status --short` is
empty apart from this report.

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1, finding 1 | `hooks/worktree-guard.py:342` → now `:436` and the `ELSEWHERE` constant above it | the bound the `allow` rests on; finding 2 is the part of it still open |
| round 1, finding 2 | `hooks/worktree-guard.py:1684` → now the walk at `:1832` and `judge_creation` at `:1658` | where the guard's reading and the writer's reading parted; finding 1 is the remainder |
| round 1, finding 3 | `hooks/cmdline.py:1801` (`parse_git` reads past `WRAPPERS` and `VAR=val`) | the reason the command-word test exists at all, and the reason finding 2 is in its class |
| round 1, findings 4 and 5 | `overview.md` §*Not verified* · `pr-notes.md` §4 | both still deferred to the repository owner; finding 2's severity rides on the first of them |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `permissions.deny` rule outranks a hook `allow` — carried from round 1, and finding 2 widens what rides on it again | `overview.md` §*Not verified* | the repository owner |
| Whether a hook `ask` still stops a session run with permissions bypassed — carried from round 1 | `overview.md` §*Not verified* · `pr-notes.md` §4 | the repository owner |
| The full suite, the repository-wide lint and the typecheck | not run — `agent-contract` §2 | the orchestrator's broad gate, once, after the rounds settle |

## What this round could not settle

| Item | Who must answer |
|---|---|
| Whether `permissionDecision: "allow"` from a hook actually bypasses a user's `permissions.deny`. Finding 2's severity is bounded if it does not and unbounded if it does; the finding stands either way, because the docstring's bound is wrong either way | the repository owner, against the harness |
| Behaviour on Linux and Windows. Nothing this round ran reads a process, but `os.path.basename` and the path comparison in finding 2's fix behave differently on Windows separators | CI's Linux and Windows legs on the pull request |

## For the record

Contract changes: `only_creates_a_worktree(command, cwd, windows=None) -> bool`
keeps its signature and narrows the set of commands it answers True for — a
segment whose command word is not `git`, or any token carrying `$`, a backtick,
`<` or `>`, is now False → `judge_creation`, its one caller in
`hooks/worktree-guard.py`, and the cases in
`tests/test_the_guard_asks_once_per_session.py`. `main`'s walk keeps `reason` on
the first segment that classifies and adds `creation_at`; no unit's signature or
returns moved.

New units: `ELSEWHERE` (depth 1); `judge_creation` (depth 1);
`test_the_allow_refuses_a_segment_that_does_anything_else` (depth 1);
`test_a_wrapper_in_front_of_the_creation_carries_no_allow` (depth 1);
`test_a_backgrounded_creation_is_still_only_a_creation` (depth 1);
`test_a_creation_behind_another_verdict_is_still_judged` (depth 1);
`test_the_switch_ladder_keeps_every_verdict_it_had` (depth 1);
`test_a_dirty_tree_does_not_decide_whether_the_creation_is_questioned` (depth 1);
`test_the_guard_is_never_silent_where_the_writer_records` (depth 1)

Needs a fix: yes — 1 and 2
Loses a record or crashes: no

## Proof

Files opened at `62b2d2e` in
`/Users/x/orca/workspaces/SpecSeal/main-worktrees/wi-237`:

- `hooks/worktree-guard.py`
- `hooks/worktree_consent.py`
- `hooks/cmdline.py`
- `tests/test_the_guard_asks_once_per_session.py`
- `tests/conftest.py`
- `bin/test`
- `docs/worktree-guard-spec.md`
- `seal/config.md`
- `seal/follow-up.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/pr-notes.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/changelog.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-asked.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-fixes.md`
- `/Users/x/.claude/skills/writing-style/SKILL.md`

Diffs read: `git diff d82a02c 3cf979b -- hooks/worktree-guard.py`,
`git diff d82a02c 3cf979b -- tests/ hooks/`,
`git diff origin/release/v0.9.1...HEAD`, `git diff --stat d82a02c..62b2d2e`.
