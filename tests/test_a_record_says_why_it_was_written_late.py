"""A round record can say WHY it was committed after the fixes it commissioned.

`chain_check.written_late` refuses such a record, on the strength of git rather
than of anything written in the file, and until this work item there was no
fourth exit from that refusal. Work item 1789034970 found the other three:
rewrite history so the adding commit moves, merge over a red line, or invent an
undocumented waiver. It ended red on a line no later commit could clear, and
the run was capped with its fixes redistributed across six issues.

So the record gains a row. `round_record.py new --written-late "<why>"` writes
`| Written late | yes — <why> |`; without the flag the row reads `no` and a
late record is refused exactly as before. `chain_check` reads it and prints
instead of failing — that half is pinned in
`tests/test_a_record_precedes_the_fixes_it_commissions.py`, beside the refusal
it relaxes.

Three things are pinned here, and the third is the one `plan.md` left as a read
nobody had made:

  the reason reaches the record                    A3
  a reason with nothing in it is refused           A4
  `close` does not lose the row when it applies    A7
  the fix table

A7 was settled by EXECUTION before the row's home was chosen, by a probe run on
2026-09-13: `close` rewrites the field rows it recognises by index and never
rebuilds the block, so an unrecognised row survives. Had it not, the reason
would have had to ride the existing `Target SHA` cell — `questions.md` Q3's
other candidate. The probe is gone (`agent-contract` §7) and this case is what
holds the answer.

Every case here was seen red before the flag existed, each by the mechanism
`plan.md` names for it. `phases/phase-3.md` has the output.
"""

import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GENERATOR = os.path.join(ROOT, "skills", "code-review", "scripts", "round_record.py")

ITEM = "seal/specs/1799000000-a-later-work-item"
ROUNDS = f"{ITEM}/rounds"
RAN_BY = "specseal:warden on a model"
ASKED = "Attack the parser first.\n"
WHY = "the fix pass was spawned before the record reached a commit"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


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


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("written-late-template") / "repo"
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declared(repo):
    write(
        repo,
        f"{ITEM}/routing.md",
        f"# {os.path.basename(ITEM)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n",
    )
    return commit(repo, "declare")


def report():
    return (
        "# what the round found\n\nProse about the finding.\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
        "| 🔴 1 | the parser drops a row | `f.py:1` | open | executed |\n\n"
        "Needs a fix: yes — 🔴 1\nLoses a record or crashes: no\n"
    )


def env():
    e = dict(os.environ)
    e.pop("GITHUB_EVENT_PATH", None)
    e.pop("GITHUB_HEAD_REF", None)
    e["GH_PROMPT_DISABLED"] = "1"
    e["GH_NO_UPDATE_NOTIFIER"] = "1"
    return e


def generate(repo, target, n=1, extra=()):
    """Run `new`; return (exit code, output, the record text or None)."""
    scratch = repo.parent
    (scratch / f"report-{n}.md").write_text(report(), encoding="utf-8")
    (scratch / f"asked-{n}.md").write_text(ASKED, encoding="utf-8")
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
            str(scratch / f"report-{n}.md"),
            "--asked",
            str(scratch / f"asked-{n}.md"),
            "--ran-by",
            RAN_BY,
            "--baseline",
            "base",
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env(),
    )
    path = repo / ROUNDS / f"round-{n}.md"
    text = path.read_text(encoding="utf-8") if path.exists() else None
    return r.returncode, r.stdout + r.stderr, text


def close(repo, n, fixes, rng):
    """Run `close`; return (exit code, output, the record text)."""
    path = repo.parent / f"fixes-{n}.md"
    path.write_text(fixes, encoding="utf-8")
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "close",
            "--item",
            str(repo / ITEM),
            "--round",
            str(n),
            "--fixes",
            str(path),
            "--range",
            rng,
            "--baseline",
            "base",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env(),
    )
    record = (repo / ROUNDS / f"round-{n}.md").read_text(encoding="utf-8")
    return r.returncode, r.stdout + r.stderr, record


def field(text, label):
    """The value of one `| label | value |` row, or None."""
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] == label:
            return cells[1]
    return None


# --- A3: the reason reaches the record --------------------------------------


def test_the_flag_writes_the_reason_into_the_record(repo):
    """A3. A state that leaves no trace is the one the refusal it relaxes was
    built for: a record written late looks finished, because by then its
    verdict cells read `fixed at <sha>`."""
    reviewed = declared(repo)
    code, out, text = generate(repo, reviewed, extra=("--written-late", WHY))
    assert code == 0, out
    assert field(text, "Written late") == f"yes — {WHY}", text


def test_the_row_reads_no_without_the_flag(repo):
    """The ordinary record, and the state that keeps every existing record
    judged exactly as it is today. The row is written either way, because a
    row that is sometimes absent is unlike every other row in the block and
    `templates/sdd-round.md` has no optional one."""
    reviewed = declared(repo)
    code, out, text = generate(repo, reviewed)
    assert code == 0, out
    assert field(text, "Written late") == "no", text


def test_the_row_sits_where_the_template_puts_it(repo):
    """Beside `Target SHA`, which is the fact it is about. The order is
    already pinned against the template by
    `tests/test_the_record_is_generated.py#test_the_field_rows_are_the_templates_in_the_templates_order`;
    this says which neighbour, which that case reads off the template and
    therefore cannot be wrong about in the other direction."""
    reviewed = declared(repo)
    _code, _out, text = generate(repo, reviewed)
    labels = [
        line.strip().strip("|").split("|")[0].strip()
        for line in text.splitlines()
        if line.startswith("| ")
    ]
    assert labels[labels.index("Target SHA") + 1] == "Written late", labels


def test_the_reason_is_written_in_the_vocabulary_the_other_two_rows_use(repo):
    """`Needs a fix` and `Loses a record or crashes` are `no` / `yes — <what>`
    and `chain_check.yes_or_no` reads both. A third spelling of one vocabulary
    is the drift that file closes everywhere else, so the flag carries the
    reason and never the whole cell."""
    reviewed = declared(repo)
    _code, _out, text = generate(repo, reviewed, extra=("--written-late", WHY))
    cell = field(text, "Written late")
    assert cell.startswith("yes "), cell
    assert WHY in cell, cell
    # A reason typed with the dash already in front of it must not land with
    # two of them.
    _code, _out, text = generate(
        repo, reviewed, n=2, extra=("--written-late", f"— {WHY}")
    )
    assert field(text, "Written late") == f"yes — {WHY}", text


# --- A4: an empty reason is refused -----------------------------------------


@pytest.mark.parametrize("given", ["", "   ", "—", " — "])
def test_a_reason_with_nothing_in_it_is_refused(repo, given):
    """A4. A bare `yes` says a record was written late and says nothing a
    reader can act on, and this row's whole purpose is that the pull request
    stops refusing the record on the strength of it. A relaxation bought with
    an empty cell is a waiver with no author — which is the third of work item
    1789034970's three bad exits, given a flag."""
    reviewed = declared(repo)
    code, out, text = generate(repo, reviewed, extra=("--written-late", given))
    assert code == 2, out
    assert "carries no reason" in out, out
    assert text is None, "the record was written despite the refusal"


def test_the_refusal_says_what_to_write(repo):
    """A refusal that names no exit is a wall. This one has to name the shape
    and give an example of the WHY it is asking for, because the person
    meeting it has just been told by `new` that HEAD moved and is deciding
    which of two readings they are in."""
    reviewed = declared(repo)
    _code, out, _text = generate(repo, reviewed, extra=("--written-late", ""))
    assert "yes — <why>" in out, out
    assert "HEAD moved mid-review" in out, out


# --- A7: `close` does not lose it -------------------------------------------


def test_close_keeps_the_row_when_it_applies_the_fix_table(repo):
    """A7, and the read `plan.md` left unmade. `close` rewrites the field rows
    it recognises by index and never rebuilds the block, so this row survives
    — which is what allows it to be a row at all rather than prose inside the
    existing `Target SHA` cell.

    The record is the shape the whole work item is about: written after its
    own fix, saying so, and then closed."""
    reviewed = declared(repo)
    _code, out, _text = generate(repo, reviewed, extra=("--written-late", WHY))
    start = commit(repo, "round 1, written after its own fixes")
    write(repo, "f.py", "x = 2\n")
    fix = commit(repo, "fix: the parser drops a row")

    _code, out, record = close(
        repo,
        1,
        "## Fixes\n\n| # | Verdict | Commit or grounds |\n|---|---|---|\n"
        f"| 1 | fixed | {fix} |\n",
        f"{start}..{fix}",
    )
    assert field(record, "Written late") == f"yes — {WHY}", out
    # And the rows `close` DOES rewrite were rewritten, so this is not a case
    # passing because `close` did nothing.
    assert "**fixed**" in record, record


# --- the template and the generator carry one spelling ----------------------


def test_the_template_documents_the_row_the_generator_writes():
    """`agent-contract` §14. The cell is read by whoever meets the refusal it
    relaxes, and a row the template does not describe is a row nobody knows
    they may write."""
    template = read("templates", "sdd-round.md")
    assert "| Written late |" in template, template[:400]
    assert "--written-late" in template
    assert "`no` · `yes — <why>`" in template
