# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — review round 2

| Field | Value |
|---|---|
| Target SHA | 2dd618acec74c3516b0d7bf6bc384dec19a21bc7 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5[1m] |
| PR | 504 |
| Broad gate | 49ee16ad against 64036785 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round, targeted at the diff of round 1's fixes
(`7f38ca1a..2dd618ac`, record commits excluded) rather than the branch. Its job
was the answers: whether each of round 1's eight findings is actually closed.

Named as finding surface rather than verification surface: the three units in
round 1's `New units` row and the contract change on
`_the_corpus_covers_every_work_item_that_has_rounds`; commit 2dd618ac, which
the orchestrator wrote after round 1 closed to answer PR #504's windows CI leg
and which answers no round-1 finding; and whether finding 6's re-anchored
ledger row states a claim its new anchor carries, with the cause deferred to
#511 not reopened.

The orchestrator's narrow runs were named so the round would not repeat them,
and windows itself was named as not yet run on 2dd618ac.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1, re-read: the terminal-line paragraph now lists the stops the join has | `docs/review-chain-spec.md:2081` | confirmed | Read against `round_record.py#BLOCK_START` at `skills/code-review/scripts/round_record.py:1280`: every listed stop is an alternative of the regex, and `#120`, `**bold**`, `<` and indented prose match none of them |
| 🟢 | round 1's finding 2, re-read: the wrapper paragraph names `chain_check.py` as classified | `docs/review-chain-spec.md:2004` | confirmed | Read: `NO_WRAPPER` at `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:66` has exactly one key, `chain_check.py`, and its reason matches the paragraph |
| 🟢 | round 1's finding 3, re-read: the fragment's counts and the `retired:` paragraph | `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/changelog.md:7` | confirmed | Executed with `git ls-tree`: 99 dirs, 1,379 files and 263 records at 6d410023, and 12, 51 and 7 at 7811c0b. The wording left over is ⬜ A |
| 🟢 | round 1's finding 4, re-read: the memo arm reads through `flat` and guards a missing memo with `folded_items` | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:306` | confirmed | Read; executed at HEAD, green |
| 🟢 | round 1's finding 5, re-read: the corpus guard filters on a record committed at HEAD | `tests/test_a_finding_id_is_a_bare_integer.py:767` | confirmed | Executed: red with the filter removed, red with the message reverted, green restored |
| 🟢 | round 1's finding 6, re-read: the fragment row no longer anchors inside this work item's directory | `seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md:6` | confirmed | Executed: `bin/evidence-check --ledger` over the fragment, 9 ok · 0 drifted · 0 broken, exit 0. The cause stays with #511. The anchor's coverage is ⬜ B |
| 🟢 | round 1's finding 7, re-read: the wrap skip matches the raw line | `tests/test_docs_line_wrap.py:170` | confirmed | Read against `unverified_check.py:107`; the indented-marker arm executed at HEAD, green |
| 🟢 | round 1's finding 8, re-read: `gathered_entry` needs a space after the hashes | `tests/conftest.py#gathered_entry` | confirmed | Executed: red with `startswith("#")`, green restored |
| 🟢 | `_committed_at_head` and its new case, judged as code | `tests/test_a_finding_id_is_a_bare_integer.py:692` | confirmed | Read through the states a round mid-flight leaves, including a record deleted from disk beside an uncommitted one; both halves of the case seen red |
| 🟢 | 2dd618ac normalises the walk's separator, and it is the only comparison of that shape | `tests/test_chain_check_at_the_pull_request.py:2228` | confirmed | Executed: a throwaway case passed with `os.sep` patched to `\`, and went red with the old line. Searched `tests/` for other git-against-walk set comparisons and found none |
| ⬜ | the fragment's *Three more moved to fixtures* makes the nine floors read as fourteen | `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/changelog.md:37` | deferred `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/changelog.md` | Read against `phases/phase-1.md` §F1–F16: F3, F7 and F8 moved to fixtures and F9 and F10 are the cutoffs, all five among the nine red rows. A correction to the run's paperwork |
| ⬜ | the re-anchored row cites `whole_range`, which selects the declaration, and not `report`, which excuses the survivors | `seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md:6` | deferred `seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md` | Read: `survivor_check.py:944` is where a matched range becomes every candidate's grounds, and no anchor in the row covers it. A correction to the run's paperwork |
| ❓ out of verified scope | the full suite, the repository-wide lint and the typecheck | the whole branch | unverified | `agent-contract` §2: the broad gate is the sealer's, after the rounds settle. The spawn prompt says the same. Answered by `specseal:sealer` |
| ❓ out of verified scope | 2dd618ac on an actual windows interpreter | `tests/test_chain_check_at_the_pull_request.py:2228` | unverified | Probed only with `os.sep` patched on macOS. Answered by the windows leg of PR #504's CI |

## Paste-ready fixes

```
  item, and neither of these is. Of those nine, three moved to fixtures that
  plant their own specimens, and two are cutoff constants that now ask whether
  their work item is
```
```
| A range that retires 88 work items reports 12,100 survivors, and one range row excuses every one of them | `skills/code-review/scripts/survivor_check.py#whole_range@aeae8cd7`, `skills/code-review/scripts/survivor_check.py#report@<hash --reverify writes>` | …unchanged… | 2026-09-23 | …unchanged, plus: `whole_range` picks the declaration and `report` makes it every candidate's grounds, so the row cites both … |
```
```python
def test_the_walk_guard_reads_a_windows_walk_as_the_listing(monkeypatch):
    """2dd618ac. git spells a path with `/`, and a walk joins with `os.sep`;
    on windows the doubled-grounds sweep reported every committed record as
    missed. Red on any platform against `set(listed) - set(records)`."""
    records = [
        p.replace("/", "\\")
        for p in _real_records()
        if re.fullmatch(r"round-\d+\.md", os.path.basename(p))
    ]
    monkeypatch.setattr(os, "sep", "\\")
    _the_walk_found_every_committed_record(records, "a windows walk")
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on a throwaway case: `_the_walk_found_every_committed_record` over the committed records spelled with `\`, with `os.sep` patched to `\`; the same input with `os.sep` left as `/`; plus the memo-arm case and the wrap marker-in-a-sentence case | exit 0, 4 passed, read directly. The throwaway file was deleted afterwards |
| `walked = {…replace(os.sep, "/")…}` mutated to `walked = set(records)`, then the patched-separator probe case | exit 1, 1 failed; restored, exit 0, 1 passed |
| the `_committed_at_head` filter removed from the guard, then `test_a_work_item_whose_records_are_all_uncommitted_was_not_lost` | exit 1, 1 failed; restored, exit 0, 1 passed |
| the guard's message reverted to *hold a round record on disk*, then the same case | exit 1, 1 failed; restored, exit 0, 1 passed |
| `gathered_entry`'s heading test reverted to `line.startswith("#")`, then `test_a_gathered_body_line_opening_with_an_issue_number_is_kept` | exit 1, 1 failed; restored, exit 0, 1 passed |
| `bin/evidence-check --ledger seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md .` | exit 0, 9 ok · 0 drifted · 0 broken, read directly |
| `git ls-tree` counts of directories, files and round records under `seal/specs/` at 6d410023, 7811c0b^, 7811c0b and 2dd618ac | 99 / 1,379 / 263 at the fork point; 12 / 51 / 7 at the retirement commit; 15 / 103 / 16 at 2dd618ac, where the release merge brought three more work items in |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet. It is the sealer's run, and nothing this round opened stands between it and the sealer |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/review-chain-spec.md:2081` | round 1's 🟡 1 — fixed |
| round-1 | `docs/review-chain-spec.md:2004` | round 1's 🟡 2 — fixed |
| round-1 | `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/changelog.md:7` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:315` | round 1's 🟡 4 — fixed |
| round-1 | `tests/test_a_finding_id_is_a_bare_integer.py:733` | round 1's 🟡 5 — fixed |
| round-1 | `seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md:6` | round 1's 🟡 6 — fixed |
| round-1 | `tests/test_docs_line_wrap.py:168` | round 1's ⬜ 7 — fixed |
| round-1 | `tests/conftest.py#gathered_entry` | round 1's ⬜ 8 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `settle --retire` does not refuse a directory a ledger row anchors into | #511, deferred by round 1's fix table and already deferred in round 1 | the owner of #511 |
