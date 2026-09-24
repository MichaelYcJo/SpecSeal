# Round 3 report — a release writes the gathered text back

Target SHA: `7bc34064` · base `61f0d0d8` · the verifying round, and the
terminal record of a run capped at the reopening bound. Its target is round
2's fix range `ab9b026b..e5dc540d` (d66b9632, e5dc540d); `7bc34064` changes
`rounds/round-2.md` alone. Read and run in a `git clone --no-local` at the
target, under this round's scratch directory. Nothing was written in the main
checkout except this file.

## Summary

Round 2's fix does what round 2 asked. The split is now `corrected`'s third
return, `score` subtracts it only where the source sentence is in
`CHANGELOG.md`, and `examine` is the only caller of either. The new case is
red with d66b9632's parent script and green at the target. Every shape round
2 tabled answers at the target exactly as round 2's per-source column
predicted.

This round opened one thing, and it is paperwork, not the tool:

1. **The records describe the one report-less shape by a condition that no
   longer decides it.** `plan.md` phase 1, the overview and ledger row H1
   say the shape is silent because the gathered rewording *shares nothing
   with what `CHANGELOG.md` lost*. Since round 2's fix, sharing with the
   changelog's loss no longer lets gathered wording split another file's
   sentence, so a second shape (Y1 below) is silent too. The behaviour is
   the rule the fix states. The sentence describing it is narrower than the
   rule (⬜ 1).

Nothing needs a fix, and nothing loses a record or crashes.

## What the fix range changed, read against the code

- **Where the split is built** (`skills/code-review/scripts/survivor_check.py:1033`,
  `:1068-1070`, `:1077`): read. `moved` is non-empty only inside
  `if path == CHANGELOG and path in after:` (`:1038-1043`), so `held` is
  empty for every other path. `split` therefore only ever holds n-grams of
  a gathered sentence that also occur in a sentence `CHANGELOG.md` itself
  lost. `written` no longer receives any of them.
- **Where the split is subtracted** (`:1187-1190`, `score`): read.
  `source.path == CHANGELOG` compares the path `corrected` read from
  `git diff --name-only`, which is repository-relative, against
  `"CHANGELOG.md"`. A nested `docs/CHANGELOG.md` never matches, and it never
  receives `moved` in `corrected` either, so the two tests agree on which
  file is the changelog.
- **No other source can be scored against the split.** Read: `score` is the
  only reader of `split`, and the subtraction sits inside the `CHANGELOG`
  test. `keep` (`wanted`) still contains the split n-grams, so `carriers`
  still finds their candidates and every other file's removed sentence is
  scored with them in place. That is the fix's point. `split` defaults to
  `frozenset()`, so a caller that omits it scores as before the fix.
  Executed: a repository-wide search for calls to `corrected(`, `score(`,
  `.examine(` and `.survivors(` finds only `examine`'s two lines.
- **The docstrings and comment** (module docstring `:174-178`, `corrected`'s
  docstring, the comment at `:1060-1067`, the comment at `:1188-1189`): read
  against the code. Each says what the code does.
- **The case** (`tests/test_a_corrected_sentence_survives_elsewhere.py:3085`):
  round 2's paste-ready case, byte for byte. Executed: red with d66b9632's
  parent script swapped in (1 failed, `exit 0`, `against 3 sentence(s)`),
  green at the target, module 104 passed.
- **The paperwork** (e5dc540d: `plan.md` phase 1 and its alternatives row,
  `spec.md` §*Out*, `overview.md`, ledger H1, H3 and step A's F1, the
  `seal/ledger.md` rows re-anchored on `corrected` and `score`): read as a
  word diff. Every row that said the split n-grams are *written* now says
  they are subtracted from `CHANGELOG.md`'s removed sentences alone. The
  re-anchored rows add a dated re-read note and leave their claims
  unchanged. H1's own clause (*no gathered text subtracts another file's
  sentence*) is true at the target. ⬜ 1 is about the open-shape paragraph
  beside that clause, not the clause.

The orchestrator's six-mutation account is a claim. Two of the six were
re-run here and agree: `mine -= split` removed turns X5 alone red, and the
`CHANGELOG` test made true for every source turns the new case alone red.
The other four were not re-run.

## Findings

### ⬜ 1 — the report-less shape is described by a condition the fix made irrelevant

`seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144`,
and the same sentence in `overview.md:53` and in ledger row H1's note
(`seal/ledger/1790221963-a-release-writes-the-gathered-text-back.md`, row
H1). Each describes the one shape that reports less than the base as
a sentence deleted from another file whose only rewording is a gathered
fragment's, and gives the reason as *that rewording shares nothing with what
`CHANGELOG.md` lost, so it is held and never written*. The reason implies
that a gathered rewording which does share wording with the changelog's loss
would split the other file's sentence. That was true at `e6c85df6`, and it
is exactly what round 2's fix removed.

**Executed** (throwaway repositories, exit codes read directly, `b` = the
report names `docs/b.md`). Shape Y1: `docs/a.md` deletes a sentence outright
and `docs/b.md` quotes it. The release renames `## Unreleased`, whose live
entry shares a four-word phrase with that sentence, and gathers a fragment
carrying the same phrase. Two controls: Y1w, where the range itself writes
the fragment's sentence into `docs/c.md`, and Y1c, where that sentence
stands in `docs/c.md` before the range.

| Shape | base `61f0d0d8` | `e6c85df6` | target `7bc34064` |
|---|---|---|---|
| Y1 | 1 b | 1 b | **0** |
| Y1w | 1 b | 1 b | 1 b |
| Y1c | 0 | 0 | 0 |

At the target, Y1 behaves like Y1c, wording that stood before the range. It
does not behave like Y1w, wording the range wrote. That is round 2's
judgment of W carried one step further, and it is the rule ledger row H1's
clause now states. So the code is right. What is wrong is the description.
Two report-less shapes stand where the records name one, and the reason the
records give would lead a reader to expect Y1 to report.

**Why it matters.** The repository owner is asked to decide whether a
gathered rewording should count as written by the release that gathers it
(`overview.md`, `spec.md` §*Out*). That decision covers Y1 as well as W, and
the records present it as covering W alone. The release does not ship a
defect if this stands, so it is ⬜. Its location is under `seal/specs/` and
`seal/ledger/`, so it is a correction and not counted in `Needs a fix`. The
run is capped, so it goes to a new issue rather than to this branch.

## Executed separately from read

- **Executed**: the module at the target; the new case with d66b9632's
  parent script swapped in; two mutations of `score`; fourteen round-2
  shapes plus X5W at four script states; Y1 and its two controls at three
  script states; `ruff check` and `ruff format --check` over the two changed
  Python files; the sweep over the fix range with this work item's
  `survivors.md`; `evidence-check --strict` over this report's copy in the
  clone.
- **Read**: the whole fix diff; `corrected`, `wanted`, `carriers`, `score`,
  `examine`, `Sentence` in full; the test helpers `build`, `changelog`,
  `run`, and the cases G1–G6, X5 and the new case; the paperwork diff as a
  word diff; rounds 1 and 2's records and reports.
- **Not re-run, claimed by the orchestrator**: four of the six mutations
  (guard off, filter off, both off, split written back); the hygiene modules
  (`150 passed` at e5dc540d, module included). The ❓ row carries the second.

## Regression tests to plant

None. This round commissions nothing (the run is capped at the reopening
bound). Y1 is the rule working. If the owner decides a gathered rewording
counts as written, Y1 and W become the cases for that change, and the new
issue carries their shapes.

## Facts for the evidence ledger

- At `7bc34064`, `split` is non-empty only for `CHANGELOG.md`, because
  `moved` is filled only for that path. `score` subtracts it only from a
  source whose path is `CHANGELOG.md`, so a gathered sentence never changes
  how another file's removed sentence is scored. Executed as Y1 against Y1c.
- The report-less class since round 2's fix: a sentence deleted from a file
  other than `CHANGELOG.md` with no rewording of its own, where the only
  rewording is gathered. It is silent whether or not that rewording shares
  wording with what `CHANGELOG.md` lost (W, Y1). This belongs in ledger row
  H1's note, replacing the *shares nothing* reason.

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

### The shape table

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

P6, P6d, H1k, H1, H2k, X5 and Z1 are built as the module's cases build them.
H1c, H2, X5W, W, Wc, Ww, Z2 and Z1n were rebuilt from rounds 1 and 2's
descriptions, because round 2's probe was deleted. Wc and Ww here keep the
release but gather nothing. Every cell matches round 2's table, with the
target column matching round 2's per-source column.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — the report-less class since round 2's fix is W and Y1, not W alone; `plan.md:144`, `overview.md:53` and ledger row H1's note give W a reason that no longer decides it | #563, joined by a comment the orchestrator files, carrying Y1 and its two controls beside W, Wc and Ww, and the replacement wording below | the repository owner, who decides whether a gathered rewording counts as written by the release that gathers it; the same issue's fix corrects the three sentences |

## Paste-ready fixes

### ⬜ 1 — the open-shape sentence, for the new issue

For ledger row H1's note, replacing *because that rewording is the
fragment's branch's wording and shares nothing with what `CHANGELOG.md`
lost*. `plan.md:144` and `overview.md:53` take the same change.

```
because that rewording is the fragment's branch's wording. Since round 2's
fix it is silent whether or not the rewording shares wording with what
`CHANGELOG.md` lost: the shared n-grams split `CHANGELOG.md`'s own removed
sentences and never another file's (round 3's Y1, exit 1 at `61f0d0d8` and
`e6c85df6`, 0 at `7bc34064`; its controls, wording that stood before the
range exit 0 and wording the range wrote exit 1, in every state).
```

Needs a fix: no
Loses a record or crashes: no

The gate has come due. This report leaves nothing open that this branch
fixes: ⬜ 1 is a paperwork correction deferred to a new issue, and the ❓ row
is the sealer's. What comes due is the sealer's spawn at `7bc34064`.

## Proof block

Files opened this round, in the clone at `7bc34064` unless marked:
`skills/code-review/scripts/survivor_check.py` (the fix diff; `corrected`,
`wanted`, `carriers`, `score`, `examine`, `survivors`, `Sentence` in full;
the `CHANGELOG` and `READER` constants; the import block);
`tests/test_a_corrected_sentence_survives_elsewhere.py` (the header, `run`,
`resolves`, `build`, `FOUND`, `REPAIRED`, `FILLER`, `RELEASED_HEADINGS`,
`SHIPPED`, `FRAGMENT`, `changelog`, `two_sections`, G1–G6, X5 and the new
case); `bin/test`; `.github/scripts/run_tests.py` (the virtualenv lines);
in the main checkout, this work item's `rounds/round-1.md` (the verdict
table), `rounds/round-1-report.md` (the shape lines), `rounds/round-2.md`
and `rounds/round-2-report.md` in full, `overview.md:40-70`, the e5dc540d
diff of `plan.md`, `spec.md` and `overview.md`, the word diff of
`seal/ledger.md` and `seal/ledger/`, and ledger rows H1–H3 of this work
item's fragment; `seal/specs/…/questions.md`, `spec.md` and
`phases/phase-1.md` and `phase-3.md` by search only. Nothing was posted,
pushed or committed. The probe files, the swapped scripts and the throwaway
repositories were deleted, and the clone's `git status` was clean after
every swap.
