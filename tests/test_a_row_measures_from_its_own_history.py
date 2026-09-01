"""A ledger row's drift baseline is derived from history, not typed into it.

Issue #52. A stamp is a SHA typed into the row by hand, and there is no commit
a feature branch can type that is both reachable after the squash and current
with its coordinates. Stamp the base and the row reads DRIFTED at birth; stamp
the branch and the squash orphans it. #48 merged, `9b5501d` stopped existing,
seven rows pointed at it, and #49 repaired them one cell at a time.

Deriving it has no such choice to make. The answer is computed on the history
in front of it, so after a squash it is the squash commit — exactly the value
that repair wrote in by hand. `test_a_squash_does_not_orphan_the_baseline`
builds that merge and measures it.

**First appearance, not last touch**, and that is the half a reader is most
likely to get wrong: last touch is what one `git blame` answers for free, and
it resets a row on any edit to its line. `test_a_bulk_rewrite_does_not_reset_a_row`
builds the commit that made the difference measurable.

Three more things this file pins, because each is how a derived baseline goes
quiet:

  the stamp still wins  a row written under the old rule keeps measuring from
                        the SHA it wrote, or every stamped row in this
                        repository silently changes meaning
  prose is not a stamp  a row about a commit names it, and that word used to
                        become the row's baseline — and the ledger's
  a fragment is checked `.specseal/map/<work-item>.md` carries no baseline
                        header. Before this that meant "drift check skipped",
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
    assert all(sha != "0" * 40 for sha, _ in lines.values()), lines
    assert max(lines) < 5, (
        f"the uncommitted line got an anchor: {lines}. Blame reports it as "
        "the all-zero SHA, which resolves to no commit"
    )


def test_a_bulk_rewrite_does_not_reset_a_row(repo):
    """The case that decided last touch against first appearance.

    A ledger's rows get rewritten en masse for reasons that re-read nothing —
    a release commit fixing stamps, a reformat, a merge-conflict resolution.
    Under last touch every row it touched takes that commit as its baseline
    and the drift window collapses to nothing. Measured on this repository's
    own ledger: one release commit held the baseline for 16 rows of 36 that
    way, and for none of them by first appearance.

    Here the rewrite is a re-worded Notes cell, which is the cheapest possible
    version of it — nobody opened the code — and the row still has to report
    the drift it had before.
    """
    fragment(repo, "| POL-1 | `src/service.py:2` | | | first wording |\n")
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")

    r = run(["."], str(repo))
    assert "DRIFTED" in r.stdout, f"the fixture never drifted:\n{r.stdout}"

    path = repo / ".specseal" / "map" / "core.md"
    path.write_text(path.read_text().replace("first wording", "second wording"))
    git(repo, "commit", "-qam", "re-word the notes cell, reading nothing")

    r = run(["."], str(repo))
    assert "DRIFTED" in r.stdout, (
        "re-wording the row cleared its drift — the baseline followed the "
        f"edit instead of the row's first appearance:\n{r.stdout}"
    )


def test_a_moved_row_would_lose_its_history(repo):
    """Why a migration carries every stamp forward verbatim.

    A migration is a PARTIAL move: `.specseal/map.md` stays and some of its
    rows go to a fragment. `git log -L` does not follow a row out of a file
    that stays, so in the fragment the row's history begins at the move — and
    a migration that stripped stamps would reset every window it touched in
    one commit that re-read nothing.

    The distinction is worth the fixture. A WHOLE-file move is a rename, which
    git detects and follows; the first version of this case did that by
    accident and the row's history came through intact. That is not the shape
    a migration has, and reading the rename result as the general one is how
    the stamp rule would get dropped as unnecessary.

    This is the grounds for the rule rather than a behaviour of the checker,
    which is why it asks git rather than `row_baseline`.
    """
    fragment(
        repo,
        "| POL-1 | `src/service.py:2` |\n| POL-2 | `src/service.py:3` |\n",
        name="old.md",
    )
    born = head(repo)

    old_map = repo / ".specseal" / "map" / "old.md"
    old_map.write_text(
        old_map.read_text().replace("| POL-1 | `src/service.py:2` |\n", "")
    )
    fragment(repo, "| POL-1 | `src/service.py:2` |\n", name="new.md")
    moved = head(repo)

    r = git(repo, "log", "-L", "3,3:.specseal/map/new.md", "--format=%H", "-s", "HEAD")
    shas = [line.strip() for line in r.stdout.splitlines() if len(line.strip()) == 40]
    assert shas and shas[-1] == moved, (
        f"git followed the row out of a file that stayed: {shas}, born {born}. "
        "If that is now true, the carry-the-stamp rule can be revisited"
    )
    assert born not in shas, born


def test_a_commit_named_in_a_rows_prose_is_not_its_baseline(repo):
    """Found by running the checker against this work item's own fragment.

    A row that carries no stamp used to hand its baseline to the first
    SHA-shaped word in the line that git could resolve. Rows write no stamp
    now, so every hex word in a row is prose — and a row explaining why the
    stamp went names commits, which is how that fragment came to measure from
    a commit resolvable in the clone that wrote it and nowhere else.

    A baseline is a date and a SHA together. Prose is not.
    """
    older = head(repo)
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")
    fragment(
        repo,
        f"| POL-1 | `src/service.py:2` | | | the commit {older} is discussed here |\n",
    )

    r = run(["."], str(repo))
    assert "DRIFTED" not in r.stdout, (
        f"the row measured from a commit its prose merely named:\n{r.stdout}"
    )
    assert "1 ok" in r.stdout, r.stdout


def test_a_commit_named_in_a_row_is_not_the_ledgers_baseline_either(repo):
    """The same word, read by the header scan instead.

    `find_baseline` reads the first 2000 characters, which reaches into the
    rows of any ledger shorter than that — so the prose above also became the
    whole file's declared baseline, and got printed as one. The header now
    ends above the first row that cites code, and a Baseline declaration cites
    none.
    """
    older = head(repo)
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")
    fragment(
        repo,
        f"| POL-1 | `src/service.py:2` | | | the commit {older} is discussed here |\n",
    )

    r = run(["."], str(repo))
    assert older[:9] not in r.stdout, (
        f"a commit named in a row became the ledger's baseline:\n{r.stdout}"
    )


def test_a_baseline_declared_in_the_header_is_still_read(repo):
    """The narrowing above must not cost the declaration it was narrowed
    around. `.specseal/map.md` declares its baseline in a table ROW, so a cut
    at the first table row would have thrown it away."""
    base = head(repo)
    (repo / ".specseal").mkdir(exist_ok=True)
    (repo / ".specseal" / "map.md").write_text(
        f"# map\n\n## Baseline\n\n| Item | Value |\n|---|---|\n"
        f"| Baseline commit | `{base}` |\n| Coordinate notation | `<path>:<line>` |\n\n"
        "| POL-1 | `src/service.py:2` |\n"
    )
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "map")
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")

    r = run(["."], str(repo))
    assert f"baseline: {base[:9]}" in r.stdout, r.stdout


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
    for n, (sha, _) in lines.items():
        assert not sha.startswith("^"), f"line {n} kept a boundary marker: {sha}"
        assert (
            git(repo, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode
            == 0
        ), f"line {n} got an anchor git cannot resolve: {sha}"


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
    monkeypatch.setattr(mod, "blame_lines", lambda *a, **k: {1: ("x", 1), 3: ("y", 3)})
    monkeypatch.setattr(mod, "first_appearance", lambda *a, **k: "^9829412")
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
    """A reader has to be able to check the rule, which means naming the
    reading. `first appeared` and `last touch` are two different rules with
    the same one-line summary, and the one-line summary is what a document
    that skips this ends up carrying."""
    for parts in (
        ("CLAUDE.md",),
        ("templates", "map.md"),
        ("skills", "evidence-check", "SKILL.md"),
    ):
        text = flat(*parts)
        assert "first appear" in text, (
            "/".join(parts) + " does not say WHICH commit of the row's history"
        )
        assert "last touch" in text, (
            "/".join(parts) + " does not say what was rejected, so the next "
            "reader takes the cheaper reading for the same rule"
        )


def test_the_reason_first_appearance_beats_last_touch_is_measured():
    """A rule with no number behind it gets reverted by whoever finds the
    cheaper implementation. The measurement is one release commit holding 16
    of 36 baselines one way and none the other."""
    for parts in (("templates", "map.md"), ("skills", "evidence-check", "SKILL.md")):
        text = flat(*parts)
        assert "16 rows of 36" in text or "16 of them" in text, (
            "/".join(parts) + " states the rule with no measurement behind it"
        )


def test_the_migration_rule_is_written_down_beside_the_ledger():
    """`git log -L` does not follow a line across a file boundary, so a row
    moved into a fragment with its stamp stripped would take the move as its
    baseline. Executed in `test_a_moved_row_would_lose_its_history`."""
    for parts in (("CLAUDE.md",), ("templates", "map.md"), (".specseal", "map.md")):
        text = flat(*parts)
        assert "does not follow a row out of a file that stays" in text, (
            "/".join(parts) + " does not say why a moved row keeps its stamp"
        )


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


def test_a_re_verified_row_can_clear_its_drift(repo):
    """The escape hatch the derivation needs, and the reason a stamp survives.

    A row whose cited code changed after the row's line first appeared reads
    DRIFTED, and re-reading the code cannot clear it: `git log -L` walks past
    an edit to the row on purpose, so re-wording it leaves the baseline exactly
    where it was. Without a way to say "I read this at commit X", such a row is
    DRIFTED for good — which is the state this work item's own fragment
    reached, four rows at once.
    """
    fragment(repo, "| POL-1 | `src/service.py:2` | | | first wording |\n")
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")
    at = head(repo)

    assert "DRIFTED" in run(["."], str(repo)).stdout

    path = repo / ".specseal" / "map" / "core.md"
    path.write_text(path.read_text().replace("| first wording |", "| re-read |"))
    git(repo, "commit", "-qam", "re-word the row after re-reading")
    assert "DRIFTED" in run(["."], str(repo)).stdout, (
        "re-wording the row cleared the drift, so the derivation followed the "
        "edit — this case and the bulk-rewrite one cannot both be true"
    )

    path.write_text(path.read_text().replace("| re-read |", f"| 2026-09-01 `{at}` |"))
    git(repo, "commit", "-qam", "record the commit it was re-read at")
    r = run(["."], str(repo))
    assert "DRIFTED" not in r.stdout, (
        f"a stamp cannot clear drift, so a drifted row stays drifted:\n{r.stdout}"
    )
    assert r.returncode == 0, r.stdout


def test_an_orphaned_stamp_falls_back_to_the_right_answer(repo):
    """Which is why a stamp may name a commit the branch made.

    The old rule forbade it because an orphaned stamp fell back to the ledger
    HEADER — a baseline from before the work, silently, in every clone but the
    one that wrote it. The fallback is the row's own first appearance now, and
    after a squash that is the squash commit. The stamp becoming unresolvable
    costs nothing.
    """
    git(repo, "switch", "-q", "-c", "feature")
    (repo / "src" / "service.py").write_text("".join(f"new{i}\n" for i in range(1, 9)))
    git(repo, "commit", "-qam", "change the code")
    at = head(repo)
    fragment(repo, f"| POL-1 | `src/service.py:2` | 2026-09-01 `{at}` |\n")

    git(repo, "switch", "-q", "main")
    git(repo, "merge", "-q", "--squash", "feature")
    git(repo, "commit", "-qm", "squashed feature")
    git(repo, "branch", "-qD", "feature")
    git(repo, "reflog", "expire", "--expire=now", "--all")
    git(repo, "gc", "--prune=now", "-q", check=False)

    assert (
        git(repo, "cat-file", "-e", f"{at}^{{commit}}", check=False).returncode != 0
    ), "the fixture did not actually destroy the stamped commit"

    r = run(["."], str(repo))
    assert r.returncode == 0, r.stdout
    assert "1 ok" in r.stdout, r.stdout


FRAGMENT = ("1788229400-every-branch-appends-to-the-same-two-files.md",)


def test_the_fragment_this_work_item_wrote_carries_no_baseline_header():
    """Dogfood. The convention is worth what the repository that wrote it
    actually does, and a fragment that quietly carried a baseline header would
    make every case above vacuous here.

    Rows in it DO carry stamps, and that is not a lapse: four of them drifted
    when the design changed under them, and a stamp is the only thing that
    clears a drifted row. The case below is what holds those honest.
    """
    frag = os.path.join(ROOT, ".specseal", "map", *FRAGMENT)
    assert os.path.isfile(frag), "this work item recorded no evidence at all"
    text = read(".specseal", "map", *FRAGMENT)
    assert "Baseline commit" not in text, "a fragment carries no baseline header"
    assert "## Baseline" not in text


def test_no_stamp_in_a_fragment_resolves_only_in_the_clone_that_wrote_it():
    """`tests/test_ledger_stamps_resolve.py` holds this for `.specseal/map.md`
    and reads no fragment, so this is the same property one directory over.

    It is deliberately WEAKER in one direction. That file requires every stamp
    to exist, because an unresolvable one there fell back to the ledger header
    — a baseline from before the work, silently. A fragment has no header, so
    an unresolvable stamp falls back to the row's own first appearance, which
    is right; the squash that destroys a stamp is therefore allowed here.

    What is never allowed is the middle case: a stamp that RESOLVES and that no
    ref reaches. That object lives in the worktree that wrote it and nowhere
    else, so the row is measured one way locally and another way in CI, with
    nothing printed either side.
    """
    import glob

    stamps = []
    for path in sorted(glob.glob(os.path.join(ROOT, ".specseal", "map", "*.md"))):
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f.read().splitlines(), 1):
                if not line.strip().startswith("|"):
                    continue
                for m in re.finditer(
                    r"\b\d{4}-\d{2}-\d{2}\s+`?([0-9a-f]{7,40})`?", line
                ):
                    stamps.append((os.path.relpath(path, ROOT), n, m.group(1)))

    def git_root(*args):
        return subprocess.run(
            ["git", "-C", ROOT, *args], capture_output=True, encoding="utf-8"
        ).returncode

    local_only = [
        s
        for s in stamps
        if git_root("cat-file", "-e", f"{s[2]}^{{commit}}") == 0
        and git_root("merge-base", "--is-ancestor", s[2], "HEAD") != 0
    ]
    assert not local_only, (
        f"stamps that resolve but no ref reaches: {local_only}. The object "
        "survives in the worktree that wrote it and nowhere else, so the row "
        "measures from one commit locally and another in CI"
    )
