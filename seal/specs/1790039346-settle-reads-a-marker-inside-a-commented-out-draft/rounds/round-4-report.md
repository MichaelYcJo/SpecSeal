# Round 4 — the verifying round, against round 3's fix range

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

Target SHA `3c1372d6aa7ff3845c74884f5668df2dcf639db8`. Fix range
`b202171cb6d44f21022119797b37dbf034b12225..dbe8006cfe9786693e861efa960a190b7673d4aa`,
three commits. Every command below ran in a `git clone --no-local` of this
repository at the target SHA.

## What this round found, in one paragraph

Round 3's finding 1 is **not closed**. Its named shape — one code span that
quotes a closing delimiter and then an opening one — is closed, and the
control run proves it. The *class* is not: the pass computes its stop inside
one span, so a line whose closing delimiter sits in an earlier span and whose
re-opening delimiter sits in a later one still has that opener blanked, still
reads a parked marker as a fold record, and still takes `settle --retire`
from *nothing to retire* at exit 1 to `removed seal/specs/<id>/` at exit 0.
That is the fourth formulation doing what the second and the third did, one
span further along, and it is the fourth round of this branch to find the
repair moving the fold gate toward deleting.

The contract the same commit added says the opposite, as a measured fact:
*it never reads live a line that reading parks … fuzzed at 0 over 40,000
generated documents*. Rebuilt independently, that oracle agrees with the fix
pass's criticism of round 3's — a pure HTML reading does not know code spans
and cannot produce a cheap-direction count at all, which is why round 3's
`0 cheap` was a tell. The rebuild is a correction and not a tuning. What is
wrong is the **generator**, not the oracle: over 40,000 documents whose lines
carry at most one code span the expensive count really is 0, and over 40,000
documents whose lines can carry several it is 21.

---

## 🔴 1 · The stop is computed inside one span, so a closing delimiter in an earlier span does not stop the blanking in a later one

`skills/verify/scripts/unverified_check.py#blank_code_spans`, the `else` arm
(`stop = span.find(CLOSER)`, at `skills/verify/scripts/unverified_check.py:378`).

`a8648f33` narrowed the blanking to the openers that appear before **the
span's** first closing delimiter. The span is the wrong unit. Inside a parked
draft the backticks are not spans at all, and the draft ends at the first
closing delimiter **on the line**, wherever it happens to fall — including
inside an earlier run of backticks that the pass is treating as a span of its
own. Everything after that point is ordinary text, so an opening delimiter
there re-opens the draft and must not be blanked. The shipped rule starts each
later span's stop search from scratch, finds no closing delimiter inside that
span, sets `stop = len(span)`, and blanks the opener.

**Why it matters.** The marker below the line then reads as a genuine fold
record, `folded_items` returns the work item's id, and `settle --retire`
deletes that work item's whole SDD set with nothing having absorbed it. This
is the harm round 3's finding 1 named, at exit 0, with a success line printed.

Executed, on a throwaway git repository, with a `docs/` policy document whose
parked draft carries the line

- `prose that quotes` — closing delimiter in one span — `then` — opening
  delimiter in a second span — `here`

| Shape | exit | stdout | directory |
|---|---|---|---|
| closing delimiter in one span, opening delimiter in a **later** span | **0** | `removed seal/specs/1700000042-quoted/` | **deleted** |
| round 3's shape, both delimiters in **one** span (control) | 1 | *nothing to retire* | kept |
| a draft with no quotation at all (control) | 1 | *nothing to retire* | kept |

The same shape read through `settle.coordinates` puts the parked draft's row
under `1700000002-beta`, the section the quotation was never part of.

**It does not rest on a contested markdown subtlety.** Both readings park the
marker, and they park it for different reasons, so either one alone condemns
the line: a pure HTML reading, which knows no markdown at all, ends the
comment at the first closing delimiter in the document and the later opening
delimiter starts a new one; the interleaved reading ends the comment at the
same place, re-enters markdown, pairs the remaining backticks into a span that
**stops before** the opening delimiter, and reads that delimiter as real.
`comment_scan` over the raw five-line document answers *began inside* for the
marker line; the shipped pipeline answers *began outside*.

**The corpus is unmoved and the shape does not occur today.** Re-derived
rather than carried: `seal/ledger.md` 761 not-live lines, 94 live marker
occurrences over 83 unique ids, the three named markers live at lines 767,
992 and 1619, and 0 lines of the whole corpus — the shared ledger, every
`seal/ledger/*.md` fragment and every top-level `docs/` document — answering
differently from the rule that blanked every span or from round 3's rule. Two
lines of `seal/ledger.md` do already carry more than one delimiter-bearing
span (80 and 1891), and neither sits in a parked draft, so no answer moves.
What keeps this harmless today is that no instance occurs, not that the shape
cannot.

**The fix.** The stop belongs to the line, not to the span: an opener is
blanked only when no closing delimiter occurs earlier on the line, inside a
span or out of one. The direction is safe. If the line really was inside a
draft, the draft ended at that closing delimiter and the opener is real, so
leaving it alone is correct. If it was not, the closing delimiter is inert,
the span is a real span, and leaving the opener alone only parks more lines —
the mistake this module has already chosen. Measured with the patch applied:
finding 1's shape parks again, both modules stay green at 178 passed exit 0,
the corpus figures are unchanged (761, 83, the three markers live, 0 lines
differing), and in the same structured 40,000-document fuzz the expensive
direction goes from 21 lines to **0** while the cheap direction rises from
3,758 to 5,287. The paste-ready patch is below.

**The altitude answer, named and not taken.** The only formulation that has no
residue is the interleaved walk itself — comment state and code spans read in
one pass. `live_lines`'s docstring says why it is not on offer here: the scan
serves `strip_comments`, whose exact output `seal/ledger.md` pins, and
`readable()` is refused a third pass by
`tests/test_chain_hooks.py#reader_blanking_passes`. Four formulations have now
each closed one shape of the approximation and opened the next, so the choice
between another narrowing and a real walk is worth making deliberately rather
than by default.

## 🟡 2 · The contract states a guarantee as a measured 0, and it is false

`skills/verify/scripts/unverified_check.py#blank_code_spans`, the
*What it guarantees* bullet at
`skills/verify/scripts/unverified_check.py:307`. The same claim is carried by
`spec.md` G3, `plan.md` §*Operational impact*, `overview.md`'s correction row
and R8 of the work item's ledger fragment.

The bullet reads *It never reads live a line that reading parks … Fuzzed
2026-09-22 over 40,000 generated documents of delimiters and backtick runs:
**0***. Finding 1 is a counterexample, reproduced by hand and executed end to
end, so the sentence is false as a guarantee. The number behind it is a
coverage artifact.

Rebuilt independently, the oracle the fix pass describes is the right one and
its criticism of round 3's is correct: a pure HTML reading does not know code
spans, so it counts the pass's whole purpose as a violation and can never
report a cheap-direction disagreement — round 3's `0 cheap` is that artifact
showing. What the rebuild did not fix is the generator. With a generator whose
lines are a random run of tokens, at most one code span a line in practice, I
reproduce the reported answer: 0 expensive over 40,000 documents. With a
generator that can put several spans on one line, the same oracle and the same
count of documents give 16 documents and 21 lines in the expensive direction,
and finding 1's shape is what they are.

**Why it matters beyond the wording.** This is a gate's stated contract, and
`CONTRIBUTING.md` §*What a change to a gate must carry* is what asks for it.
The next session measures its formulation against this paragraph, exactly as
the paragraph asks. A reader who trusts the 0 will not re-run the fuzz, and
neither the oracle nor the generator is in the tree, so no reader can. A
figure nobody can re-derive is the aggregate `skills/agent-contract/SKILL.md`
§5 is about: the number can be checked, the claim it stands for cannot.

**The fix.** Say what is guaranteed and what was measured, keep them apart,
and name the generator's shape so the next reader knows what the number covers.
The paste-ready wording is below; it is written for the code with finding 1's
patch applied, because the sentence has to be true of whatever ships.

## ⬜ 3 · `spec.md` G3 says three formulations moved the gate toward deleting; the docstring says two of the three before this one

`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39`
against `skills/verify/scripts/unverified_check.py:303`.

Both sentences landed in this fix range, one commit apart, and they count the
same history differently. Read from the branch: blanking every span was
formulation 1 and its defect left drafts open — more lines parked, a row
misfiled, not a directory deleted. Formulations 2 and 3 each moved the gate
toward deleting and a round caught each. That is *two of the three*, which is
what the docstring says. G3's *three* has no third. It is a correction to the
run's paperwork rather than a defect in the tool, so it is outside
`Needs a fix`.

## ⬜ 4 · A stamp on a round report is tracked as a live claim — confirmed

`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61`.

Confirmed rather than re-opened, as the hand-over asked. The anchor
`skills/settle/scripts/settle.py#coordinates` is quoted in seven places
across five files — both ledger fragments, `spec.md`, `round-2.md`,
`round-1-report.md` and `round-2-report.md` twice — so a commit that moves the
unit rewrites all of them; `68a023af` is that commit, four files and five
stamps. The consequence the observation names is in the tree: `round-2.md`
carries `Target SHA 7f2d6f1c` and, beside it, the hash the unit first had at
`281308c7`, which is not an ancestor of `7f2d6f1c` — `git merge-base
--is-ancestor` exits 1. The record states a value that did not exist at its
own target. A home for the decision is `seal/follow-up.md`, not this branch.

---

## What was verified and holds

**Round 3's finding 1, the named shape.** Closed. Executed: with both
delimiters in one span, `settle --retire` refuses at exit 1 and the directory
stays. The residue is finding 1 above, which is the class and not the shape.

**Round 3's finding 2.** The HTML ground is gone from all four live sites the
round named, and the census of six is answerable. Swept the tree for the
ground: the only live site that still carries the phrase is `overview.md:44`,
and it carries it to say the row used to rest on it and that it is false.
Everything else that matches sits in `round-2.md`, `round-2-report.md`,
`round-3.md` and `round-3-report.md` — round records, which are history and
were correctly left alone. What replaces the ground is finding 2 above.

**Round 3's finding 3.** Fixed. The `OPENER` constant's comment no longer
claims that no reader blanks into a span holding a closing delimiter, and
`CLOSER` is a constant beside it with the reason.

**The two new units, against the mutation that should redden each.** Derived
rather than taken. Three mutations, each applied alone and restored, tree
byte-identical after each:

| Mutation | What goes red |
|---|---|
| drop the stop — blank every opener in the span (round 3's rule) | `test_an_opener_after_a_quoted_closer_still_parks_the_marker_below` **alone**, 1 failed of 62 |
| `CLOSER` no longer spells the closing delimiter | the same case alone, 1 failed of 62 |
| blank the whole span that holds an opener (round 1's rule) | `test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in` alone, 1 failed of 62 |

So `CLOSER`'s **value** is pinned, not merely its existence, and the new case
is red against exactly the formulation it replaced and green against the two
before that — which is the right pin for a case that marks one step of a
narrowing. Neither unit is vacuous. `tests/test_unverified_rows_close.py`
stays at 116 passed under all three.

**The docstring's four contract claims.** Three hold.

| Claim | Verdict |
|---|---|
| *What it approximates* — the pass is state-free and runs before `comment_scan`, so it cannot be the interleaved reading | true; `live_lines` composes the pass ahead of `opens_outside_a_comment`, and its docstring gives the reason the walk is not on offer, although it never uses the word |
| *What it guarantees* — never reads live a line that reading parks, 0 in the fuzz | **false**, finding 2 |
| *What it gives up* — parks lines reading calls live, 132 in the same fuzz | direction true, figure not re-derivable; a different generator gives a different number and none is in the tree |
| *Which mistake it prefers* — the second, as `settle.py`'s module docstring chooses | true; that docstring says the failure the arrangement may produce is *a thin policy document, which a reader can see, rather than a directory deleted with nothing absorbing it, which nobody can* |

The figures are the fix pass's own and not round 3's: round 3 recorded 5
expensive and 0 cheap, the docstring records 0 and 132.

**The sentence the survivor sweep caught.** The docstring now says the pass
blanks *an opener and never the span around it … not every opener, either:
only those before the span's first closing delimiter*, and the code blanks an
opener whose end is at or before the span's first closing delimiter. The
sentence matches the code exactly. The code is what finding 1 is about, so the
prose followed the stop this time and the stop is what was wrong.

**The fix pass's own depth reading.** Agreed. The new case pins a defect in
the `else` arm round 2's pass created, `blank_code_spans` itself is a build (NAME NOT IN TREE)
unit, and depth 1 is the right reading. `round-record` measured 1 and did not
refuse it.

**`spec.md` G3 judges the build rather than excusing it.** It names its own
false ground and says which round found it false, states the direction and
what the rule gives up, and does not claim the widening was forced. Its
factual claims: `folded_items` is reached by the hygiene workflow's
unverified-record step through the `--baseline` arm at
`skills/verify/scripts/unverified_check.py:1119`, which is what
`.github/workflows/hygiene.yml:161` passes — true. A case seen red first —
true, by mutation. Round 2's exit 1 to exit 0 measurement — carried from
round 2's record, not re-run here. The fuzz guarantee — false, finding 2. The
count of formulations — finding 3.

**The corpus invariant survives the fourth formulation.** Re-derived, not
carried: 761 not-live lines in `seal/ledger.md`, 94 live marker occurrences
over 83 unique ids, the three named markers live at 767, 992 and 1619, and 0
lines of the corpus answering differently from the rule that blanked every
span or from round 3's rule.

## Questions nobody in this round can answer

The broad gate. `skills/agent-contract/SKILL.md` §2 gives the full suite, the
repository-wide lint and the typecheck to the sealer, and this definition
hands me none of the three. The orchestrator reports the four affected modules
at 335 passed exit 0, `evidence_check.py --strict .` at exit 0 with 0 drifted
and 0 broken, and `survivor-check` at exit 0, all at this SHA; this round did
not re-run them and does not certify them. The caller answers it.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The stop is computed inside one span, so a closing delimiter quoted in an earlier span does not stop the blanking in a later one — a marker inside a parked draft reads as a fold record and `settle --retire` removes the work item's directory at exit 0 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | open | Round 3's finding 1 is closed for its named shape and open for its class. Executed on a throwaway git repository: the two-span shape takes `settle --retire` from exit 1 *nothing to retire* to exit 0 `removed seal/specs/1700000042-quoted/` with the directory deleted, while round 3's one-span control and a quotation-free control both refuse at exit 1. `settle.coordinates` files the parked draft's row under `1700000002-beta`. Both readings park the marker — `comment_scan` over the raw document answers *began inside*, and the interleaved reading pairs the remaining backticks into a span that stops before the opening delimiter — so the finding does not rest on a markdown subtlety. Corpus unmoved and no instance today: 761 / 83 / markers live at 767, 992, 1619 / 0 lines differing. The paste-ready patch moves the stop to the line, keeps both modules green at 178 passed exit 0 and the corpus figures unchanged, and takes the structured fuzz's expensive direction from 21 lines to 0 |
| 2 | 🟡 The contract's *What it guarantees* bullet states as a measured 0 that the pass never reads live a line the reading parks; finding 1 is a counterexample and the 0 is a generator artifact | `skills/verify/scripts/unverified_check.py#blank_code_spans` | open | Executed: rebuilt the interleaved oracle independently. With a generator whose lines carry at most one span, 0 expensive over 40,000 documents — the reported answer reproduces. With a generator that can put several spans on one line, the same oracle gives 16 documents and 21 lines expensive over 40,000, and every one is finding 1's shape. The fix pass's criticism of round 3's oracle is itself correct: a pure HTML reading knows no code spans and can never report a cheap-direction disagreement, which is what round 3's `0 cheap` was. So the rebuild is a correction, not a tuning; the generator is what is narrow. Neither oracle nor generator is in the tree, so no reader can re-derive either figure. The same claim is carried by `spec.md` G3, `plan.md` §*Operational impact*, `overview.md` and R8 of the ledger fragment |
| ⬜ 3 | `spec.md` G3 says three formulations moved the gate toward deleting; the docstring one commit earlier says two of the three before this one | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39` | open | Read, and counted from the branch: formulation 1 left drafts open and misfiled a row rather than deleting; formulations 2 and 3 each moved the gate toward deleting and a round caught each. *Two of the three* is right and G3's *three* has no third. Under `seal/specs/`, so a correction to the run's paperwork and outside `Needs a fix` |
| ⬜ | A stamp on a round report is tracked as a live claim, so a record states a value that did not exist at its own `Target SHA` | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61` | confirmed | Confirmed as asked rather than re-opened. The anchor is quoted seven times across five files, and `68a023af` rewrote five stamps in four of them. Executed: `git merge-base --is-ancestor 281308c7 7f2d6f1c` exits 1, so the hash `round-2.md` carries beside `Target SHA 7f2d6f1c` first existed three commits later. A home for the decision is `seal/follow-up.md`, not this branch |
| 🟢 confirmation | Round 3's finding 1 is closed for the shape it named | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Executed: with both delimiters inside one span, `settle --retire` refuses at exit 1 *nothing to retire* and the directory stays, against exit 0 and a deletion before `a8648f33`. The residue is finding 1 above, which is the class rather than the shape |
| 🟢 confirmation | Round 3's finding 2 is closed — the HTML ground is gone from every live site, and the census of six is answerable | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Re-derived the census rather than carrying it: swept the tree for the ground and the only live site still carrying the phrase is `overview.md:44`, which carries it to say the row used to rest on it and that it is false. Every other match is inside `round-2.md`, `round-2-report.md`, `round-3.md` or `round-3-report.md` — records, correctly left alone, because rewriting one deletes what was true at that round. What stands in the ground's place is finding 2 above |
| 🟢 confirmation | Round 3's finding 3 is closed — the `OPENER` comment no longer claims nothing blanks into such a span | `skills/verify/scripts/unverified_check.py:107-118` | **fixed**, verified | Read. The comment states why the closing delimiter is a constant, and `CLOSER` sits beside it |
| 🟢 confirmation | Both new units are red under a mutation and the mapping is one-to-one | both test modules and `skills/verify/scripts/unverified_check.py` | confirmed | Executed, three mutations each applied alone and restored, the file byte-identical after each. Dropping the stop reddens the new case alone (1 failed of 62); spelling `CLOSER` wrongly reddens the same case alone, so its value is pinned and not merely its existence; round 1's rule reddens round 2's case instead, so the new case marks exactly the step it was written for. `tests/test_unverified_rows_close.py` stays at 116 passed under all three |
| 🟢 confirmation | Three of the docstring's four contract claims hold, and the figures are the pass's own | `skills/verify/scripts/unverified_check.py#blank_code_spans` | confirmed | Read and executed. *What it approximates* is true — `live_lines` calls the pass before `opens_outside_a_comment` and the pass holds no state. *Which mistake it prefers* is true — `settle.py`'s module docstring makes the same choice in the same words, a thin policy document a reader can see against a directory deleted with nothing absorbing it. *What it gives up* is true in direction and its figure is not re-derivable. *What it guarantees* is finding 2. Round 3 recorded 5 and 0; the docstring records 0 and 132, so the numbers are the pass's own |
| 🟢 confirmation | The docstring's sentence about which openers are blanked matches the code | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Read against the `else` arm: the prose says *only those before the span's first closing delimiter* and the code blanks an opener whose end is at or before that delimiter. The prose followed the stop this time; the stop is what finding 1 is about |
| 🟢 confirmation | The fix pass's own depth reading is right | `skills/verify/scripts/unverified_check.py#blank_code_spans` | confirmed | Agreed. The new case pins a defect in the `else` arm round 2's pass created, and `blank_code_spans` is a build unit, so depth 1 is the reading; `round-record` measured 1 and did not refuse it (NAME NOT IN TREE) |
| 🟢 confirmation | `spec.md` G3 judges the build rather than excusing it, and its other claims are true | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39` | confirmed | Read and executed. It names its own false ground and the round that found it false. `folded_items` is reached through the `--baseline` arm at `skills/verify/scripts/unverified_check.py:1119`, which is what `.github/workflows/hygiene.yml:161` passes. The case-seen-red item holds by mutation. Its fuzz claim is finding 2 and its count of formulations is finding 3 |
| 🟢 confirmation | The corpus invariant survives the fourth formulation | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed over `seal/ledger.md`, every `seal/ledger/*.md` fragment and every top-level `docs/` document, eleven files: 761 not-live lines; 94 live marker occurrences over 83 unique ids; the three named markers live at 767, 992 and 1619; and 0 lines answering differently from the rule that blanked every span or from round 3's rule |
| ❓ out of verified scope | Whether the repository's full suite, the repository-wide lint and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports the four affected modules at 335 passed exit 0, `evidence_check.py --strict .` at exit 0 with 0 drifted and 0 broken, and `survivor-check` at exit 0, all at this SHA; this round did not re-run them and does not certify them. The caller answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the two affected modules, pristine, in the clone | 178 passed, exit 0, read with `echo $?` and not through a pipe |
| the corpus under four liveness rules — fence-only, blank-every-span, round 3's, shipped | `seal/ledger.md` 761 not live; 0 lines of eleven corpus files disagree between shipped and either earlier span rule |
| unique section ids in `seal/ledger.md` under the shipped rule | 83, from 94 live marker occurrences |
| the three named markers, through the shipped rule | live at `seal/ledger.md` lines 767, 992 and 1619 |
| ten adversarial span shapes — shipped against blank-every-span against round 1's rule against an independently written interleaved reading | nine agree; the two-span shape reads live where the reading parks, and that shape is finding 1 |
| the two-span shape through `settle.coordinates` on a throwaway ledger | the parked draft's row filed under `1700000002-beta` |
| `folded_items` and `settle --retire` over finding 1's fixture, on a throwaway git repository | `{'1700000042-quoted'}`, exit 0, `removed seal/specs/1700000042-quoted/`, directory deleted |
| the same command over round 3's one-span shape and over a quotation-free draft, as controls | exit 1 *nothing to retire* for both, directories kept |
| the same five-line document through `comment_scan` — a pure HTML reading, no markdown at all | the marker line answers *began inside*; the shipped pipeline answers *began outside* |
| a 40,000-document fuzz against an independently written interleaved oracle, lines built from a random token run (at most one span a line in practice) | 0 expensive, 210 cheap lines — the fix pass's reported answer reproduces under this generator |
| the same 40,000-document fuzz with a generator that can put several spans on one line | **16 documents, 21 lines expensive**; 2,281 documents, 3,758 lines cheap |
| the proposed patch — the stop moved from the span to the line — against the same structured fuzz | **0 expensive**; 3,156 documents, 5,287 lines cheap |
| the proposed patch against the two modules and the corpus | 178 passed exit 0; 761 not-live, 83 ids, the three markers live, 0 lines differing |
| three mutations, each applied alone and restored, against the units the `New units` row names | dropping the stop → the new case red alone, 1 failed of 62; `CLOSER` misspelled → the new case red alone; round 1's rule → round 2's case red alone. `tests/test_unverified_rows_close.py` 116 passed under all three |
| the ground census — a tree-wide sweep for the HTML ground the fix range removed | one live site, `overview.md:44`, which carries the phrase only to call it false; every other match is a round record |
| `git merge-base --is-ancestor 281308c7 7f2d6f1c` | exit 1 — `round-2.md`'s stamp postdates its own `Target SHA` |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it, and what stands between it and that spawn is finding 1 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 | the orchestrator |

## Paste-ready fixes

Finding 1. In `blank_code_spans`, hoist the stop out of the span loop so it is (NAME NOT IN TREE)
the line's first closing delimiter. Replace the two lines that compute the
runs and the cursor:

```python
        runs = [(m.start(), m.end()) for m in re.finditer(r"`+", line)]
        chars, i = list(line), 0
        # The stop is the LINE's first closing delimiter, not each span's.
        # Inside a parked draft these backticks are not spans at all: the
        # draft ends at the first closing delimiter on the line, wherever it
        # falls, and every delimiter after that point is ordinary text. A
        # closing delimiter quoted in an EARLIER span ends the draft just as
        # surely as one quoted in this span, so blanking an opener after it
        # re-opens a draft that reading has already closed — a parked marker
        # read as a fold record, and `settle --retire` removing the directory
        # at exit 0 (round 4, finding 1; round 3, finding 1 one span over).
        # Outside a draft the earlier closing delimiter is inert and the whole
        # run really is a span, so the surviving opener parks the lines below
        # it instead: fewer lines live, a fold reported as a deletion, which
        # is the direction this module has already chosen to be wrong in.
        stop = line.find(CLOSER)
        stop = len(line) if stop == -1 else stop
```

and replace the `else` arm's stop computation and loop:

```python
            else:
                # The DELIMITER, not the span around it — and only the
                # openers this span can still be quoting, judged against the
                # line's stop above rather than this span's own text.
                for m in re.finditer(re.escape(holding), span):
                    if start + m.end() <= stop:
                        chars[start + m.start() : start + m.end()] = " " * len(holding)
```

The `CLOSER` constant's comment loses one word, because the stop is no longer
the span's:

```python
# The opening delimiter of an HTML comment, and the only one `live_lines` asks
# `blank_code_spans` to look for. Its pair is a constant too, and only because
# the pass has to know where a line's quotation STOPS: inside a parked draft
# the first closing delimiter on the line really ends it, so an opener after
# that point is ordinary text and a real opener. Nothing blanks a closing
# delimiter — see `blank_code_spans`'s docstring for why a surviving one is
# the safe half.
OPENER = "<!--"
CLOSER = "-->"
```

The case that pins it, beside the one round 3 planted. Shown red by reverting
the patch above, where it fails on its only assertion with the row reported
under the section the quotation was never part of:

```python
def test_a_closer_quoted_in_one_span_stops_the_blanking_in_a_later_one(tree):
    """The residue round 4 found in round 3's repair. The stop was the span's
    and it belongs to the line: inside a parked draft the backticks are not
    spans at all, so a closing delimiter quoted in an EARLIER span ends the
    draft and an opener quoted in a LATER one re-opens it. Blanking that
    opener read a parked marker as a fold record, and `settle --retire`
    removed the directory at exit 0 with nothing having absorbed it."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the line below ends it and re-opens it
        + "prose that quotes `--> and x` then `<!--` here\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n"
        + "-->\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" not in rows.get("1700000002-beta", []), dict(rows)
```

Finding 2. Replace the *What it guarantees* and *What it gives up* bullets of
`blank_code_spans`'s contract, written for the code with finding 1's patch (NAME NOT IN TREE)
applied:

```python
    - *What it guarantees.* Against every shape measured so far it has not
      read live a line the interleaved reading parks, which is the direction
      that retires a directory and the one this module may not be wrong in.
      That is a measurement and not a proof: the pass is an approximation of
      a reading it cannot perform, and three formulations before this one
      passed the fuzz of their day and were broken by a shape the generator
      did not build. Measured 2026-09-22 over 40,000 generated documents
      whose lines carry SEVERAL code spans each — the generator's shape is
      the whole of what a count like this covers, and a generator of
      single-span lines reports 0 for a rule that has this defect: **0**.
    - *What it gives up.* It parks lines the reading calls live — 5,287 over
      the same 40,000 documents. A marker that stops counting is a fold
      record unread: a directory kept and a deletion reported, which a person
      can see.
```

Finding 3. In `spec.md` G3, the count:

```
Two of the three formulations before this one moved the gate the other way
and a round caught each
```

---

Needs a fix: yes — finding 1, the span-local stop, which still removes a work
item's directory at exit 0 on a line whose closing and re-opening delimiters
sit in different code spans; and finding 2, the contract's guarantee, which
is stated as a measured 0 and is false.
Loses a record or crashes: yes — finding 1, a work item's whole SDD set
removed at exit 0 with nothing having absorbed it, executed on a throwaway
git repository at the target SHA.

Files opened: `skills/verify/scripts/unverified_check.py`,
`skills/settle/scripts/settle.py`,
`tests/test_settle_reads_before_it_removes.py`,
`tests/test_unverified_rows_close.py`, `bin/test`,
`.github/workflows/hygiene.yml`, `CONTRIBUTING.md`, `CLAUDE.md`,
`seal/config.md`, `seal/ledger.md`,
`seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`,
and, under
`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/`:
`spec.md`, `plan.md`, `overview.md`, `survivors.md`, `rounds/round-2.md`,
`rounds/round-3.md`, `rounds/round-3-report.md`.

Every command ran in a `git clone --no-local` of this repository at
`3c1372d6aa7ff3845c74884f5668df2dcf639db8`. Probe files were named
`test_tmp_*`, ran once, and are deleted; the clone and the virtualenv
`bin/test` built inside it go with this round. Nothing was written,
committed, pushed or posted in the working tree except this report.
