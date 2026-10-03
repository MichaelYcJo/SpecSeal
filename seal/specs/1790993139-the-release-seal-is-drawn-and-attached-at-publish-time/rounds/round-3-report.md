# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — round 3 report

Round 3 is the run's verifying round, and its last. It targets `7adfec7b`,
over round 2's fix range `a143af1d..5ffe4b95` (four commits) and the closing
commit `7adfec7b`, which closes round 2 and corrects one sentence in round 1's
⬜ 6 grounds. It was asked whether each of round 2's four answers holds, whether
the re-reads that rode along with ⬜ 12 (W4, 0.11.1 S9, 0.15.0 P1c) hold, and
whether the corrected sentence is true.

All four answers hold, the three re-reads hold, and the corrected sentence is
true. One new ⬜ sits in the text round 2's own paste-ready fix wrote: the
checklist's new clause uses `--` where the paragraph around it uses an em dash.
It ships no defect and needs no fix.

## Carried, not re-derived

- Round 2's executed results over the code that the fix range does not touch:
  the `chain_counts` guards, the `describe` caps and 564 / 972 / 1,378, the
  workflow's timeouts and `persist-credentials`, and 0.17.0's `(10, 27, 6, 12)`.
  The fix range changes one docstring paragraph in `release_seal.py`, one
  checklist box, one test case, the changelog fragment and ledger notes, so
  none of those results can have moved. Carried.
- Round 2's executed claim that line 77's G2 row still holds against
  `describe` (every gate in every group). This round checked only that the note
  now sits there. Carried.
- Round 1's base measurement for `MESSAGE_RESERVE`, carried by round 2. Carried.

## Round 2's answers

### ⬜ 10 — the `describe` note now sits on the row that cites `describe`

Executed, byte comparison of `seal/releases/0.16.0.md` across revisions.
Line 35, the changelog-gather and ledger-fold G2 row, is byte-identical at
`7adfec7b` to the line at round 1's target `28c807fc` and at `f118f7b5^`. It
cites no `dispatch.py` unit. So `3dbf7a1c` removed exactly the note round 1's fix
pass had put there, and nothing else on the row moved.

Line 77, the `stop` group's G2 row, cites `hooks/dispatch.py#describe`. Against
`28c807fc` it differs in two places only: the `describe` anchor re-stamped from
`@d3ccfe60` to `@3cb712c3` (round 1's fix pass), and the note, appended word for
word as round 2's paste-ready fix gave it. `evidence-check .` reads 0 drifted
and 0 broken. Confirmed.

### ⬜ 11 — the changelog states the Verdicts-cell rule

Read, `changelog.md:11-12`. The panel's last row is now *how many issues the
rounds' verdicts deferred (a deferral written only in a round record's
`## Deferred` table is not counted)*. That matches the `chain_counts` docstring
(*distinct issues named in a Verdicts cell whose verdict is `deferred`*) and the
code at `release_seal.py:470`, which collects `#N` from the Verdicts cell alone.
It also names the 0.17.0 case where the two counts differ (12 against 13).
The `## ` inside the code span sits mid-line, so the gather's
heading refusal does not read it as a heading. Confirmed.

The fix left one line at 87 columns where its neighbours wrap near 76
(`changelog.md:13`). Markdown renders it the same, so this is noted and not
raised.

### ⬜ 12 — the checklist's reasons match the refusal, and the pin is red without them

Read: the refusal at `release_seal.py:560-565` names three causes for a missing
table: edited after publication, went out without one, or the pull requests
moved between the two lists. The box at `docs/release-checklist.md:341-344` now
gives the same three under *the glance table was not in the note as generated*.

Executed: `test_the_checklist_box_says_where_a_missing_seal_is_explained` passes
at `7adfec7b`. Three mutations of the checklist, each alone and each restored,
turn it red:

- the checklist at `729c644e^` fails at `test_the_release_seal_is_drawn.py:907`;
- *published without one* removed fails at line 907;
- *the pull requests moved between the two lists* removed fails at line 908.

The case reads the box through `flat`, which joins whitespace, so the second
phrase is found across its line wrap. Confirmed.

### ⬜ 13 — the module docstring's by-hand route

Read, `release_seal.py:42-46`. The route now runs *from a checkout at the tag*
and ends at *shown with `gh release edit --notes-file`*. That agrees with the
checklist box's route (`docs/release-checklist.md:345-349`), which round 1's
⬜ 8 fixed. No case pins the docstring, and round 2 asked for none (*prose with
no reader to pin them*). Confirmed.

## The re-reads that rode along with ⬜ 12

All three rows re-anchor `docs/release-checklist.md#"## 6. After the merge"`
from `@c4138c25` to `@a4f4eacb`, and W4 also re-anchors the box case to
`@58ec83d1`. `evidence-check .` reads every anchor ok.

- **W4.** Its note says the box's reasons now match the refusal's three causes
  and *the box case pins two of them*. Read: the case pins *published without
  one* and *the pull requests moved*. No assertion in the box case pins the
  third cause, *edited before the job reached it*. So *two* is accurate. The
  claim (the box names the job, the `::warning::` line, the never-fails sentence
  and the by-hand route) is pinned by the case, which passes. Holds.
- **0.11.1 S9.** The claim is that §6 states the trigger and the input the
  tree has, and that `grep -n "on the tag"` returns nothing. Executed:
  `grep -c "on the tag" docs/release-checklist.md` prints 0 and exits 1. Read:
  `729c644e` changes four lines inside the release-note box and no trigger or
  input sentence. Holds.
- **0.15.0 P1c.** The claim is about the closer's paragraphs. Read: the same
  four lines are the whole of `729c644e`'s checklist edit, and none is in the
  closer's paragraphs. Holds.

## Round 1's corrected ⬜ 6 grounds

`7adfec7b` changes round 1's ⬜ 6 grounds from *0.17.0 reads 12 and the seal says
so* to *0.17.0 reads 12; the changelog states the rule since round 2's ⬜ 11
(corrected at `4ac391e0`)*. Read: round 2 showed the old clause false. The panel
reads `deferred 12 issues` and the alt text `12 issues deferred`, and neither
says which deferrals count. The new clause is true. `4ac391e0` is the commit
that edits `changelog.md`, and the sentence there states the rule (⬜ 11 above).
The row keeps its verdict word `answered`, and its `#` cell keeps `⬜ 6`.

Executed: `chain_check.py --baseline 233f0455` over the clone at `7adfec7b`
refuses for exactly two reasons. `Broad gate` is `not yet`, and `Pass` sits
beside `Fixes checked by: nobody`. The second is the field this round answers,
and the first is the sealer's. It raises no complaint about round 1's edited
row or about any verdict cell in either record.

## Stage 2 — what the fix range added

### ⬜ 14 — the checklist's new clause uses `--` where the paragraph uses an em dash

`docs/release-checklist.md:342`. `729c644e` wrote *the glance table was not in
the note as generated -- edited before the job reached it, …*. Three lines
above, the same paragraph writes *A missing title line is not one of them — it
falls back to the tag name*. The file uses ` — ` 25 times and ` -- ` only here.
GitHub renders `--` literally, so the release checklist shows a double hyphen
in the one sentence this run added. The `--` came from round 2's paste-ready
fix, which copied the refusal's ASCII. The refusal prints to a log, where
ASCII is right. The checklist is rendered prose.

The behaviour and the fact are both right, and only the punctuation reads
badly. So this is ⬜, and `Needs a fix` does not count it. If the run takes
it, the change is one character, and the box case does not read that
character, so no pin moves.

## Regression tests to plant

None. ⬜ 14 is punctuation, and nothing should pin it.

## Facts for the evidence ledger

None new. The re-reads above confirm rows the fix pass already wrote.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 10 is closed — the `describe` re-read note sits on the `stop` group's G2 row, which cites `describe`, and the changelog-gather G2 row is back to its bytes at `28c807fc` | `seal/releases/0.16.0.md:77` | confirmed | Executed: line 35 byte-identical to `28c807fc`; line 77 differs only by the re-stamped `describe` anchor and the note; `evidence-check .` 0 drifted, 0 broken |
| 🟢 | round 2's finding 11 is closed — the changelog says the row counts issues a Verdicts cell defers and that a `## Deferred` table alone is not counted | `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/changelog.md:11` | confirmed | Read: agrees with the `chain_counts` docstring and `release_seal.py:470` |
| 🟢 | round 2's finding 12 is closed — the checklist box gives the refusal's three causes, and the box case pins two of them | `docs/release-checklist.md:341` | confirmed | Executed: the case passes; red with the checklist at `729c644e^` and with each new phrase removed alone |
| 🟢 | round 2's finding 13 is closed — the docstring's by-hand route starts at a checkout at the tag and ends at `gh release edit --notes-file` | `.github/scripts/release_seal.py:45` | confirmed | Read: agrees with the checklist's route; no pin asked for |
| 🟢 | the re-reads of W4, 0.11.1 S9 and 0.15.0 P1c hold against `729c644e` | `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md` | confirmed | Executed: `evidence-check .` exit 0; S9's grep prints 0. Read: the edit is four lines inside the release-note box; W4's *two of them* is accurate |
| 🟢 | round 1's ⬜ 6 grounds now say the changelog states the rule since `4ac391e0`, in place of the false *the seal says so* | `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/rounds/round-1.md:39` | confirmed | Read: `4ac391e0` is the changelog commit, and the sentence there states the rule. Executed: `chain_check.py` raises nothing about either record's verdict rows |
| carried | round 2's executed results over the code the fix range does not touch (the `chain_counts` guards, the `describe` caps and 564 / 972 / 1,378, the workflow lines, 0.17.0's `(10, 27, 6, 12)`) | `.github/scripts/release_seal.py#chain_counts` | carried, not re-derived | The fix range touches no code under them: one docstring paragraph, one checklist box, one test case, prose and ledger notes |
| ⬜ 14 | The checklist's new clause writes `--` where its own paragraph and the rest of the file write an em dash, so the rendered checklist shows a double hyphen | `docs/release-checklist.md:342` | open | Read: 25 ` — ` in the file, one ` -- `; came from round 2's paste-ready fix copying the log refusal's ASCII. Ships no defect |
| ❓ | What GitHub reports for the `seal` job when its `timeout-minutes` fires under the job-level `continue-on-error` (carried from round 2) | `.github/workflows/publish-release.yml:79` | ❓ out of verified scope | Nothing local runs a job timeout. The repository owner answers, from the first run that reaches one |
| ❓ | The `seal` job on GitHub's runners: Q11's font, Q9's browsers, and the suite at a tag push (carried from rounds 1 and 2) | `.github/workflows/publish-release.yml` | ❓ out of verified scope | The repository owner answers at 0.18.0's tag push, from the job log and the release page |

## Paste-ready fixes

### ⬜ 14 (optional; not counted in Needs a fix)

```
      suite at the tag did not pass, a `gh` call failed, or the glance
      table was not in the note as generated — edited before the job
      reached it, published without one, or the pull requests moved
      between the two lists. That job never fails the release.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_release_seal_is_drawn.py -q` in the clone at `7adfec7b` | 45 passed, exit 0 |
| The box case alone, then against three checklist mutations, each restored (a one-file probe, deleted) | baseline passed; checklist at `729c644e^` failed at line 907; *published without one* removed failed at 907; *the pull requests moved between the two lists* removed failed at 908; clone clean afterwards |
| Byte comparison of `seal/releases/0.16.0.md` lines 35 and 77 at `28c807fc`, `f118f7b5^` and `7adfec7b` | line 35 identical; line 77 differs by the `describe` re-stamp and the note only |
| `bin/evidence-check .` over the clone | exit 0; total 3684 ok, 0 drifted, 0 broken |
| `bin/correction-check --range 233f0455...HEAD` over the clone | exit 0; no merge commit in the range |
| `chain_check.py --baseline 233f0455 --root .` over the clone | exit 1, for two reasons only: `Broad gate` is `not yet`, and `Pass` beside `Fixes checked by: nobody`; nothing about either record's verdict rows |
| `grep -c "on the tag" docs/release-checklist.md` | 0, exit 1 |
| The broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle; nothing this round leaves open stands in its way, so the sealer's spawn is what comes due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, at `7adfec7b` in the clone or the worktree:

- `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/rounds/round-2.md`, `round-2-report.md`; `round-1.md` through the fix diff
- `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/changelog.md`
- `.github/scripts/release_seal.py` lines 30-50 and 540-575, and its `deferred` lines
- `docs/release-checklist.md` lines 330-352
- `tests/test_the_release_seal_is_drawn.py` lines 859-908
- `seal/releases/0.16.0.md` lines 35 and 77, `seal/releases/0.11.1.md` line 23, `seal/releases/0.15.0.md` line 35, and the work item's ledger fragment, line 23
- `skills/code-review/scripts/chain_check.py`, its header and `main`
