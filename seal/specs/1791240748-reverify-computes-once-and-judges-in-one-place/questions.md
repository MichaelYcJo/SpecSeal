# `--reverify` computes once and judges in one place — questions for the planner

<!-- seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Answered before the frame, or by the tree

Listed so nobody reopens them. The grounds are in `spec.md` where a row
names a section.

| Decision | Answer | Who answered | Grounds |
|---|---|---|---|
| Patch or reimplement the core of `--reverify` | Reimplement | the owner, delegating to the orchestrator, 2026-10-06 | #824's body; `routing.md` |
| Keep #786's D2 (an order of writing plus revisits) | Drop it. Every code coordinate is judged once from disk; coordinates naming planned ledger lines are recomputed against the plan until nothing changes; one write; a move is (hash before, hash after) | the orchestrator | #824's first bullet; spec D1, D5 |
| One judgment function for `--strict`, `reverify` and `reverify --into` | Yes; the duplicated place logic, the held-coordinate loop's copy, `current_hash` and `left_because` go | the orchestrator | #824's second bullet; spec D2 |
| #809: which verdict is right for an unsure place with a claim whose minor region does not hold the row's hash | The check's, `DRIFTED`. `--reverify` re-stamps the minor region's hash; where the region is gone it leaves the row and the record says `BROKEN`, the pact doc's word for *left by the re-read* | the framer, from the tree | `docs/the-evidence-ledger.md` §*A row is a content anchor*: *only the major level can be broken*; `test_a_stale_claim_on_an_unsure_place_drifts_rather_than_breaking` (round 8); `docs/the-pact.md`'s definition of the record's `BROKEN`. Spec §*Two departures*, D3. The 0.4.0 round-6 rule was written for a row with no claim and is narrowed to it by a `Corrected ·` row |
| #809's comment: how a claim tie among unsure places is worded | As the check words it: `locator is ambiguous — N places: … (K hold the recorded content, a tie it cannot break)` | the framer, from the tree | one judge, one sentence; `left_because` goes |
| A row that never settles (its Code grounds quote its own line) | Left at the hash the row held, named on a `LEFT` line, exit 1 — where `cited_first` left it silently for `--strict` | the framer, from the tree | *Five things `--reverify` leaves at exit 0* is a closed list of named leavings, and a silent one is the defect the lineage reports; `docs/the-evidence-ledger.md` §*A released row is read again*, the fifth item |
| Whether the vendored `Pact notify` reader (#756, #759) is the same shape as #809 | No. It is a deliberate copy for a checker shipped without `hooks/`, and `tests/test_a_signatory_declares_its_pact.py` holds the two equal. Out of scope | the framer, from the tree | spec §*Out* |
| A narrowed run's `LEFT` line for a moved line in a file left out | Reads every ledger coordinate, not only citations (#806's class one arm over) | the framer, from the tree | §12; `citations_left` reads `row_citation` only (`:3906-3978`); spec D4 |
| A permanent differential test against the base script | No; a `test_tmp_*` probe with its figures recorded | the framer, from the tree | §7; the base is wrong in the named cells, so the test would carry a growing allowlist; the suite is the standing differential (spec §*Out*) |
| Plan the #822 rename, or plan around it | Around it; the overlapping files and the rebase are in `plan.md` §*Overlap with #822* | the orchestrator's spawn prompt | — |

## Open

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The recomputation's scheme and bound: judge every dynamic coordinate against the previous round's plan (order-free by construction) or edit the plan in file order and re-walk (must prove S4); and how many rounds before a still-moving row is named — the count of dynamic coordinates plus two, or a repeated-state check. The tree cannot answer it: no document fixes either, and the only constraint is the two cases S4 and S6 | the work | Previous-round judging: S4 holds without argument, one more plan rebuild per round. File-order editing: fewer rounds on a chain, and S4 must be shown. A repeated-state check names a row the first time its text recurs; a fixed count may run a few extra rounds on a long chain | previous-round judging; the bound is the number of dynamic coordinates plus two, which is `cited_first`'s own bound carried over | ⬜ |
| Q2 | Is `--strict .` over this repository's ledger byte-identical between the base script and phase 1's, and over every tree the suite builds? The tree cannot answer it before the code exists | a measurement (D6, probes 1 and 2) | Identical: phase 1 is the refactor it claims. A difference: either a copy of the judgment disagreed with `classify` somewhere this frame did not read, which is a finding to fix in phase 1, or a fixture reached a cell the issues name, which is classified | identical | ⬜ |
| Q3 | How many released rows are owed a `Re-read ·` after phases 1–3, and how many of the rows citing `#main`, `#check_text` and `#family_view` drift at all. The counts in `plan.md` are per coordinate and over-count rows | a measurement (`bin/evidence-check --strict .` after phase 3, then `--reverify --into`) | Decides the size of phase 4 and nothing else | the plan's table | ⬜ |
| Q4 | Whether `skills/evidence-check/SKILL.md` §*Re-verifying* needs a sentence. It says nothing about walks and nothing false was found at `6d763c40`; whether phase 2's output adds a leaving the section should name (the unsettled row) is known once the line's words exist | the work | Add one sentence naming the unsettled row and pin it; or leave the section, because the home's *left*-reasons sentence already carries it | leave it unless a sentence there is false | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

No row here names a person. The two decisions a person could overturn are
recorded above as answered from the tree — #809's verdict and the unsettled
row's exit code — with the grounds a reviewer can open; overturning either is
one `Corrected` note in this file and one case changed.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
