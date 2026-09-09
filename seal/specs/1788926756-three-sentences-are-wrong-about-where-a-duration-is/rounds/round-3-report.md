# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — review round 3

The round that ends a run whose every finding was in a sentence. It was asked
three things: whether the pin now exists, whether the corrected diagnosis is
the measured one, and whether anything still on the page says something false
about where a duration is or what a check did.

All three of round 2's departures from the report were right, and each is
verified below by execution rather than by reading its account. What this
round opened is one thing in the tool and two corrections, and they share a
cause worth stating before the findings.

**Three sweeps ran on this branch for the same class and each one's pattern
could not match the next instance.** Round 1 swept `N passed` and corrected
68 → 69. Round 2 swept the same clause and corrected 105 → 97. Round 2's fix
pass swept `N passed`, `N cases` and `N assertions` by construction. The
figure two positions to the right of the one it just corrected reads `N ok`,
so no sweep could see it (finding 19) — and the class's other shape is a
*total against its own enumeration*, which no `N <word>` pattern reaches at
all (finding 18). The instance that survived three sweeps is the one the run
wrote itself, in the fix for the finding about that very clause.

The third finding is the same shape one layer up: the case round 2 planted to
stop a sentence regressing passes against the regression its own docstring
names.

## 18 ⬜ *Three printed figures* against an enumeration of five, in the same sentence

`spec.md:76` bolds the claim and then contradicts it in the same table cell:

> **No PRINTED figure in THIS PROJECT's transcripts moves under `max(end)`,
> and three move elsewhere on the machine** — … 2 row spans move a printed
> figure (368.5m → 368.7m, 195.7m → 195.8m); the between-the-rows figure
> moves on 3 transcripts (6.7m → 6.6m, 24.4m → 24.2m, 3.3m → 3.2m).

Five printed figures are named with their before-and-after values, and the
total in front of them is three. `questions.md:11` states it more plainly
still — *Machine-wide three printed figures do move — 2 row spans and 3
between-the-rows figures* — which is 2 + 3 in the same clause as the word
*three*. The number three is the between-the-rows count read as the total.

Four live carriers, and the reason this one is worth the closing commit is
which they are:

- `seal/specs/1788926756-…/spec.md:76` — the acceptance fact row
- `seal/specs/1788926756-…/questions.md:11` — Q1's answer
- `seal/ledger/1788926756-…​.md` row 4 — the **Claim** column, whose own
  Verified cell beside it enumerates the 2 and the 3
- `seal/specs/1788926756-…/changelog.md:13-14` — the release note

**The fourth is why it should not be left *corrected in passing or not at
all*.** `CLAUDE.md` §*a change writes fragments* has `gather_changelog.py`
concatenate that fragment verbatim into the released section, and this work
item's own `survivors.md` argues #307 on the grounds that a released entry may
not be edited afterwards — *editing it to match a later change makes the
history lie about what shipped*. So the window for this correction closes at
the release, and after it the repository's own convention forbids the fix.
The ledger row is the same shape one file over: at the fold it moves into
`seal/ledger.md` with a Claim that contradicts its Verified cell.

Round 1's finding 3 named these exact four carriers, its fix pass rewrote all
four, and the flat total is what the rewrite introduced. Round 2 recorded
*closed on all four* and read the number rather than adding it up. That
verdict was mine, and this is its correction.

Every `Location` here is under `seal/specs/` or `seal/ledger/`, so
`docs/review-chain-spec.md` §*The last round verifies* makes it a correction
and keeps it out of `Needs a fix`. Editing the Claim text does not move the
row's anchor — the coordinate is
`skills/verify/scripts/session_cost.py#analyse@c8423846` and the
hash is over the code — so `bin/evidence-check` stays at 1041 ok · 0 drifted
across the edit.

Two paperwork carriers quote the corrected text as round 1's answer:
`rounds/round-1.md:77` and `:80`.

## 19 ⬜ The proof line's third figure is the base's, and the right one is one file over

`overview.md:20` reads `evidence-check` (1033 ok · 0 drifted, exit 0) inside a
clause labelled **executed**. Executed in a clone: **1041 ok** at `bcaba67`,
at `b411e77`, and at `80cc7ce` — the commit that wrote that line. 1033 is the
number at `7ca5008`, the branch's spec commit, before this work item added its
five ledger rows and re-stamped fourteen. The figure was already stale when it
was written.

`phases/phase-3.md:40` carries the honest number: *`evidence-check` reads
1041 ok · 0 drifted · 0 broken, exit 0*. So the correct value is already in
the work item, in the record written by the pass that made the rows.

This is the third figure in one parenthetical run. Round 1 corrected the
first, round 2 the second, and both sweeps ran a pattern that reads `passed`.

## 20 🟡 The case planted for finding 12 passes against the regression it names

Its docstring states the job: *without this case an edit can put the rarer
cause back as the ordinary one and no check says anything.* Executed, one
mutation at a time in a clone, each restored and sha256-compared after:

| The edit | The case |
|---|---|
| the two causes swapped — *A background command is the ordinary way in and batching is the rarer one* | **exit 0, not caught** |
| the measurement inverted — *came from a call that crossed a turn and none of it from calls batched into one message* | **exit 0, not caught** |
| *Something running in the background is the usual cause.* added sentence-initially | **exit 0, not caught** |
| *never as something running in the background* — the old wording restored lowercase mid-sentence | exit 1, caught |

The four assertions test for the presence of four literal strings, and all
four survive a reordering of the sentences that carry them. So the case pins
the paragraph's vocabulary and not the claim: it passes against the exact
inverse of the measurement, and against the promotion of the rarer cause that
round 1's finding 1 was about. The one arm that fires is the one the fix pass
ran — its four red arms each deleted or reworded a phrase, which measures the
assertion's literal string rather than the claim above it. §15 was satisfied
and the pin is still weaker than the account.

The negative assertion is also case-sensitive, so the same wording returning
at the start of a sentence passes.

The paste-ready fix below pins the ranking clause and the measurement clause
whole, and lowercases the negative. Executed against all five arms: green as
shipped, red on every one, including the three the shipped case misses.

## 21 ⬜ `New units`'s depth is a literal 1, not a derived one

The prompt describes the depth as *derived from the AST comparison itself*.
It is not. `round_record.py`'s `close` writes
`[units_entry(n, 1) for n in …]` — the 1 is a constant, and no path in the
generator can emit `(depth 2)`, because `depth_two` refuses the whole write
before any cell is written whenever depth 2 would apply.

That is coherent as enforcement, and it makes one paragraph of
`skills/code-review/orchestration.md` unreachable: *per entry rather than per
round, because a single fix pass can answer a finding in code that predates
the run and a finding inside an earlier unit in the same breath, and one
number for the round would be false of one of them.* A mixed round is refused
outright rather than recorded per entry, so the per-entry justification
describes a record that cannot be written.

The withdrawal of the depth-2 exit itself is **right**, and I re-derived both
halves rather than taking them. `depth_two` returns at `if not named or not
added`, and `units_named_earlier` over `round-1.md`'s `| New units | none |`
yields nothing, so the mechanised refusal cannot fire. And `New units` is
written from a top-level Python AST comparison, so a Markdown paragraph can
never be the parent it refuses under. What neither of `orchestration.md`'s two
cases covers is a finding inside a paragraph an earlier round's *fix pass*
wrote — round 2 deferred exactly that as finding 12's third bullet, and it is
not re-argued here.

## 22 ⬜ The empty code span already has a home, so #309 would be its second

Agreed that it is pre-existing, and it should not go on #309. It is already
recorded where it is caused, as a `# RIDER:` at `round_record.py:2512-2524`,
which names the mechanism (`chain.SEPARATORS` carries no backtick), the repair
site (the `note` line, *NOT* `chain.SEPARATORS`, because widening it there
would strip a backtick off a `deferred` home), the reading date, and the owner
— another work item's round 2 finding 9. A second ticket for it is the
duplicate that rider exists to prevent.

## 23 ⬜ `close` overwrites the grounds cell, and it is milder than it looks

Confirmed and asymmetric. `fixed` appends the reviewer's grounds — `grounds +
(f"; {old}" if old else "")` — while `answered` and `deferred` both assign
over `old`. For `deferred` the two cells are then set from the same value, so
the Grounds column becomes a copy of the Verdict column: `round-2.md`'s
findings 15 and 16 both read `#309` in both cells.

It loses less than the fix pass judged, and the reason changes the answer. The
reviewer's grounds are durable — `rounds/round-2-report.md` is committed, and
the `Finding` column survives the overwrite, so what a row loses is evidence
that exists at a coordinate one file over. What would genuinely have been lost
is the fix pass's *own* deferral grounds, and committing
`rounds/round-2-fixes.md` is what keeps those. That mitigation was the right
one. So: worth a row on #309 as the Grounds-column asymmetry, not worth a
reader.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 12 | Round 2's 12 — the corrected disclosure shipped unpinned and the depth-2 exit could not apply | `skills/verify/SKILL.md:429-438`, `tests/test_a_segment_feeds_the_flow_log.py` | answered | closed, and the withdrawal of the exit is right. Re-derived both halves in the code rather than taken: `depth_two` returns at `if not named or not added` and `units_named_earlier` over `round-1.md`'s `none` yields nothing; `New units` comes from a top-level Python AST comparison, so a Markdown paragraph can never be its parent. Executed: the case is green at `bcaba67` exit 0 and red against `2479859`'s `skills/verify/SKILL.md` exit 1, naming the clause it lost. **The pin is weaker than the account — see finding 20** |
| 13 | Round 2's 13 — the recorded mechanism was document frequency and the repair beside it moved the score by 0.001 | `survivors.md`, `overview.md` §*Not verified*, `phases/phase-3.md:57-58` | answered | closed on all four carriers, and every number reproduces. Executed by importing `survivor_check` and running its own pipeline one change at a time over `78d2c12..6a22d56`: the two candidates score **1.626** at `9d9e717`, **0.758** as shipped, **1.829** with `wanted`'s subtraction disabled, **0.757** with every `survivors.md` dropped from `corpus`, **1.853** with both — so the corpus side is worth 0.001 and the diff side is the cause. The reported phrase changes from `span is taken from` to the weaker `the last result`, which is deletion rather than reweighting. Read: `corrected`'s second return is the added sentences' n-grams and `wanted` subtracts them, so an exemption quote leaves the search set by construction. #308's citation is honest — its top comment opens *This issue's diagnosis is wrong*, carries the same three numbers, and moves the repair to `records_a_past_round` |
| 13b | The CI range's green is green for the reason #308 names | `bin/survivor-check` | answered | confirmed. Executed at `bcaba67`: `78d2c12..HEAD` with every `seal/specs/*/survivors.md` passed as CI passes them, and the same range with **no** `--exempt`, produce byte-identical output — 764 files, 80 removed sentences, *no removed wording is still standing*, exit 0 both times, `diff` empty. The flag changes nothing in either direction. The two release-note candidates score nothing above 0.01 at `bcaba67`, and 1.829 with the subtraction disabled |
| 13c | The fix range's green is honest | `bin/survivor-check`, range `044fc61..2caff29` | answered | confirmed by grep as claimed. 764 files against 17 removed sentences, exit 0. Every removed phrase of the old diagnosis — *mechanism is document frequency*, *dilutes the very score*, *a third carrier*, *below 1.0 at*, *drives the candidate under the floor*, *adding a unit to pin a unit* — survives only in `rounds/` records, which `corpus` excludes through `records_a_past_round`. So nothing stands in the scored pool, independently of the subtraction |
| 14 | Round 2's 14 — the proof line said 105 for the pair | `overview.md` §verified | answered | closed, **and the refusal of my 96 was correct**. Executed at `bcaba67` with exits read directly: `tests/test_session_cost.py` 69, `tests/test_a_segment_feeds_the_flow_log.py` 28, the pair **97**, exit 0. Writing 96 would have made the line false about the tree it ships in, which is round 1's finding 11 for the third time in one clause. The line's shape — both modules named, the 28 given as 27 plus this pass's case, and 96 recorded as the figure before it — is what makes the number auditable rather than merely right. **The third figure in the same clause was not swept — see finding 19** |
| 15 | Round 2's 15 — `round-1.md`'s two terminal rows stop mid-clause | `rounds/round-1.md:12-13` | deferred #309 | already deferred, named so it is not re-litigated. Confirmed standing at `bcaba67`, and #309's body carries both halves with the parse rule and the one judgment in it |
| 16 | Round 2's 16 — `round_record.py new` truncates a wrapped terminal-condition value | `skills/code-review/scripts/round_record.py` | deferred #309 | already deferred. #309 names the field as one another command parses, which is the half that makes it more than cosmetic |
| 18 | **A flat *three printed figures* stands against its own enumeration of five, in four live carriers — and one of them is the release note that ships.** `spec.md:76` bolds *three move elsewhere on the machine* and then lists 2 row spans and 3 between-the-rows figures with all five before-and-after pairs; `questions.md:11` writes the total and the 2 + 3 in one clause. The run introduced it in round 1's fix for the finding about this clause, and round 2 recorded *closed on all four* without adding it up | `seal/specs/1788926756-…/spec.md:76`, `questions.md:11`, `seal/ledger/1788926756-…​.md` row 4, `seal/specs/1788926756-…/changelog.md:13-14` | open | ⬜ correction — every Location is under `seal/specs/` or `seal/ledger/`, so §*The last round verifies* keeps it out of `Needs a fix`. **It belongs in the closing commit rather than *in passing*:** `gather_changelog.py` folds the fragment verbatim into the released section, and this item's own `survivors.md` argues #307 on the grounds that a released entry may not then be edited. The ledger row is the same at the fold. Read, and the arithmetic is on one line in each carrier. Editing a Claim cell moves no anchor — `bin/evidence-check` is 1041 ok · 0 drifted either side |
| 19 | **The proof line's `evidence-check` figure is the base's number, never re-measured.** `overview.md:20` says 1033 ok inside a clause labelled **executed**; the check reports 1041 | `seal/specs/1788926756-…/overview.md:20` | open | ⬜ correction. Executed in a clone at four commits: **1033** at `7ca5008`, 1026 ok · 7 drifted at `7244a4c`, **1041** at `80cc7ce` — the commit that wrote the line — and 1041 at `b411e77` and `bcaba67`. The honest figure is already in the work item at `phases/phase-3.md:40`. Third figure in one parenthetical, and no `N passed` sweep can match `N ok` |
| 20 | **The case planted for finding 12 passes against the regression its own docstring names.** Its four assertions test four literal strings, and a reordering of the sentences carrying them satisfies all four — so the paragraph's *vocabulary* is pinned and its *claim* is not | `tests/test_a_segment_feeds_the_flow_log.py:536-561` | open | 🟡, executed. Four mutations one at a time in a clone, each restored and sha256-compared: the two causes swapped → **exit 0**; the measurement inverted to *came from a call that crossed a turn and none of it from calls batched into one message* → **exit 0**; *Something running in the background is the usual cause.* added sentence-initially → **exit 0** (the negative assertion is case-sensitive); the old wording restored lowercase mid-sentence → exit 1. The last is the fix pass's own arm 4, and it is the only one of the four that fires — its red arms all deleted or reworded a phrase, which measures the assertion's string and not the claim. The fix below pins the ranking clause and the measurement clause whole: executed green as shipped and red on all five arms |
| 21 | The depth in `New units` is a literal `1`, not derived, and `orchestration.md`'s per-entry justification describes a record the generator cannot write | `skills/code-review/scripts/round_record.py` §`close`, `skills/code-review/orchestration.md:238-242` | open | ⬜, and a correction of the prompt's account rather than of the record. Read: `close` writes `[units_entry(n, 1) for n in …]`, and `depth_two` refuses the whole write before any cell whenever depth 2 applies — so `(depth 2)` is unreachable and a mixed round is refused rather than recorded per entry. The row `(depth 1)` is honest as the mechanism's only output; what a reader cannot tell is a measured 1 from a default 1 |
| 22 | The empty code span already has a home, and #309 would be its second | `skills/code-review/scripts/round_record.py:2512-2524` | open | ⬜, agreed pre-existing and **disagreed on the destination**. The `# RIDER:` at that coordinate already records the mechanism (`chain.SEPARATORS` carries no backtick), the repair site (the `note` line, not `chain.SEPARATORS`, because widening it there strips a backtick off a `deferred` home), the reading date, and the owner — another work item's round 2 finding 9. Read; visible in `round-1.md` rows 1-3 as the rider says |
| 23 | `close` assigns over the grounds cell for `answered` and `deferred` where `fixed` appends, and for `deferred` the Grounds column becomes a copy of the Verdict column | `skills/code-review/scripts/round_record.py` §`close` | open | ⬜, agreed and **milder than judged**. Read: `fixed` writes `grounds + ("; " + old)` while the other two arms assign `value`, and the `deferred` arm sets both cells from it — `round-2.md`'s 15 and 16 read `#309` twice. Nothing is lost: the reviewer's grounds are durable in the committed `rounds/round-2-report.md` and the `Finding` column survives, so the only grounds at risk were the fix pass's own, which is exactly what committing `rounds/round-2-fixes.md` keeps. The mitigation was right; the asymmetry is a row on #309 and owes no reader |

## Paste-ready fixes

```python
def test_the_section_names_batching_as_the_way_a_share_passes_one_hundred():
    """A share over 100% is a true reading, and WHY it happens is the half a
    person acts on. The paragraph used to send that reader looking for a
    background command; measured over one machine's transcripts, 100% of the
    overlap above a second is calls batched into one assistant message and
    none of it crosses a turn. Nothing else in the tree reads this clause, so
    without this case an edit can put the rarer cause back as the ordinary
    one and no check says anything.

    The two ranking and measurement clauses are asserted WHOLE rather than by
    their vocabulary. Round 3 measured why: with one substring per phrase,
    swapping the two causes and inverting the measurement both leave every
    phrase standing, so the case passed against the exact regression this
    docstring names. `section_body` collapses whitespace, so a clause survives
    a re-wrap and only a change to the wording itself turns this red."""
    body = section_body()
    assert "calls running at once" in body, (
        "the paragraph must name concurrent calls as what puts a share over "
        "100%, not something running in the background"
    )
    assert (
        "Batching is the ordinary way in and a background command is the "
        "rarer one" in body
    ), (
        "batching is the ordinary way a share passes 100% and the background "
        "command the rarer one; asserting the two words separately passes "
        "with the ranking reversed, which is the edit this case exists to stop"
    )
    assert (
        "every second of overlap above a second came from calls batched into "
        "one message and none of it from a call that crossed a turn" in body
    ), (
        "the measured claim has a direction, and the vocabulary of both "
        "halves survives inverting it — so the clause is asserted whole"
    )
    assert "something running in the background" not in body.lower(), (
        "the old wording named the rarer cause as the ordinary one. Lowered "
        "because the same phrase returning at the start of a sentence is the "
        "same regression"
    )
```

```
| **No PRINTED figure in THIS PROJECT's transcripts moves under `max(end)`, and five move elsewhere on the machine — 2 row spans and 3 between-the-rows figures** — this project's directory: 16 transcripts, 12 to 836 calls, 0 spans and 0 rows move.
```

```
| 1 | The readings already posted to #51 need no marking line for the span's new definition | **Executed, on every printed surface.** This project's 16 transcripts move nothing: no run span, no row span, no between-the-rows figure. Machine-wide five printed figures do move — 2 row spans and 3 between-the-rows figures — and every one is in another project's transcript.
```

```
| No printed figure in THIS PROJECT's transcripts moves under the new span rule, on any printed surface; five figures move elsewhere on the machine — 2 row spans and 3 between-the-rows figures |
```

```
  **Nothing this repository has published moves, and elsewhere on the machine
  five printed figures do — 2 row spans and 3 between-the-rows figures.**
```

```
            `evidence-check` (1041 ok · 0 drifted, exit 0),
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on both modules the skill change touches, at `bcaba67` | 97 passed, exit 0 read directly. Separately 69 and 28 — round 2's 97 is right and the 96 it was told to write would have been false |
| `bin/evidence-check` at `7ca5008`, `7244a4c`, `80cc7ce`, `b411e77`, `bcaba67` | 1033 ok · 0 drifted; 1026 ok · 7 drifted; 1041; 1041; 1041 — all exit 0. `overview.md:20` says 1033 |
| `bin/unverified-check` at `bcaba67` | exit 0 — 59 overviews · 204 open · 47 closed · 0 unreadable, matching the fix pass's figure |
| the new case, green and red against `2479859`'s `skills/verify/SKILL.md` | exit 0 green, exit 1 red on assertion 1, naming the clause it lost |
| four mutations of the span paragraph against the new case, one at a time | causes swapped **exit 0**; measurement inverted **exit 0**; old phrase added sentence-initially **exit 0**; old phrase restored lowercase mid-sentence exit 1. `skills/verify/SKILL.md` restored and sha256-compared after every arm, `fd3a4e7d285d` throughout |
| the same five arms against the proposed replacement assertions | green as shipped, red on every arm including the three the shipped case misses |
| `bin/survivor-check --range 78d2c12..HEAD` at `bcaba67`, with every `seal/specs/*/survivors.md` and with none | byte-identical, `diff` empty — 764 files, 80 removed sentences, *no removed wording is still standing*, exit 0 both times |
| `bin/survivor-check --range 044fc61..2caff29` with this item's exemption and with none | 764 files against 17 removed sentences, *no removed wording is still standing*, exit 0 both times |
| grep for every removed phrase of the old diagnosis across the tree | only in `rounds/` records, which `corpus` excludes — so the fix range's green is honest independently of the subtraction |
| `survivor_check`'s own pipeline over `78d2c12..6a22d56`, one change at a time, reading the two release-note candidates out of the result | 1.626 at `9d9e717`; 0.758 as shipped; 1.829 with `wanted`'s subtraction off; 0.757 with `survivors.md` out of `corpus` (pool 764 → 760); 1.853 with both. Reported phrase `span is taken from` → `the last result`. At `bcaba67` the pair scores nothing above 0.01 |
| `bin/survivor-check --range 7ca5008..HEAD` at `62347dc`, all exemptions | 763 files against 85 removed sentences, no removed wording standing, exit 0 — `phases/phase-3.md:59` reproduces exactly, on the build range it names |
| `gh issue view` on #307, #308, #309 | #308's body still states the disproved cause and the 0.001 repair; its top comment opens *This issue's diagnosis is wrong*, carries 0.758 / 0.757 / 1.829, moves the repair to `records_a_past_round` and says what is still true. The citation is honest. #309 carries both of round 2's 15 and 16 |
| the row counts behind `overview.md`'s evidence line | this item's ledger fragment holds 5 rows after its header; `seal/ledger.md` is 7 changed lines over the branch |

```
# In a `git clone --no-local` of the repository at bcaba67, from the clone
# root, with a `uv` venv because pytest is not installed for the system
# interpreter. Every probe was named test_tmp_*, run once and deleted; both
# the clone and the working checkout are clean and nothing was written in the
# working checkout except this report.

uv venv .venv && uv pip install --python .venv/bin/python pytest

./bin/test tests/test_session_cost.py tests/test_a_segment_feeds_the_flow_log.py -q ; echo $?
./bin/evidence-check ; echo $?
./bin/unverified-check ; echo $?

# One figure per commit, read with the exit taken directly:
for s in 7ca5008 7244a4c 80cc7ce b411e77 bcaba67; do
  git checkout -q $s && ./bin/evidence-check | grep '^total'
done ; git checkout -q bcaba67

./bin/survivor-check --range 78d2c12..HEAD \
  $(for f in seal/specs/*/survivors.md; do printf -- "--exempt %s " "$f"; done) > a.txt
./bin/survivor-check --range 78d2c12..HEAD > b.txt
diff a.txt b.txt ; echo $?

# The mutation arms and the mechanism isolation, in outline: a Python probe
# holds skills/verify/SKILL.md's bytes, replaces one clause, runs the single
# case through bin/test, writes the bytes back and asserts the sha256 matches
# before the next arm -- every substitution asserted present first, so a
# pattern that missed is a failure rather than a silent pass. The isolation
# imports survivor_check as a module and runs its own pipeline:
#   gone, written = corrected(root, A, B)      # written = set() for one arm
#   keep = wanted(gone, written)
#   pool = corpus(root, B)                     # survivors.md filtered for one
#   where, files = carriers(pool, keep)
#   score(gone, keep, where, weights(len(pool), files), 0.01)
# then reads the rows whose candidate path is CHANGELOG.md or the 1788700685
# fragment and whose raw text holds the exempted sentence.
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `skills/verify/SKILL.md:429-438`, `tests/test_a_segment_feeds_the_flow_log.py:536-561` | round 2's 12 — answered, and finding 20 is inside the unit it planted |
| round-2 | `survivors.md`, `phases/phase-3.md:57-58`, `overview.md` §*Not verified* | round 2's 13 — answered on all four carriers |
| round-2 | `overview.md` §verified | round 2's 14 — answered, and findings 18 and 19 are the same clause's remaining figures |
| round-2 | `rounds/round-1.md:12-13`, `skills/code-review/scripts/round_record.py` | round 2's 15 and 16 — at #309, not re-litigated |
| round-1 | `spec.md:76`, `questions.md` Q1, `seal/ledger/1788926756-…​.md` row 4, this item's changelog fragment | round 1's 3 — reopened as finding 18. The four carriers its fix pass rewrote are the four that carry the flat total |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 20 — the pin tests vocabulary rather than the claim. The run is capped, so this is a deferred candidate rather than a commissioned fix | a new issue, or the closing commit if the owner takes the paste-ready case | the owner |
| Finding 21 — `orchestration.md`'s per-entry depth justification describes a record `close` cannot write | #309, with the generator's other two | the orchestrator |
| Finding 23 — `close`'s Grounds-column asymmetry between `fixed` and `deferred`/`answered` | #309 | the orchestrator |
| Finding 22 — the empty code span. **Not** #309: it already has a home | the `# RIDER:` at `round_record.py:2512-2524` and another work item's round 2 finding 9 | that work item |
| `orchestration.md` names no case for a finding inside something an earlier round's fix pass wrote — round 2's finding 12, third bullet | already deferred by round 2 to an issue with finding 16 | the orchestrator |
| Q3, Q4 and the disclosure-placement question | `questions.md`, already deferred by rounds 1 and 2 | the owner |
| The full suite, the repository-wide lint and the typecheck; `ruff` is absent from the working checkout | `agent-contract` §2 — the orchestrator's, once, and now due | the orchestrator |
| Windows | #103's standing gap | nobody has run it |

Needs a fix: yes — finding 20, the only one in the tool; findings 18 and 19 are corrections §*The last round verifies* keeps out of this field, and 18 belongs in the closing commit because the release folds one of its carriers beyond reach
Loses a record or crashes: no — every finding is a sentence or an assertion that does not fire, `bin/evidence-check`, `bin/unverified-check` and `bin/survivor-check` all exit 0, and nothing leaves the root or raises

## Proof

Opened: `seal/specs/1788926756-…/overview.md`, `spec.md`, `questions.md`,
`changelog.md`, `survivors.md`, `phases/phase-3.md`,
`rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-2.md`,
`rounds/round-2-report.md`, `rounds/round-2-fixes.md`;
`seal/ledger/1788926756-three-sentences-are-wrong-about-where-a-duration-is.md`;
`skills/verify/SKILL.md:415-450`; `tests/test_a_segment_feeds_the_flow_log.py`;
`skills/code-review/scripts/survivor_check.py`;
`skills/code-review/scripts/round_record.py`;
`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it*;
`docs/review-chain-spec.md` §*The last round verifies*; `CLAUDE.md`;
`skills/agent-contract/SKILL.md`. GitHub issues #307, #308, #309.

Not opened, and no verdict rests on them: the full suite, `ruff`, the
typecheck, and the machine's transcripts under the user's own project
directory — finding 18's arithmetic is read off the four carriers' own
enumerations rather than re-measured there.
