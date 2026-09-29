# Round 1 report — 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated

| Field | Value |
|---|---|
| Round | 1 (first round, no earlier `round-N.md`) |
| Target | `fix/508-387-follow-up-names-are-checked-and-a-re-read-is-dated` at `ae2c6330` |
| Base | `release/v0.16.0` at `3911a8cf`; diff read as `git diff 3911a8cf...ae2c6330` |
| Reviewed by | specseal:warden, in a `git clone --no-local` at `<scratchpad>/1790635414/round-1/clone` |

## Summary

Four defects, all 🟡, and two paperwork corrections. Three of the four sit
exactly where the spawn prompt pointed:

- **A date written where no re-read happened** (🟡 1). A heal that only moves
  a file keeps its recorded hash. `--checked` still dates the row and prints
  that its hash moved.
- **A false `NOT-IN-TREE` on a legitimate reference** (🟡 2, 🟡 3). A
  cross-repo `path#name` in a parity repository is refused on the same run
  where the stamp half calls the same path `EXTERNAL`. A markdown heading
  fragment and a GitHub line anchor are read as unit names and refused.
- **A hash that does not move for an edit it should catch** (🟡 4). This
  branch moved `resolve_unit` onto `gfm_lines`. `.github/scripts/rider_check.py#region_lines`
  still slices the region out of the `splitlines` list, so the numbers and
  the list no longer agree.

Nothing found loses a record or crashes. Everything the account asserts that
I checked holds, except the three claims named under 🟡 1, 🟡 2 and 🟡 4.

## What the account asserted, and what the code does

| The account says | What I found |
|---|---|
| `overview.md`: the records arm reads `seal/follow-up.md` and leaves it out of the corpus | Holds. Executed: a follow-up row naming an absent compound name is exit 2 with the file named, and `check_records` over this tree returns 0 findings over 402 names |
| `spec.md` R6 and the docstring of `tests/test_a_row_points_by_content.py#test_a_healed_row_is_dated_under_checked_and_named_without`: "a re-anchor by identical content moves the hash" | True for a rename only. A file move reconstructs with the recorded hash, and the row is still dated (🟡 1, executed) |
| `spec.md` P4: an unresolved path is read "exactly as the bare backticked name would be" | Holds as written. It also makes the name half disagree with the stamp half about a cross-repo path, which `seal/releases/0.9.0.md` R5 and the comment above the `check_records` call in `main` both say must not happen (🟡 2, executed) |
| `phases/phase-5.md`: every hash-side split moved to `gfm_lines`, and `rider_check.py` is "B's files; not named by #664" | Inside the checker it holds: no `str.splitlines` call is left, only prose mentions (read, `grep`). Outside the checker, `rider_check.py` is coupled to `resolve_unit`'s numbering the way `round_record.py` is coupled to `readable`, and the table does not say so (🟡 4, ⬜ 6) |
| `--checked` writes into `Checked`, else `Date`, else the fourth cell of a five-cell headerless row | Holds (read: `date_column`, `dated_cell`, and the header walk in `ledger_table_rows`) |
| `fold_check`'s line count moved | Holds (read: `skills/settle/scripts/fold_check.py:424`) |
| A's O4 and 0.9.0's R1 were corrected | Holds (read: both rows in the diff now state what the code does) |
| The Korean README paragraph is native prose (put to the review chain) | It reads as native prose, and it says the same thing as the English paragraph (read) |

## Findings from execution

### 🟡 1 — A file move that keeps its hash is dated, and the run says its hash moved

`skills/evidence-check/scripts/evidence_check.py:2321` (the heal edit) and
`:2385` (the per-row grouping).

**What is wrong.** The heal path rewrites a BROKEN row only where one unit
reconstructs the recorded hash. When only the file moved and the unit name
stayed, the reconstructed region is the unit as it is. So the hash the heal
writes is the hash that was already there. The grouping loop then treats
every edit as a moved hash. Under `--checked`, it dates the row and prints
`dated … 1 row whose hash moved`. Without the flag, it names the row as one
that "took a new hash and kept its date".

**Why it matters.** The owner's answer to #387 was that only rows whose hash
moved are dated, and that an unmoved row is never touched. This row's hash
did not move. The date it receives claims a reading the tool itself proved
unnecessary, and the run's own output misstates what happened.
`skills/evidence-check/SKILL.md:306` states both halves at once ("a row
re-anchored by identical content is dated too, and a row whose hash did not
move is never touched"), and they contradict each other for this row. The
file-move repair is the flow `CONTRIBUTING.md:291` sends a contributor to
(*Renamed a cited symbol or file?*). Without the flag, that contributor is
now told the row carries an undated reading.

**Seen.** In a fixture, `src/old_home.py` was moved to `src/new_home.py`.
After `--reverify --checked 2026-09-28`, the row's date cell read
`2026-01-01 · 2026-09-28` and the recorded hash `f0658027` was unchanged.

The existing R6 case renames the function, which does move the hash, so
nothing in the suite covers this shape (coverage probe, read).

**Fix.** Carry whether each edit moved the hash, and date or name a row only
when one of its edits did. Also reword the SKILL.md sentence.

### 🟡 2 — In a parity repository, a cross-repo `path#name` is refused where its stamp is `EXTERNAL`

`skills/evidence-check/scripts/evidence_check.py:2928`
(`coordinate_misses`' unresolved branch).

**What is wrong.** The repository declares cross-repo intent (a
`seal/parity.md`), and the original checkout is absent, as it is in CI. A
record line that writes the original's function as `path#name` with no hash
now falls through to the bare-name rule and is refused. Its compound name is
not in this repository's corpus. On the same run, the same path written with
a hash is graded `EXTERNAL` at exit 0 by `check_text`, because that branch
checks `cross_repo_intent`.

**Why it matters.** This is the shape round 1's 🔴 1 of 0.9.0's work item
removed ("a migration repository's CI exited 2 on every run"). The comment
above the `check_records` call in `main` states the rule this breaks: an
anchor grades the same way in both arms. Before this branch the span was not
read at all. After it, a migration consumer who cites the original the way
`SKILL.md` documents cross-repo coordinates goes red at the upgrade. The
changelog names follow-up names and wrong-file names as the upgrade break,
not this.

**Seen.** In a fixture with `seal/parity.md` and no original checkout, line 1
(the name form) is `NOT-IN-TREE` and line 2 (the stamp form of the same path)
is `EXTERNAL`. The head exits 2 and the base exits 0.

**Fix.** Before the bare-name fallback, return "nothing read" under exactly
the condition `check_text` answers `EXTERNAL` for.

### 🟡 3 — A markdown heading fragment and a line anchor are read as unit names and refused

`skills/evidence-check/scripts/evidence_check.py:2924`
(`coordinate_misses`' resolved branch).

**What is wrong.** Take a record that points at a section the way GitHub
links one: a markdown path, then `#`, then a lower-cased one-word slug. The
path resolves, so the slug has to be a token of the file. The heading holds
the word capitalised, and the token set is case-sensitive, so the reference
is refused. A GitHub line anchor on a code path (`#L1`) is refused the same
way, with a message saying the line number "is not a token" of the file.

**Why it matters.** Neither span names a unit. P3 reads a one-word name
because "the path is what makes it a claim". That holds for a code unit and
not for a fragment, which is the commonest thing a person writes after `#`
in prose. The remedy the refusal offers, `NAME NOT IN TREE`, is wrong for
both, because the section and the line both exist. This repository's records
carry no such span (executed: 0 of every `RECORD_COORD_RE` match in
`seal/specs/`), so F8 stays green here and the defect reaches consumers only.

**Seen.** A record with both forms: head exit 2 with two `NOT-IN-TREE`
lines, base exit 0.

**Fix.** For a markdown path, also accept the lower-cased tokens. Do not read
a name made only of line anchors. The price: a real one-segment unit spelled
`L` plus digits is no longer checked.

### 🟡 4 — `rider_check.py` slices a region numbered on another list of lines

`.github/scripts/rider_check.py:344` (`region_lines`).

**What is wrong.** `region_lines` takes `(start, end)` from
`checker.resolve_unit`, which this branch moved to `gfm_lines`. It then
slices `text.splitlines()`. Above a form feed, NEL or U+2028 standing
mid-line, the two lists number lines differently, so the slice is one line
early for each such character. At the base, both sides used `splitlines`,
and the region was the unit.

**Why it matters.** A rider in a `.md`, `.yml`, `.sh` or other non-Python
file (`READABLE`) hashes the wrong lines. Its unit's last line falls outside
the hash, so an edit there passes without a DRIFTED. This is the direction
#664 exists to close, reopened one file over. `.py` riders are unchanged,
because `py_spans` already used `ast`'s numbering at the base. Today no
tracked file holds any of the eight characters, so no rider here is wrong
yet.

**Seen.** A heading-anchored rider region below a mid-line U+2028. At the
base, the region is `(4, 6)` and an edit to its last line moves the hash. At
the head, the region `(3, 5)` is sliced as the line above the heading
through the section's second line, and the same edit does not move the hash.

**Fix.** Slice the list `resolve_unit` numbered. `comment_blocks` takes the
same list, so the block numbers stay aligned.

## Findings from reading

### ⬜ 5 — Correction: the fragment's R1 row says a re-anchor by identical content is always dated

`seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md`,
row R1. The claim is true only once a heal moves the hash. When 🟡 1's fix
lands, the claim changes, and the row is corrected there. This is the run's
paperwork, so it is not counted in `Needs a fix`.

### ⬜ 6 — Correction: phase 5's enumeration misses a coupled reader

`seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-5.md`,
the row that lists `rider_check.py` among "B's files; not named by #664".
The table does record the coupled readers of `readable`. It does not record
that `region_lines` is coupled to `resolve_unit`, which this branch did move.
That is the fact 🟡 4 turns on. This is paperwork too.

## Regression tests to plant

Each case below is in the paste-ready blocks. Each is red at `ae2c6330` by
construction, because it pins the behaviour the finding measured. Show each
one red before committing it (§15). The fixture helpers the two records cases
call are placeholders for that file's own helpers, and are to be swapped for
them; the other two cases use helpers their files already carry.

- 🟡 1: `tests/test_a_row_points_by_content.py`, beside the R6 case.
- 🟡 2: `tests/test_a_record_states_what_the_tree_has.py`, beside the
  existing `EXTERNAL`-is-exit-0 case (the one asserting
  `0 refused · 0 drifted · 1 external`).
- 🟡 3: `tests/test_a_record_states_what_the_tree_has.py`, with the P cases.
- 🟡 4: `tests/test_a_rider_reaches_its_file.py`.

## Facts for the evidence ledger

These go in this work item's fragment after the fixes. None of them has a
hash yet.

- The heal path dates and names a row only where the hash it writes differs
  from the recorded one: the `reverify` unit of
  `skills/evidence-check/scripts/evidence_check.py`, and the 🟡 1 case.
- The name half of the records arm answers "not read" for a path the stamp
  half calls `EXTERNAL`: `coordinate_misses`, and the 🟡 2 case.
- `.github/scripts/rider_check.py#region_lines` slices `checker.gfm_lines`,
  the list `resolve_unit` numbers on, together with the 🟡 4 case.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A move-only heal keeps its recorded hash, and `--checked` still dates the row and prints that its hash moved. Without the flag the row is named as one that took a new hash | `skills/evidence-check/scripts/evidence_check.py:2321`, `:2385`; `skills/evidence-check/SKILL.md:306` | open | executed: fixture ledger row dated `2026-01-01 · 2026-09-28` with the recorded hash unchanged. The owner's answer dates only rows whose hash moved |
| 🟡 2 | In a parity repository with the original absent, a cross-repo `path#name` is `NOT-IN-TREE` while the same path's stamp is `EXTERNAL` | `skills/evidence-check/scripts/evidence_check.py:2928` | open | executed: head exit 2, base exit 0. Contradicts `seal/releases/0.9.0.md` R5 (`EXTERNAL` is exit 0 in the records arm) and the comment above the `check_records` call in `main` |
| 🟡 3 | A markdown heading fragment and a GitHub line anchor after a resolving path are refused as unit names | `skills/evidence-check/scripts/evidence_check.py:2924` | open | executed: head exit 2 with two `NOT-IN-TREE`, base exit 0. Both references exist, so the offered marker is false |
| 🟡 4 | `region_lines` slices `splitlines` with numbers `resolve_unit` now takes from `gfm_lines`, so a non-Python rider below a mid-line U+2028 hashes the wrong lines and an edit to the unit's last line passes | `.github/scripts/rider_check.py:344` | open | executed: region `(3, 5)` at head against `(4, 6)` at base, and the last-line edit moves no hash at head |
| ⬜ 5 | Correction: the fragment's R1 row claims every re-anchor by identical content is dated | `seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md` R1 | open | read. Corrected in place when 🟡 1's fix lands. Paperwork, not counted in `Needs a fix` |
| ⬜ 6 | Correction: phase 5's enumeration lists `rider_check.py` as not coupled, and it is coupled to `resolve_unit` | `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-5.md` | open | read. Paperwork, not counted in `Needs a fix` |
| 🟢 | The records arm reads `seal/follow-up.md` on every run and leaves it out of the corpus | `skills/evidence-check/scripts/evidence_check.py#check_records`, `#tree_names` | confirmed | executed: a follow-up row naming an absent compound name is exit 2 with no live work item. This tree's records arm returns 0 findings over 402 names |
| 🟢 | No `str.splitlines` call is left in the checker; the eleven hash-side sites read `gfm_lines` | `skills/evidence-check/scripts/evidence_check.py` | confirmed | read: `grep` finds the word only in two comments and one docstring |
| 🟢 | The date cell is `Checked`, else `Date`, else the fourth of five headerless cells, and escaped pipes do not move it | `skills/evidence-check/scripts/evidence_check.py#date_column`, `#dated_cell` | confirmed | read against `ledger_table_rows` and the vendored and shared `split_row`, which split on the same unescaped pipe |
| 🟢 | A's O4 and 0.9.0's R1 now state what the code does | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` O4, `seal/releases/0.9.0.md` R1 | confirmed | read |
| 🟢 | The Korean README paragraph is native prose and says what the English one says | `README.ko.md:167` | confirmed | read |
| ❓ | CI's Windows, Linux and macOS legs over the new cases, including the built coordinate of a follow-up refusal | the pull request | ❓ out of verified scope | not runnable in a round. The pull request's CI run answers it |

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

The fixtures, reconstructed so the next round can run them again:

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
text:  "# Doc\nalpha beta\n## Target\nline one\nline two\n## Next\nx\n"
call:  rider_check.region_lines(checker, "doc.md", '"## Target"', text)
edit:  "line two" -> "line two EDITED"; compare checker.content_hash of the two regions
```

## Paste-ready fixes

### 🟡 1 — date and name a row only where a hash moved

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

### 🟡 2 — the name half says nothing where the stamp half says EXTERNAL

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

### 🟡 3 — a markdown fragment and a line anchor are not unit names

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

### 🟡 4 — slice the list resolve_unit numbered

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
    text = "# Doc\nalpha beta\n## Target\nline one\nline two\n## Next\nx\n"
    edited = text.replace("line two", "line two EDITED")
    a, _ = riders.region_lines(CHECKER, "doc.md", '"## Target"', text)
    b, _ = riders.region_lines(CHECKER, "doc.md", '"## Target"', edited)
    assert a[0] == "## Target", a
    assert CHECKER.content_hash(a) != CHECKER.content_hash(b)
```

Needs a fix: yes — 🟡 1 (a move-only heal is dated as a re-read), 🟡 2 (a cross-repo name is refused where its stamp is EXTERNAL), 🟡 3 (a heading fragment or line anchor is refused as a name), 🟡 4 (`region_lines` slices a list `resolve_unit` no longer numbers)
Loses a record or crashes: no

## Proof block

Files opened in this round, at `ae2c6330` in the clone:

- `skills/evidence-check/scripts/evidence_check.py`: the whole diff, plus
  `gfm_lines`, `unquoted`, `normalise`, `content_hash`, `vendored_split_row`,
  `cell_rule`, `read`, `contained`, `place`, `cross_repo_intent`,
  `resolve_unit`, `content_matches`, `ledger_table_rows`, the `EXTERNAL`
  branch of `check_text`, `reverify` in full, `check_records`, and `main`'s
  writer and records sections
- `skills/settle/scripts/fold_check.py` (the diff)
- `skills/verify/scripts/unverified_check.py` (`split_row`)
- `.github/scripts/rider_check.py` (`RIDER_ROOTS`, `READABLE`,
  `load_checker`, `comment_blocks`' docstring, `region_lines`,
  `region_hash`, the `py_spans` site at line 574)
- `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/overview.md`,
  `spec.md`, `changelog.md`, `phases/phase-5.md`
- The diff of `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, `README.ko.md`,
  `agents/warden.md`, `docs/release-checklist.md`,
  `docs/the-evidence-ledger.md`, `seal/follow-up.md`,
  `skills/code-review/SKILL.md`, `skills/code-review/orchestration.md`,
  `skills/evidence-check/SKILL.md`, `skills/evidence-ci/SKILL.md`,
  `skills/implement/SKILL.md`, `skills/settle/SKILL.md`,
  `templates/evidence-check.yml`, `templates/ledger.md`,
  `seal/releases/0.9.0.md`, and
  `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md`
- `tests/test_a_row_points_by_content.py` (lines 1880–1935) and the R rows of
  this work item's ledger fragment

Not opened: `plan.md`, `questions.md`, `routing.md`, `phases/phase-1.md`
through `phase-4.md`, the diffs of the other `seal/releases/*.md` files, and
the new cases of `tests/test_a_record_states_what_the_tree_has.py`. Every
probe file, fixture and the extracted base checker under
`<scratchpad>/1790635414/round-1/` was deleted, and the clone was removed
after this report was written.
