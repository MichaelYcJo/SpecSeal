# Round 2 report — 1790206437-a-second-fold-writes-a-second-heading

| Field | Value |
|---|---|
| Target SHA | 9951af3b |
| Base | `release/v0.15.1` (9f846733) |
| Scope | the verifying round: round 1's fix range `0c72d956..44146cf3` (bc186868, 44146cf3), pull request #552 (draft) |
| Reviewed in | a `git clone --no-local` of the worktree at the target SHA; nothing was written in the worktree but this file |
| Earlier rounds | round 1 — its record and report read for coordinates; every verdict below is re-derived |

Round 1's four rows hold at the target. The recount of 🟡 1 is right, the
twenty doubled markers are right, all three new rewordings state what the
code does in the case that matters, the two `survivors.md` rows have sound
grounds, and the four gate answers are in the pull request body.

This round opens one 🟡 and three ⬜. The 🟡 is in the same class as round
1's 🟡 1. It is an unmeasured fact about how the instance happened, and it
sits in the sentences the fix pass rewrote. The second `0.9.3` heading
landed thirty-one minutes after the preparation commit, not *the day after*
it. Nothing here loses a record or crashes.

## What the fixes were checked against

### 🟡 1 — the recount, re-measured (verified)

I measured these myself rather than reading them from round 1.

- `9f846733:seal/ledger.md` heads `0.9.3` at lines 1673 and 1764. After
  line 1764 there are seventeen version sections, `0.9.4` at 1773 through
  `0.15.0` at 2656. At the target the one `0.9.3` heading sits at line 1673
  and the same seventeen follow it.
- `git tag --sort=v:refname` prints eighteen tags after `v0.9.3`. `v0.13.2`
  is the one with no ledger section: the target's section list goes
  `0.13.1`, then `0.14.0`.
- All five carriers state the figure: `.github/scripts/fold_ledger.py:23-26`,
  `tests/test_release_hygiene.py:1119-1123`,
  `tests/test_the_ledger_fragments_fold_at_release.py:314-315`, the
  changelog fragment lines 6–8, and fragment row F3's Notes. Each carrier
  says how the figure was counted. `git grep -i "six release"` finds the
  phrase only in round 1's record and report, which are records of the
  finding.

One extra fact, which makes none of the carriers false:
`git show v0.9.3^{commit}:seal/ledger.md` already heads `0.9.3` twice. That
is true of every tag from `v0.9.3` to `v0.15.0`. So nineteen tagged releases
shipped the doubled heading, `v0.9.3` included. The carriers say *eighteen
tags after `v0.9.3`*, which is exactly true, and none of them says `v0.9.3`
shipped clean.

### ⬜ 2 — twenty doubled markers (verified)

`grep -c '^&lt;!-- specs/[^ ]* -->$' seal/ledger.md` prints 118 at the
target. The same lines through `sort -u | wc -l` print 98, and through
`uniq -d` they print 20. `overview.md` §Not done and `phases/phase-5.md` say
twenty, 118 and 98. They name #553 as the home, and #553 is open under
milestone `release: 0.15.1`. One thing outside the tree is still wrong about
it, and ⬜ 7 below covers it.

### ⬜ 3 — the three rewordings, read against `same_run` (verified, with ⬜ 6)

`kept_broad_gate` (`skills/code-review/scripts/round_record.py:347-386`)
splits the held cell and then asks `same_run(entries[0], value)`. That
compares the **newest** entry only, keeps both halves (commit by SHA prefix,
base by exact word) and drops that one entry on a match. Every other held
entry is kept.

- `agents/sealer.md:139-143` says a new commit, or another base, is kept, and
  the same commit against the same base is replaced. That is right for the
  newest entry.
- `docs/review-chain-spec.md:341-346` says the same. Its *recorded beside the
  first rather than over it* no longer uses the removed phrase, and it keeps
  the `GATE_CARRIERS` stands phrase `earlier run`.
- `skills/code-review/scripts/chain_check.py:3662-3669` is the tenth
  carrier, in `broad_gate`'s docstring. It describes the writer correctly:
  a re-seal at a new commit is kept, the same comparison taken again is
  replaced. The questions the function asks of `named[0]` are untouched by
  that, and the docstring still says so.

All three drop one qualifier the code carries, *the newest*, and ⬜ 6 below
covers that. I also read the one printed message in the same function that
talks about a kept run (`chain_check.py`, the no-SHA branch: *so a run the
cell holds is kept*). It is about `close --broad-gate` where fixes and the
gate land in one pass. That pass is always a new commit, so the sentence is
true, and I did not open it as a finding.

`bin/test tests/test_the_broad_gate_cell_keeps_every_run.py` is green
within the narrow run below, so every `GATE_CARRIERS` stands phrase
survives the rewording.

### ⬜ 3 — the two `survivors.md` rows (verified)

The rule in `docs/review-chain-spec.md` §*The survivor sweep* is that a
deliberate carrier is excused by a row quoting it. `survivor_check.py`
§*The escape* adds that the row is for a survivor somebody opened and judged
legitimate. Its §*A deletion is one row* names `CHANGELOG.md` among *the
durable copies that are supposed to survive*.

Both rows fit that. The first quotes the released 0.15.0 entry in
`CHANGELOG.md`. The second quotes the gathered fragment that entry came
from, `1790174138`'s `changelog.md`. Both quotes appear verbatim in their
files: I checked with whitespace collapsed. The grounds match the precedent
in `1790173209`'s `survivors.md`, where a released entry is a record of its
release. For the second row, the claim that rewriting it would leave the two
copies disagreeing is also correct.

What the rows do not do today, measured: at the tip they are never
consulted. `survivor-check --range 0c72d956..bc186868` reports the three
places. `--range 0c72d956..44146cf3` **without** `--exempt` reports nothing.
That is because 44146cf3's rewording of `chain_check.py` writes *records a
second run instead of erasing the first* and *so a re-seal* again, so the
phrases the two released copies share with the removed sentence count as
wording the range wrote. The rows are harmless and hold latently: a later
rewording of that docstring would bring the two survivors back and the rows
would excuse them. The sweep is green at the tip because nothing is
reported, not because the rows excuse anything. I am not opening this as a
finding. I record it so that nobody reads the green run as the rows being
exercised.

### ⬜ 4 — the gate answers (answered)

`gh pr view 552` shows the body's §*What a change to a gate must carry — the
`--check` arm* table with all four rows: seen red, failure direction,
prompt budget zero, platform honesty. ⬜ 8 below covers one sentence in it
that is out of date.

### The shared ledger re-stamps (verified)

Seven rows in `seal/ledger.md` changed only in an anchor hash and an
appended dated note: G2, S9, the `chain_check.broad_gate` needs-no-second-reader
row, and A5 on `chain_check.py#broad_gate`; R1 and the `no fixes to check`
row on `agents/sealer.md`; and C4 on `docs/review-chain-spec.md`. Each note
names what changed and says that the claim holds. For every one of them the
changed sentence is the docstring or prose above and not the behaviour the
row claims. `evidence-check --strict .` at the target reports
`1686 ok · 0 drifted · 0 broken`. `correction-check --range 9f846733...HEAD`
exits 0. Fragment rows F1 and F3 were re-stamped for the two docstrings.

## Findings

### 🟡 5 · *the day after* is a second unmeasured fact about the instance, in the sentences 🟡 1's fix rewrote

`tests/test_release_hygiene.py:1118-1119` says the second heading came
*when a fragment landed the day after the release-preparation commit
(`4ac9bf35`)*. `tests/test_the_ledger_fragments_fold_at_release.py:317`
says *a fragment landed the next day*. Fragment row F3's Notes say the
heading *was written by `4ac9bf35` on 2026-09-09, the day after the 0.9.3
preparation commit `bee7ae99`*.

Measured with `git log -S'## 0.9.3 — ' -- seal/ledger.md` and
`git log --date=iso-strict`:

- `bee7ae99`, the preparation commit, is dated `2026-09-09T02:04:21+09:00`.
- `4ac9bf35`, which wrote the second heading, is dated
  `2026-09-09T02:35:35+09:00`.

They are thirty-one minutes apart on the same day. In UTC they are both on
2026-09-08, the date the `0.9.3` heading carries. No time zone makes *the
day after* true. The phrase most likely came from comparing the heading's
date (09-08) with the commit's local date (09-09).

The frame's measured-state table in `spec.md` §*What is true today* records
only *2026-09-09, after the preparation commit*. So the *day after* in
`spec.md:19` was never measured, and it reached every carrier from there.
In the hygiene docstring, the parenthetical `4ac9bf35` also sits right
after *release-preparation commit*, so it reads as the SHA of that commit.
It is not: `4ac9bf35` is #180's fix, and the preparation commit is
`bee7ae99`.

Why 🟡 and not ⬜: this is the bar round 1 set for 🟡 1. The fact is wrong
rather than the sentence, and F3's Notes fold into `seal/ledger.md` at the
release. The fix pass rewrote the neighbouring clause in all three carriers
for 🟡 1's count and left this fact standing next to it, which is contract
§12's shape: the class was *an unmeasured fact about the instance's
history*, and only the count was fixed.

The carriers, enumerated with `git diff --name-only 9f846733..9951af3b`
and a `grep -i -E "day after|next day|a day later|following day"` over the
result, round records excluded:

- the two test docstrings above;
- F3's Notes;
- `seal/specs/1790206437-a-second-fold-writes-a-second-heading/spec.md:19`
  and `questions.md:14-15`, which are work-item paperwork that `settle`
  retires;
- pull request #552's #540 row, which is ⬜ 8's.

Paste-ready fixes are below for all five in-tree carriers. After the edits,
F3 and F1's anchors on the two tests need `evidence-check --reverify`.

### ⬜ 6 · three rewordings say *a run the cell already held* where the code compares the newest entry alone

`same_run` is asked of `entries[0]` only (`round_record.py:382`), and the
precise carriers say so: `kept_broad_gate`'s docstring (*A run the newest
entry already records*), the `broad-gate.md` comment
(`round_record.py:4282-4284`) and the handoff protocol's `Broad gate` row.

The imprecise ones say it of any held run:

- `agents/sealer.md:140-142` (fix range): *a run the cell already held kept
  after it as `earlier run` unless it is the same commit against the same
  base, which the new entry replaces*;
- `docs/review-chain-spec.md:343-344` (fix range): *the same comparison
  taken again replaces its own entry*;
- `chain_check.py:3667-3668` (fix range), in the same words;
- `skills/code-review/orchestration.md:527-529` and `:537-539` (phase 3,
  outside the fix range, the same class).

Here is a sequence where the prose and the code part: seal A against B1,
then A against B2, then A against B1 again. The code writes
`A against B1; earlier run: A against B2; earlier run: A against B1`, which
is two entries for one comparison. By the sentences above, the older
matching entry would have been replaced.

The sequence needs a base that changes and then changes back, so it is
rare, and the code is on the spec's unchanged list. This is prose that is
wider than the code in an edge case, so ⬜. The prose fix is one word,
*newest*. The code-side choice (drop every matching entry, not only the
newest) belongs to the repository owner if anyone wants it, and it would
also make `kept_broad_gate`'s *count of entries = count of distinct
comparisons* hold without that edge.

### ⬜ 7 · #553 still says two in its title and body, and its correcting comment labels the wrong commit

#553's title and body still say *two 0.15.0 work items' markers*, *two above
the folded sections* and *the two duplicate lines are removed (four lines
with their blanks)*. The orchestrator's comment corrects the count to
twenty, but it gives the twenty pairs' line numbers *in `seal/ledger.md` at
9f846733*.

Measured: at 9f846733 the eleven pairs after line 1764 stand two lines
lower. They are 1775/1778, 1795/1798, 2524/2527 … 2703/2706. The numbers in
the comment (1773/1776 … 2701/2704) are 9f5902e5's and the target's, after
this branch removed two lines. At 9f846733, line 1773 is the `## 0.9.4`
heading.

Step D (#547) takes #553 and will read its body first, so the body is what
states the job: two lines to remove, not twenty. The fix is the
orchestrator's, outside the tree. Correct the title and body to twenty, and
change the comment's *at 9f846733* to *at this branch's tip (9f5902e5 and
after)*. Paperwork, out of `Needs a fix`.

### ⬜ 8 · the pull request body says `--check` is green over this tree, and carries 🟡 5's *day after*

The gate table's *Test seen red* row ends *green over this tree*. Its
*Failure direction* row cites *this tree's own `--check` (exit 0)*.

At the target, `fold_ledger.py --check --root .` exits 1. It names
`seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md` as a
fragment that never folded, which is the expected state of a feature
branch carrying a fragment. Round 1 said this about the hand-back. The
doubled-version arm is silent over this tree, and that is the claim the
body means. The #540 row of *What changes* also says *written by 4ac9bf35
the day after the 0.9.3 preparation*, which is 🟡 5's fact.

Suggested wording for the orchestrator: *the doubled-version arm silent
over this tree (the command exits 1 only on this branch's unfolded
fragment)*, and in the #540 row *written by `4ac9bf35` thirty-one minutes
after the 0.9.3 preparation commit `bee7ae99`*. This is the pull request
body, the orchestrator's, and it is out of `Needs a fix`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 5 | *the day after* the preparation commit is false — `bee7ae99` 02:04:21 and `4ac9bf35` 02:35:35 on 2026-09-09 (+0900), thirty-one minutes apart and one date in either zone; the hygiene docstring also reads `4ac9bf35` as the preparation commit | `tests/test_release_hygiene.py:1118-1119`, `tests/test_the_ledger_fragments_fold_at_release.py:317`, fragment row F3's Notes (and `spec.md:19`, `questions.md:14-15`) | open | executed — `git log -S'## 0.9.3 — ' -- seal/ledger.md` and `git log -1 --date=iso-strict` on both commits; the frame's measured-state table records no *day after*; the same class as round 1's 🟡 1, and F3 ships in `seal/ledger.md` |
| ⬜ 6 | three rewordings say a held run at the same commit and base is replaced, where `same_run` is asked of the newest entry alone | `agents/sealer.md:140-142`, `docs/review-chain-spec.md:343-344`, `skills/code-review/scripts/chain_check.py:3667-3668` (and `skills/code-review/orchestration.md:527-529`, `:537-539`) | open | read — `round_record.py:382` compares `entries[0]` only; A/B1, A/B2, A/B1 keeps two entries for one comparison; rare and prose-only, so ⬜ |
| ⬜ 7 | #553's title and body still say two, and its correcting comment gives the twenty pairs as *at 9f846733* where the eleven after line 1764 are the tip's numbers | issue #553 | open | executed — the pair lines at 9f846733, 9f5902e5 and 9951af3b; step D reads the body; the orchestrator's, outside the tree, out of `Needs a fix` |
| ⬜ 8 | the pull request body's gate table says `--check` is green over this tree, and its #540 row carries *the day after* | pull request #552 body | open | executed — `fold_ledger.py --check --root .` exits 1 on the unfolded fragment at the target; the orchestrator's, out of `Needs a fix` |
| 🟢 | round 1's 🟡 1 is closed — the five carriers state the measured figure | `.github/scripts/fold_ledger.py:23-26`, `tests/test_release_hygiene.py:1119-1123`, `tests/test_the_ledger_fragments_fold_at_release.py:314-315`, the changelog fragment, F3 | verified | executed — seventeen `## 0.9.4`…`## 0.15.0` sections after line 1764 at 9f846733 and after 1673 at the target; eighteen tags after `v0.9.3`, `v0.13.2` sectionless; no *six release* outside the round records; the `v0.9.3` tag itself heads `0.9.3` twice, which no carrier contradicts |
| 🟢 | round 1's ⬜ 2 is closed — twenty doubled markers, 118 and 98, #553 named | `overview.md` §Not done, `phases/phase-5.md` | verified | executed — `grep -c` 118, `sort -u` 98, `uniq -d` 20 at the target |
| 🟢 | round 1's ⬜ 3 is closed — the two rewordings and the tenth carrier state the same-commit-same-base replace, `GATE_CARRIERS` intact | `agents/sealer.md:139-143`, `docs/review-chain-spec.md:341-346`, `skills/code-review/scripts/chain_check.py:3662-3669` | verified | read against `kept_broad_gate` and `same_run`; executed — the cell module green in the narrow run; the one qualifier they drop is ⬜ 6 |
| 🟢 | the two `survivors.md` rows' grounds hold under §*The survivor sweep*, and both quotes stand verbatim | `seal/specs/1790206437-a-second-fold-writes-a-second-heading/survivors.md` | verified | executed — quotes matched with whitespace collapsed; `survivor-check` over the fix range and over `9f846733..9951af3b` exit 0; at 44146cf3 the rows are not consulted, because the new docstring re-carries the shared phrases |
| 🟢 | round 1's ⬜ 4 is closed — the four gate answers stand in the pull request body | pull request #552 body | answered | executed — `gh pr view 552`; one of the four rows' sentences is ⬜ 8 |
| 🟢 | the seven shared ledger rows and F1, F3 re-stamped with dated notes; the ledger resolves | `seal/ledger.md` G2, S9, R1, C4, A5 and two unnamed rows; the fragment's F1, F3 | verified | executed — `evidence-check --strict .` `1686 ok · 0 drifted · 0 broken`; `correction-check` exit 0; read — each note against its changed sentence |
| ❓ | the broad gate — the full suite, the repository-wide lint and the format check over the settled branch | the sealer's `broad-gate` run | ❓ out of verified scope | `agent-contract` §2 keeps it from this round; the sealer answers it, and its spawn comes due once the run's last record has `Pass` checked with nothing needing a fix |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_release_hygiene.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py -q` in the clone at 9951af3b | 151 passed, exit 0 |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0; `total: 1686 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `python3 skills/evidence-check/scripts/correction_check.py --range 9f846733...HEAD` | exit 0; no merge commit in the range |
| `python3 .github/scripts/fold_ledger.py --check --root .` at 9951af3b | exit 1 on this branch's unfolded fragment; no doubled-version report |
| `bin/survivor-check --range 0c72d956..bc186868` | three places reported: `chain_check.py:3662`, `CHANGELOG.md:150`, `1790174138`'s `changelog.md:29` |
| `bin/survivor-check --range 0c72d956..44146cf3`, with and without `--exempt` the work item's `survivors.md` | no removed wording standing either way — the two rows are not consulted at this tip |
| `bin/survivor-check --range 9f846733..9951af3b --exempt` the same file | 39 removed sentences, no removed wording standing |
| the two `survivors.md` quotes searched in `CHANGELOG.md` and `1790174138`'s `changelog.md`, whitespace collapsed | True, True |
| `grep -n '^## [0-9]'` over `9f846733:seal/ledger.md` and the target's | seventeen sections after line 1764 at the base, the same seventeen after 1673 at the target, `0.13.2` absent |
| `git tag --sort=v:refname` after `v0.9.3` | 18 tags, `v0.9.4` … `v0.15.0` |
| `git show <tag>^{commit}:seal/ledger.md \| grep -c '^## 0.9.3'` for `v0.9.3`, `v0.9.4`, `v0.9.5`, `v0.10.0`, `v0.13.2`, `v0.14.0`, `v0.15.0` | 2 at every one, `v0.9.3` included |
| `git log -1 --date=iso-strict` on `bee7ae99` and `4ac9bf35`; `git log -S'## 0.9.3 — ' -- seal/ledger.md` | `2026-09-09T02:04:21+09:00` and `2026-09-09T02:35:35+09:00`; those two commits wrote the two headings |
| `grep -c '^&lt;!-- specs/[^ ]* -->$' seal/ledger.md`, then through `sort -u \| wc -l` and `sort \| uniq -d \| wc -l` | 118, 98, 20 |
| the doubled marker pairs located at 9f846733, 9f5902e5 and 9951af3b | 9f846733's eleven pairs after line 1764 stand two lines lower than the ones #553's comment gives |
| `gh pr view 552 --json isDraft,baseRefName,headRefOid,body` | draft, base `release/v0.15.1`, head 9951af3b; the four gate answers present; *green over this tree* and *the day after* in the body |
| `gh issue view 553 --json title,body,comments` | open, milestone `release: 0.15.1`; title and body say two; one comment corrects to twenty with 9f5902e5's line numbers labelled 9f846733 |
| the broad gate — the full suite, the repository-wide lint and the format check | not yet |

The clone, its `.venv` and the output files under the round's scratch
directory were removed before hand-over. No probe file was written.

## Paste-ready fixes

### 🟡 5

`tests/test_release_hygiene.py:1117-1123`, the docstring:

```
    """The gathered ledger, the same way. #540: `fold_ledger.py` wrote a
    second `## 0.9.3` heading when a fragment landed half an hour after
    the release-preparation commit (`bee7ae99`, then `4ac9bf35`), and the
    file carried both through seventeen ledger sections (`0.9.4` to
    `0.15.0`, counted after the second heading; eighteen tags after
    `v0.9.3`) while the ticket said nobody had run the fold twice. Seen
    red against that tree: `0.9.3 twice, at lines [1673, 1764]`."""
```

`tests/test_the_ledger_fragments_fold_at_release.py:317`, one line:

```
    fragment landed half an hour later, and the second fold wrote a second
```

Fragment row F3's Notes, the first sentence:

```
The second heading was written by `4ac9bf35` at 02:35 on 2026-09-09 (+0900), thirty-one minutes after the 0.9.3 preparation commit `bee7ae99` at 02:04 — both 2026-09-08 in UTC, the date the heading carries — a fragment landing after the release pull request went red, #289's shape one file over.
```

`seal/specs/1790206437-a-second-fold-writes-a-second-heading/spec.md:19-20`:

```
  sections), the second written by `4ac9bf35` thirty-one minutes after the
  0.9.3 preparation commit bee7ae99 — a fragment landing after the release
```

`seal/specs/1790206437-a-second-fold-writes-a-second-heading/questions.md:14-15`:

```
   `seal/ledger.md` heads `0.9.3` twice, written by `4ac9bf35` thirty-one
   minutes after the 0.9.3 preparation commit (1).
```

### ⬜ 6

`agents/sealer.md:140-141`:

```
was — the new run written first, and a run the cell already held kept after
it as `earlier run` unless the newest is the same commit against the same base,
```

`docs/review-chain-spec.md:343-344` and `chain_check.py:3667`: replace
*the same comparison taken again replaces its own entry* with:

```
the same comparison as the newest entry replaces that entry
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 5, *the day after* in the two test docstrings and fragment row F3 (with `spec.md` and `questions.md`)
Loses a record or crashes: no

## Proof

- executed — the six narrow modules, `evidence-check --strict`, `correction-check`, `fold_ledger.py --check`, four `survivor-check` ranges, the quote match, the section, tag, per-tag heading and marker counts, the commit dates, `gh pr view 552`, `gh issue view 553` and `547`
- read — round 1's `round-1.md` and `round-1-report.md`; the whole fix diff `0c72d956..44146cf3`, with every changed ledger row diffed segment by segment; `skills/code-review/scripts/round_record.py:300-410` and `:4278-4288`, `:4510-4525`; `skills/code-review/scripts/chain_check.py:395-460` and `:3640-3740`; `skills/code-review/scripts/survivor_check.py:60-160`; `docs/review-chain-spec.md:336-348` and `:2036-2090`; `agents/sealer.md:136-146`; `skills/code-review/orchestration.md:64-92` and `:524-540`; `docs/review-handoff-protocol.md:171`; `tests/test_the_broad_gate_cell_keeps_every_run.py:23-90`; `tests/test_release_hygiene.py:1114-1123`; `tests/test_the_ledger_fragments_fold_at_release.py:313-320`; the work item's `spec.md:17-22` and `:80-92`, `questions.md:12-16`, `overview.md`, `phases/phase-5.md`, `survivors.md`, `changelog.md`; `seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/survivors.md`
- unverified — the broad gate: the sealer
