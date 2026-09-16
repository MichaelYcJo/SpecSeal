# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — review round 1

| Field | Value |
|---|---|
| Target SHA | 27a2d403 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 425 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | batch_instructions (depth 1); test_the_sweep_refuses_a_planted_instruction_in_every_spelling (depth 1) |
| Needs a fix | yes — finding 1, the #422 sweep that matches nothing in the tree, so both halves of the repair revert green; and findings 2, 3, 4 and 5, each of which the smith may instead answer with grounds. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the run, against the whole branch — there is nothing earlier to
inherit. Spec compliance first, then quality.

All three subjects are checks that passed while blind to what they are named
for, and a repair for that class has one characteristic failure: being blind
itself, one layer down. This release has produced exactly that four times. So
the round was told its first job is **not** to confirm the ten mutations the
build already reported red, but to look for a fifth instance inside the
repairs — and to reach for the mutation the build did not run.

It was also asked to check five things the build reported rather than trust
them: the corrected folded-member count, the second stale width nobody had
reported, the four drifted ledger rows read before re-stamping, that phase 5
moved rendering and never prose, and the two phases that carry no mutation and
say why — because a phase excused from proof is the shape this work item is
about.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The #422 sweep matches nothing in the tree, so both halves of the repair can be reverted with the module green | `tests/test_chain_hooks_hardening.py:1000-1013` | **fixed** `930a6cbb` | fixed at 930a6cbb — the finding was confirmed before it was built to: zero batch-phrase occurrences across all five `agents/*.md`, and two of the round's five mutations reproduced at exit 0. The sweep is now `batch_instructions(body)` — emphasis strip, finder, window and stem set in one function — and a new case runs that same function over text it writes. All five mutations are exit 1 now, each on that case. The sweep CALLS the function, so there is one definition read twice and #418's Q3 grounds do not reach it; Executed: zero batch-phrase occurrences across all five `agents/*.md`; five separate mutations of the finder, the emphasis strip, the stem set and the window each leave the module at exit 0, 50 passed. The two new cases pin the constants, not the composition the sweep performs — the release's own rule is to pin what the production path calls. The planted-definition proof of phases 3 and 4 did not survive the commit |
| 🟡 2 | The finder strips `*` only, beside an existing repository normaliser that strips `*`, `_` and backticks; the marker these files use most is missed and unrecorded | `tests/test_chain_hooks_hardening.py:843`; compare `skills/code-review/scripts/chain_check.py:419` | **fixed** `930a6cbb` | fixed at 930a6cbb — the finder strips `` * _ ` `` like `chain_check.py`'s normaliser of the same name, and `BATCH_PHRASE` gains `into`. The round's argument won: stripping `_` cannot change what is found, so the whole cost is the printed window — and `*` alone left out the marker these files use most. Two constants named `EMPHASIS` meaning different things is also what the one-word-one-meaning sweep exists to stop; Executed: `` in `one batch` ``, `in _one batch_` and `into one batch` are all missed. Code spans outnumber asterisks in four of five definitions (warden 250/159, smith 202/142, sealer 98/68). Stripping `_` cannot change what is found — no stem and no phrase carries one — so the stated cost is the printed window only, which `chain_check.py` already pays. With `[*_`]+` the module is 50 passed at exit 0 |
| 🟡 3 | The back anchor dropped `asker`, `answerer` and `questioner`, and the new case pins that loss as correctness | `tests/test_chain_hooks_hardening.py:866` | **fixed** `930a6cbb` | fixed at 930a6cbb — `asker`, `answerer` and `questioner` moved out of the correctness block into their own, with a comment saying the back anchor cost them, that `agent-contract` §4 writes `answerer` for the party this guard looks for, and that reversing it is a widening needing its own argument. The stems are unchanged; Executed: all six agent-noun forms fire under the old front-anchored pattern and are silent now. The assertion's message calls them ordinary words *for a question nobody is asking*; an answerer is the word `agent-contract` §4 uses for the party this guard looks for. Not a request to widen the stem set — `spec.md` §*Out* refuses that with grounds — but the narrowing is asserted as right rather than recorded as residue |
| 🟡 4 | The work item's own ledger row carries a coordinate the checker cannot parse, and the checker reports it as nothing | `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6` | **fixed** `c9b10fe3` | fixed at c9b10fe3 — the row is anchored on three real locators: `#COVERED` and quoted-line anchors on the two docstring lines that state the numbers, so every number the row claims is held by the line that states it. Measured, where all three were silent before: `109→999` is exit 2 BROKEN, `90→999` is exit 2 DRIFTED, the restatement is exit 1 DRIFTED. The Notes say what a quoted-line anchor costs; Executed: `ANCHOR_RE` (`evidence_check.py:65`) accepts only a dotted symbol or a quoted line, `OLD_COORD_RE` does not catch the row either, and `#<module>@deadbeef` is equally `ok`. Corrupting the documented width the row claims leaves `bin/evidence-check .` at exit 0, 0 drifted. A11 passes over it while the claim is held by neither a case nor an anchor. `#COVERED` is a real unit whose comment carries one of the numbers |
| 🟡 5 | Phase 6's no-mutation row rests on a follow-up item about a different act, and a mutation was available | `plan.md:130`, `spec.md:126-128` | answered | `2da3d8eb` — the finding is right and it is located in records, so it closes as a correction. The true reason is written into `phases/phase-6.md` and `overview.md`, both naming this finding: a mutation was available and the round ran it, and the case is declined because the work item's scope is correcting the numbers, not because a follow-up row blocks it. `plan.md` and `spec.md` are left standing on purpose — they are the framer's documents and their prose is the design the gate approved, so a fix pass rewriting them would erase what was actually approved. That is a `survivors.md` row with the standing text quoted; Read: `seal/follow-up.md`'s open row holds whether two files join `COVERED`, which widens what the test guards. Pinning a docstring number against `prose_lines` and `display_width` guards nothing new. Executed: changing a documented width reddens nothing. Phase 5's row by contrast holds — cause removed by #414, and `tests/test_chain_check_at_the_pull_request.py` 114 passed at exit 0 |
| ⬜ | Four corrections that commission nothing: Q1's *four definitions* (five), A5's *four members* (five), the ordered-tuple brittleness of the folded-member assertion, and `agents/scribe.md` outside `SEAL_SWEPT` | `questions.md:35`, `spec.md:148`, `tests/test_one_word_one_meaning.py:482`, `tests/test_one_word_one_meaning.py:193` | correction | See §*Corrections*. Each is measured; none changes what the branch does |
| 🟢 | #413 holds — both of the issue's measured swaps are red, and the presence loop still fires first for a cell naming no shell | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:242-266` | confirmed | Executed: names exchanged in the refused row, exit 1; in the allowed row, exit 1; 18 passed untouched. Read: the presence loop at `:245` precedes both attribution assertions |
| 🟢 | #418 holds — both measured mutations are red, the five folded members and seven phrases are correct, and the recorded residue behaves as recorded | `tests/test_one_word_one_meaning.py:253`, `:388`, `:459-503` | confirmed | Executed: a seam-carrying phrase added to `SEGMENT_LOOSE`, exit 1; `chain_check.py` added to `SEAL_SWEPT`, exit 1 (2 failed); a phrase written inline in the case body, exit 0 — which is the residue the docstring records |
| 🟢 | Phase 5 repaired rendering only, and the records still parse | `seal/specs/1789445605-…/rounds/round-2.md:39-40` | confirmed | Read the full diff of both cells: `. ` removed after the em-dash, no other character changed. Executed: `tests/test_chain_check_at_the_pull_request.py` 114 passed, exit 0 |
| 🟢 | All four documented widths equal what the module's own helpers report | `tests/test_docs_line_wrap.py:20-24`, `:59` | confirmed | Executed with `prose_lines` and `display_width`: scribe 160, smith 109, writing-style 209, implement 90. The third restatement at `:59` is corrected; the fourth, in another work item's phase record, is correctly left as what was true when written |
| ❓ | The full suite, the repository-wide lint and the typecheck | the whole tree at this SHA | out of verified scope | `agent-contract` §2 assigns the broad gate to the sealer and `agents/warden.md` hands me none of the three. Not yet run. Answered by the sealer, spawned by the orchestrator after the rounds settle |

## Paste-ready fixes

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
```
`tests/test_docs_line_wrap.py#COVERED@b9362cc3`
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py` counts a coordinate that matches neither `ANCHOR_RE` nor `OLD_COORD_RE` as nothing rather than refusing it, which is the silence the comment under `ANCHOR_RE` names as unacceptable. Two rows in the tree sit in that hole today | a new issue — it is the checker rather than this branch, and `seal/ledger/1789518345-…` carries the other row | the repository owner |
| Whether `agents/scribe.md` joins `SEAL_SWEPT` | already open in `overview.md` §*Not verified* as the neighbouring question about `chain_check.py`, which is a change to what a test guards | the repository owner |
