# 1790138190-settle-leaves-twelve-directories-with-no-way-out — review round 1

| Field | Value |
|---|---|
| Target SHA | 4d19cc0418c97dd341f886b4d11c728bff8033d9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #525 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `492c9b8e59f2db4d41ddb4eb5b45711a590d5856..100058fa0956b66048b52e80840d10eb10472e29`, 10 commits |
| Contract changes | none |
| New units | CHECKER (depth 1); wrote_a_spec (depth 1); test_a_specs_directory_outside_the_seal_root_stays_in_the_range (depth 1); test_a_spec_deleted_by_an_earlier_merge_is_not_a_rule_retirement (depth 1); test_a_fenced_anchor_still_keeps_the_directory (depth 1); test_a_row_at_the_old_evidence_address_keeps_the_directory (depth 1); test_a_closed_row_is_told_to_merge_before_its_directory_goes (depth 1); test_a_spec_deleted_by_an_earlier_merge_is_still_a_deletion (depth 1); test_a_history_git_cannot_read_counts_as_a_spec_written (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4 (🟡); finding 5 is ⬜ and not counted |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 read the whole branch against its base, `f8f1c9d..4d19cc0`. Stage 1 compared it with `spec.md` and the owner's design comment on #517 (D1–D3). Stage 2 attacked five things: the #511 guard's coverage, the one retirement predicate shared by four readers, whether a reader can pass a deletion that is not a retirement, the empty-root floors, and the documents that change how a fold runs. It also judged whether this branch caused `survivor-check`'s drop from 15 standing-sentence reports to 7.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the #511 guard reads live lines of two ledger addresses; evidence-check reads every line of three, so a fenced or `_evidence.md` anchor is removed and reported BROKEN afterwards | `skills/settle/scripts/settle.py:459` | **fixed** `29390035` | fixed at 29390035 — (guard reads the checker's own address list, every line), a5acea6a (skill and policy prose, pinned), 2c74aad5 (ledger G3 row corrected and re-verified); executed: fenced row's directory removed, then `file not found` from evidence-check; `evidence_check.py:1207` scans the whole text; `evidence_check.py:919` lists the third address |
| 2 | 🟡 a memo row closed and its directory retired in one pull request passes `settle --retire` and fails `unverified_check` and `chain_check` at the merge base; the skill prescribes that order | `skills/settle/SKILL.md:94` | **fixed** `6f9ff718` | fixed at 6f9ff718 — the skill, `docs/the-evidence-ledger.md` and `RULE_KEPT_HEADING` say the closure merges in its own pull request before the one that retires the directory; pinned by `test_a_closed_row_is_told_to_merge_before_its_directory_goes`; executed: settle exit 0, then both readers exit 1; also `docs/the-evidence-ledger.md:184` and `RULE_KEPT_HEADING` |
| 3 | 🟡 a spec deleted in one merged pull request lets the next retire its directory with no marker, and every reader passes both pull requests | `skills/verify/scripts/unverified_check.py:1115` | **fixed** `c70c801d` | fixed at c70c801d — (`wrote_a_spec` asks history; `docs/review-chain-spec.md` rewritten), 100058fa (pins the git-failure direction); executed: the one-PR control is refused; PR 1 and PR 2 each exit 0 in all three readers; the claim at `docs/review-chain-spec.md:755` holds only inside one pull request |
| 4 | 🟡 `WORK_ITEM_DIR` matches any `*/specs/<x>/`, so a whole deletion under `docs/specs/` is dropped from the survivor range | `skills/code-review/scripts/survivor_check.py:522` | **fixed** `89d41871` | fixed at 89d41871 — `WORK_ITEM_DIR` anchored at the start; executed: `retired_directories` returned `docs/specs/login-flow`; `corrected()` measured 0 sentences |
| 5 | ⬜ the report lists an anchored spec-less directory under *`settle --retire` removes these* | `skills/settle/scripts/settle.py:614` | **fixed** `1160761c` | fixed at 1160761c — `survey` drops a directory the anchored guard holds from the rule-arm list; read: `survey["rule"]` is filled before `holding` is applied; `retire()` keeps it correctly |
| 🟢 | one predicate asked by four readers, not re-derived | `skills/verify/scripts/unverified_check.py:1090` | not a defect | read: each reader calls `retired_by_rule` on the loaded module |
| 🟢 | a partial removal or a memo removed from a directory that stays is still a deletion | `skills/verify/scripts/unverified_check.py:1384` | not a defect | read: both CI arms require the directory gone |
| 🟢 | the guard reads rows above the first marker and every fragment | `skills/settle/scripts/settle.py:435` | not a defect | read and executed (P1: two of three rows caught) |
| 🟢 | REMOVED and narrow wording matches `CLAUDE.md` and Q2's default | `skills/settle/scripts/settle.py:374` | not a defect | read |
| 🟢 | G8 floors moved to independent listings or `tmp_path` corpora, none lowered | `tests/conftest.py` | not a defect | read, the diff of every re-pointed case |
| 🟢 | no document still says a fold is a work item or that the ledger does not move | `skills/settle/SKILL.md:211` | not a defect | read, `git grep` outside `seal/specs/` and `CHANGELOG.md` |
| 🟢 | an absent `seal/specs/` under a present root is exit 0, and a mistyped path is still exit 2 | `skills/verify/scripts/unverified_check.py` | not a defect | executed |
| 🟢 | the A10 divergence: exit 1 for a hand removal of non-retirable directories | `seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/overview.md` | not a defect | read |
| 🟢 | `98e1183` committed with the old-roots module red, fixed at `bc7a869` | `tests/test_no_document_names_the_old_roots.py` | not a defect | executed, narrow: 1 failed at `98e1183`, 16 passed at `bc7a869` |
| 🟢 | the survivor drop from 15 to 7 is not this branch's code | `skills/code-review/scripts/survivor_check.py:641` | not a defect | executed: the base and head scripts agree on all three ranges; see Deferred |
| 🟢 | Windows path handling in the new comparisons | `skills/code-review/scripts/survivor_check.py:612` | not a defect | read only; execution unverified, answered by the Windows leg at this pull request |

## Paste-ready fixes

```python
    sources = []
    if os.path.isfile(under(root, LEDGER)):
        sources.append(LEDGER)
    for path in sorted(glob.glob(os.path.join(under(root, FRAGMENTS), "*.md"))):
        sources.append(f"{FRAGMENTS}/{os.path.basename(path)}")
    # evidence-check's third address, still read for a repository that never
    # moved it (`evidence_check.py#default_patterns`). A row there anchored
    # inside a retiring directory is BROKEN after the removal all the same.
    for path in sorted(
        glob.glob(os.path.join(root, "docs", "**", "_evidence.md"), recursive=True)
    ):
        sources.append(os.path.relpath(path, root).replace(os.sep, "/"))
    found = []
    for rel in sources:
        with open(under(root, rel), encoding="utf-8") as f:
            lines = f.read().split("\n")
        # Every line, fenced and commented ones included. evidence-check reads
        # an anchor wherever it stands (`check_text` scans the whole file), and
        # a guard that reads fewer lines than the checker keeps fewer
        # directories than the checker will report BROKEN. `live_lines` biases
        # an ambiguous line toward "not live", which keeps a directory for the
        # marker reader and would remove one here.
        for number, line in enumerate(lines, start=1):
```
```python
def test_a_fenced_anchor_still_keeps_the_directory(tree):  # NAME NOT IN TREE
    """evidence-check reads an anchor inside a fence as a coordinate like any
    other, so the guard has to as well: a fenced row's directory removed is a
    BROKEN row found after the fact, which is #511."""
    fold(tree, "1700000001-alpha")
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + f"\n```markdown\n{INSIDE_ROW}\n```\n",
        encoding="utf-8",
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text


def test_a_row_at_the_old_evidence_address_keeps_the_directory(tree):  # NAME NOT IN TREE
    fold(tree, "1700000001-alpha")
    old = tree / "docs" / "area" / "_evidence.md"
    old.parent.mkdir(parents=True)
    old.write_text(INSIDE_ROW + "\n", encoding="utf-8")
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text
    assert "docs/area/_evidence.md:1" in text, text
```
```markdown
**Close it in a pull request of its own, and let that one merge first.** The
CI readers ask the rule of the merge base, so a row closed and its directory
retired in one pull request is still open where they look, and
`unverified-check` and `chain-check` refuse the removal that `settle --retire`
just made. A row re-homed is closed the same way — ✅ naming where it went —
because a row deleted from `overview.md` is refused on any pull request. Once
the closure has merged, the next `settle --retire` takes the directory.
```
```python
RULE_KEPT_HEADING = (
    "kept by the rule — no `spec.md`, but the record still holds an open "
    "row, which\nleaves by being closed (✅ with what closed it) in a pull "
    "request merged before the\none that retires the directory, never with it:"
)
```
```python
def test_the_skill_says_a_closed_row_merges_before_its_directory_goes():  # NAME NOT IN TREE
    text = flat(skill())
    assert "merge first" in text, (
        "the skill lets a fold close a row and retire its directory in one "
        "pull request, which the CI readers refuse at the merge base"
    )
```
```python
def wrote_a_spec(root, ref, directory):  # NAME NOT IN TREE
    """Whether any commit reachable from `ref` (HEAD when None) touched
    `directory/spec.md` — D3 names a work item that WROTE no spec, which is a
    question about history, not about the tree the branch left. Asked of the
    merge base alone, a spec deleted by an earlier merge read as never written.
    """
    r = subprocess.run(
        ["git", "-C", root, "log", "-1", "--format=%H", ref or "HEAD", "--",
         f"{directory}/{SPEC}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode != 0 or bool(r.stdout.strip())
```
```python
    if f"{directory}/{SPEC}" in paths or wrote_a_spec(root, ref, directory):  # NAME NOT IN TREE
        return False
```
```markdown
the merge base rather than of the tree the branch left, and asked whether the
directory ever held one, a spec deleted in one commit — or in an earlier
pull request — and the directory in the next is still a deletion.
```
```python
def test_a_spec_deleted_by_an_earlier_merge_is_not_a_rule_retirement(repo):  # NAME NOT IN TREE
    item = "seal/specs/1787700001-a-spec"
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration())
    write(repo, f"{item}/spec.md", "# a spec\n\nA rule nobody folded.\n")
    commit(repo, "a work item that stated a rule")
    (repo / item / "spec.md").unlink()
    commit(repo, "an earlier pull request drops the spec")
    git(repo, "switch", "-q", "feature")
    git(repo, "merge", "-q", "base")
    shutil.rmtree(repo / item)
    commit(repo, "the directory, removed with no marker")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "retired: by the rule" not in out, out
```
```python
# A work item's directory, read off a path: the `seal/` root's `specs/`, or
# the legacy top-level `specs/` a repository from before 0.4.0 still carries.
# Anchored at the start, so `docs/specs/<name>/` is a directory of prose
# like any other and stays in the range.
WORK_ITEM_DIR = re.compile(r"^((?:seal/)?specs/[^/]+)/")
```
```python
def test_a_specs_directory_outside_the_seal_root_stays_in_the_range(tmp_path):  # NAME NOT IN TREE
    # Build with this module's fixture helpers: a base commit holding
    # docs/specs/login-flow/design.md, and a range that deletes the directory whole.
    ...
    assert survivor.retired_directories(root, a, b, ["docs/specs/login-flow/design.md"]) == set()
```

## Executed probes

| What was run | Result |
|---|---|
| fixture: three folded directories, anchored by a fenced row, a comment-line row and a row after a stray backtick; `settle --retire`, then `evidence-check .` | settle exit 1, fenced directory removed and the other two kept; evidence-check then reports that anchor `file not found` |
| this repository's ledger at 4d19cc0: `ANCHOR_RE` over every line vs `COORDINATE_RE` over live lines | 1938 and 1938; no non-live anchor under a `specs/` path |
| fixture: open memo row closed on the branch, then `settle --retire`, then the three readers against the base | settle exit 0; `unverified_check` exit 1; `chain_check` exit 1; `survivor_check` exit 0 |
| fixture: spec plus declaration plus closed memo; one-PR delete (control), then PR 1 deletes only `spec.md`, merged, then PR 2 runs `settle --retire` | control: `unverified_check` 1, `chain_check` 1; PR 1: all three exit 0; PR 2: settle removes by the rule, and all three exit 0 |
| fixture: range deletes `docs/specs/login-flow/` whole; `retired_directories` and `corrected()` | `{'docs/specs/login-flow'}`; 0 sentences measured |
| `survivor_check.py` from f8f1c9d and from 4d19cc0, over `f8f1c9d...e463a4c`, `f8f1c9d...4d19cc0`, and 4d19cc0 with `survivors.md` removed | 15 / 7 / 15 for both scripts, all exit 1 |
| head `survivor_check.py --range f8f1c9d...4d19cc0` with every `survivors.md` passed as `--exempt`, as `hygiene.yml` passes them | exit 0; 7 `exempt` lines printed |
| `unverified_check.py seal/specs/` under a present `seal/`, no `specs/`; then with a second mistyped path | exit 0 with the settled sentence; exit 2 *no such path* |
| `bin/test tests/test_no_document_names_the_old_roots.py` at `98e1183` and at `bc7a869` | 1 failed and 15 passed; 16 passed |
| `bin/settle` and `bin/evidence-check --strict .` on the clone at 4d19cc0 | settle exit 0 (8 to retire by the rule, 2 kept, 2 ungrouped); evidence-check exit 0 |
| the full suite, the repository-wide lint and the typecheck (the broad gate) | not yet — not run by this round, and not this agent's to run; the sealer's single run after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a committed `survivors.md` silences the survivors it quotes by subtraction in `survivor_check.py#wanted`, with no `exempt` line printed, with or without `--exempt`; mechanism present at f8f1c9d, so it predates this branch | not filed yet — `overview.md` §*Not done* hands it to the repository owner to file as an issue | the repository owner, who files the issue |
