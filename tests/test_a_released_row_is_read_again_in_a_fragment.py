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

  S1  a coordinate is OK when any reading in R's family recorded what it holds
  S2  a re-read is per row: it vouches for the row it cites and no other
  S3  a `Corrected ·` row supersedes R; its own coordinates are what is checked
  S4  a citation that does not hold is named, never skipped

`seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-
never-changes/spec.md` D2 and D3 are the decisions these cases hold.
"""

import importlib.util
import os
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
    text = (repo / rel).read_text()
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
    (d / "src" / "service.py").write_text(SERVICE)
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
    path.write_text(body)
    return rows


def fragment(repo, rows, name="2000000001-a-later-item"):
    path = repo / "seal" / "ledger" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(row + "\n" for row in rows))
    return path


def citation(row, literal, version="0.1.0", section=SECTION):
    return f'seal/releases/{version}.md#"{section}">"{literal}"@{line_hash(row)}'


def edit_handler(repo):
    (repo / "src" / "service.py").write_text(SERVICE.replace("y = x + 1", "y = x + 2"))


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
    """The lines the run printed under the ledger NAME, up to its counts."""
    lines = out.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == name)
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
    (repo / "src" / "service.py").write_text(SERVICE.split("\n\n\ndef other")[0] + "\n")
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
    path.write_text(path.read_text().replace("| read |", "| read again |"))
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
        + "".join(r + "\n" for r in rows)
    )
    lines = path.read_text().splitlines()
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
    (repo / "src" / "service.py").write_text(SERVICE.split("\n\n\ndef other")[0] + "\n")
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
        "| Checked | Notes |\n|---|---|---|---|---|\n" + row + "\n"
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
        f"| Ledger frozen from | {value} |\n"
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
        SERVICE.replace("y = x + 1", "y = x + 2").replace("x * 2", "x * 3")
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
    written = (repo / INTO).read_text().splitlines()
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
    first = (repo / INTO).read_text()
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 0, out.stdout
    assert (repo / INTO).read_text() == first


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
    assert f"src/service.py#handler@{h}" in (repo / INTO).read_text()
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
    text = (repo / "src" / "service.py").read_text()
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
        SERVICE.replace("    return y\n", "    return y  # the sum\n")
    )
    frozen(repo)
    out = run(["--reverify", "--into", INTO, "--checked", "2026-02-01", "."], repo)
    assert out.returncode == 0, out.stdout + out.stderr
    assert '#handler>"return y"@' in (repo / INTO).read_text()
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
    (repo / "src" / "service.py").write_text(SERVICE.replace("x * 2", "x * 7"))
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
    written = (repo / "seal" / "ledger" / "3000000001-y.md").read_text()
    now = unit_hash(repo, "src/service.py", "other")
    assert f"`src/service.py#other@{now}`" in written, written
    assert run(["--strict", "."], repo).returncode == 0
