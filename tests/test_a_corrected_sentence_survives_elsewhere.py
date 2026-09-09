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
#
# Both commits were squashed into a release branch and their feature branches
# were later deleted, which took the last ref that reached them: a clone with
# `fetch-depth: 0` gets branches and tags, never `refs/pull/*`, so CI went red
# here the day the branch list was tidied. They are now anchored by the tags
# `fixture/survivor-pin-left-behind` and `fixture/survivor-class-left-standing`
# rather than by any branch. Delete either tag and every case below skips.
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
        "skipping and the check has nothing real left to be held to. Push "
        "the `fixture/survivor-*` tags back at these commits, or replace them "
        "with commits that carry the same two shapes -- a pin left behind by "
        "a reworded sentence, and a claim corrected at one coordinate and "
        "left at another"
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
    # And ONLY that one. This is where the floor is pinned from both sides:
    # raise it and the survivor goes missing, and take the corpus scale out of
    # the weighting -- so a one-run coincidence is worth `log2(F)` instead of
    # 1.0 -- and this range grows the false positive the calibration measured,
    # a single six-word run counted four ways.
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
    # **Under a floor that would admit them**, and a mutation sweep is why.
    # At the shipped floor those two records score 1.51 against 1.6, so this
    # case passed with the exclusion switched off entirely -- it was measuring
    # the threshold and reading as though it measured the exclusion. 1.4 is
    # below their score and above nothing else on this range.
    _code, text = run(
        "--range",
        f"{CLASS_LEFT_STANDING}^..{CLASS_LEFT_STANDING}",
        "--root",
        ROOT,
        "--floor",
        "1.4",
    )
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
    # Both shapes are named, because either one would have been a row. The
    # refusal used to name only the per-survivor table, and after #297 that
    # sentence would send somebody to write the shape they had not chosen.
    assert "no `| Path | Quote | Grounds |` or" in text, text
    assert "`| Range | Grounds |` row" in text, text


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


def test_one_independent_run_can_never_clear_the_floor():
    """Where the independence requirement actually lives.

    A run is worth `log2(F / df) / log2(F)`, at most 1.0 and only when nothing
    else carries the phrase, so a floor past 1.0 refuses every one-run
    candidate on its own. There used to be a second constant asserting the
    same thing and a mutation sweep found it could not change an answer --
    which is worse than redundant, because it told a reader the requirement
    lived in a count."""
    reader = module()
    assert reader.FLOOR > 1.0, (
        f"FLOOR is {reader.FLOOR}, so a single run can clear it and one "
        "six-word coincidence is a survivor again"
    )
    # And the cap is real, at both ends of a plausible corpus.
    for size in (3, 633, 100000):
        weight = reader.weights(size, {"a rare phrase": 1})["a rare phrase"]
        assert weight == pytest.approx(1.0), (
            f"a phrase unique in a {size}-file corpus is worth {weight}, not "
            "1.0; the unit is not one phrase that occurs nowhere else"
        )


def test_a_one_file_corpus_reports_nothing_rather_than_dividing_by_zero():
    """`log2(1)` is 0. A corpus with one file has no elsewhere, so the honest
    answer is that nothing can be reported -- not a traceback."""
    assert module().weights(1, {"a rare phrase": 1}) == {}


def test_an_exemption_row_with_no_quote_does_not_silence_a_whole_file(tmp_path):
    """The row that would have exempted everything.

    An empty quote is a zero-length word run, and a zero-length run is
    contained in every text. So a row with an empty Quote cell would silence
    its path entirely -- the *check nothing* value this design says it does
    not have. It is refused instead."""
    table = tmp_path / "survivors.md"
    table.write_text(
        "| Path | Quote | Grounds |\n|---|---|---|\n| `seal/ledger.md` |  | no quote |\n",
        encoding="utf-8",
    )
    code, text = run("--range", "HEAD..HEAD", "--root", ROOT, "--exempt", str(table))
    assert code == 2, (
        f"a row with an empty quote was accepted; exit {code}. An empty anchor "
        f"matches every text, so that row exempts a whole file\n{text}"
    )


def test_a_quote_whose_words_are_scattered_does_not_exempt():
    """The anchor is a run, not a bag of words.

    Every word of `report once findings` appears in the sentence below and
    none of them adjacently. Matching on membership would exempt a carrier
    that says something else entirely with the same vocabulary."""
    reader = module()
    candidate = reader.Sentence(
        "notes.md", 1, "The report says findings reach the record once verified."
    )
    rows = [("notes.md", reader.words("report once findings"), "why")]
    assert reader.exempted(candidate, rows) is None, (
        "a quote whose words are scattered through the text exempted it, so "
        "the anchor is a bag of words rather than a phrase"
    )
    contiguous = [("notes.md", reader.words("`findings` reach the record"), "why")]
    assert reader.exempted(candidate, contiguous) == "why", (
        "a quote that IS a run of the text did not match, so the case above "
        "passes for the wrong reason"
    )


# --- the escape for a documented deletion, which is one sentence ------------
#
# #297. A branch that DELETES a shipped section leaves every sentence of it
# standing in the durable copies that are supposed to survive a deletion --
# `docs/flow.md` §*A shipped version's section is deleted, not kept* names
# them. Measured on #293's own range: **153** survivors at 1.60-1.62, every
# one of them correct as a report and none of them a defect. Per-survivor
# rows would have cost 153 written sentences, which is not an escape anybody
# takes; the branch turns the check off instead, which is the outcome the
# escape exists to prevent.
#
# **The row is anchored on the range AND on the work item it lives in**, the
# way the quote is for a per-survivor row. Run the check over a different range
# and the row does not hold; run it over a range that touches nothing in the
# declaring work item and it does not hold either. The second anchor is round
# 1's 🔴 1 and the block further down is where it is measured: the range alone
# is not one, because `origin/<base>...HEAD` re-resolves per checkout.


def one_survivor(repo):
    """A range that corrects one statement and leaves its twin standing."""
    os.makedirs(repo, exist_ok=True)
    claim = (
        "The verdict cell is written by the reviewing round itself and the "
        "orchestrator never edits it afterwards."
    )
    build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst. {claim}\n\nSecond. {claim}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the claim, stated twice",
    )
    fixed = (
        "The verdict cell is written by the generator and the "
        "orchestrator leaves it untouched afterwards."
    )
    return build(
        repo,
        {"notes.md": f"# notes\n\nFirst. {fixed}\n\nSecond. {claim}\n"},
        "corrected the first statement only",
    )


GROUNDS = "the deleted section's sentences stand in the durable copies by design"


def test_an_undeclared_deletion_still_fails(tmp_path):
    """The floor the whole escape sits on, stated first.

    Without a declaration the range reports exactly as it does today. If this
    case ever passes, none of the ones below measure anything."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, text
    assert "notes.md" in text


def test_a_whole_range_row_excuses_the_survivors_of_that_range(tmp_path):
    """#297's chosen approach: one row with grounds, covering a range.

    Still PRINTED, and that is not negotiable — the per-survivor row's own
    rule. A row that silences something invisibly is a row nobody audits, and
    with 153 of them the grounds are the only thing a reader has to judge."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    table = tmp_path / "survivors.md"
    table.write_text(
        f"| Range | Grounds |\n|---|---|\n| `{head}^..{head}` | {GROUNDS} |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", str(table)
    )
    assert code == 0, f"the whole-range row did not silence the run\n{text}"
    assert GROUNDS in text, (
        "the grounds are not printed, so nobody can audit the declaration"
    )
    assert "notes.md" in text, (
        "and the survivors themselves are still named. A range row that "
        "prints only its own grounds hides what it covered"
    )


def test_a_whole_range_row_is_resolved_rather_than_string_matched(tmp_path):
    """The row a session actually writes names refs, not oids.

    In CI the range is `origin/<base>...HEAD`, and that is the spelling a
    smith copies into the declaration. Comparing the text would refuse it
    against the same range spelled as two SHAs, which is the same range."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    table = tmp_path / "survivors.md"
    table.write_text(
        f"| Range | Grounds |\n|---|---|\n| `HEAD^..HEAD` | {GROUNDS} |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", str(table)
    )
    assert code == 0, f"a ref expression naming the same range was refused\n{text}"


def test_a_whole_range_row_does_not_reach_a_different_range(tmp_path):
    """The anchor, and the direction it degrades in.

    This is the per-survivor row's *quote is the anchor* property in the
    shape a range row has. A declaration that covered any range would let a
    branch delete a section and hide a real correction's survivor behind the
    same sentence for the rest of the work item's life."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    table = tmp_path / "survivors.md"
    table.write_text(
        f"| Range | Grounds |\n|---|---|\n| `HEAD..HEAD` | {GROUNDS} |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", str(table)
    )
    assert code == 1, f"a row declaring a different range silenced this one\n{text}"
    assert "notes.md" in text


# --- the second anchor: the work item that wrote the declaration ------------
#
# Round 1's 🔴 1. The case above varies the SPEC's text on one checkout, and an
# elastic spec is identical to itself under that. `origin/<base>...HEAD` is not
# a range, it is a RELATION, and it resolves to whatever range the checkout it
# is read on is over -- so the case that reaches this varies the CHECKOUT and
# leaves the spec alone.

CLAIM_A = (
    "The verdict cell is written by the reviewing round itself and the "
    "orchestrator never edits it afterwards."
)
# Both claims are shaped the way `one_survivor`'s is, and the shape is what
# clears the floor rather than the length: the correction WRITES BACK a phrase
# in the middle, so the wording it removed reads as two stretches that do not
# touch. A single contiguous run is worth its rarest n-gram and no more --
# 1.0, under the floor -- because the floor's whole job is to require two
# independent pieces of evidence. Measured: this claim's first draft was one
# run, scored exactly 1.0, and the case would have gone green on a clean
# report rather than on the fix.
CLAIM_B = (
    "The exemption row is anchored by the range it declares and the checker "
    "never widens that reach afterwards."
)
ITEM_A = "seal/specs/1799000001-work-item-a"


def probe_git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def base_and_item_a(repo):
    """A base carrying two claims twice over, plus work item A's branch.

    Shaped after `one_survivor`, twice: each claim stands twice in its own
    file, and each branch corrects the first statement only, so the twin
    survives at that branch's tip and the range reports it.

    Leaves `work-item-a` checked out with `origin/release` still at the base,
    which is what a work item's own pull request looks like.
    """
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            "a-notes.md": f"# a\n\nFirst. {CLAIM_A}\n\nSecond. {CLAIM_A}\n",
            "b-notes.md": f"# b\n\nFirst. {CLAIM_B}\n\nSecond. {CLAIM_B}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "both claims, each stated twice",
    )
    probe_git(repo, "branch", "-M", "release")
    # A real remote, because `origin/<base>` is the spelling CI passes and the
    # one the module docstring recommends. Resolved against a local branch
    # name the case would be measuring a spelling nobody writes.
    probe_git(repo, "remote", "add", "origin", str(repo))
    probe_git(repo, "fetch", "-q", "origin")
    probe_git(repo, "switch", "-qc", "work-item-a")
    fixed = (
        "The verdict cell is written by the generator and the "
        "orchestrator leaves it untouched afterwards."
    )
    return build(
        repo,
        {
            "a-notes.md": f"# a\n\nFirst. {fixed}\n\nSecond. {CLAIM_A}\n",
            f"{ITEM_A}/survivors.md": (
                "| Range | Grounds |\n|---|---|\n"
                f"| `origin/release...HEAD` | {GROUNDS} |\n"
            ),
        },
        "work item A corrects its claim and declares the whole range",
    )


def declaration_of_a(repo):
    return os.path.join(str(repo), ITEM_A, "survivors.md")


def test_a_work_items_own_declaration_still_holds_in_the_ci_spelling(tmp_path):
    """The direction that would break the escape if the narrowing went too far.

    Work item A's row, read on A's own checkout over A's own range, covers it:
    the range touches the directory the row lives in, because a work item's
    routing declaration is committed there before its first edit. Refusing
    this would leave #297's 153-survivor case with no escape at all, so it is
    stated before the case that narrows anything.
    """
    repo = tmp_path / "probe"
    base_and_item_a(repo)
    code, text = run(
        "--range",
        "origin/release...HEAD",
        "--root",
        str(repo),
        "--exempt",
        declaration_of_a(repo),
    )
    assert code == 0, (
        "a work item's own declaration did not cover its own range, so the "
        f"escape #297 exists for is unusable\n{text}"
    )
    assert GROUNDS in text, f"the grounds are not printed\n{text}"
    # Without these two the case passes on a report that found nothing, which
    # measures the fixture rather than the declaration.
    assert "a-notes.md" in text, (
        f"A's own survivor was never found, so nothing was excused\n{text}"
    )
    assert "every survivor is excused by a row above" in text, (
        f"the run was clean rather than declared\n{text}"
    )


def test_a_declaration_does_not_reach_a_work_item_that_did_not_write_it(tmp_path):
    """Round 1's 🔴 1, and the reason the range alone was not an anchor.

    `hygiene.yml` hands every `seal/specs/*/survivors.md` in the tree to every
    run, and a `survivors.md` lives from the work item's first row until the
    release that ships it. So work item A's row, spelled the way CI and the
    docstring both spell it, resolved on work item B's checkout to exactly B's
    own range — matched it, excused every one of B's survivors, and turned the
    step off for the rest of the release. That is the outcome the escape
    exists to prevent, arriving through the escape.

    The declaration is refused here and it PRINTS. A row that quietly stopped
    applying is the one failure a rotting anchor must not have, and that rule
    binds in this direction too.
    """
    repo = tmp_path / "probe"
    base_and_item_a(repo)
    probe_git(repo, "switch", "-q", "release")
    probe_git(repo, "merge", "-q", "--ff-only", "work-item-a")
    probe_git(repo, "fetch", "-q", "origin")
    probe_git(repo, "switch", "-qc", "work-item-b", "release")
    fixed = (
        "The exemption row is anchored by the work item and the checker "
        "leaves that reach untouched afterwards."
    )
    build(
        repo,
        {"b-notes.md": f"# b\n\nFirst. {fixed}\n\nSecond. {CLAIM_B}\n"},
        "work item B corrects its claim and declares nothing",
    )
    code, text = run(
        "--range",
        "origin/release...HEAD",
        "--root",
        str(repo),
        "--exempt",
        declaration_of_a(repo),
    )
    assert code == 1, (
        "work item A's declaration excused work item B's whole run, so one "
        "merged row turns the step off for every later branch cut from the "
        f"same base\n{text}"
    )
    assert "b-notes.md" in text, f"B's own survivor was not reported\n{text}"
    assert "1799000001-work-item-a" in text, (
        "the refused declaration is not printed with the work item it belongs "
        f"to, so nobody reading the report can tell why it did not apply\n{text}"
    )


def test_a_range_row_that_does_not_resolve_silences_nothing_and_says_so(tmp_path):
    """Reported, never exit 2, and the reason is a landmine avoided.

    A `survivors.md` lives in the tree from the work item's first row until
    the release that ships it, and the refs its range names — a release
    branch — get deleted. Refusing the whole run then would turn every later
    range's check into exit 2 for a row that has nothing to do with it."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    table = tmp_path / "survivors.md"
    table.write_text(
        f"| Range | Grounds |\n|---|---|\n| `origin/gone..HEAD` | {GROUNDS} |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", str(table)
    )
    assert code == 1, f"an unresolvable declaration silenced the run\n{text}"
    assert "origin/gone..HEAD" in text, (
        "and it names the row that could not be resolved. A declaration that "
        "quietly stopped applying is the one failure a rotting anchor must "
        "not have"
    )


def test_a_file_holding_only_a_range_row_is_not_refused_as_empty(tmp_path):
    """A range row IS a row.

    The emptiness refusal exists because a file that silences nothing was
    probably not written. A file holding one range row was written, and
    reading it as empty would refuse the very shape #297 adds."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    table = tmp_path / "survivors.md"
    table.write_text(
        f"| Range | Grounds |\n|---|---|\n| `{head}^..{head}` | {GROUNDS} |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", str(table)
    )
    assert code != 2, f"a file holding one range row was refused as empty\n{text}"


def test_a_range_row_with_no_grounds_is_not_a_declaration(tmp_path):
    """The grounds are the whole content of the escape.

    What a reviewer reads is the written sentence; a row without one silences
    153 places on the strength of nothing. It is not a row, so a file holding
    only that is refused as empty — which is the loud direction."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    table = tmp_path / "survivors.md"
    table.write_text(
        f"| Range | Grounds |\n|---|---|\n| `{head}^..{head}` |  |\n",
        encoding="utf-8",
    )
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", str(table)
    )
    assert code == 2, f"a range row with empty grounds was accepted\n{text}"


def test_a_path_row_and_a_range_row_are_told_apart(tmp_path):
    """Asked of the parser, because the two shapes share a file.

    A path cell cannot be read as a range and a range cell cannot be read as
    a path — the second is what would happen to `| A..B | grounds |` under
    the old parser, which needed three cells and skipped it in silence."""
    reader = module()
    table = tmp_path / "survivors.md"
    table.write_text(
        "| Path | Quote | Grounds |\n|---|---|---|\n"
        "| `seal/ledger.md` | never a leaf | the row records its own correction |\n"
        # Two cells, which is the documented range shape, sitting in the same
        # table as a three-cell path row. That is how the two coexist in one
        # `survivors.md` — the file takes both and the first cell decides.
        "| `abc1234..def5678` | a documented deletion |\n",
        encoding="utf-8",
    )
    rows, ranges = reader.read_exemptions([str(table)])
    assert [where for where, _q, _g in rows] == ["seal/ledger.md"], (
        f"a range row was read as a per-survivor row, whose path cell it is not: {rows}"
    )
    # Three elements, and the third is the file the row was read from. That is
    # the declaration's second anchor: `whole_range` asks whose work item it
    # is, because the range spelling CI passes re-resolves per checkout and so
    # anchors nothing on its own.
    assert ranges == [("abc1234..def5678", "a documented deletion", str(table))], ranges


def test_a_three_dot_range_starts_at_the_merge_base(tmp_path):
    """`A...B` is what a pull request compares, and it is not `A..B`.

    **Asked of `parse_range` rather than through a report, and that is a
    decision with a reason.** Three end-to-end fixtures were built for this
    and each was absorbed by a different part of the design: a base's
    additions read as removals under `A..B`, but they survive nowhere at `B`;
    where both sides wrote the same sentence, `wanted` subtracts it as wording
    the range also added; and an identical copy shares one contiguous run,
    which the floor refuses. So the difference the merge base makes is real in
    the input and hard to make visible in the output on a two-file probe.

    What the unit promises is that `A...B` starts at the merge base, and that
    is what is asked here. `docs/review-handoff-protocol.md`'s own reason for
    the spelling stands behind it: CI compares against the base a pull request
    actually has, and reading `...` as `..` would hand this check every commit
    the base made too."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    common = build(repo, {"a.md": "# a\n\nFirst.\n"}, "the common commit")
    base = build(repo, {"a.md": "# a\n\nFirst. Second.\n"}, "the base moves on")
    subprocess.run(
        ["git", "-C", str(repo), "checkout", "-q", "-b", "side", common], check=True
    )
    tip = build(repo, {"b.md": "# b\n\nThe branch's own.\n"}, "the branch moves on")

    reader = module()
    two = reader.parse_range(str(repo), f"{base}..{tip}")
    three = reader.parse_range(str(repo), f"{base}...{tip}")
    assert two == (base, tip), f"`A..B` did not resolve to its two ends: {two}"
    assert three == (common, tip), (
        f"`A...B` resolved to {three[0][:7]}..{three[1][:7]} where the merge "
        f"base is {common[:7]}. Read as `A..B`, this check is handed every "
        "commit the base made as well, and reports a branch for wording it "
        "never touched"
    )
    assert two != three, (
        "the two spellings resolved to the same range, so this probe's tips "
        "never diverged and the case is measuring nothing"
    )


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


def test_the_workflow_step_skips_a_release_range_and_says_why():
    """The range is what decides whether this check means anything.

    It was calibrated over 77 fix-pass ranges and its floor of 1.6 was chosen
    against that curve. A pull request into `main` carries the union of every
    work item the release holds, which is a range no fix pass ever writes: one
    item's removed wording is scored against four other items' prose, and each
    of those items was already checked at its own pull request. Measured on the
    release that shipped this check — 72 places reported, not one of them a
    survivor of the range that removed the wording.

    The guard prints rather than being a job-level `if:`, which is the shape
    the two steps above it already use: a skipped step reads as *did not run*,
    and a printed line says which of the two it was.
    """
    workflow = read(".github", "workflows", "hygiene.yml")
    step = workflow[workflow.index("- name: wording this branch removed") :]
    step = step[: step.index("\n      - name:", 1)]
    assert 'github.base_ref }}" = "main" ]' in step, (
        "the survivor step does not bound itself to a release branch's pull "
        "requests, so a release pull request scores five work items against "
        "each other"
    )
    assert "exit 0" in step, (
        "the guard does not let the step pass on a release pull request"
    )
    assert "not a range a fix pass wrote" in step, (
        "the guard skips without saying why, which is the state where the "
        "next reader deletes it"
    )


@pytest.mark.parametrize(
    "carrier",
    [
        ("skills", "code-review", "orchestration.md"),
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
    skill = read("skills", "code-review", "orchestration.md")
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
