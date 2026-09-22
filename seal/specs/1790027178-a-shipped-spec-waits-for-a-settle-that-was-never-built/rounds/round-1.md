# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — review round 1

| Field | Value |
|---|---|
| Target SHA | 0adf3ed3345cf33574dfa0ab011ad7d2584d9230 |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 486 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `73ca11d14adffc688100bbc3a191e8a92ca8faa6..f27f7e864fe144597e16510601e1d5958d0ab2f5`, 2 commits |
| Contract changes | retire → round-1-report.md, round-1.md, survey, main, pytest |
| New units | OPTIN (depth 1); test_local_mode_is_refused_rather_than_read_as_an_empty_repository (depth 1); test_a_repository_with_no_root_at_either_place_says_so (depth 1); test_a_held_item_is_skipped_and_named_even_when_its_fold_is_recorded (depth 1); test_a_complete_retirement_is_not_reported_as_nothing_ever_folded (depth 1); test_an_untouched_tree_still_says_nothing_has_been_folded (depth 1); test_a_marker_inside_a_fenced_block_is_not_a_fold_record (depth 1); test_every_fence_shape_a_policy_document_can_carry (depth 1); test_the_shipped_skill_copied_into_docs_records_no_fold (depth 1); test_a_marker_below_the_top_level_of_docs_is_not_a_fold_record (depth 1); test_the_folded_line_reads_as_a_sentence (depth 1) |
| Needs a fix | yes — findings 1 through 6. Findings 1 and 2 are the fold's only safety property; 3 to 5 are what the command tells a reader; 6 is the pin the interlock in `spec.md` assumes. |
| Loses a record or crashes | yes — finding 1 removes a work item's directory under `seal/specs/` with no policy document having absorbed it, which is the one loss `skills/settle/SKILL.md` §4 says nothing can undo. The removal is recoverable from git until the fold branch commits, and the fold's next act is that commit. |

- [x] Pass

## What this round was asked

Round 1 of the build, against the whole branch — thirteen commits, 35 files,
the first review this work item has had. Spec compliance first, then quality.

Three classes were named for it, each to be enumerated by construction rather
than by grep: every path where `settle --retire` can remove a directory, with
the guard deliberately left unsatisfied; every reader whose corpus is
`seal/specs/`, to check the frame's count of fourteen modules and six
population floors; and both language editions, where a sentence corrected in
one and not the other is this branch's own measured defect class.

Five shapes were named to try to break: `settle` in local mode, a tie in the
majority rule that groups a work item, an `evidence-todo.md` with an open row,
a second run over an already-folded tree and a run interrupted between folded
and retired, and the interpreter floor.

Five corrections were handed over for re-judgement: the ticket's false
headline claim about what reads the shipped work items, the policy document
that specified `settle` before the ticket did, the owner's Q1 answered by its
default so that nothing is folded here, the builder's edit of `seal/ledger.md`
against its own prompt, and its divergence from the plan's reuse sentence.

The broad gate was withheld — it is the sealer's one act after the rounds
settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A fold marker inside a fenced code block satisfies the removal guard, and the skill's own example is that shape with a real work item id | `skills/verify/scripts/unverified_check.py:85` · `:636` | **fixed** `d5ea1d4a` | fixed at d5ea1d4a; executed — `settle --retire` removed the directory, exit 0 |
| 2 | 🟡 A marker in a non-policy file under `docs/` satisfies the guard; the walk is recursive where the fold is flat | `skills/verify/scripts/unverified_check.py:604` | **fixed** `d5ea1d4a` | fixed at d5ea1d4a; executed — a marker in `docs/experiments/` removed the directory |
| 3 | 🟡 In local mode the root is not resolved and the refusal written for local mode is unreachable | `skills/settle/scripts/settle.py:497` · `:508` | **fixed** `d5ea1d4a` | fixed at d5ea1d4a; executed — "a repository with none has nothing to settle" against a repository with one |
| 4 | 🟡 An item the evidence-todo guard is holding is reported as waiting to be retired, and counted `0 skipped` | `skills/settle/scripts/settle.py:377` · `:426` | **fixed** `d5ea1d4a` | fixed at d5ea1d4a; executed — `spec.md` G3 says skipped and named |
| 5 | 🟡 After a complete retirement the next run reports that nothing was ever folded, at exit 1 | `skills/settle/scripts/settle.py:450` | **fixed** `d5ea1d4a` | fixed at d5ea1d4a; executed — markers still in `docs/`; docstring `:52` says exit 1 is a refusal |
| 6 | 🟡 `open_rows` is duplicated into the shipped script with no test holding the two copies in step, while `FLOOR` in the same file is pinned | `skills/settle/scripts/settle.py:218` · `.github/scripts/fold_ledger.py:210` | deferred #487 | #487 — The repair is a walk comparing two functions' source and their regex constants — mechanism a fix pass may not add, and it pins nothing findings 1–5 wrote. The finding holds as read: the two `open_rows` are identical to the character and all four assertions call `settle.open_rows`; read — the interlock in `spec.md` rests on the two agreeing |
| 7 | ⬜ A space before a comma in a printed line, unpinned | `skills/verify/scripts/unverified_check.py:862` | **fixed** `d5ea1d4a` | fixed at d5ea1d4a; read |
| 8 | ⬜ The memo lists the six `Ran by` cells as unverified; `0adf3ed3` answered them | `overview.md:81` | **fixed** `d5ea1d4a` | fixed at d5ea1d4a; read — all six cells name `specseal:smith` |
| 9 | ⬜ `CLAUDE.md`'s ledger exception names removal only; this branch's case was drift-by-edit | `CLAUDE.md` §*a change writes fragments, never the shared file* | deferred #488 | #488 — A rule change to `CLAUDE.md` and `CONTRIBUTING.md`, which is mechanism a fix pass may not add, and `CLAUDE.md` is the repository owner's file. The finding holds: the exception names removal, this branch's case was drift-by-edit, and the gate refuses the branch that leaves the row unstamped; read |
| 🟢 confirmation | The framer's population-floor table, all eight modules | `spec.md` §*The ticket's headline claim is false* | confirmed | each coordinate opened; independent scan found the same fourteen |
| 🟢 confirmation | The eleven `seal/ledger.md` re-stamps were real re-reads, not `--reverify` stamping | `seal/ledger.md` | confirmed | four checked against the branch's diff; S7 re-verified by execution |
| 🟢 confirmation | The A10 dry-run figures | `overview.md` §*The dry run over this repository's own 97* | confirmed | executed — 81/37/16/0, 14 + 2, reproduced exactly |
| 🟢 confirmation | The grounds for diverging from `plan.md`'s `fold_ledger.py` reuse | `overview.md` §*Where spec and implementation diverged* | confirmed | `SHIPS` excludes `.github/` |
| 🟢 confirmation | Both language editions carry the same corrections | `README*.md` · `docs/one-root-by-lifetime*.md` | confirmed | read, diffed side by side |
| 🟢 confirmation | A7, the interpreter floor | `skills/settle/scripts/settle.py:95` | confirmed | executed at 3.9.6 and 3.12.9 |
| ❓ scope | The broad gate | whole tree | ❓ out of verified scope | §2 gives it to the sealer and the prompt withholds it; the orchestrating session answers |

## Paste-ready fixes

```python
DOCS = "docs"
FOLD_MARKER = re.compile(r"^<!-- specs/(\S+) -->$", re.M)
# A fence is a quotation, and the one document a session reads before it folds
# — `skills/settle/SKILL.md` §2 — shows the marker inside one, with a real
# released work item id. Copy that example into a `docs/` document and the
# line anchor below reads it as a fold, so `settle --retire` removes a
# directory no policy absorbed. `hooks/config.py` shipped this class once and
# `evidence_check` still carries it: the anchor says the marker stands alone
# on its line, never that the line is prose.
FENCE = re.compile(r"^(?P<fence>```+|~~~+).*?(?:^(?P=fence)`*\s*$|\Z)", re.M | re.S)


def outside_fences(text):
    """`text` with every fenced block blanked, line count preserved."""
    return FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
```
```python
            found.update(FOLD_MARKER.findall(outside_fences(text)))
```
```python
    for name in sorted(os.listdir(top)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(top, name)
        if not os.path.isfile(path):
            continue
        # The top level only. `spec.md` G2 and `skills/settle/SKILL.md` fix
        # the destination as a flat `docs/` — merge into a document that
        # exists, create one only for a new area, no `docs/policy/`. A fold
        # never writes below this level, so a marker below it is somebody's
        # notes: `docs/experiments/` is four scratch files, and one of them
        # holding a quoted marker excused a removal nothing absorbed.
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        found.update(FOLD_MARKER.findall(outside_fences(text)))
    return found
```
```python
READER = os.path.join(HERE, "..", "..", "verify", "scripts", "unverified_check.py")
OPTIN = os.path.join(HERE, "..", "..", "..", "hooks", "optin.py")
```
```python
    # `<root>/seal/` then `<git-common-dir>/seal/`, through the one resolver,
    # the way `evidence_check.py#seal_home` reaches it from the same depth.
    # Without this a local-mode repository was told it had no work items while
    # holding ninety-eight, and the sentence written for local mode — in the
    # `--released-at` refusal below — could never be printed, because this
    # check fired first and always.
    home = load(OPTIN, "specseal_optin").home_at(root)
    specs = os.path.join(home, "specs") if home else under(root, SPECS)
    if not os.path.isdir(specs):
        sys.stderr.write(
            f"settle: {root} has no {SPECS}/ at either place — nothing was read. "
            "This command folds work items, and a repository with none has "
            "nothing to settle.\n"
        )
        return 2
```
```python
    for work_item_id in survey["released"]:
        # The guard first. `spec.md` G3 says an item with an open row is
        # skipped AND NAMED, never folded — and an item that is both folded
        # and held was being named under "waiting to be retired", which is
        # the opposite instruction, while the summary counted it `0 skipped`.
        # `retire()` reads `open_items` again and keeps it either way; what
        # this fixes is what the reader is told before running anything.
        if work_item_id in held:
            survey["skipped"].append((work_item_id, held[work_item_id]))
            continue
        if work_item_id in folded:
            survey["folded"].append(work_item_id)
            continue
```
```python
    held = open_items(root)
    refused = [i for i in found["folded"] if i in held]
    removable = [i for i in found["folded"] if i not in held]
    if not removable and not refused:
        # Two states, and they used to share one sentence. A marker in `docs/`
        # whose directory is already gone leaves `survey` nothing to list, so
        # a second run reported that nothing had ever been folded — the one
        # thing the tree plainly contradicts, and the state every run of
        # `docs/release-checklist.md` step 2b ends in.
        marked = load(READER, "specseal_unverified_reader").folded_items(root)
        if marked:
            out.write(
                f"nothing left to retire: {len(marked)} work item"
                f"{plural(len(marked))} carry a `<!-- specs/<id> -->` marker "
                "in docs/ and none of them still has a directory under "
                f"{SPECS}/. The fold is complete.\n"
            )
            return 0
        out.write(
            "nothing to retire: no released work item carries a "
            "`<!-- specs/<id> -->` marker in docs/, so none of them has been "
            "folded yet. `settle` alone says which ones are waiting for one.\n"
        )
        return 1
```
```python
def test_the_guard_is_the_same_reader_as_the_release_folds():
    """`settle.py` carries its own `open_rows` because `.github/` is not on
    the list of what the plugin ships, so a shipped command may not import
    from it. `spec.md` §*One interlock does hold* then rests on the two
    answering alike — the only directories a fold removes are ones the
    release guard was never holding — and nothing held them together. The
    floor in the same file is pinned this way already."""
    import ast

    def source_of(path, name):
        tree = ast.parse(open(path, encoding="utf-8").read())
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == name:
                return ast.dump(ast.parse(ast.unparse(node)))
        raise AssertionError(f"{path} has no {name}")

    fold = os.path.join(ROOT, ".github", "scripts", "fold_ledger.py")
    mine = os.path.join(ROOT, "skills", "settle", "scripts", "settle.py")
    assert source_of(mine, "open_rows") == source_of(fold, "open_rows"), (
        "settle.py#open_rows and fold_ledger.py#open_rows have diverged. They "
        "are one rule in two files on purpose; a fold that reads an open row "
        "differently from the release guard removes a directory the guard was "
        "holding"
    )
    for const in ("SEPARATOR_RE", "DRAINED_RE"):
        assert getattr(settle, const).pattern == getattr(
            fold_ledger_module(), const
        ).pattern, f"{const} differs between the two readers"
```

## Executed probes

| What was run | Result |
|---|---|
| `settle --retire` against a fixture whose `docs/` document carries the marker inside a ```` ```markdown ```` fence | `removed seal/specs/1788302682-…/`, exit 0 — finding 1 |
| `settle --retire` against a fixture whose marker sits in `docs/experiments/2026-09-03-a-note.md` | directory removed, exit 0 — finding 2 |
| `settle` against a fixture whose `seal/` sits under the common git directory | exit 2, "has no seal/specs/ … a repository with none has nothing to settle" — finding 3 |
| `settle` then `settle --retire` against a fixture with a marker and one open `evidence-todo.md` row | listing said "waiting to be retired" and `0 skipped`; retire kept it, exit 1 — finding 4 |
| `settle --retire` twice against a fixture with one marked and one unmarked item | first removed the marked one at exit 0; second said "none of them has been folded yet", exit 1 — finding 5 |
| `settle --released-at origin/main` over this repository at the target SHA | `81 work items in 37 segments, 16 ungrouped, 0 skipped`, 1 unreleased, 14 + 2, 0.08 s — A10 reproduced |
| `settle` under `/usr/bin/python3` (3.9.6) and `/opt/homebrew/bin/python3.12` (3.12.9) | exit 2 with the floor sentence; exit 0 with the report — A7 |
| `settle.segment_of` over two coordinates in two files, via the command | `aaa/a.py`, the path-order winner |
| the six changed test modules, `uvx ruff check`, `uvx ruff format --check` | not run in this round — the orchestrator executed them at this SHA and handed the result over |
| the broad gate — full suite, repository-wide lint and typecheck | not yet. §2 assigns it to the sealer, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `settle` against a second real repository | already deferred in `overview.md` §*Not verified* | the repository owner, the next time the plugin is used elsewhere |
| whether the six population floors are still six after a fold | already deferred in `overview.md` §*Not verified* | the work item that folds this repository's own 97 |
