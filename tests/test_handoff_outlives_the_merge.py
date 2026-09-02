"""The round records live beside the work item, and outlive the merge.

Two things went wrong with the old home, and only one of them was known.

**The key was unusable.** The records sat at `.specseal/handoff/PR-<id>/`,
named after a pull request. A review round runs BEFORE the pull request opens,
so the key did not exist at the moment the record had to be written, and
conformance rule 1 — *reads before reviewing* — named a directory no correct
session could have created. A branch can therefore run its rounds, produce
findings, and leave no committed trace of what was open.

**Deletion was already reversed, and that half stays.** Deleting the directory
before the merge bought one thing worth keeping — a deadline that forced the
draining — and cost more: rows left for durable homes because the directory
was about to disappear, and those homes sit outside what the next reviewer
reads, so a finding deferred in round 1 came back in round 2.

Three halves are load-bearing here:

  the home       records live in the work item's directory, which exists from
                 its first commit, and every document that describes them says
                 the same thing
  the lifetime   they are closed at the merge, not deleted
  the deadline   deletion is gone, so the merge-time reminder replaces it

**The home gained one level.** Records sit at `<work item>/rounds/`, because
`round-N` is the only member of the SDD set that is plural and unbounded --
six records beside six other files is the shape it grows into. No reader looks
at the flat location any more, and nothing migrates a repository that updates
the plugin. What that trade costs is a work item whose review
silently stops counting, so it is bought back with a message: a record left
flat is named, along with the directory it must move to. If that message ever
degrades to a generic "no round record", the trade stops being sound, which is
why the tests below assert the two substrings rather than that something was
printed.
"""

import os
import re

from conftest import declare_routing, load_hook_module, rounds_dir, run_hook

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def payload(command, repo, session="s1"):
    return {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": command},
        "cwd": str(repo),
    }


# --- the home ---------------------------------------------------------------


def test_the_protocol_puts_the_records_with_the_work_item():
    protocol = read("docs", "review-handoff-protocol.md")
    assert "directory that holds the work item" in protocol, (
        "the protocol has to name the home abstractly — a project adopting it "
        "does not have this repository's `seal/specs/` layout"
    )
    assert "not the protocol" in protocol, (
        "without this the protocol has quietly acquired a path dependency"
    )
    assert "Draft 0.4" in protocol, "a changed layout or rule moves the draft"


def test_the_protocol_says_what_the_move_to_rounds_costs():
    """The trade is only sound while the message that replaces the fallback
    carries both halves. The protocol has to require that of a conforming
    tool, or the next implementation ships the generic sentence."""
    protocol = read("docs", "review-handoff-protocol.md")
    assert "rounds/" in protocol
    assert "No fallback ships" in protocol
    assert "must carry both" in protocol, (
        "without this a conforming tool may report a stray as a review that "
        "never happened, which is what makes the missing fallback unbearable"
    )


def test_this_repository_keeps_no_record_at_the_old_location():
    """S9. The migration, pinned so it cannot be undone one file at a time.

    Nothing migrates a repository automatically, this one included, and a
    record written flat by a later session would be read by nothing at all.

    A lower bound on the nested count used to sit under the assert below. It
    was there because "the old location is empty" is satisfied by DELETING
    the records just as well as by moving them, and the bound made the
    difference visible. That number was a fact about one migration rather
    than a rule, and this tree starts at 0.0.1 carrying no records at all, so
    it would fail on a truth. Put a bound back when there are rounds worth
    protecting — a count nobody can reach is not a guard, and neither is one
    that is trivially true.
    """
    specs = os.path.join(ROOT, "seal", "specs")
    flat = []
    for n in sorted(os.listdir(specs)):
        d = os.path.join(specs, n)
        if not os.path.isdir(d):
            continue
        flat += [f"{n}/{f}" for f in sorted(os.listdir(d)) if f.startswith("round-")]
    assert not flat, f"round records still at the work item's top level: {flat}"


def test_the_protocol_says_why_the_pull_request_was_the_wrong_key():
    """The reason is the half that stops someone keying it back."""
    protocol = read("docs", "review-handoff-protocol.md")
    assert "does not exist yet" in protocol
    assert "never been created" in protocol


def test_the_pull_request_survives_as_a_field():
    """Which change the work went to still has to be recorded."""
    protocol = read("docs", "review-handoff-protocol.md")
    assert "| PR |" in protocol
    assert "A field, not the key" in protocol


def test_the_documents_that_instruct_never_name_the_old_directory():
    """Eight documents describe these records. A path that changes in one of
    them and not the others is how two answers ship at once.

    These six tell a session where to write. The old path may not appear in
    them at all — not even hedged, because a reader following instructions
    stops at the first path they see.
    """
    for parts in (
        ("seal", "README.md"),
        ("templates", "seal-README.md"),
        ("templates", "sdd-round.md"),
        ("skills", "implement", "SKILL.md"),
        ("agents", "warden.md"),
        ("README.md",),
        ("README.ko.md",),
    ):
        assert ".specseal/handoff" not in read(*parts), "/".join(parts)


def test_the_instructing_documents_name_rounds_as_the_destination():
    """The same class as the check above, for the move this release made.

    That one looks for `.specseal/handoff` and nothing else, so every document
    telling a session to write `round-N.md` beside the work item passed it.
    Review round 1 found three: the round template's own header comment, the
    reminder the hook prints at the moment a record is written, and the
    migration command in the changelog. A session that follows any of them
    produces the stray this release fails the pull request for.

    Checked as "names the new path", not "does not name the old one": the old
    spelling is a suffix of the new one, so an absence test cannot tell them
    apart.
    """
    # `chain_check.py` is deliberately absent: it QUOTES the old failure text
    # (`holds no round-N.md`) to explain what a repository that moved nothing
    # would have seen, which is the same reason the two specifications keep the
    # old path in the check below. What it PRINTS is covered by
    # `test_every_migration_command_creates_its_destination`.
    for parts in (
        ("templates", "sdd-round.md"),
        ("hooks", "review-history-guard.py"),
    ):
        text = read(*parts)
        assert "rounds" in text, "/".join(parts)
        # Every mention of the record's own name carries the directory in
        # front of it. Spelled as a regex rather than a string replace,
        # because two of these three build the path from `routing.ROUNDS_DIR`
        # in an f-string and never hold the literal.
        # `round-N.md` and the template's `round-<N>.md` both. The first
        # version of this check missed the angle-bracket spelling, so the
        # mutation that sent the template back to the flat path walked
        # straight through it.
        # `round-N.md`, the template's `round-<N>.md`, AND a real number:
        # round 2 pointed the hook at `round-1.md` and the check let it
        # through, because only the placeholder spellings were looked for.
        for hit in re.finditer(r"round-(?:<?N>?|\d+)\.md", text):
            before = text[max(0, hit.start() - 40) : hit.start()]
            assert "rounds" in before or "ROUNDS_DIR" in before, (
                "/".join(parts)
                + f" names round-N.md with no directory: ...{before[-40:]!r}"
            )


def test_every_migration_command_creates_its_destination():
    """`git mv a b/` fails when `b` does not exist, and this release ships
    that command in three places as the entire migration path.

    Executed in round 1: `fatal: destination directory does not exist`. The
    command a person is told to run has to run, and dropping the trailing
    slash — what someone tries next — renames a single record to a FILE named
    `rounds`, which both readers then report as no review at all.
    """
    for parts in (
        ("CHANGELOG.md",),
        ("hooks", "review-history-guard.py"),
        ("skills", "code-review", "scripts", "chain_check.py"),
    ):
        text = read(*parts)
        # COMMANDS, not lines. Round 4 walked past the line rule three ways:
        # two `git mv` on one line (the first decides), the command split
        # across a wrapped line, and a prescription hidden behind an ellipsis
        # on a line whose warning word sat elsewhere. Window -> span -> line
        # were all proximity wearing a different unit.
        #
        # A command is a backticked span or a fenced-block line. One with an
        # argument after `git mv` prescribes; one without names the command in
        # a sentence about it, and an elided one warns about the broken form —
        # and the warning has to be inside the span, not near it.
        commands = re.findall(r"`([^`\n]*git mv[^`\n]*)`", text)
        fence = False
        for line in text.splitlines():
            if line.strip().startswith("```"):
                fence = not fence
                continue
            if fence and "git mv" in line:
                commands.append(line.strip())

        for cmd in commands:
            after = cmd.split("git mv", 1)[1]
            if not after.strip():
                continue  # the command's NAME
            if "\u2026" in after:
                # An ellipsis is not a path, so the span cannot be copied and
                # run at all — it illustrates, it does not prescribe. Checked
                # by what the text IS rather than by what sits near it: the
                # first version looked for the warning word inside the span
                # and it lives outside the backticks, and looking outside is
                # the proximity rule this whole check has been walking away
                # from for three rounds.
                continue
            assert "mkdir" in cmd, (
                "/".join(parts) + f": a `git mv` that creates nothing: {cmd}"
            )


def test_the_documents_that_explain_say_the_old_directory_is_gone():
    """The two specifications keep it, because the reason it moved is the
    half that stops someone moving it back. They have to mark it as past."""
    for parts in (
        ("docs", "review-handoff-protocol.md"),
        ("docs", "review-chain-spec.md"),
    ):
        text = read(*parts)
        assert ".specseal/handoff" in text, "/".join(parts)
        assert "never" in text, f"{'/'.join(parts)} names it without saying it is gone"


def test_the_hook_reads_the_new_home():
    guard = read("hooks", "review-history-guard.py")
    assert "routing.item_dir" in guard
    assert "handoff" not in guard.split('"""', 2)[2], (
        "the code below the docstring still builds the old path"
    )


# --- the Pass field ---------------------------------------------------------


def test_a_round_record_carries_its_own_verdict():
    """ "Was it reviewed" and "did it pass" were the same question, and only
    the first was answerable from the tree."""
    protocol = read("docs", "review-handoff-protocol.md")
    assert "| Pass |" in protocol
    assert "- [ ] Pass" in protocol
    assert "last round's checkbox" in protocol, (
        "without this a reader has to open every round file to get one answer"
    )
    assert "cannot read" in protocol, (
        "a tolerant read of the verdict table reports no open findings, which "
        "is indistinguishable from all of them closed"
    )


def test_the_template_ships_the_checkbox_unchecked():
    tpl = read("templates", "sdd-round.md")
    assert "- [ ] Pass" in tpl
    assert "- [x] Pass" not in tpl, "a template must not ship a claim"
    assert "| Target SHA |" in tpl and "| PR |" in tpl and "| Broad gate |" in tpl


def test_the_deferred_field_is_required_on_a_round_record():
    """The one-line carrier. Without it a deferral lives only in follow-up.md,
    which no round opens."""
    protocol = read("docs", "review-handoff-protocol.md")
    assert "| Deferred |" in protocol
    assert 'yes (may be "none")' in protocol, (
        "an optional field is one that goes unwritten in the rounds that needed it"
    )


# --- the lifetime -----------------------------------------------------------


def test_the_protocol_keeps_the_records_and_says_what_deletion_cost():
    protocol = read("docs", "review-handoff-protocol.md")
    assert "outlives the merge" in protocol
    assert "closed, not deleted" in protocol
    assert "inheritance range" in protocol, (
        "the protocol lost the reason deletion was dropped, which is the half "
        "that stops someone reinstating it"
    )


def test_the_third_conformance_rule_closes_rather_than_deletes():
    protocol = read("docs", "review-handoff-protocol.md")
    assert "**Closes before merging**" in protocol
    assert "nothing to drain" in protocol
    assert "before the directory is deleted" not in protocol


def test_no_document_still_says_the_records_are_deleted():
    for parts in (
        ("docs", "review-handoff-protocol.md"),
        ("seal", "README.md"),
        ("templates", "seal-README.md"),
        ("skills", "implement", "SKILL.md"),
    ):
        text = read(*parts)
        for stale in (
            "deleted in a cleanup commit",
            "deleted before merge",
            "deleted per-change before merge",
            "is deleted, so drain it first",
        ):
            assert stale not in text, f"{'/'.join(parts)} still says: {stale}"


def test_the_reviewer_does_not_re_raise_a_deferral():
    warden = read("agents", "warden.md")
    assert "Deferred** field is neither of those columns" in warden
    assert "already deferred" in warden


# --- a record left at the old location --------------------------------------


def test_a_stray_record_is_named_along_with_where_it_must_go(repo):
    """S3. Two substrings, not one, and not merely that something printed.

    The design refused a permanent dual read, and the price of that refusal is
    a repository whose review silently stops counting when it updates the
    plugin. The message is what buys it back, so it has to carry both halves:
    which file is in the wrong place, and where it goes. Degraded to a generic
    "no round record" it names neither, and the trade stops being sound.
    """
    (repo / "seal").mkdir(exist_ok=True)
    item = declare_routing(repo)
    (item / "round-1.md").write_text("| Target SHA | abc |\n")
    out = run_hook(
        "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
    )
    # `os.path.join`, not a literal `/`. The message spells its paths the way
    # the platform does — a person has to recognise their own repository in it
    # and then type the `mkdir` — and a test that hardcodes the separator
    # passes on posix and fails on windows for a reason that is the test's,
    # not the code's. CI's windows leg found this pair; the code had the same
    # defect one line over, printing `specs\item/rounds` in one command.
    assert os.path.join(item.parent.name, item.name, "round-1.md") in out, out
    assert os.path.join(item.name, "rounds") + os.sep in out, out
    # And the command it prescribes has to run. `git mv` does not create its
    # destination, so a message giving it alone sends a person to `fatal:
    # destination directory does not exist` — and the slash-less retry that
    # follows renames the record to a FILE. Asserted on the RENDERED text
    # because a source-level check is defeated by degrading the command to
    # its own name, which is what round 2 did to the first version.
    assert "mkdir" in out and "git mv" in out, out


def test_the_post_reminder_sends_the_session_to_rounds(repo):
    """The one message a session acts on at the moment it writes the record.

    Asserted on the RENDERED text. The source-level check does this too, by
    requiring `rounds` within forty characters before the record's name — and
    round 2 walked through it, because the sentence directly above happens to
    mention `ROUNDS_DIR` for an unrelated reason. Proximity is not the
    property; what the session is told to write is.
    """
    (repo / "seal").mkdir(exist_ok=True)
    declare_routing(repo)
    out = run_hook(
        "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
    )
    assert "holds no round record" in out, out
    where = load_hook_module("routing.py", "routing_post").ROUNDS_DIR
    assert os.path.join(where, "round-N.md") in out, (
        "the session is told to write the record somewhere nothing reads it: " + out
    )


def test_a_stray_record_does_not_also_report_as_missing(repo):
    """One state, one message. "holds no round record" beside "your record is
    in the wrong place" teaches a reader to skim past both."""
    (repo / "seal").mkdir(exist_ok=True)
    item = declare_routing(repo)
    (item / "round-1.md").write_text("| Target SHA | abc |\n")
    out = run_hook(
        "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
    )
    assert "holds no round record" not in out, out


def test_a_migrated_work_item_is_not_told_to_migrate(repo):
    """The state every repository lands in after the move. A message here
    would fire forever, on every work item, which is how a reminder becomes
    something people click through."""
    (repo / "seal").mkdir(exist_ok=True)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text("| Target SHA | abc |\n")
    out = run_hook(
        "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
    )
    assert out.strip() == "", out


# --- the deadline that replaced deletion ------------------------------------


def test_a_merge_with_unclosed_records_is_reminded(repo):
    (repo / "seal").mkdir(exist_ok=True)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text("| Target SHA | abc123 |\n")
    out = run_hook("review-history-guard.py", payload("gh pr merge 7 --squash", repo))
    assert "no closing note" in out, out


def test_closed_records_are_not_reminded(repo):
    (repo / "seal").mkdir(exist_ok=True)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text("| Deferred | nothing to drain |\n")
    out = run_hook("review-history-guard.py", payload("gh pr merge 7 --squash", repo))
    assert out.strip() == "", out


def test_a_merge_in_a_repo_that_never_opted_in_says_nothing(repo):
    """A globally installed plugin must not nag unrelated repositories."""
    declare_routing(repo)
    out = run_hook("review-history-guard.py", payload("gh pr merge 7 --squash", repo))
    assert out.strip() == "", out


def test_a_merge_with_no_round_record_at_all_says_nothing(repo):
    """Most changes never open a review round. Reminding there would teach
    people to click through the reminder that matters."""
    (repo / "seal").mkdir(exist_ok=True)
    declare_routing(repo)
    out = run_hook("review-history-guard.py", payload("gh pr merge 7 --squash", repo))
    assert out.strip() == "", out


# --- where the records live ------------------------------------------------

routing = load_hook_module("routing.py", "routing_rounds")


def item(tmp_path, name="1788138405-a-work-item"):
    d = tmp_path / "seal" / "specs" / name
    d.mkdir(parents=True)
    (d / "routing.md").write_text("| Branch | x |\n", encoding="utf-8")
    return d


def test_a_record_under_rounds_is_found(tmp_path):
    """S1. The whole point of the move, and the first thing that breaks if
    `ROUNDS_DIR` and the readers ever disagree."""
    d = item(tmp_path)
    (d / "rounds").mkdir()
    (d / "rounds" / "round-1.md").write_text("x", encoding="utf-8")
    assert routing.rounds(str(d)) == [str(d / "rounds" / "round-1.md")]


def test_ten_records_order_numerically_under_rounds(tmp_path):
    """S2. `round-10.md` sorts before `round-2.md` as text, and the reader
    that takes the LAST record is the one whose verdict speaks. The rule lives
    in `round_number`; this pins that the new path still goes through it."""
    d = item(tmp_path)
    (d / "rounds").mkdir()
    for n in range(1, 11):
        (d / "rounds" / f"round-{n}.md").write_text("x", encoding="utf-8")
    assert os.path.basename(routing.rounds(str(d))[-1]) == "round-10.md"


def test_the_rest_of_the_set_is_not_read_as_a_record(tmp_path):
    """`routing.md` and the SDD files sit beside `rounds/`, and one of them
    reaching the sort is how `sorted` raises on None against an int."""
    d = item(tmp_path)
    (d / "rounds").mkdir()
    for name in ("spec.md", "plan.md", "overview.md", "notes.md"):
        (d / "rounds" / name).write_text("x", encoding="utf-8")
    (d / "rounds" / "round-2.md").write_text("x", encoding="utf-8")
    assert [os.path.basename(p) for p in routing.rounds(str(d))] == ["round-2.md"]


def test_a_work_item_with_no_records_anywhere_reads_as_empty(tmp_path):
    """S4. 28 of this repository's 35 work items are in this state. Both
    readers have to answer "nothing here" rather than raising on a `rounds/`
    that does not exist."""
    d = item(tmp_path)
    assert routing.rounds(str(d)) == []
    assert routing.stray_rounds(str(d)) == []


def test_a_flat_record_is_not_read_as_a_record(tmp_path):
    """S3, the half about reading. The file is left where it is and the
    reader does not count it -- a dual read would put two places to look in
    the module four gates import."""
    d = item(tmp_path)
    (d / "round-1.md").write_text("x", encoding="utf-8")
    assert routing.rounds(str(d)) == []


def test_a_flat_record_is_reported_as_a_stray(tmp_path):
    """S3, the half about saying so. Silence here is indistinguishable from a
    work item that never ran a review."""
    d = item(tmp_path)
    (d / "round-2.md").write_text("x", encoding="utf-8")
    (d / "round-1.md").write_text("x", encoding="utf-8")
    assert routing.stray_rounds(str(d)) == [
        str(d / "round-1.md"),
        str(d / "round-2.md"),
    ]


def test_a_record_under_rounds_is_not_a_stray(tmp_path):
    """The migrated state must be quiet, or every repository that moved its
    records gets told to move them again."""
    d = item(tmp_path)
    (d / "rounds").mkdir()
    (d / "rounds" / "round-1.md").write_text("x", encoding="utf-8")
    assert routing.stray_rounds(str(d)) == []


def test_a_merge_on_an_undeclared_branch_says_nothing(repo):
    """The cost of one key instead of two, pinned so it is not a surprise.

    What replaced the deadline is the pull-request check in CI, which reads
    the same declaration from the diff.
    """
    (repo / "seal").mkdir(exist_ok=True)
    out = run_hook("review-history-guard.py", payload("gh pr merge 7 --squash", repo))
    assert out.strip() == "", out
