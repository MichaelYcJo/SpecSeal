# Round 1 report — survivors.md silences what it quotes

Target SHA `bc38c8f37e0ada75808f105e870d1ca6452be827`, base `cbb58091fddb9a02e3136156d7963dcd66798d1b`, the whole branch `fix/308-survivors-md-silences-what-it-quotes` (eleven commits). Reviewed in a `git clone --no-local` of the worktree at the target SHA, with the base fetched from the main checkout under a second remote; nothing was written in the worktree except this file. Reviewer: `specseal:warden`. There is no earlier round record for this work item, so nothing is carried from one; the coordinates carried are the ones `spec.md`, `plan.md` and the four phase records name, and each was opened.

Every claim below is labelled **executed** (I ran it, in the clone, exit code read directly), **read** (I opened the code or the record), or **unverified** (nobody in this round ran it, and the answerer is named).

## The verdict in one paragraph

The build follows `spec.md`. One predicate, `records_a_past_state`, is applied at both call sites and nowhere else; it is true for a round record, for `survivors.md` directly under a work item directory, and for anything under that directory's `phases/`; `OWNER_DIR` reads the owner off the `seal/specs/<id>` prefix at any depth. Every executed number in the hand-back reproduces from the committed tree: 69 cases green, nine standing and nine `exempt` on the branch's own range, 14 / 0 / 0 on the three pull-request ranges in every state including the file deleted at the tip, five places on #525 that vanish only through a live file, and the mutations red. One finding needs a fix, and it is in a test rather than in the tool: the S6 pool case asserts both directions of the pool-side defect but on its own four-file fixture only the dilution direction can ever turn it red; a 32-file pool makes the other direction the one that bites, and it is a one-parameter change. Four corrections to the run's paperwork are listed as ⬜. Nothing found leaves the root or crashes.

## Stage 1 — does the build follow `spec.md`

**The predicate, and both call sites** (read, `skills/code-review/scripts/survivor_check.py#records_a_past_state`, `#corpus`, `#corrected`). The function calls `records_a_past_round` first, then reads the segments after `specs/<id>/`: true when they are exactly `["survivors.md"]`, or when the first is `phases` and there is at least one more. `corpus` filters `tracked()` by it and `corrected` filters the `git diff --name-only` list by it, before `retired_directories` and before either side of the range is read, so the exclusion holds on the removed side and the added side alike. `whole_range`'s changed-file list is unfiltered, which `spec.md` §*Data & interfaces* requires and `test_every_path_list_this_module_derives_from_git_is_filtered_or_named` pins with its `NAMED_EXCEPTION`. `records_a_past_round` is byte-for-byte what it was, so `seal/ledger.md` row S6 of `1788873640` still anchors on an untouched function. A grep over the tree finds no other caller of either predicate.

**What the new arms remove from the pool** (executed, `git ls-files` in the clone): seven `seal/specs/<id>/survivors.md` files and 25 files under `seal/specs/<id>/phases/`, and no tracked file outside `seal/specs/` matches either shape. The reach the phase-1 record describes for a `docs/specs/<name>/` path is the existing predicate's and is not exercised by anything tracked today.

**A row is read against a found survivor rather than subtracted from the search** (executed, the branch's own range, below): nine places stand without `--exempt` at exit 1 and the same nine print under `exempt` with it at exit 0, each with the grounds of a row in this item's file. That is the property the three pull requests lost, holding on the first exemption file written on a range the fix checks.

**A deeper `survivors.md` belongs to the work item above it** (read, `OWNER_DIR`, `whole_range`; executed, the parametrised case). The tail is `.+$`; `whole_range` is unchanged and asks the ownership question of whatever the pattern hands it. The `[deeper/]` arm is the one the old tail turns red (mutation table below), the `[]` arm is green under both tails.

**Unchanged on purpose** (read): `.github/workflows/hygiene.yml` still globs `seal/specs/*/survivors.md` one level deep; `docs/`, `skills/code-review/orchestration.md`, `agents/smith.md`, `templates/` and `bin/survivor-check` are untouched in the diff. `docs/review-chain-spec.md`'s folded statement at line 2011 says a round record is outside the corpus on both sides and does not say *only* a round record, so no policy sentence became false.

## Stage 2 — the four questions

### 1. The re-measurement, and the branch's own sweep

**Executed**, in the clone at `bc38c8f3`, the module driven from Python with each exemption file passed by its path in the clone:

| Range | Rows | With `--exempt` | Without | Removed sentences |
|---|---|---|---|---|
| #525 `f8f1c9d..edd022a` | 29 | exit 0, **14** `exempt`, 0 standing | exit 1, **14** standing | 162 in both runs |
| #528 `c626382..24ea206` | 4 | exit 0, 0 | exit 0, 0 | 5 |
| #527 `edd022a..c626382` | 3 | exit 0, 0 | exit 0, 0 | 8 |

Every one of #525's fourteen `exempt` lines carries grounds found verbatim in that item's file (counted by the probe against the file's text). The `against N sentence(s)` count is the same with and without the file, which is S1's third condition on a real range.

**The file deleted at the tip** (executed): a `git clone --shared` of the clone, `edd022a` checked out, the #525 exemption file removed in one further commit driven from Python, range `f8f1c9d..<probe tip>`: exit 1 with **14** standing without `--exempt`, exit 0 with **14** `exempt` when the worktree's copy of the file is passed. Neither count moves. The scratch clone was removed before the probe returned.

**The branch's own sweep** (executed, `bin/survivor-check --range <base>...HEAD` spelled with the clone's second remote, `--exempt seal/specs/1790174139-survivors-md-silences-what-it-quotes/survivors.md`): exit 0, nine `exempt` lines, `every survivor is excused by a row above (9)`, over 371 files and 36 removed sentences. Without `--exempt`: exit 1, the same nine coordinates standing. Seven rows excuse nine places because the row quoting *A fix pass may not add mechanism, which is why this is a row* matches three lines of `seal/follow-up.md` (65, 80, 81) on normalised words, which `exempted` is documented to do, and the file's preamble counts them as it should: eight carriers of the deleted follow-up row's wording and one ledger row recording a red message the case no longer prints. The `corrected` column of the report confirms the split: eight name `seal/follow-up.md:62` as the source and one names `tests/test_a_corrected_sentence_survives_elsewhere.py:649`. I read each of the seven grounds cells against its standing line and each says why the place is right where it stands; none is a *check nothing*.

### 2. The eight new cases under mutation, and what S6 pins

**Executed**, five of the eight mutations the phase records name, each applied to the module's text on disk in the clone, the full module run with `pytest -q -p no:cacheprovider` after clearing the bytecode cache directories beside the module and the tests, the bytes restored and compared afterwards:

| Mutation | Red |
|---|---|
| the `survivors.md` arm removed | 4 — the four exemption-file cases |
| the `phases/` arm removed | 3 — the three phase-record cases |
| `OWNER_DIR` back to `[^/]+$` | 1 — the deeper arm of `test_a_declaration_one_directory_deeper_still_has_an_owner`; the layout arm green |
| `corpus` back on `records_a_past_round` | **6** — S1, S2, S3, both phase-record pool-side cases, and `test_every_path_list_this_module_derives_from_git_is_filtered_or_named` |
| `corrected` back on `records_a_past_round` | **6** — S1, S3, S4, both phase-record range-side cases, and the same path-list case |

The three docstring mutations (the class collapsed to round records, each new paragraph's opener broken) were not re-run here; the record's claim for them is **read**. The two counts in bold differ from the record — `phases/phase-4.md` and ledger row E1 say 3 and 5 — and the difference is in the direction that costs nothing (more red than recorded). It is a correction to the paperwork, ⬜ below.

**Whether S6 pins both directions** (executed). `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` asserts `code == 1` and then `named == ["guide.md"]`. On its fixture — three prose files plus the record — a fourth carrier halves every quoted phrase's weight, the total falls to 1.0 under the 1.6 floor, and the `phases/` arm removed produces exit 0 with nothing named: the first assertion fails and the second is never reached. The reported-record direction the frame named cannot occur on that pool at all. It needs a pool of 32 files or more: with `F` files and two carriers the weight is `log2(F / 2) / log2(F)`, two runs clear 1.6 only when that is at least 0.8, which is `F >= 32`. I built the same fixture with 29 filler files and ran it under both modules:

| Pool | Shipped module | `phases/` arm removed |
|---|---|---|
| 4 files (the case as committed) | exit 1, names `guide.md` | exit 0, names nothing |
| 33 files | exit 1, names `guide.md` | exit 1, names `guide.md` **and** the phase record |

So the case as committed has been seen red in one direction only, and its second assertion has never been the one that failed. Ledger row E3 claims the pool half both ways — *neither reported nor a carrier that dilutes* — and `overview.md` §*diverged* says *the case pins both*. The code does the right thing on both pools; what is missing is the arm that lets the `named` assertion bite. Finding 🟡 1, paste-ready fix below: parametrise the case over the two pool sizes, and the smith sees the 33-file arm red by its own assertion before it is committed (§15).

### 3. The follow-up rows

**Read**, `git diff <base>...HEAD -- seal/follow-up.md`: exactly one row removed and one added. The removed row opens *Writing a `survivors.md` row silences its survivor a SECOND way, and that way does not rot* and its body is the range half — `corrected` reading the quote as wording the range added and `wanted` subtracting its n-grams. Nothing else leaves the file. The added row, under *Schedulable items with nowhere else to go*, names what the sweep gives up (a correction inside an HTML comment beside a claim still rendered in bold, caught in #423's pass only because phase records were in the pool), names the refused narrower answer with its grounds, states the two options, and its answerer cell reads *the repository owner*. That is the row `spec.md` §*Data & interfaces* asked for.

### 4. The five places that vanish through a live file on #525's range

**Executed**, in-process, the module imported from the clone and `records_a_past_state` widened for one run to also exclude #525's `overview.md`, `changelog.md` and ledger fragment: 14 candidates shipped, 19 widened, five appear only when widened, at the coordinates `overview.md` §*Not done* lists (`docs/review-chain-spec.md:392` at 2.93, `tests/test_the_last_rounds_fixes_are_checked.py:8` at 2.74, `skills/code-review/SKILL.md:210` at 1.87, `docs/review-chain-spec.md:845` at 1.76, `skills/code-review/orchestration.md:263` at 1.63). The scores differ from the phase-1 record in the second decimal for two of them, which the phase-2 record already explains (a score moves when the pool shrinks; the coordinates are what the record compares).

Then the question the round was asked. All five have the same source, `seal/ledger.md:78` at the range's start — the sentence beginning *The first is `1788137177-the-axis-nobody-was-asked`, where round 2 found seven defects inside round 1's fixes and round 2's own then went in unread* — and for every one of the five the phrases it shares with that source are carried at the tip by `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md`, the ledger fragment #525 wrote. The range did not correct that sentence; it moved it out of the shared ledger into the item's fragment, and the fragment is a live statement standing at the tip. *A phrase the fix kept is not a phrase the fix corrected* is exactly the rule that subtracts them, and reporting them would name five coordinates nobody should be asked to correct — a false name that spends a round, which is the failure #365 named. They are the class `spec.md` §*Out* keeps in on purpose, and on this range they are not a defect the fix missed; they are the sweep being right. `overview.md` §*Not done* records the count for the repository owner, which is where `questions.md` Q3 sends it. Confirmed, 🟢 below.

## The hand-back's other claims, checked

- **69 passed** (executed): `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone, exit 0 read directly, 69 passed in 18 s. The runner built the clone's own venv, which is the repository's tooling and not a leaving of mine.
- **`evidence-check --strict` exit 0** (executed): `bin/evidence-check --strict .` in the clone, exit 0, 0 drifted, 0 broken. The six `seal/ledger.md` rows the plan named each carry a `Re-read 2026-09-24 by work item 1790174139` note (six occurrences, counted). Only hashes and the notes changed in that file — six rows removed and six added in the diff, the same six.
- **`unverified-check --baseline` exit 0** (executed): exit 0, three open rows on this item's memo, each with an answerer.
- **The identifier rule over the new records** (executed, coverage probe, the one module): `bin/test tests/test_no_real_identifiers.py -q`, exit 0, 5 passed.
- **Tree-wide `ruff check` and `format --check`** (unverified here): the hand-back says the orchestrator ran them at `bc38c8f3`; I did not, on §2 grounds. The sealer's.
- **The frame's read claim about #528** (executed): the four rows match nothing over `c626382..24ea206` in any state, so the divergence row in `overview.md` stands.
- **Q2's 14 of 29 consulted** (executed): fourteen `exempt` lines against the 29 rows, and each carries a row's grounds. I did not re-derive which 22 rows are dead beyond the count.

## Findings

### 🟡 1 — the S6 pool case can only go red by dilution, so its second assertion has never been seen red

`tests/test_a_corrected_sentence_survives_elsewhere.py`, `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` (the `assert named == ["guide.md"]` line). On the four-file pool the `phases/` arm removed yields exit 0 and the `code == 1` assertion fails first, every time; the assertion that refuses the record being named cannot be reached. With 29 filler files the same mutation reports the phase record beside `guide.md` at exit 1, and then only the `named` assertion catches it. The claim in ledger row E3 (*neither reported nor a carrier that dilutes*) and in `overview.md` (*the case pins both*) is therefore half-evidenced, and a future change that keeps phase records in the pool while the floor or the weighting moves would pass this case with the record reported. Why it matters: the direction the spec named for S6 is the one #460 measured in the tree — a record reported beside the real survivor — and it is the direction with no red behind it. The fix is one parameter and no new helper; the smith shows the `[29]` arm red under the arm-off mutation before committing it, and E3's evidence sentence gains the second direction.

### ⬜ a — `overview.md` §*Not verified* still says the `Ran by` cells read `unknown`

`seal/specs/1790174139-survivors-md-silences-what-it-quotes/overview.md`, the second row of *Not verified*. All four phase records now read `| Ran by | specseal:smith on claude-fable-5-1 |` (commit `bc38c8f3`, read), so the row describes a state the tree no longer has and `unverified-check` counts it as open. The orchestrating session, which filled the cells, closes the row. Paperwork under `seal/specs/`, out of `Needs a fix`.

### ⬜ b — the mutation counts for the two call-site reversions are 6 and 6, not 3 and 5

`seal/specs/1790174139-survivors-md-silences-what-it-quotes/phases/phase-4.md` §*Mutations* and `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` row E1. Measured above: `corpus` back on the old predicate turns six cases red and `corrected` back turns six red, the path-list case among them both times. The recorded numbers understate, which harms nothing, but a later reader re-running the mutation would find the record wrong. Paperwork, out of `Needs a fix`.

### ⬜ c — *13 cases seen red first* in the memo's verified line does not add up from the phase records

`overview.md` line 12. The phase records report six red at `531cc723`, four at `c1311c53` and one at `95956de8` — eleven red runs over ten distinct cases (the docstring case counted twice, once per extension). If the smith counted something else (the two docstring paragraphs deleted one at a time, the parametrised case's two arms), the line should say what. Paperwork, out of `Needs a fix`.

### ⬜ d — a `survivors.md` one directory deeper is owned for its range rows and still silences through its path rows

`survivor_check.py#records_a_past_state` matches `survivors.md` directly under the work item directory only, so a deeper file handed to `--exempt` by hand is now asked the ownership question for a `| Range | Grounds |` row and is still in the pool and in the range for its `| Path | Quote | Grounds |` rows — which is #507's and #308's shape at depth, reachable only by a hand run with a file the layout does not place. This is stated intent, found where it has to be: `spec.md` §*Data & interfaces* (*a `survivors.md` sitting directly under a `specs/<id>/` directory*), the function's own docstring (*one level deeper it is somebody's prose until the layout says otherwise*), and `phases/phase-3.md`'s S8 row. Grounds, not a pass by trust; recorded so the next reader of the predicate does not take the asymmetry for an oversight. No fix asked.

## Regression tests to plant

One, the fix for 🟡 1, in `tests/test_a_corrected_sentence_survives_elsewhere.py`: the pool case parametrised over `fillers in (0, 29)`, the `0` arm red at exit 0 and the `29` arm red on the `named` assertion under the `phases/` arm removed. No new file.

## Facts for the evidence ledger

- Row E3's evidence sentence, once 🟡 1 lands: the pool half seen red in both directions — dilution to exit 0 on a four-file pool, and the record named beside the survivor at exit 1 on a 33-file pool — with the arm-off mutation red on both arms.
- Row E1's mutation counts: `corpus` and `corrected` each back on `records_a_past_round`, six red each, the path-list case among them.
- Row E2 holds as written: 14 / 0 / 0 re-executed at `bc38c8f3` with the file present, absent from `--exempt`, and deleted at the tip.
- A fact worth a row nowhere yet: on #525's range every one of the five places that vanish through a live file has `seal/ledger.md:78` as its source and the item's ledger fragment as the carrier of the subtracted phrases — the sentence was moved, not corrected. That is the measured instance of *a phrase the fix kept is not a phrase the fix corrected* the next reader of `spec.md` §*Out* will want.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The S6 pool case asserts both directions but only dilution can turn it red on its fixture; the `named` assertion has never failed | `tests/test_a_corrected_sentence_survives_elsewhere.py` `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` | open | Executed: `phases/` arm removed → 4-file pool exit 0 nothing named, 33-file pool exit 1 naming `guide.md` and the record. Ledger E3 and `overview.md` claim both directions pinned. Paste-ready fix below |
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

## Paste-ready fixes

Finding 🟡 1, `tests/test_a_corrected_sentence_survives_elsewhere.py`, replacing the whole of `test_a_phase_record_standing_in_the_pool_is_not_a_survivor`:

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

Needs a fix: yes — 🟡 1, the second arm of the S6 pool case, seen red on the `named` assertion under the `phases/` arm removed before it is committed; the four ⬜ rows are paperwork corrections and are not counted here
Loses a record or crashes: no

## Proof block

Files opened in the clone at `bc38c8f3`: `skills/code-review/scripts/survivor_check.py` (the diff against the base and the functions `records_a_past_round`, `records_a_past_state`, `retired_directories`, `corpus`, `corrected`, `wanted`, `carriers`, `weights`, `weigh`, `score`, `examine`, `read_exemptions`, `whole_range`, `exempted`, the `OWNER_DIR` and `WORK_ITEM_DIR` patterns), `tests/test_a_corrected_sentence_survives_elsewhere.py` (the diff against the base and the helpers `build`, `run`, `paths_in`, `one_survivor`, the constants `FOUND`, `REPAIRED`, `RECORD`, `ITEM_A`, `GROUNDS`), `skills/code-review/scripts/chain_check.py` (the closed-verdict words), `skills/code-review/scripts/round_record.py` (the headings it parses), `.github/workflows/hygiene.yml` (the survivor step), `docs/review-chain-spec.md` (the survivor-sweep section and the folded statement at line 2011), `seal/follow-up.md` and `seal/ledger.md` (their diffs against the base), `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md`, and under `seal/specs/1790174139-survivors-md-silences-what-it-quotes/`: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `routing.md`, `changelog.md`, `survivors.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`, `phases/phase-4.md`. Executed: the commands in the probes table, from one Python probe file in the session's scratch directory, run once and deleted, and the runner and checker invocations named above.
