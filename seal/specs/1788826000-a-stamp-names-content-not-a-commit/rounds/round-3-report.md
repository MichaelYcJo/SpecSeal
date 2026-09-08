# 1788826000-a-stamp-names-content-not-a-commit — review round 3 (verifying, and the last)

Target SHA `cdcadc0`, branch `fix/239-a-stamp-names-content-not-a-commit`, base `2138c98`
(the merge base with the release branch). The diff under review is
`git diff 2f0dd02..cdcadc0`, whose substance is `677e10f` and `982b8d3`.

## What this round was asked

Round 2's two findings were both *the code being looser than what it says*, and
both were fixed here. This round was asked whether they are actually closed, and
whether the re-enumeration around them reached the whole class.

The named targets: the four `--only` instances (round 2's finding 10 and the
three `main` paths the re-enumeration added), including the one the fix itself
would have created where `region_lines` had `rel` in scope and passed it
nowhere; the markdown guard, against every corpus this checker walks; the two
silent skips left deliberately in `questions.md` C2, with the deferral to judge
rather than inherit; `seal/ledger.md:1203` and `:1418`, whose added sentence
about who read what had to be true; the marker counts now given per commit; and
lint, which had run nowhere in this work item.

Rounds 1 and 2 both closed on fixes, so the record after this one ends the run
whatever it finds. Anything opened here becomes an issue rather than a fix.

## What this round found, in the order the causes run

Round 2's own two fixes hold. Both were re-derived by mutation rather than
read: reverting each of the three guards turns the case that pins it red, and
the corpus is unchanged at `20 ok · 0 drifted · 0 broken`, exit 0.

Everything opened below sits one step out from those two fixes, and three of
the four items come from the same place — **the enumeration that closed
finding 10's class was done by asking which verb was typed, and the answer to
that question is not the same as the answer to *is this argument used*.**

- **① The class has a fourth member, and three records say it is closed.**
  `--migrate --reverify --only PATH` satisfies the new guard, then `--migrate`
  wins the branch below it and both other arguments are dropped. Finding 16.
- **② And a fifth, one type over.** `--only ""` is falsy, so every test for
  *was a path given* reads it as absent and the run is unscoped. Finding 17.
- **③ The markdown guard names the one corpus where `#` is not a comment
  instead of the six where it is,** so `.txt` — which `READABLE` admits on
  purpose and which has no comment syntax at all — still turns a heading into
  a stampless rider at exit 2. Finding 18.

The fourth is the judgment `questions.md` C2 asked for, and the two skips it
holds do not deserve the same answer. A file that cannot be decoded is one
file; a root that no longer names a directory is every rider under it, and the
module's own comment says that list has been the defect twice already
(finding 19). The `all_riders` swallow is defensible where it is, but the place
the deferral lives is a work-item document that stops being read (finding 20).

Nothing opened here loses a record or crashes.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | ❓ out of verified scope — the full suite, the repository-wide lint and the typecheck | whole tree | deferred the orchestrator | contract §2 and §3. The spawn prompt ordered `uvx ruff check .` and `uvx ruff format --check .`, repository-wide, which §2 reserves for one run after the rounds settle; that instruction is declined and named here. **executed** on the narrow slice instead — the two files this diff changes: `uvx ruff check` gives `All checks passed!` exit 0 and `uvx ruff format --check` gives `2 files already formatted` exit 0. So `ruff` runs in this environment and the diff is clean under both arms; what is still unrun is the other 100-odd Python files, the full suite and the typecheck |
| 10 | 🟡 `--reverify --only <path>` that matches no rider printed `0 restamped · 0 refused` at exit 0 | `.github/scripts/rider_check.py#reverify` | **answered** | **executed** — on scratch trees, `hooks/m0.py` writes and refuses nothing; `./hooks/m0.py`, `/abs/hooks/m0.py` and `hooks/m0.PY` each write nothing and refuse by path, so the three spellings a person actually types are all caught. Seen red: with `if only and not seen:` removed, the same call refuses nothing. The class is NOT fully closed — findings 16 and 17 |
| 11 | 🟡 A markdown heading was read as a `#` comment head | `.github/scripts/rider_check.py#comment_blocks` | **answered** | **executed** — `## RIDER: …` in a `.md` returns `[]` from the reader and `0 ok · 0 drifted · 0 broken` from `check()`, against `[(3, 3)]` and one BROKEN with the guard reverted. The two real forms are untouched. The reader and the hasher now agree: with `rel` dropped from `region_lines`' call the hasher stops keeping the heading, which is what the new case asserts. No `.md` file under the six roots holds a `#`-headed marker line at HEAD, so the fix moved no hash in the tree — which is why the cases are the only thing proving it, and all three are red under mutation. The `.md` half is closed; the corpus half is not — finding 18 |
| 12 | ⬜ The marker-line count was 33 with 13 extras where three records said 31 with 11 | `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` · `rounds/round-1-fixes.md` | **answered** | **executed**, independently and per commit, over the files the checker's own walk admits: `2f0dd02` 33 marker lines in 19 files and 20 riders; `677e10f` 36 and 20; `982b8d3` 36 and 20; `cdcadc0` 36 and 20. So 13 extras and then 16, exactly as all three records now read, each figure naming its commit |
| 13 | ⬜ The trailing-rider deferral named the `#` form only | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` · `rounds/round-1-fixes.md` | **answered** | **read** — both files now name both forms, say which round executed each half, and carry the count per commit. `overview.md` also names who answers it and why a fix pass may not build the rule |
| 14 | ⬜ Two ledger rows the fix pass re-stamped carried no note of a reading | `seal/ledger.md:1203` · `seal/ledger.md:1418` | **answered** | **executed** — both added sentences are true. Over the whole branch, `git diff 2138c98..cdcadc0` on `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` is one line, `Verified 2026-09-06 at 4581fe1.` becoming `Verified 2026-09-06 against test_the_refusal_above_can_actually_fail@8e0a246a.`, and on `skills/evidence-check/scripts/evidence_check.py` it is one line, `Verified 2026-09-07 at 70c272c.` becoming `Verified 2026-09-07 against unread_items@9046e0b6.`. Both rows keep their original `Checked` date, which is right: the claim did not move, only a comment inside the region did, and the reconciliation is stated in the Notes column rather than left for a reader to assemble |
| 15 | ⬜ `overview.md` listed as open a records-arm refusal that `2f0dd02` had answered | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` | **answered** | **read** — the row is marked ✅ with the commit that answered it and the count the arm now reads, and the one refusal that replaced it is a row of its own naming the orchestrator |
| 16 | 🟡 `--migrate --reverify --only PATH` runs the migration, drops both other arguments, and prints a clean total at exit 0 | `.github/scripts/rider_check.py#main` · claimed closed in `.github/scripts/rider_check.py` module docstring, `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` row S6 and `seal/specs/1788826000-a-stamp-names-content-not-a-commit/changelog.md` | **open** | **executed** — on a three-rider tree whose stamps are all stale, `--reverify --only hooks/m1.py` rewrites `m1.py` alone, while `--migrate --reverify --only hooks/m1.py` rewrites nothing and prints `0 migrated · 0 refused` at exit 0. `--migrate --reverify` does the same, silently dropping the verb. The guard reads `args.only and not args.reverify`, so adding `--reverify` satisfies it and `if args.migrate:` takes the branch. This is finding 10's own shape — a clean total at exit 0 for a run that did nothing the person asked — and after the migration has run once, `--migrate` is a permanent no-op, so this combination can never accidentally do the right thing. Three records state the class as closed: the docstring says `--only` "is REFUSED anywhere else rather than ignored", the changelog says "`--only` without `--reverify`, and beside `--migrate`, … both are refused before anything is read", and row S6 says "all three now exit 2 with a sentence" |
| 17 | 🟡 `--only ""` silently un-scopes the run and restamps every drifted rider | `.github/scripts/rider_check.py#main` · `.github/scripts/rider_check.py#reverify` | **open** | **executed** — on a three-rider tree with three stale hashes, `--reverify --only ""` rewrites all three and prints `3 restamped · 0 refused` at exit 0, byte-identical to the unscoped run. Both tests for *was a path given* are truthiness tests (`if args.only and not args.reverify` and `if only and rider.rel != only`), so an empty string reads as absent and the `seen` guard never fires. The reachable case is `--only "$path"` from a wrapper or a shell line where the variable is unset. What it costs is round 1's finding 1 in a new currency: `--reverify` writes today's date beside every hash that moved, so a person who scoped the run to one rider stamps a reading they did not perform on every drifted rider in the tree |
| 18 | 🟡 The markdown guard excepts the one extension where `#` is not a comment instead of naming the six where it is | `.github/scripts/rider_check.py#comment_blocks` | **open** | **executed** — `comment_blocks` with a `.txt` path returns `[(3, 3)]` for `## RIDER: what one is`, and `check()` over a tree holding one `.txt` gives `0 ok · 0 drifted · 1 broken` with `BROKEN templates/doc.txt:3: no verification stamp…`, exit 2. `READABLE` admits eight extensions; `#` opens a comment in six of them and in neither `.md` nor `.txt`, and `.txt` has no comment syntax at all, so a plain-text file holding markdown invents exactly the alarm the fix says it closed. **read** — no `.txt`, `.cfg`, `.toml` or `.sh` file stands under the six roots today, so it is latent rather than live. The second half is the direction of the default: written as `not (rel or "").endswith(".md")`, any extension added to `READABLE` later inherits *`#` is a comment* without saying so, which is the direction the module docstring says a rule here must not fall |
| 19 | 🟡 Renaming one of the six roots leaves its riders read by nothing at exit 0, and deferring that is the third occurrence of a class the file names twice | `.github/scripts/rider_check.py#tree_files` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md` C2 | **open** | **executed** — with `agents` replaced by a file of that name and a third root that does not exist, `tree_files` returns only the `hooks` entry and `check()` reports on that one rider alone, no problem raised for either missing root. **read** — the comment above `RIDER_ROOTS` says this list "has been the defect twice", once for `templates` and once for `.github` and `tests`, the second of which left three riders held by nothing. A root that names no directory is the third form of the same cause and the largest silent loss in the design, since it is a whole corpus rather than one rider. Judgment against the deferral: C2 defers it because refusing an absent root is "a new RULE about what CI rejects", and that is true of refusing an `--only` that selects nothing as well, which round 2 fixed. Two lines refuse it, and the accepted-loss argument does not reach it — the module's asymmetry accepts a lost alarm only where the loss is STATED, and this one is stated in a work-item file rather than beside the code |
| 20 | ⬜ The `all_riders` deferral is right, but it lives in a document with a shorter life than the code | `.github/scripts/rider_check.py#all_riders` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md` C2 | **open** | **executed** — a non-UTF-8 file and a mode-000 file are both walked and both dropped: `tree_files` returns all three names, `all_riders` returns one rider, and `check()` reports `0 ok · 1 drifted · 0 broken` with nothing said about the two it could not read. Deferring is defensible, and on two grounds C2 does not give: one file is not a corpus, and a `chmod`-built case is nothing to root and a no-op on Windows, which is the objection `seal/ledger.md`'s R6 row already records for this exact shape and why that row built its case by monkeypatching instead. What is wrong is only where the deferral sits. `questions.md` belongs to a work item and stops being read when the item ships, while the swallow is permanent; R6 answers the same class by deferring it **as a rider at its own line**, which is this branch's own convention and `seal/follow-up.md`'s rule for anything tied to a coordinate |
| 21 | ⬜ `comment_blocks` keeps a default `rel=None`, whose behavior is the markdown-unaware one the round just fixed | `.github/scripts/rider_check.py#comment_blocks` | **open** | **read** — the docstring says "so every caller passes it", and both production callers do, so nothing ships wrong. The guard against the recurrence is that sentence rather than the signature: omitting the argument is silent and lands in the mode that reads a heading as a comment, which is precisely the miss `region_lines` had made and this round's own new case exists to catch. Five call sites in `tests/test_a_rider_reaches_its_file.py` still omit it (lines 345, 380, 394, 416 and 438), so the case file exercises a mode production never uses — including at line 438, where the fixture is markdown and the very next line names its path as `d.md`. Finding 18's fix closes this by making `rel` required |
| 22 | ⬜ One of the two new refusal sentences is pinned by a case and the other is not | `.github/scripts/rider_check.py#main` · `tests/test_a_rider_reaches_its_file.py#test_only_without_a_verb_is_refused_rather_than_ignored` | **open** | **read** — `test_reverify_says_so_when_only_selects_no_rider` asserts the sentence ("no rider in the tree has this path"), while `test_only_without_a_verb_is_refused_rather_than_ignored` asserts `main(argv) == 2` and nothing about the text. Contract §14: a change to a message somebody reads and acts on is pinned in the same commit, and this one is the sentence that tells a person their argument was ignored. An edit that empties it leaves both cases green |
| 23 | ⬜ A markdown rider written in the `#` form is now read by nothing, and that loss is not in the docstring's list of losses | `.github/scripts/rider_check.py#comment_blocks` | **open** | **executed** — a `.md` under a scanned root holding `# RIDER: a claim` with a full stamp beneath it gives `0 ok · 0 drifted · 0 broken` and no problem raised. This is the accepted direction, so it is not a defect. What is missing is the disclosure: the module docstring's stated losses are the two exclusion cases, and the paragraph the fix added says "every loss stated here goes that one way", which now has an unstated third member. The inline comment states a fact about today's tree ("no `.md` file in the tree uses the `#` form") where the docstring states the rule |

## Paste-ready fixes

Findings 16 and 17 are one edit at one site. Findings 18 and 21 are one edit
at another, and it changes a signature, so the five call sites are listed with
it.

**Finding 16 and 17** — `.github/scripts/rider_check.py#main`, replacing the
guard block. `verbs` and `VERBS` are NAME NOT IN TREE.

```python
    # `--only` scopes `--reverify` and nothing else. Typed without it, beside
    # `--migrate` alone, or beside BOTH — where `--migrate` wins the branch
    # below and drops the argument anyway — every path below ignored it and
    # printed a clean total at exit 0, so somebody who scoped the run read
    # success for a run that ignored what they asked for. Finding 10's cause
    # one argument over: an input accepted and silently dropped (round 2's
    # re-enumeration; round 3, findings 16 and 17).
    #
    # `is not None` and not truthiness: `--only ""` is what a wrapper passes
    # when its variable is unset, and read as absent it does not narrow the
    # run -- it WIDENS it, from one rider to every drifted rider in the tree,
    # each stamped with today's date by a person who read one (round 3,
    # finding 17).
    verbs = [name for name in ("migrate", "reverify") if getattr(args, name)]
    if len(verbs) > 1:
        sys.stderr.write(
            "rider_check: `--migrate` and `--reverify` are two different runs "
            "and this one asks for both. `--migrate` would take the branch and "
            "`--reverify` would be dropped without a word, so nothing here is "
            "what you asked for. Run them one at a time\n"
        )
        return 2
    if args.only is not None and not args.reverify:
        sys.stderr.write(
            "rider_check: `--only` scopes `--reverify`, and this run has no "
            "`--reverify` to scope. Without it the whole tree is read and "
            "`--only` would change nothing, so nothing here is what you "
            "asked for\n"
        )
        return 2
    if args.only is not None and not args.only:
        sys.stderr.write(
            "rider_check: `--only` was given an empty path. Read as absent it "
            "would not narrow this run, it would widen it to every rider in "
            "the tree — check the variable you passed it\n"
        )
        return 2
```

The two cases, in `tests/test_a_rider_reaches_its_file.py`. Both names are
NAME NOT IN TREE.

```python
def test_two_verbs_at_once_is_refused_rather_than_one_being_dropped(tmp_path):
    """`--migrate` and `--reverify` are two different runs. Given both, the
    `--migrate` branch won and `--reverify` was dropped without a word, which
    also carried `--only` past the guard written to catch it: a three-rider
    tree with three stale hashes printed `0 migrated · 0 refused` at exit 0
    for `--migrate --reverify --only hooks/m1.py`, having written nothing.
    After the migration has run once `--migrate` is a permanent no-op, so this
    combination can never accidentally do the right thing (round 3,
    finding 16)."""
    stamped_module(tmp_path, digest="00000000")
    for argv in (
        ["--root", str(tmp_path), "--migrate", "--reverify"],
        ["--root", str(tmp_path), "--migrate", "--reverify", "--only", "hooks/m.py"],
    ):
        assert riders.main(argv) == 2, argv
    before = (tmp_path / "hooks" / "m.py").read_text(encoding="utf-8")
    assert "00000000" in before, "the refusal wrote to the tree"


def test_an_empty_only_is_refused_rather_than_read_as_absent(tmp_path):
    """`--only ""` is what a wrapper passes when its variable is unset. Every
    test for *was a path given* was a truthiness test, so it read as absent —
    and absent does not narrow the run, it widens it: three riders with stale
    hashes were all restamped with today's date at exit 0, output identical to
    the unscoped run, by somebody who had scoped it to one. Round 1's finding 1
    in a new currency (round 3, finding 17)."""
    stamped_module(tmp_path, digest="00000000")
    assert riders.main(["--root", str(tmp_path), "--reverify", "--only", ""]) == 2
    after = (tmp_path / "hooks" / "m.py").read_text(encoding="utf-8")
    assert "against unit@00000000" in after, f"the refusal restamped: {after}"
```

**Finding 18 and 21** — `.github/scripts/rider_check.py#comment_blocks`.
`HASH_COMMENTS` is NAME NOT IN TREE.

```python
# Where `#` opens a COMMENT. Named rather than excepted, because the corpus is
# what the reader has to know and `READABLE` is longer than this list: `#` opens
# a HEADING in markdown, and in a `.txt` it opens nothing at all, since plain
# text has no comment syntax to open. Excepting `.md` alone left a `.txt`
# holding markdown turning a heading into a stampless rider at exit 2 -- the
# one alarm this design invents rather than loses, one extension over from
# where it was closed. Written this way, an extension added to `READABLE` later
# states its own answer instead of inheriting `#` (round 3, finding 18).
HASH_COMMENTS = (".py", ".yml", ".yaml", ".sh", ".toml", ".cfg")
```

```python
def comment_blocks(lines, rel):
```

The docstring paragraph, in place of the one that asks callers to remember:

```
    **`rel` is REQUIRED, because it decides whether `#` opens a comment at
    all.** It has no default: the mode a forgotten argument would land in is
    the markdown-unaware one, which is the miss `region_lines` made -- it had
    `rel` in scope and passed it nowhere, so the reader returned no rider for a
    heading while the hasher still cut that line out of the region it hashes. A
    signature that cannot be called wrong is the guard; a sentence asking every
    caller to pass it is not (round 3, finding 21).
```

```python
    hash_opens_a_comment = rel.endswith(HASH_COMMENTS)
```

Five call sites in `tests/test_a_rider_reaches_its_file.py` pass no path today
and must name their corpus. Each fixture's own form says which:

```python
    # line 345 -- a `#` fixture built by `a_module()`
    assert len(riders.comment_blocks(two.splitlines(), "hooks/m.py")) == 2, (
    # line 380 -- prose and string literals, no comment head in any form
    assert riders.comment_blocks(text.splitlines(), "hooks/m.py") == []
    # line 394 -- a `#` block carrying a bare `#` continuation line
    assert riders.comment_blocks(lines, "hooks/m.py") == [(2, 4)]
    # line 416 -- two `#` riders back to back
    blocks = riders.comment_blocks(src.splitlines(), "hooks/m.py")
    # line 438 -- an HTML fixture whose own next line already calls it `d.md`
    blocks = riders.comment_blocks(src.splitlines(), "d.md")
```

The case, whose name is NAME NOT IN TREE:

```python
def test_a_heading_in_a_plain_text_file_is_not_a_rider():
    """`READABLE` admits eight extensions and `#` opens a comment in six. It
    opens a HEADING in markdown, and in a `.txt` it opens nothing at all --
    plain text has no comment syntax. Excepting `.md` alone left a `.txt`
    holding markdown reporting `BROKEN … no verification stamp` at exit 2 for a
    line nobody wrote as a rider, which is the one loss this design invents
    rather than loses (round 3, finding 18)."""
    src = f"# Title\n\n## {'RIDER:'} what one is\n\nprose.\n"
    assert riders.comment_blocks(src.splitlines(), "templates/doc.txt") == []
    # every extension where `#` really does open one, and the two where it
    # does not
    for ext, blocks in (
        (".py", [(3, 3)]),
        (".yml", [(3, 3)]),
        (".yaml", [(3, 3)]),
        (".sh", [(3, 3)]),
        (".toml", [(3, 3)]),
        (".cfg", [(3, 3)]),
        (".md", []),
        (".txt", []),
    ):
        assert riders.comment_blocks(src.splitlines(), "a" + ext) == blocks, ext
```

**Finding 19** — `.github/scripts/rider_check.py#tree_files`, returning what it
could not read alongside what it found. `missing` is NAME NOT IN TREE.

```python
def tree_files(root, roots=RIDER_ROOTS):
    """(every readable file under the rider roots, sorted; the roots that are
    not directories).

    **A root that names no directory is REFUSED rather than skipped.** Skipped,
    renaming one of the six leaves every rider under it read by nothing and the
    run still prints a clean total at exit 0 -- the largest silent loss this
    design has, because it is a whole corpus rather than one rider. The comment
    above `RIDER_ROOTS` says that list has been the defect twice, for
    `templates` and then for `.github` and `tests`; this is the same cause a
    third time, arriving through a rename instead of an omission (round 3,
    finding 19).
    """
    found, missing = [], []
    for top in roots:
        base = os.path.join(root, top)
        if not os.path.isdir(base):
            missing.append(top)
            continue
        for here, dirs, names in os.walk(base):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(names):
                if name.endswith(READABLE):
                    found.append(os.path.relpath(os.path.join(here, name), root))
    return sorted(found), missing
```

`all_riders` and `check` take the second value; `check` turns it into a
problem, which is what makes it loud:

```python
def all_riders(root, roots=RIDER_ROOTS):
    out = []
    for rel in tree_files(root, roots)[0]:
```

```python
    checker = checker or load_checker()
    ok, drifted, problems = 0, 0, []
    for top in tree_files(root, roots)[1]:
        problems.append(
            (
                top,
                "BROKEN",
                "a rider root that is not a directory. Every rider under it is "
                "read by nothing, and this run would otherwise print a clean "
                "total. Restore the directory, or take the name out of "
                "`RIDER_ROOTS`",
            )
        )
```

The case, whose name is NAME NOT IN TREE:

```python
def test_a_rider_root_that_is_not_a_directory_is_refused(tmp_path):
    """Renaming one of the six roots left every rider under it read by nothing
    while the run printed a clean total at exit 0. The comment above
    `RIDER_ROOTS` says that list has been the defect twice already; this is the
    same cause arriving through a rename (round 3, finding 19)."""
    stamped_module(tmp_path)
    (tmp_path / "agents").write_text("a FILE where a root was\n", encoding="utf-8")
    ok, drifted, problems = riders.check(
        str(tmp_path), roots=("hooks", "agents", "renamed"), checker=CHECKER
    )
    named = {where for where, _severity, _why in problems}
    assert named == {"agents", "renamed"}, (named, problems)
    assert ok == 1 and drifted == 0, (ok, drifted)
```

**Finding 20** — the deferral moves from `questions.md` C2 to the coordinate it
is about, as a rider, which is the form `seal/ledger.md`'s R6 row uses for the
same class. Above `all_riders` in `.github/scripts/rider_check.py`:

```python
    # RIDER: a file this cannot read or decode holds riders nothing reads, and
    # the run says nothing about it. Deferred rather than fixed, on two grounds
    # a root's absence does not have: the loss is one file rather than a
    # corpus, and a case for it built with `chmod` is nothing to root and a
    # no-op on Windows, so pinning it means monkeypatching the reader the way
    # `check_records`' own case does. Overturned by a file in the tree that
    # cannot be decoded, which no root holds today (round 3, finding 20).
    # Verified <date> against all_riders@<hash>
```

**Finding 22** — the sentence gets asserted, in
`tests/test_a_rider_reaches_its_file.py#test_only_without_a_verb_is_refused_rather_than_ignored`.
The signature takes `capsys` beside `tmp_path`, which is pytest's own capture
and needs no import the file does not already have:

```python
def test_only_without_a_verb_is_refused_rather_than_ignored(tmp_path, capsys):
```

```python
    stamped_module(tmp_path)
    for argv in (
        ["--root", str(tmp_path), "--only", "hooks/m.py"],
        ["--root", str(tmp_path), "--migrate", "--only", "hooks/m.py"],
    ):
        assert riders.main(argv) == 2, argv
        # contract §14 -- the sentence is what a person reads and acts on, so
        # an edit that empties it fails here rather than passing on the code
        printed = capsys.readouterr().err
        assert "`--only` scopes `--reverify`" in printed, (argv, printed)
```

**Finding 23** — one sentence in the module docstring, under the paragraph the
fix added, so the list of losses stays the whole list:

```
The third loss is the corollary of that fix rather than a cost of it: a rider
written in the `#` form inside a markdown file is read by nothing and says
nothing about it. Markdown's rider form is the HTML comment, and the reader
cannot tell a rider meant as one from the heading that broke the build.
```

## Executed probes

| What was run | Result |
|---|---|
| `python3 .github/scripts/rider_check.py` on the working tree, exit read without a pipe | `20 ok · 0 drifted · 0 broken`, exit 0 |
| `./bin/test tests/test_a_rider_reaches_its_file.py -q` | `29 passed in 0.51s`, exit 0 |
| `uvx ruff check` on the two files this diff changes | `All checks passed!`, exit 0 |
| `uvx ruff format --check` on the same two | `2 files already formatted`, exit 0 |
| Marker lines and riders per commit, over `RIDER_ROOTS` filtered by `READABLE`, each commit read through its own `rider_check.py` | `2f0dd02` 33 lines / 19 files / 20 riders · `677e10f` 36 / 19 / 20 · `982b8d3` 36 / 19 / 20 · `cdcadc0` 36 / 19 / 20 |
| Five argument combinations on a three-rider tree with three stale hashes, each on a fresh copy, recording which files were rewritten | `--reverify` → all three, exit 0 · `--reverify --only hooks/m1.py` → `m1.py` alone, exit 0 · **`--migrate --reverify --only hooks/m1.py` → none, `0 migrated · 0 refused`, exit 0** · **`--migrate --reverify` → none, same total, exit 0** · `--migrate --only hooks/m1.py` → none, refused, exit 2 |
| `--reverify --only ""` on the same three-rider tree | all three rewritten, `3 restamped · 0 refused`, exit 0 — byte-identical to the unscoped run |
| `--only` spellings against a one-rider tree | `hooks/m0.py` written 1 refused 0 · `./hooks/m0.py` 0/1 · `/abs/hooks/m0.py` 0/1 · `hooks/m0.PY` 0/1 |
| `comment_blocks` on one `## RIDER:` heading, once per extension | `.txt` `[(3, 3)]` · `.cfg` `[(3, 3)]` · `.toml` `[(3, 3)]` · `.sh` `[(3, 3)]` · `.yml` `[(3, 3)]` · `.md` `[]` |
| `check()` over a tree holding one `.txt` with that heading | `0 ok · 0 drifted · 1 broken` — `BROKEN templates/doc.txt:3: no verification stamp…` |
| `check()` over a tree holding one `.md` with a `#`-form rider and a full stamp | `0 ok · 0 drifted · 0 broken`, no problem raised |
| Three guards reverted one at a time on a copy, each substitution asserted to match exactly once, against the reader/hasher agreement case and the `--only` case | `region_lines` drops `rel` → reader `[]`, hasher stops keeping the marker line, they disagree · the markdown guard removed → reader `[(5, 5)]` · the `seen` counter removed → an `--only` selecting nothing refuses 0 |
| `.md` files under the six roots holding a `#`-headed marker line, at HEAD | 0 — so the markdown fix moved no hash in the tree |
| `tree_files` with one root replaced by a file of that name and one root absent | returns the surviving root's file only; `check()` reports on that one rider, nothing said about either root |
| `all_riders` over a tree holding a non-UTF-8 file and a mode-000 file, both with markers | `tree_files` names all three, `all_riders` returns one rider, `check()` gives `0 ok · 1 drifted · 0 broken` |
| `git diff 2138c98..cdcadc0` on the two files the re-stamped ledger rows cite | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` one line, the rider's own stamp · `skills/evidence-check/scripts/evidence_check.py` one line, the same |
| `grep -rn rider` over `.github/workflows/` and the runner wrappers | no workflow calls the checker directly; `tests/test_a_rider_reaches_its_file.py` runs it as a subprocess against the real root and asserts exit 0, so CI enforces it through the suite |

The probe file was one `test_tmp_*` script, run twice while it was being
completed, and deleted before this report was written.

## Inherited coordinates

Carried from the earlier rounds rather than re-established. Each was opened
once here and used; none of their verdicts were inherited.

| From | Coordinate | Why it was worth opening |
|---|---|---|
| round-2 | `.github/scripts/rider_check.py#reverify` · `#main` | round 2's 10, and where findings 16 and 17 sit |
| round-2 | `.github/scripts/rider_check.py#comment_blocks` · `#region_lines` | round 2's 11, and where findings 18, 21 and 23 sit |
| round-2 | `seal/ledger.md:1203` · `seal/ledger.md:1418` | round 2's 14 — the sentences to check |
| round-2 | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md` C2 | the two deferred skips — findings 19 and 20 |
| round-2 | `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` row S6 | the class the re-enumeration claimed closed — finding 16 |
| round-1 | whole tree | round 1's 9, still row 9 — the broad gate |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, the repository-wide lint and the typecheck. The narrow slice is executed and clean under both `ruff` arms | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md`, the row that already names it | the orchestrator — contract §2, and §3 for the instruction to run it here |
| Whether a rider written as a trailing comment should be caught at all, in either form | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` | the repository owner (carried, unchanged) |
| Whether a file `all_riders` cannot decode should be named — the deferral is right, its home is not (finding 20) | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md` C2 today; the fix moves it to a rider at the coordinate | the repository owner |
| Whether the mid-run `git checkout 29e0460 -- .` lost any uncommitted work | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` | the implementing session (carried, unchanged) |
| Whether a drifted rider is answered often enough to be worth its noise | `seal/follow-up.md` | the repository owner (carried, unchanged) |
| `templates/evidence-check.yml`'s rider is half spent | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` | the repository owner (carried, unchanged) |
| The quoted old-form stamp in two records, exempt by the `Target SHA` argument | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md` C1 | the repository owner (carried, unchanged) |

Findings 16 through 23 are NOT deferred in that sense. The run is capped, so
they become issues rather than fixes, and the record after this one ends the
run.

## For the record

Needs a fix: yes — findings 16, 17, 18 and 19
Loses a record or crashes: no
Contract changes: none in this round. Finding 18's fix would make `rel`
required on `.github/scripts/rider_check.py#comment_blocks`, whose callers are
`#riders_in`, `#region_lines` and five call sites in
`tests/test_a_rider_reaches_its_file.py`; finding 19's would widen
`#tree_files`' return, read by `#all_riders` and `#check`.
New units: none — this round writes no code.

Finding 17 is the one to read the floor line against, since it can overwrite
`Verified` dates for riders nobody re-read. It is `no` here on the same ground
round 1 answered `no` for the twelve dates it had actually destroyed: nothing
leaves the `seal/` root and nothing crashes.

The broad gate has come due. It has run nowhere in this work item — the record
should carry `not yet` for it — and this round's findings become issues rather
than fixes, so nothing is scheduled to spend it.

## Proof

Files opened for this round, all at `cdcadc0` unless a commit is named:

- `.github/scripts/rider_check.py` — whole file
- `tests/test_a_rider_reaches_its_file.py` — lines 255-285 and 335-570
- `ruff.toml`
- `seal/ledger.md` — lines 1170-1215 and 1400-1425, and the round-2 diff of both rows
- `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` — rows S1 through S6
- `seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-2.md`
- `seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-2-fixes.md` — the verdict and probe tables
- `seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-1.md` — the floor rows only
- `seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-1-fixes.md` — lines 48-56
- `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md`
- `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` — lines 30-45
- `seal/specs/1788826000-a-stamp-names-content-not-a-commit/changelog.md` — the round-2 diff
- `skills/evidence-check/scripts/evidence_check.py` — the branch diff, and loaded as the resolver for every probe
- `.github/workflows/` — the file list, and a grep for the checker
- `/Users/x/.claude/skills/writing-style/SKILL.md`
