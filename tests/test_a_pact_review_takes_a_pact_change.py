"""`pact-check` reads a signatory's pact changes, and a pact review takes them (#647, D).

A signatory's re-read records a pact change in
`seal/pact-changes/<work-item-id>.md` (`tests/test_a_signatory_records_a_
pact_change.py`). At the pact's repository `pact-check` reads every such
record, following the signatory's `Pact notify` as read now, and reports a row
citing a clause of this pact as `NOT TAKEN` until a row of a pact review,
`seal/pact-reviews/<work-item-id>.md`, names the signatory and the record at
its current content hash. S12-S17 of the work item's `spec.md`.

The two repositories are `test_pact_check.py`'s `world`; each record here is
written by the signatory's own `evidence-check --reverify`, so the format read
is the format written.
"""

import os
import subprocess
import sys

import pytest
from test_pact_check import (
    LOCATOR,
    PACT_URL,
    SIGNATORY_URL,
    V1,
    V2,
    checker,
    clause,
    commit,
    config,
    make_world,
    pact,
    run,
    write,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVIDENCE = os.path.join(
    ROOT, "skills", "evidence-check", "scripts", "evidence_check.py"
)
ITEM = "1791020000-a-field-is-added"
SOURCE = "def serialize(order):\n    return {'id': order.id}\n"


def unit_hash(repo):
    text = (repo / "src" / "orders.py").read_text(encoding="utf-8")
    places, _ = checker.resolve_unit("src/orders.py", "serialize", text)
    a, b = places[0]
    return checker.content_hash(checker.gfm_lines(text)[a - 1 : b])


def record(world, cites=V2, label="O1", step=1):
    """Have the signatory's re-read record one pact change, citing the clause
    at CITES' hash (None: no clause), and return (the anchor, the record's
    content hash)."""
    web = world["web"]
    write(web, "src/orders.py", SOURCE.replace("order.id", f"order.id + {step - 1}"))
    old = unit_hash(web)
    anchor = f"pact:orders-api/{LOCATOR}@{clause(cites)}" if cites else None
    grounds = (f"`{anchor}`, " if anchor else "") + f"`src/orders.py#serialize@{old}`"
    write(
        web,
        f"seal/ledger/{ITEM}.md",
        f"| {label} · the field list | {grounds} | read | 2026-09-01 | |\n",
    )
    write(web, "src/orders.py", SOURCE.replace("order.id", f"order.id + {step}"))
    done = subprocess.run(
        [
            sys.executable,
            EVIDENCE,
            "--reverify",
            "--into",
            f"seal/ledger/{ITEM}.md",
            "--checked",
            "2026-09-04",
            str(web),
        ],
        cwd=str(web),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert "recorded" in done.stdout, done.stdout + done.stderr
    text = (web / "seal" / "pact-changes" / f"{ITEM}.md").read_text(encoding="utf-8")
    return anchor, checker.content_hash(checker.gfm_lines(text))


def notify(world, value):
    write(
        world["web"],
        "seal/config.md",
        config(("Pact", PACT_URL), ("Pact notify", value)),
    )


def review(world, *rows, name="1791030000-the-pact-review"):
    body = "".join(f"| {s} | {c} | {v} |\n" for s, c, v in rows)
    write(
        world["api"],
        f"seal/pact-reviews/{name}.md",
        f"# Pact review\n\n| Signatory | Change | Verdict |\n|---|---|---|\n{body}",
    )


RECORD = f"seal/pact-changes/{ITEM}.md"


def pact_with(other):
    """The pact at v2, listing the signatory and OTHER."""
    return pact(V2, (SIGNATORY_URL, other))


@pytest.fixture
def world(tmp_path):
    return make_world(tmp_path)


def test_s12_an_untaken_pact_change_is_not_taken(world):
    """S12. The line names the signatory, the record and line, the clause,
    the work item and the record's hash, and the exit is 1."""
    anchor, digest = record(world)
    code, out = run(world)
    assert code == 1, out
    assert (
        f"NOT TAKEN {SIGNATORY_URL} {RECORD}:7 {anchor} — the pact has not taken "
        f"work item {ITEM}'s pact change: a pact review here takes it with a row "
        f"naming the signatory and `{ITEM}@{digest}`"
    ) in out, out
    assert "1 pact change read, 0 taken" in out, out
    assert "· 1 pact change read · 0 taken" in out, out


def test_s13_a_row_citing_no_clause_is_noted_under_always(world):
    """S13. Under `always` a `—` row is `NOTED`, and the exit stays 0."""
    notify(world, "always")
    _anchor, digest = record(world, cites=None)
    code, out = run(world)
    assert code == 0, out
    assert (
        f"NOTED {SIGNATORY_URL} {RECORD}:7 — work item {ITEM} recorded a change to "
        "code that cites no clause (`Pact notify`: always); it reads noted until "
        f"a pact review here takes `{ITEM}@{digest}`"
    ) in out, out


def test_s13_a_row_citing_no_clause_is_not_read_when_the_pact_is_touched(world):
    """S13. Recorded under `always`, read after the signatory went back to
    the default: the `—` row is not read."""
    notify(world, "always")
    record(world, cites=None)
    notify(world, "when the pact is touched")
    code, out = run(world)
    assert code == 0, out
    assert "NOTED" not in out and "0 pact changes read, 0 taken" in out, out


def test_s13_under_never_no_row_is_read(world):
    """S13. Recorded, then the signatory said `never`: nothing is read."""
    record(world)
    notify(world, "never")
    code, out = run(world)
    assert code == 0, out
    assert "NOT TAKEN" not in out and "0 pact changes read, 0 taken" in out, out


def test_s14_a_pact_review_at_the_current_hash_takes_it(world):
    """S14. A row naming the signatory and `<id>@<current hash>`, `holds`."""
    _anchor, digest = record(world)
    review(world, (SIGNATORY_URL, f"{ITEM}@{digest}", "holds"))
    code, out = run(world)
    assert code == 0, out
    assert "1 pact change read, 1 taken" in out, out
    assert "· 1 pact change read · 1 taken" in out, out


def test_s15_a_record_grown_after_its_review_is_not_taken_again(world):
    """S15. The record gained a row after the review: `NOT TAKEN` names the
    hash the review took and the hash the record holds now."""
    _anchor, first = record(world)
    review(world, (SIGNATORY_URL, f"{ITEM}@{first}", "holds"))
    anchor, now = record(world, label="O2", step=2)
    assert now != first
    code, out = run(world)
    assert code == 1, out
    assert (
        f"NOT TAKEN {SIGNATORY_URL} {RECORD}:8 {anchor} — a pact review took work "
        f"item {ITEM}'s record at @{first}, and it holds @{now} now: a pact review "
        f"here takes it again with `{ITEM}@{now}`"
    ) in out, out


REVIEWS = "seal/pact-reviews/1791030000-the-pact-review.md"


@pytest.mark.parametrize(
    "case",
    [
        "amended, the clause unmoved",
        "an unlisted signatory",
        "a record not held",
        "a verdict outside the two",
        "a change not written as one",
    ],
)
def test_s16_a_pact_review_row_that_cannot_be_true_is_refused(world, case):
    """S16. Each is `REFUSED` at exit 2, naming the review's file and line."""
    _anchor, digest = record(world)
    row, said = {
        "amended, the clause unmoved": (
            (SIGNATORY_URL, f"{ITEM}@{digest}", "amended"),
            f"the pact review says `amended` for work item {ITEM} from "
            f"{SIGNATORY_URL}, and the clause pact:orders-api/{LOCATOR}@{clause(V2)} "
            "still has the hash the record recorded: amend the clause, or say `holds`",
        ),
        "an unlisted signatory": (
            ("https://example.com/org/orders-mobile", f"{ITEM}@{digest}", "holds"),
            "the pact review names `https://example.com/org/orders-mobile`, which "
            "the pact's `Signatory` table does not list",
        ),
        "a record not held": (
            (SIGNATORY_URL, f"1791099999-another@{digest}", "holds"),
            f"the pact review takes `1791099999-another` from {SIGNATORY_URL}, "
            "which holds no seal/pact-changes/1791099999-another.md",
        ),
        "a verdict outside the two": (
            (SIGNATORY_URL, f"{ITEM}@{digest}", "breaks"),
            "the pact review's verdict `breaks` is neither `holds` nor `amended`",
        ),
        "a change not written as one": (
            (SIGNATORY_URL, ITEM, "holds"),
            f"the pact review's change `{ITEM}` is not written "
            "`<work-item-id>@<content hash>`, as `pact-check` prints it",
        ),
    }[case]
    review(world, row)
    code, out = run(world)
    assert code == 2, out
    assert f"REFUSED {REVIEWS}:5 — {said}" in out, out


def test_s16_amended_is_taken_where_the_clause_moved(world):
    """The other side of the `amended` refusal: the record cites v1, the
    pact amended the clause to v2, so `amended` can be true."""
    _anchor, digest = record(world, cites=V1)
    review(world, (SIGNATORY_URL, f"{ITEM}@{digest}", "amended"))
    _code, out = run(world)
    assert "REFUSED" not in out, out
    assert "1 pact change read, 1 taken" in out, out


def test_s17_a_record_that_will_not_read_or_parse_is_exit_2(world):
    """S17, the signatory's side."""
    write(
        world["web"],
        "seal/pact-changes/1791020001-x.md",
        "| Clause | Row | Code | Checked |\n|---|---|---|---|\n| a | b | c | soon |\n",
    )
    (world["web"] / "seal" / "pact-changes" / "1791020002-y.md").mkdir()
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {SIGNATORY_URL} seal/pact-changes/1791020001-x.md — the record "
        "has a row at line 3 whose `Checked` is `soon`, not a date written YYYY-MM-DD"
    ) in out, out
    assert (
        f"REFUSED {SIGNATORY_URL} seal/pact-changes/1791020001-x.md:3 — the "
        "record's `Clause` cell"
    ) not in out, out
    assert (
        f"UNREADABLE {SIGNATORY_URL} seal/pact-changes/1791020002-y.md — the "
        "record of pact changes could not be read"
    ) in out, out


def test_s17_a_review_that_will_not_read_or_parse_is_exit_2(world):
    """S17, the pact's side."""
    write(
        world["api"],
        "seal/pact-reviews/1791030001-a.md",
        "| Signatory | Change |\n|---|---|\n",
    )
    (world["api"] / "seal" / "pact-reviews" / "1791030002-b.md").mkdir()
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact-reviews/1791030001-a.md — the record holds no "
        "`| Signatory | Change | Verdict |` table"
    ) in out, out
    assert (
        "UNREADABLE seal/pact-reviews/1791030002-b.md — the pact review could not "
        "be read"
    ) in out, out


def test_a_clause_cell_that_is_neither_is_refused(world):
    write(
        world["web"],
        "seal/pact-changes/1791020001-x.md",
        "| Clause | Row | Code | Checked |\n|---|---|---|---|\n| a clause | b | c | 2026-09-04 |\n",
    )
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {SIGNATORY_URL} seal/pact-changes/1791020001-x.md:3 — the "
        "record's `Clause` cell `a clause` is neither a pact anchor nor `—`"
    ) in out, out


def test_a_review_of_another_signatory_takes_nothing_here(world):
    """A pact review row naming another signatory, at this record's very id
    and hash, does not take this signatory's record."""
    _anchor, digest = record(world)
    mobile = "https://example.com/org/orders-mobile"
    write(world["api"], "seal/pact.md", pact_with(mobile))
    commit(world["api"], "a second signatory")
    review(world, (mobile, f"{ITEM}@{digest}", "holds"))
    code, out = run(world)
    assert code == 1, out
    assert f"NOT TAKEN {SIGNATORY_URL} {RECORD}:7" in out, out
    assert "1 pact change read, 0 taken" in out, out


def test_a_review_of_another_record_takes_nothing_here(world):
    """Two records; a review takes the first. The second is not taken, and
    its line says it was never reviewed, not that it grew."""
    _anchor, first = record(world)
    later = "1791020001-a-later-item"
    (world["web"] / "seal" / "pact-changes" / f"{ITEM}.md").rename(
        world["web"] / "seal" / "pact-changes" / f"{later}.md"
    )
    _anchor, _ = record(world, step=2)
    review(world, (SIGNATORY_URL, f"{later}@{first}", "holds"))
    code, out = run(world)
    assert code == 1, out
    assert (
        f"NOT TAKEN {SIGNATORY_URL} {RECORD}:7 pact:orders-api/{LOCATOR}@"
        f"{clause(V2)} — the pact has not taken work item {ITEM}'s pact change"
    ) in out, out


def test_a_row_citing_another_pact_is_not_this_pacts(world):
    """A signatory of two pacts records changes under both; a row citing
    only the other pact is neither read nor refused here."""
    write(
        world["web"],
        f"seal/pact-changes/{ITEM}.md",
        "| Clause | Row | Code | Checked |\n|---|---|---|---|\n"
        '| pact:billing/"## Invoices"@5e6f7a8b | seal/ledger/x.md · B1 | `a.py#f@1` '
        "BROKEN | 2026-09-04 |\n",
    )
    code, out = run(world)
    assert code == 0, out
    assert "0 pact changes read, 0 taken" in out, out


def test_an_amended_review_at_an_older_hash_is_not_judged_again(world):
    """An `amended` that was true at the hash it took stays true after the
    record grows with a row citing the amended clause (round 1, yellow 3)."""
    _anchor, first = record(world, cites=V1)
    _anchor, now = record(world, cites=V2, label="O2", step=2)
    review(
        world,
        (SIGNATORY_URL, f"{ITEM}@{first}", "amended"),
        (SIGNATORY_URL, f"{ITEM}@{now}", "holds"),
    )
    code, out = run(world)
    assert code == 0, out
    assert "REFUSED" not in out, out
    assert "2 pact changes read, 2 taken" in out, out


def test_a_review_row_naming_a_signatory_since_dropped_stays_refused(world):
    """A pact review record is permanent, so a row naming a signatory the
    pact has since taken out of its `Signatory` table is refused at exit 2,
    as a typo would be: the two are the same text (round 1, white 7). The
    policy says to take such rows out with the signatory, in one change."""
    _anchor, digest = record(world)
    review(world, (SIGNATORY_URL, f"{ITEM}@{digest}", "holds"))
    code, out = run(world)
    assert code == 0, out
    mobile = "https://example.com/org/orders-mobile"
    write(world["api"], "seal/pact.md", pact(V2, (mobile,)))
    commit(world["api"], "orders-web leaves the pact")
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {REVIEWS}:5 — the pact review names `{SIGNATORY_URL}`, which "
        "the pact's `Signatory` table does not list"
    ) in out, out
