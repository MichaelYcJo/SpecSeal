# 1790297085-settle-retires-a-directory-main-has-not-seen-closed — review round 1

| Field | Value |
|---|---|
| Target SHA | b589cf9164f9d3cf13e6fb8675df180d625e870f |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 605 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `32993c08dc67018f808d73dd1a44509478dbf339..9b5f7be9028c95184feb0a3221c76d89fed5a241`, 4 commits |
| Contract changes | report → report, main, round-2-report.md, round-3-report.md, pytest |
| New units | RULE_MOVED_HEADING (depth 1); NO_BASE_SAYS (depth 1); base_heading (depth 1); names_path (depth 1); test_the_path_is_found_as_a_windows_oserror_spells_it (depth 1); test_a_base_that_moved_past_the_fork_names_the_merge_that_moves_it (depth 1); test_the_report_refuses_a_survey_with_no_base (depth 1); test_a_shallow_clone_is_not_told_the_refs_share_no_commit (depth 1); test_each_sibling_is_refused_with_its_own_purpose (depth 1) |
| Needs a fix | yes — 🟡 1 (the heading printed when the base has moved past the fork says the CI readers ask there and gives a remedy that changes nothing) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item 1790297085 reviews the build at b589cf91 against spec.md and plan.md (frame ce4e96a8, approved 1880cf92). It covers three things: settle --retire asking the rule at the release's base (#602); the exit code of the four scripts that load a sibling by path (#590); and the gather refusing a fragment's own ## line (#586, the owner's option (a)). The classes are every revision settle could ask that CI does not, every loader copied alone, every line shape either release reader ends a section on, and every ledger row the build re-stamped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Once `--released-at` has moved past the fork carrying the closure, `settle` keeps the directory and prints that the CI readers ask at the fork point and that the closure must be merged to the release's branch; both are false, and the remedy that works (merge the ref into this branch) is never named | `skills/settle/scripts/settle.py#RULE_BASE_HEADING`, `#report`, `#retire`, `#main` | **fixed** `c5e06d2674fce8ca8b0064395c60f9a3eb2daab7` | fixed at c5e06d2674fce8ca8b0064395c60f9a3eb2daab7; Executed: a fixture where `main` holds the closure printed the heading, while `retired_by_rule` at `main`'s tip was True and the merge-ref merge base was `main`'s tip; CI checks out the merge ref (`.github/workflows/hygiene.yml`, no `ref:`) |
| ⬜ 2 | The changelog fragment, ledger M2, 0.14.0 D3's correction note and `plan.md`'s rejected-alternative row say CI asks at the fork point | `changelog.md` #602 entry; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2; `seal/releases/0.14.0.md` D3; `plan.md` §*Alternatives considered* | answered | corrected at 9b5f7be9028c95184feb0a3221c76d89fed5a241: the changelog fragment's #602 entry, ledger fragment M2, `seal/releases/0.14.0.md` D3's correction note, and plan.md's Alternatives rows; Paperwork correction, outside `Needs a fix`; the changelog sentence ships as `CHANGELOG.md` prose |
| ⬜ 3 | A shallow clone is told the two refs "share no commit" | `skills/settle/scripts/settle.py#main` | **fixed** `c5e06d2674fce8ca8b0064395c60f9a3eb2daab7` | fixed at c5e06d2674fce8ca8b0064395c60f9a3eb2daab7; Executed: a depth-1 clone of related history exited 2 with that sentence; `merge_base`'s docstring and `chain_check.py`'s refusal both name the shallow state |
| ⬜ 4 | `report` raises `KeyError` on a base-less survey that `retire` refuses at 2 | `skills/settle/scripts/settle.py#report` | **fixed** `c5e06d2674fce8ca8b0064395c60f9a3eb2daab7` | fixed at c5e06d2674fce8ca8b0064395c60f9a3eb2daab7; Read; no caller reaches it today |
| ⬜ 5 | Nothing pins the purpose `settle` gives `READER` and `CHECKER`; the renamed case inserts the phrase it then asserts | `tests/test_settle_reads_before_it_removes.py#test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback` | **fixed** `c5e06d2674fce8ca8b0064395c60f9a3eb2daab7` | fixed at c5e06d2674fce8ca8b0064395c60f9a3eb2daab7; Read; the class case reaches `OPTIN` only |
| ⬜ 6 | `skills/implement/scripts/seal.py` copied alone dies with a `ModuleNotFoundError` traceback at exit 1, and the spec's enumeration of loaders does not name it | `spec.md` §Scope *Out* | deferred #610 | #610 — becf6b124247a1e45ae9b6528ea42a404a57985f names `seal.py` in spec.md §Scope *Out* and points at #610; Executed; the enumeration's grep cannot see a `sys.path.insert` import. Paperwork correction; the orchestrator files or leaves the script |
| 🟢 | #590: three loaders refuse a missing sibling at 2 with a sentence naming the path and the purpose; the rider is discharged, and no sentence calling it open remains | `fold_check.py#load`, `settle.py#load`, `round_record.py#load` | confirmed | Read the three and their docstrings; the class case green in this round's run; S3 grep empty |
| 🟢 | #586: the gather refuses exactly the lines both release readers end a section on, among the fragments it would write, before anything is written or printed | `.github/scripts/gather_changelog.py#main`, `#section_lines` | confirmed | Read against `insert` and `publish_release_note.py#section_body`; module green in this round's run |
| 🟢 | The 14 ledger rows re-stamped in the range each still hold against the edit to their anchored unit | `seal/releases/0.12.2.md`, `0.13.0.md`, `0.14.0.md`, `0.15.0.md`, `0.15.1.md`, `0.15.3.md` | confirmed | Read each against its unit; `evidence-check` exit 0 on all seven files; D3's note is ⬜ 2 |

## Paste-ready fixes

```python
# beside RULE_BASE_HEADING
# #602, round 1: `--released-at` has moved past the fork. The CI readers ask
# at its tip (a pull request is checked out as the merge ref), and this asks
# at the fork, so a closure already merged there is not read here until the
# ref is merged into this branch.
RULE_MOVED_HEADING = (
    "kept until the closure reaches {base} — no `spec.md` and nothing open "
    "here, but\nthe record there still holds an open row. {ref} has moved past "
    "that commit: where\n{ref} already holds the closure, merge {ref} into this "
    "branch and run `settle`\nagain; otherwise merge the closure to {ref} "
    "first. The directory goes in a later\npull request:"
)


def base_heading(found):
    """The heading for a directory kept at the base, true of both label forms:
    the ref's own commit, where the CI readers ask too, or a fork the ref has
    moved past, where they do not."""
    if found.get("base_moved"):
        return RULE_MOVED_HEADING.format(base=found["base_label"], ref=found["ref"])
    return RULE_BASE_HEADING.format(base=found["base_label"])
```
```python
# survey: replace the two base lines of the dict
    ref_commit = reader.commit_of(root, ref)
    survey = {
        "base": base,
        "base_label": reader.base_label(ref, ref_commit, base),
        "base_moved": base != ref_commit,
        "ref": ref,
```
```python
# report
    if found["rule_base_kept"]:
        write(f"\n{base_heading(found)}\n")
        write_rule_kept(found["rule_base_kept"], out, base=found["base_label"])

# retire
    if base_kept:
        out.write(f"\n{base_heading(found)}\n")
        write_rule_kept(base_kept, out, base=label)
```
```python
    # #602: the rule arm asks its predicate of the merge base of the ref and
    # `HEAD`. The CI readers compute the same merge base from their own
    # `HEAD`, which on a pull request is the merge ref, so theirs is the
    # base's tip: the same commit while the base has not moved since the
    # fork, and a later one when it has, where this keeps more and never
    # less. Two histories that share no commit have none, and the predicate
    # asked of nothing would be asked of the working tree alone.
```
```python
# #602: nothing is open in the tree, and the base still holds a row open.
# `{base}` is `unverified_check.py#base_label`'s spelling of the merge base of
# `--released-at` and `HEAD`. It is the revision the CI readers ask at when
# the ref has not moved since the fork; `RULE_MOVED_HEADING` is the other case.
```
```python
def test_a_base_that_moved_past_the_fork_names_the_merge_that_moves_it(tree):
    """Round 1, 🟡 1. `main` took the closure after this branch forked, and
    this branch never merged it back. CI asks at `main`'s tip and would pass;
    `settle` asks at the fork and keeps the directory. That keeps more than
    it must, which is the safe direction, but the remedy it prints has to be
    the one that works: merge `main` in."""
    moment(tree, overview=OVERVIEW_OPEN)
    git(tree, "branch", "-M", "main")
    git(tree, "switch", "-qc", "work")
    ov = tree / "seal" / "specs" / MOMENT / "overview.md"
    ov.write_text(OVERVIEW_CLOSED, encoding="utf-8")
    git(tree, "add", "--", f"seal/specs/{MOMENT}")
    git(tree, "commit", "-qm", "close on work")
    git(tree, "switch", "-q", "main")
    ov.write_text(OVERVIEW_CLOSED, encoding="utf-8")
    git(tree, "add", "--", f"seal/specs/{MOMENT}")
    git(tree, "commit", "-qm", "hotfix: close on main")
    git(tree, "switch", "-q", "work")
    code, text = at(tree, "main", "--retire")
    assert (tree / "seal" / "specs" / MOMENT).exists(), text
    assert code == 1, text
    flat_text = " ".join(text.split())
    assert "merge main into this branch" in flat_text, text
    assert "the CI readers ask the rule there" not in flat_text, text
```
```python
    if found["base"] is None:
        sys.stderr.write(
            f"settle: --released-at {args.released_at} and HEAD share no commit "
            f"in {root}, or this clone is too shallow to reach the one they "
            "share (`git fetch --unshallow`) — nothing was read. The rule arm "
            "asks whether a record is closed at their merge base, and there is "
            "none to ask.\n"
        )
        return 2
```
```python
@pytest.mark.parametrize(
    "which, phrase",
    [
        ("READER", "it is where the fold record is read from"),
        ("CHECKER", "it is what resolves a ledger row's anchor"),
        ("OPTIN", "it is what finds the repository's seal/ root"),
    ],
)
def test_each_sibling_is_refused_with_its_own_purpose(which, phrase, monkeypatch, capsys):
    """#590's second half, per file: the table entry for each real sibling,
    not an entry the case put there itself."""
    path = getattr(settle, which)
    real = os.path.isfile
    monkeypatch.setattr(os.path, "isfile", lambda p: False if p == path else real(p))
    with pytest.raises(SystemExit) as raised:
        settle.load(path, "absent")
    assert raised.value.code == 2
    assert phrase in capsys.readouterr().err
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test` on `tests/test_a_script_copied_alone_exits_2.py`, `tests/test_settle_reads_before_it_removes.py`, `tests/test_the_changelog_is_gathered_at_release.py` and `tests/test_a_folded_statement_names_what_enforces_it.py`, in this round's clone at b589cf91 | exit 0, 189 passed |
| Probe (one file, run once, deleted): moved base. `main` closes the row after the fork, the branch closes it too, `settle.retire` with `--released-at main` | exit 1, kept under "kept until the closure reaches the merge-base of main and HEAD (84610db)" with "the CI readers ask the rule there"; `retired_by_rule` at `main`'s tip True; merge base of `main` and a merge of the branch into `main` equals `main`'s tip |
| Same probe file: a `--depth 1 --no-single-branch` clone of related history, `settle.main --released-at origin/main` | exit 2, "share no commit" |
| `skills/implement/scripts/seal.py` copied alone to an empty directory, `python3 seal.py mode` | exit 1, `ModuleNotFoundError: No module named 'config'` traceback |
| `./bin/evidence-check --ledger <file> .` on the fragment and the six edited `seal/releases/*.md` | exit 0 on each, 0 drifted, 0 broken |
| The broad gate: the full suite, lint and typecheck | not yet. That run belongs to the sealer, once, after the rounds settle; this round ran four modules only |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
