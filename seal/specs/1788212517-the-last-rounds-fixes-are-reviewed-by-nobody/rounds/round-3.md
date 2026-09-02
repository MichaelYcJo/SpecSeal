# 1788212517-the-last-rounds-fixes-are-reviewed-by-nobody — review round 3

<!-- The verifying round that ended the run. Its target was the diff of round
2's fixes. It opened three things and none of them needed a fix, which is the
terminal condition `docs/review-chain-spec.md` states: a run ends at a round
that wrote no code nobody read. -->

| Field | Value |
|---|---|
| Target SHA | `f7cfbae` (the diff `2ea13da..f7cfbae`) |
| PR | not yet |
| Broad gate | `f28b95d`, against `origin/release/v0.0.2` — 958 passed, 1 skipped; `ruff check .` clean; `ruff format --check .` 60 files already formatted; `evidence_check` 28 ok · 0 drifted · 0 broken |
| Fixes checked by | no fixes to check |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 2's nine verdicts | `rounds/round-2.md` | answered — all nine closed | Seven confirmed by execution, two by reading. The site round 1 fixed and round 2 reopened was struck hardest and produced no new 🔴, so `docs/review-chain-spec.md:34-56`'s structure signal did not fire |
| 🟡 2 | A tab or a non-breaking space between the verdict word and its commit reopens a closed finding. The boundary set is a space and a comma, and nothing else | `chain_check.py:926` | answered — deferred with grounds | Verified by the orchestrator, executed: `fixed\tabc1234` and `fixed\xa0abc1234` both stay outside the vocabulary and count open. Round 1's `CITATION` cut on `\s+`, which covers both, so this spelling narrowed. **Fail-closed**, and outside this repository's house style — all 43 real verdict cells pass. Deferred rather than fixed: a third edit at this site after the last round would be the unreviewed final fix this whole work item exists to prevent |
| 🟡 3 | The comma boundary also runs the other way. `fixed, but reopened in round 3` reads as **closed**, and as a fix | `chain_check.py:926` | answered — deferred with grounds | Verified by the orchestrator, executed. This is the unsafe direction and it is the more serious of the two. The comma is there so `answered, and **sharpened** in \`96a1ae3\`` reads as `answered`, so narrowing it is a real design choice rather than a typo. Same site as 🟡 2 and deferred on the same grounds; both go to the follow-up together, because they are one line and one decision |
| 🟡 4 | `plan.md` still describes the deleted mechanism — *"see through … the commit citation after the word"* — where phase 10 in the same file records that `CITATION` was deleted | `plan.md:57-61` ↔ `:116` | answered — named, not fixed | Read. True as a description of the RESULT and false as a description of the mechanism, so it is the residue of a deleted vocabulary rather than round 1's 🔴 3 a fourth time. `plan.md:111` uses the same words legitimately: phase 5 is a chronicle of what that phase did. Left because editing it after the last round is the same unreviewed edit as 🟡 2 and 🟡 3 |
| ❓ 5 | A verifying round writing `fixed` in its own verdict cells has no legal value for `Fixes checked by`. Nothing says the last record's verdicts must be spelled `answered` | `skills/code-review/SKILL.md:196` · `templates/sdd-round.md` | answered — this record is the demonstration | Verified by the reviewer, executed, five combinations in a work item whose id equals `STRICT_FROM`: `fixed` beside `no fixes to check` exits 1, beside `nobody` exits 1, beside `round-4` exits 1; `answered` beside `no fixes to check` exits 0. It fails loudly rather than silently, so it self-corrects — but the next person writing one of these files pays for it once. **This file is written the way that passes**, and whether the rule should be documented goes to the follow-up |

## Executed probes

| What was run | Result |
|---|---|
| `verdict_of` on six spellings at `f7cfbae`, by the orchestrator | `fixed\tabc1234` · `fixed\xa0abc1234` → open (🟡 2). `fixed, but reopened in round 3` → `fixed`, closed **and** a fix (🟡 3). `answered, and sharpened in 96a1ae3` and `**answered** — round 2 closed at 8a5628a` → `answered`, not a fix |
| `verdict_of` on 40 spellings, by the reviewer | house style all closed; tab, NBSP, colon and a spaceless em dash all open |
| Every verdict cell in `specs/*/rounds/round-*.md` through the real `verdict_table` | 43 rows, 0 unrecognised, 0 table errors |
| Nine mutations on a copy, each asserted to have matched before running | The seven round 2 called red are red — the cutting regex restored (8 cases), whole-cell search (2), boundary removal (1), `mine[0]`, `theirs[0]`, squash path deleted, `>`. `VOCAB` sort removed and reversed are **green**, exactly as the smith disclosed |
| `PYTHONHASHSEED` 1–8 over `VOCAB` | the same order eight times — the ordering is deterministic and the defence is genuinely future-only |
| A protocol row renamed, its Required cell blanked, the row deleted | each time only `test_the_protocol_carries_the_field_as_a_row_of_its_table` goes red |
| A rule inverted in place vs. an opposite rule appended elsewhere | in place: 1 red. Appended: 72 green — matching what the comment at `tests/…:918-932` now claims, rather than what it used to claim |
| `.specseal/map.md` re-parsed per section header | 23 rows, 0 malformed, every `Checked` carrying a SHA |
| Five `round-3.md` shapes in a work item at `STRICT_FROM` | the table under ❓ 5 |
| **Broad gate**, once, at `f28b95d` | 958 passed, 1 skipped · `ruff check .` clean · `ruff format --check .` 60 files · `evidence_check` 28 ok · 0 drifted · 0 broken |

The branch was rebased onto `origin/release/v0.0.2` first and that **broke it**:
every commit was rewritten, so both earlier records' `Target SHA` values and
the ledger's stamps pointed at commits that no longer existed —
`test_ledger_stamps_resolve` went red and `chain_check` reported three
unreachable targets. `CLAUDE.md` says exactly this happens. The rebase was
undone and the release branch merged in instead, which preserves the SHAs the
records name. The broad gate above ran after that.

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1 and 2 | `chain_check.py` `verdict_of` and its boundary set | Round 1 fixed it, round 2 reopened it, round 3 found two more spellings on the same line. Three rounds have touched it and the next change here needs a reason, not a patch |
| rounds 1, 2 and 3 | `plan.md`, `spec.md`, `overview.md`, `README.md` | Prose outliving the code it describes, found in every round of this run |
| round 3 | `skills/code-review/SKILL.md:196` · `templates/sdd-round.md` | The last record's verdict spelling is load-bearing and undocumented |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The boundary set at `chain_check.py:926` is wrong in both directions — tab and NBSP reopen a closed finding, and `fixed, …` closes one that says it is not | a follow-up issue, with both directions and the executed evidence | the repository owner |
| Nothing documents that a verifying round's own verdict cells must not start with `fixed` | the same issue | the repository owner |
| `plan.md:57-61` describes the deleted mechanism | named here and in the pull request body; one line, no code | whoever next edits `plan.md` |
| Whether `evidence_check` should refuse a row whose cell count disagrees with its section header | issue #31, where rounds 1 and 2 also sent this file's coordinate drift | the repository owner |
| Q2, Q3, Q4 | `questions.md`. Q3 carries its first measurement and stays ⬜ | the repository owner |
