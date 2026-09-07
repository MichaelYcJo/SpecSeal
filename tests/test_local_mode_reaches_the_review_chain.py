"""Local mode reaches the review chain: the record tool resolves the root, and
the pull-request check says which root it searched.

Issue #225, observed on 0.8.3 in a repository switched with `seal mode local`.
Two halves of one path.

`round_record.py#where` derived the repository from the ITEM, through a
`git rev-parse --show-toplevel` run from inside it. A local-mode item sits
under the common git directory, where that question is refused — measured
2026-09-08: exit 128, `fatal: this operation must be run in a work tree`. So
every call needed `--root "$PWD"` and the first one without it read as an item
that is nowhere.

`chain_check.py` then printed *Add seal/specs/<work-item>/routing.md to
declare* while the declaration sat at `<git-common-dir>/seal/specs/<item>/
routing.md`. Nothing is committed in local mode, so a false *no declaration*
was indistinguishable from a genuinely undeclared work item — and that
distinction is the only thing the gate exists to give.

The scenario ids are `seal/specs/1788817289-local-mode-from-first-setup-to-
the-gate/spec.md`'s. Every case here was written against the unfixed scripts
and seen red first (contract §15); the output is in the body of the commit
that added this file.

What is deliberately NOT pinned: that local mode reports *declared*. It does
not, and `spec.md` §*The sharp question* holds the argument — this check reads
what git carries, and local mode commits nothing, so naming the root is the
whole fix. Q3 of `questions.md` is the option that was left open.
"""

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, "skills", "code-review", "scripts")
GENERATOR = os.path.join(SCRIPTS, "round_record.py")
CHECK = os.path.join(SCRIPTS, "chain_check.py")

ITEM_ID = "1799000000-a-local-work-item"
RAN_BY = "specseal:warden on a model"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def generator():
    return _load("specseal_round_record_local_mode", GENERATOR)


def git(where, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(where), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=check,
    )


def _build(d):
    d.mkdir(parents=True)
    git(d, "init", "-q", "-b", "base")
    (d / "f.py").write_text("x = 1\n", encoding="utf-8")
    git(d, "add", "-A")
    git(d, "-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "b")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("local-mode-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def common_dir(where):
    """The clone's common git directory, absolute — asked of git, never
    spelled `.git`, which is a FILE in a linked worktree."""
    out = git(where, "rev-parse", "--git-common-dir").stdout.strip()
    return os.path.normpath(os.path.join(str(where), out))


def local_item(repo, item=ITEM_ID, branch="feature"):
    """A work item under the LOCAL root, with a declaration naming `branch`.

    Nothing here is committed, and nothing can be: that is the mode.
    """
    d = os.path.join(common_dir(repo), "seal", "specs", item)
    os.makedirs(os.path.join(d, "rounds"), exist_ok=True)
    with open(os.path.join(d, "routing.md"), "w", encoding="utf-8") as f:
        f.write(
            f"# {item} — routing\n\n"
            "| Axis | Answer |\n|---|---|\n"
            "| Review | through the review chain |\n"
            "| Destination | open the pull request |\n"
            f"| Branch | {branch} |\n"
        )
    return d


def shared_item(repo, item=ITEM_ID):
    d = repo / "seal" / "specs" / item
    (d / "rounds").mkdir(parents=True, exist_ok=True)
    return str(d)


def args_for(item, root=None, round_number=1):
    return argparse.Namespace(item=item, root=root, round=round_number)


# --- S1-S4: the root a work item resolves to -------------------------------


def test_a_local_mode_item_resolves_to_its_repository(generator, repo):
    """S1. The root is the repository, not None — and not something the
    caller had to pass in."""
    item = local_item(repo)
    _reader, _routing, root, where, _rounds = generator.where(args_for(item))
    assert os.path.realpath(root) == os.path.realpath(str(repo))
    assert os.path.realpath(where) == os.path.realpath(item)


def test_a_local_mode_item_writes_its_record(generator, repo, tmp_path):
    """S1, end to end: the command that refused now writes the file."""
    item = local_item(repo)
    report = tmp_path / "report.md"
    report.write_text(
        "# round 1\n\n## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
        "| 🟢 1 | nothing | `f.py:1` | not a defect | read |\n\n"
        "Needs a fix: no\nLoses a record or crashes: no\n",
        encoding="utf-8",
    )
    asked = tmp_path / "asked.md"
    asked.write_text("Read the diff.\n", encoding="utf-8")
    target = git(repo, "rev-parse", "HEAD").stdout.strip()

    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    env["GH_PROMPT_DISABLED"] = "1"
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "new",
            "--item",
            item,
            "--round",
            "1",
            "--target",
            target,
            "--report",
            str(report),
            "--asked",
            str(asked),
            "--ran-by",
            RAN_BY,
            "--baseline",
            "base",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        cwd=str(repo),
        env=env,
    )
    written = os.path.join(item, "rounds", "round-1.md")
    assert r.returncode == 0, r.stdout + r.stderr
    assert os.path.isfile(written), r.stdout + r.stderr


def test_an_item_under_no_repository_is_still_refused(generator, tmp_path):
    """S2. The refusal that stays has to keep refusing — a resolver that
    answers for everything is the fail-open one layer down. And it names what
    it looked for, because `is not a directory inside a git repository` was
    true of a local-mode item too."""
    orphan = tmp_path / "nowhere" / "specs" / "1799000000-x"
    orphan.mkdir(parents=True)
    with pytest.raises(generator.Refused) as caught:
        generator.where(args_for(str(orphan)))
    said = str(caught.value)
    assert str(orphan) in said
    assert "not inside a git repository" in said
    assert "common git directory" in said, (
        "the refusal does not say the local-mode place was tried, which is "
        "what made the old one indistinguishable from a mistyped path"
    )


def test_a_path_that_is_not_a_directory_says_so_on_its_own(generator, tmp_path):
    """The two halves of the old sentence are told apart. It read `is not a
    directory inside a git repository` for both, and that was TRUE of a
    correctly placed local-mode item — which is how one read as a typo."""
    missing = tmp_path / "not-there"
    with pytest.raises(generator.Refused) as caught:
        generator.where(args_for(str(missing)))
    assert str(caught.value) == f"--item {missing} is not a directory"


def test_a_linked_worktree_resolves_to_itself(generator, repo, tmp_path, monkeypatch):
    """S3. The local root is shared by every worktree of the clone, so the
    item alone cannot say which tree this run is about. The caller's is the
    answer: its HEAD and its branch are what the record is a record of."""
    side = tmp_path / "side"
    git(repo, "worktree", "add", "-q", "-b", "side", str(side))
    item = local_item(repo, branch="side")
    monkeypatch.chdir(str(side))
    _reader, _routing, root, _where, _rounds = generator.where(args_for(item))
    assert os.path.realpath(root) == os.path.realpath(str(side))


def test_a_shared_mode_item_resolves_the_way_it_always_did(generator, repo):
    """S4. The path that worked is untouched: the item is in the work tree,
    so git answers for it directly and nothing new runs."""
    item = shared_item(repo)
    _reader, _routing, root, _where, _rounds = generator.where(args_for(item))
    assert os.path.realpath(root) == os.path.realpath(str(repo))


def test_a_shared_item_in_a_linked_worktree_resolves_to_that_worktree(
    generator, repo, tmp_path
):
    """S4, the half a mutation survived. Asking git about the ITEM is what
    answers this one: a shared root lives in ONE tree, so the item names its
    own worktree and the caller's does not get a say. Dropping the shared-mode
    fast path left every case green and moved this answer to the MAIN tree,
    because the fallback below picks the first entry `git worktree list`
    prints. Nothing had reason to look."""
    side = tmp_path / "side"
    git(repo, "worktree", "add", "-q", "-b", "side", str(side))
    item = side / "seal" / "specs" / ITEM_ID
    (item / "rounds").mkdir(parents=True)
    _reader, _routing, root, _where, _rounds = generator.where(args_for(str(item)))
    assert os.path.realpath(root) == os.path.realpath(str(side))


def test_an_explicit_root_still_wins(generator, repo, tmp_path):
    """`--root` is the escape hatch every 0.8.3 caller had to use, and it
    keeps working — a fix that broke it would break the workaround before
    the workaround stopped being needed."""
    item = local_item(repo)
    named = tmp_path / "elsewhere"
    named.mkdir()
    _reader, _routing, root, _where, _rounds = generator.where(
        args_for(item, root=str(named))
    )
    assert os.path.realpath(root) == os.path.realpath(str(named))


# --- S5, S6: the root chain-check says it searched --------------------------


def run_check(repo, *extra):
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    r = subprocess.run(
        [
            sys.executable,
            CHECK,
            "--worktree",
            "--baseline",
            "HEAD",
            "--root",
            str(repo),
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        cwd=str(repo),
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


ADD_THE_FILE = "Add seal/specs/<work-item>/routing.md to declare"


def test_local_mode_is_told_it_is_local_mode(repo):
    """S5. The sentence a local-mode repository used to get named a path it
    does not use and a file it already had. It names the root instead."""
    local_item(repo)
    code, out = run_check(repo)
    assert code == 0, out
    assert ADD_THE_FILE not in out, out
    assert "local mode" in out, out
    assert os.path.join(common_dir(repo), "seal") in out, out
    assert "seal mode shared" in out, out


def test_local_mode_still_examines_nothing(repo):
    """S5, the half that must NOT move. Naming the root does not turn an
    untracked declaration into a checked one: CI reads what git carries, and
    local mode commits nothing. The verdict stays a pass with a notice."""
    local_item(repo)
    _code, out = run_check(repo)
    assert "examined nothing" in out, out
    assert "through the review chain" not in out, out


def test_shared_mode_is_still_told_to_add_the_file(repo):
    """S6. A shared-mode repository with no declaration is the state the old
    sentence was written for, and it is still true there."""
    (repo / "seal" / "specs").mkdir(parents=True)
    code, out = run_check(repo)
    assert code == 0, out
    assert ADD_THE_FILE in out, out
    assert "local mode" not in out, out


def test_the_shared_sentence_says_what_it_searched_and_for_what(repo):
    """S6, the half a mutation survived. *Add this file* on its own does not
    say a search happened — it reads as advice, and the whole complaint in
    #225 is that a reader cannot tell a search that found nothing from one
    that looked in the wrong place. The prefix and the branch are what make
    the sentence checkable."""
    (repo / "seal" / "specs").mkdir(parents=True)
    _code, out = run_check(repo)
    assert "under `seal/specs/`" in out, out
    assert "declares `feature`" in out, out


def test_a_repository_with_no_root_is_told_to_add_the_file(repo):
    """The third state, and it takes the shared wording: there is no root to
    name, so the file to write is the answer."""
    code, out = run_check(repo)
    assert code == 0, out
    assert ADD_THE_FILE in out, out
    assert "local mode" not in out, out
