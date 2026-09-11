# Round 1 — the writer of the contract is not its executor

Target SHA `67c47ce60c2f55238fe0531cd84a4ef34058191c` · base
`origin/release/v0.11.0` = `47c993d2eb150d546574723a3034ed229caed3f4` ·
46 files, +2857 / −180. Reviewed in a `git clone --no-local` at the target
SHA; nothing was written in the working checkout except this file.

## What this round found, in one paragraph

**The code is right and the sweeps are not finished.** Every production
change on this branch holds under execution — the fourth axis parses, the two
marks do not answer for each other, the notice prints one line for two axes
and its singular form is byte-identical to what 0.7.0 shipped. What is
unfinished is the class the branch itself is an instance of: a new member
joins an enumerated set, and the enumerations that name the set have to be
swept. Two of them were (`tests/test_docs_line_wrap.py`'s `COVERED`,
`tests/test_one_word_one_meaning.py`'s `SEAL_SWEPT`); three were not, and one
of those three is read by a checker that CI fails on. Beneath that sit two new
cases that stay green when the rule they were written for is inverted.

The four items the handoff named are answered at the end, under
§*The four named items*. Three of the four are correct as built; the ledger
one is correct for the reason the handoff doubted and wrong for a reason
nobody raised.

---

## The ledger check exits 2 at this SHA, and the `ledger` CI job fails on it

**Location** — `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/survivors.md:11`,
`.../phases/phase-2.md:77`, `:133`, `:166`, `.../phases/phase-4.md:35`,
`:36`, `:82`.

The orchestrator's handed-over fact is true and is only the ledger arm of the
command. `bin/evidence-check` unscoped reports **1121 ok · 0 drifted · 0
broken** for the ledger, and then its **records** arm reports **7 refused · 1
drifted** and the process exits **2**. At the base it exits **0** with
`0 refused · 0 drifted`, so the branch is what changed it.

Exit 2 is not a warning. `skills/evidence-check/scripts/evidence_check.py:2473`
returns 2 when anything is refused, and `.github/workflows/test.yml:89-94`
reads that:

```
if [ "$code" -ge 2 ]; then exit "$code"; fi
if [ "$code" -eq 1 ]; then echo "::warning::…" fi
```

The `ledger` job has no base-ref gate — `test.yml` runs on every
`pull_request` — so draft pull request #352 carries a red check now, and will
whatever it is retargeted at. `overview.md:40` reasons about this and reasons
only about the drift: *CI runs the checker without `--strict`, so drift is a
warning*. That is right about the DRIFTED line and does not reach the seven
refusals, which are exit 2 with or without `--strict` (both forms exit 2 here;
I ran them separately).

Every one of the seven is a record correctly quoting a name the branch itself
removed — the design-gate case phase 2 split, and the predicate phase 4b
renamed. The records are right; what is missing is the marker the checker's own
message names. **Executed**: adding `NAME NOT IN TREE` to those seven lines in
the clone took the run from exit 2 to exit 1, `0 refused`, and CI's exit-1 arm
is a `::warning::`. The repository has done exactly this before — work item
`1789002694` carries the same treatment in `phases/phase-4.md:112` and in
seven other record lines.

`docs/review-chain-spec.md:155` puts this finding's location in records, so it
is a correction rather than a round: it owes no fix pass and no reader, and it
is corrected in the closing commit. It stays out of `Needs a fix` for that
reason and for no other — it is the single most consequential thing in this
report.

## Then the same sweep was missed in a place no checker reads

**Location** — `tests/test_the_records_can_be_carried_out_and_in.py:55`.

`BESIDE_THE_ROOT` enumerates the session-state files that sit beside the root
under the common git directory, and its own comment states what the list is
for: *None may ever be in a zip, and the case that asserts it builds every one
of them.* The branch creates a sixth such file, `specseal-planner`, and the
tuple still holds five. So the case builds five files and asserts about five,
and the sentence above it is no longer true of the list.

**The exclusion itself holds** — I checked rather than assumed, because the
answer decides whether this is a leak or a stale list. Nothing in
`skills/implement/scripts/seal.py` or `hooks/root-migrate.py` carries a name
list; the root is its own directory and the walk never leaves it. **Executed**:
adding `"specseal-planner"` to the tuple in the clone and running the module
gives **96 passed**, so the new mark is excluded structurally and the case
simply gets stronger for free.

This is the §12 shape rather than a one-off. The branch swept
`tests/test_docs_line_wrap.py`'s `COVERED` and
`tests/test_one_word_one_meaning.py`'s `SEAL_SWEPT` for the same reason — a new
file joins a list somebody already looked at — and stopped at two of three.

## A new case stays green when the rule it was written for is inverted

**Location** — `tests/test_a_question_says_who_can_answer_it.py:121`, against
`agents/framer.md:223`.

`test_a_person_answerable_row_reaches_the_report_in_full` exists for Q2's
answer: a row only a person can answer goes into the framer's report **in
full**, and the other two answerers get the path and the count. Its own
docstring says the old rule was the opposite and that reversing it is what the
case is guarding.

**Executed** — I replaced `agents/framer.md:223`'s

    - **A row only a person can answer is reproduced in full.**

with

    - **A row only a person can answer is the path and the count.**

and ran `bin/test tests/test_a_question_says_who_can_answer_it.py`: **6
passed**. The rule was inverted to the exact state the case was written to
catch, and nothing went red. Clone restored with `git checkout --`.

Why each of the four assertions survives:

- `"never the rows' text" not in report` — that string has never been in
  `agents/framer.md`. It is absent whatever the rule says.
- `"in full" in report` — satisfied by the OTHER bullet, four lines down:
  *sending them in full is how a batch stops being answerable in one sitting*.
- `"handed a count of"` and `"the path and the count"` — both survive in the
  surrounding explanation, which the inversion did not touch.

What the case actually pins is that the paragraph still exists. The module's
sibling shows the right shape: `test_the_report_does_not_reduce_the_frame_to_counts`
asserts the literal `"The phases, one line each"`, and that half does go red.

This is §15 at one remove. The case was shown red before it was committed —
against a `framer.md` that had no such section at all — and a case that goes
red against an absent section is not the same as a case that goes red against a
wrong one.

## And the case beside it pins only half of what it claims

**Location** — `tests/test_a_question_says_who_can_answer_it.py:150`, against
`agents/framer.md:217`.

Same file, same cause: a heading fragment used as the anchor.
`test_the_report_does_not_reduce_the_frame_to_counts` claims two things, and the
second is unpinned. **Executed** — replacing

    - **What you put out of scope, and why, one line each.**

with

    - **What you put out of scope, as a count.**

and running `-k does_not_reduce_the_frame_to_counts` gives **1 passed, 5
deselected**. The assertion is `"out of scope" in report`, which is the
heading's first three words and survives the change that matters.

The half that is unpinned is the half the docstring says the case is for: this
frame's own scope enumerated the documents calling the agent set four and
omitted both README editions, which is what phase 1 then hit. The phase half
of the same case is sound — inverting it goes red.

## A follow-up row was written outside its own table

**Location** — `seal/follow-up.md:65-66`.

The branch adds the row recording that the THIRD routing axis's template pin is
self-consistent by construction. It is inserted after the blank line that
already closed the table above it, and followed by another blank line, so
Markdown renders it as a paragraph opening with a literal `|` rather than as a
row of the list. The two rows before it sit inside the table.

It is not silently dropped from any check — `tests/test_a_rider_reaches_its_file.py:52`
collects any line starting with `|` under the heading, so
`test_no_schedulable_row_carries_a_coordinate` still sees it, and its
coordinate is an anchor rather than a `file:line`, so that case is green on its
own terms. What is lost is the human half: this is the row `overview.md` and
`seal/ledger/1789081272-…md`'s P3 both send the repository owner to, and a
reader scanning the table does not meet it as an item. One blank line.

## Five ledger rows were re-hashed and none moved its `Checked` date

**Location** — `seal/ledger.md:275`, `:276`, `:277`, `:283`, `:284`.

`CLAUDE.md:118` — *The `Checked` column holds the date somebody read the code.
Re-verifying is re-reading and then running `evidence-check --reverify`, which
recomputes the hash and names what it changed.*

Ten rows were re-hashed on this branch. Five moved `Checked` from 2026-09-10 to
2026-09-11. The other five — every one of them an implementer row phase 4b
touched — kept 2026-09-08, 2026-09-02, 2026-09-05, 2026-09-02, 2026-09-02. So
the branch demonstrates the convention and departs from it in the same diff.

Two of the five contradict themselves inside the row: `:275` and `:283` both
carry **Re-read 2026-09-11 by work item 1789081272 (#84)** in `Notes` beside a
`Checked` cell that says the code was last read on 2026-09-08 and 2026-09-02.
The other three record nothing at all — a recomputed hash with no statement
that anybody looked.

## The template's own count went stale where it tells a reader to look

**Location** — `templates/sdd-routing.md:59`, reached from `:25`.

The new `Planning` comment block says *OPTIONAL, on exactly the terms the
`Implementation` row below has, and for the same reasons — read them there*, and
deliberately writes no second copy. A reader sent there meets:

    This one ships as a PLACEHOLDER while the other two ship answered,
    and the difference is deliberate

There are now three other axes, not two, and one of them — `Planning`, the row
that sent the reader here — also ships as a placeholder. The sentence's
argument is still right; its arithmetic is the thing the redirect was supposed
to protect from drifting.

## S10's own acceptance row is the one place the deferral is not written

**Location** — `spec.md:87`.

The deferral of phase 5 to #350 is recorded consistently in seven places —
`spec.md:36-48`, `plan.md:90` and `:96-104`, `overview.md:29`, `:57`, `:96`,
`phases/phase-6.md`, `pr.ko.md`, `docs/flow.md:102`. The acceptance table's S10
row carries no marker: its `Verifiable how` cell still reads *a new case over a
built transcript tree, executed*, so a reviewer reading the table row by row —
which is stage 1 of a review — meets a live criterion and has to descend into
§Scope to learn it is not one. Every other place uses `deferred #350`.

## Two cosmetic leavings

`docs/one-root-by-lifetime.md:111` and `docs/one-root-by-lifetime.ko.md:109` —
the new `specseal-planner` line in the tree diagram is one column left of the
`specseal-implementer` line below it, in both editions.

`plan.md`'s third `Status` value has no home outside this work item.
`plan.md:96-104` argues well that `deferred #N` satisfies the rule rather than
bending it, and `templates/sdd-plan.md` still says *Status is empty, or the
commit that closed the phase.* The argument is the kind that belongs where the
next work item reads it — the template, or a `seal/follow-up.md` row. Neither
exists.

---

## The four named items

**1 — the re-pointed ledger row. The handoff's doubt is answered by
`CONTRIBUTING.md`, and it does not need a judgment call.** `CLAUDE.md:121`'s
bare sentence is not the whole rule. `CONTRIBUTING.md:105-115` splits it in
two — *the claim still holds and you have re-read it* → `--reverify`; *the
claim went with the code* → remove the row — and `:116-119` then names the
rename case outright: *Renamed a cited symbol or file? `bin/evidence-check
--reverify .` re-anchors every row whose content provably moved intact.* A
rename with the claim intact is the first branch and the sanctioned command is
re-anchoring. Phase 4b took the correct branch. **No finding**, and what would
help the next reader is a pointer from `CLAUDE.md:121` to those two branches,
since the sentence alone reads as an unconditional prohibition. What IS wrong
about the row is its `Checked` cell, above, which nobody raised.

**2 — the constant count.** The builder is right and the reasoning is the
repository's own. An alias is two spellings of one string, `PLANNING_ANSWERS =
(BY_FRAMER, BY_SESSION)` says the thing by using the string, and nothing would
go red if a later edit gave the alias a different value. **No finding.** One
observation: `spec.md` §Data & interfaces still lists four constants with no
marker, where §Scope item 7 carries its reversal struck through with grounds. A
reader meets a four-constant interface that was never built. Leaving the frame
alone is defensible — it is the framer's writing — but the same document shows
how a reversal is recorded when somebody decides to record one.

**3 — `deferred #350` as a third `Status` value.** The argument holds. An issue
number asserts a past state somebody can open, exactly as a hash does, and this
repository already writes `deferred #N` in every round record's fix table. **No
finding on the value**; see the last cosmetic item for where the argument still
needs a home.

**4 — `fold_ledger.py --check` exiting 1.** Reproduced, and the reading is
correct. `--check` exit 1; `--version 0.11.0 --dry-run` exit 0 writing nothing;
`gather_changelog.py --version 0.11.0 --dry-run` exit 0. `.github/workflows/hygiene.yml:96`
and `:115` both gate on `github.base_ref != main` and exit 0 early otherwise, so
neither runs on a feature pull request. **No finding.**

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | `bin/evidence-check` exits 2 at this SHA on seven `NOT-IN-TREE` refusals, and `test.yml`'s `ledger` job fails on any exit ≥ 2. Base exits 0 | `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/survivors.md:11`; `phases/phase-2.md:77`, `:133`, `:166`; `phases/phase-4.md:35`, `:36`, `:82` | open | Executed at base and at HEAD, exit codes read directly. Marking the seven lines in the clone took the run to exit 1 / `0 refused`, which CI renders as a warning. A record location, so a correction per `docs/review-chain-spec.md:155` — but the CI failure is live |
| 2 | `test_a_person_answerable_row_reaches_the_report_in_full` cannot fail: inverting the rule it exists for leaves it green | `tests/test_a_question_says_who_can_answer_it.py:121` | open | Executed. `agents/framer.md:223` inverted to its opposite, module run: 6 passed. Each of the four assertions is satisfied by text the inversion did not touch |
| 3 | `test_the_report_does_not_reduce_the_frame_to_counts` pins the phases half and not the out-of-scope half | `tests/test_a_question_says_who_can_answer_it.py:150` | open | Executed. `agents/framer.md:217` changed to a count, `-k` run: 1 passed, 5 deselected. `"out of scope"` is a heading fragment that survives the change |
| 4 | `BESIDE_THE_ROOT` does not carry `specseal-planner`, so the case its comment describes builds five of six | `tests/test_the_records_can_be_carried_out_and_in.py:55` | open | Executed. Adding the entry gives 96 passed, so the exclusion is structural and the list is merely stale. Two sibling enumerations were swept on this branch and this one was not |
| 5 | The new follow-up row sits outside its table and renders as literal text | `seal/follow-up.md:65-66` | open | Read, then checked against `tests/test_a_rider_reaches_its_file.py:52`: the parser still sees it, so no check is bypassed; only a human reader loses it |
| 6 | Five ledger rows were re-hashed with `Checked` left stale; two contradict their own `Notes` | `seal/ledger.md:275`, `:276`, `:277`, `:283`, `:284` | open | Executed against the diff: ten rows re-hashed, five moved 2026-09-10 → 2026-09-11, these five did not. `:275` and `:283` say **Re-read 2026-09-11** beside `Checked` cells of 2026-09-08 and 2026-09-02 |
| 7 | `the other two ship answered` is now a miscount, in the paragraph the new `Planning` comment redirects readers to | `templates/sdd-routing.md:59` | open | Read. Three other axes now, and `Planning` also ships as a placeholder |
| 8 | S10's acceptance row is the only place the #350 deferral is not written | `spec.md:87` | open | Read against seven places that do record it |
| 9 | The `specseal-planner` tree-diagram line is one column out in both editions | `docs/one-root-by-lifetime.md:111`, `docs/one-root-by-lifetime.ko.md:109` | open | Read |
| 10 | `plan.md`'s third `Status` value is argued only inside this work item; `templates/sdd-plan.md` still states two, and no follow-up row carries it | `plan.md:96-104`, `templates/sdd-plan.md:93` | open | Read. The argument is sound; it has no home the next work item reads |
| 11 | Named item 1 — the ledger row re-pointed rather than removed | `seal/ledger.md:275`, `CONTRIBUTING.md:105-119` | withdrawn | `CONTRIBUTING.md:116` names the rename case and sanctions `--reverify` re-anchoring. Phase 4b took the branch the rule assigns |
| 12 | Named item 2 — three constants where `spec.md` names four | `hooks/routing.py:61-66` | withdrawn | The fourth was an alias; `PLANNING_ANSWERS` says the thing by using `BY_SESSION`. Recorded as a divergence |
| 13 | Named item 3 — `deferred #350` as a `Status` value | `plan.md:90` | withdrawn | Satisfies the rule's stated reason; see finding 10 for the part still owed |
| 14 | Named item 4 — `fold_ledger.py --check` exit 1 on this branch | `plan.md` row 6, `.github/workflows/hygiene.yml:115` | withdrawn | Reproduced; the hygiene steps gate on `base_ref == main` and exit 0 early otherwise |
| 15 | The broad gate — full suite, repository-wide lint, typecheck | `seal/config.md` `Broad gate` row | ❓ out of verified scope | Contract §2 makes it one act with one owner and `agents/sealer.md` is the owner. Not run. Answerer: the orchestrator, through the sealer spawn |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_implementer_is_recorded.py tests/test_routing_is_recorded.py` at target SHA, in the clone | 55 passed |
| `bin/test tests/test_the_records_can_be_carried_out_and_in.py` at target SHA | 96 passed |
| `bin/evidence-check` unscoped at target SHA, exit code read directly | ledger 1121 ok · 0 drifted · 0 broken; records 7 refused · 1 drifted; **exit 2** |
| `bin/evidence-check --strict` unscoped at target SHA | **exit 2** |
| `bin/evidence-check` unscoped at `origin/release/v0.11.0` | 1100 ok · 0 drifted · 0 broken; records 0 refused · 0 drifted; **exit 0** |
| `bin/evidence-check` with `NAME NOT IN TREE` added to the seven refused lines in the clone | 1121 ok · **0 refused** · 1 drifted; **exit 1** — which `test.yml` renders as a warning |
| `python3 .github/scripts/rider_check.py` at target SHA | 26 ok · 0 drifted; exit 0 |
| `python3 .github/scripts/fold_ledger.py --check` | exit 1 — the correct answer on a feature branch |
| `python3 .github/scripts/fold_ledger.py --version 0.11.0 --dry-run` | exit 0, wrote nothing |
| `python3 .github/scripts/gather_changelog.py --version 0.11.0 --dry-run` | exit 0, wrote nothing |
| Mutation: `agents/framer.md:223` inverted, then `bin/test tests/test_a_question_says_who_can_answer_it.py` | **6 passed** — the case cannot fail |
| Mutation: `agents/framer.md:217` reduced to a count, then `-k does_not_reduce_the_frame_to_counts` | **1 passed, 5 deselected** — half the case cannot fail |
| Mutation: `specseal-planner` added to `BESIDE_THE_ROOT`, module re-run | 96 passed — the exclusion is structural, the list is stale |
| Probe `test_tmp_notice_at_the_declaring_commit.py` — the notice against a `git commit` payload in three built repositories | Both axes unfulfilled → one line naming both; implementation only → byte-identical to the 0.7.0 wording; planning mark standing → speaks only for the axis that is missing. Deleted after the run |
| Broad gate — `bin/test -q && uvx ruff check . && uvx ruff format --check .` | **not yet** — not run by this round, and out of its scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the third routing axis's template pin should be widened the way the fourth's was | `seal/follow-up.md:66` — already open, and finding 5 is about how that row renders, not about re-opening it | the repository owner |
| Whether both README editions join `spec.md` §Scope item 8, and whether `agents/framer.md` preloads the two utility skills | `questions.md` Q4 — already open | the repository owner |
| Whether the records arm should tolerate a superseded coordinate quoted beside its successor | `overview.md:40` — already open; the DRIFTED line at `phases/phase-1.md:131` is exit-1 class and CI renders it as a warning | the repository owner |
| #350, the per-agent wall clock | `docs/flow.md:102` under 0.11.1, and `spec.md` §Scope item 7 | already scheduled |

## Paste-ready fixes

Finding 1 — append the marker to each of the seven prose lines. Nothing else
on the line changes.

```
seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/survivors.md:11
phases/phase-2.md:77   phases/phase-2.md:133   phases/phase-2.md:166
phases/phase-4.md:35   phases/phase-4.md:36    phases/phase-4.md:82

Append to each line:  <!-- NAME NOT IN TREE: the name this branch removed, quoted as the record read it -->
```

Finding 2 — anchor on the bullet's own literal, the way the sibling case does.

```python
    assert "A row only a person can answer is reproduced in full" in report, (
        "the report no longer sends a person-answerable row's own text. "
        "Nobody can answer a question they were handed a count of, so a "
        "frame obeying the shorter rule ships an approval given against "
        "nothing"
    )
```

Finding 3 — the same repair on the other half.

```python
    assert "What you put out of scope, and why, one line each" in report, (
        "the report gives a count of what was excluded instead of the "
        "exclusions. That is where a framing error hides: what was decided "
        "is visible and what was left out is not"
    )
```

Finding 4 — one entry, and the comment above it already says why.

```python
BESIDE_THE_ROOT = (
    "specseal-implementer",
    "specseal-planner",
    "specseal-reviewed",
    "specseal-parity",
    "specseal-scratch",
    "specseal-last-export.json",
    "specseal-session-lease",
)
```

Finding 5 — delete the blank line at `seal/follow-up.md:65` so the row rejoins
the table above it. The blank line at `:67`, before `## Riders waiting on a
file another branch holds`, stays.

Finding 6 — set `Checked` to `2026-09-11` in the five rows, which is the date
their own `Notes` and `phases/phase-4.md` give for the re-read.

```
seal/ledger.md:275   2026-09-08 -> 2026-09-11
seal/ledger.md:276   2026-09-02 -> 2026-09-11
seal/ledger.md:277   2026-09-05 -> 2026-09-11
seal/ledger.md:283   2026-09-02 -> 2026-09-11
seal/ledger.md:284   2026-09-02 -> 2026-09-11
```

Finding 7 — `templates/sdd-routing.md:59`.

```
     This one and the `Planning` row above ship as PLACEHOLDERS while
     `Review` and `Destination` ship answered, and the difference is
     deliberate:
```

Finding 8 — `spec.md:87`, in the shape §Scope item 7 already uses.

```
| ~~S10 an agent's own wall clock is a number~~ — **deferred to #350**, milestone 0.11.1, on 2026-09-11 | ~~Given a transcript with subagent transcripts beside it · When `session-cost` runs in the new mode · Then one row per segment, named by the spawn's `subagent_type`, with its own span, calls and tokens — and the count of segments it could not name is printed rather than hidden~~ | ~~a new case over a built transcript tree, executed~~ — nothing in this work item answers it |
```

Finding 9 — `docs/one-root-by-lifetime.md:111` and
`docs/one-root-by-lifetime.ko.md:109`: four more spaces after
`specseal-planner`, so the description column lines up with the
`specseal-implementer` line below it.

Finding 10 — no code fix. Either add the third value to
`templates/sdd-plan.md`'s `Status` sentence, or open a `seal/follow-up.md` row
carrying `plan.md:96-104`'s argument with the repository owner as answerer.

Needs a fix: yes — findings 2, 3 and 4, all three in `tests/`. Findings 1 and
5 through 10 are corrections owed at the closing commit rather than a fix
pass, and finding 1 is the one that must land before the pull request is read,
because the `ledger` job is red without it.

Loses a record or crashes: no — nothing found leaves the root or crashes.
Finding 1 fails a CI job; it does not lose or corrupt anything.

---

## Proof block

- opened — `spec.md`, `plan.md`, `questions.md`, `overview.md`, `survivors.md`,
  `phases/phase-4.md`, `routing.md` · `agents/framer.md`, `agents/smith.md`,
  `agents/sealer.md` (diffs) · `hooks/implementer.py`,
  `hooks/implementer-mark.py`, `hooks/implementer-notice.py`,
  `hooks/routing.py` · `templates/sdd-routing.md`, `templates/sdd-plan.md`,
  `templates/sdd-questions.md` (diffs) · `skills/implement/SKILL.md`,
  `skills/implement/orchestration.md`, `skills/feature-planner/SKILL.md`,
  `skills/confidence-check/SKILL.md` (diffs) · `README.md`, `README.ko.md`,
  `docs/flow.md`, `docs/review-chain-spec.md:140-175` and `:1448-1480`,
  `docs/one-root-by-lifetime.md`, `docs/one-root-by-lifetime.ko.md` ·
  `CLAUDE.md:110-130`, `CONTRIBUTING.md:98-130` · `seal/config.md`,
  `seal/follow-up.md:58-70`, `seal/ledger.md` (changed rows),
  `seal/ledger/1789081272-the-writer-of-the-contract-is-not-its-executor.md` ·
  `.github/workflows/test.yml`, `.github/workflows/hygiene.yml`,
  `skills/evidence-check/scripts/evidence_check.py` (exit branches),
  `bin/test` · `tests/test_a_question_says_who_can_answer_it.py`,
  `tests/test_the_records_can_be_carried_out_and_in.py`,
  `tests/test_a_rider_reaches_its_file.py`, `tests/test_docs_line_wrap.py`,
  `tests/test_one_word_one_meaning.py` (diffs)
- executed — the fifteen rows of §*Executed probes*, every exit code read
  directly and never through a pipe
- read, not executed — the builder's red-first demonstrations for the 40 cases
  and the 39 mutations, except the five I re-ran myself above; the ruff runs the
  handoff reports; the ruleset readings
- unverified — the broad gate, answerer the orchestrator through the sealer
- probe — one file, `tests/test_tmp_notice_at_the_declaring_commit.py`, written
  in the clone, run once, deleted. The clone's `git status` is clean; no
  worktree, branch or checkout was left behind. Nothing was written in the
  working checkout except this report.
