# 1789296300-a-segments-own-wall-clock-is-in-no-column — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `47a1959` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and a value a segment sources from its own idea of what it is cannot be checked against anything |

## What this phase was asked

Build `plan.md`'s row 2 and nothing past it: the printed mode. `--segments`
prints one row per segment (agent · span · calls · t/turn · gap · tokens),
states the unnamed count, names the tolerance it joined within, prints the
transcripts-walked and spawns-found counts even when they agree, and refuses a
table when it found no segment. `segment` brought to one meaning where a spawn
cycle is currently called one.

Verified by output cases pinning each printed line, red first (contract §14),
and the word case in `tests/test_one_word_one_meaning.py` asserting the pinned
phrasing **and** the absence of the loose one.

## What this phase found

**The loose word had exactly three shipped homes, and the sweep is what
found the third.** `skills/verify/SKILL.md` and `session_cost.py`'s module
docstring were the two the frame implied; `tests/test_session_cost.py:1615`
carries the same sentence verbatim in a comment, and it is the file a reader
opens beside the module. Records — `CHANGELOG.md` and every `seal/specs/…`
directory — were left alone, which is the boundary the seal sweep already
draws in that module: a record of what was true when it was written is not
brought to a new wording.

**A truncated path is worse than no path, and the fixture caught it.** The
label column is 30 wide and the unnamed row's label is
`main/subagents/inner/agent-deep.jsonl`. Cut the way every other label in this
file is cut, it prints `main/subagents/inner/agent-dee` — the directories a
reader already knows, with the file name gone. It is cut from the left
instead, because a path is read from the right. The case that caught it was
asserting the file name is on the page, which is the thing a reader opens.

**Two literals that had to agree became one constant.** `segment_label` cuts
to the column width and `report_segments` pads to it, so `LABEL_WIDTH` is
named once — the day one of the two moves, the table goes ragged and nothing
says so.

**A column pinned only at zero could be printing anything.** The phase-1
fixture's segments spent no tokens, so the first version of the table case
asserted a `0` in the tokens column and would have passed against a column
that printed any constant. The fixture now spends 700 output + 300 cache write
in one segment and 40 cache read in the other, and the case pins `1,000` and
`40` — which also pins the column as the sum of the three fields its own
legend names.

**Executed against a real transcript, and the instrument agrees with the
bars it is read against.** A current SpecSeal run printed six rows: three
framers at 1.59–1.79 tools per turn and three smiths at 1.02–1.19.
`docs/review-handoff-protocol.md` §*After the run — the per-segment bars* puts
the reviewing bar at ≥ 1.8 and gives the implementing loop a measured
1.08–1.17. The mode reproduces that split from a single command, where today
it is one invocation per transcript by hand.

**How each case was seen red.** The eight output cases failed on
`unrecognized arguments: --segments`, exit 2. The two word cases failed on the
standing sentence, quoted back by the assertion.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The sentence *an orchestrator's segments are spawn cycles inside one file*, from `skills/verify/SKILL.md`, `session_cost.py`'s module docstring and `tests/test_session_cost.py`'s comment | The corrected rule in `skills/verify/SKILL.md` §*Measure the segment*, which states what a segment is and that a spawn cycle is not one; the other two are brought to it. `tests/test_one_word_one_meaning.py` holds both halves, so the removal cannot silently come back |
| Nothing else — no printed line, key or number that existed before this phase changed | none |
