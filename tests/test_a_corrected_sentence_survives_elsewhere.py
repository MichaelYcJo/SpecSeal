"""A range's removed wording is looked for everywhere else in the tree.

`agent-contract` §12 -- *a defect belongs to a class; do not fix the
coordinate* -- reaches every agent at startup and has been re-broken seven
times, once by a session that had read it and restated it as the cap. #180's
answer is a check rather than an eighth sentence, and this module is what holds
the check to the two events it was built from.

**Both are real commits in this repository, not fixtures**, and that is the
whole design of this file. A check that reports survivors and has never
reported one is a sentence with a shebang.

  `7bcf36a`  reworded `agents/warden.md` §6 and left `GENERATOR_NAMED[WARDEN]`
             in `tests/test_the_rules_have_one_owner.py` pinning the sentence
             it replaced. That module was red from this commit through two
             review rounds and two broad gates (#269), because contract §2
             reserves the broad gate for the orchestrator. The pin is one
             sentence split across two adjacent string literals, so no LINE
             holds it and nothing line-oriented finds it.

  `ad6f81a`  corrected a docstring that called a join's receiver *an argument
             ... never a leaf* and left the identical claim in the work item's
             ledger fragment and in `seal/ledger.md` row R3, the shared file a
             reader meets first (#267). Those rows PARAPHRASE rather than
             copy: the longest identical run is three words.

The cases resolve those commits and skip if they are gone. A feature branch
squashes into its release branch by rule, so these SHAs live only while the
unsquashed branches do -- `test_the_measured_commits_are_still_here` is the one
case that FAILS rather than skips, so their disappearance is reported once
rather than turning this whole module green by vacancy.
"""

import importlib.util
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "code-review", "scripts", "survivor_check.py")

# The two measured events, and what each one left standing.
PIN_LEFT_BEHIND = "7bcf36a"
PIN_CARRIER = "tests/test_the_rules_have_one_owner.py"
CLASS_LEFT_STANDING = "ad6f81a"
CLASS_CARRIERS = (
    "seal/ledger.md",
    "seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md",
)
# The round record and the reviewer's report for the same round both quote the
# finding's wording verbatim. Neither is a survivor: a round record states a
# past state by design.
CLASS_ROUND_RECORDS = (
    "1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds"
)


def module():
    spec = importlib.util.spec_from_file_location("specseal_survivor_check", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def resolves(rev):
    out = subprocess.run(
        ["git", "-C", ROOT, "rev-parse", "--verify", "-q", rev + "^{commit}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return out.stdout.strip() if out.returncode == 0 else None


def run(*args):
    out = subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return out.returncode, out.stdout + out.stderr


def over(commit):
    """The check over one commit's own range, as text plus its exit code."""
    return run("--range", f"{commit}^..{commit}", "--root", ROOT)


def paths_in(text):
    """The coordinates a report names, one per reported survivor."""
    return [
        line.split(":")[0]
        for line in text.splitlines()
        if line and not line.startswith((" ", "survivor-check")) and ":" in line
    ]


# --- the two events -------------------------------------------------------


def test_the_measured_commits_are_still_here():
    """The one case that fails rather than skips.

    Every other case here skips when its commit is gone, which is right --
    a squash is not a defect. What is a defect is this module quietly
    measuring nothing, so exactly one case says so out loud."""
    missing = [
        rev for rev in (PIN_LEFT_BEHIND, CLASS_LEFT_STANDING) if not resolves(rev)
    ]
    assert not missing, (
        f"{missing} no longer resolve, so every case in this module is now "
        "skipping and the check has nothing real left to be held to. Either "
        "restore the branches that carry them or replace them with commits "
        "that carry the same two shapes -- a pin left behind by a reworded "
        "sentence, and a claim corrected at one coordinate and left at another"
    )


def test_a_reworded_sentence_reports_the_pin_it_left_behind():
    """#269, and the case a literal grep cannot pass.

    The surviving pin is `"... from this report once the "` followed by
    `"orchestrator has verified its findings"` -- two adjacent string
    literals. Normalisation collapses the quotes and the line break, which is
    the only reason this is findable at all."""
    if not resolves(PIN_LEFT_BEHIND):
        pytest.skip(f"{PIN_LEFT_BEHIND} is not in this clone")
    code, text = over(PIN_LEFT_BEHIND)
    assert code == 1, f"the range reported nothing; exit {code}\n{text}"
    assert PIN_CARRIER in text, (
        f"{PIN_CARRIER} still pinned the sentence this commit replaced, and "
        f"the check did not name it:\n{text}"
    )
    assert "has verified its findings" in text, (
        "the report does not print the wording that survived, so a reader "
        f"cannot find it:\n{text}"
    )
    # And ONLY that one. This is where both thresholds are pinned from the
    # outside: raise `FLOOR` and the survivor goes missing, drop `SHARED_FLOOR`
    # to one and this range grows the false positive the calibration measured
    # -- `plan.md` records it as a single six-word run counted four ways.
    named = paths_in(text)
    assert named == [PIN_CARRIER], (
        f"the range reported {named}; the pin is the one thing standing, and "
        f"anything beside it is the score letting a coincidence through:\n{text}"
    )


def test_the_report_names_the_sentence_that_was_corrected_too():
    """A coordinate on its own is half an answer.

    The reader has to decide whether the survivor is stale or deliberate, and
    that needs the wording that replaced it -- which lives in the other file."""
    if not resolves(PIN_LEFT_BEHIND):
        pytest.skip(f"{PIN_LEFT_BEHIND} is not in this clone")
    _code, text = over(PIN_LEFT_BEHIND)
    assert "agents/warden.md" in text, (
        f"the report does not say where the sentence was corrected:\n{text}"
    )
    for word in ("standing", "corrected", "shared"):
        assert re.search(rf"^\s+{word}\b", text, re.M), (
            f"the report has no `{word}` line, so it names a coordinate and "
            f"not what a reader has to compare:\n{text}"
        )


@pytest.mark.parametrize("carrier", CLASS_CARRIERS)
def test_a_correction_at_one_coordinate_reports_the_class(carrier):
    """#267, and the case a phrase floor cannot pass.

    The shared file is in this list on purpose. Round 3 found both, and the
    fragment's own header paragraph says why the shared one matters more: a
    claim corrected only in a fragment leaves the false one standing where a
    reader will find it first."""
    if not resolves(CLASS_LEFT_STANDING):
        pytest.skip(f"{CLASS_LEFT_STANDING} is not in this clone")
    code, text = over(CLASS_LEFT_STANDING)
    assert code == 1, f"the range reported nothing; exit {code}\n{text}"
    assert carrier in text, (
        f"{carrier} still carried the claim this commit corrected in the "
        f"docstring, and the check did not name it:\n{text}"
    )


def test_a_record_of_a_past_round_is_not_a_survivor():
    """The by-construction exclusion, measured on the range that needs it.

    `round-2.md` and `round-2-report.md` both quote the finding's wording, so
    without this exclusion the same range reports four places where two are
    the reviewer describing the defect."""
    if not resolves(CLASS_LEFT_STANDING):
        pytest.skip(f"{CLASS_LEFT_STANDING} is not in this clone")
    _code, text = over(CLASS_LEFT_STANDING)
    named = paths_in(text)
    assert named, f"the report named no coordinate at all:\n{text}"
    offenders = [path for path in named if CLASS_ROUND_RECORDS in path]
    assert not offenders, (
        f"{offenders} are round records, which quote the wording a round found "
        "and carry the SHA they were written against. Reporting one asks "
        f"somebody to correct a record of a past state:\n{text}"
    )


def test_a_run_that_removed_nothing_is_silent_and_says_what_it_read():
    """Exit 0, and a line naming what was examined.

    A check that prints only what it found cannot be told apart from one that
    looked at nothing, which is how a green step comes to mean nothing."""
    code, text = run("--range", "HEAD..HEAD", "--root", ROOT)
    assert code == 0, f"a range with no commits between its ends reported; {text}"
    assert "examined" in text, f"the run does not say what it read:\n{text}"
    assert re.search(r"examined \d+ files", text), (
        f"the run names no number of files, so `examined` is a word:\n{text}"
    )


# --- the reader ------------------------------------------------------------


def test_a_sentence_split_across_two_string_literals_reads_as_one():
    """The normalisation #269 turns on, asked of the function directly.

    Both halves of the pin, spelled as python spells them, have to come back
    as one word sequence -- otherwise the n-grams that cross the split never
    exist and the survivor is unreachable however good the score is."""
    reader = module()
    split = '        "`round_record.py new` writes the record from this report once the "\n        "orchestrator has verified its findings"'
    found = reader.sentences("probe.py", split)
    joined = " ".join(sentence.key for sentence in found)
    assert "report once the orchestrator has verified its findings" in joined, (
        "the two literals did not join, so no n-gram crosses the split and "
        f"the pin cannot be found at all: {joined!r}"
    )


def test_a_stray_strike_marker_cannot_reach_past_its_own_line():
    """The measured defect, pinned.

    `seal/ledger.md` carries an ODD number of `~~` markers, so one is
    unpaired. Written with DOTALL, the span after the stray one ran across
    lines and swallowed row R3 -- the check reported the fragment and stayed
    silent about the shared file, which is the carrier #267 is about."""
    reader = module()
    text = (
        "one ~~struck~~ two\n~~stray\nthree keeps its words\nfour ~~also struck~~ five"
    )
    blanked = reader.blank_struck(text)
    assert "struck" not in blanked.split("\n")[0], "a real strike was not blanked"
    assert "three keeps its words" in blanked, (
        "an unpaired marker reached across lines and blanked a later line, "
        f"which is how row R3 went missing: {blanked!r}"
    )
    assert blanked.count("\n") == text.count("\n"), (
        "blanking changed the line count, so every line number after a strike "
        "is now wrong"
    )


def test_a_table_row_is_not_one_sentence():
    """A ledger row is one line and thousands of words.

    Left whole, its token set contains most of the corpus and it matches
    anything. The `|` is what splits it into cells before sentences are
    looked for."""
    reader = module()
    row = "| the claim is here | `path#unit@abcd1234` | the grounds are here |"
    found = reader.sentences("seal/ledger.md", row)
    assert len(found) >= 3, (
        f"a three-cell row read as {len(found)} sentence(s); a cell boundary "
        "has to end one or a row matches everything"
    )


def test_overlapping_ngrams_count_as_one_piece_of_evidence():
    """The measurement that changed the metric.

    *be a second reader of the* is one six-word run. At `n = 3` it is four
    overlapping n-grams, and scored one by one it cleared 26 bits -- the
    clearest false positive of the first calibration. Both real survivors
    share exactly TWO runs that do not touch."""
    reader = module()
    words = ["be", "a", "second", "reader", "of", "the"]
    grams = reader.ngrams(words)
    assert len(grams) == 4, f"expected four trigrams, got {grams}"
    runs = reader.runs(grams, set(grams))
    assert len(runs) == 1, (
        f"four overlapping n-grams read as {len(runs)} pieces of evidence; "
        "one contiguous run is one piece however many ways it can be read"
    )
    total, named = reader.weigh(grams, set(grams), dict.fromkeys(grams, 1.0))
    assert total == 1.0, (
        f"the run scored {total} where its rarest n-gram is worth 1; summing "
        "the overlaps counts the same evidence once per position"
    )
    assert named == [("be a second reader of the", 1.0)], (
        f"the run is not named as the phrase a reader would search for: {named}"
    )


def test_two_separate_runs_are_two_pieces_of_evidence():
    """The other half, or the case above passes for a check that counts one.

    This is the shape both real survivors have: two stretches of shared
    wording with unshared words between them."""
    reader = module()
    words = ["alpha", "beta", "gamma", "nothing", "here", "delta", "epsilon", "zeta"]
    grams = reader.ngrams(words)
    shared = {"alpha beta gamma", "delta epsilon zeta"}
    runs = reader.runs(grams, shared)
    assert len(runs) == 2, f"two separated stretches read as {len(runs)}: {runs}"
    total, named = reader.weigh(grams, shared, dict.fromkeys(grams, 1.0))
    assert total == 2.0, f"two independent runs scored {total}, not 2"
    assert len(named) == 2, f"the report names {len(named)} phrase(s): {named}"


def build(where, files, message):
    """Commit `files` into a repository at `where`, and answer with the sha.

    Git is driven from python rather than from a shell line, per contract §8:
    a probe that commits reaches the commit gate exactly as real work does,
    and the prompt lands on whoever is at the keyboard -- which, in a suite
    run, is nobody."""
    where = str(where)
    if not os.path.isdir(os.path.join(where, ".git")):
        for command in (
            ["init", "-q", "-b", "main"],
            ["config", "user.email", "probe@example.com"],
            ["config", "user.name", "probe"],
            ["config", "commit.gpgsign", "false"],
        ):
            subprocess.run(["git", "-C", where, *command], check=True)
    for name, body in files.items():
        path = os.path.join(where, name)
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(
            path
        ) else None
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(body)
    subprocess.run(["git", "-C", where, "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", where, "commit", "-q", "--no-verify", "-m", message], check=True
    )
    out = subprocess.run(
        ["git", "-C", where, "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return out.stdout.strip()


def test_a_claim_corrected_in_one_place_and_left_in_another_of_the_same_file(tmp_path):
    """The counted difference, which membership cannot see.

    A sentence is *corrected* when the file holds it FEWER times after than
    before -- not when it is absent after. #267 is this shape one file wider:
    the docstring was repaired and two ledger rows carrying the same claim
    were not. Tested inside one file because that is the case a membership
    test gets wrong: the wording is still in the file, so it reads as
    untouched."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    # The rewrite below changes the sentence in TWO separated places, which is
    # the shape both real survivors have and the shape `SHARED_FLOOR` is set
    # for. Written first with a single contiguous change, this probe shared one
    # run and was correctly not reported -- a fixture defect that read as a
    # missing feature, and the reason the two spots are pointed out here.
    claim = (
        "The verdict cell is written by the reviewing round itself and the "
        "orchestrator never edits it afterwards."
    )
    build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {claim}\n\nSecond statement. {claim}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the claim, stated twice in one file",
    )
    fixed = (
        "The verdict cell is written by the generator and the "
        "orchestrator leaves it untouched afterwards."
    )
    head = build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {fixed}\n\nSecond statement. {claim}\n",
        },
        "corrected the first statement only",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the second statement still carries the claim the first one corrected, "
        f"in the same file, and the check called the range clean; exit {code}\n{text}"
    )
    assert "notes.md" in text, text


# --- the escape ------------------------------------------------------------


def test_an_exemption_silences_one_carrier_and_still_prints_it(tmp_path):
    """The escape, on the real range it is for.

    Printed rather than dropped: a row that silences something invisibly is a
    row nobody audits, and the grounds are what the next reader needs."""
    if not resolves(CLASS_LEFT_STANDING):
        pytest.skip(f"{CLASS_LEFT_STANDING} is not in this clone")
    table = tmp_path / "survivors.md"
    table.write_text(
        "| Path | Quote | Grounds |\n|---|---|---|\n"
        f"| `{CLASS_CARRIERS[0]}` | never a leaf | the row records its own correction |\n"
        f"| `{CLASS_CARRIERS[1]}` | never a leaf | the fragment side of the same row |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range",
        f"{CLASS_LEFT_STANDING}^..{CLASS_LEFT_STANDING}",
        "--root",
        ROOT,
        "--exempt",
        str(table),
    )
    assert code == 0, f"the exemptions did not silence the run; exit {code}\n{text}"
    assert "exempt" in text, f"an exempted survivor was dropped silently:\n{text}"
    assert "the row records its own correction" in text, (
        f"the grounds are not printed, so nobody can audit the row:\n{text}"
    )
    assert "excused" in text, (
        "the run says nothing survived, which is false when a survivor was "
        f"found and excused:\n{text}"
    )


def test_an_exemption_whose_quote_is_gone_stops_holding(tmp_path):
    """The anchor, and the direction it degrades in.

    A row naming a quote the standing text no longer carries does not silence
    it. That is the ledger's own behaviour: an anchor that stops resolving
    reports, it does not excuse."""
    if not resolves(CLASS_LEFT_STANDING):
        pytest.skip(f"{CLASS_LEFT_STANDING} is not in this clone")
    table = tmp_path / "survivors.md"
    table.write_text(
        "| Path | Quote | Grounds |\n|---|---|---|\n"
        f"| `{CLASS_CARRIERS[0]}` | never a petal | the quote is spent |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range",
        f"{CLASS_LEFT_STANDING}^..{CLASS_LEFT_STANDING}",
        "--root",
        ROOT,
        "--exempt",
        str(table),
    )
    assert code == 1, (
        f"a row whose quote is no longer in the text still silenced it; the "
        f"anchor has to rot loudly\n{text}"
    )
    assert CLASS_CARRIERS[0] in text


def test_an_exemption_file_with_no_rows_is_refused(tmp_path):
    """Exit 2, because a file that silences nothing was probably not written.

    Read as empty, it would be indistinguishable from a work item that judged
    every survivor legitimate -- and `seal/follow-up.md`'s first open row is
    about exactly that failure direction in a checker of claims."""
    table = tmp_path / "survivors.md"
    table.write_text("# survivors\n\nnothing judged yet.\n", encoding="utf-8")
    code, text = run("--range", "HEAD..HEAD", "--root", ROOT, "--exempt", str(table))
    assert code == 2, f"an exemption file with no rows was accepted; exit {code}"
    assert "no `| Path | Quote | Grounds |` row" in text, text


def test_a_second_exemption_file_with_no_rows_is_refused_too(tmp_path):
    """The one that was wrong when it was written.

    The emptiness check counted the rows collected SO FAR, so a second
    `--exempt` naming an empty file passed on the strength of the first
    one's rows."""
    good = tmp_path / "one.md"
    good.write_text(
        "| Path | Quote | Grounds |\n|---|---|---|\n| `a.md` | some text | why |\n",
        encoding="utf-8",
    )
    empty = tmp_path / "two.md"
    empty.write_text("# nothing\n", encoding="utf-8")
    code, text = run(
        "--range",
        "HEAD..HEAD",
        "--root",
        ROOT,
        "--exempt",
        str(good),
        "--exempt",
        str(empty),
    )
    assert code == 2, (
        f"the empty second file passed because the first one had rows; "
        f"exit {code}\n{text}"
    )
    assert "two.md" in text, f"the refusal names the wrong file:\n{text}"


# --- the refusals ----------------------------------------------------------


@pytest.mark.parametrize(
    "spec",
    ["not-a-range", "deadbeefdeadbeef..HEAD", "HEAD..deadbeefdeadbeef"],
)
def test_an_unusable_range_is_exit_2_with_a_sentence(spec):
    """Two is *nothing was examined*, and it has to be distinguishable from
    *nothing survived*. A traceback is neither."""
    code, text = run("--range", spec, "--root", ROOT)
    assert code == 2, f"`{spec}` was accepted; exit {code}\n{text}"
    assert "Traceback" not in text, text
    assert "survivor-check:" in text, f"the refusal does not name itself:\n{text}"


def test_a_three_dot_range_resolves_through_the_merge_base():
    """`A...B` is how a pull request spells its own comparison.

    Refusing it would send whoever runs this at a pull request to work the
    merge base out by hand, and CI passes exactly that form."""
    code, text = run("--range", "HEAD...HEAD", "--root", ROOT)
    assert code == 0, f"`A...B` was refused; exit {code}\n{text}"
    assert "examined" in text


# --- where it is run -------------------------------------------------------


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


@pytest.mark.parametrize(
    "carrier",
    [
        ("skills", "code-review", "SKILL.md"),
        ("agents", "smith.md"),
        (".github", "workflows", "hygiene.yml"),
    ],
)
def test_every_place_that_runs_the_check_names_the_command(carrier):
    """#269's second clause is the whole reason this case exists: the walk
    that would have caught the defect *lived in a reviewer's clone*. A check
    nothing in the tree invokes is that walk again."""
    text = read(*carrier)
    assert "survivor" in text and "--range" in text, (
        f"{'/'.join(carrier)} does not run the check with a range, so the "
        "check exists and nothing reaches it"
    )


def test_the_fix_pass_is_told_to_run_it_over_the_range_close_already_takes():
    """The range is not a new thing to work out.

    `round_record.py close --range <a>..<b>` already takes it, so the step
    costs one command and no derivation. Saying so is what keeps it from
    reading as a second range somebody has to establish."""
    skill = read("skills", "code-review", "SKILL.md")
    block = skill[skill.index("## Orchestrator: a fix pass resumes") :]
    block = block[: block.index("## Orchestrator: the run ends")]
    assert "survivor-check --range" in block, (
        "the fix-pass section does not name the check, so the one party that "
        "can run it is not told to"
    )
    assert "close" in block and "--range" in block


def test_the_windows_wrapper_points_at_the_same_script():
    """`bin/` is on the Bash tool's PATH while the plugin is enabled, and the
    two wrappers are resolved by different shells for the same command."""
    posix = read("bin", "survivor-check")
    windows = read("bin", "survivor-check.cmd")
    for text, name in (
        (posix, "bin/survivor-check"),
        (windows, "bin/survivor-check.cmd"),
    ):
        assert "survivor_check.py" in text, f"{name} does not name the script"
    assert "code-review" in posix and "code-review" in windows, (
        "one wrapper points into a different skill's scripts directory"
    )
