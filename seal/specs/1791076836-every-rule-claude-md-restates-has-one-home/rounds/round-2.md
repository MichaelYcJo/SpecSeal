# 1791076836-every-rule-claude-md-restates-has-one-home — review round 2

| Field | Value |
|---|---|
| Target SHA | e49839ec2fb28425c8ffe4e2f56de85817396dc9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #767 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item `1791076836-every-rule-claude-md-restates-has-one-home` (#730, PR #767). This is the verifying round for round 1's fixes, `8a0e440b..0be7deb4`.

Open each fix and judge whether each round-1 verdict is closed:
- 🟡1: the generated-block strip moved from `words` to `tree` and now applies to `CLAUDE.md` alone. `BASELINE` gains `agents/smith.md` ↔ the block template at 13.
- 🟡2: `agents/warden.md` now cites `CONTRIBUTING.md`, and `LINKED` and `CARRIERS` hold it. The pass grepped every spelling of the four rules to close the class.
- ⬜3: the comment.
- ⬜4: the distinct-window counts.

The one new unit, `test_a_paste_into_the_block_template_is_named` (depth 1), is a finding surface. Also judge the two `Re-read ·` rows the pass wrote for 0.8.1 R7 and 0.9.2 S3.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The comment calls *go in one batch (emphasised) before the first edit* verbatim from `CLAUDE.md`'s goal sentence, which emphasised the whole phrase at every commit from #44 to #730 | `tests/test_chain_hooks_hardening.py:917` | open | Read: `git show fd71605:CLAUDE.md` and the base both carry the whole phrase in emphasis; the case does not depend on the spelling |
| ⬜ 2 | The `shared_counts` docstring says TEXTS holds raw text, and since the fix the region is dropped by `tree`, not by the function | `tests/test_no_passage_is_pasted_into_a_second_file.py:139` | open | Read: every caller passes `tree` output or synthetic text, so no case is wrong |
| 🟢 | Round 1's yellow finding 1 is closed: the region is dropped from `CLAUDE.md` alone and the template is read whole | `tests/test_no_passage_is_pasted_into_a_second_file.py:182` | confirmed | Executed: `BASELINE` equals the counts both ways at 104 pairs; strip-everywhere turns the new case and the generated-block case red, strip-nowhere turns the generated-block and baseline cases red |
| 🟢 | Round 1's yellow finding 2 is closed: `agents/warden.md` cites the home, and `LINKED` and `CARRIERS` hold it | `agents/warden.md:404` | confirmed | Executed: round 1's text put back fails the pin module; my enumeration of every `CLAUDE.md` mention found no other citation of the four rules |
| 🟢 | Round 1's ⬜ 3 is closed on its coordinate: the line number is gone and the rule's new home is named | `tests/test_chain_hooks_hardening.py:917` | confirmed | Read; the remaining inaccuracy is ⬜ 1 |
| 🟢 | Round 1's ⬜ 4 is closed: the records give the per-pair sum and the distinct windows apart | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:10` | confirmed | Executed: 1,170 distinct at `b7206ab1`, 1,197 at `f7e82f09`, 1,210 at the target, each matching the records |
| 🟢 | The new unit names a paste inside the template's region and is red against the old strip | `tests/test_no_passage_is_pasted_into_a_second_file.py:356` | confirmed | Executed at the target and under the strip-everywhere mutation |
| 🟢 | The `Re-read ·` rows for 0.8.1 R7 and 0.9.2 S3 hold: the fix edits only the identifiers sentence of §Report | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:18` | confirmed | Read against the fix diff; executed: the four cases the two rows name pass, and `evidence-check --strict` on the fragment is 54 ok, 0 drifted |
| ❓ | Whether the claims of the two `Corrected ·` rows and the 0.4.0 row re-read in phase 2 still hold against §*House rules* | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:13` | ❓ out of verified scope | Carried from round 1, unanswered. The fix range does not touch `CONTRIBUTING.md`, so this round's diff gives no new reading; the orchestrator answers whether a second reading is wanted |

## Paste-ready fixes

```python
#   *go in **one batch** before the first edit*  -- one of the spellings
#       #422 measured; `CLAUDE.md`'s goal section emphasised the whole
#       phrase until #730 left the rule to `skills/implement/SKILL.md` §1.
#       Either way the emphasis markers break the literal;
```
```python
    """`{(a, b): n}`, the distinct `WINDOW`-word runs each pair shares.

    TEXTS maps a path to its text as `tree` hands it over, with `CLAUDE.md`'s
    generated region already dropped, so a case can hand in a planted copy.
    Raw `CLAUDE.md` text passed here is read whole."""
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the ratchet, the pin module, the reviewer-report module, the census module, the identifiers module, the wrap module, the contract-preamble module and the one-word module, at e49839ec | 134 passed |
| `bin/test tests/test_chain_hooks_hardening.py -k batch` | 1 passed |
| The four cases 0.8.1 R7 and 0.9.2 S3 name, in `tests/test_the_record_is_generated.py`, `tests/test_the_rules_have_one_owner.py` and `tests/test_the_reviewers_report_reaches_the_record.py` | 4 passed |
| `uvx ruff check` and `uvx ruff format --check` on the three changed Python modules | exit 0, exit 0 |
| `claude_block.py --check` | exit 0 |
| Probe: the module's own counts against `BASELINE`, with totals | equal both ways; 68 files, 189,359 words, 104 pairs, sum 2,104, 1,210 distinct |
| Probe: the same totals at `b7206ab1` and `f7e82f09` | 67, 184,317, 102, 2,064, 1,170; and 68, 188,585, 103, 2,091, 1,197 |
| Probe: the strip put back on every file | `test_a_paste_into_the_block_template_is_named` and `test_the_generated_block_fences_and_headings_are_not_read` failed; 6 passed |
| Probe: the strip removed from `CLAUDE.md` too | the generated-block case failed at 744 shared runs, with the baseline case and the removed-copy case; 5 passed |
| Probe: round 1's `agents/warden.md` put back, the pin module run | `test_every_linked_file_names_each_home_and_section` failed on `('agents/warden.md', 'identifiers')` |
| Probe: every tracked `CLAUDE.md` mention outside `seal/` and `CHANGELOG.md`, in a three-line window against the four rules' words, plus the Korean editions | no citation of the four rules beyond the six `LINKED` holds |
| `evidence-check --strict` on #730's fragment | exit 0; 54 ok, 0 drifted |
| `evidence-check --strict` on the whole ledger | exit 2; 10 drifted rows on three units this branch does not touch, the release head's rows #766 re-reads; none on `agents/warden.md` |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_no_passage_is_pasted_into_a_second_file.py:105` | round 1's 🟡 1 — fixed |
| round-1 | `agents/warden.md:404` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_chain_hooks_hardening.py:917` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:10` | round 1's ⬜ 4 — answered |
| round-1 | `CLAUDE.md:40` | round 1's 🟢 — confirmed |
| round-1 | `CONTRIBUTING.md:265` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_no_passage_is_pasted_into_a_second_file.py:193` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md:79` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_shrunken_corpus_declines_to_judge.py:174` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:13` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
