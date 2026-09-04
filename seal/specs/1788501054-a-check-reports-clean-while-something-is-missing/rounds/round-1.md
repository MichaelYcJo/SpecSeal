# 1788501054-a-check-reports-clean-while-something-is-missing — review round 1

| Field | Value |
|---|---|
| Target SHA | 15278db |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | not yet — and no broad run has happened on this branch at all |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | `case_insensitive` (depth 1); `test_a_hard_link_to_the_ledger_is_not_reported_as_skipped` (depth 1); `test_a_case_spelling_of_the_ledger_is_not_reported_as_skipped` (depth 1); `test_a_record_deleted_and_re_added_after_the_fix_is_judged_on_the_later_add` (depth 1); `test_a_fixed_verdict_naming_no_commit_passes` (depth 1); `test_the_spec_and_the_template_state_the_reach_and_ask_for_the_commit` (depth 1) |
| Needs a fix | yes — 🟡 1 three `seal/ledger.md` rows assert a read on a date the content did not exist; 🟡 2 the refusal's reach is the SHA a verdict cell happens to carry, and 20 of this repository's 235 fix-word cells carry none; 🟡 3 `found[-1]` is undefended and is the permissive direction; 🟡 4 the skipped-ledger comparison folds case on Windows alone |
| Loses a record or crashes | no |

- [ ] Pass

<!-- Written and committed BEFORE the fix pass it commissions, which is the
rule `ORDER_FROM` adds in this very branch. The reviewer named that as the one
thing that could still make this the release's fourth self-break, and the act
is the orchestrator's rather than the branch's. Its verdict cells therefore
read `open`: the fixes do not exist yet, and a cell reading `fixed at <sha>`
here would be the shape #150 was opened about. -->

## What this round was asked

The whole branch against `release/v0.8.0`, with the **unscoped** `evidence-check`
handed over rather than the scoped form — phase 1's own rule, applied to this
branch's rounds before it ships, because a guidance change binds sessions only
after the release.

Six surfaces in order, four of them the implementer's own leads: the
self-application of both rules; `commissioned_fixes` reading only the verdict
cell; `SHA_RE` over a prose cell; the `--ledger` notice's `realpath`/`normcase`
comparison; the mutation that survived the first loop and the case that says in
its own docstring it cannot be red at HEAD; and how the rebase question was
settled.

Two disclosures were named to be judged rather than accepted: that the
implementer widened its own scope once with a repository-wide `ruff` and said
so, and that `questions.md` Q2 is open with the repository owner.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | The branch's own claim — the unscoped read finds what the scoped one hides | `seal/ledger.md` | answered | Executed unscoped in a clone: `517 ok · 1 drifted · 0 broken`, the drift being S8, drifted on the base too. Eight shared-ledger rows were re-stamped by this branch and **none is in its own fragment**, so the scoped read would have reported clean the whole way. #153's measurement reproduced by the branch fixing it |
| 🟢 2 | The self-application of #150's refusal | `chain_check.py` | answered | The refusal fires on the shape it is meant to and passes the shape a correct record has, both executed. `ORDER_FROM` is this item's own second and `item_began` returns the same value, so `began < ORDER_FROM` is False and this branch fails rather than prints |
| 🟢 3 | `SHA_RE` over a prose verdict cell | `chain_check.py:1997` | answered | Executed: a cell reading `see <sha> in the changelog` does fire. The reviewer could not build a false positive — the `commissioned` filter drops any commit the round already reviewed, so what survives is a commit created after the round's target and cited in a `fixed` cell, which is a fix. A head-of-cell rule would be no safer and would lose the ordinary spelling |
| 🟢 4 | The mutation that survived the implementer's first loop | `tests/test_a_record_precedes_the_fixes_it_commissions.py` | answered | Run again by the reviewer: dropping `--diff-filter=A` turns exactly one case red, and it is the one whose docstring says it cannot be red at HEAD. **The case is evidence rather than a description.** Three further mutations each turned exactly one case red |
| 🟢 5 | How the rebase question was settled | `docs/review-chain-spec.md` | answered | Both halves correct and neither breakable. A rebase replays in order so a passing record stays passing; the rewritten fix's new hash makes a stale cell resolve to nothing, which is the permissive direction, stated as knowingly open with the cost of closing it named |
| 🟡 6 | Three rows in `seal/ledger.md` carry `Checked` dates of 2026-09-02 over hashes covering content this branch wrote on 2026-09-04 | `seal/ledger.md:102`, `:381`, `:434` | open | `CLAUDE.md`: *"The `Checked` column holds the date somebody read the code. Re-verifying is re-reading and then running `--reverify`."* Eight rows were re-stamped and `phases/phase-4.md` names two as re-read on their merits, which says what happened to the other six. **This is the work item's own shape one level in**: the fix surfaced the drift, and what the drift bought was a re-stamp with no re-read — a check reporting `517 ok` while the trace that would show it, the date, is missing. Row `:102` also still says `Draft 0.6` where this branch moved the protocol to 1.2 |
| 🟡 7 | The refusal's reach is the SHA a verdict cell happens to carry | `chain_check.py:1997` | open | Executed and counted: **235 fix-word verdict cells in this repository, 215 carrying a SHA, 20 carrying none** — the round reported 231/212/19 and the fix pass re-took the count through the checker's own `verdict_table`, `verdict_of`, `FIX_WORDS` and `SHA_RE` at both this target and HEAD, getting the same answer twice. The direction is untouched; the number moved — ordinary house style, not malformed. So the reach is not a decision about which column to read; it is contingent on whether the orchestrator pasted a SHA, and a record written entirely the third way is invisible however late it was committed. `templates/sdd-round.md` asks for no such thing and the new spec table enumerates six pass states without naming the commonest |
| 🟡 8 | `added_on_branch` takes `found[-1]`, its docstring says so, and nothing pins it | `chain_check.py:1975` | open | Mutating to `found[0]` left **all twenty cases green** — `--diff-filter=A` normally returns one commit, so the spellings differ only on a delete-and-re-add, which no case builds. It is the permissive direction, and a delete-and-re-add is exactly the shape that makes a late record look early |
| 🟡 9 | The skipped-ledger comparison folds case on Windows alone, so the notice can name a file it just read | `evidence_check.py:911` | open | Executed on a case-insensitive filesystem: `--ledger 'SEAL/ledger.md'` names `seal/ledger.md` among the ledgers it did not read. `normcase` is the identity outside Windows and `realpath` canonicalises no case anywhere. `agent-contract` §13's shape — a defence resting on the platform where nobody removed the guarantee. Over-reporting, so nothing goes unread; what it costs is the notice's credibility on the run it was added to make trustworthy |
| ⬜ 10 | A verdict cell naming two commits prints the 90-word failure twice | `chain_check.py` | noted | The grouping key is the resolved commit, so seven-cells-one-commit is solved and one-cell-many-commits is not. Rare and stricter, so a note |

<!-- Two things this record got wrong, corrected here rather than left for a
reader to find. The count above was 231/212/19 and is 235/215/20 — the round
counted by hand and the fix pass re-took it through the checker's own readers.

And the message that commissioned the fix pass claimed THIS FILE carried the
reviewer's paste-ready replacements. It does not: `grep -c` for a fenced block
returns 0. The record is not in breach of what phase 4 added — its probe rows
name commands and mutations, not proposed replacements, so nothing in it owed a
block — but the implementer went looking on the orchestrator's word and wrote
all four fixes again.

That is #150's own shape from a third side. The first instance was a record
that did not exist; the second was a record that said it verified something it
did not carry; this one is a record that was correct while the prose
commissioning work from it was not. Only the first two are things a check could
see. -->

## Executed probes

| What was run | Result |
|---|---|
| `evidence_check.py .` unscoped, clone at target | exit 1, `517 ok · 1 drifted · 0 broken` — S8 only |
| the fix-word verdict cells counted across `seal/specs/*/rounds/round-*.md` | the round said 212 of 231 with a SHA; re-taken through the checker's own readers it is **215 of 235, 20 without** — 🟡 7 |
| a fully late record with its fix in the Grounds column | **exit 0** — 🟡 7 |
| `found[-1]` → `found[0]`, twenty cases | **all green** — 🟡 8 |
| `--diff-filter=A` dropped | 1 red, and it is the case that says it cannot be red at HEAD |
| the `Target SHA` filter dropped · the `FIX_WORDS` filter dropped | 1 red each, both singletons |
| the verdict cell widened to the whole row | **0 red** |
| `--ledger 'SEAL/ledger.md'` on a case-insensitive filesystem | names the file it just read — 🟡 9 |
| the three new suites | 36 passed |
| `chain_check --baseline release/v0.8.0` | exit 1, `holds no round-N.md` — the honest pre-round state |
| `unverified-check` · `uvx ruff check` on the five changed Python files | exit 0 · clean |

## Inherited coordinates

Round 1 — nothing to inherit. What it was handed instead were the implementer's
four leads and the unscoped command, which is phase 1's rule applied before
phase 1 ships.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `questions.md` Q2 — a blind `--reverify` takes S8 along and leaves the `Checked` column asserting a read nobody did. The round sharpens the question rather than answering it: 🟡 6 is Q2's cost arriving on the first branch | `questions.md` | the repository owner |
| Whether the six re-stamped rows' claims still hold. The round checked the dates, not the claims | the fix pass for 🟡 6 | the fix pass |
| **The broad gate has not run at all on this branch.** The implementer's repository-wide `ruff` before phase 3 was followed by edits and is spent | `overview.md` §Not verified | the orchestrator, after the rounds settle |
| `seal/ledger.md` S8 | work item `1788472135`'s memo | the repository owner |
