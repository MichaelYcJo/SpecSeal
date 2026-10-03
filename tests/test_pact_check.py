"""`pact-check` reads every signatory from the pact's repository (#647, B).

Two temporary repositories side by side: the pact's repository, whose
`seal/pact.md` carries one clause committed as v1 and then v2 on `main`, with
v3 on a side branch HEAD does not hold; and a signatory, which names the pact
in its `seal/config.md` and cites the clause from a ledger fragment. `HOME`
is a temporary directory, so the machine-local map is whatever a case writes
there. S3 and S8-S12 of the work item's `spec.md`.
"""

import importlib.util
import io
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "pact_check.py")
WRAPPER = os.path.join(ROOT, "bin", "pact-check")

PACT_URL = "git@example.com:org/orders-api.git"
SIGNATORY_URL = "https://example.com/org/orders-web"
LOCATOR = '"## Order response shape / ### Fields"'


def load():
    spec = importlib.util.spec_from_file_location("pact_check_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pc = load()
checker = pc.load(pc.CHECKER, "evidence_for_pact_tests")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    ).stdout


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
    return git(repo, "rev-parse", "HEAD").strip()


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def pact(fields, signatories=(SIGNATORY_URL,)):
    rows = "".join(f"| {s} |\n" for s in signatories)
    return (
        "# Pact\n\n| Signatory |\n|---|\n"
        + rows
        + f"\n## Order response shape\n\n### Fields\n\n{fields}\n\n## Errors\n\nx\n"
    )


V1, V2, V3 = "id, total", "id, total, currency", "id, total, currency, tax"


def clause(fields):
    digest, why = pc.clause_hash(checker, pact(fields), LOCATOR)
    assert why is None
    return digest


def config(*rows):
    return "# config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n" + "".join(
        f"| {item} | {value} |\n" for item, value in rows
    )


def ledger_row(anchor):
    return (
        f"| S1 · the field list | `{anchor}`, `src/a.py#f@00000000` | read | "
        "2026-10-03 | |\n"
    )


@pytest.fixture
def world(tmp_path):
    """The pact's repository and the signatory as siblings under `work/`,
    and an empty HOME."""
    work = tmp_path / "work"
    home = tmp_path / "home"
    home.mkdir()
    api = work / "orders-api"
    api.mkdir(parents=True)
    git(api, "init", "-q", "-b", "main")
    git(api, "remote", "add", "origin", PACT_URL)
    write(api, "seal/pact.md", pact(V1))
    commit(api, "pact v1")
    write(api, "seal/pact.md", pact(V2))
    commit(api, "pact v2")
    git(api, "switch", "-qc", "side")
    write(api, "seal/pact.md", pact(V3))
    commit(api, "pact v3")
    git(api, "switch", "-q", "main")
    web = work / "orders-web"
    web.mkdir()
    git(web, "init", "-q", "-b", "main")
    git(web, "remote", "add", "origin", SIGNATORY_URL)
    write(web, "seal/config.md", config(("Pact", PACT_URL)))
    commit(web, "signatory")
    return {"api": api, "web": web, "home": home, "tmp": tmp_path}


def cite(world, digest, locator=LOCATOR, where="seal/ledger/1790000000-x.md"):
    anchor = f"pact:orders-api/{locator}@{digest}"
    write(world["web"], where, ledger_row(anchor))
    return anchor


def run(world, root=None):
    out = io.StringIO()
    code = pc.check(str(root or world["api"]), out=out, home_dir=str(world["home"]))
    return code, " ".join(out.getvalue().split())


def test_s12_a_signatory_citing_the_current_clause_is_clean(world):
    """S12. Every listed signatory resolves, names this repository, and
    cites the current hash: exit 0 and the summary line."""
    cite(world, clause(V2))
    write(
        world["web"],
        "seal/specs/1790000000-x/spec.md",
        f"| `pact:orders-api/{LOCATOR}@{clause(V2)}` | built against it |\n",
    )
    code, out = run(world)
    assert code == 0, out
    assert (
        f"READ {SIGNATORY_URL} {world['web']} — `Pact notify`: when the pact is "
        "touched; 2 pact anchors naming `orders-api`"
    ) in out, out
    assert (
        "pact-check: the pact `orders-api` — 1 of 1 signatory read · 2 ok · 0 "
        "superseded · 0 not taken · 0 unmatched · 0 broken"
    ) in out, out


def test_s8_a_hash_from_heads_own_history_is_superseded(world):
    """S8. v1's hash, which `main` gave the clause before v2."""
    anchor = cite(world, clause(V1))
    code, out = run(world)
    assert code == 1, out
    assert (
        f"SUPERSEDED {SIGNATORY_URL} seal/ledger/1790000000-x.md:1 {anchor} — the "
        "signatory was built against a superseded clause"
    ) in out, out
    assert f"it reads @{clause(V2)} now" in out, out


def test_s9_a_hash_only_another_ref_holds_is_not_taken_and_names_it(world):
    """S9. v3 is on `side`, which HEAD does not hold."""
    anchor = cite(world, clause(V3))
    code, out = run(world)
    assert code == 1, out
    assert (
        f"NOT TAKEN {SIGNATORY_URL} seal/ledger/1790000000-x.md:1 {anchor} — the "
        "pact has not taken the signatory's recorded change: this hash is the "
        "clause on side"
    ) in out, out


def test_s10_a_hash_no_commit_gave_is_unmatched(world):
    """S10, first half: exit 1."""
    cite(world, "deadbeef")
    code, out = run(world)
    assert code == 1, out
    assert "UNMATCHED " in out and "Read both sides" in out, out


def test_s10_a_heading_path_that_resolves_to_nothing_is_broken(world):
    """S10, second half: exit 2, and the verdict says what to do."""
    cite(world, clause(V2), locator='"## Order response shape / ### Gone"')
    code, out = run(world)
    assert code == 2, out
    assert (
        "BROKEN " in out
        and "the heading path resolves to no clause in the pact: the clause was "
        "renamed or removed. Re-coordinate the signatory"
        in out
    ), out


def test_s11_a_checkout_nowhere_on_this_machine_names_the_map_line(world):
    """S11, first half: not in the map and not a sibling, so exit 1 with the
    line to add."""
    moved = world["tmp"] / "elsewhere" / "orders-web"
    moved.parent.mkdir()
    world["web"].rename(moved)
    code, out = run(world)
    assert code == 1, out
    assert (
        f"NOT FOUND {SIGNATORY_URL} — no checkout of it was found on this "
        f"machine: add `| {SIGNATORY_URL} | <the path of its checkout> |` to "
        "~/.claude/specseal/pact-paths.md"
    ) in out, out
    # The map finds it, keyed by the URL compared normalised.
    write(
        world["home"],
        ".claude/specseal/pact-paths.md",
        f"| Remote | Path |\n|---|---|\n| git@example.com:org/orders-web.git | {moved} |\n",
    )
    world["web"] = moved
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 0, out


def test_s11_a_relationship_recorded_on_one_side_is_refused(world):
    """S11, second half: the pact lists the signatory and its config does
    not name the pact, so exit 2."""
    write(world["web"], "seal/config.md", config())
    code, out = run(world)
    assert code == 2, out
    assert (
        f"ONE-SIDED {SIGNATORY_URL} seal/config.md — the pact lists it, and its "
        f"config names no `Pact` row for {PACT_URL}: the relationship is "
        "recorded on one side only"
    ) in out, out


def test_s3_a_notify_value_outside_the_vocabulary_is_exit_2(world):
    """S3, the `pact-check` half: the reader's refusal, read strictly."""
    write(
        world["web"],
        "seal/config.md",
        config(("Pact", PACT_URL), ("Pact notify", "sometimes")),
    )
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {SIGNATORY_URL} seal/config.md — `Pact notify | sometimes` is "
        "not one of `always`, `when the pact is touched`, `never`"
    ) in out, out


def test_no_pact_here_and_no_origin_are_unusable_input(world):
    """Exit 2 for the two ways the pact's repository cannot be read."""
    code, out = run(world, root=world["web"])
    assert code == 2 and "holds no seal/pact.md" in out, out
    git(world["api"], "remote", "remove", "origin")
    code, out = run(world)
    assert code == 2 and "has no origin remote" in out, out


def test_an_anchor_naming_another_pact_is_not_read(world):
    """A signatory of two pacts cites the other one too; only this pact's
    name is graded here."""
    write(
        world["web"],
        "seal/ledger/1790000000-x.md",
        ledger_row(f"pact:billing/{LOCATOR}@deadbeef")
        + ledger_row(f"pact:orders-api/{LOCATOR}@{clause(V2)}"),
    )
    code, out = run(world)
    assert code == 0, out
    assert "1 ok" in out, out


def test_the_wrapper_runs_the_script_from_any_directory(world):
    """S14's command, run as a person types it."""
    if os.name == "nt":
        pytest.skip("the POSIX wrapper; bin/pact-check.cmd is its Windows twin")
    cite(world, clause(V2))
    env = {**os.environ, "HOME": str(world["home"])}
    done = subprocess.run(
        ["sh", WRAPPER, str(world["api"])],
        cwd=str(world["tmp"]),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert "1 ok" in done.stdout, done.stdout
    assert sys.executable  # the wrapper runs python3 from PATH, as the others do


def test_a_heading_path_naming_two_clauses_is_broken(world):
    """An ambiguous address is no address: BROKEN, naming the count."""
    text = pact(V2) + "\n## Order response shape\n\n### Fields\n\nagain\n"
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a second clause under one heading")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert "the heading path resolves to 2 clauses in the pact" in out, out


def test_two_siblings_with_the_signatorys_origin_are_not_guessed_between(world):
    """Nothing is guessed: two checkouts of one signatory, and no map line,
    is a signatory not found, with both named."""
    twin = world["web"].parent / "orders-web-2"
    twin.mkdir()
    git(twin, "init", "-q", "-b", "main")
    git(twin, "remote", "add", "origin", SIGNATORY_URL)
    code, out = run(world)
    assert code == 1, out
    assert "2 sibling directories have its origin" in out, out
    assert "nothing here guesses which" in out, out


def test_a_map_that_will_not_read_is_refused_rather_than_read_as_empty(world):
    """Read as empty, every signatory it names would be reported missing."""
    (world["home"] / ".claude" / "specseal" / "pact-paths.md").mkdir(parents=True)
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert "REFUSED ~/.claude/specseal/pact-paths.md — " in out, out
    assert "is there and could not be read" in out, out


def test_a_pact_under_local_mode_has_no_history_and_says_so(world):
    """Local mode: every mismatch reads UNMATCHED, said once in the
    summary."""
    api = world["api"]
    common = git(api, "rev-parse", "--git-common-dir").strip()
    local = os.path.join(str(api), common, "seal")
    os.makedirs(local)
    os.replace(str(api / "seal" / "pact.md"), os.path.join(local, "pact.md"))
    os.rmdir(str(api / "seal"))
    anchor = cite(world, clause(V1))
    code, out = run(world)
    assert code == 1, out
    assert f"UNMATCHED {SIGNATORY_URL} seal/ledger/1790000000-x.md:1 {anchor}" in out
    assert (
        "The pact sits under the git directory (local mode), so it has no "
        "history and every mismatch reads unmatched"
    ) in out, out


def test_a_map_line_naming_a_checkout_of_another_repository_is_not_trusted(world):
    """The map is keyed by URL and the checkout it names must have that
    origin; a stale line pointing elsewhere is a signatory not found."""
    other = world["tmp"] / "unrelated"
    other.mkdir()
    git(other, "init", "-q", "-b", "main")
    git(other, "remote", "add", "origin", "git@example.com:org/unrelated.git")
    write(
        world["home"],
        ".claude/specseal/pact-paths.md",
        f"| Remote | Path |\n|---|---|\n| {SIGNATORY_URL} | {other} |\n",
    )
    code, out = run(world)
    assert code == 1, out
    assert f"NOT FOUND {SIGNATORY_URL} — the map names {other}, whose origin is" in out


def test_an_anchor_quoted_in_a_closed_fence_is_an_example_and_not_graded(world):
    """A spec showing the anchor's shape in a code block cites nothing,
    the rule the ledger reader keeps for a fenced row."""
    write(
        world["web"],
        "seal/specs/1790000000-x/spec.md",
        f"```\npact:orders-api/{LOCATOR}@deadbeef\n```\n",
    )
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 0, out
    assert "1 ok · 0 superseded · 0 not taken · 0 unmatched" in out, out


def test_a_clause_a_merge_did_not_keep_is_still_heads_history(world):
    """Main held v2; a branch cut from v1 changed the clause, and the merge
    kept the branch's text. A signatory built against v2 is SUPERSEDED, not
    UNMATCHED: v2 is in HEAD's history, on the side git's default history
    simplification does not follow."""
    api = world["api"]
    git(api, "switch", "-qc", "early", "main~1")
    write(api, "seal/pact.md", pact("id, total, tax"))
    commit(api, "the clause, changed from v1")
    git(api, "switch", "-q", "main")
    git(api, "merge", "-q", "--no-ff", "-s", "ours", "--no-commit", "early")
    write(api, "seal/pact.md", pact("id, total, tax"))
    commit(api, "merge early, keeping its clause")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 1, out
    assert "SUPERSEDED" in out and "UNMATCHED " not in out, out


def test_a_signatory_row_the_table_walk_cannot_read_is_exit_2(world):
    """The row with no closing pipe is refused at the pact, so a signatory
    below it is never reported as clean by omission."""
    text = pact(V2).replace(
        f"| {SIGNATORY_URL} |\n",
        f"| {SIGNATORY_URL} |\n| https://example.com/org/orders-mobile\n",
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a row with no closing pipe")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signatory` table that stops at "
        "`| https://example.com/org/orders-mobile`"
    ) in out, out


@pytest.mark.parametrize(
    "anchor",
    [
        'pact:orders-api#"## Order response shape / ### Fields"@1a2b3c4d',
        "pact:orders-api/## Order response shape@1a2b3c4d",
        'pact:orders-api/"## Order response shape / ### Fields"',
    ],
    ids=["hash for slash", "no quotes", "no hash"],
)
def test_a_pact_anchor_that_does_not_parse_is_refused(world, anchor):
    """A mistyped citation is read by nobody else: not the signatory's own
    check, not chain-check. Here it is named and exit 2."""
    write(world["web"], "seal/ledger/1790000000-x.md", ledger_row(anchor))
    code, out = run(world)
    assert code == 2, out
    assert (f"REFUSED {SIGNATORY_URL} seal/ledger/1790000000-x.md:1 — `") in out, out
    assert (
        'does not parse as `pact:orders-api/"<heading path>"@<hash>`, so '
        "nothing grades it"
    ) in out, out


def test_a_signatory_with_no_seal_root_is_one_sided(world):
    """Without a root it cannot name the pact, and nothing is read from the
    directory the command happens to stand in."""
    import shutil

    shutil.rmtree(world["web"] / "seal")
    code, out = run(world)
    assert code == 2, out
    assert (
        f"ONE-SIDED {SIGNATORY_URL} {world['web']} — the pact lists it, and it "
        "has no seal/ root to name this pact in: the relationship is recorded "
        "on one side only"
    ) in out, out


def test_a_signatory_config_that_will_not_read_is_unreadable(world):
    (world["web"] / "seal" / "config.md").unlink()
    (world["web"] / "seal" / "config.md").mkdir()
    code, out = run(world)
    assert code == 2, out
    home = os.path.join(str(world["web"]), "seal")
    assert f"UNREADABLE {SIGNATORY_URL} {home}/config.md — could not be read" in out


def test_an_anchor_file_that_will_not_read_is_unreadable(world):
    (world["web"] / "seal" / "ledger" / "1790000000-x.md").mkdir(parents=True)
    code, out = run(world)
    assert code == 2, out
    assert (
        f"UNREADABLE {SIGNATORY_URL} seal/ledger/1790000000-x.md — could not be read"
    ) in out, out


def test_a_pact_that_will_not_read_is_unreadable(world):
    (world["api"] / "seal" / "pact.md").unlink()
    (world["api"] / "seal" / "pact.md").mkdir()
    code, out = run(world)
    assert code == 2, out
    pact_path = os.path.join(str(world["api"]), "seal", "pact.md")
    assert f"UNREADABLE {pact_path} — the pact could not be read" in out, out


def test_a_pact_listing_its_own_repository_says_so(world):
    """Not `NOT FOUND`, which would send a person looking for a checkout of
    the repository they stand in."""
    write(world["api"], "seal/pact.md", pact(V2, (SIGNATORY_URL, PACT_URL)))
    commit(world["api"], "the pact lists itself")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {PACT_URL} seal/pact.md — the pact lists its own repository; "
        "the `Signatory` table lists every OTHER signatory, so take this row out"
    ) in out, out
    assert "NOT FOUND" not in out, out


def test_a_signatory_row_below_a_blank_line_is_refused(world):
    """A blank line ends the table's walk; a row written below it is a
    signatory nobody reads, so it is refused rather than passed over."""
    text = pact(V2).replace(
        f"| {SIGNATORY_URL} |\n",
        f"| {SIGNATORY_URL} |\n\n| https://example.com/org/orders-mobile |\n",
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a blank line inside the table")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signatory` table that ends above "
        "`| https://example.com/org/orders-mobile |`, a row the walk never "
        "reaches — it and every signatory below it would go unread"
    ) in out, out
