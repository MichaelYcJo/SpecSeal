"""A ledger check narrowed to one fragment reported clean, and it was blind.

`evidence-check --ledger '<fragment>'` reads that fragment and nothing else —
never `seal/ledger.md`, where the rows with the longest reach live. Issue #153
measured what that costs: one work item's three review rounds and two fix
passes all ran the scoped form and all reported ok, and the unscoped read at
the pull request found fifteen drifted rows and one broken claim, every one in
a file the branch had touched.

The guidance half of the answer is pinned in
`tests/test_the_handoff_names_the_form_it_ran.py`. Guidance binds a session
that reads it, and the session this trap was sprung on narrowed the command on
its own initiative — so the tool announces its own narrowing as well, and what
is here is that: a fixture repository, the checker run on it, and the line it
prints read back.

Every case here was seen red at `23c7ccb`, before the line existed.
"""

import importlib.util
import os
import subprocess
import sys
import types

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")

SERVICE = "def handler(x):\n    return x + 1\n"
# `handler`'s body, hashed the way the checker hashes it. Pinned rather than
# computed, so a fixture cannot agree with a broken hasher.
GOOD = "9207ed06"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    return " ".join(read(*parts).split())


@pytest.fixture
def proj(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    return d


def ledger(proj, body, at="seal/ledger.md"):
    path = proj / at
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# map\n\n" + body, encoding="utf-8")
    return path


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def test_the_hash_in_this_files_fixtures_is_the_real_one(proj):
    """Pinned rather than computed: a fixture that asks the checker for its
    own expected value agrees with a broken checker."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_a_narrowed_run_names_the_shared_ledger_it_did_not_read(proj):
    """The case #153 is about. The fragment is clean, the shared ledger is
    broken, and the scoped run exits 0 — so the only thing that can tell
    anyone is the run saying what it skipped."""
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    (proj / "SPEC.md").write_text(
        f"| POL-1 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert r.returncode == 0, r.stdout
    assert "--ledger narrowed this run" in r.stdout, r.stdout
    assert "not read" in r.stdout, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, (
        "the run reports a clean SPEC.md and never names the ledger it "
        "skipped — which reads exactly like a repository with one ledger"
    )
    assert "run without --ledger" in r.stdout, (
        "naming the skipped file without naming the way to read it leaves "
        "the reader where the narrowing put them"
    )
    assert "gone" not in r.stdout, (
        "the skipped ledger was actually READ — the notice is a report on "
        "what was skipped, not a second pass over it"
    )


def test_every_skipped_ledger_is_named_not_counted(proj):
    """A count is not a coordinate. The reader has to open the files, and
    `2 ledgers were not read` names none of them."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    ledger(
        proj,
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n",
        at="seal/ledger/1788486395-other.md",
    )
    (proj / "SPEC.md").write_text(
        f"| POL-3 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert "2 ledgers" in r.stdout, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, r.stdout
    assert os.path.join("seal", "ledger", "1788486395-other.md") in r.stdout, r.stdout


def test_the_notice_counts_one_ledger_in_the_singular(proj):
    """`1 ledgers` is the tell that nobody read the line they shipped."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    (proj / "SPEC.md").write_text(
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert "1 ledger " in r.stdout and "1 ledgers" not in r.stdout, r.stdout
    assert "was not read" in r.stdout, r.stdout


def test_an_unnarrowed_run_says_nothing_about_skipping(proj):
    """The line is a report on a narrowing. A run that narrowed nothing has
    nothing to report, and printing it anyway trains people past it."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "were not read" not in r.stdout and "was not read" not in r.stdout, r.stdout


def test_a_narrowing_that_skips_nothing_says_nothing(proj):
    """`--ledger seal/ledger.md` on a repository holding only that file read
    everything there was. A notice there would be false."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", "seal/ledger.md", "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout
    assert "not read" not in r.stdout, r.stdout


def test_a_second_spelling_of_the_same_file_is_not_reported_as_skipped(proj):
    """`--ledger ./seal/ledger.md` names the file the resolver would have
    opened, spelled with a `./` in front — which is what a person types. Two
    paths compared as raw strings are two files, so the run would report the
    ledger it had just read as one it skipped: a false notice, on the one run
    that narrowed nothing."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", os.path.join(".", "seal", "ledger.md"), "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout
    assert "not read" not in r.stdout, r.stdout


def case_insensitive(tmp_path):
    """Whether this filesystem really folds case, probed rather than assumed.

    The precondition the case below needs, stated and checked. A platform
    assertion nobody removed the guarantee from is exactly what round 1's
    🟡 9 was about, so this file does not get to assume its own.
    """
    d = tmp_path / "case-probe"
    d.mkdir()
    (d / "x").write_text("", encoding="utf-8")
    return (d / "X").exists()


def test_a_hard_link_to_the_ledger_is_not_reported_as_skipped(proj):
    """Round 1's 🟡 9, in the form that is red on every platform.

    `realpath` resolves symlinks and knows nothing about hard links, so two
    names for one inode look like two files and the run reports the ledger it
    just read as one it skipped. Folding by `st_dev`/`st_ino` answers hard
    links, case folding and symlinks in one, and needs no platform to be true.
    """
    target = ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    link = proj / "seal" / "same-file.md"
    os.link(target, link)
    r = run(["--ledger", os.path.join("seal", "same-file.md"), "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout
    assert "not read" not in r.stdout, (
        "the run names as skipped a file it read under another name — the "
        "notice is false on the one run that narrowed nothing"
    )


def test_a_case_spelling_of_the_ledger_is_not_reported_as_skipped(proj, tmp_path):
    """The platform half of 🟡 9, executed where the platform allows it.

    `os.path.normcase` folds case on Windows and is the identity everywhere
    else, and `realpath` canonicalises case nowhere — so on the
    case-insensitive filesystem this was built on, `--ledger SEAL/ledger.md`
    read the ledger and then listed it as unread. `agent-contract` §13: a
    defence resting on the platform where nobody removed the guarantee.
    """
    if not case_insensitive(tmp_path):
        pytest.skip("case-sensitive filesystem — the hard-link case covers it")
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", os.path.join("SEAL", "ledger.md"), "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout
    assert "not read" not in r.stdout, r.stdout


def checker_module():
    """`evidence_check.py` in this process, for the one case a subprocess
    cannot reach: the platform state has to be produced from inside."""
    spec = importlib.util.spec_from_file_location("specseal_ec_for_tests", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_an_inode_of_zero_does_not_fold_two_files_into_one(proj, monkeypatch):
    """Round 2's 🟡 8. Python's contract is *"if non-zero, uniquely identifies
    the file"*, and CPython's Windows `stat` leaves both fields 0 when it
    cannot open a file. A zero reaches no `OSError`, so it went straight into
    the identity — and every zeroed file then had the SAME identity, so a
    ledger that was read swallowed every ledger that was not.

    **That is silence, which is the direction this notice exists to end** and
    the reverse of the one its docstring declares. Whether a zero actually
    arrives on `windows-latest` is the CI leg's to answer; what is pinned
    here is what the code does with one.

    In-process rather than through the CLI, because the state cannot be
    produced from outside. `os.stat` is zeroed for the two ledgers alone, so
    everything else that stats on the way — `glob`, and `seal_home` looking
    for its own `SKILL.md` — keeps working.

    **Two zeroings, and the second is what makes this about `st_ino`**
    (round 3's 🟡 6). Zeroing BOTH fields is the state Windows produces, and
    it cannot separate the two: swapping the test to `info.st_dev` left the
    whole suite green, because a zero device falls back exactly as a zero
    inode does. A real device with a zero inode is the state that tells them
    apart — under `st_dev` the pair then reads as one identity again and the
    unread fragment goes unnamed, which is the silence this exists to end.
    Python's contract is about `st_ino` alone, so `st_ino` is the test.
    """
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    ledger(
        proj,
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n",
        at="seal/ledger/1788501054-unread.md",
    )
    read = [str(proj / "seal" / "ledger.md")]
    zeroable = {
        os.path.realpath(read[0]),
        os.path.realpath(proj / "seal" / "ledger" / "1788501054-unread.md"),
    }

    module = checker_module()
    real = module.os.stat

    def faking(fields):
        def stat(path, *args, **kwargs):
            info = real(path, *args, **kwargs)
            if os.path.realpath(path) in zeroable:
                return types.SimpleNamespace(**fields(info))
            return info

        return stat

    both = faking(lambda info: {"st_dev": 0, "st_ino": 0})
    inode_only = faking(lambda info: {"st_dev": info.st_dev, "st_ino": 0})

    for what, stat in (("both fields", both), ("the inode alone", inode_only)):
        monkeypatch.setattr(module.os, "stat", stat)
        missed = module.skipped_by_narrowing(str(proj), read)
        assert [os.path.basename(p) for p in missed] == ["1788501054-unread.md"], (
            f"with {what} zeroed, the fragment nobody read was named by "
            f"nothing — every zeroed ledger had one identity. Got {missed}"
        )

    # Round 4's 🟡 5, as assertions here rather than as a unit of its own.
    # Both corrected paragraphs are inside `skipped_by_narrowing`, which is
    # what this case already covers, and both were false in the same way:
    # they explained a guard through a platform fact that is not the reason.
    # A recorded limit that is wrong tells the next battery a live line is
    # dead, so the corrected words are pinned (§14).
    # `read` is the local list of ledgers above, so the module-level reader
    # is reached through `flat`.
    source = flat("skills", "evidence-check", "scripts", "evidence_check.py")
    assert (
        "folds case on WINDOWS alone, not wherever the platform folds it" in source
    ), (
        "the fallback sentence is back to tying `normcase` to what the "
        "filesystem does — it folds on Windows and nowhere else, which is "
        "round 1's 🟡 9 restated one function over"
    )
    assert "reached by `OSError` on every platform" in source, (
        "the reachability paragraph is back to explaining the fallback "
        "through the zeroed inode alone, which is Windows-only where the "
        "fallback is not"
    )
    memo = flat(
        "seal",
        "specs",
        "1788501054-a-check-reports-clean-while-something-is-missing",
        "overview.md",
    )
    for phrase in (
        "re-deriving all four found three of the four reasons false",
        "reached by `OSError` on EVERY platform",
    ):
        assert phrase in memo, (
            f"the memo's limit table no longer says: {phrase} — the "
            "measurement is written in two places and pinning one is the "
            "class this branch keeps finding"
        )


def test_two_devices_that_share_an_inode_number_are_two_ledgers(proj, monkeypatch):
    """The device is half the identity, and dropping it left every case
    green.

    Inode numbers are handed out per filesystem, so a ledger on one device
    and a fragment on another can legitimately carry the same number. Under
    `(st_ino,)` alone the two fold together and the fragment nobody read is
    swallowed by the one that was — the same silence a zeroed inode
    produced, arriving from the other half of the pair.

    Nothing in a one-filesystem fixture can build this, so the two devices
    are produced from inside. What is pinned is what the code does with the
    pair, not that a repository spans two mounts.
    """
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    ledger(
        proj,
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n",
        at="seal/ledger/1788501054-unread.md",
    )
    read = [str(proj / "seal" / "ledger.md")]
    other = os.path.realpath(proj / "seal" / "ledger" / "1788501054-unread.md")

    module = checker_module()
    real = module.os.stat

    def two_mounts(path, *args, **kwargs):
        info = real(path, *args, **kwargs)
        if os.path.realpath(path) == os.path.realpath(read[0]):
            return types.SimpleNamespace(st_dev=101, st_ino=7)
        if os.path.realpath(path) == other:
            return types.SimpleNamespace(st_dev=202, st_ino=7)
        return info

    monkeypatch.setattr(module.os, "stat", two_mounts)
    missed = module.skipped_by_narrowing(str(proj), read)
    assert [os.path.basename(p) for p in missed] == ["1788501054-unread.md"], (
        "two files on different devices sharing an inode number folded into "
        f"one, so the fragment nobody read went unnamed — got {missed}"
    )


def test_the_skipped_set_is_subtracted_from_the_list_the_defaults_come_from(
    proj, monkeypatch
):
    """Ledger row R4's claim, which nothing held: `default_patterns` exists so
    that the list deciding what gets NAMED as skipped is the same list the
    run reads from, rather than a second copy of it.

    The cost of two copies is invisible until the defaults change, which is
    why no ordinary case reaches it — the two would be identical on the day
    they were written. So the defaults are moved instead: a fourth location
    appears, and the skipped set has to follow it. A copy inlined here would
    keep naming the three it was written with.
    """
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    fourth = proj / "docs" / "elsewhere" / "claims.md"
    fourth.parent.mkdir(parents=True, exist_ok=True)
    fourth.write_text(f"| POL-9 | `src/service.py#handler@{GOOD}` |\n", "utf-8")

    module = checker_module()
    real = module.default_patterns
    monkeypatch.setattr(
        module, "default_patterns", lambda root: [*real(root), str(fourth)]
    )
    missed = module.skipped_by_narrowing(str(proj), [str(proj / "seal" / "ledger.md")])
    assert str(fourth) in [os.path.realpath(p) for p in missed] or fourth.name in [
        os.path.basename(p) for p in missed
    ], (
        "a location the defaults now read was not reported as skipped, so "
        f"the skipped set is a second copy of the list — got {missed}"
    )


def test_one_file_matched_by_two_patterns_is_read_once(proj):
    """`resolve_patterns` deduplicates, and nothing showed it. The defaults
    are disjoint, so no run through them can produce the same file twice —
    but `--ledger` takes any number of globs, and two overlapping ones are
    the ordinary way somebody widens a narrowed run.

    Without the deduplication the ledger is opened twice and every row in it
    is counted twice, which reads as a repository with twice the evidence it
    has.

    The assertion is on the TOTAL and not on a per-ledger line, which is what
    makes it able to fail: each pass over the file prints its own `1 ok`, so
    a duplicate is invisible there and shows up only where the passes are
    added together. Written against the per-ledger line first, and it stayed
    green under the mutation.
    """
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", "seal/ledger.md", "--ledger", "seal/*.md", "."], proj)
    assert r.returncode == 0, r.stdout
    assert "total: 1 ok" in r.stdout, (
        "one file matched by two patterns was read twice, so its rows were "
        f"counted twice:\n{r.stdout}"
    )


def test_one_file_matched_under_two_spellings_is_read_once(proj):
    """Round 13 of work item 1788501054 — the Windows CI leg's finding, as
    the class rather than the platform.

    `resolve_patterns` deduplicated on the string `glob.glob` returns, and
    `glob.glob` keeps a literal pattern's spelling while joining a wildcard's
    matches with `os.sep`. On Windows `seal/ledger.md` and `seal/*.md`
    therefore name one file two ways -- `seal/ledger.md` and
    `seal\\ledger.md` -- the set kept both, and the case above went red there
    after twelve green rounds everywhere else. That is the platform-inside-
    the-fold shape round 1 removed from `skipped_by_narrowing` with the inode,
    one function over.

    The class is *one file, two spellings*, and `./seal/ledger.md` against
    `seal/ledger.md` is that class on every platform, so this case is red on
    the machine that fixes it and not only on the leg that found it. The fold
    is now `os.path.normpath`, which collapses separators and `.` segments
    and folds no case -- so it is not the `normcase` mistake either.
    """
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--ledger", "./seal/ledger.md", "--ledger", "seal/ledger.md", "."], proj)
    assert r.returncode == 0, r.stdout
    assert "total: 1 ok" in r.stdout, (
        "one file named under two spellings was read twice, so its rows were "
        f"counted twice:\n{r.stdout}"
    )


def test_a_ledger_that_cannot_be_stat_ed_is_named_rather_than_crashing(proj):
    """The `OSError` half of the fallback, and nothing reached it until the
    mutation loop asked: dropping the fallback and letting `os.stat` raise
    left every case green.

    A broken symlink is how it arrives through the CLI. `glob` returns one
    for a literal pattern, because it tests `lexists`, and `os.stat` then
    raises `ENOENT` — so the checker meets a path it found and cannot stat.
    The fallback keys it by path, which over-reports: the fragment is NAMED
    as unread rather than swallowed, which is the direction this notice
    declares.
    """
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    dangling = proj / "seal" / "ledger" / "1788501054-gone.md"
    dangling.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(proj / "seal" / "ledger" / "nothing-here.md", dangling)
    except (OSError, NotImplementedError, AttributeError):
        pytest.skip("this platform will not create a symlink without privileges")
    r = run(["--ledger", os.path.join("seal", "ledger.md"), "."], proj)
    assert r.returncode == 0, r.stdout
    assert "1788501054-gone.md" in r.stdout, (
        "a ledger the run found and could not stat was passed over in "
        f"silence, which is the state the notice exists to end:\n{r.stdout}"
    )


def test_the_notice_survives_a_narrowing_that_matches_nothing(proj):
    """The worst silence of the set. `--ledger` with a typo in it matches no
    file, the run says `no evidence ledgers found` and exits 0, and the
    repository's real ledgers are sitting right there."""
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    r = run(["--ledger", "TYPO.md", "."], proj)
    assert r.returncode == 0, r.stdout
    assert "no evidence ledgers found" in r.stdout, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, (
        "a narrowing that matched nothing reported an empty repository, "
        "which is the same sentence a repository with no ledger gets"
    )


def test_the_notice_reaches_a_reverify_run(proj):
    """`--reverify` is the run the narrowing exists FOR, so it is the run
    most likely to be narrowed and the one whose skipped set matters most:
    every row it did not re-stamp stays whatever it was."""
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    (proj / "SPEC.md").write_text(
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "--reverify", "."], proj)
    assert r.returncode == 0, r.stdout
    assert os.path.join("seal", "ledger.md") in r.stdout, (
        "the write that the narrowing exists to bound does not say what it left alone"
    )


def test_the_skill_documents_the_line_the_tool_prints():
    """A message a person reads and acts on, documented where the flag is
    documented. Without it the line is a fact about one release."""
    skill = flat("skills", "evidence-check", "SKILL.md")
    assert "which ledgers it did not read" in skill, (
        "`--ledger` is documented and its announcement is not, so the next "
        "edit to the message has nothing to check itself against"
    )
