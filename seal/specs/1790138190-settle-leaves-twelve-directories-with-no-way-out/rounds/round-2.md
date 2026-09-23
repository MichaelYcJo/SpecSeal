# 1790138190-settle-leaves-twelve-directories-with-no-way-out — review round 2

| Field | Value |
|---|---|
| Target SHA | 207c7e3391b7b0e7b8bb836e59130286e2c25d3d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 525 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `5d777c12288c588dbd3f96e4de95d056a0277cad..157e2d1cc0329d93e0b81aa49ca064c13743757e`, 3 commits |
| Contract changes | none |
| New units | test_a_commented_out_row_is_named_by_its_claim (depth 1); test_a_spec_dropped_on_the_far_side_of_a_merge_is_still_written (depth 1) |
| Needs a fix | yes — finding 6 (🟡): `wrote_a_spec` needs `--full-history`, so a spec dropped before a release's merge into `main` still counts as written. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round. Its target was the diff of round 1's fixes, `492c9b8e..100058fa` (10 commits), and the record commit `207c7e33`, not the branch. It asked whether each of round 1's five `fixed` verdicts is closed, by re-running round 1's own probes against the fix. It judged the units round 1's `New units` row names as code nobody had reviewed: the CHECKER change in `settle.py`, `wrote_a_spec`, and the seven new cases. It also judged the one mutation the smith left surviving, `wrote_a_spec` asking HEAD instead of `ref`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the #511 guard read fewer lines and fewer ledgers than evidence-check | `skills/settle/scripts/settle.py:459` | answered | executed: round 1's probe re-run, the fenced row and the comment row both keep their directory, exit 1; read: sources come from `default_patterns` and `resolve_patterns` |
| 2 | 🟡 a closure and a retirement in one pull request | `skills/settle/SKILL.md:94` | answered | read: the skill, the policy and the report heading all require the closure to merge first; executed: the planted case passes and was red at `492c9b8e` |
| 3 | 🟡 a spec deleted in an earlier merged pull request | `skills/verify/scripts/unverified_check.py:1115` | answered | executed: the reproduced shape (one release branch) is refused by all three planted cases, each red at `492c9b8e`; the class remains open as finding 6 |
| 4 | 🟡 `WORK_ITEM_DIR` matched `docs/specs/` | `skills/code-review/scripts/survivor_check.py:522` | answered | executed: the planted CLI case keeps the directory in the range and measures its sentence; red at `492c9b8e` |
| 5 | ⬜ an anchored spec-less directory listed under the rule heading | `skills/settle/scripts/settle.py:614` | answered | read: `survey["rule"]` is filtered before the report, and `retire()` recomputes its own lists; executed: `0 to retire by the rule` |
| 6 | 🟡 `wrote_a_spec` uses default history simplification, so a spec dropped before a merge commit (release into `main`) reads as never written, and the next release retires it by the rule with no marker | `skills/verify/scripts/unverified_check.py:1140` | **fixed** `3bc96429` | fixed at 3bc96429 — (`--full-history` in `wrote_a_spec`, and the merge-commit case), 157e2d1c (D3 ledger row corrected and re-verified); executed: `wrote_a_spec` False and `retired_by_rule` True at the merge; `unverified_check --baseline` exit 0 *retired by the rule*; `--full-history` flips both; the proposed case is red at `207c7e33` and green with the fix |
| 7 | ⬜ a commented-out anchored row prints `&lt;!--` as its claim | `skills/settle/scripts/settle.py:431` | **fixed** `4fff55bb` | fixed at 4fff55bb — `first_cell` removes a leading comment opener before it splits the row; pinned by `test_a_commented_out_row_is_named_by_its_claim`; executed: the probe's report line `seal/ledger.md:36  &lt;!--`; the directory is kept correctly |
| 🟢 | the surviving mutation (HEAD in place of `ref`) is not a defect | `skills/verify/scripts/unverified_check.py:1121` | not a defect | read: in every caller `ref` is HEAD or an ancestor of it, so the mutation only refuses more |
| 🟢 | CHECKER sources the checker's own address list, including local mode | `skills/settle/scripts/settle.py:475` | not a defect | read, and executed through the old-address case |
| 🟢 | the seven new cases were seen red | `tests/test_settle_reads_before_it_removes.py` | not a defect | executed: 11 of 11 selected failed with `skills/` and `docs/` at `492c9b8e`, and 11 passed at `207c7e33` |
| 🟢 | `207c7e33`'s self-anchored ledger row re-hash and the three markers | `seal/ledger.md` | not a defect | executed: `bin/evidence-check --strict .` exit 0 at `207c7e33` |

## Paste-ready fixes

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a committed `survivors.md` silences the survivors it quotes by subtraction | already deferred in round 1 to `overview.md` §*Not done*; not re-examined here | the repository owner, who files the issue |
