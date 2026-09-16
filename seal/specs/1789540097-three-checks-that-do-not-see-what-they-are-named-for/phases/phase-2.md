# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | <pending> |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#418. The three search phrases the two sweeps look for become module
constants that both the sweep cases and the seam-safety case read, so the set
that case checks is every phrase either sweep searches for rather than a copy
of it. The folded members are pinned as well, so a `.py` member joining a
sweep turns the case red. The reason the set is closed rather than short is
written where a reader meets it, and the residue goes beside the constants.
Both of #418's measured mutations have to go red; the issue's paste-ready
patch closes only the second.

## What this phase found

**The closure's number is wrong everywhere it is written, and the number is
the whole of the closure argument.** #418 states *Across both sweeps exactly
four members are `.py`*; `plan.md` §*Technical context* and `spec.md` scope
item 2 both carry it. Measured with the module's own lists:

```
skills/verify/scripts/seal_stamp.py
skills/code-review/scripts/round_record.py
skills/verify/scripts/broad_gate.py        <- SEAL_SWEPT, three
skills/verify/scripts/session_cost.py
tests/test_session_cost.py                 <- SEGMENT_SWEPT, two
```

**Five.** The SUBSTANCE of the argument is untouched — `swept` is still every
phrase either sweep searches for in the members `flat` folds, and seven is
still the right size — so what was wrong is the count and not the claim. The
docstring and the pinned tuple say five, and the pinned tuple is what makes
the number impossible to restate wrongly from here: it is the list itself
rather than a number beside it. This is `agent-contract` §5's aggregate in
its own habitat — a number that can be checked standing in for a claim that
had not been, and it reached three documents.

**Q3 is answered `leave it`, the default, and the reachable shape was looked
for before taking it.** An assertion that the sweep cases actually read the
constants has to recognise what "searching for a phrase" looks like inside a
case body, which is the second implementation of the sweep that #418's own
*Not this* refuses. Counting each phrase's occurrences in this module's own
source is not that, but it is unusable: `the seal` stands in comments, in two
docstrings and inside the seam fixtures `'"the " "seal is taken once"'`, so
the count is noise. The risk is written beside `SEAL_BARE` instead, naming
the folded-member assertion as what covers the other half of the same hole.

**`SEGMENT_LOOSE` is a mapping rather than a tuple**, because the segment
sweep's two assertions carry different messages and folding them into one
loop would have cost the per-phrase message. The phrase is the key, so the
seam case reads `*SEGMENT_LOOSE` and gets the phrases alone.

**Mutation 2 surfaced a bare `the seal` in `chain_check.py:668` and it is not
a defect.** With that file in `SEAL_SWEPT` the sweep case went red too, on
*Named for the COMMAND that writes it, not for the seal* — a comment that
DISCUSSES the word, with the collision named in the next sentence, which is
the shape both existing `SEAL_EXCLUDED` entries have. Bringing the file under
the sweep would need an exclusion and is a change to what a test guards, so
it is not made here; it is reported rather than fixed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The two per-phrase literals and their messages in `test_no_shipped_document_calls_a_spawn_cycle_a_segment` | `SEGMENT_LOOSE`, which the same case now reads — the messages are its values, unchanged |
| The hand-copied `swept` tuple in `test_folding_the_seam_cannot_hide_an_instance_it_would_have_found` | the same case, built from `SEAL_BARE`, `SEAL_BARE_IS_THE_CONCEPT` and `SEGMENT_LOOSE` |
