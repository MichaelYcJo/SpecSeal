"""#417 and #858: the checklist box asking whether the release reached the
directory has a command behind it, that command never fails a release, and it
says nothing about a directory it did not read.

  A6  per marketplace file: an entry or not, which commit is pinned, and
      whether that commit is an ancestor of `main`
  A7  absence and a failed fetch are reports, and both exit 0. The only
      non-zero exit is a malformed argument, which is the author's
  #858 A1  the run claims nothing about the directory -- the catalog people
      browse inside Claude, which no script can read -- tells nobody to
      submit or resubmit, and closes by naming the page a person opens for
      each kind of listing
  #858 A3  an absent entry is one line: which file, over how many entries,
      and no act

**The marketplace files are not the directory.** They are the two public
`.claude-plugin/marketplace.json` files the command reads, outputs of the
review pipeline and nothing more; *listed* is a word about the directory, so
no line here says it (`seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/spec.md`
§*Vocabulary*).

**Nothing here reaches the network.** `fetch` is replaced at the module, and
the fixtures below are the four `source` shapes measured over the two real
files on 2026-09-22, rewritten onto neutral names. A fixture captured whole
would carry real organisation names into the tree, which `CONTRIBUTING.md`
§*House rules*, *No real identifiers*, refuses; the shapes are what the
reader is about, and the shapes are what these carry.

**The ancestry answer has three values, not two**, and that is the half a
reader most easily loses. A commit this clone does not have is not a commit
that is unreachable — and reporting the two as one turns an unfetched
checkout into a stale-pin warning at the exact moment somebody is deciding
whether a file is behind. `test_a_commit_this_clone_does_not_have_is_not_called_unreachable`
is that case, and it builds a real repository to have an ancestry to ask
about.

**Shown red before it was committed (§15).** Each case was run against the
script with the one behaviour it pins removed; the mutations and what each
case said were recorded in
phase 3 of work item `1790076050-the-release-tail-is-three-acts-no-document-names`,
whose rule `docs/branch-and-release.md` §*Cutting a release* now carries. The
#858 cases and the pins they moved were run red against the command as #417
left it, and with each new line removed, in phase 1 of work item
`1791384161-the-plugin-directory-check-reads-the-directory`.
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


def marketplace(*entries):
    """A marketplace file in the shape both real ones have."""
    return json.dumps({"name": "a-marketplace", "plugins": list(entries)})


def pinning(sha=SHA, **source):
    """This plugin's entry, pointing outward and pinning `sha`."""
    body = {"source": "url", "url": "https://github.com/example-org/kit.git"}
    if sha is not None:
        body["sha"] = sha
    body.update(source)
    return {"name": NAME, "description": "a plugin", "source": body}


def other(name):
    return {"name": name, "description": "someone else", "source": f"./plugins/{name}"}


# --- A6: the three facts the box asks for ----------------------------------


def test_an_entry_reports_its_pinned_commit(tmp_path):
    """A6's first two facts, asserted on the line that carries them.

    The commit is named twice — once as *what is pinned* and once inside the
    ancestry sentence below it — so a check for the hash anywhere in the
    report passes with the first line gutted. Measured: dropping the hash
    from the entry line left this case green until it was pinned to that
    line. The first line is the one the box is read for, because the ancestry
    sentence is absent whenever the clone cannot answer.
    """
    mod = checker()
    out = mod.line(
        "official",
        "example-org/marketplace",
        marketplace(other("a"), pinning(), other("b")),
        None,
        NAME,
        str(tmp_path),
        "main",
    )
    head = out[0]
    assert "an entry" in head and "not an entry" not in head
    assert SHA[:12] in head, (
        "the line that says the file has an entry does not say which commit "
        f"the entry pins: {head!r}"
    )
    assert mod.pinned(pinning()) == (
        SHA,
        "https://github.com/example-org/kit.git",
    )


def test_an_absent_entry_names_the_file_and_its_count_and_no_act(tmp_path):
    """#858 A3, and A6's other shape. The count is what tells a reader the
    file was read at all — *not an entry* over an empty list and over 310
    entries are different facts, and only one of them is about this plugin.

    The line is the whole answer for that file. It used to be followed by an
    instruction to submit through a short link, about a directory nothing here
    had read; the owner's Console page said *published* while this said *not
    listed* in both files (#858). An absent entry in a marketplace file is a
    fact about that file, and a second line is where an act would come back.
    """
    mod = checker()
    out = mod.line(
        "community",
        "example-org/marketplace",
        marketplace(other("a"), other("b")),
        None,
        NAME,
        str(tmp_path),
        "main",
    )
    assert len(out) == 1, (
        f"an absent entry is followed by more than its own line: {out!r}"
    )
    assert "not an entry" in out[0]
    assert "2 entries" in out[0], "a `not an entry` that does not say over how many"
    assert "example-org/marketplace" in out[0], "the line does not say which file"
    assert "listed" not in out[0], (
        "the line speaks of a listing, which is the directory's word, about a "
        "marketplace file"
    )


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
            "example-org/marketplace",
            marketplace(entry),
            None,
            NAME,
            str(tmp_path),
            "main",
        )
    )
    assert "an entry" in out and "not an entry" not in out
    assert "pinning no commit" in out


def test_a_commit_this_clone_does_not_have_is_not_called_unreachable(tmp_path):
    """The third ancestry value. Folding *unknown here* into *not reachable*
    would tell a reader a file is behind because their checkout was not
    fetched."""
    mod = checker()
    repo = tmp_path / "r"
    repo.mkdir()
    git = lambda *a: subprocess.run(
        ["git", "-C", str(repo), *a], check=True, capture_output=True, encoding="utf-8"
    )
    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (repo / "f.txt").write_text("one\n", encoding="utf-8")
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
            "example-org/marketplace",
            marketplace(pinning(sha=head)),
            None,
            NAME,
            str(repo),
            "main",
        )
    )
    assert "Reachable from main" in reachable
    # #858: this is the line that used to end *resubmit through* a short link.
    # Only a real ancestry reaches it, which is why it is pinned here and not
    # in the run-wide case below.
    assert "submit" not in reachable.lower(), (
        f"the reachable line sends the reader to submit or resubmit: {reachable!r}"
    )
    unknown = "\n".join(
        mod.line(
            "official",
            "example-org/marketplace",
            marketplace(pinning()),
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
            "example-org/marketplace",
            None,
            "HTTP 503",
            NAME,
            str(tmp_path),
            "main",
        )
    )
    assert "could not be read" in out and "HTTP 503" in out
    assert "not a reason to stop" in out


def test_a_payload_that_is_not_a_marketplace_file_is_a_report(tmp_path):
    mod = checker()
    for payload in ("<html>a login page</html>", json.dumps({"message": "Not Found"})):
        out = "\n".join(
            mod.line(
                "official",
                "example-org/marketplace",
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
        pytest.param((marketplace(other("a")), None), id="absent from both"),
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
        "a marketplace file is missing from the report"
    )
    assert "was not read" in out, (
        "the run does not say what it cannot answer, which is the half a "
        "reader would otherwise take it to have answered"
    )


# --- #858 A1: nothing here claims what the directory holds ------------------


@pytest.mark.parametrize(
    "outcome",
    [
        pytest.param((marketplace(other("a")), None), id="no entry"),
        pytest.param((marketplace(pinning()), None), id="an entry pinning a commit"),
        pytest.param((None, "HTTP 503"), id="a failed fetch"),
    ],
)
def test_the_run_claims_nothing_about_the_directory_and_names_the_pages(
    monkeypatch, capsys, outcome
):
    """#858 A1. The directory is measured unreachable from a script, so the
    run says that and names the page a person opens, by the kind of listing
    each answers for. Whatever the files hold, nothing printed says the plugin
    is or is not listed, and nothing sends the reader to submit or resubmit —
    on the portal nothing is resubmitted, and a Console listing takes no new
    version (`spec.md` §*Vocabulary*, three facts from the docs)."""
    mod = checker()
    assert not hasattr(mod, "PORTAL"), (
        "the short link that answers 302 to a documentation page is still a "
        "constant here"
    )
    monkeypatch.setattr(mod, "fetch", lambda url: outcome)
    assert mod.main(["--root", ROOT]) == 0
    out = capsys.readouterr().out
    assert "submit" not in out.lower(), (
        f"the run tells the reader to submit or resubmit:\n{out}"
    )
    assert "listed" not in out, (
        f"the run says the plugin is or is not listed, about a directory it "
        f"did not read:\n{out}"
    )
    closing = out[out.index("was not read") :] if "was not read" in out else ""
    assert closing, f"the run does not say the directory was not read:\n{out}"
    assert "Submissions" in closing, (
        "the closing lines do not name the portal's Submissions page"
    )
    assert "Console" in closing, "the closing lines do not name the Console page"
    assert mod.SUBMISSIONS_PAGE in closing and mod.CONSOLE_PAGE in closing, (
        "the closing lines name the pages without the addresses a person opens"
    )
    # Round 1's 🟡 1: under the default publish setting a person selects
    # Publish for every version that passes, so *on its own* overstated it.
    assert "without a resubmission" in closing and "publish setting" in closing, (
        "the closing lines do not say a portal listing picks up new versions "
        "without a resubmission and goes live by its publish setting"
    )


def test_a_malformed_argument_is_the_only_non_zero_exit():
    """Stated in `spec.md` A7 as the one exception, and it is argparse's."""
    mod = checker()
    with pytest.raises(SystemExit) as raised:
        mod.main(["--no-such-flag"])
    assert raised.value.code == 2


def test_a_root_with_no_manifest_is_a_malformed_argument(tmp_path):
    """Round 1's ⬜ 6. A `--root` holding no `.claude-plugin/plugin.json` is the
    author's mistake, so it takes argparse's exit 2 and one line saying what
    is missing, not a traceback and exit 1."""
    mod = checker()
    with pytest.raises(SystemExit) as raised:
        mod.main(["--root", str(tmp_path)])
    assert raised.value.code == 2


# --- what it reads the name from -------------------------------------------


def test_the_name_comes_from_the_manifest_rather_than_a_literal():
    """A literal would be a second place the name is written down, and the
    name is the one thing that cannot change any more — users have the plugin
    installed under it. A rename then shows up as *not an entry* rather than
    as a check grading a name nobody uses."""
    mod = checker()
    assert mod.plugin_name(ROOT) == "specseal"
    source = open(SCRIPT, encoding="utf-8").read()
    body = source.split('"""', 2)[2]
    assert '"specseal"' not in body and "'specseal'" not in body, (
        "the plugin's name is written into the script as a literal"
    )


def test_it_reads_the_path_the_marketplace_files_actually_have():
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
