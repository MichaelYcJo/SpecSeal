# Round 2 report — 1790562542-the-verifying-round-is-bounded-not-cheapest

Target: round 1's fix range `e062e3a7..1200940f` (`14ddebd6` the fixes,
`1200940f` the record corrections and re-stamps), with the branch at
`08e6eeb4` and draft PR #648. This is the verifying round. I reviewed it in a
`git clone --no-local` at `<scratchpad>/1790562542/round-2/clone`, which is
removed at hand-over.

Carried from round 1, not re-established: the coordinates of the four
closed verdicts, the class sweep's member list, and #89's per-round readings
of #82 as round 1 recorded them. Round 1's three 🟢 confirmations are
inherited and not re-reviewed, as the prompt asks.

## What this round answers

```
round 1 closed four verdicts at 14ddebd6 and 1200940f
   ├─ finding 1: the #82 comparison left the three carriers   → closed
   ├─ finding 2: the warden's scoping paragraph re-grounded   → closed
   ├─ note 3: the chain spec's median names its unit          → closed
   ├─ correction 4: the paperwork follows finding 1           → closed
   └─ new surface: CARRIERS' fifth tuple and the two-gone
      CHEAPEST_81_CARRIERS entries                            → correct
```

Nothing in the diff needs a fix.

## Round 1's finding 1 is closed — no carrier holds the #82 comparison

`skills/code-review/SKILL.md:229-233`, `templates/sdd-round.md:298-300` and
the module docstring of `tests/test_a_segments_record_says_what_it_was_asked.py`
now carry only what #89 measured for #81: five defects, one 🔴 and four 🟡,
in 29 calls (and 7.6 minutes in the template and the docstring). A tree-wide
grep for `three times the calls` and `six rounds averaged` finds the phrase
only in the test's own gone halves and under `seal/`, where it is quoted as
retracted.

The pin is real. I executed it in the clone: re-adding the comparison beside
the stands phrase turned `test_81s_round_one_is_not_called_the_cheapest_again`
red, once for the skill and once for the template, with the present half
still passing.

The new docstring says #89's readings of #82's rounds are 35, 38, 36, 29 and
30 calls, and that round 2 found seven. I read #89's comments through `gh`
again, and they match. Round 2 is "a 🔴 and six 🟡", and round 5 has no call
count, so the five figures are all the readings #89 gives.

## Round 1's finding 2 is closed — the scoping paragraph is grounded on the job

`agents/warden.md:110-114` now says re-reading the whole diff "re-reviews
what earlier rounds already reviewed instead of answering the finding that
came back". That is the same ground as C4 one bullet below, so the file no
longer disagrees with itself. The paragraph is the fifth entry of `CARRIERS`.

I executed both halves. Restoring the paragraph as it stood at `5a66666d`
turned the stands case and the gone case red. Keeping the new clause and
appending only "which is how a review loop costs more than the work it
reviews" turned the gone case red on its own. `git show 1fa25931` holds the
same paragraph, so the tuple's comment is true that the gone half is the
wording at both commits.

For the class, I grepped `price`, `cheaper`, `cheapest` and `affordab`
across `agents/`, `skills/`, `docs/`, `templates/`, both READMEs and
`CONTRIBUTING.md`. Every hit other than C4's "not its price" is about
something other than what a review round spends. That matches round 1's
sweep, and I found no new member.

## Round 1's note 3 is closed — the median names its unit

`docs/review-chain-spec.md:220` now reads "0.83 × the span of their own work
item's round 1". The changelog fragment, the module docstring, V1 and
`overview.md` say "span" too. The stands phrase went red when I deleted
`the span of`.

The stands phrase writes the sign as `\N{MULTIPLICATION SIGN}`, and its
comment says ruff's RUF001 refuses the literal. I executed that: a one-line
file holding the literal sign gets RUF001 from ruff 0.16.9, and the
repository's `pyproject.toml` selects `RUF`. `ruff check` and
`ruff format --check` pass on both changed test modules.

## Round 1's correction 4 is closed — the paperwork follows finding 1

- The changelog fragment says "five defects in 7.6 minutes and 29 tool
  calls … with no comparison to other rounds".
- Ledger row V2's claim carries a `Corrected 2026-09-28` note, and its skill
  anchor is the new sentence.
- `phases/phase-1.md:56-63` carries a dated correction naming the clause
  and the commit it left at.
- `overview.md` closes its *Not verified* row with `✅`, which is the shape
  `templates/sdd-overview.md` gives and what `unverified_check.py` reads as
  closed.

`evidence_check.py .` exits 0 with nothing drifted. The six re-stamped
release rows (0.5.0, 0.8.1, 0.10.0, 0.11.4, 0.15.0 A11, 0.15.1 D1) each
change only their hash and add a dated re-read note. I read each note
against the word diff of the edit it names, and each describes that edit
correctly. None of the edits touches the clause its row claims.

## The new surface — the two changed constants

- **`CARRIERS`' fifth tuple.** It shares its path with the fourth. Every
  consumer unpacks the tuples in a loop and nothing keys a dict on the path,
  so the fourth tuple is not shadowed. Both gone halves were seen red on
  their own (above).
- **`CHEAPEST_81_CARRIERS`.** The gone halves are now tuples. The present
  case unpacks `path, phrase, _gone`, which is unaffected. The absent case
  iterates over each gone, and both of the new second gones were seen red.
  The comment above the constant says the first gone is the base's wording
  and the second is round 1's find, which is accurate.

Round 1's `New units` is `none`, and the diff adds no function, so nothing
else is new.

## Round 1's deferral, outside the tree

#51's body, read through `gh`, now follows "Surface size, not round kind"
with "Later rounds did not hold this reading either … (corrected 2026-09-28,
from #639's round 1)". The orchestrator's account of this is true.

## The broad gate

Not yet run. This round leaves nothing open, so the gate has come due, and
what comes due is the sealer's spawn.

## Regression tests to plant

None. Each closure already has its pin, and each pin was seen red this
round.

## Facts for the evidence ledger

- #89's readings of #82's rounds are 35, 38, 36, 29, not stated and 30 calls,
  and round 2 found a 🔴 and six 🟡 (read through `gh`, this round). V2's
  correction note already carries this.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — the #82 comparison is gone from the skill, the template comment and the module docstring, and both carriers pin its absence | `skills/code-review/SKILL.md:230` | confirmed | Read at `08e6eeb4`; a tree-wide grep finds it only in gone halves and `seal/` quotations. Executed: re-adding it to the skill, and then to the template, turned the absent case red each time |
| 🟢 | round 1's finding 2 is closed — the warden's scoping paragraph is grounded on answering the finding, not on a first round's price | `agents/warden.md:111` | confirmed | Read; it now matches C4's ground. Executed: the `5a66666d` paragraph restored turned both cases red, and the old clause appended alone turned the gone case red. A price-word sweep found no further member |
| 🟢 | round 1's note 3 is closed — the chain spec's median names round 1's span | `docs/review-chain-spec.md:220` | confirmed | Read; the fragment, docstring, V1 and `overview.md` agree. Executed: deleting `the span of` turned the stands case red. RUF001 on the literal sign confirmed with ruff |
| 🟢 | round 1's correction 4 is closed — the changelog fragment, V2, phase 1 and the overview row follow the corrected wording with dated notes | `seal/ledger/1790562542-the-verifying-round-is-bounded-not-cheapest.md:4` | confirmed | Read each; `evidence_check.py .` exits 0 (executed). The six release re-stamps change only hash and note, each note true to its edit |
| 🟢 | the fifth `CARRIERS` tuple and the tuple-valued gones in `CHEAPEST_81_CARRIERS` are consumed correctly and each gone is live | `tests/test_the_verifying_round_is_bounded_not_cheapest.py:65` | confirmed | Read every consumer. Executed: each added gone seen red on its own, and both modules pass at `08e6eeb4` |
| ❓ | Whether #639's median 0.83, its range 0.26–1.27 and the five at or above round 1 reproduce | `docs/review-chain-spec.md:219` | ❓ out of verified scope | Carried from round 1 and not re-derived here. Answered by a measurement from #639's author (`questions.md` Q1) |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_verifying_round_is_bounded_not_cheapest.py` and `tests/test_a_segments_record_says_what_it_was_asked.py`, in the clone at `08e6eeb4` | exit 0, 15 passed, before the mutations and again after the bytes were restored |
| Mutation: the #82 comparison re-added to `skills/code-review/SKILL.md` beside the stands phrase | exit 1, 1 failed (`test_81s_round_one_is_not_called_the_cheapest_again`), 14 passed |
| Mutation: the #82 comparison re-added to the `templates/sdd-round.md` comment | exit 1, the same case failed, 14 passed |
| Mutation: the `agents/warden.md` scoping paragraph restored as at `5a66666d` | exit 1, 2 failed (the stands case and the gone case), 13 passed |
| Mutation: the new warden clause kept and "which is how a review loop costs more than the work it reviews" appended | exit 1, 1 failed (the gone case), 14 passed |
| Mutation: `the span of` deleted from `docs/review-chain-spec.md` | exit 1, 1 failed (the stands case), 14 passed |
| `evidence_check.py .` in the clone | exit 0, 0 drifted |
| `bin/survivor-check --range e062e3a7..1200940f` in the clone | exit 0, "no removed wording is still standing" over 454 files and 35 removed sentences |
| `ruff check` and `ruff format --check` on the two changed test modules | exit 0, and both already formatted |
| `ruff check` on a one-line scratch file holding a literal `×` in a string | RUF001 reported |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — not run by this round. It is the sealer's, and it is now due |

Needs a fix: no
Loses a record or crashes: no

## Proof

Opened this round, at `08e6eeb4` in the clone unless noted:
`rounds/round-1.md`; `rounds/round-1-report.md`; the full diff
`e062e3a7..1200940f` outside `seal/releases/`; the word diff of
`seal/releases/` over the same range; the diffstat of `1200940f..08e6eeb4`;
`tests/test_the_verifying_round_is_bounded_not_cheapest.py` in full;
`tests/test_a_segments_record_says_what_it_was_asked.py:270-330`;
`agents/warden.md:105-128`; `agents/warden.md:108-114` at `1fa25931`;
`bin/test`; the ruff section of `pyproject.toml`; the `✅` handling in
`skills/verify/scripts/unverified_check.py` and `templates/sdd-overview.md:38`.
Read through `gh`: #89's comments (the lines naming #82's rounds) and #51's
body (the "Surface size" paragraph).
