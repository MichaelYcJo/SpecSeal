# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — phase 2

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-2.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 93acc277 |
| Ran by | smith on Fable 5.1 |

## What this phase was asked

A released changelog section and a gathered fragment are records (#307):
the released-region blank over a root `CHANGELOG.md` keyed on `## <version>`
headings (`## Unreleased` stays live), the gathered set read off
`<!-- specs/<id> -->` markers in the tip's `CHANGELOG.md` — read by the
sweep itself, not imported from `gather_changelog.py` — applied in
`corrected` and `corpus`; the docstring paragraph; `EXCLUSIONS` extended;
cases S7–S12; S12's counts B 9 → 8, C 1 → 0; `questions.md` Q3 and Q4
filled.

## What this phase found

**Q4 — the shape in code.** A sibling predicate and a text step, as the
question's default said. `blank_released` sits beside `blank_struck` and is
applied in `sentences` when the path is exactly `CHANGELOG.md`, the way
`python_prose` is applied there for `.py`; `a_gathered_fragment(path,
gathered)` is applied beside `records_a_past_state` in both `corrected` and
`corpus`, each of which reads the gathered set through
`gathered_fragments(root, rev)` — one `read_blobs` call on `CHANGELOG.md`
at the tip, and no path list, so
`test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
counts what it counted before. A parameter on `records_a_past_state` was
not taken because that predicate is a pure function of the path and this
one needs a file's contents. `PREDICATE` in the test module is unchanged;
`EXCLUSIONS` gained the fourth opener.

**S12 did not land where the frame put it, at one coordinate.** C is 1 → 0
and exits 0 as expected. B is **8 → 8** rather than 8 → 7 (phase 1 had
already taken it from 9 to 8): `CHANGELOG.md:2090` is gone, and
`skills/code-review/scripts/survivor_check.py:142` — the module's own *The
**quote is the anchor**, so the exemption stops applying the moment the text
changes* sentence — crossed the floor at **1.61** against the
`seal/follow-up.md:62` row the range deleted, sharing *text changes and* and
*the anchor so*. At `476af109` the same pair scored **1.51**, under the floor
(measured by stashing phase 2 and re-running with `--floor 1.4`). The pool
went from 387 to 378 files at that tip — nine gathered fragments out — and
the weight of every phrase they held rose, which is the movement
`plan.md` §*Operational impact* says phases 1–3 can produce and the reason
S6 pins a set rather than a count. The sentence is true where it stands, the
report is at the margin, and the case pins the new set.

| Range | After phase 1 → after phase 2 | Gone | Joined |
|---|---|---|---|
| 0 `cbb5809..576fe39` | 4 → 4 | — | — (2.77 → 2.76 on `chain_check.py:2374`, the pool 372 → 363) |
| C `576fe39..cc49ae6` | 1 → 0, exit 0 | `CHANGELOG.md:2252` | — |
| B `cc49ae6..3dd2407` | 8 → 8 | `CHANGELOG.md:2090` | `survivor_check.py:142` at 1.61 |
| A `3dd2407..d2f2c0d` | 1 → 1 | — | — |

Executed 2026-09-24 at `93acc277`, the same command as phase 1's. The
`against N sentence(s)` counts moved too — 0: 65 → 60, C: 90 → 61, B: 36 →
35, A: 171 → 156 — because each of those ranges edited `CHANGELOG.md` or a
gathered fragment, and those lines are no longer removed sentences.

**Q3 — the exemption rows the two classes would have spared.** Read
2026-09-24 across the ten `seal/specs/*/survivors.md` in the tree at
`93acc277`, against each row's own grounds cell. Three files hold only a
`| Range | Grounds |` row and are not counted; the other seven hold 56
`| Path | Quote | Grounds |` rows. Of those, **17 are the code-idiom
class** — a quote that is a line of code, and grounds saying so: 8 in
`1790138190`, 2 in `1790154759`, 2 in `1790173106`, 1 in `1790173209`, 4 in
`1790174138` — and **3 are the released-changelog class**, one each in
`1790138190`, `1790173209` and `1790174139`. Twenty of 56 rows, 36 per
cent. The rows stay (spec judgment 8); the count goes to `overview.md`.

**Seen red first, executed 2026-09-24 against the script at `476af109`:** S7
under all three heading spellings at exit 1 naming `CHANGELOG.md`; S9 at
`against 1 sentence(s)`; S10's range arm at `against 1`; S11 with the
opener absent; S12 on B and C. S8 and S10's ungathered arm were green
before and after. S10's pool arm was green before for the wrong reason —
with the same sentence in the released body and the fragment, the two
carriers halved each other's weight to 1.49 — so the fixture's released
body carries an unrelated entry, and the arm is shown red by the
mutation below instead.

**Mutations, executed at `93acc277` from Python, file restored
byte-identical each time:**

| Mutation | Cases run | Result |
|---|---|---|
| the released blank never applies | S7, S9, S12 | red (6 of 9) |
| `VERSION_HEADING` matches `## Unreleased` too | S8 | red |
| `a_gathered_fragment` returns False | S10's two gathered arms | red (2 of 3) |
| `a_gathered_fragment` ignores the gathered set | the ungathered arm | red |
| `corpus` stops applying it | the pool arm | red |
| `corrected` stops applying it | the range arm | red |
| the paragraph's opener altered | S11 | red |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
