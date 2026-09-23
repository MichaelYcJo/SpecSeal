# 1790138190-settle-leaves-twelve-directories-with-no-way-out — review round 3 report

Target SHA: `29b79dc9d7924157246792fe8858c3bebacbd347`. Target: round 2's fix range
`5d777c12..157e2d1c` (3 commits) and the record commit `29b79dc9`, not the branch.
This is a verifying round and the last round of the run: round 2 spent the one
reopening. Every probe ran in a `git clone --no-local` at the target SHA.

## What this round was asked

Round 3 is a verifying round, and it is the run's last round because round 2 spent
the one reopening. Its target was the diff of round 2's fixes,
`5d777c12..157e2d1c` (3 commits), plus the record commit `29b79dc9`. It did not
review the whole branch. It asked whether findings 6 and 7, recorded `fixed` in
`rounds/round-2.md`, are actually closed, by re-running round 2's own probes
against the fix. It judged the two cases in round 2's `New units` row as code
nobody had reviewed. It also judged the sibling the smith named and left alone:
the path-limited `git log --diff-filter=A` in `chain_check.py#added_on_branch`,
which predates this branch. The question was whether that call has finding 6's
shape.

## Findings

### Finding 6 is closed: a spec dropped on the far side of a merge now counts as written

`skills/verify/scripts/unverified_check.py:1146` adds `--full-history` to the
one `git log` in `wrote_a_spec`. Round 2's probe was re-run in a scratch repository:
a work item's spec is added and then dropped on `release`, `release` is merged
into `main` with `--no-ff`, and a later branch removes the directory.

- With the fix: `wrote_a_spec` True, `retired_by_rule` False, and
  `unverified_check.py seal/specs --baseline <merge>` exits 1. It names the
  directory's overview as *present at <merge> and not here*, which is a deletion.
- With `3bc96429` reverted alone: `wrote_a_spec` False, `retired_by_rule` True,
  exit 0, and *1 retired by the rule*. That is round 2's defect as it recorded it.

Every reader of the rule goes through this one predicate: `settle.py:634`,
`settle.py:875`, `unverified_check.py:1427` and `chain_check.py:4110` all call
`retired_by_rule`, and `retired_by_rule` is the only caller of `wrote_a_spec`.
So the one-line fix covers the whole class of readers (read). The fix's failure
direction is safe. `--full-history` can only find more commits touching the path,
so the worst it can do is keep a directory.

### Finding 7 is closed: a commented-out row is named by its claim

`skills/settle/scripts/settle.py:437` strips a leading `&lt;!--` before
`first_cell` splits the row. Round 2's probe was re-run through the test module's
own fixture: a fenced row into alpha and a commented-out row into beta, then
`settle --retire`. It exits 1 and keeps both directories. Both rows are named
`a claim read in a round record`, at `seal/ledger.md:33` and `:36`. Round 2's
report showed `&lt;!--` in the second one's place.

### The two new units were seen red against their own fix

Each fix commit's `skills/` hunk was reverted alone and the two cases were run by name:

- `3bc96429` reverted: `test_a_spec_dropped_on_the_far_side_of_a_merge_is_still_written`
  fails on its message *a spec dropped before a merge commit read as never written*.
  The other case passes.
- `4fff55bb` reverted: `test_a_commented_out_row_is_named_by_its_claim` fails on its
  claim assertion. The report line reads `seal/ledger.md:32  &lt;!--`. The other
  case passes.
- At the target SHA both pass.

Reading the cases turned up no defect. The merge-commit case builds exactly the
topology that release-into-`main` produces. Its second assertion
(`not retired_by_rule`) is implied by the first, so it adds no protection, but it
does no harm. The comment case asserts both the positive name and the absence of
the bare opener line, and the red run shows the positive assertion is the one
that fires.

### Finding 8 (⬜): `first_cell` still names any other prefix as the claim

`skills/settle/scripts/settle.py:437` handles one prefix, the comment opener.
The checker reads an anchor on every line whatever comes in front of it, so any
other prefix before the row's first pipe is printed as the claim too. This was
executed: `first_cell` returns `'>'` for `> | claim C | x |` and `'-'` for
`- | claim D | x |`. It also returns `note ... -->` for a one-line comment that
is not a row. The trailing `-->` is cosmetic and the name is otherwise right.

The directory is kept in every case and the file and line are printed, so a
person can still find the row. Only its label is wrong, and nothing ships wrong
if this stands, which makes it ⬜ and not 🟡. It is the same class as finding 7,
and the fix enumerated only the instance the finding named (`agent-contract`
§12). No row of this shape exists in the repository's ledgers today (executed: a grep for a `>`, `-`, `*` or `+` before a row's first pipe over `seal/ledger.md`, `seal/ledger/*.md` and the `_evidence.md` files returned nothing). A paste-ready
fix is below for the orchestrator to take or leave.

### The sibling in `chain_check.py#added_on_branch` has the shape only in one unusual topology, and predates the branch

`skills/code-review/scripts/chain_check.py:2868` was last changed by `e27c197`
(2026-09-05), well before this branch. It runs
`git log --diff-filter=A base..HEAD -- <record>` and takes the first line as the
record's latest add. Three topologies were probed, executed:

- The record is added on the feature branch, and the feature branch then merges an
  advanced base: the add is found. The record exists at HEAD, and the merge is
  TREESAME (identical for that path) to the parent that holds it, so default
  simplification follows the right side.
- The record is added on a side branch merged into the feature branch with `--no-ff`:
  the add is found.
- The record is added on the feature branch, then deleted and re-added with identical
  content on a side branch that is merged back: `added_on_branch` returns the EARLY
  add. With `--full-history` the late add comes first. The merge is TREESAME to both
  parents, so git follows only the first one, and the re-add is pruned.

The third topology is finding 6's shape, a path event on the far side of a merge
pruned by simplification. Its direction is the unsafe one: the docstring's reason
for taking the latest add is that a record judged on an early add can pass as
written before its fixes. The ordinary shapes are unaffected, and the shape
predates this branch, so it goes to Deferred, not to a fix. I did not verify
whether `--full-history` makes merge commits themselves appear as `A` in the
ordinary shape. Whoever writes that fix has to settle that before swapping the flag
in (unverified).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 6 | 🟡 `wrote_a_spec` used default history simplification, so a spec dropped before a merge commit read as never written | `skills/verify/scripts/unverified_check.py:1146` | answered | executed: round 2's scratch-repository probe, with the fix `wrote_a_spec` True, `retired_by_rule` False, `--baseline <merge>` exit 1 *present at … and not here*; with `3bc96429` reverted alone, False / True / exit 0 *1 retired by the rule*. read: every reader goes through `retired_by_rule` (`settle.py:634`, `:875`, `unverified_check.py:1427`, `chain_check.py:4110`) |
| 7 | ⬜ a commented-out anchored row printed `&lt;!--` as its claim | `skills/settle/scripts/settle.py:437` | answered | executed: round 2's probe (fenced row into alpha, commented row into beta, `settle --retire`) exit 1, both kept, both named *a claim read in a round record* at `seal/ledger.md:33` and `:36` |
| 🟢 | new unit: the merge-commit case | `tests/test_unverified_rows_close.py:1988` | not a defect | executed: red with `3bc96429` reverted alone (1 failed, 1 passed), green at the target SHA |
| 🟢 | new unit: the commented-out row case | `tests/test_settle_reads_before_it_removes.py:380` | not a defect | executed: red with `4fff55bb` reverted alone (1 failed, 1 passed), green at the target SHA |
| 🟢 | the D3 ledger row's re-anchor to `wrote_a_spec` at `2c1e77d1` and the new case's anchor | `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md` | not a defect | executed: `bin/evidence-check --strict .` exit 0 at the target SHA |
| 8 | ⬜ `first_cell` names any other prefix before the first pipe (`>`, `-`) as the claim; finding 7's class, one instance fixed | `skills/settle/scripts/settle.py:437` | deferred #530 | executed: `first_cell` returns `'>'` and `'-'` for a blockquoted and a listed row; the directory is kept and the line printed, so only the label is wrong |

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

The probe was one file named test_tmp_r3 inside the clone. It was run and deleted,
and the clone's `git status` is clean.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `chain_check.py#added_on_branch` (`skills/code-review/scripts/chain_check.py:2868`, from `e27c197`) runs a path-limited `git log --diff-filter=A` under default simplification, so a record deleted and re-added on a side branch that merges back is judged on its EARLY add. That is finding 6's shape in the unsafe direction, and it predates this branch | MichaelYcJo/SpecSeal#529 | the repository owner, who files the issue |
| a committed `survivors.md` silences the survivors it quotes by subtraction | already deferred in round 1 to `overview.md` §*Not done*; not re-examined here | the repository owner, who files the issue |

## Paste-ready fixes

Finding 8 (⬜, optional; nothing ships wrong if it stands). Remove every prefix
before the row's first unescaped pipe, not just the comment opener:

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

Needs a fix: no — findings 6 and 7 are closed; finding 8 is ⬜ and the chain_check sibling predates the branch and is deferred.
Loses a record or crashes: no — nothing this round found removes a directory, drops a row or raises.

## Proof block

Files opened this round: `seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/rounds/round-2.md`,
`seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/rounds/round-2-report.md`,
`skills/verify/scripts/unverified_check.py` (1090–1160), `skills/settle/scripts/settle.py`
(374, 428–510), `skills/code-review/scripts/chain_check.py` (810–818, 2818–2872),
`tests/test_settle_reads_before_it_removes.py` (89–135, 255–395),
`tests/test_unverified_rows_close.py` (1913–2025), the overview of this work item
(`## Not verified`), `bin/test`, and the diff `5d777c12..29b79dc9`.
