# 1790154761-folded-statements-pile-into-one-spec — review round 3

| Field | Value |
|---|---|
| Target SHA | 2d43c78d38663e9f432a7067443cf2eda1d263c0 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 527 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no — finding 3 is closed, the four corrections and six new units hold; the two ⬜ are paperwork and a sentence, and 4 is already deferred to #507 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A verifying round over round 2's fixes (`8549aa3a..bbd98466`, two commits, plus the record commit `2d43c78d`), not the branch, and the run's last. It asked whether finding 3, recorded `fixed`, is actually closed, re-running round 2's own probe against the fix. It judged the following as code nobody had reviewed:

- the four ⬜ corrections that rode the same commit
- the new `survivors.md` with its three exemptions
- the six units in round 2's `New units` row

It also asked whether the widened `HEADING` starts reading a line under `docs/` that is not a heading, and whether the real-tree pairing check stays green.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 2 finding 3: after a deliberate removal the digest message reported a swap as fact and neither message named the recompute | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | verified | Executed: round 2's probe (frozen at 1, old two-id digest) returns the conditional message naming `marker_digest()`; frozen at 2 returns the count message naming the recompute; the recomputed digest is clean; the real tree is clean |
| 🟢 | Round 2 correction: both `HEADING` patterns read a tab or the end of the line after the hashes | `tests/test_both_editions_carry_the_same_folds.py#HEADING`; `tests/test_a_folded_statement_names_what_enforces_it.py#HEADING` | verified | Executed: no line under `docs/` reads differently under the new pattern; no bare or tab-headed hash line exists there; fenced code is not live; `#<number>` still refused; the pairing module is green |
| 🟢 | Round 2 correction: `***Rule.***` opens bold | `tests/test_a_folded_statement_names_what_enforces_it.py#BOLD_OPENING` | verified | Executed on eight openings; only `***Rule.***`, `**Rule**` and a pre-existing unclosed form pass |
| 🟢 | Round 2 correction: a symlink inside the root to a file outside it is refused | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | verified | Executed: outside link and dangling outside link refused; inside link, symlinked root and relative root accepted |
| 🟢 | Round 2 correction: ledger rows E1, S1 and P1 anchor `HEADING`, `BOLD_OPENING` and the re-hashed units | `seal/ledger/1790154761-folded-statements-pile-into-one-spec.md`, rows E1, S1, P1 | verified | Executed: `evidence-check --strict .` exit 0 |
| 🟢 | The six units in round 2's `New units` row | the three test modules | verified | Executed: 43 passed; each case red with its unit reverted, one at a time |
| 🟢 | `survivors.md`, three exemptions | `seal/specs/1790154761-folded-statements-pile-into-one-spec/survivors.md` | verified | Executed: `survivor-check` over `8549aa3a..d8aa3054` names exactly these three; read: each quote matches and each grounds sentence is true |
| ⬜ | The symlink refusal says the path is not inside the repository; the path is inside and the file it opens is not | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | correction | Executed: `docs/link.txt is not a path inside the repository` for a link at `docs/link.txt`. The refusal is right, the sentence is wrong |
| ⬜ | `spec.md` still states the space-only heading rule in a second sentence `survivors.md` does not name | `seal/specs/1790154761-folded-statements-pile-into-one-spec/spec.md` §*Data & interfaces*, bullet "**A heading**" | correction | Read. Paperwork: add it to `survivors.md` or correct it; `overview.md` already carries the widened clause |
| 4 | 🟡 `survivor-check` goes silent over a range that adds the `survivors.md` quoting its survivors, with or without `--exempt`, and lists none of them under `exempt` | `skills/code-review/scripts/survivor_check.py#corrected` | deferred MichaelYcJo/SpecSeal#507 | Executed, see probes. Already deferred in MichaelYcJo/SpecSeal#507 and MichaelYcJo/SpecSeal#308; outside this branch's diff and not in a unit its fixes created |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| Round 2's finding-3 probe through `ceiling_problems` at `2d43c78d` | frozen at 1 with old digest: conditional message naming `marker_digest()`; frozen at 2: count message naming the recompute; recomputed digest: `[]`; real tree: `[]` |
| Old against new `HEADING` over every live line of every `.md` under `docs/` | no line differs; no raw bare or tab-headed hash line; `live_lines` marks fenced lines not live |
| `BOLD_OPENING` on eight openings; `target_problem` on outside, dangling, inside symlinks, `.`, `../out.txt`, a symlinked root and a relative root | as stated in the findings |
| Each of the six new cases with its unit reverted, one at a time | all six red; the tree restored after each |
| `bin/test` over the three modules of this work item | 43 passed |
| `bin/test` over `test_settle_reads_before_it_removes`, `test_docs_line_wrap`, `test_the_rules_have_one_owner`, `test_no_real_identifiers` | 159 passed |
| `bin/evidence-check --strict .`; `bin/unverified-check` | exit 0; exit 0 |
| `uvx ruff check` and `uvx ruff format --check` on the three touched modules only | all checks passed; 3 files already formatted |
| `survivor-check --range 8549aa3a..d8aa3054` | exit 1, the three places `survivors.md` names |
| `survivor-check --range 8549aa3a..bbd98466`, with and without `--exempt` | exit 0 both, none listed under `exempt` |
| The same range rebuilt with the three `survivors.md` quotes replaced by text that matches nothing | exit 1 both, all three reported (finding 4). Probe files and both clones deleted |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet run, and not this round's; the sealer's, and it comes due now that this round leaves nothing needing a fix |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | round 1's 1 — fixed |
| round-1 | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | round 1's 2 — fixed |
| round-1 | `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*, first bullet | round 1's ⬜ — correction |
| round-1 | `skills/settle/SKILL.md` §*2. Write one standing statement per segment*; `tests/test_a_folded_statement_names_what_enforces_it.py#shape_problems` | round 1's ⬜ — correction |
| round-1 | `tests/test_both_editions_carry_the_same_folds.py#outline` | round 1's ⬜ — correction |
| round-1 | `docs/one-root-by-lifetime.ko.md` | round 1's 🟢 — verified |
| round-1 | `tests/test_both_editions_carry_the_same_folds.py` | round 1's 🟢 — verified |
| round-1 | the three new modules | round 1's 🟢 — verified |
| round-2 | `tests/test_a_folded_statement_names_what_enforces_it.py#BOLD_OPENING` | round 2's ⬜ — correction |
| round-2 | `tests/test_both_editions_carry_the_same_folds.py#HEADING`; `tests/test_a_folded_statement_names_what_enforces_it.py#HEADING` | round 2's ⬜ — correction |
| round-2 | `seal/ledger/1790154761-folded-statements-pile-into-one-spec.md`, rows E1 and S1 | round 2's ⬜ — correction |
| round-2 | `docs/the-evidence-ledger.md`; `skills/settle/SKILL.md`; the two `HEADING` patterns | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 4 — a `survivors.md` in the range silences the survivors it quotes, with or without `--exempt` | MichaelYcJo/SpecSeal#507 (and MichaelYcJo/SpecSeal#308), already open; this round adds a measured instance | MichaelYcJo, the repository owner who holds #507 |
