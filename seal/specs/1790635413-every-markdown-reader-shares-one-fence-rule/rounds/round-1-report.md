# Round 1 — warden report

Target: branch `fix/584-every-markdown-reader-shares-one-fence-rule` at `68bcb224`, against `release/v0.16.0` at `551c7967`, the whole branch. No earlier rounds, so nothing was carried and every verdict below is derived in this round. The account read in full: `overview.md`, `spec.md`, `questions.md`, `survivors.md`, and the phase records through the plan's claims.

## What this round found, in one view

The branch does what it says on today's tree. Every marker count, every rider block and the ten touched test modules come out the same as the account claims. What it does not cover is text the new rule will meet later:

1. The release scripts now read markers through `live_lines`, but they still write whatever a fragment holds. A fragment that leaves a fence or a comment open makes the next marker they write unreadable to their own reader (🟡 1 for the changelog, 🟡 2 for the ledger). This is one class in two files.
2. The config reader's comment half cannot see a code span. A comment opener and a closer quoted in prose on either side of the live table hide that table, so the docs' promise that no file that reads today stops reading is false for this shape (🟡 3).
3. The rider check computes its fence spans with no comment state. A fence line inside a rider's own comment body hides every rider below it in that file (🟡 4).
4. One cleanup on the hook path (⬜ 5).

## The account, checked

| Claimed | Found |
|---|---|
| The gather's switch to live markers "changes no current answer" (`spec.md` §*Assumed, not asked*) | Confirmed by execution: `CHANGELOG.md` reads 140 live markers and 140 line-anchored ones |
| The ledger's markers are unchanged, with 0 fence lines in the ledger files | Confirmed by execution: 125 live markers against 125 line-anchored ones across `seal/ledger.md` and `seal/releases/*.md` |
| Phase 3 changes no current rider | Confirmed by execution: the old and new `comment_blocks` agree on every file under the rider roots |
| S13's case was red first | Sampled and confirmed: with `table_lines` swapped back to `unfenced`, the S13 file reads `Broad gate = old -q` alone |
| The ledger's residual, an unclosed fence hiding the markers below it, "needs … an unclosed fence in a ledger file. Neither exists today" | True of today's files. But the fold writes such a file itself from one fragment, and then reports the fold wrongly with exit 0. See 🟡 2 |
| "An unclosed comment hides nothing, so no file that reads today stops reading" (`spec.md`, `docs/the-broad-gate.md:87`, `templates/config.md:292`, `hooks/config.py:240`) | False for one shape that reads today. See 🟡 3 |
| "A block already open runs to its closing marker regardless, because inside a comment nothing is markdown" (`rider_check.py#comment_blocks`) | True for that block. But the fence state computed inside the comment outlives it and hides the riders that follow. See 🟡 4 |

## 🟡 1 — a gathered fragment can hide every marker below it, and `--check` then asks for a second gather

`.github/scripts/gather_changelog.py:102` (`live_markers`) and `:138` (`ungathered`).

`section` writes each fragment's body verbatim, followed by the next fragment's marker, and `insert` puts the new section above every older one. If a fragment opens a fenced block and never closes it, or writes a bare comment opener in prose, the next marker no longer stands on a live line. The same goes for the markers of every older release when the fence is left open. The gather writes those markers and its own reader then cannot see them.

Executed with two fragments, A leaving the block open and B ordinary:

- The gather exits 0.
- `--check` exits 1 and says B "never reached CHANGELOG.md". B's entry is in the file.
- Following the printed advice, `gather_changelog.py --version X.Y.Z`, exits 0 and writes B's entry a second time. The file then holds B twice.
- In the fence shape `--check` stays red after that too, because the second marker is also below A's fence, and the older release's marker has stopped counting as well.

Before this branch the substring test passed the file. A rendering defect was already there, but no check lied about it. The branch introduced the disagreement between what the gather writes and what it reads, and the advice this produces corrupts the release note. The fix refuses such a fragment before anything is written, in the same shape as the #586 refusal beside it, and asks `live_lines` itself, so there is no second rule.

## 🟡 2 — the fold writes the same trap into a release file, and `--check` passes with a wrong count

`.github/scripts/fold_ledger.py:216` (`live_markers`), `:238` (`is_marked`), `:867` (`--check`'s count).

This is the same class, and it is quieter. Executed with a ledger fragment A holding `| x | y |` and then an opened fence, plus an ordinary B:

- The fold exits 0 and writes two markers into `seal/releases/0.2.0.md`.
- `live_markers` reads only A's.
- `fold_ledger.py --check` exits 0 and prints "1 work items marked across seal/ledger.md and 1 release file" after two were folded.

From then on `is_marked` and `doubled_markers` cannot see B's fold. A fragment for B that comes back, for example from a stacked branch, folds a second time without the refusal that exists to prevent it. `demote`'s docstring still promises that "a block that never closes runs to the end, as it did". With the fix that block never reaches `demote`, so that sentence should say the fold refuses it.

## 🟡 3 — prose quoting the comment delimiters in code spans hides the live config table

`hooks/config.py:232` (`commented`), with the sentences at `hooks/config.py:240`, `docs/the-broad-gate.md:87` and `templates/config.md:292`.

`commented` reads a comment opener inside a code span as an opener, which the docstring states and the parity shape 8 pins. The consequence is not stated anywhere. Executed on a `config.md` whose prose reads "To park a row, open it with `` `&lt;!--` ``." above the table and "and close it with `` `-->` ``." below it:

- `config_rows` returns `[]`. Before the branch it returned both rows.
- `declared_mode` answers `none`, so `mode-gate` asks the mode question on a repository that answered it.
- `broad-gate` refuses with the new sentence: the live `| Broad gate | bin/test -q |` is "written inside an HTML comment" and should be taken "out of the comment". The person sees that row in a rendered, live table, so this is the wrong-cause shape #415 and #429 were opened about.
- Read, not executed: `seal.py#with_row` then finds no table through `table_span` and appends a second one below the closing line.

Three shipped sentences promise that no file that reads today stops reading. This file did read, and now does not. The cheaper repair is to state the shape where the promise is made, and the fix below does that. The alternative is to teach `commented` a code span that closes on its own line. That also changes the parity test's oracle, because `comment_scan` does not model code spans, and it is the plan's decision to reopen, not this round's.

## 🟡 4 — a fence line inside a rider's own comment hides every rider below it

`.github/scripts/rider_check.py:210` (`fenced_lines`), read by `comment_blocks` at `:286`.

`fenced_lines` takes `fence_spans` over the whole file, and `fence_spans` has no comment state. A markdown rider whose body holds a line such as a code-fence opener (say, a snippet in a note) therefore opens a "fence" inside the comment. That fence runs until the next matching delimiter or to the end of the file, and every rider in that span is skipped.

Executed: a file with rider one, whose body holds such a line, and rider two below it. The old reader returns blocks `(3, 7)` and `(11, 12)`, and the branch returns `(3, 7)` alone. Rider two is never resolved and never reported. That is the silence #239 closed for riders outside the rider roots. No file in today's tree has this shape (executed), so the finding is latent. The fix asks `fence_opener` only on a line that begins outside every comment. With it, both riders are read and a fenced quotation of a rider still reads as none (executed).

## ⬜ 5 — the hook computes the fence walk twice per table walk

`hooks/config.py:281` (`table_lines`).

`table_lines` calls `commented`, which walks `fence_map`, and then `unfenced`, which walks `fence_map` again. This runs on every Bash call through `mode-gate`. The files are small, so the cost is small, but it is the path whose cost the spec cited to keep the copy at all. `commented` could take the shown lines as a parameter and `table_lines` could compute `fence_map` once. This is not a defect.

## Regression tests to plant

- `tests/test_the_changelog_is_gathered_at_release.py`: a fragment that leaves a fence or a comment open is refused, and nothing is written (🟡 1). In the fix block below.
- `tests/test_the_ledger_fragments_fold_at_release.py`: the same for the fold, and no release file is written (🟡 2). In the fix block below.
- `tests/test_a_rider_reaches_its_file.py`: a fence line inside a rider's body hides no rider below it (🟡 4). In the fix block below.
- `tests/test_the_mode_question_is_asked_once.py`: pin whichever reading 🟡 3 settles on for the code-span shape. If it is the documented one, pin `config_rows` returning `[]`, so the next edit has to change the case.

The three cases for 🟡 1, 🟡 2 and 🟡 4 were run in the clone as a scratch module, taken verbatim from the fences below. All four parametrised cases fail at `68bcb224` and pass with the fixes applied. They have not been run inside their destination modules.

## Facts for the evidence ledger

- The release scripts refuse a fragment that leaves a fence or a comment open, so every marker they write stands on a live line. Anchor it on the new refusals once they land.
- `rider_check.py#fenced_lines` decides a fence only on a line that begins outside every HTML comment. Anchor it on `fenced_lines` once 🟡 4's fix lands.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A changelog fragment that leaves a fence or a comment open hides the markers the gather writes below it. `--check` then calls a gathered entry missing, and the gather it advises writes the entry twice | `.github/scripts/gather_changelog.py:102` | open | Executed: gather 0, `--check` 1 naming B, regather 0, B's entry twice in the file |
| 🟡 2 | A ledger fragment that leaves a fence open hides the markers folded below it. `--check` passes with a wrong count, and `is_marked` cannot see the fold | `.github/scripts/fold_ledger.py:216` | open | Executed: fold 0, two markers written, one live, `--check` 0 printing 1 |
| 🟡 3 | A comment opener and a closer quoted in code spans on either side of the live config table hide that table. The live row is then called commented out, and three shipped sentences promise this cannot happen | `hooks/config.py:232` | open | Executed: `config_rows` `[]`, `declared_mode` none, `broad-gate` gives the commented-out refusal quoting the live row |
| 🟡 4 | The rider check's fence spans ignore comment state, so a fence line inside a rider's body hides every rider below it | `.github/scripts/rider_check.py:210` | open | Executed: old reader 2 blocks, branch 1. None in today's tree |
| ⬜ 5 | `table_lines` walks `fence_map` twice on every Bash call | `hooks/config.py:281` | open | Read |
| 🟢 | The marker readers change no current count | `CHANGELOG.md`, `seal/ledger.md`, `seal/releases/*.md` | confirmed | Executed: 140/140 and 125/125 |
| 🟢 | The rider reader changes no current block | `.github/scripts/rider_check.py:226` | confirmed | Executed: 0 files differ between the base and the branch |
| 🟢 | S13's case fails without the comment half | `hooks/config.py:281` | confirmed | Executed: the swap back to `unfenced` reads the parked row alone |
| ❓ | The ledger fragment's rows, and the re-read and corrected notes across `seal/releases/*.md`, were not run through `evidence-check` | `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | ❓ out of verified scope | A plugin check the broad gate runs. The sealer answers it |
| ❓ | The new cases on the Windows and Linux legs | `tests/test_a_script_copied_alone_exits_2.py` | ❓ out of verified scope | Only macOS ran here. CI's test matrix at the pull request answers it |

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

## Paste-ready fixes

### 🟡 1 — `.github/scripts/gather_changelog.py`

After `ungathered`:

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

In `main`, directly after the `headed` refusal's `return 1`:

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

The case, in `tests/test_the_changelog_is_gathered_at_release.py`:

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

### 🟡 2 — `.github/scripts/fold_ledger.py`

After `is_marked`:

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

In `main`, directly before `date = args.date or …`:

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

In `demote`'s docstring, replace "A block that never closes runs to the end, as it did." with:

```text
A block that never closes would run to the end, and `main` refuses the
fragment that holds one before it reaches here, because every marker folded
below it would read as no fold.
```

The case, in `tests/test_the_ledger_fragments_fold_at_release.py`:

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

### 🟡 3 — the three sentences that promise no file stops reading

In `docs/the-broad-gate.md`, replace "A comment that never closes hides nothing, so no file that reads today stops reading," with:

```text
A comment that never closes hides nothing. One shape that read before does
stop reading: a comment opener and a closer each quoted in a code span, on
lines either side of the table, are read as a comment that closes, as
`comment_scan` reads them, and the table between them is hidden;
```

In `templates/config.md`, replace "**A comment that is never closed hides nothing**, so a stray comment opener changes no row that reads today." with:

```text
**A comment that is never closed hides nothing**, so a stray comment opener
changes no row that reads today. A delimiter inside a code span still counts:
prose that quotes the opener above the table and the closer below it hides
the table, so quote both on one line.
```

In `hooks/config.py#commented`'s docstring, replace the sentence that begins "A comment that never closes hides nothing, so no file that reads today stops reading:" and ends "leaves every row where it was." with:

```text
    A comment that never closes hides nothing: an unclosed opener above the
    live table leaves every row where it was. The one shape that read before
    and does not now is a delimiter quoted in a code span -- an opener in
    prose above the table and a closer below it hide the table between,
    which `tests/test_unverified_rows_close.py`'s shape 8 pins.
```

### 🟡 4 — `.github/scripts/rider_check.py#fenced_lines`

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

The case, in `tests/test_a_rider_reaches_its_file.py`:

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

Needs a fix: yes — 🟡 1 and 🟡 2 (the release scripts write markers their own readers cannot see), 🟡 3 (the config reader hides a live table and three sentences promise it cannot), 🟡 4 (the rider check hides riders below a fence line inside a comment)
Loses a record or crashes: no

## Proof block

Files opened this round, all in a `git clone --no-local` at `68bcb224`:

- `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/overview.md`, `spec.md`, `questions.md`, `survivors.md`
- `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` (the head of it)
- `hooks/config.py`, `skills/verify/scripts/broad_gate.py`, `skills/verify/scripts/unverified_check.py`, `skills/implement/scripts/seal.py`
- `.github/scripts/fold_ledger.py`, `.github/scripts/gather_changelog.py`, `.github/scripts/rider_check.py`
- `skills/evidence-check/scripts/correction_check.py`, `skills/verify/scripts/payload_meter.py`, `skills/evidence-check/SKILL.md`
- `docs/the-broad-gate.md`, `templates/config.md`
- `tests/test_unverified_rows_close.py`, `tests/test_the_mode_question_is_asked_once.py`, and the other touched test modules' headers
- `.github/workflows/hygiene.yml` (the `--check` steps)
- The branch diff `551c7967...68bcb224` for every code file above
