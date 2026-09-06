"""A fix's surface — what it changed and what it created — is a row, not a diff.

Issue #57 traced ten regressions on one work item to the fixes that opened
them. The largest class, four of ten, was a fix that changed a unit's
contract — signature, return arity, return type, or set of returnable
values — while not every place that contract reaches was revisited. The diff
names the changed signature and `grep` names the reach, and a person reading
the diff missed all four. The second class a machine can hold is the units a
fix CREATES: one fix commit created eight new units and four carried defects,
while the verifying round's own rule (*answers, not new findings*) told it to
skip exactly those.

So `round-N.md` carries two more rows, and `chain_check.py` refuses a new
record without them:

  Contract changes   every changed unit with the call sites it reaches,
                     `unit → site, site`, units separated by `;`. A unit
                     listed without its reach is refused — the reach is the
                     half a diff does not show
  New units          the top-level definitions and constants the fixes
                     added — the verifying round's finding surface

Both accept `none`, with or without a reason. Records of work items begun
before `SURFACE_FROM` print rather than fail — the grandfathering shape
`Fixes checked by` already uses, keyed to the same directory-name second.

The prose cases at the bottom are prose assertions, worth exactly what their
substrings are chosen to be; each picks the sentence a rewrite would have to
destroy.
"""

import ast
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
# The generator, for the words it can put in a reach half. Two cases read
# them out of the module rather than typing them, and each catches one thing
# the other cannot: the named form alone reads `only the first is a unit
# name`, and the derived form alone sees a value ADDED to `call_sites`. A
# rename and a reword redden both (#177, round 1's finding 1).
RECORD = os.path.join(ROOT, "skills", "code-review", "scripts", "round_record.py")

# A work item begun before `chain_check.SURFACE_FROM`: missing rows print.
OLD_ITEM = "seal/specs/1787700000-a-work-item"
# One begun after it: missing rows fail. The two differ only in the second
# their names start with, which is the whole of what the grandfathering reads.
NEW_ITEM = "seal/specs/1799000000-a-later-work-item"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
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
    d = tmp_path_factory.mktemp("fix-surface-template") / "repo"
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


def record(sha, contract="none", new_units="none"):
    """A record that passes every check but the two rows each case is about.

    The verdict closes without a fix and `Fixes checked by` says so, so
    `Pass` beside `nobody` never fires and a failure can only have come from
    the fix-surface rows. `contract=None` / `new_units=None` leave the row
    out entirely, which is the state the grandfathering decides.
    """
    rows = ""
    if contract is not None:
        rows += f"| Contract changes | {contract} |\n"
    if new_units is not None:
        rows += f"| New units | {new_units} |\n"
    # The floor row is `no` for the same reason the verdict closes without a
    # fix: `NEW_ITEM` began after `chain_check.FLOOR_FROM`, so leaving it out
    # would fail every record here for a rule this file does not pin.
    # `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` is where
    # that one is pinned.
    rows += "| Loses a record or crashes | no |\n| Needs a fix | no |\n"
    # `Ran by` is here for the reason the floor row above is: `NEW_ITEM`
    # began after `chain_check.RUNNER_FROM`, so leaving it out would fail
    # every record in this file for a rule it does not pin.
    # `tests/test_a_record_says_what_ran_it.py` is where that one is pinned.
    rows += "| Ran by | specseal:warden on a model |\n"
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n"
        f"| Fixes checked by | no fixes to check |\n{rows}\n"
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


def declared(repo, item, body):
    write(repo, f"{item}/routing.md", declaration(item))
    sha = commit(repo, "declare")
    write(repo, f"{item}/rounds/round-1.md", body(sha))
    commit(repo, "round 1")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_module():
    """`chain_check.py` itself, for `SURFACE_FROM` — typed here, the boundary
    case would pin a number instead of the boundary."""
    return _load("specseal_surface_check_for_tests", CHECK)


def reader_module():
    """`unverified_check.py`, the same reader `chain_check` loads — a second
    implementation of `strip_comments` here would be free to drift."""
    return _load(
        "specseal_surface_reader_for_tests",
        os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py"),
    )


# --- the rows are required, after the cutoff --------------------------------


def test_a_record_without_the_contract_row_fails(repo):
    """The largest measured regression class, refused as a missing row."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, contract=None))
    code, out = run(repo)
    assert code == 1, out
    assert "Contract changes" in out
    assert "reach" in out, (
        "the failure has to say what the row is FOR — the diff names the "
        "signature, and the reach is the half it does not show"
    )


def test_a_record_without_the_new_units_row_fails(repo):
    declared(repo, NEW_ITEM, lambda sha: record(sha, new_units=None))
    code, out = run(repo)
    assert code == 1, out
    assert "New units" in out
    assert "finding surface" in out, (
        "without the reason, the row reads as a schema change nobody "
        "explained — what it buys is the verifying round's surface"
    )


def test_records_predating_the_rule_print_rather_than_fail(repo):
    """The grandfathering, which is what keeps the eight merged records of
    `1788229400-…` — and every other pre-rule record — green."""
    declared(repo, OLD_ITEM, lambda sha: record(sha, contract=None, new_units=None))
    code, out = run(repo)
    assert code == 0, out
    assert "Contract changes" in out and "New units" in out, (
        "passing in silence would hide the state the rows exist to surface"
    )


def test_a_work_item_begun_at_the_cutoff_second_is_held_to_the_rule(repo):
    """`>=`, and the item on the boundary is the one that wrote the rule —
    read from the module so a moved cutoff moves this case with it."""
    began = check_module().SURFACE_FROM
    declared(
        repo,
        f"seal/specs/{began}-the-item-that-wrote-the-rule",
        lambda sha: record(sha, contract=None),
    )
    code, out = run(repo)
    assert code == 1, out


def test_a_work_item_with_no_timestamp_prefix_is_grandfathered(repo):
    """No date to compare — failing would fail a naming convention."""
    declared(
        repo,
        "seal/specs/a-work-item-with-no-date",
        lambda sha: record(sha, contract=None, new_units=None),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_draft_pull_request_is_not_excused_the_rows(repo):
    """The `Pass` excuse does not reach here, exactly as it does not reach
    `Fixes checked by`: the honest mid-run value is `none — <why>`, so a
    missing row is missing at every stage."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, contract=None))
    code, out = run(repo, draft=True)
    assert code == 1, out
    assert "Contract changes" in out


# --- what the cells may say -------------------------------------------------


def test_none_is_an_answer_in_both_rows(repo):
    declared(repo, NEW_ITEM, lambda sha: record(sha))
    code, out = run(repo)
    assert code == 0, out


def test_none_with_a_reason_is_still_none(repo):
    """`none — the fixes changed no signature` is the honest spelling a
    session writes, and the one every other vocabulary here allows a tail
    on. Backticks are how every document shows the value."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(
            sha,
            contract="`none` — the fixes changed no signature",
            new_units="none, nothing added",
        ),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_unit_with_its_reach_passes(repo):
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(
            sha,
            contract="`read()` gained a `None` return → `check_ledger`, "
            "`reverify`; `place()` grew a guard → its own three branches",
            # Each entry carries the depth it was added at, which
            # `chain_check.DEPTH_FROM` requires of an item begun this late.
            new_units="`SURFACE_FROM` (depth 1); `fix_surface` (depth 1)",
        ),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_unit_without_its_reach_fails(repo):
    """The refusal the row exists for: the diff already names the changed
    signature, so a row restating it without the call sites adds nothing."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, contract="`read()` gained a `None` return"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "call site" in out


def test_one_entry_without_reach_fails_among_good_ones(repo):
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, contract="`a()` → `b`; `c()` widened its set"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "`c()` widened its set" in out, "the failure has to name the entry"


def test_an_ascii_arrow_is_the_arrow(repo):
    """`->` is what somebody types when `→` is not on the keyboard."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, contract="`a()` -> `b`, `d`"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_an_entry_carrying_a_literal_separator_is_refused(repo):
    """Round 2's 🔴 1, as a fixture, pinning the choice whichever way a later
    change goes.

    `;` splits the cell before anything looks at code spans, so an entry that
    describes the character in a code span is cut in half and the tail is
    refused for having no reach. That is what happened to the record naming
    this branch's own fix surface, and CI runs the same command on every pull
    request, so the branch would have opened red. The workaround is to spell
    the character as a word; closing it would mean parsing code spans, which
    is the enumeration the arrow's limit already declines.

    It lives here rather than in `test_chain_check_at_the_pull_request.py`,
    which the round named: every other `Contract changes` refusal is in this
    file, and that file's work item predates `SURFACE_FROM`, so the same cell
    would print there instead of failing.
    """
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, contract="`says_none` accepts a trailing `;`"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "call site" in out, (
        "the tail after the separator is what is refused, and the failure "
        "has to name the reach it is missing"
    )


def test_an_empty_cell_is_not_an_answer(repo):
    """A row that says nothing answers nothing, on any record — unlike the
    absent row, an empty one is always the author's to fill."""
    declared(repo, OLD_ITEM, lambda sha: record(sha, contract=""))
    code, out = run(repo)
    assert code == 1, out
    assert "empty" in out


def test_a_cell_of_only_separators_is_not_an_answer(repo):
    """Round 1's 🟡 1, on this work item's own diff: `;` split into empty
    entries, every one was skipped, and both rows passed — not `none`, not
    empty. The empty-cell refusal's own sentence already covers it: a row
    that says nothing answers nothing."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, contract=";", new_units="—"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "Contract changes" in out and "New units" in out, (
        "both rows have to be refused — the guard sits before the "
        "contract-only entry walk"
    )


# Round 1's 🟡 3, closed as a RECORDED LIMIT rather than a parser. The arrow
# is found by substring, so an ASCII `->` inside a backticked unit name reads
# as the reach separator — and parsing code spans to close that would be the
# enumeration over an unbounded domain the diff's own rule 6 refuses. The
# sentence is pinned (rule 8 applied to itself) and the behavior is executed,
# so whoever closes the limit meets both and deletes them consciously.
RECORDED_LIMIT = (
    "an ASCII `->` inside a backticked unit name reads as the reach separator"
)


def test_the_recorded_limit_an_ascii_arrow_inside_a_name(repo):
    """The limit, executed: `` `operator->` `` alone passes, because the
    substring arrow splits the name itself. If this case ever fails, the
    limit was closed — delete the sentence the case below pins."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, contract="`operator->` widened its set"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_the_arrow_limit_is_recorded_where_the_rule_lives():
    """A recorded limit that is recorded nowhere is a closed finding — the
    exact shape rule 6 refuses. `→` is named as the spelling that avoids
    the limit, in the check and in the document that carries its refusals."""
    for parts in (
        ("docs", "review-chain-spec.md"),
        ("skills", "code-review", "scripts", "chain_check.py"),
    ):
        text = flat(*parts)
        assert RECORDED_LIMIT in text, "/".join(parts)


def test_the_section_names_the_words_the_writer_can_put_in_a_reach():
    """Round 2's ⬜ 11 of #156. The section defined the reach as `unit → call
    sites` and named none of the values `call_sites` actually writes, so a
    round opened a finding against `hide_from_git → build, ensure, pytest` on
    the grounds that nothing is called `pytest`. It was the generator's own
    output, re-derived at the record's SHA. A reach word the document does not
    carry is a correct cell somebody will spend a round on."""
    spec = flat("docs", "review-chain-spec.md")
    generator = _load("specseal_round_record_for_reach_words", RECORD)
    for word in (generator.PYTEST, generator.PYTEST_ONLY, generator.NO_SITE):
        assert f"`{word}`" in spec, f"the section does not name `{word}`"
    assert "only the first is a unit name" in spec, (
        "the section names the words without saying which of them is a unit"
    )


# The derived case's refusal, named so its wording can be pinned (contract
# §14). It used to read `the section does not name X` and nothing else, so the
# only act it suggested was editing a shipped document -- even where X was a
# comparison operand `call_sites` can never hand back. It names both
# directions now, because `handed_back`'s call arm still over-reaches by one
# documented step and the reader is the one who can tell which case they are
# in.
REACH_REFUSAL = (
    "the derived reach set carries it and the section does not name it. "
    "Add it to the section if `call_sites` really can hand it back; if it "
    "cannot, `handed_back` over-reached and the fix is here, not in the "
    "document"
)


# Enumerated twice over, never listed. One entry per ARM of `handed_back` --
# the arms are its own branch set, so the enumeration is by construction and
# an arm added without a fixture here is visible as an arm a mutation
# survives. Then one entry per over-collection shape round 1's finding 2
# actually measured, which is the second closed set: a comparison operand, an
# f-string, a keyword argument and a dict key each used to arrive as a reach
# value. Choosing fixtures by listing is the very failure this row closes one
# level up, so neither half is a list somebody thought of.
DERIVATIONS = (
    # the arms
    ('WORD = "a word"\n\ndef call_sites():\n    return [WORD]\n', {"a word"}),
    ('def call_sites():\n    return ["a literal"]\n', {"a literal"}),
    (
        'WORD = "a word"\n\ndef call_sites():\n    return (WORD, "in a tuple")\n',
        {"a word", "in a tuple"},
    ),
    ('def call_sites():\n    return {"in a set"}\n', {"in a set"}),
    (
        'WORD = "a word"\n\ndef call_sites():\n'
        '    if here:\n        return ["a literal"]\n'
        '    return [WORD, "and another"]\n',
        {"a word", "a literal", "and another"},
    ),
    (
        'WORD = "a word"\n\ndef call_sites():\n    return [WORD] + ["concatenated"]\n',
        {"a word", "concatenated"},
    ),
    ('WORD = "a word"\n\ndef call_sites():\n    return elsewhere(WORD)\n', {"a word"}),
    ('WORD = "a word"\n\ndef call_sites():\n    return elsewhere()\n', set()),
    ("COUNT = 3\n\ndef call_sites():\n    return [COUNT]\n", set()),
    ("def call_sites():\n    return [3, None]\n", set()),
    # the over-collection shapes finding 2 measured
    (
        'P = "pytest"\n\ndef call_sites():\n    return [P] if kind == "test" else named\n',
        {"pytest"},
    ),
    ('def call_sites():\n    return [f"{n} only"]\n', set()),
    ('def call_sites():\n    return build(sep=", ")\n', set()),
    ('def call_sites():\n    return {"a key": 1}\n', set()),
)


@pytest.mark.parametrize("source, want", DERIVATIONS)
def test_the_derivation_reads_both_shapes_a_return_can_fix(source, want):
    """`reach_values` against fixtures rather than against the generator,
    because the generator reaches four of `handed_back`'s arms and no more.
    Today every return in `call_sites` names a constant and none writes a
    literal, returns a tuple, or concatenates — so those arms are unreachable
    from the real module and a mutation deleting one survives. The case above
    stays green either way, and that is what these are for.

    The two non-string fixtures are a value that must NOT arrive: a reach
    half is a word somebody reads in a record, and dropping either type check
    turns a count or a `None` into one. The name arm and the literal arm each
    need their own, because a name never reaches the literal arm.

    `elsewhere(WORD)` and `elsewhere()` are the recorded OVER- and UNDER-reach
    executed: a constant handed to a call is read, and a value only that call
    knows is not. Whoever closes either limit will find one of them red.

    The last four are round 1's finding 2, each measured over-collecting
    before the repair — `test` out of a comparison, ` only` out of an
    f-string, `, ` out of a keyword argument, `a key` out of a dict. None can
    reach a record, and each one used to make the case above red while
    telling the reader to add it to a shipped document."""
    assert reach_values(source) == want


def test_the_refusal_names_the_other_direction_too():
    """Contract §14, on a message a maintainer acts on. Round 1's finding 2:
    the refusal read `the section does not name X` and nothing else, so the
    only act it suggested was editing a shipped document — even where X was a
    comparison operand `call_sites` can never hand back. It names both
    directions now, and this holds that it does.

    The pin has a limit worth stating where it is: it holds the wording and
    the fact that the derived case cites the constant, not that the string a
    reader sees is this one. A different message inlined beside the constant
    leaves this green, and only a reader catches that."""
    for half in ("Add it to the section", "over-reached and the fix is here"):
        assert half in REACH_REFUSAL, half
    body = read("tests", "test_the_fixes_name_their_surface.py")
    wanted = "test_the_section_names_every_reach_value_the_generator_fixes"
    found = [
        node
        for node in ast.walk(ast.parse(body))
        if isinstance(node, ast.FunctionDef) and node.name == wanted
    ]
    assert len(found) == 1, f"{wanted}: {len(found)} definitions, expected 1"
    assert "REACH_REFUSAL" in ast.get_source_segment(body, found[0]), (
        "the derived case does not use the refusal this pins, so the wording "
        "a maintainer reads is somewhere else"
    )


def test_a_second_call_sites_is_refused_rather_than_picked_from():
    """The derivation reads one function, so two of that name is an ambiguity
    it must not resolve silently — picking the first would derive a set from
    a definition nobody meant and report it as the generator's."""
    two = "def call_sites():\n    return []\n\n\ndef call_sites():\n    return []\n"
    with pytest.raises(AssertionError, match="2 definitions"):
        reach_values(two)


def handed_back(node, constants):
    """The strings this expression can hand to `call_sites`' caller.

    One arm per way an expression carries a value outward, and nothing else
    reaches anything: a `Constant` is its own string, a `Name` is the
    module-level constant it names, a sequence is the union of its elements,
    a conditional is both branches, a concatenation is both sides, and a call
    is its positional arguments. An f-string, a keyword argument, a dict, a
    comparison operand and an attribute are none of those, so they arrive as
    nothing — which is the whole repair, because each of them used to arrive
    as a reach value.

    The arms are the enumeration this function is derived from, and
    `DERIVATIONS` carries one fixture per arm for that reason. An arm with no
    fixture is an arm a mutation survives, which is the defect this whole row
    exists against, one level down.
    """
    if isinstance(node, ast.Constant):
        return {node.value} if isinstance(node.value, str) else set()
    if isinstance(node, ast.Name):
        return {constants[node.id]} if node.id in constants else set()
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return set().union(*(handed_back(part, constants) for part in node.elts))
    if isinstance(node, ast.IfExp):
        return handed_back(node.body, constants) | handed_back(node.orelse, constants)
    if isinstance(node, ast.BinOp):
        return handed_back(node.left, constants) | handed_back(node.right, constants)
    if isinstance(node, ast.Call):
        return set().union(*(handed_back(arg, constants) for arg in node.args))
    return set()


def reach_values(source=None):
    """Every reach value fixed in `call_sites`' own source, derived from it.

    Two shapes are read out of the function's `return` statements: a
    module-level string constant HANDED BACK by one, and a string literal
    handed back by one. So a value added to the function joins this set
    without anybody editing this file, which is the whole difference between
    this and listing the words beside the case.

    **Handed back, never merely present.** This walked the whole `Return`
    subtree for one round, and every string anywhere inside it became a reach
    value — a comparison operand in `return [P] if kind == "test" else named`
    arrived as `test`, a keyword argument in `return build(sep=", ")` as
    `, `, an f-string's literal half as ` only`, a dict key as itself. None of
    those can reach a record, and the refusal below then told a maintainer to
    put one into a shipped document. `handed_back` asks the question the row
    is about instead of the question the parser makes easy.

    `source` is the generator's text, and the default reads the real module.
    The cases hand it fixtures for one reason: today's generator names a
    constant in every return and writes no literal into one, so the literal
    arm cannot be reached — and an arm no case can kill is an arm that
    proves nothing, whatever the suite total says.

    **What the derivation UNDER-reaches, recorded rather than closed.** Five
    shapes hand a value back and are read as nothing, each measured:

    - a bare local — `w = "a word"` then `return [w]`;
    - a constant reached through an attribute — `return [chain.PYTEST]`,
      which is what a constant moved to another module looks like;
    - a constant declared with an annotation — `W: str = "a word"`, an
      `ast.AnnAssign` that the module-level scan below does not read;
    - a value handed back by `yield` rather than by `return`;
    - a value another function alone knows — `return elsewhere()`.

    The floor in the case below catches all five only when the whole
    vocabulary moves at once. Closing any of them means following a value
    across a statement or across a call, which is the enumeration over an
    unbounded domain `RECORDED_LIMIT` above declines for the same reason.

    **What it OVER-reaches, in one place and on purpose.** A `Call`'s
    positional arguments count as handed back, so `return elsewhere(WORD)`
    yields `WORD`'s value even though `elsewhere` may return something else
    entirely. That is the conservative direction for this row — a word that
    might reach a record is worth a red case — and it is the one remaining
    way the refusal below can name a value the function cannot actually hand
    back, which is why the refusal says so rather than only naming the word.

    **The two values the section names as CATEGORIES** rather than as words,
    the enclosing top-level unit and the file's basename, are deliberately
    outside all of this: those are the reviewed repository's names and not
    the generator's, so there is no finite set to derive.
    """
    if source is None:
        source = read("skills", "code-review", "scripts", "round_record.py")
    tree = ast.parse(source)
    constants = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Constant):
            continue
        if not isinstance(node.value.value, str):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                constants[target.id] = node.value.value
    found = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "call_sites"
    ]
    assert len(found) == 1, f"call_sites: {len(found)} definitions, expected 1"
    values = set()
    for node in ast.walk(found[0]):
        if isinstance(node, ast.Return) and node.value is not None:
            values |= handed_back(node.value, constants)
    return values


def test_the_section_names_every_reach_value_the_generator_fixes():
    """#177. The case above reads three constants BY NAME, so it goes red on
    a rename and on a reword and stays green when a SIXTH value is added
    beside them — and an addition is the drift the paragraph exists against:
    the document would go stale and the suite would say nothing. This one
    derives the set from `call_sites` instead, so a value the function gains
    has to reach the document before the suite is green again.

    Both are kept because neither covers the other, and the split is measured
    rather than argued. A value ADDED to `call_sites` is invisible to the
    named case and reddens this one; the sentence `only the first is a unit
    name` is read by the named case alone, so dropping it from the section
    reddens that one and leaves this one green. A rename and a reword kill
    BOTH, because the floor below reads the same three constants by attribute
    name — round 1's finding 1, which is what this paragraph used to get
    wrong, and getting it wrong here is what would have licensed deleting the
    named case. `reach_values`' docstring carries what neither reaches."""
    spec = flat("docs", "review-chain-spec.md")
    generator = _load("specseal_round_record_for_derived_reach", RECORD)
    values = reach_values()
    floor = {generator.PYTEST, generator.PYTEST_ONLY, generator.NO_SITE}
    assert floor <= values, (
        f"the derivation missed {sorted(floor - values)}, so it has stopped "
        "reading the function and the loop below proves nothing"
    )
    for word in sorted(values):
        assert f"`{word}`" in spec, f"`{word}`: {REACH_REFUSAL}"


def test_a_row_inside_a_comment_is_not_the_row(repo):
    """One reader, not two: the template explains the rows in a comment
    beside them, and an explanation must not read as an answer."""
    body = record("0" * 40, contract=None).replace(
        "- [x] Pass",
        "<!--\n| Contract changes | none |\n-->\n\n- [x] Pass",
    )
    write(repo, f"{NEW_ITEM}/routing.md", declaration(NEW_ITEM))
    commit(repo, "declare")
    write(repo, f"{NEW_ITEM}/rounds/round-1.md", body)
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "Contract changes" in out


# --- the rows, as every document that describes them spells them ------------


CARRIERS = (
    ("templates", "sdd-round.md"),
    ("docs", "review-handoff-protocol.md"),
    ("docs", "review-chain-spec.md"),
    ("skills", "code-review", "SKILL.md"),
    ("skills", "code-review", "scripts", "chain_check.py"),
)


@pytest.mark.parametrize("parts", CARRIERS)
def test_the_rows_are_spelled_the_same_everywhere(parts):
    """A row spelled one way in the template and another in the check is a
    record a session writes from the template and CI refuses."""
    text = read(*parts)
    assert "Contract changes" in text, "/".join(parts)
    assert "New units" in text, "/".join(parts)


def test_the_template_rows_are_rows_a_session_can_copy():
    """Counted outside comments, because `chain_check` reads a commented row
    as absent — a template whose only mention is commented ships a record
    that fails the moment it is written."""
    lines = reader_module().strip_comments(
        read("templates", "sdd-round.md").splitlines()
    )
    for label, needles in (
        ("| Contract changes", ("`none`", "→")),
        ("| New units", ("`none`",)),
    ):
        rows = [line for line in lines if line.strip().startswith(label)]
        assert len(rows) == 1, f"{label}: {len(rows)} rows outside comments"
        value = rows[0].split("|")[2].strip()
        assert value.startswith("<") and value.endswith(">"), (
            f"a template must not ship a claim, and `{value}` is one"
        )
        for needle in needles:
            assert needle in value, f"{label} row offers no `{needle}`"


def test_the_protocol_carries_the_rows_and_moved_its_draft():
    lines = reader_module().strip_comments(
        read("docs", "review-handoff-protocol.md").splitlines()
    )
    # `Loses a record or crashes` joins the two: `templates/sdd-round.md:7`
    # names this document as the file that carries the format, and round 1 of
    # `1788472135-…` found it carrying neither of the branch's rules —
    # `grep -c` for the floor row returned 0.
    # `Ran by` joins them on the same footing and for the same reason (#137):
    # a session writing a record from THIS document rather than from the
    # template reads the field table and nothing else, so a row missing here
    # is a row that session does not know exists — and `chain_check.py`
    # refuses the record it then writes.
    for label in (
        "| Contract changes",
        "| New units",
        "| Loses a record or crashes",
        "| Ran by",
    ):
        rows = [line for line in lines if line.strip().startswith(label)]
        assert len(rows) == 1, f"{label}: {len(rows)} rows outside comments"
        required = rows[0].split("|")[2].strip()
        assert required.startswith("yes"), (
            f"the Required column reads `{required}` — a field the protocol "
            "does not require is a field a record can leave out"
        )
    units = next(line for line in lines if line.strip().startswith("| New units"))
    for needle in ("depth", "`;`"):
        assert needle in units, (
            f"the protocol's `New units` row offers no `{needle}`, so a "
            "record written from THIS document is refused by the checker — "
            "and the comma spelling it still teaches is the one refused"
        )
    # The claim is that the rows arrived WITH a bump, not that the draft
    # stays at the number they arrived in — the literal `Draft 0.7` spelling
    # broke at the very next bump (0.8), which is this pin's own class of
    # finding. The title/Status agreement is pinned in
    # test_the_handoff_before_round_one.py.
    title = read("docs", "review-handoff-protocol.md").splitlines()[0]
    match = re.search(r"draft (\d+\.\d+)", title)
    assert match, f"the title names no draft: `{title}`"
    assert float(match.group(1)) >= 1.1, "a changed field moves the draft"


def test_the_protocol_no_longer_grandfathers_both_rows_by_one_key():
    """`DEPTH_FROM` made that sentence false for half of `New units`: the row
    is owed from one second and the depth in it from a later one, so a
    project can be past the first cutoff and before the second."""
    text = " ".join(read("docs", "review-handoff-protocol.md").split())
    assert "keyed the same way as `Fixes checked by`'s grandfathering" in text, (
        "the sentence that carries the grandfathering moved, and this case "
        "cannot say what it now claims"
    )
    assert "the depth has a cutoff of its own" in text, (
        "the protocol still says one key grandfathers both fix-surface rows, "
        "which stopped being true when the depth got a cutoff of its own"
    )


def test_the_documents_say_why_older_records_are_excused():
    """`SURFACE_FROM` with no reason beside it reads as a leftover constant,
    and removing it turns a release pull request red on merged history.

    The constant's NAME alone is a tautology for `chain_check.py` — it is
    defined and read there, so the file cannot stop containing the string
    while the code runs. That was round 2's ❓ 10 on the sibling case for
    `RUNNER_FROM`, and §12 reaches here because the shape is the same rather
    than because this row was reported. Each file is pinned on a phrase from
    the reason as well, which a deletion actually removes.
    """
    for parts, reason in (
        (("docs", "review-chain-spec.md"), "deriving a depth now for"),
        (
            ("skills", "code-review", "scripts", "chain_check.py"),
            "nobody re-read fabricates a review",
        ),
    ):
        text = flat(*parts)
        assert "SURFACE_FROM" in text, "/".join(parts)
        # Counted, not merely present. `fixes nobody re-read` and
        # `a merged record has no honest repair` each appear twice in
        # `chain_check.py`, so a needle spelled either way is satisfied by
        # the copy belonging to a different cutoff.
        assert text.count(reason) == 1, (
            f"{'/'.join(parts)} does not carry the reason exactly once "
            "beside `SURFACE_FROM`"
        )
    spec = flat("docs", "review-chain-spec.md")
    assert "print" in spec and "grandfather" in spec


# --- the verifying round's finding surface ----------------------------------

FINDING_SURFACE = {
    ("skills", "code-review", "SKILL.md"): (
        "treats it as a finding surface — *is this correct* — rather than a "
        "verification surface"
    ),
    ("agents", "warden.md"): (
        "judge them as code — *is this correct* — never as fixes"
    ),
}
SURFACE_BACKWARDS = (
    "verification surface — *is this correct* — rather than a finding",
    "never as code",
    "as fixes, never as code",
)


@pytest.mark.parametrize("parts", sorted(FINDING_SURFACE))
def test_new_units_are_a_finding_surface_not_a_verification_surface(parts):
    """The warden's own scope rule says *answers rather than new findings*,
    which read literally skips the one set of units nobody has reviewed.
    Round 4's fix commit created eight; four carried defects."""
    text = flat(*parts)
    assert FINDING_SURFACE[parts] in text, "/".join(parts)
    for backwards in SURFACE_BACKWARDS:
        assert backwards not in text, f"{'/'.join(parts)}: {backwards}"
    assert "New units" in text, "/".join(parts)


# --- the review-skill rules issue #57 writes down ---------------------------


def test_the_paste_ready_rule_covers_premises_as_well_as_names():
    """The first clause covers invented names; three of one round's four 🔴
    arrived as sketches whose unexamined premise was the defect."""
    skill = flat("skills", "code-review", "SKILL.md")
    assert "A fix touching an OS boundary states its assumed precondition." in skill
    for boundary in (
        "path resolution",
        "file modes",
        "symlinks",
        "subprocess working directory",
        "encoding",
    ):
        assert boundary in skill, f"the precondition clause lost `{boundary}`"


CLOSINGS = (
    # Rule 6: one such rule cost three rounds and closed only by an owner
    # decision one level up (`generic_units`, rounds 4-6 of 1788229400).
    "An enumeration over an unbounded domain is a recorded limit, not a "
    "closed finding.",
    # Rule 7: rounds 4, 5 and 6 reported 15/15, 12/12 and 12/12 killed, and
    # all three were rounds whose fixes opened findings.
    "the pins discriminate — the fix is *tested* — and says nothing about "
    "whether it is *safe*",
    # Rule 8: 🟡 11-13 and 🟡 H were the same class one round apart; the
    # moment pins existed they found a fourth file nobody had covered.
    "A document claim gets a pin.",
)


@pytest.mark.parametrize("sentence", CLOSINGS)
def test_the_skill_refuses_the_three_closings_that_arrive_too_early(sentence):
    assert sentence in flat("skills", "code-review", "SKILL.md"), sentence
