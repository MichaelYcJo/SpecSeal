"""The gate and CI ran the same five checks over one branch and asked them
about different ranges (#423).

`broad_gate.py` built every child check's argument out of `--base` as the
caller typed it, so a plain branch name resolved to the LOCAL ref.
`.github/workflows/hygiene.yml` spells the same thing `origin/<base>`, which
is not a choice it made — a runner's checkout has no local branch, so that is
the only spelling that resolves there. On 2026-09-16 the local ref was one
commit behind its remote: the gate reported two survivors, all excused, exit 0
and drew the stamp, and CI reported seven places and exit 1 on the same
branch, the same check and the same commit.

This module holds the repair. Three halves, and they go red for different
edits:

  the resolver    `resolve_base` reaches for what CI will read — the given
                  ref's upstream where the checkout declares one, else
                  `refs/remotes/origin/<base>`, else the ref as given. A
                  repository with no remote at all resolves to itself, which
                  is what keeps all but ONE assertion of
                  `tests/test_the_seal_is_taken_once_by_the_sealer.py`
                  reading as it did. The one that moved is the `Broad gate`
                  cell's base half: the consumers are handed the resolved
                  commit even where the resolution lands on the ref as given
                  (round 1, finding 3, and the A3 row of `overview.md`)
  end to end      a fixture whose local `base` is one commit behind
                  `origin/base` and whose branch has merged `origin/base` in.
                  The survivor arm parts from the local spelling only there:
                  `survivor_check.py#parse_range` resolves `A...B` through
                  `git merge-base`, so the two spellings agree entirely until
                  HEAD already carries the base's newer commits
  structural      `broad_gate.py` reads `args.base` exactly once, and the
                  spelling it reaches for is held against the workflow's, so
                  the two readers cannot drift apart again in silence

`spec.md` §*User scenarios & acceptance* numbers the rows A1 to A12 and each
case below names the one it holds.
"""

import ast
import importlib.util
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")
HYGIENE = os.path.join(ROOT, ".github", "workflows", "hygiene.yml")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gate_module():
    return _load("specseal_broad_gate_for_range_tests", GATE)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


# --- fixtures: a repository that actually has a remote ----------------------
#
# Every gate fixture in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
# is built by a `git init` with no remote, which is why the fallback leaves
# almost all of that module alone (A3). It is NOT byte-identical: one
# assertion in `test_the_gate_with_record_seals_the_item_and_counts_its_rounds`
# reads the commit where it read the ref, because the consumers take the
# resolved commit even where the resolution lands on the ref as given
# (round 1, finding 3). A remote is new work, and it is built here rather than
# there so that one moved reading stays checkable by reading the diff.


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(repo, message):
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "commit",
        "-qm",
        message,
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def short(repo, rev):
    return git(repo, "rev-parse", "--short", f"{rev}^{{commit}}").stdout.strip()


def upstream_repo(d, content="# the first tree\n"):
    """A repository on branch `base`, to be cloned from. Not bare: a commit
    made here is what moves the remote under a clone's feet."""
    d.mkdir(parents=True)
    git(d, "init", "-q", "-b", "base")
    write(d, "docs/first.md", content)
    commit(d, "base")
    return d


def clone(src, dst):
    """`dst`, cloned from `src`: a local `base` tracking `origin/base`."""
    subprocess.run(
        ["git", "clone", "-q", str(src), str(dst)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return dst


ITEM = "seal/specs/1700000000-a-fixture"
PASSING_TEST = "def test_ok():\n    assert True\n"
OVERVIEW = "# overview\n\n## Not verified\n\nnone — the fixture verifies nothing\n"
SUITE_ROW = f"{sys.executable} -m pytest -q -p no:cacheprovider tests"
CONFIG = (
    "# Repository config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n"
    f"| Broad gate | {SUITE_ROW} |\n"
)

# The sentence the branch replaces, and the copy of it that stays standing.
# They part in the middle, so the pair shares two runs of wording that do not
# touch — which is what `survivor_check.py#runs` counts as two independent
# pieces of evidence rather than one phrase written several ways.
REPLACED = (
    "# notes\n\nThe resolver reaches for the remote tracking ref because a "
    "runner holds no local branch to read.\n"
)
STANDING = (
    "# notes\n\nThe resolver reaches for the remote tracking ref and therefore "
    "a runner holds no local branch to read.\n"
)
REPLACEMENT = (
    "# notes\n\nWhich commit the merge is judged against decides what every "
    "check below was asked.\n"
)


def env_without_a_pull_request():
    """`chain_check` reads `GITHUB_EVENT_PATH` and `GITHUB_HEAD_REF` to decide
    draft against ready and to match a routing declaration. On a runner both
    are set and both describe the REAL pull request, so a fixture repository
    would be judged with this branch's own event."""
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    env["GH_PROMPT_DISABLED"] = "1"
    env["GH_NO_UPDATE_NOTIFIER"] = "1"
    return env


@pytest.fixture(autouse=True)
def _no_ambient_pull_request(monkeypatch):
    for name in ("GITHUB_EVENT_PATH", "GITHUB_HEAD_REF"):
        monkeypatch.delenv(name, raising=False)


def gate_upstream(d):
    """A repository the gate can run over, on branch `base`."""
    d.mkdir(parents=True)
    git(d, "init", "-q", "-b", "base")
    write(d, "tests/test_one.py", PASSING_TEST)
    write(d, "seal/config.md", CONFIG)
    write(d, f"{ITEM}/overview.md", OVERVIEW)
    write(d, "docs/first.md", "# the first tree\n\nNothing here moves.\n")
    commit(d, "base")
    return d


def behind_gate_repo(tmp_path, plant=False):
    """A clone whose local `base` is one commit behind `origin/base`, on a
    branch that has MERGED `origin/base` in.

    That merge is the whole condition. `survivor_check.py#parse_range`
    resolves `A...B` through `git merge-base`, so the local and the
    remote-tracking spelling give the same answer until HEAD already carries
    the base's newer commits — a fixture built from the ticket's wording,
    where a stale base *can only narrow the range*, would not reproduce the
    defect at all.

    With `plant`, the base's newer commit writes a sentence twice and the
    branch replaces one of the two copies. In the resolved range that is a
    removal with a survivor standing; in the stale range the sentence was
    never there to remove, so the replacement reads as wording this branch
    wrote."""
    up = gate_upstream(tmp_path / "up")
    work = clone(up, tmp_path / "work")
    if plant:
        write(up, "docs/moved.md", REPLACED)
        write(up, "docs/echo.md", STANDING)
    else:
        write(up, "docs/second.md", "# the tree moved\n\nA sibling landed.\n")
    commit(up, "a sibling merged while this branch was open")
    git(work, "fetch", "-q", "origin")
    git(work, "switch", "-qc", "feature")
    write(work, "README.md", "# a fixture\n")
    commit(work, "feature")
    git(
        work,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-edit",
        "origin/base",
    )
    if plant:
        write(work, "docs/moved.md", REPLACEMENT)
        commit(work, "the sentence the base carried, replaced")
    return work


def run_gate(repo, keep, *extra):
    return subprocess.run(
        [
            sys.executable,
            GATE,
            "--base",
            "base",
            "--root",
            str(repo),
            "--shape",
            "--keep-output",
            str(keep),
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        env=env_without_a_pull_request(),
    )


def asked(keep, name):
    """The `$ ` line `run` writes at the head of a kept output file — the
    command as the gate actually spelled it."""
    text = read(os.path.join(str(keep), f"{name}.txt"))
    first = text.splitlines()[0]
    assert first.startswith("$ "), first
    return first


def behind_clone(tmp_path):
    """A clone whose local `base` is one commit behind `origin/base`.

    The commit is made in the upstream and fetched, never pulled, so the two
    refs name different commits in the one checkout — which is the state
    2026-09-16 was found in.

    Returns the CLONE alone. Every caller works in it, and the upstream is
    still reachable from the clone's own remote for a case that ever needs to
    move the base again."""
    up = upstream_repo(tmp_path / "up")
    work = clone(up, tmp_path / "work")
    write(up, "docs/second.md", "# the tree moved\n")
    commit(up, "a sibling merged while this branch was open")
    git(work, "fetch", "-q", "origin")
    return work


# --- phase 1: the resolver --------------------------------------------------


def test_the_base_resolves_to_the_ref_the_checkout_says_it_tracks(tmp_path):
    """The rule's first step, and the measured case. `base@{upstream}` is
    `origin/base`, which is one commit ahead, and that is the commit every
    check has to be asked about."""
    work = behind_clone(tmp_path)
    mod = gate_module()
    base = mod.resolve_base(str(work), "base")
    assert base.given == "base"
    assert base.ref == "origin/base", f"resolved to {base.ref}"
    assert base.commit == short(work, "origin/base")
    assert base.given_commit == short(work, "base")
    assert base.commit != base.given_commit, "the fixture is not behind at all"
    assert base.moved is True


def test_the_base_resolves_to_origin_where_the_branch_tracks_nothing(tmp_path):
    """The rule's second step: `refs/remotes/origin/<base>`, the spelling
    `.github/workflows/hygiene.yml` uses literally. A checkout whose local
    branch declares no upstream still has the remote-tracking ref."""
    work = behind_clone(tmp_path)
    git(work, "branch", "--unset-upstream", "base")
    mod = gate_module()
    base = mod.resolve_base(str(work), "base")
    assert base.ref == "origin/base", f"resolved to {base.ref}"
    assert base.commit == short(work, "origin/base")


def test_what_the_branch_tracks_wins_over_origin_when_the_two_differ(tmp_path):
    """The order is not decoration. A clone whose base branch tracks a SECOND
    remote — a fork with an upstream — would compare against the fork's stale
    copy if `origin/` came first, and that is the defect class being repaired
    (`plan.md` §*Alternatives considered*)."""
    fork = upstream_repo(tmp_path / "fork")
    work = clone(fork, tmp_path / "work")
    other = upstream_repo(tmp_path / "other")
    # The second remote carries the branch that is actually ahead.
    write(other, "docs/second.md", "# the tree moved\n")
    commit(other, "the real base moved")
    git(work, "remote", "add", "other", str(other))
    git(work, "fetch", "-q", "other")
    git(work, "branch", "--set-upstream-to=other/base", "base")
    mod = gate_module()
    base = mod.resolve_base(str(work), "base")
    assert base.ref == "other/base", (
        f"origin won over the declared upstream: {base.ref}"
    )
    assert base.commit == short(work, "other/base")
    assert base.commit != short(work, "origin/base")


def test_a_base_with_no_remote_counterpart_resolves_to_itself(tmp_path):
    """A8. A remote is present and the base is absent from it — the
    never-pushed branch. It resolves to the ref as given and `moved` is
    false, so nothing is printed about the resolution.

    **What the consumers are HANDED still moves**, and this is the fixture
    that sentence is about: `base.commit` is the ref's commit, where every
    check used to be handed `args.base` itself (round 1, finding 3). This
    docstring said *nothing about that run changes* until round 2 ran the
    fixture and found the children holding a hash."""
    work = behind_clone(tmp_path)
    git(work, "switch", "-qc", "never-pushed", "base")
    mod = gate_module()
    base = mod.resolve_base(str(work), "never-pushed")
    # These two already pin what the docstring above now says: the ref is the
    # branch name and the commit is its hash, so the consumers cannot be
    # holding the ref. Round 2's paste-ready fix added a third assertion,
    # `base.commit != base.ref`, and it was measured UNREACHABLE — the
    # mutation that hands the consumers the ref stops at the line above it, so
    # the extra line could never fail. A check that cannot fail is the
    # counterfeit `skills/verify/SKILL.md` §*The Seal Test* names, and this
    # work item already carries one finding about planting one.
    assert base.ref == "never-pushed", f"resolved to {base.ref}"
    assert base.commit == short(work, "never-pushed")
    assert base.moved is False


def test_a_bare_commit_sha_is_used_as_given(tmp_path):
    """A9. `<sha>@{upstream}` and `refs/remotes/origin/<sha>` both fail to
    resolve, and neither may abort the run."""
    work = behind_clone(tmp_path)
    sha = short(work, "base")
    mod = gate_module()
    base = mod.resolve_base(str(work), sha)
    assert base.ref == sha, f"a bare SHA resolved to {base.ref}"
    assert base.commit == sha
    assert base.moved is False


def test_a_repository_with_no_remote_at_all_resolves_to_the_ref_as_given(tmp_path):
    """The fallback A3 rests on. Every gate fixture in the suite today is
    exactly this repository, so the answer here is what keeps all but one
    assertion of `tests/test_the_seal_is_taken_once_by_the_sealer.py` reading
    as it did. What still moves there is the spelling the consumers get, which
    is round 1's finding 3."""
    d = upstream_repo(tmp_path / "solo")
    mod = gate_module()
    base = mod.resolve_base(str(d), "base")
    assert base.ref == "base"
    assert base.commit == short(d, "base")
    assert base.moved is False


def test_a_base_that_resolves_nowhere_comes_back_with_no_commit(tmp_path):
    """A10's half inside the resolver. The refusal itself is `gate()`'s and
    has to quote the spelling the caller typed, so the resolver hands back
    that spelling with no commit rather than raising."""
    d = upstream_repo(tmp_path / "solo")
    mod = gate_module()
    base = mod.resolve_base(str(d), "no-such-ref")
    assert base.given == "no-such-ref"
    assert base.commit is None
    assert base.given_commit is None


def test_a_linked_worktree_reads_the_same_remote_tracking_refs(tmp_path):
    """A12. Remote-tracking refs and branch tracking config live in the common
    git directory, so a worktree answers as the main checkout does — and the
    sealer runs from a worktree in this repository's own flow, which is why
    the claim is worth a case rather than a sentence."""
    work = behind_clone(tmp_path)
    linked = tmp_path / "linked"
    git(work, "worktree", "add", "-q", "--detach", str(linked), "base")
    try:
        mod = gate_module()
        base = mod.resolve_base(str(linked), "base")
        assert base.ref == "origin/base", f"resolved to {base.ref}"
        assert base.commit == short(work, "origin/base")
        assert base.moved is True
    finally:
        git(work, "worktree", "remove", "--force", str(linked))


# --- phase 2: gate() resolves once, and every consumer takes the commit -----


def test_every_check_is_handed_the_commit_the_remote_tracking_ref_names(tmp_path):
    """A1. The three checks that take a base on the command line are read out
    of the files the gate keeps, which is where the command it actually spelled
    is written down."""
    work = behind_gate_repo(tmp_path)
    keep = tmp_path / "out"
    out = run_gate(work, keep)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    resolved = short(work, "origin/base")
    stale = short(work, "base")
    assert resolved != stale, "the fixture is not behind at all"
    for name in ("unverified", "chain", "survivors"):
        line = asked(keep, name)
        assert resolved in line, f"{name} was not asked about {resolved}: {line}"
        assert stale not in line, f"{name} was asked about the local ref: {line}"


def test_the_survivor_arm_reports_what_ci_reports(tmp_path):
    """A2. The measured case, end to end. The base's newer commit wrote one
    sentence in two files, the branch merged that commit in and replaced one
    copy, and the other copy is still standing — which is what CI reported
    seven of on 2026-09-16 while the gate reported two, all excused, and drew
    the stamp."""
    work = behind_gate_repo(tmp_path, plant=True)
    keep = tmp_path / "out"
    out = run_gate(work, keep)
    assert out.returncode == 1, (
        f"the gate sealed a branch the same check refuses at CI:\n"
        f"{out.stdout}\n{out.stderr}"
    )
    assert "NOT SEALED" in out.stdout, out.stdout
    assert "survivors" in out.stdout, out.stdout
    assert "docs/echo.md" in read(os.path.join(str(keep), "survivors.txt"))


def test_the_gate_reads_the_given_base_exactly_once(tmp_path):
    """The closure is structural rather than a list. `spec.md` §*The class,
    enumerated by construction* names six consumers of `args.base`; counting
    the reads is what stops a seventh, written later, from taking the
    unresolved value without this count going red."""
    parsed = ast.parse(read(GATE))
    reads = [
        node
        for node in ast.walk(parsed)
        if isinstance(node, ast.Attribute)
        and node.attr == "base"
        and isinstance(node.value, ast.Name)
        and node.value.id == "args"
    ]
    assert len(reads) == 1, (
        f"`args.base` is read {len(reads)} times in broad_gate.py; after the "
        "resolution it is read once, at the resolution"
    )


# --- phase 3: the gate says what it compared against ------------------------


def level_gate_repo(tmp_path):
    """A clone whose local `base` and `origin/base` name the same commit —
    the ordinary checkout, where resolving changes nothing."""
    up = gate_upstream(tmp_path / "up")
    work = clone(up, tmp_path / "work")
    git(work, "switch", "-qc", "feature")
    write(work, "README.md", "# a fixture\n")
    commit(work, "feature")
    return work


def test_a_base_that_agrees_with_its_remote_prints_nothing_extra(tmp_path):
    """A4. A line printed on every run is a line people learn to skip, so the
    absence is asserted rather than left to be noticed."""
    work = level_gate_repo(tmp_path)
    out = run_gate(work, tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert "CI reads" not in out.stderr, (
        f"the moved-line printed over a base that had not moved:\n{out.stderr}"
    )


def test_a_base_behind_its_remote_says_so_with_both_refs_and_the_distance(tmp_path):
    """A5. All four values and how far apart they are, in one line, and the
    run continues — `plan.md` §*Alternatives considered* rejected the refusal
    because its only repair is a fetch and a second nine-minute gate."""
    work = behind_gate_repo(tmp_path)
    out = run_gate(work, tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    line = [ln for ln in out.stderr.splitlines() if "CI reads" in ln]
    assert len(line) == 1, f"expected one moved-line:\n{out.stderr}"
    said = line[0]
    for value in (
        "base",
        short(work, "base"),
        "origin/base",
        short(work, "origin/base"),
    ):
        assert value in said, f"the line does not name {value!r}: {said}"
    assert "1 ahead" in said and "0 behind" in said, said


def test_a_base_with_no_local_commit_at_all_is_told_so_and_runs(tmp_path):
    """The moved-line's second filling. A clone that never made a local branch
    for its base is an ordinary checkout, and it used to be exit 2 here —
    resolving silently would be the defect this work item is about."""
    up = gate_upstream(tmp_path / "up")
    work = clone(up, tmp_path / "work")
    git(work, "switch", "-qc", "feature")
    write(work, "README.md", "# a fixture\n")
    commit(work, "feature")
    git(work, "branch", "-qD", "base")
    out = run_gate(work, tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    said = "\n".join(ln for ln in out.stderr.splitlines() if "CI reads" in ln)
    assert "names no commit in this checkout" in said, out.stderr
    assert short(work, "origin/base") in said, said


def test_the_panel_names_the_ref_the_base_came_from(tmp_path):
    """A6, over `panel`'s rows and over what a reader actually sees.
    `seal_stamp.letter` cuts a value at the frame, so rows alone would not
    show that the ref survives the rendering."""
    mod = gate_module()
    base = mod.Base("base", "aaaaaaa", "origin/base", "bbbbbbb")
    checks = {
        name: mod.Check(name, 0, "1 passed in 0.1s", "out.txt")
        for name in (mod.SUITE, mod.LEDGER, mod.CHAIN_NAME)
    }
    rows = mod.panel("ccccccc", base, checks, None)
    assert ("base", "bbbbbbb") in rows, rows
    assert ("from", "origin/base") in rows, rows

    work = behind_gate_repo(tmp_path)
    out = run_gate(work, tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert re.search(r"\bfrom\s+[^\n|]*origin/base", out.stdout), (
        f"the rendered panel does not carry the ref:\n{out.stdout}"
    )


def test_the_failure_form_names_the_base_the_checks_were_asked_about(tmp_path):
    """A7. `NOT SEALED <tree> against <base>` is what a reader meets on a red
    run, and it carries the same base the panel would have."""
    work = behind_gate_repo(tmp_path, plant=True)
    out = run_gate(work, tmp_path / "out")
    assert out.returncode == 1, f"{out.stdout}\n{out.stderr}"
    head = out.stdout.splitlines()[0]
    assert head.startswith("NOT SEALED"), head
    assert short(work, "origin/base") in head, head
    assert short(work, "base") not in head, (
        f"the failure form names the local ref: {head}"
    )


# --- phase 4: the two readers, held against each other ----------------------
#
# The defect was not a bug inside either file. It was two files answering one
# question differently, each correct on its own, with nothing in the tree
# comparing them. `tests/test_the_lenient_run_says_what_the_broad_gate_will_
# say.py` was written for #354's identical shape — three readers grading one
# tree — and its structural half is the precedent this follows.

# Every place the workflow names a base, not only the ones spelled as a
# quoted argument at the start of a line. The value may be quoted or bare,
# and a bare one can carry a `${{ … }}` expression with spaces inside it, so
# the unquoted alternative treats such an expression as part of one token.
# An `env:` assignment counts: `.github/workflows/hygiene.yml` already names
# a base that way at its milestone step, and a `run:` block reading `$BASE`
# is as much a reader of the base as one spelling it on a command line.
BASE_ARGUMENT = re.compile(
    r"(?:--baseline|--range)\s+(?:\"([^\"]*)\"|((?:\$\{\{[^}]*\}\}|\S)+))"
)
BASE_ENVIRONMENT = re.compile(r"^\s*BASE:\s*(\S.*?)\s*$")
# A step that passes the base through a shell variable names the `env:`
# assignment, which this reader checks on its own — requiring the
# remote-tracking spelling here as well would turn the case red for a
# refactor that left the workflow correct.
SHELL_VARIABLE = re.compile(r'^"?\$\{?BASE\}?"?$')
REMOTE_TRACKING = "origin/${{ github.base_ref }}"


def base_spellings(text):
    """Every revision `text` names as a base, as it spells it.

    Takes text rather than reading the file, so the reader itself can be
    driven over shapes the workflow does not happen to use today — round 1's
    finding 4 was that a reader nothing drives is a reader nobody can tell is
    partial.
    """
    found = []
    for line in text.splitlines():
        for match in BASE_ARGUMENT.finditer(line):
            found.append(match.group(1) or match.group(2))
        environment = BASE_ENVIRONMENT.match(line)
        if environment:
            found.append(environment.group(1))
    return found


def workflow_base_arguments():
    """Every revision the hygiene workflow names as a base.

    A substring search for the remote-tracking spelling stays green while a
    fourth base-taking step is added without it, because the earlier three
    still carry the string — so each occurrence is read on its own.
    """
    found = base_spellings(read(HYGIENE))
    assert found, "the hygiene workflow names no base at all"
    return found


def test_the_gate_reaches_for_the_spelling_the_workflow_uses(tmp_path):
    """A11. The gate and CI are two readers of one question, and this is what
    keeps them from drifting apart in silence again.

    Red from either side: edit the workflow to drop `origin/` and the first
    half fails; edit the resolver to stop naming the remote-tracking ref, or
    to stop being called at all, and the rest does."""
    for argument in workflow_base_arguments():
        if SHELL_VARIABLE.match(argument):
            continue
        assert argument.startswith(REMOTE_TRACKING), (
            f"the workflow no longer asks about the remote-tracking ref: "
            f"{argument!r}. A runner's checkout has no local branch, so this "
            "is the only spelling that resolves there — if it moved, the gate "
            "has to move with it"
        )

    mod = gate_module()
    assert mod.REMOTE_LABEL == "origin/{ref}", mod.REMOTE_LABEL
    assert mod.REMOTE_BASE.endswith(mod.REMOTE_LABEL), (
        f"the gate's fallback {mod.REMOTE_BASE!r} is not the workflow's "
        f"{mod.REMOTE_LABEL!r} under a full ref path"
    )
    assert REMOTE_TRACKING.startswith(mod.REMOTE_LABEL.format(ref="")), (
        f"the workflow spells the base {REMOTE_TRACKING!r} and the gate "
        f"reaches for {mod.REMOTE_BASE!r}"
    )
    # Formatted, not as written: the template doubles its braces to survive
    # `str.format`, so the literal it holds is `{ref}@{{upstream}}` and only
    # the filled value is the revision git is actually asked for.
    assert mod.UPSTREAM_BASE.format(ref="base") == "base@{upstream}", mod.UPSTREAM_BASE

    called = [
        node
        for node in ast.walk(ast.parse(read(GATE)))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "resolve_base"
    ]
    assert len(called) == 1, (
        f"`resolve_base` is called {len(called)} times in broad_gate.py; the "
        "spelling above is only the workflow's while the gate still reaches "
        "for it"
    )


# --- phase 5: the documents say which base, and go red if they stop ---------

SEALER = os.path.join(ROOT, "agents", "sealer.md")
VERIFY = os.path.join(ROOT, "skills", "verify", "SKILL.md")

# Each document needs ONE block carrying both halves — that the base is
# resolved, and what it is resolved TO. A mention of `origin/` in a table
# three hundred lines from the sentence about the base is not the fact stated;
# `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`'s
# §*no document describes the lenient reader alone* is the precedent.
#
# `broad_gate.py` is NOT in this list and is checked below instead. Its
# `REMOTE_BASE` and `UPSTREAM_BASE` constants sit in one block and carry both
# words between them, so a whole-file block walk passes on the code whatever
# the docstring says — a check that cannot fail, which is the counterfeit
# `skills/verify/SKILL.md` §*The Seal Test* is about. Measured: deleting the
# docstring's paragraph left this case green.
DESCRIBES_THE_BASE = (SEALER, VERIFY)


def says_what_the_base_resolves_to(text):
    """True where one block of `text` carries both halves of the fact."""
    return any("origin/" in b and "upstream" in b for b in text.split("\n\n"))


def test_the_block_reader_can_fail():
    """The reader above, driven both ways, so the cases that use it are not
    asserting something nothing can break."""
    assert says_what_the_base_resolves_to("resolved to origin/<base>, its upstream")
    assert not says_what_the_base_resolves_to("the base is the ref you typed")
    assert not says_what_the_base_resolves_to("origin/<base>\n\nits upstream")


def test_no_document_leaves_the_base_reading_as_the_ref_you_typed():
    """§14. The resolution is a change to what a person reads — the sealer
    passes the base, and the panel and the printed line are read by whoever
    doubts a seal. A document that still describes the base as the ref as
    typed is a false sentence, and this is what makes that red rather than
    quiet."""
    missing = [
        os.path.relpath(path, ROOT)
        for path in DESCRIBES_THE_BASE
        if not says_what_the_base_resolves_to(read(path))
    ]
    assert not missing, (
        f"these describe the gate's base without saying what it resolves to: {missing}"
    )


def test_the_gates_own_docstring_says_the_base_is_resolved():
    """The interface a reader meets before the code. Read as the module's
    docstring rather than as the file, because the file also holds the
    constants that name the same refs and would answer for it."""
    doc = ast.get_docstring(ast.parse(read(GATE)))
    assert doc, "broad_gate.py has no module docstring"
    assert says_what_the_base_resolves_to(doc), (
        "the gate's docstring describes the base without saying what it "
        f"resolves to:\n{doc}"
    )


def test_the_documents_name_the_panel_row_the_gate_actually_prints():
    """The `from` row is the half of the stamp a reader uses to tell a fresh
    base from a stale one, so the agent that reports the stamp has to know it
    is there."""
    said = read(SEALER)
    assert "`from`" in said, "agents/sealer.md does not name the panel's ref row"
    mod = gate_module()
    base = mod.Base("base", "aaaaaaa", "origin/base", "bbbbbbb")
    checks = {
        name: mod.Check(name, 0, "1 passed in 0.1s", "out.txt")
        for name in (mod.SUITE, mod.LEDGER, mod.CHAIN_NAME)
    }
    labels = [row[0] for row in mod.panel("ccccccc", base, checks, None) if row]
    assert "from" in labels, f"the panel has no such row: {labels}"


# --- round 1, finding 2: the line may not speak for CI about a second remote


def a_clone_tracking_a_second_remote(tmp_path):
    """A clone whose `base` was retargeted to a second remote while
    `origin/base` still exists at a different commit — a fork with an
    upstream, which is the case `plan.md` §*Alternatives considered* puts step
    1 of the rule first for."""
    fork = upstream_repo(tmp_path / "fork")
    work = clone(fork, tmp_path / "work")
    other = upstream_repo(tmp_path / "other")
    write(other, "docs/second.md", "# the tree moved\n")
    commit(other, "the real base moved")
    git(work, "remote", "add", "other", str(other))
    git(work, "fetch", "-q", "other")
    git(work, "branch", "--set-upstream-to=other/base", "base")
    return work


def test_the_line_does_not_claim_ci_reads_a_second_remote(tmp_path):
    """The gate prefers what the checkout says the base tracks, and that can
    be a remote CI never reads: every base-taking step of the workflow spells
    `origin/<base>`. The line may say what resolving found; it may not say a
    runner reads it. `agents/sealer.md` has the sealer quote this line, so a
    false sentence here is a false sentence in a report."""
    work = a_clone_tracking_a_second_remote(tmp_path)
    mod = gate_module()
    said = mod.moved_line(str(work), mod.resolve_base(str(work), "base"))
    assert "other/base" in said, said
    assert "CI reads other/base" not in said, (
        f"the line speaks for CI about a remote no runner has: {said}"
    )
    assert "origin/base" in said, f"the runner's own spelling is missing: {said}"


def test_the_line_still_speaks_for_ci_where_the_two_agree(tmp_path):
    """The other direction, so the branch above cannot be satisfied by never
    mentioning CI at all. An ordinary clone tracks `origin/<base>`, which is
    exactly what a runner reads."""
    work = behind_clone(tmp_path)
    mod = gate_module()
    said = mod.moved_line(str(work), mod.resolve_base(str(work), "base"))
    assert "CI reads origin/base" in said, said


def test_the_distance_says_what_it_is_measured_against(tmp_path):
    """Finding 7. `1 ahead, 0 behind` names no subject, and both refs are in
    the sentence."""
    work = behind_clone(tmp_path)
    mod = gate_module()
    said = mod.moved_line(str(work), mod.resolve_base(str(work), "base"))
    assert "origin/base is 1 ahead and 0 behind base" in said, (
        f"the counts name nothing they are relative to: {said}"
    )


# --- round 1, finding 6: `@{upstream}` is a suffix on any revision ----------


def test_a_revision_that_is_not_a_branch_does_not_take_a_branchs_upstream(tmp_path):
    """`{given}@{{upstream}}` builds from any revision expression, so
    `HEAD@{upstream}` answers for the CURRENT branch rather than for what
    `--base` named. The rule is about what a BRANCH tracks, so step 1 is
    asked only of a branch."""
    work = behind_clone(tmp_path)
    git(work, "switch", "-qc", "topic")
    git(work, "branch", "--set-upstream-to=origin/base", "topic")
    write(work, "README.md", "# the topic moved ahead\n")
    commit(work, "topic")
    mod = gate_module()
    base = mod.resolve_base(str(work), "HEAD")
    # Two instances, one cause. Guarding step 1 alone moved the defect down a
    # step: a clone creates `refs/remotes/origin/HEAD`, so `--base HEAD` then
    # resolved to `origin/HEAD` instead. Both are asserted, because the first
    # fix was measured passing this case's first half while failing here.
    assert base.ref != "origin/HEAD", "step 2 took a ref that is not a branch"
    assert base.ref == "HEAD", f"`--base HEAD` resolved to {base.ref}"
    assert base.commit == short(work, "HEAD"), base.commit
    assert base.moved is False


def test_a_bare_sha_does_not_take_a_branchs_upstream(tmp_path):
    """A9 by the same mechanism, and the one the guard must not break: a
    commit is not a branch, so step 1 never applies to it."""
    work = behind_clone(tmp_path)
    git(work, "branch", "--set-upstream-to=origin/base", "base")
    sha = short(work, "base")
    mod = gate_module()
    base = mod.resolve_base(str(work), sha)
    assert base.ref == sha, f"a bare SHA resolved to {base.ref}"
    assert base.moved is False


# --- round 1, finding 4: the reader saw three of the workflow's shapes ------

# The six spellings round 1 drove the old pattern over. Three were invisible
# to it, and one of those three — the `BASE:` assignment — is not
# hypothetical: `.github/workflows/hygiene.yml` already spells a base that
# way, and `plan.md` §*Technical context* counts that line among the four
# base-taking steps. So the pin covered three of the four the plan enumerates
# while `phases/phase-4.md` and the changelog claimed all of them.
WORKFLOW_SHAPES = [
    (
        '            --baseline "origin/${{ github.base_ref }}" seal/specs/',
        "origin/${{ github.base_ref }}",
    ),
    (
        '          python3 x.py --baseline "origin/${{ github.base_ref }}" specs/',
        "origin/${{ github.base_ref }}",
    ),
    (
        "            --baseline origin/${{ github.base_ref }}",
        "origin/${{ github.base_ref }}",
    ),
    ('            --baseline "$BASE"', "$BASE"),
    ("          BASE: origin/${{ github.base_ref }}", "origin/${{ github.base_ref }}"),
    (
        '            --range "origin/${{ github.base_ref }}...HEAD" ${exempt[@]+"${exempt[@]}"}',
        "origin/${{ github.base_ref }}...HEAD",
    ),
]


def test_the_workflow_reader_sees_every_shape_a_base_is_spelled_in():
    """Finding 4. The flag on its own continuation line, the flag on the same
    line as its command, the value unquoted, a shell variable, an `env:`
    assignment, and a range. A reader that sees only the first shape passes
    while a step added in any of the others goes unread."""
    for line, expected in WORKFLOW_SHAPES:
        found = base_spellings(line)
        assert found == [expected], f"{line!r} was read as {found}"


def test_the_workflow_reader_finds_the_env_assignment_the_file_already_has():
    """The `BASE:` shape, over the real file rather than over a sample — it is
    the one the plan counts and the old pattern could not see."""
    found = workflow_base_arguments()
    assert len(found) >= 4, f"the workflow names {len(found)} bases: {found}"
    assert any(spelling == REMOTE_TRACKING for spelling in found), (
        f"no bare `{REMOTE_TRACKING}` among {found} — the `BASE:` assignment is unread"
    )


# --- round 1, finding 5: the `from` row was cut with no marker --------------

STAMP = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")


def stamp_module():
    return _load("specseal_seal_stamp_for_range_tests", STAMP)


def panel_of(mod, ref, given="release/x"):
    base = mod.Base(given, "aaaaaaa", ref, "bbbbbbb")
    checks = {
        name: mod.Check(name, 0, "1 passed in 0.1s", "out.txt")
        for name in (mod.SUITE, mod.LEDGER, mod.CHAIN_NAME)
    }
    return dict(row for row in mod.panel("ccccccc", base, checks, None) if row)


def test_the_panel_value_width_is_what_the_stamp_actually_gives():
    """Two statements of one fact, and neither may move without the other
    going red. `broad_gate` has to know where the frame cuts in order to
    elide before it, and `seal_stamp.letter` is what decides — measured here
    by rendering a value nothing could fit rather than by restating the
    formula."""
    rendered = stamp_module().letter([("from", "x" * 200)])[2]
    assert rendered.count("x") == gate_module().PANEL_VALUE_WIDTH, (
        f"the panel gives a value {rendered.count('x')} columns and "
        f"broad_gate elides at {gate_module().PANEL_VALUE_WIDTH}"
    )


def test_a_ref_too_long_for_the_panel_says_it_was_cut(tmp_path):
    """A6, and round 1's finding 5. `seal_stamp.letter` cuts at the frame with
    no ellipsis, and A4 means nothing prints beside the row on an agreeing
    run — so a ref that does not fit has to say so in the row itself. The
    tail is kept, because for the `origin/<base>` a runner reads the prefix is
    the part a reader can infer and the branch name is not. Where step 1 lands
    on a second remote the prefix is not inferable, which is round 1's finding
    2 and the cost `panel`'s docstring now states."""
    mod = gate_module()
    long_ref = "origin/release/2026-09-21-hotfix"
    assert len(long_ref) > mod.PANEL_VALUE_WIDTH, "the fixture ref already fits"
    shown = panel_of(mod, long_ref)["from"]
    assert shown != long_ref[: len(shown)], f"the ref was cut with no marker: {shown!r}"
    assert shown.endswith("hotfix"), shown
    rendered = stamp_module().letter([("from", shown)])[2]
    assert "hotfix" in rendered, f"the marker cost the tail its place: {rendered!r}"


def test_a_ref_that_fits_is_left_exactly_as_it_is(tmp_path):
    """The other direction. This repository's own release refs are 22 columns
    and fit, which is why no case caught the cut — so the elision must not
    start marking refs that were never in danger."""
    mod = gate_module()
    for ref in ("origin/base", "origin/release/v0.12.2"):
        assert panel_of(mod, ref)["from"] == ref, ref


# --- #461: the line may not name a ref no runner's checkout can hold --------


def a_checkout_whose_previous_branch_is_the_base(tmp_path):
    """A clone whose local `base` is one commit behind `origin/base`, sitting
    on a second branch that was switched to FROM `base`. `@{-1}` therefore
    names the base, and `--base @{-1}` resolves through step 1 of the rule."""
    work = behind_clone(tmp_path)
    git(work, "switch", "-qc", "topic")
    git(work, "switch", "-q", "base")
    git(work, "switch", "-q", "topic")
    return work


def test_the_guard_states_the_property_the_command_actually_has(tmp_path):
    """A1, and the measurement behind it. `check-ref-format --branch` EXPANDS
    `@{-N}` and then checks what it expanded to, so `@{-1}` is accepted while
    `HEAD`, `HEAD~1`, `base@{u}` and `topic@{1}` are refused. The docstring
    used to state the class `@{…}`, which is not the class the command
    refuses (round 2, finding 10)."""
    work = a_checkout_whose_previous_branch_is_the_base(tmp_path)
    mod = gate_module()
    assert mod.names_a_branch(str(work), "@{-1}") is True, (
        "the command no longer expands `@{-N}`, so A1's docstring is stale"
    )
    for refused in ("HEAD", "HEAD~1", "base@{u}", "topic@{1}"):
        assert mod.names_a_branch(str(work), refused) is False, refused
    doc = mod.names_a_branch.__doc__
    assert "@{-1}" in doc, "the docstring does not name the spelling it accepts"


def test_the_line_does_not_name_a_ref_a_runners_checkout_cannot_hold(tmp_path):
    """A2, and #461's second half. The runner label built out of `@{-1}` is
    `origin/@{-1}`, which git refuses as a refname — so no runner's checkout
    holds one and the line may not name it as the ref a runner reads.

    Seen red against the shipped line, which round 2's finding 10 quotes
    whole: *— not the origin/@{-1} a runner reads —*. `agents/sealer.md` has
    the sealer quote this line verbatim into a report, which is why the
    assertion is on the printed sentence and not on the guard behind it."""
    work = a_checkout_whose_previous_branch_is_the_base(tmp_path)
    mod = gate_module()
    base = mod.resolve_base(str(work), "@{-1}")
    assert base.ref == "origin/base", f"the fixture did not resolve: {base.ref}"
    assert base.moved is True, "the fixture prints no line at all"
    said = mod.moved_line(str(work), base)
    assert "origin/@{-1}" not in said, (
        f"the line names a ref no runner's checkout can hold: {said}"
    )
    assert "a runner reads" not in said, (
        f"the line still speaks for a runner about that spelling: {said}"
    )
    assert "a runner's checkout has no counterpart for @{-1}" in said, (
        f"the line says nothing about why the runner clause is absent: {said}"
    )
    assert "origin/base, which is" in said, (
        f"the line stopped saying what this checkout resolved to: {said}"
    )
