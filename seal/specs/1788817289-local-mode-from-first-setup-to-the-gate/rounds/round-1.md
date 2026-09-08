# 1788817289-local-mode-from-first-setup-to-the-gate — review round 1

| Field | Value |
|---|---|
| Target SHA | 9d2f440 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed under round 3 |
| Fixes checked by | round-2 |
| Contract changes | already_asked → already_asked, main, choose, round-1-report.md; git_dir_of → marker_dir, round-1-report.md, pytest |
| New units | RETRY_DIR (depth 1); unreadable (depth 1); marker_dir (depth 1); common_dir_of (depth 1); shares_the_clone (depth 1); test_a_separated_git_directory_does_not_displace_the_callers_tree (depth 1); test_the_clone_is_identified_from_the_directory_it_was_asked_about (depth 1); test_a_root_that_is_not_a_work_tree_is_refused (depth 1); test_the_third_command_of_a_session_is_silent (depth 1); test_the_two_prompts_are_counted_apart (depth 1); test_a_config_nobody_can_open_is_silence_not_a_deny (depth 1); test_one_local_root_is_one_question_for_the_whole_clone (depth 1); test_a_shared_root_is_still_a_question_per_work_tree (depth 1); test_the_marker_directory_is_absolute_for_either_question (depth 1) |
| Needs a fix | yes — 1, 2, 3, 4 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of `1788817289-local-mode-from-first-setup-to-the-gate` (tickets #225, #151), at target `9d2f440`, base `86e140f`. No prior rounds, and no pull request open — the orchestrator opens it after this round.

Four stages were built, in the reverse of the order a repository meets them. `round_record.py#where` derived the repository from the work-item path, which is inside `.git` in local mode where `git rev-parse --show-toplevel` exits 128; it now asks `git worktree list --porcelain` and takes the tree the caller is in, and the refusal was split in two because `--item … is not a directory inside a git repository` was true of a correctly placed item and so could not be told from a typo. `chain_check` said *Add seal/specs/<work-item>/routing.md to declare* while the declaration sat under the git common dir and nothing was committed for it to find; it now says which root it looked in. A new gate, `hooks/mode-gate.py`, denies once where `seal/` is present with no `Mode` row. And the `CLAUDE.md` preset block — the range `install.sh` copies into a user's own file — now states the condition before telling a session to write the root.

The design decision was the orchestrator's and was not the round's to reopen: an uncommitted declaration is not read, and `chain_check` reports which root it searched and nothing more. What the round was to judge is whether the reasoning given is sound and whether the code does what it says.

The named targets: this adds a gate, so `CONTRIBUTING.md` §*What a change to a gate must carry* governs and its four answers in `pr-notes.md` were to be checked against the tree rather than against the prose — above all whether the prompt budget is the number claimed, since a gate that fires more often than its pull request says is what that section exists to catch. The `cwd`-versus-root question, where the build's own mutation testing found that using the repository root silences the gate for every session in a subdirectory and that the silence is indistinguishable from a repository whose row is already written. The three mutations that survived the build's own sweep, each to be re-run because a case written to kill a mutation sometimes pins the mutation rather than the property. `git worktree list --porcelain` as the root oracle, executed from inside `.git`, from a linked worktree, from a bare clone, from a `--separate-git-dir` repository and from outside any clone. Whether two parsers really became one. And whether a crash in the new gate can read as a silent allow.

`tests/test_the_records_can_be_carried_out_and_in.py`'s four failures were named as not this branch's — #111's timezone defect, already fixed on the branch that merges first — and were not to be opened.

The report was to be written to a file, finding ids bare integers, every verdict row carrying one, and no finding carrying two rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The `ask` never stops: the gate fires on every Bash call, so after the first deny every command in the session needs an approval — including the `seal mode` that would end it. The budget `pr-notes.md` states is one deny per session per repository | `hooks/mode-gate.py:223-226` | **fixed** `1a54687` | fixed at 1a54687; executed — ten ordinary Bash calls in one session returned deny + nine asks; the sibling gate returned silence on nine of the same ten |
| 2 | 🟡 A `config.md` that exists and cannot be read is treated as one that declared nothing, so the gate denies. Its own docstring says everything here fails toward silence | `hooks/mode-gate.py:105-122` · `hooks/config.py:104-111` | **fixed** `1a54687` | fixed at 1a54687; executed — a directory of that name, undecodable bytes and `chmod 000` each returned deny then ask; a readable row returned silence |
| 3 | 🟡 The marker is keyed per work tree while a local root is one folder for the whole clone, so one session is denied once per worktree. `README.md` says once per repository | `hooks/mode-gate.py:125-142` | **fixed** `1a54687` | fixed at 1a54687; executed — one session, one clone, one local root, two denies |
| 4 | 🟡 `repo_of` returns a directory that is not a work tree for a `--separate-git-dir` repository and for a bare clone, discarding the caller's real tree even when the caller is in it. `pr-notes.md` claims this case is the one the design avoids | `skills/code-review/scripts/round_record.py:1384-1439` | **fixed** `1a54687` | fixed at 1a54687; executed — `git worktree list --porcelain` prints the git directory with no `bare` line; `round_record.py new` from inside the work tree exits 2 with *is not in a git repository* |
| 5 | ⬜ Every Bash call in every repository on the machine now costs one extra `git rev-parse --show-toplevel`, paid again on calls that have nothing left to say | `hooks/mode-gate.py:210-226` | **fixed** `a3bea92` | fixed at a3bea92; executed — one `git` call against the sibling's zero for `ls`; 69.4 ms against 53.8 ms, median of twelve |
| 6 | ⬜ `already_asked`'s `cwd` argument is discarded because `git_dir_of` returns an absolute path; the sibling it was copied from passes a relative one, where the join matters | `hooks/mode-gate.py:94` | **fixed** `1a54687` | fixed at 1a54687; read |
| 7 | ⬜ `templates/config.md` still opens with *an absent row is not an error*, which is no longer true of the `Mode` row | `templates/config.md` | **fixed** `a3bea92` | fixed at a3bea92; read |
| 8 | ⬜ The changelog fragment does not say the gate fires in every repository that opted in before this branch | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/changelog.md` | **fixed** `a3bea92` | fixed at a3bea92; read |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether `--worktree` should read routing declarations from the working tree | `questions.md` Q3 and `seal/follow-up.md` | the repository owner — already deferred by this branch, not re-filed here |
| `tests/test_the_pull_request_language_is_the_repositorys.py#items` reimplements `config_rows` | `overview.md` §*Not verified* | the repository owner — already deferred by this branch, not re-filed here |
| the nine DRIFTED rows in `seal/ledger.md` | `overview.md` §*Not done* | the repository owner — already deferred by this branch |
