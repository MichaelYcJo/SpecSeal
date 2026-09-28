# Round 1 report — 1790562542-the-verifying-round-is-bounded-not-cheapest

Target: `docs/639-the-verifying-round-is-bounded-not-cheapest` at `5a66666d`,
against `origin/release/v0.15.7` (`1fa25931`), draft PR #648. First round;
no earlier `round-N.md` exists, so nothing is carried. Reviewed in a
`git clone --no-local` under the session scratchpad
(`<scratchpad>/1790562542/round-1/clone`), which is removed at hand-over.

## How the two findings relate

```
#639 corrects a cost claim that was false for the verifying round
   ├─ C1–C6: corrected, pinned, and the pins go red (checked)
   ├─ the #81 correction the orchestrator added replaces one unsupported
   │  comparison with another from the same #89 comment      → 🟡 1
   └─ the class sweep stopped one paragraph early in agents/warden.md,
      whose previous bullet still grounds scoping on price    → 🟡 2
```

## Spec compliance

C1–C6 each landed as spec *In* 1–6 describe, and I read each against the
spec rather than against the hand-back:

- **C1**, `skills/code-review/orchestration.md:132`. Keeps "bounded", drops
  "cheapest", names the frame, the records and the probes, points at the
  chain spec, carries no figure and no bare `|`.
- **C2**, `docs/review-handoff-protocol.md:634`. `exempt` stays. The Grounds
  cell carries the target, the job and #51 observation 1, and no cost or size
  word. I read #51's first revision (2026-09-01T01:49Z, through
  `userContentEdits`): it holds "verifying ~1.5 (fewer independent axes to
  open)", so the new ground is #51's own.
- **C3**, `docs/review-chain-spec.md:216-224`. It carries the median, the
  count, the releases, the range, the five at or above round 1, the five
  source issues and #456's nine-for-nine. That was every item *In* 3 asks for.
- **C4**, `agents/warden.md:121-125`; **C5**, the docstring at
  `tests/test_the_last_rounds_fixes_are_checked.py:1089`; **C6**, the
  `WHAT_IT_TARGETS` needle. All three are as specified.
- The new module holds a gone/stands pair per carrier, a Grounds-cell case
  and the tree-wide case, matching *In* 6.

The #81 correction is a divergence from spec *Out*, S9 and plan A7, and
`overview.md` records it with its grounds (the orchestrator's instruction).
The divergence is recorded properly. What the correction now says is 🟡 1.

## 🟡 1 — The #81 correction swaps one unsupported comparison for another

**Where:** `skills/code-review/SKILL.md:230-233`, `templates/sdd-round.md:298-301`,
the module docstring and `CHEAPEST_81_CARRIERS` in
`tests/test_a_segments_record_says_what_it_was_asked.py` (lines 3-5, 8-12,
286-287).

**What is wrong.** The new text says #81's round 1 found "five defects in 29
tool calls, where #82's six rounds averaged three times the calls for fewer".
The phrase is quoted from #89's comment of 2026-09-03T02:26Z. The same #89
thread, in comments I read through `gh`, holds #82's rounds one by one:

| #82 round | calls | findings |
|---|---|---|
| 1 | 35 | 6 |
| 2 | 38 | 7 |
| 3 | 36 | 4 |
| 4 | 29 | 3 |
| 5 | not stated | 3 |
| 6 | 30 | 2 |

The five stated counts average 33.6 calls a round, which is 1.16 × 29 and
not 3 ×. For the six to average 87, round 5 alone would need about 354
calls. Per finding, #81 is 5.8 calls a defect. #82's five known rounds are
168 calls for 22 findings, 7.6 a finding, which is about 1.3 ×. "For fewer"
also fails for rounds 1 and 2, which found six and seven. No reading of #89's
own rows I could find gives three times.

**Why it matters.** This work item exists to make each sentence say only
what was measured. The correction takes out "the cheapest round on record"
and puts in a comparison whose source's own rows contradict it, in a skill
the orchestrator reads before every round and in a template every round
record is copied from. `test_81s_round_one_is_described_by_its_yield` now
requires that comparison to stand. I checked this by execution: deleting it
from the skill turned that case red. So the next person to correct it has to
fight a pin as well. `overview.md`'s *Not verified* row names this
comparison as read and not re-derived, which is accurate. It still went into
the tree as a measured fact.

**The fix.** State what was measured for #81 alone, which is five defects,
one 🔴 and four 🟡, in 7.6 minutes and 29 calls, and drop the #82
comparison. Then move the pins with the text. The paperwork copies are ⬜ 4.

## 🟡 2 — The class sweep stopped one paragraph short in `agents/warden.md`

**Where:** `agents/warden.md:110-112`.

**What is wrong.** The paragraph right above C4 reads: "Re-reading the whole
diff each time turns every returned finding into the price of a first round,
which is how a review loop costs more than the work it reviews." It says
that keeping a re-check round to its fix is what keeps it below a first
round's price. That is the class, a verifying round costing less because its
target is a diff, in other words. The measured basis this branch prints
contradicts it. #456 measured nine rounds, scoped or not, at 13.8–17.8
minutes and 46–58 calls, "whatever its target". The 29 rounds of
0.14.0–0.15.5 ran at a median of 0.83 × round 1, all of them scoped.
Scoped re-checks already cost about a first round.

Spec *Met and left alone* keeps it as "an upper bound no measurement
tested". I do not accept that ground. The sentence does not state a bound.
It names widening as the cause of a first round's price, and the measurement
shows that price arriving without any widening. The file now also disagrees
with itself: the next bullet (C4) says "The reason is the round's job, not
its price", one paragraph below a sentence whose reason is price.

**Why it matters.** A warden reads this paragraph before a verifying round,
and it tells the warden the opposite of C4 about why to stay scoped. The
tree-wide pin cannot catch it, because it does not use the phrase. The
module docstring says a carrier in other words is "a reviewer's catch".

**The fix.** Ground the scoping on the job, as C4 does, and add the
paragraph to the new module's carriers so it stays gone. The warden's §Role
rows in `seal/releases/0.15.0.md` (A11) and `seal/releases/0.15.1.md` (D1)
anchor the whole section. They will drift again and need re-reading once
more.

## ⬜ 3 — The chain spec leaves out the median's unit

`docs/review-chain-spec.md:220` says "a median of 0.83 × their own work
item's round 1". #639 and #51 both say "× their own round 1's span". Here
the ratio is of wall clock and not of calls or tokens, and the paragraph
names no unit. A reader who compares it with #456's call counts cannot tell.
The fact stands, so this is a note.

## ⬜ 4 — The paperwork carries 🟡 1's comparison too (correction)

- `seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/changelog.md:28`,
  which becomes released `CHANGELOG.md` text at the gather.
- `seal/ledger/1790562542-the-verifying-round-is-bounded-not-cheapest.md:4`,
  row V2's claim, and its minor anchor, which quotes the skill sentence
  🟡 1's fix rewrites.
- `phases/phase-1.md:56-58`, which calls the comparison something #89 "did
  measure and support".

These are paperwork under `seal/`, so they are reported as a correction and
are not counted in `Needs a fix`. They follow 🟡 1's wording once it lands.

## Class enumeration (§12)

I swept by meaning over `agents/`, `skills/` (scripts included), `docs/`,
`templates/`, both READMEs, `CONTRIBUTING.md`, `hooks/` and every test
docstring and needle. The terms were `cheap*`, `afford*`, `costs? less`,
`less expensive`, `price of`, `full walk`, `pays? for`, `costs? more`,
`as much as`, and every verifying-round line near a size or cost word.

Members found: C1–C5, the #81 carriers, and `agents/warden.md:110-112`
(🟡 2).

Met and left out, with grounds:

- `skills/code-review/scripts/round_record.py:3695`, "the reason the cost is
  affordable". This is the computational cost of one function over a fix
  range, not what a round spends.
- `docs/round-record-spec.md:603`, "prompt budget is zero". This is about who
  fills the rows, not what a round spends.
- `docs/review-handoff-protocol.md:14` and `skills/code-review/SKILL.md:235`,
  "round *n* costs *n* full walks". This is about coordinates lost without
  records, not about the target.
- Every "costs no round" line is cap arithmetic, the same as the spec's row.

`bin/survivor-check --range 1fa25931..5a66666d` exits 0. I ran it.

## The measured basis, opened

- **#639's figure.** I executed a count over the five issues' lead
  sentences, and it finds exactly 29 later-round warden readings: 6 in #496,
  5 in #535, 5 in #577, 9 in #601 and 4 in #619. A sample of the ratios from
  those lead sentences sits around 0.4–0.95 (for example #520 0.95 and 0.88,
  #518 0.69, #519 0.39, and in #535 item 0 0.72, item C 0.86, item A 0.86
  and 0.51). That is consistent with a 0.83 median. I did not re-derive the
  median, the range or the five-at-or-above count. Several rounds give calls
  and no minutes in the lead sentence, so their spans sit in the metered
  blocks, and those I did not read. This stays ❓ with #639's author.
- **#456.** I read it. It holds nine rounds, three per work item, at 13.8–17.8
  minutes and 46–58 calls, and the cause sentence is quoted exactly. The
  chain spec's use is faithful.
- **#89 and #51 for the "not the cheapest" half of the #81 correction.**
  I read both. #79's round 2 at 5.6 m and 28 calls was posted at
  2026-09-02T11:50Z. #79's round 3 at 4.6 m and 22 calls was posted at
  12:02Z. Both came before #81's round-1 comment at 2026-09-03T02:26Z and
  before the template sentence entered at `5107e30`. #51's first revision
  already carries #29's 4.2 m and 10 calls. That half of the correction is
  true. Only the replacement comparison is not (🟡 1).
- **#51, outside the tree.** #636's revision now holds "none of those shrink
  with the diff" and then, two paragraphs later, "**Surface size, not round
  kind**, and a diff is simply the smaller surface." The second sentence is
  the claim this branch retracts. It is not a file here, so it is under
  Deferred.

## The ledger re-stamps

I read all eleven re-stamped rows word by word against the edits: `seal/ledger.md`
(the handoff-before-round-1 row), 0.4.0, 0.5.0, 0.8.1 R9, 0.8.2 R4, 0.9.3
(two rows), 0.10.0, 0.11.4, 0.15.0 A11 and 0.15.1 D1. Each changes only its
hash and adds a dated re-read note. Each note describes the edit accurately.
No claim was made false. For example, 0.4.0's "a verifying segment exempt"
still holds, because the verdict cell is unchanged. I ran `evidence_check.py .`
in the clone and it exits 0. The two new rows V1 and V2 are the work item's
own. V2 carries 🟡 1's comparison (⬜ 4).

## Regression tests to plant

- `tests/test_a_segments_record_says_what_it_was_asked.py`: the #82
  comparison as a second gone half for both #81 carriers (in 🟡 1's fix).
- `tests/test_the_verifying_round_is_bounded_not_cheapest.py`: a fifth
  `CARRIERS` entry for `agents/warden.md`'s scoping paragraph (in 🟡 2's fix).
  Seen red: restoring the old sentence after the fix lands.

## Facts for the evidence ledger

- #639's "29 verifying rounds" count reproduces from the five issues' lead
  sentences (executed, this round). The median, range and the five at or
  above round 1 are not re-derived.
- #89's per-round #82 readings (35, 38, 36, 29, not stated, 30 calls; 6, 7,
  4, 3, 3, 2 findings) do not support "three times the calls" (read, this
  round).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The #81 correction states "#82's six rounds averaged three times the calls for fewer", and #89's own per-round readings for #82 (35, 38, 36, 29, ?, 30 calls) average about 1.2 × 29. The stands pin now requires the unsupported comparison | `skills/code-review/SKILL.md:231` | open | Read from #89's comments through `gh`. Deleting the comparison turned `test_81s_round_one_is_described_by_its_yield` red (executed). The same wording is at `templates/sdd-round.md:299` and in the module docstring |
| 🟡 2 | The paragraph above C4 still grounds keeping a re-check round scoped on price ("turns every returned finding into the price of a first round"), which #456 and #639's data contradict, and it disagrees with C4's "the round's job, not its price" | `agents/warden.md:111` | open | Read. It is outside the tree-wide pin because it does not use the phrase. The spec's "upper bound" ground does not hold, because the sentence names widening as the cause of a price that scoped rounds already pay |
| ⬜ 3 | The chain spec's median has no unit. The source says span | `docs/review-chain-spec.md:220` | open | Read #639 and #51. Both say "round 1's span" |
| ⬜ 4 | 🟡 1's comparison is also in the changelog fragment, in ledger row V2's claim and anchor, and in phase 1's record (correction) | `seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/changelog.md:28` | open | Paperwork under `seal/`, so not counted in `Needs a fix`. It follows 🟡 1's wording |
| 🟢 | C1–C6 match spec *In* 1–6, and the #81 divergence is recorded in `overview.md` with its grounds | `skills/code-review/orchestration.md:132` | confirmed | Read against spec.md. Executed: the four touched modules pass, and restoring the old protocol Grounds cell turned all four new cases red |
| 🟢 | The eleven re-stamped ledger rows left no claim false | `seal/releases/0.4.0.md:114` | confirmed | Read word by word against the edits. `evidence_check.py .` exits 0 (executed) |
| 🟢 | The "not the cheapest when written" half of the #81 correction is true | `tests/test_a_segments_record_says_what_it_was_asked.py:8` | confirmed | Read #89's timestamps (#79's round 2 at 5.6 m and 28 calls, and round 3 at 4.6 m and 22 calls, both before 2026-09-03T02:26Z) and #51's first revision (#29 at 4.2 m and 10 calls) |
| ❓ | Whether #639's median 0.83, its range 0.26–1.27 and the five at or above round 1 reproduce | `docs/review-chain-spec.md:219` | ❓ out of verified scope | Count of 29 reproduced (executed). The ratios need the metered blocks, which this round did not read. It is answered by a measurement from #639's author (questions.md Q1) |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_verifying_round_is_bounded_not_cheapest.py`, `tests/test_the_last_rounds_fixes_are_checked.py`, `tests/test_a_segments_record_says_what_it_was_asked.py` and `tests/test_the_handoff_before_round_one.py`, in the clone at `5a66666d` | exit 0, 105 passed |
| `evidence_check.py .` in the clone | exit 0 |
| `bin/survivor-check --range 1fa25931..5a66666d` in the clone | exit 0, "no removed wording is still standing" over 454 files and 20 removed sentences |
| Mutation: the protocol's old `verifying` Grounds cell restored, then the new module run | exit 1, 4 failed |
| Mutation: the #82 comparison deleted from `skills/code-review/SKILL.md`, then the #81 module run | exit 1, 1 failed, 10 passed. The stands pin requires the comparison |
| A regex count of later-round warden readings over the bodies and comments of #496, #535, #577, #601 and #619 | 29 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet run. It is the sealer's, after the rounds settle |

## Paste-ready fixes

### 🟡 1

`skills/code-review/SKILL.md`, the sentence at lines 229-233:

```
something still to verify. #81's round 1 is the
measured reason — five defects, one 🔴 and four 🟡, in 29 tool calls,
because its prompt named eight specific things to try to break, and that
fact today survives only in a transcript.
```

`templates/sdd-round.md`: keep the comment's opening marker on line 298 as
it is, and replace the rest of the sentence (lines 298-301) with:

```
#81: round 1 of that work item found five defects in 7.6 minutes and
29 tool calls — one 🔴 and four 🟡 — because its spawn prompt named eight
specific things to try to break, in order.
```

`tests/test_a_segments_record_says_what_it_was_asked.py`, the docstring's
first paragraph and the last sentence of its second:

```
"""Neither a round record nor a build phase said what it was ASKED to do,
only what it found. #81 is the measured cost on the review side: round 1 of
the work item it names found five defects in 7.6 minutes and 29 tool calls —
one 🔴 and four 🟡 — because its spawn prompt named eight specific things to
try to break, in order. That fact survives today only in a transcript.
```

```
calls, and #51's baseline #29's at 4.2 minutes and 10. What #89 measured for
it is five defects in 29 calls, so that is what the carriers say and what the
gone/stands pairs at the foot of this module hold (#639).
```

The same file, the carriers and the absent half:

```python
CHEAPEST_81_CARRIERS = (
    (
        REVIEW_SKILL,
        "five defects, one 🔴 and four 🟡, in 29 tool calls",
        ("the cheapest round on record", "averaged three times the calls"),
    ),
    (
        ROUND_TEMPLATE,
        "found five defects in 7.6 minutes and 29 tool calls",
        ("was the cheapest round measured", "averaged three times the calls"),
    ),
)
```

```python
def test_81s_round_one_is_not_called_the_cheapest_again():
    """The absent half, evidence only beside the present half above. #89
    held #79's verifying round at 5.6 minutes and 28 calls before it wrote
    7.6 and 29 up as the cheapest review round in the log, and its own
    readings of #82's rounds do not give three times the calls."""
    for path, _phrase, gones in CHEAPEST_81_CARRIERS:
        for gone in gones:
            assert gone not in flat(path), (
                f"{os.path.relpath(path, ROOT)} carries a retracted claim "
                f"about #81's round 1 again: {gone!r}"
            )
```

### 🟡 2

`agents/warden.md`, lines 110-114:

```
  A round that exists to check one fix is scoped to that fix. Re-reading the
  whole diff each time re-reviews what earlier rounds already reviewed instead
  of answering the finding that came back, and the answer is what the round
  is for. The exception is a fix that changes what an earlier verdict rested
  on — say so, and widen deliberately.
```

`tests/test_the_verifying_round_is_bounded_not_cheapest.py`, a fifth entry
at the end of `CARRIERS`:

```python
    (
        ("agents", "warden.md"),
        "instead of answering the finding that came back",
        ("turns every returned finding into the price of a first round",),
    ),
```

### ⬜ 3

`docs/review-chain-spec.md:219-220`:

```
those shrink with the diff. Measured over 0.14.0–0.15.5, 29 verifying rounds
ran at a median of 0.83 × the span of their own work item's round 1, with a
range of
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #51's body, as #636 revised it, says "Surface size, not round kind, and a diff is simply the smaller surface" two paragraphs after "none of those shrink with the diff". That is the retracted claim, and it is outside the tree | #51's body | the orchestrating session, which made #636's revision |

Needs a fix: yes — 🟡 1 (the #81 correction quotes an unsupported #82 comparison, and its pin requires it) and 🟡 2 (`agents/warden.md:110-112` still grounds scoping on price)
Loses a record or crashes: no

## Proof

Files opened this round, all at `5a66666d` in the clone unless noted:
the work item's `spec.md`, `overview.md`, `questions.md`, `changelog.md`
and `phases/phase-1.md` (lines 45-70); the full diff of `agents/warden.md`,
`docs/review-chain-spec.md`, `docs/review-handoff-protocol.md`,
`skills/code-review/SKILL.md`, `skills/code-review/orchestration.md`,
`templates/sdd-round.md`, and the three test modules;
`docs/review-chain-spec.md:180-230`; `docs/round-record-spec.md:590-615`;
`skills/code-review/scripts/round_record.py:3670-3720`;
`skills/implement/scripts/seal.py:1025-1090`; `agents/warden.md:110-125`;
`skills/code-review/SKILL.md:264-304`; the word-level diff of every changed
row in `seal/ledger.md`, `seal/releases/*.md` and the new ledger fragment.
Issues read through `gh`: #639, #456, #89, #51 (the body and every
`userContentEdits` revision), #81 (its title and date), #496, #535, #577,
#601 and #619. `plan.md`, `routing.md` and `phases/phase-2.md` were not
opened.
