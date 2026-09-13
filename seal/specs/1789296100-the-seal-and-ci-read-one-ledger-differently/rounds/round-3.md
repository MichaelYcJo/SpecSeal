# 1789296100-the-seal-and-ci-read-one-ledger-differently — review round 3

| Field | Value |
|---|---|
| Target SHA | a5fa14bac2ea877864a5ad54363ddd51a3056447 |
| Ran by | warden on claude-opus-5 |
| PR | 378 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

A verifying round with a scope of one commit: `ae5b935..6730690`, three paragraphs re-wrapped in three files. Round 2 opened nothing needing a fix; it graded that unwrapping ⬜ and deliberately kept it off the fix list, and the orchestrator fixed it anyway because a changelog fragment is concatenated verbatim at the release and that line would have reached `CHANGELOG.md`. That made it round 2's one commissioned fix, and this round is what reads it.

Rounds 1 and 2 are inherited. The reviewer was told the expected outcome is "nothing" and that reaching for something to say is the failure mode here.

**It opened nothing.** Four checks, all executed: the words are unchanged — the three files taken at both commits with whitespace normalised give three empty diffs, so only line breaks moved; nothing else moved in the commit — three files, 9 added and 9 removed; the changelog bullet still reads as a changelog entry, its marker, its two-space indent and its trailing `(#354)` intact; and the split repair is genuine, checked in both directions rather than taken from the prompt — `6730690` is not an ancestor of `ae5b935`, `ae5b935` holds only three files under `rounds/` and therefore none of the re-fold, and `chain_check` against `release/v0.11.3` emits no `written_late` line for `round-2.md`.

**One ⬜, recorded with the instruction not to fix it.** The re-fold did not flow to the end of two paragraphs, leaving a 40-column line at `changelog.md:8` and a 31-column line at `spec.md:10` mid-paragraph. Both render identically and neither path is in `test_docs_line_wrap.py`'s `COVERED`, so nothing goes red. Fixing it would cost a commit and one more verifying round and change nothing anybody sees — which is the arithmetic the orchestrator got wrong one round earlier, and the reviewer applied it correctly here. Left as a note for whoever next edits those paragraphs.

What `chain_check` still reports is this record closing round 3's own cell, and the `Broad gate` cell, which is the sealer's. Neither is a defect in the reviewed commit. The rounds have settled.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 2's finding 10 is fixed: the three paragraphs were re-wrapped and no word moved | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/changelog.md` · `overview.md` · `spec.md` | answered | executed — each file at `ae5b935` against the same file at `6730690` with whitespace collapsed, all three diffs empty; `git show --stat` is three files, 9 insertions and 9 deletions, nothing else |
| 2 | The changelog bullet still reads as a changelog entry after the re-wrap | `…/changelog.md:4-21` | answered | read — words, `- **…**` lead, two-space continuation indent and the trailing `(#354)` all unchanged; it is the file that is concatenated verbatim at the release, so it was read whole |
| 3 | The `written_late` repair is genuine: the record commit does not contain the fix and does not descend from it | `ae5b935` · `6730690` | answered | executed — `git merge-base --is-ancestor 6730690 ae5b935` exits 1 and the reverse exits 0, read directly; `git show --name-only ae5b935` is three `rounds/` files and no re-wrapped path; `chain_check.py --baseline release/v0.11.3` prints no `written_late` line for `round-2.md` |
| 4 | The commit message's "nothing went red" is true for the reason it gives | `tests/test_docs_line_wrap.py` `COVERED` | answered | read — the list carries no `seal/specs/` path and no `CHANGELOG.md`; round 2 had already run the module at 23 passed and the fix cannot change the list |
| 5 | `round-2.md` describes the edit `6730690` actually made, and its `Contract changes` and `New units` cells hold | `…/rounds/round-2.md` | answered | read — the narrative names the same three re-folded paragraphs, row 10 carries `fixed` and the commit, and the commit adds no unit and touches no contract surface |
| 6 | ⬜ The fold was not cascaded: a 40-column line remains mid-paragraph in `changelog.md` and a 31-column line in `spec.md` | `…/changelog.md:8` · `…/spec.md:10` | open | executed — column widths measured per line at both commits: `overview.md` cascaded to 74/78/76/67, `changelog.md` moved its orphan from 30 columns to 40, `spec.md` replaced a 101-column line with a 31-column one. A correction only; nothing renders differently and no check covers either path |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `git show --stat ae5b935..6730690` | three files — `changelog.md`, `overview.md`, `spec.md` under the work item — **9 insertions, 9 deletions**. Nothing else moved |
| Each of the three files at `ae5b935` against the same file at `6730690`, every run of whitespace collapsed to one space | **all three diffs empty.** The re-wrap changed line breaks and no word |
| Per-line display widths of the three paragraphs at both commits | `overview.md` 74/78/76/67, cascaded clean; `changelog.md` orphan moved 30 → 40 columns; `spec.md` 101-column line replaced, 31-column line left at line 10 |
| `git merge-base --is-ancestor 6730690 ae5b935` and the reverse | **exit 1** and **exit 0**, read directly. The record commit is the fix commit's parent, so the adding commit does not descend from the fix |
| `git show --name-only ae5b935`, and `git show --stat ae5b935` restricted to the three re-wrapped paths | three `rounds/` files; the restricted form returns **nothing**. The record commit does not contain the fix |
| `chain_check.py --baseline release/v0.11.3 --root .` | **exit 1**, read directly. **No `written_late` line for `round-2.md`** — the arm that refused the first attempt is quiet. The two messages printed are `Broad gate` is `not yet` and `Pass` beside `Fixes checked by: nobody`, which the sealer and this round's record close |
| `git merge-base --is-ancestor bc70e7d HEAD` | **exit 0** — `round-2.md`'s `Target SHA` is reachable from HEAD, so the reachability line above it is the requirement being stated and not a failure |
| `git status --porcelain` at the start, and again after every command | **empty each time.** Every command was read-only; no file was written inside the repository except this report |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It has not been taken at any SHA on this branch and it is not this round's to take (contract §2). This round opens nothing needing a fix, so it is what comes due next: the sealer's spawn, not a run for the session reading this to assemble |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:251` · `skills/verify/scripts/broad_gate.py:590` | round 1's 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:65` · `seal/ledger.md:63,71,81,143` | round 1's 2 — fixed |
| round-1 | `agents/framer.md:91` · `tests/test_chain_hooks_hardening.py:1014` | round 1's 3 — deferred |
| round-1 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md` | round 1's 4 — fixed |
| round-1 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md:138` | round 1's 5 — fixed |
| round-1 | `spec.md:83` · `skills/evidence-check/SKILL.md:178` · `CONTRIBUTING.md:21` | round 1's 6 — fixed |
| round-1 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/phases/phase-1.md` | round 1's 7 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1723` · `:2423` · `CONTRIBUTING.md:21` | round 1's 8 — fixed |
| round-1 | `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` | round 1's 9 — fixed |
| round-2 | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` · `skills/verify/scripts/broad_gate.py` | round 2's 1 — answered |
| round-2 | `seal/follow-up.md` §*Schedulable items with nowhere else to go* | round 2's 2 — answered |
| round-2 | same file, §*Where spec and implementation diverged* | round 2's 4 — answered |
| round-2 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md` | round 2's 5 — answered |
| round-2 | `skills/evidence-check/SKILL.md` · `CONTRIBUTING.md` · `spec.md` | round 2's 6 — answered |
| round-2 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/phases/` | round 2's 7 — answered |
| round-2 | `skills/evidence-check/SKILL.md` · `CONTRIBUTING.md` | round 2's 8 — answered |
| round-2 | `spec.md:8` · `overview.md:11` · `changelog.md:7` | round 2's 10 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `round_record.py`'s `fix_table` cuts the SHA out of the middle of its own code span, so row 10 of `round-2.md` reads `fixed at 6730690 — ``;`. **Already ridered** and already named in round 2's Deferred table so it is not re-reported as new. Listed here only to say it was seen again and left alone | the existing rider on that function | the repository owner |
| Whether `broad-gate`'s own end-to-end run shows the notice absent at exit 2 | `overview.md` §*Not verified*. Already deferred by this branch | the sealer |
| `ANCHOR_RE` drops a coordinate it cannot parse instead of naming it | `seal/follow-up.md` §*Schedulable items with nowhere else to go*. Already deferred, and round 2 confirmed the row's count | the repository owner |
| The framer / overview-case contradiction | #379. Already deferred by round 1's fix pass | the repository owner |
