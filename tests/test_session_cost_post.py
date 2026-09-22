"""`session_cost.py --post` posts one segment's reading, or refuses.

Issue #330. Of the three acts the ticket measured a miss for, two closed
while it sat and one is still a sentence: posting the segment's reading to
the flow log, written out in full in `skills/verify/SKILL.md` §*Measure the
segment, and feed the flow log* and typed by nobody. This is that procedure
as a command, and this module is what holds it.

**Nothing here touches a network.** Every case replaces the module's own
`run_gh`, which is the single seam every `gh` call goes through, and records
the argv it was handed. That is what lets a case assert the two properties
the prose cares about most: that an issue is never opened, and that nothing
is posted in any state but the one open log.

The five states, and the exit each ends on:

  no `--says`                   exit 2, nothing looked up  (A5)
  the label has no history      exit 0, nothing posted     (A6)
  history and nothing open      exit 1, nothing opened     (A7)
  more than one open            exit 1, both named         (A8)
  exactly one open              exit 0, one comment        (A9)

**Red-first, per the contract's §15.** Every case here was run against
`session_cost.py` before the mode existed: `--post` was not a flag, so
argparse exited 2 on all of them, and only A5 was red for its own reason.
The phase record names the run. After the mode landed, each unit it added was
broken one at a time and the module re-run, and the mutations are in that
record too.
"""

import importlib.util
import io
import json
import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "session_cost.py")


def _cost():
    """The script, imported so `run_gh` can be replaced.

    Imported rather than shelled out for the reason
    `tests/test_a_release_rolls_the_flow_measurement_issue.py` records for
    its own neighbour: the seam is a module attribute, and a subprocess would
    have to be handed a stub on PATH to reach it.
    """
    spec = importlib.util.spec_from_file_location("session_cost_for_post", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _listing(*issues):
    """What `gh issue list --json number,state` hands back."""
    return json.dumps([{"number": n, "state": s} for n, s in issues])


def _gh(monkeypatch, module, listing=None, list_code=0, comment_code=0, stderr=""):
    """Replace `run_gh` and return the list of argvs it was given."""
    seen = []

    def fake(args):
        seen.append(list(args))
        if args[:2] == ["issue", "list"]:
            return list_code, ("[]" if listing is None else listing), stderr
        if args[:2] == ["issue", "comment"]:
            return comment_code, "", stderr
        raise AssertionError(f"no case expects `gh {' '.join(args)}`")

    monkeypatch.setattr(module, "run_gh", fake)
    return seen


def _opened(seen):
    """Whether any call would have created an issue."""
    return [a for a in seen if a[:2] == ["issue", "create"]]


def _posted(seen):
    return [a for a in seen if a[:2] == ["issue", "comment"]]


# --- A5: the reading is the orchestrator's, and the command refuses without it


def test_post_without_says_refuses_and_says_where_the_reading_comes_from(
    monkeypatch, capsys, tmp_path
):
    """A5. `parser.error` exits 2, and the message names both ways in: a file
    and `-`. The refusal has to carry that, because the whole point is that
    the command will not write the sentence itself."""
    module = _cost()
    seen = _gh(monkeypatch, module)
    monkeypatch.setattr(module.sys, "argv", ["session_cost.py", "x.jsonl", "--post"])
    with pytest.raises(SystemExit) as exit_info:
        module.main()
    assert exit_info.value.code == 2
    said = capsys.readouterr().err
    assert "--says" in said
    assert "stdin" in said and "invented" in said
    assert seen == [], "nothing may be looked up before the refusal"


def test_post_with_json_refuses(monkeypatch, capsys):
    """The two ask for different things — one posts, one prints for a program
    — and silently preferring either is a reading somebody does not get."""
    module = _cost()
    monkeypatch.setattr(
        module.sys,
        "argv",
        ["session_cost.py", "x.jsonl", "--post", "--says", "-", "--json"],
    )
    with pytest.raises(SystemExit) as exit_info:
        module.main()
    assert exit_info.value.code == 2
    assert "separately" in capsys.readouterr().err


def test_says_reads_from_stdin(monkeypatch):
    """`--says -` is the form a session already has the sentence in hand for."""
    module = _cost()
    monkeypatch.setattr(module.sys, "stdin", io.StringIO("the segment ran long\n"))
    assert module.read_says("-").strip() == "the segment ran long"


def test_says_reads_from_a_file(tmp_path):
    module = _cost()
    path = tmp_path / "says.md"
    path.write_text("nine rounds, and the cap never bound\n", encoding="utf-8")
    assert "nine rounds" in module.read_says(str(path))


# --- A6: a repository that never made the log is the expected case ------------


def test_no_history_posts_nothing_and_does_not_fail(monkeypatch, capsys):
    """A6. Measured 2026-09-22 (`questions.md` Q1): the lookup exits 0 with
    empty output where the label exists nowhere. Most installed repositories
    are in that state, so a command that went red here would be red for
    following the document beside it."""
    module = _cost()
    seen = _gh(monkeypatch, module, listing="[]")
    code = module.post("the reading", "what it says", "flow-measurement")
    assert code == 0
    said = capsys.readouterr().out
    assert "does not run that log" in said
    assert _posted(seen) == [] and _opened(seen) == []


def test_an_unreadable_lookup_is_a_no_op_and_never_a_post(monkeypatch, capsys):
    """A non-zero exit is a lookup that FAILED, which is a different fact
    from an absent label — and `plan.md`'s failure direction says a wrong
    guess must cost a refusal and never a wrong post."""
    module = _cost()
    seen = _gh(
        monkeypatch, module, list_code=1, stderr="could not resolve to a Repository"
    )
    code = module.post("the reading", "what it says", "flow-measurement")
    assert code == 0
    said = capsys.readouterr().out
    assert "could not run" in said and "could not resolve" in said
    assert _posted(seen) == [] and _opened(seen) == []


def test_gh_missing_from_path_is_the_same_no_op(monkeypatch, capsys):
    """`run_gh` answers `None` for a `gh` that is not installed, which the
    caller must not read as the exit code 0 that `None` is not."""
    module = _cost()
    seen = _gh(monkeypatch, module, list_code=None, stderr="no gh")
    assert module.post("r", "s", "flow-measurement") == 0
    assert "not on PATH" in capsys.readouterr().out
    assert _posted(seen) == [] and _opened(seen) == []


# --- A7: a closed log is named, never reopened --------------------------------


def test_a_closed_log_is_named_and_nothing_is_opened(monkeypatch, capsys):
    """A7. Opening one is not a session's act: two sessions finishing
    segments at once both read zero and both create, and the next release
    fails on two or more."""
    module = _cost()
    seen = _gh(monkeypatch, module, listing=_listing((41, "CLOSED"), (40, "CLOSED")))
    code = module.post("the reading", "what it says", "flow-measurement")
    assert code == 1
    said = capsys.readouterr().out
    assert "nothing is open" in said
    assert "not a session's act" in said
    assert _opened(seen) == [], "a closed log must never be reopened"
    assert _posted(seen) == []


# --- A8: a broken invariant is named, not guessed past ------------------------


def test_more_than_one_open_is_named_and_nothing_is_posted(monkeypatch, capsys):
    """A8. Both numbers in the message, because picking the current log is
    what a person does next."""
    module = _cost()
    seen = _gh(
        monkeypatch,
        module,
        listing=_listing((42, "OPEN"), (41, "OPEN"), (40, "CLOSED")),
    )
    code = module.post("the reading", "what it says", "flow-measurement")
    assert code == 1
    said = capsys.readouterr().out
    assert "#41" in said and "#42" in said
    assert "exactly one may" in said
    assert _posted(seen) == [] and _opened(seen) == []


# --- A9: exactly one open posts once ------------------------------------------


def test_one_open_posts_once_to_that_issue(monkeypatch, capsys):
    """A9. The argv is asserted, not just the exit: what makes this mode
    worth having is that the command is composed the same way every time."""
    module = _cost()
    seen = _gh(monkeypatch, module, listing=_listing((42, "OPEN"), (41, "CLOSED")))
    bodies = {}
    real = module.run_gh

    def capture(args):
        if args[:2] == ["issue", "comment"]:
            with open(args[args.index("--body-file") + 1], encoding="utf-8") as handle:
                bodies["text"] = handle.read()
        return real(args)

    monkeypatch.setattr(module, "run_gh", capture)
    code = module.post("span 19m, 99 calls", "the rounds ran long", "flow-measurement")
    assert code == 0
    posted = _posted(seen)
    assert len(posted) == 1, posted
    assert posted[0][:3] == ["issue", "comment", "42"]
    assert "--body-file" in posted[0]
    assert _opened(seen) == []
    assert "posted the segment's reading to #42" in capsys.readouterr().out
    assert "the rounds ran long" in bodies["text"]
    assert "span 19m, 99 calls" in bodies["text"]


def test_the_body_file_is_removed_after_the_post(monkeypatch):
    """A temp file per segment boundary, left behind, is the leaving
    `agent-contract` §7 is about — and this one is the command's, not a
    probe's, so nothing else would ever clean it."""
    module = _cost()
    paths = []
    seen = _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    real = module.run_gh

    def capture(args):
        if args[:2] == ["issue", "comment"]:
            paths.append(args[args.index("--body-file") + 1])
        return real(args)

    monkeypatch.setattr(module, "run_gh", capture)
    module.post("r", "s", "flow-measurement")
    assert paths and not os.path.exists(paths[0])
    assert seen


def test_a_comment_that_fails_to_post_is_named_and_fails(monkeypatch, capsys):
    """The one state where the log was found and the write did not land.
    Silently exiting 0 there is the counterfeit: the reading is gone and the
    log looks fed."""
    module = _cost()
    _gh(
        monkeypatch,
        module,
        listing=_listing((42, "OPEN")),
        comment_code=1,
        stderr="HTTP 403",
    )
    assert module.post("r", "s", "flow-measurement") == 1
    assert "was not posted" in capsys.readouterr().out


# --- the lookup and the body --------------------------------------------------


def test_the_lookup_reads_the_label_and_the_whole_history(monkeypatch):
    """One call, not two. `--state all` answers both of the skill's
    questions, because every open issue is in it — and the limit is raised
    off the default so a label with more than thirty closed logs does not
    read as one that never existed."""
    module = _cost()
    seen = _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    module.open_log("flow-baseline")
    assert len(seen) == 1, seen
    argv = seen[0]
    assert argv[:2] == ["issue", "list"]
    assert argv[argv.index("--label") + 1] == "flow-baseline"
    assert argv[argv.index("--state") + 1] == "all"
    assert int(argv[argv.index("--limit") + 1]) > 30


def test_the_durable_log_is_reachable_under_its_own_label(monkeypatch, capsys):
    """`skills/verify/SKILL.md` names two logs and says a cross-version
    reading posted to the rolling one is scheduled for deletion. One flag is
    what keeps the durable one reachable with the same code."""
    module = _cost()
    seen = _gh(monkeypatch, module, listing=_listing((7, "OPEN")))
    assert module.post("r", "s", "flow-baseline") == 0
    assert seen[0][seen[0].index("--label") + 1] == "flow-baseline"
    assert _posted(seen)[0][2] == "7"


def test_the_default_label_is_the_rolling_log():
    module = _cost()
    assert module.ROLLING_LABEL == "flow-measurement"


def test_the_body_carries_the_judgment_before_the_numbers():
    """What a reader of the log came for is what the numbers say. The reading
    is fenced below it so the report's columns survive markdown."""
    module = _cost()
    body = module.comment_body("agent   span   calls\nsmith   19m    99", "it ran long")
    assert body.index("it ran long") < body.index("agent")
    assert "```" in body


def test_unreadable_json_is_a_no_op_rather_than_a_crash(monkeypatch, capsys):
    """`gh` answering something that is not the JSON it was asked for is a
    lookup that did not work, and it takes the same exit as one that failed
    outright."""
    module = _cost()
    seen = _gh(monkeypatch, module, listing="not json at all")
    assert module.post("r", "s", "flow-measurement") == 0
    assert "could not run" in capsys.readouterr().out
    assert _posted(seen) == [] and _opened(seen) == []


@pytest.mark.parametrize(
    "listing, expected",
    [
        ("[]", "no history"),
        (_listing((1, "CLOSED")), "closed"),
        (_listing((1, "OPEN")), "one open"),
        (_listing((1, "OPEN"), (2, "OPEN")), "many open"),
    ],
)
def test_the_four_states_are_read_off_one_listing(monkeypatch, listing, expected):
    module = _cost()
    _gh(monkeypatch, module, listing=listing)
    state, _payload = module.open_log("flow-measurement")
    assert state == expected


# --- through `main`, which is where `emit` lives ------------------------------


def _row(second, block):
    return json.dumps(
        {
            "timestamp": f"2026-09-22T00:{second // 60:02d}:{second % 60:02d}.000Z",
            "message": {"content": [block], "usage": {"input_tokens": 1000}},
        }
    )


@pytest.fixture
def transcript(tmp_path):
    """The smallest transcript with a paired call in it, built the way
    `tests/test_session_cost.py` builds its own."""
    path = tmp_path / "t.jsonl"
    path.write_text(
        "\n".join(
            [
                _row(
                    0,
                    {
                        "type": "tool_use",
                        "id": "a",
                        "name": "Bash",
                        "input": {"command": "pytest tests -q"},
                    },
                ),
                _row(10, {"type": "tool_result", "tool_use_id": "a"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def test_main_posts_the_report_it_would_have_printed(
    monkeypatch, capsys, tmp_path, transcript
):
    """`emit` is the seam between printing a reading and posting it, and the
    body has to carry the same text either way. A mode that posted an empty
    body would look identical in every argv assertion above."""
    module = _cost()
    says = tmp_path / "says.md"
    says.write_text("one call, ten seconds of it\n", encoding="utf-8")
    seen = _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    bodies = {}
    stub = module.run_gh

    def capture(args):
        if args[:2] == ["issue", "comment"]:
            with open(args[args.index("--body-file") + 1], encoding="utf-8") as handle:
                bodies["text"] = handle.read()
        return stub(args)

    monkeypatch.setattr(module, "run_gh", capture)
    monkeypatch.setattr(
        module.sys,
        "argv",
        ["session_cost.py", str(transcript), "--post", "--says", str(says)],
    )
    assert module.main() == 0
    assert _posted(seen)[0][2] == "42"
    assert "one call, ten seconds of it" in bodies["text"]
    # The report's own words, so the body is the reading rather than an empty
    # fence with the sentence above it.
    assert "command" in bodies["text"]
    printed = capsys.readouterr().out
    assert "posted the segment's reading to #42" in printed


def test_the_posted_body_does_not_carry_the_transcripts_path(
    monkeypatch, tmp_path, transcript
):
    """Round 1's 🔴. `--post` writes into an issue tracker and a transcript
    path lives under the user's home directory, carrying the account name
    twice and the session id once. The report prints it; the body must not.

    The branch that leaks is the documented one: `report_segments`' empty
    branch fires whenever the named transcript has no subagents beside it,
    which is every segment measured on its own — the case
    `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*
    is written for.
    """
    module = _cost()
    says = tmp_path / "says.md"
    says.write_text("one call, ten seconds of it\n", encoding="utf-8")
    _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    bodies = {}
    stub = module.run_gh

    def capture(args):
        if args[:2] == ["issue", "comment"]:
            with open(args[args.index("--body-file") + 1], encoding="utf-8") as handle:
                bodies["text"] = handle.read()
        return stub(args)

    monkeypatch.setattr(module, "run_gh", capture)
    monkeypatch.setattr(
        module.sys,
        "argv",
        [
            "session_cost.py",
            str(transcript),
            "--segments",
            "--post",
            "--says",
            str(says),
        ],
    )
    assert module.main() == 0
    assert str(transcript) not in bodies["text"]
    assert os.path.dirname(str(transcript)) not in bodies["text"]
    # The basename stays, because a reading that names no file is a reading
    # nobody can place.
    assert os.path.basename(str(transcript)) in bodies["text"]


def test_the_spawns_report_leaks_no_path_either(monkeypatch, tmp_path, transcript):
    """The same empty branch, one report over. `report_spawns` prints
    `0 spawns found in {path}` and reaches the body through the same seam, so
    fixing one call site and not the other is the shape the finding is about:
    the rule was already in the file and applied in one place of three."""
    module = _cost()
    says = tmp_path / "says.md"
    says.write_text("no spawns in this one\n", encoding="utf-8")
    _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    bodies = {}
    stub = module.run_gh

    def capture(args):
        if args[:2] == ["issue", "comment"]:
            with open(args[args.index("--body-file") + 1], encoding="utf-8") as handle:
                bodies["text"] = handle.read()
        return stub(args)

    monkeypatch.setattr(module, "run_gh", capture)
    monkeypatch.setattr(
        module.sys,
        "argv",
        [
            "session_cost.py",
            str(transcript),
            "--spawns",
            "--post",
            "--says",
            str(says),
        ],
    )
    assert module.main() == 0
    assert os.path.dirname(str(transcript)) not in bodies["text"]


def test_an_empty_reading_is_refused_rather_than_posted(
    monkeypatch, capsys, tmp_path, transcript
):
    """Round 1's second finding. The invariant is that the numbers are the
    script's and the sentence is not, and `spec.md` §Scope states it as *it
    refuses to post without a reading* — not without the flag. Enforced
    against the missing flag alone, a `--says` naming an empty file posts a
    fence with nothing above it, which is the shape a session reaches by
    accident with `--says -` and nothing piped in."""
    module = _cost()
    says = tmp_path / "empty.md"
    says.write_text("   \n", encoding="utf-8")
    seen = _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    monkeypatch.setattr(
        module.sys,
        "argv",
        ["session_cost.py", str(transcript), "--post", "--says", str(says)],
    )
    assert module.main() == 1
    assert _posted(seen) == [] and _opened(seen) == []
    assert "no reading" in capsys.readouterr().out


def test_an_empty_reading_is_refused_before_the_log_is_looked_up(
    monkeypatch, tmp_path, transcript
):
    """The refusal is about what the session supplied, so it does not depend
    on the tracker answering. Checked at the seam rather than by reading the
    message: nothing reaches `gh` at all."""
    module = _cost()
    says = tmp_path / "empty.md"
    says.write_text("\n\n", encoding="utf-8")
    seen = _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    monkeypatch.setattr(
        module.sys,
        "argv",
        ["session_cost.py", str(transcript), "--post", "--says", str(says)],
    )
    assert module.main() == 1
    assert seen == [], seen


def test_main_without_post_still_prints_the_report(monkeypatch, capsys, transcript):
    """The refactor that made `--post` possible must leave the printing path
    exactly where it was: every reading this script takes now runs through
    `emit`."""
    module = _cost()
    monkeypatch.setattr(module.sys, "argv", ["session_cost.py", str(transcript)])
    assert module.main() == 0
    assert "command" in capsys.readouterr().out


def test_no_state_ever_opens_an_issue(monkeypatch):
    """The property, over every state rather than in the one case about it.
    A command that opened a log would break the invariant from the other
    side, which is the failure the skill names."""
    module = _cost()
    for listing in (
        "[]",
        _listing((1, "CLOSED")),
        _listing((1, "OPEN")),
        _listing((1, "OPEN"), (2, "OPEN")),
    ):
        seen = _gh(monkeypatch, module, listing=listing)
        module.post("r", "s", "flow-measurement")
        assert _opened(seen) == [], listing
