# 1790138190-settle-leaves-twelve-directories-with-no-way-out — review round 2 report

| Field | Value |
|---|---|
| Target SHA | 207c7e3391b7b0e7b8bb836e59130286e2c25d3d |
| Kind | verifying round — the diff of round 1's fixes, `492c9b8e..100058fa`, plus the record commit `207c7e33` |
| Ran by | specseal:warden on claude-opus-5-5 |

## What this round was asked

Round 2 is a verifying round. Its target was the diff of round 1's fixes,
`492c9b8e..100058fa` (10 commits), and the record commit `207c7e33`, not the
branch. It asked whether each of round 1's five `fixed` verdicts is closed,
by re-running round 1's own probes against the fix. It judged the units
round 1's `New units` row names as code nobody had reviewed: the CHECKER
change in `settle.py`, `wrote_a_spec`, and the seven new cases. It also
judged the one mutation the smith left surviving, `wrote_a_spec` asking HEAD
instead of `ref`.

## Findings

### 6. 🟡 A spec dropped before a merge commit still reads as never written

`skills/verify/scripts/unverified_check.py:1121` (`wrote_a_spec`, the
`git log` call at line 1140).

`wrote_a_spec` runs `git log -1 <ref> -- <dir>/spec.md` with git's default
history simplification. At a merge commit whose result matches one parent
for that path, git follows that parent alone and prunes the other side.
This repository merges every release branch into `main` with a 3-way merge
commit, and `main` never held the work item before the merge. So a
`spec.md` that was written and then dropped within one release is pruned
from `main`'s history for that path, and every later base reads it as never
written.

The scenario is the common one here, not a corner. A spec dropped in
release N is found in release N+1, when `settle` runs, and release N+1 is
cut from `main`. There the directory is retired by the rule with no marker,
and `unverified-check`, `chain-check`, the survivor sweep and `settle` all
agree, because they share the one predicate. That is round 1's finding 3
again, one merge further out. The fix closed the shape round 1 reproduced
(both pull requests on one release branch) and not the class.

The same false claim stands in three places this fix range wrote: the
docstring of `retired_by_rule`, `docs/review-chain-spec.md:755-758` (*or in
an earlier pull request*), and the ledger fragment's D3 row
(`seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md:18`,
*no commit reachable from there ever held its `spec.md`*). All three become
true with the one-word fix below. Nothing in the prose needs to change, but
the ledger row's anchor hash on `wrote_a_spec` moves and needs
`--reverify`.

Executed: a scratch repository with `main`, a `release` branch that adds and
then drops `spec.md` (two commits), a commit on `main`, and `release` merged
with `--no-ff`. At the merge, `wrote_a_spec` returned False and
`retired_by_rule` returned True. `git log --full-history` found the commit.
A `release2` and a `feature` branch cut from there removed the directory with
no marker, and `unverified_check.py seal/specs --baseline <merge>` exited 0
with *retired by the rule*. With `--full-history` patched in,
`retired_by_rule` returned False. The proposed case below failed against the
code at `207c7e33` and passed with the fix. The four affected modules,
narrowed with `-k "spec or rule or predicate or retire"`, gave 73 passed
with the fix applied.

Cost to this repository's own tree: none. For every directory under
`seal/specs/` at `207c7e33`, the default and `--full-history` readings agree
on whether a `spec.md` was ever written.

### 7. ⬜ A commented-out anchored row prints `&lt;!--` where its claim goes

`skills/settle/scripts/settle.py:431` (the claim cell, read as the first
table cell).

The guard now reads every line (finding 1's fix), so it also names an anchor
inside an HTML comment. The directory is kept and the `file:line` is right.
But the claim is read as a table row's first cell, and for a line that
opens with `&lt;!-- |` the report prints `seal/ledger.md:36  &lt;!--` where the
claim should be. Nothing downstream reads that text and the behaviour is
right, so this is ⬜. The fix would strip a leading `&lt;!--` before splitting
the cells, or fall back to the whole line.

### Round 1's findings, re-checked

- **1: answered.** Round 1's probe was re-run against the fix: one fenced row
  (alpha) and one row inside an HTML comment (beta). `settle --retire`
  exited 1 and kept both directories, naming `seal/ledger.md:33` and `:36`.
  Before the fix, the fenced directory was removed. Read: the guard now asks
  `evidence_check.py#default_patterns` and `resolve_patterns` for its
  sources, so the third address `docs/**/_evidence.md` and local mode's
  `seal/` under the git directory come from the checker's own list. The
  paths are made relative with `relpath` and opened through `under`, and a
  worktree's `..` spelling joins correctly. The case at the old address
  passes.
- **2: answered.** The fix is prose and a heading, and the readers still
  refuse a closure made in the same pull request. That is now the documented
  order, not a gap. Executed: the planted case reads the new sentence from
  settle's report, from the skill and from the policy.
- **3: answered, for the scenario round 1 reproduced.** Both pull requests
  on one branch are now refused, and all three planted cases pass. The class
  is not closed; finding 6 above is the instance that remains.
- **4: answered.** `WORK_ITEM_DIR` is anchored at the start of the path.
  Executed: the planted CLI case keeps `docs/specs/login-flow` in the range
  and measures its sentence.
- **5: answered.** Read: `survey["rule"]` is filtered by `holding` before the
  report and before `retiring`, and `retire()` recomputes its own lists, so
  nothing else reads the filtered value. Executed: the planted case asserts
  `0 to retire by the rule`.

### The new units

- **CHECKER** (`settle.py`): correct. The module loads through `load`, so a
  missing checker is refused with a sentence. Sources are de-duplicated by
  relative path after the inode fold in `resolve_patterns`.
- **`wrote_a_spec`**: correct in its failure direction (a git error keeps
  the directory) and wrong across a merge commit (finding 6).
- **The seven new cases**: all were seen red. With `skills/` and `docs/`
  reverted to `492c9b8e` and the new tests kept, 11 of 11 selected cases
  failed. At `207c7e33` all 11 pass.

### The surviving mutation: `wrote_a_spec` asking HEAD instead of `ref`

Not a defect; I agree with the smith. In every caller, `ref` is HEAD itself
(`settle`) or an ancestor of HEAD (the CI readers' merge base, which the
checked-out head contains). HEAD's history is therefore a superset of
`ref`'s. The mutation can only find a spec that `ref` cannot: one added on
the branch itself to a directory the branch then removes. It answers *wrote
one* there and refuses, which is the direction that keeps a directory. A
spec written and discarded inside one pull request never reached the base,
so nothing is lost either way. A case that pins the difference would be
pinning the less careful reading.

## Regression tests to plant

- `tests/test_unverified_rows_close.py`: the merge-commit case in
  *Paste-ready fixes*, beside `test_a_spec_deleted_by_an_earlier_merge_is_still_a_deletion`.

## Facts for the evidence ledger

- The D3 row in
  `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md:18`
  becomes true after finding 6's fix. Re-read it and run
  `evidence-check --reverify` on its `wrote_a_spec` anchor.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the #511 guard read fewer lines and fewer ledgers than evidence-check | `skills/settle/scripts/settle.py:459` | answered | executed: round 1's probe re-run, the fenced row and the comment row both keep their directory, exit 1; read: sources come from `default_patterns` and `resolve_patterns` |
| 2 | 🟡 a closure and a retirement in one pull request | `skills/settle/SKILL.md:94` | answered | read: the skill, the policy and the report heading all require the closure to merge first; executed: the planted case passes and was red at `492c9b8e` |
| 3 | 🟡 a spec deleted in an earlier merged pull request | `skills/verify/scripts/unverified_check.py:1115` | answered | executed: the reproduced shape (one release branch) is refused by all three planted cases, each red at `492c9b8e`; the class remains open as finding 6 |
| 4 | 🟡 `WORK_ITEM_DIR` matched `docs/specs/` | `skills/code-review/scripts/survivor_check.py:522` | answered | executed: the planted CLI case keeps the directory in the range and measures its sentence; red at `492c9b8e` |
| 5 | ⬜ an anchored spec-less directory listed under the rule heading | `skills/settle/scripts/settle.py:614` | answered | read: `survey["rule"]` is filtered before the report, and `retire()` recomputes its own lists; executed: `0 to retire by the rule` |
| 6 | 🟡 `wrote_a_spec` uses default history simplification, so a spec dropped before a merge commit (release into `main`) reads as never written, and the next release retires it by the rule with no marker | `skills/verify/scripts/unverified_check.py:1140` | open | executed: `wrote_a_spec` False and `retired_by_rule` True at the merge; `unverified_check --baseline` exit 0 *retired by the rule*; `--full-history` flips both; the proposed case is red at `207c7e33` and green with the fix |
| 7 | ⬜ a commented-out anchored row prints `&lt;!--` as its claim | `skills/settle/scripts/settle.py:431` | open | executed: the probe's report line `seal/ledger.md:36  &lt;!--`; the directory is kept correctly |
| 🟢 | the surviving mutation (HEAD in place of `ref`) is not a defect | `skills/verify/scripts/unverified_check.py:1121` | not a defect | read: in every caller `ref` is HEAD or an ancestor of it, so the mutation only refuses more |
| 🟢 | CHECKER sources the checker's own address list, including local mode | `skills/settle/scripts/settle.py:475` | not a defect | read, and executed through the old-address case |
| 🟢 | the seven new cases were seen red | `tests/test_settle_reads_before_it_removes.py` | not a defect | executed: 11 of 11 selected failed with `skills/` and `docs/` at `492c9b8e`, and 11 passed at `207c7e33` |
| 🟢 | `207c7e33`'s self-anchored ledger row re-hash and the three markers | `seal/ledger.md` | not a defect | executed: `bin/evidence-check --strict .` exit 0 at `207c7e33` |

## Executed probes

| What was run | Result |
|---|---|
| the new cases at `207c7e33`, narrowed to their names across the four modules | 11 passed |
| the same selection with `skills/` and `docs/` checked out at `492c9b8e` | 11 failed |
| round 1's probe for finding 1: a fenced row into alpha and an HTML-comment row into beta, `settle --retire` | exit 1, both directories kept, rows named at `seal/ledger.md:33` and `:36` (claim printed as `&lt;!--`, finding 7) |
| scratch repository: spec added and dropped on `release`, merged into `main` with `--no-ff`; `wrote_a_spec`, `retired_by_rule`, `git log` with and without `--full-history` | False, True, empty, the commit found |
| the same repository, a later branch removes the directory; `unverified_check.py seal/specs --baseline <merge>` | exit 0, *1 retired by the rule* |
| the proposed merge-commit case at `207c7e33`, then with `--full-history` added | 1 failed; 1 passed |
| the four affected modules with `--full-history` added, `-k "spec or rule or predicate or retire"` | 73 passed |
| `bin/settle` and `bin/evidence-check --strict .` at `207c7e33` | settle exit 0 (8 to retire by the rule, 2 kept, 2 ungrouped, as in round 1); evidence-check exit 0 |
| every directory under `seal/specs/` at `207c7e33`: `git log` with and without `--full-history` for its `spec.md` | the two readings agree on every directory without a spec |
| the full suite, the repository-wide lint and the typecheck (the broad gate) | not yet: not run by this round and not this agent's to run; it is the sealer's single run after the rounds settle |

## Paste-ready fixes

Finding 6, in `skills/verify/scripts/unverified_check.py#wrote_a_spec`:

```python
    r = subprocess.run(
        [
            "git",
            "-C",
            root,
            "log",
            # Without it, a merge commit whose result matches one parent for
            # this path is followed down that parent alone, and a spec added
            # and dropped on the other side is pruned. Every release reaches
            # `main` through such a merge, so the next release read a spec
            # its predecessor dropped as never written (round 2's finding 6).
            "--full-history",
            "-1",
            "--format=%H",
            ref or "HEAD",
            "--",
            f"{directory}/{SPEC}",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
```

Finding 6, the case for `tests/test_unverified_rows_close.py`:

```python
def test_a_spec_dropped_on_the_far_side_of_a_merge_is_still_written(tmp_path):
    """Round 2's finding 6. A spec added and dropped on a branch that reached
    this one through a merge commit is history git's default simplification
    prunes: at the merge the path matches the parent that never held it, so
    `git log` follows that parent alone. Every release reaches `main` that
    way, so a spec dropped in one release read as never written in the next."""
    d = tmp_path / "r"
    d.mkdir()

    def git(*args):
        subprocess.run(["git", "-C", str(d), *args], check=True, capture_output=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "x@example.com")
    git("config", "user.name", "x")
    (d / "README.md").write_text("r\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "root")
    git("switch", "-qc", "release")
    item = d / "seal" / "specs" / "1780000009-x"
    item.mkdir(parents=True)
    (item / "routing.md").write_text("# x — routing\n", encoding="utf-8")
    (item / "spec.md").write_text("# a spec\n\nA rule.\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "a work item with a spec")
    git("rm", "-q", "seal/specs/1780000009-x/spec.md")
    git("commit", "-qm", "the spec, dropped")
    git("switch", "-q", "main")
    (d / "other.md").write_text("o\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "main moves")
    git("merge", "-q", "--no-ff", "-m", "release into main", "release")
    assert uc.wrote_a_spec(str(d), "HEAD", "seal/specs/1780000009-x"), (
        "a spec dropped before a merge commit read as never written"
    )
    assert not uc.retired_by_rule(str(d), "HEAD", "seal/specs/1780000009-x")
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a committed `survivors.md` silences the survivors it quotes by subtraction | already deferred in round 1 to `overview.md` §*Not done*; not re-examined here | the repository owner, who files the issue |

Needs a fix: yes — finding 6 (🟡): `wrote_a_spec` needs `--full-history`, so a spec dropped before a release's merge into `main` still counts as written.
Loses a record or crashes: no

Proof block: files opened — `seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/rounds/round-1.md`; the diff `492c9b8e..100058fa` of `skills/`, `tests/` and `docs/`; `207c7e33`'s changes to `seal/ledger.md` and `round-1-report.md`; `skills/evidence-check/scripts/evidence_check.py` (`default_patterns`, `resolve_patterns`); `skills/settle/scripts/settle.py` (lines 143–200 and 590–660, 760–900); fixture helpers in `tests/test_settle_reads_before_it_removes.py` and `tests/test_unverified_rows_close.py`. Probes ran in a `--no-local` clone at `207c7e33` in the session scratchpad, which is deleted.
