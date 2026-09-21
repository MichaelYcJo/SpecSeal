# 1789621028-nothing-reads-a-record-against-the-tree — survivor exemptions

## Round 1's fix pass — `b38bd920..bf693bc1`

`survivor-check` over this pass first reported six places. **One was
corrected rather than exempted**, and it is the one that mattered: the
constant comment in `skills/code-review/scripts/chain_check.py` carried the
unmethoded corpus count in shipped code, where a reader would act on it.

The five rows below are exempt, on three grounds. Re-run with this file as
`--exempt`, the range is **exit 0** and **one** row is used — the other four
name wording later commits in the same range took out on their own, which is
what an exemption anchored on a quote does when the quote stops standing.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789621028-nothing-reads-a-record-against-the-tree/spec.md` | 39 fix-table files, 11 of which state a range in their first eight lines | **The framer's record of what it measured before the build.** A frame is not rewritten by the party that builds to it — the implementer's finding goes into the build's own records and the hand-back (`agents/smith.md` §1), and both happened: `phases/phase-3.md` carries the figure-by-figure comparison and `overview.md` §*Where spec and implementation diverged* carries the row. Nothing reads `spec.md` as the current state of the corpus, and the three documents a reader would act on — `docs/review-chain-spec.md`, the changelog fragment and `seal/ledger/1789621028-…md` — now all name the command and the tree state it was run at |
| `seal/specs/1789621028-nothing-reads-a-record-against-the-tree/phases/phase-4.md` | one produces a notice and no error | **A record of a moment, corrected the way this repository corrects one.** The claim held at the commit that phase closed, and stopped holding when this work item's own `round-1.md` became the first record to carry the row. A phase record is not rewritten — an HTML comment beside the sentence says what changed, when, and where the corrected claim lives (`seal/ledger/1789621028-…md` R6), which is the convention `rounds/round-1.md` of 1789034970-… already uses for a hand-repaired cell and which phase 5 of this work item applied four times. The live claim is R6's and the case's own assertions; this line is history with its correction attached |
| `skills/code-review/scripts/round_record.py` | `raise Refused(f"git diff {a[:7]}..{b[:7]} failed in {root}")` | **A generic refusal idiom, not a copy of a corrected claim.** The shared phrases are `a b if` and `is none raise refused` at 1.68 — the shape *call git, refuse if it answered nothing*, which this repository writes the same way everywhere. What this pass changed is narrower: `close`'s count guard now checks `isdigit()` as well as `is None`, so every other instance of the idiom matched the sentence that changed. `touched` makes no claim about validating a count |
| `skills/code-review/scripts/survivor_check.py` | `b = resolves(root, right.strip() or "HEAD")` | **The same idiom, in this checker's own range parser.** Its subject is resolving a ref, not reading a number back from git, and nothing here asserts how a count is validated |
| `skills/code-review/scripts/survivor_check.py` | **The filter goes on `paths`, so it holds on both sides of the range.** | **The same idiom inside a docstring about filtering paths.** The match is the two generic phrases and nothing else; the sentence is about which files enter the comparison |
