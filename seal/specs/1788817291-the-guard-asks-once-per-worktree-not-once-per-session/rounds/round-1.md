# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — review round 1

| Field | Value |
|---|---|
| Target SHA | d82a02c |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed under round 3 |
| Fixes checked by | round-2 |
| Contract changes | decide → decide, main, pytest |
| New units | ELSEWHERE (depth 1); judge_creation (depth 1); test_the_allow_refuses_a_segment_that_does_anything_else (depth 1); test_a_wrapper_in_front_of_the_creation_carries_no_allow (depth 1); test_a_backgrounded_creation_is_still_only_a_creation (depth 1); test_a_creation_behind_another_verdict_is_still_judged (depth 1); test_the_switch_ladder_keeps_every_verdict_it_had (depth 1); test_a_dirty_tree_does_not_decide_whether_the_creation_is_questioned (depth 1); test_the_guard_is_never_silent_where_the_writer_records (depth 1) |
| Needs a fix | yes — 1, 2, 3 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of `1788817291-the-guard-asks-once-per-worktree-not-once-per-session` (ticket #237), at target `d82a02c`, base `86e140f`. No prior rounds, and no pull request open — the orchestrator opens it after this round.

The branch weakens a guard, and the round was told to review it as such. `hooks/worktree-guard.py` answered worktree creation with `ask` at every site, and the `[worktree-ok]` site says in writing that this is not a choice: the token is written into the command by whoever issues it, so it is not evidence a person answered, and `has_token`'s docstring refuses a loose read for exactly that reason. The consequence was that no path through the guard cost zero prompts, and a run needing six worktrees paid six hard stops — measured on this release's own run on 2026-09-08. The branch's answer is that the harness only runs a `git worktree add` that was approved, so a `PostToolUse` observation of one that actually ran is consent the command text cannot forge; a new `hooks/worktree_consent.py` writes a per-session record and `PreToolUse` allows a later creation in that session. The invariant changes from *creating a worktree always takes one confirmation* to *the first creation of a session takes one*.

The named targets. Whether the record can be produced without a person — every way `PostToolUse` can fire for a `git worktree add`, including one that never ran because an earlier segment failed, one denied by a permission rule, one in a session with permissions bypassed, and a command the lexer misreads; any of those writing a record makes the consent forgeable after all and is a 🔴. The bounded allow, since `permissionDecision: "allow"` covers the whole tool call, tested against `&&`, `;`, `|`, a subshell, a heredoc, backgrounding, and a creation whose arguments contain a quoted `&&`. The `Agent` path going silent rather than allowing, and whether silence reads as allow to the harness. The four decisions made rather than brought back, with the last — that a FAILED `git worktree add` records consent — named as the one most likely to be wrong. The record's own failure modes: an unwritable `.git`, a read-only filesystem, a record path that is a directory, a session id with separators, a missing session id, a stale record from an exited session. The gate answers in `pr-notes.md` against `CONTRIBUTING.md` §*What a change to a gate must carry*, with the prompt budget verified by running the guard rather than reading it. And what must NOT have changed: a session with no consent record still asks, the single-stream site still denies, and any path that lets a session with no prior approval create a worktree silently is a 🔴.

The open question the build could not settle — whether a `permissions.deny` rule outranks a hook `allow` — was to be carried into the report with an answerer.

`tests/test_the_records_can_be_carried_out_and_in.py`'s four failures were named as not this branch's — #111's timezone defect, already fixed on the branch that merges first — and were not to be opened.

The report was to be written to a file, finding ids bare integers, every verdict row carrying one, and no finding carrying two rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The bounded allow is not bounded. A command substitution, a backtick, an output redirection, a subshell and a heredoc all survive `only_creates_a_worktree`, so `permissionDecision: "allow"` covers whatever the shell runs beside the creation | `hooks/worktree-guard.py:342` · `:1746` | **fixed** `86c4ddb` | fixed at 86c4ddb — `` — `only_creates_a_worktree` now asks two things of each SEGMENT rather than one thing of the compound: `git` is the segment's own command word, and no token carries `$`, a backtick, `<` or `>`. All eleven shapes fall to `ask`. Seen red first: `bin/test tests/test_tmp_round1_red.py` printed `allow` for every one of them, and the shell half printed `marker exists: True` and `victim holds: ''`; **Executed** at `d82a02c` with a consent record present: six shapes answer `allow`. Two were run in a real shell — `$( )` created its marker, `>` truncated a file holding `important`. The signals to refuse them already exist and are discarded: `cmdline.understood` (`hooks/cmdline.py:1282`) inspects the command word only, and `walk_command`'s `wheres`, which carry `Unresolved(CONSTRUCT)` for the subshell, are thrown away at `hooks/worktree-guard.py:368`. The fix below closes all six with the five existing guard modules green (164 passed, 1 skipped) |
| 2 | 🔴 A creation the guard never judged still mints session-wide consent. `main`'s walk stops at the first classified segment while the writer reads every segment, so a `git switch` written in front of a creation takes the verdict and the creation runs unjudged | `hooks/worktree-guard.py:1684` · `hooks/worktree_consent.py:138` | **fixed** `86c4ddb` | fixed at 86c4ddb — ``, placement corrected in `3cf979b` — the walk records where a creation ANYWHERE in the command acts, and it is judged between the switch ladder's halves: below the three concurrency rows, which all deny, and above the tracked-changes `ask` and the silent single-stream exit, neither of which protects a tree. The earlier `if not top` exit falls through too. The switch ladder keeps every verdict it had; the report's paste-ready fix, which makes the creation outrank the earlier verdict, turns a switch denied under an ACTIVE session into an `ask` and was refused for that. Seen red first: `git switch feature/x && git worktree add ../wt f`, `… ; …` and `git checkout feature/x && …` were all **silent** with the record written; **Executed** at `d82a02c`, clean single-stream tree, no record: `git worktree add ../wt f` denies, `git status && git worktree add ../wt f` denies, and `git switch feature/x && git worktree add ../wt f` is **silent** — and the writer records for it. This falsifies `spec.md:59` (*runs only if the guard's `deny` did not fire and its `ask` was answered yes*) and the "Forgeable by the model: no" row that rests on it. The fix below turns that row into `deny` with the same five modules green |
| 3 | 🟡 A wrapper carries the allow. `parse_git` reads past `WRAPPERS` and leading `VAR=val`, so `sudo git worktree add …` and `env LD_PRELOAD=… git worktree add …` are vouched for as creation-and-nothing-else | `hooks/worktree-guard.py:342` · `hooks/cmdline.py:37` | **fixed** `86c4ddb` | fixed at 86c4ddb — `` — the command-word test is the same line as finding 1's first. `sudo`, `env VAR=…`, a bare `VAR=…` and `command git …` all answer `ask`; `git -C <repo> worktree add`, `-b <branch> <start>`, a `~` path and a glob path still allow. Seen red first: all four answered `allow`; **Executed**: both allow at `d82a02c`; both fall to `ask` with the one added line, and `git -C /other worktree add …` and `git worktree add ../a -b feature/x origin/main` still allow. `tests/test_worktree_guard.py` and `tests/test_the_guard_asks_once_per_session.py` stayed green (102 passed) |
| 4 | ❓ Whether a `permissions.deny` rule outranks a hook `allow`. If it does not, a user who explicitly denied `git worktree add` is overridden from their first approval onward | `hooks/worktree-guard.py:1746` | deferred seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md | seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md |
| 5 | ❓ Whether `pr-notes.md` §4's auto-answered `ask` is hypothetical, and the `overview.md` row for it names no answerer — it closes with *the same standing every gate in this repository has*, which is a deferral to nobody | `pr-notes.md` §4 · `overview.md` §*Not verified* | deferred seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md | seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md |
| 6 | ⬜ Three `seal/ledger.md` rows follow `dispatch.py#GROUPS` to its new hash while keeping `Checked` at `2026-09-02`, and `evidence-check --reverify` does not touch that column | `seal/ledger.md:269` · `:337` · `:379` | **fixed** `20553cb` | fixed at 20553cb — `` — the three `seal/ledger.md` rows at `:269`, `:337` and `:379` were re-read at `dispatch.py#GROUPS` and their `Checked` moved to `2026-09-08`, each with the re-read written into `Notes` in the shape the row above them uses. The branch's edit added `worktree_consent.py` to `post-bash` and a `post-agent` group beside it, and touches no group those three rows claim about, so all three claims hold; **Read.** `CLAUDE.md` says the column holds the date somebody read the code; the row directly above them writes its re-read into `Notes` and moves the date. Paperwork — not counted in `Needs a fix` |

## Paste-ready fixes

```python
# The characters that make a segment do something besides run its command
# word: a substitution the shell expands before git is invoked, and a
# redirection that writes a file the allow was never about. `understood`
# asks about the command WORD, which is the right question for "where does
# the shell land" and the wrong one for "does this do anything else" --
# executed, `git worktree add ../wt f $(touch <marker>)` created the marker
# and `git worktree add ../wt f > <file>` truncated the file, both under an
# `allow` that covered the whole tool call.
ELSEWHERE = "$`<>"


def only_creates_a_worktree(command: str, cwd: str, windows=None) -> bool:
    ...
    if not parses_cleanly(command, windows):
        return False
    seen = False
    for tokens, wheres in walk_command(command, cwd, windows):
        if not tokens:
            continue
        if not cmdline.adds_a_worktree(tokens):
            return False
        # `parse_git` reads past WRAPPERS and leading VAR=val on purpose --
        # the question it answers is "is this a git invocation". This one is
        # "is this nothing but a creation", and `sudo git worktree add` and
        # `env LD_PRELOAD=… git worktree add` are not.
        if os.path.basename(tokens[0]) != "git":
            return False
        # The reader's own refusals, honoured at the one site where being
        # wrong costs more than a prompt: a subshell, an `eval`, a command
        # word this process cannot read before expansion.
        if not cmdline.understood(tokens) or any(
            isinstance(where, cmdline.Unresolved) for where in wheres
        ):
            return False
        if any(ch in tok for tok in tokens for ch in ELSEWHERE):
            return False
        seen = True
    return seen
```
```python
    reason = None
    eff_cwd = cwd
    # A creation ANYWHERE in the command outranks an earlier verdict. This
    # walk used to stop at the first segment it could classify, so
    # `git switch feature/x && git worktree add ../wt f` was judged as a
    # switch: the creation ladder never ran, the shell created the worktree,
    # and hooks/worktree_consent.py -- which reads every segment -- then
    # recorded consent for a creation nobody was asked about. The two
    # readings have to agree, and the writer's is the correct one.
    for tokens, wheres in walk_command(command, cwd):
        for where in wheres:
            here, target = judgeable(tokens, where, cwd)
            found = classify(tokens, here)
            if not found:
                continue
            if reason is None or found == "worktree-add":
                reason, eff_cwd = found, target
            break
        if reason == "worktree-add":
            break
    if not reason:
        sys.exit(0)
```
```
| … | `hooks/dispatch.py#GROUPS@a5e67d2c`, … | … | 2026-09-08 | … **Re-read 2026-09-08 for #237**, which added `worktree_consent.py` to `post-bash` and a `post-agent` group beside it; neither touches what this row claims, so the claim holds |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_guard_asks_once_per_session.py -q` at `d82a02c` | **26 passed** in 4.62s |
| `bin/test` on `test_worktree_guard.py`, `test_worktree_guard_signals.py`, `test_guard_resolves_the_tree_it_judges.py`, `test_dispatch.py` at `d82a02c` | **133 passed, 1 skipped** |
| `only_creates_a_worktree` over 13 command shapes, and the guard's decision for each with a consent record present | `allow` for `$( )`, backticks, `> file`, a subshell, a heredoc, `sudo` and a trailing `&`; `ask` for a pipe, `2>&1`, `;` and an `eval` prefix — finding 1 |
| `bash -c 'git worktree add /nonexistent/x $(touch <marker>)'` and the same with `> <file>` | the marker exists; the file that held `'important'` holds `''` — the allow covers real side effects |
| The guard's verdict on `git switch feature/x && git worktree add ../wt f`, clean single-stream tree, no record | **silent**; `git status && git worktree add …` denies at the same tree state — finding 2 |
| `worktree_consent.py` on that same command | record written — finding 2's second half |
| `worktree_consent.py` over 10 shapes that mention a creation without running one (quoted, heredoc body, `python3 -c`, broken lexer, `git worktree list`) | no record for any of them; the writer fails toward the prompt |
| `worktree_consent.py` on `Agent` payloads with `isolation` `worktree` / `WORKTREE` / `remote` / absent | records for the first two only |
| Mutation re-run on a copy of `hooks/`: `granted` using `os.path.exists` | a directory at the record path answers `True` — `test_a_directory_at_the_record_path_is_not_a_record` has teeth |
| Mutation: `consent_path` without the `(".", "..")` guard | `.` and `..` both resolve to a path inside the consent directory — the case has teeth |
| Mutation: `record` re-raising instead of returning `False` | the hook exits **1** with `FileExistsError` on stderr — the case has teeth |
| Both paste-ready fixes applied, then `bin/test` on the five guard modules plus the probe | **164 passed, 1 skipped**; every shape in finding 1 falls to `ask` and finding 2's row becomes `deny` |
| Wrapper half of the fix applied, then `bin/test tests/test_worktree_guard.py tests/test_the_guard_asks_once_per_session.py` | **102 passed**; `sudo`, `env VAR=…` and `VAR=… git` fall to `ask`, `git -C /other worktree add` and `-b feature/x origin/main` still allow |
| `bin/evidence-check --strict .` | `771 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 4 — a `permissions.deny` rule against a hook `allow` | already in `overview.md` §*Not verified*, with an answerer | the repository owner |
| 5 — whether a hook `ask` still stops a session run with permissions bypassed | `overview.md` §*Not verified*, whose row needs the answerer written into it | the repository owner |
