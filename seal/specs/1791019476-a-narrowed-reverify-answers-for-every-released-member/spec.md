# Feature Specification: a narrowed `--reverify` answers for every family a file it read holds a member of (#740)

<!-- seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/spec.md
     WHAT this work delivers and how we'll know. The policy documents in docs/
     outrank this file; cite them, don't restate. -->

#740 carries two findings that #736's capped round 3 deferred
(`seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/rounds/round-3-report.md`,
§*🟡 16* and §*⬜ 17*, read in full for this frame).

- **🟡 16.** `evidence-check --reverify --ledger <file>` answers only for a
  released family whose *root* sits in a file it read. Narrowed to a release
  file that holds a folded `Re-read ·` member, it writes nothing and exits 0,
  while `--strict` with the same narrowing reads that member DRIFTED.
- **⬜ 17.** A row whose `Checked` cell holds a date the calendar does not
  have (`2026-13-45`) is described as "the reading of no date".

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, the paragraph opening **Without the row, a released row is kept true where it stands.** — its last sentence | The property 🟡 16 breaks: a narrowed `--reverify` names what it could not clear and exits 1. This work makes the sentence true and rewrites it to say what the code then does (D1, D4) |
| the same section, the paragraph opening **`evidence-check --reverify --into …` writes the re-reads.** | Under the freeze, `--into` writes one `Re-read ·` row per released row a re-read owes, and without `--into` the run names each row it left. Both must hold for a narrowed run too (S2, S3) |
| the same section, the paragraph opening **The checker reads a released row together with the rows that read it, as one family:** | The newest-reading rule. A reading that matches the code but is outranked by a newer reading holding other content is DRIFTED. That is what makes an *older* member in the narrowed file report DRIFTED, and why the fragment cell (D1) exists. ⬜ 17's sentence is added here (D5) |
| the same section, its first paragraph, and `seal/config.md`'s `Ledger frozen from \| 1790993141` | This work item (1791019476) is bound by the freeze. Its re-reads of released rows go into `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md` through `--reverify --into … --checked`, and no released file is edited |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*, "an edit drifts the row … its claim first corrected in place with a `Corrected <date>` note" | Ledger row L4 sits in #736's fragment `seal/ledger/1790993138-….md`, not in a released file, until the 0.18.0 fold. It is corrected in place, with a `Corrected <date>` note |
| `skills/agent-contract/SKILL.md` §12 | The defect is a class: every cell of placement × freeze × newest-reading location × narrowing is enumerated by construction, not by example (§*The class, enumerated*) |
| `skills/agent-contract/SKILL.md` §14, §15 | ⬜ 17 changes a message a person reads, so its new text is documented and pinned in the same commit. Every new case is seen red before it is committed |

## Scope

**In.**

- `skills/evidence-check/scripts/evidence_check.py`:
  - `released_drift`: its family filter, which reads `if top[0] not in wanted`, and its docstring;
  - `reverify_into`: its docstring, plus the argument it passes on, where D2 needs it;
  - `main`'s `--reverify` branch: the comment above the no-freeze `LEFT` loop, and the list the freeze branch hands to `reverify_into`;
  - `family_view`'s emission loop: the "the reading of no date" wording (⬜ 17), with a helper for the date as written if one is needed.
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the two cases round 3's report lists under *Regression tests to plant*, the enumeration case (§*The class, enumerated*), and ⬜ 17's case.
- `docs/the-evidence-ledger.md`, the section above: the sentence 🟡 16 made false, and one sentence for ⬜ 17.
- `seal/specs/1791019476-…/changelog.md`: one `### Fixed` entry per finding.
- `seal/ledger/1790993138-….md`: row L4 corrected in place, and every row of that fragment whose hash this edit moves re-read and re-stamped in place.
- `seal/ledger/1791019476-….md`: this work item's new rows, and the `Re-read ·` rows it owes released rows whose anchors it moved.

**Out, with the reason for each.**

- **README editions, `skills/evidence-check/SKILL.md`, `templates/ledger.md` and `docs/release-checklist.md`.** None of them states what a narrowed `--reverify` does with a family. Checked with `git grep -i narrow` over `docs`, `skills/evidence-check`, `templates`, `CONTRIBUTING.md`, `CLAUDE.md` and `README*.md`. The hits there say only "narrow the write with `--ledger`", which stays true.
- **#736's records** (`spec.md`, `plan.md`, `overview.md`, the round reports). They record a past state, and records are not rewritten. `settle` folds them later.
- **A root in `seal/ledger.md` rather than in a release file.** `ledger_kind` returns `released` for both, and no line of `released_drift` tells them apart. One placement axis covers both, so it is not multiplied out.
- **`--checked` as an axis.** `--into` requires it, and the home tells a reader to pass it. Every cell passes it. Without it, a re-stamped row keeps its date, which is still the newest wherever it was the newest before, so the result does not change (read: `reverify`'s date write happens only where a hash moved).
- **The `LEFT` line's clause "sits in a file this run did not write" in a cell where it is not true.** One such cell may exist: the newest reading sits in a file the run read but could not re-stamp, because that row has no date cell under `--checked`. That row already gets its own `LEFT` line and the run already exits 1, so the error is one of wording, never of a missed answer. It is questions.md W1, and the work decides it if the enumeration meets it.
- **`seal/follow-up.md`'s row about unread re-stamps.** It is a different defect, and its answer belongs to a person.

## The decisions, with their grounds

**D1 — A family is the run's to answer for when any of its members sits in a file the run read, released or fragment.** The round 3 report states the property per narrowing (§*The smith's reading of 🟡 12*): *a narrowed `--reverify` never exits 0 while a narrowed `--strict` over the same files reads a row DRIFTED.* The report's paste-ready fix keys the filter on released members only. That leaves one cell of the same class open:

- the narrowed file is a fragment holding an *older* re-read F;
- F matches the code, and a newer reading in another file holds other content.

`--strict --ledger <F's fragment>` then reads F DRIFTED, through the newest-reading rule in `family_view`'s emission loop. `--reverify --ledger <F's fragment>` re-stamps nothing, because F's hash did not move, and it builds `wanted` from released files only, so it exits 0. This is read, not executed. questions.md M1 is the measurement, and phase 1 shows the cell red before it is fixed.

The work item's slug says *released member* because the ticket does. D1 is wider, and questions.md Q1 records that this frame chose it.

**D2 — `released_drift` takes membership from every ledger the run read.** Two things change:

- The first loop, over released rows outside every family, stays restricted to released files.
- The family filter tests `view.families[top]` against the identities of all of LEDGERS. The paste-ready fix collected members from the graded readings instead. `families` is the member list `family_view` defines, and the graded readings derive from it.

The freeze branch of `main` currently passes `released` to `reverify_into`. It passes the full narrowed list instead, and `reverify_into` writes no file but INTO either way. The no-freeze branch already passes the full list.

**D3 — Unnarrowed runs do not change.** Every released file is already in `wanted` there. A family rooted in a fragment — a `Corrected ·` row there, or a citing row whose citation resolves to nothing — holds no released member, because a citation into a fragment joins nothing, and `released_drift` grades a family's coordinate only from a member under a released root; so every family that can owe a re-read is already answered. A change that widens which members grade a coordinate keeps that guard on the root's kind. The enumeration's unnarrowed column is the control that holds this.

*Corrected 2026-10-03 at round 2's close (⬜ 10): one unnarrowed run does change. A coordinate only fragment re-reads carry whose anchored statement is gone is one no in-place re-stamp clears; it used to exit 0 while `--strict` exited 2, and it now names the released root and exits 1, as a released carrier already did.*

*Corrected 2026-10-03 by round 1's fix pass (⬜ 9): D3 said "every family's root is released", which is false for the two fragment-rooted families named above; the conclusion held only through the released-member filter, which 🟡 1's fix widens under a released-root guard.*

**D4 — The `LEFT` line and the written row name the family's root, even where the run did not read the root's file.** A `Re-read ·` row cites the root (`reverify_into`'s docstring), so the root is where the repair lands, and `--into` already prints `citing <root>`. The home's rewritten sentence says "by its root row", as the paste-ready text does.

**D5 — ⬜ 17's message has three forms, and the date as written is named:**

- a calendar date: `the reading of 2026-02-01`, as now;
- a cell with `YYYY-MM-DD`-shaped text and no calendar date: `the reading dated 2026-13-45, a date the calendar does not have`, naming each such string in cell order, joined by `, `;
- no date at all: `the reading of no date`, as now.

The paste-ready text, `no date the calendar has`, merges the second and third forms and drops the typo the person has to fix. The verdict and the ordering do not change: an invalid date still orders nothing (L1). questions.md Q2 records the wording as the frame's default.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | **Report case 1, under the freeze.** R sits in `seal/releases/0.1.0.md` at h1, dated 2026-01-01. C is a folded `Re-read ·` of R in `0.2.0.md` at h1, dated 2026-02-01. F is a fragment `Re-read ·` at h2, dated 2026-03-01, and the code is back at h1. When `--reverify --into <INTO> --checked 2026-04-01 --ledger seal/releases/0.2.0.md .` runs, then it prints `1 citing row written`, and `--strict .` exits 0 | a new case in the test module, seen red at `2b1dcb1f`'s checker (`0 citing rows written`) |
| S2 | **Report case 2, without the freeze.** The same family. When `--reverify --ledger seal/releases/0.2.0.md .` runs, then it exits 1 and prints `LEFT  seal/releases/0.1.0.md:5` | a new case, seen red (exit 0, no `LEFT`) |
| S3 | **Under the freeze without `--into`.** The same family. When `--reverify --ledger seal/releases/0.2.0.md .` runs, then it exits 1, names the root with the `--into` repair, and writes no released byte | a cell of S4's enumeration. sha256 of the released files before and after, as `digests` already does |
| S4 | **The class, by construction.** For every cell of §*The class, enumerated*: whenever the narrowed `--reverify` exits 0, `--strict` with the same narrowing, run after it, exits 0. Under the freeze with `--into`, wherever the narrowed set holds a member, unnarrowed `--strict` exits 0 after the run | one parametrized case over the product. Against `2b1dcb1f`'s checker the M-in-a-release, N-in-a-release and M-in-a-fragment cells fail, and the phase record names which |
| S5 | **Narrowing to a file that holds no member, and the unnarrowed run, are unchanged.** | the enumeration's `unrelated` and `unnarrowed` columns. Both pass before the fix and after it |
| S6 | **⬜ 17.** R is dated `2026-13-45`, a fragment re-read is dated 2026-02-01, and the code is reverted to R's hash. `--strict` names R with `the reading dated 2026-13-45, a date the calendar does not have`. A row with no date keeps `the reading of no date` | a new case pinning both substrings. The first is seen red against the old wording |
| S7 | **The home and L4 say what the code does.** The **Without the row** paragraph says a narrowed `--reverify` names, by its root row, each family that a file it read holds a member of, where no in-place re-stamp of the files it read clears that family, and exits 1. L4 drops its "(… round 3's 🟡 16, deferred)" clause and carries a `Corrected <date>` note | read by the warden. `tests/test_the_ledger_rules_have_one_home.py` and `tests/test_docs_line_wrap.py` executed |
| S8 | **The ledger is whole under the freeze.** After phase 3, `evidence-check --strict .` reads 0 drifted. `git diff --name-only 2b1dcb1f...HEAD -- seal/releases seal/ledger.md` is empty | executed by the builder at the phase 3 boundary (the one ledger run). The diff command is the warden's |
| S9 | **No surviving false sentence.** `bin/survivor-check --range 2b1dcb1f...HEAD` reports nothing that is not judged in this work item's `survivors.md` | executed by the builder before handing back |

## The class, enumerated

The family has three readings of one code coordinate, and the code is back at
the hash the two older ones recorded. N is the only reading that does not hold.

- **R**, the root: `seal/releases/0.1.0.md`, h1, the oldest.
- **M**, an older `Re-read ·` at h1: either folded into `seal/releases/0.2.0.md` or sitting in a fragment.
- **N**, the newest `Re-read ·` at h2: either in another fragment or folded into `seal/releases/0.3.0.md`.

The axes, multiplied out:

| Axis | Values |
|---|---|
| M's location | folded release · fragment |
| N's location | fragment · folded release |
| narrowed set | R's file · M's file · N's file · R's and M's files, as two `--ledger` flags · an unrelated fragment · no `--ledger` |
| mode | no freeze · freeze without `--into` · freeze with `--into` |

That is 2 × 2 × 6 × 3 = 72 cells. The assertion is S4's invariant, never a per-cell expected value, so a cell cannot be mis-expected by hand. One extra control cell stands outside the product: R superseded by a `Corrected ·` row, narrowed to R's file. Nothing in R's family is graded there, and the run must exit 0.

Two variants are not axes, on purpose:

- **Two `--ledger` flags against a glob matching both files.** `resolve_patterns` flattens both to one list, so the two-flag form stands for both.
- **`--checked`.** See §*Scope*.

The builder may cut cells that construction makes identical. Each such cut names the line of code that makes them identical, in `phases/phase-1.md`.

## Data & interfaces

- **No new flag and no new file kind.**
- **Output changes.** A narrowed `--reverify` gains `LEFT` lines (no freeze, or freeze without `--into`) or writes rows (freeze with `--into`) in the cells above, and exits 1 where it exited 0. `family_view` gains D5's second message form.
- **The units edited.** All are in `skills/evidence-check/scripts/evidence_check.py`: `#released_drift`, `#reverify_into` (docstring, argument), `#main` (the `--reverify` branch), `#family_view` (the emission loop).
  - The ledger rows citing `#main` will drift: one each in `seal/releases/0.4.0.md`, `0.8.3.md` and `0.9.0.md`, two in `0.16.0.md`, and six in #736's fragment. These counts come from `git grep -c` at `2b1dcb1f` and include every row citing `evidence_check.py#main`.
  - The rows citing `#family_view`, `#released_drift` or `#reverify_into` all sit in #736's fragment.
- **Under the freeze**, the released rows are re-read into this work item's fragment, and #736's fragment rows are re-stamped in place, each read first.

## Open questions → questions.md

`questions.md` holds two rows decided by this frame (Q1, Q2), two measurements
(M1, M2) and two rows for the work (W1, W2). None blocks the build.

Framed 2026-10-03 by framer, before the build.
