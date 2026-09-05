# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — review round 3

| Field | Value |
|---|---|
| Target SHA | da047ab |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | #168 — https://github.com/MichaelYcJo/SpecSeal/pull/168 |
| Broad gate | da047ab against origin/release/v0.8.1 — 2258 passed · 1 skipped · 0 failed with -n auto; ruff check . and ruff format --check . clean. Nothing after it changes code: this record, round-2's reach-back cell and the overview's closed rows |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The run's last verifying round, at `git diff c7a7267..da047ab` — **3 commits**,
two fixes and the record's closing commit, given as a count the round re-took.

Round 2's five verdicts as the agenda, at their coordinates; its `New units`
(`fenced_after`, `FRAGMENT_RE`, `FENCE`, four cases) as the finding surface,
judged as code with mutation; the pull request's legs at `da047ab`;
`chain_check` on the real tree and the terminal shape it will read once this
record commits with `no fixes to check`; and every Deferred row of rounds 1
and 2, each with a named answerer or the one that has none.

The reopening was spent at round 2, so a finding here that needs a fix ends
the run `capped`: each such finding arrives with an issue-ready paragraph. The
two findings this round opened are answerable with grounds and go to #169 —
the orchestrator's one act on this table.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 10 | The record points at fixes it does not carry: `new` copies the probes table and drops the fenced blocks under it | `skills/code-review/scripts/round_record.py#build` and `#fenced_after` | answered | executed — `new` over reports with one fence, two fences (backtick and tilde) and prose between and after them: every fence lands under the table in order, no prose line reaches the record; a record carrying a fence goes through `close` with the fence intact and `New units` filled; mutation A (raise removed) and B (copy removed) each turn one of the two planted cases red; read — spec `:1120-1127` and A5 now say the generator carries the blocks and nothing else of the section, pinned by `test_the_generator_carries_the_fenced_blocks_under_the_probes_table`. One member of the class remains: 🟡 15 |
| 🟡 11 | A Location of the form `path#a` and `#b` reads `a` alone | `skills/code-review/scripts/round_record.py#location_units` and `#FRAGMENT_RE` | answered | executed — the 11 distinct Location cells of round-1.md and round-2.md against HEAD's tracked set: round-1 🟡 4 yields `location_units` and `depth_two` in `round_record.py`; the heading anchors, `seal/ledger.md` F1 and `seal/ledger.md:517` yield nothing; `#168`, `PR #168 — …`, `issue #161's term 3`, `docs/x.md#intro`, `C# and F#` yield nothing; `#b` before any path binds to `None`, the widest reading, which `depth_two` resolves across the touched files; `fragment-after-path` is planted and green, seen red in round 2 |
| ⬜ 12 | The ⬜ 8 sentence names one red window and the leg has two | `skills/code-review/SKILL.md#"## Orchestrator: the pull request opens before round 1, and a phase is re-run"` | answered | executed — release leg at da047ab (run 33965965021): `judged as a draft pull request`, then `Pass` beside `nobody` on round-2.md, exit 1, the reason the sentence names; pinned by `test_the_release_leg_is_red_again_until_the_verifying_rounds_record_commits`. *Once more* reads as one window where the window recurs after every `close`; the fact stays right (rule 3) |
| ⬜ 13 | A binary the range touches is named in the heuristic comment | `skills/code-review/scripts/round_record.py#measure` | answered | read — a binary's diff has no `+` line, so the heuristic did read it and yielded nothing; the comment is true and reads oddly, rule 3; a binary check in `measure` is mechanism outside this diff. The Grounds sentence in round-2.md (*left for the release the heuristic comment already names the file*) is broken — rule 1, coordinate only |
| ⬜ 14 | S8's anchor drifts on the base and the branch edited under it | `seal/ledger.md:517` | answered | carried from round 2 — the same 3 drifts on the base export; the three commits under review touch neither `seal/ledger.md` nor `templates/config.md` (`git show --stat`); re-stamping base drifts at the release-preparation commit is where the other two go, so the grounds hold |
| 🟡 15 | A fence under the probes table that closes after `## Deferred` is accepted: the section is copied inside the fence and the record's own Deferred table reads `nothing to drain` | `skills/code-review/scripts/round_record.py#fenced_after` | deferred #169 | executed — a report whose fence opens under the probes table and closes between the Deferred table and the terminal lines: `new` exit 0, the record's probes section carries `## Deferred` and its row inside the fence, the generated `## Deferred` reads `nothing to drain`, and the check exits 0 (draft); the refusal fires only for a fence closed nowhere, and one closed at the end of the file is refused by `terminal_value` for 0 `Needs a fix:` lines. Fix below, applied in the clone: the late-closed shape exit 2 naming `## Deferred`, a Python comment at column 0 inside a fence still accepted, the two planted fence cases green, ruff clean. Answerable with grounds: the report shape has no closer after `## Deferred`, and the swallowed heading is visible to a reader of the record |
| ⬜ 16 | *Nothing else of the section* has no case: a mutation copying the whole probes section passes both planted fence cases | `tests/test_the_record_is_generated.py#test_a_fenced_block_under_the_probes_table_reaches_the_record` | deferred #169 | executed — prose between the table and the fence and after it is absent from the record at da047ab (the code is right); read — the planted report has no prose under its table, so nothing pins it. Case below |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` at da047ab, `uv venv`, `pytest` on `test_the_record_is_generated.py`, `test_the_fixes_close_the_record.py`, `test_the_rules_have_one_owner.py` | 119 passed; `uvx ruff check` on the generator and the three test files exit 0; `ruff format --check` on the generator exit 0 |
| `git log --oneline c7a7267..da047ab`, `git show --stat` on each | 3 commits: 72c3ad7 (generator, spec, A5, three test files), f68a4a9 (SKILL.md and one pin), da047ab (round-2.md alone); none touches `seal/ledger.md` or `templates/` |
| `gh pr view 168 --json headRefOid,isDraft`, `gh pr checks 168` twice | headRefOid da047ab, draft; release fail 6s, lint pass, ledger pass, macos pass, ubuntu pass, windows pending then pass 3m55s |
| `gh run view 33965965021 --log-failed` (the release leg) | `judged as a draft pull request`, then `Pass` is checked beside `Fixes checked by: nobody — the fixes are not yet written` on round-2.md, exit 1 |
| `chain_check.py --baseline origin/release/v0.8.1` on the real tree at HEAD da047ab, HEAD read and `--worktree` | exit 1 both: `judged as a ready pull request (no pull-request event payload)`; `2 round record(s), last is round-2.md`; `round-2.md:0 Pass is checked beside Fixes checked by: nobody` with the way-out sentence |
| `round_record.py new --round 3 --target da047ab` in the clone over an all-`answered` report, then `chain_check` as `--worktree`, as a HEAD read after a Python-driven commit, and with a draft payload | round-3 `Fixes checked by` is `no fixes to check`, `Pass` ticked, round-2's cell set to `round-3`; exit 0 in all three readings; clone reset to da047ab, status clean |
| `FRAGMENT_RE` and `location_units` on the 11 distinct Location cells of round-1.md and round-2.md against HEAD's tracked set, and on ten synthetic cells | the table in 🟡 11's grounds: heading anchors, `#168`, `PR #168 — …`, `issue #161's term 3` yield nothing; `#depth_two` after a path binds to that path; `#b` before any path binds to `None` |
| `test_tmp_round3_probe.py` in the clone: prose under the probes table, two fences (backtick and tilde), a fence closed after the Deferred table, a fence closed at end of file, a fence through `close` | prose absent and both fences in order; late-closed fence accepted with exit 0 and `nothing to drain` written (🟡 15); end-of-file closer refused for 0 `Needs a fix:` lines; the fence survives `close` with `fixed_it (depth 1)` and `Pass` ticked; probe deleted |
| Mutations of `fenced_after` in the clone: the unclosed-fence raise removed; the copy into `probes` removed | each: 1 failed, 1 passed over the two planted fence cases; generator restored, status clean |
| The fix below applied in the clone, with a late-closed report and a fence holding a `# comment` at column 0 | late-closed exit 2 naming `## Deferred`; the column-0 comment accepted; the two planted fence cases green; `ruff check` exit 0; reverted, status clean |

```python
# skills/code-review/scripts/round_record.py — 🟡 15, before `def fenced_after`
# (VERDICTS, PROBES and DEFERRED are already bound above it)
SECTIONS = (VERDICTS, PROBES, DEFERRED)
```
```python
# skills/code-review/scripts/round_record.py#fenced_after — 🟡 15, in place of the
# closing `return out`
    swallowed = [ln for ln in out if ln.strip() in SECTIONS]
    if swallowed:
        raise Refused(
            f"a fenced block under `{heading}` closes after "
            f"`{swallowed[0].strip()}` — copied as it stands it would carry "
            "that section inside the fence, where no check reads it"
        )
    return out
```
```python
# tests/test_the_record_is_generated.py — 🟡 15 (red at da047ab: exit 0) and ⬜ 16
def test_a_fence_closed_after_the_deferred_table_is_refused(repo):
    declared(repo)
    text = "# what the round found\n\nProse.\n\n"
    text += f"## Verdicts\n\n{VERDICT_HEADER}{OPEN_ROW}\n"
    text += f"## Executed probes\n\n{PROBE_HEADER}{PROBE_ROW}\n"
    text += "```python\ndef helper(a):\n    return a\n"
    text += f"## Deferred\n\n{DEFERRED_HEADER}{DEFERRED_ROW}\n```\n\n"
    text += "Needs a fix: yes — 🔴 1\nLoses a record or crashes: no\n"
    code, out, record = generate(repo, report_text=text)
    assert code == 2, out
    assert "closes after `## Deferred`" in out
    assert record is None


def test_prose_under_the_probes_table_stays_in_the_report(repo):
    declared(repo)
    probes = PROBE_ROW + "\nPROSE-BEFORE.\n\n" + FENCE + "\nPROSE-AFTER.\n"
    code, out, text = generate(repo, report_text=report(probes=probes))
    assert code == 0, out
    assert "PROSE-BEFORE" not in text and "PROSE-AFTER" not in text
    assert FENCE.strip() in text
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_rules_have_one_owner.py#occurrences` | round 1's 🔴 1 — fixed |
| round-1 | `docs/review-chain-spec.md#"##### The last round verifies"` and `agents/smith.md` fix-table paragraph | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#close` | round 1's 🟡 3 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#location_units` and `#depth_two` | round 1's 🟡 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#measure` | round 1's 🟡 5 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#reach_back` | round 1's 🟡 6 — fixed |
| round-1 | `skills/code-review/SKILL.md#"## Orchestrator: the pull request opens before round 1, and a phase is re-run"` | round 1's ⬜ 8 — fixed |
| round-1 | `seal/ledger.md` F1 and R4 rows | round 1's ⬜ 9 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py#build` (`table_of` copies rows alone) | round 2's 🟡 10 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py#location_units` | round 2's 🟡 11 — fixed |
| round-2 | `seal/ledger.md:517` | round 2's ⬜ 14 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, repository-wide lint and typecheck (`Broad gate` stays `not yet`; this round opens no fix, so the gate is due once this record commits) | the broad gate, once after the rounds settle (§2) | the orchestrator |
| 🟡 15 — a fence closed after `## Deferred` is accepted; the fix and its case are above | the smith's grounds, or an issue for the release after 0.8.1 | the orchestrator |
| ⬜ 16 — the prose-exclusion case | planted beside the two fence cases, seen red by copying the section body | the fix pass of the next item, or the release preparer |
| `templates/sdd-round.md:210-211`'s severity comment still reads without ⬜ (round 1's Deferred, answerer `nobody`) | `overview.md` §Not done, unchanged at da047ab | nobody — no named answerer |
| Whether the orchestrator re-ran each phase's suite before the next (round 1) | nothing in the tree records it | the orchestrator |
| ⬜ 13 — a binary named in the heuristic comment; and round-2.md's broken Grounds sentence for it | the release the heuristic comment already goes to; the sentence is rule 1, coordinate only | the fix pass, optional |
| ⬜ 14 — S8's anchor drifts on the base | re-stamped at the release-preparation commit with the other two base drifts | the release preparer |
