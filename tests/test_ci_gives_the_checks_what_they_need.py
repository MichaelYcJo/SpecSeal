"""Two workflow settings decide whether the checks below them mean anything.

Neither is visible from the checks themselves, and both failed silently.

**Checkout depth.** `actions/checkout@v4` fetches one commit unless told
otherwise. Two tests in this suite ask git whether a recorded SHA is an
ancestor of HEAD — the rider stamps and the ledger stamps — and at depth 1 no
SHA is, because no SHA is in the clone at all. Reproduced with
`git clone --depth 1`: `git cat-file -t <a stamped SHA>` answers *Not a valid object
name* and the rider test goes red on every matrix leg.

**Which pull-request events run.** `on: pull_request:` with no `types:` runs
on `opened`, `synchronize` and `reopened` — and on nothing else. A review that
has not finished opens its pull request as a DRAFT, which `chain_check.py`
excuses the checked `Pass` for. Pressing *Ready for review* adds no commit, so
`synchronize` never fires, the workflow never re-runs, and the green the draft
earned stays on that SHA through the merge. The one requirement this branch
added is voided by two clicks and no commit.

These are assertions about YAML, which is not this repository's usual shape
for a test. They are here because the alternative is a comment in the workflow
asking the next editor to remember.
"""

import os
import re

import pytest
from conftest import _unquote, code_lines

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")

# Events GitHub does NOT include by default and that this repository needs,
# because a draft is the documented way past `chain_check.py`'s `Pass`
# requirement (`docs/round-record-spec.md` §`Pass` has to be checked).
DRAFT_EVENTS = ("ready_for_review", "converted_to_draft")


def strip_comments(text):
    """The workflow with its comment lines removed.

    A setting that exists only in a comment is not a setting. The comment
    above each `types:` list names both draft events, so a substring test on
    the raw trigger passes with the `types:` line itself deleted -- measured:
    dropping the real line and keeping the comment left both checks green,
    which is exactly the edit that reopens the defect they were written for.

    What a comment is belongs to `tests/conftest.py#code_line`, the one rule
    every workflow reader in the suite uses, so a trailing comment is off
    the line here too (#482).
    """
    return "\n".join(code_lines(text))


def read(name):
    with open(os.path.join(WORKFLOWS, name), encoding="utf-8") as f:
        return strip_comments(f.read())


def workflows():
    return sorted(n for n in os.listdir(WORKFLOWS) if n.endswith((".yml", ".yaml")))


def jobs(text):
    """{job name: its block} — a two-space indent under `jobs:`.

    Hand-parsed rather than with PyYAML, which CI does not install: the
    workflow being read is the one that decides what CI installs, and it
    installs a test runner and a way to run it in parallel -- no parser.
    """
    body = text.split("\njobs:\n", 1)
    assert len(body) == 2, "no `jobs:` block"
    out, name, lines = {}, None, []
    for line in body[1].splitlines():
        m = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if m:
            if name:
                out[name] = "\n".join(lines)
            name, lines = m.group(1), []
            continue
        if name is not None:
            lines.append(line)
    if name:
        out[name] = "\n".join(lines)
    return out


_FLOW_ITEM = re.compile(r"^\s*-\s*\{(.*)\}\s*$")
_FLOW_PAIR = re.compile(r"\s*([A-Za-z0-9_-]+):\s+(\S.*?)\s*")


def _flow_mapping(body, line):
    """One `{ … }` item's keys and values, quotes off; refuses what it cannot
    read whole."""
    parts, quote, start = [], None, 0
    for i, c in enumerate(body):
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c in "{}[]":
            raise ValueError(f"a nested collection in a matrix entry: {line!r}")
        elif c == ",":
            parts.append(body[start:i])
            start = i + 1
    if quote:
        raise ValueError(f"an unclosed quote in a matrix entry: {line!r}")
    parts.append(body[start:])
    entry = {}
    for part in parts:
        m = _FLOW_PAIR.fullmatch(part)
        if not m or m.group(1) in entry:
            raise ValueError(f"a matrix entry that is not `key: value, …`: {line!r}")
        entry[m.group(1)] = _unquote(m.group(2))
    return entry


def pytest_matrix(text):
    """The `pytest` job's `include:` entries, one dict per entry (#864).

    The suite's one reading of the matrix of `.github/workflows/test.yml`,
    beside `jobs`, which finds the job. Four cases used to slice the job out
    of the raw text by its neighbour's name, and the one that read entries
    took every line starting `- { os:`: an entry written another way was not
    an entry, and nothing said so.

    Input class: *owned*. The file is this repository's own, and every entry
    in it is a one-line flow mapping, `- { os: …, python: "…", … }`. That is
    the one shape read here, and values come back as strings with their
    quotes off, as `conftest.py#_unquote` reads a step's name. Comments are
    taken off first, through `conftest.py#code_lines`, so a commented-out
    entry is not an entry. Anything else under `include:` -- a block-style
    item, a nested value, a key written twice -- is refused with a
    `ValueError` naming its line rather than skipped, and so is a workflow
    with no `pytest` job, a job with no single `include:`, or one with no
    entry under it.
    """
    job = jobs("\n".join(code_lines(text))).get("pytest")
    if job is None:
        raise ValueError("no `pytest` job under `jobs:`")
    lines = job.splitlines()
    heads = [i for i, ln in enumerate(lines) if ln.strip() == "include:"]
    if len(heads) != 1:
        raise ValueError(f"the `pytest` job has {len(heads)} `include:` keys, not one")
    head = len(lines[heads[0]]) - len(lines[heads[0]].lstrip(" "))
    entries = []
    for line in lines[heads[0] + 1 :]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent < head or (indent == head and not line.lstrip().startswith("-")):
            break
        m = _FLOW_ITEM.match(line)
        if not m:
            raise ValueError(
                "an `include:` item that is not a one-line `- { … }` flow "
                f"mapping, the one shape this reader owns: {line.strip()!r}"
            )
        entries.append(_flow_mapping(m.group(1), line.strip()))
    if not entries:
        raise ValueError("the `pytest` job's `include:` holds no entry")
    return entries


# A matrix in this repository's shape, with a commented entry, a trailing
# comment, a single-quoted value, a value holding a `#`, a sibling key that
# ends `include:` and a second job's matrix. Neutral values
# only (`CONTRIBUTING.md` §*House rules*, *No real identifiers*).
MATRIX = """\
name: tests

jobs:
  lint:
    runs-on: ubuntu-latest
  pytest:
    strategy:
      matrix:
        include:
          - { os: ubuntu-latest, python: "3.12", timeout: 15 }
          # - { os: macos-latest, python: "3.12", timeout: 35 }
          - { os: macos-latest, python: "3.12", split: "--splits 2 --group 1", timeout: 5 }  # one
          - { os: example-os, python: '3.12', note: "a # b" }
        exclude:
          - { os: example-os, python: "3.12" }
    runs-on: ${{ matrix.os }}
    steps:
      - run: pytest tests/ ${{ matrix.split }}
  other:
    strategy:
      matrix:
        include:
          - { os: not-this-job }
"""

LAST_ENTRY = "- { os: example-os, python: '3.12', note: \"a # b\" }"


def test_the_matrix_entries_are_read_with_their_quotes_off():
    assert pytest_matrix(MATRIX) == [
        {"os": "ubuntu-latest", "python": "3.12", "timeout": "15"},
        {
            "os": "macos-latest",
            "python": "3.12",
            "split": "--splits 2 --group 1",
            "timeout": "5",
        },
        {"os": "example-os", "python": "3.12", "note": "a # b"},
    ]


def test_a_commented_matrix_entry_is_not_an_entry():
    entries = pytest_matrix(MATRIX)
    assert [e["os"] for e in entries] == [
        "ubuntu-latest",
        "macos-latest",
        "example-os",
    ], entries


@pytest.mark.parametrize(
    "item",
    [
        '- os: macos-latest\n            python: "3.12"',
        "- { os: macos-latest, python: [3.12] }",
        "- { os: macos-latest, os: example-os }",
        '- { os: macos-latest, split: "--splits 2 }',
        "- os-only",
    ],
    ids=["block-style", "nested", "key-twice", "unclosed-quote", "scalar"],
)
def test_an_include_item_this_reader_does_not_own_is_refused_by_its_line(item):
    text = MATRIX.replace(LAST_ENTRY, item)
    assert text != MATRIX
    with pytest.raises(ValueError) as caught:
        pytest_matrix(text)
    assert item.splitlines()[0].strip() in str(caught.value), caught.value


def test_a_workflow_with_no_entry_to_read_is_refused():
    with pytest.raises(ValueError, match="no `pytest` job"):
        pytest_matrix(MATRIX.replace("  pytest:", "  tests:"))
    with pytest.raises(ValueError, match="holds no entry"):
        pytest_matrix(MATRIX.split("          - { os: ubuntu")[0] + "    runs-on: x\n")
    with pytest.raises(ValueError, match="0 `include:` keys"):
        pytest_matrix(
            MATRIX.replace(
                "        include:\n          - { os: ubuntu",
                "          - { os: ubuntu",
                1,
            )
        )


def test_every_job_that_runs_pytest_has_the_whole_history():
    """A check that cannot resolve a SHA is not excused from resolving it."""
    offenders = []
    for name in workflows():
        for job, block in jobs(read(name)).items():
            if "pytest " not in block and "pytest\n" not in block:
                continue
            if "actions/checkout" not in block:
                continue
            if "fetch-depth: 0" not in block:
                offenders.append(f"{name}:{job}")
    assert not offenders, (
        f"jobs that run pytest on a shallow checkout: {offenders}. "
        "At depth 1 a ref this repository's own records name is MISSING "
        "rather than wrong, so a case that resolves one skips instead of "
        "failing — which turns the one checkout setting that voids these "
        "checks into the setting that silences them. "
        "`tests/test_the_reopening_is_one.py#"
        "test_the_whole_check_names_no_earlier_items_record` is the live "
        "case: it resolves `origin/release/v0.8.1` and skips when it cannot. "
        "Neither of the two mechanisms that used to be the reason is one any "
        "more — a ledger row has named no commit since the anchors went to "
        "content, and a rider stamp has named none since #239, which is also "
        "why `tests/test_a_rider_reaches_its_file.py` no longer appears here"
    )


def test_a_pull_request_workflow_reruns_when_a_draft_becomes_ready():
    """Otherwise the draft excuse is permanent rather than temporary.

    `chain_check.py` lets a draft pull request open with an unchecked `Pass`
    because a review still running has to have somewhere to be. That excuse is
    meant to end when the pull request stops being a draft. Without these two
    event types it never does — no commit is needed to leave draft state, and
    no commit means no `synchronize`.
    """
    for name in workflows():
        text = read(name)
        if "\n  pull_request:" not in text:
            continue
        trigger = text.split("\n  pull_request:", 1)[1].split("\njobs:", 1)[0]
        for event in DRAFT_EVENTS:
            assert event in trigger, (
                f"{name}: `on.pull_request` does not list `{event}`. The "
                "default set is opened/synchronize/reopened, so leaving draft "
                "state re-runs nothing and the draft's green is what merges"
            )
