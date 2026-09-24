# 1790206437-a-second-fold-writes-a-second-heading — review round 2

| Field | Value |
|---|---|
| Target SHA | 9951af3b76d0cadbf307875f675a65f53edf85bd |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 552 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `9da6a30355a5589461eec306e62ea43c4626f586..fd6a8fd3161dd6fc5f82399774ba42f505a6e914`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 5, *the day after* in the two test docstrings and fragment row F3 (with `spec.md` and `questions.md`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round at round 1's fixes: the range `0c72d956..44146cf3` on `fix/540-a-second-fold-writes-a-second-heading`, two commits, plus the record commit that closed round 1, reviewed at 9951af3b. It asked whether 🟡 1's figure is now measured in all five carriers (re-counted), whether ⬜ 2's twenty doubled markers are what the records say, whether each new #542 sentence states the rule `same_run` keeps — including the tenth carrier the fix pass found in `chain_check.py#broad_gate`'s docstring — whether the two `survivors.md` rows fit the sweep's rule for released records, and whether the pull request body now carries the four gate answers. A round that opens nothing needing a fix does not consume the cap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 5 | *the day after* the preparation commit is false — `bee7ae99` 02:04:21 and `4ac9bf35` 02:35:35 on 2026-09-09 (+0900), thirty-one minutes apart and one date in either zone; the hygiene docstring also reads `4ac9bf35` as the preparation commit | `tests/test_release_hygiene.py:1118-1119`, `tests/test_the_ledger_fragments_fold_at_release.py:317`, fragment row F3's Notes (and `spec.md:19`, `questions.md:14-15`) | **fixed** `fd6a8fd3` | fixed at fd6a8fd3 — every in-tree carrier states the measured gap: `bee7ae99` at 02:04:21 and `4ac9bf35` at 02:35:35 on 2026-09-09 +0900, thirty-one minutes apart (17:04:21 and 17:35:35 UTC on 2026-09-08); the hygiene docstring names `bee7ae99` as the preparation commit; the two test docstrings, fragment row F3, `spec.md` and `questions.md`; no *day after* or *next day* left on this subject; executed — `git log -S'## 0.9.3 — ' -- seal/ledger.md` and `git log -1 --date=iso-strict` on both commits; the frame's measured-state table records no *day after*; the same class as round 1's 🟡 1, and F3 ships in `seal/ledger.md` |
| ⬜ 6 | three rewordings say a held run at the same commit and base is replaced, where `same_run` is asked of the newest entry alone | `agents/sealer.md:140-142`, `docs/review-chain-spec.md:343-344`, `skills/code-review/scripts/chain_check.py:3667-3668` (and `skills/code-review/orchestration.md:527-529`, `:537-539`) | **fixed** `fd6a8fd3` | fixed at fd6a8fd3 — `agents/sealer.md`, `docs/review-chain-spec.md`, `chain_check.py#broad_gate`'s docstring and both `skills/code-review/orchestration.md` paragraphs name the newest entry as the one a same comparison replaces, matching `same_run(entries[0], value)`; no code changed; four round-1 ledger notes narrowed in place; read — `round_record.py:382` compares `entries[0]` only; A/B1, A/B2, A/B1 keeps two entries for one comparison; rare and prose-only, so ⬜ |
| ⬜ 7 | #553's title and body still say two, and its correcting comment gives the twenty pairs as *at 9f846733* where the eleven after line 1764 are the tip's numbers | issue #553 | answered | corrected outside the tree by the orchestrator: #553's title and body say twenty, list the pairs at 9f846733 and name the two-line shift on a branch carrying #540's repair; executed — the pair lines at 9f846733, 9f5902e5 and 9951af3b; step D reads the body; the orchestrator's, outside the tree, out of `Needs a fix` |
| ⬜ 8 | the pull request body's gate table says `--check` is green over this tree, and its #540 row carries *the day after* | pull request #552 body | answered | corrected outside the tree by the orchestrator: PR #552's body no longer says *the day after* and says the doubled-version arm is silent over this tree while `--check` as a whole exits 1 on the branch's own unfolded fragment; executed — `fold_ledger.py --check --root .` exits 1 on the unfolded fragment at the target; the orchestrator's, out of `Needs a fix` |
| 🟢 | round 1's 🟡 1 is closed — the five carriers state the measured figure | `.github/scripts/fold_ledger.py:23-26`, `tests/test_release_hygiene.py:1119-1123`, `tests/test_the_ledger_fragments_fold_at_release.py:314-315`, the changelog fragment, F3 | verified | executed — seventeen `## 0.9.4`…`## 0.15.0` sections after line 1764 at 9f846733 and after 1673 at the target; eighteen tags after `v0.9.3`, `v0.13.2` sectionless; no *six release* outside the round records; the `v0.9.3` tag itself heads `0.9.3` twice, which no carrier contradicts |
| 🟢 | round 1's ⬜ 2 is closed — twenty doubled markers, 118 and 98, #553 named | `overview.md` §Not done, `phases/phase-5.md` | verified | executed — `grep -c` 118, `sort -u` 98, `uniq -d` 20 at the target |
| 🟢 | round 1's ⬜ 3 is closed — the two rewordings and the tenth carrier state the same-commit-same-base replace, `GATE_CARRIERS` intact | `agents/sealer.md:139-143`, `docs/review-chain-spec.md:341-346`, `skills/code-review/scripts/chain_check.py:3662-3669` | verified | read against `kept_broad_gate` and `same_run`; executed — the cell module green in the narrow run; the one qualifier they drop is ⬜ 6 |
| 🟢 | the two `survivors.md` rows' grounds hold under §*The survivor sweep*, and both quotes stand verbatim | `seal/specs/1790206437-a-second-fold-writes-a-second-heading/survivors.md` | verified | executed — quotes matched with whitespace collapsed; `survivor-check` over the fix range and over `9f846733..9951af3b` exit 0; at 44146cf3 the rows are not consulted, because the new docstring re-carries the shared phrases |
| 🟢 | round 1's ⬜ 4 is closed — the four gate answers stand in the pull request body | pull request #552 body | answered | executed — `gh pr view 552`; one of the four rows' sentences is ⬜ 8 |
| 🟢 | the seven shared ledger rows and F1, F3 re-stamped with dated notes; the ledger resolves | `seal/ledger.md` G2, S9, R1, C4, A5 and two unnamed rows; the fragment's F1, F3 | verified | executed — `evidence-check --strict .` `1686 ok · 0 drifted · 0 broken`; `correction-check` exit 0; read — each note against its changed sentence |
| ❓ | the broad gate — the full suite, the repository-wide lint and the format check over the settled branch | the sealer's `broad-gate` run | ❓ out of verified scope | `agent-contract` §2 keeps it from this round; the sealer answers it, and its spawn comes due once the run's last record has `Pass` checked with nothing needing a fix |

## Paste-ready fixes

```
    """The gathered ledger, the same way. #540: `fold_ledger.py` wrote a
    second `## 0.9.3` heading when a fragment landed half an hour after
    the release-preparation commit (`bee7ae99`, then `4ac9bf35`), and the
    file carried both through seventeen ledger sections (`0.9.4` to
    `0.15.0`, counted after the second heading; eighteen tags after
    `v0.9.3`) while the ticket said nobody had run the fold twice. Seen
    red against that tree: `0.9.3 twice, at lines [1673, 1764]`."""
```
```
    fragment landed half an hour later, and the second fold wrote a second
```
```
The second heading was written by `4ac9bf35` at 02:35 on 2026-09-09 (+0900), thirty-one minutes after the 0.9.3 preparation commit `bee7ae99` at 02:04 — both 2026-09-08 in UTC, the date the heading carries — a fragment landing after the release pull request went red, #289's shape one file over.
```
```
  sections), the second written by `4ac9bf35` thirty-one minutes after the
  0.9.3 preparation commit bee7ae99 — a fragment landing after the release
```
```
   `seal/ledger.md` heads `0.9.3` twice, written by `4ac9bf35` thirty-one
   minutes after the 0.9.3 preparation commit (1).
```
```
was — the new run written first, and a run the cell already held kept after
it as `earlier run` unless the newest is the same commit against the same base,
```
```
the same comparison as the newest entry replaces that entry
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/fold_ledger.py:24` (and `tests/test_release_hygiene.py:1120`, `tests/test_the_ledger_fragments_fold_at_release.py:314`, the changelog fragment lines 6–7, fragment row F3's Notes) | round 1's 🟡 1 — fixed |
| round-1 | `seal/specs/1790206437-a-second-fold-writes-a-second-heading/overview.md` §Not done, `phases/phase-5.md` §What this phase found, pull request #552 §Found outside the item | round 1's ⬜ 2 — fixed |
| round-1 | `docs/review-chain-spec.md:342-343`, `agents/sealer.md:140-142` | round 1's ⬜ 3 — fixed |
| round-1 | pull request #552 body | round 1's ⬜ 4 — answered |
| round-1 | the four test modules the diff adds to | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/fold_ledger.py:398-411`, fragment row F2 | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/fold_ledger.py#insert` | round 1's 🟢 — confirmed |
| round-1 | the sealer's `broad-gate` run | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
