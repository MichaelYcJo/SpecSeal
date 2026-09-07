# 1788761915-a-record-states-what-nothing-reads — review round 1

| Field | Value |
|---|---|
| Target SHA | d80469a0209495cde85a1a743aefa5e4ea49808c |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 214 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1 and 2 must be fixed; 3 through 12 are fix or justify, and 3, 5, 6 and 9 each rest on a sentence this branch ships as true |
| Loses a record or crashes | no |

- [ ] Pass

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
| 1 | 🔴 `main` drops `default_repo`, so the same anchor is `OK` in a ledger and `BROKEN` in a record, exit 2, with the cross-repo scan back on | `skills/evidence-check/scripts/evidence_check.py:2115` | open | executed: identical anchor, `1 ok` in the ledger arm and `BROKEN … 1 refused` in the records arm under `--default-repo`; passing the argument by hand returns `[]` |
| 2 | 🔴 `bound_line` carries the reopening walk only, prints `one reopening remains` at round 2 and the gate refuses the round 3 it invites | `skills/code-review/scripts/round_record.py:1056` | open | executed: three `new` runs — round 2 exit 0 with the line, round 3 exit 1 with `the count of round records after this one reaches 2` |
| 3 | 🟡 the corpus is `os.walk`, not `git ls-files`: an untracked or ignored file silences a refusal | `skills/evidence-check/scripts/evidence_check.py:1885` | open | executed: exit 2 to exit 0 after writing one untracked `scratch-notes.txt`; same for a `.gitignore`d `dist/bundle.js` |
| 4 | 🟡 local mode drops `seal/ledger.md` from the corpus, so identical bytes answer exit 0 shared and exit 2 local | `skills/evidence-check/scripts/evidence_check.py:97` | open | executed: two fixtures differing only in where `seal/` sits |
| 5 | 🟡 `EXTERNAL` in a record is exit 2 where a ledger's is exit 0, and `SKILL.md` documents exit 0 | `skills/evidence-check/scripts/evidence_check.py:2126` | open | executed in a `seal/parity.md` repository: `1 external` exit 0 from the ledger, `1 refused` exit 2 from the record |
| 6 | 🟡 the boundary is *has a fragment*, not *has not shipped*, and the arm never names what it skipped | `skills/evidence-check/scripts/evidence_check.py:1699` | open | executed: a live work item with no fragment reads `0 names read`, exit 0; 41 work item directories against 7 ids that ever had a fragment; this branch's own records unread through five of six phases |
| 7 | 🟡 three corpus guards have no observer while `phase-2.md` records eleven mutations all killed | `tests/test_a_record_states_what_the_tree_has.py` | open | executed: dropping `.git` from `SKIP_DIRS`, dropping `NAME_FILE_CAP`, and folding case each leave 33 passed; `UNREADABLE` has no case at all |
| 8 | 🟡 `bound_line` skips the gate's grandfathering and declares the run capped where the gate only notices | `skills/code-review/scripts/round_record.py:1017` | open | executed on `1788500000-an-item` and on a work item whose directory is not `<epoch>-<slug>` |
| 9 | 🟡 no document a checker's user reads mentions the arm; two `evidence-ci` sentences and the `--strict` template are now false | `skills/evidence-check/SKILL.md:230` | open | read: `NOT-IN-TREE` and `UNREADABLE` appear in no document; `evidence-ci/SKILL.md:56, :63`; `templates/evidence-check.yml:43` under `bash -e` |
| 10 | 🟡 `seal/ledger/.md` makes `item` empty and the whole `specs/` tree one live work item | `skills/evidence-check/scripts/evidence_check.py:1735` | open | executed: a shipped work item's record refused with that file present |
| 11 | 🟡 a fenced quotation and an HTML comment are read as claims, and `compound`'s docstring understates the class it gives up | `skills/evidence-check/scripts/evidence_check.py:1822` | open | executed: both refused; four of the 35 compound names in this tree are abbreviated case names the corpus cannot carry |
| 12 | 🟡 an unreadable record drops out of the fix walk, the permissive direction, against the unit's own docstring | `skills/code-review/scripts/round_record.py:1041` | open | executed at `chmod 000`: `one reopening remains` while `wrote_fixes` reads True; `fixes[0]` to `fixes[-1]` survives all six cases |
| 13 | ⬜ three statements in the PR body do not survive the code | PR #214 body | open | executed: the corpus is not `git ls-files`; it blocks in five places, not one; `6de1bca` exits 1 |
| 14 | ⬜ `SKIP_DIRS`' comment is false of `scan_candidates`, and `stamps_read` counts findings rather than stamps | `skills/evidence-check/scripts/evidence_check.py:95` | open | executed: a broken record stamp's hint read `same name at .venv/lib/site-packages/pkg/a.py` |

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
