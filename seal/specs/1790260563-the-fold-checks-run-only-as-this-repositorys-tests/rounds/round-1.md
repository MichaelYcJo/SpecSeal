# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — review round 1

| Field | Value |
|---|---|
| Target SHA | e9dfe623431a1472261c76004cfad56eb57269ab |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 587 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `f181e30abd4539320446d17dd5cbc0eee6f20b68..d32c365a843cecb12bc20b9a1a84c94b9655252f`, 2 commits |
| Contract changes | load → plugin_name, read_version, hygiene.yml, CHANGELOG.md, main, running, load_input, dead_session_ids, fresh_leases, 0.9.1.md, round-1-report.md, round-1.md, load, pull_request_state, chain, where, orchestration.md, read_state, plugin_version, reader, optin, config_rows, open_rows, coordinates, anchored_rows, survey, retire, SKILL.md, broad_command, refusal, rows_read, fenced_row_at, fence_left_open, gate, broad_gate.py, measure, segment_slices, pytest |
| New units | why (depth 1); optin (depth 1); located (depth 1); git_init (depth 1); test_the_command_typed_in_a_subdirectory_reads_the_repository (depth 1); test_an_opted_out_repository_is_told_it_opted_out (depth 1); test_a_repository_with_no_root_is_told_it_has_none (depth 1); test_a_listed_document_below_the_top_level_is_named_as_outside_it (depth 1); test_a_target_file_that_will_not_parse_exits_2_naming_it (depth 1); test_a_document_that_is_not_utf8_exits_2_naming_it (depth 1); test_a_script_copied_on_its_own_says_which_sibling_it_misses (depth 1) |
| Needs a fix | yes — 🟡 1 (a subdirectory run passes having checked nothing), 🟡 2 (a crash at exit 1 on an unparseable target or an undecodable document), 🟡 3 (the opted-out sentence is false), 🟡 4 (a listed file that exists is reported missing) |
| Loses a record or crashes | yes — 🟡 2: `fold-check` crashes with a traceback on a `::name` target that will not parse and on a `docs/*.md` that is not UTF-8 |

- [x] Pass

## What this round was asked

Round 1 of work item 1790260563 reviews the build at e9dfe623 against spec.md and plan.md (frame b6525a56): fold_check.py and bin/fold-check reading three config rows, first_cell's container prefixes (#530), and the wrap skip for Enforced-by lines (#583). The classes enumerated are the readers of the shape and the ceiling, every container prefix, every line the wrap skip could reach, and every carrier still naming the removed constants.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | typed in a subdirectory, `fold-check` reads no row and exits 0 having checked nothing | `skills/settle/scripts/fold_check.py:547` | **fixed** `0bbf219f` | fixed at 0bbf219f; executed in the clone's `docs/` and in a planted repository: exit 0, "nothing was checked"; the other shipped readers resolve the repository through `hooks/optin.py#repo_root` |
| 🟡 2 | a `::name` target that will not parse, or a `docs/*.md` that will not decode, crashes the command with a traceback at exit 1 | `skills/settle/scripts/fold_check.py:254` | **fixed** `0bbf219f` | fixed at 0bbf219f; executed: `SyntaxError` and `UnicodeDecodeError` tracebacks, both at exit 1, which is the code for "problems found"; `read` at `:325` is the second site |
| 🟡 3 | an opted-out repository is told it "has no seal/ root at either place" | `skills/settle/scripts/fold_check.py:553` | **fixed** `0bbf219f` | fixed at 0bbf219f; executed with the scratch marker under `.git/`: that sentence, exit 0; `settle.py#main` splits the two states `home_at` folds into `""` |
| 🟡 4 | a listed document below the top level of `docs/` is reported as not existing | `skills/settle/scripts/fold_check.py:337` | **fixed** `0bbf219f` | fixed at 0bbf219f; executed: `docs/deep/big.md is listed over the ceiling and does not exist` for a file that exists |
| ⬜ 5 | the shape module's docstring says the prose is pinned "against this constant" | `tests/test_a_folded_statement_names_what_enforces_it.py:15` | **fixed** `0bbf219f` | fixed at 0bbf219f; read; the pin reads the `Fold shape from` row, and no constant remains |
| ⬜ 6 | the cutoff statement's `Enforced by:` names only `fold_check.py::bound`, which holds no value | `docs/the-evidence-ledger.md:195` | **fixed** `0bbf219f` | fixed at 0bbf219f; read; the spec asked for the re-point, and the real-tree case is what holds the value |
| ⬜ 7 | `load`'s refusal gives the markers reason for the config reader and the resolver too | `skills/settle/scripts/fold_check.py:137` | **fixed** `0bbf219f` | fixed at 0bbf219f; read |
| ⬜ 8 | `docs_documents` re-spells `fold_check.documents` | `tests/test_a_folded_statement_names_what_enforces_it.py:58` | **fixed** `0bbf219f` | fixed at 0bbf219f; read \| · NAME NOT IN TREE |
| 🟢 | S1 to S11 hold as the spec states them | `skills/settle/scripts/fold_check.py`, the six touched test modules | confirmed | executed: `bin/fold-check` exit 0 with the S1 line; `--shape-from 0` exit 1 binding 136; the six touched modules and the script-reach module pass narrow |
| 🟢 | #530 is closed as the class, not the five tokens | `skills/settle/scripts/settle.py:447` | confirmed | executed: the old rule restored in memory fails every container case; probe edges drop or keep as the spec enumerates |
| 🟢 | the wrap skip is no wider than the shape reader | `tests/test_docs_line_wrap.py:186` | confirmed | read: one predicate, `names_targets`, decides both |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
