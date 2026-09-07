# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — review round 1 report

| Field | Value |
|---|---|
| Target SHA | `d82a02c` |
| Base | `86e140f` |
| Branch | `fix/237-the-guard-asks-once-per-worktree-not-once-per-session` |
| Worktree | `/Users/michael/orca/workspaces/SpecSeal/main-worktrees/wi-237` |
| PR | not yet |
| Broad gate | not yet — the full suite, the repository-wide lint and the typecheck are the orchestrator's, once, after the rounds settle (`agent-contract` §2) |

## What this round was asked

Review a change that **weakens a guard**, as such. The branch replaces *creating
a worktree always takes one confirmation* with *the first creation of a session
takes one*, and rests that on one claim: a `PostToolUse` observation of a
`git worktree add` that actually ran is consent the command text cannot forge.

The prompt named the attack surface and this round worked it: whether the record
can be produced without a person, whether the bounded `allow` is bounded,
whether the `Agent` path's silence is the same thing as an allow, the four
decisions `questions.md` records, the failure modes of the record itself, the
gate answers `CONTRIBUTING.md` requires, and what must not have changed.

`tests/test_the_records_can_be_carried_out_and_in.py` was left alone, as
instructed.

## The shape of what was found

The design is sound and the record itself is well built. Both defects are in the
**perimeter around it** rather than in the record, and they are the same
sentence read two ways.

```
The claim:  a creation reaches PostToolUse only after the guard's deny
            did not fire and its ask was answered yes
                    │
      ┌─────────────┴─────────────┐
      │                           │
  ① the guard does not always     ② the "ask" the guard skips is
    put the creation question       replaced by an "allow" that covers
    (finding 2)                     more than a creation (finding 1)
```

Finding 2 mints consent without the creation question ever being put. Finding 1
spends that consent on commands that do more than create a worktree. Either one
alone is a hole; together they are a path from *the model writes one compound
command* to *every Bash call shaped like a creation bypasses the permission
system for the rest of the session*.

---

### 1 🔴 The bounded allow is not bounded — six command shapes run other things and are allowed anyway

`hooks/worktree-guard.py:342` says in its own docstring that
`permissionDecision: "allow"` bypasses the user's permission settings for the
**whole** tool call, and that the guard therefore speaks only for *worktree
creation and nothing else*. The predicate does not enforce that. It splits the
command into segments and asks each one whether it is a `git worktree add`; it
never asks what else is inside a segment.

A shell runs a great deal inside one segment. Executed against the branch at
`d82a02c`, with a consent record present, these are the decisions today:

| Command | Decision today | What the shell also runs |
|---|---|---|
| `git worktree add ../wt f $(touch /tmp/pwned)` | **allow** | the substitution body, before git is invoked |
| ``git worktree add ../wt f `touch /tmp/pwned` `` | **allow** | the same, in the older spelling |
| `git worktree add ../wt f > /tmp/clobber` | **allow** | truncates `/tmp/clobber` |
| `(git worktree add ../wt f)` | **allow** | a subshell `cmdline.understood` already refuses to read |
| `git worktree add ../wt f <<EOF …` | **allow** | a heredoc the judgment read discarded |
| `sudo git worktree add ../wt f` · `env LD_PRELOAD=… git worktree add …` | **allow** | `parse_git` reads past `WRAPPERS` and leading `VAR=val` |

Two of those were run in a real shell to confirm the shell does what the table
says: `$( )` created its marker file, and `>` left a file that held `important`
holding `''`.

**Why the reader cannot see this today.** `cmdline.understood` at
`hooks/cmdline.py:1282` is the module's own answer to *could I read this
segment*, and it inspects the **command word** only — the right question for
*where does the shell land*, the wrong one for *does this command do anything
else*. `only_creates_a_worktree` also throws away `walk_command`'s `wheres`,
which is where the existing `Unresolved(CONSTRUCT)` signal for a subshell
arrives. So two signals the codebase already computes are discarded at the one
site that most needs them.

The predicate is the newest unit on the branch and the fix belongs to it, not to
`cmdline.py`: `understood` is correct for its own question.

**What the account asserted.** `plan.md`'s alternatives table rejects *`allow`
for any command containing a creation* on the grounds that *the allow is bounded
to a command that is worktree creation and nothing else*, and `phase-3.md` says
*a command the lexer gave up on is not vouched for*. Both are the right rule.
What the code implements is narrower than the rule: it vouches for a command the
lexer read and the reader did not understand.

Related, and closed by the same fix: `seal/ledger/1788817291-….md:8` records
*The allow covers only a command that is worktree creation and nothing else* as
**Executed**, and `docs/worktree-guard-spec.md` and `spec.md` state it as a
property. The three shapes the cases cover — a compound, a `cd`-prefixed
creation, an unbalanced quote — are the three that do fall to `ask`, and the six
above were never asked.

### 2 🔴 …and the record can be minted by a creation the guard was never given the chance to judge

`main`'s walk at `hooks/worktree-guard.py:1684` stops at the **first** segment it
can classify. `hooks/worktree_consent.py:138` reads **every** segment, on purpose
— its docstring says a creation anywhere in a command that ran is a creation that
was approved. Those two readings disagree, and the gap between them is writable
by whoever composes the command.

Executed at `d82a02c`, in a clean single-stream tree with no consent record:

| Command | Guard's PreToolUse verdict | Record written afterwards |
|---|---|---|
| `git worktree add ../wt f` | **deny**, steered to `git switch` | — |
| `git status && git worktree add ../wt f` | **deny** | — |
| `git switch feature/x && git worktree add ../wt f` | **silent** | **yes** |

The third row is the whole finding. `classify` reaches `switch` first, the
branch-switch ladder allows a plain switch in a clean single-stream tree by
saying nothing, and the creation ladder never runs. The shell then creates the
worktree, `PostToolUse` observes it, and the session holds a consent record from
that point on.

**Why this matters more than the pre-existing hole it grows out of.** The
first-verdict-wins walk predates this branch, and so does the escape it gives a
compound. What is new is that the escape now **mints session-wide consent**. The
spec's central premise at `spec.md:59` — *a `git worktree add` runs only if the
guard's `deny` did not fire and its `ask` was answered yes* — is false for
exactly this shape, and `spec.md`'s "Forgeable by the model: no" row rests on it.
The model does not have to forge the record. It only has to choose which
question gets asked, and the command's first segment is where that is chosen.

Whether a person sees any prompt at all for the third row is then the harness's
generic Bash policy rather than the guard's, which is the one thing the design
set out not to depend on.

The fix belongs in the guard rather than in the writer: the writer's rule is
right, and it is the guard that is judging the wrong segment.

**What the account asserted.** `phase-2.md` names this asymmetry deliberately —
*The writer reads every segment where the guard reads only the first … a creation
anywhere in a command that ran is a creation that was approved* — and then names
one example: `git status && git worktree add …`. That example is the safe half of
the class. `git status` classifies to nothing, so the walk moves on and the
creation ladder does run. A first segment that produces a **different** verdict
was never tried, and it is the half where *a creation that ran* stops meaning *a
creation that was approved*.

### 3 🟡 A wrapper in front of the creation carries the allow with it

`parse_git` reads past `WRAPPERS` (`command`, `env`, `nohup`, `time`, `sudo`) and
past leading `VAR=val` assignments, which is correct for *is this a git
invocation* and wrong for *is this nothing but a creation*. Executed:
`sudo git worktree add ../wt f` and `env LD_PRELOAD=/tmp/e.so git worktree add
../wt f` both allow today. A user's own `permissions.deny` on `Bash(sudo:*)`
would be spoken over by a hook that was reasoning about worktrees.

Nobody types either form on purpose, so refusing them costs nothing. It is listed
apart from finding 1 because the fix is a different line.

### 4 ❓ Does a `permissions.deny` rule outrank a hook `allow`?

The build could not settle it and neither could this round — it is a harness
property, not observable from this repository. If a hook `allow` wins, a user who
explicitly denied `git worktree add` is overridden from their first approval
onward, and findings 1 and 3 decide how much else rides along with that.

`overview.md`'s *Not verified* table already carries it with an answerer named,
which is the shape `agent-contract` §4 asks for. This round adds only that the
question is now larger than the build measured it: findings 1 and 3 widen what an
`allow` is covering when it wins.

**Answerer: the repository owner**, against the harness.

### 5 ❓ A session running with permissions bypassed, and a row that names no answerer

`pr-notes.md` §4 states this in the future tense: *If a future harness
auto-answered hook `ask` decisions, a record could be written with nobody asked.*
`--dangerously-skip-permissions` exists today, and whether a hook `ask` still
stops a session in that mode decides whether the sentence is hypothetical or
current.

The `overview.md` row for it closes with *the same standing every gate in this
repository has*, which names no person. That is the deferral to nobody
`agent-contract` §4 exists to stop, and it is the row where it matters most —
the two harness facts named there are the entire foundation of the change.

Not executed, and not executable from here. If `ask` is auto-answered in that
mode, the honest form of the sentence is that the record means *the harness
permitted it*, which is what `docs/worktree-guard-spec.md` already says in the
paragraph beginning "The harness only runs" and what `spec.md:59` does not.

### 6 ⬜ Three `seal/ledger.md` rows were re-pointed without their `Checked` date moving

`seal/ledger.md:269`, `:337` and `:379` follow `hooks/dispatch.py#GROUPS` from
`b3d45306` to `a5e67d2c`, which is what `CONTRIBUTING.md` prescribes for a claim
that still holds. All three keep `Checked` at `2026-09-02`. `CLAUDE.md` says that
column holds the date somebody read the code, and the precedent one row above
them writes the re-read into `Notes` and moves the date. `evidence-check` does
not touch the column, so nothing else will.

Paperwork, not behaviour, and not counted in `Needs a fix`.

## What was checked and found unchanged

Executed, and worth stating because these are the rows the work must not move.

- A session with no record still meets the single-stream **deny** and is still
  steered to `git switch`.
- The switch direction never reads the record, at any tree state.
- No `PreToolUse` path writes the record it later reads.
- The record is per session and per clone, and a linked worktree shares the main
  clone's.
- The writer fails toward the prompt on every shape tried: a creation inside a
  quoted string, inside a heredoc body, inside a `python3 -c` argument, and in a
  command whose apostrophe broke the lexer all leave no record.
- The `Agent` path returns silently rather than allowing, and silence is not
  allow — the harness's own permission flow still applies, which is what
  `pr-notes.md` §3's second residual claims.

The build's mutation claim was re-run rather than read. Three of the sixteen
mutations were reproduced on a copy of `hooks/` and each one changes observable
behaviour, so the three cases named in `pr-notes.md` §1 have something behind
them.

## Inherited coordinates

No earlier round exists for this work item, so nothing was carried. What was
opened rather than re-derived: `docs/worktree-guard-spec.md` §*Choice sites* for
what the neighbouring marker means, `hooks/cmdline.py`'s `understood`/`Unresolved`
docstrings for what the reader already refuses to read, and `CONTRIBUTING.md`
§*What a change to a gate must carry* for the four answers the pull request owes.

`pr-notes.md` answers all four. The prompt-budget number — one per worktree
unbounded to one per session — is correct for a single-segment creation and is
verified below; both stated residuals are real.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The bounded allow is not bounded. A command substitution, a backtick, an output redirection, a subshell and a heredoc all survive `only_creates_a_worktree`, so `permissionDecision: "allow"` covers whatever the shell runs beside the creation | `hooks/worktree-guard.py:342` · `:1746` | open | **Executed** at `d82a02c` with a consent record present: six shapes answer `allow`. Two were run in a real shell — `$( )` created its marker, `>` truncated a file holding `important`. The signals to refuse them already exist and are discarded: `cmdline.understood` (`hooks/cmdline.py:1282`) inspects the command word only, and `walk_command`'s `wheres`, which carry `Unresolved(CONSTRUCT)` for the subshell, are thrown away at `hooks/worktree-guard.py:368`. The fix below closes all six with the five existing guard modules green (164 passed, 1 skipped) |
| 2 | 🔴 A creation the guard never judged still mints session-wide consent. `main`'s walk stops at the first classified segment while the writer reads every segment, so a `git switch` written in front of a creation takes the verdict and the creation runs unjudged | `hooks/worktree-guard.py:1684` · `hooks/worktree_consent.py:138` | open | **Executed** at `d82a02c`, clean single-stream tree, no record: `git worktree add ../wt f` denies, `git status && git worktree add ../wt f` denies, and `git switch feature/x && git worktree add ../wt f` is **silent** — and the writer records for it. This falsifies `spec.md:59` (*runs only if the guard's `deny` did not fire and its `ask` was answered yes*) and the "Forgeable by the model: no" row that rests on it. The fix below turns that row into `deny` with the same five modules green |
| 3 | 🟡 A wrapper carries the allow. `parse_git` reads past `WRAPPERS` and leading `VAR=val`, so `sudo git worktree add …` and `env LD_PRELOAD=… git worktree add …` are vouched for as creation-and-nothing-else | `hooks/worktree-guard.py:342` · `hooks/cmdline.py:37` | open | **Executed**: both allow at `d82a02c`; both fall to `ask` with the one added line, and `git -C /other worktree add …` and `git worktree add ../a -b feature/x origin/main` still allow. `tests/test_worktree_guard.py` and `tests/test_the_guard_asks_once_per_session.py` stayed green (102 passed) |
| 4 | ❓ Whether a `permissions.deny` rule outranks a hook `allow`. If it does not, a user who explicitly denied `git worktree add` is overridden from their first approval onward | `hooks/worktree-guard.py:1746` | unverified | Not executable from this repository — a harness property. `overview.md`'s *Not verified* table already carries it with an answerer, which is the right shape; this round adds that findings 1 and 3 widen what the `allow` covers when it wins. **Answerer: the repository owner** |
| 5 | ❓ Whether `pr-notes.md` §4's auto-answered `ask` is hypothetical, and the `overview.md` row for it names no answerer — it closes with *the same standing every gate in this repository has*, which is a deferral to nobody | `pr-notes.md` §4 · `overview.md` §*Not verified* | unverified | Not executed, same harness property. `--dangerously-skip-permissions` exists today, so the sentence may be present tense. The two harness facts named in that row are the whole foundation of the change, which is the row that least tolerates an unnamed answerer (`agent-contract` §4). **Answerer: the repository owner** |
| 6 | ⬜ Three `seal/ledger.md` rows follow `dispatch.py#GROUPS` to its new hash while keeping `Checked` at `2026-09-02`, and `evidence-check --reverify` does not touch that column | `seal/ledger.md:269` · `:337` · `:379` | open | **Read.** `CLAUDE.md` says the column holds the date somebody read the code; the row directly above them writes its re-read into `Notes` and moves the date. Paperwork — not counted in `Needs a fix` |

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

Probes were three `test_tmp_*` files; all three are deleted and
`git status --short` is empty. The mutation probe copied `hooks/` to a temp
directory rather than editing the tree. The two fix verifications did patch
`hooks/worktree-guard.py` and were reverted with `git checkout --`; each
substitution asserted its pattern matched before writing (`agent-contract` §9).

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 4 — a `permissions.deny` rule against a hook `allow` | already in `overview.md` §*Not verified*, with an answerer | the repository owner |
| 5 — whether a hook `ask` still stops a session run with permissions bypassed | `overview.md` §*Not verified*, whose row needs the answerer written into it | the repository owner |

## Paste-ready fixes

**Finding 1 and finding 3** — `hooks/worktree-guard.py`. Add the constant above
`only_creates_a_worktree` and replace the loop body. Executed: closes all six
shapes and leaves every legitimate form allowed.

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

**Finding 2** — `hooks/worktree-guard.py`, in `main`. A creation anywhere in the
command outranks an earlier verdict, which makes the guard's reading agree with
the writer's. Executed: `git switch feature/x && git worktree add ../wt f` moves
from silent to `deny` on a clean single-stream tree, with the five guard modules
green.

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

**Finding 6** — `seal/ledger.md`. Move `Checked` to the date the three rows were
re-read, in the same shape the row above them already uses.

```
| … | `hooks/dispatch.py#GROUPS@a5e67d2c`, … | … | 2026-09-08 | … **Re-read 2026-09-08 for #237**, which added `worktree_consent.py` to `post-bash` and a `post-agent` group beside it; neither touches what this row claims, so the claim holds |
```

## Regression cases to plant

Destinations named, so the fix pass has nowhere to guess.

| Case | Destination |
|---|---|
| A creation carrying a command substitution, a backtick, a redirection, a subshell or a heredoc answers `ask` with a record present | `tests/test_the_guard_asks_once_per_session.py`, beside `test_the_allow_covers_only_a_command_that_is_nothing_else` |
| A creation behind `sudo`, `env VAR=…` or a bare `VAR=…` answers `ask`; `git -C <path> worktree add` and `-b <branch> <start>` still allow | the same file |
| `git switch <branch> && git worktree add …` denies in a clean single-stream tree, and the writer's record after it is the one the guard asked about | the same file, beside `test_the_first_creation_is_still_a_question` |

## Facts for the evidence ledger

| Claim | Where it belongs |
|---|---|
| The allow refuses a segment carrying a substitution, a redirection, a subshell, a heredoc or a wrapper, and allows `git -C <path>` and `-b <branch> <start>` | narrows `seal/ledger/1788817291-….md:8`, whose current cell reads **Executed** for a property the six shapes above contradict |
| A creation anywhere in the command takes the creation verdict, so the guard judges the segment the writer records | a new row in the same fragment |

---

Needs a fix: yes — 1, 2, 3

Loses a record or crashes: no

Nothing found leaves the `seal/` root and nothing crashes. Findings 1 and 2 are
🔴 because they let a permission decision cover more than it was reasoned about
and let consent be recorded without the question being put, which is a security
property rather than a durability one.

Contract changes: `guard_worktree_creation` gains a keyword parameter
`consented="ask"` (`hooks/worktree-guard.py:1341`) — default-valued, so no
existing call site changes meaning. `classify`'s worktree branch delegates to
`cmdline.adds_a_worktree` with its signature and returnable set unchanged. No
other signature on the branch moved.

New units: `adds_a_worktree (depth 1)`, `only_creates_a_worktree (depth 1)`,
`CONSENT_DIR (depth 1)`, `consent_path (depth 1)`, `granted (depth 1)`,
`record (depth 1)`, `creation_directory (depth 1)`, `main (depth 1)`

## Proof block

Files opened for this round:

- `hooks/worktree-guard.py`, `hooks/worktree_consent.py`, `hooks/cmdline.py`,
  `hooks/dispatch.py`, `hooks/hooks.json`, `hooks/optin.py`
- `tests/test_the_guard_asks_once_per_session.py`, `bin/test`,
  `.github/scripts/run_tests.py`
- `docs/worktree-guard-spec.md`, `docs/flow.md`, `seal/ledger.md`,
  `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md`,
  `seal/config.md`
- `seal/specs/1788817291-…/{spec.md,plan.md,questions.md,pr-notes.md,overview.md,routing.md,changelog.md,phases/phase-1.md … phase-6.md}`
- `CONTRIBUTING.md` §*What a change to a gate must carry* and §*House rules*,
  `CLAUDE.md`, `gh issue view 237`
- `skills/evidence-check/scripts/evidence_check.py` (the `--reverify` contract),
  `skills/code-review/scripts/round_record.py` (the `depth` vocabulary),
  `seal/specs/1788212517-…/rounds/round-1.md` (the record's shape)
