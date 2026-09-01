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
    assert "EXTERNAL" not in r.stdout, r.stdout
    # UNMEASURED is what proves the derivation was NOT applied. Were this
    # repository's history used, the row would have a baseline and read OK or
    # DRIFTED; the mapped repo supplies none, so nothing was compared. Before
    # round 1's 🔴 4 this printed `1 ok`, which is the same state described as
    # a comparison that happened.
    assert "UNMEASURED legacy/src/old.py:2" in r.stdout, r.stdout


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
    assert all(sha != "0" * 40 for sha, _, _ in lines.values()), lines
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


def test_a_renamed_ledger_still_catches_drift(repo):
    """Round 1, 🔴 3. Renaming a ledger turned that file's drift check OFF.

    `git log -L <n>,<n>:<path> <sha>` resolves `<path>` inside `<sha>`, and
    the anchor commit predates the rename — so handing it the working-tree
    name answers `fatal: There is no path ... in the commit`, rc 128. The row
    then had no baseline and was appended as `ok`. Executed before the fix: a
    ledger whose row read `1 drifted`/exit 1 read `1 ok`/exit 0 after nothing
    but `git mv`.

    The path now comes from blame's own `filename`, which is the name git knew
    the line by at that commit.
    """
    fragment(repo, "| POL-1 | `src/service.py:2` |\n", name="old.md")
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")

    before = run(["."], str(repo))
    assert "DRIFTED" in before.stdout and before.returncode == 1, before.stdout

    git(repo, "mv", ".specseal/map/old.md", ".specseal/map/new.md")
    git(repo, "commit", "-qm", "rename the ledger")

    after = run(["."], str(repo))
    assert "DRIFTED" in after.stdout, (
        f"the rename turned the drift check off:\n{after.stdout}"
    )
    assert after.returncode == 1, after.stdout


def test_the_blamed_path_survives_a_suppressed_filename_block(repo):
    """The half of 🔴 3's fix that a regex would have got wrong.

    Porcelain prints the metadata block only for the FIRST line of each
    commit — every later line of the same commit is a bare header with no
    `filename` at all. Measured on this repository's own fragment: line 1
    carries a block, line 2 does not. A reader taking `filename` from beside
    each header therefore has it for one line per commit, so the path is
    remembered per commit instead.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fragment(
        repo,
        "| POL-1 | `src/service.py:2` |\n| POL-2 | `src/service.py:3` |\n",
        name="old.md",
    )
    git(repo, "mv", ".specseal/map/old.md", ".specseal/map/new.md")
    git(repo, "commit", "-qm", "rename the ledger")

    lines = mod.blame_lines(str(repo), ".specseal/map/new.md", {})
    assert len(lines) >= 4, lines
    for n, (_, _, name) in lines.items():
        assert name == ".specseal/map/old.md", (
            f"line {n} lost the path git knew it by: {name}. Only the first "
            "line of each commit carries a `filename` block"
        )


def test_a_row_with_no_baseline_is_not_reported_ok(repo):
    """Round 1, 🔴 4. `OK` used to be appended unconditionally.

    A row nobody has committed yet has no baseline at all, and printing `ok`
    for it says a comparison happened. A fragment spends most of its working
    life uncommitted, so this is the ordinary state rather than a corner.

    It prints and passes; `--strict` is where it fails. A red light on every
    ordinary run is one a session learns to click past.
    """
    fragment(repo, "| POL-1 | `src/service.py:2` |\n")
    with open(repo / ".specseal" / "map" / "core.md", "a", encoding="utf-8") as f:
        f.write("| POL-2 | `src/service.py:3` |\n")

    r = run(["."], str(repo))
    assert "UNMEASURED src/service.py:3" in r.stdout, r.stdout
    assert "1 ok · " in r.stdout, f"the committed row stopped being ok:\n{r.stdout}"
    assert r.returncode == 0, r.stdout

    strict = run(["--strict", "."], str(repo))
    assert strict.returncode == 2, strict.stdout


def test_a_coordinate_between_a_date_and_a_hex_word_makes_no_stamp(repo):
    """Round 1, 🟡 5, first half.

    The coordinate was blanked with a single SPACE before the stamp scan, and
    a space is exactly what `STAMP_RE` accepts between a date and a hex word.
    A row reading `2026-01-01` then a coordinate under a directory named like
    a SHA then another hex word therefore collapsed into a stamp out of two
    values that were never beside each other.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    real = head(repo)
    fragment(repo, f"| POL-1 | 2026-01-01 `{real}/x.py:3` {real} |\n")
    text = (repo / ".specseal" / "map" / "core.md").read_text()
    assert mod.row_stamps(text, text.index("POL-1"), str(repo), {}) == [], (
        "a date and a hex word with only a coordinate between them were read as a stamp"
    )


def test_a_preceding_cell_does_not_beat_the_checked_column(repo):
    """Round 1, 🟡 5, second half.

    The scan reads the physical row, so the first resolvable stamp wins — and
    `Verified behavior`, free prose where this repository's own fragments name
    commits, sits BEFORE `Checked`. Rather than guess which cell the author
    meant, a row carrying two distinct stamps is reported and measured from
    neither.
    """
    older = head(repo)
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")
    newer = head(repo)

    fragment(
        repo,
        f"| POL-1 | `src/service.py:2` | seen at 2026-01-01 `{older}` "
        f"| 2026-09-01 `{newer}` |\n",
    )
    r = run(["."], str(repo))
    # Round 2, 🔴 4: this used to assert AMBIGUOUS and `DRIFTED not in`, and
    # that is the bug rather than the property. The fixture's cited file was
    # genuinely rewritten after the older stamp, so the row IS drifted — and
    # skipping the comparison to report ambiguity turned exit 1 into exit 0.
    # A second stamp anywhere in the row was a way to silence a real finding.
    #
    # What has to hold: no stamp is silently PICKED, the row is measured from
    # the widest candidate, and the drift still reports.
    assert "DRIFTED  src/service.py:2" in r.stdout, r.stdout
    assert f"touched since {older[:9]}" in r.stdout, (
        f"measured from the narrower candidate, or from neither:\n{r.stdout}"
    )
    assert older[:9] in r.stdout and newer[:9] in r.stdout, (
        f"the report names neither of the two stamps:\n{r.stdout}"
    )
    assert "row carries 2 stamps" in r.stdout, (
        f"the ambiguity went unreported:\n{r.stdout}"
    )
    assert r.returncode == 1, r.stdout


def test_two_stamps_on_an_untouched_row_still_report_ambiguous(repo):
    """The other half, or the case above passes by never reading AMBIGUOUS.

    Where nothing drifted there is no verdict competing with the ambiguity, so
    the row says so and passes — and fails under `--strict`, which is where a
    release asks for the stricter reading.
    """
    older = head(repo)
    open(repo / "src" / "other.py", "w").write("x\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "an unrelated commit")
    newer = head(repo)

    fragment(
        repo,
        f"| POL-1 | `src/service.py:2` | seen at 2026-01-01 `{older}` "
        f"| 2026-09-01 `{newer}` |\n",
    )
    r = run(["."], str(repo))
    assert "AMBIGUOUS src/service.py:2" in r.stdout, r.stdout
    assert "row carries 2 stamps" in r.stdout, r.stdout
    assert "DRIFTED" not in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout
    assert run(["--strict", "."], str(repo)).returncode == 2


def test_one_commit_written_at_two_lengths_is_one_stamp(repo):
    """Round 2, 🟡 5. `23cbd2e` and `23cbd2e24` are the same commit.

    Dedup ran on the matched STRING, so two spellings read as two disagreeing
    stamps and switched that row's drift check off. A ledger repaired by hand
    is exactly where mixed lengths occur — pull request #49 rewrote stamps
    across seven rows — so this is the ordinary shape, not a corner.
    """
    older = head(repo)
    (repo / "src" / "service.py").write_text("CHANGED\n" * 8)
    git(repo, "commit", "-qam", "rewrite the file")

    fragment(
        repo,
        f"| POL-1 | `src/service.py:2` | seen 2026-01-01 `{older[:7]}` "
        f"| 2026-09-01 `{older[:11]}` |\n",
    )
    r = run(["."], str(repo))
    assert "AMBIGUOUS" not in r.stdout, (
        f"two spellings of one commit read as two stamps:\n{r.stdout}"
    )
    assert "DRIFTED  src/service.py:2" in r.stdout, r.stdout
    assert r.returncode == 1, r.stdout


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


# A header long enough to reach the 2000-character bound. Round 2 found the
# existing header cases all using short fixtures, so the bound was never
# exercised by any of them and reverting the fix left 55 cases green.
LONG_PROSE = "rationale rationale rationale rationale rationale rationale\n" * 45


def test_a_sha_deep_in_a_prose_header_is_not_the_baseline(repo):
    """Round 2, 🟡 8. Removing the cap left a fragment's prose unbounded.

    The header baseline is the fallback for every row the derivation cannot
    anchor, so a commit that a rationale paragraph happens to mention became
    the thing those rows were measured against. An honest UNMEASURED turning
    into a measurement against an arbitrary commit is the quiet direction.

    A declaration is deliberate and stays unbounded; prose is accidental and
    is only read near the top.
    """
    sha = head(repo)
    fragment(
        repo,
        f"{LONG_PROSE}the design was settled at {sha} for the reasons above.\n\n"
        "| POL-1 | `src/service.py:2` |\n",
    )
    body = (repo / ".specseal" / "map" / "core.md").read_text()
    assert body.index(sha) > 2000, (
        f"the fixture puts the SHA at {body.index(sha)}, inside the bound"
    )

    r = run(["."], str(repo))
    assert f"baseline: {sha[:9]}" not in r.stdout, (
        f"a commit named in a rationale paragraph became the ledger's "
        f"baseline:\n{r.stdout}"
    )
    assert "none in the header" in r.stdout, r.stdout


def test_a_declared_baseline_past_the_bound_is_still_read(repo):
    """Round 2, 🟡 9. Nothing guarded the header fix at all.

    Reverting `header_of` to its cap-first body left the three ledger test
    files green — 55 passed — because every header fixture was short enough
    that cut and cap agree. This one is not: the declaration sits past 2000,
    where a bound on the search would silently drop it and the run would print
    the same line as a healthy file.
    """
    sha = head(repo)
    (repo / ".specseal" / "map").mkdir(parents=True, exist_ok=True)
    (repo / ".specseal" / "map" / "core.md").write_text(
        f"# map\n\n{LONG_PROSE}\n| Baseline commit | `{sha}` |\n\n"
        "| POL-1 | `src/service.py:2` |\n"
    )
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "ledger with a long header")
    body = (repo / ".specseal" / "map" / "core.md").read_text()
    assert body.index("Baseline commit") > 2000, (
        f"the fixture puts the declaration at {body.index('Baseline commit')}"
    )

    r = run(["."], str(repo))
    assert f"baseline: {sha[:9]} from a Baseline row" in r.stdout, (
        f"a declared baseline past the bound was dropped:\n{r.stdout}"
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
    for n, (sha, _, _) in lines.items():
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
    monkeypatch.setattr(
        mod, "blame_lines", lambda *a, **k: {1: ("x", 1, "f"), 3: ("y", 3, "f")}
    )
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


# Every document that states where a row's baseline comes from. Round 1 found
# this list holding three of seven: the design moved from last touch to first
# appearance at `9a7ce62` and only the three files that commit happened to
# touch came with it, so four documents went on stating the reading this work
# item measured and rejected. Two of them ship to plugin users through
# `hygiene.yml`'s `ships` glob.
#
# A file is added here when it states the rule, not when it merely mentions
# the ledger — the case below is about documents that would send a reader to
# the wrong reading.
BASELINE_DOCUMENTS = (
    ("CLAUDE.md",),
    ("templates", "map.md"),
    ("templates", "sdd-plan.md"),
    ("skills", "evidence-check", "SKILL.md"),
    ("skills", "implement", "SKILL.md"),
    ("README.md",),
)


def test_the_documents_say_where_the_baseline_comes_from_now():
    """A reader has to be able to check the rule, which means naming the
    reading. `first appeared` and `last touch` are two different rules with
    the same one-line summary, and the one-line summary is what a document
    that skips this ends up carrying."""
    for parts in BASELINE_DOCUMENTS:
        text = flat(*parts)
        assert "first appear" in text, (
            "/".join(parts) + " does not say WHICH commit of the row's history"
        )


def test_no_document_still_states_the_rejected_reading():
    """The absence half, which is what actually went wrong.

    A document can gain the corrected sentence and keep the old one, and a
    reader stops at whichever comes first. `git blame` naming the SOURCE of a
    row's baseline is the rejected reading — the derivation still uses blame
    to anchor a line, so the phrase is allowed where it describes that.
    """
    for parts in BASELINE_DOCUMENTS:
        text = flat(*parts)
        for rejected in (
            "comes from `git blame` of",
            "baseline is the commit `git blame` names",
            "It comes from `git blame` of",
        ):
            assert rejected not in text, (
                "/".join(parts) + f" still states the rejected reading: {rejected!r}"
            )


def test_the_korean_readme_states_the_same_reading():
    """`README.ko.md` cannot be checked with the English phrase, and leaving
    it out of the list above is exactly how it kept the rejected reading while
    every English document was corrected. `CONTRIBUTING.md` requires the two
    READMEs to move together, so this is the half that gets forgotten."""
    ko = flat("README.ko.md")
    assert "처음 나타난" in ko, (
        "README.ko.md does not say the baseline is the row's FIRST appearance"
    )
    assert "마지막으로 건드린" in ko, (
        "README.ko.md does not say which reading was rejected, so a Korean "
        "reader gets the cheaper one for the same rule"
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
