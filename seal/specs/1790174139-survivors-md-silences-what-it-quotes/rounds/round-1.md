# 1790174139-survivors-md-silences-what-it-quotes — review round 1

| Field | Value |
|---|---|
| Target SHA | bc38c8f37e0ada75808f105e870d1ca6452be827 |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 539 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `e7dacbf896662667530ab07c72f7b6f6caffac13..09292fa8988915727a527e7bd3cec934e817f7b4`, 2 commits |
| Contract changes | test_a_phase_record_standing_in_the_pool_is_not_a_survivor → round-1-report.md, round-1.md |
| New units | none |
| Needs a fix | yes — 🟡 1, the second arm of the S6 pool case, seen red on the `named` assertion under the `phases/` arm removed before it is committed; the four ⬜ rows are paperwork corrections and are not counted here |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the survivor sweep, the whole branch `fix/308-survivors-md-silences-what-it-quotes` against `release/v0.15.0`: four tickets in three code phases and one record phase, #507 and #308, #460, #304. Stage 1 asked whether the build follows `spec.md`: one predicate, `records_a_past_state`, puts a work item's `survivors.md` and its `phases/` out of both sides of the sweep, the range and the pool, so an exemption row is read against a found survivor rather than subtracted from the search; and a `survivors.md` one directory deeper belongs to the work item above it. Stage 2 asked four things:

- whether the three-range re-measurement (7 → 14 rows read on #525, 0 on the other two, unchanged by the file's presence) reproduces from the committed tree, and whether the branch's own sweep over `origin/release/v0.15.0...HEAD` finds nine and excuses nine on grounds that hold
- whether the eight new cases go red under the mutations `phases/phase-{1,2,3}.md` name, and whether the S6 case pins both directions of the pool-side defect (dilution to exit 0 and the phase record reported)
- whether the `seal/follow-up.md` row phase 2 writes names what the sweep gives up and who answers, and whether the row phase 1 removes was the range-half row and nothing else
- whether the five places that vanish through a live file on #525's range (`overview.md` §Not done) are the class `spec.md` §Out keeps in on purpose, or a defect this fix should have caught

The hand-back labelled the broad gate unverified; the sealer answers that after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The S6 pool case asserts both directions but only dilution can turn it red on its fixture; the `named` assertion has never failed | `tests/test_a_corrected_sentence_survives_elsewhere.py` `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` | **fixed** `d3e544d6` | fixed at d3e544d6 — `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` parametrised over a 4-file and a 33-file pool; with the `phases/` arm removed both arms go red on their own assertion (`[0]`: exit 0, nothing named; `[29]`: the record named beside `guide.md`), restored and green. The ⬜ corrections went in `09292fa8`: `overview.md`'s `Ran by` row closed, `phases/phase-4.md` and ledger E1 read 6/6, the memo's "13 cases" reads "eleven red runs over ten cases (6+4+1)", E3 re-read with the mutation in the phase-2 table; the fourth ⬜ is not a defect and was not edited. The orchestrator re-ran at `09292fa8`: module 70 passed, `evidence-check --strict` exit 0, tree-wide ruff clean, CI-form sweep nine excused; Executed: `phases/` arm removed → 4-file pool exit 0 nothing named, 33-file pool exit 1 naming `guide.md` and the record. Ledger E3 and `overview.md` claim both directions pinned. Paste-ready fix below |
| 🟢 | One predicate, `records_a_past_state`, at both call sites and nowhere else; `whole_range`'s list unfiltered; `records_a_past_round` untouched | `skills/code-review/scripts/survivor_check.py` `#records_a_past_state`, `#corpus`, `#corrected` | answered | Read; the path-list case green; 5 mutations red at the counts above; no other caller in the tree |
| 🟢 | A row is read against a found survivor and printed, never subtracted from the search | the branch's own range, `seal/specs/1790174139-survivors-md-silences-what-it-quotes/survivors.md` | answered | Executed: nine standing at exit 1 without `--exempt`, nine `exempt` at exit 0 with it, every grounds a row's; seven rows cover nine places by normalised-word matching, as `exempted` documents |
| 🟢 | The three-range re-measurement reproduces, the file's presence changing nothing | `phases/phase-1.md`, `phases/phase-2.md`, ledger row E2 | answered | Executed: 14 / 0 / 0 with `--exempt`, without, and with the file deleted at the tip in a scratch clone driven from Python |
| 🟢 | A deeper exemption file is owned and refused with `not yours`; the layout position is unchanged | `survivor_check.py#OWNER_DIR`, the parametrised case | answered | Read the pattern and `whole_range`; executed: the old tail turns the `[deeper/]` arm red and leaves `[]` green |
| 🟢 | The follow-up row removed is the range-half row and nothing else; the row added names the loss and the repository owner | `seal/follow-up.md` | answered | Read the diff: one row out, one row in, the answerer cell reads *the repository owner* |
| 🟢 | The five places on #525 are the class `spec.md` §*Out* keeps in, and on this range not a defect at all | `overview.md` §*Not done* | answered | Executed in-process: all five share one source, `seal/ledger.md:78`, whose phrases the item's ledger fragment carries at the tip — the sentence was moved, not corrected |
| ⬜ | `overview.md` §*Not verified* says the `Ran by` cells read `unknown`; they name the smith since `bc38c8f3` | `seal/specs/1790174139-survivors-md-silences-what-it-quotes/overview.md`, *Not verified* row 2 | answered | Correction for the orchestrating session: close the row |
| ⬜ | Mutation counts recorded as 3 and 5 measure 6 and 6 | `phases/phase-4.md` §*Mutations*; `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` E1 | answered | Correction; executed counts above, the path-list case red in both |
| ⬜ | *13 cases seen red first* does not follow from the phase records' 6 + 4 + 1 | `overview.md` line 12 | answered | Correction; the smith says what was counted or writes eleven |
| ⬜ | A deeper `survivors.md` is owned for range rows and still in the sweep for path rows | `survivor_check.py#records_a_past_state` | not a defect | Stated intent found in `spec.md` §*Data & interfaces*, the docstring and `phases/phase-3.md` S8; hand-run only; recorded so the asymmetry is not mistaken for an oversight |
| ❓ | Tree-wide `ruff check` and `ruff format --check`, and the full suite | the repository | out of verified scope | Not run in this round on §2 grounds; the hand-back labels them the sealer's and the orchestrator says it ran ruff at `bc38c8f3`. The sealer answers |

## Paste-ready fixes

```python
@pytest.mark.parametrize("fillers", [0, 29])
def test_a_phase_record_standing_in_the_pool_is_not_a_survivor(tmp_path, fillers):
    """The pool half, and the one #460 paid for twice in one pass: a record
    carrying the removed wording was reported beside the real survivor, and
    answering it meant editing a record of a past state.

    Two pools, because the two directions of the defect need different sizes
    to show. On four files a fourth carrier halves every quoted phrase's
    weight and nothing clears the floor -- the record silences the survivor
    (exit 0). On 33 files the halving is small enough that both carriers
    clear it -- the record is REPORTED beside the survivor, which is what
    #460 measured in the tree. The `named` assertion is the only one that
    catches the second; the `code` assertion is the only one that catches
    the first."""
    repo = tmp_path / "probe"
    os.makedirs(repo, exist_ok=True)
    files = {
        "notes.md": f"# notes\n\nFirst statement. {FOUND}\n",
        "guide.md": f"# guide\n\nSecond statement. {FOUND}\n",
        "filler.md": "# filler\n\nUnrelated prose that shares nothing.\n",
        PHASE: phase_record(FOUND),
    }
    for index in range(fillers):
        files[f"filler-{index}.md"] = (
            f"# filler {index}\n\nUnrelated prose number {index} that shares nothing at all.\n"
        )
    build(
        repo,
        files,
        "the claim in two files, and an earlier phase's record quoting it",
    )
    head = build(
        repo,
        {"notes.md": f"# notes\n\nFirst statement. {REPAIRED}\n"},
        "corrected notes.md only",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        f"guide.md's copy went unreported on a pool of {fillers + 4}; exit {code}\n{text}"
    )
    named = paths_in(text)
    assert "guide.md" in named, f"the report does not name the survivor:\n{text}"
    assert named == ["guide.md"], (
        f"the report names {named} on a pool of {fillers + 4}. A phase record "
        "quotes what a phase found and instructs nobody, so reporting it asks "
        f"somebody to correct a record of a past state:\n{text}"
    )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `bc38c8f3` | exit 0, 69 passed |
| `bin/survivor-check --range <base>...HEAD --exempt seal/specs/1790174139-survivors-md-silences-what-it-quotes/survivors.md` | exit 0, 9 `exempt`, `every survivor is excused by a row above (9)`, 371 files, 36 removed sentences |
| the same without `--exempt` | exit 1, 9 standing, the same nine coordinates |
| `--range f8f1c9d..edd022a` with and without `--exempt` (the #525 file) | exit 0 with 14 `exempt` / exit 1 with 14 standing; `against 162 sentence(s)` both |
| `--range c626382..24ea206` and `--range edd022a..c626382`, with and without | exit 0, 0 `exempt`, 0 standing, all four runs |
| #525 with the exemption file deleted at the tip in a `git clone --shared` driven from Python, then removed | exit 1, 14 standing without; exit 0, 14 `exempt` with the worktree's file |
| Q3 in-process: `records_a_past_state` widened for one run over #525's `overview.md`, `changelog.md`, ledger fragment | 14 shipped, 19 widened, 5 only when widened; all 5 sourced at `seal/ledger.md:78`, subtracted through the item's ledger fragment |
| mutation: `survivors.md` arm removed | 4 red |
| mutation: `phases/` arm removed | 3 red |
| mutation: `OWNER_DIR` tail back to `[^/]+$` | 1 red (`[deeper/]`), `[]` green |
| mutation: `corpus` back on `records_a_past_round` | 6 red |
| mutation: `corrected` back on `records_a_past_round` | 6 red |
| S6 pool fixture, 4 files and 33 files, shipped module | exit 1 naming `guide.md`, both |
| S6 pool fixture, 4 files and 33 files, `phases/` arm removed | 4 files: exit 0, nothing named · 33 files: exit 1 naming `guide.md` and the phase record |
| `bin/evidence-check --strict .` | exit 0, 0 drifted, 0 broken; six `Re-read 2026-09-24 by work item 1790174139` notes |
| `bin/unverified-check --baseline <base> seal/specs/` | exit 0, three open rows on this memo |
| `bin/test tests/test_no_real_identifiers.py -q` (coverage probe over the new records) | exit 0, 5 passed |
| the probe's leavings | module bytes compared equal after every mutation, scratch clone and fixture repositories removed, `git status` in the clone empty, the probe file deleted |
| Broad gate — full suite, tree-wide `ruff check`, `ruff format --check` | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
