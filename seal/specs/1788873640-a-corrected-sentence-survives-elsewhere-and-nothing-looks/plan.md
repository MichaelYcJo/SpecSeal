# Implementation Plan: a corrected sentence survives elsewhere and nothing looks

<!-- seal/specs/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks/plan.md
— HOW, in phases. This is the Design Gate's artifact. -->

## Summary

One script, `skills/code-review/scripts/survivor_check.py`, reachable as
`survivor-check`. It takes a commit range, works out which sentences the range
**removed**, and reports every place in the tree at the range's tip that still
carries one of them.

The whole design turns on one sentence: **the input is the diff, so nothing is
a list.** A hand-written list of phrases rots the way #210's did, which is a
fixed finding of this repository already. The corrected sentence and the
distinguishing terms both come out of the range's own diff.

## Technical context

**What it stands on.** `skills/code-review/scripts/round_record.py:2502`
(`close`) already takes `--range A..B` and calls `parse_range`, so the range a
fix pass writes is an argument the chain already produces and the smith already
types. `chain_check.py` holds `resolves_to` and `is_ancestor`. This check reads
the same range and needs nothing the chain does not already hand it.

**The corpus** is `git ls-files` at the range's tip, every blob that decodes as
text. Not a curated set: the two measured cases live in `seal/ledger.md` and in
`tests/test_the_rules_have_one_owner.py`, one prose and one a string literal in
code, so a corpus of markdown only would have caught one of the two.

### The metric, and why it is not a literal grep

The two real cases rule out the two obvious mechanics, each on its own case.

- **A literal grep of the removed sentence fails S1.** The pin is one sentence
  split across two adjacent string literals — `"… from this report once the "`
  then `"orchestrator has verified its findings"`. No line in the file holds
  the sentence, so a line-oriented search finds nothing. Normalisation has to
  collapse quotes, backticks and line breaks before anything is compared.
- **A longest-common-phrase rule fails S2.** The ledger rows are a *paraphrase*
  of the corrected docstring, not a copy: *an argument to an operand, never a
  leaf* against *an argument to element 4, never a leaf of the expression*. The
  longest identical run is three words, which no phrase-length floor can accept
  without accepting every three-word run in the corpus.

So the metric is **rarity-weighted n-gram overlap**, and the weighting is what
lets a three-word phrase count while *of the expression* does not:

1. Normalise text to a word sequence — lowercase, and every run of characters
   outside `[a-z0-9]` becomes one space. Quotes, backticks, underscores, dots
   and newlines all vanish, which is what joins S1's split literal.
2. Segment both sides into sentences. A segment ends at `.!?;` before
   whitespace, at a blank line, at a markdown block start, and **at a `|`** —
   the last one is what keeps a ledger row from being one 3,000-word sentence
   whose token set contains everything.
3. `corrected` = the sentences the file held at `A` and does not hold at `B`.
   Derived by set difference on normalised text rather than by parsing hunks,
   so a sentence that merely moved within the file is not called corrected.
4. Build the n-gram index over the corpus, `n = 3`, and weight each n-gram
   `idf(g) = log2(F / df(g))` where `F` is the corpus file count and `df` the
   files carrying `g`.
5. Drop every n-gram that occurs in the changed files **at `B`**. That is the
   whole use of the new wording, and it is what makes the score mean *removed*:
   a phrase the fix kept is not a phrase the fix corrected.
6. `score(corrected, candidate)` = the summed `idf` of the n-grams they share.
   Report a candidate whose score reaches `BITS`.

A bit score rather than a ratio, because a ratio is diluted by length and the
carriers here differ in length by two orders of magnitude — a 12-word test
needle and a 3,000-word ledger cell.

**`BITS` is calibrated, not chosen.** Phase 3 raises it from zero against the
two real ranges and measures the noise over every work-item range in the
release, and the number and the measurement are recorded in that phase's
record. A threshold picked before the measurement is the hand-written list one
constant wide.

### What breaks in six months

The corpus grows and `idf` shifts under every row, so a range that was silent
becomes noisy or the reverse. That is tolerable in the direction it fails: a
growing corpus makes `df` larger and `idf` smaller, so the score falls and the
check goes quiet rather than red. It loses an alarm and never invents one,
which is the direction `rider_check.py`'s own docstring argues for and the same
asymmetry this repository already accepted there.

The second one is sharper. **The check reads the tip of the range, so a
survivor introduced after the range is invisible to it.** It answers *did this
range leave wording standing*, never *is the tree consistent now*. Naming that
is why the report prints what it examined.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Widen contract §12 with the method** — #180's third rule | The rule has been written, read, restated and re-broken seven times, once by a session that had restated it as the cap. An eighth sentence is one more sentence in the state that failed seven times | Rejected — it is the ticket's own *Not this*, and #229 says the second candidate is stronger *because it is a check rather than an instruction, and it can fail* |
| **A curated list of sentences duplicated across the corpus, checked for agreement** | This is #210's finding with new words: a written list of the arms rots, and the list would have to be extended by whoever writes the next shared sentence — the party that just demonstrated it will not | Rejected |
| **Give the reviewer a repeat-fact arm** (#229's first candidate) | A review round cannot see what its own fix pass leaves behind: contract §2 reserves the broad gate for the orchestrator, and S1's module was red from the rewording commit through *two* rounds. The reviewer is the one party structurally unable to run this | Rejected as the primary home; the reviewer already reads the report the check prints |
| **A `git grep` of a phrase the fixer types** | It is the walk that already exists in a reviewer's clone (#269), and it left with the clone. A phrase somebody types is also the coordinate again: the fixer chooses the search key from the finding, which is the judgment §12 says goes wrong | Rejected |
| **Longest-common-phrase with a word floor** | Fails S2 at any floor above three, and accepts the whole corpus at three. Measured above | Rejected |
| **Report only, never fail** — the shape of `issue_claims_check.py` | The act it guards is a commit, not a pull request body, and the loss is silent: S1 shipped red for two rounds with nobody reading anything. A report at a moment nobody is looking is #269's second clause | Rejected for the command; taken for the CI step if phase 3's noise measurement says so, and that is the one thing the measurement decides |

## False positives, and the escape that is not turning it off

**This is the design's real risk and it has three answers, in order of how much
of the class each one takes.**

**First, by construction: a record of a past state is excluded.** Everything
under `seal/specs/*/rounds/` is out of the corpus. A round record and a
reviewer's report carry the SHA they were written against and quote the
defective wording verbatim — that is what they are for, and `skills/implement/SKILL.md`
says so: *a round record carries the SHA it reviewed, so it never asserts a
present state*. Measured on S2: the corrected clause stands in
`rounds/round-2.md` and `rounds/round-2-report.md`, and reporting either would
be wrong. This is one exclusion with a written reason, not a list of paths.

**Second, by construction: struck-through text is excluded.** A `~~…~~` span is
this repository's own mark for a claim it no longer makes — `seal/ledger.md`
row R3 carries three of them — so text inside one is by definition not a
standing sentence. Also one rule, also with a reason.

**Third, by judgment, recorded and content-anchored.** A survivor a person has
opened and judged legitimate gets a row in
`seal/specs/<work-item-id>/survivors.md` naming the path, a **quoted
distinctive substring** of the surviving text, and the grounds. The quote is
the anchor, so the exemption stops applying the moment the text changes, and
what it degrades to is *reported again*. There is no path value meaning *check
nothing*: the row exempts one carrier of one sentence, and the grounds are read
by whoever comes next.

**What this repository's known deliberate pair does under the check, and it is
not the exemption case.** `CLAUDE.md` and `CONTRIBUTING.md` deliberately carry
the same sentence about ledger removals. A branch that corrects it in one and
not the other is reported — and that report is **correct**, because those two
have already disagreed once and the disagreement left a branch with no reading
that permits the only correct act. The deliberate-duplication case is the
check's strongest true positive, not its false one. The exemption exists for
the third kind of carrier: text that quotes the old wording in order to say it
was wrong.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The reader, the check and the calibrated threshold — normalisation, segmentation, corpus enumeration, the two by-construction exclusions, the score, the report and the exit codes | Executed against `7bcf36a` and `ad6f81a`; the curve over 77 real ranges in `phases/phase-1.md` | f168d33 |
| 2 | `bin/survivor-check` + `.cmd`, the exemption reader (S6), the prose at the places that run it (S7), and the CI step | The wrapper cases the suite already parametrises over `bin/`; cases for S4, S5, S6, S7 | 23066d4 |
| 3 | What a probe repository found that the two real cases could not: a threshold that measured this repository's size, and a self-match guard comparing a line across revisions | `tests/test_a_corrected_sentence_survives_elsewhere.py`, 31 cases, and the two mutation sweeps in `phases/phase-3.md` | 28b90da · 198d580 |

**Three phases where the table above first said four, and the merge is the
divergence `overview.md` records.** Planned phases 1–3 were the reader, the
check and the calibration, and none of the three is a runnable slice on its
own: a threshold is a measurement OF the finished check, and the reader's
normalisation is only observable through the score that reads it. Splitting
them would have bought three commits that could not be verified apart.
Planned phase 4 is phase 2 here, unchanged. Phase 3 is new, and it is the
phase the plan could not have named — see its record.

## Operational impact

- **New command**, `survivor-check`, shipped through `bin/`. `bin/` is on the
  Bash tool's PATH while the plugin is enabled, so this reaches users at the
  next release the same way a skill does.
- **A new CI step** on `hygiene.yml`, whose failure mode phase 3 decides.
- **No new dependency.** Standard library only, and no construct above the
  interpreter floor — `tests/test_a_script_says_which_interpreter_it_needs.py`
  enumerates every shipped script, so this one either stays at the floor or
  owes a guard.
- **No migration.** A repository with no `survivors.md` has no exemptions,
  which is the state every repository is in today.
