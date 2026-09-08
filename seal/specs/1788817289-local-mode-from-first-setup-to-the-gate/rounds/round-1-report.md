# Round 1 — `1788817289-local-mode-from-first-setup-to-the-gate` (#225, #151)

Target SHA `9d2f440` · base `86e140f` · branch
`fix/225-151-local-mode-from-first-setup-to-the-gate` · no pull request open.

## What this round was asked

Read the four SDD documents, the five phase records and both tickets, then
attack five things: the prompt budget `pr-notes.md` claims for the new gate,
`cwd` against the repository root inside that gate, the three mutations the
build's own sweep let through, `git worktree list --porcelain` as the root
oracle, and whether one config parser is now really one. `hooks/dispatch.py`
and `hooks/hooks.json` were in scope for wiring and for what an unreadable
`config.md` does.

The design decision — that an uncommitted declaration is not read, and
`chain_check` only says which root it searched — was out of scope to reopen,
and this round did not reopen it. Judged instead: whether the reasoning given
is sound, and whether the code does what it says. On both, yes.

Four of the 78 cases in `tests/test_the_records_can_be_carried_out_and_in.py`
were named as #111's and were not opened.

## How the findings hang together

Three of the four things needing a fix are one cause. The gate was moved off
the commit and onto every Bash call, which is the right placement for the
question — and every property that used to be bounded by *how often does
somebody commit* is now bounded by *how often does somebody run a command*,
which is not the same number and was not re-derived.

```
  the gate fires on every Bash call, not on a commit
        ↓
  ① the follow-up `ask` never stops — one deny and nine asks over ten calls
        ↓ compounds
  ② a config.md that cannot be READ is treated as one that answered nothing
  ③ the marker is keyed per work tree while a local root is one per clone
```

④ is separate, and it is in the other half of the branch: the new root oracle
answers a directory that is not a work tree.

## ① Every Bash call after the first one asks

**`hooks/mode-gate.py:223-226`. 🔴 blocks — the budget stated is not the
budget the code has.**

`pr-notes.md` §*A prompt budget* says *one deny per session per repository*,
and *the worst case for an unattended run is one stalled command and one
approval, not a halt*. `CONTRIBUTING.md` §*What a change to a gate must
carry* asks for that number because a gate that fires more often than its
pull request says is the defect the section exists to catch.

Executed, ten ordinary Bash calls in one session in a repository with `seal/`
and no `Mode` row:

```
call  1  ls                       -> deny
call  2  cat README.md            -> ask
call  3  git status               -> ask
...
call 10  wc -l f.py               -> ask
```

The sibling gate under the same ten calls is silent on nine of them and denies
only the commit, because `commit-review-gate.py#main` returns early for a
command that is not a commit. This gate has no such early return, so
`already_asked` returning `True` — which it does forever after the first call —
lands on `decide("ask", …)` every time.

**Why it matters more than one extra prompt.** The way out is `seal mode`, and
`seal mode` is a Bash call, so it meets the `ask` too. A run that cannot answer
an `ask` therefore cannot reach the command that would end the asking, and
every command it tries is blocked rather than one. That is the outage the
gate's own docstring (`hooks/mode-gate.py:52-56`) says it cannot become.

**Who meets this.** Every repository that opted in before this branch. The
`Mode` row is written by `seal mode` and, from this branch onwards, by the
bootstrap; nothing back-fills it, and nothing at session start writes one. So
on upgrade every existing installation without that row meets the deny on its
next session's first command and the `ask` on every command after it.

## ② And a `config.md` it cannot read counts as one that answered nothing

**`hooks/mode-gate.py:105-122` with `hooks/config.py:104-111`. 🟡 fix or
justify.**

`hooks/mode-gate.py`'s docstring closes with *Everything here fails toward
silence, the way `hooks/optin.py` does: a repository this cannot read is one it
says nothing about.* Executed, it does not:

| `seal/config.md` | first call | second call |
|---|---|---|
| `\| Mode \| shared \|` | silent | silent |
| a directory of that name | **deny** | **ask** |
| bytes UTF-8 cannot decode | **deny** | **ask** |
| `chmod 000` | **deny** | **ask** |

The direction comes from `hooks/config.py#declared_mode`, which folds
*unreadable* into `"none"` and is right to: `seal.py` is the writer, and a file
it cannot read is a file it goes on to write. A gate is not a writer. For it,
*no answer* and *an answer I could not open* are different states, and the
second is where `hooks/optin.py` says to say nothing.

The reachable case is not exotic. `hooks/optin.py:63-76` already records a
repository under a path a cp949 console cannot decode; a `Record language`
row hand-edited in a non-UTF-8 locale puts the same bytes in this file. With ①
standing, such a repository gets a prompt on every command of every session and
`seal mode` cannot clear it, because the row it would write is in a file
nothing can parse.

## ③ One clone, one local root, two denies

**`hooks/mode-gate.py:125-142`. 🟡 fix or justify — the README's count and the
code's key disagree.**

`README.md`'s gate row says **Once per session per repository**.
`git_dir_of` asks for `--absolute-git-dir`, which in a linked worktree is
`<common>/worktrees/<name>`, so the marker is keyed per work tree.

In shared mode that is right: each work tree has its own `<repo>/seal/`, so
each is a separate unanswered root. In local mode there is **one** root under
the common git directory serving every work tree, and `undeclared()` reads that
one root from all of them. Executed, one session across one clone:

```
main tree              -> deny
main tree again        -> ask
linked worktree        -> deny      ← the same folder, asked again
linked worktree again  -> ask
```

The docstring gives the mechanism (*a linked worktree's marker lands in that
worktree's own git directory*) but not the reason, and the reason does not hold
for the mode this branch is about.

## ④ The root oracle answers a directory that is not a work tree

**`skills/code-review/scripts/round_record.py#worktrees_of` and `#repo_of`
(lines 1384-1439). 🟡 fix or justify.**

`pr-notes.md` §*Platform honesty* says a repository built with
`--separate-git-dir` *is why the root resolution asks `git worktree list`
instead of taking `dirname` of the common directory, so the untested case is
the one the design avoids relying on rather than the one it depends on*.

Executed, that is the case it gets wrong. `git worktree list --porcelain`
prints the **git directory** as the worktree path when the tree was separated
from it, and there is no `bare` line to tell them apart:

```
worktree /…/sepgit
HEAD c7e5ecd…
branch refs/heads/base
```

So `worktrees_of` returns `['/…/sepgit']`, the caller's real tree `/…/septree`
is not in that set, and `repo_of` falls through to `trees[0]` and returns the
git directory — **even when the caller is standing in the work tree.** End to
end, `round_record.py new --item <that item>` from inside the work tree:

```
round-record: wrote …/rounds/round-1.md
chain-check: /…/sepgit is not in a git repository — nothing was compared
exit 2
```

The record is written and the chain check never runs. A bare clone takes the
same path — `worktree /…/bare.git` plus `bare` — and `repo_of` names it too.

Nothing is lost and nothing crashes; what ships is a root every later
`git -C <root>` refuses, reported as the root.

## Smaller things

**⑤ Every Bash call in every repository on the machine now costs one more
`git`.** Measured with a logging `git` on `PATH`, one `ls` in a repository with
no `seal/` at all: `mode-gate.py` makes one `git rev-parse --show-toplevel`,
`commit-review-gate.py` makes zero, because it returns before resolving
anything for a command that is not a commit. Wall time for the gate alone, the
median of twelve: 69.4 ms against the sibling's 53.8 ms.
`hooks/optin.py#repo_root` carries a RIDER counting exactly this class of cost;
this adds a caller to it and the budget section does not mention it.
`already_asked` is checked after the resolution rather than before, so the
cost is paid again on every call that has nothing left to say.

**⑥ `already_asked`'s first parameter does nothing in this gate.**
`hooks/mode-gate.py:94` joins `cwd` with `git_dir`, and `git_dir_of` returns an
absolute path, so `os.path.join` discards `cwd`. The sibling it was copied from
passes a **relative** git dir, where the join is load-bearing. Nothing is wrong
today; a later change of `--absolute-git-dir` to `--git-dir` would move every
marker silently.

**⑦ `templates/config.md` still says an absent row is not an error.** Its
opening — *This file is optional, and an absent row is not an error* — is now
false for one row: an absent `Mode` denies a command. The `## Mode` section
already carves out the *no default* half and does not carve out this one.

**⑧ Nothing tells an existing installation what upgrading costs it.** The
changelog fragment describes the gate accurately and never says it fires in
every repository that opted in before this branch. That is the sentence a
reader needs in order to run `seal mode` before the gate asks them to.

## What was attacked and came back clean

**The three surviving mutations are dead, and each case pins the property
rather than the mutation.** Re-run one at a time against a clone at `9d2f440`
with the caches off; each killed exactly one case, and reading those three
cases, none of them asserts the mutant's text:

| Mutation | Killed by |
|---|---|
| `repo_of` — drop the shared-mode fast path | `test_a_shared_item_in_a_linked_worktree_resolves_to_that_worktree` |
| `nothing_declared` — drop the new half of the shared sentence | `test_the_shared_sentence_says_what_it_searched_and_for_what` |
| `mode-gate.main` — take `cwd` for the repository root | `test_a_session_in_a_subdirectory_is_still_asked` |

**`cwd` against the root, everywhere else in the new gate.** `main()` resolves
the root from the payload's `cwd` and passes the **root** to `undeclared()` and
to `git_dir_of()`; both want the root. The one remaining place the two could be
confused is ⑥ above, where the wrong one is currently harmless.

**Two parsers really are one.** `hooks/config.py` holds the only production
implementation; `seal.py` binds the names to it rather than copying it, and
`test_the_command_and_the_gate_read_one_parser` checks that by `__code__.
co_filename`, which a re-copy cannot fool. The third copy —
`tests/test_the_pull_request_language_is_the_repositorys.py#items` at line 297
— is a test-local reimplementation and is **already deferred** in
`overview.md` §*Not verified* with the repository owner as its answerer. Not
re-opened here.

**The new gate is reached and its neighbours still pass.** `mode-gate.py` is in
`dispatch.GROUPS["pre-bash"]` and `hooks.json` routes `Bash` there. A crash in
it is swallowed by `dispatch.run_gate`, which reads as an allow — that is the
documented RIDER at `hooks/dispatch.py:80-94` and is the same fail-open every
gate in the group already has, not something this branch introduced. Eight
neighbouring gate modules that were **not** edited by this branch were run and
all pass, so the blast radius of adding a voice to `pre-bash` really was the two
modules the branch touched.

**The `git worktree list` oracle, from five places.** Answers correctly from
inside `.git/seal/…`, from a linked worktree (the caller's tree wins), and from
outside the clone (the main tree, which is what the docstring promises).
Refuses correctly for an item under no repository. The two it gets wrong are
④.

**`chain_check`'s two sentences.** Both branches were run: a local-mode
repository is told which root it uses and is not told to add a file; a
shared-mode repository and a repository with no root both still get *Add
seal/specs/<work-item>/routing.md to declare*, now with the prefix and the
branch it searched for. The verdict does not move in either — `examined
nothing`, exit 0 — which is what `spec.md` §*The sharp question* argued for.

## Coordinates carried rather than re-derived

| Carried | From | Used for |
|---|---|---|
| `commit-review-gate.py#already_asked` is the marker rule this gate copies | `hooks/mode-gate.py:84` | the comparison in ① and ⑥ — re-read, and the two differ in the `cwd` argument |
| `optin.repo_root`'s RIDER counts `git` calls per gated command | `hooks/optin.py:53-57` | ⑤, which adds a caller to that count |
| `dispatch.run_gate`'s catch reads as an allow | `hooks/dispatch.py:80-94` | the crash question, answered as pre-existing |
| four cases in `test_the_records_can_be_carried_out_and_in.py` are #111's | the spawn prompt and `overview.md` | not opened |
| the third `config_rows` copy is a test-local one with a named answerer | `overview.md` §*Not verified* | named as already deferred, not re-filed |

No `rounds/round-*.md` exists for this work item, so there were no earlier
verdicts to inherit or re-derive.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The `ask` never stops: the gate fires on every Bash call, so after the first deny every command in the session needs an approval — including the `seal mode` that would end it. The budget `pr-notes.md` states is one deny per session per repository | `hooks/mode-gate.py:223-226` | open | executed — ten ordinary Bash calls in one session returned deny + nine asks; the sibling gate returned silence on nine of the same ten |
| 2 | 🟡 A `config.md` that exists and cannot be read is treated as one that declared nothing, so the gate denies. Its own docstring says everything here fails toward silence | `hooks/mode-gate.py:105-122` · `hooks/config.py:104-111` | open | executed — a directory of that name, undecodable bytes and `chmod 000` each returned deny then ask; a readable row returned silence |
| 3 | 🟡 The marker is keyed per work tree while a local root is one folder for the whole clone, so one session is denied once per worktree. `README.md` says once per repository | `hooks/mode-gate.py:125-142` | open | executed — one session, one clone, one local root, two denies |
| 4 | 🟡 `repo_of` returns a directory that is not a work tree for a `--separate-git-dir` repository and for a bare clone, discarding the caller's real tree even when the caller is in it. `pr-notes.md` claims this case is the one the design avoids | `skills/code-review/scripts/round_record.py:1384-1439` | open | executed — `git worktree list --porcelain` prints the git directory with no `bare` line; `round_record.py new` from inside the work tree exits 2 with *is not in a git repository* |
| 5 | ⬜ Every Bash call in every repository on the machine now costs one extra `git rev-parse --show-toplevel`, paid again on calls that have nothing left to say | `hooks/mode-gate.py:210-226` | open | executed — one `git` call against the sibling's zero for `ls`; 69.4 ms against 53.8 ms, median of twelve |
| 6 | ⬜ `already_asked`'s `cwd` argument is discarded because `git_dir_of` returns an absolute path; the sibling it was copied from passes a relative one, where the join matters | `hooks/mode-gate.py:94` | open | read |
| 7 | ⬜ `templates/config.md` still opens with *an absent row is not an error*, which is no longer true of the `Mode` row | `templates/config.md` | open | read |
| 8 | ⬜ The changelog fragment does not say the gate fires in every repository that opted in before this branch | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/changelog.md` | open | read |

## Executed probes

| What was run | Result |
|---|---|
| `hooks/mode-gate.py` fed ten ordinary Bash payloads in one session, repo with `seal/` and no `Mode` row | `deny` then `ask` ×9; with the row written after call 6, `silent` from call 7 |
| the same ten payloads through `hooks/commit-review-gate.py` | `silent` ×9, `deny` on the commit only |
| `hooks/mode-gate.py` against six states of `seal/config.md` | readable row → silent; directory / undecodable bytes / `chmod 000` → deny then ask; `\| :--- \|` separator → silent |
| `hooks/mode-gate.py` in a linked worktree of a local-mode clone, one session | main tree `deny`, worktree `deny` — one root, two denies |
| `git worktree list --porcelain` and `round_record.repo_of` from five places | main tree, linked worktree, outside the clone: correct. bare clone and `--separate-git-dir`: the git directory returned as the root. no repository: `None` |
| `round_record.py new --item …` end to end in a `--separate-git-dir` repository, from inside the work tree | exit 2, record written, `chain-check: /…/sepgit is not in a git repository — nothing was compared` |
| the same command in an ordinary local-mode and an ordinary shared-mode repository | identical output in both; the `../../..` ladder in the printed path is the macOS `/var` symlink and is present at the base too, so not this branch's |
| the three named mutations, one at a time, against a `--no-local` clone at `9d2f440` with caches off | all three killed, one case each — see the table above |
| `tests/test_local_mode_reaches_the_review_chain.py`, `…the_mode_question_is_asked_once.py`, `…first_setup_asks_once.py`, `test_dispatch.py`, `test_gate_judges_the_repo_it_commits_to.py` | 178 passed |
| eight neighbouring gate modules this branch did not edit (`test_gates_do_not_fail_open.py`, `test_chain_hooks_hardening.py`, `test_console_is_not_utf8.py`, `test_the_root_migrates_itself.py`, `test_chain_hooks.py`, `test_review_skill_gate.py`, `test_the_implementer_is_recorded.py`, `test_the_mode_is_a_row_and_a_command.py`) | 234 passed |
| a logging `git` on `PATH`, one `ls` payload, repo with no `seal/` | mode-gate 1 `git` call, commit-review-gate 0 |
| each of the four fixes below, applied to the clone and exercised | fix 1 → `deny, ask, silent, silent…`; fix 2 → the work tree, and `None` from outside; fix 3 → silence for all three unreadable states, deny still for no row; fix 4 → local one deny, shared two. Every touched suite green (38, 13, 124, 124) |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether `--worktree` should read routing declarations from the working tree | `questions.md` Q3 and `seal/follow-up.md` | the repository owner — already deferred by this branch, not re-filed here |
| `tests/test_the_pull_request_language_is_the_repositorys.py#items` reimplements `config_rows` | `overview.md` §*Not verified* | the repository owner — already deferred by this branch, not re-filed here |
| the nine DRIFTED rows in `seal/ledger.md` | `overview.md` §*Not done* | the repository owner — already deferred by this branch |

## Paste-ready fixes

**Finding 1** — `hooks/mode-gate.py`. Spend the `ask` once too, so the budget is
the one `pr-notes.md` states. Four edits; the second and third only thread a
parameter. Verified: `deny, ask, silent, silent, silent, silent` in one
session, `deny, ask, silent` in the next, silent once the row exists, and
`test_the_mode_question_is_asked_once.py` + `test_dispatch.py` green (38
passed) — `test_the_second_attempt_in_a_session_only_asks` still sees deny then
ask.

One trade to state in the record: with no session id, both markers count as
already written and the gate goes silent instead of asking on every call. That
is the direction the docstring already commits to.

```python
CHOICE_DIR = "specseal-mode-choice"
# The second and last prompt of the session: the approvable retry the deny
# tells the model to make. Its own directory, so the two are counted apart
# the way the deny and the ask are two different questions.
RETRY_DIR = "specseal-mode-retry"
```

```python
def already_asked(cwd, git_dir, session, choice_dir=CHOICE_DIR):
```

```python
    path = os.path.join(cwd or ".", git_dir, choice_dir, session)
```

```python
    session = payload.get("session_id")
    # No session id means no way to record that the question was asked, so a
    # deny would repeat forever. `ask` cannot loop: approving is the way out.
    #
    # And the ASK is spent too, once. This gate fires on every Bash call
    # rather than on a commit, so an `ask` that stands for the rest of the
    # session is a permission prompt on every command -- measured 2026-09-08,
    # one deny and nine asks over ten ordinary calls, where the sibling gate
    # was silent on nine of the same ten. The way out is `seal mode`, which is
    # itself a Bash call, so a run that cannot answer an `ask` cannot reach the
    # command that ends the asking. That is the outage the docstring above
    # says this cannot become.
    git_dir = git_dir_of(root)
    if session and not already_asked(root, git_dir, session, CHOICE_DIR):
        decide("deny", question_reason(root, home))
    elif session and not already_asked(root, git_dir, session, RETRY_DIR):
        decide("ask", ask_reason(root, home))
```

**Finding 2** — `hooks/mode-gate.py`. Tell *no answer* apart from *an answer
this could not open*, in the gate, leaving `hooks/config.py`'s four spellings
alone for the writer. Verified: directory, undecodable bytes and `chmod 000`
all silent; no file and no `Mode` row still deny; 124 passed across the three
gate suites.

```python
def undeclared(root):
    home = optin.home_at(root)
    if not home:
        return ""
    if unreadable(repo_config.config_path(home)):
        return ""
    kind, _value = repo_config.declared_mode(home)
    return "" if kind == "mode" else home


def unreadable(path):
    """True when `path` is there and this process cannot read it as text.

    `config.py` folds no file, no row, an empty value and a file that will not
    open into one answer, and that is right for the WRITER: `seal mode` goes
    on to write the row either way. For a GATE the fourth is different in
    kind. A file that exists and cannot be opened -- a directory of that name,
    a permission this process does not have, bytes this locale cannot decode
    -- is not a repository that failed to answer. It is one whose answer could
    not be read, and `hooks/optin.py` is the module that says what to do then:
    say nothing.
    """
    if not os.path.lexists(path):
        return False
    try:
        with open(path, encoding="utf-8") as handle:
            handle.read()
    except (OSError, ValueError):
        return True
    return False
```

**Finding 3** — `hooks/mode-gate.py`. Key the marker to the root rather than to
the tree. Verified: local mode denies once across a clone's two work trees,
shared mode still denies in each (they are two roots); 124 passed.

```python
def git_dir_of(root, which="--absolute-git-dir"):
    """`root`'s git directory as an absolute path, or "".

    Absolute, so the join in `already_asked` does not depend on which
    directory this process is in.

    `which` picks WHOSE git directory, and that follows the root rather than
    the tree. A shared root lives in one work tree, so the question is that
    tree's. A LOCAL root is one folder every worktree of the clone shares, so
    the question is the clone's and `--git-common-dir` is the only key that
    counts it once -- measured 2026-09-08: one session, one clone, one local
    root, two denies.
    """
    try:
        done = subprocess.run(
            ["git", "-C", root, "rev-parse", which],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return (done.stdout or "").strip() if done.returncode == 0 else ""


def marker_dir(root, home):
    """The git directory this root's answer is recorded in.

    Per work tree for a shared root, which one tree owns; per CLONE for a
    local one, which every worktree of the clone shares.
    """
    shared, _local = optin.home_paths(root)
    if shared and os.path.realpath(home) == os.path.realpath(shared):
        return git_dir_of(root)
    return git_dir_of(root, "--git-common-dir")
```

and in `main()`, `git_dir_of(root)` becomes `marker_dir(root, home)`.

**Finding 4** — `skills/code-review/scripts/round_record.py`. Prefer the
caller's tree whenever it belongs to the item's clone, compared by common git
directory rather than by the paths `git worktree list` prints; and refuse
rather than name a path that is not a work tree. Verified: the
`--separate-git-dir` work tree is returned when the caller is in it, `None`
when the caller is outside; 13 passed.

```python
    here = reader.repo_root(os.getcwd())
    if here and (
        os.path.realpath(here) in {os.path.realpath(t) for t in trees}
        or shares_the_clone(here, item)
    ):
        return here
    # `git worktree list` prints the GIT DIRECTORY rather than a work tree for
    # a bare clone and for one made with `--separate-git-dir` -- measured
    # 2026-09-08, both, and the second carries no `bare` line to tell it by. A
    # root every later `git -C <root>` refuses is not a root, so this refuses
    # instead of naming one.
    first = trees[0]
    return first if reader.repo_root(first) else None


def common_dir_of(where):
    """`where`'s common git directory, absolute and resolved, or ""."""
    try:
        out = git(where, "rev-parse", "--git-common-dir")
    except (OSError, subprocess.SubprocessError):
        return ""
    out = (out or "").strip()
    return os.path.realpath(os.path.join(where, out)) if out else ""


def shares_the_clone(root, item):
    """True when `root` is a work tree of the clone `item` sits in.

    Compared by common git directory, never by the paths `git worktree list`
    prints: with `--separate-git-dir` those ARE the git directory, so the
    caller's own tree is not in the list it belongs to.
    """
    ours, theirs = common_dir_of(root), common_dir_of(item)
    return bool(ours) and ours == theirs
```

**Findings 5-8** need no code beside a decision. ⑤ is a sentence in the budget
section naming the per-call `git` cost, or an early `already_asked` check
before the resolution. ⑥ is either dropping the parameter or a comment saying
the join is a no-op here. ⑦ is one clause in `templates/config.md`'s opening.
⑧ is one sentence in the changelog fragment saying every repository that
opted in before this branch meets the gate on upgrade.

## For the record the orchestrator writes

Needs a fix: yes — 1, 2, 3, 4
Loses a record or crashes: no

Nothing found leaves the root or crashes. Finding 4's command exits 2 **after**
writing the record, so the file is on disk; what is lost is the chain check
that would have run, and the message says so rather than passing silently.
Finding 1 blocks commands and records nothing wrong.

Contract changes: `round_record.where`'s refusal became two sentences, so
anything matching the old `--item … is not a directory inside a git repository`
no longer matches · `chain_check`'s no-declaration sentence gained a second
form for local mode · `seal.py`'s `CONFIG`, `ROW_ITEM`, `LOCAL`, `SHARED`,
`MODES`, `CONFIG_HEADER`, `CONFIG_ROW`, `CONFIG_SEPARATOR`, `config_path`,
`config_rows` and `declared` are now aliases of `hooks/config.py`, same
signatures · `dispatch.GROUPS["pre-bash"]` gained a member, so the group can
now produce a decision on a command that is not a commit.

New units: `config_path (depth 1)` · `config_rows (depth 1)` ·
`declared_mode (depth 1)` · `already_asked (depth 1)` · `undeclared (depth 1)`
· `git_dir_of (depth 1)` · `question_reason (depth 1)` · `ask_reason (depth 1)`
· `decide (depth 1)` · `main (depth 1)` · `local_root (depth 1)` ·
`nothing_declared (depth 1)` · `worktrees_of (depth 1)` · `repo_of (depth 1)`

Broad gate: not yet. The full suite, the repository-wide lint and the typecheck
are the orchestrator's, after these findings are answered
(`agent-contract` §2). This round ran the changed slice and its gate
neighbours only.

## Proof

Read: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `pr-notes.md`,
`changelog.md`, `routing.md` and `phases/phase-1..5.md` under
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/` ·
`hooks/mode-gate.py`, `hooks/config.py`, `hooks/optin.py`, `hooks/dispatch.py`,
`hooks/hooks.json`, `hooks/commit-review-gate.py` (main, `already_asked`,
decision shape), `hooks/routing.py` (exports) ·
`skills/code-review/scripts/round_record.py` (`git`, `worktrees_of`,
`repo_of`, `where`), `skills/code-review/scripts/chain_check.py`
(`declared_for_this_branch`, `local_root`, `nothing_declared`),
`skills/implement/scripts/seal.py` (the config block), `skills/implement/SKILL.md`
(the Bootstrap diff) · `tests/test_local_mode_reaches_the_review_chain.py`,
`tests/test_the_mode_question_is_asked_once.py`,
`tests/test_first_setup_asks_once.py`, `tests/test_dispatch.py`,
`tests/test_gate_judges_the_repo_it_commits_to.py`,
`tests/test_the_pull_request_language_is_the_repositorys.py` (lines 285-340) ·
`CLAUDE.md`, `README.md`, `README.ko.md`, `templates/config.md`, `install.sh`,
`bin/test`, `CONTRIBUTING.md` (the test command) · `seal/config.md`.

Executed: the eleven probe runs in the table above, against a
`git clone --no-local` of this worktree at `9d2f440` with a `uv` virtualenv,
and against throwaway repositories built by Python driving `git` — no probe
left anything in `wi-225`, and every probe file lives in the session
scratchpad.
