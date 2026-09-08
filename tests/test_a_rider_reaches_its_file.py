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


def test_the_header_states_the_stamp_form_riders_actually_carry():
    """`seal/follow-up.md` is where the convention is written down, and it
    described the old form for as long as the old form existed. A rule stated
    in one place and enforced in another drifts, and the direction it drifts
    is always toward the document, because that is what a person reads."""
    text = read(FOLLOW_UP)
    assert "Verified <date> against <anchor>@<hash>" in text
    assert ".github/scripts/rider_check.py" in text
    assert "the date it was read and the content it" in text
    assert "date and SHA it was verified at" not in text, (
        "the header still describes the stamp form #239 removed"
    )


def test_the_round_template_says_why_target_sha_is_exempt():
    """The other half of #239's answer, pinned beside the half it is about.

    135 round records carry a `Target SHA`, and the same squash that orphaned
    the rider stamps runs past every one of them. Leaving it is correct — a
    round record names a MOMENT, `chain_check.py#reachable` already falls back
    to `refs/remotes/pull/<N>/head` which a squash does not touch, and a whole
    reviewed tree has no anchor to write. What is not correct is leaving that
    unwritten, because the next person to count the rows re-opens it.

    The namespace has to be the one the code scans. `PULL_HEADS` is
    `refs/remotes/pull/`, the mirror CI fetches; a reader who runs
    `git for-each-ref 'refs/pull/*/head'` in a working clone gets nothing and
    reads a true ground as false (round 1, deferred).

    This case lives in the rider file rather than beside the other round-record
    cases on purpose: the ticket asked for one answer covering both mechanisms
    so they could not drift into different rules, and a pin in two files is
    how they would."""
    text = read(os.path.join(ROOT, "templates", "sdd-round.md"))
    assert "exempt from the rule" in text
    assert "carried_by_a_pull_head" in text
    assert "refs/remotes/pull/<N>/head" in text
    assert "records a MOMENT" in text


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
HTML_MARK = "<!-- " + "RIDER:"


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
        f'HTML_MARK = "{HTML_MARK}"\n'
        f"a paragraph naming the `{HTML_MARK}` opener in passing\n"
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


def test_a_second_rider_directly_under_the_first_is_its_own_rider():
    """Back-to-back riders merged into one comment run, so `all_riders`
    returned one rider, `Rider.new` read the FIRST stamp, and the second
    rider's hash was never resolved, never compared, and never reported as
    missing. A rider held by nothing is the defect #239 closed for
    `RIDER_ROOTS`; this is the same one inside a block.

    Phase 3 met this shape in its own fixture — the second rider it inserted
    merged into the first — and hardened the fixture without carrying the
    finding to the production reader (round 1, finding 4)."""
    src = (
        "def unit():\n"
        f"    {MARK} first claim\n"
        "    # Verified 2026-01-01 against unit@00000000\n"
        f"    {MARK} second claim, written straight under the first\n"
        "    # Verified 2026-01-02 against unit@deadbeef\n"
        "    value = 1\n"
        "    return value\n"
    )
    blocks = riders.comment_blocks(src.splitlines())
    assert len(blocks) == 2, f"the two riders merged into one block: {blocks}"
    stamps = [r.new.group("hash") for r in riders.riders_in("m.py", src)]
    assert "deadbeef" in stamps, f"the second rider's stamp was never read: {stamps}"


def test_a_second_rider_sharing_one_html_comment_is_its_own_rider():
    """The other half of the case above, found by construction rather than by
    a second finding. Fixing the `#` form and stopping there would leave the
    markdown corpus — `agents/smith.md` and `skills/implement/SKILL.md` carry
    real riders — holding the defect the `#` form had just been cleared of.

    A second marker before the closing `-->` opens a second rider inside the
    same comment, so the line that opens it carries no `<!--` of its own."""
    src = (
        "## Heading\n"
        "\n"
        f"{HTML_MARK} first claim\n"
        '     Verified 2026-01-01 against "## Heading"@00000000.\n'
        f"     {'RIDER:'} second claim, written into the same comment\n"
        '     Verified 2026-01-02 against "## Heading"@deadbeef. -->\n'
    )
    blocks = riders.comment_blocks(src.splitlines())
    assert len(blocks) == 2, f"the two riders merged into one block: {blocks}"
    stamps = [r.new.group("hash") for r in riders.riders_in("d.md", src) if r.new]
    assert "deadbeef" in stamps, f"the second rider's stamp was never read: {stamps}"


def test_a_markdown_heading_naming_the_marker_is_not_a_rider():
    """`comment_blocks`'s own docstring gives the `#` form to Python, YAML and
    shell and gives markdown the HTML comment. The code asked only that the
    stripped line start with `#`, which in markdown is a HEADING, so a heading
    naming the marker became a rider with no stamp and the check exited 2 on a
    line nobody wrote as a rider. The mirror of the HTML opener `923f86c`
    closed — a reader looser than the paragraph above it (round 2, finding 11).

    Every other loss this design states for itself loses an alarm. This was
    the one place it invented one, which is why it is the mirror and not the
    twin."""
    src = f"# Title\n\n## {'RIDER:'} what one is\n\nprose.\n"
    assert riders.comment_blocks(src.splitlines(), "skills/x/SKILL.md") == []
    assert riders.riders_in("skills/x/SKILL.md", src) == []
    # the two real forms are untouched
    py = f"def u():\n    {MARK} claim\n    # Verified 2026-01-01 against u@00000000\n"
    assert riders.comment_blocks(py.splitlines(), "hooks/m.py") == [(2, 3)]
    md = (
        f"## H\n\n{HTML_MARK} claim\n"
        '     Verified 2026-01-01 against "## H"@00000000. -->\n'
    )
    assert riders.comment_blocks(md.splitlines(), "a.md") == [(3, 4)]


def test_the_hasher_reads_a_markdown_heading_the_same_way_the_reader_does():
    """`region_lines` had `rel` in scope and passed it to nothing, so the two
    callers of `comment_blocks` would have disagreed about what a block is the
    moment the reader learned about markdown: the reader returns no rider for
    a `#`-headed heading and the hasher would still cut that line out of the
    region it hashes. Found by enumerating the call sites of the fix above
    rather than by a finding.

    The marker heading is one level DEEPER than the anchor, so it sits inside
    the region rather than ending it — a sibling heading closes the section and
    would be outside the hash for a reason that has nothing to do with this."""
    src = f"## H\n\nprose under it.\n\n### {'RIDER:'} what one is\n\nmore prose.\n"
    assert riders.comment_blocks(src.splitlines(), "a.md") == []
    kept, why = riders.region_lines(CHECKER, "a.md", '"## H"', src)
    assert kept is not None, why
    assert any("RIDER:" in line for line in kept), (
        "the hasher excluded a markdown heading the reader does not read as a "
        f"rider, so the two disagree: {kept}"
    )


def stamped_module(tmp_path, digest=None, date="2026-01-01"):
    """A rider file under `hooks/`, stamped with its own true hash by default."""
    d = tmp_path / "hooks"
    d.mkdir(exist_ok=True)
    src = a_module(stamp=f"Verified {date} against unit@00000000")
    if digest is None:
        digest, why = riders.region_hash(CHECKER, "hooks/m.py", "unit", src)
        assert digest, why
    src = src.replace("unit@00000000", f"unit@{digest}")
    (d / "m.py").write_text(src, encoding="utf-8")
    return src


def test_reverify_does_not_move_a_date_whose_hash_did_not_move(tmp_path):
    """What `--reverify` may move and what it may not.

    The skip condition required the hash AND the date to match, so a rider
    whose region hashed to exactly what its stamp recorded — nobody edited it,
    nobody re-read it — was rewritten because the date differed. That is a
    stamp asserting a reading that did not happen, which is the half
    `--migrate` refuses to manufacture arriving from the writer instead, and
    it erased twelve original dates this migration had proved (round 1,
    findings 1 and 2). It also drifted the ledger row of a unit nobody had
    touched, because a ledger hash covers comments (finding 3)."""
    before = stamped_module(tmp_path)
    written, refused = riders.reverify(
        str(tmp_path), roots=("hooks",), today="2026-12-31", checker=CHECKER
    )
    assert not written and not refused, (written, refused)
    after = (tmp_path / "hooks" / "m.py").read_text(encoding="utf-8")
    assert after == before, (
        "`--reverify` moved the date of a rider whose content had not moved:\n"
        f"{before!r}\n{after!r}"
    )


def test_reverify_still_moves_the_date_of_a_rider_that_did_change(tmp_path):
    """The other half, so the case above cannot be passed by doing nothing."""
    stamped_module(tmp_path, digest="00000000")
    written, refused = riders.reverify(
        str(tmp_path), roots=("hooks",), today="2026-12-31", checker=CHECKER
    )
    assert len(written) == 1 and not refused, (written, refused)
    after = (tmp_path / "hooks" / "m.py").read_text(encoding="utf-8")
    assert "Verified 2026-12-31 against unit@" in after, after


def test_reverify_says_so_when_only_selects_no_rider(tmp_path):
    """`--only` selects by exact relative path. One that matches nothing
    printed `0 restamped · 0 refused` and exited 0, so a reader answering a
    drifted rider read success for a run that wrote nothing — and exit 0 is
    what a script reads (round 2, finding 10)."""
    stamped_module(tmp_path, digest="00000000")
    written, refused = riders.reverify(
        str(tmp_path),
        only="hooks/no-such-file.py",
        roots=("hooks",),
        today="2026-12-31",
        checker=CHECKER,
    )
    assert not written and len(refused) == 1, (written, refused)
    assert "no rider in the tree has this path" in refused[0][1], refused


def test_only_without_a_verb_is_refused_rather_than_ignored(tmp_path):
    """`--only` scopes `--reverify` and nothing else. Typed without it, or
    beside `--migrate`, argparse accepted it and every code path ignored it:
    the whole tree was checked and `20 ok · 0 drifted · 0 broken` printed at
    exit 0, so a person who scoped the run read success for a run that ignored
    their argument. The same cause as finding 10 one argument over — an input
    accepted and silently dropped — found by enumerating the entry points
    rather than by a finding."""
    stamped_module(tmp_path)
    for argv in (
        ["--root", str(tmp_path), "--only", "hooks/m.py"],
        ["--root", str(tmp_path), "--migrate", "--only", "hooks/m.py"],
    ):
        assert riders.main(argv) == 2, argv


def test_the_drift_message_says_the_re_stamp_takes_a_file(tmp_path):
    """`--only` selects a FILE, not a rider. Three files carry more than one
    rider, so a reader who answers one drifted rider with the command this
    message hands them re-stamps every other drifted rider in the same file —
    asserting they read those too. The message has to say so (round 1,
    finding 2, second half)."""
    stamped_module(tmp_path, digest="00000000")
    ok, drifted, problems = riders.check(
        str(tmp_path), roots=("hooks",), checker=CHECKER
    )
    assert (ok, drifted, len(problems)) == (0, 1, 1), (ok, drifted, problems)
    _where, severity, sentence = problems[0]
    assert severity == "DRIFTED"
    assert "--reverify --only hooks/m.py" in sentence, sentence
    assert "takes a FILE" in sentence and "read the others" in sentence, sentence


def test_a_refusal_names_which_of_the_three_things_failed(repo):
    """`content_at` returned None for any non-zero exit and `--migrate`
    printed one sentence for it: *git cannot resolve <sha> any more*. Three
    different things fail there and they are three different repairs. The
    migration's own headline evidence was a stamp whose commit git resolves
    perfectly well — the file simply was not in that tree — read as the squash
    orphaning a stamp in the act (round 1, finding 6)."""
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.strip()

    text, why = riders.content_at(str(repo), head, "f.txt")
    assert why is None and text == "one\ntwo\nthree\n", (text, why)

    (repo / "later.py").write_text("x = 1\n", encoding="utf-8")
    text, why = riders.content_at(str(repo), head, "later.py")
    assert text is None and "resolves, but" in why and "later.py" in why, why

    text, why = riders.content_at(str(repo), "0" * 40, "f.txt")
    assert text is None and "cannot resolve" in why, why


def test_a_held_file_is_named_with_the_branch_holding_it():
    """A rider that cannot be planted has to say what unblocks it, or it is a
    deferral to nobody."""
    for target in rows("Riders waiting on a file another branch holds"):
        assert "held by" in target[0], target[0]
        assert target[-1].strip() not in ("", "—"), f"no answerer: {target}"
