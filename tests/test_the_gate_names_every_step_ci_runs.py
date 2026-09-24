"""The gate's arm list was kept in step with the workflow's by whoever
remembered, and nothing held the two lists against each other (#468).

`skills/verify/scripts/broad_gate.py#gate` runs a handful of arms so the
sealer's one run says what CI will say. `.github/workflows/hygiene.yml`'s
`release` job runs thirteen named steps. #424 added one of those thirteen and
the gate was not extended, so from that merge onward a green seal covered a
shorter list than the merge is judged by — and no case in the suite went red
for it.

The repair is a declared partition: every step of that job is either mirrored
by a named arm or excluded with a reason a person wrote. This module is what
keeps the partition total, and it is driven RED FROM BOTH SIDES, which is the
half #423's finding 4 was about:

  A1   a step added to the workflow and left unclassified fails here, so the
       seventh arm cannot arrive in silence
  A2   a partition entry naming a step the workflow no longer has fails here,
       so the list cannot rot into naming steps nobody runs

`spec.md` §*User scenarios & acceptance* numbers the rows A1 to A7 and each
case below names the one it holds.

**The step names are read out of `hygiene.yml` itself.** `plan.md` retypes
them for a human reader and says in the same breath that its copy will rot; a
case driven by a list in a document is a case that grades the document. No
YAML parser either — `broad_gate.py` runs with no third-party dependency, so
the reader is text, and it is driven over shapes this repository's workflow
does not happen to have. A reader nothing drives is a reader nobody can tell
is partial (#424's finding 4).
"""

import ast
import importlib.util
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")
HYGIENE = os.path.join(ROOT, ".github", "workflows", "hygiene.yml")
EVIDENCE = os.path.join(
    ROOT, "skills", "evidence-check", "scripts", "evidence_check.py"
)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gate_module():
    return _load("specseal_broad_gate_for_partition_tests", GATE)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


gate = gate_module()


# --- the reader, driven over shapes the workflow does not have -------------


WORKFLOW_WITH_TWO_JOBS = """\
name: example

on:
  pull_request:

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # - name: a step somebody commented out
      - name: the first step
        run: true
      - name: the second step
        run: true
  ledger:
    runs-on: ubuntu-latest
    steps:
      - name: a step of another job
        run: true
"""


def test_the_reader_takes_the_steps_of_the_job_it_was_asked_for():
    """A1's reader. In file order, this job only, and an unnamed step — the
    checkout every job opens with — is not one."""
    assert gate.job_steps(WORKFLOW_WITH_TWO_JOBS, "release") == [
        "the first step",
        "the second step",
    ]
    assert gate.job_steps(WORKFLOW_WITH_TWO_JOBS, "ledger") == ["a step of another job"]


def test_a_commented_out_step_is_not_a_step():
    """A step that exists only in a comment is not a step — the same reading
    `tests/test_ci_gives_the_checks_what_they_need.py#strip_comments` takes of
    the same file, for the same reason."""
    assert "a step somebody commented out" not in gate.job_steps(
        WORKFLOW_WITH_TWO_JOBS, "release"
    )


def test_a_job_the_workflow_does_not_have_reads_as_no_steps():
    assert gate.job_steps(WORKFLOW_WITH_TWO_JOBS, "nosuchjob") == []


def test_a_file_that_declares_no_jobs_reads_as_no_steps():
    """Not an exception. The gate calls this on whatever file sits at the
    workflow's path in the repository it was pointed at, and a file it cannot
    read as a workflow must leave the run exactly as it was (A7)."""
    assert gate.job_steps("name: not a workflow at all\n", "release") == []
    assert gate.job_steps("", "release") == []


def test_a_quoted_step_name_comes_back_unquoted():
    """YAML lets a name be quoted, and the partition holds the name a reader
    sees rather than the bytes the file spells it in."""
    text = 'jobs:\n  release:\n    steps:\n      - name: "the quoted step"\n'
    assert gate.job_steps(text, "release") == ["the quoted step"]
    text = "jobs:\n  release:\n    steps:\n      - name: 'the other quoting'\n"
    assert gate.job_steps(text, "release") == ["the other quoting"]


def test_a_step_name_carrying_a_colon_survives_the_reader():
    """`- name: a: b` is one name, not a mapping. A reader that split on the
    first colon would take `a` and the partition would name a step nobody
    runs — which is exactly A2's failure, arriving through the reader."""
    text = "jobs:\n  release:\n    steps:\n      - name: the step: and its tail\n"
    assert gate.job_steps(text, "release") == ["the step: and its tail"]


# --- A1 and A2: the partition is total, in both directions ------------------


def workflow_steps():
    steps = gate.job_steps(read(HYGIENE), gate.RELEASE_JOB)
    assert steps, (
        f"{HYGIENE} names no step of the `{gate.RELEASE_JOB}` job. Either the "
        "job was renamed or the file's shape moved under the reader — and a "
        "reader that comes back empty grades nothing, so this is a refusal "
        "rather than a pass"
    )
    return steps


def test_every_step_the_workflow_runs_is_classified():
    """A1. Red when a step is added to the workflow and nobody classifies it.

    This is the direction the work item exists for: #424 added the thirteenth
    step, the gate was not extended, and the suite said nothing. A step with
    no row is the silence this ends — `classified` includes `excluded`, and an
    exclusion carries prose rather than a category (A4).
    """
    classified = {name for name, _, _ in gate.PARTITION}
    missing = [name for name in workflow_steps() if name not in classified]
    assert not missing, (
        f"these steps of `hygiene.yml`'s `{gate.RELEASE_JOB}` job are in no "
        f"row of `broad_gate.py#PARTITION`: {missing}. Add an arm that mirrors "
        "each, or a row excluding it with the reason no arm can — there is no "
        "third state, and a step with no row is a seal that covers less than "
        "the merge is judged by"
    )


def test_every_entry_of_the_partition_names_a_step_the_workflow_has():
    """A2. The other side. Red when a step is renamed in the workflow, or
    removed, and the partition still names it.

    Without this the partition rots into a list of steps nobody runs, and a
    reader counting what the seal did not answer is counting ghosts."""
    steps = set(workflow_steps())
    stale = [name for name, _, _ in gate.PARTITION if name not in steps]
    assert not stale, (
        f"`broad_gate.py#PARTITION` names steps `hygiene.yml`'s "
        f"`{gate.RELEASE_JOB}` job does not have: {stale}. A renamed step is "
        "a row to rename here; a deleted one is a row to delete"
    )


def test_the_partition_names_each_step_once():
    """Two rows for one step is two answers to one question, and the second
    is unreachable — whichever way a reader resolves it, the count of what the
    seal did not answer is wrong by one."""
    names = [name for name, _, _ in gate.PARTITION]
    twice = sorted({name for name in names if names.count(name) > 1})
    assert not twice, f"these steps carry more than one row: {twice}"


def test_a_row_is_an_arm_or_a_reason_and_never_both_or_neither():
    """The partition's shape, which A1 and A2 assume and neither asserts. A
    row with both says a step is mirrored AND excluded; a row with neither is
    the silence written down."""
    broken = [
        (name, arm, reason)
        for name, arm, reason in gate.PARTITION
        if bool(arm) == bool(reason)
    ]
    assert not broken, (
        f"these rows are neither mirrored nor excluded, or claim to be both: {broken}"
    )


# --- A3: an arm the partition names is an arm the gate runs -----------------


def gate_function():
    """`gate()`, as a syntax tree.

    Read as a tree rather than as text for the reason
    `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py#failure_loop`
    gives about the same function: the claim is about which checks the gate
    RUNS, and a substring search cannot tell a call from a mention of one in a
    docstring or a comment.
    """
    parsed = ast.parse(read(GATE))
    found = [
        node
        for node in ast.walk(parsed)
        if isinstance(node, ast.FunctionDef) and node.name == "gate"
    ]
    assert len(found) == 1, f"broad_gate.py has {len(found)} functions named gate"
    return found[0]


def arms_the_gate_runs():
    """The check name each `checks[...] = run(...)` in `gate()` records.

    The key is read as source rather than resolved, so `checks[CHAIN_NAME]`
    comes back as the constant's NAME — which is what the partition holds too,
    because a row names the arm by the same constant.
    """
    names = []
    for node in ast.walk(gate_function()):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Subscript):
                continue
            if ast.unparse(target.value) != "checks":
                continue
            call = node.value
            ran = isinstance(call, ast.Call) and ast.unparse(call.func) == "run"
            if ran:
                names.append(ast.unparse(target.slice))
    return names


def test_every_arm_the_partition_names_is_an_arm_the_gate_runs():
    """A3. Red when an arm is deleted from `gate()` while its partition row
    stands — the row would then say a step is mirrored by nothing.

    The partition holds the arm's VALUE (`"chain"`) and `gate()` subscripts
    `checks` by the constant's NAME (`CHAIN_NAME`), so the two are joined
    through the module: a constant renamed in one place and not the other is
    red here rather than quiet."""
    ran = arms_the_gate_runs()
    assert ran, "gate() records no check at all"
    values = {}
    for name in ran:
        assert hasattr(gate, name), (
            f"gate() records `checks[{name}]` and broad_gate.py has no such constant"
        )
        values[getattr(gate, name)] = name
    missing = sorted({arm for _, arm, _ in gate.PARTITION if arm and arm not in values})
    assert not missing, (
        f"`PARTITION` says these arms mirror a step of the workflow and "
        f"`gate()` runs no check by those names: {missing}. The arms it does "
        f"run are {sorted(values)}"
    )


def test_the_gate_runs_no_arm_the_partition_does_not_account_for():
    """A3's other side. An arm the gate runs and the partition never names is
    an arm nobody can say which step it stands for — the `suite` and `ledger`
    arms aside, which answer no step of this job at all: `suite` is the
    repository's own command from the `Broad gate` row of `seal/config.md`,
    and `ledger` mirrors `evidence_check.py` as `.github/workflows/test.yml`
    runs it in its `ledger` job. `hygiene.yml` declares one job, so the
    earlier wording — *they answer the workflow's other jobs* — sent a
    maintainer to a category that is empty (round 1, finding 4)."""
    answering_no_release_step = {gate.SUITE, gate.LEDGER}
    named = {arm for _, arm, _ in gate.PARTITION if arm}
    loose = sorted(
        getattr(gate, name)
        for name in arms_the_gate_runs()
        if getattr(gate, name) not in named | answering_no_release_step
    )
    assert not loose, (
        f"`gate()` runs these arms and no partition row names them: {loose}. "
        "An arm belongs to a step of the `release` job, or it answers "
        "something outside that job — the repository's own command, or a job "
        "of another workflow — and belongs in the set above"
    )


# --- A5: the branch whose merge dropped a correction ------------------------


HANDLER = "def handler(x):\n    y = x + 1\n    return y\n"
LEDGER_HEAD = (
    "# Evidence ledger\n\n| Claim | Coordinate | Evidence | Notes |\n"
    "|---|---|---|---|\n"
)


def ledger_row(key, anchor, evidence):
    return f"| {key} | `{anchor}` | {evidence} | none |\n"


def anchor_for(text):
    """`src/service.py#handler@<hash>`, computed the way the checker does.

    The fixture's ledger has to survive `evidence-check --strict`, or the
    gate refuses for the ledger's sake and A5 proves nothing about the arm it
    is actually about."""
    ec = _load("specseal_evidence_check_for_partition_tests", EVIDENCE)
    places = ec.resolve("src/service.py", "handler", text)
    assert len(places) == 1, f"fixture anchor is not unique: {places}"
    first, last = places[0]
    digest = ec.content_hash(text.splitlines()[first - 1 : last])
    return f"src/service.py#handler@{digest}"


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
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
        "--allow-empty",
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


CONFIG = (
    "# Repository config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n"
    f"| Broad gate | {sys.executable} -c pass |\n"
)
OVERVIEW = "# overview\n\n## Not verified\n\nnone — the fixture verifies nothing\n"
ITEM = "seal/specs/1799000000-a-fixture-work-item"


def sealable_repo(tmp_path, resolution):
    """A repository on `base` with a `feature` branch whose HEAD is a merge.

    `resolution` is the `seal/ledger.md` the merge was resolved to, so one
    fixture builds both A5's branch — the merge dropped a marker — and the
    branch that dropped nothing, which is what says the arm's verdict tracks
    the merge rather than the fixture.

    Driven from Python, per `agent-contract` §8: a probe that commits reaches
    the commit gate exactly as real work does, and the prompt lands on nobody
    while a round is running.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "base")
    write(repo, "src/service.py", HANDLER)
    anchor = anchor_for(HANDLER)
    plain_a = ledger_row("A1 · the first claim", anchor, "**Read** 2026-09-01.")
    plain_b = ledger_row("B1 · the second claim", anchor, "**Read** 2026-09-01.")
    write(repo, "seal/config.md", CONFIG)
    write(repo, f"{ITEM}/overview.md", OVERVIEW)
    write(repo, "seal/ledger.md", LEDGER_HEAD + plain_a + plain_b)
    commit(repo, "base")

    corrected_a = ledger_row(
        "A1 · the first claim",
        anchor,
        "**Read** 2026-09-01. Corrected 2026-09-15 by review round 3.",
    )
    reread_b = ledger_row(
        "B1 · the second claim",
        anchor,
        "**Read** 2026-09-01. Re-read 2026-09-05 and widened.",
    )
    git(repo, "switch", "-qc", "side")
    write(repo, "seal/ledger.md", LEDGER_HEAD + plain_a + reread_b)
    commit(repo, "side re-reads its row")

    git(repo, "switch", "-q", "base")
    git(repo, "switch", "-qc", "feature")
    write(repo, "seal/ledger.md", LEDGER_HEAD + corrected_a + plain_b)
    commit(repo, "feature corrects its row")
    git(repo, "merge", "--no-commit", "--no-ff", "side", check=False)
    write(
        repo,
        "seal/ledger.md",
        LEDGER_HEAD + (corrected_a if resolution == "kept" else plain_a) + reread_b,
    )
    commit(repo, "Merge branch 'side' into feature")
    return repo


def run_gate(repo, keep):
    return subprocess.run(
        [
            sys.executable,
            GATE,
            "--base",
            "base",
            "--root",
            str(repo),
            "--shape",
            "--keep-output",
            str(keep),
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        env={
            key: value
            for key, value in os.environ.items()
            if key not in ("GITHUB_EVENT_PATH", "GITHUB_HEAD_REF")
        },
    )


def test_a_merge_that_dropped_a_correction_is_not_sealed(tmp_path):
    """A5. The instance that started the work item: #424 added the step to
    the workflow, the gate did not mirror it, and a branch in exactly this
    state sealed green and met a red leg.

    Red against the gate as it stood — every other arm passes on this
    fixture, so before the `corrections` arm existed the run drew the stamp.
    """
    repo = sealable_repo(tmp_path, resolution="dropped")
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "NOT SEALED" in result.stdout, result.stdout
    assert gate.CORRECTIONS_NAME in result.stdout, (
        f"the failure form does not name the `{gate.CORRECTIONS_NAME}` arm, "
        f"so whatever refused this branch, it was not the dropped marker:\n"
        f"{result.stdout}"
    )
    assert "Corrected 2026-09-15" in result.stdout, result.stdout


def test_the_same_branch_with_the_correction_kept_is_sealed(tmp_path):
    """A5's other half, and it is what makes the case above mean anything. A
    gate that refused every branch would pass the assertions above without
    reading the merge at all."""
    repo = sealable_repo(tmp_path, resolution="kept")
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SEALED" in result.stdout, result.stdout


def test_a_mode_row_that_disagrees_with_the_folder_is_not_sealed(tmp_path):
    """A3's behavioural half for the other arm #468 added. `seal/config.md`
    says the root lives under the git directory and the root is committed in
    the tree, which is the one direction of that disagreement CI can ever
    reach — and the gate said nothing about it until this arm existed.

    Red against the gate as it stood: this fixture sealed green."""
    repo = sealable_repo(tmp_path, resolution="kept")
    write(
        repo, "seal/config.md", CONFIG.replace("| Mode | shared |", "| Mode | local |")
    )
    commit(repo, "the row now says local while the folder is committed")
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "NOT SEALED" in result.stdout, result.stdout
    assert gate.MODE_NAME in result.stdout, (
        f"the failure form does not name the `{gate.MODE_NAME}` arm:\n{result.stdout}"
    )


# --- A6: the run says which of the workflow's steps it did not answer -------


FIXTURE_WORKFLOW = """\
name: hygiene

on:
  pull_request:

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: a declared review chain has the round record it claimed
        run: true
      - name: the milestone this release claims is the work it carries
        run: true
      - name: both READMEs move together
        run: true
"""


def panel_rows(repo):
    """The stamp's rows for a run over `repo`'s workflow, computed rather
    than scraped off the drawing — the rendered line is asserted separately,
    and a value's WIDTH cannot be measured once the frame has cut it."""
    checks = {
        name: gate.Check(name, 0, "", "")
        for name in (gate.SUITE, gate.LEDGER, gate.CHAIN_NAME)
    }
    base = gate.Base("base", "cccccccc", "base", "cccccccc")
    return gate.panel(
        "ccccccc", base, checks, None, read(repo / ".github/workflows/hygiene.yml")
    )


def with_workflow(repo):
    """The fixture, given a hygiene workflow whose `release` job runs three
    real steps: one this gate mirrors and two it does not."""
    write(repo, ".github/workflows/hygiene.yml", FIXTURE_WORKFLOW)
    commit(repo, "the repository gains a hygiene workflow")
    return repo


def test_the_stamp_says_how_many_steps_the_seal_did_not_answer(tmp_path):
    """A6, on the rendered output rather than on the data behind it.

    W1's choice, recorded: **the panel carries the count and the names go to
    the stream beside it.** `seal_stamp.letter` gives a panel value 23
    columns — `broad_gate.PANEL_VALUE_WIDTH`, measured over there — and three
    step names do not fit in it, let alone thirteen. A reader given only a
    number would have to reconstruct WHICH from two files, which is the
    reconstruction this work item exists to remove, so both are printed and
    neither alone."""
    repo = with_workflow(sealable_repo(tmp_path, resolution="kept"))
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 0, result.stdout + result.stderr

    rendered = [line for line in result.stdout.splitlines() if "not answered" in line]
    assert len(rendered) == 1, (
        f"the stamp says nothing about the steps this seal did not answer:\n"
        f"{result.stdout}"
    )
    # Whole, not cut. `seal_stamp.letter` truncates AT THE FRAME with no
    # marker, so a value one column too wide reads on the stamp as a shorter
    # true statement — which is the failure mode the elision beside the `from`
    # row was added for. The substring is the assertion: a cut value would not
    # carry its tail.
    assert "2 of 3 not answered" in rendered[0], rendered[0]
    value = next(
        v for _, v in [r for r in panel_rows(repo) if r] if "not answered" in v
    )
    assert len(value) <= gate.PANEL_VALUE_WIDTH, (
        f"the value is {len(value)} columns and the panel gives "
        f"{gate.PANEL_VALUE_WIDTH}: {value!r}. This is W1's whole reason for a "
        "count rather than the names"
    )

    assert "the milestone this release claims is the work it carries" in result.stderr
    assert "both READMEs move together" in result.stderr
    assert (
        "a declared review chain has the round record it claimed"
        not in (result.stderr.split("Not answered", 1)[-1])
    ), "a step the gate DOES mirror is listed among the ones it did not answer"


def test_a_seal_that_answers_every_step_says_so(tmp_path):
    """The other value of the same line. A run that leaves nothing unanswered
    must not go quiet: silence there is indistinguishable from a gate that
    stopped looking, which is the state this work item found the gate in."""
    repo = sealable_repo(tmp_path, resolution="kept")
    write(
        repo,
        ".github/workflows/hygiene.yml",
        FIXTURE_WORKFLOW.replace(
            "      - name: the milestone this release claims is the work it carries\n"
            "        run: true\n"
            "      - name: both READMEs move together\n"
            "        run: true\n",
            "",
        ),
    )
    commit(repo, "a workflow whose every step this gate mirrors")
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "answers every one of" in result.stderr, result.stderr


# --- A4: a reason is prose a person wrote -----------------------------------


def reasons():
    return [(name, reason) for name, _, reason in gate.PARTITION if reason]


def test_every_exclusion_carries_prose_rather_than_a_category():
    """A4. Red against a reason cell reduced to a category word.

    `EXCLUDED` tells the next reader nothing, and the reason is the whole
    value of the row — it is what a person checks when they wonder whether
    the seal covers them. Two structural rules stand in for that judgment: a
    reason is several words, and it is written in the prose case rather than
    as a marker.

    **What this cannot catch is a category in prose clothing.** *not
    applicable here* passes every rule below and says as little as
    `EXCLUDED`. Only a reader catches that one, and `plan.md` §*The failure
    scenario at six months* is where it is written down as an open hole
    rather than a closed one.
    """
    thin = [
        (name, reason)
        for name, reason in reasons()
        if len(reason.split()) < 3 or reason == reason.upper()
    ]
    assert not thin, (
        f"these rows give a marker where a reason belongs: {thin}. A reason "
        "is prose somebody wrote — `needs the pull request's body` is one, "
        "`EXCLUDED` is not"
    )


def test_every_exclusion_says_what_the_gate_cannot_reach():
    """A4's second half. A reason that never names the thing out of reach is
    a sentence rather than a reason — it reads as prose and answers nothing.

    Held loosely on purpose: the vocabulary below is what the four kinds of
    unreachable thing are called in this repository, and a fifth kind is a
    word to add here rather than a case to delete."""
    out_of_reach = (
        "pull request",
        "tracker",
        "fetch",
        "network",
        "never fails",
        "warning",
        ".github/scripts/",
        "inline",
        "second reading",
        "second implementation",
    )
    silent = [
        name
        for name, reason in reasons()
        if not any(word in reason for word in out_of_reach)
    ]
    assert not silent, (
        f"these rows give a reason that names nothing out of the gate's "
        f"reach: {silent}. Say what the gate cannot get at — the pull "
        "request, the tracker, a fetch, a step that only warns, or a check "
        "this repository owns rather than the plugin"
    )


# --- A7: a repository with no such workflow is untouched --------------------


# The panel of a run with no workflow, as it has stood release to release.
# `gate` joined it in 0.15.1 (#475): which copy of the gate drew the stamp,
# `tree <version>` or `plugin <version>`, because a branch that changes the
# gate used to be measured by the installed copy and the stamp could not say
# which one. It is the one row this partition's A7 admits, for every
# repository — nothing else about a run without a workflow changed.
HISTORICAL_ROWS = (
    "SEALED",
    "tree",
    "base",
    "from",
    "gate",
    "suite",
    "row",
    "ledger",
    "chain",
)


def test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before(tmp_path):
    """A7. The partition describes THIS repository's CI and `broad_gate.py`
    ships to every repository that installs the plugin. For one with no such
    workflow the run must be what it was: the same panel rows, and no line
    about steps nobody runs.

    Red against a gate that prints the row unconditionally — which is what a
    partition held as a constant and printed from would do, and why
    `questions.md` Q1's answer (a) survives only while this case is green.
    """
    repo = sealable_repo(tmp_path, resolution="kept")
    assert not (repo / ".github").exists(), "the fixture has a workflow after all"
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "not answered" not in result.stdout, (
        f"the stamp of a repository with no hygiene workflow says something "
        f"about that workflow's steps:\n{result.stdout}"
    )
    assert "release" not in result.stderr.replace(str(repo), ""), result.stderr
    assert gate.WORKFLOW not in result.stderr, result.stderr

    labels = tuple(
        row[0]
        for row in gate.panel(
            "ccccccc",
            gate.Base("base", "cccccccc", "base", "cccccccc"),
            {
                name: gate.Check(name, 0, "", "")
                for name in (gate.SUITE, gate.LEDGER, gate.CHAIN_NAME)
            },
            None,
        )
        if row
    )
    assert labels == HISTORICAL_ROWS, (
        f"the panel of a run with no workflow is no longer the panel it was: {labels}"
    )


def test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was(tmp_path):
    """A7's other shape, and the one that ends the run rather than changing
    it. `UnicodeDecodeError` is a `ValueError`, not an `OSError`, and
    `broad_gate.main` catches only `Refused` — so before this the gate ended
    on a traceback for a repository whose workflow file happens to be
    latin-1. A repository this partition is not about must come out of the
    run exactly as it went in, and a traceback is the largest departure from
    that there is. Round 1, finding 5."""
    repo = sealable_repo(tmp_path, resolution="kept")
    path = repo / ".github" / "workflows" / "hygiene.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        "jobs:\n  release:\n    steps:\n      - name: café step\n".encode("latin-1")
    )
    commit(repo, "a workflow file that is not utf-8")
    assert gate.workflow_text(str(repo)) is None
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SEALED" in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr
    assert "not answered" not in result.stdout, result.stdout


UNCLASSIFIED_WORKFLOW = """\
name: hygiene

on:
  pull_request:

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: a declared review chain has the round record it claimed
        run: true
      - name: deploy to staging
        run: true
"""


def test_a_step_no_row_classifies_is_not_said_to_carry_a_reason():
    """A6's other repository, and round 1's finding 3. `PARTITION` describes
    THIS repository's `release` job, and `broad_gate.py` ships to every
    installation — so a repository with a `release` job of its own has steps
    no row has ever heard of.

    Counting them as unanswered is honest; telling their reader the reason is
    in `PARTITION` is not, because `PARTITION` holds thirteen rows about a
    workflow that repository does not run. A reader who follows the pointer
    finds somebody else's list and no answer, which is the reconstruction
    from two files this work item exists to remove, one level further out."""
    said = gate.coverage_line(UNCLASSIFIED_WORKFLOW)
    assert "deploy to staging" in said, said
    with_reasons = said.split("no arm mirrors it in", 1)
    assert len(with_reasons) == 1 or "deploy to staging" not in with_reasons[1], (
        f"a step in no row of PARTITION is named among the ones PARTITION "
        f"gives a reason for:\n{said}"
    )
    assert "no row of `broad_gate.py#PARTITION` at all" in said, said


def test_a_step_a_row_excludes_is_still_pointed_at_its_reason():
    """The other half, and what keeps the case above from being answered by
    deleting the pointer. A step the partition DOES exclude carries a written
    reason, and naming where it is written is the whole of `spec.md` §Scope
    5."""
    said = gate.coverage_line(read(HYGIENE))
    assert "no arm mirrors it in `broad_gate.py#PARTITION`" in said, said
    assert "both READMEs move together" in said.split("no arm mirrors it in", 1)[1]
    assert "no row of `broad_gate.py#PARTITION` at all" not in said, said


MIXED_WORKFLOW = """\
name: hygiene

on:
  pull_request:

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: a declared review chain has the round record it claimed
        run: true
      - name: both READMEs move together
        run: true
      - name: deploy to staging
        run: true
"""


def test_the_two_clauses_render_together_and_hold_the_right_names():
    """Round 2's coverage note. The two cases above each exercise one clause
    — `UNCLASSIFIED_WORKFLOW` leaves `excluded` empty and this repository's
    own workflow leaves `unknown` empty — so the JOINED sentence, which is
    the one a mixed repository's reader actually has to parse, was rendered
    by nothing.

    The two comprehensions are disjoint by construction, which is why the
    reviewer called this a coverage note rather than a defect. It is still
    the sentence that goes wrong if either clause ever learns to claim the
    other's steps."""
    said = gate.coverage_line(MIXED_WORKFLOW)
    assert "runs 3 steps and this seal answers 1" in said, said

    reasoned, _, unknown = said.partition(
        "In no row of `broad_gate.py#PARTITION` at all"
    )
    assert unknown, f"the second clause did not render at all:\n{said}"
    assert "no arm mirrors it in `broad_gate.py#PARTITION`" in reasoned, said

    assert "both READMEs move together" in reasoned, said
    assert "both READMEs move together" not in unknown, (
        f"a step `PARTITION` excludes with a reason is named among the ones "
        f"it has never heard of:\n{said}"
    )
    assert "deploy to staging" in unknown, said
    assert "deploy to staging" not in reasoned, (
        f"a step in no row of `PARTITION` is named among the ones it gives a "
        f"reason for:\n{said}"
    )
    assert "a declared review chain has the round record it claimed" not in said, (
        f"a step the gate DOES mirror is named as unanswered:\n{said}"
    )
