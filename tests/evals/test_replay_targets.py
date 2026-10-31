"""`evals/scripts/replay_targets.py`, one class per function.

The replay generator writes a behaviour case from a review round this
repository already ran: the target the round reviewed, and a `truth-`
grader for each finding the next round confirmed fixed. These cases pin
which findings count as truths, how a labelled record and a record in
`seal` blocks are each read by the check of the commit that wrote it, and
the line window a truth accepts.
`test_a_named_case_is_read_at_every_release_tag` holds the seeded
generator too, because both read the release tags through this module.

#942's phase 6 placed these cases from
`tests/behaviour/test_a_rewritten_definition_proved_non_inferior.py`.
"""

import importlib.util
import os
import re
import subprocess

import pytest
from conftest import ROOT, census_case

TARGET = "evals/scripts/replay_targets.py"


def load_script(name):
    path = os.path.join(ROOT, "evals", "scripts", f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The last release whose check reads a round record in labelled lines. This
# tree's check reads `seal` blocks from #1198 on, so a case that needs a
# commit's check to accept a labelled record takes that release's check.
LABELLED_AT = "v0.26.0"


def labelled_check_files():
    """`{path: text}` for each of `replay_targets.CHECK_FILES` the release
    `LABELLED_AT` holds, read from this repository's history."""
    found = {}
    for rel in load_script("replay_targets").CHECK_FILES:
        shown = subprocess.run(
            ["git", "-C", ROOT, "show", f"{LABELLED_AT}:{rel}"],
            capture_output=True,
            encoding="utf-8",
        )
        if shown.returncode == 0:
            found[rel] = shown.stdout
    assert found, f"this clone holds no `{LABELLED_AT}` tag to take its check from"
    return found


def tree_check_files():
    """`{path: text}` for each of `replay_targets.CHECK_FILES` this tree
    holds: a check that reads a round record's `seal` blocks."""
    found = {}
    for rel in load_script("replay_targets").CHECK_FILES:
        path = os.path.join(ROOT, *rel.split("/"))
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                found[rel] = f.read()
    return found


LABELLED_ROUND_1 = """# i — review round 1

target: 1a2b3c4 against main

## Findings

### 1. a fixed defect

severity: must
location: `src/a.py:12`, `docs/a.md`
evidence: read `src/a.py:12`
verdict: fixed abc1234

why it matters.

answer: fixed

### 2. a finding that does not hold

severity: should
location: `src/b.py:3`
evidence: executed `git grep -n b -- src`
verdict: rejected

answer: it holds

## Confirmations

confirms: none
a claim of the frame that matched.
"""

LABELLED_ROUND_2 = """# i — review round 2

target: 2b3c4d5, fixes 1a2b3c4..2b3c4d5

## Findings

## Confirmations

confirms: round-1#1
holds.

confirms: round-1#2
holds.

confirms: round-3#1
another round's.
"""

# The two records above in `seal` blocks, as `templates/records/sdd-round.md`
# lays a record out since #1198.
BLOCK_ROUND_1 = """# i — review round 1

```seal
target: 1a2b3c4 against main
```

## Findings

### 1. a fixed defect

```seal
severity: must
location: `src/a.py:12`, `docs/a.md`
evidence: read `src/a.py:12`
```

why it matters.

```seal
verdict: fixed abc1234
answer: fixed
```

### 2. a finding that does not hold

```seal
severity: should
location: `src/b.py:3`
evidence: executed `git grep -n b -- src`
```

```seal
verdict: rejected
answer: it holds
```

## Confirmations

```seal
confirms: none
```
a claim of the frame that matched.
"""

BLOCK_ROUND_2 = """# i — review round 2

```seal
target: 2b3c4d5, fixes 1a2b3c4..2b3c4d5
```

## Findings

## Confirmations

```seal
confirms: round-1#1
```
holds.

```seal
confirms: round-1#2
```
holds.

```seal
confirms: round-3#1
```
another round's.
"""

# One work item in each layout a release has kept its round records in, as
# `(item, its directory, the directory of its round records, its branch)`.
SPECS_ITEM = (
    "1791000001-a-specs-item",
    "seal/specs/1791000001-a-specs-item",
    "rounds",
    "feat/1-a-specs-item",
)
THREADS_ITEM = (
    "1792000001-a-threads-item",
    "seal/threads/1792000001-a-threads-item",
    "trail/rounds",
    "feat/2-a-threads-item",
)


def two_layouts(
    tmp_path,
    monkeypatch,
    rt,
    check=labelled_check_files,
    rounds=(LABELLED_ROUND_1, LABELLED_ROUND_2),
):
    """A repository whose tag `v1.0.0` holds `SPECS_ITEM`'s rounds 1 and 2
    and whose tag `v1.1.0` holds `THREADS_ITEM`'s, each pair in its own
    layout, as ROUNDS gives their text, with the check files CHECK gives
    committed before either: labelled lines and the check of `LABELLED_AT`
    by default. Round 1 of each reviewed the commit that added its
    `routing.md`, against the base, and closed finding 1 fixed; round 2
    confirms it. Neither pair stands in the working tree. RT reads the
    repository. `{name: commit}`."""
    repo = tmp_path / "layouts"
    repo.mkdir()
    who = ["-c", "user.name=x", "-c", "user.email=x@example.com"]

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(repo), *who, *args],
            check=True,
            capture_output=True,
            encoding="utf-8",
        ).stdout.strip()

    def put(rel, text):
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    git("init", "-q")
    for rel, said in check().items():
        put(rel, said)
    put("src/a.py", "x = 1\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    commits = {"base": git("rev-parse", "HEAD")}
    first_round, second_round = rounds
    for (item, home, held, branch), tag in (
        (SPECS_ITEM, "v1.0.0"),
        (THREADS_ITEM, "v1.1.0"),
    ):
        put(
            f"{home}/routing.md",
            f"| Axis | Answer |\n|---|---|\n| Branch | {branch} |\n",
        )
        git("add", "-A")
        git("commit", "-qm", f"routing of {item}")
        commits[item] = git("rev-parse", "HEAD")
        first = first_round.replace("# i ", f"# {item} ").replace(
            "1a2b3c4 against main", f"{commits[item]} against {commits['base']}"
        )
        put(f"{home}/{held}/round-1.md", first)
        put(
            f"{home}/{held}/round-2.md",
            second_round.replace("# i ", f"# {item} "),
        )
        git("add", "-A")
        git("commit", "-qm", f"rounds of {item}")
        git("tag", tag)
        git("rm", "-rq", home)
        git("commit", "-qm", f"settled {item}")
    monkeypatch.setattr(rt, "ROOT", str(repo))
    return commits


def tagged_repo(tmp_path, monkeypatch, rt):
    """A repository holding no round record in either layout, its one commit
    tagged `v1.0.0` and `v1.1.0`, with RT reading it."""
    repo = tmp_path / "empty"
    repo.mkdir()
    who = ["-c", "user.name=x", "-c", "user.email=x@example.com"]
    for args in (
        ["init", "-q"],
        ["commit", "-q", "--allow-empty", "-m", "base"],
        ["tag", "v1.0.0"],
        ["tag", "v1.1.0"],
    ):
        subprocess.run(["git", "-C", str(repo), *who, *args], check=True)
    monkeypatch.setattr(rt, "ROOT", str(repo))


class Test_confirmed:
    def test_accepts_a_fixed_finding_the_next_round_confirmed(self):
        """Guards the replay set's ground truth: a finding of the old table
        closed fixed and named closed by the next round's closing row, and no
        other."""
        rt = load_script("replay_targets")
        nxt = (
            "| \U0001f7e2 | round 1's finding 2 is closed — x | `a.md:3` | confirmed | read |\n"
            "| \U0001f7e2 | round 1's \U0001f7e1 4 is closed — y | `a.md:9` | confirmed | read |\n"
            "| \U0001f7e2 | round 2's finding 3 is closed — z | `a.md:9` | confirmed | read |\n"
            "| \U0001f7e1 5 | round 1's finding 5 is closed | `a.md:9` | open | read |\n"
        )
        assert rt.confirmed(nxt, 1) == {2, 4}

    def test_a_truth_of_a_labelled_record_is_a_fixed_finding_the_next_round_confirms(
        self,
    ):
        """Guards the replay set's ground truth on 0.22.0's record: a finding is
        a `### <n>. ` section read through `chain_check.py`'s own reader, with
        its `location:` value whole and whether its `verdict:` is `fixed`, and
        the next round confirms it on a `confirms: round-<N>#<n>` line. The
        table case above reads only the old rows, so without this one a reader
        that found no finding in any labelled record, which is what the
        generator did before #964, left every 0.22.0 round out unnoticed."""
        rt = load_script("replay_targets")
        rel = "seal/specs/i/rounds/round-1.md"
        assert rt.labelled(LABELLED_ROUND_1)
        assert not rt.labelled(
            "| \U0001f7e2 | round 1's finding 2 is closed | `a:1` | confirmed |"
        )
        read, why = rt.labelled_round(LABELLED_ROUND_1, rel, 1, at=LABELLED_AT)
        assert why == ""
        assert read["sha"] == "1a2b3c4"
        assert read["value"] == "1a2b3c4 against main"
        assert read["findings"] == [
            (1, "a fixed defect", "`src/a.py:12`, `docs/a.md`", True),
            (2, "a finding that does not hold", "`src/b.py:3`", False),
        ]
        assert rt.confirmed(LABELLED_ROUND_2, 1, at=LABELLED_AT) == {1, 2}
        assert rt.confirmed(LABELLED_ROUND_2, 2, at=LABELLED_AT) == set()

    def test_refuses_a_labelled_record_the_check_refuses(self):
        """Guards that a replay reads only what a pull request accepted: a
        record `chain_check.py` refuses is left out naming the refusal, and a
        next record it refuses confirms nothing, so a grader is never built on
        a line the check would not read. Nothing else holds the generator to
        the check's refusals, which is the class #923 found leaking three
        times."""
        rt = load_script("replay_targets")
        rel = "seal/specs/i/rounds/round-1.md"
        bad = LABELLED_ROUND_1.replace("fixed abc1234", "fixed abc1234 and more")
        read, why = rt.labelled_round(bad, rel, 1, at=LABELLED_AT)
        assert read is None
        assert why.startswith("the check refuses the record at line 12: ")
        assert "reads `verdict: fixed abc1234 and more`" in why
        worse = LABELLED_ROUND_2.replace("round-1#1\n", "round-1#1 and more\n")
        assert rt.confirmed(worse, 1, at=LABELLED_AT) == set()


class Test_truth_pattern:
    def test_accepts_a_location_inside_its_line_window_and_no_further(self):
        rt = load_script("replay_targets")
        """A truth reads a finding's `location:` line, the line within ±15 of
    the original's, and never a confirmation's or a table's coordinate."""
        pattern = re.compile(rt.truth_pattern("`docs/x.md:100`", "HEAD"), re.M)
        assert pattern.search("location: `docs/x.md:115`")
        assert pattern.search("location: `a.py:1`, `docs/x.md:85-90`")
        assert not pattern.search("location: `docs/x.md:116`")
        assert not pattern.search("location: `docs/x.md:1000`")
        assert not pattern.search("holds, at `docs/x.md:100`. read.")
        assert not pattern.search("| none | f | `docs/x.md:100` | g |")
        assert not pattern.search("Location: `docs/x.md:100`")

    def test_refuses_a_coordinate_the_check_refuses(self, monkeypatch):
        """`chain_check.py` refuses a `path#unit` coordinate, so a truth that
        matched one would pass a proofer for a record the pull request then
        fails. A Python truth reads its unit's lines within ±15 and never the
        unit's name after a `#`, and a truth with no lines reads the bare path
        or `path:<line>`, never `path#<anything>`."""
        rt = load_script("replay_targets")
        source = "x = 0\n\n\ndef f(a):\n    return a\n"
        monkeypatch.setattr(rt, "git", lambda *_a, **_k: source)
        for location in ("`a.py:5`", "`a.py#f`"):
            pattern = re.compile(rt.truth_pattern(location, "HEAD"), re.M)
            assert pattern.search("location: `a.py:5`"), location
            assert pattern.search("location: `b.md:1`, `a.py:4-5`"), location
            assert not pattern.search("location: `a.py:40`"), location
            assert not pattern.search("location: `a.py#f`"), location
            assert not pattern.search("location: `a.py#f:5`"), location
        bare = re.compile(rt.truth_pattern("`docs/x.md#unit`", "HEAD"), re.M)
        assert bare.search("location: `docs/x.md`")
        assert bare.search("location: `docs/x.md:7`")
        assert not bare.search("location: `docs/x.md#unit`")


class Test_module:
    def test_a_labelled_record_is_read_by_the_grammar_of_the_commit_that_wrote_it(
        self, tmp_path, monkeypatch
    ):
        """Guards the owner's decision on #985: a record is judged by the grammar
        in force when it was written. A round written before the table gained
        its `evidence:` row lacks the line, so the tree's check refuses it, and
        the replay set lost 18 of its 31 rounds that way. Read through the check
        of the commit that last wrote it, in the tree or at a release tag, it is
        read as its pull request accepted it. A record no commit wrote is read
        by the tree's check, which reads `seal` blocks since #1198 and refuses
        a record in labelled lines."""
        rt = load_script("replay_targets")
        repo = tmp_path / "repo"
        repo.mkdir()

        who = ["-c", "user.name=x", "-c", "user.email=x@example.com"]

        def git(*args):
            return subprocess.run(
                ["git", "-C", str(repo), *who, *args],
                check=True,
                capture_output=True,
                encoding="utf-8",
            ).stdout.strip()

        def put(rel, text):
            path = repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

        git("init", "-q")
        # The check's files as `replay_targets.py` copies them for a commit, as
        # the last release that read labelled lines holds them, the grammar
        # document apart because the commit below holds an older one.
        held = labelled_check_files()
        for rel, said in held.items():
            if not rel.startswith("docs/"):
                put(rel, said)
        doc = held["docs/the-review-record.md"]
        row = next(
            ln + "\n" for ln in doc.splitlines() if ln.startswith("| `evidence:` |")
        )
        put("docs/the-review-record.md", doc.replace(row, ""))
        rel = "seal/specs/i/rounds/round-1.md"
        text = re.sub(r"^evidence: .*\n", "", LABELLED_ROUND_1, flags=re.M)
        put(rel, text)
        git("add", "-A")
        git("commit", "-qm", "a round written before the evidence row")
        written = git("rev-parse", "HEAD")
        put("docs/the-review-record.md", doc)
        git("commit", "-qam", "the evidence row")
        git("tag", "v1.0.0")
        monkeypatch.setattr(rt, "ROOT", str(repo))

        assert rt.written_at(rel, []) == written
        refused, why = rt.labelled_round(text, rel, 1)
        assert refused is None and "no round block" in why, why
        read, why = rt.labelled_round(text, rel, 1, at=written)
        assert why == ""
        assert read["findings"] == [
            (1, "a fixed defect", "`src/a.py:12`, `docs/a.md`", True),
            (2, "a finding that does not hold", "`src/b.py:3`", False),
        ]
        nxt = LABELLED_ROUND_2.replace(
            "## Findings\n",
            "## Findings\n\n### 1. a deferred defect\n\nseverity: should\n"
            "location: `src/c.py:1`\nverdict: deferred #9\n\nanswer: filed\n",
        )
        assert rt.confirmed(nxt, 1) == set()
        assert rt.confirmed(nxt, 1, at=written) == {1, 2}

        seen = []

        def stub(_text, rel, _n, at=None):
            seen.append((rel, at))
            return None, "stubbed"

        monkeypatch.setattr(rt, "labelled_round", stub)
        assert rt.targets([]) == ([], [("i", 1, "stubbed")])
        assert seen == [(rel, written)]

        git("rm", "-q", rel)
        git("commit", "-qm", "settled")
        assert rt.written_at(rel, ["v1.0.0"]) == written
        assert rt.written_at("seal/specs/i/rounds/round-9.md", ["v1.0.0"]) is None

    def test_a_labelled_record_is_read_by_the_reader_that_judged_it(self, monkeypatch):
        """S10 of #1012: a record at a release tag can carry a template
        comment, and the reader of the commit that wrote it hid the comment
        while this tree's reads it as text. The record's lines are read by
        the reader that judged it, so a `location:` line inside the comment
        is no finding's location. Seen red against the generator that judged
        with the commit's reader and read with this tree's: it took the
        comment's line."""
        rt = load_script("replay_targets")
        check, reader = rt.checks_at(LABELLED_AT)

        class Judged:
            """The reader of `LABELLED_AT` as a reader before #1012 read a
            record: a comment's lines are blank, and none is refused."""

            def __getattr__(self, name):
                return getattr(reader, name)

            def readable(self, text):
                lines, inside = reader.readable(text), False
                for i, line in enumerate(lines):
                    opens = line.lstrip().startswith("<!--")
                    if inside or opens:
                        inside = "-->" not in line
                        lines[i] = ""
                return lines

            def comment_lines(self, lines):
                return []

        monkeypatch.setattr(rt, "checks_at", lambda at: (check, Judged()))
        text = LABELLED_ROUND_1.replace(
            "severity: must\n",
            "<!-- guidance copied from the template\nlocation: `src/z.py:1`\n-->\n"
            "severity: must\n",
        )
        rel = "seal/specs/i/rounds/round-1.md"
        read, why = rt.labelled_round(text, rel, 1, at="abc1234")
        assert why == ""
        assert read["findings"] == [
            (1, "a fixed defect", "`src/a.py:12`, `docs/a.md`", True),
            (2, "a finding that does not hold", "`src/b.py:3`", False),
        ]

    def test_targets_reads_the_next_round_by_the_commit_that_wrote_it(
        self, monkeypatch
    ):
        """Guards the owner's decision on #985 where `targets` reads the round
        after a fixed finding: that round is judged by the check of the commit
        that wrote it, so a round written before the `evidence:` row still
        confirms the fix it names, and the replay keeps the target."""
        rt = load_script("replay_targets")
        two = "seal/threads/i/trail/rounds/round-2.md"
        _specs, threads = rt.LAYOUTS
        monkeypatch.setattr(
            rt,
            "records",
            lambda _tags, _items=None: {
                ("i", 1): (threads, LABELLED_ROUND_1),
                ("i", 2): (threads, LABELLED_ROUND_2),
            },
        )
        monkeypatch.setattr(rt, "written_at", lambda rel, _tags: f"at {rel}")
        monkeypatch.setattr(
            rt,
            "labelled_round",
            lambda _text, _rel, _n, at=None: (
                {
                    "sha": "abc1234",
                    "value": "abc1234 against main",
                    "findings": [(1, "x", "`src/a.py:12`", True)],
                    "confirms": set(),
                },
                "",
            ),
        )
        monkeypatch.setattr(rt, "resolve", lambda _rev: True)
        monkeypatch.setattr(
            rt, "target_base", lambda _value, _target, _landed=None: ("abc1234", "main")
        )
        # The one git call left before `confirmed`: routing.md at the target.
        monkeypatch.setattr(rt, "git", lambda *_args, check=True: "| Branch | b |\n")
        asked = []

        def spy(_text, n, rel, at=None):
            asked.append((n, rel, at))
            return set()

        monkeypatch.setattr(rt, "confirmed", spy)
        rt.targets([])
        assert asked == [(1, two, f"at {two}")], asked

    def test_a_labelled_target_names_its_base(self, monkeypatch):
        """Guards where a labelled replay's clone starts: a fix range's first
        commit, an `against <sha>` commit, or the merge-base with
        `origin/<base>` for `against <base>`, and no base where none resolves,
        which leaves the round out rather than cloning the wrong range. The old
        reader found a base only in an asked paragraph, which 0.22.0's record
        does not carry."""
        rt = load_script("replay_targets")
        known = {"1a2b3c4": "1" * 40, "ce448bbe": "c" * 40, "origin/main": "d" * 40}
        monkeypatch.setattr(rt, "resolve", lambda rev: known.get(rev, ""))
        monkeypatch.setattr(
            rt,
            "git",
            lambda *a, **_k: "m" * 40 + "\n" if a[:2] == ("merge-base", "T") else "",
        )
        fixes = rt.target_base("2b3c4d5, fixes 1a2b3c4..2b3c4d5", "T")
        assert fixes == ("1" * 40, None)
        assert rt.target_base("2b3c4d5 against ce448bbe", "T") == ("c" * 40, None)
        assert rt.target_base("2b3c4d5 against main", "T") == ("m" * 40, "origin/main")
        assert rt.target_base("2b3c4d5 against gone", "T") == ("", None)
        # A release branch deleted after its release: the commit the work landed
        # on stands for it where the caller knows that commit (#986).
        landed = ("m" * 40, "origin/gone")
        assert rt.target_base("2b3c4d5 against gone", "T", landed="L") == landed
        assert rt.base_of("Round 1, against origin/gone.", "T") == ("", None)
        assert rt.base_of("Round 1, against origin/gone.", "T", landed="L") == landed

    def test_records_read_only_the_named_items(self, monkeypatch, tmp_path):
        """Guards `--case`'s reach over every release tag: only the named work
        items' records are read, so reading all tags costs one listing a tag and
        a `git show` per named record, never one per record in the history.
        Each record comes with the layout it was read in, from the working
        tree and from a tag, in both layouts a release has kept its records
        in."""
        rt = load_script("replay_targets")
        listed, shown = [], []
        for item in ("1793-c", "1794-d"):
            rounds = tmp_path / "seal" / "threads" / item / "trail" / "rounds"
            rounds.mkdir(parents=True)
            (rounds / "round-1.md").write_text(f"the tree's {item}", encoding="utf-8")

        def git(*args, check=True):
            if args[0] == "ls-tree":
                listed.append(args)
                return (
                    "seal/specs/1791-a/rounds/round-1.md\n"
                    "seal/specs/1792-b/rounds/round-1.md\n"
                    "seal/threads/1793-c/trail/rounds/round-1.md\n"
                    "seal/threads/1795-e/trail/rounds/round-2.md\n"
                )
            shown.append(args[1])
            return f"text of {args[1]}"

        monkeypatch.setattr(rt, "ROOT", str(tmp_path))
        monkeypatch.setattr(rt, "git", git)
        found = rt.records(["v1.0.0"], {"1791", "1793", "1795"})
        specs, threads = rt.LAYOUTS
        assert found == {
            ("1791-a", 1): (
                specs,
                "text of v1.0.0:seal/specs/1791-a/rounds/round-1.md",
            ),
            ("1793-c", 1): (threads, "the tree's 1793-c"),
            ("1795-e", 2): (
                threads,
                "text of v1.0.0:seal/threads/1795-e/trail/rounds/round-2.md",
            ),
        }
        assert listed == [
            ("ls-tree", "-r", "--name-only", "v1.0.0", "seal/specs", "seal/threads")
        ]
        assert shown == [
            "v1.0.0:seal/specs/1791-a/rounds/round-1.md",
            "v1.0.0:seal/threads/1795-e/trail/rounds/round-2.md",
        ]

    def test_reads_a_round_record_in_either_layout_a_release_kept_it_in(
        self, tmp_path, monkeypatch
    ):
        """Guards #1150: every release from 0.23.0 on keeps its round records
        at `seal/threads/<id>/trail/rounds/`, and the generator read only the
        layout before it, so `--list` over the last two tags printed nothing.
        A record in either layout gives a target, the next round, `routing.md`
        at the target and the report path each in the layout of the record
        they derive from. Seen red against the reader of one layout, which
        kept the `seal/specs/` item alone."""
        rt = load_script("replay_targets")
        commits = two_layouts(tmp_path, monkeypatch, rt)
        kept, left = rt.targets(["v1.1.0", "v1.0.0"])
        assert [
            (
                t["item"],
                t["target"],
                t["base"],
                t["branch"],
                [x["k"] for x in t["truths"]],
            )
            for t in kept
        ] == [
            (item, commits[item], commits["base"], branch, [1])
            for item, _home, _rounds, branch in (SPECS_ITEM, THREADS_ITEM)
        ]
        assert left == [
            (SPECS_ITEM[0], 2, "target 2b3c4d5 does not resolve"),
            (THREADS_ITEM[0], 2, "target 2b3c4d5 does not resolve"),
        ]
        for t, (_item, home, rounds, _branch) in zip(
            kept, (SPECS_ITEM, THREADS_ITEM), strict=True
        ):
            report = f"{home}/{rounds}/round-1.md"
            assert f"Write the report to `{report}`" in rt.prompt(t)
            assert f"run `cat {report}` once" in rt.prompt(t)

    def test_reads_a_round_record_in_seal_blocks_by_the_check_that_wrote_it(
        self, tmp_path, monkeypatch
    ):
        """Guards #1150's second half: from #1198 on a round record holds its
        fields in `seal` blocks, and the generator read such a record as a
        table, leaving each out as `Target SHA (none) does not resolve`. A
        record whose blocks hold a round block is read through the check of
        the commit that wrote it: its base is the round block's `target:`
        value, a truth is a finding block's `location:` value whose close
        block reads `fixed`, and the next round confirms it in a
        confirmation block. Seen red against phase 1's reader, which left
        both round 1 records out with that reason."""
        rt = load_script("replay_targets")
        commits = two_layouts(
            tmp_path,
            monkeypatch,
            rt,
            check=tree_check_files,
            rounds=(BLOCK_ROUND_1, BLOCK_ROUND_2),
        )
        kept, left = rt.targets(["v1.1.0", "v1.0.0"])
        assert [
            (
                t["item"],
                t["target"],
                t["base"],
                t["base_ref"],
                t["asked"],
                [(x["k"], x["finding"], x["location"]) for x in t["truths"]],
            )
            for t in kept
        ] == [
            (
                item,
                commits[item],
                commits["base"],
                None,
                "",
                [(1, "a fixed defect", "`src/a.py:12`, `docs/a.md`")],
            )
            for item, _home, _rounds, _branch in (SPECS_ITEM, THREADS_ITEM)
        ]
        assert left == [
            (SPECS_ITEM[0], 2, "target 2b3c4d5 does not resolve"),
            (THREADS_ITEM[0], 2, "target 2b3c4d5 does not resolve"),
        ]

    def test_refuses_a_record_in_seal_blocks_the_check_refuses(self):
        """Guards that a replay reads only what a pull request accepted, for
        a record in `seal` blocks as for a labelled one: a record the check
        refuses is left out naming the refusal, and a next record it refuses
        confirms nothing. A record that holds a `seal` opener is judged as a
        record in blocks and never read as a table, whether the parser reads
        any of its blocks or refuses every one: its round block beside
        finding blocks it reads, its round block alone, a fence that never
        closes, or a fence the walk cannot place. A refusal that names no
        opener leaves the record to the labelled and table readers. Seen red
        against phase 1's reader for the first, and against phase 2's for
        the other three, each of which gave `Target SHA (none) does not
        resolve`; the last three are seen red against a reader that counts
        every refusal, or a comment line, an unclosed fence or an unplaced
        one of any info string."""
        rt = load_script("replay_targets")
        _specs, threads = rt.LAYOUTS
        fence = "`" * 3
        bad = BLOCK_ROUND_1.replace("against main", "against main and more")
        head = "# i — review round 1\n\n"
        tail = "\n## Findings\n\n## Confirmations\n"
        refused = {
            bad: (4, "`target: 1a2b3c4 against main and more` does not read"),
            f"{head}{fence}seal\ntarget: 1a2b3c4 against main and more\n"
            f"{fence}\n{tail}": (
                4,
                "`target: 1a2b3c4 against main and more` does not read",
            ),
            f"{head}{fence}seal\ntarget: 1a2b3c4 against main\n{tail}": (
                0,
                "no `## Findings` section",
            ),
            f"{head}<div>\n{fence}seal\ntarget: 1a2b3c4 against main\n"
            f"{fence}\n{tail}": (4, "the walk cannot place this fence line"),
        }
        for text, (line, said) in refused.items():
            t, why = rt.round_target(
                "i", 1, text, BLOCK_ROUND_2, lambda _rel: None, layout=threads
            )
            assert t is None
            assert why.startswith(
                f"the check refuses the record at line {line}: {said}"
            ), why
        # A refusal that names no `seal` opener leaves the record to the
        # other readers: a comment line, and a fence of another info string
        # that never closes or that the walk cannot place.
        commented = LABELLED_ROUND_1.replace(
            "## Findings\n", "## Findings\n\n<!-- a template comment -->\n"
        )
        table = "| Target SHA | 1a2b3c4 |\n"
        assert rt.judged_by(commented) is rt.labelled_round
        assert rt.judged_by(f"{table}\n{fence}python\nx = 1\n") is None
        assert rt.judged_by(f"{table}\n<div>\n{fence}text\nx\n{fence}\n") is None
        worse = BLOCK_ROUND_2.replace("round-1#1\n", "round-1#1 and more\n")
        assert rt.confirmed(BLOCK_ROUND_2, 1) == {1, 2}
        assert rt.confirmed(worse, 1) == set()

    def test_says_so_and_exits_1_where_it_reads_no_round_record(
        self, tmp_path, monkeypatch, capsys
    ):
        """Guards #1150's silent read: a run that found no round record in
        either layout printed nothing and exited 0, which reads as "nothing
        to do". It names both layouts and the tags it read on stderr, and
        exits 1. Seen red against that exit 0."""
        rt = load_script("replay_targets")
        tagged_repo(tmp_path, monkeypatch, rt)
        assert rt.main(["--list"]) == 1
        said = capsys.readouterr()
        assert said.out == ""
        assert said.err == (
            "replay_targets: no round record in `seal/specs/<item>/rounds/` or "
            "`seal/threads/<item>/trail/rounds/`, in the working tree or at "
            "v1.1.0, v1.0.0\n"
        )

    def test_names_each_named_case_it_did_not_write_with_its_reason(
        self, tmp_path, monkeypatch, capsys
    ):
        """Guards `--case` on a name no written case answers: the run named
        nothing and exited 1, so a reader could not tell a record left out
        from a record never read. Each such name is said on stderr with the
        reason `round_target` gave, or that no record of its work item, or
        of that round, was read. Seen red against the silent exit 1. A name
        given twice is one name, where the run that wrote its case exited 1
        saying nothing; seen red against that exit 1."""
        rt = load_script("replay_targets")
        tagged_repo(tmp_path, monkeypatch, rt)
        monkeypatch.setattr(rt, "origin_url", lambda: "https://example.com/x/y.git")
        assert rt.main(["--case", "replay-1-r1"]) == 1
        assert capsys.readouterr().err == (
            "replay_targets: replay-1-r1 not written: no record of its work item "
            "was read\n"
        )
        two_layouts(tmp_path, monkeypatch, rt)
        names = ["replay-1792000001-r2", "replay-1792000001-r5"]
        assert rt.main([x for name in names for x in ("--case", name)]) == 1
        assert capsys.readouterr().err == (
            "replay_targets: replay-1792000001-r2 not written: target 2b3c4d5 "
            "does not resolve\n"
            "replay_targets: replay-1792000001-r5 not written: no round 5 record "
            "of its work item was read\n"
        )
        kept = ["--case", "replay-1792000001-r1"]
        assert rt.main(["--out", str(tmp_path / "out"), *kept, *kept]) == 0
        assert capsys.readouterr().err == ""

    def test_names_each_named_case_no_listed_line_answers_with_its_reason(
        self, tmp_path, monkeypatch, capsys
    ):
        """Guards `--list` with `--case`: the list returned before the names
        no written case answers were said, so a name no record answered
        printed nothing and exited 0, where `seed_defects.py` says on the
        same input that it read nothing and exits 1. A name no listed line
        answers is said on stderr as `--case` says it, and the run exits 1;
        a name a kept or a `left out:` line answers is said there alone.
        Seen red against that exit 0. A name is read only in a case's form,
        and any other name is answered with that form: a listed round named
        without `replay-` was told no record of that round was read (round
        3 of #1150); seen red against that reason."""
        rt = load_script("replay_targets")
        tagged_repo(tmp_path, monkeypatch, rt)
        assert rt.main(["--list", "--case", "replay-1-r1"]) == 1
        said = capsys.readouterr()
        assert said.out == ""
        assert said.err == (
            "replay_targets: replay-1-r1 not written: no record of its work item "
            "was read\n"
        )
        two_layouts(tmp_path, monkeypatch, rt)
        names = ["replay-1792000001-r2", "replay-1792000001-r5"]
        assert rt.main(["--list", *[x for n in names for x in ("--case", n)]]) == 1
        said = capsys.readouterr()
        assert said.out.splitlines()[1:] == [
            "1792000001-a-threads-item r2  left out: target 2b3c4d5 does not resolve"
        ]
        assert said.err == (
            "replay_targets: replay-1792000001-r5 not written: no round 5 record "
            "of its work item was read\n"
        )
        listed = ["replay-1792000001-r1", names[0]]
        assert rt.main(["--list", *[x for n in listed for x in ("--case", n)]]) == 0
        assert capsys.readouterr().err == ""
        # A name out of a case's form is read as none, here the round listed
        # above without `replay-` and its work item without a round.
        other = ["1792000001-r1", "replay-1792000001"]
        assert rt.main(["--list", *[x for n in other for x in ("--case", n)]]) == 1
        said = capsys.readouterr()
        assert said.out == ""
        assert said.err == "".join(
            f"replay_targets: {n} not written: a case is named "
            "replay-<the work item's epoch>-r<the round>\n"
            for n in other
        )

    @pytest.mark.parametrize(
        "blocks",
        [
            # exempt from vacated_paths: the path a commit before #1060 holds it at
            "hooks/blocks.py",
            "hooks/lib/blocks.py",
        ],
        ids=["before", "lib"],
    )
    def test_a_commit_has_its_hook_module_copied_where_it_holds_it(
        self, tmp_path, monkeypatch, blocks
    ):
        """#1060 moved the hook module `blocks.py` into `hooks/lib/`. A commit's
        check loads the module from where that commit holds it, so the copy
        `checks_at` makes takes it from either path and puts it at the same
        path. A copy that read only the old path would give a commit after the
        move no module, and its check would fail to load its reader."""
        rt = load_script("replay_targets")
        repo = tmp_path / "repo"
        held = tmp_path / "held"
        who = ["-c", "user.name=x", "-c", "user.email=x@example.com"]

        def git(*args):
            return subprocess.run(
                ["git", "-C", str(repo), *who, *args],
                check=True,
                capture_output=True,
                encoding="utf-8",
            ).stdout.strip()

        for rel in (rt.CHECK_FILES[0], blocks):
            path = repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {rel}\n", encoding="utf-8")
        git("init", "-q")
        git("add", "-A")
        git("commit", "-qm", "a commit holding the hook module")
        monkeypatch.setattr(rt, "ROOT", str(repo))
        monkeypatch.setattr(rt.tempfile, "mkdtemp", lambda prefix: str(held))
        check = type("Check", (), {"READER": "", "load": lambda *_a: None})
        monkeypatch.setattr(rt, "load_check", lambda _path, _name: check)
        rt.checks_at(git("rev-parse", "HEAD"))
        copied = held.joinpath(*blocks.split("/"))
        assert copied.read_text(encoding="utf-8") == f"# {blocks}\n"

    @pytest.mark.parametrize(
        ("script", "name", "items"),
        [
            ("replay_targets", "replay-1791382684-r2", {"1791382684"}),
            ("seed_defects", "seeded-279a580b", {"279a580b"}),
        ],
    )
    def test_a_named_case_is_read_at_every_release_tag(
        self, monkeypatch, script, name, items
    ):
        """Guards that a committed case regenerates after the release that moved
        its records or commits out of the window `--list` reads: `--case` reads
        every release tag, for the named items alone. Before #964 both
        generators read the last two or three tags, and none of the eight
        committed replay and seeded cases was still on either list once 0.22.0
        was tagged, so `--case` exited 1 for each."""
        module = load_script(script)
        rt = module if script == "replay_targets" else module.rt
        calls = []
        # One round read and left out, so `--list` has a read to list.
        if script == "replay_targets":
            read = ([], [("1-i", 1, "left out")])
        else:
            read = ([], [("c" * 40, "left out")], 1)
        monkeypatch.setattr(rt, "last_tags", lambda count=2: calls.append(count) or [])
        monkeypatch.setattr(
            module, "targets", lambda tags, only=None: calls.append(only) or read
        )
        monkeypatch.setattr(rt, "origin_url", lambda: "https://example.com/x/y.git")
        assert module.main(["--case", name]) == 1
        assert calls == [None, items]
        calls.clear()
        assert module.main(["--list"]) == 0
        assert calls[1] is None and calls[0] in (2, 3)

    def test_a_record_with_no_asked_paragraph_ends_the_spawn_at_the_report(self):
        """Guards the replay prompt of a labelled record, which carries no asked
        paragraph: the spawn ends at the report's path with nothing after it,
        and a table record's paragraph still follows that sentence after one
        space, as the four committed cases were written."""
        rt = load_script("replay_targets")
        t = {
            "item": "1-i",
            "n": 2,
            "report": "seal/threads/1-i/trail/rounds/round-2.md",
            "branch": "b",
            "target": "t" * 40,
            "base": "a" * 40,
            "base_ref": None,
            "asked": "",
        }
        assert "and return its path.\n\nEND PROMPT" in rt.prompt(t)
        t["asked"] = "Round 2,\n  the verifying round."
        assert "and return its path. Round 2, the verifying round.\n\nEND" in rt.prompt(
            t
        )


test_census = census_case(TARGET)
