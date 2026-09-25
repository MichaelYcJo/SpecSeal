"""The suite reads a workflow's text one way (#482, #462).

No YAML parser is installed anywhere this suite runs, so every case that
reads `.github/workflows/*.yml` reads text, and each one that re-derived
what a comment is got it slightly differently. `tests/conftest.py` holds the
one reading: `code_line` and `code_lines` for the comment rule,
`workflow_step` for a step found by its name, and `step_running` for the one
step whose code names a script. The cases here drive them over fixtures,
because a reader nothing drives is a reader nobody can tell is partial.

The six sites that used to slice the workflow on a bare token, enumerated by
`grep` over the modules that read `hygiene.yml` on 2026-09-25, are:

  - `test_a_merge_cannot_silently_drop_a_correction.py`, its three A9 cases
  - `test_a_body_naming_two_issues_claims_one.py#
    test_the_body_reaches_the_script_through_the_environment`
  - `test_the_changelog_is_gathered_at_release.py#
    test_the_check_only_runs_for_a_release`
  - `test_the_ledger_fragments_fold_at_release.py#
    test_the_check_only_runs_for_a_release`

All six now read through these helpers. Nothing structural stops a seventh,
and `spec.md` §*Out, and why* says why.
"""

import pytest
from conftest import code_line, step_running, workflow_step, workflow_steps

# A comment naming the script above an unrelated step, the real step below
# it, a step with no name, a quoted name and a second job. Neutral values
# only (`CLAUDE.md`, no real identifiers).
WORKFLOW = """\
jobs:
  release:
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # the base is diffed

      # The step below runs correction_check.py, and this comment is not it.
      - name: an unrelated step
        run: echo unrelated

      - name: "the real step"
        shell: bash
        run: |
          if [ "${{ github.base_ref }}" = "main" ]; then
            echo "skipped"; exit 0
          fi

          python3 correction_check.py --range "x...HEAD"  # the range
  other:
    steps:
      - name: a step of another job
        run: echo other
"""


@pytest.mark.parametrize(
    "line, code",
    [
        ("# a whole-line comment", None),
        ("   # an indented one", None),
        ("run: x --range foo  # --baseline bar", "run: x --range foo"),
        ("fetch-depth: 0 # why", "fetch-depth: 0"),
        # A `#` is a comment only after a blank, and only outside quotes.
        ("url: a#b", "url: a#b"),
        ('run: echo "a # b"', 'run: echo "a # b"'),
        ("run: echo 'a # b'", "run: echo 'a # b'"),
        ('run: echo "a # b" # c', 'run: echo "a # b"'),
        # An escaped quote does not close a double-quoted string (round 1, ⬜ 7).
        ('run: echo "a \\" # b"', 'run: echo "a \\" # b"'),
        ('run: echo "a \\"" # b', 'run: echo "a \\""'),
        ("name: plain", "name: plain"),
    ],
)
def test_one_rule_says_what_a_comment_is(line, code):
    """The comment rule, one owner. A line whose first non-blank character is
    `#` is no code at all; a `#` after a blank and outside quotes ends the
    code there, where YAML ends a plain scalar and the shell stops reading."""
    assert code_line(line) == code, repr(code_line(line))


def test_a_comment_naming_a_script_cannot_move_the_step():
    """B4, #482. The comment above the unrelated step names
    `correction_check.py`, and the step that runs it is found anyway: only
    code lines are asked whether they name the script."""
    step = step_running(WORKFLOW, "correction_check.py")
    assert "the real step" in step, step
    assert "echo unrelated" not in step, step
    assert '--range "x...HEAD"' in step, step
    # The step's code keeps its blank line, and loses its trailing comment.
    assert "the range" not in step, step


def test_a_step_is_found_by_its_name_and_ends_at_the_next_one():
    """`workflow_step` reads the name the way `broad_gate.py#unquote` does,
    and the block stops at the next step of its list or at the next job."""
    step = workflow_step(WORKFLOW, "the real step")
    assert 'github.base_ref }}" = "main"' in step, step
    assert "exit 0" in step, step
    assert "a step of another job" not in step, step
    assert "echo other" not in step, step
    unrelated = workflow_step(WORKFLOW, "an unrelated step")
    assert [ln.strip() for ln in unrelated.splitlines() if ln.strip()] == [
        "- name: an unrelated step",
        "run: echo unrelated",
    ], unrelated


def test_every_step_of_every_job_is_read_and_a_nameless_one_has_none():
    names = [name for name, _ in workflow_steps(WORKFLOW)]
    assert names == [
        None,
        "an unrelated step",
        "the real step",
        "a step of another job",
    ], names


@pytest.mark.parametrize(
    "call",
    [
        lambda: workflow_step(WORKFLOW, "no such step"),
        lambda: step_running(WORKFLOW, "no_such_script.py"),
        # `echo` is in three steps' code: a region that is not one step.
        lambda: step_running(WORKFLOW, "echo"),
    ],
)
def test_a_reader_that_does_not_find_exactly_one_step_says_so(call):
    """A step layout the reader does not model fails loudly rather than
    reading the wrong region."""
    with pytest.raises(AssertionError):
        call()
