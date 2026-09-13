"""Three readers run one checker over one tree and grade it differently.

`bin/evidence-check` -- the command every document names -- comes back exit 1
on drift. CI's `ledger` job runs the same script and renders exit 1 as a
warning. `broad-gate` runs it with `--strict`, where drift is exit 2 and the
branch comes back `NOT SEALED`. A session that runs the documented command
more often never finds this, because the documented command is not the one
that decides (#354).

The repair is one printed line on the one exit code where the readers
disagree, and this file is what keeps the line honest. Two halves:

  behavioural   the line appears on exit 1 and on no other exit code. Exit 0
                and exit 2 are states every reader grades alike, and a line
                that prints on every run is a line people learn to skip
  structural    the line asserts something about another file -- that
                `broad_gate.py` passes `--strict` at its ledger call site,
                that `bin/evidence-check` adds no flag of its own, and that
                `NOT SEALED` is a word `seal_stamp` actually prints. Held
                against those files here, so the assertion cannot go stale in
                silence (`questions.md` Q1, answered (a) by the owner)

**The sentence is written out in this file as a literal.** That is the
pinning `agent-contract` §14 asks for: the checker's wording cannot move
without this module going red, which is what keeps the next edit from
quietly taking the fact back.
"""

import ast
import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")
BROAD_GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")
SEAL_STAMP = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")
WRAPPER = os.path.join(ROOT, "bin", "evidence-check")


def load():
    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = load()

# The sentence, stated here and in the checker. Two statements of one fact is
# the point: neither can move without the other going red.
NOTICE = (
    "exit 1 is the lenient reading. `broad-gate` runs this same check with "
    "`--strict`, where drift is exit 2, and this tree would come back NOT SEALED."
)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


SERVICE = "def handler(x):\n    y = x + 1\n    return y\n"


def repo(tmp_path, body=SERVICE):
    """A repository whose one ledger row cites `src/service.py#handler` at the
    content it holds right now. Nothing here runs git: the checker calls git
    for nothing outside `--migrate`."""
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "seal" / "ledger").mkdir(parents=True)
    (d / "src" / "service.py").write_text(body, encoding="utf-8")
    places = ec.resolve("src/service.py", "handler", body)
    assert len(places) == 1, f"fixture anchor is not unique: {places}"
    a, b = places[0]
    h = ec.content_hash(body.splitlines()[a - 1 : b])
    (d / "seal" / "ledger" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `src/service.py#handler@{h}` |\n", encoding="utf-8"
    )
    return d


def drifted(tmp_path):
    """The same repository after the cited function changed and nobody said
    they re-read it. Drift, nothing broken, nothing old-format."""
    d = repo(tmp_path)
    (d / "src" / "service.py").write_text(
        "def handler(x):\n    y = x + 2\n    return y\n", encoding="utf-8"
    )
    return d


# --- behavioural: the line lands on exit 1 and on nothing else ---------------


def test_a_drifted_tree_is_told_what_the_gate_would_say(tmp_path):
    """S1. The documented command says what the deciding one will say."""
    r = run(["."], drifted(tmp_path))
    assert r.returncode == 1, r.stdout + r.stderr
    assert "1 drifted" in r.stdout, r.stdout
    assert NOTICE in r.stdout, f"the lenient run said nothing, verbatim:\n{r.stdout}"


def test_the_deciding_form_does_not_repeat_itself(tmp_path):
    """S2. A reader who passed `--strict` already ran the form that decides.
    Telling them about it is the line printed on every run that #354's own
    reasoning refuses."""
    r = run(["--strict", "."], drifted(tmp_path))
    assert r.returncode == 2, r.stdout + r.stderr
    assert NOTICE not in r.stdout, r.stdout


def test_a_clean_tree_is_silent(tmp_path):
    """S3. Exit 0 is a state every reader grades alike."""
    r = run(["."], repo(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr
    assert NOTICE not in r.stdout, r.stdout


def test_a_broken_anchor_is_silent(tmp_path):
    """S3. Exit 2 is a state every reader grades alike, so there is no
    disagreement to report."""
    d = repo(tmp_path)
    (d / "src" / "service.py").write_text("def other(x):\n    return x\n", "utf-8")
    r = run(["."], d)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "BROKEN" in r.stdout, r.stdout
    assert NOTICE not in r.stdout, r.stdout


def test_an_old_format_row_is_silent(tmp_path):
    """S3. OLD-FORMAT exits 2 with or without the flag, so both readers
    already agree and the remedy the run names is the migrator."""
    d = repo(tmp_path)
    (d / "seal" / "ledger" / "f.md").write_text(
        "# frag\n\n| CLAUSE | `src/service.py:1-3` |\n", encoding="utf-8"
    )
    r = run(["."], d)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "OLD-FORMAT" in r.stdout, r.stdout
    assert NOTICE not in r.stdout, r.stdout


def test_the_line_is_the_last_thing_an_exit_1_run_prints(tmp_path):
    """It is appended after the totals a reader compares it against, so a
    caller asserting on those lines by substring keeps working."""
    r = run(["."], drifted(tmp_path))
    assert r.stdout.rstrip().endswith(NOTICE), repr(r.stdout[-400:])


# --- the condition is the exit code itself ----------------------------------


def test_the_grading_is_one_function_and_the_line_reads_its_answer():
    """The condition for the line is *this run is about to return 1*, not a
    predicate written beside the grading that can drift from it."""
    zero = dict.fromkeys(("OK", "DRIFTED", "BROKEN", "EXTERNAL", "OLD-FORMAT"), 0)

    def code(strict=False, **totals):
        return ec.exit_code({**zero, **totals}, 0, 0, strict)

    assert code(OK=1) == 0
    assert code(DRIFTED=1) == 1
    assert code(DRIFTED=1, strict=True) == 2
    assert code(BROKEN=1) == 2
    assert code(BROKEN=1, strict=True) == 2
    assert ec.exit_code({**zero, "OLD-FORMAT": 1}, 0, 0, False) == 2
    assert ec.exit_code({**zero, "OLD-FORMAT": 1}, 0, 0, True) == 2
    # The records arm reaches the same grading through its own two counts.
    assert ec.exit_code(zero, 1, 0, False) == 2, "a refused record is exit 2"
    assert ec.exit_code(zero, 0, 1, False) == 1, "a drifted record is exit 1"
    assert ec.exit_code(zero, 0, 1, True) == 2


def test_the_checker_states_the_sentence_once():
    """One constant, and this module's literal is its second statement."""
    assert ec.LENIENT_NOTICE == NOTICE, repr(ec.LENIENT_NOTICE)


def test_the_sentence_is_one_line():
    """A reader greps for it and a case asserts it by substring. A sentence
    wrapped across two lines survives neither."""
    assert "\n" not in ec.LENIENT_NOTICE, repr(ec.LENIENT_NOTICE)


# --- structural: the line asserts something about three other files ---------


def ledger_call_site():
    """`broad_gate.py`'s `checks[LEDGER] = run(...)` call, parens balanced, so
    a reformatting that wraps the call does not read as a missing flag."""
    lines = read(BROAD_GATE).splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("checks[LEDGER]"):
            call, depth = "", 0
            for text in lines[i:]:
                call += text + "\n"
                depth += text.count("(") - text.count(")")
                if depth <= 0:
                    return call
            return call
    raise AssertionError("broad_gate.py has no checks[LEDGER] call site")


def failure_loop():
    """`gate()` and the loop inside it that collects every failing check.

    Read as a syntax tree rather than as text: the claim is about which
    checks the loop lets through, and a substring search cannot tell an
    exemption (`if name == LEDGER: continue`) from the enrichment already
    there (`if name == SUITE:`), which is not a skip at all."""
    parsed = ast.parse(read(BROAD_GATE))
    gates = [
        n
        for n in ast.walk(parsed)
        if isinstance(n, ast.FunctionDef) and n.name == "gate"
    ]
    assert len(gates) == 1, f"broad_gate.py has {len(gates)} functions named gate"
    loops = [
        n
        for n in ast.walk(gates[0])
        if isinstance(n, ast.For) and ast.unparse(n.iter) == "checks.items()"
    ]
    assert len(loops) == 1, f"gate() has {len(loops)} loops over checks.items()"
    return gates[0], loops[0]


def flag_the_notice_names():
    flags = re.findall(r"`(--[a-z-]+)`", ec.LENIENT_NOTICE)
    assert flags == ["--strict"], f"the notice names {flags}"
    return flags[0]


def test_the_gate_still_passes_the_flag_the_notice_names():
    """S4. The half of the sentence that is about another file. Delete
    `--strict` from `broad_gate.py`'s ledger call and the checker's line
    becomes a false statement -- this is what makes that go red instead of
    quiet."""
    call = ledger_call_site()
    flag = flag_the_notice_names()
    assert f'"{flag}"' in call, f"the gate no longer passes {flag}:\n{call}"
    assert "EVIDENCE" in call, f"this is not the ledger check any more:\n{call}"


def test_the_wrapper_holds_no_default_of_its_own():
    """S4. The notice says exit 1 is what *this* reader gives. It is true only
    while the wrapper passes arguments straight through and adds none."""
    exec_line = [
        line
        for line in read(WRAPPER).splitlines()
        if line.startswith("exec ") and "evidence_check.py" in line
    ]
    assert len(exec_line) == 1, exec_line
    assert '"$@"' in exec_line[0], exec_line[0]
    assert "--" not in exec_line[0], f"the wrapper adds a flag: {exec_line[0]}"


def test_the_notice_borrows_the_word_the_failing_gate_prints():
    """S4. `NOT SEALED` is `seal_stamp`'s word and the checker is borrowing
    it. A loan is honest while the lender still says it."""
    assert "NOT SEALED" in ec.LENIENT_NOTICE
    assert "NOT SEALED" in read(SEAL_STAMP), "seal_stamp no longer prints it"
    assert "broad-gate" in ec.LENIENT_NOTICE, "the notice names no reader"
    assert "exit 2" in ec.LENIENT_NOTICE, "the notice names no grading"


def test_a_failing_ledger_check_is_what_reaches_the_failure_form():
    """S4's third limb, and the one the case above does not reach.

    `test_the_notice_borrows_the_word_the_failing_gate_prints` shows that
    `seal_stamp` still says `NOT SEALED`. It does not show that a drifted
    tree gets there. Two steps carry it and neither is read anywhere else:
    `gate()` skips a check on its own exit code and on nothing else -- no
    exemption by name -- and a non-empty `failures` is what takes the
    failure form.

    Exempting the ledger check here is *make the broad gate lenient*, the
    one change `spec.md` §Scope puts out of bounds, and it would leave the
    checker printing a false sentence on every lenient run with the whole
    suite green. Round 1 measured exactly that: the mutation
    `if name == LEDGER or not check.failed: continue` left this module at 13
    passed."""
    gate, loop = failure_loop()
    skips = [
        ast.unparse(node.test)
        for node in ast.walk(loop)
        if isinstance(node, ast.If)
        and any(isinstance(stmt, ast.Continue) for stmt in node.body)
    ]
    assert skips == ["not check.failed"], (
        f"the failure loop skips a check on something other than that "
        f"check's own result: {skips}"
    )
    last = loop.body[-1]
    collected = (
        isinstance(last, ast.Expr)
        and isinstance(last.value, ast.Call)
        and ast.unparse(last.value.func) == "failures.append"
    )
    assert collected, (
        f"the loop no longer ends by collecting every check it let through: "
        f"{ast.unparse(last)}"
    )
    taken = [
        node
        for node in ast.walk(gate)
        if isinstance(node, ast.If) and ast.unparse(node.test) == "failures"
    ]
    assert len(taken) == 1, "gate() no longer branches on a non-empty `failures`"
    body = ast.unparse(taken[0])
    assert "stamp.not_sealed(" in body, f"the failure form is no longer taken:\n{body}"


DESCRIBES_THE_CHECK = (
    os.path.join("skills", "evidence-check", "SKILL.md"),
    "README.md",
    "README.ko.md",
    "CONTRIBUTING.md",
    os.path.join(".github", "workflows", "test.yml"),
)


def test_no_document_describes_the_lenient_reader_alone():
    """S5. Every document that tells a reader what drift exits has to name the
    reader that grades it otherwise. Each file needs one BLOCK carrying both
    names -- a mention of `broad-gate` in a table of agents three hundred
    lines away is not the strict reader named beside the lenient one."""
    missing = []
    for rel in DESCRIBES_THE_CHECK:
        blocks = read(os.path.join(ROOT, rel)).split("\n\n")
        if not any("--strict" in b and "broad-gate" in b for b in blocks):
            missing.append(rel)
    assert not missing, f"these describe one reader alone: {missing}"
