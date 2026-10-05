"""A released ledger row is read again by a new row in a fragment (#715).

A released ledger file -- `seal/ledger.md` or a `seal/releases/<X.Y.Z>.md` --
never changes once its release is tagged. So a branch that re-reads a row
there, or finds its claim false, does not edit it. It writes a citing row
into its own fragment, `seal/ledger/<work-item-id>.md`:

    | Re-read · <the claim> | `<citation of R>`, `<code at its current hash>` | … | <date> | Re-read <date> … |
    | Corrected · <the new claim> | `<citation of R>`, `<new code>` | … | <date> | Corrected <date> … |

The citation names the row R by content: the release file, the
`### <work-item-id>` heading R sits under, and a literal from the start of
R's first cell. `evidence-check` then reads R together with every row that
re-reads it, as one family:

  S1  a coordinate is OK when one of its newest readings in R's family -- the
      members recording it with the newest `Checked` date, ties together --
      recorded what it holds
  S2  a re-read is per row: it vouches for the row it cites and no other
  S3  a `Corrected ·` row supersedes R; its own coordinates are what is checked
  S4  a citation that does not hold is named, never skipped

`seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-
never-changes/spec.md` D2 and D3 are the decisions these cases hold.
"""

import importlib.util
import itertools
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def load():
    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = load()

SERVICE = (
    "def handler(x):\n"
    "    y = x + 1\n"
    "    return y\n"
    "\n"
    "\n"
    "def other(x):\n"
    "    return x * 2\n"
)

SECTION = "### 1000000001-the-first-item"


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def unit_hash(repo, rel, locator):
    """What `rel#locator` holds now, as the checker hashes it."""
    text = (repo / rel).read_text(encoding="utf-8")
    places, _ = ec.resolve_unit(rel, locator, text)
    assert len(places) == 1, places
    a, b = places[0]
    return ec.content_hash(ec.gfm_lines(text)[a - 1 : b])


def line_hash(line):
    return ec.content_hash([line])


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    (d / "seal").mkdir()
    return d


def released(repo, rows, version="0.1.0", section=SECTION):
    """Write `seal/releases/<version>.md` holding ROWS under SECTION, and
    return the rows as written, one line each."""
    path = repo / "seal" / "releases" / f"{version}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    body = f"## {version} — 2026-01-01\n\n{section}\n\n" + "".join(
        row + "\n" for row in rows
    )
    path.write_text(body, encoding="utf-8")
    return rows


def fragment(repo, rows, name="2000000001-a-later-item"):
    path = repo / "seal" / "ledger" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(row + "\n" for row in rows), encoding="utf-8")
    return path


def citation(row, literal, version="0.1.0", section=SECTION):
    return f'seal/releases/{version}.md#"{section}">"{literal}"@{line_hash(row)}'


def edit_handler(repo):
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("y = x + 1", "y = x + 2"), encoding="utf-8"
    )


def findings(out):
    """`[(status, coordinate)]` for every finding line the run printed."""
    found = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] in (
            "DRIFTED",
            "BROKEN",
            "MALFORMED",
            "EXTERNAL",
        ):
            found.append((parts[0], parts[1]))
    return found


def ledger_section(out, name):
    """The lines the run printed under the ledger NAME, up to its counts.

    The checker prints a ledger's path with the platform's separator, so the
    heading is compared in POSIX form, as the rest of this suite compares
    paths (`.replace(os.sep, "/")`)."""
    lines = out.splitlines()
    start = next(
        i for i, line in enumerate(lines) if line.strip().replace(os.sep, "/") == name
    )
    block = []
    for line in lines[start + 1 :]:
        block.append(line)
        if " ok · " in line:
            break
    return "\n".join(block)


# --- S1 ----------------------------------------------------------------------


def test_a_re_read_clears_a_drifted_released_row(repo):
    """S1. R records `handler` as it was; the code moved; a fragment's
    `Re-read ·` row cites R and records `handler` as it is now."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    new = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{new}` | read: it adds two now, and the claim "
            "is about the addition | 2026-02-01 | Re-read 2026-02-01 by work item 2000000001 |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert not findings(out.stdout), out.stdout


def test_without_the_re_read_the_same_row_is_drifted(repo):
    """The control for S1: the drift is real, and the re-read is what clears
    it."""
    old = unit_hash(repo, "src/service.py", "handler")
    released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    assert ("DRIFTED", "src/service.py#handler") in findings(out.stdout)


def test_a_re_read_of_a_re_read_belongs_to_the_same_family(repo):
    """A re-read folded into a release is itself a released row, and a later
    re-read cites it: the family is R, every re-read citing R, and every
    re-read citing one of those."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    other = unit_hash(repo, "src/service.py", "other")
    (rr,) = released(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#other@{other}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        version="0.2.0",
        section="### 2000000001-a-later-item",
    )
    edit_handler(repo)
    new = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            "| Re-read · Re-read · R1 · handler adds one | "
            f"`{citation(rr, 'Re-read · R1 · handler', '0.2.0', '### 2000000001-a-later-item')}`, "
            f"`src/service.py#handler@{new}` | read | 2026-03-01 | Re-read 2026-03-01 |"
        ],
        name="3000000001-a-third-item",
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr


# --- S2 ----------------------------------------------------------------------


def test_a_re_read_vouches_for_the_row_it_cites_and_no_other(repo):
    """S2. R1 and R2 both cite `handler`, both drifted. The fragment re-reads
    R1 alone, so R1 is clear and R2 is still DRIFTED: a reading is of a row,
    and nobody opened R2."""
    old = unit_hash(repo, "src/service.py", "handler")
    r1, _ = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |",
            f"| R2 · handler returns its sum | `src/service.py#handler@{old}` | read | 2026-01-01 | |",
        ],
    )
    edit_handler(repo)
    new = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r1, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{new}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    release = ledger_section(out.stdout, "seal/releases/0.1.0.md")
    assert "1 drifted" in release, release
    assert ("DRIFTED", "src/service.py#handler") in findings(release)
    assert out.returncode == 2, out.stdout


# --- S3 ----------------------------------------------------------------------


def test_a_correction_supersedes_the_row_it_cites(repo):
    """S3. R's coordinate drifted, and the correction says what is true now
    and cites different code. R is no longer checked; the correction is."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    other = unit_hash(repo, "src/service.py", "other")
    fragment(
        repo,
        [
            f"| Corrected · the doubling lives in other | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#other@{other}` | read | 2026-02-01 | "
            "Corrected 2026-02-01 by work item 2000000001: handler adds two |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert not findings(out.stdout), out.stdout


def test_a_stale_coordinate_in_the_correction_is_drifted(repo):
    """S3's other half: the correcting row starts a family of its own, and
    its coordinates are checked like any row's."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    fragment(
        repo,
        [
            f"| Corrected · the doubling lives in other | `{citation(r, 'R1 · handler adds one')}`, "
            "`src/service.py#other@00000000` | read | 2026-02-01 | Corrected 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert ("DRIFTED", "src/service.py#other") in findings(out.stdout), out.stdout
    assert ("DRIFTED", "src/service.py#handler") not in findings(out.stdout)
    assert out.returncode == 2


def test_removal_is_a_correction_whose_grounds_hold_the_citation_alone(repo):
    """The claim went with the code: the unit R cites is gone, and a
    `Corrected ·` row with the citation alone says so. R is not BROKEN."""
    old = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · other doubles | `src/service.py#other@{old}` | read | 2026-01-01 | |"
        ],
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.split("\n\n\ndef other")[0] + "\n", encoding="utf-8"
    )
    fragment(
        repo,
        [
            f"| Corrected · nothing doubles any more | `{citation(r, 'R1 · other doubles')}` "
            "| read: `other` was removed | 2026-02-01 | Corrected 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr


# --- S4 ----------------------------------------------------------------------


def test_a_citation_into_a_fragment_is_refused_and_names_the_repair(repo):
    """S4. A fragment is not released and moves at the fold, so a citation
    into one would break at the next release. The repair is to re-stamp that
    fragment's row in place."""
    old = unit_hash(repo, "src/service.py", "handler")
    row = f"| F1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
    fragment(repo, [row], name="1500000001-an-unreleased-item")
    cite = f'seal/ledger/1500000001-an-unreleased-item.md#"F1 · handler adds one"@{line_hash(row)}'
    fragment(
        repo,
        [
            f"| Re-read · F1 · handler adds one | `{cite}`, `src/service.py#handler@{old}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    named = [
        line
        for line in out.stdout.splitlines()
        if line.strip().startswith("MALFORMED") and "seal/ledger/1500000001" in line
    ]
    assert named, out.stdout
    assert "fragment" in named[0] and "in place" in named[0], named[0]


def test_a_citing_row_without_its_marker_is_named(repo):
    """S4. A citing row carries `Re-read <date>` or `Corrected <date>` in its
    Notes, the vocabulary `correction-check` reads; one without is named."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{old}` | read | 2026-02-01 | read by somebody |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    named = [
        line
        for line in out.stdout.splitlines()
        if line.strip().startswith("MALFORMED") and "Re-read <date>" in line
    ]
    assert named, out.stdout


def test_a_citation_whose_row_is_gone_is_broken(repo):
    """S4. The literal names no row in the section: the cited row is gone,
    and that is BROKEN rather than the DRIFTED an ordinary minor anchor
    degrades to, because the family it names no longer exists."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    fragment(
        repo,
        [
            f"| Re-read · R9 · a row nobody wrote | `{citation(r, 'R9 · a row nobody wrote')}`, "
            f"`src/service.py#handler@{old}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    broken = [c for s, c in findings(out.stdout) if s == "BROKEN"]
    assert broken and broken[0].startswith("seal/releases/0.1.0.md#"), out.stdout


def test_a_released_file_changed_under_a_citation_drifts_it(repo):
    """The citation's hash is the hash of R's own line. A released file that
    changed under it -- a re-stamp in place by a branch cut before the rule --
    drifts the citation, loudly."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{old}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    path = repo / "seal" / "releases" / "0.1.0.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| read |", "| read again |"),
        encoding="utf-8",
    )
    out = run(["--strict", "."], repo)
    drifted = [c for s, c in findings(out.stdout) if s == "DRIFTED"]
    assert any(c.startswith("seal/releases/0.1.0.md#") for c in drifted), out.stdout


def test_the_help_says_what_a_citing_row_is():
    """The docstring and `--help` carry the shape, so a reader of the command
    meets it without opening the spec."""
    out = subprocess.run(
        [sys.executable, SCRIPT, "--help"], capture_output=True, encoding="utf-8"
    )
    assert "Re-read ·" in out.stdout and "Corrected ·" in out.stdout, out.stdout
    assert "Re-read ·" in ec.__doc__ and "Corrected ·" in ec.__doc__


# --- the citation a tool writes (W1) -----------------------------------------


def test_the_citation_written_for_a_row_names_that_row_alone(repo):
    """`citation_for` builds what `--reverify --into` writes, and the two
    shapes that defeated a plain prefix are here: a first cell opening with
    a code span, and a heading holding a backtick, which would close the
    code span the citation sits in. Each citation resolves to its own row."""
    old = unit_hash(repo, "src/service.py", "handler")
    rows = [
        f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |",
        f"| R1 · handler adds one, again | `src/service.py#handler@{old}` | read | 2026-01-01 | |",
        f"| `handler` is the only adder | `src/service.py#handler@{old}` | read | 2026-01-01 | |",
    ]
    path = repo / "seal" / "releases" / "0.1.0.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        f"## 0.1.0 — 2026-01-01\n\n{SECTION}\n\n#### `handler`, and what it adds\n\n"
        + "".join(r + "\n" for r in rows),
        encoding="utf-8",
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    files = {}

    def load(p):
        ident = ec.file_identity(p)
        body = ec.read(p)
        files[ident] = (
            p,
            body,
            ec.gfm_lines(ec.unquoted(body)),
            {n: (h, c) for n, h, c in ec.ledger_table_rows(body)},
        )
        return ident, files[ident]

    for row in rows:
        number = lines.index(row) + 1
        cite = ec.citation_for(str(repo), str(path), number)
        assert cite is not None, row
        assert "`" not in cite and SECTION in cite, cite
        m = ec.ANCHOR_RE.fullmatch(cite)
        assert m is not None, cite
        status, detail, target = ec.cited_row(m, "Re-read", str(repo), {}, None, load)
        assert (status, target[1]) == ("OK", number), (cite, detail)


# --- where the family is read from -------------------------------------------


def drifted_and_re_read(repo):
    """S1's tree: a drifted released row and the fragment row re-reading it."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    new = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{new}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )


def test_a_narrowed_run_still_reads_the_re_reads_it_does_not_report(repo):
    """`--ledger` chooses what is reported. A released row reported DRIFTED
    because its re-read sat in a file the narrowing left out would be a
    false finding."""
    drifted_and_re_read(repo)
    out = run(["--strict", "--ledger", "seal/releases/*.md", "."], repo)
    assert ("DRIFTED", "src/service.py#handler") not in findings(out.stdout), out.stdout
    assert out.returncode == 0, out.stdout


def test_the_commit_advisor_reads_one_view_of_every_ledger(repo):
    """The post-commit advisor names BROKEN rows. A released row whose unit
    is gone and which a fragment's `Corrected ·` row supersedes is not one,
    and only a reader holding both files can tell."""
    old = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · other doubles | `src/service.py#other@{old}` | read | 2026-01-01 | |"
        ],
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.split("\n\n\ndef other")[0] + "\n", encoding="utf-8"
    )
    fragment(
        repo,
        [
            f"| Corrected · nothing doubles any more | `{citation(r, 'R1 · other doubles')}` "
            "| read | 2026-02-01 | Corrected 2026-02-01 |"
        ],
    )
    spec = importlib.util.spec_from_file_location(
        "specseal_evidence_advisor", os.path.join(ROOT, "hooks", "evidence-advisor.py")
    )
    advisor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(advisor)
    assert advisor.failing_rows(str(repo), str(repo / "seal")) == []


def test_a_citation_into_the_gathered_ledger_names_its_row(repo):
    """`seal/ledger.md` is released too: the rows from before the fragments
    existed, under its `##` area headings and their tables' headers."""
    old = unit_hash(repo, "src/service.py", "handler")
    row = f"| G1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
    (repo / "seal" / "ledger.md").write_text(
        "# map\n\n## Coordinates\n\n| Clause | Code grounds | Verified behavior "
        "| Checked | Notes |\n|---|---|---|---|---|\n" + row + "\n",
        encoding="utf-8",
    )
    edit_handler(repo)
    new = unit_hash(repo, "src/service.py", "handler")
    cite = f'seal/ledger.md#"## Coordinates">"G1 · handler adds one"@{line_hash(row)}'
    fragment(
        repo,
        [
            f"| Re-read · G1 · handler adds one | `{cite}`, `src/service.py#handler@{new}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr


def test_in_local_mode_the_seal_prefix_is_read_under_the_git_directory(repo):
    """A citation spells the root `seal/…`. In local mode the root sits under
    the common git directory, and the citation still resolves there."""
    drifted_and_re_read(repo)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "seal").rename(repo / ".git" / "seal")
    out = run(["--strict", "."], repo)
    assert ("DRIFTED", "src/service.py#handler") not in findings(out.stdout), out.stdout
    assert out.returncode == 0, out.stdout + out.stderr


@pytest.mark.parametrize(
    "grounds, said",
    [
        ("`src/service.py#handler@{old}`", "names neither"),
        ('`seal/releases/0.1.0.md#"{section}"@{row}`', "names a section, not a row"),
        ("read by eye", "names none"),
    ],
)
def test_a_citing_row_that_names_no_released_row_is_named(repo, grounds, said):
    """Beside S4's three: a first coordinate that is code rather than a
    ledger row, a citation naming a whole section, and no coordinate at all.
    None of them is read as a citation, and each says why."""
    old = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |"
        ],
    )
    text = grounds.format(old=old, section=SECTION, row=line_hash(r))
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | {text} | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    named = [
        line
        for line in out.stdout.splitlines()
        if line.strip().startswith("MALFORMED") and said in line
    ]
    assert named, out.stdout
    assert out.returncode == 2


def test_a_citation_whose_literal_lands_on_prose_names_no_row(repo):
    """The literal is unique in the section and on a line that is not a
    ledger row -- the section's own prose. That line has no family, so the
    citation is BROKEN rather than read as a row."""
    old = unit_hash(repo, "src/service.py", "handler")
    _, _, r = released(
        repo,
        [
            "<!-- a note about handler and why it adds -->",
            "",
            f"| R1 · handler adds one | `src/service.py#handler@{old}` | read | 2026-01-01 | |",
        ],
    )
    cite = (
        citation(r, "a note about handler").rsplit("@", 1)[0]
        + "@"
        + line_hash("<!-- a note about handler and why it adds -->")
    )
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `src/service.py#handler@{old}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    named = [line for line in out.stdout.splitlines() if "not a ledger row" in line]
    assert named and named[0].strip().startswith("BROKEN"), out.stdout


# --- S5: `--reverify --into` writes the citing rows ---------------------------

INTO = "seal/ledger/2000000001-a-later-item.md"


def frozen(repo, value="1"):
    (repo / "seal" / "config.md").write_text(
        "# Repository config\n\n| Item | Value |\n|---|---|\n"
        f"| Ledger frozen from | {value} |\n",
        encoding="utf-8",
    )


def digests(repo):
    """sha256 of every released ledger file, by path."""
    import hashlib

    found = {}
    for path in sorted((repo / "seal").rglob("*.md")):
        rel = path.relative_to(repo).as_posix()
        if rel == "seal/ledger.md" or rel.startswith("seal/releases/"):
            found[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return found


def two_drifted_rows(repo):
    """R1 cites `handler` and `other`, R2 cites `handler`; then both units
    change, so R1 drifts on two coordinates and R2 on one."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    rows = released(
        repo,
        [
            f"| R1 · handler adds one and other doubles | `src/service.py#handler@{h}`, "
            f"`src/service.py#other@{o}` | read | 2026-01-01 | |",
            f"| R2 · handler returns its sum | `src/service.py#handler@{h}` | read | 2026-01-01 | |",
        ],
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("y = x + 1", "y = x + 2").replace("x * 2", "x * 3"),
        encoding="utf-8",
    )
    return rows


def test_into_writes_one_citing_row_per_drifted_row_and_no_released_byte(repo):
    """S5. Two drifted rows, three drifted coordinates: two rows are written,
    one per row and never one per coordinate, each carrying every drifted
    coordinate at its current hash. Every released file is byte-identical,
    and the tree then checks clean."""
    frozen(repo)
    two_drifted_rows(repo)
    before = digests(repo)
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert digests(repo) == before
    written = (repo / INTO).read_text(encoding="utf-8").splitlines()
    assert len(written) == 2, written
    assert written[0].startswith("| Re-read · R1 · handler adds one"), written[0]
    assert written[0].count("src/service.py#") == 2, written[0]
    assert "Re-read 2026-02-01" in written[0] and "| 2026-02-01 |" in written[0]
    assert "by work item 2000000001-a-later-item" in written[0], written[0]
    assert written[1].startswith("| Re-read · R2 · handler returns its sum"), written[1]
    assert (
        "seal/releases/0.1.0.md:5" in out.stdout
        and "seal/releases/0.1.0.md:6" in out.stdout
    )
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


def test_into_writes_nothing_for_a_row_its_family_already_re_read(repo):
    """A row whose family already holds the current hash is not drifted, so
    a second run writes no second row."""
    frozen(repo)
    two_drifted_rows(repo)
    run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    first = (repo / INTO).read_text(encoding="utf-8")
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 0, out.stdout
    assert (repo / INTO).read_text(encoding="utf-8") == first


def test_a_frozen_reverify_without_into_writes_no_released_file(repo):
    """S5. Under `Ledger frozen from` a plain `--reverify` still re-stamps the
    fragments in place, leaves every released file byte-identical, and exits
    non-zero naming each released row it left and the `--into` form."""
    frozen(repo)
    two_drifted_rows(repo)
    h = unit_hash(repo, "src/service.py", "handler")
    own = f"| F1 · handler adds two | `src/service.py#handler@{h[:-1]}0` | read | 2026-02-01 | |"
    fragment(repo, [own])
    before = digests(repo)
    out = run(["--reverify", "."], repo)
    assert out.returncode == 1, out.stdout
    assert digests(repo) == before
    assert f"src/service.py#handler@{h}" in (repo / INTO).read_text(encoding="utf-8")
    assert "--into" in out.stdout
    assert (
        "seal/releases/0.1.0.md:5" in out.stdout
        and "seal/releases/0.1.0.md:6" in out.stdout
    )


def test_into_without_checked_is_refused_and_writes_nothing(repo):
    """S5. A citing row with no date is a stamp nobody read."""
    frozen(repo)
    two_drifted_rows(repo)
    out = run(["--reverify", "--into", INTO, "."], repo)
    assert out.returncode == 2, out.stdout
    assert "--checked" in out.stderr
    assert not (repo / INTO).exists()


def test_into_names_a_fragment_or_is_refused(repo):
    """`--into` is where the branch's own rows go: a fragment, never a
    released file."""
    frozen(repo)
    two_drifted_rows(repo)
    before = digests(repo)
    out = run(
        [
            "--reverify",
            "--into",
            "seal/releases/0.1.0.md",
            "--checked",
            "2026-02-01",
            ".",
        ],
        repo,
    )
    assert out.returncode == 2, out.stdout
    assert "fragment" in out.stderr
    assert digests(repo) == before


def test_without_the_row_reverify_re_stamps_in_place_as_before(repo):
    """S5. A repository that does not declare the freeze keeps the behaviour
    every installed copy had."""
    two_drifted_rows(repo)
    before = digests(repo)
    out = run(["--reverify", "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 0, out.stdout
    assert digests(repo) != before
    assert not (repo / "seal" / "ledger").exists()


def test_a_freeze_row_that_is_not_an_id_is_refused(repo):
    """A cutoff that will not parse is refused with the row named, the way
    `fold-check` refuses `Fold shape from`."""
    frozen(repo, "soon")
    two_drifted_rows(repo)
    out = run(["--reverify", "."], repo)
    assert out.returncode == 2, out.stdout
    assert "Ledger frozen from" in out.stderr


def test_the_commit_advisor_names_into_where_the_ledger_is_frozen(repo):
    """D4: the post-commit advisor prints the same repair. Under the freeze a
    released row is not re-anchored in place, so the line names `--into`."""
    frozen(repo)
    released(
        repo,
        ["| R1 · gone | `src/service.py#gone@abcdef12` | read | 2026-01-01 | |"],
    )
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": "git commit -m x"},
        "cwd": str(repo),
    }
    import json

    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    out = subprocess.run(
        [sys.executable, os.path.join(ROOT, "hooks", "evidence-advisor.py")],
        input=json.dumps(payload),
        capture_output=True,
        encoding="utf-8",
    )
    assert "BROKEN" in out.stdout, out.stdout + out.stderr
    assert "--into" in out.stdout, out.stdout


# --- S15: the freeze is a documented row --------------------------------------


def test_every_row_this_repository_declares_is_documented_in_the_template():
    """S15. `templates/config.md` documents every row; this repository's own
    `seal/config.md` declares six. A row the template does not name is a row
    another repository cannot learn to read."""
    spec = importlib.util.spec_from_file_location(
        "specseal_config", os.path.join(ROOT, "hooks", "config.py")
    )
    config = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.join(ROOT, "hooks"))
    try:
        spec.loader.exec_module(config)
    finally:
        sys.path.pop(0)
    with open(os.path.join(ROOT, "seal", "config.md"), encoding="utf-8") as fh:
        rows = config.config_rows(fh.read())
    with open(os.path.join(ROOT, "templates", "config.md"), encoding="utf-8") as fh:
        template = fh.read()
    items = [item for item, _ in rows]
    assert "Ledger frozen from" in items, items
    missing = [
        item
        for item in items
        if f"`{item}`" not in template and f"## {item}" not in template
    ]
    assert not missing, missing
    assert (
        "| Ledger frozen from | 1790993141 |"
        in open(os.path.join(ROOT, "seal", "config.md"), encoding="utf-8").read()
    )


def test_a_vendored_copy_reads_the_freeze_without_the_plugin_beside_it(repo):
    """`evidence-ci` puts the checker alone in a repository's `tools/`, where
    `hooks/config.py` is not beside it. The copy still reads the row and
    still writes no released file."""
    import shutil

    tools = repo / "tools"
    tools.mkdir()
    shutil.copy(SCRIPT, tools / "evidence_check.py")
    frozen(repo)
    two_drifted_rows(repo)
    before = digests(repo)
    out = subprocess.run(
        [sys.executable, str(tools / "evidence_check.py"), "--reverify", "."],
        cwd=str(repo),
        capture_output=True,
        encoding="utf-8",
    )
    assert out.returncode == 1, out.stdout + out.stderr
    assert digests(repo) == before
    assert "--into" in out.stdout


def test_into_re_reads_a_claimed_coordinate_at_its_minor_region(repo):
    """A coordinate narrowed by a claim records the hash of the statement
    it names, and the citing row carries that hash, not the unit's."""
    text = (repo / "src" / "service.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/service.py", "handler", text)
    (inside,) = ec.minor_region("src/service.py", text, places[0], '"return y"')
    lines = ec.gfm_lines(text)
    old = ec.content_hash(lines[inside[0] - 1 : inside[1]])
    released(
        repo,
        [
            f'| R1 · handler returns y | `src/service.py#handler>"return y"@{old}` '
            "| read | 2026-01-01 | |"
        ],
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("    return y\n", "    return y  # the sum\n"), encoding="utf-8"
    )
    frozen(repo)
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert '#handler>"return y"@' in (repo / INTO).read_text(encoding="utf-8")
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


def test_into_without_reverify_says_which_command_it_belongs_to(repo):
    """`--into` alone is refused for the command it lacks, not for the date."""
    frozen(repo)
    two_drifted_rows(repo)
    out = run(["--into", INTO, "."], repo)
    assert out.returncode == 2, out.stdout
    assert "no `--reverify`" in out.stderr, out.stderr


def test_into_re_reads_a_coordinate_a_folded_re_read_carries(repo):
    """The drifted coordinate sits on a folded `Re-read ·` row, not on the
    family's root: the row `--into` writes names it whole. It wrote a bare
    hash and exited 0 before, because the match was sliced against the
    root's line (warden round 1, 🔴 1)."""
    handler = unit_hash(repo, "src/service.py", "handler")
    other = unit_hash(repo, "src/service.py", "other")
    (row,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{handler}` | read | 2026-01-01 | |"
        ],
    )
    folded = (
        f"| Re-read · R1 · handler adds one | `{citation(row, 'R1 · handler adds one')}`, "
        f"`src/service.py#other@{other}` | read | 2026-02-01 | Re-read 2026-02-01 by work item 2 |"
    )
    released(repo, [folded], version="0.2.0", section="### 2000000001-a-later-item")
    frozen(repo, "0")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 7"), encoding="utf-8"
    )
    r = run(
        [
            "--reverify",
            "--into",
            "seal/ledger/3000000001-y.md",
            "--checked",
            "2026-03-01",
            ".",
        ],
        repo,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    written = (repo / "seal" / "ledger" / "3000000001-y.md").read_text(encoding="utf-8")
    now = unit_hash(repo, "src/service.py", "other")
    assert f"`src/service.py#other@{now}`" in written, written
    assert run(["--strict", "."], repo).returncode == 0


# --- the newest reading of each coordinate decides (round 1, 🟡 2) -----------


def test_a_partial_revert_to_an_older_reading_is_drifted(repo):
    """P1. R reads (h1, o1); both units change and a re-read records
    (h2, o2); then `handler` alone goes back to h1. The pair (h1, o2) was
    never read together, and the claim about how the two fit can be false
    there. Only the newest reading of each coordinate counts, so `handler`
    at h1 matches R's older reading alone and is DRIFTED."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    o1 = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler and other agree | `src/service.py#handler@{h1}`, "
            f"`src/service.py#other@{o1}` | read | 2026-01-01 | |"
        ],
    )
    both = SERVICE.replace("y = x + 1", "y = x + 2").replace("x * 2", "x * 3")
    (repo / "src" / "service.py").write_text(both, encoding="utf-8")
    h2 = unit_hash(repo, "src/service.py", "handler")
    o2 = unit_hash(repo, "src/service.py", "other")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler and other agree | `{citation(r, 'R1 · handler and other')}`, "
            f"`src/service.py#handler@{h2}`, `src/service.py#other@{o2}` | read "
            "| 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    assert run(["--strict", "."], repo).returncode == 0
    (repo / "src" / "service.py").write_text(
        both.replace("y = x + 2", "y = x + 1"), encoding="utf-8"
    )
    assert unit_hash(repo, "src/service.py", "handler") == h1
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    assert ("DRIFTED", "src/service.py#handler") in findings(out.stdout), out.stdout
    assert "2026-02-01" in out.stdout, out.stdout


def test_two_readings_of_one_coordinate_on_the_same_day_are_a_union(repo):
    """Two parallel branches re-read one row on the same day and record two
    hashes for one unit: neither is newer, so both count, and the content
    either one recorded reads OK."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("y = x + 1", "y = x + 3"), encoding="utf-8"
    )
    h3 = unit_hash(repo, "src/service.py", "handler")
    cite = citation(r, "R1 · handler adds one")
    for name, h in (("2000000001-a", h2), ("2000000002-b", h3)):
        fragment(
            repo,
            [
                f"| Re-read · R1 · handler adds one | `{cite}`, `src/service.py#handler@{h}` "
                "| read | 2026-02-01 | Re-read 2026-02-01 |"
            ],
            name=name,
        )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    assert run(["--strict", "."], repo).returncode == 0


def test_into_re_reads_a_revert_a_folded_newer_reading_outranks(repo):
    """R reads h1, a folded re-read reads h2 a month later, and the code goes
    back to h1. R's reading matches and is older, so the family is drifted,
    and `--into` writes a re-read at h1 that clears it."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    released(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h2}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        version="0.2.0",
        section="### 2000000001-a-later-item",
    )
    frozen(repo, "0")
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    assert run(["--strict", "."], repo).returncode == 2
    out = run(["--reverify", "--into", INTO, "--checked", "2026-03-01", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert f"`src/service.py#handler@{h1}`" in (repo / INTO).read_text(encoding="utf-8")
    assert run(["--strict", "."], repo).returncode == 0


def test_a_moved_released_row_is_told_its_correction_carries_every_coordinate(
    repo,
):
    """A `Corrected ·` row supersedes the whole released row, so one that
    re-points only the moved coordinate stops the rest being checked. The
    repair `--into` prints, and the commit advisor's, say the correction
    carries every coordinate the claim still rests on (round 1, 🟡 3)."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    released(
        repo,
        [
            f"| R1 · handler and other agree | `src/service.py#handler@{h}`, "
            f"`src/service.py#other@{o}` | read | 2026-01-01 | |"
        ],
    )
    frozen(repo)
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("def handler", "def handle2"), encoding="utf-8"
    )
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 1, out.stdout
    assert "carries every other coordinate the claim still rests on" in out.stdout, (
        out.stdout
    )
    spec = importlib.util.spec_from_file_location(
        "specseal_evidence_advisor_repair",
        os.path.join(ROOT, "hooks", "evidence-advisor.py"),
    )
    advisor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(advisor)
    assert "every coordinate the claim still rests on" in advisor.FROZEN_REPAIR


def test_a_released_row_corrected_by_two_rows_names_both(repo):
    """Two branches each find one released row false and each write a
    `Corrected ·` row: two claims, both OK, and nothing reconciled them. The
    conflict two in-place corrections used to meet on is gone, so both rows
    are named DRIFTED, each listing the other (round 1, 🟡 4)."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    for name, claim in (("2000000001-a", "two"), ("2000000002-b", "three")):
        fragment(
            repo,
            [
                f"| Corrected · handler adds {claim} | `{cite}`, `src/service.py#handler@{h}` "
                "| read | 2026-02-01 | Corrected 2026-02-01 |"
            ],
            name=name,
        )
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    named = [
        line
        for line in out.stdout.splitlines()
        if line.strip().startswith("DRIFTED") and "corrected by 2 rows" in line
    ]
    assert len(named) == 2, out.stdout
    for line in named:
        assert "2000000001-a.md:1" in line and "2000000002-b.md:1" in line, line


def test_a_released_row_corrected_once_is_not_named(repo):
    """The control: one correction is the ordinary case and reads clean."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    fragment(
        repo,
        [
            f"| Corrected · handler adds two | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Corrected 2026-02-01 |"
        ],
    )
    assert run(["--strict", "."], repo).returncode == 0


def test_a_first_cell_that_also_ends_another_cell_still_gets_a_citation(repo):
    """R2's last cell is `see R1 · handler adds one`, so every prefix of R1's
    first cell and its closing-pipe tail stand on R2's line too. The cell
    whole, after the row's leading pipe, begins no other line, and names R1
    alone (round 1, ⬜ 9)."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    r1, _ = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |",
            f"| R2 · other doubles | `src/service.py#other@{o}` | read | 2026-01-01 | see R1 · handler adds one |",
        ],
    )
    path = repo / "seal" / "releases" / "0.1.0.md"
    number = path.read_text(encoding="utf-8").splitlines().index(r1) + 1
    cite = ec.citation_for(str(repo), str(path), number)
    assert cite is not None
    m = ec.ANCHOR_RE.fullmatch(cite)
    assert m is not None, cite
    files = {}

    def load(p):
        ident = ec.file_identity(p)
        body = ec.read(p)
        files[ident] = (
            p,
            body,
            ec.gfm_lines(ec.unquoted(body)),
            {n: (hd, c) for n, hd, c in ec.ledger_table_rows(body)},
        )
        return ident, files[ident]

    status, _, target = ec.cited_row(m, "Re-read", str(repo), {}, None, load)
    assert (status, target[1]) == ("OK", number), cite


def test_a_folded_double_correction_is_cleared_by_retiring_one(repo):
    """Both corrections folded, so neither can be edited: a third
    `Corrected ·` row citing one of them retires it, and the notice goes
    (round 2, 🟡 11)."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    sec = "### 2000000001-a-later-item"
    c1, c2 = (
        f"| Corrected · handler adds {n} | `{cite}`, `src/service.py#handler@{h}` "
        "| read | 2026-02-01 | Corrected 2026-02-01 |"
        for n in ("two", "three")
    )
    released(repo, [c1, c2], version="0.2.0", section=sec)
    frozen(repo, "0")
    assert run(["--strict", "."], repo).returncode == 2
    retire = citation(
        c2, "Corrected · handler adds three", version="0.2.0", section=sec
    )
    fragment(
        repo,
        [
            f"| Corrected · handler adds two, as the other row says | `{retire}`, "
            f"`src/service.py#handler@{h}` | read | 2026-03-01 | Corrected 2026-03-01 |"
        ],
        name="3000000001-y",
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout


def test_a_narrowed_into_re_reads_a_family_a_fragment_outranks(repo):
    """The newest reading sits in a fragment `--ledger` leaves out, so no
    in-place re-stamp reaches it: `--into` still owes the released row a
    re-read (round 2, 🟡 12)."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h2}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name="2000000009-z",
    )
    frozen(repo, "0")
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    assert run(["--strict", "."], repo).returncode == 2
    out = run(
        [
            "--reverify",
            "--into",
            INTO,
            "--checked",
            "2026-03-01",
            "--ledger",
            "seal/releases/0.1.0.md",
            ".",
        ],
        repo,
    )
    assert "1 citing row written" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 0


def test_an_unfrozen_narrowed_reverify_names_a_family_it_could_not_clear(repo):
    """Without the freeze `--reverify` re-stamps in place, but narrowed to the
    release file it cannot reach the newer reading in a fragment the
    narrowing left out. It exits 1 naming the row rather than 0 while the
    family reads DRIFTED (round 2, 🟡 12's sibling)."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h2}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name="2000000009-z",
    )
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    out = run(["--reverify", "--ledger", "seal/releases/0.1.0.md", "."], repo)
    assert run(["--strict", "."], repo).returncode == 2
    assert out.returncode == 1, out.stdout
    left = [line for line in out.stdout.splitlines() if "LEFT" in line]
    assert left and "seal/releases/0.1.0.md:5" in left[0], out.stdout
    # The newest reading sits in the fragment the narrowing left out, so the
    # `--ledger` remedy is the true one, and the run left nothing itself
    # (#792, S11).
    assert "newest reading" in left[0], left[0]
    assert left[0].endswith("run it without `--ledger`"), left[0]
    assert "this run left" not in left[0], left[0]


def test_a_checked_cell_the_calendar_does_not_have_does_not_outrank_a_re_read(repo):
    """A `Checked` date now orders readings, so `2026-13-45`, compared as a
    string, outranked every reading after it: `--into` reported a row written
    and the family still read DRIFTED. A date the calendar does not have
    orders nothing (round 2, ⬜ 13)."""
    h = unit_hash(repo, "src/service.py", "handler")
    released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-13-45 | |"
        ],
    )
    frozen(repo, "0")
    edit_handler(repo)
    out = run(["--reverify", "--into", INTO, "--checked", "2026-03-01", "."], repo)
    assert "1 citing row written" in out.stdout, out.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


def test_a_first_cell_equal_to_another_rows_cell_still_gets_a_citation(repo):
    """R2's Notes cell is exactly R1's first cell, pipes and all, so even
    `| R1 · handler adds one |` stands on R2's line. A literal that opens
    with a row's leading pipe is matched where a line begins with it, and
    only one line does (round 2, ⬜ 14)."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    r1, _ = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |",
            f"| R2 · other doubles | `src/service.py#other@{o}` | read | 2026-01-01 | R1 · handler adds one |",
        ],
    )
    path = repo / "seal" / "releases" / "0.1.0.md"
    number = path.read_text(encoding="utf-8").splitlines().index(r1) + 1
    cite = ec.citation_for(str(repo), str(path), number)
    assert cite is not None
    edit_handler(repo)
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, "
            f"`src/service.py#handler@{unit_hash(repo, 'src/service.py', 'handler')}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout


# --- a narrowed `--reverify` answers for every family a file it read holds a
# member of (#740, round 3's 🟡 16) -------------------------------------------

R_FILE = "seal/releases/0.1.0.md"
UNRELATED = "seal/ledger/2000000009-unrelated.md"
MEMBER_INTO = "seal/ledger/4000000001-the-re-reading-item.md"


def three_readings(repo, m_at, n_at, carrier="the root"):
    """One family of three readings of one unit, the code back at h1.

    R, the root, sits in `seal/releases/0.1.0.md`, dated 2026-01-01, and
    cites `handler` as it is. M is an older `Re-read ·` of R at h1, dated
    2026-02-01, folded into `seal/releases/0.2.0.md` or sitting in a
    fragment (M_AT `release` or `fragment`). N is the newest `Re-read ·` of R
    at h2, dated 2026-03-01, in another fragment or folded into
    `seal/releases/0.3.0.md` (N_AT likewise). N is the only reading that
    does not hold, and it outranks the ones that do, so every member carrying
    the unit reads DRIFTED under `--strict`. An unrelated fragment holds one
    row of its own, which holds.

    CARRIER says which members carry that unit. `the root`: it is `handler`,
    and R records h1 too. `re-reads only`: it is `other`, which R does not
    cite, so the unit is held by a released row only where M or N is folded,
    and by fragment rows alone where both sit in fragments.

    Returns `{"R": file, "M": file, "N": file}`, each relative to the repo.
    The two placements and the carrier are the axes `released_drift`'s
    family filter and its choice of reading are keyed on; a member kind
    `ledger_kind` names a third way is a third value for the placements, and
    belongs here."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    other = unit_hash(repo, "src/service.py", "other")
    unit = "handler" if carrier == "the root" else "other"
    h1 = unit_hash(repo, "src/service.py", unit)
    if unit == "handler":
        edit_handler(repo)
    else:
        (repo / "src" / "service.py").write_text(
            SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
        )
    h2 = unit_hash(repo, "src/service.py", unit)
    files = {"R": R_FILE}
    for name, h, date, at, version, item in (
        ("M", h1, "2026-02-01", m_at, "0.2.0", "2000000002-the-older-re-read"),
        ("N", h2, "2026-03-01", n_at, "0.3.0", "3000000003-the-newer-re-read"),
    ):
        row = (
            f"| Re-read · R1 · handler adds one | `{cite}`, "
            f"`src/service.py#{unit}@{h}` | read | {date} | Re-read {date} |"
        )
        if at == "release":
            released(repo, [row], version=version, section=f"### {item}")
            files[name] = f"seal/releases/{version}.md"
        else:
            fragment(repo, [row], name=item)
            files[name] = f"seal/ledger/{item}.md"
    fragment(
        repo,
        [
            f"| U1 · other doubles | `src/service.py#other@{other}` | read | 2026-01-01 | |"
        ],
        name="2000000009-unrelated",
    )
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    return files


NARROWINGS = {
    "R's file": ("R",),
    "M's file": ("M",),
    "N's file": ("N",),
    "R's and M's files": ("R", "M"),
    "an unrelated fragment": (UNRELATED,),
    "no --ledger": (),
}
MODES = ("no freeze", "freeze without --into", "freeze with --into")


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("narrowed", list(NARROWINGS))
@pytest.mark.parametrize("n_at", ("fragment", "release"))
@pytest.mark.parametrize("m_at", ("release", "fragment"))
@pytest.mark.parametrize("carrier", ("the root", "re-reads only"))
def test_a_narrowed_reverify_exits_0_only_where_the_narrowed_strict_does(
    repo, carrier, m_at, n_at, narrowed, mode
):
    """The class round 3's 🟡 16 is one instance of, by construction: which
    members carry the drifted coordinate (the root among them, or only its
    re-reads, so with both re-reads in fragments no released row holds it),
    where a family's older reading M and newest reading N sit (a folded
    release file or a fragment), which files `--ledger` names, and whether
    the freeze is declared and `--into` given. 2 x 2 x 2 x 6 x 3 cells.

    Asserted per cell, never as a per-cell expected value: a narrowed
    `--reverify` that exits 0 is followed by a `--strict` with the same
    narrowing that exits 0 too. Under the freeze no released byte moves, and
    with `--into`, wherever the narrowing holds a member, the whole tree then
    checks clean. A narrowed run names the files it did not read before
    anything else it prints."""
    files = three_readings(repo, m_at, n_at, carrier)
    flags = []
    for name in NARROWINGS[narrowed]:
        flags += ["--ledger", files.get(name, name)]
    if mode != "no freeze":
        frozen(repo, "0")
    into = ["--into", MEMBER_INTO, "--checked", "2026-04-01"]
    before = digests(repo)
    fix = run(
        ["--reverify", *(into if mode == "freeze with --into" else []), *flags, "."],
        repo,
    )
    assert fix.returncode in (0, 1), fix.stdout + fix.stderr
    if flags:
        assert fix.stdout.startswith("--ledger narrowed this run"), fix.stdout
    check = run(["--strict", *flags, "."], repo)
    if fix.returncode == 0:
        assert check.returncode == 0, (
            f"--reverify exited 0 and --strict with the same narrowing exited "
            f"{check.returncode}\n{fix.stdout}\n---\n{check.stdout}"
        )
    if mode != "no freeze":
        assert digests(repo) == before, fix.stdout
    if mode == "freeze with --into" and narrowed != "an unrelated fragment":
        whole = run(["--strict", "."], repo)
        assert whole.returncode == 0, fix.stdout + "\n---\n" + whole.stdout


@pytest.mark.parametrize("mode", MODES)
def test_a_narrowed_reverify_answers_for_a_coordinate_only_fragments_carry(repo, mode):
    """Round 1's 🟡 1, the axis the first 72 cells held fixed: which members
    carry the coordinate. R cites `handler` alone; an older fragment re-read
    M adds `other` as it is, a newer re-read N in another fragment holds
    other content, and no released member carries `other`. A run narrowed to
    M's fragment exits 0 only where `--strict` with the same narrowing does,
    and names or writes for the family's root otherwise."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    o1 = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    o2 = unit_hash(repo, "src/service.py", "other")
    for name, h, date in (
        ("2000000002-the-older-re-read", o1, "2026-02-01"),
        ("3000000003-the-newer-re-read", o2, "2026-03-01"),
    ):
        fragment(
            repo,
            [
                f"| Re-read · R1 · handler adds one | `{cite}`, "
                f"`src/service.py#other@{h}` | read | {date} | Re-read {date} |"
            ],
            name=name,
        )
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    flags = ["--ledger", "seal/ledger/2000000002-the-older-re-read.md"]
    if mode != "no freeze":
        frozen(repo, "0")
    into = ["--into", MEMBER_INTO, "--checked", "2026-04-01"]
    fix = run(
        ["--reverify", *(into if mode == "freeze with --into" else []), *flags, "."],
        repo,
    )
    assert fix.returncode in (0, 1), fix.stdout + fix.stderr
    check = run(["--strict", *flags, "."], repo)
    if fix.returncode == 0:
        assert check.returncode == 0, fix.stdout + "\n---\n" + check.stdout
    if mode == "freeze with --into":
        assert "citing seal/releases/0.1.0.md:5" in fix.stdout, fix.stdout
        assert run(["--strict", "."], repo).returncode == 0
    else:
        assert fix.returncode == 1, fix.stdout
        assert "LEFT  seal/releases/0.1.0.md:5" in fix.stdout, fix.stdout


def test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read(repo):
    """The guard beside round 1's 🟡 1 fix (⬜ 9): a coordinate is graded
    from a fragment member only under a released root. A `Corrected ·` row
    in a fragment roots its own family, and here its one coordinate names a
    statement the code no longer has, which an in-place re-stamp leaves.
    Under the freeze the run names no `Re-read ·` owed to that fragment row:
    a citation into a fragment is refused, and the row is the fragment's own
    to repair."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    text = (repo / "src" / "service.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/service.py", "other", text)
    (inside,) = ec.minor_region("src/service.py", text, places[0], '"x * 2"')
    stated = ec.content_hash(ec.gfm_lines(text)[inside[0] - 1 : inside[1]])
    fragment(
        repo,
        [
            f"| Corrected · other doubles | `{citation(r, 'R1 · handler adds one')}`, "
            f'`src/service.py#other>"x * 2"@{stated}` | read | 2026-02-01 | '
            "Corrected 2026-02-01 by work item 2000000001 |"
        ],
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    frozen(repo, "0")
    out = run(["--reverify", "."], repo)
    left = [line for line in out.stdout.splitlines() if line.startswith("  LEFT")]
    assert not [line for line in left if "seal/ledger/" in line], out.stdout


@pytest.mark.parametrize("mode", MODES)
def test_a_narrowing_to_a_superseded_root_answers_nothing(repo, mode):
    """The control outside the product: R is superseded by a `Corrected ·`
    row, so nothing in R's family is graded, and a run narrowed to R's file
    owes nothing. Without the correction the same narrowing exits 1, or,
    with `--into`, writes the row R's family owes and exits 0."""
    three_readings(repo, "release", "fragment")
    other = unit_hash(repo, "src/service.py", "other")
    r = (repo / R_FILE).read_text(encoding="utf-8").splitlines()[4]
    fragment(
        repo,
        [
            f"| Corrected · the doubling lives in other | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#other@{other}` | read | 2026-03-15 | "
            "Corrected 2026-03-15 by work item 3000000004 |"
        ],
        name="3000000004-the-correction",
    )
    if mode != "no freeze":
        frozen(repo, "0")
    into = ["--into", MEMBER_INTO, "--checked", "2026-04-01"]
    out = run(
        [
            "--reverify",
            *(into if mode == "freeze with --into" else []),
            "--ledger",
            R_FILE,
            ".",
        ],
        repo,
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "LEFT" not in out.stdout, out.stdout


@pytest.mark.parametrize("carrier", ("the root", "re-reads only"))
@pytest.mark.parametrize("member", ("release", "fragment"))
def test_a_frozen_reverify_narrowed_to_a_member_names_the_root_with_into(
    repo, member, carrier
):
    """S3 (round 1, ⬜ 7): under the freeze and without `--into`, a run
    narrowed to the file holding the older reading M names the family's
    root, not M, with the `--into` repair, and writes no released byte --
    also where the drifted coordinate is one only the re-reads carry, so the
    reading the run picks is M's own."""
    files = three_readings(repo, member, "fragment", carrier)
    frozen(repo, "0")
    before = digests(repo)
    out = run(["--reverify", "--ledger", files["M"], "."], repo)
    assert out.returncode == 1, out.stdout
    left = [line for line in out.stdout.splitlines() if "LEFT" in line]
    assert len(left) == 1, out.stdout
    assert left[0].split()[:2] == ["LEFT", "seal/releases/0.1.0.md:5"], left[0]
    assert "--reverify --into seal/ledger/<work-item-id>.md" in left[0], left[0]
    assert digests(repo) == before


def test_a_narrowed_into_re_reads_a_family_whose_folded_member_it_read(repo):
    """Round 3's first case (🟡 16): under the freeze, narrowed to the release
    file holding a folded re-read C of an older release's R, while a newer
    fragment re-read F holds other content. `--into` writes the re-read the
    family owes, citing R, and the tree checks clean. It wrote nothing and
    exited 0, because the family's root sits in a file the run did not
    read."""
    three_readings(repo, "release", "fragment")
    frozen(repo, "0")
    out = run(
        [
            "--reverify",
            "--into",
            MEMBER_INTO,
            "--checked",
            "2026-04-01",
            "--ledger",
            "seal/releases/0.2.0.md",
            ".",
        ],
        repo,
    )
    assert "1 citing row written" in out.stdout, out.stdout
    assert "citing seal/releases/0.1.0.md:5" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 0


def test_an_unfrozen_reverify_narrowed_to_a_folded_member_names_the_root(repo):
    """Round 3's second case (🟡 16): the same family without the freeze. The
    narrowed run cannot re-stamp the newer reading, so it exits 1 and names
    the family's root, the row a `Re-read ·` cites, though it did not read
    the root's file."""
    three_readings(repo, "release", "fragment")
    out = run(["--reverify", "--ledger", "seal/releases/0.2.0.md", "."], repo)
    assert out.returncode == 1, out.stdout
    left = [line for line in out.stdout.splitlines() if "LEFT" in line]
    assert left, out.stdout
    assert left[0].split()[:2] == ["LEFT", "seal/releases/0.1.0.md:5"], left[0]


@pytest.mark.parametrize(
    "cell, said",
    [
        (
            "2026-13-45",
            "the reading dated 2026-13-45, a date the calendar does not have",
        ),
        (
            "2026-13-45, 2026-02-30",
            "the reading dated 2026-13-45 and 2026-02-30, dates the calendar does not have",
        ),
        (
            "2026-13-45, 2026-02-30, 2026-00-00",
            "the reading dated 2026-13-45, 2026-02-30 and 2026-00-00, dates the "
            "calendar does not have",
        ),
        (
            "2026-13-45, 2026-13-45",
            "the reading dated 2026-13-45, a date the calendar does not have",
        ),
        ("", "the reading of no date"),
    ],
)
def test_a_checked_date_the_calendar_does_not_have_is_named_as_written(
    repo, cell, said
):
    """Round 3's ⬜ 17: R's `Checked` cell holds a date the calendar does not
    have, a fragment re-read dated 2026-02-01 holds other content, and the
    code is back at R's hash. R is DRIFTED, as before, and the line names
    the date as the cell wrote it, because fixing that typo is the repair.
    It said "the reading of no date", which is kept for a cell with no
    date at all."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | {cell} | |"
        ],
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h2}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    out = run(["--strict", "."], repo)
    assert out.returncode == 2, out.stdout
    section = ledger_section(out.stdout, R_FILE)
    assert f"matches only {said}; the newest reading" in section, section


# --- `--into` refuses a row its `--checked` date cannot make count (#746, ⬜ 12)
#
# A `Re-read ·` row is a new reading at exactly `--checked`. Where a newer
# reading of a coordinate it carries sits out of the run's reach -- in a
# fragment the narrowing left out, or in a released file -- that newer reading
# outranks the new row and the family stays DRIFTED. No `Re-read ·` row is
# written for it and it is named; the moves under it are still recorded where
# a pact clause is cited (round 1 of #746, yellow 2).

N_PLACE = {
    "fragment": "seal/ledger/3000000003-the-newer-re-read.md:1",
    "release": "seal/releases/0.3.0.md:5",
}
# Where N is a fragment, a run that reads it re-stamps it in place, which
# clears the family before any `Re-read ·` row is owed; so the run is
# narrowed to M's file, which leaves N out. A folded N is out of every run's
# reach, so that run is not narrowed.
STALE_TREES = [
    (m_at, n_at, carrier)
    for carrier in ("the root", "re-reads only")
    for m_at in ("release", "fragment")
    for n_at in ("fragment", "release")
]


def stale_run(repo, m_at, n_at, carrier, checked):
    files = three_readings(repo, m_at, n_at, carrier)
    frozen(repo, "0")
    flags = ["--ledger", files["M"]] if n_at == "fragment" else []
    out = run(
        ["--reverify", "--into", MEMBER_INTO, "--checked", checked, *flags, "."], repo
    )
    return files, flags, out


@pytest.mark.parametrize("m_at, n_at, carrier", STALE_TREES)
def test_into_refuses_a_row_its_checked_date_cannot_make_count(
    repo, m_at, n_at, carrier
):
    """⬜ 12 (A1, A2). `--checked 2026-02-15` falls between M (2026-02-01) and
    N (2026-03-01, other content). The row it would write is outranked by N,
    so the run writes nothing, prints no `wrote` line, and exits 1 naming the
    root, the date, N's date and place, and the repair. It wrote the row and
    exited 0 while `--strict` read the family DRIFTED."""
    _, _, out = stale_run(repo, m_at, n_at, carrier, "2026-02-15")
    assert out.returncode == 1, out.stdout + out.stderr
    assert not (repo / MEMBER_INTO).exists(), out.stdout
    assert "  wrote " not in out.stdout, out.stdout
    assert "0 citing rows written · 1 released row left" in out.stdout, out.stdout
    left = [line for line in out.stdout.splitlines() if line.startswith("  LEFT")]
    unit = "handler" if carrier == "the root" else "other"
    assert left == [
        "  LEFT  seal/releases/0.1.0.md:5  R1 · handler adds one — "
        "`--checked 2026-02-15` is older than the newest reading of "
        f"src/service.py#{unit}, 2026-03-01 at {N_PLACE[n_at]}, so a "
        "`Re-read ·` row dated 2026-02-15 would not outrank it and the row "
        "would stay DRIFTED; no `Re-read ·` row was written for this row — "
        "read the code again and run it with the date of that reading"
    ], out.stdout


@pytest.mark.parametrize("m_at, n_at, carrier", STALE_TREES)
def test_into_writes_a_row_dated_on_the_newest_reading(repo, m_at, n_at, carrier):
    """A3. A `--checked` equal to N's date ties with it, the two readings are
    a union, and the row is written and clears the family: only a date
    strictly older than the newest reading is refused."""
    _, flags, out = stale_run(repo, m_at, n_at, carrier, "2026-03-01")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "1 citing row written · 0 released rows left" in out.stdout, out.stdout
    assert run(["--strict", *flags, "."], repo).returncode == 0
    assert run(["--strict", "."], repo).returncode == 0


@pytest.mark.parametrize("checked", ("2026-02-15", "2026-03-01"))
@pytest.mark.parametrize("narrowed", ("M's file", "N's file", "no --ledger"))
@pytest.mark.parametrize("m_at, n_at, carrier", STALE_TREES)
def test_a_reverify_into_exits_0_only_where_strict_does_at_any_date(
    repo, m_at, n_at, carrier, narrowed, checked
):
    """A4, the grid's invariant with the date as its axis (questions.md Q4):
    the narrowed grid runs `--into` at a date newer than every reading, so a
    date between M and N was never asked. Over every placement and carrier,
    narrowed to M's file, to N's, or not at all, and at a date between M and
    N or on N's: a `--reverify --into` that exits 0 is followed by a
    `--strict` with the same narrowing that exits 0, and no released byte
    moves."""
    files = three_readings(repo, m_at, n_at, carrier)
    frozen(repo, "0")
    flags = [] if narrowed == "no --ledger" else ["--ledger", files[narrowed[0]]]
    before = digests(repo)
    fix = run(
        ["--reverify", "--into", MEMBER_INTO, "--checked", checked, *flags, "."], repo
    )
    assert fix.returncode in (0, 1), fix.stdout + fix.stderr
    assert digests(repo) == before, fix.stdout
    if fix.returncode == 0:
        check = run(["--strict", *flags, "."], repo)
        assert check.returncode == 0, fix.stdout + "\n---\n" + check.stdout


def test_a_refused_row_does_not_stop_the_rows_beside_it(repo):
    """A6. Two drifted released rows in one run: R1 was read on 2026-01-01
    and R2 on 2026-03-01. `--checked 2026-02-01` writes R1's `Re-read ·` row,
    leaves R2's whole, and exits 1 for the row it left."""
    h = unit_hash(repo, "src/service.py", "handler")
    released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |",
            f"| R2 · handler returns its sum | `src/service.py#handler@{h}` | read | 2026-03-01 | |",
        ],
    )
    frozen(repo, "0")
    edit_handler(repo)
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 1, out.stdout + out.stderr
    written = (repo / INTO).read_text(encoding="utf-8").splitlines()
    assert len(written) == 1 and written[0].startswith("| Re-read · R1 ·"), written
    assert "1 citing row written · 1 released row left" in out.stdout, out.stdout
    left = [line for line in out.stdout.splitlines() if line.startswith("  LEFT")]
    assert len(left) == 1, out.stdout
    assert left[0].startswith(
        "  LEFT  seal/releases/0.1.0.md:6  R2 · handler returns its sum — "
        "`--checked 2026-02-01` is older than the newest reading of "
        "src/service.py#handler, 2026-03-01 at seal/releases/0.1.0.md:6"
    ), left[0]


def test_a_reading_dated_after_today_is_named_with_a_correction(repo):
    """A7. A released row whose `Checked` date is after today: `--checked`
    refuses a date after today, so no `Re-read ·` row can outrank that
    reading, and the line names a `Corrected ·` row as the repair. `--strict`
    does not refuse such a date (questions.md Q2, measured), so the tree is
    an ordinary drifted row otherwise."""
    h = unit_hash(repo, "src/service.py", "handler")
    released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2999-01-01 | |"
        ],
    )
    frozen(repo, "0")
    edit_handler(repo)
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 1, out.stdout + out.stderr
    assert not (repo / INTO).exists(), out.stdout
    left = [line for line in out.stdout.splitlines() if line.startswith("  LEFT")]
    assert len(left) == 1, out.stdout
    assert left[0].startswith(
        "  LEFT  seal/releases/0.1.0.md:5  R1 · handler adds one — "
        "`--checked 2026-02-01` is older than the newest reading of "
        "src/service.py#handler, 2999-01-01 at seal/releases/0.1.0.md:5, "
        "which is after today ("
    ), left[0]
    assert left[0].endswith(
        "and `--checked` takes no date after today, so no `Re-read ·` row can "
        "outrank it; no `Re-read ·` row was written for this row — a "
        "`Corrected ·` row in your own fragment supersedes the row and every "
        "reading of it"
    ), left[0]


def test_the_refusal_reads_the_date_the_grading_reads():
    """The refusal and the grading order readings by one function, so the two
    cannot disagree about which reading is newest (spec S1): a date the
    calendar does not have orders nothing, and the newest of several wins."""
    header = list(ec.LEDGER_COLUMNS)
    cells = [
        "R1",
        "`a.py#f@00000000`",
        "read",
        "2026-01-01 · 2026-13-45 · 2026-03-01",
        "",
    ]
    assert ec.reading_date(header, cells) == "2026-03-01"
    cells[3] = "2026-13-45"
    assert ec.reading_date(header, cells) == ""


def test_a_refusal_names_the_newest_of_the_readings_that_outrank_the_row(repo):
    """R1 cites `handler` and `other`; a fragment re-read dated 2026-03-01
    holds other content for `handler`, another dated 2026-04-01 for `other`,
    and the run, narrowed to R's file, reaches neither. Both outrank
    `--checked 2026-02-15`, and the line names the later one, 2026-04-01,
    which is the reading a new reading has to reach."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler and other | `src/service.py#handler@{h}`, "
            f"`src/service.py#other@{o}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler and other")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("y = x + 1", "y = x + 2").replace("x * 2", "x * 3"),
        encoding="utf-8",
    )
    for name, unit, date in (
        ("3000000003-the-handler-re-read", "handler", "2026-03-01"),
        ("3000000004-the-other-re-read", "other", "2026-04-01"),
    ):
        fragment(
            repo,
            [
                f"| Re-read · R1 · handler and other | `{cite}`, "
                f"`src/service.py#{unit}@{unit_hash(repo, 'src/service.py', unit)}` "
                f"| read | {date} | Re-read {date} |"
            ],
            name=name,
        )
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    frozen(repo, "0")
    out = run(
        [
            "--reverify",
            "--into",
            MEMBER_INTO,
            "--checked",
            "2026-02-15",
            "--ledger",
            R_FILE,
            ".",
        ],
        repo,
    )
    assert out.returncode == 1, out.stdout + out.stderr
    left = [line for line in out.stdout.splitlines() if line.startswith("  LEFT")]
    assert len(left) == 1, out.stdout
    assert (
        "the newest reading of src/service.py#other, 2026-04-01 at "
        "seal/ledger/3000000004-the-other-re-read.md:1, so a"
    ) in left[0], left[0]


@pytest.mark.parametrize(
    "where, sentence",
    [
        (
            "docs/the-evidence-ledger.md",
            "the run writes no row for it, still records the pact changes its "
            "moved coordinates owe, names it with both dates and the place of the "
            "later reading, and exits 1. Read the code "
            "again and date that reading; a date equal to the newest ties and is "
            "written",
        ),
        (
            "docs/the-evidence-ledger.md",
            "a newest reading dated after today, which no `--checked` reaches, "
            "takes a `Corrected ·` row",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "A row a reading dated after --checked outranks gets no Re-read row, "
            "is named, and the run exits 1.",
        ),
        (
            "docs/the-pact.md",
            "finds the code under such a row moved where `--into` refuses it a "
            "`Re-read ·` row for a stale `--checked`, or leaves a coordinate of "
            "one BROKEN, the same command records a pact change, and that test "
            "is the whole trigger.",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "A row `--into` refuses a `Re-read ·` row for a stale --checked is "
            "recorded too, by the run that refuses it (#746).",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "or `--into` refuses such a row a `Re-read ·` row for a stale "
            "`--checked` while the code under it moved, one row per ledger row "
            "is appended to",
        ),
        (
            "templates/config.md",
            "`evidence-check --reverify` records a pact change in "
            "`seal/pact-changes/<work-item-id>.md` where `docs/the-pact.md` §*A "
            "signatory records a pact change* says, and that section's first "
            "sentence is the whole trigger.",
        ),
    ],
    ids=[
        "the home: the refusal",
        "the home: after today",
        "the usage",
        "the pact's trigger",
        "the usage: the signatory's record",
        "the skill: the signatory's record",
        "the config template: the trigger's home",
    ],
)
def test_the_home_and_the_usage_say_a_stale_row_is_left(where, sentence):
    """§14: the refusal is something a person reads before running `--into`
    with a back-dated `--checked`, so each sentence is pinned where it
    stands (#746)."""
    with open(os.path.join(ROOT, where), encoding="utf-8") as handle:
        text = " ".join(handle.read().split())
    assert sentence in text, (where, sentence)


# --- what no re-read clears (#746, ⬜ 11) ------------------------------------
#
# `docs/the-evidence-ledger.md` names five things `--reverify` leaves at exit 0
# while `--strict` exits 2: a double correction, a BROKEN coordinate, a family
# rooted in a fragment whose anchored statement is gone, a citing row refused
# MALFORMED, and a citation whose released line changed. Each case below holds
# one of them over the three modes, narrowed to the file holding a row
# `--strict` names or not narrowed. Each pins behaviour that already held, so
# each was seen red under a mutation of the code that grades it.

WITHOUT_HANDLER = "def other(x):\n    return x * 2\n"


def both_exits(repo, mode, flags):
    """`(--reverify's exit, --strict's exit)` for one run in MODE, both
    narrowed by FLAGS, the `--reverify` run's output beside them."""
    if mode != "no freeze":
        frozen(repo, "0")
    into = ["--into", MEMBER_INTO, "--checked", "2026-04-01"]
    fix = run(
        ["--reverify", *(into if mode == "freeze with --into" else []), *flags, "."],
        repo,
    )
    check = run(["--strict", *flags, "."], repo)
    return fix.returncode, check.returncode, fix.stdout + fix.stderr


def placed(repo, row, at, version, item):
    """ROW written into a fragment named ITEM, or folded into
    `seal/releases/<VERSION>.md` under ITEM's heading; its file, relative."""
    if at == "folded":
        released(repo, [row], version=version, section=f"### {item}")
        return f"seal/releases/{version}.md"
    fragment(repo, [row], name=item)
    return f"seal/ledger/{item}.md"


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("narrowed", ("no --ledger", "the first", "the second"))
@pytest.mark.parametrize("at", ("fragment", "folded"))
def test_a_double_correction_is_left_at_exit_0_and_read_at_exit_2(
    repo, at, narrowed, mode
):
    """A8. Two `Corrected ·` rows of one released row, both in fragments or
    both folded: `--strict` names each and exits 2, and `--reverify` exits 0,
    because which claim stays is a person's choice."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    files = [
        placed(
            repo,
            f"| Corrected · handler adds {claim} | `{cite}`, `src/service.py#handler@{h}` "
            "| read | 2026-02-01 | Corrected 2026-02-01 |",
            at,
            version,
            item,
        )
        for claim, version, item in (
            ("two", "0.2.0", "2000000001-a"),
            ("three", "0.3.0", "2000000002-b"),
        )
    ]
    flags = {
        "no --ledger": [],
        "the first": ["--ledger", files[0]],
        "the second": ["--ledger", files[1]],
    }[narrowed]
    fix, check, out = both_exits(repo, mode, flags)
    assert (fix, check) == (0, 2), out


BROKEN_CARRIERS = ("a released row", "a fragment row", "a folded re-read", "a re-read")


def broken_tree(repo, carrier):
    """A coordinate whose unit is gone, carried as CARRIER says. A re-read
    carries `other`, which its root does not cite, so where it sits in a
    fragment no released row carries the coordinate. Returns the carrier's
    file."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    if carrier == "a fragment row":
        fragment(
            repo,
            [f"| F1 · handler | `src/service.py#handler@{h}` | read | 2026-01-01 | |"],
            name="2000000001-f",
        )
        (repo / "src" / "service.py").write_text(WITHOUT_HANDLER, encoding="utf-8")
        return "seal/ledger/2000000001-f.md"
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    if carrier == "a released row":
        (repo / "src" / "service.py").write_text(WITHOUT_HANDLER, encoding="utf-8")
        return R_FILE
    at = "folded" if carrier == "a folded re-read" else "fragment"
    where = placed(
        repo,
        f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
        f"`src/service.py#other@{o}` | read | 2026-02-01 | Re-read 2026-02-01 |",
        at,
        "0.2.0",
        "2000000002-m",
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.split("\n\n\ndef other")[0] + "\n", encoding="utf-8"
    )
    return where


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("narrowed", (False, True))
@pytest.mark.parametrize("carrier", BROKEN_CARRIERS)
def test_a_broken_coordinate_is_named_only_where_a_released_row_carries_it_frozen(
    repo, carrier, narrowed, mode
):
    """A9. `--strict` exits 2 over a BROKEN coordinate wherever it sits.
    `--reverify` names it, with the `Corrected ·` repair, and exits 1 only
    where a released row carries it under the freeze; where only fragment
    rows carry it, or without the freeze, it exits 0."""
    where = broken_tree(repo, carrier)
    flags = ["--ledger", where] if narrowed else []
    fix, check, out = both_exits(repo, mode, flags)
    named = mode != "no freeze" and carrier in ("a released row", "a folded re-read")
    assert (fix, check) == (1 if named else 0, 2), out
    if named:
        assert "BROKEN" in out and "`Corrected ·` row" in out, out


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("narrowed", (False, True))
@pytest.mark.parametrize("at", ("fragment", "folded"))
def test_a_correction_whose_anchored_statement_is_gone_is_named_only_released(
    repo, at, narrowed, mode
):
    """A10. A `Corrected ·` row roots its own family, and its one coordinate
    names a statement the code no longer has. In a fragment, the in-place
    re-stamp has nothing to hash and leaves it, and a family rooted in a
    fragment is owed no released re-read: `--reverify` exits 0 while
    `--strict` exits 2. Folded, the root is released and the run names it and
    exits 1."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    text = (repo / "src" / "service.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/service.py", "other", text)
    (inside,) = ec.minor_region("src/service.py", text, places[0], '"x * 2"')
    stated = ec.content_hash(ec.gfm_lines(text)[inside[0] - 1 : inside[1]])
    where = placed(
        repo,
        f"| Corrected · other doubles | `{citation(r, 'R1 · handler adds one')}`, "
        f'`src/service.py#other>"x * 2"@{stated}` | read | 2026-02-01 | '
        "Corrected 2026-02-01 by work item 2000000001 |",
        at,
        "0.2.0",
        "2000000001-c",
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    flags = ["--ledger", where] if narrowed else []
    fix, check, out = both_exits(repo, mode, flags)
    assert (fix, check) == (0 if at == "fragment" else 1, 2), out


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("narrowed", (False, True))
@pytest.mark.parametrize("shape", ("no marker", "a citation into a fragment"))
def test_a_citing_row_refused_malformed_is_left_at_exit_0(repo, shape, narrowed, mode):
    """A citing row `family_view` refuses: one with no `Re-read <date>` in its
    Notes, or one whose citation names a fragment row. `--strict` exits 2 on
    the refusal, and `--reverify` exits 0, because the repair is an edit."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    if shape == "no marker":
        (r,) = released(
            repo,
            [
                f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
            ],
        )
        cite = citation(r, "R1 · handler adds one")
        notes = "read again"
    else:
        f = fragment(
            repo,
            [f"| F1 · handler | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"],
            name="2000000001-f",
        )
        first = f.read_text(encoding="utf-8").splitlines()[0]
        cite = f'seal/ledger/2000000001-f.md#"F1 · handler"@{line_hash(first)}'
        notes = "Re-read 2026-02-01"
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, "
            f"`src/service.py#handler@{h2}` | read | 2026-02-01 | {notes} |"
        ],
        name="2000000002-g",
    )
    flags = ["--ledger", "seal/ledger/2000000002-g.md"] if narrowed else []
    fix, check, out = both_exits(repo, mode, flags)
    assert (fix, check) == (0, 2), out
    strict = run(["--strict", *flags, "."], repo).stdout
    assert any(line.strip().startswith("MALFORMED") for line in strict.splitlines()), (
        strict
    )


@pytest.mark.parametrize("mode", ("freeze without --into", "freeze with --into"))
@pytest.mark.parametrize("narrowed", (False, True))
def test_a_folded_citation_whose_released_line_changed_is_left_at_exit_0(
    repo, narrowed, mode
):
    """Under the freeze, a folded `Re-read ·` row whose cited released line
    was edited: the citation is DRIFTED, `--strict` exits 2, and `--reverify`
    exits 0, because no released file is written. The freeze forbids that
    edit, and `correction-check` refuses it at the pull request."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    where = placed(
        repo,
        f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
        f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |",
        "folded",
        "0.2.0",
        "2000000002-m",
    )
    path = repo / R_FILE
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| 2026-01-01 | |", "| 2026-01-01 | edited |"
        ),
        encoding="utf-8",
    )
    flags = ["--ledger", where] if narrowed else []
    fix, check, out = both_exits(repo, mode, flags)
    assert (fix, check) == (0, 2), out


M_ITEM = "2000000002-m"


def unfrozen_r_and_m(repo):
    """S4's tree (#772), no freeze: R and its fragment re-read M both record
    `handler` as it was, and the code moves. Returns M's row as written."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    m = (
        f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
        f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
    )
    fragment(repo, [m], name=M_ITEM)
    edit_handler(repo)
    return m


def test_one_unfrozen_run_restamps_the_citation_its_restamp_moves(repo):
    """S4 (#772). One run re-stamps R in place, which moves the line M cites,
    and re-stamps M's citation against the line it moved R to, because a
    coordinate naming a line the run writes is judged against that line
    (#824): exit 0, and `--strict` exits 0 with no second run. The fragment
    sorts first, so a walk in file order hashed M's citation against R's old
    line."""
    unfrozen_r_and_m(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


def test_one_unfrozen_run_walks_an_older_release_before_the_newer_citing_it(repo):
    """S5 (#772). A citing row folded into `seal/releases/0.10.0.md` cites a
    row of `seal/releases/0.9.0.md`. File order puts `0.10.0.md` first, so
    a kind order (released files, then fragments) walks the citing file
    before the cited one too; the dependency order does not."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
        version="0.9.0",
    )
    released(
        repo,
        [
            f"| Re-read · R1 · handler adds one | "
            f"`{citation(r, 'R1 · handler adds one', version='0.9.0')}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        version="0.10.0",
        section="### 2000000002-m",
    )
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


@pytest.mark.parametrize("record", ["written", "refused", "R's file not written"])
def test_a_narrowed_unfrozen_run_names_the_citation_it_moved_and_left(
    repo, record, monkeypatch, capsys
):
    """S6 (#772). Narrowed to R's file, the run moves the line M cites and
    cannot re-stamp M, whose file the narrowing left out. It names M's row on
    a `LEFT` line with the repair, and exits 1 rather than 0. The line says
    the run re-stamps R's line, so it prints only once that write landed: a
    run whose pact-change record is refused writes nothing and says nothing
    of the kind, and neither does a run whose write of R's file fails (W8,
    round 1, yellow 3)."""
    unfrozen_r_and_m(repo)
    if record == "refused":
        # `always` owes a record for every moved row, and no work item names one.
        (repo / "seal" / "config.md").write_text(
            "| Item | Value |\n|---|---|\n| Mode | shared |\n"
            "| Pact | git@example.com:org/orders-api.git |\n"
            "| Pact notify | always |\n",
            encoding="utf-8",
        )
    before = (repo / R_FILE).read_bytes()
    args = ["--reverify", "--checked", "2026-03-01", "--ledger", R_FILE, "."]
    if record == "R's file not written":
        real = ec.write_atomic

        def refuses_r(path, text):
            if os.path.basename(path) == os.path.basename(R_FILE):
                raise PermissionError(13, "Permission denied")
            return real(path, text)

        monkeypatch.setattr(ec, "write_atomic", refuses_r)
        monkeypatch.setattr(sys, "argv", ["evidence_check.py", *args])
        monkeypatch.chdir(repo)
        assert ec.main() == 1
        out = capsys.readouterr().out
        assert f"  LEFT  {R_FILE}  could not be written" in out, out
        assert "its citation of" not in out, out
        assert (repo / R_FILE).read_bytes() == before
        return
    fix = run(args, repo)
    assert fix.returncode == 1, fix.stdout
    left = [line for line in fix.stdout.splitlines() if line.startswith("  LEFT")]
    if record == "refused":
        assert "nothing was re-stamped" in fix.stdout, fix.stdout
        assert "its citation of" not in fix.stdout, fix.stdout
        assert (repo / R_FILE).read_bytes() == before
        return
    assert left == [
        f"  LEFT  seal/ledger/{M_ITEM}.md:1  Re-read · R1 · handler adds one — its "
        f"citation of {R_FILE}:5 is DRIFTED: this run re-stamps the line it cites, "
        "and the narrowing left this row's file out; run it without `--ledger`"
    ], fix.stdout


@pytest.mark.parametrize(
    "shape",
    ["drifted before the run", "another file moved", "another row of its file moved"],
)
def test_a_narrowed_unfrozen_run_names_no_citation_it_did_not_move(repo, shape):
    """S6's other side. A citation already DRIFTED before the run is not
    this run's to name, and neither is one whose cited line the run does not
    move: narrowed to another release file, or to R's own file where only
    another row of it moves, R's line stays where M cites it."""
    unfrozen_r_and_m(repo)
    narrowed = R_FILE
    if shape == "drifted before the run":
        path = repo / R_FILE
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "| 2026-01-01 | |", "| 2026-01-01 | x |"
            ),
            encoding="utf-8",
        )
    else:
        h = unit_hash(repo, "src/service.py", "other")
        r2 = (
            f"| R2 · other doubles | `src/service.py#other@{h}` | read | 2026-01-01 | |"
        )
        if shape == "another file moved":
            released(repo, [r2], version="0.2.0")
            narrowed = "seal/releases/0.2.0.md"
        else:
            # R's file is written by the run, and M's line in it is not.
            (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
            r1 = (repo / R_FILE).read_text(encoding="utf-8").splitlines()[4]
            released(repo, [r1, r2])
        (repo / "src" / "service.py").write_text(
            (repo / "src" / "service.py")
            .read_text(encoding="utf-8")
            .replace("x * 2", "x * 3"),
            encoding="utf-8",
        )
    fix = run(
        ["--reverify", "--checked", "2026-03-01", "--ledger", narrowed, "."], repo
    )
    assert "its citation of" not in fix.stdout, fix.stdout


LEAVINGS = "a file citing itself, beside what the run leaves"


@pytest.mark.parametrize(
    "shape",
    [
        "a file citing itself",
        "a file citing itself, undated",
        "two files citing each other",
        LEAVINGS,
    ],
)
def test_one_unfrozen_run_settles_a_self_citing_file_in_one_run(repo, shape):
    """#772, round 1, yellow 1. A second fold of the newest release joins its
    file, so a release file can hold R1 and a `Re-read ·` row citing R1. The
    walk this replaced planned a file's own re-stamp only when its walk
    ended, so the citation was hashed against the old line, and `--strict`
    exited 2 until a second run; the same held for two files citing each
    other. Every citation is judged against the text the run writes, so one
    run leaves `--strict` at 0, and each row it dated is named once. Beside a
    row it cannot date, a coordinate it cannot place and a ledger citing it
    that will not decode, each of those is named once."""
    h = unit_hash(repo, "src/service.py", "handler")

    def r(n):
        return (
            f"| R{n} · handler adds one | `src/service.py#handler@{h}` | read "
            "| 2026-01-01 | |"
        )

    def reread(cite):
        return (
            f"| Re-read · the row it cites | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    if shape != "two files citing each other":
        left = []
        if shape == LEAVINGS:
            left = [
                # Four cells: no date cell, so `--checked` leaves it whole.
                f"| R2 · four cells | `src/service.py#handler@{h}` | read | 2026-01-01 |",
                f"| R3 · a gone unit | `src/service.py#gone@{h}` | read | 2026-01-01 | |",
                "| R4 · a bare hash | `src/service.py@abcdef12` | read | 2026-01-01 | |",
            ]
        # The citing row quotes R1's first cell, so the citation is taken with
        # it in place: a literal R1's line alone holds would match both lines.
        released(repo, [r(1), reread(citation(r(1), "R1 · handler adds one")), *left])
        cite = ec.citation_for(str(repo), str(repo / R_FILE), 5)
        released(repo, [r(1), reread(cite), *left])
        if shape == LEAVINGS:
            (repo / "seal" / "ledger").mkdir(parents=True)
            (repo / "seal" / "ledger" / "2000000004-bytes.md").write_bytes(
                (reread(cite) + "\n")
                .encode("utf-8")
                .replace(b"| read |", b"| caf\xe9 |")
            )
            with pytest.raises(UnicodeDecodeError):
                (repo / "seal" / "ledger" / "2000000004-bytes.md").read_text(
                    encoding="utf-8"
                )
            edit_handler(repo)
            fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
            assert fix.returncode == 1, fix.stdout
            for said in (
                "ledger unreadable",
                "its hash moved and the row has no date cell",
                "src/service.py#gone",
                "MALFORMED",
            ):
                assert fix.stdout.count(said) == 1, (said, fix.stdout)
            return
    else:
        released(repo, [r(2)], version="0.3.0")
        released(repo, [r(1)], version="0.4.0")
        to_4 = ec.citation_for(str(repo), str(repo / "seal/releases/0.4.0.md"), 5)
        to_3 = ec.citation_for(str(repo), str(repo / "seal/releases/0.3.0.md"), 5)
        released(repo, [r(2), reread(to_4)], version="0.3.0")
        released(repo, [r(1), reread(to_3)], version="0.4.0")
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    dated = [] if shape.endswith("undated") else ["--checked", "2026-03-01"]
    fix = run(["--reverify", *dated, "."], repo)
    assert fix.returncode == 0, fix.stdout
    named = [line for line in fix.stdout.splitlines() if line.startswith("    seal/")]
    assert named and len(named) == len(set(named)), fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


HASH_LINE = re.compile(r"^  (\S.*?)  ([0-9a-f]{6,12}) -> ([0-9a-f]{6,12})$")


def ledger_texts(repo):
    return "".join(
        p.read_text(encoding="utf-8") for p in sorted((repo / "seal").rglob("*.md"))
    )


@pytest.mark.parametrize("checked", [True, False], ids=["dated", "undated"])
@pytest.mark.parametrize("depth", [1, 2], ids=["a chain of one", "a chain of two"])
def test_one_unfrozen_run_names_each_coordinate_it_restamps_once(repo, depth, checked):
    """Round 2, yellow 1. A self-citing release holds R1 and a chain of
    `Re-read ·` rows each citing the one before; a fragment cites the last.
    The line a citation of a citing row quotes moves more than once over,
    by its code hash and date and by its own citation. The run names every
    coordinate it re-stamps once, from the hash the tree held before the run
    to the hash the tree holds after it, counts each once, and names each row
    it dated, or left undated, once. Red at 2a4ed251, which
    named such a citation once per walk -- the first line naming a hash no
    file ever held -- and counted every line."""
    h = unit_hash(repo, "src/service.py", "handler")
    rows = [
        f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
    ]

    def reread(cite, label):
        return (
            f"| Re-read · {label} | `{cite}`, `src/service.py#handler@{h}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    # Each citation is taken with the row quoting it in place, until the two
    # agree: a literal unique without the citing row may not be with it.
    for label in ["the row it cites", "the re-read of it"][:depth]:
        cite = citation(rows[-1], rows[-1].split(" | ")[0][2:])
        for _ in range(3):
            released(repo, [*rows, reread(cite, label)])
            again = ec.citation_for(str(repo), str(repo / R_FILE), 4 + len(rows))
            if again == cite:
                break
            cite = again
        rows.append(reread(cite, label))
    released(repo, rows)
    last = ec.citation_for(str(repo), str(repo / R_FILE), 4 + len(rows))
    # The fragment's first row moves only by its citation, so it is dated on
    # the walk that re-stamps it, and every offset after that date moves
    # before the second row's citation is re-stamped again: what names a
    # coordinate across walks cannot be its offset.
    o = unit_hash(repo, "src/service.py", "other")
    first = reread(last, "the fragment's first").replace(
        f"src/service.py#handler@{h}", f"src/service.py#other@{o}"
    )
    fragment(repo, [first, reread(last, "the fragment's")])
    assert run(["--strict", "."], repo).returncode == 0
    before = ledger_texts(repo)
    edit_handler(repo)
    dated = ["--checked", "2026-03-01"] if checked else []
    fix = run(["--reverify", *dated, "."], repo)
    assert fix.returncode == 0, fix.stdout
    after = ledger_texts(repo)
    named = [line for line in fix.stdout.splitlines() if line.startswith("    seal/")]
    assert len(named) == len(set(named)) == depth + 3, fix.stdout
    said = [HASH_LINE.match(line) for line in fix.stdout.splitlines()]
    said = [m for m in said if m]
    # R1's code, each citing row's code and citation, the fragment's second
    # row's too, and the fragment's first row's citation.
    assert len(said) == 1 + 2 * (depth + 1) + 1, fix.stdout
    assert f"{len(said)} rows re-verified" in fix.stdout, fix.stdout
    for m in said:
        assert f"@{m.group(2)}`" in before, (m.group(0), fix.stdout)
        assert f"@{m.group(3)}`" in after, (m.group(0), fix.stdout)
    # The fragment's two rows cite one line, so two lines name one citation.
    cited = [m.group(1) for m in said if m.group(1).startswith("seal/")]
    assert len(cited) == depth + 2 and len(set(cited)) == depth + 1, fix.stdout
    assert run(["--strict", "."], repo).returncode == 0


def test_a_row_naming_one_coordinate_twice_is_named_twice(repo):
    """What names a coordinate across walks keeps a row's two spellings of
    one coordinate apart (round 2, yellow 1): each is re-stamped and named,
    as before the walk was repeated."""
    h = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| F1 · handler, twice | `src/service.py#handler@{h}`, "
            f"`src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    said = [line for line in fix.stdout.splitlines() if HASH_LINE.match(line)]
    assert len(said) == 2 and "2 rows re-verified" in fix.stdout, fix.stdout


def test_a_ledger_coordinate_restamped_on_two_walks_is_one_move(repo):
    """#791. A row that is not a citing row names, among its Code grounds, a
    citing row of its own self-citing release file. The run moves that line
    twice over -- its code hash and date, and its citation, which names a
    line the run also moves -- and `reverify` hands MOVES one part for the
    coordinate naming it, from the hash the ledger held before the run to the
    hash the file holds after it: the permanent pact-change record is written
    from MOVES, and a part ending at a hash on the way names a hash no file
    ever held. Red at baeafe10, which handed over one part per walk."""
    line = ledger_coordinate_on_a_moving_line(repo)
    moves = []
    ec.reverify([str(repo / R_FILE)], str(repo), {}, None, "2026-03-01", moves)
    after = (repo / R_FILE).read_text(encoding="utf-8")
    x = [move for move in moves if move[1] == 7]
    assert len(x) == 1, moves
    assert x[0][3] == line.rsplit("@", 1)[1], moves
    assert f"@{x[0][4]}`" in after, moves
    assert run(["--strict", "."], repo).returncode == 0


def moved_then_left(repo):
    """X1's coordinate names the `Re-read ·` line of its own self-citing
    release, by a claim quoting that line's citation hash. The run re-stamps
    that citation, so in the text the run writes the quoted hash is gone and
    X1 is left. Returns X1's coordinate as written; `handler` is edited, so
    the run has its moves to make."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"

    def reread(cite):
        return (
            f"| Re-read · the row it cites | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    released(repo, [r1, reread(citation(r1, "R1 · handler adds one"))])
    cite = ec.citation_for(str(repo), str(repo / R_FILE), 5)
    # X1 sits under a second heading, so its own copy of the quoted hash is
    # outside the section its claim is read in.
    line = citation(reread(cite), f"@{cite.rsplit('@', 1)[1]}")
    (repo / R_FILE).write_text(
        f"## 0.1.0 — 2026-01-01\n\n{SECTION}\n\n{r1}\n{reread(cite)}\n\n"
        "### 1000000002-the-second-item\n\n"
        f"| X1 · other, beside the re-read | `src/service.py#other@{o}`, "
        f"`{line}` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    return line


def test_a_coordinate_whose_statement_the_run_removes_is_left_at_its_hash(repo, capsys):
    """S8, in `moved_then_left`'s tree. Nothing is written for a coordinate
    the run leaves, so X1 keeps the hash it recorded, MOVES holds
    `(recorded, None)` for it and nothing else, and its `left` line carries
    the check's *anchored statement is gone*. Red at e6d5a055, which wrote an
    intermediate hash on one walk and left it on the next, recording a move
    to a hash nobody read and BROKEN after it."""
    line = moved_then_left(repo)
    coord, recorded = line.rsplit("@", 1)
    moves = []
    ec.reverify([str(repo / R_FILE)], str(repo), {}, None, "2026-03-01", moves)
    out = capsys.readouterr().out
    assert f"`{line}`" in (repo / R_FILE).read_text(encoding="utf-8"), out
    x = [(old, new) for _ledger, number, _coord, old, new in moves if number == 10]
    assert x == [(recorded, None)], moves
    said = [s for s in out.splitlines() if s.startswith(f"  {coord}  ")]
    assert len(said) == 1, out
    assert "the anchored statement is gone" in said[0], said
    assert said[0].endswith(" — left"), said


def left_then_unchanged(repo, stale=False):
    """X1 was stamped while handler was at v1, quoting the citation hash its
    `Re-read ·` line held then; handler moved and came back, so the run
    re-stamps that line back to the bytes X1 recorded. Against the tree on
    disk the quoted hash is gone; against the text the run writes it is
    there, and X1 reads unchanged, or, where X1's hash is STALE, is
    re-stamped. Returns R_FILE's text as X1's hash says it ends."""
    o = unit_hash(repo, "src/service.py", "other")
    day = "2026-03-01"

    def r1(h):
        return (
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | {day} | |"
        )

    def reread(cite, h):
        return (
            f"| Re-read · the row it cites | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | {day} | Re-read {day} |"
        )

    def cite_for(h):
        released(repo, [r1(h), reread(citation(r1(h), "R1 · handler adds one"), h)])
        return ec.citation_for(str(repo), str(repo / R_FILE), 5)

    def write(h, cite, x):
        (repo / R_FILE).write_text(
            f"## 0.1.0 — 2026-01-01\n\n{SECTION}\n\n{r1(h)}\n{reread(cite, h)}\n\n"
            "### 1000000002-the-second-item\n\n"
            f"| X1 · other, beside the re-read | `src/service.py#other@{o}`, "
            f"`{x}` | read | {day} | |\n",
            encoding="utf-8",
        )

    h1 = unit_hash(repo, "src/service.py", "handler")
    cite1 = cite_for(h1)
    x = citation(reread(cite1, h1), f"@{cite1.rsplit('@', 1)[1]}")
    write(h1, cite1, x)
    assert run(["--strict", "."], repo).returncode == 0
    before = (repo / R_FILE).read_text(encoding="utf-8")
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    write(h2, cite_for(h2), x.rsplit("@", 1)[0] + "@0000beef" if stale else x)
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    return before


def test_a_coordinate_left_and_then_read_unchanged_records_nothing(repo):
    """Second post-review pass of #791, in `left_then_unchanged`'s tree: the
    file ends where X1's hash says. MOVES holds nothing for X1: a BROKEN from
    a reading against the tree on disk would write the permanent record a
    trigger for a coordinate `--strict` reads clean. Red at 5ef5d315."""
    before = left_then_unchanged(repo)
    moves = []
    ec.reverify([str(repo / R_FILE)], str(repo), {}, None, "2026-03-01", moves)
    assert (repo / R_FILE).read_text(encoding="utf-8") == before
    assert [m for m in moves if m[1] == 10] == [], moves
    assert run(["--strict", "."], repo).returncode == 0


def test_one_unfrozen_run_names_a_citing_row_it_left_whole_once(repo):
    """Round 2, white 2: the narrowed-run reader skips every file the run
    writes. A citing row in a table with no date column is left whole by
    `--checked`, so its citation of the line the run re-stamped stays
    DRIFTED. The `undatable` line names it, and no line says a narrowing
    left its file out: no narrowing did. Red with the skip removed."""
    h = unit_hash(repo, "src/service.py", "handler")
    released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read "
            "| 2026-01-01 | |"
        ],
    )
    cite = ec.citation_for(str(repo), str(repo / R_FILE), 5)
    (repo / "seal" / "releases" / "0.2.0.md").write_text(
        "## 0.2.0 — 2026-01-02\n\n### 1000000002-the-second-item\n\n"
        "| Clause | Code grounds | Verified behavior | Notes |\n|---|---|---|---|\n"
        f"| Re-read · the row it cites | `{cite}`, `src/service.py#handler@{h}` "
        "| read | Re-read 2026-02-01 |\n",
        encoding="utf-8",
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 1, fix.stdout
    left = [line for line in fix.stdout.splitlines() if line.startswith("  LEFT")]
    assert len(left) == 1, fix.stdout
    assert left[0].startswith(
        "  LEFT  seal/releases/0.2.0.md:7  its hash moved and the row has no date cell"
    ), fix.stdout


@pytest.mark.parametrize(
    "sentence",
    [
        "**Five things `--reverify` leaves at exit 0 while `--strict` exits 2.**",
        "A released row corrected by two `Corrected ·` rows.",
        "Only where a released row carries it under the freeze does `--reverify` "
        "name it, with the `Corrected ·` repair, and exit 1.",
        "A family rooted in a fragment, a `Corrected ·` row there, whose anchored "
        "statement is gone.",
        "A citing row refused `MALFORMED`: one without its marker, or one whose "
        "citation names a fragment row.",
        "A citation whose released line changed under it.",
        "Without the freeze it is not among them: one run over every ledger "
        "re-stamps a released row and every citation of it that it moves, "
        "because it walks a cited file before every file citing it (#772).",
        "A release file citing a row of itself, which a second fold writes, is "
        "walked again until it settles.",
        "A run narrowed with `--ledger` that moves a line cited from a file it "
        "left out names the citing row on a `LEFT` line and exits 1.",
        "Each repair is an edit or a correction, which a person makes.",
    ],
    ids=[
        "the five",
        "double correction",
        "broken",
        "statement gone",
        "malformed",
        "citation",
        "one unfrozen run",
        "a file citing itself",
        "a narrowed unfrozen run",
        "the lead: a person repairs each",
    ],
)
def test_the_home_names_each_thing_no_re_read_clears(sentence):
    """§14 for ⬜ 11: the paragraph a person reads before trusting a
    `--reverify` that exited 0, pinned sentence by sentence (#746)."""
    with open(
        os.path.join(ROOT, "docs", "the-evidence-ledger.md"), encoding="utf-8"
    ) as handle:
        text = " ".join(handle.read().split())
    assert sentence in text, sentence


# --- an in-place re-stamp leaves a reading its family already holds (#785) ---
#
# The family paragraph counts only a coordinate's newest readings, so a
# reading a newer one outranks is history. Re-stamping and dating it claims a
# reading nobody took, and the date can make it the newest. `reverify` judges
# each code coordinate once, before its first walk, by `family_view`'s own
# `held` and `superseded`.

A_ITEM = "2000000001-a"
B_ITEM = "3000000001-b"


def at_version(repo, n):
    """Write `handler` as `y = x + N`, and return its hash."""
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("y = x + 1", f"y = x + {n}"), encoding="utf-8"
    )
    return unit_hash(repo, "src/service.py", "handler")


def re_read_of(r, h, day, extra=""):
    """A `Re-read ·` row citing released R1 (row R), recording `handler` at H
    on DAY, with EXTRA coordinates after it."""
    return (
        f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
        f"`src/service.py#handler@{h}`{extra} | read | {day} | Re-read {day} |"
    )


def outranked_family(repo, b_day="2026-03-01"):
    """#785's probe: R1 at h0 on 2026-01-01, fragment A re-reading it at h1 on
    2026-02-01, fragment B at h2 on B_DAY, and the code at h2. Returns A's
    file. B holds, so `--strict` reads the family OK."""
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    h1 = at_version(repo, 2)
    a = fragment(repo, [re_read_of(r, h1, "2026-02-01")], name=A_ITEM)
    h2 = at_version(repo, 3)
    fragment(repo, [re_read_of(r, h2, b_day)], name=B_ITEM)
    return a


@pytest.mark.parametrize("checked", [True, False], ids=["dated", "undated"])
def test_an_in_place_reverify_leaves_a_reading_its_family_holds(repo, checked):
    """S1 and S6 (#785). Under the freeze, A is outranked by B, which holds.
    The run leaves A byte for byte, names it on no hash line, no dated line
    and no undated line, and exits 0; `--strict` still exits 0. Red at
    a3aa139a, which re-stamped A to h2 and dated it `2026-02-01 ·
    2026-04-01`, or named it undated."""
    a = outranked_family(repo)
    frozen(repo, "0")
    assert run(["--strict", "."], repo).returncode == 0
    before = a.read_bytes()
    dated = ["--checked", "2026-04-01"] if checked else []
    fix = run(["--reverify", *dated, "."], repo)
    assert fix.returncode == 0, fix.stdout
    assert a.read_bytes() == before, fix.stdout
    assert f"seal/ledger/{A_ITEM}.md" not in fix.stdout, fix.stdout
    assert not [line for line in fix.stdout.splitlines() if HASH_LINE.match(line)]
    assert run(["--strict", "."], repo).returncode == 0


@pytest.mark.parametrize("narrowed", [False, True], ids=["every ledger", "R's file"])
def test_an_unfrozen_reverify_leaves_a_root_a_newer_reading_holds(repo, narrowed):
    """S2 (#785). No freeze: R1 records h0, and fragment B, newer, holds h2.
    R1's line is left byte for byte, the run exits 0 and prints no `LEFT`
    line, over every ledger and narrowed to R1's file. Red at a3aa139a: the
    unnarrowed run re-stamped and dated R1, and the narrowed one did too,
    which moved the line B cites and exited 1 on `citations_left`."""
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    h2 = at_version(repo, 3)
    fragment(repo, [re_read_of(r, h2, "2026-02-01")], name=B_ITEM)
    assert run(["--strict", "."], repo).returncode == 0
    before = (repo / R_FILE).read_bytes()
    flags = ["--ledger", R_FILE] if narrowed else []
    fix = run(["--reverify", "--checked", "2026-03-01", *flags, "."], repo)
    assert fix.returncode == 0, fix.stdout
    assert (repo / R_FILE).read_bytes() == before, fix.stdout
    assert "LEFT" not in fix.stdout, fix.stdout
    assert run(["--strict", "."], repo).returncode == 0


def test_a_reading_tied_with_one_that_holds_is_left_alone(repo):
    """S3 (#785). A and B are dated the same day; B holds and A does not.
    Readings on one date are a union, so the family holds and A is left.
    Red at a3aa139a."""
    a = outranked_family(repo, b_day="2026-02-01")
    frozen(repo, "0")
    assert run(["--strict", "."], repo).returncode == 0
    before = a.read_bytes()
    fix = run(["--reverify", "--checked", "2026-04-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    assert a.read_bytes() == before, fix.stdout


def test_a_superseded_root_is_left_and_its_correction_re_stamped(repo):
    """S4 (#785). No freeze: R1 drifted, and a `Corrected ·` row citing it,
    whose own coordinate drifted too. `--strict` checks none of R1's
    coordinates, so R1 is left byte for byte; the correcting row's own
    coordinate is re-stamped and dated as before. Red at a3aa139a, which
    re-stamped R1."""
    h0 = at_version(repo, 1)
    o = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    c = fragment(
        repo,
        [
            f"| Corrected · handler adds two | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#other@{o}` | read | 2026-02-01 | Corrected 2026-02-01 |"
        ],
        name=A_ITEM,
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("y = x + 1", "y = x + 2").replace("x * 2", "x * 3"),
        encoding="utf-8",
    )
    before = (repo / R_FILE).read_bytes()
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    assert (repo / R_FILE).read_bytes() == before, fix.stdout
    o2 = unit_hash(repo, "src/service.py", "other")
    after = c.read_text(encoding="utf-8")
    assert f"src/service.py#other@{o2}`" in after and "2026-03-01" in after, after
    assert run(["--strict", "."], repo).returncode == 0


def test_a_family_no_reading_holds_is_re_stamped_as_before(repo):
    """S5, the control (#785). No freeze: R1 at h0 and A at h1, the code at
    h2, so no reading holds. Every member whose hash moves is re-stamped and
    dated, as before. Green at a3aa139a; red with every family member left
    alone."""
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    h1 = at_version(repo, 2)
    a = fragment(repo, [re_read_of(r, h1, "2026-02-01")], name=A_ITEM)
    h2 = at_version(repo, 3)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    for path in (repo / R_FILE, a):
        text = path.read_text(encoding="utf-8")
        assert f"src/service.py#handler@{h2}`" in text, text
        assert "· 2026-03-01 |" in text, text
    assert run(["--strict", "."], repo).returncode == 0


def test_a_held_coordinate_on_a_row_the_run_dates_is_re_stamped_with_it(repo):
    """#785, a row carrying two coordinates. B holds `handler`, and A's
    `other` drifted with no reading holding it. The run re-stamps A's
    `other` and dates A, which makes A the newest reading of every
    coordinate on it, `handler` included: A's `handler` is re-stamped with
    it, because the date says the whole row was read. Left at h1, it would
    outrank B and the family would read DRIFTED. Green at a3aa139a, which
    re-stamped every coordinate; red with a held coordinate always left."""
    o0 = unit_hash(repo, "src/service.py", "other")
    a = outranked_family(repo)
    a.write_text(
        a.read_text(encoding="utf-8").replace(
            "` | read |", f"`, `src/service.py#other@{o0}` | read |", 1
        ),
        encoding="utf-8",
    )
    frozen(repo, "0")
    (repo / "src" / "service.py").write_text(
        (repo / "src" / "service.py")
        .read_text(encoding="utf-8")
        .replace("x * 2", "x * 3"),
        encoding="utf-8",
    )
    fix = run(["--reverify", "--checked", "2026-04-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    h2 = unit_hash(repo, "src/service.py", "handler")
    text = a.read_text(encoding="utf-8")
    assert f"src/service.py#handler@{h2}`" in text, text
    assert "· 2026-04-01 |" in text, text
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


def test_a_superseded_familys_citation_is_still_re_stamped(repo):
    """#785's judgment is about code coordinates: a citation is a ledger
    line no family grades. R1, re-read by A and corrected by C, had its
    Notes edited, so both citations of it read DRIFTED. R1's family is
    superseded, and A's citation is re-stamped all the same, as C's is;
    `--strict` exits 0 after. Red with a citation judged as a code
    coordinate."""
    h0 = at_version(repo, 1)
    o = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    fragment(repo, [re_read_of(r, h0, "2026-02-01")], name=A_ITEM)
    fragment(
        repo,
        [
            f"| Corrected · handler adds one, then other | "
            f"`{citation(r, 'R1 · handler adds one')}`, `src/service.py#other@{o}` "
            "| read | 2026-02-01 | Corrected 2026-02-01 |"
        ],
        name=B_ITEM,
    )
    path = repo / R_FILE
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| 2026-01-01 | |", "| 2026-01-01 | x |"
        ),
        encoding="utf-8",
    )
    assert run(["--strict", "."], repo).returncode == 2
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


TWICE = SERVICE + "\n\ndef handler(x):\n    return x\n"


def test_a_held_coordinate_with_two_places_is_left_alone(repo):
    """#785. `handler` names two places, and B's hash is what one of them
    holds, so the family holds it. A's older hash matches neither place,
    and a re-stamp would leave A BROKEN with a `left` line; a reading the
    family holds is history, so A is left, silently. Red with the
    resolution guard removed."""
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    h1 = at_version(repo, 2)
    a = fragment(repo, [re_read_of(r, h1, "2026-02-01")], name=A_ITEM)
    (repo / "src" / "service.py").write_text(TWICE, encoding="utf-8")
    text = TWICE
    places, _ = ec.resolve_unit("src/service.py", "handler", text)
    assert len(places) == 2, places
    a_, b_ = places[0]
    held = ec.content_hash(ec.gfm_lines(text)[a_ - 1 : b_])
    fragment(repo, [re_read_of(r, held, "2026-03-01")], name=B_ITEM)
    frozen(repo, "0")
    assert run(["--strict", "."], repo).returncode == 0
    before = a.read_bytes()
    fix = run(["--reverify", "--checked", "2026-04-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    assert a.read_bytes() == before, fix.stdout
    assert "src/service.py#handler" not in fix.stdout, fix.stdout


@pytest.mark.parametrize("checked", ["2026-04-01", None], ids=["dated", "undated"])
def test_a_held_coordinate_with_two_places_on_a_dated_row_is_left_and_named(
    repo, capsys, checked
):
    """Round 1, yellow 1: the rider rule meeting the resolution guard. B
    holds `handler` through one of its two places; A carries it at an older
    hash beside `other`, which drifted with no reading holding it. Dated for
    `other`, A becomes the newest reading of `handler`, at a hash neither
    place holds: the run names it `left` and hands MOVES a BROKEN part, as
    for any coordinate no one place holds. Undated, A is not the newest
    reading, and `handler` stays silent. Red at 0667af2e, which was silent
    on the dated row too."""
    o0 = unit_hash(repo, "src/service.py", "other")
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    h1 = at_version(repo, 2)
    a = fragment(
        repo,
        [re_read_of(r, h1, "2026-02-01", extra=f", `src/service.py#other@{o0}`")],
        name=A_ITEM,
    )
    places, _ = ec.resolve_unit("src/service.py", "handler", TWICE)
    x, y = places[0]
    held = ec.content_hash(ec.gfm_lines(TWICE)[x - 1 : y])
    b = fragment(repo, [re_read_of(r, held, "2026-03-01")], name=B_ITEM)
    (repo / "src" / "service.py").write_text(
        TWICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    moves = []
    ec.reverify([str(a), str(b)], str(repo), {}, None, checked, moves)
    out = capsys.readouterr().out
    said = [
        line
        for line in out.splitlines()
        if line.startswith("  src/service.py#handler  ") and line.endswith("left")
    ]
    # The line gives the check's own sentence (round 2; #824).
    assert all(
        "locator is ambiguous — 2 places: " in s
        and "(none holds the recorded content) — left" in s
        for s in said
    ), out
    broken = ("src/service.py#handler", h1, None) in [m[2:] for m in moves]
    assert (len(said), broken) == ((1, True) if checked else (0, False)), (
        out,
        moves,
    )


def test_a_held_coordinate_one_of_whose_places_holds_it_rides_a_dated_row_silently(
    repo, capsys
):
    """Round 2, yellow 1. A records `handler` at what one of its two places
    holds, and carries `other`, which drifted. Dated for `other`, A becomes
    the newest reading of `handler` at content one place holds, which the
    check calls OK: the run says nothing about `handler` and records no
    BROKEN for it, as on a row no family holds. Red at 930078de, which named
    it `left` and handed MOVES a BROKEN part."""
    o0 = unit_hash(repo, "src/service.py", "other")
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    places, _ = ec.resolve_unit("src/service.py", "handler", TWICE)
    x, y = places[0]
    held = ec.content_hash(ec.gfm_lines(TWICE)[x - 1 : y])
    a = fragment(
        repo,
        [re_read_of(r, held, "2026-02-01", extra=f", `src/service.py#other@{o0}`")],
        name=A_ITEM,
    )
    (repo / "src" / "service.py").write_text(
        TWICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    moves = []
    ec.reverify([str(a)], str(repo), {}, None, "2026-04-01", moves)
    out = capsys.readouterr().out
    assert "src/service.py#handler" not in out, out
    assert [m for m in moves if m[2] == "src/service.py#handler"] == [], moves
    assert run(["--strict", "."], repo).returncode == 0


LEFT_BEHIND = (
    "func main() {\n    return handler(1)\n}\n\nfunc other(x) {\n    return x * 2\n}\n"
)


@pytest.mark.parametrize(
    "destination", ["one", "one, renamed", "none"], ids=lambda d: d
)
def test_a_held_coordinate_with_an_unsure_place_on_a_dated_row_heals_to_its_destination(
    repo, capsys, destination
):
    """#808, round 3 of #785's review, yellow 1. B holds `handler` in
    `src/lib.go` through the one place the declaration rule is unsure of, the
    call a move left behind; A records the unit itself, which now lives in
    `src/moved.go`, and carries `other`, which drifted. Dated for `other`, A
    becomes the newest reading of `handler`, and the run reads it as the
    ordinary path reads such a coordinate: it heals A onto the one
    destination that reconstructs A's hash, and `--strict` reads the tree
    clean; with no destination it is left, in the check's own words, with
    its BROKEN part. Where the unit was renamed as it moved, the hash
    follows the name and MOVES gets the move. Red at 0de15c70, which named
    the first two `left` with BROKEN parts, and dropped the last's
    wording."""
    lib, dest = "src/lib.go", "src/moved.go"
    (repo / "src" / "lib.go").write_text(LEFT_BEHIND, encoding="utf-8")
    unit = "func handler(x) {\n    y := x + 2\n    return y\n}\n"
    (repo / "src" / "moved.go").write_text(unit, encoding="utf-8")
    places, unsure = ec.resolve_unit(lib, "handler", LEFT_BEHIND)
    assert unsure and len(places) == 1, places
    x, y = places[0]
    held = ec.content_hash(ec.gfm_lines(LEFT_BEHIND)[x - 1 : y])
    a_at = unit_hash(repo, dest, "handler")
    name = "handler"
    if destination == "none":
        (repo / "src" / "moved.go").unlink()
    elif destination == "one, renamed":
        name = "total"
        (repo / "src" / "moved.go").write_text(
            unit.replace("func handler(", "func total("), encoding="utf-8"
        )
    o0 = unit_hash(repo, lib, "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `{lib}#handler@{line_hash('    return handler(0)')}` "
            "| read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    a = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{lib}#handler@{a_at}`, "
            f"`{lib}#other@{o0}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name=A_ITEM,
    )
    b = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{lib}#handler@{held}` "
            "| read | 2026-03-01 | Re-read 2026-03-01 |"
        ],
        name=B_ITEM,
    )
    (repo / "src" / "lib.go").write_text(
        LEFT_BEHIND.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    moves = []
    ec.reverify([str(a), str(b)], str(repo), {}, None, "2026-04-01", moves)
    out = capsys.readouterr().out
    broken = [m for m in moves if m[2] == f"{lib}#handler" and m[4] is None]
    if destination != "none":
        assert f"{lib}#handler -> {dest}#{name}  (identical content)" in out, out
        assert broken == [], moves
        now = unit_hash(repo, dest, name)
        assert f"`{dest}#{name}@{now}`" in a.read_text(encoding="utf-8")
        moved = [m[3:] for m in moves if m[2] == f"{lib}#handler"]
        assert moved == ([] if now == a_at else [(a_at, now)]), moves
        assert run(["--strict", "."], repo).returncode == 0
    else:
        # The check's own sentence, which names the place and its hash so a
        # person can record it by hand (#824).
        (said,) = [s for s in out.splitlines() if s.startswith(f"  {lib}#handler  ")]
        assert said.startswith(
            f"  {lib}#handler  the declaration rule is unsure of the only place it "
            "found, and none holds the recorded content — "
        ), said
        assert said.endswith("; record one by hand if it is still the unit — left")
        assert len(broken) == 1, moves


THRICE = (
    SERVICE
    + "\n\ndef handler(x):\n    y = x + 1\n    return y * 2\n"
    + "\n\ndef handler(x):\n    y = x + 9\n    return y * 3\n"
)


def test_a_held_claim_two_places_tie_on_a_dated_row_is_left_and_named(repo, capsys):
    """#808, round 3 of #785's review, yellow 2, the dated cell. B holds the
    claim `handler>"y = x"` at the third of three `handler` units; A, older,
    records the line the first two share, and carries `other`, which
    drifted. Dated for `other`, A becomes the newest reading, and two places
    holding a claim's minor hash is a tie the check calls BROKEN: the run
    names it `left` in the check's terms and hands MOVES the BROKEN part.
    Red at 0de15c70, which read the tie as unchanged and said nothing."""
    claim = 'src/service.py#handler>"y = x"'
    places, _ = ec.resolve_unit("src/service.py", "handler", THRICE)
    assert len(places) == 3, places

    def minor(n):
        (inside,) = ec.minor_region("src/service.py", THRICE, places[n], '"y = x"')
        return ec.content_hash(ec.gfm_lines(THRICE)[inside[0] - 1 : inside[1]])

    o0 = unit_hash(repo, "src/service.py", "other")
    h0 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    a = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{claim}@{minor(0)}`, "
            f"`src/service.py#other@{o0}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name=A_ITEM,
    )
    b = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{claim}@{minor(2)}` "
            "| read | 2026-03-01 | Re-read 2026-03-01 |"
        ],
        name=B_ITEM,
    )
    (repo / "src" / "service.py").write_text(
        THRICE.replace("x * 2\n", "x * 3\n", 1), encoding="utf-8"
    )
    moves = []
    ec.reverify([str(a), str(b)], str(repo), {}, None, "2026-04-01", moves)
    out = capsys.readouterr().out
    (said,) = [s for s in out.splitlines() if s.startswith(f"  {claim}  ")]
    assert said.startswith(f"  {claim}  locator is ambiguous — 3 places: "), said
    assert said.endswith(
        "(2 hold the recorded content, a tie it cannot break) — left"
    ), said
    assert (claim, minor(0), None) in [m[2:] for m in moves], moves


def test_a_held_ledger_coordinate_the_run_moves_is_re_stamped(repo):
    """Round 1, yellow 2. #785's judgment is made before the walk, on the
    premise that a walk moves no code. A coordinate naming a line of a ledger
    the run writes is the exception: Q and B both name R1's line, B newer and
    holding it, and the run re-stamps R1 in place, which moves that line. Q
    and B are re-stamped with it, as before #785, and `--strict` reads the
    tree clean. Red at 0667af2e, which left both at the stale hash."""
    h = unit_hash(repo, "src/service.py", "handler")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
    released(repo, [r1])
    lc = citation(r1, "R1 · handler adds one")
    second = "### 1000000002-the-second-item"
    q = f"| Q · beside R1 | `{lc}` | read | 2026-01-01 | |"
    released(repo, [q], version="0.2.0", section=second)
    cq = citation(q, "Q · beside R1", version="0.2.0", section=second)
    fragment(
        repo,
        [
            f"| Re-read · Q · beside R1 | `{cq}`, `{lc}` | read | 2026-02-01 | "
            "Re-read 2026-02-01 |"
        ],
        name=B_ITEM,
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


@pytest.mark.parametrize(
    "where, sentence",
    [
        (
            "docs/the-evidence-ledger.md",
            "No such reading is owed where the family already holds a coordinate, "
            "or where a `Corrected ·` row supersedes the family, so an in-place "
            "re-stamp leaves that coordinate's hash and date as they are (#785).",
        ),
        (
            "docs/the-evidence-ledger.md",
            "On a row it dates for another coordinate it moves a held one's hash "
            "too, since that date makes the row its newest reading.",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "**Where no re-read is owed, the hash and the date stay** (#785).",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "A row the run dates for another coordinate takes a held one's new "
            "hash too, because its date makes it that coordinate's newest reading.",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "A reading whose family's newest reading holds the code, and a "
            "superseded family's, stay as they are",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "**A coordinate its family already holds, or that a superseded family "
            "carries, stays where it stands** (#785, `left_alone`).",
        ),
    ],
    ids=[
        "the home: no re-read owed",
        "the home: a dated row",
        "the skill: the hash and the date stay",
        "the skill: a dated row",
        "the usage text",
        "reverify's docstring",
    ],
)
def test_the_documents_say_a_held_reading_is_left_alone(where, sentence):
    """§14 for #785: every place that says what an in-place `--reverify`
    rewrites says which readings it leaves, sentence by sentence."""
    with open(os.path.join(ROOT, where), encoding="utf-8") as handle:
        text = " ".join(handle.read().split())
    assert sentence in text, sentence


# --- each coordinate's outcome is printed once (#792) ------------------------


@pytest.mark.parametrize("last", ["unchanged", "moved"])
def test_a_left_line_a_later_walk_takes_back_is_not_printed(repo, last):
    """S9 (#792's comment), `left_then_unchanged`'s tree through `main`.
    Against the text the run writes X1 reads unchanged, or is re-stamped
    where its hash was stale, so no line says X1 is left, and `--strict`
    reads it clean. Red at a3aa139a, which printed the first walk's `the
    anchored statement is gone … left` and nothing after it."""
    before = left_then_unchanged(repo, stale=last == "moved")
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    if last == "unchanged":
        assert (repo / R_FILE).read_text(encoding="utf-8") == before
    else:
        assert "0000beef -> " in fix.stdout, fix.stdout
    assert "— left" not in fix.stdout and "; left" not in fix.stdout, fix.stdout
    assert run(["--strict", "."], repo).returncode == 0


def a_correction_whose_statement_is_gone(repo):
    """A10's tree, folded: a `Corrected ·` row in `seal/releases/0.2.0.md`
    roots its own family, and its one coordinate names a statement `other`
    no longer has. Returns the file it sits in."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    text = (repo / "src" / "service.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/service.py", "other", text)
    (inside,) = ec.minor_region("src/service.py", text, places[0], '"x * 2"')
    stated = ec.content_hash(ec.gfm_lines(text)[inside[0] - 1 : inside[1]])
    where = placed(
        repo,
        f"| Corrected · other doubles | `{citation(r, 'R1 · handler adds one')}`, "
        f'`src/service.py#other>"x * 2"@{stated}` | read | 2026-02-01 | '
        "Corrected 2026-02-01 by work item 2000000001 |",
        "folded",
        "0.2.0",
        "2000000001-c",
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    return where


@pytest.mark.parametrize(
    "tree, narrowed",
    [
        ("a move, then left", False),
        ("a correction whose statement is gone", False),
        ("a correction whose statement is gone", True),
    ],
    ids=[
        "S10: a move then left, every ledger",
        "S10: A10 folded, every ledger",
        "S12: A10 folded, narrowed to its file",
    ],
)
def test_a_coordinate_the_run_left_itself_names_no_ledger_remedy(repo, tree, narrowed):
    """S10 and S12 (#792). The run leaves a coordinate itself, on a row in a
    file it writes, and no reading outside the run is newer: the family
    `LEFT` line names the coordinate and says the run left it, and names no
    `--ledger` remedy, which could not clear it. The line naming why it was
    left is printed once, and the exit stays 1. Red at a3aa139a, which told
    the person to run it without `--ledger`."""
    if tree == "a move, then left":
        line = moved_then_left(repo)
        coord, where = line.rsplit("@", 1)[0], f"{R_FILE}:10"
        flags = []
    else:
        file = a_correction_whose_statement_is_gone(repo)
        coord, where = 'src/service.py#other>"x * 2"', f"{file}:5"
        flags = ["--ledger", file] if narrowed else []
    fix = run(["--reverify", "--checked", "2026-03-01", *flags, "."], repo)
    assert fix.returncode == 1, fix.stdout
    family = [
        line for line in fix.stdout.splitlines() if line.startswith(f"  LEFT  {where}")
    ]
    assert len(family) == 1, fix.stdout
    assert f"this run left {coord} where it stands" in family[0], family[0]
    assert "--ledger" not in family[0], family[0]
    said = [
        line
        for line in fix.stdout.splitlines()
        if line.startswith(f"  {coord}  ") and line.endswith("left")
    ]
    assert len(said) == 1, fix.stdout


def test_a_family_no_remedy_clears_is_named_without_one(repo):
    """Questions Q3, the measured shape: the family's newest reading sits in
    a ledger the run walks and cannot read strictly, so neither reason
    holds. The family `LEFT` line names the coordinate and says it is still
    DRIFTED, and names no remedy it cannot support; the `ledger unreadable`
    line beside it names the file. Red at a3aa139a, which named the
    `--ledger` remedy."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    bad = repo / "seal" / "ledger" / f"{A_ITEM}.md"
    bad.parent.mkdir(parents=True)
    bad.write_bytes(
        (re_read_of(r, h, "2026-02-01") + "\n")
        .encode("utf-8")
        .replace(b"| read |", b"| caf\xe9 |")
    )
    edit_handler(repo)
    fix = run(["--reverify", "."], repo)
    assert fix.returncode == 1, fix.stdout
    assert f"  LEFT  seal/ledger/{A_ITEM}.md  ledger unreadable" in fix.stdout
    family = [line for line in fix.stdout.splitlines() if "still DRIFTED" in line]
    assert len(family) == 1, fix.stdout
    assert "src/service.py#handler" in family[0], family[0]
    assert "--ledger" not in family[0] and "this run left" not in family[0], family[0]


@pytest.mark.parametrize(
    "where, sentence",
    [
        (
            "docs/the-evidence-ledger.md",
            "The line names a remedy per coordinate, by why the family is still "
            "owed one (#792).",
        ),
        (
            "docs/the-evidence-ledger.md",
            "Only where a newest reading of it sits in a file the run did not "
            "write does it say to run without `--ledger`.",
        ),
        (
            "docs/the-evidence-ledger.md",
            "Where the run left the coordinate itself, on a `left` line or by "
            "leaving its row whole for want of a date cell, the line says so and "
            "points at the line naming why, and a run over every ledger names "
            "such a family too.",
        ),
        (
            "docs/the-evidence-ledger.md",
            "A `left` line names why: a path outside the repository or any known "
            "checkout, a file the run could not read, no one place holding the "
            "unit, or a quoted statement its file no longer has.",
        ),
        ("docs/the-evidence-ledger.md", "Where neither is found it names no remedy."),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "**Every `left` line carries the check's own sentence**, so the two "
            "commands cannot describe one row two ways (#809).",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "**Every coordinate is judged once, by `judge`, against the text the "
            "run writes** (#824).",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "Each round judges against the round before it, never against a plan "
            "being edited file by file, so what the run writes and prints is a "
            "function of the tree and not of the order LEDGERS names the files in.",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "**A coordinate that does not settle is left at the hash its row "
            "recorded**",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "Nothing is written for a coordinate the run leaves, so there is no "
            "hash between the two to record.",
        ),
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "A row naming a ledger line the run writes is read against the line "
            "the run writes, so one run settles it; one that never settles is "
            "left, named, and exits 1",
        ),
    ],
    ids=[
        "the home: per coordinate",
        "the home: --ledger only outside",
        "the home: left by the run",
        "the home: every left reason",
        "the home: neither",
        "reverify's docstring: the check's sentence",
        "reverify's docstring: judged once",
        "reverify's docstring: no order",
        "reverify's docstring: a coordinate that does not settle",
        "reverify's docstring: before and after",
        "the usage text: one run settles a ledger line",
    ],
)
def test_the_documents_say_each_outcome_is_printed_once(where, sentence):
    """§14 for #792: the paragraph a person reads beside a family `LEFT`
    line, and the docstring a contributor adding a `left` reason reads."""
    with open(os.path.join(ROOT, where), encoding="utf-8") as handle:
        text = " ".join(handle.read().split())
    assert sentence in text, sentence


def test_reverifys_docstring_no_longer_says_a_later_walk_is_silent():
    """#792's comment: `a walk after the first names nothing the first one
    named` described the defect. Red at a3aa139a."""
    assert "names nothing the first one named" not in " ".join(
        ec.reverify.__doc__.split()
    )


def test_a_row_left_whole_for_want_of_a_date_cell_is_named_as_left_by_the_run(
    repo,
):
    """#792, reason (ii)'s second shape. A released row outside every family
    sits in a table with no date column, so `--checked` leaves it whole and
    it stays DRIFTED. The family `LEFT` line says the run left it, beside the
    line naming why, and names no `--ledger` remedy. Red at a3aa139a."""
    h = unit_hash(repo, "src/service.py", "handler")
    (repo / "seal" / "releases").mkdir(parents=True)
    (repo / R_FILE).write_text(
        f"## 0.1.0 — 2026-01-01\n\n{SECTION}\n\n"
        "| Clause | Code grounds | Verified behavior | Notes |\n|---|---|---|---|\n"
        f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | |\n",
        encoding="utf-8",
    )
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 1, fix.stdout
    assert f"  LEFT  {R_FILE}:7  its hash moved and the row has no date cell" in (
        fix.stdout
    )
    family = [line for line in fix.stdout.splitlines() if "still DRIFTED" in line]
    assert len(family) == 1, fix.stdout
    assert "this run left src/service.py#handler where it stands" in family[0]
    assert "--ledger" not in family[0], family[0]


def test_an_older_reading_outside_the_narrowing_names_no_ledger_remedy(repo):
    """#792, reason (i) is about the newest readings. A10's folded
    correction is the newest reading of its coordinate, and the run leaves
    it; an older `Re-read ·` of it sits in a fragment the narrowing left
    out. A run without `--ledger` would re-stamp that older one and clear
    nothing, so the line names only the run's own leaving. Red with every
    reading counted, not only the newest."""
    file = a_correction_whose_statement_is_gone(repo)
    text = (repo / file).read_text(encoding="utf-8")
    row = text.splitlines()[4]
    cite = ec.citation_for(str(repo), str(repo / file), 5)
    stated = row.split('"x * 2"@', 1)[1].split("`", 1)[0]
    fragment(
        repo,
        [
            f"| Re-read · other doubles | `{cite}`, "
            f'`src/service.py#other>"x * 2"@{stated}` | read | 2026-01-15 | '
            "Re-read 2026-01-15 |"
        ],
        name=B_ITEM,
    )
    fix = run(["--reverify", "--checked", "2026-03-01", "--ledger", file, "."], repo)
    assert fix.returncode == 1, fix.stdout
    family = [line for line in fix.stdout.splitlines() if "still DRIFTED" in line]
    assert len(family) == 1 and family[0].startswith(f"  LEFT  {file}:5"), fix.stdout
    assert "this run left" in family[0] and "--ledger" not in family[0], family[0]


# --- one judge for every command (#824, closing #809) ------------------------
#
# `judge` is the one reading of a coordinate: `--strict` prints its finding,
# `--reverify` acts on it, and `--into` writes its hash. A claim on a place the
# declaration rule is unsure of is what the readings disagreed about (#809).

UNSURE_CS = "public new void Render(int x) {\n    var a = x + 2;\n}\n"
UNSURE_CLAIM = 'src/a.cs#Render>"var a"'


def unsure_claim(repo, body=UNSURE_CS):
    """Write `src/a.cs` holding BODY, whose `Render` the declaration rule is
    unsure of (`new` is a statement word elsewhere), and return the hash of
    the statement `UNSURE_CLAIM` quotes, as the check hashes it."""
    (repo / "src" / "a.cs").write_text(body, encoding="utf-8")
    places, unsure = ec.resolve_unit("src/a.cs", "Render", body)
    assert unsure and len(places) == 1, places
    (inside,) = ec.minor_region("src/a.cs", body, places[0], '"var a"')
    return ec.content_hash(ec.gfm_lines(body)[inside[0] - 1 : inside[1]])


def test_into_re_reads_a_claim_on_an_unsure_place_at_its_statement(repo):
    """S3a, the `--into` arm (#809, cell C8). `--strict` calls a stale claim
    on a place the declaration rule is unsure of DRIFTED; `--into` writes a
    `Re-read ·` row carrying the statement's hash, and the tree reads clean.
    Red at e6d5a055, which left the row with *no one place to hash*."""
    now = unsure_claim(repo)
    released(
        repo,
        [f"| R1 · render adds two | `{UNSURE_CLAIM}@0000beef` | read | 2026-01-01 | |"],
    )
    frozen(repo, "0")
    check = run(["--strict", "."], repo)
    assert f"DRIFTED  {UNSURE_CLAIM}  content changed" in check.stdout, check.stdout
    assert "BROKEN" not in check.stdout, check.stdout
    fix = run(["--reverify", "--into", INTO, "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    assert f"`{UNSURE_CLAIM}@{now}`" in (repo / INTO).read_text(encoding="utf-8")
    assert "no one place to hash" not in fix.stdout, fix.stdout
    assert run(["--strict", "."], repo).returncode == 0


def the_checks_detail(out, coord):
    """What `--strict` said about COORD, after the coordinate: the sentence
    every `left` line of `--reverify` now carries."""
    said = [line for line in out.splitlines() if f" {coord}  " in line]
    assert len(said) == 1, out
    return said[0].split(f" {coord}  ", 1)[1]


def test_reverify_restamps_a_claim_on_an_unsure_place_at_its_statement(repo, capsys):
    """S3a in place (#809, cell C8). The check calls the claim DRIFTED, and
    `--reverify` re-stamps it at its statement's hash and hands MOVES the
    move; nothing records BROKEN. Red at e6d5a055, which left the row as
    *only a place the declaration rule is unsure of*."""
    now = unsure_claim(repo)
    f = fragment(
        repo,
        [f"| F1 · render adds two | `{UNSURE_CLAIM}@0000beef` | read | 2026-01-01 | |"],
    )
    moves = []
    ec.reverify([str(f)], str(repo), {}, None, "2026-03-01", moves)
    out = capsys.readouterr().out
    assert f"`{UNSURE_CLAIM}@{now}`" in f.read_text(encoding="utf-8"), out
    assert [m[2:] for m in moves] == [(UNSURE_CLAIM, "0000beef", now)], moves
    assert "left" not in out, out
    assert run(["--strict", "."], repo).returncode == 0


THREE_UNSURE = (
    "public new void Render(int x) {\n    var a = x + 1;\n}\n\n"
    "public new void Render(string s) {\n    var a = x + 1;\n}\n\n"
    "public new void Render(long n) {\n    var a = n + 9;\n}\n"
)


@pytest.mark.parametrize("holding", ["two hold it", "none holds it"])
def test_reverify_names_a_tie_among_unsure_places_as_the_check_does(
    repo, capsys, holding
):
    """S3b (#809's comment, cells CU and CU0). A claim over three places the
    declaration rule is unsure of, two holding its recorded content or none:
    the check calls it BROKEN, ambiguous, and `--reverify`'s `left` line is
    the check's sentence followed by ` — left`; MOVES gets the BROKEN part.
    Red at e6d5a055, which said *only a place the declaration rule is unsure
    of*."""
    (repo / "src" / "a.cs").write_text(THREE_UNSURE, encoding="utf-8")
    places, unsure = ec.resolve_unit("src/a.cs", "Render", THREE_UNSURE)
    assert unsure and len(places) == 3, places
    recorded = (
        line_hash("    var a = x + 1;") if holding == "two hold it" else "0000beef"
    )
    f = fragment(
        repo,
        [f"| F1 · render adds | `{UNSURE_CLAIM}@{recorded}` | read | 2026-01-01 | |"],
    )
    check = run(["--strict", "."], repo)
    detail = the_checks_detail(check.stdout, UNSURE_CLAIM)
    assert detail.startswith("locator is ambiguous — 3 places: "), detail
    held = "2 hold the recorded content" if recorded != "0000beef" else "none holds"
    assert held in detail, detail
    moves = []
    ec.reverify([str(f)], str(repo), {}, None, "2026-03-01", moves)
    out = capsys.readouterr().out
    assert f"  {UNSURE_CLAIM}  {detail} — left" in out.splitlines(), out
    assert [m[2:] for m in moves] == [(UNSURE_CLAIM, recorded, None)], moves


def test_reverify_leaves_a_claim_whose_statement_is_gone_in_the_checks_words(
    repo, capsys
):
    """S3c. S3a's row with the quoted statement deleted: the check says
    DRIFTED, *the anchored statement is gone*, and `--reverify` leaves the
    row with that sentence and hands MOVES the BROKEN part, the pact's word
    for *left by the re-read*. Green at e6d5a055 for the verdicts, red for
    the words."""
    body = "public new void Render(int x) {\n    return;\n}\n"
    (repo / "src" / "a.cs").write_text(body, encoding="utf-8")
    assert ec.resolve_unit("src/a.cs", "Render", body)[1]
    f = fragment(
        repo,
        [f"| F1 · render adds two | `{UNSURE_CLAIM}@0000beef` | read | 2026-01-01 | |"],
    )
    check = run(["--strict", "."], repo)
    detail = the_checks_detail(check.stdout, UNSURE_CLAIM)
    assert detail.startswith("the anchored statement is gone from Render"), detail
    moves = []
    ec.reverify([str(f)], str(repo), {}, None, "2026-03-01", moves)
    out = capsys.readouterr().out
    assert f"  {UNSURE_CLAIM}  {detail} — left" in out.splitlines(), out
    assert [m[2:] for m in moves] == [(UNSURE_CLAIM, "0000beef", None)], moves


# --- every coordinate judged once, one write (#824, closing #806) ------------

B_FILE = "seal/ledger/1000000003-b.md"
Q_FILE = "seal/releases/0.2.0.md"
Q_SECTION = "### 1000000002-the-second-item"


def names_a_released_line(repo):
    """#806's probe p10, no freeze. Fragment B re-reads R1 and also names,
    by a quoted line, row Q of `seal/releases/0.2.0.md`; `handler` and
    `other` both change. B's file sorts before Q's. Returns B's coordinate of
    Q's line, without its hash."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    (q,) = released(
        repo,
        [f"| Q · other doubles | `src/service.py#other@{o}` | read | 2026-01-01 | |"],
        version="0.2.0",
        section=Q_SECTION,
    )
    names_q = citation(q, "Q · other doubles", version="0.2.0", section=Q_SECTION)
    (repo / B_FILE).parent.mkdir(parents=True, exist_ok=True)
    (repo / B_FILE).write_text(
        f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
        f"`src/service.py#handler@{h}`, `{names_q}` | read | 2026-02-01 | "
        "Re-read 2026-02-01 |\n",
        encoding="utf-8",
    )
    assert run(["--strict", "."], repo).returncode == 0
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("y = x + 1", "y = x + 2").replace("x * 2", "x * 3"),
        encoding="utf-8",
    )
    return names_q.rsplit("@", 1)[0]


def test_one_run_restamps_a_coordinate_naming_a_line_it_moves(repo):
    """S2, #806's probe p10. One run over every ledger re-stamps Q, which
    moves the line B names, and judges B's coordinate against the line the
    run writes: exit 0, `--strict` exits 0, and a second run writes nothing.
    Red at e6d5a055, which walked B before Q's file and left B DRIFTED until
    a second run."""
    names_a_released_line(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout
    before = ledger_texts(repo)
    again = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert again.returncode == 0, again.stdout
    assert ledger_texts(repo) == before, again.stdout


def test_a_narrowed_run_names_a_coordinate_of_a_line_it_moved_and_left(repo):
    """S9, spec D4. Narrowed to Q's file, the run re-stamps Q's line, and B,
    in a file the narrowing left out, names that line by a coordinate that is
    not its citation. The run names B's row and that coordinate on a `LEFT`
    line with the `--ledger` remedy, and exits 1. Red at e6d5a055, which
    named citations alone and exited 0."""
    coord = names_a_released_line(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "--ledger", Q_FILE, "."], repo)
    assert fix.returncode == 1, fix.stdout
    left = [line for line in fix.stdout.splitlines() if line.startswith("  LEFT")]
    assert left == [
        f"  LEFT  {B_FILE}:1  Re-read · R1 · handler adds one — its coordinate "
        f"{coord} is DRIFTED: this run re-stamps the line it names, and the "
        "narrowing left this row's file out; run it without `--ledger`"
    ], fix.stdout


SELF = '"X · quotes itself"'


def test_a_row_that_never_settles_is_named_and_left_at_its_hash(repo):
    """S6. A released row's Code grounds quote its own line, hash included,
    so every re-stamp moves the line it names. The run leaves that
    coordinate at the hash the row recorded, names it on a `LEFT` line that
    says it does not settle, and exits 1; the file's other row is
    re-stamped. Red at e6d5a055, which re-stamped it once, said nothing, and
    exited 0 over a row `--strict` refuses."""
    h = unit_hash(repo, "src/service.py", "handler")
    coord = f'{R_FILE}#"{SECTION}">{SELF}'
    released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |",
            f"| X · quotes itself | `{coord}@0000beef` | read | 2026-01-01 | |",
        ],
    )
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 1, fix.stdout
    text = (repo / R_FILE).read_text(encoding="utf-8")
    assert f"`{coord}@0000beef`" in text, text
    assert (
        f"src/service.py#handler@{unit_hash(repo, 'src/service.py', 'handler')}`"
        in (text)
    )
    left = [line for line in fix.stdout.splitlines() if line.startswith("  LEFT")]
    named = [line for line in left if "does not settle" in line]
    assert len(named) == 1 and named[0].startswith(f"  LEFT  {R_FILE}:6  "), left
    assert f" — {coord} does not settle" in named[0], named


def test_a_row_naming_one_that_never_settles_is_restamped(repo):
    """S6's other side. X quotes its own line and also carries `handler`, so
    the run moves X's line once, by that hash and its date, and Y names X's
    line. Only X's own quotation is on a cycle: it is left and named, and
    Y, downstream of it, is re-stamped against the line the run writes and
    named nowhere. Red with every coordinate still moving at the bound left,
    cycle or not (`on_a_cycle` answering nothing)."""
    h = unit_hash(repo, "src/service.py", "handler")
    x_coord = f'{R_FILE}#"{SECTION}">{SELF}'
    x = (
        f"| X · quotes itself | `src/service.py#handler@{h}`, `{x_coord}@0000beef` "
        "| read | 2026-01-01 | |"
    )
    # A literal opening with the row's leading pipe names the line that
    # begins with it, never Y's own copy of the literal.
    y_coord = f'{R_FILE}#"{SECTION}">"\\| X · quotes"'
    released(
        repo,
        [x, f"| Y · names X | `{y_coord}@{line_hash(x)}` | read | 2026-01-01 | |"],
    )
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 1, fix.stdout
    lines = (repo / R_FILE).read_text(encoding="utf-8").splitlines()
    assert f"`{x_coord}@0000beef`" in lines[4], lines
    assert f"`{y_coord}@{line_hash(lines[4])}`" in lines[5], (lines, fix.stdout)
    named = [line for line in fix.stdout.splitlines() if "does not settle" in line]
    assert len(named) == 1 and x_coord in named[0], fix.stdout
    assert y_coord not in "\n".join(named), fix.stdout


def test_of_two_rows_quoting_each_other_only_the_one_still_moved_is_named(repo):
    """S6, a cycle of two. A quotes B's line and carries `handler`; B quotes
    A's line. Every re-stamp of either moves the other, so both are left at
    the bound. Left there, A's line moves once, by `handler` and its date,
    and B's not at all: A's quotation of B still holds, and is named
    nowhere, while B's of A does not, and is named. Red with every
    coordinate left on a cycle named, whatever it reads at the end."""
    h = unit_hash(repo, "src/service.py", "handler")
    a_names_b = f'{R_FILE}#"{SECTION}">"\\| B · quotes"'
    b_names_a = f'{R_FILE}#"{SECTION}">"\\| A · quotes"'
    b = f"| B · quotes A | `{b_names_a}@0000beef` | read | 2026-01-01 | |"
    a = (
        f"| A · quotes B | `src/service.py#handler@{h}`, "
        f"`{a_names_b}@{line_hash(b)}` | read | 2026-01-01 | |"
    )
    released(repo, [a, b])
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 1, fix.stdout
    lines = (repo / R_FILE).read_text(encoding="utf-8").splitlines()
    assert lines[5] == b, lines
    named = [line for line in fix.stdout.splitlines() if "does not settle" in line]
    assert len(named) == 1 and b_names_a in named[0], fix.stdout


def test_a_re_point_is_judged_against_the_section_the_run_writes(repo):
    """A row names a section of `seal/releases/0.2.0.md` that moved, intact,
    to `seal/releases/0.3.0.md`, and the run re-stamps a row of that section.
    Against the tree on disk the moved section reconstructs the row's hash,
    a destination; against the text the run writes it does not, so the row
    is left with the check's sentence and is not re-pointed onto content no
    longer identical. Red with a BROKEN verdict kept from the first round
    the way an unchanged file's is."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    moved = "### 2000000009-moved"
    released(
        repo,
        [f"| P · other doubles | `src/service.py#other@{o}` | read | 2026-01-01 | |"],
        version="0.2.0",
        section="### 2000000008-stays",
    )
    released(
        repo,
        [
            f"| M · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
        version="0.3.0",
        section=moved,
    )
    text = (repo / "seal/releases/0.3.0.md").read_text(encoding="utf-8")
    (place,) = ec.resolve_unit("seal/releases/0.3.0.md", f'"{moved}"', text)[0]
    section = ec.content_hash(ec.gfm_lines(text)[place[0] - 1 : place[1]])
    coord = f'seal/releases/0.2.0.md#"{moved}"'
    f = fragment(
        repo, [f"| F · names a section | `{coord}@{section}` | read | 2026-01-01 | |"]
    )
    before = f.read_text(encoding="utf-8")
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert f.read_text(encoding="utf-8") == before, fix.stdout
    (said,) = [s for s in fix.stdout.splitlines() if s.startswith(f"  {coord}  ")]
    assert said.endswith(" — left"), said
    assert "same name at seal/releases/0.3.0.md (content differs)" in said, said


def six_files(repo):
    """The tree of the walk-order case #824 removed: a release file citing a
    row of itself, two release files citing each other, a release file no
    citation names, and two fragments citing released rows. `handler` then
    changes. Returns the six paths, fragments first."""
    h = unit_hash(repo, "src/service.py", "handler")

    def r(n):
        return (
            f"| R{n} · handler adds one | `src/service.py#handler@{h}` | read "
            "| 2026-01-01 | |"
        )

    def reread(cite):
        return (
            f"| Re-read · the row it cites | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    def at(version):
        return str(repo / f"seal/releases/{version}.md")

    released(repo, [r(1), reread(citation(r(1), "R1 · handler adds one"))])
    to_1 = ec.citation_for(str(repo), at("0.1.0"), 5)
    released(repo, [r(1), reread(to_1)])
    released(repo, [r(1)], version="0.2.0")
    released(repo, [r(2)], version="0.3.0")
    released(repo, [r(1)], version="0.4.0")
    to_2 = ec.citation_for(str(repo), at("0.2.0"), 5)
    to_3 = ec.citation_for(str(repo), at("0.3.0"), 5)
    to_4 = ec.citation_for(str(repo), at("0.4.0"), 5)
    released(repo, [r(2), reread(to_4)], version="0.3.0")
    released(repo, [r(1), reread(to_3)], version="0.4.0")
    fragment(repo, [reread(to_1)], name=M_ITEM)
    fragment(repo, [reread(to_2)], name="2000000003-n")
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    return [
        f"seal/ledger/{M_ITEM}.md",
        "seal/ledger/2000000003-n.md",
        *(f"seal/releases/0.{n}.0.md" for n in range(1, 5)),
    ]


def test_one_run_settles_a_self_citation_and_a_cycle(repo):
    """S5. Over `six_files`' tree one unnarrowed run exits 0 and `--strict`
    exits 0 after it: every citation of a line the run writes is judged
    against that line, the self-citing file and the cycle included."""
    six_files(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout


def build_tree(repo, tree):
    """Build TREE in REPO and return the ledger paths in their file order."""
    if tree == "p10":
        names_a_released_line(repo)
        return [B_FILE, R_FILE, Q_FILE]
    return six_files(repo)


def orderings(paths):
    """Every permutation of three paths, and a dozen of six chosen without a
    random seed: the identity, its reverse, and ten rotations and swaps."""
    if len(paths) <= 3:
        return [list(p) for p in itertools.permutations(paths)]
    picked = [list(paths), list(reversed(paths))]
    for k in range(1, 6):
        picked.append(paths[k:] + paths[:k])
    for i, j in ((0, 5), (1, 4), (2, 3), (0, 2), (3, 5)):
        swapped = list(paths)
        swapped[i], swapped[j] = swapped[j], swapped[i]
        picked.append(swapped)
    return picked


def by_file(out):
    """The run's lines, grouped by the file each names, so two runs compare
    up to the order of lines about different files."""
    return sorted(out.splitlines())


@pytest.mark.parametrize("tree", ["p10", "six files"])
def test_the_run_writes_the_same_bytes_in_any_ledger_order(tmp_path, tree):
    """S4. The result is a function of the tree, never of the order the
    ledgers are named in: any permutation of `--ledger` arguments writes the
    same bytes to every file and prints the same lines. Red under the
    mutation *judge ledger coordinates against the disk*."""

    def fresh(name):
        repo = tmp_path / name
        (repo / "src").mkdir(parents=True)
        (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
        (repo / "seal").mkdir()
        return repo

    seen = None
    for n, order in enumerate(orderings(build_tree(fresh("paths"), tree))):
        repo = fresh(f"run{n}")
        build_tree(repo, tree)
        args = ["--reverify", "--checked", "2026-03-01"]
        for path in order:
            args += ["--ledger", path]
        fix = run([*args, "."], repo)
        result = (fix.returncode, ledger_texts(repo), by_file(fix.stdout))
        if seen is None:
            seen = result
        assert result == seen, (order, fix.stdout)
        assert run(["--strict", "."], repo).returncode == 0, order


def ledger_coordinate_on_a_moving_line(repo):
    """#791's tree. X1 is not a citing row, and names among its Code grounds
    the `Re-read ·` row of its own self-citing release file, whose code hash,
    date and citation the run all move. Returns X1's coordinate as
    written."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"

    def reread(cite):
        return (
            f"| Re-read · the row it cites | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    released(repo, [r1, reread(citation(r1, "R1 · handler adds one"))])
    cite = ec.citation_for(str(repo), str(repo / R_FILE), 5)
    line = citation(reread(cite), "Re-read · the row it cites \\|")
    released(
        repo,
        [
            r1,
            reread(cite),
            f"| X1 · other, beside the re-read | `src/service.py#other@{o}`, "
            f"`{line}` | read | 2026-01-01 | |",
        ],
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    return line


def parts_of(path):
    """`{(row, coordinate, nth): hash}` for every non-citation coordinate of
    the ledger at PATH, read as `reverify` reads it."""
    text = path.read_text(encoding="utf-8")
    lines = ec.gfm_lines(text)
    rows = {n: (h, c) for n, h, c in ec.ledger_table_rows(text)}
    found, nth = {}, {}
    for number, line in enumerate(lines, 1):
        cite = None
        if number in rows:
            cite = ec.row_citation(line, *rows[number])
        for m in ec.ANCHOR_RE.finditer(line):
            if cite is not None and m.span() == cite.span():
                continue
            spot = (number, ec.coordinate_of(m))
            nth[spot] = nth.get(spot, 0) + 1
            found[(*spot, nth[spot])] = m.group("hash")
    return found


S7_TREES = {
    "a move, then left": lambda repo: moved_then_left(repo),
    "left, then unchanged": lambda repo: left_then_unchanged(repo),
    "left, then re-stamped": lambda repo: left_then_unchanged(repo, stale=True),
    "a ledger coordinate on a moving line": ledger_coordinate_on_a_moving_line,
    "R and M": unfrozen_r_and_m,
    "p10": names_a_released_line,
}


@pytest.mark.parametrize("tree", list(S7_TREES))
def test_the_record_and_the_lines_are_what_the_file_holds(repo, capsys, tree):
    """S7. After the run, each MOVES part's new hash is the hash the file
    holds at that coordinate, or None where the line still holds the
    recorded hash and a `left` line names it; every non-citation coordinate
    whose hash the run moved has its part; and each printed `a -> b` has `b`
    in the file. Red under the mutation *record the first recomputation's
    hash*."""
    S7_TREES[tree](repo)
    paths = sorted((repo / "seal").rglob("*.md"))
    paths = [p for p in paths if p.name != "config.md"]
    before = {p: parts_of(p) for p in paths}
    moves = []
    ec.reverify([str(p) for p in paths], str(repo), {}, None, "2026-03-01", moves)
    out = capsys.readouterr().out
    after = {p: parts_of(p) for p in paths}
    texts = "".join(p.read_text(encoding="utf-8") for p in paths)
    for ledger, number, coord, old, new in moves:
        line = ec.gfm_lines(open(ledger, encoding="utf-8").read())[number - 1]
        if new is None:
            assert f"{coord}@{old}" in line, (coord, line)
            assert any(
                said.startswith(f"  {coord}  ")
                or (said.startswith("  LEFT") and coord in said)
                for said in out.splitlines()
            ), out
        else:
            assert f"{coord}@{new}" in line, (coord, new, line, moves)
    recorded = {(os.path.abspath(m[0]), m[1], m[2], m[3], m[4]) for m in moves}
    for path in paths:
        for (number, coord, _nth), was in before[path].items():
            now = after[path].get((number, coord, _nth))
            if now is not None and now != was:
                assert (str(path), number, coord, was, now) in recorded, (
                    path,
                    number,
                    coord,
                    moves,
                )
    for said in out.splitlines():
        m = HASH_LINE.match(said)
        if m:
            assert f"@{m.group(3)}`" in texts, (said, out)
