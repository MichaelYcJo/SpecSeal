# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — review round 1

| Field | Value |
|---|---|
| Target SHA | 07b7dc1b0246fb838dc9826628badb36e2f662e5 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5[1m] |
| PR | 504 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `7f38ca1a2e16645e4ffb0d32006e7846b5373267..34a31f274367025f7afd5a628c5a361ac9897f49`, 7 commits |
| Contract changes | _the_corpus_covers_every_work_item_that_has_rounds → pytest only |
| New units | _committed_at_head (depth 1); test_a_work_item_whose_records_are_all_uncommitted_was_not_lost (depth 1); test_a_gathered_body_line_opening_with_an_issue_number_is_kept (depth 1) |
| Needs a fix | yes — 🟡 1 to 🟡 6: two folded statements the tree contradicts, a changelog fragment with three false facts and one change left out, a re-point whose remaining arm crashes, a new guard that goes red in an ordinary state, and a ledger row that the next retirement breaks |
| Loses a record or crashes | no — finding 4's TypeError is in a test, on an arm HEAD cannot reach, and finding 6's row breaks only at a later fold; nothing shipped leaves the root or crashes |

- [x] Pass

## What this round was asked

Round 1, the first reading of the fold after it was merged with
`release/v0.13.1`, with nothing to inherit. Spec compliance first.

The round was pointed at five things in order: whether any of the 38 standing
statements is false of the tree or restores a sentence a later work item
overturned, which `overview.md` §Not verified hands to the review chain; the
two shipped-check changes, `chain_check`'s `retired:` arm and the wrap rule's
fold-marker skip, both halves of each; the three ledger rows REMOVED and two
narrowed; the orchestrator's merge commit 6c718758 and its fix commit
07b7dc1b, whose four re-pointed cases were to be judged against
`skills/settle/SKILL.md` §3 and whose two new test helpers were named as
correctness surface; and the Range cell of `survivors.md`.

The orchestrator's narrow runs on 07b7dc1b were named so the round would not
repeat them, the broad gate was withheld for the sealer, and the round was
told to use the branch's own `bin/` rather than the installed 0.13.0 on PATH.
#499 and #501 through #510 were named as filed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The folded terminal-line paragraph says `#`, `**` and `<` stop a join, and the code joins `**` and `<` and stops `#` only before a space | `docs/review-chain-spec.md:2081` | **fixed** `11b45013fa99d3d306913866b8a5d6f459416948` | fixed at 11b45013fa99d3d306913866b8a5d6f459416948 — the paragraph under the 1789347354 marker now names the stops `round_record.py#BLOCK_START` has (a heading marker followed by a space, list, quote or table markers, a fence, a thematic break, a setext underline) and says `#120`, `**bold**`, an HTML tag and an indented run are joined. No other copy of the old list stands: `docs/review-handoff-protocol.md` already said this; `round_record.py:1263-1270`, and 1789347354's own spec line 156 at `6d410023` |
| 🟡 2 | The folded wrapper paragraph says every named script has a `bin/` pair, and `chain_check.py` has none by classification | `docs/review-chain-spec.md:2004` | **fixed** `11b45013fa99d3d306913866b8a5d6f459416948` | fixed at 11b45013fa99d3d306913866b8a5d6f459416948 — the paragraph under the 1789338080 marker now says a named script has a wrapper pair or is classified in the pinning case, and names `chain_check.py` as the one classified, per `NO_WRAPPER` in `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`; `ls bin`, and `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:67` |
| 🟡 3 | The changelog fragment says the ledger is byte-identical, gives 38 files and ten re-pointed floors, and leaves out the `retired:` change to `chain_check` | `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/changelog.md:7` | **fixed** `8249982870e5f9ec78862328b862e641dc3d916c` | fixed at 8249982870e5f9ec78862328b862e641dc3d916c — 51 files, the ledger edited (three rows removed and two narrowed), nine red floors with three moved to fixtures, and a paragraph for `chain_check`'s `retired:` arm. 40919f38dfe2fd10d3368030b3c59db257f6e063 then brings the guard's wording to *a committed record*, to match finding 5's fix; the phase 11 step 3 table and before/after table, and the phase 1 floor table |
| 🟡 4 | The memo arm calls the local list `read`, so it raises `TypeError` whenever the memo exists, and it has no fold guard | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:315` | **fixed** `2bdf4be061ccbe274b55b3c7c79eecc351726702` | fixed at 2bdf4be061ccbe274b55b3c7c79eecc351726702 — the memo is read through `flat`, and a missing memo passes only where `docs/` carries the item's fold marker. Executed: green at HEAD; red with the marker removed; with the memo restored from `6d410023` green, and red with one pinned phrase edited. The restored file was then deleted. `seal/ledger.md` R3 re-read and re-verified; executed: memo restored, TypeError; memo removed, pass |
| 🟡 5 | The corpus guard fails on an uncommitted round record and blames the listing | `tests/test_a_finding_id_is_a_bare_integer.py:733` | **fixed** `40919f38dfe2fd10d3368030b3c59db257f6e063` | fixed at 40919f38dfe2fd10d3368030b3c59db257f6e063 — a work item counts as lost only when one of its records is at HEAD (`git cat-file -e` per path), and the message says *committed at HEAD*. New case `test_a_work_item_whose_records_are_all_uncommitted_was_not_lost`, red with the filter removed and red with the message reverted. Executed on the real tree: an uncommitted-only work item planted, red at the old guard and green at the new one; executed: planted an uncommitted round-1.md, got 1 failed; without it, 1 passed |
| 🟡 6 | A new ledger fragment row anchors inside this work item's directory, which the next retirement removes | `seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md:6` | **fixed** `841536744aecfc40290928431a63cf4c0423d11e` | fixed at 841536744aecfc40290928431a63cf4c0423d11e — the row now anchors at `skills/code-review/scripts/survivor_check.py#whole_range@aeae8cd7`, Checked 2026-09-23, and a note says why. Every ledger anchor into `seal/specs/` was enumerated, and the one left is `seal/ledger.md:78`, whose directory is kept. The cause, that `settle --retire` does not stop when a ledger row anchors into a directory it removes, is new mechanism: deferred #511; the same class as the five rows phase 11 repaired; `settle.py#coordinates` refuses nothing |
| ⬜ 7 | The wrap skip matches the stripped line, while the reader matches the raw line | `tests/test_docs_line_wrap.py:168` | **fixed** `9922e543d478cb6c57fc148867ddabfc89ed7094` | fixed at 9922e543d478cb6c57fc148867ddabfc89ed7094 — `prose_lines` matches the raw line, as `unverified_check.py#FOLD_MARKER` does. The marker-in-a-sentence case gained an indented-marker arm, which was red with the skip matching the stripped line. The fragment's row 1 was re-read and re-verified; `unverified_check.py:107` |
| ⬜ 8 | `gathered_entry` treats any line starting with `#` as a heading | `tests/conftest.py#gathered_entry` | **fixed** `34a31f274367025f7afd5a628c5a361ac9897f49` | fixed at 34a31f274367025f7afd5a628c5a361ac9897f49 — `gathered_entry` counts a line as a heading only when `#` to `######` is followed by a space. New case `test_a_gathered_body_line_opening_with_an_issue_number_is_kept`, red when the check is `startswith("#")`; `round_record.py#BLOCK_START` requires a space |

## Paste-ready fixes

```
**A wrapped terminal line is one value, and the join stops at a blank line.**
A terminal row a narrow window wrapped is still one value, so a continuation
is joined to it. A line that opens a new markdown block stops the join too —
a heading marker with a space after it, a list or quote marker, a fence, a
thematic break or a setext underline — and a continuation opening with an
issue number, `**bold**`, an HTML tag or an indent is joined, because its
first characters cannot tell it from prose. The blank line is the only stop
that covers every shape, and that sentence is the one that keeps the next
reader from widening the marker list instead of trusting the blank line.
```
```
**A script a shipped document tells an agent to run is reachable by a
command.** Every `skills/*/scripts/*.py` a shipped document names either has
a `bin/` wrapper pair or is classified, with its reason, in the case that
pins this rule — `chain_check.py` is classified, because CI runs it by path
and no shipped document shows it as a command to type. Every document naming
a script also names a form that can be typed: the wrapper, or the script's
repository-relative path. A document that names a script and no way to reach
it is an instruction with no executable spelling.
```
```
  `settle --retire` removes the directories the prose now covers. Measured
  before and after: 99 directories and 1,379 files under `seal/specs/`
  become 12 and 51, and the round-record corpus goes from 263 to 7. Eleven
  directories are kept by name — ten because they wrote no `spec.md` and so
  state no rule, and one because a permanent `seal/ledger.md` row anchors
  into its round record and the repository's own rule refuses a re-point.
  Five other `seal/ledger.md` rows anchored into a retired `spec.md`: the
  three whose only anchor that was are removed, and the two with a live code
  anchor keep it and drop the dead one.
```
```
  **No floor literal was lowered.** Nine checks carried a population floor
  over `seal/specs/` that the fold turns red, and every one of them was
  re-pointed rather than reduced — `assert len(records) > 200` becomes *the
```
```
  **The pull request's chain check now tells a retirement from a
  deletion.** A `routing.md` that `settle --retire` removed prints
  `retired: …` where a top-level `docs/` file carries the work item's
  `<!-- specs/<work-item-id> -->` marker on a live line, and is still refused
  where none does. The first fold put 88 such declarations in one diff, and
  the check had failed every one.
```
```python
    if not os.path.exists(memo_path):
        return
    memo = flat(os.path.relpath(memo_path, ROOT))
```
```python
def _committed_at_head(specs_dir, item):
    """Whether any round record `item` holds on disk is also at HEAD.

    A record written and not yet committed is the ordinary state of a round
    mid-flight, which `_the_walk_found_every_committed_record` already
    allows; a work item whose records are all uncommitted was not lost by
    the listing, because the listing is of HEAD.
    """
    rounds = os.path.join(specs_dir, item, "rounds")
    for name in os.listdir(rounds):
        if not re.fullmatch(r"round-\d+\.md", name):
            continue
        spec = f"HEAD:seal/specs/{item}/rounds/{name}"
        probe = subprocess.run(
            ["git", "-C", ROOT, "cat-file", "-e", spec], capture_output=True
        )
        if probe.returncode == 0:
            return True
    return False
```
```python
    missed = sorted(
        d for d in with_rounds - covered if _committed_at_head(specs, d)
    )
```
```
| A range that retires 88 work items reports 12,100 survivors, and one range row excuses every one of them | `skills/code-review/scripts/survivor_check.py#whole_range@<hash --reverify writes>` | …unchanged… | 2026-09-22 | …unchanged, plus: anchored at the checker rather than at this work item's `survivors.md`, which the next fold retires … |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_narrowed_ledger_read_says_what_it_skipped.py::test_an_inode_of_zero_does_not_fold_two_files_into_one`, with 1788501054's `overview.md` restored from `6d410023` | exit 1: `TypeError: 'list' object is not callable` at line 315. With the file removed again: 1 passed |
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py::test_the_committed_records_only_lose_a_miscount`, with an uncommitted `rounds/round-1.md` planted under this work item | exit 1: "1 work item(s) hold a round record on disk and contributed nothing". Without the file: exit 0, 1 passed |
| `bin/test tests/test_chain_check_at_the_pull_request.py tests/test_docs_line_wrap.py -k "retired or no_marker or fold_marker or marker_that_is_not"` | exit 0, 4 passed |
| The broad gate (`bin/test -q`, `uvx ruff check .`, `uvx ruff format --check .`) on the folded tree | not yet. It is the sealer's run, after the rounds settle, and this round did not run it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
