# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — round 2 report

| Field | Value |
|---|---|
| Work item | `1790076070-the-fold-ships-and-the-corpus-is-still-on-disk` |
| Branch | `chore/497-the-fold-the-mechanism-was-built-for` |
| Target SHA | `2dd618acec74c3516b0d7bf6bc384dec19a21bc7` |
| Base | `origin/release/v0.13.1` |
| PR | #504 |
| Round | 2 — the verifying round, at `7f38ca1a..2dd618ac` less the record commits under `rounds/` |

## What this round read

The target is the diff of round 1's fixes, and nothing wider. The clone was a
`git clone --no-local` at 2dd618ac. Round 1's record and fix table gave the
coordinates; each verdict below was re-derived from the code, not carried.

Three surfaces nobody had reviewed were judged as code:

- the three units in round 1's `New units` row, plus the contract change on
  `_the_corpus_covers_every_work_item_that_has_rounds`;
- commit 2dd618ac, which answers no round 1 finding and fixes the windows leg
  of PR #504's CI;
- the re-anchored row in this work item's ledger fragment, whose cause went to
  #511.

All eight of round 1's findings are closed. Two corrections are left, and both
sit in this work item's own paperwork, so neither needs a fix.

## Round 1's eight findings — the account against the code

**Findings 1 and 2, the two folded paragraphs.** Read against the code they
describe. The terminal-line paragraph at `docs/review-chain-spec.md:2081` now
lists the stops `round_record.py#BLOCK_START` has at
`skills/code-review/scripts/round_record.py:1280`. Those are a heading marker
followed by whitespace or the end of the line, a list, quote or table marker, a
fence, a thematic break and a `=` setext underline. It also says `#120`,
`**bold**`, an HTML tag and an indented prose run are joined. The regex agrees
on every one: it allows leading whitespace before a marker, and nothing in it
matches `#1`, `**b` or `<`. The wrapper paragraph at
`docs/review-chain-spec.md:2004` names `chain_check.py` as the one classified
script. `NO_WRAPPER` in
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:66` has
exactly one key, and it is that one.

**Finding 3, the changelog fragment's counts.** Measured with `git ls-tree`.
At the fork point 6d410023 `seal/specs/` held 99 directories, 1,379 files
and 263 records. At the retirement commit 7811c0b it held 12, 51 and 7. The
fragment's before and after are both true, the ledger sentence matches what
phase 11 did, and the `retired:` paragraph is present. One sentence still reads
as a wrong count, which is correction ⬜ A below.

**Finding 4, the memo arm.** Read, and executed at HEAD. The memo now reads
through `flat`, so the `TypeError` path is gone. A missing memo asserts that
`folded_items(ROOT)` names the item before it returns, so a deletion with no
marker behind it fails. The case passed at HEAD in this round.

**Finding 5, the corpus guard.** Executed. The new case goes red with the
`_committed_at_head` filter removed and red with the message reverted to *on
disk*, and green with both restored. What the code does is below, under the
new units.

**Finding 6, the ledger row.** The directory anchor is gone and the row
resolves. The anchor it moved to carries half the claim, which is correction
⬜ B below. The cause, that `settle --retire` does not refuse a directory a
ledger row anchors into, is deferred to #511, and this round did not reopen it.

**Finding 7, the wrap skip.** Read, and the arm executed. `prose_lines` matches
`FOLD_MARKER` against the raw line, as the reader's own
`^<!-- specs/(\S+) -->$` at `skills/verify/scripts/unverified_check.py:107`
does. The indented-marker arm passed at HEAD in this round.

**Finding 8, `gathered_entry`.** Executed. The new case goes red when the check
is `line.startswith("#")` and green at HEAD. `#{1,6}(?:\s|$)` rejects seven
hashes followed by a space, and it agrees with the heading arm of
`BLOCK_START`.

## The new units, judged as code

**`_committed_at_head` is correct for every state I could construct.** It is
called only for a work item already in `with_rounds`, so its `rounds/`
directory exists. It asks about each record that is on disk, which is the same
set `with_rounds` was built from. Take a work item whose `round-1.md` is at HEAD
and deleted from disk, and whose `round-2.md` is on disk and not committed.
`on_disk` drops round 1 from the corpus, and this helper sees only round 2, so
the item is not called lost. That is the documented behaviour, *a work item
whose records are all uncommitted was not lost*. The `HEAD:` path is spelled
with `/`, which is what git wants on every platform.

**The new case tests both halves.** Its first call fails if the filter is
removed, because the mid-flight item would then count as missed. Its second
call passes an empty corpus, so the committed item is missed and the message
has to say *committed at HEAD*. Both mutations went red in this round.

**The `root` parameter is a contract change with one production caller.** It
is `tests/test_a_finding_id_is_a_bare_integer.py:850`, which leaves the default
`ROOT`. Nothing outside `pytest` calls the guard.

**The changelog case plants a body line that opens with `#120`, and it went red
against the old check.** It also asserts that the next release's entry is not
in the body, so a regex that stopped at no heading at all would fail it too.

## Commit 2dd618ac — the windows population guard

**The normalisation is correct, and the class has one member.** The
doubled-grounds sweep builds `records` with `os.path.relpath`, which joins with
`os.sep`, while `_real_records` returns git's `/` spelling. Before this commit
the set difference compared the two spellings, so on windows every committed
record read as unwalked. The fix-range sweep already normalised its own list.
The same sweep's later call to `doubled_grounds` also normalised already. On
POSIX the new `replace` does nothing, so no other platform's behaviour changed.

I searched `tests/` for other set comparisons between a git listing and a walk.
Only this helper does one. The corpus guard compares directory names from
`os.listdir` with the third component of git paths split on `/`, and both are
free of separators.

**Probed, because the windows leg has not run it yet.** A throwaway case passed
this repository's committed records to the helper spelled with backslashes. It
passed with `os.sep` patched to `\`, it went red with the old `set(records)`,
and it went red with `os.sep` left as `/`. It is a probe of the helper under a
patched separator. It is not a windows run, and the windows CI leg on PR #504
is still the check that answers for the platform.

**Nothing planted pins the fix off windows.** On macOS and Linux, reverting the
line leaves every case green, so only the windows leg would catch a revert. The
probe above could be planted, and it is under *Regression tests to plant*. It
is not a finding, because the windows CI leg already goes red on a revert.

## ⬜ A — the changelog reads as fourteen checks where there were nine

`seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/changelog.md:37`.

The paragraph opens *Nine checks carried a population floor … and every one of
them was re-pointed*. It then says *Three more moved to fixtures … and two
cutoff constants now ask*. The phase 1 floor table,
`phases/phase-1.md` §F1–F16, has nine red rows: F1 to F5 and F7 to F10. F3, F7
and F8 moved to fixtures, and F9 and F10 are the two cutoffs. So the three and
the two are part of the nine. *Three more* makes a reader add them, and the
paragraph then reads as fourteen checks.

The fix pass for round 1 finding 3 changed *Two more* to *Three more*, which is
where this was carried in. The count is right and the word *more* is wrong. It
sits under `seal/specs/`, so it is a correction and not a fix.

## ⬜ B — the re-anchored ledger row is held by the half that selects, not the half that excuses

`seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md:6`.

The clause is *one range row excuses every one of them*, and two units do
that. `whole_range` at `skills/code-review/scripts/survivor_check.py:824`
picks the declaration. It returns the first one that resolves onto the run's
range and belongs to a work item the range touches, which is what the row's
note says. `report` does the excusing, at
`skills/code-review/scripts/survivor_check.py:944`:
`grounds = whole[1] if whole else exempted(candidate, exemptions)`.

The row anchors only `whole_range`. If `report` changed so that a matched range
no longer excused every candidate, the clause would be false and the row would
still hash clean. The row is true today, because
`bin/survivor-check` was run at the fix range and `bin/evidence-check` resolves
the fragment, and nothing in it is broken. The coverage is half of what the
claim needs. It sits under `seal/ledger/`, so it is a correction.

The fragment's 12,100 and 88 figures are measurements of one range. No code
anchor could carry them, and the Verified-behavior cell already labels them
executed.

## Regression tests to plant

- `tests/test_chain_check_at_the_pull_request.py`, beside
  `test_the_records_in_this_repository_carry_no_doubled_grounds`: a case that
  calls `_the_walk_found_every_committed_record` with this repository's
  committed records spelled with `\` and `os.sep` monkeypatched to `\`. It is
  red against the pre-2dd618ac line on any platform. The body is in the fence
  under *Paste-ready fixes*.

## Facts for the evidence ledger

- The corpus guard's filter and its message are each defended by
  `test_a_work_item_whose_records_are_all_uncommitted_was_not_lost`. Executed
  in this round: removing the filter goes red, and so does reverting the
  message.
- `gathered_entry`'s heading test is defended by
  `test_a_gathered_body_line_opening_with_an_issue_number_is_kept`. Executed:
  `startswith("#")` goes red.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `settle --retire` does not refuse a directory a ledger row anchors into | #511, deferred by round 1's fix table and already deferred in round 1 | the owner of #511 |

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

The changelog block replaces the two lines at `changelog.md:37-38` up to
*whether their work item is*, and the reflow after it is the author's.

Needs a fix: no

Loses a record or crashes: no

The broad gate has come due. Nothing this round opened needs a fix, so what
comes next is the sealer's spawn at 2dd618ac, or at whatever commit carries the
two corrections.

## Proof block

Files opened in this round: `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/rounds/round-1.md`,
`rounds/round-1-fixes.md`, `changelog.md`, `phases/phase-1.md`,
`phases/phase-11.md` (grep), the diff `7f38ca1a..2dd618ac` in full,
`tests/test_a_finding_id_is_a_bare_integer.py:640-800`,
`tests/test_chain_check_at_the_pull_request.py:2160-2240, 2660-2720, 2840-2900`,
`tests/conftest.py#on_disk`, `skills/code-review/scripts/round_record.py:1273-1340`,
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:66-80, 232-261`,
`skills/verify/scripts/unverified_check.py:107, 897-907`,
`skills/code-review/scripts/survivor_check.py:824-905, 944, 1030-1060`,
`docs/review-chain-spec.md` §*A verdict row that commissions nothing*, and
`seal/specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys/rounds/round-2-report.md`
for the verifying-round shape.
