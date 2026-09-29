# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — review round 1

| Field | Value |
|---|---|
| Target SHA | ae2c6330d1064ad592140b4cdff80a05af8c1efe |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #668 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `0cfbcb55da0f61be5e097859a3b2602f63f468bf..42cd6435fd5d141a75b9e58d34c29e0d1d82c4f8`, 2 commits |
| Contract changes | none |
| New units | LINE_ANCHOR_RE (depth 1); test_a_cross_repo_name_is_not_read_where_its_stamp_is_external (depth 1); test_a_heading_fragment_and_a_line_anchor_are_not_refused (depth 1); test_a_rider_region_below_a_line_separator_is_the_unit (depth 1); test_a_file_moved_whole_is_re_pointed_and_neither_dated_nor_named (depth 1) |
| Needs a fix | yes — 🟡 1 (a move-only heal is dated as a re-read), 🟡 2 (a cross-repo name is refused where its stamp is EXTERNAL), 🟡 3 (a heading fragment or line anchor is refused as a name), 🟡 4 (`region_lines` slices a list `resolve_unit` no longer numbers) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first finding round, over the work item's own diff `3911a8cf...ae2c6330`. Asked to review the records arm reading `seal/follow-up.md` and `path#name`, `--reverify --checked` against the owner's pre-edit answer, and the hash side's move to `gfm_lines`, with a false `NOT-IN-TREE`, a date written where no re-read happened, and a hash that moves or misses wrongly named as where a defect would leave the root.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A move-only heal keeps its recorded hash, and `--checked` still dates the row and prints that its hash moved. Without the flag the row is named as one that took a new hash | `skills/evidence-check/scripts/evidence_check.py:2321`, `:2385`; `skills/evidence-check/SKILL.md:306` | **fixed** `671f4e64` | fixed at 671f4e64 — each reverify edit records whether it moved the hash; a row whose edits moved none is re-pointed, neither dated nor named; executed: fixture ledger row dated `2026-01-01 · 2026-09-28` with the recorded hash unchanged. The owner's answer dates only rows whose hash moved |
| 🟡 2 | In a parity repository with the original absent, a cross-repo `path#name` is `NOT-IN-TREE` while the same path's stamp is `EXTERNAL` | `skills/evidence-check/scripts/evidence_check.py:2928` | **fixed** `671f4e64` | fixed at 671f4e64 — `coordinate_misses` leaves a name unread under exactly the condition `check_text` answers `EXTERNAL`; executed: head exit 2, base exit 0. Contradicts `seal/releases/0.9.0.md` R5 (`EXTERNAL` is exit 0 in the records arm) and the comment above the `check_records` call in `main` |
| 🟡 3 | A markdown heading fragment and a GitHub line anchor after a resolving path are refused as unit names | `skills/evidence-check/scripts/evidence_check.py:2924` | **fixed** `671f4e64` | fixed at 671f4e64 — a fragment after a `.md` path is also matched against the file's lower-cased tokens, and a `#L<n>` line anchor is not read; executed: head exit 2 with two `NOT-IN-TREE`, base exit 0. Both references exist, so the offered marker is false |
| 🟡 4 | `region_lines` slices `splitlines` with numbers `resolve_unit` now takes from `gfm_lines`, so a non-Python rider below a mid-line U+2028 hashes the wrong lines and an edit to the unit's last line passes | `.github/scripts/rider_check.py:344` | **fixed** `671f4e64` | fixed at 671f4e64 — `rider_check.py#region_lines` slices `gfm_lines`, the numbering `resolve_unit` uses; executed: region `(3, 5)` at head against `(4, 6)` at base, and the last-line edit moves no hash at head |
| ⬜ 5 | Correction: the fragment's R1 row claims every re-anchor by identical content is dated | `seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md` R1 | answered | corrected at `42cd6435`: the fragment's R1 claim; read. Corrected in place when 🟡 1's fix lands. Paperwork, not counted in `Needs a fix` |
| ⬜ 6 | Correction: phase 5's enumeration lists `rider_check.py` as not coupled, and it is coupled to `resolve_unit` | `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-5.md` | answered | corrected at `42cd6435`: `phases/phase-5.md`'s row for `rider_check.py#region_lines`; read. Paperwork, not counted in `Needs a fix` |
| 🟢 | The records arm reads `seal/follow-up.md` on every run and leaves it out of the corpus | `skills/evidence-check/scripts/evidence_check.py#check_records`, `#tree_names` | confirmed | executed: a follow-up row naming an absent compound name is exit 2 with no live work item. This tree's records arm returns 0 findings over 402 names |
| 🟢 | No `str.splitlines` call is left in the checker; the eleven hash-side sites read `gfm_lines` | `skills/evidence-check/scripts/evidence_check.py` | confirmed | read: `grep` finds the word only in two comments and one docstring |
| 🟢 | The date cell is `Checked`, else `Date`, else the fourth of five headerless cells, and escaped pipes do not move it | `skills/evidence-check/scripts/evidence_check.py#date_column`, `#dated_cell` | confirmed | read against `ledger_table_rows` and the vendored and shared `split_row`, which split on the same unescaped pipe |
| 🟢 | A's O4 and 0.9.0's R1 now state what the code does | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` O4, `seal/releases/0.9.0.md` R1 | confirmed | read |
| 🟢 | The Korean README paragraph is native prose and says what the English one says | `README.ko.md:167` | confirmed | read |
| ❓ | CI's Windows, Linux and macOS legs over the new cases, including the built coordinate of a follow-up refusal | the pull request | ❓ out of verified scope | not runnable in a round. The pull request's CI run answers it |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, reverify(): the heal branch
                    new_hash = content_hash(gfm_lines(target)[a - 1 : b])
                    edits.append(
                        (
                            m.start("path"),
                            m.end("hash"),
                            new_raw
                            + text[m.end("path") : m.start("locator")]
                            + name
                            + text[m.end("locator") : m.start("hash")]
                            + new_hash,
                            f"  {raw_path}#{locator} -> {shown}  (identical content)",
                            # A move reconstructs with the recorded hash, so
                            # only a rename moves it (#387: the rule is the hash).
                            new_hash != m.group("hash"),
                        )
                    )

# the re-stamp branch: the hash moved by construction
            edits.append(
                (
                    m.start("hash"),
                    m.end("hash"),
                    got,
                    f"  {shown}  {m.group('hash')} -> {got}",
                    True,
                )
            )

# the per-row loop
        for number, row_edits in sorted(by_row.items()):
            header, cells = rows.get(number, (None, []))
            spliced = [edit[:4] for edit in row_edits]
            if not any(edit[4] for edit in row_edits):
                # Re-pointed, and no hash moved: there is no reading to date
                # and no undated reading to name.
                kept.extend(spliced)
                continue
            column = date_column(header, cells) if cells else None
            where = f"{name}:{number}"
            if checked is not None:
                if column is None:
                    undatable.append(where)
                    continue
                cell = dated_cell(lines[number - 1], column[0], checked)
                if cell is not None:
                    at = starts[number - 1]
                    kept.append((at + cell[0], at + cell[1], cell[2], None))
                dated.append((where, row_label(cells)))
            else:
                undated.append(
                    (
                        where,
                        row_label(cells),
                        f"{column[1]}: {cells[column[0]] or '(empty)'}"
                        if column
                        else "no date cell",
                    )
                )
            kept.extend(spliced)
```
```text
skills/evidence-check/SKILL.md:305-306, the sentence replaced:

cell, and nothing where the cell already ends in it. A row is dated once
however many of its coordinates moved. A rename heal moves the hash, so it is
dated too; a moved file whose unit reconstructs with the recorded hash is
re-pointed and neither dated nor named, and a row whose hash did not move is
never touched.
```
```python
# tests/test_a_row_points_by_content.py, beside the R6 case
def test_a_moved_file_whose_hash_did_not_move_is_neither_dated_nor_named(repo):
    """#387: the owner's rule dates a row whose HASH moved. A whole-file move
    reconstructs with the recorded hash, so the row is re-pointed, its date is
    byte-identical, and neither block names it."""
    row = f"| C1 | `{anchor(repo, 'handler')}` | read | 2026-09-01 | n |\n"
    for args in (["--reverify", "--checked", READ_ON, "."], ["--reverify", "."]):
        ledger = ledger_of(repo, row)
        (repo / "src" / "service.py").rename(repo / "src" / "moved.py")
        r = run(args, str(repo))
        assert "(identical content)" in r.stdout, r.stdout
        assert "| 2026-09-01 | n |" in ledger.read_text(), ledger.read_text()
        assert "dated" not in r.stdout and "kept its date" not in r.stdout, r.stdout
        (repo / "src" / "moved.py").rename(repo / "src" / "service.py")
```
```python
# skills/evidence-check/scripts/evidence_check.py, coordinate_misses()
    if tokens is not None:
        return True, [s for s in segments if s not in tokens], True
    if (
        repo == root
        and cross_repo_intent(root, default_repo)
        and "/" in rel
        and not os.path.exists(os.path.join(root, rel.split("/")[0]))
    ):
        # `check_text` grades this path EXTERNAL at exit 0: the repository
        # declared another checkout and this run has not got it. The name
        # half of the same arm must not refuse what the stamp half calls
        # somebody else's (0.9.0's R5; round 1 of 1790635414).
        return False, [], False
    claimed = [s for s in segments if compound(s)]
    return bool(claimed), [s for s in claimed if s not in known], False
```
```python
# tests/test_a_record_states_what_the_tree_has.py, beside the EXTERNAL case
def test_a_cross_repo_name_in_a_parity_repository_is_not_refused(tmp_path):
    """The name half grades a cross-repo path the way the stamp half does: a
    repository with a parity config and no original checkout is exit 0."""
    root = live_repo(tmp_path)  # the file's own live-work-item fixture helper
    (root / "seal" / "parity.md").write_text("# parity\n")
    record(root, "Ports `legacy/src/service.py#get_user_by_id`.\n")
    got = run_check(root)
    assert got.returncode == 0, got.stdout
    assert "NOT-IN-TREE" not in got.stdout, got.stdout
```
```python
# skills/evidence-check/scripts/evidence_check.py, beside RECORD_COORD_RE
# A GitHub line anchor (`#L120`) locates a line, not a unit, so a name made of
# nothing else is not read.
LINE_ANCHOR_RE = re.compile(r"L[0-9]+")

# coordinate_misses(), the resolved branch
    if repo is not None:
        full = os.path.join(repo, rel)
        if full not in file_tokens:
            body = read(full)
            found = None if body is None else set(TOKEN_RE.findall(body))
            if found is not None and rel.endswith(".md"):
                # After a markdown path the fragment is GitHub's heading
                # anchor, which lower-cases the heading's words.
                found |= {t.lower() for t in found}
            file_tokens[full] = found
        tokens = file_tokens[full]
    if tokens is not None:
        if all(LINE_ANCHOR_RE.fullmatch(s) for s in segments):
            return False, [], True
        return True, [s for s in segments if s not in tokens], True
```
```python
# tests/test_a_record_states_what_the_tree_has.py, with the P cases
def test_a_heading_fragment_and_a_line_anchor_are_not_refused(tmp_path):
    root = live_repo(tmp_path)
    (root / "README.md").write_text("# Tool\n\n## Install\n\nRun it.\n")
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "app.py").write_text("def main():\n    return 0\n")
    record(root, "Setup is in `README.md#install`, entry at `src/app.py#L1`.\n")
    got = run_check(root)
    assert got.returncode == 0, got.stdout
    assert "NOT-IN-TREE" not in got.stdout, got.stdout
```
```python
# .github/scripts/rider_check.py, region_lines()
    start, end = places[0]
    # The lines `resolve_unit` numbered its answer on (#664). `splitlines`
    # also ends a line at a form feed, NEL or U+2028, so its list put the
    # region one line early per such character above it, and an edit to the
    # unit's last line passed.
    lines = checker.gfm_lines(text)
    blocks = comment_blocks(lines, rel)
```
```python
# tests/test_a_rider_reaches_its_file.py
def test_a_rider_region_below_a_line_separator_is_the_unit():
    """#664 one file over: the region is sliced from the list `resolve_unit`
    numbered, so an edit to the unit's last line moves the hash."""
    text = "# Doc\nalpha
beta\n## Target\nline one\nline two\n## Next\nx\n"
    edited = text.replace("line two", "line two EDITED")
    a, _ = riders.region_lines(CHECKER, "doc.md", '"## Target"', text)
    b, _ = riders.region_lines(CHECKER, "doc.md", '"## Target"', edited)
    assert a[0] == "## Target", a
    assert CHECKER.content_hash(a) != CHECKER.content_hash(b)
```

## Executed probes

| What was run | Result |
|---|---|
| Move-only heal: a fixture repository whose ledger row cites a unit in a file that was then moved, `--reverify --checked 2026-09-28` | exit 0. The row was re-pointed, its hash stayed `f0658027`, and its date cell became `2026-01-01 · 2026-09-28`. Printed `dated 2026-09-28 — 1 row whose hash moved` |
| The same fixture, `--reverify` without the flag | exit 0. Printed `1 row took a new hash and kept its date` for a row whose hash did not change |
| A live record carrying a markdown heading fragment and a GitHub line anchor, head checker and base checker | head exit 2, two `NOT-IN-TREE`; base exit 0 |
| A parity repository (`seal/parity.md`, no original checkout) whose record writes one cross-repo name without a hash and one with a hash | head exit 2: the name `NOT-IN-TREE`, the stamp `EXTERNAL`; base exit 0 with the stamp `EXTERNAL` |
| `rider_check.region_lines` over a markdown text with a mid-line U+2028 above a `"## Target"` section, with the base checker and the head checker | base region `(4, 6)`, and an edit to its last line moves the hash; head region `(3, 5)` sliced one line early, and the same edit does not move the hash |
| A follow-up row proposing a compound name nothing carries, no live work item | exit 2, `NOT-IN-TREE` at `seal/follow-up.md:3`, summary ends `seal/follow-up.md read`. Intended, and the changelog's *Changed* entry says so |
| `check_records` over the clone at `ae2c6330`, and a count of `RECORD_COORD_RE` matches in `seal/specs/` with a `.md` path or a line-anchor name | 0 findings, 402 names read, 0 stamps. 0 such spans |
| The work item's test modules (`tests/test_a_row_points_by_content.py`, `tests/test_a_record_states_what_the_tree_has.py`, `tests/test_a_document_has_room_for_the_next_fold.py`) | not run in this round. The smith's account labels them executed, and this round's findings rest on the probes above |
| The broad gate — the full suite, the repository-wide lint and the typecheck over this branch | not yet. It is the sealer's, once the rounds settle, and it is not due: this report leaves four findings open |

```text
# 🟡 1
src/new_home.py:   def helper_one(): return 1          (moved from src/old_home.py)
seal/ledger.md:    | C1 | `src/old_home.py#helper_one@f0658027` | returns one | 2026-01-01 | |
run:               evidence_check.py --reverify --checked 2026-09-28 <root>

# 🟡 3
README.md:         # Tool / ## Install / Run the installer.
seal/specs/1700000000-probe/plan.md:
                   Setup is in `README.md#install`.
                   The entry point is `src/app.py#L1`.
seal/ledger/1700000000-probe.md: (empty, so the work item is live)

# 🟡 2
seal/parity.md:    # parity
seal/specs/1700000000-probe/plan.md:
                   Ports `legacy/src/service.py#get_user_by_id`.
                   Stamped `legacy/src/service.py#get_user_by_id@abcdef12`.

# 🟡 4
text:  "# Doc\nalpha
beta\n## Target\nline one\nline two\n## Next\nx\n"
call:  rider_check.region_lines(checker, "doc.md", '"## Target"', text)
edit:  "line two" -> "line two EDITED"; compare checker.content_hash of the two regions
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
