"""The floor's reopening is one, and then the run is capped.

The floor's count (`tests/test_the_record_is_held_to_the_floor_and_the_depth.py`)
stops at the first later record that reopened the run or closed on a fix, and
every such record is itself a record that met the floor — so the count
restarts there and nothing bounds the chain. #161 measured fifteen rounds on
one branch, with the exception used by every verifying round of it.

  the reopening   after a record that met the floor, at most ONE later record
                  may close on a fix. The second is refused, naming it and the
                  floor record it follows, for work items begun on or after
                  `REOPEN_FROM`; earlier items print. The exit is `capped`
  deferred        `deferred <home>` closes a finding and is not a fix word;
                  a bare `deferred` stays open

The refusal cases were seen red before the walk existed, the vocabulary cases
before the word was in `CLOSED_WORDS`, and each spec pin with its sentence
stashed (§15). Git is driven from Python (§8).
"""

import importlib.util
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
SPEC = ("docs", "review-chain-spec.md")

# The boundary second, typed on both sides of it: the case is about the
# boundary and not about a number the module could be asked for.
ITEM_BEFORE = "seal/specs/1788597029-an-item-begun-a-second-before"
ITEM_AT = "seal/specs/1788597030-an-item-begun-at-the-cutoff"
# The refusal's own words, and the exit it names.
CAPPED = "the run is `capped`"
NOT_THE_COUNT = "at most one more"
# A phrase every message in the family carries, so an assertion on its
# absence is about the check having nothing to say and not about wording.
GRANDFATHERED = "prints instead of failing"

HEADING = "##### The reopening — one, and then the run is capped"
NEXT_HEADING = "##### The depth in `New units`"
PREVIOUS_HEADING = "##### `Needs a fix` — the row the bound"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_module():
    return _load("specseal_reopening_check_for_tests", CHECK)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(*parts).split())


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
    d = tmp_path_factory.mktemp("reopening-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declaration(item):
    return (
        f"# {os.path.basename(item)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )


def record(
    sha,
    verdict="answered",
    checker="no fixes to check",
    needs="no",
    floor="no",
    box="x",
):
    """A record that passes every check but the walk each case is about.

    `verdict` is the one 🔴 row's verdict cell; `checker` the `Fixes checked
    by` that goes with it. The defaults are the terminal record of a run:
    closed without a fix, nothing to check, the run stopped.
    """
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n"
        f"| Fixes checked by | {checker} |\n"
        "| Contract changes | none |\n"
        "| New units | none |\n"
        "| Ran by | specseal:warden on a model |\n"
        f"| Needs a fix | {needs} |\n"
        f"| Loses a record or crashes | {floor} |\n\n"
        f"- [{box}] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| 🔴 1 | something | `f.py:1` | {verdict} | grounds |\n"
    )


def floor_record(sha):
    """A record that met the floor and whose verdicts closed without a fix."""
    return record(sha)


def reopening(sha, reader, floor="no"):
    """A verifying round that opened something and whose fix `reader` opened.

    A `fixed` verdict naming no commit is house style and passes the
    ordering rule, so the fixture needs no second commit per record.
    """
    return record(
        sha,
        verdict="**fixed**",
        checker=f"round-{reader}",
        needs="yes — one, inside the fixes",
        floor=floor,
        box=" ",
    )


def run(repo):
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    r = subprocess.run(
        [sys.executable, CHECK, "--baseline", "base", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


def declared(repo, item, *bodies):
    """The declaration, then one record per body, each in its own commit, so
    every record's `Target SHA` descends from the one before it."""
    write(repo, f"{item}/routing.md", declaration(item))
    sha = commit(repo, "declare")
    for number, body in enumerate(bodies, start=1):
        write(repo, f"{item}/rounds/round-{number}.md", body(sha))
        sha = commit(repo, f"round {number}")
    return sha


# --- one reopening passes, a second is refused --------------------------------


def test_the_two_record_run_after_the_floor_is_kept_green(repo):
    """The floor record, the verifying round that reopened the run and closed
    on a fix, and the terminal record that read that fix. The one legal shape
    of a reopening, and the well-written run the bound must not touch."""
    declared(
        repo,
        ITEM_AT,
        floor_record,
        lambda sha: reopening(sha, reader=3),
        lambda sha: record(sha),
    )
    code, out = run(repo)
    assert code == 0, out
    assert CAPPED not in out


def test_a_second_fix_closing_record_after_the_floor_is_refused(repo):
    """Round 2 reopened and fixed; round 3 read those fixes, reopened and
    fixed again; round 4 read those. The second reopening is refused, naming
    round 3's file and the floor record it follows, and saying the exit."""
    declared(
        repo,
        ITEM_AT,
        floor_record,
        lambda sha: reopening(sha, reader=3),
        lambda sha: reopening(sha, reader=4),
        lambda sha: record(sha),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "round-3.md" in out, out
    assert "round-1.md" in out, out
    assert CAPPED in out, out
    for phrase in ("deferred #N", "no fixes to check", "chain: capped"):
        assert phrase in out, f"the refusal does not name the exit ({phrase!r}): {out}"
    assert NOT_THE_COUNT not in out, (
        "the floor's count fired on this sequence, so the case is not "
        "showing the reopening walk"
    )


def test_the_records_between_do_not_matter(repo):
    """The reopening record answers the floor `yes`, so it is not a floor
    record and the count never starts from it. The count from round 1 stops
    at round 2. Only the reopening walk sees round 3 — the case that tells
    the two walks apart."""
    declared(
        repo,
        ITEM_AT,
        floor_record,
        lambda sha: reopening(sha, reader=3, floor="yes — the export drops a row"),
        lambda sha: reopening(sha, reader=4),
        lambda sha: record(sha),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "round-3.md" in out and CAPPED in out, out
    assert NOT_THE_COUNT not in out


def test_a_second_reopening_prints_for_an_item_begun_a_second_before(repo):
    """The grandfathering, at the boundary: a second before `REOPEN_FROM`
    prints, the second itself fails. The rounds a printed notice names are
    over, and no record anybody writes now un-spawns them."""
    declared(
        repo,
        ITEM_BEFORE,
        floor_record,
        lambda sha: reopening(sha, reader=3),
        lambda sha: reopening(sha, reader=4),
        lambda sha: record(sha),
    )
    code, out = run(repo)
    assert code == 0, out
    assert CAPPED in out and GRANDFATHERED in out, out


def test_the_cutoff_is_this_work_items_own_id():
    """The shape the six cutoffs before it set: the constant is one work
    item's id, that work item is in the tree, and it is later than the
    cutoff before it."""
    module = check_module()
    assert module.REOPEN_FROM == 1788597030
    assert module.REOPEN_FROM > module.ORDER_FROM
    items = os.listdir(os.path.join(ROOT, "seal", "specs"))
    assert [d for d in items if d.startswith(f"{module.REOPEN_FROM}-")], (
        "the cutoff names a work item whose directory is not in the tree"
    )


# --- `deferred <home>` closes; bare `deferred` is open --------------------------


def cells(verdict):
    return ["🔴 1", "something", "`f.py:1`", verdict, "grounds"]


@pytest.mark.parametrize(
    "cell",
    [
        "deferred #170",
        "**deferred** #170",
        "deferred seal/follow-up.md",
        "deferred — #170",
        "deferred, #170",
    ],
)
def test_deferred_with_a_home_reads_as_closed_and_not_as_a_fix(cell):
    chain = check_module()
    word = chain.verdict_of(cells(cell), 3)
    assert word in chain.CLOSED_WORDS, (cell, word)
    assert word not in chain.FIX_WORDS, (cell, word)


@pytest.mark.parametrize(
    "cell", ["deferred", "**deferred**", "deferred —", "deferred."]
)
def test_bare_deferred_reads_as_open(cell):
    """The word with nothing after it says something was left and not where —
    the state a `nobody` with no reason is refused for."""
    chain = check_module()
    word = chain.verdict_of(cells(cell), 3)
    assert word not in chain.CLOSED_WORDS, (cell, word)
    assert "deferred" in word, "the open reading still says what the cell said"


def test_the_word_is_a_closing_word_and_not_a_fix_word():
    chain = check_module()
    assert chain.DEFERRED in chain.CLOSED_WORDS
    assert chain.DEFERRED not in chain.FIX_WORDS


def test_a_ready_pull_request_passes_a_blocking_finding_deferred_to_an_issue(repo):
    """Through `check_round`'s path: `Pass` ticked beside a 🔴 whose verdict
    is `deferred #170` is consistent, and `no fixes to check` beside it is
    the truth — a deferral produced no code."""
    declared(repo, ITEM_AT, lambda sha: record(sha, verdict="deferred #170"))
    code, out = run(repo)
    assert code == 0, out


def test_a_ready_pull_request_refuses_a_blocking_finding_deferred_nowhere(repo):
    declared(repo, ITEM_AT, lambda sha: record(sha, verdict="deferred"))
    code, out = run(repo)
    assert code == 1, out
    assert "`Pass` is checked, and this" in out, out
    assert "deferred" in out, out


def test_a_capped_run_has_a_legal_end(repo):
    """The spec's scenario: the floor record, the one reopening, and a last
    record whose verdicts read `deferred #N` with `no fixes to check` beside
    them and `Pass` ticked. Every check accepts it."""
    declared(
        repo,
        ITEM_AT,
        floor_record,
        lambda sha: reopening(sha, reader=3),
        lambda sha: record(sha, verdict="deferred #170", needs="yes — 🔴 1, deferred"),
    )
    code, out = run(repo)
    assert code == 0, out


# --- this repository's own records, under the new arm -------------------------


def _real_records():
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "-z", "--", "seal/specs/*/rounds/round-*.md"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    ).stdout
    return sorted(p for p in out.split("\0") if p)


def test_this_repositorys_own_records_are_not_refused_by_the_reopening_walk():
    """Every earlier work item began before `REOPEN_FROM`, so a run of theirs
    that reopened twice prints and is not refused; and this item's records,
    once they exist, are held to it. Nothing here FAILS on the new arm."""
    chain = check_module()
    reader = _load("reader_for_reopening", chain.READER)
    routing = _load("routing_for_reopening", chain.ROUTING)
    records = _real_records()
    assert records, "no round records found — the glob or the layout moved"
    by_item = {}
    for rel in records:
        by_item.setdefault(rel.rsplit("/rounds/", 1)[0], []).append(rel)
    failures = []
    for rels in by_item.values():
        ordered = sorted(rels, key=lambda r: routing.round_number(os.path.basename(r)))
        for index, rel in enumerate(ordered):
            errors, _ = chain.stopping_floor(reader, ROOT, rel, ordered[index + 1 :])
            failures.extend(e for e in errors if CAPPED in e[2])
    assert not failures, "this repository's own records are refused:\n" + "\n".join(
        f"  {rel}: {message}" for rel, _, message in failures
    )


def test_the_whole_check_names_no_earlier_items_record(monkeypatch, capsys):
    """`chain_check --baseline origin/release/v0.8.1`, in-process, on this
    repository: whatever it says about this branch's own item, no line names
    a record of an earlier item."""
    chain = check_module()
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    monkeypatch.delenv("GITHUB_HEAD_REF", raising=False)
    base = "origin/release/v0.8.1"
    if subprocess.run(
        ["git", "-C", ROOT, "rev-parse", "--verify", "-q", base],
        capture_output=True,
    ).returncode:
        pytest.skip(f"{base} is not fetched here")
    chain.main(["--baseline", base, "--root", ROOT])
    out = capsys.readouterr().out
    own = f"seal/specs/{chain.REOPEN_FROM}-"
    named = [
        line
        for line in out.splitlines()
        if "/rounds/round-" in line and own not in line
    ]
    assert not named, "\n".join(named)


# --- the spec states the rule, beside the eight ------------------------------


def subsection():
    text = flat(*SPEC)
    assert HEADING in text, "the spec has no subsection for the reopening"
    start = text.index(HEADING)
    return text[start : text.index(NEXT_HEADING, start)]


def test_the_subsection_sits_between_needs_a_fix_and_the_depth():
    text = flat(*SPEC)
    assert text.index(PREVIOUS_HEADING) < text.index(HEADING) < text.index(NEXT_HEADING)


@pytest.mark.parametrize(
    "phrase",
    [
        "at most one later record may close on a fix",
        "two fix-closing records",
        "REOPEN_FROM",
        "no timestamp prefix",
        "blocks more",
        "ships as an issue",
        "`chain: capped`",
        "`deferred #N`",
        "`no fixes to check`",
        "`deferred <home>` is a closing word and not a fix word",
        "A bare `deferred`",
        "two decide different things",
    ],
)
def test_the_subsection_states_the_rule_the_refusal_the_cutoff_the_direction_and_the_exit(
    phrase,
):
    assert phrase in subsection(), (
        f"the reopening subsection does not carry {phrase!r}, so the refusal "
        "is readable only in the failure it prints"
    )


def test_the_spec_lists_deferred_where_it_lists_the_closing_words():
    """The ordering rule's table names the words that close a finding and
    produce no code; `deferred <home>` is one of them now."""
    assert (
        "a verdict closing with `answered`, `withdrawn`, `not a defect` or "
        "`deferred <home>`"
    ) in flat(*SPEC)


def test_the_spec_says_worktree_is_local_only():
    """Phase 1 added the flag and left the sentence to this phase: the check
    reads `HEAD`, `--worktree` reads the working tree, and CI keeps the
    default because a tree that differs from `HEAD` is what CI never sees."""
    text = flat(*SPEC)
    arm = text[text.index("#### The declaration, and where the check went") :]
    arm = arm[: arm.index("##### `Pass` has to be checked")]
    assert "`--worktree`" in arm, "the review arm does not mention the flag"
    assert "CI keeps the default" in arm, "the arm does not say CI never passes it"


def test_the_module_docstring_names_the_reopening():
    text = flat("skills", "code-review", "scripts", "chain_check.py")
    opening = text.index('"""')
    head = text[opening : text.index('"""', opening + 3)]
    assert "REOPEN_FROM" in head and "capped" in head, (
        "the checker's own inventory of what it refuses omits the reopening"
    )
