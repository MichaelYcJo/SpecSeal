# 1791019476-a-narrowed-reverify-answers-for-every-released-member — questions for the planner

<!-- seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/questions.md
     decisions only a human can make, extracted so nothing ships on a silent
     assumption. -->

**Nothing here blocks the build.** The owner pressed `automation` for the
whole milestone, and nobody is left to ask. Where a person would decide, this
frame chose a stated default with its grounds (Q1, Q2). Either can be
overturned by opening what the frame opened.

**Judgments the tickets left open that the tree answered.** They are listed so
nobody reopens them. Each one's grounds are in `spec.md`.

1. **Whose row the `LEFT` line names when the run did not read the root's file.** It names the root (spec D4). `reverify_into` cites the root, and `--into` already prints `citing <root>`.
2. **Where membership comes from.** It comes from `view.families[top]`, not from the graded readings (spec D2). `families` is the list `family_view` defines.
3. **Whether unnarrowed runs change.** They do not (spec D3). Every released file is already in `wanted`, and every family's root is released.
4. **Where L4 is corrected.** In place, in #736's fragment, with a `Corrected <date>` note. It is a fragment until the 0.18.0 fold (`CLAUDE.md` §*a change writes fragments*).
5. **Where the enumeration lives.** In the existing test module, beside its helpers. No line ceiling covers `tests/` (plan §*Alternatives*).
6. **Whether `--checked` and the glob form are axes.** They are not (spec §*The class, enumerated*).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does a narrowed `--reverify` answer for a family whose member in the narrowed set is a **fragment** row, not only a released one? The ticket and the slug say *released member*. | a person | **(a)** Released members only, which is round 3's paste-ready fix. One cell stays open: a narrowing to a fragment holding an outranked older re-read exits 0 while the narrowed `--strict` reads it DRIFTED. **(b)** Any member, released or fragment. The property round 3 stated per narrowing holds in every cell, and no cell gives up anything | **(b)**, decided by frame. The tree does not leave this open: round 3's report states the property per narrowing, not per file kind, and agent contract §12 owes the fix to the class. It is a row because it widens what the ticket asked for | ⬜ |
| Q2 | What does the message say for a reading whose `Checked` cell holds only a date the calendar does not have? | a person | **(a)** `no date the calendar has`, round 3's paste. It reads the same for an empty cell and for a typo, and does not show the typo. **(b)** `the reading dated 2026-13-45, a date the calendar does not have`, with `the reading of no date` kept for an empty cell. It names what the person has to fix | **(b)**, decided by frame (spec D5). The report's own grounds for ⬜ 17 are that "the person's repair is to fix the typo", and only (b) shows the typo | ⬜ |
| M1 | Is the fragment cell red today? The cell: M in a fragment, narrowed to M's file. The question is whether `--strict` with that narrowing exits 2 while `--reverify` exits 0 | a measurement | Phase 1(c) runs the enumeration against `2b1dcb1f`'s filter. If the cell is green there, D1's fragment half fixes nothing observable, and the phase record says so. The invariant stays asserted either way | the frame's reading: red, by `family_view`'s emission loop and `released_drift`'s released-only `wanted` | ⬜ |
| M2 | Is 72 cells × about 3 subprocess runs too slow under `bin/test`? | a measurement | Time the parametrized case. If it is slow, cut cells that construction makes identical. For example, `R's file` gives the same result whatever N's location is, because the root is already in `wanted`. Name the line of code behind each cut. Never cut a whole axis | all 72 cells | ⬜ |
| W1 | Does any cell make the `LEFT` line's clause "sits in a file this run did not write" false? The candidate: the newest reading sits in a file the run read but could not re-stamp, because it has no date cell under `--checked` | the work | If the enumeration meets such a cell, phase 1 decides the wording there and records it. If it meets none, nothing changes. The run already exits 1 with a separate `LEFT` for that row, so no answer is lost either way | out of scope unless met | ⬜ |
| W2 | Which rows do the edits drift, and does the 0.18.0 fold land before this branch? | the work | Phase 3 reads `--strict`'s drift list after the edits; the spec's count of rows citing `#main` is a ceiling, not a list. If the fold has landed first, L4 is a released row, and its correction becomes a `Corrected ·` row in `seal/ledger/1791019476-….md` that cites it in `seal/releases/0.18.0.md` | correct L4 in place; the branch lands first | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be accountable for.
- **a measurement** — a probe, a command or a count settles it.
- **the work** — unknowable at framing time; the phase that meets it decides it and records it there.

**The framer opens rows and does not own their answers.** `Status` is ticked by
whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
