"""evidence-check's records arm: what a live work item's records say is there.

A ledger row is a claim about the tree that something reads. A record --
`spec.md`, `plan.md`, `overview.md`, `rounds/round-N.md`, `phases/phase-N.md`
-- states the same kind of thing and nothing reads it (#190). This file holds
the boundary that decides whose records are read, the identifier arm, the
stamp arm, and the escape hatch.

**No fixture here runs git.** The boundary is the presence of a file and the
arms resolve content, the way `test_a_row_points_by_content.py` does.
"""

import importlib.util
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def module():
    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def home(tmp_path):
    """A `seal/` root with `specs/` and `ledger/` under it."""
    h = tmp_path / "seal"
    (h / "specs").mkdir(parents=True)
    (h / "ledger").mkdir(parents=True)
    return h


def work_item(h, item, fragment=True, **files):
    """A work item directory, with or without its ledger fragment.

    `fragment=False` is a work item that has shipped: the release folded its
    rows into the gathered ledger and removed the file.
    """
    d = h / "specs" / item
    d.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        path = d / name.replace("__", "/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if fragment:
        (h / "ledger" / f"{item}.md").write_text(
            "| Clause | Coordinate | Grounds | Checked |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    return d


# --- the boundary: has this work item shipped -------------------------------


def test_a_work_item_with_a_ledger_fragment_has_not_shipped(tmp_path):
    h = home(tmp_path)
    work_item(h, "1780000000-live", **{"spec.md": "# live\n"})
    assert set(module().unshipped(str(h))) == {"1780000000-live"}


def test_a_work_item_whose_fragment_was_folded_away_has_shipped(tmp_path):
    h = home(tmp_path)
    work_item(h, "1780000000-shipped", fragment=False, **{"spec.md": "# shipped\n"})
    assert module().unshipped(str(h)) == {}


def test_the_boundary_reads_the_fragments_beside_the_specs(tmp_path):
    """Two work items, one folded — only the unfolded one is live.

    The pair, not either alone: a reader that returned everything and a
    reader that returned nothing both pass a single-arm case.
    """
    h = home(tmp_path)
    work_item(h, "1780000000-live", **{"spec.md": "# a\n"})
    work_item(h, "1770000000-shipped", fragment=False, **{"spec.md": "# b\n"})
    assert set(module().unshipped(str(h))) == {"1780000000-live"}


def test_a_fragment_whose_records_are_not_here_is_not_a_work_item(tmp_path):
    """`seal export` carries the records out and leaves the fragment.

    An arm that reads records has nothing to say about a work item that has
    none in this tree, and returning the id would make every caller check the
    directory again.
    """
    h = home(tmp_path)
    (h / "ledger" / "1780000000-carried-out.md").write_text("rows\n", encoding="utf-8")
    assert module().unshipped(str(h)) == {}


def test_a_directory_in_the_fragment_folder_is_not_a_fragment(tmp_path):
    h = home(tmp_path)
    work_item(h, "1780000000-live", fragment=False, **{"spec.md": "# a\n"})
    (h / "ledger" / "1780000000-live.md").mkdir()
    assert module().unshipped(str(h)) == {}


def test_a_root_with_no_fragment_folder_reads_as_nothing_live(tmp_path):
    """A repository that has never written a fragment, not a crash."""
    h = tmp_path / "seal"
    (h / "specs").mkdir(parents=True)
    assert module().unshipped(str(h)) == {}


def test_the_records_read_are_every_md_in_the_work_item(tmp_path):
    """The whole SDD set, not the round records alone.

    #190's three instances landed in a `plan.md`, an `overview.md` and a
    ledger row; nothing here reads a file name to decide.
    """
    h = home(tmp_path)
    d = work_item(
        h,
        "1780000000-live",
        **{
            "spec.md": "# a\n",
            "overview.md": "# b\n",
            "rounds__round-1.md": "# c\n",
            "phases__phase-1.md": "# d\n",
            "notes.txt": "not a record\n",
        },
    )
    found = {
        os.path.relpath(p, str(d)).replace(os.sep, "/")
        for p in module().record_files(str(d))
    }
    assert found == {
        "spec.md",
        "overview.md",
        "rounds/round-1.md",
        "phases/phase-1.md",
    }


def test_the_walk_does_not_descend_into_a_cache(tmp_path):
    """A `__pycache__` under a work item is not a record.

    The same reason the name corpus skips one: build output carries copies of
    names the tree no longer has.
    """
    h = home(tmp_path)
    d = work_item(h, "1780000000-live", **{"spec.md": "# a\n"})
    (d / "__pycache__").mkdir()
    (d / "__pycache__" / "stale.md").write_text("# stale\n", encoding="utf-8")
    found = [os.path.basename(p) for p in module().record_files(str(d))]
    assert found == ["spec.md"]


def test_the_cli_still_runs_with_the_boundary_in_place(tmp_path):
    """The arm is wired in later; nothing about phase 1 changes the CLI."""
    (tmp_path / "seal").mkdir()
    r = run(["."], tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "no evidence ledgers found" in r.stdout
