"""#417: the checklist box asking whether the release reached the directory
has a command behind it, and that command never fails a release.

  A6  per directory: listed or not, which commit is pinned, and whether that
      commit is an ancestor of `main`
  A7  absence and a failed fetch are reports, and both exit 0. The only
      non-zero exit is a malformed argument, which is the author's

**Nothing here reaches the network.** `fetch` is replaced at the module, and
the fixtures below are the four `source` shapes measured over the two real
files on 2026-09-22, rewritten onto neutral names. A fixture captured whole
would carry real organisation names into the tree, which `CLAUDE.md` §*no
real identifiers in examples or fixtures* refuses; the shapes are what the
reader is about, and the shapes are what these carry.

**The ancestry answer has three values, not two**, and that is the half a
reader most easily loses. A commit this clone does not have is not a commit
that is unreachable — and reporting the two as one turns an unfetched
checkout into a stale-pin warning at the exact moment somebody is deciding
whether to resubmit. `test_a_commit_this_clone_does_not_have_is_not_called_unreachable`
is that case, and it builds a real repository to have an ancestry to ask
about.

**Shown red before it was committed (§15).** Each case was run against the
script with the one behaviour it pins removed; the mutations and what each
case said are in
`seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-3.md`.
"""

import importlib.util
import json
import os
import subprocess

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "plugin_directory_check.py")

NAME = "examplekit"


def checker():
    spec = importlib.util.spec_from_file_location(
        "specseal_plugin_directory_check_for_tests", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SHA = "0123456789abcdef0123456789abcdef01234567"


def directory(*entries):
    """A directory file in the shape both real ones have."""
    return json.dumps({"name": "a-directory", "plugins": list(entries)})


def listed(sha=SHA, **source):
    body = {"source": "url", "url": "https://github.com/example-org/kit.git"}
    if sha is not None:
        body["sha"] = sha
    body.update(source)
    return {"name": NAME, "description": "a plugin", "source": body}


def other(name):
    return {"name": name, "description": "someone else", "source": f"./plugins/{name}"}


# --- A6: the three facts the box asks for ----------------------------------


def test_a_listed_entry_reports_its_pinned_commit(tmp_path):
    """A6's first two facts, asserted on the line that carries them.

    The commit is named twice — once as *what is pinned* and once inside the
    ancestry sentence below it — so a check for the hash anywhere in the
    report passes with the first line gutted. Measured: dropping the hash
    from the `listed,` line left this case green until it was pinned to that
    line. The first line is the one the box is read for, because the ancestry
    sentence is absent whenever the clone cannot answer.
    """
    mod = checker()
    out = mod.line(
        "official",
        "example-org/directory",
        directory(other("a"), listed(), other("b")),
        None,
        NAME,
        str(tmp_path),
        "main",
    )
    head = out[0]
    assert "listed" in head and "not listed" not in head
    assert SHA[:12] in head, (
        "the line that says the plugin is listed does not say which commit "
        f"the entry pins: {head!r}"
    )
    assert mod.pinned(listed()) == (
        SHA,
        "https://github.com/example-org/kit.git",
    )


def test_an_absent_entry_says_so_and_says_how_many_it_read(tmp_path):
    """A6's other shape. The count is what tells a reader the file was read at
    all — *not listed* over an empty list and over 310 entries are different
    facts, and only one of them is about this plugin."""
    mod = checker()
    out = "\n".join(
        mod.line(
            "community",
            "example-org/directory",
            directory(other("a"), other("b")),
            None,
            NAME,
            str(tmp_path),
            "main",
        )
    )
    assert "not listed" in out
    assert "2 entries" in out, "a `not listed` that does not say over how many"
    assert mod.PORTAL in out, "it does not say what to do about it"


@pytest.mark.parametrize(
    "source",
    [
        # The four shapes measured over both real files on 2026-09-22. The two
        # without a `sha` are the ones a reader assuming `source["sha"]` raises
        # on: 52 of official's 310 entries carry the string form.
        pytest.param({"source": "./plugins/examplekit"}, id="string source"),
        pytest.param(
            {"source": {"source": "url", "url": "https://github.com/e/k.git"}},
            id="object, no sha",
        ),
        pytest.param(
            {
                "source": {
                    "source": "git-subdir",
                    "url": "https://github.com/e/k.git",
                    "ref": "v1.0.0",
                    "path": "plugins/k",
                }
            },
            id="ref but no sha",
        ),
    ],
)
def test_an_entry_that_pins_no_commit_is_read_rather_than_raised_on(tmp_path, source):
    """A6's tolerance. These are somebody else's file's shapes, so they are
    not this repository's to hold steady — and every one of them exists
    today."""
    mod = checker()
    entry = {"name": NAME, "description": "a plugin", **source}
    out = "\n".join(
        mod.line(
            "official",
            "example-org/directory",
            directory(entry),
            None,
            NAME,
            str(tmp_path),
            "main",
        )
    )
    assert "listed" in out and "not listed" not in out
    assert "pinning no commit" in out


def test_a_commit_this_clone_does_not_have_is_not_called_unreachable(tmp_path):
    """The third ancestry value. Folding *unknown here* into *not reachable*
    would tell a reader to resubmit because their checkout was not fetched."""
    mod = checker()
    repo = tmp_path / "r"
    repo.mkdir()
    git = lambda *a: subprocess.run(
        ["git", "-C", str(repo), *a], check=True, capture_output=True, text=True
    )
    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (repo / "f.txt").write_text("one\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    head = git("rev-parse", "HEAD").stdout.strip()

    assert mod.is_ancestor(str(repo), head, "main") is True
    assert mod.is_ancestor(str(repo), SHA, "main") is None, (
        "a commit the clone does not have is reported as unreachable, which "
        "reads as a stale pin"
    )
    assert mod.is_ancestor(str(repo), head, "no-such-ref") is None

    reachable = "\n".join(
        mod.line(
            "official",
            "example-org/directory",
            directory(listed(sha=head)),
            None,
            NAME,
            str(repo),
            "main",
        )
    )
    assert "Reachable from main" in reachable
    unknown = "\n".join(
        mod.line(
            "official",
            "example-org/directory",
            directory(listed()),
            None,
            NAME,
            str(repo),
            "main",
        )
    )
    assert "unknown here" in unknown and "NOT reachable" not in unknown


# --- A7: nothing here fails a release --------------------------------------


def test_a_failed_fetch_is_a_report(tmp_path):
    """A7. The thing that failed is somebody else's server."""
    mod = checker()
    out = "\n".join(
        mod.line(
            "community",
            "example-org/directory",
            None,
            "HTTP 503",
            NAME,
            str(tmp_path),
            "main",
        )
    )
    assert "could not be read" in out and "HTTP 503" in out
    assert "not a reason to stop" in out


def test_a_payload_that_is_not_a_directory_is_a_report(tmp_path):
    mod = checker()
    for payload in ("<html>a login page</html>", json.dumps({"message": "Not Found"})):
        out = "\n".join(
            mod.line(
                "official",
                "example-org/directory",
                payload,
                None,
                NAME,
                str(tmp_path),
                "main",
            )
        )
        assert "could not be read" in out, payload


@pytest.mark.parametrize(
    "outcome",
    [
        pytest.param((None, "HTTP 503"), id="both fetches fail"),
        pytest.param((directory(other("a")), None), id="absent from both"),
    ],
)
def test_the_run_exits_zero_on_absence_and_on_a_failed_fetch(
    monkeypatch, capsys, outcome
):
    """A7 end to end. Exit 0 is the claim, and it is the whole reason this is
    a command behind a box rather than an arm of a gate."""
    mod = checker()
    monkeypatch.setattr(mod, "fetch", lambda url: outcome)
    assert mod.main(["--root", ROOT]) == 0
    out = capsys.readouterr().out
    assert "specseal" in out, "the run does not say which plugin it asked about"
    assert out.count("official") and out.count("community"), (
        "a directory is missing from the report"
    )
    assert "readable from nowhere public" in out, (
        "the run does not say what it cannot answer, which is the half a "
        "reader would otherwise take it to have answered"
    )


def test_a_malformed_argument_is_the_only_non_zero_exit():
    """Stated in `spec.md` A7 as the one exception, and it is argparse's."""
    mod = checker()
    with pytest.raises(SystemExit) as raised:
        mod.main(["--no-such-flag"])
    assert raised.value.code == 2


# --- what it reads the name from -------------------------------------------


def test_the_name_comes_from_the_manifest_rather_than_a_literal():
    """A literal would be a second place the name is written down, and the
    name is the one thing that cannot change any more — users have the plugin
    installed under it. A rename then shows up as *not listed* rather than as
    a check grading a name nobody uses."""
    mod = checker()
    assert mod.plugin_name(ROOT) == "specseal"
    source = open(SCRIPT, encoding="utf-8").read()
    body = source.split('"""', 2)[2]
    assert '"specseal"' not in body and "'specseal'" not in body, (
        "the plugin's name is written into the script as a literal"
    )


def test_it_reads_the_path_the_directories_actually_have():
    """Measured 2026-09-22: the root `marketplace.json` that #417 and
    `spec.md` both name is 404 in both repositories, and the file is under
    `.claude-plugin/`. A reader at the ticket's path reports *could not be
    read* forever, which is A7 working and A6 answering nothing."""
    mod = checker()
    assert mod.MANIFEST == ".claude-plugin/marketplace.json"
    assert mod.manifest_url("owner/repo").startswith("https://api.github.com/"), (
        "the reader moved off an allowed host; "
        "`tests/test_no_real_identifiers.py` allows github.com and is silent "
        "on the raw-content host"
    )
