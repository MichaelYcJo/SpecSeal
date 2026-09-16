# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | ef2bebb3 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#422 half two. Markdown emphasis normalised out before the search, and the
preposition and article read as a small set rather than as one literal, so
`in **one batch**`, `in a single batch` and `as a single batch` all reach the
window that judges them. The residue goes beside the case — what the window
still cannot tell apart, and that it crosses headings. Each of the three
spellings the issue measured passing at exit 0 has to go red, and the module
has to stay green over `agents/*.md` untouched.

## What this phase found

**All three spellings reproduced, in both directions, in one run.** Each was
planted beside a person answering in `agents/smith.md`, and the module was
run twice per plant — once with the finder as phase 3 left it, once with this
phase's:

| Planted spelling | Finder as of `7d1bf5bf` | After this phase |
|---|---|---|
| *Questions a person genuinely has to answer go in `**`one batch`**` before the first edit* — `CLAUDE.md:39` verbatim | exit 0 | exit 1 |
| *Collect what a person has to answer in a single batch.* | exit 0 | exit 1 |
| *Collect what a person has to answer as a single batch.* | exit 0 | exit 1 |

The first column is `agent-contract` §5 being taken at its word: the issue's
claim was opened rather than built on.

**The emphasis strip reads `*` and not `_`, and that is a judgment the ticket
does not make.** Both are markdown emphasis, and both would have to come out
for the normalisation to be complete. `_` is load-bearing in every identifier
these definitions name — `round_record.py`, `test_the_…` — so stripping it
would mangle the window the refusal prints for a person to read. An
instruction hidden behind `_one batch_` therefore still passes; it is written
into the residue rather than left to be found, which is the shape round 2 of
#419 already used.

**The refusal message now quotes the spelling it found.** It used to say
*collect in one batch* whatever the document wrote, because the literal it
searched for was the only spelling it could name. It says `found.group(0)`
now, so a person meeting the refusal reads their own words back.

**A12 holds and was checked rather than assumed.** The module is green over
`agents/*.md` as they stand, with no edit to any definition: 50 passed, exit
0. Nothing in the tree had to be reworded for either half of #422.

**`WINDOW` is gone as a local name.** The sweep reads `ASKING_WINDOW`
directly, so there is one name for the span rather than a local aliasing a
module constant — which is the same one-definition-read-twice shape phase 2
applied to the phrase sets.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The literal finder `flat_body.find("in one batch")` and its `while` loop | `BATCH_PHRASE.finditer` over the emphasis-normalised body, pinned by `test_the_batch_phrase_is_found_by_its_claim_not_by_one_spelling` |
| The local `WINDOW = ASKING_WINDOW` alias | the sweep reads `ASKING_WINDOW` itself |
| The refusal's hard-coded phrase *collect in one batch* | the message quotes `found.group(0)`, the spelling actually found |
