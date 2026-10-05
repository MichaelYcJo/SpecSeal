"""`pact-check` reads every signer from the pact's repository (#647, B).

Two temporary repositories side by side: the pact's repository, whose
`seal/pact.md` carries one clause committed as v1 and then v2 on `main`, with
v3 on a side branch HEAD does not hold; and a signer, which names the pact
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
SIGNER_URL = "https://example.com/org/orders-web"
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


def pact(fields, signers=(SIGNER_URL,)):
    rows = "".join(f"| {s} |\n" for s in signers)
    return (
        "# Pact\n\n| Signer |\n|---|\n"
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
    """The pact's repository and the signer as siblings under `work/`,
    and an empty HOME."""
    return make_world(tmp_path)


def make_world(tmp_path):
    """`world`'s body, which `tests/test_a_pact_review_takes_a_pact_change.py`
    builds its own fixture from."""
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
    git(web, "remote", "add", "origin", SIGNER_URL)
    write(web, "seal/config.md", config(("Pact", PACT_URL)))
    commit(web, "signer")
    return {"api": api, "web": web, "home": home, "tmp": tmp_path}


def cite(world, digest, locator=LOCATOR, where="seal/ledger/1790000000-x.md"):
    anchor = f"pact:orders-api/{locator}@{digest}"
    write(world["web"], where, ledger_row(anchor))
    return anchor


def posix(path):
    """A path as `pact-check` prints one outside HOME: every separator `/`.
    Each case comparing a printed path compares this, so a Windows run
    holds the same sentence a POSIX one does."""
    return str(path).replace(os.sep, "/")


def run(world, root=None):
    out = io.StringIO()
    code = pc.check(str(root or world["api"]), out=out, home_dir=str(world["home"]))
    return code, " ".join(out.getvalue().split())


def test_s12_a_signer_citing_the_current_clause_is_clean(world):
    """S12. Every listed signer resolves, names this repository, and
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
        f"READ {SIGNER_URL} {posix(world['web'])} — `Pact notify`: when the pact is "
        "touched; 2 pact anchors naming `orders-api`"
    ) in out, out
    assert (
        "pact-check: the pact `orders-api` — 1 of 1 signer read · 2 ok · 0 "
        "superseded · 0 not taken · 0 unmatched · 0 broken"
    ) in out, out


# --- the header 0.18.x wrote (#822) ------------------------------------------
#
# A pact begun before 0.19.0 heads its table with the word the release
# renamed. It reads as one headed `Signer`, and one line names the rename;
# the exit is what the new header gives.

RENAME = (
    "pact-check: seal/pact.md heads its table `| Signatory |`, the word before "
    "0.19.0 — `| Signer |` is the header now; rename it when the file is next "
    "edited"
)


def old_header(text):
    return text.replace("| Signer |\n|---|", "| Signatory |\n|---|", 1)


def test_s1_a_pact_headed_signer_reads_with_no_word_of_a_rename(world):
    """S1 of #822. The header `templates/pact.md` now begins a pact with is
    read as the old one was, and nothing is said about a rename."""
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 0, out
    assert (
        f"READ {SIGNER_URL} {posix(world['web'])} — `Pact notify`: when the pact "
        "is touched; 1 pact anchor naming `orders-api`"
    ) in out, out
    assert "heads its table" not in out and "Signatory" not in out, out


def test_s2_a_pact_headed_as_0_18_wrote_it_reads_the_same_and_names_it(world):
    """S2 of #822. The same pact headed `| Signatory |` reads identically,
    one line before its `READ` line names the file, both headers and the
    release, and the exit is the new header's."""
    cite(world, clause(V2))
    new_code, new_out = run(world)
    write(world["api"], "seal/pact.md", old_header(pact(V2)))
    commit(world["api"], "the pact as 0.18.0 began it")
    code, out = run(world)
    assert code == new_code == 0, (out, new_out)
    assert out.count(RENAME) == 1, out
    read = f"READ {SIGNER_URL} {posix(world['web'])}"
    assert read in out and out.index(RENAME) < out.index(read), out
    assert out.replace(RENAME + " ", "") == new_out, (out, new_out)


def test_s2_a_broken_table_under_the_old_header_is_refused_naming_it(world):
    """The refusal names the header the walk was asked for, so a table
    under the old header that will not read says `Signatory`, beside the
    rename line; the exit is the refusal's."""
    text = old_header(pact(V2)).replace(
        f"| {SIGNER_URL} |\n",
        f"| {SIGNER_URL} |\n| https://example.com/org/orders-mobile\n",
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "an old header over a row with no closing pipe")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert RENAME in out, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signatory` table that stops at "
        "`| https://example.com/org/orders-mobile`"
    ) in out, out


def test_s2_a_refusal_naming_the_table_names_the_header_the_pact_holds(world):
    """`pact-check`'s own sentences about the pact's table call it by the
    header the pact holds, so a person told to edit the table finds it."""
    write(world["api"], "seal/pact.md", old_header(pact(V2, (SIGNER_URL, PACT_URL))))
    commit(world["api"], "an old pact lists itself")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {PACT_URL} seal/pact.md — the pact lists its own repository; "
        "the `Signatory` table lists every OTHER signer, so take this row out"
    ) in out, out


def test_s4_a_pact_holding_both_tables_is_exit_2_naming_the_old_one(world):
    """Round 1's yellow 1, end to end. The old table above the new one,
    under a heading of its own, holds a signer the `Signer` table does not
    list. Read silently it would be a signer nobody reads at exit 0; it is
    refused instead, and no rename line is printed, because the header read
    is the new one."""
    text = pact(V2).replace(
        "# Pact\n\n",
        "# Pact\n\n| Signatory |\n|---|\n| https://example.com/org/orders-mobile |"
        "\n\n## Before 0.19.0\n\n",
        1,
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a new table above an old one")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact also holds a `| Signatory |` header, the "
        "word before 0.19.0, and nothing under it is read while the `| Signer |` "
        "table stands — move its rows into that table and delete it"
    ) in out, out
    assert "heads its table" not in out, out


def test_s7_the_summary_counts_two_signers(world):
    """S7 of #822: the plural. The second signer has no checkout here, so
    one of the two is read."""
    write(
        world["api"],
        "seal/pact.md",
        pact(V2, (SIGNER_URL, "https://example.com/org/orders-mobile")),
    )
    commit(world["api"], "a second signer")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 1, out
    assert "pact-check: the pact `orders-api` — 1 of 2 signers read · " in out, out


def test_s8_a_hash_from_heads_own_history_is_superseded(world):
    """S8. v1's hash, which `main` gave the clause before v2."""
    anchor = cite(world, clause(V1))
    code, out = run(world)
    assert code == 1, out
    assert (
        f"SUPERSEDED {SIGNER_URL} seal/ledger/1790000000-x.md:1 {anchor} — the "
        "signer was built against a superseded clause"
    ) in out, out
    assert f"it reads @{clause(V2)} now" in out, out


def test_s9_a_hash_only_another_ref_holds_is_not_taken_and_names_it(world):
    """S9. v3 is on `side`, which HEAD does not hold."""
    anchor = cite(world, clause(V3))
    code, out = run(world)
    assert code == 1, out
    assert (
        f"NOT TAKEN {SIGNER_URL} seal/ledger/1790000000-x.md:1 {anchor} — the "
        "pact has not taken the signer's recorded change: this hash is the "
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
        "renamed or removed. Re-coordinate the signer"
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
        f"NOT FOUND {SIGNER_URL} — no checkout of it was found on this "
        f"machine: add `| {SIGNER_URL} | <the path of its checkout> |` to "
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
    """S11, second half: the pact lists the signer and its config does
    not name the pact, so exit 2."""
    write(world["web"], "seal/config.md", config())
    code, out = run(world)
    assert code == 2, out
    assert (
        f"ONE-SIDED {SIGNER_URL} seal/config.md — the pact lists it, and its "
        f"config names no `Pact` row for {PACT_URL}: the relationship is "
        "recorded on one side only"
    ) in out, out


@pytest.mark.parametrize(
    "notify, refusal",
    [
        (
            [("Pact notify", "sometimes")],
            "`Pact notify | sometimes` is not one of `always`, "
            "`when the pact is touched`, `never`",
        ),
        (
            [("Pact notify", "never"), ("Pact notify", "always")],
            "`Pact notify` appears 2 times — one value",
        ),
    ],
    ids=["outside the vocabulary", "written twice"],
)
def test_s3_a_notify_value_outside_the_vocabulary_is_exit_2(world, notify, refusal):
    """S3, the `pact-check` half: the reader's refusal, read strictly. A row
    written twice has no value either, and the `READ` line says so rather
    than printing its first row (round 2 of PR #756, white 3)."""
    write(
        world["web"],
        "seal/config.md",
        config(("Pact", PACT_URL), *notify),
    )
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert f"REFUSED {SIGNER_URL} seal/config.md — {refusal}" in out, out
    assert "— `Pact notify`: will not parse;" in out, out


def test_s7_a_notify_row_below_the_signers_table_is_exit_2(world):
    """S7 of #759. A `Pact notify` row under a blank line that ended the
    signer's table was read as the default and the run was clean. It
    names a pact and is not a pact row in the one spelling read, so it is
    refused, naming the line, and the notify reads as no value."""
    write(
        world["web"],
        "seal/config.md",
        config(("Pact", PACT_URL)) + "\n| Pact notify | always |\n",
    )
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {SIGNER_URL} seal/config.md — `| Pact notify | always |` "
        "names a pact and is not a `Pact` or `Pact notify` row in the one "
        "spelling read: write it as `| Pact | … |` or `| Pact notify | … |` "
        "inside the `| Item | Value |` table, or take it out of this file"
    ) in out, out
    assert "— `Pact notify`: will not parse;" in out, out


def test_no_pact_here_and_no_origin_are_unusable_input(world):
    """Exit 2 for the two ways the pact's repository cannot be read."""
    code, out = run(world, root=world["web"])
    assert code == 2 and "holds no seal/pact.md" in out, out
    git(world["api"], "remote", "remove", "origin")
    code, out = run(world)
    assert code == 2 and "has no origin remote" in out, out


def test_an_anchor_naming_another_pact_is_not_read(world):
    """A signer of two pacts cites the other one too; only this pact's
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


def test_two_siblings_with_the_signers_origin_are_not_guessed_between(world):
    """Nothing is guessed: two checkouts of one signer, and no map line,
    is a signer not found, with both named."""
    twin = world["web"].parent / "orders-web-2"
    twin.mkdir()
    git(twin, "init", "-q", "-b", "main")
    git(twin, "remote", "add", "origin", SIGNER_URL)
    code, out = run(world)
    assert code == 1, out
    assert "2 sibling directories have its origin" in out, out
    assert "nothing here guesses which" in out, out


def test_a_map_that_will_not_read_is_refused_rather_than_read_as_empty(world):
    """Read as empty, every signer it names would be reported missing."""
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
    assert f"UNMATCHED {SIGNER_URL} seal/ledger/1790000000-x.md:1 {anchor}" in out
    assert (
        "The pact sits under the git directory (local mode), so it has no "
        "history and every mismatch reads unmatched"
    ) in out, out


def test_a_map_line_naming_a_checkout_of_another_repository_is_not_trusted(world):
    """The map is keyed by URL and the checkout it names must have that
    origin; a stale line pointing elsewhere is a signer not found."""
    other = world["tmp"] / "unrelated"
    other.mkdir()
    git(other, "init", "-q", "-b", "main")
    git(other, "remote", "add", "origin", "git@example.com:org/unrelated.git")
    write(
        world["home"],
        ".claude/specseal/pact-paths.md",
        f"| Remote | Path |\n|---|---|\n| {SIGNER_URL} | {other} |\n",
    )
    code, out = run(world)
    assert code == 1, out
    assert (
        f"NOT FOUND {SIGNER_URL} — the map names {posix(other)}, whose origin is"
    ) in out, out


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
    kept the branch's text. A signer built against v2 is SUPERSEDED, not
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


def test_a_signer_row_the_table_walk_cannot_read_is_exit_2(world):
    """The row with no closing pipe is refused at the pact, so a signer
    below it is never reported as clean by omission."""
    text = pact(V2).replace(
        f"| {SIGNER_URL} |\n",
        f"| {SIGNER_URL} |\n| https://example.com/org/orders-mobile\n",
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a row with no closing pipe")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signer` table that stops at "
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
    """A mistyped citation is read by nobody else: not the signer's own
    check, not chain-check. Here it is named and exit 2."""
    write(world["web"], "seal/ledger/1790000000-x.md", ledger_row(anchor))
    code, out = run(world)
    assert code == 2, out
    assert (f"REFUSED {SIGNER_URL} seal/ledger/1790000000-x.md:1 — `") in out, out
    assert (
        'does not parse as `pact:orders-api/"<heading path>"@<hash>`, so '
        "nothing grades it"
    ) in out, out


def test_a_signer_with_no_seal_root_is_one_sided(world):
    """Without a root it cannot name the pact, and nothing is read from the
    directory the command happens to stand in."""
    import shutil

    shutil.rmtree(world["web"] / "seal")
    code, out = run(world)
    assert code == 2, out
    assert (
        f"ONE-SIDED {SIGNER_URL} {posix(world['web'])} — the pact lists it, and it "
        "has no seal/ root to name this pact in: the relationship is recorded "
        "on one side only"
    ) in out, out


def test_a_signer_config_that_will_not_read_is_unreadable(world):
    (world["web"] / "seal" / "config.md").unlink()
    (world["web"] / "seal" / "config.md").mkdir()
    code, out = run(world)
    assert code == 2, out
    # Relative to the signer's checkout and in POSIX form: the sentence
    # used to join a native absolute path with `/` (#647's separator note).
    assert f"UNREADABLE {SIGNER_URL} seal/config.md — could not be read" in out, out


def test_an_anchor_file_that_will_not_read_is_unreadable(world):
    (world["web"] / "seal" / "ledger" / "1790000000-x.md").mkdir(parents=True)
    code, out = run(world)
    assert code == 2, out
    assert (
        f"UNREADABLE {SIGNER_URL} seal/ledger/1790000000-x.md — could not be read"
    ) in out, out


def test_a_pact_that_will_not_read_is_unreadable(world):
    (world["api"] / "seal" / "pact.md").unlink()
    (world["api"] / "seal" / "pact.md").mkdir()
    code, out = run(world)
    assert code == 2, out
    assert "UNREADABLE seal/pact.md — the pact could not be read" in out, out


def test_a_pact_listing_its_own_repository_says_so(world):
    """Not `NOT FOUND`, which would send a person looking for a checkout of
    the repository they stand in."""
    write(world["api"], "seal/pact.md", pact(V2, (SIGNER_URL, PACT_URL)))
    commit(world["api"], "the pact lists itself")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        f"REFUSED {PACT_URL} seal/pact.md — the pact lists its own repository; "
        "the `Signer` table lists every OTHER signer, so take this row out"
    ) in out, out
    assert "NOT FOUND" not in out, out


def test_a_signer_row_below_a_blank_line_is_refused(world):
    """A blank line ends the table's walk; a row written below it is a
    signer nobody reads, so it is refused rather than passed over."""
    text = pact(V2).replace(
        f"| {SIGNER_URL} |\n",
        f"| {SIGNER_URL} |\n\n| https://example.com/org/orders-mobile |\n",
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a blank line inside the table")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signer` table that ends above "
        "`| https://example.com/org/orders-mobile |`, a row the walk never "
        "reaches — it and every signer below it would go unread"
    ) in out, out


@pytest.mark.parametrize(
    "body",
    [
        "This work item signs pact:orders-api, the order contract.",
        "This work item signs `pact:orders-api`.",
        'Cite each clause as `pact:orders-api/"<heading path>"@<hash>`.',
        "See pact:orders-api.",
    ],
    ids=["prose", "code span", "the form with its placeholders", "a sentence's end"],
)
def test_prose_naming_the_pact_is_not_a_citation(world, body):
    """A refusal is for a token that begins an anchor, `pact:<name>/` or
    `pact:<name>#`, and does not complete. Naming the pact is not that."""
    cite(world, clause(V2))
    write(world["web"], "seal/specs/1790000001-y/spec.md", f"# spec\n\n{body}\n")
    code, out = run(world)
    assert code == 0, out
    assert "does not parse" not in out, out


def test_a_pact_name_inside_a_graded_anchors_heading_is_not_a_near_miss(world):
    """A clause heading may spell the pact's own name; the anchor around it
    is graded, and the spelling inside it is not a second citation."""
    write(
        world["web"],
        "seal/ledger/1790000000-x.md",
        ledger_row('pact:orders-api/"## On pact:orders-api/old shapes"@deadbeef'),
    )
    code, out = run(world)
    assert code == 2 and "BROKEN " in out, out
    assert "does not parse" not in out, out


def test_a_signer_written_as_an_autolink_is_never_passed_over(world):
    """S2 (🟡 18 of #735's round 3). GFM renders a second signer from an
    autolink line under the table; the walk refuses the line rather than end
    the table there, so the run never says every signer was read."""
    text = pact(V2).replace(
        f"| {SIGNER_URL} |\n",
        f"| {SIGNER_URL} |\n<https://example.com/org/orders-mobile>\n",
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a signer written as an autolink")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signer` table that continues "
        "with `<https://example.com/org/orders-mobile>`, a line with no pipe "
        "that GFM reads as one of its rows — write it as `| … |`"
    ) in out, out


def test_an_entry_refusal_is_printed_after_the_pact(world):
    text = pact(V2).replace(f"| {SIGNER_URL} |\n", f"| {SIGNER_URL} |\n|  |\n")
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "an empty row")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signer` entry that will not "
        "read: an empty row"
    ) in out, out


def test_the_map_is_named_in_posix_form_on_every_platform(world, monkeypatch):
    """The map lives at one documented place, `~/.claude/specseal/
    pact-paths.md`, and every sentence names it that way. Loaded with
    Windows' `os.path.join`, as on a Windows runner, the module still says
    it with `/`; reading the file stays native."""
    import ntpath

    with monkeypatch.context() as patched:
        patched.setattr(os.path, "join", ntpath.join)
        windows = load()
    config = pc.load(os.path.join(pc.HOOKS, "config.py"), "config_for_posix_map")
    signer = (SIGNER_URL, "example.com/org/orders-web", "orders-web")
    _, why = windows.checkout(config, signer, str(world["tmp"] / "nowhere"), {})
    assert "~/.claude/specseal/pact-paths.md" in why, why
    assert "\\" not in why, why


# --- #647 C and D, PR #749's phase 2: the grammar and the printed paths ----


@pytest.mark.parametrize(
    "shape",
    [
        "pact:orders-api{loc}@{h}",
        "pact:orders-api:{loc}@{h}",
        "pact:orders-api {loc}@{h}",
        "pact:orders-api@{h}",
    ],
    ids=[
        "no slash",
        "a colon for the slash",
        "a space for the slash",
        "no heading path",
    ],
)
def test_an_anchor_missing_its_slash_is_refused(world, shape):
    """S4 (🟡 19 of #735's round 3). An anchor whose `/` went missing is still
    an attempt, and the shipped section says one that does not parse is exit
    2. Round 2's narrowing had made each of these a mention, read by nobody."""
    anchor = shape.format(loc=LOCATOR, h=clause(V2))
    write(world["web"], "seal/ledger/1790000000-x.md", ledger_row(anchor))
    code, out = run(world)
    assert code == 2, out
    assert "does not parse" in out, out


@pytest.mark.parametrize(
    "shape",
    [
        "pact:orders-api.{loc}@{h}",
        "pact:orders-api-{loc}@{h}",
        "pact:orders-api_{loc}@{h}",
        "pact:orders-api./{loc}@{h}",
        "pact:orders-api-/{loc}@{h}",
        "pact:orders-api_/{loc}@{h}",
        "pact:orders-api.@{h}",
    ],
    ids=[
        "a dot for the slash",
        "a hyphen for the slash",
        "an underscore for the slash",
        "a dot before the slash",
        "a hyphen before the slash",
        "an underscore before the slash",
        "a dot, no heading path",
    ],
)
def test_a_mark_the_name_holds_is_not_a_second_name(world, shape):
    """`.`, `-` and `_` are marks the grammar's "one mark" covers and the
    name pattern also takes in, so each made the token name another pact,
    read by nobody (round 1, yellow 4). Each is refused at exit 2."""
    anchor = shape.format(loc=LOCATOR, h=clause(V2))
    write(world["web"], "seal/ledger/1790000000-x.md", ledger_row(anchor))
    code, out = run(world)
    assert code == 2, out
    assert "does not parse" in out, out


def test_a_pact_whose_name_extends_this_ones_is_another_pact(world):
    """One mark only: `orders-api-legacy-` begins with this pact's name and
    ends in a mark, and it is another pact's name, cited whole, so it is
    neither graded nor refused here."""
    write(
        world["web"],
        "seal/ledger/1790000000-x.md",
        ledger_row(f"pact:orders-api-legacy-/{LOCATOR}@deadbeef")
        + ledger_row(f"pact:orders-api/{LOCATOR}@{clause(V2)}"),
    )
    code, out = run(world)
    assert code == 0, out
    assert "does not parse" not in out, out


def test_the_refusal_names_both_remedies(world):
    """S5 (⬜ 23). The grammar stands -- a `/` after `pact:<name>` begins an
    anchor -- so the half-typed form in prose is refused, and the sentence
    names the second remedy beside the first: a fenced block for an
    example."""
    cite(world, clause(V2))
    write(
        world["web"],
        "seal/specs/1790000001-y/spec.md",
        "# spec\n\nThe clauses sit under pact:orders-api/ in that repository.\n",
    )
    code, out = run(world)
    assert code == 2, out
    assert (
        "Quote the heading path and give it a hash, `@00000000` until the first "
        "report names the real one; or, where it shows the shape rather than "
        "citing a clause, put it in a fenced code block, which nothing reads"
    ) in out, out


@pytest.mark.parametrize(
    "path, repo, home, want",
    [
        (
            r"C:\Users\x\work\orders-web\seal\config.md",
            r"C:\Users\x\work\orders-web",
            r"C:\Users\x",
            "seal/config.md",
        ),
        (
            r"C:\Users\x\.claude\specseal\pact-paths.md",
            None,
            r"C:\Users\x",
            "~/.claude/specseal/pact-paths.md",
        ),
        (r"C:\Users\x\work\orders-web", None, r"C:\Users\x", "~/work/orders-web"),
        (r"D:\work\orders-web", None, r"C:\Users\x", "D:/work/orders-web"),
        (r"D:\Users\x\work", None, r"C:\Users\x", "D:/Users/x/work"),
        (r"Users\x\work", None, r"\Users\x", "Users/x/work"),
        (r"D:\data\xy\work", None, r"D:\data\x", "D:/data/xy/work"),
        ("C:/Users/x/work/a\\b.md", r"C:\Users\x\work", None, "a/b.md"),
    ],
    ids=[
        "inside its repository",
        "the map",
        "a checkout under home",
        "another drive",
        "the same segments on another drive",
        "a relative path under no anchor",
        "a longer segment is not under home",
        "both separators",
    ],
)
def test_every_printed_path_is_in_posix_form(path, repo, home, want):
    """S6. The one helper every printed path goes through, fed Windows paths
    through `ntpath`, so the POSIX guarantee is removed rather than relied on
    (`agent-contract` §13): no `\\` survives, a path under home begins `~/`,
    and one inside its repository is relative to it."""
    import ntpath

    got = pc.shown(path, repo, home, flavour=ntpath)
    assert got == want
    assert "\\" not in got


def test_no_line_formats_a_path_without_the_helper():
    """S6, the class: every `{…}` in an f-string of `pact_check.py` that names
    a path variable goes through `shown`. Restoring the old
    `{their_home}/{CONFIG_FILE}` puts one back, and this names it."""
    import ast

    with open(SCRIPT, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    # `where` is not among them: every value it holds is built by `shown`
    # or is a literal `seal/...` label.
    paths = {
        "path",
        "repo",
        "root",
        "pact_path",
        "their_home",
        "their_repo",
        "file_path",
        "home",
        "home_dir",
        "h",
        "hits",
    }
    raw = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.JoinedStr):
            continue
        for part in node.values:
            if (
                isinstance(part, ast.FormattedValue)
                and isinstance(part.value, ast.Name)
                and part.value.id in paths
            ):
                raw.append((node.lineno, part.value.id))
    assert raw == [], raw
