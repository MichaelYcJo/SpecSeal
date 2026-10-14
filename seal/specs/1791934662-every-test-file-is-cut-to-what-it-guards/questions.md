# every test file is cut to what it guards — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. -->

**Judgments the ticket left open that the owner or the tree answered** — listed so nobody reopens them; the grounds are in `spec.md` and `plan.md` §*Alternatives considered*.

- The item lands wholly in 0.22.0; neither a long CI wait nor a deferral of heavy files is an option (the owner, 2026-10-14; alternatives B, C).
- The unit of rebuilding is the shipped module; the old tests are a baseline (killed mutants) and a reference (real-bug regressions), taken once; redundant or heavy parts are rebuilt per unit and the old content deleted at the same path; a thin case that alone kills a mutant stays (the owner; alternatives A, F, G).
- A tangled decision is extracted into a pure function before it is tested; the frame names the modules by measurement (`spec.md` §*What the remaining suite is*), the phase names the units.
- The per-pull-request bound is the slowest job, not a summed leg: `cases` job ≤ 5 min on every pull request, `slowest-job` ≤ 5 min at the item's end, both rows ratcheted (the owner; alternative H).
- The proof model is one run per function reading the killer set (#929 Q2 (i)), which the orchestrator passes to #929's smith as the default.
- A prose-pinning function gets its `Kills:` line here and is never removed or re-pointed here (#923's boundary; #929 S5).
- Which files are rebuilt and which cut is a measured classification (`spec.md` §*The two strategies*), 65 and 115, re-set by a phase only with the reason in its record.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | For #929's remaining phases: whether the enumeration files (phase 3) and the sealer file (phase 5) take this item's strategy — baseline from the old file once, decision tables per unit, one end-to-end case per path, deletion once non-inferior — in place of proving each legacy case; and, for the `cases` job, one run per function reading the killer set, `timeout-minutes: 5`, and the failure message *restructure: test the decision directly* past it | the work — #929's phase 2, 3 and 5, its smith; this item does not edit #929's frame | adopted: the sealer file's 98 `run_gate` call sites become one table and a path each, and the enumerations become a table over the reader; not adopted: #929 proves 457 + 4,228 legacy cases one at a time and its `cases` job runs 1 + 2N file runs | this item builds as if adopted; where #929 lands the two-run job, this item's targets still hold its own pull requests under 5 minutes | ⬜ |
| Q2 | Whether an extracted pure function may change a module's public shape (a new top-level name beside the thin caller) without a `Removes` row or a changelog line | the work — each extraction phase, read against `docs/the-reader-registry.md` §*Who declares* | a new unit is a `Reads:` line and a ledger row; a renamed one is a `Corrected ·` row | new unit, caller unchanged in name and behaviour; the battery red before and after is the proof | ⬜ |
| Q3 | The ubuntu seconds of one file run against its Windows price; 0.23 (the suite's median minutes, 9.9/42.4) is assumed per file and sets the `cases` job estimate | a measurement — phase 1's `cases` job summary | — | 0.23; the targets re-set from phase 1's figure | ⬜ |
| Q4 | Per rebuilt file, the inventory of real paths (git, hooks, filesystem, process) and so the end-to-end case count; the frame assumes ten | the work — each phase, before the new file is written | — | ten; the file's seconds target re-set from the inventory with the reason | ⬜ |
| Q5 | Whether `mutation-check`'s output names a collection error as a killer: the frame's parse read `FAILED` lines and recorded three red mutants with no killer | a measurement — phase 1, one run with `-rfE` beside `-rf` | — | the table reads `-rfE`; a collection error names the file as the killer | ⬜ |
| Q6 | Per file, which cases of the measured port list (597 of 1,086 functions in the fourteen; the regex errs over) encode a real regression and are ported, and which are named as needing no port | the work — each phase, case by case | — | every listed case read; a case not ported is named with why | ⬜ |
| Q7 | For each opened file, which functions it lined but left to #923 (prose pins), and whether #923's phase that moves a sentence re-points the line in the same commit | the work — each phase's record here; #923's phases for the re-pointing | — | listed per phase; #923 re-points | ⬜ |

No row waits on a person: the owner's answers of 2026-10-14 are in the header, and every row is the work's or a measurement's. The three kinds are the template's.
