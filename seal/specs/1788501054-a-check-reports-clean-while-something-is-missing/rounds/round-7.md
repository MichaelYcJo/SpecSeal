# 1788501054-a-check-reports-clean-while-something-is-missing — review round 7

| Field | Value |
|---|---|
| Target SHA | d1bf521 |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | `ff22b34`, against `origin/release/v0.8.0` — carried from `round-6.md`, whose row holds the numbers. Every commit since is markdown or the fix this record commissions, and the certifying run is re-taken after that fix lands |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1, the run has no terminal record any of the three exits will accept, because the floor's bound reads `Needs a fix` and that row answers what the REVIEWER opened, not whether fixes were written; 🟡 2 and 🟡 3, the same stale *not yet written* clause left on three cells of `round-5.md` and one of `round-6.md`; 🟡 4, the fragment header's second paragraph names R6 among the six it says were not found by reading |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE RUN IS PAST ITS BOUND AT THIS RECORD, and this time it is not a
choice of the orchestrator's. Round 6 answered `no`; the orchestrator fixed
its two 🟡 anyway, honestly, and set the verdict cells to `**fixed**`. That
act removed the last terminal shape `chain_check.py` accepts:

  A  round-7.md with Pass ticked         -> stopping_floor refuses round-5.md:
                                            two records follow the floor and
                                            neither says the run reopened
  B1 end at round 6, no fixes to check   -> refused: a verdict closed on a fix
  B2 end at round 6, nobody — <why>      -> refused beside a checked Pass

The bound walks `Needs a fix`, which is the reviewer's answer to *what did I
open*. What the bound needs is *were fixes written that owe a reader*, and the
two questions come apart exactly when the orchestrator fixes a 🟡 the reviewer
said could be answered with grounds. The record already carries the missing
fact — `closed_with_a_fix` returns True for round-6.md, which is what refuses
B1 — and the walk never reads it. So the fix is a second stop condition in the
walk, and it is a change to a gate: `CONTRIBUTING.md` §*What a change to a gate
must carry* governs it, and the repository owner's standing instruction for
this round is that the orchestrator writes the fixes rather than a smith.

The fix makes the walk stop one record earlier in one sequence, which is the
ALLOW direction. It is still the cheaper mistake: the alternative is a checker
that forces a false record — verdicts rewritten to `answered` over fixes that
exist — and a false record is this work item's own subject.

Written and committed before the fixes it commissions, so both fix-surface
rows start pending. -->

## What this round was asked

The verifying round at `git diff ff22b34..d1bf521` — **three commits**, all
the orchestrator's, given as a count the round was told to re-take. It did:
`git rev-list --count` returns 3.

Round 6 had answered `Needs a fix: no` and the orchestrator fixed its two 🟡
anyway, so this round existed to read those two corrections — a false row
count in a ledger fragment's header, and a trace in `round-3.md` asserting a
rule phase 9 had reverted.

**Six specific things to try to break**: the ordering rule applied to
`round-6.md`'s own adding commit; both corrections against what they claim to
fix; the class under the stale count — other prose counts in this work item's
documents and the ledger files this branch touched; whether `fold_ledger.py`
really ships the fragment's comment verbatim, since that was the whole stated
reason for fixing rather than answering; every parsed cell of all six records
through the checkers rather than read; and **the terminal state itself, built
in a clone** — the run had never yet been in a state where a ready pull
request could open, and nobody had checked that it could.

The sixth is what found 🔴 1.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The run has no legal terminal record. `stopping_floor` walks the records after `round-5.md` and stops at the first whose `Needs a fix` says the run reopened; `round-6.md` says `no`, so a `round-7.md` is a second uncounted record after a round that met the floor. Ending at round 6 instead is refused both ways: `no fixes to check` because a verdict closed on a fix, `nobody` because `Pass` is ticked beside it | `chain_check.py#stopping_floor`, the walk; trigger `rounds/round-6.md:9` and its verdict cells | open | **Executed** by the round in `--no-local` clones, all three end states, each exit 1 with the refusing sentence quoted. `item_began` reads `1788501054`, above `FLOOR_FROM`, so nothing grandfathers it. **Why it is the checker's defect**: `run_reopened` reads `Needs a fix`, which answers what the reviewer opened; the bound needs whether fixes were written, and `closed_with_a_fix` already answers that for this very record. **Why the honest state closed the last door**: at `c73c56f` the verdict cells read `open` and B1 would have passed — falsely. `d1bf521` set them to `**fixed**` and removed it. The round's replacement — a `wrote_fixes` predicate beside `stopping_floor` and one clause in the walk — was seen red first and then green with 275 existing cases still passing, which also says no case covers this sequence |
| 🟡 2 | `round-5.md`'s three cells still say the fixes are unwritten. Round 6 was the verifying round at round 5's fix diff and says so twice | `rounds/round-5.md:9-11` | open | **Read**, and `chain_check` prints the false sentence on every run — it is in the HEAD output. This is the class `d1bf521` fixed one file over: that commit stripped the identical clause from `round-6.md`'s two surface rows and left all three instances on `round-5.md`, where it had been false for a full round longer. The orchestrator forgot the reach-back at round 6, which is the lapse the pending arm was built to catch and cannot, because the arm keys on `Fixes checked by` and that is one of the three cells left stale |
| 🟡 3 | `round-6.md`'s own checker cell keeps the clause `d1bf521` removed from the two rows beneath it — *this round's fixes are not yet written* — while the same file's verdict column says `**fixed**` twice and its comment says *Round 7 is the reader* | `rounds/round-6.md:9` | open | **Read**. Round 6's own 🟡 1 restated: one pass wrote three copies of a sentence, corrected two, and the criterion that separated them was narrower than the falsehood. The value becomes `round-7` once this record is committed and later, which it now is |
| 🟡 4 | The fragment header's second paragraph names six rows for *the six* and one of them is not one of the six. The paragraph above defines the six as R1, R2, R3, R4, R7, R8; the sentence *not one of the six was found by reading* then lists R1, R3, R8, R2, R6, R7 — R6 in, R4 out, and R6's stated route is *reading* | `seal/ledger/1788501054-…md:19-22` | open | **Read**, and **executed**: `fold_ledger.py --version 9.9.9 --dry-run` puts the comment verbatim under this work item's heading in what becomes `seal/ledger.md`. Same class as round 6's 🟡 2, same paragraph block, one sentence down |
| 🟢 5 | The ordering rule, applied to `round-6.md` | `c73c56f`, `0d4a31f`, `d1bf521` | answered | **Executed**: `merge-base --is-ancestor 0d4a31f c73c56f` exits 1 — the adding commit does not descend from the fix. The update at `d1bf521` does descend from it (exit 0), which is what a correct record looks like |
| 🟢 6 | Round 6's 🟡 2, against the file | `seal/ledger/1788501054-…md:4` | answered | **Executed** per commit: `73ee5a1` took the file 8→10 rows with the header at *Eight*, so R10 was unaccounted from the moment it was written; `cd7998e` dropped R9 to nine; the header now says *Nine* over nine rows and the paragraph accounts for 6+2+1. The new R10 sentence is true of R10's row — two of four limits false, over three false reasons |
| 🟢 7 | Round 6's 🟡 1, against `round-3.md` | `rounds/round-3.md:47` | answered | **Read**: `phase-9.md` exists and reverted the rule, the past tense is correct, the trace beneath still stands, and no true sentence went out with the false one |
| 🟢 8 | `fold_ledger.py`, the stated reason for fixing rather than answering | `.github/scripts/fold_ledger.py#demote` | answered | **Executed**: `demote()` copies every non-heading line byte for byte, the comment carries no `#`-leading line, and the dry run puts `Nine rows.` into `seal/ledger.md`. The reason round 6's record gave was correct |
| 🟢 9 | Every parsed cell of all six records | the six records | answered | **Executed**: no malformed cell. `chain_check` at HEAD raises only the two `nobody` notices and the unchecked `Pass`; `**fixed** \`0d4a31f\`` parses as a `FIX_WORD`, proven by B1's refusal quoting it. `New units | none` for `0d4a31f` is true — the commit is two markdown files |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count ff22b34..d1bf521` | **3** |
| `git merge-base --is-ancestor 0d4a31f c73c56f` · the same for `d1bf521` | exit 1 · exit 0 — the record precedes its fix and the update follows it |
| **the three terminal states, each built in a `--no-local` clone**, driven from Python, `chain_check --baseline origin/release/v0.8.0` against each | **A** exit 1, `round-5.md` *2 round records follow this one with none of them saying the run reopened* · **B1** exit 1, `round-6.md` *says `no fixes to check` while a verdict in this round's own table closed on a fix* · **B2** exit 1, `round-6.md` *`Pass` is checked beside `Fixes checked by: nobody`* |
| the proposed `wrote_fixes` clause, applied in the clone with `round-7.md` present | unpatched exit 1 naming `round-5.md`; patched **exit 0**. Then **275 passed** across six floor-, surface- and checker-reading suites — every existing case green, so none covers this sequence |
| the fragment's rows per commit, `73ee5a1` → `cd7998e` → HEAD | 10 → 9 → 9, header *Eight* → *Eight* → *Nine* |
| `fold_ledger.py --version 9.9.9 --dry-run` | the fragment's comment lands verbatim under `### 1788501054-…`; `Nine rows.` reaches `seal/ledger.md` |
| every parsed cell of all six records through `says_none`, `says_not_yet`, `depth_problems`, `yes_or_no`, `nobody_reason`, `CHECKER_RE`, `verdict_of` | clean |
| twelve record-, ledger- and fold-reading suites at HEAD | **503 passed** |
| `evidence_check.py .` **unscoped**, no `--reverify` | `533 ok · 1 drifted · 0 broken` — S8 alone at `@45edf260` |
| `bin/unverified-check` · `fold_ledger.py --check` | exit 0 · exit 1, four ungathered fragments, the ordinary state between releases |
| `chain_check.py --baseline origin/release/v0.8.0` at HEAD | exit 1 — `round-5.md`'s stale `nobody` (🟡 2), `round-6.md`'s stale `nobody` (🟡 3), and the unchecked `Pass` |

The replacement the fourth row ran, which is 🔴 1's fix — a predicate beside
`stopping_floor` and one clause in its walk:

```python
def wrote_fixes(reader, root, rel):
    """True when this record's own verdicts closed on a fix somebody wrote."""
    text = read_record(root, rel)
    if text is None:
        return False
    return closed_with_a_fix(reader, reader.readable(text), rel)
```

```python
            counted += 1
            if run_reopened(reader, root, other) or wrote_fixes(reader, root, other):
                break
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 6 | `seal/ledger/1788501054-…md`'s header comment | Round 6 found the count wrong, round 7 found the sentence below it naming the wrong rows. The next reader opens the whole comment, not the line the last round fixed |
| rounds 3–7 | whichever cell of a round record the orchestrator last filled | Round 4's 🔴, round 6's two, round 7's three 🟡 — every one a cell or clause of the orchestrator's. The class is *a record filled by the session that wrote the prompt*, and it has now cost four rounds |
| round 7 | `chain_check.py#stopping_floor`, `#run_reopened`, `#closed_with_a_fix` | The bound reads one of two cells that answer the same question, and the two come apart when the orchestrator fixes over a `no` |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **The run is past its bound.** Seven rounds; three is the rule and five the ceiling while a 🔴 is open. Round 7 opened a 🔴 in the checker, and by the documents that is the structure signal — stop regardless. The repository owner's standing instruction for this round is that the orchestrator writes the fixes; the reader those fixes then owe is a verifying round at their diff, which the same documents say costs nothing against the cap if it opens nothing | this row, and `overview.md` §Not done | **the repository owner**, who has already answered the first half |
| ❓ from round 6 — a ledger coordinate with no `@hash` is counted in no bucket by `evidence-check` | `rounds/round-6.md` Deferred | the repository owner — unchanged |
| Whether `st_ino == 0` arrives on `windows-latest`, and the `normcase` pairing | `overview.md` §Not verified | the windows CI leg at this pull request — carried from rounds 2 through 6 |
| `questions.md` Q2, Q3, Q4 — all confirmed still written as questions. Q4's first option, *key on the sibling records*, is the neighbourhood of 🔴 1 | `questions.md` | the repository owner |
| Issue #160's four macOS-only export failures | issue #160 | the repository owner |
