# Feature Specification: the census and the tie that nothing holds

<!-- seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/spec.md
— WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three sets of #424 leftovers, all left open where that run capped before it
could spend them as reopenings: #469, #470 and #471. Not one of them changes
what `correction-check` does. Two of them make a reader believe a number the
same work item measured to be false, and the third leaves half of a sentence
a reader acts on held by nothing.

**What this frame found that the three tickets could not have known.** The
0.12.2 release, commit `a8bf2a86`, folded all three `seal/ledger/*.md`
fragments into `seal/ledger.md` and deleted them. So the corpus every figure
in `correction_check.py` is stated over has moved twice since the figures were
taken, and #470's own prescribed repair — *state it over `seal/ledger.md`
alone, a corpus a branch cannot move* — names a corpus that a release has
already moved and that **this branch moves again** the moment it corrects
ledger row C1. The corpus rule this work writes has to survive that, and the
figures it states have to be taken after the branch's own ledger edit rather
than before it. `plan.md`'s phase order exists for that reason.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §5 — *Nothing that reaches you in prose is evidence*, *an aggregate is not a coordinate* | Why this spec states no digit. Every figure the three tickets and the round reports hand over was taken before the 0.12.2 fold; each is re-measured at this branch's tip or it is not written |
| `skills/agent-contract/SKILL.md` §12 — *A defect belongs to a class — enumerate the class* | Why A4 enumerates the sites by construction rather than from round 3's list of six. Two of those six have moved: the ledger fragment was folded into `seal/ledger.md` and the changelog fragment was gathered into `CHANGELOG.md` §0.12.2, which is a seventh site |
| `skills/agent-contract/SKILL.md` §14 — *A fix that changes what a person sees documents it and pins it* | #471's whole argument. The parent SHA is the line that decides which hunk a person opens, and half the sentence that chooses it shipped with nothing holding it |
| `skills/agent-contract/SKILL.md` §15 — *A new case is not planted until it has been seen red* | Both cases this work plants are shown failing first, and A7 fixes exactly which mutation counts as the red — a census case can be made green by the wrong instrument as easily as by correct code |
| `CLAUDE.md` §*A ledger coordinate names content, never a position* | A9. `seal/ledger.md:1172` stands in the module comment, in a test docstring and in the work-item records as the address of the longest qualifier. A line number is the coordinate this repository's own rule refuses |
| `CLAUDE.md` §*A change writes fragments, never the shared file* — *Appended is the word, and a removal is not one* | Why this branch may touch `seal/ledger.md` at all. Row C1's claim is false, so leaving the ledger true means correcting it there; new claims go in this work item's own fragment |
| `CONTRIBUTING.md` §*House rules* — *One branch does edit `CHANGELOG.md`, and it is the one based on `main`* | Why the seventh site, `CHANGELOG.md` §0.12.2, is Q1 rather than an acceptance row. This branch is not that one |
| `skills/implement/SKILL.md` §*Document layout — two roots, three lifetimes* | The line A4 draws between a record that asserts a PRESENT fact — `spec.md`, `plan.md`, `overview.md`, `changelog.md`, a ledger row — and one that asserts a PAST state at a named SHA — `rounds/round-N.md`, `rounds/round-N-report.md`, `phases/phase-N.md`. The first kind is corrected; the second is the audit trail every correction cites and is left alone |
| `skills/code-review/orchestration.md` — *A fix pass adds no mechanism* | Why #469 is a work item at all. The corpus walk is mechanism, so #424's fix passes could not add it, and it was deferred to an issue instead of built |

## Scope

### In

1. **#469 — a case that takes an independent census over the real ledger
   corpus and asserts the bound covers every candidate site** (A7). The
   property, never a spelling and never a number. The instrument is not
   `MARKER`, the case says how its number was taken, and it names what it
   does when the corpus grows a longer run.
2. **#470 — the two arithmetically false statements the module makes about
   its own corpus** (A1, A2, A3, A4, A6). The bound comparison, restated over
   a named corpus with its instrument and the moment it was taken; and the
   `404 on 190 rows` sentence, corrected at every present-state site the class
   actually has at this SHA.
3. **#471 — the tie clause of the parent-naming rule** (A8). Round 3's
   paste-ready `test_a_tie_falls_to_the_first_parent`, driven green on shipped
   code and red on the mutation that reverses the walk.
4. **The positional coordinates for the longest qualifier** (A9), replaced by
   content ones.
5. **The evidence this work drifts or establishes** (A10).

### Explicitly out

- **Removing the bound.** #469's *Not this*.
  `test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier` is red without
  it, and the bound is what stops a verb reaching across a clause to a date
  nobody wrote it against.
- **Pinning another literal spelling.** That is the repair that has now failed
  twice, once inside the fix for the other time.
- **Re-measuring anything with `MARKER`.** #470's *Not this*, and A7 turns it
  into a mutation the case must be shown to survive.
- **Removing the numbers.** #470's *Not this*. A bound with no stated census
  is how the first two went wrong.
- **Any change to what the check does.** `MARKER`, `markers`, `rows`,
  `standing`, `losses`, `marker_counts`, `honoured` and `examine` keep their
  behaviour; no exit code, verdict or printed line moves. What this work adds
  is cases and true sentences.
- **`CHANGELOG.md` §0.12.2, unless Q1 is answered otherwise.** It carries the
  same false figure and it is a released section of a file `CONTRIBUTING.md`
  says this branch does not edit. A4 states what happens under the default.
- **Editing the body of #469.** Round 3 measured that its histogram table is
  neither corpus and sums to 412. `agent-contract` §6 withholds posting from
  every agent, so no agent repairs it; Q2 is where it goes.
- **`rounds/round-N.md`, `rounds/round-N-report.md` and `phases/phase-N.md` of
  work item 1789969379.** They assert a past state at a named SHA and they are
  the audit trail the corrections cite.
- **A structured correction column in place of the prose convention.** The
  module docstring already names it as what would close the class this check
  cannot see; it is not this work item.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given `correction_check.py`, when a reader looks for a figure about the corpus, then there is exactly **one** site that states one — the census note beside `MARKER` — and the module docstring and every other comment point at it rather than restating a digit | `grep -nE '[0-9]{3}' skills/evidence-check/scripts/correction_check.py` returns digits only inside the census note (and `SIZE_CAP`'s arithmetic). Six sites stating one number is the defect #470 reports; the repair is one site, not six corrected ones |
| A2 | Given the census note, when a reader asks what any figure in it is true of, then the note states three things for every figure and a reader can re-take it from them: the **corpus** (`seal/ledger.md` alone, named with why), the **instrument** (the unbounded walk, stated as explicitly not `MARKER`), and the **moment** (the date it was taken, with the two ways the corpus moves under it — a release folding fragments in, and a branch correcting a row, this branch included) | The walk the note describes, re-run at the branch tip, reproduces every digit in the note. The note's reason for choosing `seal/ledger.md` is *it is what a release folds the fragments into and what survives one*, and nowhere claims a branch cannot move it |
| A3 | Given the tree, when a reader looks for a figure stated over *the three ledger files*, then there is none — that corpus does not exist at this SHA | `a8bf2a86` deleted all three `seal/ledger/*.md` fragments (read: `git show --stat a8bf2a86`), and `seal/ledger/` is absent from the working tree. `grep -rn 'three ledger files\|411\|412\|413' --include='*.py' --include='*.md'` over the tracked tree returns only past-state records |
| A4 | Given the class *statements that `seal/ledger.md` carries 404 marker occurrences on 190 rows*, when this work closes, then every **present-state** site has been enumerated by construction and corrected, and every **past-state** record is untouched | The class is taken by grepping the tracked tree for the figure, not from round 3's list of six — two of which have moved (the ledger fragment folded into `seal/ledger.md` as row C1; the changelog fragment gathered into `CHANGELOG.md` §0.12.2, a site the list does not name). Under Q1's default the released `CHANGELOG.md` copy is left, and that divergence is a row of this work item's `overview.md` §*Not verified* naming the repository owner, plus a `seal/follow-up.md` item |
| A5 | Given a correction this work makes, when a reader asks what stood there and who says otherwise, then the marker beside it says so — and the marker's spelling is decided by **which file class it sits in** | An SDD record takes the marker work item 1789996775 fixed, adopted verbatim: `<!-- CORRECTED <date> by work item 1789996780 (#<issue>). What stood here: "<quoted>". It is false because <what disproved it, with the coordinate>. … -->`, uppercase verb. `seal/ledger.md` row C1 takes the ledger's own sentence-case `Corrected <date> by work item 1789996780 (#470).` in its Notes cell, because `correction-check` reads that file and that spelling. Code and test comments are corrected in place with no marker: git history is the audit trail for code, and a marker there would answer a hand-grep for the ledger's |
| A6 | Given `seal/ledger.md` row C1, when a reader takes its Notes cell, then it no longer states both halves of the contradiction in one sentence — the file's total, the part on rows and the part in prose are distinguished, and the sentence says the survival test never acts on the prose part | Round 3's paste-ready text is the shape; the digits in it are **re-measured at the branch tip**, after every ledger edit this work makes, and never restated from the report. `correction_check.py`'s own §*Markers in prose are out of scope, by construction* is the rule the sentence must agree with |
| A7 | Given the real ledger corpus, when the census case runs, then it asserts the **property** — every candidate marker site the unbounded walk finds is one `MARKER` also sees — and asserts **no count**; it reads the corpus through the module's own `LEDGER` and `FRAGMENTS` constants rather than a hard-coded file list; it refuses to pass over an empty corpus; and its docstring states how its number was taken and why the instrument cannot be `MARKER` | Two mutations, and the pair is the point. **Narrow the bound to four → the case goes red**, naming the file, the row, the run length and the spelling, because the tree carries a five-word run. **Narrow the bound to four AND take the census with `MARKER` → the case stays green**, which is the circularity that went wrong twice, demonstrated rather than asserted. Both are run and recorded; the second is what proves the instrument choice load-bearing |
| A8 | Given a merge where both parents carry one marker and the resolution drops it, when `correction-check` reports it, then it names the **first** parent, and a case says so | Round 3's paste-ready `test_a_tie_falls_to_the_first_parent`, planted in `tests/test_a_merge_cannot_silently_drop_a_correction.py` beside `test_the_parent_named_is_the_one_that_lost_the_most`. Green on shipped code; **red on the mutation that walks the parents in reversed order** — the mutation round 3 measured leaves 48 of 48 green. §15: the red is shown and the handover says how |
| A9 | Given a statement naming the longest qualifier the tree carries, when a later commit moves lines in `seal/ledger.md`, then the statement is still true | Every site addressing it as `seal/ledger.md:1172` — the census note, `test_the_longest_qualifier_the_tree_carries_is_seen`'s docstring, and the work-item records — names the row and the spelling instead. `CLAUDE.md`: a coordinate names content, never a position. Whether that spelling is still the longest at this SHA is Q6, a measurement |
| A10 | Given the evidence this work touches, when it closes, then the ledger is true about it | New rows in `seal/ledger/1789996780-the-census-and-the-tie-that-nothing-holds.md` for the census case (A7) and the tie case (A8), each naming the case and the mutation that reddened it. C1 corrected in `seal/ledger.md` (A6). Whether the comment edits drift the anchors `#MARKER`, `#VERBS`, `#markers` and `#examine` is Q3: **every row citing a drifted coordinate is read by hand before `evidence-check --reverify` runs**, because `--reverify` re-stamps every row that cites a coordinate the drift report names once |
| A11 | Given the whole change, when the module and its suite run, then nothing a person reads has moved except the sentences this spec names | `tests/test_a_merge_cannot_silently_drop_a_correction.py` stays green with nothing excused and grows by exactly the two cases. No exit code, verdict or printed line changes — the work adds cases and corrects prose |

## Data & interfaces

No schema, no endpoint, no payload. The surfaces, with the evidence
coordinate where one exists:

| Surface | What moves | Ledger anchor |
|---|---|---|
| `skills/evidence-check/scripts/correction_check.py` module docstring | the figures leave it; it points at the census note (A1, A4) | none — the docstring is not an anchored unit |
| `skills/evidence-check/scripts/correction_check.py` census note, above `MARKER` | rewritten: corpus, instrument, moment, and the conclusion the figures support (A1, A2, A3, A9) | `skills/evidence-check/scripts/correction_check.py#MARKER@17486986`, row C1 — whether a comment above the assignment drifts the hash is Q3. **It does not**: the anchor covers the assignment alone, so the note was rewritten whole and `evidence-check` reported no drift on it (measured 2026-09-22). The path was missing from this cell when the frame was written, which made `evidence-check`'s records arm read it as a live claim it could not resolve and exit 2 |
| `skills/evidence-check/scripts/correction_check.py#examine` | nothing. The tie clause its comment states is what A8 pins | `skills/evidence-check/scripts/correction_check.py#examine@73c871f1`, rows C8 and C9 — unchanged, so neither drifts. Confirmed 2026-09-22: `evidence-check` named neither. The path was missing here too |
| `tests/test_a_merge_cannot_silently_drop_a_correction.py` | two new cases (A7, A8); the `404 on 190 rows` docstring at `test_both_verbs_count_because_re_read_is_the_common_one` corrected (A4); the positional coordinate in `test_the_longest_qualifier_the_tree_carries_is_seen` (A9) | the module's anchored cases are cited by rows C1–C9; A7 and A8 add rows rather than moving them |
| `seal/ledger.md` row C1 | the contradicting sentence corrected in place, with a sentence-case `Corrected <date>` marker (A5, A6) | the row itself |
| `seal/specs/1789969379-…/spec.md`, `plan.md`, `overview.md`, `changelog.md` | the false figures corrected in place under `<!-- CORRECTED … -->` (A4, A5) | none |
| `CHANGELOG.md` §0.12.2 | nothing, under Q1's default | none |
| `seal/ledger/1789996780-….md` | this work item's new rows (A10) | new fragment |

**One consequence of A5 the plan is built around.** Writing `Corrected <date>`
into C1 adds a marker to `seal/ledger.md`, which is the corpus the census note
states its figures over. The figure is therefore taken **after** that edit, at
the branch tip, and the note says the corpus moves. Stating it earlier is the
third mechanism #470 reports, repeated by the fix for it.

## Open questions → questions.md

Six rows. Two are a person's and `smith` must not answer either; three are
measurements it takes itself; one belongs to the work.

Framed 2026-09-22 by framer, before the build.
