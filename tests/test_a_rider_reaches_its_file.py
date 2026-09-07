"""A deferral is either a rider or a schedulable item, and they live apart.

Thirteen rows sat in `.specseal/follow-up.md`. Classified by their answerer
column, most of them were not "someone should do this" at all — they were
*"if you open this file, do this too"*, which is worth exactly as much as its
chance of reaching the person who opens that file. A file nobody opens to find
out what to work on next has none.

So a rider goes to its coordinate as a `# RIDER:` comment, and
`grep -rn "RIDER:"` is the list. What stays in `follow-up.md` is the narrow
case issue #34 named in its own third checkbox: a schedulable item in a
repository with no tracker.

The failure this guards against is the file quietly refilling. A coordinate-
tied row written here is one nobody at that coordinate will ever see.
"""

import importlib.util
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOLLOW_UP = os.path.join(ROOT, "seal", "follow-up.md")


def _load(name, path):
    """A sibling script by path — `.github/scripts/` is not importable."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


riders = _load(
    "rider_check", os.path.join(ROOT, ".github", "scripts", "rider_check.py")
)
CHECKER = riders.load_checker()

# A coordinate is `path/to/file.ext:123` — the shape a rider is written at.
COORDINATE = re.compile(r"[\w./-]+\.(?:py|md|json|yml|yaml|sh):\d+")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def rows(section):
    """Table rows under one `## ` heading of follow-up.md."""
    text = read(FOLLOW_UP)
    body = text.split(f"## {section}", 1)[1].split("\n## ", 1)[0]
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if set("".join(cells)) <= set(":- ") or cells[0] in ("Item", "Target"):
            continue
        out.append(cells)
    return out


def test_no_schedulable_row_carries_a_coordinate():
    """A row with a `file.py:120` in it is a rider filed where its reader is
    not. The rider list is `grep RIDER:`, and this section is not it."""
    offenders = [
        r
        for r in rows("Schedulable items with nowhere else to go")
        if COORDINATE.search(" ".join(r))
    ]
    assert not offenders, f"coordinate-tied rows in the schedulable list: {offenders}"


def test_the_header_says_what_belongs_and_what_does_not():
    text = read(FOLLOW_UP)
    assert "schedulable item in a repository with no tracker" in text
    assert "Anything tied to a coordinate" in text
    assert 'grep -rn "RIDER:"' in text


def test_the_header_stops_the_answerer_that_is_really_a_condition():
    """The file already forbade a deferral to nobody, and every one of its
    seventeen rows read `repository owner, next time X is opened` — a
    condition wearing a person's clothes. Issue #34 is that pair."""
    text = read(FOLLOW_UP)
    assert "no condition attached" in text
    assert "condition wearing a person's clothes" in text
    for row in rows("Schedulable items with nowhere else to go"):
        assert "next time" not in " ".join(row), row


def test_the_file_records_what_the_move_costs_and_that_it_can_be_overturned():
    """A judgment nobody can find is a judgment nobody can reverse."""
    text = read(FOLLOW_UP)
    assert "Nothing forces a rider to be deleted" in text
    assert "overturned" in text


def test_the_riders_exist_where_the_rows_said_they_would():
    """Every file a row said its rider went to.

    `hooks/worktree-guard.py` is held by `fix/the-guard-that-could-not-read`,
    and its four riders waited a round for that reason. They are planted now
    because the conflict they were avoiding does not exist: the file is the
    same blob at HEAD and at that branch's tip, so nothing there is being
    rewritten yet."""
    for rel in (
        "hooks/optin.py",
        "hooks/review-skill-gate.py",
        "hooks/review-history-guard.py",
        "hooks/cmdline.py",
        "hooks/dispatch.py",
        "hooks/worktree-guard.py",
        "templates/evidence-check.yml",
    ):
        assert "# RIDER:" in read(os.path.join(ROOT, rel)), rel


# Where riders are allowed to live.
#
# This list has now been the defect twice. `templates` was missing, so the
# rider in `templates/evidence-check.yml` was checked by nothing at all.
# `.github` and `tests` were missing for the same reason and cost three more:
# `.github/scripts/fold_ledger.py` and two under `tests/`, one of which had
# never carried a stamp in any form and so was invisible to every case here.
#
# The line the list draws is not "code": `agents/smith.md` and
# `skills/implement/SKILL.md` carry real riders. It is that these roots hold
# what this repository executes or ships, while `docs/`, `CLAUDE.md` and
# `seal/` hold prose ABOUT riders. A description of the convention quotes the
# marker and is not a rider, which is why the block reader below requires the
# marker to sit at the head of a COMMENT rather than merely to appear.
RIDER_ROOTS = list(riders.RIDER_ROOTS)

# What a stamp said before #239, kept so a case can name it and never so one
# can pass it.
OLD_STAMP = re.compile(r"Verified \d{4}-\d{2}-\d{2} at ([0-9a-f]{7,40})\b")


def rider_stamps():
    """(file, line) for every rider in the tree, however it is stamped."""
    found = [(r.rel, r.start) for r in riders.all_riders(ROOT)]
    assert found, "no riders found at all"
    return found


def test_every_rider_carries_a_verification_stamp():
    """A rider that outlives its fix is the cost of this arrangement, and the
    stamp is the mitigation: a reader can tell how old the claim is without
    trusting it. A rider carrying none is indistinguishable from a spent one.

    `tests/test_the_records_can_be_carried_out_and_in.py` held exactly that
    for two releases — a real rider whose staleness line read *"green at
    3f8f846, measured 2026-09-03"*, matching no stamp form, sitting outside
    the roots this file scanned."""
    unstamped = [r.where() for r in riders.all_riders(ROOT) if not r.new]
    assert not unstamped, f"riders with no `Verified … against …@…` stamp: {unstamped}"


def test_no_rider_stamp_names_a_commit():
    """The defect itself, pinned from the other side.

    A feature branch squashes into its release branch and the squash keeps
    none of the branch's own commits, so a stamp naming one resolves to
    nothing for whoever reads it next — on the RELEASE branch, where the
    person who meets it is never the person who wrote it, and with no mistake
    required anywhere. `skills/evidence-check/SKILL.md` cites this failure as
    grounds for the ledger's content anchors; #239 is the same repair reaching
    the mechanism that supplied the evidence."""
    naming = []
    for rel, _line in rider_stamps():
        for chunk in read(os.path.join(ROOT, rel)).split(riders.MARKER)[1:]:
            found = OLD_STAMP.search(chunk.split("\n\n", 1)[0])
            if found:
                naming.append(f"{rel} → {found.group(1)}")
    assert not naming, (
        f"stamps still naming a commit: {naming}. A squash discards it and the "
        "check then fails on a branch nobody who caused it is looking at"
    )


def test_every_rider_stamp_resolves_and_reproduces_its_hash():
    """The replacement for the ancestry check, and the whole of the guarantee.

    OK is the anchor resolving once to content that hashes to what the stamp
    recorded. DRIFTED is it resolving to content that changed — the rider
    firing at whoever edited the unit without answering the comment in it,
    which is the arrival `seal/follow-up.md` moved riders to their coordinates
    to get. BROKEN is it resolving to nothing, to several places, or only by
    resurrection."""
    ok, drifted, problems = riders.check(ROOT, checker=CHECKER)
    assert not problems, "\n".join(f"{s} {w}: {why}" for w, s, why in problems)
    assert ok and not drifted


def test_the_check_asks_git_for_nothing():
    """What actually removes the class, rather than repairing the instance.

    The old check ran `git merge-base --is-ancestor`, so the merge rule could
    reach it. This one resolves an anchor inside a file and hashes it, and a
    squash, a rebase and a fresh shallow clone are all invisible to that. The
    case that used to sit here asserted the clone was not shallow, because
    `git clone --depth 1` left NO stamp resolvable and would have turned the
    one checkout setting that voids the check into the setting that silences
    it. Nothing needs saying about depth any more.

    Pinned by execution rather than by reading: `git` is replaced on PATH with
    a script that RECORDS being called, and the case reads the record.

    A tripwire that only returns a failing code was tried first and proved
    nothing — `subprocess.run` with `capture_output` does not raise, so a call
    whose result the caller ignores leaves the exit code untouched and the
    case passed with a `git status` added to the check. The mutation that
    caught it is the reason this writes a file instead."""
    bin_dir = tempfile.mkdtemp()
    called = os.path.join(bin_dir, "called")
    tripwire = os.path.join(bin_dir, "git")
    with open(tripwire, "w", encoding="utf-8") as f:
        f.write(f'#!/bin/sh\necho "$@" >> "{called}"\nexit 97\n')
    os.chmod(tripwire, 0o755)
    env = dict(os.environ, PATH=bin_dir + os.pathsep + os.environ["PATH"])
    run = subprocess.run(
        [sys.executable, os.path.join(ROOT, ".github", "scripts", "rider_check.py")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert not os.path.exists(called), "the check called git: " + read(
        called
    ).strip().replace("\n", " · ")
    assert run.returncode == 0, (
        f"the check failed for another reason: exit {run.returncode}\n"
        f"{run.stdout}\n{run.stderr}"
    )


# --- the machinery, on fixtures ----------------------------------------------

# Built rather than written, so this file can carry rider fixtures without
# planting riders in itself: every line below opens with `{MARK}` and not with
# a `#`, which is exactly the distinction `comment_blocks` draws.
MARK = "# " + "RIDER:"


def a_module(claim="the claim", stamp="Verified 2026-01-01 against unit@00000000"):
    return (
        "def unit():\n"
        f"    {MARK} {claim}\n"
        f"    # {stamp}\n"
        "    value = 1\n"
        "    return value\n"
    )


def hashed(tmp_path, text, locator="unit", name="m.py"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    digest, why = riders.region_hash(CHECKER, name, locator, text)
    assert digest, why
    return digest


def test_the_hash_does_not_cover_the_rider_that_carries_it(tmp_path):
    """The residual this design exists to answer.

    A rider is a comment inside the file it is about, so a hash covering it
    would be written into the region it hashes and no fixed point would
    exist. Measured when this was designed: twelve of the nineteen riders in
    the tree sat inside the AST span of the unit they were about."""
    plain = "def unit():\n    value = 1\n    return value\n"
    with_rider = a_module()
    assert (
        riders.region_hash(CHECKER, "m.py", "unit", plain)[0]
        == riders.region_hash(CHECKER, "m.py", "unit", with_rider)[0]
    ), "planting a rider changed the hash of the unit it sits in"


def test_editing_a_riders_own_prose_does_not_drift_it(tmp_path):
    """A rider's wording is not what it verified. Reporting a clarification as
    a code change would be false, and would train a reader to re-stamp
    without looking."""
    assert hashed(tmp_path, a_module("the claim")) == hashed(
        tmp_path, a_module("the claim, said at greater length and more clearly")
    )


def test_a_second_rider_in_a_unit_does_not_drift_the_first(tmp_path):
    """Why the rule is EVERY block and not this one. Three files already carry
    more than one rider, so a design where they perturb each other gets worse
    the more the convention is used."""
    one = a_module()
    two = one.replace(
        "    return value\n",
        f"    {MARK} a second claim\n"
        "    # Verified 2026-01-02 against unit@00000000\n"
        "    return value\n",
    )
    assert len(riders.comment_blocks(two.splitlines())) == 2, (
        "the fixture put its second rider straight after the first, so the "
        "two merged into ONE comment run and this case would pass with the "
        "rule applied to `blocks[:1]`. Found by mutating exactly that"
    )
    assert hashed(tmp_path, one) == hashed(tmp_path, two)


def test_a_changed_unit_drifts(tmp_path):
    """The alarm the whole arrangement is for."""
    before = hashed(tmp_path, a_module())
    after = hashed(tmp_path, a_module().replace("value = 1", "value = 2"))
    assert before != after, "changing the code under a rider did not move the hash"


def test_a_vanished_anchor_is_broken_not_drifted(tmp_path):
    """BROKEN stays reserved for the one case where re-reading cannot help,
    because the subject no longer exists. DRIFTED says *go re-read*, which is
    the work; BROKEN says *go edit the stamp*, which is the bookkeeping the
    ledger's design removed."""
    digest, why = riders.region_hash(CHECKER, "m.py", "gone", a_module())
    assert digest is None and "resolves to nothing" in why


def test_the_marker_in_prose_or_a_string_is_not_a_rider():
    """What keeps this file, `rider_check.py` and `seal/follow-up.md` out of
    the corpus they describe. The marker has to sit at the head of a comment,
    not merely appear."""
    text = (
        f'assert "{MARK}" in source\n'
        f"**Anything tied to a coordinate is a `{MARK}` comment.**\n"
        f"| a table cell mentioning {MARK} | and its answerer |\n"
    )
    assert riders.comment_blocks(text.splitlines()) == []


def test_a_comment_block_runs_through_its_blank_comment_lines():
    """`hooks/worktree-guard.py`'s rider carries a bare `#` in the middle of
    it, and a reader that stopped there would hash the rest of the rider as
    though it were code."""
    lines = [
        "def unit():",
        f"    {MARK} first paragraph",
        "    #",
        "    # second paragraph",
        "    value = 1",
    ]
    assert riders.comment_blocks(lines) == [(2, 4)]


def test_a_held_file_is_named_with_the_branch_holding_it():
    """A rider that cannot be planted has to say what unblocks it, or it is a
    deferral to nobody."""
    for target in rows("Riders waiting on a file another branch holds"):
        assert "held by" in target[0], target[0]
        assert target[-1].strip() not in ("", "—"), f"no answerer: {target}"
