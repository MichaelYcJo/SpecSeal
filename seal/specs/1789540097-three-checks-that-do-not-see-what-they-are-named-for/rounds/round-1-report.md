# Round 1 — three checks that do not see what they are named for

Target SHA `27a2d40347b90d780bb676d3810b19235dee09cd`, branch
`test/413-418-422-three-checks-that-do-not-see-what-they-are-named-for`, base
`release/v0.12.0`, pull request #425. The working tree was clean at the start
and the SHA did not move during the round. Everything below was read or run in
a `git clone --no-local` of the repository checked out at that SHA; the only
file written outside it is this report.

Round 1, so nothing is inherited.

## The relationship between the findings

Three repairs, and they do not share a verdict.

```
  #413  the two `&` cells        HOLDS   both measured swaps red
  #418  the phrase set made live  HOLDS   both measured mutations red

  #422  the stems and the finder  the PATTERNS are correct and
                                  NOTHING HOLDS THEM — the sweep they
                                  repair matches nothing in the tree, and
                                  five separate mutations of it are green
                                    ↓ and from the same cause
                                  the finder was written beside a
                                  normaliser this repository already had,
                                  narrower than it, and the gap was
                                  recorded as residue instead
                                    ↓ and the same shape once more
                                  the ledger row this work writes to
                                  record its own measurement carries an
                                  anchor the checker cannot parse, and the
                                  checker says nothing
```

The review was asked to reach for a fifth instance of the class this release
keeps producing. It is finding 1, and findings 2 and 4 are the same shape at
one remove.

## #413 and #418 hold, and I ran the mutations rather than reading the claim

Both issues' measured mutations are red at this SHA. The counts the build
reported are correct: five folded members, not four, and seven phrases in the
seam case's set. The four documented widths are what the module's own helpers
report today. Details are in `## Executed probes`.

One thing the prompt asked about specifically. The presence loop in
`test_both_ampersand_cells_name_both_shells` is still separable and still
fires first — it stands at `tests/test_the_broad_gate_row_is_asked_for_and_
runs_as_written.py:245` and the two attribution assertions at `:257` and
`:262`, so a cell naming no shell at all reaches the loop's message and never
reaches the attribution assertion. Hoisting `flat()` to `:242` did not break
that ordering.

## #422's repair is correct, and nothing in the committed tree holds it

**`tests/test_chain_hooks_hardening.py:1000-1013`** — the sweep body of
`test_the_questions_are_collected_before_the_work_not_during_it`.

The sweep finds **zero** batch-phrase occurrences across all five files in
`agents/*.md`. It found zero before this branch too. So the loop that composes
the finder, the emphasis strip, the window and the stem set never executes its
body, and every mutation of that composition leaves the module at exit 0:

| What was changed in the sweep, constants untouched | Module |
|---|---|
| the emphasis strip dropped | 50 passed, exit 0 |
| the finder back to the literal `in one batch` | 50 passed, exit 0 |
| the stem set back to front-anchored-only | 50 passed, exit 0 |
| the window widened to 400 | 50 passed, exit 0 |
| the window narrowed to 5 | 50 passed, exit 0 |

**Why this matters, and who it costs.** Both halves of #422 can be reverted
by an ordinary edit and the suite will not say so. The two new cases —
`test_the_asking_stems_are_anchored_at_both_ends` and
`test_the_batch_phrase_is_found_by_its_claim_not_by_one_spelling` — pin the
patterns in isolation, and the patterns are not what the guard is. The guard
is the composition, and that is the object the release's own rule names:
*pin the function the production path calls, never the helper beside it.*

The second of the two rules is broken in the same place. *Check that a case's
own assertion can fire before a fixture's guard does* — here there is no
fixture guard, there is simply nothing in the corpus to find, which is the
same silence arriving by a different road.

The build's proof does not survive the commit. Phase 3 and phase 4 were shown
red **with a definition planted in the tree**, which is the right way to see a
case red, but the planted definition was then removed. What ships is a check
that has never fired and cannot fire on anything committed.

The repository has already written this lesson down, four lines above the
constant finding 2 is about. `skills/code-review/scripts/chain_check.py:415`:

> a normalizer that read only the bare word matched NOTHING this repository
> ever wrote … Neither refusal that reads a verdict cell had ever fired on a
> real record.

`overview.md` §*Not done* records the analogous #418 gap (Q3) and does not
record this one. `## Not verified` does not carry it either.

The fix is a function the sweep calls and a case that calls the same function
with text it writes. That is not a derivation of anything — it re-implements
nothing, so `questions.md` Q3's grounds do not reach it. Verified: with the
paste-ready fix below, four of the five mutations above go red, and the fifth
(the stem set) goes red once the negative assertion in the same block is
added.

## The same repair narrowed a normaliser the repository already had

**`tests/test_chain_hooks_hardening.py:843`** — `EMPHASIS = re.compile(r"\*+")`.

`skills/code-review/scripts/chain_check.py:419` already holds
`EMPHASIS = re.compile(r"[*_`]+")`, under the same name, stripping all three
markdown markers. The new constant strips one of the three and the comment
beside it records `_` as residue. Backticks are recorded nowhere.

Measured, at this SHA, with the module's own constants:

| Spelling | Reaches the window? |
|---|---|
| `go in **one batch** before the first edit` | found |
| ``go in `one batch` before the first edit`` | **missed** |
| `questions go in _one batch_ before the edit` | **missed** |
| `collect them into one batch` | **missed** |

**Why the backtick is the wrong one to leave out.** Code spans outnumber
asterisks in four of the five definitions — `agents/warden.md` 250 to 159,
`agents/smith.md` 202 to 142, `agents/sealer.md` 98 to 68. The repair's own
subject is that an occurrence must be found by what it claims rather than by
one spelling, and the marker it skips is the one these files use most.

The comment's stated reason for leaving `_` out is that underscores are
load-bearing in the identifiers these definitions name. That cost is real but
it is confined to the window text a person reads in the refusal: neither
`BATCH_PHRASE` nor any stem in `ASKING` contains an underscore, so stripping
`_` cannot change what is found. `chain_check.py` pays exactly that cost
already.

Executed: with `EMPHASIS` widened to `[*_`]+`, the module is 50 passed at
exit 0 and all three markers are found.

`into one batch` is a separate hole in `BATCH_PHRASE` and is in the same fix.

## The back anchor also stopped the words that name the party who answers

**`tests/test_chain_hooks_hardening.py:866`** — the assertion that pins
`persona`, `personas`, `users`, `humanity` and `asker` as words the guard
must not fire on.

Anchoring the back of the bare stems was right, and `persona` and `users` are
the two the issue measured. But the same anchor silently dropped the agent
nouns, and the new case writes that loss down as correctness. Measured:

| Word | Front-anchored only (before) | Both ends (now) |
|---|---|---|
| `asker`, `askers` | fires | silent |
| `answerer`, `answerers` | fires | silent |
| `questioner`, `questioners` | fires | silent |

**Why this is not the same as `users`.** An asker is precisely the party
asking, and an answerer is precisely the party who answers — `agent-contract`
§4 uses that second word for exactly the party this guard is looking for. The
assertion's own message says the opposite:

> `{word}` fires the guard, so a definition using an ordinary word has to be
> reworded for a question nobody is asking

That message is true of `persona` and `humanity`. It is false of `asker`,
which is why pinning the five together turns a measured repair into a
judgment nobody made.

This does not have to be reopened as a widening — `spec.md` §*Out* rules
widening the stem set out with grounds, and I am not asking for that. What is
owed is that the loss is either taken back for the agent nouns or recorded as
residue beside the other three. Right now it is asserted as correct.

## The ledger row this work writes has an anchor the checker cannot read

**`seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-
for.md:6`** — `tests/test_docs_line_wrap.py#<module>@00000000`.

`ANCHOR_RE` at `skills/evidence-check/scripts/evidence_check.py:65` accepts a
locator that is either a dotted symbol name, `[A-Za-z_][A-Za-z0-9_.]*`, or a
quoted line. `<module>` is neither, so the coordinate does not parse as an
anchor at all — and `OLD_COORD_RE`, which exists to catch a coordinate the
first pattern misses and call it `old-format`, does not match it either. The
row falls through both nets in silence.

Measured, in the clone:

| Anchor in that row | `bin/evidence-check .` |
|---|---|
| `#<module>@00000000` as committed | exit 0 · 6 ok · 0 drifted · 0 broken · 0 old-format |
| `#<module>@deadbeef` | exit 0 · 6 ok · 0 drifted |
| `#COVERED@00000000` | exit 1 · DRIFTED, content changed at 49-99 |
| `#nosuchunit@00000000` | exit 2 · BROKEN, locator not found |

And with the documented width corrupted from 109 to 999 — the exact claim the
row makes — `bin/evidence-check .` is still exit 0 with 0 drifted.

**Why this matters here rather than anywhere.** A11 asks that no row be
BROKEN, and it passes. The row's own Notes say no case pins these numbers.
So the one measurement this work item took by hand is held by neither a test
nor a working anchor, inside the work item whose subject is a check blind to
what it is named for.

The comment directly under `ANCHOR_RE` names this outcome as the one it will
not accept: *the one unacceptable outcome is silence*.

`#COVERED` is a real unit and its own comment carries one of the two numbers,
so the row can be anchored without inventing anything. The checker's own
hole — an unparseable coordinate counted as nothing instead of refused — is
outside this branch's diff and is in `## Deferred`.

## Phase 6's excuse from proof cites a follow-up row about a different act

The two phases that carry no mutation are not equally grounded.

**Phase 5 is sound.** `plan.md:129` — the cause was removed by #414, that work
item's own cases hold it, and what this phase owes is that the corrected cells
still parse. I ran it: `tests/test_chain_check_at_the_pull_request.py`, 114
passed, exit 0, and its `_real_records` case reads the committed records. I
also read both cells: only `. ` is removed after the em-dash in each, and no
prose moved.

**Phase 6's reason does not hold as written.** `plan.md:130` excuses the phase
because *planting a reader is new mechanism aimed at the file
`seal/follow-up.md` already holds open for the owner*. That follow-up row holds
a different act — whether `agents/smith.md` and `agents/scribe.md` join
`COVERED`, which widens what the test guards. Pinning the docstring's numbers
against the module's own helpers guards nothing new; it asserts that a number
the module states about itself equals what the module measures.

A mutation was available and needs no new mechanism, and I ran it: change a
documented width and nothing in the repository goes red. That is the
demonstration, and the docstring now admits it in prose — *a number written by
hand goes stale silently, and two of these four had*.

This is fix-or-justify. If the answer is still no, the reason should be the
one that is true rather than the follow-up row.

## Corrections, which commission nothing

- `questions.md:35`, Q1's status cell: *no `in one batch` occurrence stands in
  any of the four definitions today*. There are five —
  `framer.md`, `scribe.md`, `sealer.md`, `smith.md`, `warden.md`. The
  measurement is right; the count beside it is not.
- `spec.md:148`, A5: *the comment names the `.py`-only fold and the four
  members*. The shipped comment names five, correctly.
  `overview.md:30` records the divergence for scope item 2 and for `plan.md`
  and lists three documents; A5 is a fourth statement of the same stale number
  and is not among them.
- `tests/test_one_word_one_meaning.py:482-497`: the folded-member assertion
  pins an ordered tuple, so a pure reorder of two `.py` entries in
  `SEAL_SWEPT` reddens the case (executed, exit 1) with the message *the set
  of members `flat` folds has moved* when it has not. Phase 1 deliberately
  avoided this brittleness for the `&` row and the same argument applies here.
- `agents/scribe.md` is the one definition absent from `SEAL_SWEPT`. Nothing
  is missed today — it holds zero occurrences of the swept phrase, measured —
  and it is pre-existing rather than this branch's. Noting it because the
  list's own comment records three earlier rounds of *the list closed where
  somebody had already looked*.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The #422 sweep matches nothing in the tree, so both halves of the repair can be reverted with the module green | `tests/test_chain_hooks_hardening.py:1000-1013` | open | Executed: zero batch-phrase occurrences across all five `agents/*.md`; five separate mutations of the finder, the emphasis strip, the stem set and the window each leave the module at exit 0, 50 passed. The two new cases pin the constants, not the composition the sweep performs — the release's own rule is to pin what the production path calls. The planted-definition proof of phases 3 and 4 did not survive the commit |
| 🟡 2 | The finder strips `*` only, beside an existing repository normaliser that strips `*`, `_` and backticks; the marker these files use most is missed and unrecorded | `tests/test_chain_hooks_hardening.py:843`; compare `skills/code-review/scripts/chain_check.py:419` | open | Executed: `` in `one batch` ``, `in _one batch_` and `into one batch` are all missed. Code spans outnumber asterisks in four of five definitions (warden 250/159, smith 202/142, sealer 98/68). Stripping `_` cannot change what is found — no stem and no phrase carries one — so the stated cost is the printed window only, which `chain_check.py` already pays. With `[*_`]+` the module is 50 passed at exit 0 |
| 🟡 3 | The back anchor dropped `asker`, `answerer` and `questioner`, and the new case pins that loss as correctness | `tests/test_chain_hooks_hardening.py:866` | open | Executed: all six agent-noun forms fire under the old front-anchored pattern and are silent now. The assertion's message calls them ordinary words *for a question nobody is asking*; an answerer is the word `agent-contract` §4 uses for the party this guard looks for. Not a request to widen the stem set — `spec.md` §*Out* refuses that with grounds — but the narrowing is asserted as right rather than recorded as residue |
| 🟡 4 | The work item's own ledger row carries a coordinate the checker cannot parse, and the checker reports it as nothing | `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6` | open | Executed: `ANCHOR_RE` (`evidence_check.py:65`) accepts only a dotted symbol or a quoted line, `OLD_COORD_RE` does not catch the row either, and `#<module>@deadbeef` is equally `ok`. Corrupting the documented width the row claims leaves `bin/evidence-check .` at exit 0, 0 drifted. A11 passes over it while the claim is held by neither a case nor an anchor. `#COVERED` is a real unit whose comment carries one of the numbers |
| 🟡 5 | Phase 6's no-mutation row rests on a follow-up item about a different act, and a mutation was available | `plan.md:130`, `spec.md:126-128` | open | Read: `seal/follow-up.md`'s open row holds whether two files join `COVERED`, which widens what the test guards. Pinning a docstring number against `prose_lines` and `display_width` guards nothing new. Executed: changing a documented width reddens nothing. Phase 5's row by contrast holds — cause removed by #414, and `tests/test_chain_check_at_the_pull_request.py` 114 passed at exit 0 |
| ⬜ | Four corrections that commission nothing: Q1's *four definitions* (five), A5's *four members* (five), the ordered-tuple brittleness of the folded-member assertion, and `agents/scribe.md` outside `SEAL_SWEPT` | `questions.md:35`, `spec.md:148`, `tests/test_one_word_one_meaning.py:482`, `tests/test_one_word_one_meaning.py:193` | correction | See §*Corrections*. Each is measured; none changes what the branch does |
| 🟢 | #413 holds — both of the issue's measured swaps are red, and the presence loop still fires first for a cell naming no shell | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:242-266` | confirmed | Executed: names exchanged in the refused row, exit 1; in the allowed row, exit 1; 18 passed untouched. Read: the presence loop at `:245` precedes both attribution assertions |
| 🟢 | #418 holds — both measured mutations are red, the five folded members and seven phrases are correct, and the recorded residue behaves as recorded | `tests/test_one_word_one_meaning.py:253`, `:388`, `:459-503` | confirmed | Executed: a seam-carrying phrase added to `SEGMENT_LOOSE`, exit 1; `chain_check.py` added to `SEAL_SWEPT`, exit 1 (2 failed); a phrase written inline in the case body, exit 0 — which is the residue the docstring records |
| 🟢 | Phase 5 repaired rendering only, and the records still parse | `seal/specs/1789445605-…/rounds/round-2.md:39-40` | confirmed | Read the full diff of both cells: `. ` removed after the em-dash, no other character changed. Executed: `tests/test_chain_check_at_the_pull_request.py` 114 passed, exit 0 |
| 🟢 | All four documented widths equal what the module's own helpers report | `tests/test_docs_line_wrap.py:20-24`, `:59` | confirmed | Executed with `prose_lines` and `display_width`: scribe 160, smith 109, writing-style 209, implement 90. The third restatement at `:59` is corrected; the fourth, in another work item's phase record, is correctly left as what was true when written |
| ❓ | The full suite, the repository-wide lint and the typecheck | the whole tree at this SHA | out of verified scope | `agent-contract` §2 assigns the broad gate to the sealer and `agents/warden.md` hands me none of the three. Not yet run. Answered by the sealer, spawned by the orchestrator after the rounds settle |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_chain_hooks_hardening.py -q` at the target SHA | exit 0 · 50 passed |
| `bin/test tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py -q` | exit 0 · 18 passed |
| `bin/test tests/test_one_word_one_meaning.py -q` | exit 0 · 18 passed |
| `bin/test tests/test_docs_line_wrap.py -q` | exit 0 · 23 passed |
| `bin/test tests/test_chain_check_at_the_pull_request.py -q` (phase 5's own command) | exit 0 · 114 passed |
| `bin/evidence-check .` | exit 0 · 1321 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| #413 mutation 1 — `/bin/sh` and `cmd.exe` exchanged in the refused `&` row of `templates/config.md:206` | exit 1 · 1 failed, 17 passed |
| #413 mutation 2 — the same exchange in the allowed row at `:225` | exit 1 · 1 failed, 17 passed |
| #418 mutation 1 — a seam-carrying phrase added to `SEGMENT_LOOSE` | exit 1 · 1 failed, 17 passed |
| #418 mutation 2 — `hooks/chain_check.py` added to `SEAL_SWEPT` | exit 1 · 2 failed, 16 passed |
| #418 residue — a phrase written inline in the sweep case body instead of the constant | exit 0 · 18 passed, as the docstring records |
| #418 brittleness — two `.py` members swapped in position in `SEAL_SWEPT`, no membership change | exit 1 · 1 failed, 17 passed |
| #422 mutation A — the emphasis strip removed from the sweep, `EMPHASIS` untouched | exit 0 · 50 passed |
| #422 mutation B — the sweep's finder back to the literal `in one batch`, `BATCH_PHRASE` untouched | exit 0 · 50 passed |
| #422 mutation C — the sweep's stems back to front-anchored-only, `ASKING` untouched | exit 0 · 50 passed |
| #422 mutation D — the sweep's window widened to 400, `ASKING_WINDOW` untouched | exit 0 · 50 passed |
| #422 mutation E — the sweep's window narrowed to 5 | exit 0 · 50 passed |
| Corpus measurement — batch-phrase occurrences across `agents/*.md` | 0 in all five definitions, before and after the repair |
| Spellings put through `EMPHASIS` then `BATCH_PHRASE` | found: `**one batch**`, `in a batch`, `as a batch`, `in one batch`; missed: `` `one batch` ``, `_one batch_`, `into one batch`, `in one single batch` |
| `ASKING` over the agent nouns | `asker`, `askers`, `answerer`, `answerers`, `questioner`, `questioners` all silent; each fires under the previous front-anchored pattern |
| `EMPHASIS` widened to `[*_`]+` | exit 0 · 50 passed, and all three markers found |
| The proposed fix for finding 1, under the five #422 mutations | 4 of 5 red; the fifth red once the negative assertion in the same block is added |
| Markdown-marker counts in `agents/*.md` | warden 250 backticks / 159 asterisks · smith 202/142 · framer 146/147 · sealer 98/68 · scribe 8/16 |
| Widths re-derived with `prose_lines` and `display_width` | scribe 160 · smith 109 · writing-style 209 · implement 90 · sealer 79 · framer 78 · warden 86 |
| Folded members derived from `SEAL_SWEPT` and `SEGMENT_SWEPT` | five, in the order the case pins them |
| `bin/evidence-check .` with the ledger row's anchor varied | `#<module>@00000000` ok · `#<module>@deadbeef` ok · `#COVERED@00000000` DRIFTED · `#nosuchunit@00000000` BROKEN |
| `bin/evidence-check .` with the documented width corrupted to 999 | exit 0 · 0 drifted · 0 broken — the row's own claim goes unremarked |
| The full suite, the repository-wide lint, the typecheck | not yet — the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py` counts a coordinate that matches neither `ANCHOR_RE` nor `OLD_COORD_RE` as nothing rather than refusing it, which is the silence the comment under `ANCHOR_RE` names as unacceptable. Two rows in the tree sit in that hole today | a new issue — it is the checker rather than this branch, and `seal/ledger/1789518345-…` carries the other row | the repository owner |
| Whether `agents/scribe.md` joins `SEAL_SWEPT` | already open in `overview.md` §*Not verified* as the neighbouring question about `chain_check.py`, which is a change to what a test guards | the repository owner |

## Paste-ready fixes

**Finding 1** — `tests/test_chain_hooks_hardening.py`. Insert the helper and
the case immediately above `def test_the_questions_are_collected_before_the_
work_not_during_it():` at `:913`. Both names it introduces are proposed:
`batch_instructions` — NAME NOT IN TREE
`test_the_sweep_refuses_a_planted_instruction_in_every_spelling` — NAME NOT IN TREE

```python
def batch_instructions(body):
    """Every batching instruction in `body` whose window names a person
    answering, as (phrase, window, names).

    The sweep below IS this function over `agents/*.md`, and the case beside
    it is this function over text the case writes. Nothing in the tree
    contains a batch phrase — measured, zero occurrences in all five
    definitions — so before this function existed every mutation of the
    finder, the emphasis strip, the window and the stem set left the module
    green while the two pattern cases went on passing. That is the defect this
    whole work item is about, one layer down: the cases pinned the pieces and
    the production path was a copy of them
    (`seal/specs/1789455558-…/overview.md` — pin the function the production
    path calls).
    """
    flat_body = EMPHASIS.sub("", " ".join(body.split()))
    for hit in BATCH_PHRASE.finditer(flat_body):
        at = hit.start()
        window = flat_body[max(0, at - ASKING_WINDOW) : at + ASKING_WINDOW]
        named = sorted({m.group(0).lower() for m in ASKING.finditer(window)})
        if named:
            yield hit.group(0), window, named


def test_the_sweep_refuses_a_planted_instruction_in_every_spelling():
    """The whole guard, run on text this case writes, because the corpus
    holds nothing for it to find.

    Red with the emphasis strip removed from `batch_instructions`, red with
    the finder back to the literal `in one batch`, red with the window at 5
    or at 400, and red with the stems front-anchored only — the last on the
    negative at the end, which is the direction a wider stem set is wrong in.
    """
    for spelling in (
        "questions go in **one batch** before the first edit and the person "
        "answers them",
        "collect in a single batch everything a person has to answer",
        "collect as a single batch everything the user answers",
        "collect in one batch what a person answers",
    ):
        assert list(batch_instructions(spelling)), (
            f"the guard does not refuse {spelling!r}, so an instruction "
            "written that way reaches no window that would refuse it"
        )
    # The window bounds the distance. Prose that names a person two hundred
    # characters from a batch phrase is not this instruction.
    far = "collect them in one batch." + " filler" * 40 + " a person answers"
    assert not list(batch_instructions(far)), (
        "the window no longer bounds the distance, so ordinary prose far "
        "from a batch phrase is refused"
    )
    # `agent-contract` §10's own legitimate wording, with the two words the
    # back anchor exists to stop one clause away.
    assert not list(
        batch_instructions(
            "open every coordinate a task names in one batch; the persona "
            "the smith writes for and the users who install this plugin are "
            "not parties to it"
        )
    ), "batching READS is refused, which is the false refusal round 2 bought off"
```

And the sweep at `:998-1013` becomes a caller of it:

```python
    for path in definitions:
        with open(path, encoding="utf-8") as f:
            body = f.read()
        relative = os.path.relpath(path, ROOT)
        for phrase, window, named in batch_instructions(body):
            raise AssertionError(
                f"{relative} tells an agent to collect {phrase} something a "
                f"person answers — the window names {named}. No agent this "
                "plugin spawns has `AskUserQuestion`, so collecting a batch "
                "of questions is an instruction nothing can carry out; the "
                "act belongs to the session that spawns the work. Batching "
                "READS is a different thing and is what `agent-contract` §10 "
                f"asks for — that wording is not refused here.\n  …{window}…"
            )
```

**Finding 2** — `tests/test_chain_hooks_hardening.py:837` and `:843`.

```python
BATCH_PHRASE = re.compile(
    r"\b(?:in|into|as) (?:one|a single|a) batch\b", re.IGNORECASE
)
# All three markdown markers, which is what `chain_check.py:419` already
# settled on under this same name. `*` alone left the commonest one out:
# code spans outnumber asterisks in four of the five definitions
# (`agents/warden.md` 250 to 159, `agents/smith.md` 202 to 142), so
# `in `one batch`` reached no window at all.
#
# Stripping `_` costs the window a person reads in the refusal — a file name
# prints without its underscores — and cannot change WHAT IS FOUND, because
# no stem in `ASKING` and no word in `BATCH_PHRASE` carries one. That is the
# same trade `chain_check.py` makes, for the same reason.
EMPHASIS = re.compile(r"[*_`]+")
```

**Finding 3** — `tests/test_chain_hooks_hardening.py:864-871`. Split the
assertion so the two groups stop being one claim.

```python
    # The back anchor, on the words the issue measured: a population, or a
    # word that merely contains a stem.
    for word in ("persona", "personas", "users", "humans", "humanity"):
        assert not ASKING.search(word), (
            f"{word} fires the guard, so a definition using an ordinary word "
            "has to be reworded for a question nobody is asking"
        )
    # WHAT THE BACK ANCHOR ALSO COST, pinned so the next reader meets it
    # rather than discovering it: the agent nouns stopped matching, and each
    # of them names the party this guard is looking for. `agent-contract` §4
    # writes `answerer` for exactly that party. Widening the stem set is
    # refused with grounds in `seal/specs/1789540097-…/spec.md` §*Out*, so
    # this is residue and not a defect — but it is residue, not correctness,
    # and the assertion above used to say otherwise.
    for word in ("asker", "answerer", "questioner"):
        assert not ASKING.search(word), (
            f"{word} is an agent noun the back anchor stops. If this line is "
            "ever reversed, it is a widening of what the guard refuses and "
            "needs the argument `spec.md` §*Out* asks for"
        )
```

**Finding 4** — `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6`, the Code grounds cell only.

```
`tests/test_docs_line_wrap.py#COVERED@b9362cc3`
```

Re-stamp with `bin/evidence-check . --reverify` rather than copying that hash
by hand. `COVERED` is the unit whose own comment carries the `109 and 160`
restatement, so the anchor moves with the claim; `#<module>` parses as no
anchor at all and the checker counts it as nothing. If the docstring genuinely
has no anchorable unit, the honest home is a row in
`seal/specs/1789540097-…/evidence-todo.md` with an answerer, not a coordinate
the checker cannot read.

**Finding 5** — `plan.md:130`, the Verified-by cell's last sentence.

```
**No mutation, and the reason is not that none exists.** Changing a documented
number reddens nothing in the repository — that is the measurement, and it is
what the docstring now states in prose. What stands in its place is
re-derivation from the module's own `prose_lines` and `display_width`, run in
this phase. Pinning the four numbers against those helpers guards nothing new
and is NOT the covered-list widening `seal/follow-up.md` holds open for the
owner; it is declined here only because `spec.md` §*Out* scopes this work item
to correcting the numbers, and it is recorded in `## Not verified` with the
owner named.
```

Needs a fix: yes — finding 1, the #422 sweep that matches nothing in the tree, so both halves of the repair revert green; and findings 2, 3, 4 and 5, each of which the smith may instead answer with grounds.

Loses a record or crashes: no

## Proof block

Files opened in this round, all at `27a2d403`:

- `tests/test_chain_hooks_hardening.py`, `tests/test_one_word_one_meaning.py`,
  `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
  `tests/test_docs_line_wrap.py`
- `templates/config.md` (the two `&` rows), `skills/code-review/scripts/chain_check.py`
  (the `EMPHASIS` constant and its comment),
  `skills/evidence-check/scripts/evidence_check.py` (`ANCHOR_RE`, `OLD_COORD_RE`,
  the resolver's docstrings), `bin/test`, `bin/evidence-check`
- `seal/specs/1789540097-…/spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `routing.md`, `changelog.md`
- `seal/ledger/1789540097-….md`, the diff of `seal/ledger/1789518345-….md`,
  the diff of `seal/ledger.md`
- `seal/specs/1789445605-…/rounds/round-2.md` (the two repaired cells)
- `CLAUDE.md` (repository), `~/.claude/CLAUDE.md`,
  `~/.claude/skills/writing-style/SKILL.md`

Read but not opened in full: `seal/specs/1789540097-…/phases/phase-1.md`
through `phase-6.md` were read only for their commit rows and phase 2's
folded-member sentence.

Claims in this report are labelled: every row of `## Executed probes` was run
in this round and its exit code read directly; everything under `Read:` was
read and not run. The broad gate was not run and is the sealer's.
