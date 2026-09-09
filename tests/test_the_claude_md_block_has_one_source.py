"""The `CLAUDE.md` block has one source, and the copy is checked, not trusted.

Issue #292 measured the block the repository's `CLAUDE.md` carries against
the one installed in `~/.claude/CLAUDE.md` and found `## Git` 95 % identical:
one sentence had moved in one copy and not the other. Nothing read both.
`install.sh` copied the block out of the repository's `CLAUDE.md`, and the
`preset-setup` and `update` skills read it from there at runtime, so the
repository's own always-loaded file was doubling as the source of a file it
distributes -- and an edit to either half was an edit to one of them.

So the block lives in `templates/claude-md-block.md`, markers included.
`install.sh` reads it from there; `.github/scripts/claude_block.py --write`
regenerates the region inside `CLAUDE.md` from it; `--check` exits 1 naming
the first line that differs, and the hygiene workflow runs `--check` on every
pull request. The repository's `CLAUDE.md` keeps a generated copy, by the
owner's answer (`questions.md` Q1): a contributor without the plugin still
has to read the rules.

Exit codes, as `spec.md` §*Data & interfaces* states them: 0 the two agree
(or `--write` made them), 1 they differ, 2 a file the script cannot read or a
target with no markers -- which is not a disagreement but a file it cannot
place a block in.
"""

import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "claude_block.py")
TEMPLATE = os.path.join(ROOT, "templates", "claude-md-block.md")
TARGET = os.path.join(ROOT, "CLAUDE.md")
INSTALL = os.path.join(ROOT, "install.sh")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "hygiene.yml")
START, END = "<!-- specseal:start -->", "<!-- specseal:end -->"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def block_of(text):
    """The marker region, the way `install.sh`'s `awk` cuts it: from the line
    holding the start marker through the line holding the end marker."""
    lines = text.splitlines(keepends=True)
    first = next(i for i, line in enumerate(lines) if START in line)
    last = next(i for i, line in enumerate(lines) if END in line)
    return "".join(lines[first : last + 1])


def run(*args, script=SCRIPT):
    return subprocess.run(
        [sys.executable, script, *args],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def copies(tmp_path):
    """The template and the real `CLAUDE.md`, copied where a case may edit
    them. Every case that mutates works on these, never on the tree."""
    template = tmp_path / "claude-md-block.md"
    target = tmp_path / "CLAUDE.md"
    shutil.copy(TEMPLATE, template)
    shutil.copy(TARGET, target)
    return str(template), str(target)


def flip_one_byte_inside_the_block(path):
    """One character of the block's prose changed -- inside the markers, on a
    line that is neither marker, so the edit is a disagreement and not a
    damaged block. Returns the 1-based line number within the block."""
    text = read(path)
    lines = text.splitlines(keepends=True)
    first = next(i for i, line in enumerate(lines) if START in line)
    # The first heading after the start marker: `## Tooling` -> `## Toolinh`.
    index = first + 1
    assert lines[index].startswith("## "), lines[index]
    old = lines[index]
    lines[index] = old[:-2] + chr(ord(old[-2]) + 1) + old[-1]
    assert lines[index] != old
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    return index - first + 1


# --- the check ---------------------------------------------------------------


def test_the_template_is_the_block_and_nothing_else():
    """The template is what `install.sh` cuts with `awk` and what the script
    compares, so a line outside its markers is a line that reaches nobody and
    a line inside is one that reaches every user."""
    text = read(TEMPLATE)
    assert text.startswith(START + "\n"), (
        "the template does not open with the start marker"
    )
    assert text.endswith(END + "\n"), "the template does not close with the end marker"
    assert text.count(START) == 1 and text.count(END) == 1


def test_the_repository_copy_agrees_with_the_template():
    """The state CI holds every pull request to. If this is red, somebody
    edited one of the two and did not run `--write`."""
    out = run("--check")
    assert out.returncode == 0, out.stdout + out.stderr
    assert block_of(read(TARGET)) == block_of(read(TEMPLATE))


def test_one_byte_of_difference_exits_1_naming_the_line(tmp_path):
    """S7. The whole check: a one-byte edit inside the block is a
    disagreement, the exit says so, and the message names the first
    differing line with both sides quoted -- a reader has to know WHICH line
    to know which copy to believe."""
    template, target = copies(tmp_path)
    line = flip_one_byte_inside_the_block(target)
    out = run("--check", "--template", template, "--target", target)
    assert out.returncode == 1, out.stdout + out.stderr
    report = out.stdout + out.stderr
    assert f"line {line}" in report, report
    assert "## Tooling" in report and "## Toolinh" in report, (
        f"the report does not quote both sides of the differing line: {report!r}"
    )
    assert "--write" in report, "the report does not say how to fix it"


def test_a_line_added_before_the_end_marker_is_a_disagreement(tmp_path):
    """The other shape of drift: every line the template has is there, and
    one more. A comparison that stops at the shorter block calls that equal,
    which is how a rule appended to the copy would ship to nobody. Both blocks
    end at their end-marker line, so the line named is the template's marker
    against the copy's extra rule."""
    template, target = copies(tmp_path)
    text = read(target)
    text = text.replace(END, "- a rule only the copy has\n" + END, 1)
    with open(target, "w", encoding="utf-8") as f:
        f.write(text)
    out = run("--check", "--template", template, "--target", target)
    assert out.returncode == 1, out.stdout + out.stderr
    report = out.stdout + out.stderr
    assert (
        f"template: {END}" in report
        and "copy:     - a rule only the copy has" in report
    ), report


def test_write_restores_the_copy_and_touches_nothing_outside_the_markers(tmp_path):
    """`--write` regenerates the region and leaves the owner's rules below the
    end marker byte for byte. Those are the repository's own and the script
    has no business there -- the same boundary `install.sh` keeps."""
    template, target = copies(tmp_path)
    before = read(target)
    flip_one_byte_inside_the_block(target)
    assert run("--check", "--template", template, "--target", target).returncode == 1
    out = run("--write", "--template", template, "--target", target)
    assert out.returncode == 0, out.stdout + out.stderr
    assert read(target) == before, "`--write` did not restore the file exactly"
    assert run("--check", "--template", template, "--target", target).returncode == 0
    outside = read(target).split(END, 1)[1]
    assert outside == before.split(END, 1)[1]


def test_an_edit_outside_the_markers_is_not_a_disagreement(tmp_path):
    """The rules below the block are the repository's own. The check reads
    the marker region and nothing else, or every edit to a house rule would
    fail the pull request that made it."""
    template, target = copies(tmp_path)
    with open(target, "a", encoding="utf-8") as f:
        f.write("\n## A house rule added after the block\n- something local\n")
    out = run("--check", "--template", template, "--target", target)
    assert out.returncode == 0, out.stdout + out.stderr


def test_a_target_with_no_markers_exits_2_for_both_modes(tmp_path):
    """Not a disagreement: a file the script cannot place a block in. Exit 2
    keeps it apart from 1 so a CI step that fails on 1 says the right thing,
    and `--write` refuses rather than appending -- appending is `install.sh`'s
    act, on a user's file, with a backup."""
    template, _ = copies(tmp_path)
    target = tmp_path / "bare.md"
    target.write_text("# nothing here\n", encoding="utf-8")
    for mode in ("--check", "--write"):
        out = run(mode, "--template", template, "--target", str(target))
        assert out.returncode == 2, (
            f"{mode}: {out.returncode} {out.stdout + out.stderr}"
        )
        assert "marker" in (out.stdout + out.stderr).lower()
    assert target.read_text(encoding="utf-8") == "# nothing here\n", (
        "`--write` wrote into a file with no markers"
    )


def test_a_template_that_cannot_be_read_exits_2(tmp_path):
    """The other file the script cannot proceed without."""
    _, target = copies(tmp_path)
    out = run("--check", "--template", str(tmp_path / "missing.md"), "--target", target)
    assert out.returncode == 2, out.stdout + out.stderr


def test_exactly_one_mode_is_required():
    """Neither flag, or both, is a usage error and not a silent check."""
    out = run()
    assert out.returncode == 2, out.stdout + out.stderr
    out = run("--check", "--write")
    assert out.returncode == 2, out.stdout + out.stderr


def test_the_script_asks_nobody_anything():
    """S8: prompt budget zero. The check exits with a message and never a
    question."""
    text = read(SCRIPT)
    assert "input(" not in text and "AskUserQuestion" not in text


# --- the readers -------------------------------------------------------------


def test_install_sh_reads_the_template():
    """`install.sh:43` used to read `$REPO_DIR/CLAUDE.md`, which is the
    generated copy now. The installer reads the source."""
    text = read(INSTALL)
    assert 'SOURCE="$REPO_DIR/templates/claude-md-block.md"' in text, (
        "install.sh does not read the block from the template"
    )
    assert 'SOURCE="$REPO_DIR/CLAUDE.md"' not in text


def test_install_sh_puts_the_template_block_into_a_fresh_target(tmp_path):
    """S7, executed: `bash install.sh <scratch target>` and the file read
    afterwards. The block in the target is the template's block."""
    target = tmp_path / "probe-CLAUDE.md"
    out = subprocess.run(
        ["bash", INSTALL, str(target)],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert block_of(target.read_text(encoding="utf-8")) == read(TEMPLATE)


def test_install_sh_replaces_an_older_block_from_the_template(tmp_path):
    """The update path: a target already holding a block gets the template's
    block in its place, and its own text on either side stays."""
    target = tmp_path / "CLAUDE.md"
    stale = read(TEMPLATE).replace("## Tooling", "## Tooling (old)")
    assert stale != read(TEMPLATE)
    target.write_text(
        "# mine, above\n\n" + stale + "\n# mine, below\n", encoding="utf-8"
    )
    out = subprocess.run(
        ["bash", INSTALL, str(target)],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert out.returncode == 0, out.stdout + out.stderr
    after = target.read_text(encoding="utf-8")
    assert block_of(after) == read(TEMPLATE)
    assert after.startswith("# mine, above\n") and after.endswith("# mine, below\n")


def test_the_runtime_readers_name_the_template_path():
    """`preset-setup` reads the block at runtime from the plugin's cache and
    `update` diffs it from the marketplace clone. Both used to name the
    plugin's `CLAUDE.md`; both name the source now, or they read a copy the
    check does not hold to anything on the machine the skill runs on."""
    for parts in (("preset-setup",), ("update",)):
        text = read(os.path.join(ROOT, "skills", *parts, "SKILL.md"))
        assert "templates/claude-md-block.md" in text, (
            f"{parts[0]} does not name the template"
        )
        assert "plugin's CLAUDE.md" not in text, (
            f"{parts[0]} still reads the plugin's CLAUDE.md"
        )
        assert "marketplaces/specseal/CLAUDE.md" not in text, (
            f"{parts[0]} still diffs against the clone's CLAUDE.md"
        )


def test_hygiene_runs_the_check_on_every_pull_request():
    """The step is what makes the copy a copy rather than a second source.
    Read with comments stripped: a command that exists only in a comment is
    not a step."""
    lines = [
        line
        for line in read(WORKFLOW).splitlines()
        if not line.lstrip().startswith("#")
    ]
    body = "\n".join(lines)
    assert "claude_block.py --check" in body, "hygiene.yml does not run the check"
    step = body[: body.index("claude_block.py --check")]
    step = step[step.rindex("- name:") :]
    assert "base_ref" not in step, (
        "the check is gated on the base branch; the block is read by every "
        "session in this repository, so every pull request is held to it"
    )


# --- the sentence the block changes -------------------------------------------


def test_the_block_sends_a_fresh_repository_to_the_orchestration_file():
    """`spec.md` §*Scope* item 5. The Bootstrap left `skills/implement/SKILL.md`
    in phase 2, so *load the `implement` skill, and follow its Bootstrap
    section* now sends a reader to a section a `Skill implement` load no
    longer carries. The sentence names the file the Bootstrap moved to."""
    block = read(TEMPLATE)
    rule = re.search(r"- \*\*Routing, decided at the start\*\*.*", block).group(0)
    lead = rule[: rule.index("write `seal/specs/")]
    assert "skills/implement/orchestration.md" in lead, (
        "the routing rule still sends the reader to a Bootstrap section the "
        "`implement` skill no longer carries"
    )
    assert "Bootstrap" in lead
