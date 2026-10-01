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

import os
import subprocess

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
    write_config(home, table(("Reference specs", "specs/, docs/adr ,./design/")))
    roots = config.reference_roots(home)
    assert roots == ("specs", "docs/adr", "design"), roots
    for rel in ("specs/x/spec.md", "docs/adr/0001.md", "design/a.md", "specs"):
        assert config.under_reference_root(rel, roots), rel
    for rel in ("docs/adrs/0001.md", "docs/specs/x.md", "src/specs.py", "spec/x"):
        assert not config.under_reference_root(rel, roots), rel


def test_no_row_means_every_specs_directory_outside_the_root(tmp_path):
    """Absent, empty or unreadable: the ticket's default, at any depth."""
    home = str(tmp_path / "seal")
    for body in (None, table(("Mode", "shared")), table(("Reference specs", ""))):
        if body is not None:
            write_config(home, body)
        roots = config.reference_roots(home)
        assert roots is None, (body, roots)
        for rel in ("specs/x/spec.md", "docs/specs/y.md", "a/b/specs/c/d.md"):
            assert config.under_reference_root(rel, roots), rel
        for rel in ("seal/specs/1790000000-x/spec.md", "docs/spec.md", "specsheet/a"):
            assert not config.under_reference_root(rel, roots), rel
    assert config.reference_roots("") is None, "no root is the default, not a crash"


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
