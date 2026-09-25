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
             leaves the broad gate to whichever agent definition assigns it
             and no reviewer's does. The pin is one sentence split across two
             adjacent string literals, so no LINE holds it and nothing
             line-oriented finds it.

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

import ast
import importlib.util
import os
import re
import shutil
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
# The cases name the tags rather than the commits' SHAs: a history rewrite
# moves each tag to its commit's new SHA, and a SHA written here would stop
# resolving while the tag still reaches the same commit.
PIN_LEFT_BEHIND = "fixture/survivor-pin-left-behind"
PIN_CARRIER = "tests/test_the_rules_have_one_owner.py"
CLASS_LEFT_STANDING = "fixture/survivor-class-left-standing"
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


# The two shapes the space requirement buys, one per alternative it was added
# to. Each is a genuine hand-wrapped continuation, and each was split by the
# bare `[-*+>#]` class this module used to carry — the second at `[-*+]`, the
# first at `#`. Dropping either lookahead turns its own arm red and nothing
# else, which is how they were measured.
WRAPPED_ONTO = (
    "#120's, and no other module reads that field",
    "**round 4** found it, and no other module reads that field",
)


@pytest.mark.parametrize("tail", WRAPPED_ONTO)
def test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence(tail):
    """The same class as `round_record.py#BLOCK_START`, one module over.

    `BLOCK` used to carry a bare `[-*+>#]`, so a hand-wrapped sentence whose
    second line opens with an issue number was split at a boundary that is
    not there — in a corpus of round records and ledger rows where a line
    beginning `#120` is ordinary prose. The consequence differs from the
    record generator's: nothing is truncated, the sentence is mis-scored, and
    a survivor whose evidence straddles the wrap becomes unreachable because
    no n-gram crosses the split.

    `.github/scripts/issue_claims_check.py` states the trap in its own
    comment and `seal/ledger.md` records it executed by mutation. This is the
    third carrier of that pattern and the last one that did not ask for the
    space CommonMark requires."""
    reader = module()
    text = f"the parser this work item was filed against is\n{tail}"
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert any(
        "filed against is" in k and "no other module reads" in k for k in keys
    ), (
        "the wrap was read as a block boundary, so the sentence split in two "
        f"and no n-gram crosses it: {keys!r}"
    )


# The alternative that predates this branch and that phase 4 retyped without
# pinning. Mutated to match nothing, the whole module stayed green — round 1's
# 🟡 5, and retyping a pattern is the cheapest moment it will have.
@pytest.mark.parametrize("rule", ["---", "___", "***", "==="])
def test_a_whole_line_of_one_marker_ends_the_segment(rule):
    """A thematic break and a setext underline are blocks in their own right.

    Without this alternative a claim above a horizontal rule and an unrelated
    claim below it land in one segment, which is the false positive
    `.github/scripts/issue_claims_check.py` spends its own whole-line
    alternatives to avoid. The hole runs in the same direction this branch
    closed one in: two unrelated claims merging and scoring as one."""
    reader = module()
    # No full stop above the rule, on purpose. `END` already ends a sentence
    # at `.!?;`, so a claim that carries one is separated whatever `BLOCK`
    # does — which is why round 1's paste-ready form of this case stayed
    # green with the alternative mutated to match nothing. The block boundary
    # has to be the only thing that can end this one.
    text = f"the claim above the rule\n{rule}\nan unrelated claim below it"
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert not any("above the rule" in k and "below it" in k for k in keys), (
        f"{rule!r} is a block of its own and the segment ran straight through "
        f"it: {keys!r}"
    )


# The ordered-list alternative, the second of the constant's five that nothing
# pins — same constant, same retyping, same argument as round 1's 🟡 5. It is
# the one worth taking for a reason the bullet and heading alternatives do not
# share: killing either of those widens the pattern, and
# `test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence` catches a
# widening from the other side. Killing this one is caught from neither.
#
# Only the `)` half can be pinned here. `END` ends a sentence at `.` before
# whitespace, so an arm written `1.` is green whatever `BLOCK` does — measured,
# and it is the same trap that made round 1's first attempt at the whole-line
# case useless. `1)x` is green for the other reason: no space after the
# delimiter, so it is prose under both spellings and the lookahead that says so
# is pinned by nothing.
@pytest.mark.parametrize("opener", ["1)", "12)"])
def test_an_ordered_list_item_ends_the_segment(opener):
    """A list item is a block, so the prose above it is a sentence of its own.

    Without this alternative a claim hard-wrapped above a list and the list's
    first item land in one segment, and an n-gram crosses a boundary that is
    real — the mis-scoring direction this module's constant exists to avoid,
    rather than the truncation `round_record.py` guards."""
    reader = module()
    # No full stop above the item, on purpose: the block boundary has to be
    # the only thing that can end this sentence.
    text = f"the claim above the item\n{opener} an unrelated claim below it"
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert not any("above the item" in k and "below it" in k for k in keys), (
        f"{opener!r} opens a list item and the segment ran straight through "
        f"it: {keys!r}"
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


# --- the range's own review paperwork --------------------------------------


# The wording a round finds and a fix corrects. Two stretches of shared text
# with unshared words between them, which is the shape both real survivors
# have and the shape the floor is set for -- a single contiguous change shares
# one run and is correctly not reported.
FOUND = (
    "The verdict cell is written by the reviewing round itself and the "
    "orchestrator never edits it afterwards."
)
REPAIRED = (
    "The verdict cell is written by the generator and the "
    "orchestrator leaves it untouched afterwards."
)
# A work item id of the shape the tree uses, so `records_a_past_round` matches
# on the path's own shape: a `rounds` directory inside a `specs` directory.
RECORD = "seal/specs/1700000000-a-claim-stands-in-two-places/rounds/round-1.md"


def test_a_round_record_the_range_added_does_not_subtract_the_survivor_it_quotes(
    tmp_path,
):
    """#365 -- the silencing input is produced by the review chain itself.

    A reviewer's report quotes the defective wording verbatim, because that is
    what a report is for. Left in the range, that quotation lands in
    `corrected`'s second return, `wanted` subtracts it, and the gate reports
    success having measured nothing -- on exactly the branches that went
    through review, which are the branches where a survivor is most likely.

    The POOL has refused round records since this module shipped. The RANGE
    did not, and the two are computed by different functions, which is why the
    docstring could state the intent while the code carried it on one side."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {FOUND}\n",
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the claim, stated in two files",
    )
    head = build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {REPAIRED}\n",
            RECORD: (
                "# Round 1\n\n"
                "## Findings\n\n"
                "The wording this round found stands in two files and was "
                "corrected in one of them.\n\n"
                f"{FOUND}\n"
            ),
        },
        "corrected notes.md, and posted the round record that quotes it",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "guide.md still carries the wording this range removed from notes.md, "
        "and the round record quoting that wording is what silenced it -- the "
        f"quote counted as wording the fix wrote; exit {code}\n{text}"
    )
    assert "guide.md" in text, f"the report does not name the survivor:\n{text}"
    # The filter goes on the path list, and a record the range ADDED removes
    # nothing, so the number of sentences the range is measured against is the
    # same number it was before the filter existed.
    assert re.search(r"against 1 sentence\(s\)", text), (
        f"the removed-sentence count moved when the filter was applied:\n{text}"
    )
    assert "/rounds/" not in text, (
        "the report names a round record. A record is out of the pool and out "
        f"of the range, so it is neither a survivor nor a source:\n{text}"
    )


def test_a_round_record_the_range_edited_does_not_become_a_source(tmp_path):
    """The other side of the same list, which is why the filter goes on `paths`.

    A sentence REMOVED from a round record is not corrected wording either.
    Filtering the added side alone would leave this range naming the record as
    the place a claim was corrected, and asking somebody to correct an account
    of a past state -- which is the one thing the pool has refused to do since
    this module shipped."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            RECORD: f"# Round 1\n\n## Findings\n\n{FOUND}\n",
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the record quotes the finding, and the guide carries the claim",
    )
    head = build(
        repo,
        {RECORD: f"# Round 1\n\n## Findings\n\n{REPAIRED}\n"},
        "reflowed the round record and nothing else",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "this range edited a round record and touched nothing else, and the "
        "check read that edit as a correction somebody has to chase into "
        f"guide.md; exit {code}\n{text}"
    )
    assert re.search(r"against 0 sentence\(s\)", text), (
        "wording removed from a round record still counts as wording the "
        f"range removed, so a range that touched only paperwork is not empty:\n{text}"
    )
    assert "/rounds/" not in text, (
        f"the report names the round record as the source of a correction:\n{text}"
    )


# --- the work item's own exemption file -------------------------------------
#
# One directory above its round records, and a stronger instance of the same
# defect: a `survivors.md` row QUOTES the surviving wording, because the quote
# is the anchor. Left in the range, the row's quote counts as wording the fix
# wrote and `wanted` subtracts the very survivor the row excuses (#507). Left
# in the pool, the file is one more carrier of exactly the phrases that
# produced the score, and a survivor near the floor drops under it (#308).
# Either way the `exempt` line never prints, and the check goes green because
# the survivor was not found rather than because it was excused. Measured on
# three pull requests of one release: 36 rows written, 7 consulted.
EXEMPTION = "seal/specs/1700000000-a-claim-stands-in-two-places/survivors.md"
EXCUSED = "the guide states it on purpose, and this row is what a reader audits"
# The two stretches of FOUND that REPAIRED does not write back, as `weigh`
# names them. Two independent runs is what clears the floor, and each is worth
# 1.0 only while nothing else in the pool carries it.
FOUND_RUNS = (
    "by the reviewing round itself and the",
    "the orchestrator never edits it afterwards",
)


def exemption_row(where, quote):
    """A per-survivor row for `where`, quoting `quote`, with grounds."""
    return f"| Path | Quote | Grounds |\n|---|---|---|\n| `{where}` | {quote} | {EXCUSED} |\n"


def in_repo(repo, path):
    return os.path.join(str(repo), *path.split("/"))


def test_an_exemption_file_the_range_added_does_not_subtract_the_survivor_it_quotes(
    tmp_path,
):
    """#507 -- the range half. Writing the row is what stopped the survivor
    being reported.

    Without `--exempt` the survivor has to be REPORTED: the row's quote is
    not wording the fix wrote, and the count of removed sentences is the
    count it was before the file existed. With `--exempt` naming the file,
    the same survivor prints under `exempt` with the row's grounds, which is
    the only thing a row was ever supposed to do. Red today at exit 0 in both
    runs, with no `exempt` line in either."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {FOUND}\n",
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the claim, stated in two files",
    )
    head = build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {REPAIRED}\n",
            EXEMPTION: exemption_row("guide.md", FOUND),
        },
        "corrected notes.md, and wrote the row that excuses guide.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "guide.md still carries the wording this range removed from notes.md, "
        "and the exemption file quoting that wording is what silenced it -- the "
        f"row's quote counted as wording the fix wrote; exit {code}\n{text}"
    )
    assert "guide.md" in text, f"the report does not name the survivor:\n{text}"
    assert re.search(r"against 1 sentence\(s\)", text), (
        f"the removed-sentence count moved when the filter was applied:\n{text}"
    )
    assert EXEMPTION not in text, (
        "the report names the exemption file. It is out of the pool and out of "
        f"the range, so it is neither a survivor nor a source:\n{text}"
    )
    code, text = run(
        "--range",
        f"{head}^..{head}",
        "--root",
        str(repo),
        "--exempt",
        in_repo(repo, EXEMPTION),
    )
    assert code == 0, f"the row did not excuse its own survivor; exit {code}\n{text}"
    assert re.search(
        rf"^\s+exempt\s+guide\.md:\d+ -- {re.escape(EXCUSED)}", text, re.M
    ), (
        "the survivor is not printed under `exempt` with the row's grounds, so "
        f"nobody at the pull request reads why it was excused:\n{text}"
    )
    assert "every survivor is excused by a row above (1)" in text, (
        f"the run was clean rather than excused:\n{text}"
    )


def test_an_exemption_file_in_the_pool_does_not_dilute_the_survivor_it_quotes(
    tmp_path,
):
    """#308 -- the corpus half, where the file was committed BEFORE the range.

    The file is then not in the diff at all, so the range half cannot be what
    silences the survivor: it is the pool. A four-file pool with two carriers
    of the quoted run weighs that run at `log2(4 / 2) / log2(4)`, half of what
    it is worth with the file absent, and the total falls under the floor.
    Asserted on the score and on which phrases are named, both -- two scores
    under the floor were both the weaker phrase when #308 was measured, and a
    score comparison alone passes for the wrong reason there."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {FOUND}\n",
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
            EXEMPTION: exemption_row("guide.md", FOUND),
        },
        "the claim in two files, and a row already written for the guide's copy",
    )
    head = build(
        repo,
        {"notes.md": f"# notes\n\nFirst statement. {REPAIRED}\n"},
        "corrected notes.md only",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "guide.md still carries the wording this range removed, and the "
        "exemption file sitting in the pool diluted the phrases it quotes under "
        f"the floor; exit {code}\n{text}"
    )
    assert "guide.md" in text, f"the report does not name the survivor:\n{text}"
    shared = re.search(r"^\s+shared\s+(\d+) phrase\(s\), ([\d.]+):(.*)$", text, re.M)
    assert shared is not None, f"the report has no `shared` line:\n{text}"
    assert shared.group(2) == "2.00", (
        f"the survivor scored {shared.group(2)} where each of its two runs is "
        "worth 1.0 with the exemption file out of the pool; the file is still "
        f"counted as a carrier of the phrases it quotes:\n{text}"
    )
    for phrase in FOUND_RUNS:
        assert phrase in shared.group(3), (
            f"the report does not name “{phrase}”, so the phrase reported is "
            f"not the one the row quotes:\n{text}"
        )


def test_the_report_is_the_same_with_the_exemption_file_and_with_it_deleted(
    tmp_path,
):
    """The property the three pull requests lost, as one invariant.

    The same range read at a tip that carries the file and at the same tip
    with the file deleted in a further commit has to name the same candidates
    with the same scores. The file is invisible to the search; only `--exempt`
    reads it."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    base = build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {FOUND}\n",
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the claim, stated in two files",
    )
    head = build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {REPAIRED}\n",
            EXEMPTION: exemption_row("guide.md", FOUND),
        },
        "corrected notes.md, and wrote the row",
    )
    os.remove(in_repo(repo, EXEMPTION))
    gone = build(repo, {}, "the exemption file deleted at the tip")

    def body(report):
        # Everything but the header, which names the tip's own SHA.
        return [
            line
            for line in report.splitlines()
            if not line.startswith("survivor-check:")
        ]

    code_with, with_file = run("--range", f"{base}..{head}", "--root", str(repo))
    code_gone, without = run("--range", f"{base}..{gone}", "--root", str(repo))
    assert code_gone == 1 and "guide.md" in without, (
        f"the range with no exemption file in it reported nothing, so the "
        f"invariant below is vacuous:\n{without}"
    )
    assert (code_with, body(with_file)) == (code_gone, body(without)), (
        "the report changes with the exemption file present at the tip, so the "
        f"file is an input of the search rather than a judgment on its result:\n"
        f"--- with the file\n{with_file}\n--- with it deleted\n{without}"
    )


def test_an_exemption_file_the_range_edited_does_not_become_a_source(tmp_path):
    """The other side of the same list, which is why the filter goes on `paths`.

    A quote REMOVED from an exemption row is not corrected wording. Filtering
    the added side alone would leave a reflowed row reading as a correction
    somebody has to chase into the file the row was written about."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            EXEMPTION: exemption_row("guide.md", FOUND),
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the row quotes the guide, and the guide carries the claim",
    )
    head = build(
        repo,
        {EXEMPTION: exemption_row("guide.md", REPAIRED)},
        "reflowed the exemption row and nothing else",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "this range edited an exemption file and touched nothing else, and the "
        "check read that edit as a correction somebody has to chase into "
        f"guide.md; exit {code}\n{text}"
    )
    assert re.search(r"against 0 sentence\(s\)", text), (
        "wording removed from an exemption row still counts as wording the "
        f"range removed, so a range that touched only the file is not empty:\n{text}"
    )
    assert EXEMPTION not in text, (
        f"the report names the exemption file as the source of a correction:\n{text}"
    )


# --- a phase record is a record (#460) --------------------------------------
#
# `phases/phase-N.md` says what a phase was asked, what building it found and
# what it removed -- a past state, quoted for audit, instructing nobody, which
# is what a round record is. It was in the sweep on both sides: in the pool it
# was reported as a survivor (two of four places in one measured pass) and
# diluted the real ones, and in the range it subtracted what it quoted, which
# is #507's shape one directory over.
PHASE = "seal/specs/1700000000-a-claim-stands-in-two-places/phases/phase-3.md"


def phase_record(quote):
    return f"# phase 3\n\n## What this phase found\n\nThe narrow answer as phase 3 left it. {quote}\n"


def test_a_phase_record_the_range_added_does_not_subtract_the_survivor_it_quotes(
    tmp_path,
):
    """The range half, in the shape S1 has for the exemption file."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {FOUND}\n",
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the claim, stated in two files",
    )
    head = build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst statement. {REPAIRED}\n",
            PHASE: phase_record(FOUND),
        },
        "corrected notes.md, and closed the phase with a record quoting it",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "guide.md still carries the wording this range removed from notes.md, "
        "and the phase record quoting that wording is what silenced it; "
        f"exit {code}\n{text}"
    )
    assert "guide.md" in text, f"the report does not name the survivor:\n{text}"
    assert re.search(r"against 1 sentence\(s\)", text), (
        f"the removed-sentence count moved when the filter was applied:\n{text}"
    )
    assert "/phases/" not in text, (
        f"the report names the phase record; a record is neither a survivor "
        f"nor a source:\n{text}"
    )


def test_a_phase_record_the_range_edited_does_not_become_a_source(tmp_path):
    """The other side of the list. A phase record is corrected in place while
    its work item is live -- which is what #423's pass did to two of them --
    and a sentence removed from one is not corrected wording."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            PHASE: phase_record(FOUND),
            "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the record quotes the finding, and the guide carries the claim",
    )
    head = build(
        repo,
        {PHASE: phase_record(REPAIRED)},
        "corrected the phase record in place and nothing else",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "this range edited a phase record and touched nothing else, and the "
        "check read that edit as a correction somebody has to chase into "
        f"guide.md; exit {code}\n{text}"
    )
    assert re.search(r"against 0 sentence\(s\)", text), (
        "wording removed from a phase record still counts as wording the "
        f"range removed:\n{text}"
    )
    assert "/phases/" not in text, (
        f"the report names the phase record as the source of a correction:\n{text}"
    )


@pytest.mark.parametrize("fillers", [0, 29])
def test_a_phase_record_standing_in_the_pool_is_not_a_survivor(tmp_path, fillers):
    """The pool half, and the one #460 paid for twice in one pass: a record
    carrying the removed wording was reported beside the real survivor, and
    answering it meant editing a record of a past state.

    Two pools, because the two directions of the defect need different sizes
    to show. On four files a fourth carrier halves every quoted phrase's
    weight and nothing clears the floor -- the record silences the survivor
    (exit 0). On 33 files the halving is small enough that both carriers
    clear it -- the record is REPORTED beside the survivor, which is what
    #460 measured in the tree. The `named` assertion is the only one that
    catches the second; the `code` assertion is the only one that catches
    the first. Round 1 found the case on one pool had seen only the first."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    files = {
        "notes.md": f"# notes\n\nFirst statement. {FOUND}\n",
        "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
        "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        PHASE: phase_record(FOUND),
    }
    for index in range(fillers):
        files[f"filler-{index}.md"] = (
            f"# filler {index}\n\nUnrelated prose number {index} that shares nothing at all.\n"
        )
    build(
        repo,
        files,
        "the claim in two files, and an earlier phase's record quoting it",
    )
    head = build(
        repo,
        {"notes.md": f"# notes\n\nFirst statement. {REPAIRED}\n"},
        "corrected notes.md only",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        f"guide.md's copy went unreported on a pool of {fillers + 4}; exit {code}\n{text}"
    )
    named = paths_in(text)
    assert "guide.md" in named, f"the report does not name the survivor:\n{text}"
    assert named == ["guide.md"], (
        f"the report names {named} on a pool of {fillers + 4}. A phase record "
        "quotes what a phase found and instructs nobody, so reporting it asks "
        f"somebody to correct a record of a past state:\n{text}"
    )


# Every exclusion the module docstring states, by the bold opener of its
# paragraph, in the order the section states them. The round record stays
# first: it is the one whose one-sided shipping (#365) is the reason the
# section names sides at all. A member of the class that is excluded in code
# and absent here is the docstring falling behind the code, which is the
# state #365 lived in for five releases.
EXCLUSIONS = (
    "**A record of a past round.**",
    "**The work item's own exemption file.**",
    "**A phase record.**",
    "**A released changelog section, and a gathered fragment.**",
)


def test_the_docstring_names_both_sides_of_the_round_record_exclusion():
    """`agent-contract` §14 -- a fix that changes a verdict pins the sentence.

    What this replaces read *Everything under a work item's `rounds/` is
    out.* and named no side, so a reader could not tell the pool from the
    range in it. That is the sentence which was true of the design and false
    of the code for five releases: the module's own account of itself was not
    wrong while only one of the two functions filtered, because it never said
    which one."""
    source = open(SCRIPT, encoding="utf-8").read()
    heading = "## What is excluded, by construction rather than by list"
    assert heading in source, (
        "the module docstring lost the section that states the exclusions, so "
        "the exclusions are now carried by code alone and a reader has no "
        "account of them to check the code against"
    )
    section = source[source.index(heading) + len(heading) :]
    section = section[: section.index("\n## ")]
    for opener in EXCLUSIONS:
        assert opener in section, f"{opener} is no longer an exclusion stated"
    positions = [section.index(opener) for opener in EXCLUSIONS]
    assert positions == sorted(positions), (
        f"the exclusions are stated out of order, and {EXCLUSIONS[0]} has to come first"
    )
    flats = {}
    for opener in EXCLUSIONS:
        paragraph = section[section.index(opener) :]
        paragraph = paragraph.split("\n\n")[0]
        flat = flats[opener] = " ".join(paragraph.split())
        for side in ("pool", "range"):
            assert side in flat, (
                f"the {opener} paragraph does not say the exclusion applies to "
                f"the {side}. Naming one side is exactly how this defect "
                "survived -- the intent was stated here and carried in one of "
                f"the two functions:\n{flat}"
            )
        assert "both sides" in flat, (
            f"the {opener} paragraph names the pool and the range without "
            "saying the exclusion holds on both SIDES of the range's path "
            "list, which leaves the added-side-only reading that was already "
            f"true and already wrong:\n{flat}"
        )
    flat = flats[EXCLUSIONS[0]]
    assert "`rounds/` is out." not in flat, (
        "the one-sided sentence is back: `Everything under a work item's "
        "`rounds/` is out.` states the intent and names neither function it "
        f"has to be true of:\n{flat}"
    )


# The predicate, and every place in the module that turns a git-derived path
# list into a judgment about prose. Declared here and CHECKED against the
# source below, rather than grepped for: the defect this case exists for was a
# call site the predicate had never reached, standing beside two it had, and
# what hid it is that the pool and the range are computed by different
# functions. A fourth one -- a `--since` flag, a second range, a cache of
# changed files -- turns this red until somebody classifies it.
#
# **The unit is the CALL SITE, and it took round 1 to make that true of the
# code.** `spec.md`'s class table is headed `Call site` and gives `corrected`
# and `whole_range` separate rows for the same spelling of the same command;
# this case keyed its walk by function NAME, so two sites in one scope
# collapsed to one entry and a list at module scope was not found at all. Two
# of the three shapes `plan.md:46-50` names as this change's own six-month
# failure scenario -- a second range, a cache of changed files -- passed it.
PREDICATE = "records_a_past_state"
FILTERS_ITS_OWN_LIST = {"corrected"}
# `tracked` returns an unfiltered list, so every caller is named with the
# filter it applies. `corrected` reads it at the range's left end for the
# gathered fragments alone (#564): `a_gathered_fragment` keeps only
# `<x>/specs/<id>/changelog.md`, which `records_a_past_state` can never name,
# and the text read there is held, never a source and never written.
FILTERED_BY_ITS_CALLERS = {
    "tracked": {"corpus": PREDICATE, "corrected": "a_gathered_fragment"},
}
NAMED_EXCEPTION = {
    "whole_range": (
        "asks whether the range belongs to the work item that WROTE a "
        "declaration, and a round record committed under "
        "seal/specs/<id>/rounds/ is evidence of that ownership rather than "
        "wording the fix wrote. Filtering here makes the ownership test "
        "stricter and can turn a legitimate declaration into `foreign` -- a "
        "row that quietly stops applying, which is the one failure a rotting "
        "anchor must not have and the direction this function's own docstring "
        "says it must not move in"
    ),
}
# Anything that lists paths, however it is spelled. Kept wider than the two
# forms the module uses today, so a fourth call site written as a direct
# `subprocess.run(["git", ...])` is found too.
LISTS_PATHS = {"--name-only", "ls-files", "ls-tree"}
# How many path-listing calls each scope is allowed to make. Module scope is a
# scope, and it is spelled here so a list built at import time is named rather
# than missed.
MODULE_SCOPE = "<module>"
PATH_LIST_CALLS = {"corrected": 1, "tracked": 1, "whole_range": 1}


def _path_list_words(call):
    """The path-listing words `call` names ITSELF, nested calls excluded.

    Excluded because a nested call is its own site. `foo(git(… "ls-tree" …),
    git(… "diff" …))` holds two path lists, and reading the constants of the
    whole subtree would see the outer call once and collapse them -- which is
    round 1's finding again, one level down."""
    words, stack = set(), list(ast.iter_child_nodes(call))
    while stack:
        node = stack.pop()
        if isinstance(node, ast.Call):
            continue
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                words.add(node.value)
            continue
        stack.extend(ast.iter_child_nodes(node))
    return words & LISTS_PATHS


def _derives_a_path_list(tree):
    """`{scope: how many path-listing calls it makes}`.

    Scopes rather than functions, and counts rather than names, because the
    unit of the class is the CALL SITE. A second unfiltered list inside a
    function that already filters one is this defect one LINE over rather than
    one function over, and a set of function names cannot see it; a list built
    at module scope is in no function at all."""
    found = {}

    def visit(node, scope):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit(child, child.name)
                continue
            if isinstance(child, ast.Call) and _path_list_words(child):
                found[scope] = found.get(scope, 0) + 1
            visit(child, scope)

    visit(tree, MODULE_SCOPE)
    return found


def _mentions(tree, function, name):
    """True when `function`'s body names `name` anywhere."""
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function
        ):
            return any(
                isinstance(inner, ast.Name) and inner.id == name
                for inner in ast.walk(node)
            )
    raise AssertionError(f"{function} is no longer a function in this module")


def _callers_of(tree, name):
    """The functions that call `name`."""
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for call in ast.walk(node):
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == name
            ):
                out.add(node.name)
    return out


def test_every_path_list_this_module_derives_from_git_is_filtered_or_named():
    """The reason #365 existed was that a docstring asserted the intent and
    nothing measured it.

    So this case measures it: every function that asks git for a list of
    paths is either filtered by the predicate, filtered by each caller that
    reaches it, or named above with grounds a reader can weigh. Add a fourth and it goes
    red until it is classified -- which is the only thing that stops the same
    defect happening one function over."""
    source = open(SCRIPT, encoding="utf-8").read()
    tree = ast.parse(source)
    derivers = _derives_a_path_list(tree)
    declared = (
        FILTERS_ITS_OWN_LIST | set(FILTERED_BY_ITS_CALLERS) | set(NAMED_EXCEPTION)
    )
    assert set(derivers) == declared, (
        f"the module derives a path list from git in {sorted(derivers)} and "
        f"this case accounts for {sorted(declared)}. Classify the difference "
        f"{sorted(set(derivers) ^ declared)}: it either applies "
        f"`{PREDICATE}`, or it is named here with the grounds for why a round "
        "record belongs in its list"
    )
    assert derivers == PATH_LIST_CALLS, (
        f"the module derives path lists at {derivers} and this case accounts "
        f"for {PATH_LIST_CALLS}. The unit is the CALL SITE: a second list "
        "inside a scope that already holds one is classified nowhere, and the "
        "grounds recorded above are about the call this case counted rather "
        "than about the one just added"
    )
    for name in FILTERS_ITS_OWN_LIST:
        assert _mentions(tree, name, PREDICATE), (
            f"{name} derives a path list and no longer applies `{PREDICATE}`. "
            "A round record quotes the wording a round found, so left in this "
            "list it counts as wording the fix wrote and subtracts the "
            "survivor it quotes -- on exactly the branches that went through "
            "review"
        )
    for name, callers in FILTERED_BY_ITS_CALLERS.items():
        for caller, applies in callers.items():
            assert _mentions(tree, caller, applies), (
                f"{name}'s list is declared filtered by {caller}, and {caller} "
                f"no longer applies `{applies}`"
            )
        assert _callers_of(tree, name) == set(callers), (
            f"{name} is reached from {sorted(_callers_of(tree, name))} and "
            f"only {sorted(callers)} are declared filtering its result, so the "
            "list now leaves this module unfiltered by one of those paths"
        )
    for name, grounds in NAMED_EXCEPTION.items():
        assert not _mentions(tree, name, PREDICATE), (
            f"{name} now applies `{PREDICATE}` and this case still carries "
            "the grounds for why it must not. One of the two is wrong: if the "
            f"filter is right, move {name} into FILTERS_ITS_OWN_LIST and "
            "delete the grounds rather than leaving both standing"
        )
        body = ast.get_source_segment(source, _function(tree, name))
        # Two assertions rather than one conjunction, because they fail for
        # opposite reasons and a single message can only blame one party.
        # `grounds` is a constant in THIS file, so the first is about an edit
        # to the case and the second about an edit to the module.
        assert "foreign" in grounds, (
            f"the grounds recorded here for leaving {name} unfiltered no "
            "longer rest on `foreign`, so this case is about to check the "
            "module against an argument that has been rewritten above it"
        )
        assert "foreign" in body, (
            f"the grounds for leaving {name} unfiltered rest on `foreign` -- "
            "a declaration refused and PRINTED rather than silently dropped. "
            "That mechanism is not in the function any more, so the grounds "
            "are an argument about code that is gone"
        )


def _function(tree, name):
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == name
        ):
            return node
    raise AssertionError(f"{name} is no longer a function in this module")


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
# the design records under `seal/specs/`, `CHANGELOG.md` and the tickets
# themselves. Measured on #293's own range: **153** survivors at 1.60-1.62, every
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


# #304. `OWNER_DIR` read the owner off `seal/specs/<id>/<file>` and stopped one
# segment short, so a `survivors.md` one directory deeper had no owner -- and
# an ownerless declaration is not asked the ownership question at all. It kept
# the unbounded reach the question exists to refuse, in silence, because
# `not yours` prints only when ownership is asked. CI cannot hand it such a
# file (`hygiene.yml` globs one level); a hand run can.
@pytest.mark.parametrize("depth", ["", "deeper/"])
def test_a_declaration_one_directory_deeper_still_has_an_owner(tmp_path, depth):
    """The owner is the `seal/specs/<id>` prefix wherever the file sits
    beneath it, so the deeper file is asked the same question and refused
    the same way -- printed, with the work item named. At the layout position
    nothing changes, which the `""` arm holds."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    where = os.path.join(str(repo), *f"{ITEM_A}/{depth}survivors.md".split("/"))
    os.makedirs(os.path.dirname(where), exist_ok=True)
    with open(where, "w", encoding="utf-8") as handle:
        handle.write(
            f"| Range | Grounds |\n|---|---|\n| `{head}^..{head}` | {GROUNDS} |\n"
        )
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", where
    )
    assert code == 1, (
        "a declaration whose range touches nothing in its own work item "
        f"excused the run, at depth {depth!r}; exit {code}\n{text}"
    )
    assert "notes.md" in text, f"the survivor itself was not reported\n{text}"
    assert "not yours" in text and "1799000001-work-item-a" in text, (
        "the declaration was refused without saying so, or without naming the "
        f"work item it belongs to, at depth {depth!r}:\n{text}"
    )
    assert "this range touches nothing in it" in text, (
        f"a shared-mode refusal no longer names the diff test as its reason:\n{text}"
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


UNRESOLVED_ROW = (
    f"| Range | Grounds |\n|---|---|\n| `origin/gone..HEAD` | {GROUNDS} |\n"
)


def test_an_unresolved_declaration_of_another_work_item_prints_nothing(tmp_path):
    """S13 (#439). A shipped work item's `survivors.md` names a release
    branch that was deleted at the release, and every later run was handed
    it and printed `unresolved` for a declaration that could never have
    applied to it -- three lines on every seal of one release. The second
    anchor is asked first: this range touches nothing in that work item's
    directory, so the row could not have excused this run whether or not it
    resolved, and the line is addressed to nobody. The exit is the case
    above's, because an unresolved row excuses nothing either way."""
    repo = tmp_path / "probe"
    head = one_survivor(repo)
    where = os.path.join(str(repo), *f"{ITEM_A}/survivors.md".split("/"))
    os.makedirs(os.path.dirname(where), exist_ok=True)
    with open(where, "w", encoding="utf-8") as handle:
        handle.write(UNRESOLVED_ROW)
    code, text = run(
        "--range", f"{head}^..{head}", "--root", str(repo), "--exempt", where
    )
    assert code == 1, f"an unresolvable declaration silenced the run\n{text}"
    assert "notes.md" in text, f"the survivor itself was not reported\n{text}"
    assert "unresolved" not in text and "origin/gone..HEAD" not in text, (
        "a declaration belonging to a work item this range touches nothing of "
        f"was printed to this run, which could never have used it:\n{text}"
    )


def test_an_unresolved_declaration_of_the_work_item_the_range_touches_prints(
    tmp_path,
):
    """S14, the half that must not move. The same row under a work item this
    range does touch is a declaration this run could have used, and a row
    that quietly stopped applying is the one failure a rotting anchor must
    not have -- so it prints, as it did before #439."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst. {CLAIM_A}\n\nSecond. {CLAIM_A}\n",
            "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        },
        "the claim, stated twice",
    )
    fixed = (
        "The verdict cell is written by the generator and the "
        "orchestrator leaves it untouched afterwards."
    )
    head = build(
        repo,
        {
            "notes.md": f"# notes\n\nFirst. {fixed}\n\nSecond. {CLAIM_A}\n",
            f"{ITEM_A}/routing.md": "# routing\n\nDeclared before the first edit.\n",
            f"{ITEM_A}/survivors.md": UNRESOLVED_ROW,
        },
        "work item A corrects its claim and declares a range that is gone",
    )
    code, text = run(
        "--range",
        f"{head}^..{head}",
        "--root",
        str(repo),
        "--exempt",
        os.path.join(str(repo), *f"{ITEM_A}/survivors.md".split("/")),
    )
    assert code == 1, f"an unresolvable declaration silenced the run\n{text}"
    assert "unresolved" in text and "origin/gone..HEAD" in text, (
        "the work item's own unresolved declaration was not printed to its "
        f"own run, so the row rotted in silence:\n{text}"
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


def test_the_reason_no_round_can_run_it_survives_the_rewrite_of_s2():
    """#120 rewrote §2, and this paragraph's grounds were a quotation of it.

    It read *§2 reserves the broad gate for you*, addressed to the
    orchestrator. §2 no longer reserves anything for the orchestrator -- it
    makes the gate one act and leaves each definition to say whether it is its
    agent's -- so the sentence had to be re-derived rather than re-pointed.
    The conclusion is unchanged and it is what this case holds: the reviewer
    is the one party structurally unable to see what its own fix pass leaves
    behind, which is why the step belongs to the fix pass.

    Pinned because a reason nothing checks is the first thing a later edit
    drops, and what is left then is a step with a rule number beside it and no
    argument -- which is the shape somebody deletes."""
    skill = " ".join(read("skills", "code-review", "orchestration.md").split())
    assert "no reviewer's does" in skill, (
        "the grounds for `No round can run it` went. Without them the step "
        "reads as a preference about who types the command"
    )
    assert "structurally unable" in skill, (
        "the paragraph stopped saying that a round CANNOT see this rather "
        "than that it is not asked to, which is the whole of the argument"
    )
    assert "§2 reserves the broad gate for you" not in skill, (
        "the pre-#120 quotation is back, and §2 does not say it any more"
    )


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


# --- #517: a retired directory is out of the range, either arm -------------

RETIRED_SPEC_SENTENCE = (
    "The quarterly ferry manifest is reconciled by the harbour clerk before "
    "any cargo leaves the eastern pier."
)
RETIRED_MOMENT_SENTENCE = (
    "The lighthouse keeper logs every lantern trim in the brass ledger kept "
    "beside the spiral stair."
)
# What the fold wrote into `docs/`: the same fact restated, one word
# changed. A verbatim copy is ONE shared run, and a run scores at most 1.0, so
# it could never reach the floor; a restatement shares two runs, which is what
# the 153 survivors #293's range reported were.
STANDING_SPEC = RETIRED_SPEC_SENTENCE.replace("harbour", "night")
STANDING_MOMENT = RETIRED_MOMENT_SENTENCE.replace("brass", "copper")
CLOSED_MEMO = (
    "# a moment\n\n## Not verified\n\n| Item | Who must answer |\n|---|---|\n"
    "| ✅ a claim | run on 2026-01-01 |\n"
)
MARKED = "seal/specs/1700000001-a-folded-item"
MOMENT = "seal/specs/1700000002-a-release-entry"
# A pool large enough that a phrase unique to one file scores as one: the
# score is scaled by `log2` of the pool, so two files cannot report anything.
FILLER = {
    f"filler/{n}.md": f"# filler {n}\n\nUnrelated prose number {n} shares nothing.\n"
    for n in range(12)
}


def retired_range(repo, also=None):
    """Two directories retired in one range — one by its marker, one by the
    rule — with their sentences standing in `docs/`, where a fold puts them.
    `also` is a further change to `docs/` in the same range."""
    build(
        repo,
        {
            "docs/policy.md": (f"# policy\n\n{STANDING_SPEC}\n\n{STANDING_MOMENT}\n"),
            "docs/guide.md": f"# guide\n\nFirst statement. {FOUND}\n",
            "docs/notes.md": f"# notes\n\nSecond statement. {FOUND}\n",
            f"{MARKED}/spec.md": f"# spec\n\n{RETIRED_SPEC_SENTENCE}\n",
            f"{MOMENT}/routing.md": f"# routing\n\n{RETIRED_MOMENT_SENTENCE}\n",
            f"{MOMENT}/overview.md": CLOSED_MEMO,
            **FILLER,
        },
        "two work items, released",
    )
    shutil.rmtree(os.path.join(repo, *MARKED.split("/")))
    shutil.rmtree(os.path.join(repo, *MOMENT.split("/")))
    # The marker in a document of its own, so `docs/policy.md` is untouched
    # and its sentences are neither removed nor written by this range.
    files = {
        "docs/a-segment.md": (
            f"# a segment\n\n<!-- specs/{os.path.basename(MARKED)} -->\n"
            "The standing statement.\n"
        )
    }
    files.update(also or {})
    return build(repo, files, "fold one, retire the other by the rule")


def test_a_retired_directory_is_not_corrected_wording(tmp_path):
    """A8. A fold removes a directory whose sentences stand in `docs/` by
    design, and the sweep reported every one of them — which is why a fold
    owed a `survivors.md` range-row, and under #517's D1 a fold has no work
    item directory to hold one. Left out of the range on both sides, the way
    a round record already is."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    head = retired_range(repo)
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, f"a retirement's standing sentences were reported:\n{text}"
    assert "docs/policy.md" not in text.split("examined")[-1], text


def test_a_sentence_the_same_range_removes_from_docs_is_still_measured(tmp_path):
    """The exclusion is the retired directories and nothing else: a range
    that retires them and also corrects `docs/` is still read for what it
    left standing there."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    head = retired_range(
        repo, also={"docs/guide.md": f"# guide\n\nFirst statement. {REPAIRED}\n"}
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, text
    assert "docs/notes.md" in text, text


def test_a_verbatim_fold_hides_no_correction_the_same_range_made(tmp_path):
    """S4 (#591). A range retires a directory whose `spec.md` states FOUND,
    folds FOUND verbatim into `docs/b.md`, and corrects FOUND in `docs/a.md`.
    Dropped before the pairing, the retired side left the fold's arrival to
    pair with the correction, and the correction was held rather than
    removed. The retired side now takes part in the pairing and leaves the
    range after it, so the fold's text is held and the correction is the
    source. Red at 4665def0: exit 0, `against 0 sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            f"{MARKED}/spec.md": f"# spec\n\n{FOUND}\n",
            **FILLER,
            **MORE_FILLER,
        },
        "the claim, and a work item stating it",
    )
    shutil.rmtree(os.path.join(repo, *MARKED.split("/")))
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "docs/a-segment.md": (
                f"# a segment\n\n<!-- specs/{os.path.basename(MARKED)} -->\n"
                "The standing statement.\n"
            ),
            "docs/b.md": f"# b\n\n{FOUND}\n",
        },
        "fold the work item verbatim into b.md, and correct a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the fold's verbatim text was written as the range's own and held the "
        f"correction; exit {code}\n{text}"
    )
    assert coordinates_in(text) == {"docs/b.md:3"}, text
    assert set(corrected_lines(text)) == {"docs/a.md:3"}, text
    assert re.search(r"against 1 sentence\(s\)", text), (
        f"the retired spec's sentences are still counted as removed:\n{text}"
    )


def test_a_spec_less_directory_with_an_open_row_stays_in_the_range(tmp_path):
    """The rule arm's condition, asked of the range's left end through the
    one predicate: a directory whose record held an open row was not retired
    by the rule, and its sentences are corrected wording like any other."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/policy.md": f"# policy\n\n{STANDING_MOMENT}\n",
            f"{MOMENT}/routing.md": f"# routing\n\n{RETIRED_MOMENT_SENTENCE}\n",
            f"{MOMENT}/overview.md": CLOSED_MEMO.replace("✅ a claim", "a claim"),
            **FILLER,
        },
        "a moment with an open row",
    )
    shutil.rmtree(os.path.join(repo, *MOMENT.split("/")))
    head = build(repo, {"filler/0.md": "# filler\n\nStill unrelated.\n"}, "removed")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, text
    assert "docs/policy.md" in text, text


def test_a_specs_directory_outside_the_seal_root_stays_in_the_range(tmp_path):
    """Round 1's finding 4. A work item lives under `seal/specs/` or the
    pre-0.4.0 top-level `specs/`, never under `docs/specs/`: a directory of
    design notes deleted whole there holds no `spec.md` and nothing open, so
    an unanchored pattern read it as retired by the rule and the sweep
    measured none of its sentences."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    notes = "docs/specs/login-flow"
    build(
        repo,
        {
            "docs/policy.md": f"# policy\n\n{STANDING_MOMENT}\n",
            f"{notes}/design.md": f"# design\n\n{RETIRED_MOMENT_SENTENCE}\n",
            **FILLER,
        },
        "design notes under docs/specs",
    )
    shutil.rmtree(os.path.join(repo, *notes.split("/")))
    head = build(repo, {"filler/0.md": "# filler\n\nStill unrelated.\n"}, "removed")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, text
    assert "docs/policy.md" in text, text


def test_a_spec_less_directory_that_stays_is_still_in_the_range(tmp_path):
    """A retirement removes the directory: one still present at the range's
    right end was edited, not retired, and what the edit removed is measured
    like any other correction."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/policy.md": f"# policy\n\n{STANDING_MOMENT}\n",
            f"{MOMENT}/routing.md": f"# routing\n\n{RETIRED_MOMENT_SENTENCE}\n",
            f"{MOMENT}/overview.md": CLOSED_MEMO,
            **FILLER,
        },
        "a moment, nothing open",
    )
    head = build(
        repo, {f"{MOMENT}/routing.md": "# routing\n\nReworded entirely.\n"}, "edited"
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, text
    assert "docs/policy.md" in text, text


# --- #543: a Python file's prose is its comments, docstrings and literals ---
#
# A line of code normalises to the same words in every file that walks a list
# the same way, so a branch that rewrote one loop was told that every other
# loop of that shape still stood: four of one branch's five exemption rows,
# and the fourth arrived from another work item's merge as a red hygiene job.
# The fix is a narrower reading of what a `.py` file SAYS, never a file kind
# skipped -- #269's pin is a string literal in a test, and the real survivor
# on the 0.15.0 release's fourth range is a `#` comment.


def coordinates_in(text):
    """The `path:line` coordinates a report names, one per reported survivor."""
    return {
        line.strip()
        for line in text.splitlines()
        if line and not line.startswith((" ", "survivor-check")) and ":" in line
    }


# Two generic line-list walks, shaped after `round_record.py`'s removed
# `section_body` scan and the four carriers #543 names. They share three
# stretches of code tokens -- `end next i for i in range`, `len lines if
# lines i` and `startswith len lines` -- and no sentence.
WALK = (
    "def section_body(lines, heading):\n"
    '    """The lines of one section."""\n'
    "    starts = sections(lines, heading)\n"
    "    start = starts[0]\n"
    "    end = next(\n"
    '        (i for i in range(start + 1, len(lines)) if lines[i].startswith("#")),\n'
    "        len(lines),\n"
    "    )\n"
    "    return lines[start:end]\n"
)
OTHER_WALK = (
    "def table_lines(lines, header_idx):\n"
    '    """The rows of one table."""\n'
    "    end = next(\n"
    "        (i for i in range(header_idx + 1, len(lines))"
    ' if lines[i].strip().startswith("## ")),\n'
    "        len(lines),\n"
    "    )\n"
    "    return lines[header_idx + 1 : end]\n"
)
REWRITTEN_WALK = (
    "def section_body(lines, heading):\n"
    '    """The lines of one section."""\n'
    "    starts = sections(lines, heading)\n"
    "    start = starts[0]\n"
    "    end = start + 1\n"
    '    while end < len(lines) and not lines[end].startswith("#"):\n'
    "        end += 1\n"
    "    return lines[start:end]\n"
)


def test_a_loop_rewritten_in_one_file_is_not_reported_at_every_other_loop(
    tmp_path,
):
    """S1. Two modules walk a list the same way; the range rewrites one.

    Under the whole-file reading the other module's loop shares three runs
    of code tokens with the removed one and scores over the floor -- which
    is the report #543 quotes at 2.77. A loop is not wording, so the range
    is clean."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(repo, {"walker.py": WALK, "other.py": OTHER_WALK, **FILLER}, "two walks")
    head = build(repo, {"walker.py": REWRITTEN_WALK}, "rewrote one of them")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "the other module's loop was reported as wording this range removed; "
        f"a line of code is not a sentence. exit {code}\n{text}"
    )
    assert "other.py" not in text.split("examined", 1)[-1], text


# A claim stated in a docstring, and the same claim carried by a comment or by
# another docstring one file over. Both are what a `.py` file SAYS, so a
# correction to the first has to be reported at the second.
CARRIERS_OF_PROSE = {
    "comment": f"# {FOUND}\n\n\ndef reader():\n    return None\n",
    "docstring": f'def reader():\n    """{FOUND}"""\n    return None\n',
}


@pytest.mark.parametrize("carrier", sorted(CARRIERS_OF_PROSE))
def test_a_docstring_corrected_in_one_file_is_reported_where_prose_carries_it(
    tmp_path, carrier
):
    """S2. The direction that would break if the reader took too much.

    A docstring is exactly where a removed rule survives, and the real
    survivor on one of the four measured ranges is a `#` comment. Skipping
    `.py` files would lose both; this case is green before the reader and
    has to stay green after it."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "stated.py": f'def writer():\n    """{FOUND}"""\n    return None\n',
            "carrier.py": CARRIERS_OF_PROSE[carrier],
            **FILLER,
        },
        "the claim in a docstring, and once more in another module",
    )
    head = build(
        repo,
        {"stated.py": f'def writer():\n    """{REPAIRED}"""\n    return None\n'},
        "corrected the docstring only",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        f"carrier.py still carries the claim in a {carrier}, and the range was "
        f"called clean; exit {code}\n{text}"
    )
    assert "carrier.py" in text, f"the report does not name the {carrier}:\n{text}"


def test_a_code_token_between_two_literals_ends_the_sentence():
    """S4. `"first half", name, "second half"` is two sentences.

    Under the whole-file reading the line normalises to `first half name
    second half`, one sentence carrying both halves. A code token between
    two literals is where the sentence ends; two literals with only a line
    break between them -- Python's implicit concatenation, #269's pin --
    are still one, and the case above this section holds that side."""
    reader = module()
    keys = [
        s.key for s in reader.sentences("probe.py", '"first half", name, "second half"')
    ]
    assert not any("first half" in k and "second half" in k for k in keys), (
        f"the two literals read as one sentence across a code token: {keys!r}"
    )
    assert any("first half" in k for k in keys) and any(
        "second half" in k for k in keys
    ), f"a literal was lost rather than separated: {keys!r}"


def test_an_fstring_expression_ends_the_sentence_and_its_quotes_do_not():
    """On 3.12 an f-string is FSTRING_START, FSTRING_MIDDLE and FSTRING_END
    with its expressions as ordinary tokens. The expression is code, so it
    ends the sentence; the quotes are the literal's delimiters, so a plain
    string beside them is implicitly concatenated and reads as one."""
    reader = module()
    keys = [
        s.key
        for s in reader.sentences("probe.py", 'x = f"hello {name} world" "and more"\n')
    ]
    assert any("world and more" in k for k in keys), (
        f"the f-string's closing quote ended the sentence before `and more`: {keys!r}"
    )
    assert not any("hello" in k and "world" in k for k in keys), (
        f"the expression between `hello` and `world` did not end the sentence: {keys!r}"
    )


def test_a_file_the_tokenizer_refuses_is_read_whole_as_before(tmp_path):
    """S5. An unterminated triple-quoted string is a file the tokenizer
    cannot read, and the fallback is today's whole-file reading -- the
    direction that reports more, which is the one a checker of claims may
    fail in. The claim stands twice in the file, once as a comment and once
    inside the unterminated string; the range corrects the comment, and the
    second copy is reported as it is today."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    unterminated = f'x = 1\n# {FOUND}\n\n\ndef f():\n    """{FOUND}\n'
    build(repo, {"bad.py": unterminated, **FILLER}, "a file python cannot parse")
    head = build(
        repo,
        {"bad.py": unterminated.replace(f"# {FOUND}", f"# {REPAIRED}")},
        "corrected the comment only",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the unterminated file's second copy of the claim went unreported, so "
        f"the tokenizer's refusal read as a file with no sentences; exit {code}\n{text}"
    )
    assert "bad.py" in text, text
    assert "Traceback" not in text, text


# S6: the four squash commits of the 0.15.0 release as they stand on `main`,
# each over its own range -- exactly the range its pull request was checked
# over -- and what each reports once code is not wording. Every coordinate
# below is prose; the six places the whole-file reading named beside them
# were function bodies matched on loop, assignment and `if` shapes, and
# `spec.md` §*The measured state* holds the table they came from. The
# commits are reachable from `main` and from `release/v0.15.1` in every
# clone, and the case skips rather than fails when one is gone, in the
# pattern of the two fixture tags above.
RELEASE_RANGES = {
    # 0 · #537: `chain_check.py:2960`, one function body against another's, gone
    "576fe39d": {
        "docs/review-chain-spec.md:1418",
        "skills/code-review/scripts/chain_check.py:2374",
        "seal/ledger.md:820",
        "skills/code-review/scripts/chain_check.py:2370",
    },
    # C · #538: `fold_ledger.py:358`, a `main` body against the gatherer's,
    # gone; then `CHANGELOG.md:2252`, a released entry, gone too
    "cc49ae64": set(),
    # B · #539: no code idiom in the POOL on this range, and one in the range
    # itself. The whole-file reading named `seal/ledger.md:2053` at 2.47
    # against a "sentence" that was a test's docstring and three of its
    # assert messages joined by the code between them; read one literal per
    # sentence, the best of those sources shares one run at 1.00, under the
    # floor. Then `CHANGELOG.md:2090`, a released entry, gone -- and with
    # nine gathered fragments out of the pool the weight of every phrase
    # they held rose, and `survivor_check.py:142` (the module's own *quote
    # is the anchor* sentence) crossed the floor at 1.61 against the
    # `seal/follow-up.md` row the range deleted. The weighting moving, as
    # `plan.md` §*Operational impact* says it can; seven stand and one joins.
    "3dd24073": {
        "skills/code-review/scripts/survivor_check.py:142",
        "seal/follow-up.md:65",
        "tests/test_chain_check_at_the_pull_request.py:1506",
        "seal/follow-up.md:80",
        "seal/follow-up.md:81",
        "skills/verify/scripts/broad_gate.py:549",
        "seal/follow-up.md:59",
        "seal/follow-up.md:82",
    },
    # A · #541: the four #543 names gone; the one real survivor, a ledger row
    # carrying a `#` comment the range removed, stays
    "d2f2c0dc": {"seal/ledger.md:2041"},
}


@pytest.mark.parametrize("commit", sorted(RELEASE_RANGES))
def test_the_four_real_ranges_report_their_prose_and_none_of_their_code(commit):
    """S6. The measured state, pinned coordinate for coordinate.

    A set rather than a count, because dropping code carriers raises the
    weight of every phrase they held and a prose coordinate that moves is
    the weighting moving -- which this case exists to see rather than
    assume."""
    if not resolves(commit):
        pytest.skip(f"{commit} is not in this clone")
    code, text = over(commit)
    expected = RELEASE_RANGES[commit]
    assert coordinates_in(text) == expected, (
        f"over {commit}^..{commit} the report names "
        f"{sorted(coordinates_in(text))} where the measured prose is "
        f"{sorted(expected)}:\n{text}"
    )
    assert code == (1 if expected else 0), f"exit {code}\n{text}"


def test_the_docstring_states_what_a_sentence_is_in_a_python_file():
    """`agent-contract` §14 -- the rule that changed the verdict is stated
    where a reader looks for the module's account of itself."""
    source = open(SCRIPT, encoding="utf-8").read()
    heading = "## What a sentence is in a Python file"
    assert heading in source, "the module docstring does not state the rule"
    section = source[source.index(heading) + len(heading) :]
    section = " ".join(section[: section.index("\n## ")].split())
    for word in ("comment", "docstring", "string literal", "code"):
        assert word in section, f"the section does not mention {word!r}:\n{section}"


# --- #307: a released changelog section and a gathered fragment are records --
#
# A released section records what a past release did, in that release's
# words, and a released entry is not rewritten (`CLAUDE.md` §*Repo rule — a
# change writes fragments, never the shared file*). So the branch that changes
# the behaviour it describes was reported against it and could correct
# nothing; two of the four measured ranges carried exactly that report. The
# region is read off the HEADING rather than the file whole, because a
# repository following `agents/smith.md`'s *let the entry accumulate
# unreleased* keeps live prose under `## Unreleased` in the same file. A
# fragment counts as gathered when its `<!-- specs/<id> -->` marker stands in
# `CHANGELOG.md` at the range's tip, which is the rule the gatherer pins.

RELEASED_HEADINGS = ("## 1.0.0 — 2026-01-01", "## [1.2.0] - 2026-01-01", "## v1.2.0")
SHIPPED = "seal/specs/1700000003-a-shipped-item"
FRAGMENT = f"{SHIPPED}/changelog.md"


def changelog(heading, body, marker=None):
    mark = f"<!-- specs/{os.path.basename(SHIPPED)} -->\n" if marker else ""
    return f"# Changelog\n\n{heading}\n{mark}\n### Fixed\n\n- {body}\n"


@pytest.mark.parametrize("heading", RELEASED_HEADINGS)
def test_a_released_changelog_section_is_not_a_carrier(tmp_path, heading):
    """S7. The claim corrected in `docs/a.md` stands under a version heading
    of `CHANGELOG.md`, and the range is clean: that section is the record of
    a release, and nobody may correct it."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": changelog(heading, FOUND),
            **FILLER,
        },
        "the claim, and the release that recorded it",
    )
    head = build(repo, {"docs/a.md": f"# a\n\n{REPAIRED}\n"}, "corrected docs/a.md")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        f"a released changelog section under {heading!r} was reported as a "
        f"survivor; a released entry is not rewritten. exit {code}\n{text}"
    )
    assert "CHANGELOG.md" not in text.split("examined", 1)[-1], text


def test_an_unreleased_changelog_section_is_a_carrier(tmp_path):
    """S8. The same sentence under `## Unreleased` is this release's own
    prose, and it is reported. Green before and after: the half that must
    not move."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": changelog("## Unreleased", FOUND),
            **FILLER,
        },
        "the claim, and an unreleased entry carrying it",
    )
    head = build(repo, {"docs/a.md": f"# a\n\n{REPAIRED}\n"}, "corrected docs/a.md")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"the unreleased entry went unreported; exit {code}\n{text}"
    assert "CHANGELOG.md" in text, text


def test_a_range_that_edits_only_a_released_section_removes_no_sentence(tmp_path):
    """S9. The source side. A line changed under `## 1.0.0` is not a
    correction anybody has to chase into `docs/`, and the count of removed
    sentences says so."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], FOUND),
            **FILLER,
        },
        "the claim, and the release that recorded it",
    )
    head = build(
        repo,
        {"CHANGELOG.md": changelog(RELEASED_HEADINGS[0], REPAIRED)},
        "reflowed a released entry and nothing else",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "a range that touched only a released section was read as a "
        f"correction somebody has to chase into docs/a.md; exit {code}\n{text}"
    )
    assert re.search(r"against 0 sentence\(s\)", text), (
        f"wording removed from a released section still counts as removed:\n{text}"
    )


def test_a_release_that_moves_the_unreleased_section_under_a_version_removes_nothing(
    tmp_path,
):
    """Round 1's 🟡 1. The release commit of a repository that lets the entry
    accumulate unreleased: `## Unreleased` takes a version heading and
    nothing else changes. The section is live at `a` and blanked at `b`, so
    without the held-count every sentence of it reads as removed and the
    document restating an entry is reported at the release with nothing
    anybody may correct. Two disjoint runs in the restatement, because one
    run scores 1.00 and never clears the floor."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    restated = FOUND.replace("itself and the", "itself and, from then on, the")
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{restated}\n",
            "CHANGELOG.md": changelog("## Unreleased", FOUND),
            **FILLER,
        },
        "the entry under Unreleased, and a document restating it",
    )
    head = build(
        repo,
        {"CHANGELOG.md": changelog(RELEASED_HEADINGS[0], FOUND)},
        "release 1.0.0: the unreleased section takes a version heading",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "a release that only moved the unreleased section under a version "
        f"heading was read as a correction to chase into docs/a.md; exit {code}\n{text}"
    )
    assert "docs/a.md" not in text.split("examined", 1)[-1], text


def two_sections(unreleased, older):
    return (
        f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {unreleased}\n\n"
        f"## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- {older}\n"
    )


def test_a_release_that_rewords_an_entry_still_reports_its_verbatim_copy(tmp_path):
    """Round 2's 🟡 1. The release rewords the entry as it moves it under a
    version heading, and a document quotes the old wording verbatim. The new
    wording has to reach `written`, or the removed sentence is one run at
    1.00 and never clears the floor. Red at 1f8cdcda: exit 0, `against 2
    sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": changelog("## Unreleased", FOUND),
            **FILLER,
        },
        "the entry under Unreleased, and a document quoting it verbatim",
    )
    head = build(
        repo,
        {"CHANGELOG.md": changelog(RELEASED_HEADINGS[0], REPAIRED)},
        "release 1.0.0, rewording the entry as it is released",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the release reworded the entry and docs/a.md still quotes the old "
        f"wording verbatim; exit {code}\n{text}"
    )
    assert "docs/a.md" in text, text


def test_a_sentence_in_an_older_release_does_not_hold_the_unreleased_one(tmp_path):
    """Round 2's 🟡 2. Only what the range put under a version heading is
    held. A sentence that also stands in an older release must not keep its
    unreleased copy from counting as removed. Red at 1f8cdcda: exit 0,
    `against 0 sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": two_sections(FOUND, FOUND),
            **FILLER,
        },
        "an unreleased entry repeating an older release's sentence",
    )
    head = build(
        repo,
        {"CHANGELOG.md": two_sections(REPAIRED, FOUND)},
        "reword the unreleased entry; no release",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the unreleased entry was reworded and its copy in docs/a.md went "
        f"unreported because 0.9.0 carries the same sentence; exit {code}\n{text}"
    )
    assert "docs/a.md" in text, text


def test_a_release_that_renames_unreleased_and_gathers_still_reports(tmp_path):
    """Round 3's 🟡 1. The release renames `## Unreleased` to a version and
    gathers a fragment into the same section, and the same commit corrects
    `docs/a.md`. The renamed heading is a lost sentence, so the moved
    section's fresh wording is written -- and the gathered fragment's text,
    which quotes the old wording, must not be written with it, or it
    subtracts the survivor standing in `docs/b.md`. The fragment stays, as
    the gatherer leaves it. Red at 0c335744: exit 0, `against 2
    sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    entry = "The frobnicator now rejects a negative width with a plain message."
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {entry}\n\n{older}"
            ),
            **FILLER,
        },
        "an unreleased entry, a fragment quoting the claim, two documents",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(
                RELEASED_HEADINGS[0], f"{FOUND}\n\n- {entry}", marker=True
            )
            + f"\n{older}",
        },
        "release 1.0.0: rename Unreleased, gather the fragment, correct docs/a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered fragment's text was written back with the renamed "
        f"section and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text


def test_a_release_that_gathers_and_deletes_the_fragment_still_reports(tmp_path):
    """H1. The release above, by a gatherer that deletes the fragment it
    gathered. Nothing of the fragment stands at the range's tip, so the text
    to hold is read where it still stands, at the range's left end. Read at
    the tip instead, the held set is empty, the gathered wording is written
    and the survivor in `docs/b.md` is subtracted: exit 0. Red at 61f0d0d8
    (exit 0, `against 2 sentence(s)`), and red under that mutation."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    entry = "The frobnicator now rejects a negative width with a plain message."
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {entry}\n\n{older}"
            ),
            **FILLER,
        },
        "an unreleased entry, a fragment quoting the claim, two documents",
    )
    os.remove(repo / FRAGMENT)
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(
                RELEASED_HEADINGS[0], f"{FOUND}\n\n- {entry}", marker=True
            )
            + f"\n{older}",
        },
        "release 1.0.0: rename Unreleased, gather and delete the fragment",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the deleted fragment's gathered text was written back with the "
        f"renamed section and subtracted the survivor in docs/b.md; exit {code}\n"
        f"{text}"
    )
    assert "docs/b.md" in text, text


def test_a_release_that_rewords_an_entry_and_gathers_still_reports(tmp_path):
    """H2k. `## Unreleased` stays, its entry is reworded as it is released
    under a new version heading, and a fragment is gathered into the same
    section and left in place. The reworded entry is a lost sentence, so the
    released wording is written, as round 2's reworded-release case needs --
    all of it but the gathered fragment's, which quotes the wording the same
    commit corrected in `docs/a.md`. Red at 61f0d0d8: exit 0, `against 2
    sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    entry = "The frobnicator now rejects a negative width with a plain message."
    reworded = "The frobnicator now refuses a negative width and names the flag."
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    marker = f"<!-- specs/{os.path.basename(SHIPPED)} -->"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {entry}\n\n{older}"
            ),
            **FILLER,
        },
        "an unreleased entry, a fragment quoting the claim, two documents",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n{RELEASED_HEADINGS[0]}\n{marker}\n\n"
                f"### Fixed\n\n- {FOUND}\n\n- {reworded}\n\n{older}"
            ),
        },
        "release 1.0.0: keep Unreleased, reword its entry, gather the fragment",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered fragment's text was written back with the reworded "
        f"release and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text


GATHERER = os.path.join(ROOT, ".github", "scripts", "gather_changelog.py")


def gathered_section(version, date, entries):
    """The released section exactly as the gatherer lays it down: its own
    `section`, loaded by path, so the layout follows the gatherer if it ever
    changes. A test may depend on this repository's release automation; the
    shipped script may not, which is why the sweep spells `MARKER` itself."""
    spec = importlib.util.spec_from_file_location("specseal_gatherer", GATHERER)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded.section(version, date, entries)


def test_a_gathered_fragment_that_opens_with_prose_is_still_held(tmp_path):
    """G4, `agent-contract` §12's member of the class above. The gatherer
    writes the marker line and the fragment's body directly under it, with no
    blank line between, and a marker line starts no block. So a fragment
    whose first line is prose has its first sentence joined to the marker's
    words, a key that matches nothing in the fragment, and that one sentence
    escapes the held set. Every fragment in this tree opens with `###` or
    `- `, which starts a block, and no template fixes the shape. Red with
    the gathered text held and the marker read as prose: exit 0, `against 2
    sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    entry = "The frobnicator now rejects a negative width with a plain message."
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    body = f"{FOUND} A second sentence says what else changed.\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: body,
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {entry}\n\n{older}"
            ),
            **FILLER,
        },
        "an unreleased entry, a prose fragment quoting the claim, two documents",
    )
    released = gathered_section(
        "1.0.0", "2026-01-01", [(os.path.basename(SHIPPED), body.strip())]
    )
    assert f"-->\n{FOUND}" in released, (
        f"the gatherer no longer writes the body directly under the marker:\n{released}"
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n{released}\n### Fixed\n\n- {entry}\n\n{older}"
            ),
        },
        "release 1.0.0: rename Unreleased, gather a prose fragment, correct docs/a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the prose fragment's first sentence, joined to its marker line, was "
        f"written back and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text


def test_a_release_that_writes_its_entry_directly_and_loses_nothing_reports(
    tmp_path,
):
    """#555's pin, the `lost` guard alone. The release writes a new version
    section whose entry quotes the claim, with no marker and no fragment,
    and `CHANGELOG.md` loses no sentence; the same commit corrects
    `docs/a.md`. Nothing of the file was removed, so there is nothing the
    released wording could split, and it is not written. The fragment
    filter cannot protect this shape -- nothing here was gathered -- so the
    guard is the only thing between the entry's wording and the survivor in
    `docs/b.md`. Red with the guard replaced by `if False:` and the filter
    in place: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            "CHANGELOG.md": f"# Changelog\n\n{older}",
            **FILLER,
        },
        "an older release and two documents carrying the claim",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], FOUND) + f"\n{older}",
        },
        "release 1.0.0: an entry written in place, and docs/a.md corrected",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "a release that lost no sentence wrote its entry's wording back and "
        f"subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text


def test_a_gathered_release_that_loses_nothing_reports(tmp_path):
    """#555's own shape (P6), and the pair's pin. The release gathers a
    fragment quoting the claim under a new version heading, `CHANGELOG.md`
    loses no sentence, and the same commit corrects `docs/a.md`. Two things
    each keep the gathered text out of `written` here: the `lost` guard,
    because the file lost nothing, and the fragment filter, because the text
    is gathered. So this case goes red only with both removed (exit 0), and
    stays green with either one removed alone -- which is why the guard's
    own pin is the case above and the filter's are the gathered releases
    that lose a sentence."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": f"# Changelog\n\n{older}",
            **FILLER,
        },
        "an older release, a fragment quoting the claim, two documents",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], FOUND, marker=True)
            + f"\n{older}",
        },
        "release 1.0.0: gather the fragment, correct docs/a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "a gathered release that lost no sentence wrote the gathered text "
        f"back and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text


def test_a_release_that_replaces_an_entry_with_a_gathered_rewording_reports(
    tmp_path,
):
    """The gathered-text filter's other side (round 1's 🟡 1). The release
    replaces the live entry `FOUND` with a gathered fragment whose text
    rewords it, and `docs/b.md` quotes `FOUND`. The fragment's rewording is
    withheld from `written`, but it must still split the sentence
    `CHANGELOG.md` itself lost into the runs it no longer shares, as a
    reworded release does; withheld whole, `FOUND` is one run under the
    floor and its copy goes silent. Red at bf7ba905: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": "# a\n\nUnrelated.\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {REPAIRED}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {FOUND}\n\n{older}"
            ),
            **FILLER,
        },
        "a live entry, a fragment rewording it, a document quoting the entry",
    )
    head = build(
        repo,
        {
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], REPAIRED, marker=True)
            + f"\n{older}",
        },
        "release: the live entry replaced by the gathered rewording",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered rewording was withheld whole, so the lost entry never "
        f"split and its copy in docs/b.md went silent; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text


def test_a_gathered_fragment_cannot_subtract_a_survivor_through_a_lost_entry(
    tmp_path,
):
    """Round 2's 🟡 1. The release rewords a live entry that quotes the claim,
    gathers a fragment quoting it verbatim, and corrects `docs/a.md`. What the
    fragment shares with the lost entry splits that entry and nothing else:
    written for every file, it subtracts the claim from `docs/a.md`'s
    corrected sentence too, and the survivor in `docs/b.md` goes silent. The
    same release without the fragment reports. Red at e6c85df6: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    quoting = f"The docs no longer say that {FOUND[0].lower()}{FOUND[1:]}"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {quoting}\n\n{older}"
            ),
            **FILLER,
        },
        "a live entry quoting the claim, a fragment quoting it, two documents",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(
                RELEASED_HEADINGS[0],
                f"{FOUND}\n\n- The docs now name the generator as its writer.",
                marker=True,
            )
            + f"\n{older}",
        },
        "release 1.0.0: reword the entry, gather the fragment, correct docs/a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered text shared with the lost entry was written for every "
        f"file and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text


def test_a_gathered_fragment_standing_in_the_pool_is_not_a_survivor(tmp_path):
    """S10, the pool side. The fragment's marker is in `CHANGELOG.md` at the
    tip, so the fragment is the released entry one file over and is not
    reported.

    The released section itself carries an unrelated entry here, on
    purpose: with the same sentence in both, the two carriers halve each
    other's weight and the fragment falls under the floor unreported, and
    this case was green against the unchanged reader for that reason alone."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": changelog(
                RELEASED_HEADINGS[0], "An unrelated entry.", marker=True
            ),
            **FILLER,
        },
        "the claim, its fragment, and the release that gathered it",
    )
    head = build(repo, {"docs/a.md": f"# a\n\n{REPAIRED}\n"}, "corrected docs/a.md")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        f"a gathered fragment was reported as a survivor; exit {code}\n{text}"
    )
    assert FRAGMENT not in text, text


def test_a_gathered_fragment_the_range_edited_is_not_a_source(tmp_path):
    """S10, the range side. A sentence removed from a gathered fragment is
    not corrected wording, for the reason a round record's is not."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], FOUND, marker=True),
            **FILLER,
        },
        "the claim, its fragment, and the release that gathered it",
    )
    head = build(
        repo, {FRAGMENT: f"### Fixed\n\n- {REPAIRED}\n"}, "reflowed the fragment"
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "a range that edited a gathered fragment and nothing else was read as "
        f"a correction to chase into docs/a.md; exit {code}\n{text}"
    )
    assert re.search(r"against 0 sentence\(s\)", text), text


def test_an_ungathered_fragment_is_still_a_carrier(tmp_path):
    """S10, the half that must not move. With no marker in `CHANGELOG.md` the
    fragment is this release's own prose, and it is reported."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], "An unrelated entry."),
            **FILLER,
        },
        "the claim, and a fragment nothing has gathered",
    )
    head = build(repo, {"docs/a.md": f"# a\n\n{REPAIRED}\n"}, "corrected docs/a.md")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"an ungathered fragment went unreported; exit {code}\n{text}"
    assert FRAGMENT in text, text


def test_a_marker_quoted_in_a_fence_gathers_nothing(tmp_path):
    """S9 (#487's class, one reader over). A gathered fragment is EXCUSED
    from the sweep, so its marker counts only on a live line, as
    `folded_items` reads `docs/`. A `CHANGELOG.md` that shows the marker
    inside a fenced example has gathered nothing, and the fragment is still
    this release's own prose. Seen red against `c52e8350`, whose
    `MARKER.findall` over the whole file excused the fragment: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    quoted = (
        changelog(RELEASED_HEADINGS[0], "An unrelated entry.")
        + "\nThe gather writes a line like this:\n\n```markdown\n"
        + f"<!-- specs/{os.path.basename(SHIPPED)} -->\n```\n"
    )
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": quoted,
            **FILLER,
        },
        "the claim, and a fragment whose marker is only quoted",
    )
    head = build(repo, {"docs/a.md": f"# a\n\n{REPAIRED}\n"}, "corrected docs/a.md")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a quoted marker excused the fragment; exit {code}\n{text}"
    assert FRAGMENT in text, text


# --- #551: a file moved and reworded in one commit is a rename to git ------
#
# `git diff --name-only` runs with rename detection, so a file moved whole is
# listed under its new path alone and the range removed nothing the sweep
# could see. Right for a pure move -- and identical for a move with one
# sentence reworded, which git calls a rename too (`R096` when measured): the
# reworded sentence never entered `wanted`, and its copy standing in another
# file was never reported. Read with `--no-renames`, a rename is a deletion
# plus an addition, so the old path is read; and since #563 a sentence that
# arrives verbatim at the new path is held, so a pure move removes nothing.

# Long enough that git reads the move as a rename even with one sentence
# changed; the case asserts that it did, so the fixture cannot quietly turn
# into the delete-plus-add shape the sweep already handled.
LONG_SECTION = "## The verdict cell\n\n{claim}\n\n" + "".join(
    f"Paragraph {n} of the section says something nobody else repeats, at length.\n\n"
    for n in range(40)
)


def name_status(repo, head):
    out = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-status", f"{head}^", head],
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return out.stdout


def moved_section(repo, moved_claim):
    """`a.md` with a long section and its claim quoted in `notes.md`, then the
    section moved to `b.md` in one commit carrying `moved_claim`."""
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            "a.md": f"# a\n\n{LONG_SECTION.format(claim=FOUND)}",
            "notes.md": f"# notes\n\nQuoted here: {FOUND}\n",
            **FILLER,
        },
        "the section, and a note quoting its claim",
    )
    os.remove(os.path.join(str(repo), "a.md"))
    return build(
        repo,
        {"b.md": f"# b\n\n{LONG_SECTION.format(claim=moved_claim)}"},
        "the section moved to b.md",
    )


def test_a_file_moved_as_a_rename_with_one_sentence_reworded_is_still_measured(
    tmp_path,
):
    """S17 (#551). Probe 3's shape: git reports the move as a rename, and the
    reworded claim's copy in `notes.md` has to be reported all the same.
    Red against rename detection at exit 0 and `against 0 sentence(s)`."""
    repo = tmp_path / "probe"
    head = moved_section(repo, REPAIRED)
    status = name_status(repo, head)
    assert status.startswith("R"), (
        f"git did not read the move as a rename, so this case measures the "
        f"delete-plus-add shape instead:\n{status}"
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "notes.md still carries the claim the moved section reworded, and the "
        f"range was read as removing nothing because git called the move a "
        f"rename; exit {code}\n{text}"
    )
    assert "notes.md" in text, f"the report does not name the survivor:\n{text}"


def test_a_file_moved_verbatim_is_silent_because_it_removes_nothing(tmp_path):
    """S18 (#551, rewritten for #563). The half that must not move.

    A pure move is silent because a sentence the range moved to another
    path is held, never removed and never written: the count of removed
    sentences is 0. It used to be positive, every sentence removed and
    written back, and that count was this case's proof that the old path
    was read at all. That proof is S17's now -- a rename that rewords one
    sentence can only be measured if the old path is read."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    body = f"# a\n\n{LONG_SECTION.format(claim=FOUND)}"
    build(
        repo,
        {"a.md": body, "notes.md": f"# notes\n\nQuoted here: {FOUND}\n", **FILLER},
        "the section, and a note quoting its claim",
    )
    os.remove(os.path.join(str(repo), "a.md"))
    head = build(repo, {"b.md": body}, "a.md moved whole to b.md")
    assert name_status(repo, head).startswith("R")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, f"a verbatim move was reported; exit {code}\n{text}"
    assert "no removed wording is still standing" in text, text
    assert re.search(r"against 0 sentence\(s\)", text), (
        "a verbatim move still counts its sentences as removed, so the moved "
        f"text is written and subtracts whatever it shares:\n{text}"
    )


# --- #563: a sentence moved to another path is held, never written ---------
#
# Read as a deletion plus an addition, a move wrote its whole text back as the
# range's own, and that text subtracted every n-gram it shared with a
# correction made elsewhere in the same range. So a quote the move carried
# along hid itself and every other copy of the corrected claim. A move changes
# no sentence's author: a sentence removed at one path and added verbatim at
# another is neither removed nor written, the in-file counting rule applied
# across paths. Two quoting copies halve each other's weight, so the pool is
# made large enough that two independent runs still clear the floor.

MORE_FILLER = {
    f"filler/more-{n}.md": f"# more filler {n}\n\nAnother unrelated line {n}.\n"
    for n in range(48)
}


def test_a_file_moved_whole_still_reports_the_quote_it_carried(tmp_path):
    """M1, #563's probe. `c.md` quotes `docs/a.md`'s claim and is moved
    whole to `d.md` in the commit that corrects `docs/a.md`. Written as the
    range's own, the moved quote subtracted the correction's removed
    wording and neither copy was reported. Red at c52e8350: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    quote = f"# c\n\nQuoted here: {FOUND}\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            "docs/c.md": quote,
            **FILLER,
            **MORE_FILLER,
        },
        "the claim, and two documents quoting it",
    )
    os.remove(os.path.join(str(repo), "docs", "c.md"))
    head = build(
        repo,
        {"docs/a.md": f"# a\n\n{REPAIRED}\n", "docs/d.md": quote},
        "move c.md to d.md, and correct a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the moved quote was written as the range's own and subtracted the "
        f"corrected claim; exit {code}\n{text}"
    )
    assert "docs/b.md" in text and "docs/d.md" in text, (
        f"both copies of the corrected claim stand and the report names:\n{text}"
    )


def test_a_split_document_still_reports_the_quote_it_moved(tmp_path):
    """M2, the split #563 names as reachable here: `docs/c.md` keeps one of
    its sections and the other, which quotes the claim, moves to `docs/d.md`
    in the commit that corrects `docs/a.md`. Both files remain, so no
    whole-file rule sees a move. Red at c52e8350: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    one = f"## One\n\nQuoted here: {FOUND}\n"
    two = "## Two\n\nThe second section says something else entirely.\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            "docs/c.md": f"# c\n\n{one}\n{two}",
            **FILLER,
            **MORE_FILLER,
        },
        "the claim, a document quoting it, and a two-section document",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "docs/c.md": f"# c\n\n{two}",
            "docs/d.md": f"# d\n\n{one}",
        },
        "split c.md's first section into d.md, and correct a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the split's moved section was written as the range's own and "
        f"subtracted the corrected claim; exit {code}\n{text}"
    )
    assert "docs/b.md" in text and "docs/d.md" in text, (
        f"both copies of the corrected claim stand and the report names:\n{text}"
    )


def test_a_move_holds_only_as_many_copies_as_it_carried(tmp_path):
    """M6, the pairing is one for one. `docs/a.md` states the claim twice;
    the range moves one statement to `docs/d.md` and corrects the other.
    One copy arrived, so one is held and the other is still removed --
    paired by key alone, both were held and the correction measured
    nothing. Red at c52e8350 (exit 0, the moved copy written), and red with
    the pairing's count left undecremented."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\nFirst. {FOUND}\n\nSecond. {FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            **FILLER,
            **MORE_FILLER,
        },
        "the claim stated twice, and a document quoting it",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\nFirst. {REPAIRED}\n",
            "docs/d.md": f"# d\n\nSecond. {FOUND}\n",
        },
        "move the second statement to d.md, and correct the first",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "one copy of the claim moved and the other was corrected, and the "
        f"move held both; exit {code}\n{text}"
    )
    assert "docs/b.md" in text and "docs/d.md" in text, text


def test_a_copy_written_beyond_the_ones_moved_is_the_ranges_writing(tmp_path):
    """M7, the other side of one for one. `docs/c.md`'s quote moves to
    `docs/d.md`, and the same range writes a second copy of it into
    `docs/e.md`. One copy arrived by the move and is held; the other is
    wording this range wrote, and it is subtracted as any written wording
    is, so the run is silent. Holding every copy of a key that was moved
    once reported both files -- red with the pairing's second count left
    undecremented."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    quote = f"# c\n\nQuoted here: {FOUND}\n"
    build(
        repo,
        {"docs/a.md": f"# a\n\n{FOUND}\n", "docs/c.md": quote, **FILLER, **MORE_FILLER},
        "the claim, and a document quoting it",
    )
    os.remove(os.path.join(str(repo), "docs", "c.md"))
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "docs/d.md": quote,
            "docs/e.md": f"# e\n\nQuoted here: {FOUND}\n",
        },
        "move c.md to d.md, write a second copy into e.md, correct a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "the copy this range wrote into e.md was held with the moved one, so "
        f"wording the range wrote was not subtracted; exit {code}\n{text}"
    )
    assert re.search(r"against 1 sentence\(s\)", text), (
        f"only a.md's corrected sentence is removed; the move removes nothing:\n{text}"
    )


# --- #592: a move pairs with its own origin, and the correction is named ----
#
# A key removed at two paths and added at one used to pair with whichever
# departure came first in path order. When one departure was a correction and
# the other a move, the report's `corrected` line could name the path that
# only moved. The verdict and the score are the same either way -- the key,
# and so its n-grams, is identical -- so what these cases pin is the line a
# person follows to find the correction.


def corrected_lines(text):
    """The `path:line` each report's `corrected` line names."""
    return [
        line.split()[1]
        for line in text.splitlines()
        if line.startswith("  corrected   ")
    ]


def moved_and_corrected(repo, corrected, moved, before, remains, arrived):
    """`corrected` states FOUND and is corrected to REPAIRED; in the same
    commit `moved` goes from `before` to `remains` (None: removed) and
    `arrived` lands at `docs/z.md`. `docs/b.md` keeps FOUND throughout."""
    os.makedirs(repo)
    build(
        repo,
        {
            corrected: f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\n{FOUND}\n",
            moved: before,
            **FILLER,
            **MORE_FILLER,
        },
        "the claim, a copy of it, and a document carrying it too",
    )
    if remains is None:
        os.remove(os.path.join(str(repo), *moved.split("/")))
        files = {}
    else:
        files = {moved: remains}
    files.update({corrected: f"# a\n\n{REPAIRED}\n", "docs/z.md": arrived})
    return build(repo, files, "correct one copy and move the other")


def test_a_move_pairs_with_its_own_origin_and_the_correction_is_named(tmp_path):
    """S1. `docs/a.md` corrects FOUND, and `docs/m.md` -- the same sentence
    under a heading of its own -- moves whole to `docs/z.md`. The arrival
    shares two keys with `docs/m.md` and one with `docs/a.md`, so it pairs
    with the move, and the correction is the source every report names.
    Red at 2e0e2fa7: `corrected` named `docs/m.md:3`, the path that moved."""
    repo = tmp_path / "probe"
    moved = f"# m\n\n{FOUND}\n"
    head = moved_and_corrected(repo, "docs/a.md", "docs/m.md", moved, None, moved)
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"exit {code}\n{text}"
    assert coordinates_in(text) == {"docs/b.md:3", "docs/z.md:3"}, text
    assert set(corrected_lines(text)) == {"docs/a.md:3"}, (
        f"the report names the path that only moved as the correction:\n{text}"
    )


def test_a_split_pairs_with_its_own_origin_while_both_files_remain(tmp_path):
    """S1's split. `docs/m.md` keeps one section and the other, carrying
    FOUND, moves to `docs/z.md`; both files remain, so nothing is gone at `b`
    and only the shared keys tell the move from the correction. Red at
    2e0e2fa7, and red with affinity dropped from the order."""
    repo = tmp_path / "probe"
    section, kept = (
        f"## Moved\n\n{FOUND}\n",
        "## Kept\n\nThe kept section says little.\n",
    )
    head = moved_and_corrected(
        repo, "docs/a.md", "docs/m.md", f"{section}\n{kept}", kept, section
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"exit {code}\n{text}"
    assert set(corrected_lines(text)) == {"docs/a.md:3"}, text


def test_path_order_does_not_decide_which_departure_is_the_source(tmp_path):
    """S2. The moved file sorts first, so path order alone already names the
    correction; the case holds the answer under an order that would favour
    the other file, which a reversed order turns red."""
    repo = tmp_path / "probe"
    moved = f"# m\n\n{FOUND}\n"
    head = moved_and_corrected(repo, "docs/q.md", "docs/0.md", moved, None, moved)
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"exit {code}\n{text}"
    assert set(corrected_lines(text)) == {"docs/q.md:3"}, text


def test_a_one_sentence_move_pairs_with_the_path_gone_at_the_tip(tmp_path):
    """S3. `docs/m.md` holds only the sentence, so both departures share one
    key with the arrival. The tie goes to the departure whose path is gone
    at `b`: the moved file. Red at 2e0e2fa7 (`docs/m.md:1`)."""
    repo = tmp_path / "probe"
    head = moved_and_corrected(
        repo, "docs/a.md", "docs/m.md", f"{FOUND}\n", None, f"{FOUND}\n"
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"exit {code}\n{text}"
    assert set(corrected_lines(text)) == {"docs/a.md:3"}, text


# --- #554: a local-mode declaration owns the range on its own branch --------
#
# In local mode the `seal/` root is `<git-common-dir>/seal/` and nothing under
# it is committed (`agent-contract` §16), so a work item's own directory is
# never in a range's diff, and the ownership test the second anchor asks --
# does the range touch the directory the file sits in -- refused the work
# item's own range row as `not yours`. There the owner is read from the work
# item's `routing.md` `Branch` row: the row holds over a range whose tip is on
# that branch and on no local branch that one was cut from. Shared mode is
# unchanged.

LOCAL_ITEM = "1799000001-work-item-a"


def local_mode_items(repo):
    """A base carrying two claims twice over, and two branches each
    correcting the first statement of one. Work item A's declaration and
    routing name `work-item-a` and live under the common git directory.
    Leaves `release` checked out and answers A's `survivors.md`."""
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
    probe_git(repo, "switch", "-qc", "work-item-a")
    build(
        repo,
        {
            "a-notes.md": (
                "# a\n\nFirst. The verdict cell is written by the generator and "
                f"the orchestrator leaves it untouched afterwards.\n\nSecond. {CLAIM_A}\n"
            )
        },
        "work item A corrects its claim",
    )
    probe_git(repo, "switch", "-q", "release")
    probe_git(repo, "switch", "-qc", "work-item-b")
    build(
        repo,
        {
            "b-notes.md": (
                "# b\n\nFirst. The exemption row is anchored by the work item and "
                f"the checker leaves that reach untouched afterwards.\n\nSecond. {CLAIM_B}\n"
            )
        },
        "work item B corrects its claim",
    )
    probe_git(repo, "switch", "-q", "release")
    item = os.path.join(str(repo), ".git", "seal", "specs", LOCAL_ITEM)
    os.makedirs(item)
    with open(os.path.join(item, "routing.md"), "w", encoding="utf-8") as handle:
        handle.write(
            "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n"
            "| Destination | open the pull request |\n| Branch | work-item-a |\n"
        )
    survivors = os.path.join(item, "survivors.md")
    with open(survivors, "w", encoding="utf-8") as handle:
        handle.write(
            f"| Range | Grounds |\n|---|---|\n| `release...HEAD` | {GROUNDS} |\n"
        )
    return survivors


def checkout(repo, branch, linked):
    """`branch` checked out in `repo` itself, or in a linked worktree of it.

    Both, because `git rev-parse --git-common-dir` answers `.git`, relative
    to the directory it ran in, in the main worktree and an absolute path in
    a linked one -- the two spellings `whole_range` has to place a file
    against."""
    if not linked:
        probe_git(repo, "switch", "-q", branch)
        return str(repo)
    where = os.path.join(os.path.dirname(str(repo)), f"linked-{branch}")
    probe_git(repo, "worktree", "add", "-q", where, branch)
    return where


@pytest.mark.parametrize(
    "linked, aliased",
    [(False, False), (True, False), (False, True)],
    ids=["main", "linked", "symlinked"],
)
def test_a_local_mode_work_item_owns_its_own_range_row(tmp_path, linked, aliased):
    """O1 (#554). Work item A's range row, read on A's own branch over A's
    own range, excuses the run -- in the main worktree, in a linked one, and
    with `--exempt` spelled through a symlink to the repository, which git
    never answers with (`agent-contract` §13: the real-path comparison is
    shown to be what places the file, not a temporary directory that happens
    to be spelled one way). Red at c52e8350: exit 1, the row printed under
    `not yours` because the range's diff can never hold a file under the git
    directory."""
    repo = tmp_path / "probe"
    survivors = local_mode_items(repo)
    root = checkout(repo, "work-item-a", linked)
    if aliased:
        alias = tmp_path / "alias"
        try:
            os.symlink(str(repo), str(alias), target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            pytest.skip(f"this platform will not make a symlink here: {exc}")
        survivors = os.path.join(str(alias), os.path.relpath(survivors, str(repo)))
    code, text = run("--range", "release...HEAD", "--root", root, "--exempt", survivors)
    assert "not yours" not in text, (
        f"a local-mode work item's own range row was refused as foreign:\n{text}"
    )
    assert code == 0, f"the declaration did not excuse its own range\n{text}"
    assert "a-notes.md" in text and "every survivor is excused" in text, (
        f"the run was clean rather than declared, which measures nothing:\n{text}"
    )


def test_a_local_mode_declaration_does_not_reach_another_branch(tmp_path):
    """O2, the bound. Local `survivors.md` files are shared by every worktree
    of the clone, and `release...HEAD` re-resolves on each checkout, so on
    work item B's branch A's row resolves onto B's own range. B's tip is not
    on `work-item-a`, so the row is refused and printed with its work item,
    and B's survivor is reported. Red against an ownership test reduced to
    `True`."""
    repo = tmp_path / "probe"
    survivors = local_mode_items(repo)
    root = checkout(repo, "work-item-b", linked=False)
    code, text = run("--range", "release...HEAD", "--root", root, "--exempt", survivors)
    assert code == 1, (
        f"work item A's local declaration excused work item B's run\n{text}"
    )
    assert "b-notes.md" in text, f"B's own survivor was not reported\n{text}"
    assert "not yours" in text and LOCAL_ITEM in text, (
        f"the refused declaration was not printed with its work item:\n{text}"
    )
    # §14: the reason printed is the test that refused the row, so the reader
    # opens `routing.md`, not a diff that could never hold the file.
    assert "tip is not on the branch its routing.md names" in text, text
    assert "touches nothing in it" not in text, text


def test_a_stacked_childs_declaration_does_not_reach_its_parents_range(tmp_path):
    """O6. Work item A's branch is cut from work item B's, so B's tip is an
    ancestor of A's branch; on B's checkout A's `release...HEAD` row
    resolves onto B's own range. The tip being on A's branch is not enough:
    it is on B's, which A's was cut from, and the range is B's run. Red at
    6e48cb5f: exit 0, B's survivor excused by A's row."""
    repo = tmp_path / "probe"
    survivors = local_mode_items(repo)
    probe_git(repo, "switch", "-q", "work-item-b")
    probe_git(repo, "switch", "-qc", "work-item-a-stacked")
    item = os.path.dirname(survivors)
    with open(os.path.join(item, "routing.md"), "w", encoding="utf-8") as handle:
        handle.write(
            "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n"
            "| Destination | open the pull request |\n| Branch | work-item-a-stacked |\n"
        )
    build(repo, {"filler.md": "# filler\n\nA's own later change.\n"}, "A on top of B")
    root = checkout(repo, "work-item-b", linked=False)
    code, text = run("--range", "release...HEAD", "--root", root, "--exempt", survivors)
    assert code == 1, f"a stacked child's declaration excused its parent\n{text}"
    assert "b-notes.md" in text and "not yours" in text, text
    # §14: the reason names the cut, not a branch the tip is off.
    assert (
        "this range's tip is on a branch the one its routing.md names was cut from"
        in text
    ), text


@pytest.mark.parametrize(
    "routing, reason",
    [
        (None, "it has no routing.md this run can read"),
        (
            "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n",
            "its routing.md is not a declaration naming a branch",
        ),
        (
            "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n"
            "| Destination | open the pull request |\n| Branch | no-such-branch |\n",
            "the branch its routing.md names, no-such-branch, is not here",
        ),
    ],
    ids=["missing", "no-branch", "unknown-branch"],
)
def test_a_local_mode_declaration_nobody_can_place_is_not_yours(
    tmp_path, routing, reason
):
    """O4. A local-mode work item whose `routing.md` is missing, names no
    branch, or names a branch this repository does not have, cannot say
    whose its declaration is, so the row excuses nothing and prints under
    `not yours` -- on the very branch it was written for, which is the loud
    direction -- with the reason that refused it (§14). Red at 6e48cb5f,
    where all three printed one sentence naming a branch."""
    repo = tmp_path / "probe"
    survivors = local_mode_items(repo)
    where = os.path.join(os.path.dirname(survivors), "routing.md")
    if routing is None:
        os.remove(where)
    else:
        with open(where, "w", encoding="utf-8") as handle:
            handle.write(routing)
    root = checkout(repo, "work-item-a", linked=False)
    code, text = run("--range", "release...HEAD", "--root", root, "--exempt", survivors)
    assert code == 1, f"a declaration nobody can place excused the run\n{text}"
    assert "not yours" in text and LOCAL_ITEM in text, (
        f"the declaration stopped applying without saying so:\n{text}"
    )
    # §14: the reason is what refused the row, never a branch nobody named.
    assert reason in text, text
    assert "tip is not on the branch" not in text, text


def test_a_missing_routing_reader_refuses_rather_than_placing_nothing(tmp_path):
    """O5. `hooks/routing.py` ships in the plugin beside this script; a copy
    without it cannot say whose a local-mode declaration is, and that is
    unusable input (exit 2's `Refused`), the way a missing retirement reader
    is -- never a quiet `not yours` that looks like a judgment."""
    loaded = module()
    loaded.ROUTING = str(tmp_path / "gone" / "routing.py")
    with pytest.raises(loaded.Refused, match=r"routing\.py"):
        loaded.on_its_branch(str(tmp_path), str(tmp_path), "HEAD")


def test_a_missing_common_dir_reader_refuses_rather_than_placing_nothing(tmp_path):
    """O5's twin for `hooks/optin.py`: a copy without it cannot say where
    local mode's root is, and refuses (exit 2's `Refused`) naming that."""
    loaded = module()
    loaded.OPTIN = str(tmp_path / "gone" / "optin.py")
    with pytest.raises(loaded.Refused, match=r"optin\.py, which says where"):
        loaded.local_specs(str(tmp_path))


# --- #564: the gathered reading reads one path, past a heading, over CRLF ---
#
# Three assumptions the gathered-text reading made, each a way the released
# region or the gathered fragment is misread by its shape rather than a policy
# choice. The shape is round 3's 🟡 1: a release renames `## Unreleased`,
# gathers a fragment quoting the claim, and corrects `docs/a.md` in the same
# commit, so a gathered text that is written rather than held subtracts the
# survivor standing in `docs/b.md`.

ENTRY = "The frobnicator now rejects a negative width with a plain message."
OLDER = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
GATHER_MARK = f"<!-- specs/{os.path.basename(SHIPPED)} -->"


def renamed_and_gathered(repo, fragment, body, released_body, write=None):
    """Round 3's 🟡 1 at `fragment`, with `body` as the fragment's text and
    `released_body` as what the release writes under its marker. `write`
    lays `CHANGELOG.md` down itself when the bytes matter (G10)."""
    before = f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {ENTRY}\n\n{OLDER}"
    after = (
        f"# Changelog\n\n{RELEASED_HEADINGS[0]}\n{GATHER_MARK}\n{released_body}\n"
        f"### Fixed\n\n- {ENTRY}\n\n{OLDER}"
    )
    files = {
        "docs/a.md": f"# a\n\n{FOUND}\n",
        "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
        fragment: body,
        **FILLER,
    }
    if write is None:
        files["CHANGELOG.md"] = before
    else:
        write(before)
    build(repo, files, "an unreleased entry, a fragment quoting the claim, two docs")
    files = {"docs/a.md": f"# a\n\n{REPAIRED}\n"}
    if write is None:
        files["CHANGELOG.md"] = after
    else:
        write(after)
    return build(repo, files, "release 1.0.0: rename Unreleased, gather, correct a.md")


def test_a_gathered_fragment_at_the_other_spelling_is_held(tmp_path):
    """G7 (#564 ⬜5). `a_gathered_fragment` accepts `specs/<id>/changelog.md`
    and the reader in `corrected` spelled `seal/specs/<id>/changelog.md`
    alone, so a fragment at the pre-0.4.0 root was out of the pool and the
    range and its gathered text was written all the same. One predicate
    spells the path now. Red at c52e8350: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    fragment = f"specs/{os.path.basename(SHIPPED)}/changelog.md"
    head = renamed_and_gathered(
        repo, fragment, f"### Fixed\n\n- {FOUND}\n", f"### Fixed\n\n- {FOUND}\n"
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        f"the fragment at {fragment} was out of the range and still not held, "
        f"so its gathered text subtracted the survivor in docs/b.md; exit {code}\n"
        f"{text}"
    )
    assert "docs/b.md" in text, text


def test_a_gathered_fragment_carrying_a_heading_stays_released(tmp_path):
    """G8 (#564 ⬜6). A fragment with a `## Notes` line before its quoting
    sentence: under the old region rule any `## ` ended the released
    section, so the gathered text after it read as live prose the release
    wrote, and it subtracted the survivor in `docs/b.md`. After a version
    heading only another version heading or `Unreleased` changes the region.
    Red at c52e8350: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    body = f"## Notes\n\n- {FOUND}\n"
    head = renamed_and_gathered(repo, FRAGMENT, body, body)
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered text after the fragment's own heading was read as live "
        f"and written, subtracting the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text
    assert "CHANGELOG.md:" not in text, (
        f"the released text after the fragment's heading was reported:\n{text}"
    )


def test_an_unreleased_section_below_a_release_is_still_a_carrier(tmp_path):
    """G9, the half that must not move. A changelog that keeps
    `## Unreleased` below a version section -- where this repository's
    gatherer leaves it when it inserts a release above the first `## ` --
    holds live prose there, and its entry restating a corrected claim is
    reported. Green at c52e8350; red against the region rule with the
    `Unreleased` exception deleted."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n{RELEASED_HEADINGS[0]}\n\n### Fixed\n\n"
                f"- An older entry.\n\n## [Unreleased]\n\n### Fixed\n\n- {FOUND}\n"
            ),
            **FILLER,
        },
        "a release, then an unreleased entry carrying the claim",
    )
    head = build(repo, {"docs/a.md": f"# a\n\n{REPAIRED}\n"}, "corrected docs/a.md")
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"the unreleased entry went unreported; exit {code}\n{text}"
    assert "CHANGELOG.md" in text.split("examined", 1)[-1], text


def test_a_crlf_changelog_still_has_its_gathered_ids(tmp_path):
    """G10 (#564 ⬜7). `MARKER` is `$`-anchored under `re.M`, and `$` stands
    before `\\n`, never before `\\r\\n`, so a changelog committed with CRLF
    had no gathered ids: the fragment stayed in the pool and the range, and
    its text was written. Normalised where every text is read. Red at
    c52e8350: exit 0.

    The fixture sets `core.autocrlf=false` and asserts the committed blob
    holds `\\r\\n` (`agent-contract` §13): a runner whose git converts line
    endings would otherwise commit LF and this case would pass measuring
    nothing."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    for command in (
        ["init", "-q", "-b", "main"],
        ["config", "user.email", "probe@example.com"],
        ["config", "user.name", "probe"],
        ["config", "commit.gpgsign", "false"],
        ["config", "core.autocrlf", "false"],
    ):
        probe_git(repo, *command)

    def write(text):
        with open(repo / "CHANGELOG.md", "wb") as handle:
            handle.write(text.replace("\n", "\r\n").encode("utf-8"))

    head = renamed_and_gathered(
        repo, FRAGMENT, f"### Fixed\n\n- {FOUND}\n", f"### Fixed\n\n- {FOUND}\n", write
    )
    blob = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-p", f"{head}:CHANGELOG.md"],
        capture_output=True,
        check=True,
    ).stdout
    assert b"\r\n" in blob and GATHER_MARK.encode() + b"\r\n" in blob, (
        "the committed CHANGELOG.md holds no CRLF, so this case measures an LF "
        "file and proves nothing about line endings"
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the CRLF changelog's marker was not read, so the fragment's gathered "
        f"text was written and subtracted the survivor in docs/b.md; exit {code}\n"
        f"{text}"
    )
    assert "docs/b.md" in text, text


# --- #603: a ledger row removed because its anchor left is no correction ---
#
# `CLAUDE.md`: *a row whose anchor a change removes is REMOVED, not
# re-pointed. Its claim went with the code.* So a range that deletes a unit
# and the row anchored on it has corrected nothing, and a document still
# stating the rule is not a survivor of it. Measured on #587: exit 1, eight
# places, every one sourced from the three removed rows. A row corrected in
# place is a removed line beside an added one, and it IS a correction, so the
# exit is narrower than "a removed row": at least one anchor must resolve at
# the range's left end and not at its right.

LEDGER = "seal/ledger.md"
LEDGER_HEAD = (
    "# ledger\n\n| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
)
# FOUND with one word changed between its two corrected stretches, so it
# shares two runs with FOUND and with what REPAIRED removed from it alike.
RESTATED = FOUND.replace("itself and the", "itself while the")
MODULE = (
    "def helper(width):\n    return width\n\n\ndef other(width):\n    return width\n"
)
KEPT_MODULE = "def other(width):\n    return width\n"


def ledger_row(claim, anchors=("pkg/mod.py#helper",)):
    cited = ", ".join(f"`{anchor}@0123abcd`" for anchor in anchors)
    return f"| R1 · {claim} | {cited} | **Executed** 2026-01-01 | 2026-01-01 | |\n"


def ledger_range(repo, row_after, module_after, ledger_before=None, pool=FILLER):
    """A ledger row anchored on `pkg/mod.py#helper` whose claim `docs/x.md`
    restates, then one commit taking the ledger to `row_after` (None: the
    row removed) and `pkg/mod.py` to `module_after`."""
    os.makedirs(repo, exist_ok=True)
    build(
        repo,
        {
            LEDGER: ledger_before or LEDGER_HEAD + ledger_row(FOUND),
            "pkg/mod.py": MODULE,
            "docs/x.md": f"# x\n\n{RESTATED}\n",
            **pool,
        },
        "a ledger row, its code, and a document stating its claim",
    )
    return build(
        repo,
        {LEDGER: LEDGER_HEAD + (row_after or ""), "pkg/mod.py": module_after},
        "the range",
    )


def test_a_row_removed_with_its_anchor_is_not_a_correction(tmp_path):
    """S7 (#603). The range deletes `helper` and removes the row anchored on
    it. The row's claim went with its code, so `docs/x.md` stating the same
    rule survived nothing. Red at 4910e445: exit 1, `docs/x.md:3`."""
    head = ledger_range(tmp_path / "probe", None, KEPT_MODULE)
    code, text = run("--range", f"{head}^..{head}", "--root", str(tmp_path / "probe"))
    assert code == 0, f"a removed row's claim was read as a correction:\n{text}"


def test_a_row_corrected_in_place_is_still_a_correction(tmp_path):
    """S8. The claim cell is reworded and re-stamped with `helper` still
    there: a removed line beside an added one, and the one ledger act that
    IS a correction. Green before this work, and red against an exit taken
    by every removed row line."""
    head = ledger_range(
        tmp_path / "probe",
        ledger_row(REPAIRED).replace("0123abcd", "4567cdef"),
        MODULE,
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(tmp_path / "probe"))
    assert code == 1, f"a row corrected in place went silent:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text
    assert set(corrected_lines(text)) == {f"{LEDGER}:5"}, text


def test_a_row_removed_while_its_anchors_resolve_stays_measured(tmp_path):
    """S9. The row goes and `helper` stays. No rule removes a row whose
    anchors all still resolve, so the removal is read as any other and the
    restatement is reported. Red with the anchor condition dropped."""
    head = ledger_range(tmp_path / "probe", None, MODULE)
    code, text = run("--range", f"{head}^..{head}", "--root", str(tmp_path / "probe"))
    assert code == 1, f"a row removed with its anchor standing was excused:\n{text}"
    assert set(corrected_lines(text)) == {f"{LEDGER}:5"}, text


def test_one_anchor_leaving_a_file_that_remains_is_enough(tmp_path):
    """S10, the shape of `seal/releases/0.15.1.md` S1 on #587's range: two
    anchors, and only one unit is removed, from a file that stays. The row
    takes the exit on the one that left."""
    repo = tmp_path / "probe"
    both = ("pkg/mod.py#helper", "pkg/mod.py#other")
    head = ledger_range(repo, None, KEPT_MODULE, LEDGER_HEAD + ledger_row(FOUND, both))
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, f"a row one of whose anchors left was measured:\n{text}"


def test_a_row_corrected_in_place_while_an_anchor_is_renamed_is_a_correction(
    tmp_path,
):
    """The shape #589's squash has (`seal/releases/0.15.1.md` R1): the claim
    is corrected in place, and the same range renames one of the row's
    units, so the old name resolves at the left end and not at the right.
    The row still stands, re-pointed, because a live row of the same file
    cites every anchor of it that still resolves; its old claim is a
    correction and stays measured. Red at afb03a4c: exit 0."""
    repo = tmp_path / "probe"
    both = ("pkg/mod.py#helper", "pkg/mod.py#other")
    renamed = MODULE.replace("def helper(", "def helper_renamed(")
    head = ledger_range(
        repo,
        ledger_row(REPAIRED, ("pkg/mod.py#helper_renamed", "pkg/mod.py#other")),
        renamed,
        LEDGER_HEAD + ledger_row(FOUND, both),
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a row corrected in place took the exit:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text
    assert set(corrected_lines(text)) == {f"{LEDGER}:5"}, text


def test_a_row_whose_anchor_never_resolved_here_stays_measured(tmp_path):
    """Condition (c)'s first half. A row anchored on a path this repository
    never held -- a cross-repository row, read with `--map` -- resolves at
    neither end, so nothing shows its anchor LEFT, and its removal is read
    as any other. Red with the left-end half of the condition dropped."""
    repo = tmp_path / "probe"
    elsewhere = LEDGER_HEAD + ledger_row(FOUND, ("vendor/other.py#helper",))
    head = ledger_range(repo, None, KEPT_MODULE, elsewhere)
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a row whose anchor never resolved took the exit:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text


def test_a_row_whose_line_still_stands_takes_no_exit(tmp_path):
    """Condition (b). The row stood twice and one copy is removed with its
    anchor; the other still stands at the tip, so the row was not removed
    and the removed copy is measured as any removed line is. A ledger in this
    state has a BROKEN row `evidence-check` refuses, which is why the loud
    direction is the one kept. Red with the standing-line test dropped.
    The standing copy is a second carrier of every phrase, which halves each
    one's weight, so the pool is `MORE_FILLER`'s size, as #563's cases are."""
    repo = tmp_path / "probe"
    twice = LEDGER_HEAD + ledger_row(FOUND) + ledger_row(FOUND)
    head = ledger_range(
        repo, ledger_row(FOUND), KEPT_MODULE, twice, {**FILLER, **MORE_FILLER}
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a row still standing at the tip took the exit:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text


@pytest.mark.parametrize(
    "open_, close",
    [("```text\n", "```\n"), ("<!--\n", "-->\n")],
    ids=["fence", "comment"],
)
def test_a_row_quoted_in_a_fence_or_a_comment_stays_measured(tmp_path, open_, close):
    """S11. A "row" inside a fenced block or an HTML comment of a ledger
    file is an example, not a claim, so it takes no exit, the way a quoted
    fold marker gathers nothing. Red with the live-line test dropped."""
    repo = tmp_path / "probe"
    quoted = LEDGER_HEAD + "\n" + open_ + ledger_row(FOUND) + close
    head = ledger_range(repo, None, KEPT_MODULE, quoted)
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a quoted row took the exit:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text


def test_a_removed_rows_claim_carried_to_a_new_row_is_held_not_written(tmp_path):
    """S12. The row goes with its anchor, and its claim cell arrives
    verbatim in a work item's fragment row with a new anchor. The arrival is
    a move, so it is held rather than written, and a correction of the same
    claim in `docs/a.md` stays measured: `docs/b.md` is reported. The removed
    row leaves AFTER the pairing; dropped before it, the fragment's copy was
    written and subtracted the correction -- red that way (exit 0)."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            LEDGER: LEDGER_HEAD + ledger_row(FOUND),
            "pkg/mod.py": MODULE,
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\n{FOUND}\n",
            **FILLER,
            **MORE_FILLER,
        },
        "a ledger row, its code, and two documents stating its claim",
    )
    head = build(
        repo,
        {
            LEDGER: LEDGER_HEAD,
            "pkg/mod.py": KEPT_MODULE,
            "seal/ledger/1700000004-a-new-home.md": ledger_row(
                FOUND, ("pkg/mod.py#other",)
            ),
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
        },
        "the row moves to a fragment on a new anchor, and a.md is corrected",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"the fragment's copy was written and hid a.md:\n{text}"
    assert "docs/b.md:3" in coordinates_in(text), text
    assert set(corrected_lines(text)) == {"docs/a.md:3"}, text


def test_a_removed_rows_cells_are_the_lines_the_row_stood_on(tmp_path):
    """`removed_ledger_rows` keys a row by the line it stood on at the
    range's left end, and `corrected` drops the removed sentences read from
    that line. The two numberings have to agree: 1-based, the way `segments`
    counts. A sentence of the row carries the line the predicate names."""
    loaded = module()
    text = LEDGER_HEAD + ledger_row(FOUND)
    row = next(s for s in loaded.sentences(LEDGER, text) if "verdict" in s.words)
    repo = tmp_path / "probe"
    head = ledger_range(repo, None, KEPT_MODULE)
    base = resolves_in(repo, f"{head}^")
    removed = loaded.removed_ledger_rows(
        str(repo), base, head, {LEDGER: text}, {LEDGER: LEDGER_HEAD}
    )
    assert removed == {(LEDGER, row.line)}, (removed, row.line)


def resolves_in(repo, rev):
    out = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", rev],
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return out.stdout.strip()


def test_the_ledger_shapes_are_the_ones_the_ledger_checker_reads():
    """The sweep spells the four ledger locations as git path shapes, and
    `evidence_check.py#default_patterns` is where they are decided. Held
    against that function's own answer, in shared mode, so a fifth location
    added there turns this red rather than leaving the sweep reading four."""
    loaded = module()
    checker = loaded.evidence()
    tails = {
        os.path.relpath(pattern, ROOT).replace(os.sep, "/")
        for pattern in checker.default_patterns(ROOT)
    }
    assert tails == set(loaded.LEDGER_SHAPES), (tails, loaded.LEDGER_SHAPES)
    for path, ledger in (
        ("seal/ledger.md", True),
        ("seal/ledger/1700000004-a-new-home.md", True),
        ("seal/releases/0.15.3.md", True),
        ("docs/_evidence.md", True),
        ("docs/policy/deep/_evidence.md", True),
        ("seal/ledger/nested/x.md", False),
        ("docs/ledger.md", False),
        ("seal/specs/1700000004-a-new-home/ledger.md", False),
    ):
        assert bool(loaded.LEDGER_PATH.match(path)) is ledger, path


def test_a_missing_ledger_checker_refuses_rather_than_measuring(tmp_path):
    """`evidence_check.py` ships beside this script under `skills/`. A copy
    without it cannot say which rows left with their code, and that is
    unusable input (exit 2's `Refused`), the way a missing retirement reader
    is -- never a quiet reading of every removed row as a correction."""
    loaded = module()
    loaded.EVIDENCE = str(tmp_path / "gone" / "evidence_check.py")
    with pytest.raises(loaded.Refused, match=r"evidence_check\.py, which says"):
        loaded.removed_ledger_rows(
            str(tmp_path), "HEAD", "HEAD", {LEDGER: LEDGER_HEAD}, {}
        )


# #587's squash on `release/v0.15.3`: it removed three ledger rows whose
# anchors left `tests/test_a_document_has_room_for_the_next_fold.py` and the
# fold checker's old home, and every one of the eight places it reported was
# sourced from those rows.
REMOVED_ROWS_RANGE = "58629718"


def test_the_measured_range_that_removed_three_rows_reports_nothing():
    """S13. Red at 4910e445: exit 1, eight places."""
    if not resolves(REMOVED_ROWS_RANGE):
        pytest.skip(f"{REMOVED_ROWS_RANGE} is not in this clone")
    code, text = over(REMOVED_ROWS_RANGE)
    assert code == 0, f"the removed rows' claims were read as corrections:\n{text}"
