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
"""

import importlib.util
import io
import os
import pathlib
import subprocess

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

    The prose BEFORE the date varies too, in ten spellings across 39 of the
    file's 404 markers, and this case does not reach that — round 1's finding
    1, and `test_a_qualifier_between_the_verb_and_the_date_is_the_same_marker`
    below is where it is held."""
    found = cc.markers("Corrected 2026-09-15 by issue #98, and Re-read 2026-09-05.")
    assert found == {("Corrected", "2026-09-15"): 1, ("Re-read", "2026-09-05"): 1}


def test_both_verbs_count_because_re_read_is_the_common_one():
    """A2. Measured in the tree: 10 rows carry a `Corrected` marker and 185
    carry a `Re-read` — 404 marker occurrences on 190 rows, since a row can
    carry a marker in more than one cell. A check watching only the rare verb
    would have ignored every row the previous work item re-read."""
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
    cannot pass both. `Re-read` is the marker 185 rows of the shared file
    carry against `Corrected`'s 10."""
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
    """A4. `fold_ledger.py` moves every fragment into the shared file at the
    release, so a check watching only `seal/ledger.md` would go blind exactly
    when the rows become shared. Both are watched from the first commit."""
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
    """`seal/ledger.md` spells 39 of its 404 markers this way — `again` 19
    times, `and re-executed` 5, `a third time` 4, and seven more shapes — and
    one row carries no other spelling at all. A pattern demanding the date
    immediately after the verb watches neither that row nor a reword."""
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

    The longest qualifier the tree actually carries is five words (`and
    re-stamped a third time`, at `seal/ledger.md:1172`), and the bound is
    five — round 2's finding 6. This case is red
    the moment that bound stops being a bound."""
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
    """`seal/ledger.md:1172` spells five lowercase words between the verb and
    the date — `Re-read and re-stamped a third time <date>` — and the bound
    was four, so the file's own longest spelling was invisible to the check
    watching that file.

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
