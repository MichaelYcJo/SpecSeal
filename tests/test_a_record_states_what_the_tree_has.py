"""evidence-check's records arm: what a live work item's records say is there.

A ledger row is a claim about the tree that something reads. A record --
`spec.md`, `plan.md`, `overview.md`, `rounds/round-N.md`, `phases/phase-N.md`
-- states the same kind of thing and nothing reads it (#190). This file holds
the boundary that decides whose records are read, the identifier arm, the
stamp arm, and the escape hatch.

**No fixture here runs git, and no fixture here may.** The checker calls git
for nothing outside `--migrate` (`README.md` §*A row carries no line number
and no commit*), so a fixture that needed an index would be pinning behaviour
the checker is not allowed to have. The boundary is the presence of a file
and the arms resolve content, the way `test_a_row_points_by_content.py` does.
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


def test_a_repository_with_no_records_reads_as_nothing_to_check(tmp_path):
    (tmp_path / "seal").mkdir()
    r = run(["."], tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "no evidence ledgers found" in r.stdout


# --- the identifier arm: a name the tree does not have ----------------------


def tree(tmp_path, **files):
    """Files outside `seal/`, which is what the name corpus is built from."""
    for name, text in files.items():
        path = tmp_path / name.replace("__", "/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def refusals(tmp_path):
    findings, read, _stamps = module().check_records(
        str(tmp_path), str(tmp_path / "seal")
    )
    return [(status, coord, detail) for status, coord, detail in findings], read


def test_a_live_record_naming_a_unit_the_tree_lacks_is_refused(tmp_path):
    h = home(tmp_path)
    tree(tmp_path, **{"mod.py": "def kept_helper():\n    return 1\n"})
    work_item(
        h,
        "1780000000-live",
        **{"rounds__round-2.md": "# r\n\nthe alias `gone_helper` has one call site\n"},
    )
    found, read = refusals(tmp_path)
    assert read == 1
    assert len(found) == 1
    status, coord, detail = found[0]
    assert status == "NOT-IN-TREE"
    assert coord.endswith("rounds/round-2.md:3")
    assert "`gone_helper`" in detail


def test_the_refusal_names_the_file_the_line_and_the_name(tmp_path):
    """All three, because a class is enumerated from a coordinate.

    A refusal that named the file alone would send the reader through a
    record looking for which of its backticks moved.
    """
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{"plan.md": "# p\n\n\n\nphase 2 builds `gone_helper` here\n"},
    )
    found, _ = refusals(tmp_path)
    coord, detail = found[0][1], found[0][2]
    assert coord.replace(os.sep, "/").endswith("1780000000-live/plan.md:5")
    assert "`gone_helper`" in detail


def test_a_shipped_work_items_record_is_left_alone(tmp_path):
    """129 occurrences sit in this repository's shipped records and they are
    history — a plan proposing a helper built under another name is a correct
    record of what was decided then."""
    h = home(tmp_path)
    work_item(
        h,
        "1770000000-shipped",
        fragment=False,
        **{"plan.md": "# p\n\nbuild `gone_helper`\n"},
    )
    assert refusals(tmp_path) == ([], 0)


def test_a_name_the_tree_carries_passes(tmp_path):
    h = home(tmp_path)
    tree(tmp_path, **{"mod.py": "def kept_helper():\n    return 1\n"})
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`kept_helper` stays\n"})
    assert refusals(tmp_path) == ([], 1)


def test_a_file_name_is_a_name_the_tree_carries(tmp_path):
    """A record naming `test_foo` is naming a module as often as a function."""
    h = home(tmp_path)
    tree(tmp_path, **{"tests__test_the_thing.py": "x = 1\n"})
    work_item(
        h, "1780000000-live", **{"plan.md": "# p\n\n`test_the_thing` covers it\n"}
    )
    assert refusals(tmp_path) == ([], 1)


def test_a_single_word_name_is_not_read_as_a_claim(tmp_path):
    """`cmp`, `rpartition`, `Starred` — a shell command, a str method and an
    ast node. Nineteen such names sit in this repository's records and not one
    is a claim about a unit, so the pattern is narrowed rather than the
    exemption widened."""
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{"plan.md": "# p\n\nthe reviewer ran `cmp` and read `rpartition`\n"},
    )
    assert refusals(tmp_path) == ([], 0)


def test_the_marker_exempts_the_line(tmp_path):
    """The escape hatch a reviewer already writes beside a proposed name."""
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{"rounds__round-1.md": "# r\n\n`gone_helper` — NAME NOT IN TREE\n"},
    )
    assert refusals(tmp_path) == ([], 0)


def test_the_marker_exempts_the_line_and_not_the_name(tmp_path):
    """Marked on one line, the same name is still a claim on the next.

    The exemption is a marker on the LINE for the reason `plan.md` gives: a
    list inside the checker gets widened by whoever is annoyed, and a name
    exempted once would be exempt everywhere it is claimed afterwards.
    """
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{
            "rounds__round-1.md": (
                "# r\n\n`gone_helper` — NAME NOT IN TREE\n\n"
                "and `gone_helper` is what the module calls\n"
            )
        },
    )
    found, _ = refusals(tmp_path)
    assert len(found) == 1
    assert found[0][1].endswith(":5")


def test_a_cache_in_the_tree_does_not_supply_a_name(tmp_path):
    """A compiled module carries its own identifiers in its constants pool,
    so a corpus that reads one answers "still there" for a name the tree lost
    at the last commit."""
    h = home(tmp_path)
    cache = tmp_path / "__pycache__"
    cache.mkdir()
    (cache / "mod.cpython-312.pyc").write_text("gone_helper\n", encoding="utf-8")
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper`\n"})
    found, _ = refusals(tmp_path)
    assert len(found) == 1


def test_a_binary_file_does_not_supply_a_name(tmp_path):
    """A compiled artefact outside a cache directory is still not the tree.

    Decoded with `errors="replace"`, a `.pyc`, an archive or an image yields
    token-shaped runs from its own bytes, and a name that turns up there is a
    name nobody wrote. The failure that guard prevents is a false PASS, which
    is the expensive direction: the record keeps a claim that is not true.
    """
    h = home(tmp_path)
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "thing.bin").write_bytes(b"\x00\x01gone_helper\x00")
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper`\n"})
    found, _ = refusals(tmp_path)
    assert len(found) == 1


def test_the_records_own_directory_is_not_its_own_corpus(tmp_path):
    """A name that only another work item's record carries is still a name
    the tree does not have."""
    h = home(tmp_path)
    work_item(
        h, "1770000000-shipped", fragment=False, **{"plan.md": "# p\n\n`gone_helper`\n"}
    )
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper`\n"})
    found, _ = refusals(tmp_path)
    assert len(found) == 1
    assert "1780000000-live" in found[0][1]


def test_a_work_items_own_ledger_fragment_is_not_part_of_the_corpus(tmp_path):
    """A fragment is the work item writing about itself, same branch and same
    lifetime as the records beside it.

    Found while writing this work item's own rows: naming four units in the
    fragment put them in the corpus and silenced four refusals in its own
    `phase-2.md`. A work item could clear the check on its records by naming
    the unit in its own ledger file.
    """
    h = home(tmp_path)
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper` is gone\n"})
    (h / "ledger" / "1780000000-live.md").write_text(
        "| Clause | Coordinate |\n|---|---|\n| R1 · `gone_helper` went | x |\n",
        encoding="utf-8",
    )
    found, _ = refusals(tmp_path)
    assert len(found) == 1
    assert "`gone_helper`" in found[0][2]


def test_the_gathered_ledger_is_part_of_the_corpus(tmp_path):
    """`seal/ledger.md` keeps a renamed unit's old name beside the new one on
    purpose, so a reader coming from an older record can follow it. Excluding
    the whole of `seal/` refuses five such occurrences in this repository."""
    h = home(tmp_path)
    (h / "ledger.md").write_text(
        "| Clause | Coordinate |\n|---|---|\n"
        "| R1 · renamed from `gone_helper` | `mod.py#kept@deadbeef` |\n",
        encoding="utf-8",
    )
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper` was renamed\n"})
    assert refusals(tmp_path)[0] == []


def test_a_refusal_fails_the_run(tmp_path):
    h = home(tmp_path)
    (h / "ledger" / "1780000000-live.md").write_text("rows\n", encoding="utf-8")
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper`\n"})
    r = run(["."], tmp_path)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "NOT-IN-TREE" in r.stdout
    assert "1 refused" in r.stdout


def test_the_records_arm_runs_even_when_a_narrowing_finds_no_ledger(tmp_path):
    """`--ledger` narrows the LEDGERS read; it says nothing about records, and
    a narrowing that matched none must not silence the other arm."""
    h = home(tmp_path)
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper`\n"})
    r = run(["--ledger", "nothing/here/*.md", "."], tmp_path)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "NOT-IN-TREE" in r.stdout


# --- the corpus reaches a local-mode root (round 1, 🟡 4) -------------------


def test_the_gathered_ledger_is_in_the_corpus_in_local_mode_too(tmp_path):
    """Identical bytes answered exit 0 shared and exit 2 local.

    In local mode `seal/` sits under the git common directory, which every
    walk here prunes with `.git` — so `seal/ledger.md`, which is IN the
    corpus by design, was dropped for no reason but where the root happens to
    sit.
    """
    (tmp_path / "mod.py").write_text("def kept_helper():\n    return 1\n")
    local = tmp_path / ".git" / "seal"
    (local / "specs").mkdir(parents=True)
    (local / "ledger").mkdir(parents=True)
    work_item(local, "1780000000-live", **{"plan.md": "# p\n\n`renamed_helper`\n"})
    (local / "ledger.md").write_text(
        "| S1 | `mod.py#renamed_helper@00000000` | read | 2026-09-07 |\n",
        encoding="utf-8",
    )
    findings, read, _stamps = module().check_records(str(tmp_path), str(local))
    assert (findings, read) == ([], 1)


# --- the stamp arm: an anchor a record wrote down ---------------------------

SERVICE = "def handler(x):\n    return x + 1\n"
# `handler`'s body, hashed the way the checker hashes it. Pinned rather than
# computed, so a fixture cannot agree with a broken hasher.
GOOD = "9207ed06"


def test_a_stamp_the_tree_contradicts_is_named(tmp_path):
    """#190's own worked example: an `overview.md` naming an anchor stamp the
    tree no longer holds."""
    h = home(tmp_path)
    tree(tmp_path, **{"src__service.py": "def handler(x):\n    return x + 2\n"})
    work_item(
        h,
        "1780000000-live",
        **{"overview.md": f"# o\n\nstamped `src/service.py#handler@{GOOD}`\n"},
    )
    findings, _names, stamps = module().check_records(
        str(tmp_path), str(tmp_path / "seal")
    )
    assert stamps == 1
    assert len(findings) == 1
    status, coord, detail = findings[0]
    assert status == "DRIFTED"
    assert coord.endswith("overview.md:3")
    assert "src/service.py#handler" in detail


def test_a_stamp_naming_a_file_the_tree_lacks_is_broken(tmp_path):
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{"plan.md": "# p\n\nthe fixture `mod.py#helper@deadbeef`\n"},
    )
    findings, _names, _stamps = module().check_records(
        str(tmp_path), str(tmp_path / "seal")
    )
    assert [f[0] for f in findings] == ["BROKEN"]
    assert findings[0][1].endswith("plan.md:3")


def test_a_stamp_the_tree_still_holds_passes(tmp_path):
    h = home(tmp_path)
    tree(tmp_path, **{"src__service.py": SERVICE})
    work_item(
        h,
        "1780000000-live",
        **{"overview.md": f"# o\n\n`src/service.py#handler@{GOOD}`\n"},
    )
    findings, _names, stamps = module().check_records(
        str(tmp_path), str(tmp_path / "seal")
    )
    assert (findings, stamps) == ([], 1)


def test_the_marker_exempts_a_stamp_line_too(tmp_path):
    """One marker, named in one place. `plan.md` and a round record in this
    repository both carry the fixture stamp `mod.py#helper@deadbeef`, which is
    exactly the shape the marker exists for."""
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{"plan.md": "# p\n\n`mod.py#helper@deadbeef` — NAME NOT IN TREE\n"},
    )
    assert module().check_records(str(tmp_path), str(tmp_path / "seal")) == ([], 0, 0)


def test_a_shipped_work_items_stamp_is_left_alone(tmp_path):
    h = home(tmp_path)
    work_item(
        h,
        "1770000000-shipped",
        fragment=False,
        **{"overview.md": f"# o\n\n`src/service.py#handler@{GOOD}`\n"},
    )
    assert module().check_records(str(tmp_path), str(tmp_path / "seal")) == ([], 0, 0)


def test_a_location_column_is_not_an_unmigrated_coordinate(tmp_path):
    """`path:line` is what the round template prescribes for a Location cell.

    `old_format_rows` reads every table row for that shape and tells the
    author to run the migrator, which is right for a ledger and wrong for a
    record — so the records arm calls `check_text` and not `check_ledger`.
    """
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{
            "rounds__round-1.md": (
                "# r\n\n| # | Finding | Location |\n|---|---|---|\n"
                "| 1 | the guard | `hooks/review-history-guard.py:130` |\n"
            )
        },
    )
    assert module().check_records(str(tmp_path), str(tmp_path / "seal")) == ([], 0, 0)


def test_two_lines_stamping_one_unit_are_two_claims(tmp_path):
    """A record repeating a stale stamp is stale twice, and a reader who has
    to open one line has to open the other."""
    h = home(tmp_path)
    tree(tmp_path, **{"src__service.py": "def handler(x):\n    return x + 2\n"})
    work_item(
        h,
        "1780000000-live",
        **{
            "overview.md": (
                f"# o\n\n`src/service.py#handler@{GOOD}`\n\n"
                f"and again `src/service.py#handler@{GOOD}`\n"
            )
        },
    )
    findings, _names, stamps = module().check_records(
        str(tmp_path), str(tmp_path / "seal")
    )
    assert stamps == 2
    assert [f[1].rsplit(":", 1)[1] for f in findings] == ["3", "5"]


def test_a_records_drift_does_not_fail_the_run_and_a_broken_anchor_does(tmp_path):
    """A live work item's branch is editing the units its records stamp, so a
    run that failed on drift would be red by construction — the state the
    ledger CI job's own comment refuses. A name or an anchor that does not
    resolve has no mid-flight excuse."""
    h = home(tmp_path)
    (h / "ledger" / "1780000000-live.md").write_text("rows\n", encoding="utf-8")
    tree(tmp_path, **{"src__service.py": "def handler(x):\n    return x + 2\n"})
    d = work_item(
        h,
        "1780000000-live",
        **{"overview.md": f"# o\n\n`src/service.py#handler@{GOOD}`\n"},
    )
    drift = run(["."], tmp_path)
    assert drift.returncode == 1, drift.stdout + drift.stderr
    assert "0 refused · 1 drifted" in drift.stdout

    strict = run(["--strict", "."], tmp_path)
    assert strict.returncode == 2, strict.stdout + strict.stderr

    (d / "overview.md").write_text(
        "# o\n\n`src/gone.py#handler@deadbeef`\n", encoding="utf-8"
    )
    broken = run(["."], tmp_path)
    assert broken.returncode == 2, broken.stdout + broken.stderr
    assert "1 refused · 0 drifted" in broken.stdout


# --- a quotation is not a claim (round 1, 🟡 11) -----------------------------


def test_a_fenced_name_is_a_quotation_and_not_a_claim(tmp_path):
    """`## Paste-ready fixes` is fences of code the tree does not have yet —
    that is what a paste-ready fix IS. Refusing one asks the writer to mark
    up a block they copied verbatim, and a marker inside a fence changes the
    fix somebody pastes."""
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{
            "rounds__round-1.md": "# r\n\n## Paste-ready fixes\n\n"
            "```python\ndef gone_helper():\n    return `gone_helper`\n```\n"
        },
    )
    assert refusals(tmp_path) == ([], 0)


def test_a_name_after_the_fence_closes_is_a_claim_again(tmp_path):
    """The pair: a reader that switched the arm off at the first fence would
    pass the case above and read nothing after it."""
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{
            "rounds__round-1.md": "# r\n\n```python\n`inside_a_fence`\n```\n\n"
            "and then `gone_helper` in prose\n"
        },
    )
    found, read = refusals(tmp_path)
    assert read == 1
    assert [s for s, _, _ in found] == ["NOT-IN-TREE"], found
    assert "`gone_helper`" in found[0][2]


def test_an_html_comment_is_an_aside_and_not_a_claim(tmp_path):
    """A template's comments describe fields rather than assert units, and
    the records are bootstrapped from templates that carry them."""
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{"plan.md": "# p\n\n<!-- `gone_helper` — what this field holds -->\n"},
    )
    assert refusals(tmp_path) == ([], 0)


def test_a_fenced_stamp_is_a_quotation_too(tmp_path):
    """One reader for both arms: a stamp in a fence is a quoted anchor
    exactly as a name in one is a quoted name."""
    h = home(tmp_path)
    work_item(
        h,
        "1780000000-live",
        **{"plan.md": "# p\n\n```\nrow `mod.py#helper@deadbeef`\n```\n"},
    )
    assert refusals(tmp_path) == ([], 0)


# --- the boundary says what it did not read (round 1, 🟡 6) ------------------


def test_a_work_item_with_no_fragment_is_counted_as_unread(tmp_path):
    h = home(tmp_path)
    work_item(h, "1780000000-live", **{"spec.md": "# a\n"})
    work_item(h, "1770000000-shipped", fragment=False, **{"spec.md": "# b\n"})
    assert module().unread_items(str(h)) == ["1770000000-shipped"]


def test_the_run_says_how_many_work_items_it_did_not_read(tmp_path):
    """`0 names read` and exit 0 is the same output for *every record is
    clean* and *no record was opened*, and this arm's own work item sat in
    the second state through five of its six phases."""
    h = home(tmp_path)
    work_item(h, "1780000000-unwritten", fragment=False, **{"spec.md": "# a\n"})
    got = run(["."], tmp_path)
    assert got.returncode == 0, got.stdout + got.stderr
    assert "0 work items read · 1 unread · 0 names read" in got.stdout, got.stdout


def test_a_fragment_named_only_md_is_not_a_work_item(tmp_path):
    """`seal/ledger/.md` leaves the id empty, `os.path.join(specs, "")` is
    `specs/` itself and `isdir` says yes — so the whole records tree became
    one live work item and every shipped record in it was read."""
    h = home(tmp_path)
    work_item(
        h, "1770000000-shipped", fragment=False, **{"plan.md": "# `gone_helper`\n"}
    )
    (h / "ledger" / ".md").write_text("rows\n", encoding="utf-8")
    assert module().unshipped(str(h)) == {}
    assert refusals(tmp_path) == ([], 0)


# --- what `main` hands the arm ----------------------------------------------


def test_an_external_anchor_in_a_record_is_exit_0_as_it_is_in_a_ledger(tmp_path):
    """`EXTERNAL` is what a coordinate reads in a repository that has
    DECLARED cross-repo intent, and `SKILL.md` documents it at exit 0.
    Counting it as a refusal made a migration repository's records fail for
    the state its parity config exists to allow."""
    h = home(tmp_path)
    (h / "parity.md").write_text("| Original | somewhere |\n", encoding="utf-8")
    work_item(
        h,
        "1780000000-live",
        **{"overview.md": "# o\n\n`legacy/mod.py#handler@deadbeef`\n"},
    )
    findings, _names, stamps = module().check_records(str(tmp_path), str(h))
    assert stamps == 1
    assert [s for s, _, _ in findings] == ["EXTERNAL"], findings
    got = run(["."], tmp_path)
    assert got.returncode == 0, got.stdout + got.stderr
    assert "0 refused · 0 drifted · 1 external" in got.stdout, got.stdout


def test_two_stamps_of_one_unit_on_one_line_are_two_stamps(tmp_path):
    """`check_text` dedupes a repeated anchor, so counting what it RETURNS
    counted findings: one line stamping a unit twice read as one stamp, and
    the number beside a refusal was never the number of stamps."""
    h = home(tmp_path)
    tree(tmp_path, **{"src__service.py": SERVICE})
    work_item(
        h,
        "1780000000-live",
        **{
            "overview.md": f"# o\n\n`src/service.py#handler@{GOOD}` twice: "
            f"`src/service.py#handler@{GOOD}`\n"
        },
    )
    findings, _names, stamps = module().check_records(str(tmp_path), str(h))
    assert (findings, stamps) == ([], 2)


# --- the corpus guards, each with an observer (round 1, 🟡 7) ----------------


def test_a_deleted_name_surviving_in_the_git_directory_is_not_a_name(tmp_path):
    """`.git` is where every deleted version of every file lives, so a walk
    that read it would answer *the tree still has this* for a name the tree
    lost. Constructed without `git init`, so `SKIP_DIRS` is what refuses it
    rather than the index."""
    h = home(tmp_path)
    tree(tmp_path, **{".git__objects__pack__loose.txt": "gone_helper\n"})
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper`\n"})
    found, _read = refusals(tmp_path)
    assert [s for s, _, _ in found] == ["NOT-IN-TREE"], found


def test_a_broken_stamps_hint_does_not_point_into_a_vendored_package(tmp_path):
    """The scan looks for where a unit WENT, and a cache or a vendored
    package is the one place it cannot have gone. A hint reading `same name
    at .venv/lib/site-packages/pkg/a.py` sends the reader somewhere the
    repository does not own, and it is what made `SKIP_DIRS`' own comment —
    *directories no walk in this file descends* — false."""
    h = home(tmp_path)
    tree(tmp_path, **{".venv__lib__pkg__service.py": "def handler(x):\n    return x\n"})
    work_item(
        h,
        "1780000000-live",
        **{"overview.md": "# o\n\n`src/service.py#handler@deadbeef`\n"},
    )
    findings, _names, _stamps = module().check_records(str(tmp_path), str(h))
    assert [s for s, _, _ in findings] == ["BROKEN"], findings
    assert ".venv" not in findings[0][2], findings[0][2]


def test_a_file_over_the_size_cap_supplies_no_name(tmp_path):
    """A minified bundle or a lockfile is megabytes of tokens that name
    nothing anyone claims. Without the cap the run pays for reading them on
    every invocation, and the guard had no observer."""
    h = home(tmp_path)
    big = tmp_path / "bundle.min.js"
    big.write_text("x" * (module().NAME_FILE_CAP + 1) + "\ngone_helper\n")
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`gone_helper`\n"})
    found, _read = refusals(tmp_path)
    assert [s for s, _, _ in found] == ["NOT-IN-TREE"], found


def test_the_corpus_does_not_fold_case(tmp_path):
    """`Gone_Helper` and `gone_helper` are two identifiers in every language
    this reads, and a corpus that folded case would answer for one when the
    tree carries the other."""
    h = home(tmp_path)
    tree(tmp_path, **{"mod.py": "def gone_helper():\n    return 1\n"})
    work_item(h, "1780000000-live", **{"plan.md": "# p\n\n`Gone_Helper`\n"})
    found, _read = refusals(tmp_path)
    assert [s for s, _, _ in found] == ["NOT-IN-TREE"], found
    assert "`Gone_Helper`" in found[0][2]


def test_a_record_that_cannot_be_read_is_named(tmp_path, monkeypatch):
    """The status had no case at all. Constructed by refusing the read rather
    than by `chmod 000`, which is nothing to root and sets only a read-only
    flag on Windows — `test_gates_do_not_fail_open.py` makes the same choice
    for the same reason."""
    mod = module()
    h = home(tmp_path)
    work_item(h, "1780000000-live", **{"plan.md": "# p\n"})
    monkeypatch.setattr(mod, "read", lambda path: None)
    findings, names, stamps = mod.check_records(str(tmp_path), str(h))
    assert (names, stamps) == (0, 0)
    assert [s for s, _, _ in findings] == [mod.UNREADABLE_STATUS], findings
    assert findings[0][2] == "the record could not be read"


def test_the_same_anchor_answers_the_same_in_both_arms_under_default_repo(tmp_path):
    """`--default-repo` reaches the records arm, the way it reaches the ledger.

    Both arms resolve an anchor through `check_text`, so a coordinate that
    grades `OK` in `seal/ledger.md` has to grade `OK` in a record stating the
    same thing. `main` handed the records arm `maps` and not `default_repo`
    (round 1, 🔴 1), so the identical anchor read `1 ok` from the ledger and
    `BROKEN` from the record — exit 2, with the cross-repo look-alike scan
    switched back on, which is a migration repository's CI failing on every
    invocation.
    """
    root = tmp_path / "repo"
    root.mkdir()
    original = tmp_path / "original"
    (original / "src").mkdir(parents=True)
    (original / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    h = home(root)
    anchor = f"src/service.py#handler@{GOOD}"
    work_item(h, "1780000000-live", **{"overview.md": f"# o\n\n`{anchor}`\n"})
    (h / "ledger" / "1780000000-live.md").write_text(
        f"| S1 | `{anchor}` | read | 2026-09-07 |\n", encoding="utf-8"
    )
    got = run([".", "--default-repo", str(original)], root)
    assert got.returncode == 0, got.stdout + got.stderr
    assert "1 ok · 0 drifted · 0 broken" in got.stdout, got.stdout
    assert "1 stamp read · 0 refused" in got.stdout, got.stdout
    assert "BROKEN" not in got.stdout, got.stdout


# --- this repository's own records ------------------------------------------


def test_this_repositorys_own_records_state_nothing_the_tree_lacks():
    """The measurement #190 was opened for, run against the tree itself.

    Four occurrences of one name in work item `1788749195`'s round records —
    the instance that work item's own round 3 found by READING, three weeks of
    records later. This is what a check names at the commit that writes it.
    """
    findings, _names, _stamps = module().check_records(ROOT, os.path.join(ROOT, "seal"))
    assert findings == [], "\n".join(f"{c}  {d}" for _s, c, d in findings)
