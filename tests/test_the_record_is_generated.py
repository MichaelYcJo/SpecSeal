"""The round record is generated from the reviewer's report, never written.

Issue #161 measured the last branch: 12.8 of its 18.8 active hours sat in
front of record commits, and half of its 65 findings were located in a record
rather than in code. The record is nine parsed fields and four tables, every
one of them derivable from something that is not prose -- the target from
git, the two terminal lines and the three tables from the reviewer's report,
the reach-back from the record that came before -- and the orchestrator was
typing all of it by hand, one cell at a time, with a reviewer waiting.

`skills/code-review/scripts/round_record.py new` writes the record. These
cases pin one derivation each, on a scratch repository, and read the cell
back through the same reader `chain_check.py` uses -- so a cell that reads
right here is a cell the pull-request check reads the same way.

`chain_check.py --worktree` is the other half: the generator runs the check
before the record is committed, which the check could not do while it read
`git show HEAD:`. Both directions of that flag are pinned below, and the
cases were written before the flag existed and seen red (§15).
"""

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, "skills", "code-review", "scripts")
GENERATOR = os.path.join(SCRIPTS, "round_record.py")
CHECK = os.path.join(SCRIPTS, "chain_check.py")
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")

# Begun after every cutoff `chain_check.py` carries, so every rule it has
# applies to the records written here. The second is what the grandfathering
# reads, and nothing else in the name matters.
ITEM = "seal/specs/1799000000-a-later-work-item"
ROUNDS = f"{ITEM}/rounds"

RAN_BY = "specseal:warden on a model"
ASKED = "Attack the parser first, then the reach-back.\n\nTwo coordinates.\n"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generator_module():
    return _load("specseal_round_record_for_tests", GENERATOR)


def check_module():
    return _load("specseal_chain_check_for_generated_records", CHECK)


def reader_module():
    return _load("specseal_reader_for_generated_records", READER)


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(repo, message):
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "commit",
        "-qm",
        message,
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("generated-record-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declaration():
    return (
        f"# {os.path.basename(ITEM)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )


def declared(repo):
    """The routing declaration committed; returns the commit, which is the
    natural `Target SHA` of round 1."""
    write(repo, f"{ITEM}/routing.md", declaration())
    return commit(repo, "declare")


VERDICT_HEADER = (
    "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
)
PROBE_HEADER = "| What was run | Result |\n|---|---|\n"
DEFERRED_HEADER = "| Finding | Where it went | Who answers it |\n|---|---|---|\n"

OPEN_ROW = "| 🔴 1 | the parser drops a row | `f.py:1` | open | executed |\n"
CLOSED_ROW = "| 🟢 2 | round 0's finding | `f.py:1` | answered | read |\n"
PROBE_ROW = "| `pytest tests/test_x.py -q` | 3 passed |\n"
DEFERRED_ROW = "| the windows leg | `overview.md` | the CI leg |\n"


def report(
    verdicts=OPEN_ROW,
    probes=PROBE_ROW,
    deferred=DEFERRED_ROW,
    needs="yes — 🔴 1",
    floor="no",
    verdict_header=VERDICT_HEADER,
    lines=True,
):
    """A reviewer's report in the shape `agents/warden.md` §Report asks for.

    `probes=None` / `deferred=None` leave that table out entirely, which is a
    state the generator has to fill rather than refuse. `verdicts=None`
    leaves the verdict table out, which it refuses. `lines=False` drops the
    two terminal lines, which it refuses too.
    """
    text = "# what the round found\n\nProse about 🔴 1, with a paste-ready fix.\n\n"
    if verdicts is not None:
        text += f"## Verdicts\n\n{verdict_header}{verdicts}\n"
    if probes is not None:
        text += f"## Executed probes\n\n{PROBE_HEADER}{probes}\n"
    if deferred is not None:
        text += f"## Deferred\n\n{DEFERRED_HEADER}{deferred}\n"
    if lines:
        text += f"Needs a fix: {needs}\nLoses a record or crashes: {floor}\n"
    return text


def env_without_a_pull_request():
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    # `gh` may or may not be on PATH here, and a scratch repository has no
    # remote either way, so the `PR` cell lands on `not yet opened` on every
    # machine -- as long as `gh` does not stop to ask something.
    env["GH_PROMPT_DISABLED"] = "1"
    env["GH_NO_UPDATE_NOTIFIER"] = "1"
    return env


def generate(
    repo,
    n=1,
    target=None,
    report_text=None,
    asked=ASKED,
    ran_by=RAN_BY,
    extra=(),
):
    """Run `round_record.py new`; return (exit code, output, record text).

    The report and the round paragraph are written OUTSIDE the repository,
    which is where a session keeps them (`questions.md` A2): they are not
    committed, and they must not show up in the working-tree diff either.
    """
    scratch = repo.parent
    report_path = scratch / f"report-{n}.md"
    asked_path = scratch / f"asked-{n}.md"
    report_path.write_text(
        report() if report_text is None else report_text, encoding="utf-8"
    )
    asked_path.write_text(asked, encoding="utf-8")
    target = target or git(repo, "rev-parse", "HEAD").stdout.strip()
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "new",
            "--item",
            str(repo / ITEM),
            "--round",
            str(n),
            "--target",
            target,
            "--report",
            str(report_path),
            "--asked",
            str(asked_path),
            "--ran-by",
            ran_by,
            "--baseline",
            "base",
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env_without_a_pull_request(),
    )
    path = repo / ROUNDS / f"round-{n}.md"
    text = path.read_text(encoding="utf-8") if path.exists() else None
    return r.returncode, r.stdout + r.stderr, text


def fields(text):
    """Every `| label | value |` row of a record, through the shared reader."""
    reader = reader_module()
    chain = check_module()
    rows = chain.table_rows(reader, reader.readable(text))
    return {cells[0].strip(): cells[1].strip() for cells in rows if len(cells) == 2}


def section(text, heading):
    """The lines of one `## …` section, comments and fences blanked."""
    lines = reader_module().readable(text)
    starts = [i for i, ln in enumerate(lines) if ln.strip() == heading]
    assert len(starts) == 1, f"{heading!r} appears {len(starts)} times"
    body = []
    for line in lines[starts[0] + 1 :]:
        if line.startswith("#"):
            break
        body.append(line)
    return body


def rows_of(text, heading):
    """The table rows under a heading, as raw lines, header and separator
    included."""
    return [ln.strip() for ln in section(text, heading) if ln.strip().startswith("|")]


# --- the field table, one case per derivation --------------------------------


def test_the_target_is_the_flag_and_it_has_to_resolve(repo):
    sha = declared(repo)
    code, out, text = generate(repo, target=sha)
    assert code == 0, out
    assert fields(text)["Target SHA"] == sha

    code, out, text = generate(repo, n=2, target="0" * 40)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "does not resolve" in out


def test_ran_by_is_the_flag(repo):
    declared(repo)
    code, out, text = generate(repo, ran_by="specseal:warden on sonnet")
    assert code == 0, out
    assert fields(text)["Ran by"] == "specseal:warden on sonnet"


def test_the_pr_cell_is_the_flag_or_not_yet_opened(repo):
    """A scratch repository has no remote, so `gh` -- present or not -- can
    name no pull request, and the honest value is the template's."""
    declared(repo)
    code, out, text = generate(repo)
    assert code == 0, out
    assert fields(text)["PR"] == "not yet opened"

    code, out, text = generate(repo, n=2, extra=("--pr", "#7 — draft"))
    assert fields(text)["PR"] == "#7 — draft", out


def test_the_pr_cell_reads_gh_when_it_answers():
    """`gh pr view --json number,url` is the source when it succeeds; the
    number comes first so `chain_check.PR_RE` finds it before the digits in
    the URL. Injected rather than run, because a real `gh` needs a remote."""
    generator = generator_module()

    def which(name):
        return "/Users/x/bin/gh" if name == "gh" else None

    def run(argv, **kwargs):
        assert argv[:3] == ["gh", "pr", "view"], argv
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout=json.dumps({"number": 12, "url": "https://example.com/o/r/pull/12"}),
            stderr="",
        )

    cell = generator.pull_request_cell("/Users/x/repo", None, which=which, run=run)
    assert cell.startswith("#12 "), cell
    assert "https://example.com/o/r/pull/12" in cell

    def failing(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 1, stdout="", stderr="no remote")

    assert (
        generator.pull_request_cell("/Users/x/repo", None, which=which, run=failing)
        == "not yet opened"
    )
    assert (
        generator.pull_request_cell("/Users/x/repo", None, which=lambda n: None)
        == "not yet opened"
    )


def test_the_broad_gate_is_the_flag_or_not_yet(repo):
    declared(repo)
    code, out, text = generate(repo)
    assert code == 0, out
    assert fields(text)["Broad gate"] == "not yet"

    code, out, text = generate(repo, n=2, extra=("--broad-gate", "abc1234 vs base"))
    assert fields(text)["Broad gate"] == "abc1234 vs base", out


def test_a_round_with_an_open_finding_lands_on_the_pending_values(repo):
    """The values `ORDER_FROM` requires of a record committed before its
    fixes exist -- spelled from `chain_check`'s own constants, so the
    generator and the checker cannot disagree about the string."""
    chain = check_module()
    declared(repo)
    code, out, text = generate(repo)
    assert code == 0, out
    cells = fields(text)
    assert cells["Fixes checked by"] == f"{chain.NOBODY} — {chain.NOT_YET}"
    assert cells["Contract changes"] == f"{chain.NONE_WORD} — {chain.NOT_YET}"
    assert cells["New units"] == f"{chain.NONE_WORD} — {chain.NOT_YET}"
    assert "- [ ] Pass" in text


def test_a_round_that_closes_everything_without_a_fix_says_no_fixes_to_check(repo):
    """The terminal record of a run. `fix_surface`'s docstring names the
    pair this refuses to write: *not yet written* beside `no fixes to check`
    is false the moment it is written, because a round that commissioned no
    fixes will never have any."""
    chain = check_module()
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(verdicts=CLOSED_ROW, needs="no")
    )
    assert code == 0, out
    cells = fields(text)
    assert cells["Fixes checked by"] == chain.NO_FIXES
    assert cells["Contract changes"] == chain.NONE_WORD
    assert cells["New units"] == chain.NONE_WORD
    assert "- [x] Pass" in text


def test_the_two_terminal_lines_are_copied_after_the_colon(repo):
    """The row names the field, so the cell is the value alone -- the
    field's first user copied the whole line and had nothing to read."""
    declared(repo)
    code, out, text = generate(
        repo,
        report_text=report(needs="yes — 🔴 1 and 🟡 2", floor="yes — a record leaves"),
    )
    assert code == 0, out
    cells = fields(text)
    assert cells["Needs a fix"] == "yes — 🔴 1 and 🟡 2"
    assert cells["Loses a record or crashes"] == "yes — a record leaves"
    assert "Needs a fix: " not in cells["Needs a fix"]


@pytest.mark.parametrize("missing", ["Needs a fix", "Loses a record or crashes"])
def test_a_report_without_one_of_the_two_lines_is_refused(repo, missing):
    declared(repo)
    text = report()
    text = "\n".join(ln for ln in text.splitlines() if not ln.startswith(missing))
    code, out, record = generate(repo, report_text=text)
    assert code == 2, out
    assert record is None, "a refusal writes no record"
    assert missing in out


def test_the_field_rows_are_the_templates_in_the_templates_order(repo):
    """Derived from `templates/sdd-round.md` rather than listed here, the way
    `test_the_run_stops_at_the_last_finding` reads the same table: a row the
    template gains and the generator does not is what this catches."""
    declared(repo)
    code, out, text = generate(repo)
    assert code == 0, out
    # The field table is what stands above the `Pass` box, in both files.
    template = read("templates", "sdd-round.md")
    template = re.findall(
        r"^\| ([^|]+?) \| <",
        template[: template.index("- [ ] Pass")],
        flags=re.MULTILINE,
    )
    generated = [
        cells[0].strip()
        for cells in check_module().table_rows(
            reader_module(), reader_module().readable(text[: text.index("] Pass")])
        )
        if len(cells) == 2 and cells[0].strip() not in ("Field", "---")
    ]
    assert generated == template, (generated, template)


# --- the four sections -------------------------------------------------------


def test_the_asked_section_is_the_file_verbatim(repo):
    declared(repo)
    code, out, text = generate(repo)
    assert code == 0, out
    body = "\n".join(section(text, "## What this round was asked")).strip()
    assert body == ASKED.strip()


def test_an_empty_round_paragraph_is_refused(repo):
    """#119: a record that does not say what it was asked is a record whose
    scope a later reader cannot tell from one the round invented."""
    declared(repo)
    code, out, text = generate(repo, asked="  \n")
    assert code == 2, out
    assert text is None


def test_the_three_tables_are_copied_row_for_row(repo):
    declared(repo)
    two = OPEN_ROW + CLOSED_ROW
    probes = PROBE_ROW + "| `python3 x.py` | exit 1 |\n"
    code, out, text = generate(
        repo, report_text=report(verdicts=two, probes=probes, needs="yes — 🔴 1")
    )
    assert code == 0, out
    assert rows_of(text, "## Verdicts") == [
        ln.strip() for ln in (VERDICT_HEADER + two).splitlines()
    ]
    assert rows_of(text, "## Executed probes") == [
        ln.strip() for ln in (PROBE_HEADER + probes).splitlines()
    ]
    assert rows_of(text, "## Deferred") == [
        ln.strip() for ln in (DEFERRED_HEADER + DEFERRED_ROW).splitlines()
    ]


def test_a_report_without_a_verdict_table_is_refused(repo):
    declared(repo)
    code, out, text = generate(repo, report_text=report(verdicts=None))
    assert code == 2, out
    assert text is None
    assert "## Verdicts" in out


def test_a_verdict_table_with_the_wrong_header_is_refused(repo):
    """The record's own columns, or nothing: a report whose header differs
    is a report the checker's column lookup would read differently."""
    declared(repo)
    wrong = "| # | Finding | Where | Verdict | Grounds |\n|---|---|---|---|---|\n"
    code, out, text = generate(repo, report_text=report(verdict_header=wrong))
    assert code == 2, out
    assert text is None
    assert "Location" in out


def test_absent_probe_and_deferred_tables_become_the_templates_empty_ones(repo):
    declared(repo)
    code, out, text = generate(repo, report_text=report(probes=None, deferred=None))
    assert code == 0, out
    assert rows_of(text, "## Executed probes") == [
        ln.strip() for ln in PROBE_HEADER.splitlines()
    ]
    assert rows_of(text, "## Deferred") == [
        ln.strip() for ln in DEFERRED_HEADER.splitlines()
    ]
    assert "nothing to drain" in "\n".join(section(text, "## Deferred"))


def test_round_one_inherits_nothing(repo):
    declared(repo)
    code, out, text = generate(repo)
    assert code == 0, out
    assert rows_of(text, "## Inherited coordinates") == [
        "| From | Coordinate | Why it is still worth opening |",
        "|---|---|---|",
    ]


def test_a_later_round_inherits_every_earlier_location_once(repo):
    """One row per `Location` cell of every earlier record, deduplicated by
    the coordinate: two findings at one place are one place to open."""
    declared(repo)
    first = (
        "| 🔴 1 | a | `f.py:1` | open | executed |\n"
        "| 🟡 2 | b | `g.py#unit` | answered | read |\n"
        "| 🟡 3 | c | `f.py:1` | open | read |\n"
        "| 🟡 4 | d | `h.py:3` and `h.py:9` \\| both | open | read |\n"
    )
    code, out, _ = generate(repo, report_text=report(verdicts=first))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, text = generate(repo, n=2, report_text=report(verdicts=CLOSED_ROW))
    assert text is not None, out
    assert rows_of(text, "## Inherited coordinates")[2:] == [
        "| round-1 | `f.py:1` | round 1's 🔴 1 — open |",
        "| round-1 | `g.py#unit` | round 1's 🟡 2 — answered |",
        # The pipe the reader unescaped is escaped again on the way out, or
        # the row it lands in has one cell too many.
        "| round-1 | `h.py:3` and `h.py:9` \\| both | round 1's 🟡 4 — open |",
    ]


def test_a_missing_report_or_paragraph_file_is_refused(repo):
    declared(repo)
    code, out, text = generate(repo, extra=("--report", str(repo.parent / "no.md")))
    assert code == 2, out
    assert text is None
    assert "no.md" in out


def test_the_baseline_defaults_to_the_upstream_else_origin_main(repo):
    generator = generator_module()
    assert generator.default_baseline(str(repo)) == "origin/main"
    git(repo, "branch", "--set-upstream-to=base")
    assert generator.default_baseline(str(repo)) == "base"


# --- the reach-back ----------------------------------------------------------


def test_the_previous_record_gets_its_checker_cell_and_nothing_else(repo):
    """Round N sets round N-1's `Fixes checked by` to `round-N`, and touches
    no other byte of that file -- the reach-back the orchestrator forgot
    five times on the last branch."""
    declared(repo)
    code, out, _ = generate(repo)
    assert code == 0, out
    commit(repo, "round 1")
    before = (repo / ROUNDS / "round-1.md").read_text(encoding="utf-8")
    write(repo, "f.py", "x = 2\n")
    commit(repo, "fix")
    code, out, text = generate(repo, n=2, report_text=report(verdicts=CLOSED_ROW))
    assert text is not None, out
    after = (repo / ROUNDS / "round-1.md").read_text(encoding="utf-8")
    assert fields(after)["Fixes checked by"] == "round-2"
    assert len(before.splitlines()) == len(after.splitlines())
    changed = [
        (a, b)
        for a, b in zip(before.splitlines(), after.splitlines(), strict=True)
        if a != b
    ]
    assert len(changed) == 1, changed
    assert changed[0][0].startswith("| Fixes checked by |")


def test_a_missing_previous_record_is_refused(repo):
    declared(repo)
    code, out, text = generate(repo, n=2)
    assert code == 2, out
    assert text is None
    assert "round-1.md" in out


def test_a_previous_record_whose_checker_cell_does_not_parse_is_refused(repo):
    declared(repo)
    code, out, _ = generate(repo)
    assert code == 0, out
    path = repo / ROUNDS / "round-1.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"^\| Fixes checked by \|.*$",
        "| Fixes checked by | the session that wrote them |",
        text,
        flags=re.MULTILINE,
    )
    path.write_text(text, encoding="utf-8")
    commit(repo, "round 1")
    code, out, record = generate(repo, n=2)
    assert code == 2, out
    assert record is None
    assert "Fixes checked by" in out
    assert fields(path.read_text(encoding="utf-8"))["Fixes checked by"] == (
        "the session that wrote them"
    ), "a refusal leaves the earlier record as it was"


def test_the_two_record_run_reads_back_through_chain_check(repo):
    """The reach-back as `chain_check` reads it: round 1 commissioned a fix,
    the fix landed, round 1's cells were closed, round 2 verified. Exit 0
    end to end, with the second record still uncommitted -- which is what
    `--worktree` is for."""
    sha1 = declared(repo)
    code, out, _ = generate(repo, target=sha1)
    assert code == 0, out
    commit(repo, "round 1")
    write(repo, "f.py", "x = 2\n")
    fix = commit(repo, "fix")
    path = repo / ROUNDS / "round-1.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("| open |", f"| **fixed** `{fix[:7]}` |")
    text = re.sub(
        r"^\| (Contract changes|New units) \|.*$",
        r"| \1 | none |",
        text,
        flags=re.MULTILINE,
    )
    path.write_text(text, encoding="utf-8")
    sha2 = commit(repo, "round 1 closed")
    code, out, record = generate(
        repo, n=2, target=sha2, report_text=report(verdicts=CLOSED_ROW, needs="no")
    )
    assert record is not None, out
    assert code == 0, out
    assert "chain-check:" in out, "the check's own output is printed"
    assert fields(path.read_text(encoding="utf-8"))["Fixes checked by"] == "round-2"


# --- a malformed cell cannot be written --------------------------------------


def test_a_cell_writer_refuses_a_pipe_and_a_newline():
    generator = generator_module()
    for bad in ("a | b", "a\nb", "a\rb"):
        with pytest.raises(generator.Refused):
            generator.cell("Ran by", bad)
    assert generator.cell("Ran by", "a on b") == "| Ran by | a on b |"


def test_the_surface_rows_refuse_a_comma_too():
    """`depth_problems` splits an entry on a comma, so a comma in `New
    units` is two entries; the writer refuses it before the checker has to."""
    generator = generator_module()
    chain = check_module()
    for label in (chain.NEW_UNITS, chain.CONTRACT):
        with pytest.raises(generator.Refused):
            generator.cell(label, "get(a, b) (depth 1)")
    # A comma in any other row is prose and stays.
    assert "," in generator.cell(chain.NEEDS, "yes — 🔴 1, 🟡 2")


def test_a_flag_carrying_a_pipe_writes_no_record(repo):
    declared(repo)
    code, out, text = generate(repo, ran_by="specseal:warden | a model")
    assert code == 2, out
    assert text is None
    code, out, text = generate(repo, extra=("--broad-gate", "not yet\nreally"))
    assert code == 2, out
    assert text is None


def test_an_existing_record_is_not_overwritten(repo):
    declared(repo)
    code, out, first = generate(repo)
    assert code == 0, out
    code, out, second = generate(repo)
    assert code == 2, out
    assert "round-1.md" in out
    assert second == first


def test_the_exit_code_is_chain_checks_and_the_record_stays(repo):
    """A record the check refuses is still written -- the orchestrator
    corrects it in place -- and the generator's exit is the check's."""
    declared(repo)
    code, out, text = generate(repo, ran_by="a runner with no model")
    assert text is not None, out
    assert code == 1, out
    assert "Ran by" in out


# --- `chain_check --worktree`, both directions -------------------------------


def record(sha, passed=True, verdict="answered", finding="🟢 1"):
    """A record that passes every check `chain_check` makes of a new work
    item, so a failure can only come from what a case edits."""
    box = "x" if passed else " "
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n"
        f"| Ran by | {RAN_BY} |\n"
        "| Fixes checked by | no fixes to check |\n"
        "| Contract changes | none |\n| New units | none |\n"
        "| Needs a fix | no |\n| Loses a record or crashes | no |\n\n"
        f"- [{box}] Pass\n\n"
        "## Verdicts\n\n"
        f"{VERDICT_HEADER}"
        f"| {finding} | something | `f.py:1` | {verdict} | grounds |\n"
    )


def run_check(repo, worktree=False):
    r = subprocess.run(
        [
            sys.executable,
            CHECK,
            "--baseline",
            "base",
            "--root",
            str(repo),
            *(["--worktree"] if worktree else []),
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env_without_a_pull_request(),
    )
    return r.returncode, r.stdout + r.stderr


def test_an_uncommitted_edit_that_breaks_a_record_is_seen_only_with_the_flag(repo):
    sha = declared(repo)
    write(repo, f"{ROUNDS}/round-1.md", record(sha))
    commit(repo, "round 1")
    code, out = run_check(repo)
    assert code == 0, out
    path = repo / ROUNDS / "round-1.md"
    path.write_text(
        path.read_text(encoding="utf-8")
        .replace("| 🟢 1 |", "| 🔴 1 |")
        .replace("| answered |", "| open |"),
        encoding="utf-8",
    )
    code, out = run_check(repo)
    assert code == 0, "without the flag HEAD is judged, and HEAD is clean: " + out
    code, out = run_check(repo, worktree=True)
    assert code == 1, out
    assert "open" in out


def test_an_uncommitted_edit_that_repairs_a_record_is_seen_only_with_the_flag(repo):
    sha = declared(repo)
    write(repo, f"{ROUNDS}/round-1.md", record(sha, verdict="open", finding="🔴 1"))
    commit(repo, "round 1")
    code, out = run_check(repo)
    assert code == 1, out
    path = repo / ROUNDS / "round-1.md"
    path.write_text(
        path.read_text(encoding="utf-8")
        .replace("| 🔴 1 |", "| 🟢 1 |")
        .replace("| open |", "| answered |"),
        encoding="utf-8",
    )
    code, out = run_check(repo)
    assert code == 1, "without the flag HEAD is judged, and HEAD is broken: " + out
    code, out = run_check(repo, worktree=True)
    assert code == 0, out


def test_an_untracked_record_is_a_record_only_with_the_flag(repo):
    """The generator's own case: the record exists on disk and in no commit.
    Without the flag it is what CI would see, which is nothing."""
    sha = declared(repo)
    write(repo, f"{ROUNDS}/round-1.md", record(sha))
    code, out = run_check(repo)
    assert code == 1, out
    assert "holds no `round-N.md`" in out
    code, out = run_check(repo, worktree=True)
    assert code == 0, out


def test_an_untracked_records_target_is_held_to_the_branch(repo):
    """The untracked file is in the working-tree DIFF as well as on disk, so
    the record counts as one this pull request adds and its `Target SHA` has
    to be reachable. Listing the file without adding it to the diff would
    read the record and make no claim about where its commit is."""
    declared(repo)
    write(repo, f"{ROUNDS}/round-1.md", record("0" * 40))
    code, out = run_check(repo, worktree=True)
    assert code == 1, out
    assert "not an ancestor" in out


def test_the_flag_says_so_in_the_output(repo):
    """§14: a flag that changes what is read says so where the reader looks,
    because a local pass that CI will not repeat has to be recognisable as
    one."""
    sha = declared(repo)
    write(repo, f"{ROUNDS}/round-1.md", record(sha))
    commit(repo, "round 1")
    code, out = run_check(repo, worktree=True)
    assert code == 0, out
    assert "working tree" in out
    code, out = run_check(repo)
    assert "working tree" not in out


# --- the warden's report is the record's input -------------------------------


def test_the_wardens_report_headers_are_the_generators_constants():
    """One constant, two carriers. The generator refuses a table whose header
    is not the record's, so the headers `agents/warden.md` §Report tells the
    reviewer to write are read out of the generator and looked for there."""
    generator = generator_module()
    body = read("agents", "warden.md")
    report = body[body.index("\n## Report\n") :]
    for heading, header in generator.REPORT_TABLES:
        assert heading in report, heading
        assert generator.row(header) in report, generator.row(header)
    assert "round_record.py new" in report, (
        "the reviewer has to be told the tables are copied, or a finding "
        "outside them reads as a finding"
    )


def test_the_generators_headings_are_the_checkers_where_the_checker_has_one():
    """`## Verdicts` and the `Verdict` column are `chain_check`'s constants;
    the generator spells neither a second time."""
    generator = generator_module()
    chain = check_module()
    assert generator.VERDICTS == chain.VERDICTS
    assert chain.VERDICT_COLUMN in generator.VERDICT_HEADER
    assert f"{chain.NONE_WORD} — {chain.NOT_YET}" == generator.PENDING_SURFACE
    assert f"{chain.NOBODY} — {chain.NOT_YET}" == generator.PENDING_CHECKER
