"""A signatory's CI prints its pact and verifies nothing about it (#647, A).

#647's decision 2: there is no CI token, so a signatory's pull request can
read only its own repository. `chain_check.py` therefore prints the
relationship its `seal/config.md` records -- the pact's repository, the
notify value, how many pact anchors the declared work item's `spec.md`
carries -- and says that `pact-check`, run at the pact's repository, is where
the reconciliation runs. **No exit status moves on any of it**: a row that
will not parse and an anchor naming an undeclared pact are notices too
(S5 and S6 of the work item's `spec.md`).

Every case builds the same tree twice, once with the pact and once without,
and compares the two exit statuses: the claim is *does not move*, which a
fixed expected code could satisfy by accident.
"""

import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
ITEM = "seal/specs/1787700000-a-work-item"
PACT_URL = "git@example.com:org/orders-api.git"
ANCHOR = 'pact:orders-api/"## Order response shape / ### Fields"@1a2b3c4d'
NOT_HERE = (
    "This CI reads no other repository, so nothing here verifies it: "
    "`pact-check`, run at the pact's repository, is where the reconciliation "
    "runs"
)


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


def config(*rows):
    return "# config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n" + "".join(
        f"| {item} | {value} |\n" for item, value in rows
    )


DECLARATION = (
    "# 1787700000-a-work-item — routing\n\n"
    "| Axis | Answer |\n|---|---|\n"
    "| Review | through the review chain |\n"
    "| Destination | open the pull request |\n"
    "| Branch | feature |\n"
)


def record(sha, passed):
    box = "x" if passed else " "
    return (
        "# round 1\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n"
        "| Fixes checked by | nobody — the run ended here |\n\n"
        f"- [{box}] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        "| 🔴 1 | something | `f.py:1` | fixed | grounds |\n"
    )


def tree(tmp_path, name, config_text, spec, passed=True, declare=True, pact=None):
    """A repository on `feature` off `base`; DECLARE adds a chain declaration
    with one round record, PASSED or not; SPEC is its `spec.md`."""
    repo = tmp_path / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", "base")
    write(repo, "f.py", "x = 1\n")
    commit(repo, "base")
    git(repo, "switch", "-qc", "feature")
    if config_text is not None:
        write(repo, "seal/config.md", config_text)
    if pact is not None:
        write(repo, "seal/pact.md", pact)
    if declare:
        write(repo, f"{ITEM}/routing.md", DECLARATION)
        write(repo, f"{ITEM}/spec.md", spec)
        sha = commit(repo, "declare")
        write(repo, f"{ITEM}/rounds/round-1.md", record(sha, passed))
    else:
        write(repo, "g.py", "y = 2\n")
    commit(repo, "work")
    return repo


def run(repo):
    env = dict(os.environ)
    env.pop("GITHUB_HEAD_REF", None)
    event = repo.parent / f"{repo.name}-event.json"
    event.write_text(json.dumps({"pull_request": {"draft": False}}), "utf-8")
    env["GITHUB_EVENT_PATH"] = str(event)
    done = subprocess.run(
        [sys.executable, CHECK, "--baseline", "base", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    return done.returncode, " ".join((done.stdout + done.stderr).split())


SPEC = f"# spec\n\n| Policy clause | What it fixes |\n|---|---|\n| `{ANCHOR}` | x |\n"


@pytest.mark.parametrize("passed", [True, False], ids=["passing", "failing"])
def test_a_signatory_prints_its_pact_and_its_exit_status_does_not_move(
    tmp_path, passed
):
    """S5. The printed sentence is pinned (§14), and the exit status is the
    one the same tree has with no `Pact` row, passing or failing."""
    two = SPEC + f"\nAnd again: `{ANCHOR}`.\n"
    signed = tree(tmp_path, "signed", config(("Pact", PACT_URL)), two, passed)
    plain = tree(tmp_path, "plain", config(), two, passed)
    code, out = run(signed)
    plain_code, plain_out = run(plain)
    assert code == plain_code == (0 if passed else 1), (out, plain_out)
    assert (
        f"this repository signs the pact held at {PACT_URL} (`Pact notify`: "
        "when the pact is touched). 2 pact anchors naming `orders-api` in "
        f"{ITEM}/spec.md. {NOT_HERE}"
    ) in out, out
    assert "signs the pact" not in plain_out, plain_out


def test_a_pull_request_declaring_nothing_still_prints_the_pact(tmp_path):
    """The relationship is a fact about the tree, so it is printed before
    the early return a pull request with no declaration takes."""
    signed = tree(tmp_path, "signed", config(("Pact", PACT_URL)), None, declare=False)
    code, out = run(signed)
    plain_code, _ = run(tree(tmp_path, "plain", config(), None, declare=False))
    assert code == plain_code == 0, out
    assert (
        "0 pact anchors naming `orders-api` in no declared work item's "
        "spec.md, since this pull request declares none"
    ) in out, out


@pytest.mark.parametrize(
    "rows, said",
    [
        (
            [("Pact", "orders-api")],
            "a `Pact` row this CI does not verify: `orders-api` is not a remote URL",
        ),
        (
            [("Pact", PACT_URL), ("Pact notify", "sometimes")],
            "a `Pact` row this CI does not verify: `Pact notify | sometimes` "
            "is not one of `always`, `when the pact is touched`, `never`",
        ),
        (
            [("Pact", PACT_URL), ("Pact notify", "never"), ("Pact notify", "always")],
            "(`Pact notify`: a value that will not parse)",
        ),
    ],
    ids=["not a url", "notify outside the vocabulary", "notify written twice"],
)
def test_a_row_that_will_not_parse_is_a_notice_and_never_a_failure(
    tmp_path, rows, said
):
    """S6. The strict reading of the same rows is `pact-check`'s."""
    signed = tree(tmp_path, "signed", config(*rows), SPEC)
    code, out = run(signed)
    plain_code, _ = run(tree(tmp_path, "plain", config(), SPEC))
    assert code == plain_code == 0, out
    assert said in out, out
    assert "`pact-check` at the pact's repository exits 2 on it" in out, out


def test_s11_a_notify_row_below_the_table_is_a_notice_naming_it(tmp_path):
    """S11 of #759. A `Pact notify` row the table walk does not reach is
    refused by the reader; here that is a notice carrying the sentence, the
    notify prints as no value, and the exit status does not move."""
    rows = config(("Pact", PACT_URL)) + "\n| Pact notify | always |\n"
    code, out = run(tree(tmp_path, "signed", rows, SPEC))
    plain_code, _ = run(tree(tmp_path, "plain", config(), SPEC))
    assert code == plain_code == 0, out
    assert (
        "a `Pact` row this CI does not verify: `| Pact notify | always |` is "
        "shaped as a `Pact notify` row and is not read as one, because it "
        "stands outside the `| Item | Value |` table, spells the item another "
        "way, or holds a character that cuts the line. Write it as "
        "`| Pact notify | … |` inside that table. Printed rather than refused"
    ) in out, out
    assert "(`Pact notify`: a value that will not parse)" in out, out


def test_an_anchor_naming_an_undeclared_pact_is_a_notice(tmp_path):
    """S6. A spec citing a pact no `Pact` row names is printed, not
    refused."""
    spec = SPEC.replace("pact:orders-api/", "pact:billing/")
    signed = tree(tmp_path, "signed", config(("Pact", PACT_URL)), spec)
    code, out = run(signed)
    plain_code, _ = run(tree(tmp_path, "plain", config(), spec))
    assert code == plain_code == 0, out
    assert (
        "cites `pact:billing/…`, and no `Pact` row in seal/config.md names a "
        "pact called `billing`"
    ) in out, out


def test_the_pacts_repository_prints_how_many_signatories_it_lists(tmp_path):
    """Where the repository holds `seal/pact.md`, the count of the pact's
    `Signatory` table, and still nothing compared."""
    pact = (
        "# Pact\n\n| Signatory |\n|---|\n"
        "| git@example.com:org/orders-web.git |\n"
        "| https://example.com/org/billing |\n\n## Order response shape\n\nx\n"
    )
    held = tree(tmp_path, "held", config(), SPEC, pact=pact)
    code, out = run(held)
    plain_code, _ = run(tree(tmp_path, "plain", config(), SPEC))
    assert code == plain_code == 0, out
    assert (
        "this repository holds the pact, which lists 2 signatories. This CI "
        "reads no other repository, so nothing here compares them with it"
    ) in out, out
