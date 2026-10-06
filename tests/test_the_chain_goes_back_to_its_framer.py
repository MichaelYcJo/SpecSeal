"""The gate counts a fix of a fix per run, and holds the resumption to a
redrawn frame (#823).

`round_record.py new` writes `Fix of a fix` (`tests/test_a_fix_of_a_fix_is_counted.py`).
This is the other half: `chain_check.fix_of_a_fix` reads the row on every
record, counts the declarations per run, and refuses a run that went past the
stop or resumed without a `Reframed … after round <N>.` line at the foot of
`spec.md`. The floor's walks stop at the same boundary, so the redesign's own
rounds are not later records of the run that stopped.

S8 to S11 of the work item's `spec.md`. Each refusal was seen red before its
arm existed: the records here are hand-written, so every case runs against a
tree whose only variable is the cell or the line it is about.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys

import pytest
from conftest import cutoff_item_is_traceable

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, "skills", "code-review", "scripts")
CHECK = os.path.join(SCRIPTS, "chain_check.py")
GENERATOR = os.path.join(SCRIPTS, "round_record.py")

ITEM = "seal/specs/1799000000-a-later-work-item"

FRAMED = "Framed 2026-10-06 by framer, before the build."
REFRAMED = "Reframed 2026-10-07 by framer, after round 3."
FIRST = "first — 🟡 1 at f.py#x, a unit round-1's fixes changed"
SECOND = (
    "second — 🟡 1 at f.py#x, a unit round-2's fixes changed; "
    "the fix passes stop here and the work item goes back to its framer"
)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_module():
    return _load("specseal_chain_check_for_the_reframe", CHECK)


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
    d = tmp_path_factory.mktemp("reframe-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declaration(item, planning=None):
    rows = (
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )
    if planning is not None:
        rows += f"| Planning | {planning} |\n"
    return (
        f"# {os.path.basename(item)} — routing\n\n| Axis | Answer |\n|---|---|\n{rows}"
    )


def record(
    sha,
    fof="no",
    verdict="answered",
    checker="no fixes to check",
    floor="yes — a crash",
    needs="no",
):
    """A record every arm passes but the one each case is about. `fof=None`
    leaves the `Fix of a fix` row out. The floor defaults to `yes — <what>` so
    the floor's walks stay silent wherever a case is not about them."""
    fof_row = f"| Fix of a fix | {fof} |\n" if fof is not None else ""
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n"
        f"| Broad gate | {sha} against base |\n"
        f"| Fixes checked by | {checker} |\n"
        "| Fix range | none |\n"
        "| Contract changes | none |\n"
        "| Ran by | specseal:warden on a model |\n"
        "| New units | none |\n"
        f"{fof_row}"
        f"| Needs a fix | {needs} |\n"
        f"| Loses a record or crashes | {floor} |\n\n"
        "- [x] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| 🟡 1 | something | `f.py:1` | {verdict} | grounds |\n"
    )


def declared(repo, item, *bodies, planning=None, spec=None):
    """The declaration (and `spec.md`, `plan.md` where given), then one record
    per body, each in its own commit and each targeting the HEAD before it."""
    write(repo, f"{item}/routing.md", declaration(item, planning))
    if spec is not None:
        write(repo, f"{item}/spec.md", f"# a spec\n\nWhat it delivers.\n\n{spec}\n")
        write(
            repo,
            f"{item}/plan.md",
            "# a plan\n\nApproved 2026-10-06 by the repository owner, "
            "when `smith` was spawned.\n",
        )
    sha = commit(repo, "declare")
    for number, body in enumerate(bodies, start=1):
        write(repo, f"{item}/rounds/round-{number}.md", body(sha))
        sha = commit(repo, f"round {number}")
    return sha


def run(repo, draft=None):
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    if draft is not None:
        path = repo / "event.json"
        path.write_text(json.dumps({"pull_request": {"draft": draft}}), "utf-8")
        env["GITHUB_EVENT_PATH"] = str(path)
    r = subprocess.run(
        [sys.executable, CHECK, "--baseline", "base", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


def rec(**kwargs):
    return lambda sha: record(sha, **kwargs)


# A run that stopped at round 3, and the redesign's first record.
STOPPED = (
    rec(),
    rec(fof=FIRST),
    rec(fof=SECOND, verdict="deferred the frame"),
    rec(),
)


# --- S8, the gate on the row -----------------------------------------------


ABSENT = "no `| Fix of a fix | … |` row"


def test_an_absent_row_fails_at_the_cutoff(repo):
    """At `REFRAME_FROM` itself, so the case pins the boundary and not a
    number somewhere above it."""
    item = f"seal/specs/{check_module().REFRAME_FROM}-an-item"
    declared(repo, item, rec(fof=None))
    code, out = run(repo)
    assert code == 1, out
    assert ABSENT in out, out


@pytest.mark.parametrize(
    "item",
    ["seal/specs/{before}-an-earlier-item", "seal/specs/a-work-item-with-no-prefix"],
)
def test_an_absent_row_prints_before_the_cutoff(repo, item):
    item = item.format(before=check_module().REFRAME_FROM - 1)
    declared(repo, item, rec(fof=None))
    code, out = run(repo)
    assert code == 0, out
    assert ABSENT in out and "began before the rule landed" in out, out


@pytest.mark.parametrize("cell", ["", "first", "second", "first —", "fourth — x"])
@pytest.mark.parametrize(
    "item", [ITEM, "seal/specs/{before}-an-earlier-item"], ids=["after", "before"]
)
def test_a_row_that_is_none_of_the_three_fails_at_any_age(repo, cell, item):
    item = item.format(before=check_module().REFRAME_FROM - 1)
    declared(repo, item, rec(fof=cell))
    code, out = run(repo)
    assert code == 1, out
    assert "which is none of its three values" in out, out


def test_the_three_values_pass(repo):
    declared(repo, ITEM, *STOPPED, spec=f"{FRAMED}\n{REFRAMED}")
    code, out = run(repo)
    assert code == 0, out


# --- S9, the gate on the count ---------------------------------------------


def test_a_second_landing_written_as_first_fails(repo):
    declared(repo, ITEM, rec(), rec(fof=FIRST), rec(fof=FIRST))
    code, out = run(repo)
    assert code == 1, out
    assert "round-2.md already landed in this run, so the count says" in out, out
    assert "the work item goes back to its framer" in out, out


def test_a_third_landing_in_one_run_fails_naming_the_one_it_went_past(repo):
    declared(repo, ITEM, rec(), rec(fof=FIRST), rec(fof=FIRST), rec(fof=FIRST))
    code, out = run(repo)
    assert code == 1, out
    assert (
        "the third fix of a fix in one run, after round-2.md and round-3.md "
        "— the fix passes went past the stop at round-3.md"
    ) in out, out


def test_a_second_whose_verdicts_closed_on_a_fix_fails(repo):
    declared(
        repo,
        ITEM,
        rec(),
        rec(fof=FIRST),
        rec(fof=SECOND, verdict="**fixed** `deadbee`", checker="round-4"),
        rec(),
        spec=f"{FRAMED}\n{REFRAMED}",
    )
    _code, out = run(repo, draft=True)
    assert "reads `second` and this record's verdicts closed on a fix" in out, out


ORPHAN = "and no earlier record of this run landed, so the count says `first`"
FIRST_OF_A_RUN = "on the first record of its run, which follows no fix pass of the run"


def test_a_second_with_no_earlier_landing_fails_and_does_not_cut_the_run(repo):
    """Round 1's ⬜ 2. An orphan `second` disagrees with its run; and since it
    does not cut the run, the record after it needs no reframe and is not
    read as a run's first record."""
    declared(repo, ITEM, rec(), rec(fof=SECOND), rec())
    code, out = run(repo)
    assert code == 1, out
    assert ORPHAN in out, out
    assert "carries no `Reframed" not in out, out


def test_a_landing_on_round_one_fails(repo):
    declared(repo, ITEM, rec(fof=FIRST), rec(fof=SECOND))
    code, out = run(repo)
    assert code == 1, out
    assert f"reads `{FIRST}` {FIRST_OF_A_RUN}" in out, out


def test_a_landing_on_the_first_record_after_a_stop_fails(repo):
    declared(repo, ITEM, *STOPPED[:3], rec(fof=FIRST), spec=f"{FRAMED}\n{REFRAMED}")
    code, out = run(repo)
    assert code == 1, out
    assert FIRST_OF_A_RUN in out, out
    assert out.count(FIRST_OF_A_RUN) == 1, out


def test_a_foot_that_does_not_end_with_the_mark_says_what_the_foot_may_end_on(repo):
    """Round 1's ⬜ 4, pinned (§14): a foot may end on `Reframed` lines, so the
    refusal names them rather than asking for the mark on the last line. An
    unfilled `Reframed … after round <N>.` reaches this sentence."""
    declared(
        repo,
        ITEM,
        rec(),
        planning="framer",
        spec=f"{FRAMED}\nReframed <date> by <who>, after round <N>.",
    )
    code, out = run(repo)
    assert code == 1, out
    assert (
        "The last non-empty line that is not a `Reframed <date> by <who>, after "
        "round <N>.` line — a reframe writes those UNDER the mark, with a round "
        "number — has to read `Framed <date> by <who>, before the build.`"
    ) in out, out


def test_a_record_after_a_second_needs_the_reframe(repo):
    declared(repo, ITEM, *STOPPED, spec=FRAMED)
    code, out = run(repo)
    assert code == 1, out
    assert (
        "round-3.md reads `second`, and this record comes after it while "
        f"{ITEM}/spec.md's foot carries no `Reframed <date> by <who>, after "
        "round 3.`"
    ) in out, out


def test_a_reframe_naming_another_round_does_not_permit_it(repo):
    declared(repo, ITEM, *STOPPED, spec=f"{FRAMED}\n{REFRAMED[:-2]}2.")
    code, out = run(repo)
    assert code == 1, out
    assert "carries no `Reframed <date> by <who>, after round 3.`" in out, out


def test_a_reframe_by_a_party_the_declaration_does_not_name_fails(repo):
    reframed = REFRAMED.replace("by framer", "by the session")
    declared(repo, ITEM, *STOPPED, planning="framer", spec=f"{FRAMED}\n{reframed}")
    code, out = run(repo)
    assert code == 1, out
    assert "The declaration and the reframe disagree" in out, out


def test_an_unfilled_reframe_line_fails(repo):
    reframed = "Reframed <date> by <who>, after round 3."
    declared(repo, ITEM, *STOPPED, planning="framer", spec=f"{FRAMED}\n{reframed}")
    code, out = run(repo)
    assert code == 1, out
    assert "the UNFILLED reframe line" in out, out


def test_a_reframe_the_declaration_names_passes(repo):
    declared(repo, ITEM, *STOPPED, planning="framer", spec=f"{FRAMED}\n{REFRAMED}")
    code, out = run(repo)
    assert code == 0, out


# --- S10, the walks stop at the boundary -----------------------------------


REOPENED_TWICE = "is the second later record whose verdicts closed on a fix"


def boundary(fof_at_three):
    """Floor `no` at round 2, the stop at round 3, and the redesign's rounds 4
    (closed on a fix) and 5 (its verifying round, closed on a fix too)."""
    fixed = "**fixed** `deadbee`"
    return (
        rec(verdict=fixed, checker="round-2", needs="yes — a crash"),
        rec(fof=FIRST, floor="no", verdict=fixed, checker="round-3", needs="yes — x"),
        rec(
            fof=fof_at_three, floor="no", verdict="deferred the frame", needs="yes — x"
        ),
        rec(floor="no", verdict=fixed, checker="round-5", needs="yes — y"),
        rec(
            floor="no",
            verdict=fixed,
            checker="nobody — the fixes are written and no round has opened them",
        ),
    )


def test_the_floor_does_not_reach_across_a_second(repo):
    declared(repo, ITEM, *boundary(SECOND), spec=f"{FRAMED}\n{REFRAMED}")
    _code, out = run(repo, draft=True)
    assert REOPENED_TWICE not in out, out


def test_without_the_second_the_same_tree_is_refused_by_the_floor(repo):
    """The red half of the case above: the stop is the only difference."""
    declared(repo, ITEM, *boundary("no"), spec=f"{FRAMED}\n{REFRAMED}")
    code, out = run(repo, draft=True)
    assert code == 1, out
    assert REOPENED_TWICE in out, out


def bound_for_round_five(repo, fof_at_three):
    generator = _load("specseal_round_record_for_the_reframe", GENERATOR)
    reader = _load("specseal_reader_for_the_reframe", generator.chain.READER)
    routing = _load("specseal_routing_for_the_reframe", generator.chain.ROUTING)
    declared(repo, ITEM, *boundary(fof_at_three)[:4])
    return generator.bound_line(reader, routing, str(repo / ITEM / "rounds"), 5)


def test_the_printed_bound_does_not_reach_across_a_second(repo):
    line = bound_for_round_five(repo, SECOND)
    assert "round-2.md" not in (line or ""), line


def test_without_the_second_the_printed_bound_names_the_stopped_floor(repo):
    line = bound_for_round_five(repo, "no")
    assert line is not None and "round-2.md met the floor" in line, line


# --- S11, the foot still reads ---------------------------------------------


def test_a_foot_of_framed_then_reframed_passes_the_frame(repo):
    declared(repo, ITEM, rec(), planning="framer", spec=f"{FRAMED}\n{REFRAMED}")
    code, out = run(repo)
    assert code == 0, out


def test_a_reframe_above_the_framed_line_permits_nothing(repo):
    declared(repo, ITEM, *STOPPED, spec=f"{REFRAMED}\n{FRAMED}")
    code, out = run(repo)
    assert code == 1, out
    assert "carries no `Reframed <date> by <who>, after round 3.`" in out, out


def test_the_template_still_ends_with_the_framed_line():
    with open(os.path.join(ROOT, "templates", "sdd-spec.md"), encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
    chain = check_module()
    assert chain.MARK_RE.match(lines[-1]), lines[-1]
    assert not any(chain.REFRAME_RE.match(ln) for ln in lines), (
        "the template carries a `Reframed` line, which only a reframe writes"
    )


def test_the_cutoff_names_a_work_item():
    chain = check_module()
    reader = _load("specseal_reader_for_the_reframe_cutoff", chain.READER)
    ok, how = cutoff_item_is_traceable(ROOT, reader, chain.REFRAME_FROM)
    assert ok, how
