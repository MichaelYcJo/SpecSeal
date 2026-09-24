# 1790221963-a-release-writes-the-gathered-text-back — review round 3

| Field | Value |
|---|---|
| Target SHA | 7bc34064685a71ca006b9401f21db26e7bc1566b |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 560 |
| Broad gate | 25904591 against 61f0d0d8 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the terminal record of a run capped at the reopening bound — round 2 opened a 🟡 and spent the one reopening — reviewed at 7bc34064: round 2's fix range `ab9b026b..e5dc540d`, the source-scoped split. It asked whether the new case is red with the parent script and green at the target, whether Z1, Z2, Z1n, X5, W, Wc, Ww and step A's seven shapes give round 2's table at the target, and whether any source other than `CHANGELOG.md` can be scored against the split. It was told to commission nothing and to give anything it opened a home elsewhere.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the records name one report-less shape and give it a reason the fix made irrelevant: a gathered rewording that shares wording with what `CHANGELOG.md` lost is also silent for another file's deleted sentence (Y1), as the rule now says | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | deferred #563 | executed: Y1 exit 1 naming `docs/b.md` at `61f0d0d8` and `e6c85df6`, exit 0 at the target; controls Y1w exit 1 at all three and Y1c exit 0 at all three; the same sentence at `overview.md:53` and ledger row H1's note; paperwork correction, not counted in Needs a fix; the run is capped, so no fix on this branch; the new issue is for the owner's decision on whether gathered rewording counts as written, which covers W and Y1 alike |
| 🟢 | round 2's finding 1 is closed — the split is subtracted from `CHANGELOG.md`'s removed sentences alone, so a gathered fragment no longer subtracts another file's survivor | `skills/code-review/scripts/survivor_check.py:1187` | confirmed | executed: the new case failed (1 failed, 103 deselected, `exit 0`, `against 3 sentence(s)`) with `ab9b026b`'s script swapped in, restored with `git checkout`; module 104 passed at the target; Z1 and Z2 exit 1 naming `docs/b.md` at the target, 0 at `e6c85df6`; Z1n exit 1 at every state; mutations: `mine -= split` removed, X5 alone red; the `CHANGELOG` test made true for every source, the new case alone red |
| 🟢 | no source other than `CHANGELOG.md` can be scored against the split | `skills/code-review/scripts/survivor_check.py:1038` | confirmed | read: `moved`, and therefore `held` and `split`, is filled only for `CHANGELOG.md`; `score` subtracts `split` only inside `source.path == CHANGELOG`; executed: a repository-wide search finds `examine` the only caller of `corrected` and `score` |
| 🟢 | round 1's and round 2's shapes answer at the target as round 2's per-source column predicted: P6, P6d, H1k, H1, H1c, H2k, H2, X5, X5W, Ww, Z1, Z2, Z1n exit 1 naming `docs/b.md`; W and Wc exit 0 | `skills/code-review/scripts/survivor_check.py:1068` | confirmed | executed at `61f0d0d8`, `bf7ba905`, `e6c85df6` and the target; every cell equals round 2's table, the target column equal to round 2's per-source column |
| 🟢 | round 1's finding 2 stays closed — W is the rule working | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | confirmed | executed: W exit 0, Wc exit 0, Ww exit 1 naming `docs/b.md` at the target; the one-shape wording beside it is ⬜ 1 |
| carried | round 1's finding 3 is closed — the records say step A's gate row was left as written | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md:23` | confirmed | carried from round 2 and not re-derived: the fix range does not touch `questions.md`; the sweep over `ab9b026b..e5dc540d` with `survivors.md` exit 0, 21 sentences, nothing standing |
| carried | round 1's finding 4, a file moved whole writes the corrected wording it quotes | `skills/code-review/scripts/survivor_check.py:1054` | deferred #563 | already deferred in round 1; not re-run, and the fix range does not touch the rename reading |
| carried | round 1's findings 5–7: the fragment path spelled two ways, a fragment's own `## ` heading, a CRLF changelog | `skills/code-review/scripts/survivor_check.py:1016` | deferred #564 | already deferred in round 1; not re-run, and the fix range does not touch `a_gathered_fragment`, `newly_released` or `gathered_fragments` |
| ❓ | the other modules that load the sweep and the hygiene modules were not re-run this round | `tests/` | ❓ out of verified scope | the orchestrator reports `150 passed` at `e5dc540d`; this round ran the one module. Who answers it: the sealer, whose full suite covers them |

## Paste-ready fixes

```
because that rewording is the fragment's branch's wording. Since round 2's
fix it is silent whether or not the rewording shares wording with what
`CHANGELOG.md` lost: the shared n-grams split `CHANGELOG.md`'s own removed
sentences and never another file's (round 3's Y1, exit 1 at `61f0d0d8` and
`e6c85df6`, 0 at `7bc34064`; its controls, wording that stood before the
range exit 0 and wording the range wrote exit 1, in every state).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -p no:xdist` in the clone at `7bc34064` | 104 passed, exit 0 |
| The same module, `-k` the new case, with `ab9b026b`'s `survivor_check.py` swapped in, then `git checkout` | exit 1, 1 failed, 103 deselected; `exit 0` and `against 3 sentence(s)` in the assertion message; `git status` clean after |
| The module with the `CHANGELOG` test in `score` made true for every source (via `Edit`) | exit 1, 1 failed (the new case), 103 passed |
| The module with `mine -= split` replaced by `pass` (via `Edit`), then `git checkout` | exit 1, 1 failed (X5), 103 passed; `git status` clean after |
| Fifteen shapes at `61f0d0d8`, `bf7ba905`, `e6c85df6` and the target (a Python probe importing the module's own fixtures and driving git per contract §8, deleted) | see the table below |
| Y1, Y1w, Y1c at `61f0d0d8`, `e6c85df6` and the target (the same kind of probe, deleted) | Y1: 1b, 1b, 0; Y1w: 1b, 1b, 1b; Y1c: 0, 0, 0 |
| `uvx ruff check` and `uvx ruff format --check` over `survivor_check.py` and the module | exit 0 and exit 0 |
| `bin/survivor-check --range ab9b026b..e5dc540d --exempt` this work item's `survivors.md` | exit 0; 408 files, 21 sentences; nothing standing |
| `bin/evidence-check --strict .` over this report's copy in the clone | exit 0; see the proof block |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it on this branch, and it is the sealer's |

```
shape      base       bf7       e6c    target
P6           1b        1b        1b        1b
P6d          1b        1b        1b        1b
H1k           0        1b        1b        1b
H1            0        1b        1b        1b
H1c          1b        1b        1b        1b
H2k           0        1b        1b        1b
H2            0        1b        1b        1b
X5           1b         0        1b        1b
X5W          1b         0        1b        1b
W            1b         0         0         0
Wc            0         0         0         0
Ww           1b        1b        1b        1b
Z1            0        1b         0        1b
Z2            0        1b         0        1b
Z1n          1b        1b        1b        1b
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:1047` | round 1's 🟡 1 — fixed |
| round-1 | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | round 1's ⬜ 2 — answered |
| round-1 | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md:23` | round 1's ⬜ 3 — answered |
| round-1 | `skills/code-review/scripts/survivor_check.py:1054` | round 1's ⬜ 4 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:1016` | round 1's ⬜ 5 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:554` | round 1's ⬜ 6 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:810` | round 1's ⬜ 7 — deferred |
| round-1 | `tests/test_a_corrected_sentence_survives_elsewhere.py` | round 1's 🟢 — confirmed |
| round-1 | `tests/` | round 1's ❓ — out of verified scope |
| round-2 | `skills/code-review/scripts/survivor_check.py:1062` | round 2's 🟡 1 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — the report-less class since round 2's fix is W and Y1, not W alone; `plan.md:144`, `overview.md:53` and ledger row H1's note give W a reason that no longer decides it | #563, joined by a comment the orchestrator files, carrying Y1 and its two controls beside W, Wc and Ww, and the replacement wording below | the repository owner, who decides whether a gathered rewording counts as written by the release that gathers it; the same issue's fix corrects the three sentences |
