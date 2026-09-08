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
    fixes=None,
):
    """A reviewer's report in the shape `agents/warden.md` §Report asks for.

    `probes=None` / `deferred=None` leave that table out entirely, which is a
    state the generator has to fill rather than refuse. `verdicts=None`
    leaves the verdict table out, which it refuses. `lines=False` drops the
    two terminal lines, which it refuses too. `fixes=None` leaves the
    paste-ready section out, which is the empty arm and is a record.
    """
    text = "# what the round found\n\nProse about 🔴 1, with a paste-ready fix.\n\n"
    if verdicts is not None:
        text += f"## Verdicts\n\n{verdict_header}{verdicts}\n"
    if fixes is not None:
        text += f"## Paste-ready fixes\n\n{fixes}\n"
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


FENCE = "```python\ndef helper(a):\n    return a  # the replacement\n```\n"


def test_a_fenced_block_under_the_probes_table_reaches_the_record(repo):
    """Round 2 of #161's own chain (🟡 10): round-1.md read *Fix below (A)*
    seven times and carried no block, because `new` copied the table alone.
    The block lands under the table, nothing else of the section does, and
    the check exits 0 over a record carrying a fence."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(probes=PROBE_ROW + "\n" + FENCE)
    )
    assert code == 0, out
    probes, rest = text.split("## Executed probes", 1)[1].split(
        "## Inherited coordinates", 1
    )
    assert FENCE.strip() in probes, text
    assert "the replacement" not in rest


def test_an_unclosed_fence_under_the_probes_table_is_refused(repo):
    """An unclosed fence copied as it stands swallows every heading after
    it in the record, so the generator refuses it by name and writes
    nothing."""
    declared(repo)
    unclosed = "```python\ndef helper(a):\n    return a\n"
    code, out, text = generate(
        repo, report_text=report(probes=PROBE_ROW + "\n" + unclosed)
    )
    assert code == 2, out
    assert "never closed" in out
    assert text is None


# --- where a fence closes, relative to the section it opened in --------------
#
# #169 called the late-closed shape "the one member of the class left open".
# Decomposed rather than listed (contract §12), the class is one boolean over
# one span: a fence has a closer or it has not, and where it has one the span
# from opener to closer either crosses a line the generator reads the report
# by, or it does not. `readable` blanks a fence, so anything inside that span
# is invisible to every walk downstream -- which is why the span, and not the
# crossed line's name, is what decides.
#
# Every member, and what each did at `c4d7077` before the guard:
#
#   no closer                     exit 2 -- but as `never closed` only for a
#                                 fence under the probes table, and otherwise
#                                 as `0 Needs a fix: lines`, because an
#                                 unclosed fence runs to the end of the file
#                                 and takes the terminal lines with it
#   closer, nothing crossed       copied whole, correctly     (case above)
#   closer, `## Verdicts`         exit 2, `the report has no ## Verdicts`
#   closer, `## Executed probes`  EXIT 0 -- the table silently gone
#   closer, `## Deferred`         EXIT 0 -- the section silently gone (#169)
#   closer, a terminal line       exit 2, `0 Needs a fix: lines`
#   closer, a prose heading       exit 0, and left that way (`spec.md` §Out)
#
# So two members lost a whole table with nothing said, not the one #169
# named; and three more were caught by a message that blames the reviewer
# for a section they did write. #169's proposed `SECTIONS` membership test
# inside `fenced_after` reaches neither group: `## Executed probes` taken
# means `fenced_after` is never called at all.
#
# The last row is the deliberate limit, and it is also what keeps this work
# item generating its own records: a reviewer of THIS branch pastes
# record-shaped blocks, headings and all. What is refused is a report LOSING
# a section, never a fence mentioning one.

TERMINAL = "Needs a fix: yes — 🔴 1\nLoses a record or crashes: no\n"
HEAD_AND_VERDICTS = (
    "# what the round found\n\nProse about 🔴 1.\n\n"
    f"## Verdicts\n\n{VERDICT_HEADER}{OPEN_ROW}\n"
)
PROBES_TABLE = f"## Executed probes\n\n{PROBE_HEADER}{PROBE_ROW}\n"
DEFERRED_TABLE = f"## Deferred\n\n{DEFERRED_HEADER}{DEFERRED_ROW}\n"
OPENER = "```python\ndef helper(a):\n    return a\n\n"
CLOSER = "```\n\n"


def test_a_fence_closed_after_the_deferred_table_is_refused(repo):
    """#169, found by round 3 of #161's own chain. The fence opens under the
    probes table and closes below the Deferred table, so `## Deferred` sits
    inside it -- and `readable` blanks a fence, which means `section_body`
    never stops there and the fence reads as closed. Executed at `c4d7077`
    before the guard: exit 0, the record carrying `## Deferred` and its row
    inside the fence while its own Deferred section read `nothing to drain`.
    """
    declared(repo)
    late = HEAD_AND_VERDICTS + PROBES_TABLE + OPENER + DEFERRED_TABLE + CLOSER
    code, out, text = generate(repo, report_text=late + TERMINAL)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "swallows `## Deferred`" in out


# One entry per REQUIRED section, which is what the guard below may refuse a
# report over. `## Paste-ready fixes` is deliberately absent — it is optional,
# so a fence quoting it while it is missing is a report the guard must accept,
# and that is a case of its own rather than a parameter here.
SECTION_TEXT = {
    "## Verdicts": f"## Verdicts\n\n{VERDICT_HEADER}{OPEN_ROW}\n",
    "## Executed probes": PROBES_TABLE,
    "## Deferred": DEFERRED_TABLE,
}


@pytest.mark.parametrize("taken", list(SECTION_TEXT))
def test_a_fence_that_takes_a_section_the_generator_reads_is_refused(repo, taken):
    """The class itself, over the generator's own list of what it reads
    (contract §12). The fence opens above one section and closes below it,
    so that section is gone by every later reading -- and each reading has
    its own wrong answer for absence: an empty template for the two optional
    tables, `the report has no ## Verdicts section` for the required one.
    Each blames the reviewer for a section they did in fact write.

    Parametrized over `REQUIRED_HEADINGS` rather than over the names typed
    here, which is the whole argument against #169's `SECTIONS` tuple: a
    section added later is guarded, and gets a case, by being added there.

    `REQUIRED_HEADINGS` and not `READ_HEADINGS`, because the refusal is only
    correct for a section the report MUST carry — round 1's 🟡 3.
    `test_a_fence_quoting_the_optional_heading_is_kept_when_it_is_absent`
    holds the other side, and the two lists differing by exactly the optional
    section is what keeps the pair honest.

    `## Executed probes` is the member #169 did not name, and it is the one
    that settles where the guard lives -- a fence that takes that heading
    means `build` never calls `fenced_after` for it, so no guard inside that
    function could ever see the shape. Executed at `c4d7077`: exit 0 for
    `## Deferred` and `## Executed probes`."""
    generator = generator_module()
    assert list(generator.REQUIRED_HEADINGS) == list(SECTION_TEXT)
    assert set(generator.READ_HEADINGS) - set(SECTION_TEXT) == {
        generator.PASTE_READY
    }, "the optional section is the one this guard must NOT refuse over"
    declared(repo)
    body = "# what the round found\n\nProse about 🔴 1.\n\n"
    for heading, text in SECTION_TEXT.items():
        body += (OPENER + text + CLOSER) if heading == taken else text
    code, out, text = generate(repo, report_text=body + TERMINAL)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert f"swallows `{taken}`" in out


def test_an_unclosed_fence_above_the_probes_table_names_the_fence(repo):
    """§14, and the unclosed half of the class opened one section earlier.
    That refusal used to live in `fenced_after`, which `build` calls for the
    probes section alone -- and a fence opened under the verdict table takes
    `## Executed probes` with it, so the call never happened for a section
    the report no longer had. Nothing was lost silently, because an unclosed
    fence runs to the end of the file and takes the terminal lines too:
    executed at `c4d7077`, exit 2 reading `the report has 0 Needs a fix:
    lines`, which sends the writer to look for a line they wrote. The rule
    is report-wide or it reads one section, and the message names the fence
    or it names a symptom."""
    declared(repo)
    early = HEAD_AND_VERDICTS + OPENER + PROBES_TABLE + DEFERRED_TABLE
    code, out, text = generate(repo, report_text=early + TERMINAL)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "never closed" in out


def test_a_fence_that_swallows_a_terminal_line_names_the_fence(repo):
    """§14. This shape was already refused at `c4d7077`, for having `0
    Needs a fix: lines` -- which tells the writer to add a line they did in
    fact write. The fence is what is wrong, so the fence is what is named.

    The fence opens below the Deferred table and closes at the end of the
    file, so the terminal lines are the only thing it takes: a report that
    also loses a section is named by the section, which is the more useful
    half of the same message."""
    declared(repo)
    end = HEAD_AND_VERDICTS + PROBES_TABLE + DEFERRED_TABLE + OPENER + TERMINAL
    code, out, text = generate(repo, report_text=end + "```\n")
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "swallows `Needs a fix:`" in out


def test_a_fence_quoting_a_heading_is_kept_while_the_real_one_stands(repo):
    """The limit of the rule. A report may quote a heading inside a fence --
    a reviewer of this very work item does -- and what decides is whether
    the real section still stands outside the fence. This report's does, so
    the block is copied and the Deferred table is read as written."""
    declared(repo)
    quoted = "```markdown\n## Deferred\n\nnothing to drain\n```\n"
    code, out, text = generate(
        repo, report_text=report(probes=PROBE_ROW + "\n" + quoted)
    )
    assert code == 0, out
    assert quoted.strip() in text
    assert rows_of(text, "## Deferred") == [
        ln.strip() for ln in (DEFERRED_HEADER + DEFERRED_ROW).splitlines()
    ]


def test_a_comment_at_column_zero_inside_a_fence_is_not_a_heading(repo):
    """A `#` at column 0 is a heading in Markdown and a comment in Python,
    and only the fence tells them apart. So the guard reads the lines a
    fence hid against what the generator actually looks up in the report,
    never against the `#` character."""
    declared(repo)
    commented = "```python\n# rebuild the row, then:\n"
    commented += "def helper(a):\n    return a\n```\n"
    code, out, text = generate(
        repo, report_text=report(probes=PROBE_ROW + "\n" + commented)
    )
    assert code == 0, out
    assert "# rebuild the row, then:" in text


def test_prose_under_the_probes_table_stays_in_the_report(repo):
    """A fence is copied whole and nothing else of the section is
    (`fenced_after`'s docstring, and `questions.md` A5 of #161's item).
    Round 3 of that chain (⬜ 16) found the clause had no case at all: a
    mutation widening the copy to the whole section body passes both fence
    cases above, because both look only at what the fence itself carries."""
    declared(repo)
    prose = "The block replaces the helper; this sentence must not travel.\n"
    code, out, text = generate(
        repo, report_text=report(probes=PROBE_ROW + "\n" + prose + "\n" + FENCE)
    )
    assert code == 0, out
    assert FENCE.strip() in text
    assert "must not travel" not in text


# --- the same boolean, applied to the two texts and the third input ----------
#
# Round 1 of this work item's own chain measured what the seven-member table
# above did NOT cover, and none of it is a new member of that partition. The
# partition is one boolean over one span, and it is complete for that boolean;
# what was under-counted is what the boolean was applied TO.
#
#   the text          `swallowed` reads `strip_comments(report)`, and
#                     `fenced_after` reads `raw`. A fence opener inside an
#                     HTML comment is absent from the first and present in
#                     the second, so the report-wide check reads a text that
#                     does not have it while the copy reads one that does
#   the line          the partition's read lines were `REPORT_TABLES`'
#                     headings and `TERMINAL_LINES`. The generator also reads
#                     the table ROWS under a standing heading, and a fence
#                     that takes those alone leaves the heading in place
#   the input         the round paragraph is spliced into the record above
#                     every section a reader looks up, and it never passed
#                     through the guard at all
#
# Round 2 then found that list one member short, and the missing one was
# created by round 1's own fix (contract §12: the enumeration is re-run with
# the new pair in it). The three axes above are one axis -- the text a hider
# is asked about -- and there is a second: WHICH hider. `readable` blanks with
# two passes and `strip_comments` runs first, so an HTML comment opened and
# never closed blanks every line below it exactly as an open fence does, and
# the fence pass cannot see it because by then those lines are already gone.
#
# The grid is the three copies the generator makes -- `build` splices the
# round paragraph whole, `table_of` copies a row out of `raw`, `fenced_after`
# copies a block out of `raw` -- crossed with the two hiders. Measured at
# `aed3ca0`, before the second column existed:
#
#                       an open fence            an open HTML comment
#   the report          `NEVER_CLOSED`           exit 2 on `0 Needs a fix:
#                                                lines` -- the writer sent to
#                                                add a line they did write
#   the round paragraph `ASKED_NEVER_CLOSED`     EXIT 1, RECORD WRITTEN, and
#                                                four of its five sections
#                                                unreadable                🔴 7
#   a copied block      `NEVER_CLOSED_VERBATIM`  unreachable: an opener inside
#                                                the block whose closer is
#                                                outside it puts the block's
#                                                own closing fence inside the
#                                                comment, so the fence pass
#                                                sees an unclosed fence first
#   a copied row        `SWALLOWED_TABLE`        the straddle: balanced in the
#                                                report, half in the record.
#                                                Open, `overview.md` §Not done
#
# Two cells are closed below. The row straddle stays open because it needs a
# limit argument the others do not -- a copied block may legitimately carry a
# whole comment, so its question is balance across the slice, not presence.


UNCLOSED_COMMENT_ASKED = "Attack the parser first.\n\n<!-- the coordinate to open\n"
# A fence that closes, holding a comment that does not. `strip_comments` runs
# first, so the block's own closing fence is inside the comment and blank by
# the time the fence pass looks -- which is why the comment is asked first.
COMMENT_INSIDE_A_FENCE = "Attack it.\n\n```python\n<!-- a note\nx = 1\n```\n"


def test_an_unclosed_html_comment_in_the_round_paragraph_is_refused(repo):
    """🔴 7 of round 2, and it is 🟡 3's own fix one hider over. The guard
    round 1 added asks `strip_comments(asked)` whether a fence is still open;
    `build` splices `asked` VERBATIM. So an unterminated comment is invisible
    to the check and present in the copy -- the same check/copy asymmetry as
    🔴 1, inside the guard written to close 🟡 3.

    Executed at `aed3ca0` before this: exit 1 with the record WRITTEN, and
    read back through the shared reader only `## What this round was asked`
    resolved -- `## Verdicts`, `## Executed probes`, `## Inherited
    coordinates` and `## Deferred` each 0 occurrences.

    The second half is the limit. A spawn prompt carries HTML comments as
    routinely as it carries fences -- the one that produced this work item
    does -- and a balanced one is copied whole, comment and all."""
    declared(repo)
    code, out, text = generate(repo, asked=UNCLOSED_COMMENT_ASKED)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "never closed" in out
    assert "round paragraph" in out
    assert "HTML comment" in out
    # And the shape that makes the ORDER load-bearing: the comment opens
    # inside a fenced block whose closer it therefore blanks. Asked the
    # fence question first, this is refused for a fence that is closed in
    # the text as written -- the wrong hider, named to the wrong writer.
    code, out, text = generate(repo, asked=COMMENT_INSIDE_A_FENCE)
    assert code == 2, out
    assert text is None
    assert "HTML comment" in out, "the fence closes; the comment does not"
    code, out, text = generate(repo, asked=UNCLOSED_COMMENT_ASKED + "-->\n")
    assert code == 0, out
    assert "the coordinate to open" in text


UNCLOSED_COMMENT_REPORT = "<!-- a note about the row\nstill the note\n"


def test_an_unclosed_html_comment_in_the_report_names_the_comment(repo):
    """§14, and the same hider on the other input. Here nothing is lost
    silently -- an unterminated comment runs to the end of the file, so it
    always takes the terminal lines with it -- and what was wrong is the
    message. Executed at `aed3ca0`: exit 2 reading `the report has no ##
    Verdicts section` for a comment above the table, and `the report has 0
    Needs a fix: lines` for one below it. Both send the writer to look for
    something they did in fact write, which is the defect §14 and
    `test_a_fence_that_swallows_a_terminal_line_names_the_fence` already
    fixed for fences.

    The comment question is asked BEFORE the fence question, because an open
    comment blanks the closing fence of every block below it: asked the other
    way round, a report with one unterminated comment is refused for a fence
    that is closed in the text as written."""
    declared(repo)
    head = "# what the round found\n\n" + UNCLOSED_COMMENT_REPORT
    tail = f"\nProse about 🔴 1.\n\n## Verdicts\n\n{VERDICT_HEADER}{OPEN_ROW}\n"
    tail += PROBES_TABLE + DEFERRED_TABLE + TERMINAL
    code, out, text = generate(repo, report_text=head + tail)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "never closed" in out
    assert "HTML comment" in out
    # The order, on the report side: the comment opens inside a fenced block
    # under the probes table, so the block's own closer is blanked before the
    # fence pass runs. Asked the fence question first, this is refused as
    # `a fenced block in the report is never closed` -- and the fence closes.
    inside = "```python\n<!-- a note\nx = 1\n```\n"
    body = HEAD_AND_VERDICTS + f"## Executed probes\n\n{PROBE_HEADER}{PROBE_ROW}\n"
    code, out, text = generate(
        repo, report_text=body + inside + "\n" + DEFERRED_TABLE + TERMINAL
    )
    assert code == 2, out
    assert text is None
    assert "HTML comment" in out, "the fence closes; the comment does not"
    code, out, text = generate(repo, report_text=head + "-->\n" + tail)
    assert code == 0, out
    assert rows_of(text, "## Deferred") == [
        ln.strip() for ln in (DEFERRED_HEADER + DEFERRED_ROW).splitlines()
    ]


COMMENTED_OPENER = "<!-- a note about the row\n```\nstill the note\n-->\n"


def test_a_fence_opened_inside_an_html_comment_is_refused(repo):
    """🔴 1 of round 1. `swallowed` reads `strip_comments(report)` and
    `fenced_after` reads `raw`, so an opener inside an HTML comment is
    invisible to the report-wide check and an opener to the copy. Executed at
    `861ad16` before this: exit 0 with the record written, and read back
    through the shared reader its `## Inherited coordinates` and `## Deferred`
    each resolved to 0 occurrences -- the defect this work item exists to fix,
    arriving through the door phase 1 opened by calling `fenced_after`'s
    never-closed raise unreachable."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(probes=PROBE_ROW + "\n" + COMMENTED_OPENER)
    )
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "never closed" in out
    assert "HTML comment" in out


# A comment that opens inside a fenced block and closes AFTER it. Every fence
# here closes; the block's closer is inside the comment, which is one pass
# earlier, so the fence question is asked of a text that no longer has it.
CROSSING_COMMENT = "```python\n<!-- a note\nx = 1\n```\n-->\n"


def test_a_comment_that_crosses_a_fence_names_the_comment(repo):
    """🟡 11 of round 3, and the third answer the two questions needed.

    Executed at `8114937` before this: exit 2 reading `a fenced block in the
    report is never closed`, and `blank_fences` over the report as WRITTEN
    leaves no fence open -- so the reviewer is sent to look for something that
    is not there. That is the defect §14 exists for and the one round 2 of
    this generator's own chain paid for once already, one hider over.

    The comment question passes here, which is why the order cannot prevent
    it: the comment is balanced report-wide. What is unbalanced is the
    comment's span against the block's closing fence, and only asking the
    fence question of the raw text as well tells that from a fence nobody
    closed."""
    declared(repo)
    body = HEAD_AND_VERDICTS + f"## Executed probes\n\n{PROBE_HEADER}{PROBE_ROW}\n"
    code, out, text = generate(
        repo, report_text=body + CROSSING_COMMENT + "\n" + DEFERRED_TABLE + TERMINAL
    )
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "opens inside a fenced block and closes outside it" in out
    assert "names a fence you did close" in out, "the message says what it is not"
    assert "never closed" not in out, "no fence in this report is unclosed"
    # And the coordinate, because `somewhere in the report` is not actionable.
    assert "<!-- a note" in out


def test_a_comment_that_crosses_a_fence_in_the_round_paragraph(repo):
    """§12's other instance: the same cause on the other text asked. A spawn
    prompt carries fenced blocks and HTML comments routinely, and the
    paragraph is spliced above every section a reader looks up.

    Executed at `8114937` before this: exit 2 reading `a fenced block in the
    round paragraph is never closed`, about a paragraph whose every fence
    closes."""
    declared(repo)
    code, out, text = generate(repo, asked="Attack it.\n\n" + CROSSING_COMMENT)
    assert code == 2, out
    assert text is None
    assert "round paragraph" in out
    assert "opens inside a fenced block and closes outside it" in out
    assert "never closed" not in out


FENCED_DEFERRED = f"## Deferred\n\n```\n{DEFERRED_HEADER}{DEFERRED_ROW}```\n"


def test_a_fence_hiding_a_whole_table_under_a_standing_heading_is_refused(repo):
    """🟡 2 of round 1. The heading stands, so the heading loop sees nothing,
    and the table is what the fence took: the record then reads `nothing to
    drain` beside a row the reviewer wrote. Executed at `861ad16` before this:
    exit 0, the record's Deferred section reading `nothing to drain`.

    The condition is F3's shape one level down -- the loss, never the mention.
    A fence quoting rows beside a table that still stands is copied as it
    always was, which is what keeps a reviewer of THIS generator able to paste
    record-shaped blocks."""
    declared(repo)
    body = HEAD_AND_VERDICTS + PROBES_TABLE + FENCED_DEFERRED + "\n"
    code, out, text = generate(repo, report_text=body + TERMINAL)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "every table row of `## Deferred`" in out


QUOTED_ROWS = f"```markdown\n{DEFERRED_HEADER}{DEFERRED_ROW}```\n"
EMPTY_DEFERRED = "## Deferred\n\nnothing to drain\n\n"


def test_a_fence_quoting_table_rows_is_kept_while_the_table_stands(repo):
    """The limit of the row half, and the case both of its narrowing clauses
    needed. The report is the one a reviewer of THIS generator writes: a
    record-shaped block pasted under the probes table, rows and all, beside a
    Deferred section that is honestly empty.

    Two mutations turn this red and turn nothing else red, which is why the
    case exists rather than an argument in a comment:

      dropping *the table still stands*   the probes section has hidden rows
                                          and a table, so the block a probes
                                          row owes is refused -- the guard
                                          stopping the tool on its own rounds
      dropping the positional scoping     the hidden rows are under the probes
                                          table and `## Deferred` is empty for
                                          its own reasons, so an empty section
                                          is blamed for a fence in another one
    """
    declared(repo)
    body = (
        HEAD_AND_VERDICTS
        + f"## Executed probes\n\n{PROBE_HEADER}{PROBE_ROW}\n"
        + QUOTED_ROWS
        + "\n"
        + EMPTY_DEFERRED
    )
    code, out, text = generate(repo, report_text=body + TERMINAL)
    assert code == 0, out
    assert QUOTED_ROWS.strip() in text, text
    assert [ln.strip() for ln in section(text, "## Deferred") if ln.strip()] == [
        "| Finding | Where it went | Who answers it |",
        "|---|---|---|",
        "nothing to drain",
    ]


UNCLOSED_ASKED = "Attack the parser first.\n\n```python\ndef helper(a):\n    return a\n"


def test_an_unclosed_fence_in_the_round_paragraph_is_refused(repo):
    """🟡 3 of round 1. The round paragraph is the orchestrator's copy of a
    spawn prompt, and spawn prompts carry fenced blocks routinely -- the one
    that produced this work item does. It is spliced above every section a
    reader looks up and never passed through the guard. Executed at `861ad16`
    before this: the record was WRITTEN, all four sections resolved to 0
    occurrences, and the run then failed blaming a missing `## Verdicts`."""
    declared(repo)
    code, out, text = generate(repo, asked=UNCLOSED_ASKED)
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "never closed" in out
    assert "round paragraph" in out


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


def test_a_previous_record_that_commissioned_no_fixes_keeps_its_cell(repo):
    """Round 1's 🟡 6 of #161's own chain: a round whose every verdict closed
    without a fix word reads `no fixes to check`, and the reach-back wrote
    `round-2` over it -- a claim that round 2 read fixes that never existed.
    The cell is kept, the record is untouched, and `new` says so."""
    chain = check_module()
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=CLOSED_ROW, needs="no"))
    assert code == 0, out
    commit(repo, "round 1")
    path = repo / ROUNDS / "round-1.md"
    before = path.read_text(encoding="utf-8")
    assert fields(before)["Fixes checked by"] == chain.NO_FIXES
    write(repo, "f.py", "x = 2\n")
    commit(repo, "an unrelated edit")
    code, out, text = generate(repo, n=2, report_text=report(verdicts=CLOSED_ROW))
    assert text is not None, out
    assert path.read_text(encoding="utf-8") == before, "the record is untouched"
    assert f"`{chain.NO_FIXES}`" in out, out
    assert "round-2" not in out.split("round-record: wrote")[0], out


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
    for bad in ("a | b", "a\nb", "a\rb", "", "   "):
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


# --- a pipe the reviewer wrote is text, and the row keeps its width ----------
#
# #189: a `|` inside a Verdicts cell makes the row carry more cells than the
# header declares, every renderer drops the surplus, and everything from that
# character on is invisible in the rendered record while surviving in the raw
# file. Measured on work item 1788691941 round 1 -- six cells against a
# five-column header, and both paste-ready fixtures the round commissioned
# invisible. The sweep over this repository's 125 committed records found
# eight such rows; every one of them has its pipe inside a backtick code
# span, and one of the eight has it in a column that is not the last.


def cells_under(text, heading, n):
    """The n-th body row of a record table, read the way every reader reads
    it: through the shared splitter, which unescapes `\\|`."""
    reader = reader_module()
    rows = rows_of(text, heading)
    return [reader.visible(c) for c in reader.split_row(rows[2 + n])]


def test_a_bare_pipe_in_a_grounds_cell_keeps_the_row_at_its_header_width(repo):
    """The last column is free text, and a bare `|` in it used to split the
    row. The record's row has as many cells as its header, and the cell
    renders the pipe the reviewer wrote."""
    declared(repo)
    grounds = "the augmented assignment reads a |= b, not a or b"
    row = f"| 🔴 1 | the parser drops a row | `f.py:1` | open | {grounds} |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 5, rows_of(text, "## Verdicts")
    assert cells[4] == grounds


def test_a_pipe_inside_a_code_span_stays_in_its_own_column(repo):
    """The probes table's first column is a command, and a command has a
    pipe in it. Folding the surplus into the last column would move half the
    command into `Result`; a `|` inside a code span is the reviewer's own
    markup saying it is text."""
    declared(repo)
    ran = "reviewer: `grep -c '^| L'` on the fragment"
    probes = f"| {ran} | 10 rows |\n"
    code, out, text = generate(repo, report_text=report(probes=probes))
    assert code == 0, out
    cells = cells_under(text, "## Executed probes", 0)
    assert len(cells) == 2, rows_of(text, "## Executed probes")
    assert cells[0] == ran
    assert cells[1] == "10 rows"


def test_a_pipe_in_the_deferred_table_keeps_its_width(repo):
    """Every table the record copies, not the Verdicts table alone."""
    declared(repo)
    who = "the CI leg, which reads `a | b`"
    deferred = f"| the windows leg | `overview.md` | {who} |\n"
    code, out, text = generate(repo, report_text=report(deferred=deferred))
    assert code == 0, out
    cells = cells_under(text, "## Deferred", 0)
    assert len(cells) == 3, rows_of(text, "## Deferred")
    assert cells[2] == who


def test_an_escaped_pipe_the_reviewer_wrote_is_not_doubled(repo):
    """A reviewer who already escaped the pipe gets one backslash back, not
    two: the copy unescapes and re-escapes, and the round trip is the
    identity.

    **Green on the base as well, and deliberately so.** The base copied the
    row verbatim, which is also correct for an already-escaped pipe, so this
    pins the fix rather than a defect. It is seen red by mutation instead —
    dropping `split_cells`' unescape doubles the backslash."""
    declared(repo)
    row = "| 🔴 1 | a \\| b | `f.py:1` | open | executed |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    raw = rows_of(text, "## Verdicts")[2]
    assert "\\\\|" not in raw, raw
    assert cells_under(text, "## Verdicts", 0)[1] == "a | b"


def test_the_plain_reading_is_the_readers_own(repo):
    """`split_cells` with both knobs off has to be `reader.split_row`, or a
    cell the generator composes is one the pull-request check reads
    differently. Asserted over the shapes the two could disagree about:
    escapes, an empty last cell, a missing closing pipe, a line that is not
    a row at all."""
    generator, reader = generator_module(), reader_module()
    for line in (
        "| a | b |",
        "| a | b",
        "| a | |",
        "|",
        "| a \\| b | c |",
        "| a | b \\|",
        "| `x | y` | z |",
        "|---|---|",
        "  | a | b |  ",
        "not a row",
        "",
    ):
        assert generator.split_cells(line) == reader.split_row(line), line


def test_a_pipe_in_a_column_that_is_not_the_last_stays_there(repo):
    """The eighth of the eight over-wide rows this repository has written:
    `Contract changes | none` quoted in the FINDING column. Folding the
    surplus into the last column would put the location in the verdict cell,
    which `chain_check` reads."""
    declared(repo)
    finding = "the cell reads `Contract changes | none`"
    row = f"| 🔴 1 | {finding} | `f.py:1` | open | executed |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 5, rows_of(text, "## Verdicts")
    assert cells[1] == finding
    assert cells[2] == "`f.py:1`"
    assert cells[3] == "open"


def test_a_bare_pipe_before_the_last_column_keeps_its_text(repo):
    """The stated limit, pinned so it is a decision and not a surprise: a
    bare `|` outside a code span cannot be placed, so the rest of the row
    lands in the last column. Nothing is dropped, which is the whole of what
    this buys."""
    declared(repo)
    row = "| 🔴 1 | a | b | `f.py:1` | open | executed |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 5, rows_of(text, "## Verdicts")
    assert cells[4] == "open | executed"


# --- the paste-ready fix reaches the record ----------------------------------
#
# #187: the findings format spends four paragraphs requiring a paste-ready fix
# for every 🔴/🟡, and `new` copied the tables and dropped everything else, so
# not one of those blocks reached the file the fix pass is told to open
# instead of the report. Measured on work item 1788686494 round 1 -- a
# 162-line report with three fenced snippets became an 80-line record with
# none of them, and the fix pass said so unprompted and rebuilt all three,
# getting its first reproduction wrong. Measured again five times on the
# branch merged at `bc123aa`: a 264-line report, an 82-line record, and
# `grep -c '```'` answering 0.
#
# The mechanism is `fenced_after`, which the file has carried since #161 for
# this exact loss one section over. It is now called for a second heading.

ONE_FIX = (
    "```python\nif requester != owner:   # NAME NOT IN TREE\n    raise Error\n```\n"
)
OTHER_FIX = "```python\ncells = row_cells(reader, line, width)\n```\n"


def paste_ready(text):
    """The record's paste-ready section as raw lines, fences included."""
    body = text.split("## Paste-ready fixes", 1)[1]
    return body.split("\n## ", 1)[0]


def test_a_paste_ready_fix_reaches_the_record(repo):
    """The block lands in the record verbatim, fence and marked name intact.
    Before this, the record's only durable home for a fix was a Grounds
    cell -- which is a single line, and which #189 then truncated."""
    declared(repo)
    code, out, text = generate(repo, report_text=report(fixes=ONE_FIX))
    assert code == 0, out
    assert ONE_FIX.strip() in paste_ready(text), text


def test_two_paste_ready_fixes_stay_apart_and_in_the_reviewers_order(repo):
    """One entry per finding, and the reviewer's order is the fix pass's
    agenda order."""
    declared(repo)
    both = f"For 🔴 1:\n\n{ONE_FIX}\nFor 🟡 2:\n\n{OTHER_FIX}"
    code, out, text = generate(repo, report_text=report(fixes=both))
    assert code == 0, out
    section = paste_ready(text)
    assert ONE_FIX.strip() in section, text
    assert OTHER_FIX.strip() in section, text
    assert section.index(ONE_FIX.strip()) < section.index(OTHER_FIX.strip())


def test_prose_under_the_paste_ready_heading_stays_in_the_report(repo):
    """A fence is copied whole and nothing else of the section is. Prose
    nobody parses in a file `chain_check.py` reads is what `plan.md` refused
    when it turned down keeping the report verbatim."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(fixes=f"This paragraph explains it.\n\n{ONE_FIX}")
    )
    assert code == 0, out
    assert "This paragraph explains it" not in text, text
    assert ONE_FIX.strip() in paste_ready(text)


def test_a_report_with_no_paste_ready_fix_is_still_a_record(repo):
    """The empty arm is a scenario, not an edge case: a verifying round that
    opens nothing writes no fix, and the record still has to be written. The
    section says what the generator observed -- that the report carried
    none -- rather than claiming none was needed."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(verdicts=CLOSED_ROW, needs="no", fixes=None)
    )
    assert code == 0, out
    assert generator_module().NO_PASTE_READY in paste_ready(text), text


def test_an_empty_paste_ready_section_says_the_report_carried_none(repo):
    """The heading written with only prose under it lands on the same
    sentence: what reaches the record is what a fence carried, and there
    was no fence."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(fixes="Described, not shown.\n")
    )
    assert code == 0, out
    assert generator_module().NO_PASTE_READY in paste_ready(text), text


def test_an_unclosed_fence_under_the_paste_ready_heading_is_refused(repo):
    """The same refusal the probes section already carries: an open fence
    copied as it stands blanks every section below it in the record, and the
    record is written before any reader gets to say so.

    **Green on the base as well, and deliberately so.** `swallowed` asks the
    never-closed question over the WHOLE report, so an unclosed fence under a
    heading the base did not read was already refused. What this pins is that
    the new section inherits that guard rather than needing one of its own;
    the shape the section really does add is the comment-hidden opener, which
    is the case below it."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(fixes="```python\ndef helper(a):\n    return a\n")
    )
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert "never closed" in out


def test_a_fence_opened_inside_a_comment_under_the_paste_ready_heading(repo):
    """The second text, for the second section `fenced_after` is called on.
    `swallowed` reads the report with its comments stripped and this copy
    reads it as written, so an opener a comment hides is absent from the
    report-wide check and an opener to the copy. Without the verbatim raise
    the record is written carrying an open fence, and every section below it
    is gone to every reader."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(fixes=ONE_FIX + "\n" + COMMENTED_OPENER)
    )
    assert code == 2, out
    assert text is None, "a refusal writes no record"
    assert generator_module().PASTE_READY in out, out
    assert "never closed" in out


def test_the_reviewer_is_told_where_the_paste_ready_fixes_go():
    """A heading the generator extracts from and no reviewer is told to write
    is a section that arrives empty every round — which is #187 again with an
    extra step. The heading is read out of the generator, so the two carriers
    cannot drift, and it is looked for in the three places a reviewer, a
    record and a reader meet it."""
    generator = generator_module()
    heading = generator.PASTE_READY
    # Round 1's 🟡 7: each assertion names the PLACE its document owes, not
    # the region the heading may stand anywhere inside. Measured — a
    # presence-in-a-region pin passed the heading moving out of the reviewer's
    # fenced contract into prose, the section moving to the end of the
    # template, and the protocol's row moving out of the field table.
    #
    # 1. warden.md: inside a fenced block of §Report, which IS the reviewer's
    #    output contract. §Report is the file's last section, so a slice of it
    #    is the whole tail.
    body = read("agents", "warden.md")
    section = body[body.index("\n## Report\n") :]
    blocks = re.findall(r"\n```[^\n]*\n(.*?\n)```\n", section, re.S)
    assert any(f"\n{heading}\n" in f"\n{block}" for block in blocks), (
        "the heading has to stand in a fenced block of the reviewer's output "
        "contract, not only in the prose around it"
    )
    skill = read("skills", "code-review", "SKILL.md")
    findings = skill[skill.index("\n## Findings format\n") :]
    assert f"`{heading}`" in findings, (
        "the findings format is where a reviewer reads what a paste-ready "
        "fix is; it has to say where the fix goes"
    )
    # 2. sdd-round.md: in the record's own section order, which `build`
    #    writes. A section moved to the end of the template describes a record
    #    nobody gets.
    order = re.findall(r"(?m)^##\s.*$", read("templates", "sdd-round.md"))
    assert order.index(heading) == order.index(generator.VERDICTS) + 1, order
    assert order.index(generator.PROBES) == order.index(heading) + 1, order
    # 3. review-handoff-protocol.md: a row of the field table, which is the
    #    table of what a record carries — not the prose below it.
    proto = read("docs", "review-handoff-protocol.md")
    table = proto[proto.index("\n| Field | Required | Content |\n") :]
    assert f"| {heading.lstrip('# ')} |" in table[: table.index("\n#### ")], table


def test_the_reviewer_is_not_told_the_report_is_read_for_tables_alone():
    """The sentence that has to change with the section, pinned so the next
    edit does not take it back. `agents/warden.md` told the reviewer the
    generator *reads nothing else of the report*, which was true when the
    fenced blocks reached no file and is what #187 measured.

    Round 1's ⬜ 9: the replacement said *reads no other prose*, and that is
    false in the other direction — `terminal_value` reads `Needs a fix:` and
    `Loses a record or crashes:` off prose lines, which the same section
    names four paragraphs later. Both spellings are refused here, because a
    reviewer who believes either one writes a report the generator cannot
    read."""
    body = read("agents", "warden.md")
    report = body[body.index("\n## Report\n") :]
    flat = " ".join(report.split())
    for false_claim in ("reads nothing else of the report", "reads no other prose"):
        assert false_claim not in flat, (
            f"`{false_claim}` is false: the generator reads the fenced blocks "
            "under two headings and the two terminal lines off prose"
        )
    chain = check_module()
    for label in (chain.NEEDS, chain.FLOOR):
        assert f"{label}:" in flat, (
            f"the section has to keep naming `{label}:` — it is one of the "
            "prose lines the generator does read"
        )


# --- the two texts must agree about what a `|` is ----------------------------
#
# Round 1's 🔴 1 and 🟡 2. `table_body` counts a row's columns on `lines`,
# where `strip_comments` has already blanked the HTML comments; `copied_row`
# rebuilds the row from `raw`, where they stand. Where the two texts disagree
# about one character, the record loses a column — and it loses it at exactly
# header width, so nothing downstream complains and the Location ends up in
# the Verdict cell `chain_check` reads. That is the placement `plan.md` names
# as its reason for refusing the fold, produced by the fix that refused it.


def verdict_row_as_written(text, n=0):
    """The n-th verdict row of a record as the FILE holds it.

    `rows_of` goes through `readable`, which blanks comment content — that is
    the right view for what a checker reads and the wrong one for asking
    whether the reviewer's own text survived the copy. Both are asserted
    below, because the defect showed up in one and the repair has to hold in
    both."""
    body = text.split("## Verdicts", 1)[1].split("\n## ", 1)[0]
    rows = [ln.strip() for ln in body.splitlines() if ln.strip().startswith("|")]
    return rows[2 + n]


def test_a_pipe_inside_an_html_comment_is_not_a_column_break(repo):
    """🔴 1. A comment a reviewer wrote inside a cell is theirs to keep —
    `table_of` copies `raw` for exactly that reason — so the copy has to read
    the comment the way the column count did."""
    declared(repo)
    finding = "a <!-- read | again --> b"
    row = f"| 🔴 1 | {finding} | `f.py:1` | open | executed |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    written = verdict_row_as_written(text)
    assert "<!-- read \\| again -->" in written, written
    assert finding in written.replace("\\|", "|"), written
    # The width a RENDERER sees, which is where the loss lives: reading the
    # record back through `readable` strips the comment before it counts, so
    # the row looks five wide even while it renders as six.
    assert len(reader_module().split_row(written)) == 5, written
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 5, rows_of(text, "## Verdicts")
    assert cells[2] == "`f.py:1`"
    assert cells[3] == "open", "the Location must not stand in the Verdict cell"
    assert cells[4] == "executed"


def test_two_html_comments_in_one_row_keep_their_columns(repo):
    """The same defect twice in one row. One comment cost a column; two cost
    two, and the record came out narrower than its own header — a row the
    generator wrote and its own checker will not read."""
    declared(repo)
    row = "| 🔴 1 | a <!-- p | q --> b | `f.py:1` | <!-- r | s --> open | executed |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    row_as_written = verdict_row_as_written(text)
    assert len(reader_module().split_row(row_as_written)) == 5, row_as_written
    written = row_as_written.replace("\\|", "|")
    assert "<!-- p | q -->" in written, written
    assert "<!-- r | s -->" in written, written
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 5, rows_of(text, "## Verdicts")
    assert cells[2] == "`f.py:1`"
    assert cells[3] == "open", "the Location must not stand in the Verdict cell"
    assert cells[4] == "executed"


def test_a_row_carrying_a_span_pipe_and_a_bare_pipe_keeps_its_columns(repo):
    """🟡 2. Either pipe alone is handled — the code-span reading takes the
    first, the capped plain reading takes the second. Together, the span
    reading is over the width and the plain cap re-splits the reviewer's code
    span, shifting every later column left. The cap has to be taken with the
    span reading still on."""
    declared(repo)
    finding = "the cell reads `Contract changes | none`"
    grounds = "executed; a |= b"
    row = f"| 🔴 1 | {finding} | `f.py:1` | open | {grounds} |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 5, rows_of(text, "## Verdicts")
    assert cells[1] == finding
    assert cells[2] == "`f.py:1`"
    assert cells[3] == "open", "the Location must not stand in the Verdict cell"
    assert cells[4] == grounds


def test_an_unbalanced_backtick_run_still_reads_a_comment_as_text(repo):
    """The last reading, which nothing observed until this case.

    An unbalanced backtick run swallows every break, so the code-span
    reading comes in under the width and the plain cap is the answer. That
    reading has to read an HTML comment the same way the others do — with
    a comment pipe and a bare surplus pipe in the same row, dropping it puts
    the Location in the Verdict cell exactly as round 1's 🔴 1 did, in the
    one path 🔴 1's own cases never reach."""
    declared(repo)
    finding = "a `b <!-- p | q --> c"
    grounds = "executed; x | y"
    row = f"| 🔴 1 | {finding} | `f.py:1` | open | {grounds} |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 5, rows_of(text, "## Verdicts")
    assert cells[2] == "`f.py:1`"
    assert cells[3] == "open", "the Location must not stand in the Verdict cell"
    assert cells[4] == grounds
    assert "<!-- p \\| q -->" in verdict_row_as_written(text)


def test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one(repo):
    """The first reading, which nothing observed until this case.

    A row missing a column and carrying a comment pipe is the one shape
    where the reader's own splitter and the raw reading disagree BELOW the
    header width: `split_row` counts the comment's pipe and reports a full
    row, `table_body` counted the stripped text and saw a short one. Copying
    the first would invent a column — the record would look complete with
    the Finding's tail standing in `Location` — where the reviewer in fact
    left one out."""
    declared(repo)
    row = "| 🔴 1 | a <!-- p | q --> b | `f.py:1` | open |\n"
    code, out, text = generate(repo, report_text=report(verdicts=row))
    assert code == 0, out
    # The reader's view is four cells either way -- it strips the comment
    # before it counts -- so what separates the two readings is the ESCAPE,
    # which is what a renderer sees. Escaped, the row renders at four
    # columns, which is the number `table_body` counted; unescaped it
    # renders at five, one of them invented from a comment.
    written = verdict_row_as_written(text)
    assert "<!-- p \\| q -->" in written, written
    cells = cells_under(text, "## Verdicts", 0)
    assert len(cells) == 4, rows_of(text, "## Verdicts")
    assert cells[2] == "`f.py:1`"
    assert cells[3] == "open"


def test_a_fence_quoting_the_optional_heading_is_kept_when_it_is_absent(repo):
    """Round 1's 🟡 3. `## Paste-ready fixes` is the first member of the
    guard's heading list whose section is OPTIONAL — a round that opened
    nothing needing a fix is told to leave it out. The guard's premise,
    hidden AND absent means swallowed, holds only where the report must
    carry the section: here absence is a legitimate state, so the refusal
    reports a loss that did not happen and writes no record.

    It is also the shape that stops this tool during its own review rounds.
    A reviewer of the record generator pastes record-shaped blocks, headings
    and all, and a round that opened nothing is exactly the round whose
    report quotes the empty section's own sentence. `seal/ledger.md` F3 names
    that scenario as what the guard must never do."""
    declared(repo)
    quoted = (
        f"```\n{generator_module().PASTE_READY}\n\n"
        f"{generator_module().NO_PASTE_READY}\n```\n"
    )
    code, out, text = generate(
        repo,
        report_text=report(
            verdicts=CLOSED_ROW, needs="no", probes=PROBE_ROW + "\n" + quoted
        ),
    )
    assert code == 0, out
    assert generator_module().NO_PASTE_READY in paste_ready(text), text
    probes = text.split("## Executed probes", 1)[1].split("## Inherited", 1)[0]
    assert quoted.strip() in probes, "the quoted block is copied as it always was"


def test_the_empty_arms_sentence_is_the_generators_constant():
    """Round 1's 🟡 6. The two empty-arm cases read `NO_PASTE_READY` out of
    the module on BOTH sides of their comparison, so they hold whatever it
    says — rewording it to `none was needed` left the whole module green,
    and that reading is the one thing the sentence exists not to say.

    Three documents quote it word for word, and the ledger fragment's R2
    calls it a load-bearing wording rather than a default string. This is
    what makes that true: one constant, four carriers."""
    sentence = generator_module().NO_PASTE_READY
    assert "report" in sentence, (
        "the sentence names what was OBSERVED — that the report carried no "
        "fence — and never that no fix was needed, which nothing can know"
    )
    for parts in (
        ("agents", "warden.md"),
        ("templates", "sdd-round.md"),
        ("docs", "review-handoff-protocol.md"),
    ):
        assert sentence in " ".join(read(*parts).split()), parts


def test_a_paste_ready_fence_carrying_a_table_is_not_read_as_hidden_rows(repo):
    """`swallowed`'s ROW loop reads `REPORT_TABLES` and not `READ_HEADINGS`,
    which is round 1's 🟡 3 one level down and was pinned by nothing.

    The row half asks whether a section's rows stand ONLY inside a fence. A
    section with no table of its own answers that vacuously, so widening the
    loop to the optional section makes any fenced fix containing a markdown
    table read as hidden rows — and this repository's own paste-ready fixes
    carry tables. Measured before this case: widening the row loop left all
    78 cases green."""
    declared(repo)
    fix = (
        "```markdown\n"
        "| Finding | Where it went | Who answers it |\n"
        "|---|---|---|\n"
        "| the windows leg | `overview.md` | the CI leg |\n"
        "```\n"
    )
    code, out, text = generate(repo, report_text=report(fixes=fix))
    assert code == 0, out
    assert fix.strip() in paste_ready(text), text


# --- the bound the next round is under (#207) --------------------------------
#
# `docs/review-chain-spec.md` bounds a run one step earlier than the cap: after
# a record whose floor row reads `no`, at most one later record may close on a
# fix, and the record that reads its fixes ends the run whatever it finds.
# `chain_check.py` enforces that at the broad gate, after every round has
# already been spawned. `new` says it as it writes the record, which is the
# moment the orchestrator decides whether to spawn again.

FIXED_ROW = "| 🟡 2 | round 1's finding | `f.py:1` | fixed `abc1234` | executed |\n"


def bound_of(out):
    """The bound line `new` printed, or None."""
    for line in out.splitlines():
        if line.startswith("round-record: ") and (
            "ends the run" in line or "reopening remains" in line
        ):
            return line
    return None


def test_a_first_round_says_nothing_about_the_bound(repo):
    """There is no earlier record, so there is no floor and no bound.

    A sentence invented for a state that has none is worse than silence: the
    cap still governs here, and the cap is not this line's subject.
    """
    declared(repo)
    code, out, _ = generate(repo)
    assert code == 0, out
    assert bound_of(out) is None, out


def test_a_run_whose_floor_is_not_met_says_nothing_about_the_bound(repo):
    declared(repo)
    code, out, _ = generate(repo, report_text=report(floor="yes — a record leaves"))
    assert code == 0, out
    commit(repo, "round 1")
    _code, out, text = generate(repo, n=2, report_text=report(verdicts=CLOSED_ROW))
    assert text is not None, out
    assert bound_of(out) is None, out


def test_a_record_after_the_floor_with_no_fix_says_one_reopening_remains(repo):
    declared(repo)
    code, out, _ = generate(repo, report_text=report(floor="no"))
    assert code == 0, out
    commit(repo, "round 1")
    _code, out, text = generate(repo, n=2, report_text=report(verdicts=CLOSED_ROW))
    assert text is not None, out
    line = bound_of(out)
    assert line is not None, out
    assert "one reopening remains" in line
    assert "round-1.md" in line


def test_a_record_reading_the_reopenings_fixes_says_it_ends_the_run(repo):
    """Round 1 met the floor, round 2 closed on a fix, and round 3 is the
    record that reads those fixes — so it ends the run whatever it finds."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(floor="no"))
    assert code == 0, out
    commit(repo, "round 1")
    _code, out, text = generate(repo, n=2, report_text=report(verdicts=FIXED_ROW))
    assert text is not None, out
    commit(repo, "round 2")
    _code, out, text = generate(repo, n=3, report_text=report(verdicts=CLOSED_ROW))
    assert text is not None, out
    line = bound_of(out)
    assert line is not None, out
    assert "this record ends the run" in line
    assert "round-1.md" in line and "round-2.md" in line
    # The exit the refusal at the gate names, in the one spelling both carry.
    assert check_module().CAPPED_EXIT in line


def test_the_floor_record_is_the_earliest_and_not_the_latest(repo):
    """The count keyed to the LATEST record that met the floor is unbounded by
    construction — every record it stops at is itself a record that met the
    floor, so the count restarts there. `chain_check.stopping_floor` records
    that failure in its own docstring, and the writer's side must not re-make
    it.

    Round 1 met the floor, round 2 closed on a fix, round 3 met the floor
    again. Writing round 4: from the earliest, one later record has closed on
    a fix and this one ends the run. From the latest, nothing has, and the run
    reads as having a reopening left.
    """
    generator = generator_module()
    reader = reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_for_bounds")
    rounds = repo / ROUNDS
    rounds.mkdir(parents=True, exist_ok=True)

    def record(n, floor, verdicts):
        (rounds / f"round-{n}.md").write_text(
            f"# item — review round {n}\n\n"
            "| Field | Value |\n|---|---|\n"
            f"| Loses a record or crashes | {floor} |\n\n"
            f"## Verdicts\n\n{VERDICT_HEADER}{verdicts}\n",
            encoding="utf-8",
        )

    record(1, "no", CLOSED_ROW)
    record(2, "yes — a record leaves", FIXED_ROW)
    record(3, "no", CLOSED_ROW)

    floor_at, fixes, counted, running, counted_at = generator.floor_and_fixes(
        reader, generator.earlier_records(routing, str(rounds), 4)
    )
    assert os.path.basename(floor_at) == "round-1.md"
    assert [os.path.basename(p) for p in fixes] == ["round-2.md"]
    # Round 1's count walk stopped at round 2, which closed on a fix. Round
    # 3's floor row reads `no` and starts a walk of its own, but nothing
    # follows it, so that walk has spent nothing. `counted` reports the
    # firing walk and there is none, so the two values cannot disagree.
    assert (counted, running, counted_at) == (0, False, None)

    line = generator.bound_line(reader, routing, str(rounds), 4)
    assert "this record ends the run" in line, line


def test_a_record_that_cannot_be_read_is_not_the_floor_record(repo):
    """`stopping_floor` reports an unreadable record and a malformed row at
    the gate. A second reader inventing a sentence about either here would be
    the failure #207 is about, one file over."""
    generator = generator_module()
    reader = reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_for_bounds_2")
    rounds = repo / ROUNDS
    rounds.mkdir(parents=True, exist_ok=True)
    (rounds / "round-1.md").write_text(
        "# item — review round 1\n\n| Field | Value |\n|---|---|\n"
        "| Loses a record or crashes | possibly |\n",
        encoding="utf-8",
    )
    assert generator.bound_line(reader, routing, str(rounds), 2) is None


# --- the count walk, and what the gate grandfathers (round 1, 🟡 2, 8, 12) ---
#
# `chain_check.stopping_floor` runs TWO walks over the records after the
# floor. The reopening walk counts fix-closing records wherever they sit; the
# COUNT walk counts every later record up to and including the first that
# reopened or closed on a fix, and refuses a second counted record. Reading
# only the first invited a round the gate refuses.


def chain_of(repo, name, *records):
    """A work item directory holding hand-written records, and its rounds path.

    Direct-call rather than `generate`, because what these cases vary is the
    work item's NAME — the second the grandfathering reads — and `generate`
    writes into one item.
    """
    rounds = repo / "seal" / "specs" / name / "rounds"
    rounds.mkdir(parents=True, exist_ok=True)
    for n, floor, needs, verdicts in records:
        (rounds / f"round-{n}.md").write_text(
            f"# {name} — review round {n}\n\n"
            "| Field | Value |\n|---|---|\n"
            f"| Needs a fix | {needs} |\n"
            f"| Loses a record or crashes | {floor} |\n\n"
            f"## Verdicts\n\n{VERDICT_HEADER}{verdicts}\n",
            encoding="utf-8",
        )
    return rounds


LATE = "1799000000-a-later-work-item"


def test_two_quiet_rounds_after_the_floor_end_the_run(repo):
    """The defect #207's own fix carried (round 1, 🔴 2).

    Round 1 met the floor and round 2 was quiet — it neither reopened the run
    nor closed on a fix. The gate's count walk then counts round 2 AND round
    3 and refuses at two, so round 3 is a round it will not accept. Reading
    the reopening walk alone, `new` printed `one reopening remains` at round
    2 and the session spawned the round the gate was about to refuse. That is
    the same *round N of a cap of five* mistake #207 exists to end, made by
    the line written to end it.
    """
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_count_walk")
    rounds = chain_of(
        repo,
        LATE,
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", CLOSED_ROW),
    )
    line = generator.bound_line(reader, routing, str(rounds), 3)
    assert line is not None, "the count walk says round 3 is over the bound"
    assert "this record ends the run" in line, line
    assert "reaches 2" in line, line
    assert check_module().CAPPED_EXIT in line, line


def test_an_intermediate_floor_record_starts_a_count_walk_of_its_own(repo):
    """`stopping_floor` is called on EVERY record, so a second record whose
    floor row reads `no` starts a count walk of its own (round 2, 🟡 1).

    Round 1 met the floor and reopened, round 2 met the floor and reopened,
    round 3 was quiet. Round 1's own walk stopped at round 2, so reading the
    earliest floor record alone found nothing running and printed `one
    reopening remains` — while the gate refused round 4 at `round-2.md`,
    whose walk counts round 3 and then this one. That is round 1's 🔴 2 one
    floor record over.
    """
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_second_floor")
    rounds = chain_of(
        repo,
        LATE,
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "yes — 🟡 3", CLOSED_ROW),
        (3, "no", "no", CLOSED_ROW),
    )
    line = generator.bound_line(reader, routing, str(rounds), 4)
    assert line is not None and "this record ends the run" in line, line
    # The record the firing walk STARTED from, not the earliest floor record:
    # a sentence naming round-1.md would send the reader to a walk that
    # stopped, which is the one place the message can be checked.
    assert "round-2.md" in line and "round-1.md" not in line, line
    assert "reaches 2" in line, line


def test_the_count_walks_message_says_records_when_it_counted_two(repo):
    """The plural branch of the count-walk line, which no case reached
    (round 2, ⬜ 6). §14 asks the printed line to be pinned, and `1 records`
    is what an unpinned plural branch ships."""
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_plural")
    rounds = chain_of(
        repo,
        LATE,
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", CLOSED_ROW),
        (3, "no", "no", CLOSED_ROW),
    )
    line = generator.bound_line(reader, routing, str(rounds), 4)
    assert line is not None, line
    assert "the 2 records after it" in line, line
    assert "reaches 3" in line, line


def test_a_round_that_reopened_without_writing_fixes_stops_the_count(repo):
    """The gate's count walk stops AT the record that reopened, so the record
    being written now is not counted and the gate allows it.

    `Needs a fix: yes` with every verdict `answered` is the sequence where
    the two walks come apart: nothing was written for a later round to read,
    so the reopening walk still finds no fix — and the count walk has already
    stopped, so nothing here ends the run. Counting it anyway would print
    `ends the run` over a round the gate is about to permit.
    """
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_count_stop")
    rounds = chain_of(
        repo,
        LATE,
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "yes — 🟡 3", CLOSED_ROW),
    )
    line = generator.bound_line(reader, routing, str(rounds), 3)
    assert line is not None, line
    assert "one reopening remains" in line, line


def test_the_reopening_named_is_the_first_record_that_closed_on_a_fix(repo):
    """The reopening walk never stops, so a run that closed on a fix twice
    has two paths in `fixes` — and the one the line names is the reopening
    this floor allowed, which is the FIRST. Naming the last would put the
    record the gate refuses in the sentence explaining why the run is over.
    """
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_two_fixes")
    rounds = chain_of(
        repo,
        LATE,
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", FIXED_ROW),
        (3, "no", "no", FIXED_ROW),
    )
    line = generator.bound_line(reader, routing, str(rounds), 4)
    assert "this record ends the run" in line, line
    assert "round-2.md" in line and "round-3.md" not in line, line


def test_a_work_item_older_than_the_count_rule_prints_nothing(repo):
    """Below `FLOOR_FROM` the gate prints a notice instead of failing, so
    there is no bound for this line to state. Declaring the run capped where
    the gate only notices is the finding (round 1, 🟡 8)."""
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_old_item")
    assert check_module().FLOOR_FROM > 1788400000
    rounds = chain_of(
        repo,
        "1788400000-an-early-item",
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", CLOSED_ROW),
    )
    assert generator.bound_line(reader, routing, str(rounds), 3) is None


def test_the_two_walks_are_grandfathered_against_different_constants(repo):
    """`1788500000-an-item` sits between `FLOOR_FROM` and `REOPEN_FROM`.

    The gate REFUSES its count walk there and only notices its reopening
    walk, so one guard covering both would have silenced a bound that is
    really enforced.
    """
    check = check_module()
    assert check.FLOOR_FROM < 1788500000 < check.REOPEN_FROM
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check.ROUTING, "specseal_routing_between")

    quiet = chain_of(
        repo,
        "1788500000-an-item",
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", CLOSED_ROW),
    )
    line = generator.bound_line(reader, routing, str(quiet), 3)
    assert line is not None and "this record ends the run" in line, line

    fixed = chain_of(
        repo,
        "1788500001-another-item",
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", FIXED_ROW),
    )
    assert generator.bound_line(reader, routing, str(fixed), 3) is None


def test_a_work_item_with_no_epoch_in_its_name_prints_nothing(repo):
    """`item_began` answers None for a repository that names its work items
    some other way, and the gate grandfathers every such record.

    Both branches, because they are guarded separately: with only the floor
    record on disk the line would be `one reopening remains`, and with a
    quiet round after it the line would be the count walk's.
    """
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_no_epoch")
    alone = chain_of(repo, "my-work-item", (1, "no", "yes — 🔴 1", CLOSED_ROW))
    assert generator.bound_line(reader, routing, str(alone), 2) is None
    quiet = chain_of(
        repo,
        "another-work-item",
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", CLOSED_ROW),
    )
    assert generator.bound_line(reader, routing, str(quiet), 3) is None


def test_an_unreadable_record_answers_nothing_rather_than_no_fix(repo, monkeypatch):
    """A record dropped from the fix walk alone reads as a run that still has
    its reopening — the permissive direction, and against what the unit's own
    docstring says it does (round 1, 🟡 12).

    Constructed by refusing the read rather than by `chmod 000`, which is
    nothing to root and sets only a read-only flag on Windows —
    `test_gates_do_not_fail_open.py` makes the same choice for the same
    reason.
    """
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_unreadable")
    rounds = chain_of(
        repo,
        LATE,
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "no", FIXED_ROW),
    )
    assert generator.bound_line(reader, routing, str(rounds), 3) is not None

    real = open

    def refuse(path, *args, **kwargs):
        if str(path).endswith("round-2.md"):
            raise PermissionError(13, "permission denied")
        return real(path, *args, **kwargs)

    monkeypatch.setattr(generator, "open", refuse, raising=False)
    assert generator.bound_line(reader, routing, str(rounds), 3) is None
