# 1790635413-every-markdown-reader-shares-one-fence-rule — review round 1

| Field | Value |
|---|---|
| Target SHA | 68bcb224819609a77d1601f4bba2fee80e293cfd |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #663 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `1d3eb8a5cdf36c3f4fc03cfc288f5f20619cd363..a06f23b2094ae4319d6d91764550540d9e27dfd1`, 5 commits |
| Contract changes | commented → table_lines, commented_row_at |
| New units | test_a_fence_line_inside_a_rider_body_hides_no_rider_below (depth 1); QUOTED_DELIMITERS (depth 1); test_delimiters_quoted_in_code_spans_either_side_hide_the_table (depth 1) |
| Needs a fix | yes — 🟡 1 and 🟡 2 (the release scripts write markers their own readers cannot see), 🟡 3 (the config reader hides a live table and three sentences promise it cannot), 🟡 4 (the rider check hides riders below a fence line inside a comment) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first finding round, over the whole branch `551c7967...68bcb224`. Asked to review nine readers moved onto the shared fence rule, the config reader's new closed-comment rule, and the user-visible change that a row standing only inside a closed HTML comment in `seal/config.md` stops being read, with the config reader (every Bash call) and the release scripts' counts named as where a defect would leave the root.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A changelog fragment that leaves a fence or a comment open hides the markers the gather writes below it. `--check` then calls a gathered entry missing, and the gather it advises writes the entry twice | `.github/scripts/gather_changelog.py:102` | deferred phase 9 of this branch | phase 9 of this branch — Closing it needs a new refusal in the gather, which a fix pass may not add. The owner's standing answer this run is to fix a defect in the branch where it arose, not file it, so `questions.md` Q5 is answered (a) and it is built as phase 9; Executed: gather 0, `--check` 1 naming B, regather 0, B's entry twice in the file |
| 🟡 2 | A ledger fragment that leaves a fence open hides the markers folded below it. `--check` passes with a wrong count, and `is_marked` cannot see the fold | `.github/scripts/fold_ledger.py:216` | deferred phase 9 of this branch | phase 9 of this branch — The same class in `fold_ledger.py`, in the same phase; Executed: fold 0, two markers written, one live, `--check` 0 printing 1 |
| 🟡 3 | A comment opener and a closer quoted in code spans on either side of the live config table hide that table. The live row is then called commented out, and three shipped sentences promise this cannot happen | `hooks/config.py:232` | **fixed** `5ff35cd2` | fixed at 5ff35cd2 — the reading is kept and the three sentences that denied it now state the shape; Executed: `config_rows` `[]`, `declared_mode` none, `broad-gate` gives the commented-out refusal quoting the live row |
| 🟡 4 | The rider check's fence spans ignore comment state, so a fence line inside a rider's body hides every rider below it | `.github/scripts/rider_check.py:210` | **fixed** `710e3716` | fixed at 710e3716 — `e7318ff9`, `3375a4ef`; Executed: old reader 2 blocks, branch 1. None in today's tree |
| ⬜ 5 | `table_lines` walks `fence_map` twice on every Bash call | `hooks/config.py:281` | **fixed** `5ff35cd2` | fixed at 5ff35cd2; Read |
| 🟢 | The marker readers change no current count | `CHANGELOG.md`, `seal/ledger.md`, `seal/releases/*.md` | confirmed | Executed: 140/140 and 125/125 |
| 🟢 | The rider reader changes no current block | `.github/scripts/rider_check.py:226` | confirmed | Executed: 0 files differ between the base and the branch |
| 🟢 | S13's case fails without the comment half | `hooks/config.py:281` | confirmed | Executed: the swap back to `unfenced` reads the parked row alone |
| ❓ | The ledger fragment's rows, and the re-read and corrected notes across `seal/releases/*.md`, were not run through `evidence-check` | `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | ❓ out of verified scope | A plugin check the broad gate runs. The sealer answers it |
| ❓ | The new cases on the Windows and Linux legs | `tests/test_a_script_copied_alone_exits_2.py` | ❓ out of verified scope | Only macOS ran here. CI's test matrix at the pull request answers it |

## Paste-ready fixes

```python
def leaves_open(body):
    """Whether a marker written below BODY would stand on no live line: the
    fragment opens a fenced block or an HTML comment and never closes it
    (#584). `section` writes the next fragment's marker below it, and
    `insert` puts every older section's below that, so `ungathered` would
    call each of them missing and a second gather would write them twice."""
    probe = [*body.splitlines(), "", marker("probe")]
    return not list(reader.live_lines(probe))[-1][1]
```
```python
    unclosed = [work_item_id for work_item_id, body in missing if leaves_open(body)]
    if unclosed:
        print(
            "changelog fragments that open a fenced block or an HTML comment "
            "and never close it, so every marker written below them would "
            "read as not gathered:"
        )
        for work_item_id in unclosed:
            print(f"  seal/specs/{work_item_id}/changelog.md")
        print(
            "\nClose it in the fragment in a pull request into the release "
            "branch, then gather again. Nothing was written."
        )
        return 1
```
```python
@pytest.mark.parametrize(
    "body",
    ["- A\n\n```\nquoted, never closed", "- A mentions a " + "<" + "!--" + " in prose"],
    ids=["fence", "comment"],
)
def test_a_fragment_that_leaves_a_block_open_is_refused(tmp_path, body):
    """#584 round 1, finding 1. The gather wrote a marker its own reader
    then called ungathered, and the gather `--check` advised wrote the entry
    a second time."""
    spec = importlib.util.spec_from_file_location("specseal_gather_r1f1", SCRIPT)
    gather = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gather)
    before = (
        "# Changelog\n\n## 0.1.0 — 2026-01-01\n\n"
        + gather.marker("100-old")
        + "\n- old\n"
    )
    (tmp_path / "CHANGELOG.md").write_text(before, encoding="utf-8")
    for work_item_id, text in [("200-a", body), ("300-b", "- B")]:
        d = tmp_path / "seal" / "specs" / work_item_id
        d.mkdir(parents=True)
        (d / "changelog.md").write_text(text + "\n", encoding="utf-8")
    assert gather.main(["--version", "0.2.0", "--root", str(tmp_path)]) == 1
    assert (tmp_path / "CHANGELOG.md").read_text(encoding="utf-8") == before
```
```python
def leaves_open(text):
    """Whether a marker folded below TEXT would stand on no live line: the
    fragment opens a fenced block or an HTML comment and never closes it
    (#584). `section` folds the next fragment's marker below it, so
    `is_marked`, `doubled_markers` and `--check`'s count would read that
    fold as none."""
    probe = [*text.split("\n"), "", marker("probe")]
    return not list(reader.live_lines(probe))[-1][1]
```
```python
    unclosed = [work_item_id for work_item_id, text in frags if leaves_open(text)]
    if unclosed:
        print(
            "ledger fragments that open a fenced block or an HTML comment and "
            "never close it, so every marker folded below them would read as "
            "no fold:"
        )
        for work_item_id in unclosed:
            print(f"  {FRAGMENTS}/{work_item_id}.md")
        print(
            "\nClose it in the fragment, then fold again.\n"
            f"nothing folded: {RELEASES}/ and {FRAGMENTS}/ are untouched"
        )
        return 1
```
```text
A block that never closes would run to the end, and `main` refuses the
fragment that holds one before it reaches here, because every marker folded
below it would read as no fold.
```
```python
def test_a_fragment_that_leaves_a_fence_open_is_refused(tmp_path):
    """#584 round 1, finding 2. The fold wrote B's marker below A's open
    fence, and `--check` then counted one fold where two had happened."""
    spec = importlib.util.spec_from_file_location("specseal_fold_r1f2", SCRIPT)
    fold = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fold)
    (tmp_path / "seal" / "ledger").mkdir(parents=True)
    (tmp_path / "seal" / "releases").mkdir()
    (tmp_path / "seal" / "ledger.md").write_text("# Evidence ledger\n", encoding="utf-8")
    (tmp_path / "seal" / "ledger" / "200-a.md").write_text(
        "| x | y |\n\n```\nnever closed\n", encoding="utf-8"
    )
    (tmp_path / "seal" / "ledger" / "300-b.md").write_text("| p | q |\n", encoding="utf-8")
    assert fold.main(["--version", "0.2.0", "--root", str(tmp_path)]) == 1
    assert not (tmp_path / "seal" / "releases" / "0.2.0.md").exists()
    assert (tmp_path / "seal" / "ledger" / "200-a.md").exists()
```
```text
A comment that never closes hides nothing. One shape that read before does
stop reading: a comment opener and a closer each quoted in a code span, on
lines either side of the table, are read as a comment that closes, as
`comment_scan` reads them, and the table between them is hidden;
```
```text
**A comment that is never closed hides nothing**, so a stray comment opener
changes no row that reads today. A delimiter inside a code span still counts:
prose that quotes the opener above the table and the closer below it hides
the table, so quote both on one line.
```
```text
    A comment that never closes hides nothing: an unclosed opener above the
    live table leaves every row where it was. The one shape that read before
    and does not now is a delimiter quoted in a code span -- an opener in
    prose above the table and a closer below it hide the table between,
    which `tests/test_unverified_rows_close.py`'s shape 8 pins.
```
```python
def fenced_lines(lines):
    """0-based indices of `lines` inside a fenced block, delimiters included,
    a block that never closes running to the end (#584).

    A delimiter line opens a fence only where it begins outside every HTML
    comment: inside a comment nothing is markdown, so a ``` line in a
    rider's own body opens nothing, and the riders below it are still read.

    The reader is loaded at the first markdown file that carries the marker,
    so a run over a tree with none never needs it."""
    global _reader
    if _reader is None:
        _reader = load_reader()
    fenced, fence, comment = set(), None, False
    for n, line in enumerate(lines):
        if fence is not None:
            fenced.add(n)
            if _reader.fence_closes(line, fence):
                fence = None
            continue
        if not comment:
            fence = _reader.fence_opener(line)
            if fence is not None:
                fenced.add(n)
                continue
        pos = 0
        while True:
            token = _reader.CLOSER if comment else _reader.OPENER
            at = line.find(token, pos)
            if at == -1:
                break
            pos, comment = at + len(token), not comment
    return fenced
```
```python
def test_a_fence_line_inside_a_rider_body_hides_no_rider_below():
    """#584 round 1, finding 4. The fence spans had no comment state, so a
    fence line in rider one's body opened a fence that swallowed rider two."""
    opener = "<" + "!-- RIDER: "
    text = (
        "# doc\n\n"
        + opener + "one\n```python\nsnippet\n"
        "Verified 2026-01-01 against x@abcdef12. -->\n\nprose\n\n"
        + opener + "two\nVerified 2026-01-01 against y@abcdef12. -->\n"
    )
    assert riders.comment_blocks(text.splitlines(), "doc.md") == [(3, 6), (10, 11)]
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the ten touched modules (`test_the_changelog_is_gathered_at_release`, `test_the_ledger_fragments_fold_at_release`, `test_a_rider_reaches_its_file`, `test_a_merge_cannot_silently_drop_a_correction`, `test_a_script_copied_alone_exits_2`, `test_a_section_marked_for_one_role_reaches_only_that_role`, `test_the_payload_meter_says_what_it_measured`, `test_the_mode_question_is_asked_once`, `test_the_seal_is_taken_once_by_the_sealer`, `test_unverified_rows_close`), at `68bcb224` | 638 passed, exit 0 |
| Live markers against line-anchored markers, on the real `CHANGELOG.md` and on the ledger files | 140/140; 125/125 |
| Gather with fragment A leaving a fence open and an ordinary B, then `--check`, then gather again | 0; 1 naming B; 0; B's entry twice |
| The same with a bare comment opener in A's prose | 0; 1 naming B; 0; B's entry twice |
| Fold with ledger fragment A leaving a fence open and an ordinary B, then `--check` | 0; 0 printing "1 work items marked" with two markers written |
| `config.md` with the comment delimiters quoted in code spans on either side of the table: `config_rows`, `declared_mode`, `missing_row` | `[]`; `none`; the commented-out refusal quoting the live `Broad gate` row |
| `comment_blocks` on a markdown file whose first rider's body holds a fence line, old and branch | `(3, 7), (11, 12)` against `(3, 7)` |
| `comment_blocks` over every file under the rider roots, old and branch | 0 files differ |
| S13's file with `table_lines` swapped for `unfenced` | reads `Broad gate = old -q` alone |
| `correction_check.py --range 551c7967...68bcb224` | exit 0; the range holds no merge commit |
| Fixes 1, 2 and 4 below applied in the clone: the three affected modules, then the probes above | 150 passed, exit 0; gather and fold exit 1 with nothing written; both riders read, a fenced rider reads as none |
| The three proposed cases below, verbatim, as a scratch module in the clone: at `68bcb224`, then with fixes 1, 2 and 4 applied | 4 failed; 4 passed |
| The full suite, lint, format and typecheck | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
