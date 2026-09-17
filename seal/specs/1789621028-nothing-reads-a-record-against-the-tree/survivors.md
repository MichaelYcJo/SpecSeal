# 1789621028-nothing-reads-a-record-against-the-tree — survivor exemptions

## Round 1's fix pass — `b38bd920..HEAD`

`survivor-check` over this pass reports six places against 27 removed
sentences. **Two were corrected rather than exempted**, and they are the two
that mattered: the constant comment in
`skills/code-review/scripts/chain_check.py` carried the unmethoded corpus
count in shipped code, and `phases/phase-4.md` described a case whose claim
this pass narrowed. Four are exempt below, on two different grounds.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789621028-nothing-reads-a-record-against-the-tree/spec.md` | 39 fix-table files, 11 of which state a range in their first eight lines | **The framer's record of what it measured before the build.** A frame is not rewritten by the party that builds to it — the implementer's finding goes into the build's own records and the hand-back (`agents/smith.md` §1), and both happened: `phases/phase-3.md` carries the figure-by-figure comparison and `overview.md` §*Where spec and implementation diverged* carries the row. Nothing reads `spec.md` as the current state of the corpus, and the three documents a reader would act on — `docs/review-chain-spec.md`, the changelog fragment and `seal/ledger/1789621028-…md` — now all name the command and the tree state it was run at |
| `skills/code-review/scripts/round_record.py` | `raise Refused(f"git diff {a[:7]}..{b[:7]} failed in {root}")` | **A generic refusal idiom, not a copy of a corrected claim.** The shared phrases are `a b if` and `is none raise refused` at 1.68 — the shape *call git, refuse if it answered nothing*, which this repository writes the same way everywhere. What this pass changed is narrower: `close`'s count guard now checks `isdigit()` as well as `is None`, so every other instance of the idiom matched the sentence that changed. `touched` makes no claim about validating a count |
| `skills/code-review/scripts/survivor_check.py` | `b = resolves(root, right.strip() or "HEAD")` | **The same idiom, in this checker's own range parser.** Its subject is resolving a ref, not reading a number back from git, and nothing here asserts how a count is validated |
| `skills/code-review/scripts/survivor_check.py` | **The filter goes on `paths`, so it holds on both sides of the range.** | **The same idiom inside a docstring about filtering paths.** The match is the two generic phrases and nothing else; the sentence is about which files enter the comparison |
