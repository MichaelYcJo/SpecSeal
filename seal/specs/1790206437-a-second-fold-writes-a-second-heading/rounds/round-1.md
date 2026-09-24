# 1790206437-a-second-fold-writes-a-second-heading — review round 1

| Field | Value |
|---|---|
| Target SHA | 9f5902e5a0f62121a0cf5d9972552a25aad6481a |
| Written late | no |
| Ran by | warden on Fable 5.1 |
| PR | 552 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1, the *six releases* count in five carriers |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 was asked to review the whole branch at 9f5902e5 against `release/v0.15.1` (9f846733): spec compliance first against `spec.md`, `plan.md` and the gate table for the `--check` arm, then quality, in a clone under the round's own directory, narrow runs only, with the smith's handoff before round 1 as the account to audit — the dead kept-date override and `insert`'s line splitting, the per-carrier judgment for #542's two extra carriers, the doubled marker lines the branch found and left filed, and step D building on top of these helpers so a signature change costs it a rebase.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | *for six releases* is an unmeasured count, false in five carriers: seventeen ledger sections and eighteen tags stand between the second `0.9.3` heading and its removal | `.github/scripts/fold_ledger.py:24` (and `tests/test_release_hygiene.py:1120`, `tests/test_the_ledger_fragments_fold_at_release.py:314`, the changelog fragment lines 6–7, fragment row F3's Notes) | open | executed — `awk 'NR>1673 && /^## [0-9]/'` over the ledger prints 17; `git tag --sort=v:refname` after `v0.9.3` prints 18 |
| ⬜ 2 | the hand-back's *two* doubled marker lines are twenty — 118 marker lines, 98 distinct — and the issue the orchestrator files should carry that number | `seal/specs/1790206437-a-second-fold-writes-a-second-heading/overview.md` §Not done, `phases/phase-5.md` §What this phase found, pull request #552 §Found outside the item | open | executed — `grep -c` and `sort -u \| wc -l` over the marker lines; the twenty pairs' line numbers are in the prose. Paperwork: out of `Needs a fix` |
| ⬜ 3 | two carriers outside phase 3's five phrases still say a held run always stays — the spec's *a re-seal records a second run rather than erasing the first* and the sealer's *never erases the record of the first* | `docs/review-chain-spec.md:342-343`, `agents/sealer.md:140-142` | open | read against `same_run` and `templates/sdd-round.md:39`; both rewordings keep the `GATE_CARRIERS` stands phrase. The smith may answer the sealer's with `kept_broad_gate`'s reading; the spec's has none |
| ⬜ 4 | the pull request body carries none of the four gate answers for the new `--check` arm, and `CONTRIBUTING.md` says the prompt budget is answered there or not at all | pull request #552 body | open | read — `CONTRIBUTING.md:186-190`; the orchestrator writes the body before ready. Out of `Needs a fix` |
| 🟢 | S1–S16 hold as the table above says; every new case was seen red, and I reproduced each red — the five fold cases against the base script, the seal case against the base generator, the split case with one carrier mutated | the four test modules the diff adds to | confirmed | executed, §Executed probes |
| 🟢 | the `--check` arm carries the four gate answers in code and in fragment F2: red on the real base ledger, blocks more, zero prompts, a line-shaped read with no path printed | `.github/scripts/fold_ledger.py:398-411`, fragment row F2 | confirmed | executed — the real-tree run over 9f846733's ledger |
| 🟢 | `insert` places entries before the next `## ` with one blank line each side on a dateless heading, a mid-file section and a heading-only file; no helper signature is touched by any finding, so step D rebases over nothing new | `.github/scripts/fold_ledger.py#insert` | confirmed | executed — three in-process probes |
| ❓ | the broad gate — the full suite, the repository-wide lint and the format check over the settled branch | the sealer's `broad-gate` run | ❓ out of verified scope | `agent-contract` §2 keeps it from this round; the sealer answers it, and its spawn comes due once this round's `Pass` is checked |

## Paste-ready fixes

```
ordinary shape, and the fold used to write a second `## X.Y.Z` heading for
it, below everything: `seal/ledger.md` headed `0.9.3` twice through the
seventeen releases from `0.9.4` to `0.15.0`.
```
```
    release-preparation commit (`4ac9bf35`), and the file carried both
    through seventeen releases while the ticket said nobody had run the
    fold twice. Seen red against that tree: `0.9.3 twice, at lines [1673,
    1764]`."""
```
```
    """#540. `seal/ledger.md` headed `0.9.3` twice through seventeen releases:
```
```
  and `seal/ledger.md` carried a second `## 0.9.3` from exactly that through
  seventeen releases while the ticket said nobody had run the fold twice.
```
```
the repair arrived seventeen releases after the instance
```
```
again, the cell keeps every run: the newest entry first, each `<sha> against
<base>`, the earlier ones behind it as `earlier run` — so a run at a new
commit, or at the same commit against another base, is recorded beside the
first rather than over it, while the same comparison taken again replaces
its own entry — and the reader still takes the first SHA-shaped word as the
run (#174).
```
```
sets that cell and leaves every other line of the file byte for byte as it
was — the new run written first, and a run the cell already held kept after
it as `earlier run` unless it is the same commit against the same base,
which the new entry replaces, so a second broad run at a new commit or
against another base never erases the record of the first (#174) — and
which refuses outright on three things — the last record's `Pass` box
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_release_hygiene.py tests/test_the_report_standard_is_one_in_three_places.py tests/test_no_real_identifiers.py tests/test_the_broad_gate_cell_keeps_every_run.py -q` in the clone | 109 passed, exit 0 |
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q -k same_run_re_seal_replaces` at the target | 1 passed, exit 0 |
| the same case with `9f846733:skills/code-review/scripts/round_record.py` swapped in, restored by `git checkout` | 1 failed (the stands half), exit 1 |
| `bin/test tests/test_the_ledger_fragments_fold_at_release.py -q -k "second_fold or kept_date or wherever_it_stands or heads_a_version_twice"` with `9f846733:.github/scripts/fold_ledger.py` swapped in, restored by `git checkout` | 5 failed, exit 1 |
| `bin/test tests/test_the_report_standard_is_one_in_three_places.py -q -k split_a_finding` with one word of the sentence changed in `docs/review-chain-spec.md`, restored by `git checkout` | 1 failed naming that carrier, exit 1 |
| `python3 .github/scripts/fold_ledger.py --check --root <scratch root holding git show 9f846733:seal/ledger.md>` | exit 1: `seal/ledger.md heads a version twice — one release, one section:` / `0.9.3  at lines 1673, 1764`; no backslash |
| `python3 .github/scripts/fold_ledger.py --check --root <the clone>` at 9f5902e5 | exit 1 on the fragment this branch carries — the expected state of a branch with a fragment; no doubled-version report |
| `doubled_versions` over the base ledger, in process; `" |
| `insert` in process over a dateless heading mid-file with three blank lines before the next `## `, a heading-only file without a trailing newline, and with one | entries before the next `## `, one blank line each side, no `\n\n\n`, one trailing newline in each |
| `grep -c '^&lt;!-- specs/[^ ]* -->$' seal/ledger.md` and the same through `sort -u \| wc -l` | 118 and 98 — twenty work items with their marker line twice |
| `awk 'NR>1673 && /^## [0-9]/' seal/ledger.md`; `git tag --sort=v:refname` from `v0.9.3` | 17 version sections after the `0.9.3` heading; 18 tags after `v0.9.3` |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` in the clone | exit 0; `total: 1686 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `python3 skills/evidence-check/scripts/correction_check.py --range 9f846733...HEAD` | exit 0 |
| `bin/survivor-check --range 9f846733...HEAD` | exit 0; 399 files examined against 30 removed sentences, no removed wording standing |
| `bin/test tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py -q` | 49 passed, exit 0 |
| `gh pr view 552 --json title,body,isDraft,baseRefName` | draft, base `release/v0.15.1`; the body carries no gate answers (⬜ 4) and says *two* marker lines (⬜ 2) |
| the broad gate — the full suite, the repository-wide lint and the format check | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| twenty work items stand with their marker line twice in `seal/ledger.md` (98 distinct of 118), and whether the fold should drop a fragment's own marker line from its body | a new issue — the smith's hand-back already sends it to the orchestrator to file; ⬜ 2 supplies the count | the repository owner, through the issue the orchestrator files |
