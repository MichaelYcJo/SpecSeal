# 1788826000-a-stamp-names-content-not-a-commit — review round 3

| Field | Value |
|---|---|
| Target SHA | cdcadc0 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed on the fully merged tree — 2735 passed, 2 skipped; `ruff check .` and `ruff format --check .` both exit 0; `rider_check.py` 23 ok, 0 drifted, 0 broken; `evidence-check .` exits 1 on drift alone, which CI reads as a warning. Merging last cost what merging last is for: one rider arrived BROKEN — #225's provisional `at <sha>` stamp, which its own text said the later branch must re-stamp — and `--migrate` closed it; three more arrived DRIFTED, each claim read and re-verified; and two ledger anchors were REMOVED rather than re-pointed, because #239 deleted the units #211's row cited while the claim itself stayed true on the two that survive |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 16, 17, 18 and 19 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of `1788826000-a-stamp-names-content-not-a-commit` (ticket #239), at target `cdcadc0`, base `origin/release/v0.9.1`. The verifying round over round 2's fixes, whose substance is `677e10f` and `982b8d3`, and the last round this work item gets: rounds 1 and 2 both closed on fixes, so the record after this one ends the run whatever it finds. This branch is the last of the release to merge, because its migration sweeps the stamps three sibling branches planted in the old form — so a finding here was stated as expensive and a missed one as shipping the convention wrong.

Round 2 had opened two things, both the code being looser than what it says: a `--reverify --only <path that does not exist>` reporting `0 restamped · 0 refused` at exit 0, which is the answer a script reads for a command the drift message hands a person to type; and a markdown heading read as a `#` comment head, so a single `## RIDER:` line in a `.md` file exits 2 — the only loss in this design that invents an alarm where every other one misses one.

The named targets. The re-enumeration's three further `--only` instances and the one the fix itself would have created, where `region_lines` had `rel` in scope and passed it nowhere, so the reader would have returned no rider for a heading while the hasher still cut that line out of the region — a hash and a corpus disagreeing about what a block is. The markdown guard, verified for every corpus the checker walks, including a file whose extension is not `.md` but whose content is markdown. The two silent skips left as a judgment for the repository owner, with the round asked whether a silent skip in the checker that exists to stop silent skips is a finding of its own. The `Checked` column once more, since this work item had already destroyed twelve true dates once and re-stamped two ledger rows before reading them, and round 2 touched both rows again to add the sentence saying who read what. The marker counts, now given per commit. And lint, which had run nowhere in the work item — `uvx` was named as available, on the ground that *unverified* is not the same as *clean*.

Rounds 1 and 2's subject matter — the twelve restored dates, the exclusion rule, the self-reference fixed point and the `Target SHA` exemption — was settled and not to be re-reviewed.

The report was to be a file, finding ids bare integers, one row per finding, every coordinate carrying its full path, `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry, no literal HTML comment marker outside a real one, no real user path, and no version at or above the running one.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | ❓ out of verified scope — the full suite, the repository-wide lint and the typecheck | whole tree | answered | contract §2 and §3. The spawn prompt ordered `uvx ruff check .` and `uvx ruff format --check .`, repository-wide, which §2 reserves for one run after the rounds settle; that instruction is declined and named here. **executed** on the narrow slice instead — the two files this diff changes: `uvx ruff check` gives `All checks passed!` exit 0 and `uvx ruff format --check` gives `2 files already formatted` exit 0. So `ruff` runs in this environment and the diff is clean under both arms; what is still unrun is the other 100-odd Python files, the full suite and the typecheck |
| 10 | 🟡 `--reverify --only <path>` that matches no rider printed `0 restamped · 0 refused` at exit 0 | `.github/scripts/rider_check.py#reverify` | **answered** | **executed** — on scratch trees, `hooks/m0.py` writes and refuses nothing; `./hooks/m0.py`, `/abs/hooks/m0.py` and `hooks/m0.PY` each write nothing and refuse by path, so the three spellings a person actually types are all caught. Seen red: with `if only and not seen:` removed, the same call refuses nothing. The class is NOT fully closed — findings 16 and 17 |
| 11 | 🟡 A markdown heading was read as a `#` comment head | `.github/scripts/rider_check.py#comment_blocks` | **answered** | **executed** — `## RIDER: …` in a `.md` returns `[]` from the reader and `0 ok · 0 drifted · 0 broken` from `check()`, against `[(3, 3)]` and one BROKEN with the guard reverted. The two real forms are untouched. The reader and the hasher now agree: with `rel` dropped from `region_lines`' call the hasher stops keeping the heading, which is what the new case asserts. No `.md` file under the six roots holds a `#`-headed marker line at HEAD, so the fix moved no hash in the tree — which is why the cases are the only thing proving it, and all three are red under mutation. The `.md` half is closed; the corpus half is not — finding 18 |
| 12 | ⬜ The marker-line count was 33 with 13 extras where three records said 31 with 11 | `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` · `rounds/round-1-fixes.md` | **answered** | **executed**, independently and per commit, over the files the checker's own walk admits: `2f0dd02` 33 marker lines in 19 files and 20 riders; `677e10f` 36 and 20; `982b8d3` 36 and 20; `cdcadc0` 36 and 20. So 13 extras and then 16, exactly as all three records now read, each figure naming its commit |
| 13 | ⬜ The trailing-rider deferral named the `#` form only | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` · `rounds/round-1-fixes.md` | **answered** | **read** — both files now name both forms, say which round executed each half, and carry the count per commit. `overview.md` also names who answers it and why a fix pass may not build the rule |
| 14 | ⬜ Two ledger rows the fix pass re-stamped carried no note of a reading | `seal/ledger.md:1203` · `seal/ledger.md:1418` | **answered** | **executed** — both added sentences are true. Over the whole branch, `git diff 2138c98..cdcadc0` on `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` is one line, `Verified 2026-09-06 at 4581fe1.` becoming `Verified 2026-09-06 against test_the_refusal_above_can_actually_fail@8e0a246a.`, and on `skills/evidence-check/scripts/evidence_check.py` it is one line, `Verified 2026-09-07 at 70c272c.` becoming `Verified 2026-09-07 against unread_items@9046e0b6.`. Both rows keep their original `Checked` date, which is right: the claim did not move, only a comment inside the region did, and the reconciliation is stated in the Notes column rather than left for a reader to assemble |
| 15 | ⬜ `overview.md` listed as open a records-arm refusal that `2f0dd02` had answered | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md` | **answered** | **read** — the row is marked ✅ with the commit that answered it and the count the arm now reads, and the one refusal that replaced it is a row of its own naming the orchestrator |
| 16 | 🟡 `--migrate --reverify --only PATH` runs the migration, drops both other arguments, and prints a clean total at exit 0 | `.github/scripts/rider_check.py#main` · claimed closed in `.github/scripts/rider_check.py` module docstring, `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` row S6 and `seal/specs/1788826000-a-stamp-names-content-not-a-commit/changelog.md` | deferred #250 | **executed** — on a three-rider tree whose stamps are all stale, `--reverify --only hooks/m1.py` rewrites `m1.py` alone, while `--migrate --reverify --only hooks/m1.py` rewrites nothing and prints `0 migrated · 0 refused` at exit 0. `--migrate --reverify` does the same, silently dropping the verb. The guard reads `args.only and not args.reverify`, so adding `--reverify` satisfies it and `if args.migrate:` takes the branch. This is finding 10's own shape — a clean total at exit 0 for a run that did nothing the person asked — and after the migration has run once, `--migrate` is a permanent no-op, so this combination can never accidentally do the right thing. Three records state the class as closed: the docstring says `--only` "is REFUSED anywhere else rather than ignored", the changelog says "`--only` without `--reverify`, and beside `--migrate`, … both are refused before anything is read", and row S6 says "all three now exit 2 with a sentence" |
| 17 | 🟡 `--only ""` silently un-scopes the run and restamps every drifted rider | `.github/scripts/rider_check.py#main` · `.github/scripts/rider_check.py#reverify` | deferred #250 | **executed** — on a three-rider tree with three stale hashes, `--reverify --only ""` rewrites all three and prints `3 restamped · 0 refused` at exit 0, byte-identical to the unscoped run. Both tests for *was a path given* are truthiness tests (`if args.only and not args.reverify` and `if only and rider.rel != only`), so an empty string reads as absent and the `seen` guard never fires. The reachable case is `--only "$path"` from a wrapper or a shell line where the variable is unset. What it costs is round 1's finding 1 in a new currency: `--reverify` writes today's date beside every hash that moved, so a person who scoped the run to one rider stamps a reading they did not perform on every drifted rider in the tree |
| 18 | 🟡 The markdown guard excepts the one extension where `#` is not a comment instead of naming the six where it is | `.github/scripts/rider_check.py#comment_blocks` | deferred #250 | **executed** — `comment_blocks` with a `.txt` path returns `[(3, 3)]` for `## RIDER: what one is`, and `check()` over a tree holding one `.txt` gives `0 ok · 0 drifted · 1 broken` with `BROKEN templates/doc.txt:3: no verification stamp…`, exit 2. `READABLE` admits eight extensions; `#` opens a comment in six of them and in neither `.md` nor `.txt`, and `.txt` has no comment syntax at all, so a plain-text file holding markdown invents exactly the alarm the fix says it closed. **read** — no `.txt`, `.cfg`, `.toml` or `.sh` file stands under the six roots today, so it is latent rather than live. The second half is the direction of the default: written as `not (rel or "").endswith(".md")`, any extension added to `READABLE` later inherits *`#` is a comment* without saying so, which is the direction the module docstring says a rule here must not fall |
| 19 | 🟡 Renaming one of the six roots leaves its riders read by nothing at exit 0, and deferring that is the third occurrence of a class the file names twice | `.github/scripts/rider_check.py#tree_files` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md` C2 | deferred #250 | **executed** — with `agents` replaced by a file of that name and a third root that does not exist, `tree_files` returns only the `hooks` entry and `check()` reports on that one rider alone, no problem raised for either missing root. **read** — the comment above `RIDER_ROOTS` says this list "has been the defect twice", once for `templates` and once for `.github` and `tests`, the second of which left three riders held by nothing. A root that names no directory is the third form of the same cause and the largest silent loss in the design, since it is a whole corpus rather than one rider. Judgment against the deferral: C2 defers it because refusing an absent root is "a new RULE about what CI rejects", and that is true of refusing an `--only` that selects nothing as well, which round 2 fixed. Two lines refuse it, and the accepted-loss argument does not reach it — the module's asymmetry accepts a lost alarm only where the loss is STATED, and this one is stated in a work-item file rather than beside the code |
| 20 | ⬜ The `all_riders` deferral is right, but it lives in a document with a shorter life than the code | `.github/scripts/rider_check.py#all_riders` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md` C2 | deferred #250 | **executed** — a non-UTF-8 file and a mode-000 file are both walked and both dropped: `tree_files` returns all three names, `all_riders` returns one rider, and `check()` reports `0 ok · 1 drifted · 0 broken` with nothing said about the two it could not read. Deferring is defensible, and on two grounds C2 does not give: one file is not a corpus, and a `chmod`-built case is nothing to root and a no-op on Windows, which is the objection `seal/ledger.md`'s R6 row already records for this exact shape and why that row built its case by monkeypatching instead. What is wrong is only where the deferral sits. `questions.md` belongs to a work item and stops being read when the item ships, while the swallow is permanent; R6 answers the same class by deferring it **as a rider at its own line**, which is this branch's own convention and `seal/follow-up.md`'s rule for anything tied to a coordinate |
| 21 | ⬜ `comment_blocks` keeps a default `rel=None`, whose behavior is the markdown-unaware one the round just fixed | `.github/scripts/rider_check.py#comment_blocks` | deferred #250 | **read** — the docstring says "so every caller passes it", and both production callers do, so nothing ships wrong. The guard against the recurrence is that sentence rather than the signature: omitting the argument is silent and lands in the mode that reads a heading as a comment, which is precisely the miss `region_lines` had made and this round's own new case exists to catch. Five call sites in `tests/test_a_rider_reaches_its_file.py` still omit it (lines 345, 380, 394, 416 and 438), so the case file exercises a mode production never uses — including at line 438, where the fixture is markdown and the very next line names its path as `d.md`. Finding 18's fix closes this by making `rel` required |
| 22 | ⬜ One of the two new refusal sentences is pinned by a case and the other is not | `.github/scripts/rider_check.py#main` · `tests/test_a_rider_reaches_its_file.py#test_only_without_a_verb_is_refused_rather_than_ignored` | deferred #250 | **read** — `test_reverify_says_so_when_only_selects_no_rider` asserts the sentence ("no rider in the tree has this path"), while `test_only_without_a_verb_is_refused_rather_than_ignored` asserts `main(argv) == 2` and nothing about the text. Contract §14: a change to a message somebody reads and acts on is pinned in the same commit, and this one is the sentence that tells a person their argument was ignored. An edit that empties it leaves both cases green |
| 23 | ⬜ A markdown rider written in the `#` form is now read by nothing, and that loss is not in the docstring's list of losses | `.github/scripts/rider_check.py#comment_blocks` | deferred #250 | **executed** — a `.md` under a scanned root holding `# RIDER: a claim` with a full stamp beneath it gives `0 ok · 0 drifted · 0 broken` and no problem raised. This is the accepted direction, so it is not a defect. What is missing is the disclosure: the module docstring's stated losses are the two exclusion cases, and the paragraph the fix added says "every loss stated here goes that one way", which now has an unstated third member. The inline comment states a fact about today's tree ("no `.md` file in the tree uses the `#` form") where the docstring states the rule |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` · `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` row S4 | round 1's 1 — fixed |
| round-1 | `.github/scripts/rider_check.py:421` · message at `:344` | round 1's 2 — fixed |
| round-1 | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` | round 1's 3 — fixed |
| round-1 | `.github/scripts/rider_check.py:197` and `:218` | round 1's 4 — fixed |
| round-1 | `agents/smith.md:60` · `skills/implement/SKILL.md:379` · `templates/evidence-check.yml:5` | round 1's 5 — fixed |
| round-1 | `.github/scripts/rider_check.py:359` and `:504` · `phases/phase-4.md` · ledger row S4 | round 1's 6 — fixed |
| round-1 | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md:28` · `overview.md:36` | round 1's 7 — fixed |
| round-1 | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-3.md` | round 1's 8 — fixed |
| round-1 | whole tree | round 1's 9 — deferred |
| round-2 | `.github/scripts/rider_check.py#reverify` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` | round 2's 1 — answered |
| round-2 | `.github/scripts/rider_check.py:477` · message at `:368` | round 2's 2 — answered |
| round-2 | `.github/scripts/rider_check.py#reverify` · `phases/phase-4.md` | round 2's 3 — answered |
| round-2 | `.github/scripts/rider_check.py:170-232` | round 2's 4 — answered |
| round-2 | `.github/scripts/rider_check.py:387` · `phases/phase-4.md` · ledger row S4 | round 2's 6 — answered |
| round-2 | `questions.md:28` · `overview.md:38` | round 2's 7 — answered |
| round-2 | `phases/phase-3.md` | round 2's 8 — answered |
| round-2 | `.github/scripts/rider_check.py:464` and `:603-610` | round 2's 10 — fixed |
| round-2 | `.github/scripts/rider_check.py:219`, docstring at `:170-196` | round 2's 11 — fixed |
| round-2 | `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md:20` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:36` · `rounds/round-1-fixes.md:52` | round 2's 12 — answered |
| round-2 | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:36` · `rounds/round-1-fixes.md:52` | round 2's 13 — answered |
| round-2 | `seal/ledger.md:1203` · `seal/ledger.md:1418` | round 2's 14 — answered |
| round-2 | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:37` | round 2's 15 — answered |

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
