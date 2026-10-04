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
# outranks the new row and the family stays DRIFTED. The row is left whole,
# named, and nothing of it is written or recorded.

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
        "would stay DRIFTED; nothing was written or recorded for this row — "
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
        "outrank it; nothing was written or recorded for this row — a "
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
