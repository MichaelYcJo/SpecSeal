# 1788761915-a-record-states-what-nothing-reads — review round 1

| Field | Value |
|---|---|
| Target SHA | d80469a0209495cde85a1a743aefa5e4ea49808c |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 214 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | floor_and_fixes → round-1.md, bound_line, pytest |
| New units | unread_items (depth 1); claim_lines (depth 1); test_the_gathered_ledger_is_in_the_corpus_in_local_mode_too (depth 1); test_a_fenced_name_is_a_quotation_and_not_a_claim (depth 1); test_a_name_after_the_fence_closes_is_a_claim_again (depth 1); test_an_html_comment_is_an_aside_and_not_a_claim (depth 1); test_a_fenced_stamp_is_a_quotation_too (depth 1); test_a_work_item_with_no_fragment_is_counted_as_unread (depth 1); test_the_run_says_how_many_work_items_it_did_not_read (depth 1); test_a_fragment_named_only_md_is_not_a_work_item (depth 1); test_an_external_anchor_in_a_record_is_exit_0_as_it_is_in_a_ledger (depth 1); test_two_stamps_of_one_unit_on_one_line_are_two_stamps (depth 1); test_a_deleted_name_surviving_in_the_git_directory_is_not_a_name (depth 1); test_a_broken_stamps_hint_does_not_point_into_a_vendored_package (depth 1); test_a_file_over_the_size_cap_supplies_no_name (depth 1); test_the_corpus_does_not_fold_case (depth 1); test_a_record_that_cannot_be_read_is_named (depth 1); test_the_same_anchor_answers_the_same_in_both_arms_under_default_repo (depth 1); chain_of (depth 1); LATE (depth 1); test_two_quiet_rounds_after_the_floor_end_the_run (depth 1); test_a_round_that_reopened_without_writing_fixes_stops_the_count (depth 1); test_the_reopening_named_is_the_first_record_that_closed_on_a_fix (depth 1); test_a_work_item_older_than_the_count_rule_prints_nothing (depth 1); test_the_two_walks_are_grandfathered_against_different_constants (depth 1); test_a_work_item_with_no_epoch_in_its_name_prints_nothing (depth 1); test_an_unreadable_record_answers_nothing_rather_than_no_fix (depth 1) |
| Needs a fix | yes — findings 1 and 2 must be fixed; 3 through 12 are fix or justify, and 3, 5, 6 and 9 each rest on a sentence this branch ships as true |
| Loses a record or crashes | no |
<!-- New units: templates/evidence-check.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1, spawned against `d80469a` with the draft pull request open and nothing
to inherit.

**The prompt stated the bound rather than a round number, and said it was the
last time it would have to** — this branch is #207, which makes
`round_record.py new` print that same bound as it writes each record. It carried
the orchestrator's own re-execution of the seen-red pair in a clone, and two
corrections the build had already made to the orchestrator's handoff facts:
three stamps rather than two, and none in an unreleased work item, so the stamp
arm has cases and mutations behind it and no live occurrence.

Three facts were handed over with an instruction attached rather than as
findings. The build had measured **19 of 55 distinct names as false positives**
and narrowed the pattern to compound names — *re-derive that, because the arm's
precision rests on it*. It had found **two ways a work item could clear the
check on its own records** — its own ledger fragment, and the marker's worked
example in a skill, which put `chain_module` back into the corpus <!-- NAME NOT IN TREE --> — and the
prompt asked for a third. And it had run 36 mutations with one genuine
survivor, so the prompt asked the round to assume a second.

Five axes: every case the diff adds against what it guards; the boundary, asked
what happens to a work item with no fragment, one whose fragment is written
late, and one whose records exist before its fragment does; the corpus and what
its exclusions lose; #207's keying, with a chain constructed where earliest and
latest disagree; and the ledger read unscoped.

The round found the third way in, the second survivor and two more beside it,
and two of the five axes returned a 🔴.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `main` drops `default_repo`, so the same anchor is `OK` in a ledger and `BROKEN` in a record, exit 2, with the cross-repo scan back on | `skills/evidence-check/scripts/evidence_check.py:2115` | **fixed** `d5d25d9` | fixed at d5d25d9 — `` — both resolution arguments reach the records arm; the class was enumerated by signature, `check_records` has two optional arguments and one product call site; executed: identical anchor, `1 ok` in the ledger arm and `BROKEN … 1 refused` in the records arm under `--default-repo`; passing the argument by hand returns `[]` |
| 2 | 🔴 `bound_line` carries the reopening walk only, prints `one reopening remains` at round 2 and the gate refuses the round 3 it invites | `skills/code-review/scripts/round_record.py:1056` | **fixed** `94d1923` | fixed at 94d1923 — `` — `floor_and_fixes` carries the gate's count walk beside the reopening walk, and `bound_line` stops where the gate stops; executed: three `new` runs — round 2 exit 0 with the line, round 3 exit 1 with `the count of round records after this one reaches 2` |
| 3 | 🟡 the corpus is `os.walk`, not `git ls-files`: an untracked or ignored file silences a refusal | `skills/evidence-check/scripts/evidence_check.py:1885` | answered | The repair is `git ls-files`; `README.md` §*A row carries no line number and no commit* and `CLAUDE.md` make `--migrate` the checker's one call to git, and `test_the_checker_asks_git_for_nothing` holds it with a run under an empty `PATH` that a `subprocess` call would not survive. Written, measured against six cases, reverted at `7dac665`; the hole is documented in `tree_names` and `SKILL.md`, and `questions.md` Q1 puts the exception to the owner. It leans safe — CI reads a clean checkout, so CI is the stricter reader and only a local run is lenient |
| 4 | 🟡 local mode drops `seal/ledger.md` from the corpus, so identical bytes answer exit 0 shared and exit 2 local | `skills/evidence-check/scripts/evidence_check.py:97` | **fixed** `c6282e3` | fixed at c6282e3 — `` — the corpus reaches a local-mode `seal/` root; the class was enumerated over the three `SKIP_DIRS` walks and only `tree_names` builds the corpus; executed: two fixtures differing only in where `seal/` sits |
| 5 | 🟡 `EXTERNAL` in a record is exit 2 where a ledger's is exit 0, and `SKILL.md` documents exit 0 | `skills/evidence-check/scripts/evidence_check.py:2126` | **fixed** `7dac665` | fixed at 7dac665 — `` — `EXTERNAL` is exit 0 in both arms; executed in a `seal/parity.md` repository: `1 external` exit 0 from the ledger, `1 refused` exit 2 from the record |
| 6 | 🟡 the boundary is *has a fragment*, not *has not shipped*, and the arm never names what it skipped | `skills/evidence-check/scripts/evidence_check.py:1699` | **fixed** `7dac665` | fixed at 7dac665 — `` — `unread_items`, and the summary line carries the unread count; executed: a live work item with no fragment reads `0 names read`, exit 0; 41 work item directories against 7 ids that ever had a fragment; this branch's own records unread through five of six phases |
| 7 | 🟡 three corpus guards have no observer while `phase-2.md` records eleven mutations all killed | `tests/test_a_record_states_what_the_tree_has.py` | **fixed** `7dac665` | fixed at 7dac665 — `` — cases for the three unobserved corpus guards and for `UNREADABLE`; executed: dropping `.git` from `SKIP_DIRS`, dropping `NAME_FILE_CAP`, and folding case each leave 33 passed; `UNREADABLE` has no case at all |
| 8 | 🟡 `bound_line` skips the gate's grandfathering and declares the run capped where the gate only notices | `skills/code-review/scripts/round_record.py:1017` | **fixed** `94d1923` | fixed at 94d1923 — `` — grandfathering applied per walk, as the gate applies it; executed on `1788500000-an-item` and on a work item whose directory is not `<epoch>-<slug>` |
| 9 | 🟡 no document a checker's user reads mentions the arm; two `evidence-ci` sentences and the `--strict` template are now false | `skills/evidence-check/SKILL.md:230` | **fixed** `7dac665` | fixed at 7dac665 — `` — `evidence-check/SKILL.md`, the two `evidence-ci/SKILL.md` sentences and `templates/evidence-check.yml`; read: `NOT-IN-TREE` and `UNREADABLE` appear in no document; `evidence-ci/SKILL.md:56, :63`; `templates/evidence-check.yml:43` under `bash -e` |
| 10 | 🟡 `seal/ledger/.md` makes `item` empty and the whole `specs/` tree one live work item | `skills/evidence-check/scripts/evidence_check.py:1735` | **fixed** `7dac665` | fixed at 7dac665 — `` — an empty id is not a work item; the class was enumerated over `unshipped`, the one place a file name becomes an id; executed: a shipped work item's record refused with that file present |
| 11 | 🟡 a fenced quotation and an HTML comment are read as claims, and `compound`'s docstring understates the class it gives up | `skills/evidence-check/scripts/evidence_check.py:1822` | **fixed** `7dac665` | fixed at 7dac665 — `` — a fence and an HTML comment are quotations, not claims, and `compound`'s docstring names what it gives up; executed: both refused; four of the 35 compound names in this tree are abbreviated case names the corpus cannot carry |
| 12 | 🟡 an unreadable record drops out of the fix walk, the permissive direction, against the unit's own docstring | `skills/code-review/scripts/round_record.py:1041` | **fixed** `94d1923` | fixed at 94d1923 — `` — an unreadable record stops the walk rather than dropping out of it; executed at `chmod 000`: `one reopening remains` while `wrote_fixes` reads True; `fixes[0]` to `fixes[-1]` survives all six cases |
| 13 | ⬜ three statements in the PR body do not survive the code | PR #214 body | answered | Corrected in the PR #214 body itself, which is not a commit anybody can open — four edits: the corpus is not `git ls-files` and the hole and Q1 are named; the failure direction is five kinds of place with their exit codes; and the phase-3 commit that corrects the four lines is `0 refused` in the records arm while the run there exits 1 on three unrelated `seal/ledger.md` drifts — that claim appeared twice in the body and both were corrected. The body is not committed in this repository, so this row names the artifact rather than a SHA |
| 14 | ⬜ `SKIP_DIRS`' comment is false of `scan_candidates`, and `stamps_read` counts findings rather than stamps | `skills/evidence-check/scripts/evidence_check.py:95` | **fixed** `7dac665` | fixed at 7dac665 — `` — `SKIP_DIRS`' comment, and `stamps_read` counted from the line rather than from the findings; executed: a broken record stamp's hint read `same name at .venv/lib/site-packages/pkg/a.py` |

## Paste-ready fixes

```python
# 1 — skills/evidence-check/scripts/evidence_check.py:2115
    records, names_read, stamps_read = check_records(
        root, seal_home(root), maps, default_repo
    )
```
```python
# 2 — floor_and_fixes gains the gate's second walk. The reopening walk is
# keyed to the EARLIEST floor record and counts fix-closing records wherever
# they sit. The COUNT walk counts every later record up to and including the
# first that reopened (`Needs a fix: yes`) or closed on a fix, and the gate
# refuses at two — so a quiet verifying round leaves the NEXT record already
# over, whatever the reopening walk says.
def floor_and_fixes(reader, earlier):
    floor_at, fixes, counted, stopped = None, [], 0, False
    for _k, path in earlier:
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            # Not the floor record, and not a fix either: an unreadable record
            # dropped from `fixes` alone reads as a run that still has its
            # reopening. Say nothing rather than say that. (finding 12)
            return None, [], 0
        lines = reader.readable(text)
        if floor_at is None:
            cell_value = chain.field(chain.table_rows(reader, lines), chain.FLOOR)
            if cell_value is not None:
                word, _reason = chain.yes_or_no(reader.visible(cell_value).strip())
                if word == chain.FLOOR_NO:
                    floor_at = path
            continue
        wrote = chain.closed_with_a_fix(reader, lines, path)
        if wrote:
            fixes.append(path)
        if not stopped:
            counted += 1
            needs = chain.field(chain.table_rows(reader, lines), chain.NEEDS)
            reopened = needs is not None and (
                chain.yes_or_no(reader.visible(needs).strip())[0] == chain.FLOOR_YES
            )
            if reopened or wrote:
                stopped = True
    return floor_at, fixes, counted
```
```python
# 2, continued — in bound_line, after the grandfathering guard of fix 8
    if counted and not fixes:
        # Every record after the floor so far was quiet, so this one is the
        # gate's second counted record and the count walk already refuses it.
        return (
            f"round-record: {ENDS_THE_RUN} — {met} met the floor and the "
            f"{counted} record(s) after it neither reopened nor closed on a "
            "fix, so the gate's count of records after the floor reaches "
            f"{counted + 1} here. {chain.CAPPED_EXIT}"
        )
```
```python
# 3 — the corpus is what git carries
def tracked_paths(root):  # NAME NOT IN TREE — proposed here, not cited
    """The repository-relative paths git carries at `root`, or None where
    `root` is not a git tree.

    The corpus is what the TREE has, and an untracked file is not the tree.
    Measured: one untracked `scratch-notes.txt` containing `gone_helper` took
    a live refusal from exit 2 to exit 0, and a `.gitignore`d
    `dist/bundle.js` did the same. A reviewer's own `test_tmp_*` probe, a
    scratch note, and a dependency tree under a name `SKIP_DIRS` does not
    list all silence this arm without one committed byte — and CI, reading a
    clean checkout, then answers differently from the tree the record was
    written in.
    """
    r = subprocess.run(
        ["git", "-C", root, "ls-files", "-z", "--cached"],
        capture_output=True, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        return None
    return {p for p in r.stdout.split("\0") if p}
```
```python
# 3, continued — inside tree_names' existing loop, every other guard untouched
    tracked = tracked_paths(root)   # NAME NOT IN TREE — see above
    ...
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if tracked is not None and (
                os.path.relpath(path, root).replace(os.sep, "/") not in tracked
            ):
                continue
            names.update(TOKEN_RE.findall(filename))
```
```python
# 4 — walk the seal home explicitly, because `.git` is pruned and local mode
# puts `seal/ledger.md` under it. `names` is a set, so shared mode pays a few
# files and nothing else; `excluded` keeps `specs/` and `ledger/` out either way.
    for base in (root, home):
        for dirpath, dirnames, filenames in os.walk(base):
```
```python
# 5 — EXTERNAL is not a refusal in either arm
    drifted = sum(1 for status, _, _ in records if status == "DRIFTED")
    external = sum(1 for status, _, _ in records if status == "EXTERNAL")
    refused = len(records) - drifted - external
```
```python
# 6 — say what the boundary skipped
def unread_items(home):  # NAME NOT IN TREE — proposed here, not cited
    """Work item directories under `<home>/specs/` carrying no fragment.

    The boundary reads *a fragment exists* as *this work item has not
    shipped*, which is sound, and then acts on the converse, which is not.
    Measured over this repository: 41 work item directories, 7 ids that ever
    carried a fragment, 27 of the rest opened after the convention landed —
    and this arm's own work item was unread through five of its six phases.
    Naming them is not a refusal; it is `skipped_by_narrowing`'s rule one arm
    over: a checker that reads nothing says what it did not read.
    """
    live = unshipped(home)
    specs = os.path.join(home, SPECS_DIR)
    try:
        names = sorted(os.listdir(specs))
    except OSError:
        return []
    return [n for n in names if n not in live and os.path.isdir(os.path.join(specs, n))]
```
```python
# 8 — grandfather the printed line the way the gate does, at the top of
# bound_line once floor_at is known
    began = chain.item_began(floor_at.replace(os.sep, "/"))
    if began is None or began < chain.REOPEN_FROM:
        return None
```
```python
# 10 — an empty id is not a work item
        item = name[: -len(".md")]
        if not item:
            # `seal/ledger/.md` leaves `item` empty, `os.path.join(specs, "")`
            # is `specs/` itself and `isdir` is true — so the whole records
            # tree became one live work item and every shipped record was read.
            continue
```
```python
# 11 — a fence is a quotation, not a claim
def stated_names(lines):
    out, fenced = [], False
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or NOT_IN_TREE in line:
            continue
        for match in RECORD_NAME_RE.finditer(line):
            name = match.group(1)
            if compound(name):
                out.append((number, name))
    return out
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/evidence-check .` at `61ea096`, `--no-local` clone | exit 2 · `176 names read · 4 refused`, `chain_module` at `round-2.md:62` twice, `round-3.md:53`, `:58` <!-- NAME NOT IN TREE --> |
| the same at `6de1bca` | exit 1 · records arm `169 names read · 0 refused`; the 1 is three unrelated `seal/ledger.md` drifts |
| the same at `d80469a` | exit 0 · `760 ok` · records `207 names read · 0 stamps read · 0 refused` |
| `./bin/test` on four modules | 242 passed |
| corpus probe: untracked `scratch-notes.txt`, `.gitignore`d `dist/bundle.js` | exit 2 to exit 0 in both |
| boundary probe: live work item without then with a fragment | `0 names read` exit 0, then `NOT-IN-TREE` exit 2 |
| `--default-repo` probe, anchor resolving in the original checkout | ledger `1 ok`, record `BROKEN … file not found`, exit 2; passing the argument returns `[]` |
| `--default-repo` probe with a local look-alike | refusal reads `same name at app/mod.py (content differs)` |
| `seal/parity.md` probe, one cross-repo anchor in each file | ledger `1 external` exit 0 · record `EXTERNAL … 1 refused` exit 2 |
| local vs shared mode, identical bytes | exit 0 shared · exit 2 local |
| deleted-file probe: unit removed, present in history | still refused — the `.git` prune works on this path |
| narrowing re-derivation over the base with this branch's corpus and pattern | 533 occurrences · 182 distinct · 35 compound / 147 single-word; the 19 non-SHA single words are exactly the docstring's list |
| work item census over `seal/ledger/` history against `seal/specs/` | 41 directories · 7 ids that ever had a fragment · 27 of the remainder opened after the convention |
| eight mutations of the records arm against its 33 cases | `.git`, `NAME_FILE_CAP` and case-folding each leave 33 passed; `__pycache__`, `isdir`, `enumerate`, `refused = 0` each go red |
| fourteen mutations of `floor_and_fixes` / `bound_line` against the six new cases | 11 killed; `fixes[0]` to `fixes[-1]`, `except OSError` to `raise`, and dropping the post-floor `continue` survive |
| `round_record.py new` three times, floor `no` then two quiet rounds | round 2 exit 0 with `one reopening remains`; round 3 exit 1, `the count … reaches 2` |
| grandfathering probe on `1788500000-an-item` and on `seal/specs/my-work-item` | the gate notices; the line prints `this record ends the run … capped` |
| non-UTF-8 record probe | `bound_line` raises `UnicodeDecodeError` — **not reported**: `inherited_rows` already reads every earlier record the same way, so the class is pre-existing and this adds no reach |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
