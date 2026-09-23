# 1790154761-folded-statements-pile-into-one-spec — round 3 report

Target SHA `2d43c78d38663e9f432a7067443cf2eda1d263c0`, a verifying round and
the last of this run. Reviewed by specseal:warden in a `--no-local` clone at
that SHA.

## What this round was asked

A verifying round over round 2's fixes (`8549aa3a..bbd98466`, two commits,
plus the record commit `2d43c78d`), not the branch. For finding 3, recorded
`fixed`, it asked whether the finding is actually closed, re-running round 2's
own probe against the fix. It judged the four ⬜ corrections that rode the same
commit (`BOLD_OPENING` widened to `***`; both `HEADING` patterns reading a tab
or the end of the line after the hashes; `target_problem` resolving both sides
through `realpath`; ledger rows E1, S1 and P1 re-anchored), the new
`survivors.md` with its three exemptions, and the six units in round 2's `New
units` row, as code nobody had reviewed. It also asked whether the widened
`HEADING` starts reading a line under `docs/` that is not a heading, and
whether the real-tree pairing check stays green. No full suite, repository-wide
lint or broad gate was asked for, and none was run.

## Findings

**Finding 3 is closed (executed).** Round 2's probe, a document frozen at 1
marker with the digest of the old two-marker file, now returns the digest
message stating the swap and the deliberate removal as two conditions, each
with its repair, and naming `marker_digest()`. With the count not yet lowered
the count message names the recompute. With the digest recomputed the listing
is clean. The real tree has no problems.

**The four corrections hold (executed).**

- `HEADING`, both copies: across every `.md` under `docs/`, no line reads
  differently under the new pattern than under the old one, and no raw line
  under `docs/` is a bare run of hashes or hashes followed by a tab. Fenced code
  is not live to `live_lines`, so a bare `#` inside a code block is never read.
  `#<number>` is still refused, because a digit is neither a space, a tab nor
  the end of the line. The pairing module is green on the real tree.
- `BOLD_OPENING`: `***Rule.***` and `**Rule**` open bold; `***`, `**`,
  `** Rule`, `*** Rule` and `****Rule` do not.
- `target_problem`: a symlink inside the root to a file outside is refused, a
  dangling symlink to a path outside is refused, a symlink to a file inside is
  accepted, a root reached through a symlink and a relative root both resolve.
- Ledger rows E1, S1 and P1: `evidence-check --strict .` exits 0, so every new
  anchor resolves and every hash matches.

**The six new cases were each seen red (executed).** Reverting one unit at a
time in the clone — each `HEADING` to the space-only pattern, `BOLD_OPENING` to
`**` only, `realpath` to `normpath` on the target, and each of the two messages
to its old wording — fails exactly the case written for it.

**The three `survivors.md` exemptions are sound (read and executed).** Each
quote matches its surviving text, and each grounds sentence is true: the
comment above `FROZEN_IDS_DIGEST` and the docstring of the swap case both
describe a real swap, conditionally, and both readers still refuse
`#<number>`. `survivor-check` over `8549aa3a..d8aa3054` names exactly these
three places.

**⬜ The symlink refusal names the path as outside the repository, and the
path is inside (executed).** `target_problem` returns `docs/link.txt is not a
path inside the repository` for a link at `docs/link.txt`. The case's own
docstring says the opposite: "the path is inside, and the file it opens is
not". The refusal is correct and only the sentence is wrong, so this is a
correction and not a fix. No such target is written anywhere in the tree.

**⬜ `spec.md` §*Data & interfaces* still states the space-only rule, in a
sentence `survivors.md` does not name (read).** `survivors.md` answers the
sentence at `spec.md` line 41. A second one, the bullet opening "**A heading**
is a live line matching `^#{1,6} `. The space is required", states the rule
round 2's fix widened (and the indentation round 1's fix added). `overview.md`
carries the widened clause as inferred, so the record is not wrong as a whole;
this sentence is the one a settle pass would read if it folded the spec.
`survivor-check` does not report it, because its wording differs from what the
range removed. This is paperwork under `seal/specs/`, so a correction.

**🟡 4 — the survivor check goes silent over a range that includes the
`survivors.md` quoting its survivors (executed, already deferred).** Over
`8549aa3a..bbd98466`, `survivor-check` prints `no removed wording is still
standing` with or without `--exempt`, and the three survivors are not listed
under `exempt`. With the three quotes in `survivors.md` replaced by text that
matches nothing, the same range reports all three again, with or without
`--exempt`. So the survivors are silenced because the quote in `survivors.md`
counts as wording the fix wrote, not because the exemption was consulted. The
branch's exemptions are correct, so this changes nothing about this branch.
It is the tool's defect, and it is already open as MichaelYcJo/SpecSeal#507
and MichaelYcJo/SpecSeal#308.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 4 — a `survivors.md` in the range silences the survivors it quotes, with or without `--exempt` | MichaelYcJo/SpecSeal#507 (and MichaelYcJo/SpecSeal#308), already open; this round adds a measured instance | MichaelYcJo, the repository owner who holds #507 |

Needs a fix: no — finding 3 is closed, the four corrections and six new units hold; the two ⬜ are paperwork and a sentence, and 4 is already deferred to #507

Loses a record or crashes: no

## Proof block

Files opened this round: `seal/specs/1790154761-folded-statements-pile-into-one-spec/rounds/round-2.md`,
`seal/specs/1790154761-folded-statements-pile-into-one-spec/rounds/round-2-report.md`,
the diff `8549aa3a..2d43c78d` in full,
`tests/test_a_document_has_room_for_the_next_fold.py` (lines 1-140),
`tests/test_a_folded_statement_names_what_enforces_it.py` (lines 40-140, 200-215),
`skills/code-review/scripts/survivor_check.py` (lines 1-160, 498-540),
`docs/the-evidence-ledger.md` (lines 133-147),
`skills/settle/SKILL.md` (lines 142-152),
`seal/specs/1790154761-folded-statements-pile-into-one-spec/spec.md` (lines 41, 160-168).
