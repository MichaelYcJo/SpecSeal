# Round 1 report — 1790206437-a-second-fold-writes-a-second-heading

| Field | Value |
|---|---|
| Target SHA | 9f5902e5 |
| Base | `release/v0.15.1` (9f846733) |
| Scope | whole branch, `fix/540-a-second-fold-writes-a-second-heading`, pull request #552 (draft) |
| Reviewed in | a `git clone --no-local` of the worktree at the target SHA; nothing was written in the worktree but this file |
| Earlier rounds | none |

The branch does what the three tickets ask, every new case was seen red and
I reproduced each red myself, and the code paths I probed beyond the cases
hold. Nothing here crashes or loses a record. What I opened is one false
count that reached five carriers, and three corrections to paperwork and
prose.

## Stage 1 — spec compliance

Read against `spec.md` §User scenarios, `plan.md` §Phases and the four
answers `CONTRIBUTING.md` §*What a change to a gate must carry* asks of the
new `--check` arm.

| Scenario | What I found | How |
|---|---|---|
| S1 the repair | `seal/ledger.md` heads `0.9.3` once, at line 1673; `1788890000`'s marker and `###` stand under it after `1788873640`'s rows with one blank line between; the ledger diff against the base is 15 insertions and 17 deletions, of which the two content deletions are the heading and its blank and the rest are re-stamped rows | executed — `grep -n "^## 0.9.3"`, a read of lines 1760–1768, `git diff -U0` |
| S2 the real-tree case | `test_no_version_heads_two_sections_of_this_ledger` reads `seal/ledger.md` through `duplicated_version_headings`; over the base ledger the script's own reader returns `[('0.9.3', [1673, 1764])]`, which is the red the phase-1 record copied | executed — the reader over `git show 9f846733:seal/ledger.md` |
| S3–S8 the join, the kept date, the placement, the dry run, the message, the refusal | the five new cases in the fold module pass at the target and all five fail against the base script swapped in | executed — 5 failed against 9f846733's script, 48 passed at the target |
| S5 the date line | `date = args.date or …` is byte-identical to the base; the kept date is `insert` dropping the block's heading and `main` printing the file's own | read — the diff; the phase-2 mutation record says the override was dead, and the code agrees: `date` reaches nothing but the block heading `insert` drops |
| S8 the real tree | `fold_ledger.py --check --root <scratch copy of 9f846733's ledger>` exits 1 with `0.9.3  at lines 1673, 1764` and the one-release-one-section line; no backslash in the output | executed |
| S9 the documents | the module docstring names the join under `--version`, the doubled-heading refusal under `--check` and in the exit-code paragraph; `docs/release-checklist.md` §2 gained the one sentence | read |
| S10 the written comment | the seal case passes at the target and fails against the base generator swapped in, on the stands half | executed — 1 failed, then 1 passed |
| S11 the docstring | `kept_broad_gate`'s count sentence is the round-3 report's block; the body is unchanged | read — the diff hunk at `round_record.py:362-370` |
| S11b the class | the handoff protocol's `Broad gate` row and the orchestration skill's two sealer sentences state the same-commit-same-base replace in one clause each; `GATE_CARRIERS`' stands phrases survive and the cell module passes | read, and executed (the cell module in the narrow run). ⬜ 3 below: the phrase enumeration stopped short of two more carriers |
| S12 A11 | the clause reads *was a code comment no test pinned* with a `**Corrected 2026-09-24**` note naming S10's case; the anchors resolve | read; `evidence-check --strict .` exit 0 |
| S13 the convention | `SPLIT_AT_TWO_DEPTHS` is one text in the three `REVIEWER_CARRIERS`; the case fails with one word changed in `docs/review-chain-spec.md` | executed — 1 failed with the mutation, 7 passed restored |
| S14 nothing else moves | `depth_two`, `same_run`, `kept_broad_gate`'s body, `gather_changelog.py`, `fragments`, `demote`, `marker`, `is_marked`, `open_rows`, `append`: unchanged in the diff. `skills/code-review/orchestration.md` changed by two clauses, recorded as a divergence in `overview.md` — S11b named it and the unchanged list was wrong by one file, which the phase-3 record says | read — `git diff --stat` and the hunks |
| S15 the ledger stays true | `evidence-check --strict .`: `1686 ok · 0 drifted · 0 broken`; `correction-check --range 9f846733...HEAD` exit 0 | executed |
| S16 the branch's sweep | `survivor-check --range 9f846733...HEAD`: 399 files, 30 removed sentences, nothing standing, exit 0 | executed |

**The four gate answers for the `--check` arm** (`CONTRIBUTING.md`
§*What a change to a gate must carry*): seen red — reproduced above over
the real base ledger; failure direction — the arm only adds an exit 1, so
the gate blocks more, and a wrong deny costs a release pull request one
hand edit that `--check`'s output spells out; prompt budget — zero, the arm
prints and exits; platform honesty — a line-shaped read over `\n` with no
path printed, and the case asserts no backslash. All four hold in the
code and in fragment row F2. What is missing is where `CONTRIBUTING.md`
says the prompt budget is answered — the pull request body — which is ⬜ 4.

**Judgments the tree answered, checked.** Judgment 1 (the premise is
measured): confirmed, the base ledger heads `0.9.3` twice. Judgment 4
(two deleted lines): confirmed. Judgment 9 (the date line): confirmed
byte-identical. Judgment 10 (five carriers): the count is short, ⬜ 3.
Q1 stands as the owner answered it and I did not reopen `depth_two`.

## Stage 2 — quality

### 🟡 1 · *for six releases* is a count nothing measured, and it is false in five places

`.github/scripts/fold_ledger.py:24` says `seal/ledger.md` headed `0.9.3`
twice *for six releases*. The second heading was written by `4ac9bf35` on
2026-09-09 and stood until this branch removed it after `9f846733`
(v0.15.0). Between those, the ledger holds seventeen version sections
(`0.9.4` through `0.15.0`, line 1673 onward) and git holds eighteen tags
after `v0.9.3` (`v0.13.2` has no ledger section). No reading of *release*
gives six. The same phrase stands in `tests/test_release_hygiene.py:1120`,
`tests/test_the_ledger_fragments_fold_at_release.py:314`, the changelog
fragment `seal/specs/1790206437-a-second-fold-writes-a-second-heading/changelog.md:6-7`
and fragment row F3's Notes (*the repair arrived six releases after the
instance*), so it reaches `CHANGELOG.md` and `seal/ledger.md` at the
release. This is the shape `agent-contract` §5 names — an aggregate that is
not a coordinate — and the frame's measured-state table carried the
commit and the date but never a release count, so the number arrived in
phase 1 unsourced. 🟡 rather than ⬜ because the fact is wrong, not the
sentence, and it ships in two release-facing files.

### ⬜ 2 · the doubled marker lines are twenty, not two

`overview.md` §Not done, `phases/phase-5.md` and the pull request body say
`1790173106`'s and `1790174138`'s marker lines stand twice and `--check`'s
118 is *two above* the folded sections. Measured at the target:
`seal/ledger.md` carries 118 marker lines on a line of their own and 98
distinct ones — twenty work items stand with their marker line twice, at
lines 1214/1217, 1258/1261, 1332/1335, 1369/1372, 1397/1400, 1433/1436,
1524/1527, 1588/1591, 1627/1630, 1773/1776, 1793/1796, 2522/2525,
2549/2552, 2568/2571, 2599/2602, 2615/2618, 2635/2638, 2656/2659,
2675/2678 and 2701/2704. Eleven are 0.8.x–0.9.x sections and nine are
0.13.x–0.15.0, so a fragment beginning with its own marker line was the
ordinary shape for two stretches, not a slip of two neighbours. Paperwork
under `seal/specs/`, so a correction and out of `Needs a fix` — but the
orchestrator is about to file an issue with the number in the hand-back,
and the number to file it with is twenty, 98 distinct of 118.

### ⬜ 3 · two more carriers state the rule `same_run` replaced

Phase 3 enumerated #542's class by five phrases (*taken again*, *stays
behind*, *earlier one stays*, *count of runs*, *count of entries*) and
closed it at five carriers. Two sentences carry none of those phrases and
state the same claim the handoff protocol's row was reworded for — that a
held run always stays:

- `docs/review-chain-spec.md:342-343`: *so a re-seal records a second run
  rather than erasing the first*. A re-seal is the sealer run again over an
  unchanged checkout, which is the very case `same_run` was written for,
  and there it replaces the entry rather than recording a second run.
- `agents/sealer.md:140-142`: *a run the cell already held kept after it as
  `earlier run`, so a second broad run never erases the record of the
  first*. Unconditional; true of a run at a new commit or against another
  base, and not of the same comparison taken again.

`kept_broad_gate`'s docstring reads the sealer's sentence as the promise
for the other-base case, so the smith may answer with that reading; the
spec sentence has no such reading. Both rewordings below keep the
`GATE_CARRIERS` stands phrase `earlier run` and reintroduce neither gone
phrase. Prose, behaviour right: ⬜.

### ⬜ 4 · the pull request body carries none of the four gate answers

`CONTRIBUTING.md` §*What a change to a gate must carry* ends: *the prompt
budget … is answered in the pull request body or it is not answered*. The
body of #552 names the `--check` refusal and nothing of the four answers.
They are in fragment F2's Notes; the body is where the contribution rule
reads them. The orchestrator writes the body, so this is theirs at the
moment the draft is marked ready, and it is out of `Needs a fix`.

### What I probed beyond the cases and found sound

- `insert` over a heading with no date, over a section standing mid-file
  with three blank lines before the next `## `, and over a file that is a
  heading alone with and without a trailing newline: the entries land
  before the next `## `, one blank line each side, no run of three
  newlines, and the file ends in one newline. Step D (#547) can build on
  the three helpers as they stand: no finding here touches a signature.
- `doubled_versions` and the hygiene reader agree over the base ledger;
  the ledger carries no U+2028 and no `\r`, so the two readers' line
  numbers cannot diverge on this tree today (they would on a row holding
  U+2028, the hygiene reader using `splitlines()` — a limit of #289's
  reader, not of this branch).
- `--check` at the target exits 1 on the fragment this branch carries,
  which is the expected state of a feature branch; the hand-back's *this
  tree exit 0 (118 marked)* was phase 2's measurement, before phase 5
  wrote the fragment.

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
| `doubled_versions` over the base ledger, in process; `" " in text`, `"\r" in text` | `[('0.9.3', [1673, 1764])]`; False, False |
| `insert` in process over a dateless heading mid-file with three blank lines before the next `## `, a heading-only file without a trailing newline, and with one | entries before the next `## `, one blank line each side, no `\n\n\n`, one trailing newline in each |
| `grep -c '^&lt;!-- specs/[^ ]* -->$' seal/ledger.md` and the same through `sort -u \| wc -l` | 118 and 98 — twenty work items with their marker line twice |
| `awk 'NR>1673 && /^## [0-9]/' seal/ledger.md`; `git tag --sort=v:refname` from `v0.9.3` | 17 version sections after the `0.9.3` heading; 18 tags after `v0.9.3` |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` in the clone | exit 0; `total: 1686 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `python3 skills/evidence-check/scripts/correction_check.py --range 9f846733...HEAD` | exit 0 |
| `bin/survivor-check --range 9f846733...HEAD` | exit 0; 399 files examined against 30 removed sentences, no removed wording standing |
| `bin/test tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py -q` | 49 passed, exit 0 |
| `gh pr view 552 --json title,body,isDraft,baseRefName` | draft, base `release/v0.15.1`; the body carries no gate answers (⬜ 4) and says *two* marker lines (⬜ 2) |
| the broad gate — the full suite, the repository-wide lint and the format check | not yet |

Every swap above was restored with `git checkout` and `git status --short`
read empty afterwards; the scratch ledger copy was deleted; the clone's
`.venv` is `bin/test`'s own and stays.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| twenty work items stand with their marker line twice in `seal/ledger.md` (98 distinct of 118), and whether the fold should drop a fragment's own marker line from its body | a new issue — the smith's hand-back already sends it to the orchestrator to file; ⬜ 2 supplies the count | the repository owner, through the issue the orchestrator files |

## Paste-ready fixes

### 🟡 1

`.github/scripts/fold_ledger.py:23-24`, the module docstring:

```
ordinary shape, and the fold used to write a second `## X.Y.Z` heading for
it, below everything: `seal/ledger.md` headed `0.9.3` twice through the
seventeen releases from `0.9.4` to `0.15.0`.
```

`tests/test_release_hygiene.py:1119-1121`, the docstring:

```
    release-preparation commit (`4ac9bf35`), and the file carried both
    through seventeen releases while the ticket said nobody had run the
    fold twice. Seen red against that tree: `0.9.3 twice, at lines [1673,
    1764]`."""
```

`tests/test_the_ledger_fragments_fold_at_release.py:314`, the docstring's
first line:

```
    """#540. `seal/ledger.md` headed `0.9.3` twice through seventeen releases:
```

`seal/specs/1790206437-a-second-fold-writes-a-second-heading/changelog.md:6-7`:

```
  and `seal/ledger.md` carried a second `## 0.9.3` from exactly that through
  seventeen releases while the ticket said nobody had run the fold twice.
```

Fragment row F3's Notes, the last clause:

```
the repair arrived seventeen releases after the instance
```

### ⬜ 3

`docs/review-chain-spec.md:341-344`:

```
again, the cell keeps every run: the newest entry first, each `<sha> against
<base>`, the earlier ones behind it as `earlier run` — so a run at a new
commit, or at the same commit against another base, is recorded beside the
first rather than over it, while the same comparison taken again replaces
its own entry — and the reader still takes the first SHA-shaped word as the
run (#174).
```

`agents/sealer.md:139-142`:

```
sets that cell and leaves every other line of the file byte for byte as it
was — the new run written first, and a run the cell already held kept after
it as `earlier run` unless it is the same commit against the same base,
which the new entry replaces, so a second broad run at a new commit or
against another base never erases the record of the first (#174) — and
which refuses outright on three things — the last record's `Pass` box
```

### ⬜ 2 and ⬜ 4

Paperwork and the pull request body; the numbers and the four answers are
in the prose above and need no fence.

Needs a fix: yes — 🟡 1, the *six releases* count in five carriers
Loses a record or crashes: no

## Proof

- executed — the narrow modules, the three red reproductions, the real-tree `--check`, the in-process `insert` and `doubled_versions` probes, the marker and release counts, `evidence-check --strict`, `correction-check`, `survivor-check`, the line-wrap and one-word modules, `gh pr view 552`
- read — `.github/scripts/fold_ledger.py` (whole), `.github/scripts/gather_changelog.py#section_heading`/`#existing_date`/`#insert`, the diff of every file the branch touches against 9f846733, `tests/test_the_ledger_fragments_fold_at_release.py:1-200` and the new cases, `tests/test_release_hygiene.py:1076-1130`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:2611-2634`, `tests/test_the_report_standard_is_one_in_three_places.py:20-110`, `tests/test_the_broad_gate_cell_keeps_every_run.py:23-93`, `agents/sealer.md:130-190`, `docs/review-chain-spec.md:336-348` and `:1623-1633`, `CONTRIBUTING.md:160-190`, `seal/ledger.md` at the `0.9.3` region, A9, A11 and every `Re-read 2026-09-24 by work item 1790206437` note, `seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md`, and under the work item `routing.md`, `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`, `phases/phase-1.md` through `phase-5.md`
- unverified — the broad gate: the sealer
