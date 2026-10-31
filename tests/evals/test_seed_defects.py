"""`evals/scripts/seed_defects.py`, one class per function.

The seeded generator plants one defect in a shipped commit's round 1
target and counts round 1's confirmed fixes as the case's truths. These
cases pin the target it builds on, the commits it leaves out, the scaffold
that leaves round 1's tree and no copy of it, and that a seed lands on a
code token. `test_the_replay_and_seeded_generators_read_the_entries_too`
holds the replay generator too, because both read the recurred entries.

#942's phase 6 placed these cases from
`tests/behaviour/test_a_rewritten_definition_proved_non_inferior.py`.
"""

import os
import re
import subprocess

import pytest
from conftest import census_case, commit_everything_as_e, git_out, write
from test_replay_targets import (
    LABELLED_ROUND_1,
    LABELLED_ROUND_2,
    labelled_check_files,
    load_script,
)
from test_rule_cases import entry, recurred_file, truth_regex

TARGET = "evals/scripts/seed_defects.py"

TRUTH = r"^location: .*(?:src\/a\.py:(?:10|11|12)(?!\d))"

SEEDED_ITEM = "1790000001-a-shipped-item"
SEEDED_BRANCH = "feat/1-a-shipped-item"
# Two units 38 lines apart, so the window of round 1's finding at line 2
# reaches the first and not the second.
SEEDED_SOURCE = (
    "def f(a):\n    return a == 1\n" + "\n" * 34 + "\n\ndef g(b):\n    return b != 2\n"
)


def seeded_round_1(target):
    """Round 1 of the shipped item, written before the `evidence:` row: its
    TARGET against `main`, a branch the clone has no ref for, a finding at
    `a.py:2` closed fixed and one at `b.py:1` rejected."""
    return re.sub(
        r"^evidence: .*\n",
        "",
        LABELLED_ROUND_1.replace("# i ", f"# {SEEDED_ITEM} ")
        .replace("1a2b3c4 against main", f"{target} against main")
        .replace("`src/a.py:12`, `docs/a.md`", "`a.py:2`")
        .replace("`src/b.py:3`", "`b.py:1`"),
        flags=re.M,
    )


# The two layouts a release has kept its round records in, as `(the
# directory a work item's directory stands in, the directory of its round
# records under it)`.
LAYOUTS = [("seal/specs", "rounds"), ("seal/threads", "trail/rounds")]


def shipped_item(
    tmp_path,
    monkeypatch,
    first=seeded_round_1,
    second=True,
    crlf=False,
    layout=LAYOUTS[0],
):
    """A repository that shipped one work item, with `rt` reading it: a base
    holding the check of a grammar with no `evidence:` row, a branch of a
    code commit and a records commit, and the branch squashed onto the base
    with round 1, FIRST of the target, and round 2 where SECOND is set,
    added as a shipped squash commit holds them, in LAYOUT. No `main` ref
    but the local branch exists, so the squash's first parent stands for
    the base round 1 names. Every file is written with LF line ends and
    stored as written, `a.py` with CRLF where CRLF is set. `({name:
    commit}, its path)`."""
    rt = load_script("seed_defects").rt
    repo = tmp_path / "shipped"
    repo.mkdir()
    who = ["-c", "user.name=x", "-c", "user.email=x@example.com"]
    # A fixed date, so a commit the scaffold amends today cannot match it.
    dated = dict(os.environ, GIT_COMMITTER_DATE="2026-01-01T00:00:00+00:00")

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(repo), *who, *args],
            check=True,
            capture_output=True,
            encoding="utf-8",
            env=dated,
        ).stdout.strip()

    def put(rel, text, newline="\n"):
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline=newline)

    git("init", "-q", "-b", "main")
    git("config", "uploadpack.allowAnySHA1InWant", "true")
    git("config", "core.autocrlf", "false")
    for rel, text in labelled_check_files().items():
        # The check of the last release that read labelled lines, at the one
        # path of `CHECK_FILES` it holds each file at.
        if rel == "docs/the-review-record.md":
            text = re.sub(r"^\| `evidence:` \|.*\n", "", text, flags=re.M)
        put(rel, text)
    put("b.py", "x = 1\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    commits = {"base": git("rev-parse", "HEAD")}
    git("checkout", "-q", "-b", SEEDED_BRANCH)
    home, rounds = layout
    spec = f"{home}/{SEEDED_ITEM}"
    put(
        f"{spec}/routing.md",
        f"| Axis | Answer |\n|---|---|\n| Branch | {SEEDED_BRANCH} |\n",
    )
    put("a.py", SEEDED_SOURCE, newline="\r\n" if crlf else "\n")
    git("add", "-A")
    git("commit", "-qm", "feat: f and g")
    commits["code"] = git("rev-parse", "HEAD")
    put(
        f"{spec}/plan.md", f"| Phase | Status |\n|---|---|\n| 1 | {commits['code']} |\n"
    )
    git("add", "-A")
    git("commit", "-qm", "record: phase 1")
    commits["target"] = git("rev-parse", "HEAD")
    git("checkout", "-q", "main")
    git("merge", "-q", "--squash", SEEDED_BRANCH)
    put(f"{spec}/{rounds}/round-1.md", first(commits["target"]))
    if second:
        put(f"{spec}/{rounds}/round-2.md", LABELLED_ROUND_2)
    git("add", "-A")
    git("commit", "-qm", "feat: a shipped item (#1)")
    commits["squash"] = git("rev-parse", "HEAD")
    monkeypatch.setattr(rt, "ROOT", str(repo))
    return commits, repo


def two_near_fixes(target):
    """Round 1 with both findings closed fixed, three lines apart."""
    return (
        seeded_round_1(target)
        .replace("`b.py:1`", "`a.py:5`")
        .replace("verdict: rejected", "verdict: fixed abc1234")
    )


def based_repo(tmp_path, monkeypatch):
    """A repository holding one base commit, with `rt` reading it: `(the
    repository, the base commit)`."""
    rt = load_script("seed_defects").rt
    repo = tmp_path / "based"
    repo.mkdir()
    git_out(repo, "init", "-q")
    write(repo, "b.py", "x = 1\n")
    base = commit_everything_as_e(repo, "base")
    monkeypatch.setattr(rt, "ROOT", str(repo))
    return repo, base


class Test_seed:
    def test_accepts_the_first_operator_in_order_on_a_line_two_could_take(
        self, tmp_path, monkeypatch
    ):
        """Guards the operator order: on an added line two operators land on
        once, the seed is the first of `OPERATORS`, with the whole line before
        and after and the unit it stands in."""
        sd = load_script("seed_defects")
        repo, base = based_repo(tmp_path, monkeypatch)
        write(repo, "a.py", "def f(a, b):\n    return a and b == 1\n")
        target = commit_everything_as_e(repo, "target")
        assert sd.seed(base, target) == (
            "a.py",
            2,
            "    return a and b == 1",
            "    return a and b != 1",
            ["f"],
        )

    @pytest.mark.parametrize(
        ("source", "line", "unit"),
        [
            ("X = 1 == 1\n\n\ndef f(a):\n    return a != 2\n", 5, ["f"]),
            ('def f(a):\n    s = "a == b"\n    return a != 2\n', 3, ["f"]),
            (
                "def f(a):\n    return a == 1\n\n\ndef g(a):\n    return a == 1\n"
                "\n\ndef h(a):\n    return a != 2\n",
                10,
                ["h"],
            ),
        ],
        ids=["outside-any-unit", "inside-a-string", "whose-text-occurs-twice"],
    )
    def test_refuses_a_line_no_seed_may_take(
        self, tmp_path, monkeypatch, source, line, unit
    ):
        """Guards sd9, sd6 and sd8 of #1017: an added line outside every
        `def` and `class`, an operator inside a string, and a line whose text
        the file holds twice take no seed, so a mutation always lands on one
        code token a unit owns. Each source puts that line first, and the seed
        goes to the line after it."""
        sd = load_script("seed_defects")
        repo, base = based_repo(tmp_path, monkeypatch)
        write(repo, "a.py", source)
        target = commit_everything_as_e(repo, "target")
        assert sd.seed(base, target) == (
            "a.py",
            line,
            "    return a != 2",
            "    return a == 2",
            unit,
        )


class Test_target_of:
    @pytest.mark.parametrize("layout", LAYOUTS, ids=["specs", "threads"])
    def test_accepts_a_shipped_commit_and_builds_its_case_on_round_1s_target(
        self, tmp_path, monkeypatch, layout
    ):
        """Guards S8: a seeded case is the tree the shipped item's round 1
        reviewed, not the squash commit. Its scaffold fetches round 1's target
        and base, removes no file, and after the amend expires the reflog,
        removes `FETCH_HEAD` and prunes what nothing reaches. Its prompt names
        HEAD and round 1's base, and no commit of the tree without the seed.
        A work item in either layout a release has kept its records in is
        found by the `routing.md` the commit adds, and the report is written
        in its layout (#1150); the reader of one layout left a thread-layout
        item out as adding no work item."""
        sd = load_script("seed_defects")
        commits, _repo = shipped_item(tmp_path, monkeypatch, layout=layout)
        t, why = sd.target_of(commits["squash"])
        assert why == "", why
        assert (t["target"], t["base"], t["base_ref"], t["branch"]) == (
            commits["target"],
            commits["base"],
            "origin/main",
            SEEDED_BRANCH,
        )
        lines = sd.scaffold(t, "https://example.com/x/y.git").split("\n")
        assert lines[:6] == [
            "git init -q .",
            "git remote add origin https://example.com/x/y.git",
            f"git fetch -q --no-tags origin {commits['target']}",
            f"git fetch -q --no-tags origin {commits['base']}",
            f"git update-ref refs/remotes/origin/main {commits['base']}",
            f"git checkout -q -b {SEEDED_BRANCH} {commits['target']}",
        ]
        assert lines[-3:] == [
            "git reflog expire --expire=now --all",
            "rm -f .git/FETCH_HEAD",
            "git gc -q --prune=now",
        ]
        assert not any(line.startswith("git rm") for line in lines), lines
        prompt = sd.prompt(t)
        assert f"on branch `{SEEDED_BRANCH}` at HEAD" in prompt
        assert f"the base is `{commits['base']}`" in prompt
        assert commits["target"] not in prompt and commits["squash"] not in prompt
        report = f"{layout[0]}/{SEEDED_ITEM}/{layout[1]}/round-1.md"
        assert f"Write the report to `{report}`" in prompt
        assert f"run `cat {report}` once" in prompt

    @pytest.mark.parametrize("layout", LAYOUTS, ids=["specs", "threads"])
    def test_a_seeded_case_counts_round_1s_confirmed_fixes_as_truths(
        self, tmp_path, monkeypatch, layout
    ):
        """Guards S9: at round 1's target the tree holds the defects round 1
        found, so each finding round 1 closed fixed that round 2 confirmed is a
        `truth-` grader beside `truth-seeded`, and the seed lands on no line a
        truth's window accepts: `f`'s line is in finding 1's window, so the
        seed goes to `g`. Round 2 is read in round 1's layout, either of the
        two (#1150)."""
        sd = load_script("seed_defects")
        commits, _repo = shipped_item(tmp_path, monkeypatch, layout=layout)
        t, _why = sd.target_of(commits["squash"])
        assert (t["path"], t["line"], t["new"]) == ("a.py", 40, "    return b == 2")
        truths = {
            name: truth_regex(name, text)
            for name, text in sd.graders(t)
            if name.startswith("truth-")
        }
        assert sorted(truths) == ["truth-1.md", "truth-seeded.md"]
        assert truths["truth-1.md"].search("location: `a.py:2`")
        for n in range(1, 60):
            row = f"location: `a.py:{n}`"
            assert sum(bool(g.search(row)) for g in truths.values()) <= 1, row

    def test_a_seeded_case_needs_no_round_after_round_1(self, tmp_path, monkeypatch):
        """Guards what the seeded generator asks of a round that the replay
        generator does not: a work item whose round 1 no round followed still
        gives a case, its one truth the seed. A replay of that round has
        nothing to confirm a fix and is left out."""
        sd = load_script("seed_defects")
        commits, _repo = shipped_item(tmp_path, monkeypatch, second=False)
        t, why = sd.target_of(commits["squash"])
        assert why == "", why
        assert t["truths"] == []
        names = [name for name, _ in sd.graders(t) if name.startswith("truth-")]
        assert names == ["truth-seeded.md"]

    def test_refuses_a_shipped_commit_whose_round_1_truths_share_a_line(
        self, tmp_path, monkeypatch
    ):
        """Guards S9's rule that one finding is never counted as two: where two
        findings round 1 fixed lie so near that both truths accept one
        `location:` line, the generator leaves the commit out, naming the line,
        rather than writing a case the suite then refuses (`questions.md` Q3
        of #986)."""
        sd = load_script("seed_defects")
        commits, _repo = shipped_item(tmp_path, monkeypatch, first=two_near_fixes)
        t, why = sd.target_of(commits["squash"])
        assert t is None
        assert why == "two of round 1's truths accept `location: `a.py:1``", why

    @pytest.mark.parametrize(
        ("rel", "text", "why"),
        [
            ("b.py", "x = 2\n", "adds 0 work items' routing.md"),
            (
                "seal/specs/1790000002-an-unreviewed-item/routing.md",
                "| Axis | Answer |\n|---|---|\n| Branch | feat/2-an-unreviewed-item |\n",
                "holds no round 1 record",
            ),
            (
                "seal/threads/1790000002-an-unreviewed-item/routing.md",
                "| Axis | Answer |\n|---|---|\n| Branch | feat/2-an-unreviewed-item |\n",
                "holds no round 1 record",
            ),
        ],
        ids=[
            "adds-no-work-item",
            "holds-no-round-1-record",
            "holds-no-round-1-record-in-the-thread-layout",
        ],
    )
    def test_refuses_a_squashed_pull_request_with_no_round_1_to_seed(
        self, tmp_path, monkeypatch, rel, text, why
    ):
        """Guards sd2 and sd3 of #1017: a squashed pull request that adds no
        work item's `routing.md`, such as a dependency bump, and a work item
        shipped with no review round have no round 1 tree to seed. Each is
        left out saying which, and neither is read as a work item."""
        sd = load_script("seed_defects")
        repo, _base = based_repo(tmp_path, monkeypatch)
        write(repo, rel, text)
        shipped = commit_everything_as_e(repo, "feat: a shipped change (#2)")
        assert sd.target_of(shipped) == (None, why)


class Test_module:
    def test_a_seeded_case_is_looked_for_among_the_named_commits_alone(
        self, monkeypatch
    ):
        """Guards what reading every release tag costs the seeded generator: a
        shipped commit `--case` does not name is skipped before any git call
        for it, so the whole history is listed and only the named commits are
        read. The wiring case, `tests/evals/test_replay_targets.py`'s
        `test_a_named_case_is_read_at_every_release_tag`, stubs `targets`, so
        only this one reaches the filter."""
        sd = load_script("seed_defects")
        monkeypatch.setattr(
            sd, "shipped", lambda _tags: ["aaaaaaaa1111", "bbbbbbbb2222"]
        )
        monkeypatch.setattr(sd.rt, "git", lambda *_a, **_k: "")
        kept, left, held = sd.targets(["v1.0.0"], {"aaaaaaaa"})
        assert (kept, held) == ([], 0)
        assert left == [("aaaaaaaa1111", "not a squashed pull request")]
        assert len(sd.targets(["v1.0.0"])[1]) == 2

    def test_says_so_and_exits_1_where_no_commit_holds_a_round_1_record(
        self, tmp_path, monkeypatch, capsys
    ):
        """Guards #1150's silent read on the seeded side: over commits none of
        which holds a round 1 record in either layout, the run still prints
        each commit's `left out:` line, then names both layouts and the tags
        on stderr and exits 1. Seen red against its exit 0, where the
        thread-layout item read as adding no work item."""
        sd = load_script("seed_defects")
        repo, _base = based_repo(tmp_path, monkeypatch)
        write(repo, "b.py", "x = 2\n")
        bump = commit_everything_as_e(repo, "chore: a bump (#2)")
        write(
            repo,
            "seal/threads/1790000003-an-unreviewed-item/routing.md",
            "| Axis | Answer |\n|---|---|\n| Branch | feat/3-an-unreviewed-item |\n",
        )
        item = commit_everything_as_e(repo, "feat: an unreviewed item (#3)")
        monkeypatch.setattr(sd.rt, "last_tags", lambda count=2: ["v1.1.0", "v1.0.0"])
        monkeypatch.setattr(sd, "shipped", lambda _tags: [item, bump])
        assert sd.main(["--list"]) == 1
        said = capsys.readouterr()
        assert said.out == (
            f"{item[:8]} left out: holds no round 1 record\n"
            f"{bump[:8]} left out: adds 0 work items' routing.md\n"
        )
        assert said.err == (
            "seed_defects: no shipped commit read at v1.1.0, v1.0.0 holds a round 1 "
            "record in `seal/specs/<item>/rounds/` or "
            "`seal/threads/<item>/trail/rounds/`\n"
        )
        # One commit that holds a round 1 record is a read, whatever its case.
        commits, _repo = shipped_item(tmp_path, monkeypatch, layout=LAYOUTS[1])
        monkeypatch.setattr(sd, "shipped", lambda _tags: [commits["squash"]])
        assert sd.main(["--list"]) == 0
        assert capsys.readouterr().err == ""

    def test_names_each_named_case_no_shipped_commit_answers_with_its_reason(
        self, tmp_path, monkeypatch, capsys
    ):
        """Guards `--case` answering a name as `replay_targets.py` answers it
        (#1150): a name no listed line answers, or without `--list` no
        written case, is said on stderr with why, and the run exits 1, where
        it said nothing and `--list` exited 0 while another named commit held
        a round 1 record. A name a kept or a `left out:` line answers is said
        there alone, and a run that read no round 1 record still says that
        after the names. Seen red against that silence. The reason for a
        name no commit read answers says what the run read, and not that no
        release shipped the commit (round 2's finding 1); seen red against
        that reason. A name is read only in a case's form, `seeded-` and
        eight lower-case hex digits, and any other name is answered with
        that form: the bare digits of a commit the run listed, and a full
        SHA, were told no shipped commit read had them (round 3's finding
        1); seen red against that reason. A name given twice is one name,
        where the run that wrote its case exited 1 saying nothing; seen red
        against that exit 1."""
        sd = load_script("seed_defects")
        commits, repo = shipped_item(tmp_path, monkeypatch)
        write(repo, "b.py", "x = 2\n")
        bump = commit_everything_as_e(repo, "chore: a bump (#2)")
        monkeypatch.setattr(sd.rt, "last_tags", lambda count=2: ["v1.1.0", "v1.0.0"])
        monkeypatch.setattr(sd, "shipped", lambda _tags: [commits["squash"], bump])
        monkeypatch.setattr(sd.rt, "origin_url", lambda: "https://example.com/x/y.git")
        kept = f"seeded-{commits['squash'][:8]}"
        gone = f"seeded-{bump[:8]}"
        nothing = "seeded-12345678"
        unshipped = (
            "seed_defects: seeded-12345678 not written: no shipped commit read "
            "has 12345678 as its first eight digits\n"
        )

        def case(*names, run=("--list",)):
            return sd.main([*run, *[x for n in names for x in ("--case", n)]])

        assert case(kept, gone, nothing) == 1
        said = capsys.readouterr()
        assert said.out.splitlines()[1:] == [
            f"{bump[:8]} left out: adds 0 work items' routing.md"
        ]
        assert said.err == unshipped
        assert case(kept, gone) == 0
        assert capsys.readouterr().err == ""
        form = (
            " not written: a case is named seeded-<a shipped commit's first "
            "eight hex digits, in lower case>\n"
        )
        sha = commits["squash"]
        bare = kept.removeprefix("seeded-")
        assert case(kept, f"seeded-{sha}", bare) == 1
        said = capsys.readouterr()
        assert said.out.startswith(f"{bare} a.py:"), said.out
        assert said.err == f"seed_defects: seeded-{sha}{form}seed_defects: {bare}{form}"
        out = ("--out", str(tmp_path / "out"))
        assert case(kept, kept, run=out) == 0
        assert capsys.readouterr().err == ""
        assert case(kept, gone, nothing, run=out) == 1
        said = capsys.readouterr()
        assert said.out.startswith(f"{kept}: a.py#g, "), said.out
        assert said.err == (
            f"seed_defects: {gone} not written: adds 0 work items' routing.md\n"
            + unshipped
        )
        empty = (
            "seed_defects: no shipped commit read at v1.1.0, v1.0.0 holds a round 1 "
            "record in `seal/specs/<item>/rounds/` or "
            "`seal/threads/<item>/trail/rounds/`\n"
        )
        assert case(nothing) == 1
        assert capsys.readouterr().err == unshipped + empty
        assert case(nothing, run=out) == 1
        assert capsys.readouterr().err == unshipped + empty
        assert case(bare, run=out) == 1
        assert capsys.readouterr().err == f"seed_defects: {bare}{form}" + empty

    def test_the_replay_and_seeded_generators_read_the_entries_too(
        self, tmp_path, monkeypatch
    ):
        """Guards S6 for the other two generators: each writes an entry's truth
        for the case it names, beside its own."""
        rt = load_script("replay_targets")
        sd = load_script("seed_defects")
        replay = "replay-1791382684-r2"
        seeded = "seeded-279a580b"
        path = recurred_file(
            tmp_path, entry(case=replay, locations=["x.py"]), entry(case=seeded)
        )
        monkeypatch.setattr(rt, "TRUTHS", path)
        monkeypatch.setattr(sd.rt, "TRUTHS", path)
        t = {
            "item": "1791382684-every-reader-and-record-is-inventoried",
            "n": 2,
            "report": "seal/threads/1791382684-a/trail/rounds/round-2.md",
            "target": "HEAD",
            "truths": [{"k": 1, "finding": "f", "pattern": TRUTH}],
        }
        assert [name for name, _ in rt.graders(t) if name.startswith("truth-")] == [
            "truth-1.md",
            "truth-no-case.md",
        ]
        s = {
            "commit": "279a580b" + "0" * 32,
            "item": "1791384154-a-records-finding-closes-once-at-the-runs-end",
            "n": 1,
            "report": "seal/threads/1791384154-a/trail/rounds/round-1.md",
            "target": "HEAD",
            "truths": [],
            "path": "a.py",
            "unit": "f",
            "old": "a == b",
            "new": "a != b",
            "pattern": TRUTH,
        }
        assert [name for name, _ in sd.graders(s) if name.startswith("truth-")] == [
            "truth-seeded.md",
            "truth-no-case.md",
        ]

    def test_a_seed_lands_on_a_code_token_and_never_in_a_string(self):
        sd = load_script("seed_defects")
        source = 'def f(a):\n    """a == b"""\n    return a == 1\n'
        tokens = sd.code_tokens(source)
        assert (3, "==") in tokens
        assert (2, "==") not in tokens

    def test_the_seeded_scaffold_leaves_round_1s_tree_and_no_copy_of_it(
        self, tmp_path, monkeypatch
    ):
        """Guards S10 on a repository a case can fetch for nothing: the clone
        holds no round record, the commit the plan's Status cell names
        resolves, the target's own commit does not, and no file under `.git`
        outside its objects names it. The amended commit keeps the target's
        committer and date, so no field of the log marks the seed's commit, and
        the clone keeps no remote (`seed_defects.py`'s module docstring says
        what that closes and what it leaves), while the base ref round 1 names
        still resolves."""
        sd = load_script("seed_defects")
        commits, repo = shipped_item(tmp_path, monkeypatch)
        t, _why = sd.target_of(commits["squash"])
        clone = tmp_path / "clone"
        clone.mkdir()
        (clone / "scaffold.sh").write_text(
            # A URL, as `replay_targets.py#origin_url` gives the generator: a
            # native Windows path in an unquoted `sh` word loses its backslashes.
            "set -eu\n" + sd.scaffold(t, repo.as_uri()) + "\n",
            encoding="utf-8",
        )
        run = subprocess.run(
            ["sh", "scaffold.sh"], cwd=clone, capture_output=True, encoding="utf-8"
        )
        assert run.returncode == 0, run.stderr
        assert not (clone / "seal" / "specs" / SEEDED_ITEM / "rounds").exists()
        assert (clone / "a.py").read_text(encoding="utf-8").split("\n")[39] == (
            "    return b == 2"
        )

        def exists(rev):
            return subprocess.run(
                ["git", "-C", str(clone), "cat-file", "-e", f"{rev}^{{commit}}"],
                capture_output=True,
            ).returncode

        assert exists(commits["code"]) == 0
        assert exists(commits["target"]) != 0
        named = []
        for directory, dirs, files in os.walk(clone / ".git"):
            if "objects" in dirs:
                dirs.remove("objects")
            for name in files:
                path = os.path.join(directory, name)
                with open(path, "rb") as f:
                    if commits["target"].encode() in f.read():
                        named.append(path)
        assert named == [], named

        def log(where, rev):
            return subprocess.run(
                ["git", "-C", str(where), "log", "-1", "--format=%cn %ce %cI", rev],
                capture_output=True,
                encoding="utf-8",
            ).stdout

        assert log(clone, "HEAD") == log(repo, commits["target"]) != ""
        remotes = subprocess.run(
            ["git", "-C", str(clone), "remote"], capture_output=True, encoding="utf-8"
        )
        assert (remotes.returncode, remotes.stdout) == (0, "")
        assert exists("origin/main") == 0

    @pytest.mark.parametrize(
        ("crlf", "autocrlf"),
        [(False, "true"), (True, "false")],
        ids=["an-lf-file-checked-out-with-crlf", "a-file-stored-with-crlf"],
    )
    def test_the_seeded_scaffold_mutates_a_line_that_ends_with_crlf(
        self, tmp_path, monkeypatch, crlf, autocrlf
    ):
        """Guards the scaffold's own check of the line it mutates, on every
        platform. Git for Windows checks a file out with CRLF line ends
        (`core.autocrlf`), so the line read from the checkout carries a carriage
        return, which `tests` run 39691387210 met on a Windows split; a file
        stored with CRLF carries one in the commit too. The carriage return is
        the line's end, not its text: the seed is found and written without it,
        and the mutated line keeps it."""
        sd = load_script("seed_defects")
        commits, repo = shipped_item(tmp_path, monkeypatch, crlf=crlf)
        t, why = sd.target_of(commits["squash"])
        assert why == "", why
        assert (t["line"], t["old"], t["new"]) == (
            40,
            "    return b != 2",
            "    return b == 2",
        )
        clone = tmp_path / "clone"
        clone.mkdir()
        (clone / "scaffold.sh").write_text(
            "set -eu\n" + sd.scaffold(t, repo.as_uri()) + "\n", encoding="utf-8"
        )
        env = dict(
            os.environ,
            GIT_CONFIG_COUNT="1",
            GIT_CONFIG_KEY_0="core.autocrlf",
            GIT_CONFIG_VALUE_0=autocrlf,
        )
        run = subprocess.run(
            ["sh", "scaffold.sh"],
            cwd=clone,
            capture_output=True,
            encoding="utf-8",
            env=env,
        )
        assert run.returncode == 0, run.stderr
        with open(clone / "a.py", encoding="utf-8", newline="") as f:
            assert f.read().split("\n")[39] == "    return b == 2\r"


test_census = census_case(TARGET)
