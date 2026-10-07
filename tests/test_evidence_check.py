"""evidence-check: ledger discovery, the CLI surface, and the exit codes.

The verdict machinery itself lives in `test_a_row_points_by_content.py`. What
is here is everything around it — which files are read, how several are
aggregated, and what a CI step sees.

**No fixture in this file runs git.** It used to need a repository with real
commits, because a row's baseline was a commit and drift was a diff. A
coordinate that names content needs only the file, which is the shortest
statement of what the redesign removed.
"""

import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")

SERVICE = "def handler(x):\n    return x + 1\n\n\ndef other():\n    return 0\n"
# `handler`'s body, hashed the way the checker hashes it.
GOOD = "9207ed06"


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def usable_bash():
    """Whether `bash` here actually executes what it is handed.

    The precondition this file's guard tests assume, stated and checked
    rather than assumed: on Windows, `bash` on PATH can resolve to the WSL
    stub in System32, which fails every command with its own exit code no
    matter what was asked — so every assertion expecting the guarded 1
    passed for that wrong reason, and only the one expecting 0 could fail.
    The step under test runs on the ubuntu leg of real CI, so a skip here
    costs the guard nothing it is ever asked to do.
    """
    try:
        r = subprocess.run(["bash", "-c", "exit 7"], capture_output=True, timeout=30)
    except OSError:
        return False
    return r.returncode == 7


def step(args, cwd):
    """The exit code of the CI step `evidence-ci` prints, guard included."""
    quoted = " ".join(f"'{a}'" for a in args)
    # `sys.executable`, not `python3`: the name does not exist on Windows.
    # Forward slashes, not `os.sep`: inside bash's single quotes a backslash
    # is literal, so `C:\...\python.exe` never resolves to the interpreter,
    # the command exits before the guard runs, and every case expecting the
    # guarded 1 passed for that wrong reason while the one expecting 0
    # failed. Both spellings name the same file to Windows Python.
    exe = sys.executable.replace("\\", "/")
    script = SCRIPT.replace("\\", "/")
    return subprocess.run(
        [
            "bash",
            "-e",
            "-c",
            f"'{exe}' '{script}' {quoted} || [ $? -eq 1 ]",
        ],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
    ).returncode


@pytest.fixture
def proj(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    return d


def ledger(proj, body, at="seal/ledger.md"):
    path = proj / at
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# map\n\n" + body, encoding="utf-8")
    return path


def test_the_hash_in_this_files_fixtures_is_the_real_one(proj):
    """Pinned rather than computed, so a fixture cannot agree with a broken
    hash function by using it to build its own expectation."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("ec", SCRIPT)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    assert ec.content_hash(SERVICE.splitlines()[0:2]) == GOOD


def test_a_matching_row_is_ok_and_exits_zero(proj):
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_drift_exits_one_and_strict_exits_two(proj):
    ledger(proj, "| POL-1 | `src/service.py#handler@00000000` |\n")
    assert run(["."], proj).returncode == 1
    assert run(["--strict", "."], proj).returncode == 2


def test_a_broken_coordinate_exits_two(proj):
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    r = run(["."], proj)
    assert "BROKEN" in r.stdout and r.returncode == 2, r.stdout


def test_a_deleted_root_level_file_is_broken_not_external(proj):
    """`main.py#f` with the file deleted used to classify as EXTERNAL — first
    path element missing meant "other repo" — and EXTERNAL never fails the
    build. A root-level coordinate has no cross-repo prefix, so a missing file
    there is a broken citation."""
    ledger(proj, "| POL-1 | `src/service.py#handler@00000000` |\n")
    (proj / "src" / "service.py").unlink()
    r = run(["."], proj)
    assert r.returncode == 2 and "BROKEN" in r.stdout and "EXTERNAL" not in r.stdout


def test_duplicate_coordinates_are_counted_once(proj):
    ledger(
        proj,
        f"| POL-1 | `src/service.py#handler@{GOOD}` |\n"
        f"| POL-2 | `src/service.py#handler@{GOOD}` |\n",
    )
    assert "1 ok" in run(["."], proj).stdout


def test_map_resolves_a_prefixed_cross_repo_path(proj, tmp_path):
    other = tmp_path / "legacy"
    (other / "src").mkdir(parents=True)
    (other / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    ledger(proj, f"| POL-1 | `legacy/src/service.py#handler@{GOOD}` |\n")
    # EXTERNAL needs declared cross-repo intent since round 4's 🔴 3; a
    # parity config is one of the three declarations.
    (proj / "seal" / "parity.md").write_text("# parity\n", encoding="utf-8")
    assert "1 external" in run(["."], proj).stdout
    r = run(["--map", f"legacy={other}", "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_a_missing_prefix_without_cross_repo_intent_is_broken(proj):
    """EXTERNAL is a claim about ANOTHER repository, and only a declaration —
    `seal/parity.md`, `--map`, `--default-repo` — says this project has
    one. Without intent, a deleted or renamed directory turned its rows
    EXTERNAL and the build stayed green (round 4, 🔴 3)."""
    ledger(proj, "| POL-1 | `legacy/src/old.py#handler@00000000` |\n")
    r = run(["."], proj)
    assert "EXTERNAL" not in r.stdout and "BROKEN" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_migrate_reads_map_and_default_repo(proj, tmp_path):
    """`--migrate` ignored both, so a legacy-parity ledger could never
    migrate and the OLD-FORMAT prescription line was circular for exactly
    those repositories (round 4, 🟡 9)."""
    other = tmp_path / "legacy"
    (other / "src").mkdir(parents=True)
    (other / "src" / "old.py").write_text(SERVICE, encoding="utf-8")
    orig = tmp_path / "orig"
    (orig / "apps").mkdir(parents=True)
    (orig / "apps" / "svc.py").write_text(SERVICE, encoding="utf-8")
    ledger(
        proj,
        "| POL-1 | `legacy/src/old.py:1-2` | 2026-08-31 |\n"
        "| POL-2 | `apps/svc.py:1-2` | 2026-08-31 |\n",
    )
    r = run(
        ["--migrate", "--map", f"legacy={other}", "--default-repo", str(orig), "."],
        proj,
    )
    assert "2 rows migrated" in r.stdout, r.stdout
    text = (proj / "seal" / "ledger.md").read_text(encoding="utf-8")
    assert f"legacy/src/old.py#handler@{GOOD}" in text, text
    assert f"apps/svc.py#handler@{GOOD}" in text, text


def test_default_repo_resolves_an_unprefixed_cross_repo_path(proj, tmp_path):
    """A migration ledger states coordinates against the ORIGINAL repo with no
    prefix. The property is resolution: found in the other checkout rather than
    reported EXTERNAL or BROKEN."""
    orig = tmp_path / "orig"
    (orig / "apps").mkdir(parents=True)
    (orig / "apps" / "svc.py").write_text(SERVICE, encoding="utf-8")
    ledger(proj, f"| POL-9 | `apps/svc.py#handler@{GOOD}` |\n")
    r = run(["--default-repo", str(orig), "."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_no_ledger_at_all_is_a_no_op(proj):
    r = run(["."], proj)
    assert "no evidence ledgers found" in r.stdout and r.returncode == 0


@pytest.mark.parametrize(
    "at",
    ["seal/ledger.md", "seal/ledger/core.md", "docs/policies/demo/_evidence.md"],
)
def test_the_checker_finds_the_ledger_with_no_arguments(proj, at):
    """The current home, the per-work-item fragment, and the pre-0.10 address."""
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n", at=at)
    r = run(["."], proj)
    assert "no evidence ledgers found" not in r.stdout, r.stdout
    assert "src/service.py#gone" in r.stdout, r.stdout
    assert r.returncode == 2


def test_a_custom_ledger_glob_is_read_instead(proj):
    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    (proj / "SPEC.md").write_text(
        f"| POL-1 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert "SPEC.md" in r.stdout and "1 ok" in r.stdout and r.returncode == 0


def test_several_ledgers_aggregate_and_the_worst_one_decides(proj):
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    ledger(proj, "| POL-9 | `src/service.py#gone@00000000` |\n", at="seal/ledger/b.md")
    r = run(["."], proj)
    assert "1 ok" in r.stdout and "1 broken" in r.stdout
    assert r.returncode == 2, "a broken coordinate in the second ledger must fail"


def test_a_coordinate_in_a_dot_directory_resolves(proj):
    """A leading dot is allowed: `.github/...` was read as `github/...` and
    reported EXTERNAL, so the plugin could not cite its own directory."""
    (proj / ".github").mkdir()
    (proj / ".github" / "svc.py").write_text(SERVICE, encoding="utf-8")
    ledger(proj, f"| POL-1 | `.github/svc.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_letting_drift_warn_takes_both_halves(proj):
    """`evidence-ci` twice described a softer mode that does not exist.

    Drift fails a `bash -e` step either way; the guard only lets it through
    once `--strict` is gone too, and a broken coordinate still fails through
    that same guard. A malformed coordinate follows the flag the way drift
    does (work item 1790381328), so the guard lets it through as well, which
    is what `evidence-ci`'s step 4 now says."""
    if not usable_bash():
        pytest.skip("no usable bash — the step under test runs on ubuntu CI")
    ledger(proj, "| POL-1 | `src/service.py#handler@00000000` |\n")
    assert run(["."], proj).returncode == 1, "drift already fails without --strict"
    assert run(["--strict", "."], proj).returncode == 2
    assert step(["--strict", "."], proj) == 1, "the guard cannot swallow exit 2"
    assert step(["."], proj) == 0, "both halves together let drift warn"

    ledger(proj, "| POL-1 | `src/service.py#gone@00000000` |\n")
    assert step(["."], proj) == 1, "the guard must not swallow a broken coordinate"

    ledger(proj, "| POL-1 | `src/service.py#handler@0` |\n")
    assert step(["."], proj) == 0, "the guard lets a malformed coordinate warn"
    assert step(["--strict", "."], proj) == 1, "--strict still refuses it"


def test_the_ci_skill_prints_the_step_that_matches_that_behavior():
    """The executed fact above is worth what the sentence beside it says."""
    with open(
        os.path.join(ROOT, "skills", "evidence-ci", "SKILL.md"), encoding="utf-8"
    ) as f:
        text = f.read()
    snippet = text.split("```yaml")[1].split("```")[0]
    assert "|| [ $? -eq 1 ]" in snippet, "the step lost the guard"
    assert "--strict" not in snippet, (
        "the printed step keeps --strict, whose exit 2 the guard cannot swallow"
    )
    assert "drop `--strict`" in text, "the prose stopped naming the other half"


# --- Q2 (#80): which `seal/` the defaults are joined under -------------------
#
# No git runs here either: a `.git` DIRECTORY at the root is the common git
# directory, and `hooks/optin.py` answers that case without a process.


def local_root(proj):
    """`.git/seal/` and nothing at `<root>/seal/` — a local-mode repository
    as the checker sees it."""
    home = proj / ".git" / "seal"
    home.mkdir(parents=True)
    assert not (proj / "seal").exists()
    return home


def test_the_plugins_copy_resolves_the_root_under_the_git_directory(proj):
    """Q2 (a). The plugin's copy sits beside `hooks/optin.py` and asks it
    where `seal/` is; the defaults were joined under ROOT, so a local-mode
    ledger was "no evidence ledgers found", exit 0 — a green run that
    examined nothing."""
    local_root(proj)
    ledger(
        proj, "| POL-1 | `src/service.py#gone@00000000` |\n", at=".git/seal/ledger.md"
    )
    r = run(["."], proj)
    assert "no evidence ledgers found" not in r.stdout, r.stdout
    assert "src/service.py#gone" in r.stdout, r.stdout
    assert r.returncode == 2


def test_the_plugins_copy_reads_the_parity_config_under_the_resolved_root(proj):
    """The other join: `seal/parity.md` is the declaration that lets an
    unplaceable prefixed row read EXTERNAL instead of BROKEN, and it was
    looked for under ROOT only."""
    local_root(proj)
    (proj / ".git" / "seal" / "parity.md").write_text("# parity\n", encoding="utf-8")
    ledger(
        proj,
        "| POL-1 | `legacy/src/old.py#handler@00000000` |\n",
        at=".git/seal/ledger.md",
    )
    r = run(["."], proj)
    assert "EXTERNAL" in r.stdout and "BROKEN" not in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout


def test_the_tree_root_still_wins_for_the_plugins_copy(proj):
    """S1's order, through the checker: `<root>/seal/` first."""
    local_root(proj)
    ledger(
        proj, "| POL-1 | `src/service.py#gone@00000000` |\n", at=".git/seal/ledger.md"
    )
    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["."], proj)
    assert "total: 1 ok" in r.stdout and ".git" not in r.stdout, r.stdout
    assert r.returncode == 0


def vendored_copy(tmp_path):
    """The checker as `evidence-ci` vendors it: alone in `tools/`, with no
    `hooks/` and no `SKILL.md` beside it."""
    tools = tmp_path / "elsewhere" / "tools"
    tools.mkdir(parents=True)
    dst = tools / "evidence_check.py"
    dst.write_bytes(open(SCRIPT, "rb").read())
    return dst


def test_a_copy_with_no_hooks_beside_it_reads_the_tree_root_only(proj, tmp_path):
    """Q2 (a)'s other half. The vendored copy cannot import `hooks/optin.py`,
    and it runs in CI, which is shared mode: it reads `<root>/seal/` as it
    always did. A local-mode ledger is invisible to it, and says so."""
    copy = vendored_copy(tmp_path)
    local_root(proj)
    ledger(
        proj, "| POL-1 | `src/service.py#gone@00000000` |\n", at=".git/seal/ledger.md"
    )
    r = subprocess.run(
        [sys.executable, str(copy), "."],
        cwd=str(proj),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert "no evidence ledgers found" in r.stdout and r.returncode == 0, r.stdout

    ledger(proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = subprocess.run(
        [sys.executable, str(copy), "."],
        cwd=str(proj),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_a_copy_under_a_plugin_tree_without_a_skill_beside_it_is_still_vendored(
    proj, tmp_path
):
    """`seal_home`'s `os.path.isfile(skill)` conjunct, which stood recorded as
    unreachable and is not.

    The rider here said the state that separates the two conjuncts is a
    vendored copy inside a tree that HAS a plugin above it, and that nothing
    constructs it. This constructs it. The copy sits three directories under a
    tree carrying `hooks/optin.py`, so the FIRST conjunct passes; there is no
    `SKILL.md` one level up, so the second is the only thing left to say this
    is not the plugin's own copy.

    Against a local-mode repository the two answers differ — `<root>/seal/`
    with the conjunct, `<git-common-dir>/seal/` without it — so dropping it
    makes a vendored copy read a root it must not read. That is a wrong
    ANSWER rather than merely an unheld line, and the mutation that survived
    every evidence suite dies here.
    """
    tree = tmp_path / "tree"
    (tree / "hooks").mkdir(parents=True)
    (tree / "hooks" / "optin.py").write_bytes(
        open(os.path.join(ROOT, "hooks", "optin.py"), "rb").read()
    )
    scripts = tree / "a" / "b" / "scripts"
    scripts.mkdir(parents=True)
    copy = scripts / "evidence_check.py"
    copy.write_bytes(open(SCRIPT, "rb").read())
    assert (tree / "hooks" / "optin.py").is_file(), "the first conjunct must pass"
    assert not (tree / "a" / "b" / "SKILL.md").exists(), (
        "a SKILL.md here would let the first conjunct decide and the case "
        "would prove nothing"
    )

    local_root(proj)
    ledger(
        proj, f"| POL-1 | `src/service.py#handler@{GOOD}` |\n", at=".git/seal/ledger.md"
    )
    r = subprocess.run(
        [sys.executable, str(copy), "."],
        cwd=str(proj),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert "no evidence ledgers found" in r.stdout, (
        "a vendored copy read the local-mode root: the `SKILL.md` conjunct is "
        f"what keeps it on `<root>/seal/`\n{r.stdout}"
    )
    assert r.returncode == 0, r.stdout


def test_the_ledger_flag_overrides_the_resolver_either_way(proj):
    """`--ledger` is unchanged: a pattern given by hand is joined under ROOT,
    whatever the resolver would have said."""
    local_root(proj)
    ledger(
        proj, "| POL-1 | `src/service.py#gone@00000000` |\n", at=".git/seal/ledger.md"
    )
    (proj / "SPEC.md").write_text(
        f"| POL-1 | `src/service.py#handler@{GOOD}` |\n", encoding="utf-8"
    )
    r = run(["--ledger", "SPEC.md", "."], proj)
    assert "SPEC.md" in r.stdout and "1 ok" in r.stdout and r.returncode == 0
    assert "gone" not in r.stdout, "the resolved default was read beside --ledger"


# --- #444: a row inside a closed fence is an example, not a claim ----------

FENCED_EXAMPLE = (
    "A row looks like this:\n\n"
    "```markdown\n"
    "| X | `nosuchfile.py#nothing@deadbeef` | read | 2026-01-01 | |\n"
    "| Y | `src/service.py#handler@00000000` | old `src/service.py:1-2` 2026-01-01 abcdef1 | |\n"
    "```\n\n"
)


def test_a_fenced_example_row_is_not_checked(proj):
    """S1, #444's reproduction. A ledger that explains its own row format
    shows an example row in a fenced block, and nobody wrote that row. Seen
    red against `c52e8350`: `BROKEN  nosuchfile.py#nothing  file not found`
    and exit 2 — the broad gate failing over an example."""
    ledger(proj, FENCED_EXAMPLE + f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = run(["--strict", "."], proj)
    assert "nosuchfile" not in r.stdout, r.stdout
    assert "OLD-FORMAT" not in r.stdout, r.stdout
    assert "1 ok · 0 drifted · 0 broken" in r.stdout and r.returncode == 0, r.stdout


def test_the_writers_leave_a_fenced_example_byte_for_byte(proj):
    """S2. `--reverify` rewrites a hash by position and `--migrate` rewrites an
    old `path:line` row, and neither may touch an example: a person's example
    that `--reverify` rewrote would stop showing the shape it was written to
    show. Seen red against `c52e8350`: `--reverify` rewrote the fenced
    `00000000` and `--migrate` rewrote the fenced `src/service.py:1-2`."""
    path = ledger(
        proj,
        FENCED_EXAMPLE
        + "| POL-1 | `src/service.py#handler@00000000` |\n"
        + "| POL-2 | old `src/service.py:1-2` 2026-01-01 |\n",
    )
    fenced = FENCED_EXAMPLE
    r = run(["--reverify", "."], proj)
    assert r.returncode == 0, r.stdout
    after = path.read_text(encoding="utf-8")
    assert fenced in after, after
    assert f"`src/service.py#handler@{GOOD}` |\n| POL-2" in after, after
    r = run(["--migrate", "."], proj)
    after = path.read_text(encoding="utf-8")
    assert fenced in after, after
    assert "| POL-2 | old `src/service.py#handler@" in after, after


def test_an_unclosed_fence_still_holds_its_rows(proj):
    """S3, which pins the direction rather than a change: only a block that
    closes is certainly a quotation. A fence the author never closed runs to
    the end of the file, and reading nothing from there on would pass a
    broken row in silence. Passes before and after #444."""
    ledger(
        proj,
        "```markdown\nan example the author never closed\n\n"
        "| POL-1 | `src/gone.py#handler@00000000` |\n",
    )
    r = run(["."], proj)
    assert "BROKEN   src/gone.py#handler" in r.stdout and r.returncode == 2, r.stdout


def test_a_vendored_copy_skips_a_fenced_example_too(proj, tmp_path):
    """The copy `evidence-ci` puts alone in `tools/` has no shared reader
    beside it, so it asks its own pair of delimiter functions. The verdict
    must be the plugin's."""
    copy = vendored_copy(tmp_path)
    ledger(proj, FENCED_EXAMPLE + f"| POL-1 | `src/service.py#handler@{GOOD}` |\n")
    r = subprocess.run(
        [sys.executable, str(copy), "--strict", "."],
        cwd=str(proj),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert "nosuchfile" not in r.stdout and r.returncode == 0, r.stdout


def test_the_vendored_fence_rule_agrees_with_the_shared_one():
    """The vendored pair is a second copy of `unverified_check.py`'s
    delimiter rule, kept for the one reason `hooks/blocks.py#FENCE` keeps its
    own: the copy cannot load the reader. This holds the two in step over the
    shape table the config reader's agreement case walks, opener and closer
    alike."""
    import importlib.util

    from test_unverified_rows_close import FENCE_SHAPES, uc

    spec = importlib.util.spec_from_file_location("ec_vendored_rule", SCRIPT)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    assert ec.fence_rule()[0].__module__ == "specseal_unverified_reader", (
        "the plugin's copy must ask the shared reader, not its vendored pair"
    )
    lines = {line for shape in FENCE_SHAPES for line in shape}
    for line in lines:
        assert ec.vendored_fence_opener(line) == uc.fence_opener(line), line
        for opener in {uc.fence_opener(o) for o in lines} - {None}:
            assert ec.vendored_fence_closes(line, opener) == uc.fence_closes(
                line, opener
            ), (line, opener)


def test_the_vendored_cell_rule_agrees_with_the_shared_one():
    """The `MALFORMED` arm (#299) reads a ledger row's `Code grounds` cell,
    so the checker splits table rows, and a copy `evidence-ci` vendors alone
    cannot load the shared reader's `split_row` any more than its fence rule.
    The plugin's copy asks the shared reader; this holds the vendored split
    in step with it over the shapes a ledger row takes."""
    import importlib.util

    from test_unverified_rows_close import uc

    spec = importlib.util.spec_from_file_location("ec_vendored_cells", SCRIPT)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    assert ec.cell_rule().__module__ == "specseal_unverified_reader", (
        "the plugin's copy must ask the shared reader, not its vendored split"
    )
    for line in (
        "| a | b |",
        "|a|b",
        "  | indented | row |  ",
        "| a \\| b | c |",
        '| `x.py#"p \\| q"@00000000` | c |',
        "| ends on an escape \\|",
        "| | | |",
        "|---|:-:|",
        "|",
        "not a row",
        "",
    ):
        assert ec.vendored_split_row(line) == uc.split_row(line), line


# The config table's own shapes, for S4 of #867: every shape the vendored
# twin can meet in a CI checkout's `seal/config.md`. **No fence and no
# comment**, on purpose: the twin is blind to both, as inventory row E46 of
# #834 states, and a vendored copy reads a file whose table is its own. A
# shape added here that holds either would hold the twin to a rule it does
# not carry.
_HEAD = "# Repository config\n\n| Item | Value |\n|---|---|\n"
CONFIG_SHAPES = {
    "plain": _HEAD + "| Mode | shared |\n| Broad gate | bin/test -q |\n",
    "a doubled row": _HEAD + "| Mode | shared |\n| Mode | local |\n",
    "an empty value": _HEAD + "| Mode |  |\n| Broad gate | x |\n",
    "an escaped pipe": _HEAD + "| Broad gate | a \\| b |\n| Mode | shared |\n",
    "a stray separator": _HEAD + "| Mode | shared |\n|---|---|\n| Broad gate | x |\n",
    "a second header": _HEAD
    + "| Mode | shared |\n| Item | Value |\n|---|---|\n| Broad gate | x |\n",
    "no header": "| Mode | shared |\n| Broad gate | x |\n",
    "rows above the header": "| Mode | local |\n\n" + _HEAD + "| Mode | shared |\n",
    "an empty item": _HEAD + "|| x |\n| Mode | shared |\n",
    "a three-column row": _HEAD
    + "| Mode | shared |\n| a | b | c |\n| Broad gate | x |\n",
    "prose under the table": _HEAD
    + "| Mode | shared |\n\nsome prose\n| Broad gate | x |\n",
    "a line before the first row": _HEAD + "| not a row\n| Mode | shared |\n",
    "crlf": (_HEAD + "| Mode | shared |\n| Broad gate | x |\n").replace("\n", "\r\n"),
    "no table": "# nothing here\n",
}


def _checker(name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    return ec


@pytest.mark.parametrize("name", sorted(CONFIG_SHAPES))
def test_the_vendored_config_rule_agrees_with_the_shared_one(name):
    """S4 of #867. A copy `evidence-ci` vendors alone cannot load
    `hooks/config.py`, so it carries twins of the table walk and the value
    rule; this holds both equal to the plugin's reader over the config
    table's own shapes, item by item. The twin's table walk had no case at
    all (inventory row E46 said it had one, and none existed), and it read a
    stray separator, a second header and an empty item differently: seen red
    against 5623d728's `vendored_config_rows` on those three shapes."""
    from conftest import load_hook_module

    config = load_hook_module("config.py", "specseal_config_for_the_twin")
    ec = _checker("ec_vendored_config")
    assert os.path.realpath(
        ec.config_rule()[1].__code__.co_filename
    ) == os.path.realpath(config.config_rows.__code__.co_filename), (
        "the plugin's copy must ask hooks/config.py, not its vendored twin"
    )
    text = CONFIG_SHAPES[name]
    rows = config.config_rows(text)
    assert ec.vendored_config_rows(text) == rows, name
    for item in ("Mode", "Broad gate", "Ledger frozen from", "x", ""):
        assert ec.vendored_config_value(rows, item) == config.value_of(rows, item), (
            name,
            item,
        )


@pytest.mark.parametrize("shape", ["absent", "readable", "directory", "undecodable"])
def test_the_vendored_config_file_reader_agrees_with_the_shared_one(tmp_path, shape):
    """S4's file half: the twin of `hooks/config.py#config_text` tells an
    absent file from one that is there and will not read, in the reader's
    own sentence, so a vendored `--reverify` refuses exactly where the
    plugin's does."""
    from conftest import load_hook_module

    config = load_hook_module("config.py", "specseal_config_for_the_file_twin")
    ec = _checker("ec_vendored_config_file")
    path = tmp_path / "config.md"
    if shape == "readable":
        path.write_text(CONFIG_SHAPES["plain"], encoding="utf-8")
    elif shape == "directory":
        path.mkdir()
    elif shape == "undecodable":
        path.write_bytes(b"| Item | Value |\n|---|---|\n| Mode | \xff |\n")
    assert ec.vendored_config_text(str(tmp_path)) == config.config_text(str(tmp_path))
