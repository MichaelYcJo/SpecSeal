# 1788472135-the-run-outlives-its-last-finding — review round 3

| Field | Value |
|---|---|
| Target SHA | 6f6908f323d3344d4f79b8d2f8c428df2c33cff2 |
| PR | not yet opened |
| Broad gate | `7b71727`, against `release/v0.8.0`. Full suite 1950 passed · 1 skipped; `ruff check .` and `ruff format --check .` clean over 96 files; `chain_check --baseline main` and `unverified-check` exit 0. `evidence-check` exits 1 on S8 alone, which the pull-request job warns at and fails only at two, and `gather_changelog --check` exits 1 because a feature branch's fragment is meant to be ungathered |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round of round 2's fixes — target `git diff 8a4bf3e..HEAD`, and
round 2's four verdicts as the agenda. Round 1's were closed by round 2 and
were not to be reopened.

The prompt named where the run stood, because it bounds what a round should
do: rounds 1 and 2 both opened findings, so this was the third of an ordinary
cap of three. *Do not go looking for work* was stated.

Three units were named as the finding surface — `SPLIT_LIMIT`, `_module`,
`_real_records` — and four disclosures the implementer had made were named as
things to judge rather than accept: a mutation it cannot catch, one it re-ran
after finding its own mutation faulty, one it left standing without claiming
it as a fix, and a half of 🟡 2 it recorded rather than closed.

**And one thing that had never been shown outside a fixture**: `round-1.md`
answers the floor `no`, round 2 reopened the run, so a third record should be
legal and `chain_check` should stay clean when `round-3.md` lands. The round
was asked to construct that in a clone, since §6 forbids it committing here.

`agent-contract` §6 and §2 were stated rather than assumed, because round 1's
reviewer broke §6.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | The live three-record sequence — the rule this branch shipped, on real records | `chain_check.py`, `rounds/` | answered | Built `round-3.md` in a clone, committed it, ran `chain_check.py --baseline main` → **exit 0**. `stopping_floor` called directly over rounds 1–3 with the real `later` lists → zero errors. Round 1's 🔴 1 is closed against records rather than fixtures |
| 🟢 2 | Round 2's 🔴 1, the literal `;` | `chain_check.py`, `docs/review-chain-spec.md` | answered | The sentence is in both files, `SPLIT_LIMIT` pins it in both, and all four mutations of that pin were killed. `round-2.md`'s own cell spells the character as a word and passes |
| 🟢 3 | Round 2's 🟡 2, `` `NONE` (depth 1) `` | `chain_check.py:1476` | answered | Seven cells executed. The guard keys on the parenthesised marker, so an ordinary reason survives — `none, nothing added` and `none — the depth was not recorded` still read as `none` |
| 🟢 4 | Round 2's 🟡 9, `COMMA_LIMIT` | `chain_check.py` | answered | The sentence now says *a comma anywhere in the entry outside the depth marker*, which is what the code does, and the case is parametrised over both places a comma can sit |
| 🟡 5 | An invisible character in `Needs a fix` still prints empty backticks. The floor row reads its cell through `reader.visible`; the new `Needs a fix` branch reads the raw cell, so one cell is judged by two readers one line apart | `chain_check.py:1838`, `:1844` | answered | Executed on `""`, U+200B and U+FE0F. This is round 2's 🟡 3 one input further out: its stated cause was *two rows reading the same vocabulary answer the same state at different quality*, and that is still true |
| 🟡 6 | The refusal a record author actually reads still names the wrong cause. The limit is now in a docstring and in the spec; the message quotes a fragment with an unclosed code span and says to add a reach to it, which is not the repair | `chain_check.py:1748` | answered | Round 2's 🔴 1 cost a committed record and a fix commit, and CI runs this on every pull request. Same shape as round 1's 🟡 6 — a refusal whose own instruction produces a cell meaning something else |
| 🟡 7 | `_real_records` says HEAD and reads the index, and its sort raises `TypeError` on a record name it cannot number | `tests/test_chain_check_at_the_pull_request.py:1250`, `:1299` | answered | Executed both: a staged-uncommitted record is listed by `ls-files` and then read as `None`, so it is checked by nobody while the test stays green; `rounds/round-2-draft.md` raises. The repository's own two listers both filter before sorting |
| 🟡 8 | Nothing tests the real-records test. Emptying both `failures.extend` calls leaves it green | `tests/test_chain_check_at_the_pull_request.py:1291` | answered | Executed with a genuinely refused `round-3.md` committed. The `assert records` guard is in the committed code and proves the listing ran; nothing proves the checking did. §15 was met — the case was seen red at `4adbb86` naming the real entry — and the limit is written where whoever loosens the loop meets it |
| 🟡 9 | `seal/ledger.md:182` was re-stamped against a behaviour change three days after its `Checked` date. The row's anchor is `says_none`, whose behaviour this branch changed | `seal/ledger.md:182` | answered | The claim did not go false — the row's four listed values were executed under the new guard and still hold. Not the deferral already on the books: `overview.md` names three rows at 2026-09-03 and defers a convention question; this is a fourth at 2026-09-01 and is not a convention question, because somebody did read that function |

## Executed probes

| What was run | Result |
|---|---|
| `chain_check.py --baseline main` in a clone, with a legal `round-3.md` | **exit 0** — the live case |
| the same with `Fixes checked by: nobody — …` | exit 1, `Pass` beside `nobody` |
| `stopping_floor` over rounds 1–3 with real `later` lists | zero errors |
| the real-records case with a self-refusing `round-3.md` | exit 1, names the truncated entry |
| the same with both `failures.extend` emptied | exit 0 — 🟡 8 |
| `.venv/bin/pytest` × 3 touched modules, clone at HEAD | 154 passed |
| `.venv/bin/pytest` × 3 adjacent modules | 201 passed |
| 4 mutations of the recorded-limit sentences | all four red, restored green |
| `sorted` over `rounds/round-2-draft.md` | `TypeError` — 🟡 7 |
| `ls-files` vs `ls-tree HEAD` on a staged-uncommitted record | listed / not listed — 🟡 7 |
| `evidence_check.py --strict .` | exit 2, `481 ok · 1 drifted` — S8 only |
| `fold_ledger.py --version 0.8.0 --dry-run` · `bin/unverified-check` | exit 0 · exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 2 | `chain_check.py:1748`, the `Contract changes` refusal message | Round 2 closed the limit's *record*; 🟡 6 is that the *message* still names the wrong cause |
| round 2 | `chain_check.py:1838`, the `Needs a fix` message branch | Round 2 closed the empty cell; 🟡 5 is the invisible one |
| round 1 | `seal/ledger.md` S8, and `--reverify` taking no row selector | Still the owner's, still re-stamped by any `--reverify` run on this tree |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Round 3's 🟡 5 and 🟡 6 — two refusal messages: one reads its cell by a different rule than the row beside it, one names the wrong cause | an issue of its own | the repository owner |
| Round 3's 🟡 7 and 🟡 8 — `_real_records` reads the index while its docstring says HEAD, crashes on an unnumbered name, and nothing tests it | an issue of its own | the repository owner |
| Round 3's 🟡 9 — the `Checked` date on `seal/ledger.md:182` | `overview.md` §Not verified, as a fourth row beside the three already there | the repository owner |
| S8's false claim, and that `evidence-check --reverify` takes no row selector | `overview.md` §Not verified | the repository owner |
| A bare `yes` in `Needs a fix` lengthening the floor's count | issue #138 | the repository owner |
| Round 1's reviewer spawning agents and switching the shared tree, against §6 | an issue of its own | the repository owner |

**The run ends here.** Nothing this round opened needs a fix; every 🟡 is
answerable with grounds and has a durable home above. The broad gate is next.
