# 1788844127-the-reviewers-report-reaches-the-record-retyped — review round 3

| Field | Value |
|---|---|
| Target SHA | 89772db |
| Ran by | warden on claude-opus-5 |
| PR | 258 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 9, an edit is owed on agents/warden.md; but the run is capped, so it goes out as an issue rather than as a round 4 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A verifying round, spawned after round 2's fixes were committed and targeted at
the diff of those fixes: `eef8610..35ad9cd`, plus `89772db`, which only closes
round 2's record. Its job was stated as round 2's two open answers rather than
new findings, with one surface exempt — what the fix pass itself created. The
cap's last round, and it was told so.

Four checks, in the order the prompt set them.

1. **Round 2's 🟡 7 — does the replacement block send the marker to the right
   place?** Round 2 had measured that `NAME NOT IN TREE` in prose is refused at
   `NOT-IN-TREE` exit 2 while the same name inside a fence is 0 refused,
   because `claim_lines` reads a fence as a quotation. The round was asked to
   reproduce that measurement itself rather than take the number, then judge
   whether the new text stops the failure it names — a reviewer following it
   should put the marker on a prose line and never inside a paste-ready fix —
   and in particular to judge the added third paragraph about a real-looking
   domain outside the allowlist, for truth and for placement.
2. **Round 2's ⬜ 8 — is the corrected ground true?** `plan.md` and
   `overview.md` now say a narrower gate, guarded on the conventional path
   actually holding a file, needs no new record field, no template section and
   no checker, and passes all 41 cases at `b76ce68`. The round was told to
   measure the 41/41 claim, and that a correction is worse than the sentence it
   replaces if the new figure is wrong.
3. **The branch was red on its own broad gate, and this is the exempt
   surface.** `tests/test_the_rules_have_one_owner.py`'s
   `GENERATOR_NAMED[WARDEN]` pinned a sentence in `agents/warden.md` §6 that
   this branch had reworded, so the module was `1 failed` before any of round
   2's fixes; contract §2 reserves the broad gate for the orchestrator and this
   was the first time it ran. The round was asked to verify both halves — that
   the module is green and that the pin fails when the sentence it names
   changes — and then to answer the wider question **by construction**: are
   there other pins, in that module or any module, left behind by a sentence
   this branch moved? The enumeration was the point of the check, not the one
   instance already found.
4. **The two record corrections round 2 left standing** — its own ⬜ 7 and ⬜ 8,
   the reader-class count of nine and `record_files` being outside the class.

Carried as not the round's to close: the records-arm refusals and the ledger
re-verification, which the orchestrator takes at the closing commit;
`docs/flow.md`'s box; and the broad gate under contract §2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 7 | the reviewer warning's one worked example sent the exemption marker into a fenced paste-ready fix | `agents/warden.md:289` | answered | closed at `35ad9cd`. Executed — the asymmetry reproduces on my own probe: an invented underscored name in prose is refused at `NOT-IN-TREE`, exit 2, 1 refused; the same name inside a fence is 0 refused. The replacement scopes the scan to prose, says a fence is already exempt, forbids the marker there with the reason, and names the prose line as where it goes instead. The old example is gone rather than patched |
| ⬜ 8 | the recorded ground for deferring the report gate named a cost the narrow gate does not have | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/plan.md:69` | answered | corrected at `35ad9cd` in `plan.md` and `overview.md`. Executed at `b76ce68` — the unconditional gate is 36 failed / 5 passed of 41, and the same refusal guarded on the conventional path is 41 passed, exit 0. Also executed: the narrow gate is not inert — it refuses an uncommitted report at the convention and stays silent once it is committed |
| 🟡 9 | the whole of the text written to answer 🟡 7 is pinned by no case, one commit after the branch planted a pin for the same block | `agents/warden.md:289` | deferred #269 | #269 |
| ⬜ 10 | the identifier rule's second half sits two paragraphs from the rule, so *the same module* reaches back across a different tool, and *quote a URL* is narrower than `DOMAIN_RE`, which matches any bare host-shaped token | `agents/warden.md:295` | deferred #269 | #269 |
| ⬜ 11 | one line of the pasted correction was not re-wrapped: 90 columns in a paragraph otherwise at 74–78 | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/overview.md:60` | deferred #269 | #269 |

## Paste-ready fixes

```python
        (
            "marking one up corrupts it",
            "the fence rule is gone, and the block is back to the state "
            "round 2 found: an exemption marker illustrated inside the one "
            "region the checker reads as a quotation, where nothing reads it "
            "and the smith pastes it into the fix",
        ),
        (
            "a real-looking domain outside",
            "the identifier rule's second half is unstated, so a reviewer "
            "quoting a host meets the domain arm of the same module with no "
            "warning and no way through",
        ),
```
```
    pinned for that reason: the fixture user path, the evidence checker's own
    per-line exemption marker, the rule that the marker never goes inside a
    fence (round 2, 🟡 7 -- the block's first version illustrated it there,
    which is the one region the checker never reads), and the identifier
    rule's second half, the domain arm.
```
```markdown
turns `tests/test_no_real_identifiers.py` red at the pull request, after your
round has ended and where nobody can ask you what you meant. Name paths
relative to the repository root, and spell a user path `/Users/x/`. That
module has a second arm: any host-shaped token outside its allowlist fails
it, scheme or no scheme, so name a host only when the allowlist already
carries it and reach for `example.com` otherwise.
```
```markdown
The identifier rule has a second half as well: a real-looking domain outside
its allowlist fails the same module, so quote a URL only from a host that
allowlist already carries.
```
```markdown
measurement. **A gate that reaches every run needs `new` to record the path
it read, which is a new record field, a template section and a checker.**
That is a mechanism nobody has decided to build. **A narrower gate needs
none of it** — guarded on
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_rules_have_one_owner.py -q`, in a clone at `89772db` | 42 passed, exit 0 |
| the same module with `once` changed to `after` in the §6 sentence the warden pin names | 1 failed, 41 passed, exit 1 — `test_the_linking_carrier_names_the_generator` on the warden carrier alone |
| a probe markdown file under this work item naming an invented underscored name in prose, through `evidence_check.py --strict --ledger` | exit 2 — `NOT-IN-TREE` at that line, 77 names read · 1 refused, and the refusal names the marker |
| the same invented name backticked inside a fence and in a docstring inside that fence, same command | 76 names read · **0 refused**; exit 2 from the four drifted ledger rows, not the probe |
| round 1's unconditional `close` gate inserted after the target check at `b76ce68`, `bin/test` over the close module in a second clone | **36 failed, 5 passed** of 41, exit 1 |
| the same gate wrapped in a file test at the conventional report path, same commit, same module | **41 passed**, exit 0 (`$?` read directly) |
| a probe pair at `b76ce68`: `close` with an uncommitted report at the conventional path, then with the same report committed | 2 passed — refuses in the first, silent in the second. The narrow gate is not inert |
| both new paragraphs deleted from `agents/warden.md` §Report, `bin/test` over the six modules that read that file | **186 passed, exit 0** — nothing pins either paragraph |
| the left-behind-pin walk over every changed carrier read at `origin/release/v0.9.2` and at `89772db`, against every string constant under `tests/` | **0 literals** present at the baseline and gone at the target |
| the same walk with the target at `eef8610` | **exactly 1** — `tests/test_the_rules_have_one_owner.py:451`, gone from the whole tree. The enumeration seen finding the known instance |
| `bin/test` over the 28 modules that read one of the four changed carriers as document data | **857 passed**, exit 0 |
| `bin/test` over the three modules whose corpus is the committed round records | **122 passed, 1 skipped**, exit 0 |
| `wrote_fixes` and `run_reopened` called on round 1 and round 2 at `89772db`, and `stopping_floor` from round 1's floor row | round 2 is `wrote_fixes` `True` / `run_reopened` `False`; `stopping_floor` returns 0 errors, 0 notices as the records stand |
| a scratch repository carrying rounds 1 and 2 verbatim plus a synthetic round 3, `stopping_floor` from round 1's floor row, git driven from Python | round 3 closing on a fix: **1 error** naming it the second fix-closing record; round 3 closing `deferred #999`: **0 errors, 0 notices** |
| `evidence_check.py --strict --ledger seal/ledger/<this item>.md .` at `89772db`, probe removed | 10 ok · 4 drifted · 0 broken · 0 external · 0 old-format; records arm 0 refused. The drift is the orchestrator's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_finding_id_is_a_bare_integer.py:275` | round 1's 🟡 1 — fixed |
| round-1 | `agents/warden.md` §Report | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/SKILL.md` §And commit the record before commissioning the fixes | round 1's 🟡 3 — answered |
| round-1 | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:739` | round 1's ⬜ 6 — fixed |
| round-2 | `tests/test_a_finding_id_is_a_bare_integer.py:302` | round 2's 🟡 1 — answered |
| round-2 | `agents/warden.md:272` | round 2's 🟡 2 — answered |
| round-2 | `skills/code-review/SKILL.md:182` | round 2's 🟡 3 — answered |
| round-2 | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md:42` | round 2's ⬜ 4 — answered |
| round-2 | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md:60` | round 2's ⬜ 5 — answered |
| round-2 | `agents/warden.md:286` | round 2's 🟡 7 — fixed |
| round-2 | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/plan.md:69` | round 2's ⬜ 8 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 9 — the two paragraphs of `agents/warden.md` §Report written to answer round 2's 🟡 7 are pinned by no case (contract §14). The run is capped, so an issue rather than a fix; the paste-ready needles are in this record | a new issue, verdict `deferred #N` | the orchestrator, at the closing commit |
| ⬜ 10 — the identifier rule's second half is two paragraphs from the rule and its advice is narrower than the check. Same file and same block as 🟡 9, so the same issue carries it | the 🟡 9 issue | the orchestrator |
| ⬜ 11 — the un-re-wrapped line in `overview.md` | the closing commit, as a record correction | the orchestrator |
| a gate in `close` that survives the flag, in either form — and the narrow form also refuses a run that passed `--report` while a stale uncommitted file sits at the convention, which the record does not say | `overview.md` §*Not done*, unchanged by this round | the orchestrator |
| the four drifted ledger rows in this work item's fragment, one of them re-drifted by this fix range, and the unscoped ledger read | `seal/ledger/1788844127-the-reviewers-report-reaches-the-record-retyped.md` | the orchestrator, at the closing commit |
| `--asked` carrying the same defect `--report` had, and the two sibling files named in no shipped document | `questions.md` Q2 and Q3, opened by round 1 | the orchestrator |
| `docs/flow.md`'s `#228` box | `overview.md` §*Not verified* | the orchestrator |
