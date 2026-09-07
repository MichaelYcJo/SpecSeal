# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — review round 1

| Field | Value |
|---|---|
| Target SHA | d82a02c |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 1, 2, 3 |
| Loses a record or crashes | no |

- [ ] Pass

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
| 1 | 🔴 The bounded allow is not bounded. A command substitution, a backtick, an output redirection, a subshell and a heredoc all survive `only_creates_a_worktree`, so `permissionDecision: "allow"` covers whatever the shell runs beside the creation | `hooks/worktree-guard.py:342` · `:1746` | open | **Executed** at `d82a02c` with a consent record present: six shapes answer `allow`. Two were run in a real shell — `$( )` created its marker, `>` truncated a file holding `important`. The signals to refuse them already exist and are discarded: `cmdline.understood` (`hooks/cmdline.py:1282`) inspects the command word only, and `walk_command`'s `wheres`, which carry `Unresolved(CONSTRUCT)` for the subshell, are thrown away at `hooks/worktree-guard.py:368`. The fix below closes all six with the five existing guard modules green (164 passed, 1 skipped) |
| 2 | 🔴 A creation the guard never judged still mints session-wide consent. `main`'s walk stops at the first classified segment while the writer reads every segment, so a `git switch` written in front of a creation takes the verdict and the creation runs unjudged | `hooks/worktree-guard.py:1684` · `hooks/worktree_consent.py:138` | open | **Executed** at `d82a02c`, clean single-stream tree, no record: `git worktree add ../wt f` denies, `git status && git worktree add ../wt f` denies, and `git switch feature/x && git worktree add ../wt f` is **silent** — and the writer records for it. This falsifies `spec.md:59` (*runs only if the guard's `deny` did not fire and its `ask` was answered yes*) and the "Forgeable by the model: no" row that rests on it. The fix below turns that row into `deny` with the same five modules green |
| 3 | 🟡 A wrapper carries the allow. `parse_git` reads past `WRAPPERS` and leading `VAR=val`, so `sudo git worktree add …` and `env LD_PRELOAD=… git worktree add …` are vouched for as creation-and-nothing-else | `hooks/worktree-guard.py:342` · `hooks/cmdline.py:37` | open | **Executed**: both allow at `d82a02c`; both fall to `ask` with the one added line, and `git -C /other worktree add …` and `git worktree add ../a -b feature/x origin/main` still allow. `tests/test_worktree_guard.py` and `tests/test_the_guard_asks_once_per_session.py` stayed green (102 passed) |
| 4 | ❓ Whether a `permissions.deny` rule outranks a hook `allow`. If it does not, a user who explicitly denied `git worktree add` is overridden from their first approval onward | `hooks/worktree-guard.py:1746` | unverified | Not executable from this repository — a harness property. `overview.md`'s *Not verified* table already carries it with an answerer, which is the right shape; this round adds that findings 1 and 3 widen what the `allow` covers when it wins. **Answerer: the repository owner** |
| 5 | ❓ Whether `pr-notes.md` §4's auto-answered `ask` is hypothetical, and the `overview.md` row for it names no answerer — it closes with *the same standing every gate in this repository has*, which is a deferral to nobody | `pr-notes.md` §4 · `overview.md` §*Not verified* | unverified | Not executed, same harness property. `--dangerously-skip-permissions` exists today, so the sentence may be present tense. The two harness facts named in that row are the whole foundation of the change, which is the row that least tolerates an unnamed answerer (`agent-contract` §4). **Answerer: the repository owner** |
| 6 | ⬜ Three `seal/ledger.md` rows follow `dispatch.py#GROUPS` to its new hash while keeping `Checked` at `2026-09-02`, and `evidence-check --reverify` does not touch that column | `seal/ledger.md:269` · `:337` · `:379` | open | **Read.** `CLAUDE.md` says the column holds the date somebody read the code; the row directly above them writes its re-read into `Notes` and moves the date. Paperwork — not counted in `Needs a fix` |

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
