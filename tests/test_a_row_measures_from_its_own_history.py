"""A ledger row's drift baseline comes from `git blame`, not from a stamp.

Issue #52. A stamp is a SHA typed into the row by hand, and there is no commit
a feature branch can type that is both reachable after the squash and current
with its coordinates. Stamp the base and the row reads DRIFTED at birth; stamp
the branch and the squash orphans it. #48 merged, `9b5501d` stopped existing,
seven rows pointed at it, and #49 repaired them one cell at a time.

Blame has no such choice to make. The answer is computed on the tree as it
stands, so after a squash it names the squash commit — which is exactly the
value that repair wrote in by hand. `test_a_squash_does_not_orphan_the_baseline`
builds that merge and measures it.

Two things this file also pins, because both are how the fallback goes quiet:

  the stamp still wins  a row written under the old rule keeps measuring from
                        the SHA it wrote, or every stamped row in this
                        repository silently changes meaning
  a fragment is checked `.specseal/map/<work-item>.md` carries no baseline
                        header. Before blame that meant "drift check skipped",
                        which is a pass nobody asked for
"""

import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    return " ".join(read(*parts).split())


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def git(d, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(d), *args],
        check=check,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def head(d):
    return git(d, "rev-parse", "HEAD").stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """`src/service.py` with eight lines, committed, on `main`."""
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    git(d, "init", "-q", "-b", "main")
    git(d, "config", "user.email", "t@example.com")
    git(d, "config", "user.name", "t")
    (d / "src" / "service.py").write_text("".join(f"line{i}\n" for i in range(1, 9)))
    git(d, "add", "-A")
    git(d, "commit", "-qm", "base")
    return d


def fragment(d, body, name="core.md"):
    """A ledger fragment with NO baseline header, committed."""
    (d / ".specseal" / "map").mkdir(parents=True, exist_ok=True)
    (d / ".specseal" / "map" / name).write_text("# " + name + "\n\n" + body)
    git(d, "add", "-A")
    git(d, "commit", "-qm", "ledger row")


def test_a_fragment_with_no_header_is_checked_rather_than_skipped(repo):
    """The header baseline is what a fragment does not have.

    `find_baseline` scans the first 2000 characters for a resolvable SHA and a
    fragment carries none, so before blame every row in one measured from
    nothing at all — reported as `drift check skipped`, printed once, and
    counted as OK.
    """
    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")

    r = run(["."], str(repo))
    assert "drift check skipped" not in r.stdout, r.stdout
    assert "DRIFTED" in r.stdout, r.stdout
    assert r.returncode == 1, r.stdout


def test_an_untouched_coordinate_stays_ok(repo):
    """The other direction, or the case above passes by drifting everything."""
    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    r = run(["."], str(repo))
    assert "DRIFTED" not in r.stdout, r.stdout
    assert "1 ok" in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout


def test_the_stamp_still_wins_where_a_row_wrote_one(repo):
    """A row stamped under the old rule must not change meaning.

    The row here names the FIRST commit and its line was written later, so
    blame and the stamp disagree — and only the stamp reaches back past the
    edit to `src/service.py`. If blame won, the row would read OK and the
    drift the stamp is preserving would disappear.
    """
    base = head(repo)
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")
    fragment(repo, f"| POL-1 | `src/service.py:2` | 2026-01-01 `{base}` |\n")

    r = run(["."], str(repo))
    assert "DRIFTED" in r.stdout, r.stdout
    assert base[:9] in r.stdout, r.stdout


def test_an_uncommitted_ledger_line_falls_back_to_the_header(repo):
    """Blame calls a line nobody has committed the all-zero SHA.

    Using it would send `git diff 000..HEAD` at a commit that does not exist,
    and `changed_ranges` would answer "nothing changed" — a pass produced by a
    failure. The row falls back to the header baseline instead.
    """
    base = head(repo)
    (repo / ".specseal").mkdir(exist_ok=True)
    (repo / ".specseal" / "map.md").write_text(
        f"# map\n| Baseline commit | `{base}` |\n\n| POL-1 | `src/service.py:2` |\n"
    )
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")

    r = run(["."], str(repo))
    assert base[:9] in r.stdout, r.stdout
    assert "DRIFTED" in r.stdout, r.stdout


def test_a_squash_does_not_orphan_the_baseline(repo):
    """The whole point, built as the merge that broke it.

    A feature branch writes the row and the code together; the branch squashes
    into `main` and every commit it made stops being reachable. A stamp naming
    one of those commits is what #49 repaired by hand. Blame answers with the
    squash commit, which contains both the row and the code it cites, so the
    row reads OK on the merged tree with nobody touching it.
    """
    git(repo, "switch", "-q", "-c", "feature")
    (repo / "src" / "service.py").write_text("".join(f"new{i}\n" for i in range(1, 9)))
    git(repo, "commit", "-qam", "change the code")
    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    branch_tip = head(repo)

    git(repo, "switch", "-q", "main")
    git(repo, "merge", "-q", "--squash", "feature")
    git(repo, "commit", "-qm", "squashed feature")
    git(repo, "branch", "-qD", "feature")

    assert (
        git(
            repo, "merge-base", "--is-ancestor", branch_tip, "HEAD", check=False
        ).returncode
        != 0
    ), "the fixture did not actually orphan the branch's commits"

    r = run(["."], str(repo))
    assert r.returncode == 0, r.stdout
    assert "1 ok" in r.stdout, r.stdout
    assert "drift check skipped" not in r.stdout, r.stdout


def test_a_cross_repo_coordinate_does_not_take_this_repos_blame(repo, tmp_path):
    """A commit of THIS repository is not a diff base in another checkout.

    Handing blame's answer to `git diff` in the mapped repo would either fail
    or, worse, resolve against an unrelated commit of the same name. The row
    falls back to the header baseline for that repo, which is what
    `--default-repo` and `--map` already establish.
    """
    other = tmp_path / "legacy"
    (other / "src").mkdir(parents=True)
    git(other, "init", "-q", "-b", "main")
    git(other, "config", "user.email", "t@example.com")
    git(other, "config", "user.name", "t")
    (other / "src" / "old.py").write_text("".join(f"line{i}\n" for i in range(1, 9)))
    git(other, "add", "-A")
    git(other, "commit", "-qm", "legacy base")

    fragment(repo, "| POL-1 | `legacy/src/old.py:2` |\n")
    r = run(["--map", f"legacy={other}", "."], str(repo))
    assert r.returncode == 0, r.stdout
    assert "1 ok" in r.stdout, r.stdout
    assert "EXTERNAL" not in r.stdout, r.stdout


def test_the_reader_is_still_the_one_the_stamp_test_calls(repo):
    """`tests/test_ledger_stamps_resolve.py` calls `row_baseline` with four
    positional arguments and asks only what the row WROTE.

    Adding blame behind that signature would make every stamped row answer
    with its blame commit there, and the case that checks stamp and reader
    agree would compare two different things and pass by accident.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    text = (repo / ".specseal" / "map" / "core.md").read_text()
    pos = text.index("POL-1")
    assert mod.row_baseline(text, pos, str(repo), {}) is None, (
        "the four-argument form gained a blame answer"
    )


def test_blame_drops_the_all_zero_sha(repo):
    """Read at the unit, because the integration case above can only show the
    fallback happening — not that the zero SHA was what was refused."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    with open(repo / ".specseal" / "map" / "core.md", "a", encoding="utf-8") as f:
        f.write("| POL-2 | `src/service.py:3` |\n")
    lines = mod.blame_lines(str(repo), ".specseal/map/core.md", {})
    assert lines, "blame answered for nothing at all"
    assert "0" * 40 not in lines.values()
    assert max(lines) < 5, (
        f"the uncommitted line got a baseline: {lines}. Blame reports it as "
        "the all-zero SHA, which resolves to no commit"
    )


def test_a_boundary_line_gets_a_baseline_git_can_resolve(repo):
    """Blame's default and `-s` forms decorate a boundary commit with `^`.

    Measured on this repository: `git blame -s HEAD -- .specseal/map.md`
    answers `^9829412` for every line reaching the walk's first commit, and
    `git cat-file -e ^9829412` rejects that name. Porcelain spells the same
    SHA plainly and puts `boundary` on a metadata line, which is why the
    format is not interchangeable.

    The first line of a fragment IS a boundary line — it reaches the commit
    that created the file — so this is the ordinary case, not a corner. What
    the row must get is a name git resolves.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    lines = mod.blame_lines(str(repo), ".specseal/map/core.md", {})
    assert lines, "blame answered for nothing at all"
    for n, sha in lines.items():
        assert not sha.startswith("^"), f"line {n} kept a boundary marker: {sha}"
        assert (
            git(repo, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode
            == 0
        ), f"line {n} got a baseline git cannot resolve: {sha}"


def test_a_baseline_that_does_not_resolve_is_refused(repo, monkeypatch):
    """The check sits where blame's answer leaves `row_baseline`, so a name
    from any format git might grow is refused rather than passed to
    `git diff` — where an unresolvable base answers "nothing changed", a pass
    produced by a failure."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    path = repo / ".specseal" / "map" / "core.md"
    text = path.read_text()
    monkeypatch.setattr(mod, "blame_lines", lambda *a, **k: {1: "^9829412", 3: "^dead"})
    assert (
        mod.row_baseline(
            text, text.index("POL-1"), str(repo), {}, ledger=str(path), root=str(repo)
        )
        is None
    ), "a decorated boundary name was handed on as a baseline"


# --- the documents ----------------------------------------------------------


def test_no_document_still_tells_a_session_to_stamp_a_sha():
    """The rule a session reads has to be the rule the checker runs.

    `CLAUDE.md` and the implement skill both described the dilemma issue #52
    is about — stamp the base and drift at birth, stamp the branch and break
    at the merge — as something the author has to steer between. There is
    nothing to steer now, and a document that still says there is sends the
    next session looking for a commit to type.
    """
    for parts in (
        ("CLAUDE.md",),
        ("skills", "implement", "SKILL.md"),
        ("agents", "smith.md"),
        ("templates", "map.md"),
        ("templates", "sdd-plan.md"),
    ):
        text = flat(*parts)
        assert (
            "stamp a `.specseal/map.md` row with a commit this branch made" not in text
        ), "/".join(parts) + " still forbids what nothing writes any more"
        assert "the HEAD SHA you read it at" not in text, (
            "/".join(parts) + " still asks for a SHA in the Checked column"
        )


def test_the_documents_say_where_the_baseline_comes_from_now():
    """Naming `git blame` is what makes the rule checkable by a reader. Two
    documents state it: the one always loaded, and the one a session bootstraps
    a ledger from."""
    for parts in (
        ("CLAUDE.md",),
        ("templates", "map.md"),
        ("skills", "implement", "SKILL.md"),
    ):
        assert "git blame" in flat(*parts), "/".join(parts) + " does not say"


def test_the_known_limit_is_written_down_where_the_rule_is():
    """Blame answers for the row's LINE, so re-wording a Notes cell moves the
    baseline with nobody re-reading the code. A rule that hides its own cost
    gets reverted by whoever finds it."""
    for parts in (("templates", "map.md"), ("skills", "evidence-check", "SKILL.md")):
        text = flat(*parts)
        assert "re-wording" in text or "re-worded" in text, (
            "/".join(parts) + " does not say what an unrelated edit to the row does"
        )
        assert "date" in text.lower()


def test_the_fragment_home_is_named_in_the_documents_that_instruct():
    """A convention nobody is told about is not a convention. These are the
    files a session opens to learn where evidence goes."""
    for parts in (
        (".specseal", "README.md"),
        ("templates", "specseal-README.md"),
        ("skills", "implement", "SKILL.md"),
        ("skills", "evidence-check", "SKILL.md"),
    ):
        assert "map/<work-item-id>.md" in read(*parts), (
            "/".join(parts) + " does not name the fragment a work item writes"
        )


def test_the_existing_ledger_says_what_it_now_is():
    """`.specseal/map.md` is not moved — the migration is incremental — so its
    own header is the only place a reader learns that new rows go elsewhere
    and that the header baseline is now a narrow fallback."""
    text = flat(".specseal", "map.md")
    assert "map/<work-item-id>.md" in text, (
        "the ledger does not send a new work item to a fragment"
    )
    assert "git blame" in text
    for stale in (
        "carries the date AND the commit SHA it was read at",
        "Rows without one fall back to the baseline above.",
    ):
        assert stale not in text, f"the header still states the old rule: {stale!r}"


def test_the_fragment_this_work_item_wrote_carries_no_header_and_no_stamp():
    """Dogfood. The convention is worth what the repository that wrote it
    actually does, and a fragment that quietly carried a baseline header would
    make every case above vacuous here."""
    frag = os.path.join(
        ROOT,
        ".specseal",
        "map",
        "1788229400-every-branch-appends-to-the-same-two-files.md",
    )
    assert os.path.isfile(frag), "this work item recorded no evidence at all"
    text = read(
        ".specseal", "map", "1788229400-every-branch-appends-to-the-same-two-files.md"
    )
    assert "Baseline commit" not in text, "a fragment carries no baseline header"
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        assert not re.search(r"\b\d{4}-\d{2}-\d{2}\s+`?[0-9a-f]{7,40}`?", line), (
            f"a row in the fragment still carries a stamped SHA: {line.strip()[:80]}"
        )
