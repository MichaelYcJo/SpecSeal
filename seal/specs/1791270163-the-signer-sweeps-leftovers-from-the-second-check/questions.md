# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing here blocks the build.** No row needs a person. #831 was filed
with its fixes already executed once and written out, and every judgment the
issue left open was settled by something in the tree that can be opened.

**What the tree answered, so nobody reopens it.**

| Judgment | Answered by |
|---|---|
| Whether this item is above the spec rung of `skills/implement/SKILL.md` §3 | **Yes.** Finding 3 changes a refusal sentence `pact-check` prints and a person acts on (they search the file for the quoted line and delete it). One file of wording qualifies; the rung is behaviour, not file count |
| Whether R1 and R6 are edited where they stand | **No.** `seal/config.md` declares `Ledger frozen from \| 1790993141`; 1791239490 is above it; both rows were folded into `seal/releases/0.19.0.md` (lines 31 and 36) by 0.19.0's release and `seal/ledger/` no longer exists. `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* puts the correction in this item's fragment, and `correction-check` (`.github/workflows/hygiene.yml:307`) refuses the range otherwise |
| `Re-read ·` or `Corrected ·` for each of the two rows | **R1 `Corrected ·`, R6 `Re-read ·`.** R1's clause "refused once, as a line inside that table" is false for finding 2's shape and stays false after the fix (the stray-row refusal names the second table instead), so a re-read would date a false claim as read true — the P11/E6 precedent in 1791239490's `overview.md`. R6's clause "to the end of its paragraph" becomes true once finding 1 lands, so a re-read of the moved coordinate is the right instrument, and `--into` writes it |
| Whether the `Corrected · R1` row may carry only the drifted coordinates | **No.** A `Corrected ·` row supersedes the whole family and "a coordinate it leaves out is not checked again" (the same section). It carries every coordinate R1 lists, fifteen, each at its current hash |
| Whether `text.splitlines()[line - 1]` is the line `gfm_table` numbered | **Yes.** `hooks/config.py#gfm_table` splits with `text.splitlines()` and appends `(index + 1, found)` with `index` the position in that list (read). The repository's one-line-ending rule (work item 1790655302) is about the reader ending lines where GFM does, and both sides here use the same split |
| Whether finding 1's widened end needs its own case | **No.** `post-review-check-2.md` §*Regression tests to plant* says the two sweep cases hold it and the six plants are what is seen red; R6's `Re-read ·` row records the plants in its notes (§*Facts for the evidence ledger*) |
| Whether `docs/the-pact.md`'s statement or `Enforced by:` line moves | **No.** No `def` is added or renamed, and the second check read the glued sentence against the statement and the 0.19.0 changelog and found no contradiction |
| Whether `seal/follow-up.md` holds an item this work is the prerequisite for | **No.** Its rows (lines 60, 62, 80) are about `tests/test_docs_line_wrap.py`, `hits()` in the release-sizing test, and the survivor sweep's phase records |
| Where the changelog fragment goes and under which heading | `seal/specs/1791270163-…/changelog.md`, `### Fixed`, no `## ` line (`docs/the-record-layout.md` §*A change writes fragments, never a shared file*; precedent `seal/specs/1791128260-…/changelog.md`) |
| The language of the records | English — `seal/config.md` has no `Record language` row (`skills/implement/SKILL.md` §*The language the records are written in*) |
| Who runs the broad gate | Nobody in this segment. `routing.md`: Review `straight to the PR`, Destination `stop before the pull request`; `overview.md` §*Not verified* names CI at the pull request, or the session that opens it |

**The rows below are the residue.** One is a measurement the build runs; one
is the work's to decide when it meets it.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | How many released rows does phase 3's `--reverify --into` write a `Re-read ·` row for, and does it exit 0? The frame's `grep` finds three rows citing the moved units: `Corrected · P8` (`seal/releases/0.19.0.md:22`, `read_table`), R1 (`:31`, `read_table` and the S4 case) and R6 (`:36`, `without_the_policy_span`) | a measurement | three rows at exit 0 is the expectation; a fourth means a coordinate the grep missed and is read before the row is kept; exit 1 with a `LEFT` line names a repair in the line itself (a stale `--checked`, or no citation naming the row alone) | the grep's three; the run's list wins | ✅ three rows (P8, R1, R6) at exit 0, `0 released rows left` — phase 3, 2026-10-06 |
| W1 | How phase 1 shows the six block plants red: a `test_tmp_*` probe calling `without_the_policy_span` on `docs/the-pact.md`'s text with each plant inserted after the statement's last line, or planting into the working-tree file and running the two sweep cases, then reverting | the work | the probe is one file, run once, deleted, and touches no tracked file; the plant exercises the cases as they read the tree but leaves a dirty file until reverted. Either satisfies §15 if the hand-back says which | the probe | ✅ the probe, patching `open` for `docs/the-pact.md` so both sweep cases read the plants; run before and after the change (twice, so the before state was measured too) and deleted — `phases/phase-1.md` |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. There is none here.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row in `overview.md`; it does not travel
  back to the framer.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.
