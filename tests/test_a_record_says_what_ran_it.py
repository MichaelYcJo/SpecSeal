"""What ran the round, executed — what `chain_check.py` refuses.

Phase 1 wrote the row down in both record templates and in the handoff
protocol. A row no check reads is true only while somebody is awake, which is
the finding #110's review already paid for once: `Needs a fix` sat in the
template from draft 0.5 with nothing reading it, and the template said so of
itself. These are the cases that make `Ran by` enforceable.

  Ran by   absent (after `RUNNER_FROM`) fails and prints before it. Present
           and unreadable fails on ANY record: empty, a bare `unknown` with
           no reason, or a cell naming ONE thing where the row's whole
           purpose is two

The two-halves rule is the part worth stating twice. An agent without a model
cannot be compared against another run of the same agent, and a model without
an agent cannot be told apart from the orchestrating session's own turns —
which is exactly what #145 is about, and what #84's last line waits on.

The grandfathering is the work item's own id, `RUNNER_FROM`, the fourth cutoff
of the shape `STRICT_FROM`, `SURFACE_FROM` and `FLOOR_FROM` already carry: a
merged record has no honest repair — nobody can recover what ran a segment
whose session is over — and a check whose first production act is red on
history nobody can fix is a check people learn to skip.

The sibling prose cases live in
`tests/test_a_phase_hands_the_next_one_a_record.py` (the phase template's row)
and `tests/test_the_fixes_name_their_surface.py` (the protocol's field table).
What is here is execution: a fixture repository, the checker run on it, and the
exit code read.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")

# A work item begun before the cutoff: a missing row prints.
OLD_ITEM = "seal/specs/1787700000-a-work-item"
# One begun after it: a missing row fails. The two differ only in the second
# their names start with, which is the whole of what the grandfathering reads.
NEW_ITEM = "seal/specs/1799000000-a-later-work-item"

# The value the templates show, as a session would copy it.
RUNNER = "specseal:smith on Opus 5 (1M context)"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_module():
    """`chain_check.py` itself, for the cutoff and the vocabulary — typed
    here, the boundary cases would pin a number instead of the boundary."""
    return _load("specseal_runner_check_for_tests", CHECK)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


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
    d = tmp_path_factory.mktemp("ran-by-template") / "repo"
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


def record(sha, ran_by=RUNNER):
    """A record that passes every check but the one row each case is about.

    The verdict closes without a fix and `Fixes checked by` says so, so `Pass`
    beside `nobody` never fires; the fix-surface rows and the floor are `none`
    and `no` for the same reason. `ran_by=None` leaves the row out entirely,
    which is the state the grandfathering decides.
    """
    rows = (
        "| Fixes checked by | no fixes to check |\n"
        "| Contract changes | none |\n"
        "| New units | none |\n"
        "| Needs a fix | no |\n"
        "| Loses a record or crashes | no |\n"
    )
    if ran_by is not None:
        rows += f"| Ran by | {ran_by} |\n"
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n{rows}\n"
        "- [x] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        "| 🟢 1 | something | `f.py:1` | answered | grounds |\n"
    )


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


def declared(repo, item, *bodies):
    """The declaration, then one record per body, each in its own commit.

    Each record is handed the HEAD that existed before it, so round 2's
    `Target SHA` is a descendant of round 1's — what a real run looks like,
    since the fixes are what moved HEAD between the rounds. The same shape
    `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` uses, and
    for the same reason: the every-record claim cannot be tested with one
    record.
    """
    write(repo, f"{item}/routing.md", declaration(item))
    sha = commit(repo, "declare")
    for number, body in enumerate(bodies, start=1):
        write(repo, f"{item}/rounds/round-{number}.md", body(sha))
        sha = commit(repo, f"round {number}")
    return sha


# --- the row is absent ------------------------------------------------------


def test_an_absent_row_fails_after_the_cutoff(repo):
    """The refusal this work item exists for. Every segment measured before
    it landed is one nothing can attribute afterwards."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, ran_by=None))
    code, out = run(repo)
    assert code == 1, out
    assert "Ran by" in out
    assert "what executed it" in out


def test_an_absent_row_only_prints_before_the_cutoff(repo):
    """A merged record has no honest repair: the session that would know
    what ran the segment is over, and a value invented now is worse than the
    blank — a reading nobody can trust reads exactly like one nobody took."""
    declared(repo, OLD_ITEM, lambda sha: record(sha, ran_by=None))
    code, out = run(repo)
    assert code == 0, out
    assert "Ran by" in out, (
        "passing in silence would hide the state the row exists to surface"
    )
    assert "prints instead of failing" in out


def test_a_work_item_with_no_timestamp_prefix_is_grandfathered(repo):
    """Round 1's 🟡 3. `item_began` answers None for a work item named some
    other way, and None is below every cutoff — failing would fail a naming
    convention rather than a state anybody chose.

    The arm had no case anywhere. All three sibling suites carry one, and
    this branch is what took their coverage away: making each `record()`
    helper always emit `Ran by` left every one of them running with the row
    PRESENT, so none of them reaches this arm any more. Remove `began is
    None` from the guard and `None < int` raises, with nothing red.
    """
    declared(
        repo,
        "seal/specs/a-work-item-with-no-date",
        lambda sha: record(sha, ran_by=None),
    )
    code, out = run(repo)
    assert code == 0, out
    assert "Ran by" in out, (
        "passing in silence would hide the state the row exists to surface"
    )


def test_the_row_is_read_on_every_record_not_only_the_last(repo):
    """Round 1's 🟡 2. The every-record choice was written down twice as a
    decision and held by nothing.

    **This case cannot be red at HEAD**, because the behaviour it pins is
    already correct there — it is red only under the mutation that narrows
    `ran_by` to the last record, which is how §15 was satisfied for it.
    Measured before the case existed: that narrowing left 272 cases green
    across the five suites reading `chain_check.py`. Do not delete this as a
    case that never fails.

    What it protects is the comparison the row exists to make. A work item
    whose rounds ran under different runners — a cheaper model on round 2,
    say — is exactly what anyone reading the measurement log wants to see,
    and a check reading the last record alone answers it for one round.
    """
    declared(repo, NEW_ITEM, lambda sha: record(sha, ran_by=None), record)
    code, out = run(repo)
    assert code == 1, out
    assert "round-1.md" in out, (
        "the earlier record is missing the row and the failure does not name "
        "it, so the check is reading the last record alone"
    )


def test_the_cutoff_is_the_work_items_own_second(repo):
    """The boundary, read off the module rather than typed — a literal here
    would pin the number and not the rule."""
    began = check_module().RUNNER_FROM
    item = f"seal/specs/{began}-the-item-that-added-the-rule"
    declared(repo, item, lambda sha: record(sha, ran_by=None))
    code, out = run(repo)
    assert code == 1, (
        "the work item that ADDED the rule is the first one held to it, and "
        f"{began} is its own second — `>=`, not `>`"
    )
    assert "Ran by" in out


# --- the row is there and says something --------------------------------


def test_the_form_the_templates_show_passes(repo):
    """Copied from `templates/sdd-round.md` as a session would write it. A
    vocabulary whose own documented spelling is refused teaches the refusal
    and not the spelling."""
    declared(repo, NEW_ITEM, record)
    code, out = run(repo)
    assert code == 0, out


def test_a_model_name_may_carry_spaces_and_brackets(repo):
    """`Opus 5 (1M context)` is a real model name, and the split takes the
    FIRST ` on ` so everything after it is the model however it is spelled."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, "the session on Opus 5 (1M)"))
    code, out = run(repo)
    assert code == 0, out


def test_backticks_do_not_change_the_answer(repo):
    """`EMPHASIS` strips them, the way it does for every other cell — a
    record is prose a person writes, and code-spanning a value is what a
    person does to it."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, "`specseal:warden` on `a model`"))
    code, out = run(repo)
    assert code == 0, out


@pytest.mark.parametrize("item", [OLD_ITEM, NEW_ITEM])
def test_unknown_with_a_reason_is_an_answer(repo, item):
    """`agents/*.md` pins no model — it is a spawn-time argument — so a
    session spawning through another harness may genuinely have no name for
    one. Accepted at ANY age: the honest answer is not a thing the cutoff
    grandfathers, it is the answer."""
    declared(
        repo, item, lambda sha: record(sha, "unknown — spawned through another harness")
    )
    code, out = run(repo)
    assert code == 0, out


# --- the row is there and says nothing ---------------------------------


@pytest.mark.parametrize("item", [OLD_ITEM, NEW_ITEM])
def test_a_bare_unknown_is_not_an_answer(repo, item):
    """The `nobody — <why>` rule, one row over: without the reason the cell
    records that something is missing and not what.

    Refused at BOTH ages, which is the split `fix_surface` makes and the
    reason for it — an absent row is a review nobody can repair, and a
    present one is formatting, which is always the author's.
    """
    declared(repo, item, lambda sha: record(sha, "unknown"))
    code, out = run(repo)
    assert code == 1, out
    assert "no reason after it" in out


@pytest.mark.parametrize("item", [OLD_ITEM, NEW_ITEM])
def test_an_empty_cell_is_not_an_answer(repo, item):
    declared(repo, item, lambda sha: record(sha, ""))
    code, out = run(repo)
    assert code == 1, out
    assert "answers nothing" in out


@pytest.mark.parametrize("value", ["specseal:smith", "Opus 5", "the orchestrator"])
def test_one_thing_named_is_not_two(repo, value):
    """The rule the spec fixed and left the plan no room to soften: the row
    names the agent AND the model.

    A model alone cannot be told from the orchestrating session's own turns,
    and an agent alone cannot be compared against another run of itself —
    which is the comparison #145 needs and the one #84's `time per agent`
    waits on.
    """
    declared(repo, NEW_ITEM, lambda sha: record(sha, value))
    code, out = run(repo)
    assert code == 1, out
    assert "names one thing" in out


@pytest.mark.parametrize("value", ["monitor", "carbon"])
def test_the_on_must_stand_alone(repo, value):
    """Whitespace on BOTH sides, so the `on` inside a name is not the
    separator. Each of these is one thing however it is spelled.

    `monitor` is the case that pins the rule and `carbon` is the one that
    looks like it does. Dropping the whitespace from `ON_RE` leaves `carbon`
    refused anyway — it splits into `carb` and an empty tail, and an empty
    half is refused by the very next clause — so a case carrying only that
    word stays green against the mutation it exists to catch. `monitor`
    splits into two non-empty halves and is the one that goes red.
    """
    declared(repo, NEW_ITEM, lambda sha: record(sha, value))
    code, out = run(repo)
    assert code == 1, out
    assert "names one thing" in out


def test_a_row_inside_a_comment_is_not_the_row(repo):
    """One reader, not two: the template explains the row in a comment
    beside it, and an explanation must not read as an answer.

    Round 1's 🟡 5 is why this goes through `declared()` like every other
    case here. It used to hand-build the fixture with a `Target SHA` of forty
    zeroes, and that SHA is unreachable — so the exit code was 1 whatever the
    comment held. Moving the row out of the comment, making it a legitimate
    answer, still exited 1. The needle below did catch that, so it was never
    a hole; it is the class named in this work item's own phase 4 arriving a
    third time, and this time in the exit code rather than in a needle.

    With a real SHA the exit code means what the case says it means, and the
    two assertions now fail together rather than one propping up the other.
    """
    body = record("PLACEHOLDER", ran_by=None).replace(
        "- [x] Pass",
        f"<!--\n| Ran by | {RUNNER} |\n-->\n\n- [x] Pass",
    )
    declared(repo, NEW_ITEM, lambda sha: body.replace("PLACEHOLDER", sha))
    code, out = run(repo)
    assert code == 1, out
    assert "Ran by" in out


# --- the behaviour spec states the refusal and names its cutoff ------------


def test_the_behaviour_spec_carries_a_subsection_for_this_refusal():
    """Round 1's 🟡 1. `docs/review-chain-spec.md` owns every refusal the
    checker makes at the pull request, and this one arrived without a
    subsection while `Pass`, `Fixes checked by`, the fix-surface rows, the
    floor, `Needs a fix` and the depth each have one.

    The grounds first offered for leaving it out — *that file owns the cap
    and the floor, and `Ran by` is neither* — do not survive reading it:
    `Contract changes` and `New units` make no claim about when a run stops
    either, and they have a subsection with their cutoff named beside them.
    """
    text = read("docs", "review-chain-spec.md")
    assert "##### What ran the round" in text, (
        "the behaviour spec has a subsection for every other refusal the "
        "checker makes and none for this one, so the only statement of what "
        "it refuses is the code that does the refusing"
    )
    assert "RUNNER_FROM" in text, (
        "the subsection does not name the cutoff, where every neighbour "
        "names its own — a reader cannot tell which records are excused"
    )


def test_the_documents_say_why_older_records_are_excused():
    """The sibling arrangement `SURFACE_FROM` already has: a constant with no
    reason beside it reads as a leftover, and removing it turns a release
    pull request red on merged history."""
    for parts in (
        ("docs", "review-chain-spec.md"),
        ("skills", "code-review", "scripts", "chain_check.py"),
    ):
        text = flat(*parts)
        assert "RUNNER_FROM" in text, "/".join(parts)


def test_the_spec_states_the_two_halves_and_the_unknown_answer():
    """A table a session reads instead of the template has to teach the same
    vocabulary, or a record written from THIS document is refused."""
    text = flat("docs", "review-chain-spec.md")
    for needle in ("agent on model", "unknown — <why>", "bare `unknown`"):
        assert needle in text, (
            f"the spec's `Ran by` subsection does not state `{needle}`, so a "
            "record written from it meets a refusal the document never named"
        )


# --- the skills that tell a session to fill it -----------------------------


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(*parts).split())


# Every shipped file that instructs a session to write one of these records,
# with what each has to carry. A file that shows the record's rows and omits
# this one sends its reader to write a record `chain_check.py` refuses — the
# failure this repository has now paid for three times, and the reason phase 1
# landed before phase 2.
#
# The needle differs by KIND, and it has to. The three files that carry the
# row AS A ROW are pinned on the row: checking the bare name there passed
# against a mutation renaming `| Ran by |` to `| Run by |`, because those
# files also say `Ran by` in prose around it. The two skills carry no table,
# so the name is all there is to pin.
INSTRUCTORS = [
    (("skills", "code-review", "SKILL.md"), "Ran by"),
    (("skills", "verify", "SKILL.md"), "Ran by"),
    (("docs", "review-handoff-protocol.md"), "| Ran by |"),
    (("templates", "sdd-round.md"), "| Ran by |"),
    (("templates", "sdd-phase.md"), "| Ran by |"),
]


@pytest.mark.parametrize("parts,needle", INSTRUCTORS)
def test_every_instructing_file_names_the_row(parts, needle):
    assert needle in read(*parts), "/".join(parts)


@pytest.mark.parametrize(
    "parts", [("skills", "code-review", "SKILL.md"), ("skills", "verify", "SKILL.md")]
)
def test_the_skills_say_the_spawning_session_fills_it(parts):
    """The one thing a reader cannot infer from the row itself.

    Shown without it, the row reads as something the segment reports about
    itself — and the subject is the one filler whose answer nothing can check
    against anything. Both skills have to carry it because they are read by
    different sessions at different moments: `code-review` by the
    orchestrator writing the round record, `verify` by whoever watches a
    segment end and posts its numbers.
    """
    text = flat(*parts)
    assert "spawn" in text and "Ran by" in text, "/".join(parts)
    assert "value it writes about itself is the value it was told" in text, (
        f"{'/'.join(parts)} shows the row without saying whose it is, so the "
        "filler it invites is the subject — the one whose answer cannot be "
        "checked against anything"
    )


def test_verify_says_how_a_phase_record_comes_to_carry_the_row():
    """`skills/verify/SKILL.md` covers BOTH records, and only one of them is
    written by the session that knows the answer.

    `rounds/round-N.md` is the orchestrator's file, so *you fill it* is one
    act. `phases/phase-N.md` is written by the segment that just ran, so a
    skill saying *it is yours and not the segment's* and stopping there has
    told the orchestrator to fill a row in a file it does not write. The two
    ways out — hand the value over in the spawn prompt, or fill the row
    afterwards — are what make the rule performable rather than merely true.
    """
    text = flat("skills", "verify", "SKILL.md")
    assert "that record is written by the segment" in text, (
        "the skill does not say a phase record is written by somebody other "
        "than the session holding the answer, so the rule above it reads as "
        "an instruction nobody can carry out"
    )
    assert "hand the value over in the spawn prompt" in text


@pytest.mark.parametrize(
    "parts", [("skills", "code-review", "SKILL.md"), ("skills", "verify", "SKILL.md")]
)
def test_the_skills_offer_the_unknown_answer(parts):
    """A skill teaching only the confident answer gets the confident answer
    written, true or not. `agents/*.md` pins no model."""
    text = flat(*parts)
    assert "unknown — <why>" in text, "/".join(parts)
    assert "bare `unknown`" in text, (
        f"{'/'.join(parts)} offers `unknown` without saying the reason is "
        "required, and a cell with no reason records that something is "
        "missing and not what"
    )


# --- the parser, without a repository around it ----------------------------


@pytest.mark.parametrize(
    "value",
    [
        RUNNER,
        "specseal:warden on a model",
        "unknown — no name for it",
        "unknown, the harness does not say",
        "UNKNOWN — shouted, still an answer",
        "a on b",
    ],
)
def test_the_parser_accepts(value):
    assert check_module().runner_problem(value) is None, value


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        "unknown",
        "UNKNOWN",
        "unknown —",
        "smith",
        "on",
        "on model",
        "x on",
        # The mutation `carbon` alone does not catch: with the whitespace
        # gone from `ON_RE` this splits into two non-empty halves and passes.
        "monitor",
        "carbon",
    ],
)
def test_the_parser_refuses(value):
    assert check_module().runner_problem(value) is not None, value


def test_the_recorded_limit_an_unknown_that_leads_with_on():
    """`unknown on Opus` is an unknown WITH A REASON, not a half-named pair.

    Recorded rather than parsed away, the way `fix_surface` records its own
    three. Nothing is lost by the limit — the model is still written where a
    reader sees it.
    """
    check = check_module()
    assert check.runner_problem("unknown on Opus") is None
    assert check.runner_problem("unknown — not recorded on this run") is None


def test_the_arm_order_changes_the_reading_and_never_the_verdict():
    """Round 1's 🟡 4. The docstring claimed the order was load-bearing and
    three durable records disagreed about it; this is the claim that stands.

    Whether a cell is accepted does not depend on the order, and it cannot:
    the `unknown` arm refuses when nothing follows the separator, and nothing
    following means there is no ` on ` in the tail either. So every cell that
    would split is one the `unknown` arm accepts anyway.

    What the order settles is what the cell was read AS, which reaches a
    person only through the message. The pair below is the whole difference:
    under the other order the first would be a pair whose agent is the reason
    and whose model is `this run`, and it would still be accepted.
    """
    check = check_module()
    for value in ("unknown — not recorded on this run", "unknown on Opus"):
        assert check.runner_problem(value) is None, value
    # The by-construction half, asserted rather than described: a cell the
    # `unknown` arm REFUSES has no ` on ` left in it to split on either.
    bare = "unknown"
    assert check.runner_problem(bare) is not None
    assert check.ON_RE.search(bare) is None, (
        "a bare `unknown` with something splittable in it would be the one "
        "cell where the two orders could disagree about the verdict"
    )
