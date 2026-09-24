# Round 3 report — 1790206437-a-second-fold-writes-a-second-heading

| Field | Value |
|---|---|
| Target SHA | 74a93fea |
| Base | `release/v0.15.1` (9f846733) |
| Scope | the verifying round, and the last of the run: round 2's fix range `9da6a303..fd6a8fd3` (one commit, fd6a8fd3), plus the record commit 74a93fea that closed round 2; issue #553 and pull request #552 (draft) for round 2's two out-of-tree rows |
| Reviewed in | a `git clone --no-local` of the worktree at the target SHA, under the session scratchpad; nothing was written in the worktree but this file |
| Earlier rounds | round 1 and round 2 — records and reports read for coordinates; every verdict below is re-derived |

Round 2's four rows hold at the target. The two commit times are what the
carriers now say. Every sentence the fix pass rewrote for ⬜ 6 names the
newest entry, which is the one entry `same_run` is asked about. The pull
request body and #553's title and body are corrected.

This round opens one 🟡 and one ⬜. The 🟡 came from the class grep the
prompt asked for. Two comments in `round_record.py`, the script #542 names,
still state the rule as it stood before `same_run`: a held run is kept, with
no replace. That is #542's own class in #542's own file, and phase 3's
*the class is closed at five carriers* missed them. The run is capped, so
it is deferred to a new issue. The ⬜ is #553's correcting comment, which
still labels the branch tip's line numbers as 9f846733's. Nothing here loses
a record or crashes.

## What the fixes were checked against

### 🟡 5 — the thirty-one minutes, re-measured (verified)

I measured these myself rather than reading them from round 2.

- `git log -1 --date=iso-strict` prints `2026-09-09T02:04:21+09:00` for
  `bee7ae99` (*chore: release 0.9.3 — five fragments, …*) and
  `2026-09-09T02:35:35+09:00` for `4ac9bf35` (*fix: the survivor step ran on
  a release range no fix pass wrote, and failed the release on it (#180)*).
  The same two commits under `TZ=UTC` print 17:04:21 and 17:35:35 on
  2026-09-08. The gap is 31 minutes 14 seconds.
- `4ac9bf35` is the direct child of `bee7ae99`: `git log bee7ae99..4ac9bf35`
  prints the one commit. So *a fragment landing after the release pull
  request went red* is the history as it stands.
- `git log -S'## 0.9.3 — ' -- seal/ledger.md` names `bee7ae99`, `4ac9bf35`
  and this branch's `d08c671`. `bee7ae99:seal/ledger.md` heads `0.9.3` once
  at line 1683; `4ac9bf35:seal/ledger.md` heads it at 1683 and 1774. Both
  headings read `2026-09-08`, which is the UTC date F3's Notes give as *the
  date the heading carries*.

The five in-tree carriers read against those numbers:

- `tests/test_release_hygiene.py:1117-1123` says *thirty-one minutes after
  the release-preparation commit (`bee7ae99` at 02:04:21, then `4ac9bf35` at
  02:35:35, 2026-09-09 +0900)*. The parenthetical now names `bee7ae99` first
  and as the preparation commit, which was round 2's second point. The
  count clause round 1's 🟡 1 fixed (seventeen sections, eighteen tags) is
  still there.
- `tests/test_the_ledger_fragments_fold_at_release.py:317-318` says
  *thirty-one minutes later (`bee7ae99` at 02:04, then `4ac9bf35` at 02:35,
  2026-09-09 +0900)*.
- Fragment row F3's Notes give both times, the +0900 date, and both UTC
  times on 2026-09-08. They add a sentence saying round 2 measured this.
- `spec.md:16-22` gives *(02:35:35 and 02:04:21 on 2026-09-09, +0900)* in
  the order the sentence names the two commits.
- `questions.md:13-15` gives *thirty-one minutes after the 0.9.3 preparation
  commit `bee7ae99`*.

`git grep -i -E "day after|next day|a day later|following day"` over the
whole tree, round records excluded, finds nothing on this subject. The pull
request body's #540 row now reads *thirty-one minutes after the 0.9.3
preparation commit bee7ae99*. `ruff check` and `ruff format --check` pass
on both test files and on `chain_check.py`.

### ⬜ 6 — the five rewordings, read against `same_run` (verified)

`kept_broad_gate` (`skills/code-review/scripts/round_record.py:347-386`)
splits the held cell and asks `same_run(entries[0], value)`. A match drops
that one entry. Every other held entry stays. `same_run` itself
(`:389`) compares both halves: commit by SHA prefix, base by exact word.

- `agents/sealer.md:139-143` now reads *a run the cell already held kept
  after it as `earlier run` unless the newest is the same commit against
  the same base, which the new entry replaces*. That is round 2's
  paste-ready block, byte for byte.
- `docs/review-chain-spec.md:341-346` reads *while the same comparison as
  the newest entry replaces that entry*. That is also round 2's block. The
  `GATE_CARRIERS` stands phrase `earlier run` survives.
- `skills/code-review/scripts/chain_check.py:3662-3669`, `broad_gate`'s
  docstring, carries the same words. It is a docstring change only, and the
  questions the function asks of `named[0]` are untouched.
- `skills/code-review/orchestration.md:527-529` reads *in front of any run
  the cell already held, which stays behind it as `earlier run`, unless the
  newest is the same commit against the same base, which the new entry
  replaces*. `:536-539` reads *a run the cell already holds is kept behind
  the new entry by either writer, and the newest, where it is the same
  commit against the same base, is replaced by either*.

All five name the newest entry, and none of them names any other held run
as replaced. Two of them put the *unless* after a subject that means any
held run, so a hurried reader could take the condition as applying to all
of them. The relative clause *which the new entry replaces* names the
newest as the one replaced, so I read that as right and did not open it.

The smith said the other carriers already said *the newest*. I opened them:
`docs/review-handoff-protocol.md:171`, `templates/sdd-round.md:39`, the
written comment at `round_record.py:4276-4285`, and `kept_broad_gate`'s own
docstring. All four do. No code changed in the range: the diff touches a
docstring in `chain_check.py` and prose everywhere else.

`bin/survivor-check --range 9da6a303..fd6a8fd3` examines 399 files against
the 24 sentences the range removed and finds no removed wording standing,
with or without `--exempt` the work item's `survivors.md`. So *taken again*
and *its own entry* survive nowhere.

### ⬜ 7 and ⬜ 8 — the out-of-tree corrections (answered, with ⬜ 10)

`gh issue view 553` shows the title *twenty ledger fragments began with
their own marker line …*. The body says twenty, 118 marker lines and 98
distinct. It lists the twenty pairs *at 9f846733 (the v0.15.0 tag)* and
says the eleven after line 1764 sit two lines higher on a branch carrying
#540's repair. I recounted the pairs at 9f846733 and at the target. The
body's twenty pairs are exactly 9f846733's, and the target's differ by two
from `1773/1776` on.

The correcting comment is unchanged: `gh api` reports its update time
equal to its creation time, 00:53:35Z. It still gives 1773/1776 …
2701/2704 as the pairs *in `seal/ledger.md` at 9f846733*, and those are the
target's numbers. Round 2's ⬜ 7 asked for that label to change as well.
The body is now right and says what the shift is, so step D reading the
body gets the right job. The comment is ⬜ 10 below.

`gh pr view 552` shows the gate table's *Test seen red* row saying the
doubled-version arm is silent over this branch's tree while `--check` as a
whole exits 1 on the branch's own unfolded fragment. I ran it:
`fold_ledger.py --check --root .` exits 1 and names only
`seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md`. The #540
row says *thirty-one minutes*. The pull request is still a draft, its base
is `release/v0.15.1`, and its head is 74a93fea.

### The ten ledger re-stamps (verified)

Eight rows in `seal/ledger.md` changed, and two in the fragment:

- four rows got a new dated `Re-read 2026-09-24 … round-2 fix pass` note:
  the `orchestration.md` seam row, R1, the `no fixes to check` row and A5;
- four round-1 notes were narrowed in place: G2, S9, the
  `chain_check.broad_gate` needs-no-second-reader row and C4. Each now quotes
  the new wording and says in brackets that round 2's fix pass narrowed it;
- F1 and F3 got new dated notes, and their anchors on the two test
  functions moved.

I diffed each row one changed segment at a time. Every changed hash
belongs to a unit the range edited. Every note describes the sentence that
changed, and none of the claims depends on it. `evidence-check --strict .`
reports `1686 ok · 0 drifted · 0 broken · 0 external · 0 old-format`,
exit 0. `correction-check --range 9f846733...HEAD` exits 0, with no merge
commit in the range.

## Findings

### 🟡 9 · two comments in `round_record.py` still state #542's replaced rule, and phase 3's grep did not reach them

These are from reading. The prompt asked for the grep across `agents/`,
`docs/`, `skills/` and `templates/`.

`skills/code-review/scripts/round_record.py:3955-3956`, in `close`:

> Through the same path as `seal` (round 1's 🟡 1): a run the cell already
> holds is kept behind the new entry by either writer.

`skills/code-review/scripts/round_record.py:4516-4519`, in `seal`:

> ONE ENTRY PER RUN, NEWEST FIRST (#174). A run the cell already holds is
> kept behind the new one as `earlier run`, because a second broad run …
> used to REPLACE the first …

Both comments sit directly above the `kept_broad_gate` call. Both say a
held run is kept, with no exception. The call they describe drops the
newest entry when it is the same commit against the same base. That is the
common case `same_run` exists for: the sealer re-run over an unchanged
checkout.

Why this is the ticket's own class. `spec.md` defines #542 as *sentences in
`skills/code-review/scripts/round_record.py` [that] describe the `Broad
gate` cell's rule as it stood before round 2's `same_run` fix*. Phase 3
judged the sentence at `orchestration.md:536-537`, *a run the cell already
holds is kept behind the new entry by either writer*, as *same falsehood*
and gave it the replace clause. The comment at `round_record.py:3955-3956`
is that sentence word for word, in the file #542 names. Phase 3 recorded
its grep terms: *taken again*, *stays behind*, *earlier one stays*, *count
of runs*, *count of entries*. None of them matches *is kept behind*, so
*the class is closed at five carriers* is short by these two. The pull
request closes #542 with them standing. Round 2 read `:4510-4525` and did
not open it.

Why 🟡 and not ⬜. This run has held carriers of the same-run rule at ⬜
when the prose was only wider than the code in an edge case (round 1's
⬜ 3, round 2's ⬜ 6). These two comments state a false fact about the
ordinary case. They are also the defect #542 exists to remove, and the
release ships that ticket as closed. By round 1's bar, that is a wrong fact
and not a sentence that reads badly.

A weaker third member, read and left to the fixer's judgment:
`agents/sealer.md:189` says *the newest first, and every earlier run kept
behind it*. The same file states the exception at `:141`, and a replaced
same-comparison entry is arguably not an *earlier run*. The block below
offers a wording that holds either way.

Neither comment is inside a unit this run's fixes created, since `close`
and `seal` predate the work item. So the run's cap defers this finding
rather than handing it back to the branch. Home: a new issue the
orchestrator files, milestone the owner's. After the edit, the ledger rows
anchored on `round_record.py#close` and `round_record.py#seal` need
`evidence-check --reverify`, and so does R1's `agents/sealer.md` anchor if
the third line is taken. #542's spec rejected pinning `round_record.py`
source text in `GATE_CARRIERS`. A pin is therefore the new issue's own
decision, not something this report assumes.

### ⬜ 10 · #553's correcting comment still labels the tip's line numbers as 9f846733's

Executed: `gh api …/issues/553/comments` shows the one comment unedited.
It gives the twenty pairs *in `seal/ledger.md` at 9f846733*, but from
`1773/1776` on they are the target's numbers. At 9f846733 line 1773 is the
`## 0.9.4` heading. The body is correct and now says what the shift is, so
the risk is a reader who opens the comment rather than the body. This is the
orchestrator's, outside the tree, and out of `Needs a fix`. The fix is one
edit to the comment: change *at 9f846733* to *at this branch's tip
(9f5902e5 and after)*, or delete the line list and point to the body.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 9 | two comments above the `kept_broad_gate` call say a held run is kept, with no same-run replace — #542's class in #542's file, which phase 3's grep terms did not match | `skills/code-review/scripts/round_record.py:3955-3956`, `:4516-4519` (and `agents/sealer.md:189`, weaker) | deferred #556 | read — `kept_broad_gate` drops `entries[0]` on `same_run`; `:3955-3956` is word for word the `orchestration.md` sentence phase 3 judged *same falsehood* and reworded; phase 3's grep terms (`phases/phase-3.md`) do not match *is kept behind*; the enclosing units `close` and `seal` predate the work item, so the cap defers it; a new issue the orchestrator files |
| ⬜ 10 | #553's correcting comment gives the target's twenty pairs as *at 9f846733* | issue #553, the comment of 2026-09-24T00:53:35Z | open | executed — pairs recounted at 9f846733 and 74a93fea; the comment's update time equals its creation time; the body is correct; the orchestrator's, outside the tree, out of `Needs a fix` |
| 🟢 | round 2's 🟡 5 is closed — every in-tree carrier states the measured thirty-one minutes, with `bee7ae99` as the preparation commit | `tests/test_release_hygiene.py:1117-1123`, `tests/test_the_ledger_fragments_fold_at_release.py:314-318`, fragment row F3, `spec.md:16-22`, `questions.md:13-15` | verified | executed — `git log -1 --date=iso-strict` and `TZ=UTC` on both commits (02:04:21 and 02:35:35 +0900; 17:04:21 and 17:35:35 UTC on 2026-09-08); `4ac9bf35` the child of `bee7ae99`; both headings `2026-09-08`; no *day after*, *next day* or similar on this subject in the tree outside the round records |
| 🟢 | round 2's ⬜ 6 is closed — the five rewordings name the newest entry as the one a same comparison replaces | `agents/sealer.md:139-143`, `docs/review-chain-spec.md:341-346`, `skills/code-review/scripts/chain_check.py:3662-3669`, `skills/code-review/orchestration.md:527-529`, `:536-539` | verified | read against `kept_broad_gate` and `same_run(entries[0], value)`; the handoff-protocol row, the template row, the written comment and the docstring were already precise; executed — `survivor-check` over the fix range, 24 removed sentences, none standing; the narrow modules green |
| 🟢 | round 2's ⬜ 7 is answered — #553's title and body say twenty and list 9f846733's pairs | issue #553 | answered | executed — `gh issue view 553`; the twenty pairs recounted at 9f846733 match the body; the comment's leftover is ⬜ 10 |
| 🟢 | round 2's ⬜ 8 is answered — the pull request body says the doubled-version arm is silent and `--check` exits 1 on the unfolded fragment, and gives thirty-one minutes | pull request #552 body | answered | executed — `gh pr view 552`; `fold_ledger.py --check --root .` exits 1 naming only this branch's fragment |
| 🟢 | the ten ledger rows re-stamped with dated or narrowed notes; the ledger resolves | `seal/ledger.md` G2, S9, R1, C4, A5, the seam row, the `no fixes to check` row, the needs-no-second-reader row; the fragment's F1, F3 | verified | executed — `evidence-check --strict .` `1686 ok · 0 drifted · 0 broken`; `correction-check` exit 0; read — each changed segment against the sentence it describes |
| 🟢 | round 1's four findings stay closed — the count clause round 1's 🟡 1 fixed survives the rewrite of the same docstrings | `tests/test_release_hygiene.py:1117-1123`, `tests/test_the_ledger_fragments_fold_at_release.py:314-315`, F3 | verified | read — seventeen sections and eighteen tags still stated; the range touches no other round-1 surface |
| ❓ | the broad gate — the full suite, the repository-wide lint and the format check over the settled branch | the sealer's `broad-gate` run | ❓ out of verified scope | `agent-contract` §2 keeps it from this round; the sealer answers it, and its spawn comes due once this round's record is closed with 🟡 9 deferred |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_release_hygiene.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py -q` in the clone at 74a93fea | 151 passed, exit 0 |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0; `total: 1686 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `python3 skills/evidence-check/scripts/correction_check.py --range 9f846733...HEAD` | exit 0; no merge commit in the range |
| `bin/survivor-check --range 9da6a303..fd6a8fd3`, with and without `--exempt` the work item's `survivors.md` | 399 files against 24 removed sentences; no removed wording standing either way |
| `python3 .github/scripts/fold_ledger.py --check --root .` | exit 1, naming only this branch's unfolded fragment; no doubled-version report |
| `uvx ruff check` and `uvx ruff format --check` on the two test files and `chain_check.py` | all checks passed; 3 files already formatted |
| `git log -1 --date=iso-strict`, and the same under `TZ=UTC`, on `bee7ae99` and `4ac9bf35` | `2026-09-09T02:04:21+09:00` / 17:04:21 UTC 2026-09-08; `2026-09-09T02:35:35+09:00` / 17:35:35 UTC 2026-09-08 |
| `git log -S'## 0.9.3 — ' -- seal/ledger.md`; `git log bee7ae99..4ac9bf35`; the `0.9.3` heading lines at both commits | `bee7ae99`, `4ac9bf35`, `d08c671`; one commit between; line 1683 at `bee7ae99`, 1683 and 1774 at `4ac9bf35`, both dated 2026-09-08 |
| `git grep -i -E "day after\|next day\|a day later\|following day"` over the tree, round records excluded | nothing on this subject |
| `git grep` for the same-run wordings (*same commit against the same base*, *same comparison*, *taken again*, *its own entry*, *already held*, *already holds*, *every earlier run*) over `agents/`, `docs/`, `skills/`, `templates/` | the five reworded carriers name the newest; `round_record.py:3955-3956` and `:4516-4519` state no replace (🟡 9); `agents/sealer.md:189` weaker |
| the twenty doubled marker pairs located at 9f846733 and at 74a93fea | 9f846733's pairs match #553's body; from `1773/1776` on, the comment's numbers are the target's |
| `gh issue view 553 --json title,body,comments`; `gh api` on its comments | title and body say twenty; the comment's update time equals its creation time |
| `gh pr view 552 --json isDraft,baseRefName,headRefOid,body` | draft, base `release/v0.15.1`, head 74a93fea; *thirty-one minutes*; the doubled-version arm silent, `--check` exit 1 on the fragment |
| the broad gate — the full suite, the repository-wide lint and the format check | not yet |

The clone and the output files under the round's scratch directory were
removed before hand-over. No probe file was written.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 9 · two comments in `round_record.py` (`close`, `seal`) say a held run is kept with no same-run replace; `agents/sealer.md:189` weaker | #556, milestone `release: 0.15.1`, taken by the document item `1790208643`; the run is capped and the units predate the work item | the orchestrator, who files it; the smith of the work item that takes it |

## Paste-ready fixes

### 🟡 9

`skills/code-review/scripts/round_record.py:3955-3956`, in `close`:

```
    # Through the same path as `seal` (round 1's 🟡 1): a run the cell
    # already holds is kept behind the new entry by either writer, and the
    # newest, where it is the same commit against the same base, is replaced
    # by either (`same_run`).
```

`skills/code-review/scripts/round_record.py:4516-4520`, in `seal`:

```
    # ONE ENTRY PER RUN, NEWEST FIRST (#174). A run the cell already holds is
    # kept behind the new one as `earlier run`, because a second broad run --
    # after a pre-existing failure, or after the last fixes landed -- used to
    # REPLACE the first and the run-level table was then filled from memory.
    # The newest entry alone is replaced, where it is the same commit against
    # the same base (`same_run`).
    # `kept_broad_gate` is the one path, shared with `close --broad-gate`.
```

`agents/sealer.md:189-190`, if the fixer takes the weaker line:

```
  entry of the cell records — the newest first, and every earlier comparison
  kept behind it. A tree that moves afterwards is a tree with no seal on it.
```

Needs a fix: yes — 🟡 9, the two `round_record.py` comments that state the
pre-`same_run` rule; deferred to #556 because the run is capped

Loses a record or crashes: no

## Proof

- executed — the six narrow modules, `evidence-check --strict`,
  `correction-check`, `survivor-check` over the fix range with and without
  the exemption file, `fold_ledger.py --check`, `ruff check` and
  `ruff format --check` on three files, the commit dates in two zones, the
  heading history, the tree-wide grep for the day wording, the class grep,
  the marker-pair recount at two commits, `gh issue view 553`, `gh api` on
  its comments, `gh pr view 552`
- read — round 1's and round 2's records and reports; the whole fix diff
  `9da6a303..fd6a8fd3`, every changed ledger row one segment at a time;
  `skills/code-review/scripts/round_record.py:305-395`, `:3950-3962`,
  `:4276-4290`, `:4510-4525`; `skills/code-review/scripts/chain_check.py:3658-3675`;
  `agents/sealer.md:134-150`, `:183-195`; `docs/review-chain-spec.md:336-348`;
  `skills/code-review/orchestration.md:520-542`;
  `docs/review-handoff-protocol.md:171`; `templates/sdd-round.md:39`;
  `skills/verify/scripts/broad_gate.py:1-20`; the work item's `spec.md:1-80`,
  `phases/phase-3.md:1-90`, `questions.md:11-16`
- unverified — the broad gate: the sealer
