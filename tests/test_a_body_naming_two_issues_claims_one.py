"""`Closes #153 and #150` claims one issue, and nothing said so.

PR #162 wrote that sentence; the 0.8.0 release closed #153 and left #150 open.
Nothing malfunctioned -- a closing keyword claims the one number that follows
it, GitHub reads it that way, and `close_issues_on_release.py` says so in a
comment above its own regex. The answer was written down and nothing acted on
it.

`issue_claims_check.py` is what acts on it, and these are its cases. Two
things they are watching for, because both are ways the check quietly stops
being worth having:

**A false positive.** A warning on a body that is correct teaches people to
scroll past the check, which costs more than the defect. Most of the cases
below are bodies that must produce NOTHING -- a fenced quote of the failure
shape (this repository's own documents carry those), a separate paragraph, a
separate list item, a number before the keyword.

**A missed hard wrap.** Every body here is wrapped at 88 columns, so one
sentence spans lines routinely and the defect arrives split across two of
them. A segmenter that treats a line as a sentence passes every other case in
this file and misses the one it was written for.

The real #162 body is deliberately NOT a fixture. It carries a session URL on
a domain outside this repository's fixture allowlist, so committing it turns
`tests/test_no_real_identifiers.py` red — and the shape is what matters rather
than the numbers anyway. It was run live instead, and the output is in this
work item's `phases/phase-2.md`.
"""

import importlib.util
import os
import sys

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _load(name):
    path = os.path.join(ROOT, ".github", "scripts", name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


check = _load("issue_claims_check")


def read(body):
    return check.read(body)


def warned(body):
    """The `(claimed, unclaimed)` pairs the body earns a warning for."""
    return [(kept, lost) for kept, lost, _ in read(body)[2]]


# --- the measured shape ------------------------------------------------------


def test_the_sentence_that_lost_an_issue():
    """PR #162's shape, with neutral numbers. One claim, one loss, one line
    telling the author which is which."""
    claimed, mentioned, warnings = read("Closes #11 and #22 — both are done.")
    assert claimed == ["11"]
    assert mentioned == ["22"]
    assert [(k, lost) for k, lost, _ in warnings] == [("11", "22")]


def test_the_comma_spelling_is_the_same_defect():
    """`Closes #1, #2` is the form the sibling script's own comment names."""
    assert warned("Closes #11, #22") == [("11", "22")]


def test_the_warning_quotes_the_sentence_as_the_author_wrote_it():
    """Not the masked copy. A code span blanked out of the quote reads as a
    different sentence, and the author has to recognise their own."""
    body = "Closes #11 and #22 — see `close_issues_on_release.py` for why."
    ((_, _, sentence),) = read(body)[2]
    assert "`close_issues_on_release.py`" in sentence


def test_a_hard_wrapped_sentence_is_still_one_sentence():
    """The case that rules out "a line is a sentence". Every body in this
    repository is wrapped at 88 columns, so this is how the defect actually
    arrives -- measured on #162, whose `Closes` sentence runs across three
    lines."""
    assert warned("Closes #11 and\n#22 are both done.") == [("11", "22")]


def test_the_same_number_twice_in_one_sentence_is_one_warning():
    """One warning per unclaimed NUMBER, not per occurrence. The sentence is
    one thing to fix, and the same annotation printed twice reads as two."""
    assert warned("Closes #11 and #22, and #22 again.") == [("11", "22")]


def test_the_same_number_in_two_sentences_earns_a_warning_each():
    """The set is per segment. Two sentences that each lose the number are two
    places the author has to write the keyword."""
    assert warned("Closes #11 and #22. Closes #33 and #22.") == [
        ("11", "22"),
        ("33", "22"),
    ]


def test_a_numeric_url_fragment_beside_a_claim_is_a_warning():
    """A link ending `#22` reads as an issue number here, which is what the
    mention list already says. Beside a claim in the same sentence that is a
    warning rather than a mention -- excluding a `#N` preceded by a URL
    character would be a second syntax to be wrong about."""
    assert warned("Closes #11, and https://example.com/x#22 has the rest.") == [
        ("11", "22")
    ]


def test_the_nearest_claim_is_the_one_named():
    """With two keywords ahead of it, the number the author was reusing is the
    one beside it -- naming the first would send them to the wrong keyword."""
    assert warned("Closes #11 and closes #22 and #33") == [("22", "33")]


# --- what must produce nothing -----------------------------------------------


def test_a_fenced_quote_of_the_failure_shape_is_not_an_instance_of_it():
    """A body quoting `Closes #1, #2` as an EXAMPLE of the defect must not be
    reported as one. This repository's own documents do exactly that, and its
    bodies quote its documents routinely."""
    body = (
        "The defect looks like this:\n\n```\nCloses #11, #22\n```\n\nDo not write that."
    )
    assert read(body) == ([], [], [])


def test_an_inline_span_claims_nothing_and_mentions_nothing():
    assert read("see `Closes #11, #22` in the ticket") == ([], [], [])


def test_a_fence_does_not_splice_the_line_above_it_onto_the_line_below():
    """The masking is length-preserving for this reason. Collapsing a fenced
    block to one space would join `Closes #11` to `#22` across it, and invent
    the very warning the fence exists to prevent."""
    body = "Closes #11\n\n```\nsome code\n```\n\n#22 is a different matter."
    assert warned(body) == []


def test_a_second_keyword_loses_nothing():
    claimed, mentioned, warnings = read("Closes #11 and closes #22")
    assert claimed == ["11", "22"]
    assert mentioned == []
    assert warnings == []


def test_a_number_the_body_claims_elsewhere_is_never_warned_about():
    """It is claimed, so nothing is lost, wherever else it also appears."""
    assert warned("Closes #11 and #22 is the other one. This closes #22.") == []


def test_a_new_sentence_is_a_new_segment():
    assert warned("Closes #11. See #22 for the background.") == []


def test_a_blank_line_ends_the_segment():
    assert warned("Closes #11\n\n#22 is unrelated.") == []


def test_a_list_item_ends_the_segment_without_a_blank_line():
    """Consecutive list items carry no blank line between them, so the block
    rule is the only thing separating them."""
    assert warned("- Closes #11\n- #22 is next\n") == []


def test_a_table_row_ends_the_segment():
    assert warned("| Closes #11 |\n| #22 |\n") == []


@pytest.mark.parametrize("rule", ["---", "***", "___", "==="])
def test_a_horizontal_rule_ends_the_segment(rule):
    """A thematic break and a setext underline are blocks of their own, and
    the space every other marker requires takes all four out of the class. A
    claim above one and an unrelated number below it are not one sentence, and
    warning about them is the false positive this check spends everything to
    avoid."""
    assert warned(f"Closes #11\n{rule}\n#22 is unrelated.") == []


@pytest.mark.parametrize(
    "prose",
    [
        # A run of markers that OPENS the line and then carries prose. These
        # are what the whole-line anchor is for, and nothing else here needs
        # it: every other shape below is rejected at the first character, so a
        # case built only from those leaves the anchor unpinned. Measured --
        # dropping `$` from one alternative left all forty-two green.
        "--- not a rule",
        "*** not a rule",
        "___ not a rule",
        "=== not an underline",
        "= x",
        # And the shapes the space requirement rejects, which the four
        # alternatives must not take back.
        "a --- b",
        "--",
        "-x",
        "#22",
        "*bold* x",
    ],
)
def test_a_run_of_markers_inside_a_line_is_still_prose(prose):
    """The four break alternatives match a WHOLE line only. Widened to match
    anywhere, they would take `#22` at the start of a line back out of the
    segment it belongs to -- which is the defect this module exists to see,
    hard-wrapped."""
    assert check.BLOCK_START.match(prose) is None


def test_a_number_before_the_keyword_is_not_the_shape():
    """`Part of #11, and this closes #22` is not somebody losing a claim. Only
    a number AFTER the claim is a candidate, and that is where the whole
    false-positive budget goes."""
    claimed, mentioned, warnings = read("Part of #11, and this closes #22.")
    assert claimed == ["22"]
    assert mentioned == ["11"]
    assert warnings == []


def test_a_version_number_is_not_a_sentence_boundary():
    """`0.9.2` would split the sentence if a full stop alone ended one, and the
    warning would be lost."""
    assert warned("Closes #11 in 0.9.2 and #22 with it.") == [("11", "22")]


def test_a_trailing_full_stop_after_a_number_still_closes_the_segment():
    assert warned("Closes #11. #22 is separate.") == []


def test_an_anchor_is_not_an_issue_number():
    """`#L45` and `#heading` need a digit immediately after the hash."""
    assert read("Closes #11, see file.py#L45 and the #overview section") == (
        ["11"],
        [],
        [],
    )


def test_a_body_with_no_numbers_says_so():
    assert read("A tidy-up with no ticket behind it.") == ([], [], [])


def test_the_document_that_teaches_the_rule_carries_no_instance_of_it():
    """`docs/issues-and-milestones.md` says a body quoting the failing shape
    inside a fence or a code span is not an instance of it. This repository's
    bodies quote its documents routinely, so the section has to hold to that
    everywhere -- a narrative past-tense keyword is still a keyword, and
    `KEYWORDS` carries the past tense of all three verbs."""
    with open(
        os.path.join(ROOT, "docs", "issues-and-milestones.md"), encoding="utf-8"
    ) as f:
        _, _, warnings = read(f.read())
    assert warnings == [], warnings[0][2] if warnings else ""


# --- what a person reads -----------------------------------------------------


def test_the_warning_is_written_as_a_job_annotation():
    """`::warning::` at the start of the line is what makes GitHub render this
    on the job rather than bury it in the log. Dropping the prefix while
    tidying the f-string leaves every other case green."""
    lines = []
    check.report(*read("Closes #11 and #22"), out=lines.append)
    annotations = [line for line in lines if line.startswith("::warning::")]
    assert len(annotations) == 1, lines
    assert "#11" in annotations[0] and "#22" in annotations[0]


def test_the_two_lists_say_what_closes_and_what_does_not():
    """The author acts on these two lines. A rename that leaves `read()` alone
    changes what they are told and no case notices."""
    lines = []
    check.report(*read("Closes #11 and #22"), out=lines.append)
    assert lines[0] == "claimed (closed when the release reaches `main`): #11"
    assert lines[1] == "mentioned only (nothing closes these): #22"


def test_a_clean_body_says_so_rather_than_saying_nothing():
    """Silence reads as a check that did not run."""
    lines = []
    check.report(*read("Closes #11"), out=lines.append)
    assert lines[-1] == "no sentence claims one number and names another beside it"


# --- the process contract ----------------------------------------------------


def test_a_body_is_never_a_failure(tmp_path, capsys):
    """It reports; it never fails a pull request. A check that goes red on
    prose stops a release for a false positive."""
    for body in ("Closes #11 and #22", "", "no numbers here"):
        f = tmp_path / "body.md"
        f.write_text(body, encoding="utf-8")
        assert check.main(["--body-file", str(f)], env={}) == 0
    capsys.readouterr()


def test_an_empty_body_is_a_body():
    """A pull request opened with no description is ordinary, and reporting
    nothing for it is the answer -- not an exit code."""
    assert check.body_from(_args(None), {"PR_BODY": ""}) == ""


def test_a_step_that_examined_nothing_is_not_green(capsys):
    """No `--body-file` and no `PR_BODY` at all is a misconfigured workflow.
    The alternative is a step that is green having read nothing, which is the
    failure `templates/hygiene.yml`'s own header argues against."""
    assert check.main([], env={}) == 2
    assert "examined nothing" in capsys.readouterr().err


def test_the_environment_is_read_when_no_file_is_given():
    assert check.body_from(_args(None), {"PR_BODY": "Closes #11"}) == "Closes #11"


class _args:
    def __init__(self, body_file):
        self.body_file = body_file


# --- one definition of what GitHub reads -------------------------------------


def test_the_check_imports_the_closers_definition_rather_than_restating_it():
    """Two lists of what a closing keyword is would drift apart the first time
    either was widened, and widening one of them is precisely the repair this
    issue rejected. Identity, not equality: a copied literal passes an
    equality check on the day it is copied.

    The sibling is taken from `sys.modules`, where the check's own import put
    it — NOT loaded again by path. A second load builds a second module
    object, and then `KEYWORDS is KEYWORDS` is false for a module that
    imported it correctly. `CLOSING` would still pass, because `re.compile`
    caches by pattern and flags and hands both loads the same object: the two
    regex identities are true whether the import happened or not, and only the
    tuple actually asks the question. Measured here, in this file's first
    run."""
    closer = sys.modules["close_issues_on_release"]
    assert os.path.samefile(
        closer.__file__,
        os.path.join(ROOT, ".github", "scripts", "close_issues_on_release.py"),
    ), "the check imported some other module of that name"
    assert check.CLOSING is closer.CLOSING
    assert check.KEYWORDS is closer.KEYWORDS
    assert check.FENCE is closer.FENCE
    assert check.SPAN is closer.SPAN


def test_the_source_defines_no_keyword_list_of_its_own():
    """The identity case above passes for a module that ALSO carries its own
    copy and never uses it. This reads the file."""
    with open(
        os.path.join(ROOT, ".github", "scripts", "issue_claims_check.py"),
        encoding="utf-8",
    ) as f:
        source = f.read()
    body = source.split('"""', 2)[2]
    for spelling in ("KEYWORDS = (", "CLOSING = re.compile", "FENCE = re.compile"):
        assert spelling not in body, (
            f"{spelling!r} is defined here as well as next door — one of the "
            "two will be widened alone"
        )


# --- the wiring --------------------------------------------------------------


def test_the_workflow_runs_the_check_on_every_pull_request():
    """A check nothing calls is the standing waiver this repository refuses to
    build. It goes in the job that already runs on every pull request, so it
    needs no trigger and no token of its own."""
    with open(
        os.path.join(ROOT, ".github", "workflows", "hygiene.yml"), encoding="utf-8"
    ) as f:
        workflow = f.read()
    assert "issue_claims_check.py" in workflow
    assert os.path.isfile(
        os.path.join(ROOT, ".github", "scripts", "issue_claims_check.py")
    )


def test_the_body_reaches_the_script_through_the_environment():
    """A pull request body is attacker-controlled text and `${{ }}` inside a
    `run:` block is textual substitution into a shell script. Interpolating a
    body there hands whoever opens the pull request the runner."""
    with open(
        os.path.join(ROOT, ".github", "workflows", "hygiene.yml"), encoding="utf-8"
    ) as f:
        workflow = f.read()
    step = workflow.split("issue_claims_check.py")[0].rsplit("- name:", 1)[1]
    assert "PR_BODY: ${{ github.event.pull_request.body }}" in step
    assert "${{ github.event.pull_request.body }}" not in workflow.split("run:")[-1], (
        "the body is interpolated into a shell line"
    )


@pytest.mark.parametrize("stays_home", ["issue_claims_check"])
def test_the_check_does_not_travel_to_user_repositories(stays_home):
    """`.github/scripts/` is this repository's own automation, the way
    `gather_changelog` and `fold_ledger` are — `test_first_setup_asks_once.py`
    pins those two the same way. Shipping this one means first deciding it
    belongs under `skills/`, which is a wider change than this issue asks
    for."""
    with open(os.path.join(ROOT, "templates", "hygiene.yml"), encoding="utf-8") as f:
        assert stays_home not in f.read()
