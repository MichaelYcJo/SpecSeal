"""One opt-in signal, read one way: `seal/` at the first of two places.

`<repo>/seal/` is what shared mode commits; `<git-common-dir>/seal/` is where
local mode will keep it (#80), and 0.4.0 reads it without creating it. The
root's presence is the whole declaration, and there is no config key.

It was `.specseal/` before 0.4.0, and `_ai/` before 0.10. Neither stays
readable: `_ai/` stayed readable for a population that turned out to be
empty, and the compatibility read cost two homes to reason about in every
opt-in check. `.specseal/` is moved once by `hooks/root-migrate.py` at
session start, and until that runs every gate is silent in that repository —
the fail direction `docs/one-root-by-lifetime.md` keeps on purpose.

The same reasoning removed `docs/parity.md` as a second address for the
migration config, which is `seal/parity.md` and only that.

These cases hold the contract — the two places work in order, the old names
are not addresses at all, and the throwaway opt-out is a file under the git
directory, where nothing can commit it.
"""

import os
import subprocess

import pytest
from conftest import decision_of, fired, load_hook_module, local_home, run_hook


@pytest.fixture
def optin():
    return load_hook_module("optin.py", "specseal_optin")


def home(repo):
    (repo / "seal").mkdir(exist_ok=True)


def legacy(repo):
    (repo / ".specseal").mkdir(exist_ok=True)
    (repo / ".specseal" / "map.md").write_text("# map\n")


# --- the signal itself -----------------------------------------------------


def test_new_home_opts_in(optin, repo):
    home(repo)
    assert optin.opted_in(str(repo))
    assert optin.home(str(repo)) == os.path.join(str(repo), "seal")


def test_the_git_directory_is_the_second_place(optin, repo):
    """S2, Q3 (a). Nothing in 0.4.0 creates `.git/seal/`; the hooks read it
    so that #80 changes where the folder is created and nothing that reads
    it."""
    local_home(repo)
    assert optin.opted_in(str(repo))
    assert optin.home(str(repo)) == os.path.join(str(repo), ".git", "seal")


def test_the_shared_root_wins_when_both_exist(optin, repo):
    home(repo)
    local_home(repo)
    assert optin.home(str(repo)) == os.path.join(str(repo), "seal")


def test_the_legacy_directory_is_not_an_opt_in(optin, repo):
    """S3. Without this case the constant can come back and everything stays
    green.

    `.specseal/` reads as an ordinary directory now. A repository still
    holding one is a repository that never opted in, which is the same
    standing as any other repository on the machine — until the session-start
    hook moves it, which is the only thing that reads the name.
    """
    legacy(repo)
    assert not optin.opted_in(str(repo))
    assert not hasattr(optin, "LEGACY"), "the second address is gone, not renamed"


def test_neither_means_out(optin, repo):
    assert not optin.opted_in(str(repo))


def test_a_path_outside_any_repo_is_out(optin, tmp_path):
    assert not optin.opted_in(str(tmp_path / "nowhere"))


def test_it_answers_the_same_from_a_subdirectory(optin, repo):
    home(repo)
    sub = repo / "a" / "b"
    sub.mkdir(parents=True)
    assert optin.opted_in(str(sub))


def test_the_common_git_directory_is_answered_without_git_for_a_main_worktree(
    optin, repo, monkeypatch
):
    """A `.git` directory at the toplevel is the git directory, so the common
    case costs no process. The rider on `repo_root` counts why."""
    monkeypatch.setattr(
        optin.subprocess,
        "run",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("git was asked")),
    )
    assert optin.git_common_dir(str(repo)) == os.path.join(str(repo), ".git")


def test_the_common_git_directory_is_asked_of_git_for_a_linked_worktree(
    optin, repo, tmp_path
):
    other = tmp_path / "linked"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-q", str(other), "feature/x"],
        check=True,
        capture_output=True,
    )
    assert os.path.isfile(other / ".git"), "a linked worktree carries a .git FILE"
    assert os.path.samefile(optin.git_common_dir(str(other)), repo / ".git")


def linked_worktree(repo, tmp_path):
    other = tmp_path / "linked"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-q", str(other), "feature/x"],
        check=True,
        capture_output=True,
    )
    assert os.path.isfile(other / ".git"), "a linked worktree carries a .git FILE"
    return other


# --- #80: where the root lives, and no key -----------------------------------


def test_the_mode_is_read_from_the_folder_and_from_no_key(optin, repo, monkeypatch):
    """S1. The place the root is at says both "on" and which mode; nothing
    else is read. Asked two ways: the module's source names no config key
    and no environment variable, and a repository carrying both a git config
    answer and an environment variable, with `seal/` at neither place, is
    still out."""
    src = open(optin.__file__, encoding="utf-8").read()
    for word in ('"config"', "'config'", "environ", "getenv"):
        assert word not in src, f"optin.py reads a key: {word}"
    subprocess.run(
        ["git", "-C", str(repo), "config", "specseal.mode", "local"],
        check=True,
        capture_output=True,
    )
    monkeypatch.setenv("SPECSEAL_MODE", "local")
    assert not optin.opted_in(str(repo))
    assert optin.home(str(repo)) == ""


def test_a_linked_worktree_resolves_to_the_main_trees_common_root(
    optin, repo, tmp_path
):
    """S2. `.git/seal/` is under the COMMON git directory, so a linked
    worktree, whose `.git` is a file, reads the main tree's root."""
    home = local_home(repo)
    other = linked_worktree(repo, tmp_path)
    assert optin.opted_in(str(other))
    assert os.path.samefile(optin.home(str(other)), home)
    assert os.path.samefile(home, repo / ".git" / "seal")


def test_the_worktrees_own_shared_root_wins_over_the_common_local_one(
    optin, repo, tmp_path
):
    """S1's order, from a linked worktree: `<repo>/seal/` is read first, and
    the worktree's own tree is the repository here."""
    local_home(repo)
    other = linked_worktree(repo, tmp_path)
    (other / "seal").mkdir()
    assert os.path.samefile(optin.home(str(other)), other / "seal")


@pytest.mark.parametrize("shape", ["relative", "absolute"])
def test_gits_common_dir_answer_is_joined_whichever_shape_it_has(
    optin, repo, tmp_path, monkeypatch, shape
):
    """S2, S11. `git rev-parse --git-common-dir` answers relative to the
    directory it ran in unless the path is absolute, and with forward
    slashes on every platform. Both shapes are joined and normalised; no
    drive-letter logic is added for the second."""
    home = local_home(repo)
    other = linked_worktree(repo, tmp_path)
    real = subprocess.run
    answer = (
        os.path.relpath(repo / ".git", other)
        if shape == "relative"
        else str(repo / ".git")
    ).replace(os.sep, "/")

    def answering(args, **kwargs):
        if "--git-common-dir" in args:
            return subprocess.CompletedProcess(args, 0, stdout=answer + "\n", stderr="")
        return real(args, **kwargs)

    monkeypatch.setattr(optin.subprocess, "run", answering)
    got = optin.git_common_dir(str(other))
    assert got == os.path.normpath(got), "the answer was not normalised"
    assert os.path.samefile(got, repo / ".git")
    assert os.path.samefile(optin.home(str(other)), home)


def test_a_file_named_seal_under_the_git_directory_is_not_a_root(optin, repo):
    """The signal is a DIRECTORY at either place. A file of that name under
    the common directory is not a home, and nothing raises over it."""
    (repo / ".git" / "seal").write_text("")
    assert not optin.opted_in(str(repo))
    assert optin.home(str(repo)) == ""


def test_the_local_root_is_never_a_commit_candidate_and_needs_no_gitignore(repo):
    """S3. A declaration, a round record and a ledger fragment under the
    local root are listed by nothing and staged by nothing: git never lists
    its own directory, so no `.gitignore` line exists for it."""
    home = local_home(repo)
    item = home / "specs" / "1788000000-a-work-item"
    (item / "rounds").mkdir(parents=True)
    (item / "routing.md").write_text("# routing\n", encoding="utf-8")
    (item / "rounds" / "round-1.md").write_text("# round 1\n", encoding="utf-8")
    (home / "ledger").mkdir()
    (home / "ledger" / "1788000000-a-work-item.md").write_text("# rows\n")
    git = lambda *a: (
        subprocess.run(
            ["git", "-C", str(repo), *a],
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        ).stdout
    )
    assert git("status", "--porcelain") == ""
    git("add", "-A")
    assert git("diff", "--cached", "--name-only") == ""
    assert not (repo / ".gitignore").exists()


# --- both places, for a caller that has to name the mode it is not in -------


def test_home_paths_names_the_two_places_shared_first(optin, repo):
    """#81. `seal import --into shared|local` has to be able to CREATE the
    root the user named, which `home_at` cannot answer: it reports where the
    root is, and the other mode's root is exactly the one that is not there.

    The pair is produced here so that command spells neither path itself.
    """
    shared, local = optin.home_paths(str(repo))
    assert shared == os.path.join(str(repo), "seal")
    assert local == os.path.join(str(repo), ".git", "seal")
    assert not os.path.isdir(shared) and not os.path.isdir(local), (
        "home_paths answers where a root WOULD be; nothing here exists yet"
    )


def test_home_paths_puts_the_answer_home_at_gives_first(optin, repo):
    """The order is the mode's precedence, and it belongs with the pair
    rather than at each caller. With both roots present `home_at` returns the
    shared one, which is `home_paths`' first entry."""
    home(repo)
    local_home(repo)
    assert optin.home_at(str(repo)) == optin.home_paths(str(repo))[0]


def test_home_paths_is_empty_without_a_root(optin):
    assert optin.home_paths("") == ("", "")


def test_home_paths_costs_no_second_git_call_when_common_is_passed(optin, repo):
    """The rider on `repo_root` counts `git` calls per gated command. A caller
    that already resolved the common directory passes it, and nothing here
    asks git again."""
    common = optin.git_common_dir(str(repo))

    def refuse(*a, **k):
        raise AssertionError("home_paths asked git a second time")

    optin.subprocess.run, saved = refuse, optin.subprocess.run
    try:
        assert optin.home_paths(str(repo), common)[1] == os.path.join(common, "seal")
    finally:
        optin.subprocess.run = saved


# --- the throwaway repository -----------------------------------------------


def scratch(repo):
    (repo / ".git" / "specseal-scratch").write_text("")


def test_a_scratch_marker_takes_the_opt_in_back(optin, repo):
    """S4. A `seal/` directory is the whole opt-in signal, so a git
    repository that exists for thirty seconds as a fixture is indistinguishable
    from a repository under review — and reproducing a gate decision by hand,
    which is what developing these gates consists of, cost a waiver on every
    command (issue #68).

    The marker is written once, by a person, in the repository being thrown
    away. The fixture builders in this suite are untouched: they assert that
    the gates FIRE, and a marker silencing them would invert what they test.
    """
    home(repo)
    scratch(repo)
    assert not optin.opted_in(str(repo))


def test_without_the_marker_the_answer_is_the_one_it_always_was(optin, repo):
    """The marker is the whole difference, so removing the condition turns
    the case above red and nothing else moves."""
    home(repo)
    assert optin.opted_in(str(repo))


def test_a_directory_of_that_name_is_not_the_marker(optin, repo):
    """The signal is an empty FILE, and `os.path.exists` did not say so.

    A directory created where the marker used to live turned every gate off
    in every clone of the repository — a kill switch nobody typed. Both the
    module's own docstring and `seal/README.md` say "file"; this is the read
    catching up with them.
    """
    home(repo)
    (repo / ".git" / "specseal-scratch").mkdir()
    assert optin.opted_in(str(repo))


def test_the_old_scratch_file_is_read_by_nothing(optin, repo):
    """Q4. `.specseal/scratch` used to be the opt-out and sat in a committed
    directory. A file of that name under the root is an ordinary file now;
    `hooks/root-migrate.py` is the one reader that still looks for the old
    one, and it looks in order to refuse the move."""
    home(repo)
    (repo / "seal" / "scratch").write_text("")
    (repo / ".specseal").mkdir()
    (repo / ".specseal" / "scratch").write_text("")
    assert optin.opted_in(str(repo))


def test_the_scratch_marker_answers_the_same_from_a_subdirectory(optin, repo):
    home(repo)
    scratch(repo)
    sub = repo / "a" / "b"
    sub.mkdir(parents=True)
    assert not optin.opted_in(str(sub))


def test_the_scratch_marker_reaches_a_linked_worktree(optin, repo, tmp_path):
    """The common directory is shared, so the opt-out is too: a fixture with
    two worktrees is one throwaway repository, not one and a half."""
    home(repo)
    scratch(repo)
    other = tmp_path / "linked"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-q", str(other), "feature/x"],
        check=True,
        capture_output=True,
    )
    (other / "seal").mkdir()
    assert not optin.opted_in(str(other))


def test_a_scratch_repository_declares_no_migration_config(optin, repo):
    """The second arm reads the same root, and a repository that is not
    under review has nothing to compare against an original either."""
    home(repo)
    scratch(repo)
    (repo / "seal" / "parity.md").write_text("| Original repo | org/legacy |\n")
    assert optin.parity_config(str(repo)) == ""


# --- the migration config has one address too -------------------------------


def test_the_migration_config_is_found_at_the_one_address(optin, repo):
    home(repo)
    (repo / "seal" / "parity.md").write_text("| Original repo | org/legacy |\n")
    # The address, not one platform's spelling of it: `parity_config`
    # builds this with `os.path.join`, and a literal `/` here asserted
    # that the module answers in POSIX on a platform where nothing else
    # does.
    assert optin.parity_config(str(repo)).endswith(os.path.join("seal", "parity.md"))


def test_the_legacy_migration_config_is_not_an_address(optin, repo):
    """`.specseal/parity.md` was the 0.3 location and `docs/parity.md` the
    pre-0.10 one. Neither is read: leaving a read in meant the documents
    describing one address while the code accepted two."""
    home(repo)
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "parity.md").write_text("| Original repo | org/legacy |\n")
    (repo / ".specseal").mkdir(exist_ok=True)
    (repo / ".specseal" / "parity.md").write_text("| Original repo | org/legacy |\n")
    assert optin.parity_config(str(repo)) == ""


def test_the_move_notice_is_gone(optin):
    """Deleted, not muted. A notice with nobody left to warn is a branch that
    runs in no repository and still has to be kept true."""
    for name in ("legacy_only", "MOVE_NOTICE", "notice_due", "NOTICE_DIR"):
        assert not hasattr(optin, name), name


# --- the gates read it -----------------------------------------------------


def payload(cmd, repo):
    return {
        "tool_name": "Bash",
        "session_id": "s1",
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }


def test_commit_gate_fires_on_the_new_home(repo):
    home(repo)
    assert fired(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))


def test_commit_gate_stays_silent_on_the_legacy_marker(repo):
    """S3: every gate is silent over `.specseal/`, and the only thing that
    speaks is the migration hook at session start."""
    legacy(repo)
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "silent"


def test_review_skill_gate_fires_on_the_new_home(repo):
    home(repo)
    out = run_hook(
        "review-skill-gate.py",
        {
            "tool_name": "Skill",
            "session_id": "s1",
            "tool_input": {"skill": "code-review"},
            "cwd": str(repo),
        },
    )
    assert decision_of(out) == "deny"


def test_review_skill_gate_stays_silent_on_the_legacy_marker(repo):
    legacy(repo)
    out = run_hook(
        "review-skill-gate.py",
        {
            "tool_name": "Skill",
            "session_id": "s1",
            "tool_input": {"skill": "code-review"},
            "cwd": str(repo),
        },
    )
    assert decision_of(out) == "silent"


def test_the_home_directory_counts_as_documents_not_code(repo):
    """The parity gate compares code against an original; `seal/` is neither.

    Asking there would train people to click through the prompt, which costs
    more than the check is worth."""
    gate = load_hook_module("commit-review-gate.py", "commit_review_gate")
    (repo / "seal").mkdir()
    (repo / "seal" / "ledger.md").write_text("# ledger\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    assert not gate.touches_code(
        str(repo), gate.commit_invocations("git commit -m x")[0]
    )


def test_a_code_change_alongside_it_still_counts(repo):
    gate = load_hook_module("commit-review-gate.py", "commit_review_gate")
    (repo / "seal").mkdir()
    (repo / "seal" / "ledger.md").write_text("# ledger\n")
    (repo / "app.py").write_text("x = 1\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    assert gate.touches_code(str(repo), gate.commit_invocations("git commit -m x")[0])


def test_the_session_start_hook_says_nothing_in_a_legacy_repo(repo):
    """The repository never opted in, so this hook has no business speaking.

    It used to hear "the home moved" instead — a notice naming four
    destinations, two of which do not exist any more.
    """
    legacy(repo)
    hook = load_hook_module("version-check.py", "vc_move")
    import contextlib
    import io
    import json as _json
    import sys

    sys.stdin = io.StringIO(_json.dumps({"cwd": str(repo), "session_id": "s1"}))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        hook.main()
    assert buf.getvalue() == ""


def test_an_opted_in_repo_at_the_newest_version_hears_nothing(repo):
    home(repo)
    hook = load_hook_module("version-check.py", "vc_moved")
    hook.running = lambda: ((9, 9, 9), "https://example.com/x/y")
    hook.latest = lambda url: (0, 1, 0)
    import contextlib
    import io
    import json as _json
    import sys

    sys.stdin = io.StringIO(_json.dumps({"cwd": str(repo), "session_id": "s1"}))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        hook.main()
    assert buf.getvalue() == ""


def test_the_commit_gate_is_silent_in_a_scratch_repository(repo):
    home(repo)
    scratch(repo)
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "silent"


def test_the_review_skill_gate_is_silent_in_a_scratch_repository(repo):
    home(repo)
    scratch(repo)
    out = run_hook(
        "review-skill-gate.py",
        {
            "tool_name": "Skill",
            "session_id": "s1",
            "tool_input": {"skill": "code-review"},
            "cwd": str(repo),
        },
    )
    assert decision_of(out) == "silent"


def test_the_commit_gate_still_fires_beside_a_scratch_DIRECTORY(repo):
    """The gate-level half of the file-not-directory rule."""
    home(repo)
    (repo / ".git" / "specseal-scratch").mkdir()
    assert fired(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))


def test_a_scratch_repository_gives_no_standing_over_a_target_it_cannot_read(repo):
    """The stop for an unreadable target is the session's own repository
    speaking, so the marker has to reach that too — otherwise the probe that
    prompted issue #68 keeps prompting, one door along."""
    home(repo)
    scratch(repo)
    out = run_hook("commit-review-gate.py", payload('git -C "$WT" commit -m x', repo))
    assert decision_of(out) == "silent"
