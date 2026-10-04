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
    assert "newest reading" in left[0], left[0]


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
    and re-stamps M's citation against the line it moved R to, because the
    walk reads a cited file before every file citing it: exit 0, and
    `--strict` exits 0 with no second run. The fragment sorts first, so the
    walk in file order hashed M's citation against R's old line."""
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
def test_one_unfrozen_run_restamps_a_citation_no_order_places(repo, shape):
    """#772, round 1, yellow 1. A second fold of the newest release joins its
    file, so a release file can hold R1 and a `Re-read ·` row citing R1. A
    file's own re-stamp is planned only when its walk ends, so its citation
    was hashed against the old line, and `--strict` exited 2 until a second
    run. The same held for two files citing each other. Walked again until
    they settle, one run leaves `--strict` at 0, and each row it dated is
    named once. Beside a row it cannot date, a coordinate it cannot place and
    a ledger citing it that will not decode, each of those is named once,
    though the walk that names it is repeated."""
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


def test_the_walk_order_places_what_it_can_and_walks_the_rest_again(repo):
    """`cited_first` (#772). A file citing only placed files follows them. A
    file citing a row of itself, two files citing each other, and a file
    citing one of those are placed by no order: they keep the given order, to
    be walked again, at most two more times than the four citations among
    them. No file is lost."""
    h = unit_hash(repo, "src/service.py", "handler")
    rows = [
        f"| R{n} · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        for n in (1, 2)
    ]

    def reread(version, n):
        cite = citation(rows[n - 1], f"R{n} · handler adds one", version=version)
        return (
            f"| Re-read · R{n} · handler adds one | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    released(repo, [rows[0], reread("0.1.0", 1)], version="0.1.0")
    fragment(repo, [reread("0.1.0", 1)], name=M_ITEM)
    released(repo, [rows[0]], version="0.2.0")
    fragment(repo, [reread("0.2.0", 1)], name="2000000003-n")
    released(repo, [rows[1], reread("0.4.0", 1)], version="0.3.0")
    released(repo, [rows[0], reread("0.3.0", 2)], version="0.4.0")
    paths = [
        str(repo / f"seal/ledger/{M_ITEM}.md"),
        str(repo / "seal/ledger/2000000003-n.md"),
        str(repo / "seal/releases/0.1.0.md"),
        str(repo / "seal/releases/0.2.0.md"),
        str(repo / "seal/releases/0.3.0.md"),
        str(repo / "seal/releases/0.4.0.md"),
    ]
    once, again, walks = ec.cited_first(paths, str(repo), {}, None)
    assert once == [paths[3], paths[1]], once
    assert again == [paths[0], paths[2], paths[4], paths[5]], again
    assert walks == 6


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
