# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — review round 3

| Field | Value |
|---|---|
| Target SHA | 7adfec7b18ff4eac9503c70ab1388089cf01058d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 731 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `7adfec7b18ff4eac9503c70ab1388089cf01058d..7adfec7b18ff4eac9503c70ab1388089cf01058d`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is a verifying round and the run's last, since round 2 closed on fixes and spent the one reopening. It targets `7adfec7b` over round 2's fix range `a143af1d..5ffe4b95`. It was asked:
- whether round 2's four answers hold: ⬜ 10's moved note, ⬜ 11's changelog sentence, ⬜ 12's reason list and its pin, ⬜ 13's docstring route;
- whether the three re-reads that rode with ⬜ 12 hold;
- whether the corrected sentence in round 1's ⬜ 6 grounds is true.

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
| ⬜ 14 | The checklist's new clause writes `--` where its own paragraph and the rest of the file write an em dash, so the rendered checklist shows a double hyphen | `docs/release-checklist.md:342` | answered | Rung 1, answered with grounds and left unfixed: it is one character in a clause this branch wrote, and it renders as a literal `--` without changing what the checklist tells anyone to do. The reopening is spent, so a fix commit here would be read by no round; the em dash rides the next edit of that paragraph; Read: 25 ` — ` in the file, one ` -- `; came from round 2's paste-ready fix copying the log refusal's ASCII. Ships no defect |
| ❓ | What GitHub reports for the `seal` job when its `timeout-minutes` fires under the job-level `continue-on-error` (carried from round 2) | `.github/workflows/publish-release.yml:79` | ❓ out of verified scope | Nothing local runs a job timeout. The repository owner answers, from the first run that reaches one |
| ❓ | The `seal` job on GitHub's runners: Q11's font, Q9's browsers, and the suite at a tag push (carried from rounds 1 and 2) | `.github/workflows/publish-release.yml` | ❓ out of verified scope | The repository owner answers at 0.18.0's tag push, from the job log and the release page |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/release_seal.py:422` | round 1's 🔴 1 — fixed |
| round-1 | `.github/scripts/release_seal.py:428` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/dispatch.py:468` | round 1's 🟡 3 — fixed |
| round-1 | `.github/workflows/publish-release.yml:69` | round 1's 🟡 4 — fixed |
| round-1 | `.github/workflows/publish-release.yml:76` | round 1's 🟡 5 — fixed |
| round-1 | `.github/scripts/release_seal.py:445` | round 1's ⬜ 6 — answered |
| round-1 | `.github/scripts/release_seal.py:526` | round 1's ⬜ 7 — fixed |
| round-1 | `docs/release-checklist.md:343` | round 1's ⬜ 8 — fixed |
| round-1 | `.github/workflows/publish-release.yml:21` | round 1's ⬜ 9 — fixed |
| round-1 | `.github/scripts/release_seal.py#chain_counts` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/release_seal.py:549` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/run_tests.py#PILLOW` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py#MESSAGE_RESERVE` | round 1's 🟢 — confirmed |
| round-1 | `.github/workflows/publish-release.yml` | round 1's ❓ — out of verified scope |
| round-2 | `hooks/dispatch.py#describe` | round 2's 🟢 — verified |
| round-2 | `.github/scripts/release_seal.py:559` | round 2's 🟢 — verified |
| round-2 | `.github/workflows/publish-release.yml:20` | round 2's 🟢 — verified |
| round-2 | `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md` | round 2's 🟢 — verified |
| round-2 | `.github/scripts/release_seal.py` | round 2's 🟢 — verified |
| round-2 | `seal/releases/0.16.0.md:35` | round 2's ⬜ 10 — answered |
| round-2 | `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/changelog.md:11` | round 2's ⬜ 11 — answered |
| round-2 | `docs/release-checklist.md:341` | round 2's ⬜ 12 — fixed |
| round-2 | `.github/scripts/release_seal.py:45` | round 2's ⬜ 13 — fixed |
| round-2 | `.github/workflows/publish-release.yml:79` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
