# Round 2 report — every rule CLAUDE.md restates has one home (#730)

| Field | Value |
|---|---|
| Round | 2, the verifying round for round 1's fixes |
| Target SHA | e49839ec |
| Fix range | `8a0e440b..0be7deb4`, read against round 1's record at `e49839ec` |
| Base | `release/v0.18.1` at edee5ca2 |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the branch at the target, in the session scratchpad; the worktree was read and not written, apart from this file |

## What the account asserted, and what the code showed

The round's paragraph, round 1's report and record, the fix diff and the
ledger fragment's corrected rows were read in full and checked against the
tree. Round 1's coordinates were carried; every verdict below was
re-derived at the target.

- **Claimed: the generated-block strip moved from `words` to `tree` and now
  applies to `CLAUDE.md` alone, and `BASELINE` gains `agents/smith.md` with
  the block template at 13.** Confirmed by execution. At the target the
  module's own `shared_counts` equals `BASELINE` in both directions, with no
  pair missing on either side. The totals are 68 files, 189,359 words, 104
  pairs, a per-pair sum of 2,104 and 1,210 distinct shared windows, which
  are the figures ledger O4 states. The new pair's longest run is 27 words,
  the commit-gate waiver sentence the block carries.
- **Claimed: the cases go red both ways (ledger O3's correction).**
  Confirmed by execution. With the strip put back on every file, the new
  case and the generated-block case fail. With the strip removed from
  `CLAUDE.md` too, the generated-block case fails, naming `CLAUDE.md` and
  the template at 744 shared runs, and the baseline case fails beside it.
- **Claimed: `agents/warden.md` now cites `CONTRIBUTING.md`, `LINKED` and
  `CARRIERS` hold it, and a re-enumeration found no other citation.**
  Confirmed by execution and by my own enumeration. With round 1's
  `agents/warden.md` put back, the pin module fails on
  `('agents/warden.md', 'identifiers')`. I read every tracked line that
  mentions `CLAUDE.md` outside `seal/` and `CHANGELOG.md` in a three-line
  window against the four rules' words, every spelling of *real
  identifier*, every *Repo rule* section name, and the Korean editions. No
  other citation of `CLAUDE.md` for the merge, identifiers, cadence or
  batch rule exists. The two *batch* mentions in `hooks/worktree-guard.py`
  and `tests/test_the_guard_asks_once_per_session.py` are about the
  block's *Batch independent reads and runs*, which the block still
  carries.
- **Claimed: the comment no longer cites `CLAUDE.md:39`.** Confirmed by
  reading. The line coordinate is gone and the rule's new home is named.
  The comment still calls its quoted spelling verbatim, and `CLAUDE.md`
  never carried that spelling (⬜ 1).
- **Claimed: the records give the per-pair sum and the distinct windows
  apart, measured at three trees.** Confirmed by execution at all three:
  1,170 distinct at `b7206ab1`, 1,197 at `f7e82f09`, 1,210 at the target.
  The ledger, `phases/phase-2.md`, `questions.md` Q1 and `overview.md` now
  say so, and no *distinct runs* wording remains outside `rounds/`.
- **Claimed: the two `Re-read ·` rows for 0.8.1 R7 and 0.9.2 S3 hold.**
  Confirmed. The fix range edits one paragraph of `agents/warden.md`
  §*Report*, the identifiers sentence, and nothing R7 or S3 claims. R7
  claims the three tables under the generator's headings and the two
  terminal lines; S3 claims the reviewer writes the report, the
  orchestrator writes the record, and the report path is named. All of it
  is unchanged, and the four cases the two rows name pass at the target.
  `evidence-check --strict` on the fragment is 54 ok and 0 drifted. On the
  whole ledger it names 10 drifted rows on three units this branch never
  touches, the release head's rows #766 re-reads, and none on
  `agents/warden.md` or on the edited comment.

## Findings from reading and execution

### Round 1's findings, answered

- **Round 1's yellow finding 1 is closed.** `tree` drops the region from
  `CLAUDE.md` alone (`tests/test_no_passage_is_pasted_into_a_second_file.py:182`),
  the template is read whole, and the two marker-quoting skills regain the
  7 words each that the old strip took. Executed, as above.
- **Round 1's yellow finding 2 is closed.** `agents/warden.md:404` cites
  `CONTRIBUTING.md` §*House rules*, and `LINKED` and `CARRIERS` hold it at
  `tests/test_the_rules_claude_md_names_have_one_home.py:100` and `:116`.
  Seen red against round 1's text, and the class is enumerated.
- **Round 1's ⬜ 3 is closed on its coordinate.** What remains is ⬜ 1
  below, which round 1's grounds had already noticed.
- **Round 1's ⬜ 4 is closed.** Executed at three trees, as above.

### The new unit

`test_a_paste_into_the_block_template_is_named`
(`tests/test_no_passage_is_pasted_into_a_second_file.py:356`) is correct.
It plants a 20-word sentence of `CONTRIBUTING.md` inside the template's
region, asserts the plant landed, and asserts the template is named over
`BASELINE`. It passes at the target and fails with the old strip, so it
pins what round 1 found. It does not assert which file the template is
paired with, which costs nothing today: the only pair that rises is the
paste's.

### ⬜ 1 — The comment still calls a spelling verbatim that the sentence never had

`tests/test_chain_hooks_hardening.py:917`.

The comment quotes *go in \*\*one batch\*\* before the first edit* as
*verbatim from the sentence `CLAUDE.md`'s goal section carried until
#730*. That sentence read *go in \*\*one batch before the first edit\*\**
at every commit from #44 (`fd71605`) to #730 (`9e2dbbd`). Round 1 noted
the emphasis already differed when #422 wrote the comment. The point the
comment makes still holds for both spellings: the emphasis markers break
the literal `in one batch`. So nothing a case depends on is wrong, and
the reader is told something false about the source only.

### ⬜ 2 — `shared_counts` still says it takes raw text

`tests/test_no_passage_is_pasted_into_a_second_file.py:139`.

The docstring says *TEXTS maps a path to its raw text*. Since the fix,
the region is dropped by `tree`, so `shared_counts` reads `CLAUDE.md`'s
region whenever a caller hands it the file's raw text. Every caller today
passes `tree`'s output or synthetic text, so no case is wrong. A later
case written from the docstring would count the region as shared with the
template.

## Regression tests to plant

None. The fix pass planted the two cases round 1 asked for, and both are
seen red above.

## Facts for the evidence ledger

None new. O1, O3 and O4's corrected wording and coordinates match what was
executed here, and the fragment resolves with no drift.

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

## Paste-ready fixes

Neither finding needs a fix. These are the wordings if the smith takes them.

### ⬜ 1

In `tests/test_chain_hooks_hardening.py`, replace the first bullet of the
three spellings:

```python
#   *go in **one batch** before the first edit*  -- one of the spellings
#       #422 measured; `CLAUDE.md`'s goal section emphasised the whole
#       phrase until #730 left the rule to `skills/implement/SKILL.md` §1.
#       Either way the emphasis markers break the literal;
```

### ⬜ 2

In `tests/test_no_passage_is_pasted_into_a_second_file.py`, the
`shared_counts` docstring:

```python
    """`{(a, b): n}`, the distinct `WINDOW`-word runs each pair shares.

    TEXTS maps a path to its text as `tree` hands it over, with `CLAUDE.md`'s
    generated region already dropped, so a case can hand in a planted copy.
    Raw `CLAUDE.md` text passed here is read whole."""
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened: the round's paragraph; round 1's report and record; the fix
diff `8a0e440b..0be7deb4` in full (`agents/warden.md`,
`tests/test_chain_hooks_hardening.py` lines 910–925,
`tests/test_no_passage_is_pasted_into_a_second_file.py` whole,
`tests/test_the_rules_claude_md_names_have_one_home.py` lines 1–140, the
ledger fragment, `overview.md`, `phases/phase-2.md`, `questions.md`); the
work item's `changelog.md` and `spec.md` (O1 and D5);
`docs/the-record-layout.md` lines 195–215; `seal/releases/0.8.1.md` R7,
`seal/releases/0.9.2.md` S3 and `seal/releases/0.11.4.md` line 42;
`tests/test_the_reviewers_report_reaches_the_record.py` lines 305–345;
`tests/test_a_merge_cannot_silently_drop_a_correction.py` lines 404–412;
`tests/test_a_release_is_sized_by_a_criterion.py` lines 338–350;
`hooks/worktree-guard.py` lines 1843–1852; `bin/test`; `CLAUDE.md` at
`fd71605`, `9c23b31` and the base.
