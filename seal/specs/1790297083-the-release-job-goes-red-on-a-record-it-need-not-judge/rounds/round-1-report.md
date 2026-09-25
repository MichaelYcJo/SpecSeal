# Round 1 report — how chain_check reads a record (#598 instances 1 and 4, #529)

| Field | Value |
|---|---|
| Work item | `1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge` |
| Target SHA | c575695e |
| Reviewed against | `origin/release/v0.15.4` (7b557144); build range 97d0d2a7..c575695e over the frame 8c7569a0 |
| Reviewer | specseal:warden, round 1, in a `git clone --no-local` at the target |

## Summary

The three code changes do what `spec.md` asks, and every claim I checked held up against
the code and against execution. Three results carry the review:

- **`--find-object` without `--full-history` is safe.** I checked it in three merge shapes,
  including one where a plain path-limited log follows only the second parent. Git
  found the side-line bytes every time.
- **I found no route by which a pull request's own new record reads as restored.**
- **The draft excuse reaches exactly one refusal.** Ready and unreadable states still
  fail.

Eight mutations each turned the new cases red.

One finding needs a fix. Three documents still say the `Pass`-beside-`nobody` pair fails
the pull request at every stage. That is the class `spec.md` Scope 4 enumerated, but
these three copies were not listed there, and one of them sits in the same file as the
sentence this work replaced. It now says the opposite for a draft. The other four
findings are ⬜.

## Spec compliance (stage 1)

| Scenario | What the code does | How I know |
|---|---|---|
| A1, A2 (#529 merged re-add, skewed clock) | `added_on_branch` passes `--full-history --topo-order` (`chain_check.py#added_on_branch`) | **executed**. My probe S1 and S7 shapes both returned the late add. Mutation M6 (no `--full-history`) turned A1 and A2 red, and M5 (no `--topo-order`) turned A2 red |
| A3 (a merge is never the add) | unchanged behaviour, with a new case pinning it | **read** (the case asserts `ADDED by <side add>` and not the merge). **executed**: it passes in the narrow run |
| B1 to B3 (restoration, edited after restore, still read for everything else) | `restored_from` is asked at `main`'s `refs =` decision. `refs` is None and the line names the commit | **executed**. M8 (the `refs` ignores `restored`) turned five cases red. M1 (the predicate walks HEAD instead of the fork) turned 34 red, B2 and `test_a_record_new_in_the_pull_request_naming_a_foreign_commit_still_fails` among them |
| B4 (`written_late` silent on a restore) | `written_late` asks `restored_from` after `commissioned_fixes` and before `added_on_branch` | **executed**. M2 turned B4 red |
| C1 (draft prints) | `checked_by(..., strict)`: when `not strict` it returns a notice instead of the error | **executed**. M3 (`main` does not pass `strict`) turned C1 red |
| C2 (ready and no payload fail) | `strict = state != "draft"` in `main`, and `unknown` counts as strict | **executed**. M4 (the excuse at every stage) turned the no-payload case, the at-cutoff case and the ready case red. **read**: a malformed payload returns `unknown` in `pull_request_state`, the same path |
| C3 (no vocabulary refusal widened) | every other return in `checked_by` comes before the `strict` branch and ignores it | **read**, plus the parametrized case passing |
| C4 (`close`) | diverges from `plan.md`, as disclosed in `overview.md` | **read**, see the 🟢 row. The smith's grounds hold |
| D1 (documents) | the listed sentences carry the new behaviour | **read**. Three unlisted copies do not (🟡 1) |
| D2 (ledger) | new rows are in the fragment, and the drifted rows are re-read | **executed**: `evidence_check.py .` reported 2241 ok, 0 drifted, 0 broken |

## Where the prompt pointed hardest

**What "the fork" is.** In CI, `hygiene.yml` checks out the pull request's synthetic merge
commit with `fetch-depth: 0` and passes `--baseline origin/<base_ref>`. So `fork` is the
base tip:

- **Release pull request**: the tip of `main`.
- **Feature pull request**: the tip of `release/vX.Y.Z`.

Locally, `round_record.py close` passes the upstream or `origin/main`.

The predicate relaxes a record only when two things hold. The record is in the diff, and
its exact bytes stood at the same path in a commit the fork reaches. Two blobs match only
at the same path, and the path carries the work item id. So "common by accident" (an
empty file, a boilerplate) needs the same work item's path to have held those bytes on
the base.

A record authored on this branch reaches the base's history only through an earlier
merge of those bytes. That earlier merge is the pull request whose review the rule
defers to. **executed**: in probe 3 Q1, a branch whose own record was squashed into the
base by an earlier pull request, and which never merged the base back, keeps its record
in the diff, and `restored_from` returns None. Reachability is still asked.

On a release pull request, `fork` is `main` at the cut point. That commit holds no
record written during this release. `routing.md` is never asked, because the predicate
is called only on round records.

**`--full-history` dropped from the predicate.** I confirmed this on git 2.54.0
(**executed**, probe 1), in three shapes:

- **(a)** A side line changes the record X→Y→X and merges; the base line does not touch
  the path.
- **(b)** The same side line, while the base line changes X→Z. The merge is treesame to
  the first parent.
- **(c)** The base line goes X→Y→X while the side goes X→Z. The merge is treesame to the
  SECOND parent. A plain path-limited `git log` lists only `sideZ, addX`, so default
  simplification drops the first-parent line where Y lived.

In all three, `git log --find-object=<Y>` listed the same commits with and without
`--full-history`, and `restored_from` found Y in (c). The property rests on git's own
behaviour. `test_bytes_the_base_held_only_on_a_merged_side_line_are_found` pins it at
whatever git CI runs.

**`--topo-order` in `added_on_branch` under a skewed clock.** **executed**. Probe S7 dates
the side branch's delete and re-add before the early add, and it returned the late add.
The plan calls one shape arbitrary: two parallel adds of the same bytes, one before a
fix and one after it on a side line. I built it in both date orders, and both returned
the add that descends from the fix. The old code returned the early add there, because
default simplification follows the first parent at a treesame merge. So nothing
regressed.

**The draft notice.** Read in `checked_by` and confirmed by M3 and M4. The notice is
returned only under `last and pass_checked and began >= STRICT_FROM and not strict`.
Every other refusal returns before that point.

**C4.** The smith's premise holds. `round_record.py#run_check` (lines 2348–2367) writes
a `{"pull_request": {"draft": true}}` payload unless `pull_request_is_ready` (lines
988–1010) gets `isDraft: false` from `gh`. So `close` in the window is judged as a draft
and exits 0 with the notice. A strict path for `close` alone would be a second reading
of one pair. I searched `skills/`, `docs/`, `agents/`, `templates/` and `CONTRIBUTING.md`
for a sentence stating `close`'s exit code in that window and found none.

**The pin's rename and the replaced sentence.** The new sentence at
`skills/code-review/orchestration.md:519` is accurate. The renamed pin asserts all of it,
and it asserts that the old ending is gone. The old test name survives only in `spec.md`
and `phases/phase-3.md` prose, which describe the rename, and `evidence_check.py` refused
nothing there. But line 295 of the same file still states the old behaviour (🟡 1).

## Findings

### 🟡 1 — three copies still say `Pass` beside `nobody` fails the pull request, draft or not

**Where:** `skills/code-review/orchestration.md:295`, `templates/sdd-round.md:119`,
`README.md:609` (read).

**What is wrong.** All three say that on the last record, beside a checked `Pass`, the
pair *fails the pull request*. None of them mentions the exception this work item added:
on a draft, the pair now prints.

**Why it matters.**

- **`orchestration.md:295`** is the table the orchestrator reads to fill the cell. Line
  519 of the same file now says the opposite for a draft.
- **`templates/sdd-round.md`** is the template for every round record written from now
  on.
- **`README.md`** is where a plugin user learns what the check does.

These are the same class `spec.md` Scope 4 enumerated (§12, §14). The enumeration
listed `round-record-spec.md`, `review-chain-spec.md` and the one `orchestration.md`
sentence. It missed these three, and nothing checks them. `survivor_check` looks for the
removed sentence ("The draft excuse does not reach this row"), and none of the three
carries it.

**The fix:** add the draft half to each. The fences below are paste-ready.

### ⬜ 2 — the handoff protocol states the no-claim rule for an untouched record only

**Where:** `docs/review-handoff-protocol.md:190` and the bullet at lines 199–202 (read).

*"It makes no claim at all about a record the pull request does not touch"* is still
true. But the rule now has a second case, a record restored byte-for-byte. This copy
does not name it, and `commit-review-gate-spec.md`'s row now does. This is an incomplete
copy, not a false one.

### ⬜ 3 — the `written_late` docstring says an ordinary record pays no extra `git log`

**Where:** `skills/code-review/scripts/chain_check.py`, the last paragraph of
`written_late`'s docstring (read).

The sentence is *"Asked after the fixes are found and before the add is, so an ordinary
record pays no extra `git log`."* That holds only for a record that names no fix. A
record that names one pays a `rev-parse` and a `git log --find-object` over the fork's
whole history before `added_on_branch` runs. The last record pays that twice, once in
`main` and once here.

`phases/phase-2.md` states the qualifier correctly: *"an ordinary record with no fix
verdict"*. The cost itself is negligible. **executed**: 25 ms for one walk over this
repository's history.

### ⬜ 4 — `written_late`'s restoration exit also reaches records the pull request does not touch

**Where:** `skills/code-review/scripts/chain_check.py`, where `written_late` calls
`restored_from` (executed, probe 3 Q2).

`main` asks the predicate only for a last record in `touched`. `written_late` asks it
for every record. Probe 3 Q2 builds the case:

1. A branch's own record is squashed into the base by an earlier pull request.
2. The branch then merges the base in.
3. The record is no longer in the diff, but its adding commit `f1` is still in
   `<baseline>..HEAD`.

Before this change `written_late` judged it at `f1`. Now `restored_from` finds the
squash, and the arm is silent.

That is the right answer. The earlier pull request's range held `f1`, and the rule's *no
claim* for an untouched record is what applies. But neither `spec.md` Scope 2 nor the new
`review-chain-spec.md` row names this shape. The row describes only *"the directory is an
add … because the base retired it"*. Recorded so nobody has to find it again. No fix is
owed.

### ⬜ 5 — the changelog fragment counts three records where it means three shapes

**Where:** `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md:1`
(read).

*"stops going red on three records it had no claim to judge"*. The three are kinds of
record (a merged re-add, a restore, the draft pair), not three records. A reader of the
release note counts them.

## Regression tests to plant

None beyond what the branch planted. The eight mutations below each turned an existing
new case red. For 🟡 1, add pins if the fix pass wants them, beside
`tests/test_the_rules_have_one_owner.py::test_the_release_leg_is_not_red_until_the_verifying_rounds_record_commits`:

- the orchestration row's new clause, *"it fails a ready pull request"*;
- the draft half in `templates/sdd-round.md`.

## Facts for the evidence ledger

- `git log --find-object` lists the side-line commits of a merge whose result is
  treesame to either parent, with or without `--full-history`. Executed on git 2.54.0,
  shapes (a), (b) and (c) above. The fragment's A2 note already carries the claim;
  shape (c), the second-parent case, is new evidence for it.
- Inside `written_late`, a record whose bytes the fork already carries is silent even
  when the pull request does not touch it (⬜ 4, probe 3 Q2).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | three copies still say `Pass` beside `nobody` on the last record fails the pull request, with no draft exception | `skills/code-review/orchestration.md:295`, `templates/sdd-round.md:119`, `README.md:609` | open | read. The same class Scope 4 enumerated. Line 519 of the same orchestration file now says the opposite for a draft |
| ⬜ 2 | the handoff protocol's no-claim sentence names the untouched record and not the restored one | `docs/review-handoff-protocol.md:190` | open | read. Incomplete, not false |
| ⬜ 3 | `written_late` docstring: "an ordinary record pays no extra `git log`" is true only of a record naming no fix | `skills/code-review/scripts/chain_check.py#written_late` | open | read. `phases/phase-2.md` carries the right qualifier |
| ⬜ 4 | `written_late`'s restoration exit reaches untouched records whose add is still in range; right answer, unnamed shape | `skills/code-review/scripts/chain_check.py#written_late` | open | executed, probe 3 Q2 |
| ⬜ 5 | changelog says "three records" for three shapes | `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md:1` | open | read |
| 🟢 | `--find-object` walks both parents without `--full-history`; dropping the flag from `restored_from` is safe | `skills/code-review/scripts/chain_check.py#restored_from` | confirmed | executed, probe 1 (a)(b)(c), including the second-parent-treesame shape that a plain log simplifies |
| 🟢 | no route found by which a pull request's own new record reads as restored | `skills/code-review/scripts/chain_check.py#restored_from` | confirmed | executed, probe 3 Q1 and M1. read: same path plus same bytes in the fork's history is required, and the fork is the base tip in CI |
| 🟢 | `--topo-order` gives the late add under a skewed clock | `skills/code-review/scripts/chain_check.py#added_on_branch` | confirmed | executed, probe S7, M5 and M6 |
| 🟢 | the draft excuse reaches only `Pass` beside `nobody`; ready and unknown still fail | `skills/code-review/scripts/chain_check.py#checked_by` | confirmed | executed, M3 and M4. read: `strict = state != "draft"` |
| 🟢 | the C4 divergence's grounds hold: `run_check` judges `close` as a draft unless `gh` says ready | `skills/code-review/scripts/round_record.py#run_check` | confirmed | read, lines 2348–2367 and 988–1010. No document states `close`'s exit code in the window |
| 🟢 | the replaced orchestration sentence and its renamed pin are accurate and complete | `skills/code-review/orchestration.md:519` | confirmed | read. The pin asserts the whole sentence and the absence of the old ending |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the five touched modules (`test_chain_check_at_the_pull_request.py`, `test_a_record_precedes_the_fixes_it_commissions.py`, `test_the_last_rounds_fixes_are_checked.py`, `test_the_fixes_close_the_record.py`, `test_the_rules_have_one_owner.py`) at c575695e | 442 passed, exit 0 |
| probe 1: `git log --find-object` with and without `--full-history`, shapes (a), (b), (c) | identical lists in all three. In (c), plain `git log -- r.md` lists only `sideZ, addX`, and `restored_from` finds `mainY` |
| probe 2: `added_on_branch` on S1, S7, and the parallel add in both date orders | the late add every time |
| probe 3: a branch's own record squashed into the base; Q1 without merging the base back, Q2 after | Q1: in the diff, `restored_from` None. Q2: not in the diff, `restored_from` names the squash, while `added_on_branch` still names the branch's own add |
| eight mutations of `chain_check.py`, one at a time, each run against its modules and then restored (M1 predicate walks HEAD; M2 `written_late` skips the predicate; M3 `main` omits `strict`; M4 excuse at every stage; M5 no `--topo-order` in `added_on_branch`; M6 no `--full-history` there; M7 no `--topo-order` in the predicate; M8 `refs` ignores `restored`) | every mutation red: 34, 1, 1, 3, 1, 2, 1 and 5 failures. The clone was clean after restoring |
| `evidence_check.py .` in the clone | 2241 ok, 0 drifted, 0 broken |
| cost of one `restored_from` walk on this repository | 25 ms |
| the broad gate: full suite, lint, typecheck | not yet. Owed to the sealer, once, after the rounds settle; this round ran none of it |

### probe 1, shape (c)

```
1c result Z
1c no-full ['dfd33c6… mainBackX', '1d4f53c… mainY']
1c full    ['dfd33c6… mainBackX', '1d4f53c… mainY']
1c plain log no-full ['sideZ', 'addX']
1c restored_from 1d4f53ce3afa3d35c7c85456cb5ec981029d6008
```

### probe 3

```
3 Q1 (branch never merged base): touched? True restored_from: None
3 Q2 (branch merged base in): touched? False restored_from: ecd05c0 added_on_branch: 906ee6f f1: 906ee6f
```

## Paste-ready fixes

### 🟡 1 — `skills/code-review/orchestration.md:295`, the `nobody — <why>` row

```
| `nobody — <why>` | the gap, written down. It prints on every CI run, and on the run's **last** record beside a checked `Pass` it fails a ready pull request — a review cannot have passed while its own fixes went unread. On a draft that pair prints and names the verifying round, because the draft is where it stands between `close` and that round's record, and *Ready for review* re-runs the check. Work items begun before the rule landed are excused and only print |
```

### 🟡 1 — `templates/sdd-round.md:119–124`

```
`nobody` prints on every run. On the run's LAST record it also FAILS a ready
pull request when `Pass` is checked beside it, because that pair is the review
claiming to have passed while its own fixes went unread. On a draft the pair
prints and names the verifying round, because that is where it stands between
`close` and the verifying round's record, and *Ready for review* re-runs the
check. Work items begun before the rule landed are excused and only print. The
way out costs no round: one verifying round at the diff of those fixes, and a
round that opens nothing needing a fix does not consume the cap.
```

### 🟡 1 — `README.md:609–615`

```
- **`Fixes checked by: nobody` prints everywhere and fails in one place.** On
  the run's last record, beside a checked `Pass`, it fails a ready pull
  request: a review cannot have passed while the fixes that closed its
  findings went unread. On a draft that pair prints and names the verifying
  round, and *Ready for review* re-runs the check. Anywhere else it only
  prints. Work items begun before this rule landed are excused entirely,
  because a check whose first act is red on merged history nobody can repair
  is a check people learn to skip. The way out costs no round — one verifying
  round at the diff of those fixes.
```

Needs a fix: yes — 🟡 1, the three copies of the `Pass`-beside-`nobody` rule that still say it fails at every stage
Loses a record or crashes: no

The broad gate has not come due. This round leaves 🟡 1 open, so the sealer's spawn waits
for the round that verifies that fix.

## Proof block

Files opened this round (read or executed against), all at c575695e in the clone unless
marked as the work item's tree:

- work item: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`,
  `phases/phase-2.md`
- `seal/ledger/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge.md`
- `skills/code-review/scripts/chain_check.py`: `git`, `changed`, `pull_request_state`,
  `checked_by`, `added_on_branch`, `restored_from`, `written_late`, `main`, and the diff
  97d0d2a7..c575695e
- `skills/code-review/scripts/round_record.py`: `run_check`, `pull_request_is_ready`,
  `landing_values`
- `skills/verify/scripts/unverified_check.py`: `merge_base`
- `skills/code-review/orchestration.md`: lines 288–345 and 505–535
- `docs/review-chain-spec.md`: lines 306–320, 626–645, 685–695 and 890–925, plus the diff
- `docs/round-record-spec.md` and `docs/commit-review-gate-spec.md`: the diff
- `docs/review-handoff-protocol.md`: lines 180–205
- `templates/sdd-round.md`: lines 18–31 and 115–124
- `README.md`: lines 596–615
- `.github/workflows/hygiene.yml`: triggers, fetch depth and the `chain_check` step
- `CONTRIBUTING.md`: lines 100–125
- `bin/test`
- the test diffs of `tests/test_chain_check_at_the_pull_request.py`,
  `tests/test_a_record_precedes_the_fixes_it_commissions.py`,
  `tests/test_the_last_rounds_fixes_are_checked.py`,
  `tests/test_the_fixes_close_the_record.py` and `tests/test_the_rules_have_one_owner.py`

This round's scratch probes, fixtures and clone were deleted before handover.
