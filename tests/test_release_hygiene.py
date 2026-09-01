"""Release hygiene beyond "the changelog mentions the version".

That one is bound in `test_chain_hooks_hardening.py`. These are the two other
ways a release goes wrong inside the tree: a version number written into a
file that outlives it, and a supported-Python floor that three files state
differently.
"""

import json
import os
import re
import subprocess

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read_text(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def version():
    with open(
        os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as f:
        return json.load(f)["version"]


def tracked(*prefixes):
    out = subprocess.run(
        ["git", "ls-files", *prefixes],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.split()
    return [rel for rel in out if not rel.endswith((".gif", ".png", ".jpg"))]


def test_no_loaded_file_hardcodes_the_running_version():
    """A version number written into prose is right for exactly one release.

    `specs/` and `CHANGELOG.md` are records of a moment and keep theirs."""
    offenders = []
    for rel in tracked(
        "skills",
        "agents",
        "docs",
        "templates",
        "README.md",
        "README.ko.md",
        "CONTRIBUTING.md",
        "install.sh",
        "uninstall.sh",
    ):
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            if version() in f.read():
                offenders.append(rel)
    assert not offenders, f"{version()} written into files that outlive it: {offenders}"


def python_floor():
    """The supported floor, as ruff.toml states it: `py312` -> `3.12`."""
    with open(os.path.join(ROOT, "ruff.toml"), encoding="utf-8") as f:
        m = re.search(r'target-version = "py(\d)(\d+)"', f.read())
    assert m, "ruff.toml lost its target-version"
    return f"{m.group(1)}.{m.group(2)}"


def test_the_python_floor_is_the_same_number_everywhere():
    """Three places state it — the linter, the READMEs, the CI matrix — and a
    floor that disagrees with itself is worse than none: whoever reads the
    wrong one ships against an interpreter nobody tests."""
    floor = python_floor()
    for name in ("README.md", "README.ko.md"):
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            assert floor in f.read(), f"{name} does not state the {floor} floor"
    with open(
        os.path.join(ROOT, ".github", "workflows", "test.yml"), encoding="utf-8"
    ) as f:
        versions = re.findall(r'python: "(\d+\.\d+)"', f.read())
    assert versions, "the test matrix names no python versions"
    lowest = min(versions, key=lambda v: tuple(int(n) for n in v.split(".")))
    assert lowest == floor, (
        f"ruff.toml says {floor} and the lowest tested version is {lowest} — "
        "the floor is only real if CI stands on it"
    )


def test_update_tells_the_user_when_the_preset_block_changed():
    """`claude plugin update` installs the plugin, never the CLAUDE.md block.

    The block arrives only through `install.sh` or `/specseal:preset-setup`,
    both run by hand -- so a release can change a rule while every installed
    machine keeps stating the old one. The update command has to look and say
    so, or the change reaches no session that was already running."""
    with open(
        os.path.join(ROOT, "skills", "update", "SKILL.md"), encoding="utf-8"
    ) as f:
        update = f.read()
    assert "specseal:start" in update, (
        "the update command stopped comparing the preset block"
    )
    assert "/specseal:preset-setup" in update, (
        "the update command names no way to take a changed block"
    )
    assert "does not delete anything the user wrote" in update.lower(), (
        "taking a release started resolving overlaps with the user's own text"
    )


def test_no_section_accumulates_entries_in_the_shared_file():
    """`## Unreleased` was the region every branch appended to.

    This case used to check that it sat ABOVE every dated section, after a
    rebase conflict resolved the wrong way sank it below one. That ordering
    stopped being the problem when the section stopped existing: entries
    accumulate as `specs/<work-item-id>/changelog.md` fragments now, and the
    release gathers them into a dated section at the top. A heading by that
    name means somebody went back to the shared file, which is issue #46.

    The order still matters and is still checked — by
    `test_the_changelog_is_gathered_at_release.py`, against the gather script
    that produces it, which is the only thing that writes a section now.
    """
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        headings = re.findall(r"^## (.+)$", f.read(), re.M)
    found = [h for h in headings if h.lower().startswith("unreleased")]
    assert not found, (
        f"CHANGELOG.md carries {found} again. An entry goes in "
        "specs/<work-item-id>/changelog.md; `gather_changelog.py --version "
        "X.Y.Z` is what writes a section here"
    )


def test_the_newest_changelog_entry_is_the_version_being_shipped():
    """`test_plugin_version_is_in_changelog` accepts the version appearing
    anywhere, and an older entry satisfies that forever. What has to hold is
    that the newest dated entry IS the shipping version: a bump with no entry
    and an entry with no bump are the two ways a release goes out unexplained.

    An `## Unreleased` heading is skipped. On `next` the entries collect there
    while `plugin.json` stays at the last release, which is the whole point of
    accumulating."""
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        headings = re.findall(r"^## (.+)$", f.read(), re.M)
    dated = [h for h in headings if not h.lower().startswith("unreleased")]
    assert dated, "CHANGELOG has no released entry"
    newest = dated[0].split()[0]
    assert newest == version(), (
        f"CHANGELOG's newest entry is {newest}, plugin.json ships {version()}"
    )


def test_the_release_target_is_asked_before_the_work_starts():
    """The base branch decides whether a PR is a release, so it is a question
    with an answer available in the first minute.

    Left to the end it arrives after the branch exists and the changelog entry
    is already written under the wrong heading -- the same late-question
    failure the commit gate was moved forward to avoid."""
    for parts in (("skills", "implement", "SKILL.md"), ("agents", "smith.md")):
        # Collapsed, because both files wrap these sentences at different
        # columns and a literal match would be asserting the line breaks.
        text = " ".join(read_text(*parts).split())
        assert "a PR into `main` is a release" in text, (
            f"{parts[-1]} stopped saying which base branch means a release"
        )
        assert "release branch is not" in text, (
            f"{parts[-1]} stopped saying which base branch does NOT release"
        )
        assert "## Unreleased" in text, (
            f"{parts[-1]} lost the accumulate half of the question"
        )
        assert "yes/no" in text, (
            f"{parts[-1]} stopped saying the question has two continuing "
            "answers, which is what keeps a `no` from stranding the work"
        )


def _closer():
    """The release-closing script, imported so its regexes can be read.

    Round 2: every string the first version of this case pinned also lives in
    the module docstring, so the whole script could be replaced by a seven-line
    stub carrying those words and all twelve tests passed. A string search
    cannot see what a regex matches."""
    import importlib.util

    path = os.path.join(ROOT, ".github", "scripts", "close_issues_on_release.py")
    spec = importlib.util.spec_from_file_location("close_issues_on_release", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_token_stays_the_smallest_that_can_close_an_issue():
    """Read the permissions block as a mapping, not as text.

    A substring search for `contents: write` passes `contents:  write` — two
    spaces, one value to YAML — and that is the exact widening the block's own
    comment says it guards. Measured green before this."""
    workflow = read_text(".github", "workflows", "close-issues-on-release.yml")
    block = re.search(r"^permissions:\n((?:  [\w-]+:.*\n)+)", workflow, re.M)
    assert block, "the workflow states no permissions block, so it inherits all"
    granted = dict(re.findall(r"^  ([\w-]+):\s*(\S+)\s*$", block.group(1), re.M))
    assert granted == {"contents": "read", "issues": "write"}, (
        f"the token's scopes changed: {granted}. Its only write is a close, "
        "and an untrusted pull request body is what steers it"
    )
    on = re.search(r"^on:\n((?:  .*\n|\n)*?)^\w", workflow, re.M)
    assert on and re.findall(r"^  ([\w_]+):", on.group(1), re.M) == ["push"], (
        "the workflow gained a second trigger. A push to `main` is the only "
        "moment a closing keyword is readable, and any trigger an untrusted "
        "pull request can fire hands it the `issues: write` token"
    )
    assert re.search(r"^\s*branches:\s*\[main\]\s*$", workflow, re.M), (
        "the push trigger no longer names `main` alone"
    )


def test_the_script_only_ever_closes():
    """Fold the source before matching.

    The arguments go one per line, so `issue reopen` cannot occur as a literal
    and a forbidden-substring list over the raw text forbids nothing. The
    earlier version also carried `or "issue" in script`, whose right side is
    true of any file with the word in it."""
    folded = " ".join(
        read_text(".github", "scripts", "close_issues_on_release.py").split()
    )
    assert '"gh", "issue", "close", str(issue),' in folded, "the script stopped closing"
    for forbidden in ("reopen", "delete", "edit", "create", "comment", "transfer"):
        assert f'"gh", "issue", "{forbidden}"' not in folded, (
            f"the script gained `issue {forbidden}`. Only ever closes is what "
            "makes a re-run and a force-push safe to reason about"
        )


def test_only_a_keyword_before_a_number_closes_anything():
    """The regexes, read rather than searched for.

    The fenced `Closes #88` in `docs/branch-and-release.md` is the example a
    person copies, so a pull request body quoting the document must not close
    the issue the document names — and bodies here quote documents routinely.
    """
    m = _closer()
    assert m.keywords_in("Closes #88") == ["88"]
    assert m.keywords_in("Closes #88, closes #92") == ["88", "92"]
    assert m.keywords_in("Part of #90") == []
    assert m.keywords_in("see #90 and #92") == [], (
        "a bare number with no keyword closes an issue"
    )
    assert m.keywords_in("```\nCloses #88\n```") == [], (
        "a fenced example closes the issue it names"
    )
    assert m.keywords_in("see `Closes #54` in the doc") == [], (
        "an inline code span closes the issue it names"
    )
    assert m.keywords_in("```\nCloses #1\n```\nCloses #88") == ["88"], (
        "prose after a fence stopped being read"
    )
    assert m.MERGED_PR.search("feat: a thing (#100)").group(1) == "100"
    assert m.MERGED_PR.search("fix: the (#61) thing was wrong") is None, (
        "a number mid-subject is read as a merged pull request"
    )


def test_it_closes_the_issue_the_keyword_named_and_nothing_else(monkeypatch):
    """Swapping the key and value in `wanted` would close the pull requests
    instead of the issues, and no string check can see that."""
    m = _closer()
    closed = []
    monkeypatch.setattr(m, "arrived", lambda b, a: ["feat: a thing (#100)"])
    monkeypatch.setattr(m, "pull_request_body", lambda r, n: "Closes #88\ncloses #92")
    monkeypatch.setattr(m, "issue_state", lambda r, n: "closed" if n == 92 else "open")
    monkeypatch.setattr(m, "run", lambda *a: closed.append(a) or "")
    monkeypatch.setenv("AFTER", "x")
    monkeypatch.setenv("REPO", "example/repo")
    monkeypatch.delenv("DRY_RUN", raising=False)
    m.main()
    assert [a[3] for a in closed] == ["88"], (
        f"it closed {[a[3] for a in closed]}. #88 is the open issue the keyword "
        "named; #92 was already closed"
    )


def test_a_number_that_names_nothing_does_not_kill_the_run(monkeypatch):
    """Round 2: the fix for `(#61)` reached one call site and not the other.

    A typo in a merged body — `Closes #9999` — sent a 404 through the shared
    `run`, which exits. Issues after it in sorted order stayed open, and a
    re-run died in the same place."""
    m = _closer()
    closed = []
    monkeypatch.setattr(m, "arrived", lambda b, a: ["feat: a thing (#100)"])
    monkeypatch.setattr(m, "pull_request_body", lambda r, n: "Closes #9999\ncloses #88")
    monkeypatch.setattr(m, "issue_state", lambda r, n: None if n == 9999 else "open")
    monkeypatch.setattr(m, "run", lambda *a: closed.append(a) or "")
    monkeypatch.setenv("AFTER", "x")
    monkeypatch.setenv("REPO", "example/repo")
    monkeypatch.delenv("DRY_RUN", raising=False)
    m.main()
    assert [a[3] for a in closed] == ["88"], (
        f"it closed {[a[3] for a in closed]}. A number naming nothing must be "
        "stepped over, not fatal, and the issues after it must still close"
    )


def test_dry_run_writes_nothing(monkeypatch):
    m = _closer()
    closed = []
    monkeypatch.setattr(m, "arrived", lambda b, a: ["feat: a thing (#100)"])
    monkeypatch.setattr(m, "pull_request_body", lambda r, n: "Closes #88")
    monkeypatch.setattr(m, "issue_state", lambda r, n: "open")
    monkeypatch.setattr(m, "run", lambda *a: closed.append(a) or "")
    monkeypatch.setenv("AFTER", "x")
    monkeypatch.setenv("REPO", "example/repo")
    monkeypatch.setenv("DRY_RUN", "1")
    m.main()
    assert closed == [], (
        "DRY_RUN wrote. It exists because this script was run by hand for its "
        "output during development and closed a real issue"
    )


def test_no_korean_pr_body_claims_a_close_that_did_not_happen():
    """Round 1: two committed `pr.ko.md` files said their pull request closed
    an issue, and neither did.

    `닫습니다` is not a GitHub keyword, so it fired nothing and read as a
    settled fact to anyone opening the file — worse than the dead English
    keyword beside it, which at least looks like machinery. One of the two
    named #54, the issue this work item leaves open on purpose."""
    import glob

    for path in sorted(glob.glob(os.path.join(ROOT, "specs", "*", "pr.ko.md"))):
        text = open(path, encoding="utf-8").read()
        for line in text.splitlines():
            if "닫습니다" in line and "#" in line and "닫히지" not in line:
                raise AssertionError(
                    f"{os.path.relpath(path, ROOT)} claims a close: "
                    f"{line.strip()[:90]} — a feature pull request into "
                    "`release/*` closes nothing, so this reads as a fact that "
                    "is not one"
                )


def test_the_document_says_where_an_issue_actually_closes():
    """Three pull requests wrote a closing keyword into a base that is not the
    default branch, and GitHub closed nothing.

    #89 wrote `Closes #88`, #97 wrote `Closes #54`, #100 wrote `Closes #92`.
    All three merged into the release branch; #88 and #92 were closed by hand
    once somebody noticed and #54 is still open. The squash messages carry no
    keyword either, so the release merge does not fire one as a side effect —
    which leaves the `release/*` to `main` pull request body as the only place
    in the whole sequence where an issue closes at all.

    Four things have to survive together or the rule is not the rule: that a
    feature pull request's keyword does nothing, WHY (its base is not the
    default branch), that the squash message is not a second chance, and where
    the keywords go instead. Deleting any one of them leaves prose.

    Collapsed before matching, because both documents are hand-wrapped and a
    literal match would be asserting their line breaks.
    """
    doc = " ".join(read_text("docs", "branch-and-release.md").split())
    assert "closing keyword does nothing when the base is `release/vX.Y.Z`" in doc, (
        "the document stopped saying which base makes the keyword inert -- "
        "and round 1 found the earlier wording, which blamed the kind of "
        "branch, false for #87: a fix branch straight into `main` whose "
        "`Closes #75` fired"
    )
    assert "The base is what decides this, not the kind of branch" in doc, (
        "the exception went, so a hotfix headed for `main` reads this rule "
        "and throws away a close that would have fired"
    )
    assert "default branch, and that branch is `main`" in doc, (
        "the cause is stated with the wrong branch named as default, which "
        "inverts the whole rule while every other sentence still reads true"
    )
    assert "left no LINK either, though the mention survives" in doc, (
        "the link half went, or came back as the overstatement round 1 "
        "measured false: `closingIssuesReferences` is `[]` and no `connected` "
        "event exists, but the CROSS-REFERENCE does survive -- opening #88 "
        "still shows #89. `no record at all` is the claim to keep out"
    )
    assert "squash commit message does not carry the keyword either" in doc, (
        "nothing rules out the release merge firing the keyword as a side "
        "effect, which is the reading that makes the rule look unnecessary"
    )
    assert "a workflow reads the keywords instead" in doc, (
        "the document names no mechanism that closes an issue at all"
    )
    assert "keyword repeats before every number" in doc, (
        "the collected form lost the reason it repeats the keyword — a bare "
        "`Closes #88, #92` closes one issue of two and reads as though it "
        "closed both"
    )
    # Round 1: every assertion above pins PROSE, and what gets copied into a
    # release pull request body is the CODE BLOCK. Rewriting it to the exact
    # form the paragraph beneath it warns against left all five green.
    # The example is what a person copies. Round 1 rewrote it into the exact
    # form the paragraph beneath warns against and every prose assertion
    # stayed green, so the block itself is pinned.
    assert "```\nCloses #88\n```" in read_text("docs", "branch-and-release.md"), (
        "the example block went, or grew back into a list -- one keyword and "
        "one number is what a feature pull request writes, and it is the only "
        "form the workflow reads"
    )
    assert "skipped rather than\n" not in doc  # collapsed doc; guard the phrase below
    assert "an issue already closed is skipped rather than" in doc, (
        "the workflow's only-ever-closes property left the document, which is "
        "what makes a re-run safe to reason about"
    )
    assert "A force-push is a different case and not a safe one" in doc, (
        "the document went back to calling a force-push harmless. It is not "
        "idempotent, it FAILS -- GitHub sends the displaced SHA and the range "
        "cannot be resolved -- and the two are different claims"
    )
    assert "sanctions no shorter form" in doc, (
        "the reason the keyword repeats went. It is what the documentation "
        "PRESCRIBES -- an earlier draft asserted the bare list closes only "
        "the first issue, which no source says and round 1 caught"
    )
    assert "`Part of #N` remains the form" in doc, (
        "the feature-pull-request form is gone -- the rule now says what does "
        "not work and nothing about what to write instead"
    )
    # The rule has to sit INSIDE the release sequence. `plan.md` rejected
    # appending it to the end of the file in writing, and moving it there was
    # green: a substring search reads a document as a bag of sentences.
    shapes = doc.index("The two merge shapes are not interchangeable")
    rule = doc.index("closing keyword does nothing when the base is")
    version = doc.index("The version is provisional until the content settles")
    assert shapes < rule < version, (
        "the rule left the release sequence -- a reader walking the sequence "
        "to write the release pull request no longer arrives at it"
    )
    assert "by a workflow rather than by anybody's hand" in doc, (
        "the bullet a sequence reader meets first went back to naming the "
        "release pull request body as the place an issue closes. It sat sixty "
        "lines above the paragraph that replaced it, so a reader walking the "
        "sequence got the old answer and stopped -- and then wrote no "
        "`Closes #N` for the workflow to read"
    )
    for pr in ("#37", "#38", "#39"):
        assert pr in doc, (
            f"{pr} is gone — a rule with no incident behind it is prose, and "
            "these three are what the rule was written from"
        )
    pointer = " ".join(read_text("CONTRIBUTING.md").split())
    assert "which issues a release closes" in pointer, (
        "CONTRIBUTING's release section stopped naming this among what "
        "`docs/branch-and-release.md` holds, so a reader deciding whether to "
        "open it before a merge is not told the answer is in there"
    )


def test_the_pull_request_checks_the_chain_it_was_routed_to():
    """The step cannot be dropped without a failure here.

    Moving enforcement off the commit and onto the pull request is only
    honest while the pull request actually checks. A workflow with the
    declaration and no step is the standing waiver `docs/review-chain-spec.md`
    refuses to build — quieter than the one it replaced, because a declaration
    that nothing reads leaves no trace at all.
    """
    workflow = open(
        os.path.join(ROOT, ".github", "workflows", "hygiene.yml"), encoding="utf-8"
    ).read()
    assert "chain_check.py" in workflow, "the chain check is not wired into CI"
    assert "--baseline" in workflow
    assert os.path.isfile(
        os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
    ), "the workflow calls a script that is not there"


def test_this_repository_carries_no_scratch_marker():
    """`.specseal/scratch` turns every gate off for the repository holding it.

    It is an opt-out for a repository built to be thrown away, and
    `.specseal/` is committed by design — so one committed here would silence
    the review gate, the migration gate and the review-skill gate in every
    clone, with nothing in a diff that reads as "the workflow was switched
    off". A repository that runs the review chain on itself is the last place
    it belongs, and this is the only check that would notice.
    """
    marker = os.path.join(ROOT, ".specseal", "scratch")
    assert not os.path.exists(marker), (
        "this repository carries .specseal/scratch, which silences every gate "
        "in every clone. Delete it — it is for a scratch repository, never for "
        "one under review"
    )


def test_the_chain_check_reuses_the_reader_rather_than_writing_a_second():
    """Two readers of the same markdown drifted apart in four places across
    three review rounds here, and closing one pair opened another. A 🔴 inside
    a comment or a fenced block has to be invisible to both."""
    check = open(
        os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py"),
        encoding="utf-8",
    ).read()
    assert "unverified_check.py" in check
    assert "reader.readable(" in check, (
        "the check reads lines the shared reader never normalized"
    )
    assert "def split_row" not in check, "a second row reader"
