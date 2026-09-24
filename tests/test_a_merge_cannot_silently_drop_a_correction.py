"""A merge that takes one side drops the other side's corrections in silence.

Issue #424. Two branches each corrected rows of `seal/ledger.md` that the
other had not touched, the file conflicted in two hunks, and the two hunks
resolved in OPPOSITE directions because each side was the superset in one.
Taking a side wholesale reverted three corrections, each of which had turned a
false claim true -- and **a row reverted to a superseded state is
byte-identical to a row nobody has touched**, so `evidence-check` reports it
`ok` and `--reverify` re-stamps it. The only reason it was caught: somebody
grepped for the marker the corrections carried and found 0 occurrences of
`Corrected 2026-09-15` in a file that had had three.

What the check reads is the marker those corrections already carry, and what
separates a loss from a legitimate removal is **whether the row survived**.
`CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not re-pointed*
is that rule, so the distinction is the repository's own and not one this
check invents. A check that fired on a legitimate removal would be one people
learn to skip, which is why A3 below is an acceptance row rather than a note.

Acceptance rows A1-A9 are
`seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md`;
each case below names the row it holds.

**Every case here was seen red before it was committed** (`agent-contract`
§15), against the mutation its phase names -- phase 1's cases against the
reader's absence (`ImportError`), phase 2's against the merge walk's, and A3's
by inverting the row-survival test so the check fires on a removal.

The two cases work item 1789996780 added were shown red the same way.
`test_a_tie_falls_to_the_first_parent` (#471) against `examine`'s parent walk
reversed, the mutation that leaves every other case green.
`test_the_bound_covers_every_candidate_marker_site_the_corpus_carries` (#469)
against `MARKER`'s bound narrowed to four -- and then a second time with the
bound narrowed AND its census taken with `MARKER` itself, which leaves it
green. That pair is the point: the second run is the circular census that went
wrong twice in #424, demonstrated rather than asserted.
"""

import importlib.util
import io
import os
import pathlib
import re
import subprocess

from conftest import on_disk

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(
    ROOT, "skills", "evidence-check", "scripts", "correction_check.py"
)


def load():
    spec = importlib.util.spec_from_file_location("correction_check", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cc = load()


# A ledger the size of a fixture, in the shape the real one has: a header row,
# a separator, and rows whose first cell opens with an id token and a `·`.
HEAD = "| Claim | Code grounds | Verified behavior | Notes |\n|---|---|---|---|\n"


def ledger(*rows):
    return HEAD + "".join(row.rstrip("\n") + "\n" for row in rows)


R1 = (
    "| R1 · the gate resolves the base CI will read "
    "| `skills/verify/scripts/broad_gate.py#gate@a5dec80b` "
    "| **Executed** 2026-09-21. Corrected 2026-09-15 by review round 3, "
    "finding 3. | the row rests an argument on this |"
)
R1_REWORDED = (
    "| R1 · the gate resolves the base CI will read "
    "| `skills/verify/scripts/broad_gate.py#gate@a5dec80b` "
    "| **Executed** 2026-09-21. Corrected 2026-09-15 (#205): the wording "
    "moved to its one home. | the row rests an argument on this |"
)
R1_REVERTED = (
    "| R1 · the gate resolves the base CI will read "
    "| `skills/verify/scripts/broad_gate.py#gate@a5dec80b` "
    "| **Executed** 2026-09-21. | the row rests an argument on this |"
)
R2 = (
    "| R2 · every consumer takes the resolved commit "
    "| `skills/verify/scripts/broad_gate.py#panel@59d37fa2` "
    "| **Read** 2026-09-20. Re-read 2026-09-05 and widened. | none |"
)
R2_REVERTED = (
    "| R2 · every consumer takes the resolved commit "
    "| `skills/verify/scripts/broad_gate.py#panel@59d37fa2` "
    "| **Read** 2026-09-20. | none |"
)


# --- the reader (phase 1) --------------------------------------------------


def test_a_marker_is_the_leading_verb_and_date_and_nothing_after_it():
    """A3's sibling: matching the prose after the date pins the check to
    wording somebody will reword. At least three spellings of the `Corrected`
    sentence already exist in `seal/ledger.md`.

    The prose BEFORE the date varies too, across a minority of the file's
    markers and in a range of spellings, and this case does not reach that —
    round 1's finding 1, and
    `test_a_qualifier_between_the_verb_and_the_date_is_the_same_marker` below
    is where it is held."""
    found = cc.markers("Corrected 2026-09-15 by issue #98, and Re-read 2026-09-05.")
    assert found == {("Corrected", "2026-09-15"): 1, ("Re-read", "2026-09-05"): 1}


def test_both_verbs_count_because_re_read_is_the_common_one():
    """A2. `Re-read` is the common verb in this tree by a wide margin and
    `Corrected` is the rare one, and the marked rows carry more occurrences
    than there are marked rows, since a row can carry a marker in more than
    one cell. A check watching only the rare verb would have ignored every row
    the previous work item re-read.

    No figure stands here. This docstring used to say *404 marker occurrences
    on 190 rows*, which was one of six sites stating that number and which was
    false in its own terms — 404 was the file's total and only 401 of them
    stood on rows (#470). The figures live at one site now, the census note
    beside `correction_check.MARKER`, which names the corpus, the instrument
    and the date each one was taken on."""
    assert set(cc.VERBS) == {"Corrected", "Re-read"}


def test_a_verb_that_is_not_a_marker_is_not_read_as_one():
    assert cc.markers("Verified 2026-09-15 by somebody") == {}
    assert cc.markers("Re-reading 2026-09-05 is the work") == {}


def test_a_date_that_is_not_a_date_is_not_a_marker():
    assert cc.markers("Corrected 2026-9-15") == {}
    assert cc.markers("Corrected yesterday") == {}


def test_a_row_carries_its_markers_its_key_and_its_anchors():
    (row,) = [r for r in cc.rows(ledger(R1)) if r.markers]
    assert row.markers == {("Corrected", "2026-09-15"): 1}
    assert row.key.startswith("R1 · the gate resolves")
    assert "skills/verify/scripts/broad_gate.py#gate" in row.anchors


def test_a_separator_and_a_header_are_not_rows_that_can_be_lost():
    assert [r.key for r in cc.rows(HEAD)] == ["Claim"]


def test_a_reworded_sentence_around_a_standing_marker_is_not_a_loss():
    """A7, in the direction the frame measured. The verb and the date stand;
    only the sentence after them moved.

    This case was green while A7 was broken, because the tree also rewords the
    prose BEFORE the date and nothing here reaches it — the third
    green-while-broken unit of this work item (round 1, finding 1).
    `test_a_resolution_that_rewords_the_qualifier_is_not_a_loss` is the other
    direction."""
    assert cc.losses(ledger(R1), ledger(R1_REWORDED)) == []


def test_a_marker_gone_from_a_row_that_still_stands_is_a_loss():
    """A1's reader half. The row is byte-identical to a row nobody touched,
    which is the whole reason nothing else can see this."""
    (loss,) = cc.losses(ledger(R1), ledger(R1_REVERTED))
    assert loss.marker == ("Corrected", "2026-09-15")
    assert loss.row.key.startswith("R1 ·")
    assert loss.standing.raw == R1_REVERTED


def test_a_marker_that_went_with_its_whole_row_is_not_a_loss():
    """A3. This is `REMOVED` and correct -- `CLAUDE.md` says a row whose
    anchor a change removes goes with it. A check that fires here fires on
    work the repository's own rule requires."""
    assert cc.losses(ledger(R1, R2), ledger(R2)) == []


def test_every_lost_marker_is_named_rather_than_the_first():
    """A6's reader half. A check reporting one loss teaches a reader to fix
    one and run again."""
    lost = cc.losses(ledger(R1, R2), ledger(R1_REVERTED, R2_REVERTED))
    assert sorted(loss.marker for loss in lost) == [
        ("Corrected", "2026-09-15"),
        ("Re-read", "2026-09-05"),
    ]


def test_one_of_two_identical_markers_dropped_is_still_a_loss():
    """Markers are counted per row, not merely tested for presence. A row
    that carried `Re-read 2026-09-05` in two cells and carries it in one has
    lost a correction exactly as much as a row that carried it in one."""
    twice = (
        "| R3 · a claim | `a/b.py#f@11111111` "
        "| Re-read 2026-09-05. | Re-read 2026-09-05 and widened. |"
    )
    once = "| R3 · a claim | `a/b.py#f@11111111` | Re-read 2026-09-05. | widened. |"
    (loss,) = cc.losses(ledger(twice), ledger(once))
    assert loss.marker == ("Re-read", "2026-09-05")


def test_a_row_whose_own_claim_cell_was_corrected_is_found_by_its_anchors():
    """The first cell is the cheap identity and it is not the only one: a
    correction can land in the claim itself, and then the key moves with it.
    The anchors do not -- a row is re-anchored nowhere, it is removed."""
    moved = (
        "| R1 · the gate resolves the base that CI actually reads "
        "| `skills/verify/scripts/broad_gate.py#gate@a5dec80b` "
        "| **Executed** 2026-09-21. | the row rests an argument on this |"
    )
    (loss,) = cc.losses(ledger(R1), ledger(moved))
    assert loss.marker == ("Corrected", "2026-09-15")
    assert loss.standing.raw == moved


def test_an_anchor_two_rows_share_does_not_decide_survival():
    """The anchor fallback answers only where it answers unambiguously. Two
    rows citing one unit, one of them removed, is a removal -- and reporting
    it because its neighbour still cites the same anchor is A3 broken by the
    fallback that exists to widen A1."""
    a = "| R4 · one claim | `a/b.py#f@11111111` | Corrected 2026-09-15. | none |"
    b = "| R5 · another claim | `a/b.py#f@11111111` | Re-read 2026-09-05. | none |"
    assert cc.losses(ledger(a, b), ledger(b)) == []


def test_two_result_rows_sharing_one_anchor_decide_nothing_either():
    """The anchor route's ambiguity runs both ways, and the case above pins
    only the parent's side. A merge that split one row into two citing the
    same unit leaves that route with two answers and no grounds to choose
    between them; an arbitrary choice is a loss reported against a row that
    may not be the one the marker was ever on.

    The key route carries the same guard on both sides since round 1's
    finding 3 — `test_two_rows_sharing_a_first_cell_decide_nothing_either`
    and `test_a_row_ambiguous_on_both_identities_is_not_identified`."""
    parent = "| R6 · one claim | `a/b.py#f@11111111` | Corrected 2026-09-15. | none |"
    half = "| R6a · half a claim | `a/b.py#f@11111111` | none | none |"
    other = "| R6b · the other half | `a/b.py#f@11111111` | none | none |"
    assert cc.losses(ledger(parent), ledger(half, other)) == []


def test_a_marker_outside_a_table_row_has_no_row_to_survive():
    """The convention writes markers into row cells. Prose has no row, so
    there is nothing for the row-survival test to decide, and reporting it
    would be reporting a loss the check cannot tell from a rewrite."""
    assert cc.losses("Corrected 2026-09-15 by hand.\n", "") == []


# --- the merge walk (phase 2) ----------------------------------------------


def commit(root, message):
    """Commit the working tree, empty or not.

    `--allow-empty` because a side of the fixture that deliberately changes
    NOTHING is one of the shapes being tested — a parent that left the row
    alone is exactly the side whose wholesale acceptance reverts the other's
    correction — and without the flag git refuses and the fixture dies before
    the case reaches the check.
    """
    run(root, "add", "-A")
    run(root, "commit", "-qm", message, "--allow-empty")
    return run(root, "rev-parse", "HEAD").stdout.strip()


def run(root, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def write(root, path, text):
    target = pathlib.Path(root) / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def merged(tmp, base, ours, theirs, resolution, path="seal/ledger.md"):
    """A repository whose HEAD is a merge of two branches, resolved by hand.

    `base`, `ours`, `theirs` and `resolution` are whole file texts for `path`.
    The merge is attempted and its conflict — if git finds one — is resolved
    by writing `resolution` over the file, which is the act the ticket is
    about: a person choosing what the merged file says.

    Driven from Python rather than a shell line, per `agent-contract` §8: a
    probe that commits reaches the commit gate exactly as real work does, and
    the prompt lands on nobody while a round is running.
    """
    root = pathlib.Path(tmp) / "repo"
    root.mkdir(parents=True, exist_ok=True)
    run(root, "init", "-q")
    run(root, "config", "user.email", "t@t")
    run(root, "config", "user.name", "t")
    write(root, path, base)
    start = commit(root, "base")
    run(root, "checkout", "-q", "-b", "ours")
    write(root, path, ours)
    commit(root, "ours corrects its rows")
    run(root, "checkout", "-q", start)
    run(root, "checkout", "-q", "-b", "theirs")
    write(root, path, theirs)
    commit(root, "theirs corrects its rows")
    run(root, "checkout", "-q", "ours")
    run(root, "merge", "--no-commit", "--no-ff", "theirs", check=False)
    write(root, path, resolution)
    head = commit(root, "Merge branch 'theirs' into ours")
    return root, start, head


def check(root, spec):
    """Run the check over `spec` and return `(exit code, report)`."""
    out = io.StringIO()
    code = cc.main(["--range", spec, "--root", str(root)], out=out)
    return code, out.getvalue()


R_A = "| A1 · the first claim | `a/one.py#f@11111111` | Read. | none |"
R_B = "| B1 · the second claim | `a/two.py#g@22222222` | Read. | none |"
A_CORRECTED = (
    "| A1 · the first claim | `a/one.py#f@11111111` "
    "| Read. Corrected 2026-09-15 by review round 3. | none |"
)
B_REREAD = (
    "| B1 · the second claim | `a/two.py#g@22222222` "
    "| Read. Re-read 2026-09-05 and widened. | none |"
)


def test_a_merge_that_reverts_a_corrected_row_is_reported(tmp_path):
    """A1. `ours` corrected row A; `theirs` did not touch it; the resolution
    took `theirs`'s side of that hunk and the correction went with it. The
    row still stands, byte-identical to a row nobody touched."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(R_A, R_B),
        ours=ledger(A_CORRECTED, R_B),
        theirs=ledger(R_A, B_REREAD),
        resolution=ledger(R_A, B_REREAD),
    )
    code, text = check(root, f"{head}~2..{head}")
    assert code == 1, text
    assert "Corrected 2026-09-15" in text
    assert "seal/ledger.md" in text
    assert "A1 · the first claim" in text


def test_a_merge_that_reverts_a_re_read_row_is_reported(tmp_path):
    """A2, and it is red separately from A1 so a check watching one verb
    cannot pass both. `Re-read` is much the commoner marker in the shared
    file and `Corrected` the rare one; the counts are in the module's census
    note, which is the one site that states them and names the corpus, the
    instrument and the moment each is true of."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(R_A, R_B),
        ours=ledger(R_A, B_REREAD),
        theirs=ledger(A_CORRECTED, R_B),
        resolution=ledger(A_CORRECTED, R_B),
    )
    code, text = check(root, f"{head}~2..{head}")
    assert code == 1, text
    assert "Re-read 2026-09-05" in text


def test_a_merge_that_removes_the_whole_row_reports_nothing(tmp_path):
    """A3. `CLAUDE.md` says a row whose anchor a change removes goes with it,
    so this is the repository's own rule being followed. A check that fires
    here fires on correct work, and a check that fires on correct work is one
    people learn to skip."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(R_A, R_B),
        ours=ledger(A_CORRECTED, R_B),
        theirs=ledger(R_A, R_B),
        resolution=ledger(R_B),
    )
    code, text = check(root, f"{head}~2..{head}")
    assert code == 0, text
    assert "Corrected" not in text.split("examined")[-1].split("\n")[0]


def test_every_lost_marker_in_one_merge_is_named(tmp_path):
    """A6. A check reporting the first loss teaches a reader to fix one and
    run again, which is how the second one ships."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(R_A, R_B),
        ours=ledger(A_CORRECTED, B_REREAD),
        theirs=ledger(R_A, R_B),
        resolution=ledger(R_A, R_B),
    )
    code, text = check(root, f"{head}~2..{head}")
    assert code == 1, text
    assert "Corrected 2026-09-15" in text and "Re-read 2026-09-05" in text


def test_a_marker_a_parent_deleted_is_not_a_loss_at_the_merge(tmp_path):
    """The merge base is what tells a discarded correction from an honoured
    deletion, and M1 is why it is here: without it, `87eced1` — the v0.9.3
    release merge, which carried a deliberate re-anchoring rewrite — is the
    one thing this repository's whole reachable history reports."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(A_CORRECTED, R_B),
        ours=ledger(A_CORRECTED, B_REREAD),
        theirs=ledger(R_A, R_B),
        resolution=ledger(R_A, B_REREAD),
    )
    code, text = check(root, f"{head}~2..{head}")
    assert code == 0, text


def test_the_report_names_the_merge_and_the_parent_the_marker_came_from(tmp_path):
    """A1's second half. `spec.md` §Scope 1 asks for the file, the marker and
    the parent — a reader has to open the hunk, and a report that names only
    the marker sends them looking for which merge and which side."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(R_A, R_B),
        ours=ledger(A_CORRECTED, R_B),
        theirs=ledger(R_A, B_REREAD),
        resolution=ledger(R_A, B_REREAD),
    )
    parent = run(root, "rev-parse", f"{head}^1").stdout.strip()
    _code, text = check(root, f"{head}~2..{head}")
    assert head[:7] in text, text
    assert parent[:7] in text, text


def test_a_range_that_does_not_resolve_is_refused_and_nothing_is_examined(tmp_path):
    root, _start, _head = merged(
        tmp_path,
        base=ledger(R_A),
        ours=ledger(A_CORRECTED),
        theirs=ledger(R_A),
        resolution=ledger(R_A),
    )
    code, _text = check(root, "nosuchref..HEAD")
    assert code == 2


def test_a_marker_the_second_parent_carried_is_reported(tmp_path):
    """Both parents are read, not the one the merge was made from. Which side
    a conflict is resolved onto is whatever the person happened to have
    checked out, and the correction is as likely to be on the other one."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(R_A, R_B),
        ours=ledger(R_A, R_B),
        theirs=ledger(A_CORRECTED, R_B),
        resolution=ledger(R_A, R_B),
    )
    second = run(root, "rev-parse", f"{head}^2").stdout.strip()
    code, text = check(root, f"{head}~2..{head}")
    assert code == 1, text
    assert "Corrected 2026-09-15" in text
    assert second[:7] in text, text


# --- fragments, and the cheap path (phase 3) -------------------------------

FRAGMENT = "seal/ledger/1789969379-a-work-item.md"
F_ROW = "| F1 · a fragment claim | `a/three.py#h@33333333` | Read. | none |"
F_REREAD = (
    "| F1 · a fragment claim | `a/three.py#h@33333333` "
    "| Read. Re-read 2026-09-05 and widened. | none |"
)


def test_a_marker_lost_from_a_fragment_is_reported(tmp_path):
    """A4. `fold_ledger.py` moves every fragment into a ledger file at the
    release (`seal/releases/<X.Y.Z>.md` since #547), so a check watching only
    the gathered files would go blind exactly while the rows are being
    written. Fragments are watched from the first commit."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(F_ROW),
        ours=ledger(F_REREAD),
        theirs=ledger(F_ROW),
        resolution=ledger(F_ROW),
        path=FRAGMENT,
    )
    code, text = check(root, f"{head}~2..{head}")
    assert code == 1, text
    assert FRAGMENT in text
    assert "Re-read 2026-09-05" in text


RELEASE_FILE = "seal/releases/0.4.0.md"


def test_a_marker_lost_from_a_release_file_is_reported(tmp_path):
    """#547, S3. The fold writes each release's rows to
    `seal/releases/<X.Y.Z>.md`, so the rows that used to become shared in
    `seal/ledger.md` become shared there instead, and a check that does not
    list that directory goes blind at exactly the release. Red before
    `ledger_listing` passed `RELEASES` to `ls-tree`."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(F_ROW),
        ours=ledger(F_REREAD),
        theirs=ledger(F_ROW),
        resolution=ledger(F_ROW),
        path=RELEASE_FILE,
    )
    code, text = check(root, f"{head}~2..{head}")
    assert code == 1, text
    assert RELEASE_FILE in text
    assert "Re-read 2026-09-05" in text


def test_a_range_with_no_merge_says_it_looked_at_none(tmp_path):
    """A5. The common case is a range with no merge in it, and it has to SAY
    it looked at none: a check that prints nothing cannot be told from one
    that did nothing, and the second is what the green build then rests on."""
    root = pathlib.Path(tmp_path) / "repo"
    root.mkdir(parents=True)
    run(root, "init", "-q")
    run(root, "config", "user.email", "t@t")
    run(root, "config", "user.name", "t")
    write(root, "seal/ledger.md", ledger(A_CORRECTED))
    start = commit(root, "base")
    write(root, "seal/ledger.md", ledger(R_A))
    head = commit(root, "a correction dropped, but not at a merge")
    code, text = check(root, f"{start}..{head}")
    assert code == 0, text
    assert "no merge commit" in text
    assert "Corrected" not in text


def test_a_ledger_too_big_to_read_is_named_rather_than_passed(tmp_path, monkeypatch):
    """A blob this cannot read is a blob it cannot judge, and saying nothing
    about it is a pass it did not earn -- `skills/verify/SKILL.md` §*The Seal
    Test*. The size cap is the reachable way to produce one; a NUL byte in a
    tracked ledger is the other and behaves the same way."""
    root, _start, head = merged(
        tmp_path,
        base=ledger(R_A, R_B),
        ours=ledger(A_CORRECTED, R_B),
        theirs=ledger(R_A, B_REREAD),
        resolution=ledger(R_A, B_REREAD),
    )
    monkeypatch.setattr(cc, "SIZE_CAP", 10)
    code, text = check(root, f"{head}~2..{head}")
    assert "seal/ledger.md" in text
    assert "not judged" in text, text
    assert code == 0, text


# --- where the leg runs (phase 4) ------------------------------------------

WORKFLOW = os.path.join(ROOT, ".github", "workflows", "hygiene.yml")
BIN = os.path.join(ROOT, "bin")


def pull_request_checkout(root, base, head):
    """What `actions/checkout@v4` leaves a `pull_request` job sitting on.

    The job holds the MERGE ref — the head already merged into the base —
    rather than the head commit, which is why `.github/workflows/hygiene.yml`
    has a comment about it two steps above. Built here by making that merge,
    because M2 is a question about what is reachable from that commit and an
    answer from any other commit is about something else.
    """
    run(root, "checkout", "-q", head)
    run(root, "merge", "--no-edit", "-q", base, check=False)
    return run(root, "rev-parse", "HEAD").stdout.strip()


def test_m2_the_branchs_own_merge_is_reachable_where_the_leg_runs(tmp_path):
    """M2, measured rather than assumed. #424's incident IS a feature branch
    merging its release branch in, so the merge the check must see is one the
    branch itself made — and the leg reads `origin/<base>...HEAD` from a
    checkout that is the merge ref, not the head."""
    root = pathlib.Path(tmp_path) / "repo"
    root.mkdir(parents=True)
    run(root, "init", "-q", "-b", "release/v9.9.9")
    run(root, "config", "user.email", "t@t")
    run(root, "config", "user.name", "t")
    write(root, "seal/ledger.md", ledger(R_A, R_B))
    commit(root, "the release branch")
    # The feature branch corrects a row the release branch has not touched.
    run(root, "checkout", "-q", "-b", "fix/a-thing")
    write(root, "seal/ledger.md", ledger(A_CORRECTED, R_B))
    commit(root, "correct A")
    # The release branch moves on, touching the same file.
    run(root, "checkout", "-q", "release/v9.9.9")
    write(root, "seal/ledger.md", ledger(R_A, B_REREAD))
    commit(root, "the release branch re-reads B")
    # The feature branch merges the release branch in and resolves by taking
    # the release branch's side of both hunks -- #424's incident exactly.
    run(root, "checkout", "-q", "fix/a-thing")
    run(root, "merge", "--no-commit", "--no-ff", "release/v9.9.9", check=False)
    write(root, "seal/ledger.md", ledger(R_A, B_REREAD))
    commit(root, "Merge release/v9.9.9 into fix/a-thing")

    pull_request_checkout(root, "release/v9.9.9", "fix/a-thing")
    code, text = check(root, "release/v9.9.9...HEAD")
    assert code == 1, text
    assert "Corrected 2026-09-15" in text


def test_m2_the_squash_is_what_puts_the_merge_out_of_reach(tmp_path):
    """The other half of M2, and the reason the leg cannot move later. A
    feature branch squashes into its release branch, so after the merge there
    is one commit and no merge for this to read. `spec.md` §*What this repair
    cannot see* claims it; this is the claim executed."""
    root = pathlib.Path(tmp_path) / "repo"
    root.mkdir(parents=True)
    run(root, "init", "-q", "-b", "release/v9.9.9")
    run(root, "config", "user.email", "t@t")
    run(root, "config", "user.name", "t")
    write(root, "seal/ledger.md", ledger(R_A, R_B))
    commit(root, "the release branch")
    run(root, "checkout", "-q", "-b", "fix/a-thing")
    write(root, "seal/ledger.md", ledger(A_CORRECTED, R_B))
    commit(root, "correct A")
    run(root, "checkout", "-q", "release/v9.9.9")
    write(root, "seal/ledger.md", ledger(R_A, B_REREAD))
    before = commit(root, "the release branch re-reads B")
    run(root, "checkout", "-q", "fix/a-thing")
    run(root, "merge", "--no-commit", "--no-ff", "release/v9.9.9", check=False)
    write(root, "seal/ledger.md", ledger(R_A, B_REREAD))
    commit(root, "Merge release/v9.9.9 into fix/a-thing")

    run(root, "checkout", "-q", "release/v9.9.9")
    run(root, "merge", "--squash", "-q", "fix/a-thing", check=False)
    after = commit(root, "fix: a thing (#1)")
    code, text = check(root, f"{before}..{after}")
    assert code == 0, text
    assert "no merge commit" in text


def test_the_wrapper_pair_reaches_the_script():
    """A document that names the command has something to resolve, and the
    `.cmd` twin is what makes that true on Windows as well."""
    for name in ("correction-check", "correction-check.cmd"):
        path = os.path.join(BIN, name)
        assert os.path.isfile(path), path
    with open(os.path.join(BIN, "correction-check"), encoding="utf-8") as f:
        posix = f.read()
    assert "correction_check.py" in posix


def workflow():
    with open(WORKFLOW, encoding="utf-8") as f:
        return f.read()


def test_a9_the_leg_runs_the_check_and_is_allowed_to_fail():
    """A9, read at the workflow. Q2's default is that it blocks, like every
    other arm of this workflow: a lost correction is silent by construction,
    and A3 exists so the check does not fire on correct work."""
    text = workflow()
    assert "correction_check.py" in text, "the leg does not run the check"
    leg = text.split("correction_check.py")[0].split("- name:")[-1]
    assert "continue-on-error" not in leg, "the leg is allowed to pass while red"
    assert "::warning::" not in leg, "a warning is not a gate"


def test_a9_the_leg_asks_the_range_the_pull_request_is_about():
    """The range is `origin/<base>...HEAD`, the same spelling the survivor
    leg uses. Anything narrower misses the branch's own merge, which is the
    one M2 showed is the merge #424 is about."""
    text = workflow()
    step = text.split("correction_check.py")[1].split("- name:")[0]
    assert "origin/${{ github.base_ref }}...HEAD" in step, step


def test_a9_the_leg_skips_a_release_pull_request_and_says_why():
    """A pull request into `main` is a release, and a release branch carries
    squashed commits rather than the feature branches' merges. So the range
    there holds merges of `main` back into the release branch, which is a
    different question, and each work item was checked at its own pull
    request. The skip prints its reason rather than exiting quietly."""
    text = workflow()
    step = text.split("- name:")[
        next(
            i
            for i, part in enumerate(text.split("- name:"))
            if "correction_check.py" in part
        )
    ]
    assert 'github.base_ref }}" = "main"' in step, step
    assert "exit 0" in step, step


# --- the documents (phase 5) -----------------------------------------------

# The sentences both documents have to carry. `CLAUDE.md` and
# `CONTRIBUTING.md` have already disagreed about this rule once -- one forbade
# editing the shared ledger at all while the other forbade appending to it,
# which left a branch that had falsified a row with no reading that permits
# the only correct act. So the two are held against each other rather than
# trusted to be edited together.
#
# Needles rather than whole paragraphs: what must not drift is the
# INSTRUCTION and the argument behind it, and pinning the prose word for word
# would go red on a rewording that says the same thing, which is the failure
# this work item's own check was built to avoid.
CONFLICT_SENTENCES = (
    "resolve it hunk by hunk and read both sides",
    "`--ours`",
    "`--theirs`",
    "resolved in opposite directions",
    "byte-identical to a row nobody touched",
    "correction-check",
)


def read(path):
    """A document with its whitespace collapsed to single spaces.

    Both documents wrap at 88 columns, so a sentence long enough to be worth
    pinning is split across two lines and a raw substring test finds none of
    them. Collapsing is what makes the needle a sentence rather than a line.
    """
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


def test_a8_both_rule_documents_say_what_to_do_at_the_conflict():
    """A8. The instruction has to reach the person at the moment of the act,
    and it lives in the two documents that state the fragment rule's
    exception -- the exception being the whole cause, because a branch that
    falsifies a row is REQUIRED to repair it in the shared file."""
    for document in ("CLAUDE.md", "CONTRIBUTING.md"):
        text = read(document)
        for needle in CONFLICT_SENTENCES:
            assert needle in text, f"{document} does not say: {needle}"


def test_a8_each_document_points_at_the_other():
    """The pin is only as good as the next editor knowing it exists. Each
    document names the other and names the case that holds them together, so
    a session editing one finds out that the sentence has a twin."""
    assert "CONTRIBUTING.md` carries both paragraphs" in read("CLAUDE.md")
    assert "CLAUDE.md` carries both paragraphs" in read("CONTRIBUTING.md")
    for document in ("CLAUDE.md", "CONTRIBUTING.md"):
        assert os.path.basename(__file__) in read(document), document


def test_the_skill_says_what_the_command_is_for_and_when_it_runs():
    """A document that names a script has to give a reader a way to reach it
    (`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`), and
    a check whose moment nobody states is one that gets run at the wrong one:
    the merges it reads stop existing at the squash.

    Read inside the `correction-check` section, not over the whole file.
    `squash` appears twice more in this skill — under *A coordinate names
    content, never a position* and under *Migrating a pre-anchor ledger* — so
    a whole-file assertion stayed green with this command's entire *when it
    runs* paragraph deleted. Measured by the reviewer at round 1, and that is
    the counterfeit `skills/verify/SKILL.md` §*The Seal Test* is about.
    """
    whole = read(os.path.join("skills", "evidence-check", "SKILL.md"))
    assert "correction-check" in whole
    parts = whole.split("## `correction-check`")
    assert len(parts) == 2, "the skill has no `correction-check` section"
    section = parts[1].split(" ## ")[0]
    assert "squash" in section, (
        "the `correction-check` section does not say when the command runs; "
        "the merges it reads stop existing at the squash, and a check whose "
        "moment nobody states gets run at the wrong one"
    )


# --- the qualifier before the date (round 1, finding 1) ---------------------


def test_a_qualifier_between_the_verb_and_the_date_is_the_same_marker():
    """`seal/ledger.md` spells a minority of its markers this way — `again` is
    much the commonest, then `and re-executed` and `a third time`, with seven
    more shapes — and one row carries no other spelling at all. A pattern
    demanding the date immediately after the verb watches neither that row nor
    a reword. The counts are in the module's census note, which is the one
    site that states them and names what each is true of."""
    assert cc.markers("Re-read again 2026-09-05 and widened.") == {
        ("Re-read", "2026-09-05"): 1
    }
    assert cc.markers("Re-read a third time 2026-09-04.") == {
        ("Re-read", "2026-09-04"): 1
    }
    assert cc.markers("Corrected and widened 2026-09-07 by #98.") == {
        ("Corrected", "2026-09-07"): 1
    }


def test_the_qualifier_does_not_swallow_the_next_sentence():
    """A capital letter is the next sentence and a digit is the date."""
    assert cc.markers("Corrected. The row was Re-read 2026-09-05.") == {
        ("Re-read", "2026-09-05"): 1
    }
    assert cc.markers("Re-read 2026-09-05 and widened. Re-read 2026-09-06.") == {
        ("Re-read", "2026-09-05"): 1,
        ("Re-read", "2026-09-06"): 1,
    }


def test_a_capital_word_after_the_verb_is_not_a_qualifier():
    """The lowercase gate, which the two cases above do not reach: both put
    punctuation between the verb and the capital, so the gate is never what
    refuses them. Here there is none.

    The needles are sentences this ledger writes. Its rows argue about
    platforms constantly, so *Re-read Windows and macOS on <date>* is
    ordinary prose in which the date is saying something other than *this
    claim was re-read* — and with the gate widened to accept a capital it
    becomes a marker nobody wrote, whose loss the check would then report.

    A row id will not do the job, and that is worth saying so the next editor
    does not swap one in: `R4` carries a digit, `[A-Za-z-]*` stops before it,
    and the run fails on the bound rather than on the gate. The needle has to
    be a capitalised word that is all letters."""
    assert cc.markers("Re-read Windows and macOS on 2026-09-05") == {}
    assert cc.markers("Corrected Linux behaviour on 2026-09-05") == {}


def test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier():
    """The other direction, and the one nothing held before this round. A
    qualifier is a phrase, so the run is bounded; widen it far enough and the
    verb reaches across a whole clause to a date nobody wrote it against,
    which manufactures a marker and then reports its loss.

    The longest qualifier the tree actually carries is five words — `Re-read
    and re-stamped a third time <date>`, which stands in `seal/ledger.md`'s
    prose rather than on any row — and the bound is five, round 2's finding 6.
    The spelling is the address, not a line number: a row of this repository's
    ledger names content and never a position (`CLAUDE.md`), and the line that
    spelling sat on was cited in four places before #470. This case is red the
    moment that bound stops being a bound."""
    assert cc.markers("Corrected the claim that the reviewer read on 2026-09-05") == {}
    assert cc.markers("Re-read once the base had moved past 2026-09-05") == {}


def test_a_resolution_that_rewords_the_qualifier_is_not_a_loss():
    """A7, in the direction the tree actually spells. The verb stands and the
    date stands; only the qualifier moved, so the reading is the same reading
    and nothing was lost. This is the pair the docstring says matching on
    prose was rejected to avoid, and until this round nothing held it."""
    before = "| R1 · a claim | `a/b.py#f@11111111` | Re-read 2026-09-05. |"
    after = "| R1 · a claim | `a/b.py#f@11111111` | Re-read again 2026-09-05. |"
    assert cc.losses(ledger(before), ledger(after)) == []


def test_a_qualified_marker_reverted_at_a_merge_is_reported(tmp_path):
    """A1 and A2 over the spelling one row of `seal/ledger.md` carries and
    nothing else. This is #424's own incident shape, and the check built for
    it was silent."""
    row = "| A1 · the first claim | `a/one.py#f@11111111` | Read. |"
    corrected = (
        "| A1 · the first claim | `a/one.py#f@11111111` "
        "| Read. Re-read again 2026-09-21 after #424. |"
    )
    root, start, head = merged(
        tmp_path, ledger(row), ledger(corrected), ledger(row), ledger(row)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert "Re-read 2026-09-21" in out, out


# --- one loss, one entry (round 1, finding 2) ------------------------------


def test_a_marker_both_parents_carried_is_reported_once(tmp_path):
    """One marker gone from one row is one loss, whichever parents carried
    it — and every marker older than the fork is carried by both. Reporting
    it per parent told a reader to open two hunks for one, and the closing
    count said two."""
    row = "| A1 · the first claim | `a/one.py#f@11111111` | Read. Re-read 2026-09-05. |"
    ours = (
        "| A1 · the first claim | `a/one.py#f@11111111` "
        "| Read. Re-read 2026-09-05. | ours |"
    )
    theirs = (
        "| A1 · the first claim | `a/one.py#f@11111111` "
        "| Read. Re-read 2026-09-05. | theirs |"
    )
    dropped = "| A1 · the first claim | `a/one.py#f@11111111` | Read. | both |"
    root, start, head = merged(
        tmp_path, ledger(row), ledger(ours), ledger(theirs), ledger(dropped)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert out.count("lost        Re-read 2026-09-05") == 1, out
    assert "1 correction marker(s)" in out, out


# --- the key route gets the same guard (round 1, finding 3) ----------------


def test_two_rows_sharing_a_first_cell_decide_nothing_either():
    """The ambiguity guard is not the anchor route's alone. Two rows with the
    same first cell, one removed, is a removal — and reporting it because its
    twin still carries that cell is A3 broken by the cheap identity, exactly
    as it would be by the fallback. `seal/ledger.md` carries 123 such rows
    today: every section's table header."""
    a = "| same cell | `a/b.py#f@11111111` | Corrected 2026-09-15. | none |"
    b = "| same cell | `a/c.py#g@22222222` | Re-read 2026-09-05. | none |"
    assert cc.losses(ledger(a, b), ledger(b)) == []


def test_a_key_two_result_rows_share_falls_through_to_the_anchors():
    """Ambiguous on one identity is not ambiguous on both, and the fall-
    through is the design rather than a gap in it.

    Round 1's paste-ready fix asked for silence here and its own `standing`
    does not produce it: the parent's row is unambiguous, only ONE result row
    carries its anchors, and the anchor route answers. Answered rather than
    fixed — the reading the case wanted would refuse a row that can be named,
    which is the opposite of what the guard is for. A resolution that split a
    row in two and dropped the marker from the half carrying its anchors did
    lose a correction."""
    parent = "| R6 · one claim | `a/b.py#f@11111111` | Corrected 2026-09-15. | none |"
    half = "| R6 · one claim | `a/b.py#f@11111111` | none | first half |"
    other = "| R6 · one claim | `a/c.py#g@22222222` | none | second half |"
    (loss,) = cc.losses(ledger(parent), ledger(half, other))
    assert loss.marker == ("Corrected", "2026-09-15")
    assert loss.standing.raw == half


def test_a_row_ambiguous_on_both_identities_is_not_identified():
    """Where the key is ambiguous in the result and the row cites nothing,
    there is no second identity to fall through to, and the answer is
    silence. That is the guard `_index` holds on the key, and it is reachable
    rather than theoretical — a ledger row whose claim is about prose carries
    no coordinate at all."""
    parent = "| same cell | a claim about prose | Corrected 2026-09-15. | none |"
    half = "| same cell | a claim about prose | none | first half |"
    other = "| same cell | something else | none | second half |"
    assert cc.losses(ledger(parent), ledger(half, other)) == []


# --- the bound was one short (round 2, findings 6, 7 and 8) ----------------


def test_the_longest_qualifier_the_tree_carries_is_seen(tmp_path):
    """`seal/ledger.md` spells five lowercase words between the verb and the
    date in exactly one place — `Re-read and re-stamped a third time <date>`,
    in the file's prose rather than on any row — and the bound was four, so
    the file's own longest spelling was invisible to the check watching that
    file. The spelling is the address: the line it sits on moves for edits
    that have nothing to do with the claim, which is why `CLAUDE.md` says a
    coordinate names content and never a position.

    Round 1's finding 1 one spelling further out, and found the same way it
    was: by measuring with the run UNBOUNDED instead of with the bound under
    test. The distribution has a hole where the old bound sat — runs of 0, 1,
    2, 3 and 5 words occur and no run of 4 does — so four matched exactly what
    three matched and bought nothing."""
    assert cc.markers("Re-read and re-stamped a third time 2026-09-08.") == {
        ("Re-read", "2026-09-08"): 1
    }
    row = "| A1 · the first claim | `a/one.py#f@11111111` | Read. | none |"
    corrected = (
        "| A1 · the first claim | `a/one.py#f@11111111` "
        "| Read. Re-read and re-stamped a third time 2026-09-08. | none |"
    )
    root, start, head = merged(
        tmp_path, ledger(row), ledger(corrected), ledger(row), ledger(row)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert "Re-read 2026-09-08" in out, out


def test_a_marker_both_parents_carried_is_reported_once_across_a_rewritten_key(
    tmp_path,
):
    """Finding 2 one shape over. One parent corrected the claim cell while
    adding the marker and the other only added it; the resolution dropped it.
    Keyed on the PARENT's first cell that is two tags for one lost marker and
    a closing count of two — a reader sent to open two hunks when there is
    one, which is the defect finding 2 reported.

    The first cell is the identity a correction changes, which is why the
    anchor route exists at all (ledger row C4). Every parent's loss converges
    on the same surviving row, so that row's text is the identity that cannot
    move."""
    base = "| R1 · the gate resolves the base | `a/b.py#f@11111111` | Read. | none |"
    ours = (
        "| R1 · the gate resolves the base CI will read | `a/b.py#f@11111111` "
        "| Read. Corrected 2026-09-21. | none |"
    )
    theirs = (
        "| R1 · the gate resolves the base | `a/b.py#f@11111111` "
        "| Read. Corrected 2026-09-21. | none |"
    )
    got = "| R1 · the gate resolves the base | `a/b.py#f@11111111` | Read. | none |"
    root, start, head = merged(
        tmp_path, ledger(base), ledger(ours), ledger(theirs), ledger(got)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert out.count("lost        Corrected 2026-09-21") == 1, out
    assert "1 correction marker(s)" in out, out


def test_the_parent_named_is_the_one_that_lost_the_most(tmp_path):
    """`examine` names the parent that lost the most occurrences of the
    marker, because that is the side whose text most needs reading, and ledger
    row C9 states the rule. Nothing held it: swapping `max` for `min` left the
    whole module green, and the line a reader acts on is the one that decides
    which hunk they open (`agent-contract` §14).

    `ours` carries the marker in two cells and `theirs` in one, so the two
    sides lose different amounts of the same marker and the choice is
    visible."""
    base = "| R1 · a claim | `a/b.py#f@11111111` | Read. | none |"
    ours = (
        "| R1 · a claim | `a/b.py#f@11111111` "
        "| Read. Corrected 2026-09-21. | Corrected 2026-09-21. |"
    )
    theirs = (
        "| R1 · a claim | `a/b.py#f@11111111` | Read. Corrected 2026-09-21. | none |"
    )
    got = "| R1 · a claim | `a/b.py#f@11111111` | Read. | none |"
    root, start, head = merged(
        tmp_path, ledger(base), ledger(ours), ledger(theirs), ledger(got)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    ours_sha = run(root, "rev-parse", head + "^1").stdout.strip()
    assert f"from parent {ours_sha[:7]}" in out, out


def test_a_tie_falls_to_the_first_parent(tmp_path):
    """The other half of the sentence the case above pins, and the half that
    runs in the common case: every marker older than the fork is carried by
    BOTH parents, so both lose the same count of it and the choice is a tie.

    Ledger row C9's Notes and `examine`'s comment both say ties fall to the
    first parent -- the side the person resolving the conflict had checked
    out -- and nothing held it, so rebuilding `carried` in any other order
    would change the SHA a reader is sent to open while the whole module
    stayed green (`agent-contract` §14). Issue #471.
    """
    base = "| R1 · a claim | `a/b.py#f@11111111` | Read. | none |"
    ours = "| R1 · a claim | `a/b.py#f@11111111` | Read. Corrected 2026-09-21. | ours |"
    theirs = (
        "| R1 · a claim | `a/b.py#f@11111111` | Read. Corrected 2026-09-21. | theirs |"
    )
    got = "| R1 · a claim | `a/b.py#f@11111111` | Read. | merged |"
    root, start, head = merged(
        tmp_path, ledger(base), ledger(ours), ledger(theirs), ledger(got)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    first = run(root, "rev-parse", head + "^1").stdout.strip()
    second = run(root, "rev-parse", head + "^2").stdout.strip()
    assert f"from parent {first[:7]}" in out, out
    assert f"from parent {second[:7]}" not in out, out
    assert "1 correction marker(s)" in out, out


# --- the census over the real corpus (#469) --------------------------------

# The instrument, and it is deliberately NOT `cc.MARKER`.
#
# For every `Corrected` or `Re-read` in a ledger file, find the next date on
# the same line and read what lies between. A gap made only of lowercase words
# is a candidate marker site. Nothing here is bounded, which is the whole
# point: a census taken with the pattern under test cannot see a spelling that
# pattern misses, and that is how the bound came out one short twice -- round
# 1's finding 1 of #424 measured one side of the date only, and round 2's
# finding 6 re-measured with the widened pattern itself.
#
# **The walk is verb by verb rather than one expression over the file, and
# that is not a style choice.** A single `verb ... date` pattern consumes
# everything between the two, so a first verb whose gap is NOT a lowercase run
# swallows a second verb standing before the date, and that second site is
# never examined. Measured while this case was being written: over the same
# file, the consuming form found two candidate sites FEWER than `MARKER`
# matched. The census meant to be the wider instrument was the narrower one,
# which is round 1's mistake arriving by a third route. The difference is
# stated rather than the two totals, because a total over this corpus is stale
# the next time anybody records a correction -- which is #470 itself.
VERB = re.compile(r"\b(" + "|".join(cc.VERBS) + r")\b")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}(?!\d)")
LOWERCASE_RUN = re.compile(r"^(?:[ \t]+[a-z][a-z-]*)*[ \t]+$")


def ledger_text(path, from_index=False):
    """One ledger file's text, from the worktree or from the index.

    `git ls-files` reads the **index**, so a path it lists can be missing from
    disk -- which is exactly what a release looks like between
    `fold_ledger.py` removing the fragments and `git add` staging the
    removal. Reading the worktree blindly raised `FileNotFoundError` here,
    out of the corpus reader and before either of the census case's guards
    could run. This repository has already paid for the same class once: an
    unstaged deletion against an index-reading command cost a ten-minute run
    during a release.

    The worktree wins where it has the file, because somebody running this
    after editing a ledger should be told about the edit rather than about
    what happens to be staged. The index is the fallback, and it is the blob
    `git ls-files` just listed, so the listing and the content come from one
    place in the case that used to crash.

    **Which route to take is decided by `conftest.on_disk` in the caller, not
    here.** This used to ask `pathlib.Path.exists()` for itself, and that is a
    bespoke copy of the shared predicate which gets one tree state wrong:
    `exists()` is true of a DIRECTORY, so a tracked path that is now a
    directory took the worktree route and `read_text` raised
    `IsADirectoryError` -- the same crash class one state over from the one
    this function was written for. `on_disk` asks `os.path.isfile`.
    """
    if not from_index:
        return pathlib.Path(ROOT, path).read_text(encoding="utf-8")
    return subprocess.run(
        ["git", "-C", ROOT, "show", f":{path}"],
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout


def ledger_corpus():
    """`{path: text}` for every ledger file the check watches.

    Read through the module's own `LEDGER`, `FRAGMENTS` and `RELEASES` rather
    than a list written here, because a hard-coded list goes blind exactly
    when the fragments are folded at a release -- into the shared file until
    #547, into that release's own file since -- which `fold_ledger.py` did at
    0.12.2, leaving `seal/ledger/` an empty glob in this tree. Tracked files
    only, which is what `ledger_listing` reads through `git ls-tree` at each
    commit.

    **The listing is split by `conftest.on_disk`**, the predicate five other
    helpers in this suite share, and
    `tests/test_a_shrunken_corpus_declines_to_judge.py` re-enumerates every
    scope that derives a path list from git so that this one cannot drift out
    of the class by being forgotten. What this caller does with the missing
    half is its own decision and it is neither of the two that module
    describes: it does not skip them, which would shrink the corpus the census
    is taken over without a word, and it does not decline, because it has
    somewhere true to read them from. It reads them out of the index entry
    `git ls-files` just named, so the corpus stays whole in the one tree state
    that used to truncate it.
    """
    listed = subprocess.run(
        [
            "git",
            "-C",
            ROOT,
            "ls-files",
            "-z",
            "--",
            cc.LEDGER,
            cc.FRAGMENTS,
            cc.RELEASES,
        ],
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout
    paths = [p for p in listed.split("\0") if p.endswith(".md")]
    present, missing = on_disk(ROOT, paths)
    corpus = {p: ledger_text(p) for p in present}
    corpus.update({p: ledger_text(p, from_index=True) for p in missing})
    return corpus


def candidate_sites(text):
    """`(offset, verb, date, words)` for every candidate marker site."""
    found = []
    for verb in VERB.finditer(text):
        stop = text.find("\n", verb.end())
        tail = text[verb.end() : stop if stop != -1 else len(text)]
        date = DATE.search(tail)
        if date is None:
            continue
        gap = tail[: date.start()]
        if not LOWERCASE_RUN.match(gap):
            continue
        found.append((verb.start(), verb.group(1), date.group(0), gap.split()))
    return found


def site_row(text, offset):
    """The ledger row the site sits on, or a note that it sits in prose."""
    start = text.rfind("\n", 0, offset) + 1
    stop = text.find("\n", offset)
    line = text[start : stop if stop != -1 else len(text)].strip()
    if line.startswith("|") and not cc.SEPARATOR.match(line):
        return cc.Row(line).key
    return "(prose, outside any row)"


def test_the_bound_covers_every_candidate_marker_site_the_corpus_carries():
    """#469. The bound on `MARKER`'s qualifier has been wrong twice, and each
    repair pinned one more literal spelling -- so an eleventh spelling would
    be invisible again with every case still green, because no case asked the
    question the bound is an answer to.

    This asks it, and it asserts a PROPERTY and no count: every candidate
    marker site the unbounded census finds is one `MARKER` also sees. A number
    over this corpus is the defect #470 reports -- the corpus moves whenever a
    release folds fragments in or a branch records a correction, this branch
    included -- and a case asserting one would go red for legitimate work.

    **How the census is taken, because a third circular one is the specific
    thing #469 exists to prevent**: verb by verb, the next date on the same
    line, and the gap between them read with no bound at all. The instrument
    cannot be `MARKER`, because an instrument that cannot see what it is being
    calibrated against agrees with the mistake -- which is what happened when
    round 1's census was taken with the widened pattern itself. Narrowing the
    bound to four reddens this case; narrowing the bound to four AND taking
    the census with `MARKER` leaves it green, which is that circularity
    demonstrated rather than asserted.

    **When the corpus grows a longer run this goes red**, naming the file, the
    row, the run length and the spelling. That is deliberate and it is not a
    false refusal to be softened: a warning or a skip is a green that means
    nothing, which is the hole this case exists to close. The answer is to
    open the named row, judge whether the run is a qualifier, and raise the
    bound with this case re-driven.
    """
    # The `row` clause of the failure message below, pinned. It reaches a
    # reader only through a message no standing case builds, so without these
    # two lines `site_row` can be edited away with the module still green --
    # measured: replacing its whole body with `return ""` left 50 passed.
    # Two asserts rather than a case, because A11 bounds the number of cases
    # in this module and not the number of things a case establishes.
    on_a_row = "| R1 · a claim | `a/b.py#f@11111111` | Re-read 2026-09-05. | n |"
    assert site_row(on_a_row, on_a_row.index("Re-read")) == cc.Row(on_a_row).key
    assert site_row("Re-read 2026-09-05.", 0) == "(prose, outside any row)"

    # The index route of the corpus reader, pinned. `git ls-files` lists what
    # the INDEX holds, so a listed path can be gone from disk -- a release
    # between `fold_ledger.py`'s removal and `git add` is exactly that -- and
    # reading the worktree blindly raised `FileNotFoundError` here before
    # either guard below ran. Pinned on a path that IS present, because the
    # branch that must not rot is the one nothing else reaches; asserting the
    # two routes agree would instead go red for anyone with an edited ledger.
    assert candidate_sites(ledger_text(cc.LEDGER, from_index=True)), (
        "the staged blob of the shared ledger carries no candidate marker "
        "site, so the fallback that keeps a release fold from crashing this "
        "case is not returning a ledger"
    )

    corpus = ledger_corpus()
    assert corpus, (
        "no ledger file was found through `correction_check.LEDGER` and "
        "`FRAGMENTS`. An empty corpus makes this case vacuous, which is the "
        "hole it exists to close, so it refuses rather than passing"
    )
    unseen, total = [], 0
    for path, text in sorted(corpus.items()):
        for offset, verb, date, words in candidate_sites(text):
            total += 1
            seen = cc.MARKER.match(text, offset)
            if seen is not None and (seen.group(1), seen.group(2)) == (verb, date):
                continue
            unseen.append(
                f"{path}: a run of {len(words)} lowercase word(s) between the "
                f"verb and the date, which `MARKER` does not read as a marker "
                f"-- `{verb} {' '.join(words)} {date}`, on row "
                f"{site_row(text, offset)!r}"
            )
    assert total, (
        "the corpus carries no candidate marker site at all, so this case "
        "proved nothing. Either `correction_check.VERBS` moved or the corpus "
        "did, and both are reasons to look rather than to pass"
    )
    assert not unseen, (
        f"{len(unseen)} of {total} candidate marker site(s) fall outside the "
        "bound on `MARKER`'s qualifier. Open each row, judge whether the run "
        "is a qualifier, and raise the bound deliberately with this case "
        "re-driven:\n  " + "\n  ".join(unseen)
    )
