# Round 1 report — the fold checks run only as this repository's tests

- Work item: `1790260563-the-fold-checks-run-only-as-this-repositorys-tests`
- Pull request: #587 (draft) into `release/v0.15.3`
- Target SHA: `e9dfe623`, base `origin/release/v0.15.3` = `c52e8350`
- Reviewed in a `git clone --no-local` at the target SHA, under the round's
  scratchpad directory. Nothing was written in the main checkout except this
  file.
- Contract: `spec.md` and `plan.md` (frame `b6525a56`), issues #566, #530, #583.

## Summary

The spec is met on every scenario I opened, S1 to S11. The command reads its
three rows, the flags override them, the two test modules call the shipped
functions, `first_cell` takes the whole container class, and the wrap skip is
no wider than the shape reader. The four findings that need a fix are all in
the new command's edges, the ones a repository other than this one meets
first. The command passes having checked nothing when it is typed in a
subdirectory. It crashes on a file it cannot decode or parse. It tells an
opted-out repository that it has no `seal/` root. And it says a listed
document "does not exist" when the document exists one directory down.

## Stage 1 — spec compliance

Each claim in the hand-back was checked against the code rather than taken
as given.

- **Claimed: the command reads the three rows through
  `hooks/config.py#config_rows`.** Confirmed at
  `skills/settle/scripts/fold_check.py:399-460`. `declared` refuses a
  malformed row with the messages S5 pins. Executed: `bin/fold-check` in the
  clone printed `read 136 statements in 14 documents under docs/; the cutoff
  1790154761 binds 21` and `held 14 documents under docs/ to 1000 lines, 0
  listed over it`, exit 0 (S1).
- **Claimed: root resolution goes through `hooks/optin.py#home_at`, which
  diverges from the spec, and the overview records it.** The overview does
  record it. Its grounds say `home_at` "also honours the opt-out marker".
  What the code does with that is finding 3: the opt-out is honoured, and the
  sentence the person reads about it is false. Nothing resolves the
  repository from the directory the command was typed in. That is finding 1.
- **Claimed: the two test modules import the shipped script, and the
  constants are gone.** Confirmed. The prose pin reads through
  `fold_check.declared` (`tests/test_a_document_has_room_for_the_next_fold.py:55-62`).
  One sentence in the other module still names the removed constant (⬜ 5).
- **Claimed: `settle.py#first_cell` strips any combination of container
  syntax (`CONTAINER_RE`).** Confirmed at `skills/settle/scripts/settle.py:447-465`.
  Executed: the old rule, restored in memory, labels `> | claim |`, `- | claim |`,
  `> - | claim |`, `1. | claim |`, `>| claim |` and `&lt;!-- > | claim |` by
  their prefix, so the new cases are red against it (§15 holds for them).
  The probe's edge cases behaved as the spec says: `\t>\t-\t|`, `1.5. |`
  and `** |` drop to `claim`, and `- [ ] |` keeps its label, because a task
  box is not in the class the spec enumerates.
- **Claimed: `test_docs_line_wrap.py#prose_lines` skips exactly
  `fold_check.enforced_lines`.** Confirmed at `tests/test_docs_line_wrap.py:186-207`.
  `enforced_lines` and `shape_problems` ask the same `names_targets`
  question, so the lines skipped are the lines the shape reads as targets.
- **Claimed: Q1 measured 115 of 136 unbound where the prose says 101, and the
  prose was left alone.** Executed: `bin/fold-check --shape-from 0` read 136
  and bound 136, and the default cutoff binds 21, so 115 are unbound. The
  grounds in `questions.md` Q1 hold on reading the sentence in
  `docs/the-evidence-ledger.md` §*The fold, and what tells it from a
  deletion*: it counts "the 101 folded before it" and separately "those of
  work items released with it or still waiting from before it". I accept
  leaving the prose alone.
- **Ledger.** Executed: `bin/evidence-check .` at the target SHA, exit 0,
  2089 ok, 0 drifted, 0 broken. The three removals and the fragment rows were
  not re-derived line by line. The check is what reads them, and it is clean.

## Stage 2 — quality

### 🟡 1 — Typed in a subdirectory, `fold-check` passes having checked nothing

`skills/settle/scripts/fold_check.py:547` takes `root` from the directory the
command was typed in, not from the repository that directory belongs to.
From `docs/` in a repository that declares both rows, `home_at` finds no
`docs/seal/`, so neither row is read. The command prints `neither … is
declared in <repo>/docs, which has no seal/ root at either place, so nothing
was checked` and **exits 0**. Executed twice: once in the clone's `docs/`, and
once in a planted repository.

This matters because exit 0 is what an agent or a script acts on. The
command exists so that a fold runs unattended, and an unattended run that
started one directory too deep passes. The other shipped commands that read
a repository resolve it with `hooks/optin.py#repo_root`:
`skills/implement/scripts/seal.py:289`,
`skills/code-review/scripts/chain_check.py:4183` and
`skills/code-review/scripts/round_record.py:2431`. `settle` also uses the
current directory, but from a subdirectory it exits 2, so it cannot pass
quietly.

### 🟡 2 — A file that will not parse or decode crashes the command with a traceback at exit 1

`target_problem` parses a `::name` target with `ast.parse` and nothing
catches the result (`fold_check.py:254-255`). `read` opens every document as
UTF-8 with nothing catching that either (`fold_check.py:325-327`). Executed
in planted repositories:

- A target `tests/bad.py::x` whose file does not parse ended in
  `SyntaxError: invalid syntax`, with a traceback, at exit 1.
- A `docs/d.md` holding one Latin-1 byte ended in `UnicodeDecodeError`, with
  a traceback, at exit 1, after the command had already printed one status
  line.

Exit 1 is the command's code for "problems found", so a caller cannot tell a
crash from a result. The first case is reachable without a mistake by
anyone. A test file written for a newer Python than the one running
`fold-check` does not parse under the older one, and the 3.12 floor
guarantees nothing about the syntax of the repository's own files. The
docstring promises "2 the root or a value was unusable and nothing was
checked", and neither path reaches it.

Before this work, the same `ast.parse` lived in a test, and a crash there was
a test failure. As a shipped command it is a crash.

### 🟡 3 — An opted-out repository is told it has no `seal/` root

`fold_check.py:553-558`: `home_at` answers `""` both when there is no root
and when the repository opted out with `specseal-scratch`. `where` gives
both states the sentence "which has no seal/ root at either place". Executed:
in a planted repository with `seal/config.md` declaring both rows and the
marker under `.git/`, the command printed that sentence and exited 0.

The sentence is false for a repository that has a root. The overview
lists the opt-out as a reason for choosing `home_at`. `settle.py#main`
(`skills/settle/scripts/settle.py:1029-1047`) met this exact defect as its
own round 2 finding 7 and splits the two states. `fold_check.py` loads the
same resolver and inherited the defect settle had already fixed.

### 🟡 4 — A listed document one directory down is told it does not exist

`fold_check.py:337-338` reports every listed path that is not a top-level
`docs/*.md` as "is listed over the ceiling and does not exist". Executed: an
`Over the ceiling` entry for `docs/deep/big.md`, a file that exists, printed
`docs/deep/big.md is listed over the ceiling and does not exist` at exit 1.

Exit 1 is the right outcome, because the ceiling does not read that file.
The sentence is wrong about a fact, though. A person who reads it goes
looking for a deleted file that is still there, and learns nothing about the
actual cause: the ceiling reads only the top level.

### ⬜ 5 — A module docstring still says the prose is pinned against "this constant"

`tests/test_a_folded_statement_names_what_enforces_it.py:15-17`: "`tests/test_a_document_has_room_for_the_next_fold.py`
pins the prose against this constant." No such constant remains. The pin
reads the `Fold shape from` row. This is the one survivor I found of class 4.
A `git grep` for the four removed names, "ships no checker", "writes its own
check", "the check that holds it" and "against its constants" found nothing
else outside this work item, the changelog and the release file whose note
records the removal.

### ⬜ 6 — The cutoff statement's `Enforced by:` names a function nothing runs on its own

`docs/the-evidence-ledger.md:195`: `Enforced by: skills/settle/scripts/fold_check.py::bound`.
`bound` takes the cutoff as a parameter and holds no value. What holds this
repository's cutoff is `tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape`
together with the prose pin. The ceiling statement two paragraphs later
already names its pin beside the function. The spec asked for the re-point
to `fold_check.py`, so this is a suggestion, not a spec breach: add the
real-tree case as a second target.

### ⬜ 7 — The loader's refusal names the wrong reason for two of its three files

`fold_check.py:137-142`: `load` says "it is where the fold's markers are read
from" for whichever path is missing. That includes `hooks/config.py` and
`hooks/optin.py`, which are the config reader and the root resolver.

### ⬜ 8 — The shape test re-lists `docs/` instead of asking the command

`tests/test_a_folded_statement_names_what_enforces_it.py:58-63`,
`docs_documents`, is `fold_check.documents` spelled a second time. The · NAME NOT IN TREE
ceiling module already calls the shipped one.

## Classes enumerated (§12)

- **Every reader of the shape and the ceiling.** `git grep` for the three row
  names and the removed constants. Readers: `fold_check.declared` itself, the
  two real-tree cases, the prose pin and the S1 command case. All read
  through `fold_check.declared(fold_check.seal_home(ROOT))`. Nothing under
  `.github/` or `hooks/` reads either value.
- **Every container prefix `first_cell` can meet.** The spec's enumeration,
  plus tab-separated, mixed and repeated runs, and `- [ ]` as the one GFM
  prefix outside it (read above). The one other caller,
  `settle.py#anchored_rows` at `:529`, passes the whole line, so it gets the
  same arm.
- **Every line the wrap exemption could skip that is not an `Enforced by:`
  line with targets.** Read: `enforced_lines` returns only live lines inside
  a statement that start `Enforced by: ` and are not `nothing —`. A second
  `Enforced by:` line in one statement and a line in a statement below the
  cutoff are skipped too. The spec says "whatever the cutoff", and the shape
  check names the first of these where it binds. I found no line of another
  kind.
- **Every document or skill naming the removed constants or the old
  test-owned rule.** One survivor, ⬜ 5.

## Regression tests to plant

- `tests/test_a_document_has_room_for_the_next_fold.py`: the command typed in
  `docs/` of a planted git repository declaring a ceiling names the long
  document at exit 1 (🟡 1). A listed `docs/deep/…` entry is named as outside
  the top level, not as missing (🟡 4).
- `tests/test_a_folded_statement_names_what_enforces_it.py`: a `::name`
  target whose file does not parse is named as a problem, and the command
  exits 1 with no `Traceback` (🟡 2). A `docs/*.md` that is not UTF-8 exits 2
  naming the file (🟡 2). An opted-out planted repository's line says it
  opted out (🟡 3).

Each is in the fences below. None was run against the fix, because the fix
is the smith's to write. Each should be seen red against `e9dfe623` first.

## Facts for the evidence ledger

- `fold_check.py#main` resolves the repository from the current directory
  through `hooks/optin.py#repo_root` when `--root` is absent (after 🟡 1).
- `fold_check.py#target_problem` and `fold_check.py#read` turn an unreadable
  or unparseable file into a named problem or an exit 2, never a traceback
  (after 🟡 2).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | typed in a subdirectory, `fold-check` reads no row and exits 0 having checked nothing | `skills/settle/scripts/fold_check.py:547` | open | executed in the clone's `docs/` and in a planted repository: exit 0, "nothing was checked"; the other shipped readers resolve the repository through `hooks/optin.py#repo_root` |
| 🟡 2 | a `::name` target that will not parse, or a `docs/*.md` that will not decode, crashes the command with a traceback at exit 1 | `skills/settle/scripts/fold_check.py:254` | open | executed: `SyntaxError` and `UnicodeDecodeError` tracebacks, both at exit 1, which is the code for "problems found"; `read` at `:325` is the second site |
| 🟡 3 | an opted-out repository is told it "has no seal/ root at either place" | `skills/settle/scripts/fold_check.py:553` | open | executed with the scratch marker under `.git/`: that sentence, exit 0; `settle.py#main` splits the two states `home_at` folds into `""` |
| 🟡 4 | a listed document below the top level of `docs/` is reported as not existing | `skills/settle/scripts/fold_check.py:337` | open | executed: `docs/deep/big.md is listed over the ceiling and does not exist` for a file that exists |
| ⬜ 5 | the shape module's docstring says the prose is pinned "against this constant" | `tests/test_a_folded_statement_names_what_enforces_it.py:15` | open | read; the pin reads the `Fold shape from` row, and no constant remains |
| ⬜ 6 | the cutoff statement's `Enforced by:` names only `fold_check.py::bound`, which holds no value | `docs/the-evidence-ledger.md:195` | open | read; the spec asked for the re-point, and the real-tree case is what holds the value |
| ⬜ 7 | `load`'s refusal gives the markers reason for the config reader and the resolver too | `skills/settle/scripts/fold_check.py:137` | open | read |
| ⬜ 8 | `docs_documents` re-spells `fold_check.documents` | `tests/test_a_folded_statement_names_what_enforces_it.py:58` | open | read | · NAME NOT IN TREE
| 🟢 | S1 to S11 hold as the spec states them | `skills/settle/scripts/fold_check.py`, the six touched test modules | confirmed | executed: `bin/fold-check` exit 0 with the S1 line; `--shape-from 0` exit 1 binding 136; the six touched modules and the script-reach module pass narrow |
| 🟢 | #530 is closed as the class, not the five tokens | `skills/settle/scripts/settle.py:447` | confirmed | executed: the old rule restored in memory fails every container case; probe edges drop or keep as the spec enumerates |
| 🟢 | the wrap skip is no wider than the shape reader | `tests/test_docs_line_wrap.py:186` | confirmed | read: one predicate, `names_targets`, decides both |

## Executed probes

| What was run | Result |
|---|---|
| `bin/fold-check` at the clone root | exit 0; `read 136 statements in 14 documents under docs/; the cutoff 1790154761 binds 21`; `held 14 documents under docs/ to 1000 lines, 0 listed over it` |
| `bin/fold-check --shape-from 0` at the clone root | exit 1; binds 136; 141 problem lines |
| `bin/fold-check` typed in the clone's `docs/` | exit 0; "neither … is declared in …/docs, which has no seal/ root at either place, so nothing was checked" |
| `bin/test` over the six touched modules, `-p no:xdist` | exit 0, 233 passed |
| `bin/test tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` | exit 0, 43 passed, 7 skipped |
| `bin/evidence-check .` | exit 0; 2089 ok, 0 drifted, 0 broken |
| one probe script under the round directory, run once and deleted: opt-out, unparseable target, Latin-1 doc, deep listed path, subdirectory, six `first_cell` edges | see 🟡 1 to 🟡 4; the `first_cell` edges are listed in Stage 1 |
| the old `first_cell` rule restored in memory against six container rows | every row labelled by its prefix, so the new cases are red against it |
| broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Paste-ready fixes

### 🟡 1

In `skills/settle/scripts/fold_check.py#main`, after the `isdir` refusal:

```python
    root = os.path.abspath(args.root or os.getcwd())
    if not os.path.isdir(root):
        sys.stderr.write(
            f"fold-check: {root} is not a directory — nothing was checked\n"
        )
        return 2
    if args.root is None:
        # Typed anywhere inside a repository, the command reads that
        # repository, the way `seal.py` and `chain_check.py` resolve theirs.
        # Read from the directory it was typed in, a subdirectory has no
        # `seal/` and no `docs/`, and the run passed having checked nothing.
        root = load(OPTIN, "specseal_optin_for_folds").repo_root(root) or root
```

Its case, in `tests/test_a_document_has_room_for_the_next_fold.py`:

```python
def test_the_command_typed_in_a_subdirectory_reads_the_repository(tmp_path):
    """Round 1, finding 1: from `docs/`, the rows are the repository's."""
    root = config_root(tmp_path, [("Document line ceiling", "10")])
    subprocess.run(["git", "init", "-q", root], check=True)
    (tmp_path / "docs" / "long.md").write_text("x\n" * 11, encoding="utf-8")
    done = subprocess.run(
        [sys.executable, SCRIPT],
        cwd=str(tmp_path / "docs"),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert done.returncode == 1, done.stdout + done.stderr
    assert "docs/long.md is 11 lines, over the ceiling of 10" in done.stdout
```

### 🟡 2

In `skills/settle/scripts/fold_check.py#target_problem`:

```python
    if not path.endswith(".py"):
        return f"{target}: `::name` needs a Python file"
    try:
        with open(full, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except (OSError, ValueError, SyntaxError) as unreadable:
        # `ValueError` covers a file that is not UTF-8. A target written for
        # a newer Python than this one does not parse here, and that is a
        # problem to name, not a traceback at the exit code of a result.
        return (
            f"{target}: {path} could not be read as Python here "
            f"({type(unreadable).__name__}), so {name} was not looked for"
        )
```

And `read`, with `main` catching the refusal:

```python
def read(root, rel):
    try:
        with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
            return f.read()
    except (OSError, ValueError) as unreadable:
        raise Unusable(
            f"{rel} could not be read as UTF-8 text ({type(unreadable).__name__})"
        ) from unreadable
```

```python
    try:
        problems = run(root, (cutoff, ceiling, over, digests), where, sys.stdout)
    except Unusable as refused:
        sys.stderr.write(
            f"fold-check: {refused} — the run stopped there, and nothing above "
            "is a result\n"
        )
        return 2
```

Its cases, in `tests/test_a_folded_statement_names_what_enforces_it.py`:

```python
def test_a_target_that_does_not_parse_is_named_not_raised(tmp_path):
    """Round 1, finding 2."""
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "bad.py").write_text("def (:\n", encoding="utf-8")
    found = shape_problems(
        str(tmp_path), "d.md", f"{BOUND}\n**Rule.**\nEnforced by: tests/bad.py::x\n"
    )
    assert len(found) == 1 and "could not be read as Python here" in found[0], found


def test_a_document_that_is_not_utf8_exits_2_naming_it(tmp_path):
    """Round 1, finding 2: exit 1 means problems found, so a crash may not use it."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "d.md").write_bytes(b"caf\xe9\n")
    code, _, err = command("--root", str(tmp_path), "--ceiling", "5")
    assert code == 2 and "Traceback" not in err, err
    assert "docs/d.md could not be read as UTF-8 text" in err, err
```

### 🟡 3

In `skills/settle/scripts/fold_check.py#main`, replacing the `seal_home`
call and the `where` expression:

```python
    optin = load(OPTIN, "specseal_optin_for_folds")
    common = optin.git_common_dir(root)
    home = optin.home_at(root, common)
    if home:
        where = os.path.join(home, CONFIG)
    elif common and os.path.isfile(os.path.join(common, optin.SCRATCH)):
        # `home_at` answers "" for two states, and `settle.py#main` met them
        # given one sentence as its round 2 finding 7.
        where = (
            f"{root}, which has opted out — `{optin.SCRATCH}` is under its git "
            "directory, and its seal/config.md is not read"
        )
    else:
        where = f"{root}, which has no seal/ root at either place"
```

Its case, in `tests/test_a_document_has_room_for_the_next_fold.py`:

```python
def test_an_opted_out_repository_is_told_it_opted_out(tmp_path):
    """Round 1, finding 3: it has a root, so "no seal/ root" is false."""
    root = config_root(tmp_path, [("Document line ceiling", "10")])
    subprocess.run(["git", "init", "-q", root], check=True)
    (tmp_path / ".git" / "specseal-scratch").write_text("", encoding="utf-8")
    code, out, err = command("--root", root)
    assert code == 0, (out, err)
    assert "has opted out" in out and "no seal/ root" not in out, out
```

### 🟡 4

In `skills/settle/scripts/fold_check.py#ceiling_problems`:

```python
    for rel in sorted(set(over) - set(names)):
        if os.path.isfile(os.path.join(root, *rel.split("/"))):
            problems.append(
                f"{rel} is listed over the ceiling and is not a top-level "
                f"{DOCS}/*.md, the only documents the ceiling holds"
            )
        else:
            problems.append(f"{rel} is listed over the ceiling and does not exist")
```

Its case, in `tests/test_a_document_has_room_for_the_next_fold.py`:

```python
def test_a_listed_document_below_the_top_level_is_named_as_outside_it(tmp_path):
    """Round 1, finding 4: it exists, so "does not exist" is false."""
    root = tree(tmp_path, {"small.md": body(3)})
    (tmp_path / "docs" / "deep").mkdir()
    (tmp_path / "docs" / "deep" / "big.md").write_text(body(12, 1), encoding="utf-8")
    found = ceiling_problems(root, 10, {"docs/deep/big.md": (1, "#1")})
    assert found == [
        "docs/deep/big.md is listed over the ceiling and is not a top-level "
        "docs/*.md, the only documents the ceiling holds"
    ], found
```

Needs a fix: yes — 🟡 1 (a subdirectory run passes having checked nothing), 🟡 2 (a crash at exit 1 on an unparseable target or an undecodable document), 🟡 3 (the opted-out sentence is false), 🟡 4 (a listed file that exists is reported missing)
Loses a record or crashes: yes — 🟡 2: `fold-check` crashes with a traceback on a `::name` target that will not parse and on a `docs/*.md` that is not UTF-8

## Proof block

Files opened in this round (read or executed), all at `e9dfe623` in the clone:

- `seal/specs/1790260563-the-fold-checks-run-only-as-this-repositorys-tests/spec.md`, `overview.md`, `questions.md`, `changelog.md`; `plan.md` (the part the first output showed)
- `skills/settle/scripts/fold_check.py` (whole)
- `skills/settle/scripts/settle.py` (`CELL_RE`, `CONTAINER_RE`, `first_cell`, `anchored_rows` near `:529`, `main` to `:1075`)
- `hooks/optin.py` (`repo_root`, `git_common_dir`, `home_at`, `SCRATCH`); `hooks/config.py` (`config_rows`)
- `skills/verify/scripts/unverified_check.py` (`FOLD_MARKER`, `live_lines`)
- `tests/test_a_document_has_room_for_the_next_fold.py`, `tests/test_a_folded_statement_names_what_enforces_it.py` (whole)
- the diff of `bin/fold-check`, `bin/fold-check.cmd`, `bin/settle`, `bin/test`, `README.md`, `README.ko.md`, `docs/release-checklist.md`, `docs/the-evidence-ledger.md` (and its lines 170–215), `seal/config.md`, `skills/config/SKILL.md`, `skills/settle/SKILL.md`, `templates/config.md`, `tests/test_docs_line_wrap.py` (and `COVERED`), `tests/test_settle_reads_before_it_removes.py`, `tests/test_a_script_says_which_interpreter_it_needs.py`, `tests/test_the_settings_have_a_front_door.py`
- `seal/ledger/1790260563-the-fold-checks-run-only-as-this-repositorys-tests.md` (rows F2, F6, F8 via `git grep`; the rest through `evidence-check`)
