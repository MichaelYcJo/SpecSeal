# 1789296100-the-seal-and-ci-read-one-ledger-differently — review round 1

| Field | Value |
|---|---|
| Target SHA | 37f73213c0c1629140d89d86cc36107983d3401c |
| Ran by | warden on claude-opus-5 |
| PR | 378 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 1, the notice's `NOT SEALED` limb is pinned by no case and a mutation proves it; 2, the third shape of the deferred silence and its five live instances are not in the row that tracks it; 3, the framer's contradiction with the overview case reaches a sibling branch of this release and has no durable home. |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the work item, against the whole branch: no earlier round to inherit.

The reviewer was asked to take spec compliance first and quality second, and was pointed at six claims to open rather than to accept — the `exit_code` extraction as the real risk rather than the print, the `seal/ledger.md` re-verification against a fragment rule that names appending and removal but not re-verification, this repository's first ledger fragment, the two frame divergences the smith recorded rather than asking about, the deferral of the bare-minor-anchor defect, and the README pair.

It was asked specifically to judge whether phase 1's structural case actually holds the printed sentence and `broad_gate.py`'s ledger call site together, because the owner's Q1 answer — take the widest of three assertions — was given on that ground.

The orchestrator verified findings 1, 2 and 3 independently before this record was written: finding 1 by reading what the module asserts (`:250-251` reach `LENIENT_NOTICE` and a substring of `seal_stamp.py`, and nothing reads `broad_gate.py`'s failure loop at `:589`); finding 2 by applying the module's own `ANCHOR_RE` to `seal/ledger.md` — a wider net than the reviewer's returned seven, and the two extra proved to be path-less prose shorthand inside Notes cells rather than row anchors, so **the reviewer's five is the right number**; finding 3 by opening both coordinates and confirming they cannot both be satisfied.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The notice's `NOT SEALED` limb is pinned by nothing — exempting the ledger check from the gate's failure form leaves the module 13 passed | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:251` · `skills/verify/scripts/broad_gate.py:590` | open | executed — mutation run, file restored byte for byte, tree clean |
| 2 | A third trigger of the deferred silence stands in the shared ledger: five coordinates with bare inner quotes are dropped whole while the run prints `1148 ok` | `skills/evidence-check/scripts/evidence_check.py:65` · `seal/ledger.md:63,71,81,143` | open | executed — the module's own `ANCHOR_RE` applied per ledger file; strict counts 1148 + 5 reproduce phase 4's 1153 |
| 3 | The `overview.md` scheduling divergence is a class: `agents/framer.md` forbids the memo the case demands, and a sibling 0.11.3 branch is red on it at its tip | `agents/framer.md:91` · `tests/test_chain_hooks_hardening.py:1014` | open | executed — `git ls-tree` over `feat/350-a-segments-own-wall-clock-is-in-no-column` |
| 4 | S8 says `seal/ledger.md` untouched and the branch touches it; the act is correct and the divergence table does not carry it | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md` | open | read — S8, phase 4's narrowed verification row, and the two-row divergence table |
| 5 | `spec.md` still names `broad_gate.py#main`; the correction lives in two other files and *Fed back into the spec* reads None | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md:138` | open | read |
| 6 | Three documents state three different reader counts for a work item about who the readers are | `spec.md:83` · `skills/evidence-check/SKILL.md:178` · `CONTRIBUTING.md:21` | open | read |
| 7 | Four phase records carry `Ran by \| unknown` while every `Commit` cell was filled | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/phases/phase-1.md` | open | read |
| 8 | `--reverify` and `--migrate` also return 1 and print nothing; two documents say exit 1 always prints | `skills/evidence-check/scripts/evidence_check.py:1723` · `:2423` · `CONTRIBUTING.md:21` | open | read |
| 9 | The first ledger fragment says *No header* and carries a `####` heading | `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` | open | read |

## Paste-ready fixes

```python
def test_a_failing_ledger_check_is_what_reaches_the_failure_form():
    """S4's third limb. The notice says this tree would come back NOT SEALED,
    which is true only while a failing ledger check reaches `not_sealed`.
    `gate()` exempts no check by name: every entry of `checks` goes through
    one loop, and the loop is what this reads."""
    src = read(BROAD_GATE)
    start = src.index("    failures = []")
    head = src.index("if failures:", start)
    loop = src[start:head]
    assert "for name, check in checks.items():" in loop, loop
    assert "LEDGER" not in loop, f"the failure loop exempts a check by name:\n{loop}"
    assert "stamp.not_sealed(" in src[head:], "the failure form is no longer taken"
```
```
**A third shape was measured on 2026-09-13 during round 1 of #354, and unlike the other two it is already standing in the shared ledger**: a quoted locator whose inner quotes are bare rather than escaped as `\"`. `ANCHOR_RE` matches nothing across it, so the coordinate is dropped whole — five rows of `seal/ledger.md` (`:63`, `:71`, `:81` twice, `:143`) are anchored by nothing while the run prints `1148 ok` for that file. Executed by applying the module's own `ANCHOR_RE` per ledger file and comparing against every backticked coordinate-shaped token in it; the strict counts, 1148 and 5, reproduce the 1153 the checker itself reported. So the fix has three shapes to catch, not two, and it has live instances rather than only a hazard.
```
```
**A framed work item is red on an existing case from the framer's own commit.** `agents/framer.md` §*What the framer writes* tells the framer to write `spec.md`, `plan.md` and `questions.md` and nothing else — **not** `overview.md` — while `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview` fails the moment a directory holds a spec or a plan without a memo beside it. The two cannot both be satisfied, so every work item on the ladder carries a red case from the framer's commit until whichever phase opens the memo. Met in #354, where the smith moved the memo from phase 4 to phase 3 and recorded it as that work item's own scheduling; measured again in round 1 of #354 on a sibling branch of the same release, `feat/350-a-segments-own-wall-clock-is-in-no-column`, whose work item carries a spec and a plan and no memo at its tip. What needs a person is which side gives: the framer writes a stub memo the builder replaces, or the case exempts a work item whose plan still has an open phase. Adding an exemption changes what a gate guards, which `CONTRIBUTING.md` asks a separate argument for.
```
```
| Whether `seal/ledger.md` is touched | `spec.md` S8 and `plan.md` phase 4 both say the shared ledger is untouched; seven of its rows were re-read, re-stamped and re-dated | touched, and the rows re-verified in place | This work's edits changed content under seven anchors that file cites. `broad-gate` passes `--strict`, so leaving them drifted is exit 2 and a branch that comes back refused. `CLAUDE.md` §*a change writes fragments* forbids APPENDING and carves out removal; re-verification is the third case and it is what leaves the ledger true. Not one row was appended — the new claims are all in this work item's own fragment. Phase 4 checked `git diff --stat` for `CHANGELOG.md` alone rather than for both files, which is where S8's other half went quiet |
```
```
Coordinates this builds on, to be cited by the ledger fragment rather than
duplicated here: `skills/evidence-check/scripts/evidence_check.py#main`,
`skills/verify/scripts/broad_gate.py#gate` — the ledger call site is in
`gate`, not in `main`, which phase 4 found and the fragment records.
```
```
Three readers grade drift over one tree, and the command above is the most
lenient of them. A fourth, `hooks/evidence-advisor.py`, imports this module
in process rather than running the script, so it never reaches the exit code
and never carries the line below.
```
```
Three readers of the exit code, one tree, and the disagreement is deliberate
```
```
**So a lenient run says it.** Where a check run's answer is exit 1 and only
there, the check prints which reading you took and what `broad-gate` would
say instead. Exit 0 and exit 2 print nothing extra, because every reader
grades those alike — and `--migrate` and `--reverify` have exit codes of
their own, which report what those writers could not do rather than how
anyone reads drift (#354).
```
```
A check run that comes back exit 1 prints which reading you took
```
```
<!-- One work item's rows. No `# <id>` title — `fold_ledger.py` writes the
`###` at the release and moves this file into `seal/ledger.md`; the `####`
below demotes to `######` under it. -->
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q` at the target SHA | **13 passed** in 0.44 s, exit 0 read directly |
| The same module with `gate()` mutated so the ledger check is exempt from the failure form, restored byte for byte afterwards | **13 passed**, exit 0 — finding 1. `git status --porcelain` empty after the restore |
| The module's own `ANCHOR_RE` applied to `seal/ledger.md` and the new fragment, against every backticked coordinate-shaped token in each | 1148 and 5 strict matches — phase 4's 1153 reproduced; **5 coordinates in `seal/ledger.md` matched by nothing** — finding 2 |
| A grep for an unquoted minor anchor across every `.md` under `seal/` | one prose placeholder and no real coordinate — the fragment's two rows escape their inner quotes |
| `git ls-tree -r` over the two sibling 0.11.3 branches for each work item's `spec.md`, `plan.md` and `overview.md` | `feat/350-…` carries a spec and a plan and no memo; `feat/345-…` carries all three — finding 3 |
| The four `return`s of the old exit block against `exit_code`, enumerated by construction over its four branches | identical in every state: old-format 2, broken-or-refused 2, drifted 2-under-strict-else-1, otherwise 0. The call passes `totals, refused, drifted, args.strict` in the declared order. **No reader's exit code moves** |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It has not been taken at any SHA on this branch. It is the sealer's one act, after the rounds settle (contract §2) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `ANCHOR_RE` drops a coordinate it cannot parse instead of naming it — the hash shape, the bare minor anchor, and the bare inner quote of finding 2 | `seal/follow-up.md` §*Schedulable items with nowhere else to go*, the existing row. Already deferred by this branch; finding 2 asks only that the third shape and its five live instances join the row | the repository owner |
| Whether the broad gate's own end-to-end run shows the notice absent at exit 2 | `overview.md` §*Not verified*. Already deferred by this branch | the sealer |
