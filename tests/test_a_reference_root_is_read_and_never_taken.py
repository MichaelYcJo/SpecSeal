"""A project's own `specs/` is read as history and never taken (#688).

A person joining a project that kept its own `specs/` before the plugin
arrived used to have it read as the plugin's: moved into `seal/` at session
start, and searched as a record by the checks. The plugin writes only to its
own root. Every other directory named `specs` is a REFERENCE ROOT — read when
a change touches what it describes, cited where it was read, and never moved,
edited, absorbed or deleted.

`seal/config.md`'s `Reference specs` row names the reference roots, and with
no row every directory named `specs` outside the plugin's root is one. The row
has one reader, `hooks/config.py#reference_roots`, and one predicate,
`hooks/config.py#under_reference_root`; every check that would read a
reference root as a record asks that predicate instead of spelling its own
test. The cases below are the resolver's (C1); the checks' cases sit beside
each check's own (D1, D2, D3), and this file's last section names every
shipped check and what keeps it off a reference root.
"""

import importlib.util
import os
import re
import subprocess
import sys

from conftest import load_hook_module

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

config = load_hook_module("config.py", "config_for_reference_roots")


def write_config(home, body):
    os.makedirs(home, exist_ok=True)
    with open(os.path.join(home, "config.md"), "w", encoding="utf-8") as handle:
        handle.write(body)


def table(*rows):
    return "# config\n\n| Item | Value |\n|---|---|\n" + "".join(
        f"| {item} | {value} |\n" for item, value in rows
    )


# --- C1: the row and its default --------------------------------------------


def test_the_row_names_its_prefixes_with_or_without_a_slash(tmp_path):
    """Present: the prefixes it names, normalised, and nothing else."""
    home = str(tmp_path / "seal")
    write_config(
        home,
        table(("Reference specs", "specs/, docs/adr ,./design/, specs, tools\\notes")),
    )
    roots = config.reference_roots(home)
    assert roots == ("specs", "docs/adr", "design", "tools/notes"), roots
    for rel in (
        "specs/x/spec.md",
        "docs/adr/0001.md",
        "design/a.md",
        "specs",
        "./specs/x.md",
        "tools/notes/n.md",
    ):
        assert config.under_reference_root(rel, roots), rel
    for rel in ("docs/adrs/0001.md", "docs/specs/x.md", "src/specs.py", "spec/x"):
        assert not config.under_reference_root(rel, roots), rel


def test_no_row_means_every_specs_directory_outside_the_root(tmp_path, monkeypatch):
    """Absent, empty or unreadable: the ticket's default, at any depth."""
    home = str(tmp_path / "seal")
    for body in (None, table(("Mode", "shared")), table(("Reference specs", ""))):
        if body is not None:
            write_config(home, body)
        roots = config.reference_roots(home)
        assert roots is None, (body, roots)
        for rel in (
            "specs/x/spec.md",
            "docs/specs/y.md",
            "a/b/specs/c/d.md",
            "specs\\x\\spec.md",
        ):
            assert config.under_reference_root(rel, roots), rel
        for rel in ("seal/specs/1790000000-x/spec.md", "docs/spec.md", "specsheet/a"):
            assert not config.under_reference_root(rel, roots), rel
    # No root at either place is no reference root at all: the repository has
    # not opted in, and the 0.3.x `specs/` the checks still read was the
    # plugin's own. Never a `config.md` found relative to wherever the
    # process happens to stand, either.
    stray = tmp_path / "elsewhere"
    write_config(str(stray), table(("Reference specs", "docs/adr")))
    monkeypatch.chdir(stray)
    assert config.reference_roots("") == ()
    assert not config.under_reference_root("specs/x/spec.md", ())


def test_none_declares_no_reference_root(tmp_path):
    home = str(tmp_path / "seal")
    write_config(home, table(("Reference specs", "None")))
    roots = config.reference_roots(home)
    assert roots == (), roots
    assert not config.under_reference_root("specs/x/spec.md", roots)


def test_a_row_inside_a_fence_is_not_a_row(tmp_path):
    """`hooks/config.py#unfenced` filters in front of the table walk, so a
    row quoted in a fence above the live table is an example."""
    home = str(tmp_path / "seal")
    write_config(
        home,
        "# config\n\n```markdown\n| Item | Value |\n|---|---|\n"
        "| Reference specs | none |\n```\n\n"
        + table(("Mode", "shared")).split("\n\n", 1)[1],
    )
    assert config.reference_roots(home) is None


def test_the_plugins_own_root_is_never_a_reference_root(tmp_path):
    """A reference root is outside the root by definition; a prefix naming
    `seal/` or anything under it is dropped, and the default never reaches
    `seal/specs/` either."""
    home = str(tmp_path / "seal")
    write_config(home, table(("Reference specs", "seal/specs, seal, specs")))
    roots = config.reference_roots(home)
    assert roots == ("specs",), roots
    assert not config.under_reference_root("seal/specs/1790000000-x/spec.md", roots)
    assert not config.under_reference_root("seal/specs/1790000000-x/spec.md", None)
    optin = load_hook_module("optin.py", "optin_for_the_root_name")
    assert config.HOME == optin.HOME, "the reader spells the root another way"


def test_local_mode_reads_the_row_under_the_git_directory(tmp_path):
    """In local mode the root sits under the common git directory and nothing
    of it is in the tree, so with no row every tree `specs` is a reference
    root — and a row there is read like any other."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    optin = load_hook_module("optin.py", "optin_for_reference_roots")
    common = optin.git_common_dir(str(repo))
    home = os.path.join(common, "seal")
    os.makedirs(home)
    assert optin.home_at(str(repo), common) == home, "the fixture is not local mode"
    assert config.reference_roots(home) is None
    assert config.under_reference_root("specs/x/spec.md", None)
    write_config(home, table(("Reference specs", "docs/adr")))
    assert config.reference_roots(home) == ("docs/adr",)


# --- D3: every shipped check, and what keeps it off a reference root ---------
#
# The failure this file's plan names for six months out: a check added later
# walks the tree without asking the predicate, and the class reopens one
# script at a time. So every command `bin/` ships is named here with what
# keeps it off a team's `specs/`, and a command nobody classified turns this
# red. A check that walks no `specs/` says so; one pinned to the root names
# the constant it rests on, which the case below holds under `seal/`.

PREDICATE = "asks hooks/config.py#under_reference_root"
PINNED = "reads the plugin's root by a constant under seal/"
NO_WALK = "walks no specs/ directory"
NOT_A_CHECK = "is not a check of the tree"

SHIPPED = {
    "survivor-check": (PREDICATE, "pool and range, through a_reference_root"),
    "unverified-check": (PREDICATE, "the walk and the base, by one rule"),
    "settle": (PINNED, "settle.py#SPECS; its citation scan reads as a citer"),
    "correction-check": (PINNED, "correction_check.py#LEDGER/FRAGMENTS/RELEASES"),
    "evidence-check": (
        PINNED,
        "evidence_check.py#default_patterns; the tree corpus reads as the tree",
    ),
    "round-record": (PINNED, "writes rounds/ under seal/specs/<id>/ only"),
    "broad-gate": (NO_WALK, "hands seal/specs/ to the checks above"),
    "fold-check": (NO_WALK, "reads the top level of docs/ and seal/config.md"),
    "arm-check": (NO_WALK, "reads the Python files it is named"),
    "mutation-check": (NO_WALK, "breaks and restores the one file it is named"),
    "deferral-check": (NO_WALK, "reads the pull request body and round records"),
    "seal": (NOT_A_CHECK, "the mode command, writing seal/config.md"),
    "seal-stamp": (NOT_A_CHECK, "draws the sealer's stamp"),
    "session-cost": (NOT_A_CHECK, "measures a transcript"),
    "payload-meter": (NOT_A_CHECK, "measures a spawn's payload"),
    "test": (NOT_A_CHECK, "this repository's own suite runner"),
}


def load_script(*parts):
    path = os.path.join(ROOT, *parts)
    spec = importlib.util.spec_from_file_location(
        "specseal_" + parts[-1].replace(".", "_") + "_for_reference_roots", path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_shipped_command_is_classified():
    shipped = {
        name
        for name in os.listdir(os.path.join(ROOT, "bin"))
        if not name.endswith(".cmd")
    }
    assert shipped == set(SHIPPED), (
        "a command in bin/ is not classified here, or a classified one left: "
        f"{sorted(shipped ^ set(SHIPPED))}. Say what keeps it off a team's "
        "specs/ — the predicate, a constant under seal/, or no walk at all"
    )


def test_the_pinned_checks_read_under_the_root_alone(tmp_path):
    """Each constant a pinned check rests on, held under `seal/`. Widening one
    to a top-level `specs/` turns this red, which is the probe the plan names
    for `SPECS`, `LEDGER`/`FRAGMENTS`/`RELEASES` and `WORK_ITEMS`."""
    settle = load_script("skills", "settle", "scripts", "settle.py")
    assert settle.SPECS == "seal/specs"
    correction = load_script(
        "skills", "evidence-check", "scripts", "correction_check.py"
    )
    for name in ("LEDGER", "FRAGMENTS", "RELEASES"):
        assert getattr(correction, name).startswith("seal/"), name
    routing = load_hook_module("routing.py", "routing_for_reference_roots")
    assert routing.WORK_ITEMS == "seal/specs"
    evidence = load_script("skills", "evidence-check", "scripts", "evidence_check.py")
    (tmp_path / "seal").mkdir()
    patterns = [
        os.path.relpath(p, tmp_path).replace(os.sep, "/")
        for p in evidence.default_patterns(str(tmp_path))
    ]
    assert patterns == [
        "seal/ledger.md",
        "seal/ledger/*.md",
        "seal/releases/*.md",
        "docs/**/_evidence.md",
    ], patterns


# A repository with a `seal/` root holding one work item and one ledger row,
# built twice: once alone, and once with a team's own `specs/` planted beside
# it — a malformed overview, a spec, and a design note, edited in the second
# commit. Every check below must say the same thing about both.
SERVICE = "def handler(x):\n    return x + 1\n"
OURS = "seal/specs/1790000000-ours"
TEAM = "specs/1788000001-team-thing"


def planted(where, team):
    def git(*args):
        subprocess.run(
            ["git", "-C", str(where), *args], check=True, capture_output=True
        )

    def put(rel, text):
        path = where / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    where.mkdir(parents=True)
    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    put("src/service.py", SERVICE)
    put(f"{OURS}/routing.md", "# routing\n\n| Axis | Answer |\n|---|---|\n")
    put(f"{OURS}/overview.md", "# ours\n\n## Not verified\n\nnone — a probe\n")
    put("seal/ledger.md", "# ledger\n\n| Clause | Coordinate |\n|---|---|\n")
    if team:
        put(f"{TEAM}/spec.md", "# the team's spec\n\nA design they own.\n")
        put(f"{TEAM}/overview.md", "# theirs\n\n## Not verified\n\nnot a table\n")
        put(f"{TEAM}/design.md", "# design\n\n| Clause | Coordinate |\n|---|---|\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    # The second commit arrives by a merge, so `correction-check` has a merge
    # to read the ledger listing at rather than stopping before it reads.
    git("switch", "-qc", "side")
    put("src/service.py", SERVICE + "\n\ndef other():\n    return 0\n")
    if team:
        put(f"{TEAM}/design.md", "# design\n\nRewritten by the team.\n")
    git("add", "-A")
    git("commit", "-qm", "second")
    git("switch", "-q", "main")
    git("merge", "-q", "--no-ff", "-m", "merge", "side")
    return where


CHECKS = {
    "evidence-check": ("skills/evidence-check/scripts/evidence_check.py", ["{r}"]),
    "correction-check": (
        "skills/evidence-check/scripts/correction_check.py",
        ["--range", "HEAD~1..HEAD", "--root", "{r}"],
    ),
    "chain_check.py": (
        "skills/code-review/scripts/chain_check.py",
        ["--baseline", "HEAD~1", "--root", "{r}"],
    ),
    "unverified-check": ("skills/verify/scripts/unverified_check.py", ["{r}"]),
    "settle": (
        "skills/settle/scripts/settle.py",
        ["--root", "{r}", "--released-at", "HEAD"],
    ),
}


def test_a_planted_team_specs_changes_no_checks_verdict(tmp_path):
    """D3. Each check run over the repository with and without the team's
    `specs/` exits the same and prints the same, with the repository's own
    path written out of both; and the team's directory is on disk, untouched,
    after all of them."""
    alone = planted(tmp_path / "alone", team=False)
    joined = planted(tmp_path / "joined", team=True)
    before = {
        rel: (joined / TEAM / rel).read_bytes()
        for rel in ("spec.md", "overview.md", "design.md")
    }
    for name, (script, args) in CHECKS.items():
        said = []
        for repo in (alone, joined):
            r = subprocess.run(
                [sys.executable, os.path.join(ROOT, script)]
                + [a.replace("{r}", str(repo)) for a in args],
                cwd=str(repo),
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )
            # The two repositories' paths and commits differ by construction.
            text = re.sub(
                r"\b[0-9a-f]{7,40}\b",
                "<sha>",
                (r.stdout + r.stderr).replace(str(repo), "<repo>"),
            )
            said.append((r.returncode, text))
        assert said[0] == said[1], (
            f"{name} says something else once a team's specs/ is planted:\n"
            f"alone:\n{said[0]}\njoined:\n{said[1]}"
        )
        assert "team-thing" not in said[1][1], f"{name} read the team's specs/"
    for rel, data in before.items():
        assert (joined / TEAM / rel).read_bytes() == data, rel


# --- C2: the readers read a reference root when relevant, and cite it --------
#
# Each party that reads the tree for a decision is told, in its own file, that
# a reference root is history: read where the work touches what it describes,
# cited where it was read, and never written. Each names the row by pointing
# at `templates/config.md` §*Reference specs* rather than restating its
# grammar, so the grammar has one home.

POINTER = "`templates/config.md` §*Reference specs*"
READERS = {
    "agents/framer.md": ("cite", "spec.md"),
    "agents/smith.md": ("cite", "spec.md"),
    "agents/warden.md": ("stage 1", "spec.md"),
    "skills/settle/SKILL.md": ("cite", "standing statement"),
    "skills/implement/SKILL.md": ("cite", "spec.md"),
}


def paragraph_naming(text, phrase):
    """The blank-line-bounded block that holds `phrase`, its breaks folded."""
    at = text.index(phrase)
    start = text.rfind("\n\n", 0, at) + 2
    end = text.find("\n\n", at)
    return " ".join(text[start : end if end >= 0 else None].split())


def test_each_reader_says_when_it_reads_a_reference_root_and_where_it_cites_it():
    for rel, (act, where) in READERS.items():
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        assert POINTER in text, f"{rel} does not point at the row's section"
        said = paragraph_naming(text, POINTER)
        assert "touches what" in said and "describes" in said, (rel, said)
        assert act in said and where in said, (rel, said)
        assert re.search(r"\bnever writ", said), (rel, said)


def test_the_seal_readme_says_nothing_writes_the_old_names():
    """The sentence used to say nothing READS a top-level `specs/`, which a
    reference root now contradicts; what is true of it is that nothing
    writes there, and what moves is the plugin's own marked work items."""
    for rel in ("templates/seal-README.md", "seal/README.md"):
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        flat = " ".join(text.split())
        assert "Nothing writes `.specseal/` or a top-level `specs/`" in flat, rel
        assert "Nothing reads `.specseal/`" not in flat, rel
        assert "`routing.md` or `rounds/`" in flat, rel
