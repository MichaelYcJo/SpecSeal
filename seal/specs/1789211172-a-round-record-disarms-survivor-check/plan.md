# Implementation Plan: a round record disarms survivor-check

<!-- seal/specs/1789211172-a-round-record-disarms-survivor-check/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-12 by the repository owner, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. -->

## Summary

One filter on one list, and everything else in this plan exists so that the
filter cannot be taken back out silently.

`corrected()` builds `paths` straight from `git diff --name-only` and reads
every one of them as prose. `corpus()` builds the pool from the same kind of
list and drops a work item's round records first, because a record quoting a
defective sentence is not a place that still instructs anybody. The same
sentence is true of the range, and the code says it on one side only.

The fix applies `records_a_past_round` to `corrected`'s `paths`. The gate then
gets **stricter**: ranges that reported nothing report again. That is the
point — a branch that went through review is precisely the branch whose fix
pass corrected one coordinate and left the class standing.

## Technical context

| Coordinate | What is there |
|---|---|
| `skills/code-review/scripts/survivor_check.py:455-464` | `records_a_past_round` — matched on the path's own shape, `rounds` inside a `specs` directory, so it holds at either `seal/` root. Already normalises `\` to `/` |
| `:467-473` | `corpus` — `[p for p in tracked(root, rev) if not records_a_past_round(p)]` |
| `:479-515` | `corrected` — the defect is `:496`, `paths = [path for path in names.split("\0") if path]` |
| `:518-523` | `wanted` — `keep - written`, which is where the subtraction lands |
| `:63-79` | the docstring section that states the exclusion and never says which side |
| `:776-840` | `whole_range`, whose own `git diff --name-only` at `:833` stays unfiltered; `:802-807` is the argument for why |
| `tests/test_a_corrected_sentence_survives_elsewhere.py:200-228` | `test_a_record_of_a_past_round_is_not_a_survivor` — the pool-side sibling. It runs at `--floor 1.4` on purpose, because at the shipped floor it passed with the exclusion switched off and was measuring the threshold |
| `tests/test_a_corrected_sentence_survives_elsewhere.py:379-428` | the constructed-repository shape the new case follows |
| `tests/test_a_row_points_by_content.py:994-1025` | the enumeration-by-source shape phase 3 follows |
| `.github/workflows/hygiene.yml:229-244` | the step. Release-base pull requests only; a `main` base exits 0 with a line saying why |
| `seal/specs/1789172128-…/rounds/round-2-report.md:135-181` | the finding and the four-tip measurement |
| `seal/specs/1789172128-…/rounds/round-3.md:183-184` | the two probes that bound this work item's scope |
| `seal/follow-up.md` | the `survivors.md` row, whose *the way `rounds/` is left out of the corpus* clause this change makes stale |

**The failure scenario of the chosen approach, at six months.** Somebody adds
a fourth place that derives a path list from git — a `--since` flag, a second
range, a cache of changed files — and does not apply the predicate, because
the predicate lives beside two call sites and not beside the third. That is
this defect happening again, one function over. Phase 3 is the answer, and its
own failure scenario is that it reads the module's source and a refactor that
renames the `git` helper turns it red for no defect. That cost is one red
case with a message naming what to do, against the cost this defect already
had: a gate reporting success on every reviewed branch for the length of five
releases.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Filter only the **added** side of `corrected` — the narrowest reading of the issue | A sentence *removed* from a round record still counts as corrected wording, so a record edited inside the range becomes a **source** and the report asks somebody to correct an account of a past state. The pool already refuses a record as a candidate, so one side would be filtered against the other | **Rejected.** Round 2 measured the `paths` form: the removed-sentence count stayed at 16 and the survivor came back at 2.00 (`round-2-report.md:160-163, :177-181`) |
| Leave the code and write the intent more clearly in the docstring | The docstring at `:65` already stated the intent — *Everything under a work item's `rounds/` is out* — and the code carried it on one side. A sentence is what failed | **Rejected.** It is the same act that has been re-broken seven times and which this module exists instead of |
| Anchor the new case on the real commit `a0f0e9a`, whose range adds only round 1's record and report, with a third `fixture/*` tag | The tag is a push, which `agent-contract` §6 withholds from every agent. The case ships skipping, and `test_the_measured_commits_are_still_here` gains a third way to go red for a reason nobody caused | **Rejected as the planted case.** The real range is re-derived once and recorded as a measurement in the memo; the planted case is constructed |
| Widen this change to `seal/specs/*/survivors.md` in the same commit | The repository reserved that judgment for a person, twice. Building it decides it, and a gate change is judged by what it does when it is wrong | **Rejected as the default.** Offered as Q1, and as phase 4 if the answer is *in* |
| Exclude by a configured list of paths rather than by the path's own shape | The module's docstring argues by-construction over lists precisely because a list has to be extended by whoever writes the next record shape — the party that has already demonstrated it will not | **Rejected** |
| Raise the floor so a record's quotation cannot clear it | Records score 1.51 against a floor of 1.6 on #267's range, so the floor already refuses them there. What the exclusion buys is the other half of the arithmetic — dropping files that carry the wording raises every remaining phrase's rarity — and a raised floor moves that the wrong way | **Rejected**, and `seal/ledger.md` S6 is the measurement |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The case, **red**. A constructed repository whose range removes a sentence in one file and adds a round record under `seal/specs/<id>/rounds/` quoting it, with the same sentence standing in a third file. Nothing in the module is edited | The case run against the unedited module: it must **fail**, and `phases/phase-1.md` quotes the failing output. `agent-contract` §15 — this is the only thing that has ever caught a case written against a defect it does not measure | |
| 2 | The fix and the sentence. `records_a_past_round` applied to `corrected`'s `paths`; the docstring section at `:63-79` rewritten to name the pool **and** the range; a case pinning that sentence | Phase 1's case green. `test_a_record_of_a_past_round_is_not_a_survivor` still green — the pool side must not move. `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q`, the whole module, one command | |
| 3 | The enumeration, pinned. A case that finds every path list this module derives from git and asserts each one is filtered or named with grounds; `whole_range`'s is the one named exception, with the ownership argument in the message | The case seen red two ways, each restored and the tree left clean: the filter removed from `corrected`, and a new unfiltered path-list call added to the module. Same module command as phase 2 | |
| 4 | ~~**Conditional on Q1.** `seal/specs/*/survivors.md` out of `corrected`'s `paths` and out of `corpus`. Round 3 of #361 measured the added side alone and two of the five reports were `survivors.md`'s own quote cells, which is why the corpus half goes with it~~ **Q1 answered *out*: not built here** | The same module command, plus the real range re-run with and without `--exempt`: the exempted rows must print **under `exempt`, with their grounds**. If Q1 answers *out*, this row closes as `deferred #N` and the issue carries the measurement | `deferred #371` |
| 5 | The records. `changelog.md`; `seal/ledger/1789211172-….md` created with the new rows; `seal/ledger.md` S3 re-read and re-verified; `seal/follow-up.md`'s `survivors.md` row corrected where it describes `rounds/` as left out of the corpus; `overview.md` with `## Not verified` carrying Q1's residue and the broad gate | `bin/evidence-check .` and `bin/evidence-check --reverify .`; `bin/unverified-check seal/specs/1789211172-…/overview.md`; `bin/test` on `test_a_row_points_by_content.py`, `test_the_ledger_fragments_fold_at_release.py`, `test_the_set_a_work_item_always_has.py`, `test_a_question_says_who_can_answer_it.py`, `test_no_real_identifiers.py`, `test_one_word_one_meaning.py`, `test_docs_line_wrap.py`, one command | |

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`.

**The real-range measurement is phase 2's, and it is a measurement rather
than a phase.** Run `bin/survivor-check --range 7e17f5e..941dab5` before and
after the edit while those refs resolve, and record both in
`phases/phase-2.md`: the removed-sentence count must not move, and the
survivor at `seal/specs/1789100139-…/changelog.md` must come back. If the
local branch `docs/361-…` has gone by then, say so and skip it — nothing in
the tree may depend on it.

**Phase order is not negotiable between 1 and 2.** A case written after the
fix is a case that has never failed, which this repository's own `verify`
skill calls a counterfeit seal, and three consecutive work items produced one.

## Operational impact

**The gate gets stricter, and the first branches to meet it are the ones that
went through review.** `.github/workflows/hygiene.yml` runs this check on
every pull request into a release branch. After this lands, a branch whose
round records were subtracting its own survivors will report them, and the
answer is a correction or a `seal/specs/<id>/survivors.md` row with the
standing text quoted and the grounds written. There is no value meaning
*check nothing*, and that is deliberate.

**This change measures itself.** This work item's own branch goes through the
review chain and posts round records, so its pull request is a range of
exactly the shape the fix is about.

No migration, no new environment variable, no new dependency, no
compatibility break. `bin/survivor-check`'s command line is unchanged, both
exemption row shapes are unchanged, and `--floor`'s default is unchanged.

**Prompt budget: zero.** Nothing in this change puts a question in front of a
person at run time or at commit time. The one question this work item asks
anybody is Q1, and it is asked here, once, before the first edit.
