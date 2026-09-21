# 1789996775-the-gate-states-what-its-own-fixes-disproved — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 04946a4d, corrected at f7c9dd39 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#464's code half. `panel`'s first docstring paragraph replaced with what
`phases/phase-3.md` of work item 1789956662 records as true, and the elision's
grounds no longer assuming the dropped prefix is `origin/` (A3). Nothing
executes differently, so the check is that it does not.

## What this phase found

**The first replacement was written from the finding and not from the
reviewer's own text, and `survivor-check` is what caught it.** Round 2's
finding 13 carries a paste-ready replacement for exactly these two paragraphs
in its §*Paste-ready fixes*, and `spec.md` A3 — unlike A6 — does not name it,
so the first pass wrote its own. That version removed the sentence *the
elision keeps the TAIL: `origin/` is the part a reader can infer and the
branch name is not* outright, and `survivor-check` over the range then found
the same sentence standing in `test_a_ref_too_long_for_the_panel_says_it_was_cut`'s
docstring. The sentence is not wrong there — that case is about an `origin/`
ref — so the survivor was pointing at a removal that had been too wide.

Round 2's text is the better fix and is now what ships verbatim: it QUALIFIES
the claim rather than dropping it. *For the `origin/<base>` a runner reads,
the prefix is the part a reader can infer. Where step 1 lands on a second
remote the prefix is NOT inferable.* The test docstring carries the same
qualification.

**And round 2's paste-ready text contradicts round 2's own finding on one
point, so it is adopted with the gap stated beside it rather than adopted
whole.** The replacement ends *the line the gate prints is what names that ref
in full — it fires whenever the given and resolved commits differ*. Finding
13's own prose says the opposite about the case that matters: *Where a fork's
base and `origin`'s agree in commit, `moved` is false, nothing prints, and a
long `other/…` ref renders as its tail with the remote hidden.* Both sentences
are true and the first leaves a reader believing the printed line always
covers the cut. A third paragraph now states the gap as the cost of keeping
the tail, which is also what retires the argument A3 is about: where the line
does not fire, the row is the only statement a reader gets.

**The `panel` anchor drifted twice inside one phase**, so R5 of work item
1789956662 and G6 of work item 1789985781 were read by hand twice and each
carries both readings. `--reverify` re-stamped two rows the first time and two
the second, against a drift report naming one coordinate each time.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *a ref longer than that is cut here — which is why the line the gate prints when resolving MOVED the answer is the authoritative statement and this row is context* | nowhere; the reading is retired, and the paragraph that replaces it says why |
| the unqualified *`origin/` is the part a reader can infer* | round 2's qualified sentence, in `panel` and in the case's own docstring |
| the two survivors the removal opened, neither of them a defect | `survivors.md` rows with a quote and grounds (`seal/ledger.md` R5's Notes, and the case docstring's A4 clause) |
