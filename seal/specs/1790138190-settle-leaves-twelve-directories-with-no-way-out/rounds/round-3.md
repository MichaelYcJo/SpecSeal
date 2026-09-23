# 1790138190-settle-leaves-twelve-directories-with-no-way-out — review round 3

| Field | Value |
|---|---|
| Target SHA | 29b79dc9d7924157246792fe8858c3bebacbd347 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 525 |
| Broad gate | 2682ba76 against f8f1c9de |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no — findings 6 and 7 are closed; finding 8 is ⬜ and the chain_check sibling predates the branch and is deferred. |
| Loses a record or crashes | no — nothing this round found removes a directory, drops a row or raises. |

- [x] Pass

## What this round was asked

Round 3 is a verifying round, and it is the run's last round because round 2 spent the one reopening. Its target was the diff of round 2's fixes, `5d777c12..157e2d1c` (3 commits), plus the record commit `29b79dc9`. It did not review the whole branch. It asked whether findings 6 and 7, recorded `fixed` in `rounds/round-2.md`, are actually closed, by re-running round 2's own probes against the fix. It judged the two cases in round 2's `New units` row as code nobody had reviewed. It also judged the sibling the smith named and left alone, the path-limited `git log --diff-filter=A` in `chain_check.py#added_on_branch`, which predates this branch, for whether it has finding 6's shape.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 6 | 🟡 `wrote_a_spec` used default history simplification, so a spec dropped before a merge commit read as never written | `skills/verify/scripts/unverified_check.py:1146` | answered | executed: round 2's scratch-repository probe, with the fix `wrote_a_spec` True, `retired_by_rule` False, `--baseline <merge>` exit 1 *present at … and not here*; with `3bc96429` reverted alone, False / True / exit 0 *1 retired by the rule*. read: every reader goes through `retired_by_rule` (`settle.py:634`, `:875`, `unverified_check.py:1427`, `chain_check.py:4110`) |
| 7 | ⬜ a commented-out anchored row printed `&lt;!--` as its claim | `skills/settle/scripts/settle.py:437` | answered | executed: round 2's probe (fenced row into alpha, commented row into beta, `settle --retire`) exit 1, both kept, both named *a claim read in a round record* at `seal/ledger.md:33` and `:36` |
| 🟢 | new unit: the merge-commit case | `tests/test_unverified_rows_close.py:1988` | not a defect | executed: red with `3bc96429` reverted alone (1 failed, 1 passed), green at the target SHA |
| 🟢 | new unit: the commented-out row case | `tests/test_settle_reads_before_it_removes.py:380` | not a defect | executed: red with `4fff55bb` reverted alone (1 failed, 1 passed), green at the target SHA |
| 🟢 | the D3 ledger row's re-anchor to `wrote_a_spec` at `2c1e77d1` and the new case's anchor | `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md` | not a defect | executed: `bin/evidence-check --strict .` exit 0 at the target SHA |
| 8 | ⬜ `first_cell` names any other prefix before the first pipe (`>`, `-`) as the claim; finding 7's class, one instance fixed | `skills/settle/scripts/settle.py:437` | deferred #530 | executed: `first_cell` returns `'>'` and `'-'` for a blockquoted and a listed row; the directory is kept and the line printed, so only the label is wrong |

## Paste-ready fixes

```python
def first_cell(line):
    """The first cell of a table row, which names the row's claim.

    The checker reads an anchor on every line whatever stands in front of the
    row, so a comment opener, a blockquote marker or a list bullet before the
    first pipe is not the claim (round 2's finding 7, round 3's finding 8)."""
    text = line.strip()
    first_pipe = CELL_RE.search(text)
    if first_pipe and text[: first_pipe.start()].strip() in {"\x3c!--", ">", "-", "*", "+"}:
        text = text[first_pipe.start() :]
    cells = CELL_RE.split(text)
    if len(cells) > 1 and not cells[0].strip():
        cells = cells[1:]
    return cells[0].strip() if cells else ""
```

## Executed probes

| What was run | Result |
|---|---|
| the two new cases by name at the target SHA | 2 passed |
| the same with `skills/` at `5d777c12` | 2 failed |
| the same with `3bc96429`'s `skills/` hunk reverted alone | 1 failed (the merge-commit case), 1 passed |
| the same with `4fff55bb`'s `skills/` hunk reverted alone | 1 failed (the commented-out row case), 1 passed |
| round 2's finding 6 probe: spec added and dropped on `release`, `--no-ff` merge into `main`, a later branch removes the directory; `wrote_a_spec`, `retired_by_rule`, `unverified_check.py seal/specs --baseline <merge>` | fix: True, False, exit 1 *present at … and not here*; `3bc96429` reverted: False, True, exit 0 *1 retired by the rule* |
| round 2's finding 7 probe: fenced row into alpha, commented-out row into beta, `settle --retire` | exit 1, both kept, both rows named by their claim at `seal/ledger.md:33` and `:36` |
| `first_cell` over seven line shapes | comment-opener forms name the claim; `> \|` gives `'>'`, `- \|` gives `'-'` (finding 8) |
| `chain_check.py#added_on_branch` over three merge topologies | ordinary two: the add found; delete-and-re-add on a merged side branch: the early add returned, `--full-history` returns the late one |
| `bin/evidence-check --strict .` at the target SHA | exit 0 |
| the full suite, the repository-wide lint and the typecheck (the broad gate) | not yet: not run by this round and not this agent's to run. It is the sealer's single run, and with this round it has come due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/settle/scripts/settle.py:459` | round 1's 1 — fixed |
| round-1 | `skills/settle/SKILL.md:94` | round 1's 2 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py:1115` | round 1's 3 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:522` | round 1's 4 — fixed |
| round-1 | `skills/settle/scripts/settle.py:614` | round 1's 5 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py:1090` | round 1's 🟢 — not a defect |
| round-1 | `skills/verify/scripts/unverified_check.py:1384` | round 1's 🟢 — not a defect |
| round-1 | `skills/settle/scripts/settle.py:435` | round 1's 🟢 — not a defect |
| round-1 | `skills/settle/scripts/settle.py:374` | round 1's 🟢 — not a defect |
| round-1 | `tests/conftest.py` | round 1's 🟢 — not a defect |
| round-1 | `skills/settle/SKILL.md:211` | round 1's 🟢 — not a defect |
| round-1 | `skills/verify/scripts/unverified_check.py` | round 1's 🟢 — not a defect |
| round-1 | `seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/overview.md` | round 1's 🟢 — not a defect |
| round-1 | `tests/test_no_document_names_the_old_roots.py` | round 1's 🟢 — not a defect |
| round-1 | `skills/code-review/scripts/survivor_check.py:641` | round 1's 🟢 — not a defect |
| round-1 | `skills/code-review/scripts/survivor_check.py:612` | round 1's 🟢 — not a defect |
| round-2 | `skills/verify/scripts/unverified_check.py:1140` | round 2's 6 — fixed |
| round-2 | `skills/settle/scripts/settle.py:431` | round 2's 7 — fixed |
| round-2 | `skills/verify/scripts/unverified_check.py:1121` | round 2's 🟢 — not a defect |
| round-2 | `skills/settle/scripts/settle.py:475` | round 2's 🟢 — not a defect |
| round-2 | `tests/test_settle_reads_before_it_removes.py` | round 2's 🟢 — not a defect |
| round-2 | `seal/ledger.md` | round 2's 🟢 — not a defect |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `chain_check.py#added_on_branch` (`skills/code-review/scripts/chain_check.py:2868`, from `e27c197`) runs a path-limited `git log --diff-filter=A` under default simplification, so a record deleted and re-added on a side branch that merges back is judged on its EARLY add. That is finding 6's shape in the unsafe direction, and it predates this branch | MichaelYcJo/SpecSeal#529 | the repository owner, who files the issue |
| a committed `survivors.md` silences the survivors it quotes by subtraction | already deferred in round 1 to `overview.md` §*Not done*; not re-examined here | the repository owner, who files the issue |
