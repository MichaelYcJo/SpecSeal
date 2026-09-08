"""commit-review-gate, review-history-guard, session-lease — via real stdin."""

import ast
import importlib.util
import inspect
import json
import os
import subprocess
import textwrap

import pytest
from conftest import (
    decision_of,
    declare_routing,
    fired,
    load_hook_module,
    rounds_dir,
    run_hook,
)

# The gate's own name for the directory it records the question in. Read
# from the module rather than written again, so a rename moves both.
CHOICE_DIR = load_hook_module("commit-review-gate.py", "gate_choice_dir").CHOICE_DIR


def payload(cmd, repo, session="s1", tool="Bash", **extra):
    p = {
        "tool_name": tool,
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }
    p.update(extra)
    return p


def opt_in(repo):
    (repo / "seal").mkdir(exist_ok=True)


def git_dir(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


# --- commit-review-gate ----------------------------------------------------


def test_gate_silent_without_opt_in(repo):
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "silent"
    )


def test_gate_denies_so_the_user_is_offered_both_ways_on(repo):
    """Declining an `ask` is a bare "No": the user who wanted the other way on
    has to retype the command. A deny gives the model the turn back."""
    opt_in(repo)
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "deny"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "AskUserQuestion" in reason
    assert "[no-review]" in reason and "review chain" in reason.lower()


def test_the_next_attempt_gets_the_plain_prompt(repo):
    """Denying every time would trap a session whose answer the gate cannot
    read off the command. The fallback is the prompt this gate always had."""
    opt_in(repo)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "deny"
    )
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "ask"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "Approving is the waiver" in reason


def test_a_different_session_is_asked_the_question_too(repo):
    opt_in(repo)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "deny"
    )
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload("git commit -m x", repo, session="s2")
            )
        )
        == "deny"
    )


def test_an_unwritable_marker_counts_as_already_asked(repo):
    """The rule the chain spec states: a marker that cannot be recorded means
    the question is treated as asked. Inverted, the deny repeats forever in
    exactly the environments that cannot write, and the commit never lands."""
    opt_in(repo)
    # Unwritable on BOTH platforms. `os.chmod(gd, 0o500)` is a no-op for a
    # directory on Windows -- the mode bits are accepted and the write still
    # succeeds -- so the gate recorded the question, answered `silent`, and
    # the rule this case states went unheld on the one platform where an
    # unwritable git-dir is most likely.
    #
    # Occupying the marker directory's own name with a file raises `OSError`
    # everywhere: `makedirs(..., exist_ok=True)` re-raises when the name it
    # finds is not a directory.
    gd = git_dir(repo)
    with open(os.path.join(gd, CHOICE_DIR), "w", encoding="utf-8") as f:
        f.write("not a directory")
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "ask"
    )


def test_a_session_id_with_separators_stays_inside_the_git_dir(repo):
    """The id names a file. Measured on the sibling guard: `../../escaped`
    put an empty file at the repository root."""
    opt_in(repo)
    run_hook(
        "commit-review-gate.py",
        payload("git commit -m x", repo, session="../../escaped"),
    )
    assert not (repo / "escaped").exists()
    assert os.path.isfile(
        os.path.join(git_dir(repo), "specseal-commit-choice", "escaped")
    )


def test_without_a_session_id_it_asks_instead_of_denying(repo):
    """No id means nowhere to record that the question was asked, and a deny
    would then repeat forever. `ask` cannot loop: approving is the way out."""
    opt_in(repo)
    p = payload("git commit -m x", repo)
    del p["session_id"]
    assert decision_of(run_hook("commit-review-gate.py", p)) == "ask"


def test_gate_allows_when_cycle_reviewed(repo):
    opt_in(repo)
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    with open(os.path.join(git_dir(repo), "specseal-reviewed"), "w") as f:
        f.write(head)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "silent"
    )


def test_gate_ignores_non_commit_and_bypass_tag(repo):
    opt_in(repo)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git log", repo)))
        == "silent"
    )
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload("git commit -m x [no-review]", repo)
            )
        )
        == "silent"
    )


def test_the_marker_inside_a_message_is_prose_not_a_waiver(repo):
    """`-m "drop [no-review] from the docs"` describes work; it does not waive.

    A substring test cannot tell a waiver from a sentence about one, and the
    message body is where people write sentences."""
    opt_in(repo)
    assert fired(
        run_hook(
            "commit-review-gate.py", payload('git commit -m "x [no-review]"', repo)
        )
    )


# --- review-history-guard --------------------------------------------------


def test_history_guard_reminds_posting_without_record(repo):
    opt_in(repo)
    item = declare_routing(repo)
    out = run_hook(
        "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
    )
    assert item.name in out, out


def test_the_posting_reminder_spells_all_three_paths_from_one_base(repo):
    """A reminder is read to be TYPED, so its paths must share a base.

    Round 2 of #96: the fix that put the two todo files at the work item's
    level spelled them from the repository root and left `round-N.md`
    spelled from the work item, so a session typing the three paths it was
    handed got two right and one in the wrong place. The case above asserts
    only that the work item's name appears, which every one of the four
    spellings satisfies.
    """
    opt_in(repo)
    item = declare_routing(repo)
    out = run_hook(
        "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
    )
    # `*name.split("/")` rather than the literal: `os.path.join` with a `/`
    # inside one argument writes `…\rounds/round-N.md` on Windows against the
    # hook's `…\rounds\round-N.md`, which is the dialect mixing
    # `review-history-guard.py:152-158` records CI's windows leg catching once
    # already — reproduced here with `ntpath` before this line was written.
    for name in ("rounds/round-N.md", "tests-todo.md", "evidence-todo.md"):
        expected = os.path.join("seal", "specs", item.name, *name.split("/"))
        assert expected in out, (
            f"the reminder does not name {expected}; a path spelled from "
            f"another base is one a session types from where it is standing "
            f"and gets wrong. Message was:\n{out}"
        )


def test_history_guard_silent_when_record_exists_on_post(repo):
    opt_in(repo)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text("| Target SHA | abc |\n")
    assert (
        run_hook(
            "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
        ).strip()
        == ""
    )


def test_history_guard_says_nothing_where_no_work_item_is_declared(repo):
    """The work item is the key now. Without a declaration there is no
    directory to name, and a reminder that names nothing is noise."""
    opt_in(repo)
    assert (
        run_hook(
            "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
        ).strip()
        == ""
    )


def test_history_guard_reminds_reading_with_record(repo):
    opt_in(repo)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text("| Target SHA | abc |\n")
    out = run_hook(
        "review-history-guard.py", payload("gh pr view 42 --json comments", repo)
    )
    assert "tests-todo" in out


def test_history_guard_silent_without_opt_in(repo):
    assert (
        run_hook(
            "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
        ).strip()
        == ""
    )


def test_an_unbalanced_quote_in_a_piped_gh_command_does_not_stop_the_session():
    """`gh_segments`' `except ValueError`, which nothing watched.

    `SEG_RE` splits on `|`, so a pipe inside a quoted string leaves a segment
    whose quoting is unbalanced and `shlex.split` raises `ValueError` on it.
    The command that does it is an ordinary one — the READ branch's own
    example piped into `jq`. Without the arm the exception leaves
    `gh_segments`, passes `main()` unguarded (whose own `try` covers
    `json.load` alone) and stops the session's Bash call, which is the one
    thing R5's own argument says must never happen.

    Round 1's 🟡 1, and the same class as T1 and T3 one function over: the
    arm was found by walking `gh_segments` for `ExceptHandler`, `If` and
    `While` nodes rather than by reading it. Deleting it left this module at
    30 passed and all seven modules that reference the hook at 270 passed,
    exit 0 — the silence that looks exactly like correctness."""
    guard = load_hook_module("review-history-guard.py", "guard_unbalanced_quote")
    assert guard.gh_segments("gh pr view 1 --json comments | jq '.c[] | .b'") == [
        "gh pr view 1 --json comments"
    ]
    assert guard.gh_segments("gh pr merge 1 --squash | tee it's-done.log") == [
        "gh pr merge 1 --squash"
    ]


# --- session-lease ---------------------------------------------------------


def leases_of(repo):
    d = os.path.join(git_dir(repo), "specseal-leases")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def test_bash_leases_cwd_repo(repo):
    run_hook("session-lease.py", payload("ls", repo, session="sess-a"))
    assert leases_of(repo) == ["sess-a"]


def test_write_leases_edited_files_repo_not_cwd(repo, tmp_path):
    p = {
        "tool_name": "Write",
        "session_id": "sess-b",
        "tool_input": {"file_path": str(repo / "f.txt")},
        "cwd": str(tmp_path),
    }
    run_hook("session-lease.py", p)
    assert "sess-b" in leases_of(repo)


def test_lease_outside_any_repo_is_silent(tmp_path):
    p = {
        "tool_name": "Bash",
        "session_id": "sess-c",
        "tool_input": {"command": "ls"},
        "cwd": str(tmp_path),
    }
    assert run_hook("session-lease.py", p).strip() == ""


def test_stale_leases_are_pruned(repo):
    import time

    run_hook("session-lease.py", payload("ls", repo, session="sess-old"))
    stale = os.path.join(git_dir(repo), "specseal-leases", "sess-old")
    os.utime(stale, (time.time() - 100000,) * 2)
    run_hook("session-lease.py", payload("ls", repo, session="sess-new"))
    assert leases_of(repo) == ["sess-new"]


def test_a_pasted_fix_does_not_read_as_a_closing_note(repo):
    """Round 1's 🟡 8. The merge branch stays quiet once some record says the
    rows were drained, and it decided that by matching `nothing to drain`,
    `drained` or `closed` against the record's RAW text.

    `## Paste-ready fixes` puts the reviewer's code into every record, and
    `closed` is a word this repository's own fixes carry — the record of the
    round that found this carries `close(` five times. One pasted
    `def close(args):` and the pre-merge reminder goes silent for a record
    whose Deferred rows are still live, which is the moment the reminder
    exists for: after the merge nobody is looking.

    A probes fence could already do this, so the defect predates the section;
    what the section changes is that it is now every record rather than one
    with a probes fence."""
    opt_in(repo)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text(
        "| Target SHA | abc |\n\n"
        "## Paste-ready fixes\n\n"
        "```python\ndef close(args):\n    # the fence reads as closed\n    return 0\n```\n\n"
        "## Deferred\n\n"
        "| Finding | Where it went | Who answers it |\n|---|---|---|\n"
        "| the windows leg | nowhere yet | nobody |\n",
        encoding="utf-8",
    )
    out = run_hook("review-history-guard.py", payload("gh pr merge 42", repo))
    assert out.strip(), (
        "a closing word inside a pasted fix silenced the pre-merge reminder "
        f"for a record with a live Deferred row. Message was:\n{out!r}"
    )


def test_a_real_closing_note_still_silences_the_merge_reminder(repo):
    """The other side of 🟡 8, so the fix cannot be *never close anything*.

    `nothing to drain` stands in the Deferred section as prose, which the
    reader keeps — it blanks fenced blocks and comment bodies and nothing
    else. A record that says the rows were drained still says so.

    **Green on the base as well, and deliberately so.** The base stayed
    silent here too; what this pins is that the repair did not buy its
    silence by making the guard never close anything. It is seen red by
    mutation — dropping the drain phrase from `CLOSED_RE`."""
    opt_in(repo)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text(
        "| Target SHA | abc |\n\n"
        "## Paste-ready fixes\n\n"
        "```python\ndef close(args):\n    return 0\n```\n\n"
        "## Deferred\n\n"
        "| Finding | Where it went | Who answers it |\n|---|---|---|\n\n"
        "nothing to drain\n",
        encoding="utf-8",
    )
    out = run_hook("review-history-guard.py", payload("gh pr merge 42", repo))
    assert out.strip() == "", out


@pytest.mark.parametrize(
    "missing",
    [
        "a path that does not exist",
        "a file with no Python loader",
        "a reader that does not parse",
        "a reader whose own import is missing",
    ],
)
def test_the_guard_falls_back_to_the_raw_text_without_the_reader(tmp_path, missing):
    """§13, and the reason `reader()` returns None instead of raising.

    The reader is reached by a relative path from `hooks/` into `skills/`,
    and a copy of the plugin without that directory has to leave the hook
    printing a possibly-wrong reminder rather than stopping a session's Bash
    call. The guarantee is REMOVED here — the constant is pointed away from
    the real reader — because a defence nobody has run without its platform
    is not verified.

    **One parameter per arm `reader()` has, and each takes a different
    input.** The four:

      `except OSError`      an absent path, which raises `FileNotFoundError`
      `spec is None`        a file Python has no loader for, where
                            `spec_from_file_location` returns None and never
                            raises at all
      `except SyntaxError`  a `.py` reader that exists and does not parse —
                            a truncated copy of the plugin, or one whose
                            syntax the running Python is older than (#209)
      `except ImportError`  a `.py` reader that parses and imports something
                            this interpreter does not have, which is the
                            same truncated copy one line further in

    The last two were unwatched: deleting `SyntaxError` from the except
    tuple, and deleting `ImportError`, each left the whole module green.
    Without its arm the same input raises out of `reader()`, through
    `is_closed`, into the hook's `main()` — the one thing this case's own
    argument says must never happen.

    **`spec.loader is None` is the fifth arm and gets no parameter**, because
    no file path constructs it. The durable reason is one line of CPython
    rather than the sweep: `spec_from_file_location` assigns `spec.loader`
    inside its supported-suffix loop and returns None from that loop's
    `else`, so a truthy spec with a falsy loader is unreachable for ANY
    location string — not merely for the ones anybody tried. It is defence
    in depth, and saying so is the honest close rather than a case that
    cannot be written.

    The sweep is corroboration and is stated as such, because a sample can
    only ever say *not these* (round 1's ⬜ 5, and #205 is a ticket about a
    stated limit standing in for a case). Executed here over 21 inputs:
    `spec_from_file_location` returns None outright for a directory, a
    `.txt`, an extensionless file and an empty string, and returns a spec
    with a real loader for a `.py`, a `.pyc`, a `.so`, a missing `.py` and a
    DIRECTORY named `x.py`; none of the 21 makes `spec` truthy while its
    loader is falsy. **The suffix list is per-platform** — on the machine
    that ran it, `.cpython-314-darwin.so`, `.abi3.so`, `.so`, `.py`, `.pyc`
    — so the sweep settles one interpreter and one operating system, and
    contract §13 is the section about resting a defence on a platform.

    Measured — with one parameter, deleting the `spec is None` arm left the
    module green, which is round 2's 🟡 1 one unit over."""
    guard = load_hook_module("review-history-guard.py", "guard_without_a_reader")
    if missing == "a path that does not exist":
        guard.READER = os.path.join(str(tmp_path), "no_such_reader.py")
    elif missing == "a file with no Python loader":
        other = tmp_path / "reader.txt"
        other.write_text("not python\n", encoding="utf-8")
        guard.READER = str(other)
    elif missing == "a reader that does not parse":
        broken = tmp_path / "truncated_reader.py"
        broken.write_text("def (\n", encoding="utf-8")
        guard.READER = str(broken)
    else:
        half = tmp_path / "half_a_reader.py"
        half.write_text("import specseal_no_such_module\n", encoding="utf-8")
        guard.READER = str(half)
    assert guard.reader() is None
    record = tmp_path / "round-1.md"
    record.write_text(
        "| Target SHA | abc |\n\n```python\n# closed\n```\n", encoding="utf-8"
    )
    # Without the reader the fenced word counts, which is the pre-fix
    # behaviour and the honest fallback: a reminder that may not fire beats a
    # hook that raises inside somebody's Bash call.
    assert guard.is_closed([str(record)]) is True
    assert guard.is_closed([str(tmp_path / "nothing.md")]) is True


def test_no_records_at_all_is_not_an_unclosed_directory(tmp_path):
    """`is_closed`'s fourth arm, which nothing watched.

    Found by enumerating the function's arms out of its own source rather
    than by reading it and listing what stood out — which is how #209 and
    #210 were both missed for a round. `if not records: return True` stayed
    green when mutated to `return False`, because `main()` only calls
    `is_closed` behind `if records` and no case called it with an empty
    list.

    Defence in depth, like `reader()`'s `spec.loader is None`. Unlike that
    one it is CONSTRUCTIBLE — the call is one line — so the honest close is
    a case rather than a sentence saying no input reaches it.

    The direction is what makes it worth a case. Mutated to `return False`,
    a work item whose `rounds/` directory holds no record reads as one whose
    rows were never drained, and the pre-merge reminder fires at every merge
    for the state most work items are in — the noise this hook's own
    docstring says must stay quiet."""
    guard = load_hook_module("review-history-guard.py", "guard_with_no_records")
    assert guard.is_closed([]) is True


def test_the_reader_is_what_makes_a_fenced_closing_word_not_count(tmp_path):
    """The same pair with the reader in place, asserted on `is_closed`
    itself so the rule is pinned where it lives rather than only through the
    reminder's text."""
    guard = load_hook_module("review-history-guard.py", "guard_with_its_reader")
    assert guard.reader() is not None
    fenced = tmp_path / "fenced.md"
    fenced.write_text(
        "| Target SHA | abc |\n\n```python\n# closed\n```\n", encoding="utf-8"
    )
    plain = tmp_path / "plain.md"
    plain.write_text("| Target SHA | abc |\n\nnothing to drain\n", encoding="utf-8")
    assert guard.is_closed([str(fenced)]) is False
    assert guard.is_closed([str(plain)]) is True


def reader_blanking_passes(reader):
    """The passes `readable` composes, read out of `readable`'s own source.

    Derived rather than typed, which is the whole of #210: this list used to
    be two literals with a comment saying *a third pass added to the reader
    later wants a third entry here*, and nothing made it want one. A third
    pass was added to `readable` and the module stayed at 27 passed — a
    closing word inside an inline code span then read as hidden, `is_closed`
    returned False, and no case said a word about it.

    `readable` is `blank_fences(strip_comments(text.splitlines()))`, so the
    passes are the calls it makes by NAME to functions its own module
    defines. `text.splitlines()` is an attribute call and drops out; a
    builtin like `list` would have no function on the reader module and
    drops out too. What survives is what a closing word can be hidden by.

    **Dropping attribute calls is the limit, and it is refused rather than
    left silent** (round 1's 🟡 2). A pass written as `_SPAN_RE.sub(...)`
    hides a closing word exactly as well as a named pass and is an
    `ast.Attribute` call, so this derivation cannot see it: executed, that
    pass leaves the module at 30 passed, exit 0 while `is_closed` on a
    record whose only closing word sits in an inline span flips True to
    False — which is #210 reproduced with the tie in place. It is also the
    shape #210 and round 3 both used as their example, because a text-level
    blanker is naturally written as a sub rather than as a line-based
    function. So an attribute call other than `splitlines` fails here
    instead of quietly narrowing what the tie compares."""
    src = textwrap.dedent(inspect.getsource(reader.readable))
    called = {
        node.func.id
        for node in ast.walk(ast.parse(src))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    attrs = {
        node.func.attr
        for node in ast.walk(ast.parse(src))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert attrs <= {"splitlines"}, (
        f"`readable` makes an attribute call this derivation cannot see: "
        f"{sorted(attrs - {'splitlines'})}. A pass written as `_SPAN_RE.sub(...)` "
        "rather than as a module function hides a closing word just as well and "
        "leaves the set below unchanged — which is #210 with the tie in place. "
        "Give the pass a name on the reader module, or teach this function to "
        "read the shape you used."
    )
    return {name for name in called if inspect.isfunction(getattr(reader, name, None))}


# One entry per pass `readable` makes, keyed by the pass's own name so the
# parametrization can be read back out of the reader (`seal/ledger.md` F1's
# standard, and the case below is where the tie is asserted). `blank_fences`
# is what a pasted fix needs; `strip_comments` is what a record's own
# narration needs, and it is the arm that moves real records.
HIDDEN_CLOSING_WORD = {
    "blank_fences": (
        "```python\ndef close(args):\n    # the fence reads as closed\n"
        "    return 0\n```"
    ),
    "strip_comments": (
        "<!-- The verifying round for round 1's fixes.\n"
        "     It closed all five and opened three. -->"
    ),
}


@pytest.mark.parametrize("hider", list(HIDDEN_CLOSING_WORD))
def test_a_closing_word_a_reader_blanks_is_not_a_closing_note(tmp_path, hider):
    """Round 2's 🟡 1, and the class rather than the instance.

    The fence arm is what a pasted fix needs. The comment arm is what a
    record's own narration needs, and it is the one doing the work in
    production: over this repository's 127 committed round records the
    reader flips three from closed to not-closed, and **all three** flip on
    the comment arm — the fence arm flips none of them. All three have live
    `Deferred` rows, so the reminder firing is right.

    Measured before this case existed: swapping `readable` for
    `blank_fences` left all 24 cases of this module green, while swapping it
    for `strip_comments` turned two red. The arm that does the work rested
    on nothing.

    *It closed all five* narrates what the round found. It is not a
    statement that the Deferred rows were drained, and the three records it
    silenced all still have theirs.

    **The tie is the first assertion, and it is what makes this a class
    rather than two literals** (#210, `seal/ledger.md` F1's standard). The
    parametrization is compared with the passes read out of `readable`'s own
    source, so a pass added to the reader fails this case instead of
    arriving unguarded and silent."""
    guard = load_hook_module("review-history-guard.py", f"guard_{hider}")
    reader = guard.reader()
    assert reader is not None, "the tie needs the real reader, not the fallback"
    assert reader_blanking_passes(reader) == set(HIDDEN_CLOSING_WORD), (
        "the passes `readable` composes and the keys below have parted. If a "
        "pass was ADDED, a closing word it hides reads as hidden, `is_closed` "
        "returns False, and without this assertion nothing goes red — the "
        "silence looks exactly like correctness; add it to HIDDEN_CLOSING_WORD, "
        "keyed by its name, with a record that hides its word the way that "
        "pass hides it. If a pass was RENAMED, re-key its entry rather than "
        "adding one: an extra key leaves this assertion red."
    )
    record = tmp_path / "round-1.md"
    record.write_text(
        f"# round 1\n\n{HIDDEN_CLOSING_WORD[hider]}\n\n"
        "| Target SHA | abc |\n\n"
        "## Deferred\n\n"
        "| Finding | Where it went | Who answers it |\n|---|---|---|\n"
        "| the windows leg | nowhere yet | nobody |\n",
        encoding="utf-8",
    )
    assert guard.is_closed([str(record)]) is False


def test_a_blanking_pass_written_as_a_sub_is_refused_rather_than_unseen(tmp_path):
    """The tie's own blind spot, watched (round 1's 🟡 2).

    `reader_blanking_passes` derives the passes from the calls `readable`
    makes to `ast.Name` targets, so a pass written as `_SPAN_RE.sub(...)` is
    an `ast.Attribute` call and never reaches the set the tie compares. The
    derivation therefore answered the same two names for a reader with three
    passes, the tie held, and a closing word inside an inline code span
    began reading as hidden — #210 with the tie in place.

    The refusal is what closes it, and this is the case that watches the
    refusal. Without the assertion in `reader_blanking_passes` the reader
    below derives `{'blank_fences'}`, nothing raises, and no case in this
    repository says a word — which is the same silence the tie itself exists
    to end, one function further out."""
    fake = tmp_path / "a_reader_that_blanks_with_a_sub.py"
    fake.write_text(
        "import re\n\n"
        '_SPAN_RE = re.compile(r"`[^`]*`")\n\n\n'
        "def blank_fences(lines):\n"
        "    return lines\n\n\n"
        "def readable(text):\n"
        '    return blank_fences(_SPAN_RE.sub("", text).splitlines())\n',
        encoding="utf-8",
    )
    spec = importlib.util.spec_from_file_location("specseal_fake_reader", fake)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(AssertionError, match="attribute call this derivation"):
        reader_blanking_passes(module)


def test_the_ties_message_answers_a_rename_as_well_as_an_addition():
    """Round 1's ⬜ 6 — the message prescribed the wrong repair for a rename.

    The tie goes red for two different causes and the repairs differ. A pass
    ADDED wants a new key; a pass RENAMED wants the existing key re-keyed,
    and adding one leaves three keys against two passes and the assertion
    still red. Executed: renaming `blank_fences` on the reader turns both
    parameters red, and adding a third key does not turn them green.

    The message said only *add the pass, keyed by its name*, so a renamer
    reading it does the one thing that cannot work. This case is why the
    next edit cannot quietly take the second half back."""
    src = inspect.getsource(test_a_closing_word_a_reader_blanks_is_not_a_closing_note)
    assert "RENAMED" in src and "re-key" in src, (
        "the tie's failure message no longer tells a renamer what to do. It "
        "goes red for an ADDED pass and for a RENAMED one, and adding a key "
        "repairs only the first — a renamer who follows that advice ends up "
        "with three keys against two passes and the case still red."
    )
