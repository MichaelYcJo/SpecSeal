# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — review round 2

| Field | Value |
|---|---|
| Target SHA | 62b2d2e |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | choose → guard_worktree_creation, main |
| New units | test_a_path_qualified_git_carries_no_allow (depth 1); test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned (depth 1) |
| Needs a fix | yes — 1 and 2 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of `1788817291-the-guard-asks-once-per-worktree-not-once-per-session` (ticket #237), at target `62b2d2e`, base `origin/release/v0.9.1`. The verifying round over round 1's fixes, whose substance is `86c4ddb`, `20553cb`, `a9e76c2` and `3cf979b`.

Round 1's verdicts were inherited. It had opened two 🔴 against a change that weakens a guard: the bounded allow was not bounded, with a command substitution, backticks, a redirection, a subshell, a heredoc and `sudo`/`env` prefixes all answering `allow` while `allow` covers the whole tool call and bypasses the user's permission settings for it; and the consent record could be minted by a creation the guard never judged, since `git switch feature/x && git worktree add …` went silent and wrote the record, falsifying the *not forgeable by the model* row the design rests on.

Three things the fix pass did beyond what it was handed were named as targets. It refused round 1's paste-ready fix for finding 2, on the grounds that letting a creation beat an earlier verdict turns a `switch` denied while another session is ACTIVE into an `ask` about creation, after which one approval takes that session's branch — the claim being that `test_the_switch_ladder_keeps_every_verdict_it_had` goes red under the alternative, to be verified rather than read. Its re-enumeration found three more escapes, one worse than either 🔴: with the fallthrough at the end of the switch ladder, a dirty tree decided whether the creation question was put at all. And it removed the report's `understood` and `Unresolved` checks on the grounds that the command-word check strictly dominates, a domination claim to be tested for a counterexample rather than accepted.

Also named: the claim that no path can still mint a record, to be re-derived rather than accepted from the reported sweep; the prompt budget and its third residual, judged for whether it is honestly stated as the boundary catching up rather than widening; the five things that must not have changed; the two ❓ routed to the repository owner, checked for an answerer and for what the guard does if the answer is unfavourable; the finding sent outside the work item about `evidence-check` dropping an unreadable ledger row; and that any `# RIDER:` planted must not name a commit of this branch, #239 being the ticket for exactly that.

The bound was stated: round 1 met the floor, a round that opens nothing needing a fix does not consume the cap, and neither manufacturing nor softening a finding was acceptable.

The report was to be written to a file, finding ids bare integers, every verdict row carrying one, no finding carrying two rows, no real user path, and `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 Two of the three switch-ladder rows kept above the creation do not deny — `choose` denies once per session and asks after — so on the second attempt a person is asked about the switch, approving creates the worktree, and session-wide consent is minted with the creation question never put | `hooks/worktree-guard.py:2049` · `:1368` · `docs/worktree-guard-spec.md:168` | **fixed** `bba7dab` | fixed at bba7dab — `` — `choose` takes a `before_ask` its fallback yields to, and the switch ladder's two choice rows pass it the creation's own judgment. The deny branch is untouched, so every switch verdict is where it was; only the `ask` that would have run the command line yields. Seen red first: idle → `deny` then `ask`, detection-unusable → `deny` then `ask`, the creation question put at neither, and the `ask` reading *Approve — switch branches in this shared tree*. Mutation, `before_ask=` deleted at both sites: `test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned` and `test_the_guard_is_never_silent_where_the_writer_records` both go red, source restored from bytes saved first; **Executed.** Same command twice in one session: idle → `deny`, then `ask`; detection unusable → `deny`, then `ask`; the creation question put on neither. The bare creation at the same state denies WITH it put. 288-pair sweep with the `choose` budgets spent: 64 pairs where the writer records, the guard answers `ask`, and `judge_creation` never ran. The fix below is executed and leaves the four guard modules green |
| 2 | 🟡 `os.path.basename(tokens[0]) != "git"` is the whole command-word test, so any executable whose filename is `git` collects the `allow` that covers the tool call | `hooks/worktree-guard.py:436` · `:401` | **fixed** `bba7dab` | fixed at bba7dab — `` — `os.path.basename(tokens[0]) != "git"` becomes `tokens[0] != "git"`. The boundary the line implements is *a command word carrying no separator, so the shell resolves it on `PATH`*; anything with a `/` names a file this hook cannot identify. Re-enumerated by construction over 32 command-word shapes: exactly five pass, and all five are the word `git` after lexing (`git`, `\git`, `'git'`, `"git"`, `g"i"t`). Seen red first: `./git`, `../git`, `bin/git`, `/tmp/evil/git`, `~/git` and `*/git` all answered `allow` with a record present. Mutation, the basename restored: `test_a_path_qualified_git_carries_no_allow` goes red, source restored from bytes saved first; **Executed** with a record present: `./git`, `/tmp/evil/git`, `../git` and `bin/git worktree add ../wt f` all answer `allow`, `sudo git …` answers `ask`. The docstring's own reason for the test — a user's `permissions.deny` must not be spoken over — does not stop at `sudo`. Present at `d82a02c` too, so it is the unenumerated part of round 1's finding 3 class, in a line the fix wrote. Fix executed: the four fall to `ask`, `git -C <repo> worktree add …` and `-b <branch> <start>` still allow, modules green |
| 3 | 🟢 The refusal of round 1's paste-ready fix for finding 2 | `hooks/worktree-guard.py:1655` · `tests/test_the_guard_asks_once_per_session.py:408` | answered | **Executed** as a mutation, source restored from bytes saved first (`restored: True`): the alternative turns `test_the_switch_ladder_keeps_every_verdict_it_had` red on the ACTIVE row, `assert 'ask' == 'deny'`, 1 failed 32 passed. `judge_creation` under an ACTIVE session with no record answers `ask`, which is the protection the refusal names |
| 4 | 🟢 The shape shipped instead judges a creation wherever it sits, at both silent exits | `hooks/worktree-guard.py:1884` · `:2067` | answered | **Executed.** 18 commands × 4 tree states × 2 shell directories, fresh session id per cell: 144 pairs, 64 silent, **0** where the writer records and the guard is silent. Round 1's three shapes and the fix pass's `if not top` shape are in the enumeration |
| 5 | 🟢 The dirty-tree escape is closed and the new ordering moves no other verdict | `hooks/worktree-guard.py:2067` · `tests/test_the_guard_asks_once_per_session.py:434` | answered | **Executed.** Dirty tree, `git switch feature/x && git worktree add ../wt f` → `deny` with the creation question put. Five guard modules at `62b2d2e`: **166 passed, 1 skipped** |
| 6 | 🟢 The command-word test strictly dominates the removed `cmdline.understood` and `Unresolved` checks | `hooks/worktree-guard.py:401` · `hooks/cmdline.py:1282` | answered | **Executed** over 18 shapes: no shape where the removed checks refuse and the shipped one allows; four where the shipped one is stronger (`time`, `sudo`, `!`, `cd &&`). **Read**: every input `understood` refuses puts something other than `git` in `tokens[0]` or a character `ELSEWHERE` refuses |
| 7 | 🟢 The prompt budget is unchanged and the third residual is honestly stated | `pr-notes.md` §3 | answered | **Executed.** Six creations in one session, clean single-stream: deny, allow, allow, allow, allow, allow. Compound, `cd` prefix, expansion, redirection and wrapper each `ask`; a plain repeat still `allow`. §3's framing is right — the eleven shapes were allowed while the docstring already claimed they were not. Its still-allowed list omits finding 2's shape |
| 8 | ⬜ The `576 command/tree-state/directory combinations` in two documents cannot be reconstructed — the three axes stated give 144 | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:77` · `docs/worktree-guard-spec.md:176` | **fixed** `f4db784` | fixed at f4db784 — `` — the figure does not reconstruct and the axes were the weaker property, so both were replaced. `docs/worktree-guard-spec.md`, `spec.md` and the ledger row now carry 21 command shapes × 5 tree states × 2 shell directories × 2 record states × 3 attempts = **1260 combinations**, of which 230 are cells `worktree_consent.creation_directory` resolves a repository for, and **0** reach a verdict that lets the command run without the creation question. With both fixes reverted the same sweep finds **64**; **Executed**: the property holds at 144 and again at 288, so nothing about the guard is in question. `agent-contract` §5 — a count can be checked while the claim it stands for cannot. Paperwork; not counted in `Needs a fix` |
| 9 | 🟢 Both `❓` carry an answerer, and `pr-notes.md` says what the guard does if the answer is unfavourable | `overview.md` §*Not verified* · `pr-notes.md` §4 | answered | **Read.** Both rows name the repository owner. §4 states the auto-answered `ask` in the present tense with `--dangerously-skip-permissions` named, and gives the fallback for `permissions.deny`: the consented row answers `ask` rather than `allow`, one word at one site |
| 10 | 🟢 A session with no consent record still asks, the single-stream site still denies and steers to `git switch`, and no path creates a worktree silently without prior approval | `hooks/worktree-guard.py:1655` | answered | **Executed.** Creation with no record: `deny` on a clean single-stream tree with the `git switch` steer, `ask` under an ACTIVE session, `deny` at the first detection-unusable attempt. Plain switch unchanged in both directions. 432 pairs across the two sweeps, 0 silent where the writer would record |
| 11 | 🟢 The `evidence-check` finding was recorded outside this work item with an answerer | `seal/follow-up.md` | answered | **Read.** A schedulable row naming the repository owner, carrying the executed evidence and the judgment it needs |
| 12 | 🟢 No `# RIDER:` this branch plants names a commit of this branch | `hooks/worktree-guard.py:1760` | answered | **Executed.** The branch's diff against `origin/release/v0.9.1` adds no rider and no stamp. `git merge-base --is-ancestor 00e63c3 origin/release/v0.9.1` exits 0, so the newest stamp in the tree sits on the release branch |
| 13 | ⬜ Round 1's report states the machine's own absolute path in its `Worktree` field, which turns `tests/test_no_real_identifiers.py::test_only_fixture_user_paths` red | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-report.md:8` | **fixed** `f4db784` | fixed at f4db784 — `` — `rounds/round-1-report.md`'s `Worktree` field carried this machine's own absolute path; it is `/Users/x/…` now, the shape `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* names. Seen red first: `bin/test tests/test_no_real_identifiers.py -q` failed on that line and nothing else; green after; **Executed** at `62b2d2e`: that case fails, naming this line, and it is the only real user path anywhere under `seal/`. Committed at `86c4ddb`, so it is this branch's; the base carries none. `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* is the rule. Under `seal/specs/`, so it is a correction and out of `Needs a fix` — written up because the broad gate will hit it |

## Paste-ready fixes

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
```
| Worktree | `/Users/x/orca/workspaces/SpecSeal/main-worktrees/wi-237` |
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:342` · `:1746` | round 1's 1 — fixed |
| round-1 | `hooks/worktree-guard.py:1684` · `hooks/worktree_consent.py:138` | round 1's 2 — fixed |
| round-1 | `hooks/worktree-guard.py:342` · `hooks/cmdline.py:37` | round 1's 3 — fixed |
| round-1 | `hooks/worktree-guard.py:1746` | round 1's 4 — deferred |
| round-1 | `pr-notes.md` §4 · `overview.md` §*Not verified* | round 1's 5 — deferred |
| round-1 | `seal/ledger.md:269` · `:337` · `:379` | round 1's 6 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `permissions.deny` rule outranks a hook `allow` — carried from round 1, and finding 2 widens what rides on it again | `overview.md` §*Not verified* | the repository owner |
| Whether a hook `ask` still stops a session run with permissions bypassed — carried from round 1 | `overview.md` §*Not verified* · `pr-notes.md` §4 | the repository owner |
| The full suite, the repository-wide lint and the typecheck | not run — `agent-contract` §2 | the orchestrator's broad gate, once, after the rounds settle |
