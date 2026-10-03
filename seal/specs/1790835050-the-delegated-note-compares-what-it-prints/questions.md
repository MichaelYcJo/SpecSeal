# the delegated note compares what it prints — questions for the planner

<!-- seal/specs/1790835050-the-delegated-note-compares-what-it-prints/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person, and none blocks the build.** The owner pressed
`automation` on 2026-10-01 (`routing.md`), and the ticket asks no question of
anybody: it names the fix, the case and the class. What survives judging is
one measurement the case itself performs and one thing only the build can
see.

**Judgments the ticket left open that the tree answered.** Listed so nobody
reopens them; the grounds are in `spec.md` §*Scope* and §*The class, swept*
and in `plan.md`'s Alternatives table.

- **The decision follows the column, not the note's own seconds figure.**
  The note is a sentence about the `delegated` column — *never reaches a
  minute here* — so the value it has to agree with is the one the column
  prints, through `minutes` to one decimal place of minutes. The `.0f`
  seconds figure is the note's own detail and, once the decision follows the
  column, is bounded at `57s` and contradicts nothing (Alternatives A, D).
- **The shape is #640's**: `round(delegated_max / 60, 1) < 1.0`, as the two
  ratio comparisons read since 0.16.0, rather than a shared helper or a
  string compare (Alternatives B, C).
- **The class sweep found one defect, three sites #640 already closed, one
  same-shape site left with grounds (`:2115`), and the rest existence,
  proportional, integer or unprinted comparisons.** `spec.md` §*The class,
  swept* is the table; the build re-reads it rather than trusting it.
- **No comparability line on the page**: no number moves and `--json` is
  byte-identical, which is #640's S10 ruling (Alternative H). The changelog
  fragment names the band (57.0, 60).
- **No document is edited**: none states the 60 s threshold (Alternative J).
- **Seven ledger rows drift and none is corrected**: each claim holds
  against the diff; row 13 of `seal/releases/0.9.5.md` gets a dated re-read
  note because its free text says the block was untouched.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Do `round(x / 60, 1)` and `minutes(x)` agree at the band's edges on the interpreter the suite runs under? The framer executed seven values on one interpreter and they agreed (57.0 → `0.9`/`0.9m`, 57.02 → `1.0`/`1.0m`, 59.6 → `1.0`/`1.0m`); CPython documents both as correctly rounded from the binary value, but the suite's matrix is what the claim has to hold on | a measurement | S2's case at 57.0 s asserting the cell `0.9m` beside the note, run where the suite runs. Agree: Alternative A stands. Disagree anywhere: the comparison is written through one helper both the cell and the decision use (Alternative B), and the case still pins the edge | A, as planned | ⬜ |
| Q2 | Does `evidence-check --reverify --checked 2026-10-01 .` move exactly the seven rows `spec.md` enumerates, or does the edit's hash reach a row the framer did not find? The framer counted by `grep -c "report_spawns@"` over `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` (six in 0.9.5, one in 0.11.3); the tool names what it changed and that output is the answer | the work | Seven: phase 2 as planned. More: each extra row is read against the diff before it is re-stamped, and the phase record names it. Fewer: a row the framer counted does not anchor at the edited unit after all, and the record says which | seven | ✅ seven, answered by the work on 2026-10-01: `--reverify` moved the hash in exactly the seven rows and no other (`phases/phase-2.md`) |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. None here.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked. Answered rows feed back
into docs/ (policy clause or open-questions section) before this directory's
work merges — here, into the phase records and the changelog fragment, since
no policy document states the threshold.
